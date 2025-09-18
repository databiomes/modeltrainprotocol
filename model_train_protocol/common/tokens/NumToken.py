from .Token import Token


class NumToken(Token):
    def __init__(self, value: str, min_value: int | float, max_value: int | float, key: str | None = None,
                 desc: str | None = None):
        """
        Initializes a NumToken instance.

        A NumToken is a subclass of Token that includes an additional 'num' attribute
        to indicate if the token is associated with a numerical value.

        :param value: The string representing the token's value.
        :param min_value: The minimum numerical value the token can represent.
        :param max_value: The maximum numerical value the token can represent.
        :param key: Optional key associated with the token, a symbol, emoji, or short string.
        :param desc: Optional description of the token. Extends the value to contextualize its use.
        """
        super().__init__(value, key, desc)
        self.num: int = 1
        self.protocol_representation: str = f"<Number between {min_value} and {max_value}>"
