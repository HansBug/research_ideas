from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import pytest

from paper_stm_repair_conversion.adapters.plantuml_source import (
    java_frontend_build_identity,
    parse_plantuml_source,
)
from paper_stm_repair_conversion.evidence_integrity import (
    relevant_implementation_sha256,
)
from paper_stm_repair_representation.plantuml_source_audit import audit_lowered_artifact
from paper_stm_repair_representation.plantuml_source_lowering import (
    lower_plantuml_source,
)
from paper_stm_repair_representation.manual_pair_review import (
    RISK_ASSESSMENT_BY_TAG,
    _fcstm_anchor_matches_element,
    fcstm_evidence_anchors,
    plantuml_evidence_anchor,
)
from paper_stm_repair_representation.plantuml_working_bundle import (
    WorkingBundleError,
    load_attribution_safe_working_bundle,
)
from paper_stm_repair_representation.plantuml_working_contract import (
    bind_inspect_diagnostics,
    build_review_obligations,
)
from pyfcstm.diagnostics.inspect import inspect_model
from pyfcstm.model.load import load_state_machine_from_text


SOURCE = """@startuml
[*] --> Locked
state Locked
state Unlocked
state Alarm
Locked --> Unlocked : unlock [pin_ok] / alarm=false
Locked --> Alarm : unlock [pin_ok] / alarm=true
@enduml
"""


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "project_1_llm_state_machine_modeling").is_dir():
            return parent
    raise RuntimeError("repository root not found")


REAL_REPO = _repo_root()
PAPER_REL = Path("project_1_llm_state_machine_modeling/paper_stm_repair")
PAIR_ID = "llms_emp_feedback_final_0000"
FORMAL_EVIDENCE = (
    REAL_REPO / PAPER_REL / "pipeline/representation/reports/llms_emp_r45_java_60"
)
PUBLICATION_READY_STATUS = "main_session_reviewed_ready_for_discover"


def _exact_anchor_fixture() -> tuple[
    str, dict[str, dict], dict[str, dict]
]:
    fcstm = """state Root {
    state Left {
        state Idle named "Idle";
    }
    state Right {
        state Idle named "Idle";
    }
    state Ready named "Ready";
    Idle -> Ready : /Enter_Cooking_Time;
    Idle -> Ready : /Enter_Cooking_Time;
}
"""
    elements = [
        {
            "element_id": "source:state:Left.Idle",
            "origin": "source_owned",
            "model_refs": ["state:Root.Left.Idle"],
            "macro_ids": [],
            "metadata": {},
        },
        {
            "element_id": "source:state:Right.Idle",
            "origin": "source_owned",
            "model_refs": ["state:Root.Right.Idle"],
            "macro_ids": [],
            "metadata": {},
        },
        {
            "element_id": "source:transition:tr_0001",
            "origin": "source_owned",
            "model_refs": ["macro:transition:tr_0001"],
            "macro_ids": ["macro:transition:tr_0001"],
            "metadata": {},
        },
        {
            "element_id": "source:transition:tr_0002",
            "origin": "source_owned",
            "model_refs": ["macro:transition:tr_0002"],
            "macro_ids": ["macro:transition:tr_0002"],
            "metadata": {},
        },
        {
            "element_id": "compiler:transition_segment:tr_0001:segment:1",
            "origin": "compiler_owned",
            "model_refs": [],
            "macro_ids": ["macro:transition:tr_0001"],
            "metadata": {
                "scope": "",
                "line": "Idle -> Ready : /Enter_Cooking_Time;",
                "scope_line_occurrence": 1,
            },
        },
        {
            "element_id": "compiler:transition_segment:tr_0002:segment:1",
            "origin": "compiler_owned",
            "model_refs": [],
            "macro_ids": ["macro:transition:tr_0002"],
            "metadata": {
                "scope": "",
                "line": "Idle -> Ready : /Enter_Cooking_Time;",
                "scope_line_occurrence": 2,
            },
        },
    ]
    macros = [
        {
            "macro_id": "macro:transition:tr_0001",
            "source_element_ids": ["source:transition:tr_0001"],
            "member_element_ids": [
                "compiler:transition_segment:tr_0001:segment:1"
            ],
        },
        {
            "macro_id": "macro:transition:tr_0002",
            "source_element_ids": ["source:transition:tr_0002"],
            "member_element_ids": [
                "compiler:transition_segment:tr_0002:segment:1"
            ],
        },
    ]
    return (
        fcstm,
        {item["element_id"]: item for item in elements},
        {item["macro_id"]: item for item in macros},
    )


def _sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha_text(value: str) -> str:
    return _sha_bytes(value.encode("utf-8"))


def _sha_json(value: object) -> str:
    return _sha_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    )


def test_exact_anchor_distinguishes_duplicate_transition_occurrences():
    fcstm, elements, macros = _exact_anchor_fixture()
    first = fcstm_evidence_anchors(
        fcstm_text=fcstm,
        element_ids=["source:transition:tr_0001"],
        elements_by_id=elements,
        macros_by_id=macros,
    )
    second = fcstm_evidence_anchors(
        fcstm_text=fcstm,
        element_ids=["source:transition:tr_0002"],
        elements_by_id=elements,
        macros_by_id=macros,
    )

    assert len(first) == len(second) == 1
    assert "@line:9|" in first[0]
    assert "@line:10|" in second[0]
    assert not _fcstm_anchor_matches_element(
        fcstm_text=fcstm,
        anchor=first[0],
        element_id="source:transition:tr_0002",
        elements_by_id=elements,
        macros_by_id=macros,
    )

    reversed_elements = dict(reversed(list(elements.items())))
    assert fcstm_evidence_anchors(
        fcstm_text=fcstm,
        element_ids=["source:transition:tr_0001"],
        elements_by_id=reversed_elements,
        macros_by_id=macros,
    ) == first


def test_exact_anchor_distinguishes_same_named_states_by_scope():
    fcstm, elements, macros = _exact_anchor_fixture()
    left = fcstm_evidence_anchors(
        fcstm_text=fcstm,
        element_ids=["source:state:Left.Idle"],
        elements_by_id=elements,
        macros_by_id=macros,
    )[0]
    right = fcstm_evidence_anchors(
        fcstm_text=fcstm,
        element_ids=["source:state:Right.Idle"],
        elements_by_id=elements,
        macros_by_id=macros,
    )[0]

    assert "@line:3|" in left
    assert "@line:6|" in right
    assert not _fcstm_anchor_matches_element(
        fcstm_text=fcstm,
        anchor=left,
        element_id="source:state:Right.Idle",
        elements_by_id=elements,
        macros_by_id=macros,
    )


def test_exact_anchor_rejects_suffix_only_body_scope_match():
    fcstm = '''state Root {
    state Outer {
        state Idle named "Idle\\n[PlantUML body] active";
    }
}
'''
    element_id = "source:body:Idle:1"
    elements = {
        element_id: {
            "element_id": element_id,
            "origin": "source_owned",
            "kind": "state_body_text",
            "model_refs": [],
            "macro_ids": [],
            "metadata": {"state_id": "Idle", "text": "active"},
            "semantic_fields": {"text": "active"},
        }
    }

    assert fcstm_evidence_anchors(
        fcstm_text=fcstm,
        element_ids=[element_id],
        elements_by_id=elements,
        macros_by_id={},
    ) == []


def test_exact_anchor_matches_json_escaped_body_text():
    fcstm = '''state Root {
    state DoorOpen named "DoorOpen\\n[PlantUML body] as \\"Door Open\\"";
}
'''
    element_id = "source:body:DoorOpen:1"
    elements = {
        element_id: {
            "element_id": element_id,
            "origin": "source_owned",
            "kind": "state_body_text",
            "model_refs": [],
            "macro_ids": [],
            "metadata": {"state_id": "DoorOpen", "text": 'as "Door Open"'},
            "semantic_fields": {"text": 'as "Door Open"'},
        }
    }

    assert fcstm_evidence_anchors(
        fcstm_text=fcstm,
        element_ids=[element_id],
        elements_by_id=elements,
        macros_by_id={},
    ) == [
        'element-ref:source:body:DoorOpen:1@line:2|state DoorOpen named '
        '"DoorOpen\\n[PlantUML body] as \\"Door Open\\"";'
    ]


def test_exact_anchor_distinguishes_lifecycle_kind_and_occurrence():
    fcstm = '''state Root {
    state Running {
        enter abstract Tick;
        exit abstract Tick;
        enter abstract Tick;
    }
}
'''
    source_ids = [
        "source:lifecycle:Running:1",
        "source:lifecycle:Running:2",
        "source:lifecycle:Running:3",
    ]
    member_ids = [
        "compiler:lifecycle_action:Running:1:Tick",
        "compiler:lifecycle_action:Running:2:Tick",
        "compiler:lifecycle_action:Running:3:Tick",
    ]
    kinds = ["entry", "exit", "entry"]
    elements: dict[str, dict] = {}
    macros: dict[str, dict] = {}
    for occurrence, (source_id, member_id, lifecycle_kind) in enumerate(
        zip(source_ids, member_ids, kinds), start=1
    ):
        macro_id = f"macro:lifecycle_projection:Running:{occurrence}"
        elements[source_id] = {
            "element_id": source_id,
            "origin": "source_owned",
            "kind": "lifecycle_action",
            "model_refs": [macro_id],
            "macro_ids": [macro_id],
            "metadata": {
                "state_id": "Running",
                "lifecycle_kind": lifecycle_kind,
                "text": "Tick",
            },
        }
        elements[member_id] = {
            "element_id": member_id,
            "origin": "compiler_owned",
            "kind": "abstract_lifecycle_projection",
            "model_refs": ["action:Tick"],
            "macro_ids": [macro_id],
            "metadata": {},
        }
        macros[macro_id] = {
            "macro_id": macro_id,
            "source_element_ids": [source_id],
            "member_element_ids": [member_id],
        }

    anchors = [
        fcstm_evidence_anchors(
            fcstm_text=fcstm,
            element_ids=[source_id],
            elements_by_id=elements,
            macros_by_id=macros,
        )[0]
        for source_id in source_ids
    ]

    assert [anchor.split("@line:", 1)[1].split("|", 1)[0] for anchor in anchors] == [
        "3",
        "4",
        "5",
    ]
    assert not _fcstm_anchor_matches_element(
        fcstm_text=fcstm,
        anchor=anchors[0],
        element_id=source_ids[1],
        elements_by_id=elements,
        macros_by_id=macros,
    )


def test_exact_anchor_rejects_wrong_element_id_with_correct_line():
    fcstm, elements, macros = _exact_anchor_fixture()
    anchor = fcstm_evidence_anchors(
        fcstm_text=fcstm,
        element_ids=["source:state:Left.Idle"],
        elements_by_id=elements,
        macros_by_id=macros,
    )[0]
    forged = anchor.replace(
        "element-ref:source:state:Left.Idle",
        "element-ref:source:state:Right.Idle",
    )

    assert not _fcstm_anchor_matches_element(
        fcstm_text=fcstm,
        anchor=forged,
        element_id="source:state:Left.Idle",
        elements_by_id=elements,
        macros_by_id=macros,
    )


def test_exact_anchor_rejects_wrong_line_number_with_correct_element():
    fcstm, elements, macros = _exact_anchor_fixture()
    anchor = fcstm_evidence_anchors(
        fcstm_text=fcstm,
        element_ids=["source:state:Left.Idle"],
        elements_by_id=elements,
        macros_by_id=macros,
    )[0]
    forged = anchor.replace("@line:3|", "@line:6|")

    assert not _fcstm_anchor_matches_element(
        fcstm_text=fcstm,
        anchor=forged,
        element_id="source:state:Left.Idle",
        elements_by_id=elements,
        macros_by_id=macros,
    )


def test_exact_anchor_maps_root_scope_transition_macro():
    fcstm = """state Root {
    !Operate -> [*] : /keyOff;
}
"""
    source_id = "source:transition:tr_final"
    member_id = "compiler:transition_segment:tr_final:segment:1"
    macro_id = "macro:transition:tr_final"
    elements = {
        source_id: {
            "element_id": source_id,
            "origin": "source_owned",
            "model_refs": [macro_id],
            "macro_ids": [macro_id],
            "metadata": {},
        },
        member_id: {
            "element_id": member_id,
            "origin": "compiler_owned",
            "model_refs": [],
            "macro_ids": [macro_id],
            "metadata": {
                "scope": "__root__",
                "line": "!Operate -> [*] : /keyOff;",
                "scope_line_occurrence": 1,
            },
        },
    }
    macros = {
        macro_id: {
            "macro_id": macro_id,
            "source_element_ids": [source_id],
            "member_element_ids": [member_id],
        }
    }

    anchors = fcstm_evidence_anchors(
        fcstm_text=fcstm,
        element_ids=[source_id, member_id],
        elements_by_id=elements,
        macros_by_id=macros,
    )

    assert anchors == [
        "element-ref:compiler:transition_segment:tr_final:segment:1@line:2|"
        "!Operate -> [*] : /keyOff;"
    ]


def test_exact_anchor_maps_root_concurrent_region_metadata():
    fcstm = r"""state Root named "Root\n[PlantUML concurrent region 0] states=A" {
    state A;
}
"""
    element_id = "source:region:__root__:region:0"
    elements = {
        element_id: {
            "element_id": element_id,
            "origin": "source_owned",
            "kind": "concurrent_region",
            "model_refs": ["macro:region_projection:__root__:region:0"],
            "macro_ids": ["macro:region_projection:__root__:region:0"],
            "metadata": {"owner_scope": None, "region_index": 0},
        }
    }

    anchors = fcstm_evidence_anchors(
        fcstm_text=fcstm,
        element_ids=[element_id],
        elements_by_id=elements,
        macros_by_id={},
    )

    assert anchors == [
        'element-ref:source:region:__root__:region:0@line:1|state Root named '
        '"Root\\n[PlantUML concurrent region 0] states=A" {'
    ]


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _init_fixture_pyfcstm(repo: Path) -> str:
    pyfcstm = repo / "pyfcstm"
    pyfcstm.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(pyfcstm)], check=True)
    subprocess.run(
        ["git", "-C", str(pyfcstm), "config", "user.name", "Fixture"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(pyfcstm), "config", "user.email", "fixture@example.test"],
        check=True,
    )
    (pyfcstm / "VERSION").write_text("fixture\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(pyfcstm), "add", "VERSION"], check=True)
    subprocess.run(
        ["git", "-C", str(pyfcstm), "commit", "-q", "-m", "fixture"],
        check=True,
    )
    return subprocess.run(
        ["git", "-C", str(pyfcstm), "rev-parse", "HEAD"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()


def _derived_publication_inventory(evidence: Path) -> list[dict[str, str]]:
    paths = [
        evidence / "MANUAL_REVIEW.jsonl",
        evidence / "MANUAL_REVIEW.md",
        evidence / "PAIR_INDEX.md",
        *sorted((evidence / "pairs").rglob("*")),
    ]
    return [
        {
            "path": path.relative_to(evidence).as_posix(),
            "sha256": _sha_bytes(path.read_bytes()),
        }
        for path in paths
        if path.is_file()
    ]


def _write_reviewed_publication(
    *,
    evidence: Path,
    manifest: dict,
    pair_rows: list[dict],
    contract: dict,
    fcstm: str,
    evidence_eligible: bool,
) -> None:
    obligations = contract["review_subject"]["review_obligations"]
    review_subject_sha256 = contract["review_subject"]["review_subject_sha256"]
    working_contract_sha256 = _sha_bytes(
        (evidence / "working_contracts" / f"{PAIR_ID}.json").read_bytes()
    )
    nl_anchor = "same valid PIN"
    elements_by_id = {item["element_id"]: item for item in contract["elements"]}
    macros_by_id = {item["macro_id"]: item for item in contract["macros"]}
    correspondence_specs = []
    for source_id in ("source:state:Locked", "source:state:Unlocked"):
        source_ref = elements_by_id[source_id]["source_refs"][0]
        source_anchor = plantuml_evidence_anchor(
            source_text=SOURCE,
            source_ref=source_ref,
        )
        output_anchors = fcstm_evidence_anchors(
            fcstm_text=fcstm,
            element_ids=[source_id],
            elements_by_id=elements_by_id,
            macros_by_id=macros_by_id,
        )
        assert output_anchors
        correspondence_specs.append((source_anchor, output_anchors[0], source_id))
    reviews: list[dict] = []
    index_lines = ["# Fixture pairs", ""]
    for index, pair_row in enumerate(pair_rows):
        case_id = f"{index:04d}"
        pair_id = pair_row["pair_id"]
        risk_assessments = []
        for obligation in obligations:
            risk_tag = obligation["risk_tag"]
            risk_assessments.append(
                {
                    "obligation_id": obligation["obligation_id"],
                    "risk_tag": risk_tag,
                    "plantuml_anchors": [
                        plantuml_evidence_anchor(
                            source_text=SOURCE,
                            source_ref=source_ref,
                        )
                        for source_ref in obligation["source_refs"]
                    ],
                    "fcstm_anchors": (
                        []
                        if risk_tag == "source_normalization"
                        else fcstm_evidence_anchors(
                            fcstm_text=fcstm,
                            element_ids=obligation["element_ids"],
                            elements_by_id=elements_by_id,
                            macros_by_id=macros_by_id,
                        )
                    ),
                    "element_ids": obligation["element_ids"],
                    "assessment": RISK_ASSESSMENT_BY_TAG[risk_tag],
                    "rationale": (
                        f"{risk_tag} {obligation['obligation_id']} remains bound to its "
                        f"exact source/compiler ownership occurrence in fixture {case_id}."
                    ),
                }
            )
        risk_tags = sorted({obligation["risk_tag"] for obligation in obligations})
        review = {
            "schema_version": "paper1.manual_pair_review.v4",
            "case_id": case_id,
            "pair_id": pair_id,
            "review_subject_sha256": review_subject_sha256,
            "working_contract_sha256": working_contract_sha256,
            "reviewer_id": "main_session_llm",
            "review_method": "full_nl_plantuml_fcstm_contract_read",
            "review_context": {
                "reviewed_at": "2026-07-20T00:00:00Z",
                "session_id": "omx-pytest-fixture",
                "model_id": "gpt-fixture",
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
                    f"Fixture {case_id}: {nl_anchor} identifies the requirement that "
                    "excludes contradictory alarm outcomes."
                ),
                "plantuml_semantics": (
                    f"Fixture {case_id}: {correspondence_specs[0][0].split('|', 1)[1]} "
                    f"and {correspondence_specs[1][0].split('|', 1)[1]} remain explicit "
                    "source state occurrences."
                ),
                "fcstm_projection": (
                    f"Fixture {case_id}: {correspondence_specs[0][1].split('|', 1)[1]} "
                    f"and {correspondence_specs[1][1].split('|', 1)[1]} remain direct "
                    "FCSTM projections."
                ),
                "attribution_rationale": (
                    f"Fixture {case_id}: both correspondences bind source_owned roots; "
                    "compiler_owned and conversion elements are not promoted."
                ),
                "capability_rationale": (
                    f"Fixture {case_id}: source_static capability is eligible while runtime "
                    "evidence remains outside this review."
                ),
                "nl_anchors": [nl_anchor],
                "plantuml_anchors": [item[0] for item in correspondence_specs],
                "fcstm_anchors": [item[1] for item in correspondence_specs],
            },
            "semantic_correspondences": [
                {
                    "nl_anchor": nl_anchor,
                    "plantuml_anchor": plantuml_anchor,
                    "fcstm_anchor": fcstm_anchor,
                    "source_element_ids": [source_id],
                    "compiler_element_ids": [],
                    "projection_kind": "direct",
                    "assessment": "preserved",
                    "rationale": (
                        f"Fixture {case_id} verifies {source_id} as a direct positive-traced "
                        "source identity without compiler-owned members."
                    ),
                }
                for plantuml_anchor, fcstm_anchor, source_id in correspondence_specs
            ],
            "ownership_verdict": "pass",
            "macro_verdict": "pass",
            "capability_verdict": "pass",
            "second_pass": {
                "required": bool(obligations),
                "completed": bool(obligations),
                "review_subject_sha256": (
                    review_subject_sha256 if obligations else None
                ),
                "reviewer_id": "main_session_llm" if obligations else None,
                "review_method": (
                    "risk_focused_independent_second_pass" if obligations else None
                ),
                "risk_tags_reviewed": risk_tags,
                "risk_assessments": risk_assessments,
                "observations": (
                    f"Fixture {case_id} independently reviewed "
                    + ", ".join(risk_tags)
                    + " occurrence bindings."
                    if obligations
                    else None
                ),
                "notes": (
                    f"Fixture {case_id} second-pass evidence is independently source-bound."
                ),
            },
            "findings": [],
            "verdict": "pass",
            "notes": f"Fixture publication {case_id} is complete.",
        }
        reviews.append(review)
        pair_dir = evidence / "pairs" / case_id
        pair_dir.mkdir(parents=True)
        (pair_dir / "README.md").write_text(
            f"# Fixture {case_id}\n", encoding="utf-8"
        )
        (pair_dir / "nl.txt").write_text(pair_row["nl_text"], encoding="utf-8")
        (pair_dir / "plantuml.puml").write_text(
            pair_row["stm0_text"], encoding="utf-8"
        )
        (pair_dir / "fcstm.fcstm").write_text(fcstm, encoding="utf-8")
        index_lines.append(f"- [{case_id}](./pairs/{case_id}/README.md)")
    manual_path = evidence / "MANUAL_REVIEW.jsonl"
    manual_path.write_text(
        "".join(json.dumps(review, sort_keys=True) + "\n" for review in reviews),
        encoding="utf-8",
    )
    (evidence / "MANUAL_REVIEW.md").write_text(
        "# Fixture review\n", encoding="utf-8"
    )
    (evidence / "PAIR_INDEX.md").write_text(
        "\n".join(index_lines) + "\n", encoding="utf-8"
    )
    derived_inventory = _derived_publication_inventory(evidence)
    seal = {
        "schema_version": "paper1.llms_emp_pair_publication.v1",
        "case_count": 60,
        "evidence_eligible": evidence_eligible,
        "status": (
            PUBLICATION_READY_STATUS if evidence_eligible else "development_only"
        ),
        "manifest_sha256": _sha_bytes((evidence / "manifest.json").read_bytes()),
        "artifact_set_sha256": manifest["artifact_set_sha256"],
        "working_contract_set_sha256": manifest["working_contract_set_sha256"],
        "manual_review_file_sha256": _sha_bytes(manual_path.read_bytes()),
        "manual_review_set_sha256": _sha_json(reviews),
        "derived_artifact_inventory": derived_inventory,
        "derived_artifact_set_sha256": _sha_json(derived_inventory),
        "pair_index_sha256": _sha_bytes((evidence / "PAIR_INDEX.md").read_bytes()),
    }
    _write_json(evidence / "PUBLICATION_SEAL.json", seal)


def _refresh_publication_seal(evidence: Path) -> None:
    manifest = json.loads((evidence / "manifest.json").read_text(encoding="utf-8"))
    reviews = [
        json.loads(line)
        for line in (evidence / "MANUAL_REVIEW.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    derived_inventory = _derived_publication_inventory(evidence)
    seal = json.loads(
        (evidence / "PUBLICATION_SEAL.json").read_text(encoding="utf-8")
    )
    seal.update(
        {
            "manifest_sha256": _sha_bytes(
                (evidence / "manifest.json").read_bytes()
            ),
            "artifact_set_sha256": manifest["artifact_set_sha256"],
            "working_contract_set_sha256": manifest[
                "working_contract_set_sha256"
            ],
            "manual_review_file_sha256": _sha_bytes(
                (evidence / "MANUAL_REVIEW.jsonl").read_bytes()
            ),
            "manual_review_set_sha256": _sha_json(reviews),
            "derived_artifact_inventory": derived_inventory,
            "derived_artifact_set_sha256": _sha_json(derived_inventory),
            "pair_index_sha256": _sha_bytes(
                (evidence / "PAIR_INDEX.md").read_bytes()
            ),
        }
    )
    _write_json(evidence / "PUBLICATION_SEAL.json", seal)




def _write_bundle_fixture(
    tmp_path: Path, *, evidence_eligible: bool = True, reviewed: bool = True
) -> tuple[Path, Path]:
    repo = tmp_path / "repo"
    evidence = repo / PAPER_REL / "pipeline/representation/reports/fixture"
    pyfcstm_commit = _init_fixture_pyfcstm(repo)
    schema_dir = repo / PAPER_REL / "pipeline/representation/schemas"
    evaluation_schema_dir = repo / PAPER_REL / "pipeline/evaluation/schemas"
    schema_dir.mkdir(parents=True)
    evaluation_schema_dir.mkdir(parents=True)
    shutil.copy2(
        REAL_REPO
        / PAPER_REL
        / "pipeline/representation/schemas/working_fcstm_contract.schema.json",
        schema_dir / "working_fcstm_contract.schema.json",
    )
    shutil.copy2(
        REAL_REPO
        / PAPER_REL
        / "pipeline/representation/schemas/manual_pair_review.schema.json",
        schema_dir / "manual_pair_review.schema.json",
    )
    shutil.copy2(
        REAL_REPO
        / PAPER_REL
        / "pipeline/evaluation/schemas/source_issue_ledger.schema.json",
        evaluation_schema_dir / "source_issue_ledger.schema.json",
    )

    nl_text = (
        "Unlocking with the same valid PIN must not both disable and enable the alarm."
    )
    pair_path = repo / PAPER_REL / "corpora/fixture_pairs.jsonl"
    pair_path.parent.mkdir(parents=True)
    pair_rows = [
        {
            "pair_id": f"llms_emp_feedback_final_{index:04d}",
            "nl_text": nl_text,
            "nl_sha256": _sha_text(nl_text),
            "stm0_text": SOURCE,
            "stm0_sha256": _sha_text(SOURCE),
            "selected_stage": "phase_ii_semantic",
            "selected_stage_cell": "AE2",
        }
        for index in range(60)
    ]
    pair_row = pair_rows[0]
    pair_path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in pair_rows),
        encoding="utf-8",
    )

    canonical = parse_plantuml_source(SOURCE, example_id=PAIR_ID)
    lowered = lower_plantuml_source(canonical)
    model = load_state_machine_from_text(lowered["fcstm"])
    inspect_report = inspect_model(model).to_json()
    ast_audit = audit_lowered_artifact(
        canonical=canonical,
        fcstm=lowered["fcstm"],
        comparison=lowered["comparison"],
        model=model,
        inspect_report=inspect_report,
    )
    paths = {
        "canonical": evidence / "canonical" / f"{PAIR_ID}.json",
        "fcstm": evidence / "fcstm" / f"{PAIR_ID}.fcstm",
        "inspect": evidence / "parse_inspect" / f"{PAIR_ID}.json",
        "contract": evidence / "working_contracts" / f"{PAIR_ID}.json",
        "trace": evidence / "source_traces" / f"{PAIR_ID}.json",
        "case_report": evidence / "case_reports" / f"{PAIR_ID}.json",
    }
    _write_json(paths["canonical"], canonical)
    paths["fcstm"].parent.mkdir(parents=True)
    paths["fcstm"].write_text(lowered["fcstm"], encoding="utf-8")
    _write_json(paths["inspect"], inspect_report)
    _write_json(paths["trace"], lowered["source_trace_base"])

    contract = bind_inspect_diagnostics(
        fcstm=lowered["fcstm"],
        inspect_report=inspect_report,
        contract=lowered["working_contract"],
    )

    def rel(path: Path) -> str:
        return path.relative_to(repo).as_posix()

    contract["artifact_bindings"] = {
        "canonical_path": rel(paths["canonical"]),
        "fcstm_path": rel(paths["fcstm"]),
        "parse_inspect_path": rel(paths["inspect"]),
        "source_trace_path": rel(paths["trace"]),
        "canonical_file_sha256": _sha_bytes(paths["canonical"].read_bytes()),
        "fcstm_file_sha256": _sha_bytes(paths["fcstm"].read_bytes()),
        "parse_inspect_file_sha256": _sha_bytes(paths["inspect"].read_bytes()),
        "source_trace_file_sha256": _sha_bytes(paths["trace"].read_bytes()),
        "comparison_sha256": _sha_json(lowered["comparison"]),
        "ast_audit_sha256": _sha_json(ast_audit),
    }
    obligations = build_review_obligations(
        comparison=lowered["comparison"],
        official_identity=canonical["metadata"]["official_identity_reconciliation"],
        contract=contract,
    )
    artifact_hashes = contract["artifact_bindings"]
    review_subject_sha256 = _sha_json(
        {
            "nl_sha256": pair_row["nl_sha256"],
            "source_sha256": pair_row["stm0_sha256"],
            **{
                key: artifact_hashes[key]
                for key in (
                    "canonical_file_sha256",
                    "fcstm_file_sha256",
                    "parse_inspect_file_sha256",
                    "source_trace_file_sha256",
                    "comparison_sha256",
                    "ast_audit_sha256",
                )
            },
            "element_set_sha256": contract["inventory_digests"]["element_set_sha256"],
            "macro_set_sha256": contract["inventory_digests"]["macro_set_sha256"],
        }
    )
    contract["review_subject"] = {
        "review_subject_sha256": review_subject_sha256,
        "risk_tags": sorted({item["risk_tag"] for item in obligations}),
        "review_obligations": obligations,
        "second_pass_required": bool(obligations),
    }
    _write_json(paths["contract"], contract)
    case_report = {
        "schema_version": "r4_5.llms_emp_java_case_report.v5",
        "pair_id": PAIR_ID,
        "case_id": "0000",
        "source_sha256": pair_row["stm0_sha256"],
        "canonical_sha256": artifact_hashes["canonical_file_sha256"],
        "fcstm_sha256": artifact_hashes["fcstm_file_sha256"],
        "parse_inspect_sha256": artifact_hashes["parse_inspect_file_sha256"],
        "source_trace_sha256": artifact_hashes["source_trace_file_sha256"],
        "working_contract_sha256": _sha_bytes(paths["contract"].read_bytes()),
        "review_subject_sha256": review_subject_sha256,
        "comparison": lowered["comparison"],
        "ast_audit": ast_audit,
    }
    _write_json(paths["case_report"], case_report)
    for index in range(1, 60):
        pair_id = f"llms_emp_feedback_final_{index:04d}"
        for key, source_path in paths.items():
            suffix = source_path.suffix
            target = source_path.with_name(f"{pair_id}{suffix}")
            shutil.copy2(source_path, target)
    comparison_path = evidence / "comparison.jsonl"
    comparison_path.parent.mkdir(parents=True, exist_ok=True)
    comparison_path.write_text(
        "".join(
            json.dumps(
                {
                    "case_id": f"{index:04d}",
                    "pair_id": f"llms_emp_feedback_final_{index:04d}",
                    "case_report_sha256": _sha_bytes(
                        paths["case_report"].read_bytes()
                    ),
                    "working_contract_sha256": _sha_bytes(
                        paths["contract"].read_bytes()
                    ),
                    "review_subject_sha256": review_subject_sha256,
                },
                sort_keys=True,
            )
            + "\n"
            for index in range(60)
        ),
        encoding="utf-8",
    )
    artifact_paths = [
        path
        for directory in (
            "canonical",
            "fcstm",
            "parse_inspect",
            "working_contracts",
            "source_traces",
            "case_reports",
        )
        for path in (evidence / directory).iterdir()
        if path.is_file()
    ] + [comparison_path]
    inventory = [
        {
            "path": path.relative_to(evidence).as_posix(),
            "sha256": _sha_bytes(path.read_bytes()),
        }
        for path in sorted(artifact_paths)
    ]
    manifest = {
        "schema_version": "r4_5.llms_emp_java_batch.v5",
        "evidence_eligible": evidence_eligible,
        "output_dir": rel(evidence),
        "pairs_path": rel(pair_path),
        "pairs_sha256": _sha_bytes(pair_path.read_bytes()),
        "artifact_inventory": inventory,
        "artifact_set_sha256": _sha_json(inventory),
        "working_contract_set_sha256": _sha_json(
            [
                item
                for item in inventory
                if item["path"].startswith("working_contracts/")
            ]
        ),
        "implementation_tree_sha256": relevant_implementation_sha256(
            repo_root=repo,
            paper_root=repo / PAPER_REL,
        ),
        "java_frontend_build": java_frontend_build_identity(force=False),
        "pyfcstm_commit": pyfcstm_commit,
    }
    _write_json(evidence / "manifest.json", manifest)
    if reviewed:
        _write_reviewed_publication(
            evidence=evidence,
            manifest=manifest,
            pair_rows=pair_rows,
            contract=contract,
            fcstm=lowered["fcstm"],
            evidence_eligible=evidence_eligible,
        )
    return repo, evidence


def _confirmed_ledger(bundle) -> dict:
    elements = {
        item["element_id"]: item
        for item in bundle.working_contract["elements"]
    }
    transition_ids = [
        element_id
        for element_id, item in elements.items()
        if item["origin"] == "source_owned" and item["kind"] == "transition_macro_root"
    ][-2:]
    source_ref_by_id = {
        element_id: elements[element_id]["source_refs"][0]
        for element_id in transition_ids
    }
    source_refs = [
        {
            "element_id": element_id,
            "element_type": "transition",
            "reference": source_ref_by_id[element_id],
            "summary": "Conflicting source transition.",
        }
        for element_id in transition_ids
    ]
    source_evidence = [
        {
            "evidence_id": f"SRC{index}",
            "evidence_type": "source_stm_fragment",
            "reference": source_ref_by_id[element_id],
            "summary": "Source transition participating in the conflict.",
        }
        for index, element_id in enumerate(transition_ids, start=1)
    ]
    consistency_field_refs = [
        next(
            field_ref
            for field_ref in bundle.working_contract["capability_eligibility"]
            ["source_static_discovery"]["eligible_field_refs"]
            if field_ref.startswith(f"{element_id}#field:raw_label")
        )
        for element_id in transition_ids
    ]
    return {
        "schema_version": "source_issue_ledger.v0",
        "ledger_id": "fixture.bundle.0000",
        "case_id": "0000",
        "source_model_id": PAIR_ID,
        "ledger_scope": "formal_experiment_candidate",
        "nl_reference": {
            "reference_type": "synthetic_inline",
            "reference": "fixture NL",
            "summary": "Fixture requirement.",
        },
        "source_artifact_reference": {
            "reference_type": "synthetic_inline",
            "reference": "fixture PlantUML",
            "summary": "Fixture source state machine.",
        },
        "issues": [
            {
                "issue_id": "ISSUE.INTERNAL.001",
                "issue_level": "confirmed",
                "issue_family": "raw_internal_inconsistency",
                "confirmation_status": "confirmed",
                "confirmation_evidence_path": "raw_internal_inconsistency",
                "candidate_description": "Two source transitions conflict.",
                "source_element_refs": source_refs,
                "nl_evidence": [],
                "source_stm_evidence": source_evidence,
                "behavior_evidence": [
                    {
                        "evidence_id": "BEH1",
                        "evidence_type": "source_internal_consistency_check",
                        "reference": ";".join(consistency_field_refs),
                        "summary": "Source-static conflict check.",
                    }
                ],
                "confirmation_rationale": (
                    "The source artifact is internally contradictory; NL evidence is not "
                    "required for this v0 path."
                ),
                "attribution_boundary": {
                    "source_level_claim_allowed": True,
                    "conversion_or_lowering_related": False,
                    "representation_related": False,
                    "rationale": "The conflict is present in the raw PlantUML transitions.",
                },
                "rejection_reason": "",
                "downstream_repair_allowed": True,
                "required_future_trace": True,
                "reviewer_notes": "Fixture confirmed source issue.",
            }
        ],
        "notes": "Attribution-safe working-bundle fixture.",
    }


def test_loader_exposes_only_capability_filtered_source_fields(tmp_path: Path):
    repo, evidence = _write_bundle_fixture(tmp_path / "unreviewed", reviewed=False)
    with pytest.raises(WorkingBundleError, match="publication seal"):
        load_attribution_safe_working_bundle(evidence, "0000", repo_root=repo)
    repo, evidence = _write_bundle_fixture(tmp_path / "reviewed")
    bundle = load_attribution_safe_working_bundle(evidence, "0000", repo_root=repo)
    view = bundle.discover_view()

    assert view["pair_id"] == PAIR_ID
    assert view["source_plantuml"] == SOURCE
    assert view["protected_compiler_element_ids"]
    assert view["attribution_rules"]["candidate_conversion_artifact_policy"] == (
        "allowed_only_as_explicitly_classified_non_repairable_noise"
    )
    assert view["attribution_rules"]["source_internal_consistency_check_policy"] == (
        "manifest_bound_executed_checker_artifact_required"
    )
    assert view["attribution_rules"]["confirmed_conversion_artifact_limit"] == 0
    assert view["attribution_rules"]["repair_conversion_artifact_limit"] == 0
    assert view["attribution_rules"]["confirm_conversion_artifact_limit"] == 0
    assert view["attribution_rules"]["main_result_conversion_artifact_limit"] == 0
    assert all(
        item["element_id"].startswith("source:") for item in view["source_facts"]
    )
    assert all(
        set(item["semantic_fields"]).issubset(
            {
                field_ref.split("#field:", 1)[1]
                for field_ref in view["capability_eligibility"][
                    "source_static_discovery"
                ]["eligible_field_refs"]
                if field_ref.startswith(f"{item['element_id']}#field:")
            }
        )
        for item in view["source_facts"]
    )
    detached_contract = bundle.working_contract
    detached_contract["capability_eligibility"]["source_static_discovery"]["status"] = (
        "ineligible"
    )
    assert bundle.discover_view()["source_facts"] == view["source_facts"]
    with pytest.raises(WorkingBundleError, match="cannot authorize Confirm"):
        bundle.validate_confirm_acceptance({})


def test_loader_rejects_development_or_tampered_evidence(tmp_path: Path):
    repo, evidence = _write_bundle_fixture(tmp_path, evidence_eligible=False)
    with pytest.raises(WorkingBundleError, match="development-only"):
        load_attribution_safe_working_bundle(evidence, "0000", repo_root=repo)

    repo, evidence = _write_bundle_fixture(tmp_path / "tampered")
    fcstm = evidence / "fcstm" / f"{PAIR_ID}.fcstm"
    fcstm.write_text(fcstm.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    with pytest.raises(WorkingBundleError, match="artifact hash drift"):
        load_attribution_safe_working_bundle(evidence, "0000", repo_root=repo)


def test_loader_revalidates_rehashed_manual_review_semantics(tmp_path: Path):
    repo, evidence = _write_bundle_fixture(tmp_path)
    review_path = evidence / "MANUAL_REVIEW.jsonl"
    reviews = [
        json.loads(line)
        for line in review_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    reviews[0]["semantic_correspondences"][0]["source_element_ids"] = [
        "source:state:forged"
    ]
    review_path.write_text(
        "".join(json.dumps(review, sort_keys=True) + "\n" for review in reviews),
        encoding="utf-8",
    )
    _refresh_publication_seal(evidence)

    with pytest.raises(WorkingBundleError, match="manual review validation failed"):
        load_attribution_safe_working_bundle(evidence, "0000", repo_root=repo)


def test_loader_rejects_swapped_valid_source_correspondences(tmp_path: Path):
    repo, evidence = _write_bundle_fixture(tmp_path)
    review_path = evidence / "MANUAL_REVIEW.jsonl"
    reviews = [
        json.loads(line)
        for line in review_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    first, second = reviews[0]["semantic_correspondences"][:2]
    first["source_element_ids"] = ["source:state:Unlocked"]
    first["rationale"] = (
        "source:state:Unlocked is deliberately but incorrectly paired with the Locked "
        "PlantUML and FCSTM anchors to test relation-level validation."
    )
    second["source_element_ids"] = ["source:state:Locked"]
    second["rationale"] = (
        "source:state:Locked is deliberately but incorrectly paired with the Unlocked "
        "PlantUML and FCSTM anchors to test relation-level validation."
    )
    review_path.write_text(
        "".join(json.dumps(review, sort_keys=True) + "\n" for review in reviews),
        encoding="utf-8",
    )
    _refresh_publication_seal(evidence)

    with pytest.raises(WorkingBundleError, match="element-misaligned"):
        load_attribution_safe_working_bundle(evidence, "0000", repo_root=repo)


def test_loader_rejects_macro_correspondence_with_unrelated_compiler_member(
    tmp_path: Path,
):
    repo, evidence = _write_bundle_fixture(tmp_path)
    review_path = evidence / "MANUAL_REVIEW.jsonl"
    reviews = [
        json.loads(line)
        for line in review_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    contract = json.loads(
        (evidence / "working_contracts" / f"{PAIR_ID}.json").read_text(
            encoding="utf-8"
        )
    )
    unrelated_compiler = next(
        item["element_id"]
        for item in contract["elements"]
        if item["origin"] == "compiler_owned" and item["kind"] == "root_wrapper"
    )
    correspondence = reviews[0]["semantic_correspondences"][0]
    correspondence["compiler_element_ids"] = [unrelated_compiler]
    correspondence["projection_kind"] = "macro"
    correspondence["assessment"] = "preserved_with_exclusions"
    correspondence["rationale"] = (
        f"{correspondence['source_element_ids'][0]} is deliberately paired with unrelated "
        f"compiler member {unrelated_compiler} to test macro lineage validation."
    )
    review_path.write_text(
        "".join(json.dumps(review, sort_keys=True) + "\n" for review in reviews),
        encoding="utf-8",
    )
    _refresh_publication_seal(evidence)

    with pytest.raises(WorkingBundleError, match="not source-macro-bound"):
        load_attribution_safe_working_bundle(evidence, "0000", repo_root=repo)


def test_loader_rejects_direct_correspondence_anchored_to_undeclared_macro_member(
    tmp_path: Path,
):
    repo, evidence = _write_bundle_fixture(tmp_path)
    review_path = evidence / "MANUAL_REVIEW.jsonl"
    reviews = [
        json.loads(line)
        for line in review_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    contract = json.loads(
        (evidence / "working_contracts" / f"{PAIR_ID}.json").read_text(
            encoding="utf-8"
        )
    )
    elements = {item["element_id"]: item for item in contract["elements"]}
    macros = {item["macro_id"]: item for item in contract["macros"]}
    source_id = next(
        item["element_id"]
        for item in contract["elements"]
        if item["origin"] == "source_owned" and item["kind"] == "transition_macro_root"
    )
    member_id = macros[elements[source_id]["macro_ids"][0]]["member_element_ids"][0]
    source_text = (evidence / "pairs/0000/plantuml.puml").read_text(encoding="utf-8")
    fcstm_text = (evidence / "pairs/0000/fcstm.fcstm").read_text(encoding="utf-8")
    plantuml_anchor = plantuml_evidence_anchor(
        source_text=source_text,
        source_ref=elements[source_id]["source_refs"][0],
    )
    fcstm_anchor = fcstm_evidence_anchors(
        fcstm_text=fcstm_text,
        element_ids=[member_id],
        elements_by_id=elements,
        macros_by_id=macros,
    )[0]

    correspondence = reviews[0]["semantic_correspondences"][0]
    old_plantuml_anchor = correspondence["plantuml_anchor"]
    old_fcstm_anchor = correspondence["fcstm_anchor"]
    correspondence.update(
        {
            "plantuml_anchor": plantuml_anchor,
            "fcstm_anchor": fcstm_anchor,
            "source_element_ids": [source_id],
            "compiler_element_ids": [],
            "projection_kind": "direct",
            "assessment": "preserved",
            "rationale": (
                f"{source_id} deliberately hides compiler-owned macro member {member_id} "
                "behind a direct projection claim to exercise the ownership gate."
            ),
        }
    )
    observations = reviews[0]["observations"]
    observations["plantuml_anchors"] = [
        plantuml_anchor if anchor == old_plantuml_anchor else anchor
        for anchor in observations["plantuml_anchors"]
    ]
    observations["fcstm_anchors"] = [
        fcstm_anchor if anchor == old_fcstm_anchor else anchor
        for anchor in observations["fcstm_anchors"]
    ]
    observations["plantuml_semantics"] += (
        f" Exact transition occurrence: {plantuml_anchor.split('|', 1)[1]}"
    )
    observations["fcstm_projection"] += (
        f" Exact compiler line: {fcstm_anchor.split('|', 1)[1]}"
    )
    review_path.write_text(
        "".join(json.dumps(review, sort_keys=True) + "\n" for review in reviews),
        encoding="utf-8",
    )
    _refresh_publication_seal(evidence)

    with pytest.raises(WorkingBundleError, match="anchor ownership is undeclared"):
        load_attribution_safe_working_bundle(evidence, "0000", repo_root=repo)


def test_loader_rejects_resealed_publication_with_missing_pair_file(tmp_path: Path):
    repo, evidence = _write_bundle_fixture(tmp_path)
    (evidence / "pairs/0059/fcstm.fcstm").unlink()
    _refresh_publication_seal(evidence)

    with pytest.raises(WorkingBundleError, match="exactly 60 complete pair pages"):
        load_attribution_safe_working_bundle(evidence, "0000", repo_root=repo)


def test_loader_rejects_stale_implementation_schema(tmp_path: Path):
    repo, evidence = _write_bundle_fixture(tmp_path)
    schema_path = (
        repo
        / PAPER_REL
        / "pipeline/representation/schemas/working_fcstm_contract.schema.json"
    )
    schema_path.write_text(
        schema_path.read_text(encoding="utf-8") + "\n",
        encoding="utf-8",
    )

    with pytest.raises(WorkingBundleError, match="implementation-tree hash is stale"):
        load_attribution_safe_working_bundle(evidence, "0000", repo_root=repo)


def test_loader_rejects_stale_java_build_identity(tmp_path: Path):
    repo, evidence = _write_bundle_fixture(tmp_path)
    manifest_path = evidence / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["java_frontend_build"] = {
        **manifest["java_frontend_build"],
        "source_tree_sha256": "0" * 64,
    }
    _write_json(manifest_path, manifest)
    _refresh_publication_seal(evidence)

    with pytest.raises(WorkingBundleError, match="Java frontend build is stale"):
        load_attribution_safe_working_bundle(evidence, "0000", repo_root=repo)


def test_loader_rejects_stale_pyfcstm_commit(tmp_path: Path):
    repo, evidence = _write_bundle_fixture(tmp_path)
    version_path = repo / "pyfcstm/VERSION"
    version_path.write_text("fixture-updated\n", encoding="utf-8")
    subprocess.run(
        ["git", "-C", str(repo / "pyfcstm"), "add", "VERSION"], check=True
    )
    subprocess.run(
        ["git", "-C", str(repo / "pyfcstm"), "commit", "-q", "-m", "update"],
        check=True,
    )

    with pytest.raises(WorkingBundleError, match="pyfcstm commit is stale"):
        load_attribution_safe_working_bundle(evidence, "0000", repo_root=repo)


def test_confirmed_issue_binding_rejects_unexecuted_source_consistency_claim(
    tmp_path: Path,
):
    repo, evidence = _write_bundle_fixture(tmp_path)
    bundle = load_attribution_safe_working_bundle(evidence, "0000", repo_root=repo)
    ledger = _confirmed_ledger(bundle)
    with pytest.raises(WorkingBundleError, match="manifest-bound executed checker"):
        bundle.bind_confirmed_issues(ledger)

    compiler_id = next(
        item["element_id"]
        for item in bundle.working_contract["elements"]
        if item["origin"] == "compiler_owned"
    )
    tampered = copy.deepcopy(ledger)
    tampered["issues"][0]["source_element_refs"][0]["element_id"] = compiler_id
    with pytest.raises(WorkingBundleError, match="eligible positive source root"):
        bundle.bind_confirmed_issues(tampered)

    tampered = copy.deepcopy(ledger)
    tampered["issues"][0]["source_element_refs"][0]["reference"] = (
        "compiler:synthetic:not-in-source"
    )
    with pytest.raises(WorkingBundleError, match="source reference is not source-bound"):
        bundle.bind_confirmed_issues(tampered)

    tampered = copy.deepcopy(ledger)
    tampered["issues"][0]["source_stm_evidence"][0]["reference"] = (
        "completely fabricated source evidence"
    )
    with pytest.raises(WorkingBundleError, match="source STM evidence is not source-bound"):
        bundle.bind_confirmed_issues(tampered)

    tampered = copy.deepcopy(ledger)
    tampered["issues"][0]["source_stm_evidence"].append(
        {
            "evidence_id": "SRC-FORGED",
            "evidence_type": "source_stm_fragment",
            "reference": "compiler:synthetic:conversion-noise",
            "summary": "A forged conversion fragment beside valid source evidence.",
        }
    )
    with pytest.raises(WorkingBundleError, match="source STM evidence is not source-bound"):
        bundle.bind_confirmed_issues(tampered)


def test_confirmed_issue_binding_rejects_conversion_or_ineligible_evidence(
    tmp_path: Path,
):
    repo, evidence = _write_bundle_fixture(tmp_path)
    bundle = load_attribution_safe_working_bundle(evidence, "0000", repo_root=repo)
    ledger = _confirmed_ledger(bundle)
    ledger["issues"][0]["attribution_boundary"]["conversion_or_lowering_related"] = True
    with pytest.raises(WorkingBundleError, match="attribution contract"):
        bundle.bind_confirmed_issues(ledger)

    ledger = _confirmed_ledger(bundle)
    issue = ledger["issues"][0]
    issue["issue_family"] = "guard_condition_mismatch"
    issue["confirmation_evidence_path"] = "nl_grounded_behavioral_issue"
    issue["nl_evidence"] = [
        {
            "evidence_id": "NL1",
            "evidence_type": "nl_requirement",
            "reference": "valid PIN must not both disable and enable the alarm",
            "summary": "Requirement evidence.",
        }
    ]
    issue["behavior_evidence"] = [
        {
            "evidence_id": "BEH1",
            "evidence_type": "inspect_diagnostic",
            "reference": "inspect:fixture",
            "summary": "Baseline inspect diagnostic is attribution-ineligible.",
        }
    ]
    issue["confirmation_rationale"] = "NL and source appear inconsistent."
    with pytest.raises(WorkingBundleError, match="capability-ineligible"):
        bundle.bind_confirmed_issues(ledger)

    ledger = _confirmed_ledger(bundle)
    ledger["issues"][0]["behavior_evidence"].append(
        {
            "evidence_id": "BEH-CONVERSION",
            "evidence_type": "inspect_diagnostic",
            "reference": "compiler:synthetic:conversion-noise",
            "summary": "An ineligible conversion diagnostic mixed with valid evidence.",
        }
    )
    with pytest.raises(WorkingBundleError, match="manifest-bound executed checker"):
        bundle.bind_confirmed_issues(ledger)


def test_committed_60_cases_are_loadable_only_through_attribution_safe_view():
    manifest = _read_json_fixture(FORMAL_EVIDENCE / "manifest.json")
    if manifest.get("schema_version") != "r4_5.llms_emp_java_batch.v5":
        pytest.skip("formal v5 evidence has not been replayed yet")
    if not (FORMAL_EVIDENCE / "PUBLICATION_SEAL.json").is_file():
        pytest.skip("formal v5 evidence has not completed main-session review")
    assert manifest["evidence_eligible"] is True

    for index in range(60):
        bundle = load_attribution_safe_working_bundle(
            FORMAL_EVIDENCE,
            f"{index:04d}",
            repo_root=REAL_REPO,
        )
        view = bundle.discover_view()
        assert view["source_facts"]
        assert view["attribution_rules"]["main_result_conversion_artifact_limit"] == 0
        assert (
            view["capability_eligibility"]["repair"]["status"]
            == view["capability_eligibility"]["confirm"]["status"]
            == "not_run"
        )


def _read_json_fixture(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
