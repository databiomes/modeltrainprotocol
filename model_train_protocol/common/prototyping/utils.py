import tomllib
from pathlib import Path

from model_train_protocol import Token, TokenSet
from model_train_protocol.common.pydantic.prototyping import TokenInfoPrototypeModel


def clean_token_key(key: str) -> str:
    """Removes non-alphanumeric characters from a token key."""
    return ''.join(char for char in key if char.isalnum() or char == '_')


def convert_str_to_camel_case(snake_str: str) -> str:
    """
    Converts a snake_case string to camelCase.

    :param snake_str: The input string in snake_case format.
    :return: The converted string in camelCase format.
    """
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def get_version():
    # Start from this file: .../model_train_protocol/common/prototyping/utils.py
    current_path = Path(__file__).resolve()

    # Search upwards until we find pyproject.toml
    pyproject_path = None
    for parent in current_path.parents:
        check_path = parent / "pyproject.toml"
        if check_path.exists():
            pyproject_path = check_path
            break

    if pyproject_path is None:
        raise FileNotFoundError("Could not find pyproject.toml in any parent directories.")

    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)

    return str(pyproject["project"]["version"])


def token_class_map(token_info_model: TokenInfoPrototypeModel) -> type[Token]:
    """Maps a token info model to its corresponding class."""
    # if token_info_model.num > 0:
    #     return NumToken
    # elif len(token_info_model.num_list) > 0:
    #     return NumListToken
    # else:
    #     return Token
    return Token


def create_sanitized_token_from_model(token_info_model: TokenInfoPrototypeModel) -> Token:
    """Creates a cleaned Token from a token info model."""
    token_info: dict = token_info_model.model_dump()
    token_info['value'] = clean_token_key(token_info['value'])
    token_info['value'] = convert_str_to_camel_case(token_info['value'])
    return token_class_map(token_info_model)(**token_info)


def create_token_set_from_token_model_array(token_info_models: list[TokenInfoPrototypeModel]) -> TokenSet:
    """Creates a TokenSet from an array of token info models."""
    tokens: dict[Token, None] = {}  # Using dict as an ordered set to avoid third party dependencies
    for token_info_model in token_info_models:
        token: Token = create_sanitized_token_from_model(token_info_model)
        tokens[token] = None
    return TokenSet(tokens=list(tokens.keys()))
