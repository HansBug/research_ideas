"""Build a read-only paired before/after audit for immutable full-scale runs."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from .export import write_json


class ArtifactReference(BaseModel):
    """Hash-addressed external artifact used as one side of a comparison."""

    path: str = Field(description="Absolute path to the immutable artifact.")
    sha256: str = Field(description="SHA-256 of the exact source bytes.")
    reason: str = Field(description="Why this artifact is an authorized evaluator input.")
    basis: str = Field(description="Deterministic integrity basis for the reference.")


class ComparisonSide(BaseModel):
    """One immutable method/Judge/evaluator result surface."""

    label: str = Field(description="Human-readable before or after label.")
    method_root: ArtifactReference = Field(description="Immutable method artifact root reference.")
    judge_root: ArtifactReference = Field(description="Immutable frozen-Judge composite reference.")
    evaluation_summary: ArtifactReference = Field(description="Evaluator summary reference.")
    expected_witness_audit: ArtifactReference = Field(description="Expected-issue witness audit reference.")
    method_configuration: dict[str, Any] = Field(description="Frozen method provenance, model, hashes, and worker configuration.")
    judge_configuration: dict[str, Any] = Field(description="Frozen Judge protocol, commit, profile, and source-run configuration.")
    outcomes: dict[str, Any] = Field(description="Overall and L2 hit, match, precision, and witness metrics.")
    evidence: dict[str, Any] = Field(description="All-evidence W levels and terminal predicate execution summaries.")
    costs: dict[str, Any] = Field(description="Method and Judge cost audit, including price-eligibility facts.")
    s2_scope: dict[str, Any] = Field(description="S2 scope and exact native carrier execution inventory.")


class DifferenceRow(BaseModel):
    """One machine-auditable before/after change keyed without prose matching."""

    key: str = Field(description="Stable deterministic comparison key.")
    before: Any = Field(description="Value or structured state in the baseline artifact.")
    after: Any = Field(description="Value or structured state in the corrected artifact.")
    reason: str = Field(description="Nonempty explanation of the observed delta category.")
    basis: str = Field(description="Exact artifact fields used to derive the delta.")


class PairedComparisonArtifact(BaseModel):
    """Evaluator-only before/after comparison with no method feedback channel."""

    schema: str = Field(default="evidence-discovery.paired-comparison.v3", description="Stable schema identifier for this evaluator artifact.")
    before: ComparisonSide = Field(description="Immutable pre-correction baseline snapshot.")
    after: ComparisonSide = Field(description="Immutable soundness/S2-corrected snapshot.")
    aggregate_deltas: dict[str, Any] = Field(description="Numerical before/after deltas over fixed denominators.")
    expected_relation_changes: list[DifferenceRow] = Field(description="Expected pair-round FULL/PARTIAL/NONE changes only.")
    report_surface_changes: list[DifferenceRow] = Field(description="Typed report semantic-key additions, removals, and W/D changes by pair-round.")
    matched_input_verdict_flips: list[DifferenceRow] = Field(description="Terminal verdict flips only for exact typed canonical carrier keys present in both runs.")
    before_only_carriers: list[DifferenceRow] = Field(description="S2 typed canonical carrier keys present only in the before run and excluded from matched-input verdict flips.")
    after_only_carriers: list[DifferenceRow] = Field(description="S2 typed canonical carrier keys present only in the after run and excluded from matched-input verdict flips.")
    matched_input_carrier_count: int = Field(description="Number of exact typed canonical carrier keys in the before/after intersection, the only denominator for same-input verdict flips.")
    sampling_interpretation: str = Field(description="Boundary statement separating observed deltas from unsupported causal claims.")
    reason: str = Field(description="Why this comparison is external and read-only.")
    basis: str = Field(description="Frozen artifact and deterministic-key basis for all fields.")


def _load(path: Path) -> dict[str, Any]:
    """Load a JSON-object artifact without interpreting natural-language claims."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _items(value: Any) -> list[dict[str, Any]]:
    """Normalize JSON sequence or mapping values into object rows."""

    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        return [item for item in value.values() if isinstance(item, dict)]
    return []


def _hash(path: Path) -> str:
    """Return the content hash used to close an input artifact reference."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _reference(path: Path, reason: str) -> ArtifactReference:
    """Create one integrity-preserving reference to an evaluator input."""

    resolved = path.expanduser().resolve()
    return ArtifactReference(
        path=str(resolved),
        sha256=_hash(resolved),
        reason=reason,
        basis="SHA-256 over immutable artifact bytes; the comparison never rewrites source artifacts.",
    )


def _ratio(numerator: int, denominator: int) -> dict[str, Any]:
    """Represent a count and denominator without hiding zero-denominator cases."""

    return {
        "count": numerator,
        "denominator": denominator,
        "rate": None if denominator == 0 else numerator / denominator,
    }


def _metric_delta(before: Any, after: Any) -> Any:
    """Calculate a numerical delta while preserving nonnumeric audit values."""

    if isinstance(before, (int, float)) and isinstance(after, (int, float)):
        return after - before
    return None


def _ledger_levels(ledger_path: Path) -> dict[str, str]:
    """Read L levels only in the external evaluator, never in method execution."""

    ledger = _load(ledger_path)
    return {
        str(issue_id): str(item.get("L"))
        for issue_id, item in (ledger.get("items") or {}).items()
        if isinstance(item, dict) and item.get("L") is not None
    }


def _hit_views(expected_rows: list[dict[str, Any]], levels: dict[str, str]) -> dict[str, Any]:
    """Calculate fixed-denominator hit@1, hit@3, and hit@all from Judge rows."""

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in expected_rows:
        grouped[str(row["expected_id"])].append(row)

    def counts(ids: list[str]) -> dict[str, Any]:
        ordered = [sorted(grouped[issue_id], key=lambda row: int(row["round"])) for issue_id in ids]
        at_one = sum(rows[0]["match_status"] == "FULL" for rows in ordered)
        at_three = sum(any(row["match_status"] == "FULL" for row in rows) for rows in ordered)
        at_all = sum(all(row["match_status"] == "FULL" for row in rows) for rows in ordered)
        return {
            "hit_at_1": _ratio(at_one, len(ordered)),
            "hit_at_3": _ratio(at_three, len(ordered)),
            "hit_at_all": _ratio(at_all, len(ordered)),
        }

    all_ids = sorted(grouped)
    l2_ids = [issue_id for issue_id in all_ids if levels.get(issue_id) == "L2"]
    return {"overall": counts(all_ids), "l2": counts(l2_ids)}


def _receipt_key(receipt: dict[str, Any]) -> str:
    """Key an S2 receipt by exact typed carrier identity rather than a state name."""

    inputs = receipt.get("typed_inputs") or {}
    key = {
        "pair_id": receipt.get("pair_id"),
        "round": receipt.get("round"),
        "predicate_id": receipt.get("predicate_id"),
        "scope": inputs.get("scope"),
        "source": inputs.get("source"),
        "target": inputs.get("target"),
        "transition": inputs.get("transition"),
        "element_refs": inputs.get("element_refs") or [],
    }
    return json.dumps(key, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _semantic_key(report: dict[str, Any]) -> str:
    """Use the method's typed deduplication key, never report prose, for comparison."""

    deduplication = report.get("deduplication") or {}
    semantic_key = deduplication.get("semantic_key") or {}
    key = {
        "semantic_key": semantic_key,
        "predicate_id": report.get("predicate_id"),
    }
    return json.dumps(key, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _report_to_expected(expected_rows: list[dict[str, Any]]) -> dict[str, list[str]]:
    """Map published report IDs to external expected IDs for audit-only attribution."""

    mapping: dict[str, list[str]] = defaultdict(list)
    for row in expected_rows:
        for report in _items(row.get("matching_reports")):
            report_id = report.get("report_id")
            if report_id:
                mapping[str(report_id)].append(str(row["expected_id"]))
    return {key: sorted(set(value)) for key, value in mapping.items()}


def _s2_inventory(
    method_root: Path,
    expected_rows: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    """Collect S2 scope facts from terminal receipts and exact typed report links."""

    report_to_expected = _report_to_expected(expected_rows)
    by_key: dict[str, dict[str, Any]] = {}
    scope_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for method_path in sorted((method_root / "method").glob("*/round-*.json")):
        cell = _load(method_path)
        reports = _items(cell.get("report_issue_clusters"))
        reports_by_inputs: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for report in reports:
            if report.get("predicate_id") != "S2":
                continue
            inputs = report.get("predicate_inputs") or {}
            reports_by_inputs[json.dumps(inputs, ensure_ascii=False, sort_keys=True, separators=(",", ":"))].append(report)
        for receipt in _items(cell.get("predicate_execution_receipts")):
            if receipt.get("predicate_id") != "S2":
                continue
            inputs = receipt.get("typed_inputs") or {}
            scope = str(inputs.get("scope") or "")
            scope_type = "closed_fcstm" if scope == "closed_fcstm" else "owner_local"
            verdict = str(receipt.get("verdict") or "degraded")
            scope_counts[scope_type][verdict] += 1
            report_key = json.dumps(inputs, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            related_reports = reports_by_inputs.get(report_key, [])
            report_ids = sorted(str(report.get("issue_id")) for report in related_reports if report.get("issue_id"))
            expected_ids = sorted({expected for report_id in report_ids for expected in report_to_expected.get(report_id, [])})
            key = _receipt_key({**receipt, "pair_id": cell.get("pair_id"), "round": cell.get("round")})
            by_key[key] = {
                "scope_type": scope_type,
                "verdict": verdict,
                "terminal_state": receipt.get("terminal_state"),
                "carrier": {
                    "scope": inputs.get("scope"),
                    "source": inputs.get("source"),
                    "target": inputs.get("target"),
                    "transition": inputs.get("transition"),
                    "element_refs": inputs.get("element_refs") or [],
                },
                "report_ids": report_ids,
                "expected_ids": expected_ids,
                "reason": receipt.get("reason"),
                "basis": receipt.get("basis"),
            }
    return {
        "scope_counts": {scope: dict(sorted(counts.items())) for scope, counts in sorted(scope_counts.items())},
        "receipt_count": len(by_key),
    }, by_key


def _report_inventory(method_root: Path) -> dict[tuple[str, int], dict[str, dict[str, Any]]]:
    """Index reports by pair-round and typed semantic key for surface comparison."""

    result: dict[tuple[str, int], dict[str, dict[str, Any]]] = {}
    for method_path in sorted((method_root / "method").glob("*/round-*.json")):
        cell = _load(method_path)
        reports: dict[str, dict[str, Any]] = {}
        for report in _items(cell.get("report_issue_clusters")):
            reports[_semantic_key(report)] = {
                "issue_id": report.get("issue_id"),
                "predicate_id": report.get("predicate_id"),
                "witness_level": report.get("witness_level"),
                "d_level": report.get("d_level"),
                "property": report.get("property"),
                "violation_direction": report.get("violation_direction"),
                "locus_names": report.get("locus_names") or [],
            }
        result[(str(cell["pair_id"]), int(cell["round"]))] = reports
    return result


def _expected_changes(
    before_rows: list[dict[str, Any]], after_rows: list[dict[str, Any]]
) -> list[DifferenceRow]:
    """Compare exact external expected relations for the fixed pair-round universe."""

    def index(rows: list[dict[str, Any]]) -> dict[tuple[str, int, str], dict[str, Any]]:
        return {(str(row["pair_id"]), int(row["round"]), str(row["expected_id"])): row for row in rows}

    before_index, after_index = index(before_rows), index(after_rows)
    changes: list[DifferenceRow] = []
    for key in sorted(set(before_index) | set(after_index)):
        before, after = before_index.get(key), after_index.get(key)
        if before and after and before.get("match_status") == after.get("match_status"):
            continue
        changes.append(DifferenceRow(
            key=f"{key[0]}:r{key[1]}:{key[2]}",
            before=None if before is None else {"match_status": before.get("match_status"), "report_ids": before.get("matching_report_ids") or []},
            after=None if after is None else {"match_status": after.get("match_status"), "report_ids": after.get("matching_report_ids") or []},
            reason="The frozen external Judge relation changed for this same expected pair-round position.",
            basis="expected_issue_witness_audit rows keyed by pair_id, round, and expected_id.",
        ))
    return changes


def _report_changes(before_root: Path, after_root: Path) -> list[DifferenceRow]:
    """Compare typed report surfaces without lexical similarity or ledger input."""

    before_index, after_index = _report_inventory(before_root), _report_inventory(after_root)
    changes: list[DifferenceRow] = []
    for cell in sorted(set(before_index) | set(after_index)):
        before_reports, after_reports = before_index.get(cell, {}), after_index.get(cell, {})
        for key in sorted(set(before_reports) | set(after_reports)):
            before, after = before_reports.get(key), after_reports.get(key)
            if before == after:
                continue
            if before is None:
                reason = "Typed report semantic key appears only in the corrected run."
            elif after is None:
                reason = "Typed report semantic key appears only in the baseline run."
            else:
                reason = "The shared typed report key has a changed predicate, W, or D disposition."
            changes.append(DifferenceRow(
                key=f"{cell[0]}:r{cell[1]}:{key}",
                before=before,
                after=after,
                reason=reason,
                basis="method report_issue_clusters deduplication.semantic_key plus predicate/W/D fields.",
            ))
    return changes


def _s2_changes(
    before_inventory: dict[str, dict[str, Any]], after_inventory: dict[str, dict[str, Any]]
) -> tuple[list[DifferenceRow], list[DifferenceRow], list[DifferenceRow], int]:
    """Separate matched-input verdict flips from before-only and after-only carriers."""

    verdict_changes: list[DifferenceRow] = []
    before_only: list[DifferenceRow] = []
    after_only: list[DifferenceRow] = []
    for key in sorted(set(before_inventory) | set(after_inventory)):
        before, after = before_inventory.get(key), after_inventory.get(key)
        if before is None:
            after_only.append(DifferenceRow(
                key=key,
                before=None,
                after=after,
                reason="This exact S2 typed canonical carrier exists only in the after run and is not a same-input verdict comparison.",
                basis="S2 receipt key is pair/round plus scope, canonical source, target, transition, and element refs.",
            ))
            continue
        if after is None:
            before_only.append(DifferenceRow(
                key=key,
                before=before,
                after=None,
                reason="This exact S2 typed canonical carrier exists only in the before run and is not a same-input verdict comparison.",
                basis="S2 receipt key is pair/round plus scope, canonical source, target, transition, and element refs.",
            ))
            continue
        if before.get("verdict") == after.get("verdict"):
            continue
        verdict_changes.append(DifferenceRow(
            key=key,
            before=before,
            after=after,
            reason="The same exact S2 typed canonical carrier has a changed terminal verdict.",
            basis="S2 receipt key is pair/round plus scope, canonical source, target, transition, and element refs.",
        ))
    return verdict_changes, before_only, after_only, len(set(before_inventory) & set(after_inventory))


def _configuration(method_root: Path, judge_root: Path, evaluation: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Extract immutable configuration identity from method and Judge summaries."""

    method_summary = _load(method_root / "summary.json")
    judge_summary = _load(judge_root / "summary.json")
    return (
        {
            "run_id": method_summary.get("run_id"),
            "source_commit": method_summary.get("source_commit"),
            "profile": method_summary.get("profile"),
            "run_contract_hash": method_summary.get("run_contract_hash"),
            "registry_hash": method_summary.get("registry_hash"),
            "rounds": method_summary.get("rounds"),
            "workers": method_summary.get("workers"),
            "transport_retries": method_summary.get("transport_retries"),
            "input_hashes": evaluation.get("method", {}).get("metrics", {}).get("input_hashes"),
        },
        {
            "semantic_judge_commit": judge_summary.get("semantic_judge_commit"),
            "protocol_sha256": judge_summary.get("protocol_sha256"),
            "judge_algorithm_version": judge_summary.get("judge_algorithm_version"),
            "model_profile": judge_summary.get("model_profile"),
            "source_runs": [
                {
                    "run_id": source.get("run_id"),
                    "selected_rounds": source.get("selected_rounds"),
                    "workers": _load(Path(str(source["manifest_path"]))).get("workers"),
                }
                for source in _items(judge_summary.get("source_runs"))
            ],
        },
    )


def _side(
    *,
    label: str,
    method_root: Path,
    judge_root: Path,
    evaluator_root: Path,
    levels: dict[str, str],
) -> tuple[ComparisonSide, list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Construct one read-only snapshot and its detailed comparison indexes."""

    evaluation_path = evaluator_root / "evaluation_summary.json"
    expected_path = evaluator_root / "expected_issue_witness_audit.json"
    cost_path = evaluator_root / "judge_cost_audit.json"
    evaluation, expected, cost = _load(evaluation_path), _load(expected_path), _load(cost_path)
    expected_rows = _items(expected.get("rows"))
    method_configuration, judge_configuration = _configuration(method_root, judge_root, evaluation)
    s2_summary, s2_inventory = _s2_inventory(method_root, expected_rows)
    judge = evaluation.get("judge") or {}
    witness = evaluation.get("witness_ledger") or {}
    outcomes = {
        "hit_views": _hit_views(expected_rows, levels),
        "occurrence_overall": judge.get("overall"),
        "l2_occurrence": {
            "full": _ratio(int(judge.get("l2_full_hit_count") or 0), int(judge.get("l2_expected_count") or 0)),
            "supported": _ratio(int(judge.get("l2_supported_count") or 0), int(judge.get("l2_expected_count") or 0)),
        },
        "match_counts": witness.get("match_counts"),
        "full_hit_max_witness": {
            "full_expected_count": witness.get("full_expected_count"),
            "full_max_w2_count": witness.get("full_max_w2_count"),
            "full_max_w2_share": witness.get("full_max_w2_share"),
            "max_witness_counts": witness.get("max_witness_counts"),
        },
    }
    evidence = {
        "all_evidence_witness_levels": (evaluation.get("method") or {}).get("witness_levels"),
        "predicate_feasibility": evaluation.get("predicate_feasibility"),
    }
    costs = {
        "method_cost_usd": _load(method_root / "summary.json").get("method_cost_usd"),
        "judge_total_incurred_cost_usd": judge.get("total_judge_cost_usd"),
        "judge_cost_audit": cost,
    }
    return ComparisonSide(
        label=label,
        method_root=_reference(method_root / "summary.json", "Completed immutable method summary."),
        judge_root=_reference(judge_root / "summary.json", "Completed immutable frozen-Judge composite."),
        evaluation_summary=_reference(evaluation_path, "Evaluator-only aggregate over immutable method and Judge artifacts."),
        expected_witness_audit=_reference(expected_path, "Evaluator-only expected relation and witness audit."),
        method_configuration=method_configuration,
        judge_configuration=judge_configuration,
        outcomes=outcomes,
        evidence=evidence,
        costs=costs,
        s2_scope=s2_summary,
    ), expected_rows, s2_inventory


def _aggregate_deltas(before: ComparisonSide, after: ComparisonSide) -> dict[str, Any]:
    """Calculate high-level deltas without substituting aggregate findings for witnesses."""

    before_overall = before.outcomes["occurrence_overall"] or {}
    after_overall = after.outcomes["occurrence_overall"] or {}
    before_l2 = before.outcomes["l2_occurrence"]["full"]
    after_l2 = after.outcomes["l2_occurrence"]["full"]
    before_w2 = before.outcomes["full_hit_max_witness"]
    after_w2 = after.outcomes["full_hit_max_witness"]
    return {
        "overall_full_hit": {
            "before": _ratio(int(before_overall.get("full_hit_count") or 0), int(before_overall.get("expected_count") or 0)),
            "after": _ratio(int(after_overall.get("full_hit_count") or 0), int(after_overall.get("expected_count") or 0)),
            "count_delta": _metric_delta(before_overall.get("full_hit_count"), after_overall.get("full_hit_count")),
            "rate_delta": _metric_delta(before_overall.get("hit_rate"), after_overall.get("hit_rate")),
        },
        "l2_full_hit": {
            "before": before_l2,
            "after": after_l2,
            "count_delta": _metric_delta(before_l2.get("count"), after_l2.get("count")),
            "rate_delta": _metric_delta(before_l2.get("rate"), after_l2.get("rate")),
        },
        "semantic_precision": {
            "before": before_overall.get("semantic_precision"),
            "after": after_overall.get("semantic_precision"),
            "delta": _metric_delta(before_overall.get("semantic_precision"), after_overall.get("semantic_precision")),
        },
        "full_hit_max_w2_share": {
            "before": before_w2.get("full_max_w2_share"),
            "after": after_w2.get("full_max_w2_share"),
            "delta": _metric_delta(before_w2.get("full_max_w2_share"), after_w2.get("full_max_w2_share")),
        },
        "cost_usd": {
            "method_before": before.costs.get("method_cost_usd"),
            "method_after": after.costs.get("method_cost_usd"),
            "method_delta": _metric_delta(before.costs.get("method_cost_usd"), after.costs.get("method_cost_usd")),
            "judge_before": before.costs.get("judge_total_incurred_cost_usd"),
            "judge_after": after.costs.get("judge_total_incurred_cost_usd"),
            "judge_delta": _metric_delta(before.costs.get("judge_total_incurred_cost_usd"), after.costs.get("judge_total_incurred_cost_usd")),
        },
    }


def build_paired_comparison(
    *,
    before_method_root: str | Path,
    before_judge_root: str | Path,
    before_evaluator_root: str | Path,
    after_method_root: str | Path,
    after_judge_root: str | Path,
    after_evaluator_root: str | Path,
    ledger_path: str | Path,
) -> PairedComparisonArtifact:
    """Compare immutable full-scale results without modifying method or Judge surfaces."""

    levels = _ledger_levels(Path(ledger_path).expanduser().resolve())
    before, before_rows, before_s2 = _side(
        label="before_soundness_s2_correction",
        method_root=Path(before_method_root).expanduser().resolve(),
        judge_root=Path(before_judge_root).expanduser().resolve(),
        evaluator_root=Path(before_evaluator_root).expanduser().resolve(),
        levels=levels,
    )
    after, after_rows, after_s2 = _side(
        label="after_soundness_s2_correction",
        method_root=Path(after_method_root).expanduser().resolve(),
        judge_root=Path(after_judge_root).expanduser().resolve(),
        evaluator_root=Path(after_evaluator_root).expanduser().resolve(),
        levels=levels,
    )
    matched_input_verdict_flips, before_only_carriers, after_only_carriers, matched_input_carrier_count = _s2_changes(before_s2, after_s2)
    return PairedComparisonArtifact(
        before=before,
        after=after,
        aggregate_deltas=_aggregate_deltas(before, after),
        expected_relation_changes=_expected_changes(before_rows, after_rows),
        report_surface_changes=_report_changes(
            Path(before_method_root).expanduser().resolve(),
            Path(after_method_root).expanduser().resolve(),
        ),
        matched_input_verdict_flips=matched_input_verdict_flips,
        before_only_carriers=before_only_carriers,
        after_only_carriers=after_only_carriers,
        matched_input_carrier_count=matched_input_carrier_count,
        sampling_interpretation=(
            "Both sides use the same fixed input universe and frozen Judge, but each method round is a fresh LLM sample. "
            "A one-pair/round delta is therefore recorded as an observed paired difference, not attributed solely to "
            "the soundness/S2 implementation without additional controlled sampling."
        ),
        reason=(
            "This evaluator-only artifact compares completed immutable results after the soundness-fragment and S2-scope correction. "
            "It never feeds expected issues, Judge outcomes, or historical reports into method execution."
        ),
        basis=(
            "Frozen method/Judge/evaluator artifact bytes; ledger L labels are read only for external L2 denominators; "
            "report comparison uses typed semantic keys and S2 comparison uses exact typed canonical carriers."
        ),
    )


def _markdown(artifact: PairedComparisonArtifact) -> str:
    """Render a concise Chinese handoff summary from the machine-readable artifact."""

    delta = artifact.aggregate_deltas
    overall = delta["overall_full_hit"]
    l2 = delta["l2_full_hit"]
    precision = delta["semantic_precision"]
    w2 = delta["full_hit_max_w2_share"]
    return "\n".join([
        "# Soundness/S2 Before-After Audit",
        "",
        "- \u8fd9\u662f\u4e00\u4efd evaluator-only \u914d\u5bf9\u6bd4\u8f83\uff1bmethod \u4e0e\u51bb\u7ed3 Judge \u5236\u54c1\u5747\u4fdd\u6301\u4e0d\u53ef\u53d8\u3002",
        f"- Overall FULL: {overall['before']['count']}/{overall['before']['denominator']} -> {overall['after']['count']}/{overall['after']['denominator']} (delta {overall['count_delta']:+}).",
        f"- L2 FULL: {l2['before']['count']}/{l2['before']['denominator']} -> {l2['after']['count']}/{l2['after']['denominator']} (delta {l2['count_delta']:+}).",
        f"- Semantic precision: {precision['before']:.4f} -> {precision['after']:.4f} (delta {precision['delta']:+.4f}).",
        f"- FULL-hit max-W2 share: {w2['before']:.4f} -> {w2['after']:.4f} (delta {w2['delta']:+.4f}).",
        _s2_summary_line(artifact),
        f"- Expected pair-round relation changes: {len(artifact.expected_relation_changes)}; typed report-surface changes: {len(artifact.report_surface_changes)}.",
        "- \u5355\u6b21\u914d\u5bf9\u7ed3\u679c\u4ecd\u5305\u542b\u65b0 LLM \u91c7\u6837\u6ce2\u52a8\uff1b\u672c\u6458\u8981\u4e0d\u5c06\u4efb\u4e00\u5355\u683c\u5dee\u5f02\u5355\u72ec\u5f52\u56e0\u4e8e soundness \u6216 S2 \u4fee\u6b63\u3002",
        "",
    ])


def _s2_summary_line(artifact: PairedComparisonArtifact) -> str:
    """Render the three mutually exclusive S2 comparison counts from JSON fields."""

    return (
        f"- S2 matched-input verdict flips: {len(artifact.matched_input_verdict_flips)}/{artifact.matched_input_carrier_count}; "
        f"before-only carriers: {len(artifact.before_only_carriers)}; after-only carriers: {len(artifact.after_only_carriers)}."
    )


def _parser() -> argparse.ArgumentParser:
    """Create the explicit external-artifact CLI contract."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before-method-root", type=Path, required=True)
    parser.add_argument("--before-judge-root", type=Path, required=True)
    parser.add_argument("--before-evaluator-root", type=Path, required=True)
    parser.add_argument("--after-method-root", type=Path, required=True)
    parser.add_argument("--after-judge-root", type=Path, required=True)
    parser.add_argument("--after-evaluator-root", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary-cn", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Write the JSON comparison and its concise Chinese evaluator handoff."""

    args = _parser().parse_args(argv)
    artifact = build_paired_comparison(
        before_method_root=args.before_method_root,
        before_judge_root=args.before_judge_root,
        before_evaluator_root=args.before_evaluator_root,
        after_method_root=args.after_method_root,
        after_judge_root=args.after_judge_root,
        after_evaluator_root=args.after_evaluator_root,
        ledger_path=args.ledger,
    )
    write_json(args.output, artifact.model_dump(mode="json"))
    args.summary_cn.parent.mkdir(parents=True, exist_ok=True)
    args.summary_cn.write_text(_markdown(artifact), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
