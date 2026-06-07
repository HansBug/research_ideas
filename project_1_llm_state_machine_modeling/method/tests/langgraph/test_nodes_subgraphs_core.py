"""LG-M1-D3 LangGraph nodes / subgraphs / core split characterization tests.

These tests lock D3's maintainability refactor boundary: the default runtime
implementation moves into method.langgraph modules, the historical facade keeps
public identity stable, experiments import the non-facade F1 implementation, and
LG-C1 graph-state helper names remain centralized in core.py for auditability.
"""

from __future__ import annotations

import ast
import importlib
from pathlib import Path
from typing import Any

from method.run_record import read_agent_loop_run_record, write_agent_loop_run_record
from method.schema import AgentLoopResult, AgentLoopRunRecord


REPO_ROOT = Path(__file__).resolve().parents[4]
METHOD_ROOT = REPO_ROOT / "project_1_llm_state_machine_modeling" / "method"
LANGGRAPH_ROOT = METHOD_ROOT / "langgraph"

EXPECTED_MODULES = {
    "method.langgraph.core": [
        "_GraphLoopState",
        "_build_graph",
        "run_full_staged_langgraph_runtime",
        "_refresh_graph_state_readiness_after_operator_log",
    ],
    "method.langgraph.resume": [
        "_lg_f1_checkpoint_id_hash",
        "resume_lg_f1_from_checkpoint",
        "run_lg_f1_resume_experiment",
    ],
    "method.langgraph.subgraphs.validation": ["_ValidationSubgraphState", "_build_validation_subgraph"],
    "method.langgraph.subgraphs.repair": ["_RepairSubgraphState", "_build_repair_subgraph"],
    "method.langgraph.subgraphs.waiver": [
        "_WaiverSubgraphState",
        "_build_waiver_continuation_subgraph",
        "_build_waiver_entry_envelope",
    ],
    "method.langgraph.nodes.sc": ["SC_NODE_IDS", "register_sc_nodes"],
    "method.langgraph.nodes.sd": ["SD_NODE_IDS", "register_sd_nodes"],
    "method.langgraph.nodes.sl": ["SL_NODE_IDS", "register_sl_nodes"],
}


def _module_imports(path: Path) -> list[ast.Import | ast.ImportFrom]:
    module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return [node for node in ast.walk(module) if isinstance(node, (ast.Import, ast.ImportFrom))]


def test_lg_m1_d3_expected_modules_are_importable_and_own_symbols() -> None:
    for module_name, symbols in EXPECTED_MODULES.items():
        module = importlib.import_module(module_name)
        for symbol in symbols:
            assert hasattr(module, symbol), f"{module_name}.{symbol} missing"
            value = getattr(module, symbol)
            if callable(value) or isinstance(value, type):
                assert getattr(value, "__module__", module_name) == module_name


def test_lg_m1_d3_facade_keeps_public_identity_and_reexports_moved_objects() -> None:
    facade = importlib.import_module("method.langgraph_runtime")
    core = importlib.import_module("method.langgraph.core")
    resume = importlib.import_module("method.langgraph.resume")
    validation = importlib.import_module("method.langgraph.subgraphs.validation")
    repair = importlib.import_module("method.langgraph.subgraphs.repair")
    waiver = importlib.import_module("method.langgraph.subgraphs.waiver")

    assert facade.run_full_staged_langgraph_runtime.__module__ == "method.langgraph_runtime"
    assert facade.run_lg_f1_resume_experiment.__module__ == "method.langgraph_runtime"
    assert facade.resume_lg_f1_from_checkpoint.__module__ == "method.langgraph_runtime"
    assert facade.graph_registry_consistency.__module__ == "method.langgraph_runtime"

    assert facade._build_graph is core._build_graph
    assert facade._GraphLoopState is core._GraphLoopState
    assert facade._ValidationSubgraphState is validation._ValidationSubgraphState
    assert facade._RepairSubgraphState is repair._RepairSubgraphState
    assert facade._WaiverSubgraphState is waiver._WaiverSubgraphState
    assert facade._build_validation_subgraph is validation._build_validation_subgraph
    assert facade._build_repair_subgraph is repair._build_repair_subgraph
    assert facade._build_waiver_continuation_subgraph is waiver._build_waiver_continuation_subgraph
    assert facade._build_waiver_entry_envelope is waiver._build_waiver_entry_envelope
    assert facade._lg_f1_checkpoint_id_hash is resume._lg_f1_checkpoint_id_hash


def test_lg_m1_d3_langgraph_and_experiments_do_not_reverse_import_runtime_facade() -> None:
    checked_roots = [LANGGRAPH_ROOT, METHOD_ROOT / "experiments", METHOD_ROOT / "stages"]
    forbidden: list[str] = []
    for root in checked_roots:
        for path in sorted(root.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            rel = str(path.relative_to(REPO_ROOT))
            for node in _module_imports(path):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name == "method.langgraph_runtime":
                            forbidden.append(f"{rel} imports {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    if node.module == "method.langgraph_runtime":
                        forbidden.append(f"{rel} imports from method.langgraph_runtime")
                    if node.module == "method" and any(alias.name == "langgraph_runtime" for alias in node.names):
                        forbidden.append(f"{rel} imports method.langgraph_runtime via method re-export")
    assert forbidden == []


def test_lg_m1_d3_lg_c1_helpers_are_core_only() -> None:
    leaks: list[str] = []
    for path in sorted(LANGGRAPH_ROOT.rglob("*.py")):
        if "__pycache__" in path.parts or path.name == "core.py":
            continue
        if "_lg_c1_" in path.read_text(encoding="utf-8"):
            leaks.append(str(path.relative_to(REPO_ROOT)))
    assert leaks == []


def test_lg_m1_d3_node_registration_modules_preserve_top_level_node_ids() -> None:
    sc = importlib.import_module("method.langgraph.nodes.sc")
    sd = importlib.import_module("method.langgraph.nodes.sd")
    sl = importlib.import_module("method.langgraph.nodes.sl")

    assert sc.SC_NODE_IDS == (
        "sc0_start",
        "iteration_gate",
        "validation_decision",
        "repair_decision",
        "waiver_continue",
        "sc12_budget_exhausted",
        "sc13_trace_audit",
    )
    assert sd.SD_NODE_IDS == ("validation_pass", "repair_path")
    assert sl.SL_NODE_IDS == ("sl1_initial_modeling",)

    class CapturingGraph:
        def __init__(self) -> None:
            self.nodes: dict[str, Any] = {}

        def add_node(self, node_id: str, fn: Any) -> None:
            self.nodes[node_id] = fn

    graph = CapturingGraph()
    sentinel = lambda state: state
    sc.register_sc_nodes(
        graph,
        sc0_start=sentinel,
        iteration_gate=sentinel,
        validation_decision=sentinel,
        repair_decision=sentinel,
        waiver_continue=sentinel,
        sc12_budget_exhausted=sentinel,
        sc13_trace_audit=sentinel,
    )
    sd.register_sd_nodes(graph, validation_pass=sentinel, repair_path=sentinel)
    sl.register_sl_nodes(graph, sl1_initial_modeling=sentinel)

    assert tuple(graph.nodes) == sc.SC_NODE_IDS + sd.SD_NODE_IDS + sl.SL_NODE_IDS


def test_lg_m1_d3_f1_experiment_imports_resume_implementation_not_facade() -> None:
    source = (METHOD_ROOT / "experiments" / "checkpoint_resume.py").read_text(encoding="utf-8")
    assert "from method.langgraph.resume import run_lg_f1_resume_experiment" in source
    assert "method.langgraph_runtime" not in source


def test_lg_m1_d3_graph_trace_final_artifacts_include_validation_subgraph_summary(tmp_path: Path) -> None:
    core = importlib.import_module("method.langgraph.core")
    record_path = tmp_path / "d3-validation-trace.agent_loop.json.gz"
    write_agent_loop_run_record(
        AgentLoopRunRecord(
            schema_version="test",
            run_id="d3-validation-trace",
            created_at="2026-06-07T00:00:00Z",
            status="success",
            input_bundle={},
            run_config={},
            environment={},
            stage_graph={},
            stage_records=[],
            iteration_records=[],
            final_artifacts={},
        ),
        record_path,
    )
    result = AgentLoopResult(status="converged", run_record_id="d3-validation-trace", run_record_path=str(record_path))
    graph_trace = [
        {"event": "node_enter", "node_id": "validation_pass", "iteration": 0},
        {"event": "subgraph_enter", "node_id": "validation_subgraph", "iteration": 0},
        {"event": "node_enter", "node_id": "validation_sd2_parse", "iteration": 0},
        {"event": "node_enter", "node_id": "validation_sd4_design", "iteration": 0, "continued_after_waiver": True},
        {"event": "node_enter", "node_id": "validation_sl5_scenario_generation", "iteration": 0, "attempt_index": 1},
        {"event": "node_enter", "node_id": "validation_sd6_sim", "iteration": 0},
        {"event": "subgraph_exit", "node_id": "validation_finalize", "iteration": 0},
        {"event": "node_enter", "node_id": "repair_enter", "iteration": 0},
        {"event": "node_enter", "node_id": "waiver_subgraph_enter", "iteration": 0},
    ]

    core._augment_run_record_with_graph_trace(result, graph_trace)

    record = read_agent_loop_run_record(record_path)
    runtime_trace = record.final_artifacts["langgraph_runtime_trace"]
    validation = runtime_trace["validation_subgraph_runtime_trace"]
    assert validation["subgraph_id"] == "validation_subgraph"
    assert validation["node_trace_count"] == 6
    assert validation["node_trace_hash"].startswith("sha256:")
    assert validation["node_ids"] == [
        "validation_subgraph",
        "validation_sd2_parse",
        "validation_sd4_design",
        "validation_sl5_scenario_generation",
        "validation_sd6_sim",
        "validation_finalize",
    ]
    assert validation["stage_node_ids"] == [
        "validation_sd2_parse",
        "validation_sd4_design",
        "validation_sl5_scenario_generation",
        "validation_sd6_sim",
    ]
    assert "continued_after_waiver" in validation["join_key_fields"]
    assert "repair_subgraph_runtime_trace" in runtime_trace
    assert "waiver_subgraph_runtime_trace" in runtime_trace
