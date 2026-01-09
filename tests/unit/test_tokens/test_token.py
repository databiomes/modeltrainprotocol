"""
Unit tests for the Token class.
"""
import pytest
from model_train_protocol.common.tokens.Token import Token
from model_train_protocol.common.util import validate_string_subset


class TestToken:
    """Test cases for the Token class."""

    def test_token_creation_basic(self):
        """Test basic token creation."""
        token = Token("Test")
        assert token.value == "Test_"
        assert token.key is None
        assert token.desc is None
        assert token.num == 0
        assert token.special is None

    def test_token_creation_with_key(self):
        """Test token creation with key."""
        token = Token("Test", key="🔑")
        assert token.value == "Test_"
        assert token.key == "🔑"

    def test_token_creation_with_description(self):
        """Test token creation with description."""
        token = Token("Test", desc="A test token")
        assert token.value == "Test_"
        assert token.desc == "A test token"

    def test_token_creation_complete(self):
        """Test token creation with all parameters."""
        token = Token("Test", key="🔑", desc="A test token")
        assert token.value == "Test_"
        assert token.key == "🔑"
        assert token.desc == "A test token"

    def test_token_value_validation_valid(self):
        """Test token value validation with valid characters."""
        # Should not raise any exception
        Token("ValidToken")
        Token("Valid_Token")
        Token("Valid123")
        Token("Valid😀")

    def test_token_value_validation_invalid_character(self):
        """Test token value validation with invalid characters."""
        with pytest.raises(ValueError, match="Invalid character"):
            Token("Invalid@Token")
        
        with pytest.raises(ValueError, match="Invalid character"):
            Token("Invalid#Token")
        
        with pytest.raises(ValueError, match="Invalid character"):
            Token("Invalid Token")  # Space

    def test_token_key_validation_valid(self):
        """Test token key validation with valid characters."""
        # Should not raise any exception
        Token("Test", key="ValidKey")
        Token("Test", key="Valid_Key")
        Token("Test", key="Valid123")
        Token("Test", key="🔑")
        Token("Test", key="Valid😀")

    def test_token_key_validation_invalid_character(self):
        """Test token key validation with invalid characters."""
        with pytest.raises(ValueError, match="Invalid character"):
            Token("Test", key="Invalid@Key")
        
        with pytest.raises(ValueError, match="Invalid character"):
            Token("Test", key="Invalid#Key")
        
        with pytest.raises(ValueError, match="Invalid character"):
            Token("Test", key="Invalid Key")  # Space

    def test_token_key_setter(self):
        """Test token key setter."""
        token = Token("Test")
        assert token.key is None
        
        token.key = "🔑"
        assert token.key == "🔑"
        
        # Test validation on setter
        with pytest.raises(ValueError, match="Invalid character"):
            token.key = "Invalid@Key"

    def test_token_equality_same_tokens(self):
        """Test token equality with same tokens."""
        token1 = Token("Test")
        token2 = Token("Test")
        assert token1 == token2
        assert token1.__eq__(token2)

    def test_token_equality_different_tokens(self):
        """Test token equality with different tokens."""
        token1 = Token("Test1")
        token2 = Token("Test2")
        assert token1 != token2

    def test_token_equality_different_types(self):
        """Test token equality with different types."""
        token = Token("Test")
        assert token != "Test"
        assert token != 123
        assert token != None

    def test_token_hash_same_tokens(self):
        """Test token hash with same tokens."""
        token1 = Token("Test")
        token2 = Token("Test")
        assert hash(token1) == hash(token2)

    def test_token_hash_different_tokens(self):
        """Test token hash with different tokens."""
        token1 = Token("Test1")
        token2 = Token("Test2")
        # Hash values might be the same due to collision, but tokens should be different
        assert token1 != token2

    def test_token_string_representation(self):
        """Test token string representation."""
        token = Token("Test", key="🔑", desc="A test token")
        str_repr = str(token)
        assert "Token(" in str_repr
        assert "Value: 'Test_'" in str_repr
        assert "Key: '🔑'" in str_repr
        assert "Num: False" in str_repr
        assert "Desc: A test token" in str_repr
        assert "Special: None" in str_repr

    def test_token_to_dict(self):
        """Test token to dictionary conversion."""
        token = Token("Test", key="🔑", desc="A test token")
        token_dict = token.to_dict()
        
        expected_dict = {
            'value': 'Test_',
            'key': '🔑',
            'num': 0,
            'num_list': 0,
            'desc': 'A test token',
            'special': None,
            'type': 'Token'
        }
        assert token_dict == expected_dict

    def test_token_dict_method(self):
        """Test token __dict__ method."""
        token = Token("Test", key="🔑", desc="A test token")
        token_dict = token.__dict__()
        
        expected_dict = {
            'value': 'Test_',
            'key': '🔑',
            'num': 0,
            'num_list': 0,
            'desc': 'A test token',
            'special': None,
            'type': 'Token'
        }
        assert token_dict == expected_dict

    def test_token_with_emoji_key(self):
        """Test token with emoji key."""
        token = Token("Test", key="😀")
        assert token.key == "😀"

    def test_token_with_alphanumeric_key(self):
        """Test token with alphanumeric key."""
        token = Token("Test", key="abc123")
        assert token.key == "abc123"

    def test_token_with_underscore_key(self):
        """Test token with underscore key."""
        token = Token("Test", key="test_key")
        assert token.key == "test_key"

    def test_token_without_key(self):
        """Test token without key."""
        token = Token("Test")
        assert token.key is None

    def test_token_without_description(self):
        """Test token without description."""
        token = Token("Test", key="🔑")
        assert token.desc is None

    def test_token_minimal_creation(self):
        """Test minimal token creation."""
        token = Token("Minimal")
        assert token.value == "Minimal_"
        assert token.key is None
        assert token.desc is None

    def test_token_long_description(self):
        """Test token with long description."""
        long_desc = "A token with a very long description that explains its purpose in detail"
        token = Token("Test", key="🔑", desc=long_desc)
        assert token.desc == long_desc

    def test_token_unicode_characters(self):
        """Test token with unicode characters."""
        token = Token("Unicode", key="🚀🌟")
        assert token.value == "Unicode_"
        assert token.key == "🚀🌟"

    def test_token_special_characters_in_key(self):
        """Test token with special characters in key (should be invalid)."""
        with pytest.raises(ValueError, match="Invalid character"):
            Token("Test", key="!@#$%")

    def test_token_empty_string_value(self):
        """Test token with empty string value (should be invalid)."""
        with pytest.raises(ValueError):
            Token("")

    def test_token_none_value(self):
        """Test token with None value (should be invalid)."""
        with pytest.raises(TypeError):
            Token(None)

    def test_token_key_none(self):
        """Test token with None key."""
        token = Token("Test", key=None)
        assert token.key is None

    def test_token_key_validation_on_empty(self):
        """Test token key validation when key is empty."""
        with pytest.raises(ValueError, match="Key cannot be an empty string."):
            Token("Test", key="")

    @pytest.mark.parametrize("valid_char", [
        "a", "Z", "0", "9", "_", "😀", "🚀", "🌟", "🔑", "👤"
    ])
    def test_token_value_valid_characters(self, valid_char):
        """Test token value with various valid characters."""
        token = Token(f"Test{valid_char}")
        assert token.value == f"Test{valid_char}_"

    @pytest.mark.parametrize("invalid_char", [
        "@", "#", "$", "%", "^", "&", "*", "(", ")", "+", "=", "[", "]", "{", "}", "|", "\\", ":", ";", "'", '"', ",", ".", "<", ">", "/", "?", " ", "\t", "\n"
    ])
    def test_token_value_invalid_characters(self, invalid_char):
        """Test token value with various invalid characters."""
        with pytest.raises(ValueError, match="Invalid character"):
            Token(f"Test{invalid_char}")

    @pytest.mark.parametrize("invalid_char", [
        "🐦‍🔥", "⃝"
    ])
    def test_token_value_invalid_emojis(self, invalid_char):
        """Test token value with various invalid characters."""
        with pytest.raises(ValueError, match="Invalid character"):
            Token(f"Test{invalid_char}")

    @pytest.mark.parametrize("valid_key", [
        "ValidKey", "Valid_Key", "Valid123", "🔑", "😀", "🚀🌟", "abc123", "test_key"
    ])
    def test_token_key_valid_characters(self, valid_key):
        """Test token key with various valid characters."""
        token = Token("Test", key=valid_key)
        assert token.key == valid_key


    @pytest.mark.parametrize("invalid_key", [
        "Invalid@Key", "Invalid#Key", "Invalid Key", "Invalid.Key", "Invalid,Key"
    ])
    def test_token_key_invalid_characters(self, invalid_key):
        """Test token key with various invalid characters."""
        with pytest.raises(ValueError, match="Invalid character"):
            Token("Test", key=invalid_key)

    @pytest.mark.parametrize("invalid_key", [
        "🐦‍🔥", "⃝"
    ])
    def test_token_key_invalid_emojis(self, invalid_key):
        """Test token key with various invalid characters."""
        with pytest.raises(ValueError, match="Invalid character"):
            Token("Test", key=invalid_key)


class TestTokenSubstringValidation:
    """Test cases for token substring validation."""

    def test_validate_string_set_no_substrings(self):
        """Test validate_string_set with no substring relationships."""
        string_set = {"Apple", "Banana", "Cherry", "Date"}
        # Should not raise any exception
        validate_string_subset(string_set)

    def test_validate_string_set_perfect_substring_raises_error(self):
        """Test validate_string_set with perfect substring relationships."""
        # "Dog" should be detected as substring of "Dog_" (first match found)
        string_set = {"Cat", "Cat_", "Dog", "Dog_"}
        with pytest.raises(ValueError, match="is a substring of"):
            validate_string_subset(string_set)

    def test_validate_string_set_case_insensitive_substring(self):
        """Test validate_string_set with case insensitive substring detection."""
        # "cat" should be detected as substring of "Cat_" (first match found)
        string_set = {"cat", "Cat_", "dog", "Dog_"}
        with pytest.raises(ValueError, match="is a substring of"):
            validate_string_subset(string_set)

    def test_validate_string_set_alphanumeric_only_comparison(self):
        """Test validate_string_set with alphanumeric-only comparison."""
        # "Test" should be detected as substring of "Test_123"
        string_set = {"Test", "Test_123", "Sample", "Sample_456"}
        with pytest.raises(ValueError, match="is a substring of"):
            validate_string_subset(string_set)

    def test_validate_string_set_emoji_handling(self):
        """Test validate_string_set with emoji characters."""
        # Emojis should be preserved in comparison
        string_set = {"😀", "😀_", "🚀", "🚀_"}
        with pytest.raises(ValueError, match=" substring of "):
            validate_string_subset(string_set)

    def test_validate_string_set_mixed_content(self):
        """Test validate_string_set with mixed alphanumeric and special characters."""
        # "Data" should be detected as substring of "Data_456" (first match found)
        string_set = {"Token", "Token_123", "Data", "Data_456"}
        with pytest.raises(ValueError, match="is a substring of"):
            validate_string_subset(string_set)

    def test_validate_string_set_special_characters_ignored(self):
        """Test validate_string_set ignores special characters in comparison."""
        # "Test" should be detected as substring of "Test@#$%"
        string_set = {"Test", "Test@#$%", "Sample", "Sample!@#$"}
        with pytest.raises(ValueError, match="is a substring of 'Test@#"):
            validate_string_subset(string_set)

    def test_validate_string_set_empty_set(self):
        """Test validate_string_set with empty set."""
        string_set = set()
        # Should not raise any exception
        validate_string_subset(string_set)

    def test_validate_string_set_single_string(self):
        """Test validate_string_set with single string."""
        string_set = {"Single"}
        # Should not raise any exception
        validate_string_subset(string_set)

    def test_validate_string_set_identical_strings(self):
        """Test validate_string_set with identical strings."""
        string_set = {"Duplicate", "Duplicate", "Unique"}
        # Should not raise any exception (identical strings are not substrings)
        validate_string_subset(string_set)

    def test_validate_string_set_reverse_order(self):
        """Test validate_string_set with longer string first."""
        # "Short" should be detected as substring of "Short_" (first match found)
        string_set = {"LongerString_", "LongerString", "Short", "Short_"}
        with pytest.raises(ValueError, match="is a substring of"):
            validate_string_subset(string_set)

    def test_validate_string_set_multiple_substrings(self):
        """Test validate_string_set with multiple substring relationships."""
        string_set = {"A", "AB", "ABC", "ABCD"}
        # Should raise error for the first substring found
        with pytest.raises(ValueError, match="is a substring of"):
            validate_string_subset(string_set)

    def test_validate_string_set_unicode_characters(self):
        """Test validate_string_set with unicode characters."""
        string_set = {"αβγ", "αβγ_", "δεζ", "δεζ_"}
        with pytest.raises(ValueError, match="is a substring of"):
            validate_string_subset(string_set)

    def test_validate_string_set_numbers_only(self):
        """Test validate_string_set with numeric strings."""
        string_set = {"123", "1234", "567", "5678"}
        with pytest.raises(ValueError, match="is a substring of"):
            validate_string_subset(string_set)

    def test_validate_string_set_mixed_case_substring(self):
        """Test validate_string_set with mixed case substring detection."""
        string_set = {"test", "TEST_", "sample", "SAMPLE_"}
        with pytest.raises(ValueError, match="is a substring of"):
            validate_string_subset(string_set)

    def test_validate_string_set_complex_patterns(self):
        """Test validate_string_set with complex alphanumeric patterns."""
        string_set = {"Token123", "Token123_", "Data456", "Data456_"}
        with pytest.raises(ValueError, match="is a substring of"):
            validate_string_subset(string_set)

    def test_validate_string_set_whitespace_handling(self):
        """Test validate_string_set with whitespace in strings."""
        # Whitespace should be ignored in comparison
        string_set = {"Test", "Test ", "Sample", "Sample "}
        with pytest.raises(ValueError, match="is a substring of"):
            validate_string_subset(string_set)

    def test_validate_string_set_punctuation_ignored(self):
        """Test validate_string_set ignores punctuation in comparison."""
        string_set = {"Word", "Word.", "Text", "Text!"}
        with pytest.raises(ValueError, match="is a substring of"):
            validate_string_subset(string_set)

    def test_validate_string_set_long_strings(self):
        """Test validate_string_set with longer strings."""
        long_string = "ThisIsAVeryLongStringThatShouldNotBeASubstring"
        longer_string = "ThisIsAVeryLongStringThatShouldNotBeASubstring_"
        string_set = {long_string, longer_string, "Other", "Other_"}
        with pytest.raises(ValueError, match="is a substring of"):
            validate_string_subset(string_set)

    def test_validate_string_set_edge_case_single_character(self):
        """Test validate_string_set with single character strings."""
        string_set = {"A", "AB", "C", "CD"}
        with pytest.raises(ValueError, match="is a substring of"):
            validate_string_subset(string_set)

    def test_validate_string_set_no_common_prefix(self):
        """Test validate_string_set with strings that have no common prefix."""
        string_set = {"Apple", "Banana", "Cherry", "Date"}
        # Should not raise any exception
        validate_string_subset(string_set)

    def test_validate_string_set_partial_matches_are_substrings(self):
        """Test validate_string_set with partial matches that are substrings."""
        string_set = {"Test", "Testing", "Sample", "Sampling"}
        # "Test" is a substring of "Testing", so should raise error
        with pytest.raises(ValueError, match="is a substring of"):
            validate_string_subset(string_set)

    def test_validate_string_set_special_unicode_substring(self):
        """Test validate_string_set with special unicode substring relationships."""
        string_set = {"🚀", "🚀_", "🌟", "🌟_"}
        with pytest.raises(ValueError, match=" substring of "):
            validate_string_subset(string_set)

