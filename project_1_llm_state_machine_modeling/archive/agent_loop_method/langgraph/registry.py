"""Foundation node/edge registry for the project_1 LangGraph runtime.

The registry describes the observable StateGraph contract.  LG-C2 context
engineering identifiers are injected by the public facade in
``archive.agent_loop_method.langgraph_runtime`` so this foundation module does not import the
facade and does not own C-lane context behavior.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from langgraph.graph import END, START

from archive.agent_loop_method.langgraph.constants import LANGGRAPH_RUNTIME_BACKEND, NODE_EDGE_SCHEMA_VERSION
from archive.agent_loop_method.stages.ids import ALL_STAGE_SPECS, StageId


def canonical_stage_ids() -> list[str]:
    """Return the canonical SC/SD/SL stage order used by the graph registry."""

    return [spec.stage_id for spec in ALL_STAGE_SPECS]


def build_langgraph_node_registry(*, context_subgraph_id: str, context_node_ids: Sequence[str]) -> dict[str, Any]:
    """Return PR-langgraph's explicit StateGraph node/edge registry.

    ``context_subgraph_id`` and ``context_node_ids`` are identifier-only values
    injected by ``archive.agent_loop_method.langgraph_runtime``.  The context-engineering subgraph
    behavior, payload assembly, redaction guard, and prompt evidence remain out
    of this D1 foundation module.
    """

    context_node_ids = list(context_node_ids)
    nodes = [
        {
            "node_id": "sc0_start",
            "label": "SC-0 start/run setup",
            "kind": "control_node",
            "stage_ids": [StageId.SC_0_START.value],
            "delegated_subgraph": False,
        },
        {
            "node_id": "sl1_initial_modeling",
            "label": "SL-1 initial NL to DSL modeling",
            "kind": "llm_stage_node",
            "stage_ids": [StageId.SL_1_INITIAL_MODELING.value],
            "delegated_subgraph": False,
        },
        {
            "node_id": "iteration_gate",
            "label": "iteration budget/verdict router",
            "kind": "control_node",
            "stage_ids": [],
            "delegated_subgraph": False,
        },
        {
            "node_id": "validation_pass",
            "label": "SD/SL validation pass",
            "kind": "validation_subgraph",
            "stage_ids": [
                StageId.SD_2_PARSE.value,
                StageId.SD_3_SEMANTIC.value,
                StageId.SD_4_DESIGN.value,
                StageId.SL_5_SCENARIO_GENERATION.value,
                StageId.SD_5A_SCENARIO_COVERAGE.value,
                StageId.SC_5F_SCENARIO_FREEZE.value,
                StageId.SD_6_SIM.value,
                StageId.SL_7_MODEL_REVIEW.value,
            ],
            "delegated_subgraph": True,
            "subgraph_id": "validation_subgraph",
            "subgraph_node_ids": [
                "validation_enter",
                "validation_sd2_parse",
                "validation_sd3_semantic",
                "validation_sd4_design",
                "validation_sl5_scenario_generation",
                "validation_sd5a_scenario_coverage",
                "validation_sd5a_reuse_coverage",
                "validation_sc5f_scenario_freeze",
                "validation_sd6_sim",
                "validation_sl7_model_review",
                "validation_finalize",
            ],
        },
        {
            "node_id": "validation_decision",
            "label": "post-validation success/weak-oracle/repair router",
            "kind": "control_node",
            "stage_ids": [StageId.SC_12_EXIT.value],
            "delegated_subgraph": False,
        },
        {
            "node_id": "repair_path",
            "label": "SD-8 fix requests + SL-9 repair + SL-10 repair review",
            "kind": "repair_subgraph",
            "stage_ids": [
                StageId.SD_8_FIX_PLAN.value,
                StageId.SL_9_REPAIR.value,
                StageId.SL_10_REPAIR_REVIEW.value,
                StageId.SC_11_ACCEPT_CANDIDATE.value,
            ],
            "delegated_subgraph": True,
            "subgraph_id": "repair_subgraph",
            "nested_subgraph_ids": [context_subgraph_id],
            "subgraph_node_ids": [
                "repair_enter",
                "repair_sd8_fix_requests",
                *context_node_ids,
                "repair_sl9_repair",
                "repair_sl10_review",
                "repair_sc11_accept_candidate",
                "repair_finalize",
            ],
        },
        {
            "node_id": "repair_decision",
            "label": "post-repair retry/waiver/budget router",
            "kind": "control_node",
            "stage_ids": [StageId.SC_11_ACCEPT_CANDIDATE.value, StageId.SC_12_EXIT.value],
            "delegated_subgraph": False,
        },
        {
            "node_id": "waiver_continue",
            "label": "continue downstream validation after accepted no-edit waiver",
            "kind": "waiver_continuation_subgraph",
            "stage_ids": [
                StageId.SD_4_DESIGN.value,
                StageId.SL_5_SCENARIO_GENERATION.value,
                StageId.SD_5A_SCENARIO_COVERAGE.value,
                StageId.SC_5F_SCENARIO_FREEZE.value,
                StageId.SD_6_SIM.value,
                StageId.SL_7_MODEL_REVIEW.value,
                StageId.SC_12_EXIT.value,
            ],
            "delegated_subgraph": True,
            "subgraph_id": "waiver_continuation_subgraph",
            "nested_subgraph_ids": ["validation_subgraph"],
            "subgraph_node_ids": [
                "waiver_subgraph_enter",
                "waiver_tail_decision",
                "waiver_design_tail",
                "waiver_sim_tail",
                "waiver_subgraph_finalize",
            ],
            "validation_tail_node_ids": [
                "validation_enter",
                "validation_sd4_design",
                "validation_sl5_scenario_generation",
                "validation_sd5a_scenario_coverage",
                "validation_sd5a_reuse_coverage",
                "validation_sc5f_scenario_freeze",
                "validation_sd6_sim",
                "validation_sl7_model_review",
                "validation_finalize",
            ],
        },
        {
            "node_id": "sc12_budget_exhausted",
            "label": "SC-12 budget-exhausted verdict",
            "kind": "control_node",
            "stage_ids": [StageId.SC_12_EXIT.value],
            "delegated_subgraph": False,
        },
        {
            "node_id": "sc13_trace_audit",
            "label": "SC-13 trace audit and run-record write",
            "kind": "control_node",
            "stage_ids": [StageId.SC_13_TRACE_AUDIT.value],
            "delegated_subgraph": False,
        },
    ]
    edges = [
        {"source": START, "target": "sc0_start"},
        {"source": "sc0_start", "target": "sl1_initial_modeling"},
        {"source": "sl1_initial_modeling", "target": "iteration_gate"},
        {"source": "iteration_gate", "target": "validation_pass", "condition": "continue_validation"},
        {"source": "iteration_gate", "target": "sc12_budget_exhausted", "condition": "budget_exhausted"},
        {"source": "iteration_gate", "target": "sc13_trace_audit", "condition": "verdict_ready"},
        {"source": "validation_pass", "target": "validation_decision"},
        {"source": "validation_decision", "target": "repair_path", "condition": "repair_required"},
        {"source": "validation_decision", "target": "sc13_trace_audit", "condition": "verdict_ready"},
        {"source": "repair_path", "target": "repair_decision"},
        {"source": "repair_decision", "target": "waiver_continue", "condition": "waiver_continue"},
        {"source": "repair_decision", "target": "iteration_gate", "condition": "next_iteration"},
        {"source": "repair_decision", "target": "sc13_trace_audit", "condition": "verdict_ready"},
        {"source": "waiver_continue", "target": "iteration_gate", "condition": "next_iteration"},
        {"source": "waiver_continue", "target": "sc13_trace_audit", "condition": "verdict_ready"},
        {"source": "sc12_budget_exhausted", "target": "sc13_trace_audit"},
        {"source": "sc13_trace_audit", "target": END},
    ]
    return {
        "schema_version": NODE_EDGE_SCHEMA_VERSION,
        "runtime_backend": LANGGRAPH_RUNTIME_BACKEND,
        "opaque_wrapper": False,
        "delegated_monolithic_runtime": False,
        "canonical_stage_sequence": canonical_stage_ids(),
        "nodes": nodes,
        "edges": edges,
        "instrumentation_layer": LANGGRAPH_RUNTIME_BACKEND,
        "notes": [
            "LangGraph owns the default orchestration path; no public staged/langgraph backend switch remains.",
            "archive.agent_loop_method.staged_runtime is reused only as the canonical stage-semantics/helper library.",
        ],
    }


def graph_registry_consistency(planned_stage_graph: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    """Compare planned SC/SD/SL stage IDs with LangGraph registry coverage."""

    planned = [str(item) for item in planned_stage_graph.get("planned", [])]
    covered: list[str] = []
    node_stage_pairs: list[dict[str, str]] = []
    for node in registry.get("nodes", []):
        node_id = str(node.get("node_id") or "")
        for stage_id in node.get("stage_ids", []):
            covered_stage_id = str(stage_id)
            covered.append(covered_stage_id)
            node_stage_pairs.append({"node_id": node_id, "stage_id": covered_stage_id})
    covered_set = set(covered)
    planned_set = set(planned)
    missing = [stage_id for stage_id in planned if stage_id not in covered_set]
    extra = [stage_id for stage_id in covered if stage_id not in planned_set]
    duplicate_stage_ids = sorted({stage_id for stage_id in covered if covered.count(stage_id) > 1})
    duplicate_stage_id_nodes = {
        stage_id: [item["node_id"] for item in node_stage_pairs if item["stage_id"] == stage_id]
        for stage_id in duplicate_stage_ids
    }
    opaque = bool(registry.get("opaque_wrapper")) or len(registry.get("nodes", [])) <= 1
    delegated_monolithic = bool(registry.get("delegated_monolithic_runtime")) or any(
        str(node.get("delegation_target") or "").endswith("run_full_staged_deterministic_runtime")
        for node in registry.get("nodes", [])
        if isinstance(node, dict)
    )
    return {
        "ok": not missing and not extra and not opaque and not delegated_monolithic,
        "missing_stage_ids": missing,
        "extra_stage_ids": extra,
        "opaque_wrapper": opaque,
        "delegated_monolithic_runtime": delegated_monolithic,
        "planned_count": len(planned),
        "covered_count": len(covered),
        "duplicate_stage_ids": duplicate_stage_ids,
        "duplicate_stage_id_nodes": duplicate_stage_id_nodes,
        "duplicate_stage_id_policy": (
            "allowed_when_one SC/SD/SL stage is represented by both a stage_group node "
            "and a routing/audit control node; duplicates are reported for audit and "
            "do not by themselves make registry coverage invalid"
        ),
    }


__all__ = [
    "build_langgraph_node_registry",
    "canonical_stage_ids",
    "graph_registry_consistency",
]
