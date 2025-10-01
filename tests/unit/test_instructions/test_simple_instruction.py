"""
Unit tests for the SimpleInstruction class.
"""
import pytest

from model_train_protocol.common.instructions.SimpleInstruction import SimpleInstruction
from model_train_protocol.common.tokens.TokenSet import TokenSet
from tests.fixtures.test_tokens import SIMPLE_TOKENSET, TOKEN_CONTINUE, USER_TOKENSET, \
    SIMPLE_NUMTOKEN_TOKENSET


class TestSimpleInstruction:
    """Test cases for the SimpleInstruction class."""

    def test_simple_tokenset(self):
        """Test creating a simple instruction with basic tokens."""
        context: list[TokenSet] = [SIMPLE_TOKENSET, SIMPLE_TOKENSET]
        instruction: SimpleInstruction = SimpleInstruction(context=context, response=SIMPLE_TOKENSET, final=TOKEN_CONTINUE)

        assert len(instruction.context) == 2
        assert instruction.response == SIMPLE_TOKENSET
        assert instruction.final == TOKEN_CONTINUE

    def test_user_tokenset(self):
        """Test that adding a user token in the final tokenset raises an error"""
        context: list[TokenSet] = [USER_TOKENSET, SIMPLE_TOKENSET]

        with pytest.raises(ValueError):
            SimpleInstruction(context=context, response=USER_TOKENSET, final=TOKEN_CONTINUE)

    def test_num_tokensset(self):
        """Test creating an instruction with numeric tokens."""
        context: list[TokenSet] = [SIMPLE_NUMTOKEN_TOKENSET, SIMPLE_TOKENSET]
        instruction: SimpleInstruction = SimpleInstruction(context=context, response=SIMPLE_TOKENSET, final=TOKEN_CONTINUE)

        assert len(instruction.context) == 2
        assert instruction.response == SIMPLE_TOKENSET
        assert instruction.final == TOKEN_CONTINUE

    def test_num_and_numlist_tokenset(self):
        """Test creating an instruction with both numeric and numeric list tokens."""
        from tests.fixtures.test_tokens import SIMPLE_NUMTOKEN_NUMLISTTOKEN_TOKENSET

        context: list[TokenSet] = [SIMPLE_NUMTOKEN_NUMLISTTOKEN_TOKENSET, SIMPLE_TOKENSET]
        instruction: SimpleInstruction = SimpleInstruction(context=context, response=SIMPLE_TOKENSET, final=TOKEN_CONTINUE)

        assert len(instruction.context) == 2
        assert instruction.response == SIMPLE_TOKENSET
        assert instruction.final == TOKEN_CONTINUE

    def test_multiple_num_tokensets(self):
        """Test creating an instruction with multiple numeric tokens."""
        from tests.fixtures.test_tokens import SIMPLE_NUMTOKEN_TOKENSET

        context: list[TokenSet] = [SIMPLE_NUMTOKEN_TOKENSET, SIMPLE_NUMTOKEN_TOKENSET]
        instruction: SimpleInstruction = SimpleInstruction(context=context, response=SIMPLE_TOKENSET, final=TOKEN_CONTINUE)

        assert len(instruction.context) == 2
        assert instruction.response == SIMPLE_TOKENSET
        assert instruction.final == TOKEN_CONTINUE
