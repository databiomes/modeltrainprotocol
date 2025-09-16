import emoji
import hashlib


def get_possible_emojis() -> set[str]:
    """
    Generate a comprehensive set of emojis using the emoji library for cross-platform compatibility.

    Uses the emoji library, which uses the official Unicode emoji database to ensure compatibility across different OS.
    """
    emojis: set[str] = set()
    
    # Get all emoji names and their corresponding Unicode characters
    for emoji_char in emoji.EMOJI_DATA.keys():
        if len(emoji_char) > 1: # Grants roughly 1400 emojis when 1 character long
            continue
        emojis.add(emoji_char)
    
    return emojis

def get_extended_possible_emojis() -> set[str]:

    """
    Generate an extended set of emojis including multi-character emojis using the emoji library for cross-platform compatibility.
    """
    return set(emoji.EMOJI_DATA.keys()) # Returns roughly 5000 emojis that can be multi-character


def hash_string(key: str, output_char: int = 6) -> str:
    """
    Hashes a string into.
    """
    return hashlib.sha256(key.encode()).hexdigest()[:output_char]

