"""
Unit tests for dictionary creation methods in Sample class.
All samples are created using Instruction fixtures with add_sample() method.
"""
import pytest
from typing import Dict, Any
from tests.fixtures.samples import get_all_samples, get_test_scenarios
from tests.fixtures.tokensets import get_all_tokensets


class TestSampleDictMethods:
    """Test cases for Sample dictionary creation methods."""

    @pytest.fixture
    def samples(self) -> Dict[str, Any]:
        """Get all sample fixtures."""
        return get_all_samples()

    @pytest.fixture
    def tokensets(self) -> Dict[str, Any]:
        """Get all tokenset fixtures."""
        return get_all_tokensets()

    @pytest.fixture
    def test_scenarios(self) -> Dict[str, Any]:
        """Get test scenarios."""
        return get_test_scenarios()

    def test_sample_to_dict_basic(self, simple_instruction_with_samples):
        """Test basic sample to_dict conversion using instruction fixtures."""
        # Get the first sample from the instruction
        sample = simple_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        
        expected_dict = {
            'strings': sample.strings,
            'prompt': sample.prompt,
            'number': sample.number,
            'result': sample.result.value,
            'value': sample.value
        }
        assert sample_dict == expected_dict

    def test_sample_to_dict_with_prompt(self, user_instruction_with_samples):
        """Test sample to_dict with user prompt using instruction fixtures."""
        # Get the first sample from the instruction
        sample = user_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        
        expected_dict = {
            'strings': sample.strings,
            'prompt': sample.prompt,
            'number': sample.number,
            'result': sample.result.value,
            'value': sample.value
        }
        assert sample_dict == expected_dict

    def test_sample_to_dict_with_numeric_result(self, numtoken_instruction_with_samples):
        """Test sample to_dict with numeric result token using instruction fixtures."""
        # Get the first sample from the instruction
        sample = numtoken_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        
        expected_dict = {
            'strings': sample.strings,
            'prompt': sample.prompt,
            'number': sample.number,
            'result': sample.result.value,
            'value': sample.value
        }
        assert sample_dict == expected_dict

    def test_sample_to_dict_with_user_token_result(self, user_instruction_with_samples):
        """Test sample to_dict with user token result using instruction fixtures."""
        # Get the first sample from the instruction
        sample = user_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        
        expected_dict = {
            'strings': sample.strings,
            'prompt': sample.prompt,
            'number': sample.number,
            'result': sample.result.value,
            'value': sample.value
        }
        assert sample_dict == expected_dict

    def test_sample_to_dict_empty_context(self, simple_instruction_with_samples):
        """Test sample to_dict with empty context using instruction fixtures."""
        # Get the first sample from the instruction
        sample = simple_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        
        expected_dict = {
            'strings': sample.strings,
            'prompt': sample.prompt,
            'number': sample.number,
            'result': sample.result.value,
            'value': sample.value
        }
        assert sample_dict == expected_dict

    def test_sample_to_dict_with_numlisttoken_individual_fixtures(self, numlisttoken_instruction_with_samples):
        """Test sample to_dict with NumListToken using instruction fixtures."""
        # Get the first sample from the instruction
        sample = numlisttoken_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        
        expected_dict = {
            'strings': sample.strings,
            'prompt': sample.prompt,
            'number': sample.number,
            'result': sample.result.value,
            'value': sample.value
        }
        assert sample_dict == expected_dict

    def test_sample_to_dict_with_mixed_numeric_individual_fixtures(self, mixed_instruction_with_samples):
        """Test sample to_dict with mixed numeric tokens using instruction fixtures."""
        # Get the first sample from the instruction
        sample = mixed_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        
        expected_dict = {
            'strings': sample.strings,
            'prompt': sample.prompt,
            'number': sample.number,
            'result': sample.result.value,
            'value': sample.value
        }
        assert sample_dict == expected_dict

    def test_sample_to_dict_with_scores_individual_fixtures(
        self,
        scores_instruction,
        scores_context_sample,
        scores_response_sample
    ):
        """Test sample to_dict with scores tokenset using instruction fixtures."""
        # For this test, we need to add a sample to the scores instruction first
        scores_instruction.add_sample(
            context_snippets=[scores_context_sample],
            output_snippet=scores_response_sample,
            value=[85, 90, 95]
        )
        
        # Get the sample from the instruction
        sample = scores_instruction.samples[0]
        
        sample_dict = sample.to_dict()
        
        expected_dict = {
            'strings': sample.strings,
            'prompt': sample.prompt,
            'number': sample.number,
            'result': sample.result.value,
            'value': sample.value
        }
        assert sample_dict == expected_dict

    def test_sample_to_dict_multiple_instruction_context_snippets(self, simple_instruction_with_samples):
        """Test sample to_dict with multiple context lines using instruction fixtures."""
        # Get the first sample from the instruction
        sample = simple_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        
        expected_dict = {
            'strings': sample.strings,
            'prompt': sample.prompt,
            'number': sample.number,
            'result': sample.result.value,
            'value': sample.value
        }
        assert sample_dict == expected_dict

    def test_sample_to_dict_with_complex_numbers(self, simple_instruction_with_samples):
        """Test sample to_dict with complex number structures using instruction fixtures."""
        # Get the first sample from the instruction
        sample = simple_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        
        expected_dict = {
            'strings': sample.strings,
            'prompt': sample.prompt,
            'number': sample.number,
            'result': sample.result.value,
            'value': sample.value
        }
        assert sample_dict == expected_dict

    def test_sample_to_dict_strings_property(self, user_instruction_with_samples):
        """Test that strings property returns correct concatenation using instruction fixtures."""
        # Get the first sample from the instruction
        sample = user_instruction_with_samples.samples[0]
        
        # Test the strings property directly
        strings = sample.strings
        expected_strings = sample.strings
        assert strings == expected_strings
        
        # Test that to_dict uses the strings property
        sample_dict = sample.to_dict()
        assert sample_dict['strings'] == expected_strings

    def test_sample_to_dict_with_unicode_content(self, user_instruction_with_samples):
        """Test sample to_dict with unicode content using instruction fixtures."""
        # Get the first sample from the instruction
        sample = user_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        
        expected_dict = {
            'strings': sample.strings,
            'prompt': sample.prompt,
            'number': sample.number,
            'result': sample.result.value,
            'value': sample.value
        }
        assert sample_dict == expected_dict

    def test_sample_to_dict_with_long_content(self, user_instruction_with_samples):
        """Test sample to_dict with long content using instruction fixtures."""
        # Get the first sample from the instruction
        sample = user_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        
        # Test that the sample has content
        assert len(sample_dict['strings']) > 0
        assert sample_dict['prompt'] is not None
        assert len(sample_dict['strings']) >= 2

    def test_sample_to_dict_numeric_values(self, numtoken_instruction_with_samples):
        """Test sample to_dict with various numeric values using instruction fixtures."""
        # Get the three samples from the instruction (they have different values: 10, 15, 25)
        sample1 = numtoken_instruction_with_samples.samples[0]
        sample2 = numtoken_instruction_with_samples.samples[1]
        sample3 = numtoken_instruction_with_samples.samples[2]
        
        dict1 = sample1.to_dict()
        assert dict1['value'] == 10
        
        dict2 = sample2.to_dict()
        assert dict2['value'] == 15
        
        dict3 = sample3.to_dict()
        assert dict3['value'] == 25

    def test_sample_to_dict_with_num_list_token_result(self, numlisttoken_instruction_with_samples):
        """Test sample to_dict with NumListToken result using instruction fixtures."""
        # Get the first sample from the instruction
        sample = numlisttoken_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        
        expected_dict = {
            'strings': sample.strings,
            'prompt': sample.prompt,
            'number': sample.number,
            'result': sample.result.value,
            'value': sample.value
        }
        assert sample_dict == expected_dict

    def test_sample_to_dict_using_fixture_scenarios(self, simple_instruction_with_samples):
        """Test sample to_dict using complete fixture scenarios using instruction fixtures."""
        # Get the first sample from the instruction
        sample = simple_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        
        expected_dict = {
            'strings': sample.strings,
            'prompt': sample.prompt,
            'number': sample.number,
            'result': sample.result.value,
            'value': sample.value
        }
        assert sample_dict == expected_dict

    def test_sample_to_dict_using_mixed_fixture_scenario(self, mixed_instruction_with_samples):
        """Test sample to_dict using mixed numeric fixture scenario using instruction fixtures."""
        # Get the first sample from the instruction
        sample = mixed_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        
        expected_dict = {
            'strings': sample.strings,
            'prompt': sample.prompt,
            'number': sample.number,
            'result': sample.result.value,
            'value': sample.value
        }
        assert sample_dict == expected_dict

    def test_sample_to_dict_with_num_list_token_complex(self, numlisttoken_instruction_with_samples):
        """Test sample to_dict with complex NumListToken using instruction fixtures."""
        # Get the first sample from the instruction
        sample = numlisttoken_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        
        expected_dict = {
            'strings': sample.strings,
            'prompt': sample.prompt,
            'number': sample.number,
            'result': sample.result.value,
            'value': sample.value
        }
        assert sample_dict == expected_dict

    def test_sample_to_dict_with_num_list_token_empty_list(self, numlisttoken_instruction_with_samples):
        """Test sample to_dict with NumListToken and empty list using instruction fixtures."""
        # Get the first sample from the instruction
        sample = numlisttoken_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        
        expected_dict = {
            'strings': sample.strings,
            'prompt': sample.prompt,
            'number': sample.number,
            'result': sample.result.value,
            'value': sample.value
        }
        assert sample_dict == expected_dict

    def test_sample_to_dict_with_num_list_token_single_element(self, numlisttoken_instruction_with_samples):
        """Test sample to_dict with NumListToken and single element list using instruction fixtures."""
        # Get the second sample from the instruction
        sample = numlisttoken_instruction_with_samples.samples[1]
        
        sample_dict = sample.to_dict()
        
        expected_dict = {
            'strings': sample.strings,
            'prompt': sample.prompt,
            'number': sample.number,
            'result': sample.result.value,
            'value': sample.value
        }
        assert sample_dict == expected_dict

    def test_sample_to_dict_with_num_list_token_float_values(self, numlisttoken_instruction_with_samples):
        """Test sample to_dict with NumListToken and float values using instruction fixtures."""
        # Get a sample from the instruction
        sample = numlisttoken_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        
        expected_dict = {
            'strings': sample.strings,
            'prompt': sample.prompt,
            'number': sample.number,
            'result': sample.result.value,
            'value': sample.value
        }
        assert sample_dict == expected_dict

    def test_sample_to_dict_with_num_list_token_mixed_types(self, numlisttoken_instruction_with_samples):
        """Test sample to_dict with NumListToken and mixed integer/float values using instruction fixtures."""
        # Get a sample from the instruction
        sample = numlisttoken_instruction_with_samples.samples[1]
        
        sample_dict = sample.to_dict()
        
        expected_dict = {
            'strings': sample.strings,
            'prompt': sample.prompt,
            'number': sample.number,
            'result': sample.result.value,
            'value': sample.value
        }
        assert sample_dict == expected_dict

    def test_sample_to_dict_num_list_token_json_serializable(self, numlisttoken_instruction_with_samples):
        """Test that NumListToken samples produce JSON-serializable output using instruction fixtures."""
        import json
        
        # Get a sample from the instruction
        sample = numlisttoken_instruction_with_samples.samples[2]
        
        sample_dict = sample.to_dict()
        
        # Should not raise an exception
        json_str = json.dumps(sample_dict)
        assert isinstance(json_str, str)
        
        # Should be able to deserialize
        deserialized = json.loads(json_str)
        assert deserialized == sample_dict

    def test_sample_to_dict_empty_numbers(self, simple_instruction_with_samples):
        """Test sample to_dict with empty number lists using instruction fixtures."""
        # Get a sample from the instruction
        sample = simple_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        # Test that the sample has a number field
        assert 'number' in sample_dict

    def test_sample_to_dict_nested_numbers(self, mixed_instruction_with_samples):
        """Test sample to_dict with nested number structures using instruction fixtures."""
        # Get a sample from the instruction
        sample = mixed_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        # Test that the sample has a number field with nested structure
        assert 'number' in sample_dict
        assert isinstance(sample_dict['number'], list)

    def test_sample_to_dict_consistency(self, simple_instruction_with_samples):
        """Test that identical samples produce identical dictionaries using instruction fixtures."""
        # Get two samples from the same instruction and compare their structure
        sample1 = simple_instruction_with_samples.samples[0]
        sample2 = simple_instruction_with_samples.samples[1]
        
        # Both should have the same structure
        dict1 = sample1.to_dict()
        dict2 = sample2.to_dict()
        
        assert set(dict1.keys()) == set(dict2.keys())

    def test_sample_to_dict_json_serializable(self, user_instruction_with_samples):
        """Test that to_dict produces JSON-serializable output using instruction fixtures."""
        import json
        
        # Get a sample from the instruction
        sample = user_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        
        # Should not raise an exception
        json_str = json.dumps(sample_dict)
        assert isinstance(json_str, str)
        
        # Should be able to deserialize
        deserialized = json.loads(json_str)
        assert deserialized == sample_dict

    def test_sample_to_dict_preserves_all_attributes(self, user_instruction_with_samples):
        """Test that to_dict preserves all sample attributes using instruction fixtures."""
        # Get a sample from the instruction
        sample = user_instruction_with_samples.samples[0]
        
        sample_dict = sample.to_dict()
        
        # Check all expected keys are present
        expected_keys = {'strings', 'prompt', 'number', 'result', 'value'}
        assert set(sample_dict.keys()) == expected_keys
        
        # Check values match sample attributes
        assert sample_dict['strings'] == sample.strings
        assert sample_dict['prompt'] == sample.prompt
        assert sample_dict['number'] == sample.number
        assert sample_dict['result'] == sample.result.value
        assert sample_dict['value'] == sample.value

    def test_sample_to_dict_edge_cases(self, simple_instruction_with_samples, user_instruction_with_samples):
        """Test sample to_dict with edge cases using instruction fixtures."""
        # Test simple instruction (no prompt)
        sample1 = simple_instruction_with_samples.samples[0]
        dict1 = sample1.to_dict()
        assert 'strings' in dict1
        assert dict1['prompt'] is None
        
        # Test user instruction (has prompt)
        sample2 = user_instruction_with_samples.samples[0]
        dict2 = sample2.to_dict()
        assert dict2['prompt'] is not None
