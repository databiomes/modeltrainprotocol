import tomllib
from pathlib import Path
import emoji


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


def validate_string_subset(string_set: set[str]):
    """
    Checks if any string in a set is a perfect substring of another.

    :param string_set: A set of strings.
    :raises ValueError: If any string is a perfect substring of another (case insensitive).
    """
    # Sort the list by length, longest to shortest.
    sorted_strings = sorted(list(string_set), key=len, reverse=False)

    # Iterate through the strings and check for perfect subsets.
    for i in range(len(sorted_strings)):
        for j in range(i + 1, len(sorted_strings)):
            # If a shorter string is a perfect substring of a longer one, return False.

            # Only keep alphanumeric characters for comparison
            first_string: str = ''.join(c.lower() for c in sorted_strings[i] if c.isalnum() or emoji.purely_emoji(c))
            second_string: str = ''.join(c.lower() for c in sorted_strings[j] if c.isalnum() or emoji.purely_emoji(c))

            if first_string in second_string:
                raise ValueError(
                    f"'{sorted_strings[i]}' is a substring of '{sorted_strings[j]}' (alphanumeric characters only, case insensitive).")

