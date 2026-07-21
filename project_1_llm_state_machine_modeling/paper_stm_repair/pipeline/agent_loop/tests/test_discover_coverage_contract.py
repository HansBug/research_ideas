from __future__ import annotations

import sys
import types

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


def _relation_env(value: bool = True):
    return {"transition_exists": lambda **_: value}


def _plan(assertion: str = "transition_exists(source='Root.Idle', event='Root.go', target='Root.Done')"):
    return {
        "coverage_units": [
            {
                "coverage_unit_id": "CU-001",
                "unit_kind": "behavior_obligation",
                "segment_ids": ["SEG-NL-001"],
                "source_fact_ids": ["FACT-TRANSITION-001"],
                "statement": "go reaches Done.",
            }
        ],
        "proposition_roots": [
            {
                "node_id": "ROOT-001",
                "coverage_unit_id": "CU-001",
                "statement": "The model represents go reaching Done.",
            }
        ],
        "logical_assertions": [
            {
                "assertion_chain_id": "ASSERT-001",
                "root_node_id": "ROOT-001",
                "coverage_unit_id": "CU-001",
                "required": True,
                "assert": assertion,
                "basis_ids": ["SEG-NL-001"],
                "evidence_scope": {"claim_strength": "transition_fact"},
                "required_function_families": ["relation"],
                "rationale": "Positive bool relation assertion.",
            }
        ],
    }


def test_register_plan_gates_segment_fact_unit_root_required_and_unique_latest_expression():
    registry = CoverageRegistry(
        input_segment_ids=["SEG-NL-001", "SEG-NL-002"],
        source_fact_ids=["FACT-TRANSITION-001"],
        eval_funcs=_relation_env(),
    )

    rejected = registry.register_plan(_plan(), reason="Missing SEG-NL-002 coverage should reject the whole plan.")

    assert rejected["execution_status"] == "invalid_arguments"
    assert rejected["accepted"] is False
    assert any("uncovered_input_segments:SEG-NL-002" in item for item in rejected["errors"])
    assert registry.plan_registered is False

    duplicate = _plan()
    duplicate["segment_dispositions"] = [
        {"segment_id": "SEG-NL-002", "disposition": "context_only", "rationale": "heading only"}
    ]
    duplicate["logical_assertions"].append(
        {
            **duplicate["logical_assertions"][0],
            "assertion_chain_id": "ASSERT-002",
        }
    )
    rejected_duplicate = registry.register_plan(duplicate, reason="Duplicate latest expressions are ambiguous.")

    assert rejected_duplicate["execution_status"] == "invalid_arguments"
    assert any("duplicate_latest_expression" in item for item in rejected_duplicate["errors"])
    assert registry.plan_registered is False

    accepted_plan = _plan()
    accepted_plan["segment_dispositions"] = [
        {"segment_id": "SEG-NL-002", "disposition": "context_only", "rationale": "heading only"}
    ]
    accepted = registry.register_plan(accepted_plan, reason="Register one unit/root/assertion with all coverage closed.")

    assert accepted["execution_status"] == "completed"
    assert accepted["coverage_plan_accepted"] is True
    assert accepted["registered_reference_closure"] is True
    assert accepted["registered_worklist_complete"] is False
    assert accepted["coverage_unit_count"] == 1
    assert accepted["root_count"] == 1
    assert accepted["assertion_chain_count"] == 1


def test_register_plan_rejects_agent_rewrite_of_controller_owned_segments_or_facts_and_bad_family():
    registry = CoverageRegistry(
        input_segment_ids=["SEG-NL-001"],
        source_fact_ids=["FACT-TRANSITION-001"],
        eval_funcs=_relation_env(),
    )
    plan = _plan()
    plan["input_segments"] = [{"segment_id": "SEG-NL-AGENT-REWRITE"}]
    plan["source_facts"] = [{"fact_id": "FACT-AGENT-REWRITE"}]
    plan["logical_assertions"][0]["required_function_families"] = ["fbmcq", "source_mapping"]

    rejected = registry.register_plan(plan, reason="Agent must not rewrite frozen Controller-owned inputs.")

    assert rejected["execution_status"] == "invalid_arguments"
    assert "controller_owned_fields_not_agent_writable:input_segments,source_facts" in rejected["errors"]
    assert "invalid_required_function_family:ASSERT-001:fbmcq,source_mapping" in rejected["errors"]
    assert registry.plan_registered is False


def test_revision_is_append_only_inherits_scope_and_failed_revision_preserves_old_latest():
    registry = CoverageRegistry(input_segment_ids=["SEG-NL-001"], source_fact_ids=["FACT-TRANSITION-001"], eval_funcs=_relation_env())
    assert registry.register_plan(_plan(), reason="Initial registration.")["execution_status"] == "completed"
    old_latest = registry.chains["ASSERT-001"][-1]
    new_expression = "transition_exists(source='Root.Idle', event='Root.go', target='Root.Done', guard=None)"

    revised = registry.revise_assertion("ASSERT-001", new_expression, reason="Narrow relation check without changing obligation.")

    assert revised["execution_status"] == "completed"
    assert revised["assertion_version_id"] == "ASSERT-001@v2"
    assert revised["inherited"]["required"] is True
    assert revised["inherited"]["root_node_id"] == old_latest.root_node_id
    assert revised["inherited"]["coverage_unit_id"] == old_latest.coverage_unit_id
    assert revised["inherited"]["basis_ids"] == list(old_latest.basis_ids)
    assert revised["inherited"]["evidence_scope"] == old_latest.evidence_scope
    assert revised["inherited"]["required_function_families"] == list(old_latest.required_function_families)
    assert registry.chains["ASSERT-001"][0].assert_text != registry.chains["ASSERT-001"][-1].assert_text

    same_rejected = registry.revise_assertion("ASSERT-001", new_expression, reason="Same latest should not append.")

    assert same_rejected["execution_status"] == "invalid_arguments"
    assert same_rejected["latest_preserved_assertion_version_id"] == "ASSERT-001@v2"
    assert registry.chains["ASSERT-001"][-1].assertion_version_id == "ASSERT-001@v2"


def test_submit_gate_blocks_until_every_latest_required_assertion_is_evaluated():
    registry = CoverageRegistry(input_segment_ids=["SEG-NL-001"], source_fact_ids=["FACT-TRANSITION-001"], eval_funcs=_relation_env())
    assert registry.register_plan(_plan(), reason="Initial registration.")["execution_status"] == "completed"
    blocked = registry.assert_submit_allowed()
    assert blocked["submit_allowed"] is False
    assert blocked["missing_latest_required_assertions"][0]["assertion_version_id"] == "ASSERT-001@v1"

    registry.eval_assert(_plan()["logical_assertions"][0]["assert"], reason="Evaluate the only required latest assertion.")
    allowed = registry.assert_submit_allowed()

    assert allowed["submit_allowed"] is False
    assert "current_semantic_coverage_review_must_pass" in allowed["limitations"]
    assert allowed["missing_latest_required_assertions"] == []

    class PassingReviewGate:
        latest_result = {"reviewed_state_fingerprint": "test", "record_id": "REC"}

        @staticmethod
        def current_passed():
            return True

    registry.semantic_review_gate = PassingReviewGate()
    assert registry.assert_submit_allowed()["submit_allowed"] is True

    registry.revise_assertion("ASSERT-001", "transition_exists(source='Root.Idle')", reason="Create a new latest version.")
    blocked_after_revision = registry.assert_submit_allowed()

    assert blocked_after_revision["submit_allowed"] is False
    assert blocked_after_revision["missing_latest_required_assertions"][0]["assertion_version_id"] == "ASSERT-001@v2"


def test_submit_gate_rejects_inconclusive_latest_assertion_after_execution():
    plan = _plan(assertion="True")
    registry = CoverageRegistry(
        input_segment_ids=["SEG-NL-001"],
        source_fact_ids=["FACT-TRANSITION-001"],
        eval_funcs=_relation_env(),
    )
    assert registry.register_plan(plan, reason="Register one deliberately inconclusive assertion.")["accepted"] is True
    evaluated = registry.eval_assert("True", reason="Bare True has no model evidence.")
    assert evaluated["match_status"] == "inconclusive"

    blocked = registry.assert_submit_allowed()

    assert blocked["submit_allowed"] is False
    assert blocked["incomplete_latest_required_assertions"][0]["assertion_version_id"] == "ASSERT-001@v1"
    assert "all_latest_required_assertions_must_be_terminal" in blocked["limitations"]


def test_controller_projection_prioritizes_incomplete_and_only_confirms_via_resolver():
    plan = _plan()
    plan["logical_assertions"].append(
        {
            **plan["logical_assertions"][0],
            "assertion_chain_id": "ASSERT-002",
            "assert": "True",
        }
    )
    registry = CoverageRegistry(
        input_segment_ids=["SEG-NL-001"],
        source_fact_ids=["FACT-TRANSITION-001"],
        eval_funcs=_relation_env(False),
        issue_assessment_resolver=lambda _root: ("confirmed", True),
    )
    assert registry.register_plan(plan, reason="Register contradictory and incomplete assertions.")["accepted"] is True
    first = registry.eval_assert(
        plan["logical_assertions"][0]["assert"], reason="Observe a real contradiction."
    )
    second = registry.eval_assert("True", reason="Bare true has no model evidence.")
    assert first["match_status"] == "contradicts"
    assert second["match_status"] == "inconclusive"

    outcome = registry.project_roots()

    assert outcome["run_outcome"] == "coverage_incomplete"
    assert outcome["registered_worklist_complete"] is False
    assert outcome["proposition_roots"][0]["status"] == "incomplete"
    assert outcome["issue_root_projection"] == []
    assert outcome["incomplete_root_projection"][0]["node_id"] == "ROOT-001"


def test_latest_assertion_version_preserves_multiple_attempts_and_projects_latest():
    registry = CoverageRegistry(
        input_segment_ids=["SEG-NL-001"],
        source_fact_ids=["FACT-TRANSITION-001"],
        eval_funcs=_relation_env(),
    )
    assert registry.register_plan(_plan(), reason="Register one assertion.")["accepted"] is True
    assert registry.eval_assert(
        _plan()["logical_assertions"][0]["assert"], reason="First execution."
    )["execution_status"] == "completed"
    duplicate = registry.eval_assert(
        _plan()["logical_assertions"][0]["assert"], reason="Duplicate execution."
    )
    assert duplicate["execution_status"] == "completed"
    assert len(registry.evaluations["ASSERT-001@v1"]) == 2
    assert registry.project_roots()["proposition_roots"][0]["status"] == "ok"


def test_supporting_fact_disposition_is_known_but_not_mandatory():
    registry = CoverageRegistry(
        input_segment_ids=["SEG-NL-001"],
        source_fact_ids=["FACT-TRANSITION-001"],
        known_source_fact_ids=[
            "FACT-TRANSITION-001",
            "FACT-DIAGNOSTIC-001",
        ],
        eval_funcs=_relation_env(),
    )
    plan = _plan()
    plan["fact_dispositions"] = [
        {
            "fact_id": "FACT-DIAGNOSTIC-001",
            "disposition": "diagnostic_support",
            "rationale": "The diagnostic is supporting evidence only.",
        }
    ]
    result = registry.register_plan(plan, reason="Register known supporting fact.")
    assert result["accepted"] is True
