"""LG-E3 fixed ToolNode-style instrumentation wrappers.

The wrappers are deterministic stage-call wrappers; they do not expose tools to
LLM tool-choice and do not replace canonical SD/SL evidence.
"""

from __future__ import annotations

import json
from typing import Any

from method.langgraph.instrumentation.common import _hash_payload, _jsonable
from method.langgraph.instrumentation.operator_stream import _LG_D1_ACADEMIC_EVIDENCE_SOURCES, _append_lg_d1_operator_event
from method.run_record import read_agent_loop_run_record, write_agent_loop_run_record
from method.schema import AgentLoopResult
from method.staged_runtime import FullStagedRuntimeConfig, _hash_text
from method.stages.ids import StageId

LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION = "lg-e3.fixed-toolnode-wrapper.v1"

LG_E3_TOOLNODE_WRAPPER_INSTRUMENTATION_LAYER = "fixed_toolnode_wrapper"

def build_lg_e3_toolnode_wrapper_registry() -> dict[str, Any]:
    """Return the fixed ToolNode-style wrapper contract for deterministic SD tools.

    LG-E3 deliberately does **not** expose these tools to LLM tool-choice.  The
    graph/stage nodes call the wrappers in fixed stage order and the wrappers
    only add prompt-safe instrumentation around the original deterministic
    callable.  Canonical checker outputs and verdict sources remain the original
    SD tool return values.
    """

    def row(tool_name: str, stage_id: str, graph_nodes: list[str], callable_ref: str) -> dict[str, Any]:
        return {
            "tool_name": tool_name,
            "tool_schema_version": LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION,
            "stage_id": stage_id,
            "graph_nodes": list(graph_nodes),
            "callable_ref": callable_ref,
            "wrapper_kind": "custom_langgraph_visible_fixed_toolnode_wrapper",
            "fixed_invocation": True,
            "llm_tool_choice_exposed": False,
            "input_policy": "hash_and_safe_summary_only",
            "output_policy": "hash_and_safe_summary_only",
            "does_not_replace_academic_evidence": True,
        }

    wrappers = [
        row("sd2_parse", StageId.SD_2_PARSE.value, ["validation_sd2_parse"], "FullStagedRuntimeAdapters.parse"),
        row("sd3_semantic", StageId.SD_3_SEMANTIC.value, ["validation_sd3_semantic"], "FullStagedRuntimeAdapters.semantic"),
        row("sd4_design", StageId.SD_4_DESIGN.value, ["validation_sd4_design"], "FullStagedRuntimeAdapters.design"),
        row(
            "sd5a_scenario_coverage",
            StageId.SD_5A_SCENARIO_COVERAGE.value,
            ["validation_sd5a_scenario_coverage", "validation_sd5a_reuse_coverage"],
            "FullStagedRuntimeAdapters.scenario_coverage",
        ),
        row("sc5f_freeze_scenario_set", StageId.SC_5F_SCENARIO_FREEZE.value, ["validation_sc5f_scenario_freeze"], "freeze_scenario_set"),
        row("sd6_sim", StageId.SD_6_SIM.value, ["validation_sd6_sim"], "FullStagedRuntimeAdapters.sim"),
        row("sd8_fix_plan", StageId.SD_8_FIX_PLAN.value, ["repair_sd8_fix_requests"], "run_sd8_fix_plan"),
        row("sd10_repair_review_local_check", StageId.SD_10_REPAIR_REVIEW.value, ["repair_sl10_review"], "FullStagedRuntimeAdapters.repair_review"),
        row("warning_repair_attempt_marker", "warning_budget_state", ["repair_sd8_fix_requests"], "mark_warning_repair_attempt"),
    ]
    return {
        "schema_version": LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION,
        "instrumentation_layer": LG_E3_TOOLNODE_WRAPPER_INSTRUMENTATION_LAYER,
        "enabled_by_default": True,
        "fixed_invocation": True,
        "llm_tool_choice_exposed": False,
        "does_not_replace_academic_evidence": True,
        "academic_evidence_sources": list(_LG_D1_ACADEMIC_EVIDENCE_SOURCES),
        "wrappers": wrappers,
    }

def _lg_e3_toolnode_wrappers_enabled(runtime_cfg: FullStagedRuntimeConfig) -> bool:
    return bool(runtime_cfg.run_config_extra.get("lg_e3_toolnode_wrappers_enabled", True))

_LG_E3_SENSITIVE_SUMMARY_KEY_EXACT = {
    "dsl",
    "current_dsl",
    "old_dsl",
    "before_dsl",
    "after_dsl",
    "candidate_dsl",
    "repair_candidate_dsl",
    "source_dsl",
    "final_dsl",
    "nl",
    "messages",
    "prompt",
    "raw_prompt",
    "raw_input",
    "raw_output",
}

def _lg_e3_summary_key_is_sensitive(key_text: str) -> bool:
    normalized = key_text.lower()
    return (
        normalized in _LG_E3_SENSITIVE_SUMMARY_KEY_EXACT
        or normalized.endswith("_dsl")
        or normalized.startswith("raw_")
        or "prompt" in normalized
        or normalized in {"nl", "messages"}
    )

def _safe_lg_e3_tool_summary(value: Any) -> Any:
    safe = _jsonable(value)
    if isinstance(safe, dict):
        out: dict[str, Any] = {}
        for key, nested in safe.items():
            key_text = str(key)
            if _lg_e3_summary_key_is_sensitive(key_text):
                out[f"{key_text}_hash"] = _hash_payload(nested)
                out[f"{key_text}_chars"] = len(json.dumps(_jsonable(nested), ensure_ascii=False, sort_keys=True, default=str))
                continue
            if isinstance(nested, (dict, list, tuple, set)):
                out[f"{key_text}_hash"] = _hash_payload(nested)
                if isinstance(nested, dict):
                    out[f"{key_text}_key_count"] = len(nested)
                else:
                    out[f"{key_text}_count"] = len(nested)
                continue
            out[key_text] = nested
        return out
    if isinstance(safe, list):
        return {"item_count": len(safe), "items_hash": _hash_payload(safe)}
    if isinstance(safe, str):
        return {"text_hash": _hash_text(safe), "text_chars": len(safe)}
    return safe

def _record_lg_e3_toolnode_event(
    graph_state: _GraphLoopState,
    *,
    tool_name: str,
    stage_id: str,
    graph_node: str,
    iteration: int | None,
    input_payload: Any,
    output_payload: Any,
    status: str = "ok",
) -> None:
    if not bool(graph_state.get("toolnode_wrapper_enabled", True)):
        return
    event = {
        "schema_version": LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION,
        "instrumentation_layer": LG_E3_TOOLNODE_WRAPPER_INSTRUMENTATION_LAYER,
        "tool_name": tool_name,
        "tool_schema_version": LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION,
        "stage_id": stage_id,
        "graph_node": graph_node,
        "iteration": iteration,
        "fixed_invocation": True,
        "llm_tool_choice_exposed": False,
        "status": status,
        "input_hash": _hash_payload(input_payload),
        "output_hash": _hash_payload(output_payload),
        "input_summary": _safe_lg_e3_tool_summary(input_payload),
        "output_summary": _safe_lg_e3_tool_summary(output_payload),
        "does_not_replace_academic_evidence": True,
    }
    # Fail early if the wrapper accidentally starts carrying raw evidence fields.
    json.dumps(event, ensure_ascii=False, sort_keys=True, allow_nan=False)
    events = list(graph_state.get("toolnode_wrapper_events", []) or [])
    events.append(event)
    graph_state["toolnode_wrapper_events"] = events
    _append_lg_d1_operator_event(
        graph_state,
        event_type="fixed_toolnode_result",
        node=graph_node,
        stage_id=stage_id if stage_id.startswith(("SC-", "SD-", "SL-")) else None,
        payload={
            "tool_name": tool_name,
            "tool_schema_version": LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION,
            "input_hash": event["input_hash"],
            "output_hash": event["output_hash"],
            "fixed_invocation": True,
            "llm_tool_choice_exposed": False,
            "status": status,
        },
    )

def _lg_e3_fixed_tool_call(
    graph_state: _GraphLoopState,
    *,
    tool_name: str,
    stage_id: str,
    graph_node: str,
    iteration: int | None,
    input_payload: Any,
    call: Any,
) -> Any:
    if not bool(graph_state.get("toolnode_wrapper_enabled", True)):
        return call()
    try:
        output = call()
    except Exception as exc:
        _record_lg_e3_toolnode_event(
            graph_state,
            tool_name=tool_name,
            stage_id=stage_id,
            graph_node=graph_node,
            iteration=iteration,
            input_payload=input_payload,
            output_payload={"error_type": type(exc).__name__, "error_hash": _hash_text(str(exc))},
            status="error",
        )
        raise
    _record_lg_e3_toolnode_event(
        graph_state,
        tool_name=tool_name,
        stage_id=stage_id,
        graph_node=graph_node,
        iteration=iteration,
        input_payload=input_payload,
        output_payload=output,
        status="ok",
    )
    return output

def _augment_run_record_with_lg_e3_toolnode_trace(
    result: AgentLoopResult,
    *,
    events: list[dict[str, Any]],
    enabled: bool,
) -> None:
    if not result.run_record_path:
        return
    path = result.run_record_path
    record = read_agent_loop_run_record(path)
    safe_events = _jsonable(events if enabled else [])
    registry = build_lg_e3_toolnode_wrapper_registry()
    trace = {
        "schema_version": LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION,
        "instrumentation_layer": LG_E3_TOOLNODE_WRAPPER_INSTRUMENTATION_LAYER,
        "enabled": bool(enabled),
        "fixed_invocation": True,
        "llm_tool_choice_exposed": False,
        "event_count": len(safe_events),
        "events_hash": _hash_payload(safe_events),
        "covered_tool_names": sorted({str(event.get("tool_name") or "") for event in safe_events if isinstance(event, dict)}),
        "registry_hash": _hash_payload(registry),
        "does_not_replace_academic_evidence": True,
        "academic_evidence_sources": list(_LG_D1_ACADEMIC_EVIDENCE_SOURCES),
        "events": safe_events,
    }
    record.environment["lg_e3_toolnode_wrappers_enabled"] = bool(enabled)
    record.environment["lg_e3_toolnode_wrapper_schema_version"] = LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION
    record.environment["lg_e3_toolnode_wrapper_event_count"] = len(safe_events)
    record.environment["lg_e3_toolnode_wrapper_events_hash"] = trace["events_hash"]
    record.environment["lg_e3_toolnode_wrapper_registry_hash"] = trace["registry_hash"]
    record.environment["lg_e3_toolnode_wrapper_llm_tool_choice_exposed"] = False
    record.run_config["lg_e3_toolnode_wrappers_enabled"] = bool(enabled)
    record.run_config["lg_e3_toolnode_wrapper_schema_version"] = LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION
    record.run_config["lg_e3_toolnode_wrapper_registry"] = registry
    record.final_artifacts["toolnode_wrapper_trace"] = trace
    record.logs.append(
        {
            "event": "lg_e3_toolnode_wrapper_trace",
            "instrumentation_layer": LG_E3_TOOLNODE_WRAPPER_INSTRUMENTATION_LAYER,
            "enabled": bool(enabled),
            "event_count": len(safe_events),
            "events_hash": trace["events_hash"],
            "does_not_replace_academic_evidence": True,
        }
    )
    write_agent_loop_run_record(record, path)

