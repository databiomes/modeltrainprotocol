"""
Unit tests for the UserInstruction class.
"""
import pytest

from model_train_protocol.common.instructions.UserInstruction import UserInstruction
from model_train_protocol.common.tokens.TokenSet import TokenSet
from tests.fixtures.test_tokens import SIMPLE_TOKENSET, TOKEN_CONTINUE, USER_TOKENSET, \
    SIMPLE_NUMTOKEN_TOKENSET


class TestUserInstruction:
    """Test cases for the UserInstruction class."""

    def test_user_tokenset(self):
        """Test creating a user instruction with basic tokens."""
        context: list[TokenSet] = [SIMPLE_TOKENSET, SIMPLE_TOKENSET]
        instruction: UserInstruction = UserInstruction(context=context, user=USER_TOKENSET, final=TOKEN_CONTINUE)

        assert len(instruction.context) == 2
        assert instruction.response == USER_TOKENSET
        assert instruction.final == TOKEN_CONTINUE

    def test_simple_tokenset(self):
        """Test that adding a simple token in the user tokenset raises an error"""
        context: list[TokenSet] = [SIMPLE_TOKENSET, SIMPLE_TOKENSET]

        with pytest.raises(ValueError):
            UserInstruction(context=context, user=SIMPLE_TOKENSET, final=TOKEN_CONTINUE)

    def test_num_tokensset(self):
        """Test creating an instruction with numeric tokens."""
        context: list[TokenSet] = [SIMPLE_NUMTOKEN_TOKENSET, SIMPLE_TOKENSET]
        instruction: UserInstruction = UserInstruction(context=context, user=USER_TOKENSET, final=TOKEN_CONTINUE)

        assert len(instruction.context) == 2
        assert instruction.response == USER_TOKENSET
        assert instruction.final == TOKEN_CONTINUE

    def test_num_and_numlist_tokenset(self):
        """Test creating an instruction with both numeric and numeric list tokens."""
        from tests.fixtures.test_tokens import SIMPLE_NUMTOKEN_NUMLISTTOKEN_TOKENSET

        context: list[TokenSet] = [SIMPLE_NUMTOKEN_NUMLISTTOKEN_TOKENSET, SIMPLE_TOKENSET]
        instruction: UserInstruction = UserInstruction(context=context, user=USER_TOKENSET, final=TOKEN_CONTINUE)

        assert len(instruction.context) == 2
        assert instruction.response == USER_TOKENSET
        assert instruction.final == TOKEN_CONTINUE

    def test_multiple_num_tokensets(self):
        """Test creating an instruction with multiple numeric tokens."""
        from tests.fixtures.test_tokens import SIMPLE_NUMTOKEN_TOKENSET

        context: list[TokenSet] = [SIMPLE_NUMTOKEN_TOKENSET, SIMPLE_NUMTOKEN_TOKENSET]
        instruction: UserInstruction = UserInstruction(context=context, user=USER_TOKENSET, final=TOKEN_CONTINUE)

        assert len(instruction.context) == 2
        assert instruction.response == USER_TOKENSET
        assert instruction.final == TOKEN_CONTINUE
