from __future__ import annotations

from paper_stm_repair_loop.eval_env import EvalEnvironment, FrozenView
from paper_stm_repair_loop.eval_env.exceptions import UnsupportedEvidence
from paper_stm_repair_loop.eval_env.provenance import audit_expression
from paper_stm_repair_loop.eval_env.runtime import (
    RESULT_EXCEPTION,
    RESULT_TIMEOUT,
    RESULT_TRUE,
    RESULT_UNSUPPORTED,
    RESULT_UNTRACKED,
)


MODEL = """state Root {
    event go;
    state Idle;
    state Done;
    [*] -> Idle;
    Idle -> Done : go;
}
"""


def test_frozen_extra_view_allows_registered_field_and_rejects_unregistered_field():
    observation = FrozenView(
        "fixture",
        {"ok": True, "secret": "not registered"},
        allowed_fields={"ok"},
    )
    env = EvalEnvironment(model_text=MODEL, extra_vars={"obs": observation})

    allowed = env.eval_assert("obs.ok and transition_exists(source='Root.Idle')", "registered field", required_function_families=["relation"])
    rejected = env.eval_assert("obs.secret", "unregistered field")

    assert allowed.result == RESULT_TRUE
    assert rejected.result == RESULT_UNTRACKED
    assert any(issue["code"] == "unregistered_object_attribute" for issue in rejected.audit["issues"])


def test_public_structure_view_fields_are_accepted_through_function_results():
    env = EvalEnvironment(model_text=MODEL)

    leaf = env.eval_assert(
        "states(name='Root.Idle')[0].is_leaf is True and "
        "states(name='Root.Idle')[0].is_composite is False and "
        "states(name='Root.Idle')[0].parent_path == 'Root'",
        "Use the documented public State view fields.",
        required_function_families=["structure"],
    )
    transition = env.eval_assert(
        "transitions(source='Root.Idle')[0].transition_index == 1 and "
        "transitions(source='Root.Idle')[0].is_forced is False",
        "Use the documented public Transition view fields.",
        required_function_families=["relation"],
    )

    assert leaf.result == RESULT_TRUE
    assert leaf.audit["ok"] is True
    assert transition.result == RESULT_TRUE
    assert transition.audit["ok"] is True


def test_call_trace_records_actual_exception_and_unsupported_dependency():
    def unsupported() -> bool:
        raise UnsupportedEvidence("public API not available")

    def broken() -> bool:
        raise ValueError("boom")

    env = EvalEnvironment(
        model_text=MODEL,
        extra_functions={
            "unsupported_fact": ("formal", unsupported),
            "broken_fact": ("structure", broken),
        },
    )

    unsupported_result = env.eval_assert("unsupported_fact()", "unsupported API", required_function_families=["formal"])
    broken_result = env.eval_assert("broken_fact()", "runtime exception", required_function_families=["structure"])

    assert unsupported_result.result == RESULT_UNSUPPORTED
    assert unsupported_result.function_call_trace[0].status == "exception"
    assert unsupported_result.function_call_trace[0].exception_type == "UnsupportedEvidence"
    assert broken_result.result == RESULT_EXCEPTION
    assert broken_result.function_call_trace[0].exception_type == "ValueError"


def test_timeout_is_precise_terminal_result_for_long_running_expression():
    env = EvalEnvironment(model_text=MODEL, timeout_seconds=1)

    result = env.eval_assert("sum(1 for _ in iter(int, 1)) == 0", "infinite generator")

    assert result.result == RESULT_TIMEOUT
    assert result.match_status == "inconclusive"


def test_source_mapping_family_has_frozen_hashes_and_trace():
    env = EvalEnvironment(
        model_text=MODEL,
        source_mappings=[
            {
                "source_ref": "SEG-NL-003",
                "model_ref": "transition:Root.Idle:Root.go",
                "relation_policy": "exact_identity",
                "producer": "fixture",
            }
        ],
    )

    result = env.eval_assert(
        "'SEG-NL-003' in mapped_source_refs('transition:Root.Idle:Root.go')",
        "identity source mapping should exist",
        required_function_families=["mapping"],
    )

    assert result.result == RESULT_TRUE
    assert result.actual_function_families == ("mapping",)
    assert result.vars_hash_before == result.vars_hash_after
    assert result.function_call_trace[0].family == "mapping"
    assert result.function_call_trace[0].family != "source_mapping"
    assert result.function_call_trace[0].result_hash


def test_formal_family_uses_structured_fbmcq_result_without_exception_string_parsing():
    def fake_bmc_runner(*_args, **_kwargs):
        return (
            '{"result":{"status":"sat","property_satisfied":true,"outcome":"property_satisfied"},'
            '"property":{"kind":"reach","bound":3,"polarity":"exists"},"replay":{"ok":true}}',
            0,
        )

    env = EvalEnvironment(model_text=MODEL, bmc_runner=fake_bmc_runner)

    result = env.eval_assert(
        "fbmcq('check reach <= 3: active(\"Root.Done\");').holds is True",
        "bounded property should hold in fake structured result",
        required_function_families=["formal"],
    )

    assert result.result == RESULT_TRUE
    assert result.actual_function_families == ("formal",)
    assert result.function_call_trace[0].family == "formal"
    assert result.function_call_trace[0].family != "fbmcq"
    assert result.function_call_trace[0].function == "fbmcq"


def test_formal_family_treats_exit_one_as_stable_property_false():
    def fake_bmc_runner(*_args, **_kwargs):
        return (
            '{"result":{"status":"unsat","property_satisfied":false,"outcome":"no_witness"},'
            '"property":{"kind":"exists_always","bound":3,"polarity":"witness"},"replay":null}',
            1,
        )

    env = EvalEnvironment(model_text=MODEL, bmc_runner=fake_bmc_runner)
    result = env.eval_assert(
        "fbmcq('check exists_always <= 3: active(\"Root.Done\");').holds is True",
        "A stable false property must contradict rather than become unsupported.",
        required_function_families=["formal"],
    )

    assert result.result == "false"
    assert result.match_status == "contradicts"
    assert result.error is None


def test_comprehension_target_is_a_local_provenance_binding():
    report = audit_expression(
        "any(check(name) for name in candidates)",
        allowed_names={"any", "check", "candidates"},
    )
    assert report.ok is True
    assert "name" in report.names
