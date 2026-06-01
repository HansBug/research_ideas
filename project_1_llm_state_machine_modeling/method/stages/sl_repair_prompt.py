"""SL-9 repair prompt generator."""

from __future__ import annotations

from typing import Any

from method.schema import FixPlan, RevisedFixPlan
from method.stages.sl_prompt_common import fenced_json, fenced_text, load_grammar_digest, message_pack, to_jsonable


def build_sl9_repair_prompt(
    *,
    nl: str,
    current_dsl: str,
    fix_plan: FixPlan | RevisedFixPlan | dict[str, Any] | None = None,
    grounding_map: Any | None = None,
    selected_diagnostics: list[dict[str, Any]] | dict[str, Any] | None = None,
    grammar_digest: str | None = None,
    preserve_list: list[str] | None = None,
    scenario_summary: dict[str, Any] | None = None,
    repair_target: str | None = None,
    system_prompt: str | None = None,
    prompt_template_version: str = "sl9-repair.v1",
) -> list[dict[str, str]]:
    grammar = load_grammar_digest(grammar_digest)
    plan_kind = "RevisedFixPlan" if isinstance(fix_plan, RevisedFixPlan) else "FixPlan"
    if fix_plan is None:
        plan_kind = "legacy-focused-feedback"
    base_system = system_prompt or "You are SL-9 Repair for pyfcstm DSL."
    system = f"""
{base_system}

Template version: {prompt_template_version}.

SL-9 Repair contract:
- Input may be a FixPlan or RevisedFixPlan.  If RevisedFixPlan is present,
  preserve the original target and address the RepairRejection evidence.
- `suggested_fix` / `suggested_fix_hints` are a hint, not a command. Prefer a
  globally coherent minimal edit that satisfies NL and verification evidence.
- Preserve NL-grounded required elements in GroundingMap.
- Keep passing scenarios from regressing.
- Output corrected pyfcstm DSL only. No fences, no commentary.

## pyfcstm grammar digest
{grammar}
"""
    payload = {
        "repair_target": repair_target,
        "plan_kind": plan_kind,
        "fix_plan_or_revised_fix_plan": fix_plan,
        "grounding_map": grounding_map,
        "selected_diagnostics": selected_diagnostics or [],
        "preserve_list": preserve_list or [],
        "scenario_summary": scenario_summary or {},
    }
    user = f"""
## NL requirements

{nl.strip()}

## Current DSL
{fenced_text(current_dsl, "pyfcstm")}

## SL-9 structured repair input
{fenced_json(payload)}

Repair the DSL with the smallest safe edit. Output corrected pyfcstm DSL only.
"""
    return message_pack(system, user)
