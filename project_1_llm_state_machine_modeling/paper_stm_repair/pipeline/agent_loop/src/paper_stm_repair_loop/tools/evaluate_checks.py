from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Mapping

from ..controller import bind_discover_drafts
from ..records import sha256_json
from ..schemas import DiscoverCheckDraft
from ..schemas.tools import EvaluateChecksInput, SimpleStructuredTool
from .run_scenarios import execute as run_scenarios
from .validate_discovery_checks import execute as validate_discovery_checks
from .verify_properties import execute as verify_properties
from .verify_static_consistency import execute as verify_static_consistency


def _executed_check_ids(
    validation: Mapping[str, Any],
    scenarios: Mapping[str, Any],
    properties: Mapping[str, Any],
    static: Mapping[str, Any],
) -> set[str]:
    eligible = {
        str(item["check_id"])
        for item in validation.get("checks", [])
        if item.get("mechanically_eligible")
    }
    observed: set[str] = set()
    for group in (
        scenarios.get("scenario_results", []),
        properties.get("property_results", []),
        static.get("static_results", []),
    ):
        for item in group:
            if item.get("execution_status") in {
                "unknown",
                "timeout",
                "incomplete",
                "execution_error",
            }:
                continue
            if item.get("status") not in {"not_implemented", "error"}:
                observed.add(str(item.get("check_id")))
    return eligible & observed


def _gate(
    checks: list[dict[str, Any]],
    binding_rejections: list[dict[str, Any]],
    check_result: Mapping[str, Any],
    validation: Mapping[str, Any],
    scenarios: Mapping[str, Any],
    properties: Mapping[str, Any],
    static: Mapping[str, Any],
    *,
    formal_required: bool,
) -> dict[str, Any]:
    reasons: list[str] = []
    if not check_result.get("executable"):
        reasons.append("fcstm_not_executable")
    if not checks:
        reasons.append("issue_check_preparation_empty")
    if binding_rejections:
        rejected_ids = sorted(
            str(item.get("draft_check_id") or "unknown")
            for item in binding_rejections
        )
        reasons.append("drafts_rejected_or_unbound:" + ",".join(rejected_ids))
    if not validation.get("mechanically_eligible"):
        reasons.append("discovery_checks_not_mechanically_eligible")
    for name, result in (
        ("run_scenarios", scenarios),
        ("verify_properties", properties),
        ("static_consistency", static),
    ):
        if result.get("execution_status") not in {"completed", "not_applicable"}:
            reasons.append(f"{name}_incomplete")
    if formal_required and properties.get("execution_status") == "tool_unavailable":
        reasons.append("required_capability_unavailable:verify_properties")
    executed = _executed_check_ids(validation, scenarios, properties, static)
    required = {
        str(check["check_id"])
        for check in checks
        if check.get("required", True)
    }
    if missing := sorted(required - executed):
        reasons.append("required_checks_not_executed:" + ",".join(missing))
    return {
        "execution_status": "completed",
        "eligible": not reasons,
        "reasons": reasons,
        "executed_check_ids": sorted(executed),
    }


def execute(
    *,
    model_text: str,
    check_result: dict[str, Any],
    checks: list[DiscoverCheckDraft | dict[str, Any]],
    model_path: str = "<frozen>",
    formal_required: bool = True,
) -> dict[str, Any]:
    """Evaluate one complete Discover check-draft batch deterministically.

    This Controller adapter performs no LLM call. It validates the strict draft
    schema, binds labels to the frozen inspect payload, runs scenario/property/
    static checks, validates mechanical eligibility, and returns a transparent
    gate. It does not adjudicate issue roots or mutate the model.
    """

    model_sha256 = str(check_result.get("model_sha256") or "unknown")
    try:
        params = EvaluateChecksInput.model_validate(
            {
                "checks": [
                    item.model_dump(mode="json")
                    if isinstance(item, DiscoverCheckDraft)
                    else item
                    for item in checks
                ]
            }
        )
    except Exception as exc:
        return {
            "execution_status": "invalid_arguments",
            "model_sha256": model_sha256,
            "drafts_sha256": sha256_json(checks),
            "binding_rejections": [],
            "issue_checks": [],
            "validation": {},
            "scenarios": {},
            "properties": {},
            "static_consistency": {},
            "gate": {"eligible": False, "reasons": ["draft_schema_invalid"]},
            "limitations": [
                "invalid_check_draft_batch",
                type(exc).__name__,
                "no_issue_or_quality_verdict",
            ],
        }

    binding_rejections: list[dict[str, Any]] = []
    bound = bind_discover_drafts(
        params.checks,
        check_result.get("inspect", {}),
        binding_rejections=binding_rejections,
    )
    issue_checks = [item.model_dump(mode="json") for item in bound]
    if not issue_checks:
        return {
            "execution_status": "invalid_arguments",
            "model_sha256": model_sha256,
            "drafts_sha256": sha256_json(
                [item.model_dump(mode="json") for item in params.checks]
            ),
            "binding_rejections": binding_rejections,
            "issue_checks": [],
            "validation": {},
            "scenarios": {},
            "properties": {},
            "static_consistency": {},
            "gate": {
                "eligible": False,
                "reasons": ["issue_check_preparation_empty"],
                "executed_check_ids": [],
            },
            "limitations": [
                "all_drafts_rejected_or_unbound",
                "no_issue_or_quality_verdict",
            ],
        }

    scenarios = run_scenarios(model_text, issue_checks, model_path)
    properties = verify_properties(
        model_text,
        issue_checks,
        check_result=check_result,
        model_path=model_path,
    )
    static = verify_static_consistency(issue_checks, check_result=check_result)
    validation = validate_discovery_checks(issue_checks, check_result, properties)
    gate = _gate(
        issue_checks,
        binding_rejections,
        check_result,
        validation,
        scenarios,
        properties,
        static,
        formal_required=formal_required,
    )
    return {
        "execution_status": "completed",
        "model_sha256": model_sha256,
        "drafts_sha256": sha256_json(
            [item.model_dump(mode="json") for item in params.checks]
        ),
        "binding_rejections": binding_rejections,
        "issue_checks": issue_checks,
        "validation": validation,
        "scenarios": scenarios,
        "properties": properties,
        "static_consistency": static,
        "gate": gate,
        "limitations": [
            "bounded_current_model_evidence_only",
            "check_semantic_fidelity_not_proven",
            "coverage_completeness_not_proven",
            "no_issue_or_quality_verdict",
        ],
    }


def build_tool(
    snapshot: dict[str, Any],
    *,
    model_text: str,
    check_result: dict[str, Any],
    model_path: Path,
    formal_required: bool,
    invocation_log: list[dict[str, Any]],
) -> SimpleStructuredTool:
    """Build ``evaluate_checks`` bound to one frozen Discover model/context."""

    frozen_snapshot = copy.deepcopy(snapshot)
    frozen_check_result = copy.deepcopy(check_result)
    frozen_model = str(model_text)
    frozen_path = str(model_path)

    def evaluate_checks(checks: list[DiscoverCheckDraft]) -> dict[str, Any]:
        """Purpose
        -------
        Turn one complete batch of proposed Discover checks into executable,
        bounded evidence inside this single ``AgentApp.run``. Call this after you
        have read the NL, raw/source ``STM_0``, fcstm ``STM_0``, and inspect facts
        and have written explicit expected outcomes. The tool binds and executes
        checks; it never decides whether a root is confirmed/candidate/rejected
        and never edits the model.

        Parameters
        ----------
        ``checks`` is a non-empty JSON array. Every item is strict and contains:

        - ``check_origin``: ``nl_grounded_behavioral_issue`` or
          ``raw_internal_inconsistency``.
        - ``check_id``: Agent-local stable draft identifier, unique in this call.
        - ``check_kind``: ``scenario``, ``property``, or ``static_consistency``.
        - ``statement``: precise claim this check tests, in the run language.
        - ``expected_outcome``: typed expectation fixed before reading this tool's
          execution result. Scenario drafts normally use ``target_label``;
          property drafts use ``property_satisfied`` or ``satisfied``; source
          internal contradictions use ``consistency_status=contradicts``.
        - ``nl_basis``: list of ``{"quote":"...","role":"requirement"}``
          objects. It is required for NL-grounded checks and must be empty for
          raw-internal checks.
        - ``source_basis``: quoted source facts. Raw-internal checks require at
          least two mutually conflicting source facts.
        - ``executable_spec``: scenario ``event_labels``/``events``; property
          ``kind`` + ``target_label`` + bounded ``bound``; or supported static
          shape labels. Do not pass arbitrary code or solver expressions.
        - ``binding_refs``: usually ``[]`` in a draft; deterministic binding fills
          final typed refs.
        - ``required``: boolean, normally true for a proposition you intend to
          adjudicate.

        The strict input accepts no model text, path, run/case ID, URL, shell,
        Python/Z3, reference/gold answer, Repair patch, or extra field.

        Returns
        -------
        A JSON object with:

        - ``execution_status``: ``completed`` or ``invalid_arguments``.
        - ``model_sha256`` and ``drafts_sha256``: identities for the frozen model
          and exact submitted draft batch.
        - ``binding_rejections``: drafts rejected by deterministic origin/binding
          rules, with reasons; these are not issue verdicts.
        - ``issue_checks``: final immutable-style checks with Controller-assigned
          ``CHK-NL-*``/``CHK-SRC-*`` IDs, bound refs/specs, bases, and expectations.
        - ``validation``: per-check mechanical eligibility and bounded obligations.
        - ``scenarios``: expected/actual finite trace results with event accounting.
        - ``properties``: bounded FBMCQ or deterministic state-shape results,
          including witness/replay/status where applicable.
        - ``static_consistency``: deterministic static-shape comparisons.
        - ``gate``: ``eligible``, transparent ``reasons``, and
          ``executed_check_ids``. Eligible means the batch can be adjudicated; it
          does not mean the model or checks are correct.
        - ``limitations``: explicit epistemic boundaries.

        Execution
        ---------
        1. Validate the complete nested draft schema and origin-specific basis.
        2. Bind state/event/transition labels against frozen normalized inspect;
           ambiguous or missing bindings remain rejected/invalid, never guessed.
        3. Execute all bound scenario checks on the frozen model.
        4. Execute property checks through bounded FBMCQ or deterministic
           state-shape evaluation, preserving timeout/unknown/witness/replay.
        5. Execute supported static-consistency checks.
        6. Validate binding/executability/obligations and calculate a transparent
           batch gate. The function performs no LLM call and no model mutation.
        7. Record the exact request/result in the in-memory attempt invocation log
           so the Controller can require the final structured submission to match
           one actually evaluated batch.

        Failure semantics
        -----------------
        Invalid nested schema or an empty/all-rejected batch returns
        ``invalid_arguments`` with ``gate.eligible=false``. Partial/unbound checks,
        unsupported specs, unavailable capability, timeout, unknown, incomplete,
        or replay mismatch remain explicit in their result sections and make a
        required batch ineligible where applicable. A scenario/property that
        completes and contradicts its expectation is a normal behavioral result,
        not a tool crash. Revise only the draft/binding mistake; never alter the
        expected outcome merely to match the observed model.

        Evidence limitations
        --------------------
        Results cover this exact model, draft batch, scenario sequence, static
        shape, and declared formal bound. They do not prove NL faithfulness,
        source closure, completeness, unbounded reachability/unreachability,
        global correctness, issue status, or method effectiveness. Bounded UNSAT
        and no observed counterexample cannot independently confirm absence of a
        behavior. Conversion/lowering differences are not source behavioral
        defects unless independently grounded in source behavior.

        Permissions
        -----------
        The model, inspect, profile, and path are Controller-bound. The Agent has
        no arbitrary paths, alternate model/run/case, network, shell, Python/Z3,
        writes, future Repair/Confirm state, or hidden reference/gold access.
        The tool is behaviorally read-only: it may execute the frozen model but
        cannot publish or mutate it.

        Example
        -------
        ``{"checks":[{"check_origin":"nl_grounded_behavioral_issue","check_id":"draft-1","check_kind":"scenario","statement":"go reaches Done","expected_outcome":{"target_label":"Done"},"source_basis":[],"nl_basis":[{"quote":"When go occurs, enter Done.","role":"requirement"}],"executable_spec":{"event_labels":["go"]},"binding_refs":[],"required":true}]}``
        returns one bound ``CHK-NL-001`` plus scenario, validation, property/static
        sections and a transparent gate tied to the frozen model hash.
        """

        result = execute(
            model_text=frozen_model,
            check_result=frozen_check_result,
            checks=checks,
            model_path=frozen_path,
            formal_required=formal_required,
        )
        invocation_log.append(
            {
                "request": [
                    item.model_dump(mode="json")
                    if isinstance(item, DiscoverCheckDraft)
                    else copy.deepcopy(item)
                    for item in checks
                ],
                "snapshot_sha256": sha256_json(frozen_snapshot),
                "result": copy.deepcopy(result),
            }
        )
        return result

    return SimpleStructuredTool(
        func=evaluate_checks,
        name="evaluate_checks",
        description=evaluate_checks.__doc__ or "evaluate_checks",
        args_schema=EvaluateChecksInput,
    )


__all__ = ["build_tool", "execute"]
