"""``semantic_router`` 模块。

**作用**：本模块属于 ``expert_review`` 体系内的辅助实现层；具体职责
由内部 class / function 的 docstring 描述。

**设计思路**：见包级 :mod:`expert_review.` 文档与
``PYDOC_INVENTORY.md`` 盘点清单。
"""
from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from functools import lru_cache
import json
import re
from typing import Any, Iterable, Sequence

from langchain_openai import ChatOpenAI

from .agents.llm_helpers import invoke_llm_json
from .utils import normalize_id, normalize_text, semantic_terms


@dataclass(frozen=True, slots=True)
class SemanticCategory:
    """``SemanticCategory`` 数据/逻辑类；详见所在模块顶部 docstring。"""
    name: str
    definition: str
    positive_examples: tuple[str, ...] = ()
    negative_examples: tuple[str, ...] = ()
    threshold: float = 0.18


def _invoke_llm_json(
    llm: ChatOpenAI,
    messages: list[tuple[str, str]],
    *,
    operation: str,
) -> dict[str, Any] | None:
    """内部 helper：``_invoke_llm_json``。

    :param llm: 见函数签名与上下文。
    :param messages: 见函数签名与上下文。
    :param operation: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    return invoke_llm_json(llm, messages, operation=operation)


@lru_cache(maxsize=200000)
def _semantic_similarity(left: str, right: str) -> float:
    """内部 helper：``_semantic_similarity``。

    :param left: 见函数签名与上下文。
    :param right: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    left_text = normalize_text(left).casefold()
    right_text = normalize_text(right).casefold()
    if not left_text or not right_text:
        return 0.0
    left_terms = semantic_terms(left_text)
    right_terms = semantic_terms(right_text)
    term_overlap = 0.0
    reference_coverage = 0.0
    if left_terms and right_terms:
        term_overlap = len(left_terms & right_terms) / len(left_terms | right_terms)
        reference_coverage = len(left_terms & right_terms) / len(right_terms)
    sequence = SequenceMatcher(None, left_text, right_text).ratio()
    return 0.45 * term_overlap + 0.35 * reference_coverage + 0.20 * sequence


def _category_payload(category: SemanticCategory) -> dict[str, Any]:
    """内部 helper：``_category_payload``。

    :param category: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    return {
        "name": category.name,
        "definition": category.definition,
        "positive_examples": list(category.positive_examples),
        "negative_examples": list(category.negative_examples),
    }


def _category_score(texts: Sequence[str], category: SemanticCategory) -> float:
    """内部 helper：``_category_score``。

    :param texts: 见函数签名与上下文。
    :param category: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    references = [
        category.name.replace("_", " "),
        category.definition,
        *category.positive_examples,
    ]
    positives = [
        _semantic_similarity(text, reference)
        for text in texts
        for reference in references
        if text and reference
    ]
    positive_score = max(positives) if positives else 0.0
    negatives = [
        _semantic_similarity(text, reference)
        for text in texts
        for reference in category.negative_examples
        if text and reference
    ]
    negative_score = max(negatives) if negatives else 0.0
    return max(0.0, positive_score - 0.30 * negative_score)


@lru_cache(maxsize=50000)
def _semantic_fragments(text: str) -> tuple[str, ...]:
    """内部 helper：``_semantic_fragments``。

    :param text: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    normalized = normalize_text(text)
    if not normalized:
        return ()
    fragments: list[str] = [normalized]
    raw_pieces = re.split(r"[\n。！？!?;；,，]+", str(text))
    for piece in raw_pieces:
        clean = normalize_text(piece)
        if clean:
            fragments.append(clean)
        for sub_piece in re.split(r"[:：]\s*", clean):
            sub_clean = normalize_text(sub_piece)
            if sub_clean:
                fragments.append(sub_clean)
    deduped: list[str] = []
    seen: set[str] = set()
    for fragment in fragments:
        key = normalize_id(fragment)
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(fragment)
    return tuple(deduped)


def _prepare_texts(texts: Iterable[Any]) -> list[str]:
    """内部 helper：``_prepare_texts``。

    :param texts: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    prepared: list[str] = []
    seen: set[str] = set()
    for item in texts:
        text = normalize_text(item)
        for fragment in _semantic_fragments(text):
            key = normalize_id(fragment)
            if not key or key in seen:
                continue
            seen.add(key)
            prepared.append(fragment)
    return prepared


def semantic_single_label(
    texts: Iterable[Any],
    categories: Sequence[SemanticCategory],
    *,
    llm: ChatOpenAI | None = None,
    task_name: str,
    default_label: str = "unknown",
) -> dict[str, Any]:
    """``semantic_single_label`` 函数。

    :param texts: 见函数签名与上下文。
    :param categories: 见函数签名与上下文。
    :param llm: 见函数签名与上下文。
    :param task_name: 见函数签名与上下文。
    :param default_label: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    prepared = _prepare_texts(texts)
    if not categories:
        return {"label": default_label, "confidence": 0.0, "scores": {}, "source": "empty"}

    if llm is not None and prepared:
        payload = _invoke_llm_json(
            llm,
            [
                (
                    "system",
                    "You are a semantic classifier for an expert-review runtime. "
                    "Classify by meaning, not by surface keyword matching. "
                    "Use the provided category definitions and examples. "
                    "Return strict JSON only.",
                ),
                (
                    "user",
                    "Task name: "
                    + task_name
                    + "\n\nChoose exactly one label from the categories below.\n"
                    + "Return JSON with keys: label, confidence, rationale.\n\n"
                    + "Categories:\n"
                    + json.dumps([_category_payload(category) for category in categories], ensure_ascii=False, indent=2)
                    + "\n\nText fragments:\n"
                    + json.dumps(prepared, ensure_ascii=False, indent=2),
                ),
            ],
            operation=f"semantic_router:{task_name}",
        )
        if isinstance(payload, dict):
            label = normalize_text(payload.get("label") or default_label) or default_label
            allowed = {category.name for category in categories}
            if label in allowed:
                try:
                    confidence = max(0.0, min(1.0, float(payload.get("confidence", 0.75))))
                except Exception:
                    confidence = 0.75
                return {"label": label, "confidence": confidence, "scores": {}, "source": "llm"}

    scores = {category.name: _category_score(prepared, category) for category in categories}
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    if not ranked:
        return {"label": default_label, "confidence": 0.0, "scores": scores, "source": "deterministic"}
    label, best_score = ranked[0]
    second_score = ranked[1][1] if len(ranked) > 1 else 0.0
    threshold = next((category.threshold for category in categories if category.name == label), 0.18)
    if best_score < threshold:
        return {"label": default_label, "confidence": best_score, "scores": scores, "source": "deterministic"}
    confidence = max(0.0, min(1.0, 0.55 * best_score + 0.45 * max(0.0, best_score - second_score + 0.20)))
    return {"label": label, "confidence": confidence, "scores": scores, "source": "deterministic"}


def semantic_multi_label(
    texts: Iterable[Any],
    categories: Sequence[SemanticCategory],
    *,
    llm: ChatOpenAI | None = None,
    task_name: str,
    allow_empty: bool = True,
) -> dict[str, Any]:
    """``semantic_multi_label`` 函数。

    :param texts: 见函数签名与上下文。
    :param categories: 见函数签名与上下文。
    :param llm: 见函数签名与上下文。
    :param task_name: 见函数签名与上下文。
    :param allow_empty: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    prepared = _prepare_texts(texts)
    if not categories:
        return {"labels": [], "confidence": 0.0, "scores": {}, "source": "empty"}

    if llm is not None and prepared:
        payload = _invoke_llm_json(
            llm,
            [
                (
                    "system",
                    "You are a semantic classifier for an expert-review runtime. "
                    "Classify by meaning, not by surface keyword matching. "
                    "Use the provided category definitions and examples. "
                    "Return strict JSON only.",
                ),
                (
                    "user",
                    "Task name: "
                    + task_name
                    + "\n\nChoose zero or more labels from the categories below.\n"
                    + "Return JSON with keys: labels, confidence, rationale.\n\n"
                    + "Categories:\n"
                    + json.dumps([_category_payload(category) for category in categories], ensure_ascii=False, indent=2)
                    + "\n\nText fragments:\n"
                    + json.dumps(prepared, ensure_ascii=False, indent=2),
                ),
            ],
            operation=f"semantic_router:{task_name}",
        )
        if isinstance(payload, dict) and isinstance(payload.get("labels"), list):
            allowed = {category.name for category in categories}
            labels = [
                normalize_text(item)
                for item in payload.get("labels", [])
                if normalize_text(item) in allowed
            ]
            if labels or allow_empty:
                try:
                    confidence = max(0.0, min(1.0, float(payload.get("confidence", 0.75))))
                except Exception:
                    confidence = 0.75
                return {"labels": labels, "confidence": confidence, "scores": {}, "source": "llm"}

    scores = {category.name: _category_score(prepared, category) for category in categories}
    labels = [
        category.name
        for category in categories
        if scores.get(category.name, 0.0) >= category.threshold
    ]
    if not labels and not allow_empty and scores:
        labels = [max(scores.items(), key=lambda item: item[1])[0]]
    best_score = max(scores.values()) if scores else 0.0
    return {"labels": labels, "confidence": best_score, "scores": scores, "source": "deterministic"}


__all__ = [
    "SemanticCategory",
    "semantic_multi_label",
    "semantic_single_label",
]