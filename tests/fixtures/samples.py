"""
Sample fixtures for testing.
All samples are created on tokenset fixtures using create_snippet() method.
"""
from typing import Dict, List, Any

import pytest

from model_train_protocol import Snippet
from tests.fixtures.tokensets import (
    get_basic_tokensets,
    get_numtoken_tokensets,
    get_numlisttoken_tokensets,
    get_mixed_numeric_tokensets
)


def get_basic_samples() -> Dict[str, Any]:
    """Get basic samples created on basic tokensets."""
    tokensets = get_basic_tokensets()
    
    return {
        'simple_context_sample': tokensets['simple_tokenset'].create_snippet(string="The cat sits in the tree"),
        'simple_response_sample': tokensets['simple_tokenset'].create_snippet(string="The cat responds with a grin"),
        'user_context_sample': tokensets['user_tokenset'].create_snippet(string="Alice asks a question"),
        'user_response_sample': tokensets['user_tokenset'].create_snippet(string="Alice receives an answer"),
        'result_context_sample': tokensets['result_tokenset'].create_snippet(string="The conversation continues"),
        'result_response_sample': tokensets['result_tokenset'].create_snippet(string="The result is determined"),
        'user_result_context_sample': tokensets['user_result_tokenset'].create_snippet(string="Alice asks for a result"),
        'user_result_response_sample': tokensets['user_result_tokenset'].create_snippet(string="Alice gets the result"),
    }


def get_numtoken_samples() -> Dict[str, Any]:
    """Get samples created on tokensets with NumToken."""
    tokensets = get_numtoken_tokensets()
    
    return {
        'simple_numtoken_context_sample': tokensets['simple_numtoken_tokenset'].create_snippet(
            string="The cat sits in the tree", numbers=[10]
        ),
        'simple_numtoken_response_sample': tokensets['simple_numtoken_tokenset'].create_snippet(
            string="The cat responds with a grin", numbers=[8]
        ),
        'user_numtoken_context_sample': tokensets['user_numtoken_tokenset'].create_snippet(
            string="Alice asks a question", numbers=[12]
        ),
        'user_numtoken_response_sample': tokensets['user_numtoken_tokenset'].create_snippet(
            string="Alice receives an answer", numbers=[15]
        ),
        'result_numtoken_context_sample': tokensets['result_numtoken_tokenset'].create_snippet(
            string="The conversation continues", numbers=[7]
        ),
        'result_numtoken_response_sample': tokensets['result_numtoken_tokenset'].create_snippet(
            string="The result is determined", numbers=[9]
        ),
        'user_result_numtoken_context_sample': tokensets['user_result_numtoken_tokenset'].create_snippet(
            string="Alice asks for a result", numbers=[11]
        ),
        'user_result_numtoken_response_sample': tokensets['user_result_numtoken_tokenset'].create_snippet(
            string="Alice gets the result", numbers=[13]
        ),
    }


def get_numlisttoken_samples() -> Dict[str, Any]:
    """Get samples created on tokensets with NumListToken."""
    tokensets = get_numlisttoken_tokensets()
    
    return {
        'simple_numlisttoken_context_sample': tokensets['simple_numlisttoken_tokenset'].create_snippet(
            string="The cat sits in the tree", number_lists=[[10, 20, 30]]
        ),
        'simple_numlisttoken_response_sample': tokensets['simple_numlisttoken_tokenset'].create_snippet(
            string="The cat responds with a grin", number_lists=[[5, 15, 25]]
        ),
        'user_numlisttoken_context_sample': tokensets['user_numlisttoken_tokenset'].create_snippet(
            string="Alice asks a question", number_lists=[[1, 2, 3]]
        ),
        'user_numlisttoken_response_sample': tokensets['user_numlisttoken_tokenset'].create_snippet(
            string="Alice receives an answer", number_lists=[[4, 5, 6]]
        ),
        'result_numlisttoken_context_sample': tokensets['result_numlisttoken_tokenset'].create_snippet(
            string="The conversation continues", number_lists=[[7, 8, 9]]
        ),
        'result_numlisttoken_response_sample': tokensets['result_numlisttoken_tokenset'].create_snippet(
            string="The result is determined", number_lists=[[10, 11, 12]]
        ),
        'user_result_numlisttoken_context_sample': tokensets['user_result_numlisttoken_tokenset'].create_snippet(
            string="Alice asks for a result", number_lists=[[13, 14, 15]]
        ),
        'user_result_numlisttoken_response_sample': tokensets['user_result_numlisttoken_tokenset'].create_snippet(
            string="Alice gets the result", number_lists=[[16, 17, 18]]
        ),
        'scores_context_sample': tokensets['scores_tokenset'].create_snippet(
            string="The scores are calculated", number_lists=[[1, 2, 3, 4, 5]]
        ),
        'scores_response_sample': tokensets['scores_tokenset'].create_snippet(
            string="The final scores are ready", number_lists=[[6, 7, 8, 9, 10]]
        ),
    }


def get_mixed_numeric_samples() -> Dict[str, Any]:
    """Get samples created on tokensets with both NumToken and NumListToken."""
    tokensets = get_mixed_numeric_tokensets()
    
    return {
        'simple_mixed_context_sample': tokensets['simple_mixed_tokenset'].create_snippet(
            string="The cat sits in the tree", numbers=[10], number_lists=[[1, 2, 3]]
        ),
        'simple_mixed_response_sample': tokensets['simple_mixed_tokenset'].create_snippet(
            string="The cat responds with a grin", numbers=[8], number_lists=[[4, 5, 6]]
        ),
        'user_mixed_context_sample': tokensets['user_mixed_tokenset'].create_snippet(
            string="Alice asks a question", numbers=[12], number_lists=[[7, 8, 9]]
        ),
        'user_mixed_response_sample': tokensets['user_mixed_tokenset'].create_snippet(
            string="Alice receives an answer", numbers=[15], number_lists=[[10, 11, 12]]
        ),
        'result_mixed_context_sample': tokensets['result_mixed_tokenset'].create_snippet(
            string="The conversation continues", numbers=[7], number_lists=[[13, 14, 15]]
        ),
        'result_mixed_response_sample': tokensets['result_mixed_tokenset'].create_snippet(
            string="The result is determined", numbers=[9], number_lists=[[16, 17, 18]]
        ),
        'user_result_mixed_context_sample': tokensets['user_result_mixed_tokenset'].create_snippet(
            string="Alice asks for a result", numbers=[11], number_lists=[[19, 20, 21]]
        ),
        'user_result_mixed_response_sample': tokensets['user_result_mixed_tokenset'].create_snippet(
            string="Alice gets the result", numbers=[13], number_lists=[[22, 23, 24]]
        ),
    }


def get_all_samples() -> Dict[str, Any]:
    """Get all samples for comprehensive testing."""
    all_samples = {}
    all_samples.update(get_basic_samples())
    all_samples.update(get_numtoken_samples())
    all_samples.update(get_numlisttoken_samples())
    all_samples.update(get_mixed_numeric_samples())
    return all_samples


def get_samples_by_type() -> Dict[str, Dict[str, Any]]:
    """Get samples organized by type for easier testing."""
    return {
        'basic': get_basic_samples(),
        'numtoken': get_numtoken_samples(),
        'numlisttoken': get_numlisttoken_samples(),
        'mixed': get_mixed_numeric_samples(),
    }


def get_sample_combinations() -> Dict[str, List[Any]]:
    """Get combinations of samples for testing different scenarios."""
    samples = get_all_samples()
    
    return {
        'basic_context_response': [
            samples['simple_context_sample'],
            samples['simple_response_sample']
        ],
        'user_context_response': [
            samples['user_context_sample'],
            samples['user_response_sample']
        ],
        'numtoken_context_response': [
            samples['simple_numtoken_context_sample'],
            samples['simple_numtoken_response_sample']
        ],
        'numlisttoken_context_response': [
            samples['simple_numlisttoken_context_sample'],
            samples['simple_numlisttoken_response_sample']
        ],
        'mixed_context_response': [
            samples['simple_mixed_context_sample'],
            samples['simple_mixed_response_sample']
        ],
        'user_numtoken_context_response': [
            samples['user_numtoken_context_sample'],
            samples['user_numtoken_response_sample']
        ],
        'user_numlisttoken_context_response': [
            samples['user_numlisttoken_context_sample'],
            samples['user_numlisttoken_response_sample']
        ],
        'user_mixed_context_response': [
            samples['user_mixed_context_sample'],
            samples['user_mixed_response_sample']
        ],
    }


def get_test_scenarios() -> Dict[str, Dict[str, Any]]:
    """Get complete test scenarios with context, response, and metadata."""
    samples = get_all_samples()
    
    return {
        'basic_scenario': {
            'context_samples': [samples['simple_context_sample']],
            'response_sample': samples['simple_response_sample'],
            'prompt': None,
            'numbers': [[1, 2, 3]],
            'value': None
        },
        'user_scenario': {
            'context_samples': [samples['user_context_sample']],
            'response_sample': samples['user_response_sample'],
            'prompt': "What should I do?",
            'numbers': [[4, 5, 6]],
            'value': None
        },
        'numtoken_scenario': {
            'context_samples': [samples['simple_numtoken_context_sample']],
            'response_sample': samples['simple_numtoken_response_sample'],
            'prompt': None,
            'numbers': [[7], [8]],
            'value': 42
        },
        'numlisttoken_scenario': {
            'context_samples': [samples['simple_numlisttoken_context_sample']],
            'response_sample': samples['simple_numlisttoken_response_sample'],
            'prompt': None,
            'numbers': [[9, 10, 11], [12, 13, 14]],
            'value': [15, 16, 17]
        },
        'mixed_scenario': {
            'context_samples': [samples['simple_mixed_context_sample']],
            'response_sample': samples['simple_mixed_response_sample'],
            'prompt': "Generate mixed data",
            'numbers': [[18, [19, 20, 21]], [22, [23, 24, 25]]],
            'value': 26.5
        },
        'user_mixed_scenario': {
            'context_samples': [samples['user_mixed_context_sample']],
            'response_sample': samples['user_mixed_response_sample'],
            'prompt': "What are the coordinates?",
            'numbers': [[27, [28, 29, 30]], [31, [32, 33, 34]]],
            'value': [35, 36, 37]
        }
    }


# Individual pytest fixtures for each Snippet

# Basic samples
@pytest.fixture
def simple_context_sample(simple_tokenset) -> Snippet:
    """Basic context sample created on simple tokenset."""
    return simple_tokenset.create_snippet(string="The cat sits in the tree")


@pytest.fixture
def simple_response_sample(simple_tokenset) -> Snippet:
    """Basic response sample created on simple tokenset."""
    return simple_tokenset.create_snippet(string="The cat responds with a grin")


@pytest.fixture
def user_context_sample(user_tokenset) -> Snippet:
    """User context sample created on user tokenset."""
    return user_tokenset.create_snippet(string="Alice asks a question")


@pytest.fixture
def user_response_sample(user_tokenset) -> Snippet:
    """User response sample created on user tokenset."""
    return user_tokenset.create_snippet(string="Alice receives an answer")


@pytest.fixture
def result_context_sample(result_tokenset) -> Snippet:
    """Result context sample created on result tokenset."""
    return result_tokenset.create_snippet(string="The conversation continues")


@pytest.fixture
def result_response_sample(result_tokenset) -> Snippet:
    """Result response sample created on result tokenset."""
    return result_tokenset.create_snippet(string="The result is determined")


@pytest.fixture
def user_result_context_sample(user_result_tokenset) -> Snippet:
    """User result context sample created on user result tokenset."""
    return user_result_tokenset.create_snippet(string="Alice asks for a result")


@pytest.fixture
def user_result_response_sample(user_result_tokenset) -> Snippet:
    """User result response sample created on user result tokenset."""
    return user_result_tokenset.create_snippet(string="Alice gets the result")


# NumToken samples
@pytest.fixture
def simple_numtoken_context_sample(simple_numtoken_tokenset) -> Snippet:
    """Simple NumToken context sample."""
    return simple_numtoken_tokenset.create_snippet(string="The cat sits in the tree", numbers=[10])


@pytest.fixture
def simple_numtoken_response_sample(simple_numtoken_tokenset) -> Snippet:
    """Simple NumToken response sample."""
    return simple_numtoken_tokenset.create_snippet(string="The cat responds with a grin", numbers=[8])


@pytest.fixture
def user_numtoken_context_sample(user_numtoken_tokenset) -> Snippet:
    """User NumToken context sample."""
    return user_numtoken_tokenset.create_snippet(string="Alice asks a question", numbers=[12])


@pytest.fixture
def user_numtoken_response_sample(user_numtoken_tokenset) -> Snippet:
    """User NumToken response sample."""
    return user_numtoken_tokenset.create_snippet(string="Alice receives an answer", numbers=[15])


@pytest.fixture
def result_numtoken_context_sample(result_numtoken_tokenset) -> Snippet:
    """Result NumToken context sample."""
    return result_numtoken_tokenset.create_snippet(string="The conversation continues", numbers=[7])


@pytest.fixture
def result_numtoken_response_sample(result_numtoken_tokenset) -> Snippet:
    """Result NumToken response sample."""
    return result_numtoken_tokenset.create_snippet(string="The result is determined", numbers=[9])


@pytest.fixture
def user_result_numtoken_context_sample(user_result_numtoken_tokenset) -> Snippet:
    """User result NumToken context sample."""
    return user_result_numtoken_tokenset.create_snippet(string="Alice asks for a result", numbers=[11])


@pytest.fixture
def user_result_numtoken_response_sample(user_result_numtoken_tokenset) -> Snippet:
    """User result NumToken response sample."""
    return user_result_numtoken_tokenset.create_snippet(string="Alice gets the result", numbers=[13])


# NumListToken samples
@pytest.fixture
def simple_numlisttoken_context_sample(simple_numlisttoken_tokenset) -> Snippet:
    """Simple NumListToken context sample."""
    return simple_numlisttoken_tokenset.create_snippet(string="The cat sits in the tree", number_lists=[[10, 20, 30]])


@pytest.fixture
def simple_numlisttoken_response_sample(simple_numlisttoken_tokenset) -> Snippet:
    """Simple NumListToken response sample."""
    return simple_numlisttoken_tokenset.create_snippet(string="The cat responds with a grin", number_lists=[[5, 15, 25]])


@pytest.fixture
def user_numlisttoken_context_sample(user_numlisttoken_tokenset) -> Snippet:
    """User NumListToken context sample."""
    return user_numlisttoken_tokenset.create_snippet(string="Alice asks a question", number_lists=[[1, 2, 3]])


@pytest.fixture
def user_numlisttoken_response_sample(user_numlisttoken_tokenset) -> Snippet:
    """User NumListToken response sample."""
    return user_numlisttoken_tokenset.create_snippet(string="Alice receives an answer", number_lists=[[4, 5, 6]])


@pytest.fixture
def result_numlisttoken_context_sample(result_numlisttoken_tokenset) -> Snippet:
    """Result NumListToken context sample."""
    return result_numlisttoken_tokenset.create_snippet(string="The conversation continues", number_lists=[[7, 8, 9]])


@pytest.fixture
def result_numlisttoken_response_sample(result_numlisttoken_tokenset) -> Snippet:
    """Result NumListToken response sample."""
    return result_numlisttoken_tokenset.create_snippet(string="The result is determined", number_lists=[[10, 11, 12]])


@pytest.fixture
def user_result_numlisttoken_context_sample(user_result_numlisttoken_tokenset) -> Snippet:
    """User result NumListToken context sample."""
    return user_result_numlisttoken_tokenset.create_snippet(string="Alice asks for a result", number_lists=[[13, 14, 15]])


@pytest.fixture
def user_result_numlisttoken_response_sample(user_result_numlisttoken_tokenset) -> Snippet:
    """User result NumListToken response sample."""
    return user_result_numlisttoken_tokenset.create_snippet(string="Alice gets the result", number_lists=[[16, 17, 18]])


@pytest.fixture
def scores_context_sample(scores_tokenset) -> Snippet:
    """Scores context sample."""
    return scores_tokenset.create_snippet(string="The scores are calculated", number_lists=[[1, 2, 3, 4, 5]])


@pytest.fixture
def scores_response_sample(scores_tokenset) -> Snippet:
    """Scores response sample."""
    return scores_tokenset.create_snippet(string="The final scores are ready", number_lists=[[6, 7, 8, 9, 10]])


# Mixed numeric samples
@pytest.fixture
def simple_mixed_context_sample(simple_mixed_tokenset) -> Snippet:
    """Simple mixed context sample with both NumToken and NumListToken."""
    return simple_mixed_tokenset.create_snippet(string="The cat sits in the tree", numbers=[10], number_lists=[[1, 2, 3]])


@pytest.fixture
def simple_mixed_response_sample(simple_mixed_tokenset) -> Snippet:
    """Simple mixed response sample with both NumToken and NumListToken."""
    return simple_mixed_tokenset.create_snippet(string="The cat responds with a grin", numbers=[8], number_lists=[[4, 5, 6]])


@pytest.fixture
def user_mixed_context_sample(user_mixed_tokenset) -> Snippet:
    """User mixed context sample with both NumToken and NumListToken."""
    return user_mixed_tokenset.create_snippet(string="Alice asks a question", numbers=[12], number_lists=[[7, 8, 9]])


@pytest.fixture
def user_mixed_response_sample(user_mixed_tokenset) -> Snippet:
    """User mixed response sample with both NumToken and NumListToken."""
    return user_mixed_tokenset.create_snippet(string="Alice receives an answer", numbers=[15], number_lists=[[10, 11, 12]])


@pytest.fixture
def result_mixed_context_sample(result_mixed_tokenset) -> Snippet:
    """Result mixed context sample with both NumToken and NumListToken."""
    return result_mixed_tokenset.create_snippet(string="The conversation continues", numbers=[7], number_lists=[[13, 14, 15]])


@pytest.fixture
def result_mixed_response_sample(result_mixed_tokenset) -> Snippet:
    """Result mixed response sample with both NumToken and NumListToken."""
    return result_mixed_tokenset.create_snippet(string="The result is determined", numbers=[9], number_lists=[[16, 17, 18]])


@pytest.fixture
def user_result_mixed_context_sample(user_result_mixed_tokenset) -> Snippet:
    """User result mixed context sample with both NumToken and NumListToken."""
    return user_result_mixed_tokenset.create_snippet(string="Alice asks for a result", numbers=[11], number_lists=[[19, 20, 21]])


@pytest.fixture
def user_result_mixed_response_sample(user_result_mixed_tokenset) -> Snippet:
    """User result mixed response sample with both NumToken and NumListToken."""
    return user_result_mixed_tokenset.create_snippet(string="Alice gets the result", numbers=[13], number_lists=[[22, 23, 24]])
