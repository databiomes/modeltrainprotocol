from typing import Sequence

from .Instruction import Instruction
from ..tokens.Token import Token
from ..tokens.TokenSet import TokenSet, Snippet


class SimpleInstruction(Instruction):
    """
    A SimpleInstruction is an instruction without a user prompt.

    Samples must be added to the Instruction to provide context for the model.
    A minimum of 3 samples must be added to an Instruction.

    Example:
        tokens= [
                 ( Token("SentenceLength", num=True), Token("Greeting")),
                 ( Token("CurtResponse")),
                 ( Token("SentenceLength", num=True), Token("Goodbye")),
    """

    def __init__(self, context: Sequence[TokenSet], response: TokenSet, final: Token):
        """Initializes an Instruction instance."""
        super().__init__(context=context, response=response, final=final)
        assert not self.contains_user(), "Instruction cannot contain a user token in response. Use UserInstruction for user inputs."

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

        all_snippets: list[Snippet] = context_snippets + [output_snippet]
        sample: dict = self._create_base_sample(snippets=all_snippets, value=value)
        self.samples.append(sample)