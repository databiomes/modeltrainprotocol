from typing import List, Dict, Any
from pydantic import BaseModel, Field, validator

GENERATE_MTP_TOOL: dict = {
    "name": "generate_mtp",
    "type": "function",
    "description": "Generate developer message context array and multiple instruction sets based on the provided developer message.",
    "strict": True,
    "parameters": {
        "type": "object",
        "required": [
            "developer_message",
            "context",
            "instruction_sets"
        ],
        "properties": {
            "developer_message": {
                "type": "string",
                "description": "The main message provided by the developer to base context and instructions on."
            },
            "context": {
                "type": "array",
                "description": "Array of contexts, each explaining an aspect of the developer message context. Context should be detailed, and more information and items are better.",
                "minItems": 5,
                "items": {
                    "type": "object",
                    "required": ["context"],
                    "properties": {
                        "context": {
                            "type": "string",
                            "description": "Aspect explaining developer message context."
                        }
                    },
                    "additionalProperties": False
                }
            },
            "instruction_sets": {
                "type": "array",
                "description": "Array of instruction sets, each containing an instruction, a possible user prompt, and a response using the developer message context.",
                "minItems": 3,
                "items": {
                    "type": "object",
                    "required": [
                        "instruction",
                        "prompt",
                        "response",
                        "samples"
                    ],
                    "properties": {
                        "instruction": {
                            "type": "string",
                            "description": "Instruction derived from the developer message."
                        },
                        "prompt": {
                            "type": "string",
                            "description": "Possible user question, prompt or environment detail related to this instruction. Functions as the prompt for the model."
                        },
                        "response": {
                            "type": "string",
                            "description": "Response that uses the developer message context to answer the prompt."
                        },
                        "samples": {
                            "type": "array",
                            "description": "Array of sample responses demonstrating the instruction in action.",
                            "items": {
                                "type": "object",
                                "description": "Sample interactions of user or environment prompt and model response for this instruction.",
                                "required": ["prompt_sample", "response_sample"],
                                "properties": {
                                    "prompt_sample": {
                                        "type": "string",
                                        "description": "Sample user prompt for this instruction."
                                    },
                                    "response_sample": {
                                        "type": "string",
                                        "description": "Sample response for this instruction."
                                    }
                                },
                                "additionalProperties": False
                            },
                            "minItems": 3
                        }
                    },
                    "additionalProperties": False
                }
            }
        },
        "additionalProperties": False
    }
}


# --- Nested Models ---


class ContextItemModel(BaseModel):
    """
    A single context item explaining an aspect of the developer message.
    Corresponds to individual items in the 'context' array.
    """
    context: str = Field(..., description="Aspect explaining developer message context.")

    class Config:
        extra = "allow"  # Enforces 'additionalProperties': true


class Sample(BaseModel):
    """
    A single sample interaction of user prompt and model response for an instruction.
    Corresponds to items in the 'samples' array within an instruction set.
    """
    prompt_sample: str = Field(..., description="Sample user prompt for this instruction.")
    response_sample: str = Field(..., description="Sample response for this instruction.")

    class Config:
        extra = "allow"  # Enforces 'additionalProperties': true


class InstructionSetModel(BaseModel):
    """
    A single set containing an instruction, a possible user prompt, and a context-based response.
    Corresponds to the items in the 'instruction_sets' array.
    """
    instruction: str = Field(..., description="Instruction derived from the developer message.")
    prompt: str = Field(..., description="Possible user question or prompt related to this instruction.")
    response: str = Field(..., description="Response that uses the developer message context.")
    samples: List[Sample] = Field(...,
                                  description="Array of sample responses demonstrating the instruction in action.",
                                  min_items=3)

    class Config:
        extra = "allow"  # Enforces 'additionalProperties': true


# --- Main Model ---

class GenerateMTPResultModel(BaseModel):
    """
    The main model representing the output of the 'generate_mtp' tool.
    Corresponds to the overall 'parameters' object in the schema.
    """
    developer_message: str = Field(...,
                                   description="The main message provided by the developer to base context and instructions on.")
    context: List[ContextItemModel] = Field(...,
                                            description="Array of a minimum of five contexts with a description explaining the context of the developer message.",
                                            min_items=5)
    instruction_sets: List[InstructionSetModel] = Field(...,
                                                        description="Array of a minimum of three sets each with instruction, possible user prompt, and context-based response.",
                                                        min_items=3)

    class Config:
        extra = "forbid"  # Enforces 'additionalProperties': false


class GenerateMTPContextItemModel(BaseModel):
    """
    A single context item explaining an aspect of the developer message.
    Matches 'context.items' in the generate_mtp schema.
    """
    context: str = Field(..., description="Aspect explaining developer message context.")

    class Config:
        extra = "allow"  # corresponds to 'additionalProperties': true


class GenerateMTPInstructionSetModel(BaseModel):
    """
    A single instruction set with an instruction, possible user prompt, and context-based response.
    Matches 'instruction_sets.items' in the generate_mtp schema.
    """
    instruction: str = Field(..., description="Instruction derived from the developer message.")
    prompt: str = Field(..., description="Possible user question or prompt related to this instruction.")
    response: str = Field(..., description="Response that uses the developer message context.")

    class Config:
        extra = "allow"  # corresponds to 'additionalProperties': true


# --- Main Function Definition Model ---

class GenerateMTPFunctionInput(BaseModel):
    """
    Represents the function schema for 'generate_mtp'.
    This matches the OpenAI function/tool definition JSON.
    """
    call_id: str

    developer_message: str = Field(
        ...,
        description="The main message provided by the developer to base context and instructions on."
    )
    context: List[GenerateMTPContextItemModel] = Field(
        ...,
        description="Array of a minimum of five contexts with a description explaining the context of the developer message.",
        min_items=5
    )
    instruction_sets: List[GenerateMTPInstructionSetModel] = Field(
        ...,
        description="Array of a minimum of three sets each with instruction, possible user prompt, and context-based response.",
        min_items=3
    )

    def dump_parameters(self) -> Dict[str, Any]:
        """Custom method to dump parameters as a dictionary."""
        return {
            "developer_message": self.developer_message,
            "context": [item.model_dump() for item in self.context],
            "instruction_sets": [item.model_dump() for item in self.instruction_sets]
        }

    class Config:
        extra = "forbid"  # corresponds to 'additionalProperties': false
