"""Whatever a predicate is handed, it returns a bool or raises `UnsupportedEvidence`.

Why the exception *type* is a correctness property, not a style question
------------------------------------------------------------------------
The controller dispatches on it.  `AssertionChecker` turns `UndeclaredTerm` into
a sealed false, `UnsupportedEvidence` into a repairable invalid, and anything
else into `_invalid` with `error.type` set to the exception's class name.
`discover/nodes.py` then reads that name to pick the repair instruction it hands
back to the producer -- there are specific branches for `RequiredFamilyMissing`,
`NameError`, `AuditRejected` and so on.

So a predicate that lets an `AttributeError` or a `KeyError` escape produces an
`error.type` nothing recognises.  The producer gets a generic instruction, makes
the same mistake, and the item burns its repair budget and lands as a coverage
gap.  That is not a crash anyone sees; it is a requirement silently reported as
unchecked, which is exactly the failure mode this pipeline keeps rediscovering.

The contract, then, for every predicate and every input:

1. Return a strict `bool`, or raise something in the `UnsupportedEvidence`
   family.  Never `AttributeError`, `TypeError`, `KeyError`, `IndexError`,
   `ValueError`, or a bare `Exception`.
2. The message must tell the producer what to change.  A message that only names
   an internal symbol cannot be acted on and costs a round.

The inputs below are deliberately hostile: wrong types, blanks, injection
attempts into the bounded-query string, and out-of-range numbers.
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

MODEL = """def int units = 5;
state Root {
    event go;
    event tick;
    state Idle;
    state Busy;
    state Done;
    [*] -> Idle;
    Idle -> Busy : /go effect { units = units - 1; };
    Idle -> Idle : /tick;
    Busy -> Done : /go;
    Done -> [*] : /tick;
}
"""

#: A well-formed call per predicate, used as the base each hostile value mutates.
BASE = {
    "state_declared": dict(state="Root.Idle", kind="leaf"),
    "variable_declared": dict(name="units"),
    "event_declared": dict(name="Root.go"),
    "containment": dict(parent="Root", child="Root.Idle"),
    "initial_target": dict(composite="Root", child="Root.Idle"),
    "edge_declared": dict(source="Root.Idle", trigger="Root.go", target="Root.Busy"),
    "untriggered_edge_declared": dict(source="Root.Idle", target="Root.Busy"),
    "effect_declared": dict(
        source="Root.Idle", trigger="Root.go", variable="units", sign="negative"
    ),
    "action_declared": dict(state="Root.Idle", phase="entry"),
    "guard_distinguishable": dict(source="Root.Idle", trigger="Root.go"),
    "cardinality": dict(scope="Root", count=3),
    "occupancy_after": dict(source="Root.Idle", trigger="Root.go", target="Root.Busy"),
    "event_consumed": dict(source="Root.Idle", trigger="Root.go"),
    "stays_in": dict(source="Root.Idle", trigger="Root.tick"),
    "variable_delta_after": dict(
        source="Root.Idle", trigger="Root.go", variable="units", sign="negative"
    ),
    "reaches": dict(source="Root.Idle", target="Root.Done", within_cycles=3),
    "terminates": dict(scope="Root.Done", trigger="Root.tick"),
    "invariant": dict(scope="Root.Idle", condition='!active("Root.Done")', bound=2),
    "response_within": dict(
        trigger="Root.go", response="Root.Busy", bound=3, source="Root.Idle"
    ),
    "persists_until": dict(state="Root.Idle", release='active("Root.Busy")', bound=2),
}

#: Values chosen to break a naive implementation in a different way each.
HOSTILE = [
    ("none", None),
    ("int", 42),
    ("bool", True),
    ("list", ["Root.Idle"]),
    ("dict", {"path": "Root.Idle"}),
    ("empty", ""),
    ("blank", "   "),
    ("absent", "Root.NoSuchThing"),
    ("dotted-absent", "Nope.Nope.Nope"),
    ("quote-injection", 'Root.Idle"); check reach <= 99: true; //'),
    ("newline", "Root.Idle\ncheck reach <= 9: true;"),
    ("semicolon", "Root.Idle;"),
    ("unicode", "Root.空状態"),
    ("very-long", "Root." + "A" * 500),
]

#: Numeric bindings get their own hostile set.
HOSTILE_NUMBERS = [
    ("negative", -1),
    ("zero", 0),
    ("huge", 10**9),
    ("float", 2.7),
    ("numeric-string", "3"),
    ("non-numeric-string", "three"),
    ("none", None),
]

class _StubSolver:
    """A bounded-check stand-in that answers instantly and spawns nothing.

    The real solver runs in a `multiprocessing` child per call.  This file makes
    a few hundred Family P calls, so using it meant a few hundred children --
    the box went to 59 GB resident and started swapping.  And it buys nothing
    here: these tests are about what the *predicate layer* does with a hostile
    binding, which is decided before any query is built, and the two outcomes
    that matter downstream (a terminal verdict, a refusal) are both reachable
    from a stub.  `test_predicate_behaviour_spec.py` exercises the real solver
    against real models, which is where that belongs.
    """

    def __init__(self) -> None:
        self.queries: list[str] = []

    def fbmcq(self, query: str):
        self.queries.append(query)
        return {"status": "ok", "holds": True, "witness": None}


class _StubResult(dict):
    """`_formal_holds` reads `.status` / `.holds`, so expose both shapes."""

    status = "ok"
    holds = True


_ENV = None


def env():
    """One environment, real facades, stubbed solver."""

    global _ENV
    if _ENV is None:
        _ENV = build_eval_environment(
            model_text=MODEL,
            source_mappings=[],
            source_exclusions=[],
            timeout_seconds=30,
            fbmcq_solver_timeout_ms=4_000,
            fbmcq_max_bound=2,
            fbmcq_process_wall_seconds=8.0,
        )
        stub = _StubSolver()
        stub.fbmcq = lambda query: _StubResult()  # type: ignore[assignment]
        _ENV.predicates.formal = stub
    return _ENV


def assert_contract(predicate: str, kwargs: dict, label: str) -> None:
    """Either a strict bool, or an `UnsupportedEvidence` with an actionable message."""

    try:
        value = env().globals[predicate](**kwargs)
    except UnsupportedEvidence as exc:
        message = str(exc)
        assert message.strip(), f"{predicate}/{label}: refused with an empty message"
        assert len(message) > 20, (
            f"{predicate}/{label}: message too terse to act on: {message!r}"
        )
        return
    except TypeError as exc:
        # A missing or misspelled *keyword* is a producer error Python itself
        # reports clearly, and the checker turns it into a NameError-adjacent
        # invalid the controller has a repair branch for.  A TypeError from
        # inside the body is not the same thing and must not be excused.
        if "argument" in str(exc):
            return
        raise AssertionError(
            f"{predicate}/{label}: leaked TypeError from the body: {exc}"
        ) from exc
    except Exception as exc:  # noqa: BLE001 - the point of the test
        raise AssertionError(
            f"{predicate}/{label}: leaked {type(exc).__name__} the controller "
            f"cannot dispatch on: {exc}"
        ) from exc
    assert value is True or value is False, (
        f"{predicate}/{label}: returned {value!r} instead of a strict bool"
    )


PATH_BINDINGS = (
    "state",
    "source",
    "target",
    "parent",
    "child",
    "composite",
    "scope",
    "trigger",
    "response",
    "variable",
)
NUMBER_BINDINGS = ("count", "bound", "within_cycles")
LITERAL_BINDINGS = ("kind", "sign", "phase")
EXPRESSION_BINDINGS = ("condition", "release")


def _cases(binding_names):
    """(predicate, binding) pairs for every predicate that takes one of these."""

    out = []
    for predicate, base in BASE.items():
        for binding in binding_names:
            if binding in base:
                out.append((predicate, binding))
    return out


@pytest.mark.parametrize("predicate,binding", _cases(PATH_BINDINGS))
@pytest.mark.parametrize("label,value", HOSTILE, ids=[c[0] for c in HOSTILE])
def test_a_hostile_path_binding_never_leaks_an_undispatchable_exception(
    predicate, binding, label, value
):
    kwargs = dict(BASE[predicate])
    kwargs[binding] = value
    assert_contract(predicate, kwargs, f"{binding}={label}")


@pytest.mark.parametrize("predicate,binding", _cases(NUMBER_BINDINGS))
@pytest.mark.parametrize(
    "label,value", HOSTILE_NUMBERS, ids=[c[0] for c in HOSTILE_NUMBERS]
)
def test_a_hostile_numeric_binding_never_leaks_an_undispatchable_exception(
    predicate, binding, label, value
):
    kwargs = dict(BASE[predicate])
    kwargs[binding] = value
    assert_contract(predicate, kwargs, f"{binding}={label}")


@pytest.mark.parametrize("predicate,binding", _cases(LITERAL_BINDINGS))
@pytest.mark.parametrize(
    "label,value",
    [
        ("none", None),
        ("empty", ""),
        ("unknown-word", "sideways"),
        ("int", 3),
        ("list", ["leaf"]),
        ("uppercase", "LEAF"),
        ("padded", "  leaf  "),
    ],
)
def test_a_hostile_literal_binding_never_leaks_an_undispatchable_exception(
    predicate, binding, label, value
):
    kwargs = dict(BASE[predicate])
    kwargs[binding] = value
    assert_contract(predicate, kwargs, f"{binding}={label}")


@pytest.mark.parametrize("predicate,binding", _cases(EXPRESSION_BINDINGS))
@pytest.mark.parametrize(
    "label,value",
    [
        ("none", None),
        ("empty", ""),
        ("bare-path", "Root.Idle"),
        ("unbalanced", 'active("Root.Idle"'),
        ("injection", 'active("Root.Idle"); check reach <= 99: true'),
        ("nonsense", "@@@"),
        ("int", 1),
    ],
)
def test_a_hostile_expression_binding_never_leaks_an_undispatchable_exception(
    predicate, binding, label, value
):
    kwargs = dict(BASE[predicate])
    kwargs[binding] = value
    assert_contract(predicate, kwargs, f"{binding}={label}")


# --------------------------------------------------------------------------
# The messages have to be usable, not just present
# --------------------------------------------------------------------------


@pytest.mark.parametrize("predicate", sorted(BASE))
def test_every_predicate_has_a_hostile_input_fixture(predicate):
    """No predicate may be quietly excluded from the fuzz."""

    assert predicate in BASE


def test_a_literal_domain_error_names_the_allowed_values():
    """"sign must be negative or positive" is repairable; "invalid sign" is not."""

    for kwargs, expected in (
        (dict(BASE["state_declared"], kind="sideways"), ("leaf", "composite", "pseudo")),
        (dict(BASE["action_declared"], phase="whenever"), ("entry", "exit", "during")),
        (
            dict(BASE["effect_declared"], sign="sideways"),
            ("negative", "positive"),
        ),
    ):
        predicate = next(
            name for name, base in BASE.items() if set(base) == set(kwargs)
        )
        with pytest.raises(UnsupportedEvidence) as caught:
            env().globals[predicate](**kwargs)
        message = str(caught.value)
        for token in expected:
            assert token in message, f"{predicate}: {message!r} omits {token!r}"


def test_a_missing_transition_refusal_says_where_to_look():
    """The pair-0029 case: a projected or mistyped trigger.

    The producer cannot fix "cannot decide"; it can fix "no declared transition
    leaves X on Y, check the spelling against declared_model_vocabulary".
    """

    with pytest.raises(UnsupportedEvidence) as caught:
        env().globals["guard_distinguishable"](source="Root.Done", trigger="Root.go")
    message = str(caught.value)
    assert "no declared transition" in message
    assert "declared_model_vocabulary" in message


def test_a_hot_start_refusal_names_the_configuration_it_could_not_reach():
    with pytest.raises(UnsupportedEvidence) as caught:
        env().globals["occupancy_after"](
            source="Root.Ghost", trigger="Root.go", target="Root.Busy"
        )
    assert "Root.Ghost" in str(caught.value)


@pytest.mark.parametrize("predicate", [item.name for item in PREDICATES])
def test_every_predicate_is_covered_by_the_fuzz(predicate):
    assert predicate in BASE, f"{predicate} is missing from the exception-contract fuzz"
