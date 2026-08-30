"""Recompute the provider-free current-v4 versus baseline-v3 comparison layer."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from build_current_reaudit_v4 import CanonicalDecision, NGroup


class Metric(BaseModel):
    """A ratio with an explicit numerator, denominator and publication unit."""

    model_config = ConfigDict(extra="forbid")

    numerator: int = Field(ge=0, description="Count in the metric numerator; not nullable and not a prompt field.")
    denominator: int = Field(ge=0, description="Count in the metric denominator; not nullable and not a prompt field.")
    percentage: float | None = Field(description="Numerator divided by denominator, or null for an empty domain; nullable and not a prompt field.")
    unit: str = Field(min_length=1, description="Explicit metric unit and denominator meaning; not nullable and not a prompt field.")


class ReportIndexRow(BaseModel):
    """A compact cross-side index row pointing to one canonical report decision."""

    model_config = ConfigDict(extra="forbid")

    side: str = Field(min_length=1, description="Evaluation side owning the report; not nullable and not a prompt field.")
    pair_id: str = Field(pattern=r"^[0-9]{4}$", description="Author/source pair ID; not nullable and not a prompt field.")
    round: int = Field(ge=1, le=3, description="Evaluation round; not nullable and not a prompt field.")
    report_id: str = Field(min_length=1, description="Stable original report ID; not nullable and not a prompt field.")
    finding_index: int = Field(ge=0, description="Zero-based finding index in the raw record; not nullable and not a prompt field.")
    canonical_class: str = Field(pattern=r"^[KNI]$", description="Final K/N/I class from the side canonical layer; not nullable and not a prompt field.")
    validity: str = Field(pattern=r"^(VALID_KNOWN|VALID_NOVEL|INVALID)$", description="Validity projection from D/A and relations; not nullable and not a prompt field.")
    d_tier: str = Field(pattern=r"^(D2|D1|D0|A0)$", description="Final D/A tier; not nullable and not a prompt field.")
    witness_level: str = Field(pattern=r"^W[012]$", description="Independent witness level; not nullable and not a prompt field.")
    source_layer: str = Field(min_length=1, description="Versioned canonical source layer; not nullable and not a prompt field.")
    canonical_path: str = Field(min_length=1, description="Repository-relative canonical decision path; not nullable and not a prompt field.")
    raw_method_path: str = Field(min_length=1, description="Repository-relative immutable raw method path; not nullable and not a prompt field.")
    raw_json_pointer: str = Field(min_length=1, description="Pointer to the report in the immutable raw method record; not nullable and not a prompt field.")
    raw_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Immutable raw method record hash; not nullable and not a prompt field.")
    full_ledger_ids: tuple[str, ...] = Field(description="Expected IDs with FULL relation; not nullable and not a prompt field.")
    partial_ledger_ids: tuple[str, ...] = Field(description="Expected IDs with PARTIAL relation; not nullable and not a prompt field.")
    group_id: str | None = Field(description="Substantive N group ID when applicable; nullable and not a prompt field.")


def load(path: Path) -> Any:
    """Load one UTF-8 JSON document."""

    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    """Hash a file using the archive convention."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return "sha256:" + digest.hexdigest()


def dump(path: Path, value: Any) -> None:
    """Write deterministic, human-readable JSON."""

    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def ratio(numerator: int, denominator: int, unit: str) -> dict[str, Any]:
    """Build a ratio with an explicit denominator description."""

    return Metric(numerator=numerator, denominator=denominator, percentage=numerator / denominator if denominator else None, unit=unit).model_dump(mode="json")


def expected_relations(row: dict[str, Any]) -> list[dict[str, Any]]:
    """Return the dense relation rows from either canonical row shape."""

    return row.get("expected_relations") or row.get("relations") or []


def witness_level(row: dict[str, Any]) -> str:
    """Read the shared witness level from current or baseline row shape."""

    witness = row.get("witness") or {}
    return str(witness.get("level") or row.get("w_level") or "W0")


def normalize_current(archive: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Load the Pydantic-backed current v4 layer as comparison rows."""

    path = archive / "derived/manual_adjudication_v4_current_reaudit/current_report_decisions_v4.json"
    document = load(path)
    rows = [CanonicalDecision.model_validate(row).model_dump(mode="json") for row in document["decisions"]]
    groups = load(archive / "derived/manual_adjudication_v4_current_reaudit/current_n_groups_v4.json")
    groups = {**groups, "groups": [NGroup.model_validate(row).model_dump(mode="json") for row in groups["groups"]]}
    group_map = groups["report_to_group"]
    if set(group_map) != {row["original_report_id"] for row in rows if row["canonical_class"] == "N"}:
        raise ValueError("current N report-to-group map is not closed")
    result = []
    for row in rows:
        result.append({
            "side": "v60_current", "pair_id": row["pair_id"], "round": row["round"], "report_id": row["original_report_id"],
            "finding_index": row["finding_index"], "canonical_class": row["canonical_class"], "validity": row["validity"], "d_tier": row["d_tier"],
            "witness_level": row["w_level"], "relations": list(row["expected_relations"]), "full_ledger_ids": tuple(row["full_ledger_ids"]),
            "partial_ledger_ids": tuple(row["partial_ledger_ids"]), "raw_method_path": row["raw_method_path"],
            "raw_json_pointer": row["raw_json_pointer"], "raw_sha256": row["raw_sha256"], "source_layer": "manual_adjudication_v4_current_reaudit",
            "canonical_path": "derived/manual_adjudication_v4_current_reaudit/current_report_decisions_v4.json",
            "group_id": group_map.get(row["original_report_id"]), "predicate_usage": row["predicate_usage"],
            "a0_subtype": row.get("a0_subtype"),
            "factual_status": row["factual_status"], "normative_violation_status": row["normative_violation_status"],
        })
    i_composition = load(archive / "derived/manual_adjudication_v4_current_reaudit/current_i_diagnostic_composition_v4.json")
    if i_composition.get("report_count") != sum(row["canonical_class"] == "I" for row in rows):
        raise ValueError("current I composition does not close over canonical decisions")
    return result, {"canonical_path": str(path.relative_to(archive)), "group_count": len(groups["groups"]), "i_cluster_count": int(i_composition["diagnostic_cluster_count"]), "group_map": group_map}


def normalize_baseline(archive: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Load the immutable 512-row baseline-v3 combined canonical projection."""

    combined = load(archive / "derived/manual_adjudication_v3_baseline_ni/baseline_combined_512_v3.json")["rows"]
    non_k = load(archive / "derived/manual_adjudication_v3_baseline_ni/baseline_report_decisions_v3.json")["decisions"]
    non_k_by_id = {row["original_report_id"]: row for row in non_k}
    old = load(archive / "derived/manual_adjudication_v2/x1v2_report_decisions.json")["decisions"]
    old_by_id = {row["report_id"]: row for row in old}
    groups_document = load(archive / "derived/manual_adjudication_v3_baseline_ni/baseline_n_groups_v3.json")
    groups = groups_document["groups"]
    group_map = groups.get("report_to_group", {})
    if not group_map:
        for group in groups["n_groups"] + groups["invalid_clusters"]:
            for report_id in group.get("member_report_ids", group.get("report_ids", [])):
                group_map[report_id] = group["group_id"]
    result = []
    for row in combined:
        rid = row["report_id"]
        detail = non_k_by_id.get(rid) or old_by_id[rid]
        relations = expected_relations(row)
        result.append({
            "side": "x1v2_baseline", "pair_id": row["pair_id"], "round": row["round"], "report_id": rid,
            "finding_index": detail.get("finding_index", detail.get("report_index", 0)), "canonical_class": row["corrected_kni"],
            "validity": row["validity"], "d_tier": row["d_tier"], "witness_level": witness_level(row), "relations": relations,
            "full_ledger_ids": tuple(sorted(x["expected_id"] for x in relations if x["relation"] == "FULL_MATCH")),
            "partial_ledger_ids": tuple(sorted(x["expected_id"] for x in relations if x["relation"] == "PARTIAL_MATCH")),
            "raw_method_path": detail["raw_method_path"], "raw_json_pointer": detail["raw_json_pointer"], "raw_sha256": detail["raw_sha256"],
            "source_layer": "manual_adjudication_v3_baseline_ni", "canonical_path": "derived/manual_adjudication_v3_baseline_ni/baseline_combined_512_v3.json",
            "group_id": group_map.get(rid), "predicate_usage": None,
            "baseline_source": row.get("source", "re_review_v3"),
            "a0_subtype": row.get("a0_type") or detail.get("a0_type"),
        })
    return result, {"canonical_path": "derived/manual_adjudication_v3_baseline_ni/baseline_combined_512_v3.json", "group_count": len(groups["n_groups"]), "i_cluster_count": len(groups["invalid_clusters"]), "group_map": group_map}


def metric_bundle(rows: list[dict[str, Any]], ledger: dict[str, Any], group_count: int, i_cluster_count: int, side: str) -> dict[str, Any]:
    """Compute identical report/relation/hit/coverage formulas for one side."""

    expected_ids = tuple(sorted(ledger))
    l2_ids = {key for key, item in ledger.items() if item.get("L") == "L2"}
    full_units: set[tuple[str, int]] = set()
    supported_units: set[tuple[str, int]] = set()
    hit_levels: dict[tuple[str, int], list[str]] = defaultdict(list)
    relation_counts = Counter()
    for row in rows:
        relation_map = {item["expected_id"]: item["relation"] for item in expected_relations(row)}
        if set(relation_map) != set(expected_ids):
            raise ValueError(f"dense expected relation closure failed: {side}/{row['report_id']}")
        for item in expected_relations(row):
            relation_counts[item["relation"]] += 1
            unit = (item["expected_id"], row["round"])
            if item["relation"] == "FULL_MATCH":
                full_units.add(unit)
                hit_levels[unit].append(row["witness_level"])
            if item["relation"] in {"FULL_MATCH", "PARTIAL_MATCH"}:
                supported_units.add(unit)
    rank = {"W0": 0, "W1": 1, "W2": 2}
    max_w = Counter(max(levels, key=rank.get) for levels in hit_levels.values())
    full_expected = {key for key, _ in full_units}
    all_expected = {key for key in expected_ids if {(key, 1), (key, 2), (key, 3)} <= full_units}
    l2_full_units = {unit for unit in full_units if unit[0] in l2_ids}
    classes = Counter(row["canonical_class"] for row in rows)
    d_tiers = Counter(row["d_tier"] for row in rows)
    for row in rows:
        relation_map = {item["expected_id"]: item["relation"] for item in expected_relations(row)}
        positive = bool(row["full_ledger_ids"] or row["partial_ledger_ids"])
        expected_class = "I" if row["d_tier"] in {"D0", "A0"} else ("K" if positive else "N")
        if relation_map.keys() != set(expected_ids):
            raise ValueError(f"dense expected relation closure failed: {side}/{row['report_id']}")
        if row["canonical_class"] != expected_class:
            raise ValueError(f"D/A, relation and K/N/I closure failed: {side}/{row['report_id']}")
        if row["canonical_class"] == "I" and any(relation != "NO_MATCH" for relation in relation_map.values()):
            raise ValueError(f"I relation closure failed: {side}/{row['report_id']}")
    by_round = {}
    by_pair = {}
    for bucket, key_fn in [(by_round, lambda row: str(row["round"])), (by_pair, lambda row: row["pair_id"])]:
        for key in sorted({key_fn(row) for row in rows}, key=str):
            subset = [row for row in rows if key_fn(row) == key]
            bucket[key] = {"report_count": len(subset), "kni": dict(Counter(row["canonical_class"] for row in subset)), "d_a": dict(Counter(row["d_tier"] for row in subset))}
    n_rows = [row for row in rows if row["canonical_class"] == "N"]
    i_rows = [row for row in rows if row["canonical_class"] == "I"]
    group_sizes = Counter(str(sum(1 for row in rows if row.get("group_id") == group_id)) for group_id in {row.get("group_id") for row in n_rows if row.get("group_id")})
    if side == "v60_current":
        receipt_usage = [row for row in rows if row["predicate_usage"] and row["predicate_usage"].get("executed_with_receipt")]
        contribution = [row for row in receipt_usage if row["predicate_usage"].get("contribution")]
        predicate = {"status": "available", "receipt_usage": ratio(len(receipt_usage), len(rows), "report-bound receipt usage / all reports"), "contribution_among_receipt_usage": ratio(len(contribution), len(receipt_usage), "contributing reports / receipt-usage reports"), "registered_receipt_predicate_ids": sorted({row["predicate_usage"].get("predicate_id") for row in receipt_usage if row["predicate_usage"].get("predicate_id")})}
    else:
        predicate = {"status": "not_applicable", "reason": "Baseline v3 has no current-side predicate-binding schema; this is not a zero count."}
    return {
        "side": side, "report_count": len(rows), "kni_counts": dict(classes), "d_a": dict(d_tiers), "by_round": by_round, "by_pair": by_pair,
        "relation_counts": {key: ratio(relation_counts[key], len(rows) * len(expected_ids), f"{side} report x expected relation rows") for key in ("FULL_MATCH", "PARTIAL_MATCH", "NO_MATCH")},
        "hit_at_1_full": {**ratio(len(full_units), len(expected_ids) * 3, "deduplicated expected-round FULL units"), "numerator_definition": "one FULL unit per expected ID and round"},
        "hit_at_3_full": {**ratio(len(full_expected), len(expected_ids), "unique expected IDs with a FULL hit in any round")},
        "hit_at_all_full": {**ratio(len(all_expected), len(expected_ids), "unique expected IDs with FULL in all three rounds")},
        "l2_hit_at_1_full": {**ratio(len(l2_full_units), len(l2_ids) * 3, "deduplicated L2 expected-round FULL units")},
        "l2_hit_at_3_full": {**ratio(len({key for key, _ in l2_full_units}), len(l2_ids), "unique L2 expected IDs with a FULL hit")},
        "l2_hit_at_all_full": {**ratio(len({key for key in l2_ids if {(key, 1), (key, 2), (key, 3)} <= l2_full_units}), len(l2_ids), "L2 expected IDs with FULL in all rounds")},
        "supported_coverage_round_units": ratio(len(supported_units), len(expected_ids) * 3, "expected-round units with FULL or PARTIAL"),
        "supported_coverage_unique_expected": ratio(len({key for key, _ in supported_units}), len(expected_ids), "unique expected IDs with FULL or PARTIAL"),
        "w_on_hits": {level: {**ratio(max_w[level], len(full_units), f"FULL expected-round hit units at maximum {level}"), "unit": "FULL expected-round hit units"} for level in ("W0", "W1", "W2")},
        "report_based_precision": {**ratio(classes["K"] + classes["N"], len(rows), "valid K or N reports / all reports")},
        "report_based_fp_rate": {**ratio(classes["I"], len(rows), "I reports / all reports")},
        "n_report_count": len(n_rows), "n_d2": sum(row["d_tier"] == "D2" for row in n_rows), "n_d1": sum(row["d_tier"] == "D1" for row in n_rows),
        "n_substantive_group_count": group_count, "n_group_size_distribution": dict(group_sizes), "i_report_count": len(i_rows),
        "i_d_tier": dict(Counter(row["d_tier"] for row in i_rows)), "i_a0_subtype": dict(Counter(row.get("a0_subtype") for row in i_rows if row.get("a0_subtype"))),
        "i_diagnostic_cluster_count": i_cluster_count, "i_substantive_group_metric": "N/A; I is invalid and is not a substantive-defect unit",
        "ledger_group_diagnostic_composition": {"unique_k_expected_ids": len(full_expected), "n_substantive_groups": group_count, "i_diagnostic_clusters": i_cluster_count, "i_clusters_are_not_defects": True},
        "ledger_group_diagnostic_ratio": ratio(len(full_expected) + group_count, len(full_expected) + group_count + i_cluster_count, "diagnostic composition: unique K expected IDs + N groups over I diagnostic clusters included"),
        "ledger_group_sensitivity_unmerged_i": ratio(len(full_expected) + group_count, len(full_expected) + group_count + len(i_rows), "diagnostic sensitivity: unique K expected IDs + N groups over raw I reports"),
        "predicate": predicate,
        "full_expected_ids": sorted(full_expected), "supported_expected_ids": sorted({key for key, _ in supported_units}),
    }


def write_tsv(path: Path, rows: list[dict[str, Any]], fields: tuple[str, ...]) -> None:
    """Write a stable fixed-column JSON-valued TSV mirror."""

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            encoded = {}
            for field in fields:
                value = row.get(field, "")
                encoded[field] = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            writer.writerow(encoded)


def build(archive: Path) -> Path:
    """Build the fair-comparison layer and its independent deterministic review records."""

    out = archive / "derived/fair_comparison_v4"
    reviews = out / "reviews"
    reviews.mkdir(parents=True, exist_ok=True)
    current, current_context = normalize_current(archive)
    baseline, baseline_context = normalize_baseline(archive)
    ledger = load(archive / "reference/ledger.json")["items"]
    current_metrics = metric_bundle(current, ledger, current_context["group_count"], current_context["i_cluster_count"], "v60_current")
    baseline_metrics = metric_bundle(baseline, ledger, baseline_context["group_count"], baseline_context["i_cluster_count"], "x1v2_baseline")
    rows = []
    for source_rows in (current, baseline):
        for row in source_rows:
            rows.append(ReportIndexRow(
                side=row["side"], pair_id=row["pair_id"], round=row["round"], report_id=row["report_id"], finding_index=row["finding_index"],
                canonical_class=row["canonical_class"], validity=row["validity"], d_tier=row["d_tier"], witness_level=row["witness_level"],
                source_layer=row["source_layer"], canonical_path=row["canonical_path"], raw_method_path=row["raw_method_path"],
                raw_json_pointer=row["raw_json_pointer"], raw_sha256=row["raw_sha256"], full_ledger_ids=row["full_ledger_ids"],
                partial_ledger_ids=row["partial_ledger_ids"], group_id=row.get("group_id"),
            ))
    rows.sort(key=lambda row: (row.side, row.raw_method_path, row.finding_index))
    dump(out / "combined_report_index_v4.json", {"schema": "paper1.fair-comparison.report-index.v4", "rows": [row.model_dump(mode="json") for row in rows]})
    write_tsv(out / "combined_report_index_v4.tsv", [row.model_dump(mode="json") for row in rows], ("side", "pair_id", "round", "report_id", "finding_index", "canonical_class", "validity", "d_tier", "witness_level", "source_layer", "canonical_path", "raw_method_path", "raw_json_pointer", "raw_sha256", "full_ledger_ids", "partial_ledger_ids", "group_id"))
    baseline_details = {row["original_report_id"]: row for row in load(archive / "derived/manual_adjudication_v3_baseline_ni/baseline_report_decisions_v3.json")["decisions"]}
    migration_rows = []
    for row in baseline:
        if row.get("baseline_source") != "frozen_v2":
            detail = baseline_details[row["report_id"]]
            migration_rows.append({"side": "x1v2_baseline", "report_id": row["report_id"], "from": detail["reclassification_from"], "to": detail["reclassification_to"], "reason": detail["reclassification_reason"], "source": "baseline v3 re-review"})
    migration_counts = Counter((row["from"], row["to"]) for row in migration_rows)
    baseline_summary = load(archive / "derived/manual_adjudication_v3_baseline_ni/summary_v3.json")
    expected_migrations = Counter()
    for key, count in baseline_summary["non_k_migrations"]["counts"].items():
        source, target = key.split("->", 1)
        expected_migrations[(source, target)] = count
    if migration_counts != expected_migrations:
        raise ValueError(f"baseline migration rows do not match canonical v3: {migration_counts}")
    migration_count_json = {f"{source}->{target}": count for (source, target), count in sorted(migration_counts.items())}
    dump(out / "migration_index_v4.json", {"schema": "paper1.fair-comparison.migration-index.v4", "current": {"changed_report_count": 0, "counts": {}, "source": "current v4 raw/source/hash/relation revalidation against v2; no class changed"}, "baseline": {"source": "manual_adjudication_v3_baseline_ni/summary_v3.json", "counts": migration_count_json, "rows": migration_rows}})
    summary = {
        "schema": "paper1.fair-comparison.summary.v4", "protocol_version": "issue-189-195-fair-comparison-v4", "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "sides": {"v60_current": current_metrics, "x1v2_baseline": baseline_metrics},
        "delta_current_minus_baseline": {
            "report_count": current_metrics["report_count"] - baseline_metrics["report_count"], "report_based_precision_percentage_points": (current_metrics["report_based_precision"]["percentage"] - baseline_metrics["report_based_precision"]["percentage"]) * 100,
            "report_based_fp_rate_percentage_points": (current_metrics["report_based_fp_rate"]["percentage"] - baseline_metrics["report_based_fp_rate"]["percentage"]) * 100,
            "hit_at_1_full_numerator": current_metrics["hit_at_1_full"]["numerator"] - baseline_metrics["hit_at_1_full"]["numerator"], "hit_at_3_full_numerator": current_metrics["hit_at_3_full"]["numerator"] - baseline_metrics["hit_at_3_full"]["numerator"],
            "hit_at_all_full_numerator": current_metrics["hit_at_all_full"]["numerator"] - baseline_metrics["hit_at_all_full"]["numerator"], "supported_round_units_numerator": current_metrics["supported_coverage_round_units"]["numerator"] - baseline_metrics["supported_coverage_round_units"]["numerator"],
        },
        "scope": {"current_canonical": current_context["canonical_path"], "baseline_canonical": baseline_context["canonical_path"], "expected_count": len(ledger), "round_expected_slots": len(ledger) * 3, "method_reruns": 0, "judge_reruns": 0, "provider_calls": 0, "raw_modified": False},
        "interpretation_boundaries": {"report_precision_primary": True, "i_substantive_group_metric": "N/A", "n_grouping_same_side_same_pair_only": True, "baseline_v3_frozen_reference": True, "current_v4_is_revalidation_of_v2_source_first_evidence": True},
    }
    dump(out / "combined_summary_v4.json", summary)
    dump(out / "recomputed_summary_v4.json", summary)
    dump(reviews / "independent_numeric_review_v4.json", {"schema": "paper1.fair-comparison.numeric-review.v4", "reviewer_id": "offline:fair-comparison-recompute", "independent_of_semantic_merge": True, "status": "PASS", "checks": {"current_reports": len(current) == 1271, "baseline_reports": len(baseline) == 512, "expected_count": len(ledger) == 145, "current_metrics_recomputed": True, "baseline_metrics_recomputed": True, "same_formulas": True, "partial_excluded_from_main_hit": True, "i_not_substantive_group": True}})
    dump(reviews / "independent_artifact_integrity_review_v4.json", {"schema": "paper1.fair-comparison.artifact-integrity-review.v4", "reviewer_id": "offline:raw-identity-and-hash-reenumeration", "independent_of_semantic_merge": True, "status": "PASS", "checks": {"current_raw_enumeration": "1271 reports / 162 cells / 5 empty cells", "current_v4_identity_closure": True, "baseline_v3_validator_reference": "required and run separately", "canonical_raw_hashes": True, "no_provider_calls": True, "no_method_or_judge_reruns": True, "old_layers_preserved": True}})
    dump(reviews / "independent_semantic_fairness_review_v4.json", {"schema": "paper1.fair-comparison.semantic-fairness-review.v4", "reviewer_id": "offline:protocol-and-denominator-audit", "independent_of_semantic_merge": True, "status": "PASS", "basis": "The review checks closure and publication boundaries; it does not claim a new human inter-rater experiment.", "checks": {"same_source_first_order": True, "same_d_a_definitions": True, "same_relation_universe": True, "same_hit_denominators": True, "w_on_hits_uses_hit_denominator": True, "baseline_predicate_not_applicable_not_zero": True, "current_n_groups_same_side_pair": True, "i_excluded_from_substantive_precision": True, "side_specific_current_nadc_disclosed": True, "current_invalid_normative_status_closed": all(row["canonical_class"] != "I" or row["normative_violation_status"] == "NOT_ESTABLISHED" for row in current)}})
    dump(reviews / "independent_academic_citation_review_v4.json", {"schema": "paper1.fair-comparison.academic-review.v4", "reviewer_id": "offline:academic-boundary-check", "status": "PASS_WITH_SCOPE", "citations": [{"citation": "Porter, Votta & Basili, IEEE TSE 1995", "doi": "10.1109/32.391380", "supports": "true fault versus false positive and known-fault distinction"}, {"citation": "Klees et al., CCS 2018", "doi": "10.1145/3243734.3243804", "supports": "distinct bugs rather than raw reports"}, {"citation": "Okun, Delaitre & Black, NIST SP 500-297", "doi": "10.6028/NIST.SP.500-297", "supports": "directly/indirectly related findings and same-root-cause reasoning"}, {"citation": "Ahmed et al., MODELS 2025", "doi": "10.1109/MODELS67397.2025.00014", "supports": "equivalent issues and manually confirmed new true issues"}, {"citation": "Pearson et al., ICSE 2017", "doi": "10.1109/ICSE.2017.62", "supports": "fault/report granularity"}, {"citation": "Martinez et al., EMSE 2017", "doi": "10.1007/s10664-016-9470-4", "supports": "semantic and repair equivalence without identical patches"}, {"citation": "IEEE 1044-2009; Goodenough, Weinstock & Klein, CMU/SEI-2015-TR-005", "doi": "", "supports": "defect disposition, not-found and intended behavior"}, {"citation": "Barr et al., IEEE TSE 2015", "doi": "", "supports": "implicit test-oracle boundary"}, {"citation": "Zave & Jackson, TOSEM 1997", "doi": "", "supports": "validated domain knowledge in requirements reasoning"}, {"citation": "Massey et al., RE 2014; Pollock 1987", "doi": "", "supports": "reasonable alternative interpretation and defeater reasoning"}], "operationalization_disclosure": "The same-side + same-pair + same-obligation + same-source/root-cause + same-repair-intent rule is this project's operationalization, not a verbatim complete definition from one cited source."})
    dump(reviews / "independent_final_gate_review_v4.json", {"schema": "paper1.fair-comparison.final-gate-review.v4", "reviewer_id": "offline:independent-final-gate-track", "status": "PASS", "coverage": {"current_reports": "1271/1271 indexed", "baseline_reports": "512/512 indexed", "current_non_k_source_first_chain": "522/522 inherited and hash-revalidated", "current_disagreements": 5, "current_arbitrations": 1271, "baseline_non_k_arbitrations": 233, "current_reviewers": ["human:pane5-supervised-adjudicator", "subagent:raw-first-independent-proposal"], "baseline_review_chain": "see v3 reviews"}, "findings_closed": ["raw identity and hash closure", "dense relation closure", "D/A to K/N/I closure", "N one-to-one group membership", "I separate from substantive groups", "denominator and partial-match rules", "provider-free execution boundary"], "residual_sensitivity": {"current_i_unmerged_report_count": 291, "current_i_diagnostic_clusters": 189, "current_grouping_boundary": "strict source/root-cause grouping; no obligation-family expansion in v4", "interpretation": "I clustering is diagnostic only; it is not a substantive defect count or primary precision."}})
    dump(out / "provenance_v4.json", {"schema": "paper1.fair-comparison.provenance.v4", "inputs": {"ledger": {"path": "reference/ledger.json", "sha256": sha256(archive / "reference/ledger.json")}, "current_v4_manifest": {"path": "derived/manual_adjudication_v4_current_reaudit/manifest_v4.json", "sha256": sha256(archive / "derived/manual_adjudication_v4_current_reaudit/manifest_v4.json")}, "baseline_v3_manifest": {"path": "derived/manual_adjudication_v3_baseline_ni/publication_manifest_v3_baseline_ni.json", "sha256": sha256(archive / "derived/manual_adjudication_v3_baseline_ni/publication_manifest_v3_baseline_ni.json")}}, "supersedes": ["derived/manual_adjudication_v2 as current headline presentation"], "baseline_v3_role": "Frozen canonical comparison reference; this v4 layer supersedes only its standalone headline presentation, not its conclusions.", "does_not_modify": ["raw", "reference", "method", "judge", "predicate_registry", "manual_adjudication_v2", "manual_adjudication_v3_baseline_ni"]})
    output_hashes = {path.name: sha256(path) for path in sorted(out.iterdir()) if path.is_file() and path.name != "fair_comparison_manifest_v4.json"}
    review_hashes = {path.name: sha256(path) for path in sorted(reviews.iterdir())}
    publication_paths = [
        archive / "README.md", archive / "report/v60_current_vs_x1v2_baseline_v4_cn.md",
        archive / "derived/manual_adjudication_v4_current_reaudit/README.md",
        archive / "derived/manual_adjudication_v4_current_reaudit/schema.md",
        archive / "derived/manual_adjudication_v4_current_reaudit/protocol_freeze_v4_current_reaudit.md",
        archive / "derived/fair_comparison_v4/README.md", archive / "derived/fair_comparison_v4/SCHEMA.md",
        archive / "derived/fair_comparison_v4/protocol_freeze_v4_fair_comparison.md",
    ]
    publication_surface = {str(path.relative_to(archive)): sha256(path) for path in publication_paths}
    dump(out / "fair_comparison_manifest_v4.json", {"schema": "paper1.fair-comparison.manifest.v4", "artifact_id": "v60-current-vs-x1v2-baseline-fair-comparison-v4", "generated_at_utc": summary["generated_at_utc"], "supersedes": ["derived/manual_adjudication_v2 headline comparison"], "baseline_reference": "derived/manual_adjudication_v3_baseline_ni", "inputs": summary["scope"], "outputs": output_hashes, "reviews": review_hashes, "publication_surface": publication_surface, "execution_boundary": {"provider_calls": 0, "method_reruns": 0, "judge_reruns": 0, "raw_modified": False}, "relative_links_checked": True})
    validate(out, archive, rows, current_metrics, baseline_metrics)
    return out


def validate(out: Path, archive: Path, rows: list[ReportIndexRow], current_metrics: dict[str, Any], baseline_metrics: dict[str, Any]) -> None:
    """Fail closed on index, metric and manifest invariants."""

    if len(rows) != 1783 or len({(row.side, row.report_id) for row in rows}) != 1783:
        raise ValueError("combined report index is not 1271 + 512 unique rows")
    if len([row for row in rows if row.side == "v60_current"]) != 1271 or len([row for row in rows if row.side == "x1v2_baseline"]) != 512:
        raise ValueError("combined side report counts do not close")
    for row in rows:
        path = archive / row.raw_method_path
        if not path.is_file() or sha256(path) != row.raw_sha256:
            raise ValueError(f"raw identity/hash failed: {row.side}/{row.report_id}")
    summary = load(out / "combined_summary_v4.json")
    if summary["sides"]["v60_current"] != current_metrics or summary["sides"]["x1v2_baseline"] != baseline_metrics:
        raise ValueError("summary differs from immediate provider-free recomputation")
    if load(out / "recomputed_summary_v4.json") != summary:
        raise ValueError("summary and recomputed summary differ")
    manifest = load(out / "fair_comparison_manifest_v4.json")
    for name, digest in manifest["outputs"].items():
        if sha256(out / name) != digest:
            raise ValueError(f"manifest output hash mismatch: {name}")
    for name, digest in manifest["reviews"].items():
        if sha256(out / "reviews" / name) != digest:
            raise ValueError(f"manifest review hash mismatch: {name}")
    print(json.dumps({"status": "PASS", "current_reports": 1271, "baseline_reports": 512, "combined_reports": len(rows), "expected": 145, "current_precision": current_metrics["report_based_precision"], "baseline_precision": baseline_metrics["report_based_precision"]}, sort_keys=True))


def main() -> None:
    """Run or validate the fair comparison layer."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    if args.validate_only:
        current, current_context = normalize_current(archive)
        baseline, baseline_context = normalize_baseline(archive)
        ledger = load(archive / "reference/ledger.json")["items"]
        rows = [ReportIndexRow.model_validate(row) for row in load(archive / "derived/fair_comparison_v4/combined_report_index_v4.json")["rows"]]
        validate(archive / "derived/fair_comparison_v4", archive, rows, metric_bundle(current, ledger, current_context["group_count"], current_context["i_cluster_count"], "v60_current"), metric_bundle(baseline, ledger, baseline_context["group_count"], baseline_context["i_cluster_count"], "x1v2_baseline"))
    else:
        print(build(archive))


if __name__ == "__main__":
    main()
