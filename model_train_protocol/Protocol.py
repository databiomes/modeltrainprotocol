import itertools
import json
import os
import string

from . import Token
from ._internal.ProtocolFile import ProtocolFile
from ._internal.TemplateFile import TemplateFile
from .common.instructions.Instruction import Instruction
from .common.tokens.SpecialToken import SpecialToken
from .common.util import get_possible_emojis, get_extended_possible_emojis


class Protocol:
    """Model Training Protocol (MTP) class for creating the training configuration."""

    def __init__(self, name: str, context_lines: int):
        """
        Initialize the Model Training Protocol (MTP)

        :param name: The name of the protocol.
        :param context_lines: The number of lines in each instruction sample. Must be at least 3.
        """
        self.name: str = name
        self.context_lines: int = context_lines  # Number of lines in instruction samples
        assert self.context_lines >= 3, "A minimum of 3 sample lines is required for all instructions."

        self.context: list[str] = []
        self.tokens: set[Token] = set()
        self.instructions: set[Instruction] = set()
        self.guardrails: dict[str, list[str]] = dict()
        self.numbers: dict[str, str] = dict()
        self.none = None
        self.special_tokens: set[Token] = set()
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
        if instruction in self.instructions:
            raise ValueError("Instruction already added to the protocol.")

        # Assert all samples match the defined sample line size
        for sample in instruction.samples:
            assert len(sample['strings']) == self.context_lines, \
                "The number of sample lines does not match the memory size."

        # Add all token combos as special tokens
        for token_set in instruction.get_token_sets():

            # Add all tokens in the instruction to the protocol
            for token in token_set.tokens:
                if token not in self.tokens:
                    self._add_token(token)

        # Add the instruction to the protocol
        self.instructions.add(instruction)

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
        protocol_file: ProtocolFile = self._create_protocol_file()
        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(protocol_file.to_json(), file, indent=4, ensure_ascii=False)

    def template(self, path: str | None = None):
        """
        Create a template JSON file for the model training protocol.

        The template json file includes example usage and all possible combinations of model inputs and
        outputs based on the defined tokens and instructions.

        :param path: The directory path where the template file will be saved. If None, saves in the current directory.
        """
        if path is None:
            path = os.getcwd()

        self._set_protocol_elements()
        template_file: TemplateFile = TemplateFile(
            instructions=list(self.instructions),
            context_lines=self.context_lines
        )

        filename = f"{path}\\{self.name}_template.json"
        print(f"Saving Model Train Protocol Template to {filename}...")
        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(template_file.to_json(), file, indent=4, ensure_ascii=False)


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
        bos_token: SpecialToken = SpecialToken(value="<BOS>", key="🏁", special="start")
        eos_token: SpecialToken = SpecialToken(value="<EOS>", key="🎬", special="end")
        run_token: SpecialToken = SpecialToken(value="<RUN>", key="🏃", special="infer")
        pad_token: SpecialToken = SpecialToken(value="<PAD>", key="🗒", special="pad")
        self.special_tokens.add(bos_token)
        self.special_tokens.add(eos_token)
        self.special_tokens.add(run_token)
        self.special_tokens.add(pad_token)

        if len(self.guardrails) > 0:
            unk_token: SpecialToken = SpecialToken(value="<UNK>", key="🛑", special="unknown")
            self.special_tokens.add(unk_token)

        if self.none is None:
            non_token: SpecialToken = SpecialToken(value="<NON>", key="🫙", special="none")
            self.special_tokens.add(non_token)

    def _create_protocol_file(self) -> ProtocolFile:
        """Creates a ProtocolFile for model training."""
        self._set_protocol_elements()
        protocol_file: ProtocolFile = ProtocolFile(
            name=self.name,
            context=self.context,
            context_lines=self.context_lines
        )
        # Add regular tokens
        protocol_file.add_tokens(self.tokens)

        # Add special tokens
        protocol_file.add_tokens(self.special_tokens)

        # Add instructions
        protocol_file.add_instructions(self.instructions)

        return protocol_file

    def _set_protocol_elements(self):
        """
        Sets all elements in the protocol before serialization.

        This includes setting guardrails from their TokenSets and creating default special tokens.
        """
        self._set_guardrails()
        self._create_default_special_tokens()

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
