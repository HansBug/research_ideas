"""Validate the blind Track A proposal without provider or legacy labels."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "evaluation" / "src"
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from paper_stm_evaluation.track_a_baseline_ni_proposal import TrackAProposal


def sha256_file(path: Path) -> str:
    """Hash one frozen artifact."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def canonical_digest(value: object) -> str:
    """Hash a canonical JSON value."""

    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def load(path: Path) -> Any:
    """Read JSON from a known local path."""

    return json.loads(path.read_text(encoding="utf-8"))


def validate(archive: Path, proposal_path: Path, inventory_path: Path) -> dict[str, Any]:
    """Run all provider-free closure checks for this proposal batch."""

    proposal_raw = load(proposal_path)
    proposal = TrackAProposal.model_validate(proposal_raw)
    inventory = load(inventory_path)
    ledger = load(archive / "reference" / "ledger.json")
    expected_ids = tuple(ledger["items"])
    expected_count = len(expected_ids)
    inventory_by_key = {
        (item["raw_method_path"], item["report_index"]): item
        for item in inventory["items"]
        if item["side"] == "x1v2_baseline"
    }
    errors: list[str] = []
    seen: set[str] = set()
    expected_keys = {
        (item["raw_method_path"], item["report_index"])
        for item in inventory["items"]
        if item["side"] == "x1v2_baseline" and 0 <= int(item["pair_id"]) <= 19
    }
    actual_keys: set[tuple[str, int]] = set()
    for report in proposal.reports:
        if report.report_id in seen:
            errors.append(f"duplicate report_id: {report.report_id}")
        seen.add(report.report_id)
        key = (report.raw.method_record_path, report.finding_index)
        actual_keys.add(key)
        if key not in inventory_by_key:
            errors.append(f"inventory closure missing: {key}")
            continue
        raw_path = archive / report.raw.method_record_path
        raw_record = load(raw_path)
        raw_finding = raw_record["parsed_output"]["issues"][report.finding_index]
        inventory_item = inventory_by_key[key]
        if report.report_id != inventory_item["report_id"]:
            errors.append(f"report identity mismatch: {report.report_id}")
        # Baseline raw records retain the producer name in ``pair_id``
        # (for example ``llms_emp_feedback_final_0000``), while the proposal
        # uses the canonical four-digit pair token.  Compare the stable
        # suffix rather than treating the producer prefix as a mismatch.
        raw_pair_id = str(raw_record.get("pair_id", ""))
        if raw_pair_id.rsplit("_", 1)[-1] != report.pair_id:
            errors.append(f"raw pair mismatch: {report.report_id}")
        if report.round != int(raw_record.get("round")):
            errors.append(f"raw round mismatch: {report.report_id}")
        expected_json_pointer = f"/parsed_output/issues/{report.finding_index}"
        if report.raw.json_pointer != expected_json_pointer:
            errors.append(f"raw JSON pointer mismatch: {report.report_id}")
        if report.raw.claim_pointer != f"{expected_json_pointer}/issue":
            errors.append(f"claim pointer mismatch: {report.report_id}")
        if report.raw.where_pointer != f"{expected_json_pointer}/where":
            errors.append(f"where pointer mismatch: {report.report_id}")
        expected_nl = f"reference/x1v2_input_closure/pairs/{report.pair_id}/nl.txt"
        expected_plantuml = f"reference/x1v2_input_closure/pairs/{report.pair_id}/plantuml.puml"
        if report.author_source.nl_path != expected_nl:
            errors.append(f"NL path mismatch: {report.report_id}")
        if report.author_source.plantuml_path != expected_plantuml:
            errors.append(f"PlantUML path mismatch: {report.report_id}")
        if not report.author_source.full_files_read:
            errors.append(f"complete source read not attested: {report.report_id}")
        for field in ("issue", "where", "reason", "basis"):
            if report.raw.model_dump()[field] != raw_finding.get(field):
                errors.append(f"raw text mismatch: {report.report_id}/{field}")
        if report.raw.raw_sha256 != sha256_file(raw_path):
            errors.append(f"raw hash mismatch: {report.report_id}")
        if report.author_source.nl_sha256 != sha256_file(archive / report.author_source.nl_path):
            errors.append(f"NL hash mismatch: {report.report_id}")
        if report.author_source.plantuml_sha256 != sha256_file(archive / report.author_source.plantuml_path):
            errors.append(f"PlantUML hash mismatch: {report.report_id}")
        rows = report.relation_proposal.rows
        if report.relation_proposal.expected_count != expected_count:
            errors.append(f"ledger expected count mismatch: {report.report_id}")
        if tuple(row.expected_id for row in rows) != expected_ids:
            errors.append(f"ledger ID/order mismatch: {report.report_id}")
        if any(row.ledger_json_pointer != f"/items/{row.expected_id}" for row in rows):
            errors.append(f"ledger pointer mismatch: {report.report_id}")
        values = [{"expected_id": row.expected_id, "relation": row.relation} for row in rows]
        if canonical_digest(values) != report.relation_proposal.canonical_value_digest:
            errors.append(f"relation digest mismatch: {report.report_id}")
        if report.d_a_proposal.d_tier in {"D0", "A0"} and any(row.relation != "NO_MATCH" for row in rows):
            errors.append(f"non-defect proposal has positive relation: {report.report_id}")
    if actual_keys != expected_keys:
        errors.append(f"raw candidate key closure mismatch: expected={len(expected_keys)} actual={len(actual_keys)}")
    if proposal.scope.raw_candidate_count != len(expected_keys):
        errors.append("scope candidate count does not match raw pair-range enumeration")
    if proposal.scope.scope_gate != "OPEN_EVIDENCE_GAP":
        errors.append("scope gate must remain OPEN_EVIDENCE_GAP for this blind proposal")
    if proposal.scope.preexisting_non_k_membership_available_from_allowed_inputs:
        errors.append("proposal must not claim historical non-K membership from blind inputs")
    if proposal.coverage.reports_with_missing_annotations:
        errors.append("missing explicit annotations remain")
    if proposal.coverage.reports_with_145_relation_rows != len(proposal.reports):
        errors.append("not all reports are densely closed")
    return {
        "status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "errors": errors,
        "reports": len(proposal.reports),
        "unique_report_ids": len(seen),
        "expected_per_report": expected_count,
        "raw_candidate_keys": len(expected_keys),
        "scope_gate": proposal.scope.scope_gate,
        "preexisting_non_k_membership_available_from_allowed_inputs": proposal.scope.preexisting_non_k_membership_available_from_allowed_inputs,
        "provider_called": False,
        "legacy_label_inputs_read": False,
    }


def main() -> None:
    """Run the validator and return a machine-readable result."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--proposal", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    args = parser.parse_args()
    result = validate(args.archive_root.resolve(), args.proposal.resolve(), args.inventory.resolve())
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
