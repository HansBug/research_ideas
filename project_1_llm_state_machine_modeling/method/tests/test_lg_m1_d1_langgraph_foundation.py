"""LG-M1-D1 LangGraph foundation split characterization tests.

These tests lock the D1 contract only: foundation modules exist, the public
``method.langgraph_runtime`` facade remains stable, registry output is
canonically equivalent to the LG-M1-A baseline, and D1 does not smuggle C/E lane
runtime state or behavior into ``method.langgraph``.
"""

from __future__ import annotations

import ast
import hashlib
import importlib
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
METHOD_ROOT = REPO_ROOT / "project_1_llm_state_machine_modeling" / "method"
LANGGRAPH_ROOT = METHOD_ROOT / "langgraph"
BASELINE_PATH = METHOD_ROOT / "tests" / "fixtures" / "lg_m1_a_baseline.json"


def _load_baseline() -> dict[str, Any]:
    return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))


def _sha256_json(payload: object) -> str:
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(data.encode("utf-8")).hexdigest()


def _stable_graph_contract(registry: dict[str, Any], consistency: dict[str, Any], planned_stage_order: list[str]) -> dict[str, Any]:
    stable_registry = {
        "schema_version": registry.get("schema_version"),
        "runtime_backend": registry.get("runtime_backend"),
        "opaque_wrapper": registry.get("opaque_wrapper"),
        "delegated_monolithic_runtime": registry.get("delegated_monolithic_runtime"),
        "instrumentation_layer": registry.get("instrumentation_layer"),
        "canonical_stage_sequence": registry.get("canonical_stage_sequence"),
        "nodes": [
            {
                "node_id": node.get("node_id"),
                "kind": node.get("kind"),
                "stage_ids": node.get("stage_ids", []),
                "delegated_subgraph": bool(node.get("delegated_subgraph", False)),
                "subgraph_id": node.get("subgraph_id"),
                "nested_subgraph_ids": node.get("nested_subgraph_ids", []),
            }
            for node in registry.get("nodes", [])
        ],
        "edges": [
            {"source": edge.get("source"), "target": edge.get("target"), "condition": edge.get("condition")}
            for edge in registry.get("edges", [])
        ],
    }
    canonical_input = {"registry": stable_registry, "planned_stage_order": planned_stage_order, "consistency": consistency}
    return {
        "registry": stable_registry,
        "planned_stage_order": planned_stage_order,
        "consistency": consistency,
        "canonical_hash": _sha256_json(canonical_input),
    }


def test_lg_m1_d1_foundation_modules_do_not_reverse_import_runtime_facade() -> None:
    assert LANGGRAPH_ROOT.exists()
    checked = sorted(path for path in LANGGRAPH_ROOT.rglob("*.py") if "__pycache__" not in path.parts)
    assert checked, "D1 must create importable method/langgraph foundation modules"

    forbidden: list[str] = []
    for path in checked:
        module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(module):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "method.langgraph_runtime":
                        forbidden.append(f"{path.relative_to(REPO_ROOT)} imports {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                if node.module == "method.langgraph_runtime":
                    forbidden.append(f"{path.relative_to(REPO_ROOT)} imports from method.langgraph_runtime")
                if node.module == "method" and any(alias.name == "langgraph_runtime" for alias in node.names):
                    forbidden.append(f"{path.relative_to(REPO_ROOT)} imports method.langgraph_runtime via method re-export")
    assert forbidden == []


def test_lg_m1_d1_facade_constants_and_runtime_identity_stay_stable() -> None:
    from method.langgraph import constants as foundation_constants

    facade = importlib.import_module("method.langgraph_runtime")
    baseline = _load_baseline()
    runtime_identity = baseline["runtime_identity"]

    assert facade.GRAPH_RUNTIME_SCHEMA_VERSION == foundation_constants.GRAPH_RUNTIME_SCHEMA_VERSION
    assert facade.NODE_EDGE_SCHEMA_VERSION == foundation_constants.NODE_EDGE_SCHEMA_VERSION
    assert foundation_constants.GRAPH_RUNTIME_ID == runtime_identity["environment"]["graph_runtime_id"]
    assert facade.run_full_staged_langgraph_runtime.__module__ == "method.langgraph_runtime"
    assert runtime_identity["run_config"]["runtime_implementation"] == "method.langgraph_runtime.run_full_staged_langgraph_runtime"


def test_lg_m1_d1_registry_foundation_matches_facade_and_lg_m1_a_hash() -> None:
    from method.langgraph import registry as foundation_registry
    from method.loop import build_planned_stage_graph
    from method.schema import LoopConfig

    facade = importlib.import_module("method.langgraph_runtime")
    planned = build_planned_stage_graph(LoopConfig())
    planned_stage_order = [node.get("stage_id") for node in planned.get("nodes", [])]
    facade_registry = facade.build_langgraph_node_registry()
    foundation_output = foundation_registry.build_langgraph_node_registry(
        context_subgraph_id=facade.LG_C2_CONTEXT_SUBGRAPH_ID,
        context_node_ids=facade.LG_C2_CONTEXT_NODE_IDS,
    )

    assert foundation_output == facade_registry
    assert facade.graph_registry_consistency is foundation_registry.graph_registry_consistency
    consistency = facade.graph_registry_consistency(planned, facade_registry)
    graph = _stable_graph_contract(facade_registry, consistency, planned_stage_order)

    baseline_graph = _load_baseline()["graph_contract"]
    assert graph["canonical_hash"] == baseline_graph["canonical_hash"]
    assert graph["consistency"]["ok"] is True
    assert graph["planned_stage_order"] == graph["registry"]["canonical_stage_sequence"]
    assert graph["registry"]["opaque_wrapper"] is False
    assert graph["registry"]["delegated_monolithic_runtime"] is False


def test_lg_m1_d1_registry_context_identifiers_are_injected_without_c_lane_behavior() -> None:
    from method.langgraph import registry as foundation_registry

    facade = importlib.import_module("method.langgraph_runtime")
    fake = foundation_registry.build_langgraph_node_registry(
        context_subgraph_id="fake_context_subgraph",
        context_node_ids=["fake_collect", "fake_guard"],
    )
    real = foundation_registry.build_langgraph_node_registry(
        context_subgraph_id=facade.LG_C2_CONTEXT_SUBGRAPH_ID,
        context_node_ids=facade.LG_C2_CONTEXT_NODE_IDS,
    )

    fake_repair = next(node for node in fake["nodes"] if node["node_id"] == "repair_path")
    real_repair = next(node for node in real["nodes"] if node["node_id"] == "repair_path")
    fake_other_nodes = [node for node in fake["nodes"] if node["node_id"] != "repair_path"]
    real_other_nodes = [node for node in real["nodes"] if node["node_id"] != "repair_path"]

    assert fake_repair["nested_subgraph_ids"] == ["fake_context_subgraph"]
    assert "fake_collect" in fake_repair["subgraph_node_ids"]
    assert "fake_guard" in fake_repair["subgraph_node_ids"]
    assert real_repair["nested_subgraph_ids"] == [facade.LG_C2_CONTEXT_SUBGRAPH_ID]
    assert all(node_id in real_repair["subgraph_node_ids"] for node_id in facade.LG_C2_CONTEXT_NODE_IDS)
    assert fake_other_nodes == real_other_nodes
    assert fake["edges"] == real["edges"]


def test_lg_m1_d1_state_module_keeps_ce_lane_graph_state_out_of_foundation() -> None:
    state_path = LANGGRAPH_ROOT / "state.py"
    module = ast.parse(state_path.read_text(encoding="utf-8"), filename=str(state_path))
    class_names = {node.name for node in module.body if isinstance(node, ast.ClassDef)}
    imported_names = {
        alias.name
        for node in ast.walk(module)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }

    assert "CompatState" in class_names
    assert "_GraphLoopState" not in class_names
    assert "_LgE2SendState" not in class_names
    assert "_ValidationSubgraphState" not in class_names
    assert "_WaiverSubgraphState" not in class_names
    assert "_RepairSubgraphState" not in class_names
    assert "_LG_C2_ContextState" not in class_names
    assert "StageContext" not in imported_names
    assert "_RunState" not in imported_names
    assert "Annotated" not in imported_names
