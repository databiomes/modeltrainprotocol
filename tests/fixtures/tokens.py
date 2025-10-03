"""
Sample token data for testing.
"""
import pytest
from typing import Dict, List, Any, Union, Tuple
from model_train_protocol import Token, UserToken, NumToken, NumListToken, TokenSet


# Basic token fixtures
@pytest.fixture
def token_english() -> Token:
    """English token fixture."""
    return Token("English")


@pytest.fixture
def token_alice() -> UserToken:
    """Alice user token fixture."""
    return UserToken("Alice")


@pytest.fixture
def token_cat() -> Token:
    """Cat token fixture."""
    return Token("Cat")


@pytest.fixture
def token_tree() -> Token:
    """Tree token fixture."""
    return Token("Tree", desc="Perched in a tree, surrounded by a dense fog where nothing can be seen past a few feet, the Cheshire Cat sits smiling on a branch.")


@pytest.fixture
def token_talk() -> Token:
    """Talk token fixture."""
    return Token("Talk")


@pytest.fixture
def token_continue() -> Token:
    """Continue token fixture."""
    return Token("Continue")


@pytest.fixture
def token_sentence_length() -> NumToken:
    """Sentence length numeric token fixture."""
    return NumToken("SentenceLength", min_value=1, max_value=20, desc="The number of words in the sentence, between 1 and 20.")


@pytest.fixture
def token_coordinates() -> NumListToken:
    """Coordinates NumList token fixture."""
    return NumListToken("Coordinates", min_value=-100, max_value=100, length=3, desc="3D coordinates (x, y, z)")


@pytest.fixture
def token_scores() -> NumListToken:
    """Scores NumList token fixture."""
    return NumListToken("Scores", min_value=0, max_value=10, length=5, desc="A list of 5 scores between 0 and 10")


# Additional token fixtures for comprehensive testing
@pytest.fixture
def token_result() -> Token:
    """Result token fixture."""
    return Token("Result")


@pytest.fixture
def token_end() -> Token:
    """End token fixture."""
    return Token("End")


@pytest.fixture
def token_final() -> Token:
    """Final token fixture."""
    return Token("Final")


@pytest.fixture
def token_disappear() -> Token:
    """Disappear token fixture."""
    return Token("Disappear")


@pytest.fixture
def token_grin() -> Token:
    """Grin token fixture."""
    return Token("Grin")


@pytest.fixture
def token_ponder() -> Token:
    """Ponder token fixture."""
    return Token("Ponder")


@pytest.fixture
def user_token_user() -> UserToken:
    """User token fixture."""
    return UserToken("User")


@pytest.fixture
def num_token_count() -> NumToken:
    """Count numeric token fixture."""
    return NumToken("Count", min_value=1, max_value=10, desc="Count token")


@pytest.fixture
def num_token_scores() -> NumToken:
    """Scores numeric token fixture."""
    return NumToken("Scores", min_value=0, max_value=100, desc="Scores token")


@pytest.fixture
def numlist_token_scores() -> NumListToken:
    """Scores NumList token fixture."""
    return NumListToken("Scores", min_value=0, max_value=100, length=3, desc="Scores list token")


# Test tokens for various test scenarios
@pytest.fixture
def token_test() -> Token:
    """Basic test token fixture."""
    return Token("Test", desc="A test token")


@pytest.fixture
def token_test1() -> Token:
    """Test1 token fixture."""
    return Token("Test1")


@pytest.fixture
def token_test2() -> Token:
    """Test2 token fixture."""
    return Token("Test2")


@pytest.fixture
def token_test3() -> Token:
    """Test3 token fixture."""
    return Token("Test3")


@pytest.fixture
def token_token1() -> Token:
    """Token1 fixture."""
    return Token("Token1")


@pytest.fixture
def token_token2() -> Token:
    """Token2 fixture."""
    return Token("Token2")


@pytest.fixture
def token_token3() -> Token:
    """Token3 fixture."""
    return Token("Token3")


@pytest.fixture
def token_basic() -> Token:
    """Basic token fixture."""
    return Token("Basic")


@pytest.fixture
def token_visible() -> Token:
    """Visible token fixture."""
    return Token("Visible")


@pytest.fixture
def token_public() -> Token:
    """Public token fixture."""
    return Token("Public")


@pytest.fixture
def token_secret() -> Token:
    """Secret token fixture."""
    return Token("Secret")


@pytest.fixture
def token_hidden() -> Token:
    """Hidden token fixture."""
    return Token("Hidden")


@pytest.fixture
def token_assistant() -> Token:
    """Assistant token fixture."""
    return Token("Assistant")


@pytest.fixture
def token_question() -> Token:
    """Question token fixture."""
    return Token("Question")


@pytest.fixture
def token_answer() -> Token:
    """Answer token fixture."""
    return Token("Answer")


# Tokens for specific test scenarios
@pytest.fixture
def token_unicode() -> Token:
    """Unicode token fixture."""
    return Token("Unicode", desc="Unicode description with émojis")


@pytest.fixture
def token_long_desc() -> Token:
    """Token with long description fixture."""
    long_desc = "A token with a very long description that explains its purpose in detail and provides comprehensive context for testing purposes."
    return Token("LongDesc", desc=long_desc)


@pytest.fixture
def token_no_key() -> Token:
    """Token without key fixture."""
    return Token("NoKey", key=None, desc="A token without key")


@pytest.fixture
def token_no_desc() -> Token:
    """Token without description fixture."""
    return Token("NoDesc")


@pytest.fixture
def token_minimal() -> Token:
    """Minimal token fixture."""
    return Token("Minimal")


@pytest.fixture
def token_emoji_key() -> Token:
    """Token with emoji key fixture."""
    return Token("Emoji", desc="A token with emoji key")


@pytest.fixture
def token_alphanumeric_key() -> Token:
    """Token with alphanumeric key fixture."""
    return Token("Alpha", key="abc123", desc="A token with alphanumeric key")


@pytest.fixture
def token_underscore_key() -> Token:
    """Token with underscore key fixture."""
    return Token("Underscore", key="test_key", desc="A token with underscore key")


@pytest.fixture
def token_special_chars() -> Token:
    """Token with special characters fixture."""
    return Token("Special", key="test@key", desc="A token with special characters in key")


@pytest.fixture
def token_numeric_range() -> NumToken:
    """Token with wide numeric range fixture."""
    return NumToken("Range", min_value=0, max_value=100, desc="A token with wide numeric range")


@pytest.fixture
def token_single_value() -> NumToken:
    """Token with single numeric value fixture."""
    return NumToken("Single", min_value=5, max_value=5, desc="A token with single numeric value")


# Tokens for protocol workflow tests
@pytest.fixture
def token_workflow_tree() -> Token:
    """Tree token for workflow tests."""
    return Token("Tree")


@pytest.fixture
def token_workflow_english() -> Token:
    """English token for workflow tests."""
    return Token("English")


@pytest.fixture
def token_workflow_cat() -> Token:
    """Cat token for workflow tests."""
    return Token("Cat")


@pytest.fixture
def token_workflow_talk() -> Token:
    """Talk token for workflow tests."""
    return Token("Talk")


@pytest.fixture
def token_workflow_result() -> Token:
    """Result token for workflow tests."""
    return Token("Result")


@pytest.fixture
def token_workflow_end() -> Token:
    """End token for workflow tests."""
    return Token("End")


@pytest.fixture
def token_workflow_count() -> NumToken:
    """Count token for workflow tests."""
    return NumToken("Count", min_value=1, max_value=10)


@pytest.fixture
def token_workflow_coordinates() -> NumListToken:
    """Coordinates token for workflow tests."""
    return NumListToken("Position", min_value=-100, max_value=100, length=3)


@pytest.fixture
def token_workflow_scores() -> NumListToken:
    """Scores token for workflow tests."""
    return NumListToken("Scores", min_value=0, max_value=100, length=3)


@pytest.fixture
def user_token_workflow() -> UserToken:
    """User token for workflow tests."""
    return UserToken("User")


# Legacy token constants for backward compatibility
TOKEN_ENGLISH = Token("English")
TOKEN_ALICE = UserToken("Alice")
TOKEN_CAT = Token("Cat")
TOKEN_TREE = Token("Tree", desc="Perched in a tree, surrounded by a dense fog where nothing can be seen past a few feet, the Cheshire Cat sits smiling on a branch.")
TOKEN_TALK = Token("Talk")
TOKEN_CONTINUE = Token("Continue")
TOKEN_RESULT = Token("Result")
TOKEN_SENTENCE_LENGTH = NumToken("SentenceLength", min_value=1, max_value=20, desc="The number of words in the sentence, between 1 and 20.")
TOKEN_COORDINATES = NumListToken("Coordinates", min_value=-100, max_value=100, length=3, desc="3D coordinates (x, y, z)")
TOKEN_SCORES = NumListToken("Scores", min_value=0, max_value=10, length=5, desc="A list of 5 scores between 0 and 10")

# Create the token sets for the instructions
SIMPLE_TOKENSET = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK))
SIMPLE_NUMTOKEN_TOKENSET = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_SENTENCE_LENGTH)) # NumToken
SIMPLE_NUMLISTTOKEN_TOKENSET = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_COORDINATES)) # NumListToken
SIMPLE_NUMTOKEN_NUMLISTTOKEN_TOKENSET = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_SENTENCE_LENGTH, TOKEN_COORDINATES)) # Both NumToken and NumListToken

USER_TOKENSET = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK))
USER_NUMTOKEN_TOKENSET = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_SENTENCE_LENGTH)) # NumToken
USER_NUMLILSTTOKEN_TOKENSET = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_COORDINATES)) # NumListToken
USER_NUMTOKEN_NUMLISTTOKEN_TOKENSET = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_SENTENCE_LENGTH, TOKEN_COORDINATES)) # Both NumToken and NumListToken


def get_valid_keyless_tokens() -> Dict[str, Union[Token, UserToken, NumToken, NumListToken]]:
    """Get a collection of valid keyless tokens for testing."""
    return {
        'basic': Token("Basic", desc="A basic token"),
        'user': UserToken("User", desc="A user token"),
        'numeric': NumToken("Count", min_value=1, max_value=10, desc="A numeric token"),
        'num_list': NumListToken("Numbers", desc="A numeric list token", min_value=1, max_value=5, length=3),
        'with_desc': Token("Described", desc="A token with description"),
        'emoji_key': Token("Emoji", desc="A token with emoji key"),
        'alphanumeric_key': Token("Alpha", desc="A token with alphanumeric key"),
        'underscore_key': Token("Underscore", desc="A token with underscore key"),
        'no_key': Token("NoKey", desc="A token without key"),
        'no_desc': Token("NoDesc"),
        'minimal': Token("Minimal"),
        'long_desc': Token("LongDesc", desc="A token with a very long description that explains its purpose in detail"),
        'special_chars': Token("Special", desc="A token with special characters in key"),
        'unicode': Token("Unicode", desc="A token with unicode characters"),
        'numeric_range': NumToken("Range", min_value=0, max_value=100, desc="A token with wide numeric range"),
        'single_value': NumToken("Single", min_value=5, max_value=5, desc="A token with single numeric value")
    }


def get_invalid_tokens() -> Dict[str, Tuple[Any, ...]]:
    """Get a collection of invalid token configurations for testing."""
    return {
        'invalid_char_value': ("Test@", "key", "Invalid character in value"),
        'invalid_char_key': ("Test", "Key#", "Invalid character in key"),
        'empty_value': ("", "key", "Empty value"),
        'none_value': (None, "key", "None value"),
        'invalid_emoji_key': ("Test", "invalid_emoji", "Invalid emoji in key"),
        'numeric_invalid_range': ("Count", "key", "Invalid numeric range", 10, 5),  # min > max
        'numeric_negative_min': ("Count", "key", "Negative minimum value", -1, 10),
        'numeric_zero_max': ("Count", "key", "Zero maximum value", 1, 0)
    }


def get_token_equality_pairs() -> List[Tuple[Union[Token, UserToken, NumToken], Union[Token, UserToken, NumToken], bool]]:
    """Get pairs of tokens for testing equality."""
    return [
        (Token("Same"), Token("Same"), True),
        (Token("Different"), Token("Same"), False),
        (UserToken("User"), UserToken("User"), True),
        (UserToken("User"), Token("User"), False),  # Different types
        (NumToken("Count", min_value=1, max_value=10), NumToken("Count", min_value=1, max_value=10), True),
        (NumToken("Count", min_value=1, max_value=10), NumToken("Count", min_value=1, max_value=5), False),
    ]


def get_token_hash_pairs() -> List[Tuple[Union[Token, UserToken, NumToken], Union[Token, UserToken, NumToken], bool]]:
    """Get pairs of tokens for testing hashing."""
    return [
        (Token("HashTest"), Token("HashTest"), True),  # Same hash
        (Token("HashTest1"), Token("HashTest2"), False),  # Different hash
        (UserToken("UserHash"), UserToken("UserHash"), True),
        (NumToken("NumHash", min_value=1, max_value=10), NumToken("NumHash", min_value=1, max_value=10), True),
    ]


def get_token_serialization_data() -> Dict[str, Dict[str, Any]]:
    """Get token data for testing serialization."""
    return {
        'basic_token': {
            'token': Token("Serial", desc="Serialization test"),
            'expected_dict': {
                'value': 'Serial_',
                'key': 'Serial_',
                'user': False,
                'num': 0,
                'desc': 'Serialization test',
                'special': None
            }
        },
        'user_token': {
            'token': UserToken("UserSerial", desc="User serialization test"),
            'expected_dict': {
                'value': 'UserSerial_',
                'key': 'Serial_',
                'user': True,
                'num': 0,
                'desc': 'User serialization test',
                'special': None
            }
        },
        'numeric_token': {
            'token': NumToken("NumSerial", min_value=1, max_value=10, desc="Numeric serialization test"),
            'expected_dict': {
                'value': 'NumSerial_',
                'key': 'Serial_',
                'user': False,
                'num': 1,
                'desc': 'Numeric serialization test',
                'special': None
            }
        }
    }
