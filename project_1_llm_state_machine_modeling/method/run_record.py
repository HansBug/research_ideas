"""Single-file AgentLoopRunRecord persistence helpers for PR-2A.

The helpers here intentionally stay stdlib-only and deterministic.  They are
the narrow persistence boundary used by Path1/Path2 handoff smoke: a run is
eligible for downstream main-result statistics only when its self-contained
``*.agent_loop.json.gz`` can be loaded as a schema-valid
``AgentLoopRunRecord`` and is explicitly marked eligible.
"""

from __future__ import annotations

import gzip
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from method.schema import AgentLoopRunRecord

RUN_RECORD_SUFFIX = ".agent_loop.json.gz"


def agent_loop_run_record_path(output_dir: str | Path, run_id: str) -> Path:
    """Return the canonical single-file run record path."""
    return Path(output_dir) / f"{run_id}{RUN_RECORD_SUFFIX}"


def write_agent_loop_run_record(record: AgentLoopRunRecord, path: str | Path) -> Path:
    """Write ``record`` as canonical gzip-compressed JSON and validate it.

    Validation happens both before and after gzip round-trip so callers cannot
    accidentally persist a dict shape that only works in memory.
    The target file is replaced atomically only after JSON serialization and
    gzip round-trip validation succeed, avoiding half-written corrupt records.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    AgentLoopRunRecord(**asdict(record))
    payload = asdict(record)
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    tmp_path = path.with_name(path.name + ".tmp")
    try:
        with gzip.open(tmp_path, "wt", encoding="utf-8") as f:
            f.write(encoded)
        read_agent_loop_run_record(tmp_path)
        tmp_path.replace(path)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise
    return path


def read_agent_loop_run_record(path: str | Path) -> AgentLoopRunRecord:
    """Load and validate a gzip-compressed ``AgentLoopRunRecord``."""
    with gzip.open(path, "rt", encoding="utf-8") as f:
        payload: dict[str, Any] = json.load(f)
    return AgentLoopRunRecord(**payload)


def is_path_result_eligible(record_or_payload: AgentLoopRunRecord | dict[str, Any]) -> bool:
    """Return whether a run is allowed into Path1/Path2 main-result stats."""
    record = record_or_payload if isinstance(record_or_payload, AgentLoopRunRecord) else AgentLoopRunRecord(**record_or_payload)
    if record.status != "success":
        return False
    return bool(record.final_artifacts.get("main_result_eligible") is True)
