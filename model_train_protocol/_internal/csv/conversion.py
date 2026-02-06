from dataclasses import dataclass

import pandas as pd

from model_train_protocol import Protocol, Token, InstructionInput, TokenSet, Instruction, InstructionOutput
from model_train_protocol.common.constants import NON_TOKEN


@dataclass
class CSVLine:
    """This class represents a single line in the CSV data."""
    id: str
    group: str
    input_str: str
    output_str: str
    context_str: str
    requires_str: str


class CSVConversion:
    """This class provides methods to convert from CSV into MTP"""
    id_col: str = "ID"
    group_col: str = "Group"
    input_col: str = "Input"
    output_col: str = "Output"
    context_col: str = "Output Reference"
    required_col: str = "Requires"

    input_token: Token = Token("Input")
    input_tokenset: TokenSet = TokenSet(tokens=[input_token])

    def __init__(self, csv_data: pd.DataFrame):
        """
        Initializes the CSVConversion instance.

        :param csv_data: A dictionary where keys are column names and values are lists of column data.
        """
        self.csv_data = self._process_dataframe(csv_data)
        self.rows_by_group: dict[str, list[str]] = self._summarize_instructions()
        self.line_by_id: dict[str, CSVLine] = self._identify_lines()
        self.protocol: Protocol = Protocol(name="CSV Protocol", inputs=2, encrypt=False)
        self.required_token: Token = self._generate_required_token()
        self.required_tokenset: TokenSet = TokenSet(tokens=[self.required_token])
        self.standard_input: InstructionInput = InstructionInput(tokensets=[self.required_tokenset, self.input_tokenset])

    def to_mtp(self) -> Protocol:
        """Converts the CSV data to MTP format."""
        for instruction, ids in self.rows_by_group.items():
            self._process_instruction(instruction, ids)
        return self.protocol

    def _process_dataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Processes the input DataFrame to match expected format.

        :param dataframe: The input DataFrame.
        :return: Processed DataFrame
        """
        # Remove the descriptions row from the DataFrame, if present
        if pd.isna(dataframe.iloc[0][self.id_col]):
            dataframe = dataframe.drop(0)

        # Remove rows where Group and Input are empty
        dataframe = dataframe[~((dataframe[self.group_col].isna()) & (dataframe[self.input_col].isna()))]
        dataframe.reset_index(drop=True)
        return dataframe

    def _summarize_instructions(self) -> dict[str, list[str]]:
        """
        Summarizes the instructions in the CSV data.

        Creates a dictionary with instruction names as keys and their occurrences by index
        """
        instruction_counts: dict[str, list[str]] = {}
        latest_group: str = ""
        for row in self.csv_data.itertuples():
            input_str: str = str(getattr(row, self.input_col))
            if input_str == "" or input_str == "nan":
                continue
            latest_group: str = self._assign_latest(self.csv_data[self.group_col], row.Index, latest_group)
            if latest_group not in instruction_counts:
                instruction_counts[str(latest_group)] = []
            instruction_counts[str(latest_group)].append(str(getattr(row, self.id_col)))
        return instruction_counts

    def _identify_lines(self) -> dict[str, CSVLine]:
        """
        Maps lines in the CSV data by their ID.

        :return: A dictionary mapping line IDs to CSVLine objects.
        """
        latest_group: str = ""
        latest_output: str = ""
        latest_context: str = ""
        line_by_id: dict[str, CSVLine] = {}
        id_column: pd.Series = self.csv_data[self.id_col]
        groups_column: pd.Series = self.csv_data[self.group_col]
        inputs_column: pd.Series = self.csv_data[self.input_col]
        outputs_column: pd.Series = self.csv_data[self.output_col]
        contexts_column: pd.Series = self.csv_data[self.context_col]
        requires_column: pd.Series = self.csv_data[self.required_col]

        for idx, line_id in enumerate(id_column):
            idx += 1  # Adjust index to match CSV line numbering
            latest_group: str = self._assign_latest(groups_column, idx, latest_group)
            latest_output: str = self._assign_latest(outputs_column, idx, latest_output)
            latest_context: str = self._assign_latest(contexts_column, idx, latest_context)

            line_by_id[str(line_id)] = CSVLine(
                id=str(line_id),
                group=latest_group,
                input_str=inputs_column[idx],
                output_str=latest_output,
                context_str=latest_context,
                requires_str=requires_column[idx]
            )
        return line_by_id

    def _generate_required_token(self) -> Token:
        """Generates the required token for the protocol."""
        required_outputs: set[str] = set()
        for line in self.line_by_id.values():
            if line.requires_str != "" and not pd.isna(line.requires_str):
                required_ids: list[str] = [i for i in line.requires_str.split(",")]
                for req_id in required_ids:
                    required_line: CSVLine = self.line_by_id.get(req_id)
                    if required_line:
                        required_outputs.add(required_line.output_str)
                    else:
                        raise ValueError(f"Required ID {req_id} not found in CSV data.")

        desc: str = f"Here are previous responses that are acceptable: f{', '.join(required_outputs)}. If a previous response is given then the new response must match the example."

        return Token(value="Required", desc=desc)

    @classmethod
    def _assign_latest(cls, column: pd.Series, idx: int, latest: str) -> str:
        """Helper function to assign latest non-empty value."""
        try:
            value: str = str(column[idx])
        except KeyError:
            return latest
        if value == "" or value == "nan" or pd.isna(value):
            return latest
        return value

    def _process_instruction(self, instruction: str, ids: list[str]) -> None:
        """
        Processes a single instruction and adds it to the protocol.

        :param instruction: The instruction name.
        :param ids: List of IDs where the instruction occurs.
        """
        first_line_in_instruction: CSVLine = self.line_by_id[ids[0]]
        instruction_outputs: set[str] = self._get_unique_outputs(ids)
        acceptable_output_string: str = ", ".join(instruction_outputs)
        instruction_token: Token = Token(first_line_in_instruction.group,
                                         desc=f"The responses that are acceptable: {acceptable_output_string}.")
        instruction_tokenset: TokenSet = TokenSet(tokens=[instruction_token])
        instruction_output: InstructionOutput = InstructionOutput(
            tokenset=instruction_tokenset,
            final=NON_TOKEN
        )

        instruction: Instruction = Instruction(
            input=self.standard_input,
            output=instruction_output,
            name=instruction
        )

        for _id in ids:
            line: CSVLine = self.line_by_id[_id]
            if line.context_str != "" and not pd.isna(line.context_str):
                instruction.add_context(line.context_str)

            # Add any required outputs
            previous_response: str = NON_TOKEN.value

            if line.requires_str != "" and not pd.isna(line.requires_str):
                required_id: str = line.requires_str
                required_line: CSVLine = self.line_by_id.get(required_id)
                if required_line:
                    previous_response: str = required_line.output_str

            first_input: str = f"Based on the prompt, choose an answer that best fits. Previous answer was {previous_response}."

            instruction.add_sample(
                input_snippets=[first_input, line.input_str],
                output_snippet=line.output_str
            )

        self.protocol.add_instruction(instruction)

    def _get_unique_outputs(self, ids: list[str]) -> set[str]:
        """
        Retrieves unique outputs for a given instruction.

        :param ids: List of IDs where the instruction occurs.
        :return: A set of unique outputs.
        """
        unique_outputs: set[str] = set()
        for _id in ids:
            line: CSVLine = self.line_by_id[_id]
            unique_outputs.add(line.output_str)
        return unique_outputs
