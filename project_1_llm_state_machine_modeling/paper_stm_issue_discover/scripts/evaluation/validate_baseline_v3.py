"""Provider-free validation gates for the X1v2 baseline v3 layer."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from paper_stm_evaluation.manual_adjudication_v3_baseline_ni import (
    arbitration_record_pointer,
    DecisionSetV3,
    GroupSetV3,
    Pane5RegisterV3,
    canonical_json_sha256,
)
from recompute_baseline_v3_summary import project_metrics


def load(path: Path) -> Any:
    """Load UTF-8 JSON."""
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    """Hash one file using the archive prefix convention."""
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def raw_inventory(archive: Path) -> dict[str, dict[str, Any]]:
    """Enumerate all baseline reports directly from frozen raw records."""
    result: dict[str, dict[str, Any]] = {}
    for record_path in sorted((archive / "raw/x1v2_baseline/method").glob("run*/*/record.json")):
        run = int(record_path.parts[-3].removeprefix("run"))
        pair = record_path.parts[-2].split("-", 1)[0]
        document = load(record_path)
        for index, issue in enumerate(document.get("parsed_output", {}).get("issues", [])):
            rid = f"{pair}:r{run}:baseline_issue_{index + 1}"
            if rid in result:
                raise ValueError(f"duplicate raw report {rid}")
            result[rid] = {"pair_id": pair, "round": run, "finding_index": index, "path": str(record_path.relative_to(archive)), "pointer": f"/parsed_output/issues/{index}", "sha256": sha256(record_path), "issue": issue}
    return result


def frozen_k_projection(row: dict[str, Any]) -> dict[str, Any]:
    """Select every field that must remain byte-for-byte semantically frozen."""
    return {key: row[key] for key in ("report_id", "raw_method_path", "raw_json_pointer", "raw_sha256", "corrected_kni", "strict_da", "reason", "basis", "source_refs", "relations", "ledger_ids", "witness", "canonical_group_key")}


def validate_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Compare every TSV scalar/nested field with the canonical JSON row."""
    # Relation/source columns contain complete JSON vectors and can exceed the
    # csv module's conservative 128 KiB default field limit.
    csv.field_size_limit(max(csv.field_size_limit(), 16 * 1024 * 1024))
    with path.open(encoding="utf-8", newline="") as handle:
        tsv_rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(tsv_rows) != len(rows) or set(tsv_rows[0]) != set(rows[0]):
        raise ValueError("TSV shape does not mirror canonical decision fields")
    for source, encoded in zip(rows, tsv_rows):
        for key, value in source.items():
            expected = "" if value is None else json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) if isinstance(value, (dict, list, tuple)) else str(value)
            if encoded[key] != expected:
                raise ValueError(f"TSV mismatch at {source['original_report_id']}/{key}")


def normalized_k(row: dict[str, Any]) -> dict[str, Any]:
    """Project one combined row to the immutable frozen-K contract."""

    return {
        key: row[key]
        for key in ("report_id", "pair_id", "round", "validity", "corrected_kni", "d_tier", "witness", "relations")
    }


def main() -> None:
    """Run all deterministic v3 closure checks."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-root", type=Path, required=True)
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    v3 = archive / "derived/manual_adjudication_v3_baseline_ni"
    raw = raw_inventory(archive)
    if len(raw) != 512:
        raise ValueError(f"raw report count is {len(raw)}, expected 512")
    cell_paths = sorted((archive / "raw/x1v2_baseline/method").glob("run*/*/record.json"))
    if len(cell_paths) != 162:
        raise ValueError("raw cell count is not 162")
    by_round = Counter(row["round"] for row in raw.values())
    if by_round != Counter({1: 173, 2: 163, 3: 176}):
        raise ValueError(f"raw round distribution changed: {by_round}")

    old = load(archive / "derived/manual_adjudication_v2/x1v2_report_decisions.json")["decisions"]
    old_by_id = {row["report_id"]: row for row in old}
    if set(old_by_id) != set(raw):
        raise ValueError("raw and frozen v2 report identities differ")
    for rid, raw_row in raw.items():
        old_row = old_by_id[rid]
        if (old_row["raw_method_path"], old_row["raw_json_pointer"], old_row["raw_sha256"]) != (raw_row["path"], raw_row["pointer"], raw_row["sha256"]):
            raise ValueError(f"raw pointer/hash mismatch for {rid}")

    decision_document = load(v3 / "baseline_report_decisions_v3.json")
    decision_set = DecisionSetV3.model_validate(decision_document)
    decisions = [row.model_dump(mode="json") for row in decision_set.decisions]
    if len(decisions) != 233 or set(row["original_report_id"] for row in decisions) != {rid for rid, old_row in old_by_id.items() if old_row["corrected_kni"] != "K"}:
        raise ValueError("v3 non-K decision coverage is not exactly the frozen 233-row set")
    arbitration_log = load(v3 / "reviews/arbitration_log_v3.json")
    arbitration_entries = arbitration_log.get("entries_by_report_id", {})
    if arbitration_log.get("entry_count") != 233 or set(arbitration_entries) != {row["original_report_id"] for row in decisions}:
        raise ValueError("v3 arbitration log does not close over all 233 decisions")
    for index, row in enumerate(decisions):
        rid = row["original_report_id"]
        raw_row = raw[rid]
        if row["raw_sha256"] != raw_row["sha256"] or row["raw_method_path"] != raw_row["path"] or row["raw_json_pointer"] != raw_row["pointer"]:
            raise ValueError(f"v3 raw provenance mismatch for {rid}")
        if len(row["relations"]) != 145 or {x["expected_id"] for x in row["relations"]} != set(load(archive / "reference/ledger.json")["items"]):
            raise ValueError(f"v3 relation closure failed for {rid}")
        reviewers = row["review"]["independent_reviewer_ids"]
        if len(reviewers) < 2 or len(set(reviewers)) != len(reviewers) or any("manual-v2" in reviewer for reviewer in reviewers):
            raise ValueError(f"non-independent review chain for {rid}")
        if not row["review"]["human_confirmation"] or row["review"]["final_adjudicator_id"] != "human:pane5-supervised-adjudicator":
            raise ValueError(f"human confirmation missing for {rid}")
        for opinion in row["review"]["independent_opinions"]:
            if opinion["review_status"] != "PROPOSAL" or opinion["reference_visible"] or opinion["primary_visible"]:
                raise ValueError(f"independent opinion was not blind for {rid}")
        expected_pointer = arbitration_record_pointer(rid)
        if row["review"]["arbitration_record_pointer"] != expected_pointer:
            raise ValueError(f"arbitration pointer mismatch for {rid}")
        entry = arbitration_entries[rid]
        if entry.get("record_pointer") != expected_pointer or entry.get("decision_json_pointer") != f"/decisions/{index}":
            raise ValueError(f"arbitration log entry mismatch for {rid}")

    # The pane5 register and its evidence-read envelope are canonical inputs,
    # rather than a narrative copy of the decision file.
    register = Pane5RegisterV3.model_validate(load(v3 / "pane5_adjudications_v3.json"))
    if register.source_evidence_sha256 != sha256(v3 / "pane5_evidence_reads_v3.json"):
        raise ValueError("pane5 evidence digest does not match register")
    evidence = load(v3 / "pane5_evidence_reads_v3.json")
    if evidence.get("raw_report_count") != 512 or evidence.get("reviewed_non_k_count") != 233 or evidence.get("ledger_item_count") != 145:
        raise ValueError("pane5 evidence-read counts do not close")
    if not evidence.get("human_confirmation") or evidence.get("provider_calls") != 0 or evidence.get("method_reruns") != 0 or evidence.get("judge_reruns") != 0:
        raise ValueError("pane5 evidence envelope has invalid confirmation or call counters")
    if len(evidence.get("records", [])) != 233:
        raise ValueError("pane5 evidence-read record count is not 233")
    evidence_ids = {row["report_id"] for row in evidence["records"]}
    decision_ids = {row["original_report_id"] for row in decisions}
    if evidence_ids != decision_ids:
        raise ValueError("pane5 evidence-read IDs do not match decisions")
    register_by_id = {row.report_id: row for row in register.rows}
    for row in decisions:
        reg = register_by_id[row["original_report_id"]]
        if (reg.d_tier.value, reg.validity.value, reg.corrected_kni) != (row["d_tier"], row["validity"], row["corrected_kni"]):
            raise ValueError(f"pane5 register semantic projection mismatch for {row['original_report_id']}")
        if [(x.expected_id, x.relation.value) for x in reg.relations] != [(x["expected_id"], x["relation"]) for x in row["relations"]]:
            raise ValueError(f"pane5 register relation projection mismatch for {row['original_report_id']}")

    frozen_k = {rid: frozen_k_projection(row) for rid, row in old_by_id.items() if row["corrected_kni"] == "K"}
    snapshot = load(v3 / "frozen_k_snapshot_v3.json")
    snapshot_rows = {row["report_id"]: row for row in snapshot["rows"]}
    if len(frozen_k) != 279 or snapshot_rows != {rid: old_by_id[rid] for rid in frozen_k}:
        raise ValueError("frozen K snapshot is not an exact copy of v2 K rows")
    if canonical_json_sha256(snapshot["rows"]) != snapshot["snapshot_projection_sha256"]:
        raise ValueError("frozen K snapshot digest is incorrect")
    combined = load(v3 / "baseline_combined_512_v3.json")["rows"]
    combined_k = {row["report_id"]: normalized_k(row) for row in combined if row.get("source") == "frozen_v2"}
    old_k_normalized = {
        rid: {
            "report_id": row["report_id"], "pair_id": row["pair_id"], "round": row["round"],
            "validity": row["validity"], "corrected_kni": row["corrected_kni"], "d_tier": row["strict_da"],
            "witness": row["witness"], "relations": row["relations"],
        }
        for rid, row in old_by_id.items() if row["corrected_kni"] == "K"
    }
    if combined_k != old_k_normalized:
        raise ValueError("combined output changed the frozen v2 K projection")
    if any("track_b_full" in json.dumps(row, ensure_ascii=False) or "track_b_0020_0059" in json.dumps(row, ensure_ascii=False) for row in decisions):
        raise ValueError("forbidden full/broad Track-B artifact leaked into final decisions")
    dense = load(v3 / "baseline_relation_decisions_v3.json")["rows"]
    if len(dense) != 233 * 145 or len({(row["report_id"], row["expected_id"]) for row in dense}) != len(dense):
        raise ValueError("dense v3 relation projection does not close")
    group_document = load(v3 / "baseline_n_groups_v3.json")
    group_set = GroupSetV3.model_validate(group_document["groups"])
    final_n = {row["original_report_id"] for row in decisions if row["corrected_kni"] == "N"}
    final_i = {row["original_report_id"] for row in decisions if row["corrected_kni"] == "I"}
    decision_by_id = {row["original_report_id"]: row for row in decisions}
    expected_map = group_set.report_to_group
    if set(expected_map) != final_n | final_i or len(expected_map) != len(final_n | final_i):
        raise ValueError("N/I report-to-group mapping is not one-to-one")
    n_members = {rid for group in group_set.n_groups for rid in group.member_report_ids}
    i_members = {rid for group in group_set.invalid_clusters for rid in group.member_report_ids}
    if n_members != final_n or i_members != final_i or n_members & i_members:
        raise ValueError("group membership does not close over final N/I")
    for group in tuple(group_set.n_groups) + tuple(group_set.invalid_clusters):
        rounds = set()
        for report_id in group.member_report_ids:
            decision = decision_by_id.get(report_id)
            if decision is None:
                raise ValueError(f"group member is absent from canonical decisions: {report_id}")
            expected_kni = "N" if group.group_kind.value == "SUBSTANTIVE_N" else "I"
            if decision["pair_id"] != group.pair_id or decision["side"] != group.side or decision["corrected_kni"] != expected_kni:
                raise ValueError(f"group member crosses a decision boundary: {group.group_id}/{report_id}")
            rounds.add(decision["round"])
            expected_refs = {
                (ref["repository_path"], ref.get("json_pointer"), ref.get("line"), ref["sha256"])
                for ref in decision["source_refs"]
            }
            actual_refs = {
                (ref.repository_path, ref.json_pointer, ref.line, ref.sha256)
                for ref in group.member_source_refs[report_id]
            }
            if expected_refs != actual_refs:
                raise ValueError(f"group member source refs differ from canonical decision: {group.group_id}/{report_id}")
            for ref in group.member_source_refs[report_id]:
                ref_path = archive / ref.repository_path
                if not ref_path.exists() or sha256(ref_path) != ref.sha256:
                    raise ValueError(f"group source ref is missing or hash-invalid: {group.group_id}/{ref.repository_path}")
        if hasattr(group, "cross_round_merge") and group.cross_round_merge != (len(rounds) > 1):
            raise ValueError(f"group cross-round flag differs from decisions: {group.group_id}")
    validate_tsv(v3 / "baseline_report_decisions_v3.tsv", decisions)

    projection = load(v3 / "baseline_relation_projection_v3.json")["rows"]
    projection_by_key = {(row["report_id"], row["expected_id"]): row["relation"] for row in projection}
    combined_by_key = {
        (report["report_id"], relation["expected_id"]): relation["relation"]
        for report in combined
        for relation in report["relations"]
    }
    if len(projection) != 512 * 145 or len(projection_by_key) != 512 * 145:
        raise ValueError("full relation projection does not close")
    if projection_by_key != combined_by_key:
        raise ValueError("full relation projection differs from combined canonical rows")

    ledger = load(archive / "reference/ledger.json")
    cost = load(archive / "derived/manual_adjudication_v2/summary.json")["sides"]["x1v2_baseline"]["cost"]
    expected_metrics = project_metrics(
        combined,
        ledger,
        len(group_set.n_groups),
        len(group_set.invalid_clusters),
        len(final_i),
        cost,
    )
    for summary_name in ("summary_v3.json", "recomputed_summary_v3.json"):
        summary = load(v3 / summary_name)
        if summary.get("metrics") != expected_metrics:
            raise ValueError(f"{summary_name} does not match provider-free canonical recomputation")
    print(json.dumps({"status": "PASS", "raw_reports": len(raw), "raw_cells": 162, "frozen_k": len(frozen_k), "reviewed_non_k": len(decisions), "dense_relations": len(dense), "n_reports": len(final_n), "n_groups": len(group_set.n_groups), "i_reports": len(final_i), "i_clusters": len(group_set.invalid_clusters)}, sort_keys=True))


if __name__ == "__main__":
    main()
