"""
Pydantic models for Protocol JSON structure.
"""

from typing import List, Dict, Any, Optional, Union

from pydantic import BaseModel, Field


class TokenInfo(BaseModel):
    """Model for individual token information."""
    emoji: str
    num: bool
    user: bool
    desc: Optional[str] = None
    special: Optional[str] = None


class Sample(BaseModel):
    """Model for instruction samples."""
    sample: List[str]
    prompt: Union[str, None]
    number: Union[int, List[int], List[List[int]]]
    result: str
    value: Union[str, None]


class InstructionSet(BaseModel):
    """Model for instruction sets."""
    set: List[List[str]]
    result: str
    samples: List[Sample]
    ppo: List[Any] = Field(default_factory=list)


class Instruction(BaseModel):
    """Model for instruction configuration."""
    memory: int
    sets: List[InstructionSet]


class Guardrails(BaseModel):
    """Model for guardrails configuration."""
    nil: str = Field(default="", alias="None")

    # Dynamic field for other guardrail rules
    def __getitem__(self, key):
        return getattr(self, key, None)

    def __setitem__(self, key, value):
        setattr(self, key, value)

class Numbers(BaseModel):
    """Model for numbers configuration."""
    nil: str = Field(default="", alias="None")

class Batches(BaseModel):
    """Model for batches configuration."""
    pretrain: List[Any] = Field(default_factory=list)
    instruct: List[Any] = Field(default_factory=list)
    judge: List[Any] = Field(default_factory=list)
    ppo: List[Any] = Field(default_factory=list)


class ProtocolModel(BaseModel):
    """Main model for MTP Protocol JSON structure."""
    name: str
    context: List[str]
    tokens: Dict[str, TokenInfo]
    special_tokens: List[str]
    instruction: Instruction
    guardrails: Dict[str, Union[str, List[Union[str, List[str]]]]]  # Flexible for dynamic keys
    numbers: Numbers
    batches: Batches

    class Config:
        json_schema_extra = {
            "example": {
                "name": "cat",
                "context": [
                    "ALICE was beginning to get very tired of sitting by her sister on the bank...",
                    "So she was considering in her own mind, as well as she could..."
                ],
                "tokens": {
                    "English_": {
                        "emoji": "🇨",
                        "num": False,
                        "user": False,
                        "desc": None,
                        "special": None
                    },
                    "Alice_": {
                        "emoji": "😁",
                        "num": False,
                        "user": True,
                        "desc": None,
                        "special": None
                    }
                },
                "special_tokens": [
                    "🪾🇨😁🗣",
                    "🔄",
                    "🪾🇨🐱🗣"
                ],
                "instruction": {
                    "memory": 3,
                    "sets": []
                },
                "guardrails": {
                    "None": ""
                },
                "numbers": {
                    "None": ""
                },
                "batches": {
                    "pretrain": [],
                    "instruct": [],
                    "judge": [],
                    "ppo": []
                }
            }
        }
