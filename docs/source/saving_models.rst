Saving Your Model
=================

Once you've created your tokens, instructions, and guardrails, you can save your model training protocol.

Saving the Protocol
-------------------

.. code-block:: python

   # Save the protocol
   protocol.save()
   protocol.template() # optional template file

Generated Files
---------------

When you save your model, two files are created:

Model File: ``{name}_model.json``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the main model training protocol file that contains:

- **Context**: All background information you added with ``protocol.add_context()``
- **Tokens**: All your custom tokens with their keys and properties
- **Special Tokens**: System tokens like ``<BOS>``, ``<EOS>``, ``<RUN>``, ``<PAD>``
- **Instructions**: All your training patterns and samples
- **Guardrails**: Safety mechanisms for user interactions
- **Numbers**: Number ranges for NumTokens

This file is what you submit to Databiomes for model training.

Template File: ``{name}_template.json``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a reference file that shows:

- **Example Usage**: Valid input/output format for your model
- **All Combinations**: Complete list of all possible token combinations
- **Model Input/Output**: Structure showing how data flows through your model

Use this file to understand how your model expects to receive and format data.

File Structure Example
----------------------

::

   my_model_model.json     # Main training protocol
   my_model_template.json  # Reference and examples

The template file helps you understand the expected format when using your trained model, while the model file contains all the training data needed to create your specialized language model.

Custom Save Locations
---------------------

You can specify custom locations for saving your files:

.. code-block:: python

   # Save to a specific directory
   protocol.save(path="/path/to/save/directory")
   protocol.template(path="/path/to/save/directory")

   # Save with a custom name
   protocol.save(name="custom_model_name")
   protocol.template(name="custom_template_name")

