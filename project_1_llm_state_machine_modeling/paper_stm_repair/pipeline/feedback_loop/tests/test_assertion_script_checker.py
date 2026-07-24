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
        "seen = transition_exists(source='Root.Idle', event='Root.go', target='Root.Done')\nassert seen, '[REQ-001][AST-001-01] transition missing'",
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
        "assert transition_exists(source='Root.Done', event='Root.go', target='Root.Idle'), '[REQ-001][AST-001-01] reverse transition missing'",
        required_function_families=["relation"],
    )
    prefix_assertion_error = checker.check(
        "helper_ok = broken_helper()\nassert helper_ok, '[REQ-001][AST-001-02] helper failed'"
    )
    non_bool = checker.check("assert states(), '[REQ-001][AST-001-03] non bool'")

    assert sealed.outcome == "sealed_false"
    assert sealed.value is False
    assert prefix_assertion_error.outcome == "invalid"
    assert prefix_assertion_error.sealed.error["type"] == "AssertionError"
    assert non_bool.outcome == "invalid"
    assert non_bool.sealed.error["type"] == "NonBoolTerminalAssert"


def test_lambda_local_binding_can_reuse_one_read_only_simulation_result():
    checker = AssertionChecker(EvalEnvironment(model_text=MODEL))
    result = checker.check(
        "assert (lambda sim: bool(sim.final.is_active('Root.Done')))(simulate(cycles=[['Root.go']], initial_state='Root.Idle', initial_vars={})), '[REQ-001][AST-001-01] Done did not become active'",
        required_function_families=["simulation"],
    )
    assert result.outcome == "valid"
    assert result.actual_function_families == ("simulation",)


def test_environment_docs_list_readable_api_surface():
    for needle in [
        "terminal expression must evaluate to a strict `bool`",
        "states",
        "transition_exists",
        "effect_deltas",
        "simulate",
        "fbmcq",
        "mapped_source_refs",
    ]:
        assert needle in ASSERTION_ENVIRONMENT_API_DOCS


def test_structure_relation_effect_simulation_work_on_real_selected_models():
    fixture_root = ROOT / "feedback_loop/fixtures/selected_models"
    cases = {
        "0000": fixture_root / "0000/STM_0.fcstm",
        "0006": fixture_root / "0006/STM_0.fcstm",
        "0029": fixture_root / "0029/STM_0.fcstm",
        "0050": fixture_root / "0050/STM_0.fcstm",
    }

    env0000 = EvalEnvironment(model_text=cases["0000"].read_text(encoding="utf-8"))
    assert env0000.eval_assert(
        "simulate(cycles=[[], ['HighLevelDrivingModule.PowerOn'], ['HighLevelDrivingModule.PowerOff']]).final.is_ended is True",
        "0000 PowerOff reaches top-level final",
        required_function_families=["simulation"],
    ).result == "true"

    env0006 = EvalEnvironment(model_text=cases["0006"].read_text(encoding="utf-8"))
    assert env0006.eval_assert(
        "transition_exists(source='Root.Searching', event='Root.Task_Assignment_Received', target='Root.Attack')",
        "0006 has task assignment relation",
        required_function_families=["relation"],
    ).result == "true"

    for key in ("0029", "0050"):
        env = EvalEnvironment(model_text=cases[key].read_text(encoding="utf-8"), formal_verification_enabled=False)
        assert env.eval_assert(
            "len(states()) > 0 and len(transitions()) > 0 and any(delta > 0 for _, delta in effect_deltas())",
            f"{key} exposes structure, relation and effect facts",
            required_function_families=["structure", "relation", "effect"],
        ).result == "true"


def test_fbmcq_structured_query_uses_formal_family_with_fake_backend():
    def fake_bmc_runner(*_args, **_kwargs):
        return (
            json.dumps(
                {
                    "result": {"status": "sat", "property_satisfied": True},
                    "property": {"kind": "reach", "bound": 3, "polarity": "exists"},
                    "replay": {"ok": True},
                }
            ),
            0,
        )

    env = EvalEnvironment(model_text=MODEL, bmc_runner=fake_bmc_runner)
    result = env.eval_assert(
        "fbmcq('check reach <= 3: active(\"Root.Done\");').holds is True",
        "formal reachability query",
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
