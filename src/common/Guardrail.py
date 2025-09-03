from src.common.tokens.TokenSet import TokenSet


class Guardrail:
    """Defines a guardrail response to bad prompts. Guardrails are set on a TokenSet."""

    def __init__(self, token_set: TokenSet, good_prompt: str, bad_prompt: str, bad_output: str):
        """
        Initializes a Guardrail.
        :param token_set: The TokenSet the guardrail is set on.
        :param good_prompt: Description of a good prompt.
        :param bad_prompt: Description of a bad prompt.
        :param bad_output: The output the model should produce when a bad prompt is detected.

        Example:
            good_prompt="Quote being spoken with 1-20 words",
            bad_prompt="Quote being spoken that is irrelevant and off-topic with 1-20 words",
            output="I have no idea what you're talking about."
        """
        if not isinstance(token_set, TokenSet):
            raise TypeError("Guardrails can only be set on a TokenSet.")

        self.token_set: TokenSet = token_set
        self.good_prompt: str = good_prompt
        self.bad_prompt: str = bad_prompt
        self.bad_output: str = bad_output
        self.samples: list[str] = []
        self.key: str = self.token_set.key

    def add_sample(self, sample: str):
        """
        Add an example of a bad sample prompt to the guardrail.

        :param sample: An example of a bad prompt that should trigger the guardrail.

        Example:
            sample="Tell me a joke about politics."
        """
        assert all(not char.isdigit() for char in sample), "Sample prompt cannot contain digits."
        self.samples.append(sample)

    def format_samples(self) -> list[str]:
        """Return the guardrail as a list of strings for JSON formatting."""
        assert len(self.samples) >= 3, "At least 3 sample prompts are required. Call add_sample() to add more."
        return [self.bad_output, f"<{self.bad_prompt}>", f"<{self.good_prompt}>", self.samples]
