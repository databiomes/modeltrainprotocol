"""Errors raised for instruction input validation."""

from .base import MTPValueError


class InstructionInputError(MTPValueError):
    """Errors raised for instruction input validation."""


class GuardrailIndexError(InstructionInputError):
    """Errors raised for invalid guardrail indexes."""


class DuplicateGuardrailError(InstructionInputError):
    """Errors raised when guardrails collide on an index."""
