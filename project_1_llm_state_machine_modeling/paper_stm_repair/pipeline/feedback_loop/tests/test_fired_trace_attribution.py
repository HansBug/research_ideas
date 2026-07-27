"""Fired-transition derivation, path taint, and the attribution they unlock.

Issue #170 W1-W6.  A simulation observation only becomes attribution evidence
once the path that produced it is identified, so these tests pin the four taint
states and, critically, the cases where the derivation must *refuse* to report a
clean path.
"""

from __future__ import annotations

import json
import pathlib

import pytest

from paper_stm_feedback_loop.assertions import AssertionChecker, build_eval_environment
from paper_stm_feedback_loop.assertions.fired_trace import derive_fired_transitions
from paper_stm_feedback_loop.common.refs import reference_matches

REPORTS = (
    pathlib.Path(__file__).resolve().parents[2]
    / "representation/reports/llms_emp_r45_java_60"
)
PAIR = "llms_emp_feedback_final_0000"


def _environment(**overrides):
    trace = json.loads((REPORTS / f"source_traces/{PAIR}.json").read_text())
    kwargs = dict(
        model_text=(REPORTS / "pairs/0000/fcstm.fcstm").read_text(),
        source_mappings=trace.get("entries", []),
        source_exclusions=trace.get("attribution_exclusions", []),
        timeout_seconds=25,
        formal_verification_enabled=False,
    )
    kwargs.update(overrides)
    return build_eval_environment(**kwargs)


def _refs(result) -> list[str]:
    payload = result.to_json()
    return sorted(
        {
            ref
            for call in (payload.get("function_call_trace") or [])
            for ref in (call.get("model_refs") or [])
        }
    )


# --------------------------------------------------------------------------
# Unit level: the derivation itself
# --------------------------------------------------------------------------

TABLE = [
    {"transition_index": 0, "from_path": "R.A", "to_path": "R.B", "event": "R.go", "guard": None, "effect": None},
    {"transition_index": 1, "from_path": "R.A", "to_path": "R.C", "event": "R.go", "guard": None, "effect": None},
    {"transition_index": 2, "from_path": "R.B", "to_path": "R.D", "event": None, "guard": "TOK == 5", "effect": None},
    {"transition_index": 3, "from_path": "R.C", "to_path": "R.D", "event": None, "guard": None, "effect": None},
]


def test_unique_carrier_is_derived_with_clean_taint():
    derived = derive_fired_transitions(
        transitions=[TABLE[0]],
        active_before=["R", "R.A"],
        active_after=["R", "R.B"],
        consumed_events=["R.go"],
        is_ended=False,
    )
    assert derived["fired_transitions"] == ("transition:0",)
    assert derived["path_taint"] == "clean"


def test_target_narrows_an_otherwise_ambiguous_carrier():
    derived = derive_fired_transitions(
        transitions=TABLE,
        active_before=["R", "R.A"],
        active_after=["R", "R.C"],
        consumed_events=["R.go"],
        is_ended=False,
    )
    assert derived["fired_transitions"] == ("transition:1",)
    assert derived["path_taint"] == "clean"


def test_ambiguous_carrier_with_disagreeing_taint_is_not_promoted():
    """Two candidates, one crossing an excluded variable: must not read clean."""

    table = [
        TABLE[0],
        {
            "transition_index": 1,
            "from_path": "R.A",
            "to_path": "R.B",
            "event": "R.go",
            "guard": "TOK == 5",
            "effect": None,
        },
    ]
    derived = derive_fired_transitions(
        transitions=table,
        active_before=["R", "R.A"],
        active_after=["R", "R.B"],
        consumed_events=["R.go"],
        is_ended=False,
        excluded=("compiler:route_control:TOK",),
    )
    assert derived["path_taint"] == "ambiguous"
    assert derived["candidates"] == {"R.go": ["transition:0", "transition:1"]}


def test_ambiguous_carrier_with_agreeing_taint_stays_usable():
    """Whichever of the two fired, the path is clean, so ambiguity is harmless."""

    derived = derive_fired_transitions(
        transitions=[TABLE[0], dict(TABLE[1], to_path="R.B")],
        active_before=["R", "R.A"],
        active_after=["R", "R.B"],
        consumed_events=["R.go"],
        is_ended=False,
        excluded=("compiler:route_control:TOK",),
    )
    assert derived["path_taint"] == "clean"


def test_unexplained_state_change_is_reported_not_dropped():
    derived = derive_fired_transitions(
        transitions=[TABLE[0]],
        active_before=["R", "R.A"],
        active_after=["R", "R.Z"],
        consumed_events=[],
        is_ended=False,
    )
    assert derived["path_taint"] == "ambiguous"
    assert any("unresolved_segment" in item for item in derived["limitations"])


def test_missing_transition_table_never_reports_a_clean_path():
    derived = derive_fired_transitions(
        transitions=None,
        active_before=["R", "R.A"],
        active_after=["R", "R.B"],
        consumed_events=["R.go"],
        is_ended=False,
    )
    assert derived["path_taint"] == "ambiguous"
    assert derived["fired_transitions"] == ()


# --------------------------------------------------------------------------
# Integration level: real pair 0000 through the production checker
# --------------------------------------------------------------------------


def test_clean_path_reports_the_carrying_transition():
    env = _environment()
    result = AssertionChecker(environment=env).check(
        f'assert simulate(cycles=[[], ["{PAIR}.Power_Off"]])'
        f'.final.is_active("{PAIR}.FinalState") is True, "[R][A] m"',
        "a1",
        required_function_families=("simulation",),
    )
    refs = _refs(result)
    assert "transition:3" in refs
    assert f"{PAIR}.FinalState" in refs
    assert not any(item.startswith("route_control:") for item in refs)


def test_path_through_route_control_stays_debt_bearing():
    """The guard against over-opening: lowering on the path must still taint it."""

    env = _environment()
    result = AssertionChecker(environment=env).check(
        f'assert simulate(cycles=[[], ["{PAIR}.Power_On"], ["{PAIR}.front_distance_10"], '
        f'["{PAIR}.Human_Steering_Cmd_Brake_Pressed_in_AutoFinal"]])'
        f'.final.is_active("{PAIR}.HumanDrivingMode") is False, "[R][A] m"',
        "a1",
        required_function_families=("simulation",),
    )
    refs = _refs(result)
    assert "route_control:R45RouteToken" in refs
    assert reference_matches(
        "compiler:route_control:R45RouteToken", set(refs)
    ), "the shared matcher must see this ref as the excluded element"


def test_ignored_event_binds_to_its_declared_carrier():
    """An event nobody consumes is the defect; near miss gives it an anchor."""

    env = _environment()
    result = AssertionChecker(environment=env).check(
        f'assert simulate(initial_state="{PAIR}.HumanDrivingMode", '
        f'initial_vars={{"R45RouteToken": 0}}, cycles=[["{PAIR}.Condition_Met"]])'
        f'.final.is_active("{PAIR}.AutonomousMode") is True, "[R][A] m"',
        "a1",
        required_function_families=("simulation",),
    )
    refs = _refs(result)
    assert f"{PAIR}.Condition_Met" in refs
    assert any(item.startswith("transition:") for item in refs)


def test_simulation_and_static_evidence_agree_on_the_same_element():
    """Both families must land on the same transition for the same fact.

    This is what makes the attribution algebra reusable: the exclusion table is
    intersected against one reference vocabulary, not two.
    """

    env = _environment()
    checker = AssertionChecker(environment=env)
    dynamic = checker.check(
        f'assert simulate(cycles=[[], ["{PAIR}.Power_Off"]])'
        f'.final.is_active("{PAIR}.FinalState") is True, "[R][A] m"',
        "a1",
        required_function_families=("simulation",),
    )
    static = checker.check(
        f'assert transition_exists(event="{PAIR}.Power_Off", '
        f'target="{PAIR}.FinalState") is True, "[R][A] m"',
        "a2",
        required_function_families=("relation",),
    )
    assert "transition:3" in _refs(dynamic)
    assert "transition:3" in _refs(static)


@pytest.mark.parametrize(
    "query, expect_marker",
    [
        (f'check invariant <= 3: !active("{PAIR}.FinalState");', False),
        (f'check reach <= 1: active("{PAIR}.AutonomousMode.AutoFinal");', True),
    ],
)
def test_formal_refs_separate_counterexample_from_bounded_absence(query, expect_marker):
    env = _environment(
        formal_verification_enabled=True,
        fbmcq_solver_timeout_ms=25_000,
        fbmcq_max_bound=8,
        fbmcq_process_wall_seconds=30.0,
    )
    result = AssertionChecker(environment=env).check(
        f"assert fbmcq({query!r}).holds is True, \"[R][A] m\"",
        "a1",
        required_function_families=("formal",),
    )
    refs = _refs(result)
    assert result.value is False
    assert refs, "a refuted formal query must expose the elements it rests on"
    assert ("formal:examined_only" in refs) is expect_marker


# --------------------------------------------------------------------------
# C0: the action fields the `action_declared` predicate needs
# --------------------------------------------------------------------------

ACTION_MODEL = """def int c = 0;
state Root {
    event go;
    state Idle {
        enter { c = 1; }
        exit { c = 0; }
    }
    state Done;
    [*] -> Idle;
    Idle -> Done : /go;
}
"""


@pytest.mark.parametrize(
    "state, field, expected",
    [
        ("Root.Idle", "entry_actions", True),
        ("Root.Idle", "exit_actions", True),
        ("Root.Idle", "during_actions", False),
        ("Root.Done", "entry_actions", False),
    ],
)
def test_action_declared_predicate_is_executable(state, field, expected):
    """Without these fields the predicate is advertised but cannot be checked."""

    env = build_eval_environment(
        model_text=ACTION_MODEL,
        source_mappings=[],
        source_exclusions=[],
        timeout_seconds=10,
        formal_verification_enabled=False,
    )
    result = AssertionChecker(environment=env).check(
        f'assert bool(states(path="{state}", exact=True)[0].{field}) is True, "[R][A] m"',
        "a1",
        required_function_families=("structure",),
    )
    assert result.outcome in {"valid", "sealed_false"}
    assert result.value is expected


# --------------------------------------------------------------------------
# W6 + W9 terminal acceptance: does a simulation-only False become promotable,
# and does a tainted path still refuse to be?
# --------------------------------------------------------------------------


def _bind_one(case: str, source: str, family: str):
    """Run one assertion on a real pair and return its attribution binding."""

    from paper_stm_feedback_loop.discover import nodes
    from paper_stm_feedback_loop.discover.schemas import (
        AssertionResult,
        FrozenDiscoverInputs,
        ReleasedAssertionResults,
    )

    pair = f"llms_emp_feedback_final_{case}"
    trace = json.loads((REPORTS / f"source_traces/{pair}.json").read_text())
    contract = json.loads((REPORTS / f"working_contracts/{pair}.json").read_text())
    env = build_eval_environment(
        model_text=(REPORTS / f"pairs/{case}/fcstm.fcstm").read_text(),
        source_mappings=trace.get("entries", []),
        source_exclusions=trace.get("attribution_exclusions", []),
        timeout_seconds=25,
        formal_verification_enabled=False,
    )
    payload = AssertionChecker(environment=env).check(
        source, "AST-X-01", required_function_families=(family,)
    ).to_json()
    assert payload["value"] is False, "the fixture must produce a False to attribute"
    released = ReleasedAssertionResults(
        results=(
            AssertionResult(
                assertion_id="AST-X-01",
                requirement_id="REQ-X",
                role="primary",
                coverage_key="k",
                truth_value=False,
                evidence_family=family,
                script_hash="0" * 64,
                tool_env_hash="0" * 64,
                evidence_scope={
                    "actual_function_families": payload["actual_function_families"]
                },
                check_detail={
                    "function_call_trace": payload["function_call_trace"],
                    "actual_function_families": payload["actual_function_families"],
                },
            ),
        ),
        script_hash="0" * 64,
        tool_env_hash="0" * 64,
        sealed_hash="0" * 64,
    )
    out = nodes.bind_attribution(
        {
            "frozen_inputs": FrozenDiscoverInputs(
                run_id="probe",
                natural_language="probe",
                stm_text="probe",
                source_trace=trace,
                working_contract=contract,
                input_hashes={"nl": "0" * 64},
                tool_env_hash="0" * 64,
                profile="probe",
                language="zh-CN",
            ),
            "released_assertion_results": released,
            "node_execution_records": (),
        }
    )
    return out["attribution_projection"].bindings[0]


def test_simulation_only_false_can_now_be_promoted():
    """The terminal acceptance of the attribution line (issue #170 §7.4)."""

    binding = _bind_one(
        "0000",
        f'assert simulate(cycles=[[], ["{PAIR}.Power_Off"]])'
        f'.final.is_active("{PAIR}.FinalState") is False, "[R][A] m"',
        "simulation",
    )
    assert binding.status == "safe"
    assert binding.source_level_claim_allowed is True


def test_tainted_simulation_path_is_still_refused():
    """The guard against over-opening: granting the family is not granting the path."""

    binding = _bind_one(
        "0000",
        f'assert simulate(cycles=[[], ["{PAIR}.Power_On"], ["{PAIR}.front_distance_10"], '
        f'["{PAIR}.Human_Steering_Cmd_Brake_Pressed_in_AutoFinal"]])'
        f'.final.is_active("{PAIR}.HumanDrivingMode") is False, "[R][A] m"',
        "simulation",
    )
    assert binding.status == "representation_debt"
    assert binding.source_level_claim_allowed is False
    assert "compiler:route_control:R45RouteToken" in binding.exclusion_refs


def test_ignored_event_false_is_attributable_through_near_miss():
    binding = _bind_one(
        "0000",
        f'assert simulate(initial_state="{PAIR}.HumanDrivingMode", '
        f'initial_vars={{"R45RouteToken": 0}}, cycles=[["{PAIR}.Condition_Met"]])'
        f'.final.is_active("{PAIR}.AutonomousMode") is True, "[R][A] m"',
        "simulation",
    )
    assert binding.status == "safe"
    assert binding.source_refs
