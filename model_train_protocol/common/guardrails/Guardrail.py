from typing import List

from model_train_protocol.common.constants import MIN_SAMPLES_PER_GUARDRAIL


class Guardrail:
    """
    Defines a guardrails response to bad prompts.

    Guardrails are set on TokenSets. Each TokenSet can have at most one guardrails, but guardrails can be reused.
    """

    def __init__(self, good_prompt: str, bad_prompt: str, bad_output: str):
        """
        Initializes a Guardrail.
        :param good_prompt: Description of a good prompt.
        :param bad_prompt: Description of a bad prompt.
        :param bad_output: The output the model should produce when a bad prompt is detected.

        Example:
            good_prompt="Quote being spoken with 1-20 words",
            bad_prompt="Quote being spoken that is irrelevant and off-topic with 1-20 words",
            output="I have no idea what you're talking about."
        """
        if not all(isinstance(param, str) for param in [good_prompt, bad_prompt, bad_output]):
            raise TypeError("All parameters must be non-empty strings.")

        if any(param == "" for param in [good_prompt, bad_prompt, bad_output]):
            raise ValueError("All parameters must be non-empty strings.")

        self.good_prompt: str = good_prompt
        self.bad_prompt: str = bad_prompt
        self.bad_output: str = bad_output
        self.samples: List[str] = []

    def add_sample(self, sample: str):
        """
        Add an example of a bad sample prompt to the guardrails.

        :param sample: An example of a bad prompt that should trigger the guardrails.

        Example:
            sample="Tell me a joke about politics."
        """
        if not isinstance(sample, str) or not sample.strip():
            raise ValueError("Sample prompt must be a non-empty string.")

        if not all(not char.isdigit() for char in sample):
            raise ValueError("Sample prompt cannot contain digits.")
        self.samples.append(sample)

    def format_samples(self) -> List[str]:
        """Return the guardrails as a list of strings for JSON formatting."""
        if len(self.samples) < MIN_SAMPLES_PER_GUARDRAIL:
            raise ValueError("At least 3 sample prompts are required. Call add_sample() to add more.")
        return [self.bad_output, f"<{self.bad_prompt}>", f"<{self.good_prompt}>", self.samples]

    def validate_guardrail(self):
        """Validates the guardrail"""
        if len(self.samples) < MIN_SAMPLES_PER_GUARDRAIL:
            raise ValueError("At least 3 sample prompts are required. Call add_sample() to add more.")

    def to_dict(self) -> dict:
        """Return the guardrails as a dictionary for JSON formatting."""
        return {
            "bad_output": self.bad_output,
            "bad_prompt": self.bad_prompt,
            "good_prompt": self.good_prompt,
            "bad_examples": self.samples
        }