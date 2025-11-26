from typing import List, Union

from model_train_protocol import Snippet
from ...constants import NON_TOKEN
from ...tokens.FinalNumToken import FinalNumToken
from ...tokens.FinalToken import FinalToken
from .BaseResponse import BaseResponse

class ExtendedResponse(BaseResponse):
    """Defines the output of Instructions."""

    default_final: FinalToken = NON_TOKEN

    def __init__(self, final: FinalToken | List[FinalToken] | None = None):
        """
        Initializes a Response instance.

        :param final: A FinalToken or list of FinalToken designating the allowed final action by the model.
        """
        self.final: FinalToken | List[FinalToken] | None = final

    # noinspection PyMethodOverriding
    def validate_sample(self, string: str, value: Union[int, float, None],
                        final: FinalToken | None):
        """
        Validates the snippet against the response definition.

        :param value: The value of the Snippet to validate if Snippet has a NumToken.
        :param final: The FinalToken to validate.
        """
        if not isinstance(string, str):
            raise TypeError(f"String must be an instance of str. Got: {type(string)}")

        if not final in self.final:
            raise ValueError(
                f"FinalToken {final} is not added to the Response final tokens. Allowed finals: {self.final}")

        if not isinstance(final, FinalToken):
            raise TypeError(f"Final must be an instance of FinalToken. Got: {type(final)}")

        if isinstance(final, FinalNumToken):
            if value is None:
                raise ValueError(f"FinalToken {final} requires a numeric value, but none was provided.")

            if not isinstance(value, Union[int, float]):
                raise TypeError(f"Value must be an int or float. Got: {type(value)}")