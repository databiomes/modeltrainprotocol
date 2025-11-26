import abc
from abc import ABC
from typing import List, Optional, Sequence, Union

from .helpers.BaseResponse import BaseResponse
from ..tokens.FinalToken import FinalToken
from ..tokens.Token import Token
from ..tokens.TokenSet import TokenSet, Snippet


class Sample:
    """A Sample is a single example of input and output for an Instruction."""

    def __init__(self, context: List[str], response: str, prompt: Optional[str], number: List[List[int]],
                 number_lists: List[List[List[int]]],
                 result: Token,
                 value: Union[int, float, None]):
        self.context: List[str] = context
        self.response: str = response
        self.prompt: Optional[str] = prompt
        self.numbers: List[List[int]] = number
        self.number_lists: List[List[List[int]]] = number_lists
        self.result: Token = result
        self.value: Union[int, float, None] = value

    @property
    def strings(self) -> List[str]:
        """Returns all strings in the sample as a list."""
        return self.context + [self.response]

    def to_dict(self) -> dict:
        return {
            'strings': self.strings,
            'prompt': self.prompt,
            'numbers': self.numbers,
            'number_lists': self.number_lists,
            'result': self.result.value,  # We only need the value of the result token
            'value': self.value
        }

    def __repr__(self):
        """String representation of the Sample."""
        result_str = self.result.value
        if self.value is not None:
            result_str += f"{self.value}"
        return f"Sample(Context: {self.context}, Response: {self.response}, Result: {result_str})"


class BaseInstruction(ABC):
    """
    An Instruction is a set of tokens that show possible input combinations for a model.

    Samples must be added to the Instruction to provide context for the model.
    A minimum of 3 samples must be added to an Instruction.

    Example:
        context = TokenSet(
        context = [
                 [ Token("SentenceLength", num=True), Token("Greeting") ],
                 [ Token("CurtResponse") ],
                 [ Token("SentenceLength", num=True), Token("Goodbye") ],
                 ]
        response = TokenSet( Token("SentenceLength", num=True), Token("PoliteResponse") )
        final = Token("End")
        instruction = Instruction(context=context, response=response, final=final, name="example_instruction")
    """

    def __init__(self, context: Sequence[TokenSet], response: BaseResponse, name: str):
        """Initializes the common attributes to all Instructions."""
        self.context: Sequence[TokenSet] = context
        self.response: BaseResponse = response
        self.samples: List[Sample] = []
        self.name: str = name
        self.samples: list[Sample] = []
        if not isinstance(context, Sequence):
            raise TypeError("Context must be a sequence of TokenSet instances.")
        if not all(isinstance(ts, TokenSet) for ts in context):
            raise TypeError("All items in context must be instances of TokenSet.")
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string.")

    @abc.abstractmethod
    def add_sample(self):
        """Add a sample to the Instruction."""
        raise NotImplementedError("Subclasses must implement add_sample method.")

    @abc.abstractmethod
    def get_token_sets(self) -> List[TokenSet]:
        """Returns all tokens in the instruction as a list of tuples."""
        raise NotImplementedError("Subclasses must implement get_token_sets method.")

    def get_tokens(self) -> List[Token]:
        """Returns all tokens in the instruction as a flat list."""
        all_tokens: List[Token] = []
        for token_set in self.get_token_sets():
            all_tokens.extend(token_set.tokens)
        for sample in self.samples:
            all_tokens.append(sample.result)
        return all_tokens

    def serialize_samples(self) -> List[dict]:
        """Serializes the Instruction samples"""
        serialized_samples: List[dict] = []
        for sample in self.samples:
            serialized_samples.append(sample.to_dict())

        return serialized_samples

    def serialize_ppo(self) -> List[dict]:
        """Serialize the Instruction for PPO training."""
        # To be implemented when ppo introduced
        # ppo = []
        # ppo_strings = [sample['strings'] for sample in self.ppo]
        # ppo_prompts = [sample['prompt'] for sample in self.ppo]
        # ppo_numbers = [sample['number'] for sample in self.ppo]
        # ppo_results = [sample['result'].value for sample in self.ppo]
        # ppo_values = [sample['value'] for sample in self.ppo]
        # ppo_a_samples = [sample['a_sample'] for sample in self.ppo]
        # ppo_b_samples = [sample['b_sample'] for sample in self.ppo]
        # ppo_pref = [sample['pref'] for sample in self.ppo]
        # for s, p, n, r, v, a, b, pr in zip(ppo_strings, ppo_prompts, ppo_numbers, ppo_results, ppo_values,
        #                                    ppo_a_samples, ppo_b_samples, ppo_pref):
        #     ppo.append({'sample': s, 'prompt': p, 'number': n, 'result': r, 'value': v, 'a': a, 'b': b, 'pref': pr})
        # TODO: implement PPO training
        return []

    def serialize_memory_set(self) -> List[List[str]]:
        """Serialize the Instruction token memory set training."""
        memory_set = []
        for token_set in self.get_token_sets():
            token_strings = [t.value for t in token_set.tokens]
            memory_set.append(token_strings)
        return memory_set

    def _create_sample(self, context_snippets: List[Snippet], response_snippet: Snippet, final: FinalToken,
                       value: Union[int, float, List[Union[int, float]], None] = None) -> Sample:
        """Create a base sample dictionary without a prompt."""
        all_snippets: List[Snippet] = context_snippets + [response_snippet]

        # format sample
        numbers: List[List[int]] = []
        for snippet in all_snippets:
            numbers.append(snippet.numbers)

        number_lists: List[List[List[int]]] = []
        for snippet in all_snippets:
            number_lists.append(snippet.number_lists)

        return Sample(
            context=[snippet.string for snippet in context_snippets],
            response=response_snippet.string,
            prompt=None,
            number=numbers,
            number_lists=number_lists,
            result=final,
            value=value
        )

    @classmethod
    def _validate_snippet_matches_set(cls, snippet: Snippet, expected_token_set: TokenSet):
        """Validates that the snippet matches the expected token set."""
        if snippet.token_set_key != expected_token_set.key:
            raise ValueError(f"Snippet {snippet} does not match expected token set {expected_token_set}.")

    def _assert_context_snippet_count(self, context_snippets: List[Snippet]):
        """Assert the number of context snippets matches the number of context token sets."""
        if len(context_snippets) != len(self.context):
            raise ValueError(
                f"Number of context snippets ({len(context_snippets)}) must match number of context token sets ({len(self.context)}).")

    def _assign_final_token(self, final: Optional[FinalToken]) -> FinalToken:
        """
        Validate the final token if provided.

        The following behaviour is observed:

        If a final token is provided directly, always use it.

        If no final token is provided in the sample, and no final token is defined in the response, use the default <NON> final token.

        If no final token is provided in the sample, and only one final token is defined in the response, use that final token.

        If no final token is provided in the sample, and multiple final tokens are defined in the response, raise an error requiring clarification.
        """
        if final is not None and not isinstance(final, FinalToken):
            raise TypeError("Final must be a FinalToken instance or None.")

        if final is not None:  # Use the specified final token if provided
            return final

        if len(self.response.final) == 0:  # Return default final if no finals are defined
            return self.response.default_final

        if len(self.response.final) == 1:  # If we only have one final token, use it
            return self.response.final[0]

        raise ValueError(
            "Multiple final tokens are allowed in the Response. Specify which final token to use for this sample.")

    def __str__(self) -> str:
        """String representation of the Instruction."""
        tokens_str: str = ', '.join(
            [''.join([token.key for token in token_set.tokens]) for token_set in self.get_token_sets()])
        samples_str: str = ',\n'.join([str(sample) for sample in self.samples])
        return f"Token Set(Tokens: {tokens_str}, Result: {self.response.default_final.key}, Samples:\n{samples_str})"

    def __hash__(self) -> int:
        """Hash based on the token sets of the Instruction. Instructions with the same TokenSets in the same order
        will have the same hash."""
        return hash(str(self.get_token_sets()))

    def __eq__(self, other) -> bool:
        """
        Defines equality based on the attributes of the Instruction.
        Returns True if the other object is an Instruction and its attributes match this Instruction's attributes.
        Includes the 'name' field in comparison.
        """
        if not isinstance(other, BaseInstruction):
            return False

        attrs_to_compare = ['name', 'context', 'response', 'final', 'samples']
        for attr in attrs_to_compare:
            try:
                self_val = getattr(self, attr, None)
                other_val = getattr(other, attr, None)
                if self_val != other_val:
                    return False
            except AttributeError:
                return False

        return True

    def __dict__(self) -> dict:
        """Dictionary representation of the Instruction."""
        return self.to_dict()

    def to_dict(self) -> dict:
        """Convert the Instruction to a dictionary representation."""
        return {
            'name': self.name,
            'tokens': [[token.to_dict() for token in token_set.tokens] for token_set in self.get_token_sets()],
            'result': self.response.default_final.to_dict() if self.response.default_final else None,
            'samples': self.samples
        }
