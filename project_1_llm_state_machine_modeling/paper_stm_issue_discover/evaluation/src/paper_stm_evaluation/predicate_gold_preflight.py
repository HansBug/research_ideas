"""Correct mechanically invalid Track C preflight seals without changing review content."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .predicate_gold import canonical_sha256, sha256_path, write_json


def _utc_now() -> str:
    """Return the current RFC 3339 UTC timestamp."""

    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def seal_preflight(
    *, source_path: Path, output_path: Path, correction_log_path: Path
) -> dict[str, Any]:
    """Write a separately versioned copy with row and batch digests recomputed."""

    source = json.loads(source_path.read_text(encoding="utf-8"))
    if not isinstance(source.get("rows"), list) or not source["rows"]:
        raise ValueError("preflight must contain a non-empty rows array")

    corrected = json.loads(json.dumps(source))
    row_changes: list[dict[str, str]] = []
    for row in corrected["rows"]:
        hash_fields = [name for name in ("row_sha256", "audit_sha256") if name in row]
        if len(hash_fields) != 1:
            raise ValueError(
                f"{row.get('ledger_id')} must have exactly one row hash field, got {hash_fields}"
            )
        hash_field = hash_fields[0]
        stored = row[hash_field]
        unsigned = {key: value for key, value in row.items() if key != hash_field}
        recomputed = canonical_sha256(unsigned)
        row[hash_field] = recomputed
        row_changes.append(
            {
                "ledger_id": str(row["ledger_id"]),
                "hash_field": hash_field,
                "stored_sha256": str(stored),
                "corrected_sha256": recomputed,
            }
        )

    stored_batch = corrected.get("batch_sha256")
    if not isinstance(stored_batch, str):
        raise TypeError("preflight batch_sha256 must be a string")
    unsigned_batch = {
        key: value for key, value in corrected.items() if key != "batch_sha256"
    }
    corrected_batch = canonical_sha256(unsigned_batch)
    corrected["batch_sha256"] = corrected_batch
    write_json(output_path, corrected)

    reloaded = json.loads(output_path.read_text(encoding="utf-8"))
    for row in reloaded["rows"]:
        hash_field = "row_sha256" if "row_sha256" in row else "audit_sha256"
        unsigned = {key: value for key, value in row.items() if key != hash_field}
        if row[hash_field] != canonical_sha256(unsigned):
            raise ValueError(f"corrected row seal failed for {row['ledger_id']}")
    unsigned = {key: value for key, value in reloaded.items() if key != "batch_sha256"}
    if reloaded["batch_sha256"] != canonical_sha256(unsigned):
        raise ValueError("corrected batch seal failed")

    log_unsigned = {
        "schema_version": "paper1.predicate-gold.preflight-seal-correction.v1",
        "source_path": source_path.as_posix(),
        "source_file_sha256": sha256_path(source_path),
        "source_stored_batch_sha256": stored_batch,
        "corrected_path": output_path.as_posix(),
        "corrected_file_sha256": sha256_path(output_path),
        "corrected_batch_sha256": corrected_batch,
        "row_changes": row_changes,
        "semantic_fields_changed": False,
        "correction_reason": "The submitted row and batch digests did not match their documented canonical JSON rule; this layer changes only those digest fields.",
        "corrected_at": _utc_now(),
    }
    log = {**log_unsigned, "log_sha256": canonical_sha256(log_unsigned)}
    write_json(correction_log_path, log)
    return log


def main() -> int:
    """Seal one submitted preflight into a separate corrected layer."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--correction-log", type=Path, required=True)
    args = parser.parse_args()
    log = seal_preflight(
        source_path=args.source,
        output_path=args.output,
        correction_log_path=args.correction_log,
    )
    print(
        f"wrote {args.output} ({len(log['row_changes'])} rows, "
        f"{log['corrected_batch_sha256']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
