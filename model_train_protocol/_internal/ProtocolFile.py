from dataclasses import dataclass, field
from typing import Collection

from model_train_protocol import Token, NumToken
from model_train_protocol.common.guardrails import Guardrail
from model_train_protocol.common.instructions import Instruction
from model_train_protocol.common.tokens import TokenSet, SpecialToken


class ProtocolFile:
    """Manages the model.json file for model training protocols."""

    @dataclass
    class ProtocolInstruction:
        """Represents an instruction in the template."""

        context_lines: int
        sets: list = field(default_factory=list)

    @dataclass
    class ProtocolInstructionSet:
        """Represents an instruction set in the template."""

        set: list[list[str]]
        result: str
        samples: list
        ppo: list

    @dataclass
    class Batches:
        """Represents batches in the template."""

        pretrain: list = field(default_factory=list)
        instruct: list = field(default_factory=list)
        judge: list = field(default_factory=list)
        ppo: list = field(default_factory=list)

    def __init__(self, name: str, context: list[str], context_lines: int, tokens: Collection[Token],
                 special_tokens: Collection[Token], instructions: Collection[Instruction]):
        """Initializes the Template with a name and context."""
        self._name: str = name
        self._context: list[str] = context
        self._tokens: dict[str, dict] = {}
        self._special_token_keys: set[str] = set()
        self._instruction_token_keys: set[str] = set()
        self._instruction: ProtocolFile.ProtocolInstruction = ProtocolFile.ProtocolInstruction(
            context_lines=context_lines)
        self._guardrails: dict[str, list[str] | str] = {'None': ''}
        self._numbers: dict[str, str] = {'None': ''}
        self._batches: ProtocolFile.Batches = ProtocolFile.Batches()

        # Add regular tokens
        self.add_tokens(tokens)

        # Add special tokens
        self.add_tokens(special_tokens)

        # Add instructions
        self.add_instructions(instructions)

    def add_tokens(self, tokens: Collection[Token]):
        """Adds tokens to the template."""
        for token in tokens:
            token_dict: dict[str, dict] = token.to_dict()
            token_dict.pop("value")
            self._tokens[token.value] = token_dict

            # Add numbers to the numbers dictionary
            if isinstance(token, NumToken):
                self._numbers[token.value] = token.protocol_representation

            # Add special tokens to the special tokens set
            if isinstance(token, SpecialToken):
                self._special_token_keys.add(token.key)

    def add_instructions(self, instructions: Collection[Instruction]):
        """Adds instructions to the template."""
        for instruction in instructions:
            instruction_set: ProtocolFile.ProtocolInstructionSet = ProtocolFile.ProtocolInstructionSet(
                set=instruction.serialize_memory_set(),
                result=instruction.final.value,
                samples=instruction.serialize_samples(),
                ppo=instruction.serialize_ppo(),
            )
            self._instruction.sets.append(instruction_set)

            # Add guardrails from the instruction's TokenSets
            self._add_guardrails(instruction.get_token_sets())

            # Add instruction token keys
            for token_set in instruction.get_token_sets():
                self._add_instruction_token_key(token_set.get_token_key_set())

            # Add the result token as a special token
            if instruction.final.key is not None:
                self._add_instruction_token_key(instruction.final.key)

    def _add_instruction_token_key(self, key: str):
        """Adds an instruction token key to the template."""
        self._instruction_token_keys.add(key)

    def _add_guardrails(self, token_sets: Collection[TokenSet]):
        """Adds guardrails from TokenSets to the template."""
        for token_set in token_sets:
            if token_set.guardrail is None:
                continue
            guardrail: Guardrail = token_set.guardrail
            self._guardrails[token_set.key] = guardrail.format_samples()

    @classmethod
    def _rename_protocol_elements(cls, template: dict):
        """
        Renames elements in the template to match the previous output format for backwards compatibility.
        :param template: The original template dictionary.
        :return: The modified template dictionary with renamed elements.
        """
        # Rename Token 'key' to 'emoji'
        for token_value, token_info in template.get('common/tokens', {}).items():
            if 'key' in token_info:
                token_info['emoji'] = token_info.pop('key')

        # Rename sample number to None if an array of empty arrays
        for instruction in template.get('instruction', {}).get('sets', []):
            for sample in instruction['samples']:
                if all(num == [] for num in sample['number']):
                    sample['number'] = None

        return template

    def _get_special_token_keys(self):
        """
        Returns a sorted list of tokens that should be under 'special_tokens' in the JSON.

        :return: A sorted list of special token keys.
        """
        return sorted(self._special_token_keys | self._instruction_token_keys)

    def to_json(self):
        """Converts the template to a JSON-compatible dictionary."""
        json_dict = {
            "name": self._name,
            "context": self._context,
            "tokens": dict(sorted(self._tokens.items())),
            "special_tokens": self._get_special_token_keys(),
            "instruction": {
                "memory": self._instruction.context_lines,
                "sets": [vars(s) for s in self._instruction.sets],
            },
            "guardrails": self._guardrails,
            "numbers": self._numbers,
            "batches": {
                "pretrain": self._batches.pretrain,
                "instruct": self._batches.instruct,
                "judge": self._batches.judge,
                "ppo": self._batches.ppo,
            },
        }

        return self._rename_protocol_elements(json_dict)
