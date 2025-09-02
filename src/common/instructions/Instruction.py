import abc
from abc import ABC
from typing import Sequence

from src.common.tokens.Token import Token
from src.common.tokens.TokenSet import TokenSet, Snippet


class Instruction(ABC):
    """
    An Instruction is a set of tokens that show possible input combinations for a model.

    Samples must be added to the Instruction to provide context for the model.
    A minimum of 3 samples must be added to an Instruction.

    Example:
        context = TokenSet(
        context = [
                 ( Token("SentenceLength", num=True), Token("Greeting")),
                 ( Token("CurtResponse")),
                 ( Token("SentenceLength", num=True), Token("Goodbye")),

    """

    def __init__(self, context: Sequence[TokenSet], response: TokenSet, final: Token):
        """Initializes the common attributes to all Instructions."""
        self.context: Sequence[TokenSet] = context
        self.response: TokenSet = response
        self.result: Token = final
        self.samples: list[dict] = []

    @abc.abstractmethod
    def add_sample(self):
        """Add a sample to the Instruction."""
        raise NotImplementedError("Subclasses must implement add_sample method.")

    def get_token_sets(self) -> list[TokenSet]:
        """Returns all tokens in the instruction as a list of tuples."""
        all_tokens: list = []
        for token_set in self.context:
            all_tokens.append(token_set)
        all_tokens.append(self.response)
        return all_tokens

    def contains_user(self) -> bool:
        """
        Returns True if the response contains a user token, else False
        """
        return self.response.is_user

    def _create_base_sample(self, snippets: list[Snippet], value: int | float | None = None) -> dict:
        """Create a base sample dictionary without a prompt."""
        if value is not None:
            assert type(value) == int or type(value) == float, "Value is not a number."
        else:
            value = "None"

        # format sample
        strings: list[str] = []
        numbers: list[list[int]] = []
        for snippet in snippets:
            strings.append(snippet.sample)
            numbers.append(snippet.numbers)
            if snippet.numbers is not None:
                numbers.append(snippet.numbers)
            else:
                numbers.append([])

        return {'strings': snippets, 'number': numbers, 'result': self.result, 'value': value, 'prompt': None}

    def _assert_numbers(self, numbers: list[list[int]]):
        """
        Asserts that the provided numbers match the number of tokens that require numbers.
        :param numbers: List of numbers provided in the sample.
        """
        assert isinstance(numbers, list), "The number is not set as a list."
        num_check: list[int] = sum(
            [element if isinstance(element, list) else [element] for sublist in numbers for element in sublist], [])
        # TODO: Update assertion for clarity and speed using TokenSets and is_number attribute in token set
        assert all(isinstance(num, (int, float)) for num in num_check), "Not all elements are numbers."
        num_tokens: list[list[str]] = [[token.key] for token_set in self.get_token_sets()
                                       for token in token_set.tokens if token.num]
        num_numbers: list[int] = [item for sublist in numbers for item in sublist if item or item == 0]
        assert len(num_tokens) == len(num_numbers), "Number samples don't match memory count."
        for num, tok in zip(numbers, self.context):
            num_token: list[str] = [token.key for token in tok if token.num]
            num_array: list[int] = [num for num in num if num or num == 0]
            assert len(num_array) == len(num_token), "Not all numbers provided."

    def __str__(self) -> str:
        """String representation of the Instruction."""
        tokens_str: str = ', '.join(
            [''.join([token.key for token in token_set.tokens]) for token_set in self.get_token_sets()])
        samples_str: str = ',\n'.join([
            f"Sample(Strings: {sample['strings']}, Result: {sample['result'].key + sample['value'] if sample['value'] is not None else ''}"
            for sample in self.samples])
        return f"Token Set(Tokens: {tokens_str}, Result: {self.result.key}, Samples:\n{samples_str})"

    def to_dict(self):
        """Convert the Instruction to a dictionary representation."""
        return {
            'tokens': [[token.to_dict() for token in token_set.tokens] for token_set in self.get_token_sets()],
            'result': self.result.to_dict() if self.result else None,
            'samples': self.samples
        }
