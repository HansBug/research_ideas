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


def test_splitter_states_the_ordered_decision_not_three_parallel_options() -> None:
    head = _splitter_head()
    assert "ordered decision" in head
    assert "stop at the first branch that matches" in head
    for ordinal in ("1. `structure`", "2. Otherwise use `behavior`", "3. Otherwise use `property`"):
        assert ordinal in head, ordinal


def test_structure_is_presented_as_the_default_branch() -> None:
    head = _splitter_head()
    assert "`structure` is the default branch" in head
    assert "Use `structure` only when" not in head, (
        "restrictive phrasing biases the producer away from the default branch"
    )


def test_guard_distinguishability_precedent_reaches_the_splitter() -> None:
    """Issue #167 §5.3 lists guard overlap under `structure`; so must the prompt."""

    head = _splitter_head()
    assert "guard overlap" in head or "guard distinguishability" in head
    assert "conflicting_targets" in head, (
        "the worked precedent must name the deciding query, not just the category"
    )
    assert "stays `structure` even when it is phrased with a quantifier" in head


def test_splitter_no_longer_carries_a_competing_taxonomy() -> None:
    """`structure` must not simultaneously be a legacy checkability value."""

    head = _splitter_head()
    assert "Classify checkability by the source claim" not in head
    assert "relation for an explicitly requested static model relation" not in head


def test_splitter_is_told_what_each_branch_costs_downstream() -> None:
    """The node that freezes the kind must see the obligation it creates."""

    head = _splitter_head()
    for marker in ("simulate()", "fbmcq()", "exponential in the bound"):
        assert marker in head, marker
    assert "cannot observe guard expressions" in head


def test_requirement_reviewer_applies_the_same_ordered_rule() -> None:
    reviewer = prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "first match wins" in reviewer
    assert "guard overlap/distinguishability" in reviewer
    assert "Reject a `property` classification whose obligation an exact" in reviewer


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
