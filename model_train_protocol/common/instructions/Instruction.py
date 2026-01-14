from typing import List, Union

from .BaseInstruction import BaseInstruction, Sample
from .input.InstructionInput import InstructionInput
from .output.InstructionOutput import InstructionOutput
from ..guardrails import Guardrail
from ..tokens.FinalToken import FinalToken
from ..tokens.TokenSet import TokenSet, Snippet


class Instruction(BaseInstruction):
    """
    Instructions are provided to the model to guide its behavior.

    It includes context Tokens that define the input structure and a response TokenSet that defines the expected output.

    Samples must be added to the Instruction to provide context for the model.
    A minimum of 3 samples must be added to an Instruction.
    """
    output: InstructionOutput
    input: InstructionInput

    def __init__(self, input: InstructionInput, output: InstructionOutput, context: List[str] | None = None, name: str | None = None):
        f"""
        Initializes an Instruction instance.

        :param input: List of tuples containing Token instances that define the input structure. This precedes the model's response.
        :param output: A TokenSet instance that does not include any user tokens.
        :param context: A list of strings providing background context for the instruction.
        :param name: Optional name for the Instruction. Defaults to 'instruction'.
        """
        super().__init__(input=input, output=output, context=context, name=name)
        if not isinstance(self.output, InstructionOutput):
            raise TypeError(f"Response must be an instance of Response. Got: {type(self.output)}")
        self._validate_input_snippets()

    def _validate_snippets_match(self, inputs: List[Snippet], response_snippet: Snippet):
        """Validates that all snippets in the samples match their expected token sets."""
        all_snippets: List[Snippet] = inputs + [response_snippet]
        all_token_sets: List[TokenSet] = self.get_token_sets()

        for i in range(len(all_snippets)):
            self._validate_snippet_matches_set(snippet=all_snippets[i], expected_token_set=all_token_sets[i])

        if not isinstance(self.output, InstructionOutput):
            raise TypeError(f"Response must be an instance of Response. Got: {type(self.output)}")

        # Validate output snippet set matches output token set
        self._validate_snippet_matches_set(snippet=response_snippet, expected_token_set=self.output.tokenset)

    def get_token_sets(self) -> List[TokenSet]:
        """Returns all tokens in the instruction as a list of tuples."""
        all_tokens_sets: List = []
        for token_set in self.input.tokensets:
            all_tokens_sets.append(token_set)
        all_tokens_sets.append(self.output.tokenset)
        return all_tokens_sets

    @property
    def last_tokenset(self) -> TokenSet:
        """Returns the last TokenSet in the Instruction, which is the response TokenSet."""
        return self.output.tokenset

    @property
    def has_guardrails(self) -> bool:
        """Indicates whether the Instruction has any guardrails defined."""
        return len(self.input.guardrails) > 0

    def _enforce_response_snippet(self, snippet: Union[Snippet, str]) -> Snippet:
        """Converts a regular string to a snippet if provided as a string."""
        if isinstance(snippet, str):
            associated_tokenset: TokenSet = self.output.tokenset
            try:
                snippet = associated_tokenset.create_snippet(string=snippet)
            except Exception as e:
                raise ValueError(
                    f"Failed to create Snippet from string '{snippet}' for TokenSet {associated_tokenset}.\n"
                    f"Create a Snippet from the tokenset and add associated information: {e}")
        return snippet

    # noinspection PyMethodOverriding
    def add_sample(self, input_snippets: List[Union[str | Snippet]], output_snippet: Snippet | str,
                   output_value: Union[int, float, List[Union[int, float]], None] = None, final: FinalToken | None = None):
        f"""
        Add a sample to the Instruction.

        :param input_snippets: List of context snippets or strings that will be added to the Instruction.
        :param output_snippet: The model's response snippet.
        :param output_value: Optional value ascribed to the final Instruction output IF the final Token output is a number.
        :param final: Optional Token instance designating th e final action by the model. Defaults to a non-action Token designated {self.output.default_final}.
        """
        input_snippets: List[Snippet] = self._enforce_snippets(inputs=input_snippets)
        output_snippet: Snippet = self._enforce_response_snippet(output_snippet)
        final: FinalToken = self._assign_final_token(final=final)
        self.output.validate_sample(snippet=output_snippet, value=output_value, final=final)
        self._assert_input_snippet_count(inputs=input_snippets)
        self._validate_snippets_match(inputs=input_snippets, response_snippet=output_snippet)

        sample: Sample = self._create_sample(inputs=input_snippets, response_snippet=output_snippet,
                                             value=output_value, final=final)
        self.samples.append(sample)

    def add_guardrail(self, guardrail: Guardrail, tokenset_index: int):
        """
        Adds a guardrail to the Instruction.

        :param guardrail: The Guardrail instance to add.
        :param tokenset_index: The index of the TokenSet the guardrail applies to.
        """
        if len(guardrail.samples) < 3:
            raise ValueError(
                "Guardrail must have at least 3 samples of bad inputs before being added to an Instruction.")

        self.input.add_guardrail(guardrail=guardrail, tokenset_index=tokenset_index)
