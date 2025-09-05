class Token:
    """The lowest level unit for a model. Represents a word, symbol, or concept."""

    def __init__(self, value: str, key: str, desc: str | None = None):
        """
        Initializes a Token instance.

        :param value: The string representing the token's value.
        :param key: The key associated with the token, a symbol, emoji, or short string.
        :param desc: Optional description of the token. Extends the value to contextualize its use.
        """
        self.value: str = value + "_"
        self.key: str = key
        self.desc: str = desc
        self.user: bool = False
        self.num: bool = False
        self.special: str | None = None

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
