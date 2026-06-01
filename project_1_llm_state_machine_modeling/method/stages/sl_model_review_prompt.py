"""SL-7 lightweight model review prompt generator."""

from __future__ import annotations

from typing import Any

from method.stages.sl_prompt_common import fenced_json, fenced_text, message_pack, parse_json_response, require_one_of

MODEL_REVIEW_CATEGORIES: tuple[str, ...] = (
    "nl_fidelity",
    "component_coverage",
    "coverage_gap",
    "over_simplification",
    "unsafe_recovery",
    "structure_smell",
    "unjustified_warning_fix",
    "path1_eval_risk",
    "path2_grounding_risk",
)
MODEL_REVIEW_DECISIONS = {"pass", "fail", "audit_only", "invalid_output"}
MODEL_REVIEW_RISKS = {"none", "minor", "major"}
FINDING_SEVERITIES = {"info", "minor", "major"}


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

Goal: provide a lightweight code-review-like judgment of NL fidelity,
component coverage and holistic risk.  You supplement deterministic checks; you
do not replace parse/semantic/design/sim/repair-review.

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
- If the input is insufficient for a safe decision, use `audit_only`.

Required input fields include NL, current DSL, GroundingMap, inspect JSON,
design diagnostics summary, sim summary, 5-component summary,
warning budget exhausted list and ReviewPolicy.
"""
    payload = {
        "nl": nl,
        "current_dsl": current_dsl,
        "grounding_map": grounding_map,
        "inspect_model_to_json": inspect_json or {},
        "design_diagnostics_summary": design_diagnostics_summary or {},
        "sim_summary": sim_summary or {},
        "five_component_summary": five_component_summary or {},
        "warning_budget_exhausted": warning_budget_exhausted or [],
        "review_policy": review_policy or {},
    }
    user = f"""
## SL-7 review input
{fenced_json(payload)}

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
