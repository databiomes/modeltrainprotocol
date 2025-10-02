"""
Pydantic models for Protocol JSON structure.
"""

from typing import List, Dict, Any, Optional, Union

from pydantic import BaseModel, Field


class TokenInfoModel(BaseModel):
    """Model for individual token information."""
    emoji: str
    num: bool
    user: bool
    desc: Optional[str]
    special: Optional[str]


class SampleModel(BaseModel):
    """Model for instruction samples."""
    sample: List[str]
    prompt: Optional[Union[str]]
    number: Optional[Union[int, List[int], List[List[int]]]]
    result: str
    value: Optional[str]


class InstructionSetModel(BaseModel):
    """Model for instruction sets."""
    set: List[List[str]]
    result: str
    samples: List[SampleModel]
    ppo: List[Any] = Field(default_factory=list)


class InstructionModel(BaseModel):
    """Model for instruction configuration."""
    memory: int
    sets: List[InstructionSetModel]


class GuardrailModel(BaseModel):
    """Model for guardrails configuration."""
    nil: str = Field(default="", alias="None")

    class Config:
        extra = "allow"  # Allow extra fields for dynamic attributes

    def __getitem__(self, key: str) -> Any:
        """Get a guardrail rule by key."""
        return getattr(self, key, None)

    def __setitem__(self, key: str, value: Any) -> None:
        """Set a guardrail rule by key."""
        setattr(self, key, value)

    def get_guardrail_rules(self) -> Dict[str, Any]:
        """Get all guardrail rules as a dictionary."""
        return {k: v for k, v in self.__dict__.items() if k != 'nil'}

    def set_guardrail_rule(self, key: str, value: Union[str, List[Union[str, List[str]]]]) -> None:
        """Set a guardrail rule with proper validation."""
        if not isinstance(value, (str, list)):
            raise ValueError(f"Guardrail value must be string or list, got {type(value)}")
        setattr(self, key, value)

class NumberModel(BaseModel):
    """Model for numbers configuration."""
    nil: str = Field(default="", alias="None")

    class Config:
        extra = "allow"  # Allow extra fields for dynamic attributes

    def __getitem__(self, key: str) -> Any:
        """Get a number rule by key."""
        return getattr(self, key, None)

    def __setitem__(self, key: str, value: Any) -> None:
        """Set a number rule by key."""
        setattr(self, key, value)

    def get_number_rules(self) -> Dict[str, Any]:
        """Get all number rules as a dictionary."""
        return {k: v for k, v in self.__dict__.items() if k != 'nil'}

    def set_number_rule(self, key: str, value: str) -> None:
        """Set a number rule with proper validation."""
        if not isinstance(value, str):
            raise ValueError(f"Number value must be string, got {type(value)}")
        setattr(self, key, value)

class BatchModel(BaseModel):
    """Model for batches configuration."""
    pretrain: List[Any] = Field(default_factory=list)
    instruct: List[Any] = Field(default_factory=list)
    judge: List[Any] = Field(default_factory=list)
    ppo: List[Any] = Field(default_factory=list)


class ProtocolModel(BaseModel):
    """Main model for MTP Protocol JSON structure."""
    name: str
    context: List[str]
    tokens: Dict[str, TokenInfoModel]
    special_tokens: List[str]
    instruction: InstructionModel
    guardrails: GuardrailModel
    numbers: NumberModel
    batches: BatchModel

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
