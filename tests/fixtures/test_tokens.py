"""
Sample token data for testing.
"""
from typing import Dict, List, Any, Union, Tuple
from model_train_protocol import Token, UserToken, NumToken, NumListToken, TokenSet

TOKEN_ENGLISH = Token("English")

# Characters
TOKEN_ALICE = UserToken("Alice")
TOKEN_CAT = Token("Cat")

# Scenes
TOKEN_TREE = Token("Tree",
                   desc="Perched in a tree, surrounded by a dense fog where nothing can be seen past a few feet, the Cheshire Cat sits smiling on a branch.")
# Actions
TOKEN_TALK = Token("Talk")

# Result
TOKEN_CONTINUE = Token("Continue")

# Num Tokens
TOKEN_SENTENCE_LENGTH = NumToken("SentenceLength", min_value=1, max_value=20,
                           desc="The number of words in the sentence, between 1 and 20.")

TOKEN_COORDINATES: NumListToken = NumListToken("Coordinates", min_value=-100, max_value=100, length=3,
                                               desc="3D coordinates (x, y, z)")

# Create the token sets for the instructions
SIMPLE_TOKENSET = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK))
SIMPLE_NUMTOKEN_TOKENSET = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_SENTENCE_LENGTH)) # NumToken
SIMPLE_NUMLISTTOKEN_TOKENSET = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_COORDINATES)) # NumListToken
SIMPLE_NUMTOKEN_NUMLISTTOKEN_TOKENSET = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_CAT, TOKEN_TALK, TOKEN_SENTENCE_LENGTH, TOKEN_COORDINATES)) # Both NumToken and NumListToken

USER_TOKENSET = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK))
USER_NUMTOKEN_TOKENSET = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_SENTENCE_LENGTH)) # NumToken
USER_NUMLILSTTOKEN_TOKENSET = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_COORDINATES)) # NumListToken
USER_NUMTOKEN_NUMLISTTOKEN_TOKENSET = TokenSet(tokens=(TOKEN_TREE, TOKEN_ENGLISH, TOKEN_ALICE, TOKEN_TALK, TOKEN_SENTENCE_LENGTH, TOKEN_COORDINATES)) # Both NumToken and NumListToken


def get_valid_keyless_tokens() -> Dict[str, Union[Token, UserToken, NumToken, NumListToken]]:
    """Get a collection of valid keyless tokens for testing."""
    return {
        'basic': Token("Basic", desc="A basic token"),
        'user': UserToken("User", desc="A user token"),
        'numeric': NumToken("Count", min_value=1, max_value=10, desc="A numeric token"),
        'num_list': NumListToken("Numbers", desc="A numeric list token", min_value=1, max_value=5, length=3),
        'with_desc': Token("Described", desc="A token with description"),
        'emoji_key': Token("Emoji", desc="A token with emoji key"),
        'alphanumeric_key': Token("Alpha", desc="A token with alphanumeric key"),
        'underscore_key': Token("Underscore", desc="A token with underscore key"),
        'no_key': Token("NoKey", desc="A token without key"),
        'no_desc': Token("NoDesc"),
        'minimal': Token("Minimal"),
        'long_desc': Token("LongDesc", desc="A token with a very long description that explains its purpose in detail"),
        'special_chars': Token("Special", desc="A token with special characters in key"),
        'unicode': Token("Unicode", desc="A token with unicode characters"),
        'numeric_range': NumToken("Range", min_value=0, max_value=100, desc="A token with wide numeric range"),
        'single_value': NumToken("Single", min_value=5, max_value=5, desc="A token with single numeric value")
    }


def get_invalid_tokens() -> Dict[str, Tuple[Any, ...]]:
    """Get a collection of invalid token configurations for testing."""
    return {
        'invalid_char_value': ("Test@", "🔑", "Invalid character in value"),
        'invalid_char_key': ("Test", "Key#", "Invalid character in key"),
        'empty_value': ("", "🔑", "Empty value"),
        'none_value': (None, "🔑", "None value"),
        'invalid_emoji_key': ("Test", "invalid_emoji", "Invalid emoji in key"),
        'numeric_invalid_range': ("Count", "🔢", "Invalid numeric range", 10, 5),  # min > max
        'numeric_negative_min': ("Count", "🔢", "Negative minimum value", -1, 10),
        'numeric_zero_max': ("Count", "🔢", "Zero maximum value", 1, 0)
    }


def get_token_equality_pairs() -> List[Tuple[Union[Token, UserToken, NumToken], Union[Token, UserToken, NumToken], bool]]:
    """Get pairs of tokens for testing equality."""
    return [
        (Token("Same"), Token("Same"), True),
        (Token("Different"), Token("Same"), False),
        (UserToken("User"), UserToken("User"), True),
        (UserToken("User"), Token("User"), False),  # Different types
        (NumToken("Count", min_value=1, max_value=10), NumToken("Count", min_value=1, max_value=10), True),
        (NumToken("Count", min_value=1, max_value=10), NumToken("Count", min_value=1, max_value=5), False),
    ]


def get_token_hash_pairs() -> List[Tuple[Union[Token, UserToken, NumToken], Union[Token, UserToken, NumToken], bool]]:
    """Get pairs of tokens for testing hashing."""
    return [
        (Token("HashTest"), Token("HashTest"), True),  # Same hash
        (Token("HashTest1"), Token("HashTest2"), False),  # Different hash
        (UserToken("UserHash"), UserToken("UserHash"), True),
        (NumToken("NumHash", min_value=1, max_value=10), NumToken("NumHash", min_value=1, max_value=10), True),
    ]


def get_token_serialization_data() -> Dict[str, Dict[str, Any]]:
    """Get token data for testing serialization."""
    return {
        'basic_token': {
            'token': Token("Serial", desc="Serialization test"),
            'expected_dict': {
                'value': 'Serial_',
                'key': '🔧',
                'user': False,
                'num': 0,
                'desc': 'Serialization test',
                'special': None
            }
        },
        'user_token': {
            'token': UserToken("UserSerial", key="👤", desc="User serialization test"),
            'expected_dict': {
                'value': 'UserSerial_',
                'key': '👤',
                'user': True,
                'num': 0,
                'desc': 'User serialization test',
                'special': None
            }
        },
        'numeric_token': {
            'token': NumToken("NumSerial", key="🔢", min_value=1, max_value=10, desc="Numeric serialization test"),
            'expected_dict': {
                'value': 'NumSerial_',
                'key': '🔢',
                'user': False,
                'num': 1,
                'desc': 'Numeric serialization test',
                'special': None
            }
        }
    }
