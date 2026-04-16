from __future__ import annotations

import re
from typing import Any

from ..schema import EvidenceItem
from ..utils import normalize_id


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
    return max(0.0, min(1.0, value))


def tokenize(value: str) -> list[str]:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)
    spaced = spaced.replace("_", " ").replace("-", " ")
    return [item.lower() for item in re.findall(r"[A-Za-z][A-Za-z0-9]*", spaced)]


def content_tokens(value: str) -> list[str]:
    return [item for item in tokenize(value) if len(item) >= 3 and item not in INPUT_STOPWORDS]


def _stem(token: str) -> str:
    clean = token.lower()
    for suffix in ("ing", "ed", "es", "s"):
        if len(clean) >= 6 and clean.endswith(suffix):
            clean = clean[: -len(suffix)]
            break
    return clean[:4] if len(clean) >= 4 else clean


def token_set(value: str) -> set[str]:
    return set(content_tokens(value))


def stem_set(value: str) -> set[str]:
    return {_stem(item) for item in content_tokens(value)}


def overlap_score(a: str, b: str) -> float:
    left = token_set(a)
    right = token_set(b)
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def stem_overlap_score(a: str, b: str) -> float:
    left = stem_set(a)
    right = stem_set(b)
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def combined_overlap_score(a: str, b: str) -> float:
    lexical = overlap_score(a, b)
    stemmed = stem_overlap_score(a, b)
    return max(lexical, min(1.0, 0.88 * stemmed + 0.12 * lexical))


def dedupe_strings(items: list[str]) -> list[str]:
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
    return EvidenceItem(
        source=source,
        locator=locator,
        snippet=snippet.strip(),
        explanation=explanation.strip(),
    )


def candidate_texts_from_dossier(dossier: Any) -> list[tuple[str, str, str]]:
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
    item_tokens = token_set(text)
    if not item_tokens:
        return False
    return len(item_tokens & grounding_tokens) >= 1 or len(stem_set(text) & {_stem(x) for x in grounding_tokens}) >= 2


def major_element_name_set(dossier: Any) -> set[str]:
    names: set[str] = set()
    for item in dossier.elements:
        names.add(normalize_id(item.label or item.text))
    return {item for item in names if item}


def initial_targets_from_behaviors(dossier: Any) -> list[str]:
    targets: list[str] = []
    for behavior in dossier.behaviors:
        match = re.match(r"\[\*\]\s*(?:-->|->)\s*([A-Za-z_][A-Za-z0-9_.-]*)", behavior.strip())
        if match:
            targets.append(match.group(1).strip())
    return dedupe_strings(targets)


def shared_source_target_map(dossier: Any) -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {}
    for relation in dossier.relations:
        source = normalize_id(relation.source_label)
        target = normalize_id(relation.target_label)
        if not source or not target:
            continue
        mapping.setdefault(source, []).append(target)
    return {key: dedupe_strings(value) for key, value in mapping.items()}


def infer_count_hint(text: str) -> int | None:
    lowered = text.lower()
    for word, value in NUMBER_HINTS.items():
        if re.search(rf"\b{word}\b", lowered):
            return value
    match = re.search(r"\b([2-6])\b", lowered)
    if match:
        return int(match.group(1))
    return None
