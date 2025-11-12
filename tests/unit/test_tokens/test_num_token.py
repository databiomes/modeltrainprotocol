"""
Unit tests for the NumToken class.
"""
import pytest
from model_train_protocol.common.tokens.NumToken import NumToken


class TestNumToken:
    """Test cases for the NumToken class."""

    def test_num_token_creation_basic(self):
        """Test basic numeric token creation."""
        token = NumToken("Count", min_value=1, max_value=10)
        assert token.value == "Count_"
        assert token.key is None
        assert token.desc is None
        assert token.num == 1  # NumToken should have num=1
        assert token.special is None
        assert token.protocol_representation == "<num_1_10>"

    def test_num_token_creation_with_key(self):
        """Test numeric token creation with key."""
        token = NumToken("Count", key="🔢", min_value=1, max_value=10)
        assert token.value == "Count_"
        assert token.key == "🔢"
        assert token.num == 1

    def test_num_token_creation_with_description(self):
        """Test numeric token creation with description."""
        token = NumToken("Count", min_value=1, max_value=10, desc="A numeric token")
        assert token.value == "Count_"
        assert token.desc == "A numeric token"
        assert token.num == 1

    def test_num_token_creation_complete(self):
        """Test numeric token creation with all parameters."""
        token = NumToken("Count", key="🔢", min_value=1, max_value=10, desc="A numeric token")
        assert token.value == "Count_"
        assert token.key == "🔢"
        assert token.desc == "A numeric token"
        assert token.num == 1
        assert token.protocol_representation == "<num_1_10>"

    def test_num_token_equality_same_tokens(self):
        """Test numeric token equality with same tokens."""
        token1 = NumToken("Count", min_value=1, max_value=10)
        token2 = NumToken("Count", min_value=1, max_value=10)
        assert token1 == token2

    def test_num_token_equality_different_tokens(self):
        """Test numeric token equality with different tokens."""
        token1 = NumToken("Count1", min_value=1, max_value=10)
        token2 = NumToken("Count2", min_value=1, max_value=10)
        assert token1 != token2

    def test_num_token_equality_different_ranges(self):
        """Test numeric token equality with different ranges."""
        token1 = NumToken("Count", min_value=1, max_value=10)
        token2 = NumToken("Count", min_value=1, max_value=5)
        assert token1 != token2

    def test_num_token_equality_with_regular_token(self):
        """Test numeric token equality with regular token."""
        from model_train_protocol.common.tokens.Token import Token
        num_token = NumToken("Count", min_value=1, max_value=10)
        regular_token = Token("Count")
        # Should be different because they are different types
        assert num_token != regular_token

    def test_num_token_hash_same_tokens(self):
        """Test numeric token hash with same tokens."""
        token1 = NumToken("Count", min_value=1, max_value=10)
        token2 = NumToken("Count", min_value=1, max_value=10)
        assert hash(token1) == hash(token2)

    def test_num_token_hash_different_tokens(self):
        """Test numeric token hash with different tokens."""
        token1 = NumToken("Count1", min_value=1, max_value=10)
        token2 = NumToken("Count2", min_value=1, max_value=10)
        # Hash values might be the same due to collision, but tokens should be different
        assert token1 != token2

    def test_num_token_string_representation(self):
        """Test numeric token string representation."""
        token = NumToken("Count", key="🔢", min_value=1, max_value=10, desc="A numeric token")
        str_repr = str(token)
        assert "Token(" in str_repr
        assert "Value: 'Count_'" in str_repr
        assert "Key: '🔢'" in str_repr
        assert "Num: True" in str_repr  # Should show num=True
        assert "Desc: A numeric token" in str_repr
        assert "Special: None" in str_repr

    def test_num_token_to_dict(self):
        """Test numeric token to dictionary conversion."""
        token = NumToken("Count", key="🔢", min_value=1, max_value=10, desc="A numeric token")
        token_dict = token.to_dict()
        
        expected_dict = {
            'value': 'Count_',
            'key': '🔢',
            'num': 1,  # Should be 1 for NumToken
            'num_list': 0,
            'desc': 'A numeric token',
            'special': None
        }
        assert token_dict == expected_dict

    def test_num_token_dict_method(self):
        """Test numeric token __dict__ method."""
        token = NumToken("Count", key="🔢", min_value=1, max_value=10, desc="A numeric token")
        token_dict = token.__dict__()
        
        expected_dict = {
            'value': 'Count_',
            'key': '🔢',
            'num': 1,  # Should be 1 for NumToken
            'num_list': 0,
            'desc': 'A numeric token',
            'special': None
        }
        assert token_dict == expected_dict

    def test_num_token_inheritance(self):
        """Test that NumToken inherits from Token."""
        from model_train_protocol.common.tokens.Token import Token
        token = NumToken("Count", min_value=1, max_value=10)
        assert isinstance(token, Token)

    def test_num_token_num_flag(self):
        """Test that NumToken always has num=1."""
        token = NumToken("Count", min_value=1, max_value=10)
        assert token.num == 1

    def test_num_token_with_emoji_key(self):
        """Test numeric token with emoji key."""
        token = NumToken("Count", key="🔢", min_value=1, max_value=10)
        assert token.key == "🔢"
        assert token.num == 1

    def test_num_token_with_alphanumeric_key(self):
        """Test numeric token with alphanumeric key."""
        token = NumToken("Count", key="count123", min_value=1, max_value=10)
        assert token.key == "count123"
        assert token.num == 1

    def test_num_token_without_key(self):
        """Test numeric token without key."""
        token = NumToken("Count", min_value=1, max_value=10)
        assert token.key is None
        assert token.num == 1

    def test_num_token_without_description(self):
        """Test numeric token without description."""
        token = NumToken("Count", key="🔢", min_value=1, max_value=10)
        assert token.desc is None
        assert token.num == 1

    def test_num_token_minimal_creation(self):
        """Test minimal numeric token creation."""
        token = NumToken("Count", min_value=1, max_value=10)
        assert token.value == "Count_"
        assert token.key is None
        assert token.desc is None
        assert token.num == 1

    def test_num_token_long_description(self):
        """Test numeric token with long description."""
        long_desc = "A numeric token with a very long description that explains its purpose in detail"
        token = NumToken("Count", key="🔢", min_value=1, max_value=10, desc=long_desc)
        assert token.desc == long_desc
        assert token.num == 1

    def test_num_token_unicode_characters(self):
        """Test numeric token with unicode characters."""
        token = NumToken("Count", key="🔢🌟", min_value=1, max_value=10)
        assert token.value == "Count_"
        assert token.key == "🔢🌟"
        assert token.num == 1

    def test_num_token_key_validation(self):
        """Test numeric token key validation (inherited from Token)."""
        # Valid key
        token = NumToken("Count", key="🔢", min_value=1, max_value=10)
        assert token.key == "🔢"
        
        # Invalid key should raise ValueError
        with pytest.raises(ValueError, match="Invalid character"):
            NumToken("Count", key="Invalid@Key", min_value=1, max_value=10)

    def test_num_token_value_validation(self):
        """Test numeric token value validation (inherited from Token)."""
        # Valid value
        token = NumToken("Count", min_value=1, max_value=10)
        assert token.value == "Count_"
        
        # Invalid value should raise ValueError
        with pytest.raises(ValueError, match="Invalid character"):
            NumToken("Invalid@Count", min_value=1, max_value=10)

    def test_num_token_key_setter(self):
        """Test numeric token key setter (inherited from Token)."""
        token = NumToken("Count", min_value=1, max_value=10)
        assert token.key is None
        
        token.key = "🔢"
        assert token.key == "🔢"
        assert token.num == 1
        
        # Test validation on setter
        with pytest.raises(ValueError, match="Invalid character"):
            token.key = "Invalid@Key"

    def test_num_token_range_validation(self):
        """Test numeric token range validation."""
        # Valid range
        token = NumToken("Count", min_value=1, max_value=10)
        assert token.min_value == 1
        assert token.max_value == 10
        
        # Test edge case: same min and max
        token = NumToken("Count", min_value=5, max_value=5)
        assert token.min_value == 5
        assert token.max_value == 5

    def test_num_token_negative_values(self):
        """Test numeric token with negative values."""
        token = NumToken("Count", min_value=-10, max_value=-1)
        assert token.min_value == -10
        assert token.max_value == -1
        assert token.num == 1

    def test_num_token_zero_values(self):
        """Test numeric token with zero values."""
        token = NumToken("Count", min_value=0, max_value=0)
        assert token.min_value == 0
        assert token.max_value == 0
        assert token.num == 1

    def test_num_token_wide_range(self):
        """Test numeric token with wide range."""
        token = NumToken("Count", min_value=0, max_value=1000)
        assert token.min_value == 0
        assert token.max_value == 1000
        assert token.num == 1

    @pytest.mark.parametrize("valid_char", [
        "a", "Z", "0", "9", "_", "😀", "🚀", "🌟", "🔑", "🔢"
    ])
    def test_num_token_value_valid_characters(self, valid_char):
        """Test numeric token value with various valid characters."""
        token = NumToken(f"Count{valid_char}", min_value=1, max_value=10)
        assert token.value == f"Count{valid_char}_"
        assert token.num == 1

    @pytest.mark.parametrize("invalid_char", [
        "@", "#", "$", "%", "^", "&", "*", "(", ")", "+", "=", "[", "]", "{", "}", "|", "\\", ":", ";", "'", '"', ",", ".", "<", ">", "/", "?", " ", "\t", "\n"
    ])
    def test_num_token_value_invalid_characters(self, invalid_char):
        """Test numeric token value with various invalid characters."""
        with pytest.raises(ValueError, match="Invalid character"):
            NumToken(f"Count{invalid_char}", min_value=1, max_value=10)

    @pytest.mark.parametrize("valid_key", [
        "ValidKey", "Valid_Key", "Valid123", "🔢", "😀", "🚀🌟", "count123", "count_key"
    ])
    def test_num_token_key_valid_characters(self, valid_key):
        """Test numeric token key with various valid characters."""
        token = NumToken("Count", key=valid_key, min_value=1, max_value=10)
        assert token.key == valid_key
        assert token.num == 1

    @pytest.mark.parametrize("invalid_key", [
        "Invalid@Key", "Invalid#Key", "Invalid Key", "Invalid.Key", "Invalid,Key"
    ])
    def test_num_token_key_invalid_characters(self, invalid_key):
        """Test numeric token key with various invalid characters."""
        with pytest.raises(ValueError, match="Invalid character"):
            NumToken("Count", key=invalid_key, min_value=1, max_value=10)

    @pytest.mark.parametrize("min_val,max_val", [
        (1, 10), (0, 100), (-10, 10), (5, 5), (0, 0), (-100, -1)
    ])
    def test_num_token_various_ranges(self, min_val, max_val):
        """Test numeric token with various ranges."""
        token = NumToken("Count", min_value=min_val, max_value=max_val)
        assert token.num == 1
        assert token.protocol_representation == f"<num_{min_val}_{max_val}>"

