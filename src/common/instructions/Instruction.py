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
        self.final: Token = final
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
            strings.append(snippet.string)
            numbers.append(snippet.numbers)

        return {'strings': snippets, 'number': numbers, 'result': self.final, 'value': value, 'prompt': None}

    def _assert_valid_value(self, value: int | float | None):
        """
        Assert value is provided if self.final is a number Token, else assert value is None
        :param value: Optional value ascribed to the final Instruction output IF the final Token output is a number
        """
        if self.final.num and value is None:
            raise ValueError("Value must be provided when final token is a number.")
        if self.final.num and not (isinstance(value, int) or isinstance(value, float)):
            raise TypeError("Value must be an int or float when final token is a number.")
        if not self.final.num and value is not None:
            raise ValueError("Value must be None when final token is not a number.")

    def __str__(self) -> str:
        """String representation of the Instruction."""
        tokens_str: str = ', '.join(
            [''.join([token.key for token in token_set.tokens]) for token_set in self.get_token_sets()])
        samples_str: str = ',\n'.join([
            f"Sample(Strings: {sample['strings']}, Result: {sample['result'].key + sample['value'] if sample['value'] is not None else ''}"
            for sample in self.samples])
        return f"Token Set(Tokens: {tokens_str}, Result: {self.final.key}, Samples:\n{samples_str})"

    def to_dict(self):
        """Convert the Instruction to a dictionary representation."""
        return {
            'tokens': [[token.to_dict() for token in token_set.tokens] for token_set in self.get_token_sets()],
            'result': self.final.to_dict() if self.final else None,
            'samples': self.samples
        }
