from __future__ import annotations

from .agents import arbiter as arbiter_module
from .agents import llm_helpers as llm_helpers_module
from .agents import missing_evidence_critic as missing_evidence_critic_module
from .agents import review_policy_builder as review_policy_builder_module
from .agents.final_synthesizer import coarse_overall_judgement
from .agents.input_analyst import build_input_dossier
from .agents.review_policy_builder import build_review_policy_packet
from .compatibility import heuristic_expert_review
from .graph.runtime import run_expert_review_workflow
from .schema import DimensionReviewResult, EvidenceItem, ExpertReviewRequest, RequirementTraceResult
from .tools.artifact_probe import build_parser_dossier
from .tools.dossier_merge import merge_artifact_dossiers
from .tools import policy_library as policy_library_module
from .tools.policy_library import build_review_policy
from .tools.policy_library import infer_record_diagram_type, infer_summary_row_type, infer_summary_target
from .tools.validation import evidence_summary_from_dimensions


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
    assert result.used_review_backend.startswith("langgraph_multi_agent_v1")
    assert result.overall_score >= 0.0
    assert result.dimension_results
    assert any(item.dimension_name == "evidence_discipline" for item in result.dimension_results)
    assert all(item.reason_text for item in result.dimension_results)
    assert result.requirement_trace_results
    assert result.overall_reason_text
    assert any("Agent context trimming" in note for note in result.notes)
    assert result.llm_usage_summary.llm_configured is False
    assert result.llm_usage_summary.total_tokens == 0


def test_evidence_summary_prefers_locator_bearing_items() -> None:
    summary = evidence_summary_from_dimensions(
        [
            DimensionReviewResult(
                dimension_name="semantic_completeness",
                title="Semantic Completeness",
                score=0.8,
                judgement="good",
                reason_text="reason",
                evidence=[
                    EvidenceItem(source="input", locator=None, snippet="R1", explanation="fallback"),
                    EvidenceItem(
                        source="input",
                        locator="input:requirement:r1",
                        snippet="R1",
                        explanation="locator-bearing",
                    ),
                ],
            )
        ]
    )
    assert len(summary) == 1
    assert summary[0].locator == "input:requirement:r1"


def test_coarse_overall_judgement_can_uplift_summary_level_result() -> None:
    regime = type("Regime", (), {"regime": "summary_only"})()
    dimension_results = [
        DimensionReviewResult("semantic_completeness", "Semantic Completeness", 0.82, "good", "reason"),
        DimensionReviewResult("behavioral_consistency", "Behavioral Consistency", 0.80, "good", "reason"),
        DimensionReviewResult("requirement_traceability", "Requirement Traceability", 0.79, "good", "reason"),
        DimensionReviewResult("pragmatic_clarity", "Pragmatic Clarity", 0.81, "good", "reason"),
        DimensionReviewResult("evidence_discipline", "Evidence Discipline", 0.74, "acceptable", "reason"),
    ]
    judgement = coarse_overall_judgement(regime, {"score_semantics": "summary_quality"}, 0.72, dimension_results)
    assert judgement == "good"


def test_heuristic_review_flags_extra_structure() -> None:
    result = build_result()
    extras = [item for item in result.unsupported_model_elements if item.issue_type == "extra"]
    assert extras
    assert any("maintenance" in item.element_text.lower() for item in extras)


def test_heuristic_review_supports_missing_reference() -> None:
    result = build_result(with_reference=False)
    assert result.overall_score >= 0.0
    assert result.dimension_results
    assert result.used_review_backend.startswith("langgraph_multi_agent_v1")
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
    assert result.used_review_backend.startswith("langgraph_multi_agent_v1")
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


def test_v1_runtime_preserves_branch_family_credit_for_non_isomorphic_parallel_controls() -> None:
    request = ExpertReviewRequest(
        prompt=(
            "Review the predicted state machine. Reward semantically equivalent but differently structured designs, "
            "especially when a branch family is decomposed into more detailed control logic."
        ),
        input_text=(
            "1. There are three region in this diagram.\n"
            "2. This sub-machine becomes active when a possible frontend collision, rear-end collision or collision "
            "with pedestrian is detected.\n"
            "3. The orthogonal regions of the active mode of collision avoidance allow for concurrent activation of "
            "different collision avoidance controls."
        ),
        pred_output="""
        @startuml
        [*] --> InitialState
        state InitialState {
            [*] --> DetectionState
            DetectionState --> BrakingControl : Frontend Collision Detected
            DetectionState --> SteeringControl : Rear-End Collision Detected
            DetectionState --> AlertSystem : Collision With Pedestrian Detected
        }
        state CollisionAvoidance {
            state BrakingControl {
                [*] --> ActivateABS
                ActivateABS --> ApplyBrakes : Immediate Action Required
            }
            state SteeringControl {
                [*] --> ActivateESC
                ActivateESC --> SteerAway : Collision Imminent
            }
            state AlertSystem {
                [*] --> SendAlert
                SendAlert --> SoundAlarm
            }
        }
        @enduml
        """,
        ref_output="""
        @startuml
        state Collision_Avoidance {
         [*] --> front_inactive
         front_inactive --> avoid_frontend_collision: dist_to_front<10 & urban=true
         avoid_frontend_collision --> front_inactive: dist_to_front>15
         --
         [*] --> rear_inactive
         rear_inactive --> avoid_rearend_collision: dist_to_rear<5 & vel>30
         avoid_rearend_collision --> rear_inactive: dist_to_rear>12
         --
         [*] --> pedestrian_inactive
         pedestrian_inactive --> avoid_pedestrian_collision: pedestrian_detected
         avoid_pedestrian_collision --> pedestrian_inactive
        }
        @enduml
        """,
    )
    result = heuristic_expert_review(request)
    assert result.overall_score >= 0.55
    assert "branch-family restructuring" in result.overall_reason_text
    assert not any("InitialState" in item.element_text for item in result.unsupported_model_elements)


def test_v1_runtime_penalizes_parallel_branch_collapse_with_cross_state_transitions() -> None:
    request = ExpertReviewRequest(
        prompt=(
            "Review the predicted state machine. Penalize unsupported cross-branch transitions when the reference "
            "exposes orthogonal or parallel structure."
        ),
        input_text=(
            "1. The system begins in the PumpControl state.\n"
            "2. Within the PumpControl state, there are three main substates: PumpState, WaterState, and MethaneState.\n"
            "3. The system first transitions to the PumpState substate.\n"
            "4. The system can also transition to the WaterState substate.\n"
            "5. Similarly, the system can transition to the MethaneState substate."
        ),
        pred_output="""
        @startuml
        [*] --> PumpControl
        state PumpControl {
        [*] --> PumpState
        state PumpState
        state WaterState
        state MethaneState
        PumpState --> WaterState : Water Flow Detected
        PumpState --> MethaneState : Methane Flow Detected
        WaterState --> PumpState : Water Flow Controlled
        WaterState --> MethaneState : Transition to Methane
        MethaneState --> PumpState : Methane Flow Controlled
        MethaneState --> WaterState : Transition to Water
        }
        @enduml
        """,
        ref_output="""
        @startuml
        [*]-->PumpControl
        state PumpControl{
        [*] --> PumpState
        --
        [*] --> WaterState
        --
        [*] --> MethaneState
        }
        @enduml
        """,
    )
    result = heuristic_expert_review(request)
    assert result.overall_score < 0.5
    assert "parallel or orthogonal structure mismatch" in result.overall_reason_text
    assert any(item.issue_type == "contradiction" for item in result.unsupported_model_elements)


def test_input_dossier_splits_inline_requirement_markers() -> None:
    request = ExpertReviewRequest(
        prompt="Review this model.",
        input_text="R1: login moves system from Idle to Ready. R2: powerOff only from Ready. R3: fault leads to Error.",
        pred_output="state Idle",
        ref_output=None,
    )
    dossier = build_input_dossier(request)
    assert [item.requirement_id for item in dossier.requirements] == ["R1", "R2", "R3"]
    assert any("only from Ready" in item for item in dossier.constraints)
    assert dossier.evidence


def test_parser_dossier_probes_ttool_xml_into_structure() -> None:
    dossier = build_parser_dossier(
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
    parser_dossier = build_parser_dossier(
        "prediction",
        """
@startuml
[*] --> Idle
Idle --> Ready : login
@enduml
""",
    )
    merged = merge_artifact_dossiers(
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


def test_v1_runtime_summary_policy_distinguishes_average_and_stddev_rows() -> None:
    average_request = ExpertReviewRequest(
        prompt=(
            "You are an expert reviewer for generated software modeling artifacts under partial public evidence.\n"
            "This is a summary-level task for a published score row.\n"
            "Public summary row semantics: This published row is an average or aggregate quality statistic.\n"
            "Calibrate the coarse score to that public summary semantics and avoid pseudo-precise element blame."
        ),
        input_text=(
            "The controller has Idle, Monitoring, and Alert modes. It reacts to darkness, presence detection, and WiFi updates."
        ),
        pred_output="""
        @startuml
        [*] --> Idle
        Idle --> Monitoring : darkness
        Monitoring --> Alert : presenceDetected
        Alert --> Monitoring : clear
        Monitoring --> Idle : dayLight
        @enduml
        """,
        ref_output=None,
    )
    stddev_request = ExpertReviewRequest(
        prompt=average_request.prompt.replace(
            "average or aggregate quality statistic",
            "standard-deviation or dispersion statistic",
        ),
        input_text=average_request.input_text,
        pred_output=average_request.pred_output,
        ref_output=None,
    )
    average_result = heuristic_expert_review(average_request)
    stddev_result = heuristic_expert_review(stddev_request)
    assert average_result.overall_score > stddev_result.overall_score
    assert average_result.unsupported_model_elements == []
    assert stddev_result.unsupported_model_elements == []


def test_summary_policy_library_infers_row_type_and_target_from_public_prompt() -> None:
    prompt = (
        "You are an expert reviewer for generated software modeling artifacts under partial public evidence.\n"
        "This is a summary-level task for BD.\n"
        "Public summary row semantics: This published row is a raw public score row.\n"
        "Calibrate the coarse score to that public summary semantics and avoid pseudo-precise element blame."
    )
    assert infer_summary_row_type(prompt) == "raw_score_row"
    assert infer_summary_target(prompt) == "BD"


def test_policy_library_infers_record_diagram_type_from_prompt() -> None:
    prompt = (
        "You are an expert reviewer for generated software modeling artifacts.\n"
        "Target type: act / generated_behavior_model.\n"
        "Treat the prompt as a review contract, not as a generation request."
    )
    assert infer_record_diagram_type(prompt) == "act"


def test_v1_runtime_summary_policy_distinguishes_raw_public_row_and_smd_target() -> None:
    raw_bd_request = ExpertReviewRequest(
        prompt=(
            "You are an expert reviewer for generated software modeling artifacts under partial public evidence.\n"
            "This is a summary-level task for BD.\n"
            "Public summary row semantics: This published row is a raw public score row.\n"
            "Calibrate the coarse score to that public summary semantics and avoid pseudo-precise element blame."
        ),
        input_text=(
            "The controller has Idle, Monitoring, and Alert modes. It reacts to darkness, presence detection, and WiFi updates."
        ),
        pred_output="""
        @startuml
        [*] --> Idle
        Idle --> Monitoring : darkness
        Monitoring --> Alert : presenceDetected
        Alert --> Monitoring : clear
        Monitoring --> Idle : dayLight
        @enduml
        """,
        ref_output=None,
    )
    average_bd_request = ExpertReviewRequest(
        prompt=raw_bd_request.prompt.replace(
            "raw public score row",
            "average or aggregate quality statistic",
        ),
        input_text=raw_bd_request.input_text,
        pred_output=raw_bd_request.pred_output,
        ref_output=None,
    )
    raw_smd_request = ExpertReviewRequest(
        prompt=raw_bd_request.prompt.replace("for BD", "for SMD"),
        input_text=raw_bd_request.input_text,
        pred_output=raw_bd_request.pred_output,
        ref_output=None,
    )

    raw_bd_result = heuristic_expert_review(raw_bd_request)
    average_bd_result = heuristic_expert_review(average_bd_request)
    raw_smd_result = heuristic_expert_review(raw_smd_request)

    assert raw_bd_result.overall_score > average_bd_result.overall_score
    assert raw_bd_result.overall_score > raw_smd_result.overall_score
    assert raw_bd_result.unsupported_model_elements == []
    assert average_bd_result.unsupported_model_elements == []
    assert raw_smd_result.unsupported_model_elements == []


def test_v1_runtime_protocol_policy_exposes_vv_roles() -> None:
    request = ExpertReviewRequest(
        prompt=(
            "You are an expert reviewer of a human evaluation protocol for software modeling artifacts. "
            "There is no full per-record prediction/reference evidence in this task. "
            "Review what the protocol can validate, which V&V roles it uses, and what claims should remain uncertain."
        ),
        input_text=(
            "Execution uses manual inspection against a reference model, formal verification with a model checker, "
            "simulation on representative scenarios, and testing with TP/FP/FN based F1 reporting."
        ),
        pred_output="",
        ref_output=None,
    )
    result = heuristic_expert_review(request)
    evidence_dimension = next(item for item in result.dimension_results if item.dimension_name == "evidence_discipline")
    assert set(evidence_dimension.metric_payload.get("vv_roles", [])) >= {
        "manual inspection",
        "formal verification",
        "simulation",
        "testing",
    }
    assert any("Recognized V&V roles from evidence" in note for note in result.notes)
    assert result.confidence <= 0.42


def test_runtime_supports_mixed_language_prompt_and_shared_anchor_artifacts() -> None:
    request = ExpertReviewRequest(
        prompt="请审查这个状态机模型，重点关注行为一致性、需求覆盖以及是否有无依据的额外结构。",
        input_text=(
            "R1：当 login 发生时，系统从 Idle 进入 Ready。\n"
            "R2：当 error 发生时，系统进入 Fault。"
        ),
        pred_output="""
        {
          "states": [{"name": "Idle"}, {"name": "Ready"}, {"name": "Fault"}],
          "transitions": [
            {"source": "Idle", "target": "Ready", "event": "login", "guard": "", "action": ""},
            {"source": "Ready", "target": "Fault", "event": "error", "guard": "", "action": ""}
          ]
        }
        """,
        ref_output="""
        {
          "states": [{"name": "Idle"}, {"name": "Ready"}, {"name": "Fault"}],
          "transitions": [
            {"source": "Idle", "target": "Ready", "event": "login", "guard": "", "action": ""},
            {"source": "Ready", "target": "Fault", "event": "error", "guard": "", "action": ""}
          ]
        }
        """,
    )
    result = heuristic_expert_review(request)
    assert result.overall_score >= 0.5
    assert result.unsupported_model_elements == []
    assert {item.requirement_id for item in result.requirement_trace_results} == {"R1", "R2"}


def test_runtime_supports_cjk_model_identifiers_with_english_requirements() -> None:
    request = ExpertReviewRequest(
        prompt="Review the predicted model and focus on requirement coverage and unsupported extras.",
        input_text=(
            "R1: login moves the system from 空闲 to 就绪.\n"
            "R2: 故障 leads the system into 错误."
        ),
        pred_output="""
        {
          "states": [{"name": "空闲"}, {"name": "就绪"}, {"name": "错误"}],
          "transitions": [
            {"source": "空闲", "target": "就绪", "event": "login", "guard": "", "action": ""},
            {"source": "就绪", "target": "错误", "event": "故障", "guard": "", "action": ""}
          ]
        }
        """,
        ref_output=None,
    )
    result = heuristic_expert_review(request)
    assert result.overall_score >= 0.4
    assert result.dimension_results
    assert result.unsupported_model_elements == []


def test_policy_library_prefers_structured_multilingual_metadata() -> None:
    request = ExpertReviewRequest(
        prompt=(
            "Evalue este artefacto resumido. Aunque el texto mencione un promedio, "
            "la metadata estructurada debe gobernar la semántica de revisión."
        ),
        input_text="Resumen público del artefacto.",
        pred_output="score: 0.81",
        ref_output=None,
        metadata={
            "summary_row_type": "raw_score_row",
            "summary_target": "SMD",
            "diagram_type": "act",
        },
    )
    assert infer_summary_row_type(request.prompt, request=request) == "raw_score_row"
    assert infer_summary_target(request.prompt, request=request) == "SMD"
    assert infer_record_diagram_type(request.prompt, request=request) == "act"


def test_record_level_policy_skips_summary_semantic_llm_calls(monkeypatch) -> None:
    request = build_request()
    contract = type(
        "Contract",
        (),
        {
            "task_summary": request.prompt,
            "requested_focus": ["coverage", "equivalence"],
            "domain_knowledge": [],
            "equivalence_rules": [],
            "evidence_rules": [],
            "notes": [],
            "strictness": "balanced",
        },
    )()
    regime = type("Regime", (), {"regime": "record_level", "has_reference": True})()
    input_dossier = build_input_dossier(request)
    pred_dossier = build_parser_dossier("prediction", request.pred_output)
    ref_dossier = build_parser_dossier("reference", request.ref_output)

    def _unexpected(*args, **kwargs):
        raise AssertionError("summary semantic classifier should not run for record-level policy construction")

    monkeypatch.setattr(policy_library_module, "infer_summary_row_type", _unexpected)
    monkeypatch.setattr(policy_library_module, "infer_summary_target", _unexpected)
    monkeypatch.setattr(policy_library_module, "infer_summary_target_axis", _unexpected)
    monkeypatch.setattr(policy_library_module, "infer_record_diagram_type", lambda *args, **kwargs: "stm")

    policy = build_review_policy(
        contract,
        regime,
        request,
        input_dossier,
        pred_dossier,
        ref_dossier,
        llm=object(),
    )
    assert policy["summary_row_type"] == "direct_review"
    assert policy["summary_target"] == "unknown"
    assert policy["record_diagram_type"] == "stm"


def test_review_policy_packet_skips_llm_refinement_for_record_level(monkeypatch) -> None:
    request = build_request()
    contract = type(
        "Contract",
        (),
        {
            "task_summary": request.prompt,
            "requested_focus": ["coverage", "equivalence"],
            "domain_knowledge": [],
            "equivalence_rules": [],
            "evidence_rules": [],
            "notes": [],
            "strictness": "balanced",
        },
    )()
    regime = type(
        "Regime",
        (),
        {
            "regime": "record_level",
            "has_reference": True,
            "pred_observability": "high",
            "ref_observability": "high",
        },
    )()
    input_dossier = build_input_dossier(request)
    pred_dossier = build_parser_dossier("prediction", request.pred_output)
    ref_dossier = build_parser_dossier("reference", request.ref_output)
    notes: list[str] = []

    monkeypatch.setattr(
        review_policy_builder_module,
        "invoke_llm_json",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("record-level policy packet should skip LLM refinement")),
    )
    policy = build_review_policy_packet(
        object(),
        contract,
        regime,
        request,
        input_dossier,
        pred_dossier,
        ref_dossier,
        notes,
    )
    assert policy["record_diagram_type"] == "stm"
    assert any("kept deterministic policy" in note for note in notes)


def test_runtime_scores_component_public_evidence_from_structured_metadata() -> None:
    request = ExpertReviewRequest(
        prompt=(
            "Review the published component evidence for the state-machine artifact. "
            "Focus on the States component only and judge from TP/FP/FN semantics."
        ),
        input_text="状态机需求可以是中文，component label 可以是英文；评审必须按语义而不是按词面进行。",
        pred_output='{"artifact_type":"public_component_audit","component_target":"States","tp":6,"fp":0,"fn":3}',
        ref_output='{"states":[{"name":"Idle"},{"name":"Active"},{"name":"Done"}],"transitions":[]}',
        metadata={
            "review_surface": "summary_public_score",
            "artifact_semantics": "reactive_state_model",
            "component_target": "States",
            "component_source_kind": "xlsx_row",
            "component_public_tp": 6,
            "component_public_fp": 0,
            "component_public_fn": 3,
            "component_pred_total": 6,
            "component_reference_total": 9,
        },
    )
    result = heuristic_expert_review(request)
    assert abs(result.overall_score - 0.8) <= 0.03
    completeness = next(item for item in result.dimension_results if item.dimension_name == "semantic_completeness")
    assert completeness.metric_payload.get("component_review_mode") is True
    assert completeness.metric_payload.get("component_target") == "States"
    assert abs(float(completeness.metric_payload.get("component_public_f1")) - 0.8) <= 1e-6


def test_protocol_policy_detects_vv_roles_under_spanish_prompt_and_mixed_text() -> None:
    request = ExpertReviewRequest(
        prompt=(
            "Eres un revisor experto del protocolo de evaluación humana para artefactos de modelado. "
            "No hay evidencia completa por registro; analiza qué puede validar el protocolo y qué debe seguir incierto."
        ),
        input_text=(
            "执行流程包含 manual inspection、formal verification、simulation，以及 testing with TP/FP/FN based F1 reporting."
        ),
        pred_output="",
        ref_output=None,
    )
    result = heuristic_expert_review(request)
    evidence_dimension = next(item for item in result.dimension_results if item.dimension_name == "evidence_discipline")
    assert set(evidence_dimension.metric_payload.get("vv_roles", [])) >= {
        "manual inspection",
        "formal verification",
        "simulation",
        "testing",
    }


def test_runtime_marks_llm_fallback_only_when_no_stage_returns_usable_llm_output(monkeypatch) -> None:
    class DummyLLM:
        pass

    def _always_fail_transport(*args, **kwargs):
        raise RuntimeError("llm transport unavailable")

    monkeypatch.setattr(llm_helpers_module, "_invoke_transport", _always_fail_transport)
    result = run_expert_review_workflow(
        build_request(),
        llm=DummyLLM(),
        llm_model_name="gpt-test",
        llm_provider="provider-test",
        backend_label="langgraph_multi_agent_v1_llm",
    )
    assert result.used_review_backend == "langgraph_multi_agent_v1_llm_fallback_only"
    assert result.llm_model_name == "gpt-test"
    assert result.llm_provider == "provider-test"
    assert result.llm_usage_summary.llm_configured is True
    assert result.llm_usage_summary.effective_llm_used is False
    assert result.llm_usage_summary.operation_failure_count > 0
    assert any("effectively deterministic" in note for note in result.notes)


def test_arbiter_llm_does_not_override_status_without_explicit_conflict(monkeypatch) -> None:
    monkeypatch.setattr(
        arbiter_module,
        "invoke_llm_json",
        lambda *args, **kwargs: {
            "requirement_overrides": [
                {
                    "requirement_id": "R1",
                    "status": "missing",
                    "reason_text": "hallucinated downgrade",
                    "confidence": 0.2,
                }
            ],
            "equivalence_strength": 0.1,
            "arbitration_notes": "Keep the deterministic status.",
        },
    )
    trace_results = [
        RequirementTraceResult(
            requirement_id="R1",
            requirement_text="R1 text",
            status="matched",
            reason_text="deterministic trace",
            matched_element_ids=["t1"],
            confidence=0.8,
        )
    ]
    updated_trace, updated_report, notes = arbiter_module.arbitrate_with_llm(
        object(),
        input_dossier=type("Input", (), {"requirements": []})(),
        pred_dossier=type("Pred", (), {"summary": "pred"})(),
        ref_dossier=type("Ref", (), {"summary": "ref"})(),
        trace_results=trace_results,
        equivalence_report={"equivalence_strength": 0.6, "trace_conflict_count": 0},
    )
    assert updated_trace[0].status == "matched"
    assert updated_trace[0].reason_text == "deterministic trace"
    assert 0.54 <= updated_report["equivalence_strength"] <= 0.66
    assert any("statuses stayed with deterministic arbitration" in note for note in notes)


def test_missing_evidence_llm_cannot_invent_record_level_flags_without_base_warning(monkeypatch) -> None:
    monkeypatch.setattr(
        missing_evidence_critic_module,
        "invoke_llm_json",
        lambda *args, **kwargs: {
            "confidence_cap": 0.2,
            "warnings": ["invented structural concern"],
            "vv_roles": ["manual inspection", "simulation"],
            "missing_evidence_flags": ["missing transition X -> Y"],
        },
    )
    request = build_request()
    base_report = {
        "confidence_cap": 0.84,
        "warnings": [],
        "confidence": 0.85,
        "allow_element_level_claims": True,
        "allow_requirement_defect_claims": True,
        "missing_evidence_flags": [],
        "vv_roles": ["manual inspection"],
        "issue_taxonomy": [],
        "evidence": [],
    }
    merged = missing_evidence_critic_module.missing_evidence_with_llm(
        object(),
        contract=type("Contract", (), {"task_summary": request.prompt})(),
        regime=type("Regime", (), {"regime": "record_level"})(),
        request=request,
        policy_packet={"base_confidence_cap": 0.84},
        input_dossier=build_input_dossier(request),
        pred_dossier=build_parser_dossier("prediction", request.pred_output),
        ref_dossier=build_parser_dossier("reference", request.ref_output),
        equivalence_report={},
        quality_report={},
        base_report=base_report,
    )
    assert merged["warnings"] == []
    assert merged["missing_evidence_flags"] == []
    assert merged["vv_roles"] == ["manual inspection", "simulation"]
    assert round(merged["confidence_cap"], 6) >= 0.81
