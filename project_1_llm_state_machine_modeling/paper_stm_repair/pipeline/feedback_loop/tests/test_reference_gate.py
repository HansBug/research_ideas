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


# --------------------------------------------------------------------------
# Steps 1 and 2 of the four-step procedure, as gates


class Req:
    """A requirement carrying only what the two step gates read."""

    def __init__(self, rid, predicate, bindings, limitations=()):
        self.requirement_id = rid
        self.predicate = predicate
        self.predicate_bindings = bindings
        self.limitations = tuple(limitations)


GATE_KNOWN = frozenset({"Sys.ModeA", "Sys.ModeA.Inner", "Sys.RegionA.Done", "Sys.go"})


def test_termination_gate_reads_the_model_not_the_wording():
    """Firing on words like "final" would hit requirements about other things.

    The gate fires exactly when the model ends the run from that source on that
    trigger -- which is exactly when `terminates` can answer the claim -- so a
    sentence that merely says "finally" is untouched, and a sentence about
    termination on a model that does *not* terminate there is left alone too, since
    then the absence is the finding.
    """

    from paper_stm_feedback_loop.discover.capability import (
        termination_proposal_findings,
    )

    ends = ({"source": "Sys.ModeA", "trigger": "Sys.go", "ends_run": True},)
    proposal = Req(
        "REQ-001",
        "occupancy_after",
        {"source": "Sys.ModeA", "trigger": "Sys.go", "target": "Sys.TheEnd"},
    )
    fired = termination_proposal_findings((proposal,), GATE_KNOWN, ends)
    assert len(fired) == 1
    assert "terminates(scope='Sys.ModeA', trigger='Sys.go')" in fired[0]

    # Written per step 1, it passes.
    assert termination_proposal_findings(
        (Req("REQ-001", "terminates", {"scope": "Sys.ModeA", "trigger": "Sys.go"}),),
        GATE_KNOWN,
        ends,
    ) == ()
    # A declared target is not a proposal, so the gate has nothing to say.
    assert termination_proposal_findings(
        (
            Req(
                "REQ-002",
                "occupancy_after",
                {"source": "Sys.ModeA", "trigger": "Sys.go", "target": "Sys.ModeA.Inner"},
            ),
        ),
        GATE_KNOWN,
        ends,
    ) == ()
    # No terminating edge at all: the proposal may well be the finding.
    assert termination_proposal_findings((proposal,), GATE_KNOWN, ()) == ()
    # Terminating, but not on this trigger.
    assert termination_proposal_findings(
        (
            Req(
                "REQ-003",
                "occupancy_after",
                {"source": "Sys.ModeA", "trigger": "Sys.other", "target": "Sys.TheEnd"},
            ),
        ),
        GATE_KNOWN,
        ends,
    ) == ()


def test_the_termination_gate_follows_the_two_step_lowering():
    """Because that is how the corpus writes it, and reading one hop missed half.

    Pair 0050 ends the run from its autonomous mode by leaving the composite on the
    event and terminating on the token that exit set.  Reading only the direct edge
    caught its first fabricated terminal state and let the second through -- the
    same defect published twice, one of them invisible to the gate.
    """

    from paper_stm_feedback_loop.discover.capability import (
        termination_proposal_findings,
    )

    # The shape `_pseudo_state_facts` emits for a two-edge termination: the inner
    # exit is marked because its token reaches a run-ending edge, and the composite
    # carries a row for the same trigger so a mode-level claim can match.
    chain = (
        {"source": "Sys.ModeA.Inner", "trigger": "Sys.go", "ends_run": True,
         "via_token": "tok==9"},
        {"source": "Sys.ModeA", "trigger": "Sys.go", "ends_run": True,
         "via_token": "tok==9"},
        {"source": "Sys.ModeA", "trigger": None, "ends_run": True},
    )
    fired = termination_proposal_findings(
        (
            Req(
                "REQ-004",
                "occupancy_after",
                {"source": "Sys.ModeA", "trigger": "Sys.go", "target": "Sys.TheEnd"},
            ),
        ),
        GATE_KNOWN,
        chain,
    )
    assert len(fired) == 1
    # The chain must actually leave the named scope, not merely exist somewhere.
    assert termination_proposal_findings(
        (
            Req(
                "REQ-005",
                "occupancy_after",
                {"source": "Sys.Elsewhere", "trigger": "Sys.go", "target": "Sys.TheEnd"},
            ),
        ),
        GATE_KNOWN,
        chain,
    ) == ()
    # A source with no trigger falls back to "this source ends the run".
    assert len(
        termination_proposal_findings(
            (Req("REQ-006", "reaches", {"source": "Sys.ModeA", "target": "Sys.TheEnd"}),),
            GATE_KNOWN,
            chain,
        )
    ) == 1


def test_the_declared_elsewhere_gate_compares_leaf_names():
    """A shared state lives in one region; a sentence about the other means it.

    Whole-path comparison cannot see that, which is how a requirement proposed a
    `Done` under the region it was talking about while the vocabulary declared the
    one `Done` under the sibling -- a missing state reported as missing while
    present.
    """

    from paper_stm_feedback_loop.discover.capability import (
        redundant_proposal_findings,
    )

    fired = redundant_proposal_findings(
        (Req("REQ-001", "occupancy_after", {"target": "Sys.RegionB.Done"}),), GATE_KNOWN
    )
    assert len(fired) == 1
    assert "Sys.RegionA.Done" in fired[0]

    # A declared path, and a genuinely new leaf, are both none of its business.
    assert redundant_proposal_findings(
        (Req("REQ-002", "occupancy_after", {"target": "Sys.RegionA.Done"}),), GATE_KNOWN
    ) == ()
    assert redundant_proposal_findings(
        (Req("REQ-003", "variable_delta_after", {"variable": "unit_count"}),), GATE_KNOWN
    ) == ()
    # `[*]` and empty values are not proposals.
    assert redundant_proposal_findings(
        (Req("REQ-004", "occupancy_after", {"source": "[*]", "target": ""}),), GATE_KNOWN
    ) == ()


def test_the_declared_elsewhere_gate_has_an_exit_the_reviewer_judges():
    """Because the comparison cannot tell *shared* from *wanted per scope*.

    One `FinishState` reached from both modes is shared, and refusing a proposal
    for it is right.  "Each region shall have its own Idle" on a model declaring
    only `RegionA.Idle` is not, and there the refusal has no legal answer: bind the
    declared path and the requirement says something else, keep the proposal and
    the gate fires again -- five rounds, then the run dies.  That is the shape that
    killed pair 0006 twice.

    So the exit costs a sentence rather than nothing: the producer must state that
    the sentence demands a scope-local instance, which the Requirement Reviewer
    then judges as the step-3-versus-step-4 call it already owns.
    """

    from paper_stm_feedback_loop.discover.capability import (
        SCOPE_LOCAL_WAIVER,
        redundant_proposal_findings,
    )

    proposal = {"target": "Sys.RegionB.Done"}
    assert len(redundant_proposal_findings((Req("R1", "occupancy_after", proposal),), GATE_KNOWN)) == 1
    # The message has to name the exit, or the producer cannot find it.
    assert SCOPE_LOCAL_WAIVER in redundant_proposal_findings(
        (Req("R1", "occupancy_after", proposal),), GATE_KNOWN
    )[0]
    # Stated, the proposal survives to the Reviewer.
    assert redundant_proposal_findings(
        (
            Req(
                "R2",
                "occupancy_after",
                proposal,
                # Opens with the phrase: a waiver has to be the entry's subject,
                # not a clause buried in one, or a limitation that *denies* the need
                # reads as a waiver.
                limitations=(
                    f"{SCOPE_LOCAL_WAIVER}: NL-L009 wants a per-region completion "
                    "state, not the shared Sys.RegionA.Done",
                ),
            ),
        ),
        GATE_KNOWN,
    ) == ()
    # An unrelated limitation is not an exit: the waiver has to be said.
    assert len(
        redundant_proposal_findings(
            (Req("R3", "occupancy_after", proposal, limitations=("checked to bound 4 only",)),),
            GATE_KNOWN,
        )
    ) == 1


def test_the_termination_chain_ignores_an_unnamed_scope_or_trigger():
    """The chain walk is what catches a composite that terminates via the lowering.

    It is reached only from bindings that may be absent -- a requirement can omit
    `source` and `trigger` both -- so the guard has to hold, or the chain check
    starts matching every exit edge in the model against an empty scope.
    """

    from paper_stm_feedback_loop.discover.capability import (
        termination_proposal_findings,
    )

    chain = (
        {"source": "Sys.ModeA.Inner", "trigger": "Sys.go", "ends_run": False},
        {"source": "Sys.ModeA", "trigger": None, "ends_run": True},
    )
    # No source at all: nothing to key the chain on, so no finding.
    assert termination_proposal_findings(
        (Req("R1", "occupancy_after", {"trigger": "Sys.go", "target": "Sys.TheEnd"}),),
        GATE_KNOWN,
        chain,
    ) == ()
    # Source but no trigger still resolves through the direct-source fallback.
    assert len(
        termination_proposal_findings(
            (Req("R2", "reaches", {"source": "Sys.ModeA", "target": "Sys.TheEnd"}),),
            GATE_KNOWN,
            chain,
        )
    ) == 1


def test_the_waiver_must_open_the_limitation_not_merely_appear_in_it():
    """Because a limitation that denies the need was switching the gate off.

    As a free substring, "no scope-local instance required, this is the shared
    state" waived it -- the producer said the opposite of the waiver and got the
    waiver. Unlikely in fresh prose; likely once a producer has read the phrase in a
    refusal message and is arguing with it.
    """

    from paper_stm_feedback_loop.discover.capability import (
        SCOPE_LOCAL_WAIVER,
        redundant_proposal_findings,
    )

    proposal = {"target": "Sys.RegionB.Done"}

    def fires(*limitations):
        return bool(
            redundant_proposal_findings(
                (Req("R", "occupancy_after", proposal, limitations=limitations),),
                GATE_KNOWN,
                {"states": tuple(GATE_KNOWN)},
            )
        )

    assert fires()
    assert not fires(f"{SCOPE_LOCAL_WAIVER}: NL-L009 wants one per region")
    # Case and surrounding whitespace are not the point; leading negation is.
    assert not fires(f"  {SCOPE_LOCAL_WAIVER.upper()} -- per NL-L009  ")
    assert fires(f"no {SCOPE_LOCAL_WAIVER}, this is the shared state")
    assert fires("checked up to bound 4 only")


def test_the_declared_and_existence_readers_answer_on_real_bindings():
    """Both feed decisions elsewhere, so their empty case is not the whole story.

    `declared_path_bindings` is what a `precondition` inherits its attribution
    anchor from -- if it never reported a declared name, a proposed-name finding
    would stay unattributable and never become a confirmed issue.
    `_existence_checked_names` is what makes an absent name legal at all.
    """

    from paper_stm_feedback_loop.discover.capability import (
        _existence_checked_names,
        declared_path_bindings,
    )

    # Declared names are reported; absent ones are not this reader's business.
    assert declared_path_bindings(DELTA, KNOWN) == ("Sys.ModeA", "Sys.done")
    assert declared_path_bindings(EXISTS, KNOWN) == ()
    assert declared_path_bindings("not python at all (", KNOWN) == ()

    # An existence predicate's absent name is reported; a declared one is not, and
    # neither is an absent name bound by a predicate that merely *uses* it.
    assert _existence_checked_names(EXISTS, KNOWN) == ("uav_count",)
    assert _existence_checked_names('variable_declared(variable="units")', KNOWN) == ()
    assert _existence_checked_names(DELTA, KNOWN) == ()
    assert _existence_checked_names('state_declared(state="[*]", kind="leaf")', KNOWN) == ()
    # A binding whose value is not a literal cannot be read statically, and the
    # runtime shape check refuses whatever it evaluates to -- so this reader says
    # nothing about it rather than guessing a name.
    assert _existence_checked_names("variable_declared(variable=some_name)", KNOWN) == ()


def test_containment_and_initial_target_get_no_waiver_because_their_false_is_the_finding():
    """Proposing a scope-local name there says the same thing the worse way.

    "X shall be a substate of M" against a model declaring X at the root is answered
    by `containment(parent=M, child=<the declared X>)` coming back False -- the
    obligation is violated exactly because the declared state sits outside M.

    A proposal restates it in a form the finding cannot survive.  The proposed path
    needs a precondition `state_declared(M.X)`, which is False for exactly the reason
    the requirement is violated, so the dependent primary is `blocked` and never
    runs.  The finding is not lost outright -- a False `precondition` is published as
    an issue too (nodes.py, issue #170 §11.4) -- but the issue it produces is bound
    to the *proposed* path.  The hit criterion reads the requirement's
    `predicate_bindings` and, with no trigger to key on, needs every expected state
    matched, tolerating only one level of parent/child.  `M.X` is neither `X` nor one
    level from it, so the overlap comes to one where two are required.

    matrix-v16 shows both outcomes on one pair.  0029-gpt bound
    `{AutonomousMode, AutonomousMode.InitialState}` and scores a miss on a defect it
    did detect; 0029-claude bound the declared root path, got a direct False from
    `containment`, and hit it.  Same defect, same model, one lost hit.

    The exemption stays narrow on purpose: 0029-gpt's `REQ-030A..E` propose
    `UrbanMode.FinishState` for `occupancy_after`/`edge_declared` primaries, where the
    declared path is a *route to* the claim rather than the claim, and those keep the
    waiver.
    """

    from paper_stm_feedback_loop.discover.capability import (
        SCOPE_LOCAL_WAIVER,
        redundant_proposal_findings,
    )

    vocabulary = {"states": tuple(GATE_KNOWN)}
    waiver = (f"{SCOPE_LOCAL_WAIVER}: the sentence says substate",)

    def fired(predicate, bindings, limitations=()):
        return redundant_proposal_findings(
            (Req("R", predicate, bindings, limitations=limitations),), GATE_KNOWN, vocabulary
        )

    proposal = {"parent": "Sys.ModeA", "child": "Sys.ModeA.Done"}
    # Refused with or without the waiver, and the message says why rather than
    # pointing at an exit that does not apply.
    plain = fired("containment", proposal)
    assert len(plain) == 1
    assert SCOPE_LOCAL_WAIVER not in plain[0]
    assert "False is then the finding" in plain[0]
    assert len(fired("containment", proposal, waiver)) == 1
    assert len(fired("initial_target", {"composite": "Sys.ModeA", "child": "Sys.ModeA.Done"}, waiver)) == 1
    # Every other predicate keeps the exit.
    assert fired("occupancy_after", {"target": "Sys.RegionB.Done"}, waiver) == ()
    assert len(fired("occupancy_after", {"target": "Sys.RegionB.Done"})) == 1
