API Reference
=============

This section provides detailed API documentation for the prototyping module.

Entry Point
-----------

.. py:function:: generate_prototype_protocol(prompt_id: str, openai_api_key: str | None = None, file_path: str | None = None, name: str | None = None, encrypt: bool = False) -> Protocol

   Generates a protocol file prototype based on a given prompt ID using OpenAI's API.

   **Parameters:**
   
   - ``prompt_id`` (str): The prompt ID from OpenAI (e.g., pmpt_68e5....9a72)
   - ``openai_api_key`` (str, optional): OpenAI API key. If None, loads from OPENAI_API_KEY environment variable
   - ``file_path`` (str, optional): File path to save the generated protocol file. If None, saves in current directory
   - ``name`` (str, optional): Name of the protocol file. If None, uses model-generated name
   - ``encrypt`` (bool): Whether to encrypt the protocol file (default: False)

   **Returns:**
   
   - ``Protocol``: The generated Protocol instance

   **Raises:**
   
   - ``ValueError``: If OpenAI response parsing fails
   - ``requests.exceptions.HTTPError``: If OpenAI API request fails
   - ``requests.exceptions.RequestException``: If network error occurs

   **Example:**
   
   .. code-block:: python
   
      from model_train_protocol.prototyping import generate_prototype_protocol
      
      protocol = generate_prototype_protocol(
          prompt_id="pmpt_68e5abc123def456",
          name="my_model",
          encrypt=True
      )

Translator Functions
--------------------

.. py:function:: translate_prototype(prototype_mtp: MTPPrototypeModel, name: str | None = None, encrypt: bool = False) -> Protocol

   Translates a generated MTP prototype into a Protocol object.

   **Parameters:**
   
   - ``prototype_mtp`` (MTPPrototypeModel): The generated MTP prototype from OpenAI API
   - ``name`` (str, optional): Name for the protocol. If None, uses prototype's model name
   - ``encrypt`` (bool): Whether to encrypt the protocol (default: False)

   **Returns:**
   
   - ``Protocol``: A fully configured Protocol object ready for training

   **Example:**
   
   .. code-block:: python
   
      from model_train_protocol.prototyping import translate_prototype
      
      protocol = translate_prototype(
          prototype_mtp=prototype,
          name="custom_name",
          encrypt=True
      )

Utility Functions
-----------------

Token Processing
~~~~~~~~~~~~~~~~

.. py:function:: clean_token_key(key: str) -> str

   Removes non-alphanumeric characters from a token key, keeping only alphanumeric characters and underscores.

   **Parameters:**
   
   - ``key`` (str): The token key to clean

   **Returns:**
   
   - ``str``: Cleaned token key

   **Example:**
   
   .. code-block:: python
   
      from model_train_protocol.prototyping import clean_token_key
      
      clean_key = clean_token_key("my-dirty@token!")  # "mydirtytoken"

.. py:function:: convert_str_to_camel_case(snake_str: str) -> str

   Converts a snake_case string to camelCase format.

   **Parameters:**
   
   - ``snake_str`` (str): The snake_case string to convert

   **Returns:**
   
   - ``str``: The converted camelCase string

   **Example:**
   
   .. code-block:: python
   
      from model_train_protocol.prototyping import convert_str_to_camel_case
      
      camel = convert_str_to_camel_case("my_snake_case")  # "mySnakeCase"

.. py:function:: create_sanitized_token_from_model(token_info_model: TokenInfoPrototypeModel) -> Token

   Creates a cleaned Token object from a token info model, applying key cleaning and case conversion.

   **Parameters:**
   
   - ``token_info_model`` (TokenInfoPrototypeModel): The token info model to convert

   **Returns:**
   
   - ``Token``: A sanitized Token object

   **Example:**
   
   .. code-block:: python
   
      from model_train_protocol.prototyping import create_sanitized_token_from_model
      
      token = create_sanitized_token_from_model(token_info_model)

.. py:function:: create_token_set_from_token_model_array(token_info_models: list[TokenInfoPrototypeModel]) -> TokenSet

   Creates a TokenSet from an array of token info models, handling deduplication.

   **Parameters:**
   
   - ``token_info_models`` (list[TokenInfoPrototypeModel]): Array of token info models

   **Returns:**
   
   - ``TokenSet``: A TokenSet containing the processed tokens

   **Example:**
   
   .. code-block:: python
   
      from model_train_protocol.prototyping import create_token_set_from_token_model_array
      
      token_set = create_token_set_from_token_model_array(token_models)

Provider Functions
------------------

OpenAI Provider
~~~~~~~~~~~~~~~

.. py:function:: generate_mtp_prototype_file(prompt_id: str, openai_api_key: str | None = None) -> MTPPrototypeModel

   Calls the OpenAI API to generate an MTP prototype based on the provided prompt ID.

   **Parameters:**
   
   - ``prompt_id`` (str): OpenAI prompt ID
   - ``openai_api_key`` (str, optional): API key. If None, loads from environment

   **Returns:**
   
   - ``MTPPrototypeModel``: Structured prototype data

   **Raises:**
   
   - ``ValueError``: If API response parsing fails
   - ``requests.exceptions.HTTPError``: If API request fails
   - ``requests.exceptions.RequestException``: If network error occurs

   **Example:**
   
   .. code-block:: python
   
      from model_train_protocol.prototyping import generate_mtp_prototype_file
      
      prototype = generate_mtp_prototype_file("pmpt_68e5abc123def456")

Data Models
-----------

MTPPrototypeModel
~~~~~~~~~~~~~~~~~

.. py:class:: MTPPrototypeModel

   The main model representing the complete MTP prototype.

   **Attributes:**
   
   - ``model_name`` (str): Name of the model this prototype is for
   - ``context`` (List[ContextItemModel]): Array of context items (minimum 5)
   - ``instruction_sets`` (List[InstructionSetModel]): Array of instruction sets (minimum 3)

   **Example:**
   
   .. code-block:: python
   
      prototype = MTPPrototypeModel(
          model_name="MyModel",
          context=[...],
          instruction_sets=[...]
      )

ContextItemModel
~~~~~~~~~~~~~~~

.. py:class:: ContextItemModel

   Represents individual context items.

   **Attributes:**
   
   - ``context`` (str): Description explaining an aspect of the developer message context

   **Example:**
   
   .. code-block:: python
   
      context_item = ContextItemModel(
          context="This model helps with home repair tasks"
      )

InstructionSetModel
~~~~~~~~~~~~~~~~~~

.. py:class:: InstructionSetModel

   Represents a complete instruction set.

   **Attributes:**
   
   - ``instruction`` (str): Instruction derived from the developer message
   - ``prompt`` (str): Possible user question or prompt
   - ``response`` (str): Response using the developer message context
   - ``samples`` (List[Sample]): Array of sample interactions (minimum 3)

   **Example:**
   
   .. code-block:: python
   
      instruction_set = InstructionSetModel(
          instruction="Help with plumbing repairs",
          prompt="How do I fix a leaky faucet?",
          response="Here's how to fix a leaky faucet...",
          samples=[...]
      )

Sample
~~~~~~

.. py:class:: Sample

   Represents individual sample interactions.

   **Attributes:**
   
   - ``prompt_context`` (str): Context for the specific instruction
   - ``prompt_sample`` (str): Sample user prompt
   - ``response_sample`` (str): Sample model response

   **Example:**
   
   .. code-block:: python
   
      sample = Sample(
          prompt_context="Plumbing repair context",
          prompt_sample="How do I fix a leak?",
          response_sample="First, turn off the water supply..."
      )

TokenInfoPrototypeModel
~~~~~~~~~~~~~~~~~~~~~~~

.. py:class:: TokenInfoPrototypeModel

   Represents token information in prototypes.

   **Attributes:**
   
   - ``value`` (str): The token value string
   - ``desc`` (str): Description of the token's purpose

   **Example:**
   
   .. code-block:: python
   
      token_info = TokenInfoPrototypeModel(
          value="Plumbing",
          desc="Related to plumbing repairs and maintenance"
      )

Constants
---------

GENERATE_MTP_TOOL
~~~~~~~~~~~~~~~~~~

.. py:data:: GENERATE_MTP_TOOL

   The OpenAI function definition for the generate_mtp tool.

TOKEN_MODEL
~~~~~~~~~~~

.. py:data:: TOKEN_MODEL

   Reusable token model definition for OpenAI API.

FINAL_TOKEN_MODEL
~~~~~~~~~~~~~~~~~

.. py:data:: FINAL_TOKEN_MODEL

   Token model definition for final action tokens.
