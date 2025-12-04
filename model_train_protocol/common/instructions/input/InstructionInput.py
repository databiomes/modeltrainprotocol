from typing import List

from model_train_protocol.common.guardrails import Guardrail
from model_train_protocol.common.instructions.input.BaseInput import BaseInput
from model_train_protocol.common.tokens import TokenSet


class InstructionInput(BaseInput):
    """Defines the structure for instruction inputs."""

    def __init__(self, context: List[str] | None, tokensets: List[TokenSet]):
        """
        Initializes the InstructionInput with an instruction and optional input data.

        :param context: A list of strings providing background context for the instruction.
        :param tokensets: A list of TokenSet in the order that they appear in the instruction.
        """
        super().__init__(context=context, tokensets=tokensets)

    def add_guardrail(self, guardrail: Guardrail, tokenset_index: int):
        """
        Adds a guardrail to the InstructionInput.

        :param guardrail: The Guardrail instance to add.
        :param tokenset_index: The index of the TokenSet the guardrail applies to.
        """
        if tokenset_index > len(self.tokensets) - 1:
            raise ValueError(f"tokenset_index {tokenset_index} is out of range for the Instruction input tokensets.")

        self.guardrails[tokenset_index] = guardrail
