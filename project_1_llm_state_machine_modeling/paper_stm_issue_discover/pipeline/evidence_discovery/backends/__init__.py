from __future__ import annotations

from ..compiler.lowering import PredicatePlan
from ..inputs.models import ModelIR
from ..evidence.receipts import RawReceipt
from .bounded_verification import run_bounded_verification
from .source_static import run_source_static
from .topology import run_topology
from .trajectory import run_trajectory


def run_backend(plan: PredicatePlan, model: ModelIR, receipt_id: str) -> RawReceipt:
    if plan.predicate_id is None or not plan.executable:
        return RawReceipt(
            receipt_id=receipt_id,
            backend="none",
            terminal_state="unsupported",
            verdict="unknown",
            reason="The plan has no sound executable backend; preserve a precise candidate as W1.",
            basis="deterministic backend capability table",
            run_metadata={
                "algorithm_version": "backend-dispatch.v1",
                "failure_kind": "invalid_input" if plan.predicate_id else "unsupported_backend",
            },
        )
    if plan.predicate_id.startswith("S"):
        return run_source_static(plan, model, receipt_id)
    if plan.predicate_id.startswith("G"):
        return run_topology(plan, model, receipt_id)
    if plan.predicate_id.startswith("R"):
        return run_trajectory(plan, model, receipt_id)
    return run_bounded_verification(plan, model, receipt_id)


__all__ = ["run_backend"]
