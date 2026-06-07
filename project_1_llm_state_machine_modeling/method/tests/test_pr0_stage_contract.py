from __future__ import annotations

import json
from dataclasses import asdict, fields
from pathlib import Path

import pytest

import method.feedback.cascade as feedback_cascade
import method.loop as loop
from method.agents.repair import repair_model
import method.schema as schema
from method.schema import (
    AgentLoopRunRecord,
    BudgetState,
    DesignDiagnosticItem,
    DesignFeedback,
    FeedbackBundle,
    FixPlan,
    GroundedElement,
    GroundingMap,
    JudgeFeedback,
    ModelReviewFeedback,
    ParseFeedback,
    RepairReviewFeedback,
    SL10RepairReviewOutput,
    ReviewRunMeta,
    ScenarioResult,
    ScenarioSet,
    ScenarioStep,
    SemanticFeedback,
    SimFeedback,
    StageContext,
    StageResultMeta,
    StepResult,
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
        "SL-10",
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


def test_model_review_feedback_coerces_nested_review_and_stage_meta_from_json_dicts() -> None:
    fixture = json.loads((METHOD_ROOT / "stages" / "fixtures" / "SL-7.json").read_text(encoding="utf-8"))
    feedback = ModelReviewFeedback(
        **fixture["output"]["model_review_feedback"],
        meta=fixture["meta"],
    )

    assert isinstance(feedback.review_meta, ReviewRunMeta)
    assert feedback.review_meta.decision_threshold == 0.7
    assert feedback.review_meta.failure_policy == "fail_closed"
    assert feedback.review_meta.replay_key == "sl7:sha256:review-input"
    assert isinstance(feedback.meta, StageResultMeta)
    assert feedback.meta.stage_id == StageId.SL_7_MODEL_REVIEW.value


def test_sl10_repair_review_output_coerces_review_meta_from_fixture() -> None:
    fixture = json.loads((METHOD_ROOT / "stages" / "fixtures" / "SL-10.json").read_text(encoding="utf-8"))
    feedback = SL10RepairReviewOutput(
        **fixture["output"]["sl10_repair_review"],
        meta=fixture["meta"],
    )

    assert feedback.ok is True
    assert feedback.decision == "pass"
    assert isinstance(feedback.review_meta, ReviewRunMeta)
    assert feedback.review_meta.failure_policy == "fail_closed"
    assert feedback.review_meta.replay_key == "sl10:sha256:input"
    assert isinstance(feedback.meta, StageResultMeta)
    assert feedback.meta.stage_id == StageId.SL_10_REPAIR_REVIEW.value


def test_nested_feedback_meta_coercion_preserves_stage_contract_from_json_dicts() -> None:
    meta_dict = {
        "stage_id": StageId.SD_4_DESIGN.value,
        "stage_kind": StageKind.DETERMINISTIC.value,
        "enabled": True,
        "ran": True,
        "status": StageStatus.OK.value,
        "ok": True,
    }
    design = DesignFeedback(ok=True, meta=meta_dict)
    bundle = FeedbackBundle(
        enabled_sources=[FeedbackSource.DESIGN.value],
        design=design,
        stage_results=[],
    )

    assert isinstance(design.meta, StageResultMeta)
    assert bundle.all_ok


def test_nested_dataclass_coercion_rejects_unknown_review_meta_keys() -> None:
    with pytest.raises(TypeError, match="unexpected"):
        ModelReviewFeedback(review_meta={"provider": "fake", "unexpected": "drift"})


def test_review_run_meta_rejects_invalid_policy_threshold_and_retry() -> None:
    bad_cases = [
        dict(failure_policy="silent_pass"),
        dict(decision_threshold="not-a-float"),
        dict(decision_threshold=-0.1),
        dict(decision_threshold=1.1),
        dict(decision_threshold=True),
        dict(retry_count=-1),
        dict(retry_count="3"),
        dict(temperature="hot"),
        dict(temperature=True),
        dict(temperature=-0.1),
        dict(seed="42"),
        dict(seed=True),
        dict(schema_validation_ok="yes"),
    ]

    for kwargs in bad_cases:
        with pytest.raises((TypeError, ValueError)):
            ReviewRunMeta(**kwargs)

    meta = ReviewRunMeta(decision_threshold=1, failure_policy="audit_only")
    assert meta.decision_threshold == 1.0


def test_design_feedback_coerces_and_validates_diagnostic_items_from_json_dicts() -> None:
    design = DesignFeedback(
        ok=True,
        blocking_items=[
            {
                "code": "W_DEADLOCK_LEAF",
                "pyfcstm_severity": "warning",
                "policy_action": "budgeted_repair",
                "instance_key": "W_DEADLOCK_LEAF:state=Active",
                "budget_remaining": 1,
                "budget_exhausted": False,
            }
        ],
        advisory_items=[
            {
                "code": "W_OPTIONAL_COVERAGE",
                "pyfcstm_severity": "warning",
                "policy_action": "advisory",
                "instance_key": "W_OPTIONAL_COVERAGE:state=Idle",
            }
        ],
        info_items=[
            {
                "code": "I_REACHABLE",
                "pyfcstm_severity": "info",
                "policy_action": "info",
                "instance_key": "I_REACHABLE:state=Active",
            }
        ],
    )

    assert isinstance(design.blocking_items[0], DesignDiagnosticItem)
    assert isinstance(design.advisory_items[0], DesignDiagnosticItem)
    assert isinstance(design.info_items[0], DesignDiagnosticItem)
    assert design.blocking_items[0].policy_action == "budgeted_repair"


def test_design_diagnostic_item_rejects_invalid_policy_fields() -> None:
    base = {
        "code": "W_DEADLOCK_LEAF",
        "pyfcstm_severity": "warning",
        "policy_action": "budgeted_repair",
        "instance_key": "W_DEADLOCK_LEAF:state=Active",
    }
    bad_cases = [
        dict(pyfcstm_severity="fatal"),
        dict(policy_action="force_repair"),
        dict(budget_remaining=-1),
        dict(budget_remaining="1"),
        dict(budget_exhausted="false"),
    ]

    for override in bad_cases:
        with pytest.raises((TypeError, ValueError)):
            DesignDiagnosticItem(**(base | override))

    with pytest.raises(ValueError):
        DesignFeedback(ok=True, blocking_items=[base | {"policy_action": "force_repair"}])


def test_nested_json_boundary_payloads_coerce_to_dataclasses() -> None:
    scenario_set = ScenarioSet(
        scenario_set_id="scenario-set-pr0-001",
        scenarios=[
            {
                "name": "start_reaches_active",
                "steps": [{"events": ["Start"], "expected_state": "Active"}],
            }
        ],
        epoch=0,
        frozen=True,
    )
    sim = SimFeedback(
        ok=False,
        n_scenarios=1,
        n_scenarios_passed=0,
        scenario_results=[
            {
                "name": "start_reaches_active",
                "status": "fail",
                "step_results": [{"step_index": 0, "status": "fail", "actual_state": "Idle"}],
            }
        ],
    )
    grounding = GroundingMap(
        elements=[
            {
                "element_id": "state:Idle",
                "element_kind": "state",
                "element_ref": "Root.Idle",
                "source_stage": "SL-1",
                "evidence_text": "Idle state",
                "confidence": 1,
            }
        ]
    )
    context = StageContext(
        grounding_map={
            "elements": [
                {
                    "element_id": "state:Idle",
                    "element_kind": "state",
                    "element_ref": "Root.Idle",
                    "source_stage": "SL-1",
                    "evidence_text": "Idle state",
                    "confidence": 1,
                }
            ]
        },
        scenario_set={
            "scenario_set_id": "scenario-set-pr0-001",
            "scenarios": [
                {
                    "name": "start_reaches_active",
                    "steps": [{"events": ["Start"], "expected_state": "Active"}],
                }
            ],
            "epoch": 0,
            "frozen": True,
        },
    )

    assert isinstance(scenario_set.scenarios[0], schema.TestScenario)
    assert isinstance(scenario_set.scenarios[0].steps[0], ScenarioStep)
    assert isinstance(sim.scenario_results[0], ScenarioResult)
    assert isinstance(sim.scenario_results[0].step_results[0], StepResult)
    assert isinstance(grounding.elements[0], GroundedElement)
    assert isinstance(context.grounding_map, GroundingMap)
    assert isinstance(context.grounding_map.elements[0], GroundedElement)
    assert isinstance(context.scenario_set, ScenarioSet)
    assert isinstance(context.scenario_set.scenarios[0], schema.TestScenario)


def test_nested_json_boundary_payloads_reject_invalid_values() -> None:
    bad_cases = [
        lambda: ScenarioStep(before_cycles=-1),
        lambda: ScenarioStep(before_cycles="1"),
        lambda: StepResult(status="unknown"),
        lambda: ScenarioResult(status="unknown"),
        lambda: SimFeedback(n_scenarios=-1),
        lambda: SimFeedback(n_scenarios_passed="1"),
        lambda: ScenarioSet(epoch=-1),
        lambda: GroundedElement(
            element_id="bad",
            element_kind="bogus_kind",
            element_ref="Root.Bad",
            source_stage="SL-1",
            evidence_text="bad",
        ),
        lambda: GroundedElement(
            element_id="bad",
            element_kind="state",
            element_ref="Root.Bad",
            source_stage="SL-1",
            evidence_text="bad",
            requiredness="must",
        ),
        lambda: GroundedElement(
            element_id="bad",
            element_kind="state",
            element_ref="Root.Bad",
            source_stage="SL-1",
            evidence_text="bad",
            confidence=1.1,
        ),
    ]

    for make in bad_cases:
        with pytest.raises((TypeError, ValueError)):
            make()


def test_sim_repair_prompt_accepts_json_loaded_sim_feedback() -> None:
    feedback = FeedbackBundle(
        sim=SimFeedback(
            ok=False,
            n_scenarios=2,
            n_scenarios_passed=1,
            scenario_results=[
                {"name": "s_pass", "status": "pass"},
                {"name": "s_fail", "status": "fail"},
            ],
        )
    )

    selected, summary = repair_model.__globals__["_build_repair_context"]("sim", feedback)
    message = json.dumps({"selected_diagnostics": selected, "scenario_summary": summary}, ensure_ascii=False)

    assert "s_pass" in message
    assert "s_fail" in message


def test_review_feedback_rejects_invalid_literal_decision_and_risk_fields() -> None:
    bad_model_review_cases = [
        dict(decision="accept"),
        dict(risk_level="catastrophic"),
    ]
    for kwargs in bad_model_review_cases:
        with pytest.raises(ValueError):
            ModelReviewFeedback(ok=True, review_meta={"schema_validation_ok": True}, **kwargs)

    with pytest.raises(ValueError):
        RepairReviewFeedback(ok=True, drift_risk="catastrophic")

    with pytest.raises(ValueError):
        schema.RepairRejection(rejected_by_stage="SL-10", reason="bad", drift_risk="catastrophic")


def test_repair_review_bundle_blocks_mutated_delta_review_without_review_meta() -> None:
    meta = ok_meta(StageId.SD_10_REPAIR_REVIEW)
    feedback = RepairReviewFeedback(ok=True, target_resolved=True, meta=meta)
    feedback.delta_review = {"decision": "accept"}
    bundle = FeedbackBundle(
        enabled_sources=[FeedbackSource.REPAIR_REVIEW.value],
        repair_review=feedback,
        stage_results=[meta],
    )

    assert not bundle.all_ok
    assert "enabled source missing review_meta: repair_review" in bundle.stage_contract_errors()


def test_fix_plan_rejects_invalid_target_and_severity() -> None:
    for kwargs in [
        dict(target="judge", severity="error"),
        dict(target="parse", severity="unknown"),
    ]:
        with pytest.raises(ValueError):
            FixPlan(
                source_stage=StageId.SD_8_FIX_PLAN.value,
                source_feedback_id="fb-001",
                **kwargs,
            )

    with pytest.raises(ValueError):
        schema.RevisedFixPlan(
            original={
                "target": "judge",
                "source_stage": StageId.SD_8_FIX_PLAN.value,
                "source_feedback_id": "fb-001",
                "severity": "unknown",
            },
            rejection={
                "rejected_by_stage": StageId.SL_10_REPAIR_REVIEW.value,
                "reason": "bad repair",
            },
        )


def test_revised_fix_plan_rejects_invalid_revision_count() -> None:
    original = {
        "target": "parse",
        "source_stage": StageId.SD_2_PARSE.value,
        "source_feedback_id": "parse:error:1",
        "severity": "error",
    }
    rejection = {
        "rejected_by_stage": StageId.SL_10_REPAIR_REVIEW.value,
        "reason": "scenario regression",
    }

    for revision_count in [-1, "1", True]:
        with pytest.raises((TypeError, ValueError)):
            schema.RevisedFixPlan(original=original, rejection=rejection, revision_count=revision_count)


def test_enabled_model_review_requires_review_meta_for_all_ok() -> None:
    meta = ok_meta(StageId.SL_7_MODEL_REVIEW, StageKind.LLM)
    bundle = FeedbackBundle(
        enabled_sources=[FeedbackSource.MODEL_REVIEW.value],
        model_review=ModelReviewFeedback(ok=True, decision="pass", meta=meta),
        stage_results=[meta],
    )

    assert not bundle.all_ok
    assert "enabled source missing review_meta: model_review" in bundle.stage_contract_errors()


def test_repair_review_feedback_requires_review_meta_when_delta_review_present() -> None:
    with pytest.raises(ValueError, match="review_meta is required"):
        RepairReviewFeedback(ok=True, delta_review={"decision": "accept"})


def test_feedback_bundle_coerces_stage_results_and_feedback_from_json_dicts() -> None:
    meta_dict = {
        "stage_id": StageId.SD_2_PARSE.value,
        "stage_kind": StageKind.DETERMINISTIC.value,
        "enabled": True,
        "ran": True,
        "status": StageStatus.OK.value,
        "ok": True,
    }
    bundle = FeedbackBundle(
        enabled_sources=[FeedbackSource.PARSE.value],
        parse={"ok": True},
        stage_results=[meta_dict],
    )

    assert isinstance(bundle.parse, ParseFeedback)
    assert isinstance(bundle.stage_results[0], StageResultMeta)
    assert bundle.all_ok


def test_trace_and_context_coerce_stage_results_and_budget_state_from_json_dicts() -> None:
    meta_dict = {
        "stage_id": StageId.SD_4_DESIGN.value,
        "stage_kind": StageKind.DETERMINISTIC.value,
        "enabled": True,
        "ran": True,
        "status": StageStatus.ADVISORY.value,
        "ok": True,
    }
    budget_dict = {
        "instance_key": "W_DEADLOCK_LEAF:state=Active",
        "diagnostic_code": "W_DEADLOCK_LEAF",
        "repair_count": 1,
        "budget_remaining": 0,
        "budget_exhausted": True,
    }

    trace = schema.IterTrace(stage_results=[meta_dict], warning_budget_state={"w": budget_dict})
    context = StageContext(stage_results=[meta_dict], warning_budget_state={"w": budget_dict})

    assert isinstance(trace.stage_results[0], StageResultMeta)
    assert isinstance(trace.warning_budget_state["w"], BudgetState)
    assert isinstance(context.stage_results[0], StageResultMeta)
    assert isinstance(context.warning_budget_state["w"], BudgetState)


def test_revised_fix_plan_coerces_nested_dataclasses_from_json_dicts() -> None:
    revised = schema.RevisedFixPlan(
        original={
            "target": "parse",
            "source_stage": StageId.SD_2_PARSE.value,
            "source_feedback_id": "parse:error:1",
            "severity": "error",
        },
        rejection={
            "rejected_by_stage": StageId.SL_10_REPAIR_REVIEW.value,
            "reason": "scenario regression",
            "target_resolved": False,
            "regression_detected": True,
        },
    )

    assert isinstance(revised.original, FixPlan)
    assert isinstance(revised.rejection, schema.RepairRejection)
    assert revised.rejection.regression_detected is True


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


def test_canonical_loop_config_defaults_to_experiment_default_full_staged() -> None:
    cfg = schema.LoopConfig()
    resolved = cfg.resolved_config()

    assert cfg.condition_id == "full_staged_v1"
    assert cfg.policy_profile == "experiment_default"
    assert cfg.llm_provider_mode == "real_env"
    assert cfg.max_iterations == 5
    assert cfg.llm_max_retries == 2
    assert cfg.scenario_max_retries == 2
    assert cfg.budget_policy["min_sl10_rework_attempts"] == 1
    assert resolved["budget_policy"]["min_sl10_rework_attempts"] == 1
    assert resolved["condition_id"] == "full_staged_v1"
    assert resolved["condition_hash"].startswith("sha256:")
    assert resolved["feedback_sources"] == ["parse", "semantic", "design", "sim", "model_review"]
    assert resolved["record_policy"]["write_run_record"] is True
    assert resolved["eligibility_policy"]["exclude_weak_oracle"] is True
    assert resolved["academic_question"] == schema.DEFAULT_ACADEMIC_QUESTION


def test_planned_stage_graph_covers_full_staged_default_and_trace_fields() -> None:
    graph = loop.build_planned_stage_graph(schema.LoopConfig())

    assert graph["planned"] == [
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
        "SL-10",
        "SC-11",
        "SC-12",
        "SC-13",
    ]
    assert all({"enabled", "ran", "status", "skipped_reason"} <= set(node) for node in graph["nodes"])
    assert all(node["enabled"] is True for node in graph["nodes"])
    assert all(node["ran"] is False and node["status"] == "skipped" for node in graph["nodes"])
    assert graph["nodes"][1]["stage_kind"] == "LLM"
    assert graph["nodes"][2]["stage_kind"] == "deterministic"
    assert graph["nodes"][0]["stage_kind"] == "control"


def test_canonical_run_agent_loop_default_full_staged_writes_auditable_record(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    for key in ("LLM_ENDPOINT", "LLM_API_KEY", "LLM_MODEL"):
        monkeypatch.delenv(key, raising=False)
    cfg = schema.LoopConfig(output_dir=str(tmp_path), run_id="contract-only")

    result = loop.run_agent_loop("Start moves Idle to Active.", cfg)

    assert result.status == "api_failed"
    assert result.run_record_path is not None
    assert result.resolved_config["condition_id"] == "full_staged_v1"
    assert result.planned_stage_graph["planned"][0] == "SC-0"
    from method.run_record import read_agent_loop_run_record, is_path_result_eligible

    record = read_agent_loop_run_record(result.run_record_path)
    assert record.status == "error"
    assert record.run_config["condition_id"] == "full_staged_v1"
    assert record.run_config["academic_question"] == schema.DEFAULT_ACADEMIC_QUESTION
    assert record.run_config["contract_only"] is False
    assert record.run_config["compatibility_mode"] == "canonical_staged"
    assert record.run_config["default_loop_config_entry_integrated"] is True
    assert record.stage_graph["planned"] == result.planned_stage_graph["planned"]
    assert record.stage_graph["executed"][:2] == ["SC-0", "SL-1"]
    assert record.final_artifacts["verdict"] == "provider_error"
    assert record.final_artifacts["main_result_eligible"] is False
    assert not is_path_result_eligible(record)


def test_default_loop_rejects_seed_dsl_hot_start(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="must not use seed_dsl"):
        loop.run_agent_loop("NL", schema.LoopConfig(output_dir=str(tmp_path)), seed_dsl="state Root {}")



def test_explicit_ablation_condition_can_disable_stage_but_default_cannot() -> None:
    with pytest.raises(ValueError, match="cannot silently change stage_switches"):
        schema.LoopConfig(stage_switches={**schema.DEFAULT_STAGE_SWITCHES, "enable_model_review": False})
    with pytest.raises(ValueError, match="must write schema-valid run records"):
        schema.LoopConfig(write_run_record=False)
    with pytest.raises(ValueError, match="cannot silently change llm_policy"):
        schema.LoopConfig(llm_policy={**schema._default_llm_policy(), "provider_mode": "fake_replay"})
    with pytest.raises(ValueError, match="cannot silently weaken review modes"):
        schema.LoopConfig(model_review_mode="audit_only")

    switches = schema.DEFAULT_STAGE_SWITCHES.copy()
    switches["enable_model_review"] = False
    condition = schema.AblationCondition(
        condition_id="no_model_review_v1",
        condition_family="stage_ablation",
        base_condition_id="full_staged_v1",
        changed_factors=["enable_model_review=false"],
        stage_switches=switches,
        academic_question="轻量模型评审是否会降低 NL/DSL 语义漂移？",
    )
    cfg = schema.LoopConfig(ablation_condition=condition)

    assert cfg.condition_id == "no_model_review_v1"
    assert cfg.changed_factors == ["enable_model_review=false"]
    assert cfg.academic_question == "轻量模型评审是否会降低 NL/DSL 语义漂移？"
    assert cfg.resolved_config()["academic_question"] == "轻量模型评审是否会降低 NL/DSL 语义漂移？"
    assert "model_review" not in cfg.feedback_sources
    graph = loop.build_planned_stage_graph(cfg)
    sl7 = next(node for node in graph["nodes"] if node["stage_id"] == "SL-7")
    assert sl7["enabled"] is False
    assert sl7["skipped_reason"] == "disabled_by_condition"




def test_default_ablation_condition_preserves_default_academic_question() -> None:
    condition = schema.AblationCondition(
        condition_id="full_staged_v1",
        condition_family="canonical_agent_loop",
        academic_question="",
    )
    cfg = schema.LoopConfig(ablation_condition=condition)

    assert condition.academic_question == schema.DEFAULT_ACADEMIC_QUESTION
    assert cfg.resolved_config()["academic_question"] == schema.DEFAULT_ACADEMIC_QUESTION

def test_direct_non_default_loop_config_requires_academic_question(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    for key in ("LLM_ENDPOINT", "LLM_API_KEY", "LLM_MODEL"):
        monkeypatch.delenv(key, raising=False)

    with pytest.raises(ValueError, match="requires explicit non-default academic_question"):
        schema.LoopConfig(condition_id="iter3_v1", changed_factors=["max_iterations=3"], max_iterations=3)

    cfg = schema.LoopConfig(
        condition_id="iter3_v1",
        condition_family="budget_ablation",
        changed_factors=["max_iterations=3"],
        max_iterations=3,
        budget_policy={**schema._default_budget_policy(), "max_iterations": 3},
        academic_question="迭代预算从 5 降到 3 是否影响收敛率？",
        output_dir=str(tmp_path),
        run_id="iter3-contract",
    )
    result = loop.run_agent_loop("NL", cfg)
    from method.run_record import read_agent_loop_run_record

    record = read_agent_loop_run_record(result.run_record_path or "")
    assert result.resolved_config["academic_question"] == "迭代预算从 5 降到 3 是否影响收敛率？"
    assert record.run_config["academic_question"] == "迭代预算从 5 降到 3 是否影响收敛率？"
    assert record.run_config["condition_id"] == "iter3_v1"


def test_run_cascade_sets_enabled_sources_and_missing_judge_stays_non_ok(monkeypatch) -> None:
    monkeypatch.setattr(feedback_cascade, "check_parse", lambda dsl: ParseFeedback(ok=True))
    monkeypatch.setattr(feedback_cascade, "check_semantic", lambda dsl: SemanticFeedback(ok=True))
    monkeypatch.setattr(
        feedback_cascade,
        "check_sim",
        lambda dsl, scenarios: SimFeedback(ok=True, n_scenarios=len(scenarios), n_scenarios_passed=len(scenarios)),
    )

    bundle = feedback_cascade.run_feedback_cascade(
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
    monkeypatch.setattr(feedback_cascade, "check_parse", lambda dsl: ParseFeedback(ok=False, error_message="boom"))

    bundle = feedback_cascade.run_feedback_cascade(
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
    monkeypatch.setattr(feedback_cascade, "check_parse", lambda dsl: ParseFeedback(ok=True))
    monkeypatch.setattr(feedback_cascade, "check_semantic", lambda dsl: SemanticFeedback(ok=True))

    bundle = feedback_cascade.run_feedback_cascade(
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



def test_agent_loop_run_record_rejects_invalid_status() -> None:
    with pytest.raises(ValueError):
        AgentLoopRunRecord(
            schema_version="pr0.stage-contract.v1",
            run_id="run-test-0001",
            created_at="2026-06-01T00:00:00Z",
            status="partial",
            input_bundle={},
            run_config={},
            environment={},
            stage_graph={},
            stage_records=[],
            iteration_records=[],
        )


def test_agent_loop_run_record_accepts_contract_only_status() -> None:
    record = AgentLoopRunRecord(
        schema_version="pr-a.config-contract.v1",
        run_id="contract-only",
        created_at="2026-06-01T00:00:00Z",
        status="contract_only",
        input_bundle={},
        run_config={},
        environment={},
        stage_graph={},
        stage_records=[],
        iteration_records=[],
        final_artifacts={"main_result_eligible": False},
    )

    assert record.status == "contract_only"


def test_agent_loop_run_record_rejects_invalid_stage_records() -> None:
    with pytest.raises(ValueError, match="stage_records invalid"):
        AgentLoopRunRecord(
            schema_version="pr0.stage-contract.v1",
            run_id="run-bad-stage-record",
            created_at="2026-06-01T00:00:00Z",
            status="success",
            input_bundle={},
            run_config={},
            environment={},
            stage_graph={},
            stage_records=[
                {
                    "stage_id": "SD-404",
                    "stage_kind": "deterministic",
                    "enabled": True,
                    "ran": True,
                    "status": "ok",
                    "ok": True,
                }
            ],
            iteration_records=[],
        )


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
        feedback = DesignFeedback(**output["design_feedback"])
        for item in feedback.blocking_items + feedback.advisory_items + feedback.info_items:
            assert isinstance(item, DesignDiagnosticItem)
    elif stage_id == StageId.SC_5F_SCENARIO_FREEZE.value:
        scenario_set = ScenarioSet(**output["scenario_set"])
        for scenario in scenario_set.scenarios:
            assert isinstance(scenario, schema.TestScenario)
            for step in scenario.steps:
                assert isinstance(step, ScenarioStep)
    elif stage_id == StageId.SD_6_SIM.value:
        feedback = SimFeedback(**output["sim_feedback"])
        for scenario_result in feedback.scenario_results:
            assert isinstance(scenario_result, ScenarioResult)
            for step_result in scenario_result.step_results:
                assert isinstance(step_result, StepResult)
    elif stage_id == StageId.SL_7_MODEL_REVIEW.value:
        feedback = ModelReviewFeedback(**output["model_review_feedback"])
        assert isinstance(feedback.review_meta, ReviewRunMeta)
        assert feedback.review_meta.decision_threshold is not None
        assert feedback.review_meta.failure_policy in {"fail_open", "fail_closed", "audit_only"}
        assert feedback.review_meta.replay_key
        assert "review_meta" not in output
    elif stage_id == StageId.SD_8_FIX_PLAN.value:
        FixPlan(**output["fix_plan"])
    elif stage_id == StageId.SL_10_REPAIR_REVIEW.value:
        feedback = SL10RepairReviewOutput(**output["sl10_repair_review"])
        assert isinstance(feedback.review_meta, ReviewRunMeta)
        assert feedback.review_meta.failure_policy in {"fail_open", "fail_closed", "audit_only"}
        assert feedback.review_meta.replay_key
        assert "review_meta" not in output
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
