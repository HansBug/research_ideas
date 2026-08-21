from __future__ import annotations

from .lowering import PredicatePlan


def validate_plan(plan: PredicatePlan) -> None:
    if not plan.registry_version.startswith("four-family-19-core."):
        raise ValueError("plan uses a non-frozen registry")
    if plan.supported and (not plan.formal_program or not plan.formal_program_hash):
        raise ValueError("supported plan must carry formal program and hash")
    if plan.supported and not plan.source_gate_passed:
        raise ValueError("supported plan must pass the predicate source gate")
    if plan.formal_program and not plan.formal_program_hash:
        raise ValueError("formal program hash is required")
