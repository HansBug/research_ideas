#!/usr/bin/env python3
"""Downgrade an unproven bulk promotion to an explicit proposal snapshot.

This is a one-way audit operation for the manual-adjudication workspace.  It
does not read or write frozen raw artifacts.  It keeps all evidence payloads,
but removes final-status claims until a later per-report pane5 adjudication
record is supplied to the confirmation command.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


FINAL_FILES = (
    "v60_report_decisions.json",
    "x1v2_report_decisions.json",
    "relation_decisions.json",
    "hit_max_witness.json",
    "group_decisions.json",
    "summary.json",
    "review_log.json",
    "calibration_report.json",
    "reference_ledger_aggregate.json",
    "predicate_witness_audit.json",
)


def downgrade(value: Any) -> Any:
    """Recursively retain data while changing only workflow status fields."""
    if isinstance(value, list):
        return [downgrade(item) for item in value]
    if isinstance(value, dict):
        result = {key: downgrade(item) for key, item in value.items()}
        if result.get("review_status") in {"FINAL", "ARBITRATED"}:
            result["review_status"] = "PROPOSAL"
        if result.get("status") in {"FINAL", "ARBITRATED"}:
            result["status"] = "PROPOSAL"
        if "human_confirmation" in result:
            result["human_confirmation"] = False
        if "human_supervised_session" in result and result.get("review_status") == "PROPOSAL":
            result["human_supervised_session"] = False
        if "final_adjudicator_id" in result:
            result["final_adjudicator_id"] = None
        if "primary_reviewer_id" in result and result.get("review_status") == "PROPOSAL":
            result["primary_reviewer_id"] = "pending:pane5-supervised-adjudicator"
        return result
    return value


def main() -> None:
    """Downgrade canonical JSON files in one explicit audit directory."""
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    for name in FINAL_FILES:
        path = args.directory / name
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        path.write_text(json.dumps(downgrade(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PROPOSAL", "directory": str(args.directory), "files": list(FINAL_FILES)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
