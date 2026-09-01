"""Topology predicates evaluated by the native FCSTM verification projection."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from ..compiler.lowering import PredicatePlan
from ..inputs.models import ModelIR
from .fcstm_native import (
    NativeFCSTM,
    execute_fbmcq,
    load_native_fcstm,
    native_load_failure,
    native_receipt,
    resolve_state,
    state_path,
)


def _values(value: object) -> tuple[object, ...]:
    """Expose typed scalar/set values without inventing any node identity."""

    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Sequence):
        return tuple(item for nested in value for item in _values(nested))
    return ()


def _native_reachability(native: NativeFCSTM) -> dict[str, tuple[str, ...]]:
    """Run pyfcstm's native hierarchical leaf-level topology projection."""

    from pyfcstm.verify.topology import topological_reachable_set

    return topological_reachable_set(native.machine)


def _leaf_paths_for_binding(
    native: NativeFCSTM,
    value: object,
    *,
    role: str,
) -> tuple[str, ...] | None:
    """Expand exact native root/composite bindings through public topology APIs.

    FCSTM executes leaf configurations.  A root pseudo-state source denotes the
    closed model's initial descent, a composite source denotes its native
    initial descent and continuation set, and a composite target denotes any
    native leaf configuration for which that composite is active.  This is a
    model-class/topology projection, never a ModelIR graph reconstruction.
    """

    from pyfcstm.verify.topology import build_leaf_level_macro_graph

    values = _values(value)
    if not values:
        return None
    graph = build_leaf_level_macro_graph(native.machine)
    reachability = _native_reachability(native)
    root_path = state_path(native.machine.root_state)
    resolved: list[str] = []
    for raw_value in values:
        if raw_value == "[*]":
            if role != "source":
                return None
            resolved.extend(reachability.get(root_path, ()))
            continue
        state = resolve_state(native, raw_value)
        if state is None:
            return None
        path = state_path(state)
        if role == "source" and not state.is_leaf_state:
            resolved.extend(reachability.get(path, ()))
        elif role == "target" and not state.is_leaf_state:
            prefix = path + "."
            resolved.extend(node for node in graph.nodes if node.startswith(prefix))
        else:
            resolved.append(path)
    return tuple(dict.fromkeys(resolved)) or None


def _source_paths(native: NativeFCSTM, value: object) -> tuple[str, ...] | None:
    """Resolve source bindings to FCSTM-executable leaf configurations."""

    return _leaf_paths_for_binding(native, value, role="source")


def _target_paths(native: NativeFCSTM, value: object) -> tuple[str, ...] | None:
    """Resolve target bindings to FCSTM-executable leaf configurations."""

    return _leaf_paths_for_binding(native, value, role="target")


def _bound(native: NativeFCSTM) -> int:
    """Choose a finite native BMC horizon from the frozen FCSTM state space."""

    return max(1, len(tuple(native.machine.walk_states())))


def run_topology(plan: PredicatePlan, model: ModelIR, receipt_id: str):
    """Evaluate G1--G4 with native FCSTM topology or ``.fbmcq`` semantics."""

    predicate = plan.predicate_id or "unknown"
    try:
        native = load_native_fcstm(model)
    except Exception as exc:  # noqa: BLE001 - a failed loader is an execution audit fact.
        return native_load_failure(receipt_id, predicate, model, exc)
    inputs = plan.inputs

    if predicate == "G1":
        sources = _source_paths(native, inputs.get("source"))
        targets = _target_paths(native, inputs.get("target"))
        if not sources or not targets:
            return native_receipt(receipt_id, predicate, native, "unknown", "G1 requires exact native source and target state sets.", "G1 typed node-set contract", backend_family="fcstm_topology", algorithm_version="pyfcstm.verify.topology.v1")
        reachability = _native_reachability(native)
        matches = [
            {"source": source, "target": target}
            for source in sources
            for target in targets
            if target == source or target in reachability.get(source, ())
        ]
        verdict = "true" if matches else "false"
        return native_receipt(receipt_id, predicate, native, verdict, "The native FCSTM leaf-level macro projection was queried for an exact finite source-to-target path.", "pyfcstm.verify.topology.topological_reachable_set", backend_family="fcstm_topology", algorithm_version="pyfcstm.verify.topology.v1", counterexample=[] if matches else [{"sources": list(sources), "targets": list(targets)}], trace=matches)

    if predicate == "G2":
        sources = _source_paths(native, inputs.get("source"))
        targets = _target_paths(native, inputs.get("target"))
        if not sources or not targets or len(sources) != 1:
            return native_receipt(receipt_id, predicate, native, "unknown", "G2 requires exactly one native source and at least one exact target path for a bounded must-reach query.", "G2 typed .fbmcq input contract", backend_family="fbmcq", algorithm_version="pyfcstm.fbmcq.v1")
        source = sources[0]
        target_formula = " || ".join(f'active("{target}")' for target in targets)
        query = f'init state("{source}");\ncheck must_reach <= {_bound(native)}: {target_formula};'
        return execute_fbmcq(receipt_id=receipt_id, predicate=predicate, native=native, query=query, reason="The native FCSTM bounded semantics checked whether every admissible execution from the exact source reaches one requested target within the declared finite horizon.", basis="typed G2 source/target binding and pyfcstm .fbmcq must_reach", timeout_ms=5_000)

    if predicate == "G3":
        sources = _source_paths(native, inputs.get("source"))
        targets = _target_paths(native, inputs.get("target"))
        forbidden = _target_paths(native, inputs.get("forbidden"))
        if not sources or not targets or not forbidden or len(sources) != 1:
            return native_receipt(receipt_id, predicate, native, "unknown", "G3 requires one exact native source, one target set, and a non-empty state-only forbidden set; edge carriers remain outside this native topology fragment.", "G3 typed native route contract", backend_family="fcstm_topology", algorithm_version="pyfcstm.verify.topology.v1")
        resolved = [
            resolve_state(native, value)
            for value in (*sources, *targets, *forbidden)
        ]
        if any(state is None or not state.is_leaf_state for state in resolved):
            return native_receipt(receipt_id, predicate, native, "unknown", "G3 route avoidance is defined here only for exact native leaf-state carriers; composite and edge carriers need a different frozen input fragment.", "pyfcstm.verify.topology LeafLevelGraph carrier boundary", backend_family="fcstm_topology", algorithm_version="pyfcstm.verify.topology.v1")
        source = sources[0]
        reachability = _native_reachability(native)
        routes_through_forbidden = [
            {"forbidden": node, "target": target}
            for node in forbidden
            for target in targets
            if (
                node == source or node in reachability.get(source, ())
            )
            and (
                target == node or target in reachability.get(node, ())
            )
        ]
        verdict = "false" if routes_through_forbidden else "true"
        return native_receipt(receipt_id, predicate, native, verdict, "The native FCSTM leaf-level topology projection checked whether any source-to-target route traverses an exact forbidden state.", "pyfcstm.verify.topology.topological_reachable_set composed over exact source, forbidden, and target leaf paths", backend_family="fcstm_topology", algorithm_version="pyfcstm.verify.topology.v1", counterexample=routes_through_forbidden)

    if predicate == "G4":
        roots = _source_paths(native, inputs.get("roots"))
        marked = _target_paths(native, inputs.get("marked"))
        if not roots or not marked:
            return native_receipt(receipt_id, predicate, native, "unknown", "G4 requires exact native root and marked-state sets.", "G4 typed node-set contract", backend_family="fcstm_topology", algorithm_version="pyfcstm.verify.topology.v1")
        reachability = _native_reachability(native)
        root_reachable = set(roots)
        for root in roots:
            root_reachable.update(reachability.get(root, ()))
        bad = [
            node
            for node in sorted(root_reachable)
            if not any(mark == node or mark in reachability.get(node, ()) for mark in marked)
        ]
        verdict = "false" if bad else "true"
        return native_receipt(receipt_id, predicate, native, verdict, "Every root-reachable native FCSTM node was checked for a finite path to one marked state in the native topology projection.", "pyfcstm.verify.topology.topological_reachable_set", backend_family="fcstm_topology", algorithm_version="pyfcstm.verify.topology.v1", counterexample=[{"node": node, "marked": list(marked)} for node in bad], trace=[{"root": root, "reachable": sorted(root_reachable)} for root in roots])

    return native_receipt(receipt_id, predicate, native, "unknown", "The native topology backend has no branch for this predicate.", "explicit native topology dispatch boundary", backend_family="fcstm_topology", algorithm_version="pyfcstm.verify.topology.v1")


__all__ = ["run_topology"]
