from __future__ import annotations

import hashlib
from typing import Any

from ..compiler.lowering import PredicatePlan
from ..evidence.receipts import RawReceipt
from ..inputs.models import ModelIR, Transition


def _formal_fragment(value: Any) -> str:
    """Return the parser's exact formal fragment without semantic rewriting."""

    return str(value or "").strip()


def _metadata(model: ModelIR) -> dict[str, Any]:
    return {
        "algorithm_version": "source-static-line-parser.v1",
        "input_hash": "sha256:" + hashlib.sha256(model.source_text.encode("utf-8")).hexdigest(),
        "closed_input": True,
    }


def _transition(plan: PredicatePlan, model: ModelIR) -> Transition | None:
    ref = plan.inputs.get("transition_ref") or plan.inputs.get("transition")
    if isinstance(ref, str):
        found = model.transition(ref)
        if found is not None:
            return found
        found = next((item for item in model.transitions if item.label == ref), None)
        if found is not None:
            return found
    refs = plan.inputs.get("element_refs")
    if isinstance(refs, list):
        for ref in refs:
            found = model.transition(ref)
            if found is not None:
                return found
    return None


def _receipt(
    receipt_id: str,
    predicate: str,
    model: ModelIR,
    verdict: str,
    reason: str,
    basis: str,
    *,
    counterexample: list[dict[str, Any]] | None = None,
    trace: list[dict[str, Any]] | None = None,
) -> RawReceipt:
    return RawReceipt(
        receipt_id=receipt_id,
        backend=f"source_static:{predicate}",
        terminal_state="completed" if verdict in {"true", "false"} else "unknown",
        verdict=verdict,
        reason=reason,
        basis=basis,
        counterexample=counterexample or [],
        trace=trace or [],
        run_metadata=_metadata(model),
    )


def run_source_static(plan: PredicatePlan, model: ModelIR, receipt_id: str) -> RawReceipt:
    predicate = plan.predicate_id
    inputs = plan.inputs
    if predicate == "S1":
        element = str(inputs.get("element") or "")
        kind = str(inputs.get("kind") or "state").lower()
        if kind not in {"state", "event", "transition", "edge"}:
            return _receipt(
                receipt_id,
                predicate,
                model,
                "unknown",
                "The S1 kind input is outside the parser's decidable state/event/edge vocabulary.",
                "invalid S1 kind is preserved as UNKNOWN rather than treated as a missing element",
            )
        found = model.state(element) if kind == "state" else model.event(element)
        if found is None and kind in {"transition", "edge"}:
            found = next((item for item in model.transitions if element in {item.ref, item.label}), None)
        verdict = "true" if found is not None else "false"
        return _receipt(
            receipt_id, predicate, model, verdict,
            f"The closed declaration list {'contains' if found else 'does not contain'} the requested {kind} element {element!r}.",
            "ModelIR exact name/ref membership",
            counterexample=[] if found else [{"element": element, "kind": kind}],
        )
    if predicate == "S2":
        transition = _transition(plan, model)
        source = str(inputs.get("source") or (transition.source if transition else ""))
        target = str(inputs.get("target") or (transition.target if transition else ""))
        found = next(
            (item for item in model.transitions if item.source == source and item.target == target),
            None,
        )
        verdict = "true" if found is not None else "false"
        return _receipt(
            receipt_id, predicate, model, verdict,
            f"The closed model {'contains' if found else 'does not contain'} a transition from {source} to {target}.",
            "ModelIR exact transition endpoint membership",
            counterexample=[] if found else [{"source": source, "target": target}],
            trace=[{"transition_ref": found.ref}] if found else [],
        )
    transition = _transition(plan, model)
    if predicate in {"S3", "S5", "S6"} and transition is None:
        return _receipt(
            receipt_id, predicate, model, "unknown",
            "The plan is not bound to a concrete transition, so the static backend cannot soundly decide it.",
            "missing transition binding",
        )
    if predicate == "S3":
        expected = {_formal_fragment(item) for item in inputs.get("triggers", [])}
        observed = {_formal_fragment(item) for item in (transition.triggers if transition else ())}
        verdict = "true" if expected == observed else "false"
        return _receipt(
            receipt_id, predicate, model, verdict,
            "The parsed transition trigger sets were compared for equality.",
            "normalized parsed transition trigger sets",
            counterexample=[] if verdict == "true" else [{"expected": sorted(expected), "observed": sorted(observed)}],
        )
    if predicate == "S4":
        state = model.state(str(inputs.get("state") or ""))
        phase = str(inputs.get("phase") or "entry").lower()
        action = _formal_fragment(inputs.get("action"))
        observed = {_formal_fragment(item) for item in (state.actions.get(phase, ()) if state else ())}
        verdict = "true" if state is not None and action in observed else "false"
        return _receipt(
            receipt_id, predicate, model, verdict,
            f"The action was {'found' if verdict == 'true' else 'not found'} in the {phase} lifecycle slot of the state.",
            "ModelIR state action slot membership",
            counterexample=[] if verdict == "true" else [{"state": inputs.get("state"), "phase": phase, "action": action}],
        )
    if predicate == "S5":
        expected = _formal_fragment(inputs.get("guard"))
        observed = _formal_fragment(transition.guard if transition else None)
        verdict = "true" if expected == observed else "false"
        return _receipt(
            receipt_id, predicate, model, verdict,
            "The normalized requirement guard was compared with the parsed transition guard.",
            "parsed transition guard equality",
            counterexample=[] if verdict == "true" else [{"expected": expected, "observed": observed}],
        )
    if predicate == "S6":
        raw_effects = inputs.get("effects") or inputs.get("effect") or []
        if isinstance(raw_effects, str):
            raw_effects = [raw_effects]
        expected = {_formal_fragment(item) for item in raw_effects}
        observed = {_formal_fragment(item) for item in (transition.effects if transition else ())}
        verdict = "true" if expected <= observed else "false"
        return _receipt(
            receipt_id, predicate, model, verdict,
            "The expected effects were checked for membership in the parsed transition effects.",
            "parsed transition effect membership",
            counterexample=[] if verdict == "true" else [{"expected": sorted(expected), "observed": sorted(observed)}],
        )
    return _receipt(
        receipt_id, predicate or "unknown", model, "unknown",
        "The source-static backend has no implementation branch for this plan.",
        "explicit source-static capability boundary",
    )
