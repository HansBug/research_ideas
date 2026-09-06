"""Label frozen predicate receipts with current IDs without re-evaluating them."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

CURRENT_REGISTRY = "four-family-12-core.v1"
PRE_P1_REGISTRY = "four-family-19-core.v1"
PRE_P1_TO_CURRENT: dict[str, str | None] = {
    "S1": "S1", "S2": "S2", "S3": "S3", "S4": "S4", "S5": "S5", "S6": None,
    "G1": "G1", "G2": "G2", "G3": None, "G4": "G3",
    "R1": "R1", "R2": "R2", "R3": None, "R4": "R3",
    "V1": None, "V2": None, "V3": None, "V4": "V1", "V5": None,
}
CURRENT_IDS = frozenset(value for value in PRE_P1_TO_CURRENT.values() if value is not None)


def current_predicate_id(registry_version: str, predicate_id: str | None) -> str | None:
    """Resolve an ID within its source version; retired and unbound IDs map to null."""

    if registry_version not in {CURRENT_REGISTRY, PRE_P1_REGISTRY}:
        raise ValueError(f"unknown predicate registry version: {registry_version}")
    if predicate_id is None:
        return None
    if registry_version == PRE_P1_REGISTRY and predicate_id in PRE_P1_TO_CURRENT:
        return PRE_P1_TO_CURRENT[predicate_id]
    if registry_version == CURRENT_REGISTRY and predicate_id in CURRENT_IDS:
        return predicate_id
    raise ValueError(f"unknown predicate ID for {registry_version}: {predicate_id}")


def build_predicate_id_view(run_root: Path) -> dict[str, Any]:
    """Count every saved execution receipt, preserving original IDs and verdicts."""

    manifest_bytes = (run_root / "run_manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    version = manifest["registry_version"]
    current_predicate_id(version, None)
    cells = sorted((run_root / "method").glob("*/round-*.json"))
    if not cells:
        raise ValueError("method run contains no saved cells")
    counts: dict[str | None, Counter] = {}
    sources = []
    total = 0
    for path in cells:
        raw_bytes = path.read_bytes()
        cell = json.loads(raw_bytes)
        if cell["run_id"] != manifest["run_id"]:
            raise ValueError(f"mixed run identity: {path}")
        sources.append({"path": path.relative_to(run_root).as_posix(), "sha256": hashlib.sha256(raw_bytes).hexdigest()})
        for receipt in cell["predicate_execution_receipts"]:
            original_id = receipt["predicate_id"]
            current_predicate_id(version, original_id)
            bucket = counts.setdefault(original_id, Counter())
            bucket["receipt_count"] += 1
            total += 1
            if receipt.get("terminal_state") == "completed" and receipt.get("predicate_verdict") in {"true", "false"}:
                bucket["terminal_count"] += 1
                bucket[receipt["predicate_verdict"]] += 1
    rows = []
    for original_id, bucket in sorted(counts.items(), key=lambda item: item[0] or ""):
        mapped = current_predicate_id(version, original_id)
        rows.append({
            "source_registry_version": version,
            "original_predicate_id": original_id,
            "current_predicate_id": mapped,
            "mapping_status": "unbound" if original_id is None else "retired" if mapped is None else "retained",
            **{key: bucket[key] for key in ("receipt_count", "terminal_count", "true", "false")},
        })
    return {
        "schema": "paper1.predicate-id-view.v1",
        "source_run_id": manifest["run_id"],
        "source_registry_version": version,
        "source_registry_hash": manifest["registry_hash"],
        "source_manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "current_label_registry": CURRENT_REGISTRY,
        "interpretation": "Saved receipt counts with current labels only; no backend, witness, report, or validity re-evaluation.",
        "source_cells": sources,
        "receipt_count": total,
        "rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, help="New JSON view outside the source run and final_results; omit for stdout.")
    args = parser.parse_args(argv)
    if args.output is not None:
        target = args.output.resolve()
        if target.is_relative_to(args.run_root.resolve()) or "final_results" in target.parts:
            parser.error("the label view must be outside frozen/source artifacts")
    view = build_predicate_id_view(args.run_root)
    text = json.dumps(view, ensure_ascii=False, indent=2) + "\n"
    if args.output is None:
        print(text, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
