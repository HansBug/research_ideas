"""A hold-out that has been written about is no longer one, so this fails when that happens.

The set is frozen in `holdout.json`. Its purity is not a claim about the past -- it is a
property that has to keep holding, and every future commit is a chance to break it: a gate whose
docstring cites `pair 0010`, a test fixture named `0008-claude`, a commit body explaining that
some rule exists because of `EIS-0014-02`. Each of those silently converts the hold-out back
into a tuned cell, and nothing else in the repository would notice.

Run it directly (`python -m pytest test_holdout_stays_clean.py`) or via the eval suite.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import holdout  # noqa: E402

FROZEN = json.loads((HERE / "holdout.json").read_text())


def test_the_frozen_set_is_what_the_rule_still_produces() -> None:
    """Drift means either the ledger changed or a hold-out pair got named. Both are failures."""
    assert holdout.compute()["holdout"] == FROZEN["holdout"]


def test_no_held_out_pair_is_named_anywhere() -> None:
    fresh = holdout.compute()
    burned = sorted(set(FROZEN["holdout"]) & set(fresh["tainted_pairs"]))
    assert burned == [], (
        f"held-out pairs are now named in pipeline source, tests or a commit body: {burned}. "
        "Reporting capability on them is no longer defensible; pick replacements with "
        "`python -m holdout` and freeze a new set, stating in the report that the old one burned."
    )


def test_the_four_historical_cells_are_all_excluded() -> None:
    """0000/0006/0029/0050 are what eighteen generations were tuned against."""
    assert set(FROZEN["holdout"]).isdisjoint({"0000", "0006", "0029", "0050"})


def test_every_layer_is_represented() -> None:
    """A hold-out covering one defect layer would measure one thing and be reported as four."""
    assert set(FROZEN["holdout_layer_coverage"]) == set(holdout.LAYERS)


def test_the_denominator_is_stated_and_non_trivial() -> None:
    total = FROZEN["holdout_judgeable_total"]
    assert total == sum(row["judgeable_records"] for row in FROZEN["holdout_detail"])
    assert total >= 2 * len(FROZEN["holdout"])


def test_out_of_scope_records_are_excluded_not_counted_as_misses() -> None:
    """paper1 is `M = (S, E, V, Tr, A)`; clocks, invariants and orthogonal regions are outside it.

    A record the closed vocabulary cannot state is unfindable by construction. Counting it as a
    miss reports a declared boundary as a capability gap -- which is the error CLAUDE.md's
    project_1 boundary section exists to prevent.
    """
    excluded = FROZEN["excluded_records_inside_holdout_pairs"]
    assert excluded, "expected at least one excluded record; the filter may have stopped working"
    counted = {rid for row in FROZEN["holdout_detail"] for rid in row["record_ids"]}
    assert counted.isdisjoint(set(excluded))


def test_the_freeze_refuses_to_be_overwritten() -> None:
    """`--freeze` twice must not silently redefine the set after results are in."""
    assert holdout.main(["--freeze"]) == 2


def test_verify_passes_on_the_current_tree() -> None:
    assert holdout.main(["--verify"]) == 0
