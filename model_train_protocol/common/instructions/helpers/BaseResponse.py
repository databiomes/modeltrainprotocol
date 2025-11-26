import abc
from abc import ABC
from typing import List, Union

from ...constants import NON_TOKEN
from ...tokens.FinalToken import FinalToken
from ...tokens.TokenSet import TokenSet, Snippet


class BaseResponse(ABC):
    """Defines the output of Instructions."""

    default_final: FinalToken = NON_TOKEN

    @abc.abstractmethod
    def validate_sample(self, snippet: Snippet, value: Union[int, float, None], final: Union[FinalToken, None]):
        """
        Validates the snippet against the response definition.

        :param snippet: The snippet to validate.
        :param value: The value of the Snippet to validate if Snippet has a NumToken.
        :param final: The FinalToken to validate.
        """
        raise NotImplementedError("Subclasses must implement validate_snippet method.")
