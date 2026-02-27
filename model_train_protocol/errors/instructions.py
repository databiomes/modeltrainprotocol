"""Errors raised for instruction validation."""

from .base import MTPTypeError, MTPValueError


class InstructionError(MTPValueError):
    """Errors raised for instruction validation."""


class InstructionTypeError(MTPTypeError, InstructionError):
    """Errors raised for instruction type validation."""
