"""
Test JSON creation for basic simple protocol.
"""
import pytest
from model_train_protocol import Protocol


class TestBasicSimpleProtocolJSON:
    """Test JSON structure and content for basic simple protocol."""

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

    def test_basic_simple_protocol_json_structure(self, basic_simple_protocol):
        """Test that the JSON has the correct top-level structure."""
        # Get the JSON output
        json_output = self._get_json_output(basic_simple_protocol)
        
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

    def test_basic_simple_protocol_name(self, basic_simple_protocol):
        """Test that the protocol name is correct."""
        json_output = self._get_json_output(basic_simple_protocol)
        
        assert json_output["name"] == "basic_simple"

    def test_basic_simple_protocol_context(self, basic_simple_protocol):
        """Test that the context is correctly included."""
        json_output = self._get_json_output(basic_simple_protocol)
        
        assert "context" in json_output
        assert isinstance(json_output["context"], list)
        assert len(json_output["context"]) == 2
        assert json_output["context"][0] == "This is a basic context line."
        assert json_output["context"][1] == "This is a second basic context line."

    def test_basic_simple_protocol_tokens(self, basic_simple_protocol):
        """Test that tokens are correctly included."""
        json_output = self._get_json_output(basic_simple_protocol)
        
        assert "tokens" in json_output
        assert isinstance(json_output["tokens"], dict)
        
        # Check that we have the expected tokens (with underscores)
        token_keys = set(json_output["tokens"].keys())
        expected_tokens = {"Tree_", "English_", "Cat_", "Talk_", "Result_"}
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

    def test_basic_simple_protocol_special_tokens(self, basic_simple_protocol):
        """Test that special tokens are correctly included."""
        json_output = self._get_json_output(basic_simple_protocol)
        
        assert "special_tokens" in json_output
        assert isinstance(json_output["special_tokens"], list)
        
        # Should include instruction tokens
        assert len(json_output["special_tokens"]) > 0
        assert all(isinstance(token, str) for token in json_output["special_tokens"])

    def test_basic_simple_protocol_special_tokens_unique(self, basic_simple_protocol):
        """Test that special tokens are unique with no duplicates."""
        json_output = self._get_json_output(basic_simple_protocol)

        special_tokens = json_output["special_tokens"]
        
        # Check for duplicates
        assert len(special_tokens) == len(set(special_tokens)), "Special tokens contain duplicates"
        
        # Check that all special tokens are unique
        seen = set()
        for token in special_tokens:
            assert token not in seen, f"Duplicate special token found: {token}"
            seen.add(token)

    def test_basic_simple_protocol_special_token_format(self, basic_simple_protocol):
        """Test that special tokens have the exact format specified."""
        json_output = self._get_json_output(basic_simple_protocol)

        tokens = json_output["tokens"]
        
        # Expected special tokens with their exact format
        expected_special_tokens = {
            "<BOS>": {
                "desc": None,
                "emoji": "🏁",
                "num": False,
                "special": "start",
                "user": False
            },
            "<EOS>": {
                "desc": None,
                "emoji": "🎬",
                "num": False,
                "special": "end",
                "user": False
            },
            "<PAD>": {
                "desc": None,
                "emoji": "🗒",
                "num": False,
                "special": "pad",
                "user": False
            },
            "<RUN>": {
                "desc": None,
                "emoji": "🏃",
                "num": False,
                "special": "infer",
                "user": False
            },
            "<UNK>": {
                "desc": None,
                "emoji": "🛑",
                "num": False,
                "special": "unknown",
                "user": False
            }
        }
        
        # Check that all expected special tokens are present
        for token_key, expected_format in expected_special_tokens.items():
            assert token_key in tokens, f"Special token {token_key} not found in tokens"
            
            actual_token = tokens[token_key]
            
            # Check each field matches exactly
            for field, expected_value in expected_format.items():
                assert field in actual_token, f"Field {field} missing from {token_key}"
                assert actual_token[field] == expected_value, f"Field {field} in {token_key} has value {actual_token[field]}, expected {expected_value}"
        
        # Check that no unexpected special tokens exist
        special_token_keys = {key for key, value in tokens.items() if value.get("special") is not None}
        expected_special_keys = set(expected_special_tokens.keys())
        assert special_token_keys == expected_special_keys, f"Unexpected special tokens found: {special_token_keys - expected_special_keys}"

    def test_basic_simple_protocol_instruction(self, basic_simple_protocol):
        """Test that instruction structure is correct."""
        json_output = self._get_json_output(basic_simple_protocol)
        
        assert "instruction" in json_output
        instruction = json_output["instruction"]
        
        # Test instruction top-level keys
        assert "memory" in instruction
        assert "sets" in instruction
        
        # Test memory (should be instruction_context_snippets + 1)
        assert instruction["memory"] == 3  # 2 context lines + 1 response line
        
        # Test sets structure
        assert isinstance(instruction["sets"], list)
        assert len(instruction["sets"]) == 1  # One instruction set
        
        instruction_set = instruction["sets"][0]
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
        assert len(instruction_set["set"]) == 3  # Three context lines (2 context + 1 response)
        assert isinstance(instruction_set["set"][0], list)
        assert isinstance(instruction_set["set"][1], list)
        assert isinstance(instruction_set["set"][2], list)
        assert len(instruction_set["set"][0]) > 0  # Should have tokens
        assert len(instruction_set["set"][1]) > 0  # Should have tokens
        assert len(instruction_set["set"][2]) > 0  # Should have tokens
        
        # Test result
        assert isinstance(instruction_set["result"], str)
        assert instruction_set["result"] == "Result_"
        
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
        assert sample["prompt"] is None or isinstance(sample["prompt"], str)
        assert sample["number"] is None or isinstance(sample["number"], list)
        assert isinstance(sample["result"], str)
        assert isinstance(sample["value"], str)
        
        # Test sample content
        assert len(sample["sample"]) == 3  # Three context snippets (2 context + 1 response)
        assert sample["number"] is None or len(sample["number"]) == 0  # No numeric tokens
        assert sample["result"] == "Result_"
        assert sample["value"] == "None"  # No value for simple instruction

    def test_basic_simple_protocol_empty_guardrails(self, basic_simple_protocol):
        """Test that guardrails are correctly included."""
        json_output = self._get_json_output(basic_simple_protocol)
        
        # Basic simple protocol should have no guardrails (except None key)
        assert "guardrails" in json_output
        assert isinstance(json_output["guardrails"], dict)
        assert len(json_output["guardrails"]) == 1
        assert "None" in json_output["guardrails"]
        assert len(json_output["guardrails"]) == 1

    def test_basic_simple_protocol_one_guardrail(self, basic_simple_protocol_with_guardrail):
        """Test that guardrails are correctly included."""
        json_output = self._get_json_output(basic_simple_protocol_with_guardrail)

        # Simple protocols should never have a guardrail (except None key) as the response is from a non-user TokenSet
        assert "guardrails" in json_output
        assert isinstance(json_output["guardrails"], dict)
        assert len(json_output["guardrails"]) == 1
        assert "None" in json_output["guardrails"]
        assert len(json_output["guardrails"]) == 1

    def test_basic_simple_protocol_numbers(self, basic_simple_protocol):
        """Test that numbers are correctly included."""
        json_output = self._get_json_output(basic_simple_protocol)
        
        assert "numbers" in json_output
        assert isinstance(json_output["numbers"], dict)
        
        # Basic simple protocol should have no numeric tokens (except None key)
        assert len(json_output["numbers"]) == 1
        assert "None" in json_output["numbers"]

    def test_basic_simple_protocol_batches(self, basic_simple_protocol):
        """Test that batches are correctly included."""
        json_output = self._get_json_output(basic_simple_protocol)
        
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
        
        # Basic protocol should have no batches
        assert len(batches["pretrain"]) == 0
        assert len(batches["instruct"]) == 0
        assert len(batches["judge"]) == 0
        assert len(batches["ppo"]) == 0

    def test_basic_simple_protocol_token_descriptions(self, basic_simple_protocol):
        """Test that token descriptions are correctly included."""
        json_output = self._get_json_output(basic_simple_protocol)
        
        tokens = json_output["tokens"]
        
        # Check specific token descriptions
        if "Tree" in tokens:
            assert tokens["Tree"]["desc"] == "A tree token"
        if "English" in tokens:
            assert tokens["English"]["desc"] == "English language token"
        if "Cat" in tokens:
            assert tokens["Cat"]["desc"] == "A cat token"
        if "Talk" in tokens:
            assert tokens["Talk"]["desc"] == "A talk token"
        if "Result" in tokens:
            assert tokens["Result"]["desc"] == "Result token"

    def test_basic_simple_protocol_token_types(self, basic_simple_protocol):
        """Test that token types are correctly set."""
        json_output = self._get_json_output(basic_simple_protocol)
        
        tokens = json_output["tokens"]
        
        # Check token types - some tokens may be user tokens
        for token_key, token_info in tokens.items():
            if token_key in ["<BOS>", "<EOS>", "<PAD>", "<RUN>", "<UNK>"]:
                # Special tokens
                assert token_info["special"] is not None
            elif token_key == "Alice_":
                # User token
                assert token_info["user"] is True
                assert token_info["num"] is False
                assert token_info["special"] is None
            else:
                # Regular tokens
                assert token_info["num"] is False
                assert token_info["user"] is False
                assert token_info["special"] is None
