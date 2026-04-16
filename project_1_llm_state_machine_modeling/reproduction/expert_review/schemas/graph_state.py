from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .dossiers import ArtifactDossier, EvidenceRegime, InputDossier, ReviewContract
from .request import ExpertReviewRequest
from .result import ExpertReviewResult


@dataclass(slots=True)
class ReviewGraphState:
    request: ExpertReviewRequest
    llm: Any | None = None
    llm_model_name: str | None = None
    llm_provider: str | None = None
    backend_label: str = "langgraph_multi_agent_v1"
    notes: list[str] = field(default_factory=list)
    contract: ReviewContract | None = None
    regime: EvidenceRegime | None = None
    input_dossier: InputDossier | None = None
    pred_dossier: ArtifactDossier | None = None
    ref_dossier: ArtifactDossier | None = None
    policy_packet: dict[str, Any] = field(default_factory=dict)
    dimensions: list[Any] = field(default_factory=list)
    trace_results: list[Any] = field(default_factory=list)
    equivalence_report: dict[str, Any] = field(default_factory=dict)
    quality_report: dict[str, Any] = field(default_factory=dict)
    evidence_critic: dict[str, Any] = field(default_factory=dict)
    dimension_results: list[Any] = field(default_factory=list)
    harmful_issues: list[Any] = field(default_factory=list)
    overall_score: float = 0.0
    confidence: float = 0.0
    result: ExpertReviewResult | None = None
    context_packets: dict[str, dict[str, Any]] = field(default_factory=dict)
    fanout_log: list[str] = field(default_factory=list)
    arbitration_log: list[str] = field(default_factory=list)


__all__ = ["ReviewGraphState"]
