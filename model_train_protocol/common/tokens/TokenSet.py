import dataclasses
import warnings
from typing import Sequence, Iterable

from dataclasses import dataclass

from ..guardrails.Guardrail import Guardrail
from .Token import Token


@dataclass
class Snippet:
    string: str
    numbers: list[int] = dataclasses.field(default_factory=list)


class TokenSet:
    """A set of Tokens representing a combination of input types."""

    def __init__(self, tokens: Sequence[Token]):
        """Initializes a TokenSet instance."""
        self.tokens: Sequence[Token] = tokens
        self.is_user: bool = any(token.user for token in tokens)
        self.required_numbers: int = sum(1 for token in tokens if token.num)  # Count of tokens that require numbers
        self.key: str = ''.join(token.value for token in tokens) # Note this key is based on the value of the tokens and not the keys of the tokens
        self._guardrail: Guardrail | None = None

    @property
    def guardrail(self) -> Guardrail | None:
        """Returns the guardrails for the TokenSet, if any."""
        return self._guardrail

    def set_guardrail(self, guardrail: Guardrail):
        """Sets a guardrails for the TokenSet."""
        if self.guardrail is not None:
            warnings.warn("Overwriting existing guardrails for TokenSet.")
        if not self.is_user:
            raise ValueError("Guardrails can only be added to a user TokenSet.")
        if not isinstance(guardrail, Guardrail):
            raise TypeError("Guardrail must be an instance of the Guardrail class.")
        self._guardrail = guardrail

    def create_snippet(self, string: str, numbers: Iterable[int] | int | None = None) -> Snippet:
        """Create a snippet for the TokenSet"""
        if numbers is None:
            numbers = []
        elif isinstance(numbers, int):
            numbers = [numbers]
        elif isinstance(numbers, Iterable) and not isinstance(numbers, str):
            numbers = list(numbers)
        else:
            raise TypeError("Numbers must be an int, an Iterable of ints, or None.")
        assert len(numbers) == self.required_numbers, \
            f"{self} requires {self.required_numbers} numbers but {len(numbers)} were provided."
        return Snippet(string=string, numbers=numbers)

    def get_token_key_set(self) -> str:
        """Returns a string representing the combined token keys of the individual Tokens in the TokenSet."""
        token_key_set = ''
        for token in self.tokens:
            token_key_set += token.key
        return token_key_set

    def __repr__(self):
        """String representation of the TokenSet."""
        return f"TokenSet([{self.key}])"

    def __iter__(self):
        """Iterator over the tokens in the TokenSet."""
        return iter(self.tokens)
