from typing import Optional, Union

from .Token import Token
from model_train_protocol.errors import TokenError


class NumListToken(Token):
    def __init__(self, value: str, min_value: Union[int, float], max_value: Union[int, float], length: int,
                 key: Optional[str] = None, desc: Optional[str] = None, *args, **kwargs):
        """
        Initializes a NumListToken instance.

        A NumListToken is a special type of Token that represents a list of numbers.

        :param value: The string representing the token's value.
        :param min_value: The minimum numerical value an element in the list can represent.
        :param max_value: The maximum numerical value an element in the list can represent.
        :param length: The number of elements in the list.
        :param key: Optional key associated with the token, a symbol, emoji, or short string.
        :param desc: Optional description of the token. Extends the value to contextualize its use.
        """
        super().__init__(value=value, key=key, desc=desc)

        if length <= 0:
            raise TokenError("Length of NumListToken must be a positive non-zero integer.")
        if max_value < min_value:
            raise TokenError("Num value must be greater than or equal to max_value.")

        self.num_list: int = length
        self.min_value: float | int = min_value
        self.max_value: float | int = max_value
        self.length: int = length
        self.template_representation: str = f"<num_{min_value}_{max_value}_{length}>"
