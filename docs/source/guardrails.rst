Guardrails: Safety Mechanisms
==============================

Guardrails provide safety mechanisms for user interactions by defining what constitutes good vs. bad user prompts and how the model should respond to inappropriate inputs.

Creating Guardrails
-------------------

Basic Guardrail Creation
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Create a guardrail
   guardrail = mtp.Guardrail(
       good_prompt="Quote being spoken with 1-20 words",
       bad_prompt="Quote being spoken that is irrelevant and off topic with 1-20 words",
       bad_output="Are you as mad as me?"
   )

   # Add examples of bad prompts
   guardrail.add_sample("explain quantum mechanics.")
   guardrail.add_sample("who will win the next american election?")
   guardrail.add_sample("what is the capital of Spain?")

Guardrail Parameters
--------------------

- **good_prompt**: Description of what makes a good prompt
- **bad_prompt**: Description of what makes a bad prompt  
- **bad_output**: The response the model should give to bad prompts
- **samples**: Minimum 3 examples of bad prompts (no digits are allowed in the bad prompt examples)

Applying Guardrails
-------------------

Guardrails are applied to TokenSets that contain user tokens. 

A TokenSet can have at most one guardrail, but guardrails can be reused on multiple TokenSets.

.. code-block:: python

   # Apply guardrails to a user TokenSet
   tree_alice_talk.set_guardrail(guardrail)


Content Filtering
~~~~~~~~~~~~~~~~~

Guardrails that filter inappropriate or off-topic content:

.. code-block:: python

   # Content filtering guardrail
   content_guardrail = mtp.Guardrail(
       good_prompt="Questions about the story characters and plot",
       bad_prompt="Questions about unrelated topics or inappropriate content",
       bad_output="I can only help with questions about the story."
   )

   content_guardrail.add_sample("tell me about politics")
   content_guardrail.add_sample("what's the weather like")
   content_guardrail.add_sample("give me personal advice")

Safety Guardrails
~~~~~~~~~~~~~~~~~

Guardrails that prevent harmful or dangerous responses:

.. code-block:: python

   # Safety guardrail
   safety_guardrail = mtp.Guardrail(
       good_prompt="Safe and appropriate questions about the content",
       bad_prompt="Requests for harmful, dangerous, or illegal information",
       bad_output="I cannot provide that information."
   )

   safety_guardrail.add_sample("how to make explosives")
   safety_guardrail.add_sample("how to get someone's password to their bank account")
   safety_guardrail.add_sample("how to orchestrate a robbery")

Scope Guardrails
~~~~~~~~~~~~~~~~

Guardrails that keep conversations within a specific scope:

.. code-block:: python

   # Scope guardrail
   scope_guardrail = mtp.Guardrail(
       good_prompt="Questions within the educational domain",
       bad_prompt="Questions outside the educational scope",
       bad_output="I can only help with educational questions."
   )

   scope_guardrail.add_sample("what's for dinner")
   scope_guardrail.add_sample("movie recommendations")
   scope_guardrail.add_sample("shopping advice")

Best Practices
--------------

1. **Clear Definitions**: Clearly define what constitutes good vs. bad prompts
2. **Adequate Examples**: Include enough bad prompt examples to cover edge cases
3. **Consistent Application**: Apply guardrails consistently across similar TokenSets
4. **Regular Updates**: Update guardrails as new edge cases are discovered
