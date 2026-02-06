"""
This script updates the JSON schema files used for validating model training configurations.
"""
import json
from pathlib import Path
from typing import Optional

from model_train_protocol.common.prototyping.utils import get_version
from model_train_protocol.common.pydantic.protocol import ProtocolModel
from model_train_protocol.common.pydantic.template import TemplateModel


def save_protocol_schema(base_path: Optional[str] = None) -> str:
    """
    Generates and saves the JSON Schema for the Model Train Protocol to
    model_train_protocol/schemas/{version}/bloom_schema.json.

    This schema can be used by other languages (Go, JavaScript, etc.) to validate
    and understand the structure of the protocol JSON files.

    :param base_path: Base path for the schemas directory. If None, uses the package root.
    :return: The path to the saved schema file.
    """
    # Generate JSON Schema from the Pydantic model
    schema = ProtocolModel.model_json_schema(
        mode='serialization',
        by_alias=True
    )

    # Get version
    version = get_version()

    # Determine base path
    if base_path is None:
        package_root = Path(__file__).resolve().parents[2]
        base_path = str(package_root)

    # Create model_train_protocol/schemas/{version}/ directory
    schema_dir = Path(base_path) / "schemas" / version
    schema_dir.mkdir(parents=True, exist_ok=True)

    # Build the final schema with metadata at the top level
    # Ensure $schema is first, then other metadata, then the rest
    final_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Model Train Protocol Schema",
        "description": "JSON Schema for Model Train Protocol (MTP) model files",
        **schema  # Merge the generated schema
    }

    # Save schema to schemas/{version}/bloom_schema.json
    schema_path = schema_dir / "bloom_schema.json"
    with open(schema_path, 'w', encoding='utf-8') as f:
        json.dump(final_schema, f, indent=2, ensure_ascii=False)

    return str(schema_path)


def save_template_schema(base_path: Optional[str] = None) -> str:
    """
    Generates and saves the JSON Schema for the Model Train Protocol Template to
    model_train_protocol/schemas/{version}/template_schema.json.

    This schema can be used by other languages (Go, JavaScript, etc.) to validate
    and understand the structure of the template JSON files.

    :param base_path: Base path for the schemas directory. If None, uses the package root.
    :return: The path to the saved schema file.
    """
    # Generate JSON Schema from the Pydantic model
    schema = TemplateModel.model_json_schema(
        mode='serialization',
        by_alias=True
    )

    # Get version
    version = get_version()

    # Determine base path
    if base_path is None:
        package_root = Path(__file__).resolve().parents[2]
        base_path = str(package_root)

    # Create model_train_protocol/schemas/{version}/ directory
    schema_dir = Path(base_path) / "schemas" / version
    schema_dir.mkdir(parents=True, exist_ok=True)

    # Build the final schema with metadata at the top level
    # Ensure $schema is first, then other metadata, then the rest
    final_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Model Train Protocol Template Schema",
        "description": "JSON Schema for Model Train Protocol (MTP) template files",
        **schema  # Merge the generated schema
    }

    # Save schema to schemas/{version}/template_schema.json
    schema_path = schema_dir / "template_schema.json"
    with open(schema_path, 'w', encoding='utf-8') as f:
        json.dump(final_schema, f, indent=2, ensure_ascii=False)

    return str(schema_path)


if __name__ == "__main__":
    print("Generating protocol schema...")
    protocol_path = save_protocol_schema()
    print(f"Protocol schema saved to: {protocol_path}")
    
    print("\nGenerating template schema...")
    template_path = save_template_schema()
    print(f"Template schema saved to: {template_path}")
    
    print("\nSchema generation complete!")
