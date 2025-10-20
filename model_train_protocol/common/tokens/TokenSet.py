import dataclasses
import warnings
from typing import Sequence, Collection

from dataclasses import dataclass

from . import NumListToken
from .Token import Token
from ..guardrails.Guardrail import Guardrail
from .NumToken import NumToken


@dataclass
class Snippet:
    string: str
    token_set_key: str
    numbers: list[int | float]
    number_lists: list[list[int | float]]


class TokenSet:
    """A set of Tokens representing a combination of input types."""

    def __init__(self, tokens: Sequence[Token] | Token):
        """Initializes a TokenSet instance."""
        if isinstance(tokens, Token):
            tokens = [tokens]
        self.tokens: Sequence[Token] = tokens
        self.is_user: bool = any(token.user for token in tokens)
        self.required_numtoken_numbers: int = sum(
            token.num for token in tokens if isinstance(token, NumToken))  # Count of NumToken
        self.required_numlists: list[int] = [
            token.num_list for token in tokens if isinstance(token, NumListToken)
        ]  # List of lengths for NumListToken
        self.key: str = ''.join(token.value for token in
                                tokens)  # Note this key is based on the value of the tokens and not the keys of the tokens
        self._guardrail: Guardrail | None = None

    @property
    def guardrail(self) -> Guardrail | None:
        """Returns the guardrails for the TokenSet, if any."""
        return self._guardrail

    def set_guardrail(self, guardrail: Guardrail):
        """Sets a guardrails for the TokenSet."""
        if self.guardrail is not None:
            raise ValueError("Only one guardrail can be set per TokenSet.")
        if not self.is_user:
            raise ValueError("Guardrails can only be added to a user TokenSet.")
        if not isinstance(guardrail, Guardrail):
            raise TypeError("Guardrail must be an instance of the Guardrail class.")
        self._guardrail = guardrail

    def create_snippet(self, string: str,
                       numbers: Collection[int | float] | int | float | None = None,
                       number_lists: Collection[int | float | Collection[int | float]] | None = None) -> Snippet:
        """Create a snippet for the TokenSet"""
        if not isinstance(string, str):
            raise TypeError("String must be of type str.")

        if numbers is None:
            numbers = []
        elif isinstance(numbers, int):
            numbers = [numbers]
        elif isinstance(numbers, Collection):
            numbers = list(numbers)
        else:
            raise TypeError("Numbers must be an int, an Collection of ints, or None.")

        if number_lists is None:
            number_lists = []
        # if number lists is a single list of numbers, wrap it in another list
        elif isinstance(number_lists, Collection) and all(isinstance(nl, (float, int)) for nl in number_lists):
            number_lists = [number_lists]
        elif isinstance(number_lists, Collection) and all(isinstance(nl, Collection) for nl in number_lists):
            pass
        else:
            raise TypeError("Number lists must be an Collection of numbers or Collection of Collections or None.")

        if len(numbers) != self.required_numtoken_numbers:
            raise ValueError(
                f"{self} requires {self.required_numtoken_numbers} numbers but {len(numbers)} were provided.")
        if len(number_lists) != len(self.required_numlists):
            raise ValueError(
                f"{self} requires {len(self.required_numlists)} number lists but {len(number_lists or [])} lists were provided.")
        for (i, required_length) in enumerate(self.required_numlists):
            if len(number_lists[i]) != required_length:
                raise ValueError(
                    f"Number list at index {i} must be of length {required_length} but is of length {len(number_lists[i])}.")

        # Combine numbers and number_lists into single input for Snippet
        numbers_index = 0
        number_lists_index = 0
        # final_numbers: list[int | float] = []
        # final_number_lists: list[Collection[int | float]] = []
        # combined_numbers: list[int | float | Collection[int | float]] = []  # Combined list of numbers and number lists
        # for index, token in enumerate(self.tokens):
        #     if not isinstance(token, NumToken):
        #         continue
        #
        #     if token.num == 1:
        #         combined_numbers.append(numbers[numbers_index])
        #         numbers_index += 1
        #     elif token.num > 1:
        #         combined_numbers.append(number_lists[number_lists_index])
        #         number_lists_index += 1
        #
        # for index, token in enumerate(self.tokens):
        #
        #     if not isinstance(token, NumListToken):
        #         continue
        #
        #     number_lists.append(numbers[number_lists_index])

        return Snippet(string=string, numbers=numbers, number_lists=number_lists, token_set_key=self.key)

    def get_token_key_set(self) -> str:
        """Returns a string representing the combined token keys of the individual Tokens in the TokenSet."""
        token_key_set = ''
        for token in self.tokens:
            token_key_set += token.key
        return token_key_set

    def __eq__(self, other):
        """Equality comparison for TokenSet."""
        if not isinstance(other, TokenSet):
            return False
        return self.key == other.key and all(st == ot for (st, ot) in zip(self.tokens, other.tokens))

    def __hash__(self):
        """Hash based on the string representation of the TokenSet."""
        return hash(str(self))

    def __repr__(self):
        """String representation of the TokenSet."""
        return f"TokenSet([{self.key}])"

    def __iter__(self):
        """Iterator over the tokens in the TokenSet."""
        return iter(self.tokens)
