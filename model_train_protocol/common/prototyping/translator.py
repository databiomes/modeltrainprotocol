from model_train_protocol._internal.ProtocolFile import ProtocolFile
from model_train_protocol.common.pydantic.prototyping import MTPPrototypeModel
from .utils import create_token_set_from_token_model_array
from ... import Protocol, SimpleInstruction, Token, TokenSet, Snippet


def translate_prototype(prototype_mtp: MTPPrototypeModel, name: str | None = None,
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

    context_token: Token = Token("Context", desc="Context for the model by the model creator.")
    context_tokenset: TokenSet = TokenSet(context_token)
    for instruction_set in prototype_mtp.instruction_sets:
        prompt_token_set: TokenSet = create_token_set_from_token_model_array(instruction_set.prompt_tokens)
        response_token_set: TokenSet = create_token_set_from_token_model_array(instruction_set.response_tokens)
        final: Token = Token(**prototype_mtp.final_token.model_dump())

        simple_instruction: SimpleInstruction = SimpleInstruction(
            context=[context_tokenset, prompt_token_set], response=response_token_set, final=final
        )

        for sample in instruction_set.samples:
            context_snippets: list[Snippet] = [
                context_tokenset.create_snippet(
                    sample.prompt_context
                ), prompt_token_set.create_snippet(
                    sample.prompt_sample
                )
            ]
            simple_instruction.add_sample(
                context_snippets=context_snippets,
                output_snippet=response_token_set.create_snippet(
                    sample.response_sample
                )
            )

            protocol.add_instruction(simple_instruction)

    return protocol.get_protocol_file()
