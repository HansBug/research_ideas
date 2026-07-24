from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any


def canonical_data(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return canonical_data(value.model_dump(mode="json"))
    if isinstance(value, dict):
        return {str(k): canonical_data(value[k]) for k in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [canonical_data(v) for v in value]
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(
        canonical_data(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def sha256_data(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
