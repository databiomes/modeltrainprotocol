from typing import List

from model_train_protocol import InstructionInput
from model_train_protocol.common.tokens import TokenSet


class StateMachineInput(InstructionInput):
    """Defines the structure for State Machine Instruction inputs."""

    def __init__(self, tokensets: List[TokenSet]):
        """
        Initializes the StateMachineInput with tokensets.

        :param tokensets: A list of TokenSet in the order that they appear in the instruction.
        """
        super().__init__(tokensets=tokensets)
