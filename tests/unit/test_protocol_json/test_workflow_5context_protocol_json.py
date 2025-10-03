"""
Test JSON creation for workflow protocol with 5 context lines.
"""
import pytest
from model_train_protocol import Protocol


class TestWorkflow5ContextProtocolJSON:
    """Test JSON structure and content for workflow protocol with 5 context lines."""

    def _get_json_output(self, protocol):
        """Helper method to get JSON output from a protocol."""
        protocol._prep_protocol()
        from model_train_protocol._internal.ProtocolFile import ProtocolFile
        protocol_file = ProtocolFile(
            name=protocol.name,
            context=protocol.context,
            instruction_context_snippets=protocol.instruction_context_snippets,
            tokens=protocol.tokens,
            special_tokens=protocol.special_tokens,
            instructions=protocol.instructions
        )
        return protocol_file.to_json()

    def test_workflow_5context_protocol_json_structure(self, workflow_5context_protocol):
        """Test that the JSON has the correct top-level structure."""
        # Get the JSON output
        json_output = self._get_json_output(workflow_5context_protocol)
        
        # Test top-level keys
        assert "name" in json_output
        assert "context" in json_output
        assert "tokens" in json_output
        assert "special_tokens" in json_output
        assert "instruction" in json_output
        assert "guardrails" in json_output
        assert "numbers" in json_output
        assert "batches" in json_output
        
        # Test that no unexpected keys are present
        expected_keys = {"name", "context", "tokens", "special_tokens", "instruction", "guardrails", "numbers", "batches"}
        actual_keys = set(json_output.keys())
        assert actual_keys == expected_keys

    def test_workflow_5context_protocol_name(self, workflow_5context_protocol):
        """Test that the protocol name is correct."""
        json_output = self._get_json_output(workflow_5context_protocol)
        
        assert json_output["name"] == "workflow_5context"

    def test_workflow_5context_protocol_context(self, workflow_5context_protocol):
        """Test that the context is correctly included."""
        json_output = self._get_json_output(workflow_5context_protocol)
        
        assert "context" in json_output
        assert isinstance(json_output["context"], list)
        assert len(json_output["context"]) == 5
        assert json_output["context"][0] == "This is a 5 context line workflow protocol."
        assert json_output["context"][1] == "This is the second context line for the workflow protocol."
        assert json_output["context"][2] == "This is the third context line for the workflow protocol."
        assert json_output["context"][3] == "This is the fourth context line for the workflow protocol."
        assert json_output["context"][4] == "This is the fifth context line for the workflow protocol."

    def test_workflow_5context_protocol_tokens(self, workflow_5context_protocol):
        """Test that tokens are correctly included."""
        json_output = self._get_json_output(workflow_5context_protocol)
        
        assert "tokens" in json_output
        assert isinstance(json_output["tokens"], dict)
        
        # Check that we have the expected tokens
        token_keys = set(json_output["tokens"].keys())
        expected_tokens = {"Tree_", "English_", "Cat_", "Talk_", "Result_", "Alice_", "End_"}
        assert expected_tokens.issubset(token_keys)
        
        # Test token structure
        for token_key, token_info in json_output["tokens"].items():
            assert "emoji" in token_info
            assert "num" in token_info
            assert "user" in token_info
            assert "desc" in token_info
            assert "special" in token_info
            
            # Check data types
            assert isinstance(token_info["emoji"], str)
            assert isinstance(token_info["num"], bool)
            assert isinstance(token_info["user"], bool)
            assert token_info["desc"] is None or isinstance(token_info["desc"], str)
            assert token_info["special"] is None or isinstance(token_info["special"], str)

    def test_workflow_5context_protocol_token_types(self, workflow_5context_protocol):
        """Test that token types are correctly set."""
        json_output = self._get_json_output(workflow_5context_protocol)
        
        tokens = json_output["tokens"]
        
        # Check specific token types
        for token_key, token_info in tokens.items():
            if token_key == "Alice_":
                assert token_info["user"] is True
                assert token_info["num"] is False
            elif token_key not in ["<BOS>", "<EOS>", "<PAD>", "<RUN>", "<UNK>"]:
                assert token_info["user"] is False
                assert token_info["num"] is False
            assert isinstance(token_info["special"], (str, type(None)))

    def test_workflow_5context_protocol_special_tokens(self, workflow_5context_protocol):
        """Test that special tokens are correctly included."""
        json_output = self._get_json_output(workflow_5context_protocol)
        
        assert "special_tokens" in json_output
        assert isinstance(json_output["special_tokens"], list)
        
        # Should include instruction tokens
        assert len(json_output["special_tokens"]) > 0
        assert all(isinstance(token, str) for token in json_output["special_tokens"])

    def test_workflow_5context_protocol_instruction(self, workflow_5context_protocol):
        """Test that instruction structure is correct."""
        json_output = self._get_json_output(workflow_5context_protocol)
        
        assert "instruction" in json_output
        instruction = json_output["instruction"]
        
        # Test instruction top-level keys
        assert "memory" in instruction
        assert "sets" in instruction
        
        # Test memory (should be instruction_context_snippets + 1)
        assert instruction["memory"] == 6  # 5 context lines + 1 response line
        
        # Test sets structure
        assert isinstance(instruction["sets"], list)
        assert len(instruction["sets"]) == 2  # Two instruction sets
        
        for instruction_set in instruction["sets"]:
            self._test_instruction_set_structure(instruction_set)

    def _test_instruction_set_structure(self, instruction_set):
        """Test the structure of an instruction set."""
        # Test instruction set keys
        assert "set" in instruction_set
        assert "result" in instruction_set
        assert "samples" in instruction_set
        assert "ppo" in instruction_set
        
        # Test set structure (context tokens)
        assert isinstance(instruction_set["set"], list)
        assert len(instruction_set["set"]) == 6  # Six context lines (5 context + 1 response)
        for i in range(5):
            assert isinstance(instruction_set["set"][i], list)
            assert len(instruction_set["set"][i]) > 0  # Should have tokens
        
        # Test result
        assert isinstance(instruction_set["result"], str)
        assert instruction_set["result"] in ["Result_", "End_"]
        
        # Test samples
        assert isinstance(instruction_set["samples"], list)
        assert len(instruction_set["samples"]) == 3  # Should have 3 samples
        
        for sample in instruction_set["samples"]:
            self._test_sample_structure(sample)
        
        # Test ppo
        assert isinstance(instruction_set["ppo"], list)

    def _test_sample_structure(self, sample):
        """Test the structure of a sample."""
        # Test sample keys
        assert "sample" in sample
        assert "prompt" in sample
        assert "number" in sample
        assert "result" in sample
        assert "value" in sample
        
        # Test sample data types
        assert isinstance(sample["sample"], list)
        assert isinstance(sample["prompt"], (str, type(None)))
        assert isinstance(sample["number"], (list, type(None)))
        assert isinstance(sample["result"], str)
        assert isinstance(sample["value"], (str, int, float, type(None)))
        
        # Test sample content
        assert len(sample["sample"]) == 6  # Six context snippets (5 context + 1 response)
        assert sample["result"] in ["Result_", "End_"]
        assert sample["value"] == "None"  # No value for workflow instructions
        
        # User instruction should have prompts
        if sample["result"] == "End_":
            assert len(sample["prompt"]) > 0

    def test_workflow_5context_protocol_guardrails(self, workflow_5context_protocol):
        """Test that guardrails are correctly included."""
        json_output = self._get_json_output(workflow_5context_protocol)
        
        assert "guardrails" in json_output
        assert isinstance(json_output["guardrails"], dict)
        assert len(json_output["guardrails"]) == 1
        assert "None" in json_output["guardrails"]

    def test_workflow_5context_protocol_numbers(self, workflow_5context_protocol):
        """Test that numbers are correctly included."""
        json_output = self._get_json_output(workflow_5context_protocol)
        
        assert "numbers" in json_output
        assert isinstance(json_output["numbers"], dict)
        
        # Workflow protocol should have no numeric tokens
        assert len(json_output["numbers"]) == 1
        assert "None" in json_output["numbers"]

    def test_workflow_5context_protocol_batches(self, workflow_5context_protocol):
        """Test that batches are correctly included."""
        json_output = self._get_json_output(workflow_5context_protocol)
        
        assert "batches" in json_output
        batches = json_output["batches"]
        
        # Test batch structure
        assert "pretrain" in batches
        assert "instruct" in batches
        assert "judge" in batches
        assert "ppo" in batches
        
        # Test batch data types
        assert isinstance(batches["pretrain"], list)
        assert isinstance(batches["instruct"], list)
        assert isinstance(batches["judge"], list)
        assert isinstance(batches["ppo"], list)
        
        # Workflow protocol should have no batches
        assert len(batches["pretrain"]) == 0
        assert len(batches["instruct"]) == 0
        assert len(batches["judge"]) == 0
        assert len(batches["ppo"]) == 0

    def test_workflow_5context_protocol_instruction_sets_order(self, workflow_5context_protocol):
        """Test that instruction sets are in the correct order."""
        json_output = self._get_json_output(workflow_5context_protocol)
        
        instruction_sets = json_output["instruction"]["sets"]
        
        # Should have 2 instruction sets
        assert len(instruction_sets) == 2
        
        # First set should be user instruction (End_) - alphabetically before Result_
        assert instruction_sets[0]["result"] == "End_"
        
        # Second set should be simple instruction (Result_)
        assert instruction_sets[1]["result"] == "Result_"

    def test_workflow_5context_protocol_instruction_context_snippets(self, workflow_5context_protocol):
        """Test that the protocol correctly handles 5 context lines."""
        json_output = self._get_json_output(workflow_5context_protocol)
        
        # Memory should be instruction_context_snippets + 1
        assert json_output["instruction"]["memory"] == 6
        
        # Each instruction set should have 6 context lines (5 context + 1 response)
        for instruction_set in json_output["instruction"]["sets"]:
            assert len(instruction_set["set"]) == 6
            
            # Each sample should have 6 context snippets (5 context + 1 response)
            for sample in instruction_set["samples"]:
                assert len(sample["sample"]) == 6


class TestNumTokenWorkflow5ContextProtocolJSON:
    """Test JSON structure and content for NumToken workflow protocol with 5 context lines."""

    def _get_json_output(self, protocol):
        """Helper method to get JSON output from a protocol."""
        protocol._prep_protocol()
        from model_train_protocol._internal.ProtocolFile import ProtocolFile
        protocol_file = ProtocolFile(
            name=protocol.name,
            context=protocol.context,
            instruction_context_snippets=protocol.instruction_context_snippets,
            tokens=protocol.tokens,
            special_tokens=protocol.special_tokens,
            instructions=protocol.instructions
        )
        return protocol_file.to_json()

    def test_numtoken_workflow_5context_protocol_json_structure(self, numtoken_workflow_5context_protocol):
        """Test that the JSON has the correct top-level structure."""
        # Get the JSON output
        json_output = self._get_json_output(numtoken_workflow_5context_protocol)
        
        # Test top-level keys
        assert "name" in json_output
        assert "context" in json_output
        assert "tokens" in json_output
        assert "special_tokens" in json_output
        assert "instruction" in json_output
        assert "guardrails" in json_output
        assert "numbers" in json_output
        assert "batches" in json_output

    def test_numtoken_workflow_5context_protocol_name(self, numtoken_workflow_5context_protocol):
        """Test that the protocol name is correct."""
        json_output = self._get_json_output(numtoken_workflow_5context_protocol)
        
        assert json_output["name"] == "numtoken_workflow_5context"

    def test_numtoken_workflow_5context_protocol_context(self, numtoken_workflow_5context_protocol):
        """Test that the context is correctly included."""
        json_output = self._get_json_output(numtoken_workflow_5context_protocol)
        
        assert "context" in json_output
        assert isinstance(json_output["context"], list)
        assert len(json_output["context"]) == 5
        assert json_output["context"][0] == "This is a 5 context line NumToken workflow protocol"
        assert json_output["context"][1] == "This is the second context line for the NumToken workflow protocol."
        assert json_output["context"][2] == "This is the third context line for the NumToken workflow protocol."
        assert json_output["context"][3] == "This is the fourth context line for the NumToken workflow protocol."
        assert json_output["context"][4] == "This is the fifth context line for the NumToken workflow protocol."

    def test_numtoken_workflow_5context_protocol_tokens(self, numtoken_workflow_5context_protocol):
        """Test that tokens are correctly included."""
        json_output = self._get_json_output(numtoken_workflow_5context_protocol)
        
        assert "tokens" in json_output
        assert isinstance(json_output["tokens"], dict)
        
        # Check that we have the expected tokens
        token_keys = set(json_output["tokens"].keys())
        expected_tokens = {"Tree_", "English_", "Cat_", "Talk_", "Count_", "Alice_"}
        assert expected_tokens.issubset(token_keys)

    def test_numtoken_workflow_5context_protocol_numeric_tokens(self, numtoken_workflow_5context_protocol):
        """Test that numeric tokens are correctly identified."""
        json_output = self._get_json_output(numtoken_workflow_5context_protocol)
        
        tokens = json_output["tokens"]
        
        # Count should be marked as a numeric token
        if "Count" in tokens:
            assert tokens["Count"]["num"] is True
            assert tokens["Count"]["user"] is False

    def test_numtoken_workflow_5context_protocol_instruction(self, numtoken_workflow_5context_protocol):
        """Test that instruction structure is correct."""
        json_output = self._get_json_output(numtoken_workflow_5context_protocol)
        
        assert "instruction" in json_output
        instruction = json_output["instruction"]
        
        # Test memory (should be instruction_context_snippets + 1)
        assert instruction["memory"] == 6  # 5 context lines + 1 response line
        
        # Test sets structure
        assert isinstance(instruction["sets"], list)
        assert len(instruction["sets"]) == 1  # One instruction set
        
        instruction_set = instruction["sets"][0]
        assert len(instruction_set["set"]) == 6  # Six context lines (5 context + 1 response)
        assert instruction_set["result"] == "Count_"
        
        # Test samples
        for sample in instruction_set["samples"]:
            assert len(sample["sample"]) == 6  # Six context snippets (5 context + 1 response)
            assert len(sample["number"]) == 6  # Six numeric values (5 context + 1 response)
            assert sample["result"] == "Count_"
            assert sample["value"] in [10, 15, 20]

    def test_numtoken_workflow_5context_protocol_numbers(self, numtoken_workflow_5context_protocol):
        """Test that numbers are correctly included."""
        json_output = self._get_json_output(numtoken_workflow_5context_protocol)
        
        assert "numbers" in json_output
        assert isinstance(json_output["numbers"], dict)
        
        # Should have numeric tokens
        assert len(json_output["numbers"]) > 0
        
        # Check that Count token is in numbers
        if "Count" in json_output["numbers"]:
            count_info = json_output["numbers"]["Count"]
            assert "min" in count_info
            assert "max" in count_info
            assert "desc" in count_info
