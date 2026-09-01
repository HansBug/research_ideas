"""Scan only baseline raw records for scope-membership evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PAIR_MIN = 0
PAIR_MAX = 19
CLASSIFICATION_FIELD_NAMES = {
    "label",
    "validity",
    "category",
    "classification",
    "verdict",
    "knownness",
    "relation",
    "is_known",
    "is_invalid",
}


def sha256_file(path: Path) -> str:
    """Hash one raw artifact without interpreting its semantic contents."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def load_json(path: Path) -> Any:
    """Load one raw JSON record."""

    return json.loads(path.read_text(encoding="utf-8"))


def scan(archive_root: Path) -> dict[str, Any]:
    """Enumerate baseline raw records and report whether scope labels exist."""

    record_paths = sorted((archive_root / "raw/x1v2_baseline/method").glob("run*/**/record.json"))
    pair_counts: Counter[str] = Counter()
    requested_report_ids: list[str] = []
    field_names: set[str] = set()
    classification_fields: set[str] = set()
    basis_present = 0
    pair_id_mismatches: list[dict[str, str]] = []
    input_hashes: dict[str, str] = {}

    for path in record_paths:
        record = load_json(path)
        path_pair_id = path.parent.name.split("-", 1)[0]
        record_pair_id = str(record["pair_id"])
        round_number = int(record["round"])
        issues = record["parsed_output"]["issues"]
        relative_path = str(path.relative_to(archive_root))
        input_hashes[relative_path] = sha256_file(path)
        pair_counts[path_pair_id] += len(issues)
        if record_pair_id != path_pair_id:
            pair_id_mismatches.append({
                "path": relative_path,
                "path_derived_pair_id": path_pair_id,
                "raw_record_pair_id": record_pair_id,
            })
        for index, issue in enumerate(issues):
            field_names.update(issue)
            classification_fields.update(
                field for field in issue if field.lower() in CLASSIFICATION_FIELD_NAMES
            )
            basis_present += "basis" in issue
            if PAIR_MIN <= int(path_pair_id) <= PAIR_MAX:
                requested_report_ids.append(f"{path_pair_id}:r{round_number}:finding:{index}")

    requested_counts = {
        f"{pair_number:04d}": pair_counts.get(f"{pair_number:04d}", 0)
        for pair_number in range(PAIR_MIN, PAIR_MAX + 1)
    }
    return {
        "schema": "paper1.manual-adjudication.v3-baseline-ni.raw-scope-probe.v1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "scope_gate": "OPEN_EVIDENCE_GAP",
        "allowed_input_policy": {
            "raw_method_records_only": True,
            "forbidden_inputs_read": False,
            "forbidden_inputs": [
                "v2 decisions",
                "old labels",
                "Track B",
                "other reviewer conclusions",
                "proposals",
                "registers",
                "Judge outputs",
            ],
        },
        "raw_record_count": len(record_paths),
        "raw_report_count": sum(pair_counts.values()),
        "requested_pair_range": {
            "min_pair_id": f"{PAIR_MIN:04d}",
            "max_pair_id": f"{PAIR_MAX:04d}",
            "report_count": sum(requested_counts.values()),
            "pair_coverage": requested_counts,
            "report_identity_count": len(requested_report_ids),
        },
        "raw_finding_field_union": sorted(field_names),
        "classification_like_fields_present": sorted(classification_fields),
        "basis_field_present_count": basis_present,
        "raw_pair_id_path_mismatch_count": len(pair_id_mismatches),
        "raw_pair_id_path_mismatches": pair_id_mismatches,
        "scope_evidence": {
            "historical_non_k_membership_encoded_in_raw": False,
            "reason": "Raw findings expose issue/where/reason fields but no historical K/N/I membership field.",
            "required_external_evidence": "An allowed report-ID scope manifest for historical non-K membership.",
        },
        "input_hashes": dict(sorted(input_hashes.items())),
    }


def main() -> None:
    """Write the raw-only scope probe."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = scan(args.archive_root.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "raw_records": result["raw_record_count"],
        "raw_reports": result["raw_report_count"],
        "requested_reports": result["requested_pair_range"]["report_count"],
        "classification_like_fields_present": result["classification_like_fields_present"],
        "basis_field_present_count": result["basis_field_present_count"],
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
