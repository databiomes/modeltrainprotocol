"""
Test JSON creation for workflow protocol.
"""
import pytest
from model_train_protocol import Protocol
from tests.utils.protocol_json_utils import assert_special_tokens_in_tokens


class TestWorkflowProtocolJSON:
    """Test JSON structure and content for workflow protocol."""

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

    def test_workflow_protocol_json_structure(self, workflow_protocol):
        """Test that the JSON has the correct top-level structure."""
        # Get the JSON output
        json_output = self._get_json_output(workflow_protocol)

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
        expected_keys = {"name", "context", "tokens", "special_tokens", "instruction", "guardrails", "numbers",
                         "batches"}
        actual_keys = set(json_output.keys())
        assert actual_keys == expected_keys

    def test_workflow_protocol_name(self, workflow_protocol):
        """Test that the protocol name is correct."""
        json_output = self._get_json_output(workflow_protocol)

        assert json_output["name"] == "workflow_protocol"

    def test_workflow_protocol_context(self, workflow_protocol):
        """Test that the context is correctly included."""
        json_output = self._get_json_output(workflow_protocol)

        assert "context" in json_output
        assert isinstance(json_output["context"], list)
        assert len(json_output["context"]) == 2
        assert json_output["context"][0] == "This is workflow context line 1."
        assert json_output["context"][1] == "This is workflow context line 2."

    def test_workflow_protocol_tokens(self, workflow_protocol):
        """Test that tokens are correctly included."""
        json_output = self._get_json_output(workflow_protocol)

        assert "tokens" in json_output
        assert isinstance(json_output["tokens"], dict)

        # Check that we have the expected tokens from workflow instructions
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

    def test_workflow_protocol_token_types(self, workflow_protocol):
        """Test that token types are correctly set."""
        json_output = self._get_json_output(workflow_protocol)

        tokens = json_output["tokens"]

        # Check specific token types
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
                assert token_info["user"] is False
                assert token_info["num"] is False
                assert token_info["special"] is None

    def test_workflow_protocol_special_tokens(self, workflow_protocol):
        """Test that special tokens are correctly included."""
        json_output = self._get_json_output(workflow_protocol)

        assert "special_tokens" in json_output
        assert isinstance(json_output["special_tokens"], list)

        # Should include instruction tokens
        assert len(json_output["special_tokens"]) > 0
        assert all(isinstance(token, str) for token in json_output["special_tokens"])

    def test_workflow_protocol_special_tokens_unique(self, workflow_protocol):
        """Test that special tokens are unique with no duplicates."""
        json_output = self._get_json_output(workflow_protocol)

        special_tokens = json_output["special_tokens"]
        
        # Check for duplicates
        assert len(special_tokens) == len(set(special_tokens)), "Special tokens contain duplicates"
        
        # Check that all special tokens are unique
        seen = set()
        for token in special_tokens:
            assert token not in seen, f"Duplicate special token found: {token}"
            seen.add(token)

    def test_workflow_protocol_special_token_format(self, workflow_protocol):
        """Test that special tokens have the exact format specified."""
        json_output = self._get_json_output(workflow_protocol)

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

    def test_workflow_protocol_tokens_key_value_pairs(self, workflow_protocol):
        """Test that all items in tokens are proper key-value pairs."""
        json_output = self._get_json_output(workflow_protocol)

        tokens = json_output["tokens"]
        
        # Check that tokens is a dictionary
        assert isinstance(tokens, dict), "Tokens should be a dictionary"
        
        # Check that all items are key-value pairs (string keys with dict values)
        for token_key, token_value in tokens.items():
            # Key should be a string
            assert isinstance(token_key, str), f"Token key '{token_key}' should be a string, got {type(token_key)}"
            assert len(token_key) > 0, f"Token key should not be empty"
            
            # Value should be a dictionary
            assert isinstance(token_value, dict), f"Token value for '{token_key}' should be a dictionary, got {type(token_value)}"
            
            # Token value should have the required fields
            required_fields = {"emoji", "num", "user", "desc", "special"}
            actual_fields = set(token_value.keys())
            assert actual_fields == required_fields, f"Token '{token_key}' has fields {actual_fields}, expected {required_fields}"
            
            # Check field types
            assert isinstance(token_value["emoji"], str), f"Token '{token_key}' emoji should be string"
            assert isinstance(token_value["num"], (bool, int)), f"Token '{token_key}' num should be bool or int"
            assert isinstance(token_value["user"], bool), f"Token '{token_key}' user should be bool"
            assert token_value["desc"] is None or isinstance(token_value["desc"], str), f"Token '{token_key}' desc should be None or string"
            assert token_value["special"] is None or isinstance(token_value["special"], str), f"Token '{token_key}' special should be None or string"

    def test_workflow_protocol_special_tokens_structure(self, workflow_protocol):
        """Test the structure of special_tokens."""
        json_output = self._get_json_output(workflow_protocol)

        special_tokens = json_output["special_tokens"]
        
        # Check that special_tokens is a list
        assert isinstance(special_tokens, list), f"special_tokens should be a list, got {type(special_tokens)}"
        
        # Check that all items in special_tokens are strings
        for i, token in enumerate(special_tokens):
            assert isinstance(token, str), f"special_tokens[{i}] should be a string, got {type(token)}"
            assert len(token) > 0, f"special_tokens[{i}] should not be empty"
        
        # Check that all special tokens are valid keys in the tokens dictionary
        assert_special_tokens_in_tokens(json_output, special_tokens)

    def test_workflow_protocol_instruction_structure(self, workflow_protocol):
        """Test the structure of instruction."""
        json_output = self._get_json_output(workflow_protocol)

        instruction = json_output["instruction"]
        
        # Check that instruction is a dictionary
        assert isinstance(instruction, dict), f"instruction should be a dictionary, got {type(instruction)}"
        
        # Check required keys
        required_keys = {"memory", "sets"}
        actual_keys = set(instruction.keys())
        assert actual_keys == required_keys, f"instruction has keys {actual_keys}, expected {required_keys}"

    def test_workflow_protocol_instruction_memory(self, workflow_protocol):
        """Test the instruction memory field."""
        json_output = self._get_json_output(workflow_protocol)

        memory = json_output["instruction"]["memory"]
        
        # Check that memory is an integer
        assert isinstance(memory, int), f"instruction.memory should be an int, got {type(memory)}"
        assert memory > 0, f"instruction.memory should be positive, got {memory}"

    def test_workflow_protocol_instruction_sets(self, workflow_protocol):
        """Test the instruction sets field."""
        json_output = self._get_json_output(workflow_protocol)

        sets = json_output["instruction"]["sets"]
        
        # Check that sets is a list
        assert isinstance(sets, list), f"instruction.sets should be a list, got {type(sets)}"
        assert len(sets) > 0, "instruction.sets should not be empty"
        
        # Check that all items in sets are dictionaries
        for i, instruction_set in enumerate(sets):
            assert isinstance(instruction_set, dict), f"instruction.sets[{i}] should be a dictionary, got {type(instruction_set)}"

    def test_workflow_protocol_instruction_sets_structure(self, workflow_protocol):
        """Test the structure of each instruction set."""
        json_output = self._get_json_output(workflow_protocol)

        sets = json_output["instruction"]["sets"]
        
        for i, instruction_set in enumerate(sets):
            # Check required keys for each instruction set
            required_keys = {"set", "result", "samples", "ppo"}
            actual_keys = set(instruction_set.keys())
            assert actual_keys == required_keys, f"instruction.sets[{i}] has keys {actual_keys}, expected {required_keys}"

    def test_workflow_protocol_instruction_sets_set_field(self, workflow_protocol):
        """Test the 'set' field in instruction sets."""
        json_output = self._get_json_output(workflow_protocol)

        sets = json_output["instruction"]["sets"]
        
        for i, instruction_set in enumerate(sets):
            set_field = instruction_set["set"]
            
            # Check that set is a list
            assert isinstance(set_field, list), f"instruction.sets[{i}].set should be a list, got {type(set_field)}"
            assert len(set_field) > 0, f"instruction.sets[{i}].set should not be empty"
            
            # Check that all items in set are lists (token lists)
            for j, token_list in enumerate(set_field):
                assert isinstance(token_list, list), f"instruction.sets[{i}].set[{j}] should be a list, got {type(token_list)}"
                # Each token list should contain strings
                for k, token in enumerate(token_list):
                    assert isinstance(token, str), f"instruction.sets[{i}].set[{j}][{k}] should be a string, got {type(token)}"

    def test_workflow_protocol_instruction_sets_result_field(self, workflow_protocol):
        """Test the 'result' field in instruction sets."""
        json_output = self._get_json_output(workflow_protocol)

        sets = json_output["instruction"]["sets"]
        
        for i, instruction_set in enumerate(sets):
            result = instruction_set["result"]
            
            # Check that result is a string
            assert isinstance(result, str), f"instruction.sets[{i}].result should be a string, got {type(result)}"
            assert len(result) > 0, f"instruction.sets[{i}].result should not be empty"

    def test_workflow_protocol_instruction_sets_samples_field(self, workflow_protocol):
        """Test the 'samples' field in instruction sets."""
        json_output = self._get_json_output(workflow_protocol)

        sets = json_output["instruction"]["sets"]
        
        for i, instruction_set in enumerate(sets):
            samples = instruction_set["samples"]
            
            # Check that samples is a list
            assert isinstance(samples, list), f"instruction.sets[{i}].samples should be a list, got {type(samples)}"
            assert len(samples) > 0, f"instruction.sets[{i}].samples should not be empty"
            
            # Check that all items in samples are dictionaries
            for j, sample in enumerate(samples):
                assert isinstance(sample, dict), f"instruction.sets[{i}].samples[{j}] should be a dictionary, got {type(sample)}"

    def test_workflow_protocol_instruction_sets_samples_structure(self, workflow_protocol):
        """Test the structure of each sample in instruction sets."""
        json_output = self._get_json_output(workflow_protocol)

        sets = json_output["instruction"]["sets"]
        
        for i, instruction_set in enumerate(sets):
            samples = instruction_set["samples"]
            
            for j, sample in enumerate(samples):
                # Check required keys for each sample
                required_keys = {"sample", "prompt", "number", "result", "value"}
                actual_keys = set(sample.keys())
                assert actual_keys == required_keys, f"instruction.sets[{i}].samples[{j}] has keys {actual_keys}, expected {required_keys}"

    def test_workflow_protocol_instruction_sets_samples_sample_field(self, workflow_protocol):
        """Test the 'sample' field in samples."""
        json_output = self._get_json_output(workflow_protocol)

        sets = json_output["instruction"]["sets"]
        
        for i, instruction_set in enumerate(sets):
            samples = instruction_set["samples"]
            
            for j, sample in enumerate(samples):
                sample_field = sample["sample"]
                
                # Check that sample is a list
                assert isinstance(sample_field, list), f"instruction.sets[{i}].samples[{j}].sample should be a list, got {type(sample_field)}"
                assert len(sample_field) > 0, f"instruction.sets[{i}].samples[{j}].sample should not be empty"
                
                # Check that all items in sample are strings
                for k, snippet in enumerate(sample_field):
                    assert isinstance(snippet, str), f"instruction.sets[{i}].samples[{j}].sample[{k}] should be a string, got {type(snippet)}"

    def test_workflow_protocol_instruction_sets_samples_prompt_field(self, workflow_protocol):
        """Test the 'prompt' field in samples."""
        json_output = self._get_json_output(workflow_protocol)

        sets = json_output["instruction"]["sets"]
        
        for i, instruction_set in enumerate(sets):
            samples = instruction_set["samples"]
            
            for j, sample in enumerate(samples):
                prompt = sample["prompt"]
                
                # Check that prompt is None or a string
                assert prompt is None or isinstance(prompt, str), f"instruction.sets[{i}].samples[{j}].prompt should be None or string, got {type(prompt)}"

    def test_workflow_protocol_instruction_sets_samples_number_field(self, workflow_protocol):
        """Test the 'number' field in samples."""
        json_output = self._get_json_output(workflow_protocol)

        sets = json_output["instruction"]["sets"]
        
        for i, instruction_set in enumerate(sets):
            samples = instruction_set["samples"]
            
            for j, sample in enumerate(samples):
                number = sample["number"]
                
                # Check that number is None or a list
                assert number is None or isinstance(number, list), f"instruction.sets[{i}].samples[{j}].number should be None or list, got {type(number)}"

    def test_workflow_protocol_instruction_sets_samples_result_field(self, workflow_protocol):
        """Test the 'result' field in samples."""
        json_output = self._get_json_output(workflow_protocol)

        sets = json_output["instruction"]["sets"]
        
        for i, instruction_set in enumerate(sets):
            samples = instruction_set["samples"]
            
            for j, sample in enumerate(samples):
                result = sample["result"]
                
                # Check that result is a string
                assert isinstance(result, str), f"instruction.sets[{i}].samples[{j}].result should be a string, got {type(result)}"
                assert len(result) > 0, f"instruction.sets[{i}].samples[{j}].result should not be empty"

    def test_workflow_protocol_instruction_sets_samples_value_field(self, workflow_protocol):
        """Test the 'value' field in samples."""
        json_output = self._get_json_output(workflow_protocol)

        sets = json_output["instruction"]["sets"]
        
        for i, instruction_set in enumerate(sets):
            samples = instruction_set["samples"]
            
            for j, sample in enumerate(samples):
                value = sample["value"]
                
                # Check that value is a string
                assert isinstance(value, str), f"instruction.sets[{i}].samples[{j}].value should be a string, got {type(value)}"

    def test_workflow_protocol_instruction_sets_ppo_field(self, workflow_protocol):
        """Test the 'ppo' field in instruction sets."""
        json_output = self._get_json_output(workflow_protocol)

        sets = json_output["instruction"]["sets"]
        
        for i, instruction_set in enumerate(sets):
            ppo = instruction_set["ppo"]
            
            # Check that ppo is a list
            assert isinstance(ppo, list), f"instruction.sets[{i}].ppo should be a list, got {type(ppo)}"

    def test_workflow_protocol_instruction(self, workflow_protocol):
        """Test that instruction structure is correct."""
        json_output = self._get_json_output(workflow_protocol)

        assert "instruction" in json_output
        instruction = json_output["instruction"]

        # Test instruction top-level keys
        assert "memory" in instruction
        assert "sets" in instruction

        # Test memory (should be instruction_context_snippets + 1)
        assert instruction["memory"] == 3  # 2 context lines + 1 response line

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
        assert len(instruction_set["set"]) == 3  # Two context lines + one response line
        assert isinstance(instruction_set["set"][0], list)
        assert isinstance(instruction_set["set"][1], list)
        assert len(instruction_set["set"][0]) > 0  # Should have tokens
        assert len(instruction_set["set"][1]) > 0  # Should have tokens

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
        # prompt can be None for simple instructions
        assert sample["prompt"] is None or isinstance(sample["prompt"], str)
        # number can be None for non-numeric final tokens
        assert sample["number"] is None or isinstance(sample["number"], list)
        assert isinstance(sample["result"], str)
        assert isinstance(sample["value"], str)

        # Test sample content
        assert len(sample["sample"]) == 3  # Two context snippets + one response
        # number can be None for non-numeric final tokens
        if sample["number"] is not None:
            assert len(sample["number"]) == 0  # No numeric tokens
        assert sample["result"] in ["Result_", "End_"]
        assert sample["value"] == "None"  # No value for workflow instructions

        # User instruction should have prompts
        if sample["result"] == "End_":
            assert len(sample["prompt"]) > 0

    def test_workflow_protocol_guardrails(self, workflow_protocol):
        """Test that guardrails are correctly included."""
        json_output = self._get_json_output(workflow_protocol)

        assert "guardrails" in json_output
        # Guardrails can be a list or a dict (when empty)
        assert isinstance(json_output["guardrails"], (list, dict))
        # Workflow protocol should have no guardrails
        if isinstance(json_output["guardrails"], dict):
            # Check if the dict is effectively empty (only contains None key with empty value)
            assert json_output["guardrails"] == {
                "None": ""
            }
        else:
            assert len(json_output["guardrails"]) == 0

    def test_workflow_protocol_numbers(self, workflow_protocol):
        """Test that numbers are correctly included."""
        json_output = self._get_json_output(workflow_protocol)

        assert "numbers" in json_output
        assert isinstance(json_output["numbers"], dict)

        # Workflow protocol should have no numeric tokens
        if json_output["numbers"] == {'None': ''}:
            # Effectively empty
            pass
        else:
            assert len(json_output["numbers"]) == 0

    def test_workflow_protocol_batches(self, workflow_protocol):
        """Test that batches are correctly included."""
        json_output = self._get_json_output(workflow_protocol)

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

    def test_workflow_protocol_token_descriptions(self, workflow_protocol):
        """Test that token descriptions are correctly included."""
        json_output = self._get_json_output(workflow_protocol)

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
        if "End" in tokens:
            assert tokens["End"]["desc"] == "End token"

    def test_workflow_protocol_instruction_sets_order(self, workflow_protocol):
        """Test that instruction sets are in the correct order."""
        json_output = self._get_json_output(workflow_protocol)

        instruction_sets = json_output["instruction"]["sets"]

        # Should have 2 instruction sets
        assert len(instruction_sets) == 2

        # First set should be user instruction (End_) - alphabetically before Result_
        assert instruction_sets[0]["result"] == "End_"

        # Second set should be simple instruction (Result_)
        assert instruction_sets[1]["result"] == "Result_"

    def test_workflow_protocol_instruction_context_snippets(self, workflow_protocol):
        """Test that the protocol correctly handles 2 context lines."""
        json_output = self._get_json_output(workflow_protocol)

        # Memory should be instruction_context_snippets + 1
        assert json_output["instruction"]["memory"] == 3

        # Each instruction set should have 2 context lines + 1 response line = 3 total lines
        for instruction_set in json_output["instruction"]["sets"]:
            assert len(instruction_set["set"]) == 3

            # Each sample should have 2 context snippets + 1 response = 3 total snippets
            for sample in instruction_set["samples"]:
                assert len(sample["sample"]) == 3
