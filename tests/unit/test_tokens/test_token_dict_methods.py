"""
Unit tests for dictionary creation methods in Token classes.
"""
import pytest
from model_train_protocol.common.tokens.Token import Token
from model_train_protocol.common.tokens.UserToken import UserToken
from model_train_protocol.common.tokens.NumToken import NumToken
from model_train_protocol.common.constants import BOS_TOKEN, EOS_TOKEN, RUN_TOKEN, PAD_TOKEN, UNK_TOKEN, NON_TOKEN


class TestTokenDictMethods:
    """Test cases for Token dictionary creation methods."""

    def test_token_to_dict_basic(self):
        """Test basic token to_dict conversion."""
        token = Token("Test")
        token_dict = token.to_dict()
        
        expected_dict = {
            'value': 'Test_',
            'key': None,
            'user': False,
            'num': 0,
            'desc': None,
            'special': None
        }
        assert token_dict == expected_dict

    def test_token_to_dict_with_all_attributes(self):
        """Test token to_dict with all attributes."""
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

    def test_token_to_dict_with_special_token(self):
        """Test token to_dict with special token."""
        token_dict = BOS_TOKEN.to_dict()
        
        expected_dict = {
            'value': '<BOS>',
            'key': '🏁',
            'user': False,
            'num': 0,
            'desc': None,
            'special': 'start'
        }
        assert token_dict == expected_dict

    def test_token_dict_method_consistency(self):
        """Test that __dict__ method returns same as to_dict."""
        token = Token("Test", key="🔑", desc="A test token")
        
        assert token.__dict__() == token.to_dict()

    def test_token_to_dict_immutability(self):
        """Test that to_dict returns a new dictionary."""
        token = Token("Test", key="🔑", desc="A test token")
        token_dict = token.to_dict()
        
        # Modify the returned dictionary
        token_dict['key'] = 'Modified'
        
        # Original token should be unchanged
        assert token.key == '🔑'
        assert token.to_dict()['key'] == '🔑'

    def test_token_to_dict_with_none_values(self):
        """Test token to_dict with None values."""
        token = Token("Test", key=None, desc=None)
        token_dict = token.to_dict()
        
        expected_dict = {
            'value': 'Test_',
            'key': None,
            'user': False,
            'num': 0,
            'desc': None,
            'special': None
        }
        assert token_dict == expected_dict

    def test_token_to_dict_with_empty_strings(self):
        """Test token to_dict with empty string description."""
        token = Token("Test", key="🔑", desc="")
        token_dict = token.to_dict()
        
        expected_dict = {
            'value': 'Test_',
            'key': '🔑',
            'user': False,
            'num': 0,
            'desc': '',
            'special': None
        }
        assert token_dict == expected_dict

    def test_token_to_dict_unicode_handling(self):
        """Test token to_dict with unicode characters."""
        token = Token("Unicode", key="🚀🌟", desc="Unicode description with émojis")
        token_dict = token.to_dict()
        
        expected_dict = {
            'value': 'Unicode_',
            'key': '🚀🌟',
            'user': False,
            'num': 0,
            'desc': 'Unicode description with émojis',
            'special': None
        }
        assert token_dict == expected_dict

    def test_token_to_dict_long_description(self):
        """Test token to_dict with long description."""
        long_desc = "A very long description that contains multiple sentences and explains the purpose of this token in great detail. " * 5
        token = Token("Test", key="🔑", desc=long_desc)
        token_dict = token.to_dict()
        
        assert token_dict['desc'] == long_desc
        assert len(token_dict['desc']) > 100

    @pytest.mark.parametrize("value,expected_value", [
        ("Simple", "Simple_"),
        ("With_Underscore", "With_Underscore_"),
        ("With123Numbers", "With123Numbers_"),
        ("With😀Emoji", "With😀Emoji_"),
    ])
    def test_token_to_dict_various_values(self, value, expected_value):
        """Test token to_dict with various value formats."""
        token = Token(value)
        token_dict = token.to_dict()
        
        assert token_dict['value'] == expected_value

    def test_token_to_dict_key_types(self):
        """Test token to_dict with different key types."""
        # String key
        token1 = Token("Test", key="string_key")
        assert token1.to_dict()['key'] == "string_key"
        
        # Emoji key
        token2 = Token("Test", key="🔑")
        assert token2.to_dict()['key'] == "🔑"
        
        # None key
        token3 = Token("Test", key=None)
        assert token3.to_dict()['key'] is None

    def test_token_to_dict_boolean_flags(self):
        """Test token to_dict boolean flags."""
        # Regular token
        token = Token("Test")
        token_dict = token.to_dict()
        assert token_dict['user'] is False
        assert token_dict['num'] == 0
        
        # UserToken
        user_token = UserToken("User")
        user_dict = user_token.to_dict()
        assert user_dict['user'] is True
        assert user_dict['num'] == 0
        
        # NumToken
        num_token = NumToken("Count", min_value=1, max_value=10)
        num_dict = num_token.to_dict()
        assert num_dict['user'] is False
        assert num_dict['num'] == 1

    def test_token_to_dict_special_token_handling(self):
        """Test token to_dict with special tokens."""
        # BOS token
        bos_dict = BOS_TOKEN.to_dict()
        assert bos_dict['special'] == 'start'
        assert bos_dict['key'] == '🏁'
        assert bos_dict['value'] == '<BOS>'
        assert bos_dict['user'] is False
        assert bos_dict['num'] == 0
        assert bos_dict['desc'] is None
        
        # EOS token
        eos_dict = EOS_TOKEN.to_dict()
        assert eos_dict['special'] == 'end'
        assert eos_dict['key'] == '🎬'
        assert eos_dict['value'] == '<EOS>'
        assert eos_dict['user'] is False
        assert eos_dict['num'] == 0
        assert eos_dict['desc'] is None
        
        # RUN token
        run_dict = RUN_TOKEN.to_dict()
        assert run_dict['special'] == 'infer'
        assert run_dict['key'] == '🏃'
        assert run_dict['value'] == '<RUN>'
        assert run_dict['user'] is False
        assert run_dict['num'] == 0
        assert run_dict['desc'] is None
        
        # PAD token
        pad_dict = PAD_TOKEN.to_dict()
        assert pad_dict['special'] == 'pad'
        assert pad_dict['key'] == '🗒'
        assert pad_dict['value'] == '<PAD>'
        assert pad_dict['user'] is False
        assert pad_dict['num'] == 0
        assert pad_dict['desc'] is None
        
        # UNK token
        unk_dict = UNK_TOKEN.to_dict()
        assert unk_dict['special'] == 'unknown'
        assert unk_dict['key'] == '🛑'
        assert unk_dict['value'] == '<UNK>'
        assert unk_dict['user'] is False
        assert unk_dict['num'] == 0
        assert unk_dict['desc'] is None
        
        # NON token
        non_dict = NON_TOKEN.to_dict()
        assert non_dict['special'] == 'none'
        assert non_dict['key'] == '🫙'
        assert non_dict['value'] == '<NON>'
        assert non_dict['user'] is False
        assert non_dict['num'] == 0
        assert non_dict['desc'] is None

    def test_all_constant_special_tokens(self):
        """Test all constant special tokens comprehensively."""
        # Test all constant special tokens
        special_tokens = [
            (BOS_TOKEN, '<BOS>', '🏁', 'start'),
            (EOS_TOKEN, '<EOS>', '🎬', 'end'),
            (RUN_TOKEN, '<RUN>', '🏃', 'infer'),
            (PAD_TOKEN, '<PAD>', '🗒', 'pad'),
            (UNK_TOKEN, '<UNK>', '🛑', 'unknown'),
            (NON_TOKEN, '<NON>', '🫙', 'none')
        ]
        
        for token, expected_value, expected_key, expected_special in special_tokens:
            token_dict = token.to_dict()
            
            # Check all attributes
            assert token_dict['value'] == expected_value
            assert token_dict['key'] == expected_key
            assert token_dict['special'] == expected_special
            assert token_dict['user'] is False
            assert token_dict['num'] == 0
            assert token_dict['desc'] is None
            
            # Check that all expected keys are present
            expected_keys = {'value', 'key', 'user', 'num', 'desc', 'special'}
            assert set(token_dict.keys()) == expected_keys

    def test_constant_special_tokens_json_serializable(self):
        """Test that all constant special tokens produce JSON-serializable output."""
        import json
        
        special_tokens = [BOS_TOKEN, EOS_TOKEN, RUN_TOKEN, PAD_TOKEN, UNK_TOKEN, NON_TOKEN]
        
        for token in special_tokens:
            token_dict = token.to_dict()
            
            # Should not raise an exception
            json_str = json.dumps(token_dict)
            assert isinstance(json_str, str)
            
            # Should be able to deserialize
            deserialized = json.loads(json_str)
            assert deserialized == token_dict

    def test_constant_special_tokens_consistency(self):
        """Test that constant special tokens produce consistent dictionaries."""
        # Test that multiple calls to to_dict() produce identical results
        bos_dict1 = BOS_TOKEN.to_dict()
        bos_dict2 = BOS_TOKEN.to_dict()
        assert bos_dict1 == bos_dict2
        
        eos_dict1 = EOS_TOKEN.to_dict()
        eos_dict2 = EOS_TOKEN.to_dict()
        assert eos_dict1 == eos_dict2
        
        # Test that different special tokens produce different dictionaries
        assert BOS_TOKEN.to_dict() != EOS_TOKEN.to_dict()
        assert RUN_TOKEN.to_dict() != PAD_TOKEN.to_dict()
        assert UNK_TOKEN.to_dict() != NON_TOKEN.to_dict()

    def test_token_to_dict_consistency_across_instances(self):
        """Test that identical tokens produce identical dictionaries."""
        token1 = Token("Test", key="🔑", desc="A test token")
        token2 = Token("Test", key="🔑", desc="A test token")
        
        assert token1.to_dict() == token2.to_dict()

    def test_token_to_dict_different_tokens_produce_different_dicts(self):
        """Test that different tokens produce different dictionaries."""
        token1 = Token("Test1", key="🔑", desc="First token")
        token2 = Token("Test2", key="🔧", desc="Second token")
        
        assert token1.to_dict() != token2.to_dict()

    def test_token_to_dict_preserves_all_attributes(self):
        """Test that to_dict preserves all token attributes."""
        token = Token("Test", key="🔑", desc="A test token")
        token_dict = token.to_dict()
        
        # Check all expected keys are present
        expected_keys = {'value', 'key', 'user', 'num', 'desc', 'special'}
        assert set(token_dict.keys()) == expected_keys
        
        # Check values match token attributes
        assert token_dict['value'] == token.value
        assert token_dict['key'] == token.key
        assert token_dict['user'] == token.user
        assert token_dict['num'] == token.num
        assert token_dict['desc'] == token.desc
        assert token_dict['special'] == token.special

    def test_token_to_dict_json_serializable(self):
        """Test that to_dict produces JSON-serializable output."""
        import json
        
        token = Token("Test", key="🔑", desc="A test token")
        token_dict = token.to_dict()
        
        # Should not raise an exception
        json_str = json.dumps(token_dict)
        assert isinstance(json_str, str)
        
        # Should be able to deserialize
        deserialized = json.loads(json_str)
        assert deserialized == token_dict

    def test_token_to_dict_with_complex_unicode(self):
        """Test token to_dict with complex unicode characters."""
        complex_unicode = "🚀🌟🔑👤💫"
        token = Token("Complex", key=complex_unicode, desc=f"Description with {complex_unicode}")
        token_dict = token.to_dict()
        
        assert token_dict['key'] == complex_unicode
        assert complex_unicode in token_dict['desc']

    def test_token_to_dict_edge_cases(self):
        """Test token to_dict with edge cases."""
        # Token with only value
        token1 = Token("Minimal")
        dict1 = token1.to_dict()
        assert dict1['value'] == 'Minimal_'
        assert dict1['key'] is None
        assert dict1['desc'] is None
        
        # Token with empty description
        token2 = Token("Empty", desc="")
        dict2 = token2.to_dict()
        assert dict2['desc'] == ""
        
        # Token with very long key
        long_key = "🔑" * 50
        token3 = Token("LongKey", key=long_key)
        dict3 = token3.to_dict()
        assert dict3['key'] == long_key
