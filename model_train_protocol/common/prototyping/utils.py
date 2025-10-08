from model_train_protocol import NumToken, NumListToken, Token, TokenSet
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


def token_class_map(token_info_model: TokenInfoPrototypeModel) -> type[Token]:
    """Maps a token info model to its corresponding class."""
    if token_info_model.num > 0:
        return NumToken
    elif len(token_info_model.num_list) > 0:
        return NumListToken
    else:
        return Token

def create_cleaned_token_from_model(token_info_model: TokenInfoPrototypeModel) -> Token:
    """Creates a cleaned Token from a token info model."""
    token_info: dict = token_info_model.model_dump()
    token_info['value'] = clean_token_key(token_info['value'])
    token_info['value'] = convert_str_to_camel_case(token_info['value'])
    return token_class_map(token_info_model)(**token_info)

def create_token_set_from_token_model_array(token_info_models: list[TokenInfoPrototypeModel]) -> TokenSet:
    """Creates a TokenSet from an array of token info models."""
    tokens: list[Token] = []
    for token_info_model in token_info_models:
        token: Token = create_cleaned_token_from_model(token_info_model)
        tokens.append(token)
    return TokenSet(tokens=tokens)
