"""
Workflow instruction fixtures with different context line counts (1, 2, 5).
"""
import pytest

from model_train_protocol import Instruction, UnsetInstruction


# 2 Context Line Instructions (existing from protocol_workflow_instructions.py)
@pytest.fixture
def simple_workflow_2context_instruction_with_samples(simple_tokenset, user_tokenset, simple_context_sample, user_context_sample, simple_response_sample, token_workflow_result) -> Instruction:
    """Simple instruction with 2 context lines for workflow tests."""
    instruction = Instruction(
        context=[simple_tokenset, user_tokenset],
        response=simple_tokenset,
        final=token_workflow_result
    )
    
    # Add samples with 2 context snippets
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
def user_workflow_2context_instruction_with_samples(simple_tokenset, user_tokenset, simple_context_sample, user_context_sample, user_response_sample, token_workflow_end) -> UnsetInstruction:
    """User instruction with 2 context lines for workflow tests."""
    instruction = UnsetInstruction(
        context=[simple_tokenset, user_tokenset],
        user=user_tokenset,
        final=token_workflow_end
    )
    
    # Add samples with 2 context snippets
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
def simple_numtoken_workflow_2context_instruction_with_samples(simple_numtoken_tokenset, user_tokenset, simple_numtoken_context_sample, user_context_sample, simple_numtoken_response_sample, token_workflow_count) -> Instruction:
    """Simple instruction with NumToken and 2 context lines for workflow tests."""
    instruction = Instruction(
        context=[simple_numtoken_tokenset, user_tokenset],
        response=simple_numtoken_tokenset,
        final=token_workflow_count
    )
    
    # Add samples with 2 context snippets
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


# 5 Context Line Instructions
@pytest.fixture
def simple_workflow_5context_instruction_with_samples(
    simple_tokenset, user_tokenset, simple_context_sample, user_context_sample, simple_response_sample, token_workflow_result
) -> Instruction:
    """Simple instruction with 5 context lines for workflow tests."""
    instruction = Instruction(
        context=[simple_tokenset, user_tokenset, simple_tokenset, user_tokenset, simple_tokenset],
        response=simple_tokenset,
        final=token_workflow_result
    )
    
    # Add samples with 5 context snippets
    instruction.add_sample(
        context_snippets=[simple_context_sample, user_context_sample, simple_context_sample, user_context_sample, simple_context_sample],
        output_snippet=simple_response_sample,
        value=None
    )
    instruction.add_sample(
        context_snippets=[simple_context_sample, user_context_sample, simple_context_sample, user_context_sample, simple_context_sample],
        output_snippet=simple_response_sample,
        value=None
    )
    instruction.add_sample(
        context_snippets=[simple_context_sample, user_context_sample, simple_context_sample, user_context_sample, simple_context_sample],
        output_snippet=simple_response_sample,
        value=None
    )
    
    return instruction


@pytest.fixture
def user_workflow_5context_instruction_with_samples(
    simple_tokenset, user_tokenset, simple_context_sample, user_context_sample, user_response_sample, token_workflow_end
) -> UnsetInstruction:
    """User instruction with 5 context lines for workflow tests."""
    instruction = UnsetInstruction(
        context=[simple_tokenset, user_tokenset, simple_tokenset, user_tokenset, simple_tokenset],
        user=user_tokenset,
        final=token_workflow_end
    )
    
    # Add samples with 5 context snippets
    instruction.add_sample(
        context_snippets=[simple_context_sample, user_context_sample, simple_context_sample, user_context_sample, simple_context_sample],
        prompt="User prompt 0",
        output_snippet=user_response_sample,
        value=None
    )
    instruction.add_sample(
        context_snippets=[simple_context_sample, user_context_sample, simple_context_sample, user_context_sample, simple_context_sample],
        prompt="User prompt 1",
        output_snippet=user_response_sample,
        value=None
    )
    instruction.add_sample(
        context_snippets=[simple_context_sample, user_context_sample, simple_context_sample, user_context_sample, simple_context_sample],
        prompt="User prompt 2",
        output_snippet=user_response_sample,
        value=None
    )
    
    return instruction


@pytest.fixture
def simple_numtoken_workflow_5context_instruction_with_samples(
    simple_numtoken_tokenset, user_tokenset, simple_numtoken_context_sample, user_context_sample, simple_numtoken_response_sample, token_workflow_count
) -> Instruction:
    """Simple instruction with NumToken and 5 context lines for workflow tests."""
    instruction = Instruction(
        context=[simple_numtoken_tokenset, user_tokenset, simple_numtoken_tokenset, user_tokenset, simple_numtoken_tokenset],
        response=simple_numtoken_tokenset,
        final=token_workflow_count
    )
    
    # Add samples with 5 context snippets
    instruction.add_sample(
        context_snippets=[simple_numtoken_context_sample, user_context_sample, simple_numtoken_context_sample, user_context_sample, simple_numtoken_context_sample],
        output_snippet=simple_numtoken_response_sample,
        value=10
    )
    instruction.add_sample(
        context_snippets=[simple_numtoken_context_sample, user_context_sample, simple_numtoken_context_sample, user_context_sample, simple_numtoken_context_sample],
        output_snippet=simple_numtoken_response_sample,
        value=15
    )
    instruction.add_sample(
        context_snippets=[simple_numtoken_context_sample, user_context_sample, simple_numtoken_context_sample, user_context_sample, simple_numtoken_context_sample],
        output_snippet=simple_numtoken_response_sample,
        value=20
    )
    
    return instruction
