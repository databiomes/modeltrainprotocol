from src.common.tokens.Token import Token


class UserToken(Token):
    """A UserToken is a subclass of Token that includes an additional 'user' attribute"""

    def __init__(self, value: str, key: str, desc: str | None = None):
        """
        Initializes a UserToken instance.

        A UserToken is a subclass of Token that includes an additional 'user' attribute
        to indicate that the token represents a user input.

        :param value: The string representing the token's value.
        :param key: The key associated with the token, a symbol, emoji, or short string.
        :param desc: Optional description of the token. Extends the value to contextualize its use.
        """
        super().__init__(value, key, desc)
        self.user: bool = True
