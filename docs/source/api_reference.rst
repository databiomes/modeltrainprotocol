API Reference
=============

This section provides comprehensive API documentation for the Model Training Protocol (MTP) package.

Core Classes
------------

Protocol
~~~~~~~~

The main Protocol class for creating model training protocols.

.. code-block:: python

   class Protocol:
       def __init__(self, name: str, instruction_context_snippets: int):
           """Initialize the Model Training Protocol (MTP)"""
           
       def add_context(self, context: str):
           """Adds a line of context to the model."""
           
       def add_instruction(self, instruction: Instruction):
           """Adds an Instruction (and its components) to the protocol."""
           
       def save(self, name: str | None = None, path: str | None = None):
           """Saves the training protocol to a JSON file."""
           
       def template(self, path: str | None = None):
           """Create a usage template JSON file for the model."""

Tokens
------

Token
~~~~~

Basic token class for representing concepts, actions, or entities.

.. code-block:: python

   class Token:
       def __init__(self, value: str, key: str = None, desc: str = None):
           """Initialize a Token with value, optional key, and optional description."""

UserToken
~~~~~~~~~

Specialized token for representing user input.

.. code-block:: python

   class UserToken(Token):
       def __init__(self, value: str, key: str = None, desc: str = None):
           """Initialize a UserToken for user input scenarios."""

NumToken
~~~~~~~~

Token that can be associated with numerical values.

.. code-block:: python

   class NumToken(Token):
       def __init__(self, value: str, key: str = None, desc: str = None):
           """Initialize a NumToken for numerical data."""

TokenSet
--------

Groups multiple tokens together to define input patterns.

.. code-block:: python

   class TokenSet:
       def __init__(self, tokens: Sequence[Token]):
           """Initialize a TokenSet with a list of tokens."""
           
       def create_snippet(self, string: str, numbers: list = None):
           """Create a snippet from this TokenSet."""

Instructions
------------

Instruction
~~~~~~~~~~~~~~~~~

For scenarios where the model responds without user input.

.. code-block:: python

   class Instruction:
       def __init__(self, context: tuple, response: TokenSet, final: Token):
           """Initialize a Instruction."""
           
       def add_sample(self, context_snippets: list, output_snippet: Snippet, value=None):
           """Add a training sample to the instruction."""

UnsetInstruction
~~~~~~~~~~~~~~~

For scenarios where the model responds to user prompts.

.. code-block:: python

   class UnsetInstruction:
       def __init__(self, context: tuple, user: TokenSet, final: Token):
           """Initialize a UnsetInstruction."""
           
       def add_sample(self, context_snippets: list, prompt: str, output_snippet: Snippet, value=None):
           """Add a training sample to the instruction."""

Guardrails
----------

Safety mechanisms for user interactions.

.. code-block:: python

   class Guardrail:
       def __init__(self, good_prompt: str, bad_prompt: str, bad_output: str):
           """Initialize a Guardrail with prompt descriptions and bad output."""
           
       def add_sample(self, bad_prompt_example: str):
           """Add an example of a bad prompt."""

Module Structure
----------------

The MTP package is organized as follows:

::

   model_train_protocol/
   ├── __init__.py              # Main package exports
   ├── Protocol.py              # Core Protocol class
   └── common/
       ├── tokens/              # Token-related classes
       │   ├── Token.py
       │   ├── UserToken.py
       │   ├── NumToken.py
       │   ├── TokenSet.py
       │   └── Snippet.py
       ├── instructions/        # Instruction classes
       │   ├── Instruction.py
       │   ├── UnsetInstruction.py
       │   └── Instruction.py
       └── guardrails/          # Guardrail classes
           └── Guardrail.py

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
