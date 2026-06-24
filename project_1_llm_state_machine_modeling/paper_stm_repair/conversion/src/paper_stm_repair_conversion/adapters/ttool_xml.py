from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

from ..models import ConversionResult, Loss, State, Transition

STATE_COMPONENT_TYPES = {"5106"}
START_COMPONENT_TYPES = {"5100"}
TRANSITION_CONNECTOR_TYPES = {"5102"}


def _infoparam(element: ET.Element, name: str) -> str | None:
    for child in element.iter("infoparam"):
        if child.attrib.get("name") == name:
            return child.attrib.get("value")
    return None


def _component_ref(component: ET.Element, panel_name: str) -> str:
    return f"panel={panel_name};component_id={component.attrib.get('id')}"


def convert_ttool_xml(path: Path, *, example_id: str, seed_id: str, source_format: str = "ttool_xml") -> ConversionResult:
    result = ConversionResult(
        example_id=example_id,
        seed_id=seed_id,
        source_format=source_format,
        adapter="ttool_xml",
        status="partial",
        canonical_model_name=example_id,
        timing_level="timed_constraints",
        hierarchy_level="concurrent",
    )
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        result.status = "blocked"
        result.blocking_reason = f"TTool XML is not well-formed: {exc}"
        result.losses.append(
            Loss(
                loss_id=f"{example_id}:ttool_xml:parse_error",
                example_id=example_id,
                source_ref=path.name,
                canonical_ref=None,
                loss_type="syntax",
                severity="blocking",
                rationale=result.blocking_reason,
                needs_manual_review=True,
            )
        )
        return result

    result.metadata["xml_root"] = root.tag
    result.metadata["ttool_version"] = root.attrib.get("version")
    result.metadata["consider_timing_operators"] = root.attrib.get("considerTimingOperators")

    state_count = 0
    transition_count = 0
    panels = root.findall(".//AVATARStateMachineDiagramPanel")
    result.metadata["avatar_smd_panel_count"] = len(panels)
    for panel in panels:
        panel_name = panel.attrib.get("name") or "unnamed_panel"
        panel_id = f"panel::{panel_name}"
        if panel_id not in {s.id for s in result.states}:
            result.states.append(State(id=panel_id, label=panel_name, kind="composite", raw_ref=f"{path.name}:{panel_name}"))
        for component in panel.findall("COMPONENT"):
            typ = component.attrib.get("type")
            comp_id = component.attrib.get("id") or f"unknown_{state_count}"
            if typ in STATE_COMPONENT_TYPES:
                label = _infoparam(component, "state") or f"state_{comp_id}"
                sid = f"{panel_name}.{label}#{comp_id}"
                state_count += 1
                result.states.append(
                    State(
                        id=sid,
                        label=label,
                        kind="state",
                        parent=panel_id,
                        raw_ref=_component_ref(component, panel_name),
                        attributes={"ttool_component_type": typ, "component_id": comp_id},
                    )
                )
            elif typ in START_COMPONENT_TYPES:
                sid = f"{panel_name}.initial#{comp_id}"
                state_count += 1
                result.states.append(
                    State(
                        id=sid,
                        label="initial",
                        kind="initial",
                        parent=panel_id,
                        raw_ref=_component_ref(component, panel_name),
                        attributes={"ttool_component_type": typ, "component_id": comp_id},
                    )
                )
                result.initial_states.append(sid)
        for connector in panel.findall("CONNECTOR"):
            if connector.attrib.get("type") not in TRANSITION_CONNECTOR_TYPES:
                continue
            transition_count += 1
            p1 = connector.find("P1")
            p2 = connector.find("P2")
            sub = None
            # The transition parameters live in sibling SUBCOMPONENT elements with father id=connector id.
            conn_id = connector.attrib.get("id")
            for maybe_sub in panel.findall("SUBCOMPONENT"):
                father = maybe_sub.find("father")
                if father is not None and father.attrib.get("id") == conn_id:
                    sub = maybe_sub
                    break
            attrs = {
                "connector_id": conn_id,
                "ttool_connector_type": connector.attrib.get("type"),
                "p1_component_point_id": p1.attrib.get("id") if p1 is not None else None,
                "p2_component_point_id": p2.attrib.get("id") if p2 is not None else None,
            }
            if sub is not None:
                extra = sub.find("extraparam")
                if extra is not None:
                    for child in list(extra):
                        attrs[child.tag] = dict(child.attrib)
            result.transitions.append(
                Transition(
                    id=f"tr_{transition_count:04d}",
                    source=f"unresolved::{attrs['p1_component_point_id']}",
                    target=f"unresolved::{attrs['p2_component_point_id']}",
                    label=None,
                    scope=panel_id,
                    raw_ref=f"panel={panel_name};connector_id={conn_id}",
                    attributes=attrs,
                )
            )

    result.metadata["extracted_state_component_count"] = state_count
    result.metadata["extracted_transition_connector_count"] = transition_count
    result.metadata["resolved_states_count"] = 0
    result.metadata["resolved_transitions_count"] = 0
    result.blocking_reason = (
        "TTool XML adapter performs XML/SMD inventory only: it extracts AVATAR SMD panels, state/start components "
        "and transition connector records, but does not yet resolve graphical connecting points to exact source/target states "
        "or slice a pure T0 state machine from the full SysML/AVATAR artifact."
    )
    result.losses.append(
        Loss(
            loss_id=f"{example_id}:ttool_xml:unresolved_connectors",
            example_id=example_id,
            source_ref=path.name,
            canonical_ref=None,
            loss_type="structure",
            severity="high",
            rationale="Transition connectors retain P1/P2 graphical IDs, but R3 v0 does not resolve them to exact state component endpoints.",
            needs_manual_review=True,
        )
    )
    result.losses.append(
        Loss(
            loss_id=f"{example_id}:ttool_xml:timed_avatar_semantics",
            example_id=example_id,
            source_ref=path.name,
            canonical_ref=None,
            loss_type="timing",
            severity="medium",
            rationale="TTool/AVATAR timing fields and system-level timing requirements are inventoried but not interpreted as T0 semantics.",
            needs_manual_review=True,
        )
    )
    if state_count == 0:
        result.status = "blocked"
        result.blocking_reason = "TTool XML was well-formed but no AVATAR SMD state component could be extracted."
        result.losses.append(
            Loss(
                loss_id=f"{example_id}:ttool_xml:no_states",
                example_id=example_id,
                source_ref=path.name,
                canonical_ref=None,
                loss_type="structure",
                severity="blocking",
                rationale=result.blocking_reason,
                needs_manual_review=True,
            )
        )
    return result
