from src.common.tokens.Token import Token


class DefaultSpecialToken(Token):
    def __init__(self, value: str, key: str, desc: str | None = None, special: str = None):
        """
        Initializes a DefaultSpecialToken instance.

        A DefaultSpecialToken is a subclass of Token that includes an additional 'special' attribute
        to identify tokens with special significance or behavior.

        It differs from SpecialToken in that it is internally assigned and
        does not remove the trailing underscore from the value.

        Users should not create instances of this class directly. Use SpecialToken when defining tokens.

        :param value: The string representing the token's value.
        :param key: The key associated with the token, a symbol, emoji, or short string.
        :param desc: Optional description of the token. Extends the value to contextualize its use.
        :param special: Special attribute to identify special tokens.
        """
        super().__init__(value, key, desc)
        # Overwrite value to not have trailing underscore
        self.value: str = self.value[:-1]
        self.special: str = special
