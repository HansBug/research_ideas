from __future__ import annotations

import hashlib
from collections import deque
from collections.abc import Sequence
from typing import Any, Iterable

from ..compiler.lowering import PredicatePlan
from ..evidence.receipts import RawReceipt
from ..inputs.context import _machine_scope
from ..inputs.models import ModelIR


def _graph(model: ModelIR) -> dict[str, tuple[str, ...]]:
    graph: dict[str, list[str]] = {}
    machine_scope = _machine_scope(model)

    def aliases(value: str) -> tuple[str, ...]:
        normalized = value.strip().replace("[ * ]", "[*]")
        values = [normalized]
        if normalized.startswith("!"):
            values.append(normalized[1:])
        return tuple(dict.fromkeys(values))

    for transition in model.transitions:
        source = transition.source.strip().replace("[ * ]", "[*]")
        if source == "[*]" and transition.scope not in {None, machine_scope}:
            continue
        for source_alias in aliases(transition.source):
            for target_alias in aliases(transition.target):
                graph.setdefault(source_alias, []).append(target_alias)
        for target_alias in aliases(transition.target):
            graph.setdefault(target_alias, [])
    return {key: tuple(value) for key, value in graph.items()}


def _reachable(graph: dict[str, tuple[str, ...]], roots: Iterable[str]) -> set[str]:
    seen: set[str] = set()
    queue = deque(roots)
    while queue:
        node = queue.popleft()
        if node in seen:
            continue
        seen.add(node)
        queue.extend(graph.get(node, ()))
    return seen


def _can_reach(graph: dict[str, tuple[str, ...]], start: str, target: set[str]) -> bool:
    return bool(_reachable(graph, [start]) & target)


def _receipt(
    receipt_id: str, predicate: str, model: ModelIR, verdict: str, reason: str, basis: str,
    *, counterexample: list[dict[str, Any]] | None = None, trace: list[dict[str, Any]] | None = None,
) -> RawReceipt:
    return RawReceipt(
        receipt_id=receipt_id,
        backend=f"topology:{predicate}",
        terminal_state="completed" if verdict in {"true", "false"} else "unknown",
        verdict=verdict,
        reason=reason,
        basis=basis,
        counterexample=counterexample or [],
        trace=trace or [],
        run_metadata={
            "algorithm_version": "topology-bfs.v1",
            "input_hash": "sha256:" + hashlib.sha256(model.source_text.encode("utf-8")).hexdigest(),
            "closed_graph": True,
        },
    )


def _roots(model: ModelIR) -> tuple[str, ...]:
    machine_scope = _machine_scope(model)
    return tuple(
        item.target
        for item in model.transitions
        if item.source.strip().replace("[ * ]", "[*]") == "[*]"
        and item.scope in {None, machine_scope}
    )


def _nodes(value: object) -> tuple[str, ...]:
    """Normalize scalar or nested node inputs without stringifying containers."""

    if value is None:
        return ()
    if isinstance(value, str):
        return (value,) if value else ()
    if isinstance(value, Sequence):
        nodes: list[str] = []
        for item in value:
            nodes.extend(_nodes(item))
        return tuple(dict.fromkeys(nodes))
    node = str(value)
    return (node,) if node else ()


def run_topology(plan: PredicatePlan, model: ModelIR, receipt_id: str) -> RawReceipt:
    graph = _graph(model)
    inputs = plan.inputs
    predicate = plan.predicate_id or "unknown"
    if predicate == "G1":
        sources = _nodes(inputs.get("sources")) or _nodes(inputs.get("source"))
        targets = set(_nodes(inputs.get("targets")) or _nodes(inputs.get("target")))
        if not sources or not targets:
            return _receipt(receipt_id, predicate, model, "unknown", "G1 is missing a source or target binding.", "required topology inputs")
        reached = _reachable(graph, sources)
        found = sorted(reached & targets)
        verdict = "true" if found else "false"
        return _receipt(
            receipt_id, predicate, model, verdict,
            f"The finite graph {'can' if found else 'cannot'} reach the requested targets from the supplied sources.",
            "finite adjacency BFS over closed FCSTM graph",
            counterexample=[] if found else [{"sources": list(sources), "targets": sorted(targets)}],
            trace=[{"node": node} for node in found],
        )
    if predicate == "G2":
        sources = _nodes(inputs.get("sources")) or _nodes(inputs.get("source")) or _roots(model)
        targets = set(_nodes(inputs.get("targets")) or _nodes(inputs.get("target")))
        if not sources or not targets:
            return _receipt(receipt_id, predicate, model, "unknown", "G2 is missing a source or target-set binding.", "required topology inputs")
        reachable = _reachable(graph, sources)
        bad = sorted(node for node in reachable if not _can_reach(graph, node, targets))
        verdict = "false" if bad else "true"
        return _receipt(
            receipt_id, predicate, model, verdict,
            f"The closed graph {'contains reachable nodes that cannot reach the target' if bad else 'allows every reachable node to reach the target'}.",
            "finite universal reachability over closed graph",
            counterexample=[{"node": node} for node in bad],
        )
    if predicate == "G3":
        source = str(inputs.get("source") or "")
        target = str(inputs.get("target") or "")
        forbidden = set(inputs.get("forbidden") or [])
        if not source or not target:
            return _receipt(receipt_id, predicate, model, "unknown", "G3 is missing a source or target binding.", "required topology inputs")
        queue: deque[tuple[str, tuple[str, ...], bool]] = deque([(source, (source,), source in forbidden)])
        seen: set[tuple[str, bool]] = set()
        safe_path_exists = False
        violating_path: tuple[str, ...] | None = None
        while queue:
            node, path, touched_forbidden = queue.popleft()
            key = (node, touched_forbidden)
            if key in seen:
                continue
            seen.add(key)
            if node == target:
                if touched_forbidden:
                    violating_path = path
                else:
                    safe_path_exists = True
                continue
            for nxt in graph.get(node, ()):
                if nxt not in path:
                    queue.append((nxt, path + (nxt,), touched_forbidden or nxt in forbidden))
        if violating_path is not None:
            verdict = "false"
        elif safe_path_exists:
            verdict = "true"
        else:
            verdict = "unknown"
        return _receipt(
            receipt_id, predicate, model, verdict,
            "Route avoidance was checked over finite simple paths and terminated.",
            "finite route enumeration with explicit forbidden set",
            counterexample=[{"path": list(violating_path), "forbidden": sorted(forbidden)}] if violating_path else [],
        )
    if predicate == "G4":
        roots = _nodes(inputs.get("roots")) or _roots(model)
        marked = set(_nodes(inputs.get("marked")) or _nodes(inputs.get("targets")))
        if not roots or not marked:
            return _receipt(receipt_id, predicate, model, "unknown", "G4 is missing a root or marked-node binding.", "required topology inputs")
        reachable = _reachable(graph, roots)
        bad = sorted(node for node in reachable if not _can_reach(graph, node, marked))
        verdict = "false" if bad else "true"
        return _receipt(
            receipt_id, predicate, model, verdict,
            f"The reachable graph {'contains nodes that cannot reach a marked node' if bad else 'allows every reachable node to reach a marked node'}.",
            "finite coaccessibility over closed graph",
            counterexample=[{"node": node} for node in bad],
        )
    return _receipt(receipt_id, predicate, model, "unknown", "The topology backend has no branch for this predicate.", "explicit topology capability boundary")
