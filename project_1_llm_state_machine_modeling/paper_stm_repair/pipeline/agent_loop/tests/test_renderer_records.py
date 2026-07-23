from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

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
        agent_academic_eligible=False,
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
                "assert": "transition_exists(source='Root.Idle', target='Root.Done')",
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
                    "initialization_mode": "hot",
                    "requested_initial_state": "Root.Idle",
                    "effective_initial_state": "Root.Idle",
                    "requested_initial_vars": {"speed": 20},
                    "effective_initial_vars": {"speed": 20, "brake": 0},
                },
                "formal": {
                    "canonical_query": "A[] not brake_and_accel",
                    "property_kind": "safety",
                    "formal_bound": 20,
                    "formal_bound_origin": "analysis_bound",
                    "formal_assumption_basis_ids": ["REQ-001"],
                },
                "check": {"check_result_sha256": "check-sha", "tool_schema_hash": "tool-schema-sha"},
                "policy": {"policy_hash": "policy-sha", "evidence_policy_fingerprint": "evidence-policy-sha"},
                "function_call_trace": [{"family": "relation", "function": "transition_exists"}],
                "witness": {"transition": "Root.Idle --go--> Root.Done"},
                "limitations": [],
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
                "agent_academic_eligible": False,
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
    assert "requested_initial_vars" in text
    assert "formal_bound_origin" in text
    assert "check_result_sha256" in text
    assert "evidence_policy_fingerprint" in text
    assert "#### regression_guard_projection" in text
    assert "post_loop_experiment_gate" in text
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
