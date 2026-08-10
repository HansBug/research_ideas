"""LG-M1-D3 split module for repair subgraph.

This module owns the physical implementation moved out of
``method.langgraph_runtime``.  It imports LG-C1 graph-state contracts and shared
runtime helpers from ``method.langgraph.core`` without importing the legacy
facade, preserving the academic evidence path while making the D3 architecture
readable by file name.
"""

from __future__ import annotations

from method.langgraph.core import *  # noqa: F403 - D3 compatibility split keeps shared helper names private.


def _d3_state_graph_factory() -> Any:
    """Return facade-monkeypatchable StateGraph for legacy characterization tests."""

    import sys

    facade = sys.modules.get("method.langgraph_runtime")
    if facade is not None and hasattr(facade, "StateGraph"):
        return getattr(facade, "StateGraph")
    return StateGraph

class _RepairSubgraphState(_GraphLoopState, total=False):
    """State carried by the LG-B2 repair subgraph.

    The canonical repair data remains in ``_RunState`` / AgentLoopRunRecord.
    ``repair_*`` keys are transient subgraph channels used only to make
    SD-8→SL-9→SL-10→SC-11 orchestration visible to LangGraph.
    """

    repair_validation: Any
    repair_selected_trace: dict[str, Any]
    repair_source: str
    repair_source_stage: str
    repair_selected_feedback: Any
    repair_fix_plan: Any
    repair_effective_fix_plan: Any
    repair_request_batch: Any
    repair_aggregate_stage_ids: list[str]
    repair_max_rework_attempts: int
    repair_rework_attempt: int
    repair_rework_locked_initial: bool
    repair_active_request_batch: Any
    repair_sl9_decision: Any
    repair_candidate_dsl: str
    repair_request: Any
    repair_local_review: Any
    repair_local_meta: Any
    repair_local_check_evidence: dict[str, Any]
    repair_local_sd10_repair_review: Any
    repair_review_input_summary: dict[str, Any]
    repair_sl10_output: Any
    repair_repair_review: Any
    repair_memory: dict[str, Any]
    repair_grounding_update_hints: list[dict[str, Any]]
    repair_noop_override_waiver_audit: Any
    repair_last_iteration_patch: dict[str, Any]
    repair_last_repair_review: Any
    repair_last_sl10_output: Any
    repair_accepted: bool
    repair_patch: dict[str, Any]


def _build_repair_subgraph(
    *,
    runtime_cfg: FullStagedRuntimeConfig,
    adapters: FullStagedRuntimeAdapters,
) -> Any:
    """Build the LG-B2 stage-level repair subgraph.

    LangGraph owns the repair micro-loop: SD-8 prepares a request batch, SL-9
    proposes/accepts per-request edits, SL-10 reviews or requests rework, and
    SC-11 records accepted candidate handoff.  Canonical stage semantics remain
    in ``method.staged_runtime`` helpers; this subgraph only replaces the
    previous Python-level repair-path orchestration.
    """

    graph = _d3_state_graph_factory()(_RepairSubgraphState)

    def _state(graph_state: _RepairSubgraphState) -> _RepairSubgraphState:
        return dict(graph_state)

    def _runtime_state(graph_state: _RepairSubgraphState) -> _RunState:
        return graph_state["runtime_state"]

    def _iteration(graph_state: _RepairSubgraphState) -> int:
        return int(graph_state.get("iteration", 0))

    def repair_enter(graph_state: _RepairSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        validation = graph_state.get("repair_validation")
        if not isinstance(validation, _ValidationPass):
            raise TypeError("repair subgraph requires repair_validation=_ValidationPass")
        assert validation.selected is not None
        source, selected_feedback, source_stage = validation.selected
        selected_trace = _selected_feedback_trace(source, selected_feedback, source_stage, scenario_set=validation.scenario_set)
        variable_role_summary = _diagnostic_variable_role_summary(graph_state["nl"], selected_feedback)
        if variable_role_summary:
            selected_trace["variable_role_summary"] = variable_role_summary
        if selected_trace["pre_scenario"]:
            runtime_state.pre_scenario_repair_count += 1
        _trace_node(graph_state, "repair_enter", event="subgraph_enter", iteration=iteration, source_stage=source_stage)
        _append_flow_log(
            runtime_state.logs,
            event="repair_path_enter",
            stage_id=StageId.SD_8_FIX_PLAN.value,
            iteration=iteration,
            source=source,
            source_stage=source_stage,
            selected_feedback=selected_trace,
            current_dsl_hash=_hash_text(runtime_state.current_dsl),
            current_dsl=runtime_state.current_dsl,
            jump="SD-8",
            graph_subgraph="repair_subgraph",
            graph_node="repair_enter",
        )
        graph_state["repair_validation"] = validation
        graph_state["repair_source"] = source
        graph_state["repair_source_stage"] = source_stage
        graph_state["repair_selected_feedback"] = selected_feedback
        graph_state["repair_selected_trace"] = selected_trace
        return Command(goto="repair_sd8_fix_requests", update=graph_state)

    def repair_sd8_fix_requests(graph_state: _RepairSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        validation: _ValidationPass = graph_state["repair_validation"]
        selected_feedback = graph_state["repair_selected_feedback"]
        source = str(graph_state["repair_source"])
        source_stage = str(graph_state["repair_source_stage"])
        selected_trace = dict(graph_state.get("repair_selected_trace") or {})
        _trace_node(graph_state, "repair_sd8_fix_requests", iteration=iteration, source_stage=source_stage)

        rework_locked = runtime_state.pending_repair_rejection is not None and runtime_state.pending_original_fix_plan is not None
        if rework_locked:
            fix_plan, fix_meta = _lg_e3_fixed_tool_call(
                graph_state,
                tool_name="sd8_fix_plan",
                stage_id=StageId.SD_8_FIX_PLAN.value,
                graph_node="repair_sd8_fix_requests",
                iteration=iteration,
                input_payload={
                    "selected_feedback": None,
                    "source": "repair_review",
                    "rejection": runtime_state.pending_repair_rejection,
                    "original": runtime_state.pending_original_fix_plan,
                },
                call=lambda: run_sd8_fix_plan(
                    None,
                    source="repair_review",
                    rejection=runtime_state.pending_repair_rejection,
                    original=runtime_state.pending_original_fix_plan,
                ),
            )
        else:
            fix_plan, fix_meta = _lg_e3_fixed_tool_call(
                graph_state,
                tool_name="sd8_fix_plan",
                stage_id=StageId.SD_8_FIX_PLAN.value,
                graph_node="repair_sd8_fix_requests",
                iteration=iteration,
                input_payload={
                    "selected_feedback": selected_feedback,
                    "source": source,
                    "source_stage": source_stage,
                    "grounding_map": runtime_cfg.grounding_map,
                    "before_dsl": runtime_state.current_dsl,
                },
                call=lambda: run_sd8_fix_plan(
                    selected_feedback,
                    source=source,
                    source_stage=source_stage,
                    grounding_map=runtime_cfg.grounding_map,
                    before_dsl=runtime_state.current_dsl,
                ),
            )
        _append_stage(runtime_state.stage_records, fix_meta)
        effective_fix_plan = fix_plan.original if isinstance(fix_plan, RevisedFixPlan) else fix_plan
        assert isinstance(effective_fix_plan, FixPlan)
        aggregate_stage_ids = [fix_meta.stage_id]
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SD_8_FIX_PLAN.value,
            iteration=iteration,
            ok=True,
            status=str(fix_meta.status),
            plan_kind="RevisedFixPlan" if isinstance(fix_plan, RevisedFixPlan) else "FixPlan",
            fix_plan=_compact_json(effective_fix_plan, max_list_items=10),
            jump="SL-9",
            graph_subgraph="repair_subgraph",
            graph_node="repair_sd8_fix_requests",
        )
        request_batch = _fix_request_batch_from_plan(
            iteration=iteration,
            source=source,
            source_stage=source_stage,
            selected_trace=selected_trace,
            fix_plan=fix_plan,
            effective_fix_plan=effective_fix_plan,
            scenario_set=validation.scenario_set,
        )
        _fix_log_entry(
            state=runtime_state,
            iteration=iteration,
            phase="request_batch",
            batch=request_batch,
            old_dsl=runtime_state.current_dsl,
            next_action="sl9_decision_and_repair",
            notes=["SD-8 produced FixRequestBatch; deterministic stage does not decide final repair."],
        )
        _append_flow_log(
            runtime_state.logs,
            event="fix_request_batch",
            stage_id=StageId.SD_8_FIX_PLAN.value,
            iteration=iteration,
            batch_id=request_batch.batch_id,
            request_count=len(request_batch.requests),
            hard_block=request_batch.has_hard_block,
            requests=_jsonable(request_batch.requests),
            next_action="SL-9",
            graph_subgraph="repair_subgraph",
            graph_node="repair_sd8_fix_requests",
        )
        if source == FeedbackSource.DESIGN.value and isinstance(selected_feedback, DesignFeedback):
            _lg_e3_fixed_tool_call(
                graph_state,
                tool_name="warning_repair_attempt_marker",
                stage_id="warning_budget_state",
                graph_node="repair_sd8_fix_requests",
                iteration=iteration,
                input_payload={
                    "warning_budget_state": validation.context.warning_budget_state,
                    "instance_keys": [item.instance_key for item in selected_feedback.blocking_items],
                },
                call=lambda: mark_warning_repair_attempt(
                    validation.context.warning_budget_state,
                    [item.instance_key for item in selected_feedback.blocking_items],
                ),
            )
            runtime_state.warning_budget_state = validation.context.warning_budget_state

        graph_state["repair_fix_plan"] = fix_plan
        graph_state["repair_effective_fix_plan"] = effective_fix_plan
        graph_state["repair_request_batch"] = request_batch
        graph_state["repair_aggregate_stage_ids"] = aggregate_stage_ids
        graph_state["repair_rework_locked_initial"] = rework_locked
        graph_state["repair_max_rework_attempts"] = max(1 + runtime_cfg.min_sl10_rework_attempts, runtime_cfg.max_iterations - iteration)
        graph_state["repair_rework_attempt"] = 0
        graph_state["repair_last_iteration_patch"] = {}
        graph_state["repair_last_repair_review"] = None
        graph_state["repair_last_sl10_output"] = None
        return Command(goto="repair_sl9_repair", update=graph_state)

    def repair_sl9_repair(graph_state: _RepairSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        validation: _ValidationPass = graph_state["repair_validation"]
        selected_feedback = graph_state["repair_selected_feedback"]
        selected_trace = dict(graph_state.get("repair_selected_trace") or {})
        fix_plan = graph_state["repair_fix_plan"]
        request_batch = graph_state["repair_request_batch"]
        aggregate_stage_ids = list(graph_state.get("repair_aggregate_stage_ids") or [])
        rework_attempt = int(graph_state.get("repair_rework_attempt", 0))
        attempt_rework_locked = bool(graph_state.get("repair_rework_locked_initial")) or rework_attempt > 0
        repair_memory_for_attempt = _repair_memory_for_prompt(runtime_state.fix_log)
        active_request_batch = _fix_request_batch_with_repair_memory(
            request_batch,
            repair_memory=repair_memory_for_attempt,
            rework_locked=attempt_rework_locked,
        )
        _trace_node(
            graph_state,
            "repair_sl9_repair",
            iteration=iteration,
            rework_attempt=rework_attempt,
            rework_locked=attempt_rework_locked,
            batch_id=active_request_batch.batch_id,
        )
        _append_flow_log(
            runtime_state.logs,
            event="stage_enter",
            stage_id=StageId.SL_9_REPAIR.value,
            iteration=iteration,
            reason="fix_requests_ready" if not attempt_rework_locked else "sl10_rework_locked",
            rework_attempt=rework_attempt,
            rework_locked=attempt_rework_locked,
            batch_id=active_request_batch.batch_id,
            request_ids=[request.request_id for request in active_request_batch.requests],
            repair_memory=_compact_json(repair_memory_for_attempt, max_list_items=8),
            old_dsl=runtime_state.current_dsl,
            graph_subgraph="repair_subgraph",
            graph_node="repair_sl9_repair",
        )
        request = RepairRequest(
            nl=graph_state["nl"],
            grounding_map=runtime_cfg.grounding_map,
            old_dsl=runtime_state.current_dsl,
            fix_plan=fix_plan,
            selected_feedback=selected_feedback,
            selected_feedback_trace=selected_trace,
            scenario_set=validation.scenario_set,
            iteration=iteration,
            repair_attempt=len(runtime_state.repair_history),
            fix_request_batch=active_request_batch,
            fix_log=[
                *list(runtime_state.fix_log),
                {
                    "entry_id": f"runtime-current-repair-memory-{rework_attempt}",
                    "iteration": iteration,
                    "phase": "current_sl9_repair_memory",
                    "repair_memory": repair_memory_for_attempt,
                    "next_action": "sl9_must_address_repair_memory",
                },
            ],
            rework_locked=attempt_rework_locked,
        )
        request.repair_memory = repair_memory_for_attempt
        repair_run = _lg_d2_wrap_llm_stage_node(
            graph_state,
            stage_id=StageId.SL_9_REPAIR,
            graph_node="repair_sl9_repair",
            subgraph_id="repair_subgraph",
            call=lambda: _append_llm_stage_run(
                run=adapters.repair(request),
                expected_stage_id=StageId.SL_9_REPAIR,
                stage_records=runtime_state.stage_records,
                iteration_stage_metas=None,
                llm_interactions=runtime_state.llm_interactions,
                logs=runtime_state.logs,
                iteration=iteration,
            ),
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
            repair_meta = _sl9_meta(runtime_state.current_dsl, fix_plan, candidate_dsl)
            _append_stage(runtime_state.stage_records, repair_meta)
            aggregate_stage_ids.append(repair_meta.stage_id)
            runtime_state.llm_interactions.append(
                {
                    "stage_id": StageId.SL_9_REPAIR.value,
                    "provider": runtime_cfg.adapter_mode,
                    "model_id": "explicit-adapter",
                    "real_llm_provider_api": False,
                    "prompt_template_version": "pr-b1-repair-adapter.v2-fixrequest",
                    "input_hash": _hash_text(runtime_state.current_dsl),
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
            batch=active_request_batch,
            candidate_dsl=candidate_dsl,
            rework_locked=attempt_rework_locked,
        )
        sl9_decision.diff_summary = sl9_decision.diff_summary or _dsl_diff_summary(runtime_state.current_dsl, candidate_dsl)
        request.sl9_decision = sl9_decision
        request.diff_summary = dict(sl9_decision.diff_summary)
        request.fix_log = list(runtime_state.fix_log)
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SL_9_REPAIR.value,
            iteration=iteration,
            ok=bool(sl9_decision.accepted_request_ids),
            rework_attempt=rework_attempt,
            accepted_request_ids=sl9_decision.accepted_request_ids,
            rejected_request_ids=sl9_decision.rejected_request_ids,
            decisions=_jsonable(sl9_decision.decisions),
            diff_summary=sl9_decision.diff_summary,
            jump="SL-10" if sl9_decision.accepted_request_ids else "waiver_continue_or_exit",
            candidate_dsl=candidate_dsl,
            graph_subgraph="repair_subgraph",
            graph_node="repair_sl9_repair",
        )
        _fix_log_entry(
            state=runtime_state,
            iteration=iteration,
            phase="sl9_decision" if rework_attempt == 0 else "sl9_rework_decision",
            batch=active_request_batch,
            decisions=sl9_decision.decisions,
            old_dsl=runtime_state.current_dsl,
            candidate_dsl=candidate_dsl,
            diff_summary=sl9_decision.diff_summary,
            next_action="sl10_review" if sl9_decision.accepted_request_ids else "reject_or_waiver",
            notes=[*sl9_decision.repair_rationale, *( ["rework_locked=true"] if attempt_rework_locked else [] )],
        )
        graph_state["repair_active_request_batch"] = active_request_batch
        graph_state["repair_sl9_decision"] = sl9_decision
        graph_state["repair_candidate_dsl"] = candidate_dsl
        graph_state["repair_request"] = request
        graph_state["repair_aggregate_stage_ids"] = aggregate_stage_ids
        if sl9_decision.accepted_request_ids:
            return Command(goto="repair_sl10_review", update=graph_state)

        hard_rejected = any(req.hard_block for req in active_request_batch.requests)
        stale_waiver_audit = (
            _stale_overridden_scenario_waiver_audit(
                active_request_batch=active_request_batch,
                sl9_decision=sl9_decision,
                fix_log=runtime_state.fix_log,
                current_dsl_hash=_hash_text(runtime_state.current_dsl),
                scenario_set=validation.scenario_set,
            )
            if hard_rejected
            else None
        )
        standard_waiver_continue = (
            not hard_rejected
            and bool(active_request_batch.requests)
            and all(req.waiver_allowed for req in active_request_batch.requests)
            and all(decision.decision == "reject" for decision in sl9_decision.decisions)
        )
        waiver_continue = standard_waiver_continue or stale_waiver_audit is not None
        waiver_reason = (
            ":stale_overridden_scenario_waiver"
            if stale_waiver_audit is not None
            else ":waiver_continue"
            if standard_waiver_continue
            else ":hard_block"
            if hard_rejected
            else ":waiver_only"
        )
        rejection = RepairRejection(
            rejected_by_stage=StageId.SL_9_REPAIR.value,
            reason="sl9_rejected_all_fix_requests" + waiver_reason,
            target_resolved=waiver_continue,
            regression_detected=False,
            drift_risk="minor" if stale_waiver_audit is not None else "major" if hard_rejected else "minor",
            evidence=[
                *_jsonable(sl9_decision.decisions),
                *([_jsonable(stale_waiver_audit)] if stale_waiver_audit is not None else []),
            ],
        )
        repair_review = RepairReviewFeedback(
            ok=waiver_continue,
            target_resolved=waiver_continue,
            drift_risk=rejection.drift_risk,
            local_rejection=None if waiver_continue else rejection,
        )
        if waiver_continue:
            _append_flow_log(
                runtime_state.logs,
                event=(
                    "sl9_all_rejected_stale_scenario_waiver_continue"
                    if stale_waiver_audit is not None
                    else "sl9_all_rejected_waiver_continue"
                ),
                level="info",
                stage_id=StageId.SL_9_REPAIR.value,
                iteration=iteration,
                source_stage=str(graph_state.get("repair_source_stage") or ""),
                batch_id=active_request_batch.batch_id,
                note="no candidate DSL; downstream validation continues without SC-11 acceptance",
                waiver_audit=_jsonable(stale_waiver_audit) if stale_waiver_audit is not None else None,
                jump="continue_after_current_stage",
                graph_subgraph="repair_subgraph",
                graph_node="repair_sl9_repair",
            )
        _fix_log_entry(
            state=runtime_state,
            iteration=iteration,
            phase="sl9_all_rejected",
            batch=active_request_batch,
            decisions=sl9_decision.decisions,
            old_dsl=runtime_state.current_dsl,
            candidate_dsl=candidate_dsl,
            diff_summary=sl9_decision.diff_summary,
            next_action="continue_after_waiver" if waiver_continue else "exit_rejected",
            notes=[
                rejection.reason,
                *(
                    [f"waiver_audit:{stale_waiver_audit['kind']}:{_short_hash(stale_waiver_audit)}"]
                    if stale_waiver_audit is not None
                    else []
                ),
            ],
        )
        effective_fix_plan = graph_state["repair_effective_fix_plan"]
        repair_payload = {
            "iteration": iteration,
            "selected_feedback": selected_trace,
            "plan_kind": active_request_batch.legacy_plan_kind,
            "fix_plan": _jsonable(effective_fix_plan),
            "fix_request_batch": _jsonable(active_request_batch),
            "sl9_decision": _jsonable(sl9_decision),
            "candidate_dsl": candidate_dsl,
            "candidate_dsl_hash": _hash_text(candidate_dsl),
            "repair_review": _jsonable(repair_review),
            "accepted": False,
            "waiver_continue": waiver_continue,
            "waiver_audit": _jsonable(stale_waiver_audit) if stale_waiver_audit is not None else None,
            "repair_stage_ids": list(aggregate_stage_ids),
            "scenario_set_id": validation.scenario_set.scenario_set_id if validation.scenario_set is not None else None,
            "fix_log_entry_count": len(runtime_state.fix_log),
        }
        runtime_state.repair_history.append(repair_payload)
        graph_state["repair_accepted"] = False
        graph_state["repair_patch"] = {
            "selected_feedback": selected_trace,
            "repair_stage_ids": list(aggregate_stage_ids),
            "fix_request_batch": _jsonable(active_request_batch),
            "sl9_decision": _jsonable(sl9_decision),
            "repair_review": _jsonable(repair_review),
            "accepted_candidate": False,
            "waiver_continue": waiver_continue,
            "waiver_audit": _jsonable(stale_waiver_audit) if stale_waiver_audit is not None else None,
            "exit_reason": "all_fix_requests_rejected_as_waiver_continue" if waiver_continue else rejection.reason,
            "retryable_repair_rejection": False,
        }
        return Command(goto="repair_finalize", update=graph_state)

    def repair_sl10_review(graph_state: _RepairSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        validation: _ValidationPass = graph_state["repair_validation"]
        selected_feedback = graph_state["repair_selected_feedback"]
        selected_trace = dict(graph_state.get("repair_selected_trace") or {})
        effective_fix_plan = graph_state["repair_effective_fix_plan"]
        active_request_batch = graph_state["repair_active_request_batch"]
        sl9_decision = graph_state["repair_sl9_decision"]
        candidate_dsl = str(graph_state.get("repair_candidate_dsl") or "")
        aggregate_stage_ids = list(graph_state.get("repair_aggregate_stage_ids") or [])
        rework_attempt = int(graph_state.get("repair_rework_attempt", 0))
        attempt_rework_locked = bool(graph_state.get("repair_rework_locked_initial")) or rework_attempt > 0
        max_rework_attempts = int(graph_state.get("repair_max_rework_attempts", 1))
        _trace_node(
            graph_state,
            "repair_sl10_review",
            iteration=iteration,
            rework_attempt=rework_attempt,
            batch_id=active_request_batch.batch_id,
        )
        review_request = RepairRequest(
            nl=graph_state["nl"],
            grounding_map=runtime_cfg.grounding_map,
            old_dsl=runtime_state.current_dsl,
            fix_plan=effective_fix_plan,
            selected_feedback=selected_feedback,
            selected_feedback_trace=selected_trace,
            scenario_set=validation.scenario_set,
            candidate_dsl=candidate_dsl,
            iteration=iteration,
            repair_attempt=len(runtime_state.repair_history),
            warning_budget_state=validation.context.warning_budget_state,
            fix_request_batch=active_request_batch,
            fix_log=list(runtime_state.fix_log),
            sl9_decision=sl9_decision,
            diff_summary=sl9_decision.diff_summary,
            rework_locked=attempt_rework_locked,
        )
        local_review, local_meta = _lg_e3_fixed_tool_call(
            graph_state,
            tool_name="sd10_repair_review_local_check",
            stage_id=StageId.SD_10_REPAIR_REVIEW.value,
            graph_node="repair_sl10_review",
            iteration=iteration,
            input_payload={"repair_request": review_request},
            call=lambda: adapters.repair_review(review_request),
        )
        local_check_evidence = _local_repair_check_evidence(
            repair_review=local_review,
            repair_review_meta=local_meta,
            scenario_set=validation.scenario_set,
        )
        review_request.local_check_evidence = local_check_evidence
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SD_10_REPAIR_REVIEW.value,
            iteration=iteration,
            ok=local_review.ok,
            status=str(local_meta.status),
            local_check_evidence=local_check_evidence,
            jump="SL-10",
            graph_subgraph="repair_subgraph",
            graph_node="repair_sl10_review",
        )
        local_sd10_repair_review = _jsonable(local_review)
        repair_review_input_summary = {
            "nl_hash": _hash_text(graph_state["nl"]),
            "has_nl_input": bool(graph_state["nl"]),
            "has_grounding_map": runtime_cfg.grounding_map is not None,
            "old_dsl_hash": _hash_text(runtime_state.current_dsl),
            "candidate_dsl_hash": _hash_text(candidate_dsl),
            "fix_plan_target": getattr(effective_fix_plan, "target", None),
            "fix_plan_source_stage": getattr(effective_fix_plan, "source_stage", None),
            "fix_request_batch_id": active_request_batch.batch_id,
            "scenario_set_id": validation.scenario_set.scenario_set_id if validation.scenario_set is not None else None,
            "inputs": ["NL", "GroundingMap", "old_dsl", "candidate_dsl", "FixRequestBatch", "SL9Decisions", "FixLog", "LocalCheckEvidence", "ScenarioSet"],
            "local_check_stage_id": StageId.SD_10_REPAIR_REVIEW.value,
            "active_review_stage_id": StageId.SL_10_REPAIR_REVIEW.value,
            "rework_attempt": rework_attempt,
            "rework_locked": attempt_rework_locked,
        }
        if adapters.sl10_review is not None:
            _append_flow_log(
                runtime_state.logs,
                event="stage_enter",
                stage_id=StageId.SL_10_REPAIR_REVIEW.value,
                iteration=iteration,
                reason="candidate_dsl_and_local_evidence_ready",
                rework_attempt=rework_attempt,
                batch_id=active_request_batch.batch_id,
                inputs=repair_review_input_summary["inputs"],
                old_dsl_hash=_hash_text(runtime_state.current_dsl),
                candidate_dsl_hash=_hash_text(candidate_dsl),
                graph_subgraph="repair_subgraph",
                graph_node="repair_sl10_review",
            )
            sl10_run = _lg_d2_wrap_llm_stage_node(
                graph_state,
                stage_id=StageId.SL_10_REPAIR_REVIEW,
                graph_node="repair_sl10_review",
                subgraph_id="repair_subgraph",
                call=lambda: _append_llm_stage_run(
                    run=adapters.sl10_review(review_request, local_review),
                    expected_stage_id=StageId.SL_10_REPAIR_REVIEW,
                    stage_records=runtime_state.stage_records,
                    iteration_stage_metas=None,
                    llm_interactions=runtime_state.llm_interactions,
                    logs=runtime_state.logs,
                    iteration=iteration,
                ),
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
                        local_override_rationale=[str(item) for item in parsed.get("local_override_rationale", [])],
                        local_check_evidence=local_check_evidence,
                        review_meta=None,
                        meta=getattr(sl10_run, "stage_meta"),
                    )
                sl10_output.local_check_evidence = sl10_output.local_check_evidence or local_check_evidence
                aggregate_stage_ids.append(getattr(sl10_run, "stage_meta").stage_id)
            else:
                sl10_output, sl10_meta = sl10_run
                _append_stage(runtime_state.stage_records, sl10_meta)
                aggregate_stage_ids.append(sl10_meta.stage_id)
        else:
            sl10_output = _default_sl10_output_from_local_checks(local_review=local_review, local_evidence=local_check_evidence)
            assert sl10_output.meta is not None
            _append_stage(runtime_state.stage_records, sl10_output.meta)
            aggregate_stage_ids.append(sl10_output.meta.stage_id)
        repair_review = _repair_review_from_sl10(
            sl10_output,
            local_review=local_review,
            candidate_dsl_hash=_hash_text(candidate_dsl),
            local_check_evidence_hash=_short_hash(local_check_evidence),
        )
        accepted = bool(sl10_output.ok)
        previous_candidate_hashes = [
            str(entry.get("candidate_dsl_hash") or "")
            for entry in runtime_state.fix_log
            if entry.get("candidate_dsl_hash")
            and str(entry.get("phase") or "") in {"sl10_review", "sl10_rework_review"}
        ]
        repair_memory = _repair_memory_for_log(
            sl10_output=sl10_output,
            local_check_evidence=local_check_evidence,
            candidate_dsl=candidate_dsl,
            previous_candidate_hashes=previous_candidate_hashes,
        )
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SL_10_REPAIR_REVIEW.value,
            iteration=iteration,
            ok=accepted,
            rework_attempt=rework_attempt,
            decision=sl10_output.decision,
            target_resolved=sl10_output.target_resolved,
            regression_detected=sl10_output.regression_detected,
            drift_risk=sl10_output.drift_risk,
            rework_instructions=sl10_output.rework_instructions,
            repair_memory=_compact_json(repair_memory, max_list_items=8),
            evidence=_compact_json(sl10_output.evidence, max_list_items=8),
            local_override_rationale=sl10_output.local_override_rationale,
            jump="SC-11" if accepted else ("SL-9 rework" if rework_attempt + 1 < max_rework_attempts else "SC-12 rejected"),
            graph_subgraph="repair_subgraph",
            graph_node="repair_sl10_review",
        )
        sl10_grounding_hints = _extract_grounding_update_hints(
            source_stage_id=StageId.SL_10_REPAIR_REVIEW.value,
            payload=sl10_output,
        )
        sl10_grounding_hints = _apply_grounding_update_hints(
            cfg=runtime_cfg,
            state=runtime_state,
            hints=sl10_grounding_hints,
            iteration=iteration,
            source_stage_id=StageId.SL_10_REPAIR_REVIEW.value,
        )
        noop_override_waiver_audit = (
            _sl10_noop_override_waiver_audit(
                active_request_batch=active_request_batch,
                sl9_decision=sl9_decision,
                local_review=local_review,
                local_check_evidence=local_check_evidence,
                sl10_output=sl10_output,
                old_dsl=runtime_state.current_dsl,
                candidate_dsl=candidate_dsl,
                scenario_set=validation.scenario_set,
            )
            if accepted
            else None
        )
        graph_state["repair_aggregate_stage_ids"] = aggregate_stage_ids
        graph_state["repair_local_check_evidence"] = local_check_evidence
        graph_state["repair_local_sd10_repair_review"] = local_sd10_repair_review
        graph_state["repair_review_input_summary"] = repair_review_input_summary
        graph_state["repair_sl10_output"] = sl10_output
        graph_state["repair_repair_review"] = repair_review
        graph_state["repair_memory"] = repair_memory
        graph_state["repair_grounding_update_hints"] = sl10_grounding_hints
        graph_state["repair_noop_override_waiver_audit"] = noop_override_waiver_audit
        if noop_override_waiver_audit is not None:
            _append_flow_log(
                runtime_state.logs,
                event="sl10_noop_override_waiver_continue",
                level="info",
                stage_id=StageId.SL_10_REPAIR_REVIEW.value,
                iteration=iteration,
                source_stage=str(graph_state.get("repair_source_stage") or ""),
                batch_id=active_request_batch.batch_id,
                note="SL-10 accepted a no-op local override; downstream validation continues without SC-11 budget consumption",
                waiver_audit=_jsonable(noop_override_waiver_audit),
                jump="continue_after_current_stage",
                graph_subgraph="repair_subgraph",
                graph_node="repair_sl10_review",
            )
            repair_review = RepairReviewFeedback(ok=True, target_resolved=True, regression_detected=False, drift_risk="minor")
            _fix_log_entry(
                state=runtime_state,
                iteration=iteration,
                phase="sl10_noop_override_waiver",
                batch=active_request_batch,
                decisions=sl9_decision.decisions,
                old_dsl=runtime_state.current_dsl,
                candidate_dsl=candidate_dsl,
                diff_summary=sl9_decision.diff_summary,
                local_check_evidence=local_check_evidence,
                sl10_review=sl10_output,
                repair_memory=repair_memory,
                next_action="continue_after_waiver",
                notes=[
                    f"waiver_audit:{noop_override_waiver_audit['kind']}:{_short_hash(noop_override_waiver_audit)}",
                    *sl10_output.local_override_rationale,
                    *(f"grounding_update_hint:{item['hint_hash']}" for item in sl10_grounding_hints),
                ],
            )
            repair_payload = {
                "iteration": iteration,
                "selected_feedback": selected_trace,
                "plan_kind": active_request_batch.legacy_plan_kind,
                "fix_plan": _jsonable(effective_fix_plan),
                "fix_request_batch": _jsonable(active_request_batch),
                "sl9_decision": _jsonable(sl9_decision),
                "candidate_dsl": candidate_dsl,
                "candidate_dsl_hash": _hash_text(candidate_dsl),
                "repair_review_input_summary": repair_review_input_summary,
                "local_check_evidence": _jsonable(local_check_evidence),
                "sd10_repair_review": local_sd10_repair_review,
                "sl10_repair_review": _jsonable(sl10_output),
                "grounding_update_hints": _jsonable(sl10_grounding_hints),
                "repair_review": _jsonable(repair_review),
                "accepted": False,
                "accepted_noop_override": True,
                "waiver_continue": True,
                "waiver_audit": _jsonable(noop_override_waiver_audit),
                "repair_stage_ids": list(aggregate_stage_ids),
                "scenario_set_id": validation.scenario_set.scenario_set_id if validation.scenario_set is not None else None,
                "fix_log_entry_count": len(runtime_state.fix_log),
                "rework_attempt": rework_attempt,
            }
            runtime_state.repair_history.append(repair_payload)
            graph_state["repair_accepted"] = False
            graph_state["repair_patch"] = {
                "selected_feedback": selected_trace,
                "repair_stage_ids": list(aggregate_stage_ids),
                "fix_request_batch": _jsonable(active_request_batch),
                "sl9_decision": _jsonable(sl9_decision),
                "local_check_evidence": _jsonable(local_check_evidence),
                "sl10_repair_review": _jsonable(sl10_output),
                "grounding_update_hints": _jsonable(sl10_grounding_hints),
                "repair_review": _jsonable(repair_review),
                "accepted_candidate": False,
                "accepted_noop_override": True,
                "waiver_continue": True,
                "waiver_audit": _jsonable(noop_override_waiver_audit),
                "fix_log_entry_count": len(runtime_state.fix_log),
                "rework_attempts_used": rework_attempt + 1,
                "exit_reason": "sl10_noop_override_waiver_continue",
                "retryable_repair_rejection": False,
            }
            return Command(goto="repair_finalize", update=graph_state)
        if accepted:
            return Command(goto="repair_sc11_accept_candidate", update=graph_state)
        _fix_log_entry(
            state=runtime_state,
            iteration=iteration,
            phase="sl10_review" if rework_attempt == 0 else "sl10_rework_review",
            batch=active_request_batch,
            decisions=sl9_decision.decisions,
            old_dsl=runtime_state.current_dsl,
            candidate_dsl=candidate_dsl,
            diff_summary=sl9_decision.diff_summary,
            local_check_evidence=local_check_evidence,
            sl10_review=sl10_output,
            repair_memory=repair_memory,
            next_action="sl9_rework" if rework_attempt + 1 < max_rework_attempts else "exit_rejected_rework_budget_exhausted",
            notes=[
                *sl10_output.rework_instructions,
                *(
                    f"repair_memory:{item.get('kind') or item}" if isinstance(item, dict) else f"repair_memory:{item}"
                    for item in repair_memory.get("actionable_rework_guidance", [])
                    if item
                ),
                *(f"grounding_update_hint:{item['hint_hash']}" for item in sl10_grounding_hints),
            ],
        )
        repair_payload = {
            "iteration": iteration,
            "selected_feedback": selected_trace,
            "plan_kind": active_request_batch.legacy_plan_kind,
            "fix_plan": _jsonable(effective_fix_plan),
            "fix_request_batch": _jsonable(active_request_batch),
            "sl9_decision": _jsonable(sl9_decision),
            "candidate_dsl": candidate_dsl,
            "candidate_dsl_hash": _hash_text(candidate_dsl),
            "repair_review_input_summary": repair_review_input_summary,
            "local_check_evidence": _jsonable(local_check_evidence),
            "sd10_repair_review": local_sd10_repair_review,
            "sl10_repair_review": _jsonable(sl10_output),
            "grounding_update_hints": _jsonable(sl10_grounding_hints),
            "repair_review": _jsonable(repair_review),
            "accepted": False,
            "repair_stage_ids": list(aggregate_stage_ids),
            "scenario_set_id": validation.scenario_set.scenario_set_id if validation.scenario_set is not None else None,
            "fix_log_entry_count": len(runtime_state.fix_log),
            "rework_attempt": rework_attempt,
        }
        runtime_state.repair_history.append(repair_payload)
        graph_state["repair_last_repair_review"] = repair_review
        graph_state["repair_last_sl10_output"] = sl10_output
        graph_state["repair_last_iteration_patch"] = {
            "selected_feedback": selected_trace,
            "repair_stage_ids": list(aggregate_stage_ids),
            "fix_request_batch": _jsonable(active_request_batch),
            "sl9_decision": _jsonable(sl9_decision),
            "local_check_evidence": _jsonable(local_check_evidence),
            "sl10_repair_review": _jsonable(sl10_output),
            "grounding_update_hints": _jsonable(sl10_grounding_hints),
            "repair_review": _jsonable(repair_review),
            "accepted_candidate": False,
            "fix_log_entry_count": len(runtime_state.fix_log),
            "rework_attempts_used": rework_attempt + 1,
        }
        runtime_state.pending_repair_rejection = None
        runtime_state.pending_original_fix_plan = None
        runtime_state.pending_rework_request = _jsonable(sl10_output)
        if rework_attempt + 1 < max_rework_attempts:
            graph_state["repair_rework_attempt"] = rework_attempt + 1
            return Command(goto="repair_sl9_repair", update=graph_state)
        last_patch = dict(graph_state.get("repair_last_iteration_patch") or {})
        last_patch["exit_reason"] = repair_review.local_rejection.reason if repair_review.local_rejection is not None else "sl10 repair review requested rework"
        last_patch["retryable_repair_rejection"] = False
        last_patch["next_iteration_repair_plan"] = "<none:sl10_rework_budget_exhausted>"
        graph_state["repair_accepted"] = False
        graph_state["repair_patch"] = last_patch
        return Command(goto="repair_finalize", update=graph_state)

    def repair_sc11_accept_candidate(graph_state: _RepairSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        validation: _ValidationPass = graph_state["repair_validation"]
        selected_trace = dict(graph_state.get("repair_selected_trace") or {})
        effective_fix_plan = graph_state["repair_effective_fix_plan"]
        active_request_batch = graph_state["repair_active_request_batch"]
        sl9_decision = graph_state["repair_sl9_decision"]
        candidate_dsl = str(graph_state.get("repair_candidate_dsl") or "")
        aggregate_stage_ids = list(graph_state.get("repair_aggregate_stage_ids") or [])
        rework_attempt = int(graph_state.get("repair_rework_attempt", 0))
        local_check_evidence = dict(graph_state.get("repair_local_check_evidence") or {})
        local_sd10_repair_review = graph_state.get("repair_local_sd10_repair_review")
        repair_review_input_summary = dict(graph_state.get("repair_review_input_summary") or {})
        sl10_output = graph_state["repair_sl10_output"]
        repair_review = graph_state["repair_repair_review"]
        repair_memory = dict(graph_state.get("repair_memory") or {})
        sl10_grounding_hints = list(graph_state.get("repair_grounding_update_hints") or [])
        _trace_node(
            graph_state,
            "repair_sc11_accept_candidate",
            iteration=iteration,
            rework_attempt=rework_attempt,
            candidate_dsl_hash=_hash_text(candidate_dsl),
        )
        sc11_meta = _meta(StageId.SC_11_ACCEPT_CANDIDATE, ok=True)
        _append_stage(runtime_state.stage_records, sc11_meta)
        aggregate_stage_ids.append(sc11_meta.stage_id)
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SC_11_ACCEPT_CANDIDATE.value,
            iteration=iteration,
            ok=True,
            reason="SL-10 accepted candidate; next iteration must restart at SD-2",
            old_dsl_hash=_hash_text(runtime_state.current_dsl),
            candidate_dsl_hash=_hash_text(candidate_dsl),
            jump="SD-2 next iteration",
            candidate_dsl=candidate_dsl,
            graph_subgraph="repair_subgraph",
            graph_node="repair_sc11_accept_candidate",
        )
        _fix_log_entry(
            state=runtime_state,
            iteration=iteration,
            phase="sl10_review" if rework_attempt == 0 else "sl10_rework_review",
            batch=active_request_batch,
            decisions=sl9_decision.decisions,
            old_dsl=runtime_state.current_dsl,
            candidate_dsl=candidate_dsl,
            diff_summary=sl9_decision.diff_summary,
            local_check_evidence=local_check_evidence,
            sl10_review=sl10_output,
            repair_memory=repair_memory,
            next_action="sc11_accept_then_sd2",
            notes=[
                *sl10_output.rework_instructions,
                *(
                    f"repair_memory:{item.get('kind') or item}" if isinstance(item, dict) else f"repair_memory:{item}"
                    for item in repair_memory.get("actionable_rework_guidance", [])
                    if item
                ),
                *(f"grounding_update_hint:{item['hint_hash']}" for item in sl10_grounding_hints),
            ],
        )
        repair_payload = {
            "iteration": iteration,
            "selected_feedback": selected_trace,
            "plan_kind": active_request_batch.legacy_plan_kind,
            "fix_plan": _jsonable(effective_fix_plan),
            "fix_request_batch": _jsonable(active_request_batch),
            "sl9_decision": _jsonable(sl9_decision),
            "candidate_dsl": candidate_dsl,
            "candidate_dsl_hash": _hash_text(candidate_dsl),
            "repair_review_input_summary": repair_review_input_summary,
            "local_check_evidence": _jsonable(local_check_evidence),
            "sd10_repair_review": local_sd10_repair_review,
            "sl10_repair_review": _jsonable(sl10_output),
            "grounding_update_hints": _jsonable(sl10_grounding_hints),
            "repair_review": _jsonable(repair_review),
            "accepted": True,
            "repair_stage_ids": list(aggregate_stage_ids),
            "scenario_set_id": validation.scenario_set.scenario_set_id if validation.scenario_set is not None else None,
            "fix_log_entry_count": len(runtime_state.fix_log),
            "rework_attempt": rework_attempt,
        }
        runtime_state.repair_history.append(repair_payload)
        runtime_state.current_dsl = candidate_dsl
        runtime_state.pending_repair_rejection = None
        runtime_state.pending_original_fix_plan = None
        runtime_state.pending_rework_request = None
        graph_state["repair_aggregate_stage_ids"] = aggregate_stage_ids
        graph_state["repair_accepted"] = True
        graph_state["repair_patch"] = {
            "selected_feedback": selected_trace,
            "repair_stage_ids": list(aggregate_stage_ids),
            "fix_request_batch": _jsonable(active_request_batch),
            "sl9_decision": _jsonable(sl9_decision),
            "local_check_evidence": _jsonable(local_check_evidence),
            "sl10_repair_review": _jsonable(sl10_output),
            "grounding_update_hints": _jsonable(sl10_grounding_hints),
            "repair_review": _jsonable(repair_review),
            "accepted_candidate": True,
            "fix_log_entry_count": len(runtime_state.fix_log),
            "rework_attempts_used": rework_attempt + 1,
            "exit_reason": "candidate_accepted_for_next_full_pass",
        }
        return Command(goto="repair_finalize", update=graph_state)

    def repair_finalize(graph_state: _RepairSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        _trace_node(
            graph_state,
            "repair_finalize",
            event="subgraph_exit",
            iteration=iteration,
            accepted=bool(graph_state.get("repair_accepted")),
            repair_stage_ids=list(graph_state.get("repair_patch", {}).get("repair_stage_ids", [])) if isinstance(graph_state.get("repair_patch"), dict) else [],
        )
        if "repair_patch" not in graph_state:
            raise RuntimeError(
                "repair subgraph contract violation: repair_finalize requires an explicit repair_patch; "
                "each SD-8/SL-9/SL-10/SC-11 exit branch must record accept/reject/waiver evidence before finalizing"
            )
        return Command(goto=END, update=graph_state)

    graph.add_node("repair_enter", repair_enter)
    graph.add_node("repair_sd8_fix_requests", repair_sd8_fix_requests)
    graph.add_node("repair_sl9_repair", repair_sl9_repair)
    graph.add_node("repair_sl10_review", repair_sl10_review)
    graph.add_node("repair_sc11_accept_candidate", repair_sc11_accept_candidate)
    graph.add_node("repair_finalize", repair_finalize)
    graph.add_edge(START, "repair_enter")
    # The parent graph already owns the run-level checkpoint.  The repair
    # subgraph intentionally carries live _RunState / feedback / adapter
    # objects so that SD-8/SL-9/SL-10/SC-11 can update the canonical evidence
    # ledger in place.  Giving this nested graph its own pickle-backed
    # checkpointer would try to serialize pyfcstm/runtime objects on every
    # waiver/rework boundary and can fail with weakref objects in real runs.
    # Stage-level visibility is preserved through explicit _trace_node events,
    # flow logs, fix_log, repair_history and the parent graph checkpoint.
    return graph.compile(checkpointer=False)
