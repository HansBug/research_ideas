"""`occupancy_after` must be non-decreasing in `within_cycles`.

Not a metric — a boolean identity. The parameter is named `within_cycles`, the
docstring says "within ``cycles``", and the splitter prompt tells the producer to
raise it towards the number of declared edges. All three mean "at some point in
the first N cycles". Reading only `view.final` implements "after *exactly* N",
and the two differ whenever an eventless completion edge leaves the target again.

Measured on pair 0018 before the fix:

    occupancy_after(ChargedFlash --Charged_true--> TakePicture, within_cycles=1) -> True
    the same call at within_cycles=2..8                                          -> False

`Junction3 -> join2 -> Junction2 -> TakePicture` collapses into a single cycle --
a pseudo-state is not a stoppable successor, so `join2` synchronises nothing --
and the four spare cycles then let `TakePicture -> WriteMemory` carry the machine
away. So the False was an artefact of the horizon, not a property of the model.

Two costs this had before it was found:

1. Across v22+v23, **51 of 219** False results (23.3%) are True at a smaller
   horizon. Every one was published as a finding.
2. It was mis-attributed. The one `unaccounted_safe_false_assertions` entry in
   v23 was recorded as "concurrency (a join awaiting parallel branches) produced
   this False, and paper1 excludes concurrency" -- i.e. a fixable implementation
   bug was filed as a semantic boundary. `join2` waits for nothing here; the
   trace fires `transition:8` and lands on `TakePicture` in cycle 0. Filing a bug
   as a boundary is worse than filing it as a bug, because a boundary is
   permanent by construction.

`_HORIZON_PROBE` cannot catch this: it searches only *upward*
(`range(asked + 1, ...)`), and its own comment states the assumption it relies on
-- "a genuine defect does not become satisfied at a longer horizon". That
assumption is false for eventless out-edges, which is exactly the population this
predicate meets on a pseudo-state-dense model.
"""

from __future__ import annotations

import pathlib

import pytest

from paper_stm_feedback_loop.assertions.runtime import EvalEnvironment

SEEDS = (
    pathlib.Path(__file__).resolve().parents[3] / "selected_seed_examples"
)

#: The regression that motivated the fix, spelled out so a future edit that
#: reverts the scan-all-cycles behaviour fails on the exact call that found it.
REGRESSION = (
    "0018",
    "ChargedFlash",
    "Charged_true",
    "TakePicture",
)


def _api(pair: str):
    model = SEEDS / f"llms_emp_feedback_final_{pair}" / "model.fcstm"
    if not model.is_file():
        pytest.skip(f"no seed model for {pair}")
    return EvalEnvironment(model_text=model.read_text())


def test_regression_call_is_true_at_every_horizon() -> None:
    """The specific call that was True at 1 and False at 2..8."""

    pair, source, trigger, target = REGRESSION
    env = _api(pair)
    prefix = f"llms_emp_feedback_final_{pair}."
    values = [
        env.predicates.occupancy_after(
            source=prefix + source,
            trigger=prefix + trigger,
            target=prefix + target,
            within_cycles=cycles,
        )
        for cycles in range(1, 9)
    ]
    assert values[0] is True, "the 1-cycle answer was True before the fix too"
    assert all(values), (
        "occupancy_after fell back to False at a longer horizon: "
        f"{dict(zip(range(1, 9), values))}. `within_cycles` means 'within', so a "
        "True at a smaller horizon must stay True at a larger one."
    )


@pytest.mark.parametrize("pair", ["0018", "0038"])
def test_monotone_over_declared_states(pair: str) -> None:
    """No (source, trigger, target) may be True at a small horizon and False later.

    Restricted to two pairs and a small horizon set on purpose: the simulator is
    the slow part, and these two carry every pseudo-state in the grid that the
    projection actually marked. A wider sweep belongs in a nightly job, not in a
    test that must stay fast enough to run on every push.
    """

    env = _api(pair)
    api = env.predicates
    states = [row.path for row in api.structure.states()][:8]
    events = [row.qualified_name for row in api.structure.events()][:3]

    violations = []
    for source in states:
        for target in states:
            if source == target:
                continue
            for trigger in events:
                series = []
                for cycles in (1, 4):
                    try:
                        series.append(
                            api.occupancy_after(
                                source=source, trigger=trigger,
                                target=target, within_cycles=cycles,
                            )
                        )
                    except Exception:
                        # A refusal (UnsupportedEvidence and friends) is not a
                        # monotonicity question; skip rather than swallow the
                        # whole triple.
                        series = []
                        break
                if len(series) == 2 and series[0] and not series[1]:
                    violations.append((source, trigger, target, series))

    assert not violations, (
        f"{len(violations)} monotonicity violation(s) on {pair}: "
        f"{violations[:3]}"
    )
