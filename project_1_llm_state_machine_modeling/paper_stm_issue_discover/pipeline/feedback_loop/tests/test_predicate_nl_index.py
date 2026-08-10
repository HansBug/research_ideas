"""The forward index from sentence shape to predicate must stay complete.

The catalogue the splitter reads is written from the predicate's side -- signature,
what it asserts, what it exposes.  That direction only helps a reader who has
already guessed which predicate they want.  A producer holds a sentence, and in
the 324-cell v37 run the single largest loss (127 of 288 all-zero positions) was
the needs layer never forming the obligation at all: five predicates appeared in
the whole 77 KB prompt exactly once, in their own signature line, with nothing
saying when to reach for them.

These tests pin the property that fixed it, not the wording that fixed it: every
predicate is reachable from the sentence side, and the index the producer scans
lists all of them.  A twentieth predicate added without an index entry fails at
import (the fields are required), and these tests catch the weaker failures --
an entry that is present but empty, duplicated, or missing from the render.
"""

from __future__ import annotations

import pytest

from paper_stm_feedback_loop.discover.predicates import (
    PREDICATES,
    vocabulary_prompt,
)


@pytest.mark.parametrize("predicate", PREDICATES, ids=lambda item: item.name)
def test_every_predicate_carries_both_directions(predicate) -> None:
    """No predicate may be reachable only from its own name."""

    assert predicate.nl_index.strip(), f"{predicate.name} has no index line"
    assert predicate.nl_cue.strip(), f"{predicate.name} has no cue"


@pytest.mark.parametrize("predicate", PREDICATES, ids=lambda item: item.name)
def test_index_line_stays_scannable(predicate) -> None:
    """The index is scanned, not read: one line each, no newlines."""

    assert "\n" not in predicate.nl_index
    assert len(predicate.nl_index) <= 120, len(predicate.nl_index)


def test_index_lines_are_distinct() -> None:
    """Two predicates sharing an index line make the choice between them a coin flip."""

    seen: dict[str, str] = {}
    for item in PREDICATES:
        assert item.nl_index not in seen, (
            f"{item.name} and {seen[item.nl_index]} share an index line"
        )
        seen[item.nl_index] = item.name


def test_rendered_vocabulary_lists_every_predicate_in_the_index() -> None:
    """The render must not drop a predicate the table declares."""

    rendered = vocabulary_prompt()
    head, _, catalogue = rendered.partition("Family S --")
    assert "Which predicate the sentence is asking for" in head
    for item in PREDICATES:
        assert f"<- {item.nl_index}" in head, f"{item.name} missing from the index"
        assert f"reach for it when: {item.nl_cue}" in catalogue, item.name


def test_cue_sits_where_the_choice_is_made() -> None:
    """Under ``asserts``, before ``exposes`` -- the reader decides there."""

    rendered = vocabulary_prompt()
    for item in PREDICATES:
        asserts = rendered.index(f"asserts: {item.meaning}")
        cue = rendered.index(f"reach for it when: {item.nl_cue}")
        exposes = rendered.index(f"exposes: {item.proves}", asserts)
        assert asserts < cue < exposes, item.name
