#!/usr/bin/env python3
"""Persist one addressable pane5 arbitration record for every v3 report.

This migration only adds audit pointers and copies existing review-chain facts
into a versioned log.  It does not alter D/A, relation, validity, K/N/I, raw
text, source references, or any frozen v2 row.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from paper_stm_evaluation.manual_adjudication_v3_baseline_ni import (
    ARBITRATION_LOG_PATH,
    arbitration_record_pointer,
)


def load(path: Path) -> Any:
    """Read one UTF-8 JSON artifact."""

    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    """Return the archive-prefixed SHA-256 of one file."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    """Write deterministic, human-readable UTF-8 JSON."""

    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Mirror canonical decision rows using the established fixed-column encoding."""

    fields = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({
                key: json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                if isinstance(value, (dict, list, tuple)) else ("" if value is None else value)
                for key, value in row.items()
            })


def main() -> None:
    """Add pointers, write the arbitration log, and mirror the TSV."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-root", type=Path, required=True)
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    v3 = archive / "derived/manual_adjudication_v3_baseline_ni"
    decision_path = v3 / "baseline_report_decisions_v3.json"
    pane5_path = v3 / "pane5_adjudications_v3.json"
    evidence_path = v3 / "pane5_evidence_reads_v3.json"

    decisions_doc = load(decision_path)
    pane5_doc = load(pane5_path)
    decisions = decisions_doc["decisions"]
    pane5_rows = pane5_doc["rows"]
    decision_ids = {row["original_report_id"] for row in decisions}
    pane5_ids = {row["report_id"] for row in pane5_rows}
    if decision_ids != pane5_ids or len(decision_ids) != 233:
        raise ValueError("decision and pane5 row identities do not close over 233 reports")

    pane5_by_id = {row["report_id"]: row for row in pane5_rows}
    entries: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(decisions):
        report_id = row["original_report_id"]
        review = row["review"]
        review["arbitration_record_pointer"] = arbitration_record_pointer(report_id)
        pane5_review = pane5_by_id[report_id]["review"]
        pane5_review["arbitration_record_pointer"] = arbitration_record_pointer(report_id)
        entries[report_id] = {
            "report_id": report_id,
            "decision_json_pointer": f"/decisions/{index}",
            "disagreement_flag": review["disagreement_flag"],
            "disagreement_details": review["disagreement_details"],
            "independent_reviewer_ids": review["independent_reviewer_ids"],
            "independent_opinion_submission_hashes": [
                opinion["submission_hash"] for opinion in review["independent_opinions"]
            ],
            "pane5_primary_reviewer_id": review["primary_reviewer_id"],
            "arbitration_reason": review["arbitration_reason"],
            "arbitration_basis": review["arbitration_basis"],
            "final_adjudicator_id": review["final_adjudicator_id"],
            "human_confirmation": review["human_confirmation"],
            "confirmation_time_utc": review["confirmation_time_utc"],
            "human_session_reference": review["human_session_reference"],
            "review_status": review["review_status"],
            "source_evidence_path": "pane5_evidence_reads_v3.json",
            "source_evidence_sha256": sha256(evidence_path),
            "record_pointer": arbitration_record_pointer(report_id),
        }

    log = {
        "schema": "paper1.manual-adjudication.v3-baseline-ni.arbitration-log",
        "protocol_version": "issue-189-195-baseline-ni-v3",
        "scope": "One persisted pane5 arbitration record for each of the 233 re-reviewed non-K reports.",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "generated_by": "materialize_v3_arbitration_log.py",
        "source_decisions_path": "baseline_report_decisions_v3.json",
        "source_pane5_path": "pane5_adjudications_v3.json",
        "entries_by_report_id": entries,
        "entry_count": len(entries),
        "disagreement_count": sum(1 for entry in entries.values() if entry["disagreement_flag"]),
        "human_adjudicator_id": "human:pane5-supervised-adjudicator",
        "human_confirmation": True,
        "provider_calls": 0,
        "method_reruns": 0,
        "judge_reruns": 0,
        "record_pointer_format": f"{ARBITRATION_LOG_PATH}#/entries_by_report_id/<report_id>",
    }
    write_json(v3 / "reviews/arbitration_log_v3.json", log)
    write_json(decision_path, decisions_doc)
    write_json(pane5_path, pane5_doc)
    write_tsv(v3 / "baseline_report_decisions_v3.tsv", decisions)
    print(json.dumps({"status": "PASS", "entries": len(entries), "disagreements": log["disagreement_count"], "provider_calls": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
