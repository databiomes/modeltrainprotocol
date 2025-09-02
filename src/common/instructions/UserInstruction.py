from typing import Sequence

from src.common.instructions.Instruction import Instruction
from src.common.tokens.Token import Token
from src.common.tokens.TokenSet import TokenSet


class UserInstruction(Instruction):
    """
    A UserInstruction is a specialized Instruction that includes at least one user token in the user token set.

    Note: The response is not set in a UserInstruction.

    This Instruction type includes a prompt provided by the user to guide the model's response.
    """

    def __init__(self, context: Sequence[TokenSet], user: TokenSet, final: Token, prompt: str):
        """
        Initializes a UserInstruction instance.

        :param context: List of tuples containing Token instances that define the input structure.
        :param final: A Token instance representing the expected output.
        :param prompt: A string provided by the user to guide the model's response.
        """
        super().__init__(context=context, response=user, final=final)
        assert self._contains_user(), "UserInstruction requires a user token in the response. Use Instruction for non-user inputs."
        self.prompt: str = prompt


    # noinspection PyMethodOverriding
    def add_sample(self, strings: list[str], prompt: str, numbers: list[list[int]] | None = None,
                   value: int | float | None = None):
        """Add a sample to the Instruction."""
        sample: dict = self._create_base_sample(strings, numbers, value)
        sample['prompt'] = prompt
        self.samples.append(sample)
