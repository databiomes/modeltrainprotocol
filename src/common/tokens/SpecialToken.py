from src.common.tokens.Token import Token


class SpecialToken(Token):
    def __init__(self, value: str, key: str, desc: str | None = None, special: str = None):
        """
        Initializes a SpecialToken instance.

        A SpecialToken is a subclass of Token that includes an additional 'special' attribute
        to identify tokens with special significance or behavior.

        :param value: The string representing the token's value.
        :param key: The key associated with the token, a symbol, emoji, or short string.
        :param desc: Optional description of the token. Extends the value to contextualize its use.
        :param special: Special attribute to identify special tokens.
        """
        super().__init__(value, key, desc)
        self.special: str = special