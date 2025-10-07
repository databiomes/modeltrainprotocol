"""
Instruction classes for the Model Train Protocol package.
"""

from .BaseInstruction import BaseInstruction
from .Instruction import Instruction
from .UnsetInstruction import UnsetInstruction

__all__ = [
    "BaseInstruction",
    "Instruction",
    "UnsetInstruction"
]
