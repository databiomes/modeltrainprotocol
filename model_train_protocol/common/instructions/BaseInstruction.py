import abc
from abc import ABC
from typing import Sequence, Union

from ..tokens.Token import Token
from ..tokens.TokenSet import TokenSet, Snippet
from ... import NumToken, NumListToken


class Sample:
    """A Sample is a single example of input and output for an Instruction."""

    def __init__(self, context: list[str], response: str, prompt: str | None, number: list[list[int]], result: Token,
                 value: int | float | None):
        self.context: list[str] = context
        self.response: str = response
        self.prompt: str | None = prompt
        self.number: list[list[int]] = number
        self.result: Token = result
        self.value: int | float | None = value

    @property
    def strings(self) -> list[str]:
        """Returns all strings in the sample as a list."""
        return self.context + [self.response]

    def to_dict(self) -> dict:
        return {
            'strings': self.strings,
            'prompt': self.prompt,
            'number': self.number,
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
    A BaseInstruction is a set of tokens that show possible input combinations for a model.

    Samples must be added to the BaseInstruction to provide context for the model.
    A minimum of 3 samples must be added to an BaseInstruction.

    Example:
        context = TokenSet(
        context = [
                 [ TokenSet([Token("SentenceLength", num=True), Token("Greeting")]) ],
                 [ TokenSet([Token("CurtResponse")]) ],
                 [ TokenSet([Token("SentenceLength", num=True), Token("Goodbye")]) ],
                 ]
        response = TokenSet( Token("SentenceLength", num=True), Token("PoliteResponse") )
        final = Token("End")
        instruction = BaseInstruction(context=context, response=response, final=final)
    """

    def __init__(self, context: Sequence[TokenSet], response: TokenSet, final: Token):
        """Initializes the common attributes to all BaseInstructions."""
        self.context: Sequence[TokenSet] = context
        self.response: TokenSet = response
        self.final: Token = final
        self.samples: list[Sample] = []
        if not isinstance(context, Sequence):
            raise TypeError("Context must be a sequence of TokenSet instances.")
        if not all(isinstance(ts, TokenSet) for ts in context):
            raise TypeError("All items in context must be instances of TokenSet.")
        if not isinstance(response, TokenSet):
            raise TypeError("Response must be an instance of TokenSet.")
        if not isinstance(final, Token):
            raise TypeError("Final must be an instance of Token.")

    @abc.abstractmethod
    def add_sample(self):
        """Add a sample to the Instruction."""
        raise NotImplementedError("Subclasses must implement add_sample method.")

    def get_token_sets(self) -> list[TokenSet]:
        """Returns all tokens in the instruction as a list of tuples."""
        all_tokens_sets: list = []
        for token_set in self.context:
            all_tokens_sets.append(token_set)
        all_tokens_sets.append(self.response)
        return all_tokens_sets

    def get_tokens(self) -> list[Token]:
        """Returns all tokens in the instruction as a flat list."""
        all_tokens: list[Token] = []
        for token_set in self.get_token_sets():
            all_tokens.extend(token_set.tokens)
        all_tokens.append(self.final)
        return all_tokens

    def contains_user(self) -> bool:
        """
        Returns True if the response contains a user token, else False
        """
        return self.response.is_user

    def serialize_samples(self) -> list[dict]:
        """Serializes the Instruction samples"""
        serialized_samples: list[dict] = []
        for sample in self.samples:
            serialized_samples.append(sample.to_dict())

        return serialized_samples

    def serialize_ppo(self) -> list[dict]:
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

    def serialize_memory_set(self) -> list[list[str]]:
        """Serialize the Instruction token memory set training."""
        memory_set = []
        for token_set in self.get_token_sets():
            token_strings = [t.value for t in token_set.tokens]
            memory_set.append(token_strings)
        return memory_set

    def _create_sample(self, context_snippets: list[Snippet], output_snippet: Snippet,
                       value: int | float | list[int | float] | None = None) -> Sample:
        """Create a base sample dictionary without a prompt."""
        all_snippets: list[Snippet] = context_snippets + [output_snippet]

        # format sample
        numbers: list[list[int]] = []
        for snippet in all_snippets:
            numbers.append(snippet.numbers)

        return Sample(
            context=[snippet.string for snippet in context_snippets],
            response=output_snippet.string,
            prompt=None,
            number=numbers,
            result=self.final,
            value=value
        )

    def _assert_valid_value(self, value: int | float | list | None):
        """
        Assert value is provided if self.final is a number Token, else assert value is None
        :param value: Optional value ascribed to the final Instruction output IF the final Token output is a number
        """
        if isinstance(self.final, NumToken) and not isinstance(value, Union[int, float]):
            raise ValueError("Value must be provided as an int or float when final token is a NumToken.")
        elif isinstance(self.final, NumListToken) and not isinstance(value, list):
            raise ValueError("Value must be provided as a list of int or float when final token is a NumListToken.")
        elif not isinstance(self.final, (NumToken, NumListToken)) and value is not None:
            raise ValueError("Value must be None when final token is not a NumToken or NumListToken.")

    def _validate_snippets_match(self, context_snippets: list[Snippet], output_snippet: Snippet):
        """Validates that all snippets in the samples match their expected token sets."""
        all_snippets: list[Snippet] = context_snippets + [output_snippet]
        all_token_sets: list[TokenSet] = self.get_token_sets()

        for i in range(len(all_snippets)):
            self._validate_snippet_matches_set(snippet=all_snippets[i], expected_token_set=all_token_sets[i])

        # Validate output snippet set matches output token set
        self._validate_snippet_matches_set(snippet=output_snippet, expected_token_set=self.response)

    @classmethod
    def _validate_snippet_matches_set(cls, snippet: Snippet, expected_token_set: TokenSet):
        """Validates that the snippet matches the expected token set."""
        if snippet.token_set_key != expected_token_set.key:
            raise ValueError(f"Snippet f{snippet} does not match expected token set {expected_token_set}.")

    def _assert_context_snippet_count(self, context_snippets: list[Snippet]):
        """Assert the number of context snippets matches the number of context token sets."""
        if len(context_snippets) != len(self.context):
            raise ValueError(
                f"Number of context snippets ({len(context_snippets)}) must match number of context token sets ({len(self.context)}).")

    def __str__(self) -> str:
        """String representation of the Instruction."""
        tokens_str: str = ', '.join(
            [''.join([token.key for token in token_set.tokens]) for token_set in self.get_token_sets()])
        samples_str: str = ',\n'.join([str(sample) for sample in self.samples])
        return f"Token Set(Tokens: {tokens_str}, Result: {self.final.key}, Samples:\n{samples_str})"

    def __hash__(self) -> int:
        """Hash based on the attributes of the Instruction."""
        return hash(str(sorted(self.to_dict().items())))

    def __eq__(self, other) -> bool:
        """
        Defines equality based on the attributes of the Instruction.
        Returns True if the other object is an Instruction and its attributes match this Instruction's attributes.
        """
        return isinstance(other, BaseInstruction) and self.__dict__ == other.__dict__

    def __dict__(self) -> dict:
        """Dictionary representation of the Instruction."""
        return self.to_dict()

    def to_dict(self) -> dict:
        """Convert the Instruction to a dictionary representation."""
        return {
            'tokens': [[token.to_dict() for token in token_set.tokens] for token_set in self.get_token_sets()],
            'result': self.final.to_dict() if self.final else None,
            'samples': self.samples
        }
