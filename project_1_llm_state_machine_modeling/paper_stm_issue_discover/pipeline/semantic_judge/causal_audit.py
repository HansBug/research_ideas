"""Deterministic exact source-unit plans for complete causal-field audits."""

from __future__ import annotations

import hashlib

from .models import (
    CandidateReport,
    CausalAuditPlan,
    CausalAuditUnit,
    CausalFieldAuditPlan,
    CausalReportField,
    ReportCausalAuditPlan,
)

MAX_SOURCE_UNIT_CHARACTERS = 64
_SENTENCE_BOUNDARIES = frozenset(".!?;。！？；\n")
_PREFERRED_CHUNK_BOUNDARIES = frozenset(",，:")


def _sentence_segments(text: str) -> tuple[tuple[int, int], ...]:
    """Partition complete text at explicit sentence boundaries without gaps."""

    segments: list[tuple[int, int]] = []
    start = 0
    index = 0
    while index < len(text):
        index += 1
        if text[index - 1] not in _SENTENCE_BOUNDARIES:
            continue
        while index < len(text) and text[index].isspace():
            index += 1
        segments.append((start, index))
        start = index
    if start < len(text):
        segments.append((start, len(text)))
    if not segments:
        segments.append((0, len(text)))
    return tuple(segments)


def _bounded_segments(text: str) -> tuple[tuple[int, int], ...]:
    """Bound every source unit while preferring readable punctuation cuts."""

    bounded: list[tuple[int, int]] = []
    for segment_start, segment_end in _sentence_segments(text):
        start = segment_start
        while segment_end - start > MAX_SOURCE_UNIT_CHARACTERS:
            hard_end = start + MAX_SOURCE_UNIT_CHARACTERS
            preferred_end = next(
                (
                    position + 1
                    for position in range(hard_end - 1, start + 31, -1)
                    if text[position] in _PREFERRED_CHUNK_BOUNDARIES
                ),
                hard_end,
            )
            bounded.append((start, preferred_end))
            start = preferred_end
        if start < segment_end:
            bounded.append((start, segment_end))
    return tuple(bounded)


def build_causal_audit_plan(
    reports: tuple[CandidateReport, ...],
) -> CausalAuditPlan:
    """Build the same gap-free causal source partition for either report adapter."""

    report_plans: list[ReportCausalAuditPlan] = []
    for report in reports:
        field_plans: list[CausalFieldAuditPlan] = []
        for field_name in ("reason", "basis", "observed"):
            text = getattr(report, field_name)
            if not isinstance(text, str):
                continue
            units = tuple(
                CausalAuditUnit(
                    assertion_id=f"A{index}",
                    source_start=start,
                    source_end=end,
                    exact_source_quote=text[start:end],
                    exact_source_sha256="sha256:"
                    + hashlib.sha256(text[start:end].encode("utf-8")).hexdigest(),
                )
                for index, (start, end) in enumerate(
                    _bounded_segments(text), start=1
                )
            )
            field_plans.append(
                CausalFieldAuditPlan(
                    report_field=CausalReportField(field_name),
                    source_units=units,
                )
            )
        report_plans.append(
            ReportCausalAuditPlan(
                report_id=report.report_id,
                field_plans=tuple(field_plans),
            )
        )
    return CausalAuditPlan(report_plans=tuple(report_plans))
