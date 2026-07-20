from __future__ import annotations

import sys
import types

import pytest

if "utils.agent" not in sys.modules:
    utils_pkg = types.ModuleType("utils")
    utils_pkg.__path__ = []
    agent_mod = types.ModuleType("utils.agent")
    agent_mod.AgentApp = object
    agent_mod.AgentSpec = object
    llm_mod = types.ModuleType("utils.llm")
    llm_mod.LLMRegistry = object
    llm_mod.load_llm_registry = lambda *_, **__: None
    sys.modules.update({"utils": utils_pkg, "utils.agent": agent_mod, "utils.llm": llm_mod})

from paper_stm_repair_loop.tools.coverage_registry import CoverageRegistry
from paper_stm_repair_loop.tools.eval_assert import build_tool as build_eval_assert_tool


ASSERT_TEXT = "transition_exists(source='Root.Idle', event='Root.go', target='Root.Done')"


def _registered_registry(*, relation_value: bool = True) -> CoverageRegistry:
    registry = CoverageRegistry(
        input_segment_ids=["SEG-NL-001"],
        source_fact_ids=["FACT-TRANSITION-001"],
        eval_funcs={"transition_exists": lambda **_: relation_value},
        model_sha256="model-sha",
    )
    result = registry.register_plan(
        {
            "coverage_units": [
                {
                    "coverage_unit_id": "CU-001",
                    "segment_ids": ["SEG-NL-001"],
                    "source_fact_ids": ["FACT-TRANSITION-001"],
                    "statement": "go reaches Done.",
                }
            ],
            "proposition_roots": [{"node_id": "ROOT-001", "coverage_unit_id": "CU-001"}],
            "logical_assertions": [
                {
                    "assertion_chain_id": "ASSERT-001",
                    "root_node_id": "ROOT-001",
                    "coverage_unit_id": "CU-001",
                    "required": True,
                    "assert": ASSERT_TEXT,
                    "basis_ids": ["SEG-NL-001"],
                    "required_function_families": ["relation"],
                    "evidence_scope": {"claim_strength": "transition_fact"},
                }
            ],
        },
        reason="Register exact latest assertion.",
    )
    assert result["execution_status"] == "completed"
    return registry


def test_eval_assert_public_schema_is_strict_assert_reason_only():
    tool = build_eval_assert_tool(_registered_registry())
    schema = tool.args_schema.model_json_schema()

    assert schema["additionalProperties"] is False
    assert set(schema["properties"]) == {"assert", "reason"}

    with pytest.raises(Exception):
        tool.invoke({"assert": ASSERT_TEXT, "reason": "One assertion.", "id": "ASSERT-001"})
    with pytest.raises(Exception):
        tool.invoke({"assert": [ASSERT_TEXT], "reason": "No arrays."})
    with pytest.raises(Exception):
        tool.invoke({"batch": [ASSERT_TEXT], "reason": "No batch."})


def test_eval_assert_matches_exactly_one_unique_latest_expression_and_exports_reason_context():
    registry = _registered_registry(relation_value=False)
    tool = build_eval_assert_tool(registry)
    reason = "ROOT-001 evaluates the registered positive transition relation."

    unknown = tool.invoke({"assert": "transition_exists(source='Root.Missing')", "reason": "Unregistered expression."})
    assert unknown["execution_status"] == "invalid_arguments"
    assert unknown["match_count"] == 0
    assert "assert_must_match_exactly_one_latest_registered_expression" in unknown["limitations"]

    result = tool.invoke({"assert": ASSERT_TEXT, "reason": reason})

    assert result["execution_status"] == "completed"
    assert result["match_status"] == "contradicts"
    assert result["python_value_type"] == "bool"
    assert result["python_value"] is False
    assert result["reason"] == reason
    assert result["assertion_chain_id"] == "ASSERT-001"
    assert result["reason_context"] == {
        "phase": "assertion_execution",
        "related_segment_ids": ["SEG-NL-001"],
        "related_coverage_unit_ids": ["CU-001"],
        "related_root_node_ids": ["ROOT-001"],
        "related_assertion_chain_ids": ["ASSERT-001"],
        "related_assertion_version_ids": ["ASSERT-001@v1"],
        "assert_sha256": result["assert_sha256"],
        "expected_fact_kind": "assertion_result",
    }
    assert result["record_id"].startswith("LOCAL-REC-")


def test_eval_assert_failed_runtime_keeps_structured_record_and_family_gate():
    registry = _registered_registry(relation_value=True)
    registry.revise_assertion("ASSERT-001", "True", reason="Bad revision with no evidence.")
    no_evidence = registry.eval_assert("True", reason="This should not become evidence.")

    assert no_evidence["execution_status"] == "inconclusive"
    assert no_evidence["match_status"] == "inconclusive"
    assert "no_model_evidence" in no_evidence["limitations"]

    registry.revise_assertion("ASSERT-001", "len(states()) >= 1", reason="Uses structure while relation remains required.")
    registry.eval_runtime.funcs["states"] = lambda **_: [{"qualified_name": "Root.Idle"}]  # type: ignore[attr-defined]
    missing_family = registry.eval_assert("len(states()) >= 1", reason="Missing relation family should gate off.")

    assert missing_family["execution_status"] == "inconclusive"
    assert "required_function_family_not_observed" in missing_family["limitations"]
    assert "relation" in missing_family["limitations"]
    assert missing_family["function_calls"][0]["function_name"] == "states"
