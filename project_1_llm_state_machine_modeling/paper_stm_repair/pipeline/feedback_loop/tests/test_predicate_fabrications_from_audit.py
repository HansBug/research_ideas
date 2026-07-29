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


def refused(model: str, expression: str) -> bool:
    """Whether the predicate declined to answer.

    `eval_assert` converts `UnsupportedEvidence` into `result="unsupported"` with a
    `None` value rather than propagating it, so a test that catches the exception
    would never see a refusal.
    """

    return env(model).eval_assert(expression, "audit regression").result == "unsupported"


def test_the_one_step_fact_the_order_pair_shares_is_visible_to_both_models():
    """Premise: the edge is declared and taken in both, so order is the only变量."""

    edge = 'edge_declared(source="Root.A", trigger="Root.other", target="Root.C") is True'
    occupancy = (
        'occupancy_after(source="Root.A", trigger="Root.other", target="Root.C") is True'
    )
    for model in (_TARGET_FIRST, _COMPETITOR_FIRST):
        assert ask(model, edge) is True
        assert ask(model, occupancy) is True


@pytest.mark.parametrize("cycles", [1, 3, 20])
def test_reaches_must_not_depend_on_transition_declaration_order(cycles):
    """Fixed by offering each declared event on its own instead of all at once."""

    expression = (
        f'reaches(source="Root.A", target="Root.C", within_cycles={cycles}) is True'
    )
    assert ask(_TARGET_FIRST, expression) == ask(_COMPETITOR_FIRST, expression)


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


#: `go` is routed to `Other`, so the obligation genuinely fails here.  Kept beside
#: the two satisfying models so a fix cannot pass by weakening the check.
_MISROUTED = _RESPONSE.format(tail="        Busy -> Idle : /ack;").replace(
    "    Idle -> Busy : /go;", "    state Other named \"Other\";\n    Idle -> Other : /go;"
)


@pytest.mark.parametrize("bound", [2, 4, 8])
def test_response_within_must_not_require_the_response_state_to_be_a_sink(bound):
    """Leaving the response state later is not a violation of the obligation.

    Fixed by carrying the pinned configuration into the trigger condition, which is
    what `source` was documented to mean: `trigger (event(E, current) &&
    active(<source>))`.  Without it `init state(...)` bound step 0 while the
    obligation quantified over every step, so the solver answered a different
    question -- "the trigger must be answered from every reachable configuration",
    which nothing satisfies unless the response is a sink.
    """

    expression = (
        f'response_within(trigger="Root.go", response="Root.Busy", bound={bound}, '
        f'source="Root.Idle") is True'
    )
    assert ask(_SINK, expression) is True
    assert ask(_LEAVABLE, expression) is True
    # The other half: a model that really does route the trigger elsewhere still
    # fails, so the scoping did not simply make the predicate permissive.
    assert ask(_MISROUTED, expression) is False


def test_stays_in_discriminates_when_the_named_state_is_the_one_occupied():
    """Premise: at leaf level the predicate already answers correctly."""

    expression = 'stays_in(source="Root.Mode.Inner", trigger="Root.go") is True'
    assert ask(_SELF_LOOP, expression) is True
    assert ask(_MOVES, expression) is False


@pytest.mark.parametrize("ancestor", ["Root", "Root.Mode"])
def test_stays_in_must_not_answer_true_for_an_undiscriminating_ancestor(ancestor):
    """Either refuse the binding or answer about the state actually occupied.

    Both would remove the fabrication, so this asserts only that the violating
    model does not come back True.  The fix chose refusal, because "stays inside
    this composite" and "stays in this exact state" are different claims and a
    composite binding does not say which the sentence meant -- and it refuses on
    both models, not just the failing one, so the check has to be symmetric.
    """

    expression = f'stays_in(source="{ancestor}", trigger="Root.go") is True'
    for model in (_MOVES, _SELF_LOOP):
        assert refused(model, expression) or ask(model, expression) is False, ancestor


#: Nothing reaches `Unreachable`, and it takes two *different* events to get near
#: it -- the shape the one-event-at-a-time enumeration cannot settle.
_SEQUENCE = """\
state Root named "Root" {
    event first named "first";
    event second named "second";
    state A named "A";
    state B named "B";
    state C named "C";
    state Unreachable named "Unreachable";
    [*] -> A;
    A -> B : /first;
    B -> C : /second;
}
"""


def test_the_search_finds_a_multi_event_witness_and_still_reports_unreachable():
    """Completeness for the bound is what makes a False sound.

    A target needing `first` then `second` has to be found -- that is the use these
    predicates exist for, and offering one event per run would miss it.  A target
    nothing can reach has to come back False rather than being refused, or the
    predicate could never expose the defect it advertises.  The breadth-first
    sequence search delivers both: it prunes by landing configuration, so it stays
    polynomial while remaining exhaustive over the bound.
    """

    # Two different events in sequence.
    assert ask(_SEQUENCE, 'reaches(source="Root.A", target="Root.C", within_cycles=4) is True') is True
    # Declared but with no incoming edge at all: the reachable set closes without it.
    assert (
        ask(_SEQUENCE, 'reaches(source="Root.A", target="Root.Unreachable", within_cycles=4) is True')
        is False
    )
    # One event away, unchanged.
    assert ask(_SEQUENCE, 'reaches(source="Root.A", target="Root.B", within_cycles=4) is True') is True


def test_the_budget_is_part_of_the_claim_so_a_smaller_one_can_fail():
    """And the horizon still bounds it, rather than the search running away."""

    # `C` is two events away, so one cycle cannot witness it.
    assert ask(_SEQUENCE, 'reaches(source="Root.A", target="Root.C", within_cycles=1) is True') is False
    assert ask(_SEQUENCE, 'reaches(source="Root.A", target="Root.C", within_cycles=2) is True') is True


def test_a_single_candidate_still_answers_false_because_that_search_is_complete():
    """With the event named, the enumeration is exhaustive and a False is sound.

    This is the shape every `terminates` call in matrix-v16 used -- eight of them,
    all naming their trigger -- which is why the order defect never reached the
    published results.
    """

    # `first` cannot end the run in this model, and that is a complete answer.
    assert ask(_SEQUENCE, 'terminates(scope="Root.A", trigger="Root.first") is True') is False
    ending = _SEQUENCE.replace("    B -> C : /second;", "    B -> [*] : /second;")
    assert ask(ending, 'terminates(scope="Root.B", trigger="Root.second") is True') is True


def test_the_search_refuses_rather_than_answering_past_its_budget(monkeypatch):
    """A False that only means "I stopped looking" is the defect being fixed.

    Forced with a tiny ceiling rather than a huge model: what matters is which of
    the two answers the exhausted branch gives, and that is independent of the
    number that exhausts it.
    """

    from paper_stm_feedback_loop.assertions.predicate_api import PredicateAPI

    monkeypatch.setattr(PredicateAPI, "_SEARCH_BUDGET", 2)
    assert refused(
        _SEQUENCE, 'reaches(source="Root.A", target="Root.C", within_cycles=4) is True'
    )


def test_the_search_refuses_when_it_cannot_read_the_values_that_distinguish_runs(
    monkeypatch,
):
    """Pruning on states alone is not conservative, so it must not fall back to it.

    Two runs can share a configuration and differ in a variable a guard reads.
    Treating them as one can discard the only sequence that reaches the target, and
    the False that follows looks exactly like an honest one.
    """

    from paper_stm_feedback_loop.assertions import views

    original = views.FrozenView.keys

    def unreadable(self):
        # Only the variables view; `keys` is on the dict protocol `dict()` uses, and
        # breaking every view would prove nothing about this branch.
        if self.view_kind.endswith(".field"):
            raise RuntimeError("variables unreadable")
        return original(self)

    monkeypatch.setattr(views.FrozenView, "keys", unreadable, raising=False)
    assert refused(
        _SEQUENCE, 'reaches(source="Root.A", target="Root.C", within_cycles=4) is True'
    )
