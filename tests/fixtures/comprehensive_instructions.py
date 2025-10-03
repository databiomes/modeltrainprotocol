"""
Comprehensive instruction fixtures for testing all tokenset combinations.
Tests all possible combinations of tokensets for both SimpleInstruction and UserInstruction.
"""
import pytest

from model_train_protocol import SimpleInstruction, UserInstruction
from model_train_protocol.common.constants import NON_TOKEN
from model_train_protocol.common.tokens.NumListToken import NumListToken
from model_train_protocol.common.tokens.NumToken import NumToken
from model_train_protocol.common.tokens.Token import Token
from model_train_protocol.common.tokens.UserToken import UserToken

# Basic tokens for creating instructions
TOKEN_TREE = Token("Tree", desc="A tree token")
TOKEN_ENGLISH = Token("English", desc="English language token")
TOKEN_CAT = Token("Cat", desc="A cat token")
TOKEN_TALK = Token("Talk", desc="A talk token")
TOKEN_RESULT = Token("Result", desc="Result token")
TOKEN_END = Token("End", desc="End token")

# Numeric tokens
TOKEN_COUNT = NumToken("Count", min_value=1, max_value=100, desc="Count token")
TOKEN_COORDINATES = NumListToken("Coordinates", min_value=-100, max_value=100, length=3, desc="3D coordinates")
TOKEN_SCORES = NumListToken("Scores", min_value=0, max_value=10, length=5, desc="Scores token")

# User tokens
TOKEN_USER = UserToken("User", desc="User token")


# Individual pytest fixtures for comprehensive testing


# Individual instruction fixtures for specific combinations

# Basic SimpleInstruction fixtures
@pytest.fixture
def simple_basic_instruction(simple_tokenset) -> SimpleInstruction:
    """Basic simple instruction."""
    return SimpleInstruction(
        context=[simple_tokenset],
        response=simple_tokenset,
        final=TOKEN_RESULT
    )


@pytest.fixture
def simple_basic_instruction_with_samples(simple_basic_instruction, simple_context_sample, simple_response_sample) -> SimpleInstruction:
    """Basic simple instruction with samples."""
    simple_basic_instruction.add_sample(
        context_snippets=[simple_context_sample],
        output_snippet=simple_response_sample,
        value=None
    )
    return simple_basic_instruction


@pytest.fixture
def simple_numtoken_instruction(simple_numtoken_tokenset) -> SimpleInstruction:
    """Simple instruction with NumToken."""
    return SimpleInstruction(
        context=[simple_numtoken_tokenset],
        response=simple_numtoken_tokenset,
        final=TOKEN_COUNT
    )


@pytest.fixture
def simple_numtoken_instruction_with_samples(simple_numtoken_instruction, simple_numtoken_context_sample, simple_numtoken_response_sample) -> SimpleInstruction:
    """Simple instruction with NumToken and samples."""
    simple_numtoken_instruction.add_sample(
        context_snippets=[simple_numtoken_context_sample],
        output_snippet=simple_numtoken_response_sample,
        value=10
    )
    return simple_numtoken_instruction


@pytest.fixture
def simple_numlisttoken_instruction(simple_numlisttoken_tokenset) -> SimpleInstruction:
    """Simple instruction with NumListToken."""
    return SimpleInstruction(
        context=[simple_numlisttoken_tokenset],
        response=simple_numlisttoken_tokenset,
        final=TOKEN_COORDINATES
    )


@pytest.fixture
def simple_numlisttoken_instruction_with_samples(simple_numlisttoken_instruction, simple_numlisttoken_context_sample, simple_numlisttoken_response_sample) -> SimpleInstruction:
    """Simple instruction with NumListToken and samples."""
    simple_numlisttoken_instruction.add_sample(
        context_snippets=[simple_numlisttoken_context_sample],
        output_snippet=simple_numlisttoken_response_sample,
        value=[10, 20, 30]
    )
    return simple_numlisttoken_instruction


@pytest.fixture
def simple_mixed_instruction(simple_mixed_tokenset) -> SimpleInstruction:
    """Simple instruction with mixed numeric tokens."""
    return SimpleInstruction(
        context=[simple_mixed_tokenset],
        response=simple_mixed_tokenset,
        final=TOKEN_COUNT
    )


@pytest.fixture
def simple_mixed_instruction_with_samples(simple_mixed_instruction, simple_mixed_context_sample, simple_mixed_response_sample) -> SimpleInstruction:
    """Simple instruction with mixed numeric tokens and samples."""
    simple_mixed_instruction.add_sample(
        context_snippets=[simple_mixed_context_sample],
        output_snippet=simple_mixed_response_sample,
        value=25.5
    )
    return simple_mixed_instruction


@pytest.fixture
def simple_scores_instruction(scores_tokenset) -> SimpleInstruction:
    """Simple instruction with scores tokenset."""
    return SimpleInstruction(
        context=[scores_tokenset],
        response=scores_tokenset,
        final=TOKEN_SCORES
    )


@pytest.fixture
def simple_scores_instruction_with_samples(simple_scores_instruction, scores_context_sample, scores_response_sample) -> SimpleInstruction:
    """Simple instruction with scores tokenset and samples."""
    simple_scores_instruction.add_sample(
        context_snippets=[scores_context_sample],
        output_snippet=scores_response_sample,
        value=[8, 9, 7, 10, 6]
    )
    return simple_scores_instruction


# Basic UserInstruction fixtures
@pytest.fixture
def user_basic_instruction(simple_tokenset, user_tokenset) -> UserInstruction:
    """Basic user instruction."""
    return UserInstruction(
        context=[simple_tokenset],
        user=user_tokenset,
        final=TOKEN_RESULT
    )


@pytest.fixture
def user_basic_instruction_with_samples(user_basic_instruction, simple_context_sample, user_response_sample) -> UserInstruction:
    """Basic user instruction with samples."""
    user_basic_instruction.add_sample(
        context_snippets=[simple_context_sample],
        prompt="What should I do?",
        output_snippet=user_response_sample,
        value=None
    )
    return user_basic_instruction


@pytest.fixture
def user_numtoken_instruction(simple_numtoken_tokenset, user_numtoken_tokenset) -> UserInstruction:
    """User instruction with NumToken."""
    return UserInstruction(
        context=[simple_numtoken_tokenset],
        user=user_numtoken_tokenset,
        final=TOKEN_COUNT
    )


@pytest.fixture
def user_numtoken_instruction_with_samples(user_numtoken_instruction, simple_numtoken_context_sample, user_numtoken_response_sample) -> UserInstruction:
    """User instruction with NumToken and samples."""
    user_numtoken_instruction.add_sample(
        context_snippets=[simple_numtoken_context_sample],
        prompt="Count the items",
        output_snippet=user_numtoken_response_sample,
        value=20
    )
    return user_numtoken_instruction


@pytest.fixture
def user_numlisttoken_instruction(simple_numlisttoken_tokenset, user_numlisttoken_tokenset) -> UserInstruction:
    """User instruction with NumListToken."""
    return UserInstruction(
        context=[simple_numlisttoken_tokenset],
        user=user_numlisttoken_tokenset,
        final=TOKEN_COORDINATES
    )


@pytest.fixture
def user_numlisttoken_instruction_with_samples(user_numlisttoken_instruction, simple_numlisttoken_context_sample, user_numlisttoken_response_sample) -> UserInstruction:
    """User instruction with NumListToken and samples."""
    user_numlisttoken_instruction.add_sample(
        context_snippets=[simple_numlisttoken_context_sample],
        prompt="Provide coordinates",
        output_snippet=user_numlisttoken_response_sample,
        value=[5, 15, 25]
    )
    return user_numlisttoken_instruction


@pytest.fixture
def user_mixed_instruction(simple_mixed_tokenset, user_mixed_tokenset) -> UserInstruction:
    """User instruction with mixed numeric tokens."""
    return UserInstruction(
        context=[simple_mixed_tokenset],
        user=user_mixed_tokenset,
        final=TOKEN_COUNT
    )


@pytest.fixture
def user_mixed_instruction_with_samples(user_mixed_instruction, simple_mixed_context_sample, user_mixed_response_sample) -> UserInstruction:
    """User instruction with mixed numeric tokens and samples."""
    user_mixed_instruction.add_sample(
        context_snippets=[simple_mixed_context_sample],
        prompt="Generate mixed data",
        output_snippet=user_mixed_response_sample,
        value=35.5
    )
    return user_mixed_instruction


@pytest.fixture
def user_scores_instruction(scores_tokenset, user_tokenset) -> UserInstruction:
    """User instruction with scores tokenset."""
    return UserInstruction(
        context=[scores_tokenset],
        user=user_tokenset,
        final=TOKEN_SCORES
    )


@pytest.fixture
def user_scores_instruction_with_samples(user_scores_instruction, scores_context_sample, user_response_sample) -> UserInstruction:
    """User instruction with scores tokenset and samples."""
    user_scores_instruction.add_sample(
        context_snippets=[scores_context_sample],
        prompt="Rate the performance",
        output_snippet=user_response_sample,
        value=[6.2, 7.5, 8.0, 9.1, 5.4]
    )
    return user_scores_instruction


# Edge case fixtures
@pytest.fixture
def simple_instruction_with_none_final(simple_tokenset) -> SimpleInstruction:
    """Simple instruction with NON_TOKEN final token."""
    return SimpleInstruction(
        context=[simple_tokenset],
        response=simple_tokenset,
        final=NON_TOKEN
    )


@pytest.fixture
def simple_instruction_with_non_token_final(simple_tokenset) -> SimpleInstruction:
    """Simple instruction with NON_TOKEN final."""
    return SimpleInstruction(
        context=[simple_tokenset],
        response=simple_tokenset,
        final=NON_TOKEN
    )


@pytest.fixture
def simple_instruction_with_empty_samples(simple_tokenset) -> SimpleInstruction:
    """Simple instruction with no samples."""
    return SimpleInstruction(
        context=[simple_tokenset],
        response=simple_tokenset,
        final=TOKEN_RESULT
    )


@pytest.fixture
def simple_instruction_with_multiple_samples(simple_tokenset, simple_context_sample, simple_response_sample) -> SimpleInstruction:
    """Simple instruction with multiple samples."""
    instruction = SimpleInstruction(
        context=[simple_tokenset],
        response=simple_tokenset,
        final=TOKEN_RESULT
    )
    
    # Add multiple samples
    for i in range(3):
        instruction.add_sample(
            context_snippets=[simple_context_sample],
            output_snippet=simple_response_sample,
            value=None
        )
    
    return instruction


@pytest.fixture
def user_instruction_with_multiple_samples(simple_tokenset, user_tokenset, simple_context_sample, user_response_sample) -> UserInstruction:
    """User instruction with multiple samples."""
    instruction = UserInstruction(
        context=[simple_tokenset],
        user=user_tokenset,
        final=TOKEN_RESULT
    )
    
    # Add multiple samples
    for i in range(3):
        instruction.add_sample(
            context_snippets=[simple_context_sample],
            prompt=f"User prompt {i}",
            output_snippet=user_response_sample,
            value=None
        )
    
    return instruction
