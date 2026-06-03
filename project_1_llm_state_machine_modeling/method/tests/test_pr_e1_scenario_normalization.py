from __future__ import annotations

from method.feedback.sim import check_sim
from method.loop import _normalize_scenarios_for_runtime
from method.schema import ScenarioSet, ScenarioStep, StageContext, TestScenario
from method.stages.sd_tools import run_sd6_sim


ELEVATOR_DSL = """
state ElevatorController {
    ! * -> F1 :: Reset;
    [*] -> F1;
    state F1;
    state F2;
    state MU2;
    F1 -> MU2 :: PS2;
    MU2 -> F2 :: S2;
}
"""


def test_default_entry_scenario_normalization_adds_first_empty_cycle_for_events() -> None:
    raw = TestScenario(
        name="request_second_floor",
        steps=[ScenarioStep(events=["PS2"], expected_state="ElevatorController.MU2")],
    )

    normalized = _normalize_scenarios_for_runtime([raw])[0]

    assert normalized.initial_state is None
    assert normalized.steps[0].before_cycles == 1
    assert normalized.steps[0].events == ["PS2"]
    assert "[PR-E1/default-init-cycle-normalized:" in normalized.description
    sim = check_sim(ELEVATOR_DSL, [normalized])
    assert sim.ok


def test_explicit_hot_start_is_preserved_for_non_default_local_probes() -> None:
    raw = TestScenario(
        name="request_second_floor_from_f1",
        initial_state="ElevatorController.F1",
        steps=[ScenarioStep(events=["PS2"], expected_state="ElevatorController.MU2")],
    )

    normalized = _normalize_scenarios_for_runtime([raw])[0]

    assert normalized.initial_state == "ElevatorController.F1"
    assert normalized.steps[0].before_cycles == 0
    sim = check_sim(ELEVATOR_DSL, [normalized])
    assert sim.ok


def test_unadjusted_default_entry_first_event_is_a_scenario_error_not_dsl_failure() -> None:
    raw = TestScenario(
        name="premature_event",
        steps=[ScenarioStep(events=["PS2"], expected_state="ElevatorController.MU2")],
    )

    sim = check_sim(ELEVATOR_DSL, [raw])

    assert not sim.ok
    assert sim.scenario_results[0].status == "error"


ABS_DSL = """
def int k1 = 0;
def int k2 = 0;
def int n = 0;
def float slp = 0.0;

state ABS {
    [*] -> increase;
    state increase { enter { k1 = 1; k2 = 0; n = 0; } }
    state hold { enter { k1 = 0; k2 = 0; n = 0; } }
    increase -> hold : if [slp <= 0.01];
}
"""


def test_sim_hot_start_initial_vars_are_completed_from_dsl_defaults() -> None:
    scenario = TestScenario(
        name="partial_hot_start_vars",
        initial_state="ABS.increase",
        initial_vars={"slp": 0.02},
        steps=[ScenarioStep(events=[], expected_state="ABS.increase", expected_vars={"k1": 0, "k2": 0, "n": 0})],
    )

    sim = check_sim(ABS_DSL, [scenario])

    assert sim.ok
    assert sim.scenario_results[0].setup_error is None



def test_normalized_default_state_failure_remains_repairable_sim_feedback() -> None:
    dsl = """
state Root {
    [*] -> A;
    state A;
    state B;
    state C;
    A -> C :: go;
}
"""
    raw = TestScenario(
        name="real_wrong_target_after_hotstart_normalization",
        description="valid oracle: event go from initial A should reach B",
        steps=[ScenarioStep(events=["go"], expected_state="Root.B", name="go_should_reach_B")],
    )

    normalized = _normalize_scenarios_for_runtime([raw])
    feedback, _ = run_sd6_sim(
        dsl,
        ScenarioSet(scenario_set_id="s", scenarios=normalized, source_dsl_hash="x"),
        StageContext(nl="", current_dsl=dsl),
    )

    assert not feedback.ok
    assert feedback.oracle_weak is False
    assert feedback.scenario_results[0].step_results[0].actual_state == "Root.C"


def test_non_default_hot_start_failure_is_ordinary_sim_feedback_when_preserved() -> None:
    dsl = """
state Root {
    [*] -> A;
    state A;
    state B;
    state C;
    B -> C :: go;
}
"""
    raw = TestScenario(
        name="hot_start_only_probe",
        initial_state="Root.B",
        steps=[ScenarioStep(events=["go"], expected_state="Root.C", name="go_from_B")],
    )

    normalized = _normalize_scenarios_for_runtime([raw])
    feedback, _ = run_sd6_sim(
        dsl,
        ScenarioSet(scenario_set_id="s", scenarios=normalized, source_dsl_hash="x"),
        StageContext(nl="", current_dsl=dsl),
    )

    assert feedback.ok
    assert feedback.oracle_weak is False
