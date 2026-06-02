"""Canonical full-staged agent-loop entry for project_1.

PR-C wires the PR-B1 runtime driver and PR-B2 LLM stage adapters into the
public ``method.loop.run_agent_loop`` façade.  Therefore

``run_agent_loop(nl, LoopConfig())``

now means the experiment-default ``full_staged_v1`` runtime with real-env LLM
adapters.  Fake/mock/replay providers remain available only through explicit
non-default conditions and are always marked in the run record as not eligible
for Path1/Path2 main-result statistics.
"""

from __future__ import annotations

import hashlib
import os
import uuid
from dataclasses import asdict, is_dataclass
from typing import Any, Optional

from method.llm_stages import (
    ChatProvider,
    LLMStageConfig,
    RealEnvLLMProvider,
    redact_run_record_payload,
    run_sl1_initial_modeling_llm,
    run_sl5_scenario_generation_llm,
    run_sl7_model_review_llm,
    run_sl9_repair_llm,
    run_sl10b_delta_review_llm,
)
from method.schema import AgentLoopResult, LoopConfig, StageContext
from method.staged_runtime import (
    FullStagedRuntimeAdapters,
    FullStagedRuntimeConfig,
    RepairRequest,
    ScenarioGenerationRequest,
    build_full_staged_runtime_adapters,
    run_full_staged_deterministic_runtime,
)
from method.stages.ids import ALL_STAGE_SPECS, StageId, StageStatus

RUN_RECORD_SCHEMA_VERSION = "pr-c.default-full-staged-runtime.v1"

_STAGE_SWITCH_BY_ID: dict[str, str | None] = {
    StageId.SC_0_START.value: None,
    StageId.SL_1_INITIAL_MODELING.value: "enable_initial_modeling",
    StageId.SD_2_PARSE.value: "enable_parse",
    StageId.SD_3_SEMANTIC.value: "enable_semantic",
    StageId.SD_4_DESIGN.value: "enable_design_inspect",
    StageId.SL_5_SCENARIO_GENERATION.value: "enable_scenario_generation",
    StageId.SD_5A_SCENARIO_COVERAGE.value: "enable_scenario_coverage",
    StageId.SC_5F_SCENARIO_FREEZE.value: "enable_scenario_generation",
    StageId.SD_6_SIM.value: "enable_simulation",
    StageId.SL_7_MODEL_REVIEW.value: "enable_model_review",
    StageId.SD_8_FIX_PLAN.value: "enable_fix_plan",
    StageId.SL_9_REPAIR.value: "enable_repair",
    StageId.SD_10_REPAIR_REVIEW.value: "enable_repair_review",
    StageId.SL_10B_DELTA_REVIEW.value: "enable_delta_review",
    StageId.SC_11_ACCEPT_CANDIDATE.value: "enable_repair",
    StageId.SC_12_EXIT.value: None,
    StageId.SC_13_TRACE_AUDIT.value: "enable_run_record",
}


def _stage_enabled(stage_id: str, cfg: LoopConfig) -> bool:
    switch = _STAGE_SWITCH_BY_ID.get(stage_id)
    if switch is None:
        return True
    return bool(cfg.stage_switches.get(switch, False))


def build_planned_stage_graph(config: Optional[LoopConfig] = None) -> dict[str, Any]:
    """Return the canonical full staged graph planned for a resolved config.

    Each node has the same trace fields that later runtime stage records must
    expose: ``enabled``, ``ran``, ``status`` and ``skipped_reason``.  The graph
    is intentionally a plan; actual run-record stage graphs are written by
    ``method.staged_runtime`` with the executed sequence.
    """
    cfg = config or LoopConfig()
    nodes: list[dict[str, Any]] = []
    for index, spec in enumerate(ALL_STAGE_SPECS):
        enabled = _stage_enabled(spec.stage_id, cfg)
        nodes.append(
            {
                "index": index,
                "stage_id": spec.stage_id,
                "stage_kind": spec.kind.value,
                "name": spec.name,
                "doc_filename": spec.doc_filename,
                "enabled": enabled,
                "ran": False,
                "status": StageStatus.SKIPPED.value,
                "skipped_reason": "planned_not_yet_run" if enabled else "disabled_by_condition",
            }
        )
    return {
        "schema_version": RUN_RECORD_SCHEMA_VERSION,
        "condition_id": cfg.condition_id,
        "condition_hash": cfg.resolved_config()["condition_hash"],
        "planned": [node["stage_id"] for node in nodes],
        "nodes": nodes,
    }


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


def _default_run_id(nl: str, resolved_config: dict[str, Any]) -> str:
    input_hash = hashlib.sha256(f"{nl}\n{resolved_config['condition_hash']}".encode("utf-8")).hexdigest()[:12]
    return f"pr-c-{input_hash}-{uuid.uuid4().hex[:12]}"


def _provider_config_read(cfg: LoopConfig) -> bool:
    if cfg.llm_provider_mode != "real_env":
        return False
    return all(bool(os.environ.get(key)) for key in ("LLM_ENDPOINT", "LLM_API_KEY", "LLM_MODEL"))


def _provider_model_redacted(cfg: LoopConfig, provider: ChatProvider | None) -> str:
    if cfg.llm_model:
        return cfg.llm_model
    if provider is not None:
        return getattr(provider, "model_id", "<provider:model>")
    if cfg.llm_provider_mode == "real_env":
        return os.environ.get("LLM_MODEL") or "<env:LLM_MODEL>"
    return "<mock:model>"


def _llm_stage_config(cfg: LoopConfig) -> LLMStageConfig:
    record_policy = cfg.record_policy
    return LLMStageConfig(
        provider_mode="mock" if cfg.llm_provider_mode == "mock" else "real_env",
        model=cfg.llm_model,
        temperature=float(cfg.llm_policy.get("temperature", 0.0)),
        seed=cfg.seed,
        max_retries=cfg.llm_max_retries,
        record_prompts=bool(record_policy.get("record_prompts", True)),
        record_raw_outputs=bool(record_policy.get("record_raw_outputs", True)),
        # PR-C audit records must never persist secrets.  Record policy can
        # reduce prompt/raw verbosity, but disabling redaction is not allowed on
        # the canonical entry because unredacted secrets exclude Path1/Path2
        # high-confidence results.
        redact_secrets=True,
    )


def _scenario_coverage_adapter(current_dsl: str, scenarios: list[Any]) -> tuple[dict[str, Any], Any]:
    from method.stages.sd_tools import run_sd5a_scenario_coverage

    return run_sd5a_scenario_coverage(current_dsl, scenarios)


def _normalize_scenarios_for_runtime(scenarios: list[Any]) -> list[Any]:
    """Clear SL-5 hot-start guesses on the canonical default path.

    ``TestScenario.initial_state`` is a hot-start convenience.  The PR-C
    default runtime should validate from the model's own initial transition
    unless an explicit smoke/replay profile opts into hot-start behavior.
    """

    normalized: list[Any] = []
    for scenario in scenarios:
        if hasattr(scenario, "initial_state") and getattr(scenario, "initial_state") is not None:
            clone = type(scenario)(**asdict(scenario))
            clone.initial_state = None
            normalized.append(clone)
        else:
            normalized.append(scenario)
    return normalized


def _build_runtime_adapters(
    cfg: LoopConfig,
    *,
    llm_cfg: LLMStageConfig,
    provider: ChatProvider | None,
) -> FullStagedRuntimeAdapters:
    def initial_modeling(nl: str, _context: StageContext) -> Any:
        return run_sl1_initial_modeling_llm(
            nl=nl,
            config=llm_cfg,
            provider=provider,
        )

    def scenario_generate(request: ScenarioGenerationRequest) -> Any:
        run = run_sl5_scenario_generation_llm(
            nl=request.nl,
            current_dsl=request.current_dsl,
            inspect_json=request.context.inspect_json,
            design_summary={"iteration": request.attempt_index, "context": request.context.to_summary()},
            grounding_map=request.context.grounding_map,
            coverage_directive=str(request.coverage_directive) if request.coverage_directive is not None else None,
            config=llm_cfg,
            provider=provider,
        )
        if run.ok:
            run.parsed_output = _normalize_scenarios_for_runtime(list(run.parsed_output or []))
            run.interaction["scenario_hot_start_policy"] = "default_entry_clears_initial_state"
            redacted_scenarios, scenario_redaction_report = redact_run_record_payload(
                {"scenarios": _jsonable(run.parsed_output)},
                path="llm_interaction.parsed_output",
            )
            run.interaction["parsed_output"] = redacted_scenarios
            for attempt in run.interaction.get("attempts", []):
                if attempt.get("status") == "ok":
                    attempt["parsed_output"] = redacted_scenarios
            run.redaction_report.extend(scenario_redaction_report)
        return run

    def model_review(current_dsl: str, context: StageContext, feedback: dict[str, Any]) -> Any:
        return run_sl7_model_review_llm(
            nl=context.nl,
            current_dsl=current_dsl,
            grounding_map=context.grounding_map,
            inspect_json=context.inspect_json,
            design_diagnostics_summary=_jsonable(feedback.get("design", {})),
            sim_summary=_jsonable(feedback.get("sim", {})),
            warning_budget_exhausted=[
                key for key, item in context.warning_budget_state.items() if getattr(item, "budget_exhausted", False)
            ],
            review_policy={"mode": cfg.model_review_mode, **_jsonable(cfg.feedback_policy)},
            config=llm_cfg,
            provider=provider,
        )

    def repair(request: RepairRequest) -> Any:
        return run_sl9_repair_llm(
            nl=request.nl,
            current_dsl=request.old_dsl,
            fix_plan=request.fix_plan,
            grounding_map=request.grounding_map,
            selected_diagnostics=[request.selected_feedback_trace],
            preserve_list=(request.fix_plan.required_preserve_element_ids if hasattr(request.fix_plan, "required_preserve_element_ids") else []),
            scenario_summary=(
                {
                    "scenario_set_id": request.scenario_set.scenario_set_id,
                    "epoch": request.scenario_set.epoch,
                    "n_scenarios": len(request.scenario_set.scenarios),
                    "coverage_report": request.scenario_set.coverage_report,
                }
                if request.scenario_set is not None
                else {"pre_scenario": True}
            ),
            repair_target=getattr(request.fix_plan, "target", None),
            config=llm_cfg,
            provider=provider,
        )

    def delta_review(request: RepairRequest, _repair_review: Any) -> Any:
        if request.fix_plan is None:
            raise TypeError("SL-10B delta review requires FixPlan")
        return run_sl10b_delta_review_llm(
            nl=request.nl,
            grounding_map=request.grounding_map,
            old_dsl=request.old_dsl,
            candidate_dsl=request.candidate_dsl,
            fix_plan=request.fix_plan,
            diff_summary={"selected_feedback": request.selected_feedback_trace},
            delta_review_policy={"mode": cfg.delta_review_mode, **_jsonable(cfg.feedback_policy)},
            config=llm_cfg,
            provider=provider,
        )

    adapters = build_full_staged_runtime_adapters(
        scenario_generate=scenario_generate,
        repair=repair,
        model_review=model_review,
        policy_profile=cfg.policy_profile,
        delta_review=delta_review,
    )
    adapters.initial_modeling = initial_modeling
    adapters.scenario_coverage = _scenario_coverage_adapter
    return adapters


def run_agent_loop(
    nl: str,
    config: Optional[LoopConfig] = None,
    *,
    seed_dsl: Optional[str] = None,
    llm_provider: ChatProvider | None = None,
) -> AgentLoopResult:
    """Run the canonical PR-C full-staged runtime."""
    cfg = config or LoopConfig()
    cfg.validate_for_run()
    if seed_dsl is not None and cfg.condition_id == "full_staged_v1":
        raise ValueError(
            "LoopConfig() default full_staged_v1 must not use seed_dsl/hot-start DSL; "
            "use method.legacy_loop for historical diagnostics or an explicit replay condition."
        )
    if cfg.condition_id == "full_staged_v1" and llm_provider is not None:
        raise ValueError("default full_staged_v1 must use real_env provider; provider injection requires an explicit non-default condition")
    if cfg.llm_provider_mode == "fake_replay":
        raise ValueError("PR-C default entry does not implement fake_replay; use PR-3 handoff smoke or a dedicated replay runner")
    if cfg.llm_provider_mode == "mock" and llm_provider is None:
        raise ValueError("mock provider mode requires explicit llm_provider and non-default condition")
    if not cfg.write_run_record:
        raise ValueError("PR-C run_agent_loop requires write_run_record=True for auditability")

    resolved_config = cfg.resolved_config()
    run_id = cfg.run_id or _default_run_id(nl, resolved_config)
    graph = build_planned_stage_graph(cfg)
    provider = llm_provider
    if cfg.llm_provider_mode == "real_env" and provider is None:
        provider = RealEnvLLMProvider()
    llm_cfg = _llm_stage_config(cfg)
    runtime_cfg = FullStagedRuntimeConfig(
        initial_dsl=seed_dsl or "",
        run_id=run_id,
        output_dir=cfg.output_dir,
        max_iterations=cfg.max_iterations,
        scenario_max_retries=cfg.scenario_max_retries,
        policy_profile=cfg.policy_profile,
        write_run_record=cfg.write_run_record,
        adapter_mode=cfg.llm_provider_mode,
        allow_main_result_eligible=cfg.condition_id == "full_staged_v1" and cfg.llm_provider_mode == "real_env",
        resolved_loop_config=resolved_config,
        run_config_extra={
            "runtime_implementation": "method.staged_runtime.run_full_staged_deterministic_runtime",
            "llm_max_retries": cfg.llm_max_retries,
            "planned_stage_graph": graph,
        },
        environment_extra={
            "loop_entrypoint": "method.loop.run_agent_loop",
            "record_schema_version": RUN_RECORD_SCHEMA_VERSION,
        },
        real_llm_provider_api=cfg.llm_provider_mode == "real_env",
        provider_config_read=_provider_config_read(cfg),
        provider_model_redacted=_provider_model_redacted(cfg, provider),
        default_loop_config_entry_integrated=True,
    )
    adapters = _build_runtime_adapters(cfg, llm_cfg=llm_cfg, provider=provider)
    result = run_full_staged_deterministic_runtime(nl, runtime_cfg, adapters=adapters)
    result.resolved_config = resolved_config
    result.planned_stage_graph = graph
    return result
