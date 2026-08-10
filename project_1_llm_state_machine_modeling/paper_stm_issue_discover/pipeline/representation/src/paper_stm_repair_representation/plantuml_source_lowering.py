from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Optional

from .pyfcstm_names import NameRegistry
from .plantuml_working_contract import build_working_contract


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
    route_code: Optional[int] = None
    route_trigger_count: int = 0
    emitted: list[dict[str, Any]] = field(default_factory=list)


class _Lowerer:
    def __init__(self, canonical: dict[str, Any]) -> None:
        self.canonical = canonical
        self.model = canonical["model"]
        self.states = list(self.model["states"])
        self.transitions = list(self.model["transitions"])
        self.concurrent_regions = list(self.model.get("concurrent_regions", []))
        self.concurrent_region_separators = list(
            canonical.get("metadata", {}).get("concurrent_region_separators", [])
        )
        self.source_normalizations = list(
            canonical.get("metadata", {}).get("source_normalizations", [])
        )
        self.concurrent_regions_by_scope: dict[Optional[str], list[dict[str, Any]]] = (
            defaultdict(list)
        )
        self.concurrent_separators_by_scope: dict[
            Optional[str], list[dict[str, Any]]
        ] = defaultdict(list)
        for region in self.concurrent_regions:
            self.concurrent_regions_by_scope[region.get("owner_scope")].append(region)
        for separator in self.concurrent_region_separators:
            self.concurrent_separators_by_scope[separator.get("owner_scope")].append(
                separator
            )
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
        self.line_records_by_scope: dict[
            Optional[str], list[dict[str, Any]]
        ] = defaultdict(list)
        self.synthetic_states_by_scope: dict[Optional[str], list[str]] = defaultdict(
            list
        )
        self.missing_initial_helpers: dict[Optional[str], str] = {}
        self.mappings: list[_Mapping] = []
        self.blockers: list[dict[str, Any]] = []
        self.operational_debts: list[dict[str, Any]] = []
        self.state_mappings: list[dict[str, Any]] = []
        self.synthetic_state_mappings: list[dict[str, Any]] = []
        self.synthetic_transition_mappings: list[dict[str, Any]] = []
        self.route_variable_id: Optional[str] = None
        self.route_transition_codes: dict[str, int] = {}
        self.route_source_refs: dict[str, Optional[str]] = {}
        self.priority_entry_count_by_scope: dict[Optional[str], int] = defaultdict(int)
        self.event_mappings: list[dict[str, Any]] = []
        self.body_mappings: list[dict[str, Any]] = []
        self.lifecycle_mappings: list[dict[str, Any]] = []
        self.orphan_lifecycle_mappings: list[dict[str, Any]] = []
        self.concurrent_region_mappings: list[dict[str, Any]] = []
        self.concurrent_region_separator_mappings: list[dict[str, Any]] = []
        self.source_normalization_mappings: list[dict[str, Any]] = []
        self.initial_by_scope: dict[Optional[str], list[dict[str, Any]]] = defaultdict(
            list
        )
        self.mapped_initial_scopes: set[Optional[str]] = set()
        self.lifecycle_source_count = 0
        self.lifecycle_mapped_count = 0
        self.final_source_count = 0
        self.final_mapped_count = 0

    def add_operational_debt(
        self, reason_code: str, message: str, **details: Any
    ) -> None:
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
                "source_scope": scope,
                "fcstm_id": emitted_id,
                "fcstm_parent_path": scope_path,
                "fcstm_path": f"{scope_path}.{emitted_id}",
                "display_name": display_name,
                "generated_reason": generated_reason,
                "raw_ref": raw_ref,
                "source_transition_id": source_transition_id,
            }
        )

    def index_initial_transitions(self) -> None:
        for transition in self.transitions:
            if transition["attributes"]["transition_kind"] == "initial":
                self.initial_by_scope[transition.get("scope")].append(transition)

    def prepare_missing_initial_helpers(self) -> None:
        candidate_scopes: list[Optional[str]] = [None]
        candidate_scopes.extend(
            state["id"]
            for state in self.states
            if self.is_operational_composite(state["id"])
        )
        for scope in candidate_scopes:
            if self.initial_by_scope.get(scope):
                continue
            owner_scope = self.root_id if scope is None else self.emitted_state[scope]
            canonical_scope = "__root__" if scope is None else scope
            self.add_operational_debt(
                "R45.DEBT.missing_explicit_initial",
                "The source scope has no explicit PlantUML initial transition; FCSTM enters a visible stoppable placeholder instead of guessing a child.",
                kind="scope",
                scope=canonical_scope,
            )
            synthetic = self.registry.reserve(
                raw_text="UnspecifiedInitial",
                canonical_ref=f"canonical:{canonical_scope}:missing_initial",
                object_type="lowering_state",
                scope=owner_scope,
                generated_reason="missing_source_initial_fail_closed",
            )
            self.record_synthetic_state(
                scope=scope,
                emitted_id=synthetic,
                display_name="Unspecified initial",
                generated_reason="missing_source_initial_fail_closed",
                raw_ref=None,
            )
            self.synthetic_states_by_scope[scope].append(
                f'state {synthetic} named "Unspecified initial";'
            )
            placeholder_initial = f"[*] -> {synthetic};"
            self.lines_by_scope[scope].append(placeholder_initial)
            self.record_synthetic_transition(
                scope=scope,
                line=placeholder_initial,
                generated_reason="missing_source_initial_fail_closed",
                owner_state_id=scope,
            )
            self.missing_initial_helpers[scope] = synthetic

    def record_synthetic_transition(
        self,
        *,
        scope: Optional[str],
        line: str,
        generated_reason: str,
        owner_state_id: Optional[str],
        position: Optional[int] = None,
    ) -> None:
        record = {
            "emitted_object_id": (
                f"synthetic:segment:{len(self.synthetic_transition_mappings) + 1}"
            ),
            "scope": _scope_key(scope),
            "line": line,
            "generated_reason": generated_reason,
            "owner_state_id": owner_state_id,
        }
        self.synthetic_transition_mappings.append(record)
        if position is None:
            self.line_records_by_scope[scope].append(record)
        else:
            self.line_records_by_scope[scope].insert(position, record)

    def concurrent_display_lines(self, scope: Optional[str]) -> list[str]:
        lines = []
        for region in sorted(
            self.concurrent_regions_by_scope.get(scope, []),
            key=lambda item: item["region_index"],
        ):
            states = ", ".join(region.get("state_ids", [])) or "-"
            transitions = ", ".join(region.get("transition_ids", [])) or "-"
            lines.append(
                f"[PlantUML concurrent region {region['region_index']}] "
                f"states={states}; transitions={transitions}"
            )
        for separator in self.concurrent_separators_by_scope.get(scope, []):
            lines.append(
                "[PlantUML concurrent separator] "
                f"region {separator['preceding_region_index']} -> "
                f"{separator['following_region_index']} at {separator['raw_ref']}"
            )
        return lines

    def state_label_text(self, state: dict[str, Any]) -> str:
        label = state.get("label") or state["id"]
        for body_line in state["attributes"].get("body_lines", []):
            label += f"\n[PlantUML body] {body_line.get('text') or ''}"
        for line in self.concurrent_display_lines(state["id"]):
            label += f"\n{line}"
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
            parent_scope = (
                self.root_id
                if state.get("parent") is None
                else self.emitted_state[state["parent"]]
            )
            self.emitted_state[state["id"]] = self.registry.reserve(
                raw_text=state["attributes"].get("short_name")
                or state["id"].rsplit(".", 1)[-1],
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
                    "source_parent_region_indices": state["attributes"].get(
                        "parent_region_indices", [0]
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
        for region in self.concurrent_regions:
            owner_scope = region.get("owner_scope")
            owner_path = (
                self.root_id if owner_scope is None else self.emitted_path(owner_scope)
            )
            display_line = self.concurrent_display_lines(owner_scope)[
                int(region["region_index"])
            ]
            self.concurrent_region_mappings.append(
                {
                    **region,
                    "fcstm_owner_path": owner_path,
                    "display_line": display_line,
                    "representation": "owner_display_name_and_comparison_trace",
                }
            )
        region_count_by_scope = {
            scope: len(regions)
            for scope, regions in self.concurrent_regions_by_scope.items()
        }
        for offset_by_scope, separator in enumerate(self.concurrent_region_separators):
            owner_scope = separator.get("owner_scope")
            owner_path = (
                self.root_id if owner_scope is None else self.emitted_path(owner_scope)
            )
            display_lines = self.concurrent_display_lines(owner_scope)
            display_offset = region_count_by_scope.get(owner_scope, 0)
            prior_same_scope = sum(
                1
                for prior in self.concurrent_region_separators[:offset_by_scope]
                if prior.get("owner_scope") == owner_scope
            )
            self.concurrent_region_separator_mappings.append(
                {
                    **separator,
                    "fcstm_owner_path": owner_path,
                    "display_line": display_lines[display_offset + prior_same_scope],
                    "representation": "owner_display_name_and_comparison_trace",
                }
            )
        self.source_normalization_mappings = [
            {
                **change,
                "fcstm_owner_path": self.root_id,
                "representation": "root_display_name_and_comparison_trace",
            }
            for change in self.source_normalizations
        ]
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

    def has_source_children(self, state_id: str) -> bool:
        return bool(self.children[state_id])

    def has_invalid_initial_wrapper(self, state_id: str) -> bool:
        return any(
            not self.initial_target_path(transition)
            for transition in self.initial_by_scope.get(state_id, [])
        )

    def is_operational_composite(self, state_id: str) -> bool:
        return self.has_source_children(state_id) or self.has_invalid_initial_wrapper(
            state_id
        )

    def trigger(self, transition: dict[str, Any]) -> str:
        raw_event = transition.get("event")
        return f" : /{self.events[raw_event]}" if raw_event else ""

    def route_code(self, mapping: _Mapping, transition: dict[str, Any]) -> int:
        if self.route_variable_id is None:
            self.route_variable_id = self.registry.reserve(
                raw_text="R45RouteToken",
                canonical_ref="canonical:compiler:route_token",
                object_type="lowering_variable",
                scope="",
                generated_reason="protected_cross_scope_route_token",
                named_text="PlantUML lowering route token",
            )
        code = self.route_transition_codes.setdefault(
            transition["id"],
            self.transitions.index(transition) + 1,
        )
        self.route_source_refs[transition["id"]] = transition.get("raw_ref")
        mapping.route_code = code
        return code

    def route_trigger(
        self,
        mapping: _Mapping,
        transition: dict[str, Any],
        code: int,
    ) -> str:
        if self.route_variable_id is None:
            raise RuntimeError("route token is unavailable")
        mapping.route_trigger_count += 1
        return (
            f"{self.trigger(transition)} effect "
            f"{{ {self.route_variable_id} = {code}; }}"
        )

    def route_guard(self, code: int, *, reset: bool = False) -> str:
        if self.route_variable_id is None:
            raise RuntimeError("route token is unavailable")
        suffix = f" : if [{self.route_variable_id} == {code}]"
        if reset:
            suffix += f" effect {{ {self.route_variable_id} = 0; }}"
        return suffix

    def state_chain(self, state_id: str) -> list[str]:
        chain = [state_id]
        current = self.parent[state_id]
        while current is not None:
            chain.append(current)
            current = self.parent[current]
        return list(reversed(chain))

    def source_leaf_descendants(self, state_id: str) -> list[str]:
        children = self.children[state_id]
        if not children:
            return [state_id]
        leaves: list[str] = []
        for child in children:
            leaves.extend(self.source_leaf_descendants(child))
        return leaves

    def emit_composite_leaf_exit_routes(
        self,
        *,
        mapping: _Mapping,
        transition: dict[str, Any],
        source: str,
        route_code: int,
    ) -> None:
        emitted_guards: set[tuple[Optional[str], str]] = set()
        for leaf in self.source_leaf_descendants(source):
            current = leaf
            first = True
            while current != source:
                parent_scope = self.parent[current]
                suffix = (
                    self.route_trigger(mapping, transition, route_code)
                    if first
                    else self.route_guard(route_code)
                )
                line = f"{self.emitted_state[current]} -> [*]{suffix};"
                if first:
                    self.emit(
                        mapping,
                        scope=parent_scope,
                        line=line,
                        generated_role="composite_source_leaf_trigger",
                    )
                elif (parent_scope, line) not in emitted_guards:
                    self.emit_priority_entry(
                        mapping,
                        scope=parent_scope,
                        line=line,
                        generated_role="composite_source_guarded_exit",
                    )
                    emitted_guards.add((parent_scope, line))
                first = False
                current = parent_scope

    def emit_source_route_to_scope(
        self,
        *,
        mapping: _Mapping,
        transition: dict[str, Any],
        source: str,
        stop_scope: Optional[str],
    ) -> tuple[str, int, bool]:
        route_code = self.route_code(mapping, transition)
        triggered = False
        current = source
        if self.is_operational_composite(source):
            if self.has_source_children(source):
                self.emit_composite_leaf_exit_routes(
                    mapping=mapping,
                    transition=transition,
                    source=source,
                    route_code=route_code,
                )
            triggered = True
        while self.parent[current] != stop_scope:
            parent_scope = self.parent[current]
            suffix = (
                self.route_guard(route_code)
                if triggered
                else self.route_trigger(mapping, transition, route_code)
            )
            emitter = self.emit_priority_entry if triggered else self.emit
            emitter(
                mapping,
                scope=parent_scope,
                line=f"{self.emitted_state[current]} -> [*]{suffix};",
                generated_role="source_route_exit_segment",
            )
            triggered = True
            current = parent_scope
        return current, route_code, triggered

    def complete_composite_route_synthetic_triggers(self) -> None:
        for mapping in self.mappings:
            if (
                mapping.route_code is None
                or not self.is_operational_composite(mapping.source)
            ):
                continue
            transition = self.transition_by_id[mapping.transition_id]
            existing = {
                (item["scope"], item["line"])
                for item in mapping.emitted
            }
            for synthetic in self.synthetic_state_mappings:
                scope = synthetic.get("source_scope")
                if scope is None:
                    continue
                if scope != mapping.source and mapping.source not in self.state_chain(scope):
                    continue
                line = (
                    f"{synthetic['fcstm_id']} -> [*]"
                    f"{self.route_trigger(mapping, transition, mapping.route_code)};"
                )
                key = (_scope_key(scope), line)
                self.emit(
                    mapping,
                    scope=scope,
                    line=line,
                    generated_role="composite_source_synthetic_leaf_trigger",
                )
                existing.add(key)
                current = scope
                while current != mapping.source:
                    parent_scope = self.parent[current]
                    guard_line = (
                        f"{self.emitted_state[current]} -> [*]"
                        f"{self.route_guard(mapping.route_code)};"
                    )
                    guard_key = (_scope_key(parent_scope), guard_line)
                    if guard_key not in existing:
                        self.emit_priority_entry(
                            mapping,
                            scope=parent_scope,
                            line=guard_line,
                            generated_role="composite_source_guarded_exit",
                        )
                        existing.add(guard_key)
                    current = parent_scope

    def emit_composite_descendant_target_route(
        self,
        *,
        mapping: _Mapping,
        source: str,
        path: list[str],
        route_code: int,
    ) -> None:
        scoped_targets = [(source, path[0]), *list(zip(path, path[1:]))]
        for index, (scope, child) in enumerate(scoped_targets):
            line = (
                f"[*] -> {self.emitted_state[child]}"
                f"{self.route_guard(route_code, reset=index == len(scoped_targets) - 1)};"
            )
            self.emit_priority_entry(
                mapping,
                scope=scope,
                line=line,
                generated_role="composite_source_target_entry_segment",
            )

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
        return any(
            self.initial_target_path(item) for item in self.initial_by_scope[scope]
        )

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
        path: list[str],
        route_code: int,
    ) -> None:
        pairs = list(zip(path, path[1:]))
        for index, (parent_state, child_state) in enumerate(pairs):
            line = (
                f"[*] -> {self.emitted_state[child_state]}"
                f"{self.route_guard(route_code, reset=index == len(pairs) - 1)};"
            )
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
        record = {
            "emitted_object_id": f"{mapping.transition_id}:segment:{len(mapping.emitted) + 1}",
            "scope": _scope_key(scope),
            "line": line,
            "generated_role": generated_role,
            "source_transition_id": mapping.transition_id,
        }
        self.lines_by_scope[scope].insert(position, line)
        self.line_records_by_scope[scope].insert(position, record)
        self.priority_entry_count_by_scope[scope] += 1
        mapping.emitted.append(record)

    def emit(
        self,
        mapping: _Mapping,
        *,
        scope: Optional[str],
        line: str,
        generated_role: str,
    ) -> None:
        record = {
            "emitted_object_id": f"{mapping.transition_id}:segment:{len(mapping.emitted) + 1}",
            "scope": _scope_key(scope),
            "line": line,
            "generated_role": generated_role,
            "source_transition_id": mapping.transition_id,
        }
        self.lines_by_scope[scope].append(line)
        self.line_records_by_scope[scope].append(record)
        mapping.emitted.append(record)

    def block_transition(
        self, transition: dict[str, Any], reason_code: str, message: str
    ) -> None:
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
                line=(
                    f"[*] -> {surrogate}"
                    f"{self.trigger(transition)};"
                ),
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
        route_code = (
            self.route_code(mapping, transition) if len(target_path) > 1 else None
        )
        suffix = (
            self.route_trigger(mapping, transition, route_code)
            if route_code is not None
            else self.trigger(transition)
        )
        line = f"[*] -> {self.emitted_state[target_path[0]]}{suffix};"
        self.emit(
            mapping, scope=scope, line=line, generated_role="source_initial_transition"
        )
        if route_code is not None:
            pairs = list(zip(target_path, target_path[1:]))
            for index, (parent_state, child_state) in enumerate(pairs):
                route = (
                    f"[*] -> {self.emitted_state[child_state]}"
                    f"{self.route_guard(route_code, reset=index == len(pairs) - 1)};"
                )
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
            projection_scope = self.parent[source]
            owner_scope = (
                self.root_id
                if projection_scope is None
                else self.emitted_state[projection_scope]
            )
            surrogate_label = (
                "PlantUML final boundary outside source ancestry: "
                f"{transition['target']}"
            )
            surrogate = self.registry.reserve(
                raw_text=f"InvalidFinal{transition['id']}",
                canonical_ref=transition.get("raw_ref"),
                object_type="lowering_state",
                scope=owner_scope,
                generated_reason="invalid_source_final_scope_surrogate",
                named_text=surrogate_label,
            )
            self.record_synthetic_state(
                scope=projection_scope,
                emitted_id=surrogate,
                display_name=surrogate_label,
                generated_reason="invalid_source_final_scope_surrogate",
                raw_ref=transition.get("raw_ref"),
                source_transition_id=transition["id"],
            )
            self.synthetic_states_by_scope[projection_scope].append(
                f"state {surrogate} named {_dsl_string(surrogate_label)};"
            )
            mapping = _Mapping(
                transition_id=transition["id"],
                status="mapped",
                reason_code="R45.MAP.invalid_source_final_surrogate",
                source=source,
                target=transition["target"],
                raw_ref=transition.get("raw_ref"),
            )
            if self.has_source_children(source):
                current, route_code, triggered = self.emit_source_route_to_scope(
                    mapping=mapping,
                    transition=transition,
                    source=source,
                    stop_scope=projection_scope,
                )
                if not triggered:
                    raise RuntimeError("composite final route lacks a source trigger")
                line = (
                    f"{self.emitted_state[current]} -> {surrogate}"
                    f"{self.route_guard(route_code, reset=True)};"
                )
                self.emit_priority_entry(
                    mapping,
                    scope=projection_scope,
                    line=line,
                    generated_role="invalid_source_final_surrogate",
                )
            else:
                prefix = "!" if self.is_operational_composite(source) else ""
                self.emit(
                    mapping,
                    scope=projection_scope,
                    line=(
                        f"{prefix}{self.emitted_state[source]} -> {surrogate}"
                        f"{self.trigger(transition)};"
                    ),
                    generated_role="invalid_source_final_surrogate",
                )
            self.mappings.append(mapping)
            self.final_mapped_count += 1
            self.add_operational_debt(
                "R45.DEBT.invalid_source_final_scope",
                "PlantUML final boundary belongs to a scope outside the source state's ancestry; FCSTM preserves the boundary identity in a stoppable surrogate instead of inventing cross-scope completion semantics.",
                kind="transition",
                transition_id=transition["id"],
                source=transition["source"],
                target=transition["target"],
                boundary_scope=_scope_key(boundary_scope),
                projection_scope=_scope_key(projection_scope),
                raw_ref=transition.get("raw_ref"),
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
            if (
                self.parent[source] == boundary_scope
                and not self.has_source_children(source)
            ):
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
                current, route_code, triggered = self.emit_source_route_to_scope(
                    mapping=mapping,
                    transition=transition,
                    source=source,
                    stop_scope=boundary_scope,
                )
                if not triggered:
                    raise RuntimeError("nested final route lacks a source trigger")
                continuation = (
                    f"{self.emitted_state[current]} -> {wait_state}"
                    f"{self.route_guard(route_code, reset=True)};"
                )
                self.emit_priority_entry(
                    mapping,
                    scope=boundary_scope,
                    line=continuation,
                    generated_role="nested_final_completion_continuation",
                )
            self.mappings.append(mapping)
            self.final_mapped_count += 1
            return

        if (
            self.parent[source] == boundary_scope
            and not self.has_source_children(source)
        ):
            prefix = "!" if self.is_operational_composite(source) else ""
            line = (
                f"{prefix}{self.emitted_state[source]} -> [*]"
                f"{self.trigger(transition)};"
            )
            self.emit(
                mapping,
                scope=boundary_scope,
                line=line,
                generated_role="source_final_transition",
            )
        else:
            current, route_code, triggered = self.emit_source_route_to_scope(
                mapping=mapping,
                transition=transition,
                source=source,
                stop_scope=boundary_scope,
            )
            if not triggered:
                raise RuntimeError("root final route lacks a source trigger")
            suffix = self.route_guard(route_code, reset=True)
            line = (
                f"{self.emitted_state[current]} -> [*]"
                f"{suffix};"
            )
            self.emit_priority_entry(
                mapping,
                scope=boundary_scope,
                line=line,
                generated_role="source_final_transition",
            )
        self.mappings.append(mapping)
        self.final_mapped_count += 1

    def render_same_scope(self, transition: dict[str, Any]) -> None:
        source = transition["source"]
        target = transition["target"]
        scope = self.parent[source]
        mapping = _Mapping(
            transition_id=transition["id"],
            status="mapped",
            reason_code=(
                "R45.MAP.composite_source_routed_sibling"
                if self.has_source_children(source)
                else "R45.MAP.direct_sibling"
            ),
            source=source,
            target=target,
            raw_ref=transition.get("raw_ref"),
        )
        if self.has_source_children(source):
            current, route_code, triggered = self.emit_source_route_to_scope(
                mapping=mapping,
                transition=transition,
                source=source,
                stop_scope=scope,
            )
            if not triggered:
                raise RuntimeError("composite sibling route lacks a source trigger")
            line = (
                f"{self.emitted_state[current]} -> {self.emitted_state[target]}"
                f"{self.route_guard(route_code, reset=True)};"
            )
            self.emit_priority_entry(
                mapping,
                scope=scope,
                line=line,
                generated_role="composite_source_sibling_continuation",
            )
        else:
            prefix = "!" if self.is_operational_composite(source) else ""
            line = (
                f"{prefix}{self.emitted_state[source]} -> {self.emitted_state[target]}"
                f"{self.trigger(transition)};"
            )
            self.emit(
                mapping,
                scope=scope,
                line=line,
                generated_role="source_direct_transition",
            )
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
            mapping = _Mapping(
                transition_id=transition["id"],
                status="mapped",
                reason_code="R45.MAP.composite_to_descendant_routed_reentry",
                source=source,
                target=target,
                raw_ref=transition.get("raw_ref"),
            )
            parent_scope = self.parent[source]
            current, route_code, triggered = self.emit_source_route_to_scope(
                mapping=mapping,
                transition=transition,
                source=source,
                stop_scope=parent_scope,
            )
            if not triggered or current != source:
                raise RuntimeError("composite descendant route lacks leaf triggers")
            continuation = (
                f"{self.emitted_state[source]} -> {self.emitted_state[source]}"
                f"{self.route_guard(route_code)};"
            )
            self.emit_priority_entry(
                mapping,
                scope=parent_scope,
                line=continuation,
                generated_role="composite_source_guarded_reentry",
            )
            self.emit_composite_descendant_target_route(
                mapping=mapping,
                source=source,
                path=path_inside_source,
                route_code=route_code,
            )
            self.add_operational_debt(
                "R45.DEBT.composite_source_external_reentry",
                "A PlantUML transition from a composite source to its descendant is expanded over source leaf activations and re-enters the composite through a protected route token. PlantUML does not define executable local-versus-external transition semantics, so this controller cannot support a source behavior claim.",
                kind="transition_macro",
                transition_id=transition["id"],
                source=source,
                target=target,
                leaf_source_ids=self.source_leaf_descendants(source),
                raw_ref=transition.get("raw_ref"),
            )
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
            current, route_code, triggered = self.emit_source_route_to_scope(
                mapping=mapping,
                transition=transition,
                source=source,
                stop_scope=target,
            )
            exit_suffix = (
                self.route_guard(route_code)
                if triggered
                else self.route_trigger(mapping, transition, route_code)
            )
            exit_line = f"{self.emitted_state[current]} -> [*]{exit_suffix};"
            exit_emitter = self.emit_priority_entry if triggered else self.emit
            exit_emitter(
                mapping,
                scope=target,
                line=exit_line,
                generated_role="ancestor_reentry_child_exit",
            )
            reentry = (
                f"{self.emitted_state[target]} -> {self.emitted_state[target]}"
                f"{self.route_guard(route_code, reset=True)};"
            )
            self.emit_priority_entry(
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
        target_path = target_chain[common:]
        needs_route = (
            self.has_source_children(source)
            or source != source_branch
            or len(target_path) > 1
        )
        if needs_route:
            current, route_code, triggered = self.emit_source_route_to_scope(
                mapping=mapping,
                transition=transition,
                source=source,
                stop_scope=lca_scope,
            )
            if current != source_branch:
                raise RuntimeError("cross-scope route did not reach its source branch")
            continuation_suffix = (
                self.route_guard(
                    route_code,
                    reset=len(target_path) == 1,
                )
                if triggered
                else self.route_trigger(mapping, transition, route_code)
            )
            continuation = (
                f"{self.emitted_state[current]} -> "
                f"{self.emitted_state[target_branch]}{continuation_suffix};"
            )
            continuation_emitter = self.emit_priority_entry if triggered else self.emit
            continuation_emitter(
                mapping,
                scope=lca_scope,
                line=continuation,
                generated_role="cross_scope_parent_continuation",
            )
            if len(target_path) > 1:
                self.emit_target_route(mapping, target_path, route_code)
        else:
            continuation = (
                f"{self.emitted_state[source_branch]} -> "
                f"{self.emitted_state[target_branch]}{self.trigger(transition)};"
            )
            self.emit(
                mapping,
                scope=lca_scope,
                line=continuation,
                generated_role="cross_scope_parent_continuation",
            )
        self.mappings.append(mapping)

    def map_transitions(self) -> None:
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
        mappings_by_transition = {
            mapping.transition_id: mapping for mapping in self.mappings
        }
        for transition in self.transitions:
            kind = transition["attributes"]["transition_kind"]
            mapping = mappings_by_transition.get(transition["id"])
            if (
                mapping is not None
                and mapping.route_code is not None
                and mapping.route_trigger_count > 1
            ):
                self.add_operational_debt(
                    "R45.DEBT.composite_source_activation_dispatch",
                    "A composite-source transition is represented by FCSTM single-active dispatch alternatives that share one protected route code. This does not claim that authored PlantUML orthogonal regions are mutually exclusive; concurrency remains capability-excluded. The dispatch remains compiler-owned and cannot be treated as multiple source transitions.",
                    kind="transition_macro",
                    transition_id=transition["id"],
                    raw_ref=transition.get("raw_ref"),
                    raw_label=transition.get("label"),
                    route_code=mapping.route_code,
                    alternative_trigger_count=mapping.route_trigger_count,
                )
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
                event_id = self.events.get(transition.get("event"))
                event_segment_count = (
                    sum(
                        f"/{event_id}" in emitted["line"]
                        for emitted in mapping.emitted
                    )
                    if mapping is not None and event_id
                    else 0
                )
                if (
                    mapping is not None
                    and mapping.route_code is None
                    and event_segment_count > 1
                ):
                    self.add_operational_debt(
                        "R45.DEBT.multi_segment_event_replay",
                        "One source transition is represented by multiple FCSTM routing segments that repeat the same opaque event to preserve deep/cross-scope target selection. Runtime event-consumption counts from this macro are conversion behavior and cannot support a source issue.",
                        kind="transition_macro",
                        transition_id=transition["id"],
                        raw_ref=transition.get("raw_ref"),
                        raw_label=transition.get("label"),
                        segment_count=len(mapping.emitted),
                        event_segment_count=event_segment_count,
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
        for item in self.canonical.get("metadata", {}).get(
            "orphan_lifecycle_actions", []
        ):
            self.add_operational_debt(
                "R45.DEBT.lifecycle_owner_ambiguous",
                "Bare root-level lifecycle syntax is preserved as root display metadata because the source does not identify an owning state.",
                **item,
            )
        for scope, regions in self.concurrent_regions_by_scope.items():
            self.add_operational_debt(
                "R45.DEBT.concurrent_region_semantics",
                "PlantUML orthogonal-region order and membership are preserved in FCSTM display metadata and trace, but FCSTM has no multi-active-region runtime semantics.",
                kind="concurrent_regions",
                scope=_scope_key(scope),
                region_ids=[item["id"] for item in regions],
                separator_raw_refs=[
                    item.get("raw_ref")
                    for item in self.concurrent_separators_by_scope.get(scope, [])
                ],
            )
        for change in self.source_normalizations:
            self.add_operational_debt(
                "R45.DEBT.source_input_normalization",
                "A narrowly scoped transport repair was applied before parsing; raw and normalized text remain hash-bound in the canonical and comparison trace.",
                kind="source_normalization",
                **change,
            )

    def add_unparsed_blockers(self) -> None:
        for item in self.canonical.get("metadata", {}).get(
            "unparsed_semantic_lines", []
        ):
            self.blockers.append(
                {
                    "kind": "source_line",
                    "reason_code": "R45.BLOCKED.unparsed_semantic_line",
                    "message": "A semantic PlantUML source line has no canonical representation.",
                    **item,
                }
            )

    def render_state(self, state_id: str, indent: int) -> list[str]:
        state = self.state_by_id[state_id]
        emitted = self.emitted_state[state_id]
        label = self.state_display_label(state)
        pad = " " * indent
        pseudo = state.get("kind") in {"fork", "join", "choice", "junction"}
        keyword = "pseudo state" if pseudo else "state"
        composite = self.is_operational_composite(state_id)
        lifecycle = state["attributes"].get("lifecycle_actions", [])
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
            if action["kind"] == "do" and composite:
                lines.append(f"{body_pad}>> during before abstract {action_id};")
            else:
                keyword_action = {"entry": "enter", "do": "during", "exit": "exit"}[
                    action["kind"]
                ]
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
        self.index_initial_transitions()
        self.prepare_missing_initial_helpers()
        self.map_transitions()
        self.complete_composite_route_synthetic_triggers()
        self.add_operational_debts()
        self.add_unparsed_blockers()
        root_label = self.model.get("name") or self.canonical["example_id"]
        for item in self.canonical.get("metadata", {}).get(
            "orphan_lifecycle_actions", []
        ):
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
        for line in self.concurrent_display_lines(None):
            root_label += f"\n{line}"
        for change in self.source_normalizations:
            root_label += (
                f"\n[PlantUML source normalization {change['rule_id']}] "
                f"{change['raw_ref']}: {change['before']} -> {change['after']}"
            )
        lines = []
        if self.route_variable_id is not None:
            lines.append(f"def int {self.route_variable_id} = 0;")
        lines.append(f"state {self.root_id} named {_dsl_string(root_label)} {{")
        pad = " " * 4
        for raw_event, event_id in self.events.items():
            lines.append(f"{pad}event {event_id} named {_dsl_string(raw_event)};")
        for line in self.synthetic_states_by_scope[None]:
            lines.append(f"{pad}{line}")
        for child in self.children[None]:
            lines.extend(self.render_state(child, 4))
        for line in self.lines_by_scope[None]:
            lines.append(f"{pad}{line}")
        lines.append("}")
        fcstm = "\n".join(lines) + "\n"
        for scope, emitted_lines in self.lines_by_scope.items():
            records = self.line_records_by_scope[scope]
            if len(records) != len(emitted_lines):
                raise RuntimeError(
                    f"FCSTM emitted-line ownership drift in scope {_scope_key(scope)}"
                )
            occurrence_by_text: dict[str, int] = defaultdict(int)
            for line, record in zip(emitted_lines, records):
                occurrence_by_text[line] += 1
                record["scope_line_occurrence"] = occurrence_by_text[line]

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
        structural_verdict = (
            "structure_preserved" if not self.blockers else "structure_blocked"
        )
        operational_status = (
            "within_r45_executable_projection"
            if not self.operational_debts
            else "source_ambiguity_or_unsupported_semantics_preserved"
        )
        comparison = {
            "schema_version": "r4_5.plantuml_fcstm_comparison.v4",
            "example_id": self.canonical["example_id"],
            "verdict": structural_verdict,
            "structural_verdict": structural_verdict,
            "operational_status": operational_status,
            "fcstm_execution_eligible": not self.operational_debts
            and not self.blockers,
            "discover_eligible": not self.operational_debts and not self.blockers,
            "source_state_count": len(self.states),
            "emitted_state_count": len(self.emitted_state),
            "state_coverage": f"{len(self.emitted_state)}/{len(self.states)}",
            "source_transition_count": len(self.transitions),
            "mapped_transition_count": len(mapped),
            "blocked_transition_count": len(blocked),
            "silently_dropped_transition_count": len(self.transitions)
            - len(mapped)
            - len(blocked),
            "transition_coverage": f"{len(mapped) + len(blocked)}/{len(self.transitions)}",
            "final_transition_coverage": f"{self.final_mapped_count}/{self.final_source_count}",
            "lifecycle_action_coverage": f"{lifecycle_structurally_mapped}/{lifecycle_total}",
            "abstract_lifecycle_hook_coverage": f"{self.lifecycle_mapped_count}/{lifecycle_total}",
            "body_line_coverage": f"{len(self.body_mappings)}/{body_total}",
            "concurrent_region_coverage": (
                f"{len(self.concurrent_region_mappings)}/{len(self.concurrent_regions)}"
            ),
            "concurrent_region_separator_coverage": (
                f"{len(self.concurrent_region_separator_mappings)}/"
                f"{len(self.concurrent_region_separators)}"
            ),
            "source_normalization_coverage": (
                f"{len(self.source_normalization_mappings)}/"
                f"{len(self.source_normalizations)}"
            ),
            "opaque_label_count": sum(
                1 for transition in self.transitions if transition.get("label")
            ),
            "blockers": self.blockers,
            "operational_debts": self.operational_debts,
            "state_mappings": self.state_mappings,
            "synthetic_state_mappings": self.synthetic_state_mappings,
            "synthetic_transition_mappings": self.synthetic_transition_mappings,
            "event_mappings": self.event_mappings,
            "body_mappings": self.body_mappings,
            "lifecycle_mappings": self.lifecycle_mappings,
            "orphan_lifecycle_mappings": self.orphan_lifecycle_mappings,
            "concurrent_region_mappings": self.concurrent_region_mappings,
            "concurrent_region_separator_mappings": (
                self.concurrent_region_separator_mappings
            ),
            "source_normalization_mappings": self.source_normalization_mappings,
            "route_control": (
                {
                    "fcstm_variable_id": self.route_variable_id,
                    "initial_value": 0,
                    "transition_route_codes": dict(
                        sorted(self.route_transition_codes.items())
                    ),
                    "transition_source_refs": dict(sorted(self.route_source_refs.items())),
                    "policy": "single_event_consumption_guarded_continuation.v1",
                }
                if self.route_variable_id is not None
                else None
            ),
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
                        "raw_label": self.transition_by_id[item.transition_id].get(
                            "label"
                        ),
                        "raw_event": self.transition_by_id[item.transition_id].get(
                            "event"
                        ),
                        "raw_ref": item.raw_ref,
                        "region_index": self.transition_by_id[item.transition_id][
                            "attributes"
                        ].get("region_index", 0),
                    },
                    "transition_id": item.transition_id,
                    "status": item.status,
                    "reason_code": item.reason_code,
                    "source": item.source,
                    "target": item.target,
                    "raw_ref": item.raw_ref,
                    "route_code": item.route_code,
                    "route_trigger_count": item.route_trigger_count,
                    "emitted": item.emitted,
                }
                for item in self.mappings
            ],
        }
        working_contract = build_working_contract(
            canonical=self.canonical,
            fcstm=fcstm,
            comparison=comparison,
        )
        return {
            "fcstm": fcstm,
            "comparison": comparison,
            "name_mapping": self.registry.to_jsonable(),
            "working_contract": working_contract,
            "source_trace_base": working_contract["source_trace_base"],
        }


def lower_plantuml_source(canonical: dict[str, Any]) -> dict[str, Any]:
    """Lower Java source-canonical PlantUML to an auditable FCSTM artifact."""

    if canonical.get("adapter") != "plantuml_java_scope_aware_source":
        raise ValueError("plantuml Java source canonical required")
    return _Lowerer(canonical).render()
