from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "feedback_loop/src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.assertions import AssertionChecker, EvalEnvironment  # noqa: E402
from paper_stm_feedback_loop.assertions.checker import PORTED_SOURCE_COMMIT  # noqa: E402
from paper_stm_feedback_loop.assertions.environment import ASSERTION_ENVIRONMENT_API_DOCS  # noqa: E402
from paper_stm_feedback_loop.assertions.fbmcq import (  # noqa: E402
    FBMCQAPI,
    formal_query_causality,
    parse_bmc_query,
)

MODEL = """state Root {
    event go;
    state Idle;
    state Done;
    [*] -> Idle;
    Idle -> Done : go;
}
"""

FIXTURE_METADATA = {"ported_source_commit": "c8c1ccba"}


def test_parser_checker_support_prefix_terminal_assert_and_fresh_namespace():
    env = EvalEnvironment(model_text=MODEL)
    checker = AssertionChecker(env)

    first = checker.check(
        "seen = edge_declared(source='Root.Idle', trigger='Root.go', target='Root.Done')\nassert seen, '[REQ-001][AST-001-01] transition missing'",
        reason="positive transition exists",
        required_function_families=["relation"],
    )
    second = checker.check(
        "assert seen, '[REQ-001][AST-001-02] unknown local'",
        reason="namespace isolation rejects previous prefix binding",
    )

    assert first.outcome == "valid"
    assert first.value is True
    assert first.actual_function_families == ("relation",)
    assert second.outcome == "invalid"
    assert second.sealed.error["type"] == "AuditRejected"
    assert any(issue["code"] == "unknown_name" for issue in second.to_json()["audit"]["issues"])
    assert PORTED_SOURCE_COMMIT == FIXTURE_METADATA["ported_source_commit"]


def test_strict_false_is_sealed_but_assertionerror_and_non_bool_are_invalid():
    def broken_helper() -> bool:
        raise AssertionError("helper failed")

    checker = AssertionChecker(
        EvalEnvironment(
            model_text=MODEL,
            extra_functions={"broken_helper": ("structure", broken_helper)},
        )
    )

    sealed = checker.check(
        "assert edge_declared(source='Root.Done', trigger='Root.go', target='Root.Idle'), '[REQ-001][AST-001-01] reverse transition missing'",
        required_function_families=["relation"],
    )
    prefix_assertion_error = checker.check(
        "helper_ok = broken_helper()\nassert helper_ok, '[REQ-001][AST-001-02] helper failed'"
    )
    # Every predicate returns a strict bool, so the only way left to reach the
    # non-bool guard is to fold one through a builtin.  The guard must still
    # hold: it is what stops a truthy container from closing an obligation.
    non_bool = checker.check(
        "assert sum([edge_declared(source='Root.Idle', trigger='Root.go', target='Root.Done')]), "
        "'[REQ-001][AST-001-03] non bool'"
    )

    assert sealed.outcome == "sealed_false"
    assert sealed.value is False
    assert prefix_assertion_error.outcome == "invalid"
    assert prefix_assertion_error.sealed.error["type"] == "AssertionError"
    assert non_bool.outcome == "invalid"
    assert non_bool.sealed.error["type"] == "NonBoolTerminalAssert"


def test_lambda_local_binding_can_reuse_one_read_only_simulation_result():
    # One simulation, bound once and read twice: the point is that the terminal
    # expression may carry a lambda without the audit rejecting it, and that the
    # bound result stays usable instead of forcing a second trace.
    checker = AssertionChecker(EvalEnvironment(model_text=MODEL))
    result = checker.check(
        "assert (lambda occupied: occupied is True and bool(occupied))("
        "occupancy_after(source='Root.Idle', trigger='Root.go', target='Root.Done')), "
        "'[REQ-001][AST-001-01] Done did not become active'",
        required_function_families=["simulation"],
    )
    assert result.outcome == "valid"
    assert result.actual_function_families == ("simulation",)


def test_simulation_variable_mapping_is_readable_through_the_delta_predicate() -> None:
    """Reading a variable out of the simulation state is now internal evidence.

    An assertion can no longer hold the frozen variable mapping itself, so the
    property that mattered -- a declared variable is observable at both ends of
    the trace -- is pinned through the predicate that reads it.  An unobservable
    variable raises rather than answering, so a plain ``true`` here is proof the
    mapping was actually read at both ends and not defaulted away.
    """

    model = """def int counter = 0;
state Root {
    event go;
    state Idle;
    state Done;
    [*] -> Idle;
    Idle -> Done : go effect { counter = counter + 1; };
}
"""
    checker = AssertionChecker(EvalEnvironment(model_text=model))
    result = checker.check(
        "assert variable_delta_after(source='Root.Idle', trigger='Root.go', "
        "variable='counter', sign='positive'), "
        "'[REQ-001][AST-001-02] variable mapping access failed'",
        required_function_families=["simulation"],
    )
    assert result.outcome == "valid"
    assert result.actual_function_families == ("simulation",)

    unobservable = checker.check(
        "assert variable_delta_after(source='Root.Idle', trigger='Root.go', "
        "variable='not_declared', sign='positive'), "
        "'[REQ-001][AST-001-03] variable mapping access failed'",
        required_function_families=["simulation"],
    )
    assert unobservable.outcome == "invalid"
    assert unobservable.sealed.error["type"] == "UnsupportedEvidence"


def test_environment_docs_list_readable_api_surface():
    # The doc body is hard-wrapped, so a needle that spans a wrap point has to be
    # matched against the unwrapped text or it silently never matches.
    unwrapped = " ".join(ASSERTION_ENVIRONMENT_API_DOCS.split())
    for needle in [
        "Every predicate returns a strict bool",
        "occupancy_after",
        "predicate_bindings",
        "declared_model_vocabulary",
        "EVIDENCE FAMILY",
        "The family is derived from the predicate, never declared by you",
        "Family B -> `simulation`. Family P -> `fbmcq`",
        # The doc must say what to do about an element the model lacks, since
        # that is the case a producer cannot resolve on its own.
        "Assert that existence as a `precondition`",
        "Allowed pure builtins:",
    ]:
        assert needle in unwrapped, needle
    # Naming what is gone is part of the readable surface: a producer that still
    # reaches for a removed primitive must find out here, not from an audit
    # rejection several revisions later.
    for removed in (
        "simulate",
        "fbmcq",
        "states",
        "transitions",
        "transition_exists",
        "path",
        "topology",
    ):
        assert f"no `{removed}`" in unwrapped, removed


def test_initial_target_resolves_the_structured_initial_target_to_one_child():
    fixture = ROOT / "feedback_loop/fixtures/selected_models/0029/STM_0.fcstm"
    env = EvalEnvironment(model_text=fixture.read_text(encoding="utf-8"))
    result = env.eval_assert(
        "initial_target(composite='llms_emp_feedback_final_0029.CollisionAvoidance', "
        "child='llms_emp_feedback_final_0029.CollisionAvoidance.collision_avoidance_deactive')",
        "CollisionAvoidance has the declared initial child",
        required_function_families=["structure"],
    )
    assert result.result == "true"


def test_conflicting_targets_distinguishes_same_trigger_targets() -> None:
    model = """state Root {
    event go;
    state A;
    state B;
    state C;
    [*] -> A;
    A -> B : go;
    A -> C : go;
}
"""
    env = EvalEnvironment(model_text=model)
    result = env.eval_assert(
        "guard_distinguishable(source='Root.A', trigger='Root.go') is False",
        "the same trigger has two unguarded targets",
        required_function_families=["relation"],
    )
    assert result.result == "true"


def test_effect_call_records_frozen_transition_scope() -> None:
    model = """def int semantic_count = 3;
state Root {
    event completed;
    state Active;
    state Done;
    [*] -> Active;
    Active -> Done : completed;
}
"""
    env = EvalEnvironment(model_text=model)
    result = env.eval_assert(
        "effect_declared(source='Root.Working', trigger='Root.completed', variable='semantic_count', sign='negative') is False",
        "the scoped transition does not declare the semantic effect",
        required_function_families=["effect"],
    )
    assert result.result == "true"
    assert len(result.function_call_trace) == 1
    refs = set(result.function_call_trace[0].model_refs)
    assert "Root.Active" in refs
    assert "Root.completed" in refs
    assert "transition:1" in refs


def test_unmatched_effect_probe_does_not_claim_unrelated_transition_refs() -> None:
    """Near-miss anchoring must stay a near miss, not a model-wide sweep.

    The predicate is always source- and trigger-scoped, so the old model-wide
    variable probe cannot be written any more.  What survives is the rule that
    made it safe: when neither the source nor the trigger matches anything, the
    call has no transition to anchor to, and the one declared transition of this
    model must not be handed to it as manufactured source attribution.
    """

    model = """def int counter = 0;
state Root {
    event tick;
    state A;
    state B;
    [*] -> A;
    A -> B : tick effect { counter = counter + 1; };
}
"""
    env = EvalEnvironment(model_text=model)
    result = env.eval_assert(
        "effect_declared(source='Root.Working', trigger='Root.completed', variable='counter', sign='negative')",
        "counter should decrease somewhere",
        required_function_families=["effect"],
    )
    assert result.result == "false"
    refs = set(result.function_call_trace[0].model_refs)
    assert not refs & {"Root.A", "Root.B", "Root.tick", "transition:1"}


def test_event_scoped_effect_probe_excludes_compiler_route_control() -> None:
    model = """def int R45RouteToken = 0;
state Root {
    event completed;
    state Active;
    state Done;
    [*] -> Active;
    Active -> Done : completed effect { R45RouteToken = R45RouteToken - 1; };
}
"""
    env = EvalEnvironment(
        model_text=model,
        source_exclusions=["compiler:route_control:R45RouteToken"],
    )
    result = env.eval_assert(
        "effect_declared(source='Root.Active', trigger='Root.completed', variable='R45RouteToken', sign='negative')",
        "a compiler route token is not the requested semantic quantity",
        required_function_families=["effect"],
    )
    # The token is the only assignment on that edge, and it is excluded, so the
    # answer is a clean False rather than a decrement the requirement can bank.
    assert result.result == "false"
    refs = set(result.function_call_trace[0].model_refs)
    # Excluded from the answer, so it must be recorded under the kind that does
    # not disqualify the finding as representation debt.
    assert "filtered_route_control:R45RouteToken" in refs
    assert "route_control:R45RouteToken" not in refs


def test_relation_call_records_compiler_route_control_from_guard() -> None:
    """The 0050 lowering shape: the NL edge exists only as a token-guarded one.

    Unlike the effect probe above, a relation query does not filter the token
    out.  Its presence in the guard the near miss landed on is genuine evidence
    that this edge was produced by the converter, so it must keep signalling
    debt -- otherwise the False is booked against the source author.
    """

    model = """def int R45RouteToken = 0;
state Root {
    event resume;
    state Entry;
    state Cruise;
    [*] -> Entry;
    Entry -> Cruise : if [R45RouteToken == 5] effect { R45RouteToken = 0; };
}
"""
    env = EvalEnvironment(
        model_text=model,
        source_exclusions=["compiler:route_control:R45RouteToken"],
    )
    result = env.eval_assert(
        "edge_declared(source='Root.Entry', trigger='Root.resume', target='Root.Cruise')",
        "the resume relation should not be carried by a converter-owned guard",
        required_function_families=["relation"],
    )

    assert result.result == "false"
    refs = set(result.function_call_trace[0].model_refs)
    assert "route_control:R45RouteToken" in refs
    assert "filtered_route_control:R45RouteToken" not in refs
    assert "Root.Entry" in refs


def test_failed_transition_query_records_same_trigger_wrong_target() -> None:
    model = """state Root {
    event leave;
    state Cruise;
    state Exit;
    state Finish;
    [*] -> Cruise;
    Cruise -> Finish : leave;
}
"""
    env = EvalEnvironment(
        model_text=model,
        source_exclusions=["compiler:event_projection:Root.leave"],
    )
    result = env.eval_assert(
        "edge_declared(source='Root.Cruise', trigger='Root.leave', target='Root.Exit')",
        "the local exit should not finish the whole machine",
        required_function_families=["relation"],
    )

    assert result.result == "false"
    refs = set(result.function_call_trace[0].model_refs)
    assert {"Root.Cruise", "Root.leave", "Root.Finish"} <= refs
    assert "compiler:event_projection:Root.leave" not in refs


def test_failed_transition_query_marks_different_projected_event_near_miss() -> None:
    model = """state Root {
    event pedestrian_or_distance;
    state Idle;
    state Active;
    [*] -> Idle;
    Idle -> Active : pedestrian_or_distance;
}
"""
    env = EvalEnvironment(
        model_text=model,
        source_exclusions=[
            "compiler:event_projection:Root.pedestrian_or_distance"
        ],
    )
    result = env.eval_assert(
        "edge_declared(source='Root.Idle', trigger='Root.pedestrian', target='Root.Active')",
        "an invented atomic event must not replace a combined projection",
        required_function_families=["relation"],
    )

    assert result.result == "false"
    # The bare event path is not enough: `common.refs` compares complete
    # references, so only the qualified form intersects the exclusion table and
    # keeps this False out of the source author's ledger.
    assert (
        "compiler:event_projection:Root.pedestrian_or_distance"
        in result.function_call_trace[0].model_refs
    )


def test_structure_relation_effect_simulation_work_on_real_selected_models():
    fixture_root = ROOT / "feedback_loop/fixtures/selected_models"
    cases = {
        "0000": fixture_root / "0000/STM_0.fcstm",
        "0006": fixture_root / "0006/STM_0.fcstm",
        "0029": fixture_root / "0029/STM_0.fcstm",
        "0050": fixture_root / "0050/STM_0.fcstm",
    }

    # The predicate hot-starts the configuration the trigger belongs to instead
    # of replaying a warm-up prefix by hand; `HumanDriving -> [*] : PowerOff` is
    # the edge the requirement is about.
    env0000 = EvalEnvironment(model_text=cases["0000"].read_text(encoding="utf-8"))
    assert env0000.eval_assert(
        "terminates(scope='HighLevelDrivingModule.HumanDriving', "
        "trigger='HighLevelDrivingModule.PowerOff') is True",
        "0000 PowerOff reaches top-level final",
        required_function_families=["simulation"],
    ).result == "true"

    env0006 = EvalEnvironment(model_text=cases["0006"].read_text(encoding="utf-8"))
    assert env0006.eval_assert(
        "edge_declared(source='Root.Searching', trigger='Root.Task_Assignment_Received', target='Root.Attack')",
        "0006 has task assignment relation",
        required_function_families=["relation"],
    ).result == "true"

    # Predicates name real paths, so the three families have to be exercised per
    # model rather than through one model-agnostic count expression.
    p29, p50 = "llms_emp_feedback_final_0029", "llms_emp_feedback_final_0050"
    three_families = {
        "0029": (
            "all(["
            f"state_declared(state='{p29}.HighwayMode.cruise', kind='leaf'), "
            f"edge_declared(source='{p29}.HighwayMode.lane_change', "
            f"trigger='{p29}.lane_change_completed', target='{p29}.HighwayMode.cruise'), "
            f"effect_declared(source='{p29}.HighwayMode.enter_hwy', trigger='{p29}.enter_', "
            "variable='R45RouteToken', sign='positive')"
            "])"
        ),
        "0050": (
            "all(["
            f"state_declared(state='{p50}.AutonomousMode.SubState1', kind='leaf'), "
            f"edge_declared(source='{p50}.HumanDrivingMode', "
            f"trigger='{p50}._front_distance_10', target='{p50}.AutonomousMode'), "
            f"effect_declared(source='{p50}.AutonomousMode.SubState1', trigger='{p50}.Power_Off', "
            "variable='R45RouteToken', sign='positive')"
            "])"
        ),
    }
    for key, expression in three_families.items():
        env = EvalEnvironment(model_text=cases[key].read_text(encoding="utf-8"), formal_verification_enabled=False)
        assert env.eval_assert(
            expression,
            f"{key} exposes structure, relation and effect facts",
            required_function_families=["structure", "relation", "effect"],
        ).result == "true"


def test_fbmcq_structured_query_uses_formal_family_with_fake_backend():
    def fake_bmc_runner(_model_path, query_path, **_kwargs):
        # The predicate writes the query now, so the fake has to answer the query
        # it was handed: FBMCQAPI rejects a report whose kind or bound disagrees
        # with the parsed one, which is what keeps a stale backend from being
        # read as a verdict.
        parsed = parse_bmc_query(Path(query_path).read_text(encoding="utf-8"))
        return (
            json.dumps(
                {
                    "result": {"status": "sat", "property_satisfied": True},
                    "property": {
                        "kind": parsed.property.kind,
                        "bound": parsed.property.bound,
                    },
                    "replay": {"ok": True},
                }
            ),
            0,
        )

    env = EvalEnvironment(model_text=MODEL, bmc_runner=fake_bmc_runner)
    result = env.eval_assert(
        "invariant(scope='Root.Idle', condition='active(\"Root.Done\")', bound=3) is True",
        "formal bounded query",
        required_function_families=["formal"],
    )
    obs = FBMCQAPI(MODEL, bmc_runner=fake_bmc_runner).fbmcq(
        'check reach <= 3: active("Root.Done");'
    )

    assert result.result == "true"
    assert result.actual_function_families == ("formal",)
    assert obs.query_origin == "exact_agent_query"
    assert obs.formal_bound == 3


def test_formal_query_causality_rejects_bare_reach_but_accepts_context():
    bare = formal_query_causality(
        'check reach <= 5: active("Root.Done");'
    )
    event_assumption = formal_query_causality(
        'assume event("Root.go", 0) == true;\n'
        'check reach <= 5: active("Root.Done");'
    )
    hot_start = formal_query_causality(
        'init state("Root.Idle");\n'
        'check reach <= 5: active("Root.Done");'
    )
    response = formal_query_causality(
        'check response <= 5:\n'
        'trigger event("Root.go", current)\n'
        '-> within 3 active("Root.Done");'
    )

    assert bare["causal"] is False
    assert event_assumption["causal"] is True
    assert hot_start["causal"] is True
    assert response["causal"] is True
