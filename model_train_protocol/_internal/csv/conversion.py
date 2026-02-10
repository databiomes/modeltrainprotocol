from dataclasses import dataclass

import pandas as pd

from model_train_protocol import Protocol, Token, InstructionInput, TokenSet, Instruction, InstructionOutput, Guardrail
from model_train_protocol.common.constants import NON_TOKEN


@dataclass
class CSVLine:
    """This class represents a single line in the CSV data."""
    id: str
    input_str: str
    output_str: str
    context_str: str
    requires_str: str

    @property
    def is_guardrail(self) -> bool:
        """Determines if the line is a guardrail based on its content."""
        return self.output_str == "GUARDRAIL"


class CSVConversion:
    """This class provides methods to convert from CSV into MTP"""
    instruction_name: str = "Output"
    id_col: str = "ID"
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
        self.line_by_id: dict[str, CSVLine] = self._identify_lines()
        self.protocol: Protocol = Protocol(name="CSV Protocol", inputs=2, encrypt=False)
        self.required_token: Token = self._generate_required_token()
        self.required_tokenset: TokenSet = TokenSet(tokens=[self.required_token])
        self.standard_input: InstructionInput = InstructionInput(
            tokensets=[self.required_tokenset, self.input_tokenset])

    def to_mtp(self) -> Protocol:
        """Converts the CSV data to MTP format."""
        ids: list[str] = list(self.line_by_id.keys())
        self._process_instruction(self.instruction_name, ids)
        return self.protocol

    def get_required_map(self) -> dict:
        """Creates a map of the required tokens"""
        required_map: dict[str, str] = {}
        for line in self.line_by_id.values():
            if line.requires_str != "" and not pd.isna(line.requires_str):
                required_id: str = line.requires_str
                required_line: CSVLine = self.line_by_id.get(required_id)
                if not required_line:
                    raise ValueError(f"Required ID {required_id} not found in CSV data.")
                required_map[line.output_str] = required_line.output_str
        return required_map

    def _process_dataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Processes the input DataFrame to match expected format.

        :param dataframe: The input DataFrame.
        :return: Processed DataFrame
        """
        # Remove the descriptions row from the DataFrame, if present
        if pd.isna(dataframe.iloc[0][self.id_col]):
            dataframe = dataframe.drop(0)

        # Remove rows where Input is empty
        dataframe = dataframe[~(dataframe[self.input_col].isna())]
        dataframe.reset_index(drop=True)
        return dataframe

    def _identify_lines(self) -> dict[str, CSVLine]:
        """
        Maps lines in the CSV data by their ID.

        :return: A dictionary mapping line IDs to CSVLine objects.
        """
        latest_output: str = ""
        line_by_id: dict[str, CSVLine] = {}
        id_column: pd.Series = self.csv_data[self.id_col]
        inputs_column: pd.Series = self.csv_data[self.input_col]
        outputs_column: pd.Series = self.csv_data[self.output_col]
        context_column: pd.Series = self.csv_data[self.context_col]
        requires_column: pd.Series = self.csv_data[self.required_col]

        for idx, line_id in enumerate(id_column):
            idx += 1  # Adjust index to match CSV line numbering
            latest_output: str = self._assign_latest(outputs_column, idx, latest_output)

            line_by_id[str(line_id)] = CSVLine(
                id=str(line_id),
                input_str=inputs_column[idx],
                output_str=latest_output,
                context_str=context_column[idx],
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

        desc: str = f"Here are previous responses that are acceptable: {', '.join(required_outputs)}. If a previous response is given then the new response must match the example."

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
        instruction_outputs: set[str] = self._get_unique_outputs(ids)
        acceptable_output_string: str = ", ".join(instruction_outputs)
        instruction_token: Token = Token(self.instruction_name,
                                         desc=f"The responses that are acceptable: {acceptable_output_string}.")
        instruction_tokenset: TokenSet = TokenSet(tokens=[instruction_token])
        instruction_output: InstructionOutput = InstructionOutput(
            tokenset=instruction_tokenset,
            final=NON_TOKEN
        )

        guardrail = Guardrail(
            good_prompt="Prompt related to the provided context of the model",
            bad_prompt="Prompt that is irrelevant and off topic",
            bad_output="GUARDRAIL"
        )

        instruction: Instruction = Instruction(
            input=self.standard_input,
            output=instruction_output,
            name=instruction
        )

        for _id in ids:
            line: CSVLine = self.line_by_id[_id]

            if line.is_guardrail:
                guardrail.add_sample(line.input_str)
                continue

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

        if 0 < len(guardrail.samples) < 3:
            raise ValueError(
                "At least 3 guardrail samples are required. Please add more guardrail samples to the CSV data.")
        elif len(guardrail.samples) >= 3:
            instruction.add_guardrail(guardrail=guardrail, tokenset_index=1)

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
