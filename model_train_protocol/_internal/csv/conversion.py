from dataclasses import dataclass

import pandas as pd

from model_train_protocol import FinalToken, Protocol, Token, InstructionInput, TokenSet, Instruction, InstructionOutput
from model_train_protocol.common.constants import NON_TOKEN


@dataclass
class CSVLine:
    """This class represents a single line in the CSV data."""
    id: int
    group: str
    input_str: str
    output_str: str
    context_str: str
    requires_str: str


class CSVConversion:
    """This class provides methods to convert from CSV into MTP"""
    group_col: str = "Group"
    input_col: str = "Input"
    output_col: str = "Output"
    context_col: str = "Output Reference"
    required_col: str = "Requires"

    input_token: Token = Token("Input")
    required_token: Token = Token("Required")
    input_tokenset: TokenSet = TokenSet(tokens=[input_token])
    required_tokenset: TokenSet = TokenSet(tokens=[required_token])
    standard_input: InstructionInput = InstructionInput(tokensets=[input_tokenset, required_tokenset])

    def __init__(self, csv_data: pd.DataFrame):
        """
        Initializes the CSVConversion instance.

        :param csv_data: A dictionary where keys are column names and values are lists of column data.
        """
        self.csv_data = csv_data
        self.csv_data.index += 1 # Adjust index to start from 1 to match CSV index
        self.instruction_idx: dict[str, list[int]] = self._summarize_instructions()
        self.line_by_id: dict[int, CSVLine] = self._identify_lines()
        self.protocol: Protocol = Protocol(name="CSV Protocol", inputs=2, encrypt=False)

    def to_mtp(self) -> Protocol:
        """Converts the CSV data to MTP format."""
        for instruction, idxs in self.instruction_idx.items():
            self._process_instruction(instruction, idxs)
        return self.protocol

    def _summarize_instructions(self) -> dict[str, list[int]]:
        """
        Summarizes the instructions in the CSV data.

        Creates a dictionary with instruction names as keys and their occurrences by index
        """
        instruction_counts: dict[str, list[int]] = {}
        groups: pd.Series = self.csv_data[self.group_col]
        for idx, instruction in enumerate(groups):
            idx += 1  # Adjust index to match CSV line numbering
            if instruction not in instruction_counts:
                instruction_counts[str(instruction)] = []
            instruction_counts[str(instruction)].append(idx)
        return instruction_counts

    def _identify_lines(self) -> dict[int, CSVLine]:
        """
        Maps lines in the CSV data by their ID.

        :return: A dictionary mapping line IDs to CSVLine objects.
        """
        line_by_id: dict[int, CSVLine] = {}
        groups_column: pd.Series = self.csv_data[self.group_col]
        inputs_column: pd.Series = self.csv_data[self.input_col]
        outputs_column: pd.Series = self.csv_data[self.output_col]
        contexts_column: pd.Series = self.csv_data[self.context_col]
        requires_column: pd.Series = self.csv_data[self.required_col]

        for idx in range(len(inputs_column)):
            idx += 1  # Adjust index to match CSV line numbering
            line_id: int = idx
            line_by_id[line_id] = CSVLine(
                id=line_id,
                group=groups_column[idx],
                input_str=inputs_column[idx],
                output_str=outputs_column[idx],
                context_str=contexts_column[idx],
                requires_str=requires_column[idx]
            )
        return line_by_id

    def _process_instruction(self, instruction: str, idxs: list[int]) -> None:
        """
        Processes a single instruction and adds it to the protocol.

        :param instruction: The instruction name.
        :param idxs: List of indices where this instruction occurs in the CSV data.
        """
        first_line: CSVLine = self.line_by_id.get(idxs[0])
        instruction_token: Token = Token(first_line.group)
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

        for idx in idxs:
            input_str: str = str(self.csv_data['Input'][idx])
            output_str: str = str(self.csv_data['Output'][idx])
            context_str: str = str(self.csv_data['Output Reference'][idx])
            requires_str: str = str(self.csv_data['Requires'][idx])

            required_samples: list[str] = []

            if context_str != "" and context_str != "nan":
                instruction.add_context(context_str)

            # Add any required outputs
            if requires_str != "" and requires_str != "nan":
                required_idxs: list[int] = [int(i) for i in requires_str.split(",") if i.isdigit()]
                for req_idx in required_idxs:
                    required_line: CSVLine = self.line_by_id.get(req_idx)
                    if required_line:
                        required_samples.append(required_line.output_str)

            first_input: str = ", ".join(required_samples) if required_samples else NON_TOKEN.value

            instruction.add_sample(
                input_snippets=[first_input, input_str],
                output_snippet=output_str
            )

        self.protocol.add_instruction(instruction)




    def _get_unique_outputs(self, idxs: list[int]) -> set[FinalToken]:
        """
        Retrieves unique outputs for a given instruction.

        :param idxs: List of indices where the instruction occurs.
        :return: A set of unique outputs.
        """
        unique_outputs: set[FinalToken] = set()
        outputs_column: pd.Series = self.csv_data['Output']
        for idx in idxs:
            output = outputs_column[idx]
            unique_outputs.add(FinalToken(output))
        return unique_outputs
