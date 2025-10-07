from model_train_protocol import UserToken, NumToken, NumListToken, Token, TokenSet
from model_train_protocol.common.pydantic.protocol import TokenInfoModel


def add_token_attributes(prototype_model_json: dict,
                         token_subsets=None) -> dict:
    """
    Adds 'value' and 'special' attributes to each token in the specified subsets of tokens within the protocol JSON.

    :param prototype_model_json: The protocol JSON dictionary containing instruction sets and tokens.
    :param token_subsets: A list of token subset names to process (default is ["prompt_tokens", "response_tokens"]).
    :return: The modified protocol JSON dictionary with added attributes.
    """
    if token_subsets is None:
        token_subsets = ["prompt_tokens", "response_tokens"]

    for i, instruction in enumerate(prototype_model_json["instruction_sets"]):
        for token_subset in token_subsets:
            for j, token in enumerate(instruction[token_subset]):
                prototype_model_json['instruction_sets'][i][token_subset][j]["value"] = \
                    prototype_model_json['instruction_sets'][i][token_subset][j]["key"]
                prototype_model_json['instruction_sets'][i][token_subset][j]["special"] = None

    return prototype_model_json


def convert_str_to_camel_case(snake_str: str) -> str:
    """
    Converts a snake_case string to camelCase.

    :param snake_str: The input string in snake_case format.
    :return: The converted string in camelCase format.
    """
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def token_class_map(token_info_model: TokenInfoModel) -> type[Token]:
    """Maps a token info model to its corresponding class."""
    if token_info_model.user:
        return UserToken
    elif token_info_model.num > 0:
        return NumToken
    elif len(token_info_model.num_list) > 0:
        return NumListToken
    else:
        return Token


def create_token_set_from_token_model_array(token_info_models: list[TokenInfoModel]) -> TokenSet:
    """Creates a TokenSet from an array of token info models."""
    prompt_tokens: list[Token] = []
    for token in token_info_models:
        prompt_tokens.append(
            (token_class_map(token)(**token.model_dump())))  # Add token by token type to prompt token set
    return TokenSet(tokens=prompt_tokens)
