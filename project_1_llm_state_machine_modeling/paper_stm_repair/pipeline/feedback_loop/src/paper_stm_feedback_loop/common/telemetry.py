from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime, timezone
from typing import Any

try:
    from typing import Literal
except ImportError:  # pragma: no cover - Python 3.7 compatibility
    from typing_extensions import Literal

RecordKind = Literal["node_execution", "llm_call", "transport_attempt"]
SECRET_KEY_RE = re.compile(
    r"(api[_-]?key|authorization|bearer|(?:access|auth|proxy|refresh)[_-]?token|secret|password|credential)",
    re.I,
)
SECRET_VALUE_RE = re.compile(
    r"(?i)(sk-[A-Za-z0-9_\-]{12,}|Bearer\s+[A-Za-z0-9._\-]{12,}|[A-Za-z0-9_\-]{24,}\.[A-Za-z0-9_\-]{6,}\.[A-Za-z0-9_\-]{12,})"
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _json_default(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if isinstance(value, set):
        return sorted(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=_json_default)


def sha256_json(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def redact(value: Any) -> Any:
    """Return a JSON-compatible full-shape copy with secrets redacted."""

    if is_dataclass(value):
        value = asdict(value)
    elif hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        for key, item in value.items():
            key_str = str(key)
            redacted[key_str] = "[REDACTED]" if SECRET_KEY_RE.search(key_str) else redact(item)
        return redacted
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, tuple):
        return [redact(item) for item in value]
    if isinstance(value, str):
        return SECRET_VALUE_RE.sub("[REDACTED]", value)
    return value


@dataclass(frozen=True)
class RedactedFullHash:
    redacted_full: Any
    full_sha256: str


def redacted_full_hash(value: Any) -> RedactedFullHash:
    """Preserve full redacted shape plus a hash of the unredacted payload."""

    return RedactedFullHash(redacted_full=redact(value), full_sha256=sha256_json(value))


@dataclass(frozen=True)
class TransportAttempt:
    attempt_id: str
    provider: str
    model: str
    started_at: str
    ended_at: str | None = None
    status: Literal["ok", "error", "timeout"] = "ok"
    latency_ms: int | None = None
    error_type: str | None = None
    error_message: str | None = None
    request: dict[str, Any] | None = None
    response: dict[str, Any] | None = None
    kind: Literal["transport_attempt"] = "transport_attempt"

    def to_record(self) -> dict[str, Any]:
        payload = asdict(self)
        for field in ("request", "response", "error_message"):
            if payload.get(field) is not None:
                marker = redacted_full_hash(payload[field])
                payload[field] = marker.redacted_full
                payload[f"{field}_sha256"] = marker.full_sha256
        return payload


@dataclass(frozen=True)
class LLMCall:
    call_id: str
    stage: str
    provider: str
    model: str
    started_at: str
    ended_at: str | None = None
    status: Literal["ok", "error"] = "ok"
    prompt: Any | None = None
    response: Any | None = None
    usage: dict[str, Any] | None = None
    attempts: tuple[TransportAttempt, ...] = ()
    kind: Literal["llm_call"] = "llm_call"

    def to_record(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["attempts"] = [attempt.to_record() for attempt in self.attempts]
        for field in ("prompt", "response"):
            if payload.get(field) is not None:
                marker = redacted_full_hash(payload[field])
                payload[field] = marker.redacted_full
                payload[f"{field}_sha256"] = marker.full_sha256
        return payload


@dataclass(frozen=True)
class NodeExecution:
    node_id: str
    node_type: str
    started_at: str
    ended_at: str | None = None
    status: Literal["ok", "error", "skipped"] = "ok"
    inputs: Any | None = None
    outputs: Any | None = None
    error_type: str | None = None
    error_message: str | None = None
    llm_calls: tuple[LLMCall, ...] = ()
    kind: Literal["node_execution"] = "node_execution"

    def to_record(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["llm_calls"] = [call.to_record() for call in self.llm_calls]
        for field in ("inputs", "outputs", "error_message"):
            if payload.get(field) is not None:
                marker = redacted_full_hash(payload[field])
                payload[field] = marker.redacted_full
                payload[f"{field}_sha256"] = marker.full_sha256
        return payload


def record_to_dict(record: NodeExecution | LLMCall | TransportAttempt | dict[str, Any]) -> dict[str, Any]:
    if isinstance(record, dict):
        return redact(record)
    if hasattr(record, "model_dump"):
        return redact(record.model_dump(mode="json"))
    return record.to_record()


def summarize_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    by_kind: dict[str, int] = {}
    by_status: dict[str, int] = {}
    error_count = 0
    for record in records:
        kind = str(record.get("kind", "unknown"))
        status = str(record.get("status", "unknown"))
        by_kind[kind] = by_kind.get(kind, 0) + 1
        by_status[status] = by_status.get(status, 0) + 1
        if status in {"error", "timeout"}:
            error_count += 1
    return {"record_count": len(records), "by_kind": by_kind, "by_status": by_status, "error_count": error_count}
