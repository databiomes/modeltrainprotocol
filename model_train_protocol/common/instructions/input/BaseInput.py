from abc import ABC
from typing import List

from model_train_protocol.common.tokens import TokenSet


class BaseInput(ABC):
    """Defines a BaseInput for modularity and future extension."""

    def __init__(self, background: List[str] | None, tokensets: List[TokenSet]):
        """
        Initializes the InstructionInput with an instruction and optional input data.

        :param background: A list of strings providing background context for the instruction.
        :param tokensets: A list of TokenSet in the order that they appear in the instruction.
        """
        if background is None:
            background = []
        self.background: list[str] = background
        self.tokensets = tokensets

    def __len__(self):
        return len(self.background)
