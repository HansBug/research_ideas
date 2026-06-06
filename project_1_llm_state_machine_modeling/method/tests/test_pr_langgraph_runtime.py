from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

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
    ReviewRunMeta,
    SemanticFeedback,
    SimFeedback,
    SL10RepairReviewOutput,
    ScenarioResult,
    ScenarioStep,
    StageContext,
    StageResultMeta,
    StepResult,
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



def test_lg_b3_waiver_entry_envelope_contract_separates_repair_patch_and_validation_source() -> None:
    import method.langgraph_runtime as lg

    context = StageContext(nl="waiver contract", current_dsl=_stable_dsl())
    selected = DesignFeedback(
        ok=False,
        blocking_items=[
            DesignDiagnosticItem(
                code="W_LG_B3_CONTRACT",
                pyfcstm_severity="warning",
                policy_action="budgeted_repair",
                instance_key="lg-b3:contract",
                rationale="contract fixture",
            )
        ],
    )
    validation = lg._ValidationPass(
        context=context,
        feedback={"design": selected},
        stage_metas=[_meta(StageId.SD_2_PARSE), _meta(StageId.SD_3_SEMANTIC), _meta(StageId.SD_4_DESIGN, ok=False)],
        selected=("design", selected, StageId.SD_4_DESIGN.value),
        scenario_set=None,
        scenario_history=[],
        oracle_weak=False,
        scenario_epoch=None,
    )
    repair_patch = {
        "waiver_continue": True,
        "accepted_candidate": False,
        "selected_feedback": {"source": "design", "source_stage": StageId.SD_4_DESIGN.value},
        "repair_stage_ids": [StageId.SD_8_FIX_PLAN.value, StageId.SL_9_REPAIR.value],
        "exit_reason": "all_fix_requests_rejected_as_waiver_continue",
    }

    envelope = lg._build_waiver_entry_envelope(
        repair_patch=repair_patch,
        validation_ref="transient:validation:0",
        validation=validation,
        iteration=3,
    )

    assert envelope["schema_version"] == "lg-b3.waiver-entry-envelope.v1"
    assert envelope["repair_patch"]["waiver_continue"] is True
    assert envelope["repair_patch"]["selected_feedback"]["source_stage"] == StageId.SD_4_DESIGN.value
    assert envelope["validation_ref"] == "transient:validation:0"
    assert envelope["validation_source"]["object_type"] == "_ValidationPass"
    assert envelope["validation_source"]["selected_feedback"]["source_stage"] == StageId.SD_4_DESIGN.value
    assert envelope["validation_scenario_epoch"] is None
    assert envelope["validation_oracle_weak"] is False
    assert envelope["iteration"] == 3
    assert envelope["tail_start_stage"] == StageId.SD_4_DESIGN.value
    assert envelope["tail_kind"] == "design_warning_waiver"

    with pytest.raises(ValueError, match="waiver_continue=true"):
        lg._build_waiver_entry_envelope(
            repair_patch={**repair_patch, "waiver_continue": False},
            validation_ref="transient:validation:0",
            validation=validation,
            iteration=3,
        )
    with pytest.raises(ValueError, match="no accepted_candidate"):
        lg._build_waiver_entry_envelope(
            repair_patch={**repair_patch, "accepted_candidate": True},
            validation_ref="transient:validation:0",
            validation=validation,
            iteration=3,
        )
    with pytest.raises(ValueError, match="validation_ref"):
        lg._build_waiver_entry_envelope(
            repair_patch=repair_patch,
            validation_ref="",
            validation=validation,
            iteration=3,
        )
    with pytest.raises(ValueError, match="scenario_epoch"):
        lg._build_waiver_entry_envelope(
            repair_patch={**repair_patch, "scenario_epoch": 999},
            validation_ref="transient:validation:0",
            validation=validation,
            iteration=3,
        )
    with pytest.raises(ValueError, match="oracle_weak"):
        lg._build_waiver_entry_envelope(
            repair_patch={**repair_patch, "oracle_weak": True},
            validation_ref="transient:validation:0",
            validation=validation,
            iteration=3,
        )
    with pytest.raises(ValueError, match="iteration"):
        lg._build_waiver_entry_envelope(
            repair_patch={**repair_patch, "iteration": 99},
            validation_ref="transient:validation:0",
            validation=validation,
            iteration=3,
        )
    no_selected_validation = lg._ValidationPass(
        context=context,
        feedback={"design": DesignFeedback(ok=True)},
        stage_metas=[_meta(StageId.SD_2_PARSE), _meta(StageId.SD_3_SEMANTIC), _meta(StageId.SD_4_DESIGN)],
        selected=None,
        scenario_set=None,
        scenario_history=[],
        oracle_weak=False,
        scenario_epoch=None,
    )
    with pytest.raises(ValueError, match="validation.selected"):
        lg._build_waiver_entry_envelope(
            repair_patch=repair_patch,
            validation_ref="transient:validation:no-selected",
            validation=no_selected_validation,
            iteration=3,
        )

    sim_feedback = SimFeedback(
        ok=False,
        n_scenarios=1,
        n_scenarios_passed=0,
        scenario_results=[
            ScenarioResult(
                name="contract_sim",
                status="fail",
                step_results=[StepResult(step_index=0, status="fail")],
            )
        ],
    )
    sim_validation = lg._ValidationPass(
        context=context,
        feedback={"sim": sim_feedback},
        stage_metas=[_meta(StageId.SD_2_PARSE), _meta(StageId.SD_3_SEMANTIC), _meta(StageId.SD_4_DESIGN), _meta(StageId.SD_6_SIM, ok=False)],
        selected=("sim", sim_feedback, StageId.SD_6_SIM.value),
        scenario_set=None,
        scenario_history=[],
        oracle_weak=False,
        scenario_epoch=7,
    )
    with pytest.raises(ValueError, match="selected_feedback mismatch"):
        lg._build_waiver_entry_envelope(
            repair_patch=repair_patch,
            validation_ref="transient:validation:sim",
            validation=sim_validation,
            iteration=3,
        )
    sim_waiver_patch = {
        "waiver_continue": True,
        "accepted_candidate": False,
        "selected_feedback": {"source": "sim", "source_stage": StageId.SD_6_SIM.value},
        "waiver_audit": {"kind": "stale_overridden_scenario_waiver"},
        "repair_stage_ids": [StageId.SD_8_FIX_PLAN.value, StageId.SL_9_REPAIR.value],
        "exit_reason": "all_fix_requests_rejected_as_waiver_continue",
    }
    sim_envelope = lg._build_waiver_entry_envelope(
        repair_patch=sim_waiver_patch,
        validation_ref="transient:validation:sim",
        validation=sim_validation,
        iteration=3,
    )
    assert sim_envelope["tail_kind"] == "stale_overridden_scenario_waiver"
    assert sim_envelope["tail_start_stage"] == StageId.SD_6_SIM.value
    assert sim_envelope["validation_source"]["selected_feedback"]["source_stage"] == StageId.SD_6_SIM.value

    with pytest.raises(ValueError, match="canonical SD-6 sim validation.selected"):
        lg._build_waiver_entry_envelope(
            repair_patch={
                **repair_patch,
                "waiver_audit": {"kind": "stale_overridden_scenario_waiver"},
            },
            validation_ref="transient:validation:design",
            validation=validation,
            iteration=3,
        )
    with pytest.raises(ValueError, match="unsupported waiver_audit.kind"):
        lg._build_waiver_entry_envelope(
            repair_patch={
                "waiver_continue": True,
                "accepted_candidate": False,
                "selected_feedback": {"source": "sim", "source_stage": StageId.SD_6_SIM.value},
                "waiver_audit": {"kind": "sim_waiver"},
            },
            validation_ref="transient:validation:sim",
            validation=sim_validation,
            iteration=3,
        )

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
    assert waiver_node["subgraph_id"] == "waiver_continuation_subgraph"
    assert waiver_node["nested_subgraph_ids"] == ["validation_subgraph"]
    assert {
        "waiver_subgraph_enter",
        "waiver_tail_decision",
        "waiver_design_tail",
        "waiver_sim_tail",
        "waiver_subgraph_finalize",
    }.issubset(set(waiver_node["subgraph_node_ids"]))
    delegated_node_ids = {node["node_id"] for node in registry["nodes"] if node.get("delegated_subgraph")}
    assert delegated_node_ids == {"validation_pass", "waiver_continue", "repair_path"}
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
    waiver_runtime_trace = record.final_artifacts["langgraph_runtime_trace"]["waiver_subgraph_runtime_trace"]
    assert waiver_runtime_trace["node_trace_count"] == 0
    assert waiver_runtime_trace["node_ids"] == []
    assert waiver_runtime_trace["nested_subgraph_ids"] == []



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




def _record_stage_ids(record: Any) -> list[str]:
    return [str(item.get("stage_id") if isinstance(item, dict) else item.stage_id) for item in record.stage_records]

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


def _canonical_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    import hashlib

    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _read_operator_events(record: Any) -> list[dict[str, Any]]:
    operator = record.final_artifacts.get("operator_log") or {}
    path = Path(operator["operator_log_path"])
    assert path.exists()
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _assert_no_forbidden_operator_keys(value: Any) -> None:
    forbidden = {
        "messages",
        "prompt",
        "raw_prompt",
        "raw_output",
        "chunk_text",
        "delta_text",
        "completion_text",
        "content",
        "text",
        "response_text",
        "output_text",
        "choices",
        "delta",
        "api_key",
        "authorization",
        "headers",
    }
    if isinstance(value, dict):
        for key, nested in value.items():
            assert str(key).lower() not in forbidden
            _assert_no_forbidden_operator_keys(nested)
    elif isinstance(value, list):
        for item in value:
            _assert_no_forbidden_operator_keys(item)


def _initial_modeling_llm_run_with_stream_usage(_nl: str, _context: StageContext) -> Any:
    return SimpleNamespace(
        stage_id=StageId.SL_1_INITIAL_MODELING.value,
        ok=True,
        parsed_output={"candidate_dsl": _stable_dsl(), "grounding_seeds": [], "assumptions": []},
        feedback=None,
        stage_meta=_meta(StageId.SL_1_INITIAL_MODELING),
        interaction={
            "stage_id": StageId.SL_1_INITIAL_MODELING.value,
            "provider": "mock-stream-provider",
            "model_id": "mock-stream-model",
            "schema_validation_ok": True,
            "usage": {
                "stream": True,
                "stream_include_usage_requested": True,
                "chunk_count": 7,
                "first_chunk_seconds": 0.05,
                "elapsed_seconds": 0.42,
                "prompt_chars": 1234,
                "completion_chars": 567,
                "estimated_prompt_tokens": 309,
                "estimated_completion_tokens": 142,
                "estimated_total_tokens": 451,
            },
            "attempts": [{"status": "ok", "usage": {"stream": True, "chunk_count": 7}}],
        },
    )



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
            StageId.SD_4_DESIGN.value,
            ["repair_path", "repair_decision", "validation_subgraph", "sc13_trace_audit"],
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
    assert "waiver_subgraph_enter" in post_waiver_nodes
    assert "waiver_tail_decision" in post_waiver_nodes
    assert "waiver_design_tail" in post_waiver_nodes
    assert "waiver_subgraph_finalize" in post_waiver_nodes
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
    envelope = record.iteration_records[0]["waiver_entry_envelope"]
    assert envelope["schema_version"] == "lg-b3.waiver-entry-envelope.v1"
    assert envelope["waiver_continue"] is True
    assert envelope["tail_start_stage"] == StageId.SD_4_DESIGN.value
    assert envelope["tail_kind"] == "design_warning_waiver"
    assert envelope["iteration"] == 0
    assert envelope["graph_state_iteration"] == 0
    assert envelope["repair_patch"]["waiver_continue"] is True
    assert envelope["validation_ref"]
    assert envelope["validation_source"]["object_type"] == "_ValidationPass"
    assert envelope["validation_source"]["selected_feedback"]["source_stage"] == StageId.SD_4_DESIGN.value
    assert envelope["validation_scenario_epoch"] is None
    assert envelope["validation_oracle_weak"] is False
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
    assert any(
        item.get("event") == "waiver_subgraph_enter"
        and item.get("graph_subgraph") == "waiver_continuation_subgraph"
        and item.get("tail_start_stage") == StageId.SD_4_DESIGN.value
        for item in record.logs
        if isinstance(item, dict)
    )
    waiver_runtime_trace = record.final_artifacts["langgraph_runtime_trace"]["waiver_subgraph_runtime_trace"]
    assert waiver_runtime_trace["subgraph_id"] == "waiver_continuation_subgraph"
    assert "waiver_design_tail" in waiver_runtime_trace["node_ids"]
    assert waiver_runtime_trace["nested_subgraph_ids"] == ["validation_subgraph"]


def test_waiver_continue_consumes_stale_scenario_audit_and_enters_sl7(tmp_path: Path) -> None:
    scenario_name = "lg_b1_stale_scenario"
    final_candidate = "uniform-nl-candidate-lg"
    sim_calls: list[str] = []
    model_review_payloads: list[dict[str, Any]] = []

    scenario = TestScenario(
        name=scenario_name,
        description="stale local oracle later overridden by SL-10",
        initial_state="Root.Spare",
        steps=[
            ScenarioStep(
                events=["tick"],
                expected_state="Root.Overload",
                expected_vars={"Pbat_dis": 4.0},
                name="overload_step",
            )
        ],
    )

    def scenario_generate(_request: ScenarioGenerationRequest) -> list[TestScenario]:
        return [scenario]

    def sim(dsl: str, scenarios_or_set: Any, _context: StageContext) -> tuple[SimFeedback, StageResultMeta]:
        sim_calls.append(dsl)
        scenarios = list(getattr(scenarios_or_set, "scenarios", []) or [])
        if dsl == final_candidate:
            failed = ScenarioResult(
                name=scenario_name,
                description=scenario.description,
                status="fail",
                step_results=[
                    StepResult(
                        step_index=0,
                        step_name="overload_step",
                        status="fail",
                        actual_state="Root.Overload",
                        actual_vars={"Pbat_dis": 3.0},
                        state_assertion_ok=True,
                        var_assertion_ok=False,
                        var_mismatches={"Pbat_dis": {"expected": 4.0, "actual": 3.0}},
                    )
                ],
            )
            return (
                SimFeedback(ok=False, n_scenarios=len(scenarios), n_scenarios_passed=0, scenario_results=[failed]),
                _meta(StageId.SD_6_SIM, ok=False),
            )
        return SimFeedback(ok=True, n_scenarios=len(scenarios), n_scenarios_passed=len(scenarios)), _meta(StageId.SD_6_SIM)

    def repair(request: RepairRequest) -> dict[str, Any]:
        assert request.fix_request_batch is not None
        request_id = request.fix_request_batch.requests[0].request_id
        if request.selected_feedback_trace["source_stage"] == StageId.SD_6_SIM.value:
            return {
                "decisions": [
                    {
                        "request_id": request_id,
                        "decision": "reject",
                        "rationale": "Reject stale scenario request because prior FixLog/SL-10 override shows NL conflict.",
                        "rejected_reason": "stale prior override conflicts with NL-grounded expected variable",
                    }
                ],
                "candidate_dsl": "",
                "repair_rationale": ["reuse prior scenario override and continue to SL-7"],
            }
        return {
            "decisions": [{"request_id": request_id, "decision": "accept", "rationale": "accept NL-fidelity correction"}],
            "candidate_dsl": final_candidate,
            "repair_rationale": ["produce uniform NL candidate"],
        }

    def model_review(dsl: str, _context: StageContext, feedback: dict[str, Any]) -> tuple[ModelReviewFeedback, StageResultMeta]:
        model_review_payloads.append(feedback)
        if dsl != final_candidate:
            meta = _meta(StageId.SL_7_MODEL_REVIEW, ok=False)
            return (
                ModelReviewFeedback(
                    ok=False,
                    decision="fail",
                    risk_level="major",
                    blocking_findings=[{"id": "MR-uniform", "summary": "Use the uniform NL-grounded formula."}],
                    meta=meta,
                ),
                meta,
            )
        meta = _meta(StageId.SL_7_MODEL_REVIEW)
        return (
            ModelReviewFeedback(
                ok=True,
                decision="pass",
                risk_level="none",
                findings=[{"id": "MR-waiver-seen", "summary": "stale waiver reviewed"}] if feedback.get("waiver_audit") else [],
                meta=meta,
            ),
            meta,
        )

    def local_review(request: RepairRequest) -> tuple[RepairReviewFeedback, StageResultMeta]:
        if request.candidate_dsl == final_candidate:
            rejection = RepairRejection(
                rejected_by_stage=StageId.SD_10_REPAIR_REVIEW.value,
                reason="scenario_regression",
                target_resolved=True,
                regression_detected=True,
                drift_risk="minor",
                evidence=[{"kind": "scenario_regression", "scenario_names": [scenario_name]}],
            )
            meta = _meta(StageId.SD_10_REPAIR_REVIEW, ok=False)
            return (
                RepairReviewFeedback(
                    ok=False,
                    target_resolved=True,
                    regression_detected=True,
                    drift_risk="minor",
                    local_rejection=rejection,
                    meta=meta,
                ),
                meta,
            )
        meta = _meta(StageId.SD_10_REPAIR_REVIEW)
        return RepairReviewFeedback(ok=True, target_resolved=True, regression_detected=False, drift_risk="none", meta=meta), meta

    def sl10_review(_request: RepairRequest, _local: RepairReviewFeedback) -> tuple[SL10RepairReviewOutput, StageResultMeta]:
        meta = _meta(StageId.SL_10_REPAIR_REVIEW)
        return (
            SL10RepairReviewOutput(
                ok=True,
                decision="pass",
                target_resolved=True,
                regression_detected=False,
                drift_risk="minor",
                evidence=[{"summary": "Local scenario expectation is stale and conflicts with NL."}],
                local_override_rationale=[
                    f"Override scenario_regression for {scenario_name}: expected Pbat_dis=4.0 is stale; NL-grounded value is 3.0."
                ],
                review_meta=ReviewRunMeta(
                    provider="test-adapter",
                    model_id="none",
                    prompt_template_version="SL-10.test",
                    schema_validation_ok=True,
                    parsed_schema_version="test.v1",
                    failure_policy="audit_only",
                    replay_key="SL-10:test",
                ),
                meta=meta,
            ),
            meta,
        )

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-b1-stale-scenario-waiver",
            initial_dsl="initial-needs-review",
            max_iterations=3,
            adapters=_adapters_with(
                scenario_generate=scenario_generate,
                sim=sim,
                model_review=model_review,
                repair=repair,
                repair_review=local_review,
                sl10_review=sl10_review,
            ),
        )
    )

    assert record.status == "success"
    assert record.final_artifacts["verdict"] == "success"
    assert sim_calls[-1] == final_candidate
    assert any(payload.get("waiver_audit", {}).get("kind") == "stale_overridden_scenario_waiver" for payload in model_review_payloads)
    assert record.iteration_records[-1]["waiver_continue"] is True
    assert record.iteration_records[-1]["waiver_audit"]["kind"] == "stale_overridden_scenario_waiver"
    assert record.iteration_records[-1]["post_waiver_selected_feedback"] is None
    assert record.iteration_records[-1]["post_waiver_stage_ids"] == [
        StageId.SD_6_SIM.value,
        StageId.SL_7_MODEL_REVIEW.value,
    ]
    stale_envelope = record.iteration_records[-1]["waiver_entry_envelope"]
    assert stale_envelope["tail_start_stage"] == StageId.SD_6_SIM.value
    assert stale_envelope["tail_kind"] == "stale_overridden_scenario_waiver"
    assert stale_envelope["waiver_audit_kind"] == "stale_overridden_scenario_waiver"
    assert stale_envelope["graph_state_iteration"] == stale_envelope["iteration"]
    assert stale_envelope["repair_patch"]["waiver_audit"]["kind"] == "stale_overridden_scenario_waiver"
    assert stale_envelope["validation_ref"]
    assert stale_envelope["validation_source"]["object_type"] == "_ValidationPass"
    assert stale_envelope["validation_source"]["selected_feedback"]["source_stage"] == StageId.SD_6_SIM.value
    assert stale_envelope["validation_scenario_epoch"] is not None
    sl9_all_rejected = [entry for entry in record.fix_log if entry["phase"] == "sl9_all_rejected"]
    assert sl9_all_rejected and sl9_all_rejected[-1]["next_action"] == "continue_after_waiver"
    trace_nodes = _lg_trace_nodes(record)
    post_waiver_nodes = trace_nodes[trace_nodes.index("waiver_continue") + 1 :]
    assert "waiver_subgraph_enter" in post_waiver_nodes
    assert "waiver_tail_decision" in post_waiver_nodes
    assert "waiver_sim_tail" in post_waiver_nodes
    assert "waiver_subgraph_finalize" in post_waiver_nodes
    assert "validation_sd6_sim" in post_waiver_nodes
    assert "validation_sl7_model_review" in post_waiver_nodes
    assert "validation_sd2_parse" not in post_waiver_nodes
    assert any(
        item.get("event") == "stage_result"
        and item.get("stage_id") == StageId.SD_6_SIM.value
        and item.get("reason") == "stale_overridden_scenario_waiver_marked_non_blocking_for_SL-7"
        for item in record.logs
        if isinstance(item, dict)
    )



def test_langgraph_sl10_rework_gets_same_batch_retry_on_last_iteration(tmp_path: Path) -> None:
    repair_calls: list[RepairRequest] = []
    sl10_calls: list[RepairRequest] = []

    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        if context.current_dsl == "lg-last-iter-rework":
            item = DesignDiagnosticItem(
                code="W_LG_LAST_ITER_REWORK",
                pyfcstm_severity="warning",
                policy_action="budgeted_repair",
                instance_key="W_LG_LAST_ITER_REWORK:state=Idle",
                rationale="force repair on the only LangGraph global iteration",
            )
            return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)
        return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)

    def repair(request: RepairRequest) -> dict[str, Any]:
        repair_calls.append(request)
        assert request.fix_request_batch is not None
        candidate = "lg-candidate-a" if len(repair_calls) == 1 else "lg-candidate-b"
        return {
            "decisions": [
                {"request_id": item.request_id, "decision": "accept", "rationale": "accept for test"}
                for item in request.fix_request_batch.requests
            ],
            "candidate_dsl": candidate,
            "repair_rationale": [f"emit {candidate}"],
            "diff_summary": {"summary": f"emit {candidate}"},
        }

    def repair_review(request: RepairRequest) -> tuple[RepairReviewFeedback, StageResultMeta]:
        meta = _meta(StageId.SD_10_REPAIR_REVIEW)
        return RepairReviewFeedback(ok=True, target_resolved=True, regression_detected=False, drift_risk="none", meta=meta), meta

    def sl10_review(request: RepairRequest, _local_review: RepairReviewFeedback) -> tuple[SL10RepairReviewOutput, StageResultMeta]:
        sl10_calls.append(request)
        if len(sl10_calls) == 1:
            meta = _meta(StageId.SL_10_REPAIR_REVIEW, ok=False)
            return (
                SL10RepairReviewOutput(
                    ok=False,
                    decision="rework",
                    target_resolved=False,
                    regression_detected=True,
                    drift_risk="major",
                    evidence=[{"summary": "first candidate needs rework"}],
                    rework_instructions=["Use same-batch rework to restore the dropped obligation."],
                    review_meta=ReviewRunMeta(
                        provider="test-adapter",
                        model_id="none",
                        prompt_template_version="SL-10.test",
                        schema_validation_ok=True,
                        parsed_schema_version="test.v1",
                        failure_policy="audit_only",
                        replay_key="SL-10:test-lg-rework",
                    ),
                    meta=meta,
                ),
                meta,
            )
        meta = _meta(StageId.SL_10_REPAIR_REVIEW)
        return (
            SL10RepairReviewOutput(
                ok=True,
                decision="pass",
                target_resolved=True,
                regression_detected=False,
                drift_risk="none",
                evidence=[{"summary": "second candidate follows rework guidance"}],
                review_meta=ReviewRunMeta(
                    provider="test-adapter",
                    model_id="none",
                    prompt_template_version="SL-10.test",
                    schema_validation_ok=True,
                    parsed_schema_version="test.v1",
                    failure_policy="audit_only",
                    replay_key="SL-10:test-lg-pass",
                ),
                meta=meta,
            ),
            meta,
        )

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-b1-last-iteration-sl10-rework-minimum",
            initial_dsl="lg-last-iter-rework",
            max_iterations=1,
            adapters=_adapters_with(design=design, repair=repair, repair_review=repair_review, sl10_review=sl10_review),
        )
    )

    assert len(repair_calls) == 2
    assert repair_calls[1].rework_locked is True
    assert "Use same-batch rework" in str(repair_calls[1].repair_memory)
    assert len(sl10_calls) == 2
    assert record.repair_history[-1]["accepted"] is True
    assert record.repair_history[-1]["rework_attempt"] == 1
    assert record.iteration_records[0]["rework_attempts_used"] == 2
    assert record.status == "success"
    assert record.final_artifacts["verdict"] == "success"
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SL_7_MODEL_REVIEW.value
    assert record.iteration_records[0]["budget_gate"]["post_accept_validation_attempted"] is True
    assert record.iteration_records[0]["budget_gate"]["post_accept_validation_success"] is True
    assert record.iteration_records[0]["post_accept_selected_feedback"] is None
    stage_ids = _record_stage_ids(record)
    sc11_index = stage_ids.index(StageId.SC_11_ACCEPT_CANDIDATE.value)
    sc12_index = stage_ids.index(StageId.SC_12_EXIT.value)
    assert stage_ids.index(StageId.SD_2_PARSE.value, sc11_index + 1) < sc12_index
    assert record.run_config["min_sl10_rework_attempts"] == 1
    assert record.run_config["graph_config_hash"] == record.environment["graph_config_hash"]
    assert record.stage_records[-2]["stage_id"] == StageId.SC_12_EXIT.value
    assert [entry["phase"] for entry in record.fix_log].count("sl9_rework_decision") == 1
    assert [entry["phase"] for entry in record.fix_log].count("sl10_rework_review") == 1


def test_langgraph_sc11_last_iteration_runs_post_accept_validation_before_success(tmp_path: Path) -> None:
    parse_seen: list[str] = []

    def parse(dsl: str, context: StageContext) -> tuple[ParseFeedback, StageResultMeta]:
        parse_seen.append(dsl)
        return _ok_parse(dsl, context)

    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        if context.current_dsl == "lg-needs-post-accept":
            item = DesignDiagnosticItem(
                code="W_LG_POST_ACCEPT",
                pyfcstm_severity="warning",
                policy_action="budgeted_repair",
                instance_key="W_LG_POST_ACCEPT:state=Idle",
                rationale="force accepted repair in last iteration",
            )
            return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)
        return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)

    def repair(request: RepairRequest) -> dict[str, Any]:
        assert request.fix_request_batch is not None
        return {
            "decisions": [
                {"request_id": item.request_id, "decision": "accept", "rationale": "accept post-accept repair"}
                for item in request.fix_request_batch.requests
            ],
            "candidate_dsl": "lg-post-accepted-fixed",
            "repair_rationale": ["produce post-accepted fixed candidate"],
        }

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-b1-post-accept-success",
            initial_dsl="lg-needs-post-accept",
            max_iterations=1,
            adapters=_adapters_with(parse=parse, design=design, repair=repair),
        )
    )

    assert parse_seen == ["lg-needs-post-accept", "lg-post-accepted-fixed"]
    assert record.status == "success"
    assert record.final_artifacts["verdict"] == "success"
    assert record.iteration_records[0]["budget_gate"]["post_accept_validation_attempted"] is True
    assert record.iteration_records[0]["budget_gate"]["post_accept_validation_success"] is True
    assert record.iteration_records[0]["exit_reason"] == "full_pass_all_required_feedback_ok_after_sc11_post_accept_validation"
    assert record.iteration_records[0]["post_accept_selected_feedback"] is None
    assert StageId.SD_2_PARSE.value in record.iteration_records[0]["post_accept_stage_ids"]
    trace_nodes = _lg_trace_nodes(record)
    assert trace_nodes.count("validation_subgraph") >= 2
    assert "repair_decision" in trace_nodes


def test_langgraph_sc11_last_iteration_records_post_accept_failure_contract(tmp_path: Path) -> None:
    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        item = DesignDiagnosticItem(
            code="W_LG_POST_ACCEPT_FAIL",
            pyfcstm_severity="warning",
            policy_action="budgeted_repair",
            instance_key="W_LG_POST_ACCEPT_FAIL:state=Idle",
            rationale=f"force accepted repair and then keep blocking after candidate={context.current_dsl}",
        )
        return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)

    def repair(request: RepairRequest) -> dict[str, Any]:
        assert request.fix_request_batch is not None
        return {
            "decisions": [
                {"request_id": item.request_id, "decision": "accept", "rationale": "accept but leave post-accept blocker"}
                for item in request.fix_request_batch.requests
            ],
            "candidate_dsl": "lg-post-accepted-but-still-blocked",
            "repair_rationale": ["exercise post-accept failure branch"],
        }

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-b2-post-accept-failure",
            initial_dsl="lg-needs-post-accept-failure",
            max_iterations=1,
            adapters=_adapters_with(design=design, repair=repair),
        )
    )

    assert record.status == "budget_exhausted"
    assert record.final_artifacts["verdict"] == "not_converged"
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SD_4_DESIGN.value
    assert record.iteration_records[0]["budget_gate"]["post_accept_validation_attempted"] is True
    assert record.iteration_records[0]["budget_gate"]["post_accept_validation_success"] is False
    assert record.iteration_records[0]["post_accept_selected_feedback"]["source_stage"] == StageId.SD_4_DESIGN.value
    assert record.iteration_records[0]["post_accept_stage_ids"] == [
        StageId.SD_2_PARSE.value,
        StageId.SD_3_SEMANTIC.value,
        StageId.SD_4_DESIGN.value,
    ]
    assert record.environment["checkpoint_backend"] == "memory"
    assert record.environment["checkpoint_resume_smoke"]["real_agent_loop_resume_supported"] is False

    trace_nodes = _lg_trace_nodes(record)
    assert trace_nodes.count("validation_subgraph") >= 2
    assert "repair_path" in trace_nodes
    assert "repair_decision" in trace_nodes
    repair_runtime_trace = record.final_artifacts["langgraph_runtime_trace"]["repair_subgraph_runtime_trace"]
    assert "repair_path" not in repair_runtime_trace["node_ids"]
    assert "repair_decision" not in repair_runtime_trace["node_ids"]
    assert repair_runtime_trace["stage_node_ids"] == [
        "repair_sd8_fix_requests",
        "repair_sl9_repair",
        "repair_sl10_review",
        "repair_sc11_accept_candidate",
    ]

def test_sl10_noop_override_waiver_continues_without_sc11_budget(tmp_path: Path) -> None:
    scenario_name = "lg_b1_noop_override_scenario"
    current_candidate = "noop-accepted-candidate"
    model_review_payloads: list[dict[str, Any]] = []

    scenario = TestScenario(
        name=scenario_name,
        description="local oracle expects de-alarm even though SL-10 overrides it as NL-conflicting",
        initial_state="Root.Fault",
        steps=[
            ScenarioStep(
                events=["fallback"],
                expected_state="Root.Manual",
                expected_vars={"alarm_signal": 0},
                name="fallback_keeps_alarm_oracle",
            )
        ],
    )

    def scenario_generate(_request: ScenarioGenerationRequest) -> list[TestScenario]:
        return [scenario]

    def sim(_dsl: str, scenarios_or_set: Any, _context: StageContext) -> tuple[SimFeedback, StageResultMeta]:
        scenarios = list(getattr(scenarios_or_set, "scenarios", []) or [])
        failed = ScenarioResult(
            name=scenario_name,
            description=scenario.description,
            status="fail",
            step_results=[
                StepResult(
                    step_index=0,
                    step_name="fallback_keeps_alarm_oracle",
                    status="fail",
                    actual_state="Root.Manual",
                    actual_vars={"alarm_signal": 1},
                    state_assertion_ok=True,
                    var_assertion_ok=False,
                    var_mismatches={"alarm_signal": {"expected": 0, "actual": 1}},
                )
            ],
        )
        return (
            SimFeedback(ok=False, n_scenarios=len(scenarios), n_scenarios_passed=0, scenario_results=[failed]),
            _meta(StageId.SD_6_SIM, ok=False),
        )

    def repair(request: RepairRequest) -> dict[str, Any]:
        assert request.fix_request_batch is not None
        return {
            "decisions": [
                {
                    "request_id": item.request_id,
                    "decision": "accept",
                    "rationale": "Accept no-op because SL-10 must audit the local alarm oracle against NL/FixLog.",
                }
                for item in request.fix_request_batch.requests
            ],
            "candidate_dsl": current_candidate,
            "repair_rationale": ["no DSL edit; request needs SL-10 override audit"],
            "diff_summary": {"n_diff_lines": 0, "summary": "no-op candidate"},
        }

    def local_review(_request: RepairRequest) -> tuple[RepairReviewFeedback, StageResultMeta]:
        rejection = RepairRejection(
            rejected_by_stage=StageId.SD_10_REPAIR_REVIEW.value,
            reason="scenario_regression",
            target_resolved=False,
            regression_detected=True,
            drift_risk="major",
            evidence=[{"kind": "scenario_regression", "scenario_names": [scenario_name]}],
        )
        meta = _meta(StageId.SD_10_REPAIR_REVIEW, ok=False)
        return (
            RepairReviewFeedback(
                ok=False,
                target_resolved=False,
                regression_detected=True,
                drift_risk="major",
                local_rejection=rejection,
                meta=meta,
            ),
            meta,
        )

    def sl10_review(_request: RepairRequest, _local: RepairReviewFeedback) -> tuple[SL10RepairReviewOutput, StageResultMeta]:
        meta = _meta(StageId.SL_10_REPAIR_REVIEW)
        return (
            SL10RepairReviewOutput(
                ok=True,
                decision="pass",
                target_resolved=True,
                regression_detected=False,
                drift_risk="minor",
                evidence=[{"summary": "Local alarm oracle is stale; NL requires alarm to stay active until explicit fault removal."}],
                local_override_rationale=[
                    f"Override scenario_regression for {scenario_name}: expected alarm_signal=0 is stale; actual alarm_signal=1 is NL-grounded while fault remains active."
                ],
                review_meta=ReviewRunMeta(
                    provider="test-adapter",
                    model_id="none",
                    prompt_template_version="SL-10.test",
                    schema_validation_ok=True,
                    parsed_schema_version="test.v1",
                    failure_policy="audit_only",
                    replay_key="SL-10:test-noop",
                ),
                meta=meta,
            ),
            meta,
        )

    def model_review(_dsl: str, _context: StageContext, feedback: dict[str, Any]) -> tuple[ModelReviewFeedback, StageResultMeta]:
        model_review_payloads.append(feedback)
        meta = _meta(StageId.SL_7_MODEL_REVIEW)
        return (
            ModelReviewFeedback(
                ok=True,
                decision="pass",
                risk_level="none",
                findings=[{"id": "MR-noop-waiver", "summary": "SL-10 no-op override waiver reviewed"}]
                if feedback.get("waiver_audit")
                else [],
                meta=meta,
            ),
            meta,
        )

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-b1-sl10-noop-override-waiver",
            initial_dsl=current_candidate,
            max_iterations=1,
            adapters=_adapters_with(
                scenario_generate=scenario_generate,
                sim=sim,
                repair=repair,
                repair_review=local_review,
                sl10_review=sl10_review,
                model_review=model_review,
            ),
        )
    )

    assert record.status == "success"
    assert record.final_artifacts["verdict"] == "success"
    assert any(payload.get("waiver_audit", {}).get("kind") == "sl10_noop_override_waiver" for payload in model_review_payloads)
    assert record.iteration_records[0]["waiver_continue"] is True
    assert record.iteration_records[0]["accepted_noop_override"] is True
    assert record.iteration_records[0]["waiver_audit"]["kind"] == "sl10_noop_override_waiver"
    assert record.iteration_records[0]["post_waiver_selected_feedback"] is None
    assert record.iteration_records[0]["post_waiver_stage_ids"] == [
        StageId.SD_6_SIM.value,
        StageId.SL_7_MODEL_REVIEW.value,
    ]
    noop_envelope = record.iteration_records[0]["waiver_entry_envelope"]
    assert noop_envelope["tail_start_stage"] == StageId.SD_6_SIM.value
    assert noop_envelope["tail_kind"] == "sl10_noop_override_waiver"
    assert noop_envelope["waiver_audit_kind"] == "sl10_noop_override_waiver"
    assert noop_envelope["graph_state_iteration"] == 0
    assert noop_envelope["repair_patch"]["accepted_noop_override"] is True
    assert noop_envelope["repair_patch"]["waiver_audit"]["kind"] == "sl10_noop_override_waiver"
    assert noop_envelope["validation_source"]["selected_feedback"]["source_stage"] == StageId.SD_6_SIM.value
    trace_nodes = _lg_trace_nodes(record)
    post_waiver_nodes = trace_nodes[trace_nodes.index("waiver_continue") + 1 :]
    assert "waiver_sim_tail" in post_waiver_nodes
    assert "validation_sd2_parse" not in post_waiver_nodes
    assert "SC-11 budget gate" not in str(record.iteration_records[0].get("exit_reason"))
    assert any(entry["phase"] == "sl10_noop_override_waiver" and entry["next_action"] == "continue_after_waiver" for entry in record.fix_log)
    assert any(
        item.get("event") == "stage_result"
        and item.get("stage_id") == StageId.SD_6_SIM.value
        and item.get("reason") == "sl10_noop_override_waiver_marked_non_blocking_for_SL-7"
        for item in record.logs
        if isinstance(item, dict)
    )


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
    assert "waiver_subgraph_enter" in trace_nodes
    assert "waiver_tail_decision" in trace_nodes
    assert "waiver_design_tail" in trace_nodes
    assert "validation_subgraph" in trace_nodes
    assert "validation_sl5_scenario_generation" in trace_nodes
    assert trace_nodes.count("waiver_subgraph_enter") == 1
    assert trace_nodes.count("waiver_tail_decision") == 1
    assert trace_nodes.count("waiver_design_tail") == 1
    assert trace_nodes.count("validation_subgraph") == 1
    assert trace_nodes.count("validation_sl5_scenario_generation") == 1
    assert trace_nodes[-1] == "sc13_trace_audit"
    assert record.status == "invalid"
    assert record.final_artifacts["verdict"] == "invalid"
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SL_5_SCENARIO_GENERATION.value
    assert record.iteration_records[-1]["exit_reason"].startswith(f"{StageId.SL_5_SCENARIO_GENERATION.value} retry exhausted")
    envelope = record.iteration_records[-1]["waiver_entry_envelope"]
    assert envelope["schema_version"] == "lg-b3.waiver-entry-envelope.v1"
    assert envelope["tail_kind"] == "design_warning_waiver"
    assert envelope["tail_start_stage"] == StageId.SD_4_DESIGN.value
    assert envelope["repair_patch"]["waiver_continue"] is True
    assert envelope["validation_ref"]
    waiver_runtime_trace = record.final_artifacts["langgraph_runtime_trace"]["waiver_subgraph_runtime_trace"]
    assert "waiver_subgraph_enter" in waiver_runtime_trace["node_ids"]
    assert "waiver_design_tail" in waiver_runtime_trace["node_ids"]
    assert waiver_runtime_trace["nested_subgraph_ids"] == ["validation_subgraph"]
    waiver_trace_nodes = [
        item
        for item in record.run_config.get("langgraph_node_trace", [])
        if str(item.get("node_id") or "")
        in {"waiver_subgraph_enter", "waiver_tail_decision", "waiver_design_tail", "waiver_sim_tail", "waiver_subgraph_finalize"}
    ]
    waiver_operator_node_events = [
        event
        for event in _read_operator_events(record)
        if event.get("event_type") in {"subgraph_enter", "node_enter", "subgraph_exit"}
        and event.get("node") in {"waiver_subgraph_enter", "waiver_tail_decision", "waiver_design_tail", "waiver_sim_tail", "waiver_subgraph_finalize"}
    ]
    assert [item["node_id"] for item in waiver_trace_nodes] == [event["node"] for event in waiver_operator_node_events]
    assert len(waiver_operator_node_events) == waiver_runtime_trace["node_trace_count"]
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

# PR-LG-D1 Streaming + operator log contract tests.


def test_lg_d1_operator_event_schema_is_jsonl_safe() -> None:
    from method.langgraph_runtime import LG_D1_OPERATOR_EVENT_SCHEMA_VERSION, build_lg_d1_operator_event

    event = build_lg_d1_operator_event(
        run_id="lg-d1-schema",
        event_type="llm_stream_progress",
        node="sl1_initial_modeling",
        stage_id=StageId.SL_1_INITIAL_MODELING.value,
        payload={
            "chunk_count": 3,
            "completion_chars": 42,
            "prompt": "MUST_NOT_APPEAR",
            "messages": [{"role": "user", "content": "MUST_NOT_APPEAR"}],
            "raw_output": "MUST_NOT_APPEAR",
            "delta_text": "MUST_NOT_APPEAR",
            "headers": {"Authorization": "Bearer MUST_NOT_APPEAR"},
            "api_key": "MUST_NOT_APPEAR",
        },
    )

    assert event["schema_version"] == LG_D1_OPERATOR_EVENT_SCHEMA_VERSION
    assert event["run_id"] == "lg-d1-schema"
    assert event["event_type"] == "llm_stream_progress"
    assert event["timestamp"]
    assert event["node"] == "sl1_initial_modeling"
    assert event["stage_id"] == StageId.SL_1_INITIAL_MODELING.value
    assert event["instrumentation_layer"] == "langgraph_streaming"
    assert event["payload_hash"].startswith("sha256:")
    assert event["payload"]["chunk_count"] == 3
    assert event["payload"]["completion_chars"] == 42
    assert event["payload"]["omitted_raw_content_field_count"] >= 5
    encoded = json.dumps(event, ensure_ascii=False, sort_keys=True, allow_nan=False)
    assert "MUST_NOT_APPEAR" not in encoded
    _assert_no_forbidden_operator_keys(event)


def test_lg_d1_llm_progress_event_uses_allowlist_for_raw_chunk_shapes() -> None:
    from method.langgraph_runtime import build_lg_d1_operator_event

    event = build_lg_d1_operator_event(
        run_id="lg-d1-no-raw-chunk",
        event_type="llm_stream_progress",
        payload={
            "chunk_count": 3,
            "completion_chars": 42,
            "elapsed_seconds": 1.5,
            "content": "RAW_PROMPT_OR_CHUNK_SHOULD_NOT_BE_HERE",
            "choices": [{"delta": {"content": "RAW_DELTA_SHOULD_NOT_BE_HERE"}}],
            "response_text": "RAW_OUTPUT_SHOULD_NOT_BE_HERE",
            "safe_count_but_not_allowlisted": 99,
        },
    )

    encoded = json.dumps(event, ensure_ascii=False, sort_keys=True, allow_nan=False)
    assert event["payload"]["chunk_count"] == 3
    assert event["payload"]["completion_chars"] == 42
    assert event["payload"]["elapsed_seconds"] == 1.5
    assert event["payload"]["omitted_raw_content_field_count"] >= 4
    assert "RAW_PROMPT_OR_CHUNK_SHOULD_NOT_BE_HERE" not in encoded
    assert "RAW_DELTA_SHOULD_NOT_BE_HERE" not in encoded
    assert "RAW_OUTPUT_SHOULD_NOT_BE_HERE" not in encoded
    assert "safe_count_but_not_allowlisted" not in encoded
    _assert_no_forbidden_operator_keys(event)


def test_lg_d1_generic_operator_event_sanitizes_raw_chunk_and_token_like_fields() -> None:
    from method.langgraph_runtime import build_lg_d1_operator_event

    event = build_lg_d1_operator_event(
        run_id="lg-d1-generic-no-raw",
        event_type="node_enter",
        payload={
            "node_ok": "validation_pass",
            "raw_chunk": "RAW_CHUNK_LEAK_GENERIC",
            "nested": {
                "content": "RAW_CONTENT_LEAK_GENERIC",
                "choices": [{"delta": {"content": "RAW_DELTA_LEAK_GENERIC"}}],
                "safe_secret_note": "this field name includes secret and should be omitted",
            },
            "apiKey": "camelCase secret key maybe not key-matched",
            "token_value": "secret-token-string",
            "bearer": "Bearer abcdefghijklmnopqrstuvwxyz",
        },
    )

    encoded = json.dumps(event, ensure_ascii=False, sort_keys=True, allow_nan=False)
    assert event["payload"]["node_ok"] == "validation_pass"
    assert event["payload"]["omitted_raw_content_field_count"] >= 7
    for needle in (
        "RAW_CHUNK_LEAK_GENERIC",
        "RAW_CONTENT_LEAK_GENERIC",
        "RAW_DELTA_LEAK_GENERIC",
        "secret-token-string",
        "Bearer abcdefghijklmnopqrstuvwxyz",
        "camelCase secret key maybe not key-matched",
    ):
        assert needle not in encoded
    _assert_no_forbidden_operator_keys(event)


def test_lg_d1_stream_empty_after_side_effect_does_not_invoke_twice() -> None:
    from method.langgraph_runtime import _run_graph_with_lg_d1_stream

    class EmptyAfterSideEffectApp:
        def __init__(self) -> None:
            self.llm_calls = 0

        def stream(self, _initial_state: dict[str, Any], *, config: dict[str, Any], stream_mode: str):  # noqa: ANN201
            assert stream_mode == "updates"
            assert config["configurable"]["thread_id"] == "lg-d1-no-replay"
            self.llm_calls += 1
            if False:
                yield {"node": {"runtime_result": "unreachable"}}

        def get_state(self, _config: dict[str, Any]) -> Any:
            class Checkpoint:
                values: dict[str, Any] = {}

            return Checkpoint()

        def invoke(self, _initial_state: dict[str, Any], *, config: dict[str, Any]) -> dict[str, Any]:
            self.llm_calls += 1
            return {"runtime_result": "must-not-be-called", "operator_events": [], "config": config}

    app = EmptyAfterSideEffectApp()

    try:
        _run_graph_with_lg_d1_stream(
            app,
            initial_state={"operator_events": [], "operator_stream_enabled": True, "run_id": "lg-d1-no-replay"},
            run_id="lg-d1-no-replay",
            operator_stream_enabled=True,
        )
    except RuntimeError as exc:
        assert "refusing fallback invoke" in str(exc)
    else:  # pragma: no cover - failure path documents the expected guard.
        raise AssertionError("empty stream after side effects must fail loud instead of replaying invoke")

    assert app.llm_calls == 1


def test_lg_d1_stream_typeerror_after_side_effect_does_not_invoke_twice() -> None:
    from method.langgraph_runtime import _run_graph_with_lg_d1_stream

    class TypeErrorAfterSideEffectApp:
        def __init__(self) -> None:
            self.stream_calls = 0
            self.invoke_calls = 0
            self.side_effects: list[str] = []

        def stream(self, _initial_state: dict[str, Any], *, config: dict[str, Any], stream_mode: str) -> Any:
            assert stream_mode == "updates"
            assert config["configurable"]["thread_id"] == "lg-d1-typeerror-no-replay"
            self.stream_calls += 1
            self.side_effects.append("stream-side-effect-before-typeerror")
            raise TypeError("simulated TypeError after stream side effect")

        def invoke(self, _initial_state: dict[str, Any], *, config: dict[str, Any]) -> dict[str, Any]:
            self.invoke_calls += 1
            self.side_effects.append("invoke-side-effect")
            return {"runtime_result": "must-not-be-called", "operator_events": [], "config": config}

    app = TypeErrorAfterSideEffectApp()

    try:
        _run_graph_with_lg_d1_stream(
            app,
            initial_state={"operator_events": [], "operator_stream_enabled": True, "run_id": "lg-d1-typeerror-no-replay"},
            run_id="lg-d1-typeerror-no-replay",
            operator_stream_enabled=True,
        )
    except RuntimeError as exc:
        assert "stream setup failed with TypeError" in str(exc)
        assert "refusing fallback invoke" in str(exc)
    else:  # pragma: no cover - failure path documents the expected guard.
        raise AssertionError("TypeError after stream setup side effects must fail loud instead of replaying invoke")

    assert app.stream_calls == 1
    assert app.invoke_calls == 0
    assert app.side_effects == ["stream-side-effect-before-typeerror"]


def test_lg_d1_stream_off_preserves_run_record_and_result(tmp_path: Path) -> None:
    on_record = _lg_record(
        _run_langgraph_mock(
            tmp_path / "on",
            run_id="lg-d1-stream-on",
            adapters=_adapters_with(initial_modeling=_initial_modeling_llm_run_with_stream_usage),
        )
    )
    from method.langgraph_runtime import run_full_staged_langgraph_runtime

    off_result = run_full_staged_langgraph_runtime(
        "LG-D1 stream-off control should preserve academic evidence.",
        config=LoopConfig(
            condition_id="lg-d1-stream-off",
            condition_family="test_profile",
            base_condition_id="full_staged_v1",
            changed_factors=["llm_provider_mode=mock", "lg_d1_stream_off_contract"],
            llm_provider_mode="mock",
            academic_question="test-only LG-D1 stream-off equivalence; excluded from main results",
            output_dir=str(tmp_path / "off"),
            run_id="lg-d1-stream-off",
            max_iterations=1,
            compatibility_mode="langgraph_stategraph",
        ),
        initial_dsl=_stable_dsl(),
        adapters=_adapters_with(initial_modeling=_initial_modeling_llm_run_with_stream_usage),
        operator_stream_enabled=False,
    )
    off_record = _lg_record(off_result)

    assert on_record.status == off_record.status == "success"
    for key in ("verdict", "verdict_source_stage_id", "oracle_weak", "main_result_eligible", "exclusion_reason"):
        assert on_record.final_artifacts[key] == off_record.final_artifacts[key]
    assert _lg_baseline(on_record)["stage_ids"] == _lg_baseline(off_record)["stage_ids"]
    assert on_record.fix_log == off_record.fix_log
    assert len(on_record.llm_interactions) == len(off_record.llm_interactions)
    assert _canonical_hash(on_record.llm_interactions) == _canonical_hash(off_record.llm_interactions)
    assert "operator_log" in on_record.final_artifacts
    assert "operator_log" not in off_record.final_artifacts


def test_lg_d1_langgraph_stream_emits_node_stage_llm_and_terminal_events(tmp_path: Path) -> None:
    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-d1-stream-events",
            adapters=_adapters_with(initial_modeling=_initial_modeling_llm_run_with_stream_usage),
        )
    )
    events = _read_operator_events(record)
    event_types = [event["event_type"] for event in events]

    assert "node_enter" in event_types
    assert "node_exit" in event_types
    assert "stage_result" in event_types
    assert "llm_stream_progress" in event_types
    assert "terminal_verdict" in event_types
    assert any(event["node"] == "validation_pass" and event["event_type"] == "node_enter" for event in events)
    assert any(event["node"] == "sc13_trace_audit" and event["event_type"] == "terminal_verdict" for event in events)
    assert any(event["stage_id"] == StageId.SL_1_INITIAL_MODELING.value for event in events)
    assert all(event["instrumentation_layer"] == "langgraph_streaming" for event in events)
    _assert_no_forbidden_operator_keys(events)
    assert record.final_artifacts["operator_log"]["langgraph_stream_status"] == "enabled"
    assert record.final_artifacts["operator_log"]["operator_event_count"] == len(events)


def test_lg_d1_operator_log_tee_reconstructs_progress_summary(tmp_path: Path) -> None:
    from method.langgraph_runtime import reconstruct_lg_d1_stream_summary_from_jsonl

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-d1-summary",
            adapters=_adapters_with(initial_modeling=_initial_modeling_llm_run_with_stream_usage),
        )
    )
    operator = record.final_artifacts["operator_log"]
    summary = reconstruct_lg_d1_stream_summary_from_jsonl(operator["operator_log_path"])

    assert summary["schema_version"] == "lg-d1.stream-summary.v1"
    assert summary["run_id"] == record.run_id
    assert summary["node_sequence"] == _lg_trace_nodes(record)
    assert summary["stage_sequence"] == [row["stage_id"] for row in record.stage_records]
    assert summary["final_verdict"] == record.final_artifacts["verdict"]
    assert summary["run_record_path_hash"] == operator["run_record_path_hash"]
    assert summary["llm_stream_observed"] is True
    assert summary["llm_stream_chunk_count_total"] == 7

    summary_path = Path(operator["stream_summary_path"])
    assert summary_path.exists()
    on_disk = json.loads(summary_path.read_text(encoding="utf-8"))
    assert on_disk == summary
    import hashlib

    assert operator["stream_summary_hash"] == "sha256:" + hashlib.sha256(summary_path.read_bytes()).hexdigest()
    assert operator["stream_summary_payload_hash"] == _canonical_hash(summary)


def test_lg_d1_llm_stream_flag_not_regressed_for_real_env_config(monkeypatch) -> None:
    from method.langgraph_runtime import lg_d1_llm_stream_runtime_metadata

    monkeypatch.delenv("LLM_STREAM", raising=False)
    monkeypatch.delenv("LLM_STREAM_INCLUDE_USAGE", raising=False)
    metadata = lg_d1_llm_stream_runtime_metadata(real_llm_provider_api=True)

    assert metadata["llm_stream_required"] is True
    assert metadata["llm_stream_config_enabled"] is True
    assert metadata["llm_stream_include_usage_config_enabled"] is True
    assert metadata["llm_stream_observed"] is None
    assert metadata["llm_stream_observation_source"] == "pending_llm_interactions"


def test_lg_d1_instrumentation_does_not_replace_academic_evidence(tmp_path: Path) -> None:
    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-d1-evidence-layering",
            adapters=_adapters_with(initial_modeling=_initial_modeling_llm_run_with_stream_usage),
        )
    )
    operator = record.final_artifacts["operator_log"]

    assert record.stage_records
    assert record.llm_interactions
    assert record.final_artifacts["final_dsl"]
    assert record.final_artifacts["final_dsl_hash"].startswith("sha256:")
    assert record.final_artifacts["langgraph_runtime_trace"]["delegated_monolithic_runtime"] is False
    assert operator["instrumentation_layer"] == "langgraph_streaming"
    assert operator["does_not_replace_academic_evidence"] is True
    assert operator["academic_evidence_sources"] == [
        "AgentLoopRunRecord.stage_records",
        "AgentLoopRunRecord.llm_interactions",
        "AgentLoopRunRecord.fix_log",
        "AgentLoopRunRecord.scenario_history",
        "AgentLoopRunRecord.final_artifacts.final_dsl",
    ]
    assert "operator_log" not in record.replay_index


# PR-LG-B2 Repair subgraph contract tests.



def _blocking_design_feedback() -> tuple[DesignFeedback, StageResultMeta]:
    item = DesignDiagnosticItem(
        code="LG_B2_TEST_BLOCK",
        message="mock blocking design issue for repair subgraph contract",
        pyfcstm_severity="warning",
        instance_key="lg-b2-test-block",
        policy_action="hard_block",
    )
    return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)


def test_lg_b2_repair_finalize_missing_patch_fails_loud(monkeypatch: pytest.MonkeyPatch) -> None:
    import inspect
    import method.langgraph_runtime as lg

    class CapturingStateGraph:
        def __init__(self, *_args: Any, **_kwargs: Any) -> None:
            self.nodes: dict[str, Any] = {}

        def add_node(self, name: str, fn: Any) -> None:
            self.nodes[name] = fn

        def add_edge(self, *_args: Any, **_kwargs: Any) -> None:
            return None

        def compile(self, *_args: Any, **_kwargs: Any) -> "CapturingStateGraph":
            return self

    captured_graph = CapturingStateGraph()
    monkeypatch.setattr(lg, "StateGraph", lambda *_args, **_kwargs: captured_graph)

    lg._build_repair_subgraph(runtime_cfg=SimpleNamespace(), adapters=SimpleNamespace())
    with pytest.raises(RuntimeError, match="repair subgraph contract violation"):
        captured_graph.nodes["repair_finalize"](
            {
                "runtime_state": SimpleNamespace(),
                "iteration": 0,
                "run_id": "lg-b2-missing-repair-patch",
                "graph_trace": [],
                "operator_events": [],
            }
        )

    repair_subgraph_source = inspect.getsource(lg._build_repair_subgraph)
    assert "repair_finalize requires an explicit repair_patch" in repair_subgraph_source
    assert "fallback_reason" not in repair_subgraph_source


def test_lg_b2_repair_subgraph_registry_exposes_stage_level_nodes() -> None:
    from method.langgraph_runtime import build_langgraph_node_registry

    registry = build_langgraph_node_registry()
    repair_node = next(node for node in registry["nodes"] if node["node_id"] == "repair_path")

    assert repair_node["delegated_subgraph"] is True
    assert repair_node["subgraph_id"] == "repair_subgraph"
    assert {
        "repair_enter",
        "repair_sd8_fix_requests",
        "repair_sl9_repair",
        "repair_sl10_review",
        "repair_sc11_accept_candidate",
        "repair_finalize",
    }.issubset(set(repair_node["subgraph_node_ids"]))


def test_lg_b2_repair_subgraph_not_opaque_old_repair_path_wrapper() -> None:
    import inspect
    import method.langgraph_runtime as lg

    build_graph_source = inspect.getsource(lg._build_graph)
    repair_subgraph_source = inspect.getsource(lg._build_repair_subgraph)

    assert "_build_repair_subgraph" in build_graph_source
    assert "_run_repair_path" not in build_graph_source
    assert "_run_repair_path" not in repair_subgraph_source
    assert "return graph.compile(checkpointer=False)" in repair_subgraph_source
    assert "InMemorySaver(" not in repair_subgraph_source


def test_lg_b2_repair_subgraph_trace_exposes_sd8_sl9_sl10_sc11(tmp_path: Path) -> None:
    design_calls = {"count": 0}

    def design_then_ok(_context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        design_calls["count"] += 1
        if design_calls["count"] == 1:
            return _blocking_design_feedback()
        return _ok_design(_context)

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-b2-repair-subgraph-contract",
            adapters=_adapters_with(design=design_then_ok),
            max_iterations=2,
        )
    )
    trace_nodes = _lg_trace_nodes(record)
    repair_nodes = [node for node in trace_nodes if node.startswith("repair_")]

    assert "repair_enter" in repair_nodes
    assert "repair_sd8_fix_requests" in repair_nodes
    assert "repair_sl9_repair" in repair_nodes
    assert "repair_sl10_review" in repair_nodes
    assert "repair_sc11_accept_candidate" in repair_nodes
    assert "repair_finalize" in repair_nodes
    assert _record_stage_ids(record).count(StageId.SD_8_FIX_PLAN.value) == 1
    assert _record_stage_ids(record).count(StageId.SL_9_REPAIR.value) == 1
    assert _record_stage_ids(record).count(StageId.SL_10_REPAIR_REVIEW.value) == 1
    assert _record_stage_ids(record).count(StageId.SC_11_ACCEPT_CANDIDATE.value) == 1
    assert record.repair_history[0]["accepted"] is True
    repair_runtime_trace = record.final_artifacts["langgraph_runtime_trace"]["repair_subgraph_runtime_trace"]
    assert repair_runtime_trace["stage_node_ids"] == [
        "repair_sd8_fix_requests",
        "repair_sl9_repair",
        "repair_sl10_review",
        "repair_sc11_accept_candidate",
    ]
    assert "repair_path" not in repair_runtime_trace["node_ids"]
    assert "repair_decision" not in repair_runtime_trace["node_ids"]


def test_lg_b2_operator_log_maps_repair_stage_results_to_subgraph_nodes(tmp_path: Path) -> None:
    design_calls = {"count": 0}

    def design_then_ok(_context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        design_calls["count"] += 1
        if design_calls["count"] == 1:
            return _blocking_design_feedback()
        return _ok_design(_context)

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-b2-operator-stage-node-attribution",
            adapters=_adapters_with(design=design_then_ok),
            max_iterations=2,
        )
    )
    events = _read_operator_events(record)
    repair_stage_results = [
        event
        for event in events
        if event["event_type"] == "stage_result"
        and event["stage_id"]
        in {
            StageId.SD_8_FIX_PLAN.value,
            StageId.SL_9_REPAIR.value,
            StageId.SL_10_REPAIR_REVIEW.value,
            StageId.SC_11_ACCEPT_CANDIDATE.value,
        }
    ]
    assert [(event["stage_id"], event["node"]) for event in repair_stage_results] == [
        (StageId.SD_8_FIX_PLAN.value, "repair_sd8_fix_requests"),
        (StageId.SL_9_REPAIR.value, "repair_sl9_repair"),
        (StageId.SL_10_REPAIR_REVIEW.value, "repair_sl10_review"),
        (StageId.SC_11_ACCEPT_CANDIDATE.value, "repair_sc11_accept_candidate"),
    ]
    for event in repair_stage_results:
        stage_flow = event["payload"]["stage_flow"]
        assert stage_flow["graph_subgraph"] == "repair_subgraph"
        assert stage_flow["graph_node"] == event["node"]
    assert repair_stage_results[1]["payload"]["stage_flow"]["decision_count"] == 1
    assert repair_stage_results[2]["payload"]["stage_flow"]["decision"] == "pass"
    assert "candidate_dsl_hash" in repair_stage_results[3]["payload"]["stage_flow"]


def test_lg_b2_repair_subgraph_runtime_trace_excludes_parent_repair_nodes(tmp_path: Path) -> None:
    design_calls = {"count": 0}

    def design_then_ok(_context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        design_calls["count"] += 1
        if design_calls["count"] == 1:
            return _blocking_design_feedback()
        return _ok_design(_context)

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-b2-repair-subgraph-trace-filter",
            adapters=_adapters_with(design=design_then_ok),
            max_iterations=2,
        )
    )
    all_trace_nodes = _lg_trace_nodes(record)
    assert "repair_path" in all_trace_nodes
    assert "repair_decision" in all_trace_nodes

    repair_runtime_trace = record.final_artifacts["langgraph_runtime_trace"]["repair_subgraph_runtime_trace"]
    assert repair_runtime_trace["node_ids"] == [
        "repair_enter",
        "repair_sd8_fix_requests",
        "repair_sl9_repair",
        "repair_sl10_review",
        "repair_sc11_accept_candidate",
        "repair_finalize",
    ]
    assert repair_runtime_trace["node_trace_count"] == len(repair_runtime_trace["node_ids"])


def test_lg_b2_repair_subgraph_rework_loop_is_visible_in_trace(tmp_path: Path) -> None:
    attempts = {"count": 0}
    design_calls = {"count": 0}

    def design_then_ok(_context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        design_calls["count"] += 1
        if design_calls["count"] == 1:
            return _blocking_design_feedback()
        return _ok_design(_context)

    def repair_adapter(_request: RepairRequest) -> str:
        attempts["count"] += 1
        return f"""
state Root {{
    state Idle{attempts['count']};
    [*] -> Idle{attempts['count']};
    Idle{attempts['count']} -> [*];
}}
"""

    def sl10_review_adapter(_request: RepairRequest, _local_review: RepairReviewFeedback) -> Any:
        decision = "rework" if attempts["count"] == 1 else "pass"
        return SimpleNamespace(
            stage_id=StageId.SL_10_REPAIR_REVIEW.value,
            ok=decision == "pass",
            parsed_output={"decision": decision},
            feedback=SL10RepairReviewOutput(
                ok=decision == "pass",
                decision=decision,
                target_resolved=decision == "pass",
                regression_detected=decision != "pass",
                drift_risk="none" if decision == "pass" else "minor",
                rework_instructions=[] if decision == "pass" else ["make the repair concrete"],
                evidence=[{"attempt": attempts["count"], "decision": decision}],
                review_meta=ReviewRunMeta(
                    provider="test-adapter",
                    model_id="none",
                    prompt_template_version="SL-10.lg-b2-test",
                    schema_validation_ok=True,
                    parsed_schema_version="SL10RepairReviewOutput.test.v1",
                    failure_policy="audit_only",
                    replay_key=f"SL-10:lg-b2:{decision}:{attempts['count']}",
                ),
                meta=_meta(StageId.SL_10_REPAIR_REVIEW, ok=decision == "pass"),
            ),
            stage_meta=_meta(StageId.SL_10_REPAIR_REVIEW, ok=decision == "pass"),
            interaction={"stage_id": StageId.SL_10_REPAIR_REVIEW.value, "schema_validation_ok": True},
        )

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-b2-rework-loop-visible",
            adapters=_adapters_with(
                design=design_then_ok,
                repair=repair_adapter,
                sl10_review=sl10_review_adapter,
            ),
            max_iterations=1,
        )
    )
    trace_nodes = _lg_trace_nodes(record)

    assert trace_nodes.count("repair_sl9_repair") == 2
    assert trace_nodes.count("repair_sl10_review") == 2
    assert "repair_sc11_accept_candidate" in trace_nodes
    assert record.repair_history[0]["sl10_repair_review"]["decision"] == "rework"
    assert record.repair_history[1]["sl10_repair_review"]["decision"] == "pass"
    assert record.run_config["graph_node_registry"]["nodes"]

# PR-LG-E3 fixed ToolNode wrapper contract tests.

def _lg_e3_tool_events(record: Any) -> list[dict[str, Any]]:
    trace = record.final_artifacts.get("toolnode_wrapper_trace") or {}
    events = trace.get("events") or []
    assert isinstance(events, list)
    return [event for event in events if isinstance(event, dict)]


def _lg_e3_tool_names(record: Any) -> list[str]:
    return [str(event.get("tool_name") or "") for event in _lg_e3_tool_events(record)]


def _canonical_without_lg_e3(record: Any) -> dict[str, Any]:
    """Canonical academic fields that LG-E3 instrumentation must not change."""

    return {
        "stage_records": record.stage_records,
        "deterministic_feedback": record.deterministic_feedback,
        "repair_history": record.repair_history,
        "fix_log": record.fix_log,
        "scenario_history": record.scenario_history,
        "final_artifacts": {
            key: value
            for key, value in record.final_artifacts.items()
            if key
            not in {
                "toolnode_wrapper_trace",
                "operator_log",
                "langgraph_runtime_trace",
                "transient_lifecycle",
                "lg_c1_graph_state_readiness",
            }
        },
        "status": record.status,
        "replay_index": record.replay_index,
    }


# PR-LG-C1 reducer + JSON-safe graph-state readiness contract tests.

def test_lg_c1_contract_declares_reducer_and_live_object_boundaries() -> None:
    from method.langgraph_runtime import (
        LG_C1_REDUCER_STATE_SCHEMA_VERSION,
        build_lg_c1_graph_state_contract,
    )

    contract = build_lg_c1_graph_state_contract()

    assert contract["schema_version"] == LG_C1_REDUCER_STATE_SCHEMA_VERSION
    assert contract["real_agent_loop_json_checkpoint_supported"] is False
    assert contract["checkpoint_serde_mode"] == "pickle_for_live_object_bridge_with_json_safe_reducer_channels"
    assert contract["does_not_replace_academic_evidence"] is True

    reducer_channels = set(contract["append_only_reducer_channel_names"])
    expected_reducer_channels = {
        "graph_trace",
        "operator_events",
        "toolnode_wrapper_events",
        "stage_record_events",
        "llm_interaction_events",
        "fix_log_events",
        "scenario_history_events",
        "repair_history_events",
    }
    assert expected_reducer_channels.issubset(reducer_channels)
    assert expected_reducer_channels.issubset(set(contract["json_safe_channel_names"]))

    live_channels = set(contract["live_object_channel_names"])
    assert {"runtime_state", "runtime_result", "validation_result", "repair_validation"}.issubset(live_channels)
    assert live_channels.isdisjoint(contract["json_safe_channel_names"])
    assert "runtime_state" in contract["pickle_required_channel_names"]
    assert "AgentLoopRunRecord.stage_records" in contract["academic_evidence_sources"]
    assert "AgentLoopRunRecord.fix_log" in contract["academic_evidence_sources"]


def test_lg_c1_append_only_reducer_merges_full_state_updates_without_duplicates() -> None:
    from method.langgraph_runtime import _lg_c1_append_only_reducer

    first = [{"entry_id": "1", "phase": "SD-8"}, {"entry_id": "2", "phase": "SL-9"}]
    full_state_update = [
        {"entry_id": "1", "phase": "SD-8"},
        {"entry_id": "2", "phase": "SL-9"},
        {"entry_id": "3", "phase": "SL-10"},
    ]
    merged = _lg_c1_append_only_reducer(first, full_state_update)

    assert merged == full_state_update
    assert _lg_c1_append_only_reducer(merged, full_state_update) == full_state_update


def test_lg_c1_run_record_has_json_safe_reducer_readiness_and_mirror_consistency(tmp_path: Path) -> None:
    record = _lg_record(_run_langgraph_mock(tmp_path, run_id="lg-c1-json-safe-mirror"))

    env = record.environment
    assert env["lg_c1_reducer_state_schema_version"] == "lg-c1.reducer-json-state.v1"
    assert env["checkpoint_serde_mode"] == "pickle_for_live_object_bridge_with_json_safe_reducer_channels"
    assert env["real_agent_loop_json_checkpoint_supported"] is False
    assert env["lg_c1_reducer_channel_count"] >= 8
    assert "runtime_state" in env["lg_c1_live_object_channel_names"]
    assert "stage_record_events" in env["lg_c1_json_safe_channel_names"]

    readiness = record.final_artifacts["lg_c1_graph_state_readiness"]
    assert readiness["schema_version"] == "lg-c1.reducer-json-state.v1"
    assert readiness["does_not_replace_academic_evidence"] is True
    assert readiness["final_reducer_channel_summaries"]["stage_record_events"]["count"] == len(record.stage_records)
    assert readiness["final_reducer_channel_summaries"]["llm_interaction_events"]["count"] == len(record.llm_interactions)
    assert readiness["final_reducer_channel_summaries"]["fix_log_events"]["count"] == len(record.fix_log)
    assert readiness["final_reducer_channel_summaries"]["scenario_history_events"]["count"] == len(record.scenario_history)
    assert readiness["final_reducer_channel_summaries"]["repair_history_events"]["count"] == len(record.repair_history)
    assert readiness["mirror_canonical_consistency"]["stage_records_match"] is True
    assert readiness["mirror_canonical_consistency"]["llm_interactions_match"] is True
    assert readiness["mirror_canonical_consistency"]["fix_log_match"] is True
    assert readiness["mirror_canonical_consistency"]["scenario_history_match"] is True
    assert readiness["mirror_canonical_consistency"]["repair_history_match"] is True
    assert readiness["json_serialization_audit"]["all_json_safe_reducer_channels_serializable"] is True
    assert readiness["academic_evidence_sources"] == env["lg_c1_academic_evidence_sources"]


def test_lg_c1_mirrors_non_empty_llm_interactions_without_replacing_evidence(tmp_path: Path) -> None:
    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-c1-llm-mirror",
            adapters=_adapters_with(initial_modeling=_initial_modeling_llm_run_with_stream_usage),
        )
    )

    readiness = record.final_artifacts["lg_c1_graph_state_readiness"]
    assert len(record.llm_interactions) == 1
    assert readiness["final_reducer_channel_summaries"]["llm_interaction_events"]["count"] == 1
    assert readiness["mirror_canonical_consistency"]["llm_interactions_match"] is True
    assert readiness["does_not_replace_academic_evidence"] is True
    assert record.final_artifacts["verdict"] == "success"


def test_lg_c1_mirrors_non_empty_fixlog_and_repair_history_without_reordering(tmp_path: Path) -> None:
    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        if context.current_dsl == "lg-c1-needs-repair":
            item = DesignDiagnosticItem(
                code="W_LG_C1_REPAIR",
                pyfcstm_severity="warning",
                policy_action="budgeted_repair",
                instance_key="W_LG_C1_REPAIR:state=Idle",
                rationale="force non-empty FixLog / repair_history for LG-C1 reducer mirror contract",
            )
            return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)
        return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)

    def repair(request: RepairRequest) -> dict[str, Any]:
        assert request.fix_request_batch is not None
        return {
            "decisions": [
                {"request_id": item.request_id, "decision": "accept", "rationale": "accept LG-C1 repair request"}
                for item in request.fix_request_batch.requests
            ],
            "candidate_dsl": _stable_dsl(),
            "repair_rationale": ["return stable DSL so the next validation pass converges"],
        }

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-c1-fixlog-repair-mirror",
            initial_dsl="lg-c1-needs-repair",
            adapters=_adapters_with(design=design, repair=repair),
            max_iterations=2,
        )
    )

    readiness = record.final_artifacts["lg_c1_graph_state_readiness"]
    assert record.final_artifacts["verdict"] == "success"
    assert len(record.fix_log) >= 1
    assert len(record.repair_history) >= 1
    assert readiness["final_reducer_channel_summaries"]["fix_log_events"]["count"] == len(record.fix_log)
    assert readiness["final_reducer_channel_summaries"]["repair_history_events"]["count"] == len(record.repair_history)
    assert readiness["mirror_canonical_consistency"]["fix_log_match"] is True
    assert readiness["mirror_canonical_consistency"]["repair_history_match"] is True
    assert [entry["phase"] for entry in record.fix_log] == [
        event["phase"] for event in readiness["final_reducer_channel_events"]["fix_log_events"]
    ]


def test_lg_e3_registry_declares_fixed_non_llm_toolnode_wrappers() -> None:
    from method.langgraph_runtime import build_lg_e3_toolnode_wrapper_registry

    registry = build_lg_e3_toolnode_wrapper_registry()

    assert registry["schema_version"] == "lg-e3.fixed-toolnode-wrapper.v1"
    assert registry["enabled_by_default"] is True
    assert registry["llm_tool_choice_exposed"] is False
    assert registry["fixed_invocation"] is True
    wrappers = {item["tool_name"]: item for item in registry["wrappers"]}
    expected = {
        "sd2_parse": StageId.SD_2_PARSE.value,
        "sd3_semantic": StageId.SD_3_SEMANTIC.value,
        "sd4_design": StageId.SD_4_DESIGN.value,
        "sd5a_scenario_coverage": StageId.SD_5A_SCENARIO_COVERAGE.value,
        "sc5f_freeze_scenario_set": StageId.SC_5F_SCENARIO_FREEZE.value,
        "sd6_sim": StageId.SD_6_SIM.value,
        "sd8_fix_plan": StageId.SD_8_FIX_PLAN.value,
        "sd10_repair_review_local_check": StageId.SD_10_REPAIR_REVIEW.value,
        "warning_repair_attempt_marker": "warning_budget_state",
    }
    assert set(expected).issubset(wrappers)
    for tool_name, stage_id in expected.items():
        row = wrappers[tool_name]
        assert row["stage_id"] == stage_id
        assert row["fixed_invocation"] is True
        assert row["llm_tool_choice_exposed"] is False
        assert row["does_not_replace_academic_evidence"] is True
        assert row["input_policy"] == "hash_and_safe_summary_only"
        assert row["output_policy"] == "hash_and_safe_summary_only"
    assert all("ABS" not in json.dumps(item, ensure_ascii=False) for item in registry["wrappers"])
    assert all("Elevator" not in json.dumps(item, ensure_ascii=False) for item in registry["wrappers"])
    assert all("CARA" not in json.dumps(item, ensure_ascii=False) for item in registry["wrappers"])
    assert all("LNG" not in json.dumps(item, ensure_ascii=False) for item in registry["wrappers"])


def test_lg_e3_success_path_records_fixed_tool_invocations_without_changing_canonical_evidence(tmp_path: Path) -> None:
    from method.langgraph_runtime import run_full_staged_langgraph_runtime

    cfg_base = dict(
        condition_family="test_profile",
        base_condition_id="full_staged_v1",
        changed_factors=["llm_provider_mode=mock", "lg_e3_toolnode_contract"],
        llm_provider_mode="mock",
        academic_question="test-only LG-E3 fixed ToolNode instrumentation; excluded from main results",
        max_iterations=1,
        compatibility_mode="langgraph_stategraph",
    )
    on = run_full_staged_langgraph_runtime(
        "LG-E3 wrappers must not change successful deterministic validation evidence.",
        config=LoopConfig(
            **cfg_base,
            condition_id="lg-e3-success-on",
            output_dir=str(tmp_path / "on"),
            run_id="lg-e3-success-on",
        ),
        initial_dsl=_stable_dsl(),
        adapters=_adapters(),
    )
    off = run_full_staged_langgraph_runtime(
        "LG-E3 wrappers must not change successful deterministic validation evidence.",
        config=LoopConfig(
            **cfg_base,
            condition_id="lg-e3-success-off",
            output_dir=str(tmp_path / "off"),
            run_id="lg-e3-success-off",
        ),
        initial_dsl=_stable_dsl(),
        adapters=_adapters(),
        toolnode_wrapper_enabled=False,
    )
    on_record = _lg_record(on)
    off_record = _lg_record(off)

    assert _canonical_hash(_canonical_without_lg_e3(on_record)) == _canonical_hash(_canonical_without_lg_e3(off_record))
    assert on_record.environment["lg_e3_toolnode_wrappers_enabled"] is True
    assert off_record.environment["lg_e3_toolnode_wrappers_enabled"] is False
    assert on_record.final_artifacts["toolnode_wrapper_trace"]["does_not_replace_academic_evidence"] is True
    tool_names = _lg_e3_tool_names(on_record)
    assert tool_names == [
        "sd2_parse",
        "sd3_semantic",
        "sd4_design",
        "sd5a_scenario_coverage",
        "sc5f_freeze_scenario_set",
        "sd6_sim",
    ]
    assert _lg_e3_tool_events(off_record) == []
    for event in _lg_e3_tool_events(on_record):
        assert event["schema_version"] == "lg-e3.fixed-toolnode-wrapper.v1"
        assert event["fixed_invocation"] is True
        assert event["llm_tool_choice_exposed"] is False
        assert event["input_hash"].startswith("sha256:")
        assert event["output_hash"].startswith("sha256:")
        assert "raw_input" not in event
        assert "raw_output" not in event


def test_lg_e3_repair_path_wraps_sd8_and_sd10_without_changing_fixlog(tmp_path: Path) -> None:
    from method.langgraph_runtime import run_full_staged_langgraph_runtime

    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        if context.current_dsl == "lg-e3-needs-repair":
            item = DesignDiagnosticItem(
                code="W_LG_E3_REPAIR",
                pyfcstm_severity="warning",
                policy_action="budgeted_repair",
                instance_key="W_LG_E3_REPAIR:state=Idle",
                rationale="force SD-8/SL-9/SD-10 repair path for LG-E3 contract",
            )
            return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)
        return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)

    def repair(request: RepairRequest) -> dict[str, Any]:
        assert request.fix_request_batch is not None
        return {
            "decisions": [
                {"request_id": item.request_id, "decision": "accept", "rationale": "accept LG-E3 repair request"}
                for item in request.fix_request_batch.requests
            ],
            "candidate_dsl": _stable_dsl(),
            "repair_rationale": ["return stable DSL so post-accept validation converges"],
        }

    cfg_base = dict(
        condition_family="test_profile",
        base_condition_id="full_staged_v1",
        changed_factors=["llm_provider_mode=mock", "lg_e3_repair_toolnode_contract"],
        llm_provider_mode="mock",
        academic_question="test-only LG-E3 repair path ToolNode instrumentation; excluded from main results",
        max_iterations=1,
        compatibility_mode="langgraph_stategraph",
    )
    adapters = _adapters_with(design=design, repair=repair)
    on = run_full_staged_langgraph_runtime(
        "LG-E3 wrappers must not change SD-8/SD-10 repair evidence.",
        config=LoopConfig(
            **cfg_base,
            condition_id="lg-e3-repair-on",
            output_dir=str(tmp_path / "on"),
            run_id="lg-e3-repair-on",
        ),
        initial_dsl="lg-e3-needs-repair",
        adapters=adapters,
    )
    off = run_full_staged_langgraph_runtime(
        "LG-E3 wrappers must not change SD-8/SD-10 repair evidence.",
        config=LoopConfig(
            **cfg_base,
            condition_id="lg-e3-repair-off",
            output_dir=str(tmp_path / "off"),
            run_id="lg-e3-repair-off",
        ),
        initial_dsl="lg-e3-needs-repair",
        adapters=adapters,
        toolnode_wrapper_enabled=False,
    )
    on_record = _lg_record(on)
    off_record = _lg_record(off)

    assert _canonical_hash(_canonical_without_lg_e3(on_record)) == _canonical_hash(_canonical_without_lg_e3(off_record))
    tool_names = _lg_e3_tool_names(on_record)
    assert "warning_repair_attempt_marker" in tool_names
    assert "sd8_fix_plan" in tool_names
    assert "sd10_repair_review_local_check" in tool_names
    assert [entry["phase"] for entry in on_record.fix_log] == [entry["phase"] for entry in off_record.fix_log]
    assert _canonical_hash(on_record.fix_log) == _canonical_hash(off_record.fix_log)
    assert on_record.final_artifacts["verdict"] == off_record.final_artifacts["verdict"] == "success"

    event_payload = json.dumps(_lg_e3_tool_events(on_record), ensure_ascii=False, sort_keys=True)
    assert "lg-e3-needs-repair" not in event_payload
    assert _stable_dsl().strip() not in event_payload
    for raw_key in ["before_dsl", "current_dsl", "candidate_dsl", "raw_prompt", "raw_output"]:
        assert f'"{raw_key}":' not in event_payload


def test_lg_e3_waiver_continuation_keeps_downstream_fixed_wrappers_after_lg_b3_merge(tmp_path: Path) -> None:
    def design_block(_context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        item = DesignDiagnosticItem(
            code="W_LG_E3_B3_CROSS",
            pyfcstm_severity="warning",
            policy_action="budgeted_repair",
            instance_key="lg-e3-b3-cross",
            rationale="force LG-B3 waiver continuation while auditing LG-E3 fixed wrappers",
        )
        return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)

    def reject_all_as_waiver(_request: RepairRequest) -> dict[str, Any]:
        return {
            "candidate_dsl": "",
            "decisions": [{"request_id": "all", "decision": "reject", "rationale": "safe waiver for downstream checks"}],
            "repair_rationale": ["safe waiver for downstream checks"],
            "diff_summary": {"changed": False},
        }

    record = _lg_record(
        _run_langgraph_mock(
            tmp_path,
            run_id="lg-e3-b3-waiver-toolnode-cross",
            adapters=_adapters_with(design=design_block, repair=reject_all_as_waiver),
            max_iterations=1,
        )
    )

    assert "waiver_continue" in _lg_trace_nodes(record)
    assert record.iteration_records[0]["waiver_continue"] is True
    assert record.iteration_records[0]["waiver_entry_envelope"]["schema_version"] == "lg-b3.waiver-entry-envelope.v1"
    assert record.iteration_records[0]["post_waiver_stage_ids"] == [
        StageId.SD_4_DESIGN.value,
        StageId.SL_5_SCENARIO_GENERATION.value,
        StageId.SD_5A_SCENARIO_COVERAGE.value,
        StageId.SC_5F_SCENARIO_FREEZE.value,
        StageId.SD_6_SIM.value,
        StageId.SL_7_MODEL_REVIEW.value,
    ]

    events = _lg_e3_tool_events(record)
    by_tool_node = [(event["tool_name"], event["graph_node"]) for event in events]
    assert by_tool_node == [
        ("sd2_parse", "validation_sd2_parse"),
        ("sd3_semantic", "validation_sd3_semantic"),
        ("sd4_design", "validation_sd4_design"),
        ("sd8_fix_plan", "repair_sd8_fix_requests"),
        ("warning_repair_attempt_marker", "repair_sd8_fix_requests"),
        ("sd5a_scenario_coverage", "validation_sd5a_scenario_coverage"),
        ("sc5f_freeze_scenario_set", "validation_sc5f_scenario_freeze"),
        ("sd6_sim", "validation_sd6_sim"),
    ]
    # LG-B3's post-waiver SD-4 is a waived/advisory tail marker, not a second
    # deterministic design-checker call; LG-E3 must not invent a fake wrapper
    # event for it.  The downstream deterministic tail must still be wrapped.
    assert _lg_e3_tool_names(record).count("sd4_design") == 1
    for expected_downstream_tool in ["sd5a_scenario_coverage", "sc5f_freeze_scenario_set", "sd6_sim"]:
        assert expected_downstream_tool in _lg_e3_tool_names(record)

    payload = json.dumps(events, ensure_ascii=False, sort_keys=True)
    for raw_key in ["before_dsl", "current_dsl", "candidate_dsl", "raw_prompt", "raw_output", "prompt", "messages", "nl"]:
        assert f'"{raw_key}":' not in payload
    assert _stable_dsl().strip() not in payload


def test_lg_e3_safe_summary_redacts_dsl_like_and_prompt_like_scalar_fields() -> None:
    from method.langgraph_runtime import _safe_lg_e3_tool_summary

    raw_payload = {
        "before_dsl": "state SecretBefore { [*] -> Hidden; }",
        "after_dsl": "state SecretAfter { [*] -> Hidden; }",
        "final_dsl": "state SecretFinal { [*] -> Hidden; }",
        "source_dsl": "state SecretSource { [*] -> Hidden; }",
        "repair_candidate_dsl": "state SecretCandidate { [*] -> Hidden; }",
        "raw_input": "raw input should never be mirrored",
        "raw_output": "raw output should never be mirrored",
        "prompt": "prompt should never be mirrored",
        "nl": "NL should never be mirrored",
        "messages": [{"role": "user", "content": "message should never be mirrored"}],
        "safe_stage_id": "SD-8",
    }

    summary = _safe_lg_e3_tool_summary(raw_payload)
    summary_json = json.dumps(summary, ensure_ascii=False, sort_keys=True)

    for forbidden in [
        "SecretBefore",
        "SecretAfter",
        "SecretFinal",
        "SecretSource",
        "SecretCandidate",
        "raw input should never be mirrored",
        "raw output should never be mirrored",
        "prompt should never be mirrored",
        "NL should never be mirrored",
        "message should never be mirrored",
    ]:
        assert forbidden not in summary_json
    for redacted_key in [
        "before_dsl_hash",
        "after_dsl_hash",
        "final_dsl_hash",
        "source_dsl_hash",
        "repair_candidate_dsl_hash",
        "raw_input_hash",
        "raw_output_hash",
        "prompt_hash",
        "nl_hash",
        "messages_hash",
    ]:
        assert redacted_key in summary
    assert summary["safe_stage_id"] == "SD-8"
