"""
Protocol fixtures for testing JSON creation functionality.
These protocols are built using instruction fixtures to cover various scenarios.
"""
import pytest
from model_train_protocol import Protocol


@pytest.fixture
def basic_simple_protocol(simple_workflow_instruction_with_samples) -> Protocol:
    """Basic protocol with simple instruction."""
    protocol = Protocol("basic_simple", inputs=2, encrypt=False)
    
    # Add context (minimum 10 lines total required)
    protocol.add_context("This is a basic context line.")
    protocol.add_context("This is a second basic context line.")
    protocol.add_context("This is a third basic context line.")
    protocol.add_context("This is a fourth basic context line.")
    protocol.add_context("This is a fifth basic context line.")
    protocol.add_context("This is a sixth basic context line.")
    protocol.add_context("This is a seventh basic context line.")
    protocol.add_context("This is an eighth basic context line.")
    protocol.add_context("This is a ninth basic context line.")
    protocol.add_context("This is a tenth basic context line.")
    
    # Add instruction
    protocol.add_instruction(simple_workflow_instruction_with_samples)
    
    return protocol

@pytest.fixture
def basic_simple_protocol_with_guardrail(simple_workflow_instruction_with_samples_with_guardrail) -> Protocol:
    """Basic protocol with simple instruction."""
    protocol = Protocol("basic_simple", inputs=2, encrypt=False)

    # Add context (minimum 10 lines total required)
    protocol.add_context("This is a basic context line.")
    protocol.add_context("This is a second basic context line.")
    protocol.add_context("This is a third basic context line.")
    protocol.add_context("This is a fourth basic context line.")
    protocol.add_context("This is a fifth basic context line.")
    protocol.add_context("This is a sixth basic context line.")
    protocol.add_context("This is a seventh basic context line.")
    protocol.add_context("This is an eighth basic context line.")
    protocol.add_context("This is a ninth basic context line.")
    protocol.add_context("This is a tenth basic context line.")

    # Add instruction
    protocol.add_instruction(simple_workflow_instruction_with_samples_with_guardrail)

    return protocol


@pytest.fixture
def basic_user_protocol(user_workflow_instruction_with_samples) -> Protocol:
    """Basic protocol with user instruction."""
    protocol = Protocol("basic_user", inputs=2, encrypt=False)

    # Add context (minimum 10 lines total required)
    protocol.add_context("This is a user context line.")
    protocol.add_context("This is a second user context line.")
    protocol.add_context("This is a third user context line.")
    protocol.add_context("This is a fourth user context line.")
    protocol.add_context("This is a fifth user context line.")
    protocol.add_context("This is a sixth user context line.")
    protocol.add_context("This is a seventh user context line.")
    protocol.add_context("This is an eighth user context line.")
    protocol.add_context("This is a ninth user context line.")
    protocol.add_context("This is a tenth user context line.")
    
    # Add instruction
    protocol.add_instruction(user_workflow_instruction_with_samples)

    return protocol

@pytest.fixture
def basic_user_protocol_with_guardrail(user_workflow_instruction_with_samples_and_guardrail) -> Protocol:
    """Basic protocol with simple instruction."""
    protocol = Protocol("basic_simple", inputs=2, encrypt=False)

    # Add context (minimum 10 lines total required)
    protocol.add_context("This is a basic context line.")
    protocol.add_context("This is a second basic context line.")
    protocol.add_context("This is a third basic context line.")
    protocol.add_context("This is a fourth basic context line.")
    protocol.add_context("This is a fifth basic context line.")
    protocol.add_context("This is a sixth basic context line.")
    protocol.add_context("This is a seventh basic context line.")
    protocol.add_context("This is an eighth basic context line.")
    protocol.add_context("This is a ninth basic context line.")
    protocol.add_context("This is a tenth basic context line.")

    # Add instruction
    protocol.add_instruction(user_workflow_instruction_with_samples_and_guardrail)

    return protocol


@pytest.fixture
def numtoken_protocol(simple_numtoken_workflow_instruction_with_samples) -> Protocol:
    """Protocol with NumToken instruction."""
    protocol = Protocol("numtoken_protocol", inputs=2, encrypt=False)
    
    # Add context (minimum 10 lines total required)
    protocol.add_context("This protocol uses numeric tokens.")
    protocol.add_context("This is a second context line for numeric tokens.")
    protocol.add_context("This is a third context line for numeric tokens.")
    protocol.add_context("This is a fourth context line for numeric tokens.")
    protocol.add_context("This is a fifth context line for numeric tokens.")
    protocol.add_context("This is a sixth context line for numeric tokens.")
    protocol.add_context("This is a seventh context line for numeric tokens.")
    protocol.add_context("This is an eighth context line for numeric tokens.")
    protocol.add_context("This is a ninth context line for numeric tokens.")
    protocol.add_context("This is a tenth context line for numeric tokens.")
    
    # Add instruction
    protocol.add_instruction(simple_numtoken_workflow_instruction_with_samples)
    
    return protocol


@pytest.fixture
def numlisttoken_protocol(simple_numlisttoken_workflow_instruction_with_samples) -> Protocol:
    """Protocol with NumListToken instruction."""
    protocol = Protocol("numlisttoken_protocol", inputs=2, encrypt=False)
    
    # Add context (minimum 10 lines total required)
    protocol.add_context("This protocol uses numeric list tokens.")
    protocol.add_context("This is a second context line for numeric list tokens.")
    protocol.add_context("This is a third context line for numeric list tokens.")
    protocol.add_context("This is a fourth context line for numeric list tokens.")
    protocol.add_context("This is a fifth context line for numeric list tokens.")
    protocol.add_context("This is a sixth context line for numeric list tokens.")
    protocol.add_context("This is a seventh context line for numeric list tokens.")
    protocol.add_context("This is an eighth context line for numeric list tokens.")
    protocol.add_context("This is a ninth context line for numeric list tokens.")
    protocol.add_context("This is a tenth context line for numeric list tokens.")
    
    # Add instruction
    protocol.add_instruction(simple_numlisttoken_workflow_instruction_with_samples)
    
    return protocol


@pytest.fixture
def mixed_numeric_protocol(mixed_instruction_2context_with_samples) -> Protocol:
    """Protocol with mixed numeric instruction."""
    protocol = Protocol("mixed_numeric", inputs=2, encrypt=False)
    
    # Add context (minimum 10 lines total required)
    protocol.add_context("This protocol uses mixed numeric tokens.")
    protocol.add_context("This is a second context line for mixed numeric tokens.")
    protocol.add_context("This is a third context line for mixed numeric tokens.")
    protocol.add_context("This is a fourth context line for mixed numeric tokens.")
    protocol.add_context("This is a fifth context line for mixed numeric tokens.")
    protocol.add_context("This is a sixth context line for mixed numeric tokens.")
    protocol.add_context("This is a seventh context line for mixed numeric tokens.")
    protocol.add_context("This is an eighth context line for mixed numeric tokens.")
    protocol.add_context("This is a ninth context line for mixed numeric tokens.")
    protocol.add_context("This is a tenth context line for mixed numeric tokens.")
    
    # Add instruction
    protocol.add_instruction(mixed_instruction_2context_with_samples)
    
    return protocol


@pytest.fixture
def user_mixed_protocol(user_mixed_instruction_2context_with_samples) -> Protocol:
    """Protocol with user mixed instruction."""
    protocol = Protocol("user_mixed", inputs=2, encrypt=False)
    
    # Add context (minimum 10 lines total required)
    protocol.add_context("This protocol uses user mixed tokens.")
    protocol.add_context("This is a second context line for user mixed tokens.")
    protocol.add_context("This is a third context line for user mixed tokens.")
    protocol.add_context("This is a fourth context line for user mixed tokens.")
    protocol.add_context("This is a fifth context line for user mixed tokens.")
    protocol.add_context("This is a sixth context line for user mixed tokens.")
    protocol.add_context("This is a seventh context line for user mixed tokens.")
    protocol.add_context("This is an eighth context line for user mixed tokens.")
    protocol.add_context("This is a ninth context line for user mixed tokens.")
    protocol.add_context("This is a tenth context line for user mixed tokens.")
    
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
    protocol = Protocol("multi_instruction", inputs=2, encrypt=False)
    
    # Add context (minimum 10 lines total required)
    protocol.add_context("This protocol has multiple instructions.")
    protocol.add_context("This is a second context line for multiple instructions.")
    protocol.add_context("This is a third context line for multiple instructions.")
    protocol.add_context("This is a fourth context line for multiple instructions.")
    protocol.add_context("This is a fifth context line for multiple instructions.")
    protocol.add_context("This is a sixth context line for multiple instructions.")
    protocol.add_context("This is a seventh context line for multiple instructions.")
    protocol.add_context("This is an eighth context line for multiple instructions.")
    protocol.add_context("This is a ninth context line for multiple instructions.")
    protocol.add_context("This is a tenth context line for multiple instructions.")
    
    # Add multiple instructions
    protocol.add_instruction(simple_workflow_instruction_with_samples)
    protocol.add_instruction(user_workflow_instruction_with_samples)
    protocol.add_instruction(simple_numtoken_workflow_instruction_with_samples)
    
    return protocol


@pytest.fixture
def encrypted_protocol(simple_workflow_instruction_with_samples) -> Protocol:
    """Encrypted protocol."""
    protocol = Protocol("encrypted_protocol", inputs=2, encrypt=True)
    
    # Add context (minimum 10 lines total required)
    protocol.add_context("This is an encrypted protocol.")
    protocol.add_context("This is a second context line for encrypted protocol.")
    protocol.add_context("This is a third context line for encrypted protocol.")
    protocol.add_context("This is a fourth context line for encrypted protocol.")
    protocol.add_context("This is a fifth context line for encrypted protocol.")
    protocol.add_context("This is a sixth context line for encrypted protocol.")
    protocol.add_context("This is a seventh context line for encrypted protocol.")
    protocol.add_context("This is an eighth context line for encrypted protocol.")
    protocol.add_context("This is a ninth context line for encrypted protocol.")
    protocol.add_context("This is a tenth context line for encrypted protocol.")
    
    # Add instruction
    protocol.add_instruction(simple_workflow_instruction_with_samples)
    
    return protocol


@pytest.fixture
def workflow_protocol(simple_workflow_instruction_with_samples, user_workflow_instruction_with_samples) -> Protocol:
    """Protocol with workflow instructions (2 context lines)."""
    protocol = Protocol("workflow_protocol", inputs=2, encrypt=False)
    
    # Add context (minimum 10 lines total required)
    protocol.add_context("This is workflow context line 1.")
    protocol.add_context("This is workflow context line 2.")
    protocol.add_context("This is workflow context line 3.")
    protocol.add_context("This is workflow context line 4.")
    protocol.add_context("This is workflow context line 5.")
    protocol.add_context("This is workflow context line 6.")
    protocol.add_context("This is workflow context line 7.")
    protocol.add_context("This is workflow context line 8.")
    protocol.add_context("This is workflow context line 9.")
    protocol.add_context("This is workflow context line 10.")
    
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
    protocol = Protocol("comprehensive", inputs=2, encrypt=False)
    
    # Add context (minimum 10 lines total required)
    protocol.add_context("This is a comprehensive protocol with all instruction types.")
    protocol.add_context("This is a second context line for comprehensive protocol.")
    protocol.add_context("This is a third context line for comprehensive protocol.")
    protocol.add_context("This is a fourth context line for comprehensive protocol.")
    protocol.add_context("This is a fifth context line for comprehensive protocol.")
    protocol.add_context("This is a sixth context line for comprehensive protocol.")
    protocol.add_context("This is a seventh context line for comprehensive protocol.")
    protocol.add_context("This is an eighth context line for comprehensive protocol.")
    protocol.add_context("This is a ninth context line for comprehensive protocol.")
    protocol.add_context("This is a tenth context line for comprehensive protocol.")
    
    # Add all instruction types
    protocol.add_instruction(simple_workflow_instruction_with_samples)
    protocol.add_instruction(user_workflow_instruction_with_samples)
    protocol.add_instruction(simple_numtoken_workflow_instruction_with_samples)
    
    return protocol


# 2 Context Line Workflow Protocols
@pytest.fixture
def workflow_2context_protocol(simple_workflow_2context_instruction_with_samples, user_workflow_2context_instruction_with_samples) -> Protocol:
    """Protocol with 2 context line workflow instructions."""
    protocol = Protocol("workflow_2context", inputs=2, encrypt=False)
    
    # Add context (minimum 10 lines total required)
    protocol.add_context("This is a 2 context line workflow protocol.")
    protocol.add_context("This is a second context line for 2 context workflow protocol.")
    protocol.add_context("This is a third context line for 2 context workflow protocol.")
    protocol.add_context("This is a fourth context line for 2 context workflow protocol.")
    protocol.add_context("This is a fifth context line for 2 context workflow protocol.")
    protocol.add_context("This is a sixth context line for 2 context workflow protocol.")
    protocol.add_context("This is a seventh context line for 2 context workflow protocol.")
    protocol.add_context("This is an eighth context line for 2 context workflow protocol.")
    protocol.add_context("This is a ninth context line for 2 context workflow protocol.")
    protocol.add_context("This is a tenth context line for 2 context workflow protocol.")
    
    # Add instructions
    protocol.add_instruction(simple_workflow_2context_instruction_with_samples)
    protocol.add_instruction(user_workflow_2context_instruction_with_samples)
    
    return protocol


@pytest.fixture
def numtoken_workflow_2context_protocol(simple_numtoken_workflow_2context_instruction_with_samples) -> Protocol:
    """Protocol with 2 context line NumToken workflow instruction."""
    protocol = Protocol("numtoken_workflow_2context", inputs=2, encrypt=False)
    
    # Add context (minimum 10 lines total required)
    protocol.add_context("This is a 2 context line NumToken workflow protocol.")
    protocol.add_context("This is a second context line for 2 context NumToken workflow protocol.")
    protocol.add_context("This is a third context line for 2 context NumToken workflow protocol.")
    protocol.add_context("This is a fourth context line for 2 context NumToken workflow protocol.")
    protocol.add_context("This is a fifth context line for 2 context NumToken workflow protocol.")
    protocol.add_context("This is a sixth context line for 2 context NumToken workflow protocol.")
    protocol.add_context("This is a seventh context line for 2 context NumToken workflow protocol.")
    protocol.add_context("This is an eighth context line for 2 context NumToken workflow protocol.")
    protocol.add_context("This is a ninth context line for 2 context NumToken workflow protocol.")
    protocol.add_context("This is a tenth context line for 2 context NumToken workflow protocol.")
    
    # Add instruction
    protocol.add_instruction(simple_numtoken_workflow_2context_instruction_with_samples)
    
    return protocol


# 5 Context Line Workflow Protocols
@pytest.fixture
def workflow_5context_protocol(simple_workflow_5context_instruction_with_samples, user_workflow_5context_instruction_with_samples) -> Protocol:
    """Protocol with 5 context line workflow instructions."""
    protocol = Protocol("workflow_5context", inputs=5, encrypt=False)
    
    # Add context (minimum 10 lines total required)
    protocol.add_context("This is a 5 context line workflow protocol.")
    protocol.add_context("This is a second context line for 5 context workflow protocol.")
    protocol.add_context("This is a third context line for 5 context workflow protocol.")
    protocol.add_context("This is a fourth context line for 5 context workflow protocol.")
    protocol.add_context("This is a fifth context line for 5 context workflow protocol.")
    protocol.add_context("This is a sixth context line for 5 context workflow protocol.")
    protocol.add_context("This is a seventh context line for 5 context workflow protocol.")
    protocol.add_context("This is an eighth context line for 5 context workflow protocol.")
    protocol.add_context("This is a ninth context line for 5 context workflow protocol.")
    protocol.add_context("This is a tenth context line for 5 context workflow protocol.")
    
    # Add instructions
    protocol.add_instruction(simple_workflow_5context_instruction_with_samples)
    protocol.add_instruction(user_workflow_5context_instruction_with_samples)
    
    return protocol


@pytest.fixture
def numtoken_workflow_5context_protocol(simple_numtoken_workflow_5context_instruction_with_samples) -> Protocol:
    """Protocol with 5 context line NumToken workflow instruction."""
    protocol = Protocol("numtoken_workflow_5context", inputs=5, encrypt=False)
    
    # Add context (minimum 10 lines total required)
    protocol.add_context("This is a 5 context line NumToken workflow protocol")
    protocol.add_context("This is a second context line for 5 context NumToken workflow protocol.")
    protocol.add_context("This is a third context line for 5 context NumToken workflow protocol.")
    protocol.add_context("This is a fourth context line for 5 context NumToken workflow protocol.")
    protocol.add_context("This is a fifth context line for 5 context NumToken workflow protocol.")
    protocol.add_context("This is a sixth context line for 5 context NumToken workflow protocol.")
    protocol.add_context("This is a seventh context line for 5 context NumToken workflow protocol.")
    protocol.add_context("This is an eighth context line for 5 context NumToken workflow protocol.")
    protocol.add_context("This is a ninth context line for 5 context NumToken workflow protocol.")
    protocol.add_context("This is a tenth context line for 5 context NumToken workflow protocol.")
    
    # Add instruction
    protocol.add_instruction(simple_numtoken_workflow_5context_instruction_with_samples)
    
    return protocol
