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

from paper_stm_feedback_loop.assertions.exceptions import UnsupportedEvidence  # noqa: E402
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
# `<undeclared>` is refused uniformly (issue #170 §11.2)
# --------------------------------------------------------------------------
#
# Three earlier designs judged this literal per binding kind -- seal for
# `variable` and `trigger`, refuse for state-shaped ones, refuse for expressions
# -- which took three sets of judgement, three exemptions, a dedicated exception
# type and a dedicated seal path.  The third was measured to constrain nothing:
# 60 of 60 pairs have an empty author-owned variable table, so "the table is
# empty" carried no information and a seal resting on it fired for any pair at
# all.  One rule replaces all of it, and the obligation moves to a proposed name
# plus an existence precondition, which repair can act on.


@pytest.mark.parametrize(
    "bindings",
    [
        {"variable": "<undeclared>"},
        {"trigger": "<undeclared>"},
        {"state": "<undeclared>"},
        {"release": "<undeclared>"},
        {"condition": "<undeclared>"},
        {"variable": "<undeclared>", "release": "<undeclared>"},
    ],
)
def test_every_binding_kind_is_refused_alike(bindings):
    """The declaration table is not consulted, so its contents cannot matter."""

    for variables in ([], [Row(name="battery")], [Row(name="R45RouteToken")]):
        subject = api(structure=Structure(variables=variables))
        with pytest.raises(UnsupportedEvidence, match="placeholder, not a name"):
            subject._require_well_formed_names(**bindings)


def test_the_refusal_names_the_offending_bindings_and_the_fix():
    """A producer cannot act on "refused"; it can act on "do this instead"."""

    subject = api(structure=Structure(variables=[]))
    with pytest.raises(UnsupportedEvidence) as caught:
        subject._require_well_formed_names(variable="<undeclared>", release="<undeclared>")
    message = str(caught.value)
    # One binding per refusal: the message names the first offender it meets, and
    # a producer fixes them one at a time anyway.
    assert "'variable'" in message or "'release'" in message
    assert "precondition" in message


def test_no_undeclared_binding_is_a_no_op():
    subject = api(structure=Structure(variables=[]))
    assert subject._require_well_formed_names(variable="battery", state="Root.A") is None


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


def test_a_broken_transition_facade_leaves_the_default_init_unset():
    subject = api(structure=Structure(boom={"transitions"}))
    assert subject._default_init("Root.go") is None


def test_a_trigger_declared_nowhere_has_no_default_init():
    """`response_within` then runs unpinned, which is the honest reading.

    The default used to come from the state table -- the first declared leaf,
    whatever the trigger was -- so it named a source even for an event no
    transition carries.
    """

    subject = api(structure=Structure(transitions=[]))
    assert subject._default_init("Root.nosuchevent") is None


def test_the_pseudo_initial_is_never_a_hot_start():
    assert PredicateAPI._hot_startable("[*]") is None
    assert PredicateAPI._hot_startable("") is None
    assert PredicateAPI._hot_startable(None) is None
    assert PredicateAPI._hot_startable("Root.A") == "Root.A"


def test_a_placeholder_cannot_reach_the_reference_trail():
    """Because the predicate refuses it before doing any work.

    The trail used to filter `<undeclared>` by name.  That guarded against a
    value the shape check makes unreachable, and pinning it kept a special case
    alive for one literal while `<missing_var>` would have sailed past.  The
    guarantee worth testing is the one callers depend on: ask about a placeholder
    and you get a refusal, so there is no call whose refs could contain one.
    """

    subject = api()
    subject.begin_call()
    with pytest.raises(UnsupportedEvidence):
        subject.state_declared(state="<undeclared>", kind="leaf")
    assert subject.consume_refs() == ()
    subject.begin_call()
    with pytest.raises(UnsupportedEvidence):
        subject.variable_declared(variable="<missing_var>")
    assert subject.consume_refs() == ()


def test_empty_and_none_refs_are_dropped_from_the_trail():
    """Attribution needs names; a blank string points at nothing."""

    subject = api()
    subject.begin_call()
    subject._note("", None, "Root.A")
    assert subject.consume_refs() == ("Root.A",)


# --------------------------------------------------------------------------
# The prefix audit: which scripts the checker will even run
# --------------------------------------------------------------------------
#
# These branches decide whether an assertion is accepted at all.  A false
# rejection costs the item a repair round for something the producer did
# correctly; a false acceptance lets a script reach names the environment never
# froze, and every result derived from it is unattributable.  None of them had a
# test, which is why `checker.py` sat at 74% branch coverage while the rest of
# the layer was near-complete.


def _audit(source: str, *, allowed=("occupancy_after", "len")):
    import ast

    from paper_stm_feedback_loop.assertions.checker import _assigned_names, _audit_prefix_ast

    tree = ast.parse(source, mode="exec")
    local = _assigned_names(tree)
    return _audit_prefix_ast(tree, allowed_names=set(allowed) | local)


def _codes(report):
    return sorted(issue.code for issue in report.issues)


def test_a_clean_prefix_is_accepted():
    report = _audit("limit = 3\nrows = occupancy_after")
    assert report.ok, _codes(report)


def test_a_prefix_may_bind_and_then_use_its_own_name():
    """`_assigned_names` exists for this; without it every binding is unknown."""

    report = _audit("threshold = 2\ndoubled = threshold + threshold")
    assert report.ok, _codes(report)


def test_a_function_or_class_definition_in_the_prefix_is_a_bound_name():
    """Defined names must count as assigned, or the definition rejects itself."""

    report = _audit("def helper():\n    return 1\nvalue = helper")
    assert "unknown_name" not in _codes(report), _codes(report)


def test_an_assert_in_the_prefix_is_rejected():
    """Only the terminal assert carries the verdict.

    A second assert would decide the outcome before the evidence call the
    controller records, so the sealed result would not correspond to the claim.
    """

    assert "prefix_assert_forbidden" in _codes(_audit("assert True"))


def test_a_forbidden_ast_node_is_rejected():
    report = _audit("import os")
    assert "forbidden_ast_node" in _codes(report), _codes(report)


def test_a_dunder_attribute_is_rejected():
    report = _audit("leak = occupancy_after.__globals__")
    assert "dunder_attribute" in _codes(report), _codes(report)


def test_a_dunder_call_is_rejected():
    report = _audit("leak = occupancy_after.__reduce__()")
    assert "dunder_call" in _codes(report), _codes(report)


def test_a_forbidden_name_is_rejected():
    from paper_stm_feedback_loop.assertions.provenance import FORBIDDEN_NAMES

    name = sorted(FORBIDDEN_NAMES)[0]
    report = _audit(f"leak = {name}")
    assert "forbidden_name" in _codes(report), _codes(report)


def test_a_forbidden_call_is_rejected():
    from paper_stm_feedback_loop.assertions.provenance import FORBIDDEN_NAMES

    name = sorted(FORBIDDEN_NAMES)[0]
    report = _audit(f"leak = {name}()")
    assert "forbidden_call" in _codes(report), _codes(report)


def test_an_unknown_name_is_rejected():
    """A name the environment never froze cannot be evidence.

    The controller has a dedicated repair branch for this, keyed on the code, so
    it has to be reported as `unknown_name` and not folded into something else.
    """

    assert "unknown_name" in _codes(_audit("value = mystery_helper"))


def test_an_unknown_call_is_rejected():
    assert "unknown_call" in _codes(_audit("value = mystery_helper()"))


def test_a_method_call_on_a_bound_view_is_allowed():
    """Views are frozen and their non-dunder methods are the intended surface."""

    report = _audit("rows = occupancy_after\nfirst = rows.count()")
    assert "dunder_call" not in _codes(report), _codes(report)


def test_an_unusable_required_family_is_rejected_before_anything_runs():
    """A misspelled family is a contract error, not a model finding."""

    result = _checker_for_audit().check(
        'assert state_declared(state="Root.Idle", kind="any") is True, '
        '"[REQ-001][AST-REQ-001-1] x"',
        reason="bad family",
        required_function_families=("not_a_family",),
    )
    assert result.sealed.outcome == "invalid"
    assert result.sealed.error["type"] == "InvalidFunctionFamily"


def _checker_for_audit():
    from paper_stm_feedback_loop.assertions import build_eval_environment
    from paper_stm_feedback_loop.assertions.checker import AssertionChecker

    return AssertionChecker(
        environment=build_eval_environment(
            model_text="state Root {\n    event go;\n    state Idle;\n    [*] -> Idle;\n}\n",
            source_mappings=[],
            source_exclusions=[],
            timeout_seconds=30,
            fbmcq_solver_timeout_ms=15_000,
            fbmcq_max_bound=4,
            fbmcq_process_wall_seconds=20.0,
        )
    )


# --------------------------------------------------------------------------
# The namespace snapshot feeds the before/after hash the seal rests on
# --------------------------------------------------------------------------


def test_the_namespace_snapshot_serialises_every_value_kind():
    """A value it cannot serialise would break the hash the sealed result cites.

    The hash is what proves the script did not mutate the frozen namespace, so
    an unserialisable local must degrade to a repr rather than raising.
    """

    from paper_stm_feedback_loop.assertions.checker import _namespace_snapshot

    class Opaque:
        def __repr__(self):
            return "<opaque>"

    snapshot = _namespace_snapshot(
        {
            "__hidden": "skipped",
            "a_function": lambda: None,
            "text": "s",
            "number": 3,
            "real": 1.5,
            "flag": True,
            "nothing": None,
            "listy": [1, 2],
            "tuply": (1,),
            "setty": {1},
            "dicty": {"k": "v"},
            "opaque": Opaque(),
        },
        {"a_function"},
    )
    assert "__hidden" not in snapshot, "dunder locals must not enter the hash"
    assert "a_function" not in snapshot, "registered functions are not namespace state"
    assert snapshot["text"] == "s" and snapshot["number"] == 3
    assert snapshot["flag"] is True and snapshot["nothing"] is None
    assert snapshot["listy"] == "[1, 2]" and snapshot["dicty"] == "{'k': 'v'}"
    assert snapshot["opaque"] == "<opaque>"


# --------------------------------------------------------------------------
# Rows and views that are shaped wrongly must be skipped, not crash
# --------------------------------------------------------------------------
#
# The facades come from an external tool (pyfcstm) across a version boundary.  A
# field that goes missing or changes type in an upgrade must degrade a predicate
# to "cannot answer", never to a wrong bool and never to an exception type the
# controller cannot dispatch on.  These are the guards that make that true.


def test_a_non_string_unconsumed_event_is_skipped():
    subject = api(structure=Structure(transitions=[]))
    subject.begin_call()
    subject._note_simulation(
        View(cycles=[Cycle(fired_transitions=(), unconsumed_events=(None, 7, "", "Root.go"))])
    )
    assert subject.consume_refs() == ("Root.go",)


def test_a_variable_row_without_a_usable_name_is_skipped():
    subject = api(
        structure=Structure(
            variables=[Row(name=None, init_value="1"), Row(init_value="2"), Row(name="ok", init_value="4")]
        )
    )
    assert subject._all_vars() == {"ok": 4}


def test_a_transition_row_without_an_integer_index_contributes_no_anchor():
    """The anchor is `transition:<index>`; a non-int index cannot form one."""

    subject = api(
        structure=Structure(transitions=[Row(to_path="Root.B", transition_index="tr_1")])
    )
    subject.begin_call()
    subject._note_transitions(source="Root.A")
    assert not any(r.startswith("transition:") for r in subject.consume_refs())


def test_a_non_string_consumed_event_does_not_count_as_consumed():
    """`stays_in` and friends verify consumption; a malformed entry must not pass."""

    subject = api()
    consumed = subject._consumed(
        View(cycles=[Cycle(consumed_events=(None, 3, "Root.go"))])
    )
    assert consumed == {"Root.go"}


def test_state_declared_answers_for_a_pseudo_state():
    """The `pseudo` kind had no test, so the branch was never exercised.

    A model's initial and final markers are declared states of a distinct kind,
    and a requirement can legitimately ask about one.
    """

    subject = api(
        structure=Structure(
            states=[Row(path="Root.Init", is_leaf=True, is_pseudo=True, is_composite=False)]
        )
    )
    assert subject.state_declared(state="Root.Init", kind="pseudo") is True
    assert subject.state_declared(state="Root.Init", kind="leaf") is False
    assert subject.state_declared(state="Root.Init", kind="composite") is False
    assert subject.state_declared(state="Root.Init", kind="any") is True


def test_state_declared_answers_for_a_composite():
    subject = api(
        structure=Structure(
            states=[Row(path="Root.Outer", is_leaf=False, is_pseudo=False, is_composite=True)]
        )
    )
    assert subject.state_declared(state="Root.Outer", kind="composite") is True
    assert subject.state_declared(state="Root.Outer", kind="leaf") is False


def test_a_witness_without_a_mapping_interface_yields_no_refs():
    """A solver whose counterexample shape changed must not break attribution."""

    from paper_stm_feedback_loop.assertions.predicate_api import _witness_refs

    assert _witness_refs(object()) == []
    assert _witness_refs("not a mapping") == []


def test_a_witness_step_with_a_malformed_event_is_skipped():
    from paper_stm_feedback_loop.assertions.predicate_api import _witness_refs

    witness = {"steps": [{"consumed_events": (None, 5, "", "Root.go")}]}
    assert "Root.go" in _witness_refs(witness)
    assert None not in _witness_refs(witness)


def test_reading_a_variable_from_nothing_is_none_not_zero():
    """`None` means "not observed"; 0 would be a value the run never saw.

    `variable_delta_after` subtracts these, so conflating the two would report a
    delta of zero -- "the variable did not change" -- for a variable the trace
    never reported at all.
    """

    from paper_stm_feedback_loop.assertions.predicate_api import _read_var

    assert _read_var(None, "units") is None


def test_duplicate_targets_among_three_branches_are_skipped_not_compared():
    """Two rows to the same state are one alternative; only the third is a choice.

    With just the two duplicates the count short-circuits before the comparison,
    so the skip only becomes reachable once a genuinely different target is also
    present -- which is the shape a combo lowering with a repeated branch has.
    """

    subject = api(relations=Relations(overlap=False))
    rows = [
        Row(to_path="Root.A", transition_index=0),
        Row(to_path="Root.A", transition_index=1),
        Row(to_path="Root.B", transition_index=2),
    ]
    assert subject._indistinguishable(rows) is False
    # And when the guards do overlap, the distinct pair is still found.
    overlapping = api(relations=Relations(overlap=True))
    assert overlapping._indistinguishable(rows) is True


def test_a_trace_with_no_cycles_refuses_rather_than_answering():
    """An empty trace observed nothing, so there is no delta either way.

    This used to answer `False` -- the consumption check came first and returned
    early.  That reads as "the quantity did not decrease", which is a claim about a
    quantity the run never saw.  Observability is now checked first, so an
    unobservable variable refuses regardless of what the trigger did.
    """

    class Simulation:
        @staticmethod
        def simulate(**_kwargs):
            return View(cycles=[])

    subject = api(
        structure=Structure(
            variables=[Row(name="units", init_value="5")],
            events=[Row(qualified_name="Root.go")],
            transitions=[Row(to_path="Root.B", transition_index=0)],
        ),
        simulation=Simulation(),
    )
    with pytest.raises(UnsupportedEvidence, match="not observable"):
        subject.variable_delta_after(
            source="Root.A", trigger="Root.go", variable="units", sign="negative"
        )


def test_a_frozen_view_in_the_namespace_is_serialised_structurally():
    """Views carry model facts, so the hash must cover their content, not their id."""

    from paper_stm_feedback_loop.assertions.checker import _namespace_snapshot
    from paper_stm_feedback_loop.assertions.views import FrozenView

    view = FrozenView("state", {"path": "Root.Idle"}, allowed_fields=("path",))
    snapshot = _namespace_snapshot({"row": view}, set())
    assert snapshot["row"] == view.to_json()
    assert "object at 0x" not in str(snapshot["row"]), "a repr would not pin the content"


def test_a_non_dunder_method_call_in_the_prefix_is_recorded_and_allowed():
    """Frozen views expose ordinary methods; the audit must let them through."""

    report = _audit("rows = occupancy_after\nfirst = rows.count()")
    assert report.ok, _codes(report)


def test_a_call_through_a_subscript_is_recorded_without_a_name():
    """`fns[0]()` has neither a Name nor an Attribute as its callee.

    The audit still has to walk past it rather than assume one of the two
    shapes; a producer that indexes a list of predicates is unusual but legal
    Python, and an unhandled shape in the gate that decides whether scripts run
    at all would be an unhandled exception rather than a finding.
    """

    report = _audit("fns = [occupancy_after]\nfirst = fns[0]()")
    assert "dunder_call" not in _codes(report), _codes(report)
    assert "forbidden_call" not in _codes(report), _codes(report)


# --------------------------------------------------------------------------
# `_initial_child_of` on shapes a real model does not produce
# --------------------------------------------------------------------------


def test_initial_targets_given_as_plain_dicts_are_read():
    """The facade wraps rows in `FrozenView`, but the reader must not assume it.

    The first version filtered on `isinstance(t, dict)` and therefore matched
    nothing, so every call returned `None` -- which reads as "the initial child is
    not the one claimed" rather than "this code could not look".  Accepting both
    shapes is what fixed it; this covers the dict branch that no live facade hits.
    """

    subject = api(
        structure=Structure(
            states=[
                Row(
                    path="Root.Mode",
                    initial_targets=[
                        {"target": "Root.Mode.A", "is_unconditional": True, "guard": None}
                    ],
                )
            ]
        )
    )
    assert subject._initial_child_of("Root.Mode") == "Root.Mode.A"


def test_initial_targets_present_but_carrying_no_target_yields_none():
    """A row shape change upstream must not be read as a wrong initial child."""

    subject = api(
        structure=Structure(
            states=[Row(path="Root.Mode", initial_targets=[{"guard": "x > 0"}])]
        )
    )
    assert subject._initial_child_of("Root.Mode") is None


def test_only_guarded_entries_is_refused_not_answered():
    """Every entry conditional means there is no entry taken without a guard.

    Distinct from the converter shape this fix was written for, where exactly one
    unconditional edge exists.  With none, the question has no answer from the
    declarations, so refusing is the honest outcome -- answering would pick one
    guarded re-entry point arbitrarily.
    """

    subject = api(
        structure=Structure(
            states=[
                Row(
                    path="Root.Mode",
                    initial_targets=[
                        {"target": "Root.Mode.A", "is_unconditional": False, "guard": "t == 1"},
                        {"target": "Root.Mode.B", "is_unconditional": False, "guard": "t == 2"},
                    ],
                )
            ]
        )
    )
    with pytest.raises(UnsupportedEvidence, match="none is"):
        subject._initial_child_of("Root.Mode")


def test_a_prefix_runs_under_the_alarm_when_one_is_configured():
    """The timed path through `_exec_prefix`, which no other test reaches.

    Every other script in the suite has an empty prefix, so the branch that arms
    `SIGALRM` before executing it was never taken -- and that branch is what keeps a
    runaway prefix from hanging a cell indefinitely.
    """

    from paper_stm_feedback_loop.assertions import build_eval_environment
    from paper_stm_feedback_loop.assertions.checker import AssertionChecker

    checker = AssertionChecker(
        environment=build_eval_environment(
            model_text="state Root {\n    event go;\n    state Idle;\n    [*] -> Idle;\n}\n",
            source_mappings=[],
            source_exclusions=[],
            timeout_seconds=30,
            fbmcq_solver_timeout_ms=10_000,
            fbmcq_max_bound=3,
            fbmcq_process_wall_seconds=15.0,
        )
    )
    script = (
        "wanted = 1\n"
        'assert len([state_declared(state="Root.Idle", kind="any")]) == wanted, '
        '"[REQ-001][AST-REQ-001-1] m"'
    )
    result = checker.check(script, reason="prefix", required_function_families=())
    assert result.sealed.outcome == "valid", result.sealed.metadata
