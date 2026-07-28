"""The script-level reference gate: which absent names are legal, and why.

Two rules have to hold together, and pair 0006 is the proof that deciding them
in separate places does not work.

The first rule is old: a binding naming an element the frozen model does not
declare makes its query vacuous -- nothing matches, so the check passes and hides
the defect it was written to catch.  The second rule is what the precondition
design needs: a `precondition` proposes the name of an element the model *should*
have declared, so that name is absent by construction, and so is the same name in
the claim that depends on it.

Enforced separately, they contradict.  Pair 0006 spent six revisions alternating
between the two refusals -- propose a name, rejected as unresolved; fall back to a
stand-in, rejected as not a name -- until the repair budget ran out and both
models' runs died at `convert_assertions`.  So the gate decides both at once, and
the exemption is conditional on the dependency being declared: unlinked, the
claim still runs, still matches nothing, and still passes.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover.capability import (  # noqa: E402
    placeholder_bindings,
    unresolved_model_references,
    unresolved_reference_findings,
)
from paper_stm_feedback_loop.discover.dependencies import (  # noqa: E402
    dependency_closure,
)

#: What the frozen model declares.  Deliberately small: the interesting axis is
#: which names are absent, not how many are present.
KNOWN = frozenset({"Sys.ModeA", "Sys.ModeB", "Sys.done", "units"})

EXISTS = 'variable_declared(variable="uav_count") is True'
DELTA = (
    'variable_delta_after(source="Sys.ModeA", trigger="Sys.done", '
    'variable="uav_count", sign="negative") is True'
)


class A:
    """A stand-in carrying only the fields the gate reads."""

    def __init__(self, aid, expression, rid="REQ-001", role="primary", depends_on=()):
        self.assertion_id = aid
        self.requirement_id = rid
        self.role = role
        self.expression = expression
        self.depends_on = tuple(depends_on)


# --------------------------------------------------------------------------
# The shape the design sanctions


def test_a_precondition_may_propose_a_name_the_model_does_not_declare():
    """Refusing this is refusing the mechanism itself.

    `variable_declared(variable="uav_count")` on a model with no such variable is
    not a mistake to be corrected -- it is the question, and its answer is the
    finding.
    """

    script = (A("A0", EXISTS, role="precondition"), A("A1", DELTA, depends_on=("A0",)))
    assert unresolved_reference_findings(script, KNOWN) == ()


def test_the_exemption_reaches_through_a_chain_of_prerequisites():
    """One hop is not enough.

    An existence check can rest on another -- the variable exists *and* the state
    that owns it exists -- and reading only direct `depends_on` would refuse the
    claim at the end of the chain.
    """

    script = (
        A("A0", 'state_declared(state="Sys.Missing", kind="any") is True',
          role="precondition"),
        A("A1", EXISTS, role="precondition", depends_on=("A0",)),
        A("A2", DELTA, depends_on=("A1",)),
    )
    assert unresolved_reference_findings(script, KNOWN) == ()


def test_two_requirements_may_propose_the_same_name_independently():
    """The exemption is per dependency, not per name.

    Otherwise one requirement's precondition would silently license another
    requirement's unlinked binding of the same name.
    """

    script = (
        A("A0", EXISTS, rid="REQ-001", role="precondition"),
        A("A1", DELTA, rid="REQ-001", depends_on=("A0",)),
        A("B0", EXISTS, rid="REQ-002", role="precondition"),
        A("B1", DELTA, rid="REQ-002", depends_on=("B0",)),
    )
    assert unresolved_reference_findings(script, KNOWN) == ()


# --------------------------------------------------------------------------
# What the gate must still refuse


def test_an_unlinked_claim_on_a_proposed_name_is_still_refused():
    """This is the vacuous pass the gate exists to stop.

    The precondition is present, so the name is "proposed" somewhere in the
    requirement -- but without `depends_on` the claim runs anyway on a model that
    has no such variable, and a query over a nonexistent element matches nothing
    and passes.
    """

    script = (A("A0", EXISTS, role="precondition"), A("A1", DELTA))
    findings = unresolved_reference_findings(script, KNOWN)
    assert len(findings) == 1
    assert "REQ-001/A1" in findings[0]
    assert "uav_count" in findings[0]


def test_a_name_nobody_proposed_is_refused():
    """A typo and a proposal are indistinguishable without the precondition.

    Which is the point of requiring one: the producer has to say that it means
    "this element should exist and does not", rather than leaving a name that
    reads like a path from the vocabulary.
    """

    script = (A("A1", DELTA),)
    findings = unresolved_reference_findings(script, KNOWN)
    assert len(findings) == 1
    assert "uav_count" in findings[0]


def test_depending_on_a_precondition_does_not_license_an_unrelated_name():
    """The exemption covers the proposed name, not the assertion.

    A claim may legitimately need one proposed element and still misname another;
    exempting the whole assertion would let the second through.
    """

    script = (
        A("A0", EXISTS, role="precondition"),
        A(
            "A1",
            'variable_delta_after(source="Sys.Typo", trigger="Sys.done", '
            'variable="uav_count", sign="negative") is True',
            depends_on=("A0",),
        ),
    )
    findings = unresolved_reference_findings(script, KNOWN)
    assert len(findings) == 1
    assert "Sys.Typo" in findings[0]
    assert "uav_count" not in findings[0]


def test_a_declared_only_script_produces_nothing():
    """The gate must be silent on the ordinary case."""

    script = (
        A(
            "A1",
            'occupancy_after(source="Sys.ModeA", trigger="Sys.done", '
            'target="Sys.ModeB") is True',
        ),
    )
    assert unresolved_reference_findings(script, KNOWN) == ()


# --------------------------------------------------------------------------
# Placeholders, and the bindings the scan can read


def test_a_placeholder_binding_is_reported_by_shape_not_by_a_word_list():
    """So `<missing_var>` is caught as surely as any other.

    A gate keyed on one literal would refuse the token it had been told about and
    pass every variant, and the variant reaches the runtime instead -- later, and
    with a message about identifier shape rather than about what to do.
    """

    assert placeholder_bindings('state_declared(state="<undeclared>", kind="leaf")') == (
        'state=\'<undeclared>\'',
    )
    assert placeholder_bindings('variable_declared(variable="<missing_var>")') == (
        "variable='<missing_var>'",
    )
    assert placeholder_bindings(EXISTS) == ()
    # A path template is not a binding: the angle brackets are inside prose the
    # scan never sees, and a real dotted path must not be flagged.
    assert placeholder_bindings('event_declared(event="Sys.done")') == ()


def test_a_non_literal_binding_is_skipped_rather_than_guessed():
    """Its value is not knowable statically, so no claim is made about it.

    The runtime shape check still refuses whatever it evaluates to; inventing a
    finding here would report a defect from a string this gate cannot read.
    """

    assert unresolved_model_references(
        'variable_declared(variable=some_name)', KNOWN
    ) == ()
    assert placeholder_bindings("variable_declared(variable=some_name)") == ()


def test_an_unparsable_expression_yields_no_findings():
    """The syntax gate owns that failure and reports it precisely."""

    assert unresolved_model_references("variable_declared(variable=", KNOWN) == ()
    assert placeholder_bindings("variable_declared(variable=") == ()


def test_no_known_paths_means_no_conclusion():
    """An empty vocabulary cannot establish that a name is absent.

    Every name would be "unresolved", so the gate would reject every script for a
    frozen-input problem that is not the producer's to fix.
    """

    assert unresolved_model_references(DELTA, frozenset()) == ()


# --------------------------------------------------------------------------
# The closure the gate reads


def test_the_closure_ignores_a_dangling_reference():
    """Its own gate reports it, with a message about the rewrite that dropped it.

    Following it here would raise `KeyError` from inside the reference gate, which
    names neither the missing assertion nor the dependency that still points at
    it.
    """

    script = (A("A1", DELTA, depends_on=("A0", "GONE")),
              A("A0", EXISTS, role="precondition"))
    assert dependency_closure(script) == {"A1": frozenset({"A0"}), "A0": frozenset()}
    # And the gate still exempts the name the surviving precondition proposes.
    assert unresolved_reference_findings(script, KNOWN) == ()


# --------------------------------------------------------------------------
# The keyword gate that has to run before the reference gates


def test_an_unaccepted_keyword_is_named_with_the_bindings_that_are_accepted():
    """Because the reference gates cannot see a value bound under a keyword they
    do not know, and then blame the wrong assertion.

    Replayed from the real pair-0006 script: its precondition proposed
    `uav_count` under a `name=` keyword, so the proposed name was invisible, the
    exemption never applied, and the gate reported the *dependent* assertion as
    holding an unresolved reference.  The producer was told to fix a correct name
    in a correct assertion while the typo sat one line above.
    """

    from paper_stm_feedback_loop.discover.predicates import (
        accepted_bindings,
        misspelled_binding_findings,
    )

    findings = misspelled_binding_findings('variable_declared(name="uav_count") is True')
    assert len(findings) == 1
    assert "does not accept ['name']" in findings[0]
    assert "['variable']" in findings[0], "the right spelling has to be in the message"

    assert misspelled_binding_findings(EXISTS) == ()
    # An optional binding is accepted even though it is not a required one.
    assert accepted_bindings("response_within") >= {"trigger", "response", "bound", "source"}
    assert misspelled_binding_findings(
        'response_within(trigger="Sys.evt", response="Sys.ModeB", bound=3, '
        'source="Sys.ModeA") is True'
    ) == ()
    # Builtins and unknown callables are not this gate's business.
    assert misspelled_binding_findings("all([len(x) > 0])") == ()
    assert misspelled_binding_findings("state_declared(") == ()


def test_an_existence_check_needs_no_precondition_of_its_own():
    """Its False *is* the existence answer, so it cannot be a vacuous pass.

    The exemption used to be keyed on `role == "precondition"`, which forced a
    requirement whose own predicate is an existence check into a precondition plus
    a byte-identical dependent.  Pair 0006 wrote exactly that, a reviewer objected
    to the duplication, the producer deleted one of the pair, and the survivor lost
    its exemption -- rejected on the last of its repair rounds, run dead.  Keying
    on the predicate instead is both sounder and simpler: what makes an absent name
    legitimate is that something is asking whether it exists.
    """

    script = (A("A1", EXISTS),)
    assert unresolved_reference_findings(script, KNOWN) == ()
    # And a claim that merely *uses* the name still needs the check to exist and
    # to be depended on, so the vacuous-pass protection is untouched.
    assert unresolved_reference_findings((A("A1", DELTA),), KNOWN) != ()
    assert unresolved_reference_findings(
        (A("A0", EXISTS, role="precondition"), A("A1", DELTA)), KNOWN
    ) != ()
    # A check about a *different* absent name exempts nothing.
    assert unresolved_reference_findings(
        (
            A("A0", 'variable_declared(variable="other_name") is True', role="precondition"),
            A("A1", DELTA, depends_on=("A0",)),
        ),
        KNOWN,
    ) != ()
