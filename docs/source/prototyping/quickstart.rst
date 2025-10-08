Quick Start Guide
==================

This guide will help you get started with the prototyping module in just a few minutes.

Prerequisites
-------------

1. **OpenAI Account**: You need an OpenAI account with API access
2. **Python Environment**: Python 3.8+ with the model_train_protocol package installed
3. **API Key**: Your OpenAI API key (get it from https://platform.openai.com/api-keys)

Installation
------------

.. code-block:: bash

   pip install model_train_protocol

Environment Setup
------------------

Set your OpenAI API key:

.. code-block:: bash

   export OPENAI_API_KEY="sk-your-api-key-here"

Or create a `.env` file:

.. code-block:: text

   OPENAI_API_KEY=sk-your-api-key-here

Basic Usage
-----------

1. **Create a Prompt in OpenAI**
   
   Go to https://platform.openai.com/prompts and create a new prompt. For example:
   
   .. code-block:: text
   
      "Create a model that helps users with home repair tasks. The model should provide step-by-step instructions for common repairs like fixing leaky faucets, replacing light switches, and patching drywall."
   
   .. figure:: ../../images/prototyping/create-openai-prompt.png
      :alt: Creating a prompt in OpenAI interface
      :width: 100%
      :align: center
      
      Creating a new prompt in the OpenAI interface.

2. **Get Your Prompt ID**
   
   Copy the prompt ID (starts with "pmpt_") from the OpenAI interface.

3. **Generate Your Protocol**
   
   .. code-block:: python
   
      from model_train_protocol.prototyping import generate_prototype_protocol
      
      # Generate a prototype protocol
      protocol = generate_prototype_protocol(
          prompt_id="pmpt_68e5abc123def456"
      )
      
      print(f"Generated protocol: {protocol.name}")

That's it! Your MTP protocol file has been generated and saved. You will see a file like this.

.. figure:: ../../images/prototyping/generated-protocol-json.png
   :alt: Generated MTP protocol JSON file
   :width: 100%
   :align: center
   
   The generated MTP protocol file contains all the training data for your model.

Next Steps
----------

- Review the generated protocol file
- Customize the protocol if needed
- Submit to `Databiomes <https://app.databiomes.com/agent/new>`_ for model training

.. figure:: ../../images/prototyping/upload-json-empty.png
   :alt: Uploading JSON file to Databiomes
   :width: 100%
   :align: center
   
   Upload your generated MTP protocol file to Databiomes for model training.

4. **Monitor Training Progress**
   
   Once uploaded, you can monitor your model's training progress in the Databiomes interface.

.. figure:: ../../images/prototyping/trained-databiomes-model.png
   :alt: Trained model in Databiomes
   :width: 100%
   :align: center
   
   Your trained model will appear in the Databiomes interface once training is complete.
