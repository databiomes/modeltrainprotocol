def assert_special_tokens_in_tokens(json_output: dict, special_tokens: list):
    """Assert that all special tokens in the protocol JSON are also present in the tokens dictionary."""
    tokens = json_output["tokens"]
    all_token_keys: set[str] = set([token["emoji"] for token in tokens.values()])
    for token in special_tokens:
        if '_' in token:
            for token_subset in token.split("_")[:-1]:  # Exclude the trailing empty string after last '_'
                assert token_subset + '_' in all_token_keys, f"Special token {token} not found in tokens dictionary"
        else:
            assert token in all_token_keys, f"Special token {token} not found in tokens dictionary"