Model Train Protocol (MTP)
=============================

MTP is an open-source protocol for training custom Language Models on Databiomes. MTP contains all the data that a model is trained on.

The MTP system is built on a hierarchical structure of five main components:

1. **Context** - Background information and domain knowledge for the model
2. **Tokens** - The fundamental building blocks
3. **TokenSets** - Combinations of tokens that define input patterns  
4. **Instructions** - Training patterns that inform the model what to do
5. **Guardrails** - Safety mechanisms for bad user prompts

.. toctree::
   :maxdepth: 2
   :caption: Documentation:

   getting_started/index
   context/index
   instructions/index
   saving_models
   experimental/index

