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
