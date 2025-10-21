from typing import Sequence

from .BaseInstruction import BaseInstruction, Sample
from ..constants import NON_TOKEN
from ..tokens.Token import Token
from ..tokens.TokenSet import TokenSet, Snippet


class ExtendedInstruction(BaseInstruction):
    """
    A ExtendedInstruction is a specialized Instruction that allows you to extend the context with an additional tokenset

    This Instruction type includes a prompt provided by the user to guide the model's response.

    Note: The response TokenSet is not set in a ExtendedInstruction.
    The user TokenSet sets the context for the user's prompt. The model's response is not predefined in this scenario.
    """

    def __init__(self, context: Sequence[TokenSet], final: Token=NON_TOKEN):
        """
        Initializes a ExtendedInstruction instance.

        :param context: List of tuples containing Token instances that define the input structure. This precedes the user input.
        :param final: A Token instance designating the final action by the model.
        """
        super().__init__(context=context[:-1], response=context[-1], final=final)

    # noinspection PyMethodOverriding
    def add_sample(self, context_snippets: list[Snippet], response: str,
                   value: int | float | list[int | float] | None = None):
        """
        Add a sample to the Instruction.

        :param context_snippets: List of context snippets that will be added to the Instruction.
        :param response: The prompt provided by the user.
        :param value: Optional value ascribed to the final Instruction output IF the final Token output is a number.
        """
        self._assert_valid_value(value=value)
        self._assert_context_snippet_count(context_snippets=context_snippets[:-1]) # exclude last snippet for special case
        self._validate_snippets_match(context_snippets=context_snippets[:-1], output_snippet=context_snippets[-1])

        sample: Sample = self._create_sample(context_snippets=context_snippets,
                                             response=response, value=value)
        self.samples.append(sample)

    # noinspection PyMethodOverriding
    def _create_sample(self, context_snippets: list[Snippet], response: str,
                       value: int | float | list[int | float] | None = None) -> Sample:
        """Creates a sample ExtendedInstruction string for example usages."""

        # format sample
        numbers: list[list[int]] = []
        for snippet in context_snippets:
            numbers.append(snippet.numbers)

        number_lists: list[list[list[int]]] = []
        for snippet in context_snippets:
            number_lists.append(snippet.number_lists)

        return Sample(
            context=[snippet.string for snippet in context_snippets[:-1]],
            response=context_snippets[-1].string,
            prompt=response,
            number=numbers,
            number_lists=number_lists,
            result=self.final,
            value=value
        )