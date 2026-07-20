from __future__ import annotations

import copy
import concurrent.futures
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

from paper_stm_repair_conversion.adapters.plantuml_source import (
    parse_plantuml_source,
    resolve_plantuml_jar,
)
from paper_stm_repair_conversion.adapters import plantuml_source as plantuml_adapter
from paper_stm_repair_representation.manual_pair_review import (
    _fcstm_anchor_matches_element,
    fcstm_evidence_anchors,
    plantuml_evidence_anchor,
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
PAIR_BUILDER = (
    REPO_ROOT
    / "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion"
    / "tools/build_llms_emp_pair_pages.py"
)
EVIDENCE = (
    REPO_ROOT
    / "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation"
    / "reports/llms_emp_r45_java_60"
)
PAIR_INDEX = EVIDENCE / "PAIR_INDEX.md"
PAIR_PAGES = EVIDENCE / "pairs"


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


def _load_pair_builder_module():
    spec = importlib.util.spec_from_file_location(
        "build_llms_emp_pair_pages", PAIR_BUILDER
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_manifest_fixture(
    *,
    builder: object,
    evidence_dir: Path,
    implementation_sha256: str,
    java_build: dict,
) -> None:
    contracts = evidence_dir / "working_contracts"
    contracts.mkdir(parents=True)
    for index in range(60):
        (contracts / f"llms_emp_feedback_final_{index:04d}.json").write_text(
            "{}\n", encoding="utf-8"
        )
    inventory = [
        {
            "path": path.relative_to(evidence_dir).as_posix(),
            "sha256": builder._sha256_bytes(path.read_bytes()),
        }
        for path in sorted(contracts.iterdir())
    ]
    supporting_inventory = []
    for name in (
        ".gitattributes",
        "MANUAL_REVIEW_TEMPLATE.jsonl",
        "MANUAL_REVIEW_TEMPLATE.md",
        "SUMMARY.md",
    ):
        path = evidence_dir / name
        path.write_text(f"fixture {name}\n", encoding="utf-8")
        supporting_inventory.append(
            {"path": name, "sha256": builder._sha256_bytes(path.read_bytes())}
        )
    manifest = {
        "schema_version": "r4_5.llms_emp_java_batch.v6",
        "evidence_eligible": True,
        "output_dir": "fixture-evidence",
        "implementation_tree_sha256": implementation_sha256,
        "java_frontend_build": java_build,
        "java_frontend_source_identity": builder.java_frontend_source_identity(
            java_build
        ),
        "pyfcstm_commit": "c" * 40,
        "artifact_inventory": inventory,
        "artifact_set_sha256": builder._sha256_json(inventory),
        "working_contract_set_sha256": builder._sha256_json(inventory),
        "supporting_artifact_inventory": supporting_inventory,
        "supporting_artifact_set_sha256": builder._sha256_json(supporting_inventory),
    }
    (evidence_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _fixture_java_build_identity() -> dict:
    return {
        "schema_version": "paper1.plantuml_java_build.v1",
        "plantuml_version": "1.2024.7",
        "plantuml_jar_sha256": "a" * 64,
        "java_version": "openjdk fixture",
        "javac_version": "javac fixture",
        "makefile_sha256": "b" * 64,
        "source_inventory": [
            {
                "path": "src/main/java/researchideas/plantuml/Fixture.java",
                "sha256": "c" * 64,
            }
        ],
        "input_sha256": "d" * 64,
        "class_inventory": [
            {
                "path": "researchideas/plantuml/Fixture.class",
                "sha256": "e" * 64,
            }
        ],
        "class_tree_sha256": "f" * 64,
    }


REVIEW_NL = "The controller enters Idle mode and can advance to Ready mode."
REVIEW_SOURCE = (
    "@startuml\n"
    "state Idle\n"
    "state Ready\n"
    "BodyState : note\n"
    "--\n"
    "state Fork <<fork>>\n"
    "Running : entry / Tick\n"
    "@enduml\n"
)
REVIEW_FCSTM = (
    'state Idle named "Idle";\n'
    'state Ready named "Ready";\n'
    'state BodyState named "BodyState\\n[PlantUML body] note";\n'
    'state Regions named "Regions\\n[PlantUML concurrent region 0]";\n'
    'pseudo state Fork named "Fork";\n'
    "state Running {\n"
    "    enter abstract Tick;\n"
    "}\n"
)


def _manual_review_fixture(*, second_pass_required: bool = False) -> dict:
    idle_plantuml_anchor = "source-ref:fixture.puml:line:2|state Idle"
    idle_fcstm_anchor = (
        'element-ref:source:state:Idle@line:1|state Idle named "Idle";'
    )
    ready_plantuml_anchor = "source-ref:fixture.puml:line:3|state Ready"
    ready_fcstm_anchor = (
        'element-ref:source:state:Ready@line:2|state Ready named "Ready";'
    )
    return {
        "schema_version": "paper1.manual_pair_review.v4",
        "case_id": "0000",
        "pair_id": "llms_emp_feedback_final_0000",
        "review_subject_sha256": "a" * 64,
        "working_contract_sha256": "b" * 64,
        "reviewer_id": "main_session_llm",
        "review_method": "full_nl_plantuml_fcstm_contract_read",
        "review_context": {
            "reviewed_at": "2026-07-20T12:00:00Z",
            "session_id": "omx-test-session",
            "model_id": "gpt-5.5",
        },
        "reviewed_inputs": {
            "nl": True,
            "plantuml": True,
            "fcstm": True,
            "working_contract": True,
            "source_trace": True,
        },
        "observations": {
            "nl_intent": (
                "The requirement places the controller in Idle mode and names Ready mode "
                "as a distinct subsequent condition."
            ),
            "plantuml_semantics": (
                "The source declares both state Idle and state Ready as distinct authored "
                "semantic occurrences."
            ),
            "fcstm_projection": (
                'The FCSTM retains state Idle named "Idle"; and state Ready named '
                '"Ready"; as distinct source-owned states.'
            ),
            "attribution_rationale": "Idle is source_owned; the generated wrapper remains compiler_owned.",
            "capability_rationale": "source_static capability is eligible while runtime evidence stays scoped.",
            "nl_anchors": ["Idle mode", "Ready mode"],
            "plantuml_anchors": [idle_plantuml_anchor, ready_plantuml_anchor],
            "fcstm_anchors": [idle_fcstm_anchor, ready_fcstm_anchor],
        },
        "semantic_correspondences": [
            {
                "nl_anchor": "Idle mode",
                "plantuml_anchor": idle_plantuml_anchor,
                "fcstm_anchor": idle_fcstm_anchor,
                "source_element_ids": ["source:state:Idle"],
                "compiler_element_ids": [],
                "projection_kind": "direct",
                "assessment": "preserved",
                "rationale": (
                    "source:state:Idle binds the requirement's Idle mode to the PlantUML "
                    "state and the same named FCSTM state."
                ),
            },
            {
                "nl_anchor": "Ready mode",
                "plantuml_anchor": ready_plantuml_anchor,
                "fcstm_anchor": ready_fcstm_anchor,
                "source_element_ids": ["source:state:Ready"],
                "compiler_element_ids": [],
                "projection_kind": "direct",
                "assessment": "preserved",
                "rationale": (
                    "source:state:Ready is the second positively traced semantic root; its "
                    "authored label survives as a distinct FCSTM projection."
                ),
            },
        ],
        "ownership_verdict": "pass",
        "macro_verdict": "pass",
        "capability_verdict": "pass",
        "second_pass": {
            "required": second_pass_required,
            "completed": False,
            "review_subject_sha256": None,
            "reviewer_id": None,
            "review_method": None,
            "risk_tags_reviewed": [],
            "risk_assessments": [],
            "observations": None,
            "notes": "not required" if not second_pass_required else "pending",
        },
        "findings": [],
        "verdict": "pass",
        "notes": "Case-specific source and FCSTM projection were read and cross-checked.",
    }


def _review_contract_fixture(
    *, second_pass_required: bool = False, risk_tags: list[str] | None = None
) -> dict:
    tags = risk_tags or []
    obligations = (
        [
            {
                "obligation_id": "review:synthetic_state:0001:fixture",
                "risk_tag": "synthetic_state",
                "element_ids": ["compiler:root:fixture"],
                "expected_origins": {
                    "compiler:root:fixture": "compiler_owned",
                },
                "source_refs": ["fixture.puml:line:2"],
                "rationale": "Fixture compiler-owned synthetic-state occurrence.",
            }
        ]
        if second_pass_required
        else []
    )
    return {
        "review_subject": {
            "second_pass_required": second_pass_required,
            "risk_tags": tags,
            "review_obligations": obligations,
        },
        "elements": [
            {
                "element_id": "source:state:Idle",
                "origin": "source_owned",
                "kind": "state",
                "source_refs": ["fixture.puml:line:2"],
                "model_refs": ["state:Idle"],
                "macro_ids": [],
                "metadata": {"fcstm_path": "fixture.Idle"},
                "semantic_fields": {
                    "fcstm_identifier": "fixture.Idle",
                    "kind": "state",
                },
            },
            {
                "element_id": "source:state:Ready",
                "origin": "source_owned",
                "kind": "state",
                "source_refs": ["fixture.puml:line:3"],
                "model_refs": ["state:Ready"],
                "macro_ids": [],
                "metadata": {"fcstm_path": "fixture.Ready"},
                "semantic_fields": {
                    "fcstm_identifier": "fixture.Ready",
                    "kind": "state",
                },
            },
            {
                "element_id": "source:body:BodyState:1",
                "origin": "source_owned",
                "kind": "state_body_text",
                "source_refs": ["fixture.puml:line:4"],
                "model_refs": ["macro:body_projection:BodyState:1"],
                "macro_ids": ["macro:body_projection:BodyState:1"],
                "metadata": {"state_id": "BodyState", "text": "note"},
                "semantic_fields": {
                    "display_encoding": "state_display_metadata",
                    "text": "note",
                },
            },
            {
                "element_id": "source:region:Regions:region:0",
                "origin": "source_owned",
                "kind": "concurrent_region",
                "source_refs": ["fixture.puml:line:5"],
                "model_refs": ["macro:region_projection:Regions:region:0"],
                "macro_ids": ["macro:region_projection:Regions:region:0"],
                "metadata": {"owner_scope": "Regions", "region_index": 0},
                "semantic_fields": {
                    "execution": "orthogonal_runtime_unsupported",
                    "owner_scope": "Regions",
                    "region_index": 0,
                },
            },
            {
                "element_id": "source:state:Fork",
                "origin": "source_owned",
                "kind": "state",
                "source_refs": ["fixture.puml:line:6"],
                "model_refs": ["state:Fork"],
                "macro_ids": [],
                "metadata": {"fcstm_path": "fixture.Fork"},
                "semantic_fields": {
                    "fcstm_identifier": "fixture.Fork",
                    "kind": "fork",
                },
            },
            {
                "element_id": "source:lifecycle:Running:1",
                "origin": "source_owned",
                "kind": "lifecycle_action",
                "source_refs": ["fixture.puml:line:7"],
                "model_refs": ["macro:lifecycle_projection:Running:1"],
                "macro_ids": ["macro:lifecycle_projection:Running:1"],
                "metadata": {
                    "state_id": "Running",
                    "lifecycle_kind": "entry",
                    "text": "Tick",
                },
                "semantic_fields": {
                    "execution": "abstract_action_not_execution_evidence",
                    "kind": "entry",
                    "text": "Tick",
                },
            },
            {
                "element_id": "compiler:lifecycle_action:Running:1:Tick",
                "origin": "compiler_owned",
                "kind": "abstract_lifecycle_projection",
                "source_refs": ["fixture.puml:line:7"],
                "model_refs": ["action:Tick"],
                "macro_ids": ["macro:lifecycle_projection:Running:1"],
                "metadata": {"representation": "abstract_lifecycle_action"},
                "semantic_fields": {},
            },
            {
                "element_id": "compiler:root:fixture",
                "origin": "compiler_owned",
                "kind": "root_wrapper",
                "source_refs": ["fixture.puml:line:2"],
                "model_refs": ["state:Idle"],
                "macro_ids": [],
                "metadata": {},
                "semantic_fields": {},
            },
        ],
        "macros": [
            {
                "macro_id": "macro:body_projection:BodyState:1",
                "source_element_ids": ["source:body:BodyState:1"],
                "member_element_ids": [],
            },
            {
                "macro_id": "macro:region_projection:Regions:region:0",
                "source_element_ids": ["source:region:Regions:region:0"],
                "member_element_ids": [],
            },
            {
                "macro_id": "macro:lifecycle_projection:Running:1",
                "source_element_ids": ["source:lifecycle:Running:1"],
                "member_element_ids": [
                    "compiler:lifecycle_action:Running:1:Tick"
                ],
            },
        ],
        "source_trace_base": {
            "entries": [
                {
                    "source_elements": [
                        "source:state:Idle",
                        "source:state:Ready",
                        "source:body:BodyState:1",
                        "source:region:Regions:region:0",
                        "source:state:Fork",
                        "source:lifecycle:Running:1",
                    ],
                }
            ]
        },
    }


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
        item["raw"] == "state Shared {" for item in shared["attributes"]["declarations"]
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
        (item["source"], item["target"]) for item in result["model"]["transitions"]
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
        official_links = result["metadata"]["official_validation"]["model"]["counts"][
            "links"
        ]
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
    assert (
        sum(
            item["rule_id"] == "source_input.workbook_doubled_state_quotes"
            for item in recoveries
        )
        == 5
    )
    assert (
        sum(
            item["rule_id"] == "source_input.workbook_trailing_end_quote"
            for item in recoveries
        )
        == 1
    )
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


def test_java_frontend_rebuilds_changed_source_despite_future_class_mtime(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    java_root = tmp_path / "java-frontend"
    source = java_root / "src/main/java/example/Frontend.java"
    class_file = (
        java_root / "build/classes/researchideas/plantuml/PlantUmlStateFrontend.class"
    )
    jar = java_root / "plantuml.jar"
    source.parent.mkdir(parents=True)
    class_file.parent.mkdir(parents=True)
    source.write_text("class Frontend { int version = 1; }\n", encoding="utf-8")
    class_file.write_bytes(b"old-class")
    jar.write_bytes(b"pinned-jar")
    (java_root / "Makefile").write_text("compile:\n\t@true\n", encoding="utf-8")
    monkeypatch.setattr(plantuml_adapter, "JAVA_ROOT", java_root)
    monkeypatch.setattr(plantuml_adapter, "resolve_plantuml_jar", lambda _: jar)
    monkeypatch.setattr(plantuml_adapter, "_javac_version", lambda: "javac fixture")
    monkeypatch.setattr(plantuml_adapter, "_java_version", lambda: "java fixture")

    old_input = plantuml_adapter._java_compilation_input_identity(jar)
    old_tree = plantuml_adapter._java_class_tree_identity()
    plantuml_adapter._write_build_fingerprint(
        {
            "schema_version": plantuml_adapter.BUILD_FINGERPRINT_SCHEMA,
            **old_input,
            **old_tree,
        }
    )
    source.write_text("class Frontend { int version = 2; }\n", encoding="utf-8")
    future = 4_102_444_800
    os.utime(class_file, (future, future))
    calls = []

    class Completed:
        returncode = 0
        stdout = ""
        stderr = ""

    def fake_run(command: list[str], **_: object) -> Completed:
        calls.append(command)
        class_file.parent.mkdir(parents=True, exist_ok=True)
        class_file.write_bytes(b"new-class")
        return Completed()

    monkeypatch.setattr(plantuml_adapter.subprocess, "run", fake_run)
    plantuml_adapter.compile_java_frontend(plantuml_jar=jar)

    assert calls == [["make", "clean", "compile", f"PLANTUML_JAR={jar}"]]
    fingerprint = plantuml_adapter._read_build_fingerprint()
    assert fingerprint is not None
    assert fingerprint["input_sha256"] != old_input["input_sha256"]
    assert fingerprint["class_tree_sha256"] != old_tree["class_tree_sha256"]


def test_java_frontend_force_rebuild_rejects_jointly_forged_class_and_fingerprint(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    java_root = tmp_path / "java-frontend"
    source = java_root / "src/main/java/example/Frontend.java"
    class_file = (
        java_root / "build/classes/researchideas/plantuml/PlantUmlStateFrontend.class"
    )
    jar = java_root / "plantuml.jar"
    source.parent.mkdir(parents=True)
    class_file.parent.mkdir(parents=True)
    source.write_text("class Frontend {}\n", encoding="utf-8")
    class_file.write_bytes(b"forged-class")
    jar.write_bytes(b"pinned-jar")
    (java_root / "Makefile").write_text("compile:\n\t@true\n", encoding="utf-8")
    monkeypatch.setattr(plantuml_adapter, "JAVA_ROOT", java_root)
    monkeypatch.setattr(plantuml_adapter, "resolve_plantuml_jar", lambda _: jar)
    monkeypatch.setattr(plantuml_adapter, "_javac_version", lambda: "javac fixture")
    monkeypatch.setattr(plantuml_adapter, "_java_version", lambda: "java fixture")
    forged_input = plantuml_adapter._java_compilation_input_identity(jar)
    forged_tree = plantuml_adapter._java_class_tree_identity()
    plantuml_adapter._write_build_fingerprint(
        {
            "schema_version": plantuml_adapter.BUILD_FINGERPRINT_SCHEMA,
            **forged_input,
            **forged_tree,
        }
    )
    calls = []

    class Completed:
        returncode = 0
        stdout = ""
        stderr = ""

    def fake_run(command: list[str], **_: object) -> Completed:
        calls.append(command)
        class_file.parent.mkdir(parents=True, exist_ok=True)
        class_file.write_bytes(b"source-derived-class")
        return Completed()

    monkeypatch.setattr(plantuml_adapter.subprocess, "run", fake_run)

    identity = plantuml_adapter.java_frontend_build_identity(
        plantuml_jar=jar,
        force=True,
    )

    assert calls == [["make", "clean", "compile", f"PLANTUML_JAR={jar}"]]
    assert identity["class_tree_sha256"] != forged_tree["class_tree_sha256"]


def test_formal_runner_and_pair_builder_force_clean_java_build(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    runner = _load_runner_module()
    builder = _load_pair_builder_module()
    calls = []

    def fake_identity(**kwargs: object) -> dict:
        calls.append(kwargs)
        return {"schema_version": "fixture"}

    monkeypatch.setattr(runner, "java_frontend_build_identity", fake_identity)
    monkeypatch.setattr(builder, "java_frontend_build_identity", fake_identity)
    jar = tmp_path / "plantuml.jar"

    assert runner._formal_java_frontend_build(jar) == {"schema_version": "fixture"}
    assert builder._current_java_frontend_build() == {"schema_version": "fixture"}
    assert calls == [
        {"plantuml_jar": jar, "force": True},
        {"force": True},
    ]


def test_java_frontend_source_identity_is_portable_across_jdk_builds():
    producer = _fixture_java_build_identity()
    consumer = copy.deepcopy(producer)
    consumer["java_version"] = "openjdk consumer"
    consumer["javac_version"] = "javac consumer"
    consumer["class_inventory"][0]["sha256"] = "0" * 64
    consumer["class_tree_sha256"] = "1" * 64

    assert plantuml_adapter.java_frontend_source_identity(
        producer
    ) == plantuml_adapter.java_frontend_source_identity(consumer)

    consumer["source_inventory"][0]["sha256"] = "2" * 64
    assert plantuml_adapter.java_frontend_source_identity(
        producer
    ) != plantuml_adapter.java_frontend_source_identity(consumer)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda build: build.update(schema_version="fixture.unsupported"),
        lambda build: build["source_inventory"].append(
            copy.deepcopy(build["source_inventory"][0])
        ),
        lambda build: build["source_inventory"][0].update(path="../Fixture.java"),
        lambda build: build["source_inventory"][0].update(sha256="not-a-sha256"),
    ],
)
def test_java_frontend_source_identity_rejects_malformed_producer_build(mutation):
    producer = _fixture_java_build_identity()
    mutation(producer)

    with pytest.raises(RuntimeError):
        plantuml_adapter.java_frontend_source_identity(producer)


def test_java_frontend_build_and_execution_are_process_safe():
    subprocess.run(
        ["make", "clean"],
        cwd=plantuml_adapter.JAVA_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    source = "@startuml\n[*] --> Ready\nstate Ready\n@enduml\n"
    command = [
        sys.executable,
        "-c",
        (
            "import json; "
            "from paper_stm_repair_conversion.adapters.plantuml_source "
            "import parse_plantuml_source; "
            f"result=parse_plantuml_source({source!r}, example_id='parallel'); "
            "print(json.dumps({'status': result['status']}))"
        ),
    ]

    def invoke(_: int) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        conversion_src = (
            REPO_ROOT
            / "project_1_llm_state_machine_modeling/paper_stm_repair"
            / "pipeline/conversion/src"
        )
        env["PYTHONPATH"] = os.pathsep.join(
            [str(conversion_src), env.get("PYTHONPATH", "")]
        )
        return subprocess.run(
            command,
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            env=env,
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        completed = list(executor.map(invoke, range(8)))

    assert all(item.returncode == 0 for item in completed), [
        item.stderr for item in completed if item.returncode != 0
    ]
    assert all(json.loads(item.stdout)["status"] == "converted" for item in completed)


def test_development_summary_has_non_eligible_banner():
    runner = _load_runner_module()
    manifest = {
        "evidence_eligible": False,
        "summary": {
            "source_parse_ok": 60,
            "official_raw_state_diagram": 59,
            "official_raw_not_state_diagram": 1,
            "official_validation_state_diagram": 60,
            "official_validation_links": 1,
            "source_transitions": 1,
            "official_validation_link_delta": 0,
            "mapped_transitions": 1,
            "blocked_transitions": 0,
            "silently_dropped_transitions": 0,
            "final_transitions_mapped": 0,
            "final_transitions_source": 0,
            "body_lines_mapped": 0,
            "body_lines_source": 0,
            "lifecycle_actions_mapped": 0,
            "lifecycle_actions_source": 0,
            "concurrent_regions_mapped": 0,
            "concurrent_regions_source": 0,
            "concurrent_region_separators_mapped": 0,
            "concurrent_region_separators_source": 0,
            "source_normalizations_mapped": 0,
            "source_normalizations_source": 0,
            "fcstm_parse_ok": 60,
            "fcstm_inspect_ok": 60,
            "ast_audit_ok": 60,
            "official_identity_states_aligned": 1,
            "source_states": 1,
            "official_identity_transitions_aligned": 1,
            "official_identity_state_remaps": 0,
            "official_identity_transition_remaps": 0,
            "structure_preserved": 60,
            "structure_blocked": 0,
            "fcstm_execution_eligible": 0,
            "discover_eligible": 0,
            "working_contracts_validated": 60,
            "compiler_owned_elements": 1,
            "agent_created_elements": 0,
            "attribution_scoped_discover_input": 60,
            "working_macros": 1,
            "positive_source_traces": 1,
        },
    }

    summary = runner._summary_markdown(manifest, [])

    assert "DEVELOPMENT ONLY" in summary.split("## 结论", 1)[0]
    manifest["evidence_eligible"] = True
    assert "DEVELOPMENT ONLY" not in runner._summary_markdown(manifest, [])


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


def test_batch_runner_rejects_dirty_formal_evidence_before_reading_inputs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    runner = _load_runner_module()
    monkeypatch.setattr(runner, "_checked_out_pyfcstm_commit", lambda: "a" * 40)

    def fake_git(*args: str, **_: object) -> str:
        if args == ("rev-parse", "HEAD"):
            return "b" * 40
        if args == ("branch", "--show-current"):
            return "paper1/pr-plantuml-fcstm-fix"
        if args == ("status", "--porcelain", "--untracked-files=no"):
            return " M converter.py"
        if args[:3] == ("status", "--porcelain", "--untracked-files=all"):
            return ""
        raise AssertionError(args)

    monkeypatch.setattr(runner, "_git", fake_git)
    with pytest.raises(RuntimeError, match="requires a clean tracked worktree"):
        runner.run(
            pairs_path=tmp_path / "missing.jsonl",
            output_dir=runner.PAPER_ROOT
            / "pipeline/representation/reports/dirty-run-test",
            plantuml_jar=tmp_path / "unused.jar",
        )


def test_batch_runner_rejects_untracked_implementation_before_reading_inputs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    runner = _load_runner_module()
    monkeypatch.setattr(runner, "_checked_out_pyfcstm_commit", lambda: "a" * 40)

    def fake_git(*args: str, **_: object) -> str:
        if args == ("rev-parse", "HEAD"):
            return "b" * 40
        if args == ("branch", "--show-current"):
            return "paper1/pr-plantuml-fcstm-fix"
        if args == ("status", "--porcelain", "--untracked-files=no"):
            return ""
        if args[:3] == ("status", "--porcelain", "--untracked-files=all"):
            return "?? untracked-frontend.java"
        raise AssertionError(args)

    monkeypatch.setattr(runner, "_git", fake_git)
    with pytest.raises(RuntimeError, match="untracked implementation files"):
        runner.run(
            pairs_path=tmp_path / "missing.jsonl",
            output_dir=runner.PAPER_ROOT
            / "pipeline/representation/reports/untracked-run-test",
            plantuml_jar=tmp_path / "unused.jar",
        )


def test_batch_runner_validates_pair_order_uniqueness_and_hashes():
    runner = _load_runner_module()
    rows = [
        {
            "pair_id": f"llms_emp_feedback_final_{index:04d}",
            "nl_text": f"nl-{index}",
            "nl_sha256": runner._sha256_text(f"nl-{index}"),
            "stm0_text": f"@startuml\nstate S{index}\n@enduml\n",
            "stm0_sha256": runner._sha256_text(f"@startuml\nstate S{index}\n@enduml\n"),
            "selected_stage": "phase_ii_semantic",
            "selected_stage_cell": f"AE{index + 2}",
        }
        for index in range(60)
    ]
    runner._validate_input_rows(rows)

    reordered = list(rows)
    reordered[0], reordered[1] = reordered[1], reordered[0]
    with pytest.raises(RuntimeError, match="order/identity drift"):
        runner._validate_input_rows(reordered)

    tampered = [dict(item) for item in rows]
    tampered[0]["stm0_text"] += "' changed\n"
    with pytest.raises(RuntimeError, match="PlantUML hash drift"):
        runner._validate_input_rows(tampered)


def test_runner_and_pair_builder_share_the_same_implementation_tree_hash():
    runner = _load_runner_module()
    builder = _load_pair_builder_module()

    assert runner._relevant_implementation_sha256() == (
        builder._current_implementation_sha256()
    )


@pytest.mark.parametrize(
    "changed_key",
    [
        "research_commit",
        "research_branch",
        "tracked_status",
        "untracked_implementation",
        "implementation_tree_sha256",
        "java_frontend_build",
        "pyfcstm_commit",
        "pairs_sha256",
    ],
)
def test_batch_runner_rejects_any_mid_run_identity_drift(
    tmp_path: Path, changed_key: str
):
    runner = _load_runner_module()
    staging = tmp_path / f"staging-{changed_key}"
    staging.mkdir()
    (staging / "partial.txt").write_text("partial", encoding="utf-8")
    start = {
        "research_commit": "a" * 40,
        "research_branch": "paper1/pr-plantuml-fcstm-fix",
        "tracked_status": "",
        "untracked_implementation": "",
        "implementation_tree_sha256": "b" * 64,
        "java_frontend_build": {"source_tree_sha256": "c" * 64},
        "pyfcstm_commit": "d" * 40,
        "pairs_sha256": "e" * 64,
    }
    end = copy.deepcopy(start)
    end[changed_key] = "changed"

    with pytest.raises(RuntimeError, match=changed_key):
        runner._require_stable_replay_identity(
            start_identity=start,
            end_identity=end,
            staging_dir=staging,
        )

    assert not staging.exists()


def test_batch_runner_atomic_publish_replaces_only_after_staging_is_complete(
    tmp_path: Path,
):
    runner = _load_runner_module()
    output = tmp_path / "evidence"
    staging = tmp_path / ".evidence.tmp"
    output.mkdir()
    staging.mkdir()
    (output / "old.txt").write_text("old", encoding="utf-8")
    (staging / "manifest.json").write_text("new", encoding="utf-8")

    runner._atomic_publish(staging, output)

    assert not staging.exists()
    assert not (output / "old.txt").exists()
    assert (output / "manifest.json").read_text(encoding="utf-8") == "new"


def test_pair_builder_rejects_stale_manual_review_hash():
    builder = _load_pair_builder_module()
    schema = json.loads(builder.MANUAL_REVIEW_SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    review = _manual_review_fixture()
    comparison = {"review_subject_sha256": "c" * 64}
    contract = _review_contract_fixture()

    with pytest.raises(RuntimeError, match="stale manual review subject"):
        builder._validate_review(
            review=review,
            case_id="0000",
            pair_id="llms_emp_feedback_final_0000",
            comparison=comparison,
            contract=contract,
            contract_sha256="b" * 64,
            nl_text=REVIEW_NL,
            source_text=REVIEW_SOURCE,
            fcstm_text=REVIEW_FCSTM,
            validator=validator,
        )


def test_pair_builder_accepts_source_bound_semantic_correspondences():
    builder = _load_pair_builder_module()
    validator = Draft202012Validator(
        json.loads(builder.MANUAL_REVIEW_SCHEMA.read_text(encoding="utf-8"))
    )

    builder._validate_review(
        review=_manual_review_fixture(),
        case_id="0000",
        pair_id="llms_emp_feedback_final_0000",
        comparison={"review_subject_sha256": "a" * 64},
        contract=_review_contract_fixture(),
        contract_sha256="b" * 64,
        nl_text=REVIEW_NL,
        source_text=REVIEW_SOURCE,
        fcstm_text=REVIEW_FCSTM,
        validator=validator,
    )


def test_pair_builder_rejects_incomplete_second_pass_and_blocking_finding():
    builder = _load_pair_builder_module()
    validator = Draft202012Validator(
        json.loads(builder.MANUAL_REVIEW_SCHEMA.read_text(encoding="utf-8"))
    )
    review = _manual_review_fixture(second_pass_required=True)
    comparison = {"review_subject_sha256": "a" * 64}
    contract = _review_contract_fixture(
        second_pass_required=True,
        risk_tags=["synthetic_state"],
    )
    kwargs = {
        "review": review,
        "case_id": "0000",
        "pair_id": "llms_emp_feedback_final_0000",
        "comparison": comparison,
        "contract": contract,
        "contract_sha256": "b" * 64,
        "nl_text": REVIEW_NL,
        "source_text": REVIEW_SOURCE,
        "fcstm_text": REVIEW_FCSTM,
        "validator": validator,
    }
    with pytest.raises(RuntimeError, match="second pass is incomplete"):
        builder._validate_review(**kwargs)

    review["second_pass"] = {
        "required": True,
        "completed": True,
        "review_subject_sha256": "c" * 64,
        "reviewer_id": "main_session_llm",
        "review_method": "risk_focused_independent_second_pass",
        "risk_tags_reviewed": ["synthetic_state"],
        "risk_assessments": [
            {
                "obligation_id": "review:synthetic_state:0001:fixture",
                "risk_tag": "synthetic_state",
                "plantuml_anchors": [
                    "source-ref:fixture.puml:line:2|state Idle"
                ],
                "fcstm_anchors": [
                    'element-ref:compiler:root:fixture@line:1|state Idle named "Idle";'
                ],
                "element_ids": ["compiler:root:fixture"],
                "assessment": "compiler_artifact_excluded",
                "rationale": (
                    "review:synthetic_state:0001:fixture synthetic_state was checked "
                    "against compiler:root:fixture and is not treated as the "
                    "source:state:Idle repair target."
                ),
            }
        ],
        "observations": "Second pass independently rechecked the synthetic_state ownership risk.",
        "notes": "No compiler-owned member was mistaken for a source-owned repair target.",
    }
    with pytest.raises(RuntimeError, match="second pass is not evidence-bound"):
        builder._validate_review(**kwargs)

    review["second_pass"]["review_subject_sha256"] = "a" * 64
    builder._validate_review(**kwargs)
    review["second_pass"]["risk_assessments"][0]["assessment"] = (
        "source_fact_preserved"
    )
    with pytest.raises(RuntimeError, match="incompatible with risk occurrence"):
        builder._validate_review(**kwargs)
    review["second_pass"]["risk_assessments"][0]["assessment"] = (
        "compiler_artifact_excluded"
    )
    review["findings"] = [{"severity": "I", "code": "I.STALE", "summary": "blocking"}]
    with pytest.raises(RuntimeError, match="blocking findings"):
        builder._validate_review(**kwargs)


def test_pending_manual_review_template_is_schema_valid():
    runner = _load_runner_module()
    schema_path = (
        REPO_ROOT
        / "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/schemas/manual_pair_review.schema.json"
    )
    validator = Draft202012Validator(
        json.loads(schema_path.read_text(encoding="utf-8"))
    )
    row = {
        "case_id": "0000",
        "pair_id": "llms_emp_feedback_final_0000",
        "review_subject_sha256": "a" * 64,
        "working_contract_sha256": "b" * 64,
        "second_pass_required": True,
    }
    records = [
        json.loads(line)
        for line in runner._manual_review_jsonl_template([row]).splitlines()
        if line.strip()
    ]

    assert len(records) == 1
    validator.validate(records[0])
    assert records[0]["semantic_correspondences"] == []
    assert records[0]["second_pass"]["risk_assessments"] == []


def test_pair_builder_rejects_generic_structured_self_attestation():
    builder = _load_pair_builder_module()
    validator = Draft202012Validator(
        json.loads(builder.MANUAL_REVIEW_SCHEMA.read_text(encoding="utf-8"))
    )
    review = _manual_review_fixture()
    exact = _manual_review_fixture()["observations"]
    review["observations"] = {
        "nl_intent": "This generic sentence claims that the requirement was reviewed.",
        "plantuml_semantics": "This generic sentence claims that the source was reviewed.",
        "fcstm_projection": "This generic sentence claims that the projection was reviewed.",
        "attribution_rationale": "This generic conversion sentence claims attribution was reviewed.",
        "capability_rationale": "This generic capability sentence claims eligibility was reviewed.",
        "nl_anchors": ["1"],
        "plantuml_anchors": exact["plantuml_anchors"],
        "fcstm_anchors": exact["fcstm_anchors"],
    }

    with pytest.raises(RuntimeError, match="nl_anchors are not bound"):
        builder._validate_review(
            review=review,
            case_id="0000",
            pair_id="llms_emp_feedback_final_0000",
            comparison={"review_subject_sha256": "a" * 64},
            contract=_review_contract_fixture(),
            contract_sha256="b" * 64,
            nl_text="Requirement 1",
            source_text="@startuml\nstate Idle\n@enduml\n",
            fcstm_text='state Idle named "Idle";\n',
            validator=validator,
        )


def test_pair_builder_rejects_real_anchors_with_shallow_declared_review():
    builder = _load_pair_builder_module()
    validator = Draft202012Validator(
        json.loads(builder.MANUAL_REVIEW_SCHEMA.read_text(encoding="utf-8"))
    )
    review = _manual_review_fixture()
    for item in review["semantic_correspondences"]:
        item["rationale"] = (
            f"{item['source_element_ids'][0]} and the remaining semantics were declared "
            "reviewed against the supplied anchors without a case-specific assessment."
        )

    with pytest.raises(RuntimeError, match="shallow attestation"):
        builder._validate_review(
            review=review,
            case_id="0000",
            pair_id="llms_emp_feedback_final_0000",
            comparison={"review_subject_sha256": "a" * 64},
            contract=_review_contract_fixture(),
            contract_sha256="b" * 64,
            nl_text=REVIEW_NL,
            source_text=REVIEW_SOURCE,
            fcstm_text=REVIEW_FCSTM,
            validator=validator,
        )


def test_pair_builder_rejects_duplicate_semantic_correspondence():
    builder = _load_pair_builder_module()
    validator = Draft202012Validator(
        json.loads(builder.MANUAL_REVIEW_SCHEMA.read_text(encoding="utf-8"))
    )
    review = _manual_review_fixture()
    review["semantic_correspondences"][1] = copy.deepcopy(
        review["semantic_correspondences"][0]
    )

    with pytest.raises(ValidationError):
        validator.validate(review)


def test_pair_builder_rejects_duplicate_source_occurrence_with_different_nl_anchor():
    builder = _load_pair_builder_module()
    validator = Draft202012Validator(
        json.loads(builder.MANUAL_REVIEW_SCHEMA.read_text(encoding="utf-8"))
    )
    review = _manual_review_fixture()
    first = review["semantic_correspondences"][0]
    second = review["semantic_correspondences"][1]
    second.update(
        {
            "plantuml_anchor": first["plantuml_anchor"],
            "fcstm_anchor": first["fcstm_anchor"],
            "source_element_ids": first["source_element_ids"],
            "compiler_element_ids": first["compiler_element_ids"],
            "rationale": (
                "source:state:Idle is deliberately repeated under another valid NL phrase "
                "to prove that one source occurrence cannot satisfy the two-item minimum."
            ),
        }
    )
    observations = review["observations"]
    observations["plantuml_anchors"] = [first["plantuml_anchor"]]
    observations["fcstm_anchors"] = [first["fcstm_anchor"]]

    with pytest.raises(RuntimeError, match="repeats a source semantic occurrence"):
        builder._validate_review(
            review=review,
            case_id="0000",
            pair_id="llms_emp_feedback_final_0000",
            comparison={"review_subject_sha256": "a" * 64},
            contract=_review_contract_fixture(),
            contract_sha256="b" * 64,
            nl_text=REVIEW_NL,
            source_text=REVIEW_SOURCE,
            fcstm_text=REVIEW_FCSTM,
            validator=validator,
        )


def test_pair_builder_rejects_blocked_correspondence_in_pass_review():
    builder = _load_pair_builder_module()
    validator = Draft202012Validator(
        json.loads(builder.MANUAL_REVIEW_SCHEMA.read_text(encoding="utf-8"))
    )
    review = _manual_review_fixture()
    review["semantic_correspondences"][0]["assessment"] = "blocked"

    with pytest.raises(RuntimeError, match="cannot support PASS"):
        builder._validate_review(
            review=review,
            case_id="0000",
            pair_id="llms_emp_feedback_final_0000",
            comparison={"review_subject_sha256": "a" * 64},
            contract=_review_contract_fixture(),
            contract_sha256="b" * 64,
            nl_text=REVIEW_NL,
            source_text=REVIEW_SOURCE,
            fcstm_text=REVIEW_FCSTM,
            validator=validator,
        )


def test_pair_builder_rejects_incompatible_projection_assessment():
    builder = _load_pair_builder_module()
    validator = Draft202012Validator(
        json.loads(builder.MANUAL_REVIEW_SCHEMA.read_text(encoding="utf-8"))
    )
    review = _manual_review_fixture()
    review["semantic_correspondences"][0]["projection_kind"] = "capability_excluded"

    with pytest.raises(
        RuntimeError,
        match="projection/assessment contradicts source kind or capability",
    ):
        builder._validate_review(
            review=review,
            case_id="0000",
            pair_id="llms_emp_feedback_final_0000",
            comparison={"review_subject_sha256": "a" * 64},
            contract=_review_contract_fixture(),
            contract_sha256="b" * 64,
            nl_text=REVIEW_NL,
            source_text=REVIEW_SOURCE,
            fcstm_text=REVIEW_FCSTM,
            validator=validator,
        )


def _replace_first_correspondence_for_projection(
    *,
    source_id: str,
    plantuml_anchor: str,
    fcstm_anchor: str,
    projection_kind: str,
    assessment: str,
    compiler_element_ids: list[str] | None = None,
) -> dict:
    review = _manual_review_fixture()
    correspondence = review["semantic_correspondences"][0]
    old_plantuml_anchor = correspondence["plantuml_anchor"]
    old_fcstm_anchor = correspondence["fcstm_anchor"]
    correspondence.update(
        {
            "plantuml_anchor": plantuml_anchor,
            "fcstm_anchor": fcstm_anchor,
            "source_element_ids": [source_id],
            "compiler_element_ids": compiler_element_ids or [],
            "projection_kind": projection_kind,
            "assessment": assessment,
            "rationale": (
                f"{source_id} is reviewed using the exact source occurrence and its "
                "declared FCSTM projection under the fixture capability contract."
            ),
        }
    )
    observations = review["observations"]
    observations["plantuml_anchors"] = [
        plantuml_anchor if anchor == old_plantuml_anchor else anchor
        for anchor in observations["plantuml_anchors"]
    ]
    observations["fcstm_anchors"] = [
        fcstm_anchor if anchor == old_fcstm_anchor else anchor
        for anchor in observations["fcstm_anchors"]
    ]
    observations["plantuml_semantics"] += (
        f" Exact reviewed occurrence: {plantuml_anchor.split('|', 1)[1]}"
    )
    observations["fcstm_projection"] += (
        f" Exact reviewed projection: {fcstm_anchor.split('|', 1)[1]}"
    )
    return review


@pytest.mark.parametrize(
    (
        "source_id",
        "plantuml_anchor",
        "fcstm_anchor",
        "projection_kind",
        "assessment",
        "compiler_element_ids",
    ),
    [
        (
            "source:body:BodyState:1",
            "source-ref:fixture.puml:line:4|BodyState : note",
            'element-ref:source:body:BodyState:1@line:3|state BodyState named "BodyState\\n[PlantUML body] note";',
            "metadata",
            "preserved_with_exclusions",
            [],
        ),
        (
            "source:region:Regions:region:0",
            "source-ref:fixture.puml:line:5|--",
            'element-ref:source:region:Regions:region:0@line:4|state Regions named "Regions\\n[PlantUML concurrent region 0]";',
            "capability_excluded",
            "preserved_with_exclusions",
            [],
        ),
        (
            "source:state:Fork",
            "source-ref:fixture.puml:line:6|state Fork <<fork>>",
            'element-ref:source:state:Fork@line:5|pseudo state Fork named "Fork";',
            "capability_excluded",
            "preserved_with_exclusions",
            [],
        ),
        (
            "source:lifecycle:Running:1",
            "source-ref:fixture.puml:line:7|Running : entry / Tick",
            "element-ref:compiler:lifecycle_action:Running:1:Tick@line:7|enter abstract Tick;",
            "capability_excluded",
            "preserved_with_exclusions",
            ["compiler:lifecycle_action:Running:1:Tick"],
        ),
    ],
)
def test_pair_builder_accepts_projection_matrix_combinations(
    source_id: str,
    plantuml_anchor: str,
    fcstm_anchor: str,
    projection_kind: str,
    assessment: str,
    compiler_element_ids: list[str],
):
    builder = _load_pair_builder_module()
    validator = Draft202012Validator(
        json.loads(builder.MANUAL_REVIEW_SCHEMA.read_text(encoding="utf-8"))
    )
    review = _replace_first_correspondence_for_projection(
        source_id=source_id,
        plantuml_anchor=plantuml_anchor,
        fcstm_anchor=fcstm_anchor,
        projection_kind=projection_kind,
        assessment=assessment,
        compiler_element_ids=compiler_element_ids,
    )

    builder._validate_review(
        review=review,
        case_id="0000",
        pair_id="llms_emp_feedback_final_0000",
        comparison={"review_subject_sha256": "a" * 64},
        contract=_review_contract_fixture(),
        contract_sha256="b" * 64,
        nl_text=REVIEW_NL,
        source_text=REVIEW_SOURCE,
        fcstm_text=REVIEW_FCSTM,
        validator=validator,
    )


@pytest.mark.parametrize(
    (
        "source_id",
        "plantuml_anchor",
        "fcstm_anchor",
        "projection_kind",
        "assessment",
        "compiler_element_ids",
    ),
    [
        (
            "source:body:BodyState:1",
            "source-ref:fixture.puml:line:4|BodyState : note",
            'element-ref:source:body:BodyState:1@line:3|state BodyState named "BodyState\\n[PlantUML body] note";',
            "direct",
            "preserved",
            [],
        ),
        (
            "source:region:Regions:region:0",
            "source-ref:fixture.puml:line:5|--",
            'element-ref:source:region:Regions:region:0@line:4|state Regions named "Regions\\n[PlantUML concurrent region 0]";',
            "direct",
            "preserved",
            [],
        ),
        (
            "source:state:Fork",
            "source-ref:fixture.puml:line:6|state Fork <<fork>>",
            'element-ref:source:state:Fork@line:5|pseudo state Fork named "Fork";',
            "direct",
            "preserved",
            [],
        ),
        (
            "source:lifecycle:Running:1",
            "source-ref:fixture.puml:line:7|Running : entry / Tick",
            "element-ref:compiler:lifecycle_action:Running:1:Tick@line:7|enter abstract Tick;",
            "macro",
            "preserved_with_exclusions",
            ["compiler:lifecycle_action:Running:1:Tick"],
        ),
    ],
)
def test_pair_builder_rejects_projection_matrix_overclaims(
    source_id: str,
    plantuml_anchor: str,
    fcstm_anchor: str,
    projection_kind: str,
    assessment: str,
    compiler_element_ids: list[str],
):
    builder = _load_pair_builder_module()
    validator = Draft202012Validator(
        json.loads(builder.MANUAL_REVIEW_SCHEMA.read_text(encoding="utf-8"))
    )
    review = _replace_first_correspondence_for_projection(
        source_id=source_id,
        plantuml_anchor=plantuml_anchor,
        fcstm_anchor=fcstm_anchor,
        projection_kind=projection_kind,
        assessment=assessment,
        compiler_element_ids=compiler_element_ids,
    )

    with pytest.raises(
        RuntimeError,
        match="projection/assessment contradicts source kind or capability",
    ):
        builder._validate_review(
            review=review,
            case_id="0000",
            pair_id="llms_emp_feedback_final_0000",
            comparison={"review_subject_sha256": "a" * 64},
            contract=_review_contract_fixture(),
            contract_sha256="b" * 64,
            nl_text=REVIEW_NL,
            source_text=REVIEW_SOURCE,
            fcstm_text=REVIEW_FCSTM,
            validator=validator,
        )


def test_pair_builder_rejects_unknown_source_projection_kind():
    builder = _load_pair_builder_module()
    validator = Draft202012Validator(
        json.loads(builder.MANUAL_REVIEW_SCHEMA.read_text(encoding="utf-8"))
    )
    contract = _review_contract_fixture()
    contract["elements"][0]["kind"] = "unsupported_fixture_kind"
    review = _manual_review_fixture()

    with pytest.raises(RuntimeError, match="unsupported source kind"):
        builder._validate_review(
            review=review,
            case_id="0000",
            pair_id="llms_emp_feedback_final_0000",
            comparison={"review_subject_sha256": "a" * 64},
            contract=contract,
            contract_sha256="b" * 64,
            nl_text=REVIEW_NL,
            source_text=REVIEW_SOURCE,
            fcstm_text=REVIEW_FCSTM,
            validator=validator,
        )


def test_pair_builder_rejects_risk_occurrence_bound_to_wrong_elements():
    builder = _load_pair_builder_module()
    validator = Draft202012Validator(
        json.loads(builder.MANUAL_REVIEW_SCHEMA.read_text(encoding="utf-8"))
    )
    review = _manual_review_fixture(second_pass_required=True)
    review["second_pass"] = {
        "required": True,
        "completed": True,
        "review_subject_sha256": "a" * 64,
        "reviewer_id": "main_session_llm",
        "review_method": "risk_focused_independent_second_pass",
        "risk_tags_reviewed": ["synthetic_state"],
        "risk_assessments": [
            {
                "obligation_id": "review:synthetic_state:0001:fixture",
                "risk_tag": "synthetic_state",
                "plantuml_anchors": [
                    "source-ref:fixture.puml:line:2|state Idle"
                ],
                "fcstm_anchors": [
                    'element-ref:compiler:root:fixture@line:1|state Idle named "Idle";'
                ],
                "element_ids": ["source:state:Idle"],
                "assessment": "compiler_artifact_excluded",
                "rationale": (
                    "review:synthetic_state:0001:fixture synthetic_state was checked "
                    "against source:state:Idle rather than its required occurrence."
                ),
            }
        ],
        "observations": (
            "Second pass independently rechecked the synthetic_state ownership risk."
        ),
        "notes": "The occurrence was deliberately misbound for this rejection test.",
    }

    with pytest.raises(RuntimeError, match="ownership occurrence drift"):
        builder._validate_review(
            review=review,
            case_id="0000",
            pair_id="llms_emp_feedback_final_0000",
            comparison={"review_subject_sha256": "a" * 64},
            contract=_review_contract_fixture(
                second_pass_required=True,
                risk_tags=["synthetic_state"],
            ),
            contract_sha256="b" * 64,
            nl_text=REVIEW_NL,
            source_text=REVIEW_SOURCE,
            fcstm_text=REVIEW_FCSTM,
            validator=validator,
        )


def test_pair_builder_rejects_risk_occurrence_with_unrelated_global_anchors():
    builder = _load_pair_builder_module()
    validator = Draft202012Validator(
        json.loads(builder.MANUAL_REVIEW_SCHEMA.read_text(encoding="utf-8"))
    )
    review = _manual_review_fixture(second_pass_required=True)
    review["second_pass"] = {
        "required": True,
        "completed": True,
        "review_subject_sha256": "a" * 64,
        "reviewer_id": "main_session_llm",
        "review_method": "risk_focused_independent_second_pass",
        "risk_tags_reviewed": ["synthetic_state"],
        "risk_assessments": [
            {
                "obligation_id": "review:synthetic_state:0001:fixture",
                "risk_tag": "synthetic_state",
                "plantuml_anchors": [
                    "source-ref:fixture.puml:line:2|state Idle"
                ],
                "fcstm_anchors": [
                    'element-ref:compiler:root:fixture@line:1|state Idle named "Idle";'
                ],
                "element_ids": ["compiler:root:fixture"],
                "assessment": "compiler_artifact_excluded",
                "rationale": (
                    "review:synthetic_state:0001:fixture synthetic_state deliberately "
                    "uses anchors from another source line for occurrence binding rejection."
                ),
            }
        ],
        "observations": (
            "Second pass independently rechecked the synthetic_state ownership risk."
        ),
        "notes": "This fixture deliberately uses unrelated occurrence evidence.",
    }
    contract = _review_contract_fixture(
        second_pass_required=True,
        risk_tags=["synthetic_state"],
    )
    contract["review_subject"]["review_obligations"][0]["source_refs"] = [
        "fixture.puml:line:3"
    ]

    with pytest.raises(RuntimeError, match="occurrence-misaligned"):
        builder._validate_review(
            review=review,
            case_id="0000",
            pair_id="llms_emp_feedback_final_0000",
            comparison={"review_subject_sha256": "a" * 64},
            contract=contract,
            contract_sha256="b" * 64,
            nl_text=REVIEW_NL,
            source_text=REVIEW_SOURCE,
            fcstm_text=REVIEW_FCSTM,
            validator=validator,
        )


def test_pair_builder_rejects_fcstm_anchor_for_source_normalization():
    builder = _load_pair_builder_module()
    validator = Draft202012Validator(
        json.loads(builder.MANUAL_REVIEW_SCHEMA.read_text(encoding="utf-8"))
    )
    review = _manual_review_fixture(second_pass_required=True)
    review["second_pass"] = {
        "required": True,
        "completed": True,
        "review_subject_sha256": "a" * 64,
        "reviewer_id": "main_session_llm",
        "review_method": "risk_focused_independent_second_pass",
        "risk_tags_reviewed": ["source_normalization"],
        "risk_assessments": [
            {
                "obligation_id": "review:source_normalization:0001:fixture",
                "risk_tag": "source_normalization",
                "plantuml_anchors": [
                    "source-ref:fixture.puml:line:2|state Idle"
                ],
                "fcstm_anchors": [
                    'element-ref:source:state:Idle@line:1|state Idle named "Idle";'
                ],
                "element_ids": ["source:normalization:1"],
                "assessment": "compiler_artifact_excluded",
                "rationale": (
                    "review:source_normalization:0001:fixture source_normalization "
                    "deliberately supplies an FCSTM projection that must be rejected."
                ),
            }
        ],
        "observations": (
            "Second pass independently rechecked the source_normalization boundary."
        ),
        "notes": "Transport normalization has no legitimate FCSTM occurrence anchor.",
    }
    contract = _review_contract_fixture()
    contract["elements"].append(
        {
            "element_id": "source:normalization:1",
            "origin": "source_owned",
            "source_refs": ["fixture.puml:line:2"],
            "model_refs": ["macro:normalization:1"],
            "macro_ids": ["macro:normalization:1"],
            "metadata": {},
            "semantic_fields": {},
        }
    )
    contract["review_subject"] = {
        "second_pass_required": True,
        "risk_tags": ["source_normalization"],
        "review_obligations": [
            {
                "obligation_id": "review:source_normalization:0001:fixture",
                "risk_tag": "source_normalization",
                "element_ids": ["source:normalization:1"],
                "expected_origins": {
                    "source:normalization:1": "source_owned",
                },
                "source_refs": ["fixture.puml:line:2"],
                "rationale": "Fixture transport-only source normalization occurrence.",
            }
        ],
    }

    with pytest.raises(RuntimeError, match="must be empty for source normalization"):
        builder._validate_review(
            review=review,
            case_id="0000",
            pair_id="llms_emp_feedback_final_0000",
            comparison={"review_subject_sha256": "a" * 64},
            contract=contract,
            contract_sha256="b" * 64,
            nl_text=REVIEW_NL,
            source_text=REVIEW_SOURCE,
            fcstm_text=REVIEW_FCSTM,
            validator=validator,
        )


def test_pair_builder_requires_exact_normalization_rule_before_after_binding():
    builder = _load_pair_builder_module()
    validator = Draft202012Validator(
        json.loads(builder.MANUAL_REVIEW_SCHEMA.read_text(encoding="utf-8"))
    )
    obligation_id = "review:source_normalization:0001:fixture"
    review = _manual_review_fixture(second_pass_required=True)
    review["second_pass"] = {
        "required": True,
        "completed": True,
        "review_subject_sha256": "a" * 64,
        "reviewer_id": "main_session_llm",
        "review_method": "risk_focused_independent_second_pass",
        "risk_tags_reviewed": ["source_normalization"],
        "risk_assessments": [
            {
                "obligation_id": obligation_id,
                "risk_tag": "source_normalization",
                "plantuml_anchors": [
                    "source-ref:fixture.puml:line:2|state Idle"
                ],
                "fcstm_anchors": [],
                "element_ids": ["source:normalization:1"],
                "assessment": "compiler_artifact_excluded",
                "rationale": (
                    f"{obligation_id} source_normalization was reviewed only generically "
                    "without spelling out its exact transformation."
                ),
            }
        ],
        "observations": (
            "Second pass independently rechecked the source_normalization boundary."
        ),
        "notes": "The fixture deliberately omits exact normalization transformation facts.",
    }
    contract = _review_contract_fixture()
    contract["elements"].append(
        {
            "element_id": "source:normalization:1",
            "origin": "source_owned",
            "kind": "source_normalization",
            "source_refs": ["fixture.puml:line:2"],
            "model_refs": ["macro:normalization:1"],
            "macro_ids": ["macro:normalization:1"],
            "metadata": {
                "rule_id": "source_input.fixture_rule",
                "before": "state Idle",
                "after": "state Idle normalized",
            },
            "semantic_fields": {},
        }
    )
    contract["review_subject"] = {
        "second_pass_required": True,
        "risk_tags": ["source_normalization"],
        "review_obligations": [
            {
                "obligation_id": obligation_id,
                "risk_tag": "source_normalization",
                "element_ids": ["source:normalization:1"],
                "expected_origins": {
                    "source:normalization:1": "source_owned",
                },
                "source_refs": ["fixture.puml:line:2"],
                "rationale": "Fixture transport-only source normalization occurrence.",
            }
        ],
    }

    with pytest.raises(RuntimeError, match="lacks exact rule/before/after binding"):
        builder._validate_review(
            review=review,
            case_id="0000",
            pair_id="llms_emp_feedback_final_0000",
            comparison={"review_subject_sha256": "a" * 64},
            contract=contract,
            contract_sha256="b" * 64,
            nl_text=REVIEW_NL,
            source_text=REVIEW_SOURCE,
            fcstm_text=REVIEW_FCSTM,
            validator=validator,
        )

    assessment = review["second_pass"]["risk_assessments"][0]
    assessment["rationale"] = (
        f"{obligation_id} source_normalization binds source_input.fixture_rule exactly: "
        "state Idle -> state Idle normalized."
    )
    builder._validate_review(
        review=review,
        case_id="0000",
        pair_id="llms_emp_feedback_final_0000",
        comparison={"review_subject_sha256": "a" * 64},
        contract=contract,
        contract_sha256="b" * 64,
        nl_text=REVIEW_NL,
        source_text=REVIEW_SOURCE,
        fcstm_text=REVIEW_FCSTM,
        validator=validator,
    )


def test_pair_builder_rejects_mixed_or_partial_ordered_batch(tmp_path: Path):
    builder = _load_pair_builder_module()
    path = tmp_path / "rows.jsonl"
    path.write_text(
        "".join(json.dumps({"case_id": f"{index:04d}"}) + "\n" for index in range(59)),
        encoding="utf-8",
    )
    with pytest.raises(RuntimeError, match="not the ordered 0000..0059 batch"):
        builder._ordered_rows(path, "case_id")


def test_pair_builder_rejects_stale_implementation_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    builder = _load_pair_builder_module()
    evidence = tmp_path / "evidence"
    evidence.mkdir()
    current = builder._current_implementation_sha256()
    java_build = _fixture_java_build_identity()
    _write_manifest_fixture(
        builder=builder,
        evidence_dir=evidence,
        implementation_sha256="0" * 64,
        java_build=java_build,
    )
    monkeypatch.setattr(builder, "_display", lambda _: "fixture-evidence")
    monkeypatch.setattr(builder, "_current_java_frontend_build", lambda: java_build)
    monkeypatch.setattr(
        builder,
        "_current_java_frontend_source_identity",
        lambda: builder.java_frontend_source_identity(java_build),
    )
    monkeypatch.setattr(builder, "_current_pyfcstm_commit", lambda: "c" * 40)

    with pytest.raises(RuntimeError, match="implementation-tree hash is stale"):
        builder._validate_manifest(evidence, allow_ineligible=False)

    manifest = json.loads((evidence / "manifest.json").read_text(encoding="utf-8"))
    manifest["implementation_tree_sha256"] = current
    (evidence / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    builder._validate_manifest(evidence, allow_ineligible=False)


def test_pair_builder_rejects_extra_machine_artifact_not_in_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    builder = _load_pair_builder_module()
    evidence = tmp_path / "evidence"
    evidence.mkdir()
    java_build = _fixture_java_build_identity()
    _write_manifest_fixture(
        builder=builder,
        evidence_dir=evidence,
        implementation_sha256=builder._current_implementation_sha256(),
        java_build=java_build,
    )
    monkeypatch.setattr(builder, "_display", lambda _: "fixture-evidence")
    monkeypatch.setattr(builder, "_current_java_frontend_build", lambda: java_build)
    monkeypatch.setattr(
        builder,
        "_current_java_frontend_source_identity",
        lambda: builder.java_frontend_source_identity(java_build),
    )
    monkeypatch.setattr(builder, "_current_pyfcstm_commit", lambda: "c" * 40)
    builder._validate_manifest(evidence, allow_ineligible=False)

    canonical = evidence / "canonical"
    canonical.mkdir()
    (canonical / "mixed-batch.json").write_text("{}\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="artifact inventory does not match"):
        builder._validate_manifest(evidence, allow_ineligible=False)


def test_pair_builder_rejects_pair_pool_path_or_hash_drift(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    builder = _load_pair_builder_module()
    pairs = tmp_path / "pairs.jsonl"
    pairs.write_text('{"pair_id":"fixture"}\n', encoding="utf-8")
    manifest = {
        "pairs_path": "fixture/pairs.jsonl",
        "pairs_sha256": builder._sha256_bytes(pairs.read_bytes()),
    }
    monkeypatch.setattr(builder, "_display", lambda _: "fixture/pairs.jsonl")
    builder._validate_pairs_input(manifest, pairs)

    monkeypatch.setattr(builder, "_display", lambda _: "other/pairs.jsonl")
    with pytest.raises(RuntimeError, match="pair-pool path"):
        builder._validate_pairs_input(manifest, pairs)

    monkeypatch.setattr(builder, "_display", lambda _: "fixture/pairs.jsonl")
    pairs.write_text('{"pair_id":"tampered"}\n', encoding="utf-8")
    with pytest.raises(RuntimeError, match="pair-pool hash drift"):
        builder._validate_pairs_input(manifest, pairs)


def test_pair_builder_rejects_working_contract_path_and_hash_drift(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    builder = _load_pair_builder_module()
    evidence = tmp_path / "evidence"
    pair_id = "llms_emp_feedback_final_0000"
    paths = {
        "canonical_path": evidence / "canonical" / f"{pair_id}.json",
        "fcstm_path": evidence / "fcstm" / f"{pair_id}.fcstm",
        "parse_inspect_path": evidence / "parse_inspect" / f"{pair_id}.json",
        "source_trace_path": evidence / "source_traces" / f"{pair_id}.json",
    }
    for index, path in enumerate(paths.values()):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"artifact-{index}\n", encoding="utf-8")
    source_trace = {"entries": []}
    detailed = {"verdict": "structure_preserved"}
    case_report = {"ast_audit": {"status": "passed"}}
    case_report_path = evidence / "case_reports" / f"{pair_id}.json"
    case_report_path.parent.mkdir(parents=True)
    case_report_path.write_text(
        json.dumps(case_report, sort_keys=True) + "\n", encoding="utf-8"
    )
    monkeypatch.setattr(builder, "_display", lambda path: path.name)
    bindings = {field: path.name for field, path in paths.items()} | {
        "canonical_file_sha256": builder._sha256_bytes(
            paths["canonical_path"].read_bytes()
        ),
        "fcstm_file_sha256": builder._sha256_bytes(paths["fcstm_path"].read_bytes()),
        "parse_inspect_file_sha256": builder._sha256_bytes(
            paths["parse_inspect_path"].read_bytes()
        ),
        "source_trace_file_sha256": builder._sha256_bytes(
            paths["source_trace_path"].read_bytes()
        ),
        "comparison_sha256": builder._sha256_json(detailed),
        "ast_audit_sha256": builder._sha256_json(case_report["ast_audit"]),
    }
    contract = {
        "artifact_bindings": bindings,
        "source_trace_base": source_trace,
    }
    comparison = {
        "case_report_sha256": builder._sha256_bytes(case_report_path.read_bytes())
    }
    kwargs = {
        "evidence_dir": evidence,
        "pair_id": pair_id,
        "case_id": "0000",
        "comparison": comparison,
        "detailed": detailed,
        "case_report": case_report,
        "case_report_path": case_report_path,
        "contract": contract,
        "source_trace": source_trace,
    }
    builder._validate_contract_artifact_bindings(**kwargs)

    bindings["canonical_path"] = "wrong.json"
    with pytest.raises(RuntimeError, match="canonical_path drift"):
        builder._validate_contract_artifact_bindings(**kwargs)
    bindings["canonical_path"] = paths["canonical_path"].name
    bindings["canonical_file_sha256"] = "0" * 64
    with pytest.raises(RuntimeError, match="canonical_file_sha256 drift"):
        builder._validate_contract_artifact_bindings(**kwargs)


def test_pair_builder_atomic_publish_replaces_complete_directory(tmp_path: Path):
    builder = _load_pair_builder_module()
    evidence = tmp_path / "evidence"
    staging = tmp_path / ".evidence.tmp"
    evidence.mkdir()
    staging.mkdir()
    (evidence / "old.txt").write_text("old", encoding="utf-8")
    (staging / "PAIR_INDEX.md").write_text("new", encoding="utf-8")

    builder._atomic_publish(staging, evidence)

    assert not staging.exists()
    assert not (evidence / "old.txt").exists()
    assert (evidence / "PAIR_INDEX.md").read_text(encoding="utf-8") == "new"


def test_pair_builder_check_rejects_extra_file_and_tampered_seal(tmp_path: Path):
    builder = _load_pair_builder_module()
    evidence = tmp_path / "evidence"
    staging = tmp_path / "staging"
    for root in (evidence, staging):
        (root / "pairs/0000").mkdir(parents=True)
        (root / "MANUAL_REVIEW.jsonl").write_text("review\n", encoding="utf-8")
        (root / "MANUAL_REVIEW.md").write_text("review md\n", encoding="utf-8")
        (root / "PAIR_INDEX.md").write_text("index\n", encoding="utf-8")
        (root / "pairs/0000/README.md").write_text("pair\n", encoding="utf-8")
        (root / "PUBLICATION_SEAL.json").write_text("seal\n", encoding="utf-8")
    derived = builder._derived_inventory(staging)
    builder._check_publication(
        evidence_dir=evidence,
        staging_dir=staging,
        derived_inventory=derived,
    )

    extra = evidence / "pairs/0000/stale.fcstm"
    extra.write_text("stale\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="publication inventory drift"):
        builder._check_publication(
            evidence_dir=evidence,
            staging_dir=staging,
            derived_inventory=derived,
        )
    extra.unlink()
    (evidence / "PUBLICATION_SEAL.json").write_text("tampered\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="PUBLICATION_SEAL.json"):
        builder._check_publication(
            evidence_dir=evidence,
            staging_dir=staging,
            derived_inventory=derived,
        )


def test_frozen_60_review_obligations_have_exact_occurrence_evidence():
    _require_feedback_final_evidence()
    source_rows = {row["pair_id"]: row for row in _rows()}
    obligation_count = 0
    covered_element_count = 0
    normalization_count = 0

    for pair_id, source_row in source_rows.items():
        contract = json.loads(
            (EVIDENCE / "working_contracts" / f"{pair_id}.json").read_text(
                encoding="utf-8"
            )
        )
        fcstm_text = (EVIDENCE / "fcstm" / f"{pair_id}.fcstm").read_text(
            encoding="utf-8"
        )
        source_text = source_row["stm0_text"]
        elements = {item["element_id"]: item for item in contract["elements"]}
        macros = {item["macro_id"]: item for item in contract["macros"]}
        for obligation in contract["review_subject"]["review_obligations"]:
            obligation_count += 1
            assert obligation["source_refs"]
            for source_ref in obligation["source_refs"]:
                anchor = plantuml_evidence_anchor(
                    source_text=source_text,
                    source_ref=source_ref,
                )
                assert anchor.startswith(f"source-ref:{source_ref}|")

            anchors = fcstm_evidence_anchors(
                fcstm_text=fcstm_text,
                element_ids=obligation["element_ids"],
                elements_by_id=elements,
                macros_by_id=macros,
            )
            if obligation["risk_tag"] == "source_normalization":
                normalization_count += 1
                assert anchors == []
                continue
            assert anchors
            for element_id in obligation["element_ids"]:
                covered_element_count += 1
                assert any(
                    _fcstm_anchor_matches_element(
                        fcstm_text=fcstm_text,
                        anchor=anchor,
                        element_id=element_id,
                        elements_by_id=elements,
                        macros_by_id=macros,
                    )
                    for anchor in anchors
                )

    assert obligation_count == 358
    assert normalization_count == 6
    assert covered_element_count == 773


def test_committed_60_pair_manual_review_matches_frozen_sources_and_fcstm():
    _require_feedback_final_evidence()
    if not (EVIDENCE / "PUBLICATION_SEAL.json").is_file():
        pytest.skip("main-session pair review has not been published yet")
    manifest = json.loads((EVIDENCE / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "r4_5.llms_emp_java_batch.v6"
    assert manifest["evidence_eligible"] is True
    manual_text = (EVIDENCE / "MANUAL_REVIEW.md").read_text(encoding="utf-8")
    manual_rows = [
        json.loads(line)
        for line in (EVIDENCE / "MANUAL_REVIEW.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    assert [row["case_id"] for row in manual_rows] == [
        f"{index:04d}" for index in range(60)
    ]
    assert all(row["notes"].strip() and row["verdict"] == "pass" for row in manual_rows)
    assert all(all(row["reviewed_inputs"].values()) for row in manual_rows)

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
    assert (
        set(source_rows)
        == set(comparison_rows)
        == {row["case_id"] for row in manual_rows}
    )

    for row in manual_rows:
        case_id = row["case_id"]
        fcstm_path = EVIDENCE / "fcstm" / f"{source_rows[case_id]['pair_id']}.fcstm"
        contract_path = (
            EVIDENCE / "working_contracts" / f"{source_rows[case_id]['pair_id']}.json"
        )
        actual_fcstm_sha256 = hashlib.sha256(fcstm_path.read_bytes()).hexdigest()
        actual_contract_sha256 = hashlib.sha256(contract_path.read_bytes()).hexdigest()
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        assert (
            source_rows[case_id]["stm0_sha256"]
            == comparison_rows[case_id]["source_sha256"]
        )
        assert comparison_rows[case_id]["fcstm_sha256"] == actual_fcstm_sha256
        assert row["working_contract_sha256"] == actual_contract_sha256
        assert (
            row["review_subject_sha256"]
            == comparison_rows[case_id]["review_subject_sha256"]
        )
        assert contract["usage_gate"] == "discover_input_with_capability_mask"
        assert (
            contract["attribution_policy"]["main_result_conversion_artifact_limit"] == 0
        )
        assert all(
            entry["attribution_boundary"]["closure_claim_allowed"] is False
            for entry in contract["source_trace_base"]["entries"]
        )
        assert comparison_rows[case_id]["verdict"] == "structure_preserved"
        assert comparison_rows[case_id]["fcstm_execution_eligible"] is False
        assert comparison_rows[case_id]["discover_eligible"] is False

    assert "不表示全局行为等价" in manual_text
    seal = json.loads((EVIDENCE / "PUBLICATION_SEAL.json").read_text(encoding="utf-8"))
    assert seal["case_count"] == 60
    assert seal["status"] == "main_session_reviewed_ready_for_discover"


def test_committed_pair_pages_show_complete_nl_plantuml_and_fcstm_for_all_60_cases():
    _require_feedback_final_evidence()
    if not (EVIDENCE / "PUBLICATION_SEAL.json").is_file():
        pytest.skip("main-session pair review has not been published yet")
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
            (EVIDENCE / "case_reports" / f"{pair_id}.json").read_text(encoding="utf-8")
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
        assert (case_dir / "nl.txt").read_text(encoding="utf-8") == source_row[
            "nl_text"
        ]
        assert (case_dir / "plantuml.puml").read_text(encoding="utf-8") == source_row[
            "stm0_text"
        ]
        assert (case_dir / "fcstm.fcstm").read_text(encoding="utf-8") == fcstm_text
        assert source_row["nl_sha256"] in page_text
        assert source_row["stm0_sha256"] in page_text
        assert "## Official identity ledger" in page_text
        assert case_report["official_identity_reconciliation"]["status"] == "aligned"
        assert "official identity states / transitions" in page_text
        assert (
            "working bundle usage gate：`discover_input_with_capability_mask`"
            in page_text
        )
        assert "capability source-static / simulation / transition-trace" in page_text
        assert "main-result conversion artifact limit：`0`" in page_text
        assert f"./pairs/{case_id}/README.md" in index_text
        assert f"./pairs/{case_id}/nl.txt" in index_text
        assert f"./pairs/{case_id}/plantuml.puml" in index_text
        assert f"./pairs/{case_id}/fcstm.fcstm" in index_text
        assert f"../../case_reports/{pair_id}.json" in page_text
        assert f"../../working_contracts/{pair_id}.json" in page_text
        assert f"../../source_traces/{pair_id}.json" in page_text

    assert (EVIDENCE / "PUBLICATION_SEAL.json").is_file()
