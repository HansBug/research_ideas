"""LG-M1-D2 LangGraph instrumentation split characterization tests.

These tests lock D2's no-semantic-change gates: the compatibility facade stays
usable, moved class/TypedDict objects keep identity, instrumentation submodules
never reverse-import ``method.langgraph_runtime``, LG-C1 helpers stay out of the
D2 package, and historical evidence files are read-only inputs rather than
rewritten fixtures.
"""

from __future__ import annotations

import ast
import gzip
import hashlib
import importlib
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
METHOD_ROOT = REPO_ROOT / "project_1_llm_state_machine_modeling" / "method"
LANGGRAPH_ROOT = METHOD_ROOT / "langgraph"
HISTORICAL_RECORD = (
    REPO_ROOT
    / "runs"
    / "pr_langgraph_real_agent_loop_round2_stategraph_fix"
    / "pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4"
    / "pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4.agent_loop.json.gz"
)

MOVED_SYMBOLS: dict[str, list[str]] = {
    "method.langgraph.checkpointing": [
        "_PickleCheckpointSerde",
        "_checkpoint_resume_smoke",
    ],
    "method.langgraph.instrumentation.operator_stream": [
        "LG_D1_OPERATOR_EVENT_SCHEMA_VERSION",
        "LG_D1_STREAM_SUMMARY_SCHEMA_VERSION",
        "LG_D1_INSTRUMENTATION_LAYER",
        "build_lg_d1_operator_event",
        "lg_d1_llm_stream_runtime_metadata",
        "reconstruct_lg_d1_stream_summary_from_jsonl",
        "_append_lg_d1_operator_event",
        "_write_lg_d1_operator_artifacts",
        "_run_graph_with_lg_d1_stream",
    ],
    "method.langgraph.instrumentation.trace_export": [
        "LG_G1_TRACE_EXPORT_SCHEMA_VERSION",
        "LG_G1_TRACE_EXPORT_INSTRUMENTATION_LAYER",
        "_lg_g1_trace_export_policy",
        "_lg_g1_safe_trace_payload",
        "_augment_run_record_with_lg_g1_trace_export",
    ],
    "method.langgraph.instrumentation.tool_wrappers": [
        "LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION",
        "LG_E3_TOOLNODE_WRAPPER_INSTRUMENTATION_LAYER",
        "build_lg_e3_toolnode_wrapper_registry",
        "_safe_lg_e3_tool_summary",
        "_lg_e3_fixed_tool_call",
        "_augment_run_record_with_lg_e3_toolnode_trace",
    ],
    "method.langgraph.instrumentation.retry_timeout": [
        "LG_D2_LLM_NODE_ENVELOPE_SCHEMA_VERSION",
        "LG_D2_LLM_NODE_ENVELOPE_EVENT_SCHEMA_VERSION",
        "LG_D2_LLM_NODE_ENVELOPE_INSTRUMENTATION_LAYER",
        "LG_D2_LLM_NODE_ENVELOPE_EVENT_TYPES",
        "build_lg_d2_llm_node_envelope_policy",
        "_lg_d2_envelope_event",
        "_lg_d2_error_kind_from_exception",
        "_lg_d2_operator_events_from_flow_logs",
        "_lg_d2_wrap_llm_stage_node",
    ],
    "method.langgraph.instrumentation.send_parallel": [
        "LG_E2_SEND_PARALLEL_SCHEMA_VERSION",
        "LG_E2_SEND_PARALLEL_INSTRUMENTATION_LAYER",
        "_LgE2SendState",
        "build_lg_e2_send_parallel_contract",
        "_lg_e2_canonicalize_worker_results",
        "_lg_e2_metadata_for_feedback",
        "_lg_e2_selected_feedback_digest",
        "_lg_e2_run_sd6_send_parallel_or_serial",
        "_augment_run_record_with_lg_e2_send_parallel_trace",
    ],
    "method.langgraph.instrumentation.store": [
        "langgraph_store_compat_smoke",
        "_transient_namespace",
        "_put_transient",
        "_get_transient",
        "_drop_transient",
        "_drain_transients",
    ],
    "method.langgraph.subgraphs.context_engineering": [
        "LG_C2_CONTEXT_SUBGRAPH_SCHEMA_VERSION",
        "LG_C2_CONTEXT_SUBGRAPH_ID",
        "LG_C2_CONTEXT_NODE_IDS",
        "LG_C2_CANONICAL_RECORD_FIELD",
        "_LG_C2_ContextState",
        "LG_C2_ContextRedactionBlocked",
        "LG_C2_ContextAssemblyResult",
        "build_lg_c2_context_subgraph_contract",
        "assemble_lg_c2_prompt_context",
    ],
}

IDENTITY_SYMBOLS = {
    ("method.langgraph.checkpointing", "_PickleCheckpointSerde"),
    ("method.langgraph.instrumentation.send_parallel", "_LgE2SendState"),
    ("method.langgraph.subgraphs.context_engineering", "_LG_C2_ContextState"),
    ("method.langgraph.subgraphs.context_engineering", "LG_C2_ContextRedactionBlocked"),
    ("method.langgraph.subgraphs.context_engineering", "LG_C2_ContextAssemblyResult"),
}

POSTPONED_F1_SYMBOLS = {
    "resume_lg_f1_from_checkpoint",
    "run_lg_f1_resume_experiment",
    "_lg_f1_checkpoint_id_hash",
}


def _sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _load_historical_record() -> dict[str, Any]:
    with gzip.open(HISTORICAL_RECORD, "rt", encoding="utf-8") as f:
        return json.load(f)


def _stable_historical_summary(record: dict[str, Any]) -> dict[str, Any]:
    final_artifacts = record.get("final_artifacts") if isinstance(record.get("final_artifacts"), dict) else {}
    environment = record.get("environment") if isinstance(record.get("environment"), dict) else {}
    run_config = record.get("run_config") if isinstance(record.get("run_config"), dict) else {}
    return {
        "environment.runner": environment.get("runner"),
        "environment.loop_entrypoint": environment.get("loop_entrypoint"),
        "environment.graph_runtime_backend": environment.get("graph_runtime_backend"),
        "run_config.runtime_implementation": run_config.get("runtime_implementation"),
        "run_config.canonical_runtime_backend": run_config.get("canonical_runtime_backend"),
        "record.status": record.get("status"),
        "final_artifacts.verdict": final_artifacts.get("verdict"),
        "final_artifacts.agent_loop_result_status": final_artifacts.get("agent_loop_result_status"),
        "final_artifacts.main_result_eligible": final_artifacts.get("main_result_eligible"),
        "stage_record_count": len(record.get("stage_records") or []),
        "llm_interaction_count": len(record.get("llm_interactions") or []),
        "fix_log_count": len(record.get("fix_log") or []),
        "operator_log_present": isinstance(final_artifacts.get("operator_log"), dict),
        "stream_summary_hash": (final_artifacts.get("operator_log") or {}).get("stream_summary_payload_hash")
        if isinstance(final_artifacts.get("operator_log"), dict)
        else None,
    }


def test_lg_m1_d2_modules_do_not_reverse_import_runtime_facade_or_c1_helpers() -> None:
    forbidden_imports: list[str] = []
    c1_leaks: list[str] = []
    checked = sorted(path for path in LANGGRAPH_ROOT.rglob("*.py") if "__pycache__" not in path.parts)
    assert checked
    for path in checked:
        rel = str(path.relative_to(REPO_ROOT))
        source = path.read_text(encoding="utf-8")
        module = ast.parse(source, filename=str(path))
        for node in ast.walk(module):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "method.langgraph_runtime":
                        forbidden_imports.append(f"{rel} imports {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                if node.module == "method.langgraph_runtime":
                    forbidden_imports.append(f"{rel} imports from method.langgraph_runtime")
                if node.module == "method" and any(alias.name == "langgraph_runtime" for alias in node.names):
                    forbidden_imports.append(f"{rel} imports method.langgraph_runtime via method re-export")
        if "_lg_c1_" in source and rel != "project_1_llm_state_machine_modeling/method/langgraph/core.py":
            c1_leaks.append(rel)
    assert forbidden_imports == []
    assert c1_leaks == []


def test_lg_m1_d2_facade_reexports_moved_symbols_with_identity_for_stateful_objects() -> None:
    facade = importlib.import_module("method.langgraph_runtime")
    for module_name, symbols in MOVED_SYMBOLS.items():
        module = importlib.import_module(module_name)
        for symbol in symbols:
            assert hasattr(module, symbol), f"{module_name}.{symbol} missing"
            assert hasattr(facade, symbol), f"facade missing {symbol}"
            moved = getattr(module, symbol)
            exported = getattr(facade, symbol)
            if (module_name, symbol) in IDENTITY_SYMBOLS or callable(moved):
                assert exported is moved, f"facade must re-export the exact object for {module_name}.{symbol}"
            else:
                assert exported == moved


def test_lg_m1_d2_f1_resume_entrypoints_are_postponed_in_facade() -> None:
    facade = importlib.import_module("method.langgraph_runtime")
    checkpointing = importlib.import_module("method.langgraph.checkpointing")
    for symbol in POSTPONED_F1_SYMBOLS:
        assert hasattr(facade, symbol)
        assert not hasattr(checkpointing, symbol), f"{symbol} is F1/runtime orchestration and must not move in D2"
    assert facade.run_lg_f1_resume_experiment.__module__ == "method.langgraph_runtime"


def test_lg_m1_d2_runtime_identity_and_graph_registry_facade_stay_stable() -> None:
    facade = importlib.import_module("method.langgraph_runtime")
    assert facade.run_full_staged_langgraph_runtime.__module__ == "method.langgraph_runtime"
    assert facade.graph_registry_consistency.__module__ == "method.langgraph_runtime"
    assert facade.build_langgraph_node_registry()["runtime_backend"] == "langgraph"


def test_lg_m1_d2_historical_evidence_read_only_drift_gate() -> None:
    before_hash = _sha256(HISTORICAL_RECORD)
    before_mtime = HISTORICAL_RECORD.stat().st_mtime_ns
    record = _load_historical_record()
    summary = _stable_historical_summary(record)

    assert summary == {
        "environment.runner": "method.langgraph_runtime.run_full_staged_langgraph_runtime",
        "environment.loop_entrypoint": "method.loop.run_agent_loop",
        "environment.graph_runtime_backend": "langgraph",
        "run_config.runtime_implementation": "method.langgraph_runtime.run_full_staged_langgraph_runtime",
        "run_config.canonical_runtime_backend": "langgraph",
        "record.status": "success",
        "final_artifacts.verdict": "success",
        "final_artifacts.agent_loop_result_status": "converged",
        "final_artifacts.main_result_eligible": True,
        "stage_record_count": 12,
        "llm_interaction_count": 3,
        "fix_log_count": 0,
        "operator_log_present": False,
        "stream_summary_hash": None,
    }
    # Re-read after extracting the deterministic summary so this gate also
    # proves the committed historical run record was not mutated by the test.
    assert _sha256(HISTORICAL_RECORD) == before_hash
    assert HISTORICAL_RECORD.stat().st_mtime_ns == before_mtime
