from __future__ import annotations

import json
from dataclasses import asdict

import pytest

from method.llm_stages import (
    LLMStageConfig,
    MockLLMProvider,
    run_sl1_initial_modeling_llm,
    run_sl5_scenario_generation_llm,
    run_sl7_model_review_llm,
    run_sl9_repair_llm,
    run_sl10_repair_review_llm,
    run_sl10b_delta_review_llm,
)
from method.schema import FixPlan, FixRequest, FixRequestBatch, FixRequestDecision, GroundedElement, GroundingMap
from method.stages.ids import StageId, StageStatus


BASE_DSL = """
state Root {
    state Idle;
    [*] -> Idle;
}
"""


def _cfg(**kwargs) -> LLMStageConfig:
    return LLMStageConfig(provider_mode="mock", model="mock-model", **kwargs)


def _grounding() -> GroundingMap:
    return GroundingMap(
        elements=[
            GroundedElement(
                element_id="state:Root.Idle",
                element_kind="state",
                element_ref="Root.Idle",
                source_stage="SL-1",
                evidence_text="The controller starts in Idle.",
                requiredness="required",
            )
        ],
        source_summary={"nl": "starts in Idle"},
    )



def _sl7_fail_raw() -> str:
    return json.dumps(
        {
            "decision": "fail",
            "risk_level": "major",
            "findings": [
                {
                    "category": "nl_fidelity",
                    "severity": "major",
                    "summary": "Active state is missing.",
                    "evidence": ["NL requires Active"],
                }
            ],
            "blocking_findings": [
                {
                    "category": "nl_fidelity",
                    "severity": "major",
                    "summary": "Active state is missing.",
                    "evidence": ["NL requires Active"],
                }
            ],
        },
        ensure_ascii=False,
    )

def _fix_plan() -> FixPlan:
    return FixPlan(
        target="design",
        source_stage=StageId.SD_4_DESIGN.value,
        source_feedback_id="W_DEADLOCK_LEAF:Root.Idle",
        severity="blocking_warning",
        diagnostic_ids=["W_DEADLOCK_LEAF"],
        problem_summary="Idle has no safe outgoing recovery transition.",
        suggested_fix_hints=[{"suggested_fix": "add an Idle -> Active transition"}],
        required_preserve_element_ids=["state:Root.Idle"],
    )


def test_pr_b2_sl1_retries_schema_invalid_and_records_interaction() -> None:
    provider = MockLLMProvider(
        responses=[
            "not json",
            json.dumps(
                {
                    "candidate_dsl": BASE_DSL,
                    "grounding_seeds": [asdict(_grounding().elements[0])],
                    "assumptions": [],
                },
                ensure_ascii=False,
            ),
        ]
    )

    result = run_sl1_initial_modeling_llm(
        nl="The controller starts in Idle.",
        spec_json={"states": ["Idle"]},
        config=_cfg(max_retries=2, seed=7),
        provider=provider,
    )

    assert result.ok is True
    assert result.stage_meta.stage_id == StageId.SL_1_INITIAL_MODELING.value
    assert result.stage_meta.status == StageStatus.OK
    assert result.parsed_output["candidate_dsl"] == BASE_DSL
    assert result.interaction["stage_id"] == StageId.SL_1_INITIAL_MODELING.value
    assert result.interaction["retry_count"] == 1
    assert [attempt["status"] for attempt in result.interaction["attempts"]] == ["schema_invalid", "ok"]
    assert result.interaction["schema_validation_ok"] is True
    assert result.interaction["usage"]["total_tokens"] == 2
    assert provider.calls[0]["response_format"] == {"type": "json_object"}
    assert provider.calls[0]["seed"] == 7


def test_pr_b2_sl5_retries_empty_output_and_returns_scenarios() -> None:
    provider = MockLLMProvider(
        responses=[
            "",
            json.dumps(
                {
                    "scenarios": [
                        {
                            "name": "start_idle",
                            "description": "initial checkpoint",
                            "initial_state": "Root.Idle",
                            "steps": [{"name": "check", "expected_state": "Root.Idle"}],
                        }
                    ]
                },
                ensure_ascii=False,
            ),
        ]
    )

    result = run_sl5_scenario_generation_llm(
        nl="The controller starts in Idle.",
        current_dsl=BASE_DSL,
        inspect_json={"states": [{"path": "Root.Idle"}]},
        design_summary={"ok": True},
        grounding_map=_grounding(),
        coverage_directive="cover initial state",
        config=_cfg(max_retries=1),
        provider=provider,
    )

    assert result.ok is True
    assert result.stage_meta.stage_id == StageId.SL_5_SCENARIO_GENERATION.value
    assert [attempt["status"] for attempt in result.interaction["attempts"]] == ["empty_output", "ok"]
    assert result.parsed_output[0].name == "start_idle"
    assert result.interaction["parsed_output"]["scenarios"][0]["name"] == "start_idle"


def test_pr_b2_sl5_retries_malformed_scenario_schema_instead_of_silently_downgrading() -> None:
    malformed = json.dumps(
        {
            "scenarios": [
                "not-an-object",
                {"name": "bad-steps", "steps": "not-list"},
            ]
        },
        ensure_ascii=False,
    )
    valid = json.dumps(
        {
            "scenarios": [
                {
                    "name": "valid-after-retry",
                    "steps": [{"name": "check", "expected_state": "Root.Idle"}],
                }
            ]
        },
        ensure_ascii=False,
    )
    provider = MockLLMProvider(responses=[malformed, valid])

    result = run_sl5_scenario_generation_llm(
        nl="The controller starts in Idle.",
        current_dsl=BASE_DSL,
        config=_cfg(max_retries=1),
        provider=provider,
    )

    assert result.ok is True
    assert [attempt["status"] for attempt in result.interaction["attempts"]] == ["schema_invalid", "ok"]
    assert result.parsed_output[0].name == "valid-after-retry"


def test_pr_b2_sl9_repair_records_full_context_and_treats_suggested_fix_as_hint() -> None:
    candidate = """
state Root {
    state Idle;
    state Active;
    [*] -> Idle;
    Idle -> Active;
}
"""
    provider = MockLLMProvider(responses=[candidate])

    result = run_sl9_repair_llm(
        nl="Idle must be able to move to Active.",
        current_dsl=BASE_DSL,
        fix_plan=_fix_plan(),
        grounding_map=_grounding(),
        selected_diagnostics=[{"code": "W_DEADLOCK_LEAF", "message": "Idle deadlocks"}],
        preserve_list=["state:Root.Idle"],
        scenario_summary={"scenario_set_id": "scenario-1", "passed": 1},
        repair_target="design",
        config=_cfg(max_retries=1),
        provider=provider,
    )

    prompt_text = "\n".join(message["content"] for message in provider.calls[0]["messages"])
    assert result.ok is True
    assert result.parsed_output["candidate_dsl"] == candidate.strip()
    assert "selected_diagnostics" in prompt_text
    assert "preserve_list" in prompt_text
    assert "scenario_summary" in prompt_text
    assert "hint, not a command" in prompt_text
    assert result.interaction["parsed_output"]["candidate_dsl"] == candidate.strip()
    assert result.interaction["attempts"][0]["status"] == "ok"




def test_pr_b2_sl9_normalizes_fenced_dsl_before_recording_candidate() -> None:
    fenced_candidate = """```pyfcstm
state Root {
    state Idle;
    state Active;
    [*] -> Idle;
    Idle -> Active;
}
```"""
    provider = MockLLMProvider(responses=[fenced_candidate])

    result = run_sl9_repair_llm(
        nl="Idle must be able to move to Active.",
        current_dsl=BASE_DSL,
        fix_plan=_fix_plan(),
        grounding_map=_grounding(),
        selected_diagnostics=[{"code": "W_DEADLOCK_LEAF"}],
        preserve_list=["state:Root.Idle"],
        scenario_summary={"scenario_set_id": "scenario-1"},
        repair_target="design",
        config=_cfg(),
        provider=provider,
    )

    assert result.ok is True
    assert result.parsed_output["candidate_dsl"].startswith("state Root")
    assert not result.parsed_output["candidate_dsl"].startswith("```")
    assert result.interaction["parsed_output"]["candidate_dsl"] == result.parsed_output["candidate_dsl"]

def test_pr_b2_sl7_and_sl10b_real_stage_units_return_typed_feedback() -> None:
    sl7_provider = MockLLMProvider(
        responses=[
            json.dumps(
                {
                    "decision": "fail",
                    "risk_level": "major",
                    "findings": [
                        {
                            "category": "nl_fidelity",
                            "severity": "major",
                            "summary": "Active state is missing.",
                            "evidence": ["NL requires Active"],
                        }
                    ],
                    "blocking_findings": [
                        {
                            "category": "nl_fidelity",
                            "severity": "major",
                            "summary": "Active state is missing.",
                            "evidence": ["NL requires Active"],
                        }
                    ],
                },
                ensure_ascii=False,
            )
        ]
    )
    sl7 = run_sl7_model_review_llm(
        nl="Idle must be able to move to Active.",
        current_dsl=BASE_DSL,
        grounding_map=_grounding(),
        review_policy={"mode": "blocking_major_only"},
        config=_cfg(),
        provider=sl7_provider,
    )

    assert sl7.feedback.decision == "fail"
    assert sl7.feedback.review_meta is not None
    assert sl7.feedback.review_meta.provider == "mock"
    assert sl7.interaction["parsed_schema_version"] == "ModelReviewFeedback.v1"

    sl10b_provider = MockLLMProvider(
        responses=[
            json.dumps(
                {
                    "decision": "reject",
                    "drift_risk": "major",
                    "drift_evidence": [{"summary": "candidate removes Idle"}],
                    "required_revision": ["preserve Idle"],
                },
                ensure_ascii=False,
            )
        ]
    )
    sl10b = run_sl10b_delta_review_llm(
        nl="Idle must remain available.",
        grounding_map=_grounding(),
        old_dsl=BASE_DSL,
        candidate_dsl="state Root { state Active; [*] -> Active; }",
        fix_plan=_fix_plan(),
        diff_summary={"removed": ["Root.Idle"]},
        config=_cfg(),
        provider=sl10b_provider,
    )

    assert sl10b.feedback.ok is False
    assert sl10b.feedback.drift_risk == "major"
    assert sl10b.feedback.delta_review["decision"] == "reject"
    assert sl10b.feedback.review_meta is not None
    assert sl10b.feedback.review_meta.schema_validation_ok is True
    assert sl10b.stage_meta.stage_id == StageId.SL_10B_DELTA_REVIEW.value


def test_pr_b2_llm_stage_records_redact_prompt_raw_and_attempt_secrets() -> None:
    secret = "sk-test-1234567890abcdef"
    provider = MockLLMProvider(
        responses=[
            json.dumps(
                {
                    "candidate_dsl": f"state Root {{ state Idle; }} // {secret}",
                    "grounding_seeds": [],
                    "assumptions": ["saw github_pat_deadbeef12345678"],
                },
                ensure_ascii=False,
            )
        ]
    )

    result = run_sl1_initial_modeling_llm(
        nl=f"Requirement accidentally includes {secret}",
        config=_cfg(),
        provider=provider,
    )
    record_text = json.dumps(result.interaction, ensure_ascii=False)

    assert secret not in record_text
    assert "github_pat_deadbeef12345678" not in record_text
    assert "<redacted:" in record_text
    assert result.redaction_report
    assert {item["reason"] for item in result.redaction_report} >= {"openai_api_key", "github_pat"}


def test_pr_b2_llm_stage_redacts_env_style_secrets_without_redacting_usage_tokens() -> None:
    secret = "LLM_API_KEY=proxy-secret-1234567890abcdef"
    quoted_secret = 'OPENAI_API_KEY="quoted-secret-1234567890abcdef"'
    provider = MockLLMProvider(
        responses=[
            json.dumps(
                {
                    "candidate_dsl": f"state Root {{ state Idle; }} // {secret} // {quoted_secret}",
                    "grounding_seeds": [],
                },
                ensure_ascii=False,
            )
        ]
    )

    result = run_sl1_initial_modeling_llm(
        nl=f"Requirement accidentally includes env lines {secret} and {quoted_secret}",
        config=_cfg(),
        provider=provider,
    )
    record_text = json.dumps(result.interaction, ensure_ascii=False)

    assert secret not in record_text
    assert "proxy-secret-1234567890abcdef" not in record_text
    assert quoted_secret not in record_text
    assert "quoted-secret-1234567890abcdef" not in record_text
    assert "env_secret_assignment" in record_text
    assert result.interaction["usage"]["total_tokens"] == 2
    assert result.interaction["attempts"][0]["usage"]["prompt_tokens"] == 1
    assert "env_secret_assignment" in {item["reason"] for item in result.redaction_report}


def test_pr_b2_provider_errors_retry_as_llm_layer_without_deterministic_retry() -> None:
    provider = MockLLMProvider(errors=[RuntimeError("network down")], responses=[])

    result = run_sl7_model_review_llm(
        nl="Review should fail closed after provider noise budget is exhausted.",
        current_dsl=BASE_DSL,
        grounding_map=_grounding(),
        config=_cfg(max_retries=0),
        provider=provider,
    )

    assert result.ok is False
    assert result.stage_meta.status == StageStatus.ERROR
    assert result.interaction["schema_validation_ok"] is False
    assert result.interaction["retry_error"]["error_kind"] == "provider_error"
    assert "terminal_verdict_hint" not in result.interaction
    assert "verdict" not in result.interaction["retry_error"]
    assert len(result.interaction["attempts"]) == 1
    assert provider.call_count == 1


def test_pr_b2_schema_retry_exhaustion_returns_error_kind_without_sc12_verdict() -> None:
    provider = MockLLMProvider(responses=["not json"])

    result = run_sl1_initial_modeling_llm(
        nl="Malformed JSON should remain an LLM-layer schema failure.",
        config=_cfg(max_retries=0),
        provider=provider,
    )

    assert result.ok is False
    assert result.stage_meta.status == StageStatus.ERROR
    assert result.interaction["retry_error"]["error_kind"] == "schema_invalid"
    assert result.interaction["schema_validation_error"]
    assert [attempt["status"] for attempt in result.interaction["attempts"]] == ["schema_invalid"]
    assert "terminal_verdict_hint" not in result.interaction
    assert "verdict" not in result.interaction["retry_error"]


def test_pr_b2_empty_output_retry_exhaustion_returns_error_kind_without_sc12_verdict() -> None:
    provider = MockLLMProvider(responses=[""])

    result = run_sl5_scenario_generation_llm(
        nl="Empty output should be reported to PR-B1/PR-C as invalid LLM output.",
        current_dsl=BASE_DSL,
        config=_cfg(max_retries=0),
        provider=provider,
    )

    assert result.ok is False
    assert result.stage_meta.status == StageStatus.ERROR
    assert result.interaction["retry_error"]["error_kind"] == "empty_output"
    assert result.interaction["schema_validation_error"] == "empty LLM output"
    assert [attempt["status"] for attempt in result.interaction["attempts"]] == ["empty_output"]
    assert "terminal_verdict_hint" not in result.interaction
    assert "verdict" not in result.interaction["retry_error"]


def test_pr_b2_sl7_audit_only_policy_records_but_does_not_block() -> None:
    provider = MockLLMProvider(
        responses=[
            json.dumps(
                {
                    "decision": "fail",
                    "risk_level": "major",
                    "findings": [
                        {
                            "category": "nl_fidelity",
                            "severity": "major",
                            "summary": "Audit-only finding should not block this condition.",
                            "evidence": ["policy ablation"],
                        }
                    ],
                    "blocking_findings": [
                        {
                            "category": "nl_fidelity",
                            "severity": "major",
                            "summary": "Audit-only finding should not block this condition.",
                            "evidence": ["policy ablation"],
                        }
                    ],
                },
                ensure_ascii=False,
            )
        ]
    )

    result = run_sl7_model_review_llm(
        nl="Audit-only review should be recorded for ablation.",
        current_dsl=BASE_DSL,
        grounding_map=_grounding(),
        review_policy={"mode": "audit_only"},
        config=_cfg(),
        provider=provider,
    )

    assert result.stage_meta.status == StageStatus.OK
    assert result.feedback.decision == "fail"
    assert result.feedback.ok is True
    assert result.feedback.review_meta.failure_policy == "audit_only"


def test_pr_b2_sl7_blocking_major_policy_blocks_major_findings() -> None:
    provider = MockLLMProvider(responses=[_sl7_fail_raw()])

    result = run_sl7_model_review_llm(
        nl="Blocking review should reject major NL drift.",
        current_dsl=BASE_DSL,
        grounding_map=_grounding(),
        review_policy={"mode": "blocking_major_only"},
        config=_cfg(),
        provider=provider,
    )

    assert result.stage_meta.status == StageStatus.OK
    assert result.feedback.decision == "fail"
    assert result.feedback.ok is False
    assert result.feedback.review_meta.failure_policy == "fail_closed"


def test_pr_b2_sl10b_audit_policy_records_reject_without_blocking_accept_candidate_gate() -> None:
    provider = MockLLMProvider(
        responses=[
            json.dumps(
                {
                    "decision": "reject",
                    "drift_risk": "major",
                    "drift_evidence": [{"summary": "candidate drift recorded for audit"}],
                    "required_revision": ["would revise under blocking policy"],
                },
                ensure_ascii=False,
            )
        ]
    )

    result = run_sl10b_delta_review_llm(
        nl="Delta review audit-only ablation.",
        grounding_map=_grounding(),
        old_dsl=BASE_DSL,
        candidate_dsl="state Root { state Idle; [*] -> Idle; }",
        fix_plan=_fix_plan(),
        delta_review_policy={"mode": "audit_only"},
        config=_cfg(),
        provider=provider,
    )

    assert result.stage_meta.status == StageStatus.OK
    assert result.feedback.delta_review["decision"] == "reject"
    assert result.feedback.ok is True
    assert result.feedback.regression_detected is False
    assert result.feedback.review_meta.failure_policy == "audit_only"


def test_pr_b2_sl10_pass_with_unresolved_regression_is_downgraded_to_rework() -> None:
    provider = MockLLMProvider(
        responses=[
            json.dumps(
                {
                    "decision": "pass",
                    "target_resolved": False,
                    "regression_detected": True,
                    "drift_risk": "major",
                    "evidence": [{"summary": "contradictory pass"}],
                    "rework_instructions": [],
                },
                ensure_ascii=False,
            )
        ]
    )
    batch = FixRequestBatch(
        batch_id="b1",
        iteration=0,
        source="sim",
        source_stage=StageId.SD_6_SIM.value,
        requests=[
            FixRequest(
                request_id="r1",
                target="sim",
                source_stage=StageId.SD_6_SIM.value,
                source_feedback_id="sim",
                severity="sim_fail",
                hard_block=True,
            )
        ],
    )

    result = run_sl10_repair_review_llm(
        nl="The model must satisfy the scenario.",
        grounding_map=None,
        old_dsl=BASE_DSL,
        candidate_dsl=BASE_DSL,
        request_batch=batch,
        sl9_decisions=[FixRequestDecision(request_id="r1", decision="accept")],
        local_check_evidence={
            "repair_review_feedback": {
                "ok": False,
                "target_resolved": False,
                "regression_detected": True,
                "drift_risk": "major",
            }
        },
        config=_cfg(),
        provider=provider,
    )

    assert result.ok is True  # schema-level success
    assert result.feedback.ok is False
    assert result.feedback.decision == "rework"
    assert result.feedback.target_resolved is False
    assert result.feedback.regression_detected is True
    assert result.feedback.drift_risk == "major"
    assert any("downgraded" in item for item in result.feedback.rework_instructions)


def test_pr_b2_llm_stage_attempts_emit_progress_and_elapsed(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setenv("AGENT_LOOP_PROGRESS_LOG", "true")
    provider = MockLLMProvider(responses=[_sl7_fail_raw()])

    result = run_sl7_model_review_llm(
        nl="Blocking review should reject major NL drift.",
        current_dsl=BASE_DSL,
        grounding_map=_grounding(),
        review_policy={"mode": "blocking_major_only"},
        config=_cfg(),
        provider=provider,
    )

    captured = capsys.readouterr().out
    assert result.ok is True
    assert "[agent-loop][SL-7] attempt_start" in captured
    assert "[agent-loop][SL-7] attempt_schema_ok" in captured
    attempt = result.interaction["attempts"][0]
    assert attempt["elapsed_seconds"] >= 0
