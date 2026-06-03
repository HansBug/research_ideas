"""SL-9 repair prompt generator."""

from __future__ import annotations

from typing import Any

from method.schema import FixPlan, RevisedFixPlan
from method.stages.sl_prompt_common import fenced_json, fenced_text, load_grammar_digest, message_pack


def build_sl9_repair_prompt(
    *,
    nl: str,
    current_dsl: str,
    fix_plan: FixPlan | RevisedFixPlan | dict[str, Any] | None = None,
    grounding_map: Any | None = None,
    selected_diagnostics: list[dict[str, Any]] | None = None,
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
- Do not rewrite event-triggered transitions into chain-scope `: Event`
  transitions merely to satisfy a scenario. In the parseable subset, NL trigger
  names should normally stay as local `:: EventName` transitions; scenario
  paths can use local event names after an initial empty cycle or full
  root-qualified event paths. A repair must not make the DSL less parseable or
  less faithful just to match an over-qualified scenario path.
- Output exactly one complete DSL file. Never splice two copies of the root
  state, never duplicate `state Root {{`/`state System {{`, and never output a
  diff/patch fragment.

Target-aware repair rules:
- If `repair_target` is `parse`, first eliminate all parse diagnostics and do
  not introduce semantic regressions. Use only `def int` / `def float`; encode
  boolean-like flags as int 0/1; do not emit `def bool`, `true`, `false`,
  `!flag`, `//` comments, `/* ... */` comments, event+guard mixed transitions,
  plain `during {{ ... }}` on composite states, C/JavaScript-style `if (expr)`,
  `+=` / `-=` / `*=` / `/=`, or unknown helper calls such as `max(...)`
  / `min(...)` / `ComputeRate(...)`. Use `if [expr] {{ ... }}` and ordinary
  `x = x + 1;` assignments.
- If diagnostics show undeclared event-like names inside guards, do not merely
  declare them as variables. If the NL describes them as triggers/events, encode
  them as `:: EventName` transitions; for alternative events, emit multiple
  transitions instead of `[A || B]`.
- If a parse repair creates or preserves NL-required states, make every required
  state reachable through grounded initial/transition structure before returning
  the candidate; otherwise SD-10 will reject the parse fix as a new blocking
  design diagnostic or missing required grounding.
- If a rejection mentions dangling transitions, forced-transition expansion, or
  unknown target states, repair state scope/path placement rather than merely
  renaming. Root-level forced transitions may only target states resolvable from
  the root scope; nested fallback targets need an enclosing-scope transition or
  an NL-grounded root-level fallback state. Do not leave root-level forced
  transitions pointing at unqualified nested leaves.
- If diagnostics mention `E_DURING_ASPECT_INVALID`, remove plain `during` from
  composite states by moving the action into descendant leaf states or changing
  it to `>> during before/after` as required by pyfcstm.
- If diagnostics are `W_UNWRITTEN_READ_VAR` or `W_GUARD_VARS_NEVER_CHANGE`,
  distinguish external input variables from internal state variables. Do not
  add meaningless self-assignments just to silence the warning. If the variable
  is an external input (sensor/load/environment), prefer documenting that
  modeling choice through grounded structure or using event/effect updates only
  when NL provides them; if it is internal state, add a meaningful NL-grounded
  write. If all guard variables are external inputs, keep the guard and do not
  invent plant dynamics.
- If the selected feedback is simulation failure, inspect whether the scenario
  itself violates pyfcstm execution semantics before editing DSL: default-init scenarios usually need an empty cycle before the first event, and NL/DSL-grounded local
  events such as `StartEvent` or `FaultEvent` can be injected by local name once the source
  leaf is active. Do not change correct `:: Event` transitions into `: Event`
  because of an over-qualified or premature event in the scenario.
- After editing, self-check from scratch: parse syntax, semantic target
  resolution, design target, and preservation of required grounded elements.

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
