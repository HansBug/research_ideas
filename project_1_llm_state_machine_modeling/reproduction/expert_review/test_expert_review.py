from __future__ import annotations

from .expert_review_agent import heuristic_expert_review
from .expert_review_schema import ExpertReviewRequest


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
    assert result.used_review_backend == "heuristic"
    assert result.overall_score >= 0.0
    assert result.dimension_results
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
    assert result.used_review_backend == "heuristic"
    assert result.unsupported_model_elements == []
    assert any("No reference output was provided" in item.reason_text for item in result.dimension_results)


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
    assert result.used_review_backend == "heuristic"
    assert result.dimension_results
    assert result.requirement_trace_results
    assert result.overall_reason_text
