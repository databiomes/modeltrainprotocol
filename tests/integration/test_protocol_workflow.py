"""
Integration tests for complete protocol workflows.
"""
import pytest

from model_train_protocol import Protocol


class TestProtocolWorkflow:
    """Integration tests for complete protocol workflows."""

    def test_complete_protocol_creation(self, simple_workflow_instruction_with_samples, user_workflow_instruction_with_samples):
        """Test creating a complete protocol with all components using fixtures."""
        protocol = Protocol("integration_test", context_lines=2)
        
        # Add context
        protocol.add_context("This is a test context line 1")
        protocol.add_context("This is a test context line 2")
        
        # Add instructions to protocol
        protocol.add_instruction(simple_workflow_instruction_with_samples)
        protocol.add_instruction(user_workflow_instruction_with_samples)
        
        # Verify protocol state
        assert len(protocol.instructions) == 2
        assert len(protocol.tokens) >= 6  # Should include all tokens
        assert len(protocol.context) == 2
        assert protocol.name == "integration_test"
        assert protocol.context_lines == 2

    def test_protocol_with_numeric_tokens(self, simple_numtoken_workflow_instruction_with_samples):
        """Test creating a protocol with numeric tokens using fixtures."""
        protocol = Protocol("numeric_test", context_lines=2)
        
        # Add context
        protocol.add_context("This protocol uses numeric tokens.")
        protocol.add_context("Numbers are important for calculations.")
        
        protocol.add_instruction(simple_numtoken_workflow_instruction_with_samples)
        
        # Verify protocol state
        assert len(protocol.instructions) == 1
        assert len(protocol.tokens) >= 3
        assert protocol.name == "numeric_test"

    def test_protocol_save_and_load_workflow(self, temp_directory, simple_workflow_instruction_with_samples):
        """Test complete save and load workflow using fixtures."""
        protocol = Protocol("save_test", context_lines=2)
        
        # Add context
        protocol.add_context("Context line 1")
        protocol.add_context("Context line 2")
        
        protocol.add_instruction(simple_workflow_instruction_with_samples)
        
        # Save protocol
        protocol.save(path=str(temp_directory))
        
        # Create template
        protocol.template(path=str(temp_directory))
        
        # Check files were created
        model_file = temp_directory / "save_test_model.json"
        template_file = temp_directory / "save_test_template.json"
        
        assert model_file.exists()
        assert template_file.exists()

    def test_protocol_with_guardrails_workflow(self, user_workflow_instruction_with_samples):
        """Test protocol workflow with guardrails using fixtures."""
        protocol = Protocol("guardrail_test", context_lines=2)
        
        # Add context
        protocol.add_context("This protocol uses guardrails.")
        protocol.add_context("Guardrails provide safety mechanisms.")
        
        protocol.add_instruction(user_workflow_instruction_with_samples)
        
        # Verify protocol state
        assert len(protocol.instructions) == 1
        assert len(protocol.tokens) >= 3

    def test_protocol_encryption_workflow(self, simple_workflow_instruction_with_samples):
        """Test protocol workflow with encryption using fixtures."""
        protocol = Protocol("encryption_test", context_lines=2, encrypt=True)
        
        # Add context
        protocol.add_context("This protocol uses encryption.")
        protocol.add_context("Keys are generated automatically.")
        
        protocol.add_instruction(simple_workflow_instruction_with_samples)
        
        # Verify protocol state
        assert len(protocol.instructions) == 1
        assert len(protocol.tokens) >= 3
        assert protocol.encrypt is True

    def test_protocol_unencrypted_workflow(self, simple_workflow_instruction_with_samples):
        """Test protocol workflow without encryption using fixtures."""
        protocol = Protocol("unencrypted_test", context_lines=2, encrypt=False)
        
        # Add context
        protocol.add_context("This protocol does not use encryption.")
        protocol.add_context("Keys match token values.")
        
        protocol.add_instruction(simple_workflow_instruction_with_samples)
        
        # Verify protocol state
        assert len(protocol.instructions) == 1
        assert len(protocol.tokens) >= 3
        assert protocol.encrypt is False

    def test_protocol_multiple_instructions_workflow(self, simple_workflow_instruction_with_samples, user_workflow_instruction_with_samples):
        """Test protocol workflow with multiple instructions using fixtures."""
        protocol = Protocol("multi_instruction_test", context_lines=2)
        
        # Add context
        protocol.add_context("This protocol has multiple instructions.")
        protocol.add_context("Each instruction handles different scenarios.")
        
        # Add instructions to protocol
        protocol.add_instruction(simple_workflow_instruction_with_samples)
        protocol.add_instruction(user_workflow_instruction_with_samples)
        
        # Verify protocol state
        assert len(protocol.instructions) == 2
        assert len(protocol.tokens) >= 6

    def test_protocol_complex_workflow(self, simple_workflow_instruction_with_samples, user_workflow_instruction_with_samples, simple_numtoken_workflow_instruction_with_samples):
        """Test complex protocol workflow with all features using fixtures."""
        protocol = Protocol("complex_test", context_lines=2)
        
        # Add context
        protocol.add_context("This is a complex protocol with all features.")
        protocol.add_context("It includes tokens, instructions, and guardrails.")
        
        # Add instructions to protocol
        protocol.add_instruction(simple_workflow_instruction_with_samples)
        protocol.add_instruction(user_workflow_instruction_with_samples)
        protocol.add_instruction(simple_numtoken_workflow_instruction_with_samples)
        
        # Verify protocol state
        assert len(protocol.instructions) == 3
        assert len(protocol.tokens) >= 8
        assert len(protocol.context) == 2
        assert protocol.name == "complex_test"
        assert protocol.context_lines == 2

    def test_protocol_error_handling_workflow(self):
        """Test protocol workflow with error handling."""
        protocol = Protocol("error_test", context_lines=2)
        
        # Add context
        protocol.add_context("This protocol tests error handling.")
        protocol.add_context("It should handle errors gracefully.")
        
        # Test adding instruction without samples - create a simple instruction without samples
        from model_train_protocol import Token, TokenSet, SimpleInstruction
        
        token1 = Token("Token1", key="🔑")
        token2 = Token("Token2", key="🔧")
        context_set = TokenSet(tokens=(token1,))
        response_set = TokenSet(tokens=(token2,))
        
        # Create second context set
        context_set2 = TokenSet(tokens=(token2,))

        instruction: SimpleInstruction = SimpleInstruction(
            context=[context_set, context_set2],
            response=response_set,
            final=token2
        )

        # Attempt to add instruction without samples
        with pytest.raises(ValueError, match="Instruction must have at least three samples."):
            protocol.add_instruction(instruction)

    def test_protocol_validation_workflow(self, user_workflow_instruction_with_samples):
        """Test protocol workflow with validation using fixtures."""
        protocol = Protocol("validation_test", context_lines=2)
        
        # Add context
        protocol.add_context("This protocol tests validation.")
        protocol.add_context("It should validate all components.")
        
        protocol.add_instruction(user_workflow_instruction_with_samples)
        
        # Verify protocol state
        assert len(protocol.instructions) == 1
        assert len(protocol.tokens) >= 3
        assert protocol.name == "validation_test"
        assert protocol.context_lines == 2

