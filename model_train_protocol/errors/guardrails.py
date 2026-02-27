"""Errors raised for guardrail validation."""

from .base import MTPTypeError, MTPValueError


class GuardrailError(MTPValueError):
    """Errors raised for guardrail validation."""


class GuardrailTypeError(MTPTypeError, GuardrailError):
    """Errors raised for guardrail type validation."""
