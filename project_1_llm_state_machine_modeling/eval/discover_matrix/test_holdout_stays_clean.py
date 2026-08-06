"""A hold-out that has been written about is no longer one, so this fails when that happens.

The set is frozen in `holdout.json`. Its purity is not a claim about the past -- it is a
property that has to keep holding, and every future commit is a chance to break it: a gate whose
docstring cites `pair 0010`, a test fixture named `0008-claude`, a commit body explaining that
some rule exists because of `EIS-0014-02`. Each of those silently converts the hold-out back
into a tuned cell, and nothing else in the repository would notice.

Run it directly (`python -m pytest test_holdout_stays_clean.py`) or via the eval suite.
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import holdout  # noqa: E402

FROZEN = json.loads((HERE / "holdout.json").read_text())


def test_verify_does_not_recompute_the_candidate_pool() -> None:
    """The first version asserted `compute()["holdout"] == frozen`, and running the hold-out
    destroyed it: rule 2 (never run) then excludes the very pairs that were frozen, so the
    recomputed set is necessarily different and the check is permanently red -- with the same
    message a real burn would produce. `--verify` must therefore pass on a tree where the
    hold-out has been run, and `compute()` must be allowed to differ from the frozen set.
    """
    assert holdout.main(["--verify"]) == 0
    recomputed = holdout.compute()["holdout"]
    # Not an equality assertion in either direction -- only that a difference is tolerated.
    assert isinstance(recomputed, list)


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


def test_no_held_out_pair_shares_an_nl_group_with_a_tuned_cell() -> None:
    """Same group means the same requirement text and reference model.

    A rule written against one member acts on every member, which a pair-id spelling check
    cannot see. The first freeze held two pairs sharing NL08 and NL05 with the tuned cells.
    """
    assert set(FROZEN["holdout_groups"].values()).isdisjoint(set(FROZEN["excluded_tuned_groups"]))


def test_no_nl_group_dominates_the_holdout() -> None:
    counts = collections.Counter(FROZEN["holdout_groups"].values())
    assert max(counts.values()) <= FROZEN["max_per_group"]
    assert len(counts) >= 5, f"only {len(counts)} distinct NL groups: {dict(counts)}"


def test_no_held_out_pair_was_already_run_and_published() -> None:
    """`runs/` is not the only run ledger; two pairs' results were published in a PR comment."""
    assert set(FROZEN["holdout"]).isdisjoint(set(FROZEN["previously_run_and_published"]))
    assert set(FROZEN["holdout"]).isdisjoint(set(FROZEN["run_seen_in_runs_dir"]))


def test_layers_too_thin_to_report_are_marked_as_such() -> None:
    """Reporting `@k` per layer off 2 records is reporting a Bernoulli draw as a percentage."""
    reportable = FROZEN["layers_reportable_at_k"]
    for layer, ok in reportable.items():
        n = FROZEN["holdout_layer_coverage"].get(layer, 0)
        assert ok == (n >= 4), f"{layer}: {n} records but reportable={ok}"
    assert any(reportable.values()), "no layer has enough records to report at all"


def test_an_undersized_freeze_is_refused() -> None:
    """An empty hold-out written to disk looks exactly like a valid one, and divides by zero."""
    assert FROZEN["holdout_judgeable_total"] >= 20
    assert len(FROZEN["holdout"]) >= 5


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



