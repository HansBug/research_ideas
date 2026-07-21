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
