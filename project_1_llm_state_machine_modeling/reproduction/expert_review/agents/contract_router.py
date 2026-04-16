from __future__ import annotations

from langchain_openai import ChatOpenAI

from ..prompts.contract_router import CONTRACT_ROUTER_SYSTEM_PROMPT
from ..schemas.dossiers import ReviewContract
from .llm_helpers import invoke_llm_json


def default_contract(prompt: str) -> ReviewContract:
    lowered = prompt.lower()
    focus: list[str] = []
    for item in [
        "coverage",
        "completeness",
        "behavior",
        "consistency",
        "traceability",
        "clarity",
        "syntax",
        "quality",
        "hallucination",
        "equivalence",
    ]:
        if item in lowered:
            focus.append(item)
    equivalence_rules = [
        "Equivalent but differently structured designs should receive credit when observable behavior is preserved.",
        "Pure surface mismatch is not enough to declare failure.",
    ]
    evidence_rules = [
        "Do not overclaim unsupported errors when evidence is sparse.",
        "Tie every strong judgement to visible evidence from input, prediction, or reference.",
    ]
    strictness = "strict" if any(item in lowered for item in ["strict", "rigorous", "严格"]) else "balanced"
    return ReviewContract(
        task_summary=prompt.strip() or "Review the predicted artifact against the available evidence.",
        requested_focus=focus,
        domain_knowledge=[],
        equivalence_rules=equivalence_rules,
        evidence_rules=evidence_rules,
        strictness=strictness,
        notes=[],
    )


def route_contract(prompt: str, llm: ChatOpenAI | None, notes: list[str]) -> ReviewContract:
    fallback = default_contract(prompt)
    if llm is None:
        return fallback
    payload = invoke_llm_json(
        llm,
        [
            ("system", CONTRACT_ROUTER_SYSTEM_PROMPT),
            (
                "user",
                "Extract a review contract from the prompt.\n\n"
                "Return JSON with keys: task_summary, requested_focus, domain_knowledge, "
                "equivalence_rules, evidence_rules, strictness, notes.\n\n"
                f"Prompt:\n{prompt}",
            ),
        ],
    )
    if not isinstance(payload, dict):
        notes.append("Contract router fell back to deterministic prompt parsing.")
        return fallback
    return ReviewContract(
        task_summary=str(payload.get("task_summary") or fallback.task_summary).strip(),
        requested_focus=[str(item).strip() for item in payload.get("requested_focus", []) if str(item).strip()],
        domain_knowledge=[str(item).strip() for item in payload.get("domain_knowledge", []) if str(item).strip()],
        equivalence_rules=[
            str(item).strip()
            for item in payload.get("equivalence_rules", fallback.equivalence_rules)
            if str(item).strip()
        ],
        evidence_rules=[
            str(item).strip() for item in payload.get("evidence_rules", fallback.evidence_rules) if str(item).strip()
        ],
        strictness=str(payload.get("strictness") or fallback.strictness).strip() or "balanced",
        notes=[str(item).strip() for item in payload.get("notes", []) if str(item).strip()],
    )


__all__ = ["default_contract", "route_contract"]
