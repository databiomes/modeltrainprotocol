from model_train_protocol._internal.ProtocolFile import ProtocolFile
from model_train_protocol.common.pydantic.prototyping import GenerateMTPPrototypeModel
from .utils import token_class_map, create_token_set_from_token_model_array
from ... import Protocol, Instruction, Token, TokenSet


def translate_prototype(prototype_mtp: GenerateMTPPrototypeModel, name: str | None = None,
                        encrypt: bool = False) -> ProtocolFile:
    """
    Translates a generated mtp prototype into a ProtocolFile

    :param prototype_mtp: The generated mtp prototype from the OpenAI API
    :param name: The name of the protocol file, otherwise uses model generated name
    :param encrypt: Whether to encrypt the protocol file
    """
    protocol: Protocol = Protocol(name=name if name else prototype_mtp.model_name,
                                  instruction_context_snippets=3, encrypt=encrypt)

    for context_item in prototype_mtp.context:
        protocol.add_context(context_item.context)

    context_token: Token = Token("Context")
    for instruction_set in prototype_mtp.instruction_sets:

        prompt_token_set: TokenSet = create_token_set_from_token_model_array(instruction_set.prompt_tokens)
        response_token_set: TokenSet = create_token_set_from_token_model_array(instruction_set.response_tokens)

        simple_instruction: Instruction = Instruction(
            response=instruction_set.response
        )
