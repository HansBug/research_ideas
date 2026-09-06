from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .telemetry import sha256_text


@dataclass(frozen=True)
class SourceTraceBundle:
    path: Path
    data: dict[str, Any]
    sha256: str
    entry_count: int
    attribution_exclusion_count: int


def load_json_object(path: str | Path) -> dict[str, Any]:
    source = Path(path).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    value = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {source}")
    return value


def load_source_trace(path: str | Path) -> SourceTraceBundle:
    source = Path(path).expanduser().resolve()
    text = source.read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"source trace must be a JSON object: {source}")
    entries = data.get("entries", [])
    exclusions = data.get("attribution_exclusions", [])
    if not isinstance(entries, list):
        raise ValueError("source trace entries must be a list")
    if not isinstance(exclusions, list):
        raise ValueError("source trace attribution_exclusions must be a list")
    return SourceTraceBundle(
        path=source,
        data=data,
        sha256=sha256_text(text),
        entry_count=len(entries),
        attribution_exclusion_count=len(exclusions),
    )


def source_trace_summary(bundle: SourceTraceBundle | dict[str, Any]) -> dict[str, Any]:
    data = bundle.data if isinstance(bundle, SourceTraceBundle) else bundle
    entries = data.get("entries", []) if isinstance(data.get("entries", []), list) else []
    exclusions = data.get("attribution_exclusions", []) if isinstance(data.get("attribution_exclusions", []), list) else []
    return {
        "schema_version": data.get("schema_version"),
        "trace_scope": data.get("trace_scope"),
        "entry_count": len(entries),
        "attribution_exclusion_count": len(exclusions),
        "closure_claim_allowed": (data.get("source_traceability") or {}).get("closure_claim_allowed")
        if isinstance(data.get("source_traceability"), dict)
        else None,
    }
