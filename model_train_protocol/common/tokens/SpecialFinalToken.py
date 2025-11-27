from typing import Optional

from . import SpecialToken
from .FinalToken import FinalToken
from .Token import Token


class SpecialFinalToken(SpecialToken, FinalToken):
    def __init__(self, value: str, key: str, desc: Optional[str] = None, special: str = None, *args, **kwargs):
        """
        Initializes a SpecialFinalToken instance.

        A SpecialToken that is also a FinalToken. Used as the default output case to preserve output behaviour.

        Users should not create instances of this class.

        :param value: The string representing the token's value.
        :param key: The key associated with the token, a symbol, emoji, or short string.
            Special Tokens should always have a key for readability.
        :param desc: Optional description of the token. Extends the value to contextualize its use.
        :param special: Special attribute to identify special tokens.
        """
        super().__init__(value, key, desc, special, *args, **kwargs)
