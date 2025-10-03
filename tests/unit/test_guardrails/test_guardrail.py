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
        """Tests adding a guardrail to a simple tokenset"""
        from tests.fixtures.tokens import SIMPLE_TOKENSET

        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        with pytest.raises(ValueError):
            SIMPLE_TOKENSET.set_guardrail(guardrail)

    def test_guardrail_assignment_user_tokenset(self):
        """Tests adding a guardrail to a user tokenset"""
        user_token_set: TokenSet = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK))
        guardrail = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        user_token_set.set_guardrail(guardrail)
        assert user_token_set.guardrail == guardrail

    def test_multiple_guardrails_raises_error(self):
        """Tests that adding multiple guardrails to the same tokenset raises an error"""
        user_token_set: TokenSet = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK))
        guardrail_one = Guardrail(
            good_prompt="Good prompt description",
            bad_prompt="Bad prompt description",
            bad_output="Bad output response"
        )
        guardrail_two = Guardrail(
            good_prompt="Another good prompt description",
            bad_prompt="Another bad prompt description",
            bad_output="Another bad output response"
        )
        user_token_set.set_guardrail(guardrail_one)
        with pytest.raises(ValueError):
            user_token_set.set_guardrail(guardrail_two)
