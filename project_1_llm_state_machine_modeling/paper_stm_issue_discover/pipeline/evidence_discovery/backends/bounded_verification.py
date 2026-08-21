from __future__ import annotations

import hashlib
import re
from typing import Any

from ..compiler.lowering import PredicatePlan
from ..evidence.receipts import RawReceipt
from ..inputs.context import _hierarchical_graph_facts
from ..inputs.models import ModelIR


_COMPARISON = re.compile(r"([A-Za-z_]\w*)\s*(<=|>=|==|<|>)\s*(-?\d+(?:\.\d+)?)")


def _receipt(
    receipt_id: str, predicate: str, model: ModelIR, verdict: str, reason: str, basis: str,
    *,
    counterexample: list[dict[str, Any]] | None = None,
    metadata: dict[str, Any] | None = None,
) -> RawReceipt:
    run_metadata = {
        "algorithm_version": "bounded-checker.v2",
        "input_hash": "sha256:" + hashlib.sha256(model.source_text.encode("utf-8")).hexdigest(),
        "search_bound": "finite_model_graph_or_syntactic_guard",
    }
    if metadata:
        run_metadata.update(metadata)
    return RawReceipt(
        receipt_id=receipt_id,
        backend=f"bounded_verification:{predicate}",
        terminal_state="completed" if verdict in {"true", "false"} else "unknown",
        verdict=verdict,
        reason=reason,
        basis=basis,
        counterexample=counterexample or [],
        run_metadata=run_metadata,
    )


def _guards_disjoint(left: str, right: str) -> bool | None:
    a = _COMPARISON.search(left)
    b = _COMPARISON.search(right)
    if not a or not b or a.group(1) != b.group(1):
        return None
    av, bv = float(a.group(3)), float(b.group(3))
    ao, bo = a.group(2), b.group(2)
    if ao == "==" and bo == "==":
        return av != bv
    if {ao, bo} == {"<", ">="}:
        return (ao == "<" and av <= bv) or (bo == "<" and bv <= av)
    if {ao, bo} == {"<=", ">"}:
        return (ao == "<=" and av < bv) or (bo == "<=" and bv < av)
    return None


def _terminal_states(model: ModelIR) -> set[str]:
    """Return states with an exact formal edge to the final pseudostate."""

    return {transition.source for transition in model.transitions if transition.target == "[*]"}


def run_bounded_verification(plan: PredicatePlan, model: ModelIR, receipt_id: str) -> RawReceipt:
    predicate = plan.predicate_id or "unknown"
    inputs = plan.inputs
    if predicate == "V1":
        guards = [str(value) for value in (inputs.get("guards") or [])]
        if len(guards) < 2:
            return _receipt(receipt_id, predicate, model, "unknown", "V1 requires at least two guards from the same group.", "guard-domain binding incomplete")
        results = [_guards_disjoint(guards[i], guards[j]) for i in range(len(guards)) for j in range(i + 1, len(guards))]
        if any(result is False for result in results):
            return _receipt(receipt_id, predicate, model, "false", "At least two guards may overlap under the parsed numeric constraints.", "bounded syntactic interval comparison", counterexample=[{"guards": guards}])
        if all(result is True for result in results):
            return _receipt(receipt_id, predicate, model, "true", "All parseable guard pairs are disjoint in the declared syntactic domain.", "bounded syntactic interval comparison")
        return _receipt(receipt_id, predicate, model, "unknown", "At least one guard pair is outside the decidable numeric syntax fragment.", "UNKNOWN is preserved for unsupported guard logic")
    if predicate == "V4":
        machine_scope, edges, _roots, _reachability, resolved, reachable_refs = _hierarchical_graph_facts(model)
        state_by_ref = {state.ref: state for state in model.states}
        composite_refs = {
            state.ref
            for state in model.states
            if any(child.parent == state.name for child in model.states)
        }
        outgoing = {
            source_ref: tuple(
                transition_ref
                for _target_ref, transition_ref in edge_rows
            )
            for source_ref, edge_rows in edges.items()
        }
        terminal_refs = {
            source_ref
            for source_ref, target_ref in resolved.values()
            if source_ref is not None and target_ref is None
        }
        requested_refs = {
            str(value)
            for value in (inputs.get("element_refs") or [])
            if str(value) in state_by_ref
        }
        if inputs.get("element_refs") and not requested_refs:
            return _receipt(
                receipt_id,
                predicate,
                model,
                "unknown",
                "V4 scope contains no resolvable closed-model state refs.",
                "exact element_refs scope binding",
                metadata={"scope": inputs.get("initial_scope") or "closed_fcstm_initial_scope", "element_refs": list(inputs.get("element_refs") or [])},
            )
        scope_refs = requested_refs or {
            state.ref
            for state in model.states
            if state.ref != machine_scope and state.ref not in composite_refs
        }
        reachable_scope_refs = scope_refs & reachable_refs
        if requested_refs and not reachable_scope_refs:
            return _receipt(
                receipt_id,
                predicate,
                model,
                "unknown",
                "V4 scope is precisely bound but no requested state is reachable in the finite initial-entry graph.",
                "hierarchical reachability fact; unreachable is not a deadlock verdict",
                metadata={"scope": inputs.get("initial_scope") or "closed_fcstm_initial_scope", "element_refs": sorted(scope_refs), "reachable_state_refs": sorted(reachable_refs)},
            )
        deadlock_refs = sorted(
            state_ref
            for state_ref in reachable_scope_refs
            if state_ref not in terminal_refs
            and state_ref not in composite_refs
            and not outgoing.get(state_ref)
        )
        reachable_names = sorted(state_by_ref[item].name for item in reachable_scope_refs)
        verdict = "false" if deadlock_refs else "true"
        return _receipt(
            receipt_id, predicate, model, verdict,
            f"The bound state scope {'contains' if deadlock_refs else 'contains no'} reachable nonterminal leaves without outgoing progress.",
            "finite hierarchical reachable-state graph; terminality comes only from an exact edge to [*]",
            counterexample=[{"state_ref": node, "state": state_by_ref[node].name} for node in deadlock_refs],
            metadata={
                "reachable_states": reachable_names,
                "reachable_state_refs": sorted(reachable_scope_refs),
                "terminal_state_refs": sorted(terminal_refs),
                "nonterminal_deadlock_states": [state_by_ref[node].name for node in deadlock_refs],
                "nonterminal_deadlock_state_refs": deadlock_refs,
                "scope": inputs.get("initial_scope") or "closed_fcstm_initial_scope",
                "element_refs": sorted(scope_refs),
            },
        )
    return _receipt(receipt_id, predicate, model, "unknown", "The bounded verifier has no decidable implementation branch for this predicate.", "explicit bounded-verification capability boundary")
