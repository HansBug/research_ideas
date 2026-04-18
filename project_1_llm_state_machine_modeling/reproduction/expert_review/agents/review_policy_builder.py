from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

from langchain_openai import ChatOpenAI

from ..schema import DimensionDefinition
from ..utils import normalize_id
from ..prompts.review_policy import REVIEW_POLICY_SYSTEM_PROMPT
from ..schemas.dossiers import EvidenceRegime, ReviewContract
from ..tools import build_review_policy
from .llm_helpers import invoke_llm_json


def _clone_dimension(
    name: str,
    title: str,
    description: str,
    weight: float = 1.0,
    scoring_notes: list[str] | None = None,
) -> DimensionDefinition:
    return DimensionDefinition(
        name=name,
        title=title,
        description=description,
        weight=weight,
        scoring_mode="continuous_0_1",
        positive_examples=[],
        negative_examples=[],
        scoring_notes=list(scoring_notes or []),
    )


def build_dimensions(contract: ReviewContract, regime: EvidenceRegime) -> list[DimensionDefinition]:
    focus = {normalize_id(item) for item in contract.requested_focus}
    return [
        _clone_dimension(
            "notation_syntax",
            "Notation and Syntax",
            "Whether the artifact is structurally well-formed enough to support technical review.",
            weight=1.0,
        ),
        _clone_dimension(
            "semantic_completeness",
            "Semantic Completeness",
            "Whether important requirement-driven elements and behaviors are present.",
            weight=1.25 if "coverage" in focus or "completeness" in focus else 1.0,
        ),
        _clone_dimension(
            "behavioral_consistency",
            "Behavioral Consistency",
            "Whether the predicted artifact preserves intended behavior and avoids contradictions.",
            weight=1.25 if "behavior" in focus or "consistency" in focus or "equivalence" in focus else 1.0,
        ),
        _clone_dimension(
            "requirement_traceability",
            "Requirement Traceability",
            "Whether key requirements can be mapped to the artifact and unsupported extras are controlled.",
            weight=1.15 if "traceability" in focus or "hallucination" in focus else 1.0,
        ),
        _clone_dimension(
            "pragmatic_clarity",
            "Pragmatic Clarity",
            "Whether the artifact is readable, disciplined, and not gratuitously inflated.",
            weight=1.10 if "clarity" in focus or "quality" in focus else 1.0,
        ),
        _clone_dimension(
            "evidence_discipline",
            "Evidence Discipline",
            "Whether the review stays within the available evidence regime and avoids overclaiming.",
            weight=1.20 if regime.regime != "record_level" else 1.0,
        ),
    ]


def build_review_policy_packet(
    llm: ChatOpenAI | None,
    contract: ReviewContract,
    regime: EvidenceRegime,
    request: Any,
    input_dossier: Any,
    pred_dossier: Any,
    ref_dossier: Any,
    notes: list[str],
) -> dict[str, Any]:
    policy_packet = build_review_policy(
        contract,
        regime,
        request,
        input_dossier,
        pred_dossier,
        ref_dossier,
        llm=llm,
    )
    if llm is None:
        return policy_packet
    if regime.regime in {"record_level", "mixed_evidence"} or bool(policy_packet.get("component_review_mode")):
        notes.append(
            "Policy builder kept deterministic policy for direct-artifact/component review to reduce stochastic drift in core scoring."
        )
        return policy_packet
    payload = invoke_llm_json(
        llm,
        [
            ("system", REVIEW_POLICY_SYSTEM_PROMPT),
            (
                "user",
                "Build a compact review-policy refinement packet.\n\n"
                "Return JSON with optional keys: extra_notes, equivalence_bias, confidence_cap_override.\n\n"
                f"Contract:\n{json.dumps(asdict(contract), ensure_ascii=False, indent=2)}\n\n"
                f"Regime:\n{json.dumps(asdict(regime), ensure_ascii=False, indent=2)}\n\n"
                f"Base policy:\n{json.dumps(policy_packet, ensure_ascii=False, indent=2)}",
            ),
        ],
        operation="review_policy_builder",
    )
    if not isinstance(payload, dict):
        return policy_packet
    if "confidence_cap_override" in payload:
        try:
            policy_packet["base_confidence_cap"] = max(0.0, min(1.0, float(payload["confidence_cap_override"])))
        except Exception:
            pass
    if str(payload.get("equivalence_bias", "")).strip():
        policy_packet["equivalence_bias"] = str(payload["equivalence_bias"]).strip()
    if isinstance(payload.get("extra_notes"), list):
        notes.extend(str(item).strip() for item in payload["extra_notes"] if str(item).strip())
    return policy_packet


__all__ = ["build_dimensions", "build_review_policy_packet"]
