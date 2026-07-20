from __future__ import annotations

import importlib

import pytest
from pydantic import ValidationError


def load_schema(name: str):
    return importlib.import_module(f"paper_stm_repair_loop.schemas.{name}")


def test_strict_schema_rejects_extra_fields_and_requires_bool_semantics():
    coverage = load_schema("coverage")
    assertions = load_schema("assertions")
    roots = load_schema("roots")
    discovery = load_schema("discovery")
    tool_reason = load_schema("tool_reason")

    segment = coverage.InputSegment.model_validate(
        {
            "segment_id": "SEG-NL-001",
            "source_role": "nl",
            "text": "Attack Complete returns to Searching.",
            "start_offset": 0,
            "end_offset": 37,
            "raw_start_offset": 0,
            "raw_end_offset": 37,
            "sha256": "hash",
            "language": "en-US",
            "segmenter_version": "paper1.nl_segmenter.v1",
            "segment_kind": "prose",
            "ordinal": 1,
        }
    )
    assert segment.segment_id == "SEG-NL-001"
    with pytest.raises(ValidationError):
        coverage.SegmentDisposition.model_validate(
            {
                "segment_id": "SEG-NL-001",
                "disposition": "context_only",
                "rationale": "背景。",
                "extra": "forbidden",
            }
        )

    evidence_scope = assertions.EvidenceScope.model_validate(
        {
            "semantic_profile": "single_active_leaf_fcstm_v1",
            "max_steps": 8,
            "max_time": None,
            "abstraction": "discrete_event",
            "claim_strength": "deterministic_effect_fact",
        }
    )
    logical_assertion = assertions.LogicalAssertion.model_validate(
        {
            "assertion_chain_id": "ASSERT-001",
            "assertion_version_id": "ASSERT-001@v1",
            "root_node_id": "ROOT-001",
            "coverage_unit_id": "CU-REQ-001",
            "required": True,
            "assert": "len(states(parent='Root.Searching')) >= 3",
            "assert_sha256": "hash",
            "basis_ids": ["SEG-NL-001"],
            "obligation_signature": "sig",
            "required_function_families": ["structure"],
            "evidence_scope": evidence_scope.model_dump(mode="json"),
            "rationale": "正向结构义务。",
        }
    )
    assert logical_assertion.assert_ == "len(states(parent='Root.Searching')) >= 3"
    assert tool_reason.EvalAssertInput.model_validate({"assert": "True", "reason": "single"}).assert_ == "True"
    with pytest.raises(ValidationError):
        tool_reason.EvalAssertInput.model_validate({"assert": "True", "reason": "single", "batch": []})

    root = roots.PropositionRootNode.model_validate(
        {
            "node_id": "ROOT-001",
            "coverage_unit_id": "CU-REQ-001",
            "assertion_chain_ids": ["ASSERT-001"],
            "statement": "模型包含三个搜索区域。",
            "status": "issue",
            "runtime_issue_assessment": "confirmed",
            "repair_allowed": True,
            "regression_guard": False,
        }
    )
    assert root.status == "issue"
    outcome = discovery.DiscoverOutcome.model_validate(
        {
            "run_outcome": "issues_found",
            "registered_coverage_complete": True,
            "semantic_coverage_assurance": "controller_closed_dual_llm_reviewed",
            "proposition_roots": [root.model_dump(mode="json")],
            "issue_root_projection": [root.model_dump(mode="json")],
        }
    )
    assert outcome.run_outcome == "issues_found"
    with pytest.raises(ValidationError):
        discovery.DiscoverOutcome.model_validate(
            {
                "run_outcome": "coverage_incomplete",
                "registered_coverage_complete": False,
                "semantic_coverage_assurance": "controller_closed_dual_llm_reviewed",
            }
        )
    with pytest.raises(ValidationError):
        discovery.DiscoverOutcome.model_validate(
            {
                "run_outcome": "complete_coverage_zero_issue",
                "registered_coverage_complete": True,
                "semantic_coverage_assurance": "agent_declared",
            }
        )


def test_coverage_plan_gate_enforces_segment_fact_root_assertion_closure():
    coverage = load_schema("coverage")
    unit = {
        "coverage_unit_id": "CU-REQ-001",
        "unit_kind": "behavior_obligation",
        "segment_ids": ["SEG-NL-001"],
        "source_fact_ids": ["FACT-STATE-001"],
        "statement": "Go.",
        "rationale": "行为义务。",
    }
    root = {
        "node_id": "ROOT-001",
        "coverage_unit_id": "CU-REQ-001",
        "statement": "The model contains Idle.",
        "rationale": "Root for the registered unit.",
    }
    assertion = {
        "assertion_chain_id": "ASSERT-001",
        "root_node_id": "ROOT-001",
        "coverage_unit_id": "CU-REQ-001",
        "assert": "states(name='Root.Idle')",
        "required": True,
        "basis_ids": ["SEG-NL-001"],
        "obligation_signature": "idle-exists",
        "required_function_families": ["structure"],
        "evidence_scope": {
            "semantic_profile": "single_active_leaf_fcstm_v1",
            "max_steps": None,
            "max_time": None,
            "abstraction": "discrete_event",
            "claim_strength": "structure_fact",
        },
        "rationale": "Positive structure assertion.",
    }
    assert coverage.CoveragePlan.model_validate(
        {
            "coverage_units": [unit],
            "proposition_roots": [root],
            "logical_assertions": [assertion],
            "rationale": "Complete fixture plan.",
        }
    )

    with pytest.raises(ValidationError, match="both CoverageUnit refs and SegmentDisposition"):
        coverage.CoveragePlan.model_validate(
            {
                "segment_dispositions": [
                    {
                        "segment_id": "SEG-NL-001",
                        "disposition": "context_only",
                        "rationale": "背景。",
                    }
                ],
                "coverage_units": [unit],
                "proposition_roots": [root],
                "logical_assertions": [assertion],
                "rationale": "Invalid overlap.",
            }
        )
