from typing import List

from pydantic import BaseModel, Field


class TokenInfoPrototypeModel(BaseModel):
    """Extends TokenInfoPrototypeModel to add 'value' field."""
    value: str = Field(..., description="The string representing the token value, same as the key.")
    desc: str = Field(..., description="Optional description of the token. Extends the value to a detailed description to contextualize its use.")

    class Config:
        extra = "forbid"  # Enforces 'additionalProperties': false

TOKEN_MODEL: dict = {  # Reusable token model definition
    "type": "object",
    "description": "A single token that defines part of the context of the prompt. A Noun, Adjective, Verb, or concept that defines the defines the specific context of the prompt or response. For example, the HomeRepair model might have tokens like 'Plumbing', 'Electrical', 'Carpentry', 'Painting', 'Handyman', 'Morning' etc. A combination of these tokens like 'Plumbing' and 'Morning' would define a specific context for a prompt or response.",
    "required": ["value", "desc"],
    "properties": {
        "value": {
            "type": "string",
            "description": "The string representing the token value, same as the key."
        },
        "desc": {
            "type": "string",
            "description": "Optional description of the token. Extends the value to a detailed description to contextualize its use."
        }
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
                            "minItems": 3,
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
                            }
                        }
                    },
                    "additionalProperties": False
                }
            },
            "final_token": FINAL_TOKEN_MODEL
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
    prompt_tokens: List[TokenInfoPrototypeModel] = Field(...,
                                                description="Array of tokens that defines the context of the prompt.",
                                                min_length=1)
    response: str = Field(..., description="Response that uses the developer message context.")
    response_tokens: List[TokenInfoPrototypeModel] = Field(...,
                                                  description="Array of tokens that defines the context of the response.",
                                                  min_length=1)
    samples: List[Sample] = Field(...,
                                  description="Array of sample responses demonstrating the instruction in action.",
                                  min_length=3)

    class Config:
        extra = "allow"  # Enforces 'additionalProperties': true


# --- Main Model ---

class MTPPrototypeModel(BaseModel):
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
    final_token: TokenInfoPrototypeModel = Field(...,
                                        description="A token representing the final action by the model. For example, 'Continue', 'End', or 'Execute'.")

    class Config:
        extra = "forbid"  # Enforces 'additionalProperties': false
