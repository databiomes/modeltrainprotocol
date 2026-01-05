from typing import List, Union

from . import ExtendedResponse
from .BaseInstruction import BaseInstruction, Sample
from .input.BaseInput import BaseInput
from ..guardrails import Guardrail
from ..tokens.FinalToken import FinalToken
from ..tokens.TokenSet import TokenSet, Snippet


class ExtendedInstruction(BaseInstruction):
    """
    A ExtendedInstruction is a specialized Instruction that allows you to extend the context with an additional tokenset

    This Instruction type includes a prompt provided by the user to guide the model's response.

    Note: The response TokenSet is not set in a ExtendedInstruction.
    The user TokenSet sets the context for the user's prompt. The model's response is not predefined in this scenario.
    """

    output: ExtendedResponse

    def __init__(self, input: BaseInput, output: ExtendedResponse, name: str = "extended_instruction"):
        """
        Initializes a ExtendedInstruction instance.

        :param input: BaseInput instance containing the input structure. This precedes the user input.
        :param name: Optional name for the Instruction. Defaults to 'extended_instruction'.
        """
        super().__init__(input=input, output=output, name=name)

        if not isinstance(output, ExtendedResponse):
            raise TypeError(f"response must be an instance of ExtendedResponse. Got: {type(output)}")

        self.validate_context_snippets()

    @property
    def has_guardrails(self) -> bool:
        """Indicates whether the Instruction has any guardrails defined."""
        return len(self.input.guardrails) > 0

    def get_token_sets(self) -> List[TokenSet]:
        """Returns all tokens in the instruction as a list of tuples."""
        all_tokens_sets: List = []
        for token_set in self.input.tokensets:
            all_tokens_sets.append(token_set)
        return all_tokens_sets

    @property
    def last_tokenset(self) -> TokenSet:
        """Returns the last TokenSet in the Instruction, which is the response TokenSet."""
        return self.input.tokensets[-1]

    def _validate_snippets_match(self, inputs: List[Snippet]):
        """Validates that all snippets in the samples match their expected token sets."""
        all_token_sets: List[TokenSet] = self.get_token_sets()

        for i in range(len(inputs)):
            self._validate_snippet_matches_set(snippet=inputs[i], expected_token_set=all_token_sets[i])

    # noinspection PyMethodOverriding
    def add_sample(self, inputs: List[Snippet], response_string: str,
                   value: Union[int, float, List[Union[int, float]], None]= None, final: FinalToken | None = None):
        f"""
        Add a sample to the Instruction.

        :param inputs: List of context snippets that will be added to the Instruction.
        :param response_string: The response provided by the model as a string.
        :param value: Optional value ascribed to the final Instruction output IF the final Token output is a number.
        :param final: Optional Token instance designating the final action by the model. Defaults to a non-action Token designated {self.output.default_final}.
        """
        final: FinalToken = self._assign_final_token(final=final)
        self.output.validate_sample(string=response_string, value=value, final=final)
        self._assert_context_snippet_count(inputs=inputs) # exclude last snippet for special case
        self._validate_snippets_match(inputs=inputs)

        sample: Sample = self._create_sample(inputs=inputs,
                                             response_string=response_string, value=value, final=final)
        self.samples.append(sample)

    def _create_sample(self, inputs: List[Snippet], response_string: str, final: FinalToken,
                       value: Union[int, float, List[Union[int, float]], None] = None) -> Sample:
        """Creates a sample ExtendedInstruction string for example usages."""

        # format sample
        numbers: List[List[int]] = []
        for snippet in inputs:
            numbers.append(snippet.numbers)

        number_lists: List[List[List[int]]] = []
        for snippet in inputs:
            number_lists.append(snippet.number_lists)

        return Sample(
            context=[snippet.string for snippet in inputs[:-1]],
            output=response_string,
            prompt=inputs[-1].string,
            number=numbers,
            number_lists=number_lists,
            result=final,
            value=value
        )

    def add_guardrail(self, guardrail: Guardrail, tokenset_index: int):
        """
        Adds a guardrail to the ExtendedInstruction.

        :param guardrail: The Guardrail instance to add.
        :param tokenset_index: The index of the TokenSet the guardrail applies to.
        """
        if len(guardrail.samples) < 3:
            raise ValueError(
                "Guardrail must have at least 3 samples of bad inputs before being added to an Instruction.")

        self.input.add_guardrail(guardrail=guardrail, tokenset_index=tokenset_index)

