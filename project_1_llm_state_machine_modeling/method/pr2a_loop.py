"""PR-2A deterministic integration loop.

This runner wires the PR-0/PR-1A/PR-1B contracts into one local, replayable
agent loop without calling any real LLM provider/API.  SL-9 is represented by
deterministic candidate injection so the repair/RepairReview wiring can be
tested without provider drift.  PR-2B can later replace that injection point
with real replay-aware LLM calls.
"""

from __future__ import annotations

import hashlib
import math
import platform
import subprocess
from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from method.run_record import agent_loop_run_record_path, write_agent_loop_run_record
from method.schema import (
    AgentLoopResult,
    AgentLoopRunRecord,
    FeedbackBundle,
    FixPlan,
    GroundingMap,
    IterTrace,
    ModelArtifact,
    ScenarioSet,
    StageContext,
    StageResultMeta,
    TestScenario,
    RevisedFixPlan,
)
from method.stages.ids import FEEDBACK_SOURCE_TO_STAGE_ID, STAGE_SPECS_BY_ID, FeedbackSource, StageId, StageStatus
from method.stages.sd_tools import (
    freeze_scenario_set,
    mark_warning_repair_attempt,
    run_sd2_parse,
    run_sd3_semantic,
    run_sd4_design,
    run_sd5a_scenario_coverage,
    run_sd6_sim,
    run_sd8_fix_plan,
    run_sd10_repair_review,
)
from method.stages.sl_repair_prompt import build_sl9_repair_prompt

SC_0_STAGE_GRAPH = [
    StageId.SC_0_START.value,
    StageId.SD_2_PARSE.value,
    StageId.SD_3_SEMANTIC.value,
    StageId.SD_4_DESIGN.value,
    StageId.SL_5_SCENARIO_GENERATION.value,
    StageId.SD_5A_SCENARIO_COVERAGE.value,
    StageId.SC_5F_SCENARIO_FREEZE.value,
    StageId.SD_6_SIM.value,
    StageId.SD_8_FIX_PLAN.value,
    StageId.SL_9_REPAIR.value,
    StageId.SD_10_REPAIR_REVIEW.value,
    StageId.SC_11_ACCEPT_CANDIDATE.value,
    StageId.SC_12_EXIT.value,
    StageId.SC_13_TRACE_AUDIT.value,
]

RUN_RECORD_SCHEMA_VERSION = "pr2a.agent-loop-run-record.v1"


@dataclass
class DeterministicLoopConfig:
    """Configuration for the PR-2A deterministic runner."""

    initial_dsl: str
    scenarios: list[TestScenario] = field(default_factory=list)
    repair_candidates: list[str] = field(default_factory=list)
    grounding_map: GroundingMap | None = None
    run_id: str = ""
    output_dir: str | Path = "runs"
    max_iterations: int = 3
    policy_profile: str = "generated_candidate"
    seed: int | None = None
    path_context: dict[str, Any] = field(default_factory=dict)


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _hash_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _short_hash(value: Any) -> str:
    return "sha256:" + hashlib.sha256(repr(_jsonable(value)).encode("utf-8")).hexdigest()


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(v) for v in value]
    if is_dataclass(value) and not isinstance(value, type):
        return _jsonable(asdict(value))
    if is_dataclass(value) and isinstance(value, type):
        return f"<non-json:dataclass-type:{value.__name__}>"
    return str(value)


def _strict_jsonable(value: Any) -> Any:
    """JSON-normalize run-record payloads while preserving audit visibility."""
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if math.isfinite(value):
            return value
        if math.isnan(value):
            return "<non-json-float:nan>"
        return "<non-json-float:inf>" if value > 0 else "<non-json-float:-inf>"
    if isinstance(value, dict):
        return {str(k): _strict_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_strict_jsonable(v) for v in value]
    if is_dataclass(value) and not isinstance(value, type):
        return _strict_jsonable(asdict(value))
    if is_dataclass(value) and isinstance(value, type):
        return f"<non-json:dataclass-type:{value.__name__}>"
    return f"<non-json:{type(value).__name__}>"


def _json_normalized_changed(original: Any, normalized: Any) -> bool:
    try:
        changed = normalized != original
    except Exception:
        return True
    return changed if isinstance(changed, bool) else True


def _record_payload_sanitized_log(field: str, *, message: str | None = None) -> dict[str, Any]:
    return {
        "ts": _utc_now(),
        "level": "error",
        "event": "record_payload_sanitized",
        "field": field,
        "message": message or "non-json record payload normalized; run excluded from Path1/Path2 main results",
    }


def _strict_record_field(field: str, value: Any, logs: list[dict[str, Any]]) -> tuple[Any, bool]:
    try:
        normalized = _strict_jsonable(value)
    except Exception as e:
        logs.append(
            _record_payload_sanitized_log(
                field,
                message=f"record payload normalization failed: {type(e).__name__}: {e}",
            )
        )
        return f"<non-json-normalization-error:{type(value).__name__}:{type(e).__name__}>", True
    changed = _json_normalized_changed(value, normalized)
    if changed:
        logs.append(_record_payload_sanitized_log(field))
    return normalized, changed


def _meta(stage_id: StageId, *, ok: bool = True, status: StageStatus | None = None, stage_error: str | None = None) -> StageResultMeta:
    spec = STAGE_SPECS_BY_ID[stage_id.value]
    return StageResultMeta(
        stage_id=stage_id.value,
        stage_kind=spec.kind,
        enabled=True,
        ran=True,
        status=status or (StageStatus.OK if ok else StageStatus.FAIL),
        ok=ok,
        stage_error=stage_error,
    )


def _stage_ids(stage_records: list[StageResultMeta]) -> list[str]:
    return [meta.stage_id for meta in stage_records]


def _append_stage(stage_records: list[StageResultMeta], meta: StageResultMeta) -> StageResultMeta:
    stage_records.append(meta)
    return meta


def _feedback_bundle(
    *,
    parse_feedback: Any = None,
    semantic_feedback: Any = None,
    design_feedback: Any = None,
    sim_feedback: Any = None,
    stage_results: list[StageResultMeta] | None = None,
) -> FeedbackBundle:
    return FeedbackBundle(
        enabled_sources=[
            FeedbackSource.PARSE.value,
            FeedbackSource.SEMANTIC.value,
            FeedbackSource.DESIGN.value,
            FeedbackSource.SIM.value,
        ],
        parse=parse_feedback,
        semantic=semantic_feedback,
        design=design_feedback,
        sim=sim_feedback,
        stage_results=list(stage_results or []),
    )


def _select_feedback(bundle: FeedbackBundle) -> tuple[str, Any, str] | None:
    """Pick the first feedback item that should trigger PR-2A repair."""
    if bundle.parse is not None and not bundle.parse.ok:
        return FeedbackSource.PARSE.value, bundle.parse, FEEDBACK_SOURCE_TO_STAGE_ID[FeedbackSource.PARSE.value]
    if bundle.semantic is not None and not bundle.semantic.ok:
        return FeedbackSource.SEMANTIC.value, bundle.semantic, FEEDBACK_SOURCE_TO_STAGE_ID[FeedbackSource.SEMANTIC.value]
    if bundle.design is not None and bundle.design.blocking_items:
        return FeedbackSource.DESIGN.value, bundle.design, FEEDBACK_SOURCE_TO_STAGE_ID[FeedbackSource.DESIGN.value]
    if bundle.sim is not None and not bundle.sim.ok:
        return FeedbackSource.SIM.value, bundle.sim, FEEDBACK_SOURCE_TO_STAGE_ID[FeedbackSource.SIM.value]
    return None


def _environment() -> dict[str, Any]:
    git_commit = ""
    try:
        git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        git_commit = "unknown"
    pyfcstm_version = ""
    try:
        import pyfcstm  # type: ignore

        pyfcstm_version = getattr(pyfcstm, "__version__", "unknown")
    except Exception:
        pyfcstm_version = "unavailable"
    return {
        "git_commit": git_commit,
        "python_version": platform.python_version(),
        "pyfcstm_version": pyfcstm_version,
        "runner": "method.pr2a_loop.run_pr2a_deterministic_loop",
        "llm_provider": "none",
    }


def _make_sl9_meta(prompt_messages: list[dict[str, str]], candidate_dsl: str, *, ok: bool = True) -> StageResultMeta:
    meta = _meta(StageId.SL_9_REPAIR, ok=ok, status=StageStatus.OK if ok else StageStatus.ERROR)
    meta.prompt_hash = _short_hash(prompt_messages)
    meta.output_hash = _hash_text(candidate_dsl)
    return meta


def _run_feedback_round(
    *,
    nl: str,
    current_dsl: str,
    scenario_set: ScenarioSet | None,
    grounding_map: GroundingMap | None,
    policy_profile: str,
    carried_warning_budget: dict[str, Any],
) -> tuple[StageContext, FeedbackBundle, list[StageResultMeta]]:
    context = StageContext(
        nl=nl,
        current_dsl=current_dsl,
        grounding_map=grounding_map,
        scenario_set=scenario_set,
        warning_budget_state=carried_warning_budget,
    )
    stage_results: list[StageResultMeta] = []

    parse_feedback, parse_meta = run_sd2_parse(current_dsl, context)
    stage_results.append(parse_meta)
    if not parse_feedback.ok:
        return context, _feedback_bundle(parse_feedback=parse_feedback, stage_results=stage_results), stage_results

    semantic_feedback, semantic_meta, _build = run_sd3_semantic(current_dsl, context)
    stage_results.append(semantic_meta)
    if not semantic_feedback.ok:
        return context, _feedback_bundle(
            parse_feedback=parse_feedback,
            semantic_feedback=semantic_feedback,
            stage_results=stage_results,
        ), stage_results

    design_feedback, design_meta = run_sd4_design(context, policy_profile=policy_profile)  # type: ignore[arg-type]
    stage_results.append(design_meta)
    bundle = _feedback_bundle(
        parse_feedback=parse_feedback,
        semantic_feedback=semantic_feedback,
        design_feedback=design_feedback,
        stage_results=stage_results,
    )
    if scenario_set is not None:
        sim_feedback, sim_meta = run_sd6_sim(current_dsl, scenario_set, context)
        stage_results.append(sim_meta)
        bundle.sim = sim_feedback
        bundle.stage_results.append(sim_meta)
    return context, bundle, stage_results


def _scenario_set_for_current_dsl(
    cfg: DeterministicLoopConfig,
    *,
    current_dsl: str,
    context: StageContext,
) -> tuple[ScenarioSet, list[StageResultMeta], dict[str, Any]]:
    coverage, coverage_meta = run_sd5a_scenario_coverage(current_dsl, cfg.scenarios)
    scenario_set, freeze_meta = freeze_scenario_set(
        cfg.scenarios,
        source_dsl_hash=_hash_text(current_dsl),
        source_inspect_hash=_short_hash(context.inspect_json) if context.inspect_json is not None else "",
        source_grounding_hash=_short_hash(cfg.grounding_map) if cfg.grounding_map is not None else None,
        coverage_report=coverage,
        epoch=0,
    )
    sl5_meta = _meta(StageId.SL_5_SCENARIO_GENERATION, ok=True)
    sl5_meta.output_hash = _short_hash(cfg.scenarios)
    return scenario_set, [sl5_meta, coverage_meta, freeze_meta], coverage


def _build_record(
    *,
    cfg: DeterministicLoopConfig,
    nl: str,
    status: str,
    current_dsl: str,
    run_started_at: str,
    stage_records: list[StageResultMeta],
    iteration_records: list[dict[str, Any]],
    llm_interactions: list[dict[str, Any]],
    deterministic_feedback: dict[str, Any],
    repair_history: list[dict[str, Any]],
    scenario_history: list[dict[str, Any]],
    logs: list[dict[str, Any]],
    error_message: str | None = None,
    force_invalid: bool = False,
) -> AgentLoopRunRecord:
    sanitized = force_invalid
    path_context_payload, changed = _strict_record_field("input_bundle.path_context", cfg.path_context, logs)
    sanitized = sanitized or changed
    iteration_records_payload, changed = _strict_record_field("iteration_records", iteration_records, logs)
    sanitized = sanitized or changed
    llm_interactions_payload, changed = _strict_record_field("llm_interactions", llm_interactions, logs)
    sanitized = sanitized or changed
    deterministic_feedback_payload, changed = _strict_record_field("deterministic_feedback", deterministic_feedback, logs)
    sanitized = sanitized or changed
    repair_history_payload, changed = _strict_record_field("repair_history", repair_history, logs)
    sanitized = sanitized or changed
    scenario_history_payload, changed = _strict_record_field("scenario_history", scenario_history, logs)
    sanitized = sanitized or changed

    final_status = "invalid" if sanitized else status
    main_result_eligible = final_status == "success"
    record = AgentLoopRunRecord(
        schema_version=RUN_RECORD_SCHEMA_VERSION,
        run_id=cfg.run_id,
        created_at=run_started_at,
        status=final_status,  # type: ignore[arg-type]
        input_bundle={
            "nl": nl,
            "initial_dsl_hash": _hash_text(cfg.initial_dsl),
            "path_context": path_context_payload,
        },
        run_config={
            "max_iterations": cfg.max_iterations,
            "policy_profile": cfg.policy_profile,
            "seed": cfg.seed,
            "real_llm_provider_api": False,
            "sl9_mode": "fake_replay_candidate_injection",
        },
        environment=_environment(),
        stage_graph={
            "planned": SC_0_STAGE_GRAPH,
            "executed": _stage_ids(stage_records),
        },
        stage_records=[asdict(meta) for meta in stage_records],
        iteration_records=iteration_records_payload,
        llm_interactions=llm_interactions_payload,
        deterministic_feedback=deterministic_feedback_payload,
        repair_history=repair_history_payload,
        scenario_history=scenario_history_payload,
        final_artifacts={
            "final_dsl": current_dsl,
            "final_dsl_hash": _hash_text(current_dsl),
            "verdict": final_status,
            "main_result_eligible": main_result_eligible,
            "path_result_filter": "include only status == success and main_result_eligible == true",
            "error_message": error_message,
        },
        logs=logs,
        replay_index={
            "stage_by_index": {str(i): meta.stage_id for i, meta in enumerate(stage_records)},
            "iteration_count": len(iteration_records),
            "record_replay_command": "python -m method.run_record <path>",
        },
        redaction_report=[],
    )
    return record


def run_pr2a_deterministic_loop(nl: str, cfg: DeterministicLoopConfig) -> AgentLoopResult:
    """Run the PR-2A deterministic integration loop and persist a run record."""
    run_id = cfg.run_id or "pr2a-" + hashlib.sha256(f"{nl}\n{cfg.initial_dsl}".encode("utf-8")).hexdigest()[:12]
    cfg.run_id = run_id
    run_started_at = _utc_now()
    result = AgentLoopResult(llm_model="fake-none")
    stage_records: list[StageResultMeta] = []
    iteration_records: list[dict[str, Any]] = []
    llm_interactions: list[dict[str, Any]] = []
    repair_history: list[dict[str, Any]] = []
    scenario_history: list[dict[str, Any]] = []
    deterministic_feedback: dict[str, Any] = {"iterations": []}
    logs: list[dict[str, Any]] = []
    current_dsl = cfg.initial_dsl
    status = "failed"
    error_message: str | None = None
    warning_budget_state: dict[str, Any] = {}
    pending_rejection = None
    pending_original_plan: FixPlan | None = None
    force_invalid_record = False

    _append_stage(stage_records, _meta(StageId.SC_0_START, ok=True))

    scenario_set: ScenarioSet | None = None

    for iteration in range(max(1, cfg.max_iterations)):
        context, bundle, feedback_stage_results = _run_feedback_round(
            nl=nl,
            current_dsl=current_dsl,
            scenario_set=scenario_set,
            grounding_map=cfg.grounding_map,
            policy_profile=cfg.policy_profile,
            carried_warning_budget=warning_budget_state,
        )
        warning_budget_state = context.warning_budget_state
        if iteration == 0 and scenario_set is None:
            stage_records.extend(feedback_stage_results)
            if bundle.parse is not None and bundle.parse.ok and bundle.semantic is not None and bundle.semantic.ok:
                scenario_set, scenario_stage_metas, _coverage = _scenario_set_for_current_dsl(
                    cfg,
                    current_dsl=current_dsl,
                    context=context,
                )
                context.scenario_set = scenario_set
                scenario_history.append(asdict(scenario_set))
                sim_feedback, sim_meta = run_sd6_sim(current_dsl, scenario_set, context)
                bundle.sim = sim_feedback
                bundle.stage_results.append(sim_meta)
                feedback_stage_results.append(sim_meta)
                trace_sim_rows = [sim_meta]
            else:
                scenario_stage_metas = []
                trace_sim_rows = []
            stage_records.extend(scenario_stage_metas)
            stage_records.extend(trace_sim_rows)
        else:
            stage_records.extend(feedback_stage_results)

        selected = _select_feedback(bundle)
        design_payload = asdict(bundle.design) if bundle.design is not None else None
        sim_payload = asdict(bundle.sim) if bundle.sim is not None else None
        deterministic_feedback["iterations"].append(
            {
                "iteration": iteration,
                "parse": asdict(bundle.parse) if bundle.parse is not None else None,
                "semantic": asdict(bundle.semantic) if bundle.semantic is not None else None,
                "design": design_payload,
                "sim": sim_payload,
            }
        )
        trace = IterTrace(
            iteration=iteration,
            model=ModelArtifact(dsl_text=current_dsl, iteration=iteration, produced_by="modeler" if iteration == 0 else "repair"),
            feedback=bundle,
            stage_results=list(feedback_stage_results),
            stage_context_summary=asdict(context.to_summary()),
            warning_budget_state=dict(context.warning_budget_state),
            scenario_epoch=scenario_set.epoch if scenario_set is not None else None,
        )
        result.iter_traces.append(trace)

        iteration_record: dict[str, Any] = {
            "iteration": iteration,
            "dsl_hash": _hash_text(current_dsl),
            "stage_ids": _stage_ids(feedback_stage_results),
            "stage_context_summary": asdict(context.to_summary()),
            "warning_budget_state": {k: asdict(v) for k, v in context.warning_budget_state.items()},
            "scenario_epoch": scenario_set.epoch if scenario_set is not None else None,
            "selected_feedback": None,
            "repair_review": None,
        }

        if selected is None:
            _append_stage(stage_records, _meta(StageId.SC_12_EXIT, ok=True))
            status = "success"
            iteration_record["exit_reason"] = "all_required_feedback_ok"
            iteration_records.append(iteration_record)
            result.status = "converged"
            break

        source, feedback, source_stage = selected
        iteration_record["selected_feedback"] = {"source": source, "source_stage": source_stage}

        pending_retry = pending_rejection is not None and pending_original_plan is not None
        candidate_available = iteration < len(cfg.repair_candidates)
        if not candidate_available or (iteration >= cfg.max_iterations - 1 and not pending_retry):
            _append_stage(stage_records, _meta(StageId.SC_12_EXIT, ok=False, status=StageStatus.FAIL))
            status = "failed"
            error_message = "repair budget exhausted or no deterministic candidate available"
            iteration_record["exit_reason"] = error_message
            iteration_records.append(iteration_record)
            result.status = "not_converged"
            break

        if pending_rejection is not None and pending_original_plan is not None:
            fix_plan, fix_meta = run_sd8_fix_plan(
                None,
                source="repair_review",
                rejection=pending_rejection,
                original=pending_original_plan,
            )
        else:
            fix_plan, fix_meta = run_sd8_fix_plan(
                feedback,
                source=source,
                source_stage=source_stage,
                grounding_map=cfg.grounding_map,
                before_dsl=current_dsl,
            )
        _append_stage(stage_records, fix_meta)
        if isinstance(fix_plan, RevisedFixPlan):
            effective_fix_plan = fix_plan.original
            plan_kind = "RevisedFixPlan"
        else:
            effective_fix_plan = fix_plan
            plan_kind = "FixPlan"
        assert isinstance(effective_fix_plan, FixPlan)

        candidate_dsl = cfg.repair_candidates[min(iteration, len(cfg.repair_candidates) - 1)]
        prompt_messages = build_sl9_repair_prompt(
            nl=nl,
            current_dsl=current_dsl,
            fix_plan=fix_plan,
            grounding_map=cfg.grounding_map,
            selected_diagnostics=effective_fix_plan.evidence,
            preserve_list=effective_fix_plan.required_preserve_element_ids,
            scenario_summary={
                "scenario_set_id": scenario_set.scenario_set_id if scenario_set is not None else None,
                "epoch": scenario_set.epoch if scenario_set is not None else None,
                "n_scenarios": len(scenario_set.scenarios) if scenario_set is not None else 0,
            },
        )
        sl9_meta = _make_sl9_meta(prompt_messages, candidate_dsl)
        _append_stage(stage_records, sl9_meta)
        llm_interactions.append(
            {
                "stage_id": StageId.SL_9_REPAIR.value,
                "provider": "fake",
                "model_id": "deterministic-candidate-injection",
                "prompt_template_version": "sl9-repair.v1",
                "prompt_hash": sl9_meta.prompt_hash,
                "input_hash": _hash_text(current_dsl),
                "raw_output_hash": sl9_meta.output_hash,
                "prompt_messages": prompt_messages,
                "raw_output": candidate_dsl,
                "parsed_output": {"candidate_dsl": candidate_dsl},
                "schema_validation_ok": True,
                "replay_key": f"fake-sl9:{run_id}:{iteration}",
                "note": "PR-2A never calls a real LLM provider/API.",
            }
        )
        if source == FeedbackSource.DESIGN.value and bundle.design is not None:
            mark_warning_repair_attempt(
                context.warning_budget_state,
                [item.instance_key for item in bundle.design.blocking_items],
            )

        repair_review, repair_review_meta = run_sd10_repair_review(
            nl=nl,
            grounding_map=cfg.grounding_map,
            old_dsl=current_dsl,
            candidate_dsl=candidate_dsl,
            fix_plan=effective_fix_plan,
            scenario_set=scenario_set,
        )
        _append_stage(stage_records, repair_review_meta)
        iteration_record["repair_review"] = asdict(repair_review)
        trace.repair_review = repair_review
        repair_history.append(
            {
                "iteration": iteration,
                "plan_kind": plan_kind,
                "fix_plan": asdict(effective_fix_plan),
                "revised_fix_plan": asdict(fix_plan) if isinstance(fix_plan, RevisedFixPlan) else None,
                "candidate_dsl": candidate_dsl,
                "candidate_dsl_hash": _hash_text(candidate_dsl),
                "repair_review": asdict(repair_review),
                "accepted": repair_review.ok,
            }
        )
        if repair_review.ok:
            _append_stage(stage_records, _meta(StageId.SC_11_ACCEPT_CANDIDATE, ok=True))
            trace.repair = ModelArtifact(dsl_text=candidate_dsl, iteration=iteration + 1, produced_by="repair")
            current_dsl = candidate_dsl
            iteration_record["accepted_candidate"] = True
            iteration_record["exit_reason"] = "candidate_accepted_by_repair_review"
            pending_rejection = None
            pending_original_plan = None
            iteration_records.append(iteration_record)
            if iteration >= cfg.max_iterations - 1:
                _append_stage(stage_records, _meta(StageId.SC_12_EXIT, ok=True))
                status = "success"
                result.status = "converged"
                break
            continue

        pending_rejection = repair_review.local_rejection
        pending_original_plan = effective_fix_plan
        if iteration < cfg.max_iterations - 1 and iteration + 1 < len(cfg.repair_candidates) and pending_rejection is not None:
            _append_stage(stage_records, _meta(StageId.SC_11_ACCEPT_CANDIDATE, ok=False, status=StageStatus.FAIL))
            iteration_record["accepted_candidate"] = False
            iteration_record["exit_reason"] = "repair_review_rejected_retry_with_revised_fix_plan"
            iteration_records.append(iteration_record)
            continue

        _append_stage(stage_records, _meta(StageId.SC_11_ACCEPT_CANDIDATE, ok=False, status=StageStatus.FAIL))
        _append_stage(stage_records, _meta(StageId.SC_12_EXIT, ok=False, status=StageStatus.FAIL))
        status = "rejected"
        error_message = repair_review.local_rejection.reason if repair_review.local_rejection else "repair rejected"
        iteration_record["accepted_candidate"] = False
        iteration_record["exit_reason"] = error_message
        iteration_records.append(iteration_record)
        result.status = "not_converged"
        break
    else:
        _append_stage(stage_records, _meta(StageId.SC_12_EXIT, ok=False, status=StageStatus.FAIL))
        status = "budget_exhausted"
        error_message = "max_iterations exhausted"
        result.status = "not_converged"

    result.final_dsl = current_dsl
    result.final_artifact = ModelArtifact(dsl_text=current_dsl, iteration=len(result.iter_traces), produced_by="repair")
    result.final_feedback = result.iter_traces[-1].feedback if result.iter_traces else None
    result.error_message = error_message

    trace_meta = _meta(StageId.SC_13_TRACE_AUDIT, ok=True)
    _append_stage(stage_records, trace_meta)
    record = _build_record(
        cfg=cfg,
        nl=nl,
        status=status,
        current_dsl=current_dsl,
        run_started_at=run_started_at,
        stage_records=stage_records,
        iteration_records=iteration_records,
        llm_interactions=llm_interactions,
        deterministic_feedback=deterministic_feedback,
        repair_history=repair_history,
        scenario_history=scenario_history,
        logs=logs,
        error_message=error_message,
        force_invalid=force_invalid_record,
    )
    path = write_agent_loop_run_record(record, agent_loop_run_record_path(cfg.output_dir, run_id))
    result.run_record_path = str(path)
    result.run_record_id = run_id
    return result
