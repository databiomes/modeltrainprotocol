Context
============================

Context is a foundational layer of the Model Training Protocol (MTP) system. It provides the background information and domain knowledge that helps the model understand the training data and respond appropriately in the intended context.

What is Context?
----------------

Context in MTP refers to the background information, domain knowledge, and setting that establishes the foundation for all training data. It helps the model understand:

- The domain or subject area (e.g., "medical diagnosis", "creative writing", "customer service")
- The setting or environment (e.g., "Alice in Wonderland", "modern office", "medieval fantasy")
- Key concepts and terminology specific to the domain
- The tone and style expected in responses
- Any constraints or guidelines for the model's behavior

Why Context Matters
-------------------

Context serves several critical functions:

1. **Domain Understanding**: Provides the model with essential background knowledge about the subject matter
2. **Consistency**: Ensures all training examples are interpreted within the same conceptual framework
3. **Appropriate Responses**: Helps the model generate responses that are contextually appropriate
4. **Reduced Ambiguity**: Clarifies ambiguous terms and concepts that might have different meanings in different contexts

Adding Context to Your Protocol
-------------------------------

Context is added to your protocol using the ``add_context()`` method. You can add multiple context lines to provide comprehensive background information.


Instruction Context Snippets
----------------------------
Context snippets, set as instruction_context_snippets when initializing the protocol, refers to how many snippets of context are provided to each Instruction.
Context snippets does NOT refer to the amount of total context that your model has.

Each Instruction in the protocol must have the same number of context snippets as specified when initializing the protocol.

This is not to be confused with the context added to the protocol using the ``add_context()`` method, which can be any number of lines.

A minimum of 2 instruction_context_snippets are required.

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   import model_train_protocol as mtp

   # Initialize the protocol
   protocol = mtp.Protocol(name="my_model", instruction_context_snippets=2)

   # Add context
   protocol.add_context("The Cheshire Cat is a fictional character from Lewis Carroll's 'Alice's Adventures in Wonderland'.")
   protocol.add_context("The Cheshire Cat is known for its distinctive mischievous grin and its ability to disappear and reappear at will.")
   protocol.add_context("The Cat often speaks in riddles and philosophical musings, adding a whimsical and enigmatic element to the story.")

Context Examples
----------------

Storytelling Context
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Fantasy storytelling context
   protocol.add_context("This is a medieval fantasy world with magic, dragons, and heroic quests.")
   protocol.add_context("The story follows a young mage learning to control their powers.")
   protocol.add_context("Magic is governed by ancient laws and requires both knowledge and willpower.")

Educational Context
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Educational tutoring context
   protocol.add_context("You are a patient and encouraging math tutor for middle school students.")
   protocol.add_context("Explain concepts clearly using simple language and relatable examples.")
   protocol.add_context("Always show your work step-by-step and encourage questions.")

Customer Service Context
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Customer service context
   protocol.add_context("You are a helpful customer service representative for a tech company.")
   protocol.add_context("Always be polite, professional, and solution-oriented.")
   protocol.add_context("If you cannot solve a problem, escalate to a specialist.")

Best Practices for Context
--------------------------

1. **Be Specific**: Provide clear, specific information about the domain and setting
2. **Be Comprehensive**: Include all relevant background information the model needs
3. **Be Consistent**: Ensure all context lines work together to create a coherent framework
4. **Consider Your Audience**: Tailor the context to the intended use case and user base
5. **More Is Better**: The more context you provide, the better your model will perform.

Example: Complete Context Setup
-------------------------------

Here's a complete example of setting up context for a creative writing assistant:

.. code-block:: python

   import model_train_protocol as mtp

   # Initialize the protocol
   protocol = mtp.Protocol(name="creative_writing_assistant", instruction_context_snippets=2)

   # Add comprehensive context
   protocol.add_context("You are a creative writing assistant specializing in fantasy and science fiction.")
   protocol.add_context("Your role is to help writers develop compelling characters, engaging plots, and immersive worlds.")
   protocol.add_context("You provide constructive feedback, creative suggestions, and writing techniques.")
   protocol.add_context("You encourage experimentation while maintaining narrative coherence and reader engagement.")
   protocol.add_context("Your responses should be inspiring, detailed, and actionable for writers of all skill levels.")

   # Now you can proceed with defining tokens, tokensets, and instructions
   # that all work within this creative writing context

Next Steps
----------

After establishing your context, you can proceed to:

- :doc:`../instructions/tokens` - Define the fundamental building blocks within your context
- :doc:`../instructions/tokensets` - Create meaningful patterns that fit your domain
- :doc:`../instructions/instructions` - Teach the model how to respond appropriately in your context
