class Token:
    def __init__(self, value: str, key: str, desc: str | None = None, special: str | None = None,
                 user: bool = False, num: bool = False, default: bool = False):
        """
        Initializes a Token instance.

        :param value: The string representing the token's value.
        :param key: The key associated with the token, a symbol, emoji, or short string.
        :param desc: Optional description of the token. Extends the value to contextualize its use.
        :param special: Optional special attribute to identify special tokens.
        :param user: Boolean indicating if this token represents a user input.
        :param num: Boolean indicating if this token is associated with a numerical value.
        :param default: Boolean indicating if this is a default token (like <BOS>, <EOS>).
        """
        self.value: str = value + "_" if not default else value
        self.key: str = key
        self.user: bool = user
        self.num: bool = num
        self.desc: str = desc
        self.special: str = special

    def __str__(self):
        """String representation of the token."""
        return f"Token(Value: '{self.value}', Key: '{self.key}', User: {self.user}, Num: {self.num}, Desc: {self.desc}, Special: {self.special})"

    def __hash__(self):
        """Hash based on the string representation of the token."""
        return hash(self.value)

    def __eq__(self, other):
        """
        Defines equality based on the string.
        Returns True if the other object is a Token and its string matches this token's string.
        """
        return isinstance(other, Token) and self.value == other.value

    def __dict__(self):
        """Dictionary representation of the token."""
        return self.to_dict()

    def to_dict(self):
        """Convert the token to a dictionary representation."""
        return {'value': self.value, 'key': self.key, 'user': self.user, 'num': self.num, 'desc': self.desc,
                'special': self.special}
