"""
Workflow instruction fixtures with different context line counts (1, 2, 5).
"""
import pytest

from model_train_protocol import Instruction, ExtendedInstruction, FinalToken, FinalNumToken
from model_train_protocol.common.instructions.input.InstructionInput import InstructionInput
from model_train_protocol.common.instructions.output.InstructionOutput import InstructionOutput
from model_train_protocol.common.instructions.output.ExtendedResponse import ExtendedResponse
from model_train_protocol.common.tokens.NumToken import NumToken


# 2 Context Line Instructions (existing from protocol_workflow_instructions.py)
@pytest.fixture
def simple_workflow_2context_instruction_with_samples(simple_tokenset, user_tokenset, simple_context_sample, user_context_sample, simple_response_sample, token_workflow_result) -> Instruction:
    """Simple instruction with 2 context lines for workflow tests."""
    final_token = FinalToken(token_workflow_result.value) if not isinstance(token_workflow_result, FinalToken) else token_workflow_result
    instruction_input = InstructionInput(tokensets=[simple_tokenset, user_tokenset], context=None)
    instruction_output = InstructionOutput(tokenset=simple_tokenset, final=final_token)
    instruction = Instruction(
        input=instruction_input,
        output=instruction_output,
        name="simple_workflow_2context_instruction"
    )
    
    # Add samples with 2 context snippets
    instruction.add_sample(
        input_snippets=[simple_context_sample, user_context_sample],
        output_snippet=simple_response_sample,
        output_value=None
    )
    instruction.add_sample(
        input_snippets=[simple_context_sample, user_context_sample],
        output_snippet=simple_response_sample,
        output_value=None
    )
    instruction.add_sample(
        input_snippets=[simple_context_sample, user_context_sample],
        output_snippet=simple_response_sample,
        output_value=None
    )
    
    return instruction


@pytest.fixture
def user_workflow_2context_instruction_with_samples(simple_tokenset, user_tokenset, simple_context_sample, user_context_sample, user_response_sample, token_workflow_end) -> ExtendedInstruction:
    """User instruction with 2 context lines for workflow tests."""
    final_token = FinalToken(token_workflow_end.value) if not isinstance(token_workflow_end, FinalToken) else token_workflow_end
    instruction_input = InstructionInput(tokensets=[simple_tokenset, user_tokenset, user_tokenset], context=None)
    extended_response = ExtendedResponse(final=final_token)
    instruction = ExtendedInstruction(
        input=instruction_input,
        output=extended_response,
        name="user_workflow_2context_instruction"
    )
    
    # Add samples with 2 context snippets plus output snippet
    instruction.add_sample(
        inputs=[simple_context_sample, user_context_sample, user_response_sample],
        response_string="User prompt 0",
        value=None
    )
    instruction.add_sample(
        inputs=[simple_context_sample, user_context_sample, user_response_sample],
        response_string="User prompt 1",
        value=None
    )
    instruction.add_sample(
        inputs=[simple_context_sample, user_context_sample, user_response_sample],
        response_string="User prompt 2",
        value=None
    )
    
    return instruction


@pytest.fixture
def simple_numtoken_workflow_2context_instruction_with_samples(simple_numtoken_tokenset, simple_tokenset, user_tokenset, simple_numtoken_context_sample, user_context_sample, simple_response_sample, token_workflow_count) -> Instruction:
    """Simple instruction with NumToken and 2 context lines for workflow tests."""
    if isinstance(token_workflow_count, NumToken):
        final_token = FinalNumToken(token_workflow_count.value, token_workflow_count.min_value, token_workflow_count.max_value)
    else:
        final_token = FinalToken(token_workflow_count.value) if not isinstance(token_workflow_count, FinalToken) else token_workflow_count
    instruction_input = InstructionInput(tokensets=[simple_numtoken_tokenset, user_tokenset], context=None)
    # Use simple_tokenset (without NumToken) for output, as InstructionOutput doesn't allow NumTokens in response tokenset
    instruction_output = InstructionOutput(tokenset=simple_tokenset, final=final_token)
    instruction = Instruction(
        input=instruction_input,
        output=instruction_output,
        name="simple_numtoken_workflow_2context_instruction"
    )
    
    # Add samples with 2 context snippets
    instruction.add_sample(
        input_snippets=[simple_numtoken_context_sample, user_context_sample],
        output_snippet=simple_response_sample,
        output_value=5
    )
    instruction.add_sample(
        input_snippets=[simple_numtoken_context_sample, user_context_sample],
        output_snippet=simple_response_sample,
        output_value=7
    )
    instruction.add_sample(
        input_snippets=[simple_numtoken_context_sample, user_context_sample],
        output_snippet=simple_response_sample,
        output_value=10
    )
    
    return instruction


# 5 Context Line Instructions
@pytest.fixture
def simple_workflow_5context_instruction_with_samples(
    simple_tokenset, user_tokenset, simple_context_sample, user_context_sample, simple_response_sample, token_workflow_result
) -> Instruction:
    """Simple instruction with 5 context lines for workflow tests."""
    final_token = FinalToken(token_workflow_result.value) if not isinstance(token_workflow_result, FinalToken) else token_workflow_result
    instruction_input = InstructionInput(tokensets=[simple_tokenset, user_tokenset, simple_tokenset, user_tokenset, simple_tokenset], context=None)
    instruction_output = InstructionOutput(tokenset=simple_tokenset, final=final_token)
    instruction = Instruction(
        input=instruction_input,
        output=instruction_output,
        name="simple_workflow_5context_instruction"
    )
    
    # Add samples with 5 context snippets
    instruction.add_sample(
        input_snippets=[simple_context_sample, user_context_sample, simple_context_sample, user_context_sample, simple_context_sample],
        output_snippet=simple_response_sample,
        output_value=None
    )
    instruction.add_sample(
        input_snippets=[simple_context_sample, user_context_sample, simple_context_sample, user_context_sample, simple_context_sample],
        output_snippet=simple_response_sample,
        output_value=None
    )
    instruction.add_sample(
        input_snippets=[simple_context_sample, user_context_sample, simple_context_sample, user_context_sample, simple_context_sample],
        output_snippet=simple_response_sample,
        output_value=None
    )
    
    return instruction


@pytest.fixture
def user_workflow_5context_instruction_with_samples(
    simple_tokenset, user_tokenset, simple_context_sample, user_context_sample, user_response_sample, token_workflow_end
) -> ExtendedInstruction:
    """User instruction with 5 context lines for workflow tests."""
    final_token = FinalToken(token_workflow_end.value) if not isinstance(token_workflow_end, FinalToken) else token_workflow_end
    instruction_input = InstructionInput(tokensets=[simple_tokenset, user_tokenset, simple_tokenset, user_tokenset, simple_tokenset, user_tokenset], context=None)
    extended_response = ExtendedResponse(final=final_token)
    instruction = ExtendedInstruction(
        input=instruction_input,
        output=extended_response,
        name="user_workflow_5context_instruction"
    )
    
    # Add samples with 5 context snippets plus output snippet
    instruction.add_sample(
        inputs=[simple_context_sample, user_context_sample, simple_context_sample, user_context_sample, simple_context_sample, user_response_sample],
        response_string="User prompt 0",
        value=None
    )
    instruction.add_sample(
        inputs=[simple_context_sample, user_context_sample, simple_context_sample, user_context_sample, simple_context_sample, user_response_sample],
        response_string="User prompt 1",
        value=None
    )
    instruction.add_sample(
        inputs=[simple_context_sample, user_context_sample, simple_context_sample, user_context_sample, simple_context_sample, user_response_sample],
        response_string="User prompt 2",
        value=None
    )
    
    return instruction


@pytest.fixture
def simple_numtoken_workflow_5context_instruction_with_samples(
    simple_numtoken_tokenset, simple_tokenset, user_tokenset, simple_numtoken_context_sample, user_context_sample, simple_response_sample, token_workflow_count
) -> Instruction:
    """Simple instruction with NumToken and 5 context lines for workflow tests."""
    if isinstance(token_workflow_count, NumToken):
        final_token = FinalNumToken(token_workflow_count.value, token_workflow_count.min_value, token_workflow_count.max_value)
    else:
        final_token = FinalToken(token_workflow_count.value) if not isinstance(token_workflow_count, FinalToken) else token_workflow_count
    instruction_input = InstructionInput(tokensets=[simple_numtoken_tokenset, user_tokenset, simple_numtoken_tokenset, user_tokenset, simple_numtoken_tokenset], context=None)
    # Use simple_tokenset (without NumToken) for output, as InstructionOutput doesn't allow NumTokens in response tokenset
    instruction_output = InstructionOutput(tokenset=simple_tokenset, final=final_token)
    instruction = Instruction(
        input=instruction_input,
        output=instruction_output,
        name="simple_numtoken_workflow_5context_instruction"
    )
    
    # Add samples with 5 context snippets
    instruction.add_sample(
        input_snippets=[simple_numtoken_context_sample, user_context_sample, simple_numtoken_context_sample, user_context_sample, simple_numtoken_context_sample],
        output_snippet=simple_response_sample,
        output_value=5
    )
    instruction.add_sample(
        input_snippets=[simple_numtoken_context_sample, user_context_sample, simple_numtoken_context_sample, user_context_sample, simple_numtoken_context_sample],
        output_snippet=simple_response_sample,
        output_value=7
    )
    instruction.add_sample(
        input_snippets=[simple_numtoken_context_sample, user_context_sample, simple_numtoken_context_sample, user_context_sample, simple_numtoken_context_sample],
        output_snippet=simple_response_sample,
        output_value=10
    )
    
    return instruction
