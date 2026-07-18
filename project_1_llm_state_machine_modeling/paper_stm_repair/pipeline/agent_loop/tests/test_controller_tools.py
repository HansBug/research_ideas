from __future__ import annotations

import inspect
import json
from typing import Any

from paper_stm_repair_loop.controller import _best_match, _bind_drafts
from paper_stm_repair_loop.schemas import CheckDraftSubmission
from paper_stm_repair_loop.tools.check_fcstm import execute as check_fcstm
from paper_stm_repair_loop.tools.evaluate_checks import execute as evaluate_checks
from paper_stm_repair_loop.tools.run_scenarios import (
    execute as run_scenarios,
    observe_events,
)
from paper_stm_repair_loop.tools.validate_discovery_checks import execute as validate_discovery_checks
from paper_stm_repair_loop.tools.verify_properties import execute as verify_properties
from paper_stm_repair_loop.tools.verify_static_consistency import execute as verify_static_consistency


MODEL = """state Root {
    event go;
    state Idle;
    state Done;
    [*] -> Idle;
    Idle -> Done : go;
}
"""

SETUP_MODEL = """state Root {
    event arm;
    event fire;
    state Idle;
    state Armed;
    state Done;
    [*] -> Idle;
    Idle -> Armed : arm;
    Armed -> Done : fire;
}
"""

SHORT_STATE_MODEL = """state Root {
    event fire;
    state A;
    state B;
    state Done;
    [*] -> B;
    B -> Done : fire;
}
"""


def test_controller_public_callables_have_seven_section_contract_docstrings():
    required = [
        "Purpose",
        "Parameters",
        "Returns",
        "Execution",
        "Failure semantics",
        "Evidence limitations",
        "Permissions",
        "Example",
    ]
    for func in [check_fcstm, run_scenarios, validate_discovery_checks, verify_properties, verify_static_consistency]:
        doc = inspect.getdoc(func) or ""
        for marker in required:
            assert marker in doc, f"{func.__module__}.{func.__name__} missing {marker}"
        assert "reference/gold" in doc
        assert "arbitrary" in doc or "path" in doc.lower()


def test_run_scenarios_records_expected_actual_and_cycle_event_accounting():
    result = run_scenarios(
        MODEL,
        [
            {
                "check_id": "SC-1",
                "check_kind": "scenario",
                "executable_spec": {
                    "events": ["Root.go"],
                    "precondition_state": "Root.Idle",
                },
                "expected_outcome": {"current_state": "Root.Done", "consumed_events": ["Root.go"]},
            }
        ],
    )
    assert result["execution_status"] == "completed"
    item = result["scenario_results"][0]
    assert item["status"] == "passed"
    assert item["expected_outcome_match_status"] == "matches"
    assert item["actual"]["current_state"] == "Root.Done"
    assert item["trace"]["cycles"]
    assert {"input_events", "consumed_events", "unconsumed_events"}.issubset(item["trace"]["cycles"][-1])
    assert "single_trace_cannot_prove_correctness" in result["limitations"]


def test_run_scenarios_executes_ordered_events_as_separate_cycles():
    result = run_scenarios(
        MODEL,
        [
            {
                "check_id": "SC-SEQUENCE",
                "check_kind": "scenario",
                "executable_spec": {
                    "events": ["Root.go", "Root.go"],
                    "precondition_state": "Root.Done",
                },
                "expected_outcome": {"state_in": "Root.Done"},
            }
        ],
    )
    item = result["scenario_results"][0]
    assert len(item["trace"]["cycles"]) == 3
    assert item["input_events"] == ["Root.go", "Root.go"]
    assert item["consumed_events"] == ["Root.go"]
    assert item["unconsumed_events"] == ["Root.go"]
    assert item["expected_outcome_match_status"] == "matches"


def test_run_scenarios_requires_setup_to_reach_declared_precondition():
    result = run_scenarios(
        SETUP_MODEL,
        [
            {
                "check_id": "SC-SETUP",
                "check_kind": "scenario",
                "executable_spec": {
                    "events": ["Root.arm", "Root.fire"],
                    "precondition_state": "Root.Armed",
                },
                "expected_outcome": {"state_in": "Root.Done"},
            }
        ],
    )

    item = result["scenario_results"][0]
    assert item["status"] == "passed"
    assert item["observed_precondition_state"] == "Root.Armed"
    assert item["tested_event"] == "Root.fire"
    assert item["consumed_events"] == ["Root.arm", "Root.fire"]


def test_run_scenarios_marks_missing_setup_as_invalid_precondition():
    result = run_scenarios(
        SETUP_MODEL,
        [
            {
                "check_id": "SC-NO-SETUP",
                "check_kind": "scenario",
                "executable_spec": {
                    "events": ["Root.fire"],
                    "precondition_state": "Root.Armed",
                },
                "expected_outcome": {"state_in": "Root.Done"},
            }
        ],
    )

    item = result["scenario_results"][0]
    assert item["status"] == "invalid_precondition"
    assert item["observed_precondition_state"] == "Root.Idle"
    assert item["expected_outcome_match_status"] == "inconclusive"
    assert len(item["trace"]["cycles"]) == 1


def test_exploratory_trace_runner_remains_separate_from_scenario_precondition_gate():
    result = observe_events(SETUP_MODEL, ["Root.arm", "Root.fire"])

    assert result["execution_status"] == "completed"
    assert result["final_configuration"]["current_state"] == "Root.Done"
    assert result["consumed_events"] == ["Root.arm", "Root.fire"]
    assert result["unconsumed_events"] == []


def test_evaluate_checks_rejects_invalid_scenario_precondition_from_gate():
    checked = check_fcstm(SETUP_MODEL)
    result = evaluate_checks(
        model_text=SETUP_MODEL,
        check_result=checked,
        checks=[
            {
                "check_origin": "nl_grounded_behavioral_issue",
                "check_id": "draft-fire",
                "check_kind": "scenario",
                "statement": "fire reaches Done from Armed.",
                "expected_outcome": {"target_label": "Done"},
                "source_basis": ["Idle -> Done : fire;"],
                "nl_basis": [
                    {
                        "quote": "When fire occurs in Armed, enter Done.",
                        "role": "requirement",
                    }
                ],
                "executable_spec": {
                    "event_labels": ["fire"],
                    "precondition_state_label": "Armed",
                },
                "binding_refs": [],
                "required": True,
            }
        ],
        formal_required=False,
        nl_text="When fire occurs in Armed, enter Done.",
        raw_source="Idle -> Done : fire;\nArmed -> Done : fire;",
    )

    assert result["scenarios"]["scenario_results"][0]["status"] == "invalid_precondition"
    assert result["gate"]["eligible"] is False
    assert result["gate"]["executed_check_ids"] == []
    assert result["gate"]["reasons"] == ["required_checks_not_executed:CHK-NL-001"]


def test_evaluate_checks_rejects_agent_declared_wrong_precondition_grounding():
    result = evaluate_checks(
        model_text=SETUP_MODEL,
        check_result=check_fcstm(SETUP_MODEL),
        checks=[
            {
                "check_origin": "nl_grounded_behavioral_issue",
                "check_id": "draft-wrong-precondition",
                "check_kind": "scenario",
                "statement": "fire reaches Done from Armed.",
                "expected_outcome": {"target_label": "Done"},
                "source_basis": ["Idle -> Done : fire;"],
                "nl_basis": [
                    {
                        "quote": "When fire occurs in Armed, enter Done.",
                        "role": "requirement",
                    }
                ],
                "executable_spec": {
                    "event_labels": ["fire"],
                    "precondition_state_label": "Idle",
                },
                "binding_refs": [],
                "required": True,
            }
        ],
        formal_required=False,
        nl_text="When fire occurs in Armed, enter Done.",
        raw_source="Idle -> Done : fire;\nArmed -> Done : fire;",
    )

    assert result["gate"]["eligible"] is False
    assert result["issue_checks"] == []
    assert result["binding_rejections"][0]["reason"] == (
        "scenario_precondition_conflicts_with_nl_state"
    )


def test_evaluate_checks_rejects_property_that_omits_named_behavior_context():
    result = evaluate_checks(
        model_text=SETUP_MODEL,
        check_result=check_fcstm(SETUP_MODEL),
        checks=[
            {
                "check_origin": "nl_grounded_behavioral_issue",
                "check_id": "draft-event-as-reach",
                "check_kind": "property",
                "statement": "fire reaches Done from Armed.",
                "expected_outcome": {"property_satisfied": True},
                "source_basis": [],
                "nl_basis": [
                    {
                        "quote": "When fire occurs in Armed, enter Done.",
                        "role": "requirement",
                    }
                ],
                "executable_spec": {
                    "kind": "reach",
                    "target_label": "Done",
                    "bound": 2,
                },
                "binding_refs": [],
                "required": True,
            }
        ],
        formal_required=False,
        nl_text="When fire occurs in Armed, enter Done.",
        raw_source="",
    )

    assert result["execution_status"] == "invalid_arguments"
    assert result["issue_checks"] == []
    assert result["gate"]["eligible"] is False
    rejection = result["binding_rejections"][0]
    assert rejection["reason"] == "property_behavior_context_not_encoded"
    assert rejection["mentioned_event_labels"] == ["fire"]
    assert rejection["mentioned_precondition_state_paths"] == ["Root.Armed"]
    assert rejection["suggested_check_kind"] == "scenario"


def test_evaluate_checks_accepts_scenario_that_encodes_named_behavior_context():
    result = evaluate_checks(
        model_text=SETUP_MODEL,
        check_result=check_fcstm(SETUP_MODEL),
        checks=[
            {
                "check_origin": "nl_grounded_behavioral_issue",
                "check_id": "draft-event-scenario",
                "check_kind": "scenario",
                "statement": "fire reaches Done from Armed.",
                "expected_outcome": {"target_label": "Done"},
                "source_basis": [],
                "nl_basis": [
                    {
                        "quote": "When fire occurs in Armed, enter Done.",
                        "role": "requirement",
                    }
                ],
                "executable_spec": {
                    "event_labels": ["arm", "fire"],
                    "precondition_state_label": "Armed",
                },
                "binding_refs": [],
                "required": True,
            }
        ],
        formal_required=False,
        nl_text="When fire occurs in Armed, enter Done.",
        raw_source="",
    )

    assert result["execution_status"] == "completed"
    assert result["binding_rejections"] == []
    assert result["scenarios"]["scenario_results"][0]["status"] == "passed"
    assert result["gate"]["eligible"] is True


def test_evaluate_checks_allows_state_only_reachability_property():
    result = evaluate_checks(
        model_text=SETUP_MODEL,
        check_result=check_fcstm(SETUP_MODEL),
        checks=[
            {
                "check_origin": "nl_grounded_behavioral_issue",
                "check_id": "draft-state-reach",
                "check_kind": "property",
                "statement": "Done is reachable.",
                "expected_outcome": {"property_satisfied": True},
                "source_basis": [],
                "nl_basis": [
                    {"quote": "Done is reachable.", "role": "requirement"}
                ],
                "executable_spec": {
                    "kind": "reach",
                    "target_label": "Done",
                    "bound": 2,
                },
                "binding_refs": [],
                "required": True,
            }
        ],
        formal_required=False,
        nl_text="Done is reachable.",
        raw_source="",
    )

    assert result["execution_status"] == "completed"
    assert result["binding_rejections"] == []
    assert result["issue_checks"][0]["check_kind"] == "property"


def test_evaluate_checks_rejects_property_with_statement_only_precondition():
    result = evaluate_checks(
        model_text=SETUP_MODEL,
        check_result=check_fcstm(SETUP_MODEL),
        checks=[
            {
                "check_origin": "nl_grounded_behavioral_issue",
                "check_id": "draft-statement-precondition",
                "check_kind": "property",
                "statement": "Done is reachable from Armed.",
                "expected_outcome": {"property_satisfied": True},
                "source_basis": [],
                "nl_basis": [
                    {"quote": "Done is reachable.", "role": "requirement"}
                ],
                "executable_spec": {
                    "kind": "reach",
                    "target_label": "Done",
                    "bound": 2,
                },
                "binding_refs": [],
                "required": True,
            }
        ],
        formal_required=False,
        nl_text="Done is reachable.",
        raw_source="",
    )

    assert result["execution_status"] == "invalid_arguments"
    rejection = result["binding_rejections"][0]
    assert rejection["reason"] == "property_behavior_context_not_encoded"
    assert rejection["mentioned_precondition_state_paths"] == ["Root.Armed"]


def test_evaluate_checks_rejects_source_only_nl_grounded_check():
    result = evaluate_checks(
        model_text=SETUP_MODEL,
        check_result=check_fcstm(SETUP_MODEL),
        checks=[
            {
                "check_origin": "nl_grounded_behavioral_issue",
                "check_id": "draft-source-only",
                "check_kind": "scenario",
                "statement": "fire reaches Done from Idle.",
                "expected_outcome": {"target_label": "Done"},
                "source_basis": ["Idle -> Done : fire;"],
                "nl_basis": [],
                "executable_spec": {
                    "event_labels": ["fire"],
                    "precondition_state_label": "Idle",
                },
                "binding_refs": [],
                "required": True,
            }
        ],
        formal_required=False,
        nl_text="When fire occurs in Armed, enter Done.",
        raw_source="Idle -> Done : fire;\nArmed -> Done : fire;",
    )

    assert result["gate"]["eligible"] is False
    assert result["binding_rejections"][0]["reason"] == (
        "nl_grounded_check_requires_nl_basis"
    )


def test_evaluate_checks_does_not_ignore_short_explicit_nl_state_label():
    result = evaluate_checks(
        model_text=SHORT_STATE_MODEL,
        check_result=check_fcstm(SHORT_STATE_MODEL),
        checks=[
            {
                "check_origin": "nl_grounded_behavioral_issue",
                "check_id": "draft-short-state-bypass",
                "check_kind": "scenario",
                "statement": "fire reaches Done from A.",
                "expected_outcome": {"target_label": "Done"},
                "source_basis": ["B -> Done : fire;"],
                "nl_basis": [
                    {
                        "quote": "When fire occurs in A, enter Done.",
                        "role": "requirement",
                    }
                ],
                "executable_spec": {
                    "event_labels": ["fire"],
                    "precondition_state_label": "B",
                },
                "binding_refs": [],
                "required": True,
            }
        ],
        formal_required=False,
        nl_text="When fire occurs in A, enter Done.",
        raw_source="B -> Done : fire;",
    )

    assert result["gate"]["eligible"] is False
    assert result["binding_rejections"][0]["reason"] == (
        "scenario_precondition_conflicts_with_nl_state"
    )


def test_scenario_exposes_nonstoppable_composite_entry_and_accepts_concrete_fix():
    broken = """state Root {
    event power_on;
    event enter_auto;
    state Human {
        [*] -> Init;
        state Init;
        state Auto {
            [*] -> Start;
            pseudo state Start;
        }
        Init -> Auto : enter_auto;
        Init -> Init : power_on;
    }
    [*] -> Human;
}
"""
    check = {
        "check_id": "SC-NONSTOPPABLE",
        "check_kind": "scenario",
        "executable_spec": {
            "events": ["Root.Human.enter_auto"],
            "precondition_state": "Root.Human.Init",
        },
        "expected_outcome": {
            "state_in": "Root.Human.Auto",
            "consumed_events": ["Root.Human.enter_auto"],
            "unconsumed_events": [],
        },
    }
    broken_result = run_scenarios(broken, [check])["scenario_results"][0]
    assert broken_result["status"] == "failed"
    assert broken_result["current_state"] == "Root.Human.Init"
    assert broken_result["consumed_events"] == []
    assert broken_result["unconsumed_events"] == ["Root.Human.enter_auto"]

    fixed = broken.replace(
        "            pseudo state Start;",
        "            pseudo state Start;\n            state Ready;\n            Start -> Ready;",
    )
    fixed_result = run_scenarios(fixed, [check])["scenario_results"][0]
    assert fixed_result["status"] == "passed"
    assert fixed_result["current_state"] == "Root.Human.Auto.Ready"
    assert fixed_result["consumed_events"] == ["Root.Human.enter_auto"]
    assert fixed_result["unconsumed_events"] == []


def test_binder_normalizes_typed_scenario_and_property_contracts():
    inspect_data = check_fcstm(MODEL)["inspect"]
    nl = CheckDraftSubmission.model_validate(
        {
            "checks": [
                {
                    "check_id": "draft-scenario",
                    "check_kind": "scenario",
                    "statement": "Go reaches Done.",
                    "expected_outcome": {"relation": "ends_in", "target_label": "Done"},
                    "nl_basis": [{"quote": "go reaches Done", "role": "requirement"}],
                    "executable_spec": {
                        "event_labels": ["go"],
                        "precondition_state_label": "Idle",
                    },
                },
                {
                    "check_id": "draft-property",
                    "check_kind": "property",
                    "statement": "Done is reachable.",
                    "expected_outcome": {"satisfied": True},
                    "nl_basis": [{"quote": "Done is reachable", "role": "requirement"}],
                    "executable_spec": {"kind": "reach", "target_label": "Done", "bound": 2},
                },
            ]
        }
    )
    checks = _bind_drafts(nl, CheckDraftSubmission(checks=[]), inspect_data)
    scenario, prop = (item.model_dump(mode="json") for item in checks)
    assert scenario["executable_spec"]["events"] == ["Root.go"]
    assert scenario["executable_spec"]["unbound_event_labels"] == []
    assert scenario["executable_spec"]["precondition_state"] == "Root.Idle"
    assert scenario["expected_outcome"] == {
        "state_in": "Root.Done",
        "consumed_events": ["Root.go"],
        "unconsumed_events": [],
    }
    assert prop["executable_spec"]["query"] == 'check reach <= 2: active("Root.Done");'
    assert prop["expected_outcome"] == {"property_satisfied": True}


def test_source_drafts_must_prove_a_source_internal_conflict_contract():
    source = CheckDraftSubmission.model_validate(
        {
            "checks": [
                {
                    "check_id": "normal-transition-inventory",
                    "check_kind": "static_consistency",
                    "statement": "Idle transitions to Done.",
                    "source_basis": ["Idle -> Done : go"],
                    "executable_spec": {
                        "kind": "transition_shape",
                        "source_label": "Idle",
                        "target_label": "Done",
                        "event_label": "go",
                    },
                    "required": True,
                }
            ]
        }
    )
    rejections: list[dict[str, Any]] = []
    checks = _bind_drafts(
        CheckDraftSubmission(checks=[]),
        source,
        check_fcstm(MODEL)["inspect"],
        binding_rejections=rejections,
    )
    assert checks == []
    assert rejections == [
        {
            "draft_origin": "raw_internal_inconsistency",
            "draft_check_id": "normal-transition-inventory",
            "reason": "source_internal_conflict_contract_unsatisfied",
            "required_source_basis_min": 2,
            "observed_source_basis_count": 1,
            "required_consistency_status": "contradicts",
            "observed_consistency_status": None,
        }
    ]


def test_binder_preserves_structural_property_semantics_instead_of_coercing_to_reach():
    nl = CheckDraftSubmission.model_validate(
        {
            "checks": [
                {
                    "check_id": "simple-state",
                    "check_kind": "property",
                    "statement": "Done is a simple state.",
                    "expected_outcome": {"property_satisfied": True},
                    "nl_basis": [{"quote": "Done is simple", "role": "requirement"}],
                    "executable_spec": {"kind": "simple_state", "target_label": "Done", "bound": 0},
                }
            ]
        }
    )
    check_item = _bind_drafts(nl, CheckDraftSubmission(checks=[]), check_fcstm(MODEL)["inspect"])[0].model_dump(mode="json")
    assert check_item["executable_spec"] == {
        "kind": "state_shape",
        "state": "Root.Done",
        "expect": {"is_leaf": True, "is_composite": False},
    }
    evidence = verify_properties(MODEL, [check_item], check_result=check_fcstm(MODEL))
    assert evidence["property_results"][0]["solver_status"] == "deterministic_static"
    assert evidence["property_results"][0]["property_satisfied"] is True
    assert validate_discovery_checks([check_item], check_fcstm(MODEL), evidence)["mechanically_eligible"] is True


def test_event_binding_handles_operator_and_source_lifecycle_aliases():
    events = [
        ("Root.Front_Distance_10", "Front Distance > 10"),
        ("Root.Exit_Autonomous", "Exit Autonomous"),
    ]
    assert _best_match("front_distance_gt_10", events, event_semantics=True) == "Root.Front_Distance_10"
    assert _best_match("auto_final", events, event_semantics=True) == "Root.Exit_Autonomous"


def test_best_match_refuses_equal_rank_ambiguous_labels():
    states = [("Root.Left.Idle", "Idle"), ("Root.Right.Idle", "Idle")]
    assert _best_match("Idle", states) is None


def test_validate_discovery_checks_rejects_partially_bound_scenario():
    result = validate_discovery_checks(
        [
            {
                "check_id": "SC-PARTIAL",
                "check_kind": "scenario",
                "binding_refs": ["event:Root.go"],
                "source_basis": [],
                "executable_spec": {
                    "events": ["Root.go"],
                    "requested_event_labels": ["go", "missing"],
                    "unbound_event_labels": ["missing"],
                    "precondition_state": "Root.Idle",
                    "setup_events": ["Root.go"],
                    "tested_event": None,
                },
                "required": True,
            }
        ],
        check_fcstm(MODEL),
    )
    assert result["mechanically_eligible"] is False
    assert result["checks"][0]["executability_status"] == "invalid"
    scenario = run_scenarios(
        MODEL,
        [
            {
                "check_id": "SC-PARTIAL",
                "check_kind": "scenario",
                "executable_spec": {
                    "events": ["Root.go"],
                    "unbound_event_labels": ["missing"],
                    "precondition_state": "Root.Idle",
                    "setup_events": [],
                    "tested_event": "Root.go",
                },
            }
        ],
    )
    assert scenario["scenario_results"][0]["status"] == "error"
    assert "partial scenario" in scenario["scenario_results"][0]["error"]["message"]


def test_validate_discovery_checks_rejects_incomplete_static_shape_before_helper_execution():
    result = validate_discovery_checks(
        [
            {
                "check_id": "STATIC-INCOMPLETE",
                "check_kind": "static_consistency",
                "binding_refs": ["transition:1"],
                "source_basis": ["source:a", "source:b"],
                "executable_spec": {"kind": "transition_shape", "source_label": "Idle"},
                "required": True,
            }
        ],
        check_fcstm(MODEL),
    )
    assert result["mechanically_eligible"] is False
    assert result["checks"][0]["executability_status"] == "invalid"


def test_validate_discovery_checks_has_no_semantic_quality_verdict_and_fails_unknown_obligation():
    check_result = check_fcstm(MODEL)
    result = validate_discovery_checks(
        [
            {
                "check_id": "P-UNKNOWN",
                "check_kind": "property",
                "binding_refs": ["state:Root.Idle"],
                "source_basis": ["source:req"],
                "executable_spec": {"kind": "fbmcq", "query": 'check reach <= 1: active("Root.Idle");'},
                "obligation_results": [{"kind": "non_vacuity", "status": "unknown", "replay": {"ok": True}}],
                "required": True,
            }
        ],
        check_result,
    )
    assert result["execution_status"] == "completed"
    assert result["mechanically_eligible"] is False
    dumped = json.dumps(result, ensure_ascii=False, sort_keys=True)
    for forbidden in ["semantic_correct", "coverage_sufficient", "strong", "weak", "quality_verdict", "strength"]:
        assert forbidden not in dumped


def test_validate_discovery_checks_uses_separate_bounded_property_evidence_without_mutating_check():
    check_result = check_fcstm(MODEL)
    check = {
        "check_id": "P-EXECUTED",
        "check_kind": "property",
        "binding_refs": ["state:Root.Idle"],
        "source_basis": ["source:req"],
        "executable_spec": {"kind": "fbmcq", "query": 'check reach <= 1: active("Root.Idle");'},
        "expected_outcome": {"property_satisfied": False},
        "required": True,
    }
    original = json.loads(json.dumps(check))
    result = validate_discovery_checks(
        [check],
        check_result,
        {
            "property_results": [
                {
                    "check_id": "P-EXECUTED",
                    "status": "failed",
                    "solver_status": "sat",
                    "property_satisfied": True,
                    "query": 'check reach <= 1: active("Root.Idle");',
                    "query_sha256": "query-hash",
                    "witness": {"frames": []},
                    "replay": {"ok": True, "mismatches": []},
                    "expected_outcome_match_status": "contradicts",
                }
            ]
        },
    )
    assert check == original
    assert result["mechanically_eligible"] is True
    obligation = result["checks"][0]["non_vacuity_obligations"][0]
    assert obligation["status"] == "completed"
    assert obligation["replay_required"] is True
    assert obligation["replay_ok"] is True
    assert "expected_outcome_match_status" not in obligation


def test_validate_discovery_checks_rejects_sat_witness_without_replay():
    result = validate_discovery_checks(
        [
            {
                "check_id": "P-NO-REPLAY",
                "check_kind": "property",
                "binding_refs": ["state:Root.Idle"],
                "source_basis": ["source:req"],
                "executable_spec": {"kind": "fbmcq", "query": 'check reach <= 1: active("Root.Idle");'},
                "required": True,
            }
        ],
        check_fcstm(MODEL),
        {
            "property_results": [
                {
                    "check_id": "P-NO-REPLAY",
                    "status": "completed",
                    "solver_status": "sat",
                    "property_satisfied": True,
                    "witness": {"frames": []},
                    "replay": None,
                }
            ]
        },
    )
    assert result["mechanically_eligible"] is False
    assert result["checks"][0]["non_vacuity_obligations"][0]["status"] == "missing"


def test_verify_properties_uses_bmc_json_and_never_passes_replay_mismatch():
    def fake_bmc(_model_path: str, _query_path: str, **_kwargs: Any) -> tuple[str, int]:
        payload = {
            "property": {"kind": "reach", "bound": 2, "polarity": "witness"},
            "result": {
                "status": "sat",
                "kind": "reach",
                "polarity": "witness",
                "outcome": "witness_found",
                "property_satisfied": True,
                "incomplete": False,
                "timeout_ms": None,
            },
            "witness": {"frames": []},
            "replay": {"ok": False, "mismatches": [{"step": 1}]},
        }
        return json.dumps(payload), 0

    result = verify_properties(
        MODEL,
        [
            {
                "check_id": "P-1",
                "check_kind": "property",
                "executable_spec": {"kind": "fbmcq", "query": 'check reach <= 2: active("Root.Idle");'},
                "expected_outcome": {"property_satisfied": True},
            }
        ],
        bmc_runner=fake_bmc,
    )
    item = result["property_results"][0]
    assert item["status"] == "replay_mismatch"
    assert item["passed"] is False
    assert item["expected_outcome_match_status"] == "inconclusive"
    assert item["query_sha256"]
    assert item["kind"] == "reach"
    assert item["bound"] == 2
    assert item["polarity"] == "witness"


def test_check_fcstm_can_embed_static_consistency_helper_result():
    result = check_fcstm(
        MODEL,
        static_checks=[
            {
                "check_id": "ST-1",
                "check_kind": "static_consistency",
                "source_basis": ["source:req"],
                "executable_spec": {"kind": "transition_shape", "transition_index": 1, "expect": {"event": "Root.go"}},
            }
        ],
    )
    assert result["execution_status"] == "completed"
    assert result["executable"] is True
    assert "static_consistency" in result
    assert result["static_consistency"]["static_results"][0]["status"] == "passed"
