"""
Model Train Protocol (MTP) - A Python package for creating custom Language Model training protocols.

MTP is an open-source protocol for training custom Language Models on Databiomes. 
MTP contains all the data that a model is trained on.
"""

from .common.guardrails import Guardrail
from .common.instructions import SimpleInstruction, UserInstruction
from .common.tokens import Token, UserToken, NumToken, NumListToken, SpecialToken, TokenSet, Snippet
from .Protocol import Protocol

__version__ = "1.0.0"
__all__ = [
    "Protocol",
    "Token", 
    "UserToken",
    "NumToken",
    "NumListToken",
    "SpecialToken",
    "TokenSet",
    "Snippet",
    "SimpleInstruction", 
    "UserInstruction",
    "Guardrail"
]
