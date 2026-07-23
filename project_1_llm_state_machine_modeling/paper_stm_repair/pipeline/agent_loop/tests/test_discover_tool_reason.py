from __future__ import annotations

from paper_stm_repair_loop.tools.coverage_registry import CoverageRegistry
from paper_stm_repair_loop.tools.eval_assert import build_tool as build_eval_assert_tool
from paper_stm_repair_loop.tools.register_coverage_plan import build_tool as build_register_coverage_plan_tool
from paper_stm_repair_loop.tools.revise_assertion import build_tool as build_revise_assertion_tool


ASSERT_TEXT = "transition_exists(source='Root.Idle', event='Root.go', target='Root.Done')"


def _registry() -> CoverageRegistry:
    return CoverageRegistry(
        input_segment_ids=["SEG-NL-001"],
        source_fact_ids=["FACT-TRANSITION-001"],
        eval_funcs={"transition_exists": lambda **_: True},
        model_sha256="model-sha",
    )


def _plan(assert_text: str = ASSERT_TEXT) -> dict[str, object]:
    return {
        "coverage_units": [
            {
                "coverage_unit_id": "CU-001",
                "unit_kind": "behavior_obligation",
                "segment_ids": ["SEG-NL-001"],
                "source_fact_ids": ["FACT-TRANSITION-001"],
                "statement": "go reaches Done.",
                "rationale": "One independently repairable behavior obligation.",
            }
        ],
        "segment_dispositions": [],
        "fact_dispositions": [],
        "proposition_roots": [
            {
                "node_id": "ROOT-001",
                "coverage_unit_id": "CU-001",
                "statement": "The model represents go reaching Done.",
                "rationale": "Root for CU-001.",
            }
        ],
        "logical_assertions": [
            {
                "assertion_chain_id": "ASSERT-001",
                "root_node_id": "ROOT-001",
                "coverage_unit_id": "CU-001",
                "required": True,
                "assert": assert_text,
                "basis_ids": ["SEG-NL-001"],
                "obligation_signature": "go-reaches-done",
                "required_function_families": ["relation"],
                "evidence_scope": {
                    "semantic_profile": "single_active_leaf_fcstm_v1",
                    "max_steps": None,
                    "max_time": None,
                    "abstraction": "discrete_event",
                    "claim_strength": "transition_fact",
                },
                "rationale": "Positive relation assertion.",
            }
        ],
        "rationale": "Complete registered coverage for the fixture.",
    }


def test_new_agent_facing_tools_have_required_docstring_sections_and_reason_parameters():
    registry = _registry()
    tools = [
        build_register_coverage_plan_tool(registry),
        build_revise_assertion_tool(registry),
        build_eval_assert_tool(registry),
    ]
    required_sections = [
        "Purpose",
        "When to use",
        "When not to use",
        "Parameters",
        "Returns",
        "Execution",
        "Failure semantics",
        "Evidence limitations",
        "Permissions",
        "Examples",
    ]

    for tool in tools:
        description = str(tool.description)
        for section in required_sections:
            assert section in description, f"{tool.name} missing {section}"
        schema = tool.args_schema.model_json_schema()
        assert schema["additionalProperties"] is False
        assert "reason" in schema["properties"]

    assert set(tools[0].args_schema.model_json_schema()["properties"]) == {"plan", "reason"}
    assert set(tools[1].args_schema.model_json_schema()["properties"]) == {
        "assertion_chain_id",
        "assert",
        "formal_property_kind",
        "formal_bound",
        "formal_bound_origin",
        "formal_assumption_basis_ids",
        "required_function_families",
        "reason",
    }
    assert set(tools[2].args_schema.model_json_schema()["properties"]) == {"assert", "reason"}


def test_tool_reasons_are_saved_and_eval_exports_machine_reason_context():
    registry = _registry()
    register_reason = "Register the only behavior unit without rewriting Controller-owned facts."
    revision_reason = "Revise expression while inheriting relation family and basis."
    eval_reason = "Evaluate the exact latest assertion for ROOT-001."

    registered = build_register_coverage_plan_tool(registry).invoke({"plan": _plan(), "reason": register_reason})
    assert registered["execution_status"] == "completed"
    assert registry.records[-1]["payload"]["reason"] == register_reason

    revised = build_revise_assertion_tool(registry).invoke(
        {
            "assertion_chain_id": "ASSERT-001",
            "assert": "transition_exists(source='Root.Idle', event='Root.go', target='Root.Done', guard=None)",
            "reason": revision_reason,
        }
    )
    assert revised["execution_status"] == "completed"
    assert registry.records[-1]["payload"]["reason"] == revision_reason

    evaluated = build_eval_assert_tool(registry).invoke(
        {
            "assert": "transition_exists(source='Root.Idle', event='Root.go', target='Root.Done', guard=None)",
            "reason": eval_reason,
        }
    )
    assert evaluated["execution_status"] == "completed"
    assert evaluated["reason"] == eval_reason
    assert evaluated["reason_context"]["related_segment_ids"] == ["SEG-NL-001"]
    assert evaluated["reason_context"]["related_coverage_unit_ids"] == ["CU-001"]
    assert evaluated["reason_context"]["related_root_node_ids"] == ["ROOT-001"]
    assert evaluated["reason_context"]["related_assertion_chain_ids"] == ["ASSERT-001"]
    assert evaluated["reason_context"]["assert_sha256"] == revised["assert_sha256"]


def test_revise_assertion_tool_forwards_replacement_function_families():
    registry = _registry()
    build_register_coverage_plan_tool(registry).invoke(
        {"plan": _plan(), "reason": "Register the fixture."}
    )
    revised = build_revise_assertion_tool(registry).invoke(
        {
            "assertion_chain_id": "ASSERT-001",
            "assert": (
                "transition_exists(source='Root.Idle', event='Root.go', "
                "target='Root.Done') and "
                "simulate(initial_state='Root.Idle', initial_vars={}, "
                "cycles=[['Root.go']]).final.is_active('Root.Done')"
            ),
            "required_function_families": ["relation", "simulation"],
            "reason": "Replace the static-only route with runtime evidence.",
        }
    )

    assert revised["accepted"] is True
    assert revised["inherited"]["required_function_families"] == [
        "relation",
        "simulation",
    ]
    assert revised["inherited"]["required_function_families_changed"] is True
