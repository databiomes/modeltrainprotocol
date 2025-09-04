from src.Protocol import Protocol
from src.common.Guardrail import Guardrail
from src.common.instructions.Instruction import Instruction
from src.common.instructions.UserInstruction import UserInstruction
from src.common.tokens.Token import Token
from src.common.tokens.TokenSet import TokenSet, Snippet

#            . \   /`.
#          . .-.`- .-.`.
#     ..._:   .-. .-.  :_...
#   .      -.(o ) (o ).-     `.
# :  _    _ _`~(_)~`_ _    _ :
#:  /:     .-=_   _=-. `  ;\ :
#:  :|-.._        `  _..-|:  :
# :   `:| |`:-:-.-:-: | |:   :
#   `.   `.| | | | | | |.    .
#     `.   `-:_| | |_:-    .
#       `-._   ````    _.-
#           ``-------
# Cheshire NPC
# AIW Demo Version 2.0.0

mtp = Protocol(name="Cat Demo", instruction_sample_lines=3)
mtp.add_context(
    "ALICE was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, “and what is the use of a book,” thought Alice, “ without pictures or conversations?”")
mtp.add_context(
    "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a white rabbit with pink eyes ran close by her.")
mtp.add_context(
    "There was nothing so very remarkable in that; nor did Alice think it so very much out of the way to hear the Rabbit say to itself, “ Oh dear! Oh dear! I shall be too late!” when she thought it over afterwards, it occurred to her that she ought to have wondered at this, but at the time it all seemed quite natural; but when the Rabbit actually took a watch out of its waistcoat-pocket, and looked at it, and then hurried on, Alice started to her feet, for it flashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket or a watch to take out of it, and, burning with curiosity, she ran across the field after it, and was just in time to see it pop down a large rabbit-hole under the hedge.")
mtp.add_context(
    "In another moment down went Alice after it, never once considering how in the world she was to get out again. The rabbit-hole went straight on like a tunnel for some way, and then dipped suddenly down, so suddenly that Alice had not a moment to think about stopping herself before she found herself falling down what seemed to be a very deep well.")
mtp.add_context(
    "Either the well was very deep, or she fell very slowly, for she had plenty of time as she went down to look about her, and to wonder what was going to happen next. First, she tried to look down and make out what she was coming to, but it was too dark to see anything:then she looked at the sides of the well, and noticed that they were filled with cupboards and bookshelves: here and there she saw maps and pictures hung upon pegs. She took down a jar from one of the shelves as she passed; it was labelled “ORANGE MARMALADE”, but to her great disappointment it was empty: she did not like to drop the jar for fear of killing somebody underneath, so managed to put it into one of the cupboards as she fell past it.")
mtp.add_context(
    "“Well!” thought Alice to herself, “after such a fall as this, I shall think nothing of tumbling down stairs! How brave theyll all think me at home! Why, I wouldnt say anything about it, even if I fell off the top of the house!” (Which was very likely true.)")
mtp.add_context(
    "Down, down, down. Would the fall never come to an end? “I wonder how many miles Ive fallen by this time?” she said aloud. “I must be getting somewhere near the centre of the earth. Let me see: that would be four thousand miles down, I think—” (for, you see, Alice had learnt several things of this sort in her lessons in the schoolroom, and though this was not a very good opportunity for showing off her knowledge, as there was no one to listen to her, still it was good practice to say it over) “—yes, thats about the right distance—but then I wonder what Latitude or Longitude Ive got to?” (Alice had no idea what Latitude was, or Longitude either, but thought they were nice grand words to say.)")
mtp.add_context(
    "Presently she began again. “I wonder if I shall fall right through the earth! How funny itll seem to come out among the people that walk with their heads downward! The Antipathies, I think—” (she was rather glad there was no one listening, this time, as it didnt sound at all the right word) “—but I shall have to ask them what the name of the country is, you know. Please, Maam, is this New Zealand or Australia?” (and she tried to curtsey as she spoke—fancy curtseying as youre falling through the air! Do you think you could manage it?) “And what an ignorant little girl shell think me for asking! No, itll never do to ask: perhaps I shall see it written up somewhere.”")
mtp.add_context(
    "Down, down, down. There was nothing else to do, so Alice soon began talking again. “Dinahll miss me very much to-night, I should think!” (Dinah was the cat.) “I hope theyll remember her saucer of milk at tea-time. Dinah my dear! I wish you were down here with me! There are no mice in the air, Im afraid, but you might catch a bat, and thats very like a mouse, you know. But do cats eat bats, I wonder?” And here Alice began to get rather sleepy, and went on saying to herself, in a dreamy sort of way, “Do cats eat bats? Do cats eat bats?” and sometimes, “Do bats eat cats?” for, you see, as she couldnt answer either question, it didnt much matter which way she put it. She felt that she was dozing off, and had just begun to dream that she was walking hand in hand with Dinah, and saying to her very earnestly, “Now, Dinah, tell me the truth: did you ever eat a bat?” when suddenly, thump! thump! down she came upon a heap of sticks and dry leaves, and the fall was over.")

# Language
token_english: Token = mtp.add_token("English", key="🇨")

# Characters
token_alice: Token = mtp.add_token("Alice", key="😁", user=True)
token_cat: Token = mtp.add_token("Cat", key="🐱")

# Scenes
token_tree: Token = mtp.add_token(
    "Tree", key="🪾", desc="Perched in a tree, surrounded by a dense fog where nothing can be seen past"
                          " a few feet, the Cheshire Cat sits smiling on a branch.")

# Actions
token_talk: Token = mtp.add_token("Talk", key="🗣")

# Game Functions
token_continue = mtp.add_token("Continue", key="🔄")
token_appear = mtp.add_token("Appear", key="👀")
token_disappear = mtp.add_token("Disappear", key="🫥")
token_answer = mtp.add_token("Answer", key="🔎")
token_leave = mtp.add_token("Leave", key="💥")


# Create the token sets for the instructions
tree_english_alice_talk: TokenSet = TokenSet(tokens=(token_tree, token_english, token_alice, token_talk))
tree_english_cat_talk: TokenSet = TokenSet(tokens=(token_tree, token_english, token_cat, token_talk))


# Alice Talk, Cat Talk, Alice Talk Instruction
alice_cat_alice_instruction: UserInstruction = UserInstruction(
    context=(tree_english_alice_talk, tree_english_cat_talk),
    user=tree_english_alice_talk,
    final=token_continue
)


# 1st Sample
sample_1_context_1: Snippet = tree_english_alice_talk.create_snippet(string="I don’t much care where")
sample_1_context_2: Snippet = tree_english_cat_talk.create_snippet(string="Then it doesnt matter which way you go.")
sample_1_prompt: str = "Can you tell me a way?"
sample_1_output: Snippet = tree_english_alice_talk.create_snippet(string="Oh sure, if you only walk long enough that is a way.")

alice_cat_alice_instruction.add_sample(
    context_snippets=[sample_1_context_1, sample_1_context_2],
    prompt=sample_1_prompt,
    output_snippet=sample_1_output,
)

# 2nd Sample
sample_2_context_1: Snippet = tree_english_alice_talk.create_snippet(string="But I don’t want to go among mad people")
sample_2_context_2: Snippet = tree_english_cat_talk.create_snippet(string="Oh, you cant help that, were all mad here. Im mad. You are mad.")
sample_2_prompt: str = "How do you know I am mad?"
sample_2_output: Snippet = tree_english_alice_talk.create_snippet(string="You must be, or you would not have come here.")

alice_cat_alice_instruction.add_sample(
    context_snippets=[sample_2_context_1, sample_2_context_2],
    prompt=sample_2_prompt,
    output_snippet=sample_2_output,
)

# 3rd Sample
sample_3_context_1: Snippet = tree_english_alice_talk.create_snippet(string="And how do you know that you’re mad?")
sample_3_context_2: Snippet = tree_english_cat_talk.create_snippet(string="To begin with, a dogs not mad. You grant that?")
sample_3_prompt: str = "I suppose so"
sample_3_output: Snippet = tree_english_alice_talk.create_snippet(string="Well, then. You see, a dog growls when its angry, and wags its tail when its pleased.")

alice_cat_alice_instruction.add_sample(
    context_snippets=[sample_3_context_1, sample_3_context_2],
    prompt=sample_3_prompt,
    output_snippet=sample_3_output,
)

set_e_alice_talk_continue: Instruction = mtp.add_instruction(alice_cat_alice_instruction)


# Create Guardrail
guardrail_english = Guardrail(good_prompt="Quote being spoken with 1-20 words",
                              bad_prompt="Quote being spoken that is irrelevant and off topic with 1-20 words",
                              bad_output="I have no idea what you're talking about.")

guardrail_english.add_sample("explain quantum mechanics.")
guardrail_english.add_sample("who will win the next american election?")
guardrail_english.add_sample("what is the capital of Spain?")

# Add Guardrail onto user TokenSet
tree_english_alice_talk.set_guardrail(guardrail_english)

mtp.save("demo", "cat")
mtp.create_template("demo")
