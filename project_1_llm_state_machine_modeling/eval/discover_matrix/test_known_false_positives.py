"""The false-positive ledger has to stay wired to the things it claims.

A hand-maintained adjudication list rots in two specific ways, and both would be
invisible at the moment it matters -- when a later run is scored against it:

  * a `pinned_by` path that no longer exists, so the claim "this is pinned by a
    regression test" is false and nothing would catch the defect coming back
  * an entry that is in both `fabricated` and `grounded`, which makes the
    checker's verdict depend on dict iteration order

Also checks the checker itself against the run it was adjudicated on: matrix-v16
had exactly three fabricated findings and no unadjudicated extras, so a scan of
that bundle must reproduce those numbers.  That part is skipped when the bundle
is not on disk, since `runs/` is untracked.

Run:
    PYTHONPATH=<repo root> pytest project_1_llm_state_machine_modeling/eval/discover_matrix
"""

from __future__ import annotations

import json
import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import check_false_positives  # noqa: E402

LEDGER = json.loads((HERE / "known_false_positives.json").read_text())
#: `eval/discover_matrix` -> repo root is three levels up.
ROOT = HERE.resolve().parents[2]
FEEDBACK_LOOP = ROOT / "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/feedback_loop"


@pytest.mark.parametrize("entry", LEDGER["fabricated"], ids=lambda e: f"{e['cell']}-{e['requirement_id']}")
def test_every_fabricated_entry_is_pinned_by_a_test_that_exists(entry):
    """An unpinned entry is a claim, not a guard."""

    pinned = entry["pinned_by"]
    assert pinned.startswith("feedback_loop/"), pinned
    path = FEEDBACK_LOOP / pinned.removeprefix("feedback_loop/")
    assert path.exists(), path


def test_no_entry_is_both_fabricated_and_grounded_within_one_run():
    """Across runs the same id legitimately names different claims.

    `0006-claude/REQ-001` is the substate-count finding in matrix-v16 and a missing
    mission-complete state in matrix-v18 -- both grounded, neither a contradiction.
    Within one run a contradiction would make the checker's verdict depend on dict
    iteration order, so that is what this guards.
    """

    def key(entry, req):
        return (entry.get("run", "matrix-v16"), entry["cell"], req)

    fabricated = {key(e, e["requirement_id"]) for e in LEDGER["fabricated"]}
    grounded = {
        key(e, req) for e in LEDGER["grounded"] for req in e["requirement_ids"]
    }
    assert not (fabricated & grounded), fabricated & grounded


def test_every_adjudication_names_the_run_it_was_made_against():
    """Otherwise a later run's entry silently rescopes an earlier verdict."""

    for group in ("fabricated", "grounded"):
        for entry in LEDGER[group]:
            assert entry.get("run"), (group, entry.get("cell"))


def test_every_entry_records_why():
    """The label is worthless without the evidence that produced it."""

    for entry in LEDGER["fabricated"]:
        assert entry["why_fabricated"].strip()
        assert entry["defect_class"].strip()
    for entry in LEDGER["grounded"]:
        assert entry["why_grounded"].strip()
        assert entry["requirement_ids"]


def test_the_checker_reproduces_the_run_it_was_adjudicated_on():
    """Guards the checker's matching logic, which is what a later run rests on."""

    bundle = pathlib.Path("/tmp/v16-gist/audit")
    if not bundle.is_dir():
        pytest.skip("matrix-v16 audit bundle not on disk (runs/ is untracked)")
    result = check_false_positives.scan(bundle, "matrix-v16")
    # Five, not three: 0029-gpt finished after the first adjudication pass and
    # carried two more instances of the `initial_target` class under different
    # requirement ids -- the undercount an id-keyed ledger produces, and the reason
    # `detect_fabrications.py` scores new runs instead.
    assert len(result["still_fabricating"]) == 5, result["still_fabricating"]
    assert result["unadjudicated"] == [], result["unadjudicated"]
    assert result["fixed"] == [], result["fixed"]
    # All eight cells reached a terminal state in the end.
    assert result["incomplete_cells"] == [], result["incomplete_cells"]
