"""
Unit tests for dictionary creation methods in Instruction classes.
All instructions and samples are created using fixtures.
"""
from model_train_protocol.common.constants import NON_TOKEN


class TestInstructionDictMethods:
    """Test cases for Instruction dictionary creation methods using comprehensive fixtures."""

    def test_instruction_to_dict_basic(self, simple_basic_instruction_with_samples):
        """Test basic instruction to_dict conversion using fixtures."""
        instruction_dict = simple_basic_instruction_with_samples.to_dict()
        
        # Check structure
        assert 'tokens' in instruction_dict
        assert 'result' in instruction_dict
        assert 'samples' in instruction_dict
        
        # Check tokens structure
        tokens = instruction_dict['tokens']
        assert len(tokens) == 2  # context and response
        assert len(tokens[0]) >= 1  # tokens in context set
        assert len(tokens[1]) >= 1  # tokens in response set
        
        # Check result
        assert instruction_dict['result'] is not None
        
        # Check samples
        assert len(instruction_dict['samples']) == 1

    def test_instruction_to_dict_with_multiple_samples(self, simple_instruction_with_multiple_samples):
        """Test instruction to_dict with multiple samples using fixtures."""
        instruction_dict = simple_instruction_with_multiple_samples.to_dict()
        
        # Check samples count
        assert len(instruction_dict['samples']) == 3
        
        # Check that each sample is properly formatted
        for sample in instruction_dict['samples']:
            # Convert sample to dict to check its structure
            sample_dict = sample.to_dict()
            assert 'strings' in sample_dict
            assert 'prompt' in sample_dict
            assert 'numbers' in sample_dict
            assert 'result' in sample_dict
            assert 'value' in sample_dict

    def test_instruction_to_dict_with_user_instruction(self, user_basic_instruction_with_samples):
        """Test user instruction to_dict conversion using fixtures."""
        instruction_dict = user_basic_instruction_with_samples.to_dict()
        
        # Check structure
        assert 'tokens' in instruction_dict
        assert 'result' in instruction_dict
        assert 'samples' in instruction_dict
        
        # Check that samples contain prompts
        sample = instruction_dict['samples'][0]
        sample_dict = sample.to_dict()
        assert sample_dict['prompt'] == "What should I do?"

    def test_instruction_to_dict_with_numeric_tokens(self, simple_numtoken_instruction_with_samples):
        """Test instruction to_dict with numeric tokens using fixtures."""
        instruction_dict = simple_numtoken_instruction_with_samples.to_dict()
        
        # Check that numeric values are preserved
        sample = instruction_dict['samples'][0]
        sample_dict = sample.to_dict()
        assert sample_dict['value'] == 10
        # Check that numbers array is present
        assert 'numbers' in sample_dict

    def test_instruction_to_dict_with_complex_token_sets(self, simple_mixed_instruction_with_samples):
        """Test instruction to_dict with complex token sets using fixtures."""
        instruction_dict = simple_mixed_instruction_with_samples.to_dict()
        
        # Check tokens structure
        tokens = instruction_dict['tokens']
        assert len(tokens) == 2  # context and response
        assert len(tokens[0]) >= 1  # tokens in context set
        assert len(tokens[1]) >= 1  # tokens in response set

    def test_instruction_to_dict_with_none_final(self, simple_instruction_with_none_final):
        """Test instruction to_dict with NON_TOKEN final token using fixtures."""
        instruction_dict = simple_instruction_with_none_final.to_dict()
        
        # Check that result is NON_TOKEN
        assert instruction_dict['result'] == NON_TOKEN.to_dict()

    def test_instruction_to_dict_with_non_token_final(self, simple_instruction_with_non_token_final):
        """Test instruction to_dict with NON_TOKEN final using fixtures."""
        instruction_dict = simple_instruction_with_non_token_final.to_dict()
        
        # Check that result is NON_TOKEN's dictionary
        assert instruction_dict['result'] == NON_TOKEN.to_dict()

    def test_instruction_to_dict_preserves_token_structure(self, simple_basic_instruction):
        """Test that to_dict preserves the token structure correctly using fixtures."""
        instruction_dict = simple_basic_instruction.to_dict()
        
        # Check that token dictionaries are preserved
        tokens = instruction_dict['tokens']
        context_tokens = tokens[0]
        response_tokens = tokens[1]
        
        assert len(context_tokens) >= 1
        assert len(response_tokens) >= 1
        
        # Check that all tokens have required fields
        for token in context_tokens:
            assert 'value' in token
            assert 'key' in token
        
        for token in response_tokens:
            assert 'value' in token
            assert 'key' in token
        
        assert instruction_dict['result'] is not None

    def test_instruction_to_dict_with_empty_samples(self, simple_instruction_with_empty_samples):
        """Test instruction to_dict with no samples using fixtures."""
        instruction_dict = simple_instruction_with_empty_samples.to_dict()
        
        # Check that samples list is empty
        assert instruction_dict['samples'] == []

    def test_instruction_to_dict_consistency(self, simple_basic_instruction_with_samples):
        """Test that identical instructions produce identical dictionaries using fixtures."""
        # Create two identical instructions by using the same fixture
        instruction1 = simple_basic_instruction_with_samples
        instruction2 = simple_basic_instruction_with_samples
        
        # Check that dictionaries are identical (convert samples to dicts for comparison)
        dict1 = instruction1.to_dict()
        dict2 = instruction2.to_dict()
        
        # Convert samples to dicts for proper comparison
        serializable_dict1 = {
            'tokens': dict1['tokens'],
            'result': dict1['result'],
            'samples': [sample.to_dict() for sample in dict1['samples']]
        }
        serializable_dict2 = {
            'tokens': dict2['tokens'],
            'result': dict2['result'],
            'samples': [sample.to_dict() for sample in dict2['samples']]
        }
        
        assert serializable_dict1 == serializable_dict2

    def test_instruction_to_dict_json_serializable(self, simple_basic_instruction_with_samples):
        """Test that to_dict produces JSON-serializable output using fixtures."""
        import json
        
        instruction_dict = simple_basic_instruction_with_samples.to_dict()
        
        # Convert samples to dicts for JSON serialization
        serializable_dict = {
            'tokens': instruction_dict['tokens'],
            'result': instruction_dict['result'],
            'samples': [sample.to_dict() for sample in instruction_dict['samples']]
        }
        
        # Should not raise an exception
        json_str = json.dumps(serializable_dict)
        assert isinstance(json_str, str)
        
        # Should be able to deserialize
        deserialized = json.loads(json_str)
        assert deserialized == serializable_dict

    def test_instruction_to_dict_with_unicode_content(self, simple_basic_instruction_with_samples):
        """Test instruction to_dict with unicode content using fixtures."""
        instruction_dict = simple_basic_instruction_with_samples.to_dict()
        
        # Check that unicode is preserved in token structure
        tokens = instruction_dict['tokens']
        assert len(tokens[0]) >= 1
        assert len(tokens[1]) >= 1
        
        # Check that all tokens have required fields
        for token in tokens[0]:
            assert 'key' in token
            assert 'desc' in token
        
        for token in tokens[1]:
            assert 'key' in token
            assert 'desc' in token
        
        assert instruction_dict['result'] is not None

    def test_instruction_to_dict_with_long_content(self, simple_basic_instruction_with_samples):
        """Test instruction to_dict with long content using fixtures."""
        instruction_dict = simple_basic_instruction_with_samples.to_dict()
        
        # Check that content is preserved
        sample = instruction_dict['samples'][0]
        sample_dict = sample.to_dict()
        assert len(sample_dict['strings'][0]) > 0
        assert len(sample_dict['strings'][1]) > 0

    def test_instruction_to_dict_edge_cases(self, simple_basic_instruction_with_samples):
        """Test instruction to_dict with edge cases using fixtures."""
        instruction_dict = simple_basic_instruction_with_samples.to_dict()
        
        # Check that samples are preserved
        sample = instruction_dict['samples'][0]
        sample_dict = sample.to_dict()
        assert len(sample_dict['strings']) >= 2

    def test_instruction_to_dict_preserves_all_attributes(self, simple_basic_instruction_with_samples):
        """Test that to_dict preserves all instruction attributes using fixtures."""
        instruction_dict = simple_basic_instruction_with_samples.to_dict()
        
        # Check all expected keys are present
        expected_keys = {'tokens', 'result', 'samples'}
        assert set(instruction_dict.keys()) == expected_keys
        
        # Check that tokens structure matches instruction structure
        assert len(instruction_dict['tokens']) == 2  # context and response
        assert instruction_dict['result'] is not None
        assert len(instruction_dict['samples']) == 1

    # Comprehensive tests for all tokenset combinations
    
    def test_comprehensive_instruction_coverage(self, 
                                               simple_basic_instruction_with_samples,
                                               simple_numtoken_instruction_with_samples,
                                               simple_numlisttoken_instruction_with_samples,
                                               simple_mixed_instruction_with_samples,
                                               simple_scores_instruction_with_samples,
                                               user_basic_instruction_with_samples,
                                               user_numtoken_instruction_with_samples,
                                               user_numlisttoken_instruction_with_samples,
                                               user_mixed_instruction_with_samples,
                                               user_scores_instruction_with_samples):
        """Test comprehensive instruction coverage across all tokenset combinations."""
        instructions = [
            simple_basic_instruction_with_samples,
            simple_numtoken_instruction_with_samples,
            simple_numlisttoken_instruction_with_samples,
            simple_mixed_instruction_with_samples,
            simple_scores_instruction_with_samples,
            user_basic_instruction_with_samples,
            user_numtoken_instruction_with_samples,
            user_numlisttoken_instruction_with_samples,
            user_mixed_instruction_with_samples,
            user_scores_instruction_with_samples
        ]
        
        for instruction in instructions:
            instruction_dict = instruction.to_dict()
            
            # Check basic structure
            assert 'tokens' in instruction_dict
            assert 'result' in instruction_dict
            assert 'samples' in instruction_dict
            
            # Check tokens structure
            tokens = instruction_dict['tokens']
            assert len(tokens) == 2  # context and response/user
            assert len(tokens[0]) >= 1  # tokens in context set
            assert len(tokens[1]) >= 1  # tokens in response/user set
            
            # Check that samples are properly formatted
            for sample in instruction_dict['samples']:
                sample_dict = sample.to_dict()
                assert 'strings' in sample_dict
                assert 'prompt' in sample_dict
                assert 'numbers' in sample_dict
                assert 'result' in sample_dict
                assert 'value' in sample_dict

    def test_numtoken_instruction_combinations(self, simple_numtoken_instruction_with_samples, user_numtoken_instruction_with_samples):
        """Test NumToken instruction combinations."""
        # Test simple NumToken instruction
        simple_dict = simple_numtoken_instruction_with_samples.to_dict()
        assert simple_dict['result'] is not None
        assert len(simple_dict['samples']) == 1
        
        # Test user NumToken instruction
        user_dict = user_numtoken_instruction_with_samples.to_dict()
        assert user_dict['result'] is not None
        assert len(user_dict['samples']) == 1
        
        # Check that samples have numeric values
        simple_sample = simple_dict['samples'][0].to_dict()
        user_sample = user_dict['samples'][0].to_dict()
        
        assert simple_sample['value'] == 10
        assert user_sample['value'] == 20

    def test_numlisttoken_instruction_combinations(self, simple_numlisttoken_instruction_with_samples, user_numlisttoken_instruction_with_samples):
        """Test NumListToken instruction combinations."""
        # Test simple NumListToken instruction
        simple_dict = simple_numlisttoken_instruction_with_samples.to_dict()
        assert simple_dict['result'] is not None
        assert len(simple_dict['samples']) == 1
        
        # Test user NumListToken instruction
        user_dict = user_numlisttoken_instruction_with_samples.to_dict()
        assert user_dict['result'] is not None
        assert len(user_dict['samples']) == 1
        
        # Check that samples have numeric values
        simple_sample = simple_dict['samples'][0].to_dict()
        user_sample = user_dict['samples'][0].to_dict()
        
        assert simple_sample['value'] == [10, 20, 30]
        assert user_sample['value'] == [5, 15, 25]

    def test_mixed_instruction_combinations(self, simple_mixed_instruction_with_samples, user_mixed_instruction_with_samples):
        """Test mixed numeric instruction combinations."""
        # Test simple mixed instruction
        simple_dict = simple_mixed_instruction_with_samples.to_dict()
        assert simple_dict['result'] is not None
        assert len(simple_dict['samples']) == 1
        
        # Test user mixed instruction
        user_dict = user_mixed_instruction_with_samples.to_dict()
        assert user_dict['result'] is not None
        assert len(user_dict['samples']) == 1
        
        # Check that samples have numeric values
        simple_sample = simple_dict['samples'][0].to_dict()
        user_sample = user_dict['samples'][0].to_dict()
        
        assert simple_sample['value'] == 25.5
        assert user_sample['value'] == 35.5

    def test_scores_instruction_combinations(self, simple_scores_instruction_with_samples, user_scores_instruction_with_samples):
        """Test scores instruction combinations."""
        # Test simple scores instruction
        simple_dict = simple_scores_instruction_with_samples.to_dict()
        assert simple_dict['result'] is not None
        assert len(simple_dict['samples']) == 1
        
        # Test user scores instruction
        user_dict = user_scores_instruction_with_samples.to_dict()
        assert user_dict['result'] is not None
        assert len(user_dict['samples']) == 1
        
        # Check that samples have appropriate values
        simple_sample = simple_dict['samples'][0].to_dict()
        user_sample = user_dict['samples'][0].to_dict()
        
        assert simple_sample['value'] == [8, 9, 7, 10, 6]
        assert user_sample['value'] == [6.2, 7.5, 8.0, 9.1, 5.4]

    def test_user_instruction_with_multiple_samples(self, user_instruction_with_multiple_samples):
        """Test user instruction with multiple samples."""
        instruction_dict = user_instruction_with_multiple_samples.to_dict()
        
        # Check samples count
        assert len(instruction_dict['samples']) == 3
        
        # Check that each sample has a prompt
        for sample in instruction_dict['samples']:
            sample_dict = sample.to_dict()
            assert sample_dict['prompt'] is not None
            assert 'User prompt' in sample_dict['prompt']

    def test_edge_case_instructions(self, simple_instruction_with_none_final, simple_instruction_with_non_token_final, simple_instruction_with_empty_samples):
        """Test edge case instructions."""
        # Test NON_TOKEN final
        none_dict = simple_instruction_with_none_final.to_dict()
        assert none_dict['result'] == NON_TOKEN.to_dict()
        
        # Test NON_TOKEN final
        non_token_dict = simple_instruction_with_non_token_final.to_dict()
        assert non_token_dict['result'] == NON_TOKEN.to_dict()
        
        # Test empty samples
        empty_dict = simple_instruction_with_empty_samples.to_dict()
        assert empty_dict['samples'] == []
