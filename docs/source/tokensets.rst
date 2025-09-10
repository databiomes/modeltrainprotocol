TokenSets: Combining Tokens
===========================

TokenSets group multiple Tokens together to define specific input patterns. They represent the structure of data that will be fed to the model.

TokenSets are the basic building blocks of Instructions.

Creating TokenSets
------------------

Basic TokenSet Creation
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Create a TokenSet combining multiple tokens
   tree_alice_talk = mtp.TokenSet(tokens=(tree, alice, talk))

   # Create a TokenSet with sentence length
   character_context_sentence = mtp.TokenSet(tokens=(character, context, sentence_length))

TokenSet Properties
-------------------

- **tokens**: The tokens in the set (unordered)

TokenSet Validation
-------------------

The MTP system ensures that:

- All tokens in a TokenSet are valid and properly defined
- NumTokens have associated number ranges when used in snippets
- UserTokens are properly used in interactive scenarios
- TokenSets are used consistently across instructions

Example TokenSet Patterns
------------------------

Storytelling Patterns
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Storytelling TokenSets
   scene_setting = mtp.TokenSet(tokens=(scene, setting, time))
   character_dialogue = mtp.TokenSet(tokens=(character, dialogue, emotion)) # emotion is a NumToken for intensity
   plot_development = mtp.TokenSet(tokens=(plot, development, conflict))

Educational Patterns
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Educational TokenSets
   question_answer = mtp.TokenSet(tokens=(question, answer, subject))
   explanation_concept = mtp.TokenSet(tokens=(explanation, concept, level))
   example_application = mtp.TokenSet(tokens=(example, application, domain))

Interactive Patterns
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Interactive TokenSets
   user_input_response = mtp.TokenSet(tokens=(user, input, response))
   system_prompt_output = mtp.TokenSet(tokens=(system, prompt, output))
   feedback_improvement = mtp.TokenSet(tokens=(feedback, improvement, iteration))

