from .Token import Token


class SpecialToken(Token):
    def __init__(self, value: str, key: str, desc: str | None = None, special: str = None):
        """
        Initializes a SpecialToken instance.

        A SpecialToken is a subclass of Token that includes an additional 'special' attribute
        to identify tokens with special significance or behavior. Also removes the trailing underscore from the value.

        Users should not create instances of this class.

        :param value: The string representing the token's value.
        :param key: The key associated with the token, a symbol, emoji, or short string.
            Special Tokens should always have a key for readability.
        :param desc: Optional description of the token. Extends the value to contextualize its use.
        :param special: Special attribute to identify special tokens.
        """
        super().__init__(value, key, desc)
        # Overwrite value to not have trailing underscore
        self.value: str = self.value[:-1]
        self.special: str = special

    def validate_value(self):
        """
        Special Tokens are valid by default as they are created internally
        """
        pass

    def validate_key(self):
        """
        Special Tokens are valid by default as they are created internally
        """
        pass
