from src.common.instructions.BaseInstruction import BaseInstruction
from src.common.Token import Token


class Guardrail:
    """Defines a guardrail response to bad prompts. Guardrails are set on an Instruction."""

    def __init__(self, instruction: BaseInstruction, good_prompt: str, bad_prompt: str, bad_output: str):
        """
        Initializes a Guardrail.
        :param instruction: The Instruction the guardrail is set on.
        :param good_prompt: Description of a good prompt.
        :param bad_prompt: Description of a bad prompt.
        :param bad_output: The output the model should produce when a bad prompt is detected.

        Example:
            good_prompt="Quote being spoken with 1-20 words",
            bad_prompt="Quote being spoken that is irrelevant and off-topic with 1-20 words",
            output="I have no idea what you're talking about."
        """
        self.instruction: BaseInstruction = instruction
        self.token_set: tuple[Token] = instruction.tokens[-1]
        self.good_prompt: str = good_prompt
        self.bad_prompt: str = bad_prompt
        self.bad_output: str = bad_output
        self.bad_samples: list[str] = []
        self.key: str = ""
        user_check: bool = False
        for token in self.token_set:
            if token.user:
                user_check = True
            self.key += token.value
        assert user_check, "Guardrail requires a user token in the token set."

    def add_sample(self, sample: str):
        """Add an example of a bad sample prompt to the guardrail."""
        assert all(not char.isdigit() for char in sample), "Sample prompt cannot contain digits."
        self.bad_samples.append(sample)

    def __call__(self) -> list[str]:
        """Return the guardrail as a list of strings for JSON formatting."""
        assert len(self.bad_samples) >= 3, "At least 3 sample prompts are required. Call add_sample() to add more."
        return [self.bad_output, f"<{self.bad_prompt}>", f"<{self.good_prompt}>", self.bad_samples]
