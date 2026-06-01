from __future__ import annotations

import json
from dataclasses import asdict, fields
from pathlib import Path

import method.loop as loop
import method.schema as schema
from method.schema import (
    AgentLoopRunRecord,
    BudgetState,
    DesignFeedback,
    FeedbackBundle,
    FixPlan,
    JudgeFeedback,
    ModelReviewFeedback,
    ParseFeedback,
    RepairReviewFeedback,
    ReviewRunMeta,
    ScenarioSet,
    SemanticFeedback,
    SimFeedback,
    StageContext,
    StageResultMeta,
)
from method.stages import ids
from method.stages.ids import (
    ALL_STAGE_SPECS,
    FEEDBACK_SOURCE_TO_STAGE_ID,
    STAGE_SPECS_BY_ID,
    FeedbackSource,
    StageId,
    StageKind,
    StageStatus,
)


REPO = Path(__file__).resolve().parents[3]
METHOD_ROOT = REPO / "project_1_llm_state_machine_modeling" / "method"


def ok_meta(stage_id: StageId | str, kind: StageKind | str = StageKind.DETERMINISTIC) -> StageResultMeta:
    return StageResultMeta(
        stage_id=stage_id.value if isinstance(stage_id, StageId) else stage_id,
        stage_kind=kind.value if isinstance(kind, StageKind) else kind,
        enabled=True,
        ran=True,
        status=StageStatus.OK.value,
        ok=True,
    )


def test_stage_ids_are_canonical_and_cover_pr0_loop_contract() -> None:
    stage_ids = [spec.stage_id for spec in ALL_STAGE_SPECS]

    assert len(stage_ids) == len(set(stage_ids))
    assert stage_ids == [
        "SC-0",
        "SL-1",
        "SD-2",
        "SD-3",
        "SD-4",
        "SL-5",
        "SD-5A",
        "SC-5F",
        "SD-6",
        "SL-7",
        "SD-8",
        "SL-9",
        "SD-10",
        "SL-10B",
        "SC-11",
        "SC-12",
        "SC-13",
    ]
    assert STAGE_SPECS_BY_ID["SD-4"].kind == StageKind.DETERMINISTIC
    assert STAGE_SPECS_BY_ID["SL-9"].kind == StageKind.LLM
    assert STAGE_SPECS_BY_ID["SC-12"].kind == StageKind.CONTROL
    assert StageId.SD_4_DESIGN.value == "SD-4"
    assert StageId.SC_5F_SCENARIO_FREEZE.value == "SC-5F"
    assert StageId.SC_11_ACCEPT_CANDIDATE.value == "SC-11"
    assert StageId.SC_13_TRACE_AUDIT.value == "SC-13"
    assert FeedbackSource.DESIGN.value == "design"
    assert FEEDBACK_SOURCE_TO_STAGE_ID[FeedbackSource.DESIGN.value] == StageId.SD_4_DESIGN.value


def test_schema_uses_canonical_stage_enums_from_ids_module() -> None:
    assert schema.StageStatus is ids.StageStatus
    assert schema.StageKind is ids.StageKind

    meta = StageResultMeta(
        stage_id=StageId.SD_2_PARSE.value,
        stage_kind="deterministic",
        enabled=True,
        ran=True,
        status="ok",
        ok=True,
    )

    assert meta.stage_kind is StageKind.DETERMINISTIC
    assert meta.status is StageStatus.OK
    assert meta.contract_ok
    assert not meta.blocks_all_ok


def test_feedback_bundle_all_ok_respects_enabled_but_missing_contract() -> None:
    bundle = FeedbackBundle(
        enabled_sources=[FeedbackSource.PARSE.value, FeedbackSource.SEMANTIC.value],
        parse=ParseFeedback(ok=True),
        stage_results=[ok_meta(StageId.SD_2_PARSE)],
    )

    assert not bundle.all_ok
    assert bundle.missing_enabled_sources() == [FeedbackSource.SEMANTIC.value]

    bundle.semantic = SemanticFeedback(ok=True)
    assert not bundle.all_ok
    assert bundle.missing_enabled_stage_metas() == [StageId.SD_3_SEMANTIC.value]

    bundle.stage_results.append(ok_meta(StageId.SD_3_SEMANTIC))
    assert bundle.all_ok
    assert bundle.missing_enabled_sources() == []
    assert bundle.missing_enabled_stage_metas() == []


def test_feedback_bundle_enabled_mode_ignores_non_enabled_failed_feedback() -> None:
    bundle = FeedbackBundle(
        enabled_sources=[FeedbackSource.PARSE.value],
        parse=ParseFeedback(ok=True),
        judge=JudgeFeedback(ok=False),
        stage_results=[ok_meta(StageId.SD_2_PARSE)],
    )

    assert bundle.all_ok
    assert bundle.stage_contract_errors() == []


def test_feedback_bundle_rejects_error_meta_and_nested_missing_meta() -> None:
    error_meta = StageResultMeta(
        stage_id=StageId.SD_4_DESIGN.value,
        stage_kind=StageKind.DETERMINISTIC.value,
        enabled=True,
        ran=True,
        status=StageStatus.ERROR.value,
        ok=False,
        stage_error="inspect_model crashed",
    )
    bundle = FeedbackBundle(
        enabled_sources=[FeedbackSource.DESIGN.value],
        design=DesignFeedback(ok=True, meta=error_meta),
        stage_results=[error_meta],
    )

    assert not bundle.all_ok
    assert not error_meta.contract_errors()
    assert error_meta.blocks_all_ok

    missing_nested = FeedbackBundle(
        enabled_sources=[FeedbackSource.MODEL_REVIEW.value],
        model_review=ModelReviewFeedback(ok=True),
        stage_results=[ok_meta(StageId.SL_7_MODEL_REVIEW, StageKind.LLM)],
    )
    assert not missing_nested.all_ok
    assert "enabled source missing nested meta: model_review" in missing_nested.stage_contract_errors()


def test_stage_result_meta_rejects_unknown_stage_and_kind_mismatch() -> None:
    unknown = StageResultMeta(
        stage_id="SD-404",
        stage_kind=StageKind.DETERMINISTIC.value,
        enabled=True,
        ran=True,
        status=StageStatus.OK.value,
        ok=True,
    )
    assert "unknown stage_id: SD-404" in unknown.contract_errors()
    assert unknown.blocks_all_ok

    wrong_kind = StageResultMeta(
        stage_id=StageId.SD_2_PARSE.value,
        stage_kind=StageKind.LLM.value,
        enabled=True,
        ran=True,
        status=StageStatus.OK.value,
        ok=True,
    )
    assert any("stage_kind mismatch for SD-2" in err for err in wrong_kind.contract_errors())
    assert wrong_kind.blocks_all_ok


def test_feedback_bundle_rejects_wrong_or_disabled_nested_meta() -> None:
    wrong_nested_meta = StageResultMeta(
        stage_id=StageId.SD_2_PARSE.value,
        stage_kind=StageKind.DETERMINISTIC.value,
        enabled=True,
        ran=True,
        status=StageStatus.OK.value,
        ok=True,
    )
    wrong_nested = FeedbackBundle(
        enabled_sources=[FeedbackSource.DESIGN.value],
        design=DesignFeedback(ok=True, meta=wrong_nested_meta),
        stage_results=[],
    )
    assert not wrong_nested.all_ok
    errors = wrong_nested.stage_contract_errors()
    assert "enabled source nested meta stage mismatch: design expected SD-4, got SD-2" in errors
    assert "enabled source missing stage meta: SD-4" in errors

    disabled_meta = StageResultMeta(
        stage_id=StageId.SD_4_DESIGN.value,
        stage_kind=StageKind.DETERMINISTIC.value,
        enabled=False,
        ran=True,
        status=StageStatus.OK.value,
        ok=True,
    )
    disabled_nested = FeedbackBundle(
        enabled_sources=[FeedbackSource.DESIGN.value],
        design=DesignFeedback(ok=True, meta=disabled_meta),
    )
    assert not disabled_nested.all_ok
    assert "enabled source nested meta disabled: design/SD-4" in disabled_nested.stage_contract_errors()


def test_review_run_meta_contains_replay_decision_and_failure_policy_fields() -> None:
    required = {
        "provider",
        "model_id",
        "resolved_model_id",
        "prompt_template_version",
        "prompt_hash",
        "input_hash",
        "temperature",
        "seed",
        "retry_count",
        "raw_output_hash",
        "raw_output_path",
        "parsed_schema_version",
        "schema_validation_ok",
        "schema_validation_error",
        "cache_key",
        "decision_threshold",
        "failure_policy",
        "replay_key",
    }
    actual = {f.name for f in fields(ReviewRunMeta)}

    assert required <= actual
    meta = ReviewRunMeta(decision_threshold=0.7, failure_policy="fail_closed", replay_key="sl7:sha256:input")
    assert meta.decision_threshold == 0.7
    assert meta.failure_policy == "fail_closed"
    assert meta.replay_key == "sl7:sha256:input"


def test_feedback_bundle_distinguishes_unknown_source_from_legacy_judge() -> None:
    unknown = FeedbackBundle(enabled_sources=["parser"])
    assert not unknown.all_ok
    assert "unknown enabled source: parser" in unknown.stage_contract_errors()

    missing_judge = FeedbackBundle(enabled_sources=[FeedbackSource.JUDGE.value])
    assert not missing_judge.all_ok
    assert "unknown enabled source: judge" not in missing_judge.stage_contract_errors()
    assert "enabled source missing feedback: judge" in missing_judge.stage_contract_errors()

    provided_judge = FeedbackBundle(
        enabled_sources=[FeedbackSource.JUDGE.value],
        judge=JudgeFeedback(ok=True, overall=1.0),
    )
    assert provided_judge.all_ok
    assert provided_judge.stage_contract_errors() == []


def test_feedback_bundle_rejects_wrong_stage_results_even_when_feedback_ok() -> None:
    wrong_kind_meta = StageResultMeta(
        stage_id=StageId.SD_2_PARSE.value,
        stage_kind=StageKind.LLM.value,
        enabled=True,
        ran=True,
        status=StageStatus.OK.value,
        ok=True,
    )
    bundle = FeedbackBundle(
        enabled_sources=[FeedbackSource.PARSE.value],
        parse=ParseFeedback(ok=True),
        stage_results=[wrong_kind_meta],
    )

    assert not bundle.all_ok
    assert any("stage_kind mismatch for SD-2" in err for err in bundle.stage_contract_errors())


def test_feedback_bundle_rejects_conflicting_outer_and_nested_meta() -> None:
    outer_ok = StageResultMeta(
        stage_id=StageId.SD_4_DESIGN.value,
        stage_kind=StageKind.DETERMINISTIC.value,
        enabled=True,
        ran=True,
        status=StageStatus.OK.value,
        ok=True,
    )
    nested_error = StageResultMeta(
        stage_id=StageId.SD_4_DESIGN.value,
        stage_kind=StageKind.DETERMINISTIC.value,
        enabled=True,
        ran=True,
        status=StageStatus.ERROR.value,
        ok=False,
        stage_error="inspect_model crashed",
    )
    bundle = FeedbackBundle(
        enabled_sources=[FeedbackSource.DESIGN.value],
        design=DesignFeedback(ok=True, meta=nested_error),
        stage_results=[outer_ok],
    )

    assert not bundle.all_ok
    errors = bundle.stage_contract_errors()
    assert any("conflicting stage meta for design/SD-4" in err for err in errors)
    assert "enabled source nested meta blocks all_ok: design/SD-4 status=error ok=False" in errors


def test_feedback_bundle_rejects_orphan_enabled_blocking_stage_meta() -> None:
    parse_ok = ok_meta(StageId.SD_2_PARSE)
    orphan_fail = StageResultMeta(
        stage_id=StageId.SD_4_DESIGN.value,
        stage_kind=StageKind.DETERMINISTIC.value,
        enabled=True,
        ran=True,
        status=StageStatus.FAIL.value,
        ok=False,
    )
    bundle = FeedbackBundle(
        enabled_sources=[FeedbackSource.PARSE.value],
        parse=ParseFeedback(ok=True),
        stage_results=[parse_ok, orphan_fail],
    )

    assert not bundle.all_ok
    assert "stage meta blocks all_ok: SD-4 status=fail ok=False" in bundle.stage_contract_errors()


def test_run_cascade_sets_enabled_sources_and_missing_judge_stays_non_ok(monkeypatch) -> None:
    monkeypatch.setattr(loop, "check_parse", lambda dsl: ParseFeedback(ok=True))
    monkeypatch.setattr(loop, "check_semantic", lambda dsl: SemanticFeedback(ok=True))
    monkeypatch.setattr(
        loop,
        "check_sim",
        lambda dsl, scenarios: SimFeedback(ok=True, n_scenarios=len(scenarios), n_scenarios_passed=len(scenarios)),
    )

    bundle = loop._run_cascade(
        "machine Sample {}",
        feedback_sources=[
            FeedbackSource.PARSE.value,
            FeedbackSource.SEMANTIC.value,
            FeedbackSource.SIM.value,
            FeedbackSource.JUDGE.value,
        ],
        scenarios=[],
    )

    assert bundle.enabled_sources == ["parse", "semantic", "sim", "judge"]
    assert bundle.parse and bundle.semantic and bundle.sim
    assert bundle.judge is None
    assert not bundle.all_ok
    assert "enabled source missing feedback: judge" in bundle.stage_contract_errors()
    assert [m.stage_id for m in bundle.stage_results] == ["SD-2", "SD-3", "SD-6"]


def test_run_cascade_records_gated_missing_downstream_sources(monkeypatch) -> None:
    monkeypatch.setattr(loop, "check_parse", lambda dsl: ParseFeedback(ok=False, error_message="boom"))

    bundle = loop._run_cascade(
        "broken",
        feedback_sources=[FeedbackSource.PARSE.value, FeedbackSource.SEMANTIC.value],
        scenarios=None,
    )

    assert bundle.enabled_sources == ["parse", "semantic"]
    assert bundle.parse is not None and not bundle.parse.ok
    assert bundle.semantic is None
    assert not bundle.all_ok
    errors = bundle.stage_contract_errors()
    assert "enabled source not ok: parse" in errors
    assert "enabled source missing feedback: semantic" in errors


def test_run_cascade_materializes_missing_scenarios_as_sim_error(monkeypatch) -> None:
    monkeypatch.setattr(loop, "check_parse", lambda dsl: ParseFeedback(ok=True))
    monkeypatch.setattr(loop, "check_semantic", lambda dsl: SemanticFeedback(ok=True))

    bundle = loop._run_cascade(
        "machine Sample {}",
        feedback_sources=[FeedbackSource.PARSE.value, FeedbackSource.SEMANTIC.value, FeedbackSource.SIM.value],
        scenarios=None,
    )

    assert bundle.sim is not None
    assert not bundle.sim.ok
    assert bundle.sim.setup_error == "scenario generation unavailable for enabled sim feedback"
    errors = bundle.stage_contract_errors()
    assert "enabled source not ok: sim" in errors
    assert "stage meta blocks all_ok: SD-6 status=error ok=False" in errors
    assert "enabled source stage meta blocks all_ok: SD-6 status=error ok=False" in errors


def test_run_agent_loop_preserves_scenariogen_failure_root_cause(monkeypatch) -> None:
    monkeypatch.setattr(loop, "check_parse", lambda dsl: ParseFeedback(ok=True))
    monkeypatch.setattr(loop, "check_semantic", lambda dsl: SemanticFeedback(ok=True))

    def raise_scenariogen(*args, **kwargs):
        raise RuntimeError("scenario provider down")

    monkeypatch.setattr(loop, "generate_scenarios", raise_scenariogen)
    monkeypatch.setattr(
        loop,
        "repair_model",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("repair should not hide scenariogen root cause")),
    )

    result = loop.run_agent_loop(
        "When Start occurs, move from Idle to Active.",
        schema.LoopConfig(n_iter=1, feedback_sources=[FeedbackSource.PARSE.value, FeedbackSource.SEMANTIC.value, FeedbackSource.SIM.value]),
        seed_dsl="machine Sample {}",
    )

    assert result.status == "not_converged"
    assert result.error_message is not None
    assert "scenariogen failed: RuntimeError: scenario provider down" in result.error_message
    assert result.final_feedback is not None and result.final_feedback.sim is not None
    assert result.final_feedback.sim.setup_error == "scenario generation unavailable for enabled sim feedback"


def test_stage_result_meta_validates_skipped_and_error_contracts() -> None:
    skipped_without_reason = StageResultMeta(
        stage_id=StageId.SD_4_DESIGN.value,
        stage_kind=StageKind.DETERMINISTIC.value,
        enabled=True,
        ran=False,
        status=StageStatus.SKIPPED.value,
        ok=True,
    )
    assert not skipped_without_reason.contract_ok
    assert skipped_without_reason.blocks_all_ok

    error_without_message = StageResultMeta(
        stage_id=StageId.SD_6_SIM.value,
        stage_kind=StageKind.DETERMINISTIC.value,
        enabled=True,
        ran=True,
        status=StageStatus.ERROR.value,
        ok=False,
    )
    assert not error_without_message.contract_ok
    assert error_without_message.blocks_all_ok

    advisory = StageResultMeta(
        stage_id=StageId.SD_4_DESIGN.value,
        stage_kind=StageKind.DETERMINISTIC.value,
        enabled=True,
        ran=True,
        status=StageStatus.ADVISORY.value,
        ok=True,
    )
    assert advisory.contract_ok
    assert not advisory.blocks_all_ok


def test_feedback_bundle_legacy_non_none_mode_stays_backward_compatible() -> None:
    bundle = FeedbackBundle(parse=ParseFeedback(ok=True))

    assert bundle.all_ok
    assert bundle.has_any_signal()

    bundle.semantic = SemanticFeedback(ok=False)
    assert not bundle.all_ok


def test_agent_loop_run_record_is_single_file_json_schema_fixture() -> None:
    meta = ok_meta(StageId.SD_2_PARSE)
    meta.input_hash = "sha256:input"
    meta.output_hash = "sha256:output"
    meta.elapsed_ms = 12
    record = AgentLoopRunRecord(
        schema_version="pr0.stage-contract.v1",
        run_id="run-test-0001",
        created_at="2026-06-01T00:00:00Z",
        status="success",
        input_bundle={"nl": "When Start occurs, move from Idle to Active."},
        run_config={"enabled_stages": [StageId.SD_2_PARSE.value]},
        environment={"git_commit": "test", "pyfcstm_version": "0.4.0"},
        stage_graph={"planned": [StageId.SD_2_PARSE.value], "executed": [StageId.SD_2_PARSE.value]},
        stage_records=[asdict(meta)],
        iteration_records=[{"iteration": 0, "stage_ids": [StageId.SD_2_PARSE.value]}],
        deterministic_feedback={"parse": {"ok": True}},
        final_artifacts={"final_dsl_hash": "sha256:final", "verdict": "success"},
        replay_index={"stage_by_id": {StageId.SD_2_PARSE.value: 0}},
    )

    payload = asdict(record)
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    decoded = json.loads(encoded)

    assert decoded["run_id"] == "run-test-0001"
    assert decoded["stage_records"][0]["stage_id"] == "SD-2"
    assert decoded["stage_records"][0]["status"] == StageStatus.OK.value
    assert decoded["redaction_report"] == []


def test_budget_state_and_stage_context_summary_are_json_serializable() -> None:
    state = BudgetState(
        instance_key="W_DEADLOCK_LEAF:state=Root.Idle",
        diagnostic_code="W_DEADLOCK_LEAF",
        repair_count=1,
        budget_remaining=1,
        budget_exhausted=False,
        last_status="budgeted_repair",
        last_stage=StageId.SD_4_DESIGN.value,
    )
    context = StageContext(
        nl="When Start occurs, move from Idle to Active.",
        current_dsl="machine Sample {}",
        ast=object(),
        model=object(),
        inspect_json={"diagnostics": []},
        warning_budget_state={state.instance_key: state},
    )

    payload = asdict(state)
    summary = asdict(context.to_summary())
    assert payload["instance_key"].startswith("W_DEADLOCK_LEAF")
    assert json.loads(json.dumps(payload))["budget_remaining"] == 1
    assert summary["has_ast"] and summary["has_model"]
    assert summary["warning_budget_keys"] == ["W_DEADLOCK_LEAF:state=Root.Idle"]


def test_budget_state_rejects_impossible_states() -> None:
    bad_cases = [
        dict(
            instance_key="W_DEADLOCK_LEAF:state=Active",
            diagnostic_code="W_DEADLOCK_LEAF",
            repair_count=-1,
            budget_remaining=0,
            budget_exhausted=False,
        ),
        dict(
            instance_key="W_DEADLOCK_LEAF:state=Active",
            diagnostic_code="W_DEADLOCK_LEAF",
            repair_count=0,
            budget_remaining=-1,
            budget_exhausted=False,
        ),
        dict(
            instance_key="W_DEADLOCK_LEAF:state=Active",
            diagnostic_code="W_DEADLOCK_LEAF",
            repair_count=2,
            budget_remaining=1,
            budget_exhausted=True,
        ),
    ]

    for kwargs in bad_cases:
        try:
            BudgetState(**kwargs)
        except ValueError:
            pass
        else:
            raise AssertionError(f"BudgetState accepted impossible state: {kwargs}")


def validate_stage_fixture_output(stage_id: str, output: dict) -> None:
    if stage_id == StageId.SD_2_PARSE.value:
        ParseFeedback(**output["parse_feedback"])
    elif stage_id == StageId.SD_3_SEMANTIC.value:
        SemanticFeedback(**output["semantic_feedback"])
    elif stage_id == StageId.SD_4_DESIGN.value:
        DesignFeedback(**output["design_feedback"])
    elif stage_id == StageId.SC_5F_SCENARIO_FREEZE.value:
        ScenarioSet(**output["scenario_set"])
    elif stage_id == StageId.SD_6_SIM.value:
        SimFeedback(**output["sim_feedback"])
    elif stage_id == StageId.SL_7_MODEL_REVIEW.value:
        ModelReviewFeedback(**output["model_review_feedback"])
    elif stage_id == StageId.SD_8_FIX_PLAN.value:
        FixPlan(**output["fix_plan"])
    elif stage_id == StageId.SD_10_REPAIR_REVIEW.value:
        RepairReviewFeedback(**output["repair_review_feedback"])
    elif stage_id == StageId.SC_13_TRACE_AUDIT.value:
        AgentLoopRunRecord(**output["agent_loop_run_record"])


def test_stage_docs_skill_links_and_stage_specific_fixtures_exist() -> None:
    docs_root = METHOD_ROOT / "stages" / "docs"
    fixtures_root = METHOD_ROOT / "stages" / "fixtures"
    skill_root = METHOD_ROOT / "agent_loop_skill"
    observed_statuses: set[str] = set()

    for spec in ALL_STAGE_SPECS:
        doc = docs_root / spec.doc_filename
        assert doc.exists(), f"missing stage doc: {doc}"
        text = doc.read_text(encoding="utf-8")
        for marker in ["## 目标", "## 输入", "## 输出", "## 函数名或 prompt generator 名", "## 最小示例", "## 失败语义"]:
            assert marker in text, f"{marker} missing in {doc}"
        if spec.kind == StageKind.LLM:
            assert "### LLM 输入" in text, f"LLM input section missing in {doc}"
            assert "### LLM 输出" in text, f"LLM output section missing in {doc}"

        fixture = fixtures_root / f"{spec.stage_id}.json"
        assert fixture.exists(), f"missing fixture: {fixture}"
        data = json.loads(fixture.read_text(encoding="utf-8"))
        assert data["stage_id"] == spec.stage_id
        assert data["stage_kind"] == spec.kind.value
        assert "input" in data and "output" in data and "meta" in data
        assert set(data["input"]) != {"summary"}, f"generic input fixture: {fixture}"
        assert set(data["output"]) != {"summary"}, f"generic output fixture: {fixture}"
        StageResultMeta(**data["meta"])
        observed_statuses.add(data["meta"]["status"])
        validate_stage_fixture_output(spec.stage_id, data["output"])

        skill_link = skill_root / "stages" / f"{spec.stage_id}.md"
        assert skill_link.is_symlink(), f"missing skill stage symlink: {skill_link}"
        assert skill_link.resolve() == doc.resolve()

    negative_fixture_names = ["NEG-SKIPPED", "NEG-ERROR", "NEG-ADVISORY", "NEG-BUDGET-EXHAUSTED"]
    for name in negative_fixture_names:
        data = json.loads((fixtures_root / f"{name}.json").read_text(encoding="utf-8"))
        meta = StageResultMeta(**data["meta"])
        observed_statuses.add(meta.status.value)
        assert meta.contract_ok, f"negative fixture should be valid shape: {name}"
        if name == "NEG-BUDGET-EXHAUSTED":
            budget_state = BudgetState(**data["output"]["budget_state"])
            assert budget_state.instance_key == data["input"]["instance_key"]
            assert budget_state.diagnostic_code == data["input"]["diagnostic_code"]
            assert budget_state.budget_exhausted

    assert {"ok", "fail", "skipped", "error", "advisory"}.issubset(observed_statuses)

    for link_name in ["SKILL.md", "CLAUDE.md"]:
        link = skill_root / link_name
        assert link.is_symlink(), f"{link} must be a symlink"
        assert link.resolve() == (skill_root / "AGENT_LOOP_SKILL.md").resolve()

    assert (skill_root / "tools.md").exists()
    assert (skill_root / "prompts.md").exists()
