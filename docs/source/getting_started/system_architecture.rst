System Architecture
====================

The MTP system is built on a hierarchical structure of five main components that work together to create comprehensive training protocols for language models.

Architecture Overview
---------------------

The five core components are:

1. **Context** - Background information and domain knowledge for the model
2. **Tokens** - The fundamental building blocks
3. **TokenSets** - Combinations of tokens that define input patterns
4. **Instructions** - Training patterns that inform the model what to do
5. **Guardrails** - Safety mechanisms for bad user prompts

Component Hierarchy
-------------------

Context
~~~~~~~

Context provides the foundational background information and domain knowledge that the model needs to understand the training data and respond appropriately.

- Context establishes the domain, setting, and background information
- It helps the model understand the context in which tokens, instructions, and responses should be interpreted
- Context is added to the protocol using the ``add_context()`` method

Tokens
~~~~~~

Tokens are the base building blocks of the MTP system. They represent words, symbols, concepts, or actions that the model will understand and use.

- **Basic Token**: Standard tokens for concepts, actions, or entities
- **UserToken**: Specialized tokens for user input
- **NumToken**: Tokens associated with numerical values

TokenSets
~~~~~~~~~

TokenSets group multiple Tokens together to define specific input patterns. They represent the structure of data that will be fed to the model.

- TokenSets are the basic building blocks of instructions
- They can contain any combination of token types
- Snippets are created on TokenSets to provide training examples

Instructions
~~~~~~~~~~~~

Instructions define how the model should respond to different input patterns. There are two main types:

- **Instruction**: For scenarios where the model responds without user input
- **ExtendedInstruction**: For scenarios where the model responds to user prompts

Guardrails
~~~~~~~~~~

Guardrails provide safety mechanisms for user interactions by defining what constitutes good vs. bad user prompts and how the model should respond to inappropriate inputs.

Data Flow
---------

1. **Context Establishment**: Add background information and domain knowledge
2. **Token Creation**: Define the basic building blocks
3. **TokenSet Assembly**: Combine tokens into meaningful patterns
4. **Snippet Generation**: Create training examples from TokenSets
5. **Instruction Definition**: Specify how the model should respond to TokenSet patterns
6. **Guardrail Application**: Add safety mechanisms

Best Practices
--------------

- Start with a clear understanding of your model's purpose
- Establish comprehensive context to provide domain knowledge and background information
- Define tokens that represent the core concepts in your domain
- Create TokenSets that capture meaningful input patterns
- Use instructions to teach the model appropriate responses
- Always include guardrails for user-facing applications
- Test your protocol with various examples before deployment
