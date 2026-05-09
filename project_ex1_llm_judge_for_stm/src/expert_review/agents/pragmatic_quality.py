"""``pragmatic_quality`` 模块。

**作用**：本模块属于 ``expert_review`` 体系内的辅助实现层；具体职责
由内部 class / function 的 docstring 描述。

**设计思路**：见包级 :mod:`expert_review.agents` 文档与
``PYDOC_INVENTORY.md`` 盘点清单。
"""
from __future__ import annotations

from typing import Any

from langchain_openai import ChatOpenAI

from ..schema import ElementIssue
from ..prompts import QUALITY_REVIEW_SYSTEM_PROMPT
from ..utils import normalize_id
from .common import clip01, is_grounded_to_input, make_evidence_item, requirement_grounding_tokens
from .llm_helpers import invoke_llm_json


GENERIC_NAME_TOKENS = {
    "idle",
    "start",
    "end",
    "state",
    "state1",
    "state2",
    "processing",
    "process",
    "waiting",
    "wait",
    "ready",
    "init",
    "initial",
    "final",
    "working",
    "running",
    "loop",
    "component",
    "block",
    "data",
    "message",
    "payload",
    "info",
    "node",
    "step",
    "task",
    "region",
    "mode",
}


def _issue(issue_type: str, element_text: str, reason_text: str, *, element_kind: str = "quality_signal") -> ElementIssue:
    """内部 helper：``_issue``。

    :param issue_type: 见函数签名与上下文。
    :param element_text: 见函数签名与上下文。
    :param reason_text: 见函数签名与上下文。
    :param element_kind: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    clean = element_text.strip() or issue_type
    return ElementIssue(
        element_id=f"quality_{normalize_id(clean) or normalize_id(issue_type) or 'signal'}",
        element_kind=element_kind,
        element_text=clean,
        issue_type=issue_type,
        reason_text=reason_text.strip(),
    )


def _generic_name_count(dossier: Any) -> int:
    """内部 helper：``_generic_name_count``。

    :param dossier: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    count = 0
    for item in dossier.elements:
        tokens = [part.lower() for part in (item.label or "").replace("_", " ").replace("-", " ").split() if part]
        if tokens and all(token in GENERIC_NAME_TOKENS for token in tokens):
            count += 1
    return count


def deterministic_pragmatic_quality(
    contract: Any,
    regime: Any,
    policy_packet: dict[str, Any],
    input_dossier: Any,
    pred_dossier: Any,
) -> dict[str, Any]:
    """``deterministic_pragmatic_quality`` 函数。

    :param contract: 见函数签名与上下文。
    :param regime: 见函数签名与上下文。
    :param policy_packet: 见函数签名与上下文。
    :param input_dossier: 见函数签名与上下文。
    :param pred_dossier: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    grounding_tokens = requirement_grounding_tokens(input_dossier)
    grounded_elements = 0
    unused_elements = 0
    for item in pred_dossier.elements:
        grounded = is_grounded_to_input(item.text, grounding_tokens)
        if grounded:
            grounded_elements += 1
        elif not any(normalize_id(item.label or item.text) in normalize_id(rel.evidence_text) for rel in pred_dossier.relations):
            unused_elements += 1
    element_count = max(1, len(pred_dossier.elements))
    relation_count = len(pred_dossier.relations)
    grounded_ratio = grounded_elements / element_count
    generic_name_count = _generic_name_count(pred_dossier)

    naming_score = clip01(0.92 - 0.08 * generic_name_count)
    readability_score = clip01(
        0.94
        - 0.09 * len(pred_dossier.structural_warnings)
        - 0.06 * len(pred_dossier.extraction_conflicts)
        - (0.10 if pred_dossier.format_guess == "missing" else 0.0)
    )
    noise_score = clip01(0.92 - 0.38 * max(0.0, 0.45 - grounded_ratio) - 0.08 * min(3, unused_elements))
    complexity_penalty = 0.0
    requirement_count = max(1, len(input_dossier.requirements))
    if len(pred_dossier.elements) >= max(6, 2 * requirement_count):
        complexity_penalty += 0.14
    if relation_count == 0 and len(pred_dossier.elements) >= 4:
        complexity_penalty += 0.10
    if pred_dossier.observability == "low":
        complexity_penalty += 0.06
    if regime.regime == "summary_only" and not getattr(regime, "has_reference", False):
        complexity_penalty += 0.04
    complexity_score = clip01(0.90 - complexity_penalty)

    weights = policy_packet.get("quality_axes", {})
    total_weight = sum(float(value) for value in weights.values()) or 1.0
    clarity_score_hint = clip01(
        (
            float(weights.get("readability", 1.0)) * readability_score
            + float(weights.get("naming", 1.0)) * naming_score
            + float(weights.get("noise", 1.0)) * noise_score
            + float(weights.get("complexity", 1.0)) * complexity_score
        )
        / total_weight
    )

    issues: list[ElementIssue] = []
    if generic_name_count >= 2:
        issues.append(
            _issue(
                "readability_or_naming",
                f"{generic_name_count} generic labels",
                "Multiple major elements use generic names, which reduces naming discipline and reviewability.",
            )
        )
    if pred_dossier.structural_warnings:
        issues.append(
            _issue(
                "readability_or_naming",
                pred_dossier.structural_warnings[0],
                "Structural warnings make the artifact harder to read or trust at review time.",
            )
        )
    severe_noise_signal = (
        regime.regime != "record_level"
        and (
            grounded_ratio < 0.18
            or unused_elements >= 4
            or (complexity_penalty >= 0.18 and grounded_ratio < 0.35)
            or unused_elements >= 2
            or grounded_ratio < 0.30
        )
    )
    if severe_noise_signal:
        issues.append(
            _issue(
                "unused_or_noisy_structure",
                f"grounded_ratio={grounded_ratio:.2f}",
                "Too much visible structure is weakly grounded in the stated requirements, so the artifact looks noisy or weakly justified.",
            )
        )
    if complexity_penalty >= 0.14:
        issues.append(
            _issue(
                "unused_or_noisy_structure",
                f"elements={len(pred_dossier.elements)}, relations={relation_count}",
                "The visible structure appears disproportionately complex relative to the available requirements and evidence.",
            )
        )

    summary_score_hint = clarity_score_hint
    score_semantics = policy_packet.get("score_semantics")
    if score_semantics == "summary_stat_stddev":
        instability = clip01(
            0.55 * (1.0 - readability_score)
            + 0.25 * (1.0 - naming_score)
            + 0.20 * (1.0 - complexity_score)
        )
        summary_score_hint = clip01(0.04 + 0.55 * instability)
    elif score_semantics == "summary_quality":
        summary_score_hint = clip01(
            0.18
            + 0.62 * clarity_score_hint
            + (0.08 if pred_dossier.observability == "high" else 0.03 if pred_dossier.observability == "medium" else -0.05)
            - (0.05 if not policy_packet.get("summary_semantics_explicit") else 0.0)
        )
        if policy_packet.get("aggregate_signal") == "max":
            summary_score_hint = clip01(summary_score_hint + 0.05)
        elif policy_packet.get("aggregate_signal") == "min":
            summary_score_hint = clip01(summary_score_hint - 0.08)

    evidence = []
    if pred_dossier.elements:
        evidence.append(
            make_evidence_item(
                "prediction",
                "prediction:quality:element",
                pred_dossier.elements[0].evidence_text,
                "Representative predicted element used for pragmatic quality inspection.",
            )
        )
    for idx, warning in enumerate(pred_dossier.structural_warnings[:2], start=1):
        evidence.append(
            make_evidence_item(
                "prediction",
                f"prediction:quality:warning:{idx}",
                warning,
                "Structural warning emitted by the artifact probe and reused by the quality agent.",
            )
        )

    issue_taxonomy = sorted({issue.issue_type for issue in issues})
    return {
        "clarity_score_hint": clarity_score_hint,
        "quality_score_hint": clarity_score_hint,
        "summary_score_hint": summary_score_hint,
        "grounded_ratio": grounded_ratio,
        "generic_name_count": generic_name_count,
        "naming_score": naming_score,
        "readability_score": readability_score,
        "noise_score": noise_score,
        "complexity_score": complexity_score,
        "issues": issues[:8],
        "issue_taxonomy": issue_taxonomy,
        "evidence": evidence[:4],
        "notes": [
            f"score_semantics={score_semantics}",
            f"aggregate_signal={policy_packet.get('aggregate_signal')}",
            f"grounded_ratio={grounded_ratio:.2f}",
            f"generic_name_count={generic_name_count}",
            f"unused_elements={unused_elements}",
        ],
    }


def pragmatic_quality_with_llm(
    llm: ChatOpenAI | None,
    contract: Any,
    regime: Any,
    policy_packet: dict[str, Any],
    input_dossier: Any,
    pred_dossier: Any,
    base_report: dict[str, Any],
) -> dict[str, Any] | None:
    """``pragmatic_quality_with_llm`` 函数。

    :param llm: 见函数签名与上下文。
    :param contract: 见函数签名与上下文。
    :param regime: 见函数签名与上下文。
    :param policy_packet: 见函数签名与上下文。
    :param input_dossier: 见函数签名与上下文。
    :param pred_dossier: 见函数签名与上下文。
    :param base_report: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    if llm is None:
        return None
    payload = invoke_llm_json(
        llm,
        [
            ("system", QUALITY_REVIEW_SYSTEM_PROMPT),
            (
                "user",
                "Review the artifact's pragmatic quality under the given contract and policy.\n\n"
                "Return JSON with keys: quality_score_hint, summary_score_hint, issues, notes.\n\n"
                f"Contract summary:\n{getattr(contract, 'task_summary', '')}\n\n"
                f"Regime: {getattr(regime, 'regime', '')}\n"
                f"Policy packet: {policy_packet}\n\n"
                f"Input summary:\n{input_dossier.summary}\n\n"
                f"Prediction summary:\n{pred_dossier.summary}\n\n"
                f"Visible structural warnings:\n{pred_dossier.structural_warnings}\n\n"
                f"Deterministic candidate report:\n{base_report}",
            ),
        ],
        operation="pragmatic_quality",
    )
    if not isinstance(payload, dict):
        return None

    merged = dict(base_report)
    if "quality_score_hint" in payload:
        merged["quality_score_hint"] = clip01(float(payload.get("quality_score_hint", merged.get("quality_score_hint", 0.6))))
        merged["clarity_score_hint"] = merged["quality_score_hint"]
    if "summary_score_hint" in payload:
        merged["summary_score_hint"] = clip01(float(payload.get("summary_score_hint", merged.get("summary_score_hint", 0.6))))
    llm_issues: list[ElementIssue] = []
    for idx, item in enumerate(payload.get("issues", []), start=1):
        if isinstance(item, dict):
            llm_issues.append(
                _issue(
                    str(item.get("issue_type") or "readability_or_naming"),
                    str(item.get("element_text") or f"quality_llm_{idx}"),
                    str(item.get("reason_text") or "LLM identified a pragmatic quality concern."),
                )
            )
        else:
            llm_issues.append(_issue("readability_or_naming", str(item), "LLM identified a pragmatic quality concern."))
    if llm_issues:
        merged["issues"] = llm_issues[:8]
        merged["issue_taxonomy"] = sorted({issue.issue_type for issue in llm_issues})
    if isinstance(payload.get("notes"), list):
        merged["notes"] = [str(item).strip() for item in payload["notes"] if str(item).strip()][:8]
    return merged