"""
Protocol workflow instruction fixtures with 2 context lines.
"""
import pytest

from model_train_protocol import Instruction, ExtendedInstruction, FinalToken, FinalNumToken
from model_train_protocol.common.instructions.input.InstructionInput import InstructionInput
from model_train_protocol.common.instructions.output.InstructionOutput import InstructionOutput
from model_train_protocol.common.instructions.output.ExtendedResponse import ExtendedResponse
from model_train_protocol.common.tokens.NumToken import NumToken


@pytest.fixture
def simple_workflow_instruction_with_samples(simple_tokenset, user_tokenset, simple_context_sample, user_context_sample,
                                             simple_response_sample, token_workflow_result,
                                             content_guardrail) -> Instruction:
    """Simple instruction with 2 context lines for workflow tests."""
    final_token = FinalToken(token_workflow_result.value) if not isinstance(token_workflow_result, FinalToken) else token_workflow_result
    instruction_input = InstructionInput(tokensets=[simple_tokenset, user_tokenset], context=None)
    instruction_output = InstructionOutput(tokenset=simple_tokenset, final=final_token)
    instruction = Instruction(
        input=instruction_input,
        output=instruction_output,
        name="simple_workflow_instruction"
    )

    # Add samples with 2 context snippets - one from each tokenset
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
def simple_workflow_instruction_with_samples_with_guardrail(simple_workflow_instruction_with_samples,
                                                            content_guardrail) -> Instruction:
    """Simple instruction with 2 context lines for workflow tests."""
    instruction = simple_workflow_instruction_with_samples
    # Add guardrail to the instruction at tokenset index 1 (user_tokenset)
    instruction.add_guardrail(content_guardrail, tokenset_index=1)
    return instruction


@pytest.fixture
def user_workflow_instruction_with_samples(simple_tokenset, user_tokenset, simple_context_sample, user_context_sample,
                                           user_response_sample, token_workflow_end,
                                           safety_guardrail) -> ExtendedInstruction:
    """User instruction with 2 context lines for workflow tests."""
    final_token = FinalToken(token_workflow_end.value) if not isinstance(token_workflow_end, FinalToken) else token_workflow_end
    instruction_input = InstructionInput(tokensets=[simple_tokenset, user_tokenset, user_tokenset], context=None)
    extended_response = ExtendedResponse(final=final_token)
    instruction = ExtendedInstruction(
        input=instruction_input,
        output=extended_response,
        name="user_workflow_instruction"
    )

    # Add samples with 2 context snippets plus output snippet
    instruction.add_sample(
        context_snippets=[simple_context_sample, user_context_sample, user_response_sample],
        response_string="User prompt 0",
        value=None
    )
    instruction.add_sample(
        context_snippets=[simple_context_sample, user_context_sample, user_response_sample],
        response_string="User prompt 1",
        value=None
    )
    instruction.add_sample(
        context_snippets=[simple_context_sample, user_context_sample, user_response_sample],
        response_string="User prompt 2",
        value=None
    )

    return instruction


@pytest.fixture
def user_workflow_instruction_with_samples_and_guardrail(user_workflow_instruction_with_samples,
                                                        safety_guardrail) -> ExtendedInstruction:
    """User instruction with guardrail for workflow tests."""
    instruction = user_workflow_instruction_with_samples
    # Add guardrail to the instruction at tokenset index 1 (user_tokenset)
    instruction.add_guardrail(safety_guardrail, tokenset_index=1)
    return instruction


@pytest.fixture
def simple_numtoken_workflow_instruction_with_samples(simple_numtoken_tokenset, simple_tokenset, user_tokenset,
                                                      simple_numtoken_context_sample, user_context_sample,
                                                      simple_response_sample, token_workflow_count,
                                                      content_guardrail) -> Instruction:
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
        name="simple_numtoken_workflow_instruction"
    )

    # Add samples with 2 context snippets - one from each tokenset
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

    # Add guardrail to the instruction at tokenset index 1 (user_tokenset)
    instruction.add_guardrail(content_guardrail, tokenset_index=1)

    return instruction


@pytest.fixture
def simple_numlisttoken_workflow_instruction_with_samples(
        simple_numlisttoken_tokenset, simple_tokenset, user_tokenset, simple_numlisttoken_context_sample, user_context_sample,
        simple_response_sample, token_workflow_coordinates, safety_guardrail
) -> Instruction:
    """Simple NumListToken instruction with 2 context lines for workflow tests."""
    # Note: NumListToken cannot be used as final token, using FinalToken instead
    final_token = FinalToken(token_workflow_coordinates.value) if not isinstance(token_workflow_coordinates, FinalToken) else token_workflow_coordinates
    instruction_input = InstructionInput(tokensets=[simple_numlisttoken_tokenset, user_tokenset], context=None)
    # Use simple_tokenset (without NumListToken) for output, as InstructionOutput doesn't allow NumListTokens in response tokenset
    instruction_output = InstructionOutput(tokenset=simple_tokenset, final=final_token)
    instruction = Instruction(
        input=instruction_input,
        output=instruction_output
    )

    # Add samples with 2 context snippets - one from each tokenset
    instruction.add_sample(
        input_snippets=[simple_numlisttoken_context_sample, user_context_sample],
        output_snippet=simple_response_sample,
        output_value=[1, 2, 3]
    )
    instruction.add_sample(
        input_snippets=[simple_numlisttoken_context_sample, user_context_sample],
        output_snippet=simple_response_sample,
        output_value=[4.2, .45, 6.8]
    )
    instruction.add_sample(
        input_snippets=[simple_numlisttoken_context_sample, user_context_sample],
        output_snippet=simple_response_sample,
        output_value=[7, 8, 9]
    )

    return instruction
