"""Input Analyst agent —— 把 NL 需求文本解析为 :class:`InputDossier`。

**作用**：

1. 调用 :func:`inventory.parse_requirement_items` 把 NL 需求切成离散
   的 requirement items；
2. 用 semantic router 推断 prompt 暗含的 review 上下文（如"允许语义
   等价"、"关注未支持额外结构"）；
3. 用 semantic router 给每条需求打 intent 标签（``conditional_constraint``
   / ``ambiguous_statement``）；
4. 提取 entity_hints（去 stopwords 后的内容词）；
5. 推断 observability 档位（high / medium / low），影响下游
   confidence cap。

**设计思路**：

* **deterministic-only**：本 agent 不接收 LLM 参数；所有解析与分类
  都通过 :mod:`semantic_router` 与 :mod:`inventory` 完成；
* **observability 三档判定**：requirements 数 ≥ 4 或文本 ≥ 220 字符
  → high；2-3 条 / 80-219 字符 → medium；其余 → low。
"""

from __future__ import annotations

from typing import Any

from ..schema import EvidenceItem, RequirementTraceResult
from ..inventory import parse_requirement_items
from ..semantic_router import SemanticCategory, semantic_multi_label
from ..schemas.dossiers import InputDossier
from ..utils import normalize_id
from .common import content_tokens


def _make_evidence_item(source: str, locator: str | None, snippet: str, explanation: str) -> EvidenceItem:
    """内部 helper：构造规范化的 :class:`EvidenceItem`。

    与 :func:`agents.common.make_evidence_item` 等价的本地副本，避免
    循环 import；snippet/explanation 会自动 strip。
    """
    return EvidenceItem(
        source=source,
        locator=locator,
        snippet=snippet.strip(),
        explanation=explanation.strip(),
    )


PROMPT_CONTEXT_CATEGORIES = [
    SemanticCategory(
        name="semantic_equivalence",
        definition="The review explicitly says semantically equivalent but differently structured outputs should receive credit.",
        positive_examples=(
            "reward semantically equivalent but differently structured designs",
            "允许等价但不同构的设计获得 credit",
            "focus on semantic equivalence rather than exact structure",
        ),
        negative_examples=("exact string match only",),
    ),
    SemanticCategory(
        name="unsupported_extra_structure",
        definition="The review explicitly asks to inspect unsupported, hallucinated, unjustified, or extra structure.",
        positive_examples=(
            "check unsupported extra structure",
            "指出没有需求依据的额外结构",
            "inspect hallucinated or unjustified model elements",
        ),
        negative_examples=("ignore extra content",),
    ),
]

REQUIREMENT_INTENT_CATEGORIES = [
    SemanticCategory(
        name="conditional_constraint",
        definition="The statement expresses a constraint, guard, prohibition, or condition under which behavior is allowed, required, or forbidden.",
        positive_examples=(
            "only allow logoff when printing is inactive",
            "power off only from Ready",
            "when a paper jam occurs, suspend printing",
            "必须满足条件后才能迁移",
            "仅在某条件下允许执行",
        ),
        negative_examples=("simple descriptive background sentence",),
        threshold=0.14,
    ),
    SemanticCategory(
        name="ambiguous_statement",
        definition="The statement intentionally leaves uncertainty, approximation, or optional interpretation rather than stating one precise requirement.",
        positive_examples=(
            "a possible collision may activate one of several controls",
            "roughly choose one branch and/or another",
            "可能触发其中某个动作",
            "大致如此但不完全确定",
        ),
        negative_examples=("precise requirement with explicit trigger and target",),
    ),
]


def _dedupe_strings(items: list[str]) -> list[str]:
    """内部 helper：按 normalize_id 去重保留首次原文。

    与 :func:`agents.common.dedupe_strings` 等价的本地副本。
    """
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        clean = str(item).strip()
        key = normalize_id(clean)
        if not clean or not key or key in seen:
            continue
        seen.add(key)
        result.append(clean)
    return result


def build_input_dossier(request: Any) -> InputDossier:
    """把 :class:`ExpertReviewRequest` 中的 NL 需求与 prompt 解析为
    :class:`InputDossier`。

    :param request: :class:`ExpertReviewRequest` 实例
    :return: 完整填充的 :class:`InputDossier`，含 requirements /
        behaviors / constraints / ambiguities / evidence / observability
        / entity_hints / context_clues
    """
    raw_requirements = parse_requirement_items(request.input_text, [])
    requirements = [
        RequirementTraceResult(
            requirement_id=item.requirement_id,
            requirement_text=item.text,
            status="unreviewed",
            reason_text="Requirement extracted from input text and awaiting traceability analysis.",
            matched_element_ids=[],
            confidence=0.5,
        )
        for item in raw_requirements
    ]
    requirement_texts = [item.requirement_text for item in requirements]
    clues: list[str] = []
    semantic_context = semantic_multi_label(
        [request.prompt],
        PROMPT_CONTEXT_CATEGORIES,
        task_name="input_prompt_context",
    )
    if "semantic_equivalence" in semantic_context["labels"]:
        clues.append("Prompt explicitly allows semantic equivalence beyond structural isomorphism.")
    if "unsupported_extra_structure" in semantic_context["labels"]:
        clues.append("Prompt explicitly asks to inspect unsupported extra structure.")
    behaviors = _dedupe_strings(requirement_texts)
    requirement_intents = {
        text: semantic_multi_label(
            [text],
            REQUIREMENT_INTENT_CATEGORIES,
            task_name="requirement_intent",
            allow_empty=True,
        )["labels"]
        for text in requirement_texts
    }
    constraints = _dedupe_strings(
        [text for text, labels in requirement_intents.items() if "conditional_constraint" in labels]
    )
    ambiguities = _dedupe_strings(
        [text for text, labels in requirement_intents.items() if "ambiguous_statement" in labels]
    )
    evidence = [
        _make_evidence_item(
            "input",
            f"input:requirement:{item.requirement_id}",
            item.requirement_text,
            "Requirement extracted into the input dossier.",
        )
        for item in requirements[:4]
    ]
    entity_hints = _dedupe_strings(
        [
            token
            for text in requirement_texts
            for token in content_tokens(text)
            if token not in {"shall", "should", "must", "allow", "system"}
        ]
    )[:20]
    if len(requirements) >= 4 or len(request.input_text.strip()) >= 220:
        observability = "high"
        observability_reason = "Input dossier contains multiple explicit requirements and enough textual detail for grounding."
    elif requirements or len(request.input_text.strip()) >= 80:
        observability = "medium"
        observability_reason = "Input dossier exposes some grounding clues, but not all constraints are explicit."
    else:
        observability = "low"
        observability_reason = "Input dossier is sparse, so requirement grounding will remain limited."
    return InputDossier(
        summary=request.input_text.strip() or "No explicit input description was provided.",
        requirements=requirements,
        behaviors=behaviors[:16],
        constraints=constraints[:12],
        ambiguities=ambiguities[:8],
        evidence=evidence,
        observability=observability,
        observability_reason=observability_reason,
        entity_hints=entity_hints,
        context_clues=clues,
    )


__all__ = ["build_input_dossier"]
