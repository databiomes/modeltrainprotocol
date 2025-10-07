from typing import Sequence

from .BaseInstruction import BaseInstruction, Sample
from ..constants import NON_TOKEN
from ..tokens.Token import Token
from ..tokens.TokenSet import TokenSet, Snippet


class UnsetInstruction(BaseInstruction):
    """
    A UnsetInstruction is a specialized Instruction that includes at least one user token in the user token set.

    This Instruction type includes a prompt provided by the user to guide the model's response.

    Note: The response TokenSet is not set in a UnsetInstruction.
    The user TokenSet sets the context for the user's prompt. The model's response is not predefined in this scenario.
    """

    def __init__(self, context: Sequence[TokenSet], user: TokenSet, final: Token=NON_TOKEN):
        """
        Initializes a UnsetInstruction instance.

        :param context: List of tuples containing Token instances that define the input structure. This precedes the user input.
        :param user: A TokenSet instance that must include at least one user token.
        :param final: A Token instance designating the final action by the model.
        """
        super().__init__(context=context, response=user, final=final)
        if not self.contains_user():
            raise ValueError("UnsetInstruction requires a user token in the response. Use Instruction for non-user inputs.")

    # noinspection PyMethodOverriding
    def add_sample(self, context_snippets: list[Snippet], prompt: str, output_snippet: Snippet,
                   value: int | float | list[int | float] | None = None):
        """
        Add a sample to the Instruction.

        :param context_snippets: List of context snippets that will be added to the Instruction.
        :param prompt: The prompt provided by the user.
        :param output_snippet: The model's output snippet.
        :param value: Optional value ascribed to the final Instruction output IF the final Token output is a number.
        """
        self._assert_valid_value(value=value)
        self._assert_context_snippet_count(context_snippets=context_snippets)
        self._validate_snippets_match(context_snippets=context_snippets, output_snippet=output_snippet)

        sample: Sample = self._create_sample(context_snippets=context_snippets, output_snippet=output_snippet,
                                             prompt=prompt, value=value)
        self.samples.append(sample)

    # noinspection PyMethodOverriding
    def _create_sample(self, context_snippets: list[Snippet], output_snippet: Snippet, prompt: str,
                                value: int | float | list[int | float] | None = None) -> Sample:
        """Creates a sample UnsetInstruction string for example usages."""
        all_snippets: list[Snippet] = context_snippets + [output_snippet]

        # format sample
        numbers: list[list[int]] = []
        for snippet in all_snippets:
            numbers.append(snippet.numbers)

        return Sample(
            context=[snippet.string for snippet in context_snippets],
            response=output_snippet.string,
            prompt=prompt,
            number=numbers,
            result=self.final,
            value=value
        )