"""Base error types for model_train_protocol."""


class MTPError(Exception):
    """Base error for model_train_protocol."""


class MTPValueError(ValueError, MTPError):
    """Base value error for model_train_protocol."""


class MTPTypeError(TypeError, MTPError):
    """Base type error for model_train_protocol."""


class MTPKeyError(KeyError, MTPError):
    """Base key error for model_train_protocol."""
