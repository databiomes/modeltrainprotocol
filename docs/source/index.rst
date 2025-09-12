Model Training Protocol (MTP)
=============================

MTP is an open-source protocol for training custom Language Models on Databiomes. MTP contains all the data that a model is trained on.

The MTP system is built on a hierarchical structure of four main components:

1. **Tokens** - The fundamental building blocks
2. **TokenSets** - Combinations of tokens that define input patterns  
3. **Instructions** - Training patterns that inform the model what to do
4. **Guardrails** - Safety mechanisms for bad user prompts

.. toctree::
   :maxdepth: 2
   :caption: Documentation:

   getting_started
   system_architecture
   tokens
   tokensets
   snippets
   instructions
   guardrails
   saving_models
   api_reference

