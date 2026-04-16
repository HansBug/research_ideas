from __future__ import annotations

from ..schemas.dossiers import ArtifactDossier, EvidenceRegime
from ..schemas.request import ExpertReviewRequest


def estimate_evidence_regime(
    request: ExpertReviewRequest,
    pred_dossier: ArtifactDossier,
    ref_dossier: ArtifactDossier,
) -> EvidenceRegime:
    has_prediction = bool((request.pred_output or "").strip())
    has_reference = bool((request.ref_output or "").strip())
    prompt_text = " ".join(
        part.strip().lower()
        for part in [request.prompt, request.input_text, request.pred_output or "", request.ref_output or ""]
        if part
    )
    if not has_prediction and not has_reference:
        return EvidenceRegime(
            regime="protocol_only",
            rationale="No concrete prediction or reference artifact was provided.",
            pred_observability=pred_dossier.observability,
            ref_observability=ref_dossier.observability,
            has_reference=False,
            has_prediction=False,
            caution_rules=[
                "Do not fabricate element-level findings without visible artifacts.",
                "Focus on process understanding and evidence limits rather than exact scoring.",
            ],
        )
    if ("manual inspection" in prompt_text or "formal verification" in prompt_text or "simulation" in prompt_text) and (
        pred_dossier.observability == "low" or (has_reference and ref_dossier.observability == "low")
    ):
        return EvidenceRegime(
            regime="protocol_only",
            rationale="The inputs emphasize evaluation protocol while concrete artifact evidence is sparse.",
            pred_observability=pred_dossier.observability,
            ref_observability=ref_dossier.observability,
            has_reference=has_reference,
            has_prediction=has_prediction,
            caution_rules=[
                "Keep scores coarse and confidence capped.",
                "Do not claim exact structural defects without direct evidence.",
            ],
        )
    if has_prediction and has_reference and pred_dossier.observability != "low" and ref_dossier.observability != "low":
        return EvidenceRegime(
            regime="record_level",
            rationale="Prediction and reference artifacts are both directly observable.",
            pred_observability=pred_dossier.observability,
            ref_observability=ref_dossier.observability,
            has_reference=True,
            has_prediction=True,
            caution_rules=[
                "Use strong alignment where evidence is explicit, but still allow equivalent structure variation.",
            ],
        )
    if has_prediction and not has_reference:
        regime = "summary_only" if (
            pred_dossier.format_guess == "summary_text" or "summary-level" in request.prompt.lower()
        ) else "mixed_evidence"
        rationale = "Only predicted artifact evidence is available, so review must rely on requirements and direct artifact reading."
        if regime == "summary_only":
            rationale = "Prediction evidence looks like summary-level reporting rather than a full artifact."
        return EvidenceRegime(
            regime=regime,
            rationale=rationale,
            pred_observability=pred_dossier.observability,
            ref_observability=ref_dossier.observability,
            has_reference=False,
            has_prediction=True,
            caution_rules=[
                "Avoid exact-match penalties that require a missing reference artifact.",
            ],
        )
    return EvidenceRegime(
        regime="mixed_evidence",
        rationale="Some artifact evidence is visible, but not enough for fully strict record-level matching.",
        pred_observability=pred_dossier.observability,
        ref_observability=ref_dossier.observability,
        has_reference=has_reference,
        has_prediction=has_prediction,
        caution_rules=[
            "Treat low-observability differences as uncertain rather than definitively wrong.",
        ],
    )


__all__ = ["estimate_evidence_regime"]
