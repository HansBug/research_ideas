"""LangGraph prototype for evidence-carrying issue discovery."""

# ruff: noqa: I001 - importing core first installs the local feedback-loop src path.

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any, Literal, TypedDict

from pydantic import BaseModel, Field, ValidationError
from utils.llm import LLMPricing, estimate_usage_cost_usd

from . import prototype as core

from paper_stm_feedback_loop.common.records import ImmutableRecordStore
from paper_stm_feedback_loop.discover.responder import (
    DEFAULT_TRANSPORT_RETRIES,
    DirectStructuredResponder,
    StructuredOutputValidationError,
)


DEFAULT_MAX_TOTAL_TOKENS = 200_000
DISCOVERY_SAMPLE_COUNT = len(core.DISCOVERY_GROUNDING_AUDIT_LENSES)


class PrototypeGraphInput(BaseModel):
    """Non-secret runtime configuration for one method-generation graph run."""

    case: str = Field(description="Dataset case identifier supplied by the caller; not semantic evidence.")
    profile: str = Field(description="Configured LLM profile name used for method generation.")
    report_root: str | None = Field(
        default=None, description="Optional representation-report root containing the formal input artifacts."
    )
    replay_plans_from: str | None = Field(
        default=None, description="Optional prior run directory used for explicit replay, not fresh discovery."
    )
    matched_x1v2_record: str | None = Field(
        default=None, description="Optional same-model baseline usage record for cost comparison only."
    )
    smt_timeout_ms: int = Field(
        default=3_000, description="Timeout for registered formal guard operations."
    )
    max_total_tokens: int = Field(
        default=DEFAULT_MAX_TOTAL_TOKENS,
        description="Raw method-generation safety cap; provider retries and judge calls are tracked separately.",
    )


class PrototypeGraphState(TypedDict, total=False):
    input: PrototypeGraphInput
    pair: dict[str, Any]
    inspect: dict[str, Any]
    probe_seeds: list[dict[str, Any]]
    progressive_seeds: list[dict[str, Any]]
    contract_context: str
    contract_plan: core.ContractExtractionPlan
    discovery_grounding_context: str
    replay_discovery_grounding_plans: list[core.DiscoveryGroundingPlan]
    discovery_branches: list[dict[str, Any]]
    semantic_grounding_diagnostics: list[dict[str, str]]
    outcomes: list[dict[str, Any]]
    finding_records: list[dict[str, Any]]
    d_context: str
    d_plan: core.DAdjudicationPlan
    d_feedback: list[str]
    d_frozen_decisions: list[dict[str, Any]]
    d_repair_keys: list[str]
    d_repair_output_errors: list[str]
    d_repair_count: int
    d_call_count: int
    d_call_failure: str
    d_fallback_reason: str
    d_unresolved_reason: str
    retry_d: bool
    execution_diagnostics: list[dict[str, str]]
    confirmed_issues: list[dict[str, Any]]
    accepted_issues: list[dict[str, Any]]
    llm_observations: list[dict[str, Any]]
    failure: dict[str, Any]
    final_record: dict[str, Any]


Route = Literal[
    "contract_extraction",
    "discovery_grounding",
    "execute_batch",
    "d_adjudication",
    "validate_d",
    "publish",
    "run_failed",
]


def _completed_call_id(observations: list[dict[str, Any]]) -> str | None:
    for observation in reversed(observations):
        if (
            not isinstance(observation, dict)
            or observation.get("status") != "completed"
        ):
            continue
        call_id = observation.get("llm_call_id")
        if isinstance(call_id, str) and call_id:
            return call_id
    return None


def _failure_class_from_observations(
    observations: list[dict[str, Any]],
    *,
    default: str = "internal",
) -> str:
    """Classify a failed node from responder phases, never exception wording.

    Transport/provider failures are the only retryable class. Structured output
    failures remain visible as schema errors and are never relabelled as provider
    failures merely because the node exhausted its local attempts.
    """

    phases: list[str] = []
    for observation in observations:
        if not isinstance(observation, dict):
            continue
        # A completed observation may contain an earlier failed transport
        # attempt.  That failure was recovered inside this node and must not
        # contaminate classification of a later terminal failure.
        if observation.get("status") == "completed":
            continue
        attempts = observation.get("attempts", [])
        terminal_attempt = next(
            (
                attempt
                for attempt in reversed(attempts)
                if isinstance(attempt, dict)
                and (
                    attempt.get("status") == "failed"
                    or attempt.get("failure_phase") not in {None, "none"}
                )
            ),
            None,
        )
        if terminal_attempt is None:
            continue
        for attempt in (terminal_attempt,):
            if not isinstance(attempt, dict):
                continue
            phase = attempt.get("failure_phase")
            if isinstance(phase, str) and phase != "none":
                phases.append(phase)
    if phases and all(phase in {"provider_response", "transport"} for phase in phases):
        return "provider_failure"
    if phases and all(phase.startswith("structured_") for phase in phases):
        return "schema_invalid"
    if phases:
        return "mixed_failure"
    return default


def _is_whole_cell_failure(failure_class: str) -> bool:
    return failure_class in {"provider_failure", "schema_invalid"}


def _veto_explicit_cross_sample_conflicts(
    plans: list[core.DiscoveryGroundingPlan],
    *,
    canonical_formal_ids: frozenset[str] | None = None,
) -> tuple[list[core.DiscoveryGroundingPlan], list[dict[str, str]]]:
    """Veto true formal disagreements across complementary discovery samples.

    The live model sometimes copies a qualified FCSTM path without the source
    model's pair namespace.  When the canonical AST inventory proves that this
    is one unique path, the two spellings are the same formal identity and are
    canonicalized before conflict detection.  This is structured path identity,
    not a natural-language or keyword heuristic. Ambiguous suffixes remain
    unresolved and are still fail-closed.
    """

    def canonical_id(value: str | None) -> str | None:
        if value is None or canonical_formal_ids is None or value in canonical_formal_ids:
            return value
        parts = tuple(value.split("."))
        matches = [
            candidate
            for candidate in canonical_formal_ids
            if (
                tuple(candidate.split("."))[-len(parts) :] == parts
                or parts[-len(tuple(candidate.split("."))) :] == tuple(candidate.split("."))
            )
        ]
        return matches[0] if len(matches) == 1 else value

    if canonical_formal_ids:
        normalized: list[core.DiscoveryGroundingPlan] = []
        for plan in plans:
            normalized.append(
                plan.model_copy(
                    deep=True,
                    update={
                        "concept_bindings": [
                            binding.model_copy(
                                update={
                                    "source_state_id": canonical_id(binding.source_state_id)
                                }
                            )
                            for binding in plan.concept_bindings
                        ],
                        "transition_group_bindings": [
                            binding.model_copy(
                                deep=True,
                                update={
                                    "source": canonical_id(binding.source),
                                    "targets": [
                                        target.model_copy(
                                            update={
                                                "target": canonical_id(target.target)
                                                or target.target,
                                                "observed_transition_id": canonical_id(
                                                    target.observed_transition_id
                                                ),
                                            }
                                        )
                                        for target in binding.targets
                                    ],
                                },
                            )
                            for binding in plan.transition_group_bindings
                        ],
                    },
                )
            )
        plans = normalized

    if len(plans) < 2:
        return plans, []
    concept_values: dict[str, set[str]] = {}
    for plan in plans:
        for binding in plan.concept_bindings:
            concept_values.setdefault(binding.concept_id, set()).add(
                binding.source_state_id
            )
    conflicts = {
        concept_id: values
        for concept_id, values in concept_values.items()
        if len(values) > 1
    }
    transition_values: dict[
        int, set[tuple[str, str | None, tuple[tuple[int, str, str | None], ...]]]
    ] = {}
    for plan in plans:
        for binding in plan.transition_group_bindings:
            signature = (
                binding.status,
                binding.source,
                tuple(
                    sorted(
                        (
                            target.target_index,
                            target.target,
                            target.observed_transition_id,
                        )
                        for target in binding.targets
                    )
                ),
            )
            transition_values.setdefault(binding.item_index, set()).add(signature)
    transition_conflicts = {
        item_index: values
        for item_index, values in transition_values.items()
        if len(values) > 1
    }
    if not conflicts and not transition_conflicts:
        return plans, []
    updated = []
    for plan in plans:
        unresolved = list(plan.unresolved)
        for concept_id in sorted(conflicts):
            unresolved.append(
                core.SemanticGroundingGap(
                    scope="contract",
                    item_index=0,
                    field=f"concept_bindings[{concept_id}]",
                    reason=(
                        "independent discovery samples supplied conflicting exact "
                        "formal IDs; the ensemble withheld this binding"
                    ),
                )
            )
        for item_index in sorted(transition_conflicts):
            unresolved.append(
                core.SemanticGroundingGap(
                    scope="contract",
                    item_index=item_index,
                    field=f"transition_group_bindings[{item_index}]",
                    reason=(
                        "independent discovery samples supplied conflicting exact "
                        "transition bindings; the ensemble withheld execution"
                    ),
                )
            )
        updated.append(
            plan.model_copy(
                deep=True,
                update={
                    "concept_bindings": [
                        binding
                        for binding in plan.concept_bindings
                        if binding.concept_id not in conflicts
                    ],
                    "transition_group_bindings": [
                        (
                            core.TransitionGroupGrounding(
                                item_index=binding.item_index,
                                status="unresolved",
                                reason=(
                                    "independent discovery samples supplied "
                                    "conflicting exact transition bindings"
                                ),
                            )
                            if binding.item_index in transition_conflicts
                            else binding
                        )
                        for binding in plan.transition_group_bindings
                    ],
                    "unresolved": unresolved,
                },
            )
        )
    diagnostics = [
        {
            "stage": "discovery_ensemble",
            "class": "cross_sample_formal_binding_conflict",
            "message": (
                f"{concept_id} received conflicting exact IDs {sorted(values)} and "
                "was withheld from execution"
            ),
        }
        for concept_id, values in sorted(conflicts.items())
    ]
    diagnostics.extend(
        {
            "stage": "discovery_ensemble",
            "class": "cross_sample_transition_binding_conflict",
            "message": (
                f"transition_group[{item_index}] received conflicting exact "
                "bindings and was retained only as an unexecuted coverage gap"
            ),
        }
        for item_index in sorted(transition_conflicts)
    )
    return updated, diagnostics


def _fresh_transition_binding_errors(
    raw: core.ContractExtractionPlan,
    plan: core.DiscoveryGroundingPlan,
) -> list[str]:
    """Check only the deterministic shape of fresh transition resolutions."""

    errors: list[str] = []
    grouped: dict[int, list[core.TransitionGroupGrounding]] = {}
    for binding in plan.transition_group_bindings:
        grouped.setdefault(binding.item_index, []).append(binding)
    expected = set(range(len(raw.transition_groups)))
    supplied = set(grouped)
    for item_index in sorted(expected - supplied):
        errors.append(f"transition_group[{item_index}] resolution is missing")
    for item_index in sorted(supplied - expected):
        errors.append(f"transition_group[{item_index}] does not exist in the raw plan")
    for item_index in sorted(expected & supplied):
        rows = grouped[item_index]
        if len(rows) != 1:
            errors.append(
                f"transition_group[{item_index}] has {len(rows)} resolutions; expected 1"
            )
            continue
        binding = rows[0]
        if binding.status != "grounded":
            if binding.source is not None or binding.targets:
                errors.append(
                    f"transition_group[{item_index}] {binding.status} resolution "
                    "must not carry formal bindings"
                )
            continue
        if binding.source is None:
            errors.append(f"transition_group[{item_index}] grounded source is missing")
        target_rows: dict[int, int] = {}
        for target in binding.targets:
            target_rows[target.target_index] = (
                target_rows.get(target.target_index, 0) + 1
            )
        expected_targets = set(range(len(raw.transition_groups[item_index].targets)))
        supplied_targets = set(target_rows)
        for target_index in sorted(expected_targets - supplied_targets):
            errors.append(
                f"transition_group[{item_index}].targets[{target_index}] is missing"
            )
        for target_index in sorted(supplied_targets - expected_targets):
            errors.append(
                f"transition_group[{item_index}].targets[{target_index}] does not exist"
            )
        for target_index, count in sorted(target_rows.items()):
            if count != 1:
                errors.append(
                    f"transition_group[{item_index}].targets[{target_index}] has "
                    f"{count} resolutions; expected 1"
                )
    return errors


def _partition_d_decisions(
    findings: list[dict[str, Any]],
    plan: core.DAdjudicationPlan,
) -> tuple[dict[str, core.DDecision], dict[str, list[str]], list[str]]:
    """Freeze valid D decisions and identify only the subset needing LLM repair."""

    expected = {finding["finding_key"]: finding for finding in findings}
    ordered_keys = [
        finding["finding_key"]
        for finding in sorted(findings, key=core.d_finding_sort_key)
    ]
    positions = {finding_key: index for index, finding_key in enumerate(ordered_keys)}
    grouped: dict[str, list[core.DDecision]] = {}
    for decision in plan.decisions:
        grouped.setdefault(decision.finding_key, []).append(decision)
    unexpected = sorted(set(grouped) - set(expected))
    if unexpected:
        message = (
            "D plan contains unexpected finding_key values "
            f"{unexpected!r}; the whole D plan is contract-invalid"
        )
        return {}, {finding_key: [message] for finding_key in expected}, []
    valid: dict[str, core.DDecision] = {}
    invalid: dict[str, list[str]] = {}
    for finding_key, finding in expected.items():
        decisions = grouped.get(finding_key, [])
        if len(decisions) != 1:
            invalid[finding_key] = [
                f"expected exactly one decision, received {len(decisions)}"
            ]
            continue
        raw_decision = decisions[0]
        duplicate_of = raw_decision.duplicate_of
        duplicate_errors: list[str] = []
        if duplicate_of is not None:
            if duplicate_of not in expected:
                duplicate_errors.append(
                    "duplicate_of must reference a supplied finding_key"
                )
            elif positions[duplicate_of] >= positions[finding_key]:
                eligible_earlier_keys = ordered_keys[: positions[finding_key]]
                duplicate_errors.append(
                    "duplicate_of must reference an earlier stable finding_key; "
                    f"eligible earlier keys={eligible_earlier_keys!r}; use null "
                    "when none is semantically identical"
                )
            else:
                duplicate_errors.extend(
                    core.validate_duplicate_reference(finding, expected[duplicate_of])
                )
            if not raw_decision.duplicate_rationale:
                duplicate_errors.append("duplicate_of requires duplicate_rationale")
        elif raw_decision.duplicate_rationale is not None:
            duplicate_errors.append("duplicate_rationale requires duplicate_of")

        decision = core.normalize_d_decision(raw_decision, finding=finding)
        errors = [
            *core.validate_d_decision(finding, decision),
            *duplicate_errors,
        ]
        if errors:
            invalid[finding_key] = errors
        else:
            valid[finding_key] = decision
    return valid, invalid, []


def _validate_targeted_d_repair_output(
    plan: core.DAdjudicationPlan,
    *,
    repair_keys: list[str],
    frozen_keys: set[str],
) -> tuple[list[core.DDecision], list[str]]:
    """Accept only an exact repair subset before it can join frozen decisions."""

    expected_keys = set(repair_keys)
    errors: list[str] = []
    if len(expected_keys) != len(repair_keys):
        errors.append("targeted repair keys must be unique")
    overlap = sorted(expected_keys & frozen_keys)
    if overlap:
        errors.append(
            f"targeted repair keys overlap frozen finding_key values {overlap!r}"
        )

    grouped: dict[str, list[core.DDecision]] = {}
    for decision in plan.decisions:
        grouped.setdefault(decision.finding_key, []).append(decision)
    for finding_key in repair_keys:
        count = len(grouped.get(finding_key, []))
        if count != 1:
            errors.append(
                "targeted repair must return exactly one decision for repair "
                f"finding_key {finding_key!r}; received {count}"
            )
    for finding_key in sorted(set(grouped) & frozen_keys):
        errors.append(
            f"targeted repair must not repeat frozen finding_key {finding_key!r}"
        )
    for finding_key in sorted(set(grouped) - expected_keys - frozen_keys):
        errors.append(f"targeted repair returned unknown finding_key {finding_key!r}")
    if errors:
        return [], errors
    return [grouped[finding_key][0] for finding_key in repair_keys], []


def _partially_adjudicated_findings(
    findings: list[dict[str, Any]],
    valid: dict[str, core.DDecision],
    invalid: dict[str, list[str]],
) -> list[dict[str, Any]]:
    def fallback_decision(finding_key: str, errors: list[str]) -> core.DDecision:
        """Keep every finding typed when D cannot be repaired.

        D0 is the protocol's internal fail-safe: it is retained for audit and
        excluded from the release boundary, while a structured error records
        why semantic adjudication did not establish D1/D2.
        """

        detail = "; ".join(errors) or "D decision is unavailable"
        return core.DDecision(
            finding_key=finding_key,
            grounding="none",
            violated_obligation="D adjudication did not establish a publishable obligation.",
            strongest_defeater=detail,
            defeater_kind="undercutting",
            defeater_disposition="unresolved",
            rationale=(
                "Conservative D0 fallback after bounded adjudication/repair: "
                + detail
            ),
            d_subclass="not_applicable",
            d_level="D0",
            duplicate_of=None,
            duplicate_rationale=None,
        )

    adjudicated = []
    for finding in findings:
        item = dict(finding)
        finding_key = finding["finding_key"]
        decision = valid.get(finding_key)
        if decision is None:
            errors = invalid.get(finding_key, ["D decision is unavailable"])
            item["d_decision"] = fallback_decision(finding_key, errors).model_dump(
                mode="json"
            )
            item["d_validation_errors"] = errors
            item["d_fallback"] = True
            item["d_status"] = "D0_FALLBACK"
        else:
            item["d_decision"] = decision.model_dump(mode="json")
            item["d_validation_errors"] = []
            item["d_fallback"] = False
            item["d_status"] = decision.d_level
        adjudicated.append(item)
    return adjudicated


def _quarantine_untyped_fresh_evidence(
    evidence: core.IssueDiscoveryPlan,
) -> tuple[core.IssueDiscoveryPlan, list[dict[str, str]]]:
    """Exclude fresh candidates that bypass the paper-level typed surface."""

    diagnostics: list[dict[str, str]] = []
    lanes: dict[str, list[core.BalancedEvidenceCandidate]] = {}
    for lane in ("surface_candidates", "behavior_candidates"):
        kept = []
        for item_index, candidate in enumerate(getattr(evidence, lane)):
            if candidate.domain_obligation is None:
                diagnostics.append(
                    {
                        "stage": "discovery_grounding",
                        "class": "fresh_typed_obligation_missing",
                        "message": (
                            f"{lane}[{item_index}] was quarantined because fresh "
                            "candidates require a paper-level typed obligation"
                        ),
                    }
                )
                continue
            if not candidate.observed_fact.strip():
                diagnostics.append(
                    {
                        "stage": "discovery_grounding",
                        "class": "fresh_observed_fact_missing",
                        "message": (
                            f"{lane}[{item_index}] omitted the audit-only "
                            "observed_fact; the typed formal goal remains eligible "
                            "for execution, but the omission is retained for audit"
                        ),
                    }
                )
            kept.append(candidate)
        lanes[lane] = kept
    return core.IssueDiscoveryPlan(**lanes), diagnostics


def _observation(responder: DirectStructuredResponder) -> dict[str, Any] | None:
    value = responder.take_last_observation()
    return core._jsonable(value) if value is not None else None


def _invoke_with_schema_repair(
    responder: DirectStructuredResponder,
    *,
    role: str,
    schema: type[BaseModel],
    system_prompt: str,
    user_input: str,
) -> tuple[BaseModel | None, list[dict[str, Any]], Exception | None]:
    observations: list[dict[str, Any]] = []
    first_error_text = ""
    try:
        value = responder.invoke_structured(
            role=role,
            schema=schema,
            system_prompt=system_prompt,
            user_input=user_input,
        )
        observation = _observation(responder)
        if observation:
            observations.append(observation)
        return value, observations, None
    except Exception as first_error:  # noqa: BLE001 - classified below
        first_error_text = f"{type(first_error).__name__}: {first_error}"
        observation = _observation(responder)
        if observation:
            observations.append(observation)
        if not isinstance(
            first_error, (StructuredOutputValidationError, ValidationError)
        ):
            return None, observations, first_error
    repair_input = (
        f"{user_input}\n\n# Structured-output repair feedback\n\n"
        "The previous output was rejected by the exact schema. Return the same "
        "semantic answer with these structural errors corrected; do not add new "
        f"findings or change valid content.\n\n{first_error_text}"
    )
    try:
        value = responder.invoke_structured(
            role=role,
            schema=schema,
            system_prompt=system_prompt,
            user_input=repair_input,
        )
        observation = _observation(responder)
        if observation:
            observations.append(observation)
        return value, observations, None
    except Exception as second_error:  # noqa: BLE001 - terminal schema escape hatch
        observation = _observation(responder)
        if observation:
            observations.append(observation)
        return None, observations, second_error


def _contract_plan_is_empty(plan: core.ContractExtractionPlan) -> bool:
    """Return whether the structured extractor emitted no contract of any kind."""

    return not any(
        (
            plan.initial_contracts,
            plan.containment_contracts,
            plan.transition_groups,
            plan.required_state_contracts,
            plan.required_event_scope_contracts,
            plan.required_action_contracts,
        )
    )


def _usage_budget(
    observations: list[dict[str, Any]],
    max_total_tokens: int,
    matched_x1v2_record: str | None = None,
) -> dict[str, Any]:
    totals = []
    input_totals = []
    output_totals = []
    unavailable = 0
    for observation in observations:
        usage = observation.get("usage") if isinstance(observation, dict) else None
        total = usage.get("total_tokens") if isinstance(usage, dict) else None
        input_tokens = usage.get("input_tokens") if isinstance(usage, dict) else None
        output_tokens = usage.get("output_tokens") if isinstance(usage, dict) else None
        if all(
            isinstance(value, int) for value in (total, input_tokens, output_tokens)
        ):
            totals.append(total)
            input_totals.append(input_tokens)
            output_totals.append(output_tokens)
        else:
            unavailable += 1
    observed_total = sum(totals)
    method_cost = _method_usage_cost(observations)
    comparison = _model_matched_cost_comparison(
        matched_x1v2_record, observations, method_cost
    )
    return {
        "schema": "paper1.model_matched_cost.v1",
        "raw_token_safety_cap": max_total_tokens,
        "observed_input_tokens": sum(input_totals),
        "observed_output_tokens": sum(output_totals),
        "observed_total_tokens": observed_total,
        "method_cost": method_cost,
        "model_matched_x1v2_comparison": comparison,
        "usage_unavailable_call_count": unavailable,
        "eligible": (
            unavailable == 0
            and observed_total <= max_total_tokens
            and method_cost["eligible"]
            and comparison["eligible"]
            and comparison["within_25x"]
        ),
    }


def _method_usage_cost(observations: list[dict[str, Any]]) -> dict[str, Any]:
    roles: list[dict[str, Any]] = []
    errors: list[str] = []
    for observation in observations:
        if not isinstance(observation, dict):
            errors.append("observation is not an object")
            continue
        usage = observation.get("usage")
        if not isinstance(usage, dict):
            errors.append(f"{observation.get('role')}: usage unavailable")
            continue
        pricing_raw = observation.get("pricing")
        if not isinstance(pricing_raw, dict):
            errors.append(f"{observation.get('role')}: pricing unavailable")
            continue
        try:
            pricing = LLMPricing.model_validate(pricing_raw)
        except ValidationError as exc:
            errors.append(f"{observation.get('role')}: invalid pricing: {exc}")
            continue
        prompt_cache = observation.get("prompt_cache")
        prompt_cache = prompt_cache if isinstance(prompt_cache, dict) else {}
        cost = estimate_usage_cost_usd(usage, pricing)
        if not cost["eligible"]:
            errors.extend(
                f"{observation.get('role')}: {message}" for message in cost["errors"]
            )
        roles.append(
            {
                "role": observation.get("role"),
                "configured_model": observation.get("configured_model"),
                "prompt_cache": prompt_cache,
                "cost": cost,
            }
        )
    usd_values = [
        item["cost"]["total_usd"]
        for item in roles
        if item["cost"]["total_usd"] is not None
    ]
    return {
        "accounting_rule": "sum configured USD prices for normalized usage classes",
        "roles": roles,
        "total_usd": sum(usd_values) if len(usd_values) == len(roles) else None,
        "eligible": not errors and len(roles) == len(observations),
        "errors": errors,
    }


def _model_matched_cost_comparison(
    record_path: str | None,
    observations: list[dict[str, Any]],
    method_cost: dict[str, Any],
) -> dict[str, Any]:
    if record_path is None:
        return {
            "eligible": False,
            "within_25x": False,
            "reason": "model-matched X1v2 record was not supplied",
        }
    path = Path(record_path)
    try:
        raw = path.read_bytes()
        baseline = json.loads(raw)
    except Exception as exc:  # noqa: BLE001 - audit result, not graph failure
        return {
            "eligible": False,
            "within_25x": False,
            "reason": f"cannot read X1v2 record: {type(exc).__name__}: {exc}",
        }
    models = {
        item.get("configured_model") for item in observations if isinstance(item, dict)
    }
    baseline_model = baseline.get("configured_model")
    if len(models) != 1 or baseline_model not in models:
        return {
            "eligible": False,
            "within_25x": False,
            "method_models": sorted(str(item) for item in models),
            "baseline_model": baseline_model,
            "reason": "method and X1v2 must use the exact same configured model",
        }
    pricing_raw = next(
        (
            item.get("pricing")
            for item in observations
            if isinstance(item, dict) and isinstance(item.get("pricing"), dict)
        ),
        None,
    )
    usage = baseline.get("usage")
    if not isinstance(pricing_raw, dict) or not isinstance(usage, dict):
        return {
            "eligible": False,
            "within_25x": False,
            "reason": "baseline usage or method pricing is unavailable",
        }
    pricing = LLMPricing.model_validate(pricing_raw)
    baseline_cost = estimate_usage_cost_usd(usage, pricing)
    baseline_usd = baseline_cost["total_usd"]
    method_usd = method_cost.get("total_usd")
    multiplier = (
        method_usd / baseline_usd
        if isinstance(method_usd, (int, float))
        and isinstance(baseline_usd, (int, float))
        and baseline_usd > 0
        else None
    )
    eligible = bool(method_cost.get("eligible") and baseline_cost["eligible"])
    return {
        "eligible": eligible and multiplier is not None,
        "within_25x": multiplier is not None and multiplier <= 25,
        "configured_model": baseline_model,
        "method_cost_usd": method_usd,
        "x1v2_cost_usd": baseline_usd,
        "cost_multiplier": multiplier,
        "baseline_record": str(path),
        "baseline_record_sha256": hashlib.sha256(raw).hexdigest(),
        "baseline_cost": baseline_cost,
        "reason": None if eligible else "method or baseline cost is not priceable",
    }


def _load_replay_plans(
    run_dir: Path,
    pair: dict[str, Any],
) -> tuple[
    core.ContractExtractionPlan,
    list[core.DiscoveryGroundingPlan],
    list[dict[str, Any]],
]:
    contract_files = sorted(
        (run_dir / "stages").glob("*-contract-extraction/record.json")
    )
    evidence_files = sorted(
        (run_dir / "stages").glob("*-evidence-planning/record.json")
    )
    grounding_files = sorted(
        (run_dir / "stages").glob("*-semantic-grounding/record.json")
    )
    discovery_files = sorted(
        (run_dir / "stages").glob("*-discovery-grounding/record.json")
    )
    prepare_files = sorted((run_dir / "stages").glob("*-prepare/record.json"))
    contract_record = (
        json.loads(contract_files[-1].read_text(encoding="utf-8"))
        if contract_files
        else {}
    )
    evidence_record = (
        json.loads(evidence_files[-1].read_text(encoding="utf-8"))
        if evidence_files
        else {}
    )
    grounding_record = (
        json.loads(grounding_files[-1].read_text(encoding="utf-8"))
        if grounding_files
        else {}
    )
    discovery_record = (
        json.loads(discovery_files[-1].read_text(encoding="utf-8"))
        if discovery_files
        else {}
    )
    prepare_record = (
        json.loads(prepare_files[-1].read_text(encoding="utf-8"))
        if prepare_files
        else {}
    )

    def migrate_contract_binding_status(value: Any) -> Any:
        if not isinstance(value, dict):
            return value
        migrated = dict(value)
        for field in (
            "initial_contract_bindings",
            "containment_contract_bindings",
            "transition_group_bindings",
        ):
            rows = migrated.get(field)
            if not isinstance(rows, list):
                continue
            migrated[field] = [
                {"status": "grounded", **row} if isinstance(row, dict) else row
                for row in rows
            ]
        return migrated

    contract_payload = contract_record.get("contract_plan") or prepare_record.get(
        "contract_plan"
    )
    discovery_branches = discovery_record.get("discovery_branches")
    if contract_payload and isinstance(discovery_branches, list):
        observations = discovery_record.get("llm_observations", [])
        if not isinstance(observations, list):
            observations = []
        parsed_outputs = [
            item.get("parsed_output")
            for item in observations
            if isinstance(item, dict)
            and item.get("role") == "paper1_discovery_grounding"
            and item.get("status") == "completed"
            and isinstance(item.get("parsed_output"), dict)
        ]
        branch_payloads = [
            branch["discovery_grounding_plan"]
            for branch in discovery_branches
            if isinstance(branch, dict)
            and isinstance(branch.get("discovery_grounding_plan"), dict)
        ]
        replay_payloads = (
            parsed_outputs
            if len(parsed_outputs) == len(branch_payloads)
            else branch_payloads
        )
        plans = [
            core.DiscoveryGroundingPlan.model_validate(
                migrate_contract_binding_status(payload)
            )
            for payload in replay_payloads
        ]
        if not plans:
            raise ValueError("replay run has no valid discovery branches")
        return (
            core.ContractExtractionPlan.model_validate(contract_payload),
            plans,
            observations,
        )
    discovery_payload = discovery_record.get("discovery_grounding_plan")
    if contract_payload and discovery_payload:
        contract = core.ContractExtractionPlan.model_validate(contract_payload)
        if "contract_plan" in discovery_payload:
            discovery = core.DiscoveryGroundingPlan(
                concept_bindings=[
                    core.CompactConceptBinding(
                        concept_id=item["concept_id"],
                        source_state_id=item["source_state_id"],
                    )
                    for item in discovery_payload.get("concept_bindings", [])
                ],
                initial_contract_bindings=[],
                containment_contract_bindings=[],
                transition_group_bindings=[],
                additional_contracts=core.ContractExtractionPlan.model_validate(
                    discovery_payload["contract_plan"]
                ),
                surface_candidates=discovery_payload.get("surface_candidates", []),
                behavior_candidates=discovery_payload.get("behavior_candidates", []),
                unresolved=discovery_payload.get("unresolved", []),
            )
        else:
            discovery = core.DiscoveryGroundingPlan.model_validate(
                migrate_contract_binding_status(discovery_payload)
            )
        observations = discovery_record.get("llm_observations", [])
        if not isinstance(observations, list):
            observations = []
        return contract, [discovery], observations

    evidence_payload = evidence_record.get("evidence_plan") or prepare_record.get(
        "evidence_plan"
    )
    grounding_payload = grounding_record.get("grounding_plan") or prepare_record.get(
        "grounding_plan"
    )
    if not contract_payload or not evidence_payload or not grounding_payload:
        raise ValueError(
            "replay run lacks reusable contract/evidence/semantic-grounding plans"
        )

    def migrate_observed_transition_id(value: Any) -> Any:
        if isinstance(value, list):
            return [migrate_observed_transition_id(item) for item in value]
        if not isinstance(value, dict):
            return value
        migrated = {
            key: migrate_observed_transition_id(item)
            for key, item in value.items()
            if key != "source_transition_id"
        }
        if "source_transition_id" in value and "observed_transition_id" not in migrated:
            migrated["observed_transition_id"] = value["source_transition_id"]
        return migrated

    contract = core.ContractExtractionPlan.model_validate(
        migrate_observed_transition_id(contract_payload)
    )
    evidence = core.IssueDiscoveryPlan.model_validate(
        migrate_observed_transition_id(evidence_payload)
    )
    grounding = core.SemanticGroundingPlan.model_validate(
        migrate_observed_transition_id(grounding_payload)
    )
    grounded_contract, grounded_evidence, _ = core.validate_semantic_grounding(
        pair, evidence, grounding
    )
    discovery = core.DiscoveryGroundingPlan(
        concept_bindings=[
            core.CompactConceptBinding(
                concept_id=item.concept_id,
                source_state_id=item.source_state_id,
            )
            for item in grounding.concept_bindings
        ],
        initial_contract_bindings=[],
        containment_contract_bindings=[],
        transition_group_bindings=[],
        additional_contracts=core.ContractExtractionPlan.model_validate(
            grounded_contract.model_dump(mode="python")
        ),
        surface_candidates=grounded_evidence.surface_candidates,
        behavior_candidates=grounded_evidence.behavior_candidates,
        unresolved=grounding.unresolved,
    )
    observations = grounding_record.get("llm_observations") or prepare_record.get(
        "llm_observations", []
    )
    if not isinstance(observations, list):
        observations = []
    return contract, [discovery], observations


def build_prototype_graph(responder: DirectStructuredResponder) -> Any:
    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("langgraph is required for this prototype") from exc

    def prepare(state: PrototypeGraphState) -> PrototypeGraphState:
        graph_input = state["input"]
        report_root = (
            Path(graph_input.report_root).resolve()
            if graph_input.report_root
            else core.DEFAULT_REPORT_ROOT
        )
        pair = core.load_pair(graph_input.case, report_root)
        inspect = core.inspect_fcstm(
            pair["fcstm"],
            pair["paths"]["fcstm"],
            smt_timeout_ms=graph_input.smt_timeout_ms,
        )
        probe_seeds = core.derive_probe_seeds(inspect)
        update: PrototypeGraphState = {
            "pair": pair,
            "inspect": inspect,
            "probe_seeds": probe_seeds,
            "progressive_seeds": core.derive_progressive_evidence_seeds(pair, inspect),
            "contract_context": core.build_contract_context(pair),
            "llm_observations": [],
            "d_feedback": [],
            "d_repair_count": 0,
            "execution_diagnostics": [],
        }
        if graph_input.replay_plans_from:
            try:
                contract, discoveries, observations = _load_replay_plans(
                    Path(graph_input.replay_plans_from).resolve(), pair
                )
            except Exception as exc:  # noqa: BLE001 - invalid replay is audited
                return {
                    **update,
                    "failure": {
                        "node": "prepare",
                        "class": "replay_invalid",
                        "message": f"{type(exc).__name__}: {exc}",
                    },
                }
            update.update(
                {
                    "contract_plan": contract,
                    "replay_discovery_grounding_plans": discoveries,
                    "llm_observations": observations,
                }
            )
        return update

    def contract_extraction(state: PrototypeGraphState) -> PrototypeGraphState:
        if "contract_plan" in state:
            return {"contract_plan": state["contract_plan"]}
        plan, observations, error = _invoke_with_schema_repair(
            responder,
            role="paper1_contract_extraction",
            schema=core.ContractExtractionPlan,
            system_prompt=core.CONTRACT_SYSTEM_PROMPT,
            user_input=state["contract_context"],
        )
        if error is not None or plan is None:
            failure_class = _failure_class_from_observations(observations)
            if _is_whole_cell_failure(failure_class):
                return {
                    "failure": {
                        "node": "contract_extraction",
                        "class": failure_class,
                        "message": f"{type(error).__name__}: {error}",
                    },
                    "llm_observations": [
                        *state.get("llm_observations", []),
                        *observations,
                    ],
                }
            return {
                "contract_plan": core.ContractExtractionPlan(
                    initial_contracts=[], transition_groups=[]
                ),
                "execution_diagnostics": [
                    {
                        "stage": "contract_extraction",
                        "class": failure_class,
                        "message": f"{type(error).__name__}: {error}",
                    }
                ],
                "llm_observations": [
                    *state.get("llm_observations", []),
                    *observations,
                ],
            }
        if _contract_plan_is_empty(plan):
            repair_prompt = (
                f"{state['contract_context']}\n\n# Empty-contract completeness review\n\n"
                "The previous response returned every contract array empty. Re-read "
                "all numbered NL lines and return every explicit state, initial, "
                "containment, direct-transition, event-scope, and state-owned "
                "action obligation supported by the text. Descriptive lines may "
                "remain unrepresented, but do not leave an explicit transition or "
                "named behavior requirement out merely because the artifact is "
                "incomplete. This is a completeness review, not permission to add "
                "artifact-derived obligations."
            )
            reviewed, review_observations, review_error = _invoke_with_schema_repair(
                responder,
                role="paper1_contract_extraction",
                schema=core.ContractExtractionPlan,
                system_prompt=core.CONTRACT_SYSTEM_PROMPT,
                user_input=repair_prompt,
            )
            observations.extend(review_observations)
            if review_error is None and reviewed is not None:
                plan = reviewed
        return {
            "contract_plan": plan,
            "llm_observations": [
                *state.get("llm_observations", []),
                *observations,
            ],
        }

    def discovery_grounding(state: PrototypeGraphState) -> PrototypeGraphState:
        discovery_context = core.build_discovery_grounding_context(
            state["pair"], state["inspect"], state["contract_plan"]
        )
        observations: list[dict[str, Any]] = []
        branch_inputs: list[
            tuple[
                core.DiscoveryGroundingPlan,
                str | None,
                str,
                int,
                core.DiscoveryGroundingPlan,
            ]
        ] = []
        quarantined_inputs: list[
            tuple[core.DiscoveryGroundingPlan, str | None, str, int, list[str]]
        ] = []
        branch_failures: list[dict[str, str]] = []
        if "replay_discovery_grounding_plans" in state:
            branch_inputs = [
                (plan, None, f"replay_branch_{index}", index, plan)
                for index, plan in enumerate(state["replay_discovery_grounding_plans"])
            ]
        else:
            for sample_index in range(DISCOVERY_SAMPLE_COUNT):
                lens_id, lens_prompt = core.DISCOVERY_GROUNDING_AUDIT_LENSES[
                    sample_index
                ]
                plan, sample_observations, error = _invoke_with_schema_repair(
                    responder,
                    role="paper1_discovery_grounding",
                    schema=core.FreshDiscoveryGroundingPlan,
                    system_prompt=(
                        f"{core.DISCOVERY_GROUNDING_SYSTEM_PROMPT}\n\n"
                        f"# Complementary audit lens: {lens_id}\n\n{lens_prompt}"
                    ),
                    user_input=discovery_context,
                )
                observations.extend(sample_observations)
                if error is not None or plan is None:
                    branch_failures.append(
                        {
                            "stage": "discovery_grounding",
                            "class": _failure_class_from_observations(
                                sample_observations,
                                default="internal",
                            ),
                            "message": (
                                f"sample {sample_index + 1}/{DISCOVERY_SAMPLE_COUNT}: "
                                f"{type(error).__name__}: {error}"
                            ),
                        }
                    )
                    continue
                call_id = _completed_call_id(sample_observations)
                completeness_errors = _fresh_transition_binding_errors(
                    state["contract_plan"], plan
                )
                if completeness_errors:
                    quarantined_inputs.append(
                        (
                            plan,
                            call_id,
                            lens_id,
                            sample_index,
                            completeness_errors,
                        )
                    )
                    branch_failures.append(
                        {
                            "stage": "discovery_grounding",
                            "class": "fresh_transition_binding_incomplete",
                            "message": (
                                f"sample {sample_index + 1}/{DISCOVERY_SAMPLE_COUNT} "
                                "was quarantined: " + "; ".join(completeness_errors)
                            ),
                        }
                    )
                    continue
                branch_inputs.append((plan, call_id, lens_id, sample_index, plan))
            if not branch_inputs and not quarantined_inputs:
                failure_class = _failure_class_from_observations(observations)
                if not _is_whole_cell_failure(failure_class):
                    return {
                        "discovery_grounding_context": discovery_context,
                        "discovery_branches": [],
                        "semantic_grounding_diagnostics": branch_failures,
                        "llm_observations": [
                            *state.get("llm_observations", []),
                            *observations,
                        ],
                    }
                return {
                    "discovery_grounding_context": discovery_context,
                    "failure": {
                        "node": "discovery_grounding",
                        "class": failure_class,
                        "message": "all independent discovery samples failed",
                    },
                    "llm_observations": [
                        *state.get("llm_observations", []),
                        *observations,
                    ],
                }
        inventory = core._semantic_grounding_inventory(state["pair"])
        canonical_ids = frozenset(
            [
                *(item["id"] for item in inventory.get("states", []) if item.get("id")),
                *(
                    item["id"]
                    for item in inventory.get("transitions", [])
                    if item.get("id")
                ),
            ]
        )
        plans, ensemble_diagnostics = _veto_explicit_cross_sample_conflicts(
            [plan for plan, _, _, _, _ in branch_inputs],
            canonical_formal_ids=canonical_ids,
        )
        branch_inputs = [
            (
                plan,
                branch_inputs[index][1],
                branch_inputs[index][2],
                branch_inputs[index][3],
                branch_inputs[index][4],
            )
            for index, plan in enumerate(plans)
        ]
        branches: list[dict[str, Any]] = []
        diagnostics = [*branch_failures, *ensemble_diagnostics]
        for (
            plan,
            llm_call_id,
            lens_id,
            sample_index,
            llm_semantic_plan,
        ) in branch_inputs:
            try:
                contract, evidence, branch_diagnostics = (
                    core.validate_discovery_grounding(
                        state["pair"], state["contract_plan"], plan
                    )
                )
                if "replay_discovery_grounding_plans" not in state:
                    evidence, typed_diagnostics = _quarantine_untyped_fresh_evidence(
                        evidence
                    )
                    branch_diagnostics.extend(typed_diagnostics)
            except Exception as exc:  # noqa: BLE001 - internal stages must degrade
                contract = core.GroundedContractPlan()
                evidence = core.IssueDiscoveryPlan(
                    surface_candidates=[], behavior_candidates=[]
                )
                branch_diagnostics = [
                    {
                        "stage": "discovery_grounding",
                        "class": "grounding_internal_error",
                        "message": f"{type(exc).__name__}: {exc}",
                    }
                ]
            diagnostics.extend(
                {**item, "sample_index": str(sample_index)}
                for item in branch_diagnostics
            )
            branches.append(
                {
                    "sample_index": sample_index,
                    "lens_id": lens_id,
                    "llm_call_id": llm_call_id,
                    "quarantined": False,
                    "llm_semantic_plan": llm_semantic_plan,
                    "discovery_grounding_plan": plan,
                    "grounded_contract_plan": contract,
                    "grounded_evidence_plan": evidence,
                }
            )
        for (
            plan,
            llm_call_id,
            lens_id,
            sample_index,
            completeness_errors,
        ) in quarantined_inputs:
            branches.append(
                {
                    "sample_index": sample_index,
                    "lens_id": lens_id,
                    "llm_call_id": llm_call_id,
                    "quarantined": True,
                    "quarantine_errors": completeness_errors,
                    "discovery_grounding_plan": plan,
                    "grounded_contract_plan": core.GroundedContractPlan(),
                    "grounded_evidence_plan": core.IssueDiscoveryPlan(
                        surface_candidates=[], behavior_candidates=[]
                    ),
                }
            )
        branches.sort(key=lambda item: item["sample_index"])
        return {
            "discovery_grounding_context": discovery_context,
            "discovery_branches": branches,
            "semantic_grounding_diagnostics": diagnostics,
            "llm_observations": [
                *state.get("llm_observations", []),
                *observations,
            ],
        }

    def execute_batch(state: PrototypeGraphState) -> PrototypeGraphState:
        outcomes = []
        diagnostics = list(state.get("semantic_grounding_diagnostics", []))
        stages = [
            (
                "progressive_scout",
                lambda: core.execute_progressive_evidence_seeds(
                    state["pair"],
                    state["inspect"],
                    normative_quotes=core.build_progressive_normative_quote_bindings(
                        state["pair"],
                        state["contract_plan"],
                        [
                            branch["discovery_grounding_plan"]
                            for branch in state["discovery_branches"]
                            if not branch.get("quarantined")
                        ],
                    ),
                ),
            ),
            (
                "source_static_scout",
                lambda: core.execute_source_static_evidence_scouts(
                    state["pair"], state["inspect"]
                ),
            ),
        ]
        for stage_name, execute in stages:
            try:
                outcomes.extend(execute())
            except Exception as exc:  # noqa: BLE001 - internal stages degrade
                diagnostics.append(
                    {
                        "stage": stage_name,
                        "class": type(exc).__name__,
                        "message": str(exc),
                    }
                )
        for branch in state["discovery_branches"]:
            if branch.get("quarantined"):
                continue
            semantic_provenance = core.build_llm_binding_provenance(
                state.get("llm_observations", []),
                role="paper1_discovery_grounding",
                semantic_plan=branch.get(
                    "llm_semantic_plan", branch["discovery_grounding_plan"]
                ),
                grounded_contract_plan=branch["grounded_contract_plan"],
                grounded_evidence_plan=branch["grounded_evidence_plan"],
                replayed=bool(state["input"].replay_plans_from),
                llm_call_id=branch.get("llm_call_id"),
            )
            sample_index = branch["sample_index"]
            if semantic_provenance is None:
                diagnostics.append(
                    {
                        "stage": "semantic_provenance",
                        "class": "llm_binding_provenance_unavailable",
                        "message": (
                            f"sample {sample_index}: LLM-grounded candidates cannot "
                            "qualify for W2 without a matching immutable call record"
                        ),
                    }
                )
            branch_stages = [
                (
                    "contract_execution",
                    lambda branch=branch, provenance=semantic_provenance: (
                        core.execute_contract_extraction_plan(
                            state["pair"],
                            state["inspect"],
                            branch["grounded_contract_plan"],
                            binding_authority="paper1_discovery_grounding_llm",
                            semantic_provenance=provenance,
                        )
                    ),
                ),
                (
                    "evidence_execution",
                    lambda branch=branch, provenance=semantic_provenance: (
                        core.execute_evidence_plan(
                            state["pair"],
                            state["inspect"],
                            branch["grounded_evidence_plan"],
                            binding_authority="paper1_discovery_grounding_llm",
                            semantic_provenance=provenance,
                        )
                    ),
                ),
            ]
            for stage_name, execute in branch_stages:
                try:
                    outcomes.extend(execute())
                except Exception as exc:  # noqa: BLE001 - internal stages degrade
                    diagnostics.append(
                        {
                            "stage": stage_name,
                            "class": type(exc).__name__,
                            "message": f"sample {sample_index}: {exc}",
                        }
                    )
        findings = core.build_finding_records(core.select_finding_outcomes(outcomes))
        return {
            "outcomes": outcomes,
            "finding_records": findings,
            "d_context": core.build_d_context(state["pair"], findings),
            "execution_diagnostics": diagnostics,
        }

    def d_adjudication(state: PrototypeGraphState) -> PrototypeGraphState:
        if not state["finding_records"]:
            return {
                "d_plan": core.DAdjudicationPlan(decisions=[]),
                "d_call_count": 0,
            }
        feedback = ""
        if state.get("d_feedback"):
            feedback = "\n\n# Deterministic contract feedback\n\n" + "\n".join(
                f"- {item}" for item in state["d_feedback"]
            )
        repair_keys = set(state.get("d_repair_keys", []))
        findings = sorted(
            (
                item
                for item in state["finding_records"]
                if not repair_keys or item["finding_key"] in repair_keys
            ),
            key=core.d_finding_sort_key,
        )
        context = core.build_d_context(state["pair"], findings)
        repairing = bool(repair_keys)
        frozen_context = ""
        if repairing:
            frozen_context = (
                "\n\n# Frozen valid decisions (read-only context)\n\n"
                + json.dumps(
                    [
                        {
                            "finding_key": item.get("finding_key"),
                            "d_level": item.get("d_level"),
                            "violated_obligation": item.get("violated_obligation"),
                            "duplicate_of": item.get("duplicate_of"),
                        }
                        for item in state.get("d_frozen_decisions", [])
                    ],
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                + "\n"
            )
        adjudication_header = (
            (
                "# Targeted D decision repair\n\n"
                "All omitted decisions already passed deterministic validation and "
                "are frozen. Correct only the supplied invalid decisions; do not "
                "repeat, revise, or replace any frozen decision. Set `duplicate_of` "
                "and `duplicate_rationale` to null for every repaired decision; "
                "the report keeps an independent facet rather than retrying semantic "
                "clustering here.\n\n"
            )
            if repairing
            else "# Whole-pair D adjudication\n\n"
        ) + (
            f"Return exactly {len(findings)} decisions, one for every finding in "
            "the supplied stable order. Copy each FINDING_KEY exactly from the "
            "following checklist; do not abbreviate, normalize, or invent keys.\n\n"
            "# Exact finding_key checklist\n\n"
            + "\n".join(f"- FINDING_KEY:{item['finding_key']}" for item in findings)
            + "\n\n"
        )
        plan, observations, error = _invoke_with_schema_repair(
            responder,
            role=("paper1_d_targeted_repair" if repairing else "paper1_d_adjudication"),
            schema=core.DAdjudicationPlan,
            system_prompt=core.D_SYSTEM_PROMPT,
            user_input=adjudication_header + context + frozen_context + feedback,
        )
        d_call_count = state.get("d_call_count", 0) + 1
        if error is not None or plan is None:
            failure_class = _failure_class_from_observations(
                observations,
                default="internal",
            )
            if _is_whole_cell_failure(failure_class):
                return {
                    "failure": {
                        "node": "d_adjudication",
                        "class": failure_class,
                        "message": f"{type(error).__name__}: {error}",
                    },
                    "d_call_count": d_call_count,
                    "llm_observations": [
                        *state.get("llm_observations", []),
                        *observations,
                    ],
                }
            return {
                "d_plan": core.DAdjudicationPlan(decisions=[]),
                "d_call_failure": failure_class,
                "d_call_count": d_call_count,
                "execution_diagnostics": [
                    *state.get("execution_diagnostics", []),
                    {
                        "stage": "d_adjudication",
                        "class": failure_class,
                        "message": f"{type(error).__name__}: {error}",
                    },
                ],
                "llm_observations": [
                    *state.get("llm_observations", []),
                    *observations,
                ],
            }
        if repairing:
            frozen = [
                core.DDecision.model_validate(item)
                for item in state.get("d_frozen_decisions", [])
            ]
            repaired, repair_output_errors = _validate_targeted_d_repair_output(
                plan,
                repair_keys=state["d_repair_keys"],
                frozen_keys={decision.finding_key for decision in frozen},
            )
            plan = core.DAdjudicationPlan(decisions=[*frozen, *repaired])
        else:
            repair_output_errors = []
        return {
            "d_plan": plan,
            "d_call_count": d_call_count,
            "d_repair_count": (
                state.get("d_repair_count", 0) + 1
                if repairing
                else state.get("d_repair_count", 0)
            ),
            "d_repair_output_errors": repair_output_errors,
            "llm_observations": [
                *state.get("llm_observations", []),
                *observations,
            ],
        }

    def validate_d(state: PrototypeGraphState) -> PrototypeGraphState:
        if state.get("d_call_failure"):
            errors = [
                f"D adjudication unavailable after {state['d_call_failure']} failure"
            ]
            invalid = {
                item["finding_key"]: errors for item in state["finding_records"]
            }
            findings = _partially_adjudicated_findings(
                state["finding_records"], {}, invalid
            )
            return {
                "finding_records": findings,
                "d_feedback": errors,
                "d_fallback_reason": "; ".join(errors),
                "confirmed_issues": [],
                "accepted_issues": [],
                "retry_d": False,
            }
        valid, invalid, diagnostics = _partition_d_decisions(
            state["finding_records"], state["d_plan"]
        )
        repair_output_errors = state.get("d_repair_output_errors", [])
        if repair_output_errors:
            for finding_key in state.get("d_repair_keys", []):
                valid.pop(finding_key, None)
                invalid.setdefault(finding_key, []).extend(repair_output_errors)
        errors = [
            f"{finding_key}: {message}"
            for finding_key, messages in invalid.items()
            for message in messages
        ]
        errors.extend(diagnostics)
        if invalid and state.get("d_repair_count", 0) == 0:
            return {
                "d_feedback": errors,
                "d_frozen_decisions": [
                    decision.model_dump(mode="json") for decision in valid.values()
                ],
                "d_repair_keys": sorted(invalid),
                "retry_d": True,
            }
        findings = _partially_adjudicated_findings(
            state["finding_records"], valid, invalid
        )
        if invalid:
            return {
                "finding_records": findings,
                "d_feedback": errors,
                "d_fallback_reason": "; ".join(errors),
                "confirmed_issues": core.select_confirmed_issues(findings),
                "accepted_issues": core.select_accepted_issues(findings),
                "retry_d": False,
            }
        return {
            "finding_records": findings,
            "d_feedback": errors,
            "d_repair_keys": [],
            "confirmed_issues": core.select_confirmed_issues(findings),
            "accepted_issues": core.select_accepted_issues(findings),
            "retry_d": False,
        }

    def publish(state: PrototypeGraphState) -> PrototypeGraphState:
        observations = state.get("llm_observations", [])
        usage = [
            observation.get("usage", {})
            for observation in observations
            if isinstance(observation, dict)
        ]
        report_clusters = core.build_report_issue_clusters(state["finding_records"])
        confirmed_report_issues = core.select_confirmed_report_issues(report_clusters)
        accepted_report_issues = core.select_accepted_report_issues(report_clusters)
        token_budget = _usage_budget(
            observations,
            state["input"].max_total_tokens,
            state["input"].matched_x1v2_record,
        )
        discovery_branches = state["discovery_branches"]
        final_record = {
            "schema": "paper1.evidence_discovery_langgraph_prototype.v1",
            "exploratory_only": True,
            "case": state["input"].case,
            "profile": state["input"].profile,
            "strategy": "shared_a_complementary_dual_b_formal_execution_single_d",
            "replay_plans_from": state["input"].replay_plans_from,
            "contract_plan": state["contract_plan"].model_dump(mode="json"),
            "discovery_grounding_plans": [
                branch.get(
                    "llm_semantic_plan", branch["discovery_grounding_plan"]
                ).model_dump(mode="json")
                for branch in discovery_branches
            ],
            "post_ensemble_discovery_grounding_plans": [
                branch["discovery_grounding_plan"].model_dump(mode="json")
                for branch in discovery_branches
            ],
            "grounded_contract_plans": [
                branch["grounded_contract_plan"].model_dump(mode="json")
                for branch in discovery_branches
            ],
            "grounded_evidence_plans": [
                branch["grounded_evidence_plan"].model_dump(mode="json")
                for branch in discovery_branches
            ],
            "discovery_branch_call_ids": [
                branch.get("llm_call_id") for branch in discovery_branches
            ],
            "discovery_branch_lens": [
                branch.get("lens_id") for branch in discovery_branches
            ],
            "progressive_seeds": state["progressive_seeds"],
            "outcomes": state["outcomes"],
            "finding_records": state["finding_records"],
            "confirmed_issues": state.get("confirmed_issues", []),
            "accepted_issues": state.get("accepted_issues", []),
            "report_issue_clusters": report_clusters,
            "confirmed_report_issues": confirmed_report_issues,
            "accepted_report_issues": accepted_report_issues,
            "d_contract_feedback": state.get("d_feedback", []),
            "d_fallback_reason": state.get("d_fallback_reason"),
            "d_unresolved_reason": state.get("d_unresolved_reason"),
            "execution_diagnostics": state.get("execution_diagnostics", []),
            "llm_observations": observations,
            "telemetry": {
                "llm_call_count": len(observations),
                "usage": usage,
                "requested_discovery_sample_count": (
                    1 if state["input"].replay_plans_from else DISCOVERY_SAMPLE_COUNT
                ),
                "completed_discovery_branch_count": len(discovery_branches),
                "progressive_seed_count": len(state["progressive_seeds"]),
                "finding_count": len(state["finding_records"]),
                "confirmed_issue_count": len(state.get("confirmed_issues", [])),
                "accepted_issue_count": len(state.get("accepted_issues", [])),
                "report_issue_count": len(report_clusters),
                "confirmed_report_issue_count": len(confirmed_report_issues),
                "accepted_report_issue_count": len(accepted_report_issues),
                "d_repair_count": state.get("d_repair_count", 0),
                "d_call_count": state.get("d_call_count", 0),
                "token_budget": token_budget,
            },
        }
        provenance_errors = core.validate_record_semantic_provenance(final_record)
        final_record["semantic_provenance_audit"] = {
            "schema": "paper1.semantic_provenance_audit.v1",
            "eligible": not provenance_errors,
            "errors": provenance_errors,
        }
        final_record["telemetry"]["eligible"] = bool(
            token_budget["eligible"] and not provenance_errors
        )
        return {"final_record": final_record}

    def run_failed(state: PrototypeGraphState) -> PrototypeGraphState:
        return {
            "final_record": {
                "schema": "paper1.evidence_discovery_langgraph_prototype.v1",
                "exploratory_only": True,
                "case": state["input"].case,
                "profile": state["input"].profile,
                "status": "failed",
                "failure": state["failure"],
                "llm_observations": state.get("llm_observations", []),
            }
        }

    def after_node(state: PrototypeGraphState, next_node: Route) -> Route:
        return "run_failed" if "failure" in state else next_node

    def after_validate(state: PrototypeGraphState) -> Route:
        if "failure" in state:
            return "run_failed"
        if state.get("retry_d"):
            return "d_adjudication"
        return "publish"

    graph = StateGraph(PrototypeGraphState)
    graph.add_node("prepare", prepare)
    graph.add_node("contract_extraction", contract_extraction)
    graph.add_node("discovery_grounding", discovery_grounding)
    graph.add_node("execute_batch", execute_batch)
    graph.add_node("d_adjudication", d_adjudication)
    graph.add_node("validate_d", validate_d)
    graph.add_node("publish", publish)
    graph.add_node("run_failed", run_failed)
    graph.add_edge(START, "prepare")
    graph.add_conditional_edges(
        "prepare", lambda state: after_node(state, "contract_extraction")
    )
    graph.add_conditional_edges(
        "contract_extraction", lambda state: after_node(state, "discovery_grounding")
    )
    graph.add_conditional_edges(
        "discovery_grounding", lambda state: after_node(state, "execute_batch")
    )
    graph.add_conditional_edges(
        "execute_batch", lambda state: after_node(state, "d_adjudication")
    )
    graph.add_conditional_edges(
        "d_adjudication", lambda state: after_node(state, "validate_d")
    )
    graph.add_conditional_edges("validate_d", after_validate)
    graph.add_edge("publish", END)
    graph.add_edge("run_failed", END)
    return graph.compile()


def run_graph(
    graph_input: PrototypeGraphInput,
    responder: DirectStructuredResponder,
    *,
    record_store: ImmutableRecordStore | None = None,
) -> PrototypeGraphState:
    graph = build_prototype_graph(responder)
    state: PrototypeGraphState = {"input": graph_input}
    for event in graph.stream(
        state, config={"recursion_limit": 100}, stream_mode="updates"
    ):
        for node_name, update in event.items():
            if update is None:
                continue
            state.update(update)
            if record_store is not None:
                record_store.append(node_name, update)
    return state


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", required=True)
    parser.add_argument("--profile", default="gpt-5.5")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--report-root", default=None)
    parser.add_argument("--replay-plans-from", default=None)
    parser.add_argument("--matched-x1v2-record", default=None)
    parser.add_argument("--max-output-tokens", type=int, default=10_000)
    parser.add_argument(
        "--max-total-tokens", type=int, default=DEFAULT_MAX_TOTAL_TOKENS
    )
    parser.add_argument(
        "--transport-retries", type=int, default=DEFAULT_TRANSPORT_RETRIES
    )
    stream_mode = parser.add_mutually_exclusive_group()
    stream_mode.add_argument(
        "--stream",
        dest="streaming",
        action="store_true",
        help="Use streaming responses (the default).",
    )
    stream_mode.add_argument(
        "--no-stream",
        dest="streaming",
        action="store_false",
        help="Use complete non-streaming responses.",
    )
    # Hosted sub2api may return a gateway timeout before a complete response
    # is available. Streaming is the research-run default so the connection
    # starts delivering tokens before the gateway wall-clock deadline; callers
    # can still force ``--no-stream`` for transport diagnostics.
    parser.set_defaults(streaming=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output_dir = Path(args.output_dir)
    started = time.perf_counter_ns()
    responder = DirectStructuredResponder(
        args.profile,
        max_output_tokens=args.max_output_tokens,
        transport_retries=args.transport_retries,
        streaming=args.streaming,
        repeat_schema_in_prompt=True,
        prompt_cache_ttl="1h",
    )
    graph_input = PrototypeGraphInput(
        case=args.case,
        profile=args.profile,
        report_root=args.report_root,
        replay_plans_from=args.replay_plans_from,
        matched_x1v2_record=args.matched_x1v2_record,
        max_total_tokens=args.max_total_tokens,
    )
    state = run_graph(
        graph_input,
        responder,
        record_store=ImmutableRecordStore(output_dir / "stages"),
    )
    record = core._jsonable(state["final_record"])
    record["elapsed_ms"] = (time.perf_counter_ns() - started) / 1_000_000
    output = output_dir / "record.json"
    core._write_json(output, record)
    print(
        f"[{record.get('status', 'completed')}] case={args.case} "
        f"findings={len(record.get('finding_records', []))} "
        f"confirmed={len(record.get('confirmed_issues', []))} -> {output}"
    )
    return 1 if record.get("status") == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
