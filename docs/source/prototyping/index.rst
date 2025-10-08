Prototyping Module
==================

The prototyping module provides functionality for automatically generating Model Train Protocol (MTP) files using OpenAI's API. This module streamlines the process of creating training protocols by leveraging AI to generate context, instructions, and samples based on a developer's prompt.

Prerequisites
-------------

Before you can use the prototyping module, you'll need:

1. **OpenAI Account**: A valid OpenAI account with API access
   - Sign up at https://platform.openai.com/
   - Ensure you have API credits or a billing method set up

2. **OpenAI API Key**: Your personal API key for authentication
   - Get your API key from https://platform.openai.com/api-keys
   - Keep this key secure and never share it publicly

3. **A Prompt in OpenAI**: A well-designed prompt that describes your model
   - Go to https://platform.openai.com/prompts
   - Create a new prompt describing what you want your model to do
   - Make it detailed and specific for better results
   - Copy the prompt ID (starts with "pmpt_")

Getting Started
---------------

The prototyping workflow is simple:

1. **Create a Prompt**: Design your prompt in OpenAI's interface
2. **Get Prompt ID**: Copy the prompt ID (starts with "pmpt_")
3. **Generate Protocol**: Use the prototyping module to create your MTP file

Example
~~~~~~~~~~~~~~~

.. code-block:: python

   """
   Example prototype generation using OpenAI
   
   Takes a prompt ID and OpenAI API key to generate a Model Train Protocol (MTP) file.
   
   Prototype file is then submitted to app.databiomes.com for model generation.
   """
   from model_train_protocol.prototyping import generate_prototype_protocol
   
   prompt_id: str = "pmpt_68e...4a0"  # Replace with your actual prompt ID
   openai_api_key: str = "sk-..."  # Replace with your actual OpenAI API key OR set the OPENAI_API_KEY environment variable
   
   generate_prototype_protocol(prompt_id=prompt_id,
                               openai_api_key=openai_api_key,  # Set to None to use environment variable
                               file_path=None,  # Saves to current directory,
                               name=None,  # Uses model generated name
                               encrypt=False  # Whether to encrypt the protocol file
                               )

That's it! Your MTP protocol file has been generated and saved.

What's Next?
------------

- **Quick Start Guide**: Step-by-step tutorial to get you running
- **Advanced Usage**: Complex patterns, batch processing, and customization
- **API Reference**: Complete documentation of all functions and classes

.. toctree::
   :maxdepth: 2
   :caption: Prototyping Documentation:

   quickstart
