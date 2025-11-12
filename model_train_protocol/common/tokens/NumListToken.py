from .Token import Token


class NumListToken(Token):
    def __init__(self, value: str, min_value: int | float, max_value: int | float, length: int,
                 key: str | None = None, desc: str | None = None, *args, **kwargs):
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
            raise ValueError("Length of NumListToken must be a positive non-zero integer.")

        self.num_list: int = length
        self.min_value = min_value
        self.max_value = max_value
        self.template_representation: str = f"<List of length {length} of numbers between {min_value} and {max_value}>"
