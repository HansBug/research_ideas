"""PR-B1 deterministic full-staged runtime driver.

This module intentionally implements only the **control-flow semantics** of the
canonical full staged loop.  It does not call real providers and it does not read
``.env``/process provider configuration.  SL stages are supplied through
explicit adapters so PR-B1 can prove the stage ordering, repair revalidation,
weak-oracle eligibility, and run-record trace semantics before PR-B2/PR-C wire
real LLM adapters into the canonical ``method.loop`` entry point.
"""

from __future__ import annotations

import hashlib
import platform
import subprocess
from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from method.run_record import agent_loop_run_record_path, write_agent_loop_run_record
from method.schema import (
    AgentLoopResult,
    AgentLoopRunRecord,
    DesignFeedback,
    FixPlan,
    GroundingMap,
    ModelReviewFeedback,
    ParseFeedback,
    RepairReviewFeedback,
    RevisedFixPlan,
    ScenarioSet,
    SemanticFeedback,
    SimFeedback,
    StageContext,
    StageResultMeta,
    TestScenario,
)
from method.stages.ids import ALL_STAGE_SPECS, FEEDBACK_SOURCE_TO_STAGE_ID, FeedbackSource, StageId, StageStatus, STAGE_SPECS_BY_ID
from method.stages.sd_tools import freeze_scenario_set, mark_warning_repair_attempt, run_sd8_fix_plan
from method.stages.sd_tools import (
    run_sd2_parse,
    run_sd3_semantic,
    run_sd4_design,
    run_sd5a_scenario_coverage,
    run_sd6_sim,
    run_sd10_repair_review,
)

RUN_RECORD_SCHEMA_VERSION = "pr-b1.full-staged-deterministic-runtime.v1"


@dataclass
class ScenarioGenerationRequest:
    """Input to the injectable PR-B1 ``SL-5`` scenario adapter."""

    nl: str
    current_dsl: str
    context: StageContext
    attempt_index: int = 0
    coverage_directive: Any | None = None
    previous_scenarios: list[TestScenario] = field(default_factory=list)
    scenario_epoch: int = 0


@dataclass
class RepairRequest:
    """Input shared by PR-B1 ``SL-9`` repair and ``SD-10`` review adapters."""

    nl: str
    grounding_map: GroundingMap | None
    old_dsl: str
    fix_plan: FixPlan | RevisedFixPlan | None
    selected_feedback: Any = None
    selected_feedback_trace: dict[str, Any] = field(default_factory=dict)
    scenario_set: ScenarioSet | None = None
    candidate_dsl: str = ""
    iteration: int = 0
    repair_attempt: int = 0


@dataclass
class FullStagedRuntimeConfig:
    """Configuration for the PR-B1 deterministic control-flow driver.

    ``adapter_mode`` defaults to ``test_injected`` and
    ``allow_main_result_eligible`` defaults to ``False`` on purpose: PR-B1 is a
    deterministic skeleton with injectable SL adapters, not the final PR-C
    default real-provider runtime.  PR-C may opt into main-result eligibility
    only after real adapters and default-entry integration are wired.
    """

    initial_dsl: str
    grounding_map: GroundingMap | None = None
    run_id: str = ""
    output_dir: str | Path = "runs"
    max_iterations: int = 5
    scenario_max_retries: int = 2
    policy_profile: str = "experiment_default"
    write_run_record: bool = True
    adapter_mode: str = "test_injected"
    allow_main_result_eligible: bool = False
    path_context: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.max_iterations < 0:
            raise ValueError("FullStagedRuntimeConfig.max_iterations must be >= 0")
        if self.scenario_max_retries < 0:
            raise ValueError("FullStagedRuntimeConfig.scenario_max_retries must be >= 0")


InitialModelingAdapter = Callable[[str, StageContext], Any]
ParseAdapter = Callable[[str, StageContext], tuple[ParseFeedback, StageResultMeta]]
SemanticAdapter = Callable[[str, StageContext], tuple[SemanticFeedback, StageResultMeta]]
DesignAdapter = Callable[[StageContext], tuple[DesignFeedback, StageResultMeta]]
ScenarioGenerateAdapter = Callable[[ScenarioGenerationRequest], Any]
ScenarioCoverageAdapter = Callable[[str, list[TestScenario]], tuple[dict[str, Any], StageResultMeta]]
SimAdapter = Callable[[str, ScenarioSet, StageContext], tuple[SimFeedback, StageResultMeta]]
ModelReviewAdapter = Callable[[str, StageContext, dict[str, Any]], Any]
RepairAdapter = Callable[[RepairRequest], Any]
RepairReviewAdapter = Callable[[RepairRequest], tuple[RepairReviewFeedback, StageResultMeta]]
DeltaReviewAdapter = Callable[[RepairRequest, RepairReviewFeedback], Any]


@dataclass
class FullStagedRuntimeAdapters:
    """Explicit adapters used by the PR-B1 control-flow driver.

    PR-B1 deliberately has no hidden fake defaults for SL stages.  Tests and
    future integration code must pass adapters explicitly, making the fake/real
    boundary visible in both code and run records.
    """

    parse: ParseAdapter
    semantic: SemanticAdapter
    design: DesignAdapter
    scenario_generate: ScenarioGenerateAdapter
    scenario_coverage: ScenarioCoverageAdapter
    sim: SimAdapter
    model_review: ModelReviewAdapter
    repair: RepairAdapter
    repair_review: RepairReviewAdapter
    delta_review: DeltaReviewAdapter | None = None
    initial_modeling: InitialModelingAdapter | None = None


def build_full_staged_runtime_adapters(
    *,
    scenario_generate: ScenarioGenerateAdapter,
    repair: RepairAdapter,
    model_review: ModelReviewAdapter,
    policy_profile: str = "generated_candidate",
    delta_review: DeltaReviewAdapter | None = None,
) -> FullStagedRuntimeAdapters:
    """Build PR-B1 adapters from existing deterministic SD tools.

    ``SL-5`` / ``SL-7`` / ``SL-9`` remain explicit callables so this helper does
    not hide fake providers or read provider configuration.  The deterministic
    stages are wired to the #14 SD tool façade, including ``SD-10``'s local
    repair-review gates (parse/semantic/design rerun, grounding drift and
    scenario regression checks).
    """

    def semantic_adapter(current_dsl: str, context: StageContext) -> tuple[SemanticFeedback, StageResultMeta]:
        feedback, meta, _build = run_sd3_semantic(current_dsl, context)
        return feedback, meta

    def design_adapter(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        return run_sd4_design(context, policy_profile=policy_profile)  # type: ignore[arg-type]

    def sim_adapter(current_dsl: str, scenario_set: ScenarioSet, context: StageContext) -> tuple[SimFeedback, StageResultMeta]:
        return run_sd6_sim(current_dsl, scenario_set, context)

    def repair_review_adapter(request: RepairRequest) -> tuple[RepairReviewFeedback, StageResultMeta]:
        if not isinstance(request.fix_plan, FixPlan):
            raise TypeError("SD-10 repair review requires an effective FixPlan")
        return run_sd10_repair_review(
            nl=request.nl,
            grounding_map=request.grounding_map,
            old_dsl=request.old_dsl,
            candidate_dsl=request.candidate_dsl,
            fix_plan=request.fix_plan,
            scenario_set=request.scenario_set,
        )

    return FullStagedRuntimeAdapters(
        parse=run_sd2_parse,
        semantic=semantic_adapter,
        design=design_adapter,
        scenario_generate=scenario_generate,
        scenario_coverage=run_sd5a_scenario_coverage,
        sim=sim_adapter,
        model_review=model_review,
        repair=repair,
        repair_review=repair_review_adapter,
        delta_review=delta_review,
    )


@dataclass
class _ValidationPass:
    context: StageContext
    feedback: dict[str, Any]
    stage_metas: list[StageResultMeta]
    selected: tuple[str, Any, str] | None
    scenario_set: ScenarioSet | None
    scenario_history: list[dict[str, Any]]
    oracle_weak: bool
    scenario_epoch: int | None


@dataclass
class _RunState:
    run_id: str
    run_started_at: str
    current_dsl: str
    scenario_set: ScenarioSet | None = None
    scenario_epoch: int = 0
    oracle_weak: bool = False
    stage_records: list[StageResultMeta] = field(default_factory=list)
    iteration_records: list[dict[str, Any]] = field(default_factory=list)
    deterministic_feedback: dict[str, Any] = field(default_factory=lambda: {"iterations": []})
    repair_history: list[dict[str, Any]] = field(default_factory=list)
    scenario_history: list[dict[str, Any]] = field(default_factory=list)
    llm_interactions: list[dict[str, Any]] = field(default_factory=list)
    logs: list[dict[str, Any]] = field(default_factory=list)
    final_record_status: str = "failed"
    final_verdict: str = "not_converged"
    verdict_source_stage_id: str | None = None
    verdict_reason: str | None = None
    result_status: str = "not_converged"
    error_message: str | None = None
    pre_scenario_repair_count: int = 0


@dataclass
class _LLMRetryExhausted(Exception):
    """Internal control-flow signal for PR-B2 ``LLMStageRun`` retry exhaustion."""

    stage_id: str
    retry_error: dict[str, Any]
    interaction: dict[str, Any] = field(default_factory=dict)

    @property
    def error_kind(self) -> str:
        return str(self.retry_error.get("error_kind") or "unknown")

    @property
    def error_message(self) -> str:
        return str(self.retry_error.get("error_message") or f"{self.stage_id} retry exhausted")


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _hash_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(v) for v in value]
    if is_dataclass(value) and not isinstance(value, type):
        return _jsonable(asdict(value))
    return str(value)


def _short_hash(value: Any) -> str:
    return "sha256:" + hashlib.sha256(repr(_jsonable(value)).encode("utf-8")).hexdigest()


def _git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


def _environment(cfg: FullStagedRuntimeConfig) -> dict[str, Any]:
    return {
        "git_commit": _git_commit(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "runner": "method.staged_runtime.run_full_staged_deterministic_runtime",
        "adapter_mode": cfg.adapter_mode,
        "real_llm_provider_api": False,
        "provider_config_read": False,
    }


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


def _append_stage(rows: list[StageResultMeta], meta: StageResultMeta) -> StageResultMeta:
    rows.append(meta)
    return meta


def _is_llm_stage_run(value: Any) -> bool:
    """Duck-type PR-B2 ``LLMStageRun`` without importing that branch-only module."""

    return all(hasattr(value, attr) for attr in ("stage_id", "ok", "stage_meta", "interaction", "parsed_output"))


def _retry_error_from_llm_stage_run(run: Any) -> dict[str, Any] | None:
    retry_error = getattr(run, "retry_error", None)
    if retry_error is None and isinstance(getattr(run, "interaction", None), dict):
        retry_error = run.interaction.get("retry_error")
    if retry_error:
        return dict(retry_error)
    return None


def _append_llm_stage_run(
    *,
    run: Any,
    expected_stage_id: StageId,
    stage_records: list[StageResultMeta],
    iteration_stage_metas: list[StageResultMeta] | None,
    llm_interactions: list[dict[str, Any]],
) -> Any:
    """Append PR-B2 stage metadata and raise on retry exhaustion.

    PR-B2 reports provider/schema/empty-output exhaustion as
    ``LLMStageRun.ok=False`` plus ``interaction['retry_error']``.  PR-B1's
    responsibility is control-flow routing: record the failed LLM stage and jump
    to ``SC-12`` instead of treating it as deterministic feedback or repairable
    model quality evidence.
    """

    if not _is_llm_stage_run(run):
        return run
    stage_id = str(getattr(run, "stage_id"))
    if stage_id != expected_stage_id.value:
        raise ValueError(f"LLMStageRun stage_id mismatch: expected {expected_stage_id.value}, got {stage_id}")
    meta = getattr(run, "stage_meta")
    _append_stage(stage_records, meta)
    if iteration_stage_metas is not None:
        iteration_stage_metas.append(meta)
    interaction = dict(getattr(run, "interaction", {}) or {})
    if interaction:
        llm_interactions.append(interaction)
    retry_error = _retry_error_from_llm_stage_run(run)
    if getattr(run, "ok") is False and retry_error is not None:
        raise _LLMRetryExhausted(stage_id=stage_id, retry_error=retry_error, interaction=interaction)
    return run


def _verdict_for_retry_error(error_kind: str) -> tuple[str, str]:
    if error_kind == "provider_error":
        return "provider_error", "error"
    return "invalid", "invalid"


def _result_status_for_verdict(verdict: str) -> str:
    if verdict == "success":
        return "converged"
    if verdict == "provider_error":
        return "api_failed"
    if verdict == "invalid":
        return "spec_failed"
    return "not_converged"


def _mark_sc12_verdict(
    state: _RunState,
    *,
    verdict: str,
    source_stage_id: str,
    reason: str,
    record_status: str | None = None,
    result_status: str | None = None,
    stage_ok: bool | None = None,
    stage_status: StageStatus | None = None,
) -> StageResultMeta:
    """Route the run into ``SC-12`` with an auditable verdict edge."""

    if record_status is None:
        if verdict == "success":
            record_status = "success"
        elif verdict == "provider_error":
            record_status = "error"
        elif verdict == "invalid":
            record_status = "invalid"
        else:
            record_status = "budget_exhausted"
    if result_status is None:
        result_status = _result_status_for_verdict(verdict)
    if stage_ok is None:
        stage_ok = verdict == "success"
    if stage_status is None:
        stage_status = StageStatus.OK if stage_ok else (StageStatus.ERROR if verdict in {"provider_error", "invalid"} else StageStatus.FAIL)
    meta = _meta(StageId.SC_12_EXIT, ok=stage_ok, status=stage_status)
    meta.stage_error = None if stage_ok else reason
    _append_stage(state.stage_records, meta)
    state.final_record_status = record_status
    state.final_verdict = verdict
    state.verdict_source_stage_id = source_stage_id
    state.verdict_reason = reason
    state.result_status = result_status
    state.error_message = None if verdict == "success" else reason
    state.logs.append(
        {
            "ts": _utc_now(),
            "level": "info" if verdict == "success" else "warning",
            "event": "sc12_verdict",
            "verdict": verdict,
            "source_stage_id": source_stage_id,
            "reason": reason,
        }
    )
    return meta


def _mark_retry_exhausted(state: _RunState, exc: _LLMRetryExhausted) -> None:
    verdict, record_status = _verdict_for_retry_error(exc.error_kind)
    reason = f"{exc.stage_id} retry exhausted: {exc.error_kind}: {exc.error_message}"
    _mark_sc12_verdict(
        state,
        verdict=verdict,
        source_stage_id=exc.stage_id,
        reason=reason,
        record_status=record_status,
        result_status=_result_status_for_verdict(verdict),
        stage_ok=False,
        stage_status=StageStatus.ERROR,
    )


def _stage_ids(rows: list[StageResultMeta]) -> list[str]:
    return [meta.stage_id for meta in rows]


def _planned_stage_graph(stage_records: list[StageResultMeta]) -> dict[str, Any]:
    executed = _stage_ids(stage_records)
    executed_counts: dict[str, int] = {}
    for sid in executed:
        executed_counts[sid] = executed_counts.get(sid, 0) + 1
    nodes: list[dict[str, Any]] = []
    for index, spec in enumerate(ALL_STAGE_SPECS):
        ran = executed_counts.get(spec.stage_id, 0) > 0
        nodes.append(
            {
                "index": index,
                "stage_id": spec.stage_id,
                "stage_kind": spec.kind.value,
                "name": spec.name,
                "doc_filename": spec.doc_filename,
                "enabled": True,
                "ran": ran,
                "run_count": executed_counts.get(spec.stage_id, 0),
                "status": StageStatus.OK.value if ran else StageStatus.SKIPPED.value,
                "skipped_reason": None if ran else "not_reached_in_this_run",
            }
        )
    return {
        "planned": [spec.stage_id for spec in ALL_STAGE_SPECS],
        "executed": executed,
        "nodes": nodes,
    }


def _stage_trace(stage_id: str, feedback: Any = None) -> dict[str, Any]:
    payload = {
        "source_stage": stage_id,
        "source": _source_for_stage(stage_id),
        "ok": getattr(feedback, "ok", None),
    }
    if isinstance(feedback, DesignFeedback):
        items = [*feedback.blocking_items, *feedback.advisory_items, *feedback.info_items]
        payload.update(
            {
                "policy_actions": [item.policy_action for item in items],
                "diagnostic_codes": [item.code for item in items],
                "blocking_instance_keys": [item.instance_key for item in feedback.blocking_items],
            }
        )
    elif isinstance(feedback, ModelReviewFeedback):
        payload.update(
            {
                "decision": feedback.decision,
                "risk_level": feedback.risk_level,
                "blocking_findings": _jsonable(feedback.blocking_findings),
            }
        )
    elif isinstance(feedback, (ParseFeedback, SemanticFeedback)):
        payload["diagnostics"] = _jsonable(getattr(feedback, "diagnostics", []))
    elif isinstance(feedback, SimFeedback):
        payload.update(
            {
                "n_scenarios": feedback.n_scenarios,
                "n_scenarios_passed": feedback.n_scenarios_passed,
                "setup_error": feedback.setup_error,
            }
        )
    return payload


def _source_for_stage(stage_id: str) -> str:
    for source, sid in FEEDBACK_SOURCE_TO_STAGE_ID.items():
        if sid == stage_id:
            return source
    if stage_id == StageId.SD_5A_SCENARIO_COVERAGE.value:
        return "scenario_coverage"
    return "control"


def _model_review_blocks(feedback: ModelReviewFeedback) -> bool:
    return (
        feedback.decision == "fail"
        and feedback.risk_level == "major"
        and bool(feedback.blocking_findings)
    )


def _select_first_blocking(feedback: dict[str, Any]) -> tuple[str, Any, str] | None:
    parse = feedback.get(FeedbackSource.PARSE.value)
    if isinstance(parse, ParseFeedback) and not parse.ok:
        return FeedbackSource.PARSE.value, parse, StageId.SD_2_PARSE.value

    semantic = feedback.get(FeedbackSource.SEMANTIC.value)
    if isinstance(semantic, SemanticFeedback) and not semantic.ok:
        return FeedbackSource.SEMANTIC.value, semantic, StageId.SD_3_SEMANTIC.value

    design = feedback.get(FeedbackSource.DESIGN.value)
    if isinstance(design, DesignFeedback) and design.blocking_items:
        return FeedbackSource.DESIGN.value, design, StageId.SD_4_DESIGN.value

    sim = feedback.get(FeedbackSource.SIM.value)
    if isinstance(sim, SimFeedback) and not sim.ok:
        return FeedbackSource.SIM.value, sim, StageId.SD_6_SIM.value

    review = feedback.get(FeedbackSource.MODEL_REVIEW.value)
    if isinstance(review, ModelReviewFeedback) and _model_review_blocks(review):
        return FeedbackSource.MODEL_REVIEW.value, review, StageId.SL_7_MODEL_REVIEW.value

    return None


def _scenario_history_item(
    *,
    iteration: int,
    attempt_index: int,
    scenarios: list[TestScenario],
    coverage: dict[str, Any],
    coverage_meta: StageResultMeta,
    retry_exhausted: bool = False,
    oracle_weak: bool = False,
) -> dict[str, Any]:
    return {
        "iteration": iteration,
        "attempt_index": attempt_index,
        "n_scenarios": len(scenarios),
        "scenario_names": [scenario.name for scenario in scenarios],
        "coverage": _jsonable(coverage),
        "coverage_gap": bool(coverage.get("coverage_gap")),
        "coverage_meta": _jsonable(coverage_meta),
        "retry_exhausted": retry_exhausted,
        "oracle_weak": oracle_weak,
    }


def _run_scenario_generation_and_freeze(
    *,
    nl: str,
    current_dsl: str,
    context: StageContext,
    cfg: FullStagedRuntimeConfig,
    adapters: FullStagedRuntimeAdapters,
    iteration: int,
    stage_records: list[StageResultMeta],
    iteration_stage_metas: list[StageResultMeta],
    llm_interactions: list[dict[str, Any]],
    logs: list[dict[str, Any]],
    scenario_epoch: int,
) -> tuple[ScenarioSet, list[dict[str, Any]], bool, int]:
    coverage_directive: Any | None = None
    previous_scenarios: list[TestScenario] = []
    scenario_history: list[dict[str, Any]] = []
    selected_scenarios: list[TestScenario] = []
    selected_coverage: dict[str, Any] = {"coverage_report": {}, "coverage_gap": False, "retry_directive": None}
    weak = False

    for attempt_index in range(cfg.scenario_max_retries + 1):
        request = ScenarioGenerationRequest(
            nl=nl,
            current_dsl=current_dsl,
            context=context,
            attempt_index=attempt_index,
            coverage_directive=coverage_directive,
            previous_scenarios=previous_scenarios,
            scenario_epoch=scenario_epoch,
        )
        generated = adapters.scenario_generate(request)
        generated = _append_llm_stage_run(
            run=generated,
            expected_stage_id=StageId.SL_5_SCENARIO_GENERATION,
            stage_records=stage_records,
            iteration_stage_metas=iteration_stage_metas,
            llm_interactions=llm_interactions,
        )
        if _is_llm_stage_run(generated):
            scenarios = list(getattr(generated, "parsed_output", []) or [])
        else:
            scenarios = list(generated or [])
            sl5_meta = _meta(StageId.SL_5_SCENARIO_GENERATION, ok=True)
            sl5_meta.input_hash = _hash_text(current_dsl)
            sl5_meta.output_hash = _short_hash(scenarios)
            _append_stage(stage_records, sl5_meta)
            iteration_stage_metas.append(sl5_meta)

        coverage, coverage_meta = adapters.scenario_coverage(current_dsl, scenarios)
        _append_stage(stage_records, coverage_meta)
        iteration_stage_metas.append(coverage_meta)
        selected_scenarios = scenarios
        selected_coverage = dict(coverage)
        gap = bool(coverage.get("coverage_gap"))
        retry_exhausted = gap and attempt_index >= cfg.scenario_max_retries
        weak = retry_exhausted
        scenario_history.append(
            _scenario_history_item(
                iteration=iteration,
                attempt_index=attempt_index,
                scenarios=scenarios,
                coverage=coverage,
                coverage_meta=coverage_meta,
                retry_exhausted=retry_exhausted,
                oracle_weak=weak,
            )
        )
        if not gap:
            break
        retry_directive = coverage.get("retry_directive")
        coverage_directive = retry_directive if retry_directive is not None else {"retry_reason": "coverage_gap"}
        previous_scenarios = scenarios

    if weak:
        selected_coverage = {
            **selected_coverage,
            "oracle_weak": True,
            "weak_oracle_reason": "scenario_coverage_retry_exhausted",
        }
        logs.append(
            {
                "ts": _utc_now(),
                "level": "warning",
                "event": "scenario_coverage_retry_exhausted",
                "iteration": iteration,
                "scenario_max_retries": cfg.scenario_max_retries,
            }
        )

    scenario_set, freeze_meta = freeze_scenario_set(
        selected_scenarios,
        source_dsl_hash=_hash_text(current_dsl),
        source_inspect_hash=_short_hash(context.inspect_json) if context.inspect_json is not None else "",
        source_grounding_hash=_short_hash(cfg.grounding_map) if cfg.grounding_map is not None else None,
        coverage_report=selected_coverage,
        epoch=scenario_epoch,
    )
    scenario_set.coverage_report["oracle_weak"] = weak
    _append_stage(stage_records, freeze_meta)
    iteration_stage_metas.append(freeze_meta)
    if scenario_history:
        scenario_history[-1]["scenario_set_id"] = scenario_set.scenario_set_id
        scenario_history[-1]["epoch"] = scenario_set.epoch
        scenario_history[-1]["oracle_weak"] = weak
    return scenario_set, scenario_history, weak, scenario_epoch + 1


def _reuse_or_check_scenario_set(
    *,
    current_dsl: str,
    scenario_set: ScenarioSet,
    adapters: FullStagedRuntimeAdapters,
    iteration: int,
    stage_records: list[StageResultMeta],
    iteration_stage_metas: list[StageResultMeta],
    logs: list[dict[str, Any]],
) -> tuple[ScenarioSet, list[dict[str, Any]], bool]:
    coverage, coverage_meta = adapters.scenario_coverage(current_dsl, list(scenario_set.scenarios))
    _append_stage(stage_records, coverage_meta)
    iteration_stage_metas.append(coverage_meta)
    weak = bool(coverage.get("coverage_gap"))
    if weak:
        scenario_set.coverage_report = {
            **dict(scenario_set.coverage_report),
            **dict(coverage),
            "oracle_weak": True,
            "weak_oracle_reason": "frozen_scenario_coverage_or_compatibility_gap",
        }
        logs.append(
            {
                "ts": _utc_now(),
                "level": "warning",
                "event": "frozen_scenario_coverage_gap",
                "iteration": iteration,
                "scenario_set_id": scenario_set.scenario_set_id,
            }
        )
    freeze_meta = _meta(StageId.SC_5F_SCENARIO_FREEZE, ok=True)
    freeze_meta.input_hash = _hash_text(current_dsl)
    freeze_meta.output_hash = _hash_text(scenario_set.scenario_set_id)
    _append_stage(stage_records, freeze_meta)
    iteration_stage_metas.append(freeze_meta)
    history = [
        _scenario_history_item(
            iteration=iteration,
            attempt_index=0,
            scenarios=list(scenario_set.scenarios),
            coverage=coverage,
            coverage_meta=coverage_meta,
            retry_exhausted=False,
            oracle_weak=weak,
        )
    ]
    history[0]["scenario_set_id"] = scenario_set.scenario_set_id
    history[0]["epoch"] = scenario_set.epoch
    history[0]["reused_frozen_oracle"] = True
    return scenario_set, history, weak


def _run_validation_pass(
    *,
    nl: str,
    current_dsl: str,
    cfg: FullStagedRuntimeConfig,
    adapters: FullStagedRuntimeAdapters,
    scenario_set: ScenarioSet | None,
    scenario_epoch: int,
    oracle_weak: bool,
    iteration: int,
    stage_records: list[StageResultMeta],
    logs: list[dict[str, Any]],
    llm_interactions: list[dict[str, Any]],
) -> _ValidationPass:
    context = StageContext(nl=nl, current_dsl=current_dsl, grounding_map=cfg.grounding_map, scenario_set=scenario_set)
    feedback: dict[str, Any] = {}
    iteration_stage_metas: list[StageResultMeta] = []
    scenario_history: list[dict[str, Any]] = []

    parse_feedback, parse_meta = adapters.parse(current_dsl, context)
    feedback[FeedbackSource.PARSE.value] = parse_feedback
    _append_stage(stage_records, parse_meta)
    iteration_stage_metas.append(parse_meta)
    if not parse_feedback.ok:
        return _ValidationPass(context, feedback, iteration_stage_metas, _select_first_blocking(feedback), scenario_set, scenario_history, oracle_weak, None)

    semantic_feedback, semantic_meta = adapters.semantic(current_dsl, context)
    feedback[FeedbackSource.SEMANTIC.value] = semantic_feedback
    _append_stage(stage_records, semantic_meta)
    iteration_stage_metas.append(semantic_meta)
    if not semantic_feedback.ok:
        return _ValidationPass(context, feedback, iteration_stage_metas, _select_first_blocking(feedback), scenario_set, scenario_history, oracle_weak, None)

    design_feedback, design_meta = adapters.design(context)
    feedback[FeedbackSource.DESIGN.value] = design_feedback
    _append_stage(stage_records, design_meta)
    iteration_stage_metas.append(design_meta)
    if design_feedback.blocking_items:
        return _ValidationPass(context, feedback, iteration_stage_metas, _select_first_blocking(feedback), scenario_set, scenario_history, oracle_weak, None)

    if scenario_set is None:
        scenario_set, generated_history, weak_now, next_epoch = _run_scenario_generation_and_freeze(
            nl=nl,
            current_dsl=current_dsl,
            context=context,
            cfg=cfg,
            adapters=adapters,
            iteration=iteration,
            stage_records=stage_records,
            iteration_stage_metas=iteration_stage_metas,
            llm_interactions=llm_interactions,
            logs=logs,
            scenario_epoch=scenario_epoch,
        )
        scenario_epoch = next_epoch
        scenario_history.extend(generated_history)
        oracle_weak = oracle_weak or weak_now
    else:
        scenario_set, reused_history, weak_now = _reuse_or_check_scenario_set(
            current_dsl=current_dsl,
            scenario_set=scenario_set,
            adapters=adapters,
            iteration=iteration,
            stage_records=stage_records,
            iteration_stage_metas=iteration_stage_metas,
            logs=logs,
        )
        scenario_history.extend(reused_history)
        oracle_weak = oracle_weak or weak_now

    context.scenario_set = scenario_set
    sim_feedback, sim_meta = adapters.sim(current_dsl, scenario_set, context)
    feedback[FeedbackSource.SIM.value] = sim_feedback
    _append_stage(stage_records, sim_meta)
    iteration_stage_metas.append(sim_meta)
    if not sim_feedback.ok:
        return _ValidationPass(context, feedback, iteration_stage_metas, _select_first_blocking(feedback), scenario_set, scenario_history, oracle_weak, scenario_set.epoch)

    review_run = adapters.model_review(
        current_dsl,
        context,
        {
            "parse": parse_feedback,
            "semantic": semantic_feedback,
            "design": design_feedback,
            "sim": sim_feedback,
            "oracle_weak": oracle_weak,
        },
    )
    review_run = _append_llm_stage_run(
        run=review_run,
        expected_stage_id=StageId.SL_7_MODEL_REVIEW,
        stage_records=stage_records,
        iteration_stage_metas=iteration_stage_metas,
        llm_interactions=llm_interactions,
    )
    if _is_llm_stage_run(review_run):
        review_feedback = getattr(review_run, "feedback", None)
        if not isinstance(review_feedback, ModelReviewFeedback):
            raise TypeError("SL-7 LLMStageRun must carry ModelReviewFeedback in .feedback")
        review_meta = getattr(review_run, "stage_meta")
    else:
        review_feedback, review_meta = review_run
        _append_stage(stage_records, review_meta)
        iteration_stage_metas.append(review_meta)
    feedback[FeedbackSource.MODEL_REVIEW.value] = review_feedback

    return _ValidationPass(context, feedback, iteration_stage_metas, _select_first_blocking(feedback), scenario_set, scenario_history, oracle_weak, scenario_set.epoch)


def _selected_feedback_trace(source: str, feedback: Any, source_stage: str, *, scenario_set: ScenarioSet | None) -> dict[str, Any]:
    trace = _stage_trace(source_stage, feedback)
    trace.update(
        {
            "source": source,
            "source_stage": source_stage,
            "pre_scenario": scenario_set is None,
            "is_pre_scenario": scenario_set is None,
            "blocking": True,
        }
    )
    return trace


def _record_deterministic_iteration(state: _RunState, iteration: int, validation: _ValidationPass) -> None:
    feedback = validation.feedback
    state.deterministic_feedback["iterations"].append(
        {
            "iteration": iteration,
            "parse": _jsonable(feedback.get(FeedbackSource.PARSE.value)),
            "semantic": _jsonable(feedback.get(FeedbackSource.SEMANTIC.value)),
            "design": _jsonable(feedback.get(FeedbackSource.DESIGN.value)),
            "sim": _jsonable(feedback.get(FeedbackSource.SIM.value)),
            "model_review": _jsonable(feedback.get(FeedbackSource.MODEL_REVIEW.value)),
            "stage_ids": _stage_ids(validation.stage_metas),
            "scenario_epoch": validation.scenario_epoch,
            "oracle_weak": validation.oracle_weak,
        }
    )


def _sl9_meta(current_dsl: str, fix_plan: FixPlan | RevisedFixPlan, candidate_dsl: str) -> StageResultMeta:
    meta = _meta(StageId.SL_9_REPAIR, ok=bool(candidate_dsl), status=StageStatus.OK if candidate_dsl else StageStatus.ERROR)
    meta.input_hash = _hash_text(current_dsl)
    meta.prompt_hash = _short_hash(fix_plan)
    meta.output_hash = _hash_text(candidate_dsl)
    if not candidate_dsl:
        meta.stage_error = "repair adapter returned empty candidate DSL"
    return meta


def _run_repair_path(
    *,
    nl: str,
    cfg: FullStagedRuntimeConfig,
    adapters: FullStagedRuntimeAdapters,
    state: _RunState,
    iteration: int,
    validation: _ValidationPass,
) -> tuple[bool, dict[str, Any]]:
    assert validation.selected is not None
    source, selected_feedback, source_stage = validation.selected
    selected_trace = _selected_feedback_trace(source, selected_feedback, source_stage, scenario_set=validation.scenario_set)
    if selected_trace["pre_scenario"]:
        state.pre_scenario_repair_count += 1
    fix_plan, fix_meta = run_sd8_fix_plan(
        selected_feedback,
        source=source,
        source_stage=source_stage,
        grounding_map=cfg.grounding_map,
        before_dsl=state.current_dsl,
    )
    _append_stage(state.stage_records, fix_meta)
    repair_stage_ids = [fix_meta.stage_id]
    effective_fix_plan = fix_plan.original if isinstance(fix_plan, RevisedFixPlan) else fix_plan
    assert isinstance(effective_fix_plan, FixPlan)

    if source == FeedbackSource.DESIGN.value and isinstance(selected_feedback, DesignFeedback):
        mark_warning_repair_attempt(
            validation.context.warning_budget_state,
            [item.instance_key for item in selected_feedback.blocking_items],
        )

    request = RepairRequest(
        nl=nl,
        grounding_map=cfg.grounding_map,
        old_dsl=state.current_dsl,
        fix_plan=fix_plan,
        selected_feedback=selected_feedback,
        selected_feedback_trace=selected_trace,
        scenario_set=validation.scenario_set,
        iteration=iteration,
        repair_attempt=len(state.repair_history),
    )
    repair_run = adapters.repair(request)
    repair_run = _append_llm_stage_run(
        run=repair_run,
        expected_stage_id=StageId.SL_9_REPAIR,
        stage_records=state.stage_records,
        iteration_stage_metas=None,
        llm_interactions=state.llm_interactions,
    )
    if _is_llm_stage_run(repair_run):
        parsed_output = getattr(repair_run, "parsed_output", {}) or {}
        if not isinstance(parsed_output, dict):
            raise TypeError("SL-9 LLMStageRun parsed_output must be a dict with candidate_dsl")
        candidate_dsl = str(parsed_output.get("candidate_dsl") or "")
        repair_stage_ids.append(getattr(repair_run, "stage_meta").stage_id)
    else:
        candidate_dsl = str(repair_run or "")
        repair_meta = _sl9_meta(state.current_dsl, fix_plan, candidate_dsl)
        _append_stage(state.stage_records, repair_meta)
        repair_stage_ids.append(repair_meta.stage_id)
        state.llm_interactions.append(
            {
                "stage_id": StageId.SL_9_REPAIR.value,
                "provider": cfg.adapter_mode,
                "model_id": "explicit-adapter",
                "real_llm_provider_api": False,
                "prompt_template_version": "pr-b1-repair-adapter.v1",
                "input_hash": _hash_text(state.current_dsl),
                "prompt_hash": repair_meta.prompt_hash,
                "raw_output_hash": repair_meta.output_hash,
                "raw_output": candidate_dsl,
                "parsed_output": {"candidate_dsl": candidate_dsl},
                "schema_validation_ok": bool(candidate_dsl),
                "note": "PR-B1 deterministic runtime uses an explicitly injected repair adapter; no provider/env call.",
            }
        )
    request.candidate_dsl = candidate_dsl

    review_request = RepairRequest(
        nl=nl,
        grounding_map=cfg.grounding_map,
        old_dsl=state.current_dsl,
        fix_plan=effective_fix_plan,
        selected_feedback=selected_feedback,
        selected_feedback_trace=selected_trace,
        scenario_set=validation.scenario_set,
        candidate_dsl=candidate_dsl,
        iteration=iteration,
        repair_attempt=len(state.repair_history),
    )
    repair_review, repair_review_meta = adapters.repair_review(review_request)
    _append_stage(state.stage_records, repair_review_meta)
    repair_stage_ids.append(repair_review_meta.stage_id)

    if repair_review.ok and adapters.delta_review is not None:
        delta_feedback_authoritative = False
        delta_run = adapters.delta_review(review_request, repair_review)
        delta_run = _append_llm_stage_run(
            run=delta_run,
            expected_stage_id=StageId.SL_10B_DELTA_REVIEW,
            stage_records=state.stage_records,
            iteration_stage_metas=None,
            llm_interactions=state.llm_interactions,
        )
        if _is_llm_stage_run(delta_run):
            delta_payload = getattr(delta_run, "parsed_output", {}) or {}
            delta_feedback = getattr(delta_run, "feedback", None)
            if isinstance(delta_feedback, RepairReviewFeedback):
                repair_review = delta_feedback
                delta_feedback_authoritative = True
            repair_stage_ids.append(getattr(delta_run, "stage_meta").stage_id)
        else:
            delta_payload, delta_meta = delta_run
            _append_stage(state.stage_records, delta_meta)
            repair_stage_ids.append(delta_meta.stage_id)
        repair_review.delta_review = delta_payload
        decision = str(delta_payload.get("decision", "accept"))
        if decision in {"reject", "revise"} and (not delta_feedback_authoritative or not repair_review.ok):
            repair_review.ok = False
            repair_review.target_resolved = False
            if repair_review.local_rejection is None:
                from method.schema import RepairRejection

                repair_review.local_rejection = RepairRejection(
                    rejected_by_stage=StageId.SL_10B_DELTA_REVIEW.value,
                    reason=f"delta_review_{decision}",
                    drift_risk=str(delta_payload.get("drift_risk", "major")),  # type: ignore[arg-type]
                    evidence=_jsonable(delta_payload.get("drift_evidence", [])),
                )

    accepted = bool(repair_review.ok)
    if accepted:
        sc11_meta = _meta(StageId.SC_11_ACCEPT_CANDIDATE, ok=True)
    else:
        sc11_meta = _meta(StageId.SC_11_ACCEPT_CANDIDATE, ok=False, status=StageStatus.FAIL)
    _append_stage(state.stage_records, sc11_meta)
    repair_stage_ids.append(sc11_meta.stage_id)

    repair_payload = {
        "iteration": iteration,
        "selected_feedback": selected_trace,
        "plan_kind": "RevisedFixPlan" if isinstance(fix_plan, RevisedFixPlan) else "FixPlan",
        "fix_plan": _jsonable(effective_fix_plan),
        "candidate_dsl": candidate_dsl,
        "candidate_dsl_hash": _hash_text(candidate_dsl),
        "repair_review": _jsonable(repair_review),
        "accepted": accepted,
        "repair_stage_ids": list(repair_stage_ids),
        "scenario_set_id": validation.scenario_set.scenario_set_id if validation.scenario_set is not None else None,
    }
    state.repair_history.append(repair_payload)

    iteration_patch = {
        "selected_feedback": selected_trace,
        "repair_stage_ids": list(repair_stage_ids),
        "repair_review": _jsonable(repair_review),
        "accepted_candidate": accepted,
    }
    if accepted:
        state.current_dsl = candidate_dsl
        iteration_patch["exit_reason"] = "candidate_accepted_for_next_full_pass"
    else:
        state.final_record_status = "rejected"
        state.result_status = "not_converged"
        state.error_message = repair_review.local_rejection.reason if repair_review.local_rejection is not None else "repair review rejected candidate"
        iteration_patch["exit_reason"] = state.error_message
    return accepted, iteration_patch


def _eligibility(cfg: FullStagedRuntimeConfig, *, record_status: str, oracle_weak: bool) -> tuple[bool, str | None, str | None]:
    if record_status != "success":
        return False, None, "verdict_not_success"
    reasons: list[str] = []
    if oracle_weak:
        reasons.append("weak_oracle")
    if not cfg.allow_main_result_eligible:
        reasons.append("deterministic_runtime_not_default_real_adapter")
    if reasons:
        return False, None, ";".join(reasons)
    return True, "success_full_pass_with_non_weak_oracle", None


def _build_record(
    *,
    cfg: FullStagedRuntimeConfig,
    nl: str,
    state: _RunState,
) -> AgentLoopRunRecord:
    main_eligible, inclusion_reason, exclusion_reason = _eligibility(
        cfg,
        record_status=state.final_record_status,
        oracle_weak=state.oracle_weak,
    )
    return AgentLoopRunRecord(
        schema_version=RUN_RECORD_SCHEMA_VERSION,
        run_id=state.run_id,
        created_at=state.run_started_at,
        status=state.final_record_status,  # type: ignore[arg-type]
        input_bundle={
            "nl": nl,
            "nl_hash": _hash_text(nl),
            "initial_dsl_hash": _hash_text(cfg.initial_dsl),
            "path_context": _jsonable(cfg.path_context),
            "pr_b1_control_flow_only": True,
        },
        run_config={
            "max_iterations": cfg.max_iterations,
            "scenario_max_retries": cfg.scenario_max_retries,
            "policy_profile": cfg.policy_profile,
            "adapter_mode": cfg.adapter_mode,
            "allow_main_result_eligible": cfg.allow_main_result_eligible,
            "real_llm_provider_api": False,
            "default_loop_config_entry_integrated": False,
        },
        environment=_environment(cfg),
        stage_graph=_planned_stage_graph(state.stage_records),
        stage_records=[_jsonable(meta) for meta in state.stage_records],
        iteration_records=_jsonable(state.iteration_records),
        llm_interactions=_jsonable(state.llm_interactions),
        deterministic_feedback=_jsonable(state.deterministic_feedback),
        repair_history=_jsonable(state.repair_history),
        scenario_history=_jsonable(state.scenario_history),
        final_artifacts={
            "final_dsl": state.current_dsl,
            "final_dsl_hash": _hash_text(state.current_dsl),
            "verdict": state.final_verdict,
            "verdict_source_stage_id": state.verdict_source_stage_id,
            "verdict_reason": state.verdict_reason,
            "agent_loop_result_status": state.result_status,
            "oracle_weak": state.oracle_weak,
            "main_result_eligible": main_eligible,
            "inclusion_reason": inclusion_reason,
            "exclusion_reason": exclusion_reason,
            "error_message": state.error_message,
        },
        logs=_jsonable(state.logs),
        replay_index={
            "stage_by_index": {str(i): meta.stage_id for i, meta in enumerate(state.stage_records)},
            "iteration_count": len(state.iteration_records),
            "repair_count": len(state.repair_history),
            "scenario_history_count": len(state.scenario_history),
            "pre_scenario_repair_count": state.pre_scenario_repair_count,
            "verdict": state.final_verdict,
            "verdict_source_stage_id": state.verdict_source_stage_id,
        },
    )


def run_full_staged_deterministic_runtime(
    nl: str,
    config: FullStagedRuntimeConfig,
    *,
    adapters: FullStagedRuntimeAdapters,
) -> AgentLoopResult:
    """Run the PR-B1 deterministic staged control-flow driver.

    A repair candidate accepted by ``SD-10``/optional ``SL-10B`` is only copied
    into ``current_dsl`` and then revalidated from ``SD-2`` in the next pass.
    Final success is emitted solely by a later full pass with no blocking
    feedback.
    """
    run_id = config.run_id or "pr-b1-" + hashlib.sha256(f"{nl}\n{config.initial_dsl}".encode("utf-8")).hexdigest()[:12]
    state = _RunState(run_id=run_id, run_started_at=_utc_now(), current_dsl=config.initial_dsl)
    _append_stage(state.stage_records, _meta(StageId.SC_0_START, ok=True))

    if adapters.initial_modeling is not None:
        try:
            initial_context = StageContext(nl=nl, current_dsl=state.current_dsl, grounding_map=config.grounding_map)
            initial_run = adapters.initial_modeling(nl, initial_context)
            initial_run = _append_llm_stage_run(
                run=initial_run,
                expected_stage_id=StageId.SL_1_INITIAL_MODELING,
                stage_records=state.stage_records,
                iteration_stage_metas=None,
                llm_interactions=state.llm_interactions,
            )
            if _is_llm_stage_run(initial_run):
                parsed_output = getattr(initial_run, "parsed_output", {}) or {}
                if isinstance(parsed_output, dict) and parsed_output.get("candidate_dsl"):
                    state.current_dsl = str(parsed_output["candidate_dsl"])
            elif isinstance(initial_run, str) and initial_run:
                state.current_dsl = initial_run
        except _LLMRetryExhausted as exc:
            _mark_retry_exhausted(state, exc)

    if config.max_iterations == 0 and state.verdict_source_stage_id is None:
        _mark_sc12_verdict(
            state,
            verdict="not_converged",
            source_stage_id=StageId.SC_0_START.value,
            reason="max_iterations=0 leaves no SD-2 validation budget",
            record_status="budget_exhausted",
            result_status="not_converged",
            stage_ok=False,
            stage_status=StageStatus.FAIL,
        )

    iterations = config.max_iterations
    for iteration in range(iterations):
        if state.verdict_source_stage_id is not None:
            break
        iteration_stage_start = len(state.stage_records)
        try:
            validation = _run_validation_pass(
                nl=nl,
                current_dsl=state.current_dsl,
                cfg=config,
                adapters=adapters,
                scenario_set=state.scenario_set,
                scenario_epoch=state.scenario_epoch,
                oracle_weak=state.oracle_weak,
                iteration=iteration,
                stage_records=state.stage_records,
                logs=state.logs,
                llm_interactions=state.llm_interactions,
            )
        except _LLMRetryExhausted as exc:
            _mark_retry_exhausted(state, exc)
            state.iteration_records.append(
                {
                    "iteration": iteration,
                    "dsl_hash": _hash_text(state.current_dsl),
                    "stage_ids": _stage_ids(state.stage_records[iteration_stage_start:]),
                    "selected_feedback": None,
                    "scenario_epoch": None,
                    "oracle_weak": state.oracle_weak,
                    "scenario_set_id": state.scenario_set.scenario_set_id if state.scenario_set is not None else None,
                    "exit_reason": state.verdict_reason,
                }
            )
            break
        state.scenario_set = validation.scenario_set
        if validation.scenario_set is not None:
            state.scenario_epoch = max(state.scenario_epoch, validation.scenario_set.epoch + 1)
        state.oracle_weak = validation.oracle_weak
        state.scenario_history.extend(validation.scenario_history)
        _record_deterministic_iteration(state, iteration, validation)

        selected_trace = None
        if validation.selected is not None:
            source, selected_feedback, source_stage = validation.selected
            selected_trace = _selected_feedback_trace(source, selected_feedback, source_stage, scenario_set=validation.scenario_set)

        iteration_record: dict[str, Any] = {
            "iteration": iteration,
            "dsl_hash": _hash_text(state.current_dsl),
            "stage_ids": _stage_ids(validation.stage_metas),
            "selected_feedback": selected_trace,
            "scenario_epoch": validation.scenario_epoch,
            "oracle_weak": state.oracle_weak,
            "scenario_set_id": validation.scenario_set.scenario_set_id if validation.scenario_set is not None else None,
        }

        if validation.selected is None:
            source_stage_id = validation.stage_metas[-1].stage_id if validation.stage_metas else StageId.SC_0_START.value
            _mark_sc12_verdict(
                state,
                verdict="success",
                source_stage_id=source_stage_id,
                reason="full_pass_all_required_feedback_ok",
            )
            iteration_record["exit_reason"] = "full_pass_all_required_feedback_ok"
            state.iteration_records.append(iteration_record)
            break

        try:
            accepted, repair_patch = _run_repair_path(
                nl=nl,
                cfg=config,
                adapters=adapters,
                state=state,
                iteration=iteration,
                validation=validation,
            )
        except _LLMRetryExhausted as exc:
            _mark_retry_exhausted(state, exc)
            iteration_record["exit_reason"] = state.verdict_reason
            iteration_record["repair_stage_ids"] = _stage_ids(state.stage_records[iteration_stage_start:])[len(iteration_record["stage_ids"]) :]
            state.iteration_records.append(iteration_record)
            break
        iteration_record.update(repair_patch)
        if not accepted:
            reason = state.error_message or "repair review rejected candidate"
            _mark_sc12_verdict(
                state,
                verdict="not_converged",
                source_stage_id=StageId.SC_11_ACCEPT_CANDIDATE.value,
                reason=reason,
                record_status="rejected",
                result_status="not_converged",
                stage_ok=False,
                stage_status=StageStatus.FAIL,
            )
            state.iteration_records.append(iteration_record)
            break
        if iteration + 1 >= config.max_iterations:
            reason = f"SC-11 budget gate blocked SD-2 revalidation: iter+1={iteration + 1} >= max_iterations={config.max_iterations}"
            _mark_sc12_verdict(
                state,
                verdict="not_converged",
                source_stage_id=StageId.SC_11_ACCEPT_CANDIDATE.value,
                reason=reason,
                record_status="budget_exhausted",
                result_status="not_converged",
                stage_ok=False,
                stage_status=StageStatus.FAIL,
            )
            iteration_record["exit_reason"] = reason
            iteration_record["budget_gate"] = {
                "source_stage_id": StageId.SC_11_ACCEPT_CANDIDATE.value,
                "iter_plus_one": iteration + 1,
                "max_iterations": config.max_iterations,
                "next_stage_allowed": False,
            }
            state.iteration_records.append(iteration_record)
            break
        state.iteration_records.append(iteration_record)
        # Accepted candidate deliberately falls through to the next loop
        # iteration, which starts from SD-2.  No success may be emitted here.
    else:
        if state.verdict_source_stage_id is None:
            _mark_sc12_verdict(
                state,
                verdict="not_converged",
                source_stage_id=StageId.SC_11_ACCEPT_CANDIDATE.value,
                reason="max_iterations exhausted",
                record_status="budget_exhausted",
                result_status="not_converged",
                stage_ok=False,
                stage_status=StageStatus.FAIL,
            )

    if state.final_record_status not in {"success", "rejected", "budget_exhausted", "error", "invalid"}:
        state.final_record_status = "failed"
        state.final_verdict = "not_converged"
        state.result_status = "not_converged"
        if state.error_message is None:
            state.error_message = "runtime exited without convergence"

    _append_stage(state.stage_records, _meta(StageId.SC_13_TRACE_AUDIT, ok=True))

    result = AgentLoopResult(
        final_dsl=state.current_dsl,
        status=state.result_status,  # type: ignore[arg-type]
        error_message=state.error_message,
        llm_model="none-pr-b1-explicit-adapters",
        run_record_id=run_id,
    )

    if config.write_run_record:
        record = _build_record(cfg=config, nl=nl, state=state)
        path = write_agent_loop_run_record(record, agent_loop_run_record_path(config.output_dir, run_id))
        result.run_record_path = str(path)
    return result
