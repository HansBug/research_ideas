"""A count of the author's substates must not include the ones the projection inserted.

`cardinality` already says it counts "non-pseudo direct substates" -- it accepts that its
extension needs filtering by what the author actually declared, and filters on `is_pseudo`.
That filter is incomplete. A fail-closed stand-in for a composite whose entry the author
never wrote is an ordinary named state with `is_pseudo` false, so it lands in the count.

The consequence runs both ways, which is what makes fixing it a correction rather than a
loosening:

  the author declares two, the projection adds one, the sentence enumerates three
      -> the count reaches three and the requirement passes. A real defect is masked.

  the author declares three, the projection adds one, the sentence enumerates three
      -> the count reaches four and the requirement fails. A finding is published about
         an element the author never wrote.

Both shapes are in the corpus and both are in one generation's results: one pair reported
satisfied across all three rounds while its enumeration is genuinely wrong, and another
published the same over-report in all three. Filtering the extension flips the first to
False and the second to True -- it does not move the numbers in a single direction.

The filter reads the same `source_exclusions` the attribution layer reads, so "what the
author wrote" has one definition in this pipeline rather than two.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.assertions.predicate_api import (  # noqa: E402
    UnsupportedEvidence,
)

#: Two authored children plus one the projection would have inserted.
MASKED = """state Sys {
    event go;
    state Alpha;
    state Beta;
    state UnspecifiedInitial;
    [*] -> UnspecifiedInitial;
}
"""

#: Three authored children plus the same insertion.
INFLATED = """state Sys {
    event go;
    state Alpha;
    state Beta;
    state Gamma;
    state UnspecifiedInitial;
    [*] -> UnspecifiedInitial;
}
"""


def _api(text: str, exclusions: list[str]):
    from paper_stm_feedback_loop.assertions.runtime import build_eval_environment

    return build_eval_environment(
        model_text=text,
        source_mappings=[],
        source_exclusions=exclusions,
        timeout_seconds=30,
        fbmcq_solver_timeout_ms=15_000,
        fbmcq_max_bound=4,
        fbmcq_process_wall_seconds=20.0,
    ).predicates


_EXCLUDED = ["compiler:state:Sys.UnspecifiedInitial"]


def test_a_masked_shortfall_becomes_visible() -> None:
    """Two authored, one inserted, three enumerated: the count must not reach three.

    Before the filter this answered True and the requirement was recorded as satisfied for
    all three rounds of a generation, while the model is genuinely missing a substate.
    """
    assert _api(MASKED, _EXCLUDED).cardinality(scope="Sys", count=3) is False


def test_the_authored_count_is_what_answers() -> None:
    assert _api(MASKED, _EXCLUDED).cardinality(scope="Sys", count=2) is True


def test_an_inflated_count_stops_being_a_finding() -> None:
    """Three authored, one inserted, three enumerated: this model satisfies the sentence.

    Before the filter this answered False and the over-report was published in all three
    rounds -- one of them saying in its own rationale that the extra child was synthesised
    by the converter, and publishing it anyway.
    """
    assert _api(INFLATED, _EXCLUDED).cardinality(scope="Sys", count=3) is True


def test_both_directions_are_covered_by_one_test_module() -> None:
    """Stated explicitly so a later edit cannot quietly keep only the favourable half.

    A filter that only ever lowers counts would improve precision on one pair and mask a
    defect on another; the pair of expectations above is the evidence that it does neither.
    """
    assert _api(MASKED, _EXCLUDED).cardinality(scope="Sys", count=3) is False
    assert _api(INFLATED, _EXCLUDED).cardinality(scope="Sys", count=3) is True


def test_without_an_exclusion_entry_nothing_is_filtered() -> None:
    """The filter follows the contract, not a name.

    An identically-named state that the contract does not mark compiler-owned is the
    author's, and removing it would be the pipeline second-guessing its own provenance
    record -- the failure a leaf-name substring table produced twice before.
    """
    assert _api(INFLATED, []).cardinality(scope="Sys", count=3) is False
    assert _api(INFLATED, []).cardinality(scope="Sys", count=4) is True


def test_the_extension_is_reported_so_the_count_can_be_audited() -> None:
    """`cardinality` recorded only its scope, so a polluted extension was invisible.

    Two pairs in one generation had their verdicts decided by a member nobody could see in
    the trace. Counting is the one predicate whose answer cannot be checked from its
    arguments, so it has to say what it counted.
    """
    api = _api(INFLATED, _EXCLUDED)
    api.cardinality(scope="Sys", count=3)
    noted = " ".join(str(x) for x in getattr(api, "_refs", ()) or ())
    assert "Sys.Alpha" in noted
    assert "excluded_member" in noted and "UnspecifiedInitial" in noted


def test_an_undeclared_scope_still_refuses() -> None:
    with pytest.raises(UnsupportedEvidence):
        _api(MASKED, _EXCLUDED).cardinality(scope="Sys.Ghost", count=1)
