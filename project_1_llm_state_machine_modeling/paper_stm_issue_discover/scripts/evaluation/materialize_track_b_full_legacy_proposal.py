#!/usr/bin/env python3
"""Normalize the archived blind baseline proposal into the v3 proposal schema.

The source file is proposal evidence only.  This adapter deliberately removes
the historical validity/K/N/I fields and retains only the raw identity, the
proposal D/A, the complete relation rows, and the source/hash provenance.  It
does not read the v3 decision layer and does not make a new semantic judgment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "paper1.manual-adjudication-raw-first-proposal.v3-baseline-ni.track-b-full"
PROTOCOL = "issue-189-195-baseline-ni-v3"
REVIEWER = "subagent:raw-first-independent-proposal"


def sha256(path: Path) -> str:
    """Return a prefixed SHA-256 digest for one file."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> Any:
    """Read one UTF-8 JSON artifact."""

    return json.loads(path.read_text(encoding="utf-8"))


def normalize_ref(value: dict[str, Any]) -> dict[str, Any]:
    """Retain only the stable fields required by the v3 source-ref contract."""

    path = value.get("repository_path") or value.get("path")
    return {
        "repository_path": str(path),
        "json_pointer": value.get("json_pointer") or value.get("pointer"),
        "line": value.get("line"),
        "sha256": value["sha256"],
    }


def build(archive: Path, output: Path) -> dict[str, Any]:
    """Build a proposal-only Track B artifact from the archived blind proposal."""

    source_path = archive / "derived" / "manual_adjudication_v2" / "proposals" / "x1v2_report_proposals.json"
    source = load(source_path)
    if source.get("schema") != "paper1.manual-adjudication.v2" or source.get("side") != "x1v2_baseline":
        raise ValueError("unexpected archived proposal source")
    source_rows = source.get("decisions", [])
    if len(source_rows) != 512:
        raise ValueError(f"expected 512 archived proposal rows, found {len(source_rows)}")

    ledger_path = archive / "reference" / "ledger.json"
    ledger_items = load(ledger_path)["items"]
    ledger = list(ledger_items)
    if len(ledger) != 145 or len(set(ledger)) != 145:
        raise ValueError("ledger is not the expected 145-item ordered list")

    records: list[dict[str, Any]] = []
    for old in source_rows:
        review = old.get("review", {})
        if review.get("human_confirmation") is not False or review.get("reference_visible") is not False or review.get("primary_visible") is not False:
            raise ValueError(f"archived proposal is not blind proposal-only evidence: {old.get('report_id')}")
        if review.get("independent_is_subagent_proposal") is not True:
            raise ValueError(f"archived row is not marked as a subagent proposal: {old.get('report_id')}")
        if old.get("strict_da") not in {"D2", "D1", "D0", "A0"}:
            raise ValueError(f"missing proposal D/A: {old.get('report_id')}")
        if old.get("a0_type") not in {None, "FALSE_POSITIVE"}:
            raise ValueError(f"baseline proposal has an invalid A0 subtype: {old.get('report_id')}")
        relation_rows = old.get("relations", [])
        relation_by_id = {row.get("expected_id"): row for row in relation_rows}
        if len(relation_rows) != 145 or set(relation_by_id) != set(ledger):
            raise ValueError(f"relation closure mismatch: {old.get('report_id')}")
        relations = [relation_by_id[expected_id] for expected_id in ledger]
        raw_path = archive / old["raw_method_path"]
        raw_doc = load(raw_path)
        raw_issue = raw_doc["parsed_output"]["issues"][old["report_index"]]
        raw_pointer = f"/parsed_output/issues/{old['report_index']}"
        if old["raw_json_pointer"] != raw_pointer:
            raise ValueError(f"raw pointer is not the canonical issue pointer: {old.get('report_id')}")
        raw_text = {
            "issue": raw_issue.get("issue", ""),
            "where": raw_issue.get("where", ""),
            "reason": raw_issue.get("reason", ""),
            "basis": raw_issue.get("basis"),
        }
        if sha256(raw_path) != old["raw_sha256"]:
            raise ValueError(f"raw hash mismatch in archived proposal: {old.get('report_id')}")
        records.append({
            "proposal_status": "PROPOSAL",
            "reviewer_id": REVIEWER,
            "side": "x1v2_baseline",
            "pair_id": old["pair_id"],
            "round": old["round"],
            "original_report_id": old["report_id"],
            "finding_index": old["report_index"],
            "raw_method_path": old["raw_method_path"],
            "raw_json_pointer": old["raw_json_pointer"],
            "raw_sha256": old["raw_sha256"],
            "raw_text": raw_text,
            "observed_source_fact_status": "REFUTED" if old["strict_da"] == "A0" else "ESTABLISHED",
            "d_tier": old["strict_da"],
            "a0_type": old.get("a0_type"),
            "normative_violation_status": "NOT_ESTABLISHED" if old["strict_da"] in {"D0", "A0"} else "ESTABLISHED",
            "source_loci": [old.get("witness", {}).get("concrete_location", "raw report locus")],
            "source_refs": [normalize_ref(ref) for ref in old.get("source_refs", [])],
            "relations": relations,
            "reason": old["reason"],
            "basis": old["basis"],
            "reference_visible": False,
            "primary_visible": False,
            "human_confirmation": False,
            "provider_calls": 0,
        })

    records.sort(key=lambda row: (row["pair_id"], row["round"], row["finding_index"]))
    return {
        "schema": SCHEMA,
        "protocol_version": PROTOCOL,
        "proposal_status": "PROPOSAL_ONLY",
        "reviewer_id": REVIEWER,
        "scope": {"side": "x1v2_baseline", "pair_id_min": "0000", "pair_id_max": "0059", "raw_candidate_report_count": len(records), "target_filter": "v3 builder selects the frozen non-K IDs only after blind proposal submission"},
        "input_allowlist": ["archived blind proposal evidence", "reference/ledger.json", "raw/source hashes carried by that proposal"],
        "forbidden_inputs_read": ["v3 canonical decisions", "v3 pane5 register", "current labels", "Track A proposals"],
        "source_proposal": {"repository_path": source_path.relative_to(archive).as_posix(), "sha256": sha256(source_path), "human_confirmation": False, "provider_calls": 0},
        "ledger": {"repository_path": ledger_path.relative_to(archive).as_posix(), "sha256": sha256(ledger_path), "expected_count": 145, "ordered_expected_ids": ledger},
        "coverage": {"records": len(records), "all_512_baseline_proposal_rows": True, "all_145_relations_per_record": True, "old_kni_fields_removed": True, "provider_calls": 0},
        "records": records,
    }


def main() -> None:
    """Write the normalized proposal artifact."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = build(args.archive_root.resolve(), args.output.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "records": len(payload["records"]), "relations_per_record": 145, "provider_calls": 0}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
