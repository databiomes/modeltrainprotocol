import tomllib
from pathlib import Path


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


def get_schema_url():
    """
    Retrieves the schema URL for the current version of the Model Train Protocol.
    """
    # Add conventional schema tag to JSON for validation purposes
    version_semantic: str = get_version()
    schema_url = f"https://mtp.schemas.databiomes.com/v{version_semantic[0]}/bloom_{version_semantic.replace('.', '_')}.json"
    return schema_url
