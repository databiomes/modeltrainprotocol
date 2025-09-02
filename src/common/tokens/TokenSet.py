import dataclasses
from typing import Sequence

from dataclasses import dataclass

from src.common.tokens.Token import Token


@dataclass
class Snippet:
    sample: str
    numbers: list[int] = dataclasses.field(default_factory=list)


class TokenSet:
    """A set of Tokens representing a combination of input types."""

    def __init__(self, tokens: Sequence[Token]):
        """Initializes a TokenSet instance."""
        self.tokens: Sequence[Token] = tokens
        self.is_user: bool = any(token.user for token in tokens)
        self.required_numbers: int = sum(1 for token in tokens if token.num)  # Count of tokens that require numbers
        self.key: str = ''.join(token.key for token in tokens)

    def create_snippet(self, sample: str, numbers: list[int] = None) -> Snippet:
        """Create a snippet for the TokenSet"""
        numbers = numbers if numbers is not None else []
        assert len(numbers) == self.required_numbers, \
            f"{self} requires {self.required_numbers} numbers but {len(numbers)} were provided."
        return Snippet(sample=sample, numbers=numbers)

    def __repr__(self):
        """String representation of the TokenSet."""
        return f"TokenSet([{self.key}])"

    def __iter__(self):
        """Iterator over the tokens in the TokenSet."""
        return iter(self.tokens)
