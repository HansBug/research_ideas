from __future__ import annotations

import contextvars
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Callable, Mapping

from utils.agent import AgentApp, AgentSpec
from utils.llm import LLMRegistry

from ..schemas.coverage_review import CoverageReviewVerdict
from ..schemas.tools import NonBlankString, SimpleStructuredTool, StrictToolModel
from .coverage_registry import CoverageRegistry


ReviewRunner = Callable[[str, Mapping[str, Any], int], CoverageReviewVerdict]


class CoverageReviewerError(RuntimeError):
    """Base error for one isolated coverage reviewer invocation."""


class RetryableCoverageReviewerError(CoverageReviewerError):
    """Transient provider/transport failure that permits same-fingerprint retry."""


class CoverageReviewerContractError(CoverageReviewerError):
    """Non-transient reviewer/schema failure that terminates this Discover attempt."""


class ReviewDiscoveryCoverageInput(StrictToolModel):
    reason: NonBlankString


def _stable_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()




def _evidence_scope_fingerprint_material(
    latest_evaluations: Mapping[str, Any],
) -> dict[str, Any]:
    """Extract evidence-scope metadata that must invalidate old review passes.

    The full latest evaluation payload is already fingerprinted. This explicit
    projection makes the contract reviewable and keeps future schema additions
    for initialization/formal/check/policy metadata visible to tests and audits.
    """

    watched_keys = (
        "initialization",
        "initialization_mode",
        "requested_initial_state",
        "effective_initial_state",
        "requested_initial_vars",
        "effective_initial_vars",
        "formal",
        "formal_bound",
        "formal_bound_origin",
        "formal_assumption_basis_ids",
        "property_kind",
        "canonical_query",
        "check",
        "check_result_sha256",
        "tool_schema_hash",
        "tool_hash",
        "policy",
        "policy_hash",
        "evidence_policy_fingerprint",
    )
    material: dict[str, Any] = {}
    for version_id, evaluation in latest_evaluations.items():
        if not isinstance(evaluation, Mapping):
            continue
        selected = {key: evaluation[key] for key in watched_keys if key in evaluation}
        call_metadata: list[Any] = []
        for key in ("function_calls", "function_call_trace", "call_trace", "trace"):
            calls = evaluation.get(key)
            if not isinstance(calls, list):
                continue
            for call in calls:
                if isinstance(call, Mapping):
                    picked = {watch: call[watch] for watch in watched_keys if watch in call}
                    if picked:
                        call_metadata.append(picked)
        if call_metadata:
            selected["call_metadata"] = call_metadata
        if selected:
            material[str(version_id)] = selected
    return material

def _review_system_prompt(review_kind: str, language: str) -> str:
    chinese = language == "zh-CN"
    role = (
        "semantic coverage auditor"
        if review_kind == "semantic_coverage"
        else "adversarial false-negative auditor"
    )
    language_rule = (
        "Write all explanations, problems, risks, recommendations, and pass criteria in Simplified Chinese. Keep IDs, enum values, tool names, and code in English."
        if chinese
        else "Write explanations in English; keep IDs, enum values, tool names, and code in English."
    )
    focus = (
        "Check clause by clause whether every major NL behavior and valid cue obligation is covered by an equally strong positive proposition, and whether unselected model behavior materially changes the main conclusion."
        if review_kind == "semantic_coverage"
        else "Actively construct counterexamples that could make the current assertions pass incorrectly. Look for missed paths, conditions, guards, effects, hierarchy, initialization, temporal or completion semantics, and incorrect issue projection."
    )
    return f"""You are an independent {role}. You do not participate in the Discover main Agent's reasoning and must not trust its claim of completeness.

{language_rule}

Review objective: {focus}

Keep the current main Agent profile/adapter/provider identity as a wiring constraint outside this prompt. Do not request or imply a hidden reviewer model switch.

The `review_kind` field in the structured output must equal `{review_kind}` exactly.

You have no callable tools. Your only valid response is one direct
`CoverageReviewVerdict` structured object. Never emit `query_model`,
`observe_trace`, `revise_assertion`, or any other function/tool call. Tool names
and argument contracts below are literal data for findings that the Discover
main Agent may execute after this review returns. They are not available to this
reviewer, and you must not call or pre-validate them.

Hard rules:
1. Read the complete NL, FCSTM, raw source, source trace, InputSegments, CoverageRequirements, all behavior-relevant SourceFacts, CoverageUnits, Roots, every latest assertion, and its actual execution record from the input.
2. Enumerate every ID required by `review_contract` in `reviewed_segment_ids`, `reviewed_requirement_ids`, `reviewed_source_fact_ids`, and `reviewed_root_ids`. Each corresponding `review_contract.required_*_ids` list is also the exclusive allowed ID universe for that output field and for the matching `related_*_ids` field in every finding. In particular, `review_contract.required_source_fact_ids` is the only allowed source-fact ID set. When it is empty, `reviewed_source_fact_ids` and every finding's `related_source_fact_ids` must be empty lists. You may inspect and describe other inventory facts by their model behavior or element details in prose, but never copy their inventory IDs into those fields. Still inspect the complete inventory for obvious omissions that materially affect the main NL behavior conclusion.
3. Do not use a predefined defect taxonomy and do not request D01-D12 or any other fixed taxonomy. Discover problem categories openly from this case's evidence.
4. A CoverageRequirement appearing in an assertion basis does not establish semantic coverage. Check whether the assertion preserves the original object, trigger, source state, target state, quantity, direction, order, persistence, completion scope, and time bound. Fail weak propositions.
5. A SourceFact referenced by a Unit has not necessarily been explored. For facts explicitly selected as assertion evidence, check that an executed assertion directly supports each fact. For the remaining inventory, create a blocking finding only when the omission materially changes a major NL behavior or issue conclusion. Do not require exhaustive validation of every model fact.
6. `matches` means only that one assertion is True, not that it was written correctly. `contradicts` means only that one positive proposition is False, not that issue attribution is correct. Review proposition direction and issue projection.
7. Simulation proves only the supplied trace, a local relation proves only a local fact, and bounded formal evidence proves only its stated property within its bounds. Fail evidence that is too weak for the claim.
8. Return `passed=true` only when no semantic omission, weak or misdirected assertion, material false-negative or false-positive risk, critical evidence gap, or incorrect issue projection can affect the main behavior conclusion. Put non-blocking hardening suggestions in `coverage_analysis`; do not block a research run merely to pursue exhaustive perfection.
9. When `passed=false`, every finding must cite at least one current ledger ID from `review_contract` in `related_segment_ids`, `related_requirement_ids`, `related_source_fact_ids`, `related_root_ids`, or `related_assertion_chain_ids`. Every non-empty related ID field must be a subset of its corresponding required ID list in `review_contract`; never cite an ID merely because it appears in the full inventory.
10. Every finding must first state `required_scope`, `observed_scope`, `scope_gap`, `risk`, `routes`, and `pass_criterion`. Explain the semantic scope mismatch before any tool recommendation. `recommended_tools` and `recommended_steps` are optional route aids, not quotas. Use a mandatory tool only when its semantic capability is indispensable; do not fail a ledger merely because a family/tool was not called. `recommended_action` must name at least one current ledger ID from a `related_*_ids` field and the exact object, path, initialization, variable valuation, bound, or condition to inspect. `pass_criterion` / `pass_criteria` must name an observable ledger or model result, not merely say that review passes. Never ask the main Agent to edit Controller projection, `runtime_issue_assessment`, or confirmed status directly. Never use FBMCQ or `read_fbmcq_guide` to interpret NL semantics.
11. If an explicitly in-scope NL behavior is absent from the current model, treat it as a model behavior gap or assertion gap rather than inventing an abstraction-level excuse. Do not strengthen the NL into `only`, every-state, or future-model obligations that the source does not state.
12. Check anti-gaming patterns that can directly create an incorrect main conclusion, including sentinel variables, hard-coded candidate names, cardinality after filtering, weak mappings, inspect-only issue projection, hot-start bypass of required root reachability or entry semantics, bounded-formal overclaim as unbounded proof, and topology positive-path overclaim as executable runtime behavior. Put merely theoretical edge cases that do not affect this case in `coverage_analysis` as optional improvements.
13. Do not access reference/gold data, modify the model, or repair findings for the main Agent. Review only whether the current ledger's major-behavior coverage supports this Discover conclusion. State the coverage boundary and optional improvements in `coverage_analysis`; never claim absolute 100% coverage.
14. A positive conditional obligation does not automatically create an exclusive negative obligation. "When state S receives E it reaches T" requires checking behavior when that condition holds. Unless the same related NL explicitly uses exclusive wording such as `only` or `must not`, do not require that other states receiving E cannot reach T and do not recommend an `is False` or `not(...)` conjunct merely to manufacture an issue.
15. Interpret event-free transitions using FCSTM hierarchical semantics. An `event=None` edge from a composite state may be a completion transition after its submachine reaches final; it does not fire unconditionally in every ordinary cycle. `I_TRANSITION_NEVER_EVENT_TRIGGERED` says only that an event does not trigger the edge. A claim of premature exit must cite executed simulation or formal evidence; structural presence alone is insufficient.
16. This review runs after the complete plan is registered. The Discover main Agent's later tools may only revise an existing assertion chain; they cannot add a CoverageUnit, Root, or assertion chain or register a new complete plan. Every `revise_assertion` step must use an `assertion_chain_id` from `review_contract.required_assertion_chain_ids`. Do not return a finding whose recommendation the main Agent's existing tools cannot implement.
17. Recommended assertions must preserve the positive-bool principle: True means the existing Root is satisfied. If the NL explicitly prohibits behavior, the expression must be True when the prohibited behavior is absent. Never encode the unwanted edge's presence as True and still claim it should project to an issue.
18. Treat each Controller Root and its same-clause CoverageRequirements as the frozen scope of the positive obligation. Do not broaden a source-state-specific Root to every state merely because the NL uses a pronoun such as `it` or `the system`, or because it does not restate the source state in the same sentence. Require all-state behavior only when the related NL explicitly supplies a universal quantifier. Never recommend adding a Unit, Root, or assertion chain to express an inferred broader scope.
19. Inspect-only evidence is never enough to project an issue. If a Root relies only on diagnostics, severity, counts, suggested fixes, mapping coincidence, or an inconclusive confirmation, fail it unless there is a terminal non-diagnostic executable assertion tied to real NL/source scope.
20. For simulation evidence, compare requested and effective initialization. A hot start is sufficient only for local behavior whose precondition is already being in that state with the recorded variables; it cannot prove startup reachability, initial descent, or skipped entry actions. Missing persistent variables or unexplained defaults are scope gaps when they can affect guards or effects.
21. For formal evidence, check property kind, assumptions, finite bound, and bound origin. A `requirement_bound` may support a bounded NL requirement; an `analysis_bound` must remain a finite-horizon limitation. Never let a bounded pass become an unbounded proof.
22. For topology/path evidence, remember that positive paths are guard-agnostic connectivity facts. They can support structure or localization, but they cannot by themselves prove executable runtime reachability, event availability, transition priority, or variable evolution.
23. A proposition that attributes S -> T to event E must not be narrowed to static edge existence merely because its Root, assertion, rationale, or evidence-scope label says transition/relation. Relation-only evidence is insufficient for this event-causal behavior: `transition_exists` proves a declared edge, not event consumption or the runtime target after hierarchical scheduling. Require an ordered simulation record or another equal-strength executable route. For simulation, S must hold before the event cycle, E must be supplied and consumed rather than unconsumed (`E in consumed_events` and `E not in unconsumed_events`), and T must hold after it. FCSTM `consumed_events` is a hierarchical execution observation, not a one-use resource counter: the same caller-supplied event may be recorded more than once in one cycle while nested and ancestor-level forced transitions process it. Never require `consumed_events.count(E) == 1`; duplicate consumed labels alone are neither a model issue nor evidence of repeated external consumption. Reject a trace where a leading empty cycle or completion/event-free transition reaches T before E; final-state coincidence is not event-causality evidence. Recommend a complete hot start with E in the first caller cycle, or another equal-strength route, and state these observable conditions in the pass criterion.

The following are literal data contracts for `recommended_steps.suggested_arguments` inside a finding, not tools available to this reviewer. Replace example values with real IDs, expressions, and model elements from the current ledger:
- query_model: {{"query_kind":"transitions","name_contains":null,"offset":0,"limit":50,"root_node_ids":["ROOT-..."],"reason":"..."}}; `query_kind` must be one of states/events/transitions/variables/diagnostics.
- observe_trace cold start: {{"question":"...","root_node_ids":["ROOT-..."],"cycles":[[],["Root.Event"]],"initial_state":null,"initial_vars":null,"reason":"..."}}
- observe_trace local hot start: {{"question":"...","root_node_ids":["ROOT-..."],"cycles":[["Root.Event"]],"initial_state":"Root.Source","initial_vars":{{}},"reason":"..."}}
- lookup_source_trace: {{"element_refs":["state:Root.Target"],"direction":"fcstm_to_source","reason":"..."}}; `direction` must be one of fcstm_to_source/source_to_fcstm.
- read_fbmcq_guide: {{"reason":"..."}}
- register_coverage_plan: {{"plan":{{"segment_dispositions":[],"fact_dispositions":[],"coverage_units":[],"proposition_roots":[],"logical_assertions":[],"rationale":"..."}},"reason":"..."}}; a real recommendation must provide a complete CoveragePlan that preserves all existing obligations and applies the requested revision, not a delta or `plan_change`.
- revise_assertion: {{"assertion_chain_id":"ASSERT-...","assert":"one complete positive Python bool expression","required_function_families":["simulation"],"reason":"..."}}; omit `required_function_families` only when the evidence route is unchanged, otherwise provide the complete current route rather than a quota.
- eval_assert: {{"assert":"the exact latest assertion expression","reason":"..."}}

A blocking finding should be shaped around semantic scope first, for example:
{{"finding_id":"REVIEW-GAP-001","category":"weak_or_misdirected_assertion","related_root_ids":["ROOT-..."],"required_scope":"all admissible bounded completion paths from the named state","observed_scope":"one recorded initialization and one event sequence","scope_gap":"unexamined completion branches may violate the Root while the current assertion passes","risk":"the run may publish a false zero-issue conclusion for a universal Root","routes":["Use a formal response property with a recorded requirement_bound or analysis_bound, or accept any admissible concrete counterexample as sufficient contradiction evidence."],"pass_criterion":"latest records show terminal evidence whose assumptions and bound match the Root scope"}}
"""


class LLMCoverageReviewRunner:
    """Run isolated structured reviewers through the repository Agent framework."""

    def __init__(
        self,
        *,
        llm_registry: LLMRegistry,
        profile: str,
        audit_root: Path,
        content_language: str,
        limits: Mapping[str, int | float] | None = None,
    ) -> None:
        self.llm_registry = llm_registry
        self.profile = profile
        self.audit_root = audit_root
        self.content_language = content_language
        self.limits = dict(limits or {})

    def __call__(
        self, review_kind: str, payload: Mapping[str, Any], attempt_no: int
    ) -> CoverageReviewVerdict:
        review_dir = self.audit_root / f"review-{attempt_no:03d}-{review_kind}"
        review_dir.mkdir(parents=True, exist_ok=False)
        spec = AgentSpec(
            name=f"paper1-discover-{review_kind}-reviewer",
            system_prompt=_review_system_prompt(review_kind, self.content_language),
            tools=(),
            output_schema=CoverageReviewVerdict,
            limits=self.limits or None,
            require_tool_call=False,
            retry_missing_structured_output=True,
        )
        app = AgentApp.from_registry(
            spec,
            self.llm_registry,
            profile=self.profile,
            model_options={"streaming": True, "max_retries": 0},
        )
        try:
            result = contextvars.Context().run(
                app.run,
                json.dumps(payload, ensure_ascii=False, sort_keys=True),
                renderer="quiet",
                log_level="INFO",
                audit_out=review_dir / "audit.jsonl",
                result_out=review_dir / "result.json",
                compact_trigger_ratio=0.85,
            )
        except Exception as exc:  # noqa: BLE001 - normalize provider/runtime drift
            _raise_classified_reviewer_error(review_kind, exc)
        if result.status != "success" or not result.real_llm:
            _raise_classified_reviewer_error(
                review_kind,
                result.error or result.status,
            )
        try:
            verdict = result.require_output()
            if not isinstance(verdict, CoverageReviewVerdict):
                verdict = CoverageReviewVerdict.model_validate(verdict)
        except Exception as exc:  # noqa: BLE001 - schema failure is non-transient
            raise CoverageReviewerContractError(
                f"coverage_reviewer_contract_failed:{review_kind}:{exc}"
            ) from exc
        if verdict.review_kind != review_kind:
            raise CoverageReviewerContractError(
                f"coverage_reviewer_kind_mismatch:{review_kind}:{verdict.review_kind}"
            )
        return verdict


def _raise_classified_reviewer_error(review_kind: str, error: Any) -> None:
    rendered = json.dumps(error, ensure_ascii=False, sort_keys=True, default=str)
    structured_tokens = _structured_error_tokens(error)
    contract_markers = (
        "schema",
        "validation",
        "structured_output",
        "response_format",
        "review_kind",
        "contract",
        "invalid_json",
    )
    transient_markers = (
        "provider_error",
        "remoteprotocolerror",
        "timeout",
        "rate_limit",
        "connection_error",
        "transport_error",
        "http_429",
        "http_500",
        "http_502",
        "http_503",
        "http_504",
    )
    if any(marker in token for token in structured_tokens for marker in contract_markers):
        error_type: type[CoverageReviewerError] = CoverageReviewerContractError
    elif any(
        marker in token for token in structured_tokens for marker in transient_markers
    ):
        error_type = RetryableCoverageReviewerError
    else:
        exception_type_name = type(error).__name__.lower()
        transient_exception_types = {
            "connectionerror",
            "connecterror",
            "connecttimeout",
            "readtimeout",
            "writetimeout",
            "pooltimeout",
            "remoteprotocolerror",
            "networkerror",
            "transporterror",
        }
        fallback = f"{type(error).__name__}:{error}".lower()
        precise_transient_patterns = (
            r"remoteprotocolerror",
            r"(?:read|connect|pool)timeout",
            r"connection (?:reset|refused|aborted)",
            r"rate limit",
            r"status code (?:429|50[0234])",
            r"incomplete chunked read",
            r"temporarily unavailable",
            r"service unavailable",
        )
        is_retryable_exception = exception_type_name in transient_exception_types
        is_retryable_message = any(
            re.search(pattern, fallback) for pattern in precise_transient_patterns
        )
        error_type = (
            RetryableCoverageReviewerError
            if is_retryable_exception or is_retryable_message
            else CoverageReviewerContractError
        )
    raise error_type(f"coverage_reviewer_failed:{review_kind}:{rendered}")


def _structured_error_tokens(value: Any) -> tuple[str, ...]:
    tokens: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            if str(key).lower() in {"code", "type", "status", "source", "category"}:
                tokens.append(str(item).lower())
            tokens.extend(_structured_error_tokens(item))
    elif isinstance(value, (list, tuple)):
        for item in value:
            tokens.extend(_structured_error_tokens(item))
    return tuple(tokens)


class CoverageReviewGate:
    """Append-only dual-review gate bound to one mutable assertion registry."""

    def __init__(
        self,
        *,
        registry: CoverageRegistry,
        task_snapshot: Mapping[str, Any],
        runner: ReviewRunner,
    ) -> None:
        self.registry = registry
        self.task_snapshot = json.loads(json.dumps(task_snapshot, ensure_ascii=False))
        self.runner = runner
        self.attempt_count = 0
        self.latest_result: dict[str, Any] | None = None
        self.terminal_failure = False

    def state_fingerprint(self) -> str:
        latest_evaluations: dict[str, Any] = {}
        for version in self.registry.latest_versions():
            attempts = self.registry.evaluations.get(version.assertion_version_id, [])
            latest_evaluations[version.assertion_version_id] = (
                attempts[-1] if attempts else None
            )
        return _stable_sha256(
            {
                "coverage_units": self.registry.coverage_units,
                "roots": self.registry.roots,
                "latest_assertions": [
                    item.to_record() for item in self.registry.latest_versions()
                ],
                "latest_evaluations": latest_evaluations,
                "evidence_scope_metadata": _evidence_scope_fingerprint_material(
                    latest_evaluations
                ),
                "requirement_assertion_chains": {
                    key: sorted(value)
                    for key, value in sorted(
                        self.registry.requirement_assertion_chains.items()
                    )
                },
                "source_fact_assertion_chains": {
                    key: sorted(value)
                    for key, value in sorted(
                        self.registry.source_fact_assertion_chains.items()
                    )
                },
            }
        )

    def current_passed(self) -> bool:
        return bool(
            self.latest_result
            and self.latest_result.get("passed") is True
            and self.latest_result.get("reviewed_state_fingerprint")
            == self.state_fingerprint()
        )

    def has_terminal_failure(self) -> bool:
        return self.terminal_failure

    def review(self, *, reason: str) -> dict[str, Any]:
        if self.terminal_failure and self.latest_result is not None:
            return json.loads(json.dumps(self.latest_result, ensure_ascii=False))
        if not self.registry.plan_registered:
            return self._reject(reason, ["coverage_plan_not_registered"])
        missing = self.registry.missing_latest_required_assertions()
        incomplete = self.registry.incomplete_latest_required_assertions()
        if missing or incomplete:
            errors = []
            if missing:
                errors.append("latest_required_assertions_not_executed")
            if incomplete:
                errors.append("latest_required_assertions_inconclusive")
            return self._reject(reason, errors)

        fingerprint = self.state_fingerprint()
        projection = self.registry.project_roots()
        payload = {
            "schema_version": "paper1.discovery_coverage_review_input.v1",
            "reviewed_state_fingerprint": fingerprint,
            "task_snapshot": self.task_snapshot,
            "registered_plan": {
                "coverage_units": self.registry.coverage_units,
                "proposition_roots": self.registry.roots,
                "latest_assertions": [
                    item.to_record() for item in self.registry.latest_versions()
                ],
            },
            "latest_evaluations": {
                version.assertion_version_id: (
                    self.registry.evaluations[version.assertion_version_id][-1]
                    if self.registry.evaluations.get(version.assertion_version_id)
                    else None
                )
                for version in self.registry.latest_versions()
            },
            "controller_projection_before_review": projection,
            "review_contract": {
                "required_segment_ids": sorted(self.registry.input_segment_ids),
                "required_requirement_ids": sorted(self.registry.coverage_requirements),
                "required_source_fact_ids": sorted(
                    self.registry.selected_source_fact_ids()
                ),
                "required_root_ids": sorted(self.registry.roots),
                "required_assertion_chain_ids": sorted(self.registry.chains),
                "pass_requires": [
                    "both_independent_reviews_pass",
                    "every_required_id_is_explicitly_reviewed",
                    "no_actionable_findings",
                    "review_fingerprint_matches_current_latest_ledger",
                ],
            },
        }
        reusable_verdicts: dict[str, CoverageReviewVerdict] = {}
        previous = self.latest_result or {}
        if (
            previous.get("execution_status") == "retryable_reviewer_failure"
            and previous.get("reviewed_state_fingerprint") == fingerprint
        ):
            reusable_verdicts = {
                verdict.review_kind: verdict
                for verdict in (
                    CoverageReviewVerdict.model_validate(item)
                    for item in previous.get("completed_review_verdicts", [])
                )
            }
        verdicts: list[CoverageReviewVerdict] = []
        for review_kind in (
            "semantic_coverage",
            "adversarial_falsification",
        ):
            if review_kind in reusable_verdicts:
                verdicts.append(reusable_verdicts[review_kind])
                continue
            self.attempt_count += 1
            try:
                verdicts.append(self.runner(review_kind, payload, self.attempt_count))
            except RetryableCoverageReviewerError as exc:
                return self._reviewer_retry_required(
                    reason=reason,
                    fingerprint=fingerprint,
                    review_kind=review_kind,
                    error=exc,
                    completed_verdicts=verdicts,
                )
            except Exception as exc:  # noqa: BLE001 - fail closed on bad review contracts
                return self._reviewer_contract_failed(
                    reason=reason,
                    fingerprint=fingerprint,
                    review_kind=review_kind,
                    error=exc,
                    completed_verdicts=verdicts,
                )

        expected = {
            "segment": self.registry.input_segment_ids,
            "requirement": set(self.registry.coverage_requirements),
            "source_fact": self.registry.selected_source_fact_ids(),
            "root": set(self.registry.roots),
        }
        programmatic_errors: list[str] = []
        invalid_finding_keys: set[tuple[str, str]] = set()
        scope_filtered_finding_keys: set[tuple[str, str]] = set()
        for verdict in verdicts:
            actual = {
                "segment": set(verdict.reviewed_segment_ids),
                "requirement": set(verdict.reviewed_requirement_ids),
                "source_fact": set(verdict.reviewed_source_fact_ids),
                "root": set(verdict.reviewed_root_ids),
            }
            for label, required_ids in expected.items():
                if actual[label] != required_ids:
                    missing_ids = sorted(required_ids - actual[label])
                    unknown_ids = sorted(actual[label] - required_ids)
                    programmatic_errors.append(
                        f"{verdict.review_kind}_{label}_review_set_mismatch:"
                        f"missing={','.join(missing_ids)}:unknown={','.join(unknown_ids)}"
                    )
            known_ids = {
                "segment": expected["segment"],
                "requirement": expected["requirement"],
                "source_fact": expected["source_fact"],
                "root": expected["root"],
                "assertion_chain": set(self.registry.chains),
            }
            for finding in verdict.findings:
                finding_key = (verdict.review_kind, finding.finding_id)
                finding_ids = {
                    "segment": set(finding.related_segment_ids),
                    "requirement": set(finding.related_requirement_ids),
                    "source_fact": set(finding.related_source_fact_ids),
                    "root": set(finding.related_root_ids),
                    "assertion_chain": set(finding.related_assertion_chain_ids),
                }
                for label, ids in finding_ids.items():
                    unknown = sorted(ids - known_ids[label])
                    if unknown:
                        invalid_finding_keys.add(finding_key)
                        programmatic_errors.append(
                            f"{verdict.review_kind}_finding_unknown_{label}_ids:"
                            f"finding={finding.finding_id}:unknown={','.join(unknown)}"
                        )
                if _finding_strengthens_frozen_nl(
                    finding,
                    _finding_nl_scopes(finding, self.task_snapshot),
                ):
                    invalid_finding_keys.add(finding_key)
                    scope_filtered_finding_keys.add(finding_key)
                for error in _finding_step_contract_errors(
                    finding,
                    known_assertion_chain_ids=set(self.registry.chains),
                ):
                    invalid_finding_keys.add(finding_key)
                    programmatic_errors.append(
                        f"{verdict.review_kind}_{error}:"
                        f"finding={finding.finding_id}"
                    )

        def verdict_effectively_passed(verdict: CoverageReviewVerdict) -> bool:
            valid_findings = [
                finding
                for finding in verdict.findings
                if (verdict.review_kind, finding.finding_id)
                not in invalid_finding_keys
            ]
            if valid_findings:
                return False
            if verdict.passed:
                return True
            return bool(verdict.findings) and all(
                (verdict.review_kind, finding.finding_id)
                in scope_filtered_finding_keys
                for finding in verdict.findings
            )

        passed = not programmatic_errors and all(
            verdict_effectively_passed(item) for item in verdicts
        )
        finding_actions = [
            finding.model_dump(mode="json")
            for verdict in verdicts
            for finding in verdict.findings
            if (verdict.review_kind, finding.finding_id)
            not in invalid_finding_keys
        ]
        previous = self.latest_result or {}
        if (
            programmatic_errors
            and previous.get("execution_status") == "completed"
            and previous.get("reviewed_state_fingerprint") == fingerprint
            and previous.get("programmatic_errors")
        ):
            return self._reviewer_contract_failed(
                reason=reason,
                fingerprint=fingerprint,
                review_kind="programmatic_contract",
                error=CoverageReviewerContractError(
                    "repeated_programmatic_review_mismatch:"
                    + "|".join(programmatic_errors)
                ),
                completed_verdicts=verdicts,
            )
        result = {
            "execution_status": "completed",
            "passed": passed,
            "reviewed_state_fingerprint": fingerprint,
            "review_verdicts": [item.model_dump(mode="json") for item in verdicts],
            "programmatic_errors": programmatic_errors,
            "required_actions": [
                *finding_actions,
                *_programmatic_review_actions(programmatic_errors),
            ],
            "reason": reason,
            "limitations": [] if passed else ["semantic_coverage_review_failed"],
        }
        record = self.registry.append_record(
            "discovery_coverage_review_completed", result
        )
        result["record_id"] = record["record_id"]
        self.latest_result = json.loads(json.dumps(result, ensure_ascii=False))
        self.registry.latest_projection = None
        return result

    def _reviewer_retry_required(
        self,
        *,
        reason: str,
        fingerprint: str,
        review_kind: str,
        error: Exception,
        completed_verdicts: list[CoverageReviewVerdict],
    ) -> dict[str, Any]:
        """Return a structured retry action instead of crashing the top-level Agent.

        Provider streaming failures and transient reviewer runtime errors are
        infrastructure failures, not evidence that the current ledger passed or
        failed semantically.  The gate therefore appends a failed review record,
        preserves the assertion/plan ledger, and asks the Agent to retry the same
        `review_discovery_coverage` call against the unchanged fingerprint.
        """

        previous = self.latest_result or {}
        if (
            previous.get("execution_status") == "retryable_reviewer_failure"
            and previous.get("reviewed_state_fingerprint") == fingerprint
        ):
            return self._reviewer_contract_failed(
                reason=reason,
                fingerprint=fingerprint,
                review_kind=review_kind,
                error=CoverageReviewerContractError(
                    "repeated_reviewer_infrastructure_failure:"
                    f"previous={previous.get('failed_review_kind')}:current={review_kind}"
                ),
                completed_verdicts=completed_verdicts,
            )

        error_type = type(error).__name__
        error_message = str(error)
        result = {
            "execution_status": "retryable_reviewer_failure",
            "passed": False,
            "reviewed_state_fingerprint": fingerprint,
            "failed_review_kind": review_kind,
            "completed_review_verdicts": [
                item.model_dump(mode="json") for item in completed_verdicts
            ],
            "errors": [f"coverage_reviewer_retryable_failure:{review_kind}:{error_type}"],
            "required_actions": [
                {
                    "action_id": "REVIEW-INFRA-RETRY-001",
                    "action_kind": "reviewer_infrastructure_retry",
                    "reviewed_state_fingerprint": fingerprint,
                    "failed_review_kind": review_kind,
                    "coverage_dimensions": ["reviewer_infrastructure"],
                    "problem": (
                        "Independent coverage reviewer failed before returning a "
                        "structured verdict; the semantic ledger has not been "
                        "accepted as covered."
                    ),
                    "missed_behavior_risk": (
                        "Treating a provider or streaming interruption as a tool "
                        "exception aborts the top-level Agent and loses the chance "
                        "to retry without changing the evidence ledger."
                    ),
                    "recommended_tools": ["review_discovery_coverage"],
                    "recommended_action": (
                        "Keep the coverage plan, latest assertions, and evaluations "
                        "unchanged, then call review_discovery_coverage again for "
                        "the same reviewed_state_fingerprint. Do not revise "
                        "assertions unless a later successful reviewer returns "
                        "semantic findings."
                    ),
                    "pass_criteria": (
                        "A later review_discovery_coverage call on the same current "
                        "fingerprint returns execution_status=completed with both "
                        "reviewers producing structured verdicts and no retryable "
                        "reviewer failure."
                    ),
                    "record_language": "en-US",
                    "error_type": error_type,
                    "error_message": error_message,
                }
            ],
            "reason": reason,
            "limitations": [
                "semantic_coverage_review_failed",
                "reviewer_infrastructure_retry_required",
            ],
        }
        record = self.registry.append_record(
            "discovery_coverage_review_retry_required", result
        )
        result["record_id"] = record["record_id"]
        self.latest_result = json.loads(json.dumps(result, ensure_ascii=False))
        return result

    def _reviewer_contract_failed(
        self,
        *,
        reason: str,
        fingerprint: str,
        review_kind: str,
        error: Exception,
        completed_verdicts: list[CoverageReviewVerdict],
    ) -> dict[str, Any]:
        result = {
            "execution_status": "reviewer_contract_failure",
            "passed": False,
            "reviewed_state_fingerprint": fingerprint,
            "failed_review_kind": review_kind,
            "completed_review_verdicts": [
                item.model_dump(mode="json") for item in completed_verdicts
            ],
            "errors": [
                f"coverage_reviewer_contract_failure:{review_kind}:"
                f"{type(error).__name__}"
            ],
            "required_actions": [
                {
                    "action_id": "REVIEW-INFRA-STOP-001",
                    "action_kind": "reviewer_contract_failure",
                    "reviewed_state_fingerprint": fingerprint,
                    "failed_review_kind": review_kind,
                    "recommended_tools": [],
                    "recommended_action": (
                        "Stop the current Discover attempt and preserve its audit "
                        "artifacts. This deterministic reviewer/schema failure cannot "
                        "be repaired by changing the semantic ledger or repeatedly "
                        "calling review_discovery_coverage."
                    ),
                    "pass_criteria": (
                        "A later clean run uses a corrected reviewer contract and both "
                        "reviewers return valid structured verdicts."
                    ),
                    "error_type": type(error).__name__,
                    "error_message": str(error),
                }
            ],
            "reason": reason,
            "limitations": [
                "semantic_coverage_review_failed",
                "reviewer_contract_failure",
            ],
        }
        record = self.registry.append_record(
            "discovery_coverage_review_contract_failed", result
        )
        result["record_id"] = record["record_id"]
        self.latest_result = json.loads(json.dumps(result, ensure_ascii=False))
        self.terminal_failure = True
        return result

    def _reject(self, reason: str, errors: list[str]) -> dict[str, Any]:
        result = {
            "execution_status": "prerequisite_required",
            "passed": False,
            "errors": errors,
            "required_actions": _review_prerequisite_actions(errors),
            "reason": reason,
            "limitations": ["review_requires_terminal_registered_assertions"],
        }
        self.registry.append_record("discovery_coverage_review_rejected", result)
        return result


def _finding_strengthens_frozen_nl(
    finding: Any,
    frozen_nl_scopes: tuple[str, ...],
) -> bool:
    suggested_arguments = [
        step.suggested_arguments for step in finding.recommended_steps
    ]
    action = "\n".join(
        [
            finding.recommended_action,
            finding.pass_criteria,
            json.dumps(suggested_arguments, ensure_ascii=False, sort_keys=True),
        ]
    ).lower()
    quantifier_groups = (
        (
            (r"\bonly\b", r"只能", r"仅允许"),
            (r"\bonly\b", r"只能", r"仅允许"),
        ),
        (
            (
                r"\b(?:all|every|each)[- ]states?\b",
                r"(?:所有|全部|每个|任意)状态",
            ),
            (
                r"\b(?:all|every|each)[- ]states?\b",
                r"(?:所有|全部|每个|任意)状态",
            ),
        ),
        (
            (r"future[- ]model", r"未来模型"),
            (r"future[- ]model", r"未来模型"),
        ),
    )
    for action_patterns, nl_patterns in quantifier_groups:
        action_uses_quantifier = any(
            re.search(pattern, action, re.I) for pattern in action_patterns
        )
        every_scope_authorizes = bool(frozen_nl_scopes) and all(
            any(re.search(pattern, scope, re.I) for pattern in nl_patterns)
            for scope in frozen_nl_scopes
        )
        if action_uses_quantifier and not every_scope_authorizes:
            return True
    negative_action_patterns = (
        r"\bis\s+false\b",
        r"\bmust\s+not\b",
        r"\bshall\s+not\b",
        r"\bnever\b",
        r"\bnot\s+(?:transition_exists|simulate|fbmcq|effects|guards_overlap)\b",
        r"不应",
        r"不得",
        r"禁止",
        r"不允许",
    )
    negative_nl_patterns = (
        r"\bonly\b",
        r"\bmust\s+not\b",
        r"\bshall\s+not\b",
        r"\bnever\b",
        r"\bnot\b",
        r"只能",
        r"仅允许",
        r"不应",
        r"不得",
        r"禁止",
        r"不允许",
    )
    suggested_assertions = "\n".join(
        str(arguments.get("assert", ""))
        for arguments in suggested_arguments
        if isinstance(arguments, Mapping)
    ).lower()
    action_adds_negative_obligation = any(
        re.search(pattern, suggested_assertions, re.I)
        for pattern in negative_action_patterns
    )
    every_scope_authorizes_negative = bool(frozen_nl_scopes) and all(
        any(re.search(pattern, scope, re.I) for pattern in negative_nl_patterns)
        for scope in frozen_nl_scopes
    )
    return action_adds_negative_obligation and not every_scope_authorizes_negative


def _finding_step_contract_errors(
    finding: Any,
    *,
    known_assertion_chain_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    if "register_coverage_plan" in set(finding.recommended_tools):
        errors.append("finding_cannot_reregister_plan_after_review")
    for step in finding.recommended_steps:
        if step.tool == "register_coverage_plan":
            errors.append("finding_cannot_reregister_plan_after_review")
            continue
        if step.tool != "revise_assertion":
            continue
        assertion_chain_id = step.suggested_arguments.get("assertion_chain_id")
        if assertion_chain_id not in known_assertion_chain_ids:
            errors.append(
                "finding_unknown_revise_assertion_chain:"
                f"unknown={assertion_chain_id}"
            )
    return sorted(set(errors))


def _finding_nl_scopes(
    finding: Any, task_snapshot: Mapping[str, Any]
) -> tuple[str, ...]:
    current_records = task_snapshot.get("current_records", {})
    if not isinstance(current_records, Mapping):
        return ()
    selected: list[str] = []
    requirement_ids = set(finding.related_requirement_ids)
    for requirement in current_records.get("coverage_requirements", []):
        if not isinstance(requirement, Mapping):
            continue
        if str(requirement.get("requirement_id", "")) in requirement_ids:
            selected.append(str(requirement.get("clause_text", "")))
    if not selected:
        segment_ids = set(finding.related_segment_ids)
        for segment in current_records.get("input_segments", []):
            if not isinstance(segment, Mapping):
                continue
            if str(segment.get("segment_id", "")) in segment_ids:
                selected.append(str(segment.get("text", "")))
    return tuple(item for item in selected if item)


def _programmatic_review_actions(errors: list[str]) -> list[dict[str, Any]]:
    """Give the main Agent a concrete recovery path for reviewer ID omissions."""

    return [
        {
            "action_id": f"REVIEW-CONTRACT-{ordinal:03d}",
            "action_kind": "reviewer_contract_retry",
            "coverage_dimensions": ["reviewer_infrastructure"],
            "problem": error,
            "missed_behavior_risk": (
                "The independent reviewer did not explicitly close the complete "
                "Controller-required ID set, so a full-coverage claim is unsupported."
            ),
            "recommended_action": (
                "Keep the ledger unchanged and call review_discovery_coverage again. "
                "The replacement review must explicitly enumerate every required ID; "
                "if the mismatch repeats, end the run as reviewer-infrastructure failure."
            ),
            "recommended_tools": ["review_discovery_coverage"],
            "pass_criteria": (
                "Both reviewers enumerate exactly every required Segment, Requirement, "
                "SourceFact, and Root ID with no missing or unknown ID."
            ),
            "record_language": "en-US",
        }
        for ordinal, error in enumerate(errors, start=1)
    ]


def _review_prerequisite_actions(errors: list[str]) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    for ordinal, error in enumerate(errors, start=1):
        if error == "coverage_plan_not_registered":
            tools = ["register_coverage_plan"]
            action = (
                "Do not call review_discovery_coverage again. Read the latest "
                "register_coverage_plan required_actions, correct the complete plan "
                "while preserving every frozen NL obligation, and call "
                "register_coverage_plan. Use only the SourceFacts relevant to the "
                "major NL behavior being checked."
            )
            criteria = "register_coverage_plan returns accepted=true."
        elif error == "latest_required_assertions_not_executed":
            tools = ["eval_assert"]
            action = (
                "Execute every missing latest required assertion exactly as registered."
            )
            criteria = "No latest required assertion remains without an evaluation."
        else:
            tools = ["revise_assertion", "eval_assert"]
            action = (
                "Revise each inconclusive latest assertion without weakening its "
                "obligation, then execute every new latest version."
            )
            criteria = (
                "Every latest required assertion has a terminal evidence-backed bool."
            )
        actions.append(
            {
                "action_id": f"REVIEW-PREREQ-{ordinal:03d}",
                "error": error,
                "problem": (
                    "The independent reviewers cannot run because a required "
                    "Discover prerequisite is not yet closed."
                ),
                "recommended_tools": tools,
                "recommended_action": action,
                "coverage_improvement": (
                    "Following this action closes the actual prerequisite instead "
                    "of repeating a review call that cannot inspect the ledger."
                ),
                "pass_criteria": criteria,
            }
        )
    return actions


def build_tool(gate: CoverageReviewGate) -> SimpleStructuredTool:
    """Build the mandatory semantic-completeness review tool for Discover."""

    def review_discovery_coverage(reason: str) -> dict[str, Any]:
        """Purpose
        -------
        Independently review whether the current Discover ledger covers the
        major behaviors well enough to support this run's conclusion.

        When to use
        -----------
        This is a peer business tool at the same level as ``eval_assert``.
        Call it after every latest required assertion has been executed to a
        terminal bool. Final submission is allowed only when it returns
        ``passed=true`` and its ``reviewed_state_fingerprint`` still matches
        the current ledger.

        When not to use
        ----------------
        Do not call it before coverage-plan registration or while any latest
        assertion is unexecuted or inconclusive. Never reuse an old pass after
        a later revision or evaluation changes the ledger.

        Parameters
        ----------
        ``reason`` is the natural-language rationale for starting this review
        and is copied verbatim into an append-only record. There are no path,
        model, ID-list, or verdict inputs, so the main Agent cannot alter the
        review scope.

        Returns
        -------
        Returns ``passed``, the ledger fingerprint, two complete structured
        verdicts, programmatic ID-closure errors, ``required_actions``, and the
        record ID. Every semantic finding contains related ledger IDs, the
        current gap, false-negative risk, existing recommended tools, concrete
        follow-up steps, and observable pass criteria. Reviewer-infrastructure
        actions are bound to the fingerprint and review kind and never invent
        semantic ledger IDs.

        Execution
        ---------
        The tool sends the complete NL, FCSTM, raw source, source trace, all
        InputSegments, CoverageRequirements, SourceFacts, CoverageUnits, Roots,
        latest assertions, actual execution traces, and Controller projection
        to two isolated LLM reviewers with no callable tools. One audits
        semantic coverage clause by clause; the other actively constructs
        false-negative and false-positive counterexamples. The Controller
        supplies neither a fixed defect taxonomy nor predefined issues.

        Failure semantics
        -----------------
        Fail closed when no plan is registered or any latest assertion is
        unexecuted or inconclusive. An old pass is invalid if either reviewer
        reports a gap, omits a required Segment, Requirement, SourceFact, or
        Root ID, or the ledger changes through revision or evaluation after the
        review. The Agent runtime transparently retries a temporary provider or
        stream failure at most twice with the same profile and request. If all
        retries fail, the tool preserves any verdict completed in that round
        and appends a structured record with ``passed=false`` and
        ``execution_status=retryable_reviewer_failure``. Retry the review without
        changing the current coverage-plan, assertion, or evaluation ledger.
        A failed review is not a terminal result: complete its
        ``required_actions`` or retry, then review again. Deterministic contract
        failures such as a schema-invalid verdict or wrong review kind return
        ``reviewer_contract_failure`` and terminate the current Discover attempt;
        do not misclassify and repeatedly retry them as temporary provider
        failures.

        Method-boundary calibration
        ---------------------------
        Every finding must be executable with existing capabilities and must
        first state required semantic scope, observed evidence scope, the scope
        gap, risk, equal-strength recovery routes, and observable pass criteria.
        Tool recommendations are optional route aids, not quotas; require a
        tool only when its semantic capability is indispensable. Do not recommend
        FBMCQ for interpreting NL, ask the main Agent
        to edit Controller projection state, or cite IDs outside
        ``review_contract``. If an explicitly in-scope NL behavior is absent
        from the model, treat it as a model-behavior or assertion gap rather
        than inventing an abstraction-level excuse. Do not strengthen the NL
        into ``only``, every-state, future-model, or unauthorized negative
        obligations. Calibrate event-free edges from composite states as
        completion transitions; structural presence alone does not prove that
        an edge fires immediately in an ordinary cycle. After review, only an
        existing assertion chain may be revised. Do not recommend adding Units,
        Roots, or chains or registering a new plan. Programmatically invalid
        findings are not forwarded to the main Agent. Reviewers must attack
        anti-gaming coverage based on sentinel variables, hard-coded candidate
        names, or cardinality after filtering. The complete SourceFact inventory
        may inform prose analysis, but only IDs in
        ``review_contract.required_source_fact_ids`` may appear in
        ``reviewed_source_fact_ids`` or a finding's ``related_source_fact_ids``;
        if that required list is empty, both output fields must remain empty.
        Reviewers must also check inspect-only projection, hot-start bypass,
        event-causality ordering and consumption, bounded-formal overclaim, and
        topology/path overclaim. A matching final state reached before an
        unconsumed input event cannot prove that the event caused the transition.

        Evidence limitations
        --------------------
        A reviewer pass applies only to the complete current frozen task and
        evidence ledger supplied as input. Any later ledger change invalidates
        it. The review does not access hidden gold data and does not replace
        downstream experimental evaluation.

        Permissions
        -----------
        Read only the current run's frozen inputs and append-only Discover
        ledger. Internal reviewers have no tools, files, network,
        reference/gold, Repair, Confirm, or model-mutation access.

        Examples
        --------
        ``{"reason":"All latest assertions are terminal; independently attack omissions and weak evidence and recommend concrete follow-up checks."}``
        """

        return gate.review(reason=reason)

    return SimpleStructuredTool(
        func=review_discovery_coverage,
        name="review_discovery_coverage",
        description=review_discovery_coverage.__doc__ or "review_discovery_coverage",
        args_schema=ReviewDiscoveryCoverageInput,
    )
