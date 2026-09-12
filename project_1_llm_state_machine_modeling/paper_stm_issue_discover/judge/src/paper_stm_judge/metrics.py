"""Deterministic issue #195 metrics and provider-external ID decoding."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from .models import (
    AdapterAudit,
    ExpectedOutcome,
    JudgeReading,
    ReportOutcome,
    ReportValidity,
    SemanticMetrics,
    a0_subtype_of,
    defect_tier_of,
)


def _rate(numerator: int, denominator: int, *, empty: float = 0.0) -> float:
    return numerator / denominator if denominator else empty


def compute_semantic_metrics(reading: JudgeReading) -> SemanticMetrics:
    """Compute all pair metrics from a fully validated final reading."""

    reports = tuple(reading.report_assessments)
    expected = tuple(reading.expected_assessments)
    full_hit_count = sum(row.hit for row in expected)
    supported_count = sum(row.supported for row in expected)
    valid_known_count = sum(row.validity == ReportValidity.VALID_KNOWN for row in reports)
    valid_novel_count = sum(row.validity == ReportValidity.VALID_NOVEL for row in reports)
    invalid_count = sum(row.validity == ReportValidity.INVALID for row in reports)
    valid_count = valid_known_count + valid_novel_count
    ledger_unmatched_count = sum(
        row.validity in {ReportValidity.VALID_NOVEL, ReportValidity.INVALID}
        or (
            row.validity == ReportValidity.VALID_KNOWN
            and not row.full_expected_ids
        )
        for row in reports
    )
    clusters: dict[str, list[ReportValidity]] = defaultdict(list)
    for row in reports:
        clusters[row.root_cause_cluster_key].append(row.validity)
    valid_cluster_keys = {
        key
        for key, values in clusters.items()
        if any(value != ReportValidity.INVALID for value in values)
    }
    invalid_cluster_keys = set(clusters) - valid_cluster_keys
    valid_report_keys = {
        row.root_cause_cluster_key
        for row in reports
        if row.validity != ReportValidity.INVALID
    }
    return SemanticMetrics(
        expected_count=len(expected),
        full_hit_count=full_hit_count,
        fn_count=len(expected) - full_hit_count,
        supported_count=supported_count,
        hit_rate=_rate(full_hit_count, len(expected)),
        supported_rate=_rate(supported_count, len(expected)),
        report_count=len(reports),
        valid_known_count=valid_known_count,
        valid_novel_count=valid_novel_count,
        invalid_count=invalid_count,
        semantic_precision=_rate(valid_count, len(reports), empty=1.0),
        ledger_unmatched_count=ledger_unmatched_count,
        cluster_count=len(clusters),
        valid_cluster_count=len(valid_cluster_keys),
        invalid_cluster_count=len(invalid_cluster_keys),
        root_cause_cluster_precision=_rate(
            len(valid_cluster_keys), len(clusters), empty=1.0
        ),
        redundancy_rate=_rate(len(reports) - len(clusters), len(reports)),
        valid_redundancy_rate=_rate(
            valid_count - len(valid_report_keys), valid_count
        ),
        reason="Metrics count unique FULL-hit and supported expected issues; only INVALID reports are semantic false positives; duplicate reports are measured as redundancy.",
        basis="GitHub issue #195 section 4 formulas applied deterministically to the final exact-closure reading.",
    )


def decode_outcomes(
    reading: JudgeReading,
    adapter_audit: AdapterAudit,
) -> tuple[tuple[ReportOutcome, ...], tuple[ExpectedOutcome, ...]]:
    """Restore original artifact IDs after all provider-visible judging is complete."""

    report_map = {
        row.anonymous_id: row.original_id for row in adapter_audit.report_id_map
    }
    expected_map = {
        row.anonymous_id: row.original_id for row in adapter_audit.expected_id_map
    }
    report_outcomes = tuple(
        ReportOutcome(
            original_report_id=report_map[row.report_id],
            validity=row.validity,
            defect_class=row.defect_class,
            d_tier=(
                defect_tier_of(row.defect_class) if row.defect_class is not None else None
            ),
            a0_subtype=(
                a0_subtype_of(row.defect_class) if row.defect_class is not None else None
            ),
            full_ledger_ids=tuple(expected_map[value] for value in row.full_expected_ids),
            partial_ledger_ids=tuple(
                expected_map[value] for value in row.partial_expected_ids
            ),
            root_cause_cluster_key=row.root_cause_cluster_key,
            reason=row.reason,
            basis=row.basis,
            source_refs=row.source_refs,
        )
        for row in reading.report_assessments
    )
    expected_outcomes = tuple(
        ExpectedOutcome(
            ledger_id=expected_map[row.expected_id],
            hit=row.hit,
            supported=row.supported,
            full_report_ids=tuple(report_map[value] for value in row.full_report_ids),
            partial_report_ids=tuple(
                report_map[value] for value in row.partial_report_ids
            ),
            reason=row.reason,
            basis=row.basis,
            source_refs=row.source_refs,
        )
        for row in reading.expected_assessments
    )
    return report_outcomes, expected_outcomes


def aggregate_outcomes(
    report_groups: Iterable[tuple[str, ReportOutcome]],
    expected_groups: Iterable[tuple[str, ExpectedOutcome]],
) -> SemanticMetrics:
    """Aggregate pair/run outcomes while namespacing root-cause clusters by pair."""

    reports = tuple(report_groups)
    expected = tuple(expected_groups)
    full_hit_count = sum(outcome.hit for _, outcome in expected)
    supported_count = sum(outcome.supported for _, outcome in expected)
    known = sum(outcome.validity == ReportValidity.VALID_KNOWN for _, outcome in reports)
    novel = sum(outcome.validity == ReportValidity.VALID_NOVEL for _, outcome in reports)
    invalid = sum(outcome.validity == ReportValidity.INVALID for _, outcome in reports)
    valid_count = known + novel
    unmatched = sum(
        outcome.validity in {ReportValidity.VALID_NOVEL, ReportValidity.INVALID}
        or (
            outcome.validity == ReportValidity.VALID_KNOWN
            and not outcome.full_ledger_ids
        )
        for _, outcome in reports
    )
    clusters: dict[tuple[str, str], list[ReportValidity]] = defaultdict(list)
    for pair_id, outcome in reports:
        clusters[(pair_id, outcome.root_cause_cluster_key)].append(outcome.validity)
    valid_cluster_keys = {
        key
        for key, values in clusters.items()
        if any(value != ReportValidity.INVALID for value in values)
    }
    invalid_cluster_keys = set(clusters) - valid_cluster_keys
    valid_report_cluster_keys = {
        (pair_id, outcome.root_cause_cluster_key)
        for pair_id, outcome in reports
        if outcome.validity != ReportValidity.INVALID
    }
    return SemanticMetrics(
        expected_count=len(expected),
        full_hit_count=full_hit_count,
        fn_count=len(expected) - full_hit_count,
        supported_count=supported_count,
        hit_rate=_rate(full_hit_count, len(expected)),
        supported_rate=_rate(supported_count, len(expected)),
        report_count=len(reports),
        valid_known_count=known,
        valid_novel_count=novel,
        invalid_count=invalid,
        semantic_precision=_rate(valid_count, len(reports), empty=1.0),
        ledger_unmatched_count=unmatched,
        cluster_count=len(clusters),
        valid_cluster_count=len(valid_cluster_keys),
        invalid_cluster_count=len(invalid_cluster_keys),
        root_cause_cluster_precision=_rate(
            len(valid_cluster_keys), len(clusters), empty=1.0
        ),
        redundancy_rate=_rate(len(reports) - len(clusters), len(reports)),
        valid_redundancy_rate=_rate(
            valid_count - len(valid_report_cluster_keys), valid_count
        ),
        reason="Run metrics aggregate exact pair outcomes; clusters are pair-namespaced and INVALID remains the only semantic false positive.",
        basis="Deterministic aggregation of PairJudgeResult report_outcomes and expected_outcomes under issue #195.",
    )
