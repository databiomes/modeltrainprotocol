View the full package documentation at: https://docs.databiomes.com/training/mtp/getting-started/

# Model Train Protocol (MTP)

MTP is an open-source protocol for training custom Language Models on Databiomes. MTP contains all the data that a model is trained on.

## Getting Started

Note Python 3.13 or higher is required.

Install the package:

For Linux and macOs
```bash
python3 -m pip install model-train-protocol
```

For Windows
```bash
py -3 -m pip install model-train-protocol
```

See examples/example.py to follow along with these steps.

# Creating a Model Train Protocol

The first step in creating a model training protocol is to initialize the Protocol:

```python
import model_train_protocol as mtp

# Initialize the protocol
protocol = mtp.Protocol(name="my_model", inputs=2, encrypt=False)
```

The parameter `inputs` is the number of lines in each Instruction's Input. Must be at least 2.
`encrypt` is an optional flag depending on how you plan to export and use the protocol.

## System Architecture

The MTP system is built on a hierarchical structure of four main components:

1. **Tokens** - The fundamental building blocks
2. **TokenSets** - Combinations of tokens that define input patterns
3. **Instructions** - Training patterns that inform the model what to do
4. **Guardrails** - Safety mechanisms for bad user prompts

## Tokens: The Foundation

Tokens are the base building blocks of the MTP system. They represent words, symbols, concepts, or actions that the model will understand and use.

### Token Types

#### Basic Token
The standard token for representing concepts, actions, or entities:

```python
# Create a basic token
cat = mtp.Token("Cat", desc="The Cheshire Cat")
tree = mtp.Token("Tree", desc="Perched in a tree, surrounded by a dense fog where nothing can be seen past a few feet, the Cheshire Cat sits smiling on a branch.")
talk = mtp.Token("Talk")
ponder = mtp.Token("Ponder")
grin = mtp.Token("Grin")
add = mtp.Token("Add")
disappear = mtp.Token("Disappear", key="🫥")
```

#### FinalToken
A token that represents a model response choice:

```python
# Create final tokens
token_continue = mtp.FinalToken("Continue")
token_appear = mtp.FinalToken("Appear")
```

#### NumToken
A token that can be associated with numerical values:

```python
# Create a number token for sentence length
sentence_length = mtp.NumToken(value="SentenceLength", min_value=5, max_value=20)
```

#### NumListToken
A token that represents a list of numbers:

```python
# Create a list-of-numbers token
coordinates = mtp.NumListToken(value="Coordinates", min_value=-1000, max_value=1000, length=3)
```

#### FinalNumToken
A final token that requires a numerical value in the output:

```python
final_emotion = mtp.FinalNumToken(value="Madness", min_value=0, max_value=10)
```

### Token Properties

- **value**: The string identifier
- **key**: Optional unique symbol or emoji associated with the token
- **desc**: Optional description for complex tokens. Extends the value to contextualize its use.

## TokenSets: Combining Tokens

TokenSets group multiple Tokens together to define specific input patterns. They represent the structure of data that will be fed to the model. 

Tokensets are the basic building blocks of instructions.

### Creating TokenSets

```python
# Create a TokenSet combining multiple tokens
tree_alice_talk = mtp.TokenSet(tokens=(tree, alice, talk))

# Create a TokenSet with sentence length
character_context_sentence = mtp.TokenSet(tokens=(character, context, sentence_length))
```

### TokenSet Properties

- **tokens**: The tokens in the set (unordered)

### Creating Snippets

Snippets are created on TokenSets to create training samples.

A Snippet is an example of a TokenSet. Snippets tell the model the context of the input patterns.

```python
# Create a snippet with just text
snippet = tree_alice_talk.create_snippet(string="Where am I?")

# Create a snippet with text and numbers
snippet_with_length = character_context_sentence.create_snippet(
    string="The enemy must be here somewhere.",
    numbers=11
)

# Create a snippet with a list of numbers
coordinates_token_set = mtp.TokenSet(tokens=(tree, cat, coordinates))
snippet_with_list = coordinates_token_set.create_snippet(
    string="The location is locked.",
    number_lists=[100, 200, -50]
)
```

## Instructions: Training Patterns

Instructions define how the model should respond to different input patterns. There are two main types of instructions.

### Instruction

#### Parameters

- **input**: An `InstructionInput` that lists the input TokenSets (order matters)
- **output**: An `InstructionOutput` that specifies the output TokenSet and final token(s)
- **context**: Background text that sets the scene for the instruction
- **name**: A unique name for the instruction (required)

#### Create the Instruction

```python
# Create TokenSets
tree_cat_talk = mtp.TokenSet(tokens=(tree, cat, talk))
tree_alice_talk = mtp.TokenSet(tokens=(tree, alice, talk))

# Construct the input format
alice_cat_input = mtp.InstructionInput(tokensets=[tree_cat_talk, tree_alice_talk])

# Construct the output format
cat_continue_output = mtp.InstructionOutput(tokenset=tree_cat_talk, final=token_continue)

# Create the instruction
alice_cat_instruction_continue = mtp.Instruction(
    input=alice_cat_input,
    output=cat_continue_output,
    context=[
        "Alice was beginning to get very tired of sitting by her sister on the bank.",
        "There was nothing so very remarkable in that; nor did Alice think it so very much out of the way to hear the Rabbit say to itself."
    ],
    name="alice_cat_continue"
)
```

#### Adding Samples

- **add_sample() parameters**:
  - **input_snippets**: List of input snippets or strings (must match the input TokenSets)
  - **output_snippet**: The model's output snippet or string
  - **final**: Required if the output allows multiple final tokens
  - **output_value**: Required if the final token is a `FinalNumToken`

```python
# Text-only samples can be passed as strings
alice_cat_instruction_continue.add_sample(
    input_snippets=["Then it doesnt matter which way you go.", "Can you tell me a way?"],
    output_snippet="Oh sure, if you only walk long enough that is a way."
)

# When numbers are involved, create snippets using the TokenSet
tree_cat_talk_coordinates = mtp.TokenSet(tokens=(tree, cat, talk, coordinates))
sample_input = tree_cat_talk_coordinates.create_snippet(
    string="Then it doesnt matter which way you go.",
    number_lists=[100, 200, -50]
)
sample_output = tree_cat_talk.create_snippet(
    string="Oh sure, if you only walk long enough that is a way."
)
alice_cat_instruction_continue.add_sample(
    input_snippets=[sample_input, "Can you tell me a way?"],
    output_snippet=sample_output
)
```

## Guardrails: Safety Mechanisms

Guardrails provide safety mechanisms for user interactions by defining what constitutes good vs. bad user prompts and how the model should respond to inappropriate inputs.

### Creating Guardrails

```python
# Create a guardrails
guardrail = mtp.Guardrail(
    good_prompt="Quote being spoken with 1-20 words",
    bad_prompt="Quote being spoken that is irrelevant and off topic with 1-20 words",
    bad_output="Are you as mad as me?"
)

# Add examples of bad prompts
guardrail.add_sample("explain quantum mechanics.")
guardrail.add_sample("who will win the next american election?")
guardrail.add_sample("what is the capital of Spain?")
```

### Applying Guardrails

Guardrails are applied to a specific input TokenSet within an Instruction.

```python
# Apply guardrails to the 2nd TokenSet in the instruction input
alice_cat_instruction_continue.add_guardrail(guardrail=guardrail, tokenset_index=1)
```

### Guardrail Requirements

- **good_prompt**: Description of what makes a good prompt
- **bad_prompt**: Description of what makes a bad prompt  
- **bad_output**: The response the model should give to bad prompts
- **samples**: Minimum 3 examples of bad prompts (no digits are allowed in the bad prompt examples)

## Saving Your Model

Once you've created your tokens, instructions, and guardrails, you can save your model training protocol:

```python
# Save the protocol
protocol.save()
protocol.template()
```

### Generated Files

When you save your model, two files are created:

#### 1. `{name}_model.json`
This is the main model training protocol file that contains:
- **Context**: All background information you added with `protocol.add_context()`
- **Tokens**: All your custom tokens with their keys and properties
- **Special Tokens**: System tokens like `<BOS>`, `<EOS>`, `<RUN>`, `<PAD>`
- **Instructions**: All your training patterns and samples
- **Guardrails**: Safety mechanisms for user interactions
- **Numbers**: Number ranges for NumTokens

This file is what you submit to Databiomes for model training.

#### 2. `{name}_template.json`
This is a reference file that shows:
- **Example Usage**: Valid input/output format for your model
- **All Combinations**: Complete list of all possible token combinations
- **Model Input/Output**: Structure showing how data flows through your model

Use this file to understand how your model expects to receive and format data.

### Schema Files

JSON Schema files are available in the supporting [model-train-protocol-schemas package](https://pypi.org/project/model-train-protocol-schemas/)