Snippets: Training Examples
===========================

Snippets are created on TokenSets to create training samples.

A Snippet is an example of a TokenSet being applied. Snippets tell the model the context of the input patterns.

A minimum of 3 snippets must be created per TokenSet.

Snippet Creation
----------------

Basic Snippet Creation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Create a snippet with just text
   tree_alice_snippet: Snippet = tree_alice_talk.create_snippet(string="Where am I?")

   # Create a snippet with text and and a number token
   character_context_snippet: Snippet = character_context_sentence.create_snippet(
       string="The enemy must be here somewhere.",
       numbers=[11]
   )
   # character_context_sentence is a TokenSet with a NumToken for sentence_length, thus a number is provided.


When a TokenSet contains multiple NumTokens, provide as many numbers as there are NumTokens in the TokenSet.

Snippet Types
-------------

Text Snippets
~~~~~~~~~~~~~

Simple text snippets for basic TokenSets:

.. code-block:: python

   # Basic text snippet
   greeting_snippet = greeting_tokenset.create_snippet(
       string="Hello, how are you today?"
   )

Number Snippets
~~~~~~~~~~~~~~~

Snippets that include numerical values for NumTokens:

.. code-block:: python

   # Snippet with numerical data
   age_snippet = person_age_tokenset.create_snippet(
       string="I am 25 years old",
       numbers=[25]
   )


Snippet Examples
----------------

Character Interaction
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Character interaction patterns
   character_speaking: TokenSet = mtp.TokenSet(tokens=(character, speak))
   character_thinking: TokenSet = mtp.TokenSet(tokens=(character, think))
   character_observing: TokenSet = mtp.TokenSet(tokens=(character, observe))

   speaking_snippet: Snippet = character_speaking.create_snippet(string="Hello there!")
   thinking_snippet: Snippet = character_thinking.create_snippet(string="I wonder what will happen next.")
   observing_snippet: Snippet = character_observing.create_snippet(string="The sky is clear and blue.")

Contextual Patterns
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Contextual patterns
   location_context: TokenSet = mtp.TokenSet(tokens=(location, context))
   time_context: TokenSet = mtp.TokenSet(tokens=(time, context))
   situation_context: TokenSet = mtp.TokenSet(tokens=(situation, context))

   location_snippet: Snippet = location_context.create_snippet(string="In a dark forest")
   time_snippet: Snippet = time_context.create_snippet(string="At midnight")
   situation_snippet: Snippet = situation_context.create_snippet(string="During a fierce battle")

User Interaction
~~~~~~~~~~~~~~~~

.. code-block:: python

   # User interaction patterns
   user_question: TokenSet = mtp.TokenSet(tokens=(user, question))
   user_request: TokenSet = mtp.TokenSet(tokens=(user, request))
   user_feedback: TokenSet = mtp.TokenSet(tokens=(user, feedback))

   question_snippet: Snippet = user_question.create_snippet(string="What is the meaning of life?")
   request_snippet: Snippet = user_request.create_snippet(string="Please tell me a story.")
   feedback_snippet: Snippet = user_feedback.create_snippet(string="I enjoyed that story!")

Advanced Snippet Patterns
-------------------------

Storytelling Patterns
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Storytelling TokenSets
   scene_setting: TokenSet = mtp.TokenSet(tokens=(scene, setting, time))
   character_dialogue: TokenSet = mtp.TokenSet(tokens=(character, dialogue, emotion)) # emotion is a NumToken for intensity
   plot_development: TokenSet = mtp.TokenSet(tokens=(plot, development, conflict))

   scene_snippet: Snippet = scene_setting.create_snippet(string="In a quiet village at dawn")
   dialogue_snippet: Snippet = character_dialogue.create_snippet(string="I can't believe this is happening!", numbers=[5]) # emotion intensity 5
   plot_snippet: Snippet = plot_development.create_snippet(string="The hero faces a tough choice.")

Educational Patterns
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Educational TokenSets
   question_answer: TokenSet = mtp.TokenSet(tokens=(question, answer, subject))
   explanation_concept: TokenSet = mtp.TokenSet(tokens=(explanation, concept, level))
   example_application: TokenSet = mtp.TokenSet(tokens=(example, application, domain))

   qa_snippet: Snippet = question_answer.create_snippet(string="What is photosynthesis?", numbers=[1]) # subject 1 = Biology
   explanation_snippet: Snippet = explanation_concept.create_snippet(string="Photosynthesis is the process by which green plants...", numbers=[2]) # level 2 = Intermediate
   example_snippet: Snippet = example_application.create_snippet(string="An example of photosynthesis is...", numbers=[3]) # domain 3 = Science

Interactive Patterns
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Interactive TokenSets
   user_input_response: TokenSet = mtp.TokenSet(tokens=(user, input, response))
   system_prompt_output: TokenSet = mtp.TokenSet(tokens=(system, prompt, output))
   feedback_improvement: TokenSet = mtp.TokenSet(tokens=(feedback, improvement, iteration))

   input_snippet: Snippet = user_input_response.create_snippet(string="Tell me a joke.", numbers=[1]) # response type 1 = Humorous
   output_snippet: Snippet = system_prompt_output.create_snippet(string="Here's a joke for you...", numbers=[2]) # output type 2 = Text
   improvement_snippet: Snippet = feedback_improvement.create_snippet(string="That joke was funny, but can you make it shorter?", numbers=[3]) # iteration 3 = Shorter

Snippet Validation
------------------

The MTP system ensures that:

- All snippets are created on valid TokenSets
- NumTokens have associated number ranges when used in snippets
- The number of numerical values matches the number of NumTokens in the TokenSet
- Snippets provide meaningful context for training

Example Snippet Patterns
-----------------------

Emotional Context
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Emotional context snippets
   happy_context: TokenSet = mtp.TokenSet(tokens=(emotion, context, intensity))
   sad_context: TokenSet = mtp.TokenSet(tokens=(emotion, context, intensity))
   excited_context: TokenSet = mtp.TokenSet(tokens=(emotion, context, intensity))

   happy_snippet: Snippet = happy_context.create_snippet(string="The sun is shining brightly today!", numbers=[8]) # intensity 8
   sad_snippet: Snippet = sad_context.create_snippet(string="The rain falls softly on the window.", numbers=[6]) # intensity 6
   excited_snippet: Snippet = excited_context.create_snippet(string="I can't wait for the adventure to begin!", numbers=[9]) # intensity 9

Temporal Context
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Temporal context snippets
   past_context: TokenSet = mtp.TokenSet(tokens=(time, context, duration))
   present_context: TokenSet = mtp.TokenSet(tokens=(time, context, duration))
   future_context: TokenSet = mtp.TokenSet(tokens=(time, context, duration))

   past_snippet: Snippet = past_context.create_snippet(string="Yesterday, I visited the old castle.", numbers=[1]) # duration 1 = Short
   present_snippet: Snippet = present_context.create_snippet(string="Right now, I'm walking through the garden.", numbers=[2]) # duration 2 = Medium
   future_snippet: Snippet = future_context.create_snippet(string="Tomorrow, I will start my journey.", numbers=[3]) # duration 3 = Long

Spatial Context
~~~~~~~~~~~~~~~

.. code-block:: python

   # Spatial context snippets
   indoor_context: TokenSet = mtp.TokenSet(tokens=(location, context, size))
   outdoor_context: TokenSet = mtp.TokenSet(tokens=(location, context, size))
   underground_context: TokenSet = mtp.TokenSet(tokens=(location, context, size))

   indoor_snippet: Snippet = indoor_context.create_snippet(string="Inside the cozy library", numbers=[2]) # size 2 = Medium
   outdoor_snippet: Snippet = outdoor_context.create_snippet(string="Under the vast open sky", numbers=[5]) # size 5 = Very Large
   underground_snippet: Snippet = underground_context.create_snippet(string="In the narrow tunnel", numbers=[1]) # size 1 = Small
