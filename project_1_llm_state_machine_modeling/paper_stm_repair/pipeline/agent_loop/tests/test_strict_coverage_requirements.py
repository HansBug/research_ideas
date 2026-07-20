from __future__ import annotations

from paper_stm_repair_loop.coverage_requirements import build_coverage_requirements
from paper_stm_repair_loop.nl_segmenter import segment_nl
from paper_stm_repair_loop.schemas.assertions import EvalAssertResult
from paper_stm_repair_loop.schemas.coverage import InputSegment
from paper_stm_repair_loop.tools.coverage_registry import (
    CoverageRegistry,
    _assertion_directly_verifies_source_fact,
    _registration_required_actions,
)


def _requirements(text: str):
    segments = tuple(
        InputSegment.model_validate(item) for item in segment_nl(text).segments
    )
    return segments, build_coverage_requirements(segments)


def _plan(requirement_id: str, *, family: str = "effect"):
    return {
        "segment_dispositions": [],
        "fact_dispositions": [],
        "coverage_units": [
            {
                "coverage_unit_id": "CU-001",
                "unit_kind": "behavior_obligation",
                "segment_ids": ["SEG-NL-001"],
                "source_fact_ids": [],
                "requirement_ids": [requirement_id],
                "dimensions": ["effect"],
                "statement": "Attack completion decreases the UAV count.",
                "rationale": "One independently repairable effect obligation.",
            }
        ],
        "proposition_roots": [
            {
                "node_id": "ROOT-001",
                "coverage_unit_id": "CU-001",
                "statement": "Attack completion decreases the UAV count.",
                "model_element_refs": [],
                "source_element_refs": ["SEG-NL-001"],
                "rationale": "Positive effect query for the required update.",
            }
        ],
        "logical_assertions": [
            {
                "assertion_chain_id": "ASSERT-001",
                "root_node_id": "ROOT-001",
                "coverage_unit_id": "CU-001",
                "required": True,
                "assert": "(effect_delta(source='Root.Attack', event='Root.Attack_Complete', variable='uav_count') or 0) < 0",
                "basis_ids": ["SEG-NL-001", requirement_id],
                "obligation_signature": "attack-complete-uav-count-decrease",
                "required_function_families": [family],
                "evidence_scope": {
                    "semantic_profile": "single_active_leaf_fcstm_v1",
                    "max_steps": None,
                    "max_time": None,
                    "abstraction": "discrete_event",
                    "claim_strength": "deterministic_effect_fact",
                },
                "rationale": "True means the required decrement is represented.",
            }
        ],
        "rationale": "Issue-agnostic Controller-frozen coverage plan.",
    }


def _strict_registry_and_plan():
    _, requirements = _requirements(
        "After completing the attack, the UAV count decreases."
    )
    effect = next(item for item in requirements if item.dimension == "effect")
    fact_id = "FACT-TRANSITION-001"
    registry = CoverageRegistry(
        input_segment_ids=["SEG-NL-001"],
        coverage_requirements={effect.requirement_id: effect.model_dump(mode="json")},
        source_fact_ids=[fact_id],
        known_source_fact_ids=[fact_id],
        source_fact_kinds={fact_id: "transition"},
        source_fact_details={
            fact_id: {
                "fact_id": fact_id,
                "fact_kind": "transition",
                "qualified_refs": ["transition:1"],
                "source": "Root.Attack",
                "event": "Root.Attack_Complete",
                "target": "Root.Searching",
                "guard": None,
                "effects": [],
            }
        },
        eval_funcs={
            "effect_delta": lambda **_: -1,
            "transition_exists": lambda **_: True,
        },
    )
    plan = _plan(effect.requirement_id)
    plan["coverage_units"][0]["source_fact_ids"] = [fact_id]
    plan["logical_assertions"].append(
        {
            "assertion_chain_id": "ASSERT-SOURCE-001",
            "root_node_id": "ROOT-001",
            "coverage_unit_id": "CU-001",
            "required": True,
            "assert": "transition_exists(source='Root.Attack', event='Root.Attack_Complete', target='Root.Searching')",
            "basis_ids": [fact_id],
            "obligation_signature": "source-transition-exact-audit",
            "required_function_families": ["relation"],
            "evidence_scope": {
                "semantic_profile": "single_active_leaf_fcstm_v1",
                "max_steps": None,
                "max_time": None,
                "abstraction": "discrete_event",
                "claim_strength": "exact_source_transition_fact",
            },
            "rationale": "Directly audit the complete source transition tuple.",
        }
    )
    return registry, plan, effect.requirement_id


def test_0006_style_atomizer_detects_compound_dimensions_without_taxonomy():
    text = (
        "1 This state machine model describes a UAV swarm.\n"
        "2 Before the mission is completed, it continuously searches three different areas.\n"
        "3 After completing the attack, the UAV count decreases."
    )
    segments, requirements = _requirements(text)
    assert len(segments) == 3
    assert not [item for item in requirements if item.segment_id == "SEG-NL-001"]
    assert {item.dimension for item in requirements} == {
        "behavior",
        "structure",
        "cardinality",
        "ordering",
        "continuity",
        "completion",
        "effect",
    }
    assert not any(item.cue_text in {"1", "2", "3"} for item in requirements)
    assert all("defect_family_ids" not in item.model_dump() for item in requirements)


def test_every_non_meta_clause_and_repeated_cue_gets_a_hard_row():
    _, requirements = _requirements(
        "When Alarm occurs, the valve shall close; when Reset occurs, the valve shall open."
    )
    assert len({item.clause_id for item in requirements}) == 2
    assert len([item for item in requirements if item.dimension == "behavior"]) == 2
    assert {
        item.cue_text.lower() for item in requirements if item.dimension == "transition"
    } == {"close", "open"}
    assert len([item for item in requirements if item.dimension == "condition"]) == 2


def test_strict_registry_rejects_missing_requirement():
    _, requirements = _requirements(
        "After completing the attack, the UAV count decreases."
    )
    effect = next(item for item in requirements if item.dimension == "effect")
    registry = CoverageRegistry(
        input_segment_ids=["SEG-NL-001"],
        coverage_requirements={effect.requirement_id: effect.model_dump(mode="json")},
        eval_funcs={"effect_delta": lambda **_: -1},
    )
    plan = _plan(effect.requirement_id)
    plan["coverage_units"][0]["requirement_ids"] = []
    rejected = registry.register_plan(plan, reason="Missing hard coverage row.")
    assert rejected["accepted"] is False
    assert any(
        item.startswith("uncovered_coverage_requirements:")
        for item in rejected["errors"]
    )


def test_strict_registry_rejects_wrong_evidence_family():
    _, requirements = _requirements(
        "After completing the attack, the UAV count decreases."
    )
    effect = next(item for item in requirements if item.dimension == "effect")
    registry = CoverageRegistry(
        input_segment_ids=["SEG-NL-001"],
        coverage_requirements={effect.requirement_id: effect.model_dump(mode="json")},
        eval_funcs={"transition_exists": lambda **_: True},
    )
    rejected = registry.register_plan(
        _plan(effect.requirement_id, family="relation"),
        reason="Wrong evidence route.",
    )
    assert rejected["accepted"] is False
    assert any(
        item.startswith("coverage_requirement_evidence_family_unsatisfied:")
        for item in rejected["errors"]
    )


def test_strict_registry_accepts_closed_requirement_and_assertion_route():
    _, requirements = _requirements(
        "After completing the attack, the UAV count decreases."
    )
    effect = next(item for item in requirements if item.dimension == "effect")
    registry = CoverageRegistry(
        input_segment_ids=["SEG-NL-001"],
        coverage_requirements={effect.requirement_id: effect.model_dump(mode="json")},
        eval_funcs={"effect_delta": lambda **_: -1},
    )
    plan = _plan(effect.requirement_id)
    accepted = registry.register_plan(plan, reason="Close every strict row.")
    assert accepted["accepted"] is True
    assert accepted["strict_coverage_certificate"] == {
        "status": "registered_pending_execution",
        "coverage_requirement_total": 1,
        "coverage_requirement_covered": 1,
    }
    evaluated = registry.eval_assert(
        plan["logical_assertions"][0]["assert"],
        reason="Execute the effect assertion.",
    )
    assert EvalAssertResult.model_validate(evaluated).match_status == "matches"


def test_behavior_source_fact_cannot_be_closed_by_disposition_only():
    _, requirements = _requirements(
        "After completing the attack, the UAV count decreases."
    )
    effect = next(item for item in requirements if item.dimension == "effect")
    registry = CoverageRegistry(
        input_segment_ids=["SEG-NL-001"],
        coverage_requirements={effect.requirement_id: effect.model_dump(mode="json")},
        source_fact_ids=["FACT-TRANSITION-001"],
        known_source_fact_ids=["FACT-TRANSITION-001"],
        source_fact_kinds={"FACT-TRANSITION-001": "transition"},
        eval_funcs={"effect_delta": lambda **_: -1},
    )
    plan = _plan(effect.requirement_id)
    plan["fact_dispositions"] = [
        {
            "fact_id": "FACT-TRANSITION-001",
            "disposition": "implementation_support",
            "rationale": "Attempt to bypass executable source-fact coverage.",
        }
    ]
    rejected = registry.register_plan(plan, reason="Behavior fact bypass attempt.")
    assert rejected["accepted"] is False
    assert any(
        item.startswith("behavior_source_facts_cannot_be_dispositioned:")
        for item in rejected["errors"]
    )


def test_requirement_must_be_direct_assertion_basis_not_only_unit_metadata():
    registry, plan, requirement_id = _strict_registry_and_plan()
    plan["logical_assertions"][0]["basis_ids"] = ["SEG-NL-001"]
    rejected = registry.register_plan(plan, reason="Omit requirement basis.")
    assert rejected["accepted"] is False
    assert (
        f"coverage_requirement_assertion_basis_missing:{requirement_id}"
        in rejected["errors"]
    )


def test_behavior_source_fact_requires_direct_compatible_assertion_binding():
    registry, plan, _ = _strict_registry_and_plan()
    plan["logical_assertions"][1]["assert"] = (
        "transition_exists(source='Root.Other', event='Root.other', target='Root.Done')"
    )
    rejected = registry.register_plan(plan, reason="Use unrelated fact predicate.")
    assert rejected["accepted"] is False
    assert "source_fact_not_directly_verified:FACT-TRANSITION-001" in rejected["errors"]
    action = next(
        item
        for item in rejected["required_actions"]
        if item["related_ids"] == ["FACT-TRANSITION-001"]
    )
    assert action["recommended_tools"] == ["query_model", "register_coverage_plan"]
    assert action["accepted_predicate_examples"] == [
        "transition_exists(source='Root.Attack', "
        "event='Root.Attack_Complete', target='Root.Searching')"
    ]
    assert action["pass_criteria"]


def test_direct_fact_audit_accepts_equivalent_state_hierarchy_and_eventless_forms():
    state = {
        "fact_kind": "state",
        "qualified_refs": ["state:Root.Searching"],
    }
    hierarchy = {
        "fact_kind": "hierarchy",
        "qualified_refs": ["hierarchy:Root->Root.Searching"],
        "source": "Root",
        "target": "Root.Searching",
    }
    eventless = {
        "fact_kind": "transition",
        "qualified_refs": ["transition:2"],
        "source": "Root.Intercepted",
        "event": None,
        "target": "Root.FormationAdjustment",
    }

    assert _assertion_directly_verifies_source_fact(
        "initial_child('Root') == 'Root.Searching'",
        {"structure"},
        state,
    )
    assert _assertion_directly_verifies_source_fact(
        "states(name='Root.Searching')[0].parent_path == 'Root'",
        {"structure"},
        hierarchy,
    )
    assert not _assertion_directly_verifies_source_fact(
        "len(states(parent='Root', name='Root.Searching')) == 1",
        {"structure"},
        hierarchy,
    )
    assert _assertion_directly_verifies_source_fact(
        "len(states(parent='Root', recursive=False, name='Root.Searching')) == 1",
        {"structure"},
        hierarchy,
    )
    assert _assertion_directly_verifies_source_fact(
        "len(transitions(source='Root.Intercepted', "
        "target='Root.FormationAdjustment', event=None)) == 1",
        {"relation"},
        eventless,
    )


def test_initial_transition_guidance_uses_structure_family_consistently():
    fact = {
        "fact_id": "FACT-TRANSITION-001",
        "fact_kind": "transition",
        "qualified_refs": ["transition:0"],
        "source": "[*]",
        "event": None,
        "target": "Root.Searching",
    }

    actions = _registration_required_actions(
        ["source_fact_not_directly_verified:FACT-TRANSITION-001"],
        source_fact_details={"FACT-TRANSITION-001": fact},
        coverage_requirements={},
    )

    assert actions[0]["compatible_function_families"] == ["structure"]
    assert actions[0]["accepted_predicate_examples"] == [
        "initial_child('Root') == 'Root.Searching'"
    ]
    assert _assertion_directly_verifies_source_fact(
        "initial_child('Root') == 'Root.Searching'",
        {"structure"},
        fact,
    )


def test_continuity_rejection_explains_how_to_increase_coverage():
    requirement_id = "REQ-002-01-CONTINUITY-03"
    error = (
        "assertion_semantic_policy:ASSERT-CONTINUITY:"
        f"ASSERT_CONTINUITY_EVIDENCE_REQUIRED:{requirement_id}"
    )

    actions = _registration_required_actions(
        [error],
        source_fact_details={},
        coverage_requirements={
            requirement_id: {
                "requirement_id": requirement_id,
                "dimension": "continuity",
                "cue_text": "continuously",
            }
        },
    )

    action = actions[0]
    assert action["related_ids"] == ["ASSERT-CONTINUITY", requirement_id]
    assert action["recommended_tools"] == [
        "observe_trace",
        "read_fbmcq_guide",
        "register_coverage_plan",
    ]
    assert "same expression" in action["recommended_action"]
    assert "Splitting one path per assertion" in action["recommended_action"]
    assert len(action["accepted_predicate_examples"]) == 2
    assert action["coverage_improvement"]
    assert action["pass_criteria"]


def test_revision_cannot_weaken_a_direct_source_fact_predicate():
    registry, plan, _ = _strict_registry_and_plan()
    assert registry.register_plan(plan, reason="注册含精确 source fact 的计划.")[
        "accepted"
    ]

    rejected = registry.revise_assertion(
        "ASSERT-SOURCE-001",
        "transition_exists(source='Root.Attack')",
        reason="尝试把完整迁移元组弱化为仅检查源状态.",
    )

    assert rejected["accepted"] is False
    assert "semantic_weakening_rejected" in rejected["limitations"]
    assert rejected["errors"] == [
        "source_fact_direct_evidence_weakened:FACT-TRANSITION-001"
    ]
