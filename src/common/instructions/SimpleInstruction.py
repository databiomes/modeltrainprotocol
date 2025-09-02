from typing import Sequence

from src.common.instructions.Instruction import Instruction
from src.common.tokens.Token import Token
from src.common.tokens.TokenSet import TokenSet, Snippet


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
    def add_sample(self, snippets: list[Snippet], value: int | float | None = None):
        """Add a sample to the Instruction.

        :param snippets: List of Snippet - each Snippet corresponds to a TokenSet in the context and response.
        :param value: Optional integer or float.

        Example:
            strings=["Hello, how are you?", "I'm fine.", "It was great to meet you, goodbye!"]
            numbers=[[10], [], [20]]
            value=42

        """
        sample: dict = self._create_base_sample(snippets=snippets, value=value)
        self.samples.append(sample)
