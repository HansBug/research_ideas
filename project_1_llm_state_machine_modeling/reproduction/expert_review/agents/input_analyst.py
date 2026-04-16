from __future__ import annotations

import re

from ..schema import EvidenceItem, RequirementTraceResult
from ..inventory import parse_requirement_items
from ..schemas.dossiers import InputDossier
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


def _make_evidence_item(source: str, locator: str | None, snippet: str, explanation: str) -> EvidenceItem:
    return EvidenceItem(
        source=source,
        locator=locator,
        snippet=snippet.strip(),
        explanation=explanation.strip(),
    )


def _content_tokens(value: str) -> list[str]:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)
    spaced = spaced.replace("_", " ").replace("-", " ")
    return [
        item.lower()
        for item in re.findall(r"[A-Za-z][A-Za-z0-9]*", spaced)
        if len(item) >= 3 and item.lower() not in INPUT_STOPWORDS
    ]


def _dedupe_strings(items: list[str]) -> list[str]:
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
    lowered = request.prompt.lower()
    if "equivalent" in lowered or "等效" in request.prompt:
        clues.append("Prompt explicitly allows semantic equivalence beyond structural isomorphism.")
    if "hallucination" in lowered or "额外" in request.prompt:
        clues.append("Prompt explicitly asks to inspect unsupported extra structure.")
    behaviors = _dedupe_strings(requirement_texts)
    constraints = _dedupe_strings(
        [
            text
            for text in requirement_texts
            if any(
                token in text.lower()
                for token in [" if ", " when ", " only ", " must ", " cannot ", " not ", "<", ">", "within", "every"]
            )
        ]
    )
    ambiguities = _dedupe_strings(
        [
            text
            for text in requirement_texts
            if any(token in text.lower() for token in ["possible", "may ", "maybe", "roughly", "and/or", "etc"])
        ]
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
            for token in _content_tokens(text)
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
