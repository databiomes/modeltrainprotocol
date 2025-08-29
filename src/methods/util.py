def get_possible_emojis() -> set[str]:
    """Generate a list of possible emojis from Unicode code points."""
    emojis: set[str] = set()
    for code_point in range(0x1F601, 0x1F64F):
        try:
            emoji: str = chr(code_point)
            emojis.add(emoji)
        except ValueError:
            continue
    return emojis
