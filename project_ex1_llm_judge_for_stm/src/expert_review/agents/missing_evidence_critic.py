"""``missing_evidence_critic`` 模块。

**作用**：本模块属于 ``expert_review`` 体系内的辅助实现层；具体职责
由内部 class / function 的 docstring 描述。

**设计思路**：见包级 :mod:`expert_review.agents` 文档与
``PYDOC_INVENTORY.md`` 盘点清单。
"""
from __future__ import annotations

from typing import Any

from langchain_openai import ChatOpenAI

from ..prompts import MISSING_EVIDENCE_SYSTEM_PROMPT
from ..tools import detect_vv_roles
from .common import clip01, make_evidence_item
from .llm_helpers import invoke_llm_json


def _dedup_str_list(values: list[str]) -> list[str]:
    """内部 helper：``_dedup_str_list``。

    :param values: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    result: list[str] = []
    seen: set[str] = set()
    for item in values:
        text = str(item).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def deterministic_missing_evidence_critic(
    contract: Any,
    regime: Any,
    request: Any,
    policy_packet: dict[str, Any],
    input_dossier: Any,
    pred_dossier: Any,
    ref_dossier: Any,
    equivalence_report: dict[str, Any],
    quality_report: dict[str, Any],
) -> dict[str, Any]:
    """``deterministic_missing_evidence_critic`` 函数。

    :param contract: 见函数签名与上下文。
    :param regime: 见函数签名与上下文。
    :param request: 见函数签名与上下文。
    :param policy_packet: 见函数签名与上下文。
    :param input_dossier: 见函数签名与上下文。
    :param pred_dossier: 见函数签名与上下文。
    :param ref_dossier: 见函数签名与上下文。
    :param equivalence_report: 见函数签名与上下文。
    :param quality_report: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    warnings: list[str] = []
    missing_flags: list[str] = []
    confidence_cap = float(policy_packet.get("base_confidence_cap", 0.72))

    if regime.regime == "protocol_only":
        warnings.append("Protocol-only evidence: exact element-level error claims should be treated as low-confidence.")
        missing_flags.append("protocol_only")
    elif regime.regime == "summary_only":
        warnings.append("Summary-level evidence: keep judgement coarse and avoid pseudo-precise structural claims.")
        missing_flags.append("summary_only")
    elif regime.regime == "mixed_evidence":
        warnings.append("Mixed evidence: some visible differences remain underdetermined because the public evidence is incomplete.")
        missing_flags.append("mixed_evidence")

    if not regime.has_reference:
        confidence_cap = min(confidence_cap, 0.60 if regime.regime == "mixed_evidence" else confidence_cap)
        missing_flags.append("no_reference_anchor")
    if pred_dossier.observability == "low":
        confidence_cap = min(confidence_cap, 0.52)
        warnings.append("Prediction observability is low, so downstream judgement confidence must remain capped.")
        missing_flags.append("low_prediction_observability")
    if regime.has_reference and ref_dossier.observability == "low":
        confidence_cap = min(confidence_cap, 0.58)
        warnings.append("Reference observability is low, so exact reference mismatch claims should be softened.")
        missing_flags.append("low_reference_observability")
    if not input_dossier.requirements:
        confidence_cap = min(confidence_cap, 0.60)
        warnings.append("No explicit requirement list was extracted, so traceability conclusions must stay conservative.")
        missing_flags.append("missing_requirement_list")

    vv_roles = detect_vv_roles(
        [
            str(getattr(contract, "task_summary", "") or ""),
            str(getattr(request, "prompt", "") or ""),
            str(getattr(request, "input_text", "") or ""),
            *[str(item) for item in getattr(contract, "domain_knowledge", [])],
            *[str(item) for item in getattr(contract, "notes", [])],
        ]
    )

    if policy_packet.get("score_semantics") == "summary_stat_stddev":
        confidence_cap = min(confidence_cap, 0.48)
        warnings.append("This task looks like an aggregate variability statistic, so the score should remain coarse and contract-driven.")
        missing_flags.append("aggregate_statistic_only")
    elif policy_packet.get("score_semantics") == "summary_quality":
        warnings.append("This task looks like a summary-level quality judgement; preserve coarse scoring rather than per-element blame.")

    if regime.regime == "protocol_only" and not vv_roles:
        warnings.append("No explicit V&V role could be recovered from the public protocol text.")
        missing_flags.append("missing_vv_roles")

    issue_taxonomy = ["evidence_overreach"] if warnings else []
    evidence = [
        make_evidence_item(
            "critic",
            "critic:warning:1",
            warnings[0],
            "Primary evidence-discipline warning emitted by the missing-evidence critic.",
        )
    ] if warnings else []
    return {
        "confidence_cap": confidence_cap,
        "warnings": warnings[:8],
        "confidence": min(0.85, confidence_cap + 0.05),
        "allow_element_level_claims": bool(policy_packet.get("allow_element_level_claims", False)),
        "allow_requirement_defect_claims": bool(policy_packet.get("allow_requirement_defect_claims", False)),
        "missing_evidence_flags": missing_flags[:8],
        "vv_roles": vv_roles[:5],
        "issue_taxonomy": issue_taxonomy,
        "evidence": evidence,
        "protocol_assurance_score_hint": clip01(0.32 + 0.10 * len(vv_roles) - 0.06 * max(0, 2 - len(vv_roles))),
    }


def missing_evidence_with_llm(
    llm: ChatOpenAI | None,
    contract: Any,
    regime: Any,
    request: Any,
    policy_packet: dict[str, Any],
    input_dossier: Any,
    pred_dossier: Any,
    ref_dossier: Any,
    equivalence_report: dict[str, Any],
    quality_report: dict[str, Any],
    base_report: dict[str, Any],
) -> dict[str, Any] | None:
    """``missing_evidence_with_llm`` 函数。

    :param llm: 见函数签名与上下文。
    :param contract: 见函数签名与上下文。
    :param regime: 见函数签名与上下文。
    :param request: 见函数签名与上下文。
    :param policy_packet: 见函数签名与上下文。
    :param input_dossier: 见函数签名与上下文。
    :param pred_dossier: 见函数签名与上下文。
    :param ref_dossier: 见函数签名与上下文。
    :param equivalence_report: 见函数签名与上下文。
    :param quality_report: 见函数签名与上下文。
    :param base_report: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    if llm is None:
        return None
    payload = invoke_llm_json(
        llm,
        [
            ("system", MISSING_EVIDENCE_SYSTEM_PROMPT),
            (
                "user",
                "Review the evidence limits and confidence policy.\n\n"
                "Return JSON with keys: confidence_cap, warnings, vv_roles, missing_evidence_flags.\n\n"
                f"Contract summary:\n{getattr(contract, 'task_summary', '')}\n\n"
                f"Regime: {getattr(regime, 'regime', '')}\n"
                f"Policy packet: {policy_packet}\n\n"
                f"Input summary:\n{input_dossier.summary}\n\n"
                f"Prediction observability: {pred_dossier.observability}\n"
                f"Reference observability: {ref_dossier.observability}\n\n"
                f"Equivalence candidate report:\n{equivalence_report}\n\n"
                f"Quality candidate report:\n{quality_report}\n\n"
                f"Deterministic critic report:\n{base_report}",
            ),
        ],
        operation="missing_evidence_critic",
    )
    if not isinstance(payload, dict):
        return None
    merged = dict(base_report)
    if "confidence_cap" in payload:
        proposed_cap = clip01(float(payload.get("confidence_cap", merged.get("confidence_cap", 0.6))))
        if regime.regime == "record_level" and not base_report.get("warnings"):
            base_cap = float(base_report.get("confidence_cap", 0.6))
            merged["confidence_cap"] = max(base_cap - 0.03, min(base_cap, proposed_cap))
        else:
            merged["confidence_cap"] = proposed_cap
        merged["confidence"] = min(0.85, merged["confidence_cap"] + 0.05)
    if isinstance(payload.get("warnings"), list):
        proposed_warnings = [str(item).strip() for item in payload["warnings"] if str(item).strip()]
        if regime.regime == "record_level" and not base_report.get("warnings"):
            merged["warnings"] = list(base_report.get("warnings", []))
        else:
            merged["warnings"] = _dedup_str_list([*base_report.get("warnings", []), *proposed_warnings])[:8]
        merged["issue_taxonomy"] = ["evidence_overreach"] if merged["warnings"] else []
    if isinstance(payload.get("vv_roles"), list):
        merged["vv_roles"] = _dedup_str_list([*base_report.get("vv_roles", []), *payload["vv_roles"]])[:5]
    merged["missing_evidence_flags"] = list(base_report.get("missing_evidence_flags", []))[:8]
    return merged