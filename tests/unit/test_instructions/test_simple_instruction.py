"""
Unit tests for the Instruction class.
"""
import pytest

from model_train_protocol.common.instructions.Instruction import Instruction
from model_train_protocol.common.tokens.TokenSet import TokenSet
from tests.fixtures.tokens import SIMPLE_TOKENSET, TOKEN_CONTINUE, USER_TOKENSET, \
    SIMPLE_NUMTOKEN_TOKENSET


class TestSimpleInstruction:
    """Test cases for the Instruction class."""

    def test_simple_tokenset(self):
        """Test creating a simple instruction with basic tokens."""
        context: list[TokenSet] = [SIMPLE_TOKENSET, SIMPLE_TOKENSET]
        instruction: Instruction = Instruction(context=context, response=SIMPLE_TOKENSET, final=TOKEN_CONTINUE)

        assert len(instruction.context) == 2
        assert instruction.response == SIMPLE_TOKENSET
        assert instruction.final == TOKEN_CONTINUE

    def test_user_tokenset(self):
        """Test that adding a user token in the final tokenset succeeds"""
        context: list[TokenSet] = [USER_TOKENSET, SIMPLE_TOKENSET]

        # Should not raise error since UserToken validation is no longer required
        instruction = Instruction(context=context, response=USER_TOKENSET, final=TOKEN_CONTINUE)
        assert instruction is not None

    def test_num_tokensset(self):
        """Test creating an instruction with numeric tokens."""
        context: list[TokenSet] = [SIMPLE_NUMTOKEN_TOKENSET, SIMPLE_TOKENSET]
        instruction: Instruction = Instruction(context=context, response=SIMPLE_TOKENSET, final=TOKEN_CONTINUE)

        assert len(instruction.context) == 2
        assert instruction.response == SIMPLE_TOKENSET
        assert instruction.final == TOKEN_CONTINUE

    def test_num_and_numlist_tokenset(self):
        """Test creating an instruction with both numeric and numeric list tokens."""
        from tests.fixtures.tokens import SIMPLE_NUMTOKEN_NUMLISTTOKEN_TOKENSET

        context: list[TokenSet] = [SIMPLE_NUMTOKEN_NUMLISTTOKEN_TOKENSET, SIMPLE_TOKENSET]
        instruction: Instruction = Instruction(context=context, response=SIMPLE_TOKENSET, final=TOKEN_CONTINUE)

        assert len(instruction.context) == 2
        assert instruction.response == SIMPLE_TOKENSET
        assert instruction.final == TOKEN_CONTINUE

    def test_multiple_num_tokensets(self):
        """Test creating an instruction with multiple numeric tokens."""
        from tests.fixtures.tokens import SIMPLE_NUMTOKEN_TOKENSET

        context: list[TokenSet] = [SIMPLE_NUMTOKEN_TOKENSET, SIMPLE_NUMTOKEN_TOKENSET]
        instruction: Instruction = Instruction(context=context, response=SIMPLE_TOKENSET, final=TOKEN_CONTINUE)

        assert len(instruction.context) == 2
        assert instruction.response == SIMPLE_TOKENSET
        assert instruction.final == TOKEN_CONTINUE

    def test_wrong_tokenset_snippet(self):
        """Test that creating a snippet with wrong tokenset raises an error."""
        context: list[TokenSet] = [SIMPLE_TOKENSET, SIMPLE_TOKENSET]
        instruction: Instruction = Instruction(context=context, response=SIMPLE_TOKENSET, final=TOKEN_CONTINUE)

        # Create snippet with wrong tokenset (USER_TOKENSET instead of SIMPLE_TOKENSET)
        wrong_snippet = USER_TOKENSET.create_snippet("Wrong snippet")
        correct_snippet = SIMPLE_TOKENSET.create_snippet("Correct snippet")

        with pytest.raises(ValueError, match="does not match expected token set"):
            instruction.add_sample(
                context_snippets=[wrong_snippet, correct_snippet],
                response_snippet=correct_snippet
            )
    def test_wrong_number_of_snippets(self):
        """Test that creating a snippet with wrong tokenset raises an error."""
        context: list[TokenSet] = [SIMPLE_TOKENSET, SIMPLE_TOKENSET]
        instruction: Instruction = Instruction(context=context, response=SIMPLE_TOKENSET, final=TOKEN_CONTINUE)

        # Create snippet with wrong tokenset (USER_TOKENSET instead of SIMPLE_TOKENSET)
        correct_snippet = SIMPLE_TOKENSET.create_snippet("Correct snippet")

        with pytest.raises(ValueError):
            instruction.add_sample(
                context_snippets=[correct_snippet],
                response_snippet=correct_snippet
            )