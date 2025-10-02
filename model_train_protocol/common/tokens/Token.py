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
        self._key: str | None = key
        self.desc: str = desc
        self.user: bool = False
        self.num: int = 0
        self.special: str | None = None
        self.validate_value()
        self.validate_key()

    @property
    def key(self) -> str:
        """Returns the key"""
        return self._key

    @key.setter
    def key(self, new_key: str):
        """Sets the key and validates it"""
        self._key = new_key
        self.validate_key()

    def validate_key(self):
        """
        Validates that all characters in the key are valid according to the emoji library.

        :return: True if all characters in the string are valid characters or emojis, False otherwise.
        """

        if not isinstance(self.key, str) and self.key is not None:
            raise TypeError("Key must be a string or None.")

        if self.key == "":
            raise ValueError("Key cannot be an empty string.")

        if self.key is None:
            return

        for c in self.key:
            if not (c == '_' or c.isalnum() or emoji.is_emoji(c)):
                raise ValueError(
                    f"Invalid character '{c}' found in key '{self.key}'. Only alphanumeric characters, underscores, and emojis recommended for general interchange by Unicode.org are allowed.")

    def validate_value(self):
        """
        Validates that all characters in the value are valid according to the emoji library.

        :return: True if all characters in the string are valid characters or emojis, False otherwise.
        """
        if self.value is None:
            raise ValueError("Value cannot be None.")

        if self.value == "" or self.value == "_":
            raise ValueError("Value cannot be an empty string.")

        for c in self.value:
            if not (c == '_' or c.isalnum() or emoji.is_emoji(c)):
                raise ValueError(
                    f"Invalid character '{c}' found in value '{self.value}'. Only alphanumeric characters, underscores, and emojis are allowed.")

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
