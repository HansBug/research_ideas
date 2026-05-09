"""``policy_library`` 模块。

**作用**：本模块属于 ``expert_review`` 体系内的辅助实现层；具体职责
由内部 class / function 的 docstring 描述。

**设计思路**：见包级 :mod:`expert_review.tools` 文档与
``PYDOC_INVENTORY.md`` 盘点清单。
"""
from __future__ import annotations

from typing import Any

from langchain_openai import ChatOpenAI

from ..semantic_router import SemanticCategory, semantic_multi_label, semantic_single_label


QUALITY_ISSUE_TYPES = {
    "readability_or_naming",
    "unused_or_noisy_structure",
    "evidence_overreach",
}

VV_ROLE_HINTS: dict[str, list[str]] = {
    "manual inspection": [
        "manual inspection by reviewers",
        "human reviewers compare artifacts item by item",
        "人工逐项对照或手工检查",
    ],
    "formal verification": [
        "formal verification or model checking",
        "proof-oriented validation of properties",
        "形式化验证或模型检查",
    ],
    "simulation": [
        "simulation or simulator-based validation",
        "run the model in a simulator to inspect behavior",
        "仿真或模拟验证",
    ],
    "testing": [
        "testing, benchmark scoring, TP/FP/FN, F1-like evaluation",
        "execute test cases against the artifact",
        "测试或基准打分",
    ],
    "syntax checker": [
        "syntax or grammar checking for notation well-formedness",
        "format checking rather than semantic behavior validation",
        "语法或格式检查",
    ],
}

SUMMARY_ROW_TYPE_CATEGORIES = [
    SemanticCategory(
        name="raw_score_row",
        definition="A published raw public score row without hidden per-element justification.",
        positive_examples=(
            "raw public score row",
            "published row is a raw public score row",
            "公开原始评分行",
        ),
    ),
    SemanticCategory(
        name="run_level_score",
        definition="A run-level summary score that reports the outcome of one run or one reviewed sample at summary granularity.",
        positive_examples=(
            "run-level summary score",
            "published row is a run-level summary score",
            "单次运行汇总分数",
        ),
    ),
    SemanticCategory(
        name="aggregate_stddev",
        definition="A variability or dispersion statistic such as standard deviation or variance.",
        positive_examples=(
            "standard deviation",
            "published row is a standard-deviation or dispersion statistic",
            "标准差或离散度统计",
        ),
        negative_examples=("average quality",),
    ),
    SemanticCategory(
        name="aggregate_max",
        definition="A best-case or highest-score aggregate statistic.",
        positive_examples=(
            "highest-score aggregate statistic",
            "best-case aggregate statistic",
            "最高分或最佳情况统计",
        ),
    ),
    SemanticCategory(
        name="aggregate_min",
        definition="A worst-case or minimum-score aggregate statistic.",
        positive_examples=(
            "minimum-score aggregate statistic",
            "worst-case aggregate statistic",
            "最低分或最差情况统计",
        ),
    ),
    SemanticCategory(
        name="aggregate_average",
        definition="An average, mean, or aggregate quality statistic over multiple reviewed items.",
        positive_examples=(
            "average aggregate quality statistic",
            "published row is an average or aggregate quality statistic",
            "平均值或聚合质量统计",
        ),
        negative_examples=("standard deviation",),
        threshold=0.14,
    ),
    SemanticCategory(
        name="summary_public_score",
        definition="A generic public summary score when the exact sub-type is not explicit.",
        positive_examples=("summary-level task under partial public evidence", "public summary score", "公开汇总分数"),
        threshold=0.10,
    ),
]

RECORD_DIAGRAM_TYPE_CATEGORIES = [
    SemanticCategory(
        name="stm",
        definition="A reactive behavioral model centered on states, transitions, guards, events, hierarchy, or orthogonal regions.",
        positive_examples=(
            "state machine or statechart",
            "target type: stm / generated_state_machine_model",
            "状态机或状态图",
        ),
    ),
    SemanticCategory(
        name="sd",
        definition="An interaction model centered on participants, messages, call order, and sequence semantics.",
        positive_examples=(
            "sequence diagram",
            "target type: sd / generated_sequence_diagram",
            "时序交互模型",
        ),
    ),
    SemanticCategory(
        name="act",
        definition="A control-flow or workflow model centered on actions, branches, joins, and flow progression.",
        positive_examples=(
            "activity diagram or workflow control flow",
            "target type: act / generated_behavior_model",
            "活动图或流程控制模型",
        ),
    ),
    SemanticCategory(
        name="bd",
        definition="An architectural or block-structure model centered on blocks, signals, and system composition.",
        positive_examples=(
            "block diagram or architecture model",
            "target type: bd / generated_block_diagram",
            "架构或块结构模型",
        ),
    ),
    SemanticCategory(
        name="Properties",
        definition="A model or artifact dominated by properties, constraints, rules, or verification targets rather than explicit executable behavior structure.",
        positive_examples=(
            "properties and constraints",
            "verification properties",
            "性质或约束模型",
        ),
    ),
]

VV_ROLE_CATEGORIES = [
    SemanticCategory(
        name="manual inspection",
        definition="Humans directly inspect or compare artifacts manually.",
        positive_examples=tuple(VV_ROLE_HINTS["manual inspection"]),
        threshold=0.12,
    ),
    SemanticCategory(
        name="formal verification",
        definition="The process relies on formal verification, proof, or model checking.",
        positive_examples=tuple(VV_ROLE_HINTS["formal verification"]),
        threshold=0.12,
    ),
    SemanticCategory(
        name="simulation",
        definition="The process relies on simulation or simulator-based behavioral checking.",
        positive_examples=tuple(VV_ROLE_HINTS["simulation"]),
        threshold=0.12,
    ),
    SemanticCategory(
        name="testing",
        definition="The process relies on testing, benchmark metrics, or empirical scoring.",
        positive_examples=tuple(VV_ROLE_HINTS["testing"]),
        threshold=0.12,
    ),
    SemanticCategory(
        name="syntax checker",
        definition="The process relies on syntax, grammar, or format checking rather than deep semantic review.",
        positive_examples=tuple(VV_ROLE_HINTS["syntax checker"]),
        threshold=0.35,
    ),
]

SUMMARY_TARGET_CATEGORIES = [
    SemanticCategory(
        name="BD",
        definition="The summary task targets behavior descriptions or behavioral design quality.",
        positive_examples=(
            "BD",
            "summary-level task for BD",
            "behavior description",
            "行为描述",
        ),
    ),
    SemanticCategory(
        name="SMD",
        definition="The summary task targets state-machine design or state-based model quality.",
        positive_examples=(
            "SMD",
            "summary-level task for SMD",
            "state machine design",
            "状态机设计",
        ),
    ),
    SemanticCategory(
        name="UCD",
        definition="The summary task targets use-case or interaction-oriented artifacts.",
        positive_examples=(
            "UCD",
            "summary-level task for UCD",
            "use case diagram",
            "用例或交互目标",
        ),
    ),
    SemanticCategory(
        name="Properties",
        definition="The summary task targets property definitions, property satisfaction, or constraint sets.",
        positive_examples=(
            "Properties",
            "summary-level task for Properties",
            "property target",
            "性质集合",
        ),
    ),
]

SUMMARY_TARGET_AXIS_CATEGORIES = [
    SemanticCategory(
        name="coarse_public_quality_target",
        definition="The public summary mainly reflects broad behavioral description quality, use-case communication quality, or property-set quality, so coarse visible quality signals deserve substantial weight.",
        positive_examples=(
            "BD behavior description",
            "UCD use case or interaction quality",
            "Properties property-set quality",
            "行为描述、用例表达或性质集合的总体质量",
        ),
        negative_examples=("SMD state machine design",),
        threshold=0.14,
    ),
    SemanticCategory(
        name="structure_intensive_target",
        definition="The public summary mainly reflects detailed state-machine design quality, where hidden structural rigor matters and coarse public evidence should remain more conservative.",
        positive_examples=(
            "SMD state machine design",
            "detailed state-based model structure quality",
            "状态机设计细节质量",
        ),
        negative_examples=("BD behavior description", "UCD use case"),
        threshold=0.14,
    ),
]


def _metadata_value(request: Any, key: str) -> str | None:
    """内部 helper：``_metadata_value``。

    :param request: 见函数签名与上下文。
    :param key: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    metadata = getattr(request, "metadata", {}) or {}
    value = str(metadata.get(key) or "").strip()
    return value or None


def _metadata_int(request: Any, key: str) -> int | None:
    """内部 helper：``_metadata_int``。

    :param request: 见函数签名与上下文。
    :param key: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    metadata = getattr(request, "metadata", {}) or {}
    value = metadata.get(key)
    try:
        return int(float(value))
    except Exception:
        return None


def _joined_text(values: list[str]) -> str:
    """内部 helper：``_joined_text``。

    :param values: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    return "\n".join(item for item in values if item)


def _canonical_summary_target(value: str | None) -> str | None:
    """内部 helper：``_canonical_summary_target``。

    :param value: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    if not value:
        return None
    normalized = value.strip().casefold()
    mapping = {
        "behavior_description": "BD",
        "bd": "BD",
        "behavior description": "BD",
        "state_machine_design": "SMD",
        "smd": "SMD",
        "state machine design": "SMD",
        "state-based model design": "SMD",
        "use_case_or_interaction": "UCD",
        "ucd": "UCD",
        "use case": "UCD",
        "interaction-oriented artifact": "UCD",
        "property_set": "Properties",
        "properties": "Properties",
        "property set": "Properties",
    }
    return mapping.get(normalized, value)


def _canonical_diagram_type(value: str | None) -> str | None:
    """内部 helper：``_canonical_diagram_type``。

    :param value: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    if not value:
        return None
    normalized = value.strip().casefold()
    mapping = {
        "reactive_state_model": "stm",
        "state_machine": "stm",
        "statechart": "stm",
        "stm": "stm",
        "state machine": "stm",
        "interaction_sequence_model": "sd",
        "sequence": "sd",
        "sd": "sd",
        "sequence diagram": "sd",
        "control_flow_model": "act",
        "activity": "act",
        "act": "act",
        "activity diagram": "act",
        "workflow": "act",
        "architecture_structure_model": "bd",
        "block": "bd",
        "bd": "bd",
        "block diagram": "bd",
        "property_rule_model": "Properties",
        "properties": "Properties",
        "property rule model": "Properties",
    }
    return mapping.get(normalized, value)


def _summary_target_from_metadata(request: Any) -> str | None:
    """内部 helper：``_summary_target_from_metadata``。

    :param request: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    return _canonical_summary_target(
        _metadata_value(request, "summary_target")
        or _metadata_value(request, "review_target")
        or _metadata_value(request, "target_semantics")
    )


def _summary_target_axis_from_metadata(request: Any) -> str | None:
    """内部 helper：``_summary_target_axis_from_metadata``。

    :param request: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    target = _summary_target_from_metadata(request)
    if target in {"BD", "UCD", "Properties"}:
        return "coarse_public_quality_target"
    if target == "SMD":
        return "structure_intensive_target"
    return None


def _artifact_semantics_from_metadata(request: Any) -> str | None:
    """内部 helper：``_artifact_semantics_from_metadata``。

    :param request: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    explicit = _canonical_diagram_type(_metadata_value(request, "artifact_semantics"))
    if explicit:
        return explicit
    diagram_type = (_metadata_value(request, "diagram_type") or "").casefold()
    return _canonical_diagram_type(diagram_type)


def _component_profile_from_metadata(request: Any) -> dict[str, Any]:
    """内部 helper：``_component_profile_from_metadata``。

    :param request: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    component_target = _metadata_value(request, "component_target")
    if not component_target:
        return {
            "component_target": "unknown",
            "component_review_mode": False,
            "component_public_tp": None,
            "component_public_fp": None,
            "component_public_fn": None,
            "component_pred_total": None,
            "component_reference_total": None,
            "component_source_kind": None,
        }
    return {
        "component_target": component_target,
        "component_review_mode": True,
        "component_public_tp": _metadata_int(request, "component_public_tp"),
        "component_public_fp": _metadata_int(request, "component_public_fp"),
        "component_public_fn": _metadata_int(request, "component_public_fn"),
        "component_pred_total": _metadata_int(request, "component_pred_total"),
        "component_reference_total": _metadata_int(request, "component_reference_total"),
        "component_source_kind": _metadata_value(request, "component_source_kind"),
    }


def infer_summary_row_type(*texts: str, request: Any | None = None, llm: ChatOpenAI | None = None) -> str:
    """``infer_summary_row_type`` 函数。

    :param request: 见函数签名与上下文。
    :param llm: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    metadata_hint = _metadata_value(request, "summary_row_type") if request is not None else None
    if metadata_hint:
        return metadata_hint
    specific = semantic_single_label(
        texts,
        [category for category in SUMMARY_ROW_TYPE_CATEGORIES if category.name != "summary_public_score"],
        llm=llm,
        task_name="summary_row_type_specific",
        default_label="unknown",
    )
    if specific["label"] != "unknown":
        return specific["label"]
    return semantic_single_label(
        texts,
        SUMMARY_ROW_TYPE_CATEGORIES,
        llm=llm,
        task_name="summary_row_type",
        default_label="summary_public_score",
    )["label"]


def infer_summary_target(*texts: str, request: Any | None = None, llm: ChatOpenAI | None = None) -> str:
    """``infer_summary_target`` 函数。

    :param request: 见函数签名与上下文。
    :param llm: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    metadata_hint = _summary_target_from_metadata(request) if request is not None else None
    if metadata_hint:
        return metadata_hint
    return semantic_single_label(
        texts,
        SUMMARY_TARGET_CATEGORIES,
        llm=llm,
        task_name="summary_target",
        default_label="unknown",
    )["label"]


def infer_record_diagram_type(*texts: str, request: Any | None = None, llm: ChatOpenAI | None = None) -> str:
    """``infer_record_diagram_type`` 函数。

    :param request: 见函数签名与上下文。
    :param llm: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    metadata_hint = _artifact_semantics_from_metadata(request) if request is not None else None
    if metadata_hint:
        return metadata_hint
    return semantic_single_label(
        texts,
        RECORD_DIAGRAM_TYPE_CATEGORIES,
        llm=llm,
        task_name="record_diagram_type",
        default_label="unknown",
    )["label"]


def infer_summary_target_axis(*texts: str, request: Any | None = None, llm: ChatOpenAI | None = None) -> str:
    """``infer_summary_target_axis`` 函数。

    :param request: 见函数签名与上下文。
    :param llm: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    metadata_hint = _summary_target_axis_from_metadata(request) if request is not None else None
    if metadata_hint:
        return metadata_hint
    return semantic_single_label(
        texts,
        SUMMARY_TARGET_AXIS_CATEGORIES,
        llm=llm,
        task_name="summary_target_axis",
        default_label="generic_target",
    )["label"]


def _summary_semantic_profile(summary_target: str, summary_row_type: str) -> dict[str, Any]:
    # Tier 1 ablation 验证：summary_public_gain / summary_hidden_risk_scale 单独中和 |ΔHAI| < 0.05；
    # summary_target_semantic_bias 单独中和 ΔHAI = -0.25。
    # 真正承载 ΔHAI 的字段只有 summary_row_target_interaction_bias 与（次级的）target_bias。
    """内部 helper：``_summary_semantic_profile``。

    :param summary_target: 见函数签名与上下文。
    :param summary_row_type: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    if summary_target == "SMD":
        profile_name = "structure_intensive_target"
        target_bias = -0.03
    elif summary_target == "Properties":
        profile_name = "property_constraint_target"
        target_bias = 0.02
    elif summary_target in {"BD", "UCD"}:
        profile_name = "public_behavior_quality_target"
        target_bias = 0.06
    else:
        profile_name = "generic_target"
        target_bias = 0.0

    if summary_row_type == "aggregate_stddev":
        target_bias = 0.0

    row_target_bias = 0.0
    if summary_row_type == "raw_score_row" and profile_name in {
        "public_behavior_quality_target",
        "property_constraint_target",
    }:
        row_target_bias = 0.10
    elif summary_row_type == "run_level_score" and profile_name == "structure_intensive_target":
        row_target_bias = -0.01
    elif summary_row_type in {
        "aggregate_average",
        "aggregate_max",
        "aggregate_min",
        "summary_public_score",
    } and profile_name == "structure_intensive_target":
        row_target_bias = -0.08

    return {
        "summary_profile_name": profile_name,
        "summary_target_semantic_bias": target_bias,
        "summary_row_target_interaction_bias": row_target_bias,
    }


def _record_semantic_profile(record_diagram_type: str) -> dict[str, Any]:
    # Tier 1 ablation 验证：act/sd/stm 三套
    # record_alignment_bonus_scale / record_high_fidelity_bonus_scale /
    # record_partial_penalty_scale / record_partial_only_penalty_scale 全部单独中和后 |ΔHAI| ≤ 0.07，
    # 且其中 record_high_fidelity_bonus_scale 在当前 dataset 上 if 分支一次也未触发（strict 0）。
    # 只保留 record_diagram_semantic_bias 与 record_alignment_matched_floor 这两个对 record 路径有信号的字段。
    """内部 helper：``_record_semantic_profile``。

    :param record_diagram_type: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    if record_diagram_type == "act":
        return {
            "record_profile_name": "control_flow_explicit_profile",
            "record_diagram_semantic_bias": 0.12,
            "record_alignment_matched_floor": 0.0,
        }
    if record_diagram_type == "sd":
        return {
            "record_profile_name": "interaction_order_sensitive_profile",
            "record_diagram_semantic_bias": -0.02,
            "record_alignment_matched_floor": 0.12,
        }
    if record_diagram_type == "stm":
        return {
            "record_profile_name": "state_reactive_balance_profile",
            "record_diagram_semantic_bias": 0.0,
            "record_alignment_matched_floor": 0.10,
        }
    return {
        "record_profile_name": "generic_record_profile",
        "record_diagram_semantic_bias": 0.0,
        "record_alignment_matched_floor": 0.0,
    }


def infer_aggregate_signal(*texts: str, request: Any | None = None, llm: ChatOpenAI | None = None) -> str:
    """``infer_aggregate_signal`` 函数。

    :param request: 见函数签名与上下文。
    :param llm: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    row_type = infer_summary_row_type(*texts, request=request, llm=llm)
    return _aggregate_signal_from_row_type(row_type)


def _aggregate_signal_from_row_type(row_type: str) -> str:
    """内部 helper：``_aggregate_signal_from_row_type``。

    :param row_type: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    return {
        "aggregate_stddev": "stddev",
        "aggregate_average": "average",
        "aggregate_max": "max",
        "aggregate_min": "min",
        "run_level_score": "summary",
        "raw_score_row": "summary",
        "summary_public_score": "summary",
    }.get(row_type, "direct_review")


def detect_vv_roles(texts: list[str], *, llm: ChatOpenAI | None = None) -> list[str]:
    """``detect_vv_roles`` 函数。

    :param texts: 见函数签名与上下文。
    :param llm: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    return semantic_multi_label(
        texts,
        VV_ROLE_CATEGORIES,
        llm=llm,
        task_name="validation_roles",
        allow_empty=True,
    )["labels"]


def build_review_policy(
    contract: Any,
    regime: Any,
    request: Any,
    input_dossier: Any,
    pred_dossier: Any,
    ref_dossier: Any,
    *,
    llm: ChatOpenAI | None = None,
) -> dict[str, Any]:
    """``build_review_policy`` 函数。

    :param contract: 见函数签名与上下文。
    :param regime: 见函数签名与上下文。
    :param request: 见函数签名与上下文。
    :param input_dossier: 见函数签名与上下文。
    :param pred_dossier: 见函数签名与上下文。
    :param ref_dossier: 见函数签名与上下文。
    :param llm: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
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
        str(getattr(pred_dossier, "summary", "") or ""),
        str(getattr(ref_dossier, "summary", "") or ""),
    ]
    component_profile = _component_profile_from_metadata(request)
    component_review_mode = bool(component_profile.get("component_review_mode"))
    regime_name = getattr(regime, "regime", "")

    if regime_name == "summary_only" and not component_review_mode:
        summary_row_type = infer_summary_row_type(*contract_texts, request=request, llm=llm)
        aggregate_signal = _aggregate_signal_from_row_type(summary_row_type)
        summary_semantics_explicit = aggregate_signal != "direct_review"
        summary_target = infer_summary_target(*contract_texts, request=request, llm=llm)
        if summary_target == "SMD":
            summary_target_axis = "structure_intensive_target"
        elif summary_target in {"BD", "UCD", "Properties"}:
            summary_target_axis = "coarse_public_quality_target"
        else:
            summary_target_axis = infer_summary_target_axis(*contract_texts, request=request, llm=llm)
    else:
        summary_row_type = "direct_review"
        aggregate_signal = "direct_review"
        summary_semantics_explicit = False
        summary_target = "unknown"
        summary_target_axis = "generic_target"

    if regime_name in {"record_level", "mixed_evidence"} and not component_review_mode:
        record_diagram_type = infer_record_diagram_type(*contract_texts, request=request, llm=llm)
    else:
        record_diagram_type = _artifact_semantics_from_metadata(request) if request is not None else None
        record_diagram_type = record_diagram_type or "unknown"
    summary_profile = _summary_semantic_profile(summary_target, summary_row_type)
    record_profile = _record_semantic_profile(record_diagram_type)

    quality_axes = {
        "readability": 1.20 if {"clarity", "quality"} & focus else 1.0,
        "naming": 1.15 if {"clarity", "quality"} & focus else 1.0,
        "noise": 1.15 if {"hallucination", "traceability"} & focus else 1.0,
        "complexity": 1.10 if {"quality", "behavior"} & focus else 1.0,
    }
    score_semantics = "artifact_quality"
    if getattr(regime, "regime", "") == "summary_only":
        score_semantics = "summary_stat_stddev" if aggregate_signal == "stddev" else "summary_quality"
    elif getattr(regime, "regime", "") == "protocol_only":
        score_semantics = "protocol_assurance"
    if component_review_mode:
        score_semantics = "component_public_f1"

    allow_element_level_claims = getattr(regime, "regime", "") == "record_level"
    allow_requirement_defect_claims = getattr(regime, "regime", "") == "record_level"
    if getattr(regime, "regime", "") == "mixed_evidence" and getattr(pred_dossier, "observability", "low") == "high":
        allow_requirement_defect_claims = True
    if component_review_mode:
        allow_element_level_claims = False
        allow_requirement_defect_claims = False

    base_confidence_cap = 0.84
    if getattr(regime, "regime", "") == "summary_only":
        base_confidence_cap = 0.56 if score_semantics == "summary_quality" else 0.48
    elif getattr(regime, "regime", "") == "protocol_only":
        base_confidence_cap = 0.42
    elif getattr(regime, "regime", "") == "mixed_evidence":
        base_confidence_cap = 0.68
    if component_review_mode:
        base_confidence_cap = max(base_confidence_cap, 0.88)

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
        "summary_row_type": summary_row_type,
        "summary_target": summary_target,
        "summary_target_axis": summary_target_axis,
        **summary_profile,
        "record_diagram_type": record_diagram_type,
        **record_profile,
        **component_profile,
        "allow_element_level_claims": allow_element_level_claims,
        "allow_requirement_defect_claims": allow_requirement_defect_claims,
        "base_confidence_cap": base_confidence_cap,
        "vv_role_hints": VV_ROLE_HINTS,
        "quality_issue_types": sorted(QUALITY_ISSUE_TYPES),
    }