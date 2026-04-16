from __future__ import annotations

import re
from typing import Any


QUALITY_ISSUE_TYPES = {
    "readability_or_naming",
    "unused_or_noisy_structure",
    "evidence_overreach",
}

VV_ROLE_HINTS: dict[str, list[str]] = {
    "manual inspection": ["manual inspection", "manual compare", "manually compare", "manual check", "manual", "人工", "逐项对照", "手工"],
    "formal verification": [
        "formal verification",
        "model checker",
        "model-checking",
        "verification",
        "形式化验证",
        "模型检查",
        "proof",
        "prove",
    ],
    "simulation": ["simulation", "simulator", "simulated", "仿真", "模拟"],
    "testing": ["testing", "test", "tests", "测试", "tp/fp/fn", "f1-score", "f1 score", "f1"],
    "syntax checker": ["syntax checker", "grammar", "format checking", "plantuml format", "语法", "格式检查"],
}


def _joined_text(values: list[str]) -> str:
    return "\n".join(item for item in values if item).lower()


def infer_aggregate_signal(*texts: str) -> str:
    text = _joined_text([str(item or "") for item in texts])
    if any(token in text for token in ["std dev", "std_dev", "std. dev", "standard deviation", "variance", "dispersion"]):
        return "stddev"
    if re.search(r"\baverage\b", text) or "mean score" in text or "cohort average" in text:
        return "average"
    if re.search(r"\bmax(imum)?\b", text) or "highest score" in text or "best score" in text:
        return "max"
    if re.search(r"\bmin(imum)?\b", text) or "lowest score" in text or "worst score" in text:
        return "min"
    if any(token in text for token in ["summary row", "aggregate stat", "summary-level", "cohort statistic", "raw score row"]):
        return "summary"
    return "direct_review"


def detect_vv_roles(texts: list[str]) -> list[str]:
    text = _joined_text(texts)
    roles: list[str] = []
    for role, hints in VV_ROLE_HINTS.items():
        if any(hint in text for hint in hints):
            roles.append(role)
    return roles


def build_review_policy(
    contract: Any,
    regime: Any,
    request: Any,
    input_dossier: Any,
    pred_dossier: Any,
    ref_dossier: Any,
) -> dict[str, Any]:
    focus = {str(item).strip().lower() for item in getattr(contract, "requested_focus", []) if str(item).strip()}
    contract_texts = [
        str(getattr(contract, "task_summary", "") or ""),
        *[str(item) for item in getattr(contract, "requested_focus", [])],
        *[str(item) for item in getattr(contract, "domain_knowledge", [])],
        *[str(item) for item in getattr(contract, "equivalence_rules", [])],
        *[str(item) for item in getattr(contract, "evidence_rules", [])],
        *[str(item) for item in getattr(contract, "notes", [])],
        str(getattr(request, "prompt", "") or ""),
        str(getattr(request, "input_text", "") or ""),
    ]
    aggregate_signal = infer_aggregate_signal(*contract_texts)
    summary_semantics_explicit = aggregate_signal != "direct_review"

    quality_axes = {
        "readability": 1.20 if {"clarity", "quality"} & focus else 1.0,
        "naming": 1.15 if {"clarity", "quality"} & focus else 1.0,
        "noise": 1.15 if {"hallucination", "traceability"} & focus else 1.0,
        "complexity": 1.10 if {"quality", "behavior"} & focus else 1.0,
    }
    score_semantics = "artifact_quality"
    if getattr(regime, "regime", "") == "summary_only":
        if aggregate_signal == "stddev":
            score_semantics = "summary_stat_stddev"
        elif aggregate_signal in {"average", "max", "min", "summary"}:
            score_semantics = "summary_quality"
        else:
            score_semantics = "summary_quality"
    elif getattr(regime, "regime", "") == "protocol_only":
        score_semantics = "protocol_assurance"

    allow_element_level_claims = getattr(regime, "regime", "") == "record_level"
    allow_requirement_defect_claims = getattr(regime, "regime", "") == "record_level"
    if getattr(regime, "regime", "") == "mixed_evidence" and getattr(pred_dossier, "observability", "low") == "high":
        allow_requirement_defect_claims = True

    base_confidence_cap = 0.84
    if getattr(regime, "regime", "") == "summary_only":
        base_confidence_cap = 0.56 if score_semantics == "summary_quality" else 0.48
    elif getattr(regime, "regime", "") == "protocol_only":
        base_confidence_cap = 0.42
    elif getattr(regime, "regime", "") == "mixed_evidence":
        base_confidence_cap = 0.68

    if getattr(pred_dossier, "observability", "low") == "low":
        base_confidence_cap = min(base_confidence_cap, 0.52)
    if getattr(regime, "has_reference", False) and getattr(ref_dossier, "observability", "low") == "low":
        base_confidence_cap = min(base_confidence_cap, 0.58)
    if getattr(input_dossier, "observability", "low") == "low":
        base_confidence_cap = min(base_confidence_cap, 0.60)

    policy_profile = [
        getattr(regime, "regime", "unknown"),
        score_semantics,
        "strict" if getattr(contract, "strictness", "balanced") == "strict" else "balanced",
        "summary_semantics_explicit" if summary_semantics_explicit else "summary_semantics_implicit",
    ]

    return {
        "profile_name": "/".join(policy_profile),
        "quality_axes": quality_axes,
        "aggregate_signal": aggregate_signal,
        "score_semantics": score_semantics,
        "summary_semantics_explicit": summary_semantics_explicit,
        "allow_element_level_claims": allow_element_level_claims,
        "allow_requirement_defect_claims": allow_requirement_defect_claims,
        "base_confidence_cap": base_confidence_cap,
        "vv_role_hints": VV_ROLE_HINTS,
        "quality_issue_types": sorted(QUALITY_ISSUE_TYPES),
    }
