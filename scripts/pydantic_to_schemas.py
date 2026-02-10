"""
This script updates the JSON schema files used for validating model training configurations.
"""
import json
from pathlib import Path
from typing import Optional

from model_train_protocol.utils import get_version, get_bloom_schema_url
from model_train_protocol.common.pydantic.protocol import Protocol
from model_train_protocol.common.pydantic.template import Template


def _get_base_path(base_path: Optional[str]) -> Path:
    if base_path is None:
        return Path(__file__).resolve().parents[1]
    return Path(base_path)


def _save_schema(
    schema: dict,
    title: str,
    description: str,
    filename_pattern: str,
    base_path: Optional[str] = None,
) -> str:
    version_semantic: str = get_version()
    version_underscored: str = version_semantic.replace('.', '_')
    schema_dir = _get_base_path(base_path) / "schemas" / f"v{version_semantic[0]}"
    schema_dir.mkdir(parents=True, exist_ok=True)

    schema_path = schema_dir / filename_pattern.format(version=version_underscored)

    final_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": get_bloom_schema_url(),
        "title": title,
        "description": description,
        **schema,
    }
    with open(schema_path, 'w', encoding='utf-8') as f:
        json.dump(final_schema, f, indent=2, ensure_ascii=False)

    return str(schema_path)


def save_protocol_schema(base_path: Optional[str] = None) -> str:
    """
    Generates and saves the JSON Schema for the Model Train Protocol to
    schemas/v{major}/bloom_{version}.json.

    This schema can be used by other languages (Go, JavaScript, etc.) to validate
    and understand the structure of the protocol JSON files.

    :param base_path: Base path for the schemas directory. If None, uses the repo root.
    :return: The path to the saved schema file.
    """
    schema = Protocol.model_json_schema(
        mode='serialization',
        by_alias=True
    )

    return _save_schema(
        schema=schema,
        title="Model Train Protocol Schema",
        description="JSON Schema for Model Train Protocol (MTP) model files",
        filename_pattern="bloom_{version}.json",
        base_path=base_path,
    )


def save_template_schema(base_path: Optional[str] = None) -> str:
    """
    Generates and saves the JSON Schema for the Model Train Protocol Template to
    schemas/v{major}/template_{version}.json.

    This schema can be used by other languages (Go, JavaScript, etc.) to validate
    and understand the structure of the template JSON files.

    :param base_path: Base path for the schemas directory. If None, uses the repo root.
    :return: The path to the saved schema file.
    """
    schema = Template.model_json_schema(
        mode='serialization',
        by_alias=True
    )

    return _save_schema(
        schema=schema,
        title="Model Train Protocol Template Schema",
        description="JSON Schema for Model Train Protocol (MTP) template files",
        filename_pattern="template_{version}.json",
        base_path=base_path,
    )


if __name__ == "__main__":
    print("Generating protocol schema...")
    protocol_path = save_protocol_schema()
    print(f"Protocol schema saved to: {protocol_path}")

    print("\nGenerating template schema...")
    template_path = save_template_schema()
    print(f"Template schema saved to: {template_path}")

    print("\nSchema generation complete!")
