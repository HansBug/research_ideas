"""SL-10 NL-grounded repair-review prompt generator."""

from __future__ import annotations

from typing import Any

from method.stages.sl_prompt_common import fenced_json, fenced_text, message_pack, parse_json_response, require_one_of

SL10_REVIEW_DECISIONS = {"pass", "fail", "rework"}
SL10_REVIEW_RISKS = {"none", "minor", "major"}


def build_sl10_repair_review_prompt(
    *,
    nl: str,
    grounding_map: Any,
    old_dsl: str,
    candidate_dsl: str,
    request_batch: Any,
    sl9_decisions: Any,
    fix_log: list[dict[str, Any]] | None = None,
    diff_summary: dict[str, Any] | None = None,
    local_check_evidence: dict[str, Any] | None = None,
    scenario_summary: dict[str, Any] | None = None,
    prompt_template_version: str = "sl10-repair-review.v1",
) -> list[dict[str, str]]:
    system = f"""
You are SL-10 Repair Review for the project-1 agent loop.
Template version: {prompt_template_version}.

Goal: decide whether the SL-9 repaired DSL can be accepted for the next full
top-down revalidation pass. You MUST ground the decision in the NL
requirements, the complete FixLog ledger, per-request SL-9 decisions, the DSL
diff, and local deterministic check evidence.

Important boundaries:
- Local parse/semantic/design/sim checks are evidence, not your only source of
  truth. If local checks are conservative, decide whether the NL + FixLog
  justify a pass, fail, or rework.
- If you choose "pass" while local_check_evidence reports unresolved targets,
  regression, or drift_risk="major", your evidence MUST explicitly address the
  local rejection reason/kind and explain why the NL + FixLog justify the
  override in `local_override_rationale`. A silent pass, or a pass that merely
  mentions the local reason without a concrete override rationale, is invalid
  and will be downgraded to rework by the runtime consistency gate.
- Read the complete FixLog, including any `repair_memory` blocks. They record
  previous rework objections, repeated candidate hashes, and actionable
  guidance from local checks / prior SL-10 decisions. If you pass a candidate
  after such objections, `local_override_rationale` must explicitly explain why
  the current candidate and SL-9 rationale resolve those remembered objections;
  otherwise request rework with DSL-actionable guidance instead of repeating a
  pure review-format complaint.
- When local_check_evidence includes `actionable_repair_summary` /
  scenario repair briefs, use those expected-vs-actual details in your decision
  and, on rework, translate them into DSL-actionable instructions. Do not only
  say "scenario_regression remains"; name the failing scenario/step, expected
  state/vars, actual state/vars/runtime_error, and the DSL mechanism that must
  change.
- Do not accept a candidate that drops NL-required states, events, guards,
  actions, or scenario obligations.
- For compound command/output obligations, review target-level coverage. If the
  NL requires outputs for multiple target classes, one aggregate grounding id or
  one represented target class is insufficient unless the FixLog/candidate DSL
  contains an admitted-abstraction rationale for omitted targets.
- Do not reject a previously waived/rejected non-hard request again unless new
  evidence shows a regression.
- If you choose rework, provide concrete rework instructions. Rework requests
  are locked: SL-9 must continue repairing them and may not reject them again.

Output schema (STRICT JSON):
{{
  "decision": "pass|fail|rework",
  "target_resolved": true,
  "regression_detected": false,
  "drift_risk": "none|minor|major",
  "evidence": [{{"summary": "why this decision follows from NL/FixLog/local evidence"}}],
  "local_override_rationale": ["required when passing despite major local_check_evidence"],
  "rework_instructions": ["required edits if decision is fail or rework"]
}}
"""
    payload = {
        "nl": nl,
        "grounding_map": grounding_map,
        "request_batch": request_batch,
        "sl9_decisions": sl9_decisions,
        "fix_log": fix_log or [],
        "diff_summary": diff_summary or {},
        "local_check_evidence": local_check_evidence or {},
        "scenario_summary": scenario_summary or {},
    }
    user = f"""
## SL-10 input bundle
{fenced_json(payload)}

## old DSL
{fenced_text(old_dsl, "pyfcstm")}

## candidate DSL
{fenced_text(candidate_dsl, "pyfcstm")}

Return strict JSON only.
"""
    return message_pack(system, user)


def parse_sl10_repair_review_response(content: str) -> dict[str, Any]:
    parsed = parse_json_response(content, context="SL-10")
    # Backward compatibility with older delta-review wording and providers
    # that naturally answer "accept/reject/revise" for a repair candidate.
    legacy_decision = parsed.get("decision")
    if legacy_decision == "accept":
        parsed["decision"] = "pass"
    elif legacy_decision == "reject":
        parsed["decision"] = "fail"
    elif legacy_decision == "revise":
        parsed["decision"] = "rework"
    if "target_resolved" not in parsed:
        parsed["target_resolved"] = parsed.get("decision") == "pass"
    if "regression_detected" not in parsed:
        parsed["regression_detected"] = parsed.get("decision") != "pass"
    if "evidence" not in parsed and "drift_evidence" in parsed:
        parsed["evidence"] = parsed.get("drift_evidence")
    if "rework_instructions" not in parsed and "required_revision" in parsed:
        parsed["rework_instructions"] = parsed.get("required_revision")
    if "local_override_rationale" not in parsed:
        parsed["local_override_rationale"] = []
    parsed["decision"] = require_one_of(parsed.get("decision"), SL10_REVIEW_DECISIONS, "SL-10 decision")
    parsed["drift_risk"] = require_one_of(parsed.get("drift_risk"), SL10_REVIEW_RISKS, "SL-10 drift_risk")
    if not isinstance(parsed.get("target_resolved"), bool):
        raise ValueError("SL-10 target_resolved must be a bool")
    if not isinstance(parsed.get("regression_detected"), bool):
        raise ValueError("SL-10 regression_detected must be a bool")
    evidence = parsed.get("evidence", [])
    if not isinstance(evidence, list):
        raise ValueError("SL-10 evidence must be a list")
    rework = parsed.get("rework_instructions", [])
    if not isinstance(rework, list):
        raise ValueError("SL-10 rework_instructions must be a list")
    override = parsed.get("local_override_rationale", [])
    if not isinstance(override, list):
        raise ValueError("SL-10 local_override_rationale must be a list")
    return parsed
