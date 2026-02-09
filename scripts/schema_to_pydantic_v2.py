"""
Generate Pydantic v2 models from the bloom JSON schema.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import model_train_protocol as mtp
from datamodel_code_generator import InputFileType, generate


def _get_schema_path(base_path: Optional[str]) -> Path:
    """Build the path to the versioned bloom schema file."""
    base = Path(base_path) if base_path is not None else Path(__file__).resolve().parents[1]
    version_semantic = mtp.utils.get_version()
    version_underscored = version_semantic.replace(".", "_")
    return base / "schemas" / f"v{version_semantic[0]}" / f"bloom_{version_underscored}.json"


def _get_output_path() -> Path:
    """Return the path for the generated Pydantic models module."""
    return Path(__file__).resolve().parent / "pydantic_models.py"


def _run_codegen(schema_path: Path, output_path: Path) -> None:
    """Run datamodel-code-generator to produce Pydantic v2 models."""
    generate(
        input_=schema_path,
        input_file_type=InputFileType.JsonSchema,
        output=output_path,
        output_model_type="pydantic_v2.BaseModel",
    )


def generate_pydantic_models(base_path: Optional[str] = None) -> Path:
    """Generate Pydantic v2 models from the bloom schema."""
    schema_path = _get_schema_path(base_path)
    output_path = _get_output_path()
    _run_codegen(schema_path, output_path)
    return output_path


if __name__ == "__main__":
    output = generate_pydantic_models()
    print(f"Generated Pydantic models at: {output}")

