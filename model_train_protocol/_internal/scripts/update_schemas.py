"""
This script updates the JSON schema files used for validating model training configurations.
"""
import json
from pathlib import Path
from typing import Optional

from model_train_protocol.common.prototyping.utils import get_version
from model_train_protocol.common.pydantic.protocol import ProtocolModel


def save_protocol_schema(base_path: Optional[str] = None) -> str:
    """
    Generates and saves the JSON Schema for the Model Train Protocol to schemas/{version}/bloom.json.

    This schema can be used by other languages (Go, JavaScript, etc.) to validate
    and understand the structure of the protocol JSON files.

    :param base_path: Base path for the schemas directory. If None, uses the project root.
    :return: The path to the saved schema file.
    """
    # Generate JSON Schema from the Pydantic model
    schema = ProtocolModel.model_json_schema(
        mode='serialization',
        by_alias=True
    )

    # Add metadata to the schema
    schema['$schema'] = 'https://json-schema.org/draft/2020-12/schema'
    schema['title'] = 'Model Train Protocol Schema'
    schema['description'] = 'JSON Schema for Model Train Protocol (MTP) model files'

    # Get version
    version = get_version()

    # Determine base path
    if base_path is None:
        # Find project root by looking for pyproject.toml
        current_path = Path(__file__).resolve()
        project_root = None
        for parent in current_path.parents:
            if (parent / "pyproject.toml").exists():
                project_root = parent
                break

        if project_root is None:
            raise FileNotFoundError("Could not find project root (pyproject.toml) in any parent directories.")

        base_path = str(project_root)

    # Create schemas/{version}/ directory
    schema_dir = Path(base_path) / "schemas" / version
    schema_dir.mkdir(parents=True, exist_ok=True)

    # Save schema to schemas/{version}/bloom.json
    schema_path = schema_dir / "bloom.json"
    with open(schema_path, 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)

    return str(schema_path)


if __name__ == "__main__":
    save_protocol_schema()
