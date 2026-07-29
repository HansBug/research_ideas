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


def test_the_missing_element_rule_is_one_ordered_procedure() -> None:
    """One procedure, four ordered exits, described in exactly one place.

    This test exists because the failure it guards against already happened twice.
    First two instructions contradicted each other about vocabulary binding and the
    loop ran five revisions until the provider's streamed tool call broke.  Then a
    "propose the name the element should have" paragraph was added beside a
    surviving "do not force a predicate and do not invent a name" bullet: the
    producer obeyed the newer one, invented a terminal state on a model that
    terminates correctly, and two fabricated defects were published (pair 0050).

    So the invariant is not "the wording is good" but "there is one rule".  A
    second, independent description of what to do when a binding cannot be made is
    the defect, however sensible it reads on its own.
    """

    splitter = prompts.REQUIREMENT_SPLITTER_PROMPT

    # The procedure, in order, with each step's exit named.
    for marker in (
        "Step 1 -- is the concept a pseudo-state?",
        "Step 2 -- does `declared_model_vocabulary` declare that element somewhere else?",
        "Step 3 -- does a declared element plausibly denote the same thing?",
        "Step 4 -- none of the above",
    ):
        assert marker in splitter, marker
        assert splitter.count(marker) == 1, f"{marker} is described twice"

    # Step 1 must name both predicates that answer a pseudo-state concept, or the
    # producer has the rule and no way to act on it.
    assert "`terminates`" in splitter
    assert "`initial_target`" in splitter
    # And it must point at the evidence that decides step 1, not ask for a guess.
    assert "terminating_transitions" in splitter
    assert "initial_entries" in splitter

    # The retired second description must be gone, not merely outvoted.
    assert "do not force one and do not invent a name" not in splitter
    assert "bind the closest declared term the sentence does name" not in splitter

    # The converter still owns the two-assertion shape for step 4, and only that.
    converter = prompts.ASSERTION_CONVERTER_PROMPT
    assert "needs two assertions, not one" in converter
    assert "`precondition` asserting that the missing element **exists**" in converter
    assert "with `depends_on` naming the precondition" in converter


def test_each_step_of_the_procedure_has_a_worked_object() -> None:
    """Prose alone has failed here twice; a step without an example gets skipped.

    The four steps are a decision procedure, and the one that misfires in practice
    is not step 4 -- it is stopping too late, at step 4, when step 1 or 2 applied.
    Those two need to be *shown*, not just ordered.
    """

    splitter = prompts.REQUIREMENT_SPLITTER_PROMPT
    for marker, needle in (
        ("step 1", '"predicate": "terminates"'),
        ("step 2", '"target": "Sys.RegionA.Done"'),
        # Deliberately not `Sys.Searching`: the step-3 example used to say "target
        # search task" against a declared `Searching` released by `Intercepted`, all
        # three of which pair 0006 carries verbatim in its own NL and model.  A
        # worked example that pre-answers the step-3-versus-step-4 judgement for a
        # corpus pair, in that pair's own words, is a leak -- and step 3 versus 4 is
        # exactly the call the Requirement Reviewer is supposed to make unaided.
        ("step 3", '"state": "Sys.Calibrating"'),
    ):
        assert needle in splitter, f"{marker} has no worked object ({needle})"
    # Step 4's object predates these and stays: it is the only case a proposed name
    # is legal, so it must remain visible beside the three that outrank it.
    assert '"variable": "unit_count"' in splitter


def test_the_deterministic_steps_are_gated_and_not_left_to_the_reviewer() -> None:
    """Steps 1 and 2 are settled by comparison, so a judgement call is the wrong tool.

    A reviewer asked to re-derive what a comparison answers will sometimes get it
    right, and the cost of the times it does not is the item's whole repair budget.
    The reviewer's text must therefore scope itself to steps 3 and 4 and say the
    first two are already decided -- otherwise both stages own the same rule and
    they will drift.
    """

    reviewer = prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "Judge only the last two steps" in reviewer
    assert "rejected by a gate, so do not spend a finding on them" in reviewer

    # And the gates exist, as functions over the frozen model rather than prose.
    from paper_stm_feedback_loop.discover.capability import (
        redundant_proposal_findings,
        termination_proposal_findings,
    )

    class Req:
        def __init__(self, rid, predicate, bindings):
            self.requirement_id = rid
            self.predicate = predicate
            self.predicate_bindings = bindings

    known = frozenset({"Sys.ModeA", "Sys.RegionA.Done", "Sys.shutdown"})
    ends = (
        {"source": "Sys.ModeA", "trigger": "Sys.shutdown", "ends_run": True},
    )
    # Step 1: a proposed terminal state where the model already ends the run.
    fired = termination_proposal_findings(
        (
            Req(
                "REQ-001",
                "occupancy_after",
                {"source": "Sys.ModeA", "trigger": "Sys.shutdown", "target": "Sys.FinalState"},
            ),
        ),
        known,
        ends,
    )
    assert len(fired) == 1
    assert "terminates(scope='Sys.ModeA'" in fired[0], "the message must name the exit"
    # The same requirement written per step 1 passes.
    assert termination_proposal_findings(
        (Req("REQ-001", "terminates", {"scope": "Sys.ModeA", "trigger": "Sys.shutdown"}),),
        known,
        ends,
    ) == ()
    # Step 2: a proposed path whose leaf is declared under another parent.
    fired = redundant_proposal_findings(
        (Req("REQ-002", "occupancy_after", {"target": "Sys.RegionB.Done"}),), known
    )
    assert len(fired) == 1
    assert "Sys.RegionA.Done" in fired[0], "the message must name the declared path"
    # A genuinely absent element is not this gate's business; step 4 handles it.
    assert redundant_proposal_findings(
        (Req("REQ-003", "variable_delta_after", {"variable": "unit_count"}),), known
    ) == ()


def test_no_surface_carries_a_retired_exit_for_a_missing_element() -> None:
    """A rule dropped from the code but left in a prompt is a live deadlock.

    Both retired exits are checked.  "Bind a stand-in literal" was refused by the
    conversion gate while three prompts still instructed it.  "Emit no primary and
    accept a coverage gap" is worse: the state it names no longer exists in the
    controller, so a producer following it produces a script the contract rejects
    -- and a gap is "not checked", which loses a real finding to silence.

    The check spans the assembled prompts *and* the evidence-API doc that ships
    inside the converter's and reviewer's user payloads, because that is the whole
    of what a producer reads.  The doc was missed once already: the four system
    prompts were cleaned while it went on teaching the literal.
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
    retired = (
        "<undeclared>",
        "recorded as a gap",
        "the absence is the finding and the controller records",
        "recorded rather than tested",
        "the controller records the absence",
        "records it as a coverage gap",
        "no executable primary check",
        "emit no primary",
    )
    for name, text in surfaces.items():
        for phrase in retired:
            assert phrase not in text, f"{name} still carries a retired rule: {phrase!r}"


def test_the_fold_restriction_reaches_the_stages_that_write_and_review_folds() -> None:
    """`all([...])` is allowed; folding an existence check into its dependent is not.

    One verdict cannot say whether the element is missing or whether it is present
    and behaves wrongly, and those take different repairs -- which is the whole
    point of splitting them.  The producer has to be told, and the reviewer has to
    be able to catch it, so both surfaces carry the rule.
    """

    for name in ("ASSERTION_CONVERTER_PROMPT", "ASSERTION_REVIEWER_PROMPT"):
        text = getattr(prompts, name)
        assert "never folds into the claim resting on it" in text, name
        assert "depends_on" in text, name


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


def test_every_worked_example_object_parses_and_validates() -> None:
    """A worked example the schema rejects is a guaranteed wasted revision round.

    This has cost a whole matrix once already: the `expression` examples were
    written as complete `assert` statements, producers copied the shape, and the
    controller wrapped them into `assert (assert ...), "..."` -- a syntax error on
    every assertion, every item quarantined, three of eight cells dead.  The
    prompt's own preamble concedes prose failed twice here, so the examples are
    the contract, and an example that cannot be parsed is not one.

    The same class then recurred quietly: seven of the eight objects carried
    unescaped inner double quotes, so a producer copying them verbatim emits JSON
    that does not parse.  Reading the prompt does not catch that -- parsing it
    does, which is why this is a test and not a review item.
    """

    import json

    from paper_stm_feedback_loop.discover.schemas import AssertionSpec, Requirement

    def objects(text: str, discriminator: str) -> list[str]:
        """Blocks holding ``discriminator``, found from the key outward.

        Scanning forward for a bare `{` does not survive prose: one unbalanced
        brace anywhere above swallows the rest of the prompt into a block that
        never closes, and the extractor silently reports zero examples -- which
        looks exactly like a prompt that has none.
        """

        lines = text.splitlines()
        found: list[str] = []
        for index, line in enumerate(lines):
            if f'"{discriminator}"' not in line:
                continue
            start = next(
                (i for i in range(index, -1, -1) if lines[i].strip() == "{"), None
            )
            if start is None:
                continue
            depth = 0
            for end in range(start, len(lines)):
                depth += lines[end].count("{") - lines[end].count("}")
                if depth <= 0:
                    found.append("\n".join(lines[start : end + 1]))
                    break
        return found

    cases = (
        ("ASSERTION_CONVERTER_PROMPT", "assertion_id", AssertionSpec),
        ("REQUIREMENT_SPLITTER_PROMPT", "predicate_bindings", Requirement),
    )
    for name, discriminator, schema in cases:
        checked = 0
        for block in objects(getattr(prompts, name), discriminator):
            try:
                payload = json.loads(block)
            except json.JSONDecodeError as exc:
                raise AssertionError(
                    f"{name}: a worked object is not parseable JSON ({exc}); a "
                    f"producer copying it emits the same: {block[:160]}"
                ) from exc
            schema.model_validate(payload)
            checked += 1
        assert checked >= 3, (
            f"{name} shows only {checked} complete worked objects; three is the "
            "floor a field needs before producers stop dropping it"
        )


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
