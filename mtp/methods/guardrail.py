class Guardrail:
    def __init__(self, token_set, good_prompt, bad_prompt, output):
        self.token_set = token_set
        self.good_prompt = good_prompt
        self.bad_prompt = bad_prompt
        self.output = output
        self.bad_samples = []
        self.key = ""
        user_check = False
        for token in self.token_set:
            if token.user:
                user_check = True
            self.key += token.string
        assert user_check, "Guardrail requires a user token in the token set."

    def add_sample(self, sample):
        self.bad_samples.append(sample)

    def __call__(self):
        assert all(all(not char.isdigit() for char in s) for s in self.bad_samples), "Sample prompts cannot contain a digit."
        return [self.output, f"<{self.bad_prompt}>", f"<{self.good_prompt}>", self.bad_samples]