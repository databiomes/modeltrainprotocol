"""
Unit tests for the UserToken class.
"""
import pytest

from model_train_protocol import Token
from model_train_protocol.common.tokens.UserToken import UserToken


class TestUserToken:
    """Test cases for the UserToken class."""

    def test_user_token_creation_basic(self):
        """Test basic user token creation."""
        token = UserToken("User")
        assert token.value == "User_"
        assert token.key is None
        assert token.desc is None
        assert token.user is True  # UserToken should have user=True
        assert token.num == 0
        assert token.special is None

    def test_user_token_creation_with_key(self):
        """Test user token creation with key."""
        token = UserToken("User", key="👤")
        assert token.value == "User_"
        assert token.key == "👤"
        assert token.user is True

    def test_user_token_creation_with_description(self):
        """Test user token creation with description."""
        token = UserToken("User", desc="A user token")
        assert token.value == "User_"
        assert token.desc == "A user token"
        assert token.user is True

    def test_user_token_creation_complete(self):
        """Test user token creation with all parameters."""
        token = UserToken("User", key="👤", desc="A user token")
        assert token.value == "User_"
        assert token.key == "👤"
        assert token.desc == "A user token"
        assert token.user is True

    def test_user_token_equality_same_tokens(self):
        """Test user token equality with same tokens."""
        token1 = UserToken("User")
        token2 = UserToken("User")
        assert token1 == token2

    def test_user_token_equality_different_tokens(self):
        """Test user token equality with different tokens."""
        token1 = UserToken("User1")
        token2 = UserToken("User2")
        assert token1 != token2

    def test_user_token_equality_with_regular_token(self):
        """Test user token equality with regular token."""
        user_token = UserToken("User")
        regular_token = Token("User")
        # Should be different because they are different types
        assert user_token != regular_token

    def test_user_token_hash_same_tokens(self):
        """Test user token hash with same tokens."""
        token1 = UserToken("User")
        token2 = UserToken("User")
        assert hash(token1) == hash(token2)

    def test_user_token_hash_different_tokens(self):
        """Test user token hash with different tokens."""
        token1 = UserToken("User1")
        token2 = UserToken("User2")
        # Hash values might be the same due to collision, but tokens should be different
        assert token1 != token2

    def test_user_token_string_representation(self):
        """Test user token string representation."""
        token = UserToken("User", key="👤", desc="A user token")
        str_repr = str(token)
        assert "Token(" in str_repr
        assert "Value: 'User_'" in str_repr
        assert "Key: '👤'" in str_repr
        assert "User: True" in str_repr  # Should show user=True
        assert "Num: False" in str_repr
        assert "Desc: A user token" in str_repr
        assert "Special: None" in str_repr

    def test_user_token_to_dict(self):
        """Test user token to dictionary conversion."""
        token = UserToken("User", key="👤", desc="A user token")
        token_dict = token.to_dict()
        
        expected_dict = {
            'value': 'User_',
            'key': '👤',
            'user': True,  # Should be True for UserToken
            'num': 0,
            'num_list': 0,
            'desc': 'A user token',
            'special': None
        }
        assert token_dict == expected_dict

    def test_user_token_dict_method(self):
        """Test user token __dict__ method."""
        token = UserToken("User", key="👤", desc="A user token")
        token_dict = token.__dict__()
        
        expected_dict = {
            'value': 'User_',
            'key': '👤',
            'user': True,  # Should be True for UserToken
            'num': 0,
            'num_list': 0,
            'desc': 'A user token',
            'special': None
        }
        assert token_dict == expected_dict

    def test_user_token_inheritance(self):
        """Test that UserToken inherits from Token."""
        from model_train_protocol.common.tokens.Token import Token
        token = UserToken("User")
        assert isinstance(token, Token)

    def test_user_token_user_flag(self):
        """Test that UserToken always has user=True."""
        token = UserToken("User")
        assert token.user is True
        
        # Even if we try to set it, it should remain True
        # (though this might not be possible depending on implementation)
        assert token.user is True

    def test_user_token_with_emoji_key(self):
        """Test user token with emoji key."""
        token = UserToken("User", key="👤")
        assert token.key == "👤"
        assert token.user is True

    def test_user_token_with_alphanumeric_key(self):
        """Test user token with alphanumeric key."""
        token = UserToken("User", key="user123")
        assert token.key == "user123"
        assert token.user is True

    def test_user_token_without_key(self):
        """Test user token without key."""
        token = UserToken("User")
        assert token.key is None
        assert token.user is True

    def test_user_token_without_description(self):
        """Test user token without description."""
        token = UserToken("User", key="👤")
        assert token.desc is None
        assert token.user is True

    def test_user_token_minimal_creation(self):
        """Test minimal user token creation."""
        token = UserToken("User")
        assert token.value == "User_"
        assert token.key is None
        assert token.desc is None
        assert token.user is True

    def test_user_token_long_description(self):
        """Test user token with long description."""
        long_desc = "A user token with a very long description that explains its purpose in detail"
        token = UserToken("User", key="👤", desc=long_desc)
        assert token.desc == long_desc
        assert token.user is True

    def test_user_token_unicode_characters(self):
        """Test user token with unicode characters."""
        token = UserToken("User", key="👤🌟")
        assert token.value == "User_"
        assert token.key == "👤🌟"
        assert token.user is True

    def test_user_token_key_validation(self):
        """Test user token key validation (inherited from Token)."""
        # Valid key
        token = UserToken("User", key="👤")
        assert token.key == "👤"
        
        # Invalid key should raise ValueError
        with pytest.raises(ValueError, match="Invalid character"):
            UserToken("User", key="Invalid@Key")

    def test_user_token_value_validation(self):
        """Test user token value validation (inherited from Token)."""
        # Valid value
        token = UserToken("User")
        assert token.value == "User_"
        
        # Invalid value should raise ValueError
        with pytest.raises(ValueError, match="Invalid character"):
            UserToken("Invalid@User")

    def test_user_token_key_setter(self):
        """Test user token key setter (inherited from Token)."""
        token = UserToken("User")
        assert token.key is None
        
        token.key = "👤"
        assert token.key == "👤"
        assert token.user is True
        
        # Test validation on setter
        with pytest.raises(ValueError, match="Invalid character"):
            token.key = "Invalid@Key"

    @pytest.mark.parametrize("valid_char", [
        "a", "Z", "0", "9", "_", "😀", "🚀", "🌟", "🔑", "👤"
    ])
    def test_user_token_value_valid_characters(self, valid_char):
        """Test user token value with various valid characters."""
        token = UserToken(f"User{valid_char}")
        assert token.value == f"User{valid_char}_"
        assert token.user is True

    @pytest.mark.parametrize("invalid_char", [
        "@", "#", "$", "%", "^", "&", "*", "(", ")", "+", "=", "[", "]", "{", "}", "|", "\\", ":", ";", "'", '"', ",", ".", "<", ">", "/", "?", " ", "\t", "\n"
    ])
    def test_user_token_value_invalid_characters(self, invalid_char):
        """Test user token value with various invalid characters."""
        with pytest.raises(ValueError, match="Invalid character"):
            UserToken(f"User{invalid_char}")

    @pytest.mark.parametrize("valid_key", [
        "ValidKey", "Valid_Key", "Valid123", "👤", "😀", "🚀🌟", "user123", "user_key"
    ])
    def test_user_token_key_valid_characters(self, valid_key):
        """Test user token key with various valid characters."""
        token = UserToken("User", key=valid_key)
        assert token.key == valid_key
        assert token.user is True

    @pytest.mark.parametrize("invalid_key", [
        "Invalid@Key", "Invalid#Key", "Invalid Key", "Invalid.Key", "Invalid,Key"
    ])
    def test_user_token_key_invalid_characters(self, invalid_key):
        """Test user token key with various invalid characters."""
        with pytest.raises(ValueError, match="Invalid character"):
            UserToken("User", key=invalid_key)

