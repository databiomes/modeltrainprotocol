"""
Instruction classes for the Model Train Protocol package.
"""

from .Instruction import Instruction
from .SimpleInstruction import SimpleInstruction
from .UserInstruction import UserInstruction

__all__ = [
    "Instruction",
    "SimpleInstruction",
    "UserInstruction"
]
