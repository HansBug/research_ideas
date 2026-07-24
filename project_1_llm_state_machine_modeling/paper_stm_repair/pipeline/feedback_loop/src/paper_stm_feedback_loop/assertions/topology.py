from __future__ import annotations

import copy
from collections import deque
from typing import Any

from pyfcstm.verify.topology import (
    EXIT_ROOT_SINK,
    build_leaf_level_macro_graph,
    strongly_connected_components,
    topological_finite,
    topological_inevitable_terminator,
    topological_reachable_set,
    unreachable_states,
)

from .views import FrozenView


TOPOLOGY_FIELDS = frozenset(
    {
        "initial_closure",
        "unreachable_leaves",
        "strongly_connected_components",
        "dead_ends",
        "root_exit_reachable",
        "topological_finite",
        "topological_inevitable_terminator",
        "guard_agnostic",
        "limitations",
        "states",
        "transitions",
    }
)
PATH_FIELDS = frozenset(
    {
        "exists",
        "nodes",
        "hop_count",
        "transition_refs",
        "source_macro_refs",
        "compiler_owned_nodes",
        "guard_agnostic",
        "limitations",
        "states",
        "events",
        "transitions",
    }
)


def items(inspect_data: dict[str, Any], kind: str) -> list[dict[str, Any]]:
    """Return deterministic copies of structured inspect items for one category."""

    raw = inspect_data.get(kind, [])
    if isinstance(raw, dict):
        values = raw.values()
    elif isinstance(raw, list):
        values = raw
    else:
        values = []
    return [copy.deepcopy(item) for item in values if isinstance(item, dict)]


def is_within(path: str | None, scope: str | None, *, include_self: bool = True) -> bool:
    """Return whether ``path`` is equal to or below ``scope`` in dotted topology."""

    if scope is None:
        return True
    if not isinstance(path, str):
        return False
    if path == scope:
        return include_self
    return path.startswith(scope + ".")


def ref_matches(
    actual: str | None,
    expected: str | None,
    *,
    exact: bool = False,
    suffix: bool = True,
) -> bool:
    """Match a model reference with exact or legacy suffix-compatible semantics."""

    if expected is None:
        return True
    if actual is None:
        return False
    if exact:
        return actual == expected
    return actual == expected or (suffix and actual.endswith("." + expected))


def state_path(row: dict[str, Any]) -> str | None:
    value = row.get("path")
    return value if isinstance(value, str) else None


def event_ref(row: dict[str, Any]) -> str | None:
    value = row.get("qualified_name") or row.get("path") or row.get("name")
    return value if isinstance(value, str) else None


def transition_edge(row: dict[str, Any]) -> dict[str, Any]:
    """Normalize one transition into deterministic source/event/target fields."""

    return {
        "source": row.get("from_path") or row.get("source"),
        "event": row.get("event"),
        "target": row.get("to_path") or row.get("target"),
        "transition_index": row.get("transition_index"),
        "is_forced": bool(row.get("is_forced")),
        **({"edge_kind": row.get("edge_kind")} if row.get("edge_kind") else {}),
    }


def initial_edges(state_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return deterministic virtual edges for structured composite initial targets."""

    edges: list[dict[str, Any]] = []
    for row in state_rows:
        src = row.get("path")
        if not isinstance(src, str):
            continue
        for index, target in enumerate(row.get("initial_targets") or []):
            if not isinstance(target, dict) or not isinstance(target.get("target"), str):
                continue
            edges.append(
                {
                    "source": src,
                    "event": target.get("event"),
                    "target": target.get("target"),
                    "transition_index": f"initial:{src}:{index}",
                    "is_forced": True,
                    "edge_kind": "initial",
                }
            )
    return edges


def cyclic_components(
    nodes: list[str],
    edges: dict[str, tuple[str, ...]],
) -> list[list[str]]:
    """Return deterministic cyclic SCCs for an already scoped induced graph."""

    node_set = set(nodes)
    visited: set[str] = set()
    finish_order: list[str] = []
    for start in sorted(node_set):
        if start in visited:
            continue
        stack = [(start, False)]
        while stack:
            node, expanded = stack.pop()
            if expanded:
                finish_order.append(node)
                continue
            if node in visited:
                continue
            visited.add(node)
            stack.append((node, True))
            successors = [
                item
                for item in edges.get(node, ())
                if item in node_set and item not in visited
            ]
            stack.extend((item, False) for item in reversed(sorted(successors)))

    reverse: dict[str, list[str]] = {node: [] for node in node_set}
    for source in node_set:
        for target in edges.get(source, ()):
            if target in node_set:
                reverse[target].append(source)
    assigned: set[str] = set()
    components: list[list[str]] = []
    for start in reversed(finish_order):
        if start in assigned:
            continue
        component: list[str] = []
        stack = [start]
        assigned.add(start)
        while stack:
            node = stack.pop()
            component.append(node)
            for predecessor in reversed(sorted(reverse.get(node, []))):
                if predecessor not in assigned:
                    assigned.add(predecessor)
                    stack.append(predecessor)
        ordered = sorted(component)
        if len(ordered) > 1 or (
            len(ordered) == 1 and ordered[0] in edges.get(ordered[0], ())
        ):
            components.append(ordered)
    return sorted(components)


class TopologyIndex:
    """Deterministic path/topology backend over frozen structured inspect facts.

    Parameters: ``inspect_data`` is the controller-frozen normalized inspect
    dictionary. The index copies all facts during construction.

    Returns: methods return JSON-like deterministic topology/path records.

    Execution: reads only structured states and transitions already present in
    memory; no model parsing, simulation, filesystem, network, or LLM calls are
    performed.

    Failure semantics: absent facts produce empty records/paths rather than
    guessed topology. Invalid operation policy is enforced by callers.

    Evidence limitations: static topology can describe declared graph shape but
    cannot prove runtime reachability under guards/effects or source alignment.

    Permissions: read-only in-memory inspect access only.

    Example: ``TopologyIndex(inspect).path(source="Root.A", target="Root.B")``
    returns the shortest declared transition path when one exists.
    """

    def __init__(self, inspect_data: dict[str, Any], machine: Any | None = None) -> None:
        self.inspect = copy.deepcopy(inspect_data)
        self.machine = machine
        self.states = sorted(items(self.inspect, "states"), key=lambda row: str(row.get("path") or ""))
        self.transitions = sorted(
            items(self.inspect, "transitions") + items(self.inspect, "forced_transitions") + initial_edges(self.states),
            key=lambda row: (
                str(row.get("from_path") or ""),
                str(row.get("to_path") or ""),
                str(row.get("event") or ""),
                str(row.get("transition_index") or ""),
            ),
        )

    def topology(self, *, within: str | None = None) -> dict[str, Any]:
        state_paths = []
        for row in self.states:
            path = state_path(row)
            if path and is_within(path, within):
                state_paths.append(path)
        state_set = set(state_paths)
        edges = []
        for row in self.transitions:
            edge = transition_edge(row)
            if not isinstance(edge.get("source"), str) or not isinstance(edge.get("target"), str):
                continue
            if within is not None and (edge.get("source") not in state_set or edge.get("target") not in state_set):
                continue
            edges.append(edge)
        if self.machine is None:
            return {
                "initial_closure": [],
                "unreachable_leaves": [],
                "strongly_connected_components": [],
                "dead_ends": [],
                "root_exit_reachable": False,
                "topological_finite": None,
                "topological_inevitable_terminator": None,
                "guard_agnostic": True,
                "limitations": [
                    "normalized_inspect_fallback",
                    "pyfcstm_topology_machine_unavailable",
                    "guards_events_priority_and_effects_not_evaluated",
                ],
                "states": state_paths,
                "transitions": edges,
            }
        graph = build_leaf_level_macro_graph(self.machine)
        root_path = ".".join(self.machine.root_state.path)
        reachability = topological_reachable_set(self.machine)
        initial_closure_all = list(reachability.get(root_path, ()))
        initial_closure = [
            node for node in initial_closure_all if is_within(node, within)
        ]
        dead_ends = sorted(
            node
            for node in initial_closure
            if not graph.edges.get(node, ())
        )
        graph_nodes = sorted(node for node in graph.nodes if is_within(node, within))
        graph_node_set = set(graph_nodes)
        scoped_edges = {
            source: tuple(
                target
                for target in graph.edges.get(source, ())
                if target in graph_node_set
            )
            for source in graph_nodes
        }
        graph_transitions = [
            {"source": source, "target": target}
            for source in sorted(graph.edges)
            for target in sorted(graph.edges[source])
            if within is None or (source in graph_node_set and target in graph_node_set)
        ]
        finite = topological_finite(self.machine) if within is None else None
        inevitable = (
            topological_inevitable_terminator(self.machine)
            if within is None
            else None
        )
        root_exit_reachable = (
            any(
                EXIT_ROOT_SINK in graph.edges.get(node, ())
                for node in {root_path, *initial_closure}
            )
            or self._sink_reachable(initial_closure, graph.edges)
            if within is None
            else False
        )
        return {
            "initial_closure": initial_closure,
            "unreachable_leaves": [
                node
                for node in unreachable_states(self.machine)
                if is_within(node, within)
            ],
            "strongly_connected_components": (
                cyclic_components(graph_nodes, scoped_edges)
                if within is not None
                else [
                    list(component)
                    for component in strongly_connected_components(self.machine)
                ]
            ),
            "dead_ends": dead_ends,
            "root_exit_reachable": root_exit_reachable,
            "topological_finite": (
                {
                    "value": finite.finite,
                    "counterexamples": [
                        list(item) for item in finite.counterexamples
                    ],
                }
                if finite is not None
                else None
            ),
            "topological_inevitable_terminator": (
                {
                    "value": inevitable.inevitable,
                    "counterexample_path": list(
                        inevitable.counterexample_path or ()
                    ),
                }
                if inevitable is not None
                else None
            ),
            "guard_agnostic": True,
            "limitations": [
                "guards_events_priority_and_effects_not_evaluated",
                "positive_path_is_not_runtime_execution_evidence",
                *(
                    [
                        "scoped_topology_global_metrics_not_reported",
                        "scope_boundary_edges_excluded",
                    ]
                    if within is not None
                    else []
                ),
            ],
            "states": graph_nodes,
            "transitions": graph_transitions,
        }

    def path(
        self,
        *,
        source: str,
        target: str,
        event: str | None = None,
        within: str | None = None,
        max_depth: int | None = 8,
        exact: bool = True,
        avoid: tuple[str, ...] = (),
    ) -> list[dict[str, Any]]:
        if max_depth is not None and max_depth < 0:
            return []
        candidate_path_set = set()
        for row in self.states:
            path = state_path(row)
            if path and is_within(path, within):
                candidate_path_set.add(path)
        candidate_paths = sorted(candidate_path_set)
        if self.machine is not None and event is None and within is None:
            candidate_paths = sorted(build_leaf_level_macro_graph(self.machine).nodes)
        resolved_source = self._resolve_path(source, candidate_paths, exact=exact)
        resolved_target = self._resolve_path(target, candidate_paths, exact=exact)
        if resolved_source is None or resolved_target is None:
            return [
                self._empty_path(
                    source,
                    target,
                    (
                        "source_or_target_outside_query_scope"
                        if within is not None
                        else "source_or_target_missing_or_ambiguous_in_query_scope"
                    ),
                )
            ]
        blocked = {
            path
            for value in avoid
            for path in candidate_paths
            if ref_matches(path, value, exact=exact)
        }
        if resolved_source in blocked or resolved_target in blocked:
            return [
                self._empty_path(
                    source,
                    target,
                    "source_or_target_explicitly_avoided",
                )
            ]
        if self.machine is not None and event is None and within is None:
            return [
                self._public_graph_path(
                    source=resolved_source,
                    target=resolved_target,
                    avoid=tuple(sorted(blocked)),
                    max_hops=max_depth,
                )
            ]
        state_paths = set(candidate_paths)
        adjacency: dict[str, list[dict[str, Any]]] = {}
        for row in self.transitions:
            src = row.get("from_path")
            dst = row.get("to_path")
            ev = row.get("event")
            if not isinstance(src, str):
                src = row.get("source")
            if not isinstance(dst, str):
                dst = row.get("target")
            if not isinstance(src, str) or not isinstance(dst, str):
                continue
            if within is not None and (src not in state_paths or dst not in state_paths):
                continue
            if src in blocked or dst in blocked:
                continue
            if (
                event is not None
                and isinstance(ev, str)
                and not ref_matches(ev, event, exact=exact)
            ):
                continue
            adjacency.setdefault(src, []).append(transition_edge(row))
        for edges in adjacency.values():
            edges.sort(key=lambda edge: (str(edge.get("event") or ""), str(edge.get("target") or ""), str(edge.get("transition_index") or "")))
        queue = deque([(resolved_source, [resolved_source], [], False)])
        visited = {(resolved_source, 0, False)}
        results: list[dict[str, Any]] = []
        while queue:
            current, states, edges, matched_event = queue.popleft()
            if current == resolved_target and (event is None or matched_event):
                results.append({"states": states, "events": [edge.get("event") for edge in edges], "transitions": edges})
                break
            if max_depth is not None and len(edges) >= max_depth:
                continue
            for edge in adjacency.get(current, []):
                nxt = edge.get("target")
                if not isinstance(nxt, str):
                    continue
                next_matched_event = matched_event or (
                    event is not None and isinstance(edge.get("event"), str)
                )
                key = (nxt, len(edges) + 1, next_matched_event)
                if key in visited:
                    continue
                visited.add(key)
                queue.append(
                    (nxt, [*states, nxt], [*edges, edge], next_matched_event)
                )
        if results:
            item = results[0]
            item.update(
                {
                    "exists": True,
                    "nodes": list(item["states"]),
                    "hop_count": len(item["transitions"]),
                    "transition_refs": [],
                    "source_macro_refs": [],
                    "compiler_owned_nodes": [],
                    "guard_agnostic": True,
                    "limitations": [
                        "normalized_inspect_fallback",
                        "edge_provenance_unavailable",
                        "positive_path_is_not_runtime_execution_evidence",
                    ],
                }
            )
            return results
        return [self._empty_path(source, target, "no_static_path_within_query_scope")]

    @staticmethod
    def _resolve_path(
        requested: str,
        candidates: list[str],
        *,
        exact: bool,
    ) -> str | None:
        matches = [
            candidate
            for candidate in candidates
            if ref_matches(candidate, requested, exact=exact)
        ]
        return matches[0] if len(matches) == 1 else None

    @staticmethod
    def _sink_reachable(starts: list[str], edges: Any) -> bool:
        queue = deque(starts)
        seen: set[str] = set()
        while queue:
            node = queue.popleft()
            if node == EXIT_ROOT_SINK:
                return True
            if node in seen:
                continue
            seen.add(node)
            queue.extend(edges.get(node, ()))
        return False

    def _public_graph_path(
        self,
        *,
        source: str,
        target: str,
        avoid: tuple[str, ...],
        max_hops: int | None,
    ) -> dict[str, Any]:
        graph = build_leaf_level_macro_graph(self.machine)
        blocked = set(avoid)
        if source in blocked or target in blocked:
            return self._empty_path(source, target, "source_or_target_explicitly_avoided")
        queue = deque([(source, (source,))])
        seen = {source}
        while queue:
            node, nodes = queue.popleft()
            if node == target:
                macro_refs = [
                    {"source": left, "target": right}
                    for left, right in zip(nodes, nodes[1:])
                ]
                return {
                    "exists": True,
                    "nodes": list(nodes),
                    "hop_count": len(nodes) - 1,
                    "transition_refs": [],
                    "source_macro_refs": macro_refs,
                    "compiler_owned_nodes": [
                        item for item in nodes if item == EXIT_ROOT_SINK
                    ],
                    "guard_agnostic": True,
                    "limitations": [
                        "edge_provenance_unavailable",
                        "positive_path_is_not_runtime_execution_evidence",
                    ],
                    "states": list(nodes),
                    "events": [],
                    "transitions": macro_refs,
                }
            hops = len(nodes) - 1
            if max_hops is not None and hops >= max_hops:
                continue
            for successor in sorted(graph.edges.get(node, ())):
                if successor in blocked or successor in seen:
                    continue
                seen.add(successor)
                queue.append((successor, (*nodes, successor)))
        return self._empty_path(source, target, "no_static_path_within_query_scope")

    @staticmethod
    def _empty_path(source: str, target: str, limitation: str) -> dict[str, Any]:
        return {
            "exists": False,
            "nodes": [],
            "hop_count": None,
            "transition_refs": [],
            "source_macro_refs": [],
            "compiler_owned_nodes": [],
            "guard_agnostic": True,
            "limitations": [limitation, "guard_agnostic_structural_absence"],
            "states": [],
            "events": [],
            "transitions": [],
            "requested_source": source,
            "requested_target": target,
        }


class TopologyAPI:
    """Pure eval facade over the public pyfcstm topology algorithms."""

    family = "structure"

    def __init__(self, inspect_data: dict[str, Any], machine: Any) -> None:
        self.index = TopologyIndex(inspect_data, machine)

    def topology(self) -> FrozenView:
        return FrozenView(
            "topology",
            self.index.topology(),
            allowed_fields=TOPOLOGY_FIELDS,
        )

    def path(
        self,
        source: str,
        target: str,
        avoid: tuple[str, ...] = (),
        max_hops: int | None = None,
    ) -> FrozenView:
        result = self.index.path(
            source=source,
            target=target,
            avoid=avoid,
            max_depth=max_hops,
        )[0]
        return FrozenView("topology.path", result, allowed_fields=PATH_FIELDS)


__all__ = [
    "PATH_FIELDS",
    "TOPOLOGY_FIELDS",
    "TopologyAPI",
    "TopologyIndex",
    "event_ref",
    "initial_edges",
    "is_within",
    "items",
    "ref_matches",
    "state_path",
    "transition_edge",
]
