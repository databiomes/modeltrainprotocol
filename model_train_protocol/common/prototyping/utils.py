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
