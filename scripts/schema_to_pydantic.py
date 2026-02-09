"""
Generate Pydantic models from the bloom JSON schema.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set

import model_train_protocol as mtp


PRIMITIVE_TYPE_MAP: Dict[str, str] = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "null": "None",
}


def _get_schema_path(base_path: Optional[str]) -> Path:
    """Build the path to the versioned bloom schema file."""
    base = Path(base_path) if base_path is not None else Path(__file__).resolve().parents[1]
    version_semantic = mtp.utils.get_version()
    version_underscored = version_semantic.replace(".", "_")
    return base / "schemas" / f"v{version_semantic[0]}" / f"bloom_{version_underscored}.json"


def _load_schema(schema_path: Path) -> Dict[str, Any]:
    """Load a JSON schema from disk."""
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _extract_ref_name(ref: str) -> str:
    """Extract the terminal name from a JSON schema ref."""
    return ref.split("/")[-1]


def _collect_refs(schema: Any) -> Set[str]:
    """Collect referenced definition names from a schema subtree."""
    refs: Set[str] = set()
    if isinstance(schema, dict):
        if "$ref" in schema:
            refs.add(_extract_ref_name(schema["$ref"]))
        for value in schema.values():
            refs.update(_collect_refs(value))
    elif isinstance(schema, list):
        for item in schema:
            refs.update(_collect_refs(item))
    return refs


def _topo_sort_defs(defs: Dict[str, Any]) -> List[str]:
    """Topologically sort schema definitions by reference order."""
    order: List[str] = []
    visiting: Set[str] = set()
    visited: Set[str] = set()

    def visit(name: str) -> None:
        if name in visited:
            return
        if name in visiting:
            raise ValueError(f"Cyclic dependency in schema defs at {name}")
        visiting.add(name)
        for dep in _collect_refs(defs[name]):
            if dep in defs:
                visit(dep)
        visiting.remove(name)
        visited.add(name)
        order.append(name)

    for name in defs:
        visit(name)

    return order


def _is_null_schema(schema: Dict[str, Any]) -> bool:
    """Return True if the schema represents a null type."""
    return schema.get("type") == "null"


def _dedupe(items: Iterable[str]) -> List[str]:
    """Return items with duplicates removed, preserving order."""
    seen: Set[str] = set()
    result: List[str] = []
    for item in items:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result


def _type_for_object_schema(schema: Dict[str, Any]) -> str:
    """Resolve a typing annotation for object schemas."""
    additional = schema.get("additionalProperties", None)
    if additional is True:
        return "Dict[str, Any]"
    if isinstance(additional, dict):
        return f"Dict[str, {_type_from_schema(additional)}]"
    return "Dict[str, Any]"


def _type_from_anyof(anyof: List[Dict[str, Any]]) -> str:
    """Resolve a typing annotation for anyOf schemas."""
    types: List[str] = []
    has_null = False
    for option in anyof:
        if _is_null_schema(option):
            has_null = True
        else:
            types.append(_type_from_schema(option))
    types = _dedupe(types)
    if not types:
        base_type = "Any"
    elif len(types) == 1:
        base_type = types[0]
    else:
        base_type = f"Union[{', '.join(types)}]"
    if has_null:
        return f"Optional[{base_type}]"
    return base_type


def _type_from_schema(schema: Dict[str, Any]) -> str:
    """Resolve a typing annotation for a schema node."""
    if "$ref" in schema:
        return _extract_ref_name(schema["$ref"])
    if "anyOf" in schema:
        return _type_from_anyof(schema["anyOf"])
    schema_type = schema.get("type")
    if schema_type == "array":
        return f"List[{_type_from_schema(schema['items'])}]"
    if schema_type == "object":
        return _type_for_object_schema(schema)
    if schema_type in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[schema_type]
    raise ValueError(f"Unsupported schema type: {schema_type}")


def _wrap_optional(type_str: str) -> str:
    """Wrap a type string in Optional if needed."""
    if type_str.startswith("Optional["):
        return type_str
    return f"Optional[{type_str}]"


def _render_additional_properties_config(additional: Any) -> str:
    """Render model_config for additionalProperties."""
    return (
        "    model_config = ConfigDict(\n"
        "        extra=\"allow\",\n"
        f"        json_schema_extra={{\"additionalProperties\": {additional!r}}},\n"
        "    )\n"
    )


def _render_model_class(name: str, schema: Dict[str, Any]) -> str:
    """Render a Pydantic model class from a schema."""
    description = schema.get("description")
    lines: List[str] = [f"class {name}(BaseModel):"]
    if description:
        lines.append(f"    \"\"\"{description}\"\"\"")

    properties = schema.get("properties", {})
    required = set(schema.get("required", []))
    additional = schema.get("additionalProperties", None)

    if not properties and additional is not None:
        lines.append(_render_additional_properties_config(additional).rstrip())
        return "\n".join(lines)

    if not properties:
        lines.append("    pass")
        return "\n".join(lines)

    for prop_name, prop_schema in properties.items():
        field_type = _type_from_schema(prop_schema)
        if prop_name not in required:
            field_type = _wrap_optional(field_type)
            lines.append(f"    {prop_name}: {field_type} = None")
        else:
            lines.append(f"    {prop_name}: {field_type}")

    return "\n".join(lines)


def _render_models(schema: Dict[str, Any]) -> str:
    """Render all model classes for the full schema."""
    defs = schema.get("$defs", {})
    order = _topo_sort_defs(defs)
    class_blocks: List[str] = []

    for name in order:
        class_blocks.append(_render_model_class(name, defs[name]))

    root_name = schema.get("title", "ProtocolModel")
    class_blocks.append(_render_model_class(root_name, schema))

    exports = ", ".join([f'"{name}"' for name in order + [root_name]])

    header = "\n".join(
        [
            "\"\"\"",
            "Generated Pydantic models from bloom JSON schema.",
            "Do not edit by hand; run scripts/schema_to_pydantic.py.",
            "\"\"\"",
            "from typing import Any, Dict, List, Optional, Union",
            "",
            "from pydantic import BaseModel, ConfigDict",
            "",
            f"__all__ = [{exports}]",
            "",
        ]
    )

    return "\n\n".join([header] + class_blocks) + "\n"


def _normalize_schema(value: Any, parent_key: Optional[str] = None) -> Any:
    """Normalize schema structures for stable output."""
    if isinstance(value, dict):
        return {k: _normalize_schema(v, k) for k, v in sorted(value.items()) if k != "$schema"}
    if isinstance(value, list):
        if parent_key == "required":
            return sorted(value)
        return [_normalize_schema(item) for item in value]
    return value


def _load_generated_protocol_model(module_path: Path) -> Any:
    """Load the generated ProtocolModel class from disk."""
    spec = importlib.util.spec_from_file_location("scripts.pydantic_models", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.ProtocolModel


def generate_pydantic_models(base_path: Optional[str] = None) -> Path:
    """Generate Pydantic models from the bloom schema."""
    schema_path = _get_schema_path(base_path)
    schema = _load_schema(schema_path)

    output_path = Path(__file__).resolve().parent / "pydantic_models.py"
    output_path.write_text(_render_models(schema), encoding="utf-8")
    return output_path


if __name__ == "__main__":
    output = generate_pydantic_models()
    print(f"Generated Pydantic models at: {output}")
