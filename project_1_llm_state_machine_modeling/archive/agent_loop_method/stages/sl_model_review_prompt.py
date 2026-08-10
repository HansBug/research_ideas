"""SL-7 lightweight model review prompt generator."""

from __future__ import annotations

from typing import Any

from method.stages.sl_prompt_common import fenced_json, fenced_text, message_pack, parse_json_response, require_one_of, to_jsonable

MODEL_REVIEW_CATEGORIES: tuple[str, ...] = (
    "nl_fidelity",
    "component_coverage",
    "coverage_gap",
    "over_simplification",
    "unsafe_recovery",
    "structure_smell",
    "unjustified_warning_fix",
    "nfrr_quality_cap",
    "agent_loop_root_cause",
    "path1_eval_risk",
    "path2_grounding_risk",
)
MODEL_REVIEW_DECISIONS = {"pass", "fail", "audit_only", "invalid_output"}
MODEL_REVIEW_RISKS = {"none", "minor", "major"}
FINDING_SEVERITIES = {"info", "minor", "major"}
MAX_REVIEW_LIST_ITEMS = 12
MAX_REVIEW_TEXT_CHARS = 1200


def _clip_text(value: Any, *, limit: int = MAX_REVIEW_TEXT_CHARS) -> Any:
    if not isinstance(value, str) or len(value) <= limit:
        return value
    return value[:limit] + f"...<truncated {len(value) - limit} chars>"


def _clip_value(value: Any, *, list_limit: int = MAX_REVIEW_LIST_ITEMS, text_limit: int = MAX_REVIEW_TEXT_CHARS) -> Any:
    value = to_jsonable(value)
    if isinstance(value, str):
        return _clip_text(value, limit=text_limit)
    if isinstance(value, dict):
        return {str(key): _clip_value(item, list_limit=list_limit, text_limit=text_limit) for key, item in value.items()}
    if isinstance(value, list):
        clipped = [_clip_value(item, list_limit=list_limit, text_limit=text_limit) for item in value[:list_limit]]
        if len(value) > list_limit:
            clipped.append({"_truncated_items": len(value) - list_limit})
        return clipped
    if isinstance(value, tuple):
        return _clip_value(list(value), list_limit=list_limit, text_limit=text_limit)
    return value


def _compact_named_items(items: Any, *, name_keys: tuple[str, ...], limit: int = MAX_REVIEW_LIST_ITEMS) -> list[Any]:
    if not isinstance(items, list):
        return []
    compact: list[Any] = []
    for item in items[:limit]:
        if isinstance(item, dict):
            selected: dict[str, Any] = {}
            for key in name_keys:
                if key in item:
                    selected[key] = _clip_value(item[key], list_limit=4, text_limit=300)
            compact.append(selected or _clip_value(item, list_limit=4, text_limit=300))
        else:
            compact.append(_clip_value(item, list_limit=4, text_limit=300))
    if len(items) > limit:
        compact.append({"_truncated_items": len(items) - limit})
    return compact


def compact_sl7_review_input(
    *,
    inspect_json: dict[str, Any] | None = None,
    design_diagnostics_summary: dict[str, Any] | None = None,
    sim_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a bounded SL-7 input summary for real LLM review.

    SL-7 is a lightweight reviewer, not a second deterministic analyzer.  The
    LLM needs NL/DSL plus representative inspect/design/sim evidence, but a
    full pyfcstm inspect JSON can exceed provider limits for Path2 cases.  This
    summary preserves counts, diagnostic codes, policy actions and samples while
    keeping prompt size stable and making truncation explicit.
    """
    inspect = to_jsonable(inspect_json or {})
    design = to_jsonable(design_diagnostics_summary or {})
    sim = to_jsonable(sim_summary or {})
    inspect = inspect if isinstance(inspect, dict) else {}
    design = design if isinstance(design, dict) else {}
    sim = sim if isinstance(sim, dict) else {}

    inspect_summary = {
        "root_state_path": inspect.get("root_state_path"),
        "metrics": inspect.get("metrics", {}),
        "state_count": len(inspect.get("states", []) or []),
        "transition_count": len(inspect.get("transitions", []) or []),
        "variable_count": len(inspect.get("variables", []) or []),
        "event_count": len(inspect.get("events", []) or []),
        "action_count": len(inspect.get("actions", []) or []),
        "diagnostic_count": len(inspect.get("diagnostics", []) or []),
        "states_sample": _compact_named_items(inspect.get("states", []), name_keys=("path", "name", "kind", "initial", "children")),
        "transitions_sample": _compact_named_items(inspect.get("transitions", []), name_keys=("from", "to", "source", "target", "event", "guard", "action")),
        "variables_sample": _compact_named_items(inspect.get("variables", []), name_keys=("name", "type", "init", "initial", "value")),
        "diagnostics_sample": _compact_named_items(inspect.get("diagnostics", []), name_keys=("code", "severity", "message", "refs")),
    }

    def compact_design_items(key: str) -> list[Any]:
        return _compact_named_items(
            design.get(key, []),
            name_keys=("code", "pyfcstm_severity", "policy_action", "instance_key", "message", "refs", "budget_remaining", "budget_exhausted"),
        )

    design_summary = {
        "ok": design.get("ok"),
        "policy_profile": design.get("policy_profile"),
        "blocking_count": len(design.get("blocking_items", []) or []),
        "advisory_count": len(design.get("advisory_items", []) or []),
        "info_count": len(design.get("info_items", []) or []),
        "inspect_summary": _clip_value(design.get("inspect_summary", {}), list_limit=MAX_REVIEW_LIST_ITEMS, text_limit=500),
        "blocking_items_sample": compact_design_items("blocking_items"),
        "advisory_items_sample": compact_design_items("advisory_items"),
        "info_items_sample": compact_design_items("info_items"),
    }

    sim_results = sim.get("scenario_results", []) or []
    sim_summary_compact = {
        "ok": sim.get("ok"),
        "n_scenarios": sim.get("n_scenarios"),
        "n_scenarios_passed": sim.get("n_scenarios_passed"),
        "setup_error": sim.get("setup_error"),
        "scenario_results_sample": _compact_named_items(sim_results, name_keys=("name", "description", "status", "setup_error", "step_results")),
    }
    return {
        "inspect_model_to_json_summary": inspect_summary,
        "design_diagnostics_summary": design_summary,
        "sim_summary": sim_summary_compact,
    }


def build_sl7_model_review_prompt(
    *,
    nl: str,
    current_dsl: str,
    grounding_map: Any,
    inspect_json: dict[str, Any] | None = None,
    design_diagnostics_summary: dict[str, Any] | None = None,
    sim_summary: dict[str, Any] | None = None,
    five_component_summary: dict[str, Any] | None = None,
    warning_budget_exhausted: list[str] | None = None,
    review_policy: dict[str, Any] | None = None,
    prompt_template_version: str = "sl7-model-review.v1",
) -> list[dict[str, str]]:
    categories = "\n".join(f"- {category}" for category in MODEL_REVIEW_CATEGORIES)
    system = f"""
You are SL-7 Lightweight Model Review for the project-1 agent loop.
Template version: {prompt_template_version}.

Goal: review NL fidelity, component coverage and holistic risk. Supplement
deterministic checks; do not replace SD/SC stages.

NFRR v3 review boundary:
- NFRR v3 is a review rubric, not a deterministic SD hard gate.
- Estimate tier when possible: `T0 unusable`, `T1 diagnostic_only`,
  `T2 within-scope candidate`, `T3 strong reviewed candidate`, `T4 signed reference`.
- Consider FE/NGF/REC/GAS/SCB/AAT/BVS/DMR in finding evidence.
- Run-record completeness or schema validity is not enough; empty-shell /
  low-coverage DSL should receive `nfrr_quality_cap`.

Required finding categories:
{categories}

Output schema (STRICT JSON):
{{
  "decision": "pass|fail|audit_only|invalid_output",
  "risk_level": "none|minor|major",
  "findings": [{{"category": "one listed category", "severity": "info|minor|major", "summary": "...", "evidence": []}}],
  "blocking_findings": [{{"category": "one listed category", "severity": "major", "summary": "...", "evidence": []}}]
}}

Blocking guidance:
- major nl_fidelity and unsafe_recovery findings are blocking.
- path1_eval_risk/path2_grounding_risk are blocking only under matching policy.
- minor structure smells are advisory.
- If the NL says a state is illegal or shall never occur, do not require
  deletion/unreachability as the only valid model. A reachable
  exceptional/diagnostic/fail-safe branch can be an admitted abstraction when it
  explicitly marks the violation, switches to safe outputs, and is not normal
  dispatch/recovery. Keep it blocking only when no diagnostic/fail-safe
  semantics exists.
- major `nfrr_quality_cap` is blocking when the model is T0/T1 because of
  missing required states/transitions/guards/actions, SD-6 failure, weak oracle,
  constant required output without rationale, test-harness
  pollution, or blocking diagnostics.
- Decompose compound outputs by target; aggregate ids are not enough.
- Flag `state_mode_decorative` for `! *` label-only states without mode memory.
- Separate external inputs, internal variables, and pure outputs.
- If you raise a quality C/I concern, include an `agent_loop_root_cause`
  finding. Do not stop at "model quality is poor".
- If the input is insufficient for a safe decision, use `audit_only`.

Required input fields include NL, current DSL, GroundingMap, and the bounded
payload keys `inspect_model_to_json_summary`, `design_diagnostics_summary`,
`sim_summary`, `five_component_summary`, `warning_budget_exhausted` and
`review_policy`.  `_truncated_items` means bounded evidence; use `audit_only`
if it is insufficient.
"""
    compact = compact_sl7_review_input(
        inspect_json=inspect_json,
        design_diagnostics_summary=design_diagnostics_summary,
        sim_summary=sim_summary,
    )
    payload = {
        "nl": nl,
        "current_dsl": current_dsl,
        "grounding_map": grounding_map,
        **compact,
        "five_component_summary": five_component_summary or {},
        "warning_budget_exhausted": warning_budget_exhausted or [],
        "review_policy": review_policy or {},
    }
    user = f"""
## SL-7 review input
{fenced_json(payload)}

Input labels: 5-component summary, warning budget exhausted, ReviewPolicy.

## Current DSL
{fenced_text(current_dsl, "pyfcstm")}

Return strict JSON only.
"""
    return message_pack(system, user)


def _validate_finding(finding: Any, *, field_name: str) -> dict[str, Any]:
    if not isinstance(finding, dict):
        raise TypeError(f"{field_name} entries must be objects")
    category = finding.get("category")
    if category not in MODEL_REVIEW_CATEGORIES:
        raise ValueError(f"unknown SL-7 finding category: {category}")
    require_one_of(finding.get("severity", "info"), FINDING_SEVERITIES, f"{field_name}.severity")
    if not isinstance(finding.get("summary", ""), str):
        raise TypeError(f"{field_name}.summary must be a string")
    return finding


def parse_sl7_model_review_response(content: str) -> dict[str, Any]:
    parsed = parse_json_response(content, context="SL-7")
    parsed["decision"] = require_one_of(parsed.get("decision"), MODEL_REVIEW_DECISIONS, "SL-7 decision")
    parsed["risk_level"] = require_one_of(parsed.get("risk_level"), MODEL_REVIEW_RISKS, "SL-7 risk_level")
    findings = parsed.get("findings", [])
    blocking = parsed.get("blocking_findings", [])
    if not isinstance(findings, list):
        raise ValueError("SL-7 findings must be a list")
    if not isinstance(blocking, list):
        raise ValueError("SL-7 blocking_findings must be a list")
    parsed["findings"] = [_validate_finding(item, field_name="findings") for item in findings]
    parsed["blocking_findings"] = [_validate_finding(item, field_name="blocking_findings") for item in blocking]
    return parsed
