from __future__ import annotations

import json
import re
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .telemetry import LLMCall, NodeExecution, TransportAttempt, record_to_dict, summarize_records

__all__ = [
    "LLMCall",
    "ImmutableRecordRef",
    "ImmutableRecordStore",
    "NodeExecution",
    "TransportAttempt",
    "append_jsonl_record",
    "append_jsonl_records",
    "iter_jsonl_records",
    "load_jsonl_records",
    "summarize_records",
]

_SLUG_RE = re.compile(r"[^a-z0-9-]+")


@dataclass(frozen=True)
class ImmutableRecordRef:
    sequence: int
    event: str
    path: Path


class ImmutableRecordStore:
    """Append one complete record per immutable sequence directory."""

    def __init__(self, root: str | Path, *, loop_index: int = 0) -> None:
        raw = str(root)
        if not raw or "\x00" in raw:
            raise ValueError("record root must be non-empty and contain no NUL byte")
        self.root = Path(root).expanduser().resolve()
        if self.root.exists() and not self.root.is_dir():
            raise NotADirectoryError(self.root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.loop_index = loop_index
        self._next_sequence = self._discover_next_sequence()

    def _discover_next_sequence(self) -> int:
        sequences: list[int] = []
        for child in self.root.iterdir():
            match = re.match(r"^L\d{3}-(\d{6})-", child.name)
            if child.is_dir() and match:
                sequences.append(int(match.group(1)))
        return max(sequences, default=0) + 1

    def append(self, event: str, payload: Any) -> ImmutableRecordRef:
        slug = _SLUG_RE.sub("-", event.strip().lower().replace("_", "-")).strip("-")
        if not slug:
            raise ValueError("record event must contain an alphanumeric character")
        sequence = self._next_sequence
        directory = self.root / f"L{self.loop_index:03d}-{sequence:06d}-{slug}"
        directory.mkdir(parents=False, exist_ok=False)
        path = directory / "record.json"
        value = record_to_dict(payload) if not isinstance(payload, (list, tuple)) else payload
        with path.open("x", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2, default=str)
            stream.write("\n")
        self._next_sequence += 1
        return ImmutableRecordRef(sequence=sequence, event=event, path=path)

    def refs(self) -> tuple[ImmutableRecordRef, ...]:
        refs: list[ImmutableRecordRef] = []
        for child in sorted(self.root.iterdir()):
            match = re.match(r"^L\d{3}-(\d{6})-(.+)$", child.name)
            path = child / "record.json"
            if child.is_dir() and match and path.is_file():
                refs.append(
                    ImmutableRecordRef(
                        sequence=int(match.group(1)), event=match.group(2), path=path
                    )
                )
        return tuple(refs)


def _clean_output_path(path: str | Path) -> Path:
    raw = str(path)
    if "\x00" in raw:
        raise ValueError("record path contains a NUL byte")
    resolved = Path(path).expanduser().resolve()
    if resolved.exists() and resolved.is_dir():
        raise IsADirectoryError(resolved)
    return resolved


def append_jsonl_record(path: str | Path, record: NodeExecution | LLMCall | TransportAttempt | dict[str, Any]) -> dict[str, Any]:
    """Append one redacted JSON object to a JSONL file without truncating it."""

    target = _clean_output_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = record_to_dict(record)
    with target.open("a", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, sort_keys=True)
        handle.write("\n")
    return payload


def append_jsonl_records(path: str | Path, records: Iterable[NodeExecution | LLMCall | TransportAttempt | dict[str, Any]]) -> list[dict[str, Any]]:
    written: list[dict[str, Any]] = []
    for record in records:
        written.append(append_jsonl_record(path, record))
    return written


def iter_jsonl_records(path: str | Path) -> Iterator[dict[str, Any]]:
    source = _clean_output_path(path)
    with source.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSONL at {source}:{line_number}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"JSONL record must be an object at {source}:{line_number}")
            yield value


def load_jsonl_records(path: str | Path) -> list[dict[str, Any]]:
    return list(iter_jsonl_records(path))
