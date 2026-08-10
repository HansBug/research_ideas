from __future__ import annotations

import json
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from paper_stm_repair_loop.eval_env.exceptions import UnsupportedEvidence
from paper_stm_repair_loop.eval_env.fbmcq import FBMCQAPI
from paper_stm_repair_loop.eval_env.runtime import EvalEnvironment
from paper_stm_repair_loop.inputs import PreparedCase
from paper_stm_repair_loop.records import RecordStore
from paper_stm_repair_loop.renderer import render_discover
from paper_stm_repair_loop.schemas.assertions import EvalAssertResult
from paper_stm_repair_loop.tools.coverage_registry import (
    CoverageRegistry,
    DirectEvalRuntime,
)


MODEL = """state Root {
    event go;
    state Idle;
    state Done;
    [*] -> Idle;
    Idle -> Done : go;
}
"""


def _stable_report(kind: str = "reach", bound: int = 3, *, holds: bool = True) -> str:
    return json.dumps(
        {
            "result": {"status": "sat", "property_satisfied": holds},
            "property": {"kind": kind, "bound": bound, "polarity": "exists"},
            "replay": {"ok": True},
        }
    )


def test_fbmcq_exposes_strong_bound_origin_and_assumption_metadata():
    seen_kwargs: dict[str, object] = {}

    def runner(*_args, **kwargs):
        seen_kwargs.update(kwargs)
        return _stable_report(), 0

    obs = FBMCQAPI(MODEL, bmc_runner=runner).fbmcq(
        'check reach <= 3: active("Root.Done");'
    )

    assert obs.formal_property_kind == "reach"
    assert obs.bound == 3
    assert obs.formal_bound == 3
    assert obs.controller_max_bound is None
    assert obs.query_origin == "exact_agent_query"
    assert obs.assumption_basis == ()
    assert obs.holds is True
    assert set(obs.limitations) == {
        "finite_horizon_only",
        "exact_query_and_assumptions_only",
        "does_not_establish_unbounded_correctness",
    }
    assert seen_kwargs["json_output"] is True
    assert "timeout_ms" not in seen_kwargs
    assert "max_bound" not in seen_kwargs


def test_fbmcq_cross_validates_parsed_query_against_structured_report():
    def mismatched_runner(*_args, **_kwargs):
        return _stable_report(kind="invariant", bound=4), 0

    with pytest.raises(UnsupportedEvidence) as excinfo:
        FBMCQAPI(MODEL, bmc_runner=mismatched_runner).fbmcq(
            'check reach <= 3: active("Root.Done");'
        )

    metadata = excinfo.value.metadata
    assert metadata["inconclusive_kind"] == "structured_report_mismatch"
    assert metadata["formal_property_kind"] == "reach"
    assert metadata["formal_bound"] == 3
    assert metadata["reported_property_kind"] == "invariant"
    assert metadata["reported_bound"] == 4


def test_fbmcq_explicit_controller_max_bound_is_enforced_without_hidden_default():
    captured: dict[str, object] = {}

    def runner(*_args, **kwargs):
        captured.update(kwargs)
        return _stable_report(bound=99), 0

    obs = FBMCQAPI(MODEL, max_bound=None, bmc_runner=runner).fbmcq(
        'check reach <= 99: active("Root.Done");'
    )
    assert obs.formal_bound == 99
    assert obs.controller_max_bound is None
    assert "max_bound" not in captured

    with pytest.raises(UnsupportedEvidence) as excinfo:
        FBMCQAPI(MODEL, max_bound=8, bmc_runner=runner).fbmcq(
            'check reach <= 99: active("Root.Done");'
        )
    assert excinfo.value.metadata["inconclusive_kind"] == "analysis_bound_exceeded"
    assert excinfo.value.metadata["formal_bound"] == 99
    assert excinfo.value.metadata["controller_max_bound"] == 8


def test_fbmcq_failure_modes_carry_structured_inconclusive_metadata():
    with pytest.raises(UnsupportedEvidence) as malformed:
        FBMCQAPI(MODEL).fbmcq("not a query")
    assert malformed.value.metadata["inconclusive_kind"] == "malformed_query"

    def replay_bad(*_args, **_kwargs):
        return json.dumps(
            {
                "result": {"status": "sat", "property_satisfied": True},
                "property": {"kind": "reach", "bound": 3},
                "replay": {"ok": False, "reason": "different trace"},
            }
        ), 0

    with pytest.raises(UnsupportedEvidence) as replay:
        FBMCQAPI(MODEL, bmc_runner=replay_bad).fbmcq(
            'check reach <= 3: active("Root.Done");'
        )
    assert replay.value.metadata["inconclusive_kind"] == "replay_mismatch"
    assert replay.value.metadata["replay_status"] == "mismatch"

    def budget_incomplete(*_args, **_kwargs):
        return json.dumps(
            {
                "result": {
                    "status": "unknown",
                    "property_satisfied": None,
                    "incomplete": True,
                    "incomplete_status": "budget_exhausted",
                },
                "property": {"kind": "reach", "bound": 3},
                "replay": None,
            }
        ), 0

    with pytest.raises(UnsupportedEvidence) as budget:
        FBMCQAPI(MODEL, bmc_runner=budget_incomplete).fbmcq(
            'check reach <= 3: active("Root.Done");'
        )
    assert budget.value.metadata["inconclusive_kind"] == "budget_or_incomplete"
    assert budget.value.metadata["incomplete_status"] == "budget_exhausted"


def test_eval_assert_result_schema_accepts_typed_fbmcq_metadata():
    payload = {
        "execution_status": "inconclusive",
        "assertion_chain_id": "ASSERT-001",
        "assertion_version_id": "ASSERT-001@v1",
        "assert_sha256": "abc",
        "root_node_id": "ROOT-001",
        "coverage_unit_id": "CU-001",
        "prepared_record_id": "LOCAL-REC-001",
        "match_status": "inconclusive",
        "model_sha256": "model-sha",
        "dependency_provenance": {},
        "eval_vars_hash_before": "before",
        "eval_vars_hash_after": "after",
        "function_registry_hash": "registry",
        "reason": "Timeout while evaluating the exact bounded property.",
        "reason_context": {},
        "formal_property_kind": "reach",
        "formal_bound": 3,
        "formal_bound_origin": "analysis_bound",
        "formal_assumption_basis_ids": [],
    }
    validated = EvalAssertResult.model_validate(payload)
    assert validated.formal_property_kind == "reach"
    assert validated.formal_bound == 3

    payload["formal_property_kind"] = "invented_kind"
    with pytest.raises(ValidationError):
        EvalAssertResult.model_validate(payload)


def _formal_plan(*, declared_bound: int = 3, origin: str = "analysis_bound") -> dict:
    query = 'check reach <= 3: active("Root.Done");'
    return {
        "segment_dispositions": [],
        "fact_dispositions": [],
        "coverage_units": [
            {
                "coverage_unit_id": "CU-1",
                "unit_kind": "behavior_obligation",
                "segment_ids": ["SEG-1"],
                "source_fact_ids": [],
                "requirement_ids": [],
                "dimensions": ["behavior"],
                "statement": "Done is reachable within the finite analysis horizon.",
                "rationale": "One bounded proposition.",
            }
        ],
        "proposition_roots": [
            {
                "node_id": "ROOT-1",
                "coverage_unit_id": "CU-1",
                "statement": "Done is reachable.",
                "model_element_refs": [],
                "rationale": "One positive Root.",
            }
        ],
        "logical_assertions": [
            {
                "assertion_chain_id": "ASSERT-1",
                "root_node_id": "ROOT-1",
                "coverage_unit_id": "CU-1",
                "required": True,
                "assert": f"fbmcq({query!r}).holds is True",
                "basis_ids": ["SEG-1"],
                "obligation_signature": "done-reach",
                "required_function_families": ["formal"],
                "evidence_scope": {
                    "semantic_profile": "bounded_fcstm_v1",
                    "max_steps": 3,
                    "max_time": None,
                    "abstraction": "bounded_transition_system",
                    "claim_strength": "finite_reachability",
                },
                "rationale": "Finite analysis horizon 3 is sufficient for this direct reach proposition.",
                "formal_property_kind": "reach",
                "formal_bound": declared_bound,
                "formal_bound_origin": origin,
                "formal_assumption_basis_ids": [],
            }
        ],
    }


def test_registry_reparses_exact_fbmcq_and_rejects_declared_bound_mismatch():
    accepted_registry = CoverageRegistry(
        input_segment_ids=["SEG-1"],
        fbmcq_guide_read=lambda: True,
    )
    accepted = accepted_registry.register_plan(
        _formal_plan(), reason="Register exact formal metadata."
    )
    assert accepted["accepted"] is True
    latest = accepted_registry.latest_versions()[0]
    assert latest.formal_property_kind == "reach"
    assert latest.formal_bound == 3
    assert latest.formal_bound_origin == "analysis_bound"

    rejected_registry = CoverageRegistry(
        input_segment_ids=["SEG-1"],
        fbmcq_guide_read=lambda: True,
    )
    rejected = rejected_registry.register_plan(
        _formal_plan(declared_bound=4),
        reason="Reject mismatched formal metadata.",
    )
    assert rejected["accepted"] is False
    assert any(
        error.startswith("formal_bound_mismatch:ASSERT-1")
        for error in rejected["errors"]
    )


def test_completed_fbmcq_record_preserves_bounded_limitations_at_every_layer(
    tmp_path,
):
    def runner(*_args, **_kwargs):
        return _stable_report(), 0

    store = RecordStore(tmp_path)
    environment = EvalEnvironment(model_text=MODEL, bmc_runner=runner)
    registry = CoverageRegistry(
        input_segment_ids=["SEG-1"],
        fbmcq_guide_read=lambda: True,
        eval_runtime=DirectEvalRuntime(environment),
        record_sink=lambda record_type, payload: store.append(record_type, payload),
        evidence_context={
            "check": {
                "check_record_id": "REC-CHECK",
                "check_result_sha256": "check-sha",
                "model_sha256": "model-sha",
                "tool_hash": "tool-hash",
                "tool_schema_hash": "tool-schema-sha",
            },
            "policy": {
                "policy_hash": "policy-sha",
                "evidence_policy_fingerprint": "policy-sha",
            },
        },
    )
    plan = _formal_plan()
    assert registry.register_plan(plan, reason="Register exact formal evidence.")[
        "accepted"
    ]

    evaluated = registry.eval_assert(
        plan["logical_assertions"][0]["assert"],
        reason="Execute exact bounded formal evidence.",
    )

    required = {
        "finite_horizon_only",
        "exact_query_and_assumptions_only",
        "does_not_establish_unbounded_correctness",
    }
    assert evaluated["match_status"] == "matches"
    assert required.issubset(set(evaluated["limitations"]))
    assert required.issubset(set(evaluated["formal"]["calls"][0]["limitations"]))
    record = store.latest("eval_assert_completed")
    assert record is not None
    assert required.issubset(set(record["payload"]["limitations"]))
    assert record["payload"]["formal"]["formal_bound_origin"] == "analysis_bound"

    case = PreparedCase(
        case_id="formal-renderer",
        pair_id=None,
        nl="Done is reachable within the finite analysis horizon.",
        raw_source=MODEL,
        raw_source_format="fcstm-identity",
        fcstm=MODEL,
        source_trace={"schema_version": "source_trace_base.v1"},
        metadata={},
        input_mode="custom",
    )
    completed = SimpleNamespace(
        run_id="formal-renderer",
        model_id="STM_0",
        model_sha256="model-sha",
        agent_real_llm=True,
        agent_trace_eligible=True,
        agent_trace_eligibility_scope="agent_behavior_trace",
        input_academic_eligible=False,
        input_academic_ineligibility_reason="custom_input_not_admitted_by_corpus_gate",
        test_replay=False,
        main_result_eligible=False,
        main_result_eligibility_owner="post_loop_experiment_gate",
        main_result_eligibility_reason="B-discover is intermediate.",
        outcome=None,
    )
    report = render_discover(tmp_path, case, completed, store.all(), "en-US")
    report_text = report.read_text(encoding="utf-8")
    for expected in (
        "canonical_query",
        "formal_property_kind",
        "formal_bound",
        "formal_bound_origin",
        "finite_horizon_only",
        "exact_query_and_assumptions_only",
        "does_not_establish_unbounded_correctness",
        "check_result_sha256",
        "tool_schema_hash",
        "evidence_policy_fingerprint",
    ):
        assert expected in report_text


def _formal_requirement_plan(*, assumption_basis_ids=None, assertion_basis_ids=None, expression=None):
    query = 'assume event("Root.go", 0) == true; check reach <= 3: active("Root.Done");'
    return {
        "segment_dispositions": [],
        "fact_dispositions": [],
        "coverage_units": [
            {
                "coverage_unit_id": "CU-REQ",
                "unit_kind": "behavior_obligation",
                "segment_ids": ["SEG-1"],
                "source_fact_ids": [],
                "requirement_ids": ["REQ-TIME-3"],
                "dimensions": ["timing"],
                "statement": "go reaches Done within 3 steps.",
                "rationale": "One bounded timing proposition.",
            }
        ],
        "proposition_roots": [
            {
                "node_id": "ROOT-REQ",
                "coverage_unit_id": "CU-REQ",
                "statement": "Done is reachable within the required bound.",
                "model_element_refs": [],
                "rationale": "One positive Root.",
            }
        ],
        "logical_assertions": [
            {
                "assertion_chain_id": "ASSERT-REQ",
                "root_node_id": "ROOT-REQ",
                "coverage_unit_id": "CU-REQ",
                "required": True,
                "assert": expression or f"fbmcq({query!r}).holds is True",
                "basis_ids": assertion_basis_ids or ["SEG-1", "REQ-TIME-3"],
                "obligation_signature": "go-done-within-3",
                "required_function_families": ["formal"],
                "evidence_scope": {
                    "semantic_profile": "bounded_fcstm_v1",
                    "max_steps": 3,
                    "max_time": None,
                    "abstraction": "bounded_transition_system",
                    "claim_strength": "requirement_bound_response",
                },
                "rationale": "Requirement bound 3 is stated by the timing requirement.",
                "formal_property_kind": "reach",
                "formal_bound": 3,
                "formal_bound_origin": "requirement_bound",
                "formal_assumption_basis_ids": assumption_basis_ids or ["REQ-TIME-3"],
            }
        ],
        "rationale": "Formal requirement-bound test plan.",
    }


def _timing_requirements():
    return {
        "REQ-TIME-3": {
            "requirement_id": "REQ-TIME-3",
            "segment_id": "SEG-1",
            "dimension": "timing",
            "clause_text": "After go, Done must be reached within 3 steps.",
            "cue_text": "within 3 steps",
            "required_function_family_options": [["formal"]],
        },
        "REQ-TIME-9": {
            "requirement_id": "REQ-TIME-9",
            "segment_id": "SEG-1",
            "dimension": "timing",
            "clause_text": "A different behavior has a 9 step limit.",
            "cue_text": "within 9 steps",
            "required_function_family_options": [["formal"]],
        },
    }


def test_formal_assumption_basis_must_be_current_assertion_basis_for_registration():
    registry = CoverageRegistry(
        input_segment_ids=["SEG-1"],
        coverage_requirements=_timing_requirements(),
        fbmcq_guide_read=lambda: True,
    )
    plan = _formal_requirement_plan(
        assumption_basis_ids=["REQ-TIME-9"],
        assertion_basis_ids=["SEG-1", "REQ-TIME-3"],
    )
    plan["coverage_units"][0]["requirement_ids"] = ["REQ-TIME-3", "REQ-TIME-9"]
    rejected = registry.register_plan(
        plan, reason="Reject requirement_bound grounded outside the assertion basis."
    )

    assert rejected["accepted"] is False
    assert any(
        error == "formal_assumption_basis_not_in_assertion_basis:ASSERT-REQ:REQ-TIME-9"
        for error in rejected["errors"]
    )


def test_formal_assumption_basis_rejects_unregistered_profile_like_ids():
    registry = CoverageRegistry(
        input_segment_ids=["SEG-1"],
        coverage_requirements=_timing_requirements(),
        fbmcq_guide_read=lambda: True,
    )
    plan = _formal_requirement_plan(
        assumption_basis_ids=["PROFILE-FAKE"],
        assertion_basis_ids=["SEG-1", "REQ-TIME-3"],
    )
    rejected = registry.register_plan(
        plan,
        reason="Reject a profile-looking assumption without a frozen registry entry.",
    )

    assert rejected["accepted"] is False
    assert any(
        error == "formal_assumption_basis_unknown:ASSERT-REQ:PROFILE-FAKE"
        for error in rejected["errors"]
    )
    assert any(
        error
        == "formal_assumption_basis_not_in_assertion_basis:ASSERT-REQ:PROFILE-FAKE"
        for error in rejected["errors"]
    )


def test_formal_revision_payload_inherits_basis_and_families_and_accepts_real_metadata():
    class FormalObservation:
        holds = True

    revised_query = 'assume event("Root.go", 0) == true; check reach <= 3: active("Root.Done");'
    registry = CoverageRegistry(
        input_segment_ids=["SEG-1"],
        coverage_requirements={"REQ-TIME-3": _timing_requirements()["REQ-TIME-3"]},
        fbmcq_guide_read=lambda: True,
        eval_funcs={"fbmcq": lambda _query: FormalObservation()},
    )
    initial_expression = "fbmcq('check reach <= 3: active(\"Root.Done\");').holds is True"
    accepted = registry.register_plan(
        _formal_requirement_plan(
            assumption_basis_ids=[],
            expression=initial_expression,
        ),
        reason="Register initial formal assertion without assumptions.",
    )
    assert accepted["accepted"] is True

    revised = registry.revise_assertion(
        "ASSERT-REQ",
        f"fbmcq({revised_query!r}).holds is True",
        reason="Revise to include the requirement-backed event assumption and preserve inherited scope.",
        formal_property_kind="reach",
        formal_bound=3,
        formal_bound_origin="requirement_bound",
        formal_assumption_basis_ids=["REQ-TIME-3"],
    )

    assert revised["accepted"] is True
    assert revised["assertion_version_id"] == "ASSERT-REQ@v2"
    assert revised["inherited"]["basis_ids"] == ["SEG-1", "REQ-TIME-3"]
    assert revised["inherited"]["required_function_families"] == ["formal"]

    evaluated = registry.eval_assert(
        f"fbmcq({revised_query!r}).holds is True",
        reason="Execute revised latest formal assertion.",
    )
    assert evaluated["match_status"] == "matches"
    assert evaluated["formal_property_kind"] == "reach"
    assert evaluated["formal_bound_origin"] == "requirement_bound"
    assert evaluated["formal_assumption_basis_ids"] == ["REQ-TIME-3"]


def test_formal_revision_accepts_named_analysis_bound_and_reports_real_chain_id():
    class FormalObservation:
        holds = True

    registry = CoverageRegistry(
        input_segment_ids=["SEG-1"],
        coverage_requirements={"REQ-TIME-3": _timing_requirements()["REQ-TIME-3"]},
        fbmcq_guide_read=lambda: True,
        eval_funcs={"fbmcq": lambda _query: FormalObservation()},
    )
    accepted = registry.register_plan(
        _formal_requirement_plan(
            assumption_basis_ids=[],
            expression="fbmcq('check reach <= 3: active(\"Root.Done\");').holds is True",
        ),
        reason="Register the initial formal assertion.",
    )
    assert accepted["accepted"] is True

    expression = "fbmcq('check reach <= 4: active(\"Root.Done\");').holds is True"
    rejected = registry.revise_assertion(
        "ASSERT-REQ",
        expression,
        reason="将参数修改为数值 4。",
        formal_property_kind="reach",
        formal_bound=4,
        formal_bound_origin="analysis_bound",
        formal_assumption_basis_ids=[],
    )
    assert rejected["accepted"] is False
    assert "formal_analysis_bound_rationale_missing:ASSERT-REQ:4" in rejected["errors"]

    revised = registry.revise_assertion(
        "ASSERT-REQ",
        expression,
        reason="analysis_bound=4 是该命题的有限观察窗口。",
        formal_property_kind="reach",
        formal_bound=4,
        formal_bound_origin="analysis_bound",
        formal_assumption_basis_ids=[],
    )
    assert revised["accepted"] is True
