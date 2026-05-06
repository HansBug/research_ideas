"""S2-Q1 LLM rubric-based per-dim scorer.

For each of the 6 review dimensions (notation_syntax / semantic_completeness /
behavioral_consistency / requirement_traceability / pragmatic_clarity /
evidence_discipline), prompt the LLM with a rubric (5-band scale + anchor
examples + pitfalls) and parse its score with strict sanity bounds.

Falls back to deterministic estimate on:
  - LLM call failure
  - invalid JSON
  - score outside [0, 1]
  - score deviates more than 2× the configured sanity bound from deterministic

Design source: `designs/v2/RUBRIC_DESIGN.md`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..prompts.rubric_dim_score import (
    SUPPORTED_DIMS,
    build_rubric_prompt,
)
from .llm_helpers import invoke_llm_json


# Sanity bounds: (min_offset_from_det, max_offset_from_det)
# Iter-A introduces asymmetric bounds keyed by (regime, dim) — summary regime
# needs MORE room for the LLM to express rank differentiation. Week 1 v0
# experiment showed symmetric tight bounds collapsed summary RankAlign 69→63.
_SANITY_BOUNDS_DEFAULT: dict[str, tuple[float, float]] = {
    "notation_syntax": (-0.20, 0.30),
    "semantic_completeness": (-0.20, 0.20),
    "behavioral_consistency": (-0.20, 0.20),
    "requirement_traceability": (-0.15, 0.15),  # tightest — trace_ratio is hard evidence
    "pragmatic_clarity": (-0.25, 0.25),
    "evidence_discipline": (-0.15, 0.15),
}

# Iter-A: regime-aware bounds. summary_only / protocol_only get LOOSER bounds
# so the LLM can keep its rank-differentiation advantage; record_level /
# component_review_mode keep the tight bounds to anchor LLM against
# absolute-score drift.
_SANITY_BOUNDS_BY_REGIME: dict[tuple[str, str], tuple[float, float]] = {
    # summary regime — LOOSEN ±0.30..0.35 to preserve rank differentiation
    ("summary_only", "notation_syntax"): (-0.30, 0.40),
    ("summary_only", "semantic_completeness"): (-0.35, 0.35),
    ("summary_only", "behavioral_consistency"): (-0.35, 0.35),
    ("summary_only", "requirement_traceability"): (-0.30, 0.30),
    ("summary_only", "pragmatic_clarity"): (-0.35, 0.35),
    ("summary_only", "evidence_discipline"): (-0.30, 0.30),
    # protocol regime — also loosen
    ("protocol_only", "notation_syntax"): (-0.30, 0.40),
    ("protocol_only", "semantic_completeness"): (-0.35, 0.35),
    ("protocol_only", "behavioral_consistency"): (-0.35, 0.35),
    ("protocol_only", "requirement_traceability"): (-0.30, 0.30),
    ("protocol_only", "pragmatic_clarity"): (-0.35, 0.35),
    ("protocol_only", "evidence_discipline"): (-0.30, 0.30),
}


def _get_sanity_bound(dim_name: str, regime_label: str, asymmetric: bool) -> tuple[float, float]:
    """Resolve sanity bound based on Iter-A flag (asymmetric)."""
    if asymmetric:
        key = (regime_label, dim_name)
        if key in _SANITY_BOUNDS_BY_REGIME:
            return _SANITY_BOUNDS_BY_REGIME[key]
    return _SANITY_BOUNDS_DEFAULT[dim_name]

# Hard-clip threshold: scores deviating more than 2× the bound trigger fallback
_HARD_REJECT_MULTIPLIER = 2.0


@dataclass(slots=True)
class RubricScore:
    dimension: str
    score: float
    band: str
    reason_text: str
    confidence: float
    backend: str  # "rubric_llm" | "rubric_fallback_deterministic"
    sanity_clipped: bool = False
    deterministic_estimate: float = 0.0
    raw_llm_score: float | None = None
    reason_anchor_id: str | None = None
    specific_defects: list[dict[str, Any]] = field(default_factory=list)
    error_message: str | None = None


def _truncate(text: str | None, limit: int = 800) -> str:
    s = str(text or "").strip()
    if len(s) <= limit:
        return s
    return s[:limit] + f"\n...[truncated {len(s) - limit} chars]"


def _band_from_score(score: float) -> str:
    if score >= 0.85:
        return "excellent"
    if score >= 0.65:
        return "good"
    if score >= 0.45:
        return "acceptable"
    if score >= 0.25:
        return "weak"
    return "poor"


def llm_rubric_score(
    dim_name: str,
    *,
    pred_summary: str,
    ref_summary: str | None,
    input_summary: str,
    regime_label: str,
    deterministic_estimate: float,
    extra_signals: dict[str, Any] | None = None,
    llm: Any = None,
    asymmetric_bounds: bool = False,    # Iter-A flag
    differentiation_mode: bool = False,  # Iter-B flag
) -> RubricScore:
    """Run rubric-based LLM scoring for a single dimension.

    Returns RubricScore — the caller is responsible for treating the result as
    the canonical dim_score and feeding it into the existing post-transforms
    (summary_mode / protocol_mode / component_review_mode blends).
    """
    if dim_name not in SUPPORTED_DIMS:
        raise ValueError(f"Unsupported dim: {dim_name!r}")

    det = max(0.0, min(1.0, float(deterministic_estimate)))
    bound_lo_off, bound_hi_off = _get_sanity_bound(dim_name, regime_label, asymmetric_bounds)
    bound_lo = max(0.0, det + bound_lo_off)
    bound_hi = min(1.0, det + bound_hi_off)
    hard_lo = max(0.0, det + _HARD_REJECT_MULTIPLIER * bound_lo_off)
    hard_hi = min(1.0, det + _HARD_REJECT_MULTIPLIER * bound_hi_off)

    if llm is None:
        return RubricScore(
            dimension=dim_name,
            score=det,
            band=_band_from_score(det),
            reason_text="(rubric scorer skipped: no llm client)",
            confidence=0.5,
            backend="rubric_fallback_deterministic",
            sanity_clipped=False,
            deterministic_estimate=det,
            raw_llm_score=None,
        )

    prompt = build_rubric_prompt(
        dim_name=dim_name,
        pred_summary=_truncate(pred_summary),
        ref_summary=_truncate(ref_summary) if ref_summary else None,
        input_summary=_truncate(input_summary),
        regime_label=regime_label,
        deterministic_hint=det,
        extra_signals=extra_signals,
        differentiation_mode=differentiation_mode,
    )
    messages = [
        ("system", "You are a strict, calibrated state-machine reviewer. Output only JSON."),
        ("user", prompt),
    ]
    try:
        payload = invoke_llm_json(llm, messages, operation=f"rubric_dim_score:{dim_name}")
    except Exception as exc:
        return RubricScore(
            dimension=dim_name,
            score=det,
            band=_band_from_score(det),
            reason_text="(rubric scorer error: see error_message)",
            confidence=0.5,
            backend="rubric_fallback_deterministic",
            deterministic_estimate=det,
            raw_llm_score=None,
            error_message=f"{type(exc).__name__}: {exc}",
        )

    if not isinstance(payload, dict):
        return RubricScore(
            dimension=dim_name,
            score=det,
            band=_band_from_score(det),
            reason_text="(rubric scorer returned non-dict)",
            confidence=0.5,
            backend="rubric_fallback_deterministic",
            deterministic_estimate=det,
            raw_llm_score=None,
            error_message="invalid_response_type",
        )

    try:
        raw_score = float(payload.get("score"))
    except (TypeError, ValueError):
        raw_score = None

    if raw_score is None or not (0.0 <= raw_score <= 1.0):
        return RubricScore(
            dimension=dim_name,
            score=det,
            band=_band_from_score(det),
            reason_text=str(payload.get("reason_text") or "(invalid score from rubric)"),
            confidence=float(payload.get("confidence") or 0.5),
            backend="rubric_fallback_deterministic",
            deterministic_estimate=det,
            raw_llm_score=raw_score,
            error_message="score_out_of_range",
        )

    # Hard reject: deviation too large from deterministic
    if raw_score < hard_lo or raw_score > hard_hi:
        return RubricScore(
            dimension=dim_name,
            score=det,
            band=_band_from_score(det),
            reason_text=str(payload.get("reason_text") or "(rubric score rejected: out of hard bound)"),
            confidence=float(payload.get("confidence") or 0.5),
            backend="rubric_fallback_deterministic",
            deterministic_estimate=det,
            raw_llm_score=raw_score,
            error_message="score_hard_rejected",
        )

    # Soft clip to sanity bound
    sanity_clipped = False
    final_score = raw_score
    if final_score < bound_lo:
        final_score = bound_lo
        sanity_clipped = True
    elif final_score > bound_hi:
        final_score = bound_hi
        sanity_clipped = True

    return RubricScore(
        dimension=dim_name,
        score=final_score,
        band=str(payload.get("band") or _band_from_score(final_score)),
        reason_text=str(payload.get("reason_text") or ""),
        confidence=float(payload.get("confidence") or 0.7),
        backend="rubric_llm",
        sanity_clipped=sanity_clipped,
        deterministic_estimate=det,
        raw_llm_score=raw_score,
        reason_anchor_id=payload.get("reason_anchor_id"),
        specific_defects=list(payload.get("specific_defects") or []),
    )


__all__ = ["RubricScore", "llm_rubric_score"]
