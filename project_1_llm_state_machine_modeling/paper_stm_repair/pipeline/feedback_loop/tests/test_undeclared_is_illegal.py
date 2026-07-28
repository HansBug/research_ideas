"""`<undeclared>` may not reach an assertion (issue #170 §11.2).

Three designs preceded this one, and the file keeps the history because each
failed in a way the next had to avoid.

1. **Refusal.** The predicate raised, precheck called that non-executable, the
   item burned its repair budget and the requirement was filed as a coverage gap.
   Pair 0006's expected defect -- the NL requires the swarm count to drop and the
   model declares no variable that could -- was reported as *unchecked*.

2. **Unconditional seal.** The predicate returned False for any `<undeclared>`
   binding, on the strength of a string comparison that read no declaration. That
   manufactures a defect against a model that may not have one, and it pays better
   than an honest guess: a wrong variable name costs a repair round, a shrug earns
   a finding.

3. **Seal gated on an empty declaration table.** Sound in principle. Measured on
   this corpus it constrains nothing: **60 of 60 pairs have an empty author-owned
   variable table** (the only variable any model declares is the converter's route
   token). So the gate never fired and any pair at all could produce a false
   positive -- demonstrated on pair 0000, whose NL mentions no quantity anywhere.

The current design does not judge the literal at all. The converter proposes a
name, asserts its existence as a `precondition`, and makes the real claim depend
on it, so the missing element becomes something repair can target and verify.
`<undeclared>` survives only at the requirement layer, as a statement about the
NL-versus-model difference.
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


def _checker(model=MODEL_NO_VARS, exclusions=None):
    return AssertionChecker(
        environment=build_eval_environment(
            model_text=model,
            source_mappings=[],
            source_exclusions=exclusions or [],
            timeout_seconds=30,
            fbmcq_solver_timeout_ms=15_000,
            fbmcq_max_bound=4,
            fbmcq_process_wall_seconds=20.0,
        )
    )


def _script(call):
    return f'assert {call} is True, "[REQ-001][AST-REQ-001-1] the obligation must hold"'


def _message(result):
    return str((result.sealed.error or {}).get("message", ""))


ILLEGAL = [
    'variable_delta_after(source="Root.Idle", trigger="Root.go", variable="<undeclared>", sign="negative")',
    'effect_declared(source="Root.Idle", trigger="Root.go", variable="<undeclared>", sign="negative")',
    'state_declared(state="<undeclared>", kind="leaf")',
    'occupancy_after(source="<undeclared>", trigger="Root.go", target="Root.Busy")',
    'edge_declared(source="Root.Idle", trigger="<undeclared>", target="Root.Busy")',
    'persists_until(state="Root.Idle", release="<undeclared>", bound=2)',
    'variable_declared(name="<undeclared>")',
]


@pytest.mark.parametrize("call", ILLEGAL)
def test_no_predicate_evaluates_the_literal(call):
    """Whatever the binding kind, the answer is a refusal naming the fix.

    Design 3 answered differently per binding kind -- seal for `variable` and
    `trigger`, refuse for state-shaped ones, refuse for expressions -- which took
    three sets of judgement, three exemptions, a dedicated exception type and a
    dedicated seal path to express.  One rule replaces all of it.
    """

    result = _checker().check(_script(call), reason="illegal", required_function_families=())
    assert result.sealed.outcome == "invalid", result.sealed.metadata
    assert "is a placeholder, not a name" in _message(result), _message(result)
    assert "precondition" in _message(result), "the refusal must name the fix"


@pytest.mark.parametrize("model", [MODEL_NO_VARS, MODEL_WITH_VARS])
def test_the_declaration_table_no_longer_decides_anything(model):
    """Design 3's judgement is gone, so an empty table is not a verdict.

    This is the property that mattered: with 60/60 pairs having an empty
    author-owned variable table, "table is empty" carried no information, and a
    seal resting on it was a false-positive channel open on every pair.
    """

    result = _checker(model).check(
        _script(ILLEGAL[0]), reason="illegal", required_function_families=()
    )
    assert result.sealed.outcome == "invalid"
    assert result.sealed.metadata.get("verdict_basis") is None


def test_a_route_control_only_model_is_treated_no_differently():
    """Pair 0006's exact shape used to seal here; now it refuses like the rest."""

    result = _checker(MODEL_WITH_VARS, ["compiler:route_control:c"]).check(
        _script(ILLEGAL[0]), reason="illegal", required_function_families=()
    )
    assert result.sealed.outcome == "invalid"


def test_the_replacement_shape_works_on_that_same_model():
    """What pair 0006 should now produce: existence False, delta depending on it.

    The precondition answers `False` off a real query -- `variable_declared`
    consults the table and finds no author-owned variable -- so the finding rests
    on evidence rather than on a literal, and it names `uav_count` for repair to
    add.
    """

    exists = _checker(MODEL_WITH_VARS, ["compiler:route_control:c"]).check(
        _script('variable_declared(name="uav_count")'),
        reason="existence",
        required_function_families=(),
    )
    assert exists.sealed.outcome == "sealed_false"
    assert exists.sealed.value is False


def test_an_ordinary_refusal_is_still_distinguishable():
    """A query that genuinely cannot decide must not be confused with the above."""

    result = _checker().check(
        _script('guard_distinguishable(source="Root.Busy", trigger="Root.go")'),
        reason="refusal",
        required_function_families=(),
    )
    assert result.sealed.outcome == "invalid"
    assert "is a placeholder" not in _message(result)


def test_the_removed_machinery_is_gone():
    """Design 3 needed six special cases; a re-added one would be a regression.

    Listed explicitly because each was load-bearing for a judgement that no
    longer exists, and leaving one behind means two rules for the same literal.
    """

    import paper_stm_feedback_loop.assertions.exceptions as exceptions
    import paper_stm_feedback_loop.assertions.predicate_api as predicate_api
    import paper_stm_feedback_loop.discover.nodes as nodes

    assert not hasattr(exceptions, "UndeclaredTerm")
    assert not hasattr(predicate_api, "PROVABLY_EMPTY_TABLES")
    assert not hasattr(nodes, "_undeclared_bindings_with_a_table")
    for source, marker in (
        (Path(predicate_api.__file__).read_text(), "declaration_table:"),
        (Path(nodes.__file__).read_text(), "sealed_on_absence"),
        (Path(nodes.__file__).read_text(), "unassertable"),
    ):
        assert marker not in source, marker


def test_route_control_variables_are_listed_apart_from_the_authors_own():
    """Unchanged from before and still needed: the vocabulary must not offer one.

    On pairs 0000 and 0006 the only entry under `variables` was the converter's
    route token.  Listing it as an ordinary declared variable told the producer a
    variable was available where the model has none.
    """

    from paper_stm_feedback_loop.discover.nodes import _model_vocabulary

    vocabulary = _model_vocabulary(
        {
            "variables": [{"name": "R45RouteToken"}, {"name": "battery"}],
            "states": [{"path": "Root"}],
            "events": [{"qualified_name": "Root.go"}],
        },
        ["compiler:route_control:R45RouteToken"],
    )
    assert vocabulary["variables"] == ("battery",)
    assert vocabulary["compiler_owned_variables_not_usable_as_evidence"] == (
        "R45RouteToken",
    )
