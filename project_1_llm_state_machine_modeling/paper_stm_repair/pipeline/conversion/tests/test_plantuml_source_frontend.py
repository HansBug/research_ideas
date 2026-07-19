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
    / "llms-emp-stm-subset/assets/extracted/feedback_final_pairs.jsonl"
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


def _require_feedback_final_evidence() -> None:
    first_pair = _rows()[0]["pair_id"]
    if not (EVIDENCE / "fcstm" / f"{first_pair}.fcstm").is_file():
        pytest.skip("Phase-II final frozen evidence has not been regenerated yet")


def test_scope_resolution_uses_official_first_created_qualified_identity():
    result = parse_plantuml_source(
        """@startuml
state HumanDriving {
  [*] --> InitialState
  InitialState --> Autonomous : switch
}
state Autonomous {
  [*] --> InitialState
  InitialState --> FinalState
}
@enduml
""",
        example_id="scope-fixture",
    )
    states = {state["id"]: state for state in result["model"]["states"]}
    transitions = result["model"]["transitions"]

    assert "Autonomous" not in states
    assert states["HumanDriving.Autonomous"]["kind"] == "composite"
    assert "HumanDriving.InitialState" in states
    assert "HumanDriving.Autonomous.InitialState" not in states
    assert "HumanDriving.Autonomous.FinalState" in states
    assert any(
        transition["source"] == "HumanDriving.InitialState"
        and transition["target"] == "HumanDriving.Autonomous"
        for transition in transitions
    )
    reconciliation = result["metadata"]["official_identity_reconciliation"]
    assert reconciliation["status"] == "aligned"
    assert reconciliation["canonical_state_count_after"] == 4
    assert reconciliation["official_state_count"] == 4
    autonomous_initial = next(
        transition
        for transition in transitions
        if transition["source"] == "@initial:HumanDriving.Autonomous"
    )
    assert autonomous_initial["scope"] == "HumanDriving.Autonomous"
    assert autonomous_initial["target"] == "HumanDriving.InitialState"


def test_final_transition_is_a_boundary_not_an_ordinary_end_state():
    result = parse_plantuml_source(
        """@startuml
[*] --> PoweredOn
PoweredOn --> [*] : keyOff
@enduml
""",
        example_id="final-fixture",
    )
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
    result = parse_plantuml_source(
        """@startuml
state InMotion {
  entry/Accelerate
  do/Send
  exit/Stop
  state Active
  [*] --> Active
}
@enduml
""",
        example_id="lifecycle-fixture",
    )
    states = {state["id"]: state for state in result["model"]["states"]}

    assert [
        (item["kind"], item["text"])
        for item in states["InMotion"]["attributes"]["lifecycle_actions"]
    ] == [("entry", "Accelerate"), ("do", "Send"), ("exit", "Stop")]


def test_empty_state_block_remains_an_official_composite_syntax_fact():
    result = parse_plantuml_source(
        """@startuml
state DoorsClosing {
}
state Stopping
@enduml
""",
        example_id="empty-block-fixture",
    )
    states = {state["id"]: state for state in result["model"]["states"]}

    assert states["DoorsClosing"]["kind"] == "composite"
    assert states["DoorsClosing"]["attributes"]["declared_with_block"] is True
    assert states["Stopping"]["attributes"]["declared_with_block"] is False


def test_all_supported_pseudostate_stereotypes_survive_source_frontend():
    result = parse_plantuml_source(
        """@startuml
state F <<fork>>
state J <<join>>
state C <<choice>>
state N <<junction>>
F --> C
C --> N
N --> J
@enduml
""",
        example_id="pseudostate-kind-fixture",
    )
    kinds = {state["id"]: state["kind"] for state in result["model"]["states"]}

    assert kinds == {"F": "fork", "J": "join", "C": "choice", "N": "junction"}


def test_later_nested_declaration_reuses_the_official_root_identity():
    result = parse_plantuml_source(
        """@startuml
[*] --> InitialState
InitialState --> BrakingControl : Frontend Collision Detected
state CollisionAvoidance {
  state BrakingControl
}
@enduml
""",
        example_id="forward-nested-fixture",
    )
    states = {state["id"] for state in result["model"]["states"]}
    transition = next(
        item
        for item in result["model"]["transitions"]
        if item["event"] == "Frontend Collision Detected"
    )

    assert transition["target"] == "BrakingControl"
    assert "CollisionAvoidance.BrakingControl" not in states
    assert "BrakingControl" in states


def test_official_identity_merge_keeps_declaration_body_and_lifecycle_evidence():
    result = parse_plantuml_source(
        """@startuml
[*] --> Seed
Seed --> Shared : create first
state Container {
  state Shared {
    entry/Prepare
    Shared : opaque body
  }
}
@enduml
""",
        example_id="official-identity-evidence-merge",
    )
    states = {state["id"]: state for state in result["model"]["states"]}

    assert "Container.Shared" not in states
    shared = states["Shared"]
    assert shared["kind"] == "composite"
    assert [item["text"] for item in shared["attributes"]["body_lines"]] == [
        "opaque body"
    ]
    assert [
        (item["kind"], item["text"])
        for item in shared["attributes"]["lifecycle_actions"]
    ] == [("entry", "Prepare")]
    assert any(
        item["raw"] == "state Shared {"
        for item in shared["attributes"]["declarations"]
    )


def test_layout_arrow_direction_is_restored_after_official_link_orientation():
    result = parse_plantuml_source(
        """@startuml
state A
state B
A -left-> B : left layout
B -up-> A : up layout
@enduml
""",
        example_id="official-layout-arrow-orientation",
    )

    assert [
        (item["source"], item["target"])
        for item in result["model"]["transitions"]
    ] == [("A", "B"), ("B", "A")]
    assert all(
        item["attributes"]["official_link_reversed_for_layout_arrow"] is True
        for item in result["model"]["transitions"]
    )


def test_root_transition_reuses_a_unique_implicit_nested_endpoint():
    result = parse_plantuml_source(
        """@startuml
state AutoFocus {
  choice1 --> Junction3 : ready
}
ChargedFlash --> Junction3 : charged
Junction3 --> Join2
@enduml
""",
        example_id="unique-implicit-cross-scope-fixture",
    )
    states = {state["id"] for state in result["model"]["states"]}
    transitions = result["model"]["transitions"]

    assert "AutoFocus.Junction3" in states
    assert "Junction3" not in states
    assert [
        (item["source"], item["target"])
        for item in transitions
        if item["attributes"]["raw_source"] in {"ChargedFlash", "Junction3"}
    ] == [
        ("ChargedFlash", "AutoFocus.Junction3"),
        ("AutoFocus.Junction3", "Join2"),
    ]


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
    body_count = 0
    lifecycle_count = 0
    orphan_lifecycle_count = 0
    separator_count = 0
    region_count = 0
    source_normalization_count = 0
    raw_official_statuses: dict[str, int] = {}
    normalized_official_statuses: dict[str, int] = {}
    official_validation_link_count = 0
    official_identity_state_count = 0
    official_identity_transition_count = 0
    official_link_deltas: dict[str, int] = {}
    for row in rows:
        result = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
        assert result["metadata"]["unparsed_semantic_lines"] == []
        assert result["metadata"]["source_transition_count"] == len(
            result["model"]["transitions"]
        )
        parsed_transition_count += len(result["model"]["transitions"])
        parsed_state_count += len(result["model"]["states"])
        body_count += sum(
            len(state["attributes"]["body_lines"])
            for state in result["model"]["states"]
        )
        lifecycle_count += sum(
            len(state["attributes"]["lifecycle_actions"])
            for state in result["model"]["states"]
        )
        orphan_lifecycle_count += len(result["metadata"]["orphan_lifecycle_actions"])
        separator_count += len(result["metadata"]["concurrent_region_separators"])
        region_count += len(result["model"]["concurrent_regions"])
        source_normalization_count += len(result["metadata"]["source_normalizations"])
        raw_status = result["metadata"]["official_model"]["status"]
        raw_official_statuses[raw_status] = raw_official_statuses.get(raw_status, 0) + 1
        normalized_status = result["metadata"]["official_validation"]["model"]["status"]
        normalized_official_statuses[normalized_status] = (
            normalized_official_statuses.get(normalized_status, 0) + 1
        )
        official_links = result["metadata"]["official_validation"]["model"]["counts"]["links"]
        official_validation_link_count += official_links
        reconciliation = result["metadata"]["official_identity_reconciliation"]
        assert reconciliation["status"] == "aligned"
        assert reconciliation["canonical_state_count_after"] == len(
            result["model"]["states"]
        )
        assert reconciliation["official_state_count"] == len(result["model"]["states"])
        assert reconciliation["transition_identity_alignment_count"] == len(
            result["model"]["transitions"]
        )
        official_identity_state_count += reconciliation["official_state_count"]
        official_identity_transition_count += reconciliation[
            "transition_identity_alignment_count"
        ]
        delta = official_links - len(result["model"]["transitions"])
        if delta:
            official_link_deltas[row["pair_id"][-4:]] = delta

    assert parsed_transition_count == 757
    assert parsed_state_count == 516
    assert body_count == 95
    assert lifecycle_count == 16
    assert orphan_lifecycle_count == 0
    assert separator_count == 20
    assert region_count == 29
    assert source_normalization_count == 6
    assert raw_official_statuses == {"state_diagram": 59, "not_state_diagram": 1}
    assert normalized_official_statuses == {"state_diagram": 60}
    assert official_validation_link_count == 757
    assert official_identity_state_count == 516
    assert official_identity_transition_count == 757
    assert official_link_deltas == {}


def test_named_startuml_marker_is_presentation_not_semantic_source():
    result = parse_plantuml_source(
        """@startuml MicrowaveStateMachine
[*] --> Idle
state Idle
@enduml
""",
        example_id="named-start-marker",
    )

    assert result["status"] == "converted"
    assert result["metadata"]["unparsed_semantic_lines"] == []
    start = result["metadata"]["ignored_presentation_lines"][0]
    assert start["reason"] == "plantuml_start_marker"
    assert start["diagram_name"] == "MicrowaveStateMachine"


def test_reopened_composite_keeps_0033_cross_scope_final_lexical_boundary():
    result = parse_plantuml_source(
        """@startuml
[*] --> PumpControl
PumpControl --> PumpState : activate
state PumpControl {
  [*] --> PumpState
  PumpState --> [*] : stopped
}
@enduml
""",
        example_id="reopened-boundary-fixture",
    )
    states = {item["id"] for item in result["model"]["states"]}
    final = next(
        item
        for item in result["model"]["transitions"]
        if item["attributes"]["transition_kind"] == "final"
    )

    assert "PumpState" in states
    assert "PumpControl.PumpState" not in states
    assert final["source"] == "PumpState"
    assert final["target"] == "@final:PumpControl"
    assert final["scope"] == "PumpControl"


def test_trailing_quote_on_plantuml_delimiter_is_audited_as_format_noise():
    row = _rows()[58]
    result = parse_plantuml_source(
        row["stm0_text"], example_id=row["pair_id"], source_name="phase2-0058.puml"
    )

    assert result["metadata"]["unparsed_semantic_lines"] == []
    assert {
        item.get("reason") for item in result["metadata"]["ignored_presentation_lines"]
    } == {"plantuml_start_marker", "plantuml_end_marker"}
    recoveries = result["metadata"]["source_normalizations"]
    assert len(recoveries) == 6
    assert sum(
        item["rule_id"] == "source_input.workbook_doubled_state_quotes"
        for item in recoveries
    ) == 5
    assert sum(
        item["rule_id"] == "source_input.workbook_trailing_end_quote"
        for item in recoveries
    ) == 1
    states = {item["id"]: item for item in result["model"]["states"]}
    assert "TurnOn.TurnOn_state" in states
    assert states["TurnOn.TurnOn_state"]["attributes"]["body_lines"][0]["text"] == (
        "{max=2s, min=2s}"
    )
    assert not any('""' in state_id for state_id in states)
    validation = result["metadata"]["official_validation"]
    assert validation["model"]["status"] == "state_diagram"
    assert validation["source_input_normalizations"] == recoveries


def test_concurrent_region_separator_is_preserved_as_canonical_metadata():
    result = parse_plantuml_source(
        """@startuml
state Parallel {
  [*] --> LeftIdle
  LeftIdle --> LeftDone : left
  --
  [*] --> RightIdle
  RightIdle --> RightDone : right
}
@enduml
""",
        example_id="parallel-regions",
        source_name="parallel-regions.puml",
    )

    assert result["metadata"]["unparsed_semantic_lines"] == []
    assert len(result["metadata"]["concurrent_region_separators"]) == 1
    regions = result["model"]["concurrent_regions"]
    assert [(item["owner_scope"], item["region_index"]) for item in regions] == [
        ("Parallel", 0),
        ("Parallel", 1),
    ]
    assert regions[0]["state_ids"] == ["Parallel.LeftIdle", "Parallel.LeftDone"]
    assert regions[1]["state_ids"] == ["Parallel.RightIdle", "Parallel.RightDone"]
    assert regions[0]["transition_ids"] == ["tr_0001", "tr_0002"]
    assert regions[1]["transition_ids"] == ["tr_0003", "tr_0004"]


def test_official_internal_model_is_the_qualified_identity_oracle():
    result = parse_plantuml_source(
        """@startuml
state HumanDriving {
  [*] --> InitialState
  InitialState --> Autonomous : switch
}
state Autonomous {
  [*] --> InitialState
}
@enduml
""",
        example_id="official-forward-reference-fixture",
    )
    source_states = {state["id"] for state in result["model"]["states"]}
    official_states = {
        entity["qualified_name"]
        for entity in result["metadata"]["official_validation"]["model"]["entities"]
    }

    assert "Autonomous" not in source_states
    assert "HumanDriving.Autonomous" in source_states
    assert "HumanDriving.Autonomous" in official_states
    audit = result["metadata"]["official_identity_reconciliation"]
    assert audit["status"] == "aligned"
    assert audit["canonical_state_count_after"] == audit["official_state_count"]


def test_official_note_attachment_is_identifiable_as_non_behavior_link():
    result = parse_plantuml_source(
        """@startuml
[*] --> Active
note right of Active : presentation only
@enduml
""",
        example_id="official-note-fixture",
    )
    note_links = [
        link
        for link in result["metadata"]["official_validation"]["model"]["links"]
        if link["source_kind"] == "LEAF:NOTE" or link["target_kind"] == "LEAF:NOTE"
    ]

    assert len(note_links) == 1
    assert note_links[0]["type"].startswith("NONE-DASHED")
    reconciliation = result["metadata"]["official_identity_reconciliation"]
    assert reconciliation["status"] == "aligned"
    assert reconciliation["transition_identity_alignment_count"] == 1


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
    _require_feedback_final_evidence()
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
        fcstm_path = EVIDENCE / "fcstm" / f"{source_rows[case_id]['pair_id']}.fcstm"
        actual_fcstm_sha256 = hashlib.sha256(fcstm_path.read_bytes()).hexdigest()
        assert row["source"] == source_rows[case_id]["stm0_sha256"]
        assert row["source"] == comparison_rows[case_id]["source_sha256"]
        assert row["fcstm"] == comparison_rows[case_id]["fcstm_sha256"]
        assert row["fcstm"] == actual_fcstm_sha256
        assert comparison_rows[case_id]["verdict"] == "structure_preserved"
        assert comparison_rows[case_id]["fcstm_execution_eligible"] is False
        assert comparison_rows[case_id]["discover_eligible"] is False

    assert "不表示行为等价" in manual_text


def test_committed_pair_pages_show_complete_nl_plantuml_and_fcstm_for_all_60_cases():
    _require_feedback_final_evidence()
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
        case_report = json.loads(
            (EVIDENCE / "case_reports" / f"{pair_id}.json").read_text(
                encoding="utf-8"
            )
        )
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
        assert "## Official identity ledger" in page_text
        assert (
            case_report["official_identity_reconciliation"]["status"] == "aligned"
        )
        assert "official identity states / transitions" in page_text
        assert f"./pairs/{case_id}/README.md" in index_text
        assert f"./pairs/{case_id}/nl.txt" in index_text
        assert f"./pairs/{case_id}/plantuml.puml" in index_text
        assert f"./pairs/{case_id}/fcstm.fcstm" in index_text
        assert f"../../case_reports/{pair_id}.json" in page_text
