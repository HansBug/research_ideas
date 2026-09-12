"""Recompute manual-adjudication publication metrics from canonical decisions.

The script is deterministic and provider-free.  It performs no semantic
classification: the only inputs to the aggregates are the already confirmed
Pydantic decisions, the frozen ledger, and preserved cost metadata.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from paper_stm_evaluation.manual_adjudication import (
    AdjudicationStatus,
    GroupDecisionSet,
    ManualAdjudicationManifest,
    Relation,
    RelationAuditRow,
    RelationAuditSet,
    ReportDecision,
    ReportDecisionSet,
    Side,
    validate_decision_set,
)

from generate_manual_adjudication import build_reference_aggregate


def load(path: Path) -> dict[str, Any]:
    """Load one JSON object."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def sha256_file(path: Path) -> str:
    """Return an archive-style SHA-256."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def dump(path: Path, value: Any) -> None:
    """Write stable compact JSON."""

    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")


def ratio(numerator: int, denominator: int) -> dict[str, Any]:
    """Represent every metric with an explicit numerator and denominator."""

    return {"numerator": numerator, "denominator": denominator, "percentage": numerator / denominator if denominator else None}


def compare_delta(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    """Compute absolute and percentage-point differences for paired metrics."""

    return {"absolute_numerator_difference": left["numerator"] - right["numerator"], "percentage_point_difference": (left["percentage"] - right["percentage"]) * 100 if left["percentage"] is not None and right["percentage"] is not None else None}


def distribution(counter: Counter[str], denominator: int, keys: tuple[str, ...]) -> dict[str, dict[str, Any]]:
    """Represent categorical counts with the denominator used for each axis."""

    return {key: ratio(counter[key], denominator) for key in keys}


def expected_units(decisions: list[ReportDecision], ledger: dict[str, Any], relation: str) -> set[tuple[str, int]]:
    """Return ledger-defined expected-round units supported by a relation."""

    result = set()
    for decision in decisions:
        if decision.validity.value != "VALID_KNOWN":
            continue
        for row in decision.relations:
            expected = ledger["items"].get(row.expected_id, {})
            if str(expected.get("pair")) == decision.pair_id and row.relation.value == relation:
                result.add((row.expected_id, decision.round))
    return result


def build_relation_projection(decisions: list[ReportDecision]) -> RelationAuditSet:
    """Rebuild the dense relation projection from nested canonical rows."""

    rows = tuple(
        RelationAuditRow(
            side=decision.side,
            pair_id=decision.pair_id,
            round=decision.round,
            report_id=decision.report_id,
            expected_id=relation.expected_id,
            relation=relation.relation,
            reason=relation.reason,
            basis=relation.basis,
            source_refs=relation.source_refs,
            report_owned_field_refs=relation.report_owned_field_refs,
        )
        for decision in decisions
        for relation in decision.relations
    )
    return RelationAuditSet(rows=rows)


def build_hit_witnesses(decisions: list[ReportDecision], expected_ids: tuple[str, ...]) -> dict[str, Any]:
    """Rebuild the expected-round FULL supporting witness projection."""

    rows = []
    for side in ("v60_current", "x1v2_baseline"):
        side_decisions = [decision for decision in decisions if decision.side.value == side]
        for expected_id in expected_ids:
            for round_no in (1, 2, 3):
                supporting = [
                    decision for decision in side_decisions
                    if decision.round == round_no
                    and decision.validity.value == "VALID_KNOWN"
                    and any(row.expected_id == expected_id and row.relation.value == "FULL_MATCH" for row in decision.relations)
                ]
                levels = [decision.witness.level.value for decision in supporting]
                max_level = max(levels, key={"W0": 0, "W1": 1, "W2": 2}.get) if levels else None
                rows.append({
                    "side": side,
                    "expected_id": expected_id,
                    "round": round_no,
                    "supporting_report_ids": [decision.report_id for decision in supporting],
                    "max_witness_level": max_level,
                    "hit": bool(supporting),
                    "reason": "Deterministic projection of final VALID_KNOWN + FULL canonical decisions.",
                    "basis": "Nested ReportDecision.relations and ReportDecision.witness fields.",
                })
    return {"schema": "paper1.manual-adjudication.hit-witness.v1", "witnesses": rows}


def build_predicate_audit(archive: Path, decisions: list[ReportDecision]) -> dict[str, Any]:
    """Recompute current predicate binding usage from frozen raw issue objects."""

    def terminal_boolean(issue: dict[str, Any]) -> str | None:
        """Normalize frozen completed receipt values to terminal true/false."""

        execution = issue.get("execution_receipt") if isinstance(issue.get("execution_receipt"), dict) else {}
        if execution.get("terminal_state") != "completed":
            return None
        values = [execution.get("verdict")]
        nested = issue.get("receipt") if isinstance(issue.get("receipt"), dict) else {}
        values.extend([nested.get("verdict"), (nested.get("receipt") or {}).get("verdict") if isinstance(nested.get("receipt"), dict) else None])
        for value in values:
            normalized = str(value or "").lower()
            if normalized in {"true", "pass", "passed", "satisfied", "success"}:
                return "true"
            if normalized in {"false", "violation", "violated", "fail", "failed", "unsat", "no_witness"}:
                return "false"
        return None

    registry = load(archive / "reference" / "predicate_registry.json")
    evaluation_summary_path = archive / "raw" / "v60_current" / "judge" / "composite" / "evaluator" / "evaluation_summary.json"
    evaluation_summary = load(evaluation_summary_path)
    planned_predicates = evaluation_summary.get("planned_predicates")
    if not isinstance(planned_predicates, list) or not all(isinstance(item, str) for item in planned_predicates):
        raise ValueError("frozen evaluator summary has no valid planned predicate list")
    planned_scope_count = evaluation_summary.get("planned_predicate_count")
    if planned_scope_count != len(planned_predicates):
        raise ValueError("frozen planned predicate count does not close over its ID list")
    planned_scope_id = evaluation_summary.get("planned_predicate_scope")
    if not isinstance(planned_scope_id, str) or not planned_scope_id:
        raise ValueError("frozen evaluator summary has no planned predicate scope identifier")
    predicate_ids = tuple(str(predicate["id"]) for family in registry["families"] for predicate in family["predicates"])
    registry_set = set(predicate_ids)
    raw_by_path: dict[str, dict[str, Any]] = {}
    bound_by_predicate: dict[str, list[tuple[ReportDecision, dict[str, Any]]]] = defaultdict(list)
    planning_by_predicate: dict[str, Counter[str]] = defaultdict(Counter)
    unknown_bindings: Counter[str] = Counter()
    current = [decision for decision in decisions if decision.side.value == "v60_current"]
    for decision in current:
        if decision.raw_method_path not in raw_by_path:
            raw_by_path[decision.raw_method_path] = load(archive / decision.raw_method_path)
        issue = raw_by_path[decision.raw_method_path]["report_issue_clusters"][decision.report_index]
        plan = issue.get("plan") if isinstance(issue.get("plan"), dict) else {}
        predicate_id = str(issue.get("predicate_id") or plan.get("predicate_id") or "")
        registered = predicate_id in registry_set and plan.get("predicate_registered") is True
        precise = registered and bool((issue.get("binding") or {}).get("precise")) and bool(plan.get("binding_complete")) and bool(plan.get("binding_precise")) and bool(plan.get("input_shape_valid"))
        if predicate_id in registry_set:
            planning_by_predicate[predicate_id]["planned"] += 1
            planning_by_predicate[predicate_id]["routed"] += int(registered)
            planning_by_predicate[predicate_id]["precise_binding"] += int(precise)
            planning_by_predicate[predicate_id]["receipt_present"] += int(bool(issue.get("receipt") or issue.get("execution_receipt")))
            terminal = terminal_boolean(issue)
            planning_by_predicate[predicate_id]["terminal_true"] += int(terminal == "true")
            planning_by_predicate[predicate_id]["terminal_false"] += int(terminal == "false")
        if precise:
            bound_by_predicate[predicate_id].append((decision, issue))
        elif predicate_id:
            unknown_bindings[predicate_id] += 1
    rows = []
    for predicate_id in predicate_ids:
        bound_pairs = bound_by_predicate[predicate_id]
        bound = [decision for decision, _ in bound_pairs]
        hit_bound = [
            decision for decision in bound
            if decision.validity.value == "VALID_KNOWN"
            and any(row.relation.value == "FULL_MATCH" for row in decision.relations)
        ]
        degradation_reasons = sorted({
            reason
            for decision, issue in bound_pairs
            for reason in (
                decision.witness.degradation_reason,
                (issue.get("plan") or {}).get("failure_kind") if isinstance(issue.get("plan"), dict) else None,
                (issue.get("execution_receipt") or {}).get("failure_kind") if isinstance(issue.get("execution_receipt"), dict) else None,
                ((issue.get("receipt") or {}).get("run_metadata") or {}).get("failure_kind") if isinstance(issue.get("receipt"), dict) else None,
            )
            if reason
        })
        planning = planning_by_predicate[predicate_id]
        rows.append({
            "predicate_id": predicate_id,
            "usage_binding_count": len(bound),
            "associated_finding_count": len({decision.report_id for decision in bound}),
            "planned_in_frozen_scope": predicate_id in planned_predicates,
            "report_bound_plan_count": planning["planned"],
            "route_count": planning["routed"],
            "precise_binding_count": planning["precise_binding"],
            "receipt_present_count": planning["receipt_present"],
            "terminal_true_count": planning["terminal_true"],
            "terminal_false_count": planning["terminal_false"],
            "all_usage_denominator": len(bound),
            "all_usage_w0": sum(decision.witness.level.value == "W0" for decision in bound),
            "all_usage_w1": sum(decision.witness.level.value == "W1" for decision in bound),
            "all_usage_w2": sum(decision.witness.level.value == "W2" for decision in bound),
            "terminal_receipt_count": planning["terminal_true"] + planning["terminal_false"],
            "full_hit_supporting_usage_denominator": len(hit_bound),
            "full_hit_supporting_w0": sum(decision.witness.level.value == "W0" for decision in hit_bound),
            "full_hit_supporting_w1": sum(decision.witness.level.value == "W1" for decision in hit_bound),
            "full_hit_supporting_w2": sum(decision.witness.level.value == "W2" for decision in hit_bound),
            "failure_or_degradation_reasons": degradation_reasons,
        })
    return {
        "schema": "paper1.manual-adjudication.predicate-witness.v1",
        "protocol_version": "issue-189-195-manual-evidence-v2",
        "sides": {
            "v60_current": {
                "status": "applicable",
                "registry_id": registry["registry_version"],
                "planned_scope": {
                    "scope_id": planned_scope_id,
                    "predicate_ids": planned_predicates,
                    "count": planned_scope_count,
                    "source_path": str(evaluation_summary_path.relative_to(archive)),
                    "source_sha256": sha256_file(evaluation_summary_path),
                    "reason": "Frozen evaluator planned scope; distinct from report-bound predicate usage and terminal receipt counts.",
                },
                "predicate_rows": rows,
                "finding_count": len(current),
                "unknown_binding_count": sum(unknown_bindings.values()),
                "unknown_binding_predicate_ids": dict(sorted(unknown_bindings.items())),
                "reason": "All legal frozen predicate bindings are counted, including receipt-missing/failed bindings; only exact terminal receipts qualify for W2.",
            },
            "x1v2_baseline": {
                "status": "not_applicable",
                "reason": "X1v2 has no 19-predicate binding/terminal receipt schema; its W audit is independent and is not represented as zero usage.",
            },
        },
    }


def metric_bundle(decisions: list[ReportDecision], ledger: dict[str, Any], groups: list[dict[str, Any]], cost: dict[str, Any]) -> dict[str, Any]:
    """Compute one side's complete publication and audit metric bundle."""

    expected = ledger["items"]
    expected_ids = set(expected)
    l2_ids = {key for key, value in expected.items() if value.get("L") == "L2"}
    expected_round_denominator = len(expected_ids) * 3
    l2_round_denominator = len(l2_ids) * 3
    full = expected_units(decisions, ledger, "FULL_MATCH")
    partial = expected_units(decisions, ledger, "PARTIAL_MATCH")
    supported = full | partial
    def unique(units: set[tuple[str, int]]) -> set[str]:
        return {key for key, _ in units}
    hit3 = unique(full)
    hitall = {key for key in expected_ids if {(key, 1), (key, 2), (key, 3)} <= full}
    l2_full = {unit for unit in full if unit[0] in l2_ids}
    l2_hit3 = {key for key in l2_ids if any((key, round_no) in l2_full for round_no in (1, 2, 3))}
    l2_hitall = {key for key in l2_ids if {(key, 1), (key, 2), (key, 3)} <= l2_full}
    relation_keys = ("FULL_MATCH", "PARTIAL_MATCH", "NO_MATCH")
    relation_counts = Counter(row.relation.value for decision in decisions for row in decision.relations)
    d_counts = Counter(decision.strict_da.value for decision in decisions)
    validity_counts = Counter(decision.validity.value for decision in decisions)
    kni_counts = Counter(decision.corrected_kni for decision in decisions)
    witness_counts = Counter(decision.witness.level.value for decision in decisions)
    partial_only_reports = [decision.report_id for decision in decisions if decision.corrected_kni == "K" and not any(row.relation.value == "FULL_MATCH" for row in decision.relations) and any(row.relation.value == "PARTIAL_MATCH" for row in decision.relations)]
    partial_only_expected = unique(partial - full)
    side = decisions[0].side.value
    side_groups = [group for group in groups if group["side"] == side and group["group_verdict"] in {"N", "I"}]
    n_group = sum(group["group_verdict"] == "N" for group in side_groups)
    i_group = sum(group["group_verdict"] == "I" for group in side_groups)
    ledger_denominator = len(hit3) + n_group + i_group
    hit_levels: dict[tuple[str, int], list[str]] = defaultdict(list)
    for decision in decisions:
        if decision.validity.value != "VALID_KNOWN":
            continue
        for row in decision.relations:
            if row.relation.value == "FULL_MATCH" and str(expected.get(row.expected_id, {}).get("pair")) == decision.pair_id:
                hit_levels[(row.expected_id, decision.round)].append(decision.witness.level.value)
    rank = {"W0": 0, "W1": 1, "W2": 2}
    max_w = {level: 0 for level in rank}
    for levels in hit_levels.values():
        max_w[max(levels, key=rank.get)] += 1
    w2_all_expected = sum("W2" in levels for levels in hit_levels.values())
    relation_denominator = len(decisions) * len(expected_ids)
    pair_round_rows: dict[tuple[str, int], list[ReportDecision]] = defaultdict(list)
    for decision in decisions:
        pair_round_rows[(decision.pair_id, decision.round)].append(decision)
    pair_metrics: dict[str, Any] = {}
    for pair_id in sorted({decision.pair_id for decision in decisions}):
        pair_decisions = [decision for decision in decisions if decision.pair_id == pair_id]
        pair_expected = {key for key, value in expected.items() if str(value.get("pair")) == pair_id}
        pair_full = {(decision.round, row.expected_id) for decision in pair_decisions if decision.validity.value == "VALID_KNOWN" for row in decision.relations if row.relation.value == "FULL_MATCH" and row.expected_id in pair_expected}
        pair_partial = {(decision.round, row.expected_id) for decision in pair_decisions if decision.validity.value == "VALID_KNOWN" for row in decision.relations if row.relation.value == "PARTIAL_MATCH" and row.expected_id in pair_expected}
        pair_validity = Counter(decision.validity.value for decision in pair_decisions)
        pair_da = Counter(decision.strict_da.value for decision in pair_decisions)
        pair_metrics[pair_id] = {
            "report_count": len(pair_decisions),
            "expected_count": len(pair_expected),
            "full_round_units": ratio(len(pair_full), len(pair_expected) * 3),
            "supported_round_units": ratio(len(pair_full | pair_partial), len(pair_expected) * 3),
            "report_based_precision": ratio(pair_validity["VALID_KNOWN"] + pair_validity["VALID_NOVEL"], len(pair_decisions)),
            "report_based_fp_rate": ratio(pair_validity["INVALID"], len(pair_decisions)),
            "validity_counts": dict(sorted(pair_validity.items())),
            "d_a": dict(sorted(pair_da.items())),
        }
    round_metrics: dict[str, Any] = {}
    for round_no in (1, 2, 3):
        round_decisions = [decision for decision in decisions if decision.round == round_no]
        round_full = {(decision.pair_id, row.expected_id) for decision in round_decisions if decision.validity.value == "VALID_KNOWN" for row in decision.relations if row.relation.value == "FULL_MATCH" and str(expected.get(row.expected_id, {}).get("pair")) == decision.pair_id}
        round_partial = {(decision.pair_id, row.expected_id) for decision in round_decisions if decision.validity.value == "VALID_KNOWN" for row in decision.relations if row.relation.value == "PARTIAL_MATCH" and str(expected.get(row.expected_id, {}).get("pair")) == decision.pair_id}
        round_expected = sum(1 for value in expected.values() if value.get("pair") in {decision.pair_id for decision in round_decisions})
        round_validity = Counter(decision.validity.value for decision in round_decisions)
        round_da = Counter(decision.strict_da.value for decision in round_decisions)
        round_metrics[str(round_no)] = {
            "report_count": len(round_decisions),
            "expected_round_units": round_expected,
            "full_round_units": ratio(len(round_full), round_expected),
            "supported_round_units": ratio(len(round_full | round_partial), round_expected),
            "report_based_precision": ratio(round_validity["VALID_KNOWN"] + round_validity["VALID_NOVEL"], len(round_decisions)),
            "report_based_fp_rate": ratio(round_validity["INVALID"], len(round_decisions)),
            "d_a": dict(sorted(round_da.items())),
            "witness_counts": dict(sorted(Counter(decision.witness.level.value for decision in round_decisions).items())),
        }
    return {
        "report_count": len(decisions),
        "decision_counts": dict(sorted(d_counts.items())),
        "validity_counts": dict(sorted(validity_counts.items())),
        "kni_counts": dict(sorted(kni_counts.items())),
        "witness_counts": dict(sorted(witness_counts.items())),
        "relation_counts": dict(sorted(relation_counts.items())),
        "full_partial_none": {level: ratio(relation_counts[level], relation_denominator) for level in relation_keys},
        "hit_at_1_full": ratio(len(full), expected_round_denominator),
        "hit_at_3_full": ratio(len(hit3), len(expected_ids)),
        "hit_at_all_full": ratio(len(hitall), len(expected_ids)),
        "l2_hit_at_1_full": ratio(len(l2_full), l2_round_denominator),
        "l2_hit_at_3_full": ratio(len(l2_hit3), len(l2_ids)),
        "l2_hit_at_all_full": ratio(len(l2_hitall), len(l2_ids)),
        "supported_coverage_round_units": ratio(len(supported), expected_round_denominator),
        "supported_coverage_unique_expected": ratio(len(unique(supported)), len(expected_ids)),
        "partial_only_known_report": ratio(len(partial_only_reports), len(decisions)),
        "partial_only_known_expected": ratio(len(partial_only_expected), len(expected_ids)),
        "report_based_precision": ratio(sum(value for key, value in validity_counts.items() if key != "INVALID"), len(decisions)),
        "report_based_fp_rate": ratio(validity_counts["INVALID"], len(decisions)),
        "ledger_based": {
            "K_hit": ratio(len(hit3), len(expected_ids)),
            "N_group": ratio(n_group, ledger_denominator),
            "I_group": ratio(i_group, ledger_denominator),
            "N_group_count": n_group,
            "I_group_count": i_group,
            "composition_denominator": ledger_denominator,
            "precision": ratio(len(hit3), ledger_denominator),
            "fp_rate": ratio(i_group, ledger_denominator),
            "unit": "K_hit expected issue; N/I side-separated pair-local substantive groups",
        },
        "l2_ledger_based": {"status": "not_applicable", "reason": "N/I groups have no natural L2 expected attribution; protocol forbids manufacturing an L2 ledger denominator."},
        "hit_max_witness": {"W2": ratio(max_w["W2"], len(full)), "W1": ratio(max_w["W1"], len(full)), "W0": ratio(max_w["W0"], len(full))},
        "w2_all_expected": ratio(w2_all_expected, expected_round_denominator),
        "finding_level_w": {level: ratio(witness_counts[level], len(decisions)) for level in ("W0", "W1", "W2")},
        "d_a": dict(sorted(d_counts.items())),
        "d_a_distribution": distribution(d_counts, len(decisions), ("D2", "D1", "D0", "A0")),
        "by_round": round_metrics,
        "by_pair": pair_metrics,
        "cost": cost,
    }


def main() -> None:
    """Recompute all metrics and create the final machine-readable manifest."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    args = parser.parse_args()
    directory = args.directory.resolve()
    archive = directory.parent.parent
    ledger = load(archive / "reference/ledger.json")
    inventory = load(directory / "inventory.json")
    decisions_by_side = {
        Side.V60_CURRENT: ReportDecisionSet.model_validate(load(directory / "v60_report_decisions.json")).decisions,
        Side.X1V2_BASELINE: ReportDecisionSet.model_validate(load(directory / "x1v2_report_decisions.json")).decisions,
    }
    raw_index = {item["report_id"]: item for item in inventory["items"]}
    expected_ids = tuple(sorted(ledger["items"]))
    for decisions in decisions_by_side.values():
        validate_decision_set(decisions, expected_ids=expected_ids, raw_report_index={key: value for key, value in raw_index.items() if value["side"] == decisions[0].side.value})
    groups = GroupDecisionSet.model_validate(load(directory / "group_decisions.json")).groups
    groups_json = [group.model_dump(mode="json") for group in groups]
    recomputed = load(archive / "derived" / "recomputed_summary.json")
    costs = {side.value: recomputed.get("sides", {}).get(side.value, {}).get("cost", {}) for side in decisions_by_side}
    all_decisions = list(decisions_by_side[Side.V60_CURRENT]) + list(decisions_by_side[Side.X1V2_BASELINE])
    # Rebuild deterministic projections as part of recompute so stale files
    # cannot silently become publication inputs.
    dump(directory / "relation_decisions.json", build_relation_projection(all_decisions).model_dump(mode="json"))
    dump(directory / "hit_max_witness.json", build_hit_witnesses(all_decisions, expected_ids))
    dump(directory / "predicate_witness_audit.json", build_predicate_audit(archive, all_decisions))
    dump(directory / "reference_ledger_aggregate.json", build_reference_aggregate(archive))
    summary = {"schema": "paper1.manual-adjudication.summary.v2", "protocol_version": "issue-189-195-manual-evidence-v2", "review_status": "FINAL", "human_supervised_session": True, "expected_count": len(expected_ids), "sides": {side.value: metric_bundle(list(decisions), ledger, groups_json, costs[side.value]) for side, decisions in decisions_by_side.items()}, "delta_v60_minus_x1v2": {}}
    for metric_name in ("hit_at_1_full", "hit_at_3_full", "hit_at_all_full", "l2_hit_at_1_full", "l2_hit_at_3_full", "l2_hit_at_all_full", "supported_coverage_round_units", "supported_coverage_unique_expected", "report_based_precision", "report_based_fp_rate", "partial_only_known_report", "partial_only_known_expected", "w2_all_expected"):
        summary["delta_v60_minus_x1v2"][metric_name] = compare_delta(summary["sides"][Side.V60_CURRENT.value][metric_name], summary["sides"][Side.X1V2_BASELINE.value][metric_name])
    dump(directory / "summary.json", summary)
    input_hashes = {path: sha256_file(archive / path) for path in inventory["source_manifests"]}
    canonical = {}
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.name != "MANIFEST" and "checkpoints" not in path.parts and "proposals" not in path.parts:
            canonical[str(path.relative_to(directory))] = sha256_file(path)
    manifest = ManualAdjudicationManifest(
        generated_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        protocol_version="issue-189-195-manual-evidence-v2",
        raw_input_hashes=input_hashes,
        canonical_files=canonical,
        report_counts=inventory["reports"],
        status=AdjudicationStatus.FINAL,
        review_blockers=(),
    )
    dump(directory / "MANIFEST", manifest.model_dump(mode="json"))
    print(json.dumps({"status": "PASS", "reports": inventory["reports"], "dense_relations": len(all_decisions) * len(expected_ids), "manifest_files": len(canonical), "provider_calls": 0}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
