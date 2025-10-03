"""
Protocol workflow instruction fixtures with 2 context lines.
"""
import pytest

from model_train_protocol import SimpleInstruction, UserInstruction


@pytest.fixture
def simple_workflow_instruction_with_samples(simple_tokenset, user_tokenset, simple_context_sample, user_context_sample, simple_response_sample, token_workflow_result) -> SimpleInstruction:
    """Simple instruction with 2 context lines for workflow tests."""
    instruction = SimpleInstruction(
        context=[simple_tokenset, user_tokenset],
        response=simple_tokenset,
        final=token_workflow_result
    )
    
    # Add samples with 2 context snippets - one from each tokenset
    instruction.add_sample(
        context_snippets=[simple_context_sample, user_context_sample],
        output_snippet=simple_response_sample,
        value=None
    )
    instruction.add_sample(
        context_snippets=[simple_context_sample, user_context_sample],
        output_snippet=simple_response_sample,
        value=None
    )
    instruction.add_sample(
        context_snippets=[simple_context_sample, user_context_sample],
        output_snippet=simple_response_sample,
        value=None
    )
    
    return instruction


@pytest.fixture
def user_workflow_instruction_with_samples(simple_tokenset, user_tokenset, simple_context_sample, user_context_sample, user_response_sample, token_workflow_end) -> UserInstruction:
    """User instruction with 2 context lines for workflow tests."""
    instruction = UserInstruction(
        context=[simple_tokenset, user_tokenset],
        user=user_tokenset,
        final=token_workflow_end
    )
    
    # Add samples with 2 context snippets - one from each tokenset
    instruction.add_sample(
        context_snippets=[simple_context_sample, user_context_sample],
        prompt="User prompt 0",
        output_snippet=user_response_sample,
        value=None
    )
    instruction.add_sample(
        context_snippets=[simple_context_sample, user_context_sample],
        prompt="User prompt 1",
        output_snippet=user_response_sample,
        value=None
    )
    instruction.add_sample(
        context_snippets=[simple_context_sample, user_context_sample],
        prompt="User prompt 2",
        output_snippet=user_response_sample,
        value=None
    )
    
    return instruction


@pytest.fixture
def simple_numtoken_workflow_instruction_with_samples(simple_numtoken_tokenset, user_tokenset, simple_numtoken_context_sample, user_context_sample, simple_numtoken_response_sample, token_workflow_count) -> SimpleInstruction:
    """Simple instruction with NumToken and 2 context lines for workflow tests."""
    instruction = SimpleInstruction(
        context=[simple_numtoken_tokenset, user_tokenset],
        response=simple_numtoken_tokenset,
        final=token_workflow_count
    )
    
    # Add samples with 2 context snippets - one from each tokenset
    instruction.add_sample(
        context_snippets=[simple_numtoken_context_sample, user_context_sample],
        output_snippet=simple_numtoken_response_sample,
        value=10
    )
    instruction.add_sample(
        context_snippets=[simple_numtoken_context_sample, user_context_sample],
        output_snippet=simple_numtoken_response_sample,
        value=15
    )
    instruction.add_sample(
        context_snippets=[simple_numtoken_context_sample, user_context_sample],
        output_snippet=simple_numtoken_response_sample,
        value=20
    )
    
    return instruction


@pytest.fixture
def simple_numlisttoken_workflow_instruction_with_samples(
    simple_numlisttoken_tokenset, user_tokenset, simple_numlisttoken_context_sample, user_context_sample, simple_numlisttoken_response_sample, token_workflow_coordinates
) -> SimpleInstruction:
    """Simple NumListToken instruction with 2 context lines for workflow tests."""
    instruction = SimpleInstruction(
        context=[simple_numlisttoken_tokenset, user_tokenset],
        response=simple_numlisttoken_tokenset,
        final=token_workflow_coordinates
    )

    # Add samples with 2 context snippets - one from each tokenset
    instruction.add_sample(
        context_snippets=[simple_numlisttoken_context_sample, user_context_sample],
        output_snippet=simple_numlisttoken_response_sample,
        value=[1, 2, 3]
    )
    instruction.add_sample(
        context_snippets=[simple_numlisttoken_context_sample, user_context_sample],
        output_snippet=simple_numlisttoken_response_sample,
        value=[4.2, .45, 6.8]
    )
    instruction.add_sample(
        context_snippets=[simple_numlisttoken_context_sample, user_context_sample],
        output_snippet=simple_numlisttoken_response_sample,
        value=[7, 8, 9]
    )
    
    return instruction
