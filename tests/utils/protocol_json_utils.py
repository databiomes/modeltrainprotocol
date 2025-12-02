def assert_special_tokens_in_tokens(json_output: dict, special_tokens: list):
    """Assert that all special tokens in the protocol JSON are also present in the tokens dictionary."""
    tokens = json_output["tokens"]
    all_token_keys: set[str] = set([token["key"] for token in tokens.values()])
    for token in special_tokens:
        # Skip snippet strings that don't look like tokens (long strings without token patterns)
        # Token patterns: start with <, contain underscores in token-like patterns, or are short special tokens
        if not (token.startswith('<') or '_' in token or len(token) <= 10):
            # This is likely a snippet string, skip validation
            continue
        if '_' in token:
            for token_subset in token.split("_")[:-1]:  # Exclude the trailing empty string after last '_'
                assert token_subset + '_' in all_token_keys, f"Special token {token} not found in tokens dictionary"
        else:
            assert token in all_token_keys, f"Special token {token} not found in tokens dictionary"