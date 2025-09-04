import json
import os

from src.common.instructions.Instruction import Instruction
from src.common.tokens.Token import Token
from src.common.util import get_possible_emojis


class Protocol:
    """Model Training Protocol (MTP) class for creating the training configuration."""

    def __init__(self, name: str, instruction_sample_lines: int):
        """Initialize the Model Training Protocol (MTP)"""
        self.name: str = name
        self.instruction_sample_lines: int = instruction_sample_lines  # Number of lines in instruction samples
        assert self.instruction_sample_lines >= 3, "A minimum of 3 sample lines is required for all instructions."

        self.context: list[str] = []
        self.tokens: set[Token] = set()
        self.instructions: set[Instruction] = set()
        self.guardrails: dict[str, list[str]] = dict()
        self.numbers: dict[str, str] = dict()
        self.none = None
        self.special_tokens: set[str] = set()
        self.possible_emoji_keys: set[str] = get_possible_emojis()
        self.used_keys: set[str] = set()

    def add_context(self, context: str):
        """Adds a line of context to the model."""
        self.context.append(context)

    def add_token(self, token: Token):
        """
        Adds a unique token to the protocol.

        Validates that the token's value and key are unique.
        :param token: The Token instance to add.
        """
        if token in self.tokens:
            raise ValueError(f"Token value '{token.value}' already used.")

        if token.key in self.used_keys:
            raise ValueError(f"Token key '{token.key}' already used.")

        if token.key is None:
            available_keys: set[str] = self.possible_emoji_keys - self.used_keys
            if len(available_keys) == 0:
                raise ValueError("No available emoji keys left to assign. Please specify a key for the token.")
            key = available_keys.pop()
            token.key = key

        self.tokens.add(token)
        self.used_keys.add(token.key)

    def add_instruction(self, instruction: Instruction):
        """
        Adds an Instruction (and its components) to the protocol.

        Asserts that all samples in the instruction match the defined sample line size.
        """
        # Assert all samples match the defined sample line size
        for sample in instruction.samples:
            assert len(sample['strings']) == self.instruction_sample_lines, \
                "The number of sample lines does not match the memory size."

        # Add all token combos as special tokens
        for token_set in instruction.get_token_sets():
            self.special_tokens.add(token_set.key)

        # Add the result token as a special token
        if instruction.final.key is not None:
            self.special_tokens.add(instruction.final.key)

        # Add the instruction to the protocol
        self.instructions.add(instruction)

    def add_number(self, num, min_value, max_value):
        """Adds a number range to the protocol."""
        if self.numbers is None:
            self.numbers = {"None": ''}
        key = num.value
        value = f"<Number between {min_value} and {max_value}>"
        self.numbers[key] = value

    def add_number_list(self, num, min_value, max_value, length):
        """Adds a number list range to the protocol."""
        if self.numbers is None:
            self.numbers = {"None": ''}
        key = num.value
        value = f"<List of length {length} of numbers between {min_value} and {max_value}>"
        self.numbers[key] = value

    def _set_guardrails(self):
        """Sets all guardrails from TokenSets into the protocol."""
        # Add all guardrails to the protocol
        for instruction in self.instructions:
            if instruction.response.guardrail is not None:
                # instruction.response is the user TokenSet
                self.guardrails[instruction.response.key] = instruction.response.guardrail.format_samples()

    def _create_special_tokens(self):
        """Adds all special tokens to the protocol."""
        bos_token: Token = Token(value="<BOS>", key="🏁", default=True, special="start")
        eos_token: Token = Token(value="<EOS>", key="🎬", default=True, special="end")
        run_token: Token = Token(value="<RUN>", key="🏃", default=True, special="infer")
        pad_token: Token = Token(value="<PAD>", key="🗒", default=True, special="pad")
        self.special_tokens.add(bos_token.key)
        self.special_tokens.add(eos_token.key)
        self.special_tokens.add(run_token.key)
        self.special_tokens.add(pad_token.key)

        if len(self.guardrails) > 0:
            unk_token: Token = Token(value="<UNK>", key="🛑", default=True, special="unknown")
            self.special_tokens.add(unk_token.key)

        if self.none is None:
            non_token: Token = Token(value="<NON>", key="🫙", default=True, special="none")
            self.special_tokens.add(non_token.key)

    def create_template(self, path: str | None = None):
        """
        Create a template JSON file for the model training protocol.

        :param path: The directory path where the template file will be saved. If None, saves in the current directory.
        """
        if path is None:
            path = os.getcwd()

        self._set_guardrails()

        unique_sets = {i: [] for i in range(self.instruction_sample_lines)}
        unique_results = dict()
        valid_input_list = ["🏁", ]
        valid_output_list = ["<string>", ]
        for token_set in self.instructions:
            for idx, token in enumerate(token_set.context):
                token_user = [t.user for t in token]
                token_strings = "".join([t.value for t in token])
                token_keys = []
                for t in token:
                    token_keys.append(t.key + (self.numbers[t.value] if t.num else ""))
                token_keys = "".join(token_keys)
                unique_sets[idx].append(str(token_strings) + ": " + (
                    (str(token_keys) + "USER PROMPT") if any(token_user) and (idx == (len(unique_sets) - 1)) else str(
                        token_keys)) + "\n" + ("<string>" if idx != (len(token_set.context) - 1) else ""))
                if len(valid_input_list) < (((int(self.instruction_sample_lines) * 2) - 1) + 2):
                    valid_input_list.append(((str(token_keys) + "USER PROMPT") if any(token_user) and (
                            idx == (len(unique_sets) - 1)) else str(token_keys)))
                    if idx == (len(token_set.context) - 1):
                        valid_input_list.append("🏃\n")
                    else:
                        valid_input_list.append("<string>")
            unique_results[str(token_set.final.value)] = str(token_set.final.key)
            if len(valid_output_list) < 3:
                valid_output_list.append(str(token_set.final.key))
                valid_output_list.append("🎬")

        template: dict[str, dict] = {
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
        for i in range(int(self.instruction_sample_lines)):
            template['all_combinations']['model_input'][f"{i}"] = unique_sets[i]
        template['all_combinations']['model_input']["<RUN>"] = "🏃"
        template['all_combinations']['model_output']["model_response"] = "<string>"
        template['all_combinations']['model_output']["model_results"] = unique_results
        template['all_combinations']['model_output']["<EOS>"] = "🎬"
        filename = f"{path}/template.json"
        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(template, file, indent=4, ensure_ascii=False)

    def _serialize(self):
        template = {
            "name": self.name,
            "context": self.context,
            "tokens": {},
            "special_tokens": [],
            "instruction": {'memory': self.instruction_sample_lines, 'sets': []},
            "guardrails": {'None': ''},
            "numbers": {'None': ''},
            "batches": {'pretrain': [], 'instruct': [], 'judge': [], 'ppo': []},
        }

        # Add tokens to the template
        tokens_dict: dict[str, dict] = {}
        for token in self.tokens:
            token_dict: dict[str, dict] = token.to_dict()
            token_dict.pop("value")
            tokens_dict[token.value] = token_dict
        template['tokens'] = tokens_dict
        # TODO: Refactor Tokens to have UserToken and NumberToken and SpecialToken subclasses.
        # if token.num:
        #     assert self.numbers is not None, f"{token.value} token was set to have numbers, but no numbers added."

        # Add special tokens to the template
        self._create_special_tokens()
        for special_token in self.special_tokens:
            template['special_tokens'].append(special_token)

        # Add instructions to the template
        for instruction in self.instructions:
            template['instruction']['sets'].append(
                {
                    "set": instruction.serialize_memory_set(),
                    "result": instruction.final.value,
                    "samples": instruction.serialize_samples(),
                    "ppo": instruction.serialize_ppo(),
                }
            )

        # Add guardrails to the template
        for key, value in self.guardrails.items():
            template['guardrails'][key] = value

        # Add numbers to the template
        for key, value in self.numbers.items():
            template['numbers'][key] = value

        return template

    def save(self, name: str | None = None, path: str | None = None):
        """
        Saves the protocol to a JSON file.
        :param name: The name of the file (without extension). If None, uses the protocol's name.
        :param path: The directory path where the file will be saved. If None, saves in the current directory.
        """
        if name is None:
            name = self.name
        if path is None:
            path = os.getcwd()
        os.makedirs(path, exist_ok=True)
        filename = f"{path}\\{name}.json"
        print(f"Saving Model Train Protocol to {filename}...")
        mtp_template = self._serialize()
        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(mtp_template, file, indent=4, ensure_ascii=False)
