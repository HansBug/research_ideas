from __future__ import annotations

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

from . import prompts, renderer
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
    LLMCallRecord,
    NodeExecutionRecord,
    ReleasedAssertionResults,
    RequirementCoverageProjection,
    RequirementReview,
    RequirementSet,
    RevisionFeedback,
    RunFailure,
    SealedAssertionReceipt,
)
from .utils import sha256_data, sha256_text

T = TypeVar("T", bound=BaseModel)


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
            len(output.model_dump_json()) if observation.parsed_output is not None else None
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
                    cache_creation_input_tokens=usage.get("cache_creation_input_tokens"),
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


def _fallback_prepare(discover_input: DiscoverInput) -> FrozenDiscoverInputs:
    inspected = check_fcstm(discover_input.stm_text, "<discover-input>")
    if not inspected.get("executable"):
        raise ValueError(f"FCSTM input is not executable: {inspected.get('error') or inspected.get('diagnostics')}")
    source_entries = discover_input.source_trace.get("entries", [])
    source_entries = source_entries if isinstance(source_entries, list) else []
    environment = build_eval_environment(
        model_text=discover_input.stm_text,
        inspect=inspected.get("inspect"),
        source_mappings=source_entries,
    )
    segments = {
        f"NL-L{index:03d}": line.strip()
        for index, line in enumerate(discover_input.natural_language.splitlines(), start=1)
        if line.strip()
    } or {"NL-ALL": discover_input.natural_language.strip()}
    return FrozenDiscoverInputs(
        run_id=discover_input.run_id,
        natural_language=discover_input.natural_language,
        stm_text=discover_input.stm_text,
        nl_segments=segments,
        inspect_digest={
            "parse_status": inspected.get("parse_status"),
            "semantic_status": inspected.get("semantic_status"),
            "inspect_status": inspected.get("inspect_status"),
            "diagnostics": inspected.get("diagnostics", []),
            "metrics": inspected.get("metrics", {}),
            "model_type": inspected.get("model_type"),
        },
        source_trace=discover_input.source_trace,
        working_contract=discover_input.manifest.get("working_contract", {})
        if isinstance(discover_input.manifest.get("working_contract"), dict)
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
        payload = renderer.render_requirement_split_input(frozen, current, feedback)
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
        fingerprint = sha256_data(
            output.model_dump(mode="json", exclude={"revision"})
        )
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
        coverage = RequirementCoverageProjection(
            covered_requirement_ids=tuple(
                req.requirement_id for req in output.requirements
            ),
            missing_segment_ids=tuple(
                sorted(
                    set(frozen.nl_segments)
                    - set(output.segment_disposition)
                )
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
        return {
            "requirement_set": output,
            "requirement_coverage": coverage,
            "requirement_fingerprints": (
                *state.get("requirement_fingerprints", ()),
                fingerprint,
            ),
            "node_execution_records": _append_records(state, record),
            "llm_call_records": [*state.get("llm_call_records", []), llm_record],
        }
    except Exception as exc:
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
        if output.decision == "revise":
            update["_requirement_feedback"] = RevisionFeedback(
                target="requirements",
                reason=output.rationale,
                findings=tuple(f.message for f in output.findings),
            )
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
            frozen, requirements, current, feedback
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
        fingerprint = sha256_data(
            output.model_dump(mode="json", exclude={"revision"})
        )
        if fingerprint in state.get("assertion_fingerprints", ()):
            raise ValueError(
                "no-progress gate rejected repeated AssertionScript semantics"
            )
        req_ids = {r.requirement_id for r in requirements.requirements}
        assertion_ids = {item.assertion_id for item in output.assertions}
        mapped_by_assertions: dict[str, set[str]] = {req_id: set() for req_id in req_ids}
        for assertion in output.assertions:
            if assertion.requirement_id not in req_ids:
                raise ValueError(
                    f"assertion {assertion.assertion_id} maps to unknown requirement"
                )
            expected_prefix = (
                f"[{assertion.requirement_id}][{assertion.assertion_id}]"
            )
            if not assertion.failure_message.startswith(expected_prefix):
                raise ValueError(
                    f"assertion {assertion.assertion_id} failure_message must start with {expected_prefix}"
                )
            mapped_by_assertions[assertion.requirement_id].add(assertion.assertion_id)
        assertions_by_id = {item.assertion_id: item for item in output.assertions}
        for requirement in requirements.requirements:
            if requirement.checkability != "effect":
                continue
            evidence_families = {
                assertions_by_id[assertion_id].evidence_family
                for assertion_id in mapped_by_assertions[requirement.requirement_id]
            }
            if not evidence_families.intersection({"simulation", "fbmcq"}):
                raise ValueError(
                    f"effect requirement {requirement.requirement_id} requires "
                    "at least one simulation or fbmcq assertion; relation-only evidence "
                    "is complementary, not sufficient"
                )
        if any(not ids for ids in mapped_by_assertions.values()):
            missing = sorted(req_id for req_id, ids in mapped_by_assertions.items() if not ids)
            raise ValueError(f"every requirement needs an assertion; missing: {missing}")
        if set(output.requirement_mapping) != req_ids:
            raise ValueError("requirement_mapping keys must exactly match RequirementSet ids")
        for req_id, mapped_ids in output.requirement_mapping.items():
            if set(mapped_ids) != mapped_by_assertions[req_id]:
                raise ValueError(
                    f"requirement_mapping for {req_id} does not match assertion ownership"
                )
            if not set(mapped_ids).issubset(assertion_ids):
                raise ValueError(f"requirement_mapping for {req_id} references unknown assertion")
        record = _record_node(
            state,
            node_name="convert_assertions",
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
            role="assertion_converter",
            revision=output.revision,
            system_prompt=prompts.ASSERTION_CONVERTER_PROMPT,
            user_prompt=payload,
            output=output,
        )
        return {
            "assertion_script": output,
            "assertion_fingerprints": (
                *state.get("assertion_fingerprints", ()),
                fingerprint,
            ),
            "_assertion_conversion_contract_feedback": None,
            "_assertion_contract_repair_count": 0,
            "node_execution_records": _append_records(state, record),
            "llm_call_records": [*state.get("llm_call_records", []), llm_record],
        }
    except Exception as exc:
        message = f"{type(exc).__name__}: {exc}"
        repair_count = state.get("_assertion_contract_repair_count", 0)
        can_revise_contract = (
            output is not None
            and "no-progress gate" not in message
            and repair_count < 3
        )
        if can_revise_contract:
            contract_feedback = RevisionFeedback(
                target="assertions",
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
        checker = assertion_checker or AssertionChecker(
            build_eval_environment(
                model_text=frozen.stm_text,
                source_mappings=source_entries,
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
            assertion_families_by_requirement.setdefault(item.requirement_id, set()).add(
                item.evidence_family
            )
        for assertion in script.assertions:
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
                and requirement.checkability == "effect"
                and assertion.evidence_family == "simulation"
                and "fbmcq"
                not in assertion_families_by_requirement.get(assertion.requirement_id, set())
            ):
                has_hot_start = any(
                    call.function == "simulate"
                    and call.kwargs.get("initial_state") is not None
                    for call in checked.function_call_trace
                )
                has_explicit_initial_cold_path = any(
                    call.function == "simulate"
                    and call.kwargs.get("initial_state") is None
                    and isinstance(call.kwargs.get("cycles"), list)
                    and bool(call.kwargs["cycles"])
                    and call.kwargs["cycles"][0] == []
                    and any(bool(cycle) for cycle in call.kwargs["cycles"][1:])
                    for call in checked.function_call_trace
                )
                if not has_hot_start and not has_explicit_initial_cold_path:
                    hot_start_policy_error = (
                        "effect requirement simulation must use an explicit hot-start "
                        "initial_state, or an explicit initialization cold path "
                        "cycles=[[], [causal_event]]; otherwise include a bounded "
                        "fbmcq assertion. A cold-start trace without an explicit empty "
                        "initialization cycle is not sufficient behavior evidence"
                    )
            if (
                requirement is not None
                and requirement.checkability == "effect"
                and assertion.evidence_family == "fbmcq"
            ):
                formal_calls = [
                    call
                    for call in checked.function_call_trace
                    if call.function == "fbmcq" and call.status == "completed"
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
                        "effect requirement FBMCQ evidence must connect the bounded "
                        "property to an explicit event/condition or initialization; "
                        "a bare reach target is not causal evidence. Replace it with "
                        "a response query such as `check response <= 5: trigger "
                        "event(\"Root.Go\", current) -> within 3 active(\"Root.Done\");`, "
                        "a positive event assumption plus reach, an explicit `init "
                        "state(\"Root.Idle\");` query, or a hot-start simulation. "
                        + " ".join(details)
                    )
            if (
                hot_start_policy_error is None
                and formal_causality_error is None
                and checked.outcome in {"valid", "sealed_false"}
                and type(checked.value) is bool
            ):
                public_executions.append(
                    AssertionExecutionPublic(
                        assertion_id=assertion.assertion_id,
                        requirement_id=assertion.requirement_id,
                        status="executable",
                    )
                )
                sealed_results.append(
                    AssertionResult(
                        assertion_id=assertion.assertion_id,
                        requirement_id=assertion.requirement_id,
                        truth_value=checked.value,
                        script_hash=script_hash,
                        tool_env_hash=frozen.tool_env_hash,
                        evidence_family=assertion.evidence_family,
                        failure_message=(
                            assertion.failure_message if checked.value is False else None
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
                        "Rewrite every simulation call for this effect requirement "
                        "as an explicit hot start with initial_state=<exact state "
                        "path> and initial_vars={<exact declaration name>: value}; "
                        "use declaration names, not qualified state-machine paths, "
                        "and put the causal event in cycle 0. For an initialization "
                        "claim, an explicit cold path cycles=[[], [causal_event]] is "
                        "also valid. Alternatively replace it with a causal bounded "
                        "FBMCQ query. The full assertion must then execute without "
                        "exception and return strict bool."
                    )
                elif formal_causality_error is not None:
                    if "parse failed" in str(formal_causality_error):
                        pass_criterion = (
                            "Use only the documented FBMCQ grammar. Replace the "
                            "parse-invalid query with a syntactically valid causal "
                            "query, preferably `init state(\"Root.Idle\"); check "
                            "reach <= 5: active(\"Root.Done\");`, or use an explicit "
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
                elif (
                    isinstance(detail.get("error"), dict)
                    and detail["error"].get("type") == "NameError"
                ):
                    pass_criterion = (
                        "Replace every undefined Python name with a quoted complete "
                        "state/event path, or define the alias in the same shared "
                        "prefix; then the full prefix plus this assertion must "
                        "execute without exception and return strict bool using "
                        "the declared evidence family."
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
        }
        if status == "invalid":
            invalid_signature = sha256_data(
                tuple(
                    sorted(
                        (item.assertion_id, item.error or "")
                        for item in public.executions
                        if item.status == "invalid"
                    )
                )
            )
            previous_signatures = state.get("_assertion_invalid_signatures", ())
            update["_assertion_invalid_signatures"] = (
                *previous_signatures,
                invalid_signature,
            )
            update["_assertion_feedback"] = RevisionFeedback(
                target="assertions",
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
            )
        record = _record_node(
            state,
            node_name="precheck_and_seal",
            revision=script.revision,
            kind="deterministic",
            input_value={"script_hash": script_hash},
            output_value=public,
            started_at=started_at,
            start_ns=start_ns,
        )
        if status == "invalid" and invalid_signature in previous_signatures:
            message = (
                "no-progress gate: the same assertion invalid-signature was observed "
                "again; stopping instead of repeating an unchanged revision request"
            )
            failure = RunFailure(
                run_id=_run_id(state), node_name="precheck_and_seal", message=message
            )
            failed_record = _record_node(
                state,
                node_name="precheck_and_seal",
                revision=script.revision,
                kind="deterministic",
                input_value={
                    "script_hash": script_hash,
                    "invalid_signature": invalid_signature,
                },
                output_value=public,
                started_at=started_at,
                start_ns=start_ns,
                failure=message,
            )
            update["failure"] = failure
            update["node_execution_records"] = _append_records(
                state, failed_record
            )
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
    state: DiscoverGraphState, responder: StructuredResponder
) -> DiscoverGraphState:
    started_at, start_ns = _now(), time.perf_counter_ns()
    try:
        frozen = state["frozen_inputs"]
        requirements = state["requirement_set"]
        script = state["assertion_script"]
        public_check = state["assertion_check_public"]
        payload = renderer.render_assertion_review_input(
            frozen, requirements, script, public_check
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
        if output.reviewed_script_hash != script_hash:
            raise ValueError(
                "AssertionReview reviewed_script_hash must match current script"
            )
        update: DiscoverGraphState = {"assertion_review": output}
        if output.decision == "revise":
            update["_assertion_feedback"] = RevisionFeedback(
                target="assertions",
                reason=output.rationale,
                findings=tuple(f.message for f in output.findings),
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
        bindings = []
        for result in released.results:
            if result.truth_value:
                continue
            observed = set(_flatten_strings(result.check_detail.get("function_call_trace", [])))
            matched = [entry for entry in entries if _trace_entry_matches(entry, observed)]
            matched_ids = tuple(
                str(entry.get("trace_id"))
                for entry in matched
                if entry.get("trace_id")
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
                sorted(ref for ref in exclusions if _reference_matches_observed(str(ref), observed))
            )
            safe_entries = [
                entry
                for entry in matched
                if isinstance(entry.get("attribution_boundary"), dict)
                and entry["attribution_boundary"].get("source_level_claim_allowed") is True
                and entry["attribution_boundary"].get("representation_related") is not True
                and entry["attribution_boundary"].get("conversion_or_lowering_related") is not True
            ]
            if debt_refs:
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


def _reference_matches_observed(reference: str, observed: set[str]) -> bool:
    """Match exact structured references, never leaf-name suffixes.

    Source traces may qualify a model reference with a producer namespace
    (for example ``compiler:state:Root.Done``), while assertion call traces
    usually expose the bare full path (``Root.Done``).  The kind and complete
    path are therefore normalized before comparison.  A leaf-only or suffix
    match would incorrectly bind unrelated regions such as ``Other.Idle`` or
    ``NotIdle``.
    """

    kinds = {"event", "state", "transition", "variable", "effect", "guard"}

    def identity(value: str) -> tuple[str | None, str]:
        text = value.strip()
        parts = text.split(":")
        if len(parts) >= 2 and parts[-2] in kinds:
            return parts[-2], parts[-1]
        return None, text

    ref_kind, ref_path = identity(reference)
    for value in observed:
        text = value.strip()
        if not text:
            continue
        if text == reference:
            return True
        observed_kind, observed_path = identity(text)
        if ref_kind is not None and observed_kind is not None:
            if ref_kind == observed_kind and ref_path == observed_path:
                return True
        elif ref_kind is not None and observed_kind is None:
            if ref_path == observed_path:
                return True
        elif ref_kind is None and observed_kind is not None:
            if ref_path == observed_path:
                return True
        elif ref_path == observed_path:
            return True
    return False


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
        payload = renderer.render_adjudicator_input(
            requirements, script, released, attribution
        )
        output = responder.invoke_structured(
            role="result_adjudicator",
            schema=DiscoverAdjudication,
            system_prompt=prompts.RESULT_ADJUDICATOR_PROMPT,
            user_input=payload,
        )
        false_assertions = {
            r.assertion_id for r in released.results if r.truth_value is False
        }
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
            result.assertion_id: result for result in released.results
            if result.truth_value is False
        }
        safe_false_assertions = set(false_by_assertion) & safe_assertions
        unsafe_false_assertions = set(false_by_assertion) - safe_false_assertions
        issue_assertions: set[str] = set()
        excluded_assertions: set[str] = set()
        for issue in output.issues:
            issue_ids = set(issue.assertion_ids)
            if not issue_ids.issubset(false_assertions):
                raise ValueError(
                    "adjudicated issues may only reference False assertions"
                )
            if issue.attribution_status != "safe" or not issue_ids.issubset(
                safe_assertions
            ):
                raise ValueError(
                    "confirmed issues may only reference attribution-safe False assertions"
                )
            if issue_ids & issue_assertions:
                raise ValueError("confirmed issue assertion groups must be disjoint")
            issue_assertions.update(issue_ids)
            expected_requirements = {
                requirement_by_assertion[assertion_id]
                for assertion_id in issue_ids
            }
            if issue.requirement_id not in expected_requirements or len(
                expected_requirements
            ) != 1:
                raise ValueError(
                    "confirmed issue requirement_id must match all referenced assertions"
                )
        for excluded in output.excluded_findings:
            excluded_ids = set(excluded.assertion_ids)
            if not excluded_ids.issubset(false_assertions):
                raise ValueError("excluded findings may only reference False assertions")
            if excluded.attribution_status == "safe":
                raise ValueError("excluded findings must not be attribution-safe")
            if excluded_ids & excluded_assertions:
                raise ValueError("excluded finding assertion groups must be disjoint")
            excluded_assertions.update(excluded_ids)
            expected_requirements = {
                requirement_by_assertion[assertion_id]
                for assertion_id in excluded_ids
            }
            if excluded.requirement_id not in expected_requirements or len(
                expected_requirements
            ) != 1:
                raise ValueError(
                    "excluded finding requirement_id must match all referenced assertions"
                )
            expected_statuses = {
                binding_by_assertion[assertion_id].status for assertion_id in excluded_ids
            }
            if len(expected_statuses) != 1 or excluded.attribution_status not in expected_statuses:
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
            result_by_requirement.setdefault(result.requirement_id, []).append(
                result.truth_value
            )
        expected_satisfied = {
            requirement_id
            for requirement_id, values in result_by_requirement.items()
            if all(values)
        }
        if set(output.satisfied_requirement_ids) != expected_satisfied:
            raise ValueError(
                "satisfied_requirement_ids must exactly match all-True requirements"
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
                    "checkability": "structure",
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
                    "expression": "len(states()) > 0",
                    "failure_message": "[REQ-001][AST-REQ-001-01] The frozen STM exposes no state.",
                    "evidence_family": "structure",
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
    for result in released.results:
        if result.truth_value:
            continue
        binding = bindings.get(result.assertion_id)
        status = binding.status if binding else "unattributed"
        issues.append(
            AdjudicatedIssue(
                issue_id=f"ISSUE-{result.requirement_id.removeprefix('REQ-')}",
                requirement_id=result.requirement_id,
                assertion_ids=(result.assertion_id,),
                title=f"Requirement {result.requirement_id} is not satisfied",
                rationale="The released strict bool assertion result is False.",
                attribution_status=status,
            )
        )
    return DiscoverAdjudication(
        has_confirmed_issues=bool(issues),
        issues=tuple(issues),
        rationale="Deterministic fake adjudication over released bool results.",
    )
