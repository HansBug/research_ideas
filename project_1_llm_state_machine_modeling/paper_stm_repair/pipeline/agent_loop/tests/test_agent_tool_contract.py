from __future__ import annotations

import inspect
import json
import re

import pytest
from langchain_anthropic.chat_models import convert_to_anthropic_tool
from langchain_core.utils.function_calling import convert_to_openai_tool

from paper_stm_repair_loop.agents.discover import AGENT_TOOL_NAMES, _build_tools
from paper_stm_repair_loop.prompts.discover import system_prompt
from paper_stm_repair_loop.tools.coverage_registry import callable_docstring_has_required_sections

from v2_helpers import make_controller, make_plan


def _tools(tmp_path):
    controller = make_controller(tmp_path)
    controller.prepare()
    tools, _resolver = _build_tools(controller, controller.task_snapshot(), [])
    return controller, {tool.name: tool for tool in tools}


def test_agent_exposes_only_issue165_tools_with_strict_docstrings(tmp_path):
    _controller, tools = _tools(tmp_path)
    assert tuple(tools) == AGENT_TOOL_NAMES
    assert "evaluate_checks" not in tools
    for tool in tools.values():
        assert callable_docstring_has_required_sections(tool.func), tool.name
        assert inspect.getdoc(tool.func) == tool.description
        assert tool.args_schema.model_json_schema().get("additionalProperties") is False
        assert "reference/gold" in tool.description


def test_all_model_visible_protocol_text_remains_english(tmp_path):
    cjk = re.compile(r"[\u3400-\u9fff]")
    _controller, tools = _tools(tmp_path)

    assert cjk.search(system_prompt("zh-CN")) is None
    assert cjk.search(system_prompt("en-US")) is None
    assert all(cjk.search(tool.description) is None for tool in tools.values())


def test_non_formal_profile_hides_guide_and_fbmcq_runtime(tmp_path):
    controller = make_controller(tmp_path)
    controller.manifest["formal_profile"] = False
    controller.prepare()
    tools, resolver = _build_tools(controller, controller.task_snapshot(), [])
    names = tuple(tool.name for tool in tools)

    assert "read_fbmcq_guide" not in names
    environment = controller.require_registry().eval_runtime.environment
    assert "fbmcq" not in environment.locals
    by_name = {tool.name: tool for tool in tools}
    by_name["read_fcstm_guide"].invoke({"reason": "Read FCSTM semantics."})
    by_name["read_task"].invoke({"reason": "Read the frozen non-formal task."})
    assert resolver() is None


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
        "requested_initialization",
        "effective_initialization",
        "first hot-start caller cycle",
        "consumed_events",
        "unconsumed_events",
        "same supplied event may appear more than once",
        "count of exactly one",
        "final-state coincidence",
        "transition_index",
        "Positive bool principle",
        "required function families",
        "one registered latest",
        "inconclusive",
    ):
        assert marker in description


def test_tool_input_fields_match_issue165_contract(tmp_path):
    _controller, tools = _tools(tmp_path)
    fields = {
        name: set(tool.args_schema.model_json_schema()["properties"])
        for name, tool in tools.items()
    }
    assert fields == {
        "read_fcstm_guide": {"reason"},
        "read_fbmcq_guide": {"reason"},
        "read_task": {"reason"},
        "inspect_model": {"reason"},
        "register_coverage_plan": {"plan", "reason"},
        "revise_assertion": {
            "assertion_chain_id",
            "assert",
            "formal_property_kind",
            "formal_bound",
            "formal_bound_origin",
            "formal_assumption_basis_ids",
            "required_function_families",
            "reason",
        },
        "query_model": {
            "query_kind",
            "operation",
            "name_contains",
            "exact",
            "path",
            "within",
            "parent",
            "recursive",
            "kind",
            "name",
            "scope",
            "declared",
            "used",
            "variable_type",
            "read_in",
            "written_in",
            "source",
            "event",
            "target",
            "has_event",
            "has_guard",
            "has_effect",
            "forced",
            "self_loop",
            "source_within",
            "target_within",
            "avoid",
            "max_hops",
            "offset",
            "limit",
            "root_node_ids",
            "reason",
        },
        "eval_assert": {"assert", "reason"},
        "observe_trace": {
            "question",
            "root_node_ids",
            "cycles",
            "initial_state",
            "initial_vars",
            "reason",
        },
        "lookup_source_trace": {"element_refs", "direction", "reason"},
        "review_discovery_coverage": {"reason"},
    }


@pytest.mark.parametrize(
    ("tool_name", "expected_fields", "required_fields"),
    [
        ("eval_assert", {"assert", "reason"}, {"assert", "reason"}),
        (
            "revise_assertion",
            {
                "assertion_chain_id",
                "assert",
                "formal_property_kind",
                "formal_bound",
                    "formal_bound_origin",
                    "formal_assumption_basis_ids",
                    "required_function_families",
                    "reason",
            },
            {"assertion_chain_id", "assert", "reason"},
        ),
    ],
)
def test_provider_schemas_preserve_keyword_named_assert_field(
    tmp_path, tool_name, expected_fields, required_fields
):
    _controller, tools = _tools(tmp_path)
    tool = tools[tool_name]

    openai_schema = convert_to_openai_tool(tool)["function"]["parameters"]
    anthropic_schema = convert_to_anthropic_tool(tool)["input_schema"]

    for schema in (openai_schema, anthropic_schema):
        assert set(schema["properties"]) == expected_fields
        assert set(schema["required"]) == required_fields


def test_all_agent_tool_reasons_reject_whitespace_only_input(tmp_path):
    controller, tools = _tools(tmp_path)
    payloads = {
        "read_fcstm_guide": {"reason": "   "},
        "read_fbmcq_guide": {"reason": "   "},
        "read_task": {"reason": "   "},
        "inspect_model": {"reason": "   "},
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
    action = result["required_actions"][0]["recommended_action"]
    assert "top-level JSON key" in action
    assert "inside `reason` does not fill another field" in action
    assert "top-level `assert` key" in action


def test_observe_trace_supports_targeted_pre_registration_investigation(tmp_path):
    _controller, tools = _tools(tmp_path)
    tools["read_fcstm_guide"].invoke(
        {"reason": "Read the required FCSTM guide before the tool contract test."}
    )
    tools["read_task"].invoke(
        {"reason": "Read the frozen task before the tool contract test."}
    )
    tools["read_fbmcq_guide"].invoke(
        {"reason": "Read formal capability before planning."}
    )
    description = tools["observe_trace"].description
    assert "targeted provisional clause Root" in description
    assert "before registration" in description
    assert "A complete hot start does not" in description
    assert "put E in the first hot-start" in description
    assert "Final-state equality alone does not prove" in description
    assert "input/consumed/unconsumed events" in description

    result = tools["observe_trace"].invoke(
        {
            "question": "Does Power_Off move Active to Off?",
            "root_node_ids": ["ROOT-CLAUSE-001-01"],
            "cycles": [[], ["Root.Power_Off"]],
            "reason": "Resolve the exact review-directed cycle setup.",
        }
    )

    assert result["execution_status"] == "completed"
    assert result["recommended_tools"] == ["register_coverage_plan"]
    assert "pre-registration observation" in result["recommended_action"]
    assert "complete plan" in result["pass_criteria"]

    duplicate = tools["observe_trace"].invoke(
        {
            "question": "Does Power_Off move Active to Off?",
            "root_node_ids": ["ROOT-CLAUSE-001-01"],
            "cycles": [[], ["Root.Power_Off"]],
            "reason": "Do not repeat an already completed trace.",
        }
    )
    assert duplicate["execution_status"] == "mandatory_tool_rejected"
    assert duplicate["required_tool"] == "register_coverage_plan"
    assert duplicate["required_actions"][0]["recommended_tools"] == [
        "register_coverage_plan"
    ]
    assert duplicate["required_actions"][0]["pass_criteria"]

    _controller2, tools2 = _tools(tmp_path / "unstable-root")
    tools2["read_fcstm_guide"].invoke(
        {"reason": "Read the required FCSTM guide before checking Root identity."}
    )
    tools2["read_task"].invoke(
        {"reason": "Read the frozen task before checking Root identity."}
    )
    tools2["read_fbmcq_guide"].invoke(
        {"reason": "Read formal capability before checking Root identity."}
    )
    suffixed = tools2["observe_trace"].invoke(
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

    assert "static model relation" in description
    assert "does not by itself observe the final runtime state" in description
    assert "Use simulation instead" in description
    assert "NL asks what behavior occurs after a trigger" in description


def test_query_model_supports_targeted_pre_registration_investigation(tmp_path):
    _controller, tools = _tools(tmp_path)
    tools["read_fcstm_guide"].invoke(
        {"reason": "Read the required FCSTM guide before the tool contract test."}
    )
    tools["read_task"].invoke(
        {"reason": "Read the frozen task before the tool contract test."}
    )
    tools["read_fbmcq_guide"].invoke(
        {"reason": "Read formal capability before planning."}
    )
    description = tools["query_model"].description
    assert "targeted" in description
    assert "provisional clause/Root" in description
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
    assert completed["recommended_tools"] == ["register_coverage_plan"]
    assert "pre-registration fact" in completed["recommended_action"]
    assert completed["pass_criteria"]

    duplicate = tools["query_model"].invoke(arguments)
    assert duplicate["execution_status"] == "mandatory_tool_rejected"
    assert duplicate["required_tool"] == "register_coverage_plan"
    assert duplicate["required_actions"][0]["recommended_tools"] == [
        "register_coverage_plan"
    ]


def test_fbmcq_guide_normalizes_capability_without_tool_quota(tmp_path):
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
    assert "An explicit NL bound is not required" in result["recommended_action"]
    assert "does not require later FBMCQ use" in tools["read_fbmcq_guide"].description
