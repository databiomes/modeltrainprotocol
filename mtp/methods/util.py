def get_possible_emojis():
    emojis = []
    for code_point in range(0x1F601, 0x1F64F):
        try:
            emoji = chr(code_point)
            emojis.append(emoji)
        except ValueError:
            continue
    return emojis