"""`<undeclared>` is a verdict only when the declaration table backs it.

Pair 0006's expected defect is that the NL requires the UAV count to drop after
an attack and the model declares no variable that could drop.  The splitter
encoded that correctly -- `variable_delta_after(..., variable="<undeclared>",
sign="negative")` -- and the run still missed it, because the controller treated
the resulting refusal as a non-executable assertion: two repair attempts, budget
exhausted, requirement filed as a coverage gap.  A defect reported as an
unchecked obligation is a recall loss, and every gate was green while it
happened.

The first attempt at a fix sealed a false for *any* `<undeclared>` binding, on
the strength of a string comparison that never read a declaration.  That is a
worse bug than the one it replaced: it manufactures a defect against a model
that does not have one, and it pays better than an honest guess -- a wrong
variable name costs a repair round, a shrug earns a finding.

So the line these tests draw is: the absence must be *readable*.  An empty table
of the right kind seals a false; a populated one sends the claim back to name an
element; an expression binding has no table at all and can never seal.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.assertions import build_eval_environment  # noqa: E402
from paper_stm_feedback_loop.assertions.checker import AssertionChecker  # noqa: E402
from paper_stm_feedback_loop.assertions.exceptions import (  # noqa: E402
    UndeclaredTerm,
    UnsupportedEvidence,
)

#: Pair 0006's shape: states and events, but no variable of the author's own.
MODEL_NO_VARS = """state Root {
    event go;
    event stop;
    state Idle;
    state Busy;
    [*] -> Idle;
    Idle -> Busy : /go;
    Busy -> Idle : /stop;
}
"""

#: The same machine with a variable the author declared.
MODEL_WITH_VARS = """def int c = 0;
state Root {
    event go;
    event stop;
    state Idle;
    state Busy;
    [*] -> Idle;
    Idle -> Busy : /go effect { c = c + 1; };
    Busy -> Idle : /stop;
}
"""

#: Pairs 0000 and 0006 declare exactly one variable and the converter owns it.
ROUTE_CONTROL_EXCLUSION = ["compiler:route_control:c"]


def _checker(
    model: str = MODEL_NO_VARS, exclusions: list[str] | None = None
) -> AssertionChecker:
    env = build_eval_environment(
        model_text=model,
        source_mappings=[],
        source_exclusions=exclusions or [],
        timeout_seconds=30,
        fbmcq_solver_timeout_ms=20_000,
        fbmcq_max_bound=6,
        fbmcq_process_wall_seconds=25.0,
    )
    return AssertionChecker(environment=env)


def _script(call: str) -> str:
    return f'assert {call} is True, "[REQ-001][AST-REQ-001-1] the obligation must hold"'


def _message(result) -> str:
    return str((result.sealed.error or {}).get("message", ""))


# --------------------------------------------------------------------------
# An empty table of the right kind is a readable absence, so it seals a false
# --------------------------------------------------------------------------

VARIABLE_CALLS = [
    'variable_delta_after(source="Root.Idle", trigger="Root.go", '
    'variable="<undeclared>", sign="negative")',
    'effect_declared(source="Root.Idle", trigger="Root.go", '
    'variable="<undeclared>", sign="negative")',
]


@pytest.mark.parametrize("call", VARIABLE_CALLS)
def test_a_model_with_no_variables_seals_a_false(call):
    result = _checker(MODEL_NO_VARS).check(
        _script(call), reason="undeclared", required_function_families=()
    )
    assert result.sealed.outcome == "sealed_false", result.sealed.metadata
    assert result.sealed.value is False
    assert result.sealed.metadata["verdict_basis"] == "declared_vocabulary_absence"
    assert result.sealed.metadata["undeclared_bindings"] == ["variable"]


@pytest.mark.parametrize("call", VARIABLE_CALLS)
def test_a_model_whose_only_variable_is_compiler_owned_also_seals(call):
    """Pair 0006's exact shape.

    The effect facade already drops route-control variables from every answer,
    so a model with nothing but one of those has, as far as any evidence call is
    concerned, no variables at all.  Counting it would refuse the very claim the
    expected defect is made of.
    """

    result = _checker(MODEL_WITH_VARS, ROUTE_CONTROL_EXCLUSION).check(
        _script(call), reason="undeclared", required_function_families=()
    )
    assert result.sealed.outcome == "sealed_false", result.sealed.metadata
    assert result.sealed.metadata["verdict_basis"] == "declared_vocabulary_absence"


def test_the_sealed_verdict_records_the_table_it_read():
    """`verdict_basis` must be backed by something in the evidence record."""

    result = _checker(MODEL_NO_VARS).check(
        _script(VARIABLE_CALLS[0]), reason="undeclared", required_function_families=()
    )
    refs = [
        ref
        for record in result.function_call_trace
        for ref in (getattr(record, "model_refs", ()) or ())
    ]
    assert "declaration_table:variables:empty" in refs, refs


def test_the_sealed_verdict_claims_no_evidence_family_it_did_not_gather():
    """No facade answered, so the observed family list is empty.

    Naming `structure` here -- which the first version of this fix did -- puts an
    evidence claim in the run record with no call behind it, and
    `bind_attribution` reads this field to decide whether a simulation was
    involved.
    """

    result = _checker(MODEL_NO_VARS).check(
        _script(VARIABLE_CALLS[0]), reason="undeclared", required_function_families=()
    )
    assert result.actual_function_families == ()


def test_a_required_family_demand_does_not_turn_the_verdict_back_into_invalid():
    """A Family B requirement asks for `simulation`; nothing was simulated.

    Failing the family check here would put the requirement straight back on the
    repair path this test exists to close.
    """

    result = _checker(MODEL_NO_VARS).check(
        _script(VARIABLE_CALLS[0]),
        reason="undeclared",
        required_function_families=("simulation",),
    )
    assert result.sealed.outcome == "sealed_false"


# --------------------------------------------------------------------------
# A populated table is not an absence, so it must not seal
# --------------------------------------------------------------------------


@pytest.mark.parametrize("call", VARIABLE_CALLS)
def test_a_populated_table_sends_the_claim_back_instead_of_sealing(call):
    """The defect this guards against, stated as a test.

    Same model, same transition, a variable that genuinely changes.  Binding
    `<undeclared>` must not be a cheaper route to a finding than naming it.
    """

    result = _checker(MODEL_WITH_VARS).check(
        _script(call), reason="lazy", required_function_families=()
    )
    assert result.sealed.outcome == "invalid", result.sealed.metadata
    assert "does declare elements of that kind" in _message(result), _message(result)
    assert "1 declared variables" in _message(result), _message(result)


@pytest.mark.parametrize(
    "call",
    [
        'state_declared(state="<undeclared>", kind="leaf")',
        'cardinality(scope="<undeclared>", count=3)',
        'occupancy_after(source="<undeclared>", trigger="Root.go", target="Root.Busy")',
        'edge_declared(source="Root.Idle", trigger="<undeclared>", target="Root.Busy")',
    ],
)
def test_a_state_or_event_binding_can_never_seal(call):
    """Every model declares states and events, so their table is never empty.

    A claim about a state the model lacks is a claim about a *specific* state,
    and the producer has to say which; `<undeclared>` says nothing checkable.
    """

    result = _checker(MODEL_NO_VARS).check(
        _script(call), reason="undeclared", required_function_families=()
    )
    assert result.sealed.outcome == "invalid", result.sealed.metadata


@pytest.mark.parametrize(
    "call",
    [
        'persists_until(state="Root.Idle", release="<undeclared>", bound=2)',
        'invariant(scope="Root.Idle", condition="<undeclared>", bound=2)',
    ],
)
def test_an_expression_binding_has_no_table_and_never_seals(call):
    """A boolean expression has no declaration list to be absent from."""

    result = _checker(MODEL_NO_VARS).check(
        _script(call), reason="undeclared", required_function_families=()
    )
    assert result.sealed.outcome == "invalid", result.sealed.metadata
    assert "expressions, not declared elements" in _message(result), _message(result)


# --------------------------------------------------------------------------
# One raising arm must not decide arms that never ran
# --------------------------------------------------------------------------


def test_an_undeclared_arm_does_not_seal_a_whole_fold():
    """Python short-circuits left to right, so the later arms never evaluate.

    Verified on pair 0000: `any([<undeclared>, occupancy_after(...)])` where the
    second arm is True turned a satisfied requirement into a confirmed issue.
    """

    script = _script(
        'any([variable_delta_after(source="Root.Idle", trigger="Root.go", '
        'variable="<undeclared>", sign="negative"), '
        'occupancy_after(source="Root.Idle", trigger="Root.go", target="Root.Busy")])'
    )
    result = _checker(MODEL_NO_VARS).check(
        script, reason="fold", required_function_families=()
    )
    assert result.sealed.outcome == "invalid", result.sealed.metadata
    assert "its own assertion" in _message(result), _message(result)


def test_the_same_claim_alone_still_seals():
    """The fold is the problem, not the claim -- control for the test above."""

    result = _checker(MODEL_NO_VARS).check(
        _script(VARIABLE_CALLS[0]), reason="alone", required_function_families=()
    )
    assert result.sealed.outcome == "sealed_false"


def test_a_fold_with_the_undeclared_arm_last_also_refuses():
    """Order must not decide whether a run reports a defect.

    With the raising arm second, `all([...])` evaluates the first arm, so the
    trace is non-empty and the same rule applies.  If it did not, the verdict
    would depend on how the producer happened to order a list.
    """

    script = _script(
        'all([occupancy_after(source="Root.Idle", trigger="Root.go", target="Root.Busy"), '
        'variable_delta_after(source="Root.Idle", trigger="Root.go", '
        'variable="<undeclared>", sign="negative")])'
    )
    result = _checker(MODEL_NO_VARS).check(
        script, reason="fold", required_function_families=()
    )
    assert result.sealed.outcome == "invalid", result.sealed.metadata


# --------------------------------------------------------------------------
# The two refusal kinds stay distinguishable
# --------------------------------------------------------------------------


def test_an_ordinary_refusal_is_still_invalid():
    """Only a readable absence is a verdict; a query that cannot decide is not.

    `guard_distinguishable` on a transition that does not exist genuinely cannot
    answer, and turning that into a false would report a defect the model does
    not have.
    """

    result = _checker(MODEL_NO_VARS).check(
        _script('guard_distinguishable(source="Root.Busy", trigger="Root.go")'),
        reason="refusal",
        required_function_families=(),
    )
    assert result.sealed.outcome == "invalid", result.sealed.metadata


def test_undeclared_term_is_a_kind_of_unsupported_evidence():
    """Callers that only know the parent class keep working."""

    assert issubclass(UndeclaredTerm, UnsupportedEvidence)


def test_the_repair_path_no_longer_lists_undeclared_as_unrepairable():
    """The marker that filed it as a coverage gap must be gone from the source.

    Belt and braces: the behaviour above is what matters, but the quarantine
    list is reachable from a different branch and a re-added marker would
    silently restore the old outcome.
    """

    nodes = (SRC / "paper_stm_feedback_loop/discover/nodes.py").read_text()
    marker_lines = [
        line for line in nodes.splitlines() if "unrepairable_markers = " in line
    ]
    assert marker_lines, "the quarantine list moved; re-point this check"
    assert all("UNDECLARED" not in line for line in marker_lines), marker_lines


# --------------------------------------------------------------------------
# The vocabulary must not offer a variable the evidence layer will not answer on
# --------------------------------------------------------------------------


def test_route_control_variables_are_listed_apart_from_the_authors_own():
    """A compiler-owned token is not a variable the producer may bind.

    On pairs 0000 and 0006 the only entry under `variables` was
    `R45RouteToken`, a name the converter invented for its own routing.  The
    effect facade drops it from every answer and the prompts forbid using it as
    a stand-in, so listing it as an ordinary declared variable told the producer
    a variable was available where the model has none -- and pair 0006's
    expected defect is precisely that absence.
    """

    from paper_stm_feedback_loop.discover.nodes import _model_vocabulary

    inspected = {
        "variables": [{"name": "R45RouteToken"}, {"name": "battery"}],
        "states": [{"path": "Root"}],
        "events": [{"qualified_name": "Root.go"}],
    }
    vocabulary = _model_vocabulary(
        inspected, ["compiler:route_control:R45RouteToken", "compiler:root:Root"]
    )
    assert vocabulary["variables"] == ("battery",)
    assert vocabulary["compiler_owned_variables_not_usable_as_evidence"] == (
        "R45RouteToken",
    )


def test_a_model_whose_only_variable_is_compiler_owned_reports_none():
    """The honest answer for pair 0006's shape is an empty list, not one entry."""

    from paper_stm_feedback_loop.discover.nodes import _model_vocabulary

    vocabulary = _model_vocabulary(
        {"variables": [{"name": "R45RouteToken"}]},
        ["compiler:route_control:R45RouteToken"],
    )
    assert vocabulary["variables"] == ()


def test_route_control_names_stay_in_the_fabricated_path_gate():
    """They are declared, so the gate that catches invented paths must not fire.

    Splitting the vocabulary is about what a producer *may use*; the reference
    gate is about what *exists*.  Conflating the two would make the gate report
    a declared element as non-existent.
    """

    from paper_stm_feedback_loop.discover.nodes import _fallback_prepare
    from paper_stm_feedback_loop.discover.schemas import DiscoverInput

    frozen = _fallback_prepare(
        DiscoverInput(
            run_id="route-control-gate",
            natural_language="Idle shall become Busy on go.",
            stm_text=MODEL_WITH_VARS,
            language="en-US",
            source_trace={"attribution_exclusions": ["compiler:route_control:c"]},
        )
    )
    assert "c" in frozen.known_model_paths
    assert "c" not in frozen.model_vocabulary["variables"]


# --------------------------------------------------------------------------
# The two escapes the second review found
# --------------------------------------------------------------------------


def test_an_aliased_predicate_cannot_hide_a_fold():
    """Binding a predicate to a local name is the same fold, renamed.

    Counting only `ast.Call` nodes whose func is a registered name missed
    `f = occupancy_after` / `any([<undeclared>, f(...)])`: the count came back
    1, the fold sealed, and a requirement the model satisfies became a confirmed
    issue.  The counter now looks at any load of a registered name.
    """

    script = (
        "f = occupancy_after\n"
        'assert any([variable_delta_after(source="Root.Idle", trigger="Root.go", '
        'variable="<undeclared>", sign="negative"), '
        'f(source="Root.Idle", trigger="Root.go", target="Root.Busy")]) is True, '
        '"[REQ-001][AST-REQ-001-1] the obligation must hold"'
    )
    result = _checker(MODEL_NO_VARS).check(
        script, reason="alias", required_function_families=()
    )
    assert result.sealed.outcome == "invalid", result.sealed.metadata
    assert "its own assertion" in _message(result), _message(result)


def test_a_lone_undeclared_call_still_seals_with_a_prefix_present():
    """Control: a prefix that touches nothing must not block a legitimate seal."""

    script = (
        "limit = 3\n"
        'assert variable_delta_after(source="Root.Idle", trigger="Root.go", '
        'variable="<undeclared>", sign="negative") is True, '
        '"[REQ-001][AST-REQ-001-1] the obligation must hold"'
    )
    result = _checker(MODEL_NO_VARS).check(
        script, reason="prefix", required_function_families=()
    )
    assert result.sealed.outcome == "sealed_false", result.sealed.metadata


def test_a_provable_absence_still_requires_a_primary_assertion():
    """Supporting-only was pair 0006's original loss, and it was still reachable.

    Only false *primary* assertions become issues, so a requirement whose
    `<undeclared>` claim is carried by supporting evidence alone can never be
    reported violated -- it lands as an unchecked gap, which is exactly the
    outcome the seal was built to prevent.  The waiver now applies only to
    bindings with no declaration table, where no legal primary exists.
    """

    from paper_stm_feedback_loop.discover.nodes import _undeclared_bindings_with_a_table

    # `variable` is decidable from the declarations, so a primary is required.
    assert _undeclared_bindings_with_a_table(
        {"source": "Root.Idle", "variable": "<undeclared>"}
    ) == ("variable",)
    # `release` is an expression with no table, so no legal primary exists.
    assert _undeclared_bindings_with_a_table(
        {"state": "Root.Idle", "release": "<undeclared>"}
    ) == ()
    # A requirement with no `<undeclared>` at all is unaffected.
    assert _undeclared_bindings_with_a_table({"state": "Root.Idle"}) == ()
    assert _undeclared_bindings_with_a_table(None) == ()


# --------------------------------------------------------------------------
# The expression field holds an expression
# --------------------------------------------------------------------------


def test_an_assert_statement_in_the_expression_field_is_rejected_at_schema_time():
    """Both Claude cells of matrix v7 died on this, five assertions at a time.

    The controller wraps the value as `assert (<expression>), <failure_message>`.
    A producer that writes the statement form gets
    `assert (assert ... , "..."), "..."` -- a syntax error on every assertion,
    every item quarantined, then `soft isolation cannot publish an empty
    AssertionScript`.  Rejecting it in the schema makes it the provider's own
    validation error, naming the field, repaired in one round.
    """

    import pytest as _pytest
    from paper_stm_feedback_loop.discover.schemas import AssertionSpec

    good = dict(
        assertion_id="AST-REQ-001-1",
        requirement_id="REQ-001",
        description="d",
        expression='state_declared(state="Root.Idle", kind="leaf") is True',
        failure_message="[REQ-001][AST-REQ-001-1] not a leaf",
        evidence_family="structure",
        role="primary",
        coverage_key="k",
        aggregation_group="g",
    )
    AssertionSpec(**good)  # the bare expression is accepted

    for bad in (
        'assert state_declared(state="Root.Idle", kind="leaf") is True, "[REQ-001] x"',
        'assert(state_declared(state="Root.Idle", kind="leaf"))',
        '   assert state_declared(state="Root.Idle", kind="any")',
    ):
        with _pytest.raises(ValueError, match="bare boolean expression"):
            AssertionSpec(**{**good, "expression": bad})


def test_a_word_starting_with_assert_is_not_mistaken_for_a_statement():
    """`assertion_count(...)` is not an assert statement; only the keyword is."""

    from paper_stm_feedback_loop.discover.schemas import AssertionSpec

    spec = AssertionSpec(
        assertion_id="AST-REQ-001-1",
        requirement_id="REQ-001",
        description="d",
        expression='len([state_declared(state="Root.Idle", kind="leaf")]) == 1',
        failure_message="[REQ-001][AST-REQ-001-1] x",
        evidence_family="structure",
        role="primary",
        coverage_key="k",
        aggregation_group="g",
    )
    assert spec.expression.startswith("len(")


# --------------------------------------------------------------------------
# Only a table that can be empty makes an absence provable
# --------------------------------------------------------------------------


def test_a_state_shaped_undeclared_refusal_names_the_exit():
    """Pair 0050 deadlocked here, twelve revisions and a dead cell.

    Its splitter bound `occupancy_after(source="<undeclared>")` and
    `terminates(scope="<undeclared>")`.  Every model declares states, so the
    predicate refused every primary; the controller demanded one anyway because
    `states` was in the binding-table map; and the reviewer rejected each attempt
    to substitute concrete states as changing the obligation.  No stage had a
    legal move.
    """

    result = _checker(MODEL_NO_VARS).check(
        _script('occupancy_after(source="<undeclared>", trigger="Root.go", target="Root.Busy")'),
        reason="state-shaped",
        required_function_families=(),
    )
    assert result.sealed.outcome == "invalid", result.sealed.metadata
    message = _message(result)
    assert "every model declares states" in message, message
    assert "no executable primary" in message, message
    assert "coverage gap" in message, message


def test_the_waiver_keys_on_provable_emptiness_not_on_having_a_table():
    """`states` has a table and still cannot be discharged; the two differ."""

    from paper_stm_feedback_loop.discover.nodes import _undeclared_bindings_with_a_table

    # Provably empty -> a primary is possible and therefore required.
    assert _undeclared_bindings_with_a_table({"variable": "<undeclared>"}) == ("variable",)
    assert _undeclared_bindings_with_a_table({"trigger": "<undeclared>"}) == ("trigger",)
    # Never empty, or no table -> no primary exists, so none is demanded.
    for binding in ("source", "target", "state", "scope", "parent", "child",
                    "composite", "response", "condition", "release"):
        assert _undeclared_bindings_with_a_table({binding: "<undeclared>"}) == (), binding


def test_a_variable_binding_is_still_expected_to_carry_a_primary():
    """The 0006 recall win must not be given back by the 0050 fix.

    `variable="<undeclared>"` on a model with no author variables is the whole
    reason the seal exists; waiving its primary would refile that finding as an
    unchecked gap.
    """

    result = _checker(MODEL_NO_VARS).check(
        _script(VARIABLE_CALLS[0]), reason="still seals", required_function_families=()
    )
    assert result.sealed.outcome == "sealed_false"
