"""
Integration tests for file operations.
"""
import json
from pathlib import Path

import pytest

from model_train_protocol import Protocol


class TestFileOperations:
    """Integration tests for file operations."""

    def test_protocol_save_basic(self, temp_directory, simple_workflow_instruction_with_samples):
        """Test basic protocol saving."""
        protocol: Protocol = Protocol(name="file_test", context_snippets=2, encrypt=False)
        protocol.add_instruction(simple_workflow_instruction_with_samples)

        # Save protocol
        protocol.save(name="test_save", path=str(temp_directory))

        # Check files were created
        model_file = temp_directory / "test_save_model.json"
        assert model_file.exists()

        # Check file content
        with open(model_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert data["name"] == "file_test"

    def test_protocol_template_basic(self, temp_directory, simple_workflow_instruction_with_samples):
        """Test basic protocol templating."""
        protocol: Protocol = Protocol(name="file_test", context_snippets=2, encrypt=False)
        protocol.add_instruction(simple_workflow_instruction_with_samples)

        # Create template
        protocol.template(path=str(temp_directory))

        # Check files were created
        template_file = temp_directory / "file_test_template.json"
        assert template_file.exists()

        # Check file content
        with open(template_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Template files have different structure - check for expected keys
        assert "example_usage" in data
        assert "tokens" in data
        assert "instructions" in data

    def test_protocol_template(self, temp_directory, user_workflow_instruction_with_samples):
        """Test protocol template with guardrails."""
        protocol = Protocol("guardrail_test", context_snippets=2)
        protocol.add_instruction(user_workflow_instruction_with_samples)

        # Create template
        protocol.template(path=str(temp_directory))

        # Check file was created
        template_file = temp_directory / "guardrail_test_template.json"
        assert template_file.exists()

        # Check file content
        with open(template_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Template files have different structure - check for expected keys
        assert "example_usage" in data
        assert "tokens" in data
        assert "instructions" in data

    def test_protocol_save_with_numeric_tokens(self, temp_directory, simple_workflow_instruction_with_samples):
        """Test protocol saving with numeric tokens."""
        protocol = Protocol("numeric_test", context_snippets=2)
        protocol.add_instruction(simple_workflow_instruction_with_samples)

        # Save protocol
        protocol.save(name="numeric_save", path=str(temp_directory))

        # Check file was created
        model_file = temp_directory / "numeric_save_model.json"
        assert model_file.exists()

        # Check file content
        with open(model_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert data["name"] == "numeric_test"
        assert len(data["numbers"]) >= 0

    def test_protocol_save_encrypted(self, temp_directory, simple_workflow_instruction_with_samples):
        """Test protocol saving with encryption."""
        protocol = Protocol("encrypted_test", context_snippets=2, encrypt=True)
        protocol.add_instruction(simple_workflow_instruction_with_samples)

        # Save protocol
        protocol.save(name="encrypted_save", path=str(temp_directory))

        # Check file was created
        model_file = temp_directory / "encrypted_save_model.json"
        assert model_file.exists()

        # Check file content
        with open(model_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert data["name"] == "encrypted_test"
        assert len(data["tokens"]) >= 2

    def test_protocol_save_unencrypted(self, temp_directory, simple_workflow_instruction_with_samples):
        """Test protocol saving without encryption."""
        protocol = Protocol("unencrypted_test", context_snippets=2, encrypt=False)
        protocol.add_instruction(simple_workflow_instruction_with_samples)

        # Save protocol
        protocol.save(name="unencrypted_save", path=str(temp_directory))

        # Check file was created
        model_file = temp_directory / "unencrypted_save_model.json"
        assert model_file.exists()

        # Check file content
        with open(model_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert data["name"] == "unencrypted_test"
        assert len(data["tokens"]) >= 2

    def test_protocol_save_multiple_instructions(self, temp_directory, user_workflow_instruction_with_samples, simple_workflow_instruction_with_samples):
        """Test protocol saving with multiple instructions."""
        protocol = Protocol("multi_instruction_test", context_snippets=2)
        protocol.add_instruction(user_workflow_instruction_with_samples)
        protocol.add_instruction(simple_workflow_instruction_with_samples)

        # Save protocol
        protocol.save(name="multi_save", path=str(temp_directory))

        # Check file was created
        model_file = temp_directory / "multi_save_model.json"
        assert model_file.exists()

        # Check file content
        with open(model_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert data["name"] == "multi_instruction_test"
        assert len(data["instruction"]) == 2

    def test_protocol_save_default_path(self, simple_workflow_instruction_with_samples):
        """Test protocol saving with default path."""
        protocol = Protocol("default_path_test", context_snippets=2)
        protocol.add_instruction(simple_workflow_instruction_with_samples)

        # Save protocol with default path
        protocol.save(name="default_path_save")

        # Check file was created in current directory
        model_file = Path("default_path_save_model.json")
        assert model_file.exists()

        # Clean up
        model_file.unlink()

    def test_protocol_template_default_path(self, simple_workflow_instruction_with_samples):
        """Test protocol templating with default path."""
        protocol = Protocol("default_template_test", context_snippets=2)
        protocol.add_instruction(simple_workflow_instruction_with_samples)

        # Create template with default path
        protocol.template()

        # Check file was created in current directory
        template_file = Path("default_template_test_template.json")
        assert template_file.exists()

        # Clean up
        template_file.unlink()

    def test_protocol_save_error_handling(self, temp_directory):
        """Test protocol saving error handling."""
        protocol = Protocol("error_test", context_snippets=2)

        # Add context but no instructions
        protocol.add_context("Context line 1")
        protocol.add_context("Context line 2")

        # Should raise error when trying to save without instructions
        with pytest.raises(ValueError, match="No instructions have been added"):
            protocol.save(name="error_save", path=str(temp_directory))

    def test_protocol_template_error_handling(self, temp_directory):
        """Test protocol templating error handling."""
        protocol = Protocol("template_error_test", context_snippets=2)

        # Add context but no instructions
        protocol.add_context("Context line 1")
        protocol.add_context("Context line 2")

        # Should raise error when trying to create template without instructions
        with pytest.raises(ValueError, match="No instructions have been added"):
            protocol.template(path=str(temp_directory))
