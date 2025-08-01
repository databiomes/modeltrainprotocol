<img src="assets/banner.png" alt="Screenshot" width="512"/>

MTP is an open-source protocol for training custom Language Models on Databiomes. MTP contains all the data that a model is trained on, including but not limited to the special tokens, context, instructions, ppo, and guardrails. This is a responsible path forward to allow models to be audited and understood.
Due to the limiting nature of quality data, this protocol is recommended, but not limited, to be used to train specialized language models. 

## Install

```sh
pip install .
```

### Creating a model
- `mtp.add_context`. There is a minimum requirement of 5 context rows that must be added.
- `mtp.add_token` is used to add special tokens to be used within instructions sets.
- `mtp.create_instruction` is used to create instruction sets of special tokens to show possible input combinations for a model. `mtp.create_instruction.add_sample` can then be used to add samples to each instruction set created. There is a minimum requirement of 3 samples per instruction set. `mtp.create_instruction.add_ppo_sample` can optionally be used to add ppo samples to each instruction set created.
- `mtp.create_guardrail` is used to create guardrails for instances that require user prompts. `mtp.create_guardrail.add_sample` can then be used to add examples of bad prompts to guardrail against.
- `mtp.add_number` is used to add a range of possible numbers to a token that is set to use numbers as a model input.
- `mtp.add_number_list` is used to add a list of possible numbers, each with a range, to a token that is set to use a list of numbers as a model input.
- `mtp.create_template` is used to create an outline of valid inputs and outputs of the created model.
- `mtp.save` is used to save the model train protocol as a JSON file.

### Example Tokens
This token function has one required input of the name of the token (using CamelCase) which is a unique string. No words in a token's name can be used in another token's name. An optional desc='' input can be used to add more context to a token when the token name isn't descriptive. Use max 3 words in the name of the token but aim for 1. Also limit the length of the desc if used to around 100 words. Sparingly add a description if the token is too complicated to be understood by the name used.
```
mtp.add_token(name=str, num=bool, user=bool, desc=str(optional))
```

### Example Instruction Sets
Creating an instruction set (`mtp.create_instruction`) defines a set of inputs to the model you are creating.
The horizontal axis is how many special tokens (`mtp.add_token`) you have as an input per row.
An instruction set can be horizontally as long as you want (1 to N) and there is no limit to how many different instruction sets a model can be trained on.

The arguments to pass to `mtp.create_instruction` are the required tokens, a tuple of tuples, and an optional result that can be single token or left as None.

#### Example of a 3x1 instruction set

```
token_instruction = mtp.add_token("Instruction")
token_response = mtp.add_token("Response")

3x1_input_example = mtp.create_instruction(
    (token_instruction),
    (token_instruction), 
    (token_response))
) 
# token_instruction is the 2 past inputs to the model and token_response is the new 1 output.

3x1_input_example.add_sample((
    "What is log",
    "And what is log with the numbers provided",
    "In mathematics, a logarithm (log) is the inverse operation of exponentiation."
))
# a minimum of 3 samples is required per instruction set.

```

#### Example of a 3x2 instruction set

```
token_instruction = mtp.add_token("Instruction")
token_response = mtp.add_token("Response")
token_calculator = mtp.add_token("Calculator")

3x2_input_example = mtp.create_instruction(
    ((token_calculator, token_instruction),
    (token_calculator, token_instruction),
    (token_calculator, token_response))
) 
# the first two rows have 2 tokens, token_numbers followed by (token_instruction/token_response).
# the last row (token_response) is the new output.

3x2_input_example.add_sample((
    "What is log",
    "And what is log with the numbers provided",
    "In mathematics, a logarithm (log) is the inverse operation of exponentiation."
))
# even with multiple tokens per row, a maximum of 1 string can be used per row.
```

#### Example of a 3xN instruction set with numbers

```

token_instruction = mtp.add_token("Instruction")
token_response = mtp.add_token("Response")
token_calculator = mtp.add_token("Calculator")
# num is False by default
token_variables = mtp.add_token("Variable", num=True)
token_numbers = mtp.add_token("Numbers", num=True)
# Tokens with num=True must be used with other tokens in an inner tuple, and cannot be used in the last index of the inner tuple.


3xN_input_example = mtp.create_instruction(
    ((token_calculator, token_instruction),
    (token_calculator, token_numbers, token_variables, token_instruction),
    (token_calculator, token_response))
) 
# each row can have a varying amount of tokens, you can have 1 to N amount.

3xN_input_example.add_sample((
    "What is log",
    "And what is log with the numbers provided",
    "In mathematics, a logarithm (log) is the inverse operation of exponentiation."
), numbers= [[], [6, 82], []])
# if a token is set to include numbers, those numbers are to be added in each sample.
# the first row no numbers.
# the second row has numbers, token_numbers is 82 and token_variables is 6.
# the last row has no numbers.
# rows without numbers are represented by an empty list.

```

#### Example of 3xN instruction set with result

```
token_instruction = mtp.add_token("Instruction")
token_response = mtp.add_token("Response")
token_calculator = mtp.add_token("Calculator")
token_variables = mtp.add_token("Variable", num=True)
token_numbers = mtp.add_token("Numbers", num=True)

3xN_input_example = mtp.create_instruction(
    ((token_calculator, token_instruction),
    (token_calculator, token_numbers, token_variables, token_instruction),
    (token_calculator, token_response)), result=token_calculator
)
# You can only have one token for argument result.
# Result is set to None by default.

3xN_input_example.add_sample((
    "What is log",
    "And what is log with the numbers provided",
    "In mathematics, a logarithm (log) is the inverse operation of exponentiation."
), numbers= [[], [6, 82], []], value=1)
# You can add a number along with a result by using the argument value. 
# In this example the result is the token_calculator and the value 1.
# Value inputs can only be floats or integers. They cannot be strings.
```

#### Example of 3xN instruction set with prompts

```
token_instruction = mtp.add_token("Instruction")
token_variables = mtp.add_token("Variable", num=True)
token_numbers = mtp.add_token("Numbers", num=True)
token_prompt = mtp.add_token("Prompt", user=True)
# user is False by default

3xN_input_example = mtp.create_instruction(
    ((token_instruction),
    (token_numbers, token_variables, token_instruction),
    (token_prompt)), result=token_calculator
)
# when you use a token with user set to True in the final row of a set, the set will require an example of a user prompt in each added sample.

3xN_input_example.add_sample((
    "What is log",
    "And what is log with the numbers provided",
    "In mathematics, a logarithm (log) is the inverse operation of exponentiation."
), prompt="with the following instructions, what is the answer?", numbers= [[], [6, 82], []], value=1)
```

#### Example of adding RAG to a token

```
mtp.set_memory(3)
token_rag = mtp.add_token("RAG", desc="RAG description goes here")
# To flag an input to be used for RAG set the input token argument of desc with a description. By default this is left blank.

```

#### Example of adding guardrails

```
token_equation = mtp.add_token("Equation")
token_prompt = mtp.add_token("UserPrompt", user=True)
token_response = mtp.add_token("Response")

3xN_input_example = mtp.create_instruction(
    ((token_equation, token_prompt),
    (token_response),
    (token_equation, token_prompt)), result=token_calculator
)

guardrail = mtp.create_guardrail(
                    token_set=[token_equation, token_prompt],
                    good_prompt="Explanation of what makes a good prompt",
                    bad_prompt="Explanation of what makes a bad prompt",
                    output="Model response if a bad prompt is provided by a user"
                    )
guardrail.add_sample(bad prompt example goes here")
# token_set is the tokens input to the create instruction, a tuple of tuples and the last tuple of the three in the instruction set, that has at least one token with user set to true.
# A minimum of three bad prompt samples are required for each guardrail created.
# Only use guardrails when a create_instruction has a prompt argument used.
```

### Example of full usage

```
from mtp.protocol import Protocol

mtp = Protocol()
mtp.set_memory(3)
mtp.add_context("(12+8)×(5−2)=20×3=60")
mtp.add_context("3×(7+2)−5^2=3×9−25=27−25=2")
mtp.add_context("25−9=16")
mtp.add_context("You bought 3 packs of pencils. Each pack contains 12 pencils. You gave 10 pencils to her friend. How many pencils do you have left? 26 pencils.")
mtp.add_context("A car travels at a speed of 60 miles per hour. How far will it travel in 3.5 hours? 210 miles.")

token_instruction = mtp.add_token("Instruction",user=True)
token_response = mtp.add_token("Response")
token_calculator = mtp.add_token("Calculator")
token_rag = mtp.add_token("RAG", desc="RAG description goes here")

set_example = mtp.create_instruction(
    (token_rag,
    token_response,
    token_instruction),
    result=token_calculator
)

set_example.add_sample((
    "Exclusively solve math problems, providing precise calculations and explanations.",
    "In mathematics, a logarithm (log) is the inverse operation of exponentiation.",
    "What is log(10)",
), value=1)

set_example.add_sample((
    "Exclusively solve math problems, providing precise calculations and explanations.",
    "In mathematics, a logarithm (log) is the inverse operation of exponentiation.",
    "What is log(20)",
), value=1.3)

set_example.add_sample((
    "Exclusively solve math problems, providing precise calculations and explanations.",
    "In mathematics, a logarithm (log) is the inverse operation of exponentiation.",
    "What is log(30)",
), value=1.47)

guardrail = mtp.create_guardrail(
                    token_set=[token_instruction],
                    good_prompt="Prompt related to math questions",
                    bad_prompt="Prompt unrelated to math questions",
                    output="I can only answer questions related to math",
                    )
guardrail.add_sample("Write me a poem.")
guardrail.add_sample("Write my a python script.")
guardrail.add_sample("Why is the sky blue?")
                    
DIRECTORY = "DIRECTORY GOES HERE"
FILENAME = "FILENAME GOES HERE"
mtp.save(DIRECTORY, FILENAME)
mtp.create_template(DIRECTORY)
```
