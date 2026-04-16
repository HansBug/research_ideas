from __future__ import annotations

from .expert_review_agent import heuristic_expert_review
from .expert_review_schema import ExpertReviewRequest
from .expert_review_v1_runtime import _build_input_dossier, _build_parser_dossier, _merge_artifact_dossiers


def build_request(with_reference: bool = True) -> ExpertReviewRequest:
    ref_output = """
    {
      "machine_name": "Printer",
      "states": [
        {"name": "Idle", "parent": null, "parallel_group": null, "is_history": false, "is_initial": true},
        {"name": "Ready", "parent": null, "parallel_group": null, "is_history": false, "is_initial": false},
        {"name": "Printing", "parent": null, "parallel_group": null, "is_history": false, "is_initial": false},
        {"name": "Suspended", "parent": null, "parallel_group": null, "is_history": false, "is_initial": false}
      ],
      "transitions": [
        {"source": "Idle", "target": "Ready", "event": "login", "guard": "authorized", "action": ""},
        {"source": "Ready", "target": "Printing", "event": "start", "guard": "", "action": ""},
        {"source": "Printing", "target": "Suspended", "event": "paperJam", "guard": "", "action": ""},
        {"source": "Suspended", "target": "Printing", "event": "resume", "guard": "", "action": ""}
      ]
    }
    """ if with_reference else None
    return ExpertReviewRequest(
        prompt=(
            "Review the predicted printer state machine as a modeling expert. "
            "重点检查是否遗漏关键需求，并指出任何没有需求依据的额外状态或迁移。"
        ),
        input_text=(
            "R1: When the user is authorized, printing can start.\n"
            "R2: A paper jam suspends printing and allows resume.\n"
            "R3: Logoff is not allowed during active printing."
        ),
        ref_output=ref_output,
        pred_output="""
    {
      "machine_name": "Printer",
      "states": [
        {"name": "Idle", "parent": null, "parallel_group": null, "is_history": false, "is_initial": true},
        {"name": "Ready", "parent": null, "parallel_group": null, "is_history": false, "is_initial": false},
        {"name": "Printing", "parent": null, "parallel_group": null, "is_history": false, "is_initial": false},
        {"name": "Suspended", "parent": null, "parallel_group": null, "is_history": false, "is_initial": false},
        {"name": "Maintenance", "parent": null, "parallel_group": null, "is_history": false, "is_initial": false}
      ],
      "transitions": [
        {"source": "Idle", "target": "Ready", "event": "login", "guard": "authorized", "action": ""},
        {"source": "Ready", "target": "Printing", "event": "start", "guard": "", "action": ""},
        {"source": "Printing", "target": "Suspended", "event": "paperJam", "guard": "", "action": ""},
        {"source": "Suspended", "target": "Printing", "event": "resume", "guard": "", "action": ""},
        {"source": "Ready", "target": "Maintenance", "event": "selfCheck", "guard": "", "action": ""}
      ]
    }
    """,
    )


def build_result(with_reference: bool = True):
    return heuristic_expert_review(build_request(with_reference=with_reference))


def test_heuristic_review_returns_structured_result() -> None:
    result = build_result()
    assert result.prompt.startswith("Review the predicted printer state machine")
    assert result.used_review_backend.startswith("v1_multi_agent_runtime")
    assert result.overall_score >= 0.0
    assert result.dimension_results
    assert any(item.dimension_name == "evidence_discipline" for item in result.dimension_results)
    assert all(item.reason_text for item in result.dimension_results)
    assert result.requirement_trace_results
    assert result.overall_reason_text


def test_heuristic_review_flags_extra_structure() -> None:
    result = build_result()
    extras = [item for item in result.unsupported_model_elements if item.issue_type == "extra"]
    assert extras
    assert any("maintenance" in item.element_text.lower() for item in extras)


def test_heuristic_review_supports_missing_reference() -> None:
    result = build_result(with_reference=False)
    assert result.overall_score >= 0.0
    assert result.dimension_results
    assert result.used_review_backend.startswith("v1_multi_agent_runtime")
    assert result.unsupported_model_elements == []
    assert any("mixed_evidence" in item.reason_text for item in result.dimension_results)
    assert any("Avoid exact-match penalties" in note for note in result.notes)


def test_heuristic_review_supports_unknown_free_text_format() -> None:
    request = ExpertReviewRequest(
        prompt="Help me review this behavior model and focus on coverage, missing behavior, and clarity.",
        input_text="R1: start moves the controller from Idle to Working.\nR2: error moves the controller into Fault.",
        pred_output="""
component Controller
state Idle
state Working
state Fault
Idle -> Working : start
Working -> Fault : error
    """,
        ref_output=None,
    )
    result = heuristic_expert_review(request)
    assert result.used_review_backend.startswith("v1_multi_agent_runtime")
    assert result.dimension_results
    assert result.requirement_trace_results
    assert result.overall_reason_text


def test_v1_runtime_gives_credit_to_equivalent_but_different_structure() -> None:
    request = ExpertReviewRequest(
        prompt=(
            "Review the predicted state machine. Reward semantically equivalent but differently structured designs, "
            "and focus on behavior plus unsupported extras."
        ),
        input_text=(
            "R1: login moves the system from Idle to Ready.\n"
            "R2: start moves the system from Ready to Printing.\n"
            "R3: paper jam suspends printing and allows resume.\n"
            "R4: power off can terminate from Ready or Printing."
        ),
        ref_output="""
        {
          "states": [{"name": "Idle"}, {"name": "Ready"}, {"name": "Printing"}, {"name": "Suspended"}, {"name": "Final"}],
          "transitions": [
            {"source": "Idle", "target": "Ready", "event": "login", "guard": "", "action": ""},
            {"source": "Ready", "target": "Printing", "event": "start", "guard": "", "action": ""},
            {"source": "Printing", "target": "Suspended", "event": "paperJam", "guard": "", "action": ""},
            {"source": "Suspended", "target": "Printing", "event": "resume", "guard": "", "action": ""},
            {"source": "Ready", "target": "Final", "event": "powerOff", "guard": "", "action": ""},
            {"source": "Printing", "target": "Final", "event": "powerOff", "guard": "", "action": ""}
          ]
        }
        """,
        pred_output="""
        {
          "states": [
            {"name": "Idle"},
            {"name": "Ready"},
            {"name": "Printing"},
            {"name": "Paused"},
            {"name": "JamPaused", "parent": "Paused"},
            {"name": "ReloadPaused", "parent": "Paused"},
            {"name": "Final"}
          ],
          "transitions": [
            {"source": "Idle", "target": "Ready", "event": "login", "guard": "", "action": ""},
            {"source": "Ready", "target": "Printing", "event": "start", "guard": "", "action": ""},
            {"source": "Printing", "target": "JamPaused", "event": "paperJam", "guard": "", "action": ""},
            {"source": "JamPaused", "target": "ReloadPaused", "event": "reload", "guard": "", "action": ""},
            {"source": "ReloadPaused", "target": "Printing", "event": "resume", "guard": "", "action": ""},
            {"source": "Ready", "target": "Final", "event": "powerOff", "guard": "", "action": ""},
            {"source": "Printing", "target": "Final", "event": "powerOff", "guard": "", "action": ""}
          ]
        }
        """,
    )
    result = heuristic_expert_review(request)
    assert result.overall_score >= 0.6
    assert "equivalent-but-different" in result.overall_reason_text
    behavioral = {item.dimension_name: item for item in result.dimension_results}["behavioral_consistency"]
    assert behavioral.score >= 0.5


def test_input_dossier_splits_inline_requirement_markers() -> None:
    request = ExpertReviewRequest(
        prompt="Review this model.",
        input_text="R1: login moves system from Idle to Ready. R2: powerOff only from Ready. R3: fault leads to Error.",
        pred_output="state Idle",
        ref_output=None,
    )
    dossier = _build_input_dossier(request)
    assert [item.requirement_id for item in dossier.requirements] == ["R1", "R2", "R3"]
    assert any("only from Ready" in item for item in dossier.constraints)
    assert dossier.evidence


def test_parser_dossier_probes_ttool_xml_into_structure() -> None:
    dossier = _build_parser_dossier(
        "prediction",
        """<?xml version="1.0" encoding="UTF-8"?>
<TURTLEGMODELING>
  <Modeling type="AVATAR Design" nameTab="Platoon1" tabs="Block Diagram$Camera$Leader">
    <Validated value="Vehicle;Leader;Camera;"/>
    <AVATARBlockDiagramPanel name="Block Diagram"/>
    <CONNECTOR>
      <extraparam>
        <isd value="in createPlatoon()" />
        <oso value="out createPlatoon()" />
      </extraparam>
    </CONNECTOR>
  </Modeling>
</TURTLEGMODELING>""",
    )
    assert dossier.format_guess == "ttool_xml"
    assert any(item.label == "Platoon1" for item in dossier.elements)
    assert any(item.label == "Camera" for item in dossier.elements)
    assert dossier.behaviors
    assert dossier.evidence
    assert dossier.observability in {"medium", "high"}
    assert any("probe" in note.lower() or "ttool" in note.lower() for note in dossier.parser_notes)


def test_merge_artifact_dossiers_reconciles_duplicate_llm_items() -> None:
    parser_dossier = _build_parser_dossier(
        "prediction",
        """
@startuml
[*] --> Idle
Idle --> Ready : login
@enduml
""",
    )
    merged = _merge_artifact_dossiers(
        parser_dossier,
        {
            "summary": "Merged dossier",
            "major_elements": [
                {"kind": "state", "label": "Idle", "text": "Idle state", "evidence_text": "Idle state"},
                {"kind": "state", "label": "Ready", "text": "Ready state", "evidence_text": "Ready state"},
            ],
            "major_relations": [
                {
                    "kind": "relation",
                    "source_label": "Idle",
                    "target_label": "Ready",
                    "trigger": "login",
                    "condition": "",
                    "action": "",
                    "description": "Idle to Ready on login",
                    "evidence_text": "Idle -> Ready : login",
                }
            ],
            "behaviors": ["Idle to Ready on login"],
            "constraints": [],
            "ambiguities": [],
            "observability": "high",
            "observability_reason": "LLM confirmed the same visible relation.",
        },
    )
    assert len([item for item in merged.elements if item.label == "Idle"]) == 1
    assert len([item for item in merged.relations if item.source_label == "Idle" and item.target_label == "Ready"]) == 1
    assert merged.analysis_mode == "parser_plus_llm"
