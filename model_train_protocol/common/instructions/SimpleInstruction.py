from typing import Sequence

from .Instruction import Instruction
from .. import NON_TOKEN
from ..tokens.Token import Token
from ..tokens.TokenSet import TokenSet, Snippet


class SimpleInstruction(Instruction):
    """
    A SimpleInstruction is an instruction without a user prompt.

    Samples must be added to the Instruction to provide context for the model.
    A minimum of 3 samples must be added to an Instruction.
    """

    def __init__(self, context: Sequence[TokenSet], response: TokenSet, final: Token=NON_TOKEN):
        """
        Initializes an Instruction instance.

        :param context: List of tuples containing Token instances that define the input structure. This precedes the model's response.
        :param response: A TokenSet instance that does not include any user tokens.
        :param final: Optional Token instance designating the final action by the model. Defaults to a non-action SpecialToken.
        """
        super().__init__(context=context, response=response, final=final)
        if not self.contains_user():
            raise ValueError("SimpleInstruction requires that the response does not contain a user token. Use UserInstruction for user inputs.")

    # noinspection PyMethodOverriding
    def add_sample(self, context_snippets: list[Snippet], output_snippet: Snippet,
                   value: int | float | None = None):
        """
        Add a sample to the Instruction.

        :param context_snippets: List of context snippets that will be added to the Instruction.
        :param output_snippet: The model's output snippet.
        :param value: Optional value ascribed to the final Instruction output IF the final Token output is a number.
        """
        self._assert_valid_value(value=value)
        self._assert_context_snippet_count(context_snippets=context_snippets)
        self._validate_snippets_match(context_snippets=context_snippets, output_snippet=output_snippet)

        all_snippets: list[Snippet] = context_snippets + [output_snippet]
        sample: dict = self._create_base_sample(snippets=all_snippets, value=value)
        self.samples.append(sample)