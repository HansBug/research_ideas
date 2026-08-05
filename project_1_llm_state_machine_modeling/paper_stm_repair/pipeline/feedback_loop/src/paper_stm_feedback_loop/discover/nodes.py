from __future__ import annotations

import json
import re
import time
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any, Protocol, TypeVar, cast

from pydantic import BaseModel

from paper_stm_feedback_loop.assertions import (
    AssertionChecker,
    InMemorySealedStore,
    build_eval_environment,
)
from paper_stm_feedback_loop.assertions.fbmcq import formal_query_causality
from paper_stm_feedback_loop.assertions.pyfcstm_adapter import check_fcstm
from paper_stm_feedback_loop.assertions.predicate_api import (
    PREDICATE_FAMILIES,
    PSEUDO_INITIAL,
)
from paper_stm_feedback_loop.common.nl_segmentation import resolve_nl_segments
from paper_stm_feedback_loop.common.refs import reference_matches

from . import prompts, renderer
from .dependencies import (
    blocked_by,
    cross_requirement_dependencies,
    dependency_cycles,
    execution_order,
    missing_dependency_references,
    orphan_preconditions,
)
from .capability import (
    anchors_at_initialization,
    called_evidence_functions,
    declared_path_bindings,
    initialization_anchored_findings,
    redundant_proposal_findings,
    termination_proposal_findings,
    condition_non_vacuity_findings,
    mandatory_waiver,
    placeholder_bindings,
    source_omitting_response_calls,
    unresolved_reference_findings,
)
from .predicates import (
    misspelled_binding_findings,
    procedure_mismatch,
    unmodelled_claim_paths,
)
from .schemas import (
    AdjudicatedIssue,
    AssertionCheckPublic,
    AssertionExecutionPublic,
    AssertionResult,
    AssertionReview,
    AssertionScript,
    AttributionBinding,
    AttributionProjection,
    DiscoverAdjudication,
    DiscoverCompleted,
    DiscoverGraphState,
    DiscoverInput,
    DiscoverRunIdentity,
    FrozenDiscoverInputs,
    CoverageGap,
    ExcludedObservation,
    LLMCallRecord,
    NodeExecutionRecord,
    ReleasedAssertionResults,
    RequirementCoverageProjection,
    RequirementReview,
    RequirementSet,
    RevisionFeedback,
    RevisionLedgerEvent,
    RunFailure,
    SealedAssertionReceipt,
)
from .utils import sha256_data, sha256_text

T = TypeVar("T", bound=BaseModel)

MAX_REQUIREMENT_REVIEW_REPAIRS = 5
#: Deterministic RequirementSet contract violations the splitter may repair
#: before the run gives up.  Mirrors MAX_ASSERTION_CONTRACT_REPAIRS.
MAX_REQUIREMENT_CONTRACT_REPAIRS = 5
MAX_ASSERTION_REVIEW_REPAIRS = 5
MAX_ASSERTION_CONTRACT_REPAIRS = 5
MAX_ASSERTION_NO_PROGRESS_RECOVERIES = 1
#: Per-assertion precheck repairs before that item is isolated.  Issue #167 §8.3
#: specifies a *per-item* budget; before this it was only ever a whole-script
#: scalar, which is why one bad assertion could hold 54 good ones hostage.
MAX_ASSERTION_PRECHECK_REPAIRS = 5
#: How many times the same semantic failure identity may recur before the item
#: counts as making no progress, regardless of how the expression text churns.
NO_PROGRESS_SEMANTIC_REPEATS = 3
#: Hard backstop on the precheck<->convert loop.  With the per-item budget this
#: is unreachable in practice; it exists so the edge is bounded by construction.
MAX_PRECHECK_ROUNDS = 12
#: Emitted by the evidence layer when a fired-transition derivation is not unique
#: and the candidates disagree on taint.  Attribution must not promote such a
#: result: the unresolved segment may touch compiler-owned elements.
PATH_TAINT_AMBIGUOUS_REF = "simulation:path_taint:ambiguous"
#: Emitted when a bounded model-checking answer rests on the absence of a
#: counterexample rather than on an exhibited defective trace.
FORMAL_EXAMINED_ONLY_REF = "formal:examined_only"


def _classify_reviewed_hash(reviewed: str, expected: str) -> tuple[str, str]:
    """Classify how a reviewer's transcribed script hash relates to the real one.

    A 32-hex-character agreement is 128 bits; it cannot coincidentally belong to
    a different script.  Anything shorter or divergent is reported as a
    mismatch so it lands in the audit record.

    :param reviewed: the hash string the reviewer returned.
    :param expected: the deterministically computed script hash.
    :return: ``("exact"|"prefix"|"mismatch", human-readable note)``.
    """

    normalized = "".join(ch for ch in str(reviewed).lower() if ch in "0123456789abcdef")
    if normalized == expected:
        return "exact", ""
    shared = 0
    for left, right in zip(normalized, expected):
        if left != right:
            break
        shared += 1
    if shared >= 32:
        return (
            "prefix",
            f"reviewer hash agrees on {shared} leading hex characters but was not "
            "transcribed exactly",
        )
    return (
        "mismatch",
        f"reviewer hash agrees on only {shared} leading hex characters",
    )


def _semantic_invalid_key(
    assertion_id: str, error: str | None, coverage_key: str | None
) -> str:
    """Build a churn-resistant identity for one precheck failure.

    Keyed on *what failed and why*, never on the expression text or the error
    message body: a producer that rewrites its query every revision would
    otherwise present a fresh signature each round and never look stuck.

    :param assertion_id: stable assertion id.
    :param error: the raw precheck error payload, if any.
    :param coverage_key: the assertion's coverage key.
    :return: a stable ``id|error_type|coverage_key`` string.
    """

    error_type = "unknown"
    if error:
        match = re.search(r"['\"]type['\"]\s*:\s*['\"]([A-Za-z_][\w.]*)['\"]", error)
        if match:
            error_type = match.group(1)
        else:
            head = str(error).strip().split(":", 1)[0]
            error_type = head[:64] or "unknown"
    return f"{assertion_id}|{error_type}|{coverage_key or ''}"

ALLOWED_PRIMARY_EVIDENCE_FAMILIES = {
    "structure": {"structure", "relation", "effect", "topology", "provenance"},
    "behavior": {"simulation", "relation", "effect"},
    "property": {"fbmcq", "structure", "relation", "effect"},
}

MANDATORY_PRIMARY_EVIDENCE_FAMILIES = {
    "structure": set(),
    "behavior": {"simulation"},
    "property": {"fbmcq"},
}


class StructuredResponder(Protocol):
    def invoke_structured(
        self, *, role: str, schema: type[T], system_prompt: str, user_input: str
    ) -> T: ...


class CallableStructuredResponder:
    def __init__(
        self, func: Callable[[str, type[BaseModel], str, str], BaseModel]
    ) -> None:
        self._func = func

    def invoke_structured(
        self, *, role: str, schema: type[T], system_prompt: str, user_input: str
    ) -> T:
        return cast(T, self._func(role, schema, system_prompt, user_input))


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _append_records(
    state: DiscoverGraphState, *records: NodeExecutionRecord
) -> list[NodeExecutionRecord]:
    return [*state.get("node_execution_records", []), *records]


def _append_feedback(
    state: DiscoverGraphState,
    feedback: RevisionFeedback,
) -> tuple[RevisionFeedback, ...]:
    """Keep every revision request available to later nodes and renderers."""

    return (*state.get("_assertion_feedback_history", ()), feedback)


def _revision_delta(
    previous: RequirementSet | AssertionScript | None,
    current: RequirementSet | AssertionScript,
) -> dict[str, Any]:
    """Return a compact deterministic delta that can reconstruct prior versions."""

    if isinstance(current, RequirementSet):
        current_items = {
            item.requirement_id: item.model_dump(mode="json")
            for item in current.requirements
        }
        previous_items = (
            {
                item.requirement_id: item.model_dump(mode="json")
                for item in previous.requirements
            }
            if isinstance(previous, RequirementSet)
            else {}
        )
        metadata_before = (
            previous.segment_disposition if isinstance(previous, RequirementSet) else {}
        )
        metadata_after = current.segment_disposition
    else:
        current_items = {
            item.assertion_id: item.model_dump(mode="json")
            for item in current.assertions
        }
        previous_items = (
            {
                item.assertion_id: item.model_dump(mode="json")
                for item in previous.assertions
            }
            if isinstance(previous, AssertionScript)
            else {}
        )
        metadata_before = (
            {
                "prefix": previous.prefix,
                "requirement_mapping": previous.requirement_mapping,
            }
            if isinstance(previous, AssertionScript)
            else {}
        )
        metadata_after = {
            "prefix": current.prefix,
            "requirement_mapping": current.requirement_mapping,
        }
    common = set(previous_items) & set(current_items)
    changed = [
        {
            "id": item_id,
            "before": previous_items[item_id],
            "after": current_items[item_id],
        }
        for item_id in sorted(common)
        if previous_items[item_id] != current_items[item_id]
    ]
    delta: dict[str, Any] = {
        "from_revision": previous.revision if previous is not None else None,
        "to_revision": current.revision,
        "added": [
            current_items[item_id]
            for item_id in sorted(set(current_items) - set(previous_items))
        ],
        "removed": sorted(set(previous_items) - set(current_items)),
        "changed": changed,
    }
    if metadata_before != metadata_after:
        delta["metadata_before"] = metadata_before
        delta["metadata_after"] = metadata_after
    return delta


def _append_revision_event(
    state: DiscoverGraphState,
    *,
    field: str,
    loop: str,
    event: str,
    revision: int,
    artifact_hash: str | None,
    status: str,
    artifact_delta: dict[str, Any] | None = None,
    rationale: str | None = None,
    findings: tuple[str, ...] = (),
    item_ids: tuple[str, ...] = (),
    budget_counters: dict[str, int] | None = None,
) -> tuple[RevisionLedgerEvent, ...]:
    history = tuple(state.get(cast(Any, field), ()))
    entry = RevisionLedgerEvent(
        sequence=len(history) + 1,
        loop=cast(Any, loop),
        event=cast(Any, event),
        revision=revision,
        artifact_hash=artifact_hash,
        status=status,
        artifact_delta=artifact_delta or {},
        rationale=rationale,
        findings=findings,
        item_ids=item_ids,
        budget_counters=budget_counters or {},
    )
    return (*history, entry)


def _append_coverage_gaps(
    state: DiscoverGraphState, *gaps: CoverageGap
) -> tuple[CoverageGap, ...]:
    existing = {gap.gap_id: gap for gap in state.get("coverage_gaps", ())}
    for gap in gaps:
        existing[gap.gap_id] = gap
    return tuple(existing[key] for key in sorted(existing))


def _quarantine_reviewed_assertions(
    state: DiscoverGraphState,
    *,
    script: AssertionScript,
    quarantined_ids: tuple[str, ...],
    rationale: str,
    findings: tuple[str, ...],
    sealed_store: InMemorySealedStore,
) -> dict[str, Any]:
    """Isolate review-unresolved assertions and re-seal the surviving script.

    Issue #167 §3 forbids escalating one unresolved local review finding into
    ``RUN_FAILED``.  This drops only the targeted assertions, re-seals the rest
    so ``release_results`` still sees matching script/public/receipt hashes, and
    writes one :class:`CoverageGap` per isolated item.

    :param quarantined_ids: assertion ids the reviewer never accepted.
    :param sealed_store: store holding the already-executed truth payload.
    :return: a state update dict ready to merge into the node's update.
    """

    frozen = state["frozen_inputs"]
    public = state["assertion_check_public"]
    receipt = state["sealed_assertion_results"]
    quarantined = set(quarantined_ids)
    retained = {
        item.assertion_id
        for item in script.assertions
        if item.assertion_id not in quarantined
    }

    filtered_script = _filter_assertion_script(script, retained)
    filtered_script_hash = sha256_data(filtered_script)
    filtered_public = AssertionCheckPublic(
        script_hash=filtered_script_hash,
        tool_env_hash=frozen.tool_env_hash,
        status="executable",
        executions=tuple(
            item for item in public.executions if item.assertion_id in retained
        ),
    )
    payload = tuple(sealed_store.release(receipt.sealed_hash))
    filtered_results = tuple(
        result.model_copy(update={"script_hash": filtered_script_hash})
        for result in payload
        if result.assertion_id in retained
    )
    filtered_sealed_hash = sha256_data(filtered_results)
    filtered_receipt = SealedAssertionReceipt(
        script_hash=filtered_script_hash,
        tool_env_hash=frozen.tool_env_hash,
        sealed_hash=filtered_sealed_hash,
        result_count=len(filtered_results),
        sealed_payload_ref=sealed_store.put(filtered_sealed_hash, filtered_results),
    )

    spec_by_id = {item.assertion_id: item for item in script.assertions}
    requirement_by_id = {
        item.requirement_id: item for item in state["requirement_set"].requirements
    }
    gaps = tuple(
        CoverageGap(
            gap_id=f"GAP-{assertion_id}-REVIEW",
            stage="assertion_review",
            requirement_id=spec_by_id[assertion_id].requirement_id,
            assertion_ids=(assertion_id,),
            source_segment_ids=requirement_by_id[
                spec_by_id[assertion_id].requirement_id
            ].source_segment_ids,
            reason_code="review_unresolved",
            reason=(
                "The Assertion Reviewer still requested revision after "
                f"{MAX_ASSERTION_REVIEW_REPAIRS} item repairs."
            ),
            last_revision=script.revision,
            last_feedback=rationale,
            history_refs=tuple(
                f"assertion-ledger:{event.sequence}"
                for event in state.get("_assertion_revision_ledger", ())
            ),
            coverage_impact=(
                f"Coverage key {spec_by_id[assertion_id].coverage_key} was not released."
            ),
            blocks_full_coverage=(
                (spec_by_id[assertion_id].role or "primary") == "primary"
            ),
        )
        for assertion_id in quarantined_ids
    )
    ledger = tuple(state.get("_assertion_revision_ledger", ()))
    quarantine_event = RevisionLedgerEvent(
        sequence=len(ledger) + 1,
        loop="assertions",
        event="artifact_quarantined",
        revision=script.revision,
        artifact_hash=sha256_data(script),
        status="quarantined",
        rationale=(
            "Review-unresolved assertions were isolated; accepted assertions "
            "continue to release."
        ),
        findings=findings or tuple(gap.reason for gap in gaps),
        item_ids=quarantined_ids,
        budget_counters={"review_repairs": MAX_ASSERTION_REVIEW_REPAIRS},
    )
    return {
        "assertion_script": filtered_script,
        "assertion_check_public": filtered_public,
        "sealed_assertion_results": filtered_receipt,
        "coverage_gaps": _append_coverage_gaps(state, *gaps),
        "_quarantined_assertion_ids": tuple(
            sorted({*state.get("_quarantined_assertion_ids", ()), *quarantined_ids})
        ),
        "_assertion_revision_ledger": (*ledger, quarantine_event),
        "_last_executable_assertion_script": filtered_script,
    }


def _filter_assertion_script(
    script: AssertionScript, accepted_ids: set[str]
) -> AssertionScript:
    assertions = tuple(
        item for item in script.assertions if item.assertion_id in accepted_ids
    )
    if not assertions:
        raise ValueError("soft isolation cannot publish an empty AssertionScript")
    mapping = {
        requirement_id: tuple(
            assertion_id
            for assertion_id in assertion_ids
            if assertion_id in accepted_ids
        )
        for requirement_id, assertion_ids in script.requirement_mapping.items()
    }
    mapping = {
        requirement_id: assertion_ids
        for requirement_id, assertion_ids in mapping.items()
        if assertion_ids
    }
    return script.model_copy(
        update={"assertions": assertions, "requirement_mapping": mapping}
    )


def _requirement_primary_truth(
    requirement: Any,
    values: list[bool],
) -> bool:
    if not values:
        return False
    aggregation = requirement.coverage_obligation.aggregation
    if aggregation == "all":
        return all(values)
    if aggregation == "any":
        return any(values)
    if aggregation == "exactly_one":
        return sum(values) == 1
    # Custom policies are frozen by id but not executable in this first v2
    # slice; fail closed instead of silently treating them as all/any.
    return False


def _record_node(
    state: DiscoverGraphState,
    *,
    node_name: str,
    revision: int,
    kind: str,
    input_value: Any,
    output_value: Any | None,
    started_at: datetime,
    start_ns: int,
    failure: str | None = None,
    details: dict[str, Any] | None = None,
) -> NodeExecutionRecord:
    finished_at = _now()
    run_id = _run_id(state)
    node_call_id = f"{run_id}:{node_name}:r{revision}:{len(state.get('node_execution_records', [])) + 1}"
    return NodeExecutionRecord(
        run_id=run_id,
        node_call_id=node_call_id,
        node_name=node_name,
        revision=revision,
        kind=cast(Any, kind),
        status="failed" if failure else "completed",
        input_hash=sha256_data(input_value),
        output_hash=None if output_value is None else sha256_data(output_value),
        started_at=started_at,
        finished_at=finished_at,
        elapsed_ms=(time.perf_counter_ns() - start_ns) / 1_000_000,
        failure=failure,
        details=details or {},
    )


def _run_id(state: DiscoverGraphState) -> str:
    if "run_identity" in state:
        return state["run_identity"].run_id
    if "_input" in state:
        return state["_input"].run_id
    if "frozen_inputs" in state:
        return state["frozen_inputs"].run_id
    return "unknown-run"


def _llm_call_record(
    state: DiscoverGraphState,
    *,
    responder: StructuredResponder,
    node_record: NodeExecutionRecord,
    role: str,
    revision: int,
    system_prompt: str,
    user_prompt: str,
    output: BaseModel,
) -> LLMCallRecord:
    observation = None
    take = getattr(responder, "take_last_observation", None)
    if callable(take):
        observation = take()
    if observation is None:
        return LLMCallRecord(
            run_id=_run_id(state),
            llm_call_id=f"{node_record.node_call_id}:llm",
            node_call_id=node_record.node_call_id,
            role=role,
            revision=revision,
            profile=state["frozen_inputs"].profile,
            started_at=node_record.started_at,
            finished_at=node_record.finished_at,
            elapsed_ms=node_record.elapsed_ms,
            status="completed",
            input_hash=node_record.input_hash,
            output_hash=node_record.output_hash,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            system_prompt_sha256=sha256_text(system_prompt),
            user_prompt_sha256=sha256_text(user_prompt),
            parsed_output=output.model_dump(mode="json"),
            parsed_output_sha256=sha256_data(output),
            system_prompt_chars=len(system_prompt),
            user_prompt_chars=len(user_prompt),
            output_chars=len(output.model_dump_json()),
        )
    usage = observation.usage
    core_usage = [
        usage.get("input_tokens"),
        usage.get("output_tokens"),
        usage.get("total_tokens"),
    ]
    usage_status = (
        "complete"
        if all(value is not None for value in core_usage)
        else "partial"
        if any(value is not None for value in core_usage)
        else "unavailable"
    )
    return LLMCallRecord(
        run_id=_run_id(state),
        llm_call_id=observation.llm_call_id,
        node_call_id=node_record.node_call_id,
        role=role,
        revision=revision,
        profile=observation.profile,
        adapter=observation.adapter,
        provider=observation.provider,
        configured_model=observation.configured_model,
        observed_model=observation.observed_model,
        model_id=observation.observed_model or observation.configured_model,
        started_at=observation.started_at,
        finished_at=observation.finished_at,
        elapsed_ms=observation.elapsed_ms,
        status=cast(Any, observation.status),
        input_hash=node_record.input_hash,
        output_hash=node_record.output_hash,
        system_prompt=observation.system_prompt,
        user_prompt=observation.user_prompt,
        system_prompt_sha256=sha256_text(observation.system_prompt),
        user_prompt_sha256=sha256_text(observation.user_prompt),
        parsed_output=observation.parsed_output,
        raw_response=observation.raw_response,
        parsed_output_sha256=(
            sha256_data(observation.parsed_output)
            if observation.parsed_output is not None
            else None
        ),
        raw_response_sha256=(
            sha256_data(observation.raw_response)
            if observation.raw_response is not None
            else None
        ),
        system_prompt_chars=len(observation.system_prompt),
        user_prompt_chars=len(observation.user_prompt),
        output_chars=(
            len(output.model_dump_json())
            if observation.parsed_output is not None
            else None
        ),
        input_tokens=usage.get("input_tokens"),
        output_tokens=usage.get("output_tokens"),
        total_tokens=usage.get("total_tokens"),
        cache_read_input_tokens=usage.get("cache_read_input_tokens"),
        cache_creation_input_tokens=usage.get("cache_creation_input_tokens"),
        ephemeral_5m_input_tokens=usage.get("ephemeral_5m_input_tokens"),
        ephemeral_1h_input_tokens=usage.get("ephemeral_1h_input_tokens"),
        reasoning_tokens=usage.get("reasoning_tokens"),
        usage_status=cast(Any, usage_status),
        usage_sources=tuple(usage.get("usage_sources", ())),
        transport_attempts=observation.attempts,
        failure=observation.failure,
    )


def _fail_state(
    state: DiscoverGraphState,
    node_name: str,
    exc: Exception,
    *,
    started_at: datetime | None = None,
    start_ns: int | None = None,
    input_value: Any | None = None,
    revision: int = 0,
    kind: str = "deterministic",
    responder: StructuredResponder | None = None,
    role: str | None = None,
) -> DiscoverGraphState:
    message = f"{type(exc).__name__}: {exc}"
    update: DiscoverGraphState = {
        "failure": RunFailure(
            run_id=_run_id(state), node_name=node_name, message=message
        )
    }
    if started_at is not None and start_ns is not None:
        record = _record_node(
            state,
            node_name=node_name,
            revision=revision,
            kind=kind,
            input_value=input_value,
            output_value=None,
            started_at=started_at,
            start_ns=start_ns,
            failure=message,
        )
        update["node_execution_records"] = _append_records(state, record)
        if responder is not None and role is not None:
            take = getattr(responder, "take_last_observation", None)
            observation = take() if callable(take) else None
            if observation is not None:
                usage = observation.usage
                core = [
                    usage.get("input_tokens"),
                    usage.get("output_tokens"),
                    usage.get("total_tokens"),
                ]
                usage_status = (
                    "complete"
                    if all(value is not None for value in core)
                    else "partial"
                    if any(value is not None for value in core)
                    else "unavailable"
                )
                llm_record = LLMCallRecord(
                    run_id=_run_id(state),
                    llm_call_id=observation.llm_call_id,
                    node_call_id=record.node_call_id,
                    role=role,
                    revision=revision,
                    profile=observation.profile,
                    adapter=observation.adapter,
                    provider=observation.provider,
                    configured_model=observation.configured_model,
                    observed_model=observation.observed_model,
                    model_id=observation.observed_model or observation.configured_model,
                    started_at=observation.started_at,
                    finished_at=observation.finished_at,
                    elapsed_ms=observation.elapsed_ms,
                    status="failed",
                    input_hash=record.input_hash,
                    output_hash=None,
                    system_prompt=observation.system_prompt,
                    user_prompt=observation.user_prompt,
                    system_prompt_sha256=sha256_text(observation.system_prompt),
                    user_prompt_sha256=sha256_text(observation.user_prompt),
                    parsed_output=None,
                    raw_response=observation.raw_response,
                    raw_response_sha256=(
                        sha256_data(observation.raw_response)
                        if observation.raw_response is not None
                        else None
                    ),
                    system_prompt_chars=len(observation.system_prompt),
                    user_prompt_chars=len(observation.user_prompt),
                    input_tokens=usage.get("input_tokens"),
                    output_tokens=usage.get("output_tokens"),
                    total_tokens=usage.get("total_tokens"),
                    cache_read_input_tokens=usage.get("cache_read_input_tokens"),
                    cache_creation_input_tokens=usage.get(
                        "cache_creation_input_tokens"
                    ),
                    ephemeral_5m_input_tokens=usage.get("ephemeral_5m_input_tokens"),
                    ephemeral_1h_input_tokens=usage.get("ephemeral_1h_input_tokens"),
                    reasoning_tokens=usage.get("reasoning_tokens"),
                    usage_status=cast(Any, usage_status),
                    usage_sources=tuple(usage.get("usage_sources", ())),
                    transport_attempts=observation.attempts,
                    failure=observation.failure or message,
                )
                update["llm_call_records"] = [
                    *state.get("llm_call_records", []),
                    llm_record,
                ]
    return update


def _validate_revision_pair(
    current: BaseModel | None, feedback: RevisionFeedback | None
) -> None:
    if (current is None) != (feedback is None):
        raise ValueError(
            "current_result and revision_feedback must be provided as a pair"
        )


def _canonicalize_trace_entry_ids(
    context: dict[str, Any], known_trace_ids: set[str]
) -> dict[str, Any]:
    """Canonicalize a uniquely resolvable leaf-only trace reference.

    LLMs sometimes copy ``trace:state:Child`` from a full source id such as
    ``trace:state:Mode.Child``.  This is safe to normalize only
    when the kind prefix and final path component identify exactly one frozen
    trace entry; ambiguous or unknown references remain hard errors.
    """

    raw_ids = context.get("trace_entry_ids", [])
    if not isinstance(raw_ids, (list, tuple)):
        raise ValueError("source_context.trace_entry_ids must be a list")
    canonical_ids: list[str] = []
    unknown: list[str] = []
    for raw_id in raw_ids:
        reference = str(raw_id)
        if reference in known_trace_ids:
            canonical_ids.append(reference)
            continue
        prefix, separator, leaf = reference.rpartition(":")
        if not separator:
            unknown.append(reference)
            continue
        leaf_name = leaf.rsplit(".", 1)[-1]
        candidates = sorted(
            trace_id
            for trace_id in known_trace_ids
            if trace_id.rpartition(":")[0] == prefix
            and trace_id.rpartition(":")[2].rsplit(".", 1)[-1] == leaf_name
        )
        if len(candidates) != 1:
            unknown.append(reference)
            continue
        canonical_ids.append(candidates[0])
    if unknown:
        raise ValueError(
            "source_context.trace_entry_ids contains unknown or ambiguous references: "
            f"{sorted(unknown)}"
        )
    if canonical_ids == list(raw_ids):
        return context
    return {**context, "trace_entry_ids": canonical_ids}


def prepare(state: DiscoverGraphState) -> DiscoverGraphState:
    started_at, start_ns = _now(), time.perf_counter_ns()
    discover_input = state["_input"]
    try:
        frozen = _fallback_prepare(discover_input)
        identity = DiscoverRunIdentity(
            run_id=discover_input.run_id,
            profile=discover_input.profile,
            language=discover_input.language,
            created_at=started_at,
        )
        record = _record_node(
            state,
            node_name="prepare",
            revision=0,
            kind="deterministic",
            input_value=discover_input,
            output_value=frozen,
            started_at=started_at,
            start_ns=start_ns,
        )
        return {
            "run_identity": identity,
            "frozen_inputs": frozen,
            "node_execution_records": _append_records(state, record),
        }
    except (
        Exception
    ) as exc:  # pragma: no cover - failure path covered by contract tests if needed
        return _fail_state(
            state,
            "prepare",
            exc,
            started_at=started_at,
            start_ns=start_ns,
            input_value=discover_input,
        )


#: Source-trace prefix marking a variable the converter created, not the author.
_ROUTE_CONTROL_PREFIX = "compiler:route_control:"



#: `R45RouteToken = 7;` in an effect, `R45RouteToken == 9` in a guard.  Matched by
#: shape rather than by the token's name, which is the converter's to choose.
_TOKEN_SET = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(-?\d+)")
_TOKEN_TEST = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*==\s*(-?\d+)")


_COMPILER_STATE_PREFIX = "compiler:state:"


def _pseudo_state_facts(
    inspected: dict[str, Any], exclusions: tuple[str, ...] | list[str] = ()
) -> dict[str, tuple[dict[str, Any], ...]]:
    """Return what the model expresses through `[*]` instead of through a name.

    `model_vocabulary` lists states, events and variables -- everything that has a
    name.  Entry and termination do not: they are written `[*]`.  A producer given
    only the named vocabulary therefore sees nothing that could carry "when power
    off it reaches the final state", concludes the model lacks it, and proposes a
    `FinalState` that no correctly-terminating model would declare.  Pair 0050 did
    that twice on a model whose `HumanDrivingMode -> [*] : /Power_Off` is exactly
    how termination is written.

    `ends_run` is the distinction that matters and it is not readable off the edge:
    `-> [*]` leaves whatever scope owns the source, so it ends the run only when
    that scope is the root.  Pair 0029's `enter_urban -> [*]` exits UrbanMode and
    routes onward to a declared state, which is why a completion claim there is a
    reachability question and not a termination one.

    Inside a composite it takes two edges, and *which* two is decided by the route
    token, not by ancestry.  Pair 0050 exits `SubState1` on two different events:

        SubState1 -> [*] : /Power_Off        effect { R45RouteToken = 9; }
        SubState1 -> [*] : /human_steering.. effect { R45RouteToken = 7; }
        AutonomousMode -> [*]              if [R45RouteToken == 9]   <- ends the run
        AutonomousMode -> HumanDrivingMode if [R45RouteToken == 7]   <- mode switch

    Both inner edges leave the same composite and both sit under a state that ends
    the run on *some* token, so an ancestry test calls both terminations.  It is
    wrong about the second, and being wrong there is expensive: the step-1 gate
    then tells the producer to write `terminates` for a mode switch, which is
    False, which publishes a defect the model does not have.  So the token an inner
    edge sets is matched against the guard of the outer edge, and `via_token`
    records the link for the record.
    """

    inspect = inspected.get("inspect") or {}
    rows = [r for r in (inspect.get("states") or []) if isinstance(r, dict)]
    parent_of = {
        str(r.get("path")): str(r.get("parent_path") or "")
        for r in rows
        if r.get("path")
    }
    root = str(inspect.get("root_state_path") or "")
    transitions = [t for t in (inspect.get("transitions") or []) if isinstance(t, dict)]

    def _tokens(text: Any, pattern: re.Pattern[str]) -> set[tuple[str, str]]:
        return {(m.group(1), m.group(2)) for m in pattern.finditer(str(text or ""))}

    # Tokens whose guarded outer edge ends the run, and the scope that edge leaves:
    # `AutonomousMode -> [*] if [tok == 9]` publishes `("tok","9") -> AutonomousMode`.
    ends_on_token: dict[tuple[str, str], set[str]] = {}
    for row in transitions:
        if str(row.get("to_path") or "") != PSEUDO_INITIAL:
            continue
        source = str(row.get("from_path") or "")
        if parent_of.get(source, "") != root:
            continue
        for token in _tokens(row.get("guard"), _TOKEN_TEST):
            ends_on_token.setdefault(token, set()).add(source)
    run_ending_tokens = set(ends_on_token)

    terminating: list[dict[str, Any]] = []
    # The composite an inner exit ultimately terminates, keyed by the event that
    # started the chain.  A requirement says "while in autonomous mode, power off
    # ends the run" and names the *mode*, not the substate it happened to be in, so
    # the chain has to be reported at that level too or a mode-level claim matches
    # nothing.
    chain_rows: dict[tuple[str, str | None], str] = {}
    for row in transitions:
        if str(row.get("to_path") or "") != PSEUDO_INITIAL:
            continue
        source = str(row.get("from_path") or "")
        if not source:
            continue
        scope = parent_of.get(source, "")
        direct = bool(scope) and scope == root
        matched = _tokens(row.get("effect"), _TOKEN_SET) & run_ending_tokens
        via = sorted(f"{name}=={value}" for name, value in matched)
        trigger = str(row.get("event") or "") or None
        for token in matched:
            for composite in ends_on_token[token]:
                if composite != source:
                    chain_rows[(composite, trigger)] = f"{token[0]}=={token[1]}"
        terminating.append(
            {
                "source": source,
                "trigger": trigger,
                "guard": str(row.get("guard") or "") or None,
                "exits_scope": scope,
                "ends_run": direct or bool(via),
                "via_token": via[0] if via else None,
            }
        )
    seen = {(r["source"], r["trigger"]) for r in terminating if r["ends_run"]}
    for (composite, trigger), token in sorted(
        chain_rows.items(), key=lambda kv: (kv[0][0], kv[0][1] or "")
    ):
        if (composite, trigger) in seen:
            continue
        terminating.append(
            {
                "source": composite,
                "trigger": trigger,
                "guard": None,
                "exits_scope": parent_of.get(composite, ""),
                "ends_run": True,
                "via_token": token,
            }
        )
    # States the converter inserted, from the frozen exclusion table.  An
    # unconditional entry onto one of these is not where the author said the
    # composite starts -- it is the converter's default, generated *because* no
    # author entry was unconditional.  Pair 0029 declares
    # `[*] -> enter_hwy if [R45RouteToken == 5]` alongside
    # `[*] -> UnspecifiedInitial` with no guard, and `initial_target` answers True
    # for the synthetic one and False for `enter_hwy` -- which is the credited
    # defect.  A producer told only "entry takes the unconditional edge" binds the
    # synthetic target and the defect disappears.  37 of the corpus's 157
    # unconditional entries, across 20 pairs, land on such a state.
    compiler_states = {
        str(item)[len(_COMPILER_STATE_PREFIX) :]
        for item in exclusions
        if str(item).startswith(_COMPILER_STATE_PREFIX)
    }
    entries: list[dict[str, Any]] = []
    for row in rows:
        composite = str(row.get("path") or "")
        for target in row.get("initial_targets") or []:
            if not isinstance(target, dict) or not target.get("target"):
                continue
            # The inspect table qualifies `target` and leaves `event` bare, and the
            # payload this lands in says every value must be used verbatim.  Copied
            # as-is, `Power_On` is refused by `event_declared` ("a bare name with no
            # dot is refused") and trips the step-2 gate, because the leaf matches
            # the qualified path the vocabulary does declare.  29 entries across the
            # corpus are bare, including both of pair 0000's root entries.
            trigger = str(target.get("event") or "") or None
            if trigger and "." not in trigger and root:
                trigger = f"{root}.{trigger}"
            path = str(target.get("target"))
            entries.append(
                {
                    "composite": composite,
                    "target": path,
                    "unconditional": bool(target.get("is_unconditional")),
                    "converter_generated": path in compiler_states,
                    "guard": str(target.get("guard") or "") or None,
                    "trigger": trigger,
                }
            )
    return {
        "terminating_transitions": tuple(terminating),
        "initial_entries": tuple(entries),
    }


def _model_vocabulary(
    inspected: dict[str, Any], exclusions: tuple[str, ...] | list[str] = ()
) -> dict[str, tuple[str, ...]]:
    """Return the declared state and event paths, under their real field names.

    States carry ``path``; events carry ``qualified_name``.  Reading ``path`` for
    both silently dropped every event, which made ``unresolved_model_references``
    unable to catch a fabricated event reference -- the pair-0029 ``event="/pick"``
    defect class.  One builder, so producers and gates see the same vocabulary.

    Route-control variables are listed apart from the author's own.  They are the
    converter's bookkeeping, the effect facade already drops them from every
    answer, and the prompts forbid using one as a stand-in for a quantity the NL
    names.  Listing them as ordinary variables contradicted all three: on pairs
    0000 and 0006 the *only* entry under ``variables`` was a route token, so a
    producer reading the vocabulary saw a variable available where the model has
    none.  Pair 0006's expected defect is exactly that absence, and a producer
    can only propose a name for it if the vocabulary says plainly that the model
    declares nothing of its own.
    """

    def _paths(group: str, field: str) -> tuple[str, ...]:
        return tuple(
            sorted(
                {
                    str(item[field])
                    for item in (inspected.get(group) or [])
                    if isinstance(item, dict) and item.get(field)
                }
            )
        )

    route_control = {
        item.removeprefix(_ROUTE_CONTROL_PREFIX)
        for item in exclusions
        if isinstance(item, str) and item.startswith(_ROUTE_CONTROL_PREFIX)
    }
    variables = _paths("variables", "name")
    # Three groups, three different field names.  Assuming one of them for all
    # three is what silently emptied this list; keep them explicit.
    return {
        "states": _paths("states", "path"),
        "events": _paths("events", "qualified_name"),
        "variables": tuple(v for v in variables if v not in route_control),
        "compiler_owned_variables_not_usable_as_evidence": tuple(
            v for v in variables if v in route_control
        ),
    }


def _fallback_prepare(discover_input: DiscoverInput) -> FrozenDiscoverInputs:
    inspected = check_fcstm(discover_input.stm_text, "<discover-input>")
    if not inspected.get("executable"):
        raise ValueError(
            f"FCSTM input is not executable: {inspected.get('error') or inspected.get('diagnostics')}"
        )
    source_entries = discover_input.source_trace.get("entries", [])
    source_entries = source_entries if isinstance(source_entries, list) else []
    source_exclusions = discover_input.source_trace.get("attribution_exclusions", [])
    source_exclusions = source_exclusions if isinstance(source_exclusions, list) else []
    environment = build_eval_environment(
        model_text=discover_input.stm_text,
        inspect=inspected.get("inspect"),
        source_mappings=source_entries,
        source_exclusions=source_exclusions,
    )
    # Boundaries come from `common/nl_segmentation`, which prefers a hand annotation when
    # the specification's own numbering is not machine-decidable and otherwise reproduces the
    # newline split verbatim. One corpus specification needs the former: it puts every
    # requirement on a single line, so splitting on newlines collapsed it to one segment and
    # `segment_disposition` could only carry one coarse verdict for the whole spec.
    resolved = resolve_nl_segments(discover_input.natural_language)
    segments = resolved.segments
    return FrozenDiscoverInputs(
        run_id=discover_input.run_id,
        natural_language=discover_input.natural_language,
        stm_text=discover_input.stm_text,
        nl_segments=segments,
        nl_segmentation_source=resolved.source,
        inspect_digest={
            "parse_status": inspected.get("parse_status"),
            "semantic_status": inspected.get("semantic_status"),
            "inspect_status": inspected.get("inspect_status"),
            "diagnostics": inspected.get("diagnostics", []),
            "metrics": inspected.get("metrics", {}),
            "model_type": inspected.get("model_type"),
        },
        # The gate that catches fabricated paths keeps the route-control names:
        # they *are* declared, so rejecting a reference to one would report a
        # non-existent element, which is not what that gate is for.  Whether a
        # producer may *use* one is a separate question, answered by the prompts
        # and the split in `model_vocabulary`.
        known_model_paths=tuple(
            sorted(
                {
                    path
                    for paths in _model_vocabulary(
                        inspected.get("inspect") or {}, source_exclusions
                    ).values()
                    for path in paths
                }
            )
        ),
        model_vocabulary=_model_vocabulary(
            inspected.get("inspect") or {}, source_exclusions
        ),
        pseudo_state_facts=_pseudo_state_facts(inspected, source_exclusions),
        source_trace=discover_input.source_trace,
        working_contract=discover_input.manifest.get("working_contract", {})
        if isinstance(discover_input.manifest.get("working_contract"), dict)
        else {},
        fbmcq_canary=discover_input.manifest.get("fbmcq_canary", {})
        if isinstance(discover_input.manifest.get("fbmcq_canary"), dict)
        else {},
        resource_options=discover_input.manifest.get("resource_options", {})
        if isinstance(discover_input.manifest.get("resource_options"), dict)
        else {},
        input_hashes={
            "natural_language": sha256_text(discover_input.natural_language),
            "stm_text": sha256_text(discover_input.stm_text),
            "manifest": sha256_data(discover_input.manifest),
            "source_trace": sha256_data(discover_input.source_trace),
        },
        tool_env_hash=str(
            discover_input.manifest.get("tool_env_hash")
            or sha256_data(
                {
                    "vars_hash": environment.vars_hash,
                    "function_registry_hash": environment.function_registry_hash,
                }
            )
        ),
        profile=discover_input.profile,
        language=discover_input.language,
    )


def split_requirements(
    state: DiscoverGraphState, responder: StructuredResponder
) -> DiscoverGraphState:
    started_at, start_ns = _now(), time.perf_counter_ns()
    current = state.get("requirement_set")
    feedback = state.get("_requirement_feedback")
    try:
        _validate_revision_pair(current, feedback)
        frozen = state["frozen_inputs"]
        payload = renderer.render_requirement_split_input(
            frozen,
            current,
            feedback,
            tuple(state.get("_requirement_revision_ledger", ())),
        )
        output = responder.invoke_structured(
            role="requirement_splitter",
            schema=RequirementSet,
            system_prompt=prompts.REQUIREMENT_SPLITTER_PROMPT,
            user_input=payload,
        )
        if current is None and output.revision != 1:
            raise ValueError("create RequirementSet must use revision 1")
        if current is not None:
            if output.revision <= current.revision:
                raise ValueError("revised RequirementSet revision must increase")
        for requirement in output.requirements:
            if requirement.checkability is not None:
                raise ValueError(
                    f"requirement {requirement.requirement_id} uses legacy "
                    "checkability; emit verification_kind and coverage_obligation"
                )
            if "coverage_obligation" not in requirement.model_fields_set:
                raise ValueError(
                    f"requirement {requirement.requirement_id} must explicitly emit "
                    "coverage_obligation in the v2 producer path"
                )
        known_trace_ids = {
            str(entry.get("trace_id"))
            for entry in frozen.source_trace.get("entries", [])
            if isinstance(entry, dict) and entry.get("trace_id")
        }
        normalized_requirements = tuple(
            requirement.model_copy(
                update={
                    "source_context": _canonicalize_trace_entry_ids(
                        requirement.source_context, known_trace_ids
                    )
                }
            )
            for requirement in output.requirements
        )
        if normalized_requirements != output.requirements:
            output = output.model_copy(update={"requirements": normalized_requirements})
        fingerprint = sha256_data(output.model_dump(mode="json", exclude={"revision"}))
        if fingerprint in state.get("requirement_fingerprints", ()):
            raise ValueError(
                "no-progress gate rejected repeated RequirementSet semantics"
            )
        if set(output.segment_disposition) != set(frozen.nl_segments):
            raise ValueError(
                "segment_disposition keys must exactly match the frozen NL segment ids"
            )
        for requirement in output.requirements:
            unknown = set(requirement.source_segment_ids) - set(frozen.nl_segments)
            if unknown:
                raise ValueError(
                    f"requirement {requirement.requirement_id} references unknown NL segments: {sorted(unknown)}"
                )
            context = requirement.source_context
            trace_ids = context.get("trace_entry_ids", [])
            if not isinstance(trace_ids, (list, tuple)):
                raise ValueError(
                    f"requirement {requirement.requirement_id} source_context.trace_entry_ids must be a list"
                )
            unknown_trace_ids = set(str(item) for item in trace_ids) - known_trace_ids
            if unknown_trace_ids:
                raise ValueError(
                    f"requirement {requirement.requirement_id} references unknown source trace entries: {sorted(unknown_trace_ids)}"
                )
        # Steps 1 and 2 of the four-step procedure are decided here, not reviewed.
        # Both are settled by comparing the bindings against the frozen model, so
        # asking the Requirement Reviewer for a judgement would be asking it to
        # re-derive something a comparison answers -- and a reviewer that lets one
        # through costs the item its whole repair budget.  Step 3 versus step 4 is
        # the genuinely semantic call and stays with the reviewer.
        known_paths = frozenset(frozen.known_model_paths)
        step_findings = (
            *initialization_anchored_findings(output.requirements),
            *termination_proposal_findings(
                output.requirements,
                known_paths,
                (frozen.pseudo_state_facts or {}).get("terminating_transitions") or (),
            ),
            *redundant_proposal_findings(
                output.requirements, known_paths, dict(frozen.model_vocabulary or {})
            ),
        )
        if step_findings:
            raise ValueError(
                "requirements are anchored or named against what the frozen model "
                f"already says: {list(step_findings)}"
            )
        coverage = RequirementCoverageProjection(
            covered_requirement_ids=tuple(
                req.requirement_id for req in output.requirements
            ),
            accepted_requirement_ids=tuple(
                req.requirement_id for req in output.requirements
            ),
            missing_segment_ids=tuple(
                sorted(set(frozen.nl_segments) - set(output.segment_disposition))
            ),
        )
        record = _record_node(
            state,
            node_name="split_requirements",
            revision=output.revision,
            kind="llm",
            input_value=payload,
            output_value=output,
            started_at=started_at,
            start_ns=start_ns,
        )
        llm_record = _llm_call_record(
            state,
            responder=responder,
            node_record=record,
            role="requirement_splitter",
            revision=output.revision,
            system_prompt=prompts.REQUIREMENT_SPLITTER_PROMPT,
            user_prompt=payload,
            output=output,
        )
        revision_ledger = _append_revision_event(
            state,
            field="_requirement_revision_ledger",
            loop="requirements",
            event="artifact_created",
            revision=output.revision,
            artifact_hash=sha256_data(output),
            status="created",
            artifact_delta=_revision_delta(current, output),
        )
        return {
            "requirement_set": output,
            "requirement_coverage": coverage,
            "_requirement_revision_ledger": revision_ledger,
            "requirement_fingerprints": (
                *state.get("requirement_fingerprints", ()),
                fingerprint,
            ),
            "node_execution_records": _append_records(state, record),
            "llm_call_records": [*state.get("llm_call_records", []), llm_record],
            "_requirement_split_contract_feedback": None,
        }
    except Exception as exc:
        message = f"{type(exc).__name__}: {exc}"
        repair_count = state.get("_requirement_contract_repair_count", 0)
        # The Assertion Converter has had a contract-feedback loop since v2; the
        # Requirement Splitter did not, so one malformed `source_context` or
        # `segment_disposition` ended the entire run.  Issue #167 §3 does not
        # allow a local producer defect to become RUN_FAILED, and three of eight
        # cells in matrix v3-final died exactly this way.  Hand the deterministic
        # contract error straight back and let the producer repair it.
        rejected = locals().get("output")
        can_revise = (
            rejected is not None
            and "no-progress gate" not in message
            and repair_count < MAX_REQUIREMENT_CONTRACT_REPAIRS
        )
        if can_revise:
            contract_feedback = RevisionFeedback(
                target="requirements",
                origin="requirement_review",
                reason=(
                    "The previous Requirement Splitter response violated the "
                    "deterministic RequirementSet contract. Repair exactly the "
                    "reported problem and keep every other requirement unchanged."
                ),
                findings=(message,),
            )
            record = _record_node(
                state,
                node_name="split_requirements",
                revision=(current.revision + 1) if current is not None else 1,
                kind="llm",
                input_value=locals().get("payload", state),
                output_value=None,
                started_at=started_at,
                start_ns=start_ns,
                failure=message,
            )
            return {
                "requirement_set": rejected,
                "_requirement_feedback": contract_feedback,
                "_requirement_split_contract_feedback": contract_feedback,
                "_requirement_contract_repair_count": repair_count + 1,
                "node_execution_records": _append_records(state, record),
            }
        return _fail_state(
            state,
            "split_requirements",
            exc,
            started_at=started_at,
            start_ns=start_ns,
            input_value=locals().get("payload", state),
            revision=current.revision if current is not None else 0,
            kind="llm",
            responder=responder,
            role="requirement_splitter",
        )


def review_requirements(
    state: DiscoverGraphState, responder: StructuredResponder
) -> DiscoverGraphState:
    started_at, start_ns = _now(), time.perf_counter_ns()
    try:
        frozen = state["frozen_inputs"]
        requirements = state["requirement_set"]
        coverage = state["requirement_coverage"]
        payload = renderer.render_requirement_review_input(
            frozen,
            requirements,
            coverage,
            state.get("_requirement_feedback"),
            tuple(state.get("_requirement_revision_ledger", ())),
        )
        output = responder.invoke_structured(
            role="requirement_reviewer",
            schema=RequirementReview,
            system_prompt=prompts.REQUIREMENT_REVIEWER_PROMPT,
            user_input=payload,
        )
        if output.reviewed_revision != requirements.revision:
            raise ValueError(
                "RequirementReview reviewed_revision must match current RequirementSet"
            )
        update: DiscoverGraphState = {"requirement_review": output}
        update["_requirement_revision_ledger"] = _append_revision_event(
            state,
            field="_requirement_revision_ledger",
            loop="requirements",
            event="review_completed",
            revision=requirements.revision,
            artifact_hash=sha256_data(requirements),
            status=output.decision,
            rationale=output.rationale,
            findings=tuple(f.message for f in output.findings),
        )
        review_repair_count = state.get("_requirement_review_repair_count", 0)
        if output.decision == "revise":
            targeted_requirement_ids = tuple(
                sorted(
                    {
                        finding.requirement_id
                        for finding in output.findings
                        if finding.requirement_id is not None
                    }
                )
            )
            update["_requirement_feedback"] = RevisionFeedback(
                target="requirements",
                reason=output.rationale,
                findings=tuple(f.message for f in output.findings),
                target_item_ids=targeted_requirement_ids,
                origin="requirement_review",
            )
            update["_requirement_review_repair_count"] = review_repair_count + 1
        record = _record_node(
            state,
            node_name="review_requirements",
            revision=requirements.revision,
            kind="llm",
            input_value=payload,
            output_value=output,
            started_at=started_at,
            start_ns=start_ns,
        )
        llm_record = _llm_call_record(
            state,
            responder=responder,
            node_record=record,
            role="requirement_reviewer",
            revision=requirements.revision,
            system_prompt=prompts.REQUIREMENT_REVIEWER_PROMPT,
            user_prompt=payload,
            output=output,
        )
        update["node_execution_records"] = _append_records(state, record)
        update["llm_call_records"] = [*state.get("llm_call_records", []), llm_record]
        if (
            output.decision == "revise"
            and review_repair_count >= MAX_REQUIREMENT_REVIEW_REPAIRS
        ):
            targeted = set(targeted_requirement_ids)
            retained = tuple(
                requirement
                for requirement in requirements.requirements
                if requirement.requirement_id not in targeted
            )
            if targeted and retained:
                quarantined = tuple(
                    requirement
                    for requirement in requirements.requirements
                    if requirement.requirement_id in targeted
                )
                update["requirement_set"] = requirements.model_copy(
                    update={"requirements": retained}
                )
                update["requirement_review"] = RequirementReview(
                    decision="accept",
                    reviewed_revision=requirements.revision,
                    rationale=(
                        "Remaining requirements accepted after item-local quarantine "
                        "of review-unresolved requirements."
                    ),
                )
                update["requirement_coverage"] = coverage.model_copy(
                    update={
                        "accepted_requirement_ids": tuple(
                            item.requirement_id for item in retained
                        ),
                        "quarantined_requirement_ids": tuple(sorted(targeted)),
                    }
                )
                gaps = tuple(
                    CoverageGap(
                        gap_id=f"GAP-{item.requirement_id}-REVIEW",
                        stage="requirement_split",
                        requirement_id=item.requirement_id,
                        source_segment_ids=item.source_segment_ids,
                        reason_code="revision_budget_exhausted",
                        reason=(
                            "Requirement Reviewer still requested revision after "
                            f"{MAX_REQUIREMENT_REVIEW_REPAIRS} item repairs."
                        ),
                        last_revision=requirements.revision,
                        last_feedback=output.rationale,
                        history_refs=tuple(
                            f"requirement-ledger:{event.sequence}"
                            for event in state.get("_requirement_revision_ledger", ())
                        ),
                        coverage_impact=(
                            "The source segments for this requirement were not "
                            "converted into accepted assertions."
                        ),
                        blocks_full_coverage=True,
                    )
                    for item in quarantined
                )
                update["coverage_gaps"] = _append_coverage_gaps(state, *gaps)
                update["_requirement_feedback"] = None
            else:
                message = (
                    "bounded review gate could not isolate unresolved Requirement "
                    "items without emptying the accepted RequirementSet"
                )
                update["failure"] = RunFailure(
                    run_id=_run_id(state),
                    node_name="review_requirements",
                    message=message,
                )
        return update
    except Exception as exc:
        return _fail_state(
            state,
            "review_requirements",
            exc,
            started_at=started_at,
            start_ns=start_ns,
            input_value=locals().get("payload", state),
            revision=state.get("requirement_set").revision
            if state.get("requirement_set")
            else 0,
            kind="llm",
            responder=responder,
            role="requirement_reviewer",
        )


def convert_assertions(
    state: DiscoverGraphState, responder: StructuredResponder
) -> DiscoverGraphState:
    started_at, start_ns = _now(), time.perf_counter_ns()
    current = state.get("assertion_script")
    feedback = state.get("_assertion_feedback")
    output: AssertionScript | None = None
    try:
        _validate_revision_pair(current, feedback)
        frozen = state["frozen_inputs"]
        requirements = state["requirement_set"]
        payload = renderer.render_assertion_conversion_input(
            frozen,
            requirements,
            current,
            feedback,
            tuple(state.get("_assertion_revision_ledger", ())),
        )
        output = responder.invoke_structured(
            role="assertion_converter",
            schema=AssertionScript,
            system_prompt=prompts.ASSERTION_CONVERTER_PROMPT,
            user_input=payload,
        )
        if current is None and output.revision != 1:
            raise ValueError("create AssertionScript must use revision 1")
        if current is not None:
            if output.revision <= current.revision:
                raise ValueError("revised AssertionScript revision must increase")
        fingerprint = sha256_data(output.model_dump(mode="json", exclude={"revision"}))
        review_exhausted_by_repeat = False
        if fingerprint in state.get("assertion_fingerprints", ()):
            prior_check = state.get("assertion_check_public")
            feedback_origin = feedback.origin if feedback is not None else None
            if (
                feedback_origin == "assertion_review"
                and feedback is not None
                and feedback.target_item_ids
                and prior_check is not None
                and prior_check.status == "executable"
            ):
                # The producer has nothing further to offer for the items the
                # reviewer flagged.  Issue #167 §3 says that is a local
                # no-progress condition, not a run-level failure: let the script
                # through and mark the review budget spent so review_assertions
                # isolates exactly those items on its next verdict.
                review_exhausted_by_repeat = True
            elif not (
                prior_check is not None
                and prior_check.status == "invalid"
                and feedback_origin == "assertion_precheck"
            ):
                raise ValueError(
                    "no-progress gate rejected repeated AssertionScript semantics"
                )
        req_ids = {r.requirement_id for r in requirements.requirements}
        assertion_ids = {item.assertion_id for item in output.assertions}
        legacy_assertion_ids = tuple(
            sorted(
                item.assertion_id
                for item in output.assertions
                if item.role is None
                or str(item.coverage_key).startswith("legacy:")
                or str(item.aggregation_group).startswith("legacy-group:")
            )
        )
        if legacy_assertion_ids:
            raise ValueError(
                "v2 assertions must explicitly emit role, coverage_key, and "
                f"aggregation_group; legacy-inferred items: {legacy_assertion_ids}"
            )
        mapped_by_assertions: dict[str, set[str]] = {
            req_id: set() for req_id in req_ids
        }
        for assertion in output.assertions:
            if assertion.requirement_id not in req_ids:
                raise ValueError(
                    f"assertion {assertion.assertion_id} maps to unknown requirement"
                )
            expected_prefix = f"[{assertion.requirement_id}][{assertion.assertion_id}]"
            if not assertion.failure_message.startswith(expected_prefix):
                raise ValueError(
                    f"assertion {assertion.assertion_id} failure_message must start with {expected_prefix}"
                )
            misspelled = misspelled_binding_findings(assertion.expression)
            if misspelled:
                raise ValueError(
                    f"assertion {assertion.assertion_id} passes unaccepted "
                    f"keywords: {list(misspelled)}. Checked before the reference "
                    "gates on purpose: a keyword they cannot read hides the value "
                    "bound under it, and they then report the wrong assertion"
                )
            placeholders = placeholder_bindings(assertion.expression)
            if placeholders:
                raise ValueError(
                    f"assertion {assertion.assertion_id} binds {list(placeholders)}. A "
                    "placeholder states a fact about the requirement, not a check: "
                    "nothing can be looked up under it. Give the missing element a "
                    "proposed name, assert its existence as a `precondition`, and "
                    "have this assertion depend on it (issue #170 §11.2)"
                )
            mapped_by_assertions[assertion.requirement_id].add(assertion.assertion_id)
        assertions_by_id = {item.assertion_id: item for item in output.assertions}
        # Dependency-graph gates (issue #170 §11.6).  Script-level rather than
        # per-requirement: a cycle or a dangling reference is a property of the
        # whole graph, and each of these states looks plausible downstream while
        # being wrong -- a cycle leaves every member unrun, which reads as
        # "blocked" with no prerequisite actually false anywhere.
        dangling = missing_dependency_references(output.assertions)
        if dangling:
            raise ValueError(
                f"depends_on names assertions this script does not contain: "
                f"{list(dangling)}. On revision, an assertion that is dropped must "
                "also be removed from every depends_on that referenced it"
            )
        cycles = dependency_cycles(output.assertions)
        if cycles:
            raise ValueError(
                f"depends_on forms cycles: {[list(c) for c in cycles]}. Every member "
                "of a cycle waits on another member, so none can ever run"
            )
        crossing = cross_requirement_dependencies(output.assertions)
        if crossing:
            raise ValueError(
                f"depends_on crosses requirement boundaries: {list(crossing)}. A "
                "requirement's verdict must not hinge on an assertion filed under "
                "another; repeat the prerequisite within each requirement"
            )
        orphans = orphan_preconditions(output.assertions)
        if orphans:
            raise ValueError(
                f"precondition assertions nothing depends on: {list(orphans)}. Add "
                "them to the depends_on of the assertion whose prerequisite they "
                "are, or drop them: unreferenced, the dependent runs anyway, raises "
                "on the element it needs, and enters the repair loop while the "
                "precondition already reports that same defect"
            )
        unresolved = unresolved_reference_findings(
            output.assertions, frozenset(frozen.known_model_paths)
        )
        if unresolved:
            raise ValueError(
                f"assertions reference model elements the frozen STM does not "
                f"declare: {list(unresolved)}. A relation query over a non-existent "
                "element matches nothing and passes, hiding the defect it was meant "
                "to test. If the requirement genuinely needs an element this model "
                "lacks, do not drop it and do not rename it to something that happens "
                "to exist: assert the missing element's existence in a `precondition` "
                "under the same proposed name, and list that precondition in the "
                "depends_on of every assertion that needs it"
            )
        mandatory_waivers: list[dict[str, Any]] = []
        untested_claim_paths: list[dict[str, Any]] = []
        for requirement in requirements.requirements:
            owned_assertions = tuple(
                assertions_by_id[assertion_id]
                for assertion_id in mapped_by_assertions[requirement.requirement_id]
            )
            primary_assertions = tuple(
                assertion
                for assertion in owned_assertions
                if assertion.role == "primary"
            )
            # `<undeclared>` can no longer reach an assertion (gate 7), so the
            # exemptions this block used to carry are gone with it: a requirement
            # naming a term the model lacks is checked through a proposed name and
            # an existence precondition, which is an ordinary primary like any
            # other.  See issue #170 §11.2.
            if not primary_assertions:
                raise ValueError(
                    f"requirement {requirement.requirement_id} requires at least one "
                    "primary assertion. A term the model lacks is no exception: give "
                    "it a proposed name, assert its existence as a `precondition`, "
                    "and let the primary depend on that"
                )
            # Gate D (issue #170 C3): the named predicate fixes which procedure
            # decides it, and a locator answers a weaker question.  Without this
            # check a `transition_exists` probe can close an `occupancy_after`
            # obligation, which is how pair 0006 produced a false positive while
            # every other gate passed.  Requirements with no predicate keep the
            # pre-vocabulary behaviour so v1/v2 artifacts still run.
            if requirement.predicate and primary_assertions:
                called = frozenset[str]().union(
                    *(
                        called_evidence_functions(assertion.expression)
                        for assertion in primary_assertions
                    )
                )
                mismatch = procedure_mismatch(requirement.predicate, called)
                if mismatch is not None:
                    raise ValueError(
                        f"requirement {requirement.requirement_id}: {mismatch[1]}"
                    )
                # Reported, never enforced: a statement legitimately names
                # context paths, so rejecting here would refuse valid work.  The
                # residue is recorded so pair-0029-style half-verification is
                # measurable before deciding whether it needs a gate (#170 C2).
                residue = unmodelled_claim_paths(
                    statement=requirement.statement,
                    bindings=requirement.predicate_bindings,
                    expressions=tuple(
                        assertion.expression for assertion in primary_assertions
                    ),
                    known_paths=frozenset(frozen.known_model_paths),
                )
                if residue:
                    untested_claim_paths.append(
                        {
                            "requirement_id": requirement.requirement_id,
                            "predicate": requirement.predicate,
                            "paths": list(residue),
                        }
                    )
            allowed_primary_families = ALLOWED_PRIMARY_EVIDENCE_FAMILIES[
                requirement.verification_kind
            ]
            invalid_primary_families = sorted(
                {
                    assertion.evidence_family
                    for assertion in primary_assertions
                    if assertion.evidence_family not in allowed_primary_families
                }
            )
            if invalid_primary_families:
                raise ValueError(
                    f"{requirement.verification_kind} requirement "
                    f"{requirement.requirement_id} requires primary evidence from "
                    f"{sorted(allowed_primary_families)}; invalid primary families: "
                    f"{invalid_primary_families}. Weaker evidence must be supporting"
                )
            present_primary_families = {
                assertion.evidence_family for assertion in primary_assertions
            }
            missing_mandatory_families = sorted(
                MANDATORY_PRIMARY_EVIDENCE_FAMILIES[
                    requirement.verification_kind
                ]
                - present_primary_families
            )
            if missing_mandatory_families:
                # A mandatory family exists to stop *weaker* evidence from
                # standing in for what the requirement needs.  It must not also
                # block *stronger* evidence.  When a primary assertion already
                # calls a decision procedure that settles the proposition over
                # the whole quantified domain (see discover/capability.py), the
                # mandatory family adds no information and demanding it can make
                # the obligation unsatisfiable -- pair 0029 is the worked case.
                waiver = mandatory_waiver(
                    requirement.verification_kind,
                    tuple(item.expression for item in primary_assertions),
                )
                if (
                    waiver is None
                    and missing_mandatory_families == ["fbmcq"]
                    and frozen.fbmcq_canary
                    and frozen.fbmcq_canary.get("feasible") is False
                ):
                    # Bounded formal checking does not run on this model at all
                    # (deterministic pair-level canary, recorded in the run
                    # record).  Demanding it would make the obligation
                    # unsatisfiable no matter what the producer writes, so the
                    # requirement falls back to its strongest available primary
                    # and the limitation is published instead of hidden.
                    waiver = (
                        "fbmcq_canary",
                        "Pair-level FBMCQ canary reported "
                        f"{frozen.fbmcq_canary.get('reason')} at bound "
                        f"{frozen.fbmcq_canary.get('bound')} after "
                        f"{frozen.fbmcq_canary.get('elapsed_ms')} ms; bounded "
                        "formal evidence is not obtainable on this model.",
                    )
                if waiver is None:
                    raise ValueError(
                        f"{requirement.verification_kind} requirement "
                        f"{requirement.requirement_id} is missing mandatory primary "
                        f"evidence families: {missing_mandatory_families}. Additional "
                        "exact primary evidence may complement but cannot replace them"
                    )
                mandatory_waivers.append(
                    {
                        "requirement_id": requirement.requirement_id,
                        "verification_kind": requirement.verification_kind,
                        "waived_families": missing_mandatory_families,
                        "decisive_function": waiver[0],
                        "justification": waiver[1],
                    }
                )
            # Non-vacuity is a contract property, not a style preference: a
            # query whose truth value cannot change when the defect is present
            # is not evidence at all.  The prompts already say so; enforcing it
            # here turns a wasted LLM round trip into an immediate, specific
            # finding.
            vacuity_findings = tuple(
                f"{assertion.assertion_id}: {finding}"
                for assertion in primary_assertions
                for finding in condition_non_vacuity_findings(assertion.expression)
            )
            phase = str(
                (requirement.source_context or {}).get("behavior_phase", "")
            ).lower()
            if not anchors_at_initialization(requirement.source_context):
                source_blind = tuple(
                    f"{assertion.assertion_id}: {call}(...) omits source"
                    for assertion in primary_assertions
                    for call in source_omitting_response_calls(assertion.expression)
                )
                if source_blind:
                    raise ValueError(
                        f"requirement {requirement.requirement_id} "
                        f"(behavior_phase={phase or 'unset'!r}) has "
                        f"source-blind primary evidence: {list(source_blind)}. "
                        "Without `source` the claim is only about the initial "
                        "configuration, which is initialization-only evidence for any "
                        "phase but `initialization`. Pin the exact source, one "
                        "assertion per source the requirement ranges over"
                    )
            if vacuity_findings:
                raise ValueError(
                    f"requirement {requirement.requirement_id} has non-evidential "
                    f"bounded formal primaries: {list(vacuity_findings)}"
                )
            coverage_keys = [assertion.coverage_key for assertion in primary_assertions]
            if len(coverage_keys) != len(set(coverage_keys)):
                raise ValueError(
                    f"requirement {requirement.requirement_id} contains duplicate "
                    "primary coverage_key values"
                )
        if any(not ids for ids in mapped_by_assertions.values()):
            missing = sorted(
                req_id for req_id, ids in mapped_by_assertions.items() if not ids
            )
            raise ValueError(
                f"every requirement needs an assertion; missing: {missing}"
            )
        if set(output.requirement_mapping) != req_ids:
            raise ValueError(
                "requirement_mapping keys must exactly match RequirementSet ids"
            )
        for req_id, mapped_ids in output.requirement_mapping.items():
            if set(mapped_ids) != mapped_by_assertions[req_id]:
                raise ValueError(
                    f"requirement_mapping for {req_id} does not match assertion ownership"
                )
            if not set(mapped_ids).issubset(assertion_ids):
                raise ValueError(
                    f"requirement_mapping for {req_id} references unknown assertion"
                )
        record = _record_node(
            state,
            node_name="convert_assertions",
            revision=output.revision,
            kind="llm",
            input_value=payload,
            output_value=output,
            started_at=started_at,
            start_ns=start_ns,
            details=(
                {
                    key: value
                    for key, value in (
                        ("mandatory_evidence_waivers", mandatory_waivers),
                        ("untested_claim_paths", untested_claim_paths),
                    )
                    if value
                }
                or None
            ),
        )
        llm_record = _llm_call_record(
            state,
            responder=responder,
            node_record=record,
            role="assertion_converter",
            revision=output.revision,
            system_prompt=prompts.ASSERTION_CONVERTER_PROMPT,
            user_prompt=payload,
            output=output,
        )
        revision_ledger = _append_revision_event(
            state,
            field="_assertion_revision_ledger",
            loop="assertions",
            event="artifact_created",
            revision=output.revision,
            artifact_hash=sha256_data(output),
            status="created",
            artifact_delta=_revision_delta(current, output),
        )
        return {
            "assertion_script": output,
            "_assertion_feedback": None,
            "_assertion_revision_ledger": revision_ledger,
            "assertion_fingerprints": (
                *state.get("assertion_fingerprints", ()),
                fingerprint,
            ),
            "_assertion_conversion_contract_feedback": None,
            **(
                {"_assertion_review_repair_count": MAX_ASSERTION_REVIEW_REPAIRS}
                if review_exhausted_by_repeat
                else {}
            ),
            # NOTE: _assertion_contract_repair_count is deliberately NOT reset
            # here.  Resetting on every success let a fail/succeed/fail producer
            # cycle past MAX_ASSERTION_CONTRACT_REPAIRS indefinitely (pair 0029
            # burned six resets).  The budget is per run, not per streak.
            "node_execution_records": _append_records(state, record),
            "llm_call_records": [*state.get("llm_call_records", []), llm_record],
        }
    except Exception as exc:
        message = f"{type(exc).__name__}: {exc}"
        repair_count = state.get("_assertion_contract_repair_count", 0)
        contract_failure_signature = (
            sha256_data(
                {
                    "script": output.model_dump(mode="json", exclude={"revision"}),
                    "failure": message,
                }
            )
            if output is not None
            else None
        )
        repeated_contract_failure = (
            contract_failure_signature is not None
            and contract_failure_signature
            in state.get("_assertion_contract_failure_signatures", ())
        )
        can_revise_contract = (
            output is not None
            and "no-progress gate" not in message
            and not repeated_contract_failure
            and repair_count < MAX_ASSERTION_CONTRACT_REPAIRS
        )
        if repeated_contract_failure:
            failure_message = (
                "no-progress gate rejected repeated contract-invalid "
                "AssertionScript semantics"
            )
            return _fail_state(
                state,
                "convert_assertions",
                ValueError(failure_message),
                started_at=started_at,
                start_ns=start_ns,
                input_value=locals().get("payload", state),
                revision=output.revision if output is not None else 0,
                kind="llm",
                responder=responder,
                role="assertion_converter",
            )
        if can_revise_contract:
            contract_feedback = RevisionFeedback(
                target="assertions",
                origin="assertion_contract",
                reason=(
                    "The previous Assertion Converter response violated the deterministic "
                    "script contract. Revise the existing script instead of changing the "
                    "requirements."
                ),
                findings=(message,),
            )
            record = _record_node(
                state,
                node_name="convert_assertions",
                revision=output.revision,
                kind="llm",
                input_value=locals().get("payload", state),
                output_value=output,
                started_at=started_at,
                start_ns=start_ns,
                failure=message,
            )
            llm_record = _llm_call_record(
                state,
                responder=responder,
                node_record=record,
                role="assertion_converter",
                revision=output.revision,
                system_prompt=prompts.ASSERTION_CONVERTER_PROMPT,
                user_prompt=locals().get("payload", ""),
                output=output,
            )
            return {
                "assertion_script": output,
                "_assertion_feedback": contract_feedback,
                "_assertion_conversion_contract_feedback": contract_feedback,
                "_assertion_contract_repair_count": repair_count + 1,
                "_assertion_feedback_history": _append_feedback(
                    state, contract_feedback
                ),
                "_assertion_revision_ledger": _append_revision_event(
                    state,
                    field="_assertion_revision_ledger",
                    loop="assertions",
                    event="artifact_rejected",
                    revision=output.revision,
                    artifact_hash=sha256_data(output),
                    status="contract_invalid",
                    artifact_delta=_revision_delta(current, output),
                    rationale=contract_feedback.reason,
                    findings=contract_feedback.findings,
                ),
                "_assertion_contract_failure_signatures": (
                    *state.get("_assertion_contract_failure_signatures", ()),
                    *(
                        (contract_failure_signature,)
                        if contract_failure_signature
                        else ()
                    ),
                ),
                "node_execution_records": _append_records(state, record),
                "llm_call_records": [
                    *state.get("llm_call_records", []),
                    llm_record,
                ],
            }
        return _fail_state(
            state,
            "convert_assertions",
            exc,
            started_at=started_at,
            start_ns=start_ns,
            input_value=locals().get("payload", state),
            revision=current.revision if current is not None else 0,
            kind="llm",
            responder=responder,
            role="assertion_converter",
        )


def precheck_and_seal(
    state: DiscoverGraphState,
    *,
    sealed_store: InMemorySealedStore,
    assertion_checker: AssertionChecker | None = None,
) -> DiscoverGraphState:
    started_at, start_ns = _now(), time.perf_counter_ns()
    try:
        frozen = state["frozen_inputs"]
        script = state["assertion_script"]
        script_hash = sha256_data(script)
        public_executions: list[AssertionExecutionPublic] = []
        sealed_results: list[AssertionResult] = []
        source_entries = frozen.source_trace.get("entries", [])
        source_entries = source_entries if isinstance(source_entries, list) else []
        source_exclusions = frozen.source_trace.get("attribution_exclusions", [])
        source_exclusions = (
            source_exclusions if isinstance(source_exclusions, list) else []
        )
        checker = assertion_checker or AssertionChecker(
            build_eval_environment(
                model_text=frozen.stm_text,
                source_mappings=source_entries,
                source_exclusions=source_exclusions,
            )
        )
        family_map = {
            "structure": "structure",
            "topology": "structure",
            "relation": "relation",
            "effect": "effect",
            "simulation": "simulation",
            "fbmcq": "formal",
            "provenance": "mapping",
        }
        requirement_set = state.get("requirement_set")
        requirement_by_id = (
            {
                requirement.requirement_id: requirement
                for requirement in requirement_set.requirements
            }
            if requirement_set is not None
            else {}
        )
        assertion_families_by_requirement: dict[str, set[str]] = {}
        for item in script.assertions:
            assertion_families_by_requirement.setdefault(
                item.requirement_id, set()
            ).add(item.evidence_family)
        # Topological order, not declaration order (issue #170 §11.5).  A
        # dependent must not run before the prerequisite whose truth decides
        # whether it runs at all -- `variable_delta_after` on a variable that does
        # not exist has nothing to compute, and forcing it to answer produced
        # either a false built on the converter's own route token or an
        # unrepairable refusal.  Ties break by id so two identical scripts execute
        # identically; the sealed result is hashed.
        by_id = {item.assertion_id: item for item in script.assertions}
        ordered = tuple(
            by_id[aid] for aid in execution_order(script.assertions) if aid in by_id
        )
        #: `{assertion_id: strict bool}` for assertions that produced a verdict.
        #: An id absent here was blocked or non-executable, and `blocked_by` treats
        #: both as an unmet prerequisite.
        truth: dict[str, Any] = {}
        for assertion in ordered:
            unmet = blocked_by(assertion, truth)
            if unmet:
                # Not run.  Recorded so the report can say *why* it was skipped,
                # but `blocked` is a runtime state only: downstream counts it as
                # not satisfied, and the prerequisite's own False is the finding.
                public_executions.append(
                    AssertionExecutionPublic(
                        assertion_id=assertion.assertion_id,
                        requirement_id=assertion.requirement_id,
                        role=assertion.role,
                        coverage_key=assertion.coverage_key,
                        status="blocked",
                        error=(
                            "prerequisite(s) "
                            + ", ".join(unmet)
                            + " did not hold, so this claim has nothing to evaluate"
                        ),
                    )
                )
                continue
            source = (
                f"{script.prefix.rstrip()}\nassert ({assertion.expression}), "
                f"{assertion.failure_message!r}"
                if script.prefix.strip()
                else f"assert ({assertion.expression}), {assertion.failure_message!r}"
            )
            checked = checker.check(
                source,
                reason=assertion.description,
                required_function_families=[family_map[assertion.evidence_family]],
            )
            hot_start_policy_error: str | None = None
            formal_causality_error: str | None = None
            requirement = requirement_by_id.get(assertion.requirement_id)
            if (
                requirement is not None
                and requirement.verification_kind == "behavior"
                and assertion.evidence_family == "simulation"
                and checked.outcome in {"valid", "sealed_false"}
                and type(checked.value) is bool
                and "fbmcq"
                not in assertion_families_by_requirement.get(
                    assertion.requirement_id, set()
                )
            ):
                # The producer no longer calls `simulate`; it calls a Family B
                # predicate, and the predicate hot-starts the configuration its
                # `source` binding names.  Scanning the trace for a `simulate`
                # kwarg therefore matched nothing and rejected every behavior
                # assertion, taking the runtime half of the loop dark.  The
                # property still worth enforcing is the same one: the claim must
                # be pinned to a named configuration rather than to wherever a
                # cold start happens to land.
                behaviour_calls = [
                    call
                    for call in checked.function_call_trace
                    if PREDICATE_FAMILIES.get(call.function, ("", ""))[0] == "simulation"
                ]
                # Not every Family B predicate spells its pinning argument
                # `source`: `terminates` takes `scope`.  Requiring `source`
                # rejected every `terminates` assertion and handed back repair
                # text naming `initial_state`/`cycles`, which are not parameters
                # of anything -- the item could only churn until its budget ran
                # out.
                pinning = ("source", "scope", "state", "composite")
                has_hot_start = any(
                    any(
                        isinstance(call.kwargs.get(k), str) and call.kwargs[k].strip()
                        for k in pinning
                    )
                    for call in behaviour_calls
                )
                source_context = requirement.source_context
                is_initial_configuration = (
                    isinstance(source_context, dict)
                    and source_context.get("behavior_phase") == "initialization"
                )
                if behaviour_calls and not has_hot_start and not is_initial_configuration:
                    hot_start_policy_error = (
                        "a behavior requirement must pin its claim to a named "
                        "configuration: pass the Requirement's `source` binding to "
                        "the predicate. Only a requirement whose source_context "
                        "declares behavior_phase=initialization may leave `source` "
                        "empty, because there the initial configuration is the "
                        "claim. An unpinned observation is about wherever a cold "
                        "start happened to land, not about the state the NL names"
                    )
            # A verdict sealed off an empty declaration table ran no bounded
            # query, so there is no query to judge causal.  Without this the
            # check saw zero formal calls, concluded the evidence was
            # non-causal, and sent the assertion back for repairs it cannot
            # make -- five rounds, then a coverage gap.  That is the pair-0006
            # regression coming back through a different door.
            if (
                requirement is not None
                and requirement.verification_kind == "behavior"
                and assertion.evidence_family == "fbmcq"
                and checked.outcome in {"valid", "sealed_false"}
                and type(checked.value) is bool
            ):
                formal_calls = [
                    call
                    for call in checked.function_call_trace
                    if PREDICATE_FAMILIES.get(call.function, ("", ""))[0] == "formal"
                    and call.status == "completed"
                ]
                causality_checks = [
                    formal_query_causality(call.kwargs.get("query", ""))
                    for call in formal_calls
                ]
                if not formal_calls or any(
                    not check["causal"] for check in causality_checks
                ):
                    details = [
                        check["reason"]
                        for check in causality_checks
                        if not check["causal"]
                    ]
                    formal_causality_error = (
                        "behavior requirement FBMCQ evidence must connect the bounded "
                        "property to an explicit event/condition or initialization; "
                        "a bare reach target is not causal evidence. Replace it with "
                        "a response query such as `check response <= 5: trigger "
                        'event("<declared_event_path>", current) -> within 3 '
                        'active("<target_state_path>");`, '
                        "a positive event assumption plus reach, an explicit `init "
                        'state("<exact_initial_state_path>");` query, or a hot-start simulation. '
                        + " ".join(details)
                    )
            if (
                hot_start_policy_error is None
                and formal_causality_error is None
                and checked.outcome in {"valid", "sealed_false"}
                and type(checked.value) is bool
            ):
                # Published before the dependents run, which is the whole point of
                # the topological order.
                truth[assertion.assertion_id] = checked.value
                public_executions.append(
                    AssertionExecutionPublic(
                        assertion_id=assertion.assertion_id,
                        requirement_id=assertion.requirement_id,
                        role=cast(Any, assertion.role or "primary"),
                        coverage_key=assertion.coverage_key,
                        status="executable",
                    )
                )
                sealed_results.append(
                    AssertionResult(
                        assertion_id=assertion.assertion_id,
                        requirement_id=assertion.requirement_id,
                        role=cast(Any, assertion.role or "primary"),
                        coverage_key=assertion.coverage_key,
                        aggregation_group=assertion.aggregation_group,
                        truth_value=checked.value,
                        script_hash=script_hash,
                        tool_env_hash=frozen.tool_env_hash,
                        evidence_family=assertion.evidence_family,
                        failure_message=(
                            assertion.failure_message
                            if checked.value is False
                            else None
                        ),
                        evidence_scope={
                            "required_function_families": list(
                                checked.required_function_families
                            ),
                            "actual_function_families": list(
                                checked.actual_function_families
                            ),
                        },
                        evidence_record_ids=tuple(
                            f"{assertion.assertion_id}:call:{index:02d}"
                            for index, _ in enumerate(
                                checked.function_call_trace, start=1
                            )
                        ),
                        check_detail=checked.to_json(),
                    )
                )
            else:
                detail = checked.to_json()
                if hot_start_policy_error is not None:
                    pass_criterion = (
                        "Rewrite every simulation call for this behavior requirement "
                        "as an explicit hot start with initial_state=<exact state "
                        "path> and initial_vars={<exact declaration name>: value}; "
                        "use declaration names, not qualified state-machine paths, "
                        "and put the causal event in cycle 0. For a causal initialization "
                        "claim, use an explicit cold path cycles=[[], [causal_event]]. "
                        "For a pure initial-configuration claim explicitly marked "
                        "behavior_phase=initialization, use one or more empty cold-start "
                        "cycles and inspect the initialized state. Alternatively replace "
                        "it with a causal bounded FBMCQ query. "
                        "The full assertion must then execute without exception and "
                        "return strict bool."
                    )
                elif formal_causality_error is not None:
                    if "parse failed" in str(formal_causality_error):
                        pass_criterion = (
                            "Use only the documented FBMCQ grammar. Replace the "
                            "parse-invalid query with a syntactically valid causal "
                            'query, preferably `init state("<exact_initial_state_path>"); check '
                            'reach <= 5: active("<target_state_path>");`, or use an explicit '
                            "hot-start simulation; the full assertion must execute "
                            "without exception and return strict bool."
                        )
                    else:
                        pass_criterion = (
                            "Replace a bare reach query with a causal bounded FBMCQ "
                            "query containing an event assumption, response trigger, "
                            "or explicit initialization; alternatively use an explicit "
                            "hot-start simulation. The full assertion must execute "
                            "without exception and return strict bool."
                        )
                elif (
                    isinstance(detail.get("error"), dict)
                    and detail["error"].get("type") == "RequiredFamilyMissing"
                ):
                    pass_criterion = (
                        "Change evidence_family to match the function actually "
                        "called: states/events/variables/initial_child are "
                        "structure, while transitions/transition_exists/"
                        "guards_overlap are relation. Or replace the expression "
                        "with a call from the declared family; then the full "
                        "assertion must execute without exception and return "
                        "strict bool."
                    )
                elif isinstance(detail.get("error"), dict) and (
                    detail["error"].get("type") == "NameError"
                    or (
                        detail["error"].get("type") == "AuditRejected"
                        and any(
                            issue.get("code") == "unknown_name"
                            for issue in detail.get("audit", {}).get("issues", [])
                            if isinstance(issue, dict)
                        )
                    )
                ):
                    pass_criterion = (
                        "Do not rename an undefined alias or convert it to an "
                        "uppercase token. Remove bare aliases by writing a quoted "
                        "complete state/event path directly in every path, event, "
                        "initial_state, and cycle argument. Only keep an alias when "
                        "the same script prefix explicitly assigns that exact name; "
                        "then the full prefix plus this assertion must execute "
                        "without exception and return strict bool using the declared "
                        "evidence family."
                    )
                else:
                    pass_criterion = (
                        "The full prefix plus this assertion must execute without "
                        "exception and return strict bool using the declared "
                        "evidence family."
                    )
                error_payload = {
                    "assertion_id": assertion.assertion_id,
                    "error": (
                        hot_start_policy_error
                        or formal_causality_error
                        or detail.get("error")
                    ),
                    "audit_issues": (detail.get("audit") or {}).get("issues", []),
                    "actual_function_families": detail.get(
                        "actual_function_families", []
                    ),
                    "required_function_families": detail.get(
                        "required_function_families", []
                    ),
                    "pass_criterion": pass_criterion,
                }
                public_executions.append(
                    AssertionExecutionPublic(
                        assertion_id=assertion.assertion_id,
                        requirement_id=assertion.requirement_id,
                        role=cast(Any, assertion.role or "primary"),
                        coverage_key=assertion.coverage_key,
                        status="invalid",
                        error=str(error_payload),
                    )
                )
        status = (
            "invalid"
            if any(item.status == "invalid" for item in public_executions)
            else "executable"
        )
        public = AssertionCheckPublic(
            script_hash=script_hash,
            tool_env_hash=frozen.tool_env_hash,
            status=status,
            executions=tuple(public_executions),
        )
        sealed_hash = sha256_data(sealed_results)
        sealed_ref = sealed_store.put(sealed_hash, tuple(sealed_results))
        receipt = SealedAssertionReceipt(
            script_hash=script_hash,
            tool_env_hash=frozen.tool_env_hash,
            sealed_hash=sealed_hash,
            result_count=len(sealed_results),
            sealed_payload_ref=sealed_ref,
        )
        update: DiscoverGraphState = {
            "assertion_check_public": public,
            "sealed_assertion_results": receipt,
            "_assertion_revision_ledger": _append_revision_event(
                state,
                field="_assertion_revision_ledger",
                loop="assertions",
                event="check_completed",
                revision=script.revision,
                artifact_hash=script_hash,
                status=public.status,
                rationale=(
                    "Every assertion is executable under the public check contract."
                    if public.status == "executable"
                    else "Public precheck found non-executable assertions."
                ),
                findings=tuple(
                    execution.error or execution.assertion_id
                    for execution in public.executions
                    if execution.status == "invalid"
                ),
            ),
        }
        precheck_rounds = state.get("_precheck_round_count", 0) + 1
        update["_precheck_round_count"] = precheck_rounds
        if status == "invalid":
            invalid_ids = tuple(
                sorted(
                    item.assertion_id
                    for item in public_executions
                    if item.status == "invalid"
                )
            )
            # Progress is "this item got closer to executable", not "the text
            # changed".  A byte-level signature over (expression, error) never
            # repeats against a producer that rewrites its query every round --
            # in the pair-0029 runs it fired once in twelve revisions for GPT
            # and never for Claude, so nothing was ever quarantined.  Key on the
            # *semantic* failure identity instead, and additionally bound each
            # item so churn alone cannot buy unlimited revisions.
            coverage_key_by_id = {
                item.assertion_id: item.coverage_key for item in script.assertions
            }
            semantic_keys = {
                item.assertion_id: _semantic_invalid_key(
                    item.assertion_id,
                    item.error,
                    coverage_key_by_id.get(item.assertion_id),
                )
                for item in public_executions
                if item.status == "invalid"
            }
            semantic_counts = dict(state.get("_assertion_invalid_semantic_counts", {}))
            item_repairs = dict(state.get("_assertion_item_repair_counts", {}))
            for assertion_id, key in semantic_keys.items():
                semantic_counts[key] = semantic_counts.get(key, 0) + 1
                item_repairs[assertion_id] = item_repairs.get(assertion_id, 0) + 1
            update["_assertion_invalid_semantic_counts"] = semantic_counts
            update["_assertion_item_repair_counts"] = item_repairs

            # A bounded query the model is too large for is not repairable by
            # rewriting it, and each retry costs ~25s of wall clock, so stop
            # after the first.
            unrepairable_markers = ("exceeded its budget on this model",)
            unrepairable_ids = tuple(
                item.assertion_id
                for item in public_executions
                if item.status == "invalid"
                and any(m in str(item.error or "") for m in unrepairable_markers)
            )
            exhausted_ids = tuple(
                assertion_id
                for assertion_id in invalid_ids
                if assertion_id in unrepairable_ids
                or item_repairs.get(assertion_id, 0) >= MAX_ASSERTION_PRECHECK_REPAIRS
                or semantic_counts.get(semantic_keys[assertion_id], 0)
                >= NO_PROGRESS_SEMANTIC_REPEATS
            )
            no_progress_ids = tuple(
                assertion_id
                for assertion_id in invalid_ids
                if semantic_counts.get(semantic_keys[assertion_id], 0) >= 2
            )
            # Only isolate once every still-invalid item has run out of budget;
            # a repairable neighbour must keep its remaining revisions.  The
            # round backstop makes the precheck<->convert edge bounded even if
            # a future change breaks the per-item accounting.
            quarantine_now = (
                bool(exhausted_ids) and set(exhausted_ids) == set(invalid_ids)
            ) or precheck_rounds >= MAX_PRECHECK_ROUNDS
            previous_signatures = state.get("_assertion_invalid_signatures", ())
            update["_assertion_invalid_signatures"] = (
                *previous_signatures,
                *sorted(semantic_keys.values()),
            )
            update["_assertion_feedback"] = RevisionFeedback(
                target="assertions",
                origin="assertion_precheck",
                reason=(
                    "Assertion precheck found non-executable expressions. Fix every "
                    "listed assertion; do not return the same failing expression. "
                    "If a formal query cannot encode the stated causal condition, "
                    "replace it with an executable hot-start simulation instead."
                ),
                findings=tuple(
                    e.error or e.assertion_id
                    for e in public_executions
                    if e.status == "invalid"
                ),
                target_item_ids=invalid_ids,
            )
            update["_assertion_feedback_history"] = _append_feedback(
                state, update["_assertion_feedback"]
            )
        else:
            quarantine_now = False
            no_progress_ids = ()
            exhausted_ids = ()
            update["_last_executable_assertion_script"] = script
            update["_assertion_no_progress_recovery_count"] = 0
        record = _record_node(
            state,
            node_name="precheck_and_seal",
            revision=script.revision,
            kind="deterministic",
            input_value={"script_hash": script_hash},
            output_value=public,
            started_at=started_at,
            start_ns=start_ns,
            details={
                "status": public.status,
                "invalid_assertion_ids": [
                    item.assertion_id
                    for item in public.executions
                    if item.status == "invalid"
                ],
                "no_progress_assertion_ids": list(no_progress_ids),
                "budget_exhausted_assertion_ids": list(exhausted_ids),
            },
        )
        if status == "invalid" and (quarantine_now or no_progress_ids):
            recovery_count = state.get("_assertion_no_progress_recovery_count", 0)
            if not quarantine_now and recovery_count < MAX_ASSERTION_NO_PROGRESS_RECOVERIES:
                last_executable = state.get("_last_executable_assertion_script")
                seed_assertions = (
                    {
                        item.assertion_id: item.model_dump(mode="json")
                        for item in last_executable.assertions
                        if item.assertion_id in invalid_ids
                    }
                    if last_executable is not None
                    else {}
                )
                recovery_feedback = RevisionFeedback(
                    target="assertions",
                    origin="assertion_precheck",
                    reason=(
                        "Targeted no-progress recovery: repair only the listed "
                        "assertions. Start from the last deterministic-executable "
                        "version when supplied, preserve all unresolved Reviewer "
                        "findings, and do not modify unrelated accepted assertions."
                    ),
                    findings=tuple(
                        e.error or e.assertion_id
                        for e in public_executions
                        if e.status == "invalid"
                    ),
                    target_item_ids=invalid_ids,
                    recovery_seed={
                        "last_executable_assertions": seed_assertions,
                        "unresolved_feedback": [
                            item.model_dump(mode="json")
                            for item in state.get("_assertion_feedback_history", ())
                        ],
                    },
                )
                update["_assertion_feedback"] = recovery_feedback
                update["_assertion_feedback_history"] = _append_feedback(
                    state, recovery_feedback
                )
                update["_assertion_no_progress_recovery_count"] = recovery_count + 1
                update["node_execution_records"] = _append_records(state, record)
                return update

            accepted_ids = {
                item.assertion_id
                for item in public_executions
                if item.status == "executable"
            }
            filtered_script = _filter_assertion_script(script, accepted_ids)
            filtered_script_hash = sha256_data(filtered_script)
            filtered_executions = tuple(
                item for item in public_executions if item.status == "executable"
            )
            filtered_public = AssertionCheckPublic(
                script_hash=filtered_script_hash,
                tool_env_hash=frozen.tool_env_hash,
                status="executable",
                executions=filtered_executions,
            )
            filtered_results = tuple(
                result.model_copy(update={"script_hash": filtered_script_hash})
                for result in sealed_results
                if result.assertion_id in accepted_ids
            )
            filtered_sealed_hash = sha256_data(filtered_results)
            filtered_sealed_ref = sealed_store.put(
                filtered_sealed_hash, filtered_results
            )
            filtered_receipt = SealedAssertionReceipt(
                script_hash=filtered_script_hash,
                tool_env_hash=frozen.tool_env_hash,
                sealed_hash=filtered_sealed_hash,
                result_count=len(filtered_results),
                sealed_payload_ref=filtered_sealed_ref,
            )
            spec_by_id = {item.assertion_id: item for item in script.assertions}
            requirement_by_id = {
                item.requirement_id: item
                for item in state["requirement_set"].requirements
            }
            gaps = tuple(
                CoverageGap(
                    gap_id=f"GAP-{assertion_id}-NO-PROGRESS",
                    stage="assertion_conversion",
                    requirement_id=spec_by_id[assertion_id].requirement_id,
                    assertion_ids=(assertion_id,),
                    source_segment_ids=requirement_by_id[
                        spec_by_id[assertion_id].requirement_id
                    ].source_segment_ids,
                    reason_code=(
                        "revision_budget_exhausted"
                        if item_repairs.get(assertion_id, 0)
                        >= MAX_ASSERTION_PRECHECK_REPAIRS
                        else "no_progress"
                    ),
                    reason=(
                        "The assertion exhausted its item-local precheck budget "
                        f"({item_repairs.get(assertion_id, 0)}/"
                        f"{MAX_ASSERTION_PRECHECK_REPAIRS} repairs) or repeated the "
                        "same semantic failure identity "
                        f"({semantic_counts.get(semantic_keys.get(assertion_id, ''), 0)}"
                        f"/{NO_PROGRESS_SEMANTIC_REPEATS}) despite expression churn."
                    ),
                    last_revision=script.revision,
                    last_feedback=update["_assertion_feedback"].reason,
                    history_refs=tuple(
                        f"assertion-ledger:{event.sequence}"
                        for event in state.get("_assertion_revision_ledger", ())
                    ),
                    coverage_impact=(
                        f"Coverage key {spec_by_id[assertion_id].coverage_key} "
                        "was not released."
                    ),
                    blocks_full_coverage=(
                        (spec_by_id[assertion_id].role or "primary") == "primary"
                    ),
                )
                for assertion_id in invalid_ids
            )
            ledger = tuple(update["_assertion_revision_ledger"])
            quarantine_event = RevisionLedgerEvent(
                sequence=len(ledger) + 1,
                loop="assertions",
                event="artifact_quarantined",
                revision=script.revision,
                artifact_hash=script_hash,
                status="quarantined",
                rationale=(
                    "Repeated invalid assertions were isolated after targeted "
                    "recovery; executable assertions continue."
                ),
                findings=tuple(gap.reason for gap in gaps),
                item_ids=invalid_ids,
                budget_counters={"no_progress_targeted_recovery": recovery_count},
            )
            update.update(
                {
                    "assertion_script": filtered_script,
                    "assertion_check_public": filtered_public,
                    "sealed_assertion_results": filtered_receipt,
                    "coverage_gaps": _append_coverage_gaps(state, *gaps),
                    "_quarantined_assertion_ids": tuple(
                        sorted(
                            {
                                *state.get("_quarantined_assertion_ids", ()),
                                *invalid_ids,
                            }
                        )
                    ),
                    "_assertion_revision_ledger": (
                        *ledger,
                        quarantine_event,
                    ),
                    "_assertion_feedback": None,
                    "_last_executable_assertion_script": filtered_script,
                }
            )
            update["node_execution_records"] = _append_records(state, record)
            return update
        update["node_execution_records"] = _append_records(state, record)
        return update
    except Exception as exc:
        return _fail_state(
            state,
            "precheck_and_seal",
            exc,
            started_at=started_at,
            start_ns=start_ns,
            input_value=state.get("assertion_script"),
            revision=state.get("assertion_script").revision
            if state.get("assertion_script")
            else 0,
        )


def review_assertions(
    state: DiscoverGraphState,
    responder: StructuredResponder,
    *,
    sealed_store: InMemorySealedStore | None = None,
) -> DiscoverGraphState:
    started_at, start_ns = _now(), time.perf_counter_ns()
    try:
        frozen = state["frozen_inputs"]
        requirements = state["requirement_set"]
        script = state["assertion_script"]
        public_check = state["assertion_check_public"]
        payload = renderer.render_assertion_review_input(
            frozen,
            requirements,
            script,
            public_check,
            tuple(state.get("_assertion_revision_ledger", ())),
            state.get("coverage_gaps", ()),
        )
        # Guard the explicit truth-label hiding contract before the LLM call.
        sealed_hash = (
            state.get("sealed_assertion_results").sealed_hash
            if state.get("sealed_assertion_results")
            else ""
        )
        if sealed_hash and sealed_hash in payload:
            raise ValueError("Assertion Reviewer payload leaks sealed result reference")
        output = responder.invoke_structured(
            role="assertion_reviewer",
            schema=AssertionReview,
            system_prompt=prompts.ASSERTION_REVIEWER_PROMPT,
            user_input=payload,
        )
        script_hash = sha256_data(script)
        hash_binding, hash_note = _classify_reviewed_hash(
            output.reviewed_script_hash, script_hash
        )
        if hash_binding != "exact":
            # This binding exists to prove the reviewer judged the *current*
            # revision.  The payload is rendered fresh from that revision on
            # every call, so the model cannot actually see a stale script -- the
            # only thing an exact-string test detects is a transcription slip on
            # a 64-character hex value.  GPT-5.5 produced exactly that on pair
            # 0029 (correct 32-char prefix, then a repeated middle fragment) and
            # the whole run died.  Record the discrepancy as a first-class audit
            # fact and continue with the computed hash; Issue #167 §3 does not
            # allow a local defect to become RUN_FAILED.
            output = output.model_copy(update={"reviewed_script_hash": script_hash})
        update: DiscoverGraphState = {"assertion_review": output}
        update["_assertion_revision_ledger"] = _append_revision_event(
            state,
            field="_assertion_revision_ledger",
            loop="assertions",
            event="review_completed",
            revision=script.revision,
            artifact_hash=script_hash,
            status=output.decision,
            rationale=output.rationale,
            findings=tuple(f.message for f in output.findings),
        )
        review_repair_count = state.get("_assertion_review_repair_count", 0)
        if output.decision == "revise":
            targeted_assertion_ids = tuple(
                sorted(
                    {
                        finding.assertion_id
                        for finding in output.findings
                        if finding.assertion_id is not None
                    }
                )
            )
            update["_assertion_feedback"] = RevisionFeedback(
                target="assertions",
                origin="assertion_review",
                reason=output.rationale,
                findings=tuple(f.message for f in output.findings),
                target_item_ids=targeted_assertion_ids,
            )
            update["_assertion_review_repair_count"] = review_repair_count + 1
            update["_assertion_feedback_history"] = _append_feedback(
                state, update["_assertion_feedback"]
            )
        record = _record_node(
            state,
            node_name="review_assertions",
            revision=script.revision,
            kind="llm",
            input_value=payload,
            output_value=output,
            started_at=started_at,
            start_ns=start_ns,
            details=(
                {"reviewed_hash_binding": hash_binding, "reviewed_hash_note": hash_note}
                if hash_binding != "exact"
                else None
            ),
        )
        llm_record = _llm_call_record(
            state,
            responder=responder,
            node_record=record,
            role="assertion_reviewer",
            revision=script.revision,
            system_prompt=prompts.ASSERTION_REVIEWER_PROMPT,
            user_prompt=payload,
            output=output,
        )
        update["node_execution_records"] = _append_records(state, record)
        update["llm_call_records"] = [*state.get("llm_call_records", []), llm_record]
        if (
            output.decision == "revise"
            and review_repair_count >= MAX_ASSERTION_REVIEW_REPAIRS
        ):
            # Issue #167 §3: an unresolved *local* review finding must not
            # escalate into RUN_FAILED.  Isolate the assertions the reviewer is
            # still unhappy with, publish everything else, and record the gap.
            # Only ids still present in the script can be isolated; a reviewer
            # may keep naming an item that a previous round already quarantined.
            present_ids = {item.assertion_id for item in script.assertions}
            targeted = set(targeted_assertion_ids) & present_ids
            retained_ids = present_ids - targeted
            if targeted and retained_ids and sealed_store is not None:
                update.update(
                    _quarantine_reviewed_assertions(
                        state,
                        script=script,
                        quarantined_ids=tuple(sorted(targeted)),
                        rationale=output.rationale,
                        findings=tuple(f.message for f in output.findings),
                        sealed_store=sealed_store,
                    )
                )
                update["_assertion_feedback"] = None
                update["assertion_review"] = output.model_copy(
                    update={
                        "decision": "accept",
                        "rationale": (
                            "Remaining assertions accepted after item-local "
                            "quarantine of review-unresolved assertions."
                        ),
                    }
                )
                return update
            if not targeted and retained_ids:
                # Every named item was already quarantined in an earlier round;
                # the reviewer is repeating a resolved finding.  Accept what is
                # left instead of failing the run over a stale objection.
                update["_assertion_feedback"] = None
                update["assertion_review"] = output.model_copy(
                    update={
                        "decision": "accept",
                        "rationale": (
                            "Remaining assertions accepted; every flagged item was "
                            "already isolated and recorded as a coverage gap."
                        ),
                    }
                )
                return update
            message = (
                "bounded review gate: Assertion Reviewer requested more than "
                f"{MAX_ASSERTION_REVIEW_REPAIRS} revisions and no assertion could "
                "be isolated while retaining a non-empty script"
            )
            update["failure"] = RunFailure(
                run_id=_run_id(state), node_name="review_assertions", message=message
            )
            failed_record = _record_node(
                state,
                node_name="review_assertions",
                revision=script.revision,
                kind="llm",
                input_value=payload,
                output_value=output,
                started_at=started_at,
                start_ns=start_ns,
                failure=message,
            )
            update["node_execution_records"] = [
                *update["node_execution_records"],
                failed_record,
            ]
        return update
    except Exception as exc:
        return _fail_state(
            state,
            "review_assertions",
            exc,
            started_at=started_at,
            start_ns=start_ns,
            input_value=locals().get("payload", state),
            revision=state.get("assertion_script").revision
            if state.get("assertion_script")
            else 0,
            kind="llm",
            responder=responder,
            role="assertion_reviewer",
        )


def release_results(
    state: DiscoverGraphState, *, sealed_store: InMemorySealedStore
) -> DiscoverGraphState:
    started_at, start_ns = _now(), time.perf_counter_ns()
    try:
        frozen = state["frozen_inputs"]
        script = state["assertion_script"]
        public = state["assertion_check_public"]
        receipt = state["sealed_assertion_results"]
        payload = tuple(sealed_store.release(receipt.sealed_hash))
        script_hash = sha256_data(script)
        if public.script_hash != script_hash or receipt.script_hash != script_hash:
            raise ValueError("script hash mismatch during sealed result release")
        if (
            public.tool_env_hash != frozen.tool_env_hash
            or receipt.tool_env_hash != frozen.tool_env_hash
        ):
            raise ValueError(
                "tool environment hash mismatch during sealed result release"
            )
        if sha256_data(payload) != receipt.sealed_hash:
            raise ValueError("sealed payload hash mismatch")
        released = ReleasedAssertionResults(
            script_hash=script_hash,
            tool_env_hash=frozen.tool_env_hash,
            sealed_hash=receipt.sealed_hash,
            results=payload,
        )
        record = _record_node(
            state,
            node_name="release_results",
            revision=script.revision,
            kind="deterministic",
            input_value={
                "script_hash": script_hash,
                "sealed_hash": receipt.sealed_hash,
            },
            output_value=released,
            started_at=started_at,
            start_ns=start_ns,
        )
        return {
            "released_assertion_results": released,
            "node_execution_records": _append_records(state, record),
        }
    except Exception as exc:
        return _fail_state(
            state,
            "release_results",
            exc,
            started_at=started_at,
            start_ns=start_ns,
            input_value=state.get("sealed_assertion_results"),
            revision=state.get("assertion_script").revision
            if state.get("assertion_script")
            else 0,
        )


def bind_attribution(state: DiscoverGraphState) -> DiscoverGraphState:
    started_at, start_ns = _now(), time.perf_counter_ns()
    try:
        frozen = state["frozen_inputs"]
        released = state["released_assertion_results"]
        entries = frozen.source_trace.get("entries", [])
        entries = entries if isinstance(entries, list) else []
        exclusions = frozen.source_trace.get("attribution_exclusions", [])
        exclusions = exclusions if isinstance(exclusions, list) else []
        simulation_is_ineligible = _working_contract_simulation_is_ineligible(
            frozen.working_contract
        )
        # A `precondition` on a proposed name observes only that name, which no
        # frozen trace entry covers, so on its own every such finding lands as
        # `unattributed` and is routed away from `issues`.  That is a regression
        # the split introduced: before it, the same finding rode on an assertion
        # that also bound the real source state, matched a trace entry, and was
        # published as a confirmed issue (pair 0006, both models).
        #
        # The obligation is still about real elements -- the ones its dependents
        # name.  So a precondition inherits their declared bindings, read from the
        # expression rather than from an execution trace, because a blocked
        # dependent never produced one.  The debt check runs over the same union,
        # so a dependent naming compiler-owned elements still yields
        # `representation_debt` rather than a source-level claim.
        # Read with `.get`: attribution never needed the script before, and a
        # caller that attributes one released result without one is legitimate.
        script = state.get("assertion_script")
        script_assertions = tuple(script.assertions) if script is not None else ()
        known_paths = frozenset(frozen.known_model_paths)
        expression_by_id = {
            item.assertion_id: item.expression for item in script_assertions
        }
        inherited_refs: dict[str, set[str]] = {}
        for item in script_assertions:
            for prerequisite in item.depends_on:
                inherited_refs.setdefault(prerequisite, set()).update(
                    declared_path_bindings(
                        expression_by_id.get(item.assertion_id, ""), known_paths
                    )
                )
        precondition_ids = {
            item.assertion_id
            for item in script_assertions
            if item.role == "precondition"
        }
        bindings = []
        for result in released.results:
            if result.truth_value:
                continue
            actual_families = {
                str(family)
                for family in (
                    result.evidence_scope.get("actual_function_families", [])
                    if isinstance(result.evidence_scope, dict)
                    else []
                )
            }
            detail_families = result.check_detail.get("actual_function_families", [])
            if isinstance(detail_families, (list, tuple, set)):
                actual_families.update(str(family) for family in detail_families)
            uses_simulation = (
                result.evidence_family == "simulation"
                or "simulation" in actual_families
            )
            observed = set(
                _flatten_strings(result.check_detail.get("function_call_trace", []))
            )
            if result.assertion_id in precondition_ids:
                observed |= inherited_refs.get(result.assertion_id, set())
            matched = [
                entry for entry in entries if _trace_entry_matches(entry, observed)
            ]
            matched_ids = tuple(
                str(entry.get("trace_id")) for entry in matched if entry.get("trace_id")
            )
            refs = tuple(
                sorted(
                    {
                        str(ref)
                        for entry in matched
                        for ref in entry.get("source_elements", [])
                        if isinstance(ref, str)
                    }
                )
            )
            debt_refs = tuple(
                sorted(
                    ref
                    for ref in exclusions
                    if _reference_matches_observed(str(ref), observed)
                )
            )
            if uses_simulation and simulation_is_ineligible:
                debt_refs = tuple(
                    sorted(
                        {
                            *debt_refs,
                            "contract:capability_eligibility.simulation",
                        }
                    )
                )
            safe_entries = [
                entry
                for entry in matched
                if isinstance(entry.get("attribution_boundary"), dict)
                and entry["attribution_boundary"].get("source_level_claim_allowed")
                is True
                and entry["attribution_boundary"].get("representation_related")
                is not True
                and entry["attribution_boundary"].get("conversion_or_lowering_related")
                is not True
            ]
            # A derived path that is not unique may hide a tainted segment, so
            # the resolved prefix must not be presented as a clean path.  The
            # marker is emitted by the evidence layer, not inferred here.
            path_ambiguous = PATH_TAINT_AMBIGUOUS_REF in observed
            examined_only = FORMAL_EXAMINED_ONLY_REF in observed
            if uses_simulation and simulation_is_ineligible:
                status = "representation_debt"
                rationale = (
                    "The working contract marks simulation evidence ineligible "
                    "for source-level attribution; the False result is retained "
                    "but cannot become a confirmed issue."
                )
            elif path_ambiguous:
                status = "unattributed"
                rationale = (
                    "The fired-transition derivation is not unique and the "
                    "candidates disagree on path taint, so an unresolved segment "
                    "may touch compiler-owned elements."
                )
            elif examined_only:
                status = "unattributed"
                rationale = (
                    "The bounded model-checking answer rests on the absence of a "
                    "counterexample within the bound, which examines the named "
                    "elements without exhibiting a defective trace."
                )
            elif debt_refs:
                status = "representation_debt"
                rationale = "Assertion evidence touches compiler-owned or lowering-excluded elements."
            elif safe_entries and refs:
                status = "safe"
                rationale = "False assertion evidence is bound to source-owned elements by frozen trace entries."
            else:
                status = "unattributed"
                rationale = "No attribution-safe frozen source trace entry covers the assertion evidence."
            bindings.append(
                AttributionBinding(
                    assertion_id=result.assertion_id,
                    requirement_id=result.requirement_id,
                    status=cast(Any, status),
                    source_refs=refs,
                    trace_entry_ids=matched_ids,
                    exclusion_refs=debt_refs,
                    source_level_claim_allowed=status == "safe",
                    rationale=rationale,
                )
            )
        projection = AttributionProjection(bindings=tuple(bindings))
        record = _record_node(
            state,
            node_name="bind_attribution",
            revision=0,
            kind="deterministic",
            input_value=released,
            output_value=projection,
            started_at=started_at,
            start_ns=start_ns,
        )
        return {
            "attribution_projection": projection,
            "node_execution_records": _append_records(state, record),
        }
    except Exception as exc:
        return _fail_state(
            state,
            "bind_attribution",
            exc,
            started_at=started_at,
            start_ns=start_ns,
            input_value=state.get("released_assertion_results"),
        )


def _flatten_strings(value: Any) -> tuple[str, ...]:
    values: list[str] = []
    if isinstance(value, str):
        values.append(value)
    elif isinstance(value, dict):
        for item in value.values():
            values.extend(_flatten_strings(item))
    elif isinstance(value, (list, tuple, set)):
        for item in value:
            values.extend(_flatten_strings(item))
    return tuple(values)


def _working_contract_simulation_is_ineligible(contract: dict[str, Any]) -> bool:
    """Return whether the frozen contract explicitly excludes simulation attribution.

    The representation contract is intentionally treated as capability metadata,
    not as a source of expected issues.  Only an explicit ``ineligible`` status
    blocks promotion; missing or ``not_run`` metadata must not silently change
    the existing source-trace policy.
    """

    capability_eligibility = contract.get("capability_eligibility", {})
    if isinstance(capability_eligibility, dict):
        simulation = capability_eligibility.get("simulation", {})
        if isinstance(simulation, dict) and simulation.get("status") == "ineligible":
            return True
    summary = contract.get("summary", {})
    return (
        isinstance(summary, dict) and summary.get("simulation_status") == "ineligible"
    )


def _reference_matches_observed(reference: str, observed: set[str]) -> bool:
    """Delegate to the single shared matcher; see ``common.refs``."""

    return reference_matches(reference, observed)


def _trace_entry_matches(entry: Any, observed: set[str]) -> bool:
    if not isinstance(entry, dict):
        return False
    refs = entry.get("intermediate_elements", [])
    return isinstance(refs, list) and any(
        _reference_matches_observed(str(ref), observed) for ref in refs
    )


def adjudicate_results(
    state: DiscoverGraphState, responder: StructuredResponder
) -> DiscoverGraphState:
    started_at, start_ns = _now(), time.perf_counter_ns()
    try:
        requirements = state["requirement_set"]
        script = state["assertion_script"]
        released = state["released_assertion_results"]
        attribution = state["attribution_projection"]
        # Pydantic already enforces strict bool in ReleasedAssertionResults/AssertionResult.
        # The frozen model text, so a claimed shared element can be checked rather than
        # taken on the adjudicator's word.  It cannot widen this role's authority: the set
        # of issues is closed against the released results below, so the only thing the
        # model text can change is how they are grouped and worded.
        frozen = state.get("frozen_inputs")
        payload = renderer.render_adjudicator_input(
            requirements,
            script,
            released,
            attribution,
            state.get("coverage_gaps", ()),
            stm_text=frozen.stm_text if frozen is not None else "",
        )
        output = responder.invoke_structured(
            role="result_adjudicator",
            schema=DiscoverAdjudication,
            system_prompt=prompts.RESULT_ADJUDICATOR_PROMPT,
            user_input=payload,
        )
        assertion_by_id = {
            assertion.assertion_id: assertion for assertion in script.assertions
        }
        # A `precondition` may become an issue too (issue #170 §11.4): a missing
        # model element is a real defect, and it is the *only* thing reportable
        # when the primary that needed it was blocked.  Excluding it here would
        # reinstate the loss §11.2 removes -- the finding would exist in the
        # execution record and never reach the issue list.
        primary_assertion_ids = {
            assertion.assertion_id
            for assertion in script.assertions
            if (assertion.role or "primary") in {"primary", "precondition"}
        }
        false_assertions = {
            r.assertion_id for r in released.results if r.truth_value is False
        }
        false_primary_assertions = false_assertions & primary_assertion_ids
        supporting_false_assertions = false_assertions - primary_assertion_ids
        safe_assertions = {
            binding.assertion_id
            for binding in attribution.bindings
            if binding.status == "safe"
        }
        binding_by_assertion = {
            binding.assertion_id: binding for binding in attribution.bindings
        }
        requirement_by_assertion = {
            assertion.assertion_id: assertion.requirement_id
            for assertion in script.assertions
        }
        false_by_assertion = {
            result.assertion_id: result
            for result in released.results
            if result.truth_value is False
        }
        safe_false_assertions = false_primary_assertions & safe_assertions
        unsafe_false_assertions = false_primary_assertions - safe_false_assertions
        normalized_issues = []
        annotated_citations: list[dict[str, Any]] = []
        for issue in output.issues:
            primary_ids = tuple(
                assertion_id
                for assertion_id in issue.assertion_ids
                if assertion_id in primary_assertion_ids
            )
            if primary_ids:
                update: dict[str, Any] = {"assertion_ids": primary_ids}
                dropped = tuple(
                    assertion_id
                    for assertion_id in issue.assertion_ids
                    if assertion_id not in primary_assertion_ids
                )
                # The trim above is right -- supporting evidence cannot create an issue --
                # but on its own it leaves the rationale citing an id the record no longer
                # lists, which is what pair 0029's REQ-012 published. Annotating in place
                # keeps the sentence readable and tells the auditor what became of the
                # citation; deleting the id would hide that anything was removed.
                cited = tuple(
                    assertion_id
                    for assertion_id in dropped
                    if assertion_id in issue.rationale
                )
                if cited:
                    rationale = issue.rationale
                    for assertion_id in cited:
                        rationale = rationale.replace(
                            assertion_id,
                            f"{assertion_id} [supporting evidence; removed from this "
                            f"issue's assertion_ids and recorded as an observation]",
                        )
                    update["rationale"] = rationale
                    annotated_citations.append(
                        {"issue_id": issue.issue_id, "assertion_ids": cited}
                    )
                normalized_issues.append(issue.model_copy(update=update))
        normalized_excluded = []
        for finding in output.excluded_findings:
            primary_ids = tuple(
                assertion_id
                for assertion_id in finding.assertion_ids
                if assertion_id in primary_assertion_ids
            )
            if primary_ids:
                normalized_excluded.append(
                    finding.model_copy(update={"assertion_ids": primary_ids})
                )
        supporting_observations = tuple(
            ExcludedObservation(
                assertion_id=assertion_id,
                requirement_id=assertion_by_id[assertion_id].requirement_id,
                role="supporting",
                disposition="supporting_false",
                rationale=(
                    "Supporting evidence evaluated False. It is retained for "
                    "diagnosis but cannot create a Repair issue."
                ),
            )
            for assertion_id in sorted(supporting_false_assertions)
        )
        # Which basket a primary False belongs in follows from its attribution status, which
        # is already known here -- so a finding filed in the wrong one is a clerical error,
        # not a disagreement about evidence.  Rejecting the whole response over it discarded
        # a complete run of `0029-gpt` that had the right findings in it, and this node has
        # no contract-feedback retry to soften that.  The move is recorded, never silent.
        misfiled_moves: list[dict[str, Any]] = []
        kept_issues, kept_excluded = [], []

        def _derived_status(finding: AdjudicatedIssue) -> str | None:
            """The status the bindings support, ignoring what the finding claims.

            Sorting on the model's own `attribution_status` would only repair half of what
            goes wrong, because the label and the basket fail together: a model that thinks a
            finding is unattributed both says so and files it as an exclusion. Pair 0029
            happened to get the label right and the basket wrong, but the mirror case -- right
            basket, wrong label -- dies just as hard on `excluded finding attribution_status
            must match its bindings`, and a mislabelled *merged* issue dies on the
            single-requirement rule for exclusions after being moved.

            `None` means the cited assertions disagree with each other. That is not a filing
            error and nothing here can repair it, so it falls through to the checks below.
            """
            statuses = {
                binding_by_assertion[assertion_id].status
                for assertion_id in finding.assertion_ids
                if assertion_id in binding_by_assertion
            }
            return statuses.pop() if len(statuses) == 1 else None

        for finding, origin in (
            *((f, "issues") for f in normalized_issues),
            *((f, "excluded_findings") for f in normalized_excluded),
        ):
            derived = _derived_status(finding)
            target = "issues" if derived == "safe" else "excluded_findings"
            if derived is None:
                # Mixed bindings: leave it where the model put it and let the closure checks
                # below reject it, rather than guessing at a basket.
                target = origin
            relabelled = (
                finding
                if derived is None or derived == finding.attribution_status
                else finding.model_copy(update={"attribution_status": derived})
            )
            if target != origin or relabelled is not finding:
                misfiled_moves.append(
                    {
                        "issue_id": finding.issue_id,
                        "from": origin,
                        "to": target,
                        "reported_status": finding.attribution_status,
                        "binding_status": derived,
                    }
                )
            if target == "issues":
                if origin == "excluded_findings":
                    # The prose was written to explain an exclusion; published as a confirmed
                    # issue it would read as if the adjudicator had argued for it.
                    relabelled = relabelled.model_copy(
                        update={
                            "rationale": (
                                relabelled.rationale
                                + " [relocated from excluded_findings by the deterministic "
                                "layer: the attribution binding for its assertions is safe]"
                            )
                        }
                    )
                kept_issues.append(relabelled)
            else:
                kept_excluded.append(relabelled)
        output = output.model_copy(
            update={
                "issues": tuple(kept_issues),
                "excluded_findings": tuple(kept_excluded),
                # This projection is derived from released execution truth, not
                # copied from the semantic adjudicator.  A model-written True
                # observation must never be relabelled as supporting_false.
                "excluded_observations": supporting_observations,
                "has_confirmed_issues": bool(kept_issues),
            }
        )
        # A merge whose only shared element is one both Requirements happen to bind to is the
        # shape the one questionable grouping in three rounds took: `state_declared(X,
        # composite)` merged with `cardinality(X, 3)` under the single element `X`. Binding to
        # the same state is not the same defect. It is recorded rather than rejected because a
        # genuine one-element merge exists and this layer cannot tell them apart.
        thin_merge_warnings = tuple(
            {
                "issue_id": issue.issue_id,
                "requirement_ids": issue.requirement_ids,
                "shared_elements": issue.shared_elements,
                "reason": (
                    "a merge across requirements rests on a single shared element; "
                    "check that it names the defect rather than a common binding"
                ),
            }
            for issue in output.issues
            if len(issue.requirement_ids) > 1 and len(issue.shared_elements) == 1
        )
        issue_assertions: set[str] = set()
        excluded_assertions: set[str] = set()
        for issue in output.issues:
            issue_ids = set(issue.assertion_ids)
            if not issue_ids.issubset(false_primary_assertions):
                raise ValueError(
                    "adjudicated issues may only reference primary False assertions"
                )
            # `attribution_status` is no longer checked here -- the sort above guarantees
            # it. What remains is the part no relocation can fix: a finding whose *cited
            # assertions* are not attribution-safe is making a claim the attribution layer
            # refused, and moving it would not change that.
            if not issue_ids.issubset(safe_assertions):
                raise ValueError(
                    "confirmed issues may only reference attribution-safe False assertions"
                )
            if issue_ids & issue_assertions:
                raise ValueError("confirmed issue assertion groups must be disjoint")
            issue_assertions.update(issue_ids)
            expected_requirements = {
                requirement_by_assertion[assertion_id] for assertion_id in issue_ids
            }
            # Equality, not membership: a group that drops a Requirement whose assertion it
            # references, or claims one it does not, is not describing the evidence it cites.
            if set(issue.requirement_ids) != expected_requirements:
                raise ValueError(
                    "confirmed issue requirement_ids must equal the requirements of all "
                    "referenced assertions"
                )
            if len(expected_requirements) > 1:
                # Grouping across Requirements lowers the reported defect count, so it has
                # to be argued rather than asserted.  Without these the adjudicator could
                # emit one issue over every False assertion and nothing downstream would
                # be able to tell that apart from a genuine single root cause.
                if not issue.shared_root_cause:
                    raise ValueError(
                        "an issue spanning multiple requirements must state its "
                        "shared_root_cause"
                    )
                if not issue.shared_elements:
                    raise ValueError(
                        "an issue spanning multiple requirements must name its "
                        "shared_elements"
                    )
        for excluded in output.excluded_findings:
            excluded_ids = set(excluded.assertion_ids)
            if not excluded_ids.issubset(false_primary_assertions):
                raise ValueError(
                    "excluded findings may only reference primary False assertions"
                )
            # Likewise settled by the sort above; a safe finding reaching this branch would
            # be a bug in that sort rather than a response to reject.
            assert excluded.attribution_status != "safe"
            if excluded_ids & excluded_assertions:
                raise ValueError("excluded finding assertion groups must be disjoint")
            excluded_assertions.update(excluded_ids)
            expected_requirements = {
                requirement_by_assertion[assertion_id] for assertion_id in excluded_ids
            }
            # Exclusions stay one Requirement each.  They record evidence that could not be
            # attributed, so grouping them buys no accuracy in the defect count -- the only
            # thing it changes is how hard the record is to trace back to its Requirement.
            if (
                len(expected_requirements) != 1
                or set(excluded.requirement_ids) != expected_requirements
            ):
                raise ValueError(
                    "excluded finding requirement_ids must be the single requirement of "
                    "all referenced assertions"
                )
            expected_statuses = {
                binding_by_assertion[assertion_id].status
                for assertion_id in excluded_ids
            }
            if (
                len(expected_statuses) != 1
                or excluded.attribution_status not in expected_statuses
            ):
                raise ValueError(
                    "excluded finding attribution_status must match its bindings"
                )
        if issue_assertions != safe_false_assertions:
            raise ValueError(
                "adjudication must account for every attribution-safe False assertion"
            )
        if excluded_assertions != unsafe_false_assertions:
            raise ValueError(
                "adjudication must account for every non-safe False assertion"
            )
        result_by_requirement: dict[str, list[bool]] = {}
        for result in released.results:
            # `precondition` counts toward satisfaction: a requirement whose
            # premise failed is not satisfied, whatever happened to the primary
            # (which will have been blocked).  `supporting` still does not --
            # it is corroboration, and a False there is normal.
            if result.role not in {"primary", "precondition"}:
                continue
            result_by_requirement.setdefault(result.requirement_id, []).append(
                result.truth_value
            )
        blocking_gap_requirements = {
            gap.requirement_id
            for gap in state.get("coverage_gaps", ())
            if gap.blocks_full_coverage and gap.requirement_id is not None
        }
        # A blocked assertion produces no sealed result, so aggregation alone
        # cannot see it -- and a requirement whose only primary was blocked would
        # aggregate over an empty list and, for `any`, come out satisfied.  Every
        # assertion must be *explicitly* satisfied (§11.5), so treat a blocked one
        # as disqualifying its requirement.
        public_check = state.get("assertion_check_public")
        blocked_requirements = {
            execution.requirement_id
            for execution in (public_check.executions if public_check else ())
            if execution.status == "blocked"
        }
        requirement_by_id = {
            requirement.requirement_id: requirement
            for requirement in requirements.requirements
        }
        expected_satisfied = {
            requirement_id
            for requirement_id, values in result_by_requirement.items()
            if requirement_id not in blocking_gap_requirements
            and requirement_id not in blocked_requirements
            and _requirement_primary_truth(requirement_by_id[requirement_id], values)
        }
        reported_satisfied = set(output.satisfied_requirement_ids)
        reconciliation = {
            # Rewriting a published rationale, however narrowly, has to be visible. Without
            # this entry the annotation would itself be an untraceable edit to the artefact.
            "rationale_citations_annotated": tuple(annotated_citations),
            # Relocating a finding changes which basket a reader finds it in, so the move has
            # to be as visible as the finding itself.
            "misfiled_findings_moved": tuple(misfiled_moves),
            "thin_merge_warnings": thin_merge_warnings,
            "normalization_applied": reported_satisfied != expected_satisfied,
            "reported_satisfied_requirement_ids": tuple(sorted(reported_satisfied)),
            "deterministic_satisfied_requirement_ids": tuple(
                sorted(expected_satisfied)
            ),
            "basis": (
                "released primary assertion results aggregated by frozen "
                "coverage_obligation; blocking gaps excluded"
            ),
        }
        if reported_satisfied != expected_satisfied:
            # This field is a deterministic ledger projection, not a semantic
            # judgment.  Keep the LLM's issue/exclusion decisions strict, but
            # do not discard an otherwise complete adjudication because the
            # model copied a requirement with a False assertion into this
            # derived list.
            output = output.model_copy(
                update={"satisfied_requirement_ids": tuple(sorted(expected_satisfied))}
            )
        record = _record_node(
            state,
            node_name="adjudicate_results",
            revision=0,
            kind="llm",
            input_value=payload,
            output_value=output,
            started_at=started_at,
            start_ns=start_ns,
        )
        llm_record = _llm_call_record(
            state,
            responder=responder,
            node_record=record,
            role="result_adjudicator",
            revision=script.revision,
            system_prompt=prompts.RESULT_ADJUDICATOR_PROMPT,
            user_prompt=payload,
            output=output,
        )
        return {
            "adjudication": output,
            "_adjudication_reconciliation": reconciliation,
            "node_execution_records": _append_records(state, record),
            "llm_call_records": [*state.get("llm_call_records", []), llm_record],
        }
    except Exception as exc:
        return _fail_state(
            state,
            "adjudicate_results",
            exc,
            started_at=started_at,
            start_ns=start_ns,
            input_value=locals().get("payload", state),
            revision=state.get("assertion_script").revision
            if state.get("assertion_script")
            else 0,
            kind="llm",
            responder=responder,
            role="result_adjudicator",
        )


def publish(state: DiscoverGraphState) -> DiscoverGraphState:
    started_at, start_ns = _now(), time.perf_counter_ns()
    try:
        frozen = state["frozen_inputs"]
        requirements = state["requirement_set"]
        script = state["assertion_script"]
        released = state["released_assertion_results"]
        adjudication = state["adjudication"]
        coverage_gaps = state.get("coverage_gaps", ())
        coverage_status = (
            "partial"
            if any(gap.blocks_full_coverage for gap in coverage_gaps)
            else "full"
        )
        guards = tuple(
            f"{result.assertion_id}:{result.truth_value}" for result in released.results
        )
        from .report import telemetry_summary

        completed = DiscoverCompleted(
            run_id=frozen.run_id,
            input_hashes=frozen.input_hashes,
            requirement_set_hash=sha256_data(requirements),
            assertion_script_hash=sha256_data(script),
            released_results_hash=sha256_data(released),
            adjudication=adjudication,
            issues=adjudication.issues,
            coverage_status=cast(Any, coverage_status),
            coverage_gaps=coverage_gaps,
            satisfied_requirement_ids=adjudication.satisfied_requirement_ids,
            excluded_findings=adjudication.excluded_findings,
            excluded_observations=adjudication.excluded_observations,
            adjudication_reconciliation=state.get("_adjudication_reconciliation", {}),
            regression_guards=guards,
            telemetry_summary=telemetry_summary(
                state.get("node_execution_records", []),
                state.get("llm_call_records", []),
            ),
            content_language=cast(Any, frozen.language),
        )
        record = _record_node(
            state,
            node_name="publish",
            revision=0,
            kind="deterministic",
            input_value=adjudication,
            output_value=completed,
            started_at=started_at,
            start_ns=start_ns,
        )
        return {
            "final_output": completed,
            "node_execution_records": _append_records(state, record),
        }
    except Exception as exc:
        return _fail_state(
            state,
            "publish",
            exc,
            started_at=started_at,
            start_ns=start_ns,
            input_value=state.get("adjudication"),
        )


def _fake_state(payload: str) -> str:
    """Pick a declared state path out of the rendered payload.

    The fake used to assert `len(states()) > 0`, which was model-agnostic.  No
    predicate is: they all name real elements.  So the fake has to read one out
    of the vocabulary it was handed, or the smoke path asserts about a state
    that does not exist and the run dies in the repair loop.
    """

    try:
        vocabulary = json.loads(payload).get("declared_model_vocabulary") or {}
        states = vocabulary.get("states") or []
    except Exception:
        states = []
    return str(states[0]) if states else "Root"


def default_fake_responder(
    role: str, schema: type[BaseModel], _system_prompt: str, _user_input: str
) -> BaseModel:
    if schema is RequirementSet:
        return RequirementSet(
            revision=1,
            requirements=(
                {
                    "requirement_id": "REQ-001",
                    "statement": "The STM must satisfy the supplied natural-language requirement.",
                    "source_segment_ids": ("NL-L001",),
                    "verification_kind": "structure",
                    "coverage_obligation": {
                        "domain": "model",
                        "aggregation": "all",
                    },
                },
            ),
            segment_disposition={"NL-L001": "covered"},
        )
    if schema is RequirementReview:
        return RequirementReview(
            decision="accept",
            reviewed_revision=1,
            rationale="The requirement set is faithful enough for the fake smoke path.",
        )
    if schema is AssertionScript:
        return AssertionScript(
            revision=1,
            assertions=(
                {
                    "assertion_id": "AST-REQ-001-01",
                    "requirement_id": "REQ-001",
                    "description": "Fake smoke assertion.",
                    "expression": (
                        f'state_declared(state="{_fake_state(_user_input)}", kind="any")'
                    ),
                    "failure_message": "[REQ-001][AST-REQ-001-01] The frozen STM exposes no state.",
                    "evidence_family": "structure",
                    "role": "primary",
                    "coverage_key": "model:states",
                    "aggregation_group": "REQ-001:all",
                },
            ),
            requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
        )
    if schema is AssertionReview:
        # The graph validates the actual hash after this response; fake graph runner patches this in graph.py.
        return AssertionReview(
            decision="accept",
            reviewed_script_hash="TO_BE_PATCHED",
            rationale="The assertion is executable and maps to the requirement.",
        )
    if schema is DiscoverAdjudication:
        return DiscoverAdjudication(
            has_confirmed_issues=False,
            satisfied_requirement_ids=("REQ-001",),
            rationale="All executable assertions passed in the fake smoke path.",
        )
    raise TypeError(f"unsupported fake schema {schema}")


def deterministic_adjudication_from_results(
    state: DiscoverGraphState,
) -> DiscoverAdjudication:
    released = state["released_assertion_results"]
    bindings = {
        binding.assertion_id: binding
        for binding in state["attribution_projection"].bindings
    }
    issues: list[AdjudicatedIssue] = []
    excluded: list[AdjudicatedIssue] = []
    for result in released.results:
        if result.truth_value:
            continue
        binding = bindings.get(result.assertion_id)
        status = binding.status if binding else "unattributed"
        finding = AdjudicatedIssue(
            issue_id=f"ISSUE-{result.requirement_id.removeprefix('REQ-')}",
            requirement_ids=(result.requirement_id,),
            assertion_ids=(result.assertion_id,),
            title=f"Requirement {result.requirement_id} is not satisfied",
            rationale="The released strict bool assertion result is False.",
            attribution_status=status,
        )
        # Only attribution-safe False results may be confirmed issues. The schema used to
        # reject a violation here; it no longer does, because rejecting at parse time is
        # fatal to a node that has no retry. The routing is written in rather than left to
        # a check that has since moved to `adjudicate_results`.
        (issues if status == "safe" else excluded).append(finding)
    return DiscoverAdjudication(
        has_confirmed_issues=bool(issues),
        issues=tuple(issues),
        excluded_findings=tuple(excluded),
        rationale="Deterministic fake adjudication over released bool results.",
    )
