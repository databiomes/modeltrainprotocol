from dataclasses import dataclass
from typing import Collection

from model_train_protocol import NumToken
from model_train_protocol.common.constants import BOS_TOKEN, RUN_TOKEN, EOS_TOKEN
from model_train_protocol.common.instructions import Instruction


class TemplateFile:
    """Manages the model.json file for model training protocols."""

    @dataclass
    class ExampleUsage:
        """Stores example usages of the template."""

        valid_simple_input: str
        valid_user_input: str
        valid_output: str

        guardrail_input: str
        guardrail_output: str

    class ModelInput:
        """Represents inputs to the model."""

        inputs: list[list[str]] = list()

        def add_inputs_from_instructions(self, instructions: list[Instruction], context_lines: int):
            """Adds input combinations from a list of instructions."""
            unique_sets = {i: set() for i in range(context_lines)}
            for instruction in instructions:
                for idx, token_set in enumerate(instruction.get_token_sets()):
                    token_user = [t.user for t in token_set]
                    token_strings = "".join([t.value for t in token_set])
                    token_keys = []
                    for token in token_set:
                        token_keys.append(token.key + (token.protocol_representation if isinstance(token, NumToken) else ""))
                    token_keys = "".join(token_keys)
                    unique_sets[idx].add(str(token_strings) + ": " + (
                        (str(token_keys) + "USER PROMPT") if any(token_user) and (
                                    idx == (len(unique_sets) - 1)) else str(
                            token_keys)) + "\n" + ("<string>" if idx != (len(instruction.context) - 1) else ""))

            for input_set in unique_sets.values():
                self.inputs.append(list(input_set))

        def to_json(self):
            """Converts the model input to a JSON-serializable dictionary."""
            model_json: dict[str, Collection[str] | str] = {"<BOS>": BOS_TOKEN.key}
            # Add each input sequence with its index as the key
            for idx, input_seq in enumerate(self.inputs):
                model_json[str(idx)] = input_seq
            model_json["<RUN>"] = RUN_TOKEN.key
            return model_json

    class ModelOutput:
        model_results: dict[str, str] = dict()
        model_response: str = "<string>"

        def __setitem__(self, key: str, value: str):
            self.model_results[key] = value

        def add_results_from_instructions(self, instructions: list[Instruction]):
            """Adds model results from a list of instructions."""
            for instruction in instructions:
                self.model_results[str(instruction.final.value)] = str(instruction.final.key)

        def to_json(self):
            """Converts the model output to a JSON-serializable dictionary."""
            model_json: dict[str, dict[str] | str] = {
                "model_response": self.model_response,
                "model_results": {}
            }
            # Add each model result with its key
            for key, value in self.model_results.items():
                model_json["model_results"][key] = value

            model_json["<EOS>"] = EOS_TOKEN.key
            return model_json

    def __init__(self, context_lines: int, instructions: list[Instruction], ):
        """Initializes the template"""
        self.model_input: TemplateFile.ModelInput = TemplateFile.ModelInput()
        self.model_output: TemplateFile.ModelOutput = TemplateFile.ModelOutput()
        self.context_lines: int = context_lines
        self.instructions: list[Instruction] = instructions
        self._add_io_from_instructions()

    def _add_io_from_instructions(self):
        """Adds input and output sequences from the instructions."""
        self.model_input.add_inputs_from_instructions(self.instructions, context_lines=self.context_lines)
        self.model_output.add_results_from_instructions(self.instructions)

    def to_json(self) -> dict:
        """Converts the entire template to a JSON-serializable dictionary."""
        return {
            "all_combinations": {
                "model_input": self.model_input.to_json(),
                "model_output": self.model_output.to_json()
            }
        }
