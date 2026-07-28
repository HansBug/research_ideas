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
    for marker in ("the predicate runs the model", "bounded check"):
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
        assert "ONLY evidence functions that exist" in text, name


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
    # The reviewer must be told to accept it, or the loop cannot converge.
    assert "Accept `<undeclared>`" in reviewer
    assert "unresolvable review loop" in reviewer
    # The converter must not manufacture a primary for an unassertable claim.
    assert "no executable primary check" in converter
    assert "only `supporting`" in converter

    # And the old contradictory sentence must be gone.
    assert "bind the closest declared term the sentence does name" not in splitter
