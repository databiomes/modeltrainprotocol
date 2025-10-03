"""
Instruction fixtures for testing.
All instructions are created using TokenSet and Sample fixtures.
"""
from typing import Dict, Any

import pytest

from model_train_protocol import SimpleInstruction, UserInstruction
from model_train_protocol.common.tokens.NumListToken import NumListToken
from model_train_protocol.common.tokens.NumToken import NumToken
from model_train_protocol.common.tokens.Token import Token
from model_train_protocol.common.tokens.UserToken import UserToken

# Basic tokens for creating instructions
TOKEN_TREE = Token("Tree", desc="A tree token")
TOKEN_ENGLISH = Token("English", desc="English language token")
TOKEN_CAT = Token("Cat", desc="A cat token")
TOKEN_TALK = Token("Talk", desc="A talk token")
TOKEN_COORDINATES = Token("Coordinates", desc="Coordinates token")
TOKEN_RESULT = Token("Result", desc="Result token")
TOKEN_END = Token("End", desc="End token")

# Numeric tokens
TOKEN_COUNT = NumToken("Count", min_value=1, max_value=100, desc="Count token")
TOKEN_SCORES = NumListToken("Scores", min_value=0, max_value=10, length=5, desc="Scores token")

# User tokens
TOKEN_USER = UserToken("User", desc="User token")


def get_basic_instructions() -> Dict[str, Any]:
    """Get basic instructions created using basic tokensets."""
    from tests.fixtures.tokensets import (
        simple_tokenset, user_tokenset, result_tokenset, user_result_tokenset
    )
    
    return {
        'simple_instruction': SimpleInstruction(
            context=[simple_tokenset],
            response=simple_tokenset,
            final=TOKEN_RESULT
        ),
        'user_instruction': UserInstruction(
            context=[simple_tokenset],
            user=user_tokenset,
            final=TOKEN_RESULT
        ),
        'result_instruction': SimpleInstruction(
            context=[result_tokenset],
            response=result_tokenset,
            final=TOKEN_END
        ),
        'user_result_instruction': UserInstruction(
            context=[user_tokenset],
            user=user_result_tokenset,
            final=TOKEN_END
        ),
    }


def get_numtoken_instructions() -> Dict[str, Any]:
    """Get instructions created using tokensets with NumToken."""
    from tests.fixtures.tokensets import (
        simple_numtoken_tokenset, user_numtoken_tokenset, 
        result_numtoken_tokenset, user_result_numtoken_tokenset
    )
    
    return {
        'simple_numtoken_instruction': SimpleInstruction(
            context=[simple_numtoken_tokenset],
            response=simple_numtoken_tokenset,
            final=TOKEN_COUNT
        ),
        'user_numtoken_instruction': UserInstruction(
            context=[simple_numtoken_tokenset],
            user=user_numtoken_tokenset,
            final=TOKEN_COUNT
        ),
        'result_numtoken_instruction': SimpleInstruction(
            context=[result_numtoken_tokenset],
            response=result_numtoken_tokenset,
            final=TOKEN_COUNT
        ),
        'user_result_numtoken_instruction': UserInstruction(
            context=[user_numtoken_tokenset],
            user=user_result_numtoken_tokenset,
            final=TOKEN_COUNT
        ),
    }


def get_numlisttoken_instructions() -> Dict[str, Any]:
    """Get instructions created using tokensets with NumListToken."""
    from tests.fixtures.tokensets import (
        simple_numlisttoken_tokenset, user_numlisttoken_tokenset,
        result_numlisttoken_tokenset, user_result_numlisttoken_tokenset,
        scores_tokenset
    )
    
    return {
        'simple_numlisttoken_instruction': SimpleInstruction(
            context=[simple_numlisttoken_tokenset],
            response=simple_numlisttoken_tokenset,
            final=TOKEN_SCORES
        ),
        'user_numlisttoken_instruction': UserInstruction(
            context=[simple_numlisttoken_tokenset],
            user=user_numlisttoken_tokenset,
            final=TOKEN_SCORES
        ),
        'result_numlisttoken_instruction': SimpleInstruction(
            context=[result_numlisttoken_tokenset],
            response=result_numlisttoken_tokenset,
            final=TOKEN_SCORES
        ),
        'user_result_numlisttoken_instruction': UserInstruction(
            context=[user_numlisttoken_tokenset],
            user=user_result_numlisttoken_tokenset,
            final=TOKEN_SCORES
        ),
        'scores_instruction': SimpleInstruction(
            context=[scores_tokenset],
            response=scores_tokenset,
            final=TOKEN_SCORES
        ),
    }


def get_mixed_numeric_instructions() -> Dict[str, Any]:
    """Get instructions created using tokensets with both NumToken and NumListToken."""
    from tests.fixtures.tokensets import (
        simple_mixed_tokenset, user_mixed_tokenset,
        result_mixed_tokenset, user_result_mixed_tokenset
    )
    
    return {
        'simple_mixed_instruction': SimpleInstruction(
            context=[simple_mixed_tokenset],
            response=simple_mixed_tokenset,
            final=TOKEN_COUNT
        ),
        'user_mixed_instruction': UserInstruction(
            context=[simple_mixed_tokenset],
            user=user_mixed_tokenset,
            final=TOKEN_COUNT
        ),
        'result_mixed_instruction': SimpleInstruction(
            context=[result_mixed_tokenset],
            response=result_mixed_tokenset,
            final=TOKEN_COUNT
        ),
        'user_result_mixed_instruction': UserInstruction(
            context=[user_mixed_tokenset],
            user=user_result_mixed_tokenset,
            final=TOKEN_COUNT
        ),
    }


def get_all_instructions() -> Dict[str, Any]:
    """Get all instructions for comprehensive testing."""
    all_instructions = {}
    all_instructions.update(get_basic_instructions())
    all_instructions.update(get_numtoken_instructions())
    all_instructions.update(get_numlisttoken_instructions())
    all_instructions.update(get_mixed_numeric_instructions())
    return all_instructions


def get_instructions_by_type() -> Dict[str, Dict[str, Any]]:
    """Get instructions organized by type for easier testing."""
    return {
        'basic': get_basic_instructions(),
        'numtoken': get_numtoken_instructions(),
        'numlisttoken': get_numlisttoken_instructions(),
        'mixed': get_mixed_numeric_instructions(),
    }


# Individual pytest fixtures for each Instruction

# Basic instructions
@pytest.fixture
def simple_instruction(simple_tokenset) -> SimpleInstruction:
    """Basic simple instruction."""
    return SimpleInstruction(
        context=[simple_tokenset],
        response=simple_tokenset,
        final=TOKEN_RESULT
    )


@pytest.fixture
def user_instruction(simple_tokenset, user_tokenset) -> UserInstruction:
    """Basic user instruction."""
    return UserInstruction(
        context=[simple_tokenset],
        user=user_tokenset,
        final=TOKEN_RESULT
    )


@pytest.fixture
def result_instruction(result_tokenset) -> SimpleInstruction:
    """Result instruction."""
    return SimpleInstruction(
        context=[result_tokenset],
        response=result_tokenset,
        final=TOKEN_END
    )


@pytest.fixture
def user_result_instruction(user_tokenset, user_result_tokenset) -> UserInstruction:
    """User result instruction."""
    return UserInstruction(
        context=[user_tokenset],
        user=user_result_tokenset,
        final=TOKEN_END
    )


# NumToken instructions
@pytest.fixture
def simple_numtoken_instruction(simple_numtoken_tokenset) -> SimpleInstruction:
    """Simple instruction with NumToken."""
    return SimpleInstruction(
        context=[simple_numtoken_tokenset],
        response=simple_numtoken_tokenset,
        final=TOKEN_COUNT
    )


@pytest.fixture
def user_numtoken_instruction(simple_numtoken_tokenset, user_numtoken_tokenset) -> UserInstruction:
    """User instruction with NumToken."""
    return UserInstruction(
        context=[simple_numtoken_tokenset],
        user=user_numtoken_tokenset,
        final=TOKEN_COUNT
    )


@pytest.fixture
def result_numtoken_instruction(result_numtoken_tokenset) -> SimpleInstruction:
    """Result instruction with NumToken."""
    return SimpleInstruction(
        context=[result_numtoken_tokenset],
        response=result_numtoken_tokenset,
        final=TOKEN_COUNT
    )


@pytest.fixture
def user_result_numtoken_instruction(user_numtoken_tokenset, user_result_numtoken_tokenset) -> UserInstruction:
    """User result instruction with NumToken."""
    return UserInstruction(
        context=[user_numtoken_tokenset],
        user=user_result_numtoken_tokenset,
        final=TOKEN_COUNT
    )


# NumListToken instructions
@pytest.fixture
def simple_numlisttoken_instruction(simple_numlisttoken_tokenset) -> SimpleInstruction:
    """Simple instruction with NumListToken."""
    return SimpleInstruction(
        context=[simple_numlisttoken_tokenset],
        response=simple_numlisttoken_tokenset,
        final=TOKEN_SCORES
    )


@pytest.fixture
def user_numlisttoken_instruction(simple_numlisttoken_tokenset, user_numlisttoken_tokenset) -> UserInstruction:
    """User instruction with NumListToken."""
    return UserInstruction(
        context=[simple_numlisttoken_tokenset],
        user=user_numlisttoken_tokenset,
        final=TOKEN_SCORES
    )


@pytest.fixture
def result_numlisttoken_instruction(result_numlisttoken_tokenset) -> SimpleInstruction:
    """Result instruction with NumListToken."""
    return SimpleInstruction(
        context=[result_numlisttoken_tokenset],
        response=result_numlisttoken_tokenset,
        final=TOKEN_SCORES
    )


@pytest.fixture
def user_result_numlisttoken_instruction(user_numlisttoken_tokenset, user_result_numlisttoken_tokenset) -> UserInstruction:
    """User result instruction with NumListToken."""
    return UserInstruction(
        context=[user_numlisttoken_tokenset],
        user=user_result_numlisttoken_tokenset,
        final=TOKEN_SCORES
    )


@pytest.fixture
def scores_instruction(scores_tokenset) -> SimpleInstruction:
    """Scores instruction."""
    return SimpleInstruction(
        context=[scores_tokenset],
        response=scores_tokenset,
        final=TOKEN_SCORES
    )


# Mixed numeric instructions
@pytest.fixture
def simple_mixed_instruction(simple_mixed_tokenset) -> SimpleInstruction:
    """Simple instruction with mixed numeric tokens."""
    return SimpleInstruction(
        context=[simple_mixed_tokenset],
        response=simple_mixed_tokenset,
        final=TOKEN_COUNT
    )


@pytest.fixture
def user_mixed_instruction(simple_mixed_tokenset, user_mixed_tokenset) -> UserInstruction:
    """User instruction with mixed numeric tokens."""
    return UserInstruction(
        context=[simple_mixed_tokenset],
        user=user_mixed_tokenset,
        final=TOKEN_COUNT
    )


@pytest.fixture
def result_mixed_instruction(result_mixed_tokenset) -> SimpleInstruction:
    """Result instruction with mixed numeric tokens."""
    return SimpleInstruction(
        context=[result_mixed_tokenset],
        response=result_mixed_tokenset,
        final=TOKEN_COUNT
    )


@pytest.fixture
def user_result_mixed_instruction(user_mixed_tokenset, user_result_mixed_tokenset) -> UserInstruction:
    """User result instruction with mixed numeric tokens."""
    return UserInstruction(
        context=[user_mixed_tokenset],
        user=user_result_mixed_tokenset,
        final=TOKEN_COUNT
    )


# Instruction fixtures with samples
@pytest.fixture
def simple_instruction_with_samples(
    simple_instruction,
    simple_context_sample,
    simple_response_sample
) -> SimpleInstruction:
    """Simple instruction with samples added."""
    # Add samples to the instruction - only use samples that match the instruction's TokenSet
    simple_instruction.add_sample(
        context_snippets=[simple_context_sample],
        output_snippet=simple_response_sample,
        value=None
    )
    simple_instruction.add_sample(
        context_snippets=[simple_context_sample],
        output_snippet=simple_response_sample,
        value=None
    )
    simple_instruction.add_sample(
        context_snippets=[simple_context_sample],
        output_snippet=simple_response_sample,
        value=None
    )
    return simple_instruction


@pytest.fixture
def user_instruction_with_samples(
    user_instruction,
    simple_context_sample,
    user_response_sample
) -> UserInstruction:
    """User instruction with samples added."""
    # Add samples to the instruction - only use samples that match the instruction's TokenSet
    # For UserInstruction, the output snippet should match the user TokenSet
    user_instruction.add_sample(
        context_snippets=[simple_context_sample],
        prompt="What should I do?",
        output_snippet=user_response_sample,
        value=None
    )
    user_instruction.add_sample(
        context_snippets=[simple_context_sample],
        prompt="How can I help?",
        output_snippet=user_response_sample,
        value=None
    )
    user_instruction.add_sample(
        context_snippets=[simple_context_sample],
        prompt="What's the next step?",
        output_snippet=user_response_sample,
        value=None
    )
    return user_instruction


@pytest.fixture
def numtoken_instruction_with_samples(
    simple_numtoken_instruction,
    simple_numtoken_context_sample,
    simple_numtoken_response_sample
) -> SimpleInstruction:
    """NumToken instruction with samples added."""
    # Add samples to the instruction - only use samples that match the instruction's TokenSet
    simple_numtoken_instruction.add_sample(
        context_snippets=[simple_numtoken_context_sample],
        output_snippet=simple_numtoken_response_sample,
        value=10
    )
    simple_numtoken_instruction.add_sample(
        context_snippets=[simple_numtoken_context_sample],
        output_snippet=simple_numtoken_response_sample,
        value=15
    )
    simple_numtoken_instruction.add_sample(
        context_snippets=[simple_numtoken_context_sample],
        output_snippet=simple_numtoken_response_sample,
        value=25
    )
    return simple_numtoken_instruction


@pytest.fixture
def numlisttoken_instruction_with_samples(
    simple_numlisttoken_instruction,
    simple_numlisttoken_context_sample,
    simple_numlisttoken_response_sample
) -> SimpleInstruction:
    """NumListToken instruction with samples added."""
    # Add samples to the instruction - only use samples that match the instruction's TokenSet
    # Note: The final token is a NumListToken, so value should be a number, not a list
    simple_numlisttoken_instruction.add_sample(
        context_snippets=[simple_numlisttoken_context_sample],
        output_snippet=simple_numlisttoken_response_sample,
        value=10
    )
    simple_numlisttoken_instruction.add_sample(
        context_snippets=[simple_numlisttoken_context_sample],
        output_snippet=simple_numlisttoken_response_sample,
        value=15
    )
    simple_numlisttoken_instruction.add_sample(
        context_snippets=[simple_numlisttoken_context_sample],
        output_snippet=simple_numlisttoken_response_sample,
        value=25
    )
    return simple_numlisttoken_instruction


@pytest.fixture
def mixed_instruction_with_samples(
    simple_mixed_instruction,
    simple_mixed_context_sample,
    simple_mixed_response_sample
) -> SimpleInstruction:
    """Mixed numeric instruction with samples added."""
    # Add samples to the instruction - only use samples that match the instruction's TokenSet
    simple_mixed_instruction.add_sample(
        context_snippets=[simple_mixed_context_sample],
        output_snippet=simple_mixed_response_sample,
        value=42.5
    )
    simple_mixed_instruction.add_sample(
        context_snippets=[simple_mixed_context_sample],
        output_snippet=simple_mixed_response_sample,
        value=37.2
    )
    simple_mixed_instruction.add_sample(
        context_snippets=[simple_mixed_context_sample],
        output_snippet=simple_mixed_response_sample,
        value=79.7
    )
    return simple_mixed_instruction


@pytest.fixture
def user_mixed_instruction_with_samples(
    user_mixed_instruction,
    simple_mixed_context_sample,
    user_mixed_response_sample
) -> UserInstruction:
    """User mixed instruction with samples added."""
    # Add samples to the instruction - only use samples that match the instruction's TokenSet
    # For UserInstruction, the output snippet should match the user TokenSet
    user_mixed_instruction.add_sample(
        context_snippets=[simple_mixed_context_sample],
        prompt="Generate mixed data",
        output_snippet=user_mixed_response_sample,
        value=42.5
    )
    user_mixed_instruction.add_sample(
        context_snippets=[simple_mixed_context_sample],
        prompt="What are the coordinates?",
        output_snippet=user_mixed_response_sample,
        value=37.2
    )
    user_mixed_instruction.add_sample(
        context_snippets=[simple_mixed_context_sample],
        prompt="Calculate the result",
        output_snippet=user_mixed_response_sample,
        value=79.7
    )
    return user_mixed_instruction
