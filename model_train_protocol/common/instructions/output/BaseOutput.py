import abc
from abc import ABC
from typing import Union, List

from ...constants import NON_TOKEN
from ...tokens.FinalToken import FinalToken
from ...tokens.TokenSet import Snippet, TokenSet
from model_train_protocol.errors import OutputError, OutputTypeError


class BaseOutput(ABC):
    """Defines the output of Instructions."""

    default_final: FinalToken = NON_TOKEN
    final: List[FinalToken]

    def __init__(self, tokenset: TokenSet, final: FinalToken | List[FinalToken] | None = None):
        """
        Initializes a Response instance.

        :param tokenset: The TokenSet associated with the model's response. Not used in
        :param final: A FinalToken or list of FinalToken designating the allowed final action by the model.
        """
        self.tokenset: TokenSet = tokenset
        self.validate_tokenset(tokenset=tokenset)
        if isinstance(final, FinalToken):
            final = [final]
        self.final: List[FinalToken] | None = final

    @classmethod
    def validate_tokenset(cls, tokenset: TokenSet):
        """
        Validates the TokenSet associated with the response.

        :param tokenset: The TokenSet to validate.
        """
        if not isinstance(tokenset, TokenSet):
            raise OutputTypeError(f"tokenset must be an instance of TokenSet. Got: {type(tokenset)}")

        if tokenset.has_num_list_tokens or tokenset.has_num_tokens:
            raise OutputError(
                "Response TokenSet cannot contain NumTokens or NumListTokens. To achieve a single numeric output alongside text, use a FinalNumToken as the Response final token.")


    @abc.abstractmethod
    def validate_sample(self, snippet: Snippet, value: Union[int, float, None], final: Union[FinalToken, None]):
        """
        Validates the snippet against the response definition.

        :param snippet: The snippet to validate.
        :param value: The value of the Snippet to validate if Snippet has a NumToken.
        :param final: The FinalToken to validate.
        """
        raise NotImplementedError("Subclasses must implement validate_snippet method.")

    def __str__(self):
        """Combines the output's TokenSet and final Tokens into a string representation."""
        return f"Output(TokenSet={self.tokenset}, FinalTokens=[{self.final}])"
