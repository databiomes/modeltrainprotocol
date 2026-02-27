from abc import ABC
from typing import List

from model_train_protocol.common.guardrails import Guardrail
from model_train_protocol.common.tokens import TokenSet
from model_train_protocol.errors import DuplicateGuardrailError, GuardrailIndexError


class BaseInput(ABC):
    """Defines a BaseInput for modularity and future extension."""

    def __init__(self, tokensets: List[TokenSet]):
        """
        Initializes the InstructionInput with an instruction and optional input data.

        :param tokensets: A list of TokenSet in the order that they appear in the instruction.
        """
        self.tokensets = tokensets
        self.guardrails: dict[int, Guardrail] = {}

    def add_guardrail(self, guardrail: Guardrail, tokenset_index: int):
        """
        Adds a guardrail to the InstructionInput.

        :param guardrail: The Guardrail instance to add.
        :param tokenset_index: The index of the TokenSet the guardrail applies to.
        """
        if tokenset_index < 0:
            raise GuardrailIndexError(
                f"tokenset_index {tokenset_index} is out of range for the Instruction input tokensets."
            )
        if tokenset_index > len(self.tokensets) - 1:
            raise GuardrailIndexError(
                f"tokenset_index {tokenset_index} is out of range of the Instruction input tokensets."
            )
        if tokenset_index in self.guardrails:
            raise DuplicateGuardrailError(
                f"A guardrail is already defined for tokenset_index {tokenset_index}."
            )

        self.guardrails[tokenset_index] = guardrail

    def __str__(self):
        """Combines all TokenSets to form a string representation of the Input."""
        return f"Input(TokenSets={self.tokensets})"