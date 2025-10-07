from typing import List, Dict, Any
from pydantic import BaseModel, Field, validator


# --- Nested Models ---

class ContextItemModel(BaseModel):
    """
    A single context item explaining an aspect of the developer message.
    Corresponds to individual items in the 'context' array.
    """
    context: str = Field(..., description="Aspect explaining developer message context.")

    class Config:
        extra = "allow"  # Enforces 'additionalProperties': true


class InstructionSetModel(BaseModel):
    """
    A single set containing an instruction, a possible user prompt, and a context-based response.
    Corresponds to the items in the 'instruction_sets' array.
    """
    instruction: str = Field(..., description="Instruction derived from the developer message.")
    possible_user_prompt: str = Field(..., description="Possible user question or prompt related to this instruction.")
    response_using_context: str = Field(..., description="Response that uses the developer message context.")

    class Config:
        extra = "allow"  # Enforces 'additionalProperties': true


# --- Main Model ---

class PrototypeModel(BaseModel):
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


# Example Usage:
if __name__ == "__main__":
    example_data = {
        "developer_message": "Our new service, PhotoVault, launches next week. It offers unlimited, encrypted photo storage for $5/month, and the main benefit is end-to-end encryption. Customers can sign up on our primary domain, photovault.com.",
        "context": [
            {"context": "Product Name: PhotoVault"},
            {"context": "Launch Timeline: Next week"},
            {"context": "Core Feature: Unlimited, encrypted photo storage"},
            {"context": "Pricing: $5/month"},
            {"context": "Sign-up Location: photovault.com"}
        ],
        "instruction_sets": [
            {
                "instruction": "Mention the service name and its core offering.",
                "possible_user_prompt": "What is PhotoVault?",
                "response_using_context": "PhotoVault is our new service launching next week, offering unlimited, encrypted photo storage."
            },
            {
                "instruction": "State the monthly cost and primary security feature.",
                "possible_user_prompt": "How much does PhotoVault cost and is it secure?",
                "response_using_context": "It costs $5/month, and its main benefit is end-to-end encryption, ensuring your photos are highly secure."
            },
            {
                "instruction": "Provide the website for sign-up.",
                "possible_user_prompt": "Where can I sign up for the new photo storage service?",
                "response_using_context": "You can sign up for PhotoVault on our primary domain: photovault.com."
            }
        ]
    }

    try:
        # Instantiate the model with the example data
        validated_model = PrototypeModel(**example_data)
        print("Pydantic model successfully validated the data.")
        print("\nValidated Data (as dictionary):")
        print(validated_model.model_dump_json(indent=2))

    except Exception as e:
        print(f"Validation Error: {e}")
