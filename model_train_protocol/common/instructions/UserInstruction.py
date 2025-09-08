from typing import Sequence

from .Instruction import Instruction
from ..tokens.Token import Token
from ..tokens.TokenSet import TokenSet, Snippet


class UserInstruction(Instruction):
    """
    A UserInstruction is a specialized Instruction that includes at least one user token in the user token set.

    This Instruction type includes a prompt provided by the user to guide the model's response.

    Note: The response TokenSet is not set in a UserInstruction.
    The user TokenSet sets the context for the user's prompt. The model's response is not predefined in this scenario.
    """

    def __init__(self, context: Sequence[TokenSet], user: TokenSet, final: Token):
        """
        Initializes a UserInstruction instance.

        :param context: List of tuples containing Token instances that define the input structure. This precedes the user input.
        :param user: A TokenSet instance that must include at least one user token.
        :param final: A Token instance designating the final action by the model.
        """
        super().__init__(context=context, response=user, final=final)
        assert self.contains_user(), "UserInstruction requires a user token in the response. Use Instruction for non-user inputs."

    # noinspection PyMethodOverriding
    def add_sample(self, context_snippets: list[Snippet], prompt: str, output_snippet: Snippet,
                   value: int | float | None = None):
        """
        Add a sample to the Instruction.

        :param context_snippets: List of context snippets that will be added to the Instruction.
        :param prompt: The prompt provided by the user.
        :param output_snippet: The model's output snippet.
        :param value: Optional value ascribed to the final Instruction output IF the final Token output is a number.
        """
        self._assert_valid_value(value=value)

        all_snippets: list[Snippet] = context_snippets + [output_snippet]
        sample: dict = self._create_base_sample(snippets=all_snippets, value=value)
        sample['prompt'] = prompt
        self.samples.append(sample)
