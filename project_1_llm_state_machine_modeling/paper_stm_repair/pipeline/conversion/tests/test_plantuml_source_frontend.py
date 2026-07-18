from __future__ import annotations

import json
from pathlib import Path

import pytest

from paper_stm_repair_conversion.adapters.plantuml_source import (
    parse_plantuml_source,
    resolve_plantuml_jar,
)


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


def _row(index: int) -> dict:
    return _rows()[index]


def test_scope_resolution_keeps_repeated_children_distinct_and_root_target_rooted():
    row = _row(0)
    result = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    states = {state["id"]: state for state in result["model"]["states"]}
    transitions = result["model"]["transitions"]

    assert "Autonomous" in states
    assert "HumanDriving.Autonomous" not in states
    assert "HumanDriving.InitialState" in states
    assert "Autonomous.InitialState" in states
    assert "Autonomous.FinalState" in states
    assert any(
        transition["source"] == "HumanDriving.InitialState"
        and transition["target"] == "Autonomous"
        for transition in transitions
    )


def test_final_transition_is_a_boundary_not_an_ordinary_end_state():
    row = _row(22)
    result = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    states = {state["id"] for state in result["model"]["states"]}
    finals = [
        transition
        for transition in result["model"]["transitions"]
        if transition["attributes"]["transition_kind"] == "final"
    ]

    assert "end" not in states
    assert len(finals) == 1
    assert finals[0]["source"] == "PoweredOn"
    assert finals[0]["target"] == "@final:__root__"
    assert finals[0]["label"] == "keyOff"


def test_lifecycle_actions_survive_source_frontend():
    row = _row(54)
    result = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    states = {state["id"]: state for state in result["model"]["states"]}

    assert states["InMotion.Accelerating"]["kind"] == "state"
    assert states["InMotion.Approaching"]["kind"] == "state"
    assert states["EmergencyStopping"]["kind"] == "state"

    assert [
        (item["kind"], item["text"])
        for item in states["InMotion.Accelerating"]["attributes"]["lifecycle_actions"]
    ] == [("entry", "Accelerate")]
    assert [
        (item["kind"], item["text"])
        for item in states["InMotion.Approaching"]["attributes"]["lifecycle_actions"]
    ] == [("do", "Send")]
    assert [
        (item["kind"], item["text"])
        for item in states["EmergencyStopping"]["attributes"]["lifecycle_actions"]
    ] == [("do", "Emergency Stop"), ("do", "Send Obstacle Detected")]


def test_unique_later_nested_state_is_resolved_instead_of_implicitly_duplicated():
    row = _row(7)
    result = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    states = {state["id"] for state in result["model"]["states"]}
    transition = next(
        item
        for item in result["model"]["transitions"]
        if item["event"] == "Frontend Collision Detected"
    )

    assert transition["target"] == "CollisionAvoidance.BrakingControl"
    assert "InitialState.BrakingControl" not in states


def test_out_of_block_body_line_resolves_unique_explicit_alias():
    row = _row(58)
    result = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    states = {state["id"]: state for state in result["model"]["states"]}

    assert "TurnOn_state" not in states
    assert [
        item["text"]
        for item in states["TurnOn.TurnOn_state"]["attributes"]["body_lines"]
    ] == ["{max=2s, min=2s}"]


def test_all_60_pairs_have_complete_source_transition_coverage():
    rows = _rows()
    assert len(rows) == 60

    parsed_transition_count = 0
    parsed_state_count = 0
    lifecycle_count = 0
    orphan_lifecycle_count = 0
    raw_official_statuses: dict[str, int] = {}
    normalized_official_statuses: dict[str, int] = {}
    official_validation_link_count = 0
    official_link_deltas: dict[str, int] = {}
    for row in rows:
        result = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
        assert result["metadata"]["unparsed_semantic_lines"] == []
        assert result["metadata"]["source_transition_count"] == len(
            result["model"]["transitions"]
        )
        parsed_transition_count += len(result["model"]["transitions"])
        parsed_state_count += len(result["model"]["states"])
        lifecycle_count += sum(
            len(state["attributes"]["lifecycle_actions"])
            for state in result["model"]["states"]
        )
        orphan_lifecycle_count += len(result["metadata"]["orphan_lifecycle_actions"])
        raw_status = result["metadata"]["official_model"]["status"]
        raw_official_statuses[raw_status] = raw_official_statuses.get(raw_status, 0) + 1
        normalized_status = result["metadata"]["official_validation"]["model"]["status"]
        normalized_official_statuses[normalized_status] = (
            normalized_official_statuses.get(normalized_status, 0) + 1
        )
        official_links = result["metadata"]["official_validation"]["model"]["counts"]["links"]
        official_validation_link_count += official_links
        delta = official_links - len(result["model"]["transitions"])
        if delta:
            official_link_deltas[row["pair_id"][-4:]] = delta

    assert parsed_transition_count == 754
    assert parsed_state_count == 524
    assert lifecycle_count == 18
    assert orphan_lifecycle_count == 1
    assert raw_official_statuses == {"state_diagram": 33, "not_state_diagram": 27}
    assert normalized_official_statuses == {"state_diagram": 60}
    assert official_validation_link_count == 755
    assert official_link_deltas == {"0019": 1}


def test_official_internal_model_is_differential_evidence_not_canonical_truth():
    row = _row(0)
    result = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    source_states = {state["id"] for state in result["model"]["states"]}
    official_states = {
        entity["qualified_name"]
        for entity in result["metadata"]["official_validation"]["model"]["entities"]
    }

    assert "Autonomous" in source_states
    assert "HumanDriving.Autonomous" not in source_states
    assert "HumanDriving.Autonomous" in official_states


def test_official_note_attachment_is_identifiable_as_non_behavior_link():
    row = _row(19)
    result = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    note_links = [
        link
        for link in result["metadata"]["official_validation"]["model"]["links"]
        if link["source_kind"] == "LEAF:NOTE" or link["target_kind"] == "LEAF:NOTE"
    ]

    assert len(note_links) == 1
    assert note_links[0]["type"].startswith("NONE-DASHED")


def test_wrapper_rejects_wrong_plantuml_jar_identity(tmp_path: Path):
    fake_jar = tmp_path / "plantuml.jar"
    fake_jar.write_bytes(b"not the pinned official jar")

    with pytest.raises(RuntimeError, match="identity mismatch"):
        resolve_plantuml_jar(fake_jar)
