from typing import Iterable, Sequence

from src.common.instructions.Instruction import Instruction
from src.common.tokens.Token import Token
from src.common.tokens.TokenSet import TokenSet


class SimpleInstruction(Instruction):
    """
    A SimpleInstruction is an instruction without a user prompt.

    Samples must be added to the Instruction to provide context for the model.
    A minimum of 3 samples must be added to an Instruction.

    Example:
        tokens= [
                 ( Token("SentenceLength", num=True), Token("Greeting")),
                 ( Token("CurtResponse")),
                 ( Token("SentenceLength", num=True), Token("Goodbye")),

    """
    def __init__(self, context: Sequence[TokenSet], response: TokenSet, final: Token):
        """Initializes an Instruction instance."""
        super().__init__(context=context, response=response, final=final)
        assert not self._contains_user(), "Instruction cannot contain a user token in response. Use UserInstruction for user inputs."

    # noinspection PyMethodOverriding
    def add_sample(self, strings: list[str], numbers: list[list[int]] | None = None, value: int | float | None = None):
        """Add a sample to the Instruction.

        :param strings: List of strings representing the input lines.
        :param numbers: Optional list of lists of integers representing numbers associated with the input tokens. Each sublist corresponds to a line of tokens when defining the instruction
        :param value: Optional integer or float representing the expected output value.

        Example:
            strings=["Hello, how are you?", "I'm fine.", "It was great to meet you, goodbye!"]
            numbers=[[10], [], [20]]
            value=42

        """
        sample = self._create_base_sample(strings, numbers, value)
        self.samples.append(sample)

    def _create_base_sample(self, strings: list[str], numbers: list[list[int]] | None = None,
                            value: int | float | None = None):
        """Create a base sample dictionary without a prompt."""
        if numbers is not None:
            self._assert_numbers(numbers)
        if value is not None:
            assert type(value) == int or type(value) == float, "Value is not a number."
        else:
            value = "None"
        return {'strings': strings, 'number': numbers, 'result': self.result, 'value': value, 'prompt': None}

    def _assert_numbers(self, numbers: list[list[int]]):
        """
        Asserts that the provided numbers match the number of tokens that require numbers.
        :param numbers: List of numbers provided in the sample.
        """
        assert isinstance(numbers, list), "The number is not set as a list."
        num_check: list[int] = sum(
            [element if isinstance(element, list) else [element] for sublist in numbers for element in sublist], [])
        assert all(isinstance(num, (int, float)) for num in num_check), "Not all elements are numbers."
        num_tokens: list[list[str]] = [[token.key] for tokens in self.context for token in tokens if token.num]
        num_numbers: list[int] = [item for sublist in numbers for item in sublist if item or item == 0]
        assert len(num_tokens) == len(num_numbers), "Number samples don't match memory count."
        for num, tok in zip(numbers, self.context):
            num_token: list[str] = [token.key for token in tok if token.num]
            num_array: list[int] = [num for num in num if num or num == 0]
            assert len(num_array) == len(num_token), "Not all numbers provided."
