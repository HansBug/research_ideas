from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from paper_stm_repair_conversion.adapters.plantuml_source import parse_plantuml_source
from paper_stm_repair_representation.plantuml_source_audit import audit_lowered_artifact
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


def test_unlabeled_fanout_is_structurally_preserved_with_operational_debt():
    lowered = _lower(53)

    assert "PumpState -> WaterState;" in lowered["fcstm"]
    assert "PumpState -> MethaneState;" in lowered["fcstm"]
    assert lowered["comparison"]["structural_verdict"] == "structure_preserved"
    reasons = {
        item["reason_code"] for item in lowered["comparison"]["operational_debts"]
    }
    assert "R45.DEBT.ambiguous_unlabeled_fanout" in reasons


def test_transition_to_composite_without_initial_stops_at_explicit_placeholder():
    lowered = _lower(5)
    mapped = {
        item["transition_id"]: item
        for item in lowered["comparison"]["transition_mappings"]
        if item["status"] == "mapped"
    }

    assert mapped["tr_0003"]["reason_code"] == "R45.MAP.direct_sibling"
    assert mapped["tr_0006"]["reason_code"] == "R45.MAP.descendant_to_ancestor_reentry"
    assert "DoorShut -> DoorOpen : /Door_Opened;" in lowered["fcstm"]
    assert 'state UnspecifiedInitial named "Unspecified initial";' in lowered["fcstm"]
    debts = {item["reason_code"] for item in lowered["comparison"]["operational_debts"]}
    assert "R45.DEBT.missing_explicit_initial" in debts


def test_initial_to_composite_without_child_initial_is_structurally_preserved():
    lowered = _lower(57)
    mapping = next(
        item
        for item in lowered["comparison"]["transition_mappings"]
        if item["transition_id"] == "tr_0010"
    )

    assert mapping["status"] == "mapped"
    assert mapping["reason_code"] == "R45.MAP.initial_boundary"
    assert "InitialWaittr_0010 -> CA : /Possible_collision_detected;" in lowered["fcstm"]
    assert 'state UnspecifiedInitial named "Unspecified initial";' in lowered["fcstm"]


def test_opaque_state_body_is_preserved_in_fcstm_display_name_and_trace():
    lowered = _lower(48)
    mappings = [
        item
        for item in lowered["comparison"]["body_mappings"]
        if item["representation"] == "state_display_name"
    ]

    assert {item["state_id"] for item in mappings} >= {
        "TurnOn",
        "AutoFocus",
        "DetLight",
        "ChargedFlash",
        "WriteMemory",
    }
    for item in mappings:
        assert item["text"] in lowered["fcstm"]
        assert item["raw_ref"]
    assert lowered["comparison"]["body_line_coverage"] == "5/5"


def test_invalid_self_initial_is_preserved_as_a_stoppable_surrogate():
    lowered = _lower(4)
    mapping = next(
        item
        for item in lowered["comparison"]["transition_mappings"]
        if item["transition_id"] == "tr_0002"
    )

    assert mapping["status"] == "mapped"
    assert mapping["reason_code"] == "R45.MAP.invalid_source_initial_surrogate"
    assert mapping["emitted"][0]["generated_role"] == "invalid_source_initial_surrogate"
    assert "PlantUML initial target outside child scope: DoorsClosing" in lowered["fcstm"]


def test_ownerless_lifecycle_is_preserved_as_root_display_metadata():
    lowered = _lower(24)
    orphan = lowered["comparison"]["orphan_lifecycle_mappings"]

    assert len(orphan) == 1
    assert orphan[0]["representation"] == "root_display_name"
    assert orphan[0]["text"] in lowered["fcstm"]
    assert lowered["comparison"]["lifecycle_action_coverage"] == "3/3"
    assert lowered["comparison"]["abstract_lifecycle_hook_coverage"] == "2/3"


def test_multiple_initial_edges_are_all_preserved_with_operational_debt():
    lowered = _lower(27)
    initial_mappings = [
        item
        for item in lowered["comparison"]["transition_mappings"]
        if item["transition_id"] in {"tr_0003", "tr_0004", "tr_0005"}
    ]

    assert all(item["status"] == "mapped" and item["emitted"] for item in initial_mappings)
    assert "[*] -> BrakeControlState;" in lowered["fcstm"]
    assert "[*] -> SteeringControlState;" in lowered["fcstm"]
    assert "[*] -> SensorControlState;" in lowered["fcstm"]
    assert any(
        item["reason_code"] == "R45.DEBT.multiple_initial_fanout"
        for item in lowered["comparison"]["operational_debts"]
    )


def test_ast_audit_rejects_trace_parent_drift():
    row = _rows()[0]
    canonical = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    lowered = lower_plantuml_source(canonical)
    model = load_state_machine_from_text(lowered["fcstm"])
    report = inspect_model(model).to_json()
    tampered = copy.deepcopy(lowered["comparison"])
    tampered["state_mappings"][0]["fcstm_parent_path"] = "wrong.parent"

    with pytest.raises(ValueError, match="parent mismatch"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=lowered["fcstm"],
            comparison=tampered,
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_missing_emitted_transition_occurrence():
    row = _rows()[22]
    canonical = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    lowered = lower_plantuml_source(canonical)
    removed = "PoweredOn -> [*] : /keyOff;"
    tampered_fcstm = lowered["fcstm"].replace(removed, "", 1)
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="authored transition multiset"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=lowered["comparison"],
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_joint_lowering_and_trace_endpoint_drift():
    row = _rows()[22]
    canonical = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    lowered = lower_plantuml_source(canonical)
    tampered = copy.deepcopy(lowered["comparison"])
    mapping = next(
        item for item in tampered["transition_mappings"] if item["transition_id"] == "tr_0002"
    )
    original = mapping["emitted"][0]["line"]
    rewritten = original.replace("PoweredOn -> Operate", "PoweredOn -> PoweredOn")
    mapping["emitted"][0]["line"] = rewritten
    tampered_fcstm = lowered["fcstm"].replace(original, rewritten, 1)
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="endpoint projection drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=tampered,
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_cross_scope_exit_retargeted_inside_scope():
    row = _rows()[0]
    canonical = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    lowered = lower_plantuml_source(canonical)
    tampered = copy.deepcopy(lowered["comparison"])
    mapping = next(
        item for item in tampered["transition_mappings"] if item["transition_id"] == "tr_0003"
    )
    exit_segment = next(
        item
        for item in mapping["emitted"]
        if item["generated_role"] == "cross_scope_exit_segment"
    )
    original = exit_segment["line"]
    rewritten = original.replace("-> [*]", "-> FinalState")
    exit_segment["line"] = rewritten
    tampered_fcstm = lowered["fcstm"].replace(original, rewritten, 1)
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="cross-scope exit projection drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=tampered,
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_untracked_extra_transition():
    row = _rows()[22]
    canonical = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    lowered = lower_plantuml_source(canonical)
    prefix, suffix = lowered["fcstm"].rsplit("}\n", 1)
    tampered_fcstm = prefix + "    PoweredOn -> Braking : /start;\n}\n" + suffix
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="authored transition multiset"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=lowered["comparison"],
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_joint_event_binding_drift():
    row = _rows()[22]
    canonical = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    lowered = lower_plantuml_source(canonical)
    tampered = copy.deepcopy(lowered["comparison"])
    mapping = next(
        item for item in tampered["transition_mappings"] if item["transition_id"] == "tr_0002"
    )
    original = mapping["emitted"][0]["line"]
    rewritten = original.replace("/start", "/keyOff")
    mapping["emitted"][0]["line"] = rewritten
    tampered_fcstm = lowered["fcstm"].replace(original, rewritten, 1)
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="event projection drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=tampered,
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_event_initial_wait_disconnect():
    row = _rows()[16]
    canonical = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    lowered = lower_plantuml_source(canonical)
    tampered = copy.deepcopy(lowered["comparison"])
    mapping = next(
        item for item in tampered["transition_mappings"] if item["transition_id"] == "tr_0001"
    )
    main = next(
        item
        for item in mapping["emitted"]
        if item["generated_role"] == "source_initial_transition"
    )
    original = main["line"]
    rewritten = original.replace("InitialWaittr_0001", "FormationAdjust")
    main["line"] = rewritten
    tampered_fcstm = lowered["fcstm"].replace(original, rewritten, 1)
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="initial transition endpoint projection drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=tampered,
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_composite_force_loss():
    row = _rows()[12]
    canonical = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    lowered = lower_plantuml_source(canonical)
    tampered = copy.deepcopy(lowered["comparison"])
    mapping = next(
        item
        for item in tampered["transition_mappings"]
        if item["emitted"][0]["line"].startswith("!Operate -> Off")
    )
    original = mapping["emitted"][0]["line"]
    assert original.startswith("!")
    rewritten = original[1:]
    mapping["emitted"][0]["line"] = rewritten
    tampered_fcstm = lowered["fcstm"].replace(original, rewritten, 1)
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="endpoint projection drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=tampered,
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_nested_final_target_drift():
    row = _rows()[16]
    canonical = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    lowered = lower_plantuml_source(canonical)
    tampered = copy.deepcopy(lowered["comparison"])
    mapping = next(
        item for item in tampered["transition_mappings"] if item["transition_id"] == "tr_0005"
    )
    terminal = next(
        item
        for item in mapping["emitted"]
        if item["generated_role"] == "nested_final_completion_hold"
    )
    original = terminal["line"]
    rewritten = original.replace("FinalWaittr_0005", "Area1")
    terminal["line"] = rewritten
    tampered_fcstm = lowered["fcstm"].replace(original, rewritten, 1)
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="nested final boundary projection drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=tampered,
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_fail_closed_placeholder_retargeted_to_real_child():
    row = _rows()[5]
    canonical = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    lowered = lower_plantuml_source(canonical)
    tampered = copy.deepcopy(lowered["comparison"])
    mapping = next(
        item
        for item in tampered["synthetic_transition_mappings"]
        if item["scope"] == "DoorOpen"
    )
    original = mapping["line"]
    rewritten = "[*] -> DoorOpenWithItem;"
    mapping["line"] = rewritten
    tampered_fcstm = lowered["fcstm"].replace(original, rewritten, 1)
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="synthetic initial target/reason drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=tampered,
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_multiple_initial_declaration_reordering():
    row = _rows()[27]
    canonical = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    lowered = lower_plantuml_source(canonical)
    first = "[*] -> BrakeControlState;"
    second = "[*] -> SteeringControlState;"
    tampered_fcstm = lowered["fcstm"].replace(first, "<FIRST>", 1)
    tampered_fcstm = tampered_fcstm.replace(second, first, 1).replace("<FIRST>", second, 1)
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="initial transition declaration order drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=lowered["comparison"],
            model=model,
            inspect_report=report,
        )


def test_event_specific_deep_entry_precedes_composite_default_initial():
    source = """@startuml
[*] --> Outside
state Outside
state C {
    [*] --> Default
    state Default
    state Wanted
}
Outside --> C.Wanted : Go
@enduml
"""
    canonical = parse_plantuml_source(source, example_id="priority_probe")
    lowered = lower_plantuml_source(canonical)
    assert lowered["fcstm"].index("[*] -> Wanted : /Go;") < lowered["fcstm"].index(
        "[*] -> Default;"
    )
    model = load_state_machine_from_text(lowered["fcstm"])
    report = inspect_model(model).to_json()
    audit_lowered_artifact(
        canonical=canonical,
        fcstm=lowered["fcstm"],
        comparison=lowered["comparison"],
        model=model,
        inspect_report=report,
    )
    wanted = "[*] -> Wanted : /Go;"
    default = "[*] -> Default;"
    tampered_fcstm = lowered["fcstm"].replace(wanted, "<WANTED>", 1)
    tampered_fcstm = tampered_fcstm.replace(default, wanted, 1).replace(
        "<WANTED>", default, 1
    )
    tampered_model = load_state_machine_from_text(tampered_fcstm)
    tampered_report = inspect_model(tampered_model).to_json()
    with pytest.raises(ValueError, match="transition-specific entry priority drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=lowered["comparison"],
            model=tampered_model,
            inspect_report=tampered_report,
        )
    runtime = SimulationRuntime(model)
    runtime.cycle()
    runtime.cycle([f"{model.root_state.name}.Go"])
    assert runtime.current_state.path[-2:] == ("C", "Wanted")


def test_deep_source_initial_precedes_nested_default_initial():
    source = """@startuml
state C {
    [*] --> Default
    state Default
    state Wanted
}
[*] --> C.Wanted
@enduml
"""
    canonical = parse_plantuml_source(source, example_id="deep_initial_priority_probe")
    lowered = lower_plantuml_source(canonical)
    assert lowered["fcstm"].index("[*] -> Wanted;") < lowered["fcstm"].index(
        "[*] -> Default;"
    )
    model = load_state_machine_from_text(lowered["fcstm"])
    runtime = SimulationRuntime(model)
    runtime.cycle()
    assert runtime.current_state.path[-2:] == ("C", "Wanted")


def test_ast_audit_rejects_opaque_body_metadata_loss():
    row = _rows()[53]
    canonical = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    lowered = lower_plantuml_source(canonical)
    body_text = lowered["comparison"]["body_mappings"][0]["text"]
    tampered_fcstm = lowered["fcstm"].replace(body_text, "<removed>", 1)
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="display metadata mismatch|body missing"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=lowered["comparison"],
            model=model,
            inspect_report=report,
        )


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


def test_all_60_outputs_preserve_every_source_element_and_parse_inspect():
    rows = _rows()
    assert len(rows) == 60

    totals = {
        "source": 0,
        "mapped": 0,
        "blocked": 0,
        "final_source": 0,
        "final_mapped": 0,
        "structure_preserved": 0,
        "body_source": 0,
        "body_mapped": 0,
        "lifecycle_source": 0,
        "lifecycle_mapped": 0,
    }
    debt_reasons: dict[str, int] = {}
    for row in rows:
        canonical = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
        lowered = lower_plantuml_source(canonical)
        model = load_state_machine_from_text(lowered["fcstm"])
        report = inspect_model(model).to_json()
        ast_audit = audit_lowered_artifact(
            canonical=canonical,
            fcstm=lowered["fcstm"],
            comparison=lowered["comparison"],
            model=model,
            inspect_report=report,
        )

        assert report["metrics"]["n_states_leaf"] + report["metrics"]["n_states_composite"] > 0
        assert not [
            item for item in report["diagnostics"] if item.get("severity") == "error"
        ]
        assert ast_audit["status"] == "passed"
        assert lowered["comparison"]["source_transition_count"] == len(
            canonical["model"]["transitions"]
        )
        assert lowered["comparison"]["mapped_transition_count"] == len(
            canonical["model"]["transitions"]
        )
        assert lowered["comparison"]["blocked_transition_count"] == 0
        assert lowered["comparison"]["silently_dropped_transition_count"] == 0
        assert lowered["comparison"]["fcstm_execution_eligible"] is False
        assert lowered["comparison"]["discover_eligible"] is False
        assert all(
            mapping["status"] == "mapped" and mapping["emitted"]
            for mapping in lowered["comparison"]["transition_mappings"]
        )
        assert all(
            emitted["line"] in lowered["fcstm"]
            for mapping in lowered["comparison"]["transition_mappings"]
            for emitted in mapping["emitted"]
        )
        assert lowered["comparison"]["state_coverage"] == (
            f"{len(canonical['model']['states'])}/{len(canonical['model']['states'])}"
        )
        assert len(lowered["comparison"]["state_mappings"]) == len(
            canonical["model"]["states"]
        )
        totals["source"] += lowered["comparison"]["source_transition_count"]
        totals["mapped"] += lowered["comparison"]["mapped_transition_count"]
        totals["blocked"] += lowered["comparison"]["blocked_transition_count"]
        totals["structure_preserved"] += (
            lowered["comparison"]["structural_verdict"] == "structure_preserved"
        )
        body_mapped, body_source = map(
            int, lowered["comparison"]["body_line_coverage"].split("/")
        )
        lifecycle_mapped, lifecycle_source = map(
            int, lowered["comparison"]["lifecycle_action_coverage"].split("/")
        )
        totals["body_source"] += body_source
        totals["body_mapped"] += body_mapped
        totals["lifecycle_source"] += lifecycle_source
        totals["lifecycle_mapped"] += lifecycle_mapped
        final_mapped, final_source = map(
            int, lowered["comparison"]["final_transition_coverage"].split("/")
        )
        totals["final_source"] += final_source
        totals["final_mapped"] += final_mapped
        for debt in lowered["comparison"]["operational_debts"]:
            reason = debt["reason_code"]
            debt_reasons[reason] = debt_reasons.get(reason, 0) + 1

    assert totals == {
        "source": 754,
        "mapped": 754,
        "blocked": 0,
        "final_source": 36,
        "final_mapped": 36,
        "structure_preserved": 60,
        "body_source": 96,
        "body_mapped": 96,
        "lifecycle_source": 19,
        "lifecycle_mapped": 19,
    }
    assert debt_reasons == {
        "R45.DEBT.missing_explicit_initial": 31,
        "R45.DEBT.invalid_source_initial_target": 6,
        "R45.DEBT.lifecycle_owner_ambiguous": 1,
        "R45.DEBT.explicit_concurrency_pseudostate": 1,
        "R45.DEBT.ambiguous_unlabeled_fanout": 16,
        "R45.DEBT.multiple_initial_fanout": 4,
        "R45.DEBT.opaque_state_body_semantics": 96,
        "R45.DEBT.opaque_transition_label_semantics": 525,
    }
