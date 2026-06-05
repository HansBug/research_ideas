from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any

from method import loop
from method.run_record import read_agent_loop_run_record
from method.schema import (
    DesignDiagnosticItem,
    DesignFeedback,
    LoopConfig,
    ModelReviewFeedback,
    ParseFeedback,
    RepairRejection,
    RepairReviewFeedback,
    SemanticFeedback,
    SimFeedback,
    StageContext,
    StageResultMeta,
    TestScenario,
)
from method.staged_runtime import (
    FullStagedRuntimeAdapters,
    _LLMRetryExhausted,
    RepairRequest,
    ScenarioGenerationRequest,
)
from method.stages.ids import STAGE_SPECS_BY_ID, StageId, StageStatus


def _meta(stage_id: StageId, *, ok: bool = True, status: StageStatus | None = None) -> StageResultMeta:
    spec = STAGE_SPECS_BY_ID[stage_id.value]
    return StageResultMeta(
        stage_id=stage_id.value,
        stage_kind=spec.kind,
        enabled=True,
        ran=True,
        status=status or (StageStatus.OK if ok else StageStatus.FAIL),
        ok=ok,
    )


def _stable_dsl() -> str:
    return """
state Root {
    state Idle;
    [*] -> Idle;
    Idle -> [*];
}
"""


def _ok_parse(_dsl: str, _context: StageContext) -> tuple[ParseFeedback, StageResultMeta]:
    return ParseFeedback(ok=True), _meta(StageId.SD_2_PARSE)


def _ok_semantic(_dsl: str, _context: StageContext) -> tuple[SemanticFeedback, StageResultMeta]:
    return SemanticFeedback(ok=True), _meta(StageId.SD_3_SEMANTIC)


def _ok_design(_context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
    return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)


def _ok_coverage(_dsl: str, scenarios: list[TestScenario]) -> tuple[dict[str, Any], StageResultMeta]:
    return {"coverage_report": {"ok": True, "n_scenarios": len(scenarios)}, "coverage_gap": False}, _meta(
        StageId.SD_5A_SCENARIO_COVERAGE
    )


def _ok_sim(_dsl: str, scenarios_or_set: Any, _context: StageContext) -> tuple[SimFeedback, StageResultMeta]:
    n = len(getattr(scenarios_or_set, "scenarios", []) or [])
    return SimFeedback(ok=True, n_scenarios=n, n_scenarios_passed=n), _meta(StageId.SD_6_SIM)


def _ok_model_review(_dsl: str, _context: StageContext, _feedback: dict[str, Any]) -> tuple[ModelReviewFeedback, StageResultMeta]:
    return ModelReviewFeedback(ok=True, decision="pass", risk_level="none"), _meta(StageId.SL_7_MODEL_REVIEW)


def _ok_repair_review(_request: RepairRequest) -> tuple[RepairReviewFeedback, StageResultMeta]:
    return RepairReviewFeedback(ok=True, target_resolved=True, drift_risk="none"), _meta(StageId.SD_10_REPAIR_REVIEW)


def _scenario_generate(_request: ScenarioGenerationRequest) -> list[TestScenario]:
    return [TestScenario(name="empty_smoke", steps=[])]


def _adapters() -> FullStagedRuntimeAdapters:
    return FullStagedRuntimeAdapters(
        parse=_ok_parse,
        semantic=_ok_semantic,
        design=_ok_design,
        scenario_generate=_scenario_generate,
        scenario_coverage=_ok_coverage,
        sim=_ok_sim,
        model_review=_ok_model_review,
        repair=lambda _request: _stable_dsl(),
        repair_review=_ok_repair_review,
    )


def test_langgraph_compat_smoke_exposes_versions_and_stategraph() -> None:
    from method.langgraph_runtime import langgraph_compat_smoke

    smoke = langgraph_compat_smoke()

    assert smoke["ok"] is True
    assert smoke["stategraph_compile_ok"] is True
    assert smoke["invoke_ok"] is True
    assert smoke["stream_ok"] is True
    assert smoke["checkpoint_smoke_ok"] is True
    assert smoke["langgraph_version"] != "unknown"


def test_langgraph_node_registry_is_not_opaque_and_matches_planned_graph() -> None:
    from method.langgraph_runtime import build_langgraph_node_registry, graph_registry_consistency

    planned = loop.build_planned_stage_graph(LoopConfig())
    registry = build_langgraph_node_registry()
    consistency = graph_registry_consistency(planned, registry)

    node_ids = {node["node_id"] for node in registry["nodes"]}
    assert len(registry["nodes"]) >= 9
    assert {
        "sc0_start",
        "sl1_initial_modeling",
        "iteration_gate",
        "validation_pass",
        "validation_decision",
        "repair_path",
        "repair_decision",
        "waiver_continue",
        "sc12_budget_exhausted",
        "sc13_trace_audit",
    }.issubset(node_ids)
    assert registry["delegated_monolithic_runtime"] is False
    validation_node = next(node for node in registry["nodes"] if node["node_id"] == "validation_pass")
    assert validation_node["delegated_subgraph"] is True
    assert validation_node["subgraph_id"] == "validation_subgraph"
    assert {
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
    }.issubset(set(validation_node["subgraph_node_ids"]))
    waiver_node = next(node for node in registry["nodes"] if node["node_id"] == "waiver_continue")
    assert waiver_node["delegated_subgraph"] is True
    assert waiver_node["subgraph_id"] == "validation_subgraph"
    assert all(not node.get("delegated_subgraph") for node in registry["nodes"] if node["node_id"] not in {"validation_pass", "waiver_continue"})
    assert consistency["ok"] is True
    assert consistency["missing_stage_ids"] == []
    assert consistency["opaque_wrapper"] is False
    assert consistency["delegated_monolithic_runtime"] is False
    assert StageId.SC_12_EXIT.value in consistency["duplicate_stage_ids"]
    assert consistency["duplicate_stage_id_nodes"][StageId.SC_12_EXIT.value]


def test_langgraph_stategraph_writes_metadata_and_preserves_run_record(tmp_path: Path) -> None:
    from method.langgraph_runtime import run_full_staged_langgraph_runtime

    result = run_full_staged_langgraph_runtime(
        "LangGraph StateGraph should preserve canonical evidence.",
        config=LoopConfig(
            condition_id="langgraph_stategraph_mock",
            condition_family="test_profile",
            base_condition_id="full_staged_v1",
            changed_factors=["llm_provider_mode=mock"],
            llm_provider_mode="mock",
            academic_question="test-only LangGraph StateGraph contract; excluded from main results",
            output_dir=str(tmp_path),
            run_id="pr-langgraph-stategraph-smoke",
            max_iterations=1,
            compatibility_mode="langgraph_stategraph",
        ),
        initial_dsl=_stable_dsl(),
        adapters=_adapters(),
    )

    assert result.status == "converged"
    assert result.run_record_path
    record = read_agent_loop_run_record(result.run_record_path)
    env = record.environment
    assert env["graph_runtime_backend"] == "langgraph"
    assert env["graph_runtime_status"] == "enabled"
    assert env["instrumentation_layer"] == "langgraph"
    assert env["stage_semantics_module"] == "method.staged_runtime"
    assert "delegated_stage_semantics_runner" not in env
    assert env["langgraph_version"] != "unknown"
    assert env["graph_runtime_id"].startswith("langgraph:")
    assert env["graph_config_hash"].startswith("sha256:")
    assert env["node_edge_schema_version"]
    assert env["checkpoint_backend"] == "memory"
    assert env["checkpoint_serde"] == "pickle"
    assert env["resumed_from_checkpoint"] is False
    assert env["checkpoint_resume_smoke"]["scope"] == "toy_ledger_langgraph_api_smoke"
    assert env["checkpoint_resume_smoke"]["real_agent_loop_resume_supported"] is False
    assert env["checkpoint_resume_smoke"]["fix_log_append_only"] is True
    assert env["checkpoint_resume_smoke"]["final_fix_log_count"] == 3
    assert record.run_config["runtime_implementation"] == "method.langgraph_runtime.run_full_staged_langgraph_runtime"
    assert record.run_config["stage_semantics_module"] == "method.staged_runtime"
    assert record.run_config["graph_node_registry"]["opaque_wrapper"] is False
    assert record.run_config["graph_node_registry"]["delegated_monolithic_runtime"] is False
    assert record.final_artifacts["main_result_eligible"] is False


def test_graph_config_hash_changes_with_run_config(tmp_path: Path) -> None:
    from method.langgraph_runtime import run_full_staged_langgraph_runtime

    def run_with(max_iterations: int, run_id: str) -> str:
        result = run_full_staged_langgraph_runtime(
            "Graph config hash should bind run policy, not only node registry.",
            config=LoopConfig(
                condition_id=f"langgraph_hash_mock_{max_iterations}",
                condition_family="test_profile",
                base_condition_id="full_staged_v1",
                changed_factors=["llm_provider_mode=mock", f"max_iterations={max_iterations}"],
                llm_provider_mode="mock",
                academic_question="test-only graph_config_hash sensitivity",
                output_dir=str(tmp_path),
                run_id=run_id,
                max_iterations=max_iterations,
                compatibility_mode="langgraph_stategraph",
            ),
            initial_dsl=_stable_dsl(),
            adapters=_adapters(),
        )
        record = read_agent_loop_run_record(result.run_record_path or "")
        assert record.environment["graph_config_hash"] == record.run_config["graph_config_hash"]
        return str(record.environment["graph_config_hash"])

    assert run_with(1, "pr-langgraph-hash-maxiter-1") != run_with(2, "pr-langgraph-hash-maxiter-2")


def test_loop_config_has_no_runtime_backend_option_and_default_entry_is_langgraph(tmp_path: Path) -> None:
    default_cfg = LoopConfig(output_dir=str(tmp_path), run_id="langgraph-default-config")
    resolved = default_cfg.resolved_config()

    assert "runtime_backend" not in resolved
    assert not hasattr(default_cfg, "runtime_backend")


def test_run_agent_loop_routes_default_path_through_langgraph_with_mock_provider(tmp_path: Path) -> None:
    from method.llm_stages import MockLLMProvider

    sl1 = {
        "candidate_dsl": _stable_dsl(),
        "grounding_seeds": [],
        "assumptions": [],
    }
    sl5 = {"scenarios": [{"name": "empty_smoke", "steps": []}]}
    sl7 = {"decision": "pass", "risk_level": "none", "findings": [], "blocking_findings": []}
    provider = MockLLMProvider(responses=[
        __import__("json").dumps(sl1, ensure_ascii=False),
        __import__("json").dumps(sl5, ensure_ascii=False),
        __import__("json").dumps(sl7, ensure_ascii=False),
    ])
    cfg = LoopConfig(
        condition_id="langgraph_loop_entry_mock",
        condition_family="test_profile",
        base_condition_id="full_staged_v1",
        changed_factors=["llm_provider_mode=mock"],
        llm_provider_mode="mock",
        llm_policy={"provider_mode": "mock"},
        academic_question="mock profile validates run_agent_loop langgraph routing only",
        output_dir=str(tmp_path),
        run_id="pr-langgraph-loop-entry-smoke",
        max_iterations=1,
    )

    result = loop.run_agent_loop("The controller starts in Idle.", cfg, llm_provider=provider)

    assert result.status == "converged"
    record = read_agent_loop_run_record(result.run_record_path or "")
    assert record.environment["graph_runtime_backend"] == "langgraph"
    assert record.environment["graph_runtime_status"] == "enabled"
    assert record.run_config["runtime_implementation"] == "method.langgraph_runtime.run_full_staged_langgraph_runtime"
    assert record.run_config["langgraph_called_from_loop"] is True
    assert record.run_config["canonical_runtime_backend"] == "langgraph"
    assert record.final_artifacts["main_result_eligible"] is False
    graph_events = [item for item in record.logs if isinstance(item, dict) and item.get("event") == "langgraph_node_trace"]
    assert graph_events
    node_trace = graph_events[-1]["node_trace"]
    assert any(item["node_id"] == "validation_pass" for item in node_trace)
    assert node_trace[-1]["node_id"] == "sc13_trace_audit"
    assert record.final_artifacts["langgraph_runtime_trace"]["delegated_monolithic_runtime"] is False



def test_default_langgraph_runtime_does_not_call_monolithic_staged_runtime(monkeypatch, tmp_path: Path) -> None:
    from method.llm_stages import MockLLMProvider
    import method.staged_runtime as staged_runtime

    def forbidden_monolithic_runtime(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("monolithic staged runtime must not be called by default LangGraph path")

    monkeypatch.setattr(staged_runtime, "run_full_staged_deterministic_runtime", forbidden_monolithic_runtime)
    provider = MockLLMProvider(
        responses=[
            __import__("json").dumps({"candidate_dsl": _stable_dsl(), "grounding_seeds": [], "assumptions": []}, ensure_ascii=False),
            __import__("json").dumps({"scenarios": [{"name": "empty_smoke", "steps": []}]}, ensure_ascii=False),
            __import__("json").dumps({"decision": "pass", "risk_level": "none", "findings": [], "blocking_findings": []}, ensure_ascii=False),
        ]
    )
    cfg = LoopConfig(
        condition_id="langgraph_no_monolithic_mock",
        condition_family="test_profile",
        base_condition_id="full_staged_v1",
        changed_factors=["llm_provider_mode=mock"],
        llm_provider_mode="mock",
        llm_policy={"provider_mode": "mock"},
        academic_question="mock profile validates default LangGraph path does not call monolithic staged runtime",
        output_dir=str(tmp_path),
        run_id="pr-langgraph-no-monolithic-smoke",
        max_iterations=1,
    )

    result = loop.run_agent_loop("The controller starts in Idle.", cfg, llm_provider=provider)

    assert result.status == "converged"
    record = read_agent_loop_run_record(result.run_record_path or "")
    assert record.run_config["canonical_runtime_backend"] == "langgraph"
    assert record.run_config["graph_node_registry"]["delegated_monolithic_runtime"] is False


def test_checkpoint_resume_smoke_uses_langgraph_history_and_append_only_fixlog() -> None:
    from method.langgraph_runtime import _checkpoint_resume_smoke

    smoke = _checkpoint_resume_smoke()

    assert smoke["scope"] == "toy_ledger_langgraph_api_smoke"
    assert smoke["real_agent_loop_resume_supported"] is False
    assert "not evidence" in smoke["academic_claim"]
    assert smoke["checked_breakpoints"] == ["after_SD-8", "after_SL-9", "after_SL-10_rework"]
    assert smoke["checkpoint_history_count"] >= 4
    assert smoke["final_fix_log_count"] == 3
    assert smoke["fix_log_append_only"] is True
    assert smoke["duplicate_entry_detected"] is False
    assert smoke["resume_append_only"] is True
    assert [item["breakpoint"] for item in smoke["resume_checks"]] == smoke["checked_breakpoints"]
    assert [item["prefix_count"] for item in smoke["resume_checks"]] == [1, 2, 3]
    assert all(item["prefix_preserved"] for item in smoke["resume_checks"])
    assert "StateGraph" in smoke["resume_api"]


def test_targeted_scenario_refresh_preserves_previous_oracle_by_name() -> None:
    from method.staged_runtime import _merge_scenario_sets_by_name

    previous = [
        TestScenario(name="default_init", description="root smoke"),
        TestScenario(name="fault_recovery", description="old definition"),
    ]
    targeted = [
        TestScenario(name="fault_recovery", description="updated stronger definition"),
        TestScenario(name="effect_probe", description="new mutation probe"),
    ]

    merged, audit = _merge_scenario_sets_by_name(previous, targeted)

    assert [scenario.name for scenario in merged] == ["default_init", "fault_recovery", "effect_probe"]
    assert merged[1].description == "updated stronger definition"
    assert audit["merge_policy"] == "preserve_previous_scenarios_by_name"
    assert audit["previous_count"] == 2
    assert audit["new_count"] == 2
    assert audit["merged_count"] == 3
    assert audit["new_only_names"] == ["effect_probe"]
    assert audit["updated_existing_names"] == ["fault_recovery"]


# PR-LG-A1 Command routing contract tests.

def _adapters_with(**overrides: Any) -> FullStagedRuntimeAdapters:
    base = _adapters()
    data = {
        "parse": base.parse,
        "semantic": base.semantic,
        "design": base.design,
        "scenario_generate": base.scenario_generate,
        "scenario_coverage": base.scenario_coverage,
        "sim": base.sim,
        "model_review": base.model_review,
        "repair": base.repair,
        "repair_review": base.repair_review,
        "sl10_review": base.sl10_review,
        "delta_review": base.delta_review,
        "initial_modeling": base.initial_modeling,
    }
    data.update(overrides)
    return FullStagedRuntimeAdapters(**data)


def _run_langgraph_mock(
    tmp_path: Path,
    *,
    run_id: str,
    adapters: FullStagedRuntimeAdapters | None = None,
    initial_dsl: str | None = None,
    max_iterations: int = 1,
    condition_id: str | None = None,
) -> Any:
    from method.langgraph_runtime import run_full_staged_langgraph_runtime

    return run_full_staged_langgraph_runtime(
        "LG-A1 Command routing should preserve graph evidence.",
        config=LoopConfig(
            condition_id=condition_id or run_id,
            condition_family="test_profile",
            base_condition_id="full_staged_v1",
            changed_factors=["llm_provider_mode=mock", "lg_a1_command_routing_contract"],
            llm_provider_mode="mock",
            academic_question="test-only LG-A1 Command routing contract; excluded from main results",
            output_dir=str(tmp_path),
            run_id=run_id,
            max_iterations=max_iterations,
            compatibility_mode="langgraph_stategraph",
        ),
        initial_dsl=initial_dsl or _stable_dsl(),
        adapters=adapters or _adapters(),
    )


def _lg_record(result: Any) -> Any:
    assert result.run_record_path
    return read_agent_loop_run_record(result.run_record_path)


def _lg_trace_nodes(record: Any) -> list[str]:
    return [str(item.get("node_id") or "") for item in record.run_config.get("langgraph_node_trace", [])]


def _lg_top_level_trace_nodes(record: Any) -> list[str]:
    top_level_nodes = {
        "sc0_start",
        "sl1_initial_modeling",
        "iteration_gate",
        "validation_pass",
        "validation_decision",
        "repair_path",
        "repair_decision",
        "waiver_continue",
        "sc12_budget_exhausted",
        "sc13_trace_audit",
    }
    return [node for node in _lg_trace_nodes(record) if node in top_level_nodes]


def _lg_validation_subgraph_nodes(record: Any) -> list[str]:
    return [node for node in _lg_trace_nodes(record) if node.startswith("validation_") and node not in {"validation_pass", "validation_decision"}]


def _lg_baseline(record: Any) -> dict[str, Any]:
    return {
        "stage_ids": [str(item.get("stage_id") if isinstance(item, dict) else item.stage_id) for item in record.stage_records],
        "record_status": record.status,
        "verdict": record.final_artifacts.get("verdict"),
        "verdict_source_stage_id": record.final_artifacts.get("verdict_source_stage_id"),
        "oracle_weak": record.final_artifacts.get("oracle_weak"),
        "main_result_eligible": record.final_artifacts.get("main_result_eligible"),
        "exclusion_reason": record.final_artifacts.get("exclusion_reason"),
        "iteration_count": len(record.iteration_records),
        "fix_log_count": int(record.replay_index.get("fix_log_count") or 0),
        "trace_nodes": _lg_trace_nodes(record),
    }



def _retry_exhausted_run(stage_id: StageId, error_kind: str = "provider_error") -> Any:
    message = f"{stage_id.value} {error_kind} exhausted"
    meta = _meta(stage_id, ok=False, status=StageStatus.ERROR)
    meta.stage_error = message
    return SimpleNamespace(
        stage_id=stage_id.value,
        ok=False,
        parsed_output={},
        feedback=None,
        stage_meta=meta,
        interaction={
            "stage_id": stage_id.value,
            "provider": "test-adapter",
            "model_id": "none",
            "schema_validation_ok": False,
            "retry_error": {"error_kind": error_kind, "error_message": message},
            "attempts": [{"status": error_kind, "error_kind": error_kind, "error_message": message}],
        },
    )


def _local_reject_review(_request: RepairRequest) -> tuple[RepairReviewFeedback, StageResultMeta]:
    rejection = RepairRejection(
        rejected_by_stage=StageId.SL_10_REPAIR_REVIEW.value,
        reason="mock_repair_review_rejected_candidate",
        target_resolved=False,
        regression_detected=True,
        drift_risk="major",
        evidence=[{"case": "lg_a1_repair_rejection"}],
    )
    feedback = RepairReviewFeedback(ok=False, target_resolved=False, regression_detected=True, drift_risk="major", local_rejection=rejection)
    return feedback, _meta(StageId.SD_10_REPAIR_REVIEW, ok=False)


def test_command_routing_no_next_action_as_primary_source() -> None:
    import inspect
    import method.langgraph_runtime as lg

    source = inspect.getsource(lg._build_graph)

    assert "Command(" in source
    assert "add_conditional_edges" not in source
    assert "def route_iteration_gate" not in source
    assert "def route_validation_decision" not in source
    assert "def route_repair_decision" not in source
    assert "def route_waiver_continue" not in source
    assert "graph_state.get(\"next_action\")" not in source
    assert "graph_state['next_action']" not in source
    assert 'graph_state["next_action"]' not in source


def test_lg_b1_validation_subgraph_replaces_monolithic_validation_pass(tmp_path: Path) -> None:
    import inspect
    import method.langgraph_runtime as lg

    build_graph_source = inspect.getsource(lg._build_graph)
    validation_subgraph_source = inspect.getsource(lg._build_validation_subgraph)

    assert "_build_validation_subgraph" in build_graph_source
    assert "_run_validation_pass" not in build_graph_source
    assert "_run_validation_pass" not in validation_subgraph_source

    record = _lg_record(_run_langgraph_mock(tmp_path, run_id="lg-b1-validation-subgraph-contract"))
    validation_nodes = _lg_validation_subgraph_nodes(record)

    assert validation_nodes == [
        "validation_subgraph",
        "validation_sd2_parse",
        "validation_sd3_semantic",
        "validation_sd4_design",
        "validation_sl5_scenario_generation",
        "validation_sd5a_scenario_coverage",
        "validation_sc5f_scenario_freeze",
        "validation_sd6_sim",
        "validation_sl7_model_review",
        "validation_finalize",
    ]
    assert _lg_top_level_trace_nodes(record) == [
        "sc0_start",
        "sl1_initial_modeling",
        "iteration_gate",
        "validation_pass",
        "validation_decision",
        "sc13_trace_audit",
    ]


def test_command_routing_baseline_full_pass_and_budget_exhausted_path(tmp_path: Path) -> None:
    full_pass = _lg_record(_run_langgraph_mock(tmp_path, run_id="lg-a1-full-pass", max_iterations=1))
    full_pass_baseline = _lg_baseline(full_pass)

    assert full_pass.status == "success"
    assert full_pass.final_artifacts["verdict"] == "success"
    assert full_pass.final_artifacts["verdict_source_stage_id"] == StageId.SL_7_MODEL_REVIEW.value
    assert _lg_top_level_trace_nodes(full_pass) == [
        "sc0_start",
        "sl1_initial_modeling",
        "iteration_gate",
        "validation_pass",
        "validation_decision",
        "sc13_trace_audit",
    ]
    assert _lg_validation_subgraph_nodes(full_pass) == [
        "validation_subgraph",
        "validation_sd2_parse",
        "validation_sd3_semantic",
        "validation_sd4_design",
        "validation_sl5_scenario_generation",
        "validation_sd5a_scenario_coverage",
        "validation_sc5f_scenario_freeze",
        "validation_sd6_sim",
        "validation_sl7_model_review",
        "validation_finalize",
    ]
    assert full_pass_baseline["stage_ids"][-1] == StageId.SC_13_TRACE_AUDIT.value
    assert full_pass.final_artifacts["main_result_eligible"] is False

    budget = _lg_record(_run_langgraph_mock(tmp_path, run_id="lg-a1-budget-zero", max_iterations=0))
    budget_baseline = _lg_baseline(budget)

    assert budget.status == "budget_exhausted"
    assert budget.final_artifacts["verdict"] == "not_converged"
    assert budget.final_artifacts["verdict_source_stage_id"] == StageId.SC_0_START.value
    assert _lg_top_level_trace_nodes(budget) == [
        "sc0_start",
        "sl1_initial_modeling",
        "iteration_gate",
        "sc13_trace_audit",
    ]
    assert budget.final_artifacts["main_result_eligible"] is False


def test_command_routing_equivalence_sc12_verdict_source_matrix(tmp_path: Path) -> None:
    def weak_sim(_dsl: str, _scenarios_or_set: Any, _context: StageContext) -> tuple[SimFeedback, StageResultMeta]:
        return (
            SimFeedback(ok=False, n_scenarios=1, n_scenarios_passed=0, oracle_weak=True, weak_oracle_reason="mock_weak"),
            _meta(StageId.SD_6_SIM, ok=False),
        )

    def design_block(_context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        item = DesignDiagnosticItem(
            code="W_LG_A1_BLOCK",
            pyfcstm_severity="warning",
            policy_action="hard_block",
            instance_key="lg-a1:block",
            rationale="force repair path for Command routing matrix",
        )
        return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)

    def retry_model_review(_dsl: str, _context: StageContext, _feedback: dict[str, Any]) -> tuple[ModelReviewFeedback, StageResultMeta]:
        raise _LLMRetryExhausted(
            stage_id=StageId.SL_7_MODEL_REVIEW.value,
            retry_error={"error_kind": "provider_error", "error_message": "mock retry exhausted"},
            interaction={"stage_id": StageId.SL_7_MODEL_REVIEW.value, "attempts": [{"status": "provider_error"}]},
        )

    cases = [
        (
            "full_pass",
            _adapters(),
            1,
            "success",
            "success",
            StageId.SL_7_MODEL_REVIEW.value,
            ["validation_decision", "sc13_trace_audit"],
        ),
        (
            "oracle_weak_sd6",
            _adapters_with(sim=weak_sim),
            1,
            "failed",
            "not_converged",
            StageId.SD_6_SIM.value,
            ["validation_decision", "sc13_trace_audit"],
        ),
        (
            "repair_rejection",
            _adapters_with(design=design_block, repair=lambda _request: _stable_dsl(), repair_review=_local_reject_review),
            1,
            "rejected",
            "not_converged",
            StageId.SL_10_REPAIR_REVIEW.value,
            ["repair_path", "repair_decision", "sc13_trace_audit"],
        ),
        (
            "budget_exhausted_after_accept",
            _adapters_with(design=design_block, repair=lambda _request: _stable_dsl()),
            1,
            "budget_exhausted",
            "not_converged",
            StageId.SC_11_ACCEPT_CANDIDATE.value,
            ["repair_path", "repair_decision", "sc13_trace_audit"],
        ),
        (
            "llm_retry_exhausted_sl7",
            _adapters_with(model_review=retry_model_review),
            1,
            "error",
            "provider_error",
            StageId.SL_7_MODEL_REVIEW.value,
            ["validation_pass", "validation_decision", "sc13_trace_audit"],
        ),
    ]

    for name, adapters, max_iterations, record_status, verdict, source_stage, required_nodes in cases:
        record = _lg_record(_run_langgraph_mock(tmp_path, run_id=f"lg-a1-matrix-{name}", adapters=adapters, max_iterations=max_iterations))
        assert record.status == record_status, name
        assert record.final_artifacts["verdict"] == verdict, name
        assert record.final_artifacts["verdict_source_stage_id"] == source_stage, name
        trace_nodes = _lg_trace_nodes(record)
        for node in required_nodes:
            assert node in trace_nodes, (name, trace_nodes)


def test_command_routing_preserves_eligibility_nfrr(tmp_path: Path) -> None:
    def weak_sim(_dsl: str, _scenarios_or_set: Any, _context: StageContext) -> tuple[SimFeedback, StageResultMeta]:
        return (
            SimFeedback(ok=False, n_scenarios=1, n_scenarios_passed=0, oracle_weak=True, weak_oracle_reason="mock_weak"),
            _meta(StageId.SD_6_SIM, ok=False),
        )

    success = _lg_record(_run_langgraph_mock(tmp_path, run_id="lg-a1-elig-success"))
    weak = _lg_record(_run_langgraph_mock(tmp_path, run_id="lg-a1-elig-weak", adapters=_adapters_with(sim=weak_sim)))

    assert success.final_artifacts["oracle_weak"] is False
    assert success.final_artifacts["main_result_eligible"] is False
    assert "non_real_provider_mode" in str(success.final_artifacts["exclusion_reason"])
    assert weak.final_artifacts["oracle_weak"] is True
    assert weak.final_artifacts["main_result_eligible"] is False
    assert weak.final_artifacts["exclusion_reason"] == "verdict_not_success"
    assert weak.final_artifacts["verdict_source_stage_id"] == StageId.SD_6_SIM.value


def test_command_routing_waiver_continue_path_keeps_transient_until_downstream_validation(tmp_path: Path) -> None:
    def design_block(_context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        item = DesignDiagnosticItem(
            code="W_LG_A1_WAIVER",
            pyfcstm_severity="warning",
            policy_action="budgeted_repair",
            instance_key="lg-a1:waiver",
            rationale="waiver-allowed diagnostic for Command routing",
        )
        return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)

    def reject_all_as_waiver(_request: RepairRequest) -> dict[str, Any]:
        return {
            "candidate_dsl": "",
            "decisions": [{"request_id": "all", "decision": "reject", "rationale": "safe waiver"}],
            "repair_rationale": ["safe waiver"],
            "diff_summary": {"changed": False},
        }

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-a1-waiver-continue",
            adapters=_adapters_with(design=design_block, repair=reject_all_as_waiver),
            max_iterations=1,
        )
    )

    trace_nodes = _lg_trace_nodes(record)
    assert "waiver_continue" in trace_nodes
    assert trace_nodes[-1] == "sc13_trace_audit"
    assert record.status in {"success", "budget_exhausted", "failed", "rejected"}
    assert record.iteration_records
    assert "post_waiver_stage_ids" in record.iteration_records[0]
    post_waiver_nodes = trace_nodes[trace_nodes.index("waiver_continue") + 1 :]
    assert "validation_subgraph" in post_waiver_nodes
    assert "validation_sd2_parse" not in post_waiver_nodes
    assert "validation_sd3_semantic" not in post_waiver_nodes
    assert "validation_sd4_design" in post_waiver_nodes
    assert "validation_sl5_scenario_generation" in post_waiver_nodes
    assert "validation_sd6_sim" in post_waiver_nodes
    assert "validation_sl7_model_review" in post_waiver_nodes
    assert record.iteration_records[0]["post_waiver_stage_ids"] == [
        StageId.SD_4_DESIGN.value,
        StageId.SL_5_SCENARIO_GENERATION.value,
        StageId.SD_5A_SCENARIO_COVERAGE.value,
        StageId.SC_5F_SCENARIO_FREEZE.value,
        StageId.SD_6_SIM.value,
        StageId.SL_7_MODEL_REVIEW.value,
    ]
    post_waiver_stage_logs = [
        item
        for item in record.logs
        if isinstance(item, dict)
        and item.get("event") == "stage_result"
        and item.get("stage_id") in {StageId.SD_4_DESIGN.value, StageId.SL_5_SCENARIO_GENERATION.value, StageId.SD_5A_SCENARIO_COVERAGE.value, StageId.SC_5F_SCENARIO_FREEZE.value, StageId.SD_6_SIM.value, StageId.SL_7_MODEL_REVIEW.value}
        and item.get("iteration") == 0
    ]
    post_waiver_stage_logs = post_waiver_stage_logs[-6:]
    assert post_waiver_stage_logs
    assert all(item.get("graph_subgraph") == "validation_subgraph" for item in post_waiver_stage_logs)
    assert all(str(item.get("graph_node") or "").startswith("validation_") for item in post_waiver_stage_logs)


def test_command_routing_repair_retry_exhausted_visits_decision_and_cleans_transient(tmp_path: Path) -> None:
    def design_block(_context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        item = DesignDiagnosticItem(
            code="W_LG_A1_SL9_RETRY",
            pyfcstm_severity="warning",
            policy_action="hard_block",
            instance_key="lg-a1:sl9-retry",
            rationale="force SL-9 retry-exhausted repair path",
        )
        return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-a1-sl9-retry-exhausted",
            adapters=_adapters_with(design=design_block, repair=lambda _request: _retry_exhausted_run(StageId.SL_9_REPAIR, "provider_error")),
            max_iterations=2,
        )
    )

    trace_nodes = _lg_trace_nodes(record)
    assert trace_nodes[-3:] == ["repair_path", "repair_decision", "sc13_trace_audit"]
    assert record.status == "error"
    assert record.final_artifacts["verdict"] == "provider_error"
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SL_9_REPAIR.value
    assert record.final_artifacts["main_result_eligible"] is False
    assert record.iteration_records[-1]["exit_reason"].startswith(f"{StageId.SL_9_REPAIR.value} retry exhausted")
    assert record.llm_interactions[-1]["retry_error"]["error_kind"] == "provider_error"
    assert record.llm_interactions[-1]["attempts"]
    lifecycle = _assert_lg_a2_store_metadata(record)
    assert lifecycle["put_count"] == 1
    assert lifecycle["get_count"] >= 1


def test_command_routing_waiver_continue_retry_exhausted_cleans_transient(tmp_path: Path) -> None:
    def design_block(_context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        item = DesignDiagnosticItem(
            code="W_LG_A1_WAIVER_RETRY",
            pyfcstm_severity="warning",
            policy_action="budgeted_repair",
            instance_key="lg-a1:waiver-retry",
            rationale="waiver-allowed diagnostic for Command routing retry cleanup",
        )
        return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)

    def reject_all_as_waiver(_request: RepairRequest) -> dict[str, Any]:
        return {
            "candidate_dsl": "",
            "decisions": [{"request_id": "all", "decision": "reject", "rationale": "safe waiver"}],
            "repair_rationale": ["safe waiver"],
            "diff_summary": {"changed": False},
        }

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-a1-waiver-sl5-retry-exhausted",
            adapters=_adapters_with(
                design=design_block,
                repair=reject_all_as_waiver,
                scenario_generate=lambda _request: _retry_exhausted_run(StageId.SL_5_SCENARIO_GENERATION, "empty_output"),
            ),
            max_iterations=2,
        )
    )

    trace_nodes = _lg_trace_nodes(record)
    assert "waiver_continue" in trace_nodes
    assert trace_nodes[-1] == "sc13_trace_audit"
    assert record.status == "invalid"
    assert record.final_artifacts["verdict"] == "invalid"
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SL_5_SCENARIO_GENERATION.value
    assert record.iteration_records[-1]["exit_reason"].startswith(f"{StageId.SL_5_SCENARIO_GENERATION.value} retry exhausted")
    assert record.llm_interactions[-1]["retry_error"]["error_kind"] == "empty_output"
    lifecycle = _assert_lg_a2_store_metadata(record)
    assert lifecycle["put_count"] == 1
    assert lifecycle["get_count"] >= 2


def test_command_routing_multicycle_repair_acceptance_revalidates_via_command(tmp_path: Path) -> None:
    parse_calls: list[str] = []

    def parse(dsl: str, context: StageContext) -> tuple[ParseFeedback, StageResultMeta]:
        parse_calls.append(dsl)
        return _ok_parse(dsl, context)

    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        if context.current_dsl == "needs-repair":
            item = DesignDiagnosticItem(
                code="W_LG_A1_MULTICYCLE",
                pyfcstm_severity="warning",
                policy_action="hard_block",
                instance_key="lg-a1:multicycle",
                rationale="force one accepted repair before full revalidation",
            )
            return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)
        return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-a1-multicycle-acceptance",
            initial_dsl="needs-repair",
            adapters=_adapters_with(parse=parse, design=design, repair=lambda _request: _stable_dsl()),
            max_iterations=3,
        )
    )

    trace_nodes = _lg_trace_nodes(record)
    top_level_trace_nodes = _lg_top_level_trace_nodes(record)
    assert top_level_trace_nodes == [
        "sc0_start",
        "sl1_initial_modeling",
        "iteration_gate",
        "validation_pass",
        "validation_decision",
        "repair_path",
        "repair_decision",
        "iteration_gate",
        "validation_pass",
        "validation_decision",
        "sc13_trace_audit",
    ]
    assert top_level_trace_nodes.count("iteration_gate") == 2
    assert top_level_trace_nodes.count("validation_pass") == 2
    assert top_level_trace_nodes.count("repair_decision") == 1
    assert trace_nodes.count("validation_subgraph") == 2
    assert trace_nodes.count("validation_sd2_parse") == 2
    assert trace_nodes.count("validation_sd4_design") == 2
    assert parse_calls == ["needs-repair", _stable_dsl()]
    assert record.status == "success"
    assert record.final_artifacts["verdict"] == "success"
    assert len(record.iteration_records) == 2
    assert record.iteration_records[0]["accepted_candidate"] is True
    assert record.iteration_records[1]["exit_reason"] == "full_pass_all_required_feedback_ok"


# PR-LG-A2 Store transient contract tests.

def _assert_lg_a2_store_metadata(record: Any, *, expected_status: str = "no_leak") -> dict[str, Any]:
    env = record.environment
    artifacts = record.final_artifacts
    assert env["transient_backend"] == "langgraph_inmemory_store"
    assert env["transient_namespace"] == f"transient/{record.run_id}"
    assert env["transient_store_instance_id"]
    assert env["transient_cleanup_status"] == expected_status
    assert env["transient_final_item_count"] == 0
    assert artifacts["transient_lifecycle"]["backend"] == "langgraph_inmemory_store"
    assert artifacts["transient_lifecycle"]["cleanup_status"] == expected_status
    assert artifacts["transient_lifecycle"]["final_item_count"] == 0
    assert artifacts["transient_lifecycle"]["put_count"] == env["transient_put_count"]
    assert artifacts["transient_lifecycle"]["get_count"] == env["transient_get_count"]
    assert artifacts["transient_lifecycle"]["drop_count"] == env["transient_drop_count"]
    return artifacts["transient_lifecycle"]


def test_store_compat_smoke_put_get_search_delete_and_get_store() -> None:
    from method.langgraph_runtime import langgraph_store_compat_smoke

    smoke = langgraph_store_compat_smoke()

    assert smoke["ok"] is True
    assert smoke["inmemory_store_ok"] is True
    assert smoke["namespace_isolation_ok"] is True
    assert smoke["compile_store_ok"] is True
    assert smoke["get_store_ok"] is True
    assert smoke["delete_ok"] is True


def test_store_transient_backend_replaces_global_dict(tmp_path: Path) -> None:
    from method import langgraph_runtime as lg

    before_transients = dict(lg._TRANSIENT_OBJECTS)
    record = _lg_record(_run_langgraph_mock(tmp_path, run_id="lg-a2-backend-replaces-global"))
    lifecycle = _assert_lg_a2_store_metadata(record)

    assert lifecycle["put_count"] >= 1
    assert lg._TRANSIENT_OBJECTS == before_transients
    assert "transient_store" in record.environment.get("instrumentation_layer", "") or record.environment["transient_backend"] == "langgraph_inmemory_store"


def test_store_transient_cleanup_full_pass(tmp_path: Path) -> None:
    record = _lg_record(_run_langgraph_mock(tmp_path, run_id="lg-a2-cleanup-full-pass"))
    lifecycle = _assert_lg_a2_store_metadata(record)

    assert record.status == "success"
    assert lifecycle["put_count"] == 1
    assert lifecycle["drop_count"] >= 1


def test_store_transient_cleanup_weak_oracle(tmp_path: Path) -> None:
    def weak_sim(_dsl: str, _scenarios_or_set: Any, _context: StageContext) -> tuple[SimFeedback, StageResultMeta]:
        return (
            SimFeedback(ok=False, n_scenarios=1, n_scenarios_passed=0, oracle_weak=True, weak_oracle_reason="mock_weak"),
            _meta(StageId.SD_6_SIM, ok=False),
        )

    record = _lg_record(_run_langgraph_mock(tmp_path, run_id="lg-a2-cleanup-weak-oracle", adapters=_adapters_with(sim=weak_sim)))
    lifecycle = _assert_lg_a2_store_metadata(record)

    assert record.status == "failed"
    assert record.final_artifacts["oracle_weak"] is True
    assert lifecycle["put_count"] == 1


def test_store_transient_cleanup_budget_exhausted_from_iteration_gate(tmp_path: Path) -> None:
    record = _lg_record(_run_langgraph_mock(tmp_path, run_id="lg-a2-cleanup-budget-zero", max_iterations=0))
    lifecycle = _assert_lg_a2_store_metadata(record)

    assert record.status == "budget_exhausted"
    assert lifecycle["put_count"] == 0
    assert lifecycle["final_drain_count"] >= 1


def test_store_transient_cleanup_repair_retry_exhausted(tmp_path: Path) -> None:
    def design_block(_context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        item = DesignDiagnosticItem(
            code="W_LG_A2_SL9_RETRY",
            pyfcstm_severity="warning",
            policy_action="hard_block",
            instance_key="lg-a2:sl9-retry",
            rationale="force SL-9 retry-exhausted path for Store cleanup",
        )
        return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-a2-cleanup-sl9-retry",
            adapters=_adapters_with(design=design_block, repair=lambda _request: _retry_exhausted_run(StageId.SL_9_REPAIR, "provider_error")),
            max_iterations=2,
        )
    )
    lifecycle = _assert_lg_a2_store_metadata(record)

    assert record.status == "error"
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SL_9_REPAIR.value
    assert lifecycle["put_count"] == 1
    assert lifecycle["get_count"] >= 1


def test_store_transient_cleanup_validation_retry_exhausted_after_accepted_repair(tmp_path: Path) -> None:
    design_calls = {"count": 0}

    def design_block_once(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        design_calls["count"] += 1
        if design_calls["count"] == 1:
            item = DesignDiagnosticItem(
                code="W_LG_A2_STALE_REF_REPRO",
                pyfcstm_severity="warning",
                policy_action="hard_block",
                instance_key="lg-a2:stale-ref-repro",
                rationale="force accepted repair before a next-iteration validation retry exhaustion",
            )
            return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)
        return _ok_design(context)

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-a2-cleanup-validation-retry-after-repair",
            initial_dsl="needs-repair",
            adapters=_adapters_with(
                design=design_block_once,
                repair=lambda _request: _stable_dsl(),
                model_review=lambda _dsl, _context, _feedback: _retry_exhausted_run(StageId.SL_7_MODEL_REVIEW, "provider_error"),
            ),
            max_iterations=3,
        )
    )
    lifecycle = _assert_lg_a2_store_metadata(record)

    assert record.status == "error"
    assert record.final_artifacts["verdict"] == "provider_error"
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SL_7_MODEL_REVIEW.value
    assert record.iteration_records[-1]["exit_reason"].startswith(f"{StageId.SL_7_MODEL_REVIEW.value} retry exhausted")
    assert lifecycle["put_count"] == 1
    assert lifecycle["get_count"] >= 1
    assert lifecycle["drop_count"] >= 1
    assert _lg_trace_nodes(record)[-2:] == ["validation_decision", "sc13_trace_audit"]


def test_store_transient_cleanup_waiver_retry_exhausted(tmp_path: Path) -> None:
    def design_block(_context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        item = DesignDiagnosticItem(
            code="W_LG_A2_WAIVER_RETRY",
            pyfcstm_severity="warning",
            policy_action="budgeted_repair",
            instance_key="lg-a2:waiver-retry",
            rationale="force waiver_continue retry-exhausted path for Store cleanup",
        )
        return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)

    def reject_all_as_waiver(_request: RepairRequest) -> dict[str, Any]:
        return {
            "candidate_dsl": "",
            "decisions": [{"request_id": "all", "decision": "reject", "rationale": "safe waiver"}],
            "repair_rationale": ["safe waiver"],
            "diff_summary": {"changed": False},
        }

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-a2-cleanup-waiver-retry",
            adapters=_adapters_with(
                design=design_block,
                repair=reject_all_as_waiver,
                scenario_generate=lambda _request: _retry_exhausted_run(StageId.SL_5_SCENARIO_GENERATION, "empty_output"),
            ),
            max_iterations=2,
        )
    )
    lifecycle = _assert_lg_a2_store_metadata(record)

    assert record.status == "invalid"
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SL_5_SCENARIO_GENERATION.value
    assert lifecycle["put_count"] == 1
    assert lifecycle["get_count"] >= 2


def test_store_transient_run_isolation(tmp_path: Path) -> None:
    first = _lg_record(_run_langgraph_mock(tmp_path, run_id="lg-a2-isolation-first"))
    second = _lg_record(_run_langgraph_mock(tmp_path, run_id="lg-a2-isolation-second"))

    first_lifecycle = _assert_lg_a2_store_metadata(first)
    second_lifecycle = _assert_lg_a2_store_metadata(second)
    assert first.environment["transient_namespace"] != second.environment["transient_namespace"]
    assert first.environment["transient_store_instance_id"] != second.environment["transient_store_instance_id"]
    assert first_lifecycle["put_count"] == second_lifecycle["put_count"] == 1


def test_store_transient_preserves_validation_to_repair_data(tmp_path: Path) -> None:
    seen: dict[str, Any] = {}

    def design_block(_context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        item = DesignDiagnosticItem(
            code="W_LG_A2_DATA_TO_REPAIR",
            pyfcstm_severity="warning",
            policy_action="hard_block",
            instance_key="lg-a2:data-to-repair",
            rationale="force repair path to inspect Store-backed validation payload",
        )
        return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)

    def repair(request: RepairRequest) -> str:
        seen["source_stage"] = request.selected_feedback_trace.get("source_stage")
        seen["instance_keys"] = request.selected_feedback_trace.get("blocking_instance_keys")
        seen["scenario_set_none"] = request.scenario_set is None
        return _stable_dsl()

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-a2-preserve-validation-to-repair",
            initial_dsl="needs-repair",
            adapters=_adapters_with(design=design_block, repair=repair),
            max_iterations=1,
        )
    )
    lifecycle = _assert_lg_a2_store_metadata(record)

    assert seen == {
        "source_stage": StageId.SD_4_DESIGN.value,
        "instance_keys": ["lg-a2:data-to-repair"],
        "scenario_set_none": True,
    }
    assert lifecycle["get_count"] >= 1


def test_store_transient_preserves_waiver_continue_data(tmp_path: Path) -> None:
    def design_block(_context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        item = DesignDiagnosticItem(
            code="W_LG_A2_WAIVER_DATA",
            pyfcstm_severity="warning",
            policy_action="budgeted_repair",
            instance_key="lg-a2:waiver-data",
            rationale="force waiver_continue to inspect Store-backed validation payload",
        )
        return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)

    def reject_all_as_waiver(_request: RepairRequest) -> dict[str, Any]:
        return {
            "candidate_dsl": "",
            "decisions": [{"request_id": "all", "decision": "reject", "rationale": "safe waiver"}],
            "repair_rationale": ["safe waiver"],
            "diff_summary": {"changed": False},
        }

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-a2-preserve-waiver-data",
            adapters=_adapters_with(design=design_block, repair=reject_all_as_waiver),
            max_iterations=1,
        )
    )
    lifecycle = _assert_lg_a2_store_metadata(record)

    trace_nodes = _lg_trace_nodes(record)
    assert "waiver_continue" in trace_nodes
    post_waiver_nodes = trace_nodes[trace_nodes.index("waiver_continue") + 1 :]
    assert "validation_subgraph" in post_waiver_nodes
    assert "validation_sl5_scenario_generation" in post_waiver_nodes
    assert "post_waiver_stage_ids" in record.iteration_records[0]
    assert lifecycle["get_count"] >= 2


def test_store_metadata_in_run_record(tmp_path: Path) -> None:
    record = _lg_record(_run_langgraph_mock(tmp_path, run_id="lg-a2-metadata-record"))
    lifecycle = _assert_lg_a2_store_metadata(record)

    expected_keys = {
        "backend",
        "namespace",
        "store_instance_id",
        "put_count",
        "get_count",
        "drop_count",
        "final_item_count",
        "cleanup_status",
        "final_drain_count",
    }
    assert expected_keys.issubset(lifecycle)
    assert record.environment["transient_backend"] == lifecycle["backend"]
    assert record.environment["transient_namespace"] == lifecycle["namespace"]
    assert record.environment["transient_store_instance_id"] == lifecycle["store_instance_id"]
