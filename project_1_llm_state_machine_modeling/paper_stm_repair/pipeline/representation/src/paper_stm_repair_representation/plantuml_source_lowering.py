from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Optional

from .pyfcstm_names import NameRegistry


def _dsl_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _scope_key(scope: Optional[str]) -> str:
    return scope or "__root__"


def _action_identifier_source(text: str) -> str:
    parts = [part for part in re.split(r"[^A-Za-z0-9]+", text) if part]
    return "".join(part[:1].upper() + part[1:] for part in parts) or "Action"


@dataclass
class _Mapping:
    transition_id: str
    status: str
    reason_code: str
    source: str
    target: str
    raw_ref: Optional[str]
    emitted: list[dict[str, Any]] = field(default_factory=list)


class _Lowerer:
    def __init__(self, canonical: dict[str, Any]) -> None:
        self.canonical = canonical
        self.model = canonical["model"]
        self.states = list(self.model["states"])
        self.transitions = list(self.model["transitions"])
        self.state_by_id = {state["id"]: state for state in self.states}
        self.transition_by_id = {
            transition["id"]: transition for transition in self.transitions
        }
        self.parent = {state["id"]: state.get("parent") for state in self.states}
        self.children: dict[Optional[str], list[str]] = defaultdict(list)
        for state in self.states:
            self.children[state.get("parent")].append(state["id"])
        self.registry = NameRegistry()
        self.root_id = self.registry.reserve(
            raw_text=canonical["example_id"],
            canonical_ref=f"canonical:{canonical['example_id']}",
            object_type="root_state",
            scope="",
            generated_reason="example_id",
        )
        self.emitted_state: dict[str, str] = {}
        self.events: dict[str, str] = {}
        self.lines_by_scope: dict[Optional[str], list[str]] = defaultdict(list)
        self.synthetic_states_by_scope: dict[Optional[str], list[str]] = defaultdict(list)
        self.mappings: list[_Mapping] = []
        self.blockers: list[dict[str, Any]] = []
        self.operational_debts: list[dict[str, Any]] = []
        self.state_mappings: list[dict[str, Any]] = []
        self.synthetic_state_mappings: list[dict[str, Any]] = []
        self.synthetic_transition_mappings: list[dict[str, Any]] = []
        self.priority_entry_count_by_scope: dict[Optional[str], int] = defaultdict(int)
        self.event_mappings: list[dict[str, Any]] = []
        self.body_mappings: list[dict[str, Any]] = []
        self.lifecycle_mappings: list[dict[str, Any]] = []
        self.orphan_lifecycle_mappings: list[dict[str, Any]] = []
        self.initial_by_scope: dict[Optional[str], list[dict[str, Any]]] = defaultdict(list)
        self.mapped_initial_scopes: set[Optional[str]] = set()
        self.lifecycle_source_count = 0
        self.lifecycle_mapped_count = 0
        self.final_source_count = 0
        self.final_mapped_count = 0

    def add_operational_debt(self, reason_code: str, message: str, **details: Any) -> None:
        self.operational_debts.append(
            {
                "reason_code": reason_code,
                "message": message,
                **details,
            }
        )

    def emitted_path(self, state_id: str) -> str:
        return ".".join(
            [self.root_id]
            + [self.emitted_state[item] for item in self.state_chain(state_id)]
        )

    def record_synthetic_state(
        self,
        *,
        scope: Optional[str],
        emitted_id: str,
        display_name: str,
        generated_reason: str,
        raw_ref: Optional[str],
        source_transition_id: Optional[str] = None,
    ) -> None:
        scope_path = self.root_id if scope is None else self.emitted_path(scope)
        self.synthetic_state_mappings.append(
            {
                "fcstm_id": emitted_id,
                "fcstm_parent_path": scope_path,
                "fcstm_path": f"{scope_path}.{emitted_id}",
                "display_name": display_name,
                "generated_reason": generated_reason,
                "raw_ref": raw_ref,
                "source_transition_id": source_transition_id,
            }
        )

    def record_synthetic_transition(
        self,
        *,
        scope: Optional[str],
        line: str,
        generated_reason: str,
        owner_state_id: Optional[str],
    ) -> None:
        self.synthetic_transition_mappings.append(
            {
                "emitted_object_id": (
                    f"synthetic:segment:{len(self.synthetic_transition_mappings) + 1}"
                ),
                "scope": _scope_key(scope),
                "line": line,
                "generated_reason": generated_reason,
                "owner_state_id": owner_state_id,
            }
        )

    @staticmethod
    def state_label_text(state: dict[str, Any]) -> str:
        label = state.get("label") or state["id"]
        for body_line in state["attributes"].get("body_lines", []):
            label += f"\n[PlantUML body] {body_line.get('text') or ''}"
        return label

    def state_display_label(self, state: dict[str, Any]) -> str:
        label = self.state_label_text(state)
        body_lines = state["attributes"].get("body_lines", [])
        if not body_lines:
            return label
        for body_line in body_lines:
            text = body_line.get("text") or ""
            self.body_mappings.append(
                {
                    "state_id": state["id"],
                    "fcstm_path": self.emitted_path(state["id"]),
                    "raw_ref": body_line.get("raw_ref"),
                    "text": text,
                    "representation": "state_display_name",
                }
            )
        return label

    def reserve_names(self) -> None:
        for state in self.states:
            parent_scope = self.root_id if state.get("parent") is None else self.emitted_state[state["parent"]]
            self.emitted_state[state["id"]] = self.registry.reserve(
                raw_text=state["attributes"].get("short_name") or state["id"].rsplit(".", 1)[-1],
                canonical_ref=state.get("raw_ref"),
                object_type="state",
                scope=parent_scope,
                generated_reason="qualified_source_state",
                named_text=self.state_label_text(state),
            )
        for state in self.states:
            self.state_mappings.append(
                {
                    "state_id": state["id"],
                    "source_parent": state.get("parent"),
                    "source_kind": state.get("kind"),
                    "source_label": state.get("label"),
                    "source_declared_with_block": state["attributes"].get(
                        "declared_with_block", False
                    ),
                    "fcstm_display_name": self.state_label_text(state),
                    "raw_ref": state.get("raw_ref"),
                    "fcstm_id": self.emitted_state[state["id"]],
                    "fcstm_parent_path": (
                        self.root_id
                        if state.get("parent") is None
                        else self.emitted_path(state["parent"])
                    ),
                    "fcstm_path": self.emitted_path(state["id"]),
                }
            )
        for transition in self.transitions:
            raw_event = transition.get("event")
            if raw_event and raw_event not in self.events:
                self.events[raw_event] = self.registry.reserve(
                    raw_text=raw_event,
                    canonical_ref=transition.get("raw_ref"),
                    object_type="event",
                    scope=self.root_id,
                    generated_reason="opaque_plantuml_transition_label",
                    named_text=raw_event,
                )
        self.event_mappings = [
            {
                "raw_label": raw_event,
                "fcstm_id": event_id,
                "fcstm_path": f"{self.root_id}.{event_id}",
                "representation": "opaque_named_event",
            }
            for raw_event, event_id in self.events.items()
        ]

    def is_composite(self, state_id: str) -> bool:
        return self.state_by_id[state_id].get("kind") == "composite" or bool(self.children[state_id])

    def has_lifecycle_wrapper(self, state_id: str) -> bool:
        return bool(self.state_by_id[state_id]["attributes"].get("lifecycle_actions")) and not self.is_composite(state_id)

    def has_invalid_initial_wrapper(self, state_id: str) -> bool:
        return any(
            not self.initial_target_path(transition)
            for transition in self.initial_by_scope.get(state_id, [])
        )

    def is_operational_composite(self, state_id: str) -> bool:
        return (
            self.is_composite(state_id)
            or self.has_lifecycle_wrapper(state_id)
            or self.has_invalid_initial_wrapper(state_id)
        )

    def trigger(self, transition: dict[str, Any]) -> str:
        raw_event = transition.get("event")
        return f" : /{self.events[raw_event]}" if raw_event else ""

    def state_chain(self, state_id: str) -> list[str]:
        chain = [state_id]
        current = self.parent[state_id]
        while current is not None:
            chain.append(current)
            current = self.parent[current]
        return list(reversed(chain))

    def direct_initial_targets(self, scope: Optional[str]) -> list[str]:
        child_ids = set(self.children[scope])
        return [
            transition["target"]
            for transition in self.initial_by_scope.get(scope, [])
            if transition["target"] in child_ids
        ]

    def initial_target_path(self, transition: dict[str, Any]) -> list[str]:
        scope = transition.get("scope")
        target = transition["target"]
        if target in self.children[scope]:
            return [target]
        target_chain = self.state_chain(target)
        if scope is None:
            return target_chain
        if scope in target_chain:
            position = target_chain.index(scope)
            return target_chain[position + 1 :]
        return []

    def has_valid_initial(self, scope: str) -> bool:
        return any(self.initial_target_path(item) for item in self.initial_by_scope[scope])

    def target_entry_compatible(self, target_chain: list[str], common: int) -> bool:
        target_branch = target_chain[common]
        path = target_chain[common:]
        if len(path) == 1:
            return True
        current = target_branch
        for wanted_child in path[1:]:
            if wanted_child not in self.direct_initial_targets(current):
                return False
            current = wanted_child
        return True

    def emit_target_route(
        self,
        mapping: _Mapping,
        transition: dict[str, Any],
        path: list[str],
    ) -> None:
        for parent_state, child_state in zip(path, path[1:]):
            line = f"[*] -> {self.emitted_state[child_state]}{self.trigger(transition)};"
            self.emit_priority_entry(
                mapping,
                scope=parent_state,
                line=line,
                generated_role="cross_scope_target_entry_segment",
            )

    def emit_priority_entry(
        self,
        mapping: _Mapping,
        *,
        scope: Optional[str],
        line: str,
        generated_role: str,
    ) -> None:
        position = self.priority_entry_count_by_scope[scope]
        self.lines_by_scope[scope].insert(position, line)
        self.priority_entry_count_by_scope[scope] += 1
        mapping.emitted.append(
            {
                "emitted_object_id": f"{mapping.transition_id}:segment:{len(mapping.emitted) + 1}",
                "scope": _scope_key(scope),
                "line": line,
                "generated_role": generated_role,
                "source_transition_id": mapping.transition_id,
            }
        )

    def emit(
        self,
        mapping: _Mapping,
        *,
        scope: Optional[str],
        line: str,
        generated_role: str,
    ) -> None:
        self.lines_by_scope[scope].append(line)
        mapping.emitted.append(
            {
                "emitted_object_id": f"{mapping.transition_id}:segment:{len(mapping.emitted) + 1}",
                "scope": _scope_key(scope),
                "line": line,
                "generated_role": generated_role,
                "source_transition_id": mapping.transition_id,
            }
        )

    def block_transition(self, transition: dict[str, Any], reason_code: str, message: str) -> None:
        mapping = _Mapping(
            transition_id=transition["id"],
            status="blocked_unsupported",
            reason_code=reason_code,
            source=transition["source"],
            target=transition["target"],
            raw_ref=transition.get("raw_ref"),
        )
        self.mappings.append(mapping)
        self.blockers.append(
            {
                "kind": "transition",
                "reason_code": reason_code,
                "message": message,
                "transition_id": transition["id"],
                "raw_ref": transition.get("raw_ref"),
                "raw_line": transition.get("attributes", {}).get("raw_line"),
            }
        )

    def render_initial(self, transition: dict[str, Any]) -> None:
        scope = transition.get("scope")
        target_path = self.initial_target_path(transition)
        if not target_path:
            owner_scope = self.root_id if scope is None else self.emitted_state[scope]
            target_label = transition["target"]
            surrogate_label = (
                f"PlantUML initial target outside child scope: {target_label}"
            )
            surrogate = self.registry.reserve(
                raw_text=f"InvalidInitial{transition['id']}",
                canonical_ref=transition.get("raw_ref"),
                object_type="lowering_state",
                scope=owner_scope,
                generated_reason="invalid_source_initial_target_surrogate",
                named_text=surrogate_label,
            )
            self.record_synthetic_state(
                scope=scope,
                emitted_id=surrogate,
                display_name=surrogate_label,
                generated_reason="invalid_source_initial_target_surrogate",
                raw_ref=transition.get("raw_ref"),
                source_transition_id=transition["id"],
            )
            self.synthetic_states_by_scope[scope].append(
                f"state {surrogate} named {_dsl_string(surrogate_label)};"
            )
            mapping = _Mapping(
                transition_id=transition["id"],
                status="mapped",
                reason_code="R45.MAP.invalid_source_initial_surrogate",
                source=transition["source"],
                target=transition["target"],
                raw_ref=transition.get("raw_ref"),
            )
            self.emit(
                mapping,
                scope=scope,
                line=f"[*] -> {surrogate};",
                generated_role="invalid_source_initial_surrogate",
            )
            self.mappings.append(mapping)
            self.mapped_initial_scopes.add(scope)
            self.add_operational_debt(
                "R45.DEBT.invalid_source_initial_target",
                "PlantUML initial edge targets its own scope or a state outside that scope; FCSTM preserves the raw target identity in a stoppable surrogate instead of guessing entry behavior.",
                kind="transition",
                transition_id=transition["id"],
                source=transition["source"],
                target=transition["target"],
                scope=_scope_key(scope),
                raw_ref=transition.get("raw_ref"),
            )
            return
        mapping = _Mapping(
            transition_id=transition["id"],
            status="mapped",
            reason_code="R45.MAP.initial_boundary",
            source=transition["source"],
            target=transition["target"],
            raw_ref=transition.get("raw_ref"),
        )
        # PlantUML accepts labels on initial edges and its SCXML exporter carries
        # the complete label as an event. FCSTM composite entry cannot stabilize
        # at an event-gated initial marker, so use an explicit wait state before
        # consuming the opaque event and entering the real source child.
        if transition.get("event"):
            owner_scope = self.root_id if scope is None else self.emitted_state[scope]
            wait_label = f"Awaiting initial event: {transition['event']}"
            wait_state = self.registry.reserve(
                raw_text=f"InitialWait{transition['id']}",
                canonical_ref=transition.get("raw_ref"),
                object_type="lowering_state",
                scope=owner_scope,
                generated_reason="event_gated_plantuml_initial_wait",
                named_text=wait_label,
            )
            self.record_synthetic_state(
                scope=scope,
                emitted_id=wait_state,
                display_name=wait_label,
                generated_reason="event_gated_plantuml_initial_wait",
                raw_ref=transition.get("raw_ref"),
                source_transition_id=transition["id"],
            )
            self.synthetic_states_by_scope[scope].append(
                f"state {wait_state} named {_dsl_string(wait_label)};"
            )
            self.emit(
                mapping,
                scope=scope,
                line=f"[*] -> {wait_state};",
                generated_role="source_initial_wait_entry",
            )
            line = (
                f"{wait_state} -> {self.emitted_state[target_path[0]]}"
                f"{self.trigger(transition)};"
            )
        else:
            line = f"[*] -> {self.emitted_state[target_path[0]]};"
        self.emit(mapping, scope=scope, line=line, generated_role="source_initial_transition")
        if len(target_path) > 1:
            for parent_state, child_state in zip(target_path, target_path[1:]):
                route = f"[*] -> {self.emitted_state[child_state]}{self.trigger(transition)};"
                self.emit_priority_entry(
                    mapping,
                    scope=parent_state,
                    line=route,
                    generated_role="source_initial_nested_entry_segment",
                )
        self.mappings.append(mapping)
        self.mapped_initial_scopes.add(scope)

    def render_final(self, transition: dict[str, Any]) -> None:
        self.final_source_count += 1
        source = transition["source"]
        boundary_scope = transition.get("scope")
        ancestor_scopes = set(self.state_chain(source))
        if boundary_scope is not None and boundary_scope not in ancestor_scopes:
            self.block_transition(
                transition,
                "R45.BLOCKED.final_scope_mismatch",
                "Final boundary is outside the source state's ancestor scopes.",
            )
            return
        mapping = _Mapping(
            transition_id=transition["id"],
            status="mapped",
            reason_code="R45.MAP.final_boundary",
            source=source,
            target=transition["target"],
            raw_ref=transition.get("raw_ref"),
        )
        if boundary_scope is not None:
            wait_label = f"Completed final boundary: {source}"
            wait_state = self.registry.reserve(
                raw_text=f"FinalWait{transition['id']}",
                canonical_ref=transition.get("raw_ref"),
                object_type="lowering_state",
                scope=self.emitted_state[boundary_scope],
                generated_reason="nested_plantuml_final_completion_hold",
                named_text=wait_label,
            )
            self.record_synthetic_state(
                scope=boundary_scope,
                emitted_id=wait_state,
                display_name=wait_label,
                generated_reason="nested_plantuml_final_completion_hold",
                raw_ref=transition.get("raw_ref"),
                source_transition_id=transition["id"],
            )
            self.synthetic_states_by_scope[boundary_scope].append(
                f"state {wait_state} named {_dsl_string(wait_label)};"
            )
            if self.parent[source] == boundary_scope:
                prefix = "!" if self.is_operational_composite(source) else ""
                line = (
                    f"{prefix}{self.emitted_state[source]} -> {wait_state}"
                    f"{self.trigger(transition)};"
                )
                self.emit(
                    mapping,
                    scope=boundary_scope,
                    line=line,
                    generated_role="nested_final_completion_hold",
                )
            else:
                current = source
                while self.parent[current] != boundary_scope:
                    parent_scope = self.parent[current]
                    prefix = "!" if self.is_operational_composite(current) else ""
                    suffix = self.trigger(transition)
                    line = f"{prefix}{self.emitted_state[current]} -> [*]{suffix};"
                    self.emit(
                        mapping,
                        scope=parent_scope,
                        line=line,
                        generated_role="nested_final_exit_segment",
                    )
                    current = parent_scope
                continuation = (
                    f"{self.emitted_state[current]} -> {wait_state}"
                    f"{self.trigger(transition)};"
                )
                self.emit(
                    mapping,
                    scope=boundary_scope,
                    line=continuation,
                    generated_role="nested_final_completion_continuation",
                )
            self.mappings.append(mapping)
            self.final_mapped_count += 1
            return

        current = source
        while self.parent[current] != boundary_scope:
            parent_scope = self.parent[current]
            prefix = "!" if self.is_operational_composite(current) else ""
            suffix = self.trigger(transition)
            line = f"{prefix}{self.emitted_state[current]} -> [*]{suffix};"
            self.emit(mapping, scope=parent_scope, line=line, generated_role="final_exit_segment")
            current = parent_scope
        prefix = "!" if self.is_operational_composite(current) else ""
        suffix = self.trigger(transition)
        line = f"{prefix}{self.emitted_state[current]} -> [*]{suffix};"
        self.emit(mapping, scope=boundary_scope, line=line, generated_role="source_final_transition")
        self.mappings.append(mapping)
        self.final_mapped_count += 1

    def render_same_scope(self, transition: dict[str, Any]) -> None:
        source = transition["source"]
        target = transition["target"]
        scope = self.parent[source]
        mapping = _Mapping(
            transition_id=transition["id"],
            status="mapped",
            reason_code="R45.MAP.direct_sibling",
            source=source,
            target=target,
            raw_ref=transition.get("raw_ref"),
        )
        prefix = "!" if self.is_operational_composite(source) else ""
        line = (
            f"{prefix}{self.emitted_state[source]} -> {self.emitted_state[target]}"
            f"{self.trigger(transition)};"
        )
        self.emit(mapping, scope=scope, line=line, generated_role="source_direct_transition")
        self.mappings.append(mapping)

    def render_cross_scope(self, transition: dict[str, Any]) -> None:
        source = transition["source"]
        target = transition["target"]
        source_chain = self.state_chain(source)
        target_chain = self.state_chain(target)
        common = 0
        while (
            common < len(source_chain)
            and common < len(target_chain)
            and source_chain[common] == target_chain[common]
        ):
            common += 1
        if common == len(source_chain):
            path_inside_source = target_chain[common:]
            if not path_inside_source:
                self.block_transition(
                    transition,
                    "R45.BLOCKED.noninitial_nested_target",
                    "Composite-to-descendant target does not follow an explicit initial entry path.",
                )
                return
            target_branch = path_inside_source[0]
            mapping = _Mapping(
                transition_id=transition["id"],
                status="mapped",
                reason_code="R45.MAP.composite_to_descendant_forced",
                source=source,
                target=target,
                raw_ref=transition.get("raw_ref"),
            )
            line = f"! * -> {self.emitted_state[target_branch]}{self.trigger(transition)};"
            self.emit(
                mapping,
                scope=source,
                line=line,
                generated_role="composite_source_forced_descendant_entry",
            )
            self.emit_target_route(mapping, transition, path_inside_source)
            self.mappings.append(mapping)
            return
        if common == len(target_chain):
            mapping = _Mapping(
                transition_id=transition["id"],
                status="mapped",
                reason_code="R45.MAP.descendant_to_ancestor_reentry",
                source=source,
                target=target,
                raw_ref=transition.get("raw_ref"),
            )
            current = source
            while self.parent[current] != target:
                parent_scope = self.parent[current]
                prefix = "!" if self.is_operational_composite(current) else ""
                suffix = self.trigger(transition)
                line = f"{prefix}{self.emitted_state[current]} -> [*]{suffix};"
                self.emit(
                    mapping,
                    scope=parent_scope,
                    line=line,
                    generated_role="ancestor_reentry_exit_segment",
                )
                current = parent_scope
            prefix = "!" if self.is_operational_composite(current) else ""
            suffix = self.trigger(transition)
            exit_line = f"{prefix}{self.emitted_state[current]} -> [*]{suffix};"
            self.emit(
                mapping,
                scope=target,
                line=exit_line,
                generated_role="ancestor_reentry_child_exit",
            )
            reentry = (
                f"{self.emitted_state[target]} -> {self.emitted_state[target]}"
                f"{self.trigger(transition)};"
            )
            self.emit(
                mapping,
                scope=self.parent[target],
                line=reentry,
                generated_role="ancestor_reentry_parent_continuation",
            )
            self.mappings.append(mapping)
            return

        lca_scope = source_chain[common - 1] if common else None
        source_branch = source_chain[common]
        target_branch = target_chain[common]
        mapping = _Mapping(
            transition_id=transition["id"],
            status="mapped",
            reason_code="R45.MAP.cross_scope_exit_continuation",
            source=source,
            target=target,
            raw_ref=transition.get("raw_ref"),
        )
        if source != source_branch:
            current = source
            while self.parent[current] != lca_scope:
                parent_scope = self.parent[current]
                prefix = "!" if self.is_operational_composite(current) else ""
                suffix = self.trigger(transition)
                line = f"{prefix}{self.emitted_state[current]} -> [*]{suffix};"
                self.emit(
                    mapping,
                    scope=parent_scope,
                    line=line,
                    generated_role="cross_scope_exit_segment",
                )
                current = parent_scope
        prefix = "!" if source == source_branch and self.is_operational_composite(source) else ""
        suffix = self.trigger(transition)
        continuation = (
            f"{prefix}{self.emitted_state[source_branch]} -> {self.emitted_state[target_branch]}"
            f"{suffix};"
        )
        self.emit(
            mapping,
            scope=lca_scope,
            line=continuation,
            generated_role="cross_scope_parent_continuation",
        )
        self.emit_target_route(mapping, transition, target_chain[common:])
        self.mappings.append(mapping)

    def map_transitions(self) -> None:
        for transition in self.transitions:
            if transition["attributes"]["transition_kind"] == "initial":
                self.initial_by_scope[transition.get("scope")].append(transition)
        for transition in self.transitions:
            kind = transition["attributes"]["transition_kind"]
            if kind == "initial":
                self.render_initial(transition)
            elif kind == "final":
                self.render_final(transition)
            elif self.parent[transition["source"]] == self.parent[transition["target"]]:
                self.render_same_scope(transition)
            else:
                self.render_cross_scope(transition)

    def add_operational_debts(self) -> None:
        unlabeled_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
        initial_by_scope: dict[Optional[str], list[dict[str, Any]]] = defaultdict(list)
        for transition in self.transitions:
            kind = transition["attributes"]["transition_kind"]
            if transition.get("label"):
                self.add_operational_debt(
                    "R45.DEBT.opaque_transition_label_semantics",
                    "The complete PlantUML transition label is preserved as a named FCSTM event, but R4.5 does not claim that the source text denotes an event rather than a guard, effect, timing constraint, or mixed label.",
                    kind="transition_label",
                    transition_id=transition["id"],
                    raw_ref=transition.get("raw_ref"),
                    raw_label=transition.get("label"),
                    fcstm_event_id=self.events.get(transition.get("event")),
                    representation="opaque_named_event",
                )
            if kind == "normal" and not transition.get("event"):
                unlabeled_by_source[transition["source"]].append(transition)
            elif kind == "initial":
                initial_by_scope[transition.get("scope")].append(transition)
        for source, transitions in unlabeled_by_source.items():
            if len(transitions) < 2:
                continue
            self.add_operational_debt(
                "R45.DEBT.ambiguous_unlabeled_fanout",
                "Multiple unlabeled outgoing edges are preserved structurally, but FCSTM's single-active-state runtime resolves them by priority and cannot prove nondeterministic or concurrent source semantics.",
                kind="fan_out",
                source=source,
                transition_ids=[item["id"] for item in transitions],
                raw_refs=[item.get("raw_ref") for item in transitions],
            )
        for scope, transitions in initial_by_scope.items():
            if len(transitions) < 2:
                continue
            self.add_operational_debt(
                "R45.DEBT.multiple_initial_fanout",
                "Multiple initial edges in one lexical scope are all preserved, but FCSTM executes them by priority and cannot infer choice or concurrency.",
                kind="fan_out",
                scope=_scope_key(scope),
                transition_ids=[item["id"] for item in transitions],
                raw_refs=[item.get("raw_ref") for item in transitions],
            )
        for state in self.states:
            for body_line in state["attributes"].get("body_lines", []):
                self.add_operational_debt(
                    "R45.DEBT.opaque_state_body_semantics",
                    "PlantUML state body text is preserved in the FCSTM display name and trace, but R4.5 does not interpret it as executable guard, timing, or action semantics.",
                    kind="state_body",
                    state_id=state["id"],
                    raw_ref=body_line.get("raw_ref"),
                    text=body_line.get("text"),
                )
            if state.get("kind") in {"fork", "join"}:
                self.add_operational_debt(
                    "R45.DEBT.explicit_concurrency_pseudostate",
                    "The explicit PlantUML fork/join node and edges are preserved, but FCSTM has no orthogonal-region execution semantics and therefore applies ordinary pseudo-state priority.",
                    kind="state",
                    state_id=state["id"],
                    raw_ref=state.get("raw_ref"),
                )
        for item in self.canonical.get("metadata", {}).get("orphan_lifecycle_actions", []):
            self.add_operational_debt(
                "R45.DEBT.lifecycle_owner_ambiguous",
                "Bare root-level lifecycle syntax is preserved as root display metadata because the source does not identify an owning state.",
                **item,
            )

    def render_state(self, state_id: str, indent: int) -> list[str]:
        state = self.state_by_id[state_id]
        emitted = self.emitted_state[state_id]
        label = self.state_display_label(state)
        pad = " " * indent
        pseudo = state.get("kind") in {"fork", "join", "choice"}
        keyword = "pseudo state" if pseudo else "state"
        composite = self.is_composite(state_id) or self.has_invalid_initial_wrapper(state_id)
        lifecycle = state["attributes"].get("lifecycle_actions", [])
        lifecycle_wrapper = bool(lifecycle) and not composite
        if not composite and not lifecycle:
            return [f"{pad}{keyword} {emitted} named {_dsl_string(label)};"]
        lines = [f"{pad}{keyword} {emitted} named {_dsl_string(label)} {{"]
        body_indent = indent + 4
        body_pad = " " * body_indent
        for action in lifecycle:
            self.lifecycle_source_count += 1
            action_id = self.registry.reserve(
                raw_text=_action_identifier_source(action["text"]),
                canonical_ref=action.get("raw_ref"),
                object_type="lifecycle_action",
                scope=emitted,
                generated_reason="plantuml_lifecycle_abstract_action",
                named_text=action["text"],
            )
            if action["kind"] == "do" and (composite or lifecycle_wrapper):
                lines.append(f"{body_pad}>> during before abstract {action_id};")
            else:
                keyword_action = {"entry": "enter", "do": "during", "exit": "exit"}[action["kind"]]
                lines.append(f"{body_pad}{keyword_action} abstract {action_id};")
            self.lifecycle_mappings.append(
                {
                    "state_id": state_id,
                    "fcstm_path": self.emitted_path(state_id),
                    "kind": action["kind"],
                    "text": action["text"],
                    "raw_ref": action.get("raw_ref"),
                    "fcstm_action_id": action_id,
                    "representation": "abstract_lifecycle_action",
                }
            )
            self.lifecycle_mapped_count += 1
        if lifecycle_wrapper:
            active_state = self.registry.reserve(
                raw_text="LifecycleActive",
                canonical_ref=state.get("raw_ref"),
                object_type="lowering_state",
                scope=emitted,
                generated_reason="lifecycle_only_state_active_leaf",
                named_text=f"Active body of {label}",
            )
            self.record_synthetic_state(
                scope=state_id,
                emitted_id=active_state,
                display_name=f"Active body of {label}",
                generated_reason="lifecycle_only_state_active_leaf",
                raw_ref=state.get("raw_ref"),
            )
            self.synthetic_states_by_scope[state_id].append(
                f"state {active_state} named {_dsl_string(f'Active body of {label}')};"
            )
            active_initial = f"[*] -> {active_state};"
            self.lines_by_scope[state_id].insert(0, active_initial)
            self.record_synthetic_transition(
                scope=state_id,
                line=active_initial,
                generated_reason="lifecycle_only_state_active_leaf",
                owner_state_id=state_id,
            )
        if composite:
            if state_id not in self.mapped_initial_scopes:
                self.add_operational_debt(
                    "R45.DEBT.missing_explicit_initial",
                    "Composite source state has no explicit PlantUML child initial; FCSTM enters a visible stoppable placeholder instead of guessing a child.",
                    kind="scope",
                    scope=state_id,
                )
                synthetic = self.registry.reserve(
                    raw_text="UnspecifiedInitial",
                    canonical_ref=f"canonical:{state_id}:missing_initial",
                    object_type="lowering_state",
                    scope=emitted,
                    generated_reason="missing_source_initial_fail_closed",
                )
                self.record_synthetic_state(
                    scope=state_id,
                    emitted_id=synthetic,
                    display_name="Unspecified initial",
                    generated_reason="missing_source_initial_fail_closed",
                    raw_ref=None,
                )
                lines.append(f"{body_pad}state {synthetic} named \"Unspecified initial\";")
                placeholder_initial = f"[*] -> {synthetic};"
                self.lines_by_scope[state_id].append(placeholder_initial)
                self.record_synthetic_transition(
                    scope=state_id,
                    line=placeholder_initial,
                    generated_reason="missing_source_initial_fail_closed",
                    owner_state_id=state_id,
                )
        for child in self.children[state_id]:
            lines.extend(self.render_state(child, body_indent))
        for line in self.synthetic_states_by_scope[state_id]:
            lines.append(f"{body_pad}{line}")
        for line in self.lines_by_scope[state_id]:
            lines.append(f"{body_pad}{line}")
        lines.append(f"{pad}}}")
        return lines

    def render(self) -> dict[str, Any]:
        self.reserve_names()
        self.map_transitions()
        self.add_operational_debts()
        root_label = self.model.get("name") or self.canonical["example_id"]
        for item in self.canonical.get("metadata", {}).get("orphan_lifecycle_actions", []):
            text = item.get("text") or ""
            root_label += f"\n[Unowned PlantUML {item.get('kind', 'lifecycle')}] {text}"
            self.orphan_lifecycle_mappings.append(
                {
                    "kind": item.get("kind"),
                    "text": text,
                    "raw_ref": item.get("raw_ref"),
                    "fcstm_path": self.root_id,
                    "representation": "root_display_name",
                }
            )
        lines = [f"state {self.root_id} named {_dsl_string(root_label)} {{"]
        pad = " " * 4
        for raw_event, event_id in self.events.items():
            lines.append(f"{pad}event {event_id} named {_dsl_string(raw_event)};")
        if None not in self.mapped_initial_scopes:
            self.add_operational_debt(
                "R45.DEBT.missing_explicit_initial",
                "Root source model has no explicit PlantUML initial transition; FCSTM enters a visible stoppable placeholder instead of guessing a state.",
                kind="scope",
                scope="__root__",
            )
            synthetic = self.registry.reserve(
                raw_text="UnspecifiedInitial",
                canonical_ref="canonical:__root__:missing_initial",
                object_type="lowering_state",
                scope=self.root_id,
                generated_reason="missing_source_initial_fail_closed",
            )
            self.record_synthetic_state(
                scope=None,
                emitted_id=synthetic,
                display_name="Unspecified initial",
                generated_reason="missing_source_initial_fail_closed",
                raw_ref=None,
            )
            lines.append(f"{pad}state {synthetic} named \"Unspecified initial\";")
            placeholder_initial = f"[*] -> {synthetic};"
            self.lines_by_scope[None].append(placeholder_initial)
            self.record_synthetic_transition(
                scope=None,
                line=placeholder_initial,
                generated_reason="missing_source_initial_fail_closed",
                owner_state_id=None,
            )
        for line in self.synthetic_states_by_scope[None]:
            lines.append(f"{pad}{line}")
        for child in self.children[None]:
            lines.extend(self.render_state(child, 4))
        for line in self.lines_by_scope[None]:
            lines.append(f"{pad}{line}")
        lines.append("}")
        fcstm = "\n".join(lines) + "\n"

        mapped = [mapping for mapping in self.mappings if mapping.status == "mapped"]
        blocked = [mapping for mapping in self.mappings if mapping.status != "mapped"]
        lifecycle_total = self.lifecycle_source_count + len(
            self.canonical.get("metadata", {}).get("orphan_lifecycle_actions", [])
        )
        lifecycle_structurally_mapped = self.lifecycle_mapped_count + len(
            self.orphan_lifecycle_mappings
        )
        body_total = sum(
            len(state["attributes"].get("body_lines", [])) for state in self.states
        )
        structural_verdict = "structure_preserved" if not self.blockers else "structure_blocked"
        operational_status = (
            "within_r45_executable_projection"
            if not self.operational_debts
            else "source_ambiguity_or_unsupported_semantics_preserved"
        )
        comparison = {
            "schema_version": "r4_5.plantuml_fcstm_comparison.v2",
            "example_id": self.canonical["example_id"],
            "verdict": structural_verdict,
            "structural_verdict": structural_verdict,
            "operational_status": operational_status,
            "fcstm_execution_eligible": not self.operational_debts and not self.blockers,
            "discover_eligible": not self.operational_debts and not self.blockers,
            "source_state_count": len(self.states),
            "emitted_state_count": len(self.emitted_state),
            "state_coverage": f"{len(self.emitted_state)}/{len(self.states)}",
            "source_transition_count": len(self.transitions),
            "mapped_transition_count": len(mapped),
            "blocked_transition_count": len(blocked),
            "silently_dropped_transition_count": len(self.transitions) - len(mapped) - len(blocked),
            "transition_coverage": f"{len(mapped) + len(blocked)}/{len(self.transitions)}",
            "final_transition_coverage": f"{self.final_mapped_count}/{self.final_source_count}",
            "lifecycle_action_coverage": f"{lifecycle_structurally_mapped}/{lifecycle_total}",
            "abstract_lifecycle_hook_coverage": f"{self.lifecycle_mapped_count}/{lifecycle_total}",
            "body_line_coverage": f"{len(self.body_mappings)}/{body_total}",
            "opaque_label_count": sum(1 for transition in self.transitions if transition.get("label")),
            "blockers": self.blockers,
            "operational_debts": self.operational_debts,
            "state_mappings": self.state_mappings,
            "synthetic_state_mappings": self.synthetic_state_mappings,
            "synthetic_transition_mappings": self.synthetic_transition_mappings,
            "event_mappings": self.event_mappings,
            "body_mappings": self.body_mappings,
            "lifecycle_mappings": self.lifecycle_mappings,
            "orphan_lifecycle_mappings": self.orphan_lifecycle_mappings,
            "transition_mappings": [
                {
                    "source_transition": {
                        "id": item.transition_id,
                        "scope": self.transition_by_id[item.transition_id].get("scope"),
                        "kind": self.transition_by_id[item.transition_id]["attributes"][
                            "transition_kind"
                        ],
                        "source": item.source,
                        "target": item.target,
                        "raw_label": self.transition_by_id[item.transition_id].get("label"),
                        "raw_event": self.transition_by_id[item.transition_id].get("event"),
                        "raw_ref": item.raw_ref,
                    },
                    "transition_id": item.transition_id,
                    "status": item.status,
                    "reason_code": item.reason_code,
                    "source": item.source,
                    "target": item.target,
                    "raw_ref": item.raw_ref,
                    "emitted": item.emitted,
                }
                for item in self.mappings
            ],
        }
        return {
            "fcstm": fcstm,
            "comparison": comparison,
            "name_mapping": self.registry.to_jsonable(),
        }


def lower_plantuml_source(canonical: dict[str, Any]) -> dict[str, Any]:
    """Lower Java source-canonical PlantUML to an auditable FCSTM artifact."""

    if canonical.get("adapter") != "plantuml_java_scope_aware_source":
        raise ValueError("plantuml Java source canonical required")
    return _Lowerer(canonical).render()
