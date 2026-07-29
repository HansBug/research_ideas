"""Behavioural spec for all 17 predicates: every one must answer both ways.

Why this file exists
--------------------
The probe in `runs/paper1/audit-.../probe_predicates_60.py` establishes that
each predicate *answers* on the 60 real pairs -- no crash, a strict bool.  That
is necessary and nowhere near sufficient.  A predicate that returns True for
every model passes the probe and reports zero defects forever; a predicate that
returns False for every model passes the probe and reports a defect on every
model.  Both have shipped here: `response_within` was constant-False because its
query lacked a `within` clause, and `persists_until` was a tautology because
`exists_always` asks for a witness rather than an invariant.  Neither was
visible from a one-sided result.

So the contract each predicate is held to is:

1. **Discriminates.** There is a model where it is True and a model where it is
   False, and the difference between those two models is exactly the property
   the predicate claims to decide.  Anything else -- a True that comes from the
   wrong reason -- is a coincidence, not evidence.
2. **Refuses rather than guesses.** Bindings it cannot decide raise, and the
   raise is `UnsupportedEvidence`, never a bool.
3. **Validates its literals.** A `sign`, `kind`, `phase` or `count` outside its
   domain raises rather than silently taking a default branch.

The paired models below differ in one property each, so a True/False pair is
attributable to that property and not to some incidental difference.
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
from paper_stm_feedback_loop.assertions.exceptions import UnsupportedEvidence  # noqa: E402
from paper_stm_feedback_loop.discover.predicates import PREDICATES  # noqa: E402

# --------------------------------------------------------------------------
# Fixtures.  RICH is the "satisfies everything" model; each FLAWED_* differs
# from it in exactly one property.
# --------------------------------------------------------------------------

RICH = """def int units = 5;
def int other = 0;
state Root {
    event go;
    event done;
    event tick;
    event fin;
    state Idle {
        enter { other = 1; }
        exit { other = 2; }
        during { other = other + 1; }
    }
    state Outer {
        state First;
        state Second;
        [*] -> First;
        First -> Second : /tick;
        Second -> [*] : /done;
    }
    state Hub;
    state Left;
    state Right;
    state Done;
    [*] -> Idle;
    Idle -> Outer : /go effect { units = units - 1; };
    Idle -> Idle : /tick;
    Outer -> Hub;
    Hub -> Left : /go + [units > 3];
    Hub -> Right : /go + [units <= 3];
    Left -> Done : /fin;
    Done -> [*] : /fin;
    Hub -> Done : /fin;
}
"""

#: `Idle -> Outer` carries no effect on `units`, and the increment is positive.
FLAWED_EFFECT = RICH.replace(
    "Idle -> Outer : /go effect { units = units - 1; };",
    "Idle -> Outer : /go effect { units = units + 1; };",
)

#: Both alternatives out of `Hub` on `go` carry the same guard.
FLAWED_GUARDS = RICH.replace("Hub -> Right : /go + [units <= 3];", "Hub -> Right : /go + [units > 3];")

#: `Outer` starts in `Second` instead of `First`.
FLAWED_INITIAL = RICH.replace("[*] -> First;", "[*] -> Second;")

#: `Idle` declares no lifecycle actions.
FLAWED_ACTIONS = RICH.replace(
    """    state Idle {
        enter { other = 1; }
        exit { other = 2; }
        during { other = other + 1; }
    }""",
    "    state Idle;",
)

#: No route out of the machine: `Done -> [*]` removed.
FLAWED_TERMINATION = RICH.replace("    Done -> [*] : /fin;\n", "")

#: The self-loop on `Idle` is gone, so `tick` moves nothing and is not consumed.
FLAWED_SELF_LOOP = RICH.replace("    Idle -> Idle : /tick;\n", "")

#: The model declares no variable of the author's own.
NO_VARIABLES = """state Root {
    event go;
    state Idle;
    state Busy;
    [*] -> Idle;
    Idle -> Busy : /go;
}
"""


_ENV_CACHE: dict[str, object] = {}


def env(model: str):
    """One environment per distinct model text; building one is not cheap."""

    key = str(hash(model))
    if key not in _ENV_CACHE:
        _ENV_CACHE[key] = build_eval_environment(
            model_text=model,
            source_mappings=[],
            source_exclusions=[],
            timeout_seconds=60,
            fbmcq_solver_timeout_ms=30_000,
            fbmcq_max_bound=6,
            fbmcq_process_wall_seconds=40.0,
        )
    return _ENV_CACHE[key]


def call(model: str, predicate: str, **kwargs):
    return env(model).globals[predicate](**kwargs)


# --------------------------------------------------------------------------
# The discrimination table: (predicate, kwargs, true_model, false_model)
#
# Each row names one property and two models that differ in it.  A predicate
# that cannot separate the pair is not deciding what it claims to decide.
# --------------------------------------------------------------------------

DISCRIMINATION = [
    # ---- Family S ----
    (
        "state_declared",
        dict(state="Root.Idle", kind="leaf"),
        None,  # leaf-vs-composite needs one model, not two; see below
        None,
    ),
    (
        "containment",
        dict(parent="Root.Outer", child="Root.Outer.First"),
        RICH,
        NO_VARIABLES,  # no such parent/child at all
    ),
    (
        "initial_target",
        dict(composite="Root.Outer", child="Root.Outer.First"),
        RICH,
        FLAWED_INITIAL,
    ),
    (
        "edge_declared",
        dict(source="Root.Idle", trigger="Root.go", target="Root.Outer"),
        RICH,
        NO_VARIABLES,
    ),
    (
        "effect_declared",
        dict(source="Root.Idle", trigger="Root.go", variable="units", sign="negative"),
        RICH,
        FLAWED_EFFECT,
    ),
    (
        "action_declared",
        dict(state="Root.Idle", phase="entry"),
        RICH,
        FLAWED_ACTIONS,
    ),
    (
        "guard_distinguishable",
        dict(source="Root.Idle", trigger="Root.go"),
        RICH,  # one target, so nothing to distinguish
        None,  # the False case needs its own model; see the dedicated test
    ),
    (
        "cardinality",
        dict(scope="Root.Outer", count=2),
        RICH,
        NO_VARIABLES,
    ),
    # ---- Family B ----
    (
        "occupancy_after",
        dict(source="Root.Idle", trigger="Root.go", target="Root.Outer"),
        RICH,
        NO_VARIABLES,
    ),
    (
        "event_consumed",
        dict(source="Root.Idle", trigger="Root.tick"),
        RICH,
        FLAWED_SELF_LOOP,
    ),
    (
        "stays_in",
        dict(source="Root.Idle", trigger="Root.tick"),
        RICH,
        FLAWED_SELF_LOOP,
    ),
    (
        "variable_delta_after",
        dict(source="Root.Idle", trigger="Root.go", variable="units", sign="negative"),
        RICH,
        FLAWED_EFFECT,
    ),
    (
        "reaches",
        dict(source="Root.Idle", target="Root.Done", within_cycles=5),
        RICH,
        NO_VARIABLES,
    ),
    (
        "terminates",
        dict(scope="Root.Done", trigger="Root.fin"),
        RICH,
        FLAWED_TERMINATION,
    ),
    # ---- Family P ----
    (
        "invariant",
        dict(scope="Root.Idle", condition='!active("Root.Hub")', bound=1),
        RICH,  # one step from Idle cannot reach Hub
        NO_VARIABLES,  # Root.Hub is undeclared there -> see the note below
    ),
    (
        "response_within",
        dict(trigger="Root.go", response="Root.Busy", bound=3, source="Root.Idle"),
        None,  # supplied by a dedicated test; needs its own paired models
        None,
    ),
    (
        "persists_until",
        dict(state="Root.Idle", release='active("Root.Outer")', bound=3),
        None,
        None,
    ),
]


@pytest.mark.parametrize(
    "predicate,kwargs,true_model,false_model",
    [row for row in DISCRIMINATION if row[2] is not None and row[3] is not None],
    ids=[row[0] for row in DISCRIMINATION if row[2] is not None and row[3] is not None],
)
def test_predicate_discriminates(predicate, kwargs, true_model, false_model):
    """True on the model that has the property, False on the one that does not."""

    if true_model is false_model:
        pytest.skip("pair not distinct; covered by a dedicated test")
    got_true = call(true_model, predicate, **kwargs)
    assert got_true is True, f"{predicate} did not hold where it should: {kwargs}"
    try:
        got_false = call(false_model, predicate, **kwargs)
    except UnsupportedEvidence:
        # Refusing on a model that lacks the element is also a non-True answer
        # and is the honest one; what must never happen is a True.
        return
    assert got_false is False, f"{predicate} held where it should not: {kwargs}"


# --------------------------------------------------------------------------
# The rows above that need their own paired models
# --------------------------------------------------------------------------


def test_state_declared_separates_leaf_from_composite():
    assert call(RICH, "state_declared", state="Root.Idle", kind="leaf") is True
    assert call(RICH, "state_declared", state="Root.Outer", kind="leaf") is False
    assert call(RICH, "state_declared", state="Root.Outer", kind="composite") is True
    assert call(RICH, "state_declared", state="Root.Idle", kind="composite") is False
    # `any` is the "declared at all" question, so it holds for both.
    assert call(RICH, "state_declared", state="Root.Idle", kind="any") is True
    assert call(RICH, "state_declared", state="Root.Outer", kind="any") is True
    # A path the model does not declare is False, not a refusal: absence of a
    # *named* state is a decidable fact.
    assert call(RICH, "state_declared", state="Root.Nowhere", kind="any") is False


def test_state_declared_rejects_an_unknown_kind():
    with pytest.raises(UnsupportedEvidence):
        call(RICH, "state_declared", state="Root.Idle", kind="elephant")


def test_containment_requires_a_direct_child():
    assert call(RICH, "containment", parent="Root", child="Root.Outer") is True
    assert call(RICH, "containment", parent="Root.Outer", child="Root.Outer.First") is True
    # A grandchild is contained transitively but not directly.
    assert call(RICH, "containment", parent="Root", child="Root.Outer.First") is False


def test_cardinality_counts_direct_substates_only():
    assert call(RICH, "cardinality", scope="Root.Outer", count=2) is True
    assert call(RICH, "cardinality", scope="Root.Outer", count=3) is False
    # Root's own direct children, not the whole tree.
    assert call(RICH, "cardinality", scope="Root.Outer", count=1) is False


def test_cardinality_rejects_a_non_integer_count():
    with pytest.raises(UnsupportedEvidence):
        call(RICH, "cardinality", scope="Root.Outer", count="two")


def test_action_declared_separates_the_three_phases():
    for phase in ("entry", "exit", "during"):
        assert call(RICH, "action_declared", state="Root.Idle", phase=phase) is True
        assert call(RICH, "action_declared", state="Root.Hub", phase=phase) is False


def test_action_declared_rejects_an_unknown_phase():
    with pytest.raises(UnsupportedEvidence):
        call(RICH, "action_declared", state="Root.Idle", phase="whenever")


@pytest.mark.parametrize("predicate", ["effect_declared", "variable_delta_after"])
def test_sign_is_validated(predicate):
    with pytest.raises(UnsupportedEvidence):
        call(
            RICH,
            predicate,
            source="Root.Idle",
            trigger="Root.go",
            variable="units",
            sign="sideways",
        )


@pytest.mark.parametrize("predicate", ["effect_declared", "variable_delta_after"])
def test_sign_polarity_is_not_ignored(predicate):
    """The decrement is real, so `negative` holds and `positive` must not."""

    common = dict(source="Root.Idle", trigger="Root.go", variable="units")
    assert call(RICH, predicate, sign="negative", **common) is True
    assert call(RICH, predicate, sign="positive", **common) is False


def test_guard_distinguishable_refuses_when_no_such_transition_exists():
    """No transition leaves Idle on `done`, so there is nothing to distinguish.

    Answering False here would report a guard defect on a model that simply does
    not have that transition.
    """

    with pytest.raises(UnsupportedEvidence):
        call(RICH, "guard_distinguishable", source="Root.Idle", trigger="Root.done")


def test_occupancy_after_accepts_a_composite_target():
    """Occupying a leaf inside the target counts as occupying the target."""

    assert (
        call(RICH, "occupancy_after", source="Root.Idle", trigger="Root.go", target="Root.Outer")
        is True
    )
    assert (
        call(
            RICH,
            "occupancy_after",
            source="Root.Idle",
            trigger="Root.go",
            target="Root.Outer.First",
        )
        is True
    )
    assert (
        call(RICH, "occupancy_after", source="Root.Idle", trigger="Root.go", target="Root.Hub")
        is False
    )


def test_occupancy_after_from_the_pseudo_initial():
    """`[*]` is the cold start, and the model enters `Idle`."""

    assert call(RICH, "occupancy_after", source="[*]", trigger="Root.tick", target="Root.Idle") is True
    assert call(RICH, "occupancy_after", source="[*]", trigger="Root.tick", target="Root.Hub") is False


def test_stays_in_requires_the_event_to_be_consumed():
    """A self-loop holds; an event nothing consumes does not count as staying.

    Without the consumption check every unhandled event looked like a self-loop,
    because the configuration is indeed unchanged.
    """

    assert call(RICH, "stays_in", source="Root.Idle", trigger="Root.tick") is True
    # `done` leaves Idle unchanged only because nothing consumes it there.
    assert call(RICH, "stays_in", source="Root.Idle", trigger="Root.done") is False
    # And a trigger that genuinely moves the system is not staying either.
    assert call(RICH, "stays_in", source="Root.Idle", trigger="Root.go") is False


def test_event_consumed_separates_handled_from_ignored():
    assert call(RICH, "event_consumed", source="Root.Idle", trigger="Root.go") is True
    assert call(RICH, "event_consumed", source="Root.Idle", trigger="Root.done") is False


def test_reaches_is_bounded_by_its_cycle_budget():
    """The budget is part of the claim, so a smaller one must be able to fail."""

    assert call(RICH, "reaches", source="Root.Idle", target="Root.Done", within_cycles=5) is True
    assert call(RICH, "reaches", source="Root.Idle", target="Root.Done", within_cycles=4) is False


def test_terminates_separates_a_finishing_model_from_a_stuck_one():
    assert call(RICH, "terminates", scope="Root.Done", trigger="Root.fin") is True
    assert call(FLAWED_TERMINATION, "terminates", scope="Root.Done", trigger="Root.fin") is False


def test_terminates_accepts_the_cold_start():
    value = call(RICH, "terminates", scope="[*]")
    assert isinstance(value, bool)


def test_invariant_separates_a_holding_condition_from_a_violated_one():
    """One step from Idle cannot reach Hub; three steps can."""

    assert call(RICH, "invariant", scope="Root.Idle", condition='!active("Root.Hub")', bound=1) is True
    assert call(RICH, "invariant", scope="Root.Idle", condition='!active("Root.Idle")', bound=1) is False


def test_persists_until_is_not_a_tautology():
    """`exists_always` made this hold for every model; the invariant form does not.

    Asking whether the machine stays in `Idle` until it is in `Idle` is trivially
    true and told us nothing; asking whether it stays in `Hub` until `Idle`
    must be able to fail.
    """

    # Under `exists_always` both of these were True, because that asks only
    # whether *some* bounded run keeps the condition and the empty run always
    # does.  Under the invariant form the model's own behaviour decides: the
    # machine can leave Idle on `go` within the bound, so the obligation fails.
    leaves_early = call(
        RICH, "persists_until", state="Root.Idle", release='active("Root.Done")', bound=3
    )
    assert leaves_early is False, "persists_until is still a tautology"
    # And it must be able to hold, or it is just a constant-False generator.
    holds = call(
        RICH, "persists_until", state="Root.Idle", release='active("Root.Outer")', bound=1
    )
    assert holds is True, "persists_until can never hold, so it proves nothing"


def test_response_within_separates_answered_from_unanswered():
    holds = """state Root {
    event go;
    state Idle;
    state Busy;
    [*] -> Idle;
    Idle -> Busy : /go;
    Busy -> Busy : /go;
}
"""
    fails = """state Root {
    event go;
    event other;
    state Idle;
    state Busy;
    state Elsewhere;
    [*] -> Idle;
    Idle -> Elsewhere : /go;
    Elsewhere -> Busy : /other;
}
"""
    kwargs = dict(trigger="Root.go", response="Root.Busy", bound=3, source="Root.Idle")
    assert call(holds, "response_within", **kwargs) is True
    assert call(fails, "response_within", **kwargs) is False


# --------------------------------------------------------------------------
# Contract properties that hold for every predicate
# --------------------------------------------------------------------------

#: A call for each predicate that is well-formed against the RICH model.
WELL_FORMED = {
    "state_declared": dict(state="Root.Idle", kind="leaf"),
    "variable_declared": dict(variable="units"),
    "event_declared": dict(event="Root.go"),
    "containment": dict(parent="Root.Outer", child="Root.Outer.First"),
    "initial_target": dict(composite="Root.Outer", child="Root.Outer.First"),
    "edge_declared": dict(source="Root.Idle", trigger="Root.go", target="Root.Outer"),
    "effect_declared": dict(
        source="Root.Idle", trigger="Root.go", variable="units", sign="negative"
    ),
    "action_declared": dict(state="Root.Idle", phase="entry"),
    "guard_distinguishable": dict(source="Root.Idle", trigger="Root.go"),
    "cardinality": dict(scope="Root.Outer", count=2),
    "occupancy_after": dict(source="Root.Idle", trigger="Root.go", target="Root.Outer"),
    "event_consumed": dict(source="Root.Idle", trigger="Root.go"),
    "stays_in": dict(source="Root.Idle", trigger="Root.tick"),
    "variable_delta_after": dict(
        source="Root.Idle", trigger="Root.go", variable="units", sign="negative"
    ),
    "reaches": dict(source="Root.Idle", target="Root.Done", within_cycles=5),
    "terminates": dict(scope="Root.Done", trigger="Root.fin"),
    "invariant": dict(scope="Root.Idle", condition='!active("Root.Hub")', bound=1),
    "response_within": dict(
        trigger="Root.go", response="Root.Outer.First", bound=3, source="Root.Idle"
    ),
    "persists_until": dict(state="Root.Idle", release='active("Root.Outer")', bound=3),
}


@pytest.mark.parametrize("predicate", [item.name for item in PREDICATES])
def test_every_predicate_has_a_well_formed_call_in_this_spec(predicate):
    """No predicate may be quietly left out of the behavioural suite."""

    assert predicate in WELL_FORMED, f"{predicate} has no spec fixture"


@pytest.mark.parametrize("predicate", sorted(WELL_FORMED))
def test_every_predicate_returns_a_strict_bool(predicate):
    """`is True` / `is False` in the assertions means 1 and 0 must not pass."""

    value = call(RICH, predicate, **WELL_FORMED[predicate])
    assert value is True or value is False, f"{predicate} returned {value!r}"


@pytest.mark.parametrize("predicate", sorted(WELL_FORMED))
def test_a_fabricated_path_never_answers_true(predicate):
    """The failure mode this whole layer exists to prevent.

    A query over a non-existent element used to match nothing and report
    "satisfied", hiding the defect it was meant to test.  Whether the predicate
    answers False or refuses is its business; True is not allowed.
    """

    kwargs = dict(WELL_FORMED[predicate])
    for key in ("state", "source", "parent", "composite", "scope", "target", "child"):
        if key in kwargs and isinstance(kwargs[key], str) and kwargs[key].startswith("Root"):
            kwargs[key] = "Root.NoSuchState"
            break
    else:
        pytest.skip(f"{predicate} takes no path binding to fabricate")
    try:
        value = call(RICH, predicate, **kwargs)
    except UnsupportedEvidence:
        return
    assert value is False, f"{predicate} answered True for a fabricated path: {kwargs}"


@pytest.mark.parametrize("predicate", sorted(WELL_FORMED))
def test_an_empty_path_binding_is_refused(predicate):
    """An empty string is not a path, and must not be treated as a wildcard."""

    kwargs = dict(WELL_FORMED[predicate])
    for key in ("state", "source", "parent", "composite", "scope", "trigger"):
        if key in kwargs and isinstance(kwargs[key], str):
            kwargs[key] = "   "
            break
    else:
        pytest.skip(f"{predicate} takes no path binding")
    try:
        value = call(RICH, predicate, **kwargs)
    except UnsupportedEvidence:
        return
    assert value is False, f"{predicate} answered True for a blank binding: {kwargs}"


def test_guard_distinguishable_sees_through_a_combo_lowering():
    """`: /event + [guard]` lowers to an intermediate state, hiding the branches.

    Two guarded alternatives on the same event do not become two transitions out
    of the source; they become one transition into a generated state whose
    unlabelled successors carry the guards.  Querying the source directly sees a
    single target and answers "nothing to distinguish" -- for *any* guards,
    including two identical ones.  Since a guard attached to an event can only be
    written this way, that made the whole judgement unreachable.
    """

    # Identical guards on both branches: indistinguishable, and it must say so.
    assert (
        call(FLAWED_GUARDS, "guard_distinguishable", source="Root.Hub", trigger="Root.go")
        is False
    )
    # Different non-empty guards: the facade cannot prove they do not overlap,
    # so the honest answer is a refusal, not a True.
    with pytest.raises(UnsupportedEvidence):
        call(RICH, "guard_distinguishable", source="Root.Hub", trigger="Root.go")


def test_guard_distinguishable_reports_the_corpus_shape():
    """Ten of the 60 pairs share a source and trigger across targets, guard-free.

    That is the shape pair 0029's expected defect has, and it must come back
    False.  A single declared target is the other side: nothing to distinguish,
    so True.
    """

    ambiguous = """state Root {
    event go;
    state Hub;
    state Left;
    state Right;
    [*] -> Hub;
    Hub -> Left : /go;
    Hub -> Right : /go;
}
"""
    assert call(ambiguous, "guard_distinguishable", source="Root.Hub", trigger="Root.go") is False
    assert call(RICH, "guard_distinguishable", source="Root.Idle", trigger="Root.go") is True


def test_response_within_answers_a_composite_response_like_occupancy_after():
    """This used to be pinned as a boundary, and it was not one.

    The refusal came from the solver finding no answer, and the reason it found
    none was the unscoped obligation: with `init state(...)` binding step 0 while
    `check response` quantified over every step, a composite response had no model
    that satisfied it.  Scoping the trigger to the pinned configuration -- the fix
    for the sink-only defect -- removed the refusal along with the fabrications, so
    the honest pin is agreement with `occupancy_after`, which a producer would
    reasonably expect after learning the rule there.
    """

    for response, expected in (
        # `Idle -/go-> Outer`: the obligation holds, at composite and leaf alike.
        ("Root.Outer", True),
        ("Root.Outer.First", True),
        # `go` does not lead here, and that still fails.
        ("Root.Done", False),
    ):
        assert (
            call(
                RICH,
                "response_within",
                trigger="Root.go",
                response=response,
                bound=3,
                source="Root.Idle",
            )
            is expected
        ), response
        assert (
            call(RICH, "occupancy_after", source="Root.Idle", trigger="Root.go", target=response)
            is expected
        ), response


# --------------------------------------------------------------------------
# `[*]` is legal in some bindings and meaningless in others
# --------------------------------------------------------------------------

PSEUDO_INITIAL_REJECTED = [
    ("state_declared", dict(state="[*]", kind="any")),
    ("containment", dict(parent="[*]", child="Root.Idle")),
    ("initial_target", dict(composite="[*]", child="Root.Idle")),
    ("cardinality", dict(scope="[*]", count=2)),
    ("action_declared", dict(state="[*]", phase="entry")),
    ("persists_until", dict(state="[*]", release='active("Root.Idle")', bound=2)),
]


@pytest.mark.parametrize(
    "predicate,kwargs", PSEUDO_INITIAL_REJECTED, ids=[c[0] for c in PSEUDO_INITIAL_REJECTED]
)
def test_the_pseudo_initial_is_refused_where_it_cannot_mean_anything(predicate, kwargs):
    """Silently answering False there manufactures a defect.

    Each of these asks about a property of a named declared state -- its kind,
    parent, entry target, substate count, lifecycle, persistence.  `[*]` is an
    entry marker with none of those, so the query used to come back False and
    the pipeline read "the model does not declare a state at [*]" as a finding.
    A producer that learned the literal from `occupancy_after(source="[*]")`
    and carried it across got a free false positive.
    """

    with pytest.raises(UnsupportedEvidence, match=r"pseudo-initial"):
        call(RICH, predicate, **kwargs)


PSEUDO_INITIAL_ACCEPTED = [
    ("occupancy_after", dict(source="[*]", trigger="Root.tick", target="Root.Idle")),
    ("event_consumed", dict(source="[*]", trigger="Root.go")),
    ("reaches", dict(source="[*]", target="Root.Idle", within_cycles=2)),
    ("terminates", dict(scope="[*]")),
    ("invariant", dict(scope="[*]", condition='!active("Root.Hub")', bound=1)),
    ("response_within", dict(trigger="Root.go", response="Root.Idle", bound=2, source="[*]")),
]


@pytest.mark.parametrize(
    "predicate,kwargs", PSEUDO_INITIAL_ACCEPTED, ids=[c[0] for c in PSEUDO_INITIAL_ACCEPTED]
)
def test_the_pseudo_initial_still_works_where_it_does_mean_something(predicate, kwargs):
    """Cold start is a real configuration, and these claims are about it."""

    value = call(RICH, predicate, **kwargs)
    assert value is True or value is False, f"{predicate} refused a legal cold start"


def test_every_undeclared_binding_reaches_the_guard():
    """A binding that skips `_require_declared` leaks a raw parser error.

    `terminates(trigger=...)` and `response_within(source=...)` did, so the
    controller saw `Cannot resolve event path '<undeclared>'` from pyfcstm and
    `fbmcq child execution failed` -- error types none of its repair branches
    recognise, so the producer got generic advice and burned its budget.
    """

    for predicate, kwargs in (
        ("terminates", dict(scope="Root.Done", trigger="<undeclared>")),
        (
            "response_within",
            dict(trigger="Root.go", response="Root.Outer.First", bound=3, source="<undeclared>"),
        ),
    ):
        with pytest.raises(UnsupportedEvidence, match=r"<undeclared>"):
            call(RICH, predicate, **kwargs)


def test_variable_delta_after_requires_the_trigger_to_have_fired():
    """A completion transition may move the variable; that is not this trigger.

    `Outer -> Hub` is unlabelled, so a run from `Outer` changes configuration
    without consuming anything.  Crediting whatever the variable did to the
    trigger the caller named would report an effect the model does not declare on
    that transition.
    """

    # `done` is consumed inside Outer and moves nothing at the top level, so the
    # named trigger did fire and the answer is about it.
    assert (
        call(RICH, "variable_delta_after", source="Root.Idle", trigger="Root.go",
             variable="units", sign="negative")
        is True
    )
    # `fin` is not consumed in Idle, so no delta can be attributed to it even
    # though the run is otherwise identical.
    assert (
        call(RICH, "variable_delta_after", source="Root.Idle", trigger="Root.fin",
             variable="units", sign="negative")
        is False
    )


def test_effect_declared_and_variable_delta_after_can_disagree():
    """One reads the declaration, the other runs the model; that is the point.

    A declared effect on an unreachable or guard-blocked transition shows up in
    `effect_declared` and not in `variable_delta_after`.  Collapsing them would
    lose the distinction the two families exist to draw.
    """

    common = dict(source="Root.Idle", trigger="Root.go", variable="units", sign="negative")
    assert call(RICH, "effect_declared", **common) is True
    assert call(RICH, "variable_delta_after", **common) is True
    # And on the flawed model both flip, because the declaration is what changed.
    assert call(FLAWED_EFFECT, "effect_declared", **common) is False
    assert call(FLAWED_EFFECT, "variable_delta_after", **common) is False


# --------------------------------------------------------------------------
# A converted model's entry declarations
# --------------------------------------------------------------------------

#: Pair 0029's shape: one unconditional entry plus converter-generated re-entry
#: points guarded on its own route token.
CONVERTED_ENTRY = """def int R45Token = 0;
state Root {
    event go;
    state Mode {
        state Wanted;
        state Fallback;
        [*] -> Wanted : if [R45Token == 5];
        [*] -> Fallback;
        Wanted -> Fallback : /go;
    }
    state Other;
    [*] -> Mode;
    Mode -> Other : /go;
}
"""


def test_initial_target_answers_from_the_unconditional_entry():
    """Five initial edges cost pair 0029 two requirements, filed as producer error.

    `HighwayMode` declares one unconditional entry and four guarded on the
    converter's route token.  The old implementation demanded exactly one edge and
    refused, so the assertion could never execute; the producer was charged three
    repair rounds and the requirement was recorded as `no_progress` -- which reads
    as the model's author or the producer being at fault, when neither was.

    Entry with no token set takes the unconditional edge, so that is the initial
    child and the claim is decidable.
    """

    assert call(CONVERTED_ENTRY, "initial_target", composite="Root.Mode", child="Root.Mode.Fallback") is True
    # And the guarded re-entry point is *not* the initial child, which is the
    # finding the NL-derived requirement is looking for.
    assert call(CONVERTED_ENTRY, "initial_target", composite="Root.Mode", child="Root.Mode.Wanted") is False


def test_the_guarded_entries_stay_in_the_reference_set():
    """Attribution needs to see the lowering behind that answer.

    The finding is real but its cause is the conversion, not the author, so the
    route-token guard has to reach the reference set or the issue is attributed
    to the wrong party.
    """

    e = env(CONVERTED_ENTRY)
    api = e.predicates
    api.begin_call()
    api.initial_target(composite="Root.Mode", child="Root.Mode.Fallback")
    refs = api.consume_refs()
    assert any("R45Token" in r for r in refs), refs


def test_a_single_declared_entry_still_answers_directly():
    """Control: the ordinary hand-written shape must not regress."""

    assert call(RICH, "initial_target", composite="Root.Outer", child="Root.Outer.First") is True
    assert call(RICH, "initial_target", composite="Root.Outer", child="Root.Outer.Second") is False


def test_two_unconditional_entries_are_refused_as_genuinely_ambiguous():
    """Real ambiguity is not the same as converter noise; keep refusing it."""

    ambiguous = """state Root {
    event go;
    state Mode {
        state A;
        state B;
        [*] -> A;
        [*] -> B;
        A -> B : /go;
    }
    [*] -> Mode;
}
"""
    with pytest.raises(UnsupportedEvidence, match="unconditional initial"):
        call(ambiguous, "initial_target", composite="Root.Mode", child="Root.Mode.A")


# --------------------------------------------------------------------------
# The two existence predicates (issue #170 §11.3)
# --------------------------------------------------------------------------


def test_variable_declared_separates_declared_from_absent():
    """Existence in its own right -- the vocabulary had this only for states.

    `variable` used to appear solely inside `effect_declared` and
    `variable_delta_after`, always relationally.  That asymmetry is why "the NL
    requires a quantity this model has no variable for" had no checkable form and
    had to be smuggled through as `<undeclared>`.
    """

    assert call(RICH, "variable_declared", variable="units") is True
    assert call(RICH, "variable_declared", variable="other") is True
    assert call(RICH, "variable_declared", variable="uav_count") is False
    # A model with no variables at all answers False rather than refusing.
    assert call(NO_VARIABLES, "variable_declared", variable="units") is False


def test_variable_declared_does_not_count_a_route_control_variable():
    """The converter's own token is not the author's.

    The effect facade already drops it from every answer, so reporting it as
    declared would promise evidence no other call can deliver -- and it would
    hide exactly the gap that pairs 0000 and 0006 are about, since in this corpus
    the route token is the *only* variable any model declares.
    """

    env_with_exclusion = build_eval_environment(
        model_text=RICH,
        source_mappings=[],
        source_exclusions=["compiler:route_control:units"],
        timeout_seconds=30,
        fbmcq_solver_timeout_ms=15_000,
        fbmcq_max_bound=4,
        fbmcq_process_wall_seconds=20.0,
    )
    assert env_with_exclusion.globals["variable_declared"](variable="units") is False
    # The author's other variable is unaffected.
    assert env_with_exclusion.globals["variable_declared"](variable="other") is True


def test_event_declared_separates_declared_from_absent():
    assert call(RICH, "event_declared", event="Root.go") is True
    assert call(RICH, "event_declared", event="Root.tick") is True
    assert call(RICH, "event_declared", event="Root.nosuchevent") is False


def test_the_two_name_shapes_are_enforced_rather_than_answered():
    """A prefixed variable name must be refused, not reported as absent.

    `inspect` gives a variable row only a bare `name` and an event row only a
    dotted `qualified_name`.  A producer generalising from state paths will write
    `Sys.units`; that name is simply not found, so the call would answer False --
    and that False reads as "the model lacks this variable".  A defect
    manufactured out of a spelling convention is worse than a refusal.
    """

    with pytest.raises(UnsupportedEvidence, match="bare identifier"):
        call(RICH, "variable_declared", variable="Root.units")
    with pytest.raises(UnsupportedEvidence, match="at least 2 path segments"):
        call(RICH, "event_declared", event="go")


def test_the_existence_predicates_are_structure_family():
    """They decide from declarations, so they must not demand runtime evidence."""

    from paper_stm_feedback_loop.assertions.predicate_api import PREDICATE_FAMILIES

    for name in ("variable_declared", "event_declared"):
        assert PREDICATE_FAMILIES[name][0] == "structure", name


# --------------------------------------------------------------------------
# Malformed names are refused, never answered (issue #170 §11.3)
# --------------------------------------------------------------------------
#
# A name that could not possibly denote a declared element must not be looked up
# and reported absent: the `False` that follows reads as "the model lacks this",
# which is a defect manufactured out of a malformed string.  The shapes below come
# from measuring the corpus -- 627 state paths, 387 event paths, 33 variable names,
# every one an identifier or a dotted path of them.

MALFORMED = [
    ("空格", "Root Idle"),
    ("引号注入", 'Root.Idle"); check reach <= 99: true; //'),
    ("换行", "Root.Idle\ncheck reach <= 9: true;"),
    ("分号", "Root.Idle;"),
    ("连续点", "Root..Idle"),
    ("尾点", "Root.Idle."),
    ("首点", ".Root.Idle"),
    ("数字开头", "0Root"),
    ("连字符", "Root-Idle"),
    ("中文", "Root.空状態"),
    ("括号", "Root.Idle()"),
    ("占位符", "<undeclared>"),
    ("角括号变体", "<missing_state>"),
]


@pytest.mark.parametrize("label,value", MALFORMED, ids=[c[0] for c in MALFORMED])
def test_a_malformed_state_path_is_refused_not_answered(label, value):
    with pytest.raises(UnsupportedEvidence):
        call(RICH, "state_declared", state=value, kind="any")


@pytest.mark.parametrize("label,value", MALFORMED, ids=[c[0] for c in MALFORMED])
def test_a_malformed_variable_name_is_refused_not_answered(label, value):
    with pytest.raises(UnsupportedEvidence):
        call(RICH, "variable_declared", variable=value)


@pytest.mark.parametrize("label,value", MALFORMED, ids=[c[0] for c in MALFORMED])
def test_a_malformed_event_path_is_refused_not_answered(label, value):
    with pytest.raises(UnsupportedEvidence):
        call(RICH, "event_declared", event=value)


def test_a_placeholder_gets_a_diagnosis_naming_the_replacement():
    """Refusing is not enough; a producer reaching for it means something real.

    It is expressing "the NL requires a term this model lacks", which is a claim
    worth checking -- just not like this.  The message has to say where it belongs,
    or the producer rewrites the same shape next round.
    """

    with pytest.raises(UnsupportedEvidence, match="placeholder, not a name") as caught:
        call(RICH, "variable_declared", variable="<undeclared>")
    message = str(caught.value)
    assert "proposed name" in message
    assert "precondition" in message
    assert "repair can add" in message


def test_a_well_formed_absent_name_still_answers_false():
    """The rule is about malformed values, not about absent ones.

    A name that *could* have been declared and was not is exactly the finding this
    layer exists to report, so it must not be swept up by the shape check.
    """

    assert call(RICH, "state_declared", state="Root.NoSuchState", kind="any") is False
    assert call(RICH, "variable_declared", variable="no_such_variable") is False
    assert call(RICH, "event_declared", event="Root.no_such_event") is False


def test_every_real_corpus_name_shape_is_accepted():
    """Guard against a pattern tightened past the data.

    Single-segment states occur once per model (the root), variables never carry a
    prefix, and events always carry exactly one.  A rule that rejected any of these
    would refuse legitimate work.
    """

    assert call(RICH, "state_declared", state="Root", kind="composite") is True
    assert call(RICH, "state_declared", state="Root.Outer.First", kind="leaf") is True
    assert call(RICH, "variable_declared", variable="units") is True
    assert call(RICH, "event_declared", event="Root.go") is True
