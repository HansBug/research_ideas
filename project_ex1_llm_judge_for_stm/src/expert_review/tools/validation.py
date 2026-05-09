"""``validation`` 模块。

**作用**：本模块属于 ``expert_review`` 体系内的辅助实现层；具体职责
由内部 class / function 的 docstring 描述。

**设计思路**：见包级 :mod:`expert_review.tools` 文档与
``PYDOC_INVENTORY.md`` 盘点清单。
"""
from __future__ import annotations

from typing import Any

from ..schema import DimensionReviewResult, ElementIssue, EvidenceItem, ExpertReviewResult, RequirementTraceResult


def status_counts(results: list[RequirementTraceResult]) -> tuple[int, int, int]:
    """``status_counts`` 函数。

    :param results: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    matched = sum(1 for item in results if item.status == "matched")
    partial = sum(1 for item in results if item.status == "partial")
    missing = sum(1 for item in results if item.status == "missing")
    return matched, partial, missing


def json_safe_report(report: dict[str, Any]) -> dict[str, Any]:
    """``json_safe_report`` 函数。

    :param report: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
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
    """``evidence_summary_from_dimensions`` 函数。

    :param dimension_results: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    items: list[EvidenceItem] = []
    seen: set[tuple[str, str, str]] = set()
    for dimension in dimension_results:
        ranked = sorted(
            dimension.evidence,
            key=lambda item: (
                not bool(str(item.locator or "").strip()),
                not bool(str(item.snippet or "").strip()),
                not bool(str(item.explanation or "").strip()),
            ),
        )
        for item in ranked:
            key = (
                str(item.source or "").strip(),
                str(item.locator or "").strip(),
                str(item.snippet or "").strip(),
            )
            if key in seen:
                continue
            seen.add(key)
            items.append(item)
            break
    return items[:8]


def validate_result_shape(result: ExpertReviewResult) -> ExpertReviewResult:
    """``validate_result_shape`` 函数。

    :param result: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
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