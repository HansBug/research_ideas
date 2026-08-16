"""Pin the gist anchor rule against the real GitHub slug, offline.

A wrong anchor does not 404 -- the browser lands on the top of the gist page with no
warning -- so this is the kind of defect that survives a link check that only looks at
HTTP status.  The expected values below were read out of the rendered gist DOM
(`id="file-_summary-json"`, `id="file-figure_data-tsv"`), not derived from a slug library.
"""

from __future__ import annotations

import pytest

from render_refcmp_issue import anchor, bar


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        # underscores survive -- this is the case the naive slugifier got wrong
        ("_summary.json", "file-_summary-json"),
        ("figure_data.tsv", "file-figure_data-tsv"),
        # hyphens survive too
        ("0010-review.json", "file-0010-review-json"),
        ("0058-readable.md", "file-0058-readable-md"),
        # uppercase folds
        ("README.md", "file-readme-md"),
        ("index.tsv", "file-index-tsv"),
        # only the dot is rewritten, and every dot is
        ("a.b.c", "file-a-b-c"),
    ],
)
def test_anchor_matches_github_slug(filename: str, expected: str) -> None:
    assert anchor(filename) == expected


def test_anchor_never_collapses_underscore_to_hyphen() -> None:
    """Guards the specific regression: `_x` must not become `-x`."""
    assert not anchor("_summary.json").startswith("file--")


@pytest.mark.parametrize(
    ("value", "top", "width", "expected_filled"),
    [
        (0, 10, 4, 0),
        (10, 10, 4, 4),
        (5, 10, 4, 2),
        (1, 100, 10, 0),  # rounds to nothing but must still render a full-width cell
    ],
)
def test_bar_width_is_constant(value: int, top: int, width: int, expected_filled: int) -> None:
    out = bar(value, top, width)
    assert len(out) == width, "a ragged bar column misreads as a different scale"
    assert out.count("█") == expected_filled


def test_bar_handles_zero_top() -> None:
    """A table whose maximum is zero must not raise; it has nothing to scale against."""
    assert bar(0, 0) == ""
