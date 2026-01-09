from abc import ABC
from typing import List

from model_train_protocol.common.guardrails import Guardrail
from model_train_protocol.common.tokens import TokenSet


class BaseInput(ABC):
    """Defines a BaseInput for modularity and future extension."""

    def __init__(self, context: List[str] | None, tokensets: List[TokenSet]):
        """
        Initializes the InstructionInput with an instruction and optional input data.

        :param context: A list of strings providing background context for the instruction.
        :param tokensets: A list of TokenSet in the order that they appear in the instruction.
        """
        if context is None:
            context = []
        self.context: List[str] = context
        self.tokensets = tokensets
        self.guardrails: dict[int, Guardrail] = {}

    def __len__(self):
        return len(self.context)

    def add_guardrail(self, guardrail: Guardrail, tokenset_index: int):
        """
        Adds a guardrail to the InstructionInput.

        :param guardrail: The Guardrail instance to add.
        :param tokenset_index: The index of the TokenSet the guardrail applies to.
        """
        if tokenset_index < 0:
            raise ValueError(f"tokenset_index {tokenset_index} is out of range for the Instruction input tokensets.")
        if tokenset_index > len(self.tokensets) - 1:
            raise ValueError(f"tokenset_index {tokenset_index} is out of range of the Instruction input tokensets.")
        if tokenset_index in self.guardrails:
            raise ValueError(f"A guardrail is already defined for tokenset_index {tokenset_index}.")

        self.guardrails[tokenset_index] = guardrail

    def __str__(self):
        """Combines all TokenSets to form a string representation of the Input."""
        return f"Input(TokenSets={self.tokensets})"