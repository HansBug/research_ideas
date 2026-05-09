"""Evidence Regime Estimator agent —— 推断本次评审属于哪种 evidence regime。

**作用**：根据 prompt + dossiers 把本次评审分类到以下 regime 之一：

* ``record_level``：完整 NL 需求 + 完整制品 (pred + ref)，可做 element-level 评判
* ``summary_only``：只有汇总分数 / 公开 summary 行，无 element-level evidence
* ``protocol_only``：评审 protocol / process / V&V roles，不评具体制品
* ``mixed_evidence``：上述若干混合

regime 决定下游 sanity bound、policy weight、confidence cap 等。

**设计思路**：

1. **优先看 metadata**：若 ``request.metadata["review_surface"]`` 显式
   指定了 regime，直接采用；
2. **其次用 semantic router**：把 prompt 文本归类到 3 个 surface
   category 之一（``protocol_assurance`` / ``summary_public_score`` /
   ``direct_artifact_review``）；
3. **配合 dossier observability**：综合 has_prediction / has_reference
   /pred_observability / ref_observability，得出最终 regime 标识。
"""

from __future__ import annotations

from langchain_openai import ChatOpenAI

from ..semantic_router import SemanticCategory, semantic_single_label
from ..schemas.dossiers import ArtifactDossier, EvidenceRegime
from ..schemas.request import ExpertReviewRequest


REVIEW_SURFACE_CATEGORIES = [
    SemanticCategory(
        name="protocol_assurance",
        definition="The task is mainly about reviewing the evaluation protocol, reviewer roles, evidence limits, or assurance process rather than directly judging a full concrete artifact.",
        positive_examples=(
            "review the human evaluation protocol",
            "focus on manual inspection, verification, simulation, and testing roles",
            "评审评测流程和证据边界",
        ),
        negative_examples=("review the predicted artifact against the reference",),
    ),
    SemanticCategory(
        name="summary_public_score",
        definition="The task is mainly about a public summary score or aggregate statistic when fine-grained artifact evidence is unavailable.",
        positive_examples=(
            "summary-level task under partial public evidence",
            "public summary row semantics",
            "公开汇总分数或统计行",
        ),
        negative_examples=("full artifact with visible prediction and reference",),
    ),
    SemanticCategory(
        name="direct_artifact_review",
        definition="The task is mainly about reviewing a concrete predicted artifact against input and possibly a reference artifact.",
        positive_examples=(
            "review the predicted artifact against the available evidence",
            "inspect the produced state machine",
            "评审生成的模型本身",
        ),
        threshold=0.12,
    ),
]


def _metadata_surface(request: ExpertReviewRequest) -> str | None:
    """从 ``request.metadata`` 读取显式 ``review_surface`` 提示。

    :param request: :class:`ExpertReviewRequest`
    :return: 非空字符串或 ``None``
    """
    metadata = getattr(request, "metadata", {}) or {}
    value = str(metadata.get("review_surface") or "").strip()
    return value or None


def estimate_evidence_regime(
    request: ExpertReviewRequest,
    pred_dossier: ArtifactDossier,
    ref_dossier: ArtifactDossier,
    llm: ChatOpenAI | None = None,
) -> EvidenceRegime:
    """推断本次评审的 evidence regime 分类。

    :param request: :class:`ExpertReviewRequest`
    :param pred_dossier: 预测制品 dossier
    :param ref_dossier: 参考制品 dossier
    :param llm: 可选 LLM client（当前实现主要走 deterministic
        + semantic_router 路径，``llm`` 仅作扩展位）
    :return: 完整填充的 :class:`EvidenceRegime`
    """
    has_prediction = bool((request.pred_output or "").strip())
    has_reference = bool((request.ref_output or "").strip())
    review_surface = _metadata_surface(request)
    if not review_surface:
        review_surface = semantic_single_label(
            [request.prompt, request.input_text],
            REVIEW_SURFACE_CATEGORIES,
            llm=llm,
            task_name="evidence_regime_review_surface",
            default_label="direct_artifact_review",
        )["label"]
    context_note = (
        "Structured review-surface metadata explicitly marks this task as a public summary judgement."
        if review_surface == "summary_public_score" and _metadata_surface(request)
        else "Structured review-surface metadata explicitly marks this task as protocol assurance."
        if review_surface == "protocol_assurance" and _metadata_surface(request)
        else "Semantic routing classified this task as protocol-assurance oriented."
        if review_surface == "protocol_assurance"
        else "Semantic routing classified this task as summary-public-score oriented."
        if review_surface == "summary_public_score"
        else "Semantic routing classified this task as a direct artifact review."
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
    if review_surface == "protocol_assurance" and (
        pred_dossier.observability == "low" or (has_reference and ref_dossier.observability == "low")
    ):
        return EvidenceRegime(
            regime="protocol_only",
            rationale=f"{context_note} Concrete artifact evidence remains sparse, so protocol-only assurance is safer than pseudo-precise artifact review.",
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
            pred_dossier.format_guess == "summary_text" or review_surface == "summary_public_score"
        ) else "mixed_evidence"
        rationale = "Only predicted artifact evidence is available, so review must rely on requirements and direct artifact reading."
        if regime == "summary_only":
            rationale = f"{context_note} Prediction evidence behaves like a public summary judgement rather than a full directly reviewable artifact."
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
