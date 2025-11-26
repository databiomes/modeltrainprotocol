from typing import List, Sequence, Union

from .BaseInstruction import BaseInstruction, Sample
from ..tokens.FinalToken import FinalToken
from ..tokens.TokenSet import TokenSet, Snippet
from . import ExtendedResponse


class ExtendedInstruction(BaseInstruction):
    """
    A ExtendedInstruction is a specialized Instruction that allows you to extend the context with an additional tokenset

    This Instruction type includes a prompt provided by the user to guide the model's response.

    Note: The response TokenSet is not set in a ExtendedInstruction.
    The user TokenSet sets the context for the user's prompt. The model's response is not predefined in this scenario.
    """
    response: ExtendedResponse

    def __init__(self, context: Sequence[TokenSet], response: ExtendedResponse, name: str = "extended_instruction"):
        """
        Initializes a ExtendedInstruction instance.

        :param context: List of tuples containing Token instances that define the input structure. This precedes the user input.
        :param name: Optional name for the Instruction. Defaults to 'extended_instruction'.
        """
        super().__init__(context=context, response=response, name=name)

        if not isinstance(response, ExtendedResponse):
            raise TypeError(f"response must be an instance of ExtendedResponse. Got: {type(response)}")

    def get_token_sets(self) -> List[TokenSet]:
        """Returns all tokens in the instruction as a list of tuples."""
        all_tokens_sets: List = []
        for token_set in self.context:
            all_tokens_sets.append(token_set)
        return all_tokens_sets

    def _validate_snippets_match(self, context_snippets: List[Snippet]):
        """Validates that all snippets in the samples match their expected token sets."""
        all_token_sets: List[TokenSet] = self.get_token_sets()

        for i in range(len(context_snippets)):
            self._validate_snippet_matches_set(snippet=context_snippets[i], expected_token_set=all_token_sets[i])

    # noinspection PyMethodOverriding
    def add_sample(self, context_snippets: List[Snippet], response_string: str,
                   value: Union[int, float, List[Union[int, float]], None]= None, final: FinalToken | None = None):
        f"""
        Add a sample to the Instruction.

        :param context_snippets: List of context snippets that will be added to the Instruction.
        :param response_string: The response provided by the model as a string.
        :param value: Optional value ascribed to the final Instruction output IF the final Token output is a number.
        :param final: Optional Token instance designating the final action by the model. Defaults to a non-action Token designated {self.response.default_final}.
        """
        final: FinalToken = self._assign_final_token(final=final)
        self.response.validate_sample(string=response_string, value=value, final=final)
        self._assert_context_snippet_count(context_snippets=context_snippets) # exclude last snippet for special case
        self._validate_snippets_match(context_snippets=context_snippets)

        sample: Sample = self._create_sample(context_snippets=context_snippets,
                                             response_string=response_string, value=value, final=final)
        self.samples.append(sample)

    def _create_sample(self, context_snippets: List[Snippet], response_string: str, final: FinalToken,
                       value: Union[int, float, List[Union[int, float]], None] = None) -> Sample:
        """Creates a sample ExtendedInstruction string for example usages."""

        # format sample
        numbers: List[List[int]] = []
        for snippet in context_snippets:
            numbers.append(snippet.numbers)

        number_lists: List[List[List[int]]] = []
        for snippet in context_snippets:
            number_lists.append(snippet.number_lists)

        return Sample(
            context=[snippet.string for snippet in context_snippets[:-1]],
            response=response_string,
            prompt=context_snippets[-1].string,
            number=numbers,
            number_lists=number_lists,
            result=final,
            value=value
        )

