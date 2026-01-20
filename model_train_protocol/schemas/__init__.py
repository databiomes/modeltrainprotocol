"""Packaged JSON schemas for Model Train Protocol."""

from importlib import resources
from importlib.resources.abc import Traversable
import json
from typing import Any

SCHEMA_PROTOCOL: str = "bloom_schema.json"
SCHEMA_TEMPLATE: str = "template_schema.json"


def list_schema_versions() -> list[str]:
    """Return available schema versions bundled with the package."""
    base = resources.files(__package__)
    return sorted([entry.name for entry in base.iterdir() if entry.is_dir()])


def get_schema_resource(version: str, name: str) -> Traversable:
    """Return a schema resource for the given version and filename."""
    resource = resources.files(__package__) / version / name
    if not resource.is_file():
        raise FileNotFoundError(f"Schema not found: {version}/{name}")
    return resource


def read_schema_text(version: str, name: str) -> str:
    """Read a schema as raw JSON text."""
    resource = get_schema_resource(version=version, name=name)
    return resource.read_text(encoding="utf-8")


def load_schema(version: str, name: str) -> dict[str, Any]:
    """Load a schema as a JSON object."""
    resource = get_schema_resource(version=version, name=name)
    with resource.open("r", encoding="utf-8") as handle:
        return json.load(handle)

