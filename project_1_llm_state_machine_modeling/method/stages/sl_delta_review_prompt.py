"""SL-10B delta review prompt generator."""

from __future__ import annotations

from typing import Any

from method.stages.sl_prompt_common import fenced_json, fenced_text, message_pack, parse_json_response, require_one_of

DELTA_REVIEW_DECISIONS = {"accept", "reject", "revise"}
DELTA_REVIEW_RISKS = {"none", "minor", "major"}


def build_sl10b_delta_review_prompt(
    *,
    nl: str,
    grounding_map: Any,
    old_dsl: str,
    candidate_dsl: str,
    fix_plan: Any,
    diff_summary: dict[str, Any] | None = None,
    prompt_template_version: str = "sl10b-delta-review.v1",
) -> list[dict[str, str]]:
    system = f"""
You are SL-10B Delta Review for the project-1 agent loop.
Template version: {prompt_template_version}.

Goal: judge whether a candidate repaired DSL should be accepted, rejected or
revised, focusing on NL-grounded semantic drift.  Deterministic SD-10 checks
remain authoritative for parse/semantic/sim/regression facts.

Output schema (STRICT JSON):
{{
  "decision": "accept|reject|revise",
  "drift_risk": "none|minor|major",
  "drift_evidence": [{{"summary": "evidence item"}}],
  "required_revision": ["required edits if decision is reject or revise"]
}}
"""
    payload = {
        "nl": nl,
        "grounding_map": grounding_map,
        "fix_plan_or_revised_fix_plan": fix_plan,
        "diff summary": diff_summary or {},
    }
    user = f"""
## SL-10B input bundle
{fenced_json(payload)}

## old DSL
{fenced_text(old_dsl, "pyfcstm")}

## candidate DSL
{fenced_text(candidate_dsl, "pyfcstm")}

Return strict JSON only with accept/reject/revise and drift_evidence.
"""
    return message_pack(system, user)


def parse_sl10b_delta_review_response(content: str) -> dict[str, Any]:
    parsed = parse_json_response(content, context="SL-10B")
    parsed["decision"] = require_one_of(parsed.get("decision"), DELTA_REVIEW_DECISIONS, "SL-10B decision")
    parsed["drift_risk"] = require_one_of(parsed.get("drift_risk"), DELTA_REVIEW_RISKS, "SL-10B drift_risk")
    evidence = parsed.get("drift_evidence", [])
    if not isinstance(evidence, list):
        raise ValueError("SL-10B drift_evidence must be a list")
    revisions = parsed.get("required_revision", [])
    if not isinstance(revisions, list):
        raise ValueError("SL-10B required_revision must be a list")
    return parsed
