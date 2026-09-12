"""LG-M1-D3 split module for waiver continuation subgraph.

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

from archive.agent_loop_method.langgraph.subgraphs.validation import _ValidationSubgraphState

class _WaiverSubgraphState(_ValidationSubgraphState, total=False):
    """State carried by the LG-B3 waiver continuation subgraph.

    LG-B3 keeps the canonical post-waiver evidence in ``_RunState`` and
    ``AgentLoopRunRecord``.  ``waiver_*`` keys are transient orchestration
    channels used to make the repair→waiver envelope and validation-tail
    continuation explicit without duplicating LG-B1 validation semantics.
    """

    waiver_input_envelope: dict[str, Any]
    waiver_validation_ref: str
    waiver_validation_source: Any
    waiver_tail_kind: str
    waiver_tail_start_stage: str
    waiver_result: Any


def _waiver_kind_from_patch(repair_patch: dict[str, Any]) -> str:
    waiver_audit = repair_patch.get("waiver_audit")
    if isinstance(waiver_audit, dict) and waiver_audit.get("kind"):
        kind = str(waiver_audit.get("kind"))
        if kind not in {"stale_overridden_scenario_waiver", "sl10_noop_override_waiver"}:
            raise ValueError(f"waiver entry envelope received unsupported waiver_audit.kind={kind!r}")
        return kind
    selected_trace = repair_patch.get("selected_feedback")
    if isinstance(selected_trace, dict) and selected_trace.get("source_stage") == StageId.SD_6_SIM.value:
        raise ValueError("waiver entry envelope requires SD-6 waiver_audit.kind; refusing unhandled sim waiver fallback")
    return "design_warning_waiver"


def _waiver_tail_start_stage(waiver_kind: str) -> str:
    return (
        StageId.SD_6_SIM.value
        if waiver_kind in {"stale_overridden_scenario_waiver", "sl10_noop_override_waiver"}
        else StageId.SD_4_DESIGN.value
    )


def _validate_waiver_kind_selected_consistency(*, kind: str, validation: "_ValidationPass") -> None:
    selected = validation.selected
    if selected is None:
        raise ValueError(f"waiver entry envelope requires validation.selected for tail_kind={kind!r}")
    source, feedback, source_stage = selected
    sd6_waiver_kinds = {"stale_overridden_scenario_waiver", "sl10_noop_override_waiver"}
    if kind in sd6_waiver_kinds:
        if source != FeedbackSource.SIM.value or source_stage != StageId.SD_6_SIM.value or not isinstance(feedback, SimFeedback):
            raise ValueError(
                "waiver entry envelope requires waiver_audit.kind="
                f"{kind!r} to match canonical SD-6 sim validation.selected"
            )
        return
    if kind == "design_warning_waiver":
        if source != FeedbackSource.DESIGN.value or source_stage != StageId.SD_4_DESIGN.value or not isinstance(feedback, DesignFeedback):
            raise ValueError(
                "waiver entry envelope requires design_warning_waiver to match canonical SD-4 design validation.selected"
            )
        return
    raise ValueError(f"waiver entry envelope received unsupported tail_kind={kind!r}")


def _validate_waiver_repair_patch_contract(*, repair_patch: dict[str, Any], validation: "_ValidationPass") -> dict[str, Any] | None:
    forbidden_keys = {
        "scenario_epoch",
        "oracle_weak",
        "iteration",
        "graph_state_iteration",
        "validation_ref",
        "validation_source",
        "validation_source_stage_ids",
        "validation_scenario_epoch",
        "validation_oracle_weak",
        "post_waiver_stage_ids",
        "post_waiver_selected_feedback",
        "post_waiver_scenario_epoch",
        "post_waiver_oracle_weak",
    }
    polluted_keys = sorted(str(key) for key in repair_patch.keys() if str(key) in forbidden_keys)
    if polluted_keys:
        raise ValueError(
            "waiver entry envelope forbids validation/scenario/oracle/iteration metadata inside repair_patch: "
            + ", ".join(polluted_keys)
        )
    repair_selected = repair_patch.get("selected_feedback")
    if repair_selected is None:
        return None
    if not isinstance(repair_selected, dict):
        raise ValueError("waiver entry envelope requires repair_patch.selected_feedback to be a dict when present")
    validation_selected = (
        _selected_feedback_trace(*validation.selected, scenario_set=validation.scenario_set)
        if validation.selected is not None
        else None
    )
    if not isinstance(validation_selected, dict):
        raise ValueError("waiver entry envelope requires validation.selected when repair_patch.selected_feedback is present")
    for key in ("source", "source_stage"):
        repair_value = repair_selected.get(key)
        validation_value = validation_selected.get(key)
        if repair_value is not None and str(repair_value) != str(validation_value):
            raise ValueError(
                "waiver entry envelope selected_feedback mismatch: "
                f"repair_patch.{key}={repair_value!r} validation_source.{key}={validation_value!r}"
            )
    for key in ("scenario_set_id",):
        repair_value = repair_selected.get(key)
        validation_value = validation_selected.get(key)
        if repair_value is not None and validation_value is not None and str(repair_value) != str(validation_value):
            raise ValueError(
                "waiver entry envelope selected_feedback mismatch: "
                f"repair_patch.{key}={repair_value!r} validation_source.{key}={validation_value!r}"
            )
    return validation_selected


def _build_waiver_entry_envelope(
    *,
    repair_patch: dict[str, Any],
    validation_ref: str,
    validation: Any,
    iteration: int,
) -> dict[str, Any]:
    """Build and validate the LG-B3 repair→waiver entry envelope.

    The envelope is the machine-checkable contract between LG-B2 repair output
    and LG-B3 waiver continuation.  It deliberately keeps repair decision
    evidence in ``repair_patch`` and validation-tail metadata in the transient
    ``_ValidationPass`` source instead of pretending ``repair_patch`` alone
    carries scenario/oracle/iteration state.
    """

    if not isinstance(repair_patch, dict):
        raise TypeError("waiver entry envelope requires repair_patch to be a dict")
    if not bool(repair_patch.get("waiver_continue")):
        raise ValueError("waiver entry envelope requires repair_patch.waiver_continue=true")
    if bool(repair_patch.get("accepted_candidate")):
        raise ValueError("waiver entry envelope requires no accepted_candidate")
    if "candidate_dsl" in repair_patch and str(repair_patch.get("candidate_dsl") or ""):
        raise ValueError("waiver entry envelope forbids non-empty candidate_dsl on no-edit waiver path")
    if not validation_ref:
        raise ValueError("waiver entry envelope requires a validation_ref")
    if not isinstance(validation, _ValidationPass):
        raise TypeError("waiver entry envelope requires validation to be a _ValidationPass")
    validation_selected_trace = _validate_waiver_repair_patch_contract(repair_patch=repair_patch, validation=validation)
    kind = _waiver_kind_from_patch(repair_patch)
    _validate_waiver_kind_selected_consistency(kind=kind, validation=validation)
    start_stage = _waiver_tail_start_stage(kind)
    waiver_audit = repair_patch.get("waiver_audit")
    if kind in {"stale_overridden_scenario_waiver", "sl10_noop_override_waiver"} and not isinstance(waiver_audit, dict):
        raise ValueError("waiver entry envelope requires waiver_audit dict for SD-6 waiver")
    return {
        "schema_version": LG_B3_WAIVER_ENTRY_ENVELOPE_SCHEMA_VERSION,
        "repair_patch": _jsonable(repair_patch),
        "repair_patch_keys": sorted(str(key) for key in repair_patch.keys()),
        "waiver_continue": True,
        "waiver_audit_kind": waiver_audit.get("kind") if isinstance(waiver_audit, dict) else None,
        "accepted_candidate": False,
        "selected_feedback": _jsonable(repair_patch.get("selected_feedback")),
        "repair_stage_ids": _jsonable(repair_patch.get("repair_stage_ids")),
        "exit_reason": repair_patch.get("exit_reason"),
        "validation_ref": validation_ref,
        "validation_source_stage_ids": _stage_ids(validation.stage_metas),
        "validation_scenario_epoch": validation.scenario_epoch,
        "validation_oracle_weak": validation.oracle_weak,
        "validation_source": {
            "object_type": type(validation).__name__,
            "selected_feedback": _jsonable(
                validation_selected_trace
                if validation_selected_trace is not None
                else (
                    _selected_feedback_trace(*validation.selected, scenario_set=validation.scenario_set)
                    if validation.selected is not None
                    else None
                )
            ),
            "stage_ids": _stage_ids(validation.stage_metas),
        },
        "iteration": int(iteration),
        "graph_state_iteration": int(iteration),
        "tail_start_stage": start_stage,
        "tail_kind": kind,
    }


def _drop_repair_subgraph_state(graph_state: dict[str, Any]) -> None:
    for key in list(graph_state.keys()):
        if str(key).startswith("repair_") and key != "repair_patch":
            graph_state.pop(key, None)




def _build_waiver_continuation_subgraph(*, validation_subgraph: Any) -> Any:
    """Build the LG-B3 waiver continuation subgraph.

    The subgraph normalizes the repair→waiver input envelope and delegates the
    actual SD/SL validation-tail semantics to the LG-B1 validation subgraph.
    It intentionally does not redefine SD-4/SD-6/SL-7 academic judgments.
    """

    graph = _d3_state_graph_factory()(_WaiverSubgraphState)

    def _state(graph_state: _WaiverSubgraphState) -> _WaiverSubgraphState:
        return dict(graph_state)

    def _iteration(graph_state: _WaiverSubgraphState) -> int:
        return int(graph_state.get("iteration", 0))

    def waiver_subgraph_enter(graph_state: _WaiverSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state: _RunState = graph_state["runtime_state"]
        iteration = _iteration(graph_state)
        repair_patch = dict(graph_state.get("repair_patch") or {})
        validation_ref = str(graph_state.get("validation_ref") or "")
        validation = graph_state.get("validation_continuation_source")
        if not isinstance(validation, _ValidationPass):
            raise TypeError("waiver continuation subgraph requires a _ValidationPass validation_continuation_source")
        envelope = _build_waiver_entry_envelope(
            repair_patch=repair_patch,
            validation_ref=validation_ref,
            validation=validation,
            iteration=iteration,
        )
        kind = str(envelope["tail_kind"])
        start_stage = str(envelope["tail_start_stage"])
        graph_state["waiver_input_envelope"] = envelope
        graph_state["waiver_validation_ref"] = validation_ref
        graph_state["waiver_validation_source"] = validation
        graph_state["waiver_tail_kind"] = kind
        graph_state["waiver_tail_start_stage"] = start_stage
        _trace_node(graph_state, "waiver_subgraph_enter", event="subgraph_enter", iteration=iteration, tail_kind=kind, tail_start_stage=start_stage)
        _append_flow_log(
            runtime_state.logs,
            event="waiver_subgraph_enter",
            iteration=iteration,
            waiver_tail_kind=kind,
            tail_start_stage=start_stage,
            waiver_input_envelope=_jsonable(envelope),
            graph_subgraph="waiver_continuation_subgraph",
            graph_node="waiver_subgraph_enter",
        )
        return Command(goto="waiver_tail_decision", update=graph_state)

    def waiver_tail_decision(graph_state: _WaiverSubgraphState) -> Command:
        graph_state = _state(graph_state)
        iteration = _iteration(graph_state)
        start_stage = str(graph_state.get("waiver_tail_start_stage") or StageId.SD_4_DESIGN.value)
        kind = str(graph_state.get("waiver_tail_kind") or "design_warning_waiver")
        _trace_node(graph_state, "waiver_tail_decision", iteration=iteration, tail_kind=kind, tail_start_stage=start_stage)
        return Command(goto="waiver_sim_tail" if start_stage == StageId.SD_6_SIM.value else "waiver_design_tail", update=graph_state)

    def _invoke_validation_tail(graph_state: _WaiverSubgraphState, *, tail_node: str) -> _WaiverSubgraphState:
        graph_state = _state(graph_state)
        runtime_state: _RunState = graph_state["runtime_state"]
        iteration = _iteration(graph_state)
        validation = graph_state.get("waiver_validation_source")
        if not isinstance(validation, _ValidationPass):
            validation = graph_state.get("validation_continuation_source")
        if not isinstance(validation, _ValidationPass):
            raise TypeError("waiver continuation tail requires a _ValidationPass validation source")
        graph_state["validation_continuation_source"] = validation
        repair_patch = dict(graph_state.get("repair_patch") or {})
        waiver_audit = repair_patch.get("waiver_audit")
        graph_state["validation_waiver_audit"] = _jsonable(waiver_audit) if isinstance(waiver_audit, dict) else None
        _trace_node(
            graph_state,
            tail_node,
            iteration=iteration,
            tail_kind=graph_state.get("waiver_tail_kind"),
            tail_start_stage=graph_state.get("waiver_tail_start_stage"),
        )
        try:
            invoked = dict(
                validation_subgraph.invoke(
                    graph_state,
                    config={"configurable": {"thread_id": f"{runtime_state.run_id}:waiver-tail:{tail_node}:{iteration}"}},
                )
            )
        except _LLMRetryExhausted as exc:
            graph_state["waiver_retry_error_envelope"] = dict(graph_state.get("waiver_input_envelope") or {})
            graph_state["waiver_retry_error_tail_node"] = tail_node
            raise
        continued_validation = invoked.get("validation_result")
        if not isinstance(continued_validation, _ValidationPass):
            raise TypeError("validation subgraph did not return a _ValidationPass after waiver continuation")
        invoked["waiver_result"] = continued_validation
        return invoked

    def waiver_design_tail(graph_state: _WaiverSubgraphState) -> Command:
        return Command(goto="waiver_subgraph_finalize", update=_invoke_validation_tail(graph_state, tail_node="waiver_design_tail"))

    def waiver_sim_tail(graph_state: _WaiverSubgraphState) -> Command:
        return Command(goto="waiver_subgraph_finalize", update=_invoke_validation_tail(graph_state, tail_node="waiver_sim_tail"))

    def waiver_subgraph_finalize(graph_state: _WaiverSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state: _RunState = graph_state["runtime_state"]
        iteration = _iteration(graph_state)
        continued_validation = graph_state.get("waiver_result")
        if not isinstance(continued_validation, _ValidationPass):
            continued_validation = graph_state.get("validation_result")
        if not isinstance(continued_validation, _ValidationPass):
            raise TypeError("waiver continuation subgraph did not receive a _ValidationPass result")
        envelope = dict(graph_state.get("waiver_input_envelope") or {})
        _trace_node(
            graph_state,
            "waiver_subgraph_finalize",
            event="subgraph_exit",
            iteration=iteration,
            tail_kind=graph_state.get("waiver_tail_kind"),
            tail_start_stage=graph_state.get("waiver_tail_start_stage"),
            post_waiver_stage_ids=_stage_ids(continued_validation.stage_metas),
        )
        _append_flow_log(
            runtime_state.logs,
            event="waiver_subgraph_finalize",
            iteration=iteration,
            waiver_tail_kind=graph_state.get("waiver_tail_kind"),
            tail_start_stage=graph_state.get("waiver_tail_start_stage"),
            post_waiver_stage_ids=_stage_ids(continued_validation.stage_metas),
            waiver_input_envelope_hash=_short_hash(envelope),
            graph_subgraph="waiver_continuation_subgraph",
            graph_node="waiver_subgraph_finalize",
        )
        return Command(goto=END, update=graph_state)

    graph.add_node("waiver_subgraph_enter", waiver_subgraph_enter)
    graph.add_node("waiver_tail_decision", waiver_tail_decision)
    graph.add_node("waiver_design_tail", waiver_design_tail)
    graph.add_node("waiver_sim_tail", waiver_sim_tail)
    graph.add_node("waiver_subgraph_finalize", waiver_subgraph_finalize)
    graph.add_edge(START, "waiver_subgraph_enter")
    graph.add_edge("waiver_subgraph_finalize", END)
    return graph.compile(checkpointer=False)


def _seed_waiver_exception_evidence(
    graph_state: dict[str, Any],
    *,
    envelope: dict[str, Any],
    tail_node: str,
    iteration: int,
    retry_stage_id: str | None = None,
) -> None:
    """Preserve LG-B3 evidence before entering a nested tail that may raise.

    LangGraph subgraph state updates are not returned to the parent when an
    inner node raises ``_LLMRetryExhausted``.  The parent therefore pre-seeds a
    minimal, semantically equivalent trace/envelope so retry-exhausted waiver
    tails remain distinguishable from ordinary validation failures in the final
    ``AgentLoopRunRecord``.
    """

    if not envelope:
        return
    kind = str(envelope.get("tail_kind") or "")
    start_stage = str(envelope.get("tail_start_stage") or "")
    graph_state["waiver_input_envelope"] = dict(envelope)
    graph_state["waiver_tail_kind"] = kind
    graph_state["waiver_tail_start_stage"] = start_stage
    runtime_state = graph_state.get("runtime_state")
    _trace_node(graph_state, "waiver_subgraph_enter", event="subgraph_enter", iteration=iteration, tail_kind=kind, tail_start_stage=start_stage)
    _trace_node(graph_state, "waiver_tail_decision", iteration=iteration, tail_kind=kind, tail_start_stage=start_stage)
    _trace_node(graph_state, tail_node, iteration=iteration, tail_kind=kind, tail_start_stage=start_stage)
    _trace_node(graph_state, "validation_subgraph", event="subgraph_enter", iteration=iteration, continued_after_waiver=True)
    if start_stage == StageId.SD_6_SIM.value:
        _trace_node(graph_state, "validation_sd6_sim", iteration=iteration, continued_after_waiver=True, waiver_audit_kind=envelope.get("waiver_audit_kind"))
    else:
        _trace_node(graph_state, "validation_sd4_design", iteration=iteration, continued_after_waiver=True)
    retry_node_by_stage = {
        StageId.SL_5_SCENARIO_GENERATION.value: "validation_sl5_scenario_generation",
        StageId.SD_5A_SCENARIO_COVERAGE.value: "validation_sd5a_scenario_coverage",
        StageId.SC_5F_SCENARIO_FREEZE.value: "validation_sc5f_scenario_freeze",
        StageId.SD_6_SIM.value: "validation_sd6_sim",
        StageId.SL_7_MODEL_REVIEW.value: "validation_sl7_model_review",
    }
    retry_node = retry_node_by_stage.get(str(retry_stage_id or ""))
    if retry_node is not None:
        _trace_node(graph_state, retry_node, iteration=iteration, continued_after_waiver=True, retry_exhausted=True)
    if isinstance(runtime_state, _RunState):
        _append_flow_log(
            runtime_state.logs,
            event="waiver_subgraph_enter",
            iteration=iteration,
            waiver_tail_kind=kind,
            tail_start_stage=start_stage,
            waiver_input_envelope=_jsonable(envelope),
            graph_subgraph="waiver_continuation_subgraph",
            graph_node="waiver_subgraph_enter",
        )
    seen_trace_keys: set[tuple[str, str, str]] = set()
    deduped_trace: list[dict[str, Any]] = []
    for item in list(graph_state.get("graph_trace", []) or []):
        if not isinstance(item, dict):
            continue
        key = (
            str(item.get("node_id") or ""),
            str(item.get("event") or ""),
            str(item.get("iteration") or ""),
        )
        if key in seen_trace_keys:
            continue
        seen_trace_keys.add(key)
        deduped_trace.append(item)
    graph_state["graph_trace"] = deduped_trace
