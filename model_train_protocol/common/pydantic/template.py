"""
Pydantic models for Template JSON structure.
"""

from typing import Dict, List, Literal

from pydantic import BaseModel


class TokensModel(BaseModel):
    """Model for tokens in template (input and output mappings)."""
    input: Dict[str, str]  # Maps token values to token keys with template representations
    output: Dict[str, str]  # Maps token values to token keys


class InstructionDefinitionModel(BaseModel):
    """Model for a single instruction definition in the template."""
    type: Literal["basic", "extended"]  # Instruction type: "basic" or "extended"
    input: List[str]  # List of input strings with token keys and placeholders
    output: List[str]  # List of output strings with token keys and placeholders


def _example_usage_json_schema_extra(schema: dict, model_class) -> None:
    """Customize JSON schema to specify that additionalProperties must be strings."""
    schema["additionalProperties"] = {
        "type": "string",
        "description": "Example usage string (e.g., instruction_input, valid_model_output, guardrail_model_output)"
    }


class ExampleUsageModel(BaseModel):
    """Model for example usage in template."""
    
    instruction_input: str
    valid_model_output: str
    guardrail_model_output: str


class TemplateModel(BaseModel):
    """Main model for MTP Template JSON structure."""
    version: str
    encrypt: bool
    tokens: TokensModel
    instructions: Dict[str, InstructionDefinitionModel]  # Instruction name -> instruction definition
    example_usage: ExampleUsageModel
