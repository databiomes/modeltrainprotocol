"""
Unit tests for the Token class.
"""
import pytest
from model_train_protocol.common.tokens.Token import Token


class TestToken:
    """Test cases for the Token class."""

    def test_token_creation_basic(self):
        """Test basic token creation."""
        token = Token("Test")
        assert token.value == "Test_"
        assert token.key is None
        assert token.desc is None
        assert token.user is False
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
        assert "User: False" in str_repr
        assert "Num: 0" in str_repr
        assert "Desc: A test token" in str_repr
        assert "Special: None" in str_repr

    def test_token_to_dict(self):
        """Test token to dictionary conversion."""
        token = Token("Test", key="🔑", desc="A test token")
        token_dict = token.to_dict()
        
        expected_dict = {
            'value': 'Test_',
            'key': '🔑',
            'user': False,
            'num': 0,
            'desc': 'A test token',
            'special': None
        }
        assert token_dict == expected_dict

    def test_token_dict_method(self):
        """Test token __dict__ method."""
        token = Token("Test", key="🔑", desc="A test token")
        token_dict = token.__dict__()
        
        expected_dict = {
            'value': 'Test_',
            'key': '🔑',
            'user': False,
            'num': 0,
            'desc': 'A test token',
            'special': None
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

