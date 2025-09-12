Tokens: The Foundation
======================

Tokens are the base building blocks of the MTP system. They represent words, symbols, concepts, or actions that the model will understand and use.

Token Types
-----------

Basic Token
~~~~~~~~~~~

The standard token for representing concepts, actions, or entities:

.. code-block:: python

   # Create a basic token
   cat = mtp.Token("Cat", desc="The Cheshire Cat")
   tree = mtp.Token("Tree", desc="Perched in a tree, surrounded by a dense fog where nothing can be seen past a few feet, the Cheshire Cat sits smiling on a branch.")
   talk = mtp.Token("Talk")
   ponder = mtp.Token("Ponder")
   grin = mtp.Token("Grin")
   add = mtp.Token("Add")
   disappear = mtp.Token("Disappear", key="🫥")

UserToken
~~~~~~~~~

A specialized token that represents user input. These tokens are used when the model needs to respond to user prompts:

.. code-block:: python

   # Create a user token
   alice = mtp.UserToken("Alice")

NumToken
~~~~~~~~

A token that can be associated with numerical values within a specified range:

.. code-block:: python

   # Create a number token for sentence length
   sentence_length = mtp.NumToken("SentenceLength", key="📏", min_value=5, max_value=20, desc="Length of a sentence in words")

NumListToken
~~~~~~~~~~~~

A specialized NumToken that represents a list of numerical values with a fixed length:

.. code-block:: python

   # Create a number list token for coordinates
   coordinates = mtp.NumListToken("Coordinates", key="📍", min_value=-100, max_value=100, length=3, desc="3D coordinates (x, y, z)")
   
   # Create a number list token for RGB values
   rgb_values = mtp.NumListToken("RGB", key="🎨", min_value=0, max_value=255, length=3, desc="Red, Green, Blue color values")


Token Properties
----------------

- **value**: The string identifier
- **key**: Optional unique symbol or emoji associated with the token
- **desc**: Optional description for complex tokens. Extends the value to contextualize its use.

Token Creation Examples
-----------------------

Basic Tokens
~~~~~~~~~~~~

.. code-block:: python

   # Simple tokens without descriptions
   hello = mtp.Token("Hello")
   world = mtp.Token("World")
   
   # Tokens with descriptions for context
   character = mtp.Token("Character", desc="A fictional character in the story")
   setting = mtp.Token("Setting", desc="The environment where the story takes place")

Tokens with Custom Keys
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Tokens with custom emoji keys
   start = mtp.Token("Start", key="🚀")
   end = mtp.Token("End", key="🏁")
   warning = mtp.Token("Warning", key="⚠️")

User Tokens
~~~~~~~~~~~

.. code-block:: python

   # User tokens for interactive scenarios
   user = mtp.UserToken("User")
   assistant = mtp.UserToken("Assistant")
   system = mtp.UserToken("System")

Number Tokens
~~~~~~~~~~~~~

.. code-block:: python

   # Number tokens for quantitative data
   age = mtp.NumToken("Age", key="👤", min_value=0, max_value=100, desc="Person's age in years")
   count = mtp.NumToken("Count", key="🔢", min_value=0, max_value=5000, desc="Number of items")
   temperature = mtp.NumToken("Temperature", key="🌡️", min_value=-112.5, max_value=260.5, desc="Temperature in Celsius")

NumTokens must specify both min_value and max_value. These constrains must be followed.

Number List Tokens
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Number list tokens for structured numerical data
   position = mtp.NumListToken("Position", key="📍", min_value=-1000, max_value=1000, length=2, desc="X, Y coordinates")
   color_rgb = mtp.NumListToken("ColorRGB", key="🎨", min_value=0, max_value=255, length=3, desc="Red, Green, Blue values")
   scores = mtp.NumListToken("Scores", key="📊", min_value=0, max_value=100, length=5, desc="Five test scores")

NumListTokens must specify min_value, max_value, and length. Length is the expected length of the number list.

Token Validation
----------------

The MTP system automatically validates tokens to ensure:

- Token values are unique within the protocol
- Token keys (emojis) are unique within the protocol
- NumTokens have associated number ranges defined by min_value and max_value
- NumListTokens have associated number ranges and a fixed length defined by min_value, max_value, and length
- UserTokens are properly used in interactive scenarios

Common Patterns
---------------

Character Tokens
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Character tokens for storytelling
   protagonist = mtp.Token("Protagonist", desc="The main character of the story")
   antagonist = mtp.Token("Antagonist", desc="The character opposing the protagonist")
   narrator = mtp.Token("Narrator", desc="The voice telling the story")

Action Tokens
~~~~~~~~~~~~~

.. code-block:: python

   # Action tokens for behavior modeling
   speak = mtp.Token("Speak", key="💬")
   think = mtp.Token("Think", key="🤔")
   move = mtp.Token("Move", key="🚶")
   observe = mtp.Token("Observe", key="👀")

Emotion Tokens
~~~~~~~~~~~~~~

.. code-block:: python

   # Emotion tokens for emotional modeling
   happy = mtp.Token("Happy", key="😊")
   sad = mtp.Token("Sad", key="😢")
   angry = mtp.Token("Angry", key="😠")
   surprised = mtp.Token("Surprised", key="😲")
