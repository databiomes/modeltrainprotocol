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
        if len(emoji_char) > 1:  # Grants roughly 1400 emojis when 1 character long
            continue
        emojis.add(emoji_char)

    return emojis


def get_extended_possible_emojis() -> set[str]:
    """
    Generate an extended set of emojis including multi-character emojis using the emoji library for cross-platform compatibility.
    """
    return set(emoji.EMOJI_DATA.keys())  # Returns roughly 5000 emojis that can be multi-character


def hash_string(key: str, output_char: int = 6) -> str:
    """
    Hashes a string into.
    """
    return hashlib.sha256(key.encode()).hexdigest()[:output_char]


def validate_string_set(string_set: set[str]):
    """
    Checks if any string in a set is a perfect substring of another.

    :param string_set: A set of strings.
    :raises ValueError: If any string is a perfect substring of another (case insensitive).
    """
    # Sort the list by length, longest to shortest.
    sorted_strings = sorted(list(string_set), key=len, reverse=False)

    # Iterate through the strings and check for perfect subsets.
    for i in range(len(sorted_strings)):
        for j in range(i + 1, len(sorted_strings)):
            # If a shorter string is a perfect substring of a longer one, return False.

            # Only keep alphanumeric characters for comparison
            first_string: str = ''.join(c.lower() for c in sorted_strings[i] if c.isalnum())
            second_string: str = ''.join(c.lower() for c in sorted_strings[j] if c.isalnum())

            if first_string in second_string:
                raise ValueError(
                    f"'{sorted_strings[i]}' is a substring of '{sorted_strings[j]}' (alphanumeric characters only, case insensitive).")
