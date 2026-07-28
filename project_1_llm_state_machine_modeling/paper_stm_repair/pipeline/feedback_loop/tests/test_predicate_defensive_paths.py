"""The branches a real model cannot reach: refusals, taint, and failure guards.

`test_predicate_behaviour_spec.py` drives the predicates through real FCSTM
models, which is the right way to check that they decide what they claim.  It
cannot reach three kinds of branch:

* **Refusals that need a broken environment** -- no solver configured, a solver
  timeout, a non-terminal verdict.  Each of these must come back as
  `UnsupportedEvidence`, because the alternative is a False, and a False here
  reports a defect that the run merely failed to check.
* **Attribution taint** -- a simulated trace whose fired transitions are
  ambiguous must mark itself, or a finding derived from it gets attributed to a
  model element the run cannot prove it rested on.
* **Guards around audit metadata** -- reference collection, variable seeding and
  the like are wrapped in `except` for one reason: a failure there must never
  change an outcome.  That property is only observable by making them fail.

So this file injects minimal fakes.  The fakes are deliberately dumb: each one
exists to make exactly one branch reachable, and asserting on real behaviour
stays the job of the spec file.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.assertions.exceptions import (  # noqa: E402
    UndeclaredTerm,
    UnsupportedEvidence,
)
from paper_stm_feedback_loop.assertions.predicate_api import PredicateAPI  # noqa: E402


class Row:
    """A structure row with only the attributes the predicates read."""

    def __init__(self, **fields):
        self.__dict__.update(fields)


class Cycle:
    def __init__(self, **fields):
        self.__dict__.setdefault("path_refs", ())
        self.__dict__.setdefault("fired_transitions", ())
        self.__dict__.setdefault("unconsumed_events", ())
        self.__dict__.setdefault("active_states", ())
        self.__dict__.update(fields)


class View:
    def __init__(self, cycles=(), final=None, effective_initialization=None):
        self.cycles = tuple(cycles)
        self.final = final
        self.effective_initialization = effective_initialization


class Structure:
    """Answers whatever the test hands it; raises when told to."""

    def __init__(self, *, states=(), events=(), variables=(), transitions=(), boom=()):
        self._states = list(states)
        self._events = list(events)
        self._variables = list(variables)
        self._transitions = list(transitions)
        self._boom = set(boom)

    def _guard(self, name):
        if name in self._boom:
            raise RuntimeError(f"{name} facade is broken")

    def states(self, **_kwargs):
        self._guard("states")
        return tuple(self._states)

    def events(self, **_kwargs):
        self._guard("events")
        return tuple(self._events)

    def variables(self, **_kwargs):
        self._guard("variables")
        return tuple(self._variables)

    def transitions(self, **_kwargs):
        self._guard("transitions")
        return tuple(self._transitions)


class Relations:
    def __init__(self, *, overlap=None):
        self._overlap = overlap

    def transitions(self, **_kwargs):
        return ()

    def conflicting_targets(self, **_kwargs):
        return False

    def guards_overlap(self, _left, _right):
        if isinstance(self._overlap, Exception):
            raise self._overlap
        return bool(self._overlap)


class Formal:
    def __init__(self, *, result=None, raises=None):
        self._result = result
        self._raises = raises

    def fbmcq(self, _query):
        if self._raises is not None:
            raise self._raises
        return self._result


def api(**overrides) -> PredicateAPI:
    kwargs = dict(
        structure=Structure(),
        relations=Relations(),
        effects=object(),
        simulation=object(),
    )
    kwargs.update(overrides)
    return PredicateAPI(**kwargs)


# --------------------------------------------------------------------------
# Attribution taint: an ambiguous trace must say so
# --------------------------------------------------------------------------


def test_an_ambiguous_trace_marks_itself():
    """Otherwise a finding is attributed to a path the run cannot prove it took.

    The fired-transition derivation is what lets a simulated result be tainted
    by the exclusion table the same way a static query is.  When the derivation
    cannot pin a unique path it says `ambiguous`, and that has to survive into
    the reference set -- silently dropping it upgrades an unprovable attribution
    to a confident one.
    """

    subject = api()
    subject.begin_call()
    subject._note_simulation(
        View(cycles=[Cycle(path_taint="ambiguous", path_refs=("transition:tr_1",))])
    )
    refs = subject.consume_refs()
    assert "simulation:path_taint:ambiguous" in refs
    assert "transition:tr_1" in refs


def test_a_clean_trace_does_not_claim_ambiguity():
    subject = api()
    subject.begin_call()
    subject._note_simulation(View(cycles=[Cycle(path_taint="clean", path_refs=("transition:tr_1",))]))
    assert "simulation:path_taint:ambiguous" not in subject.consume_refs()


def test_an_ignored_event_is_anchored_to_the_transitions_that_declare_it():
    """"Nothing happened" is often the defect, and it leaves no path to attribute.

    Without the anchor a real finding lands as `unattributed`, which reads as
    "we could not tell" rather than "the model ignores this event here".
    """

    subject = api(
        structure=Structure(transitions=[Row(to_path="Root.B", transition_index=0)])
    )
    subject.begin_call()
    subject._note_simulation(
        View(cycles=[Cycle(fired_transitions=(), unconsumed_events=("Root.go",))])
    )
    assert "Root.go" in subject.consume_refs()


# --------------------------------------------------------------------------
# Bounded checking: every non-answer is a refusal, never a False
# --------------------------------------------------------------------------


def test_no_solver_configured_is_a_refusal():
    subject = api(formal=None)
    with pytest.raises(UnsupportedEvidence, match="not enabled"):
        subject._formal_holds("check invariant <= 2: active(\"Root.A\");")


def test_a_solver_timeout_is_a_refusal_not_a_false():
    """A timeout means the run could not decide, not that the model is wrong.

    Reported as a timeout it went back for repair five times at ~25s each; as a
    False it would have published a defect nobody checked for.
    """

    subject = api(formal=Formal(raises=TimeoutError("solver wall clock")))
    with pytest.raises(UnsupportedEvidence, match="exceeded its budget"):
        subject._formal_holds("check invariant <= 2: active(\"Root.A\");")


def test_a_non_terminal_verdict_is_a_refusal_not_a_false():
    subject = api(formal=Formal(result=Row(status="unknown", holds=None)))
    with pytest.raises(UnsupportedEvidence, match="no terminal verdict"):
        subject._formal_holds("check invariant <= 2: active(\"Root.A\");")


@pytest.mark.parametrize("verdict", [True, False])
def test_a_terminal_verdict_is_returned_as_is(verdict):
    subject = api(formal=Formal(result=Row(status="ok", holds=verdict)))
    assert subject._formal_holds("check invariant <= 2: active(\"Root.A\");") is verdict


# --------------------------------------------------------------------------
# Combo-branch distinguishability, driven directly
# --------------------------------------------------------------------------


def test_one_target_is_distinguishable_by_definition():
    subject = api()
    assert subject._indistinguishable([Row(to_path="Root.A", transition_index=0)]) is False


def test_identical_targets_are_not_a_conflict():
    """Two rows reaching the same state are the same alternative, not a choice."""

    subject = api(relations=Relations(overlap=True))
    rows = [
        Row(to_path="Root.A", transition_index=0),
        Row(to_path="Root.A", transition_index=1),
    ]
    assert subject._indistinguishable(rows) is False


def test_overlapping_guards_to_different_targets_are_indistinguishable():
    subject = api(relations=Relations(overlap=True))
    rows = [
        Row(to_path="Root.A", transition_index=0),
        Row(to_path="Root.B", transition_index=1),
    ]
    assert subject._indistinguishable(rows) is True


def test_provably_disjoint_guards_are_distinguishable():
    subject = api(relations=Relations(overlap=False))
    rows = [
        Row(to_path="Root.A", transition_index=0),
        Row(to_path="Root.B", transition_index=1),
    ]
    assert subject._indistinguishable(rows) is False


def test_undecidable_guards_refuse_rather_than_pass():
    """The facade cannot prove two distinct non-empty guards are disjoint.

    Answering False -- "distinguishable" -- would let an overlap through as
    satisfied, which is the pair-0029 defect class.
    """

    subject = api(relations=Relations(overlap=UnsupportedEvidence("cannot decide")))
    rows = [
        Row(to_path="Root.A", transition_index=0),
        Row(to_path="Root.B", transition_index=1),
    ]
    with pytest.raises(UnsupportedEvidence):
        subject._indistinguishable(rows)


def test_no_combo_returns_none_so_the_ordinary_path_stays_in_charge():
    subject = api()
    assert subject._resolve_combo_branches([Row(to_path="Root.A")]) is None


def test_a_combo_target_expands_to_its_successors():
    successors = [
        Row(to_path="Root.A", transition_index=1),
        Row(to_path="Root.B", transition_index=2),
    ]
    subject = api(structure=Structure(transitions=successors))
    expanded = subject._resolve_combo_branches([Row(to_path="Root.__combo_x__abs_go_h1")])
    assert [r.to_path for r in expanded] == ["Root.A", "Root.B"]


# --------------------------------------------------------------------------
# `<undeclared>` against a broken or unusual declaration table
# --------------------------------------------------------------------------


def test_an_empty_variable_table_makes_the_absence_provable():
    subject = api(structure=Structure(variables=[]))
    with pytest.raises(UndeclaredTerm) as caught:
        subject._require_declared(variable="<undeclared>")
    assert caught.value.bindings == ("variable",)


def test_a_table_holding_only_route_control_counts_as_empty():
    """The effect facade drops these, so an evidence call can never reach one."""

    subject = api(
        structure=Structure(variables=[Row(name="R45RouteToken")]),
        source_exclusions=("compiler:route_control:R45RouteToken",),
    )
    with pytest.raises(UndeclaredTerm):
        subject._require_declared(variable="<undeclared>")


def test_a_populated_table_refuses_instead_of_proving_an_absence():
    subject = api(structure=Structure(variables=[Row(name="battery")]))
    with pytest.raises(UnsupportedEvidence) as caught:
        subject._require_declared(variable="<undeclared>")
    assert "1 declared variables" in str(caught.value)
    assert not isinstance(caught.value, UndeclaredTerm)


def test_an_expression_binding_can_never_prove_an_absence():
    subject = api(structure=Structure(variables=[]))
    with pytest.raises(UnsupportedEvidence) as caught:
        subject._require_declared(release="<undeclared>")
    assert "expressions, not declared elements" in str(caught.value)
    assert not isinstance(caught.value, UndeclaredTerm)


def test_a_mixed_binding_set_reports_both_reasons():
    subject = api(structure=Structure(variables=[Row(name="battery")]))
    with pytest.raises(UnsupportedEvidence) as caught:
        subject._require_declared(variable="<undeclared>", release="<undeclared>")
    message = str(caught.value)
    assert "1 declared variables" in message
    assert "expressions, not declared elements" in message


def test_no_undeclared_binding_is_a_no_op():
    subject = api(structure=Structure(variables=[]))
    assert subject._require_declared(variable="battery", state="Root.A") is None


# --------------------------------------------------------------------------
# Audit metadata must never change an outcome by failing
# --------------------------------------------------------------------------


def test_a_broken_variable_facade_is_not_swallowed():
    """Seeding is not audit metadata, so a broken facade must surface.

    The `except` guards elsewhere in this class exist because reference
    collection must never change a verdict.  Variable seeding is different: it
    feeds the simulation, so quietly substituting an empty seed would produce a
    plausible-looking answer from a broken environment.  Better that the
    assertion fails loudly and the controller records it.
    """

    subject = api(structure=Structure(boom={"variables"}))
    with pytest.raises(RuntimeError):
        subject._all_vars()


def test_a_variable_whose_initial_value_is_not_numeric_still_seeds():
    """Seeding is best-effort: an unparseable initial value becomes 0, not a crash."""

    subject = api(
        structure=Structure(
            variables=[
                Row(name="a", init_value="3"),
                Row(name="b", init_value="2.5"),
                Row(name="c", init_value="not a number"),
            ]
        )
    )
    seeded = subject._all_vars()
    assert seeded["a"] == 3
    assert seeded["b"] == 2.5
    assert seeded["c"] == 0


def test_a_broken_state_facade_leaves_the_default_init_unset():
    subject = api(structure=Structure(boom={"states"}))
    assert subject._default_init() is None


def test_a_model_with_no_leaf_states_has_no_default_init():
    subject = api(structure=Structure(states=[Row(path="Root", is_leaf=False)]))
    assert subject._default_init() is None


def test_the_pseudo_initial_is_never_a_hot_start():
    assert PredicateAPI._hot_startable("[*]") is None
    assert PredicateAPI._hot_startable("") is None
    assert PredicateAPI._hot_startable(None) is None
    assert PredicateAPI._hot_startable("Root.A") == "Root.A"


def test_the_undeclared_literal_is_never_recorded_as_a_model_reference():
    """It names nothing, so attributing a finding to it would be meaningless."""

    subject = api()
    subject.begin_call()
    subject._note("<undeclared>", "", None, "Root.A")
    assert subject.consume_refs() == ("Root.A",)
