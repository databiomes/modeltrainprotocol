"""
Sample protocols for testing.
"""
import pytest

from model_train_protocol import Protocol, UserInstruction, SimpleInstruction
from tests.fixtures.correct_protocol_utils import add_context_to_protocol, create_user_instruction, create_simple_instruction

@pytest.fixture()
def comprehensive_protocol(name: str = "example_protocol",
                                  context_lines: int = 2, encrypt: bool = False) -> Protocol:
    """Create a comprehensive example protocol with all components for testing."""
    protocol: Protocol = Protocol(name=name, context_lines=context_lines, encrypt=encrypt)
    add_context_to_protocol(protocol)

    comprehensive_simple_instruction: SimpleInstruction = create_simple_instruction(
        add_num_token=True, add_num_list_token=True
    )

    protocol.add_instruction(comprehensive_simple_instruction)

    comprehensive_user_instruction: UserInstruction = create_user_instruction(
        add_num_token=True, add_num_list_token=True, add_guardrail=True
    )

    protocol.add_instruction(comprehensive_user_instruction)

    return protocol
