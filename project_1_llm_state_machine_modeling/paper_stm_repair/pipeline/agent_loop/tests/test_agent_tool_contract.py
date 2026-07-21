from __future__ import annotations

import inspect

from paper_stm_repair_loop.agents.discover import AGENT_TOOL_NAMES, _build_tools
from paper_stm_repair_loop.tools.coverage_registry import callable_docstring_has_required_sections

from v2_helpers import make_controller


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


def test_observe_trace_guides_the_agent_back_to_plan_or_assertion_progress(tmp_path):
    _controller, tools = _tools(tmp_path)
    tools["read_fcstm_guide"].invoke(
        {"reason": "Read the required FCSTM guide before the tool contract test."}
    )
    tools["read_task"].invoke(
        {"reason": "Read the frozen task before the tool contract test."}
    )
    description = tools["observe_trace"].description
    assert "one stable provisional Root ID" in description
    assert "never mint suffix variants or new IDs" in description
    assert "model-wide pre-plan trace sweep" in description

    result = tools["observe_trace"].invoke(
        {
            "question": "Does Power_Off move Active to Off?",
            "root_node_ids": ["ROOT-CLAUSE-001-01"],
            "cycles": [[], ["Root.Power_Off"]],
            "reason": "Resolve the exact cycle setup before registration.",
        }
    )

    assert result["execution_status"] == "completed"
    assert result["recommended_tools"] == [
        "register_coverage_plan",
        "revise_assertion",
        "eval_assert",
    ]
    assert "Do not enumerate unrelated" in result["recommended_action"]
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
    assert suffixed["allowed_provisional_root_ids"] == ["ROOT-CLAUSE-001-01"]
    assert "Do not add a suffix" in suffixed["recommended_action"]


def test_query_model_guides_completed_and_rejected_calls_toward_progress(tmp_path):
    _controller, tools = _tools(tmp_path)
    tools["read_fcstm_guide"].invoke(
        {"reason": "Read the required FCSTM guide before the tool contract test."}
    )
    tools["read_task"].invoke(
        {"reason": "Read the frozen task before the tool contract test."}
    )
    arguments = {
        "query_kind": "transitions",
        "name_contains": "Power_Off",
        "offset": 0,
        "limit": 50,
        "root_node_ids": ["ROOT-CLAUSE-001-01"],
        "reason": "Resolve the exact transition before registration.",
    }

    completed = tools["query_model"].invoke(arguments)
    assert completed["execution_status"] == "completed"
    assert "Do not issue adjacent" in completed["recommended_action"]
    assert completed["pass_criteria"]

    duplicate = tools["query_model"].invoke(arguments)
    assert duplicate["execution_status"] == "invalid_arguments"
    assert "duplicate_query_not_executed" in duplicate["limitations"]
    assert "proceed to plan registration" in duplicate["recommended_action"]


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
