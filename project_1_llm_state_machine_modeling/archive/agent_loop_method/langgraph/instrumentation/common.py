"""Shared prompt-safe utilities for LG-M1-D2 LangGraph instrumentation modules."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

def _canonical_json_payload(value: Any) -> str:
    """Canonical JSON used for reproducible LG-D2 policy hashes."""

    return json.dumps(_jsonable(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False, default=str)

def _hash_canonical_payload(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json_payload(value).encode("utf-8")).hexdigest()

def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(v) for v in value]
    if is_dataclass(value) and not isinstance(value, type):
        return _jsonable(asdict(value))
    return str(value)

def _hash_payload(payload: Any) -> str:
    encoded = json.dumps(_jsonable(payload), ensure_ascii=False, sort_keys=True, default=str)
    return "sha256:" + hashlib.sha256(encoded.encode("utf-8")).hexdigest()

def _hash_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()

def _package_version(name: str) -> str:
    try:
        return importlib.metadata.version(name)
    except Exception:
        return "unknown"

