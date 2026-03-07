from model_train_protocol.errors import OutputTypeError
from .BaseOutput import BaseOutput
from ...constants import NON_TOKEN
from ...tokens.TokenSet import TokenSet, Snippet


class StateMachineOutput(BaseOutput):
    """Defines the output of StateMachineInstructions."""

    def __init__(self, tokenset: TokenSet):
        """
        Initializes a StateMachineOutput instance.

        :param tokenset: The TokenSet associated with the model's response.
        """
        super().__init__(tokenset=tokenset, final=NON_TOKEN)

    # noinspection PyMethodOverriding
    def validate_sample(self, snippet: Snippet):
        """
        Validates the snippet against the response definition.

        :param snippet: The snippet to validate.
        """
        if not isinstance(snippet, Snippet):
            raise OutputTypeError(f"Snippet must be an instance of Snippet. Got: {type(snippet)}")
