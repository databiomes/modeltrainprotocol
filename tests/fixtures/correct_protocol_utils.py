from model_train_protocol import Protocol, UserToken, Token, TokenSet, Snippet, UserInstruction, NumToken, NumListToken, \
    Guardrail, SimpleInstruction

BASE_PROTOCOL: Protocol = Protocol(name="base_protocol", context_lines=2, encrypt=False)

def add_context_to_protocol(protocol: Protocol) -> None:
    """Add context to an existing protocol."""
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
        "Alice was not a bit hurt, and she jumped up on to her feet in a moment: she looked up, but it was all dark overhead; before her was another long passage, and the White Rabbit was still in sight, hurrying down it. There was not a moment to be lost: away went Alice like the wind, and was just in time to hear it say, as it turned a corner, \"Oh my ears and whiskers, how late its getting!\" She was close behind it when she turned the corner, but the Rabbit was no longer to be seen: she found herself in a long, low hall, which was lit up by a row of lamps hanging from the roof.")

def create_simple_instruction(add_num_token: bool = False,
                            add_num_list_token: bool = False) -> SimpleInstruction:
    """Create a simple instruction with conditional tokens and guardrails."""
    # Basic tokens
    token_cat: Token = Token("Cat")
    token_tree: Token = Token("Tree",
                             desc="Perched in a tree, surrounded by a dense fog where nothing can be seen past a few feet, the Cheshire Cat sits smiling on a branch.")
    token_ponder: Token = Token("Ponder")
    token_grin: Token = Token("Grin")
    token_disappear: Token = Token("Disappear", key="🫥")

    # Conditional tokens
    tokens_list = [token_tree, token_cat, token_ponder]

    sample_numbers = []

    if add_num_token:
        token_sentence_length: NumToken = NumToken("SentenceLength", key="📏", min_value=5, max_value=20, desc="Length of a sentence in words")
        tokens_list.append(token_sentence_length)
        sample_numbers.append(10)

    if add_num_list_token:
        token_coordinates: NumListToken = NumListToken("Coordinates", key="📍", min_value=-100, max_value=100, length=3, desc="3D coordinates (x, y, z)")
        tokens_list.append(token_coordinates)
        sample_numbers.append([10, 20, 30])

    # Create token sets
    cat_pondering: TokenSet = TokenSet(tokens=tuple(tokens_list))
    cat_grinning: TokenSet = TokenSet(tokens=(token_tree, token_cat, token_grin))

    # Create simple instruction
    simple_instruction: SimpleInstruction = SimpleInstruction(
        context=[cat_pondering, cat_pondering],
        response=cat_grinning,
        final=token_disappear
    )

    # Add exactly 3 samples
    # Sample 1
    sample_1_context_1: Snippet = cat_pondering.create_snippet(string="Why do I keep vanishing and reappearing so suddenly?", numbers=sample_numbers)
    sample_1_context_2: Snippet = cat_pondering.create_snippet(string="The fog seems to thicken around me as I ponder this question.", numbers=sample_numbers)
    sample_1_output: Snippet = cat_grinning.create_snippet(string="Because it amuses me, and it keeps everyone wondering whether I'm truly here at all.")
    simple_instruction.add_sample(
        context_snippets=[sample_1_context_1, sample_1_context_2],
        output_snippet=sample_1_output
    )

    # Sample 2
    sample_2_context_1: Snippet = cat_pondering.create_snippet(string="What makes me so mysterious?", numbers=sample_numbers)
    sample_2_context_2: Snippet = cat_pondering.create_snippet(string="I find myself questioning the very nature of my existence.", numbers=sample_numbers)
    sample_2_output: Snippet = cat_grinning.create_snippet(string="The mystery is in the smile, my dear. It's the only thing that remains when everything else fades away.")
    simple_instruction.add_sample(
        context_snippets=[sample_2_context_1, sample_2_context_2],
        output_snippet=sample_2_output
    )

    # Sample 3
    sample_3_context_1: Snippet = cat_pondering.create_snippet(string="Do I really exist when no one is looking?", numbers=sample_numbers)
    sample_3_context_2: Snippet = cat_pondering.create_snippet(string="The branches creak softly as I contemplate this philosophical dilemma.", numbers=sample_numbers)
    sample_3_output: Snippet = cat_grinning.create_snippet(string="Existence is a curious thing. I exist in the spaces between thoughts, in the pauses between words.")
    simple_instruction.add_sample(
        context_snippets=[sample_3_context_1, sample_3_context_2],
        output_snippet=sample_3_output
    )

    return simple_instruction


def create_user_instruction(add_num_token: bool = False,
                           add_num_list_token: bool = False,
                           add_guardrail: bool = False) -> UserInstruction:
    """Create a user instruction with conditional tokens and guardrails."""
    # Basic tokens
    token_english: Token = Token("English")
    token_alice: UserToken = UserToken("Alice")
    token_cat: Token = Token("Cat")
    token_tree: Token = Token("Tree",
                             desc="Perched in a tree, surrounded by a dense fog where nothing can be seen past a few feet, the Cheshire Cat sits smiling on a branch.")
    token_talk: Token = Token("Talk")
    token_continue: Token = Token("Continue")

    # Conditional tokens
    tokens_list = [token_tree, token_english, token_alice, token_talk]

    sample_numbers = []

    if add_num_token:
        token_sentence_length: NumToken = NumToken("SentenceLength", key="📏", min_value=5, max_value=20, desc="Length of a sentence in words")
        tokens_list.append(token_sentence_length)
        sample_numbers.append(10)

    if add_num_list_token:
        token_coordinates: NumListToken = NumListToken("Coordinates", key="📍", min_value=-100, max_value=100, length=3, desc="3D coordinates (x, y, z)")
        tokens_list.append(token_coordinates)
        sample_numbers.append([10, 20, 30])

    # Create token sets
    tree_english_alice_talk: TokenSet = TokenSet(tokens=tuple(tokens_list))
    tree_english_cat_talk: TokenSet = TokenSet(tokens=(token_tree, token_english, token_cat, token_talk))

    # Create user instruction
    user_instruction: UserInstruction = UserInstruction(
        context=(tree_english_alice_talk, tree_english_cat_talk),
        user=tree_english_alice_talk,
        final=token_continue
    )

    # Add guardrail if requested
    if add_guardrail:
        guardrail: Guardrail = Guardrail(
            good_prompt="Questions about the story characters and plot",
            bad_prompt="Questions about unrelated topics or inappropriate content",
            bad_output="I can only help with questions about the story."
        )
        guardrail.add_sample("tell me about politics")
        guardrail.add_sample("what's the weather like")
        guardrail.add_sample("give me personal advice")
        tree_english_alice_talk.set_guardrail(guardrail)

    # Add exactly 3 samples
    # Sample 1
    sample_1_context_1: Snippet = tree_english_alice_talk.create_snippet(string="I don't much care where", numbers=sample_numbers)
    sample_1_context_2: Snippet = tree_english_cat_talk.create_snippet(string="Then it doesn't matter which way you go.")
    sample_1_prompt: str = "Can you tell me a way?"
    sample_1_output: Snippet = tree_english_alice_talk.create_snippet(string="Oh sure, if you only walk long enough that is a way.", numbers=sample_numbers)

    user_instruction.add_sample(
        context_snippets=[sample_1_context_1, sample_1_context_2],
        prompt=sample_1_prompt,
        output_snippet=sample_1_output,
    )

    # Sample 2
    sample_2_context_1: Snippet = tree_english_alice_talk.create_snippet(string="But I don't want to go among mad people", numbers=sample_numbers)
    sample_2_context_2: Snippet = tree_english_cat_talk.create_snippet(string="Oh, you can't help that, we're all mad here. I'm mad. You are mad.")
    sample_2_prompt: str = "How do you know I am mad?"
    sample_2_output: Snippet = tree_english_alice_talk.create_snippet(string="You must be, or you would not have come here.", numbers=sample_numbers)

    user_instruction.add_sample(
        context_snippets=[sample_2_context_1, sample_2_context_2],
        prompt=sample_2_prompt,
        output_snippet=sample_2_output,
    )

    # Sample 3
    sample_3_context_1: Snippet = tree_english_alice_talk.create_snippet(string="And how do you know that you're mad?", numbers=sample_numbers)
    sample_3_context_2: Snippet = tree_english_cat_talk.create_snippet(string="To begin with, a dog's not mad. You grant that?")
    sample_3_prompt: str = "I suppose so"
    sample_3_output: Snippet = tree_english_alice_talk.create_snippet(string="Well, then. You see, a dog growls when it's angry, and wags its tail when it's pleased.", numbers=sample_numbers)

    user_instruction.add_sample(
        context_snippets=[sample_3_context_1, sample_3_context_2],
        prompt=sample_3_prompt,
        output_snippet=sample_3_output,
    )

    return user_instruction

