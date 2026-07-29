"""Three predicates report defects the model does not have.

Found by auditing the 19 predicates against the corpus before matrix-v17, each
reproduced on a decisive pair of models -- one that satisfies the obligation and
one that violates it -- so a fix cannot be checked by making the failing arm pass
alone.  All three publish `False` from a primary assertion, which the adjudicator
turns into a confirmed issue, so each one puts a fabricated defect in the paper.

`reaches` / `terminates` (C1)
    Both offer the entire declared alphabet in every cycle, and the simulator
    commits one successor per cycle.  So the run follows whichever competing event
    the transition table happens to list first, and the verdict is a function of
    declaration order rather than of the model.  Corpus-wide, 124 of 412 declared
    one-step event edges have `occupancy_after` True and `reaches` False on the
    same binding.

`response_within` (C2)
    The contract says `source` pins the configuration the obligation is about.
    `init state(...)` fixes only step 0, while `check response <= k` still
    quantifies over every step, so the solver may inject the trigger in a
    configuration that cannot answer it and book that as the violation.  The
    predicate is then True only when the response state is a sink.

`stays_in` (C3)
    It compares with `state == name or state.startswith(name + ".")`, so any
    ancestor of the real configuration matches its whole subtree.  Its four
    sibling predicates all refuse the model root through
    `_reject_undiscriminating_root`; this one has no such guard, which is the same
    near-tautology already fixed for its `[*]` branch, reachable again by naming
    an ancestor.
"""

from __future__ import annotations

import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.assertions import build_eval_environment  # noqa: E402
from paper_stm_feedback_loop.assertions.exceptions import (  # noqa: E402
    UnsupportedEvidence,
)

#: `A` has two outgoing events.  Only the order of the two lines differs between
#: the pair, and no edge is eventless, so this is not the completion-edge defect.
_ORDER = """\
state Root named "Root" {{
    event go named "go";
    event other named "other";
    state A named "A";
    state B named "B";
    state C named "C";
    [*] -> A;
{edges}
}}
"""
_TARGET_FIRST = _ORDER.format(
    edges='        A -> C : /other;\n        A -> B : /go;'
)
_COMPETITOR_FIRST = _ORDER.format(
    edges='        A -> B : /go;\n        A -> C : /other;'
)

#: Identical `Idle -/go-> Busy` edge; the pair differs only in whether `Busy` can
#: be left afterwards, which the obligation says nothing about.
_RESPONSE = """\
state Root named "Root" {{
    event go named "go";
    event ack named "ack";
    state Idle named "Idle";
    state Busy named "Busy";
    [*] -> Idle;
    Idle -> Busy : /go;
{tail}
}}
"""
_SINK = _RESPONSE.format(tail="")
_LEAVABLE = _RESPONSE.format(tail="        Busy -> Idle : /ack;")

#: NL: "`go` must leave the machine in the same state."  One model self-loops and
#: satisfies it; the other moves and violates it.
_STAY = """\
state Root named "Root" {{
    event go named "go";
    state Mode named "Mode" {{
        state Inner named "Inner";
        state Done named "Done";
        [*] -> Inner;
        Inner -> {target} : /go;
    }}
    [*] -> Mode;
}}
"""
_SELF_LOOP = _STAY.format(target="Inner")
_MOVES = _STAY.format(target="Done")

_CACHE: dict[str, object] = {}


def env(model: str):
    if model not in _CACHE:
        _CACHE[model] = build_eval_environment(
            model_text=model,
            source_mappings=[],
            source_exclusions=[],
            timeout_seconds=60,
            fbmcq_solver_timeout_ms=20_000,
            fbmcq_max_bound=8,
            fbmcq_process_wall_seconds=30.0,
        )
    return _CACHE[model]


def ask(model: str, expression: str):
    return env(model).eval_assert(expression, "audit regression").value


def test_the_one_step_fact_the_order_pair_shares_is_visible_to_both_models():
    """Premise: the edge is declared and taken in both, so order is the only变量."""

    edge = 'edge_declared(source="Root.A", trigger="Root.other", target="Root.C") is True'
    occupancy = (
        'occupancy_after(source="Root.A", trigger="Root.other", target="Root.C") is True'
    )
    for model in (_TARGET_FIRST, _COMPETITOR_FIRST):
        assert ask(model, edge) is True
        assert ask(model, occupancy) is True


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Known defect (C1), pinned before the fix. strict=True so the marker cannot "
        "outlive the bug."
    ),
)
@pytest.mark.parametrize("cycles", [1, 3, 20])
def test_reaches_must_not_depend_on_transition_declaration_order(cycles):
    expression = (
        f'reaches(source="Root.A", target="Root.C", within_cycles={cycles}) is True'
    )
    assert ask(_TARGET_FIRST, expression) == ask(_COMPETITOR_FIRST, expression)


@pytest.mark.xfail(strict=True, reason="Known defect (C1), pinned before the fix.")
def test_terminates_must_not_depend_on_transition_declaration_order():
    model = 'state Root named "Root" {{\n    event go named "go";\n    event stop named "stop";\n    state A named "A";\n    state B named "B";\n    [*] -> A;\n{edges}\n}}\n'
    stop_first = model.format(
        edges='    A -> [*] : /stop;\n    A -> B : /go;'
    )
    go_first = model.format(edges='    A -> B : /go;\n    A -> [*] : /stop;')
    expression = 'terminates(scope="[*]") is True'
    assert ask(stop_first, expression) == ask(go_first, expression)


def test_the_response_pair_shares_the_edge_the_obligation_is_about():
    """Premise: both models answer `go` with `Busy` in one step."""

    for model in (_SINK, _LEAVABLE):
        assert ask(
            model,
            'occupancy_after(source="Root.Idle", trigger="Root.go", target="Root.Busy") is True',
        ) is True


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Known defect (C2), pinned before the fix. Being able to leave the response "
        "state afterwards is not a violation of 'go is answered by Busy'."
    ),
)
@pytest.mark.parametrize("bound", [2, 4, 8])
def test_response_within_must_not_require_the_response_state_to_be_a_sink(bound):
    expression = (
        f'response_within(trigger="Root.go", response="Root.Busy", bound={bound}, '
        f'source="Root.Idle") is True'
    )
    assert ask(_SINK, expression) is True
    assert ask(_LEAVABLE, expression) is True


def test_stays_in_discriminates_when_the_named_state_is_the_one_occupied():
    """Premise: at leaf level the predicate already answers correctly."""

    expression = 'stays_in(source="Root.Mode.Inner", trigger="Root.go") is True'
    assert ask(_SELF_LOOP, expression) is True
    assert ask(_MOVES, expression) is False


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Known defect (C3), pinned before the fix. An ancestor subject matches its "
        "whole subtree, so the violating model answers True."
    ),
)
@pytest.mark.parametrize("ancestor", ["Root", "Root.Mode"])
def test_stays_in_must_not_answer_true_for_an_undiscriminating_ancestor(ancestor):
    """Either refuse the binding or answer about the state actually occupied.

    Both are acceptable fixes, so this asserts only that the violating model does
    not come back True -- which is what makes the finding fabricated.
    """

    expression = f'stays_in(source="{ancestor}", trigger="Root.go") is True'
    try:
        answer = ask(_MOVES, expression)
    except UnsupportedEvidence:
        return
    assert answer is False, (ancestor, answer)
