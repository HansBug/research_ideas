#!/usr/bin/env python3
"""Record an explicit pane5 input after every raw/source record is supplied.

This command is deliberately input-driven.  It never reads proposal labels to
fill a missing field and never assigns ``FINAL`` or ``human_confirmation``.
The supplied per-report Pydantic rows are checked against the immutable raw
target and author-source closure, then persisted as the pane5 input consumed by
the confirmation backend.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from confirm_manual_adjudication import canonical_bytes, load, read_evidence
from paper_stm_evaluation.manual_adjudication import Pane5ManualInput


SCHEMA = "paper1.manual-adjudication.pane5-input.v1"
HUMAN_ID = "human:pane5-supervised-adjudicator"


def pointer(value: Any, path: str) -> Any:
    """Resolve the JSON pointer needed to quote the exact report claim."""
    for token in path[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def short_json(value: Any) -> str:
    """Render a bounded exact raw field without using lexical inference."""
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return text if len(text) <= 800 else text[:797] + "..."


def source_refs(item: dict[str, Any], evidence: dict[str, Any]) -> list[dict[str, Any]]:
    """Return the raw and author-source refs that were read for one report."""
    return [
        {"repository_path": item["raw_method_path"], "json_pointer": item["raw_json_pointer"], "line": None, "sha256": item["raw_sha256"]},
        {"repository_path": evidence["author_source"]["nl_path"], "json_pointer": None, "line": None, "sha256": evidence["author_source"]["nl_sha256"]},
        {"repository_path": evidence["author_source"]["plantuml_path"], "json_pointer": None, "line": None, "sha256": evidence["author_source"]["plantuml_sha256"]},
        {"repository_path": "reference/ledger.json", "json_pointer": None, "line": None, "sha256": evidence["ledger_sha256"]},
    ]


def main() -> None:
    """Validate and record an explicit per-report pane5 input."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True, help="JSON file containing explicit Pane5ManualInput rows.")
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    out_dir = archive / "derived" / "manual_adjudication_v2"
    inventory = load(out_dir / "inventory.json")
    ledger = load(archive / "reference/ledger.json")
    supplied = load(args.input.resolve())
    if supplied.get("schema") != "paper1.manual-adjudication.pane5-manual-input.v2":
        raise ValueError("--input must use the explicit pane5-manual-input.v2 schema")
    supplied_rows = [Pane5ManualInput.model_validate(row) for row in supplied.get("rows", [])]
    supplied_by_id = {row.report_id: row for row in supplied_rows}
    if len(supplied_by_id) != len(supplied_rows):
        raise ValueError("--input contains duplicate report IDs")
    rows: list[dict[str, Any]] = []
    for item in inventory["items"]:
        report_id = str(item["report_id"])
        row = supplied_by_id.get(report_id)
        if row is None:
            raise ValueError(f"explicit pane5 input missing for {report_id}")
        if (row.side.value, row.pair_id, row.round, row.raw_method_path, row.raw_json_pointer, row.raw_sha256) != (
            item["side"], item["pair_id"], item["round"], item["raw_method_path"], item["raw_json_pointer"], item["raw_sha256"]
        ):
            raise ValueError(f"explicit pane5 input does not close over inventory: {report_id}")
        evidence = read_evidence(archive, item, row.proposal_submission_hash, ledger)
        if row.evidence_digest != evidence["evidence_digest"]:
            raise ValueError(f"explicit pane5 input evidence digest mismatch: {report_id}")
        rows.append(row.model_dump(mode="json"))
    if set(supplied_by_id) != {str(item["report_id"]) for item in inventory["items"]}:
        raise ValueError("explicit pane5 input has extra or missing report IDs")
    if len({row["report_id"] for row in rows}) != len(inventory["items"]):
        raise ValueError("pane5 input contains duplicate report IDs")
    payload = {
        "schema": "paper1.manual-adjudication.pane5-manual-input.v2",
        "protocol_version": "issue-189-195-manual-evidence-v2",
        "reviewer_id": HUMAN_ID,
        "human_supervised_session": True,
        "human_confirmation": all(row["human_confirmation"] is True for row in rows),
        "raw_source_policy": "Every supplied row was checked after reading and hashing its raw target, author NL, author PlantUML, and ledger closure; proposal labels are never filled or promoted by this recorder.",
        "rows": rows,
    }
    (out_dir / "pane5_adjudications.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PANE5_INPUT", "v60": sum(row["side"] == "v60_current" for row in rows), "x1v2": sum(row["side"] == "x1v2_baseline" for row in rows), "targeted": sum(bool(row.get("targeted_reread")) for row in rows), "provider_calls": 0}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
