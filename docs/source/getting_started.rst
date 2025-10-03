Getting Started
===============

Installation
------------

Install the package:

For Linux and macOS:
::

   python3 -m pip install model-train-protocol

For Windows:
::

   py -3 -m pip install model-train-protocol

Quick Start
-----------

See ``examples/example.py`` to follow along with these steps.

The first step in creating a model training protocol is to initialize the Protocol:

.. code-block:: python

   import model_train_protocol as mtp

   # Initialize the protocol
   protocol = mtp.Protocol(name="my_model", instruction_context_snippets=2)

The parameter ``instruction_context_snippets`` is the number of lines in each instruction sample. This is required and must be at least 2.

Basic Example
-------------

Here's a simple example of a protocol to train a Chesire Cat model:

.. code-block:: python

   import model_train_protocol as mtp

   # Initialize the protocol
   protocol = mtp.Protocol(name="my_model", instruction_context_snippets=2)

   # Add context to the protocol
    protocol.add_context("The Cheshire Cat is a fictional character from Lewis Carroll's 'Alice's Adventures in Wonderland'.")
    protocol.add_context("The Cheshire Cat is known for its distinctive mischievous grin and its ability to disappear and reappear at will.")
    protocol.add_context("The Cat often speaks in riddles and philosophical musings, adding a whimsical and enigmatic element to the story.")

   # Create some tokens to represent characters and actions
   alice = mtp.Token("Alice")
   cat = mtp.Token("Cat", desc="The Cheshire Cat")
   tree = mtp.Token("Tree", desc="Perched in a tree")
   talk = mtp.Token("Talk")
   end = mtp.Token("End")

   # Create a TokenSet
   alice_talk = mtp.TokenSet(tokens=(alice, talk))
   cat_tree_talk = mtp.TokenSet(tokens=(cat, tree, talk))

   # Create a simple instruction using the TokenSets
   instruction = mtp.SimpleInstruction(
       context=[alice_talk],
       response=cat_tree_talk,
       final=end
   )

   # Create a conversation snippet
   cat_snippet_1 = cat_tree_talk.create_snippet(string="Hello, Alice. It's a pleasure to see you again.")
   alice_snippet = alice_talk.create_snippet(string="Why does your smile seem to linger even when you're not around?")
   cat_snippet_2 = cat_tree_talk.create_snippet(string="Oh, I'm always around, just in ways you might not expect.")

   # Add a sample
   instruction.add_sample(
       context_snippets=[cat_snippet_1, alice_snippet],
       output_snippet=cat_snippet_2
   )

   # (A minimum of 3 samples are required in each instruction)
   # add 2 more samples similarly...

   # Add instruction to protocol
   protocol.add_instruction(instruction)

   # Save the protocol
   protocol.save()
   protocol.template()


See a detailed example in ``examples/example.py``.

Next Steps
----------

Now that you have the basics, explore the following sections:

- :doc:`system_architecture` - Understand the overall system design
- :doc:`context` - Learn how to add background information and domain knowledge
- :doc:`tokens` - Learn about the fundamental building blocks
- :doc:`tokensets` - Combine tokens into meaningful patterns
- :doc:`instructions` - Create training patterns for your model
- :doc:`guardrails` - Add safety mechanisms
- :doc:`saving_models` - Save and deploy your protocol
