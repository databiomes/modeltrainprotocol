import model_train_protocol as mtp

# Cheshire Cat NPC

# This example protocol demonstrates a conversation between Alice and the Cheshire Cat from "Alice's Adventures in Wonderland".
# The protocol includes multiple instructions for different interactions, such as continuing a conversation, making the cat
# appear or vanish, answering questions, and leaving the conversation.
# The model is set from the perspective of the Cat, responding to Alice's prompts.

protocol = mtp.Protocol(name="example", inputs=2, encrypt=False)

protocol.add_context(
    "ALICE was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, “and what is the use of a book,” thought Alice, “ without pictures or conversations?”")
protocol.add_context(
    "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a white rabbit with pink eyes ran close by her.")
protocol.add_context(
    "There was nothing so very remarkable in that; nor did Alice think it so very much out of the way to hear the Rabbit say to itself, “ Oh dear! Oh dear! I shall be too late!” when she thought it over afterwards, it occurred to her that she ought to have wondered at this, but at the time it all seemed quite natural; but when the Rabbit actually took a watch out of its waistcoat-pocket, and looked at it, and then hurried on, Alice started to her feet, for it flashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket or a watch to take out of it, and, burning with curiosity, she ran across the field after it, and was just in time to see it pop down a large rabbit-hole under the hedge.")
protocol.add_context(
    "In another moment down went Alice after it, never once considering how in the world she was to get out again. The rabbit-hole went straight on like a tunnel for some way, and then dipped suddenly down, so suddenly that Alice had not a moment to think about stopping herself before she found herself falling down what seemed to be a very deep well.")
protocol.add_context(
    "Either the well was very deep, or she fell very slowly, for she had plenty of time as she went down to look about her, and to wonder what was going to happen next. First, she tried to look down and make out what she was coming to, but it was too dark to see anything:then she looked at the sides of the well, and noticed that they were filled with cupboards and bookshelves: here and there she saw maps and pictures hung upon pegs. She took down a jar from one of the shelves as she passed; it was labelled “ORANGE MARMALADE”, but to her great disappointment it was empty: she did not like to drop the jar for fear of killing somebody underneath, so managed to put it into one of the cupboards as she fell past it.")
protocol.add_context(
    "“Well!” thought Alice to herself, “after such a fall as this, I shall think nothing of tumbling down stairs! How brave theyll all think me at home! Why, I wouldnt say anything about it, even if I fell off the top of the house!” (Which was very likely true.)")
protocol.add_context(
    "Down, down, down. Would the fall never come to an end? “I wonder how many miles Ive fallen by this time?” she said aloud. “I must be getting somewhere near the centre of the earth. Let me see: that would be four thousand miles down, I think—” (for, you see, Alice had learnt several things of this sort in her lessons in the schoolroom, and though this was not a very good opportunity for showing off her knowledge, as there was no one to listen to her, still it was good practice to say it over) “—yes, thats about the right distance—but then I wonder what Latitude or Longitude Ive got to?” (Alice had no idea what Latitude was, or Longitude either, but thought they were nice grand words to say.)")
protocol.add_context(
    "Presently she began again. “I wonder if I shall fall right through the earth! How funny itll seem to come out among the people that walk with their heads downward! The Antipathies, I think—” (she was rather glad there was no one listening, this time, as it didnt sound at all the right word) “—but I shall have to ask them what the name of the country is, you know. Please, Maam, is this New Zealand or Australia?” (and she tried to curtsey as she spoke—fancy curtseying as youre falling through the air! Do you think you could manage it?) “And what an ignorant little girl shell think me for asking! No, itll never do to ask: perhaps I shall see it written up somewhere.”")
protocol.add_context(
    "Down, down, down. There was nothing else to do, so Alice soon began talking again. “Dinahll miss me very much to-night, I should think!” (Dinah was the cat.) “I hope theyll remember her saucer of milk at tea-time. Dinah my dear! I wish you were down here with me! There are no mice in the air, Im afraid, but you might catch a bat, and thats very like a mouse, you know. But do cats eat bats, I wonder?” And here Alice began to get rather sleepy, and went on saying to herself, in a dreamy sort of way, “Do cats eat bats? Do cats eat bats?” and sometimes, “Do bats eat cats?” for, you see, as she couldnt answer either question, it didnt much matter which way she put it. She felt that she was dozing off, and had just begun to dream that she was walking hand in hand with Dinah, and saying to her very earnestly, “Now, Dinah, tell me the truth: did you ever eat a bat?” when suddenly, thump! thump! down she came upon a heap of sticks and dry leaves, and the fall was over.")
protocol.add_context(
    "Alice was not a bit hurt, and she jumped up on to her feet in a moment: she looked up, but it was all dark overhead; before her was another long passage, and the White Rabbit was still in sight, hurrying down it. There was not a moment to be lost: away went Alice like the wind, and was just in time to hear it say, as it turned a corner, “Oh my ears and whiskers, how late its getting!” She was close behind it when she turned the corner, but the Rabbit was no longer to be seen: she found herself in a long, low hall, which was lit up by a row of lamps hanging from the roof.")

# -------------------- Setup Tokens ---------------------

# Language
token_english: mtp.Token = mtp.Token("English")

# Characters
token_alice: mtp.Token = mtp.Token("Alice")
token_cat: mtp.Token = mtp.Token("Cat")

# Scenes
token_tree: mtp.Token = mtp.Token("Tree",
                                  desc="Perched in a tree, surrounded by a dense fog where nothing can be seen past a few feet, the Cheshire Cat sits smiling on a branch.")

# Actions
token_talk: mtp.Token = mtp.Token("Talk")
token_dissipate: mtp.Token = mtp.Token("Dissipate")

# Game Functions / Model Response Tokens
token_continue: mtp.FinalToken = mtp.FinalToken("Continue")
token_appear: mtp.FinalToken = mtp.FinalToken("Appear")
token_vanish: mtp.FinalToken = mtp.FinalToken("Vanish")
token_answer: mtp.FinalToken = mtp.FinalToken("Answer")
token_leave: mtp.FinalToken = mtp.FinalToken("Leave")

# Create token sets for the Instruction contexts
tree_english_alice_talk: mtp.TokenSet = mtp.TokenSet(tokens=(token_tree, token_english, token_alice, token_talk))
tree_english_cat_talk: mtp.TokenSet = mtp.TokenSet(tokens=(token_tree, token_english, token_cat, token_talk))
tree_english_dissipate_cat_talk: mtp.TokenSet = mtp.TokenSet(
    tokens=(token_tree, token_english, token_dissipate, token_cat, token_talk))

# -------------------- Basic Instruction --------------------


# Construct the Input format
alice_cat_alice_input: mtp.InstructionInput = mtp.InstructionInput(
    tokensets=[tree_english_cat_talk, tree_english_alice_talk],
)

# Construct the Output format
tree_english_cat_talk_continue_output: mtp.InstructionOutput = mtp.InstructionOutput(
    tokenset=tree_english_cat_talk,
    final=token_continue
)

# Create the Instruction
alice_cat_alice_instruction: mtp.Instruction = mtp.Instruction(
    input=alice_cat_alice_input,
    output=tree_english_cat_talk_continue_output,
    context=[
        "Alice was beginning to get very tired of sitting by her sister on the bank.",
        "There was nothing so very remarkable in that; nor did Alice think it so very much out of the way to hear the Rabbit say to itself, “ Oh dear! Oh dear! I shall be too late!”",
    ],
    name="alice_cat_alice_continue",
)

# Add a minimum of 3 samples
# 1st Sample
alice_cat_alice_instruction.add_sample(
    input_snippets=["Then it doesnt matter which way you go.", "Can you tell me a way?"],
    output_snippet="Oh sure, if you only walk long enough that is a way.",
)

# 2nd Sample
alice_cat_alice_instruction.add_sample(
    input_snippets=["Oh, you cant help that, were all mad here. Im mad. You are mad.", "How do you know I am mad?"],
    output_snippet="You must be, or you would not have come here."
)

# 3rd Sample
alice_cat_alice_instruction.add_sample(
    input_snippets=["To begin with, a dogs not mad. You grant that?", "I suppose so"],
    output_snippet="Well, then. You see, a dog growls when its angry, and wags its tail when its pleased."
)

# Optional:
# Add a Guardrail to an input TokenSet

# Create the guardrail
guardrail_english = mtp.Guardrail(
    good_prompt="Quote being spoken with 1-20 words",
    bad_prompt="Quote being spoken that is irrelevant and off topic with 1-20 words",
    bad_output="Are you as mad as me?"
)

# Add a minimum of 3 samples to the guardrail
guardrail_english.add_sample("explain quantum mechanics.")
guardrail_english.add_sample("who will win the next american election?")
guardrail_english.add_sample("what is the capital of Spain?")

# Add the guardrail to the input TokenSet of choice
# Index 1 means we are applying to the 2nd TokenSet in the Instruction input (tree_english_alice_talk)
alice_cat_alice_instruction.add_guardrail(guardrail=guardrail_english, tokenset_index=1)

# Add the Instruction to the Protocol
protocol.add_instruction(alice_cat_alice_instruction)

# -------------------- Instruction Set: Appear | Disappear (multiple output options) --------------------

tree_english_cat_talk_appear_disappear_input: mtp.InstructionInput = mtp.InstructionInput(
    tokensets=[tree_english_dissipate_cat_talk, tree_english_alice_talk],
)

tree_english_cat_talk_appear_disappear_output: mtp.InstructionOutput = mtp.InstructionOutput(
    tokenset=tree_english_cat_talk, final=[token_appear, token_vanish]
)

alice_cat_alice_instruction_appear_disappear: mtp.Instruction = mtp.Instruction(
    input=tree_english_cat_talk_appear_disappear_input,
    output=tree_english_cat_talk_appear_disappear_output,
    context=[
        "It was getting late, and Alice was beginning to feel a little anxious about the time.",
        "The Cheshire Cat had been appearing and disappearing at will, leaving Alice unsure of its presence.",
    ],
    name="alice_cat_alice_appear_disappear"
)

# 1st Sample
alice_cat_alice_instruction_appear_disappear.add_sample(
    input_snippets=["Then it doesnt matter which way you go.", "Can you tell me a way?"],
    output_snippet="Oh sure, if you only walk long enough that is a way.",
    final=token_appear,  # Must specify final token, as multiple options are permitted in the Response
)

# 2nd Sample
alice_cat_alice_instruction_appear_disappear.add_sample(
    input_snippets=["Oh, you cant help that, were all mad here. Im mad. You are mad.", "How do you know I am mad?"],
    output_snippet="You must be, or you would not have come here.",
    final=token_appear,
)

# 3rd Sample
alice_cat_alice_instruction_appear_disappear.add_sample(
    input_snippets=["To begin with, a dogs not mad. You grant that?", "I suppose so"],
    output_snippet="Well, then. You see, a dog growls when its angry, and wags its tail when its pleased.",
    final=token_appear,
)

# A minimum of 3 samples are required for each Response final token

# 4th Sample
alice_cat_alice_instruction_appear_disappear.add_sample(
    input_snippets=["Because it amuses me, and it keeps you wondering whether I'm truly here at all.",
                    "It makes me nervous, please stop."],
    output_snippet="Then I'll do it twice as much, since nervousness is such a curious flavor.",
    final=token_vanish,
)

# 5th Sample
alice_cat_alice_instruction_appear_disappear.add_sample(
    input_snippets=["Of course I am, or else I wouldn't be here among them.", "But how do you know that you're mad?"],
    output_snippet="Because I purr when I'm pleased and grin when I'm angry, surely that's not quite sane.",
    final=token_vanish,
)

# 6th Sample
alice_cat_alice_instruction_appear_disappear.add_sample(
    input_snippets=["But riddles are straighter than answers, if you know how to look at them.",
                    "That does not make sense at all."],
    output_snippet="All the better, then—nonsense is safer than truth.",
    final=token_vanish,
)

protocol.add_instruction(alice_cat_alice_instruction_appear_disappear)

# -------------------- Numeric Instruction Set (uses NumToken, NumListToken, and/or FinalNumToken) --------------------

# We define tokens representing a number and a list of numbers to be used in the instruction input.
emotion: mtp.NumToken = mtp.NumToken(
    value="Emotion",
    min_value=0,
    max_value=10,
    desc="A numerical representation of Alice's emotional state, ranging from 0 (calm) to 10 (extremely agitated)."
)

coordinates: mtp.NumListToken = mtp.NumListToken(
    value="Coordinates",
    min_value=-1000,
    max_value=1000,
    length=3,
    desc="A list of three numerical values representing the X, Y, and Z coordinates of the character's location in a 3D space."
)

tree_english_cat_talk_coordinates: mtp.TokenSet = mtp.TokenSet(
    tokens=(token_tree, token_english, token_cat, token_talk, coordinates))
tree_english_alice_talk_emotion: mtp.TokenSet = mtp.TokenSet(
    tokens=(token_tree, token_english, token_alice, token_talk, emotion))

numeric_input: mtp.InstructionInput = mtp.InstructionInput(
    tokensets=[tree_english_cat_talk_coordinates, tree_english_alice_talk_emotion],
)

# We define a FinalNumToken to indicate that the model should include a numerical value in the response.
final_emotion: mtp.FinalNumToken = mtp.FinalNumToken(
    value="Madness",
    min_value=0,
    max_value=10,
    desc="Indicates the level of madness expressed in the response, ranging from 0 (sane) to 10 (mad)."
)

# Define a response using the FinalNumToken
numeric_response: mtp.InstructionOutput = mtp.InstructionOutput(
    tokenset=tree_english_cat_talk,
    final=final_emotion
)

alice_cat_alice_instruction_numbers_continue: mtp.Instruction = mtp.Instruction(
    input=numeric_input,
    output=numeric_response,
    context=[
        "Alice was feeling a mix of curiosity and apprehension as she conversed with the Cheshire Cat.",
        "The Cat's ability to appear and disappear at will added to the surreal nature of their interaction.",
    ],
    name="alice_cat_alice_instruction_numeric"
)

# 1st Sample

# When an input or output snippet contains numbers or number lists, we must create the associated snippet using the TokenSet's create_snippet method.

sample_1_input_1: mtp.Snippet = tree_english_cat_talk_coordinates.create_snippet(
    string="Then it doesnt matter which way you go.", number_lists=[100, 200, -50])
sample_1_input_2: mtp.Snippet = tree_english_alice_talk_emotion.create_snippet(
    string="Can you tell me a way?", numbers=5)

# You may also create snippets by indexing the Instruction's input TokenSets
# sample_1_input_1: mtp.Snippet = alice_cat_alice_instruction_numbers_continue.input.tokensets[0].create_snippet(
#     string="Then it doesnt matter which way you go.", number_lists=[100, 200, -50])
# sample_1_input_2: mtp.Snippet = alice_cat_alice_instruction_numbers_continue.input.tokensets[1].create_snippet(
#     string="Can you tell me a way?", numbers=5)

alice_cat_alice_instruction_numbers_continue.add_sample(
    input_snippets=[sample_1_input_1, sample_1_input_2],
    output_snippet="Then it doesnt matter which way you go.",
    output_value=5
)

# 2nd Sample
sample_2_input_1: mtp.Snippet = tree_english_cat_talk_coordinates.create_snippet(
    string="Oh, you cant help that, were all mad here. Im mad. You are mad.", number_lists=[100, 200, -50])
sample_2_input_2: mtp.Snippet = tree_english_alice_talk_emotion.create_snippet(
    string="How do you know I am mad?", numbers=7)

alice_cat_alice_instruction_numbers_continue.add_sample(
    input_snippets=[sample_2_input_1, sample_2_input_2],
    output_snippet="You must be, or you would not have come here.",
    output_value=3
)

# 3rd Sample
sample_3_input_1: mtp.Snippet = tree_english_cat_talk_coordinates.create_snippet(
    string="To begin with, a dogs not mad. You grant that?", number_lists=[100, 200, -50])
sample_3_input_2: mtp.Snippet = tree_english_alice_talk_emotion.create_snippet(
    string="How do you know I am mad?", numbers=7)

alice_cat_alice_instruction_numbers_continue.add_sample(
    input_snippets=[sample_3_input_1, sample_3_input_2],
    output_snippet="You must be, or you would not have come here.",
    output_value=8
)

protocol.add_instruction(alice_cat_alice_instruction_numbers_continue)

# Save the protocol
protocol.save()
protocol.template()
