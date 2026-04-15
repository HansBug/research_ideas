from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class DimensionDefinition:
    name: str
    title: str
    description: str
    weight: float = 1.0
    scoring_mode: str = "continuous_0_1"
    positive_examples: list[str] = field(default_factory=list)
    negative_examples: list[str] = field(default_factory=list)
    scoring_notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class EvidenceItem:
    source: str
    snippet: str
    explanation: str
    locator: str | None = None


@dataclass(slots=True)
class TraceLink:
    source_id: str
    target_id: str
    relation: str
    reason_text: str


@dataclass(slots=True)
class RequirementTraceResult:
    requirement_id: str
    requirement_text: str
    status: str
    reason_text: str
    matched_element_ids: list[str] = field(default_factory=list)
    confidence: float = 0.5


@dataclass(slots=True)
class ElementIssue:
    element_id: str
    element_kind: str
    element_text: str
    issue_type: str
    reason_text: str


@dataclass(slots=True)
class DimensionReviewResult:
    dimension_name: str
    title: str
    score: float
    judgement: str
    reason_text: str
    evidence: list[EvidenceItem] = field(default_factory=list)
    trace_links: list[TraceLink] = field(default_factory=list)
    issues: list[ElementIssue] = field(default_factory=list)
    metric_payload: dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.5


@dataclass(slots=True)
class ExpertReviewRequest:
    prompt: str
    input_text: str
    pred_output: str
    ref_output: str | None = None


@dataclass(slots=True)
class ExpertReviewResult:
    prompt: str
    overall_score: float
    overall_judgement: str
    overall_reason_text: str
    used_review_backend: str
    dimension_results: list[DimensionReviewResult] = field(default_factory=list)
    requirement_trace_results: list[RequirementTraceResult] = field(default_factory=list)
    unsupported_model_elements: list[ElementIssue] = field(default_factory=list)
    evidence_summary: list[EvidenceItem] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    llm_model_name: str | None = None
    llm_provider: str | None = None
    confidence: float = 0.5


def judgement_from_score(score: float) -> str:
    if score >= 0.9:
        return "excellent"
    if score >= 0.75:
        return "good"
    if score >= 0.55:
        return "acceptable"
    if score >= 0.35:
        return "weak"
    return "poor"


def to_dict(value: Any) -> Any:
    return asdict(value)


def to_json(value: Any) -> str:
    return json.dumps(asdict(value), ensure_ascii=False, indent=2)


def evidence_item_from_dict(payload: dict[str, Any]) -> EvidenceItem:
    return EvidenceItem(
        source=str(payload.get("source", "")),
        locator=payload.get("locator"),
        snippet=str(payload.get("snippet", "")),
        explanation=str(payload.get("explanation", "")),
    )


def trace_link_from_dict(payload: dict[str, Any]) -> TraceLink:
    return TraceLink(
        source_id=str(payload.get("source_id", "")),
        target_id=str(payload.get("target_id", "")),
        relation=str(payload.get("relation", "")),
        reason_text=str(payload.get("reason_text", "")),
    )


def element_issue_from_dict(payload: dict[str, Any]) -> ElementIssue:
    return ElementIssue(
        element_id=str(payload.get("element_id", "")),
        element_kind=str(payload.get("element_kind", "")),
        element_text=str(payload.get("element_text", "")),
        issue_type=str(payload.get("issue_type", "")),
        reason_text=str(payload.get("reason_text", "")),
    )


def requirement_trace_from_dict(payload: dict[str, Any]) -> RequirementTraceResult:
    return RequirementTraceResult(
        requirement_id=str(payload.get("requirement_id", "")),
        requirement_text=str(payload.get("requirement_text", "")),
        status=str(payload.get("status", "")),
        matched_element_ids=[str(item) for item in payload.get("matched_element_ids", [])],
        reason_text=str(payload.get("reason_text", "")),
        confidence=float(payload.get("confidence", 0.5)),
    )


def dimension_review_from_dict(payload: dict[str, Any]) -> DimensionReviewResult:
    return DimensionReviewResult(
        dimension_name=str(payload.get("dimension_name", "")),
        title=str(payload.get("title", "")),
        score=float(payload.get("score", 0.0)),
        judgement=str(payload.get("judgement", "")),
        reason_text=str(payload.get("reason_text", "")),
        evidence=[evidence_item_from_dict(item) for item in payload.get("evidence", [])],
        trace_links=[trace_link_from_dict(item) for item in payload.get("trace_links", [])],
        issues=[element_issue_from_dict(item) for item in payload.get("issues", [])],
        metric_payload=dict(payload.get("metric_payload", {})),
        confidence=float(payload.get("confidence", 0.5)),
    )


def result_to_flat_row(result: ExpertReviewResult) -> dict[str, Any]:
    return {
        "prompt": result.prompt,
        "used_review_backend": result.used_review_backend,
        "llm_model_name": result.llm_model_name,
        "llm_provider": result.llm_provider,
        "overall_score": result.overall_score,
        "overall_judgement": result.overall_judgement,
        "overall_reason_text": result.overall_reason_text,
        "dimension_results_json": json.dumps(
            [asdict(item) for item in result.dimension_results],
            ensure_ascii=False,
            sort_keys=True,
        ),
        "requirement_trace_results_json": json.dumps(
            [asdict(item) for item in result.requirement_trace_results],
            ensure_ascii=False,
            sort_keys=True,
        ),
        "unsupported_model_elements_json": json.dumps(
            [asdict(item) for item in result.unsupported_model_elements],
            ensure_ascii=False,
            sort_keys=True,
        ),
        "evidence_summary_json": json.dumps(
            [asdict(item) for item in result.evidence_summary],
            ensure_ascii=False,
            sort_keys=True,
        ),
        "notes_json": json.dumps(result.notes, ensure_ascii=False, sort_keys=True),
        "confidence": result.confidence,
    }
