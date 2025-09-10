import abc
from abc import ABC
from typing import Sequence

from ..tokens.Token import Token
from ..tokens.TokenSet import TokenSet, Snippet


class Instruction(ABC):
    """
    An Instruction is a set of tokens that show possible input combinations for a model.

    Samples must be added to the Instruction to provide context for the model.
    A minimum of 3 samples must be added to an Instruction.

    Example:
        context = TokenSet(
        context = [
                 ( Token("SentenceLength", num=True), Token("Greeting")),
                 ( Token("CurtResponse")),
                 ( Token("SentenceLength", num=True), Token("Goodbye")),

    """

    def __init__(self, context: Sequence[TokenSet], response: TokenSet, final: Token):
        """Initializes the common attributes to all Instructions."""
        self.context: Sequence[TokenSet] = context
        self.response: TokenSet = response
        self.final: Token = final
        self.samples: list[dict] = []

    @abc.abstractmethod
    def add_sample(self):
        """Add a sample to the Instruction."""
        raise NotImplementedError("Subclasses must implement add_sample method.")

    def get_token_sets(self) -> list[TokenSet]:
        """Returns all tokens in the instruction as a list of tuples."""
        all_tokens: list = []
        for token_set in self.context:
            all_tokens.append(token_set)
        all_tokens.append(self.response)
        return all_tokens

    def contains_user(self) -> bool:
        """
        Returns True if the response contains a user token, else False
        """
        return self.response.is_user

    def serialize_samples(self) -> list[dict]:
        """Serializes the Instruction samples"""
        samples = []
        sample_strings = [sample['strings'] for sample in self.samples]
        sample_prompts = [sample['prompt'] for sample in self.samples]
        sample_numbers = [sample['number'] for sample in self.samples]
        sample_results = [sample['result'].value for sample in self.samples]
        sample_values = [sample['value'] for sample in self.samples]
        for s, p, n, r, v in zip(sample_strings, sample_prompts, sample_numbers, sample_results, sample_values):
            samples.append({'sample': s, 'prompt': p, 'number': n, 'result': r, 'value': v})
        return samples

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

    def _create_base_sample(self, snippets: list[Snippet], value: int | float | None = None) -> dict:
        """Create a base sample dictionary without a prompt."""
        if value is not None:
            assert type(value) == int or type(value) == float, "Value is not a number."
        else:
            value = "None"

        # format sample
        strings: list[str] = []
        numbers: list[list[int]] = []
        for snippet in snippets:
            strings.append(snippet.string)
            numbers.append(snippet.numbers)

        return {'strings': strings, 'number': numbers, 'result': self.final, 'value': value, 'prompt': None}

    def _assert_valid_value(self, value: int | float | None):
        """
        Assert value is provided if self.final is a number Token, else assert value is None
        :param value: Optional value ascribed to the final Instruction output IF the final Token output is a number
        """
        if self.final.num and value is None:
            raise ValueError("Value must be provided when final token is a number.")
        if self.final.num and not (isinstance(value, int) or isinstance(value, float)):
            raise TypeError("Value must be an int or float when final token is a number.")
        if not self.final.num and value is not None:
            raise ValueError("Value must be None when final token is not a number.")

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
        samples_str: str = ',\n'.join([
            f"Sample(Strings: {sample['strings']}, Result: {sample['result'].key + sample['value'] if sample['value'] is not None else ''}"
            for sample in self.samples])
        return f"Token Set(Tokens: {tokens_str}, Result: {self.final.key}, Samples:\n{samples_str})"

    def __hash__(self) -> int:
        """Hash based on the attributes of the Instruction."""
        return hash(str(sorted(self.to_dict().items())))

    def __eq__(self, other) -> bool:
        """
        Defines equality based on the attributes of the Instruction.
        Returns True if the other object is an Instruction and its attributes match this Instruction's attributes.
        """
        return isinstance(other, Instruction) and self.__dict__ == other.__dict__

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
