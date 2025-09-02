from src.common.Token import Token
from src.common.instructions.Instruction import Instruction


class UserInstruction(Instruction):
    """
    A UserInstruction is a specialized Instruction that includes at least one user-provided token in the final token set.

    This Instruction type includes a prompt provided by the user to guide the model's response.
    """

    def __init__(self, tokens: list[tuple[Token]], result: Token, memory: int, prompt: str):
        """
        Initializes a UserInstruction instance.

        :param tokens: List of tuples containing Token instances that define the input structure.
        :param result: A Token instance representing the expected output.
        :param memory: An integer indicating how many previous inputs the model should consider.
        :param prompt: A string provided by the user to guide the model's response.
        """
        super().__init__(tokens, result, memory)
        self.prompt: str = prompt
        user_check: bool = False
        for token in self.tokens[-1]:
            if token.user:
                user_check = True
                break
        assert user_check, "UserInstruction requires a user token in the final token set."

    # noinspection PyMethodOverriding
    def add_sample(self, strings: list[str], prompt: str, numbers: list[list[int]] | None = None,
                   value: int | float | None = None):
        """Add a sample to the Instruction."""
        sample: dict = self._create_base_sample(strings, numbers, value)
        sample['prompt'] = prompt
        self.samples.append(sample)
