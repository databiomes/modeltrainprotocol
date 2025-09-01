from src.common.token import Token


class Guardrail:
    """Defines a guardrail response to bad prompts."""
    def __init__(self, token_set: set[Token] | list[Token], good_prompt: str, bad_prompt: str, bad_output: str):
        self.token_set: set[Token] | list[Token] = token_set
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

    def add_sample(self, sample):
        self.bad_samples.append(sample)

    def __call__(self):
        assert all(all(not char.isdigit() for char in s) for s in self.bad_samples), "Sample prompts cannot contain a digit."
        return [self.bad_output, f"<{self.bad_prompt}>", f"<{self.good_prompt}>", self.bad_samples]