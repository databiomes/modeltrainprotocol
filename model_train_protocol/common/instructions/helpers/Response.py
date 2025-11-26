from typing import List, Union

from ...constants import NON_TOKEN
from ...tokens.FinalNumToken import FinalNumToken
from ...tokens.FinalToken import FinalToken
from ...tokens.TokenSet import TokenSet, Snippet
from .BaseResponse import BaseResponse


class Response(BaseResponse):
    """Defines the output of Instructions."""

    default_final: FinalToken = NON_TOKEN

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
            raise TypeError(f"tokenset must be an instance of TokenSet. Got: {type(tokenset)}")

        if tokenset.has_num_list_tokens or tokenset.has_num_tokens:
            raise ValueError(
                "Response TokenSet cannot contain NumTokens or NumListTokens. To achieve a single numeric output alongside text, use a FinalNumToken as the Response final token.")

    def validate_sample(self, snippet: Snippet, value: Union[int, float, None],
                        final: FinalToken | None):
        """
        Validates the snippet against the response definition.

        :param snippet: The snippet to validate.
        :param value: The value of the Snippet to validate if Snippet has a NumToken.
        :param final: The FinalToken to validate.
        """
        if not isinstance(snippet, Snippet):
            raise TypeError(f"Snippet must be an instance of Snippet. Got: {type(snippet)}")

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
