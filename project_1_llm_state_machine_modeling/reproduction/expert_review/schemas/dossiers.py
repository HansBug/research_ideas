from __future__ import annotations

from dataclasses import dataclass, field

from ..expert_review_schema import EvidenceItem, RequirementTraceResult


@dataclass(slots=True)
class ReviewContract:
    task_summary: str
    requested_focus: list[str] = field(default_factory=list)
    domain_knowledge: list[str] = field(default_factory=list)
    equivalence_rules: list[str] = field(default_factory=list)
    evidence_rules: list[str] = field(default_factory=list)
    strictness: str = "balanced"
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class EvidenceRegime:
    regime: str
    rationale: str
    pred_observability: str
    ref_observability: str
    has_reference: bool
    has_prediction: bool
    caution_rules: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ArtifactElement:
    element_id: str
    kind: str
    label: str
    text: str
    evidence_text: str


@dataclass(slots=True)
class ArtifactRelation:
    relation_id: str
    kind: str
    source_label: str
    target_label: str
    trigger: str
    condition: str
    action: str
    description: str
    evidence_text: str


@dataclass(slots=True)
class ArtifactDossier:
    role: str
    format_guess: str
    artifact_family_guess: str
    summary: str
    elements: list[ArtifactElement] = field(default_factory=list)
    relations: list[ArtifactRelation] = field(default_factory=list)
    behaviors: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    ambiguities: list[str] = field(default_factory=list)
    evidence: list[EvidenceItem] = field(default_factory=list)
    observability: str = "low"
    format_confidence: float = 0.0
    observability_reason: str = ""
    analysis_mode: str = "parser_only"
    surface_markers: dict[str, int] = field(default_factory=dict)
    structural_warnings: list[str] = field(default_factory=list)
    canonical_names: list[str] = field(default_factory=list)
    extraction_conflicts: list[str] = field(default_factory=list)
    parser_notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class InputDossier:
    summary: str
    requirements: list[RequirementTraceResult]
    behaviors: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    ambiguities: list[str] = field(default_factory=list)
    evidence: list[EvidenceItem] = field(default_factory=list)
    observability: str = "low"
    observability_reason: str = ""
    entity_hints: list[str] = field(default_factory=list)
    context_clues: list[str] = field(default_factory=list)


__all__ = [
    "ArtifactDossier",
    "ArtifactElement",
    "ArtifactRelation",
    "EvidenceRegime",
    "InputDossier",
    "ReviewContract",
]
