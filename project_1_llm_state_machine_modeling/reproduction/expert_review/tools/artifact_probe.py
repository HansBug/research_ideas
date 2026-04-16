from __future__ import annotations

import re

from ..expert_review_schema import EvidenceItem
from ..schemas.dossiers import ArtifactDossier, ArtifactElement, ArtifactRelation
from .known_format_lift import (
    artifact_family_guess,
    dedupe_strings,
    inventory_from_text,
    parse_transition_signature,
    summary_from_inventory,
)


def _make_evidence_item(source: str, locator: str | None, snippet: str, explanation: str) -> EvidenceItem:
    return EvidenceItem(
        source=source,
        locator=locator,
        snippet=snippet.strip(),
        explanation=explanation.strip(),
    )


def _element_from_raw(kind: str, raw_value: str, idx: int, role: str) -> ArtifactElement:
    label = raw_value.split("|", 1)[0].strip()
    cleaned = raw_value.strip()
    if kind == "state":
        state_match = re.match(r"state\s+([A-Za-z_][A-Za-z0-9_.-]*)", cleaned)
        if state_match:
            label = state_match.group(1).strip()
    elif kind in {"block", "component"}:
        block_match = re.match(r"(?:block|component)\s+([A-Za-z_][A-Za-z0-9_.-]*)", cleaned, re.I)
        if block_match:
            label = block_match.group(1).strip()
    element_id = f"{role}_{kind}_{idx}"
    return ArtifactElement(
        element_id=element_id,
        kind=kind,
        label=label or cleaned,
        text=cleaned,
        evidence_text=cleaned,
    )


def _relation_from_raw(raw_value: str, idx: int, role: str) -> ArtifactRelation:
    source, target, trigger, condition, action = parse_transition_signature(raw_value)
    description = raw_value.strip()
    if source or target:
        description = f"{source} -> {target}".strip()
        if trigger:
            description += f" on {trigger}"
        if condition:
            description += f" if {condition}"
        if action:
            description += f" do {action}"
    return ArtifactRelation(
        relation_id=f"{role}_relation_{idx}",
        kind="relation",
        source_label=source,
        target_label=target,
        trigger=trigger,
        condition=condition,
        action=action,
        description=description,
        evidence_text=raw_value.strip(),
    )


def _element_merge_key(element: ArtifactElement) -> str:
    return re.sub(r"\s+", "", "|".join([element.kind.lower(), (element.label or element.text).lower()]))


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
    clean = re.sub(r"\s+", "", base.lower())
    if clean:
        return clean
    return re.sub(r"\s+", "", (relation.description or relation.evidence_text).lower())


def _same_relation_family(left: ArtifactRelation, right: ArtifactRelation) -> bool:
    left_pair = re.sub(r"\s+", "", "|".join([left.source_label, left.target_label]).lower())
    right_pair = re.sub(r"\s+", "", "|".join([right.source_label, right.target_label]).lower())
    if left_pair and right_pair and left_pair != right_pair:
        return False
    if left_pair != right_pair and (left_pair or right_pair):
        return False
    if left.trigger and right.trigger and left.trigger.lower().strip() != right.trigger.lower().strip():
        return False
    if left_pair and right_pair:
        return True
    return (left.description or left.evidence_text).lower().strip() == (right.description or right.evidence_text).lower().strip()


def merge_text_fragments(first: str, second: str) -> str:
    left = first.strip()
    right = second.strip()
    if not left:
        return right
    if not right or left.lower() == right.lower():
        return left
    if right.lower() in left.lower():
        return left
    if left.lower() in right.lower():
        return right
    return f"{left} | {right}"


def build_parser_dossier(role: str, text: str | None) -> ArtifactDossier:
    probe = inventory_from_text(text)
    inventory = probe["inventory"]
    elements: list[ArtifactElement] = []
    relations: list[ArtifactRelation] = []
    element_index: dict[str, int] = {}
    relation_index: dict[str, int] = {}
    for kind in ["states", "blocks", "signals", "rules"]:
        singular = kind[:-1] if kind.endswith("s") else kind
        for idx, raw_value in enumerate(inventory.get(kind, []), start=1):
            candidate = _element_from_raw(singular, raw_value, idx, role)
            key = _element_merge_key(candidate)
            if key in element_index:
                existing = elements[element_index[key]]
                existing.text = merge_text_fragments(existing.text, candidate.text)
                existing.evidence_text = merge_text_fragments(existing.evidence_text, candidate.evidence_text)
                continue
            element_index[key] = len(elements)
            elements.append(candidate)
    for idx, raw_value in enumerate(inventory.get("transitions", []), start=1):
        if "[*]" in raw_value:
            continue
        candidate = _relation_from_raw(raw_value, idx, role)
        key = _relation_merge_key(candidate)
        if key in relation_index:
            existing = relations[relation_index[key]]
            existing.description = merge_text_fragments(existing.description, candidate.description)
            existing.evidence_text = merge_text_fragments(existing.evidence_text, candidate.evidence_text)
            continue
        merged = False
        for existing_idx, existing in enumerate(relations):
            if _same_relation_family(existing, candidate) and (not existing.trigger or not candidate.trigger):
                if candidate.trigger and not existing.trigger:
                    existing.trigger = candidate.trigger
                if candidate.condition and not existing.condition:
                    existing.condition = candidate.condition
                if candidate.action and not existing.action:
                    existing.action = candidate.action
                existing.description = merge_text_fragments(existing.description, candidate.description)
                existing.evidence_text = merge_text_fragments(existing.evidence_text, candidate.evidence_text)
                relation_index[_relation_merge_key(existing)] = existing_idx
                merged = True
                break
        if merged:
            continue
        relation_index[key] = len(relations)
        relations.append(candidate)
    evidence: list[EvidenceItem] = []
    for idx, raw_value in enumerate(inventory.get("transitions", [])[:3], start=1):
        evidence.append(
            _make_evidence_item(
                role,
                f"{role}:relation:{idx}",
                raw_value,
                f"Observed {role} relation from direct parser/probe extraction.",
            )
        )
    for idx, raw_value in enumerate((inventory.get("states", []) + inventory.get("blocks", []) + inventory.get("signals", []))[:3], start=1):
        evidence.append(
            _make_evidence_item(
                role,
                f"{role}:element:{idx}",
                raw_value,
                f"Observed {role} element from direct parser/probe extraction.",
            )
        )
    return ArtifactDossier(
        role=role,
        format_guess=probe["format_guess"],
        artifact_family_guess=artifact_family_guess(inventory, text),
        summary=summary_from_inventory(
            role,
            inventory,
            probe["format_guess"],
            probe["observability"],
            probe["observability_reason"],
        ),
        elements=elements,
        relations=relations,
        behaviors=probe["behaviors"][:16],
        constraints=probe["constraints"][:12],
        ambiguities=probe["ambiguities"][:10],
        evidence=evidence[:6],
        observability=probe["observability"],
        format_confidence=float(probe["format_confidence"]),
        observability_reason=probe["observability_reason"],
        analysis_mode="parser_only",
        surface_markers=dict(probe["surface_markers"]),
        structural_warnings=list(probe["structural_warnings"]),
        canonical_names=list(probe["canonical_names"]),
        extraction_conflicts=[],
        parser_notes=list(probe["parser_notes"]),
    )


__all__ = ["build_parser_dossier", "merge_text_fragments"]
