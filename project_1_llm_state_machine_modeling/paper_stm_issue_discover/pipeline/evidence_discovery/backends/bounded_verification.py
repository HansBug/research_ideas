from __future__ import annotations

import hashlib
import re
from typing import Any

from ..compiler.lowering import PredicatePlan
from ..evidence.receipts import RawReceipt
from ..inputs.models import ModelIR


_COMPARISON = re.compile(r"([A-Za-z_]\w*)\s*(<=|>=|==|<|>)\s*(-?\d+(?:\.\d+)?)")


def _receipt(
    receipt_id: str, predicate: str, model: ModelIR, verdict: str, reason: str, basis: str,
    *, counterexample: list[dict[str, Any]] | None = None,
) -> RawReceipt:
    return RawReceipt(
        receipt_id=receipt_id,
        backend=f"bounded_verification:{predicate}",
        terminal_state="completed" if verdict in {"true", "false"} else "unknown",
        verdict=verdict,
        reason=reason,
        basis=basis,
        counterexample=counterexample or [],
        run_metadata={
            "algorithm_version": "bounded-checker.v1",
            "input_hash": "sha256:" + hashlib.sha256(model.source_text.encode("utf-8")).hexdigest(),
            "search_bound": "finite_model_graph_or_syntactic_guard",
        },
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
        outgoing: dict[str, int] = {}
        initial = [item.target for item in model.transitions if item.source == "[*]"]
        for transition in model.transitions:
            if transition.source != "[*]":
                outgoing[transition.source] = outgoing.get(transition.source, 0) + 1
        reachable = set(initial)
        changed = True
        while changed:
            changed = False
            for transition in model.transitions:
                if transition.source in reachable and transition.target not in reachable and transition.target != "[*]":
                    reachable.add(transition.target)
                    changed = True
        terminal_states = _terminal_states(model)
        deadlocks = sorted(
            node
            for node in reachable
            if node not in terminal_states and outgoing.get(node, 0) == 0
        )
        verdict = "false" if deadlocks else "true"
        return _receipt(
            receipt_id, predicate, model, verdict,
            f"The reachable stable-state graph {'contains' if deadlocks else 'contains no'} nonterminal nodes without outgoing progress.",
            "finite reachable-state graph deadlock check; terminality comes only from an exact edge to [*]",
            counterexample=[{"state": node} for node in deadlocks],
        )
    return _receipt(receipt_id, predicate, model, "unknown", "The bounded verifier has no decidable implementation branch for this predicate.", "explicit bounded-verification capability boundary")
