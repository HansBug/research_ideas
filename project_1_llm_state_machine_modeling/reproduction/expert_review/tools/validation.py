from __future__ import annotations

from typing import Any

from ..expert_review_schema import DimensionReviewResult, ElementIssue, EvidenceItem, ExpertReviewResult, RequirementTraceResult


def status_counts(results: list[RequirementTraceResult]) -> tuple[int, int, int]:
    matched = sum(1 for item in results if item.status == "matched")
    partial = sum(1 for item in results if item.status == "partial")
    missing = sum(1 for item in results if item.status == "missing")
    return matched, partial, missing


def json_safe_report(report: dict[str, Any]) -> dict[str, Any]:
    safe: dict[str, Any] = {}
    for key, value in report.items():
        if isinstance(value, list) and value and isinstance(value[0], ElementIssue):
            safe[key] = [
                {
                    "element_id": item.element_id,
                    "element_kind": item.element_kind,
                    "element_text": item.element_text,
                    "issue_type": item.issue_type,
                    "reason_text": item.reason_text,
                }
                for item in value
            ]
        elif isinstance(value, list) and value and isinstance(value[0], EvidenceItem):
            safe[key] = [
                {
                    "source": item.source,
                    "locator": item.locator,
                    "snippet": item.snippet,
                    "explanation": item.explanation,
                }
                for item in value
            ]
        elif isinstance(value, list):
            safe[key] = value
        else:
            safe[key] = value
    return safe


def evidence_summary_from_dimensions(dimension_results: list[DimensionReviewResult]) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    for dimension in dimension_results:
        items.extend(dimension.evidence[:1])
    return items[:8]


def validate_result_shape(result: ExpertReviewResult) -> ExpertReviewResult:
    result.notes = [str(item) for item in result.notes if str(item).strip()]
    result.dimension_results = list(result.dimension_results)
    result.requirement_trace_results = list(result.requirement_trace_results)
    result.unsupported_model_elements = list(result.unsupported_model_elements)
    result.evidence_summary = list(result.evidence_summary)
    return result


__all__ = [
    "evidence_summary_from_dimensions",
    "json_safe_report",
    "status_counts",
    "validate_result_shape",
]
