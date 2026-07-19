from __future__ import annotations

import hashlib
import importlib.util
import json
import re
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
RUNNER = (
    REPO_ROOT
    / "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion"
    / "tools/run_llms_emp_r45.py"
)
EVIDENCE = (
    REPO_ROOT
    / "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation"
    / "reports/llms_emp_r45_java_60"
)
PAIR_INDEX = EVIDENCE / "PAIR_INDEX.md"
PAIR_PAGES = EVIDENCE / "pairs"
FCSTM_SET_SHA256 = "591ff856f8a8985b1fcc1682d76193efeaea416be11ae84c64231abf00e17a82"
MANUAL_ROW_RE = re.compile(
    r"^\| `(?P<case>\d{4})` \| `(?P<source>[0-9a-f]{64})` \| "
    r"`(?P<fcstm>[0-9a-f]{64})` \| PASS \| (?P<notes>.+) \|$"
)


def _rows() -> list[dict]:
    return [json.loads(line) for line in PAIRS.read_text(encoding="utf-8").splitlines()]


def _row(index: int) -> dict:
    return _rows()[index]


def _load_runner_module():
    spec = importlib.util.spec_from_file_location("run_llms_emp_r45", RUNNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def test_empty_state_block_remains_explicit_source_syntax_fact():
    row = _row(4)
    result = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    states = {state["id"]: state for state in result["model"]["states"]}

    assert states["DoorsClosing"]["kind"] == "state"
    assert states["DoorsClosing"]["attributes"]["declared_with_block"] is True
    assert states["Stopping"]["attributes"]["declared_with_block"] is False


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


def test_batch_runner_rejects_uninitialized_pyfcstm_submodule(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    runner = _load_runner_module()
    monkeypatch.setattr(runner, "PYFCSTM_SRC", tmp_path)

    with pytest.raises(RuntimeError, match="submodule is not initialized"):
        runner._checked_out_pyfcstm_commit()


def test_batch_runner_records_checked_out_pyfcstm_gitlink():
    runner = _load_runner_module()
    expected_commit = runner._git("ls-tree", "HEAD", "pyfcstm").split()[2]

    assert runner._checked_out_pyfcstm_commit() == expected_commit


def test_batch_runner_refuses_to_overwrite_reviewed_output(tmp_path: Path):
    runner = _load_runner_module()
    output_dir = tmp_path / "reviewed-output"
    output_dir.mkdir()
    manual_review = output_dir / "MANUAL_REVIEW.md"
    manual_review.write_text("reviewed\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="reviewed output is frozen"):
        runner._prepare_output_dir(output_dir)

    assert manual_review.read_text(encoding="utf-8") == "reviewed\n"


def test_committed_60_pair_manual_review_matches_frozen_sources_and_fcstm():
    manual_text = (EVIDENCE / "MANUAL_REVIEW.md").read_text(encoding="utf-8")
    manual_rows = [
        match.groupdict()
        for line in manual_text.splitlines()
        if (match := MANUAL_ROW_RE.fullmatch(line)) is not None
    ]
    assert [row["case"] for row in manual_rows] == [f"{index:04d}" for index in range(60)]
    assert all(row["notes"].strip() for row in manual_rows)

    source_rows = {row["pair_id"][-4:]: row for row in _rows()}
    comparison_rows = {
        row["case_id"]: row
        for row in (
            json.loads(line)
            for line in (EVIDENCE / "comparison.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        )
    }
    assert set(source_rows) == set(comparison_rows) == {row["case"] for row in manual_rows}

    for row in manual_rows:
        case_id = row["case"]
        fcstm_path = EVIDENCE / "fcstm" / f"llms_emp_stm_results_{case_id}.fcstm"
        actual_fcstm_sha256 = hashlib.sha256(fcstm_path.read_bytes()).hexdigest()
        assert row["source"] == source_rows[case_id]["stm0_sha256"]
        assert row["source"] == comparison_rows[case_id]["source_sha256"]
        assert row["fcstm"] == comparison_rows[case_id]["fcstm_sha256"]
        assert row["fcstm"] == actual_fcstm_sha256
        assert comparison_rows[case_id]["verdict"] == "structure_preserved"
        assert comparison_rows[case_id]["fcstm_execution_eligible"] is False
        assert comparison_rows[case_id]["discover_eligible"] is False

    collection_payload = "".join(
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  "
        f"{path.relative_to(REPO_ROOT).as_posix()}\n"
        for path in sorted((EVIDENCE / "fcstm").glob("*.fcstm"))
    ).encode("utf-8")
    assert hashlib.sha256(collection_payload).hexdigest() == FCSTM_SET_SHA256
    assert "不表示行为等价" in manual_text


def test_committed_pair_pages_show_complete_nl_plantuml_and_fcstm_for_all_60_cases():
    index_text = PAIR_INDEX.read_text(encoding="utf-8")
    source_rows = {row["pair_id"][-4:]: row for row in _rows()}
    assert sorted(path.name for path in PAIR_PAGES.iterdir() if path.is_dir()) == [
        f"{index:04d}" for index in range(60)
    ]
    assert list(PAIR_PAGES.glob("[0-9][0-9][0-9][0-9].md")) == []

    for case_id, source_row in source_rows.items():
        pair_id = source_row["pair_id"]
        fcstm_text = (EVIDENCE / "fcstm" / f"{pair_id}.fcstm").read_text(
            encoding="utf-8"
        )
        case_dir = PAIR_PAGES / case_id
        page_text = (case_dir / "README.md").read_text(encoding="utf-8")
        display_nl = "\n".join(
            line.rstrip() for line in source_row["nl_text"].splitlines()
        )
        nl_suffix = "" if display_nl.endswith("\n") else "\n"
        source_suffix = "" if source_row["stm0_text"].endswith("\n") else "\n"
        fcstm_suffix = "" if fcstm_text.endswith("\n") else "\n"
        assert f"```text\n{display_nl}{nl_suffix}```" in page_text
        assert f"```plantuml\n{source_row['stm0_text']}{source_suffix}```" in page_text
        assert f"```fcstm\n{fcstm_text}{fcstm_suffix}```" in page_text
        assert (case_dir / "nl.txt").read_text(encoding="utf-8") == source_row["nl_text"]
        assert (case_dir / "plantuml.puml").read_text(
            encoding="utf-8"
        ) == source_row["stm0_text"]
        assert (case_dir / "fcstm.fcstm").read_text(encoding="utf-8") == fcstm_text
        assert source_row["nl_sha256"] in page_text
        assert source_row["stm0_sha256"] in page_text
        assert f"./pairs/{case_id}/README.md" in index_text
        assert f"./pairs/{case_id}/nl.txt" in index_text
        assert f"./pairs/{case_id}/plantuml.puml" in index_text
        assert f"./pairs/{case_id}/fcstm.fcstm" in index_text
        assert f"../../case_reports/{pair_id}.json" in page_text
