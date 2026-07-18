from __future__ import annotations

import json
from pathlib import Path

from paper_stm_repair_conversion.adapters.plantuml_source import parse_plantuml_source
from paper_stm_repair_representation.plantuml_source_lowering import (
    lower_plantuml_source,
)
from pyfcstm.diagnostics.inspect import inspect_model
from pyfcstm.model.load import load_state_machine_from_text
from pyfcstm.simulate import SimulationRuntime


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "project_1_llm_state_machine_modeling").is_dir():
            return parent
    raise RuntimeError("repository root not found")


REPO_ROOT = _repo_root()
PAIRS = (
    REPO_ROOT
    / "project_1_llm_state_machine_modeling/paper_stm_repair/corpora/seed_library"
    / "llms-emp-stm-subset/assets/extracted/pairs.jsonl"
)


def _rows() -> list[dict]:
    return [json.loads(line) for line in PAIRS.read_text(encoding="utf-8").splitlines()]


def _lower(index: int) -> dict:
    row = _rows()[index]
    canonical = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    return lower_plantuml_source(canonical)


def test_final_boundary_is_emitted_as_fcstm_exit():
    lowered = _lower(22)
    assert "PoweredOn -> [*] : /keyOff;" in lowered["fcstm"]
    assert 'state end named "end"' not in lowered["fcstm"]
    assert lowered["comparison"]["final_transition_coverage"] == "1/1"


def test_lifecycle_actions_are_emitted_as_abstract_actions():
    lowered = _lower(54)
    assert "enter abstract Accelerate;" in lowered["fcstm"]
    assert ">> during before abstract Send;" in lowered["fcstm"]
    assert ">> during before abstract EmergencyStop;" in lowered["fcstm"]
    assert ">> during before abstract SendObstacleDetected;" in lowered["fcstm"]
    assert lowered["comparison"]["lifecycle_action_coverage"] == "4/4"


def test_lifecycle_only_state_uses_a_stoppable_active_leaf():
    lowered = _lower(4)
    model = load_state_machine_from_text(lowered["fcstm"])
    runtime = SimulationRuntime(model)

    def event(name: str) -> list[str]:
        return [f"{model.root_state.name}.{name}"]

    runtime.cycle()
    runtime.cycle(event("Closed_SendDeparted"))
    assert runtime.current_state.path[-2] == "Accelerating"
    assert runtime.current_state.path[-1].startswith("LifecycleActive")
    runtime.cycle(event("Reached_Cruising_Cruise"))

    assert runtime.current_state.path[-2:] == ("InMotion", "Cruising")


def test_scope_exit_and_parent_continuation_reach_autonomous_initial_state():
    lowered = _lower(0)
    model = load_state_machine_from_text(lowered["fcstm"])
    runtime = SimulationRuntime(model)

    runtime.cycle()
    runtime.cycle([f"{model.root_state.name}.Power_On"])
    assert runtime.current_state.path[-2:] == ("HumanDriving", "InitialState")
    runtime.cycle([f"{model.root_state.name}.Front_Distance_10"])
    assert runtime.current_state.path[-1].startswith("InitialWait")
    assert runtime.current_state.path[-2] == "Autonomous"
    runtime.cycle([f"{model.root_state.name}.Enter_Autonomous"])

    assert runtime.current_state.path[-2:] == ("Autonomous", "InitialState")


def test_initial_transition_label_is_preserved_as_opaque_event():
    lowered = _lower(0)

    assert 'named "Awaiting initial event: Power On"' in lowered["fcstm"]
    assert "-> InitialState : /Power_On;" in lowered["fcstm"]
    mapping = next(
        item
        for item in lowered["comparison"]["transition_mappings"]
        if item["transition_id"] == "tr_0002"
    )
    assert mapping["status"] == "mapped"
    assert len(mapping["emitted"]) == 2
    assert mapping["emitted"][0]["generated_role"] == "source_initial_wait_entry"
    assert "/Power_On" in mapping["emitted"][1]["line"]


def test_unlabeled_fanout_is_preserved_but_not_declared_exact():
    lowered = _lower(53)

    assert "PumpState -> WaterState;" in lowered["fcstm"]
    assert "PumpState -> MethaneState;" in lowered["fcstm"]
    assert lowered["comparison"]["verdict"] == "blocked_unsupported"
    reasons = {item["reason_code"] for item in lowered["comparison"]["blockers"]}
    assert "R45.BLOCKED.ambiguous_unlabeled_fanout" in reasons


def test_transition_to_composite_without_initial_is_blocked_not_guessed():
    lowered = _lower(5)
    blocked = {
        item["transition_id"]: item
        for item in lowered["comparison"]["transition_mappings"]
        if item["status"] == "blocked_unsupported"
    }

    assert blocked["tr_0003"]["reason_code"] == "R45.BLOCKED.target_composite_missing_initial"
    assert blocked["tr_0006"]["reason_code"] == "R45.BLOCKED.target_composite_missing_initial"
    assert "DoorShut -> DoorOpen : /Door_Opened;" not in lowered["fcstm"]


def test_initial_to_composite_without_child_initial_is_blocked():
    lowered = _lower(57)
    mapping = next(
        item
        for item in lowered["comparison"]["transition_mappings"]
        if item["transition_id"] == "tr_0010"
    )

    assert mapping["status"] == "blocked_unsupported"
    assert mapping["reason_code"] == "R45.BLOCKED.initial_target_composite_missing_initial"


def test_opaque_state_body_is_preserved_as_explicit_blocker():
    lowered = _lower(48)
    blockers = [
        item
        for item in lowered["comparison"]["blockers"]
        if item["reason_code"] == "R45.BLOCKED.opaque_state_body_not_executable"
    ]

    assert {item["state_id"] for item in blockers} >= {
        "TurnOn",
        "AutoFocus",
        "DetLight",
        "ChargedFlash",
        "WriteMemory",
    }


def test_final_boundary_terminates_runtime_instead_of_entering_end_leaf():
    lowered = _lower(22)
    model = load_state_machine_from_text(lowered["fcstm"])
    runtime = SimulationRuntime(model)

    runtime.cycle()
    runtime.cycle([f"{model.root_state.name}.keyOff"])

    assert runtime.is_ended is True
    assert runtime.brief_stack == []


def test_nested_final_stabilizes_then_outer_final_can_terminate():
    lowered = _lower(7)
    model = load_state_machine_from_text(lowered["fcstm"])
    runtime = SimulationRuntime(model)

    def event(name: str) -> list[str]:
        return [f"{model.root_state.name}.{name}"]

    runtime.cycle()
    runtime.cycle(event("Frontend_Collision_Detected"))
    assert runtime.current_state.path[-2:] == ("BrakingControl", "ActivateABS")
    runtime.cycle(event("Immediate_Action_Required"))
    assert runtime.current_state.path[-1] == "ApplyBrakes"
    runtime.cycle(event("Collision_Avoided"))
    assert runtime.current_state.path[-2] == "BrakingControl"
    assert runtime.current_state.path[-1].startswith("FinalWait")
    runtime.cycle(event("No_Collision_Risk"))

    assert runtime.is_ended is True


def test_cross_scope_deep_targets_remain_event_distinguished():
    lowered = _lower(7)
    model = load_state_machine_from_text(lowered["fcstm"])
    expectations = {
        "Frontend_Collision_Detected": "BrakingControl",
        "Rear_End_Collision_Detected": "SteeringControl",
        "Collision_With_Pedestrian_Detected": "AlertSystem",
    }

    for event_name, expected_branch in expectations.items():
        runtime = SimulationRuntime(model)
        runtime.cycle()
        runtime.cycle([f"{model.root_state.name}.{event_name}"])
        assert runtime.current_state.path[-2] == expected_branch


def test_all_60_outputs_parse_and_inspect_without_dropped_source_transitions():
    rows = _rows()
    assert len(rows) == 60

    totals = {
        "source": 0,
        "mapped": 0,
        "blocked": 0,
        "final_source": 0,
        "final_mapped": 0,
        "exact": 0,
    }
    blocker_reasons: dict[str, int] = {}
    for row in rows:
        canonical = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
        lowered = lower_plantuml_source(canonical)
        model = load_state_machine_from_text(lowered["fcstm"])
        report = inspect_model(model).to_json()

        assert report["metrics"]["n_states_leaf"] + report["metrics"]["n_states_composite"] > 0
        assert lowered["comparison"]["source_transition_count"] == len(
            canonical["model"]["transitions"]
        )
        assert lowered["comparison"]["mapped_transition_count"] + lowered[
            "comparison"
        ]["blocked_transition_count"] == len(canonical["model"]["transitions"])
        assert lowered["comparison"]["silently_dropped_transition_count"] == 0
        totals["source"] += lowered["comparison"]["source_transition_count"]
        totals["mapped"] += lowered["comparison"]["mapped_transition_count"]
        totals["blocked"] += lowered["comparison"]["blocked_transition_count"]
        totals["exact"] += lowered["comparison"]["verdict"] == "exact_r45_structure"
        final_mapped, final_source = map(
            int, lowered["comparison"]["final_transition_coverage"].split("/")
        )
        totals["final_source"] += final_source
        totals["final_mapped"] += final_mapped
        for blocker in lowered["comparison"]["blockers"]:
            reason = blocker["reason_code"]
            blocker_reasons[reason] = blocker_reasons.get(reason, 0) + 1

    assert totals == {
        "source": 754,
        "mapped": 719,
        "blocked": 35,
        "final_source": 36,
        "final_mapped": 36,
        "exact": 19,
    }
    assert blocker_reasons == {
        "R45.BLOCKED.missing_explicit_initial": 33,
        "R45.BLOCKED.initial_target_not_direct_child": 6,
        "R45.BLOCKED.initial_target_composite_missing_initial": 2,
        "R45.BLOCKED.target_composite_missing_initial": 27,
        "R45.BLOCKED.lifecycle_owner_ambiguous": 1,
        "R45.BLOCKED.explicit_concurrency_pseudostate": 1,
        "R45.BLOCKED.ambiguous_unlabeled_fanout": 16,
        "R45.BLOCKED.multiple_initial_fanout": 4,
        "R45.BLOCKED.opaque_state_body_not_executable": 96,
    }
