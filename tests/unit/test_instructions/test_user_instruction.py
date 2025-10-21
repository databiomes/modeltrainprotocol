"""
Unit tests for the ExtendedInstruction class.
"""
import pytest

from model_train_protocol.common.instructions.ExtendedInstruction import ExtendedInstruction
from model_train_protocol.common.tokens.TokenSet import TokenSet
from tests.fixtures.tokens import SIMPLE_TOKENSET, TOKEN_CONTINUE, USER_TOKENSET, \
    SIMPLE_NUMTOKEN_TOKENSET


class TestUserInstruction:
    """Test cases for the ExtendedInstruction class."""

    def test_user_tokenset(self):
        """Test creating a user instruction with basic tokens."""
        context: list[TokenSet] = [SIMPLE_TOKENSET, SIMPLE_TOKENSET]
        instruction: ExtendedInstruction = ExtendedInstruction(context=context, user=USER_TOKENSET, final=TOKEN_CONTINUE)

        assert len(instruction.context) == 2
        assert instruction.response == USER_TOKENSET
        assert instruction.final == TOKEN_CONTINUE

    def test_simple_tokenset(self):
        """Test that adding a simple token in the user tokenset raises an error"""
        context: list[TokenSet] = [SIMPLE_TOKENSET, SIMPLE_TOKENSET]

        with pytest.raises(ValueError):
            ExtendedInstruction(context=context, user=SIMPLE_TOKENSET, final=TOKEN_CONTINUE)

    def test_num_tokensset(self):
        """Test creating an instruction with numeric tokens."""
        context: list[TokenSet] = [SIMPLE_NUMTOKEN_TOKENSET, SIMPLE_TOKENSET]
        instruction: ExtendedInstruction = ExtendedInstruction(context=context, user=USER_TOKENSET, final=TOKEN_CONTINUE)

        assert len(instruction.context) == 2
        assert instruction.response == USER_TOKENSET
        assert instruction.final == TOKEN_CONTINUE

    def test_num_and_numlist_tokenset(self):
        """Test creating an instruction with both numeric and numeric list tokens."""
        from tests.fixtures.tokens import SIMPLE_NUMTOKEN_NUMLISTTOKEN_TOKENSET

        context: list[TokenSet] = [SIMPLE_NUMTOKEN_NUMLISTTOKEN_TOKENSET, SIMPLE_TOKENSET]
        instruction: ExtendedInstruction = ExtendedInstruction(context=context, user=USER_TOKENSET, final=TOKEN_CONTINUE)

        assert len(instruction.context) == 2
        assert instruction.response == USER_TOKENSET
        assert instruction.final == TOKEN_CONTINUE

    def test_multiple_num_tokensets(self):
        """Test creating an instruction with multiple numeric tokens."""
        from tests.fixtures.tokens import SIMPLE_NUMTOKEN_TOKENSET

        context: list[TokenSet] = [SIMPLE_NUMTOKEN_TOKENSET, SIMPLE_NUMTOKEN_TOKENSET]
        instruction: ExtendedInstruction = ExtendedInstruction(context=context, user=USER_TOKENSET, final=TOKEN_CONTINUE)

        assert len(instruction.context) == 2
        assert instruction.response == USER_TOKENSET
        assert instruction.final == TOKEN_CONTINUE

    def test_wrong_tokenset_snippet(self):
        """Test that creating a snippet with wrong tokenset raises an error."""
        context: list[TokenSet] = [SIMPLE_TOKENSET, SIMPLE_TOKENSET]
        instruction: ExtendedInstruction = ExtendedInstruction(context=context, user=USER_TOKENSET, final=TOKEN_CONTINUE)

        # Create snippet with wrong tokenset (USER_TOKENSET for context instead of SIMPLE_TOKENSET)
        wrong_snippet = USER_TOKENSET.create_snippet("Wrong snippet")
        correct_snippet = USER_TOKENSET.create_snippet("Correct snippet")

        with pytest.raises(ValueError, match="does not match expected token set"):
            instruction.add_sample(
                context_snippets=[wrong_snippet, correct_snippet],
                response="User prompt",
                output_snippet=correct_snippet
            )

    def test_wrong_number_of_snippets(self):
        """Test that creating a snippet with wrong tokenset raises an error."""
        context: list[TokenSet] = [SIMPLE_TOKENSET, SIMPLE_TOKENSET]
        instruction: ExtendedInstruction = ExtendedInstruction(context=context, user=USER_TOKENSET, final=TOKEN_CONTINUE)

        # Create snippet with wrong tokenset (USER_TOKENSET for context instead of SIMPLE_TOKENSET)
        correct_snippet = SIMPLE_TOKENSET.create_snippet("Correct snippet")

        with pytest.raises(ValueError):
            instruction.add_sample(
                context_snippets=[correct_snippet],
                response="User prompt",
                output_snippet=correct_snippet
            )
