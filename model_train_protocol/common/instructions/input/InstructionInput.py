from typing import List


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
