"""Errors raised for protocol validation."""

from .base import MTPTypeError, MTPValueError


class ProtocolError(MTPValueError):
    """Errors raised for protocol validation."""


class ProtocolTypeError(MTPTypeError, ProtocolError):
    """Errors raised for protocol type validation."""
