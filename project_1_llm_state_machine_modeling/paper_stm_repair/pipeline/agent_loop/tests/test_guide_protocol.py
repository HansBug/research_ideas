from __future__ import annotations

import json
from pathlib import Path

import pytest

from paper_stm_repair_loop.agents.discover import _parser, _validate_guide_protocol
from paper_stm_repair_loop.inputs import load_pair, prepare_run_dir
from paper_stm_repair_loop.schemas import DiscoverSubmission
from paper_stm_repair_loop.tools.guide_access import GuideAccessState


def _submission(check_kind: str) -> DiscoverSubmission:
    executable_spec = (
        {"kind": "simple_state", "target_label": "Idle", "bound": 0}
        if check_kind == "property"
        else {"event_labels": ["Go"], "precondition_state_label": "Idle"}
    )
    return DiscoverSubmission.model_validate(
        {
            "check_drafts": [
                {
                    "check_origin": "nl_grounded_behavioral_issue",
                    "check_id": "draft-1",
                    "check_kind": check_kind,
                    "statement": "A bounded proposition.",
                    "expected_outcome": {"property_satisfied": True},
                    "source_basis": [],
                    "nl_basis": [{"quote": "A requirement.", "role": "requirement"}],
                    "executable_spec": executable_spec,
                    "binding_refs": [],
                    "required": True,
                }
            ],
            "no_issue_found": True,
            "root_nodes": [],
            "rejected_propositions": [],
            "rationale": "No root is published by this protocol-only fixture.",
        }
    )


def _mark(state: GuideAccessState, kind: str) -> None:
    state.mark_read(
        kind,
        {
            "resource_name": f"{kind}.md",
            "sha256": kind * 8,
            "pyfcstm_version": "0.6.0",
        },
    )


def test_fcstm_guide_must_precede_first_model_tool_attempt():
    state = GuideAccessState()
    state.record_attempt("read_task")
    _mark(state, "fcstm")
    with pytest.raises(ValueError, match="fcstm guide-first protocol violated"):
        _validate_guide_protocol(state, _submission("scenario"))


def test_fcstm_guide_must_be_the_first_business_tool_call():
    state = GuideAccessState()
    _mark(state, "fbmcq")
    _mark(state, "fcstm")
    state.record_attempt("read_task")
    with pytest.raises(ValueError, match="first business tool call"):
        _validate_guide_protocol(state, _submission("scenario"))


def test_scenario_only_submission_requires_fcstm_but_not_fbmcq_guide():
    state = GuideAccessState()
    _mark(state, "fcstm")
    state.record_attempt("read_task")
    state.record_attempt("evaluate_checks", property_batch=False)
    _validate_guide_protocol(state, _submission("scenario"))


def test_submission_requires_read_task_after_fcstm_guide():
    state = GuideAccessState()
    _mark(state, "fcstm")
    state.record_attempt("evaluate_checks", property_batch=False)
    with pytest.raises(ValueError, match="read_task was not called"):
        _validate_guide_protocol(state, _submission("scenario"))


def test_property_submission_requires_fbmcq_guide_before_property_attempt():
    state = GuideAccessState()
    _mark(state, "fcstm")
    state.record_attempt("read_task")
    state.record_attempt("evaluate_checks", property_batch=True)
    _mark(state, "fbmcq")
    with pytest.raises(ValueError, match="fbmcq guide-first protocol violated"):
        _validate_guide_protocol(state, _submission("property"))


def test_property_submission_accepts_both_guides_in_order():
    state = GuideAccessState()
    _mark(state, "fcstm")
    state.record_attempt("read_task")
    _mark(state, "fbmcq")
    state.record_attempt("evaluate_checks", property_batch=True)
    _validate_guide_protocol(state, _submission("property"))


def test_cli_limits_default_to_none_and_can_be_explicit():
    parser = _parser()
    defaults = parser.parse_args(
        ["--pair-id", "p", "--output-dir", "/tmp/out"]
    )
    assert defaults.max_model_calls is None
    assert defaults.max_tool_calls is None
    assert defaults.max_turns is None
    assert defaults.max_seconds is None

    explicit = parser.parse_args(
        [
            "--pair-id",
            "p",
            "--output-dir",
            "/tmp/out",
            "--max-model-calls",
            "100",
            "--max-tool-calls",
            "200",
            "--max-turns",
            "150",
            "--max-seconds",
            "3600",
        ]
    )
    assert explicit.max_model_calls == 100
    assert explicit.max_tool_calls == 200
    assert explicit.max_turns == 150
    assert explicit.max_seconds == 3600.0


@pytest.mark.parametrize(
    ("option", "value"),
    [
        ("--max-model-calls", "0"),
        ("--max-tool-calls", "-1"),
        ("--max-turns", "0"),
        ("--max-seconds", "0"),
        ("--max-seconds", "nan"),
        ("--max-seconds", "inf"),
    ],
)
def test_cli_rejects_nonpositive_or_nonfinite_limits(option: str, value: str):
    with pytest.raises(SystemExit, match="2"):
        _parser().parse_args(
            ["--pair-id", "p", "--output-dir", "/tmp/out", option, value]
        )


def test_prepare_run_dir_persists_only_explicit_limits(tmp_path: Path):
    case = load_pair("llms_emp_stm_results_0000")
    run_dir = tmp_path / "run"
    prepare_run_dir(
        run_dir,
        case,
        profile="gpt-5.5",
        content_language="zh-CN",
        renderer="quiet",
        agent_limits={"model_calls": 100, "seconds": 3600.0},
    )
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["agent_limits"] == {"model_calls": 100, "seconds": 3600.0}
    provenance = manifest["code_provenance"]
    assert provenance["status"] == "completed"
    assert len(provenance["git_commit"]) == 40
    assert isinstance(provenance["tracked_worktree_dirty"], bool)
    assert provenance["untracked_run_outputs_excluded"] is True
