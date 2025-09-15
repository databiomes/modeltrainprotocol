from dataclasses import dataclass, field
from typing import Collection

from model_train_protocol import Token, NumToken
from model_train_protocol.common.guardrails import Guardrail
from model_train_protocol.common.instructions import Instruction
from model_train_protocol.common.tokens import TokenSet, SpecialToken


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

    @dataclass
    class ModelInput:
        """Represents inputs to the model."""

        inputs: list[list[str]]
        input_count: int
        bos: str = "<BOS>"
        run: str = "<RUN>"

    @dataclass
    class ModelOutput:
        model_response: str
        model_results: dict[str, str]
        eos: str = "<EOS>"

    def __init__(self, instruction_sample_lines: int, instructions: list[Instruction],):
        """Initializes the template"""

    def to_json(self):
        """Converts the template to a JSON-compatible dictionary."""
        json_dict = {
            "name": self._name,
            "context": self._context,
            "tokens": self._tokens,
            "special_tokens": list(self._special_token_keys | self._instruction_token_keys),
            "instruction": {
                "memory": self._instruction.memory,
                "sets": [vars(s) for s in self._instruction.sets],
            },
            "guardrails": self._guardrails,
            "numbers": self._numbers,
            "batches": {
                "pretrain": self._batches.pretrain,
                "instruct": self._batches.instruct,
                "judge": self._batches.judge,
                "ppo": self._batches.ppo,
            },
        }

        return self._rename_protocol_elements(json_dict)
