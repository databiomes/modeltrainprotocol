import json
import os
from typing import List, Optional, Set, Dict

from . import Token, FinalToken, Guardrail, Instruction, InstructionInput, InstructionOutput, Snippet
from ._internal.ProtocolFile import ProtocolFile
from ._internal.TemplateFile import TemplateFile
from .common.constants import BOS_TOKEN, EOS_TOKEN, RUN_TOKEN, PAD_TOKEN, UNK_TOKEN, NON_TOKEN, \
    MINIMUM_TOTAL_CONTEXT_LINES, PER_FINAL_TOKEN_SAMPLE_MINIMUM, TokenTypeEnum, \
    MAXIMUM_CHARACTERS_PER_MODEL_CONTEXT_LINE
from .common.instructions.BaseInstruction import BaseInstruction, Sample
from .common.tokens import TokenSet
from .common.tokens.SpecialToken import SpecialToken
from .common.utils import validate_string_subset, hash_string
from .errors import ProtocolError, ProtocolTypeError


class Protocol:
    """Model Train Protocol (MTP) class for creating the training configuration."""

    def __init__(self, name: str, inputs: int, encrypt: bool = True):
        """
        Initialize the Model Train Protocol (MTP)

        :param name: The name of the protocol.
        :param inputs: The number of lines in each Instruction input. Must be at least 2.
        :param encrypt: Whether to encrypt Tokens with unspecified with hashed keys. Default is True.
        """
        self.name: str = name
        self.input_count: int = inputs  # Number of lines in instruction samples
        self.encrypt: bool = encrypt
        if self.input_count < 1:
            raise ProtocolError("A minimum of 1 inputs is required for all instructions.")
        self.context: List[str] = []
        self.tokens: Set[Token] = set()
        self.instructions: Set[BaseInstruction] = set()
        self.guardrails: Dict[str, List[str]] = dict()
        self.numbers: Dict[str, str] = dict()
        self.special_tokens: Set[Token] = set()
        self.used_keys: Set[str] = set()
        self.has_guardrails: bool = False

    @classmethod
    def from_json(cls, protocol_file: dict) -> 'Protocol':
        """
        Loads a Protocol from a JSON representation.

        Does NOT require a protocol to be valid.
        :param protocol_file: The JSON representation of the Protocol.
        :return: A Protocol instance.
        """
        name: str = protocol_file["name"]
        inputs: int = protocol_file["inputs"]
        encrypt: bool = protocol_file["encrypted"]
        protocol = Protocol(name=name, inputs=inputs, encrypt=encrypt)
        protocol.context = protocol_file["context"]

        tokens: dict[str, Token] = {}

        # Add tokens
        for token_value, token_info in protocol_file["tokens"].items():
            token_value = token_value[:-1] if token_value[-1] == "_" else token_value
            token_class: type[Token] = TokenTypeEnum[token_info["type"]]
            token: Token = token_class(value=token_value, **token_info)
            protocol._add_token(token)
            tokens[token.value] = token

        # Add instructions
        instruction_info = protocol_file["instruction"]
        for instruction in instruction_info["sets"]:
            context: List[str] = instruction["context"]
            tokensets: List[TokenSet] = []
            final_tokens: List[FinalToken] = []
            for token_set in instruction["set"]:
                tokensets.append(TokenSet([tokens[token_value] for token_value in token_set]))

            samples: List[Sample] = []
            for sample in instruction["samples"]:
                input_lines: List[str] = sample["strings"][:-1]
                output_line: str = sample["strings"][-1]
                result_token: FinalToken = tokens[sample["result"]]  # type: ignore
                final_tokens.append(result_token)
                samples.append(Sample(input=input_lines, output=output_line, prompt=None, numbers=sample["numbers"],
                                      number_lists=sample["number_lists"], result=result_token, value=sample["value"]))

            instr_input: InstructionInput = InstructionInput(
                tokensets=tokensets[:-1],
            )

            instr_output: InstructionOutput = InstructionOutput(
                tokenset=tokensets[-1],
                final=final_tokens,
            )

            protocol_instruction: Instruction = Instruction(
                input=instr_input,
                output=instr_output,
                context=context
            )

            for sample in samples:
                inputs_snippets: List[Snippet] = []
                for i, sample_input in enumerate(sample.input):
                    inputs_snippets.append(
                        tokensets[i].create_snippet(string=sample_input, number_lists=sample.number_lists[i] if len(
                            sample.number_lists[i]) > 0 else None,
                                                    numbers=sample.numbers[i] if len(sample.numbers[i]) > 0 else None))

                outputs_snippet: Snippet = tokensets[-1].create_snippet(
                    string=sample.output,
                    number_lists=sample.number_lists[-1] if len(sample.number_lists[-1]) > 0 else None
                    , numbers=sample.numbers[-1] if len(sample.numbers[-1]) > 0 else None
                )

                final_token: FinalToken = sample.result

                protocol_instruction.add_sample(
                    input_snippets=inputs_snippets,
                    output_snippet=outputs_snippet,
                    output_value=sample.value,
                    final=final_token,
                )

            # Add guardrails
            for guardrail_set in instruction["guardrails"]:
                guardrail: Guardrail = Guardrail(
                    good_prompt=guardrail_set["good_prompt"],
                    bad_prompt=guardrail_set["bad_prompt"],
                    bad_output=guardrail_set["bad_output"]
                )

                for sample in guardrail_set["bad_examples"]:
                    guardrail.add_sample(sample)

                protocol_instruction.add_guardrail(guardrail=guardrail, tokenset_index=guardrail_set["index"])

            protocol.add_instruction(protocol_instruction)

        return protocol

    def add_context(self, context: str):
        """Adds a line of context to the model."""
        if not isinstance(context, str):
            raise ProtocolTypeError("Context must be a string.")

        self._validate_context_line_length(context)

        self.context.append(context)

    @classmethod
    def _validate_context_line_length(cls, line: str):
        """Validates that each context line does not exceed MAXIMUM_CHARACTERS_PER_MODEL_CONTEXT_LINE."""
        if len(line) > MAXIMUM_CHARACTERS_PER_MODEL_CONTEXT_LINE:
            raise ProtocolError(
                f"Context line exceeds maximum length of {MAXIMUM_CHARACTERS_PER_MODEL_CONTEXT_LINE} characters.\n"
                f"Line: '{line}' has {len(line)} characters."
            )

    def add_instruction(self, instruction: BaseInstruction):
        """
        Adds an Instruction (and its components) to the protocol.

        Asserts that all samples in the instruction match the defined sample line size.
        """
        if instruction in self.instructions:
            raise ProtocolError(
                "Instruction already added to the protocol (or instruction with identical tokensets in the same order).")

        for existing_instruction in self.instructions:
            if existing_instruction.name == instruction.name:
                raise ProtocolError(f"An instruction with name '{instruction.name}' already exists in the protocol.")

        if len(instruction.samples) < 3:
            raise ProtocolError(
                f"Instruction must have at least three samples. Found {len(instruction.samples)} samples."
            )

        final_sample_table: dict[FinalToken, int] = dict()

        # Assert all samples match the defined sample line size
        for sample in instruction.samples:
            if not len(sample.input) == self.input_count:
                raise ProtocolError(
                    f"Sample input lines ({len(sample.input)}) does not match defined inputs count ({self.input_count})"
                    f"\n{sample}."
                )
            if sample.result not in final_sample_table:
                final_sample_table[sample.result] = 1
            else:
                final_sample_table[sample.result] += 1

        # Ensure each FinalToken has at least 3 samples
        for final_token, count in final_sample_table.items():
            if count < PER_FINAL_TOKEN_SAMPLE_MINIMUM:
                raise ProtocolError(
                    f"Missing minimum {PER_FINAL_TOKEN_SAMPLE_MINIMUM} samples for each FinalToken in the Output of Instruction {instruction.name}.\n"
                    f"FinalToken '{final_token.value}' must have at least 3 samples in the instruction. Found {count} samples."
                )

        # Add all tokens
        for token in instruction.get_tokens():
            self._assign_key(token=token)
            if token not in self.tokens:
                self._add_token(token)

        # Add the instruction to the protocol
        self.instructions.add(instruction)

        # Update guardrails flag
        if instruction.has_guardrails:
            self.has_guardrails = True

    def get_protocol_file(self, valid: bool) -> ProtocolFile:
        """
        Prepares and returns the ProtocolFile representation of the protocol.

        :return: The ProtocolFile instance representing the protocol.
        """
        return ProtocolFile(
            name=self.name, context=self.context, inputs=self.input_count, encrypted=self.encrypt,
            valid=valid,
            tokens=self.tokens, special_tokens=self.special_tokens, instructions=self.instructions,
        )

    def get_template_file(self) -> TemplateFile:
        """
        Prepares and returns the TemplateFile representation of the protocol.

        :return: The TemplateFile instance representing the protocol template.
        """
        return TemplateFile(
            instructions=list(self.instructions),
            inputs=self.input_count,
            encrypt=self.encrypt,
            has_guardrails=self.has_guardrails,
        )

    def save(self, name: Optional[str] = None, path: Optional[str] = None):
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
        filename = os.path.join(path, f"{name}_model.json")

        print(f"Saving Model Train Protocol to {filename}...")
        valid: bool
        error_msg: Optional[str]
        valid, error_msg = self.validate_protocol()
        if not valid:
            raise ProtocolError(error_msg)
        self._prep_protocol()

        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(self.get_protocol_file(valid=valid).to_json(), file, indent=4, ensure_ascii=False)

    def template(self, path: Optional[str] = None):
        """
        Create a template JSON file for the model training protocol.

        The template json file includes example usage and all possible combinations of model inputs and
        outputs based on the defined tokens and instructions.

        :param path: The directory path where the template file will be saved. If None, saves in the current directory.
        """
        if path is None:
            path = os.getcwd()
        filename = os.path.join(path, f"{self.name}_template.json")

        print(f"Saving Model Train Protocol Template to {filename}...")
        valid: bool
        error_msg: Optional[str]
        valid, error_msg = self.validate_protocol()
        if not valid:
            raise ProtocolError(error_msg)
        self._prep_protocol()

        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(self.get_template_file().to_json(), file, indent=4, ensure_ascii=False)

    def _assign_key(self, token: Token):
        """
        Assigns a key to a Token based on the protocol's encryption setting.

        :param token: The Token to assign the key of.
        """
        # If the user has assigned a key, use this key
        if token.key is not None:
            return

        if self.encrypt:
            # Generate a random key for the token if encrypting and no key is set
            token.key = hash_string(key=token.value, output_char=6)
        else:
            # Use the value as the key if not encrypting. I.e. Token 'Continue_' has key 'Continue_'
            token.key = token.value

    def _add_token(self, token: Token):
        """
        Adds a unique token to the protocol.

        Validates that the token's value and key are unique.
        :param token: The Token instance to add.
        """
        self._assign_key(token=token)

        if token in self.tokens:
            raise ProtocolError(f"Token value {token.value} already used. Duplicate tokens are not allowed.")

        if token.key in self.used_keys:
            raise ProtocolError(
                f"Duplicate token key '{token.key}' is already used in another token. Duplicate keys are not allowed.")

        self.tokens.add(token)
        self.used_keys.add(token.key)

        if isinstance(token, SpecialToken):
            self.special_tokens.add(token)

    def _add_default_special_tokens(self):
        """Adds all special tokens to the protocol."""
        self.special_tokens.add(BOS_TOKEN)
        self.special_tokens.add(EOS_TOKEN)
        self.special_tokens.add(RUN_TOKEN)
        self.special_tokens.add(PAD_TOKEN)
        self.special_tokens.add(NON_TOKEN)
        # Check if any instruction has guardrails
        if self.has_guardrails:
            self.special_tokens.add(UNK_TOKEN)

    def _validate_context_count(self):
        """Validates that the total context/background lines across all instructions is at least equal to MINIMUM_TOTAL_CONTEXT_LINES."""
        total_context_lines: int = len(self.context)
        for instruction in self.instructions:
            total_context_lines += len(instruction.context)

        if total_context_lines < MINIMUM_TOTAL_CONTEXT_LINES:
            raise ProtocolError(
                f"The total number of context lines across all instructions is {total_context_lines}, "
                f"which is less than the minimum required of {MINIMUM_TOTAL_CONTEXT_LINES}. Please add more context lines using protocol.add_context() "
                f"or by adding background lines to instructions."
            )

    def _prep_protocol(self):
        """
        Sets all elements in the protocol before serialization.

        Raises errors if any validation checks fail.

        Setups up all necessary components in the protocol before saving or templating.

        This includes setting guardrails from their TokenSets and creating default special tokens.
        """
        self._add_default_special_tokens()

    def validate_protocol(self) -> tuple[bool, Optional[str]]:
        """
        Validates that the protocol meets all requirements for training.
        :return: Tuple of (True if valid, error message if invalid)
        """
        try:
            if len(self.instructions) == 0:
                raise ProtocolError(
                    "No instructions have been added to Protocol. Call protocol.add_instruction() to add instructions.")

            self._validate_context_count()
            for line in self.context:
                self._validate_context_line_length(line)

            used_values: Set[str] = {token.value for token in self.tokens}
            validate_string_subset(used_values)
            validate_string_subset(self.used_keys)

            for instruction in self.instructions:
                instruction.validate_instruction()
                for guardrail in instruction.get_guardrails():
                    guardrail.validate_guardrail()

        except Exception as e:
            error_msg = str(e)
            print(f"Protocol invalid: {error_msg}")
            return False, error_msg

        return True, None
