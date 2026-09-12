#!/usr/bin/env python3
"""Provider-free validation for the blind Track-A 0020--0039 proposal."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from paper_stm_evaluation.manual_adjudication_v3_baseline_ni import RawFirstProposalEnvelope


PAPER = Path(__file__).resolve().parents[2]
ARCHIVE = PAPER / "final_results" / "v60_current_vs_x1v2_baseline"
PROPOSAL = ARCHIVE / "derived" / "manual_adjudication_v3_baseline_ni" / "proposals" / "track_a_0020_0039.json"


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def enumerate_raw_reports() -> dict[tuple[str, int, int], tuple[Path, dict[str, Any]]]:
    """Enumerate the permitted raw range without consulting any label layer."""

    found: dict[tuple[str, int, int], tuple[Path, dict[str, Any]]] = {}
    for pair_int in range(20, 40):
        pair = f"{pair_int:04d}"
        for raw_path in sorted((ARCHIVE / "raw" / "x1v2_baseline" / "method").glob(f"run*/{pair}-*/record.json")):
            raw_doc = json.loads(raw_path.read_text(encoding="utf-8"))
            round_no = int(raw_doc["round"])
            for finding_index, raw_issue in enumerate(raw_doc["parsed_output"]["issues"]):
                key = (pair, round_no, finding_index)
                if key in found:
                    raise AssertionError(f"duplicate raw identity: {key}")
                found[key] = (raw_path, raw_issue)
    return found


def main() -> None:
    doc = json.loads(PROPOSAL.read_text(encoding="utf-8"))
    model = RawFirstProposalEnvelope.model_validate(doc)
    ledger_path = ARCHIVE / "reference" / "ledger.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))["items"]
    if list(model.ledger.ordered_expected_ids_sha256 for _ in [0]) != [doc["ledger"]["ordered_expected_ids_sha256"]]:
        raise AssertionError("unreachable ledger check")
    if len(ledger) != 145 or model.ledger.expected_count != len(ledger):
        raise AssertionError("ledger count mismatch")
    if sha256(ledger_path) != model.ledger.sha256:
        raise AssertionError("ledger hash mismatch")
    if canonical_sha(list(ledger)) != model.ledger.ordered_expected_ids_sha256:
        raise AssertionError("ledger order hash mismatch")
    if model.scope.get("side") != "x1v2_baseline" or model.scope.get("pair_id_min") != "0020" or model.scope.get("pair_id_max") != "0039":
        raise AssertionError("proposal scope is not exactly baseline pairs 0020..0039")
    if model.forbidden_inputs_read:
        raise AssertionError("forbidden input list is non-empty")
    raw_inventory = enumerate_raw_reports()
    if len(raw_inventory) != len(model.reports):
        raise AssertionError(f"raw/proposal count mismatch: {len(raw_inventory)} != {len(model.reports)}")
    seen: set[str] = set()
    seen_keys: set[tuple[str, int, int]] = set()
    for report in model.reports:
        if report.original_report_id in seen:
            raise AssertionError(f"duplicate report: {report.original_report_id}")
        seen.add(report.original_report_id)
        key = (report.pair_id, report.round, report.finding_index)
        if key in seen_keys:
            raise AssertionError(f"duplicate proposal identity: {key}")
        seen_keys.add(key)
        if key not in raw_inventory:
            raise AssertionError(f"proposal is not backed by enumerated raw finding: {key}")
        expected_raw_path, expected_raw_issue = raw_inventory[key]
        if report.raw_method_path != expected_raw_path.relative_to(ARCHIVE).as_posix():
            raise AssertionError(f"raw path mismatch: {report.original_report_id}")
        if report.raw_json_pointer != f"/parsed_output/issues/{report.finding_index}":
            raise AssertionError(f"raw pointer mismatch: {report.original_report_id}")
        if int(json.loads(expected_raw_path.read_text(encoding="utf-8"))["round"]) != report.round:
            raise AssertionError(f"round mismatch: {report.original_report_id}")
        raw_path = ARCHIVE / report.raw_method_path
        raw_doc = json.loads(raw_path.read_text(encoding="utf-8"))
        raw_issue = raw_doc["parsed_output"]["issues"][report.finding_index]
        if report.raw_text.model_dump(mode="json") != {"issue": raw_issue.get("issue", ""), "where": raw_issue.get("where", ""), "reason": raw_issue.get("reason", ""), "basis": raw_issue.get("basis")}:
            raise AssertionError(f"raw text mismatch: {report.original_report_id}")
        if sha256(raw_path) != report.raw_sha256 or sha256(raw_path) != report.source_artifact_digest.raw_sha256:
            raise AssertionError(f"raw hash mismatch: {report.original_report_id}")
        if report.observed_source_fact_status.value == "REFUTED" and report.a0_type.value != "FALSE_POSITIVE":
            raise AssertionError(f"baseline A0 subtype is not FALSE_POSITIVE: {report.original_report_id}")
        if report.observed_source_fact_status.value == "ESTABLISHED" and report.a0_type is not None:
            raise AssertionError(f"established fact carries A0 subtype: {report.original_report_id}")
        for text_field in (report.observed_fact, report.reason, report.basis):
            if report.original_report_id not in text_field:
                raise AssertionError(f"non-dedicated proposal text: {report.original_report_id}")
        ref_paths = {ref.repository_path for ref in report.source_refs}
        expected_source_paths = {
            report.raw_method_path,
            f"reference/x1v2_input_closure/pairs/{report.pair_id}/nl.txt",
            f"reference/x1v2_input_closure/pairs/{report.pair_id}/plantuml.puml",
        }
        if not expected_source_paths.issubset(ref_paths):
            raise AssertionError(f"source closure refs incomplete: {report.original_report_id}")
        for ref in report.source_refs:
            ref_path = ARCHIVE / ref.repository_path
            if not ref_path.exists():
                raise AssertionError(f"source ref does not exist: {report.original_report_id} {ref.repository_path}")
            if sha256(ref_path) != ref.sha256:
                raise AssertionError(f"source ref hash mismatch: {report.original_report_id} {ref.repository_path}")
        if report.relation_digest.ordered_expected_ids != tuple(ledger):
            raise AssertionError(f"expected order mismatch: {report.original_report_id}")
        positive = {row.expected_id: row.relation.value for row in report.relation_digest.positive_rows}
        rows = []
        for expected_id in ledger:
            relation = positive.get(expected_id, "NO_MATCH")
            if relation == "NO_MATCH":
                reason = f"{report.original_report_id}: no positive relation proposed for {expected_id} in this blind raw-first pass; the complete dense row remains NO_MATCH by explicit review mapping."
            else:
                reason = f"{report.original_report_id}: the report's source-located claim is materially related to {expected_id} after reading the full author source and the ledger statement; relation is {relation}."
            rows.append({"expected_id": expected_id, "relation": relation, "reason": reason, "basis": f"{report.raw_method_path}#/parsed_output/issues/{report.finding_index}; {report.source_refs[1].repository_path}; {report.source_refs[2].repository_path}; reference/ledger.json#/items/{expected_id}; ledger_sha256={model.ledger.sha256}"})
        if canonical_sha(rows) != report.relation_digest.rows_sha256:
            raise AssertionError(f"dense relation digest mismatch: {report.original_report_id}")
        if set(report.positive_expected_ids) != set(positive):
            raise AssertionError(f"positive expected ID closure mismatch: {report.original_report_id}")
        if report.d_tier.value in {"D0", "A0"} and positive:
            raise AssertionError(f"invalid proposal has positive relation: {report.original_report_id}")
    if seen_keys != set(raw_inventory):
        raise AssertionError("proposal identities do not exactly close over raw inventory")
    if len(model.reports) != model.coverage.raw_candidate_reports:
        raise AssertionError("coverage mismatch")
    if model.coverage.dedicated_proposals != len(model.reports):
        raise AssertionError("dedicated proposal coverage mismatch")
    if model.coverage.all_145_relation_digests is not True:
        raise AssertionError("not every proposal has a 145-row digest")
    if tuple(model.coverage.missing_pair_ids_without_raw_reports) != ("0028", "0038"):
        raise AssertionError("missing pair coverage is not the raw-enumerated result")
    if model.generation.get("provider_calls") != 0 or model.generation.get("method_calls") != 0 or model.generation.get("judge_calls") != 0:
        raise AssertionError("proposal generation records a forbidden call")
    print(json.dumps({"status": "PASS", "reports": len(model.reports), "expected_rows_per_report": 145, "provider_calls": 0, "missing_pairs": list(model.coverage.missing_pair_ids_without_raw_reports), "non_k_target_reports": model.coverage.non_k_target_reports}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
