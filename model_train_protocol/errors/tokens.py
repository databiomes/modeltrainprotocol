"""Errors raised for token and token set validation."""

from .base import MTPTypeError, MTPValueError


class TokenError(MTPValueError):
    """Errors raised for token validation."""


class TokenTypeError(MTPTypeError, TokenError):
    """Errors raised for token type validation."""

class TokenSetError(MTPValueError):
    """Errors raised for token set validation."""


class TokenSetTypeError(MTPTypeError, TokenSetError):
    """Errors raised for token set type validation."""
