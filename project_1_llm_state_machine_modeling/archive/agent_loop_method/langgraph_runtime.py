"""Compatibility facade for the default LangGraph runtime.

LG-M1-D3 moves the implementation into ``method.langgraph`` modules while this
file keeps historical import paths and run-record identity stable.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from method.llm_stages import ChatProvider
from method.schema import AgentLoopResult, LoopConfig
from method.staged_runtime import FullStagedRuntimeAdapters
from method.langgraph import core as _core
from method.langgraph.core import *  # noqa: F403 - legacy compatibility facade intentionally re-exports private helpers.
from method.langgraph.subgraphs.validation import _ValidationSubgraphState, _build_validation_subgraph
from method.langgraph.subgraphs.waiver import (
    _WaiverSubgraphState,
    _build_waiver_continuation_subgraph,
    _build_waiver_entry_envelope,
    _drop_repair_subgraph_state,
    _seed_waiver_exception_evidence,
    _validate_waiver_kind_selected_consistency,
    _validate_waiver_repair_patch_contract,
    _waiver_kind_from_patch,
    _waiver_tail_start_stage,
)
from method.langgraph.subgraphs.repair import _RepairSubgraphState, _build_repair_subgraph
from method.langgraph import resume as _resume
from method.langgraph.resume import (
    _lg_f1_actual_interrupt_node,
    _lg_f1_append_only_audit,
    _lg_f1_checkpoint_id_hash,
    _lg_f1_compare_hash,
    _lg_f1_comparison_checks,
    _lg_f1_finalize_result,
    _lg_f1_graph_config,
    _lg_f1_path_hash,
    _lg_f1_prepare_runtime,
    _lg_f1_runtime_config,
    _lg_f1_sqlite_saver,
    _lg_f1_stage_replay_audit,
    _lg_f1_state_snapshot,
    _lg_f1_record_snapshot,
    _lg_f1_prefix_preserved,
    _lg_f1_patch_record_with_report,
)


def build_langgraph_node_registry() -> dict[str, Any]:
    return _core.build_langgraph_node_registry()


def graph_registry_consistency(planned_stage_graph: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    return _core.graph_registry_consistency(planned_stage_graph, registry)


def run_full_staged_langgraph_runtime(
    nl: str,
    *,
    config: LoopConfig,
    adapters: FullStagedRuntimeAdapters,
    initial_dsl: str = "",
    planned_stage_graph: dict[str, Any] | None = None,
    resolved_config: dict[str, Any] | None = None,
    run_id: str | None = None,
    provider: ChatProvider | None = None,
    called_from_loop: bool = False,
    operator_stream_enabled: bool = True,
    toolnode_wrapper_enabled: bool = True,
    lg_e2_send_parallel_enabled: bool = True,
) -> AgentLoopResult:
    return _core.run_full_staged_langgraph_runtime(
        nl,
        config=config,
        adapters=adapters,
        initial_dsl=initial_dsl,
        planned_stage_graph=planned_stage_graph,
        resolved_config=resolved_config,
        run_id=run_id,
        provider=provider,
        called_from_loop=called_from_loop,
        operator_stream_enabled=operator_stream_enabled,
        toolnode_wrapper_enabled=toolnode_wrapper_enabled,
        lg_e2_send_parallel_enabled=lg_e2_send_parallel_enabled,
    )


def resume_lg_f1_from_checkpoint(
    *,
    checkpoint_path: str | Path,
    thread_id: str,
    expected_graph_config_hash: str | None = None,
    graph_config_hash: str | None = None,
    checkpoint_id_hash: str | None = None,
    checkpoint_id: str | None = None,
    config: LoopConfig,
    adapters: FullStagedRuntimeAdapters,
    nl: str = "LG-F1 resume from durable checkpoint.",
    initial_dsl: str = "",
    interrupt_after: str = "repair_path",
    resume_diff_report_path: str | None = None,
    operator_stream_enabled: bool = False,
    toolnode_wrapper_enabled: bool = True,
    provider: ChatProvider | None = None,
) -> dict[str, Any]:
    expected_hash = expected_graph_config_hash if expected_graph_config_hash is not None else graph_config_hash
    return _resume.resume_lg_f1_from_checkpoint(
        checkpoint_path=checkpoint_path,
        thread_id=thread_id,
        expected_graph_config_hash=expected_hash or "",
        config=config,
        adapters=adapters,
        nl=nl,
        initial_dsl=initial_dsl,
        interrupt_after=interrupt_after,
        checkpoint_id_hash=checkpoint_id_hash if checkpoint_id_hash is not None else checkpoint_id,
        resume_diff_report_path=resume_diff_report_path,
        operator_stream_enabled=operator_stream_enabled,
        toolnode_wrapper_enabled=toolnode_wrapper_enabled,
        provider=provider,
    )


def run_lg_f1_resume_experiment(
    nl: str,
    *,
    config: LoopConfig,
    adapters: FullStagedRuntimeAdapters,
    initial_dsl: str = "",
    checkpoint_path: str | Path,
    interrupt_after: str = "repair_path",
    operator_stream_enabled: bool = False,
    toolnode_wrapper_enabled: bool = True,
    provider: ChatProvider | None = None,
    uninterrupted_adapters: FullStagedRuntimeAdapters | None = None,
    uninterrupted_provider: ChatProvider | None = None,
) -> dict[str, Any]:
    return _resume.run_lg_f1_resume_experiment(
        nl,
        config=config,
        adapters=adapters,
        initial_dsl=initial_dsl,
        checkpoint_path=checkpoint_path,
        interrupt_after=interrupt_after,
        operator_stream_enabled=operator_stream_enabled,
        toolnode_wrapper_enabled=toolnode_wrapper_enabled,
        provider=provider,
        uninterrupted_adapters=uninterrupted_adapters,
        uninterrupted_provider=uninterrupted_provider,
    )


__all__ = [name for name in globals() if not name.startswith("__") and name not in {"_core", "_resume"}]
