"""Contract Router agent —— 从 prompt 推断评审契约 :class:`ReviewContract`。

**作用**：解析用户给的 NL prompt，把 "评审应该关注什么 / 需要多严格 /
是否有等价规则" 等元信息抽出来打包为 :class:`ReviewContract`，下发给
后续 review_policy_builder 配置 dimension weight。

**设计思路**：

1. **deterministic 优先**：:func:`default_contract` 先用 semantic
   router（基于词嵌入相似度的分类，见 :mod:`semantic_router`）做 9 类
   focus + 2 类 strictness 分类；
2. **LLM 精化可选**：:func:`route_contract` 在 LLM 可用时尝试 LLM 路径，
   返回 JSON 的字段会覆盖 deterministic 默认；LLM 失败 / 返回非 dict
   时回退 deterministic；
3. **focus / strictness 类别静态固定**：``FOCUS_CATEGORIES`` 与
   ``STRICTNESS_CATEGORIES`` 是 hard-coded 9+2 类——保证 routing 结果
   可重复、可比对。
"""

from __future__ import annotations

from langchain_openai import ChatOpenAI

from ..prompts.contract_router import CONTRACT_ROUTER_SYSTEM_PROMPT
from ..semantic_router import SemanticCategory, semantic_multi_label, semantic_single_label
from ..schemas.dossiers import ReviewContract
from .llm_helpers import invoke_llm_json


FOCUS_CATEGORIES = [
    SemanticCategory(
        name="coverage",
        definition="Inspect whether required behaviors, elements, or cases are fully covered and not omitted.",
        positive_examples=("coverage and completeness", "检查覆盖与完整性", "是否遗漏关键需求"),
    ),
    SemanticCategory(
        name="behavior",
        definition="Inspect whether the produced artifact preserves the intended behavior and reactions.",
        positive_examples=("behavioral consistency", "行为一致性", "preserve intended behavior"),
    ),
    SemanticCategory(
        name="consistency",
        definition="Inspect whether the artifact contains contradictions, incompatible transitions, or inconsistent semantics.",
        positive_examples=("consistency", "检查矛盾和不一致", "avoid contradictory behavior"),
    ),
    SemanticCategory(
        name="traceability",
        definition="Inspect whether requirements can be grounded to the artifact and whether claims are supported by visible evidence.",
        positive_examples=("traceability", "需求可追溯", "ground requirements to the artifact"),
    ),
    SemanticCategory(
        name="clarity",
        definition="Inspect readability, naming quality, and whether the artifact remains understandable to reviewers.",
        positive_examples=("clarity and readability", "可读性和命名", "reviewability"),
    ),
    SemanticCategory(
        name="syntax",
        definition="Inspect notation conformance, structural well-formedness, or syntax-level correctness.",
        positive_examples=("syntax and notation", "语法和格式", "well-formed notation"),
    ),
    SemanticCategory(
        name="quality",
        definition="Inspect pragmatic artifact quality, proportionality, disciplined modeling, and overall engineering quality.",
        positive_examples=("overall quality", "建模质量", "pragmatic quality"),
    ),
    SemanticCategory(
        name="hallucination",
        definition="Inspect unsupported, hallucinated, unjustified, or extra structure.",
        positive_examples=("unsupported extra structure", "额外结构", "hallucinated element"),
    ),
    SemanticCategory(
        name="equivalence",
        definition="Inspect semantic equivalence and preserve credit for equivalent but differently structured designs.",
        positive_examples=("equivalent but different", "等价但不同构", "semantic equivalence"),
    ),
]

STRICTNESS_CATEGORIES = [
    SemanticCategory(
        name="strict",
        definition="The review should apply a stricter or more rigorous penalty policy and tolerate fewer weakly supported assumptions.",
        positive_examples=("strict and rigorous", "严格评审", "penalize weak evidence more aggressively"),
        negative_examples=("balanced review", "keep it coarse and balanced"),
        threshold=0.20,
    ),
    SemanticCategory(
        name="balanced",
        definition="The review should remain balanced, evidence-aware, and avoid over-penalizing uncertain cases.",
        positive_examples=("balanced review", "平衡地评审", "stay evidence-aware and not overclaim"),
        threshold=0.12,
    ),
]


def default_contract(prompt: str) -> ReviewContract:
    """根据 NL prompt 用 semantic router 构造默认 :class:`ReviewContract`。

    :param prompt: 评审 prompt
    :return: 含 focus / strictness / 默认 equivalence/evidence rules 的
        :class:`ReviewContract`
    """
    focus = semantic_multi_label([prompt], FOCUS_CATEGORIES, task_name="contract_focus", allow_empty=False)["labels"]
    equivalence_rules = [
        "Equivalent but differently structured designs should receive credit when observable behavior is preserved.",
        "Pure surface mismatch is not enough to declare failure.",
    ]
    evidence_rules = [
        "Do not overclaim unsupported errors when evidence is sparse.",
        "Tie every strong judgement to visible evidence from input, prediction, or reference.",
    ]
    strictness_label = semantic_single_label(
        [prompt],
        STRICTNESS_CATEGORIES,
        task_name="contract_strictness",
        default_label="balanced",
    )["label"]
    return ReviewContract(
        task_summary=prompt.strip() or "Review the predicted artifact against the available evidence.",
        requested_focus=focus,
        domain_knowledge=[],
        equivalence_rules=equivalence_rules,
        evidence_rules=evidence_rules,
        strictness="strict" if strictness_label == "strict" else "balanced",
        notes=["Deterministic contract routing used semantic category matching rather than keyword triggers."],
    )


def route_contract(prompt: str, llm: ChatOpenAI | None, notes: list[str]) -> ReviewContract:
    """LLM 路径优先 + deterministic fallback 的 contract routing。

    :param prompt: 评审 prompt
    :param llm: LLM client（``None`` 直接走 deterministic）
    :param notes: 由调用方提供的 list，用于追加 audit 笔记
    :return: :class:`ReviewContract`
    """
    fallback = default_contract(prompt)
    if llm is None:
        return fallback
    payload = invoke_llm_json(
        llm,
        [
            ("system", CONTRACT_ROUTER_SYSTEM_PROMPT),
            (
                "user",
                "Extract a review contract from the prompt.\n\n"
                "Return JSON with keys: task_summary, requested_focus, domain_knowledge, "
                "equivalence_rules, evidence_rules, strictness, notes.\n\n"
                f"Prompt:\n{prompt}",
            ),
        ],
        operation="contract_router",
    )
    if not isinstance(payload, dict):
        notes.append("Contract router fell back to deterministic prompt parsing.")
        return fallback
    return ReviewContract(
        task_summary=str(payload.get("task_summary") or fallback.task_summary).strip(),
        requested_focus=[str(item).strip() for item in payload.get("requested_focus", []) if str(item).strip()],
        domain_knowledge=[str(item).strip() for item in payload.get("domain_knowledge", []) if str(item).strip()],
        equivalence_rules=[
            str(item).strip()
            for item in payload.get("equivalence_rules", fallback.equivalence_rules)
            if str(item).strip()
        ],
        evidence_rules=[
            str(item).strip() for item in payload.get("evidence_rules", fallback.evidence_rules) if str(item).strip()
        ],
        strictness=str(payload.get("strictness") or fallback.strictness).strip() or "balanced",
        notes=[str(item).strip() for item in payload.get("notes", []) if str(item).strip()],
    )


__all__ = ["default_contract", "route_contract"]
