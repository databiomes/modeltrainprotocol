"""
Unit tests for the TokenSet class.
"""
import pytest

from model_train_protocol import NumListToken
from model_train_protocol.common.tokens.TokenSet import TokenSet, Snippet
from model_train_protocol.common.tokens.Token import Token
from model_train_protocol.common.tokens.UserToken import UserToken
from model_train_protocol.common.tokens.NumToken import NumToken


class TestTokenSet:
    """Test cases for the TokenSet class."""

    def test_token_set_creation_basic(self):
        """Test basic token set creation."""
        token1 = Token("Token1")
        token2 = Token("Token2")
        token_set = TokenSet(tokens=(token1, token2))
        
        assert len(token_set.tokens) == 2
        assert token1 in token_set.tokens
        assert token2 in token_set.tokens
        assert token_set.guardrail is None

    def test_token_set_creation_single_token(self):
        """Test token set creation with single token."""
        token = Token("Single")
        token_set = TokenSet(tokens=(token,))
        
        assert len(token_set.tokens) == 1
        assert token in token_set.tokens

    def test_token_set_creation_multiple_tokens(self):
        """Test token set creation with multiple tokens."""
        tokens = [Token(f"Token{i}") for i in range(5)]
        token_set = TokenSet(tokens=tuple(tokens))
        
        assert len(token_set.tokens) == 5
        for token in tokens:
            assert token in token_set.tokens

    def test_token_set_creation_empty(self):
        """Test token set creation with empty tokens."""
        token_set = TokenSet(tokens=())
        assert len(token_set.tokens) == 0

    def test_token_set_key_generation(self):
        """Test token set key generation."""
        token1 = Token("Token1", key="🔑")
        token2 = Token("Token2", key="🔧")
        token_set = TokenSet(tokens=(token1, token2))
        
        # Key should be generated based on token keys
        assert token_set.key is not None
        assert isinstance(token_set.key, str)

    def test_token_set_key_consistency(self):
        """Test that token set key is consistent for same tokens."""
        token1 = Token("Token1", key="🔑")
        token2 = Token("Token2", key="🔧")
        token_set1 = TokenSet(tokens=(token1, token2))
        token_set2 = TokenSet(tokens=(token1, token2))
        
        assert token_set1.key == token_set2.key

    def test_token_set_key_different_order(self):
        """Test that token set key is different with different order."""
        token1 = Token("Token1", key="🔑")
        token2 = Token("Token2", key="🔧")
        token_set1 = TokenSet(tokens=(token1, token2))
        token_set2 = TokenSet(tokens=(token2, token1))
        
        assert token_set1.key != token_set2.key

    def test_token_set_equality_same_tokens(self):
        """Test token set equality with same tokens."""
        token1 = Token("Token1")
        token2 = Token("Token2")
        token_set1 = TokenSet(tokens=(token1, token2))
        token_set2 = TokenSet(tokens=(token1, token2))
        
        assert token_set1 == token_set2

    def test_token_set_equality_different_tokens(self):
        """Test token set equality with different tokens."""
        token1 = Token("Token1")
        token2 = Token("Token2")
        token3 = Token("Token3")
        token_set1 = TokenSet(tokens=(token1, token2))
        token_set2 = TokenSet(tokens=(token1, token3))
        
        assert token_set1 != token_set2

    def test_token_set_equality_different_order(self):
        """Test token set equality with different token order."""
        token1 = Token("Token1")
        token2 = Token("Token2")
        token_set1 = TokenSet(tokens=(token1, token2))
        token_set2 = TokenSet(tokens=(token2, token1))
        
        assert token_set1 != token_set2

    def test_token_set_hash_same_tokens(self):
        """Test token set hash with same tokens."""
        token1 = Token("Token1")
        token2 = Token("Token2")
        token_set1 = TokenSet(tokens=(token1, token2))
        token_set2 = TokenSet(tokens=(token1, token2))
        
        assert hash(token_set1) == hash(token_set2)

    def test_token_set_hash_different_tokens(self):
        """Test token set hash with different tokens."""
        token1 = Token("Token1")
        token2 = Token("Token2")
        token3 = Token("Token3")
        token_set1 = TokenSet(tokens=(token1, token2))
        token_set2 = TokenSet(tokens=(token1, token3))
        
        # Hash values might be the same due to collision, but sets should be different
        assert token_set1 != token_set2


    def test_token_set_contains_user_token(self):
        """Test token set user token detection."""
        user_token = UserToken("User")
        regular_token = Token("Regular")
        
        # Token set with user token
        user_set = TokenSet(tokens=(user_token, regular_token))
        assert user_set.is_user is True
        
        # Token set without user token
        regular_set = TokenSet(tokens=(regular_token,))
        assert regular_set.is_user is False

    def test_token_set_create_snippet_basic(self):
        """Test token set snippet creation."""
        token = Token("Test")
        token_set = TokenSet(tokens=(token,))
        
        snippet = token_set.create_snippet("Test string")
        assert isinstance(snippet, Snippet)
        assert snippet.string == "Test string"
        assert snippet.token_set_key == token_set.key

    def test_token_set_create_snippet_with_numbers(self):
        """Test token set snippet creation with numbers."""
        num_token = NumToken("Count", min_value=1, max_value=10)
        token_set = TokenSet(tokens=(num_token,))
        
        snippet = token_set.create_snippet("Count to 5", numbers=[5])
        assert isinstance(snippet, Snippet)
        assert snippet.string == "Count to 5"
        assert snippet.numbers == [5]
        assert snippet.token_set_key == token_set.key

    def test_token_set_create_snippet_without_numbers(self):
        """Test token set snippet creation without numbers."""
        token = Token("Test")
        token_set = TokenSet(tokens=(token,))
        
        snippet = token_set.create_snippet("Test string")
        assert isinstance(snippet, Snippet)
        assert snippet.string == "Test string"
        assert snippet.numbers == []
        assert snippet.token_set_key == token_set.key

    def test_token_set_create_snippet_empty_string(self):
        """Test token set snippet creation with empty string."""
        token = Token("Test")
        token_set = TokenSet(tokens=(token,))
        
        snippet = token_set.create_snippet("")
        assert isinstance(snippet, Snippet)
        assert snippet.string == ""
        assert snippet.token_set_key == token_set.key

    def test_token_set_create_snippet_none_string(self):
        """Test token set snippet creation with None string."""
        token = Token("Test")
        token_set = TokenSet(tokens=(token,))

        with pytest.raises(TypeError):
            token_set.create_snippet(None)

    def test_token_set_create_snippet_multiple_numbers(self):
        """Test token set snippet creation with multiple numbers."""
        num_token1 = NumToken("Count1", min_value=1, max_value=10)
        num_token2 = NumToken("Count2", min_value=1, max_value=10)
        token_set = TokenSet(tokens=(num_token1, num_token2))
        
        snippet = token_set.create_snippet("Count to 5 and 7", numbers=[5, 7])
        assert isinstance(snippet, Snippet)
        assert snippet.string == "Count to 5 and 7"
        assert snippet.numbers == [5, 7]
        assert snippet.token_set_key == token_set.key

    def test_token_set_numbers_outside_limit(self):
        """Test token set snippet creation with mismatched numbers."""
        num_token = NumListToken("Count", min_value=1, max_value=10, length=3)
        token_set = TokenSet(tokens=(num_token,))

        with pytest.raises(ValueError):
            token_set.create_snippet("Count to 5", numbers=[5, 7, 19])

    def test_token_set_too_few_numbers(self):
        """Test token set snippet creation with mismatched numbers."""
        num_token = NumListToken("Count", min_value=1, max_value=10, length=3)
        token_set = TokenSet(tokens=(num_token,))

        with pytest.raises(ValueError):
            token_set.create_snippet("Count to 5", numbers=[5, 7])

    def test_token_set_with_mixed_token_types(self):
        """Test token set with mixed token types."""
        regular_token = Token("Regular")
        user_token = UserToken("User")
        num_token = NumToken("Count", min_value=1, max_value=10)
        
        token_set = TokenSet(tokens=(regular_token, user_token, num_token))
        
        assert len(token_set.tokens) == 3
        assert regular_token in token_set.tokens
        assert user_token in token_set.tokens
        assert num_token in token_set.tokens
        assert token_set.is_user is True

    def test_token_set_with_only_user_tokens(self):
        """Test token set with only user tokens."""
        user_token1 = UserToken("User1")
        user_token2 = UserToken("User2")
        
        token_set = TokenSet(tokens=(user_token1, user_token2))
        
        assert len(token_set.tokens) == 2
        assert user_token1 in token_set.tokens
        assert user_token2 in token_set.tokens
        assert token_set.is_user is True

    def test_token_set_with_only_regular_tokens(self):
        """Test token set with only regular tokens."""
        token1 = Token("Token1")
        token2 = Token("Token2")
        
        token_set = TokenSet(tokens=(token1, token2))
        
        assert len(token_set.tokens) == 2
        assert token1 in token_set.tokens
        assert token2 in token_set.tokens
        assert token_set.is_user is False

    def test_token_set_with_only_numeric_tokens(self):
        """Test token set with only numeric tokens."""
        num_token1 = NumToken("Count1", min_value=1, max_value=10)
        num_token2 = NumToken("Count2", min_value=1, max_value=10)
        
        token_set = TokenSet(tokens=(num_token1, num_token2))
        
        assert len(token_set.tokens) == 2
        assert num_token1 in token_set.tokens
        assert num_token2 in token_set.tokens
        assert token_set.is_user is False

    def test_token_set_duplicate_tokens(self):
        """Test token set with duplicate tokens."""
        token = Token("Duplicate")
        token_set = TokenSet(tokens=(token, token))
        
        # Should handle duplicates gracefully
        assert len(token_set.tokens) == 2
        assert token in token_set.tokens

    def test_token_set_key_with_none_keys(self):
        """Test token set key generation with None keys."""
        token1 = Token("Token1")  # No key
        token2 = Token("Token2")  # No key
        token_set = TokenSet(tokens=(token1, token2))
        
        # Should still generate a key
        assert token_set.key is not None
        assert isinstance(token_set.key, str)

    def test_token_set_key_with_mixed_keys(self):
        """Test token set key generation with mixed keys."""
        token1 = Token("Token1", key="🔑")
        token2 = Token("Token2")  # No key
        token_set = TokenSet(tokens=(token1, token2))
        
        # Should generate a key based on available keys
        assert token_set.key is not None
        assert isinstance(token_set.key, str)

    @pytest.mark.parametrize("token_count", [1, 2, 5, 10])
    def test_token_set_various_sizes(self, token_count):
        """Test token set with various numbers of tokens."""
        tokens = [Token(f"Token{i}") for i in range(token_count)]
        token_set = TokenSet(tokens=tuple(tokens))
        
        assert len(token_set.tokens) == token_count
        for token in tokens:
            assert token in token_set.tokens

    def test_token_set_equality_with_guardrail(self):
        """Test token set equality with guardrail."""
        from model_train_protocol.common.guardrails import Guardrail
        
        token = UserToken("Test")
        token_set1 = TokenSet(tokens=(token,))
        token_set2 = TokenSet(tokens=(token,))
        
        # Initially equal
        assert token_set1 == token_set2
        
        # Add guardrail to one
        guardrail = Guardrail(
            good_prompt="Good prompt",
            bad_prompt="Bad prompt",
            bad_output="Bad output"
        )
        token_set1.set_guardrail(guardrail)
        
        # Should still be equal (guardrail doesn't affect equality)
        assert token_set1 == token_set2

