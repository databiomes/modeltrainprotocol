import tomllib
from importlib import metadata
from pathlib import Path
from typing import Optional


def _find_pyproject_path(current_path: Path) -> Optional[Path]:
    for parent in current_path.parents:
        check_path = parent / "pyproject.toml"
        if check_path.exists():
            return check_path
    return None


def get_mtp_version() -> str:
    """
    Return the installed package version when available.
    Falls back to the local pyproject.toml for editable/dev usage.
    """
    try:
        return metadata.version("model-train-protocol")
    except metadata.PackageNotFoundError:
        pass

    current_path: Path = Path(__file__).resolve()
    pyproject_path: Optional[Path] = _find_pyproject_path(current_path)
    if pyproject_path is None:
        raise FileNotFoundError(
            "Could not find installed package metadata or pyproject.toml in any parent directories."
        )

    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)

    return str(pyproject["project"]["version"])


def get_schema_version() -> str:
    """
    Gets the schema version from the local pyproject.toml for editable/dev usage.
    """
    current_path: Path = Path(__file__).resolve()
    pyproject_path: Optional[Path] = _find_pyproject_path(current_path)
    if pyproject_path is None:
        raise FileNotFoundError(
            "Could not find pyproject.toml in any parent directories."
        )

    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)

    return str(pyproject["tool"]["model-train-protocol"]["schema-version"])


def get_bloom_schema_url():
    """
    Retrieves the schema URL for the current version of the Model Train Protocol.
    """
    version_semantic: str = get_schema_version()
    schema_url = f"https://mtp.schemas.databiomes.com/v{version_semantic[0]}/bloom_{version_semantic.replace('.', '_')}.json"
    return schema_url

def get_template_schema_url():
    """
    Retrieves the schema URL for the current version of the MTP Template.
    """
    version_semantic: str = get_schema_version()
    schema_url = f"https://mtp.schemas.databiomes.com/v{version_semantic[0]}/template_{version_semantic.replace('.', '_')}.json"
    return schema_url
