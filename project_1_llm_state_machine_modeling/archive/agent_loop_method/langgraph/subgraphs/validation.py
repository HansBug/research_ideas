"""LG-M1-D3 split module for validation subgraph.

This module owns the physical implementation moved out of
``archive.agent_loop_method.langgraph_runtime``.  It imports LG-C1 graph-state contracts and shared
runtime helpers from ``archive.agent_loop_method.langgraph.core`` without importing the legacy
facade, preserving the academic evidence path while making the D3 architecture
readable by file name.
"""

from __future__ import annotations

from archive.agent_loop_method.langgraph.core import *  # noqa: F403 - D3 compatibility split keeps shared helper names private.


def _d3_state_graph_factory() -> Any:
    """Return facade-monkeypatchable StateGraph for legacy characterization tests."""

    import sys

    facade = sys.modules.get("archive.agent_loop_method.langgraph_runtime")
    if facade is not None and hasattr(facade, "StateGraph"):
        return getattr(facade, "StateGraph")
    return StateGraph

class _ValidationSubgraphState(_GraphLoopState, total=False):
    """State carried by the LG-B1 validation subgraph.

    The subgraph mutates the canonical ``_RunState`` object in the same way as
    the old validation pass helper, but the orchestration edges are now explicit
    LangGraph nodes.  ``validation_*`` keys are transient subgraph channels and
    are not the academic evidence source; SC-13 still writes
    ``AgentLoopRunRecord`` as the canonical ledger.
    """

    validation_context: StageContext
    validation_feedback: dict[str, Any]
    validation_stage_metas: list[Any]
    validation_scenario_history: list[dict[str, Any]]
    validation_scenario_set: Any
    validation_scenario_epoch: int
    validation_oracle_weak: bool
    validation_scenario_phase_complete: bool
    validation_attempt_index: int
    validation_retry_mode: str
    validation_coverage_directive: Any
    validation_previous_scenarios: list[Any]
    validation_selected_scenarios: list[Any]
    validation_selected_coverage: dict[str, Any]
    validation_scenario_merge: dict[str, Any]
    validation_raw_generated_scenario_count: int
    validation_coverage_gap: bool
    validation_dsl_changed_since_freeze: bool
    validation_next_epoch: int
    validation_result: Any
    validation_continuation_source: Any
    validation_continued_after_waiver: bool
    validation_waiver_audit: Any
    validation_lg_e2_send_metadata: dict[str, Any]


def _build_validation_subgraph(
    *,
    runtime_cfg: FullStagedRuntimeConfig,
    adapters: FullStagedRuntimeAdapters,
) -> Any:
    """Build the LG-B1 stage-level validation subgraph.

    The canonical stage semantics remain in ``archive.agent_loop_method.staged_runtime`` helpers
    and adapters, while LangGraph now owns the SD-2→SL-7 validation routing.
    """

    graph = _d3_state_graph_factory()(_ValidationSubgraphState)

    def _state(graph_state: _ValidationSubgraphState) -> _ValidationSubgraphState:
        return dict(graph_state)

    def _runtime_state(graph_state: _ValidationSubgraphState) -> _RunState:
        return graph_state["runtime_state"]

    def _iteration(graph_state: _ValidationSubgraphState) -> int:
        return int(graph_state.get("iteration", 0))

    def _validation_result(graph_state: _ValidationSubgraphState, *, scenario_epoch: int | None) -> _ValidationPass:
        feedback = dict(graph_state.get("validation_feedback") or {})
        return _ValidationPass(
            graph_state["validation_context"],
            feedback,
            list(graph_state.get("validation_stage_metas") or []),
            _select_first_blocking(feedback),
            graph_state.get("validation_scenario_set"),
            list(graph_state.get("validation_scenario_history") or []),
            bool(graph_state.get("validation_oracle_weak", False)),
            scenario_epoch,
        )

    def validation_enter(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        scenario_set = runtime_state.scenario_set
        _trace_node(graph_state, "validation_subgraph", event="subgraph_enter", iteration=iteration)
        _append_flow_log(
            runtime_state.logs,
            event="iteration_validation_enter",
            iteration=iteration,
            current_dsl_hash=_hash_text(runtime_state.current_dsl),
            scenario_set_id=scenario_set.scenario_set_id if scenario_set is not None else None,
            oracle_weak=runtime_state.oracle_weak,
            dsl=runtime_state.current_dsl,
            graph_subgraph="validation_subgraph",
        )
        continuation_source = graph_state.get("validation_continuation_source")
        if isinstance(continuation_source, _ValidationPass):
            source, selected_feedback, source_stage = continuation_source.selected or ("", None, "")
            waiver_audit = graph_state.get("validation_waiver_audit")
            if (
                isinstance(waiver_audit, dict)
                and waiver_audit.get("kind") in {"stale_overridden_scenario_waiver", "sl10_noop_override_waiver"}
                and source == FeedbackSource.SIM.value
                and source_stage == StageId.SD_6_SIM.value
                and isinstance(selected_feedback, SimFeedback)
            ):
                waiver_kind = str(waiver_audit.get("kind") or "")
                if waiver_kind == "sl10_noop_override_waiver":
                    enter_reason = "SL-10 accepted a no-op override for the current SD-6 scenario request; continue to SL-7 without DSL edit"
                    stage_reason = "sl10_noop_override_waiver_marked_non_blocking_for_SL-7"
                    skipped_reason = (
                        "waiver_continue: SL-10 passed a no-op candidate with local_override_rationale "
                        "for the current SD-6 scenario_regression; continuing to SL-7 without SC-11 "
                        "budget consumption or DSL edit"
                    )
                else:
                    enter_reason = "SL-9 rejected stale overridden SD-6 scenario request; continue to SL-7 without DSL edit"
                    stage_reason = "stale_overridden_scenario_waiver_marked_non_blocking_for_SL-7"
                    skipped_reason = (
                        "waiver_continue: stale SD-6 scenario hard request was rejected by SL-9 "
                        "and matched a prior SL-10 local_override_rationale for the same scenario; "
                        "continuing to SL-7 without DSL edit"
                    )
                context = _clone_stage_context(continuation_source.context, current_dsl=runtime_state.current_dsl)
                context.warning_budget_state = continuation_source.context.warning_budget_state
                scenario_set = continuation_source.scenario_set
                context.scenario_set = scenario_set
                feedback = dict(continuation_source.feedback)
                waived_sim = _make_waived_sim_feedback(selected_feedback, waiver_audit)
                feedback[FeedbackSource.SIM.value] = waived_sim
                stage_metas = list(continuation_source.stage_metas)
                scenario_history = list(continuation_source.scenario_history)

                waiver_meta = _meta(StageId.SD_6_SIM, ok=True, status=StageStatus.ADVISORY)
                waiver_meta.input_hash = _hash_text(runtime_state.current_dsl)
                waiver_meta.output_hash = _short_hash(waiver_audit)
                waiver_meta.skipped_reason = skipped_reason
                _trace_node(
                    graph_state,
                    "validation_sd6_sim",
                    iteration=iteration,
                    continued_after_waiver=True,
                    waiver_audit_kind=waiver_audit.get("kind"),
                )
                _append_stage(runtime_state.stage_records, waiver_meta)
                stage_metas.append(waiver_meta)
                _append_flow_log(
                    runtime_state.logs,
                    event="waiver_continue_validation_enter",
                    iteration=iteration,
                    source_stage=StageId.SD_6_SIM.value,
                    reason=enter_reason,
                    current_dsl_hash=_hash_text(runtime_state.current_dsl),
                    current_dsl=runtime_state.current_dsl,
                    waiver_audit=_jsonable(waiver_audit),
                    graph_subgraph="validation_subgraph",
                    graph_node="validation_enter",
                )
                _append_flow_log(
                    runtime_state.logs,
                    event="stage_result",
                    stage_id=StageId.SD_6_SIM.value,
                    iteration=iteration,
                    ok=True,
                    status=str(StageStatus.ADVISORY),
                    reason=stage_reason,
                    feedback=_feedback_brief(StageId.SD_6_SIM.value, waived_sim),
                    jump="SL-7",
                    graph_subgraph="validation_subgraph",
                    graph_node="validation_sd6_sim",
                )
                graph_state["validation_context"] = context
                graph_state["validation_feedback"] = feedback
                graph_state["validation_stage_metas"] = stage_metas
                graph_state["validation_scenario_history"] = scenario_history
                graph_state["validation_scenario_set"] = scenario_set
                graph_state["validation_scenario_epoch"] = continuation_source.scenario_epoch
                graph_state["validation_oracle_weak"] = continuation_source.oracle_weak
                graph_state["validation_continued_after_waiver"] = True
                graph_state["validation_waiver_audit"] = _jsonable(waiver_audit)
                _trace_node(
                    graph_state,
                    "validation_sl7_model_review",
                    iteration=iteration,
                    continued_after_waiver=True,
                    waiver_audit_kind=waiver_audit.get("kind"),
                )
                return Command(goto="validation_sl7_model_review", update=graph_state)
            if (
                source != FeedbackSource.DESIGN.value
                or source_stage != StageId.SD_4_DESIGN.value
                or not isinstance(selected_feedback, DesignFeedback)
            ):
                graph_state["validation_result"] = continuation_source
                return Command(goto="validation_finalize", update=graph_state)
            context = _clone_stage_context(continuation_source.context, current_dsl=runtime_state.current_dsl)
            context.warning_budget_state = continuation_source.context.warning_budget_state
            waived_design = _make_waived_design_feedback(selected_feedback)
            feedback = dict(continuation_source.feedback)
            feedback[FeedbackSource.DESIGN.value] = waived_design
            stage_metas = list(continuation_source.stage_metas)
            scenario_history = list(continuation_source.scenario_history)
            scenario_set = continuation_source.scenario_set
            waiver_meta = _meta(StageId.SD_4_DESIGN, ok=True, status=StageStatus.ADVISORY)
            waiver_meta.input_hash = _hash_text(runtime_state.current_dsl)
            waiver_meta.output_hash = _short_hash([item.instance_key for item in selected_feedback.blocking_items])
            waiver_meta.skipped_reason = (
                "waiver_continue: non-hard SD-4 blocking warnings were rejected/waived by "
                "SL-9; continuing downstream validation without DSL edit"
            )
            _trace_node(graph_state, "validation_sd4_design", iteration=iteration, continued_after_waiver=True)
            _append_stage(runtime_state.stage_records, waiver_meta)
            stage_metas.append(waiver_meta)
            _append_flow_log(
                runtime_state.logs,
                event="waiver_continue_validation_enter",
                iteration=iteration,
                source_stage=StageId.SD_4_DESIGN.value,
                reason="SL-9 rejected/waived non-hard SD-4 requests; continue downstream without SC-11 DSL edit",
                current_dsl_hash=_hash_text(runtime_state.current_dsl),
                current_dsl=runtime_state.current_dsl,
                graph_subgraph="validation_subgraph",
                graph_node="validation_enter",
            )
            _append_flow_log(
                runtime_state.logs,
                event="stage_result",
                stage_id=StageId.SD_4_DESIGN.value,
                iteration=iteration,
                ok=True,
                status=str(StageStatus.ADVISORY),
                reason="waiver_continue_design_items_marked_non_blocking_for_downstream_validation",
                jump="SL-5" if scenario_set is None else "SD-5A",
                graph_subgraph="validation_subgraph",
                graph_node="validation_sd4_design",
            )
            graph_state["validation_context"] = context
            graph_state["validation_feedback"] = feedback
            graph_state["validation_stage_metas"] = stage_metas
            graph_state["validation_scenario_history"] = scenario_history
            graph_state["validation_scenario_set"] = scenario_set
            graph_state["validation_scenario_epoch"] = runtime_state.scenario_epoch
            graph_state["validation_oracle_weak"] = continuation_source.oracle_weak
            graph_state["validation_continued_after_waiver"] = True
            if scenario_set is None:
                graph_state["validation_retry_mode"] = "initial"
                graph_state["validation_attempt_index"] = 0
                graph_state["validation_coverage_directive"] = None
                graph_state["validation_previous_scenarios"] = []
                graph_state["validation_selected_scenarios"] = []
                graph_state["validation_selected_coverage"] = {"coverage_report": {}, "coverage_gap": False, "retry_directive": None}
                _trace_node(graph_state, "validation_sl5_scenario_generation", iteration=iteration, attempt_index=0, continued_after_waiver=True)
                return Command(goto="validation_sl5_scenario_generation", update=graph_state)
            _trace_node(graph_state, "validation_sd5a_reuse_coverage", iteration=iteration, continued_after_waiver=True)
            return Command(goto="validation_sd5a_reuse_coverage", update=graph_state)

        graph_state["validation_context"] = StageContext(
            nl=graph_state["nl"],
            current_dsl=runtime_state.current_dsl,
            grounding_map=runtime_cfg.grounding_map,
            scenario_set=scenario_set,
            warning_budget_state=runtime_state.warning_budget_state or {},
        )
        graph_state["validation_feedback"] = {}
        graph_state["validation_stage_metas"] = []
        graph_state["validation_scenario_history"] = []
        graph_state["validation_scenario_set"] = scenario_set
        graph_state["validation_scenario_epoch"] = runtime_state.scenario_epoch
        graph_state["validation_oracle_weak"] = runtime_state.oracle_weak
        _trace_node(graph_state, "validation_sd2_parse", iteration=iteration)
        return Command(goto="validation_sd2_parse", update=graph_state)

    def validation_sd2_parse(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        context: StageContext = graph_state["validation_context"]
        feedback = dict(graph_state.get("validation_feedback") or {})
        stage_metas = list(graph_state.get("validation_stage_metas") or [])
        _append_flow_log(runtime_state.logs, event="stage_enter", stage_id=StageId.SD_2_PARSE.value, iteration=iteration, reason="full_validation_pass")
        parse_feedback, parse_meta = _lg_e3_fixed_tool_call(
            graph_state,
            tool_name="sd2_parse",
            stage_id=StageId.SD_2_PARSE.value,
            graph_node="validation_sd2_parse",
            iteration=iteration,
            input_payload={"current_dsl": runtime_state.current_dsl, "context": context},
            call=lambda: adapters.parse(runtime_state.current_dsl, context),
        )
        feedback[FeedbackSource.PARSE.value] = parse_feedback
        _append_stage(runtime_state.stage_records, parse_meta)
        stage_metas.append(parse_meta)
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SD_2_PARSE.value,
            iteration=iteration,
            ok=parse_feedback.ok,
            status=str(parse_meta.status),
            feedback=_feedback_brief(StageId.SD_2_PARSE.value, parse_feedback),
            jump="SD-3" if parse_feedback.ok else "SD-8",
            graph_subgraph="validation_subgraph",
            graph_node="validation_sd2_parse",
        )
        graph_state["validation_feedback"] = feedback
        graph_state["validation_stage_metas"] = stage_metas
        if not parse_feedback.ok:
            graph_state["validation_result"] = _validation_result(graph_state, scenario_epoch=None)
            return Command(goto="validation_finalize", update=graph_state)
        _trace_node(graph_state, "validation_sd3_semantic", iteration=iteration)
        return Command(goto="validation_sd3_semantic", update=graph_state)

    def validation_sd3_semantic(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        context: StageContext = graph_state["validation_context"]
        feedback = dict(graph_state.get("validation_feedback") or {})
        stage_metas = list(graph_state.get("validation_stage_metas") or [])
        _append_flow_log(runtime_state.logs, event="stage_enter", stage_id=StageId.SD_3_SEMANTIC.value, iteration=iteration, reason="SD-2 ok")
        semantic_feedback, semantic_meta = _lg_e3_fixed_tool_call(
            graph_state,
            tool_name="sd3_semantic",
            stage_id=StageId.SD_3_SEMANTIC.value,
            graph_node="validation_sd3_semantic",
            iteration=iteration,
            input_payload={"current_dsl": runtime_state.current_dsl, "context": context},
            call=lambda: adapters.semantic(runtime_state.current_dsl, context),
        )
        feedback[FeedbackSource.SEMANTIC.value] = semantic_feedback
        _append_stage(runtime_state.stage_records, semantic_meta)
        stage_metas.append(semantic_meta)
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SD_3_SEMANTIC.value,
            iteration=iteration,
            ok=semantic_feedback.ok,
            status=str(semantic_meta.status),
            feedback=_feedback_brief(StageId.SD_3_SEMANTIC.value, semantic_feedback),
            jump="SD-4" if semantic_feedback.ok else "SD-8",
            graph_subgraph="validation_subgraph",
            graph_node="validation_sd3_semantic",
        )
        graph_state["validation_feedback"] = feedback
        graph_state["validation_stage_metas"] = stage_metas
        if not semantic_feedback.ok:
            graph_state["validation_result"] = _validation_result(graph_state, scenario_epoch=None)
            return Command(goto="validation_finalize", update=graph_state)
        _trace_node(graph_state, "validation_sd4_design", iteration=iteration)
        return Command(goto="validation_sd4_design", update=graph_state)

    def validation_sd4_design(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        context: StageContext = graph_state["validation_context"]
        feedback = dict(graph_state.get("validation_feedback") or {})
        stage_metas = list(graph_state.get("validation_stage_metas") or [])
        scenario_set = graph_state.get("validation_scenario_set")
        _append_flow_log(runtime_state.logs, event="stage_enter", stage_id=StageId.SD_4_DESIGN.value, iteration=iteration, reason="SD-3 ok")
        design_feedback, design_meta = _lg_e3_fixed_tool_call(
            graph_state,
            tool_name="sd4_design",
            stage_id=StageId.SD_4_DESIGN.value,
            graph_node="validation_sd4_design",
            iteration=iteration,
            input_payload={"context": context},
            call=lambda: adapters.design(context),
        )
        feedback[FeedbackSource.DESIGN.value] = design_feedback
        _append_stage(runtime_state.stage_records, design_meta)
        stage_metas.append(design_meta)
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SD_4_DESIGN.value,
            iteration=iteration,
            ok=not bool(design_feedback.blocking_items),
            status=str(design_meta.status),
            feedback=_feedback_brief(StageId.SD_4_DESIGN.value, design_feedback),
            jump="SD-8" if design_feedback.blocking_items else ("SL-5" if scenario_set is None else "SD-5A"),
            graph_subgraph="validation_subgraph",
            graph_node="validation_sd4_design",
        )
        graph_state["validation_feedback"] = feedback
        graph_state["validation_stage_metas"] = stage_metas
        if design_feedback.blocking_items:
            graph_state["validation_result"] = _validation_result(graph_state, scenario_epoch=None)
            return Command(goto="validation_finalize", update=graph_state)
        if scenario_set is None:
            graph_state["validation_retry_mode"] = "initial"
            graph_state["validation_attempt_index"] = 0
            graph_state["validation_coverage_directive"] = None
            graph_state["validation_previous_scenarios"] = []
            graph_state["validation_selected_scenarios"] = []
            graph_state["validation_selected_coverage"] = {"coverage_report": {}, "coverage_gap": False, "retry_directive": None}
            _trace_node(graph_state, "validation_sl5_scenario_generation", iteration=iteration, attempt_index=0)
            return Command(goto="validation_sl5_scenario_generation", update=graph_state)
        _trace_node(graph_state, "validation_sd5a_reuse_coverage", iteration=iteration)
        return Command(goto="validation_sd5a_reuse_coverage", update=graph_state)

    def validation_sl5_scenario_generation(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        context: StageContext = graph_state["validation_context"]
        attempt_index = int(graph_state.get("validation_attempt_index", 0))
        retry_mode = str(graph_state.get("validation_retry_mode") or "initial")
        scenario_epoch = int(graph_state.get("validation_next_epoch", graph_state.get("validation_scenario_epoch", 0))) if retry_mode == "targeted" else int(graph_state.get("validation_scenario_epoch", 0))
        coverage_directive = graph_state.get("validation_coverage_directive")
        previous_scenarios = list(graph_state.get("validation_previous_scenarios") or [])
        _append_flow_log(
            runtime_state.logs,
            event="stage_enter",
            stage_id=StageId.SL_5_SCENARIO_GENERATION.value,
            iteration=iteration,
            reason="scenario_set_absent" if retry_mode == "initial" and attempt_index == 0 else ("scenario_coverage_gap_retry" if retry_mode == "initial" else "targeted_refresh_after_frozen_gap_or_dsl_change"),
            attempt_index=attempt_index,
            coverage_directive=_compact_json(coverage_directive, max_list_items=6),
            previous_scenario_names=[scenario.name for scenario in previous_scenarios],
            graph_subgraph="validation_subgraph",
            graph_node="validation_sl5_scenario_generation",
        )
        request = ScenarioGenerationRequest(
            nl=graph_state["nl"],
            current_dsl=runtime_state.current_dsl,
            context=context,
            attempt_index=attempt_index,
            coverage_directive=coverage_directive,
            previous_scenarios=previous_scenarios,
            scenario_epoch=scenario_epoch,
        )
        generated = _lg_d2_wrap_llm_stage_node(
            graph_state,
            stage_id=StageId.SL_5_SCENARIO_GENERATION,
            graph_node="validation_sl5_scenario_generation",
            subgraph_id="validation_subgraph",
            call=lambda: _append_llm_stage_run(
                run=adapters.scenario_generate(request),
                expected_stage_id=StageId.SL_5_SCENARIO_GENERATION,
                stage_records=runtime_state.stage_records,
                iteration_stage_metas=graph_state["validation_stage_metas"],
                llm_interactions=runtime_state.llm_interactions,
                logs=runtime_state.logs,
                iteration=iteration,
                parsed_summary={"attempt_index": attempt_index, "kind": "scenario_generation" if retry_mode == "initial" else "scenario_refresh"},
            ),
        )
        raw_scenarios = list(getattr(generated, "parsed_output", []) or []) if _is_llm_stage_run(generated) else list(generated or [])
        scenarios, scenario_merge = _merge_scenario_sets_by_name(previous_scenarios, raw_scenarios)
        if _is_llm_stage_run(generated):
            try:
                generated.parsed_output = scenarios
                if isinstance(getattr(generated, "interaction", None), dict):
                    generated.interaction["scenario_merge_policy"] = scenario_merge
            except Exception:
                pass
        else:
            sl5_meta = _meta(StageId.SL_5_SCENARIO_GENERATION, ok=True)
            sl5_meta.input_hash = _hash_text(runtime_state.current_dsl)
            sl5_meta.output_hash = _short_hash(scenarios)
            _append_stage(runtime_state.stage_records, sl5_meta)
            graph_state["validation_stage_metas"].append(sl5_meta)
        graph_state["validation_selected_scenarios"] = scenarios
        graph_state["validation_scenario_merge"] = _jsonable(scenario_merge)
        graph_state["validation_raw_generated_scenario_count"] = len(raw_scenarios)
        _trace_node(graph_state, "validation_sd5a_scenario_coverage", iteration=iteration, attempt_index=attempt_index)
        return Command(goto="validation_sd5a_scenario_coverage", update=graph_state)

    def validation_sd5a_scenario_coverage(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        scenarios = list(graph_state.get("validation_selected_scenarios") or [])
        attempt_index = int(graph_state.get("validation_attempt_index", 0))
        retry_mode = str(graph_state.get("validation_retry_mode") or "initial")
        coverage, coverage_meta = _lg_e3_fixed_tool_call(
            graph_state,
            tool_name="sd5a_scenario_coverage",
            stage_id=StageId.SD_5A_SCENARIO_COVERAGE.value,
            graph_node="validation_sd5a_scenario_coverage",
            iteration=iteration,
            input_payload={"current_dsl": runtime_state.current_dsl, "scenarios": scenarios, "attempt_index": attempt_index, "retry_mode": retry_mode},
            call=lambda: adapters.scenario_coverage(runtime_state.current_dsl, scenarios),
        )
        _append_stage(runtime_state.stage_records, coverage_meta)
        graph_state["validation_stage_metas"].append(coverage_meta)
        selected_coverage = dict(coverage)
        graph_state["validation_selected_coverage"] = selected_coverage
        gap = bool(coverage.get("coverage_gap"))
        scenario_merge = graph_state.get("validation_scenario_merge") or {}
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SD_5A_SCENARIO_COVERAGE.value,
            iteration=iteration,
            ok=not gap,
            attempt_index=attempt_index,
            status=str(coverage_meta.status),
            n_scenarios=len(scenarios),
            raw_generated_scenario_count=int(graph_state.get("validation_raw_generated_scenario_count", 0)),
            scenario_names=[scenario.name for scenario in scenarios],
            scenario_merge_policy=scenario_merge,
            coverage=_compact_json(coverage, max_list_items=8),
            jump="SC-5F" if not gap else ("SL-5 retry" if attempt_index < runtime_cfg.scenario_max_retries else "SC-5F weak_oracle"),
            graph_subgraph="validation_subgraph",
            graph_node="validation_sd5a_scenario_coverage",
        )
        retry_exhausted = gap and attempt_index >= runtime_cfg.scenario_max_retries
        weak = retry_exhausted or bool(selected_coverage.get("oracle_weak"))
        history = list(graph_state.get("validation_scenario_history") or [])
        item = _scenario_history_item(
            iteration=iteration,
            attempt_index=attempt_index,
            scenarios=scenarios,
            coverage=coverage,
            coverage_meta=coverage_meta,
            retry_exhausted=retry_exhausted,
            oracle_weak=weak,
        )
        if retry_mode == "targeted":
            previous_set = graph_state.get("validation_scenario_set")
            item.update(
                {
                    "targeted_retry_after_frozen_gap": bool(graph_state.get("validation_coverage_gap")),
                    "targeted_retry_after_dsl_change": bool(graph_state.get("validation_dsl_changed_since_freeze")),
                    "previous_scenario_set_id": getattr(previous_set, "scenario_set_id", None),
                    "previous_source_dsl_hash": getattr(previous_set, "source_dsl_hash", None),
                    "current_dsl_hash": _hash_text(runtime_state.current_dsl),
                }
            )
        item["scenario_merge_policy"] = _jsonable(scenario_merge)
        history.append(item)
        graph_state["validation_scenario_history"] = history
        graph_state["validation_oracle_weak"] = weak
        if not gap or attempt_index >= runtime_cfg.scenario_max_retries:
            _trace_node(graph_state, "validation_sc5f_scenario_freeze", iteration=iteration)
            return Command(goto="validation_sc5f_scenario_freeze", update=graph_state)
        graph_state["validation_coverage_directive"] = coverage.get("retry_directive") or {"retry_reason": "coverage_gap" if retry_mode == "initial" else "frozen_scenario_coverage_gap"}
        graph_state["validation_previous_scenarios"] = scenarios
        graph_state["validation_attempt_index"] = attempt_index + 1
        _trace_node(graph_state, "validation_sl5_scenario_generation", iteration=iteration, attempt_index=attempt_index + 1)
        return Command(goto="validation_sl5_scenario_generation", update=graph_state)

    def validation_sd5a_reuse_coverage(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        context: StageContext = graph_state["validation_context"]
        scenario_set = graph_state["validation_scenario_set"]
        current_dsl_hash = _hash_text(runtime_state.current_dsl)
        dsl_changed_since_freeze = bool(scenario_set.source_dsl_hash and scenario_set.source_dsl_hash != current_dsl_hash)
        coverage, coverage_meta = _lg_e3_fixed_tool_call(
            graph_state,
            tool_name="sd5a_scenario_coverage",
            stage_id=StageId.SD_5A_SCENARIO_COVERAGE.value,
            graph_node="validation_sd5a_reuse_coverage",
            iteration=iteration,
            input_payload={"current_dsl": runtime_state.current_dsl, "scenarios": list(scenario_set.scenarios), "scenario_set_id": scenario_set.scenario_set_id},
            call=lambda: adapters.scenario_coverage(runtime_state.current_dsl, list(scenario_set.scenarios)),
        )
        _append_stage(runtime_state.stage_records, coverage_meta)
        graph_state["validation_stage_metas"].append(coverage_meta)
        gap = bool(coverage.get("coverage_gap"))
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SD_5A_SCENARIO_COVERAGE.value,
            iteration=iteration,
            ok=not gap and not dsl_changed_since_freeze,
            reason="reuse_frozen_scenario_set",
            scenario_set_id=scenario_set.scenario_set_id,
            coverage_gap=gap,
            dsl_changed_since_freeze=dsl_changed_since_freeze,
            coverage=_compact_json(coverage, max_list_items=8),
            jump="SC-5F reuse" if not gap and not dsl_changed_since_freeze else "SL-5 targeted_retry",
            graph_subgraph="validation_subgraph",
            graph_node="validation_sd5a_reuse_coverage",
        )
        item = _scenario_history_item(
            iteration=iteration,
            attempt_index=0,
            scenarios=list(scenario_set.scenarios),
            coverage=coverage,
            coverage_meta=coverage_meta,
            retry_exhausted=False,
            oracle_weak=False,
        )
        item.update(
            {
                "scenario_set_id": scenario_set.scenario_set_id,
                "epoch": scenario_set.epoch,
                "reused_frozen_oracle": True,
                "dsl_changed_since_freeze": dsl_changed_since_freeze,
                "previous_source_dsl_hash": scenario_set.source_dsl_hash,
                "current_dsl_hash": current_dsl_hash,
            }
        )
        graph_state["validation_scenario_history"] = list(graph_state.get("validation_scenario_history") or []) + [item]
        if not gap and not dsl_changed_since_freeze:
            freeze_meta = _meta(StageId.SC_5F_SCENARIO_FREEZE, ok=True)
            freeze_meta.input_hash = _hash_text(runtime_state.current_dsl)
            freeze_meta.output_hash = _hash_text(scenario_set.scenario_set_id)
            _append_stage(runtime_state.stage_records, freeze_meta)
            graph_state["validation_stage_metas"].append(freeze_meta)
            _append_flow_log(
                runtime_state.logs,
                event="stage_result",
                stage_id=StageId.SC_5F_SCENARIO_FREEZE.value,
                iteration=iteration,
                ok=True,
                reason="reused_frozen_scenario_set",
                scenario_set_id=scenario_set.scenario_set_id,
                epoch=scenario_set.epoch,
                n_scenarios=len(scenario_set.scenarios),
                jump="SD-6",
                graph_subgraph="validation_subgraph",
                graph_node="validation_sc5f_scenario_freeze",
            )
            graph_state["validation_oracle_weak"] = False
            graph_state["validation_scenario_epoch"] = scenario_set.epoch + 1
            context.scenario_set = scenario_set
            _trace_node(graph_state, "validation_sd6_sim", iteration=iteration)
            return Command(goto="validation_sd6_sim", update=graph_state)
        graph_state["validation_retry_mode"] = "targeted"
        graph_state["validation_coverage_directive"] = coverage.get("retry_directive") or {
            "retry_reason": "dsl_changed_since_scenario_freeze" if dsl_changed_since_freeze else "frozen_scenario_coverage_gap",
            "previous_scenario_set_id": scenario_set.scenario_set_id,
            "previous_source_dsl_hash": scenario_set.source_dsl_hash,
            "current_dsl_hash": current_dsl_hash,
        }
        graph_state["validation_previous_scenarios"] = list(scenario_set.scenarios)
        graph_state["validation_selected_scenarios"] = list(scenario_set.scenarios)
        graph_state["validation_selected_coverage"] = dict(coverage)
        graph_state["validation_coverage_gap"] = gap
        graph_state["validation_dsl_changed_since_freeze"] = dsl_changed_since_freeze
        graph_state["validation_next_epoch"] = scenario_set.epoch + 1
        graph_state["validation_oracle_weak"] = (runtime_cfg.scenario_max_retries == 0 and (gap or dsl_changed_since_freeze)) or bool(dict(coverage).get("oracle_weak"))
        _append_flow_log(
            runtime_state.logs,
            event="frozen_scenario_refresh_targeted_retry",
            level="warning",
            iteration=iteration,
            scenario_set_id=scenario_set.scenario_set_id,
            scenario_max_retries=runtime_cfg.scenario_max_retries,
            coverage_gap=gap,
            dsl_changed_since_freeze=dsl_changed_since_freeze,
            graph_subgraph="validation_subgraph",
        )
        if runtime_cfg.scenario_max_retries == 0:
            _trace_node(graph_state, "validation_sc5f_scenario_freeze", iteration=iteration)
            return Command(goto="validation_sc5f_scenario_freeze", update=graph_state)
        graph_state["validation_attempt_index"] = 1
        _trace_node(graph_state, "validation_sl5_scenario_generation", iteration=iteration, attempt_index=1)
        return Command(goto="validation_sl5_scenario_generation", update=graph_state)

    def validation_sc5f_scenario_freeze(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        context: StageContext = graph_state["validation_context"]
        retry_mode = str(graph_state.get("validation_retry_mode") or "initial")
        scenarios = list(graph_state.get("validation_selected_scenarios") or [])
        selected_coverage = dict(graph_state.get("validation_selected_coverage") or {})
        weak = bool(graph_state.get("validation_oracle_weak", False))
        if weak:
            selected_coverage = {
                **selected_coverage,
                "oracle_weak": True,
                "weak_oracle_reason": "scenario_refresh_retry_exhausted" if retry_mode == "targeted" else "scenario_coverage_retry_exhausted",
            }
            _append_flow_log(
                runtime_state.logs,
                event="scenario_refresh_retry_exhausted" if retry_mode == "targeted" else "scenario_coverage_retry_exhausted",
                level="warning",
                iteration=iteration,
                scenario_max_retries=runtime_cfg.scenario_max_retries,
                coverage_gap=graph_state.get("validation_coverage_gap"),
                dsl_changed_since_freeze=graph_state.get("validation_dsl_changed_since_freeze"),
                graph_subgraph="validation_subgraph",
            )
        epoch = int(graph_state.get("validation_next_epoch", graph_state.get("validation_scenario_epoch", 0))) if retry_mode == "targeted" else int(graph_state.get("validation_scenario_epoch", 0))
        scenario_set, freeze_meta = _lg_e3_fixed_tool_call(
            graph_state,
            tool_name="sc5f_freeze_scenario_set",
            stage_id=StageId.SC_5F_SCENARIO_FREEZE.value,
            graph_node="validation_sc5f_scenario_freeze",
            iteration=iteration,
            input_payload={
                "scenarios": scenarios,
                "source_dsl_hash": _hash_text(runtime_state.current_dsl),
                "source_inspect_hash": _short_hash(context.inspect_json) if context.inspect_json is not None else "",
                "source_grounding_hash": _short_hash(runtime_cfg.grounding_map) if runtime_cfg.grounding_map is not None else None,
                "coverage_report": selected_coverage,
                "epoch": epoch,
            },
            call=lambda: freeze_scenario_set(
                scenarios,
                source_dsl_hash=_hash_text(runtime_state.current_dsl),
                source_inspect_hash=_short_hash(context.inspect_json) if context.inspect_json is not None else "",
                source_grounding_hash=_short_hash(runtime_cfg.grounding_map) if runtime_cfg.grounding_map is not None else None,
                coverage_report=selected_coverage,
                epoch=epoch,
            ),
        )
        scenario_set.coverage_report["oracle_weak"] = weak
        _append_stage(runtime_state.stage_records, freeze_meta)
        graph_state["validation_stage_metas"].append(freeze_meta)
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SC_5F_SCENARIO_FREEZE.value,
            iteration=iteration,
            ok=True,
            reason="refreshed_scenario_set" if retry_mode == "targeted" else None,
            scenario_set_id=scenario_set.scenario_set_id,
            epoch=scenario_set.epoch,
            n_scenarios=len(scenario_set.scenarios),
            oracle_weak=weak,
            source_dsl_hash=scenario_set.source_dsl_hash,
            jump="SD-6",
            graph_subgraph="validation_subgraph",
            graph_node="validation_sc5f_scenario_freeze",
        )
        history = list(graph_state.get("validation_scenario_history") or [])
        if history:
            history[-1]["scenario_set_id"] = scenario_set.scenario_set_id
            history[-1]["epoch"] = scenario_set.epoch
            history[-1]["oracle_weak"] = weak
        graph_state["validation_scenario_history"] = history
        graph_state["validation_scenario_set"] = scenario_set
        graph_state["validation_scenario_epoch"] = scenario_set.epoch + 1
        graph_state["validation_oracle_weak"] = weak
        context.scenario_set = scenario_set
        _trace_node(graph_state, "validation_sd6_sim", iteration=iteration)
        return Command(goto="validation_sd6_sim", update=graph_state)

    def validation_sd6_sim(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        context: StageContext = graph_state["validation_context"]
        feedback = dict(graph_state.get("validation_feedback") or {})
        stage_metas = list(graph_state.get("validation_stage_metas") or [])
        scenario_set = graph_state["validation_scenario_set"]
        context.scenario_set = scenario_set
        _append_flow_log(
            runtime_state.logs,
            event="stage_enter",
            stage_id=StageId.SD_6_SIM.value,
            iteration=iteration,
            reason="waiver_continue_scenario_set_ready" if graph_state.get("validation_continued_after_waiver") else "scenario_set_ready",
            scenario_set_id=scenario_set.scenario_set_id,
            n_scenarios=len(scenario_set.scenarios),
            graph_subgraph="validation_subgraph",
            graph_node="validation_sd6_sim",
        )
        sim_feedback, sim_meta, lg_e2_metadata = _lg_e2_run_sd6_send_parallel_or_serial(
            graph_state,
            runtime_cfg=runtime_cfg,
            adapters=adapters,
            current_dsl=runtime_state.current_dsl,
            scenario_set=scenario_set,
            context=context,
            iteration=iteration,
            enabled_requested=bool(runtime_cfg.run_config_extra.get("lg_e2_send_parallel_enabled", True)),
        )
        feedback[FeedbackSource.SIM.value] = sim_feedback
        lg_e2_metadata = {
            **lg_e2_metadata,
            "iteration": iteration,
            "stage_id": StageId.SD_6_SIM.value,
            "scenario_set_id": scenario_set.scenario_set_id,
            "sim_meta_hash": _hash_payload(sim_meta),
        }
        graph_state["validation_lg_e2_send_metadata"] = _jsonable(lg_e2_metadata)
        lg_e2_events = list(graph_state.get("lg_e2_send_parallel_events", []) or [])
        lg_e2_events.append(_jsonable(lg_e2_metadata))
        graph_state["lg_e2_send_parallel_events"] = lg_e2_events
        _append_flow_log(
            runtime_state.logs,
            event="lg_e2_send_parallel_result",
            stage_id=StageId.SD_6_SIM.value,
            iteration=iteration,
            parallel_send_enabled=bool(lg_e2_metadata.get("parallel_send_enabled")),
            fallback_reason=lg_e2_metadata.get("fallback_reason"),
            fanout_count=lg_e2_metadata.get("fanout_count"),
            worker_count=lg_e2_metadata.get("worker_count"),
            serial_equivalence_hash=lg_e2_metadata.get("serial_equivalence_hash"),
            canonical_result_hash=lg_e2_metadata.get("canonical_result_hash"),
            selected_feedback_digest=lg_e2_metadata.get("selected_feedback_digest"),
            scenario_epoch=lg_e2_metadata.get("scenario_epoch"),
            oracle_weak=lg_e2_metadata.get("oracle_weak"),
            lg_e2_metadata=_jsonable(lg_e2_metadata),
            does_not_replace_academic_evidence=True,
            graph_subgraph="validation_subgraph",
            graph_node="validation_sd6_sim",
        )
        _append_lg_d1_operator_event(
            graph_state,
            event_type="lg_e2_send_parallel_result",
            node="validation_sd6_sim",
            stage_id=StageId.SD_6_SIM.value,
            payload={
                "parallel_send_enabled": bool(lg_e2_metadata.get("parallel_send_enabled")),
                "fallback_reason": lg_e2_metadata.get("fallback_reason"),
                "fanout_count": lg_e2_metadata.get("fanout_count"),
                "worker_count": lg_e2_metadata.get("worker_count"),
                "serial_equivalence_hash": lg_e2_metadata.get("serial_equivalence_hash"),
                "canonical_result_hash": lg_e2_metadata.get("canonical_result_hash"),
                "does_not_replace_academic_evidence": True,
            },
        )
        _append_stage(runtime_state.stage_records, sim_meta)
        stage_metas.append(sim_meta)
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SD_6_SIM.value,
            iteration=iteration,
            ok=sim_feedback.ok,
            status=str(sim_meta.status),
            feedback=_feedback_brief(StageId.SD_6_SIM.value, sim_feedback),
            jump="SL-7" if sim_feedback.ok else ("SC-12 weak_oracle" if getattr(sim_feedback, "oracle_weak", False) else "SD-8"),
            graph_subgraph="validation_subgraph",
            graph_node="validation_sd6_sim",
        )
        graph_state["validation_feedback"] = feedback
        graph_state["validation_stage_metas"] = stage_metas
        if not sim_feedback.ok:
            if getattr(sim_feedback, "oracle_weak", False):
                _append_flow_log(
                    runtime_state.logs,
                    event="sim_failed_but_oracle_weak",
                    level="warning",
                    stage_id=StageId.SD_6_SIM.value,
                    iteration=iteration,
                    weak_oracle_reason=getattr(sim_feedback, "weak_oracle_reason", ""),
                    weak_oracle_evidence=_jsonable(getattr(sim_feedback, "weak_oracle_evidence", {})),
                    after_waiver_continue=bool(graph_state.get("validation_continued_after_waiver", False)),
                    graph_subgraph="validation_subgraph",
                    graph_node="validation_sd6_sim",
                )
                graph_state["validation_oracle_weak"] = True
            graph_state["validation_result"] = _validation_result(graph_state, scenario_epoch=scenario_set.epoch)
            return Command(goto="validation_finalize", update=graph_state)
        _trace_node(graph_state, "validation_sl7_model_review", iteration=iteration)
        return Command(goto="validation_sl7_model_review", update=graph_state)

    def validation_sl7_model_review(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        context: StageContext = graph_state["validation_context"]
        feedback = dict(graph_state.get("validation_feedback") or {})
        stage_metas = list(graph_state.get("validation_stage_metas") or [])
        scenario_set = graph_state["validation_scenario_set"]
        oracle_weak = bool(graph_state.get("validation_oracle_weak", False))
        waiver_audit = graph_state.get("validation_waiver_audit")
        waiver_audit_kind = waiver_audit.get("kind") if isinstance(waiver_audit, dict) else None
        review_reason = (
            "waiver_continue_SD-6_stale_scenario_request"
            if waiver_audit_kind == "stale_overridden_scenario_waiver"
            else "waiver_continue_SD-6_sl10_noop_override"
            if waiver_audit_kind == "sl10_noop_override_waiver"
            else ("waiver_continue_SD-6 ok" if graph_state.get("validation_continued_after_waiver") else "SD-6 ok")
        )
        _append_flow_log(
            runtime_state.logs,
            event="stage_enter",
            stage_id=StageId.SL_7_MODEL_REVIEW.value,
            iteration=iteration,
            reason=review_reason,
            scenario_set_id=scenario_set.scenario_set_id,
            oracle_weak=oracle_weak,
            waiver_audit=_jsonable(waiver_audit) if isinstance(waiver_audit, dict) else None,
            graph_subgraph="validation_subgraph",
            graph_node="validation_sl7_model_review",
        )
        review_payload = {
            "parse": feedback.get(FeedbackSource.PARSE.value),
            "semantic": feedback.get(FeedbackSource.SEMANTIC.value),
            "design": feedback.get(FeedbackSource.DESIGN.value),
            "sim": feedback.get(FeedbackSource.SIM.value),
            "oracle_weak": oracle_weak,
            "waiver_continue": bool(graph_state.get("validation_continued_after_waiver", False)),
        }
        if isinstance(waiver_audit, dict):
            review_payload["waiver_audit"] = _jsonable(waiver_audit)
        review_run = _lg_d2_wrap_llm_stage_node(
            graph_state,
            stage_id=StageId.SL_7_MODEL_REVIEW,
            graph_node="validation_sl7_model_review",
            subgraph_id="validation_subgraph",
            call=lambda: _append_llm_stage_run(
                run=adapters.model_review(
                    runtime_state.current_dsl,
                    context,
                    review_payload,
                ),
                expected_stage_id=StageId.SL_7_MODEL_REVIEW,
                stage_records=runtime_state.stage_records,
                iteration_stage_metas=stage_metas,
                llm_interactions=runtime_state.llm_interactions,
                logs=runtime_state.logs,
                iteration=iteration,
            ),
        )
        if _is_llm_stage_run(review_run):
            review_feedback = getattr(review_run, "feedback", None)
            if not isinstance(review_feedback, ModelReviewFeedback):
                raise TypeError("SL-7 LLMStageRun must carry ModelReviewFeedback in .feedback")
            review_meta = getattr(review_run, "stage_meta")
        else:
            review_feedback, review_meta = review_run
            _append_stage(runtime_state.stage_records, review_meta)
            stage_metas.append(review_meta)
        feedback[FeedbackSource.MODEL_REVIEW.value] = review_feedback
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SL_7_MODEL_REVIEW.value,
            iteration=iteration,
            ok=not _model_review_blocks(review_feedback),
            status=str(review_meta.status),
            feedback=_feedback_brief(StageId.SL_7_MODEL_REVIEW.value, review_feedback),
            jump="SD-8" if _model_review_blocks(review_feedback) else "SC-12 success",
            graph_subgraph="validation_subgraph",
            graph_node="validation_sl7_model_review",
        )
        if isinstance(review_feedback, ModelReviewFeedback):
            hints = _extract_grounding_update_hints(source_stage_id=StageId.SL_7_MODEL_REVIEW.value, payload=review_feedback)
            _apply_grounding_update_hints(
                cfg=runtime_cfg,
                state=runtime_state,
                hints=hints,
                iteration=iteration,
                source_stage_id=StageId.SL_7_MODEL_REVIEW.value,
            )
        graph_state["validation_feedback"] = feedback
        graph_state["validation_stage_metas"] = stage_metas
        graph_state["validation_result"] = _validation_result(graph_state, scenario_epoch=scenario_set.epoch)
        return Command(goto="validation_finalize", update=graph_state)

    def validation_finalize(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        _trace_node(graph_state, "validation_finalize", event="subgraph_exit", iteration=graph_state.get("iteration"))
        return Command(goto=END, update=graph_state)

    graph.add_node("validation_enter", validation_enter)
    graph.add_node("validation_sd2_parse", validation_sd2_parse)
    graph.add_node("validation_sd3_semantic", validation_sd3_semantic)
    graph.add_node("validation_sd4_design", validation_sd4_design)
    graph.add_node("validation_sl5_scenario_generation", validation_sl5_scenario_generation)
    graph.add_node("validation_sd5a_scenario_coverage", validation_sd5a_scenario_coverage)
    graph.add_node("validation_sd5a_reuse_coverage", validation_sd5a_reuse_coverage)
    graph.add_node("validation_sc5f_scenario_freeze", validation_sc5f_scenario_freeze)
    graph.add_node("validation_sd6_sim", validation_sd6_sim)
    graph.add_node("validation_sl7_model_review", validation_sl7_model_review)
    graph.add_node("validation_finalize", validation_finalize)
    graph.add_edge(START, "validation_enter")
    return graph.compile(checkpointer=False)
