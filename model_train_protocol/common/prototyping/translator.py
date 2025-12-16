from typing import List, Optional

from model_train_protocol.common.pydantic.prototyping import MTPPrototypeModel
from ... import Protocol, Instruction, Token, TokenSet, Snippet


def translate_prototype(prototype_mtp: MTPPrototypeModel, name: Optional[str] = None,
                        encrypt: bool = False) -> Protocol:
    """
    Translates a generated mtp prototype into a ProtocolFile

    :param prototype_mtp: The generated mtp prototype from the OpenAI API
    :param name: The name of the protocol file, otherwise uses model generated name
    :param encrypt: Whether to encrypt the protocol file
    """
    protocol: Protocol = Protocol(name=name if name else prototype_mtp.model_name,
                                  context_snippets=2, encrypt=encrypt)

    for context_item in prototype_mtp.context:
        protocol.add_context(context_item.context)

    context_token: Token = Token("Context", desc="Context for the model.")
    context_tokenset: TokenSet = TokenSet(context_token)

    prompt_token: Token = Token("Prompt", desc="The prompt to the model.")
    prompt_tokenset: TokenSet = TokenSet(prompt_token)

    response_token: Token = Token("Response", desc="The response from the model.")
    response_tokenset: TokenSet = TokenSet(response_token)

    final: FinalToken = Token("Final", desc="Indicates the end of the model's response.")

    for instruction_set in prototype_mtp.instruction_sets:

        # Creates tokens dynamically from prototype (needs to account for duplicates still)
        # prompt_tokenset: TokenSet = create_token_set_from_token_model_array(instruction_set.prompt_tokens)
        # response_tokenset: TokenSet = create_token_set_from_token_model_array(instruction_set.response_tokens)
        # final: FinalToken = create_sanitized_token_from_model(prototype_mtp.final_token)

        simple_instruction: Instruction = Instruction(
            input=[context_tokenset, prompt_tokenset], output=response_tokenset, final=final
        )

        for sample in instruction_set.samples:
            context_snippets: List[Snippet] = [
                context_tokenset.create_snippet(
                    sample.prompt_context
                ), prompt_tokenset.create_snippet(
                    sample.prompt_sample
                )
            ]
            simple_instruction.add_sample(
                input_snippets=context_snippets,
                output_snippet=response_tokenset.create_snippet(
                    sample.response_sample
                )
            )

        protocol.add_instruction(simple_instruction)

    return protocol
