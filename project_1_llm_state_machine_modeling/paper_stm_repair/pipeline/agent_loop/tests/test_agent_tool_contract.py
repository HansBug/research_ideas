from __future__ import annotations

import inspect
import json

import pytest

from paper_stm_repair_loop.agents.discover import AGENT_TOOL_NAMES, _build_tools
from paper_stm_repair_loop.tools.coverage_registry import callable_docstring_has_required_sections

from v2_helpers import make_controller, make_plan


def _tools(tmp_path):
    controller = make_controller(tmp_path)
    controller.prepare()
    tools, _resolver = _build_tools(controller, controller.task_snapshot(), [])
    return controller, {tool.name: tool for tool in tools}


def test_agent_exposes_only_issue164_tools_with_strict_docstrings(tmp_path):
    _controller, tools = _tools(tmp_path)
    assert tuple(tools) == AGENT_TOOL_NAMES
    assert "evaluate_checks" not in tools
    for tool in tools.values():
        assert callable_docstring_has_required_sections(tool.func), tool.name
        assert inspect.getdoc(tool.func) == tool.description
        assert tool.args_schema.model_json_schema().get("additionalProperties") is False
        assert "reference/gold" in tool.description


def test_eval_assert_public_schema_and_supported_surface_are_exact(tmp_path):
    _controller, tools = _tools(tmp_path)
    schema = tools["eval_assert"].args_schema.model_json_schema()
    assert set(schema["properties"]) == {"assert", "reason"}
    description = tools["eval_assert"].description
    for marker in (
        "states",
        "transition_exists",
        "effect_delta",
        "effect_deltas",
        "simulate",
        "fbmcq",
        "mapped_source_refs",
        "is_leaf",
        "is_composite",
        "is_ended",
        "transition_index",
        "Positive bool principle",
        "required function families",
        "one registered latest",
        "inconclusive",
    ):
        assert marker in description


def test_tool_input_fields_match_issue164_contract(tmp_path):
    _controller, tools = _tools(tmp_path)
    fields = {
        name: set(tool.args_schema.model_json_schema()["properties"])
        for name, tool in tools.items()
    }
    assert fields == {
        "read_fcstm_guide": {"reason"},
        "read_fbmcq_guide": {"reason"},
        "read_task": {"reason"},
        "register_coverage_plan": {"plan", "reason"},
        "revise_assertion": {"assertion_chain_id", "assert", "reason"},
        "query_model": {
            "query_kind",
            "name_contains",
            "offset",
            "limit",
            "root_node_ids",
            "reason",
        },
        "eval_assert": {"assert", "reason"},
        "observe_trace": {"question", "root_node_ids", "cycles", "reason"},
        "lookup_source_trace": {"element_refs", "direction", "reason"},
        "review_discovery_coverage": {"reason"},
    }


def test_all_agent_tool_reasons_reject_whitespace_only_input(tmp_path):
    controller, tools = _tools(tmp_path)
    payloads = {
        "read_fcstm_guide": {"reason": "   "},
        "read_fbmcq_guide": {"reason": "   "},
        "read_task": {"reason": "   "},
        "register_coverage_plan": {"plan": make_plan(controller), "reason": "   "},
        "revise_assertion": {
            "assertion_chain_id": "ASSERT-001",
            "assert": "transition_exists(source='Root.Active', event='Root.Power_Off')",
            "reason": "   ",
        },
        "query_model": {"query_kind": "states", "reason": "   "},
        "eval_assert": {"assert": "states()", "reason": "   "},
        "observe_trace": {
            "question": "Observe one path.",
            "root_node_ids": ["ROOT-001"],
            "cycles": [[]],
            "reason": "   ",
        },
        "lookup_source_trace": {
            "element_refs": ["state:Root.Active"],
            "reason": "   ",
        },
        "review_discovery_coverage": {"reason": "   "},
    }

    assert set(payloads) == set(tools)
    for name, payload in payloads.items():
        with pytest.raises(ValueError, match="at least 1 character"):
            tools[name].args_schema.model_validate(payload)


def test_agent_tool_reasons_trim_surrounding_whitespace(tmp_path):
    _controller, tools = _tools(tmp_path)

    parsed = tools["read_fcstm_guide"].args_schema.model_validate(
        {"reason": "  Read the frozen FCSTM guide.  "}
    )

    assert parsed.reason == "Read the frozen FCSTM guide."


def test_tool_validation_feedback_names_missing_field(tmp_path):
    _controller, tools = _tools(tmp_path)

    result = json.loads(
        tools["revise_assertion"].invoke(
            {
                "assertion_chain_id": "ASSERT-001",
                "reason": "Revise the registered assertion from review feedback.",
            }
        )
    )

    assert result["execution_status"] == "invalid_arguments"
    assert result["missing_fields"] == ["assert"]
    assert result["errors"] == ["assert: Field required (missing)"]


def test_observe_trace_describes_only_post_registration_evidence_repair(tmp_path):
    _controller, tools = _tools(tmp_path)
    tools["read_fcstm_guide"].invoke(
        {"reason": "Read the required FCSTM guide before the tool contract test."}
    )
    tools["read_task"].invoke(
        {"reason": "Read the frozen task before the tool contract test."}
    )
    description = tools["observe_trace"].description
    assert "only after successful plan registration" in description
    assert "exact registered Root ID" in description
    assert "use this tool before registration" in description
    assert "provisional Root" not in description
    assert "runtime behavior is the proposition" in description
    assert "static relation alone" in description
    assert "composite, forced, completion, or pseudostate" in description

    result = tools["observe_trace"].invoke(
        {
            "question": "Does Power_Off move Active to Off?",
            "root_node_ids": ["ROOT-CLAUSE-001-01"],
            "cycles": [[], ["Root.Power_Off"]],
            "reason": "Resolve the exact review-directed cycle setup.",
        }
    )

    assert result["execution_status"] == "completed"
    assert result["recommended_tools"] == ["revise_assertion", "eval_assert"]
    assert "post-registration observation" in result["recommended_action"]
    assert "same stable Root ID" in result["pass_criteria"]

    duplicate = tools["observe_trace"].invoke(
        {
            "question": "Does Power_Off move Active to Off?",
            "root_node_ids": ["ROOT-CLAUSE-001-01"],
            "cycles": [[], ["Root.Power_Off"]],
            "reason": "Do not repeat an already completed trace.",
        }
    )
    assert duplicate["execution_status"] == "invalid_arguments"
    assert duplicate["limitations"] == ["duplicate_trace_request_not_executed"]
    assert "Do not repeat" in duplicate["recommended_action"]
    assert duplicate["pass_criteria"]

    suffixed = tools["observe_trace"].invoke(
        {
            "question": "Try to bypass the stable Root identity.",
            "root_node_ids": ["ROOT-CLAUSE-001-01B"],
            "cycles": [[], ["Root.Power_Off"]],
            "reason": "A suffix must not create a fresh exploration budget.",
        }
    )
    assert suffixed["execution_status"] == "invalid_arguments"
    assert suffixed["limitations"] == [
        "unstable_or_unknown_root_id",
        "ROOT-CLAUSE-001-01B",
    ]
    assert suffixed["allowed_root_ids"] == ["ROOT-CLAUSE-001-01"]
    assert "Do not add a suffix" in suffixed["recommended_action"]


def test_eval_assert_explains_relation_vs_runtime_behavior_evidence(tmp_path):
    _controller, tools = _tools(tmp_path)
    description = " ".join(tools["eval_assert"].description.split())

    assert "static source/event/target relation" in description
    assert "does not by itself prove the final runtime state" in description
    assert "composite, forced, completion, or pseudostate" in description
    assert "registered `simulate(...)` expression" in description
    assert "NL explicitly requires the direct relation itself" in description
    assert "reach the NL-stated source state" in description
    assert "actual function-call trace" in description
    assert "transition_exists(...) or simulate(...)" in description


def test_query_model_describes_only_post_registration_evidence_repair(tmp_path):
    _controller, tools = _tools(tmp_path)
    tools["read_fcstm_guide"].invoke(
        {"reason": "Read the required FCSTM guide before the tool contract test."}
    )
    tools["read_task"].invoke(
        {"reason": "Read the frozen task before the tool contract test."}
    )
    description = tools["query_model"].description
    assert "only after successful plan registration" in description
    assert "Do not use this tool before registration" in description
    assert "use ``[]`` only before Root IDs are registered" not in description
    arguments = {
        "query_kind": "transitions",
        "name_contains": "Power_Off",
        "offset": 0,
        "limit": 50,
        "root_node_ids": ["ROOT-CLAUSE-001-01"],
        "reason": "Resolve the exact transition named by a failed review.",
    }

    completed = tools["query_model"].invoke(arguments)
    assert completed["execution_status"] == "completed"
    assert completed["recommended_tools"] == ["revise_assertion", "eval_assert"]
    assert "registered assertion" in completed["recommended_action"]
    assert completed["pass_criteria"]

    duplicate = tools["query_model"].invoke(arguments)
    assert duplicate["execution_status"] == "invalid_arguments"
    assert "duplicate_query_not_executed" in duplicate["limitations"]
    assert "revise/evaluate the registered assertion" in duplicate["recommended_action"]


def test_fbmcq_guide_does_not_encourage_unnecessary_formal_assertions(tmp_path):
    _controller, tools = _tools(tmp_path)
    tools["read_fcstm_guide"].invoke(
        {"reason": "Read FCSTM semantics before the optional FBMCQ guide."}
    )
    tools["read_task"].invoke(
        {"reason": "Read the frozen task before deciding whether FBMCQ is needed."}
    )
    result = tools["read_fbmcq_guide"].invoke(
        {
            "reason": (
                "Read the bounded-property syntax only after identifying a "
                "necessary temporal obligation."
            )
        }
    )

    assert result["execution_status"] == "completed"
    assert "minimum sufficient plan" in result["recommended_action"]
    assert "explicit bounded temporal obligation" in result["pass_criteria"]
