from typing import Optional, Union

from .Token import Token


class NumToken(Token):
    def __init__(self, value: str, min_value: Union[int, float], max_value: Union[int, float], key: Optional[str] = None,
                 desc: Optional[str] = None, *args, **kwargs):
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
        if max_value < min_value:
            raise ValueError("Num value must be greater than or equal to max_value.")

        super().__init__(value, key, desc)
        self.num: bool = True
        self.min_value: Union[int, float] = min_value
        self.max_value: Union[int, float] = max_value
        self.template_representation: str = f"<num_{min_value}_{max_value}>"

    def __eq__(self, other):
        """Equality comparison for NumToken."""
        if not isinstance(other, NumToken):
            return False
        return self.value == other.value and self.key == other.key and self.desc == other.desc and self.num == other.num and self.template_representation == other.template_representation and self.min_value == other.min_value and self.max_value == other.max_value

    def __hash__(self):
        """Hash based on the string representation of the NumToken."""
        return hash((self.value, self.key, self.desc, self.num, self.min_value, self.max_value, self.template_representation))
