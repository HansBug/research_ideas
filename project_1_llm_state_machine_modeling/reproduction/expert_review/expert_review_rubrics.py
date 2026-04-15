from __future__ import annotations

from .expert_review_prompts import default_dimension_examples
from .expert_review_schema import DimensionDefinition


def _clone_dimensions(names: list[str], weights: dict[str, float] | None = None) -> list[DimensionDefinition]:
    weights = weights or {}
    defaults = {item.name: item for item in default_dimension_examples()}
    result = []
    for name in names:
        base = defaults[name]
        result.append(
            DimensionDefinition(
                name=base.name,
                title=base.title,
                description=base.description,
                weight=weights.get(name, base.weight),
                scoring_mode=base.scoring_mode,
                positive_examples=list(base.positive_examples),
                negative_examples=list(base.negative_examples),
                scoring_notes=list(base.scoring_notes),
            )
        )
    return result


def resolve_review_profile(prompt: str) -> tuple[str, str, list[DimensionDefinition]]:
    prompt_lower = prompt.lower()

    if "ttool" in prompt_lower or "avatar" in prompt_lower or "block diagram" in prompt_lower:
        rubric_text = (
            "Review this TTool or AVATAR modeling artifact using expert-style human grading. "
            "Focus on adequacy to the specification, plausibility of behavior, reasonableness of exchanges, "
            "readability, naming consistency, unused attributes, and syntax or well-formedness."
        )
        dimensions = [
            DimensionDefinition(
                name="adequacy_to_specification",
                title="Adequacy to Specification",
                description="Whether the architecture and behavior satisfy the stated specification.",
                weight=1.8,
            ),
            DimensionDefinition(
                name="behavioral_plausibility",
                title="Behavioral Plausibility",
                description="Whether the model looks executable and behaviorally coherent.",
                weight=1.5,
            ),
            DimensionDefinition(
                name="interaction_quality",
                title="Interaction Quality",
                description="Whether exchanges between blocks are reasonable and justified.",
                weight=1.0,
            ),
            DimensionDefinition(
                name="pragmatic_clarity",
                title="Pragmatic Clarity",
                description="Whether naming, decomposition, and overall readability are disciplined.",
                weight=1.0,
            ),
            DimensionDefinition(
                name="notation_syntax",
                title="Notation and Syntax",
                description="Whether the artifact appears structurally well-formed.",
                weight=0.9,
            ),
        ]
        return rubric_text, "rubric_only", dimensions

    if "traceability" in prompt_lower or "requirements" in prompt_lower:
        rubric_text = (
            "Review this model with emphasis on requirement completeness, traceability, behavioral consistency, "
            "and whether unsupported model content has been introduced."
        )
        dimensions = _clone_dimensions(
            [
                "semantic_completeness",
                "behavioral_consistency",
                "requirement_traceability",
                "pragmatic_clarity",
            ],
            weights={
                "semantic_completeness": 1.5,
                "behavioral_consistency": 1.5,
                "requirement_traceability": 1.4,
                "pragmatic_clarity": 0.7,
            },
        )
        return rubric_text, "trace_compatible", dimensions

    rubric_text = (
        "Review the predicted model as a software behavior modeling expert. "
        "Separate syntax, semantic completeness, behavioral consistency, requirement traceability, "
        "and pragmatic clarity. If a reference output is provided, compare against it semantically. "
        "If no reference output is provided, perform a standalone expert review against the input description."
    )
    dimensions = _clone_dimensions(
        [
            "notation_syntax",
            "semantic_completeness",
            "behavioral_consistency",
            "requirement_traceability",
            "pragmatic_clarity",
        ]
    )
    return rubric_text, "component_semantic_match", dimensions
