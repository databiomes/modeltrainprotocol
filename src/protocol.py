import random
import json
from src.methods.token import Token
from src.methods.instruction import Instruction
from src.methods.guardrail import Guardrail
from src.methods.util import get_possible_emojis


class Protocol:
    def __init__(self):
        self.name: str
        self.memory: int
        self.context = []
        self.tokens = []
        self.instructions = []
        self.guardrails = dict()
        self.numbers = dict()
        self.none = None
        self.special_tokens = []
        self.possible_emojis = get_possible_emojis()

    def add_context(self, prompt):
        self.context.append(prompt)

    def add_token(self, string, emoji=None, default=False, user=False, num=False, desc=None, special=None):
        assert not any(token.string[:-1] in string for token in self.tokens), f"Token name '{string}' already used."
        if emoji is None:
            used_emojis = {token.emoji for token in self.tokens if token.emoji}
            available_emojis = list(set(self.possible_emojis) - used_emojis)
            emoji = random.choice(available_emojis) if available_emojis else None
        token = Token((string + "_") if not default else string, emoji, user, num, desc, special)
        self.tokens.append(token)
        return token

    def set_memory(self, memory):
        self.memory = memory

    def create_instruction(self, tokens, result=None, auto=False):
        if auto:
            tokens = tuple(inner_tuple for inner_tuple, count in tokens for _ in range(count))
        assert len(tokens) == self.memory, "The number of sets does not match the memory size."
        tokens = list(tokens)
        for idx, token in enumerate(tokens):
            if not isinstance(token, tuple):
                tokens[idx] = (token, ())
                token = [token]
            if "".join([tok.emoji for tok in token]) not in self.special_tokens:
                self.special_tokens.append("".join([tok.emoji for tok in token]))
            if result is not None and result.emoji not in self.special_tokens:
                self.special_tokens.append(result.emoji)
        tokens = tuple(tokens)
        flat_tokens = self.flatten_tuple(tokens)
        assert not flat_tokens[-1][-1].num, "Last token in a set cannot be a number."
        if self.none is None:
            self.none = self.add_token("<NON>", "🫙", default=True, special="none")
            self.special_tokens.append("🫙")
        instruction = Instruction(flat_tokens, self.none if result is None else result, self.memory)
        self.instructions.append(instruction)
        return instruction

    def flatten_tuple(self, tokens):
        tuple_groups = []
        if isinstance(tokens, tuple):
            current_group = []
            for item in tokens:
                if isinstance(item, tuple):
                    if current_group:
                        tuple_groups.append(tuple(current_group))
                        current_group = []
                    tuple_groups.extend(self.flatten_tuple(item))
                else:
                    current_group.append(item)
            if current_group:
                tuple_groups.append(tuple(current_group))
        return tuple_groups

    def create_guardrail(self, token_set, good_prompt, bad_prompt, output):
        guardrail = Guardrail(token_set, good_prompt, bad_prompt, output)
        self.guardrails[guardrail.key] = guardrail()
        return guardrail

    def add_guardrail_sample(self, guardrail, sample):
        guardrail.add_sample(sample)
        self.guardrails[guardrail.key] = guardrail()

    def add_number(self, num, min_value, max_value):
        if self.numbers is None:
            self.numbers = {"None": ''}
        key = num.string
        value = f"<Number between {min_value} and {max_value}>"
        self.numbers[key] = value

    def add_number_list(self, num, min_value, max_value, length):
        if self.numbers is None:
            self.numbers = {"None": ''}
        key = num.string
        value = f"<List of length {length} of numbers between {min_value} and {max_value}>"
        self.numbers[key] = value

    def create_template(self, path):
        unique_sets = {i: [] for i in range(self.memory)}
        unique_results = dict()
        valid_input_list = ["🏁",]
        valid_output_list = ["<string>",]
        for token_set in self.instructions:
            for idx, token in enumerate(token_set.tokens):
                token_user = [t.user for t in token]
                token_strings = "".join([t.string for t in token])
                token_emojis = []
                for t in token:
                    token_emojis.append(t.emoji + (self.numbers[t.string] if t.num else ""))
                token_emojis = "".join(token_emojis)
                unique_sets[idx].append(str(token_strings) + ": " + ((str(token_emojis) + "USER PROMPT") if any(token_user) and (idx == (len(unique_sets) - 1)) else str(token_emojis)) + "\n" + ("<string>" if idx != (len(token_set.tokens) - 1) else ""))
                if len(valid_input_list) < (((int(self.memory) * 2) - 1) + 2):
                    valid_input_list.append(((str(token_emojis) + "USER PROMPT") if any(token_user) and (idx == (len(unique_sets) - 1)) else str(token_emojis)))
                    if idx == (len(token_set.tokens) - 1):
                        valid_input_list.append("🏃\n")
                    else:
                        valid_input_list.append("<string>")
            unique_results[str(token_set.result.string)] = str(token_set.result.emoji)
            if len(valid_output_list) < 3:
                valid_output_list.append(str(token_set.result.emoji))
                valid_output_list.append("🎬")

        template = {
            "example_usage": {
                "valid_input": "\n".join(valid_input_list),
                "valid_output": "\n".join(valid_output_list)
            },
            "all_combinations": {
                "model_input": {},
                "model_output": {}
            }
        }
        template['all_combinations']['model_input']["<BOS>"] = "🏁"
        for i in range(int(self.memory)):
            template['all_combinations']['model_input'][f"{i}"] = unique_sets[i]
        template['all_combinations']['model_input']["<RUN>"] = "🏃"
        template['all_combinations']['model_output']["model_response"] = "<string>"
        template['all_combinations']['model_output']["model_results"] = unique_results
        template['all_combinations']['model_output']["<EOS>"] = "🎬"
        filename = f"{path}/template.json"
        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(template, file, indent=4, ensure_ascii=False)

    def serialize(self):
        template = {
            "name": self.name,
            "context": self.context,
            "tokens": {},
            "special_tokens": [],
            "instruction": {'memory': self.memory, 'sets': []},
            "guardrails": {'None': ''},
            "numbers": {'None': ''},
            "batches": {'pretrain': [], 'instruct': [], 'judge': [], 'ppo': []},
        }
        self.add_token("<BOS>", "🏁", default=True, special="start")
        self.special_tokens.append("🏁")
        self.add_token("<EOS>", "🎬", default=True, special="end")
        self.special_tokens.append("🎬")
        self.add_token("<RUN>", "🏃", default=True, special="infer")
        self.special_tokens.append("🏃")
        self.add_token("<PAD>", "🗒", default=True, special="pad")
        self.special_tokens.append("🗒")
        if self.guardrails is not None:
            self.add_token("<UNK>", "🛑", default=True, special="unknown")
            self.special_tokens.append("🛑")
        for token in self.tokens:
            template['tokens'][token.string] = {'emoji': token.emoji, 'num': token.num, 'user': token.user, 'desc': token.desc, 'special': token.special}
            if token.num:
                assert self.numbers is not None, f"{token.string} token was set to have numbers, but no numbers added."
        for special_token in self.special_tokens:
            template['special_tokens'].append(special_token)
        for token_set in self.instructions:
            samples = []
            ppo = []
            sample_strings = [sample['strings'] for sample in token_set.samples]
            sample_prompts = [sample['prompt'] for sample in token_set.samples]
            sample_numbers = [sample['number'] for sample in token_set.samples]
            sample_results = [sample['result'].string for sample in token_set.samples]
            sample_values = [sample['value'] for sample in token_set.samples]
            for s, p, n, r, v in zip(sample_strings, sample_prompts, sample_numbers, sample_results, sample_values):
                samples.append({'sample': s, 'prompt': p, 'number': n, 'result': r, 'value': v})
            ppo_strings = [sample['strings'] for sample in token_set.ppo]
            ppo_prompts = [sample['prompt'] for sample in token_set.ppo]
            ppo_numbers = [sample['number'] for sample in token_set.ppo]
            ppo_results = [sample['result'].string for sample in token_set.ppo]
            ppo_values = [sample['value'] for sample in token_set.ppo]
            ppo_a_samples = [sample['a_sample'] for sample in token_set.ppo]
            ppo_b_samples = [sample['b_sample'] for sample in token_set.ppo]
            ppo_pref = [sample['pref'] for sample in token_set.ppo]
            for s, p, n, r, v, a, b, pr in zip(ppo_strings, ppo_prompts, ppo_numbers, ppo_results, ppo_values, ppo_a_samples, ppo_b_samples, ppo_pref):
                ppo.append({'sample': s, 'prompt': p, 'number': n, 'result': r, 'value': v, 'a': a, 'b': b, 'pref': pr})
            memory_set = []
            for token_tuple in token_set.tokens:
                token_strings = [t.string for t in token_tuple]
                memory_set.append(token_strings)
            template['instruction']['sets'].append(
                {
                    "set": memory_set,
                    "result": token_set.result.string,
                    "samples": samples,
                    "ppo": ppo,
                }
            )
        for key, value in self.guardrails.items():
            if key == "None":
                continue
            template['guardrails'][key] = value
        for key, value in self.numbers.items():
            if key == "None":
                continue
            template['numbers'][key] = value
        return template

    def save(self, path, name):
        filename = f"{path}/{name}.json"
        self.name = name
        print(f"Saving Model Train Protocol to {filename}...")
        mtp_template = self.serialize()
        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(mtp_template, file, indent=4, ensure_ascii=False)



