from typing import List, Sequence, Union

from .BaseInstruction import BaseInstruction, Sample
from .helpers.Response import Response
from ..tokens.FinalToken import FinalToken
from ..tokens.TokenSet import TokenSet, Snippet


class Instruction(BaseInstruction):
    """
    Instructions are provided to the model to guide its behavior.

    It includes context Tokens that define the input structure and a response TokenSet that defines the expected output.

    Samples must be added to the Instruction to provide context for the model.
    A minimum of 3 samples must be added to an Instruction.
    """
    response: Response

    def __init__(self, context: Sequence[TokenSet], response: Response, name: str = "instruction"):
        f"""
        Initializes an Instruction instance.

        :param context: List of tuples containing Token instances that define the input structure. This precedes the model's response.
        :param response: A TokenSet instance that does not include any user tokens.
        :param name: Optional name for the Instruction. Defaults to 'instruction'.
        """
        super().__init__(context=context, response=response, name=name)
        if not isinstance(self.response, Response):
            raise TypeError(f"Response must be an instance of Response. Got: {type(self.response)}")
        self.validate_context_snippets()

    def _validate_snippets_match(self, context_snippets: List[Snippet], response_snippet: Snippet):
        """Validates that all snippets in the samples match their expected token sets."""
        all_snippets: List[Snippet] = context_snippets + [response_snippet]
        all_token_sets: List[TokenSet] = self.get_token_sets()

        for i in range(len(all_snippets)):
            self._validate_snippet_matches_set(snippet=all_snippets[i], expected_token_set=all_token_sets[i])

        if not isinstance(self.response, Response):
            raise TypeError(f"Response must be an instance of Response. Got: {type(self.response)}")

        # Validate output snippet set matches output token set
        self._validate_snippet_matches_set(snippet=response_snippet, expected_token_set=self.response.tokenset)

    def get_token_sets(self) -> List[TokenSet]:
        """Returns all tokens in the instruction as a list of tuples."""
        all_tokens_sets: List = []
        for token_set in self.context:
            all_tokens_sets.append(token_set)
        all_tokens_sets.append(self.response.tokenset)
        return all_tokens_sets

    @property
    def last_tokenset(self) -> TokenSet:
        """Returns the last TokenSet in the Instruction, which is the response TokenSet."""
        return self.response.tokenset

    # noinspection PyMethodOverriding
    def add_sample(self, context_snippets: List[Snippet], response_snippet: Snippet,
                   value: Union[int, float, List[Union[int, float]], None] = None, final: FinalToken | None = None):
        f"""
        Add a sample to the Instruction.

        :param context_snippets: List of context snippets that will be added to the Instruction.
        :param response_snippet: The model's response snippet.
        :param value: Optional value ascribed to the final Instruction output IF the final Token output is a number.
        :param final: Optional Token instance designating th e final action by the model. Defaults to a non-action Token designated {self.response.default_final}.
        """
        final: FinalToken = self._assign_final_token(final=final)
        self.response.validate_sample(snippet=response_snippet, value=value, final=final)
        self._assert_context_snippet_count(context_snippets=context_snippets)
        self._validate_snippets_match(context_snippets=context_snippets, response_snippet=response_snippet)

        sample: Sample = self._create_sample(context_snippets=context_snippets, response_snippet=response_snippet,
                                             value=value, final=final)
        self.samples.append(sample)
