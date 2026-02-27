"""
Generate Pydantic v2 models from the bloom JSON schema.
"""
from __future__ import annotations

import tempfile
from pathlib import Path
from urllib.request import urlopen

from datamodel_code_generator import InputFileType, generate

import utils


def _get_output_path() -> Path:
    """Return the path for the generated Pydantic models module."""
    return Path(__file__).resolve().parent / "pydantic_models.py"


def _download_schema(schema_url: str) -> Path:
    """Download the schema URL to a temporary file."""
    with urlopen(schema_url) as response:
        data = response.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
        temp_file.write(data)
        return Path(temp_file.name)


def _run_codegen(schema_path: Path, output_path: Path) -> None:
    """Run datamodel-code-generator to produce Pydantic v2 models."""
    generate(
        input_=schema_path,
        input_file_type=InputFileType.JsonSchema,
        output=output_path,
        output_model_type="pydantic_v2.BaseModel",
    )


def generate_pydantic_models() -> Path:
    """Generate Pydantic v2 models from the bloom schema."""
    schema_url = utils.get_bloom_schema_url()
    schema_path = _download_schema(schema_url)
    output_path = _get_output_path()
    _run_codegen(schema_path, output_path)
    return output_path


if __name__ == "__main__":
    output = generate_pydantic_models()
    print(f"Generated Pydantic models at: {output}")

