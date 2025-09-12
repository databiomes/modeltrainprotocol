Instructions: Training Patterns
===============================

Instructions define how the model should respond to different input patterns. There are two main types of instructions.

SimpleInstruction
-----------------

For scenarios where the model responds without user input.

Parameters
~~~~~~~~~~

- **context**: Sequence of TokenSets that provide background information
- **response**: The TokenSet that defines the model's response pattern (cannot contain UserTokens)
- **final**: A Token that represents the final action or result. E.g. "Continue", "End", "Explode"

Creating SimpleInstructions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Create TokenSets
   cat_pondering = mtp.TokenSet(tokens=(tree, cat, ponder))
   cat_grinning = mtp.TokenSet(tokens=(tree, cat, grin))

   # Create a simple instruction for the Cat's internal thoughts
   instruction = mtp.SimpleInstruction(
       context=[cat_pondering],
       response=cat_grinning,
       final=disappear
   )

Adding Samples to SimpleInstructions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**add_sample() parameters**:

- **context_snippets**: List of context snippets that will be added to the Instruction
- **output_snippet**: The model's output snippet
- **value**: Optional numerical value (required if final Token is a NumToken)

.. code-block:: python

   # Samples must be made on their associated TokenSets
   sample_context = cat_pondering.create_snippet(
       string="Why do I keep vanishing and reappearing so suddenly?"
   )
   sample_output = cat_grinning.create_snippet(
       string="Because it amuses me, and it keeps everyone wondering whether I'm truly here at all."
   )

   instruction.add_sample(
       context_snippets=[sample_context],
       output_snippet=sample_output
   )

UserInstruction
---------------

For scenarios where the model responds to user prompts.

Parameters
~~~~~~~~~~

- **context**: Sequence of TokenSets that provide background information
- **user**: A TokenSet that must include at least one UserToken
- **final**: A Token that represents the final action or result

Creating UserInstructions
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Create TokenSets for Alice and Cat interaction
   alice_talk = mtp.TokenSet(tokens=(tree, alice, talk))
   cat_talk = mtp.TokenSet(tokens=(tree, cat, talk))

   # Create a user instruction for Alice asking the Cat questions
   user_instruction = mtp.UserInstruction(
       context=[alice_talk],
       user=alice_talk,  # Must contain at least one UserToken
       final=disappear
   )

Adding Samples to UserInstructions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**add_sample() parameters**:

- **context_snippets**: List of context snippets that will be added to the Instruction
- **prompt**: The prompt provided by the user
- **output_snippet**: The model's output snippet
- **value**: Optional numerical value (required if final Token is a NumToken)

.. code-block:: python

   # Samples must be made on their associated TokenSets
   sample_context = alice_talk.create_snippet(
       string="I don't much care where—"
   )
   sample_output = cat_talk.create_snippet(
       string="Then it doesn't matter which way you go."
   )

   user_instruction.add_sample(
       context_snippets=[sample_context],
       prompt="Can you tell me which way I ought to go?",
       output_snippet=sample_output
   )

Instruction Patterns
--------------------

Conversational Patterns
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Conversational instruction
   conversation_context = mtp.TokenSet(tokens=(speaker, context))
   conversation_response = mtp.TokenSet(tokens=(responder, response))

   conversation_instruction = mtp.SimpleInstruction(
       context=[conversation_context],
       response=conversation_response,
       final=mtp.Token("Continue")
   )

Question-Answer Patterns
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Q&A instruction
   question_context = mtp.TokenSet(tokens=(question, context))
   answer_response = mtp.TokenSet(tokens=(answer, response))

   qa_instruction = mtp.SimpleInstruction(
       context=[question_context],
       response=answer_response,
       final=mtp.Token("Complete")
   )

Interactive Patterns
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Interactive instruction with user input
   user_context = mtp.TokenSet(tokens=(user, context))
   system_response = mtp.TokenSet(tokens=(system, response))

   interactive_instruction = mtp.UserInstruction(
       context=[user_context],
       user=user_context,
       final=mtp.Token("Respond")
   )

Multi-Step Instructions
-----------------------

Complex instructions with multiple context steps:

.. code-block:: python

   # Multi-step instruction
   step1_context = mtp.TokenSet(tokens=(step1, context))
   step2_context = mtp.TokenSet(tokens=(step2, context))
   final_response = mtp.TokenSet(tokens=(final, response))

   multi_step_instruction = mtp.SimpleInstruction(
       context=[step1_context, step2_context],
       response=final_response,
       final=mtp.Token("Complete")
   )

Conditional Instructions
~~~~~~~~~~~~~~~~~~~~~~~~

Instructions that depend on specific conditions:

.. code-block:: python

   # Conditional instruction
   condition_context = mtp.TokenSet(tokens=(condition, context))
   conditional_response = mtp.TokenSet(tokens=(conditional, response))

   conditional_instruction = mtp.SimpleInstruction(
       context=[condition_context],
       response=conditional_response,
       final=mtp.Token("Conditional")
   )

Best Practices
--------------

1. **Clear Context**: Provide clear context that helps the model understand the situation
2. **Appropriate Responses**: Ensure responses match the expected behavior
3. **Consistent Patterns**: Use consistent instruction patterns throughout your protocol
4. **Adequate Samples**: Provide enough samples to train the model effectively
5. **Proper Token Usage**: Use the correct token types for each instruction component

Instruction Validation
----------------------

The MTP system ensures that:

- All TokenSets in instructions are properly defined
- UserInstructions contain at least one UserToken
- SimpleInstructions do not contain UserTokens in the response
- All samples match the defined instruction structure
- Final tokens are appropriate for the instruction type

Common Instruction Types
------------------------

Educational Instructions
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Educational instruction
   lesson_context = mtp.TokenSet(tokens=(lesson, topic, level))
   explanation_response = mtp.TokenSet(tokens=(explanation, detail, example))

   educational_instruction = mtp.SimpleInstruction(
       context=[lesson_context],
       response=explanation_response,
       final=mtp.Token("Learned")
   )

Creative Instructions
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Creative instruction
   creative_context = mtp.TokenSet(tokens=(creative, prompt, style))
   creative_response = mtp.TokenSet(tokens=(creative, output, result))

   creative_instruction = mtp.SimpleInstruction(
       context=[creative_context],
       response=creative_response,
       final=mtp.Token("Created")
   )

Analytical Instructions
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Analytical instruction
   analysis_context = mtp.TokenSet(tokens=(analysis, data, method))
   analysis_response = mtp.TokenSet(tokens=(analysis, result, conclusion))

   analytical_instruction = mtp.SimpleInstruction(
       context=[analysis_context],
       response=analysis_response,
       final=mtp.Token("Analyzed")
   )

Advanced Instruction Features
-----------------------------

Dynamic Instructions
~~~~~~~~~~~~~~~~~~~~

Instructions that adapt based on input:

.. code-block:: python

   # Dynamic instruction with multiple possible responses
   dynamic_context = mtp.TokenSet(tokens=(dynamic, context, condition))
   dynamic_response = mtp.TokenSet(tokens=(dynamic, response, adaptation))

   dynamic_instruction = mtp.SimpleInstruction(
       context=[dynamic_context],
       response=dynamic_response,
       final=mtp.Token("Adapted")
   )

Hierarchical Instructions
~~~~~~~~~~~~~~~~~~~~~~~~~

Instructions with nested or hierarchical structures:

.. code-block:: python

   # Hierarchical instruction
   parent_context = mtp.TokenSet(tokens=(parent, context))
   child_context = mtp.TokenSet(tokens=(child, context, parent))
   hierarchical_response = mtp.TokenSet(tokens=(hierarchical, response, level))

   hierarchical_instruction = mtp.SimpleInstruction(
       context=[parent_context, child_context],
       response=hierarchical_response,
       final=mtp.Token("Hierarchical")
   )
