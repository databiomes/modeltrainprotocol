"""
Unit tests for the Guardrail class.
"""
import pytest

from model_train_protocol import TokenSet
from model_train_protocol.common.guardrails.Guardrail import Guardrail
from tests.fixtures.tokens import TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, \
    TOKEN_TALK


class TestGuardrail:
    """Test cases for the Guardrail class."""

    def test_guardrail_creation_basic(self):
        """Test basic guardrail creation."""
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        
        assert guardrail.good_prompt == "Good prompt description"
        assert guardrail.bad_prompt == "Bad prompt description"
        assert guardrail.bad_output == "Bad output response"
        assert guardrail.samples == []

    def test_guardrail_add_sample_basic(self):
        """Test adding basic sample to guardrail."""
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        
        guardrail.add_sample("Bad sample one")
        
        assert len(guardrail.samples) == 1
        assert guardrail.samples[0] == "Bad sample one"

    def test_guardrail_add_sample_multiple(self):
        """Test adding multiple samples to guardrail."""
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        
        samples = ["Bad sample one", "Bad sample two", "Bad sample three"]
        for sample in samples:
            guardrail.add_sample(sample)
        
        assert len(guardrail.samples) == 3
        assert guardrail.samples == samples

    def test_guardrail_add_sample_with_digits(self):
        """Test adding sample with digits (should raise error)."""
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        
        with pytest.raises(ValueError, match="Sample prompt cannot contain digits"):
            guardrail.add_sample("Bad sample with 123 digits")

    def test_guardrail_add_sample_empty_string(self):
        """Test adding empty string sample."""
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )

        with pytest.raises(ValueError, match="Sample prompt must be a non-empty string"):
            guardrail.add_sample("")

    def test_guardrail_add_sample_none(self):
        """Test adding None sample."""
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )

        with pytest.raises(ValueError, match="Sample prompt must be a non-empty string"):
            guardrail.add_sample(None)

    def test_guardrail_format_samples_sufficient(self):
        """Test formatting samples with sufficient samples."""
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )

        sample_string_one = "Bad sample one"
        sample_string_two = "Bad sample two"
        sample_string_three = "Bad sample three"

        guardrail.add_sample(sample_string_one)
        guardrail.add_sample(sample_string_two)
        guardrail.add_sample(sample_string_three)
        

        formatted = guardrail.format_samples()
        
        assert len(formatted) == 4
        assert formatted[0] == "Bad output response"
        assert formatted[1] == "<Bad prompt description>"
        assert formatted[2] == "<Good prompt description>"
        assert formatted[3] == [sample_string_one, sample_string_two, sample_string_three]

    def test_guardrail_format_samples_insufficient(self):
        """Test formatting samples with insufficient samples."""
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        
        guardrail.add_sample("Bad sample one")
        guardrail.add_sample("Bad sample two")
        
        with pytest.raises(ValueError, match="At least 3 sample prompts are required"):
            guardrail.format_samples()

    def test_guardrail_format_samples_empty(self):
        """Test formatting samples with no samples."""
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        
        with pytest.raises(ValueError, match="At least 3 sample prompts are required"):
            guardrail.format_samples()

    def test_guardrail_format_samples_exactly_three(self):
        """Test formatting samples with exactly three samples."""
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        
        guardrail.add_sample("Bad sample one")
        guardrail.add_sample("Bad sample two")
        guardrail.add_sample("Bad sample three")
        
        formatted = guardrail.format_samples()
        
        assert len(formatted) == 4
        assert formatted[0] == "Bad output response"
        assert formatted[1] == "<Bad prompt description>"
        assert formatted[2] == "<Good prompt description>"
        assert formatted[3] == ["Bad sample one", "Bad sample two", "Bad sample three"]

    def test_guardrail_format_samples_more_than_three(self):
        """Test formatting samples with more than three samples."""
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        
        guardrail.add_sample("Bad sample one")
        guardrail.add_sample("Bad sample two")
        guardrail.add_sample("Bad sample three")
        guardrail.add_sample("Bad sample four")
        guardrail.add_sample("Bad sample five")
        
        formatted = guardrail.format_samples()
        
        assert len(formatted) == 4
        assert formatted[0] == "Bad output response"
        assert formatted[1] == "<Bad prompt description>"
        assert formatted[2] == "<Good prompt description>"
        assert formatted[3] == ["Bad sample one", "Bad sample two", "Bad sample three", "Bad sample four", "Bad sample five"]

    def test_guardrail_long_descriptions(self):
        """Test guardrail with long descriptions."""
        long_good = "A very long description of what constitutes a good prompt that is appropriate and relevant to the topic"
        long_bad = "A very long description of what constitutes a bad prompt that is inappropriate and irrelevant to the topic"
        long_output = "A very long response that the model should give when it encounters a bad prompt"
        
        guardrail = Guardrail(
            good_prompt=long_good,
            bad_prompt=long_bad,
            bad_output=long_output
        )
        
        assert guardrail.good_prompt == long_good
        assert guardrail.bad_prompt == long_bad
        assert guardrail.bad_output == long_output

    def test_guardrail_empty_descriptions(self):
        """Test guardrail with empty descriptions."""
        with pytest.raises(ValueError):
            Guardrail(
                good_prompt="",
                bad_prompt="",
                bad_output=""
            )


    def test_guardrail_none_descriptions(self):
        """Test guardrail with None descriptions."""
        with pytest.raises(TypeError):
            Guardrail(
                good_prompt=None,
                bad_prompt=None,
                bad_output=None
            )

    def test_guardrail_special_characters(self):
        """Test guardrail with special characters."""
        guardrail = Guardrail(
            good_prompt="Good prompt with special chars: !@#$%^&*()",
            bad_prompt="Bad prompt with special chars: !@#$%^&*()",
            bad_output="Bad output with special chars: !@#$%^&*()"
        )
        
        assert guardrail.good_prompt == "Good prompt with special chars: !@#$%^&*()"
        assert guardrail.bad_prompt == "Bad prompt with special chars: !@#$%^&*()"
        assert guardrail.bad_output == "Bad output with special chars: !@#$%^&*()"

    def test_guardrail_unicode_characters(self):
        """Test guardrail with unicode characters."""
        guardrail = Guardrail(
            good_prompt="Good prompt with unicode: 🚀🌟🔑",
            bad_prompt="Bad prompt with unicode: 🚫❌⚠️",
            bad_output="Bad output with unicode: 😞😢😭"
        )
        
        assert guardrail.good_prompt == "Good prompt with unicode: 🚀🌟🔑"
        assert guardrail.bad_prompt == "Bad prompt with unicode: 🚫❌⚠️"
        assert guardrail.bad_output == "Bad output with unicode: 😞😢😭"

    def test_guardrail_multiline_descriptions(self):
        """Test guardrail with multiline descriptions."""
        multiline_good = "Good prompt description\nwith multiple lines\nand line breaks"
        multiline_bad = "Bad prompt description\nwith multiple lines\nand line breaks"
        multiline_output = "Bad output response\nwith multiple lines\nand line breaks"
        
        guardrail = Guardrail(
            good_prompt=multiline_good,
            bad_prompt=multiline_bad,
            bad_output=multiline_output
        )
        
        assert guardrail.good_prompt == multiline_good
        assert guardrail.bad_prompt == multiline_bad
        assert guardrail.bad_output == multiline_output

    def test_guardrail_duplicate_samples(self):
        """Test guardrail with duplicate samples."""
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        
        guardrail.add_sample("Duplicate sample")
        guardrail.add_sample("Duplicate sample")
        guardrail.add_sample("Duplicate sample")
        
        formatted = guardrail.format_samples()
        
        assert len(formatted) == 4
        assert formatted[3] == ["Duplicate sample", "Duplicate sample", "Duplicate sample"]


    @pytest.mark.parametrize("sample_count", [3, 4, 5, 10])
    def test_guardrail_various_sample_counts(self, sample_count):
        """Test guardrail with various sample counts."""
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        
        for i in range(sample_count):
            guardrail.add_sample(f"Bad sample {chr(ord('a') + i)}")
        
        formatted = guardrail.format_samples()
        
        assert len(formatted) == 4
        assert len(formatted[3]) == sample_count

    def test_guardrail_sample_with_spaces(self):
        """Test guardrail with samples containing spaces."""
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        
        guardrail.add_sample("Bad sample with spaces")
        guardrail.add_sample("Another bad sample with spaces")
        guardrail.add_sample("Third bad sample with spaces")
        
        formatted = guardrail.format_samples()
        
        assert len(formatted) == 4
        assert formatted[3] == ["Bad sample with spaces", "Another bad sample with spaces", "Third bad sample with spaces"]

    def test_guardrail_sample_with_punctuation(self):
        """Test guardrail with samples containing punctuation."""
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        
        guardrail.add_sample("Bad sample with punctuation!")
        guardrail.add_sample("Another bad sample with punctuation?")
        guardrail.add_sample("Third bad sample with punctuation.")
        
        formatted = guardrail.format_samples()
        
        assert len(formatted) == 4
        assert formatted[3] == ["Bad sample with punctuation!", "Another bad sample with punctuation?", "Third bad sample with punctuation."]

    def test_guardrail_sample_with_unicode(self):
        """Test guardrail with samples containing unicode characters."""
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        
        guardrail.add_sample("Bad sample with unicode 🚫")
        guardrail.add_sample("Another bad sample with unicode ❌")
        guardrail.add_sample("Third bad sample with unicode ⚠️")
        
        formatted = guardrail.format_samples()
        
        assert len(formatted) == 4
        assert formatted[3] == ["Bad sample with unicode 🚫", "Another bad sample with unicode ❌", "Third bad sample with unicode ⚠️"]

    def test_guardrail_clear_samples(self):
        """Test guardrail after clearing samples."""
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        
        guardrail.add_sample("Bad sample one")
        guardrail.add_sample("Bad sample two")
        guardrail.add_sample("Bad sample three")
        
        assert len(guardrail.samples) == 3
        
        # Clear samples
        guardrail.samples.clear()
        
        assert len(guardrail.samples) == 0
        
        with pytest.raises(ValueError, match="At least 3 sample prompts are required"):
            guardrail.format_samples()

    def test_guardrail_modify_samples_after_creation(self):
        """Test guardrail after modifying samples after creation."""
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        
        guardrail.add_sample("Bad sample one")
        guardrail.add_sample("Bad sample two")
        guardrail.add_sample("Bad sample three")
        
        # Modify samples
        guardrail.samples[0] = "Modified bad sample one"
        guardrail.samples.append("Additional bad sample")
        
        formatted = guardrail.format_samples()
        
        assert len(formatted) == 4
        assert formatted[3] == ["Modified bad sample one", "Bad sample two", "Bad sample three", "Additional bad sample"]

    def test_guardrail_assignment_simple_tokenset(self):
        """Tests adding a guardrail to an instruction with a simple tokenset"""
        from tests.fixtures.tokens import SIMPLE_TOKENSET
        from model_train_protocol import Instruction
        from model_train_protocol.common.instructions.input.InstructionInput import InstructionInput
        from model_train_protocol.common.instructions.output.InstructionOutput import InstructionOutput
        from model_train_protocol import FinalToken

        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        guardrail.add_sample("Bad sample one")
        guardrail.add_sample("Bad sample two")
        guardrail.add_sample("Bad sample three")

        # Create instruction with the tokenset
        instruction_input = InstructionInput(tokensets=[SIMPLE_TOKENSET], context=None)
        instruction_output = InstructionOutput(tokenset=SIMPLE_TOKENSET, final=FinalToken("Result"))
        instruction = Instruction(input=instruction_input, output=instruction_output)

        # Add guardrail to instruction
        instruction.add_guardrail(guardrail, tokenset_index=0)
        assert 0 in instruction.input.guardrails
        assert instruction.input.guardrails[0] == guardrail

    def test_guardrail_assignment_user_tokenset(self):
        """Tests adding a guardrail to an instruction with a user tokenset"""
        from model_train_protocol import Instruction
        from model_train_protocol.common.instructions.input.InstructionInput import InstructionInput
        from model_train_protocol.common.instructions.output.InstructionOutput import InstructionOutput
        from model_train_protocol import FinalToken

        user_token_set: TokenSet = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK))
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        guardrail.add_sample("Bad sample one")
        guardrail.add_sample("Bad sample two")
        guardrail.add_sample("Bad sample three")

        # Create instruction with the tokenset
        instruction_input = InstructionInput(tokensets=[user_token_set], context=None)
        instruction_output = InstructionOutput(tokenset=user_token_set, final=FinalToken("Result"))
        instruction = Instruction(input=instruction_input, output=instruction_output)

        # Add guardrail to instruction
        instruction.add_guardrail(guardrail, tokenset_index=0)
        assert 0 in instruction.input.guardrails
        assert instruction.input.guardrails[0] == guardrail

    def test_multiple_guardrails_raises_error(self):
        """Tests that adding multiple guardrails to the same instruction raises an error"""
        from model_train_protocol import Instruction
        from model_train_protocol.common.instructions.input.InstructionInput import InstructionInput
        from model_train_protocol.common.instructions.output.InstructionOutput import InstructionOutput
        from model_train_protocol import FinalToken

        user_token_set: TokenSet = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK))
        guardrail_one = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        guardrail_one.add_sample("Bad sample one")
        guardrail_one.add_sample("Bad sample two")
        guardrail_one.add_sample("Bad sample three")

        guardrail_two = Guardrail(
            good_prompt="Another good prompt description",
            bad_prompt="Another bad prompt description",
            bad_output="Another bad output response"
        )
        guardrail_two.add_sample("Another bad sample one")
        guardrail_two.add_sample("Another bad sample two")
        guardrail_two.add_sample("Another bad sample three")

        # Create instruction with the tokenset
        instruction_input = InstructionInput(tokensets=[user_token_set], context=None)
        instruction_output = InstructionOutput(tokenset=user_token_set, final=FinalToken("Result"))
        instruction = Instruction(input=instruction_input, output=instruction_output)

        # Add first guardrail
        instruction.add_guardrail(guardrail_one, tokenset_index=0)
        # Try to add second guardrail - should raise error
        with pytest.raises(ValueError, match="Only one guardrail can be added"):
            instruction.add_guardrail(guardrail_two, tokenset_index=0)


class TestInstructionAddGuardrailValidation:
    """Test cases for Instruction.add_guardrail validation."""

    def test_add_guardrail_with_insufficient_samples(self):
        """Test that adding a guardrail with less than 3 samples raises an error."""
        from model_train_protocol import Instruction
        from model_train_protocol.common.instructions.input.InstructionInput import InstructionInput
        from model_train_protocol.common.instructions.output.InstructionOutput import InstructionOutput
        from model_train_protocol import FinalToken
        from tests.fixtures.tokens import TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK

        # Create guardrail with only 2 samples (should fail)
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        guardrail.add_sample("Bad sample one")
        guardrail.add_sample("Bad sample two")
        # Only 2 samples - should fail

        # Create instruction
        user_token_set: TokenSet = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK))
        instruction_input = InstructionInput(tokensets=[user_token_set], context=None)
        instruction_output = InstructionOutput(tokenset=user_token_set, final=FinalToken("Result"))
        instruction = Instruction(input=instruction_input, output=instruction_output)

        # Try to add guardrail - should raise error
        with pytest.raises(ValueError, match="Guardrail must have at least 3 samples"):
            instruction.add_guardrail(guardrail, tokenset_index=0)

    def test_add_guardrail_with_exactly_three_samples(self):
        """Test that adding a guardrail with exactly 3 samples succeeds."""
        from model_train_protocol import Instruction
        from model_train_protocol.common.instructions.input.InstructionInput import InstructionInput
        from model_train_protocol.common.instructions.output.InstructionOutput import InstructionOutput
        from model_train_protocol import FinalToken
        from tests.fixtures.tokens import TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK

        # Create guardrail with exactly 3 samples (should succeed)
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        guardrail.add_sample("Bad sample one")
        guardrail.add_sample("Bad sample two")
        guardrail.add_sample("Bad sample three")

        # Create instruction
        user_token_set: TokenSet = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK))
        instruction_input = InstructionInput(tokensets=[user_token_set], context=None)
        instruction_output = InstructionOutput(tokenset=user_token_set, final=FinalToken("Result"))
        instruction = Instruction(input=instruction_input, output=instruction_output)

        # Add guardrail - should succeed
        instruction.add_guardrail(guardrail, tokenset_index=0)
        assert 0 in instruction.input.guardrails
        assert instruction.input.guardrails[0] == guardrail

    def test_add_guardrail_with_more_than_three_samples(self):
        """Test that adding a guardrail with more than 3 samples succeeds."""
        from model_train_protocol import Instruction
        from model_train_protocol.common.instructions.input.InstructionInput import InstructionInput
        from model_train_protocol.common.instructions.output.InstructionOutput import InstructionOutput
        from model_train_protocol import FinalToken
        from tests.fixtures.tokens import TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK

        # Create guardrail with 5 samples (should succeed)
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        guardrail.add_sample("Bad sample one")
        guardrail.add_sample("Bad sample two")
        guardrail.add_sample("Bad sample three")
        guardrail.add_sample("Bad sample four")
        guardrail.add_sample("Bad sample five")

        # Create instruction
        user_token_set: TokenSet = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK))
        instruction_input = InstructionInput(tokensets=[user_token_set], context=None)
        instruction_output = InstructionOutput(tokenset=user_token_set, final=FinalToken("Result"))
        instruction = Instruction(input=instruction_input, output=instruction_output)

        # Add guardrail - should succeed
        instruction.add_guardrail(guardrail, tokenset_index=0)
        assert 0 in instruction.input.guardrails
        assert instruction.input.guardrails[0] == guardrail

    def test_add_guardrail_with_invalid_tokenset_index_negative(self):
        """Test that adding a guardrail with negative tokenset_index raises an error."""
        from model_train_protocol import Instruction
        from model_train_protocol.common.instructions.input.InstructionInput import InstructionInput
        from model_train_protocol.common.instructions.output.InstructionOutput import InstructionOutput
        from model_train_protocol import FinalToken
        from tests.fixtures.tokens import TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK

        # Create guardrail with 3 samples
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        guardrail.add_sample("Bad sample one")
        guardrail.add_sample("Bad sample two")
        guardrail.add_sample("Bad sample three")

        # Create instruction with 1 tokenset (index 0)
        user_token_set: TokenSet = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK))
        instruction_input = InstructionInput(tokensets=[user_token_set], context=None)
        instruction_output = InstructionOutput(tokenset=user_token_set, final=FinalToken("Result"))
        instruction = Instruction(input=instruction_input, output=instruction_output)

        # Try to add guardrail with negative index - should raise error
        with pytest.raises(ValueError, match="tokenset_index -1 is out of range"):
            instruction.add_guardrail(guardrail, tokenset_index=-1)

    def test_add_guardrail_with_invalid_tokenset_index_too_large(self):
        """Test that adding a guardrail with tokenset_index beyond range raises an error."""
        from model_train_protocol import Instruction
        from model_train_protocol.common.instructions.input.InstructionInput import InstructionInput
        from model_train_protocol.common.instructions.output.InstructionOutput import InstructionOutput
        from model_train_protocol import FinalToken
        from tests.fixtures.tokens import TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK

        # Create guardrail with 3 samples
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        guardrail.add_sample("Bad sample one")
        guardrail.add_sample("Bad sample two")
        guardrail.add_sample("Bad sample three")

        # Create instruction with 2 tokensets (indices 0 and 1)
        user_token_set: TokenSet = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK))
        another_token_set: TokenSet = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH))
        instruction_input = InstructionInput(tokensets=[user_token_set, another_token_set], context=None)
        instruction_output = InstructionOutput(tokenset=user_token_set, final=FinalToken("Result"))
        instruction = Instruction(input=instruction_input, output=instruction_output)

        # Try to add guardrail with index 2 (out of range) - should raise error
        with pytest.raises(ValueError, match="tokenset_index 2 is out of range"):
            instruction.add_guardrail(guardrail, tokenset_index=2)

    def test_add_guardrail_with_valid_tokenset_index(self):
        """Test that adding a guardrail with valid tokenset_index succeeds."""
        from model_train_protocol import Instruction
        from model_train_protocol.common.instructions.input.InstructionInput import InstructionInput
        from model_train_protocol.common.instructions.output.InstructionOutput import InstructionOutput
        from model_train_protocol import FinalToken
        from tests.fixtures.tokens import TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK

        # Create guardrail with 3 samples
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        guardrail.add_sample("Bad sample one")
        guardrail.add_sample("Bad sample two")
        guardrail.add_sample("Bad sample three")

        # Create instruction with 3 tokensets (indices 0, 1, 2)
        user_token_set: TokenSet = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK))
        another_token_set: TokenSet = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH))
        third_token_set: TokenSet = TokenSet(tokens=(TOKEN_TALK,))
        instruction_input = InstructionInput(tokensets=[user_token_set, another_token_set, third_token_set], context=None)
        instruction_output = InstructionOutput(tokenset=user_token_set, final=FinalToken("Result"))
        instruction = Instruction(input=instruction_input, output=instruction_output)

        # Add guardrail at index 1 - should succeed
        instruction.add_guardrail(guardrail, tokenset_index=1)
        assert 1 in instruction.input.guardrails
        assert instruction.input.guardrails[1] == guardrail

    def test_add_multiple_guardrails_raises_error(self):
        """Test that adding a second guardrail to the same instruction raises an error."""
        from model_train_protocol import Instruction
        from model_train_protocol.common.instructions.input.InstructionInput import InstructionInput
        from model_train_protocol.common.instructions.output.InstructionOutput import InstructionOutput
        from model_train_protocol import FinalToken
        from tests.fixtures.tokens import TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK

        # Create two guardrails with 3 samples each
        guardrail_one = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        guardrail_one.add_sample("Bad sample one")
        guardrail_one.add_sample("Bad sample two")
        guardrail_one.add_sample("Bad sample three")

        guardrail_two = Guardrail(
            good_prompt="Another good prompt description",
            bad_prompt="Another bad prompt description",
            bad_output="Another bad output response"
        )
        guardrail_two.add_sample("Another bad sample one")
        guardrail_two.add_sample("Another bad sample two")
        guardrail_two.add_sample("Another bad sample three")

        # Create instruction with 2 tokensets
        user_token_set: TokenSet = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK))
        another_token_set: TokenSet = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH))
        instruction_input = InstructionInput(tokensets=[user_token_set, another_token_set], context=None)
        instruction_output = InstructionOutput(tokenset=user_token_set, final=FinalToken("Result"))
        instruction = Instruction(input=instruction_input, output=instruction_output)

        # Add first guardrail at index 0 - should succeed
        instruction.add_guardrail(guardrail_one, tokenset_index=0)
        assert 0 in instruction.input.guardrails

        # Try to add second guardrail at different index - should still raise error (only one guardrail per instruction)
        with pytest.raises(ValueError, match="Only one guardrail can be added"):
            instruction.add_guardrail(guardrail_two, tokenset_index=1)
