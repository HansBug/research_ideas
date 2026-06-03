from __future__ import annotations

from method.feedback.sim import check_sim
from method.loop import _normalize_scenarios_for_runtime
from method.schema import ScenarioStep, TestScenario


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
        initial_state="ElevatorController.F1",
        steps=[ScenarioStep(events=["PS2"], expected_state="ElevatorController.MU2")],
    )

    normalized = _normalize_scenarios_for_runtime([raw])[0]

    assert normalized.initial_state is None
    assert normalized.steps[0].before_cycles == 1
    assert normalized.steps[0].events == ["PS2"]
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
