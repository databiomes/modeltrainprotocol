"""Errors raised while building protocol JSON."""

from .base import MTPValueError


class ProtocolFileError(MTPValueError):
    """Errors raised while building protocol JSON."""


class ProtocolFileLayerDepthError(ProtocolFileError):
    """Errors raised for invalid alphabetization layer depth."""
