from __future__ import annotations

from ..compiler.lowering import PredicatePlan
from ..evidence.receipts import RawReceipt
from ..inputs.models import ModelIR


def run_trajectory(plan: PredicatePlan, model: ModelIR, receipt_id: str) -> RawReceipt:
    predicate = plan.predicate_id or "unknown"
    return RawReceipt(
        receipt_id=receipt_id,
        backend=f"trajectory:{predicate}",
        terminal_state="unsupported",
        verdict="unknown",
        reason="The minimal runtime has no complete scenario, input, and scheduling contract, so no trajectory evidence is generated.",
        basis="trajectory backend boundary: no sound scenario executor in this smoke stage",
        run_metadata={"algorithm_version": "trajectory-boundary.v1", "model_hash": plan.inputs.get("model_hash")},
    )
