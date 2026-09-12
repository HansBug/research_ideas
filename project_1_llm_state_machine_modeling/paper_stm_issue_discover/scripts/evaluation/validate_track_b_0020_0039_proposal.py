#!/usr/bin/env python3
"""Provider-free closure validator for Track-B pairs 0020--0039.

This validator reads the Track-B artifact only after it has been materialized;
its input closure for rechecking is limited to raw records, author NL/
PlantUML, the frozen ledger, and the named protocol files.  It does not read
any adjudication, proposal, or Judge-label artifact.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PAPER = Path(__file__).resolve().parents[2]
ARCHIVE = PAPER / "final_results" / "v60_current_vs_x1v2_baseline"
PROPOSAL = ARCHIVE / "derived" / "manual_adjudication_v3_baseline_ni" / "proposals" / "track_b_0020_0039.json"
LEDGER = ARCHIVE / "reference" / "ledger.json"


def sha256(path: Path) -> str:
    """Return a prefixed byte hash."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: object) -> str:
    """Hash the archive's deterministic JSON representation."""

    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def resolve_ref(repository_path: str) -> Path:
    """Resolve one archive-relative or repository-relative evidence path."""

    archive_path = ARCHIVE / repository_path
    if archive_path.exists():
        return archive_path
    return PAPER / repository_path


def main() -> None:
    """Validate identity, raw text, hash closure, and 145-row relations."""

    doc = json.loads(PROPOSAL.read_text(encoding="utf-8"))
    assert doc["schema"] == "paper1.manual-adjudication.v3-baseline-ni.track-b-proposal.v1"
    assert doc["proposal_status"] == "PROPOSAL_ONLY"
    blind = doc["blindness"]
    assert blind["raw_first"] is True
    assert blind["v2_decisions_read"] is False
    assert blind["v3_decisions_read"] is False
    assert blind["track_a_read"] is False
    assert blind["other_reviewer_conclusions_read"] is False
    assert blind["judge_labels_read"] is False
    assert blind["provider_calls"] == blind["method_reruns"] == blind["judge_reruns"] == 0

    ledger_doc = json.loads(LEDGER.read_text(encoding="utf-8"))
    ledger_ids = list(ledger_doc["items"])
    assert len(ledger_ids) == 145
    assert doc["ledger"]["expected_count"] == 145
    assert doc["ledger"]["sha256"] == sha256(LEDGER)
    assert doc["ledger"]["ordered_expected_ids"] == ledger_ids
    assert doc["ledger"]["ordered_expected_ids_sha256"] == canonical_sha(ledger_ids)
    for ref in doc["protocol_refs"]:
        protocol_path = resolve_ref(ref["repository_path"])
        assert protocol_path.exists(), ref["repository_path"]
        assert ref["sha256"] == sha256(protocol_path), ref["repository_path"]

    expected_reports: dict[tuple[str, int, int], tuple[Path, dict[str, object]]] = {}
    for pair_int in range(20, 40):
        pair = f"{pair_int:04d}"
        record_paths = sorted((ARCHIVE / "raw/x1v2_baseline/method").glob(f"run*/{pair}-*/record.json"))
        for record_path in record_paths:
            record = json.loads(record_path.read_text(encoding="utf-8"))
            for finding_index, finding in enumerate(record["parsed_output"]["issues"]):
                key = (pair, int(record["round"]), finding_index)
                if key in expected_reports:
                    raise AssertionError(f"duplicate raw identity: {key}")
                expected_reports[key] = (record_path, finding)

    reports = doc["reports"]
    assert len(expected_reports) == 205
    assert len(reports) == len(expected_reports)
    actual_keys = {(item["pair_id"], item["round"], item["finding_index"]) for item in reports}
    assert actual_keys == set(expected_reports)

    seen_ids: set[str] = set()
    for item in reports:
        key = (item["pair_id"], item["round"], item["finding_index"])
        record_path, finding = expected_reports[key]
        report_id = f"{item['pair_id']}:r{item['round']}:baseline_issue_{item['finding_index'] + 1}"
        assert item["original_report_id"] == report_id
        assert report_id not in seen_ids
        seen_ids.add(report_id)
        assert item["raw_method_path"] == record_path.relative_to(ARCHIVE).as_posix()
        assert item["raw_json_pointer"] == f"/parsed_output/issues/{item['finding_index']}"
        assert item["raw_sha256"] == sha256(record_path)
        assert item["raw_text"] == {field: finding.get(field, "") if field != "basis" else finding.get(field) for field in ("issue", "where", "reason", "basis")}

        rows = item["relation_rows"]
        assert len(rows) == 145
        assert [row["expected_id"] for row in rows] == ledger_ids
        assert len({row["expected_id"] for row in rows}) == 145
        assert item["relation_digest_sha256"] == canonical_sha(rows)
        dense_positive = {row["expected_id"]: row["relation"] for row in rows if row["relation"] != "NO_MATCH"}
        evidence_positive = {row["expected_id"]: row["relation"] for row in item["positive_relations"]}
        assert dense_positive == evidence_positive
        assert item["provider_calls"] == 0
        for ref in item["source_refs"]:
            ref_path = resolve_ref(ref["repository_path"])
            assert ref_path.exists(), ref["repository_path"]
            assert ref["sha256"] == sha256(ref_path), ref["repository_path"]

        tier = item["d_tier"]
        if tier == "A0":
            assert item["observed_source_fact_status"] == "REFUTED"
            assert item["a0_type"] == "FALSE_POSITIVE"
        else:
            assert item["observed_source_fact_status"] == "ESTABLISHED"
            assert item["a0_type"] is None
        if tier in {"D0", "A0"}:
            assert item["normative_violation_status"] == "NOT_ESTABLISHED"
            assert not dense_positive
            assert item["validity_proposal"] == "INVALID"
        else:
            assert item["normative_violation_status"] == "ESTABLISHED"
            assert item["validity_proposal"] == ("VALID_KNOWN" if dense_positive else "VALID_NOVEL")

    assert doc["scope"]["missing_pair_ids"] == ["0028", "0038"]
    assert doc["scope"]["current_non_k_membership"] == "UNRESOLVED_BLIND_SCOPE"
    assert doc["scope"]["current_non_k_coverage"] == "NOT_ASSERTED"
    assert doc["coverage"]["reports_enumerated"] == 205
    assert doc["coverage"]["reports_with_dedicated_opinion"] == 205
    assert doc["coverage"]["reports_with_145_relation_rows"] == 205
    print(json.dumps({"status": "PASS", "reports": 205, "expected_rows_per_report": 145, "source_pairs_read": 18, "missing_pairs": ["0028", "0038"], "provider_calls": 0, "non_k_membership_asserted": False}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
