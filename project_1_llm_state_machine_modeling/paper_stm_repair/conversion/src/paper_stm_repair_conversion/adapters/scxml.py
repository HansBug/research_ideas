from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..models import ConversionResult, Loss, State, Transition


@dataclass(frozen=True)
class ScxmlOptions:
    adapter: str
    source_format: str
    conversion_source: str = "official_scxml"
    canonical_extraction_method: str = "xml.etree.ElementTree over official SCXML export"
    status_on_success: str = "converted"
    fallback_used: bool = False
    fallback_scope: str | None = None
    timing_level: str = "none"
    source_language: str | None = None


def _local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    return tag


def _children(element: ET.Element, name: str | None = None) -> list[ET.Element]:
    out = []
    for child in list(element):
        if name is None or _local_name(child.tag) == name:
            out.append(child)
    return out


def _xpath_ref(path: Path, parts: list[str]) -> str:
    return f"{path.name}:" + "/".join(parts)


def _state_kind(element: ET.Element, *, is_initial: bool = False, is_final: bool = False) -> str:
    tag = _local_name(element.tag)
    if is_initial or tag == "initial":
        return "initial"
    if is_final or tag == "final":
        return "final"
    if tag in {"parallel"}:
        return "composite"
    if _children(element, "state") or _children(element, "parallel") or _children(element, "initial"):
        return "composite"
    return "state"


def _transition_text(transition: ET.Element) -> str | None:
    scripts: list[str] = []
    for child in transition.iter():
        if _local_name(child.tag) == "script" and child.text and child.text.strip():
            scripts.append(child.text.strip())
    return "\n".join(scripts) if scripts else None


def convert_scxml(
    scxml_path: Path,
    *,
    example_id: str,
    seed_id: str,
    options: ScxmlOptions,
    structured_export_relpath: str | None = None,
    structured_export_sha256: str | None = None,
) -> ConversionResult:
    result = ConversionResult(
        example_id=example_id,
        seed_id=seed_id,
        source_format=options.source_format,
        adapter=options.adapter,
        status=options.status_on_success,
        canonical_model_name=example_id,
        timing_level=options.timing_level,
        hierarchy_level="flat",
    )
    result.metadata.update(
        {
            "conversion_source": options.conversion_source,
            "canonical_extraction_method": options.canonical_extraction_method,
            "structured_export_path": structured_export_relpath or str(scxml_path),
            "structured_export_sha256": structured_export_sha256,
            "fallback_used": options.fallback_used,
            "fallback_scope": options.fallback_scope,
            "source_language": options.source_language,
        }
    )
    try:
        raw_scxml_text = scxml_path.read_text(encoding="utf-8")
        # Some mature tools, notably Umple, may prepend comments before the XML declaration.
        # ElementTree requires the XML declaration to be at the beginning of the entity, so
        # we strip leading comments/whitespace only in memory while preserving the persisted
        # official SCXML file as the auditable source artifact.
        parse_text = re.sub(r"\A(?:\s*<!--.*?-->\s*)+", "", raw_scxml_text, flags=re.DOTALL)
        root = ET.fromstring(parse_text)
    except ET.ParseError as exc:
        result.status = "blocked"
        result.blocking_reason = f"Official SCXML export is not well-formed: {exc}"
        result.losses.append(
            Loss(
                loss_id=f"{example_id}:{options.adapter}:official_scxml_parse_error",
                example_id=example_id,
                source_ref=str(scxml_path),
                canonical_ref=None,
                loss_type="syntax",
                severity="blocking",
                rationale=result.blocking_reason,
                needs_manual_review=True,
            )
        )
        return result

    result.metadata["scxml_root"] = _local_name(root.tag)
    result.metadata["scxml_name"] = root.attrib.get("name")
    result.metadata["scxml_initial_attr"] = root.attrib.get("initial")
    state_ids: set[str] = set()
    transition_count = 0

    def add_state(element: ET.Element, parent: str | None, parts: list[str], *, forced_id: str | None = None, forced_kind: str | None = None) -> str:
        sid = forced_id or element.attrib.get("id") or element.attrib.get("name") or f"anon_{len(state_ids) + 1:04d}"
        kind = forced_kind or _state_kind(element)
        raw_ref = _xpath_ref(scxml_path, parts)
        if sid not in state_ids:
            result.states.append(
                State(
                    id=sid,
                    label=sid,
                    kind=kind,
                    parent=parent,
                    raw_ref=raw_ref,
                    attributes={
                        "source_node": _local_name(element.tag),
                        "conversion_source": options.conversion_source,
                        "source_attributes": dict(element.attrib),
                    },
                )
            )
            state_ids.add(sid)
        return sid

    def walk_state(element: ET.Element, parent: str | None, parts: list[str]) -> None:
        nonlocal transition_count
        sid = add_state(element, parent, parts)
        initial_attr = element.attrib.get("initial")
        if initial_attr and initial_attr not in result.initial_states:
            result.initial_states.append(initial_attr)
        for index, transition in enumerate(_children(element, "transition"), start=1):
            target = transition.attrib.get("target") or ""
            event = transition.attrib.get("event")
            guard = transition.attrib.get("cond")
            action = _transition_text(transition)
            label_parts = []
            if event:
                label_parts.append(event)
            if guard:
                label_parts.append(f"[{guard}]")
            if action:
                label_parts.append(f"/ {action}")
            transition_count += 1
            raw_ref = _xpath_ref(scxml_path, [*parts, f"transition[{index}]"])
            result.transitions.append(
                Transition(
                    id=f"tr_{transition_count:04d}",
                    source=sid,
                    target=target,
                    event=event,
                    guard=guard,
                    action=action,
                    label=" ".join(label_parts) or None,
                    scope=parent,
                    raw_ref=raw_ref,
                    attributes={
                        "conversion_source": options.conversion_source,
                        "source_attributes": dict(transition.attrib),
                        "source_node": "transition",
                    },
                )
            )
        for index, initial in enumerate(_children(element, "initial"), start=1):
            init_id = initial.attrib.get("id") or f"{sid}.__initial_{index}"
            add_state(initial, sid, [*parts, f"initial[{index}]"], forced_id=init_id, forced_kind="initial")
            if init_id not in result.initial_states:
                result.initial_states.append(init_id)
            for t_index, transition in enumerate(_children(initial, "transition"), start=1):
                target = transition.attrib.get("target") or ""
                transition_count += 1
                result.transitions.append(
                    Transition(
                        id=f"tr_{transition_count:04d}",
                        source=init_id,
                        target=target,
                        event=transition.attrib.get("event"),
                        guard=transition.attrib.get("cond"),
                        action=_transition_text(transition),
                        label=transition.attrib.get("event"),
                        scope=sid,
                        raw_ref=_xpath_ref(scxml_path, [*parts, f"initial[{index}]", f"transition[{t_index}]"]),
                        attributes={
                            "conversion_source": options.conversion_source,
                            "source_attributes": dict(transition.attrib),
                            "source_node": "transition",
                        },
                    )
                )
        for index, child in enumerate(_children(element), start=1):
            if _local_name(child.tag) in {"state", "parallel", "final"}:
                walk_state(child, sid, [*parts, f"{_local_name(child.tag)}[{index}]"])

    for index, child in enumerate(_children(root), start=1):
        if _local_name(child.tag) in {"state", "parallel", "final"}:
            walk_state(child, None, [f"scxml/{_local_name(child.tag)}[{index}]"])

    root_initial = root.attrib.get("initial")
    if root_initial and root_initial not in result.initial_states:
        result.initial_states.insert(0, root_initial)
    result.final_states = [s.id for s in result.states if s.kind == "final"]
    result.hierarchy_level = "hierarchical" if any(s.parent for s in result.states) else "flat"
    if not result.states or not result.transitions:
        result.status = "blocked"
        result.blocking_reason = "Official SCXML parsed but did not contain extractable states/transitions."
        result.losses.append(
            Loss(
                loss_id=f"{example_id}:{options.adapter}:official_scxml_empty",
                example_id=example_id,
                source_ref=structured_export_relpath or str(scxml_path),
                canonical_ref=None,
                loss_type="structure",
                severity="blocking",
                rationale=result.blocking_reason,
                needs_manual_review=True,
            )
        )
    result.diagnostics.append(
        {
            "code": "R3.STRUCTURED_EXPORT.CANONICAL_FROM_SCXML",
            "severity": "info",
            "structured_export_path": structured_export_relpath or str(scxml_path),
            "message": "Canonical states/transitions were extracted from official SCXML structured export, not from regex over source text.",
        }
    )
    return result
