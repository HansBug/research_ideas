"""Agent 共享工具函数集合 —— tokenize / overlap / evidence 构造等。

**作用**：为 :mod:`agents/` 下的多个 agent 提供"轻业务但跨 agent 复用"
的纯函数工具，包括：

1. **token / 词法工具**：:func:`tokenize` / :func:`content_tokens` /
   :func:`_stem` / :func:`token_set` / :func:`stem_set` —— 把 NL
   文本切成可比较的 token / stem 集合；
2. **重叠度计算**：:func:`overlap_score` / :func:`stem_overlap_score` /
   :func:`combined_overlap_score` —— 三种粒度的 Jaccard-like
   overlap 得分，traceability / equivalence agent 都会用；
3. **去重 / 工具构造**：:func:`dedupe_strings` /
   :func:`make_evidence_item` / :func:`candidate_texts_from_dossier`；
4. **需求 grounding**：:func:`requirement_grounding_tokens` /
   :func:`relation_signature_tokens` /
   :func:`find_best_relation_overlap` / :func:`is_grounded_to_input`；
5. **结构推断**：:func:`major_element_name_set` /
   :func:`initial_targets_from_behaviors` /
   :func:`shared_source_target_map` / :func:`infer_count_hint`。

**设计思路**：

* **纯函数 + 无副作用**：所有 helper 都不写 state / 不调 LLM；
* **stopwords / number hints 内嵌常量**：``INPUT_STOPWORDS`` 与
  ``NUMBER_HINTS`` 是 W2 期间从实际数据集 token 频率人工挑选；不
  使用外部 NLP 词库；
* **多语言友好**：tokenize 时保留 CJK 等非 ASCII 字符；
  ``content_tokens`` 对非 ASCII token 直接放行不过滤。

**关键约束**：

* :func:`_stem` 是**简单 suffix-strip stemmer**，不是 PorterStemmer
  /Lancaster 等正统算法——优势是无依赖；劣势是对屈折变化覆盖弱；
* :func:`overlap_score` 等返回值 ∈ [0, 1]，可直接用作分数维度的
  原料（不需要再归一化）。
"""

from __future__ import annotations

import re
from typing import Any

from ..schema import EvidenceItem
from ..utils import normalize_id, semantic_terms, unicode_word_tokens


INPUT_STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "into",
    "when",
    "where",
    "which",
    "while",
    "then",
    "will",
    "have",
    "has",
    "are",
    "must",
    "should",
    "than",
    "less",
    "more",
    "also",
    "other",
    "about",
    "according",
    "system",
    "information",
    "model",
    "diagram",
    "state",
    "machine",
    "behavior",
    "review",
    "expert",
}

NUMBER_HINTS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
}


def clip01(value: float) -> float:
    """把任意浮点数夹到 [0, 1] 闭区间。

    :param value: 任意 float
    :return: ``max(0, min(1, value))``

    Examples::

        >>> clip01(1.5)
        1.0
        >>> clip01(-0.2)
        0.0
        >>> clip01(0.42)
        0.42
    """
    return max(0.0, min(1.0, value))


def tokenize(value: str) -> list[str]:
    """把字符串切成小写 token 列表（含 camelCase 拆分、连字符替换为空格）。

    :param value: 任意字符串
    :return: 小写 token 列表

    Examples::

        >>> tokenize("HumanDriving-mode")
        ['human', 'driving', 'mode']
        >>> tokenize("R1: 系统启动")
        ['r1', '系统启动']
    """
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)
    spaced = spaced.replace("-", " ")
    return [item.lower() for item in unicode_word_tokens(spaced)]


def content_tokens(value: str) -> list[str]:
    """从 :func:`tokenize` 结果中过滤掉 stopwords 与短 ASCII token。

    保留所有 CJK / 含非 ASCII 字符的 token；ASCII token 长度 < 3
    或在 ``INPUT_STOPWORDS`` 中将被丢弃。

    :param value: 任意字符串
    :return: 内容 token 列表（可能为空）

    Examples::

        >>> "the" in content_tokens("the system starts")
        False
        >>> "system" in content_tokens("the system starts")
        False
        >>> "starts" in content_tokens("the system starts")
        True
    """
    result: list[str] = []
    for item in tokenize(value):
        if any(ord(char) > 127 for char in item):
            result.append(item)
            continue
        if len(item) >= 3 and item not in INPUT_STOPWORDS:
            result.append(item)
    return result


def _stem(token: str) -> str:
    """简单后缀剥离 stemmer：剥离 ``ing/ed/es/s`` 并截断到前 4 字符。

    内部 helper；非正统 stemmer，仅用于 token 重叠对比。

    :param token: 小写 token
    :return: stem 字符串
    """
    clean = token.lower()
    for suffix in ("ing", "ed", "es", "s"):
        if len(clean) >= 6 and clean.endswith(suffix):
            clean = clean[: -len(suffix)]
            break
    return clean[:4] if len(clean) >= 4 else clean


def token_set(value: str) -> set[str]:
    """:func:`content_tokens` 与 :func:`utils.semantic_terms` 的并集。

    :param value: 任意字符串
    :return: token set
    """
    return set(content_tokens(value)) | semantic_terms(value)


def stem_set(value: str) -> set[str]:
    """把 :func:`content_tokens` 的结果逐项 :func:`_stem` 后取 set。

    :param value: 任意字符串
    :return: stem set
    """
    stems: set[str] = set()
    for item in content_tokens(value):
        if any(ord(char) > 127 for char in item):
            stems.add(item)
        else:
            stems.add(_stem(item))
    return stems


def overlap_score(a: str, b: str) -> float:
    """两段文本基于 :func:`token_set` 的 Jaccard overlap。

    :param a: 字符串 A
    :param b: 字符串 B
    :return: ∈ [0, 1]，任一 token_set 为空时返回 0.0

    Examples::

        >>> 0.0 <= overlap_score("system idle", "the idle state") <= 1.0
        True
        >>> overlap_score("", "anything")
        0.0
    """
    left = token_set(a)
    right = token_set(b)
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def stem_overlap_score(a: str, b: str) -> float:
    """两段文本基于 :func:`stem_set` 的 Jaccard overlap。

    :param a: 字符串 A
    :param b: 字符串 B
    :return: ∈ [0, 1]
    """
    left = stem_set(a)
    right = stem_set(b)
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def combined_overlap_score(a: str, b: str) -> float:
    """:func:`overlap_score` 与 :func:`stem_overlap_score` 加权综合。

    返回 ``max(lexical, min(1, 0.88·stemmed + 0.12·lexical))`` ——保证
    无论 stem 相同还是 lexical 相同都能给出合理分数。

    :param a: 字符串 A
    :param b: 字符串 B
    :return: ∈ [0, 1]
    """
    lexical = overlap_score(a, b)
    stemmed = stem_overlap_score(a, b)
    return max(lexical, min(1.0, 0.88 * stemmed + 0.12 * lexical))


def dedupe_strings(items: list[str]) -> list[str]:
    """按 normalize_id 去重，保留首次出现的原文。

    :param items: 字符串列表
    :return: 去重后的字符串列表（顺序保持）

    Examples::

        >>> dedupe_strings(["A", "a", "B", " A "])
        ['A', 'B']
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


def make_evidence_item(source: str, locator: str | None, snippet: str, explanation: str) -> EvidenceItem:
    """构造一条规范化的 :class:`EvidenceItem`（snippet/explanation 自动 strip）。

    :param source: evidence 来源
    :param locator: 可选定位标识
    :param snippet: 原文片段
    :param explanation: 解释文本
    :return: :class:`EvidenceItem`
    """
    return EvidenceItem(
        source=source,
        locator=locator,
        snippet=snippet.strip(),
        explanation=explanation.strip(),
    )


def candidate_texts_from_dossier(dossier: Any) -> list[tuple[str, str, str]]:
    """把 :class:`ArtifactDossier` 中的 elements/relations/behaviors/constraints
    展平为 ``(id, kind, joined_text)`` 三元组列表。

    用于让 traceability / equivalence agent 拿到一个 "可逐条与需求对比"
    的统一候选列表。

    :param dossier: :class:`ArtifactDossier`
    :return: 三元组列表
    """
    candidates: list[tuple[str, str, str]] = []
    for item in dossier.elements:
        candidates.append((item.element_id, item.kind, " ".join([item.label, item.text, item.evidence_text]).strip()))
    for relation in dossier.relations:
        candidates.append(
            (
                relation.relation_id,
                relation.kind,
                " ".join(
                    [
                        relation.source_label,
                        relation.target_label,
                        relation.trigger,
                        relation.condition,
                        relation.action,
                        relation.description,
                        relation.evidence_text,
                    ]
                ).strip(),
            )
        )
    for idx, item in enumerate(dossier.behaviors, start=1):
        candidates.append((f"{dossier.role}_behavior_{idx}", "behavior", item))
    for idx, item in enumerate(dossier.constraints, start=1):
        candidates.append((f"{dossier.role}_constraint_{idx}", "constraint", item))
    return candidates


def requirement_grounding_tokens(input_dossier: Any) -> set[str]:
    """把 :class:`InputDossier` 中所有可作为 grounding 的文本汇总到一个 token set。

    汇总来源：requirements / behaviors / constraints / entity_hints
    四类字段。该 token set 通常作为 :func:`is_grounded_to_input` 的
    第二参数使用。

    :param input_dossier: :class:`InputDossier`
    :return: 合并后的 grounding token set
    """
    tokens: set[str] = set()
    for item in input_dossier.requirements:
        tokens.update(token_set(item.requirement_text))
    for item in input_dossier.behaviors:
        tokens.update(token_set(item))
    for item in input_dossier.constraints:
        tokens.update(token_set(item))
    for item in input_dossier.entity_hints:
        tokens.update(token_set(item))
    return tokens


def relation_signature_tokens(relation: Any) -> set[str]:
    """把一条 :class:`ArtifactRelation` 的所有文本字段拼起来取 token_set。

    :param relation: :class:`ArtifactRelation`
    :return: token set
    """
    return token_set(
        " ".join(
            [
                relation.source_label,
                relation.target_label,
                relation.trigger,
                relation.condition,
                relation.action,
                relation.description,
            ]
        )
    )


def find_best_relation_overlap(source: Any, targets: list[Any]) -> float:
    """在多个 target relation 中找到与 source 重叠度最高的 token Jaccard。

    :param source: 单条 :class:`ArtifactRelation`
    :param targets: target relation 列表
    :return: 最高 Jaccard 分 ∈ [0, 1]
    """
    source_tokens = relation_signature_tokens(source)
    if not source_tokens:
        return 0.0
    best = 0.0
    for target in targets:
        target_tokens = relation_signature_tokens(target)
        if not target_tokens:
            continue
        score = len(source_tokens & target_tokens) / len(source_tokens | target_tokens)
        best = max(best, score)
    return best


def is_grounded_to_input(text: str, grounding_tokens: set[str]) -> bool:
    """判断一段文本是否被 NL 需求 token 集合"接住"（grounded）。

    判定准则：``token_set(text) ∩ grounding_tokens >= 1`` 或者
    ``stem_set(text) ∩ stemmed_grounding >= 2``。

    :param text: 待判定文本
    :param grounding_tokens: 需求侧 grounding token 集合
        （通常来自 :func:`requirement_grounding_tokens`）
    :return: 是否 grounded
    """
    item_tokens = token_set(text)
    if not item_tokens:
        return False
    return len(item_tokens & grounding_tokens) >= 1 or len(stem_set(text) & {_stem(x) for x in grounding_tokens}) >= 2


def major_element_name_set(dossier: Any) -> set[str]:
    """从 dossier 提取所有主要 element 的 normalized name 集合。

    :param dossier: :class:`ArtifactDossier`
    :return: normalized 名称集合
    """
    names: set[str] = set()
    for item in dossier.elements:
        names.add(normalize_id(item.label or item.text))
    return {item for item in names if item}


def initial_targets_from_behaviors(dossier: Any) -> list[str]:
    """从 dossier.behaviors 中按 ``[*] --> X`` 模式抽取初始 target 名列表。

    :param dossier: :class:`ArtifactDossier`
    :return: 初始 target 名列表（已去重）
    """
    targets: list[str] = []
    for behavior in dossier.behaviors:
        match = re.match(r"\[\*\]\s*(?:-->|->)\s*([A-Za-z_][A-Za-z0-9_.-]*)", behavior.strip())
        if match:
            targets.append(match.group(1).strip())
    return dedupe_strings(targets)


def shared_source_target_map(dossier: Any) -> dict[str, list[str]]:
    """构造 ``{source_label: [target_labels]}`` 邻接字典。

    :param dossier: :class:`ArtifactDossier`
    :return: source → target list 映射（target 已去重）
    """
    mapping: dict[str, list[str]] = {}
    for relation in dossier.relations:
        source = normalize_id(relation.source_label)
        target = normalize_id(relation.target_label)
        if not source or not target:
            continue
        mapping.setdefault(source, []).append(target)
    return {key: dedupe_strings(value) for key, value in mapping.items()}


def infer_count_hint(text: str) -> int | None:
    """从文本中推断"应有的状态/事件数量"提示。

    优先匹配 NUMBER_HINTS 词（"two" / "three" / ...）；
    否则匹配 ASCII 数字 2-6。

    :param text: NL 文本
    :return: 整数提示 ∈ {2, 3, 4, 5, 6} 或 ``None``

    Examples::

        >>> infer_count_hint("there should be three states")
        3
        >>> infer_count_hint("4 transitions are needed")
        4
        >>> infer_count_hint("no number here") is None
        True
    """
    lowered = text.lower()
    for word, value in NUMBER_HINTS.items():
        if re.search(rf"\b{word}\b", lowered):
            return value
    match = re.search(r"\b([2-6])\b", lowered)
    if match:
        return int(match.group(1))
    return None
