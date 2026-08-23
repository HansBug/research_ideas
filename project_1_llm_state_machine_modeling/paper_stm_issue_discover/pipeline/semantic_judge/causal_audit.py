"""Deterministic exact source-unit plans for complete causal-field audits."""

from __future__ import annotations

import hashlib
import json

from .models import (
    CandidateReport,
    CausalAuditPlan,
    CausalAuditUnit,
    CausalFieldAuditPlan,
    CausalReportField,
    ReportCausalAuditPlan,
    ReportCoreEnvelope,
    ReportFieldClausePlan,
    ReportSourceClause,
    ValidityReportField,
)

MAX_SOURCE_UNIT_CHARACTERS = 64
_SENTENCE_BOUNDARIES = frozenset(".!?;。！？；\n")
_PREFERRED_CHUNK_BOUNDARIES = frozenset(",，:")
_VALIDITY_FIELDS = (
    ValidityReportField.CLAIM,
    ValidityReportField.PROPERTY,
    ValidityReportField.VIOLATED_OBLIGATION,
    ValidityReportField.EXPECTED,
    ValidityReportField.OBSERVED,
    ValidityReportField.REASON,
    ValidityReportField.BASIS,
)
_CORE_VALIDITY_FIELDS = frozenset(_VALIDITY_FIELDS) - {
    ValidityReportField.BASIS
}


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


def report_core_envelope_hash(
    report_id: str,
    field_plans: tuple[ReportFieldClausePlan, ...],
) -> str:
    """Hash the immutable report ID and complete validity clause partition."""

    payload = {
        "schema_version": "semantic-judge.report-core-envelope.v1",
        "report_id": report_id,
        "field_plans": [item.model_dump(mode="json") for item in field_plans],
    }
    serialized = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return "sha256:" + hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def build_report_core_envelope(report: CandidateReport) -> ReportCoreEnvelope:
    """Build a deterministic expected-isolated clause closure for one report."""

    field_plans = []
    for report_field in _VALIDITY_FIELDS:
        text = getattr(report, report_field.value)
        if not isinstance(text, str):
            continue
        clauses = tuple(
            ReportSourceClause(
                clause_id=f"C{index}",
                source_start=start,
                source_end=end,
                exact_text=text[start:end],
                exact_text_sha256="sha256:"
                + hashlib.sha256(text[start:end].encode("utf-8")).hexdigest(),
            )
            for index, (start, end) in enumerate(_bounded_segments(text), start=1)
        )
        field_plans.append(
            ReportFieldClausePlan(
                report_field=report_field,
                is_core_field=report_field in _CORE_VALIDITY_FIELDS,
                clauses=clauses,
            )
        )
    frozen_plans = tuple(field_plans)
    return ReportCoreEnvelope(
        report_id=report.report_id,
        field_plans=frozen_plans,
        envelope_hash=report_core_envelope_hash(report.report_id, frozen_plans),
        reason="The envelope includes claim, reason, and every non-null semantic or evidence field while excluding the locus-only where field.",
        basis=f"Deterministic gap-free source partition with a maximum of {MAX_SOURCE_UNIT_CHARACTERS} characters per clause and exact SHA-256 text hashes.",
    )
