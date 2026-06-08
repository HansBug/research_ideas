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
    LLMStageRun,
    RealEnvLLMProvider,
    redact_run_record_payload,
    run_sl1_initial_modeling_llm,
    run_sl5_scenario_generation_llm,
    run_sl7_model_review_llm,
    run_sl9_repair_llm,
    run_sl10_repair_review_llm,
    run_sl10b_delta_review_llm,
)
from method.schema import AgentLoopResult, LoopConfig, StageContext, StageResultMeta, ReviewRunMeta
from method.staged_runtime import (
    FullStagedRuntimeAdapters,
    RepairRequest,
    ScenarioGenerationRequest,
    build_full_staged_runtime_adapters,
    _compact_fix_log_for_prompt,
    _compact_fix_request_batch_for_prompt,
    _compact_json,
    _compact_sl9_input_for_prompt,
    _repair_memory_for_prompt,
)
from method.stages.sl_repair_prompt import build_sl9_repair_prompt
from method.stages.sl10_repair_review_prompt import build_sl10_repair_review_prompt
from method.stages.ids import ALL_STAGE_SPECS, StageId, StageStatus
from method.langgraph_runtime import LG_C2_ContextRedactionBlocked, assemble_lg_c2_prompt_context

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
    StageId.SL_10_REPAIR_REVIEW.value: "enable_repair_review",
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
    budget_policy = cfg.budget_policy
    return LLMStageConfig(
        provider_mode="mock" if cfg.llm_provider_mode == "mock" else "real_env",
        model=cfg.llm_model,
        temperature=float(cfg.llm_policy.get("temperature", 0.0)),
        seed=cfg.seed,
        max_tokens=cfg.llm_policy.get("max_tokens"),
        max_prompt_tokens=budget_policy.get("prompt_token_budget", 128_000),
        prompt_token_estimator=str(budget_policy.get("prompt_token_estimator", "chars_per_token")),
        prompt_chars_per_token=float(budget_policy.get("chars_per_token_estimate", 4.0)),
        max_retries=cfg.llm_max_retries,
        record_prompts=bool(record_policy.get("record_prompts", True)),
        record_raw_outputs=bool(record_policy.get("record_raw_outputs", True)),
        # PR-C audit records must never persist secrets.  Record policy can
        # reduce prompt/raw verbosity, but disabling redaction is not allowed on
        # the canonical entry because unredacted secrets exclude Path1/Path2
        # high-confidence results.
        redact_secrets=True,
    )


def _jsonable_fix_request_batch_full(batch: Any) -> Any:
    if batch is None:
        return None
    return _jsonable(batch)


def _jsonable_fix_log_full(fix_log: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    return _jsonable(fix_log or [])


def _sl9_prompt_payload_candidates(request: RepairRequest) -> list[tuple[str, dict[str, Any]]]:
    plan = request.fix_plan
    plan_summary = _jsonable(plan)
    if isinstance(plan_summary, dict) and "original" in plan_summary and isinstance(plan_summary["original"], dict):
        # Keep RevisedFixPlan evidence, but expose a concise top-level target for
        # providers that attend to shallow fields first.
        plan_summary = {
            "kind": "RevisedFixPlan",
            "target": plan_summary["original"].get("target"),
            "source_stage": plan_summary["original"].get("source_stage"),
            **plan_summary,
        }
    repair_memory = getattr(request, "repair_memory", None) or _repair_memory_for_prompt(request.fix_log)
    scenario_summary = (
        {
            "scenario_set_id": request.scenario_set.scenario_set_id,
            "epoch": request.scenario_set.epoch,
            "n_scenarios": len(request.scenario_set.scenarios),
            "coverage_report": request.scenario_set.coverage_report,
        }
        if request.scenario_set is not None
        else {"pre_scenario": True}
    )
    preserve_list = (
        request.fix_plan.required_preserve_element_ids
        if hasattr(request.fix_plan, "required_preserve_element_ids")
        else []
    )
    full = {
        "fix_plan_summary": plan_summary,
        "fix_request_batch": _jsonable_fix_request_batch_full(request.fix_request_batch),
        "fix_log": _jsonable_fix_log_full(request.fix_log),
        "repair_memory": _jsonable(repair_memory),
        "grounding_map_summary": _jsonable(request.grounding_map),
        "selected_diagnostics": [_jsonable(request.selected_feedback_trace)],
        "preserve_list": list(preserve_list or []),
        "scenario_summary": _jsonable(scenario_summary),
    }
    compact = _compact_sl9_input_for_prompt(
        fix_plan=request.fix_plan,
        fix_request_batch=request.fix_request_batch,
        fix_log=request.fix_log,
        grounding_map=request.grounding_map,
        selected_diagnostics=[request.selected_feedback_trace],
        preserve_list=preserve_list,
        scenario_summary=scenario_summary,
    )
    if getattr(request, "repair_memory", None):
        compact["repair_memory"] = request.repair_memory
    return [("none", full), ("level1_compact", compact)]


def _select_sl9_prompt_payload(request: RepairRequest, cfg: LLMStageConfig) -> tuple[dict[str, Any], dict[str, Any]]:
    result = assemble_lg_c2_prompt_context(
        stage_id=StageId.SL_9_REPAIR.value,
        payload_candidates=_sl9_prompt_payload_candidates(request),
        prompt_builder=lambda payload: build_sl9_repair_prompt(
            nl=request.nl,
            current_dsl=request.old_dsl,
            fix_plan=payload["fix_plan_summary"],
            fix_request_batch=payload["fix_request_batch"],
            fix_log=payload["fix_log"],
            repair_memory=payload["repair_memory"],
            grounding_map=payload["grounding_map_summary"],
            selected_diagnostics=payload["selected_diagnostics"],
            preserve_list=payload["preserve_list"],
            scenario_summary=payload["scenario_summary"],
            repair_target=getattr(request.fix_plan, "target", None),
        ),
        cfg=cfg,
    )
    metadata = dict(result.metadata)
    # Keep LG-C2 metadata out of the prompt-visible payload.  The selected
    # prompt hash/budget computed by the context subgraph must describe the
    # exact prompt later sent by ``run_sl9_repair_llm``; canonical audit evidence
    # is attached to ``AgentLoopRunRecord.llm_interactions[].context_engineering``
    # after the provider call, not echoed back into the LLM prompt.
    return dict(result.payload), metadata


def _sl10_prompt_payload_candidates(request: RepairRequest) -> list[tuple[str, dict[str, Any]]]:
    scenario_summary = (
        {
            "scenario_set_id": request.scenario_set.scenario_set_id,
            "epoch": request.scenario_set.epoch,
            "n_scenarios": len(request.scenario_set.scenarios),
            "coverage_report": request.scenario_set.coverage_report,
        }
        if request.scenario_set is not None
        else {"pre_scenario": True}
    )
    full = {
        "grounding_map": _jsonable(request.grounding_map),
        "request_batch": _jsonable_fix_request_batch_full(request.fix_request_batch),
        "sl9_decisions": _jsonable(request.sl9_decision.decisions if request.sl9_decision else []),
        "fix_log": _jsonable_fix_log_full(request.fix_log),
        "diff_summary": _jsonable(request.diff_summary),
        "local_check_evidence": _jsonable(request.local_check_evidence),
        "scenario_summary": _jsonable(scenario_summary),
    }
    compact = {
        "grounding_map": _compact_json(request.grounding_map, max_list_items=16),
        "request_batch": _compact_fix_request_batch_for_prompt(request.fix_request_batch),
        "sl9_decisions": _compact_json(request.sl9_decision.decisions if request.sl9_decision else [], max_list_items=16),
        "fix_log": _compact_fix_log_for_prompt(request.fix_log),
        "diff_summary": _compact_json(request.diff_summary, max_list_items=8),
        "local_check_evidence": _compact_json(request.local_check_evidence, max_list_items=10),
        "scenario_summary": _compact_json(scenario_summary, max_list_items=12),
    }
    return [("none", full), ("level1_compact", compact)]


def _select_sl10_prompt_payload(request: RepairRequest, cfg: LLMStageConfig) -> tuple[dict[str, Any], dict[str, Any]]:
    result = assemble_lg_c2_prompt_context(
        stage_id=StageId.SL_10_REPAIR_REVIEW.value,
        payload_candidates=_sl10_prompt_payload_candidates(request),
        prompt_builder=lambda payload: build_sl10_repair_review_prompt(
            nl=request.nl,
            grounding_map=payload["grounding_map"],
            old_dsl=request.old_dsl,
            candidate_dsl=request.candidate_dsl,
            request_batch=payload["request_batch"],
            sl9_decisions=payload["sl9_decisions"],
            fix_log=payload["fix_log"],
            diff_summary=payload["diff_summary"],
            local_check_evidence=payload["local_check_evidence"],
            scenario_summary=payload["scenario_summary"],
        ),
        cfg=cfg,
    )
    metadata = dict(result.metadata)
    # Keep LG-C2 metadata out of the prompt-visible payload for the same reason
    # as SL-9: the context subgraph's prompt hash/budget must match the exact
    # provider prompt.  The canonical record carries LG-C2 evidence separately.
    return dict(result.payload), metadata


def _lg_c2_context_redaction_blocked_run(
    *,
    exc: LG_C2_ContextRedactionBlocked,
    provider: ChatProvider | None,
    cfg: LLMStageConfig,
) -> LLMStageRun:
    """Build a safe failed LLMStageRun when LG-C2 blocks context before provider I/O."""

    stage_id = str(exc.stage_id)
    spec = next(spec for spec in ALL_STAGE_SPECS if spec.stage_id == stage_id)
    provider_name = getattr(provider, "provider_name", "mock" if cfg.provider_mode == "mock" else "openai-compatible-env")
    model_id = cfg.model or getattr(provider, "model_id", "<provider:model>")
    message = str(exc)[:500]
    review_meta = ReviewRunMeta(
        provider=provider_name,
        model_id=model_id,
        resolved_model_id=model_id,
        prompt_template_version="lg-c2-context-redaction-guard",
        prompt_hash=exc.payload_hash,
        input_hash=exc.payload_hash,
        temperature=cfg.temperature,
        seed=cfg.seed,
        retry_count=0,
        raw_output_hash=exc.payload_hash,
        raw_output_path=None,
        parsed_schema_version="LG-C2.ContextRedactionGuard.v1",
        schema_validation_ok=False,
        schema_validation_error=message,
        cache_key=f"{stage_id}:{exc.payload_hash}",
        decision_threshold=None,
        failure_policy="fail_closed",
        replay_key=f"{stage_id}:{exc.payload_hash}",
    )
    interaction = {
        "stage_id": stage_id,
        "provider": provider_name,
        "model_id": model_id,
        "resolved_model_id": model_id,
        "prompt_template_version": "lg-c2-context-redaction-guard",
        "prompt_hash": exc.payload_hash,
        "input_hash": exc.payload_hash,
        "temperature": cfg.temperature,
        "seed": cfg.seed,
        "retry_count": 0,
        "raw_output_hash": exc.payload_hash,
        "raw_output_path": None,
        "parsed_schema_version": "LG-C2.ContextRedactionGuard.v1",
        "prompt_messages_omitted": "lg_c2_context_redaction_blocked",
        "raw_output_omitted": "lg_c2_context_redaction_blocked",
        "parsed_output_omitted": "lg_c2_context_redaction_blocked",
        "schema_validation_ok": False,
        "schema_validation_error": message,
        "usage": {},
        "attempts": [],
        "retry_error": {
            "error_kind": "redaction_failed",
            "error_message": message,
        },
        "review_meta": asdict(review_meta),
        "provider_mode": cfg.provider_mode,
        "real_llm_provider_api": cfg.provider_mode == "real_env",
        "redaction_failed": True,
        "redaction_failure_path": "lg_c2_context_engineering.selected_payload",
        "context_engineering": {
            **dict(exc.guard),
            "stage_id": stage_id,
            "prompt_payload_hash": exc.payload_hash,
            "redaction_guard": dict(exc.guard),
            "redaction_guard_fail_closed": True,
            "does_not_replace_academic_evidence": True,
        },
        "omitted": "lg_c2_context_redaction_blocked",
        "llm_retry_scope": "LG-C2 context redaction guard blocks before provider; no provider retry attempted",
    }
    return LLMStageRun(
        stage_id=stage_id,
        ok=False,
        parsed_output={},
        interaction=interaction,
        stage_meta=StageResultMeta(
            stage_id=stage_id,
            stage_kind=spec.kind,
            enabled=True,
            ran=True,
            status=StageStatus.ERROR,
            ok=False,
            stage_error=message,
            output_validation_error=message,
            input_hash=exc.payload_hash,
            output_hash=exc.payload_hash,
            prompt_hash=exc.payload_hash,
        ),
        redaction_report=[
            {
                "field_path": "llm_interaction.context_engineering.selected_payload",
                "reason": "lg_c2_context_redaction_blocked",
                "replacement": "<omitted:lg_c2_context_redaction_blocked>",
                "affects_replay": True,
            }
        ],
    )


def _scenario_coverage_adapter(current_dsl: str, scenarios: list[Any]) -> tuple[dict[str, Any], Any]:
    from method.stages.sd_tools import run_sd5a_scenario_coverage

    return run_sd5a_scenario_coverage(current_dsl, scenarios)


def _normalize_scenarios_for_runtime(scenarios: list[Any]) -> list[Any]:
    """Normalize SL-5 scenarios for pyfcstm default-entry timing.

    ``TestScenario.initial_state`` is a legitimate scenario-scoped operation in
    pyfcstm: it lets the oracle probe behavior from a reachable non-default
    leaf without forcing every scenario to replay a long prefix from the root.
    The canonical default runtime therefore preserves hot starts and only adds
    one empty pre-cycle when a scenario starts from default init and immediately
    injects an event.  This keeps default-entry timing correct without turning
    valid non-default transition probes into weak-oracle failures.
    """

    from method.schema import ScenarioStep

    normalized: list[Any] = []
    for scenario in scenarios:
        changed = False
        original_initial_state = getattr(scenario, "initial_state", None)
        clone = scenario
        steps = list(getattr(clone, "steps", []) or [])
        if steps:
            first = steps[0]
            if (
                original_initial_state is None
                and
                getattr(first, "events", None)
                and getattr(first, "before_cycles", 0) == 0
            ):
                steps[0] = ScenarioStep(
                    before_cycles=1,
                    events=list(first.events) if first.events is not None else None,
                    expected_state=first.expected_state,
                    expected_vars=dict(first.expected_vars) if first.expected_vars is not None else None,
                    name=first.name,
                )
                changed = True
        if changed:
            if clone is scenario:
                clone = type(scenario)(**asdict(scenario))
            clone.steps = steps
            clone.description = (
                (clone.description + " " if clone.description else "")
                + "[PR-E1/default-init-cycle-normalized: added one empty cycle before first event; "
                "scenario initial_state was preserved.]"
            ).strip()
            normalized.append(clone)
        else:
            normalized.append(scenario)
    return normalized


def _redaction_failure_message(exc: Exception) -> str:
    return f"run record parsed_output redaction failed fail-closed: {type(exc).__name__}"


def _mark_llm_run_redaction_failed(
    run: Any,
    *,
    stage_id: StageId,
    field_path: str,
    exc: Exception,
) -> Any:
    """Fail-close an LLM stage run when interaction redaction crashes.

    The canonical PR-C entry must still yield an auditable invalid run record
    instead of letting a redaction exception escape before ``SC-13`` can write
    the record.  Because the redaction engine itself is no longer trusted on
    this branch, discard prompt/raw/parsed surfaces and keep only hashes plus a
    safe exception type.
    """

    message = _redaction_failure_message(exc)
    if hasattr(run, "ok"):
        run.ok = False
    if hasattr(run, "parsed_output"):
        run.parsed_output = []

    meta = getattr(run, "stage_meta", None)
    if meta is not None:
        meta.ok = False
        meta.status = StageStatus.ERROR
        meta.stage_error = message
        meta.output_validation_error = message

    old_interaction = dict(getattr(run, "interaction", {}) or {})
    safe_interaction = {
        "stage_id": stage_id.value,
        "provider": old_interaction.get("provider", "<unknown>"),
        "model_id": old_interaction.get("model_id", "<unknown>"),
        "resolved_model_id": old_interaction.get("resolved_model_id", old_interaction.get("model_id", "<unknown>")),
        "prompt_template_version": old_interaction.get("prompt_template_version"),
        "prompt_hash": old_interaction.get("prompt_hash"),
        "input_hash": old_interaction.get("input_hash"),
        "raw_output_hash": old_interaction.get("raw_output_hash"),
        "parsed_schema_version": old_interaction.get("parsed_schema_version"),
        "schema_validation_ok": False,
        "schema_validation_error": message,
        "retry_count": old_interaction.get("retry_count", 0),
        "retry_error": {
            "error_kind": "redaction_failed",
            "error_message": message,
        },
        "provider_mode": old_interaction.get("provider_mode"),
        "real_llm_provider_api": old_interaction.get("real_llm_provider_api"),
        "redaction_failed": True,
        "redaction_failure_path": field_path,
        "omitted": "redaction_failed",
    }
    run.interaction = {key: value for key, value in safe_interaction.items() if value is not None}

    report = list(getattr(run, "redaction_report", []) or [])
    report.append(
        {
            "field_path": field_path,
            "reason": "redaction_failed",
            "replacement": "<omitted:redaction_failed>",
            "affects_replay": True,
        }
    )
    run.redaction_report = report
    return run


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
            previous_scenarios=request.previous_scenarios,
            config=llm_cfg,
            provider=provider,
        )
        if run.ok:
            run.parsed_output = _normalize_scenarios_for_runtime(list(run.parsed_output or []))
            run.interaction["scenario_hot_start_policy"] = "preserve_explicit_hot_start_add_default_init_cycle"
            try:
                redacted_scenarios, scenario_redaction_report = redact_run_record_payload(
                    {"scenarios": _jsonable(run.parsed_output)},
                    path="llm_interaction.parsed_output",
                )
            except Exception as exc:
                return _mark_llm_run_redaction_failed(
                    run,
                    stage_id=StageId.SL_5_SCENARIO_GENERATION,
                    field_path="llm_interaction.parsed_output",
                    exc=exc,
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
        try:
            prompt_payload, budget_meta = _select_sl9_prompt_payload(request, llm_cfg)
        except LG_C2_ContextRedactionBlocked as exc:
            return _lg_c2_context_redaction_blocked_run(exc=exc, provider=provider, cfg=llm_cfg)
        run = run_sl9_repair_llm(
            nl=request.nl,
            current_dsl=request.old_dsl,
            fix_plan=prompt_payload["fix_plan_summary"],
            fix_request_batch=prompt_payload["fix_request_batch"],
            fix_log=prompt_payload["fix_log"],
            repair_memory=prompt_payload["repair_memory"],
            grounding_map=prompt_payload["grounding_map_summary"],
            selected_diagnostics=prompt_payload["selected_diagnostics"],
            preserve_list=prompt_payload["preserve_list"],
            scenario_summary=prompt_payload["scenario_summary"],
            repair_target=getattr(request.fix_plan, "target", None),
            config=llm_cfg,
            provider=provider,
        )
        if hasattr(run, "interaction") and isinstance(run.interaction, dict):
            run.interaction["context_engineering"] = budget_meta
        return run

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

    def sl10_review(request: RepairRequest, _local_review: Any) -> Any:
        if request.fix_request_batch is None or request.sl9_decision is None:
            raise TypeError("SL-10 repair review requires FixRequestBatch and SL9 decisions")
        try:
            prompt_payload, budget_meta = _select_sl10_prompt_payload(request, llm_cfg)
        except LG_C2_ContextRedactionBlocked as exc:
            return _lg_c2_context_redaction_blocked_run(exc=exc, provider=provider, cfg=llm_cfg)
        run = run_sl10_repair_review_llm(
            nl=request.nl,
            grounding_map=prompt_payload["grounding_map"],
            old_dsl=request.old_dsl,
            candidate_dsl=request.candidate_dsl,
            request_batch=prompt_payload["request_batch"],
            sl9_decisions=prompt_payload["sl9_decisions"],
            fix_log=prompt_payload["fix_log"],
            diff_summary=prompt_payload["diff_summary"],
            local_check_evidence=prompt_payload["local_check_evidence"],
            scenario_summary=prompt_payload["scenario_summary"],
            review_policy={"mode": cfg.delta_review_mode, **_jsonable(cfg.feedback_policy)},
            config=llm_cfg,
            provider=provider,
        )
        if hasattr(run, "interaction") and isinstance(run.interaction, dict):
            run.interaction["context_engineering"] = budget_meta
        return run

    adapters = build_full_staged_runtime_adapters(
        scenario_generate=scenario_generate,
        repair=repair,
        model_review=model_review,
        policy_profile=cfg.policy_profile,
        sl10_review=sl10_review,
        delta_review=None,
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
            "use method.experiments.ablation for deterministic replay/ablation diagnostics."
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
    adapters = _build_runtime_adapters(cfg, llm_cfg=llm_cfg, provider=provider)
    from method.langgraph_runtime import run_full_staged_langgraph_runtime

    result = run_full_staged_langgraph_runtime(
        nl,
        config=cfg,
        adapters=adapters,
        initial_dsl=seed_dsl or "",
        planned_stage_graph=graph,
        resolved_config=resolved_config,
        run_id=run_id,
        provider=provider,
        called_from_loop=True,
    )
    result.resolved_config = resolved_config
    result.planned_stage_graph = graph
    return result
