from model_train_protocol import Protocol
from model_train_protocol.common.prototyping.providers.openai import generate_mtp_prototype_file
from model_train_protocol.common.prototyping.translator import translate_prototype
from model_train_protocol.common.pydantic.prototyping import MTPPrototypeModel


def generate_prototype_protocol(prompt_id: str, openai_api_key: str | None = None,
                                file_path: str | None = None,
                                name: str | None = None, encrypt: bool = False):
    """
    Generates a protocol file prototype based on a given prompt ID using OpenAI's API.

    Saves the generated protocol file to be submitted to Databiomes for model generation.

    :param prompt_id: The prompt id of your prompt in OpenAI. Like pmpt_68e5....9a72.
    :param openai_api_key: Your OpenAI API key. If None, it will attempt to load "OPENAI_API_KEY" from environment variables.
    :param file_path: The file path to save the generated protocol file. If None, file will be saved in current directory with model name.
    :param name: The name of the protocol file, otherwise uses model generated name
    :param encrypt: Whether to encrypt the protocol file
    :return: The generated ProtocolFile instance.
    """
    prototype: MTPPrototypeModel = generate_mtp_prototype_file(prompt_id=prompt_id, openai_api_key=openai_api_key)
    protocol: Protocol = translate_prototype(prototype_mtp=prototype, name=name, encrypt=encrypt)
    protocol.save(name=name, path=file_path)
