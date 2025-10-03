"""
Unit tests for sample creation and validation with NumToken and NumListToken result tokens.
Tests error handling when values are not provided or wrong types are provided.
"""

import pytest
from model_train_protocol.common.tokens import Token, NumToken, NumListToken, UserToken
from model_train_protocol.common.tokens import TokenSet
from model_train_protocol.common.instructions import SimpleInstruction, UserInstruction


class TestSampleValueValidation:
    """Test sample value validation for numeric result tokens."""

    def test_numtoken_result_missing_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumToken result token raises error when value is not provided."""
        num_token = NumToken("Count", min_value=1, max_value=10)
        instruction = SimpleInstruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=num_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as a number when final token is a NumToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                output_snippet=output_snippet
                # Missing value parameter
            )

    def test_numtoken_result_wrong_type_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumToken result token raises error when value is wrong type."""
        num_token = NumToken("Count", min_value=1, max_value=10)
        instruction = SimpleInstruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=num_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as a number when final token is a NumToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                output_snippet=output_snippet,
                value="invalid_string"  # Wrong type
            )

    def test_numtoken_result_none_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumToken result token raises error when value is None."""
        num_token = NumToken("Count", min_value=1, max_value=10)
        instruction = SimpleInstruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=num_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as a number when final token is a NumToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                output_snippet=output_snippet,
                value=None  # None value
            )

    def test_numtoken_result_valid_numeric_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumToken result token raises error when value is numeric but not NumToken instance."""
        num_token = NumToken("Count", min_value=1, max_value=10)
        instruction = SimpleInstruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=num_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        # Should raise error - validation expects NumToken instance, not numeric value
        with pytest.raises(ValueError, match="Value must be provided as a number when final token is a NumToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                output_snippet=output_snippet,
                value=5  # Pass a numeric value
            )

    def test_numlisttoken_result_missing_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token raises error when value is not provided."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=3)
        instruction = SimpleInstruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=numlist_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as a list of numbers when final token is a NumListToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                output_snippet=output_snippet
                # Missing value parameter
            )

    def test_numlisttoken_result_wrong_type_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token raises error when value is wrong type."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=3)
        instruction = SimpleInstruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=numlist_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as a list of numbers when final token is a NumListToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                output_snippet=output_snippet,
                value="invalid_string"  # Wrong type
            )

    def test_numlisttoken_result_none_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token raises error when value is None."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=3)
        instruction = SimpleInstruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=numlist_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as a list of numbers when final token is a NumListToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                output_snippet=output_snippet,
                value=None  # None value
            )

    def test_numlisttoken_result_valid_list_value_succeeds(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token accepts valid list value."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=3)
        instruction = SimpleInstruction(
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
            output_snippet=output_snippet,
            value=[1, 2, 3]  # Valid list value
        )

    def test_regular_token_result_none_value_allowed(self, simple_tokenset, user_tokenset):
        """Test that regular Token result token allows None value."""
        regular_token = Token("Result")
        instruction = SimpleInstruction(
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
            output_snippet=output_snippet,
            value=None  # None value allowed for regular tokens
        )

    def test_user_token_result_none_value_allowed(self, simple_tokenset, user_tokenset):
        """Test that UserToken result token allows None value."""
        user_token = UserToken("User")
        instruction = UserInstruction(
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
            prompt="User prompt",
            output_snippet=output_snippet,
            value=None  # None value allowed for user tokens
        )

    def test_regular_token_result_non_none_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that regular Token result token raises error when value is not None."""
        regular_token = Token("Result")
        instruction = SimpleInstruction(
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
                output_snippet=output_snippet,
                value="some_value"  # Non-None value not allowed for regular tokens
            )

    def test_user_token_result_non_none_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that UserToken result token raises error when value is not None."""
        user_token = UserToken("User")
        instruction = UserInstruction(
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
                prompt="User prompt",
                output_snippet=output_snippet,
                value="some_value"  # Non-None value not allowed for user tokens
            )

    def test_numtoken_result_list_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumToken result token raises error when value is a list."""
        num_token = NumToken("Count", min_value=1, max_value=10)
        instruction = SimpleInstruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=num_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as a number when final token is a NumToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                output_snippet=output_snippet,
                value=[1, 2, 3]  # List value not allowed for NumToken
            )

    def test_numlisttoken_result_numtoken_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token raises error when value is a NumToken."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=3)
        num_token = NumToken("Count", min_value=1, max_value=10)
        instruction = SimpleInstruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=numlist_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as a list of numbers when final token is a NumListToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                output_snippet=output_snippet,
                value=num_token  # NumToken value not allowed for NumListToken
            )

    def test_numlisttoken_result_dict_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token raises error when value is a dict."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=3)
        instruction = SimpleInstruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=numlist_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as a list of numbers when final token is a NumListToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                output_snippet=output_snippet,
                value={"key": "value"}  # Dict value not allowed
            )

    def test_numlisttoken_result_boolean_value_raises_error(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token raises error when value is a boolean."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=3)
        instruction = SimpleInstruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=numlist_token
        )

        context_snippet1 = simple_tokenset.create_snippet("Context 1")
        context_snippet2 = user_tokenset.create_snippet("Context 2")
        output_snippet = simple_tokenset.create_snippet("Output")

        with pytest.raises(ValueError, match="Value must be provided as a list of numbers when final token is a NumListToken"):
            instruction.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                output_snippet=output_snippet,
                value=True  # Boolean value not allowed
            )

    def test_numlisttoken_result_empty_list_succeeds(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token accepts empty list."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=0)
        instruction = SimpleInstruction(
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
            output_snippet=output_snippet,
            value=[]  # Empty list
        )

    def test_numlisttoken_result_single_element_list_succeeds(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token accepts single element list."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=1)
        instruction = SimpleInstruction(
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
            output_snippet=output_snippet,
            value=[50]  # Single element list
        )

    def test_numlisttoken_result_multi_element_list_succeeds(self, simple_tokenset, user_tokenset):
        """Test that NumListToken result token accepts multi-element list."""
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=5)
        instruction = SimpleInstruction(
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
            output_snippet=output_snippet,
            value=[10, 20, 30, 40, 50]  # Multi-element list
        )

    def test_mixed_token_types_value_validation(self, simple_tokenset, user_tokenset):
        """Test value validation with mixed token types in instruction."""
        num_token = NumToken("Count", min_value=1, max_value=10)
        numlist_token = NumListToken("Coordinates", min_value=1, max_value=100, length=3)
        regular_token = Token("Result")
        
        # Test with NumToken
        instruction1 = SimpleInstruction(
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
                output_snippet=output_snippet,
                value="invalid"
            )
        
        # Test with NumListToken
        instruction2 = SimpleInstruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=numlist_token
        )
        
        # Should require list
        with pytest.raises(ValueError):
            instruction2.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                output_snippet=output_snippet,
                value="invalid"
            )
        
        # Test with regular Token
        instruction3 = SimpleInstruction(
            context=[simple_tokenset, user_tokenset],
            response=simple_tokenset,
            final=regular_token
        )
        
        # Should allow None only
        instruction3.add_sample(
            context_snippets=[context_snippet1, context_snippet2],
            output_snippet=output_snippet,
            value=None
        )
        
        # Should not allow non-None values
        with pytest.raises(ValueError):
            instruction3.add_sample(
                context_snippets=[context_snippet1, context_snippet2],
                output_snippet=output_snippet,
                value="any_value"
            )