from dataclasses import dataclass

from model_train_protocol import Instruction, ExtendedInstruction
from model_train_protocol.common.constants import BOS_TOKEN, RUN_TOKEN, EOS_TOKEN
from model_train_protocol.common.instructions import BaseInstruction
from model_train_protocol.common.instructions.BaseInstruction import Sample
from model_train_protocol.common.tokens import FinalToken
from model_train_protocol.common.tokens import NumToken, NumListToken
import random

class TemplateFile:
    """Manages the model.json file for model training protocols."""

    @dataclass
    class ExampleUsage:
        """Stores example usages of the template."""

        input: str
        output: str

    class Tokens:
        """Represents all tokens used in the template."""

        def __init__(self):
            self.instructions_list: list[BaseInstruction] = []

        def add_tokens_from_instructions(self, instructions: list[BaseInstruction]):
            """Stores instruction data for later token extraction."""

            self.instructions_list = instructions

        def to_json(self) -> dict[str, dict[str, str]]:
            """Extracts tokens from stored instructions and converts to JSON-serializable dictionary."""

            input_token_mapping: dict[str, str] = {}
            output_token_mapping: dict[str, str] = {}

            for instruction in self.instructions_list:
                for token_set in instruction.get_token_sets():
                    token_value = "".join([t.value for t in token_set])
                    token_key = "".join([
                        t.key + t.template_representation for t in token_set
                    ])

                    # Check if any token in the token_set is a FinalToken
                    has_final_token = any(isinstance(t, FinalToken) for t in token_set)
                    
                    if has_final_token:
                        output_token_mapping[token_value] = token_key
                    else:
                        input_token_mapping[token_value] = token_key
                
                for sample in instruction.samples:
                    output_token_mapping[sample.result.value] = sample.result.key
            
            output_token_mapping[EOS_TOKEN.value] = EOS_TOKEN.key

            return {
                "input": dict(sorted(input_token_mapping.items())),
                "output": dict(sorted(output_token_mapping.items()))
            }

    class Instructions:
        """Represents the instruction set of the template."""

        def __init__(self):
            self.instructions_list: list[BaseInstruction] = []

        def add_inputs_from_instructions(self, instructions: list[BaseInstruction]):
            """Stores instruction data for later JSON conversion."""

            self.instructions_list = instructions

        def to_json(self):
            """Converts stored instructions to JSON-serializable dictionary."""

            instructions_dict: dict[str, dict] = {}

            for instruction in self.instructions_list:
                input_list: list[str] = [BOS_TOKEN.key + '\n']
                for idx, token_set in enumerate(instruction.get_token_sets()):
                    token_key = "".join([
                        t.key + t.template_representation for t in token_set
                    ])

                    is_last_context = idx == len(instruction.get_token_sets()) - 1
                    is_extended_instruction_extra_string = isinstance(instruction,
                                                                      ExtendedInstruction) and is_last_context

                    if is_extended_instruction_extra_string:
                        token_key += "<string>"

                    token_key += "\n"

                    if not is_last_context:
                        token_key += "<string>"

                    input_list.append(token_key)

                input_list.append(RUN_TOKEN.key)

                # Build input string from structure
                input_parts = [BOS_TOKEN.key]
                for idx, token_set in enumerate(instruction.get_token_sets()):

                    is_last_context = idx == len(instruction.get_token_sets()) - 1
                    is_extended_instruction_extra_string = isinstance(instruction,
                                                                      ExtendedInstruction) and is_last_context

                    token_key = "".join([
                        t.key + t.template_representation for t in token_set
                    ])

                    if is_extended_instruction_extra_string:
                        token_key += "<string>" # Extra <string> for extended instruction embedded in key

                    input_parts.append(token_key)

                    if not is_last_context:
                        input_parts.append("<string>")

                input_parts.append(RUN_TOKEN.key)
                input_str = "\n".join(input_parts)

                output_str = "<string>\n" + instruction.response.final[0].key + "\n" + EOS_TOKEN.key

                instructions_dict[instruction.name] = {
                    "type": isinstance(instruction, ExtendedInstruction) and "extended" or "basic",
                    "structure": input_list,
                    "input": input_str,
                    "output": output_str
                }

            return instructions_dict

    def __init__(self, instruction_context_snippets: int, instructions: list[BaseInstruction], encrypt: bool):
        """Initializes the template"""

        self.tokens: TemplateFile.Tokens = TemplateFile.Tokens()
        self.instructions: TemplateFile.Instructions = TemplateFile.Instructions()
        self.instruction_context_snippets: int = instruction_context_snippets
        self.instructions_list: list[BaseInstruction] = instructions
        self.encrypt: bool = encrypt
        self._add_io_from_instructions()

    def _add_io_from_instructions(self):
        """Adds input and output sequences from the instructions."""

        self.tokens.add_tokens_from_instructions(self.instructions_list)
        self.instructions.add_inputs_from_instructions(self.instructions_list)

    @classmethod
    def _format_token_set_with_sample(cls, token_set, sample_string: str, is_extended_last: bool = False) -> str:
        """Formats a token set with actual sample data, including numbers and number lists.
        
        :param token_set: The TokenSet to format
        :param sample_string: The actual sample string to use
        :param is_extended_last: If True, format for extended instruction's last token set (no newline before string)
        """
        token_keys = "".join([token.key for token in token_set])
        
        # Add template representation for NumTokens and NumListTokens to the token key
        for token in token_set:
            if isinstance(token, NumToken):
                example_number: str = str(random.randint(token.min_value, token.max_value))
                token_keys += example_number
            elif isinstance(token, NumListToken):
                example_list: list[str] = [
                    str(random.randint(token.min_value, token.max_value))
                    for _ in range(token.length)
                ]
                token_keys += example_list
        
        if is_extended_last:
            # For extended instruction's last token set: token_key<string>\n (no newline before string)
            formatted_string = token_keys + sample_string + "\n"
        else:
            # For regular format: token_key\n<string>\n
            formatted_string = token_keys + "\n"
            formatted_string += sample_string + "\n"
        
        return formatted_string

    @classmethod
    def _create_sample_model_output(cls, instruction: BaseInstruction, sample: 'Sample') -> str:
        """Creates a sample model output string for a given instruction using actual sample data."""

        sample_output = sample.response + "\n"
        sample_output += instruction.example_final_token.key + "\n"
        sample_output += EOS_TOKEN.key
        return sample_output

    def _create_examples(self) -> dict[str, str]:
        """Creates example usages of the template using actual sample data from instructions."""

        examples: dict[str, str] = dict()
        instruction: Instruction = next(
            (i for i in self.instructions.instructions_list if isinstance(i, Instruction)), None)
        extended_instruction: ExtendedInstruction = next(
            (i for i in self.instructions.instructions_list if isinstance(i, ExtendedInstruction)), None)

        if instruction and instruction.samples:
            # Use the first sample for the example
            sample = instruction.samples[0]
            
            instruction_input = BOS_TOKEN.key + "\n"
            
            # Map context strings to context token sets
            for idx, token_set in enumerate(instruction.context):
                if idx < len(sample.context):
                    sample_string = sample.context[idx]
                    instruction_input += self._format_token_set_with_sample(token_set, sample_string)

            instruction_input += instruction.last_tokenset.key + "\n"

            instruction_input += RUN_TOKEN.key + "\n"
            examples["instruction_input"] = instruction_input

        if extended_instruction and extended_instruction.samples:
            # Use the first sample for the example
            sample = extended_instruction.samples[0]
            
            extended_instruction_input = BOS_TOKEN.key + "\n"
            
            # Map context strings to context token sets
            for idx, token_set in enumerate(extended_instruction.context):
                if idx < len(sample.context):
                    sample_string = sample.context[idx]
                    extended_instruction_input += self._format_token_set_with_sample(token_set, sample_string)
            
            last_tokenset = extended_instruction.last_tokenset  # This is the last TokenSet in the original context
            prompt_string = sample.prompt if sample.prompt else ""
            extended_instruction_input += self._format_token_set_with_sample(last_tokenset, prompt_string, is_extended_last=True)
            
            extended_instruction_input += RUN_TOKEN.key + "\n"
            examples["extended_instruction_input"] = extended_instruction_input

        first_instruction = instruction or extended_instruction
        if first_instruction and first_instruction.samples:
            sample = first_instruction.samples[0]
            examples["valid_model_output"] = self._create_sample_model_output(first_instruction, sample)

        return examples

    def to_json(self) -> dict:
        """Converts the entire template to a JSON-serializable dictionary."""

        json_dict: dict = {
            "version": "0.1",  # Version is hardcoded for now; update as needed
            "encrypt": self.encrypt,
            "tokens": self.tokens.to_json(),
            "instructions": self.instructions.to_json(),
            "example_usage": self._create_examples()
        }
        return json_dict
