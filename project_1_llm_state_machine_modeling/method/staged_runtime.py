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
import importlib.metadata
import platform
import re
import subprocess
import uuid
import difflib
from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from method.run_record import agent_loop_run_record_path, write_agent_loop_run_record
from method.schema import (
    AgentLoopResult,
    AgentLoopRunRecord,
    BudgetState,
    DesignFeedback,
    FixPlan,
    FixLogEntry,
    FixRequest,
    FixRequestBatch,
    FixRequestDecision,
    GroundedElement,
    GroundingMap,
    ModelReviewFeedback,
    ParseFeedback,
    RepairReviewFeedback,
    RepairRejection,
    RevisedFixPlan,
    ReviewRunMeta,
    SL9RepairDecisionOutput,
    SL10RepairReviewOutput,
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

RUN_RECORD_SCHEMA_VERSION = "pr-c.default-full-staged-runtime.v1"


def _identifier_token_present(text: str, token: str) -> bool:
    if not token:
        return False
    return re.search(rf"(?<![A-Za-z0-9_]){re.escape(token)}(?![A-Za-z0-9_])", text) is not None


def _diagnostic_variable_role_summary(nl: str, selected_feedback: Any) -> dict[str, Any]:
    """Build sample-agnostic variable-role context for repair prompts.

    This is intentionally advisory: it summarizes variables mentioned by
    diagnostics and generic SD-4 rationales without case IDs, benchmark names,
    or domain-specific hard-coded lexicons. SL-9 may use it to avoid inventing
    internal plant dynamics for variables already justified as external inputs,
    while SL-10 receives the complete ledger and remains the authority for
    repair acceptance/rework.
    """

    if not isinstance(selected_feedback, DesignFeedback):
        return {}
    variables: dict[str, dict[str, Any]] = {}
    for item in [*selected_feedback.blocking_items, *selected_feedback.advisory_items, *selected_feedback.info_items]:
        refs = item.refs or {}
        names: set[str] = set()
        var_name = refs.get("var_name")
        if var_name is not None:
            names.add(str(var_name))
        guard_vars = refs.get("guard_vars")
        if isinstance(guard_vars, list):
            names.update(str(name) for name in guard_vars)
        for name in sorted(names):
            entry = variables.setdefault(
                name,
                {
                    "diagnostic_codes": [],
                    "diagnostic_instance_keys": [],
                    "role_hint": "unknown",
                    "rationales": [],
                    "nl_token_present": _identifier_token_present(nl, name),
                },
            )
            entry["diagnostic_codes"].append(item.code)
            entry["diagnostic_instance_keys"].append(item.instance_key)
            if item.rationale:
                entry["rationales"].append(item.rationale)
                if "external" in item.rationale.lower():
                    entry["role_hint"] = "external_input_candidate"
    if not variables:
        return {}
    return {
        "source": "SD-4 diagnostic refs and generic NL external-input rationale",
        "policy": (
            "Advisory only. Do not invent writes for external_input_candidate "
            "variables unless NL explicitly gives update semantics; add "
            "meaningful NL-grounded writes only for internal state variables."
        ),
        "variables": variables,
    }


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
    """Input shared by PR-E1 ``SL-9`` repair and ``SL-10`` review adapters."""

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
    warning_budget_state: dict[str, BudgetState] = field(default_factory=dict)
    fix_request_batch: FixRequestBatch | None = None
    fix_log: list[dict[str, Any]] = field(default_factory=list)
    sl9_decision: SL9RepairDecisionOutput | None = None
    local_check_evidence: dict[str, Any] = field(default_factory=dict)
    diff_summary: dict[str, Any] = field(default_factory=dict)
    rework_locked: bool = False


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
    resolved_loop_config: dict[str, Any] = field(default_factory=dict)
    run_config_extra: dict[str, Any] = field(default_factory=dict)
    environment_extra: dict[str, Any] = field(default_factory=dict)
    redaction_report: list[dict[str, Any]] = field(default_factory=list)
    real_llm_provider_api: bool = False
    provider_config_read: bool = False
    provider_model_redacted: str = ""
    default_loop_config_entry_integrated: bool = False

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
SL10ReviewAdapter = Callable[[RepairRequest, RepairReviewFeedback], Any]
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
    sl10_review: SL10ReviewAdapter | None = None
    delta_review: DeltaReviewAdapter | None = None
    initial_modeling: InitialModelingAdapter | None = None


def build_full_staged_runtime_adapters(
    *,
    scenario_generate: ScenarioGenerateAdapter,
    repair: RepairAdapter,
    model_review: ModelReviewAdapter,
    policy_profile: str = "experiment_default",
    sl10_review: SL10ReviewAdapter | None = None,
    delta_review: DeltaReviewAdapter | None = None,
) -> FullStagedRuntimeAdapters:
    """Build PR-B1 adapters from existing deterministic SD tools.

    ``SL-5`` / ``SL-7`` / ``SL-9`` remain explicit callables so this helper does
    not hide fake providers or read provider configuration.  The deterministic
    stages are wired to the #14 SD tool façade.  PR-E1 keeps those local
    checks as evidence for ``SL-10`` instead of treating them as the final
    semantic judge.
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
            warning_budget_state=request.warning_budget_state,
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
        sl10_review=sl10_review,
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
    fix_log: list[dict[str, Any]] = field(default_factory=list)
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
    redaction_report: list[dict[str, Any]] = field(default_factory=list)
    pending_repair_rejection: RepairRejection | None = None
    pending_original_fix_plan: FixPlan | None = None
    pending_rework_request: dict[str, Any] | None = None
    warning_budget_state: dict[str, BudgetState] = field(default_factory=dict)


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


def _package_version(name: str) -> str:
    try:
        return importlib.metadata.version(name)
    except Exception:
        return "unknown"


def _environment(cfg: FullStagedRuntimeConfig) -> dict[str, Any]:
    resolved = dict(cfg.resolved_loop_config or {})
    provider_mode = str(resolved.get("llm_provider_mode") or cfg.adapter_mode)
    payload = {
        "git_commit": _git_commit(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "runner": "method.staged_runtime.run_full_staged_deterministic_runtime",
        "adapter_mode": cfg.adapter_mode,
        "provider_mode": provider_mode,
        "real_llm_provider_api": bool(cfg.real_llm_provider_api),
        "provider_config_read": bool(cfg.provider_config_read),
        "provider_model_redacted": cfg.provider_model_redacted or "<unknown>",
        "pyfcstm_version": _package_version("pyfcstm"),
        "dependency_versions": {
            "python": platform.python_version(),
            "pyfcstm": _package_version("pyfcstm"),
            "openai": _package_version("openai"),
        },
        "config_hash": resolved.get("condition_hash"),
        "resolved_config": _jsonable(resolved),
    }
    payload.update(_jsonable(cfg.environment_extra))
    return payload


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
    redaction_report = list(getattr(run, "redaction_report", []) or [])
    if redaction_report:
        interaction["redaction_report"] = _jsonable(redaction_report)
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
                "oracle_weak": getattr(feedback, "oracle_weak", False),
                "weak_oracle_reason": getattr(feedback, "weak_oracle_reason", ""),
                "weak_oracle_evidence": _jsonable(getattr(feedback, "weak_oracle_evidence", {})),
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
    if isinstance(sim, SimFeedback) and not sim.ok and not getattr(sim, "oracle_weak", False):
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
        weak = retry_exhausted or bool(selected_coverage.get("oracle_weak"))
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
    nl: str,
    current_dsl: str,
    context: StageContext,
    cfg: FullStagedRuntimeConfig,
    scenario_set: ScenarioSet,
    adapters: FullStagedRuntimeAdapters,
    iteration: int,
    stage_records: list[StageResultMeta],
    iteration_stage_metas: list[StageResultMeta],
    llm_interactions: list[dict[str, Any]],
    logs: list[dict[str, Any]],
) -> tuple[ScenarioSet, list[dict[str, Any]], bool, int]:
    coverage, coverage_meta = adapters.scenario_coverage(current_dsl, list(scenario_set.scenarios))
    _append_stage(stage_records, coverage_meta)
    iteration_stage_metas.append(coverage_meta)

    gap = bool(coverage.get("coverage_gap"))
    history = [
        _scenario_history_item(
            iteration=iteration,
            attempt_index=0,
            scenarios=list(scenario_set.scenarios),
            coverage=coverage,
            coverage_meta=coverage_meta,
            retry_exhausted=False,
            oracle_weak=False,
        )
    ]
    history[0]["scenario_set_id"] = scenario_set.scenario_set_id
    history[0]["epoch"] = scenario_set.epoch
    history[0]["reused_frozen_oracle"] = True

    if not gap:
        freeze_meta = _meta(StageId.SC_5F_SCENARIO_FREEZE, ok=True)
        freeze_meta.input_hash = _hash_text(current_dsl)
        freeze_meta.output_hash = _hash_text(scenario_set.scenario_set_id)
        _append_stage(stage_records, freeze_meta)
        iteration_stage_metas.append(freeze_meta)
        return scenario_set, history, False, scenario_set.epoch + 1

    coverage_directive: Any | None = coverage.get("retry_directive") or {"retry_reason": "frozen_scenario_coverage_gap"}
    previous_scenarios = list(scenario_set.scenarios)
    selected_scenarios = list(scenario_set.scenarios)
    selected_coverage = dict(coverage)
    weak = cfg.scenario_max_retries == 0 or bool(selected_coverage.get("oracle_weak"))
    next_epoch = scenario_set.epoch + 1

    logs.append(
        {
            "ts": _utc_now(),
            "level": "warning",
            "event": "frozen_scenario_coverage_gap_targeted_retry",
            "iteration": iteration,
            "scenario_set_id": scenario_set.scenario_set_id,
            "scenario_max_retries": cfg.scenario_max_retries,
        }
    )

    for retry_index in range(1, cfg.scenario_max_retries + 1):
        request = ScenarioGenerationRequest(
            nl=nl,
            current_dsl=current_dsl,
            context=context,
            attempt_index=retry_index,
            coverage_directive=coverage_directive,
            previous_scenarios=previous_scenarios,
            scenario_epoch=next_epoch,
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

        retry_coverage, retry_meta = adapters.scenario_coverage(current_dsl, scenarios)
        _append_stage(stage_records, retry_meta)
        iteration_stage_metas.append(retry_meta)
        selected_scenarios = scenarios
        selected_coverage = dict(retry_coverage)
        retry_gap = bool(retry_coverage.get("coverage_gap"))
        retry_exhausted = retry_gap and retry_index >= cfg.scenario_max_retries
        weak = retry_exhausted or bool(selected_coverage.get("oracle_weak"))
        history.append(
            {
                **_scenario_history_item(
                    iteration=iteration,
                    attempt_index=retry_index,
                    scenarios=scenarios,
                    coverage=retry_coverage,
                    coverage_meta=retry_meta,
                    retry_exhausted=retry_exhausted,
                    oracle_weak=weak,
                ),
                "targeted_retry_after_frozen_gap": True,
                "previous_scenario_set_id": scenario_set.scenario_set_id,
            }
        )
        if not retry_gap:
            break
        coverage_directive = retry_coverage.get("retry_directive") or {"retry_reason": "frozen_scenario_coverage_gap"}
        previous_scenarios = scenarios

    if weak:
        selected_coverage = {
            **selected_coverage,
            "oracle_weak": True,
            "weak_oracle_reason": "frozen_scenario_coverage_retry_exhausted",
        }
        logs.append(
            {
                "ts": _utc_now(),
                "level": "warning",
                "event": "frozen_scenario_coverage_retry_exhausted",
                "iteration": iteration,
                "previous_scenario_set_id": scenario_set.scenario_set_id,
                "scenario_max_retries": cfg.scenario_max_retries,
            }
        )

    refreshed_set, freeze_meta = freeze_scenario_set(
        selected_scenarios,
        source_dsl_hash=_hash_text(current_dsl),
        source_inspect_hash=_short_hash(context.inspect_json) if context.inspect_json is not None else "",
        source_grounding_hash=_short_hash(cfg.grounding_map) if cfg.grounding_map is not None else None,
        coverage_report=selected_coverage,
        epoch=next_epoch,
    )
    refreshed_set.coverage_report["oracle_weak"] = weak
    _append_stage(stage_records, freeze_meta)
    iteration_stage_metas.append(freeze_meta)
    if history:
        history[-1]["scenario_set_id"] = refreshed_set.scenario_set_id
        history[-1]["epoch"] = refreshed_set.epoch
        history[-1]["oracle_weak"] = weak
    return refreshed_set, history, weak, refreshed_set.epoch + 1


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
    warning_budget_state: dict[str, BudgetState] | None = None,
) -> _ValidationPass:
    context = StageContext(
        nl=nl,
        current_dsl=current_dsl,
        grounding_map=cfg.grounding_map,
        scenario_set=scenario_set,
        warning_budget_state=warning_budget_state or {},
    )
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
        scenario_set, reused_history, weak_now, next_epoch = _reuse_or_check_scenario_set(
            nl=nl,
            current_dsl=current_dsl,
            context=context,
            cfg=cfg,
            scenario_set=scenario_set,
            adapters=adapters,
            iteration=iteration,
            stage_records=stage_records,
            iteration_stage_metas=iteration_stage_metas,
            llm_interactions=llm_interactions,
            logs=logs,
        )
        scenario_epoch = next_epoch
        scenario_history.extend(reused_history)
        oracle_weak = oracle_weak or weak_now

    context.scenario_set = scenario_set
    sim_feedback, sim_meta = adapters.sim(current_dsl, scenario_set, context)
    feedback[FeedbackSource.SIM.value] = sim_feedback
    _append_stage(stage_records, sim_meta)
    iteration_stage_metas.append(sim_meta)
    if not sim_feedback.ok:
        if getattr(sim_feedback, "oracle_weak", False):
            logs.append(
                {
                    "ts": _utc_now(),
                    "level": "warning",
                    "event": "sim_failed_but_oracle_weak",
                    "iteration": iteration,
                    "weak_oracle_reason": getattr(sim_feedback, "weak_oracle_reason", ""),
                    "weak_oracle_evidence": _jsonable(getattr(sim_feedback, "weak_oracle_evidence", {})),
                }
            )
            oracle_weak = True
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


def _request_id(*, iteration: int, source_stage: str, feedback_id: str, index: int) -> str:
    digest = hashlib.sha256(f"{iteration}:{source_stage}:{feedback_id}:{index}".encode("utf-8")).hexdigest()[:10]
    safe_stage = source_stage.replace("-", "").lower()
    return f"fixreq-{iteration}-{safe_stage}-{index}-{digest}"


def _fix_request_batch_from_plan(
    *,
    iteration: int,
    source: str,
    source_stage: str,
    selected_trace: dict[str, Any],
    fix_plan: FixPlan | RevisedFixPlan,
    effective_fix_plan: FixPlan,
) -> FixRequestBatch:
    evidence_items = list(effective_fix_plan.evidence or [])
    diagnostic_ids = list(effective_fix_plan.diagnostic_ids or [])
    n_requests = max(1, len(evidence_items), len(diagnostic_ids))
    requests: list[FixRequest] = []
    for index in range(n_requests):
        feedback_id = diagnostic_ids[index] if index < len(diagnostic_ids) else effective_fix_plan.source_feedback_id
        evidence = [evidence_items[index]] if index < len(evidence_items) else list(evidence_items)
        # ``blocking_warning`` is a conservative deterministic block: SL-9 may
        # reject/waive it with an auditable rationale so the next pass can
        # continue after the warning budget is consumed. Parse/semantic/sim and
        # model-review failures remain hard requests.
        hard_block = effective_fix_plan.severity in {"error", "review_fail", "sim_fail"}
        requests.append(
            FixRequest(
                request_id=_request_id(
                    iteration=iteration,
                    source_stage=source_stage,
                    feedback_id=str(feedback_id or effective_fix_plan.source_feedback_id),
                    index=index,
                ),
                target=effective_fix_plan.target,
                source_stage=effective_fix_plan.source_stage,
                source_feedback_id=str(feedback_id or effective_fix_plan.source_feedback_id),
                severity=effective_fix_plan.severity,
                hard_block=hard_block,
                waiver_allowed=not hard_block,
                problem_summary=effective_fix_plan.problem_summary,
                evidence=evidence,
                suggested_fix_hints=list(effective_fix_plan.suggested_fix_hints or []),
                recommended_strategy=list(effective_fix_plan.recommended_strategy or []),
                forbidden_edits=list(effective_fix_plan.forbidden_edits or []),
                required_preserve_element_ids=list(effective_fix_plan.required_preserve_element_ids or []),
                local_check_required=True,
                legacy_fix_plan=_jsonable(effective_fix_plan),
            )
        )
    return FixRequestBatch(
        batch_id=f"fixbatch-{iteration}-{_hash_text(repr(_jsonable(selected_trace)))[:18].replace(':', '-')}",
        iteration=iteration,
        source=source,
        source_stage=source_stage,
        requests=requests,
        selected_feedback_trace=_jsonable(selected_trace),
        before_dsl_hash=effective_fix_plan.before_dsl_hash,
        legacy_plan_kind="RevisedFixPlan" if isinstance(fix_plan, RevisedFixPlan) else "FixPlan",
    )


def _dsl_diff_summary(old_dsl: str, candidate_dsl: str) -> dict[str, Any]:
    diff = list(
        difflib.unified_diff(
            old_dsl.splitlines(),
            candidate_dsl.splitlines(),
            fromfile="old.dsl",
            tofile="candidate.dsl",
            lineterm="",
        )
    )
    return {
        "old_dsl_hash": _hash_text(old_dsl),
        "candidate_dsl_hash": _hash_text(candidate_dsl),
        "n_diff_lines": len(diff),
        "diff_excerpt": diff[:120],
    }


def _default_sl9_output(
    *,
    batch: FixRequestBatch,
    candidate_dsl: str,
    rework_locked: bool = False,
) -> SL9RepairDecisionOutput:
    return SL9RepairDecisionOutput(
        decisions=[
            FixRequestDecision(
                request_id=request.request_id,
                decision="accept",
                rationale=(
                    "default_accept_for_legacy_dsl_only_sl9_output"
                    if not rework_locked
                    else "rework_locked_request_must_continue_repair"
                ),
                accepted_edit_intent=[request.problem_summary] if request.problem_summary else [],
                rework_locked=rework_locked,
            )
            for request in batch.requests
        ],
        candidate_dsl=candidate_dsl,
        repair_rationale=["SL-9 returned DSL-only output; runtime accepted all current hard requests for compatibility."],
        diff_summary={},
    )


def _coerce_sl9_decision_output(
    parsed_output: Any,
    *,
    batch: FixRequestBatch,
    candidate_dsl: str,
    rework_locked: bool,
) -> SL9RepairDecisionOutput:
    if isinstance(parsed_output, SL9RepairDecisionOutput):
        output = parsed_output
    elif isinstance(parsed_output, dict) and isinstance(parsed_output.get("decisions"), list):
        output = SL9RepairDecisionOutput(
            decisions=[
                decision if isinstance(decision, FixRequestDecision) else FixRequestDecision(**dict(decision))
                for decision in parsed_output.get("decisions", [])
            ],
            candidate_dsl=str(parsed_output.get("candidate_dsl") or candidate_dsl),
            repair_rationale=[str(item) for item in parsed_output.get("repair_rationale", [])],
            diff_summary=dict(parsed_output.get("diff_summary", {}) or {}),
        )
    else:
        output = _default_sl9_output(batch=batch, candidate_dsl=candidate_dsl, rework_locked=rework_locked)

    known = {request.request_id for request in batch.requests}
    existing = {decision.request_id for decision in output.decisions}
    for missing in sorted(known - existing):
        output.decisions.append(
            FixRequestDecision(
                request_id=missing,
                decision="accept" if rework_locked else "reject",
                rationale="runtime_filled_missing_sl9_decision",
                rework_locked=rework_locked,
            )
        )
    if rework_locked:
        for decision in output.decisions:
            decision.rework_locked = True
            if decision.decision == "reject":
                decision.decision = "accept"
                decision.rationale = (
                    (decision.rationale + "; ") if decision.rationale else ""
                ) + "rework_locked_request_must_not_be_rejected_again"
        if not output.accepted_request_ids and output.decisions:
            output.decisions[0].decision = "accept"
            output.decisions[0].rationale = "rework_locked_request_must_not_be_rejected_again"
            output.decisions[0].rework_locked = True
    if not output.candidate_dsl:
        output.candidate_dsl = candidate_dsl
    return output


def _local_repair_check_evidence(
    *,
    repair_review: RepairReviewFeedback,
    repair_review_meta: StageResultMeta,
) -> dict[str, Any]:
    return {
        "stage_id": StageId.SL_10_REPAIR_REVIEW.value,
        "legacy_local_check_stage_id": StageId.SD_10_REPAIR_REVIEW.value,
        "local_check_note": "PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.",
        "meta": _jsonable(repair_review_meta),
        "repair_review_feedback": _jsonable(repair_review),
    }


def _default_sl10_output_from_local_checks(
    *,
    local_review: RepairReviewFeedback,
    local_evidence: dict[str, Any],
) -> SL10RepairReviewOutput:
    decision = "pass" if local_review.ok else "rework"
    rejection = local_review.local_rejection
    review_meta = ReviewRunMeta(
        provider="local-check-evidence-fallback",
        model_id="none",
        prompt_template_version="sl10-local-fallback.v1",
        schema_validation_ok=True,
        parsed_schema_version="SL10RepairReviewOutput.local_fallback.v1",
        failure_policy="audit_only",
        replay_key="SL-10:local-fallback",
    )
    return SL10RepairReviewOutput(
        ok=local_review.ok,
        decision=decision,
        target_resolved=local_review.target_resolved,
        regression_detected=local_review.regression_detected,
        drift_risk=local_review.drift_risk,
        rework_instructions=(
            [rejection.reason] if rejection is not None and rejection.reason else []
        ),
        evidence=(
            [{"summary": rejection.reason, "evidence": _jsonable(rejection.evidence)}]
            if rejection is not None
            else [{"summary": "local checks passed"}]
        ),
        local_check_evidence=local_evidence,
        review_meta=review_meta,
        meta=_meta(StageId.SL_10_REPAIR_REVIEW, ok=local_review.ok, status=StageStatus.OK if local_review.ok else StageStatus.FAIL),
    )


def _repair_review_from_sl10(sl10: SL10RepairReviewOutput, *, local_review: RepairReviewFeedback) -> RepairReviewFeedback:
    rejection = None
    if not sl10.ok:
        rejection = RepairRejection(
            rejected_by_stage=StageId.SL_10_REPAIR_REVIEW.value,
            reason="; ".join(sl10.rework_instructions) or f"sl10_{sl10.decision}",
            target_resolved=sl10.target_resolved,
            regression_detected=sl10.regression_detected,
            drift_risk=sl10.drift_risk,
            evidence=sl10.evidence,
        )
    return RepairReviewFeedback(
        ok=sl10.ok,
        target_resolved=sl10.target_resolved,
        regression_detected=sl10.regression_detected,
        drift_risk=sl10.drift_risk,
        local_rejection=rejection,
        delta_review={
            "legacy_field": "sl10_repair_review",
            "decision": sl10.decision,
            "evidence": _jsonable(sl10.evidence),
            "local_check_evidence": _jsonable(sl10.local_check_evidence or local_review),
        },
        review_meta=sl10.review_meta,
        meta=sl10.meta,
    )


def _fix_log_entry(
    *,
    state: _RunState,
    iteration: int,
    phase: str,
    batch: FixRequestBatch,
    decisions: list[FixRequestDecision] | None = None,
    old_dsl: str = "",
    candidate_dsl: str = "",
    diff_summary: dict[str, Any] | None = None,
    local_check_evidence: dict[str, Any] | None = None,
    sl10_review: SL10RepairReviewOutput | None = None,
    next_action: str = "",
    notes: list[str] | None = None,
) -> dict[str, Any]:
    entry = FixLogEntry(
        entry_id=f"fixlog-{len(state.fix_log)}-{phase}",
        iteration=iteration,
        repair_attempt=len(state.repair_history),
        phase=phase,
        batch_id=batch.batch_id,
        request_batch=_jsonable(batch),
        decisions=[_jsonable(decision) for decision in decisions or []],
        old_dsl_hash=_hash_text(old_dsl) if old_dsl else "",
        candidate_dsl_hash=_hash_text(candidate_dsl) if candidate_dsl else "",
        diff_summary=_jsonable(diff_summary or {}),
        local_check_evidence=_jsonable(local_check_evidence or {}),
        sl10_review=_jsonable(sl10_review),
        next_action=next_action,
        notes=list(notes or []),
    )
    payload = _jsonable(entry)
    state.fix_log.append(payload)
    return payload


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
    variable_role_summary = _diagnostic_variable_role_summary(nl, selected_feedback)
    if variable_role_summary:
        selected_trace["variable_role_summary"] = variable_role_summary
    if selected_trace["pre_scenario"]:
        state.pre_scenario_repair_count += 1

    rework_locked = state.pending_repair_rejection is not None and state.pending_original_fix_plan is not None
    if rework_locked:
        fix_plan, fix_meta = run_sd8_fix_plan(
            None,
            source="repair_review",
            rejection=state.pending_repair_rejection,
            original=state.pending_original_fix_plan,
        )
    else:
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

    request_batch = _fix_request_batch_from_plan(
        iteration=iteration,
        source=source,
        source_stage=source_stage,
        selected_trace=selected_trace,
        fix_plan=fix_plan,
        effective_fix_plan=effective_fix_plan,
    )
    _fix_log_entry(
        state=state,
        iteration=iteration,
        phase="request_batch",
        batch=request_batch,
        old_dsl=state.current_dsl,
        next_action="sl9_decision_and_repair",
        notes=["SD-8 produced FixRequestBatch; deterministic stage does not decide final repair."],
    )

    if source == FeedbackSource.DESIGN.value and isinstance(selected_feedback, DesignFeedback):
        mark_warning_repair_attempt(
            validation.context.warning_budget_state,
            [item.instance_key for item in selected_feedback.blocking_items],
        )
        state.warning_budget_state = validation.context.warning_budget_state

    max_rework_attempts = max(1, cfg.max_iterations - iteration)
    aggregate_stage_ids = list(repair_stage_ids)
    last_iteration_patch: dict[str, Any] = {}
    last_repair_review: RepairReviewFeedback | None = None
    last_sl10_output: SL10RepairReviewOutput | None = None

    for rework_attempt in range(max_rework_attempts):
        attempt_rework_locked = rework_locked or rework_attempt > 0
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
            fix_request_batch=request_batch,
            fix_log=list(state.fix_log),
            rework_locked=attempt_rework_locked,
        )
        repair_run = adapters.repair(request)
        repair_run = _append_llm_stage_run(
            run=repair_run,
            expected_stage_id=StageId.SL_9_REPAIR,
            stage_records=state.stage_records,
            iteration_stage_metas=None,
            llm_interactions=state.llm_interactions,
        )
        parsed_output: Any = {}
        if _is_llm_stage_run(repair_run):
            parsed_output = getattr(repair_run, "parsed_output", {}) or {}
            if not isinstance(parsed_output, dict):
                raise TypeError("SL-9 LLMStageRun parsed_output must be a dict with candidate_dsl/decisions")
            candidate_dsl = str(parsed_output.get("candidate_dsl") or "")
            aggregate_stage_ids.append(getattr(repair_run, "stage_meta").stage_id)
        else:
            if isinstance(repair_run, dict):
                parsed_output = dict(repair_run)
                candidate_dsl = str(parsed_output.get("candidate_dsl") or "")
            else:
                candidate_dsl = str(repair_run or "")
                parsed_output = {"candidate_dsl": candidate_dsl}
            repair_meta = _sl9_meta(state.current_dsl, fix_plan, candidate_dsl)
            _append_stage(state.stage_records, repair_meta)
            aggregate_stage_ids.append(repair_meta.stage_id)
            state.llm_interactions.append(
                {
                    "stage_id": StageId.SL_9_REPAIR.value,
                    "provider": cfg.adapter_mode,
                    "model_id": "explicit-adapter",
                    "real_llm_provider_api": False,
                    "prompt_template_version": "pr-b1-repair-adapter.v2-fixrequest",
                    "input_hash": _hash_text(state.current_dsl),
                    "prompt_hash": repair_meta.prompt_hash,
                    "raw_output_hash": repair_meta.output_hash,
                    "raw_output": candidate_dsl,
                    "parsed_output": {"candidate_dsl": candidate_dsl},
                    "schema_validation_ok": bool(candidate_dsl),
                    "note": "Explicit adapter returned DSL only; runtime fills per-request SL-9 decisions for compatibility.",
                }
            )
        request.candidate_dsl = candidate_dsl

        sl9_decision = _coerce_sl9_decision_output(
            parsed_output,
            batch=request_batch,
            candidate_dsl=candidate_dsl,
            rework_locked=attempt_rework_locked,
        )
        sl9_decision.diff_summary = sl9_decision.diff_summary or _dsl_diff_summary(state.current_dsl, candidate_dsl)
        request.sl9_decision = sl9_decision
        request.diff_summary = dict(sl9_decision.diff_summary)
        request.fix_log = list(state.fix_log)

        _fix_log_entry(
            state=state,
            iteration=iteration,
            phase="sl9_decision" if rework_attempt == 0 else "sl9_rework_decision",
            batch=request_batch,
            decisions=sl9_decision.decisions,
            old_dsl=state.current_dsl,
            candidate_dsl=candidate_dsl,
            diff_summary=sl9_decision.diff_summary,
            next_action="sl10_review" if sl9_decision.accepted_request_ids else "reject_or_waiver",
            notes=[*sl9_decision.repair_rationale, *( ["rework_locked=true"] if attempt_rework_locked else [] )],
        )

        if not sl9_decision.accepted_request_ids:
            hard_rejected = any(req.hard_block for req in request_batch.requests)
            waiver_continue = (
                not hard_rejected
                and bool(request_batch.requests)
                and all(req.waiver_allowed for req in request_batch.requests)
                and all(decision.decision == "reject" for decision in sl9_decision.decisions)
            )
            rejection = RepairRejection(
                rejected_by_stage=StageId.SL_9_REPAIR.value,
                reason="sl9_rejected_all_fix_requests" + (":hard_block" if hard_rejected else ":waiver_continue" if waiver_continue else ":waiver_only"),
                target_resolved=waiver_continue,
                regression_detected=False,
                drift_risk="major" if hard_rejected else "minor",
                evidence=[_jsonable(decision) for decision in sl9_decision.decisions],
            )
            repair_review = RepairReviewFeedback(
                ok=waiver_continue,
                target_resolved=waiver_continue,
                drift_risk=rejection.drift_risk,
                local_rejection=None if waiver_continue else rejection,
            )
            if waiver_continue:
                sc11_meta = _meta(StageId.SC_11_ACCEPT_CANDIDATE, ok=True)
                _append_stage(state.stage_records, sc11_meta)
                aggregate_stage_ids.append(sc11_meta.stage_id)
            _fix_log_entry(
                state=state,
                iteration=iteration,
                phase="sl9_all_rejected",
                batch=request_batch,
                decisions=sl9_decision.decisions,
                old_dsl=state.current_dsl,
                candidate_dsl=candidate_dsl,
                diff_summary=sl9_decision.diff_summary,
                next_action="continue_after_waiver" if waiver_continue else "exit_rejected",
                notes=[rejection.reason],
            )
            repair_payload = {
                "iteration": iteration,
                "selected_feedback": selected_trace,
                "plan_kind": request_batch.legacy_plan_kind,
                "fix_plan": _jsonable(effective_fix_plan),
                "fix_request_batch": _jsonable(request_batch),
                "sl9_decision": _jsonable(sl9_decision),
                "candidate_dsl": candidate_dsl,
                "candidate_dsl_hash": _hash_text(candidate_dsl),
                "repair_review": _jsonable(repair_review),
                "accepted": False,
                "waiver_continue": waiver_continue,
                "repair_stage_ids": list(aggregate_stage_ids),
                "scenario_set_id": validation.scenario_set.scenario_set_id if validation.scenario_set is not None else None,
                "fix_log_entry_count": len(state.fix_log),
            }
            state.repair_history.append(repair_payload)
            return waiver_continue, {
                "selected_feedback": selected_trace,
                "repair_stage_ids": list(aggregate_stage_ids),
                "fix_request_batch": _jsonable(request_batch),
                "sl9_decision": _jsonable(sl9_decision),
                "repair_review": _jsonable(repair_review),
                "accepted_candidate": False,
                "waiver_continue": waiver_continue,
                "exit_reason": "all_fix_requests_rejected_as_waiver_continue" if waiver_continue else rejection.reason,
                "retryable_repair_rejection": False,
            }

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
            warning_budget_state=validation.context.warning_budget_state,
            fix_request_batch=request_batch,
            fix_log=list(state.fix_log),
            sl9_decision=sl9_decision,
            diff_summary=sl9_decision.diff_summary,
            rework_locked=attempt_rework_locked,
        )
        local_review, local_meta = adapters.repair_review(review_request)
        local_check_evidence = _local_repair_check_evidence(repair_review=local_review, repair_review_meta=local_meta)
        review_request.local_check_evidence = local_check_evidence
        local_sd10_repair_review = _jsonable(local_review)
        repair_review_input_summary = {
            "nl_hash": _hash_text(nl),
            "has_nl_input": bool(nl),
            "has_grounding_map": cfg.grounding_map is not None,
            "old_dsl_hash": _hash_text(state.current_dsl),
            "candidate_dsl_hash": _hash_text(candidate_dsl),
            "fix_plan_target": getattr(effective_fix_plan, "target", None),
            "fix_plan_source_stage": getattr(effective_fix_plan, "source_stage", None),
            "fix_request_batch_id": request_batch.batch_id,
            "scenario_set_id": validation.scenario_set.scenario_set_id if validation.scenario_set is not None else None,
            "inputs": ["NL", "GroundingMap", "old_dsl", "candidate_dsl", "FixRequestBatch", "SL9Decisions", "FixLog", "LocalCheckEvidence", "ScenarioSet"],
            "local_check_stage_id": StageId.SD_10_REPAIR_REVIEW.value,
            "active_review_stage_id": StageId.SL_10_REPAIR_REVIEW.value,
            "rework_attempt": rework_attempt,
            "rework_locked": attempt_rework_locked,
        }

        if adapters.sl10_review is not None:
            sl10_run = adapters.sl10_review(review_request, local_review)
            sl10_run = _append_llm_stage_run(
                run=sl10_run,
                expected_stage_id=StageId.SL_10_REPAIR_REVIEW,
                stage_records=state.stage_records,
                iteration_stage_metas=None,
                llm_interactions=state.llm_interactions,
            )
            if _is_llm_stage_run(sl10_run):
                sl10_output = getattr(sl10_run, "feedback", None)
                if not isinstance(sl10_output, SL10RepairReviewOutput):
                    parsed = getattr(sl10_run, "parsed_output", {}) or {}
                    sl10_output = SL10RepairReviewOutput(
                        ok=bool(parsed.get("decision") == "pass"),
                        decision=str(parsed.get("decision") or "invalid_output"),  # type: ignore[arg-type]
                        target_resolved=bool(parsed.get("target_resolved", False)),
                        regression_detected=bool(parsed.get("regression_detected", True)),
                        drift_risk=str(parsed.get("drift_risk") or "major"),  # type: ignore[arg-type]
                        rework_instructions=[str(item) for item in parsed.get("rework_instructions", [])],
                        evidence=_jsonable(parsed.get("evidence", [])),
                        local_check_evidence=local_check_evidence,
                        review_meta=None,
                        meta=getattr(sl10_run, "stage_meta"),
                    )
                sl10_output.local_check_evidence = sl10_output.local_check_evidence or local_check_evidence
                aggregate_stage_ids.append(getattr(sl10_run, "stage_meta").stage_id)
            else:
                sl10_output, sl10_meta = sl10_run
                _append_stage(state.stage_records, sl10_meta)
                aggregate_stage_ids.append(sl10_meta.stage_id)
        else:
            sl10_output = _default_sl10_output_from_local_checks(local_review=local_review, local_evidence=local_check_evidence)
            assert sl10_output.meta is not None
            _append_stage(state.stage_records, sl10_output.meta)
            aggregate_stage_ids.append(sl10_output.meta.stage_id)

        repair_review = _repair_review_from_sl10(sl10_output, local_review=local_review)
        accepted = bool(sl10_output.ok)
        if accepted:
            sc11_meta = _meta(StageId.SC_11_ACCEPT_CANDIDATE, ok=True)
            _append_stage(state.stage_records, sc11_meta)
            aggregate_stage_ids.append(sc11_meta.stage_id)

        _fix_log_entry(
            state=state,
            iteration=iteration,
            phase="sl10_review" if rework_attempt == 0 else "sl10_rework_review",
            batch=request_batch,
            decisions=sl9_decision.decisions,
            old_dsl=state.current_dsl,
            candidate_dsl=candidate_dsl,
            diff_summary=sl9_decision.diff_summary,
            local_check_evidence=local_check_evidence,
            sl10_review=sl10_output,
            next_action="sc11_accept_then_sd2" if accepted else ("sl9_rework" if rework_attempt + 1 < max_rework_attempts else "exit_rejected_rework_budget_exhausted"),
            notes=sl10_output.rework_instructions,
        )

        repair_payload = {
            "iteration": iteration,
            "selected_feedback": selected_trace,
            "plan_kind": request_batch.legacy_plan_kind,
            "fix_plan": _jsonable(effective_fix_plan),
            "fix_request_batch": _jsonable(request_batch),
            "sl9_decision": _jsonable(sl9_decision),
            "candidate_dsl": candidate_dsl,
            "candidate_dsl_hash": _hash_text(candidate_dsl),
            "repair_review_input_summary": repair_review_input_summary,
            "local_check_evidence": _jsonable(local_check_evidence),
            "sd10_repair_review": local_sd10_repair_review,
            "sl10_repair_review": _jsonable(sl10_output),
            "repair_review": _jsonable(repair_review),
            "accepted": accepted,
            "repair_stage_ids": list(aggregate_stage_ids),
            "scenario_set_id": validation.scenario_set.scenario_set_id if validation.scenario_set is not None else None,
            "fix_log_entry_count": len(state.fix_log),
            "rework_attempt": rework_attempt,
        }
        state.repair_history.append(repair_payload)

        last_repair_review = repair_review
        last_sl10_output = sl10_output
        last_iteration_patch = {
            "selected_feedback": selected_trace,
            "repair_stage_ids": list(aggregate_stage_ids),
            "fix_request_batch": _jsonable(request_batch),
            "sl9_decision": _jsonable(sl9_decision),
            "local_check_evidence": _jsonable(local_check_evidence),
            "sl10_repair_review": _jsonable(sl10_output),
            "repair_review": _jsonable(repair_review),
            "accepted_candidate": accepted,
            "fix_log_entry_count": len(state.fix_log),
            "rework_attempts_used": rework_attempt + 1,
        }
        if accepted:
            state.current_dsl = candidate_dsl
            state.pending_repair_rejection = None
            state.pending_original_fix_plan = None
            state.pending_rework_request = None
            last_iteration_patch["exit_reason"] = "candidate_accepted_for_next_full_pass"
            return True, last_iteration_patch

        state.pending_repair_rejection = None
        state.pending_original_fix_plan = None
        state.pending_rework_request = _jsonable(sl10_output)
        if rework_attempt + 1 < max_rework_attempts:
            continue
        last_iteration_patch["exit_reason"] = repair_review.local_rejection.reason if repair_review.local_rejection is not None else "sl10 repair review requested rework"
        last_iteration_patch["retryable_repair_rejection"] = False
        last_iteration_patch["next_iteration_repair_plan"] = "<none:sl10_rework_budget_exhausted>"
        return False, last_iteration_patch

    fallback_reason = "sl10_rework_budget_exhausted"
    if last_repair_review is not None and last_repair_review.local_rejection is not None:
        fallback_reason = last_repair_review.local_rejection.reason
    if last_sl10_output is not None:
        _fix_log_entry(
            state=state,
            iteration=iteration,
            phase="sl10_rework_budget_exhausted",
            batch=request_batch,
            old_dsl=state.current_dsl,
            next_action="exit_rejected",
            notes=[fallback_reason],
        )
    last_iteration_patch.setdefault("selected_feedback", selected_trace)
    last_iteration_patch.setdefault("repair_stage_ids", list(aggregate_stage_ids))
    last_iteration_patch.setdefault("accepted_candidate", False)
    last_iteration_patch["exit_reason"] = fallback_reason
    last_iteration_patch["retryable_repair_rejection"] = False
    return False, last_iteration_patch

def _eligibility(cfg: FullStagedRuntimeConfig, *, record_status: str, oracle_weak: bool) -> tuple[bool, str | None, str | None]:
    if record_status != "success":
        return False, None, "verdict_not_success"
    reasons: list[str] = []
    resolved = cfg.resolved_loop_config or {}
    condition_id = str(resolved.get("condition_id") or "")
    provider_mode = str(resolved.get("llm_provider_mode") or "")
    if oracle_weak:
        reasons.append("weak_oracle")
    if not cfg.allow_main_result_eligible:
        reasons.append("deterministic_runtime_not_default_real_adapter")
    if condition_id and condition_id != "full_staged_v1":
        reasons.append("non_default_condition")
    if provider_mode and provider_mode != "real_env":
        reasons.append("non_real_provider_mode")
    if reasons:
        return False, None, ";".join(reasons)
    return True, "success_full_pass_with_non_weak_oracle", None


def _redaction_failed_safe_payload(
    *,
    nl: str,
    cfg: FullStagedRuntimeConfig,
    state: _RunState,
    exc: Exception,
) -> dict[str, Any]:
    """Return a minimal secret-safe payload when redaction itself fails.

    PR-C's audit rule is fail-closed: an unredacted run record must never be
    written as a Path1/Path2 eligible main result.  If the redaction engine
    crashes, discard all raw text surfaces and persist only hashes plus the
    audit-blocker reason so the run is still traceable without leaking secrets.
    """

    failure_log = {
        "ts": _utc_now(),
        "level": "error",
        "event": "run_record_payload_redaction_failed",
        "message": f"{type(exc).__name__}: {str(exc)[:300]}",
        "fail_closed": True,
    }
    return {
        "input_bundle": {
            "nl": "<omitted:redaction_failed>",
            "nl_hash": _hash_text(nl),
            "initial_dsl_hash": _hash_text(cfg.initial_dsl),
            "path_context": "<omitted:redaction_failed>",
            "pr_b1_control_flow_only": False,
            "default_loop_config_entry_integrated": bool(cfg.default_loop_config_entry_integrated),
            "redaction_failed": True,
        },
        "deterministic_feedback": {
            "omitted": "redaction_failed",
            "iteration_count": len(state.iteration_records),
        },
        "repair_history": [],
        "fix_log": [],
        "scenario_history": [],
        "final_artifacts": {
            "final_dsl": "<omitted:redaction_failed>",
            "final_dsl_hash": _hash_text(state.current_dsl),
            "verdict": "invalid",
            "verdict_source_stage_id": StageId.SC_13_TRACE_AUDIT.value,
            "verdict_reason": "run record redaction failed; raw payload omitted fail-closed",
            "agent_loop_result_status": "spec_failed",
            "oracle_weak": state.oracle_weak,
            "main_result_eligible": False,
            "inclusion_reason": None,
            "exclusion_reason": "redaction_failed",
            "error_message": f"run record redaction failed: {type(exc).__name__}: {str(exc)[:300]}",
            "redaction_failed": True,
        },
        "logs": [*_jsonable(state.logs), failure_log],
    }


def _redaction_failed_safe_stage_records(stage_records: list[StageResultMeta]) -> list[dict[str, Any]]:
    """Keep stage ordering/status audit data but drop text fields."""

    safe_rows: list[dict[str, Any]] = []
    for meta in stage_records:
        row = _jsonable(meta)
        if not isinstance(row, dict):
            continue
        for key in ("skipped_reason", "stage_error", "output_validation_error"):
            if row.get(key):
                row[key] = "<omitted:redaction_failed>"
        status = row.get("status")
        if status in {StageStatus.ERROR, StageStatus.ERROR.value} and not (row.get("stage_error") or row.get("output_validation_error")):
            row["output_validation_error"] = "<omitted:redaction_failed>"
        safe_rows.append(row)
    return safe_rows


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
    resolved_config = dict(cfg.resolved_loop_config or {})
    run_config = {
        **resolved_config,
        "max_iterations": cfg.max_iterations,
        "scenario_max_retries": cfg.scenario_max_retries,
        "policy_profile": cfg.policy_profile,
        "adapter_mode": cfg.adapter_mode,
        "allow_main_result_eligible": cfg.allow_main_result_eligible,
        "real_llm_provider_api": bool(cfg.real_llm_provider_api),
        "default_loop_config_entry_integrated": bool(cfg.default_loop_config_entry_integrated),
        "contract_only": False,
    }
    run_config.update(_jsonable(cfg.run_config_extra))
    redaction_report = list(_jsonable(cfg.redaction_report) or [])
    for interaction in state.llm_interactions:
        if isinstance(interaction, dict) and interaction.get("redaction_report"):
            redaction_report.extend(_jsonable(interaction.get("redaction_report")))

    raw_payload = {
        "input_bundle": {
            "nl": nl,
            "nl_hash": _hash_text(nl),
            "initial_dsl_hash": _hash_text(cfg.initial_dsl),
            "path_context": _jsonable(cfg.path_context),
            "pr_b1_control_flow_only": False,
            "default_loop_config_entry_integrated": bool(cfg.default_loop_config_entry_integrated),
        },
        "deterministic_feedback": _jsonable(state.deterministic_feedback),
        "repair_history": _jsonable(state.repair_history),
        "fix_log": _jsonable(state.fix_log),
        "scenario_history": _jsonable(state.scenario_history),
        "final_artifacts": {
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
        "logs": _jsonable(state.logs),
    }
    redaction_failed = False
    redaction_failure_message: str | None = None
    try:
        from method.llm_stages import redact_run_record_payload

        redacted_payload, payload_report = redact_run_record_payload(raw_payload)
        raw_payload = redacted_payload
        redaction_report.extend(_jsonable(payload_report))
    except Exception as exc:
        redaction_failed = True
        redaction_failure_message = f"{type(exc).__name__}: {str(exc)[:300]}"
        raw_payload = _redaction_failed_safe_payload(nl=nl, cfg=cfg, state=state, exc=exc)
        redaction_report.append(
            {
                "field_path": "run_record",
                "reason": "redaction_failed",
                "replacement": "<omitted:redaction_failed>",
                "affects_replay": True,
            }
        )

    return AgentLoopRunRecord(
        schema_version=RUN_RECORD_SCHEMA_VERSION,
        run_id=state.run_id,
        created_at=state.run_started_at,
        status=("invalid" if redaction_failed else state.final_record_status),  # type: ignore[arg-type]
        input_bundle=raw_payload["input_bundle"],
        run_config=run_config,
        environment=_environment(cfg),
        stage_graph=_planned_stage_graph(state.stage_records),
        stage_records=(
            _redaction_failed_safe_stage_records(state.stage_records)
            if redaction_failed
            else [_jsonable(meta) for meta in state.stage_records]
        ),
        iteration_records=(
            [
                {
                    "omitted": "redaction_failed",
                    "iteration_count": len(state.iteration_records),
                    "redaction_failure": redaction_failure_message,
                }
            ]
            if redaction_failed
            else _jsonable(state.iteration_records)
        ),
        llm_interactions=(
            [
                {
                    "omitted": "redaction_failed",
                    "interaction_count": len(state.llm_interactions),
                    "redaction_failure": redaction_failure_message,
                }
            ]
            if redaction_failed
            else _jsonable(state.llm_interactions)
        ),
        deterministic_feedback=raw_payload["deterministic_feedback"],
        repair_history=raw_payload["repair_history"],
        fix_log=raw_payload["fix_log"],
        scenario_history=raw_payload["scenario_history"],
        final_artifacts=raw_payload["final_artifacts"],
        logs=raw_payload["logs"],
        replay_index={
            "stage_by_index": {str(i): meta.stage_id for i, meta in enumerate(state.stage_records)},
            "iteration_count": len(state.iteration_records),
            "repair_count": len(state.repair_history),
            "fix_log_count": len(state.fix_log),
            "scenario_history_count": len(state.scenario_history),
            "pre_scenario_repair_count": state.pre_scenario_repair_count,
            "verdict": state.final_verdict,
            "verdict_source_stage_id": state.verdict_source_stage_id,
        },
        redaction_report=redaction_report,
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
    if config.run_id:
        run_id = config.run_id
    else:
        input_hash = hashlib.sha256(f"{nl}\n{config.initial_dsl}".encode("utf-8")).hexdigest()[:12]
        run_id = f"pr-b1-{input_hash}-{uuid.uuid4().hex[:12]}"
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
                    seeds = parsed_output.get("grounding_seeds") or []
                    assumptions = parsed_output.get("assumptions") or []
                    if seeds and config.grounding_map is None:
                        try:
                            config.grounding_map = GroundingMap(
                                elements=[GroundedElement(**item) if isinstance(item, dict) else item for item in seeds],
                                source_summary={
                                    "source_stage": StageId.SL_1_INITIAL_MODELING.value,
                                    "assumptions": assumptions,
                                },
                            )
                        except Exception as exc:
                            state.logs.append({"ts": _utc_now(), "level": "warning", "event": "grounding_seed_coercion_failed", "message": str(exc)})
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
                warning_budget_state=state.warning_budget_state,
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
        state.warning_budget_state = validation.context.warning_budget_state
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

        weak_sim_feedback = validation.feedback.get(FeedbackSource.SIM.value)
        if (
            validation.selected is None
            and isinstance(weak_sim_feedback, SimFeedback)
            and not weak_sim_feedback.ok
            and getattr(weak_sim_feedback, "oracle_weak", False)
        ):
            reason = f"sim_failed_but_oracle_weak:{getattr(weak_sim_feedback, 'weak_oracle_reason', '') or 'weak_oracle'}"
            _mark_sc12_verdict(
                state,
                verdict="not_converged",
                source_stage_id=StageId.SD_6_SIM.value,
                reason=reason,
                record_status="failed",
                result_status="not_converged",
                stage_ok=False,
                stage_status=StageStatus.FAIL,
            )
            iteration_record["exit_reason"] = reason
            state.iteration_records.append(iteration_record)
            break

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
            reason = iteration_record.get("exit_reason") or "repair review rejected candidate"
            can_retry_rejection = (
                state.pending_repair_rejection is not None
                and state.pending_original_fix_plan is not None
                and iteration + 1 < config.max_iterations
            )
            if can_retry_rejection:
                iteration_record["exit_reason"] = "repair_review_rejected_retry_with_revised_fix_plan"
                iteration_record["next_iteration_repair_plan"] = "RevisedFixPlan"
                state.iteration_records.append(iteration_record)
                continue
            _mark_sc12_verdict(
                state,
                verdict="not_converged",
                source_stage_id=StageId.SC_11_ACCEPT_CANDIDATE.value,
                reason=str(reason),
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

    if state.final_record_status not in {"success", "failed", "rejected", "budget_exhausted", "error", "invalid"}:
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
        llm_model=config.provider_model_redacted or "none-pr-b1-explicit-adapters",
        run_record_id=run_id,
    )

    if config.write_run_record:
        record = _build_record(cfg=config, nl=nl, state=state)
        try:
            path = write_agent_loop_run_record(record, agent_loop_run_record_path(config.output_dir, run_id))
            result.run_record_path = str(path)
            if record.status == "invalid" and record.final_artifacts.get("redaction_failed") is True:
                result.status = "spec_failed"
                result.error_message = str(record.final_artifacts.get("error_message") or "run record redaction failed")
        except Exception as exc:
            result.status = "spec_failed"
            result.error_message = f"run record write failed: {type(exc).__name__}: {str(exc)[:300]}"
            result.run_record_path = None
    return result
