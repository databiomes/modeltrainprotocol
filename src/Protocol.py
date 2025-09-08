import itertools
import json
import os
import string

from src.common.instructions.Instruction import Instruction
from src.common.tokens.DefaultSpecialToken import DefaultSpecialToken
from src.common.tokens.Token import Token
from src.common.util import get_possible_emojis, get_extended_possible_emojis


class Protocol:
    """Model Training Protocol (MTP) class for creating the training configuration."""

    def __init__(self, name: str, instruction_sample_lines: int):
        """
        Initialize the Model Training Protocol (MTP)

        :param name: The name of the protocol.
        :param instruction_sample_lines: The number of lines in each instruction sample. Must be at least 3.
        """
        self.name: str = name
        self.instruction_sample_lines: int = instruction_sample_lines  # Number of lines in instruction samples
        assert self.instruction_sample_lines >= 3, "A minimum of 3 sample lines is required for all instructions."

        self.context: list[str] = []
        self.tokens: set[Token] = set()
        self.instructions: set[Instruction] = set()
        self.guardrails: dict[str, list[str]] = dict()
        self.numbers: dict[str, str] = dict()
        self.none = None
        self.special_tokens: set[Token] = set()
        self.instruction_token_key_sets: set[str] = set()
        self.possible_emoji_keys: set[str] = get_possible_emojis()
        self.used_keys: set[str] = set()

    def add_context(self, context: str):
        """Adds a line of context to the model."""
        self.context.append(context)

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

            # Add all tokens in the instruction to the protocol
            for token in token_set.tokens:
                if token not in self.tokens:
                    self._add_token(token)

            self.instruction_token_key_sets.add(token_set.get_token_key_set())

        # Add the result token as a special token
        if instruction.final.key is not None:
            self.instruction_token_key_sets.add(instruction.final.key)

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

    def save(self, name: str | None = None, path: str | None = None):
        """
        Saves the protocol to a JSON file. This file can be submitted to Databiomes for model training.

        :param name: The name of the file (without extension). If None, uses the protocol's name.
        :param path: The directory path where the file will be saved. If None, saves in the current directory.
        """
        if name is None:
            name = self.name
        if path is None:
            path = os.getcwd()
        os.makedirs(path, exist_ok=True)
        filename = f"{path}\\{name}_model.json"
        print(f"Saving Model Train Protocol to {filename}...")
        mtp_template = self._serialize()
        mtp_template = self._rename_template_elements(mtp_template)
        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(mtp_template, file, indent=4, ensure_ascii=False)

    def template(self, path: str | None = None):
        """
        Create a template JSON file for the model training protocol.

        The template json file includes example usage and all possible combinations of model inputs and
        outputs based on the defined tokens and instructions.

        :param path: The directory path where the template file will be saved. If None, saves in the current directory.
        """
        if path is None:
            path = os.getcwd()

        self._set_all_elements()
        unique_sets = {i: set() for i in range(self.instruction_sample_lines)}
        unique_results = dict()
        valid_input_list = ["🏁", ]
        valid_output_list = ["<string>", ]
        for instruction in self.instructions:
            for idx, token_set in enumerate(instruction.get_token_sets()):
                token_user = [t.user for t in token_set]
                token_strings = "".join([t.value for t in token_set])
                token_keys = []
                for t in token_set:
                    token_keys.append(t.key + (self.numbers[t.value] if t.num else ""))
                token_keys = "".join(token_keys)
                unique_sets[idx].add(str(token_strings) + ": " + (
                    (str(token_keys) + "USER PROMPT") if any(token_user) and (idx == (len(unique_sets) - 1)) else str(
                        token_keys)) + "\n" + ("<string>" if idx != (len(instruction.context) - 1) else ""))
                if len(valid_input_list) < (((int(self.instruction_sample_lines) * 2) - 1) + 2):
                    valid_input_list.append(((str(token_keys) + "USER PROMPT") if any(token_user) and (
                            idx == (len(unique_sets) - 1)) else str(token_keys)))
                    if idx == (len(instruction.context) - 1):
                        valid_input_list.append("🏃\n")
                    else:
                        valid_input_list.append("<string>")
            unique_results[str(instruction.final.value)] = str(instruction.final.key)
            if len(valid_output_list) < 3:
                valid_output_list.append(str(instruction.final.key))
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
            template['all_combinations']['model_input'][f"{i}"] = list(unique_sets[i])
        template['all_combinations']['model_input']["<RUN>"] = "🏃"
        template['all_combinations']['model_output']["model_response"] = "<string>"
        template['all_combinations']['model_output']["model_results"] = unique_results
        template['all_combinations']['model_output']["<EOS>"] = "🎬"
        filename = f"{path}\\{self.name}_template.json"
        print(f"Saving Model Train Protocol Template to {filename}...")
        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(template, file, indent=4, ensure_ascii=False)

    def _add_token(self, token: Token):
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
            token.key = self._get_random_key()

        self.tokens.add(token)
        self.used_keys.add(token.key)

    def _set_guardrails(self):
        """Sets all guardrails from TokenSets into the protocol."""
        # Add all guardrails to the protocol
        for instruction in self.instructions:
            if instruction.response.guardrail is not None:
                # instruction.response is the user TokenSet
                self.guardrails[instruction.response.key] = instruction.response.guardrail.format_samples()

    def _create_default_special_tokens(self):
        """Adds all special tokens to the protocol."""
        bos_token: DefaultSpecialToken = DefaultSpecialToken(value="<BOS>", key="🏁", special="start")
        eos_token: DefaultSpecialToken = DefaultSpecialToken(value="<EOS>", key="🎬", special="end")
        run_token: DefaultSpecialToken = DefaultSpecialToken(value="<RUN>", key="🏃", special="infer")
        pad_token: DefaultSpecialToken = DefaultSpecialToken(value="<PAD>", key="🗒", special="pad")
        self.special_tokens.add(bos_token)
        self.special_tokens.add(eos_token)
        self.special_tokens.add(run_token)
        self.special_tokens.add(pad_token)

        if len(self.guardrails) > 0:
            unk_token: DefaultSpecialToken = DefaultSpecialToken(value="<UNK>", key="🛑", special="unknown")
            self.special_tokens.add(unk_token)

        if self.none is None:
            non_token: DefaultSpecialToken = DefaultSpecialToken(value="<NON>", key="🫙", special="none")
            self.special_tokens.add(non_token)

    def _serialize(self):
        """Serializes the protocol to a dictionary."""
        self._set_all_elements()
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

        for token in self.special_tokens:
            token_dict: dict[str, dict] = token.to_dict()
            token_dict.pop("value")
            tokens_dict[token.value] = token_dict
        template['tokens'] = tokens_dict

        # Add special tokens to the template
        self._create_default_special_tokens()
        for special_token in self.special_tokens:
            template['special_tokens'].append(special_token.key)

        # Add instruction token key sets to the template
        for instruction_token_key_set in self.instruction_token_key_sets:
            template['special_tokens'].append(instruction_token_key_set)

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
        template['guardrails'] = {'None': ''}
        for key, value in self.guardrails.items():
            template['guardrails'][key] = value

        # Add numbers to the template
        for key, value in self.numbers.items():
            template['numbers'][key] = value

        return template

    def _set_all_elements(self):
        """Sets all elements in the protocol before serialization."""
        self._set_guardrails()
        self._create_default_special_tokens()

    @classmethod
    def _rename_template_elements(cls, template: dict):
        """
        Renames elements in the template to match the previous output format for backwards compatibility.
        :param template: The original template dictionary.
        :return: The modified template dictionary with renamed elements.
        """
        # Rename Token 'key' to 'emoji'
        for token_value, token_info in template.get('tokens', {}).items():
            if 'key' in token_info:
                token_info['emoji'] = token_info.pop('key')

        # Rename sample number to None if an array of empty arrays
        for instruction in template.get('instruction', {}).get('sets', []):
            for sample in instruction['samples']:
                if all(num == [] for num in sample['number']):
                    sample['number'] = None

        return template

    def _get_random_key(self) -> str:
        """
        Generates a random key that is not already used in the protocol.

        Prioritizes single-character emojis, then expands to multi-character emojis,
        and finally uses alphanumeric characters if all emojis are exhausted.

        :return: A unique key as a string.
        """
        available_keys: set[str] = self.possible_emoji_keys - self.used_keys

        if len(available_keys) == 0:
            self.possible_emoji_keys = get_extended_possible_emojis()
            available_keys: set = self.possible_emoji_keys - self.used_keys

            if len(available_keys) == 0:
                # If no available emoji keys, begin assigning alphanumeric keys
                alphanumeric_chars: str = string.ascii_letters + string.digits

                # Calculate how many alphanumeric keys have already been used
                already_used_alphanumeric: int = len(self.used_keys) - len(self.possible_emoji_keys)

                # Progressively generate combinations, skipping the first 'already_used_alphanumeric' keys
                key_generator = itertools.islice(
                    itertools.chain.from_iterable(
                        itertools.product(alphanumeric_chars, repeat=length)
                        for length in itertools.count(1)
                    ),
                    already_used_alphanumeric,  # Skip this many keys
                    None  # No upper limit
                )

                # Find the first unused key
                for combo in key_generator:
                    key: str = ''.join(combo)
                    if key not in self.used_keys:  # Failsafe, will be True unless user has manually added the specific key
                        return key

        key: str = available_keys.pop()
        return key
