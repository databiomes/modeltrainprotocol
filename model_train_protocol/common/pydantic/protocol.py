"""
Pydantic models for Protocol JSON structure.
"""

from typing import List, Dict, Any, Optional, Union

from pydantic import BaseModel


class TokenInfoModel(BaseModel):
    """Model for individual token information."""
    key: str
    num: bool
    num_list: int
    desc: Optional[str]
    special: Optional[str]


class SampleModel(BaseModel):
    """Model for instruction samples."""
    strings: List[str]
    prompt: Optional[Union[str]]
    numbers: Union[int, List[int], List[List[int]]]
    number_lists: Union[int, List[int], List[List[int]], List[List[List[int]]]]
    result: str
    value: Optional[Union[str, int, float, List[int], List[float]]]  # Can be string, int, float, or list


class GuardrailModel(BaseModel):
    """Model for guardrails configuration."""
    index: int
    good_prompt: str
    bad_prompt: str
    bad_output: str
    bad_examples: list[str]


class InstructionSetModel(BaseModel):
    """Model for instruction sets."""
    guardrails: List[GuardrailModel]
    context: List[str]
    set: List[List[str]]
    samples: List[SampleModel]
    ppo: List[Any]


class InstructionModel(BaseModel):
    """Model for instruction configuration."""
    memory: int
    sets: List[InstructionSetModel]


class NumberModel(BaseModel):
    """Model for numbers configuration."""

    class ConfigDict:
        extra = "allow"  # Allow extra fields for dynamic attributes

    def __getitem__(self, key: str) -> Any:
        """Get a number rule by key."""
        return getattr(self, key, None)

    def __setitem__(self, key: str, value: Any) -> None:
        """Set a number rule by key."""
        setattr(self, key, value)

    def get_number_rules(self) -> Dict[str, Any]:
        """Get all number rules as a dictionary."""
        return {k: v for k, v in self.__dict__.items()}

    def set_number_rule(self, key: str, value: str) -> None:
        """Set a number rule with proper validation."""
        if not isinstance(value, str):
            raise ValueError(f"Number value must be string, got {type(value)}")
        setattr(self, key, value)


class BatchModel(BaseModel):
    """Model for batches configuration."""
    pretrain: List[Any]
    instruct: List[Any]
    judge: List[Any]
    ppo: List[Any]


class ProtocolModel(BaseModel):
    """Main model for MTP Protocol JSON structure."""
    name: str
    context: List[str]
    tokens: Dict[str, TokenInfoModel]
    special_tokens: List[str]
    instruction: InstructionModel
    numbers: NumberModel
    batches: BatchModel

    class ConfigDict:
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
                        "num_list": [],
                        "user": False,
                        "desc": None,
                        "special": None
                    },
                    "Alice_": {
                        "emoji": "😁",
                        "num": False,
                        "num_list": [],
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
                },
                "numbers": {
                },
                "batches": {
                    "pretrain": [],
                    "instruct": [],
                    "judge": [],
                    "ppo": []
                }
            }
        }
