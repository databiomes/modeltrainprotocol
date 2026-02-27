"""Errors raised for output validation."""

from .base import MTPTypeError, MTPValueError


class OutputError(MTPValueError):
    """Errors raised for output validation."""


class OutputTypeError(MTPTypeError, OutputError):
    """Errors raised for output type validation."""
