View the full package documentation at: https://modeltrainprotocol.readthedocs.io/en/latest/

# Model Training Protocol (MTP)

MTP is an open-source protocol for training custom Language Models on Databiomes. MTP contains all the data that a model is trained on.

## Getting Started

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

# Creating a Model Training Protocol

The first step in creating a model training protocol is to initialize the Protocol:

```python
import model_train_protocol as mtp

# Initialize the protocol
protocol = mtp.Protocol(name="my_model", instruction_context_snippets=3)
```

The parameter `instruction_context_snippets` is the number of lines in each instruction sample. This is required and must be at least 3.

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

#### UserToken
A specialized token that represents user input. These tokens are used when the model needs to respond to user prompts:

```python
# Create a user token
alice = mtp.UserToken("Alice")
```

#### NumToken
A token that can be associated with numerical values:

```python
# Create a number token for sentence length
sentence_length = mtp.NumToken(value="SentenceLength", min_value=5, max_value=20)
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

A Snippet is a example of a TokenSet. Snippets tell the model the context of the input patters.

```python
# Create a snippet with just text
snippet = tree_alice_talk.create_snippet(string="Where am I?")

# Create a snippet with text and sentence length
snippet_with_length = character_context_sentence.create_snippet(string="The enemy must be here somewhere.", numbers=[11])
```

## Instructions: Training Patterns

Instructions define how the model should respond to different input patterns. There are two main types of instructions.

### Instruction

#### Parameters

- **context**: Sequence of TokenSets that provide background information
- **response**: The TokenSet that defines the model's response pattern (cannot contain UserTokens)
- **final**: A Token that represents the final action or result

#### Create the Instruction

For scenarios where the model responds without user input:

```python
# Create TokenSets
cat_pondering = mtp.TokenSet(tokens=(tree, cat, ponder))
cat_grinning = mtp.TokenSet(tokens=(tree, cat, grin))

# Create a simple instruction for the Cat's internal thoughts
instruction = mtp.Instruction(
    context=(cat_pondering,),
    response=cat_grinning,
    final=disappear
)
```

#### Adding Samples

- **add_sample() parameters**:
  - **context_snippets**: List of context snippets that will be added to the Instruction
  - **output_snippet**: The model's output snippet
  - **value**: Optional numerical value (required if final Token is a NumToken)

```python
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
```

### UnsetInstruction

#### Parameters

- **context**: Sequence of TokenSets that provide background information
- **user**: A TokenSet that must include at least one UserToken
- **final**: A Token that represents the final action or result

#### Create the UnsetInstruction

For scenarios where the model responds to user prompts:

```python
# Create TokenSets for Alice and Cat interaction
alice_talk = mtp.TokenSet(tokens=(tree, alice, talk))
cat_talk = mtp.TokenSet(tokens=(tree, cat, talk))

# Create a user instruction for Alice asking the Cat questions
user_instruction = mtp.UnsetInstruction(
    context=(alice_talk,),
    user=alice_talk,  # Must contain at least one UserToken
    final=disappear
)
```

#### Adding Samples

- **add_sample() parameters**:
  - **context_snippets**: List of context snippets that will be added to the Instruction
  - **prompt**: The prompt provided by the user
  - **output_snippet**: The model's output snippet
  - **value**: Optional numerical value (required if final Token is a NumToken)

```python
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

Guardrails are applied to TokenSets that contain user tokens. 

A TokenSet can have at most one guardrail, but guardrails can be reused.

```python
# Apply guardrails to a user TokenSet
tree_alice_talk.set_guardrail(guardrail)
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

### File Structure Example

```
my_model_model.json     # Main training protocol
my_model_template.json  # Reference and examples
```

The template file helps you understand the expected format when using your trained model, while the model file contains all the training data needed to create your specialized language model.
