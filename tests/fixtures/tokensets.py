"""
TokenSet fixtures for testing.
"""
from typing import Dict

import pytest

from model_train_protocol import TokenSet


def get_basic_tokensets(token_tree, token_english, token_cat, token_talk, token_alice, token_result) -> Dict[str, TokenSet]:
    """Get basic tokensets without numeric tokens."""
    return {
        'simple_tokenset': TokenSet(tokens=(token_tree, token_english, token_cat, token_talk)),
        'user_tokenset': TokenSet(tokens=(token_tree, token_english, token_alice, token_talk)),
        'result_tokenset': TokenSet(tokens=(token_tree, token_english, token_cat, token_talk, token_result)),
        'user_result_tokenset': TokenSet(tokens=(token_tree, token_english, token_alice, token_talk, token_result)),
    }


def get_numtoken_tokensets(token_tree, token_english, token_cat, token_talk, token_alice, token_result, token_sentence_length) -> Dict[str, TokenSet]:
    """Get tokensets with NumToken."""
    return {
        'simple_numtoken_tokenset': TokenSet(tokens=(token_tree, token_english, token_cat, token_talk, token_sentence_length)),
        'user_numtoken_tokenset': TokenSet(tokens=(token_tree, token_english, token_alice, token_talk, token_sentence_length)),
        'result_numtoken_tokenset': TokenSet(tokens=(token_tree, token_english, token_cat, token_talk, token_result, token_sentence_length)),
        'user_result_numtoken_tokenset': TokenSet(tokens=(token_tree, token_english, token_alice, token_talk, token_result, token_sentence_length)),
    }


def get_numlisttoken_tokensets(token_tree, token_english, token_cat, token_talk, token_alice, token_result, token_coordinates, token_scores) -> Dict[str, TokenSet]:
    """Get tokensets with NumListToken."""
    return {
        'simple_numlisttoken_tokenset': TokenSet(tokens=(token_tree, token_english, token_cat, token_talk, token_coordinates)),
        'user_numlisttoken_tokenset': TokenSet(tokens=(token_tree, token_english, token_alice, token_talk, token_coordinates)),
        'result_numlisttoken_tokenset': TokenSet(tokens=(token_tree, token_english, token_cat, token_talk, token_result, token_coordinates)),
        'user_result_numlisttoken_tokenset': TokenSet(tokens=(token_tree, token_english, token_alice, token_talk, token_result, token_coordinates)),
        'scores_tokenset': TokenSet(tokens=(token_tree, token_english, token_cat, token_talk, token_scores)),
    }


def get_mixed_numeric_tokensets(token_tree, token_english, token_cat, token_talk, token_alice, token_result, token_sentence_length, token_coordinates) -> Dict[str, TokenSet]:
    """Get tokensets with both NumToken and NumListToken."""
    return {
        'simple_mixed_tokenset': TokenSet(tokens=(token_tree, token_english, token_cat, token_talk, token_sentence_length, token_coordinates)),
        'user_mixed_tokenset': TokenSet(tokens=(token_tree, token_english, token_alice, token_talk, token_sentence_length, token_coordinates)),
        'result_mixed_tokenset': TokenSet(tokens=(token_tree, token_english, token_cat, token_talk, token_result, token_sentence_length, token_coordinates)),
        'user_result_mixed_tokenset': TokenSet(tokens=(token_tree, token_english, token_alice, token_talk, token_result, token_sentence_length, token_coordinates)),
    }


def get_all_tokensets(token_tree, token_english, token_cat, token_talk, token_alice, token_result, token_sentence_length, token_coordinates, token_scores) -> Dict[str, TokenSet]:
    """Get all tokensets for comprehensive testing."""
    all_tokensets = {}
    all_tokensets.update(get_basic_tokensets(token_tree, token_english, token_cat, token_talk, token_alice, token_result))
    all_tokensets.update(get_numtoken_tokensets(token_tree, token_english, token_cat, token_talk, token_alice, token_result, token_sentence_length))
    all_tokensets.update(get_numlisttoken_tokensets(token_tree, token_english, token_cat, token_talk, token_alice, token_result, token_coordinates, token_scores))
    all_tokensets.update(get_mixed_numeric_tokensets(token_tree, token_english, token_cat, token_talk, token_alice, token_result, token_sentence_length, token_coordinates))
    return all_tokensets


def get_tokensets_by_type(token_tree, token_english, token_cat, token_talk, token_alice, token_result, token_sentence_length, token_coordinates, token_scores) -> Dict[str, Dict[str, TokenSet]]:
    """Get tokensets organized by type for easier testing."""
    return {
        'basic': get_basic_tokensets(token_tree, token_english, token_cat, token_talk, token_alice, token_result),
        'numtoken': get_numtoken_tokensets(token_tree, token_english, token_cat, token_talk, token_alice, token_result, token_sentence_length),
        'numlisttoken': get_numlisttoken_tokensets(token_tree, token_english, token_cat, token_talk, token_alice, token_result, token_coordinates, token_scores),
        'mixed': get_mixed_numeric_tokensets(token_tree, token_english, token_cat, token_talk, token_alice, token_result, token_sentence_length, token_coordinates),
    }


# Individual pytest fixtures for each TokenSet

# Basic tokensets
@pytest.fixture
def simple_tokenset(token_tree, token_english, token_cat, token_talk) -> TokenSet:
    """Basic tokenset with Tree, English, Cat, Talk tokens."""
    return TokenSet(tokens=(token_tree, token_english, token_cat, token_talk))


@pytest.fixture
def user_tokenset(token_tree, token_english, token_alice, token_talk) -> TokenSet:
    """User tokenset with Tree, English, Alice, Talk tokens."""
    return TokenSet(tokens=(token_tree, token_english, token_alice, token_talk))


@pytest.fixture
def result_tokenset(token_tree, token_english, token_cat, token_talk, token_result) -> TokenSet:
    """Result tokenset with Tree, English, Cat, Talk, Result tokens."""
    return TokenSet(tokens=(token_tree, token_english, token_cat, token_talk, token_result))


@pytest.fixture
def user_result_tokenset(token_tree, token_english, token_alice, token_talk, token_result) -> TokenSet:
    """User result tokenset with Tree, English, Alice, Talk, Result tokens."""
    return TokenSet(tokens=(token_tree, token_english, token_alice, token_talk, token_result))


# NumToken tokensets
@pytest.fixture
def simple_numtoken_tokenset(token_tree, token_english, token_cat, token_talk, token_sentence_length) -> TokenSet:
    """Simple tokenset with NumToken for sentence length."""
    return TokenSet(tokens=(token_tree, token_english, token_cat, token_talk, token_sentence_length))


@pytest.fixture
def user_numtoken_tokenset(token_tree, token_english, token_alice, token_talk, token_sentence_length) -> TokenSet:
    """User tokenset with NumToken for sentence length."""
    return TokenSet(tokens=(token_tree, token_english, token_alice, token_talk, token_sentence_length))


@pytest.fixture
def result_numtoken_tokenset(token_tree, token_english, token_cat, token_talk, token_result, token_sentence_length) -> TokenSet:
    """Result tokenset with NumToken for sentence length."""
    return TokenSet(tokens=(token_tree, token_english, token_cat, token_talk, token_result, token_sentence_length))


@pytest.fixture
def user_result_numtoken_tokenset(token_tree, token_english, token_alice, token_talk, token_result, token_sentence_length) -> TokenSet:
    """User result tokenset with NumToken for sentence length."""
    return TokenSet(tokens=(token_tree, token_english, token_alice, token_talk, token_result, token_sentence_length))


# NumListToken tokensets
@pytest.fixture
def simple_numlisttoken_tokenset(token_tree, token_english, token_cat, token_talk, token_coordinates) -> TokenSet:
    """Simple tokenset with NumListToken for coordinates."""
    return TokenSet(tokens=(token_tree, token_english, token_cat, token_talk, token_coordinates))


@pytest.fixture
def user_numlisttoken_tokenset(token_tree, token_english, token_alice, token_talk, token_coordinates) -> TokenSet:
    """User tokenset with NumListToken for coordinates."""
    return TokenSet(tokens=(token_tree, token_english, token_alice, token_talk, token_coordinates))


@pytest.fixture
def result_numlisttoken_tokenset(token_tree, token_english, token_cat, token_talk, token_result, token_coordinates) -> TokenSet:
    """Result tokenset with NumListToken for coordinates."""
    return TokenSet(tokens=(token_tree, token_english, token_cat, token_talk, token_result, token_coordinates))


@pytest.fixture
def user_result_numlisttoken_tokenset(token_tree, token_english, token_alice, token_talk, token_result, token_coordinates) -> TokenSet:
    """User result tokenset with NumListToken for coordinates."""
    return TokenSet(tokens=(token_tree, token_english, token_alice, token_talk, token_result, token_coordinates))


@pytest.fixture
def scores_tokenset(token_tree, token_english, token_cat, token_talk, token_scores) -> TokenSet:
    """Tokenset with NumListToken for scores."""
    return TokenSet(tokens=(token_tree, token_english, token_cat, token_talk, token_scores))


# Mixed numeric tokensets
@pytest.fixture
def simple_mixed_tokenset(token_tree, token_english, token_cat, token_talk, token_sentence_length, token_coordinates) -> TokenSet:
    """Simple tokenset with both NumToken and NumListToken."""
    return TokenSet(tokens=(token_tree, token_english, token_cat, token_talk, token_sentence_length, token_coordinates))


@pytest.fixture
def user_mixed_tokenset(token_tree, token_english, token_alice, token_talk, token_sentence_length, token_coordinates) -> TokenSet:
    """User tokenset with both NumToken and NumListToken."""
    return TokenSet(tokens=(token_tree, token_english, token_alice, token_talk, token_sentence_length, token_coordinates))


@pytest.fixture
def result_mixed_tokenset(token_tree, token_english, token_cat, token_talk, token_result, token_sentence_length, token_coordinates) -> TokenSet:
    """Result tokenset with both NumToken and NumListToken."""
    return TokenSet(tokens=(token_tree, token_english, token_cat, token_talk, token_result, token_sentence_length, token_coordinates))


@pytest.fixture
def user_result_mixed_tokenset(token_tree, token_english, token_alice, token_talk, token_result, token_sentence_length, token_coordinates) -> TokenSet:
    """User result tokenset with both NumToken and NumListToken."""
    return TokenSet(tokens=(token_tree, token_english, token_alice, token_talk, token_result, token_sentence_length, token_coordinates))
