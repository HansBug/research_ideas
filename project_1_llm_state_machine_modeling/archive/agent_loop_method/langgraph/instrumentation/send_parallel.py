"""LG-E2 Send fan-out helpers for SD-6 scenario checking.

Raw worker order is treated as instrumentation only; canonical evidence remains
serial-equivalent and scenario-key sorted.
"""

from __future__ import annotations

import copy
import re
from collections import defaultdict
from typing import Any, TypedDict

try:
    from typing import Annotated
except ImportError:  # pragma: no cover - Python 3.10 fallback.
    from typing_extensions import Annotated

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from archive.agent_loop_method.langgraph.instrumentation.common import _hash_payload, _jsonable
from archive.agent_loop_method.langgraph.instrumentation.operator_stream import _LG_D1_ACADEMIC_EVIDENCE_SOURCES
from archive.agent_loop_method.langgraph.instrumentation.tool_wrappers import _lg_e3_fixed_tool_call
from archive.agent_loop_method.run_record import read_agent_loop_run_record, write_agent_loop_run_record
from archive.agent_loop_method.schema import AgentLoopResult, ScenarioResult, ScenarioSet, SimFeedback, StageContext, StageResultMeta
from archive.agent_loop_method.staged_runtime import FullStagedRuntimeAdapters, FullStagedRuntimeConfig, _hash_text, _meta
from archive.agent_loop_method.stages.ids import FeedbackSource, StageId, StageStatus

LG_E2_SEND_PARALLEL_SCHEMA_VERSION = "lg-e2.send-parallel-sd6.v1"

LG_E2_SEND_PARALLEL_INSTRUMENTATION_LAYER = "langgraph_send_parallel_scenario_checker"

def _lg_e2_worker_result_reducer(existing: list[dict[str, Any]] | None, new_results: Any) -> list[dict[str, Any]]:
    """Append LG-E2 Send worker results without using completion order as evidence.

    LangGraph may merge Send worker updates in runtime completion order.  LG-E2
    keeps that raw order only as instrumentation; all academic evidence is
    re-sorted later by the canonical scenario/checker key.
    """

    merged = list(existing or [])
    if new_results is None:
        return merged
    incoming = list(new_results if isinstance(new_results, list) else [new_results])
    merged.extend(item for item in incoming if isinstance(item, dict))
    return merged

class _LgE2SendState(TypedDict, total=False):
    """Internal map-reduce state for LG-E2 SD-6 scenario fan-out."""

    worker_specs: list[dict[str, Any]]
    worker_results: Annotated[list[dict[str, Any]], _lg_e2_worker_result_reducer]

_LG_E2_ORDERING_KEY_FIELDS = (
    "scenario_epoch",
    "scenario_index",
    "normalized_scenario_name",
    "checker_name",
    "input_hash",
)

def build_lg_e2_send_parallel_contract() -> dict[str, Any]:
    """Return the LG-E2 SD-6 Send fan-out contract.

    LG-E2 is an auditability/reproducibility contract, not a model-quality
    metric.  It uses LangGraph ``Send`` only for independent deterministic
    scenario workers and then reduces worker results through a canonical order
    that is independent of runtime completion order.
    """

    return {
        "schema_version": LG_E2_SEND_PARALLEL_SCHEMA_VERSION,
        "instrumentation_layer": LG_E2_SEND_PARALLEL_INSTRUMENTATION_LAYER,
        "stage_id": StageId.SD_6_SIM.value,
        "graph_node": "validation_sd6_sim",
        "send_api": "langgraph.types.Send",
        "fanout_scope": "independent deterministic SD-6 scenario simulation/checker workers",
        "ordering_key_fields": list(_LG_E2_ORDERING_KEY_FIELDS),
        "scenario_index_source": "frozen ScenarioSet.scenarios original order",
        "normalized_scenario_name_role": "tie_break_only_after_scenario_index",
        "serial_equivalence_hash_excludes": [
            "operator_event_completion_order",
            "wall_clock_timestamp",
            "provider_latency",
            "raw_prompt_or_raw_output",
        ],
        "worker_isolation": "deepcopy scenario plus isolated StageContext; shared graph state/FixLog/history are not passed to workers",
        "preflight_required": True,
        "does_not_replace_academic_evidence": True,
        "academic_evidence_sources": list(_LG_D1_ACADEMIC_EVIDENCE_SOURCES),
    }

def _lg_e2_normalized_scenario_name(name: Any) -> str:
    return re.sub(r"\s+", " ", str(name or "").strip().lower())

def _lg_e2_worker_ordering_key(worker: dict[str, Any]) -> tuple[int, int, str, str, str]:
    key = worker.get("ordering_key") if isinstance(worker.get("ordering_key"), dict) else worker
    return (
        int(key.get("scenario_epoch", 0) or 0),
        int(key.get("scenario_index", 0) or 0),
        str(key.get("normalized_scenario_name") or ""),
        str(key.get("checker_name") or ""),
        str(key.get("input_hash") or ""),
    )

def _lg_e2_canonicalize_worker_results(worker_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted([item for item in worker_results if isinstance(item, dict)], key=_lg_e2_worker_ordering_key)

def _lg_e2_feedback_scenario_results(feedback: Any) -> list[Any]:
    if isinstance(feedback, SimFeedback):
        return list(feedback.scenario_results)
    if isinstance(feedback, dict):
        return list(feedback.get("scenario_results") or [])
    return list(getattr(feedback, "scenario_results", []) or [])

def _lg_e2_scenario_result_sort_key(result: Any, scenario_index_by_name: dict[str, int]) -> tuple[int, str, str]:
    name = str(getattr(result, "name", "") or "")
    return (
        int(scenario_index_by_name.get(name, len(scenario_index_by_name) + 1)),
        _lg_e2_normalized_scenario_name(name),
        _hash_payload(result),
    )

def _lg_e2_canonicalize_scenario_results(scenario_results: list[Any], scenario_set: Any) -> list[Any]:
    scenario_index_by_name = {
        str(getattr(scenario, "name", "") or ""): index
        for index, scenario in enumerate(list(getattr(scenario_set, "scenarios", []) or []))
    }
    return sorted(
        [result for result in list(scenario_results or []) if isinstance(result, ScenarioResult)],
        key=lambda result: _lg_e2_scenario_result_sort_key(result, scenario_index_by_name),
    )

def _lg_e2_selected_feedback_digest(feedback: SimFeedback, scenario_set: Any | None = None) -> dict[str, Any]:
    selected = None
    scenario_results = (
        _lg_e2_canonicalize_scenario_results(list(feedback.scenario_results or []), scenario_set)
        if scenario_set is not None
        else list(feedback.scenario_results or [])
    )
    canonical_feedback_payload = {
        "ok": bool(feedback.ok),
        "n_scenarios": int(feedback.n_scenarios),
        "n_scenarios_passed": int(feedback.n_scenarios_passed),
        "scenario_results": _jsonable(scenario_results),
        "setup_error": feedback.setup_error,
        "oracle_weak": bool(feedback.oracle_weak),
        "weak_oracle_reason": feedback.weak_oracle_reason,
        "weak_oracle_evidence": _jsonable(feedback.weak_oracle_evidence),
    }
    if not feedback.ok and not getattr(feedback, "oracle_weak", False):
        selected = {
            "source": FeedbackSource.SIM.value,
            "source_stage": StageId.SD_6_SIM.value,
            "feedback_hash": _hash_payload(canonical_feedback_payload),
            "failing_scenario_names": [
                result.name
                for result in scenario_results
                if isinstance(result, ScenarioResult) and result.status != "pass"
            ],
            "setup_error_hash": _hash_text(feedback.setup_error) if feedback.setup_error else None,
        }
    return {
        "selected": selected,
        "selected_feedback_digest": _hash_payload(selected),
    }

def _lg_e2_scenario_history_summary(history: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for item in history or []:
        if not isinstance(item, dict):
            continue
        coverage = item.get("coverage")
        summary.append(
            {
                "iteration": item.get("iteration"),
                "attempt_index": item.get("attempt_index"),
                "scenario_set_id": item.get("scenario_set_id"),
                "epoch": item.get("epoch"),
                "scenario_names": list(item.get("scenario_names") or []),
                "coverage_gap": item.get("coverage_gap"),
                "oracle_weak": item.get("oracle_weak"),
                "coverage_hash": _hash_payload(coverage) if coverage is not None else None,
            }
        )
    return summary

def _lg_e2_coverage_summary(scenario_set: Any) -> dict[str, Any]:
    coverage = getattr(scenario_set, "coverage_report", {}) or {}
    return {
        "scenario_set_id": getattr(scenario_set, "scenario_set_id", None),
        "scenario_epoch": getattr(scenario_set, "epoch", None),
        "scenario_names": [getattr(scenario, "name", "") for scenario in list(getattr(scenario_set, "scenarios", []) or [])],
        "coverage_summary_hash": _hash_payload(coverage),
        "coverage_gap": bool(coverage.get("coverage_gap")) if isinstance(coverage, dict) else None,
        "oracle_weak": bool(coverage.get("oracle_weak")) if isinstance(coverage, dict) and "oracle_weak" in coverage else None,
    }

def _lg_e2_serial_equivalence_payload(
    *,
    scenario_results: list[Any],
    selected_feedback_digest: dict[str, Any],
    scenario_history: list[dict[str, Any]],
    scenario_set: Any,
    oracle_weak: bool,
    scenario_epoch: int | None,
    final_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": LG_E2_SEND_PARALLEL_SCHEMA_VERSION,
        "hash_input_schema_version": f"{LG_E2_SEND_PARALLEL_SCHEMA_VERSION}.serial-equivalence-hash.v1",
        "scenario_results": _jsonable(scenario_results),
        "selected_feedback_digest": _jsonable(selected_feedback_digest),
        "scenario_history_summary": _lg_e2_scenario_history_summary(scenario_history),
        "coverage_summary": _lg_e2_coverage_summary(scenario_set),
        "oracle_weak": bool(oracle_weak),
        "scenario_epoch": scenario_epoch,
        "nfrr_eligibility_verdict_summary": final_summary or {"status": "pending_at_sd6"},
    }

def _lg_e2_build_isolated_context(context: StageContext, *, current_dsl: str, scenario_set: ScenarioSet) -> StageContext:
    """Build a worker-local StageContext without sharing mutable graph objects."""

    isolated = StageContext(
        nl=str(getattr(context, "nl", "") or ""),
        current_dsl=current_dsl,
        grounding_map=copy.deepcopy(getattr(context, "grounding_map", None)),
        scenario_set=scenario_set,
        warning_budget_state=copy.deepcopy(getattr(context, "warning_budget_state", {}) or {}),
    )
    isolated.inspect_json = copy.deepcopy(getattr(context, "inspect_json", None))
    return isolated

def _lg_e2_single_scenario_set(scenario_set: ScenarioSet, scenario: Any) -> ScenarioSet:
    return ScenarioSet(
        scenario_set_id=scenario_set.scenario_set_id,
        scenarios=[copy.deepcopy(scenario)],
        source_dsl_hash=scenario_set.source_dsl_hash,
        source_inspect_hash=scenario_set.source_inspect_hash,
        source_grounding_hash=scenario_set.source_grounding_hash,
        coverage_report=copy.deepcopy(scenario_set.coverage_report),
        epoch=scenario_set.epoch,
        frozen=scenario_set.frozen,
        invalidated_by=copy.deepcopy(scenario_set.invalidated_by),
    )

def _lg_e2_preflight(
    *,
    enabled_requested: bool,
    adapters: FullStagedRuntimeAdapters,
    scenario_set: ScenarioSet,
    context: StageContext,
    current_dsl: str,
) -> dict[str, Any]:
    scenario_count = len(list(scenario_set.scenarios or []))
    preflight = {
        "schema_version": LG_E2_SEND_PARALLEL_SCHEMA_VERSION,
        "send_api_import_ok": Send is not None,
        "enabled_requested": bool(enabled_requested),
        "scenario_count": scenario_count,
        "parallel_send_enabled": False,
        "fallback_reason": "",
        "thread_safety_basis": "deepcopy_isolated_worker_context_and_single_scenario_set",
        "worker_shared_object_policy": "workers receive no graph_state, reducer channel, FixLog, scenario_history or shared ScenarioSet object",
    }
    if not enabled_requested:
        preflight["fallback_reason"] = "lg_e2_send_parallel_disabled_by_runtime_parameter"
        return preflight
    if scenario_count <= 0:
        preflight["fallback_reason"] = "no_scenarios_to_fan_out"
        return preflight
    if getattr(adapters.sim, "lg_e2_thread_safe", None) is False:
        preflight["fallback_reason"] = "sim_adapter_declared_lg_e2_thread_safe_false"
        return preflight
    if getattr(adapters.sim, "lg_e2_thread_safe", None) is not True:
        preflight["fallback_reason"] = "sim_adapter_lacks_lg_e2_thread_safety_declaration"
        return preflight
    try:
        probe_set = _lg_e2_single_scenario_set(scenario_set, scenario_set.scenarios[0])
        _lg_e2_build_isolated_context(context, current_dsl=current_dsl, scenario_set=probe_set)
        copy.deepcopy(scenario_set.scenarios[0])
        preflight["deepcopy_isolation_ok"] = True
    except Exception as exc:
        preflight["deepcopy_isolation_ok"] = False
        preflight["fallback_reason"] = f"deepcopy_isolation_failed:{type(exc).__name__}:{str(exc)[:160]}"
        return preflight
    preflight["parallel_send_enabled"] = True
    preflight["fallback_reason"] = ""
    return preflight

def _lg_e2_worker_specs(*, current_dsl: str, scenario_set: ScenarioSet, context: StageContext) -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    scenario_epoch = int(getattr(scenario_set, "epoch", 0) or 0)
    for scenario_index, scenario in enumerate(list(scenario_set.scenarios or [])):
        normalized_name = _lg_e2_normalized_scenario_name(getattr(scenario, "name", ""))
        input_hash = _hash_payload(
            {
                "current_dsl_hash": _hash_text(current_dsl),
                "scenario_set_id": scenario_set.scenario_set_id,
                "scenario_epoch": scenario_epoch,
                "scenario_index": scenario_index,
                "scenario": scenario,
            }
        )
        ordering_key = {
            "scenario_epoch": scenario_epoch,
            "scenario_index": scenario_index,
            "normalized_scenario_name": normalized_name,
            "checker_name": "sd6_sim",
            "input_hash": input_hash,
        }
        single_set = _lg_e2_single_scenario_set(scenario_set, scenario)
        specs.append(
            {
                "schema_version": LG_E2_SEND_PARALLEL_SCHEMA_VERSION,
                "current_dsl": current_dsl,
                "scenario_set": single_set,
                "context": _lg_e2_build_isolated_context(context, current_dsl=current_dsl, scenario_set=single_set),
                "scenario_name": getattr(scenario, "name", ""),
                "ordering_key": ordering_key,
                "send_arg_hash": _hash_payload({"ordering_key": ordering_key, "scenario": scenario}),
            }
        )
    return specs

def _lg_e2_execute_send_graph(
    *,
    worker_specs: list[dict[str, Any]],
    sim_adapter: Any,
) -> list[dict[str, Any]]:
    graph = StateGraph(_LgE2SendState)

    def route_workers(state: _LgE2SendState) -> list[Send]:
        return [Send("lg_e2_sd6_scenario_worker", spec) for spec in list(state.get("worker_specs") or [])]

    def worker(spec: dict[str, Any]) -> dict[str, Any]:
        ordering_key = dict(spec.get("ordering_key") or {})
        feedback, meta = sim_adapter(spec["current_dsl"], spec["scenario_set"], spec["context"])
        return {
            "worker_results": [
                {
                    "schema_version": LG_E2_SEND_PARALLEL_SCHEMA_VERSION,
                    "ordering_key": ordering_key,
                    "scenario_name": spec.get("scenario_name"),
                    "send_arg_hash": spec.get("send_arg_hash"),
                    "feedback": feedback,
                    "meta": meta,
                    "feedback_hash": _hash_payload(feedback),
                    "meta_hash": _hash_payload(meta),
                    "scenario_result_count": len(_lg_e2_feedback_scenario_results(feedback)),
                    "ok": bool(getattr(feedback, "ok", False)),
                    "oracle_weak": bool(getattr(feedback, "oracle_weak", False)),
                }
            ]
        }

    graph.add_node("lg_e2_sd6_scenario_worker", worker)
    graph.add_conditional_edges(START, route_workers)
    graph.add_edge("lg_e2_sd6_scenario_worker", END)
    app = graph.compile(checkpointer=False)
    result = app.invoke({"worker_specs": worker_specs, "worker_results": []})
    return [item for item in list(result.get("worker_results") or []) if isinstance(item, dict)]

def _lg_e2_aggregate_worker_results(
    *,
    worker_results: list[dict[str, Any]],
    scenario_set: ScenarioSet,
) -> tuple[SimFeedback, StageResultMeta, list[dict[str, Any]]]:
    canonical = _lg_e2_canonicalize_worker_results(worker_results)
    scenario_results_by_name: dict[str, list[ScenarioResult]] = defaultdict(list)
    setup_errors: list[str] = []
    weak_reasons: list[str] = []
    weak_evidence: list[Any] = []
    hard_failure_seen = False
    n_passed = 0
    ok = True
    any_error_status = False
    for worker in canonical:
        feedback = worker.get("feedback")
        meta = worker.get("meta")
        if not isinstance(feedback, SimFeedback):
            raise TypeError("LG-E2 worker must return SimFeedback")
        ok = ok and bool(feedback.ok)
        n_passed += int(getattr(feedback, "n_scenarios_passed", 0) or 0)
        for result in feedback.scenario_results:
            if isinstance(result, ScenarioResult):
                scenario_results_by_name[str(result.name or "")].append(result)
        if feedback.setup_error:
            setup_errors.append(feedback.setup_error)
        if not feedback.ok and feedback.oracle_weak:
            weak_reasons.append(feedback.weak_oracle_reason)
            weak_evidence.append(feedback.weak_oracle_evidence)
        elif not feedback.ok:
            hard_failure_seen = True
        if getattr(meta, "status", None) == StageStatus.ERROR:
            any_error_status = True
            hard_failure_seen = True
    status = StageStatus.ERROR if any_error_status else (StageStatus.OK if ok else StageStatus.FAIL)
    scenario_results: list[ScenarioResult] = []
    for scenario in list(scenario_set.scenarios or []):
        scenario_name = str(getattr(scenario, "name", "") or "")
        scenario_results.extend(scenario_results_by_name.pop(scenario_name, []))
    for leftover_name in sorted(scenario_results_by_name, key=_lg_e2_normalized_scenario_name):
        scenario_results.extend(scenario_results_by_name[leftover_name])
    feedback = SimFeedback(
        ok=ok,
        n_scenarios=len(list(scenario_set.scenarios or [])),
        n_scenarios_passed=n_passed,
        scenario_results=scenario_results,
        setup_error=setup_errors[0] if setup_errors else None,
        oracle_weak=bool(weak_reasons) and not hard_failure_seen,
        weak_oracle_reason=";".join(reason for reason in weak_reasons if reason) if bool(weak_reasons) and not hard_failure_seen else "",
        weak_oracle_evidence={"worker_evidence": _jsonable(weak_evidence)} if bool(weak_reasons) and not hard_failure_seen else {},
    )
    meta = _meta(StageId.SD_6_SIM, ok=feedback.ok, status=status)
    meta.input_hash = _hash_payload(
        {
            "scenario_set_id": scenario_set.scenario_set_id,
            "scenario_epoch": scenario_set.epoch,
            "scenario_names": [getattr(scenario, "name", "") for scenario in list(scenario_set.scenarios or [])],
        }
    )
    meta.output_hash = _hash_payload(feedback)
    return feedback, meta, canonical

def _lg_e2_first_blocking_id(selected_digest: dict[str, Any]) -> str | None:
    selected = selected_digest.get("selected") if isinstance(selected_digest, dict) else None
    if not isinstance(selected, dict):
        return None
    names = selected.get("failing_scenario_names")
    if isinstance(names, list) and names:
        return str(names[0])
    setup_hash = selected.get("setup_error_hash")
    if setup_hash:
        return f"setup_error:{setup_hash}"
    return None

def _lg_e2_metadata_for_feedback(
    *,
    enabled_requested: bool,
    preflight: dict[str, Any],
    scenario_set: ScenarioSet,
    feedback: SimFeedback,
    scenario_history: list[dict[str, Any]],
    worker_results: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    canonical_workers = _lg_e2_canonicalize_worker_results(worker_results or [])
    scenario_results = _lg_e2_canonicalize_scenario_results(list(feedback.scenario_results), scenario_set)
    selected_digest = _lg_e2_selected_feedback_digest(feedback, scenario_set)
    serial_payload = _lg_e2_serial_equivalence_payload(
        scenario_results=scenario_results,
        selected_feedback_digest=selected_digest,
        scenario_history=scenario_history,
        scenario_set=scenario_set,
        oracle_weak=feedback.oracle_weak,
        scenario_epoch=scenario_set.epoch,
    )
    canonical_result_hash = _hash_payload(_jsonable(scenario_results))
    return {
        "schema_version": LG_E2_SEND_PARALLEL_SCHEMA_VERSION,
        "instrumentation_layer": LG_E2_SEND_PARALLEL_INSTRUMENTATION_LAYER,
        "enabled_requested": bool(enabled_requested),
        "parallel_send_enabled": bool(preflight.get("parallel_send_enabled")),
        "fallback_reason": str(preflight.get("fallback_reason") or ""),
        "preflight": _jsonable(preflight),
        "send_api": "langgraph.types.Send",
        "send_api_import_ok": bool(preflight.get("send_api_import_ok")),
        "ordering_key_fields": list(_LG_E2_ORDERING_KEY_FIELDS),
        "worker_count": len(canonical_workers),
        "fanout_count": len(list(scenario_set.scenarios or [])),
        "raw_worker_order": [
            _jsonable((worker.get("ordering_key") or {}))
            for worker in list(worker_results or [])
            if isinstance(worker, dict)
        ],
        "canonical_worker_order": [
            _jsonable((worker.get("ordering_key") or {}))
            for worker in canonical_workers
        ],
        "canonical_scenario_results": _jsonable(scenario_results),
        "canonical_result_hash": canonical_result_hash,
        "coverage_summary": _lg_e2_coverage_summary(scenario_set),
        "coverage_summary_hash": _lg_e2_coverage_summary(scenario_set)["coverage_summary_hash"],
        "selected_feedback_digest": selected_digest,
        "first_blocking_id": _lg_e2_first_blocking_id(selected_digest),
        "scenario_epoch": scenario_set.epoch,
        "oracle_weak": bool(feedback.oracle_weak),
        "serial_equivalence_hash": _hash_payload(serial_payload),
        "serial_equivalence_hash_input_scope": {
            "scenario_results": True,
            "first_blocking_or_selected_feedback_digest": True,
            "scenario_history_summary": True,
            "coverage_summary": True,
            "oracle_weak": True,
            "nfrr_eligibility_verdict_summary": "pending_at_sd6_finalized_in_run_record_trace",
            "excludes_operator_event_order_wall_clock_latency": True,
        },
        "does_not_replace_academic_evidence": True,
    }

def _lg_e2_final_verdict_summary(record: Any) -> dict[str, Any]:
    final_artifacts = record.final_artifacts if isinstance(getattr(record, "final_artifacts", None), dict) else {}
    return {
        "record_status": getattr(record, "status", None),
        "verdict": final_artifacts.get("verdict"),
        "verdict_source_stage_id": final_artifacts.get("verdict_source_stage_id"),
        "agent_loop_result_status": final_artifacts.get("agent_loop_result_status"),
        "main_result_eligible": final_artifacts.get("main_result_eligible"),
        "inclusion_reason": final_artifacts.get("inclusion_reason"),
        "exclusion_reason": final_artifacts.get("exclusion_reason"),
        "oracle_weak": final_artifacts.get("oracle_weak"),
    }

def _lg_e2_finalize_metadata_from_record(record: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    finalized = dict(metadata)
    iteration = finalized.get("iteration")
    scenario_results = finalized.get("canonical_scenario_results") or []
    final_summary = _lg_e2_final_verdict_summary(record)
    final_payload = {
        "schema_version": LG_E2_SEND_PARALLEL_SCHEMA_VERSION,
        "hash_input_schema_version": f"{LG_E2_SEND_PARALLEL_SCHEMA_VERSION}.serial-equivalence-hash.v1",
        "scenario_results": _jsonable(scenario_results or []),
        "selected_feedback_digest": _jsonable(finalized.get("selected_feedback_digest") or {}),
        "scenario_history_summary": _lg_e2_scenario_history_summary(list(getattr(record, "scenario_history", []) or [])),
        "coverage_summary": _jsonable(finalized.get("coverage_summary") or {}),
        "oracle_weak": bool(finalized.get("oracle_weak")),
        "scenario_epoch": finalized.get("scenario_epoch"),
        "nfrr_eligibility_verdict_summary": final_summary,
    }
    finalized["serial_equivalence_hash"] = _hash_payload(final_payload)
    finalized["serial_equivalence_hash_finalized"] = True
    finalized["nfrr_eligibility_verdict_summary"] = final_summary
    finalized["serial_equivalence_hash_input_payload_hash"] = _hash_payload(final_payload)
    return finalized

def _lg_e2_run_sd6_send_parallel_or_serial(
    graph_state: _ValidationSubgraphState,
    *,
    runtime_cfg: FullStagedRuntimeConfig,
    adapters: FullStagedRuntimeAdapters,
    current_dsl: str,
    scenario_set: ScenarioSet,
    context: StageContext,
    iteration: int,
    enabled_requested: bool,
) -> tuple[SimFeedback, StageResultMeta, dict[str, Any]]:
    preflight = _lg_e2_preflight(
        enabled_requested=enabled_requested,
        adapters=adapters,
        scenario_set=scenario_set,
        context=context,
        current_dsl=current_dsl,
    )
    scenario_history = list(graph_state.get("validation_scenario_history") or [])
    input_payload = {
        "current_dsl": current_dsl,
        "scenario_set": scenario_set,
        "context": context,
        "lg_e2_preflight": preflight,
    }
    if not preflight.get("parallel_send_enabled"):
        sim_feedback, sim_meta = _lg_e3_fixed_tool_call(
            graph_state,
            tool_name="sd6_sim",
            stage_id=StageId.SD_6_SIM.value,
            graph_node="validation_sd6_sim",
            iteration=iteration,
            input_payload=input_payload,
            call=lambda: adapters.sim(current_dsl, scenario_set, context),
        )
        if not isinstance(sim_feedback, SimFeedback):
            raise TypeError("SD-6 sim adapter must return SimFeedback")
        metadata = _lg_e2_metadata_for_feedback(
            enabled_requested=enabled_requested,
            preflight=preflight,
            scenario_set=scenario_set,
            feedback=sim_feedback,
            scenario_history=scenario_history,
            worker_results=[],
        )
        return sim_feedback, sim_meta, metadata

    def call_parallel() -> tuple[SimFeedback, StageResultMeta, dict[str, Any]]:
        worker_specs = _lg_e2_worker_specs(current_dsl=current_dsl, scenario_set=scenario_set, context=context)
        worker_results = _lg_e2_execute_send_graph(worker_specs=worker_specs, sim_adapter=adapters.sim)
        parallel_feedback, parallel_meta, canonical_workers = _lg_e2_aggregate_worker_results(
            worker_results=worker_results,
            scenario_set=scenario_set,
        )
        parallel_metadata = _lg_e2_metadata_for_feedback(
            enabled_requested=enabled_requested,
            preflight=preflight,
            scenario_set=scenario_set,
            feedback=parallel_feedback,
            scenario_history=scenario_history,
            worker_results=worker_results,
        )
        serial_feedback, serial_meta = adapters.sim(current_dsl, scenario_set, context)
        if not isinstance(serial_feedback, SimFeedback):
            raise TypeError("SD-6 serial control adapter must return SimFeedback")
        metadata = _lg_e2_metadata_for_feedback(
            enabled_requested=enabled_requested,
            preflight=preflight,
            scenario_set=scenario_set,
            feedback=serial_feedback,
            scenario_history=scenario_history,
            worker_results=worker_results,
        )
        serial_alignment_ok = (
            parallel_metadata["canonical_result_hash"] == metadata["canonical_result_hash"]
            and parallel_metadata["serial_equivalence_hash"] == metadata["serial_equivalence_hash"]
            and bool(parallel_feedback.oracle_weak) == bool(serial_feedback.oracle_weak)
            and bool(parallel_feedback.ok) == bool(serial_feedback.ok)
        )
        metadata["parallel_canonical_result_hash"] = parallel_metadata["canonical_result_hash"]
        metadata["serial_canonical_result_hash"] = metadata["canonical_result_hash"]
        metadata["parallel_serial_equivalence_hash"] = parallel_metadata["serial_equivalence_hash"]
        metadata["serial_control_equivalence_hash"] = metadata["serial_equivalence_hash"]
        metadata["serial_control_run_executed"] = True
        metadata["serial_alignment_ok"] = serial_alignment_ok
        metadata["canonical_output_source"] = "serial_control_after_send_alignment"
        if not serial_alignment_ok:
            metadata["canonical_fallback_reason"] = "parallel_serial_alignment_mismatch_canonical_serial_used"
        else:
            metadata["canonical_fallback_reason"] = ""
        metadata["worker_count"] = len(canonical_workers)
        metadata["send_constructed_count"] = len(worker_specs)
        metadata["send_arg_hashes"] = [str(spec.get("send_arg_hash") or "") for spec in worker_specs]
        metadata["parallel_aggregate_meta_hash"] = _hash_payload(parallel_meta)
        metadata["serial_control_meta_hash"] = _hash_payload(serial_meta)
        return serial_feedback, serial_meta, metadata

    sim_feedback, sim_meta, metadata = _lg_e3_fixed_tool_call(
        graph_state,
        tool_name="sd6_sim",
        stage_id=StageId.SD_6_SIM.value,
        graph_node="validation_sd6_sim",
        iteration=iteration,
        input_payload=input_payload,
        call=call_parallel,
    )
    return sim_feedback, sim_meta, metadata

def _augment_run_record_with_lg_e2_send_parallel_trace(
    result: AgentLoopResult,
    *,
    events: list[dict[str, Any]],
    enabled: bool,
) -> None:
    if not result.run_record_path:
        return
    path = result.run_record_path
    record = read_agent_loop_run_record(path)
    contract = build_lg_e2_send_parallel_contract()
    finalized_events = [
        _jsonable(_lg_e2_finalize_metadata_from_record(record, event))
        for event in list(events or [])
        if isinstance(event, dict)
    ]
    trace = {
        "schema_version": LG_E2_SEND_PARALLEL_SCHEMA_VERSION,
        "instrumentation_layer": LG_E2_SEND_PARALLEL_INSTRUMENTATION_LAYER,
        "enabled": bool(enabled),
        "event_count": len(finalized_events),
        "events_hash": _hash_payload(finalized_events),
        "parallel_send_enabled_count": sum(1 for event in finalized_events if bool(event.get("parallel_send_enabled"))),
        "fallback_count": sum(1 for event in finalized_events if not bool(event.get("parallel_send_enabled"))),
        "serial_equivalence_hashes": [
            str(event.get("serial_equivalence_hash") or "")
            for event in finalized_events
            if event.get("serial_equivalence_hash")
        ],
        "canonical_result_hashes": [
            str(event.get("canonical_result_hash") or "")
            for event in finalized_events
            if event.get("canonical_result_hash")
        ],
        "contract_hash": _hash_payload(contract),
        "ordering_key_fields": contract["ordering_key_fields"],
        "does_not_replace_academic_evidence": True,
        "academic_evidence_sources": list(_LG_D1_ACADEMIC_EVIDENCE_SOURCES),
        "events": finalized_events,
    }
    record.environment["lg_e2_send_parallel_enabled"] = bool(enabled)
    record.environment["lg_e2_send_parallel_schema_version"] = LG_E2_SEND_PARALLEL_SCHEMA_VERSION
    record.environment["lg_e2_send_parallel_event_count"] = len(finalized_events)
    record.environment["lg_e2_send_parallel_events_hash"] = trace["events_hash"]
    record.environment["lg_e2_send_parallel_contract_hash"] = trace["contract_hash"]
    record.environment["lg_e2_send_parallel_ordering_key_fields"] = trace["ordering_key_fields"]
    record.run_config["lg_e2_send_parallel_enabled"] = bool(enabled)
    record.run_config["lg_e2_send_parallel_schema_version"] = LG_E2_SEND_PARALLEL_SCHEMA_VERSION
    record.run_config["lg_e2_send_parallel_contract"] = contract
    record.final_artifacts["lg_e2_send_parallel_trace"] = trace
    record.logs.append(
        {
            "event": "lg_e2_send_parallel_trace",
            "instrumentation_layer": LG_E2_SEND_PARALLEL_INSTRUMENTATION_LAYER,
            "enabled": bool(enabled),
            "event_count": len(finalized_events),
            "parallel_send_enabled_count": trace["parallel_send_enabled_count"],
            "fallback_count": trace["fallback_count"],
            "events_hash": trace["events_hash"],
            "does_not_replace_academic_evidence": True,
        }
    )
    write_agent_loop_run_record(record, path)

