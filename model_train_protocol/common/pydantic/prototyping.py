from typing import List, Dict, Any

from pydantic import BaseModel, Field

from model_train_protocol.common.pydantic.protocol import TokenInfoModel

TOKEN_MODEL: dict = {  # Reusable token model definition
    "type": "object",
    "description": "A single token that defines part of the context of the prompt.",
    "required": ["key", "value", "num", "num_list", "desc"],
    "properties": {
        "key": {
            "type": "string",
            "description": "The string representing the token. A noun, verb, adjective, or concept that is one or two words in length."
        },
        "value": {
            "type": "string",
            "description": "The string representing the token value, same as the key."
        },
        "desc": {
            "type": "string",
            "description": "Optional description of the token. Extends the value to a detailed description to contextualize its use."
        },
        "num": {
            "type": "number",
            "description": "If this token represents a single number, this is the number it represents. Otherwise 0."
        },
        "num_list": {
            "type": "array",
            "description": "If this token represents a list of numbers, this is the list of numbers it represents. Otherwise an empty list.",
            "items": {
                "type": "number"
            }
        },
    },
    "additionalProperties": False
}

FINAL_TOKEN_MODEL: dict = TOKEN_MODEL
FINAL_TOKEN_MODEL["description"] = "A token representing the final action by the model. For example, 'Continue', 'End', or 'Execute'."

GENERATE_MTP_TOOL: dict = {
    "name": "generate_mtp",
    "type": "function",
    "description": "Generate developer message context array and multiple instruction sets based on the provided developer message.",
    "strict": True,
    "parameters": {
        "type": "object",
        "required": [
            "model_name",
            "context",
            "instruction_sets",
            "final_token"
        ],
        "properties": {
            "model_name": {
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
                        "prompt_tokens",
                        "response",
                        "response_tokens",
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
                        "prompt_tokens": {
                            "type": "array",
                            "description": "Array of tokens that defines the context of the prompt.",
                            "items": TOKEN_MODEL,
                            "minItems": 1
                        },
                        "response": {
                            "type": "string",
                            "description": "Response that uses the developer message context to answer the prompt."
                        },
                        "response_tokens": {
                            "type": "array",
                            "description": "Array of tokens that defines the context of the response.",
                            "items": TOKEN_MODEL,
                            "minItems": 1
                        },
                        "samples": {
                            "type": "array",
                            "description": "Array of sample responses demonstrating the instruction in action.",
                            "items": {
                                "type": "object",
                                "description": "Sample interactions of user or environment prompt and model response for this instruction.",
                                "required": ["prompt_context", "prompt_sample", "response_sample"],
                                "properties": {
                                    "prompt_context": {
                                        "type": "string",
                                        "description": "The context for the specific instruction, taken from the developer message or context array. Explains what part of the developer message or context this sample is demonstrating."
                                    },
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
            },
            "final_token": {
                "type": "object",
                "description": "A token representing the final action by the model, if applicable. For example, 'Continue', 'End', or 'Execute'",
                "properties": FINAL_TOKEN_MODEL,
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
    prompt_context: str = Field(...,
                                description="The context for the specific instruction, taken from the developer message or context array. Explains what part of the developer message or context this sample is demonstrating.")
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
    prompt_tokens: List[TokenInfoModel] = Field(...,
                                                description="Array of tokens that defines the context of the prompt.",
                                                min_length=1)
    response: str = Field(..., description="Response that uses the developer message context.")
    response_tokens: List[TokenInfoModel] = Field(...,
                                                  description="Array of tokens that defines the context of the response.",
                                                  min_length=1)
    samples: List[Sample] = Field(...,
                                  description="Array of sample responses demonstrating the instruction in action.",
                                  min_length=3)

    class Config:
        extra = "allow"  # Enforces 'additionalProperties': true


# --- Main Model ---

class GenerateMTPPrototypeModel(BaseModel):
    """
    The main model representing the output of the 'generate_mtp' tool.
    Corresponds to the overall 'parameters' object in the schema.
    """
    model_name: str = Field(...,
                            description="The name of the model this prototype is for.")
    context: List[ContextItemModel] = Field(...,
                                            description="Array of a minimum of five contexts with a description explaining the context of the developer message.",
                                            min_length=5)
    instruction_sets: List[InstructionSetModel] = Field(...,
                                                        description="Array of a minimum of three sets each with instruction, possible user prompt, and context-based response.",
                                                        min_length=3)

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
        min_length=5
    )
    instruction_sets: List[GenerateMTPInstructionSetModel] = Field(
        ...,
        description="Array of a minimum of three sets each with instruction, possible user prompt, and context-based response.",
        min_length=3
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
