"""
Protocol fixtures for testing JSON creation functionality.
These protocols are built using instruction fixtures to cover various scenarios.
"""
import pytest
from model_train_protocol import Protocol


@pytest.fixture
def basic_simple_protocol(simple_workflow_instruction_with_samples) -> Protocol:
    """Basic protocol with simple instruction."""
    protocol = Protocol("basic_simple", context_snippets=2, encrypt=False)
    
    # Add context
    protocol.add_context("This is a basic context line.")
    protocol.add_context("This is a second basic context line.")
    
    # Add instruction
    protocol.add_instruction(simple_workflow_instruction_with_samples)
    
    return protocol

@pytest.fixture
def basic_simple_protocol_with_guardrail(simple_workflow_instruction_with_samples_with_guardrail) -> Protocol:
    """Basic protocol with simple instruction."""
    protocol = Protocol("basic_simple", context_snippets=2, encrypt=False)

    # Add context
    protocol.add_context("This is a basic context line.")
    protocol.add_context("This is a second basic context line.")

    # Add instruction
    protocol.add_instruction(simple_workflow_instruction_with_samples_with_guardrail)

    return protocol


@pytest.fixture
def basic_user_protocol(user_workflow_instruction_with_samples) -> Protocol:
    """Basic protocol with user instruction."""
    protocol = Protocol("basic_user", context_snippets=2, encrypt=False)

    # Add context
    protocol.add_context("This is a user context line.")
    protocol.add_context("This is a second user context line.")

    # Add instruction
    protocol.add_instruction(user_workflow_instruction_with_samples)

    return protocol

@pytest.fixture
def basic_user_protocol_with_guardrail(user_workflow_instruction_with_samples_and_guardrail) -> Protocol:
    """Basic protocol with simple instruction."""
    protocol = Protocol("basic_simple", context_snippets=2, encrypt=False)

    # Add context
    protocol.add_context("This is a basic context line.")
    protocol.add_context("This is a second basic context line.")

    # Add instruction
    protocol.add_instruction(user_workflow_instruction_with_samples_and_guardrail)

    return protocol


@pytest.fixture
def numtoken_protocol(simple_numtoken_workflow_instruction_with_samples) -> Protocol:
    """Protocol with NumToken instruction."""
    protocol = Protocol("numtoken_protocol", context_snippets=2, encrypt=False)
    
    # Add context
    protocol.add_context("This protocol uses numeric tokens.")
    protocol.add_context("This is a second context line for numeric tokens.")
    
    # Add instruction
    protocol.add_instruction(simple_numtoken_workflow_instruction_with_samples)
    
    return protocol


@pytest.fixture
def numlisttoken_protocol(simple_numlisttoken_workflow_instruction_with_samples) -> Protocol:
    """Protocol with NumListToken instruction."""
    protocol = Protocol("numlisttoken_protocol", context_snippets=2, encrypt=False)
    
    # Add context
    protocol.add_context("This protocol uses numeric list tokens.")
    protocol.add_context("This is a second context line for numeric list tokens.")
    
    # Add instruction
    protocol.add_instruction(simple_numlisttoken_workflow_instruction_with_samples)
    
    return protocol


@pytest.fixture
def mixed_numeric_protocol(mixed_instruction_2context_with_samples) -> Protocol:
    """Protocol with mixed numeric instruction."""
    protocol = Protocol("mixed_numeric", context_snippets=2, encrypt=False)
    
    # Add context
    protocol.add_context("This protocol uses mixed numeric tokens.")
    protocol.add_context("This is a second context line for mixed numeric tokens.")
    
    # Add instruction
    protocol.add_instruction(mixed_instruction_2context_with_samples)
    
    return protocol


@pytest.fixture
def user_mixed_protocol(user_mixed_instruction_2context_with_samples) -> Protocol:
    """Protocol with user mixed instruction."""
    protocol = Protocol("user_mixed", context_snippets=2, encrypt=False)
    
    # Add context
    protocol.add_context("This protocol uses user mixed tokens.")
    protocol.add_context("This is a second context line for user mixed tokens.")
    
    # Add instruction
    protocol.add_instruction(user_mixed_instruction_2context_with_samples)
    
    return protocol


@pytest.fixture
def multi_instruction_protocol(
    simple_workflow_instruction_with_samples, 
    user_workflow_instruction_with_samples,
    simple_numtoken_workflow_instruction_with_samples
) -> Protocol:
    """Protocol with multiple instructions."""
    protocol = Protocol("multi_instruction", context_snippets=2, encrypt=False)
    
    # Add context
    protocol.add_context("This protocol has multiple instructions.")
    protocol.add_context("This is a second context line for multiple instructions.")
    
    # Add multiple instructions
    protocol.add_instruction(simple_workflow_instruction_with_samples)
    protocol.add_instruction(user_workflow_instruction_with_samples)
    protocol.add_instruction(simple_numtoken_workflow_instruction_with_samples)
    
    return protocol


@pytest.fixture
def encrypted_protocol(simple_workflow_instruction_with_samples) -> Protocol:
    """Encrypted protocol."""
    protocol = Protocol("encrypted_protocol", context_snippets=2, encrypt=True)
    
    # Add context
    protocol.add_context("This is an encrypted protocol.")
    protocol.add_context("This is a second context line for encrypted protocol.")
    
    # Add instruction
    protocol.add_instruction(simple_workflow_instruction_with_samples)
    
    return protocol


@pytest.fixture
def workflow_protocol(simple_workflow_instruction_with_samples, user_workflow_instruction_with_samples) -> Protocol:
    """Protocol with workflow instructions (2 context lines)."""
    protocol = Protocol("workflow_protocol", context_snippets=2, encrypt=False)
    
    # Add context
    protocol.add_context("This is workflow context line 1.")
    protocol.add_context("This is workflow context line 2.")
    
    # Add instructions
    protocol.add_instruction(simple_workflow_instruction_with_samples)
    protocol.add_instruction(user_workflow_instruction_with_samples)
    
    return protocol


@pytest.fixture
def comprehensive_protocol(
    simple_workflow_instruction_with_samples,
    user_workflow_instruction_with_samples,
    simple_numtoken_workflow_instruction_with_samples
) -> Protocol:
    """Comprehensive protocol with all instruction types."""
    protocol = Protocol("comprehensive", context_snippets=2, encrypt=False)
    
    # Add context
    protocol.add_context("This is a comprehensive protocol with all instruction types.")
    protocol.add_context("This is a second context line for comprehensive protocol.")
    
    # Add all instruction types
    protocol.add_instruction(simple_workflow_instruction_with_samples)
    protocol.add_instruction(user_workflow_instruction_with_samples)
    protocol.add_instruction(simple_numtoken_workflow_instruction_with_samples)
    
    return protocol


# 2 Context Line Workflow Protocols
@pytest.fixture
def workflow_2context_protocol(simple_workflow_2context_instruction_with_samples, user_workflow_2context_instruction_with_samples) -> Protocol:
    """Protocol with 2 context line workflow instructions."""
    protocol = Protocol("workflow_2context", context_snippets=2, encrypt=False)
    
    # Add context
    protocol.add_context("This is a 2 context line workflow protocol.")
    
    # Add instructions
    protocol.add_instruction(simple_workflow_2context_instruction_with_samples)
    protocol.add_instruction(user_workflow_2context_instruction_with_samples)
    
    return protocol


@pytest.fixture
def numtoken_workflow_2context_protocol(simple_numtoken_workflow_2context_instruction_with_samples) -> Protocol:
    """Protocol with 2 context line NumToken workflow instruction."""
    protocol = Protocol("numtoken_workflow_2context", context_snippets=2, encrypt=False)
    
    # Add context
    protocol.add_context("This is a 2 context line NumToken workflow protocol.")
    
    # Add instruction
    protocol.add_instruction(simple_numtoken_workflow_2context_instruction_with_samples)
    
    return protocol


# 5 Context Line Workflow Protocols
@pytest.fixture
def workflow_5context_protocol(simple_workflow_5context_instruction_with_samples, user_workflow_5context_instruction_with_samples) -> Protocol:
    """Protocol with 5 context line workflow instructions."""
    protocol = Protocol("workflow_5context", context_snippets=5, encrypt=False)
    
    # Add context
    protocol.add_context("This is a 5 context line workflow protocol.")
    
    # Add instructions
    protocol.add_instruction(simple_workflow_5context_instruction_with_samples)
    protocol.add_instruction(user_workflow_5context_instruction_with_samples)
    
    return protocol


@pytest.fixture
def numtoken_workflow_5context_protocol(simple_numtoken_workflow_5context_instruction_with_samples) -> Protocol:
    """Protocol with 5 context line NumToken workflow instruction."""
    protocol = Protocol("numtoken_workflow_5context", context_snippets=5, encrypt=False)
    
    # Add context
    protocol.add_context("This is a 5 context line NumToken workflow protocol")
    # Add instruction
    protocol.add_instruction(simple_numtoken_workflow_5context_instruction_with_samples)
    
    return protocol
