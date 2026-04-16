from __future__ import annotations

from typing import Any

from ..expert_review_schema import EvidenceItem
from ..schemas.dossiers import ArtifactDossier, ArtifactElement, ArtifactRelation
from ..expert_review_utils import normalize_id
from .artifact_probe import merge_text_fragments
from .known_format_lift import dedupe_strings


def _make_evidence_item(source: str, locator: str | None, snippet: str, explanation: str) -> EvidenceItem:
    return EvidenceItem(
        source=source,
        locator=locator,
        snippet=snippet.strip(),
        explanation=explanation.strip(),
    )


def _element_merge_key(element: ArtifactElement) -> str:
    return normalize_id("|".join([element.kind, element.label or element.text]))


def _relation_merge_key(relation: ArtifactRelation) -> str:
    base = "|".join(
        [
            relation.source_label,
            relation.target_label,
            relation.trigger,
            relation.condition,
            relation.action,
        ]
    )
    if normalize_id(base):
        return normalize_id(base)
    return normalize_id(relation.description or relation.evidence_text)


def merge_artifact_dossiers(parser_dossier: ArtifactDossier, llm_payload: dict[str, Any]) -> ArtifactDossier:
    elements = list(parser_dossier.elements)
    relations = list(parser_dossier.relations)
    element_index = {_element_merge_key(item): idx for idx, item in enumerate(elements)}
    relation_index = {_relation_merge_key(item): idx for idx, item in enumerate(relations)}
    extraction_conflicts = list(parser_dossier.extraction_conflicts)
    for idx, item in enumerate(llm_payload.get("major_elements", []), start=1):
        if not isinstance(item, dict):
            continue
        label = str(item.get("label", "")).strip()
        text = str(item.get("text") or label).strip()
        if not label and not text:
            continue
        candidate = ArtifactElement(
            element_id=str(item.get("element_id") or f"{parser_dossier.role}_llm_element_{idx}"),
            kind=str(item.get("kind") or "element"),
            label=label or text,
            text=text,
            evidence_text=str(item.get("evidence_text") or text),
        )
        key = _element_merge_key(candidate)
        if key and key in element_index:
            existing = elements[element_index[key]]
            if candidate.kind != existing.kind:
                extraction_conflicts.append(
                    f"LLM retyped `{candidate.label or candidate.text}` from `{existing.kind}` to `{candidate.kind}`; kept parser kind."
                )
            existing.text = merge_text_fragments(existing.text, candidate.text)
            existing.evidence_text = merge_text_fragments(existing.evidence_text, candidate.evidence_text)
            continue
        element_index[key] = len(elements)
        elements.append(candidate)
    for idx, item in enumerate(llm_payload.get("major_relations", []), start=1):
        if not isinstance(item, dict):
            continue
        description = str(item.get("description", "")).strip()
        candidate = ArtifactRelation(
            relation_id=str(item.get("relation_id") or f"{parser_dossier.role}_llm_relation_{idx}"),
            kind=str(item.get("kind") or "relation"),
            source_label=str(item.get("source_label", "")).strip(),
            target_label=str(item.get("target_label", "")).strip(),
            trigger=str(item.get("trigger", "")).strip(),
            condition=str(item.get("condition", "")).strip(),
            action=str(item.get("action", "")).strip(),
            description=description or str(item.get("evidence_text", "")).strip(),
            evidence_text=str(item.get("evidence_text") or description),
        )
        key = _relation_merge_key(candidate)
        if key and key in relation_index:
            existing = relations[relation_index[key]]
            existing.description = merge_text_fragments(existing.description, candidate.description)
            existing.evidence_text = merge_text_fragments(existing.evidence_text, candidate.evidence_text)
            if candidate.condition and not existing.condition:
                existing.condition = candidate.condition
            if candidate.action and not existing.action:
                existing.action = candidate.action
            continue
        relation_index[key] = len(relations)
        relations.append(candidate)
    behaviors = dedupe_strings(parser_dossier.behaviors + [str(item) for item in llm_payload.get("behaviors", [])])
    constraints = dedupe_strings(
        parser_dossier.constraints + [str(item) for item in llm_payload.get("constraints", [])]
    )
    ambiguities = dedupe_strings(
        parser_dossier.ambiguities + [str(item) for item in llm_payload.get("ambiguities", [])]
    )
    evidence = list(parser_dossier.evidence)
    for idx, item in enumerate(llm_payload.get("major_elements", [])[:2], start=1):
        if not isinstance(item, dict):
            continue
        evidence.append(
            _make_evidence_item(
                parser_dossier.role,
                f"{parser_dossier.role}:llm_element:{idx}",
                snippet=str(item.get("evidence_text") or item.get("text") or item.get("label") or ""),
                explanation=f"LLM-extracted {parser_dossier.role} element summary.",
            )
        )
    for idx, item in enumerate(llm_payload.get("major_relations", [])[:2], start=1):
        if not isinstance(item, dict):
            continue
        evidence.append(
            _make_evidence_item(
                parser_dossier.role,
                f"{parser_dossier.role}:llm_relation:{idx}",
                snippet=str(item.get("evidence_text") or item.get("description") or ""),
                explanation=f"LLM-extracted {parser_dossier.role} relation summary.",
            )
        )
    summary = str(llm_payload.get("summary") or parser_dossier.summary).strip()
    artifact_family_guess_value = str(llm_payload.get("artifact_family_guess") or parser_dossier.artifact_family_guess)
    observability = str(llm_payload.get("observability") or parser_dossier.observability)
    observability_reason = str(llm_payload.get("observability_reason") or parser_dossier.observability_reason).strip()
    canonical_names = dedupe_strings(
        parser_dossier.canonical_names
        + [item.label for item in elements if item.label]
        + [relation.source_label for relation in relations if relation.source_label]
        + [relation.target_label for relation in relations if relation.target_label]
    )
    return ArtifactDossier(
        role=parser_dossier.role,
        format_guess=parser_dossier.format_guess,
        artifact_family_guess=artifact_family_guess_value,
        summary=summary,
        elements=elements[:40],
        relations=relations[:40],
        behaviors=behaviors[:20],
        constraints=constraints[:16],
        ambiguities=ambiguities[:10],
        evidence=evidence[:8],
        observability=observability,
        format_confidence=parser_dossier.format_confidence,
        observability_reason=observability_reason,
        analysis_mode="parser_plus_llm",
        surface_markers=dict(parser_dossier.surface_markers),
        structural_warnings=dedupe_strings(parser_dossier.structural_warnings),
        canonical_names=canonical_names[:40],
        extraction_conflicts=dedupe_strings(extraction_conflicts)[:12],
        parser_notes=list(parser_dossier.parser_notes),
    )


__all__ = ["merge_artifact_dossiers"]
