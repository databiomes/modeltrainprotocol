from typing import Optional

from .Token import Token


class FinalToken(Token):

    def __init__(self, value: str, key: Optional[str] = None, desc: Optional[str] = None, *args, **kwargs):
        """
        Initializes a FinalToken instance.

        A FinalToken designates the final action or output expected from the model.

        It cannot be used as part of a TokenSet input context, only as a final output token.

        :param value: The string representing the token's value.
        :param key: The key associated with the token, a symbol, emoji, or short string.
        :param desc: Optional description of the token. Extends the value to contextualize its use.
        """
        super().__init__(value, key, desc)
        self.input: bool = False
