"""
TokenSet fixtures for testing.
"""
import pytest
from typing import Dict, Any
from model_train_protocol import Token, UserToken, NumToken, NumListToken, TokenSet


# Basic tokens for creating tokensets
TOKEN_TREE = Token("Tree", desc="Perched in a tree, surrounded by a dense fog where nothing can be seen past a few feet, the Cheshire Cat sits smiling on a branch.")
TOKEN_ENGLISH = Token("English")
TOKEN_CAT = Token("Cat")
TOKEN_TALK = Token("Talk")
TOKEN_ALICE = UserToken("Alice")
TOKEN_RESULT = Token("Result")
TOKEN_CONTINUE = Token("Continue")

# NumToken for testing
TOKEN_SENTENCE_LENGTH = NumToken("SentenceLength", min_value=1, max_value=20, desc="The number of words in the sentence, between 1 and 20.")

# NumListToken for testing
TOKEN_COORDINATES = NumListToken("Coordinates", min_value=-100, max_value=100, length=3, desc="3D coordinates (x, y, z)")
TOKEN_SCORES = NumListToken("Scores", min_value=0, max_value=10, length=5, desc="A list of 5 scores between 0 and 10")


def get_basic_tokensets() -> Dict[str, TokenSet]:
    """Get basic tokensets without numeric tokens."""
    return {
        'simple_tokenset': TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK)),
        'user_tokenset': TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK)),
        'result_tokenset': TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_RESULT)),
        'user_result_tokenset': TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_RESULT)),
    }


def get_numtoken_tokensets() -> Dict[str, TokenSet]:
    """Get tokensets with NumToken."""
    return {
        'simple_numtoken_tokenset': TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_SENTENCE_LENGTH)),
        'user_numtoken_tokenset': TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_SENTENCE_LENGTH)),
        'result_numtoken_tokenset': TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_RESULT, TOKEN_SENTENCE_LENGTH)),
        'user_result_numtoken_tokenset': TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_RESULT, TOKEN_SENTENCE_LENGTH)),
    }


def get_numlisttoken_tokensets() -> Dict[str, TokenSet]:
    """Get tokensets with NumListToken."""
    return {
        'simple_numlisttoken_tokenset': TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_COORDINATES)),
        'user_numlisttoken_tokenset': TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_COORDINATES)),
        'result_numlisttoken_tokenset': TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_RESULT, TOKEN_COORDINATES)),
        'user_result_numlisttoken_tokenset': TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_RESULT, TOKEN_COORDINATES)),
        'scores_tokenset': TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_SCORES)),
    }


def get_mixed_numeric_tokensets() -> Dict[str, TokenSet]:
    """Get tokensets with both NumToken and NumListToken."""
    return {
        'simple_mixed_tokenset': TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_SENTENCE_LENGTH, TOKEN_COORDINATES)),
        'user_mixed_tokenset': TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_SENTENCE_LENGTH, TOKEN_COORDINATES)),
        'result_mixed_tokenset': TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_RESULT, TOKEN_SENTENCE_LENGTH, TOKEN_COORDINATES)),
        'user_result_mixed_tokenset': TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_RESULT, TOKEN_SENTENCE_LENGTH, TOKEN_COORDINATES)),
    }


def get_all_tokensets() -> Dict[str, TokenSet]:
    """Get all tokensets for comprehensive testing."""
    all_tokensets = {}
    all_tokensets.update(get_basic_tokensets())
    all_tokensets.update(get_numtoken_tokensets())
    all_tokensets.update(get_numlisttoken_tokensets())
    all_tokensets.update(get_mixed_numeric_tokensets())
    return all_tokensets


def get_tokensets_by_type() -> Dict[str, Dict[str, TokenSet]]:
    """Get tokensets organized by type for easier testing."""
    return {
        'basic': get_basic_tokensets(),
        'numtoken': get_numtoken_tokensets(),
        'numlisttoken': get_numlisttoken_tokensets(),
        'mixed': get_mixed_numeric_tokensets(),
    }


# Individual pytest fixtures for each TokenSet

# Basic tokensets
@pytest.fixture
def simple_tokenset() -> TokenSet:
    """Basic tokenset with Tree, English, Cat, Talk tokens."""
    return TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK))


@pytest.fixture
def user_tokenset() -> TokenSet:
    """User tokenset with Tree, English, Alice, Talk tokens."""
    return TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK))


@pytest.fixture
def result_tokenset() -> TokenSet:
    """Result tokenset with Tree, English, Cat, Talk, Result tokens."""
    return TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_RESULT))


@pytest.fixture
def user_result_tokenset() -> TokenSet:
    """User result tokenset with Tree, English, Alice, Talk, Result tokens."""
    return TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_RESULT))


# NumToken tokensets
@pytest.fixture
def simple_numtoken_tokenset() -> TokenSet:
    """Simple tokenset with NumToken for sentence length."""
    return TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_SENTENCE_LENGTH))


@pytest.fixture
def user_numtoken_tokenset() -> TokenSet:
    """User tokenset with NumToken for sentence length."""
    return TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_SENTENCE_LENGTH))


@pytest.fixture
def result_numtoken_tokenset() -> TokenSet:
    """Result tokenset with NumToken for sentence length."""
    return TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_RESULT, TOKEN_SENTENCE_LENGTH))


@pytest.fixture
def user_result_numtoken_tokenset() -> TokenSet:
    """User result tokenset with NumToken for sentence length."""
    return TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_RESULT, TOKEN_SENTENCE_LENGTH))


# NumListToken tokensets
@pytest.fixture
def simple_numlisttoken_tokenset() -> TokenSet:
    """Simple tokenset with NumListToken for coordinates."""
    return TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_COORDINATES))


@pytest.fixture
def user_numlisttoken_tokenset() -> TokenSet:
    """User tokenset with NumListToken for coordinates."""
    return TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_COORDINATES))


@pytest.fixture
def result_numlisttoken_tokenset() -> TokenSet:
    """Result tokenset with NumListToken for coordinates."""
    return TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_RESULT, TOKEN_COORDINATES))


@pytest.fixture
def user_result_numlisttoken_tokenset() -> TokenSet:
    """User result tokenset with NumListToken for coordinates."""
    return TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_RESULT, TOKEN_COORDINATES))


@pytest.fixture
def scores_tokenset() -> TokenSet:
    """Tokenset with NumListToken for scores."""
    return TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_SCORES))


# Mixed numeric tokensets
@pytest.fixture
def simple_mixed_tokenset() -> TokenSet:
    """Simple tokenset with both NumToken and NumListToken."""
    return TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_SENTENCE_LENGTH, TOKEN_COORDINATES))


@pytest.fixture
def user_mixed_tokenset() -> TokenSet:
    """User tokenset with both NumToken and NumListToken."""
    return TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_SENTENCE_LENGTH, TOKEN_COORDINATES))


@pytest.fixture
def result_mixed_tokenset() -> TokenSet:
    """Result tokenset with both NumToken and NumListToken."""
    return TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_RESULT, TOKEN_SENTENCE_LENGTH, TOKEN_COORDINATES))


@pytest.fixture
def user_result_mixed_tokenset() -> TokenSet:
    """User result tokenset with both NumToken and NumListToken."""
    return TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_RESULT, TOKEN_SENTENCE_LENGTH, TOKEN_COORDINATES))
