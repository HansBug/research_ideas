from __future__ import annotations

from dataclasses import asdict

import method.schema as schema
from method.schema import (
    BudgetState,
    DesignFeedback,
    FixPlan,
    GroundedElement,
    GroundingMap,
    RepairRejection,
    RevisedFixPlan,
    ScenarioSet,
    StageContext,
)
from method.stages.ids import StageId, StageStatus
from method.stages.sd_context import build_model_from_dsl
from method.stages.sd_tools import (
    DEFAULT_WARNING_REPAIR_BUDGET,
    freeze_scenario_set,
    run_sd2_parse,
    run_sd3_semantic,
    mark_warning_repair_attempt,
    run_sd4_design,
    run_sd5a_scenario_coverage,
    run_sd6_sim,
    run_sd8_fix_plan,
    run_sd10_repair_review,
)

OK_DSL = """
state Root {
    event Start;
    state Idle;
    state Active;
    [*] -> Idle;
    Idle -> Active :: Start;
    Active -> [*];
}
"""

DEADLOCK_DSL = """
state Root {
    state Idle;
    state Active;
    [*] -> Idle;
    Idle -> Active :: Start;
}
"""

UNREACHABLE_DSL = """
state Root {
    state Idle;
    state Orphan;
    [*] -> Idle;
    Idle -> [*];
}
"""

SEM_BAD_DSL = """
def int x = 0;
state Root {
    state Idle;
    state Active;
    [*] -> Idle;
    Idle -> Active : if [missing > 0];
}
"""


UNWRITTEN_READ_DSL = """
def int sensor = 0;
state Root {
    state Idle;
    state Active;
    [*] -> Idle;
    Idle -> Active : if [sensor > 0];
    Active -> [*];
}
"""

FORCED_DSL = """
state Root {
    state Idle;
    state Active;
    state Error;
    [*] -> Idle;
    Idle -> Active :: Start;
    ! * -> Error :: Fail;
    Active -> [*];
    Error -> [*];
}
"""


def test_per_stage_public_modules_reexport_sd_facade_functions() -> None:
    from method.stages import sd_design, sd_fix_plan, sd_parse, sd_repair_review, sd_scenario_coverage, sd_semantic, sd_sim

    assert sd_parse.run_sd2_parse is run_sd2_parse
    assert sd_semantic.run_sd3_semantic is run_sd3_semantic
    assert sd_design.run_sd4_design is run_sd4_design
    assert sd_scenario_coverage.run_sd5a_scenario_coverage is run_sd5a_scenario_coverage
    assert sd_scenario_coverage.freeze_scenario_set is freeze_scenario_set
    assert sd_sim.run_sd6_sim is run_sd6_sim
    assert sd_fix_plan.run_sd8_fix_plan is run_sd8_fix_plan
    assert sd_repair_review.run_sd10_repair_review is run_sd10_repair_review


def test_stage_context_model_handoff_reuses_canonical_build_path() -> None:
    context = StageContext(nl="Start moves Idle to Active")

    parse_feedback, parse_meta = run_sd2_parse(OK_DSL, context)
    semantic_feedback, semantic_meta, build = run_sd3_semantic(OK_DSL, context)

    assert parse_feedback.ok
    assert semantic_feedback.ok
    assert build.ok
    assert context.ast is build.ast
    assert context.model is build.model
    assert [m.stage_id for m in context.stage_results] == [StageId.SD_2_PARSE.value, StageId.SD_3_SEMANTIC.value]
    assert parse_meta.status is StageStatus.OK
    assert semantic_meta.status is StageStatus.OK


def test_build_model_from_dsl_reports_semantic_error_without_model_handoff() -> None:
    result = build_model_from_dsl(SEM_BAD_DSL)

    assert not result.ok
    assert result.ast is not None
    assert result.model is None
    assert result.error_class == "ModelValidationError"
    assert any(d["code"] == "E_UNDEFINED_VAR" for d in result.diagnostics)


def test_sd4_design_maps_high_risk_warning_to_budgeted_repair_and_hints() -> None:
    context = StageContext(nl="Start moves Idle to Active")
    run_sd3_semantic(DEADLOCK_DSL, context)

    feedback, meta = run_sd4_design(context)

    assert not feedback.ok
    assert meta.stage_id == StageId.SD_4_DESIGN.value
    assert meta.status is StageStatus.FAIL
    assert feedback.blocking_items
    item = feedback.blocking_items[0]
    assert item.code == "W_DEADLOCK_LEAF"
    assert item.policy_action == "budgeted_repair"
    assert item.budget_remaining == DEFAULT_WARNING_REPAIR_BUDGET
    assert item.suggested_fix_hints  # from refs.suggested_fix and/or codes.yaml for_llm
    assert context.inspect_json is not None
    assert item.instance_key in context.warning_budget_state


def test_sd4_design_downgrades_exhausted_warning_to_advisory() -> None:
    context = StageContext()
    run_sd3_semantic(DEADLOCK_DSL, context)
    key = "W_DEADLOCK_LEAF:state_path=Root.Active:reason=no_outgoing_transition"
    context.warning_budget_state[key] = BudgetState(
        instance_key=key,
        diagnostic_code="W_DEADLOCK_LEAF",
        repair_count=2,
        budget_remaining=0,
        budget_exhausted=True,
    )

    feedback, meta = run_sd4_design(context)

    assert feedback.ok
    assert meta.status is StageStatus.OK
    assert not feedback.blocking_items
    assert feedback.advisory_items
    assert feedback.advisory_items[0].policy_action == "advisory"


def test_sd4_design_routes_advisory_warnings_and_audit_policy() -> None:
    context = StageContext()
    run_sd3_semantic(OK_DSL, context)

    feedback, meta = run_sd4_design(context)

    assert not feedback.ok
    assert meta.status is StageStatus.FAIL
    assert any(item.code == "W_SHADOWED_EVENT" for item in feedback.blocking_items)
    assert any(item.policy_action == "requires_policy_classification" for item in feedback.blocking_items)
    assert any(item.code == "W_UNUSED_EVENT" for item in feedback.advisory_items)
    assert all(item.policy_action == "advisory" for item in feedback.advisory_items)
    assert feedback.inspect_summary["prompt_ready_summary"]

    strict_context = StageContext()
    run_sd3_semantic(UNWRITTEN_READ_DSL, strict_context)
    strict_feedback, _ = run_sd4_design(strict_context)
    audit_feedback, _ = run_sd4_design(strict_context, policy_profile="audit_only")

    assert any(item.code == "W_UNWRITTEN_READ_VAR" for item in strict_feedback.blocking_items)
    assert audit_feedback.ok
    assert any(item.code == "W_UNWRITTEN_READ_VAR" for item in audit_feedback.advisory_items)


def test_warning_budget_attempt_decrements_to_advisory() -> None:
    context = StageContext()
    run_sd3_semantic(DEADLOCK_DSL, context)
    feedback, _ = run_sd4_design(context)
    key = feedback.blocking_items[0].instance_key

    mark_warning_repair_attempt(context.warning_budget_state, [key])
    assert context.warning_budget_state[key].repair_count == 1
    assert context.warning_budget_state[key].budget_remaining == 1
    mark_warning_repair_attempt(context.warning_budget_state, [key])
    assert context.warning_budget_state[key].repair_count == 2
    assert context.warning_budget_state[key].budget_remaining == 0
    assert context.warning_budget_state[key].budget_exhausted

    feedback_after_budget, _ = run_sd4_design(context)
    assert feedback_after_budget.ok
    assert feedback_after_budget.advisory_items[0].instance_key == key


def test_sd5a_scenario_coverage_exposes_retry_directive_contract() -> None:
    report, meta = run_sd5a_scenario_coverage(OK_DSL, [])

    assert set(report) == {"coverage_report", "retry_directive", "coverage_gap"}
    assert meta.stage_id == StageId.SD_5A_SCENARIO_COVERAGE.value
    assert meta.status in {StageStatus.OK, StageStatus.ADVISORY}


def test_sd4_design_routes_info_to_info_not_repair() -> None:
    context = StageContext()
    no_event_dsl = """
state Root {
    state Idle;
    state Active;
    [*] -> Idle;
    Idle -> Active;
    Active -> [*];
}
"""
    run_sd3_semantic(no_event_dsl, context)

    feedback, _meta = run_sd4_design(context)

    assert feedback.ok
    assert not feedback.blocking_items
    assert all(item.pyfcstm_severity == "info" for item in feedback.info_items)


def test_sd8_fix_plan_uses_design_feedback_hints_as_reference_not_command() -> None:
    context = StageContext()
    run_sd3_semantic(DEADLOCK_DSL, context)
    design_feedback, _ = run_sd4_design(context)
    grounding = GroundingMap(
        elements=[
            GroundedElement(
                element_id="state:Root.Active",
                element_kind="state",
                element_ref="Root.Active",
                source_stage="SL-1",
                evidence_text="Active state is required",
                requiredness="required",
            )
        ]
    )

    plan, meta = run_sd8_fix_plan(
        design_feedback,
        source="design",
        grounding_map=grounding,
        before_dsl=DEADLOCK_DSL,
    )

    assert isinstance(plan, FixPlan)
    assert meta.stage_id == StageId.SD_8_FIX_PLAN.value
    assert plan.target == "design"
    assert plan.severity == "blocking_warning"
    assert plan.suggested_fix_hints
    assert any("hints" in strategy.lower() or "smallest" in strategy.lower() for strategy in plan.recommended_strategy)
    assert "state:Root.Active" in plan.required_preserve_element_ids
    assert plan.before_dsl_hash.startswith("sha256:")


def test_sd8_revised_fix_plan_preserves_original_target() -> None:
    original = FixPlan(
        target="sim",
        source_stage=StageId.SD_6_SIM.value,
        source_feedback_id="scenario:1",
        severity="sim_fail",
    )
    rejection = RepairRejection(
        rejected_by_stage=StageId.SD_10_REPAIR_REVIEW.value,
        reason="scenario regression",
        regression_detected=True,
        drift_risk="minor",
    )

    revised, _meta = run_sd8_fix_plan(None, source="repair_review", original=original, rejection=rejection)

    assert isinstance(revised, RevisedFixPlan)
    assert revised.original.target == "sim"
    assert revised.rejection.regression_detected


def test_sd6_sim_consumes_frozen_scenario_set() -> None:
    scenario_set, freeze_meta = freeze_scenario_set(
        [
            schema.TestScenario(
                name="start_reaches_active",
                initial_state="Root.Idle",
                steps=[{"events": ["Start"], "expected_state": "Root.Active"}],
            )
        ],
        source_dsl_hash="sha256:test",
        source_inspect_hash="sha256:inspect",
        coverage_report={"coverage_score": 1.0},
    )

    feedback, sim_meta = run_sd6_sim(OK_DSL, scenario_set)

    assert isinstance(scenario_set, ScenarioSet)
    assert freeze_meta.stage_id == StageId.SC_5F_SCENARIO_FREEZE.value
    assert feedback.ok
    assert feedback.n_scenarios == 1
    assert feedback.n_scenarios_passed == 1
    assert sim_meta.stage_id == StageId.SD_6_SIM.value


def test_sd10_repair_review_rejects_parse_semantic_and_grounding_drift() -> None:
    plan = FixPlan(target="design", source_stage=StageId.SD_4_DESIGN.value, source_feedback_id="W", severity="blocking_warning")
    grounding = GroundingMap(
        elements=[
            GroundedElement(
                element_id="state:Root.Active",
                element_kind="state",
                element_ref="Root.Active",
                source_stage="SL-1",
                evidence_text="Active state required by NL",
                requiredness="required",
            )
        ]
    )

    feedback, _meta = run_sd10_repair_review(
        nl="Start moves Idle to Active",
        grounding_map=grounding,
        old_dsl=DEADLOCK_DSL,
        candidate_dsl="state Root { state Idle; [*] -> Idle; }",
        fix_plan=plan,
    )

    assert not feedback.ok
    assert not feedback.target_resolved
    assert feedback.drift_risk == "major"
    assert feedback.local_rejection is not None
    assert any(e["kind"] == "missing_required_grounding" for e in feedback.local_rejection.evidence)


def test_sd10_repair_review_rejects_unresolved_design_target() -> None:
    context = StageContext()
    run_sd3_semantic(DEADLOCK_DSL, context)
    design_feedback, _ = run_sd4_design(context)
    plan, _ = run_sd8_fix_plan(design_feedback, source="design", before_dsl=DEADLOCK_DSL)

    feedback, _meta = run_sd10_repair_review(
        nl="Active should not deadlock",
        grounding_map=None,
        old_dsl=DEADLOCK_DSL,
        candidate_dsl=DEADLOCK_DSL,
        fix_plan=plan,
    )

    assert not feedback.ok
    assert feedback.local_rejection is not None
    assert any(e["kind"] == "design_target_unresolved" for e in feedback.local_rejection.evidence)


def test_sd10_repair_review_detects_count_and_forced_transition_drift() -> None:
    plan = FixPlan(target="sim", source_stage=StageId.SD_6_SIM.value, source_feedback_id="sim", severity="sim_fail")

    feedback, _meta = run_sd10_repair_review(
        nl="Root has normal and forced transitions",
        grounding_map=None,
        old_dsl=FORCED_DSL,
        candidate_dsl=OK_DSL,
        fix_plan=plan,
    )

    assert not feedback.ok
    assert feedback.drift_risk == "major"
    assert feedback.local_rejection is not None
    kinds = {e["kind"] for e in feedback.local_rejection.evidence}
    assert "forced_transition_count_drift" in kinds
    assert "count_drift" in kinds


def test_sd10_repair_review_rejects_event_grounding_replaced_by_same_name_state() -> None:
    old_dsl = """
state Root {
    state Idle;
    state Active;
    state Start;
    [*] -> Idle;
    Idle -> Active :: Start;
    Active -> [*];
}
"""
    candidate_dsl = """
state Root {
    state Idle;
    state Active;
    state Start;
    [*] -> Idle;
    Idle -> Active :: Reset;
    Active -> [*];
}
"""
    grounding = GroundingMap(
        elements=[
            GroundedElement(
                element_id="event:Start",
                element_kind="event",
                element_ref="Start",
                source_stage="Path1",
                evidence_text="Start event is required trigger",
                requiredness="required",
            )
        ]
    )
    plan = FixPlan(target="sim", source_stage=StageId.SD_6_SIM.value, source_feedback_id="sim", severity="sim_fail")

    feedback, _meta = run_sd10_repair_review(
        nl="Start event triggers Active; Start state also exists",
        grounding_map=grounding,
        old_dsl=old_dsl,
        candidate_dsl=candidate_dsl,
        fix_plan=plan,
    )

    assert not feedback.ok
    assert feedback.drift_risk == "major"
    assert feedback.local_rejection is not None
    assert any(e["kind"] == "missing_required_grounding" and "event:Start" in e["element_ids"] for e in feedback.local_rejection.evidence)


def test_sd10_repair_review_rejects_comment_or_prefix_only_state_grounding() -> None:
    grounding = GroundingMap(
        elements=[
            GroundedElement(
                element_id="state:Root.Active",
                element_kind="state",
                element_ref="Root.Active",
                source_stage="SL-1",
                evidence_text="Active state required by NL",
                requiredness="required",
            )
        ]
    )
    plan = FixPlan(target="design", source_stage=StageId.SD_4_DESIGN.value, source_feedback_id="W", severity="blocking_warning")

    feedback, _meta = run_sd10_repair_review(
        nl="Active state is required",
        grounding_map=grounding,
        old_dsl=DEADLOCK_DSL,
        candidate_dsl="""
state Root {
    state Idle;
    state ActiveHelper;
    // Active was deleted
    [*] -> Idle;
    Idle -> [*];
}
""",
        fix_plan=plan,
    )

    assert not feedback.ok
    assert feedback.local_rejection is not None
    assert any(e["kind"] == "missing_required_grounding" for e in feedback.local_rejection.evidence)


def test_sd10_repair_review_tracks_advisory_design_target() -> None:
    advisory_context = StageContext()
    run_sd3_semantic(OK_DSL, advisory_context)
    design_feedback, _ = run_sd4_design(advisory_context, policy_profile="audit_only")
    assert design_feedback.advisory_items
    plan, _ = run_sd8_fix_plan(design_feedback, source="design", before_dsl=OK_DSL)

    feedback, _meta = run_sd10_repair_review(
        nl="Start moves Idle to Active",
        grounding_map=None,
        old_dsl=OK_DSL,
        candidate_dsl=OK_DSL,
        fix_plan=plan,
    )

    assert not feedback.ok
    assert feedback.local_rejection is not None
    assert any(e["kind"] == "design_target_unresolved" for e in feedback.local_rejection.evidence)


def test_sd10_repair_review_detects_scenario_regression() -> None:
    scenario_set, _ = freeze_scenario_set(
        [schema.TestScenario(name="hotstart_active", initial_state="Root.Active")],
        source_dsl_hash="sha256:test",
    )
    plan = FixPlan(target="sim", source_stage=StageId.SD_6_SIM.value, source_feedback_id="hotstart_active", severity="sim_fail")

    feedback, _meta = run_sd10_repair_review(
        nl="Active is required",
        grounding_map=None,
        old_dsl=OK_DSL,
        candidate_dsl="state Root { state Idle; [*] -> Idle; }",
        fix_plan=plan,
        scenario_set=scenario_set,
    )

    assert not feedback.ok
    assert feedback.regression_detected
    assert feedback.local_rejection is not None
    assert any(e["kind"] == "scenario_regression" for e in feedback.local_rejection.evidence)


def test_sd_tools_outputs_are_json_serializable() -> None:
    context = StageContext()
    run_sd3_semantic(DEADLOCK_DSL, context)
    design_feedback, _ = run_sd4_design(context)
    plan, _ = run_sd8_fix_plan(design_feedback, source="design", before_dsl=DEADLOCK_DSL)

    assert asdict(design_feedback)["blocking_items"]
    assert asdict(plan)["target"] == "design"
