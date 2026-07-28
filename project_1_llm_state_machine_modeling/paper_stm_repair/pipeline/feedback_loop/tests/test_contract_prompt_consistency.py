"""S6 guard: the frozen design contract must actually reach the prompt.

Issue #167 §5.3 states an *ordered* classification rule and names guard overlap
as a `structure` claim.  That rule was correct and it was never transferred into
`prompts.py`: the splitter got three parallel definitions, no ordering, no guard
precedent, and `Use structure only when ...` phrasing that reads as a
restriction rather than a default.  Two independent models then classified pair
0029's distinguishability requirement as `property` -- consistently, and
defensibly given the text they were shown.

Existing tests only grepped for the presence of key phrases, which is why
`101 passed` coexisted with a reproducible misclassification.  These tests check
the *rule*: its ordering, its worked precedent, and the absence of a competing
vocabulary.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover import prompts, renderer  # noqa: E402
from paper_stm_feedback_loop.discover.predicates import PREDICATES  # noqa: E402
from paper_stm_feedback_loop.discover.nodes import _fallback_prepare  # noqa: E402
from paper_stm_feedback_loop.discover.schemas import DiscoverInput  # noqa: E402

MODEL = """state Root {
    event go;
    state Idle;
    state Done;
    [*] -> Idle;
    Idle -> Done : /go;
}
"""


def _splitter_head() -> str:
    """The splitter rules, excluding the appended language guides."""

    return prompts.REQUIREMENT_SPLITTER_PROMPT.split("=== FCSTM grammar guide")[0]


def test_every_vocabulary_predicate_reaches_the_splitter() -> None:
    """The prompt is rendered from the table, so the two cannot drift apart.

    Under v2 the classification rule was hand-written prose that had to be kept
    in sync with the design by hand; it was not, and two models then classified
    the same requirement wrongly but defensibly.  A predicate that exists in the
    table but not in the prompt would recreate exactly that gap.
    """

    head = _splitter_head()
    for item in PREDICATES:
        assert f"`{item.name}(" in head, item.name
        assert item.meaning in head, item.name


def test_splitter_is_given_the_contain_versus_do_distinction() -> None:
    """The single highest-value piece of guidance, with a worked pair."""

    head = _splitter_head()
    assert "what the model *contains* or about what the model *does*" in head
    assert "`edge_declared`" in head and "`occupancy_after`" in head
    assert "unreachable, guard-blocked" in head


def test_guard_distinguishability_precedent_reaches_the_splitter() -> None:
    """Issue #167 §5.3 puts guard overlap under structural evidence; so must the prompt."""

    head = _splitter_head()
    assert "guard_distinguishable" in head
    assert "guard_distinguishable" in head, (
        "the worked precedent must name the deciding query, not just the category"
    )


def test_splitter_is_told_what_each_family_costs_and_cannot_do() -> None:
    """The node that fixes the family must see the obligation it creates."""

    head = _splitter_head()
    for marker in ("what the model does when it runs", "checked up to a bound"):
        assert marker in head, marker
    # The caveats are the honest part: a predicate whose infrastructure is
    # partial must say so where the producer will read it.
    assert "tautology" in head, "the vacuous-invariant trap must be stated"
    # path() is gone; the surviving over-approximation the splitter must know
    # about is that `reaches` ignores triggers.
    assert "ignores triggers" in head, "the reaches over-approximation must be stated"


def test_family_is_derived_not_chosen() -> None:
    head = _splitter_head()
    assert "derived from the predicate" in head
    assert "you do not choose it" in head


def test_requirement_reviewer_applies_the_predicate_gate() -> None:
    reviewer = prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "Reject a Family S predicate" in reviewer
    assert "Reject a Family P predicate whose obligation an exact" in reviewer
    assert "name the predicates it should be split into" in reviewer


def test_assertion_stages_receive_the_procedure_binding() -> None:
    """A locator must never be able to close a claim it does not decide."""

    for name in ("ASSERTION_CONVERTER_PROMPT", "ASSERTION_REVIEWER_PROMPT"):
        text = getattr(prompts, name)
        assert "Callable predicate reference" in text, name
        assert "occupancy_after(source: str, trigger: str, target: str" in text, name
        assert "ONLY evidence functions in" in text, name


def test_splitter_no_longer_carries_a_competing_taxonomy() -> None:
    """`structure` must not simultaneously be a legacy checkability value."""

    head = _splitter_head()
    assert "Classify checkability by the source claim" not in head
    assert "relation for an explicitly requested static model relation" not in head


def test_splitter_payload_puts_the_specification_before_the_model_facts() -> None:
    import json

    frozen = _fallback_prepare(
        DiscoverInput(
            run_id="order",
            natural_language="Idle shall reach Done on go.",
            stm_text=MODEL,
            language="en-US",
        )
    )
    keys = list(json.loads(renderer.render_requirement_split_input(frozen)))
    assert keys[0] == "natural_language"
    assert keys.index("natural_language") < keys.index("inspect_digest")
    assert keys.index("nl_segments") < keys.index("stm_text")


def test_binding_output_contract_is_the_last_thing_each_producer_reads() -> None:
    """Long authoritative appendices must not bury the output schema.

    Three Claude cells in matrix v3-r2 emitted the removed legacy
    `checkability` field when the v2 contract sat mid-prompt behind a 16 KB
    grammar guide.  The schema rule has to be the final instruction.
    """

    tails = {
        "splitter": prompts.REQUIREMENT_SPLITTER_PROMPT[-1500:],
        "reviewer": prompts.REQUIREMENT_REVIEWER_PROMPT[-1500:],
        "converter": prompts.ASSERTION_CONVERTER_PROMPT[-1500:],
    }
    assert "There is no `checkability` field" in tails["splitter"]
    assert "verification_kind" in tails["splitter"]
    assert "legacy `checkability` field" in tails["reviewer"]
    assert "`role`" in tails["converter"] and "`coverage_key`" in tails["converter"]
    for name, tail in tails.items():
        assert "overrides anything above" in tail, name


def test_undeclared_binding_rule_is_consistent_across_producers() -> None:
    """Splitter, reviewer and converter must agree on the same encoding.

    Pair 0006-gpt deadlocked because two instructions contradicted each other:
    bindings had to appear verbatim in the declared vocabulary, *and* a term the
    NL required but the model did not declare had to be bound to the closest
    declared term.  The splitter obeyed the second, the reviewer enforced the
    first, and the loop ran five revisions until the growing ledger payload broke
    the provider's streamed tool call.  A contradiction between two prompts fails
    like a transport fault, so pin the agreement.
    """

    splitter = prompts.REQUIREMENT_SPLITTER_PROMPT
    reviewer = prompts.REQUIREMENT_REVIEWER_PROMPT
    converter = prompts.ASSERTION_CONVERTER_PROMPT

    for name, text in (
        ("splitter", splitter),
        ("reviewer", reviewer),
        ("converter", converter),
    ):
        assert "`<undeclared>`" in text, name

    # The splitter must be told to use it instead of substituting a declared term.
    assert "Do not substitute a different declared term" in splitter
    # The reviewer must accept it where it is the only legal encoding, or the
    # loop cannot converge -- and must reject it where the checker will refuse
    # it, or the item burns its whole repair budget instead of being fixed in
    # one round.  Both halves, or the stages contradict each other again.
    # Conditional acceptance, both directions.  Unconditional acceptance let the
    # literal through where a declared element fitted; unconditional rejection
    # produced the loop pair 0006 died in.
    assert "Accept `<undeclared>`" in reviewer
    assert "no declared element plausibly is the one the sentence means" in reviewer
    assert "**Reject it** when a declared element does plausibly fit" in reviewer
    # The converter must pass it straight through as the primary.  The earlier
    # contract said the opposite -- primary forbidden, supporting only -- and
    # that is what lost pair 0006's expected defect: with no primary the
    # requirement could only be filed as an unchecked coverage gap, so a real
    # finding was reported as "not looked at".
    # The converter no longer passes the literal to a predicate at all: it turns
    # it into a proposed name, an existence `precondition`, and a dependent
    # primary, so the gap becomes something repair can act on.
    assert "needs two assertions, not one" in converter
    assert "`precondition` asserting that the missing element **exists**" in converter
    assert "`depends_on` naming the" in converter
    assert "repair stage can add exactly that element" in converter
    assert "only `supporting`" not in converter

    # And the old contradictory sentence must be gone.
    assert "bind the closest declared term the sentence does name" not in splitter


def test_multi_field_outputs_are_shown_not_described() -> None:
    """Every multi-field structured output needs at least three worked objects.

    Prose is not enough.  The converter prompt named `role`, `coverage_key` and
    `aggregation_group` three separate times, and producers still emitted the
    first two and dropped the third; the controller back-filled it, a gate
    rejected the back-fill as legacy, every assertion in the script was isolated
    and three of eight matrix cells died with an empty script.  A field seen
    filled in three complete examples does not get dropped.
    """

    cases = [
        (
            "ASSERTION_CONVERTER_PROMPT",
            ("assertion_id", "role", "coverage_key", "aggregation_group", "evidence_family"),
        ),
        (
            "REQUIREMENT_SPLITTER_PROMPT",
            ("requirement_id", "predicate", "predicate_bindings", "coverage_obligation"),
        ),
    ]
    for name, fields in cases:
        text = getattr(prompts, name)
        for field in fields:
            shown = text.count(f'"{field}":')
            assert shown >= 3, f"{name} shows {field} in only {shown} worked objects"


def test_prompts_do_not_leak_benchmark_identifiers() -> None:
    """No prompt may name an element of the evaluation corpus.

    A producer whose system prompt contains identifiers from the 60 evaluated
    pairs is not solving the task blind, and the result would be challenged.
    """

    corpus = (
        ROOT.parent / "representation/reports/llms_emp_r45_java_60/pairs"
    )
    leaked: list[str] = []
    # Only the text this repository authors is checked.  The appended pyfcstm
    # grammar guide is upstream documentation with its own worked examples, and
    # one of its illustrative names (`EmergencyStop`) happens to also occur in
    # the corpus.  That is coincidence, not leakage, and it is not ours to edit;
    # scoping the check to our own prose keeps it meaningful instead of noisy.
    def authored(name: str) -> str:
        text = getattr(prompts, name)
        for guide in ("\n\n=== FCSTM grammar guide", "\n\n=== FBMCQ language guide"):
            head, _, _ = text.partition(guide)
            text = head
        return text

    prompt_texts = {
        name: authored(name)
        for name in (
            "REQUIREMENT_SPLITTER_PROMPT",
            "REQUIREMENT_REVIEWER_PROMPT",
            "ASSERTION_CONVERTER_PROMPT",
            "ASSERTION_REVIEWER_PROMPT",
            "RESULT_ADJUDICATOR_PROMPT",
        )
    }
    # Only multi-word identifiers are checked.  A single English word such as
    # `Condition` or `Transition` appears in ordinary prose, so matching those
    # reports the prompt's own vocabulary as a leak.  A CamelCase compound of
    # two or more words, or a snake_case compound, is corpus-specific enough
    # that a coincidental match is implausible.
    pattern = re.compile(
        r"\b(?:[A-Z][a-z]{2,}){2,}\b|\b[a-z]{3,}(?:_[a-z0-9]{2,}){2,}\b"
    )
    seen: set[str] = set()
    for case in sorted(corpus.iterdir())[:60]:
        fcstm = case / "fcstm.fcstm"
        if not fcstm.exists():
            continue
        for token in pattern.findall(fcstm.read_text()):
            if token in seen or len(token) < 10:
                continue
            seen.add(token)
            for name, text in prompt_texts.items():
                if token in text:
                    leaked.append(f"{name}: {token}")
    assert not leaked, f"benchmark identifiers reached the prompts: {sorted(set(leaked))[:10]}"


def test_requirement_stages_are_warned_off_the_two_silent_failures() -> None:
    """`[*]` misuse and model-derived requirements both pass every gate.

    Pair 0000's expected defect is that Power Off is declared on the initial
    pseudostate instead of on the running modes.  Claude bound `source="[*]"`,
    which is precisely the model's own mistake restated as the requirement; the
    check then passed, the cell reported zero issues, and nothing downstream
    could tell.  Both halves have to be said, to the splitter that writes the
    binding and to the reviewer that is the only stage able to reject it.
    """

    splitter = prompts.REQUIREMENT_SPLITTER_PROMPT
    reviewer = prompts.REQUIREMENT_REVIEWER_PROMPT

    for name, text in (("splitter", splitter), ("reviewer", reviewer)):
        assert "power-on, startup or first entry" in text, name
        assert "already running" in text, name
        assert "natural language" in text, name

    # The splitter needs the positive instruction, the reviewer the rejection.
    assert "is never on its own a reason to reach for `[*]`" in splitter
    assert "Reject `[*]` on a claim that is not about power-on" in reviewer
    assert "restates the model instead of the natural language" in reviewer


def test_the_schema_rule_survives_the_new_guidance() -> None:
    """Guidance added mid-prompt must not push the output contract out of the tail.

    Checked separately from the tail test above because the failure mode is
    additive: every future paragraph is one more chance to bury the schema rule
    that three cells already violated once.
    """

    for name in ("REQUIREMENT_SPLITTER_PROMPT", "ASSERTION_CONVERTER_PROMPT"):
        text = getattr(prompts, name)
        assert "overrides anything above" in text[-1500:], name


def test_the_undeclared_rule_is_the_same_on_all_four_producer_surfaces() -> None:
    """A rule changed on one surface and left stale on another is a deadlock.

    Pair 0006 ran five revisions and died on a transport fault because the
    splitter and the reviewer had been given contradictory `<undeclared>` rules.
    Reversing the rule for the converter and leaving the old wording in the
    predicate table and the evidence-API doc rearmed exactly that: the assertion
    reviewer reads both of those, so it was told the call "raises" and is
    "recorded rather than tested" while the converter was told to write it as a
    normal primary.

    The check is over the *assembled* prompts plus the evidence-API doc that
    ships inside the converter's and reviewer's user payloads, because that is
    the full set of text a producer sees.
    """

    from paper_stm_feedback_loop.assertions.environment import (
        get_assertion_environment_api_docs,
    )

    surfaces = {
        "splitter": prompts.REQUIREMENT_SPLITTER_PROMPT,
        "requirement_reviewer": prompts.REQUIREMENT_REVIEWER_PROMPT,
        "converter": prompts.ASSERTION_CONVERTER_PROMPT,
        "assertion_reviewer": prompts.ASSERTION_REVIEWER_PROMPT,
        "evidence_api": get_assertion_environment_api_docs(),
    }
    stale = (
        "recorded as a gap",
        "the absence is the finding and the controller records",
        "recorded rather than tested",
        "the controller records the absence",
        "records it as a coverage gap",
        "no executable primary check",
    )
    for name, text in surfaces.items():
        for phrase in stale:
            assert phrase not in text, f"{name} still carries the reversed rule: {phrase!r}"

    # And the surfaces that describe the call must describe the *current*
    # semantics: read the table, false when empty, refused when populated.
    for name in ("converter", "assertion_reviewer", "evidence_api"):
        text = surfaces[name]
        assert "declaration table" in text, name
        assert "refused" in text, name


def test_the_fold_restriction_reaches_the_stages_that_write_and_review_folds() -> None:
    """`all([...])` is allowed; an `<undeclared>` arm inside one is not.

    Verified on pair 0000 that a true second arm gets overruled by a raising
    first arm, so the producer has to be told, and the reviewer has to be able
    to catch it.
    """

    for name in ("ASSERTION_CONVERTER_PROMPT", "ASSERTION_REVIEWER_PROMPT"):
        text = getattr(prompts, name)
        assert "must stand alone" in text or "stand alone" in text, name
        assert "arms that never" in text or "never evaluated" in text or "never ran" in text, name


def test_no_stage_demands_the_binding_the_checker_refuses() -> None:
    """`<undeclared>` is now conditional, and every stage has to know the condition.

    The checker seals a false only when the declaration table is empty of the
    author's own entries; with entries present it refuses and the item goes back
    for repair.  Three stages were still stating the old unconditional rule --
    the splitter that chooses the binding, the requirement reviewer forbidden
    from asking for a declared name, and the assertion reviewer *demanding*
    `<undeclared>` whenever the NL omits an identifier.  A model that declares a
    plausible variable then had no legal move anywhere in the loop: five repair
    rounds, then a coverage gap.  That is the original pair-0006 loss with the
    branch moved over one.
    """

    splitter = prompts.REQUIREMENT_SPLITTER_PROMPT
    requirement_reviewer = prompts.REQUIREMENT_REVIEWER_PROMPT
    assertion_reviewer = prompts.ASSERTION_REVIEWER_PROMPT

    # The per-binding-kind rules are gone along with the judgement they served --
    # seal for `variable`/`trigger`, refuse for state-shaped and expression ones --
    # because the literal no longer reaches a predicate at all.  What the splitter
    # needs now is when choosing it is right in the first place.
    assert "genuinely has no term of that kind" in splitter
    assert "name that element instead" in splitter, (
        "the splitter must be told to prefer a declared element when one fits"
    )

    # Neither reviewer may state the rule unconditionally any more.
    assert "Otherwise require `variable=\"<undeclared>\"`" not in assertion_reviewer
    assert (
        "Do not ask the Splitter to replace it with a declared term"
        not in requirement_reviewer
    ), "the unconditional form contradicts the conditional acceptance above"


def test_the_splitter_is_warned_that_the_literal_now_produces_a_finding() -> None:
    """It used to cost a coverage gap; it now publishes a defect.

    That asymmetry matters for precision: reading an empty variable table proves
    the *model* declares nothing, not that the *NL* required something.  The
    stage that judges the second half is the splitter, so the caution belongs
    where it makes the call.
    """

    splitter = prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "only when the NL genuinely imposes an obligation" in splitter


def test_no_worked_example_shows_an_assert_statement_in_the_expression_field() -> None:
    """`expression` holds an expression; the controller adds the `assert`.

    Both Claude cells of matrix v7 died here.  The examples were written as
    complete `assert <call> is True, "[REQ-001][AST-001] ..."` statements to show
    the label convention, the model copied that shape into the `expression`
    field, and the controller's own wrapper turned every one into
    `assert (assert ... , "..."), "..."` -- `AssertionScriptSyntaxError` on all
    five assertions, every item quarantined, then `soft isolation cannot publish
    an empty AssertionScript`.  Four cells, zero results, and the cause was a
    prompt example rather than anything either model did wrong.
    """

    for name in ("ASSERTION_CONVERTER_PROMPT", "ASSERTION_REVIEWER_PROMPT"):
        text = getattr(prompts, name)
        offenders = [
            line.strip()
            for line in text.splitlines()
            # An indented example line is a template the producer will copy.
            if line.startswith("    ") and line.strip().startswith("assert ")
            # The one deliberate counter-example is labelled as wrong.
            and "wrong:" not in line
        ]
        assert not offenders, f"{name} shows assert-statement examples: {offenders[:3]}"

    # And the field contract has to be stated, not merely implied by the examples.
    converter = prompts.ASSERTION_CONVERTER_PROMPT
    assert "holds a bare boolean EXPRESSION" in converter
    assert "Do not write `assert`" in converter
    assert "belongs in the separate `failure_message` field" in converter


def test_every_new_field_is_shown_filled_in_at_least_three_worked_objects() -> None:
    """Prose naming a field is not enough; producers drop what they have not seen.

    Established twice: `aggregation_group` was named three times in prose and
    still omitted until it appeared in every example, and `expression` written as
    a complete `assert` statement in the examples taught four cells to emit the
    statement form.  So the four fields the precondition design adds are held to
    the same bar.
    """

    converter = prompts.ASSERTION_CONVERTER_PROMPT
    for field in ("rationale", "depends_on", "role", "coverage_key"):
        shown = converter.count(f'"{field}":')
        assert shown >= 3, f"{field} appears in only {shown} worked objects"
    # `strategies` is script-level, so one object is right -- but it must carry
    # more than one requirement, or the producer will emit a single entry.
    assert converter.count('"strategies":') >= 1
    strategies_block = converter[converter.index('"strategies":') :]
    assert strategies_block.count('": "') >= 2, "show strategies for two requirements"


def test_the_precondition_shape_appears_as_a_complete_worked_pair() -> None:
    """A precondition alone teaches nothing: the dependency is the point.

    The example has to show both objects and the `depends_on` linking them, or a
    producer writes an unreferenced precondition -- which the gate then rejects for
    being orphaned, costing a round to learn what the example could have taught.
    """

    converter = prompts.ASSERTION_CONVERTER_PROMPT
    assert '"role": "precondition"' in converter
    assert '"depends_on": ["AST-REQ-003-0"]' in converter, (
        "the dependent must be shown pointing at the precondition by id"
    )
    # And the existence predicates must be named where the shape is explained.
    for predicate in ("variable_declared", "event_declared"):
        assert predicate in converter, predicate


def test_no_worked_object_writes_a_statement_into_the_expression_field() -> None:
    """The regression that killed four cells, pinned across both assertion stages."""

    for name in ("ASSERTION_CONVERTER_PROMPT", "ASSERTION_REVIEWER_PROMPT"):
        text = getattr(prompts, name)
        offenders = [
            line.strip()
            for line in text.splitlines()
            if line.strip().startswith('"expression": "assert ')
        ]
        assert not offenders, f"{name}: {offenders[:2]}"


def test_the_name_shape_rule_reaches_the_producer() -> None:
    """A malformed name is refused, not answered, so the producer must know the shape.

    Measured from the corpus: variables are bare, states and events dotted, events
    always carry their root prefix.  A producer that guesses pays a round.
    """

    converter = prompts.ASSERTION_CONVERTER_PROMPT
    assert "well-formed FCSTM name" in converter
    assert "bare for variables" in converter
    assert "events always carry their root prefix" in converter
    assert "refused rather than answered" in converter
