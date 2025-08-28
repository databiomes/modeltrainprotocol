def get_possible_emojis() -> list[str]:
    """Generate a list of possible emojis from Unicode code points."""
    emojis: list[str] = []
    for code_point in range(0x1F601, 0x1F64F):
        try:
            emoji: str = chr(code_point)
            emojis.append(emoji)
        except ValueError:
            continue
    return emojis
