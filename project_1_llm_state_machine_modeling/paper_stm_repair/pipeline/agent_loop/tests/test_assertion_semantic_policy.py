from __future__ import annotations

from paper_stm_repair_loop.assertion_policy import (
    ERROR_CARDINALITY_COMPARISON_REQUIRED,
    ERROR_CONTINUITY_EVIDENCE_REQUIRED,
    ERROR_CONTINUITY_EXISTENTIAL_FORMAL_TOO_WEAK,
    ERROR_EFFECTS_BOOL_SUBSTITUTE,
    ERROR_EFFECT_DELTA_DIRECTION_REQUIRED,
    ERROR_SIMULATE_FIRST_CYCLE_REQUIRED,
    ERROR_CONDITION_TRIGGER_REQUIRED,
    ERROR_TRANSITION_TARGET_REQUIRED,
    validate_assertion_semantic_policy,
)


def _req(requirement_id: str, dimension: str, cue_text: str) -> dict[str, object]:
    return {
        "requirement_id": requirement_id,
        "dimension": dimension,
        "cue_text": cue_text,
    }


def _codes(errors: list[str]) -> set[str]:
    return {item.split(":", 1)[0] for item in errors}


def test_simulate_literal_cycles_must_start_with_empty_cycle():
    errors = validate_assertion_semantic_policy(
        "simulate(cycles=[['start'], []]).final.is_active('Root.Search')",
        [],
    )
    assert _codes(errors) == {ERROR_SIMULATE_FIRST_CYCLE_REQUIRED}

    assert (
        validate_assertion_semantic_policy(
            "simulate(cycles=[[], ['start']]).final.is_active('Root.Search')",
            [],
        )
        == []
    )


def test_decrease_effect_requires_negative_effect_delta_not_bool_effects():
    reqs = [_req("REQ-EFFECT", "effect", "decreases")]
    errors = validate_assertion_semantic_policy(
        "bool(effects(source='A', event='done', variable='count'))",
        reqs,
    )
    assert _codes(errors) == {
        ERROR_EFFECTS_BOOL_SUBSTITUTE,
        ERROR_EFFECT_DELTA_DIRECTION_REQUIRED,
    }

    assert (
        validate_assertion_semantic_policy(
            "(effect_delta(source='A', event='done', variable='count') or 0) < 0",
            reqs,
        )
        == []
    )


def test_increment_effect_requires_positive_effect_delta():
    reqs = [_req("REQ-EFFECT", "effect", "increments")]
    errors = validate_assertion_semantic_policy(
        "(effect_delta(source='A', event='done', variable='count') or 0) < 0",
        reqs,
    )
    assert _codes(errors) == {ERROR_EFFECT_DELTA_DIRECTION_REQUIRED}

    assert (
        validate_assertion_semantic_policy(
            "0 < (effect_delta(source='A', event='done', variable='count') or 0)",
            reqs,
        )
        == []
    )


def test_continuity_requires_formal_or_two_simulations():
    reqs = [_req("REQ-CONT", "continuity", "continuously")]
    errors = validate_assertion_semantic_policy(
        "initial_child('Root.Searching') == 'Root.Searching.Area1' and simulate(cycles=[[]]).cycles[0].is_active('Root.Searching')",
        reqs,
    )
    assert _codes(errors) == {ERROR_CONTINUITY_EVIDENCE_REQUIRED}

    assert (
        validate_assertion_semantic_policy(
            "simulate(cycles=[[], []]).final.is_active('A') and simulate(cycles=[[], ['tick']]).final.is_active('A')",
            reqs,
        )
        == []
    )
    assert _codes(
        validate_assertion_semantic_policy(
            "fbmcq('check invariant <= 4: active(\"Root.Searching\");').holds is True",
            reqs,
        )
    ) == {ERROR_CONTINUITY_EVIDENCE_REQUIRED}
    assert validate_assertion_semantic_policy(
        "all([fbmcq('check response <= 4: trigger event(\"Root.Intercepted\", current) -> within 3 active(\"Root.Searching\");').holds is True, fbmcq('check response <= 4: trigger event(\"Root.Attack_Complete\", current) -> within 1 active(\"Root.Searching\");').holds is True])",
        reqs,
    ) == []


def test_continuity_rejects_existential_path_as_exhaustive_evidence():
    reqs = [_req("REQ-CONT", "continuity", "continuously")]

    errors = validate_assertion_semantic_policy(
        "fbmcq('check exists_always <= 4: active(\"Root.Searching\");').holds is True",
        reqs,
    )

    assert _codes(errors) == {ERROR_CONTINUITY_EXISTENTIAL_FORMAL_TOO_WEAK}


def test_cardinality_requires_structural_function_number_and_direction():
    exact = [_req("REQ-CARD", "cardinality", "three different areas")]
    assert (
        validate_assertion_semantic_policy(
            "len(states(parent='Root.Searching', recursive=False)) == 3",
            exact,
        )
        == []
    )
    errors = validate_assertion_semantic_policy(
        "len(states(parent='Root.Searching', recursive=False)) >= 3",
        exact,
    )
    assert _codes(errors) == {ERROR_CARDINALITY_COMPARISON_REQUIRED}

    at_least = [_req("REQ-CARD", "cardinality", "at least 3 areas")]
    assert (
        validate_assertion_semantic_policy(
            "3 <= len(states(parent='Root.Searching', recursive=False))",
            at_least,
        )
        == []
    )
    assert _codes(
        validate_assertion_semantic_policy(
            "len(states(parent='Root.Searching', recursive=False)) <= 3",
            at_least,
        )
    ) == {ERROR_CARDINALITY_COMPARISON_REQUIRED}

    at_most = [_req("REQ-CARD", "cardinality", "at most 3 areas")]
    assert (
        validate_assertion_semantic_policy(
            "len(states(parent='Root.Searching', recursive=False)) <= 3",
            at_most,
        )
        == []
    )


def test_transition_requirement_rejects_event_only_relation():
    reqs = [_req("REQ-TRANSITION", "transition", "enters")]

    errors = validate_assertion_semantic_policy(
        "transition_exists(event='Root.Power_On')",
        reqs,
    )

    assert _codes(errors) == {ERROR_TRANSITION_TARGET_REQUIRED}
    assert validate_assertion_semantic_policy(
        "transition_exists(source='Root.Off', event='Root.Power_On', target='Root.Ready')",
        reqs,
    ) == []


def test_condition_requirement_rejects_unbound_bare_relation():
    reqs = [_req("REQ-CONDITION", "condition", "when")]

    errors = validate_assertion_semantic_policy(
        "transition_exists(source='Root.Off', target='Root.Ready')",
        reqs,
    )

    assert _codes(errors) == {ERROR_CONDITION_TRIGGER_REQUIRED}
    assert validate_assertion_semantic_policy(
        "transition_exists(source='Root.Off', event='Root.Power_On', target='Root.Ready')",
        reqs,
    ) == []
