"""
Example prototype generation using OpenAI

Takes a prompt ID and OpenAI API key to generate a Model Train Protocol (MTP) file.

Prototype file is then submitted to app.databiomes.com for model generation.
"""
from model_train_protocol.prototyping import generate_prototype_protocol

prompt_id: str = "pmpt_68e...4a0"  # Replace with your actual prompt ID
openai_api_key: str = "sk-..."  # Replace with your actual OpenAI API key

generate_prototype_protocol(prompt_id=prompt_id,
                            openai_api_key=openai_api_key,
                            file_path=None,  # Saves to current directory,
                            name=None,  # Uses model generated name
                            encrypt=False  # Whether to encrypt the protocol file
                            )
