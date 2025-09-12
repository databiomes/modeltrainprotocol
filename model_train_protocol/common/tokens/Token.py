import emoji


class Token:
    """The lowest level unit for a model. Represents a word, symbol, or concept."""

    def __init__(self, value: str, key: str | None = None, desc: str | None = None):
        """
        Initializes a Token instance.

        :param value: The string representing the token's value.
        :param key: The key associated with the token, a symbol, emoji, or short string.
        :param desc: Optional description of the token. Extends the value to contextualize its use.
        """
        self.value: str = value + "_"
        self.key: str | None = key
        self.desc: str = desc
        self.user: bool = False
        self.num: int = 0
        self.special: str | None = None

    def validate_key(self):
        """
        Validates that all characters in the key are valid according to the emoji library.

        :return: True if all characters in the string are valid characters or emojis, False otherwise.
        """
        if self.key is None:
            raise ValueError("Key is None, cannot validate.")

        invalid_emojis = []

        for char in self.key:
            # Uses the emoji library to check if the character is a valid emoji recommended by Unicode
            if emoji.emoji_count(char) >= 1 and not emoji.is_emoji(char):
                invalid_emojis.append(char)

        if len(invalid_emojis) > 0:
            raise ValueError(f"Invalid emojis found in key '{self.key}': {invalid_emojis}")

    def __str__(self):
        """String representation of the token."""
        return f"Token(Value: '{self.value}', Key: '{self.key}', User: {self.user}, Num: {self.num}, Desc: {self.desc}, Special: {self.special})"

    def __hash__(self):
        """Hash based on the string representation of the token."""
        return hash(self.value)

    def __eq__(self, other):
        """
        Defines equality based on the string.
        Returns True if the other object is of the same Token subclass and its string matches this token's string.
        """
        return isinstance(other, self.__class__) and self.value == other.value

    def __dict__(self):
        """Dictionary representation of the token."""
        return self.to_dict()

    def to_dict(self):
        """Convert the token to a dictionary representation."""
        return {'value': self.value, 'key': self.key, 'user': self.user, 'num': self.num, 'desc': self.desc,
                'special': self.special}
