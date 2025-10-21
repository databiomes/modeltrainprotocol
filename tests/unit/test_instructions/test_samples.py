"""
Unit tests for sample creation and validation with NumToken and NumListToken result tokens.
Tests error handling when values are not provided or wrong types are provided.
"""

import pytest
from model_train_protocol.common.tokens import Token, NumToken, NumListToken, UserToken
from model_train_protocol.common.tokens import TokenSet
from model_train_protocol.common.instructions import Instruction, ExtendedInstruction


class TestSampleValueValidation:
    """Test sample value validation for numeric result tokens."""

    def test_numtoken_result_missing_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumToken result token raises error when value is not provided."""
        num_token = NumToken("Count", min_value=1, max_value=10)
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=num_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as an int or float when final token is a NumToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                response_snippet=output_snippet
                # Missing value parameter
            )

    def test_numtoken_result_wrong_type_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumToken result token raises error when value is wrong type."""
        num_token = NumToken("Count", min_value=1, max_value=10)
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=num_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as an int or float when final token is a NumToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                response_snippet=output_snippet,
                value="invalid_string"  # Wrong type
            )

    def test_numtoken_result_none_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumToken result token raises error when value is None."""
        num_token = NumToken("Count", min_value=1, max_value=10)
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=num_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as an int or float when final token is a NumToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                response_snippet=output_snippet,
                value=None  # None value
            )

    def test_numtoken_result_valid_numeric_value_succeeds(self, simple_tokenset, user_tokenset):
        """Test that NumToken result token accepts valid numeric value."""
        num_token = NumToken("Count", min_value=1, max_value=10)
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=num_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        # Should not raise error - numeric values are now accepted
        instruction.add_sample(
            context_snippets=[context_snippet1, context_snippet2],
            response_snippet=output_snippet,
            value=5  # Pass a numeric value
        )

    def test_numlisttoken_result_missing_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token raises error when value is not provided."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=3)
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=numlist_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as a list of int or float when final token is a NumListToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                response_snippet=output_snippet
                # Missing value parameter
            )

    def test_numlisttoken_result_wrong_type_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token raises error when value is wrong type."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=3)
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=numlist_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as a list of int or float when final token is a NumListToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                response_snippet=output_snippet,
                value="invalid_string"  # Wrong type
            )

    def test_numlisttoken_result_none_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token raises error when value is None."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=3)
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=numlist_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as a list of int or float when final token is a NumListToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                response_snippet=output_snippet,
                value=None  # None value
            )

    def test_numlisttoken_result_valid_list_value_succeeds(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token accepts valid list value."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=3)
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=numlist_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        # Should not raise error
        instruction.add_sample(
            context_snippets=[context_snippet1, context_snippet2],
            response_snippet=output_snippet,
            value=[1, 2, 3]  # Valid list value
        )

    def test_regular_token_result_none_value_allowed(self, simple_tokenset, user_tokenset):
        """Test that regular Token result token allows None value."""
        regular_token = Token("Result")
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=regular_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        # Should not raise error
        instruction.add_sample(
            context_snippets=[context_snippet1, context_snippet2],
            response_snippet=output_snippet,
            value=None  # None value allowed for regular tokens
        )

    def test_user_token_result_none_value_allowed(self, simple_tokenset, user_tokenset):
        """Test that UserToken result token allows None value."""
        user_token = UserToken("User")
        instruction = ExtendedInstruction(
            context=[simple_tokenset, user_tokenset],
            user=user_tokenset,
            final=user_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = user_tokenset.create_snippet("Output")

        # Should not raise error
        instruction.add_sample(
            context_snippets=[context_snippet1, context_snippet2],
            response_string="User prompt",
            output_snippet=output_snippet,
            value=None  # None value allowed for user tokens
        )

    def test_regular_token_result_non_none_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that regular Token result token raises error when value is not None."""
        regular_token = Token("Result")
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=regular_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be None when final token is not a NumToken or NumListToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                response_snippet=output_snippet,
                value="some_value"  # Non-None value not allowed for regular tokens
            )

    def test_user_token_result_non_none_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that UserToken result token raises error when value is not None."""
        user_token = UserToken("User")
        instruction = ExtendedInstruction(
            context=[simple_tokenset, user_tokenset],
            user=user_tokenset,
            final=user_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = user_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be None when final token is not a NumToken or NumListToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                response_string="User prompt",
                output_snippet=output_snippet,
                value="some_value"  # Non-None value not allowed for user tokens
            )

    def test_numtoken_result_list_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumToken result token raises error when value is a list."""
        num_token = NumToken("Count", min_value=1, max_value=10)
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=num_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as an int or float when final token is a NumToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                response_snippet=output_snippet,
                value=[1, 2, 3]  # List value not allowed for NumToken
            )

    def test_numlisttoken_result_numtoken_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token raises error when value is a NumToken."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=3)
        num_token = NumToken("Count", min_value=1, max_value=10)
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=numlist_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as a list of int or float when final token is a NumListToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                response_snippet=output_snippet,
                value=num_token  # NumToken value not allowed for NumListToken
            )

    def test_numlisttoken_result_dict_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token raises error when value is a dict."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=3)
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=numlist_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as a list of int or float when final token is a NumListToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                response_snippet=output_snippet,
                value={"key": "value"}  # Dict value not allowed
            )

    def test_numlisttoken_result_boolean_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token raises error when value is a boolean."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=3)
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=numlist_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as a list of int or float when final token is a NumListToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                response_snippet=output_snippet,
                value=True  # Boolean value not allowed
            )

    def test_numlisttoken_result_empty_list_succeeds(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token accepts empty list."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=1)
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=numlist_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        # Should not raise error
        instruction.add_sample(
            context_snippets=[context_snippet1, context_snippet2],
            response_snippet=output_snippet,
            value=[]  # Empty list
        )

    def test_numlisttoken_result_single_element_list_succeeds(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token accepts single element list."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=1)
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=numlist_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        # Should not raise error
        instruction.add_sample(
            context_snippets=[context_snippet1, context_snippet2],
            response_snippet=output_snippet,
            value=[50]  # Single element list
        )

    def test_numlisttoken_result_multi_element_list_succeeds(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token accepts multi-element list."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=5)
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=numlist_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        # Should not raise error
        instruction.add_sample(
            context_snippets=[context_snippet1, context_snippet2],
            response_snippet=output_snippet,
            value=[10, 20, 30, 40, 50]  # Multi-element list
        )

    def test_mixed_token_types_value_validation(self, simple_tokenset, user_tokenset):
        """Test value validation with mixed token types in instruction."""
        num_token = NumToken("Count", min_value=1, max_value=10)
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=3)
        regular_token = Token("Result")
        
        # Test with NumToken
        instruction1 = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=num_token
        )
        
        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")
        
        # Should require NumToken instance
        with pytest.raises(ValueError):
            instruction1.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                response_snippet=output_snippet,
                value="invalid"
            )
        
        # Test with NumListToken
        instruction2 = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=numlist_token
        )
        
        # Should require list
        with pytest.raises(ValueError):
            instruction2.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                response_snippet=output_snippet,
                value="invalid"
            )
        
        # Test with regular Token
        instruction3 = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=regular_token
        )
        
        # Should allow None only
        instruction3.add_sample(
            context_snippets=[context_snippet1, context_snippet2],
            response_snippet=output_snippet,
            value=None
        )
        
        # Should not allow non-None values
        with pytest.raises(ValueError):
            instruction3.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                response_snippet=output_snippet,
                value="any_value"
            )


class TestInstructionValidation:
    """Test instruction validation for add_sample method."""

    def test_simple_instruction_wrong_context_snippet_count_raises_error(self, simple_tokenset, user_tokenset):
        """Test that Instruction raises error when context snippet count doesn't match."""
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=Token("Result")
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        # Only provide 1 context snippet when 2 are expected
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Number of context snippets \\(1\\) must match number of context token sets \\(2\\)"):
            instruction.add_sample(
                context_snippets=[context_snippet1],  # Only 1 snippet, but need 2
                response_snippet=output_snippet
            )

    def test_simple_instruction_wrong_snippet_token_set_raises_error(self, simple_tokenset, user_tokenset):
        """Test that Instruction raises error when snippet doesn't match expected token set."""
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=Token("Result")
        )

        # Create snippet with wrong token set
        wrong_snippet = user_tokenset.create_snippet("Wrong context")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Snippet f.* does not match expected token set"):
            instruction.add_sample(
                context_snippets=[wrong_snippet, context_snippet2],  # First snippet has wrong token set
                response_snippet=output_snippet
            )

    def test_simple_instruction_wrong_output_snippet_token_set_raises_error(self, simple_tokenset, user_tokenset):
        """Test that Instruction raises error when output snippet doesn't match response token set."""
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=Token("Result")
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        # Create output snippet with wrong token set
        wrong_output_snippet = user_tokenset.create_snippet("Wrong output")

        with pytest.raises(ValueError, match="Snippet f.* does not match expected token set"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                response_snippet=wrong_output_snippet  # Wrong token set for output
            )

    def test_user_instruction_wrong_context_snippet_count_raises_error(self, simple_tokenset, user_tokenset):
        """Test that ExtendedInstruction raises error when context snippet count doesn't match."""
        instruction = ExtendedInstruction(
            context=[simple_tokenset, user_tokenset],
            user=user_tokenset,
            final=Token("Result")
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        # Only provide 1 context snippet when 2 are expected
        output_snippet = user_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Number of context snippets \\(1\\) must match number of context token sets \\(2\\)"):
            instruction.add_sample(
                context_snippets=[context_snippet1],  # Only 1 snippet, but need 2
                response_string="User prompt",
                output_snippet=output_snippet
            )

    def test_user_instruction_wrong_snippet_token_set_raises_error(self, simple_tokenset, user_tokenset):
        """Test that ExtendedInstruction raises error when snippet doesn't match expected token set."""
        instruction = ExtendedInstruction(
            context=[simple_tokenset, user_tokenset],
            user=user_tokenset,
            final=Token("Result")
        )

        # Create snippet with wrong token set - use a different tokenset
        wrong_tokenset = TokenSet(tokens=(Token("Wrong"),))
        wrong_snippet = wrong_tokenset.create_snippet("Wrong context")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = user_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Snippet f.* does not match expected token set"):
            instruction.add_sample(
                context_snippets=[wrong_snippet, context_snippet2],  # First snippet has wrong token set
                response_string="User prompt",
                output_snippet=output_snippet
            )

    def test_user_instruction_wrong_output_snippet_token_set_raises_error(self, simple_tokenset, user_tokenset):
        """Test that ExtendedInstruction raises error when output snippet doesn't match user token set."""
        instruction = ExtendedInstruction(
            context=[simple_tokenset, user_tokenset],
            user=user_tokenset,
            final=Token("Result")
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        # Create output snippet with wrong token set
        wrong_output_snippet = simple_tokenset.create_snippet("Wrong output")

        with pytest.raises(ValueError, match="Snippet f.* does not match expected token set"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                response_string="User prompt",
                output_snippet=wrong_output_snippet  # Wrong token set for output
            )

    def test_user_instruction_missing_prompt_raises_error(self, simple_tokenset, user_tokenset):
        """Test that ExtendedInstruction raises error when prompt is missing."""
        instruction = ExtendedInstruction(
            context=[simple_tokenset, user_tokenset],
            user=user_tokenset,
            final=Token("Result")
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = user_tokenset.create_snippet("Output")

        with pytest.raises(TypeError, match="missing 1 required positional argument: 'prompt'"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                # Missing prompt parameter
                output_snippet=output_snippet
            )

    def test_user_instruction_invalid_value_type_raises_error(self, simple_tokenset, user_tokenset):
        """Test that ExtendedInstruction raises error when value is not int or float."""
        instruction = ExtendedInstruction(
            context=[simple_tokenset, user_tokenset],
            user=user_tokenset,
            final=Token("Result")
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = user_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be None when final token is not a NumToken or NumListToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                response_string="User prompt",
                output_snippet=output_snippet,
                value="invalid_string"  # Wrong type for ExtendedInstruction
            )

    def test_user_instruction_list_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that ExtendedInstruction raises error when value is a list."""
        instruction = ExtendedInstruction(
            context=[simple_tokenset, user_tokenset],
            user=user_tokenset,
            final=Token("Result")
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = user_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be None when final token is not a NumToken or NumListToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                response_string="User prompt",
                output_snippet=output_snippet,
                value=[1, 2, 3]  # List not allowed for ExtendedInstruction
            )

    def test_simple_instruction_creation_with_user_token_in_response_raises_error(self, simple_tokenset, user_tokenset):
        """Test that Instruction raises error when created with user token in response."""
        with pytest.raises(ValueError, match="Instruction requires that the response does not contain a UserToken"):
            Instruction(
                context=[simple_tokenset],
                response=user_tokenset,  # Contains user token
                final=Token("Result")
            )

    def test_user_instruction_creation_without_user_token_raises_error(self, simple_tokenset):
        """Test that ExtendedInstruction raises error when created without user token."""
        with pytest.raises(ValueError, match="ExtendedInstruction requires a user token in the response"):
            ExtendedInstruction(
                context=[simple_tokenset],
                user=simple_tokenset,  # No user token
                final=Token("Result")
            )

    def test_instruction_creation_with_invalid_context_type_raises_error(self):
        """Test that Instruction raises error when context is not a sequence."""
        with pytest.raises(TypeError, match="All items in context must be instances of TokenSet"):
            Instruction(
                context="not_a_sequence",  # Wrong type
                response=TokenSet(tokens=(Token("Test"),)),
                final=Token("Result")
            )

    def test_instruction_creation_with_invalid_context_items_raises_error(self):
        """Test that Instruction raises error when context contains non-TokenSet items."""
        with pytest.raises(TypeError, match="All items in context must be instances of TokenSet"):
            Instruction(
                context=[TokenSet(tokens=(Token("Test"),)), "not_a_tokenset"],  # Mixed types
                response=TokenSet(tokens=(Token("Test"),)),
                final=Token("Result")
            )

    def test_instruction_creation_with_invalid_response_type_raises_error(self):
        """Test that Instruction raises error when response is not a TokenSet."""
        with pytest.raises(TypeError, match="Response must be an instance of TokenSet"):
            Instruction(
                context=[TokenSet(tokens=(Token("Test"),))],
                response="not_a_tokenset",  # Wrong type
                final=Token("Result")
            )

    def test_instruction_creation_with_invalid_final_type_raises_error(self):
        """Test that Instruction raises error when final is not a Token."""
        with pytest.raises(TypeError, match="Final must be an instance of Token"):
            Instruction(
                context=[TokenSet(tokens=(Token("Test"),))],
                response=TokenSet(tokens=(Token("Test"),)),
                final="not_a_token"  # Wrong type
            )

    def test_simple_instruction_valid_sample_succeeds(self, simple_tokenset, user_tokenset):
        """Test that Instruction accepts valid sample."""
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=Token("Result")
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        # Should not raise error
        instruction.add_sample(
            context_snippets=[context_snippet1, context_snippet2],
            response_snippet=output_snippet
        )

    def test_user_instruction_valid_sample_succeeds(self, simple_tokenset, user_tokenset):
        """Test that ExtendedInstruction accepts valid sample."""
        instruction = ExtendedInstruction(
            context=[simple_tokenset, user_tokenset],
            user=user_tokenset,
            final=Token("Result")
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = user_tokenset.create_snippet("Output")

        # Should not raise error
        instruction.add_sample(
            context_snippets=[context_snippet1, context_snippet2],
            response_string="User prompt",
            output_snippet=output_snippet
        )

    def test_user_instruction_valid_sample_with_none_value_succeeds(self, simple_tokenset, user_tokenset):
        """Test that ExtendedInstruction accepts valid sample with None value."""
        instruction = ExtendedInstruction(
            context=[simple_tokenset, user_tokenset],
            user=user_tokenset,
            final=Token("Result")
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = user_tokenset.create_snippet("Output")

        # Should not raise error
        instruction.add_sample(
            context_snippets=[context_snippet1, context_snippet2],
            response_string="User prompt",
            output_snippet=output_snippet,
            value=None  # Valid None value for non-numeric final token
        )

    def test_simple_instruction_valid_sample_with_none_value_succeeds(self, simple_tokenset, user_tokenset):
        """Test that Instruction accepts valid sample with None value."""
        instruction = Instruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=Token("Result")
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        # Should not raise error
        instruction.add_sample(
            context_snippets=[context_snippet1, context_snippet2],
            response_snippet=output_snippet,
            value=None  # Valid None value
        )