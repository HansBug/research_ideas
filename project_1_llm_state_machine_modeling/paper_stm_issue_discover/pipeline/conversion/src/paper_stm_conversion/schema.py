from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import jsonschema
except Exception:  # pragma: no cover - tests install jsonschema in repo env
    jsonschema = None  # type: ignore[assignment]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_json(instance: dict[str, Any], schema_path: Path) -> None:
    if jsonschema is None:
        return
    schema = load_json(schema_path)
    jsonschema.Draft202012Validator(schema).validate(instance)
