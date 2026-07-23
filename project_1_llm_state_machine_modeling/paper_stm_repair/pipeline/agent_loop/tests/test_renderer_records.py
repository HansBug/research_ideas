from __future__ import annotations

import copy
from pathlib import Path
from types import SimpleNamespace

import pytest

from paper_stm_repair_loop.inputs import PreparedCase
from paper_stm_repair_loop.records import RecordStore
from paper_stm_repair_loop.renderer import render_discover


def _case() -> PreparedCase:
    return PreparedCase(
        case_id="renderer-v2-case",
        pair_id=None,
        nl="First sentence.\nSecond sentence.",
        raw_source="@startuml\n[*] --> Idle\n@enduml\n",
        raw_source_format="plantuml",
        fcstm="state Root { state Idle; }\n",
        source_trace={"schema_version": "source_trace_base.v1"},
        metadata={},
        input_mode="custom",
    )


def _completed() -> SimpleNamespace:
    return SimpleNamespace(
        run_id="run-renderer-v2",
        model_id="STM_0",
        model_sha256="fcstm-sha",
        agent_real_llm=True,
        agent_trace_eligible=True,
        agent_trace_eligibility_scope="agent_behavior_trace",
        input_academic_eligible=False,
        input_academic_ineligibility_reason="custom_input_not_admitted_by_corpus_gate",
        agent_academic_eligible=True,
        test_replay=False,
        main_result_eligible=False,
        main_result_eligibility_owner="post_loop_experiment_gate",
        main_result_eligibility_reason="B-discover is intermediate.",
        no_issue_found=False,
        issue_checks=[],
        root_nodes=[],
        rejected_propositions=[],
        rationale="V2 projection supplies root outcome.",
    )


def _append_v2_records(store: RecordStore) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    records.append(
        store.append(
            "inputs_frozen",
            {
                "run_id": "run-renderer-v2",
                "case_id": "renderer-v2-case",
                "pair_id": None,
                "input_mode": "custom",
                "raw_source_format": "plantuml",
                "nl_sha256": "raw-nl-sha",
                "normalized_nl_sha256": "norm-nl-sha",
                "fcstm_sha256": "fcstm-sha",
                "segmenter_version": "paper1.nl_segmenter.v1",
                "relation_policy": "exact_identity",
                "formal_verification_available": True,
                "formal_profile_guide_read_once": True,
                "check_result_sha256": "check-sha",
                "tool_schema_hash": "tool-schema-sha",
                "policy_hash": "policy-sha",
                "evidence_policy_fingerprint": "evidence-policy-sha",
                "scope_boundary": {"stage": "B-discover", "repair": False},
                "input_academic_eligible": False,
                "input_academic_ineligibility_reason": "custom_input_not_admitted_by_corpus_gate",
            },
        )
    )
    records.append(
        store.append(
            "input_segments_created",
            {
                "segments": [
                    {
                        "segment_id": "SEG-NL-002",
                        "text": "Second sentence.",
                        "start_offset": 16,
                        "end_offset": 32,
                        "sha256": "seg2-sha",
                    },
                    {
                        "segment_id": "SEG-NL-001",
                        "text": "First sentence.",
                        "start_offset": 0,
                        "end_offset": 15,
                        "sha256": "seg1-sha",
                    },
                ],
                "offset_mapping": {"crlf_to_lf": []},
            },
        )
    )
    records.append(
        store.append(
            "source_inventory_created",
            {
                "source_facts": [
                    {
                        "fact_id": "FACT-TRANSITION-001",
                        "fact_kind": "transition",
                        "source": "Root.Idle",
                        "target": "Root.Done",
                        "qualified_refs": ["transition:Root.Idle:Root.go"],
                        "producer": "pyfcstm.inspect@test",
                    }
                ]
            },
        )
    )
    records.append(
        store.append(
            "coverage_plan_registered",
            {
                "coverage_units": [
                    {
                        "coverage_unit_id": "CU-001",
                        "segment_ids": ["SEG-NL-001"],
                        "source_fact_ids": ["FACT-TRANSITION-001"],
                        "statement": "go reaches Done.",
                    }
                ],
                "segment_dispositions": [
                    {"segment_id": "SEG-NL-002", "disposition": "context_only", "rationale": "background"}
                ],
                "fact_dispositions": [],
                "proposition_roots": [
                    {"node_id": "ROOT-001", "coverage_unit_id": "CU-001", "statement": "go reaches Done"}
                ],
                "latest_assertions": [
                    {
                        "assertion_chain_id": "ASSERT-001",
                        "assertion_version_id": "ASSERT-001@v1",
                        "root_node_id": "ROOT-001",
                        "coverage_unit_id": "CU-001",
                        "assert": "transition_exists(source='Root.Idle', event='Root.go', target='Root.Done')",
                        "assert_sha256": "assert-sha",
                        "required_function_families": ["relation"],
                    }
                ],
                "plan_sha256": "plan-sha",
            },
        )
    )
    records.append(
        store.append(
            "assertion_revision_registered",
            {
                "assertion_chain_id": "ASSERT-001",
                "assertion_version_id": "ASSERT-001@v2",
                "assert": "simulate(cycles=[[]]).final.state == 'Root.Idle' and fbmcq('check reach <= 20: active(\"Root.Done\");').holds is True",
                "assert_sha256": "assert-v2-sha",
                "limitations": ["append_only_revision"],
            },
        )
    )
    records.append(
        store.append(
            "eval_assert_call_prepared",
            {
                "assertion_chain_id": "ASSERT-001",
                "assertion_version_id": "ASSERT-001@v2",
                "root_node_id": "ROOT-001",
                "coverage_unit_id": "CU-001",
                "assert": "transition_exists(source='Root.Idle', target='Root.Done')",
                "assert_sha256": "assert-v2-sha",
                "reason": "Keep this exact raw reason from the agent.",
                "reason_context": {"related_segment_ids": ["SEG-NL-001"]},
            },
        )
    )
    records.append(
        store.append(
            "eval_assert_completed",
            {
                "assertion_chain_id": "ASSERT-001",
                "assertion_version_id": "ASSERT-001@v2",
                "root_node_id": "ROOT-001",
                "coverage_unit_id": "CU-001",
                "assert_sha256": "assert-v2-sha",
                "execution_status": "completed",
                "match_status": "matches",
                "python_return": True,
                "initialization": {
                    "calls": [
                        {
                            "requested": {
                                "mode": "hot",
                                "state": "Root.Idle",
                                "variables": {"speed": 20, "brake": 0},
                            },
                            "effective": {
                                "mode": "hot",
                                "state": "Root.Idle",
                                "variables": {"speed": 20, "brake": 0},
                            },
                            "cycles": [[]],
                            "final": {
                                "state": "Root.Idle",
                                "variables": {"speed": 20, "brake": 0},
                            },
                        }
                    ]
                },
                "formal": {
                    "calls": [
                        {
                            "query": "check reach <= 20: active(\"Root.Done\");",
                            "canonical_query": "check reach <= 20: active(\"Root.Done\");",
                            "formal_property_kind": "reach",
                            "formal_bound": 20,
                            "limitations": [
                                "finite_horizon_only",
                                "exact_query_and_assumptions_only",
                                "does_not_establish_unbounded_correctness",
                            ],
                        }
                    ],
                    "formal_property_kind": "reach",
                    "formal_bound": 20,
                    "formal_bound_origin": "analysis_bound",
                    "formal_assumption_basis_ids": ["REQ-001"],
                },
                "check": {
                    "check_record_id": "REC-CHECK",
                    "check_result_sha256": "check-sha",
                    "model_sha256": "fcstm-sha",
                    "tool_hash": "tool-hash",
                    "tool_schema_hash": "tool-schema-sha",
                },
                "policy": {"policy_hash": "policy-sha", "evidence_policy_fingerprint": "evidence-policy-sha"},
                "function_call_trace": [
                    {"family": "simulation", "function": "simulate"},
                    {"family": "formal", "function": "fbmcq"},
                ],
                "witness": {"transition": "Root.Idle --go--> Root.Done"},
                "limitations": [
                    "finite_horizon_only",
                    "exact_query_and_assumptions_only",
                    "does_not_establish_unbounded_correctness",
                ],
            },
        )
    )
    records.append(
        store.append(
            "root_projection_completed",
            {
                "run_outcome": "reviewer_accepted_zero_issue",
                "registered_worklist_complete": True,
                "major_behavior_coverage_assurance": "agent_declared",
                "input_segment_coverage": {"total": 2, "covered": 2},
                "selected_source_fact_evidence_coverage": {"total": 1, "covered": 1},
                "assertion_execution_coverage": {"total_required": 1, "completed_latest": 1},
                "proposition_roots": [
                    {
                        "node_id": "ROOT-001",
                        "coverage_unit_id": "CU-001",
                        "assertion_chain_ids": ["ASSERT-001"],
                        "status": "ok",
                        "regression_guard": True,
                        "repair_allowed": False,
                        "statement": "go reaches Done",
                    }
                ],
                "issue_root_projection": [],
                "regression_guard_projection": [{"node_id": "ROOT-001", "status": "ok"}],
                "incomplete_root_projection": [],
                "rationale": "Deterministic projection from eval_assert result.",
            },
        )
    )
    records.append(
        store.append(
            "discover_completed",
            {
                "schema_version": "paper1.discover_completed.v2",
                "run_id": "run-renderer-v2",
                "model_id": "STM_0",
                "model_sha256": "fcstm-sha",
                "main_result_eligible": False,
                "main_result_eligibility_owner": "post_loop_experiment_gate",
                "main_result_eligibility_reason": "B-discover is intermediate.",
                "agent_real_llm": True,
                "agent_trace_eligible": True,
                "agent_trace_eligibility_scope": "agent_behavior_trace",
                "input_academic_eligible": False,
                "input_academic_ineligibility_reason": "custom_input_not_admitted_by_corpus_gate",
                "agent_academic_eligible": True,
                "test_replay": False,
            },
        )
    )
    records.append(
        store.append(
            "discover_report_render_completed",
            {"report_path": "loops/discover.md", "report_sha256": "not-yet-known-in-this-fixture"},
        )
    )
    return records


def test_record_store_accepts_v2_record_types_append_only_and_renderer_links_them(tmp_path: Path):
    store = RecordStore(tmp_path)
    records = _append_v2_records(store)
    store.validate_chain()

    assert [record["record_type"] for record in store.all()] == [record["record_type"] for record in records]

    report = render_discover(tmp_path, _case(), _completed(), store.all(), "en-US")
    text = report.read_text(encoding="utf-8")

    assert "## V2 deterministic coverage record view" in text
    assert "### NL segments" in text
    assert text.index("`SEG-NL-001`") < text.index("`SEG-NL-002`")
    assert "### SourceFacts inventory" in text
    assert "`FACT-TRANSITION-001` `transition`" in text
    assert "#### coverage_units" in text
    assert "#### segment_dispositions" in text
    assert "ASSERT-001@v2" in text
    assert "Keep this exact raw reason from the agent." in text
    assert "function_call_trace" in text
    assert "Root.Idle --go--> Root.Done" in text
    assert "formal_profile_guide_read_once" in text
    assert '"requested": {' in text
    assert '"effective": {' in text
    assert "formal_bound_origin" in text
    assert "finite_horizon_only" in text
    assert "check_result_sha256" in text
    assert "evidence_policy_fingerprint" in text
    assert "#### regression_guard_projection" in text
    assert "post_loop_experiment_gate" in text
    assert "Agent trace eligible: `true`" in text
    assert "input academic eligible: `false`" in text
    assert "custom_input_not_admitted_by_corpus_gate" in text
    assert '"stage": "B-discover"' in text

    for record_type in (
        "inputs_frozen",
        "input_segments_created",
        "source_inventory_created",
        "coverage_plan_registered",
        "assertion_revision_registered",
        "eval_assert_call_prepared",
        "eval_assert_completed",
        "root_projection_completed",
        "discover_completed",
        "discover_report_render_completed",
    ):
        assert record_type in text

    for record in store.all():
        directory = f"L{record['logical_loop_index']:03d}-{record['sequence']:06d}-{record['record_type'].replace('_', '-')}"
        assert (tmp_path / "records" / directory / "record.json").is_file()


def test_eval_assert_completed_fails_closed_before_partial_record_is_written(tmp_path: Path):
    store = RecordStore(tmp_path)

    with pytest.raises(ValueError, match="validation error"):
        store.append(
            "eval_assert_completed",
            {
                "initialization": {"calls": []},
                "formal": {"calls": []},
                "check": {},
                "policy": {},
                "limitations": [],
            },
        )

    assert store.all() == []


def _valid_formal_eval_payload() -> dict[str, object]:
    limitations = [
        "finite_horizon_only",
        "exact_query_and_assumptions_only",
        "does_not_establish_unbounded_correctness",
    ]
    return {
        "initialization": {"calls": []},
        "formal": {
            "calls": [
                {
                    "query": "check reach <= 3: true;",
                    "canonical_query": "check reach <= 3: true;",
                    "formal_property_kind": "reach",
                    "formal_bound": 3,
                    "limitations": limitations,
                }
            ],
            "formal_property_kind": "reach",
            "formal_bound": 3,
            "formal_bound_origin": "analysis_bound",
            "formal_assumption_basis_ids": [],
        },
        "check": {
            "check_record_id": "REC-CHECK",
            "check_result_sha256": "check-sha",
            "model_sha256": "model-sha",
            "tool_hash": "tool-hash",
            "tool_schema_hash": "schema-sha",
        },
        "policy": {
            "policy_hash": "policy-sha",
            "evidence_policy_fingerprint": "policy-sha",
        },
        "limitations": limitations,
    }


@pytest.mark.parametrize(
    "invalid_kind",
    ["missing_call_limitation", "missing_record_limitation", "missing_bound_origin"],
)
def test_formal_evidence_scope_fails_closed_before_write(
    tmp_path: Path, invalid_kind: str
):
    payload = copy.deepcopy(_valid_formal_eval_payload())
    if invalid_kind == "missing_call_limitation":
        payload["formal"]["calls"][0]["limitations"].remove(
            "does_not_establish_unbounded_correctness"
        )
    elif invalid_kind == "missing_record_limitation":
        payload["limitations"].remove("finite_horizon_only")
    else:
        payload["formal"]["formal_bound_origin"] = None
    store = RecordStore(tmp_path / invalid_kind)

    with pytest.raises(ValueError):
        store.append("eval_assert_completed", payload)

    assert store.all() == []


def test_discover_completed_eligibility_alias_fails_closed_before_write(tmp_path: Path):
    store = RecordStore(tmp_path)

    with pytest.raises(ValueError, match="must equal agent_trace_eligible"):
        store.append(
            "discover_completed",
            {
                "agent_trace_eligible": True,
                "agent_trace_eligibility_scope": "agent_behavior_trace",
                "input_academic_eligible": False,
                "input_academic_ineligibility_reason": "custom_input",
                "agent_academic_eligible": False,
                "main_result_eligible": False,
            },
        )

    assert store.all() == []


def test_renderer_rejects_completed_object_record_eligibility_mismatch(tmp_path: Path):
    store = RecordStore(tmp_path)
    store.append(
        "discover_completed",
        {
            "agent_trace_eligible": False,
            "agent_trace_eligibility_scope": "agent_behavior_trace",
            "input_academic_eligible": False,
            "input_academic_ineligibility_reason": "custom_input_not_admitted_by_corpus_gate",
            "agent_academic_eligible": False,
            "main_result_eligible": False,
        },
    )

    with pytest.raises(
        ValueError, match="discover_completed eligibility mismatch: agent_trace_eligible"
    ):
        render_discover(tmp_path, _case(), _completed(), store.all(), "en-US")
