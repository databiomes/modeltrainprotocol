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
    required_token: Token = Token("Required", desc="")
    input_tokenset: TokenSet = TokenSet(tokens=[input_token])
    required_tokenset: TokenSet = TokenSet(tokens=[required_token])
    standard_input: InstructionInput = InstructionInput(tokensets=[input_tokenset, required_tokenset])

    def __init__(self, csv_data: pd.DataFrame):
        """
        Initializes the CSVConversion instance.

        :param csv_data: A dictionary where keys are column names and values are lists of column data.
        """
        self.csv_data = self._process_dataframe(csv_data)
        self.rows_by_group: dict[str, list[str]] = self._summarize_instructions()
        self.line_by_id: dict[str, CSVLine] = self._identify_lines()  # Todo: make linked list
        self.protocol: Protocol = Protocol(name="CSV Protocol", inputs=2, encrypt=False)

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

        # Remove rows with empty Group values
        dataframe = dataframe[dataframe[self.group_col].notna()]
        dataframe.reset_index(drop=True)
        return dataframe

    def _summarize_instructions(self) -> dict[str, list[str]]:
        """
        Summarizes the instructions in the CSV data.

        Creates a dictionary with instruction names as keys and their occurrences by index
        """
        instruction_counts: dict[str, list[str]] = {}
        for row in self.csv_data.itertuples():
            instruction: str = str(getattr(row, self.group_col))
            if instruction == "" or instruction == "nan":
                continue
            if instruction not in instruction_counts:
                instruction_counts[str(instruction)] = []
            instruction_counts[str(instruction)].append(str(getattr(row, self.id_col)))
        return instruction_counts

    def _identify_lines(self) -> dict[str, CSVLine]:
        """
        Maps lines in the CSV data by their ID.

        :return: A dictionary mapping line IDs to CSVLine objects.
        """
        line_by_id: dict[str, CSVLine] = {}
        id_column: pd.Series = self.csv_data[self.id_col]
        groups_column: pd.Series = self.csv_data[self.group_col]
        inputs_column: pd.Series = self.csv_data[self.input_col]
        outputs_column: pd.Series = self.csv_data[self.output_col]
        contexts_column: pd.Series = self.csv_data[self.context_col]
        requires_column: pd.Series = self.csv_data[self.required_col]

        for idx, line_id in enumerate(id_column):
            idx += 1  # Adjust index to match CSV line numbering
            if self.first_id is None:
                self.first_id = str(line_id)
            line_by_id[str(line_id)] = CSVLine(
                id=str(line_id),
                group=groups_column[idx],
                input_str=inputs_column[idx],
                output_str=outputs_column[idx],
                context_str=contexts_column[idx],
                requires_str=requires_column[idx]
            )
        return line_by_id

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
                                         desc=f"Here are Inputs that are acceptable: {acceptable_output_string}. "
                                              f"Try to match inputs from examples with the same responses from the examples.")
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
            required_samples: list[str] = []

            if line.context_str != "" and not pd.isna(line.context_str):
                instruction.add_context(line.context_str)

            # Add any required outputs
            if line.requires_str != "" and not pd.isna(line.requires_str):
                required_ids: list[str] = [i for i in line.requires_str.split(",")]
                for req_id in required_ids:
                    required_line: CSVLine = self.line_by_id.get(req_id)
                    if required_line:
                        required_samples.append(required_line.output_str)

            first_input: str = ", ".join(required_samples) if required_samples else NON_TOKEN.value

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
