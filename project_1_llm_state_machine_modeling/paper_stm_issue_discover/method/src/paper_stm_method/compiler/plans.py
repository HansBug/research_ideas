from __future__ import annotations

from .lowering import PredicatePlan


def validate_plan(plan: PredicatePlan) -> None:
    if not plan.registry_version.startswith("four-family-19-core."):
        raise ValueError("plan uses a non-frozen registry")
    if plan.executable and (not plan.formal_program or not plan.formal_program_hash):
        raise ValueError("executable plan must carry formal program and hash")
    if plan.executable and not plan.artifact_attribution_complete:
        raise ValueError("executable plan must carry the closed-model attribution identity")
    if plan.formal_program and not plan.formal_program_hash:
        raise ValueError("formal program hash is required")
