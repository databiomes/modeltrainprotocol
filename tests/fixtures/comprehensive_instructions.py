"""
Comprehensive instruction fixtures for testing all tokenset combinations.
Tests all possible combinations of tokensets for both Instruction and ExtendedInstruction.
"""
import pytest

from model_train_protocol import Instruction, ExtendedInstruction, FinalToken, FinalNumToken
from model_train_protocol.common.constants import NON_TOKEN
from model_train_protocol.common.instructions.input.InstructionInput import InstructionInput
from model_train_protocol.common.instructions.output.InstructionOutput import InstructionOutput
from model_train_protocol.common.instructions.output.ExtendedResponse import ExtendedResponse
from model_train_protocol.common.tokens.NumListToken import NumListToken
from model_train_protocol.common.tokens.NumToken import NumToken
from model_train_protocol.common.tokens.Token import Token

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

# Final tokens (converted from regular tokens)
FINAL_TOKEN_RESULT = FinalToken("Result", desc="Result token")
FINAL_NUM_TOKEN_COUNT = FinalNumToken("Count", min_value=1, max_value=100, desc="Count token")
# Note: NumListToken cannot be used as final token, so use FinalToken instead
FINAL_TOKEN_COORDINATES = FinalToken("Coordinates", desc="Coordinates token")
FINAL_TOKEN_SCORES = FinalToken("Scores", desc="Scores token")

# User tokens
TOKEN_USER = Token("User", desc="User token")


# Individual pytest fixtures for comprehensive testing


# Individual instruction fixtures for specific combinations

# Basic Instruction fixtures
@pytest.fixture
def simple_basic_instruction(simple_tokenset) -> Instruction:
    """Basic simple instruction."""
    instruction_input = InstructionInput(tokensets=[simple_tokenset], context=None)
    instruction_output = InstructionOutput(tokenset=simple_tokenset, final=FINAL_TOKEN_RESULT)
    return Instruction(
        input=instruction_input,
        output=instruction_output
    )


@pytest.fixture
def simple_basic_instruction_with_samples(simple_basic_instruction, simple_context_sample, simple_response_sample) -> Instruction:
    """Basic simple instruction with samples."""
    simple_basic_instruction.add_sample(
        input_snippets=[simple_context_sample],
        output_snippet=simple_response_sample,
        output_value=None
    )
    return simple_basic_instruction


@pytest.fixture
def simple_numtoken_instruction(simple_numtoken_tokenset, simple_tokenset) -> Instruction:
    """Simple instruction with NumToken."""
    instruction_input = InstructionInput(tokensets=[simple_numtoken_tokenset], context=None)
    # Use simple_tokenset (without NumToken) for output, as InstructionOutput doesn't allow NumTokens in response tokenset
    instruction_output = InstructionOutput(tokenset=simple_tokenset, final=FINAL_NUM_TOKEN_COUNT)
    return Instruction(
        input=instruction_input,
        output=instruction_output
    )


@pytest.fixture
def simple_numtoken_instruction_with_samples(simple_numtoken_instruction, simple_numtoken_context_sample, simple_response_sample) -> Instruction:
    """Simple instruction with NumToken and samples."""
    simple_numtoken_instruction.add_sample(
        input_snippets=[simple_numtoken_context_sample],
        output_snippet=simple_response_sample,
        output_value=10
    )
    return simple_numtoken_instruction


@pytest.fixture
def simple_numlisttoken_instruction(simple_numlisttoken_tokenset, simple_tokenset) -> Instruction:
    """Simple instruction with NumListToken."""
    instruction_input = InstructionInput(tokensets=[simple_numlisttoken_tokenset], context=None)
    # Use simple_tokenset (without NumListToken) for output, as InstructionOutput doesn't allow NumListTokens in response tokenset
    instruction_output = InstructionOutput(tokenset=simple_tokenset, final=FINAL_TOKEN_COORDINATES)
    return Instruction(
        input=instruction_input,
        output=instruction_output
    )


@pytest.fixture
def simple_numlisttoken_instruction_with_samples(simple_numlisttoken_instruction, simple_numlisttoken_context_sample, simple_response_sample) -> Instruction:
    """Simple instruction with NumListToken and samples."""
    simple_numlisttoken_instruction.add_sample(
        input_snippets=[simple_numlisttoken_context_sample],
        output_snippet=simple_response_sample,
        output_value=[10, 20, 30]
    )
    return simple_numlisttoken_instruction


@pytest.fixture
def simple_mixed_instruction(simple_mixed_tokenset, simple_tokenset) -> Instruction:
    """Simple instruction with mixed numeric tokens."""
    instruction_input = InstructionInput(tokensets=[simple_mixed_tokenset], context=None)
    # Use simple_tokenset (without NumToken/NumListToken) for output, as InstructionOutput doesn't allow numeric tokens in response tokenset
    instruction_output = InstructionOutput(tokenset=simple_tokenset, final=FINAL_NUM_TOKEN_COUNT)
    return Instruction(
        input=instruction_input,
        output=instruction_output
    )


@pytest.fixture
def simple_mixed_instruction_with_samples(simple_mixed_instruction, simple_mixed_context_sample, simple_response_sample) -> Instruction:
    """Simple instruction with mixed numeric tokens and samples."""
    # Use simple_response_sample since output tokenset is simple_tokenset (without NumToken/NumListToken)
    simple_mixed_instruction.add_sample(
        input_snippets=[simple_mixed_context_sample],
        output_snippet=simple_response_sample,
        output_value=25.5
    )
    return simple_mixed_instruction


@pytest.fixture
def simple_scores_instruction(scores_tokenset, simple_tokenset) -> Instruction:
    """Simple instruction with scores tokenset."""
    instruction_input = InstructionInput(tokensets=[scores_tokenset], context=None)
    # Use simple_tokenset (without NumListToken) for output, as InstructionOutput doesn't allow NumListTokens in response tokenset
    instruction_output = InstructionOutput(tokenset=simple_tokenset, final=FINAL_TOKEN_SCORES)
    return Instruction(
        input=instruction_input,
        output=instruction_output
    )


@pytest.fixture
def simple_scores_instruction_with_samples(simple_scores_instruction, scores_context_sample, simple_response_sample) -> Instruction:
    """Simple instruction with scores tokenset and samples."""
    # Use simple_response_sample since output tokenset is simple_tokenset (without NumListToken)
    simple_scores_instruction.add_sample(
        input_snippets=[scores_context_sample],
        output_snippet=simple_response_sample,
        output_value=[8, 9, 7, 10, 6]
    )
    return simple_scores_instruction


# Basic ExtendedInstruction fixtures
@pytest.fixture
def user_basic_instruction(simple_tokenset, user_tokenset) -> ExtendedInstruction:
    """Basic user instruction."""
    instruction_input = InstructionInput(tokensets=[simple_tokenset, user_tokenset], context=None)
    extended_response = ExtendedResponse(final=FINAL_TOKEN_RESULT)
    return ExtendedInstruction(
        input=instruction_input,
        output=extended_response
    )


@pytest.fixture
def user_basic_instruction_with_samples(user_basic_instruction, simple_context_sample, user_prompt_sample) -> ExtendedInstruction:
    """Basic user instruction with samples."""
    user_basic_instruction.add_sample(
        context_snippets=[simple_context_sample, user_prompt_sample],
        response_string="Alice receives an answer",
        value=None
    )
    return user_basic_instruction


@pytest.fixture
def user_numtoken_instruction(simple_numtoken_tokenset, user_numtoken_tokenset) -> ExtendedInstruction:
    """User instruction with NumToken."""
    instruction_input = InstructionInput(tokensets=[simple_numtoken_tokenset, user_numtoken_tokenset], context=None)
    extended_response = ExtendedResponse(final=FINAL_NUM_TOKEN_COUNT)
    return ExtendedInstruction(
        input=instruction_input,
        output=extended_response
    )


@pytest.fixture
def user_numtoken_instruction_with_samples(user_numtoken_instruction, simple_numtoken_context_sample, user_numtoken_response_sample) -> ExtendedInstruction:
    """User instruction with NumToken and samples."""
    user_numtoken_instruction.add_sample(
        context_snippets=[simple_numtoken_context_sample, user_numtoken_response_sample],
        response_string="Count the items",
        value=20
    )
    return user_numtoken_instruction


@pytest.fixture
def user_numlisttoken_instruction(simple_numlisttoken_tokenset, user_numlisttoken_tokenset) -> ExtendedInstruction:
    """User instruction with NumListToken."""
    instruction_input = InstructionInput(tokensets=[simple_numlisttoken_tokenset, user_numlisttoken_tokenset], context=None)
    extended_response = ExtendedResponse(final=FINAL_TOKEN_COORDINATES)
    return ExtendedInstruction(
        input=instruction_input,
        output=extended_response
    )


@pytest.fixture
def user_numlisttoken_instruction_with_samples(user_numlisttoken_instruction, simple_numlisttoken_context_sample, user_numlisttoken_response_sample) -> ExtendedInstruction:
    """User instruction with NumListToken and samples."""
    user_numlisttoken_instruction.add_sample(
        context_snippets=[simple_numlisttoken_context_sample, user_numlisttoken_response_sample],
        response_string="Provide coordinates",
        value=[5, 15, 25]
    )
    return user_numlisttoken_instruction


@pytest.fixture
def user_mixed_instruction(simple_mixed_tokenset, user_mixed_tokenset) -> ExtendedInstruction:
    """User instruction with mixed numeric tokens."""
    instruction_input = InstructionInput(tokensets=[simple_mixed_tokenset, user_mixed_tokenset], context=None)
    extended_response = ExtendedResponse(final=FINAL_NUM_TOKEN_COUNT)
    return ExtendedInstruction(
        input=instruction_input,
        output=extended_response
    )


@pytest.fixture
def user_mixed_instruction_with_samples(user_mixed_instruction, simple_mixed_context_sample, user_mixed_response_sample) -> ExtendedInstruction:
    """User instruction with mixed numeric tokens and samples."""
    user_mixed_instruction.add_sample(
        context_snippets=[simple_mixed_context_sample, user_mixed_response_sample],
        response_string="Generate mixed data",
        value=35.5
    )
    return user_mixed_instruction


@pytest.fixture
def user_scores_instruction(scores_tokenset, user_tokenset) -> ExtendedInstruction:
    """User instruction with scores tokenset."""
    instruction_input = InstructionInput(tokensets=[scores_tokenset, user_tokenset], context=None)
    extended_response = ExtendedResponse(final=FINAL_TOKEN_SCORES)
    return ExtendedInstruction(
        input=instruction_input,
        output=extended_response
    )


@pytest.fixture
def user_scores_instruction_with_samples(user_scores_instruction, scores_context_sample, user_response_sample) -> ExtendedInstruction:
    """User instruction with scores tokenset and samples."""
    user_scores_instruction.add_sample(
        context_snippets=[scores_context_sample, user_response_sample],
        response_string="Rate the performance",
        value=[6.2, 7.5, 8.0, 9.1, 5.4]
    )
    return user_scores_instruction


# Edge case fixtures
@pytest.fixture
def simple_instruction_with_none_final(simple_tokenset) -> Instruction:
    """Simple instruction with NON_TOKEN final token."""
    instruction_input = InstructionInput(tokensets=[simple_tokenset], context=None)
    instruction_output = InstructionOutput(tokenset=simple_tokenset, final=NON_TOKEN)
    return Instruction(
        input=instruction_input,
        output=instruction_output
    )


@pytest.fixture
def simple_instruction_with_non_token_final(simple_tokenset) -> Instruction:
    """Simple instruction with NON_TOKEN final."""
    instruction_input = InstructionInput(tokensets=[simple_tokenset], context=None)
    instruction_output = InstructionOutput(tokenset=simple_tokenset, final=NON_TOKEN)
    return Instruction(
        input=instruction_input,
        output=instruction_output
    )


@pytest.fixture
def simple_instruction_with_empty_samples(simple_tokenset) -> Instruction:
    """Simple instruction with no samples."""
    instruction_input = InstructionInput(tokensets=[simple_tokenset], context=None)
    instruction_output = InstructionOutput(tokenset=simple_tokenset, final=FINAL_TOKEN_RESULT)
    return Instruction(
        input=instruction_input,
        output=instruction_output
    )


@pytest.fixture
def simple_instruction_with_multiple_samples(simple_tokenset, simple_context_sample, simple_response_sample) -> Instruction:
    """Simple instruction with multiple samples."""
    instruction_input = InstructionInput(tokensets=[simple_tokenset], context=None)
    instruction_output = InstructionOutput(tokenset=simple_tokenset, final=FINAL_TOKEN_RESULT)
    instruction = Instruction(
        input=instruction_input,
        output=instruction_output
    )
    
    # Add multiple samples
    for i in range(3):
        instruction.add_sample(
            input_snippets=[simple_context_sample],
            output_snippet=simple_response_sample,
            output_value=None
        )
    
    return instruction


@pytest.fixture
def user_instruction_with_multiple_samples(simple_tokenset, user_tokenset, simple_context_sample, user_response_sample, user_prompt_sample) -> ExtendedInstruction:
    """User instruction with multiple samples."""
    instruction_input = InstructionInput(tokensets=[simple_tokenset, user_tokenset], context=None)
    extended_response = ExtendedResponse(final=FINAL_TOKEN_RESULT)
    instruction = ExtendedInstruction(
        input=instruction_input,
        output=extended_response
    )
    
    # Add multiple samples
    for i in range(3):
        instruction.add_sample(
            context_snippets=[simple_context_sample, user_prompt_sample],
            response_string=f"User prompt {i}",
            value=None
        )
    
    return instruction
