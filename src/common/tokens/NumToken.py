from src.common.tokens.Token import Token


class NumToken(Token):
    def __init__(self, value: str, key: str, desc: str | None = None):
        """
        Initializes a NumToken instance.

        A NumToken is a subclass of Token that includes an additional 'num' attribute
        to indicate if the token is associated with a numerical value.

        :param value: The string representing the token's value.
        :param key: The key associated with the token, a symbol, emoji, or short string.
        :param desc: Optional description of the token. Extends the value to contextualize its use.
        """
        super().__init__(value, key, desc)
        self.num: bool = True
