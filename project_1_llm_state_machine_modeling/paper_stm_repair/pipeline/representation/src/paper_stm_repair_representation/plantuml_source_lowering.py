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
        self.initial_by_scope: dict[Optional[str], list[dict[str, Any]]] = defaultdict(list)
        self.mapped_initial_scopes: set[Optional[str]] = set()
        self.lifecycle_source_count = 0
        self.lifecycle_mapped_count = 0
        self.final_source_count = 0
        self.final_mapped_count = 0

    def reserve_names(self) -> None:
        for state in self.states:
            parent_scope = self.root_id if state.get("parent") is None else self.emitted_state[state["parent"]]
            self.emitted_state[state["id"]] = self.registry.reserve(
                raw_text=state["attributes"].get("short_name") or state["id"].rsplit(".", 1)[-1],
                canonical_ref=state.get("raw_ref"),
                object_type="state",
                scope=parent_scope,
                generated_reason="qualified_source_state",
                named_text=state.get("label") or state["id"],
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

    def is_composite(self, state_id: str) -> bool:
        return self.state_by_id[state_id].get("kind") == "composite" or bool(self.children[state_id])

    def has_lifecycle_wrapper(self, state_id: str) -> bool:
        return bool(self.state_by_id[state_id]["attributes"].get("lifecycle_actions")) and not self.is_composite(state_id)

    def is_operational_composite(self, state_id: str) -> bool:
        return self.is_composite(state_id) or self.has_lifecycle_wrapper(state_id)

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
            if line not in self.lines_by_scope[parent_state]:
                self.lines_by_scope[parent_state].insert(0, line)
            mapping.emitted.append(
                {
                    "scope": _scope_key(parent_state),
                    "line": line,
                    "generated_role": "cross_scope_target_entry_segment",
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
            self.block_transition(
                transition,
                "R45.BLOCKED.initial_target_not_direct_child",
                "PlantUML initial target is outside its lexical scope.",
            )
            return
        direct_target = target_path[0]
        if (
            len(target_path) == 1
            and self.is_operational_composite(direct_target)
            and not self.has_lifecycle_wrapper(direct_target)
            and not self.has_valid_initial(direct_target)
        ):
            self.block_transition(
                transition,
                "R45.BLOCKED.initial_target_composite_missing_initial",
                "Initial transition targets a composite with no valid explicit child initial; FCSTM cannot enter it without guessing a child.",
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
                self.emit(
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

        prefix = "!" if self.is_operational_composite(source) else ""
        current = source
        while self.parent[current] != boundary_scope:
            parent_scope = self.parent[current]
            suffix = self.trigger(transition)
            line = f"{prefix}{self.emitted_state[current]} -> [*]{suffix};"
            self.emit(mapping, scope=parent_scope, line=line, generated_role="final_exit_segment")
            current = parent_scope
            prefix = ""
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
            elif (
                self.is_operational_composite(transition["target"])
                and not self.has_lifecycle_wrapper(transition["target"])
                and not self.has_valid_initial(transition["target"])
            ):
                self.block_transition(
                    transition,
                    "R45.BLOCKED.target_composite_missing_initial",
                    "Transition targets a composite with no valid explicit PlantUML initial transition; FCSTM cannot enter it to a stable child without guessing.",
                )
            elif self.parent[transition["source"]] == self.parent[transition["target"]]:
                self.render_same_scope(transition)
            else:
                self.render_cross_scope(transition)

    def add_model_blockers(self) -> None:
        unlabeled_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
        initial_by_scope: dict[Optional[str], list[dict[str, Any]]] = defaultdict(list)
        for transition in self.transitions:
            kind = transition["attributes"]["transition_kind"]
            if kind == "normal" and not transition.get("event"):
                unlabeled_by_source[transition["source"]].append(transition)
            elif kind == "initial":
                initial_by_scope[transition.get("scope")].append(transition)
        for source, transitions in unlabeled_by_source.items():
            if len(transitions) < 2:
                continue
            self.blockers.append(
                {
                    "kind": "fan_out",
                    "reason_code": "R45.BLOCKED.ambiguous_unlabeled_fanout",
                    "message": "Multiple unlabeled outgoing edges are preserved structurally, but FCSTM's single-active-state runtime cannot prove nondeterministic or concurrent source semantics.",
                    "source": source,
                    "transition_ids": [item["id"] for item in transitions],
                    "raw_refs": [item.get("raw_ref") for item in transitions],
                }
            )
        for scope, transitions in initial_by_scope.items():
            if len(transitions) < 2:
                continue
            self.blockers.append(
                {
                    "kind": "fan_out",
                    "reason_code": "R45.BLOCKED.multiple_initial_fanout",
                    "message": "Multiple initial edges in one lexical scope are preserved, but cannot be treated as a single FCSTM initial choice or implicit concurrency.",
                    "scope": _scope_key(scope),
                    "transition_ids": [item["id"] for item in transitions],
                    "raw_refs": [item.get("raw_ref") for item in transitions],
                }
            )
        for state in self.states:
            for body_line in state["attributes"].get("body_lines", []):
                self.blockers.append(
                    {
                        "kind": "state_body",
                        "reason_code": "R45.BLOCKED.opaque_state_body_not_executable",
                        "message": "PlantUML state body text is preserved in canonical/source map but has no proven FCSTM executable semantics.",
                        "state_id": state["id"],
                        "raw_ref": body_line.get("raw_ref"),
                        "text": body_line.get("text"),
                    }
                )
            if state.get("kind") in {"fork", "join"}:
                self.blockers.append(
                    {
                        "kind": "state",
                        "reason_code": "R45.BLOCKED.explicit_concurrency_pseudostate",
                        "message": "FCSTM has no orthogonal-region/fork-join operational semantics; node is preserved as pseudo state only.",
                        "state_id": state["id"],
                        "raw_ref": state.get("raw_ref"),
                    }
                )
        for item in self.canonical.get("metadata", {}).get("orphan_lifecycle_actions", []):
            self.blockers.append(
                {
                    "kind": "lifecycle_action",
                    "reason_code": "R45.BLOCKED.lifecycle_owner_ambiguous",
                    "message": "Bare root-level lifecycle syntax has no explicit owning state.",
                    **item,
                }
            )

    def render_state(self, state_id: str, indent: int) -> list[str]:
        state = self.state_by_id[state_id]
        emitted = self.emitted_state[state_id]
        label = state.get("label") or state_id
        pad = " " * indent
        pseudo = state.get("kind") in {"fork", "join", "choice"}
        keyword = "pseudo state" if pseudo else "state"
        composite = self.is_composite(state_id)
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
            self.synthetic_states_by_scope[state_id].append(
                f"state {active_state} named {_dsl_string(f'Active body of {label}')};"
            )
            self.lines_by_scope[state_id].insert(0, f"[*] -> {active_state};")
        if composite:
            initial_lines = [
                line
                for line in self.lines_by_scope[state_id]
                if line.startswith("[*] ->")
            ]
            if state_id not in self.mapped_initial_scopes:
                self.blockers.append(
                    {
                        "kind": "scope",
                        "reason_code": "R45.BLOCKED.missing_explicit_initial",
                        "message": "Composite source state has no valid explicit PlantUML initial transition; generated target-entry routes do not satisfy this source obligation.",
                        "scope": state_id,
                    }
                )
            if not initial_lines:
                synthetic = self.registry.reserve(
                    raw_text="UnspecifiedInitial",
                    canonical_ref=f"canonical:{state_id}:missing_initial",
                    object_type="pseudo_state",
                    scope=emitted,
                    generated_reason="missing_source_initial_fail_closed",
                )
                lines.append(f"{body_pad}pseudo state {synthetic} named \"Unspecified initial\";")
                lines.append(f"{body_pad}[*] -> {synthetic};")
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
        self.add_model_blockers()
        lines = [f"state {self.root_id} named {_dsl_string(self.model.get('name') or self.canonical['example_id'])} {{"]
        pad = " " * 4
        for raw_event, event_id in self.events.items():
            lines.append(f"{pad}event {event_id} named {_dsl_string(raw_event)};")
        root_initial = [line for line in self.lines_by_scope[None] if line.startswith("[*] ->")]
        if None not in self.mapped_initial_scopes:
            self.blockers.append(
                {
                    "kind": "scope",
                    "reason_code": "R45.BLOCKED.missing_explicit_initial",
                    "message": "Root source model has no valid explicit PlantUML initial transition; generated target-entry routes do not satisfy this source obligation.",
                    "scope": "__root__",
                }
            )
        if not root_initial:
            synthetic = self.registry.reserve(
                raw_text="UnspecifiedInitial",
                canonical_ref="canonical:__root__:missing_initial",
                object_type="pseudo_state",
                scope=self.root_id,
                generated_reason="missing_source_initial_fail_closed",
            )
            lines.append(f"{pad}pseudo state {synthetic} named \"Unspecified initial\";")
            lines.append(f"{pad}[*] -> {synthetic};")
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
        verdict = "exact_r45_structure" if not self.blockers else "blocked_unsupported"
        comparison = {
            "schema_version": "r4_5.plantuml_fcstm_comparison.v1",
            "example_id": self.canonical["example_id"],
            "verdict": verdict,
            "discover_eligible": verdict == "exact_r45_structure",
            "source_state_count": len(self.states),
            "emitted_state_count": len(self.emitted_state),
            "state_coverage": f"{len(self.emitted_state)}/{len(self.states)}",
            "source_transition_count": len(self.transitions),
            "mapped_transition_count": len(mapped),
            "blocked_transition_count": len(blocked),
            "silently_dropped_transition_count": len(self.transitions) - len(mapped) - len(blocked),
            "transition_coverage": f"{len(mapped) + len(blocked)}/{len(self.transitions)}",
            "final_transition_coverage": f"{self.final_mapped_count}/{self.final_source_count}",
            "lifecycle_action_coverage": f"{self.lifecycle_mapped_count}/{lifecycle_total}",
            "opaque_label_count": sum(1 for transition in self.transitions if transition.get("label")),
            "blockers": self.blockers,
            "transition_mappings": [
                {
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
