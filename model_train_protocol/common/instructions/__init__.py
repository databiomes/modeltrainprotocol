"""
Instruction classes for the Model Train Protocol package.
"""

from .BaseInstruction import BaseInstruction
from .SimpleInstruction import SimpleInstruction
from .UserInstruction import UserInstruction

__all__ = [
    "BaseInstruction",
    "SimpleInstruction",
    "UserInstruction"
]
