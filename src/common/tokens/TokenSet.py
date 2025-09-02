from typing import Iterable

from src.common.tokens.Token import Token


class TokenSet:
    """A set of Tokens representing a combination of input types."""

    def __init__(self, tokens: Iterable[Token]):
        """Initializes a TokenSet instance."""
        self.tokens: Iterable[Token] = tokens
        self.is_user: bool = any(token.user for token in tokens)
        self.requires_number: bool = any(token.num for token in tokens)
        self.key: str = ''.join(token.key for token in tokens)

    def __repr__(self):
        """String representation of the TokenSet."""
        return f"TokenSet([{self.key}])"
