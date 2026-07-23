from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any, Mapping


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()



EVIDENCE_SCOPE_METADATA_KEYS: tuple[str, ...] = (
    "initialization",
    "formal",
    "check",
    "policy",
    "initialization_mode",
    "requested_initial_state",
    "effective_initial_state",
    "requested_initial_vars",
    "effective_initial_vars",
    "formal_bound",
    "formal_bound_origin",
    "formal_assumption_basis_ids",
    "check_result_sha256",
    "tool_schema_hash",
    "tool_hash",
    "policy_hash",
    "evidence_policy_fingerprint",
)


def evidence_scope_metadata(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Return reviewer-visible initialization/formal/check/policy payload fields."""

    return {key: payload[key] for key in EVIDENCE_SCOPE_METADATA_KEYS if key in payload}


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "record"


def _fsync_directory(path: Path) -> None:
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    except OSError:
        pass


class RecordStore:
    """Single-writer append-only store for paper1 method facts."""

    def __init__(self, outdir: Path) -> None:
        self.outdir = outdir.resolve()
        self.records = self.outdir / "records"
        self.records.mkdir(parents=True, exist_ok=True)

    def _existing(self) -> list[Path]:
        return sorted(path for path in self.records.iterdir() if path.is_dir() and (path / "record.json").is_file())

    def all(self) -> list[dict[str, Any]]:
        return [json.loads((path / "record.json").read_text(encoding="utf-8")) for path in self._existing()]

    def latest(self, record_type: str) -> dict[str, Any] | None:
        return next((item for item in reversed(self.all()) if item["record_type"] == record_type), None)

    def record_id_at_offset(self, offset: int = 0) -> str:
        if offset < 0:
            raise ValueError("offset must be non-negative")
        return f"REC-{len(self._existing()) + offset + 1:06d}"

    def append(
        self,
        record_type: str,
        payload: Mapping[str, Any],
        *,
        stage: str = "B-discover",
        logical_loop_index: int = 0,
        artifact_paths: Mapping[str, Path] | None = None,
    ) -> dict[str, Any]:
        existing = self.all()
        sequence = len(existing) + 1
        previous = existing[-1] if existing else None
        artifacts = []
        for role, path in sorted((artifact_paths or {}).items()):
            resolved = path.resolve()
            try:
                relative = resolved.relative_to(self.outdir)
            except ValueError as exc:
                raise ValueError(f"artifact path escapes run root: {path}") from exc
            if not resolved.is_file() or resolved.is_symlink():
                raise ValueError(f"artifact must be a regular file: {path}")
            artifacts.append({"role": role, "path": relative.as_posix(), "sha256": sha256_file(resolved)})
        body: dict[str, Any] = {
            "record_id": f"REC-{sequence:06d}",
            "sequence": sequence,
            "logical_loop_index": logical_loop_index,
            "record_type": record_type,
            "stage": stage,
            "loop_id": "discover" if logical_loop_index == 0 else f"loop-{logical_loop_index:03d}",
            "previous_record_id": previous["record_id"] if previous else None,
            "previous_record_sha256": previous["record_sha256"] if previous else None,
            "payload": dict(payload),
            "artifact_refs": artifacts,
        }
        body["record_sha256"] = sha256_json(body)
        final = self.records / f"L{logical_loop_index:03d}-{sequence:06d}-{_slug(record_type)}"
        if final.exists():
            raise FileExistsError(final)
        temporary = Path(tempfile.mkdtemp(prefix=f".{final.name}.", dir=self.records))
        try:
            record_path = temporary / "record.json"
            with record_path.open("w", encoding="utf-8") as stream:
                json.dump(body, stream, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, final)
            _fsync_directory(self.records)
        except Exception:
            shutil.rmtree(temporary, ignore_errors=True)
            raise
        return body

    def write_immutable_json(self, relative_path: str, value: Mapping[str, Any]) -> Path:
        target = (self.outdir / relative_path).resolve()
        try:
            target.relative_to(self.outdir)
        except ValueError as exc:
            raise ValueError(f"path escapes run root: {relative_path}") from exc
        if target.exists() or target.is_symlink():
            raise FileExistsError(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, name = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                json.dump(dict(value), stream, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(name, target)
            _fsync_directory(target.parent)
        finally:
            if os.path.exists(name):
                os.unlink(name)
        return target

    def evidence_index(self) -> dict[str, Any]:
        records = self.all()
        by_type: dict[str, list[str]] = {}
        for record in records:
            by_type.setdefault(record["record_type"], []).append(record["record_id"])
        return {"record_ids": [record["record_id"] for record in records], "record_ids_by_type": by_type}

    def validate_chain(self) -> None:
        previous: dict[str, Any] | None = None
        for expected, record in enumerate(self.all(), start=1):
            if record["sequence"] != expected or record["record_id"] != f"REC-{expected:06d}":
                raise ValueError("record sequence is not contiguous")
            claimed = record["record_sha256"]
            unhashed = {key: value for key, value in record.items() if key != "record_sha256"}
            if claimed != sha256_json(unhashed):
                raise ValueError(f"record hash mismatch: {record['record_id']}")
            if previous is None:
                if record["previous_record_id"] is not None or record["previous_record_sha256"] is not None:
                    raise ValueError("first record has a previous link")
            elif (record["previous_record_id"], record["previous_record_sha256"]) != (
                previous["record_id"],
                previous["record_sha256"],
            ):
                raise ValueError(f"record link mismatch: {record['record_id']}")
            previous = record
