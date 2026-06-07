"""LG-M1-A inventory and characterization baseline tests.

These tests intentionally lock observable contracts only: import surfaces,
collection count, graph registry metadata, no-provider CLI/help surfaces, and
runtime identity fields that downstream LG-M1 sub-PRs must account for.
They must not freeze private helper organization, line counts, or internal file
split decisions that LG-M1-D* is explicitly allowed to change.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
METHOD_ROOT = REPO_ROOT / "project_1_llm_state_machine_modeling" / "method"
TESTS_ROOT = METHOD_ROOT / "tests"
BASELINE_PATH = TESTS_ROOT / "fixtures" / "lg_m1_a_baseline.json"
EXPERIMENT_MODULES = [
    "method.pr_e1_real_runs",
    "method.experiments.real_run_matrix",
    "method.pr_lg_f1_resume_experiment",
    "method.experiments.checkpoint_resume",
    "method.pr_d_representative",
    "method.experiments.representative_cases",
    "method.pr2a_loop",
    "method.experiments.ablation.deterministic_loop",
]
LG_M1_C1_EXPECTED_COLLECTION_DELTA = 5
LG_M1_D1_EXPECTED_COLLECTION_DELTA = 5
LG_M1_B_ADDITIVE_STAGE_MODULES = {
    "method.stages.api",
    "method.stages.sc_control",
    "method.stages.sl_prompt_api",
}
LG_M1_B_ADDITIVE_TEST_COUNT = 7
LG_M1_C2_DELETED_LEGACY_ONLY_TEST_COUNT = 3
LG_M1_C2_ADDITIVE_ABLATION_CONTRACT_TEST_COUNT = 4
LG_M1_C2_EXPECTED_TEST_PR0_NON_LEGACY_CONTRACT_COUNT = 52
LG_M1_C2_EXPECTED_TEST_PR0_LEGACY_DIRECT_COUNT = 0
LG_M1_C2_ALLOWED_ACTIVE_LEGACY_REFERENCES = {
    "project_1_llm_state_machine_modeling/method/loop.py",
    "project_1_llm_state_machine_modeling/method/tests/crosscutting/test_lg_m1_inventory_characterization.py",
}
LG_M1_D2_EXPECTED_COLLECTION_DELTA = 5
LG_M1_D3_EXPECTED_COLLECTION_DELTA = 7
LG_M1_G_EXPECTED_COLLECTION_DELTA = 2
LG_M1_D3_REMOVED_FACADE_IMPORTS = {
    (
        "project_1_llm_state_machine_modeling/method/experiments/checkpoint_resume.py",
        "from_import",
        "run_lg_f1_resume_experiment",
        None,
    )
}
LG_M1_D3_REMOVED_DIRECT_SYMBOLS = {"run_lg_f1_resume_experiment"}

LG_M1_E_TEST_PATH_MIRROR_MAP = {
    "project_1_llm_state_machine_modeling/method/tests/test_gpt_client.py":
        "project_1_llm_state_machine_modeling/method/tests/llm/test_gpt_client.py",
    "project_1_llm_state_machine_modeling/method/tests/test_lg_m1_a_inventory_characterization.py":
        "project_1_llm_state_machine_modeling/method/tests/crosscutting/test_lg_m1_inventory_characterization.py",
    "project_1_llm_state_machine_modeling/method/tests/test_lg_m1_c1_experiments_entrypoints.py":
        "project_1_llm_state_machine_modeling/method/tests/experiments/test_experiments_entrypoints.py",
    "project_1_llm_state_machine_modeling/method/tests/test_lg_m1_d1_langgraph_foundation.py":
        "project_1_llm_state_machine_modeling/method/tests/langgraph/test_foundation.py",
    "project_1_llm_state_machine_modeling/method/tests/test_lg_m1_d2_langgraph_instrumentation.py":
        "project_1_llm_state_machine_modeling/method/tests/langgraph/test_instrumentation.py",
    "project_1_llm_state_machine_modeling/method/tests/test_lg_m1_d3_langgraph_nodes_subgraphs_core.py":
        "project_1_llm_state_machine_modeling/method/tests/langgraph/test_nodes_subgraphs_core.py",
    "project_1_llm_state_machine_modeling/method/tests/test_pr0_stage_contract.py":
        "project_1_llm_state_machine_modeling/method/tests/stages/test_stage_contract.py",
    "project_1_llm_state_machine_modeling/method/tests/test_pr1a_sd_tools.py":
        "project_1_llm_state_machine_modeling/method/tests/stages/test_sd_tools.py",
    "project_1_llm_state_machine_modeling/method/tests/test_pr1b_sl_prompt_generators.py":
        "project_1_llm_state_machine_modeling/method/tests/stages/test_sl_prompt_generators.py",
    "project_1_llm_state_machine_modeling/method/tests/test_pr2a_deterministic_loop.py":
        "project_1_llm_state_machine_modeling/method/tests/experiments/ablation/test_deterministic_loop.py",
    "project_1_llm_state_machine_modeling/method/tests/test_pr2b_llm_review_integration.py":
        "project_1_llm_state_machine_modeling/method/tests/llm/test_llm_review_integration.py",
    "project_1_llm_state_machine_modeling/method/tests/test_pr3_handoff_smoke.py":
        "project_1_llm_state_machine_modeling/method/tests/handoff_smoke/test_handoff_smoke.py",
    "project_1_llm_state_machine_modeling/method/tests/test_pr_b1_deterministic_runtime.py":
        "project_1_llm_state_machine_modeling/method/tests/crosscutting/test_full_staged_runtime_contract.py",
    "project_1_llm_state_machine_modeling/method/tests/test_pr_b2_llm_stage_adapters.py":
        "project_1_llm_state_machine_modeling/method/tests/llm/test_llm_stage_adapters.py",
    "project_1_llm_state_machine_modeling/method/tests/test_pr_c_default_entry.py":
        "project_1_llm_state_machine_modeling/method/tests/crosscutting/test_default_agent_loop_entry.py",
    "project_1_llm_state_machine_modeling/method/tests/test_pr_d_representative.py":
        "project_1_llm_state_machine_modeling/method/tests/experiments/test_representative_cases.py",
    "project_1_llm_state_machine_modeling/method/tests/test_pr_e1_real_runs.py":
        "project_1_llm_state_machine_modeling/method/tests/experiments/test_real_run_matrix.py",
    "project_1_llm_state_machine_modeling/method/tests/test_pr_e1_scenario_normalization.py":
        "project_1_llm_state_machine_modeling/method/tests/experiments/test_scenario_normalization.py",
    "project_1_llm_state_machine_modeling/method/tests/test_pr_langgraph_runtime.py":
        "project_1_llm_state_machine_modeling/method/tests/langgraph/test_runtime_contract.py",
    "project_1_llm_state_machine_modeling/method/tests/test_pr_lg_f1_resume_experiment.py":
        "project_1_llm_state_machine_modeling/method/tests/experiments/test_checkpoint_resume.py",
}


def _lg_m1_e_mirror_path(path: str) -> str:
    return LG_M1_E_TEST_PATH_MIRROR_MAP.get(path, path)


def _load_baseline() -> dict[str, Any]:
    return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))


def _sha256_json(payload: object) -> str:
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(data.encode("utf-8")).hexdigest()


def _python_env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = "project_1_llm_state_machine_modeling"
    return env


def _scan_langgraph_facade_consumers() -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    alias_attrs: list[dict[str, str]] = []
    for path in sorted(METHOD_ROOT.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        rel = str(path.relative_to(REPO_ROOT))
        module = ast.parse(path.read_text(encoding="utf-8"))
        alias_names: set[str] = set()
        for node in ast.walk(module):
            if isinstance(node, ast.ImportFrom) and node.module == "method.langgraph_runtime":
                for alias in node.names:
                    entries.append({"module_path": rel, "kind": "from_import", "symbol": alias.name, "asname": alias.asname})
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "method.langgraph_runtime":
                        alias_names.add(alias.asname or "langgraph_runtime")
                        entries.append({"module_path": rel, "kind": "module_import", "symbol": alias.name, "asname": alias.asname})
            elif isinstance(node, ast.ImportFrom) and node.module == "method":
                for alias in node.names:
                    if alias.name == "langgraph_runtime":
                        alias_names.add(alias.asname or alias.name)
                        entries.append({"module_path": rel, "kind": "method_reexport_import", "symbol": alias.name, "asname": alias.asname})
        for node in ast.walk(module):
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id in alias_names:
                alias_attrs.append({"module_path": rel, "alias": node.value.id, "attribute": node.attr})
    return {
        "entry_count": len(entries),
        "alias_attribute_count": len(alias_attrs),
        "direct_symbols": sorted({entry["symbol"] for entry in entries if entry["kind"] == "from_import"}),
        "reexporter_paths_checked": [
            str((METHOD_ROOT / "__init__.py").relative_to(REPO_ROOT)),
            str((METHOD_ROOT / "loop.py").relative_to(REPO_ROOT)),
            str((METHOD_ROOT / "staged_runtime.py").relative_to(REPO_ROOT)),
        ],
        "entries": sorted(entries, key=lambda item: (item["module_path"], item["kind"], item["symbol"])),
        "alias_attributes": sorted(alias_attrs, key=lambda item: (item["module_path"], item["alias"], item["attribute"])),
    }


def _scan_stage_api() -> dict[str, Any]:
    modules: list[dict[str, Any]] = []
    for path in sorted((METHOD_ROOT / "stages").glob("*.py")):
        if path.name == "__init__.py":
            continue
        module = ast.parse(path.read_text(encoding="utf-8"))
        funcs = [node.name for node in module.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_")]
        classes = [node.name for node in module.body if isinstance(node, ast.ClassDef) and not node.name.startswith("_")]
        constants: list[str] = []
        for node in module.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and (target.id.isupper() or target.id.endswith("_ID")) and not target.id.startswith("_"):
                        constants.append(target.id)
        modules.append({
            "module": f"method.stages.{path.stem}",
            "path": str(path.relative_to(REPO_ROOT)),
            "functions": funcs,
            "classes": classes,
            "constants": constants,
        })
    return {"module_count": len(modules), "modules": modules}


def _scan_legacy_contract_tests() -> dict[str, Any]:
    path = TESTS_ROOT / "stages" / "test_stage_contract.py"
    module = ast.parse(path.read_text(encoding="utf-8"))
    tests: list[dict[str, Any]] = []
    for node in module.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            legacy_direct = False
            for child in ast.walk(node):
                if isinstance(child, ast.Name) and child.id == "legacy_loop":
                    legacy_direct = True
                elif isinstance(child, ast.Attribute) and isinstance(child.value, ast.Name) and child.value.id == "legacy_loop":
                    legacy_direct = True
            tests.append({"name": node.name, "lineno": node.lineno, "legacy_loop_direct": legacy_direct})
    active_import_paths: list[str] = []
    for py_file in sorted(METHOD_ROOT.rglob("*.py")):
        if "__pycache__" in py_file.parts or py_file.name == "legacy_loop.py":
            continue
        text = py_file.read_text(encoding="utf-8")
        if "method.legacy_loop" in text or "legacy_loop" in text:
            active_import_paths.append(str(py_file.relative_to(REPO_ROOT)))
    return {
        "active_import_paths": active_import_paths,
        "test_pr0_stage_contract": {
            "path": str(path.relative_to(REPO_ROOT)),
            "test_count": len(tests),
            "legacy_loop_direct_count": sum(1 for row in tests if row["legacy_loop_direct"]),
            "non_legacy_contract_count": sum(1 for row in tests if not row["legacy_loop_direct"]),
            "tests": tests,
        },
    }


def _stable_graph_contract() -> dict[str, Any]:
    from method.langgraph_runtime import build_langgraph_node_registry, graph_registry_consistency
    from method.loop import build_planned_stage_graph
    from method.schema import LoopConfig

    planned = build_planned_stage_graph(LoopConfig())
    registry = build_langgraph_node_registry()
    consistency = graph_registry_consistency(planned, registry)
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
    planned_stage_order = [node.get("stage_id") for node in planned.get("nodes", [])]
    canonical_input = {"registry": stable_registry, "planned_stage_order": planned_stage_order, "consistency": consistency}
    return {
        "registry": stable_registry,
        "planned_stage_order": planned_stage_order,
        "consistency": consistency,
        "canonical_hash": _sha256_json(canonical_input),
        "hash_excludes": ["timestamps", "absolute temporary paths", "dict insertion ordering", "raw provider output", "secrets"],
    }


def test_lg_m1_a_baseline_fixture_is_structured_and_secret_free() -> None:
    baseline = _load_baseline()

    assert baseline["schema_version"] == "lg_m1_a_baseline_v1"
    assert baseline["baseline_scope"].startswith("LG-M1-A inventory")
    assert baseline["captured_commit"]
    assert baseline["artifact_policy"] == {
        "contains_raw_model_text": False,
        "contains_raw_provider_output": False,
        "contains_secret": False,
        "fixture_is_programmatic_baseline_source": True,
    }
    serialized = BASELINE_PATH.read_text(encoding="utf-8").lower()
    assert "llm_api_key" not in serialized
    assert "bearer " not in serialized
    assert "sk-" not in serialized


def test_lg_m1_a_facade_stage_and_legacy_inventory_match_current_observable_surface() -> None:
    baseline = _load_baseline()

    current_facade = _scan_langgraph_facade_consumers()
    fixture_facade = baseline["facade_reexport_scan"]
    current_entries = {
        (_lg_m1_e_mirror_path(entry["module_path"]), entry["kind"], entry["symbol"], entry.get("asname"))
        for entry in current_facade["entries"]
    }
    fixture_entries = {
        (_lg_m1_e_mirror_path(entry["module_path"]), entry["kind"], entry["symbol"], entry.get("asname"))
        for entry in fixture_facade["entries"]
    }
    assert fixture_entries - current_entries == LG_M1_D3_REMOVED_FACADE_IMPORTS
    assert current_entries - fixture_entries == set()
    assert current_facade["entry_count"] + len(LG_M1_D3_REMOVED_FACADE_IMPORTS) == fixture_facade["entry_count"]
    assert current_facade["alias_attribute_count"] == fixture_facade["alias_attribute_count"]
    assert set(fixture_facade["direct_symbols"]) - set(current_facade["direct_symbols"]) == LG_M1_D3_REMOVED_DIRECT_SYMBOLS
    assert set(current_facade["direct_symbols"]) - set(fixture_facade["direct_symbols"]) == set()
    assert set(current_facade["reexporter_paths_checked"]) == set(fixture_facade["reexporter_paths_checked"])
    assert "project_1_llm_state_machine_modeling/method/loop.py" in current_facade["reexporter_paths_checked"]

    current_stage = _scan_stage_api()
    fixture_stage = baseline["stage_api_scan"]
    baseline_modules = fixture_stage["modules"]
    additive_modules = [row for row in current_stage["modules"] if row["module"] in LG_M1_B_ADDITIVE_STAGE_MODULES]
    non_additive_modules = [row for row in current_stage["modules"] if row["module"] not in LG_M1_B_ADDITIVE_STAGE_MODULES]
    assert current_stage["module_count"] == fixture_stage["module_count"] + len(LG_M1_B_ADDITIVE_STAGE_MODULES)
    assert non_additive_modules == baseline_modules
    assert {row["module"] for row in additive_modules} == LG_M1_B_ADDITIVE_STAGE_MODULES
    assert any("run_sd2_parse" in module["functions"] for module in current_stage["modules"])

    current_legacy = _scan_legacy_contract_tests()
    # LG-M1-C2 is the approved cleanup point for the old A0-A4 legacy loop.
    # It removes three legacy-only full-loop tests and rewrites the remaining
    # legacy-direct contract checks into function-named helpers, so the PR-0
    # contract test file becomes fully non-legacy while preserving/auditing the
    # useful cascade and trace/schema contracts.
    assert set(current_legacy["active_import_paths"]) <= LG_M1_C2_ALLOWED_ACTIVE_LEGACY_REFERENCES
    assert current_legacy["test_pr0_stage_contract"]["legacy_loop_direct_count"] == LG_M1_C2_EXPECTED_TEST_PR0_LEGACY_DIRECT_COUNT
    assert current_legacy["test_pr0_stage_contract"]["non_legacy_contract_count"] == LG_M1_C2_EXPECTED_TEST_PR0_NON_LEGACY_CONTRACT_COUNT
    assert current_legacy["test_pr0_stage_contract"]["test_count"] == LG_M1_C2_EXPECTED_TEST_PR0_NON_LEGACY_CONTRACT_COUNT


def test_lg_m1_a_graph_contract_and_runtime_identity_are_stable_without_provider() -> None:
    baseline = _load_baseline()
    graph = _stable_graph_contract()

    assert graph["canonical_hash"] == baseline["graph_contract"]["canonical_hash"]
    assert graph["consistency"]["ok"] is True
    assert graph["registry"]["runtime_backend"] == "langgraph"
    assert graph["registry"]["opaque_wrapper"] is False
    assert graph["registry"]["delegated_monolithic_runtime"] is False
    assert graph["planned_stage_order"] == graph["registry"]["canonical_stage_sequence"]
    assert "timestamps" in baseline["graph_contract"]["hash_excludes"]

    runtime = baseline["runtime_identity"]
    assert runtime["source"]["type"] == "committed_historical_agent_loop_record_gzip"
    assert Path(runtime["source"]["path"]).exists()
    assert runtime["source"]["record_status"] == "success"
    assert runtime["environment"]["runner"] == "method.langgraph_runtime.run_full_staged_langgraph_runtime"
    assert runtime["environment"]["loop_entrypoint"] == "method.loop.run_agent_loop"
    assert runtime["environment"]["graph_runtime_backend"] == "langgraph"
    assert runtime["environment"]["graph_runtime_id"] == "langgraph:pr-langgraph.stategraph.v1"
    assert runtime["environment"]["node_edge_schema_version"] == "pr-langgraph.stage-nodes.v1"
    assert runtime["run_config"]["runtime_implementation"] == "method.langgraph_runtime.run_full_staged_langgraph_runtime"
    assert runtime["run_config"]["canonical_runtime_backend"] == "langgraph"
    assert runtime["run_config"]["graph_node_registry"]["opaque_wrapper"] is False
    assert runtime["run_config"]["graph_node_registry"]["delegated_monolithic_runtime"] is False


def test_lg_m1_a_experiment_cli_baseline_is_import_or_help_only() -> None:
    baseline = _load_baseline()
    rows = baseline["experiment_cli_import_baseline"]["modules"]
    fixture_modules = [row["module"] for row in rows]
    assert fixture_modules == EXPERIMENT_MODULES[:-1]
    rows = [
        *rows,
        {
            "module": "method.experiments.ablation.deterministic_loop",
            "import_exit_code": 0,
            "help_exit_code": 0,
            "help_usage_first_line": "",
            "provider_invocation": False,
        },
    ]

    for row in rows:
        import_proc = subprocess.run(
            [sys.executable, "-c", f"import {row['module']}; print({row['module']}.__name__)"],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=_python_env(),
            check=False,
        )
        help_proc = subprocess.run(
            [sys.executable, "-m", row["module"], "--help"],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=_python_env(),
            check=False,
        )
        assert import_proc.returncode == row["import_exit_code"] == 0
        assert help_proc.returncode == row["help_exit_code"] == 0
        assert row["provider_invocation"] is False
        first_line = (help_proc.stdout.splitlines() or [""])[0]
        assert first_line == row["help_usage_first_line"]


def test_lg_m1_a_pytest_collection_baseline_plus_registered_c1_d1_and_b_deltas_is_current() -> None:
    baseline = _load_baseline()
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "project_1_llm_state_machine_modeling/method/tests"],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=_python_env(),
        check=True,
    )
    match = re.search(r"(\d+) tests? collected", proc.stdout + proc.stderr)
    assert match, proc.stdout + proc.stderr
    # LG-M1-A captured the pre-maintenance collection count. C1, D1, B, and D2
    # register exact additive deltas. C2 is the approved cleanup point that
    # legally removes three old full-loop legacy-only tests, adds one explicit
    # old/new ablation path equivalence test, two non-legacy evidence
    # preservation tests, and one LG-C2 redaction false-positive regression test.
    # It also rewrites the remaining legacy-direct contracts into non-legacy
    # helper/schema tests.
    deltas = baseline["collection"]["expected_deltas"]
    assert deltas["lg_m1_c1_experiments_entrypoints"]["count"] == LG_M1_C1_EXPECTED_COLLECTION_DELTA
    assert deltas["lg_m1_d1_langgraph_foundation"]["count"] == LG_M1_D1_EXPECTED_COLLECTION_DELTA
    assert deltas["lg_m1_d2_langgraph_instrumentation"]["count"] == LG_M1_D2_EXPECTED_COLLECTION_DELTA
    assert deltas["lg_m1_d3_langgraph_nodes_subgraphs_core"]["count"] == LG_M1_D3_EXPECTED_COLLECTION_DELTA
    assert deltas["lg_m1_g_final_integration_stabilization"]["count"] == LG_M1_G_EXPECTED_COLLECTION_DELTA
    expected_c1_d1_count = (
        baseline["collection"]["count"]
        + LG_M1_C1_EXPECTED_COLLECTION_DELTA
        + LG_M1_D1_EXPECTED_COLLECTION_DELTA
    )
    assert expected_c1_d1_count == baseline["collection"]["current_expected_count_after_c1_and_d1"]
    expected_d2_count = (
        expected_c1_d1_count
        + LG_M1_B_ADDITIVE_TEST_COUNT
        + LG_M1_D2_EXPECTED_COLLECTION_DELTA
    )
    assert expected_d2_count == baseline["collection"]["current_expected_count_after_c1_d1_b_and_d2"]
    expected_c2_count = (
        expected_d2_count
        - LG_M1_C2_DELETED_LEGACY_ONLY_TEST_COUNT
        + LG_M1_C2_ADDITIVE_ABLATION_CONTRACT_TEST_COUNT
    )
    assert expected_c2_count == baseline["collection"]["current_expected_count_after_c1_d1_b_d2_and_c2"]
    expected_d3_count = expected_c2_count + LG_M1_D3_EXPECTED_COLLECTION_DELTA
    assert expected_d3_count == baseline["collection"]["current_expected_count_after_c1_d1_b_d2_c2_and_d3"]
    expected_count = expected_d3_count + LG_M1_G_EXPECTED_COLLECTION_DELTA
    assert expected_count == baseline["collection"]["current_expected_count_after_c1_d1_b_d2_c2_d3_and_g"]
    assert int(match.group(1)) == expected_count
