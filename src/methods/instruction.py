from src.methods.token import Token


class Instruction:
    """
    Class representing an instruction with tokens, result, memory, and samples.

    An Instruction is a set of tokens that show possible input combinations for a model.

    Samples must be added to the Instruction to provide context for the model.
    A minimum of 3 samples must be added to an Instruction.
    """

    def __init__(self, tokens: list[tuple[Token]], result: Token, memory: int):
        """Initializes an Instruction instance."""
        self.tokens: list[tuple[Token]] = tokens
        self.result: Token = result
        self.memory: int = memory
        self.samples: list[dict] = []

    def add_sample(self, strings: list[str], prompt=None, numbers=None, value=None):
        """Add a sample to the Instruction."""
        assert len(strings) >= self.memory, "The number of lines does not match the memory size."
        if numbers is not None:
            self.number_check(numbers)
        if value is not None:
            assert type(value) == int or type(value) == float, "Value is not a number."
        else:
            value = "None"
        self.samples.append({'strings': strings, 'prompt': prompt, 'number': numbers, 'result': self.result,
                             'value': value})

    def number_check(self, numbers):
        assert isinstance(numbers, list), "The number is not set as a list."
        num_check = sum(
            [element if isinstance(element, list) else [element] for sublist in numbers for element in sublist], [])
        assert all(isinstance(num, (int, float)) for num in num_check), "Not all elements are numbers."
        num_tokens = [[token.key] for tokens in self.tokens for token in tokens if token.num]
        num_numbers = [item for sublist in numbers for item in sublist if item or item == 0]
        assert len(num_tokens) == len(num_numbers), "Number samples don't match memory count."
        for num, tok in zip(numbers, self.tokens):
            num_token = [token.key for token in tok if token.num]
            num = [num for num in num if num or num == 0]
            assert len(num) == len(num_token), "Not all numbers provided."

    def __str__(self):
        """String representation of the Instruction."""
        tokens_str = ', '.join([''.join([token.key for token in token_tuple]) for token_tuple in self.tokens])
        samples_str = ',\n'.join([f"Sample(Strings: {sample['strings']}, Result: {sample['result'].key + sample['value'] if sample['value'] is not None else ''}" for sample in self.samples])
        return f"Token Set(Tokens: {tokens_str}, Result: {self.result.key}, Samples:\n{samples_str})"

    def to_dict(self):
        """Convert the Instruction to a dictionary representation."""
        return {
            'tokens': [[token.to_dict() for token in token_tuple] for token_tuple in self.tokens],
            'result': self.result.to_dict() if self.result else None,
            'samples': self.samples
        }