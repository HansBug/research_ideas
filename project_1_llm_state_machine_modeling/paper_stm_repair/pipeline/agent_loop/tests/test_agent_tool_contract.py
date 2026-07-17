from __future__ import annotations

import inspect
import json
from pathlib import Path
from typing import Any

import pytest

from paper_stm_repair_loop.tools.check_fcstm import execute as check_fcstm
from paper_stm_repair_loop.tools.evaluate_checks import build_tool as build_evaluate_checks_tool
from paper_stm_repair_loop.tools.guide_access import GuideAccessState, guard_tool, property_batch_requested
from paper_stm_repair_loop.tools.lookup_source_trace import build_tool as build_lookup_source_trace_tool
from paper_stm_repair_loop.tools.observe_trace import build_tool as build_observe_trace_tool
from paper_stm_repair_loop.tools.post_batch_investigation import PostBatchInvestigationState
from paper_stm_repair_loop.tools.query_model import build_tool as build_query_model_tool
from paper_stm_repair_loop.tools.read_task import build_tool as build_read_task_tool
from paper_stm_repair_loop.tools.read_fbmcq_guide import build_tool as build_read_fbmcq_guide_tool
from paper_stm_repair_loop.tools.read_fcstm_guide import build_tool as build_read_fcstm_guide_tool
from paper_stm_repair_loop.schemas.common import DiscoverSubmission
from utils.agent import AgentSpec


SNAPSHOT: dict[str, Any] = {
    "stage": "B-discover",
    "loop_no": 0,
    "model": {
        "fcstm": "state Root { event go; state Idle; state Done; [*] -> Idle; Idle -> Done : go; }",
        "fcstm_sha256": "model-sha",
        "context_snapshot_head": "ctx-sha",
        "normalized_inspect": {
            "states": [{"path": "Root.Idle"}, {"path": "Root.Done"}],
            "events": [{"qualified_name": "Root.go"}],
            "transitions": [{"transition_index": 1, "source": "Root.Idle", "target": "Root.Done", "event": "Root.go"}],
            "variables": [],
            "diagnostics": [{"code": "demo", "severity": "info"}],
        },
    },
    "targets": [],
    "current_records": {
        "nl": {"content": "When go occurs, Done is reachable."},
        "raw_source": {"content": "Idle -> Done on go"},
        "source_trace": {
            "trace_sha256": "trace-sha",
            "entries": [
                {"source_elements": ["source:req1"], "intermediate_elements": ["transition:T1"]},
                {"source_elements": ["source:req2a", "source:req2b"], "intermediate_elements": ["transition:T2"]},
            ],
        },
        "issue_checks": [],
        "tool_results": {},
    },
    "readable_history": [],
    "source_trace": {
        "trace_sha256": "trace-sha",
        "entries": [
            {"source_elements": ["source:req1"], "intermediate_elements": ["transition:T1"]},
            {"source_elements": ["source:req2a", "source:req2b"], "intermediate_elements": ["transition:T2"]},
        ],
    },
}


def deterministic_runner(*, events: list[str], max_steps: int | None = None) -> dict[str, Any]:
    assert max_steps is None or max_steps >= len(events)
    return {
        "execution_status": "completed",
        "cycles": len(events),
        "input_events": events,
        "consumed_events": events,
        "unconsumed_events": [],
        "final_configuration": {"current_state": "Root.Done"},
        "diagnostics": [],
    }


def eligible_scenario_payload(check_id: str = "draft-go") -> dict[str, Any]:
    return {
        "checks": [
            {
                "check_origin": "nl_grounded_behavioral_issue",
                "check_id": check_id,
                "check_kind": "scenario",
                "statement": "The go event reaches Done.",
                "expected_outcome": {"target_label": "Done"},
                "source_basis": [],
                "nl_basis": [
                    {"quote": "When go occurs, Done is reachable.", "role": "requirement"}
                ],
                "executable_spec": {"event_labels": ["Root.go"]},
                "binding_refs": [],
                "required": True,
            }
        ]
    }


def test_discover_submission_schema_rejects_empty_rejected_check_relation():
    base = {
        "submission_type": "submit_discovery",
        "assessment_origin": "discover",
        "check_drafts": [
            {
                "check_id": "draft-1",
                "check_origin": "nl_grounded_behavioral_issue",
                "check_kind": "scenario",
                "statement": "The go event reaches Done.",
                "nl_basis": [{"quote": "When go occurs, Done is reachable.", "role": "requirement"}],
            }
        ],
        "no_issue_found": True,
        "root_nodes": [],
        "rejected_propositions": [
            {
                "proposition_id": "rejected-1",
                "statement": "The scenario does not reveal a defect.",
                "rationale": "The observed state matches the requirement.",
                "considered_check_ids": ["draft-1"],
            }
        ],
        "rationale": "The complete final batch was considered.",
    }
    assert DiscoverSubmission.model_validate(base).no_issue_found is True

    empty_relation = json.loads(json.dumps(base))
    empty_relation["rejected_propositions"][0]["considered_check_ids"] = []
    with pytest.raises(ValueError, match="at least 1 item"):
        DiscoverSubmission.model_validate(empty_relation)

def registered_tools(*, unlock_fcstm: bool = False, unlock_fbmcq: bool = False):
    model_text = SNAPSHOT["model"]["fcstm"]
    state = GuideAccessState()
    evaluation_invocations: list[dict[str, Any]] = []
    investigation_state = PostBatchInvestigationState(evaluation_invocations)
    fcstm_guide = build_read_fcstm_guide_tool(state)
    fbmcq_guide = build_read_fbmcq_guide_tool(state)
    tools = (
        fcstm_guide,
        fbmcq_guide,
        guard_tool(build_read_task_tool(SNAPSHOT), state),
        guard_tool(build_query_model_tool(SNAPSHOT), state),
        guard_tool(build_observe_trace_tool(SNAPSHOT, deterministic_runner, investigation_state), state),
        guard_tool(build_lookup_source_trace_tool(SNAPSHOT, investigation_state), state),
        guard_tool(build_evaluate_checks_tool(
            SNAPSHOT,
            model_text=model_text,
            check_result=check_fcstm(model_text),
            model_path=Path("<frozen>"),
            formal_required=True,
            invocation_log=evaluation_invocations,
        ), state, require_fbmcq_when=property_batch_requested),
    )
    if unlock_fcstm:
        fcstm_guide.invoke({})
    if unlock_fbmcq:
        fbmcq_guide.invoke({})
    return tools


def test_agent_spec_exposes_single_run_discover_tools_with_contract_descriptions():
    spec = AgentSpec(name="discover-tool-contract", system_prompt="Use tools safely.", tools=registered_tools())
    assert spec.tool_names == (
        "read_fcstm_guide",
        "read_fbmcq_guide",
        "read_task",
        "query_model",
        "observe_trace",
        "lookup_source_trace",
        "evaluate_checks",
    )
    forbidden = {"check_fcstm", "validate_discovery_checks", "run_scenarios", "verify_properties", "compare_models", "read_issue_history", "read_loop"}
    assert not forbidden.intersection(spec.tool_names)
    required_sections = ["Purpose", "Parameters", "Returns", "Execution", "Failure semantics", "Evidence limitations", "Permissions", "Example"]
    for tool in spec.tools:
        description = str(getattr(tool, "description", ""))
        description_flat = " ".join(description.split())
        assert description == inspect.getdoc(tool.func)
        for section in required_sections:
            assert section in description, f"{tool.name} missing {section}"
        assert "reference/gold" in description
        assert "arbitrary paths" in description_flat or "No path" in description_flat or "no path" in description_flat


def test_agent_tool_descriptions_define_parameter_and_result_fields_not_only_section_headings():
    descriptions = {tool.name: str(tool.description) for tool in registered_tools()}
    required_markers = {
        "read_task": [
            "exactly ``{}``",
            "exactly six top-level fields",
            "``stage``",
            "``loop_no``",
            "``model``",
            "``targets``",
            "``current_records``",
            "``readable_history``",
            "same six fields, values, model hash, record set",
        ],
        "read_fcstm_guide": [
            "integrity-checked FCSTM grammar",
            "``pyfcstm_version``",
            "``sha256``",
            "must precede the first ``read_task`` call",
        ],
        "read_fbmcq_guide": [
            "integrity-checked FBMCQ authoring guide",
            "property kinds",
            "definedness",
            "vacuity",
        ],
        "query_model": [
            "required string enum",
            "case-insensitive substring",
            "must be 1 through 500",
            "``matched_items``",
            "``total_matches``",
            "``truncated``",
            "If ``truncated=true``",
        ],
        "observe_trace": [
            "required JSON array of strings",
            "offered in a separate cycle",
            "not a coverage engine",
            "do not enumerate event permutations",
            "eligible full-batch ``evaluate_checks`` result",
            "``consumed_events`` / ``unconsumed_events``",
            "``final_configuration``",
            "``timeout``",
            "A no-counterexample observation is never a proof",
        ],
        "lookup_source_trace": [
            "required JSON array of strings",
            "``fcstm_to_source``",
            "``source_to_fcstm``",
            "``exact_matches``",
            "``ambiguous_matches``",
            "``untraceable_refs``",
            "Every requested ref appears in exactly one",
        ],
        "evaluate_checks": [
            "one complete batch",
            "inside this single ``AgentApp.run``",
            "``check_origin``",
            "``expected_outcome``",
            "``issue_checks``",
            "``validation``",
            "``scenarios``",
            "``properties``",
            "``static_consistency``",
            "``gate``",
            "never alter the expected outcome",
        ],
    }
    for tool_name, markers in required_markers.items():
        description = " ".join(descriptions[tool_name].split())
        for marker in markers:
            assert marker in description, f"{tool_name} description missing detailed contract marker: {marker}"


def test_agent_tool_input_schemas_are_strict_and_do_not_leak_identity_or_permissions():
    forbidden_props = {"path", "model_path", "model_text", "model", "run_id", "case_id", "pair_id", "url", "shell", "python", "z3"}
    for tool in registered_tools():
        schema = tool.args_schema.model_json_schema()
        assert schema.get("additionalProperties") is False
        props = set(schema.get("properties", {}))
        assert not forbidden_props.intersection(props), f"{tool.name} leaked {forbidden_props.intersection(props)}"
    assert set(registered_tools()[0].args_schema.model_json_schema().get("properties", {})) == set()
    assert set(registered_tools()[1].args_schema.model_json_schema().get("properties", {})) == set()
    assert set(build_read_task_tool(SNAPSHOT).args_schema.model_json_schema().get("properties", {})) == set()
    assert set(build_query_model_tool(SNAPSHOT).args_schema.model_json_schema()["properties"]) == {"query_kind", "name_contains", "offset", "limit"}
    assert set(build_observe_trace_tool(SNAPSHOT, deterministic_runner).args_schema.model_json_schema()["properties"]) == {"events", "max_steps"}
    assert set(build_lookup_source_trace_tool(SNAPSHOT).args_schema.model_json_schema()["properties"]) == {"element_refs", "direction"}
    evaluate_schema = registered_tools()[-1].args_schema.model_json_schema()
    assert set(evaluate_schema["properties"]) == {"checks"}


def test_docstring_examples_match_signatures_and_strict_schema_dry_run():
    tools = {tool.name: tool for tool in registered_tools()}
    assert list(inspect.signature(tools["read_fcstm_guide"].func).parameters) == []
    assert list(inspect.signature(tools["read_fbmcq_guide"].func).parameters) == []
    assert list(inspect.signature(tools["read_task"].func).parameters) == []
    assert list(inspect.signature(tools["query_model"].func).parameters) == ["query_kind", "name_contains", "offset", "limit"]
    assert list(inspect.signature(tools["observe_trace"].func).parameters) == ["events", "max_steps"]
    assert list(inspect.signature(tools["lookup_source_trace"].func).parameters) == ["element_refs", "direction"]
    assert list(inspect.signature(tools["evaluate_checks"].func).parameters) == ["checks"]

    blocked = tools["read_task"].invoke({})
    assert blocked["execution_status"] == "prerequisite_required"
    assert blocked["required_tool"] == "read_fcstm_guide"
    fcstm_guide = tools["read_fcstm_guide"].invoke({})
    assert fcstm_guide["execution_status"] == "completed"
    assert fcstm_guide["content"].startswith("# FCSTM")

    task = tools["read_task"].invoke({})
    assert set(task) == {"stage", "loop_no", "model", "targets", "current_records", "readable_history"}
    assert task["model"]["fcstm_sha256"] == "model-sha"

    query = tools["query_model"].invoke({"query_kind": "states", "name_contains": "Root", "offset": 0, "limit": 1})
    assert query["execution_status"] == "completed"
    assert query["total_matches"] == 2
    assert query["truncated"] is True
    assert query["model_sha256"] == "model-sha"

    duplicate_query = tools["query_model"].invoke(
        {"query_kind": "states", "name_contains": "Root", "offset": 0, "limit": 1}
    )
    assert duplicate_query["execution_status"] == "invalid_arguments"
    assert "duplicate_query_not_executed" in duplicate_query["limitations"]

    same_fact_new_filter = tools["query_model"].invoke(
        {"query_kind": "states", "name_contains": "Idle", "offset": 0, "limit": 50}
    )
    assert same_fact_new_filter["execution_status"] == "invalid_arguments"
    assert "no_new_structural_fact" in same_fact_new_filter["limitations"]

    complete_events = tools["query_model"].invoke(
        {"query_kind": "events", "offset": 0, "limit": 50}
    )
    assert complete_events["execution_status"] == "completed"
    assert complete_events["truncated"] is False
    redundant_filtered_events = tools["query_model"].invoke(
        {"query_kind": "events", "name_contains": "go", "offset": 0, "limit": 50}
    )
    assert redundant_filtered_events["execution_status"] == "invalid_arguments"
    assert "category_already_returned_untruncated" in redundant_filtered_events["limitations"]

    trace_before_batch = tools["observe_trace"].invoke({"events": ["Root.go"], "max_steps": 2})
    assert trace_before_batch["execution_status"] == "prerequisite_required"
    assert trace_before_batch["diagnostics"][0]["code"] == "eligible_evaluate_checks_required_first"

    mapping_before_batch = tools["lookup_source_trace"].invoke(
        {"element_refs": ["transition:T1"], "direction": "fcstm_to_source"}
    )
    assert mapping_before_batch["execution_status"] == "prerequisite_required"
    assert "eligible_evaluate_checks_required_first" in mapping_before_batch["limitations"]

    evaluated_scenario = tools["evaluate_checks"].invoke(eligible_scenario_payload())
    assert evaluated_scenario["execution_status"] == "completed"
    assert evaluated_scenario["gate"]["eligible"] is True

    trace = tools["observe_trace"].invoke({"events": ["Root.go"], "max_steps": 2})
    assert trace["execution_status"] == "completed"
    assert trace["consumed_events"] == ["Root.go"]
    assert "single_trace_cannot_prove_correctness" in trace["limitations"]

    mapping = tools["lookup_source_trace"].invoke({"element_refs": ["transition:T1", "transition:T2", "transition:missing"], "direction": "fcstm_to_source"})
    assert mapping["execution_status"] == "completed"
    assert [item["requested_ref"] for item in mapping["exact_matches"]] == ["transition:T1"]
    assert [item["requested_ref"] for item in mapping["ambiguous_matches"]] == ["transition:T2"]
    assert mapping["untraceable_refs"] == ["transition:missing"]
    assert mapping["trace_sha256"] == "trace-sha"

    repeated_trace = tools["observe_trace"].invoke({"events": ["Root.go"], "max_steps": 2})
    assert repeated_trace["execution_status"] == "invalid_arguments"
    assert repeated_trace["diagnostics"][0]["code"] == "post_batch_trace_already_completed"

    repeated_mapping = tools["lookup_source_trace"].invoke(
        {"element_refs": ["transition:T1"], "direction": "fcstm_to_source"}
    )
    assert repeated_mapping["execution_status"] == "invalid_arguments"
    assert "post_batch_source_lookup_already_completed" in repeated_mapping["limitations"]

    repeated_evaluation = tools["evaluate_checks"].invoke(eligible_scenario_payload())
    assert repeated_evaluation["drafts_sha256"] == evaluated_scenario["drafts_sha256"]
    still_blocked = tools["observe_trace"].invoke({"events": ["Root.go"], "max_steps": 2})
    assert still_blocked["execution_status"] == "invalid_arguments"

    changed_evaluation = tools["evaluate_checks"].invoke(
        eligible_scenario_payload("draft-go-revised")
    )
    assert changed_evaluation["drafts_sha256"] != evaluated_scenario["drafts_sha256"]
    reopened_for_distinct_batch = tools["observe_trace"].invoke(
        {"events": ["Root.go"], "max_steps": 2}
    )
    assert reopened_for_distinct_batch["execution_status"] == "completed"

    property_payload = (
        {
            "checks": [
                {
                    "check_origin": "nl_grounded_behavioral_issue",
                    "check_id": "draft-simple-state",
                    "check_kind": "property",
                    "statement": "Done is a simple state.",
                    "expected_outcome": {"property_satisfied": True},
                    "source_basis": [],
                    "nl_basis": [{"quote": "Done is simple.", "role": "requirement"}],
                    "executable_spec": {"kind": "simple_state", "target_label": "Done", "bound": 0},
                    "binding_refs": [],
                    "required": True,
                }
            ]
        }
    )
    blocked_property = tools["evaluate_checks"].invoke(property_payload)
    assert blocked_property["execution_status"] == "prerequisite_required"
    assert blocked_property["required_tool"] == "read_fbmcq_guide"
    fbmcq_guide = tools["read_fbmcq_guide"].invoke({})
    assert fbmcq_guide["execution_status"] == "completed"
    assert fbmcq_guide["content"].startswith("# FBMCQ")
    evaluated = tools["evaluate_checks"].invoke(property_payload)
    assert evaluated["execution_status"] == "completed"
    assert evaluated["gate"]["eligible"] is True
    assert evaluated["issue_checks"][0]["check_id"] == "CHK-NL-001"
    assert evaluated["properties"]["property_results"][0]["solver_status"] == "deterministic_static"


def test_evaluate_checks_rejects_partially_bound_final_batch():
    tool = {tool.name: tool for tool in registered_tools(unlock_fcstm=True, unlock_fbmcq=True)}["evaluate_checks"]
    evaluated = tool.invoke(
        {
            "checks": [
                {
                    "check_origin": "nl_grounded_behavioral_issue",
                    "check_id": "draft-valid",
                    "check_kind": "property",
                    "statement": "Done is a simple state.",
                    "expected_outcome": {"property_satisfied": True},
                    "source_basis": [],
                    "nl_basis": [{"quote": "Done is simple.", "role": "requirement"}],
                    "executable_spec": {"kind": "simple_state", "target_label": "Done", "bound": 0},
                    "binding_refs": [],
                    "required": True,
                },
                {
                    "check_origin": "raw_internal_inconsistency",
                    "check_id": "draft-invalid-source-contract",
                    "check_kind": "static_consistency",
                    "statement": "One source fact does not establish an internal contradiction.",
                    "expected_outcome": {"consistency_status": "contradicts"},
                    "source_basis": ["only-one-source-fact"],
                    "nl_basis": [],
                    "executable_spec": {"kind": "transition_shape", "source_label": "Idle"},
                    "binding_refs": [],
                    "required": True,
                },
            ]
        }
    )

    assert evaluated["execution_status"] == "completed"
    assert [item["draft_check_id"] for item in evaluated["binding_rejections"]] == [
        "draft-invalid-source-contract"
    ]
    assert evaluated["gate"]["eligible"] is False
    assert evaluated["gate"]["reasons"] == [
        "drafts_rejected_or_unbound:draft-invalid-source-contract"
    ]


def test_evaluate_checks_returns_structured_rejection_for_non_integer_property_bound():
    tool = {
        tool.name: tool
        for tool in registered_tools(unlock_fcstm=True, unlock_fbmcq=True)
    }["evaluate_checks"]
    evaluated = tool.invoke(
        {
            "checks": [
                {
                    "check_origin": "nl_grounded_behavioral_issue",
                    "check_id": "draft-invalid-bound",
                    "check_kind": "property",
                    "statement": "Done must be reached within the declared bound.",
                    "expected_outcome": {"property_satisfied": True},
                    "source_basis": [],
                    "nl_basis": [
                        {"quote": "Done is reached after go.", "role": "requirement"}
                    ],
                    "executable_spec": {
                        "kind": "must_reach",
                        "target_label": "Done",
                        "bound": {"upper": 3},
                    },
                    "binding_refs": [],
                    "required": True,
                }
            ]
        }
    )

    assert evaluated["execution_status"] == "invalid_arguments"
    assert evaluated["gate"]["eligible"] is False
    assert evaluated["binding_rejections"] == [
        {
            "draft_origin": "nl_grounded_behavioral_issue",
            "draft_check_id": "draft-invalid-bound",
            "reason": "property_bound_must_be_positive_integer",
            "observed_type": "dict",
        }
    ]


def test_root_issue_schema_rejects_candidate_repair_permission_before_publication():
    from pydantic import ValidationError

    from paper_stm_repair_loop.schemas import RootIssue

    with pytest.raises(ValidationError, match="candidate_only root cannot be repair eligible"):
        RootIssue.model_validate(
            {
                "node_id": "ISS-1@n0",
                "issue_id": "ISS-1",
                "assessment": "candidate_only",
                "downstream_repair_allowed": True,
                "statement": "Candidate only.",
                "rationale": "Source attribution is incomplete.",
                "required_check_ids": ["CHK-NL-001"],
            }
        )


@pytest.mark.parametrize(
    ("tool_name", "payload", "status"),
    [
        ("query_model", {"query_kind": "states", "offset": -1, "limit": 1}, "invalid_arguments"),
        ("observe_trace", {"events": [], "max_steps": 1}, "invalid_arguments"),
        ("observe_trace", {"events": ["Root.unknown"], "max_steps": 2}, "invalid_arguments"),
        ("lookup_source_trace", {"element_refs": [], "direction": "fcstm_to_source"}, "invalid_arguments"),
    ],
)
def test_tools_return_structured_failures_not_permission_or_exception_leaks(tool_name: str, payload: dict[str, Any], status: str):
    tools = {tool.name: tool for tool in registered_tools(unlock_fcstm=True)}
    if tool_name in {"observe_trace", "lookup_source_trace"}:
        evaluated = tools["evaluate_checks"].invoke(eligible_scenario_payload())
        assert evaluated["gate"]["eligible"] is True
    tool = tools[tool_name]
    result = tool.invoke(payload)
    assert result["execution_status"] == status
    serialized = json.dumps(result, ensure_ascii=False).lower()
    assert "/home/" not in serialized
    assert "traceback" not in serialized
    assert "reference" not in serialized or "reference/gold" not in serialized
