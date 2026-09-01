"""Four ways a predicate reported a defect the model did not have.

Each was found by auditing the 19 predicates against the real corpus before a
run, and each is the same failure class: a question the layer could not answer
came back as `False` instead of a refusal, and `False` from a primary assertion
is published as a confirmed issue.  So these are not robustness tests -- an
unfixed one puts a fabricated defect in the paper.

Every case is pinned in both directions: the shape that used to be wrong, and
the neighbouring shape that must keep working, because three of the four fixes
are one branch away from breaking the path that already worked.
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
from paper_stm_feedback_loop.assertions.exceptions import (  # noqa: E402
    UnsupportedEvidence,
)

#: A mode with an inner leaf, so a claim can be stated about either level, plus a
#: second leaf so `[*]` has somewhere to settle that is not the target.
MODEL = """\
state Root {
    state Mode {
        state Inner { }
        state Done { }
        [*] -> Inner;
        Inner -> Done : /go;
        Inner -> Inner : /tick;
    }
    state Other { }
    [*] -> Mode;
    Mode -> Other : /leave;
}
"""

_ENV = {}


def env():
    if "env" not in _ENV:
        _ENV["env"] = build_eval_environment(
            model_text=MODEL,
            source_mappings=[],
            source_exclusions=[],
            timeout_seconds=60,
            fbmcq_solver_timeout_ms=20_000,
            fbmcq_max_bound=5,
            fbmcq_process_wall_seconds=30.0,
        )
    return _ENV["env"]


def call(name, **kwargs):
    return env().globals[name](**kwargs)


# --------------------------------------------------------------------------
# A composite source: the trigger was burned on the entry cycle


def test_a_mode_level_claim_is_answered_about_the_mode():
    """Committing the entry into a composite's initial child *is* a cycle.

    The hot-start plan offered the trigger in cycle 0, which is the cycle that
    commits the entry, so it was never consumed and every B-family question about
    a mode came back False.  Measured on pair 0000: pinned at `AutonomousMode`,
    `[[Condition_Met]]` consumes nothing while `[[], [Condition_Met]]` consumes it
    and reaches `AutoFinal`.  704 bindings across 58 of the 60 pairs name a
    composite source, so this reported an ignored event on models that handle it.
    """

    assert call(
        "occupancy_after", source="Root.Mode", trigger="Root.go", target="Root.Mode.Done"
    ) is True
    assert call("event_consumed", source="Root.Mode", trigger="Root.go") is True
    # The leaf-level claim is the one that already worked; the settle cycle must
    # not change it.
    assert call(
        "occupancy_after",
        source="Root.Mode.Inner",
        trigger="Root.go",
        target="Root.Mode.Done",
    ) is True
    assert call("event_consumed", source="Root.Mode.Inner", trigger="Root.go") is True
    # And discrimination survives: a wrong target is still False, from either
    # level, or the fix would have bought True by answering nothing.
    assert call(
        "occupancy_after", source="Root.Mode", trigger="Root.go", target="Root.Other"
    ) is False


# --------------------------------------------------------------------------
# `[*]` outside the two bindings where it means anything


@pytest.mark.parametrize(
    "name,kwargs",
    [
        ("edge_declared", dict(source="Root.Mode.Inner", trigger="[*]", target="Root.Mode.Done")),
        ("effect_declared", dict(source="Root.Mode.Inner", trigger="[*]", variable="counter", sign="negative")),
        ("effect_declared", dict(source="Root.Mode.Inner", trigger="Root.go", variable="[*]", sign="negative")),
        ("occupancy_after", dict(source="Root.Mode.Inner", trigger="Root.go", target="[*]")),
        ("reaches", dict(source="Root.Mode.Inner", target="[*]")),
        ("state_declared", dict(state="[*]", kind="leaf")),
        ("variable_declared", dict(variable="[*]")),
        ("event_declared", dict(event="[*]")),
        ("containment", dict(parent="[*]", child="Root.Mode")),
    ],
)
def test_the_pseudo_initial_is_refused_outside_a_starting_configuration(name, kwargs):
    """It marks where a run begins, so only `source` and `scope` can carry it.

    This was a per-predicate allowlist, and the list was the bug: `trigger`,
    `variable` and `target` were absent from every entry, so each of these
    answered a model-independent False -- "the model declares no edge on `[*]`"
    -- on all 60 pairs.  One rule over bindings cannot be missed a slot at a time.
    """

    with pytest.raises(UnsupportedEvidence, match="pseudo-initial"):
        call(name, **kwargs)


def test_the_pseudo_initial_still_works_where_a_run_can_begin():
    """The rule has to leave the cold-start idiom alone.

    `[*]` in `source` is how a power-on claim is stated, and the vocabulary
    documents it; refusing it there would break the initialization requirements
    this predicate set was extended to cover.
    """

    assert call(
        "edge_declared", source="[*]", trigger="Root.go", target="Root.Mode"
    ) in (True, False)
    assert call(
        "occupancy_after", source="[*]", trigger="Root.go", target="Root.Mode.Done"
    ) in (True, False)
    assert call("cardinality", scope="Root", count=2) in (True, False)


def test_a_static_guard_query_refuses_the_pseudo_initial_bucket():
    """The facade reports every composite's local entry under the same `[*]`.

    So the literal is not a source there but a bucket: on pair 0002 it merged the
    entry edges of two concurrent regions, and `conflicting_targets` -- which has
    no notion of scope -- reported non-determinism between transitions in
    disjoint scopes.  `source` is legal for the simulating predicates and not for
    this one, which is why the per-predicate list still exists.
    """

    with pytest.raises(UnsupportedEvidence, match="pseudo-initial"):
        call("guard_distinguishable", source="[*]", trigger="Root.go")


# --------------------------------------------------------------------------
# `stays_in` from the initial configuration


def test_staying_in_the_initial_configuration_is_refused_when_none_was_entered():
    """Two wrong answers in a row, so this one is pinned as a refusal.

    First it compared real state paths against the literal `"[*]"`, which nothing
    can equal, so a power-on self-loop claim reported a missing self-loop on every
    model.  Comparing against the pre-trigger ancestry instead is worse in the
    other direction: a configuration that committed nothing has only the root in
    its ancestry, the root is active in every run, and the answer becomes True
    whatever the trigger does.  Neither is evidence, so refuse.
    """

    # Pair 0000 is the witness: its initial entry is event-triggered
    # (`[*] -> HumanDrivingMode : /Power_On`), so nothing is occupied until that
    # event fires.  This model's entries are unconditional, so it settles into a
    # state and the question is answerable there -- which is the contrast worth
    # keeping in one test.
    corpus = (
        ROOT.parent
        / "representation/reports/llms_emp_r45_java_60/pairs/0000/fcstm.fcstm"
    )
    pair = build_eval_environment(
        model_text=corpus.read_text(),
        source_mappings=[],
        source_exclusions=[],
        timeout_seconds=60,
        fbmcq_solver_timeout_ms=20_000,
        fbmcq_max_bound=5,
        fbmcq_process_wall_seconds=30.0,
    )
    prefix = "llms_emp_feedback_final_0000"
    with pytest.raises(UnsupportedEvidence, match="enters no state before"):
        pair.globals["stays_in"](source="[*]", trigger=f"{prefix}.Power_On")
    # Where the cold start *does* commit a configuration, the question is answerable
    # and gets a real verdict rather than a refusal.  This model's entries are
    # unconditional, so `[*]` settles into `Mode.Inner` before the trigger.
    assert call("stays_in", source="[*]", trigger="Root.tick") is True
    assert call("stays_in", source="[*]", trigger="Root.go") is False
    # The named-source form is the one that decides the defect, and it still does.
    assert call("stays_in", source="Root.Mode.Inner", trigger="Root.tick") is True
    assert call("stays_in", source="Root.Mode.Inner", trigger="Root.go") is False


# --------------------------------------------------------------------------
# `response_within` with `source` omitted


def test_an_omitted_source_is_resolved_from_the_trigger_or_refused():
    """It used to be "the first leaf in inspect order", which ignored the trigger.

    So the same obligation answered True on a model whose first declared leaf
    happened to be the trigger's source and False on one that declares an
    unrelated state first -- declaration order deciding a verdict.  Resolving it
    from the trigger is the documented intent; an ambiguous trigger is refused
    rather than resolved by picking one, because only the caller knows which
    source the requirement means.
    """

    predicates = env().predicates
    # `go` leaves exactly one state here, so the default is unambiguous.
    assert predicates._default_init("Root.go") == "Root.Mode.Inner"
    # An event no transition carries names no source: the obligation runs
    # unpinned rather than against an invented one.
    assert predicates._default_init("Root.nosuchevent") is None
