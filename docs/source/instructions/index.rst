Instructions
=============

Instructions are the core training components that define how the model should behave. This section covers the hierarchical structure of MTP's instruction system.

MTP Instruction Hierarchy
-------------------------

The MTP system is built on a hierarchical structure where each component builds upon the previous one:

1. **Tokens** → The fundamental building blocks
2. **TokenSets** → Combinations of tokens that define input patterns  
3. **Instructions** → Training patterns that inform the model what to do
4. **Guardrails** → Safety mechanisms placed on tokensets to prevent harmful outputs

**How the Hierarchy Works:**

- **Tokens** are the basic units (words, concepts, actions)
- **TokenSets** group tokens together to create meaningful input patterns
- **Instructions** use tokensets to define complete training scenarios
- **Guardrails** are applied to tokensets to ensure safe and appropriate responses

This hierarchical approach allows you to build complex, nuanced training patterns while maintaining control over your model's behavior and safety.

.. toctree::
   :maxdepth: 2
   :caption: Instructions:

   tokens
   tokensets
   instructions
   guardrails
   samples/index
