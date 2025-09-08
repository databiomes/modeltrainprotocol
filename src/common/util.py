import emoji


def get_possible_emojis() -> set[str]:
    """
    Generate a comprehensive set of emojis using the emoji library for cross-platform compatibility.

    Uses the emoji library, which uses the official Unicode emoji database to ensure compatibility across different OS.
    """
    emojis: set[str] = set()
    
    # Get all emoji names and their corresponding Unicode characters
    for emoji_char in emoji.EMOJI_DATA.keys():
        if len(emoji_char) > 1: # Grants roughly 1400 emojis when 1 character long and 5000 when 2 characters long
            continue
        emojis.add(emoji_char)
    
    return emojis
