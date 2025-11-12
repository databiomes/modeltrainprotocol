from dataclasses import dataclass
from typing import Collection

from model_train_protocol import NumToken, Instruction, ExtendedInstruction
from model_train_protocol.common.constants import BOS_TOKEN, RUN_TOKEN, EOS_TOKEN
from model_train_protocol.common.instructions import BaseInstruction


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
        
        def to_json(self) -> dict[str, str]:
            """Extracts tokens from stored instructions and converts to JSON-serializable dictionary."""

            token_mapping: dict[str, str] = {}
            
            for instruction in self.instructions_list:
                for token_set in instruction.get_token_sets():
                    token_value = "".join([t.value for t in token_set])
                    token_key = "".join([
                        t.key + (t.protocol_representation if isinstance(t, NumToken) else "")
                        for t in token_set
                    ])
                    
                    token_mapping[token_value] = token_key
                token_mapping[instruction.final.value] = instruction.final.key

            return dict(sorted(token_mapping.items()))
        
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
                input_dict = {"<BOS>": BOS_TOKEN.key}
                
                for idx, token_set in enumerate(instruction.get_token_sets()):
                    token_key = "".join([
                        t.key + (t.protocol_representation if isinstance(t, NumToken) else "")
                        for t in token_set
                    ])
                    
                    token_value = "".join([t.value for t in token_set])
                    is_last_context = idx == len(instruction.get_token_sets()) - 1
                    is_user_prompt = isinstance(instruction, ExtendedInstruction) and is_last_context
                    
                    if is_user_prompt:
                        token_key += "<prompt>"
                    token_key += "\n"
                    
                    if not is_last_context:
                        token_key += "<string>"
                    
                    input_dict[str(idx)] = {token_value: token_key}
                
                input_dict["<RUN>"] = RUN_TOKEN.key
                
                # Build input string from structure
                input_parts = [BOS_TOKEN.key]
                for idx, token_set in enumerate(instruction.get_token_sets()):
                    token_key = "".join([
                        t.key + (t.protocol_representation if isinstance(t, NumToken) else "")
                        for t in token_set
                    ])
                    input_parts.append(token_key)
                    
                    is_last_context = idx == len(instruction.get_token_sets()) - 1
                    is_user_prompt = isinstance(instruction, ExtendedInstruction) and is_last_context
                    
                    if is_user_prompt:
                        input_parts.append("<prompt>")
                    elif not is_last_context:
                        input_parts.append("<string>")
                
                input_parts.append(RUN_TOKEN.key)
                input_str = "\n".join(input_parts)
                
                output_str = "<string>\n" + instruction.final.key + "\n" + EOS_TOKEN.key

                instructions_dict[instruction.name] = {
                    "type": isinstance(instruction, ExtendedInstruction) and "extended" or "basic",
                    "structure": input_dict,
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

    def _create_sample_model_output(self, instruction: BaseInstruction) -> str:
        """Creates a sample model output string for a given instruction."""

        sample_output = "<string>\n"
        sample_output += instruction.final.key + "\n"
        sample_output += EOS_TOKEN.key
        return sample_output

    def _create_examples(self) -> dict[str, str]:
        """Creates example usages of the template."""

        examples: dict[str, str] = dict()
        simple_instruction: Instruction = next(
            (i for i in self.instructions.instructions_list if isinstance(i, Instruction)), None)
        user_instruction: ExtendedInstruction = next(
            (i for i in self.instructions.instructions_list if isinstance(i, ExtendedInstruction)), None)

        if simple_instruction:
            simple_input = BOS_TOKEN.key + "\n"
            for token_set in simple_instruction.get_token_sets():
                token_keys = "".join([token.key for token in token_set])
                simple_input += token_keys + "\n"
                simple_input += "<string>\n"
            simple_input += RUN_TOKEN.key + "\n"
            examples["simple_instruction_input"] = simple_input + self._create_sample_model_output(simple_instruction)

        if user_instruction:
            user_input = BOS_TOKEN.key + "\n"
            token_sets = user_instruction.get_token_sets()
            for idx, token_set in enumerate(token_sets):
                token_keys = "".join([token.key for token in token_set])
                user_input += token_keys + "\n"
                if idx != len(token_sets) - 1:
                    user_input += "<string>\n"
                else:
                    user_input += "<prompt>\n"
            user_input += RUN_TOKEN.key + "\n"
            examples["user_instruction_input"] = user_input

        first_instruction = simple_instruction or user_instruction
        if first_instruction:
            examples["valid_model_output"] = self._create_sample_model_output(first_instruction)

        return examples

    def to_json(self) -> dict:
        """Converts the entire template to a JSON-serializable dictionary."""

        examples: dict[str, str] = self._create_examples()
        json_dict: dict = {
            "version": "0.1",       # Version is hardcoded for now; update as needed
            "encrypt": self.encrypt,
            "tokens": self.tokens.to_json(),
            "instructions": self.instructions.to_json(),
            "example_usage": examples
        }
        return json_dict
