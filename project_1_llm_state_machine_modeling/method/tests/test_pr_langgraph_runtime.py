from __future__ import annotations

from pathlib import Path
from typing import Any

from method import loop
from method.run_record import read_agent_loop_run_record
from method.schema import (
    DesignFeedback,
    LoopConfig,
    ModelReviewFeedback,
    ParseFeedback,
    RepairReviewFeedback,
    SemanticFeedback,
    SimFeedback,
    StageContext,
    StageResultMeta,
    TestScenario,
)
from method.staged_runtime import (
    FullStagedRuntimeAdapters,
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
    assert all(not node.get("delegated_subgraph") for node in registry["nodes"])
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
