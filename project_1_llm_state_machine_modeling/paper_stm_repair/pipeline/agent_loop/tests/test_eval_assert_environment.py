from __future__ import annotations

import inspect
from concurrent.futures import ThreadPoolExecutor

from paper_stm_repair_loop.config import SELECTED_ROOT
from paper_stm_repair_loop.eval_env import EvalEnvironment
from paper_stm_repair_loop.eval_env.runtime import (
    ALLOWED_FUNCTION_FAMILIES,
    RESULT_FALSE,
    RESULT_NO_MODEL_EVIDENCE,
    RESULT_NON_BOOL,
    RESULT_REQUIRED_FAMILY_MISSING,
    RESULT_TRUE,
    RESULT_UNSUPPORTED,
    RESULT_UNTRACKED,
)


MODEL = """state Root {
    event go;
    event back;
    state Idle;
    state Done;
    [*] -> Idle;
    Idle -> Done : go;
    Done -> Idle : back;
}
"""


EFFECT_MODEL = """def int uav_count = 3;
state Root {
    event Attack_Complete;
    state Attack;
    state Searching;
    [*] -> Attack;
    Attack -> Searching : Attack_Complete effect {
        uav_count = uav_count - 1;
    }
}
"""


NO_EFFECT_MODEL = """def int uav_count = 3;
state Root {
    event Attack_Complete;
    state Attack;
    state Searching;
    [*] -> Attack;
    Attack -> Searching : Attack_Complete;
}
"""


TERMINATING_MODEL = """state Root {
    event stop;
    state Running;
    [*] -> Running;
    Running -> [*] : stop;
}
"""


def test_eval_environment_public_docstring_declares_contract_sections():
    doc = inspect.getdoc(EvalEnvironment) or ""
    for marker in [
        "Parameters",
        "Returns",
        "Execution",
        "Failure semantics",
        "Evidence limitations",
        "Permissions",
        "Example",
    ]:
        assert marker in doc
    assert "open" in doc
    assert "__import__" in doc
    assert "not a malicious-code sandbox" in doc


def test_direct_eval_positive_bool_expression_returns_true_with_structure_trace():
    env = EvalEnvironment(model_text=MODEL)

    result = env.eval_assert(
        "transition_exists(source='Root.Idle', event='Root.go', target='Root.Done')",
        "go should move Idle to Done",
        required_function_families=["relation"],
    )

    assert result.result == RESULT_TRUE
    assert result.match_status == "matches"
    assert result.value is True
    assert result.vars_hash_before == result.vars_hash_after
    assert result.function_registry_hash
    assert [call.function for call in result.function_call_trace] == ["transition_exists"]
    assert result.actual_function_families == ("relation",)
    assert result.to_json()["function_call_trace"][0]["kwargs_hash"]


def test_direct_eval_false_expression_is_contradiction_not_exception():
    env = EvalEnvironment(model_text=MODEL)

    result = env.eval_assert(
        "transition_exists(source='Root.Done', event='Root.go', target='Root.Idle')",
        "wrong direction should not exist",
        required_function_families=["relation"],
    )

    assert result.result == RESULT_FALSE
    assert result.match_status == "contradicts"
    assert result.value is False


def test_direct_eval_executes_inside_agent_worker_thread():
    env = EvalEnvironment(model_text=MODEL, timeout_seconds=2)
    with ThreadPoolExecutor(max_workers=1) as pool:
        result = pool.submit(
            env.eval_assert,
            "transition_exists(source='Root.Idle', event='Root.go', target='Root.Done')",
            "worker-thread regression",
            required_function_families=["relation"],
        ).result(timeout=5)
    assert result.result == RESULT_TRUE
    assert result.value is True


def test_non_bool_and_no_model_evidence_are_precise_inconclusive_results():
    env = EvalEnvironment(model_text=MODEL)

    non_bool = env.eval_assert("len(states())", "non-bool return", required_function_families=["structure"])
    no_model = env.eval_assert("1 + 1 == 2", "bare tautology")

    assert non_bool.result == RESULT_NON_BOOL
    assert non_bool.match_status == "inconclusive"
    assert non_bool.actual_function_families == ("structure",)
    assert no_model.result == RESULT_NO_MODEL_EVIDENCE
    assert no_model.match_status == "inconclusive"
    assert no_model.function_call_trace == ()


def test_required_family_missing_overrides_python_bool_result():
    env = EvalEnvironment(model_text=MODEL)

    result = env.eval_assert(
        "transition_exists(source='Root.Idle', event='Root.go', target='Root.Done')",
        "structure called but simulation was required",
        required_function_families=["relation", "simulation"],
    )

    assert result.result == RESULT_REQUIRED_FAMILY_MISSING
    assert result.value is True
    assert result.error == {"type": "RequiredFamilyMissing", "missing": ["simulation"]}


def test_function_family_enum_is_exact_and_rejects_legacy_fbmcq_source_mapping_names():
    env = EvalEnvironment(model_text=MODEL)

    assert ALLOWED_FUNCTION_FAMILIES == frozenset({"structure", "relation", "effect", "simulation", "formal", "mapping"})
    registry_families = {meta["family"] for meta in env.function_registry_hash and env._raw_functions.values() for meta in [{"family": meta[0]}]}
    assert registry_families <= ALLOWED_FUNCTION_FAMILIES
    assert "fbmcq" not in registry_families
    assert "source_mapping" not in registry_families

    legacy_formal = env.eval_assert("transition_exists(source='Root.Idle')", "legacy family", required_function_families=["fbmcq"])
    legacy_mapping = env.eval_assert("transition_exists(source='Root.Idle')", "legacy family", required_function_families=["source_mapping"])

    assert legacy_formal.result == RESULT_UNSUPPORTED
    assert legacy_formal.error["type"] == "InvalidFunctionFamily"
    assert legacy_mapping.result == RESULT_UNSUPPORTED
    assert legacy_mapping.error["invalid"] == ["source_mapping"]


def test_unknown_names_forbidden_builtins_dunder_and_unregistered_attrs_are_rejected_before_eval():
    env = EvalEnvironment(model_text=MODEL)

    for expr in [
        "missing_name()",
        "open('/tmp/forbidden')",
        "__import__('os').environ",
        "states()[0].__class__",
        "states()[0].secret",
    ]:
        result = env.eval_assert(expr, "reject untracked dependency")
        assert result.result == RESULT_UNTRACKED, expr
        assert result.function_call_trace == (), expr


def test_simulate_uses_cycle_semantics_and_final_view_method():
    env = EvalEnvironment(model_text=MODEL)

    result = env.eval_assert(
        "simulate(cycles=[[], ['Root.go']]).final.is_active('Root.Done')",
        "empty stabilization cycle then go",
        required_function_families=["simulation"],
    )

    assert result.result == RESULT_TRUE
    assert result.actual_function_families == ("simulation",)
    trace_hash = result.function_call_trace[0].result_hash
    assert trace_hash
    direct = env.simulation.simulate(cycles=[[], ["Root.go"]])
    assert len(direct.cycles) == 2
    assert direct.cycles[0].index == 0
    assert direct.cycles[1].index == 1
    assert direct.cycles[1].input_events == ("Root.go",)
    assert direct.cycles[1].is_active("Root.Done") is True
    assert direct.cycles[1].is_ended is False
    assert direct.model_sha256


def test_simulate_exposes_terminal_state_without_reading_current_state():
    env = EvalEnvironment(model_text=TERMINATING_MODEL)

    result = env.eval_assert(
        "simulate(cycles=[[], ['Root.stop']]).final.is_ended is True",
        "stop should terminate the root machine",
        required_function_families=["simulation"],
    )

    assert result.result == RESULT_TRUE
    assert result.match_status == "matches"
    direct = env.simulation.simulate(cycles=[[], ["Root.stop"]])
    assert direct.final.is_ended is True
    assert direct.final.active_states == ()


def test_manual_0000_power_off_reaches_top_level_final():
    model_path = (
        SELECTED_ROOT
        / "llms-emp-gpt4o-hldcs-manual-identity"
        / "model.fcstm"
    )
    env = EvalEnvironment(model_text=model_path.read_text(encoding="utf-8"))

    result = env.eval_assert(
        "simulate(cycles=[[], ['HighLevelDrivingModule.PowerOn'], "
        "['HighLevelDrivingModule.PowerOff']]).final.is_ended is True",
        "manual 0000 PowerOff should terminate the top-level machine",
        required_function_families=["simulation"],
    )

    assert result.result == RESULT_TRUE
    assert result.match_status == "matches"
    direct = env.simulation.simulate(
        cycles=[
            [],
            ["HighLevelDrivingModule.PowerOn"],
            ["HighLevelDrivingModule.PowerOff"],
        ]
    )
    assert direct.final.is_ended is True
    assert direct.final.active_states == ()


def test_effect_delta_reuses_structured_effects_and_missing_effect_is_false_with_contract_expression():
    good = EvalEnvironment(model_text=EFFECT_MODEL)
    missing = EvalEnvironment(model_text=NO_EFFECT_MODEL)

    expr = "(effect_delta(source='Root.Attack', event='Root.Attack_Complete', variable='uav_count') or 0) < 0"

    good_result = good.eval_assert(
        expr, "decrement expected", required_function_families=["effect"]
    )
    missing_result = missing.eval_assert(
        expr,
        "missing decrement should be false",
        required_function_families=["effect"],
    )

    assert good_result.result == RESULT_TRUE
    assert missing_result.result == RESULT_FALSE
    assert good_result.actual_function_families == ("effect",)


def test_effect_deltas_open_interface_traces_effect_family_without_variable_probe():
    good = EvalEnvironment(model_text=EFFECT_MODEL)
    missing_effect = EvalEnvironment(model_text=NO_EFFECT_MODEL)
    no_variables = EvalEnvironment(model_text=MODEL)
    expr = (
        "any(delta < 0 for _, delta in "
        "effect_deltas(source='Root.Attack', event='Root.Attack_Complete', target='Root.Searching'))"
    )

    good_result = good.eval_assert(
        expr, "some matching effect decrements", required_function_families=["effect"]
    )
    missing_result = missing_effect.eval_assert(
        expr,
        "missing effect is a contradiction",
        required_function_families=["effect"],
    )
    no_variables_result = no_variables.eval_assert(
        expr,
        "no variables/effects is stable absence",
        required_function_families=["effect"],
    )

    assert good.effects.effect_deltas(
        source="Root.Attack", event="Root.Attack_Complete", target="Root.Searching"
    ) == (("uav_count", -1),)
    assert good_result.result == RESULT_TRUE
    assert missing_result.result == RESULT_FALSE
    assert no_variables_result.result == RESULT_FALSE
    for result in (good_result, missing_result, no_variables_result):
        assert result.actual_function_families == ("effect",)
        assert [call.function for call in result.function_call_trace] == ["effect_deltas"]
