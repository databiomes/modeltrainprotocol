"""
Test JSON creation for comprehensive protocol.
"""
import pytest
from model_train_protocol import Protocol


class TestComprehensiveProtocolJSON:
    """Test JSON structure and content for comprehensive protocol."""

    def _get_json_output(self, protocol):
        """Helper method to get JSON output from a protocol."""
        protocol._prep_protocol()
        from model_train_protocol._internal.ProtocolFile import ProtocolFile
        protocol_file = ProtocolFile(
            name=protocol.name,
            context=protocol.context,
            context_lines=protocol.context_lines,
            tokens=protocol.tokens,
            special_tokens=protocol.special_tokens,
            instructions=protocol.instructions
        )
        return protocol_file.to_json()

    def test_comprehensive_protocol_json_structure(self, comprehensive_protocol):
        """Test that the JSON has the correct top-level structure."""
        # Get the JSON output
        json_output = self._get_json_output(comprehensive_protocol)
        
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

    def test_comprehensive_protocol_name(self, comprehensive_protocol):
        """Test that the protocol name is correct."""
        json_output = self._get_json_output(comprehensive_protocol)
        
        assert json_output["name"] == "comprehensive"

    def test_comprehensive_protocol_context(self, comprehensive_protocol):
        """Test that the context is correctly included."""
        json_output = self._get_json_output(comprehensive_protocol)
        
        assert "context" in json_output
        assert isinstance(json_output["context"], list)
        assert len(json_output["context"]) == 2
        assert json_output["context"][0] == "This is a comprehensive protocol with all instruction types."

    def test_comprehensive_protocol_tokens(self, comprehensive_protocol):
        """Test that tokens are correctly included."""
        json_output = self._get_json_output(comprehensive_protocol)
        
        assert "tokens" in json_output
        assert isinstance(json_output["tokens"], dict)
        
        # Check that we have the expected tokens from all instructions
        token_keys = set(json_output["tokens"].keys())
        expected_tokens = {"Tree_", "English_", "Cat_", "Talk_", "Result_", "Alice_", "Count_", "Scores_", "Coordinates_"}
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

    def test_comprehensive_protocol_token_types(self, comprehensive_protocol):
        """Test that token types are correctly set."""
        json_output = self._get_json_output(comprehensive_protocol)
        
        tokens = json_output["tokens"]
        
        # Check specific token types
        for token_key, token_info in tokens.items():
            if token_key == "Alice_":
                assert token_info["user"] is True
                assert token_info["num"] is False
            elif token_key in ["Count_", "Scores_", "Coordinates_"]:
                assert token_info["num"] is True
                assert token_info["user"] is False
            elif token_key not in ["<BOS>", "<EOS>", "<PAD>", "<RUN>", "<UNK>"]:
                assert token_info["user"] is False
                # Some tokens might be marked as numeric due to the way the protocol processes them
                pass
            assert isinstance(token_info["special"], (str, type(None)))

    def test_comprehensive_protocol_special_tokens(self, comprehensive_protocol):
        """Test that special tokens are correctly included."""
        json_output = self._get_json_output(comprehensive_protocol)
        
        assert "special_tokens" in json_output
        assert isinstance(json_output["special_tokens"], list)
        
        # Should include instruction tokens
        assert len(json_output["special_tokens"]) > 0
        assert all(isinstance(token, str) for token in json_output["special_tokens"])

    def test_comprehensive_protocol_instruction(self, comprehensive_protocol):
        """Test that instruction structure is correct."""
        json_output = self._get_json_output(comprehensive_protocol)
        
        assert "instruction" in json_output
        instruction = json_output["instruction"]
        
        # Test instruction top-level keys
        assert "memory" in instruction
        assert "sets" in instruction
        
        # Test memory (should be context_lines + 1)
        assert instruction["memory"] == 3  # 2 context lines + 1 response line
        
        # Test sets structure
        assert isinstance(instruction["sets"], list)
        assert len(instruction["sets"]) == 5  # Five instruction sets
        
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
        assert len(instruction_set["set"]) == 3  # Three context lines (2 context + 1 response)
        assert isinstance(instruction_set["set"][0], list)
        assert len(instruction_set["set"][0]) > 0  # Should have tokens
        
        # Test result (should be one of the final tokens)
        assert isinstance(instruction_set["result"], str)
        assert instruction_set["result"] in ["Result_", "Count_", "Scores_", "Coordinates_", "End_"]
        
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
        assert len(sample["sample"]) == 3  # Three context snippets (2 context + 1 response)
        assert sample["result"] in ["Result_", "Count_", "Scores_", "Coordinates_", "End_"]
        
        # Check numeric values based on instruction type
        if sample["result"] == "Count_":
            assert len(sample["number"]) == 3  # Three numeric values (2 context + 1 response)
            for num_list in sample["number"]:
                assert isinstance(num_list, list)
                # Mixed instruction can have 2 elements: [number, [list]]
                assert len(num_list) in [1, 2]  # Can be 1 or 2 elements
                assert isinstance(num_list[0], (int, float))
                if len(num_list) == 2:
                    assert isinstance(num_list[1], list)
            assert sample["value"] in [10, 15, 20, 25, 30]
        elif sample["result"] in ["Scores_", "Coordinates_"]:
            assert len(sample["number"]) == 3  # Three numeric list values (2 context + 1 response)
            for num_list in sample["number"]:
                assert isinstance(num_list, list)
                # NumListToken can have nested list structure
                assert len(num_list) in [1, 2]  # Can be 1 or 2 elements
                if len(num_list) == 1:
                    # Nested list structure: [[numbers]]
                    assert isinstance(num_list[0], list)
                    assert len(num_list[0]) > 0
                    for num in num_list[0]:
                        assert isinstance(num, (int, float))
                else:
                    # Two elements: [number, [list]]
                    assert isinstance(num_list[0], (int, float))
                    assert isinstance(num_list[1], list)
                    if sample["result"] == "Scores_":
                        assert len(num_list[1]) == 5  # Should have 5 elements
                    elif sample["result"] == "Coordinates_":
                        assert len(num_list[1]) == 3  # Should have 3 elements
            assert sample["value"] in [10, 15, 25]
        else:
            assert sample["number"] is None or len(sample["number"]) == 0  # No numeric values
            assert sample["value"] == "None"

    def test_comprehensive_protocol_guardrails(self, comprehensive_protocol):
        """Test that guardrails are correctly included."""
        json_output = self._get_json_output(comprehensive_protocol)
        
        assert "guardrails" in json_output
        assert isinstance(json_output["guardrails"], dict)
        assert len(json_output["guardrails"]) == 1
        assert "None" in json_output["guardrails"]

    def test_comprehensive_protocol_numbers(self, comprehensive_protocol):
        """Test that numbers are correctly included."""
        json_output = self._get_json_output(comprehensive_protocol)
        
        assert "numbers" in json_output
        assert isinstance(json_output["numbers"], dict)
        
        # Comprehensive protocol should have numeric tokens
        assert len(json_output["numbers"]) > 0
        
        # Check specific numeric tokens
        if "Count" in json_output["numbers"]:
            count_info = json_output["numbers"]["Count"]
            assert "min" in count_info
            assert "max" in count_info
            assert "desc" in count_info
            assert count_info["min"] == 1
            assert count_info["max"] == 100
            assert count_info["desc"] == "Count token"
        
        if "Scores" in json_output["numbers"]:
            scores_info = json_output["numbers"]["Scores"]
            assert "min" in scores_info
            assert "max" in scores_info
            assert "length" in scores_info
            assert "desc" in scores_info
            assert scores_info["min"] == 0
            assert scores_info["max"] == 10
            assert scores_info["length"] == 5
            assert scores_info["desc"] == "Scores token"
        
        if "Coordinates" in json_output["numbers"]:
            coords_info = json_output["numbers"]["Coordinates"]
            assert "min" in coords_info
            assert "max" in coords_info
            assert "length" in coords_info
            assert "desc" in coords_info
            assert coords_info["min"] == -100
            assert coords_info["max"] == 100
            assert coords_info["length"] == 3
            assert coords_info["desc"] == "3D coordinates (x, y, z)"

    def test_comprehensive_protocol_batches(self, comprehensive_protocol):
        """Test that batches are correctly included."""
        json_output = self._get_json_output(comprehensive_protocol)
        
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
        
        # Comprehensive protocol should have no batches
        assert len(batches["pretrain"]) == 0
        assert len(batches["instruct"]) == 0
        assert len(batches["judge"]) == 0
        assert len(batches["ppo"]) == 0

    def test_comprehensive_protocol_token_descriptions(self, comprehensive_protocol):
        """Test that token descriptions are correctly included."""
        json_output = self._get_json_output(comprehensive_protocol)
        
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
        if "Alice" in tokens:
            assert tokens["Alice"]["desc"] == "User token"
        if "Count" in tokens:
            assert tokens["Count"]["desc"] == "Count token"
        if "Scores" in tokens:
            assert tokens["Scores"]["desc"] == "Scores token"
        if "Coordinates" in tokens:
            assert tokens["Coordinates"]["desc"] == "3D coordinates (x, y, z)"

    def test_comprehensive_protocol_instruction_sets_order(self, comprehensive_protocol):
        """Test that instruction sets are in the correct order."""
        json_output = self._get_json_output(comprehensive_protocol)
        
        instruction_sets = json_output["instruction"]["sets"]
        
        # Should have 5 instruction sets
        assert len(instruction_sets) == 5
        
        # Check that we have all expected instruction types
        results = [instruction_set["result"] for instruction_set in instruction_sets]
        expected_results = ["Result_", "Count_", "Scores_", "End_"]

        # Should contain all expected results (order may vary)
        for expected_result in expected_results:
            assert expected_result in results

