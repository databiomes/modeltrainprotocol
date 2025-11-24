from typing import List

from ...constants import NON_TOKEN
from ...tokens.FinalToken import FinalToken
from ...tokens.TokenSet import TokenSet

class Response:
    """Defines the output of Instructions."""

    default_final: FinalToken = NON_TOKEN

    def __init__(self, tokenset: TokenSet, final: FinalToken | List[FinalToken] | None = None):
        """
        Initializes a Response instance.

        :param tokenset: The TokenSet associated with the model's response. Not used in
        :param final: A FinalToken or list of FinalToken designating the allowed final action by the model.
        """
        self.tokenset: TokenSet = tokenset
        self.final: FinalToken | List[FinalToken] | None = final