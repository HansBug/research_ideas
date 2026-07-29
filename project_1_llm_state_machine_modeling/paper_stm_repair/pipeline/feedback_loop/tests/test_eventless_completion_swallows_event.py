"""`occupancy_after` reports a defect the model does not have, when the pinned
state has an eventless completion edge.

Found in matrix-v16's published output, not by inspection: 0050-gpt's only issue
was `AST-REQ-005-1`, an `occupancy_after(AutonomousMode, human_steering..., 
HumanDrivingMode, within_cycles=2)` that came back False.  The pair carries no
expected issue, so that False was published as a confirmed defect the model does
not have -- a fabricated finding in the paper's results.

The model is fine.  Its route is the converter's standard lowering:

    state AutonomousMode {
        [*] -> SubState1;
        SubState1 -> SubState2;      # eventless completion edge
        SubState1 -> [*] : /HS effect { token = 7; };
        ...
    }
    AutonomousMode -> HumanDrivingMode : if [token == 7] ...;

Pinned at `FinalWaittr_0005`, where no eventless edge is outgoing, the predicate
answers True and fires the token route.  Pinned anywhere an eventless edge leaves
-- which is every substate the converter generated, and the composite itself --
it answers False and fires only the eventless edges.  Raising `within_cycles` does
not help: it is False at 9 cycles too, because the event is offered once and that
offer lands on a cycle an unconditional edge has already claimed.

An eventless completion edge is by definition not waiting for anything, so a
configuration that has one outgoing is not a configuration an event can be
observed in.  Settling through them before the event is offered is the only
reading under which the predicate answers the question the requirement asks.
"""

from __future__ import annotations

import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.assertions import build_eval_environment  # noqa: E402

#: The 0050 shape, reduced to what reproduces it: one eventless completion chain,
#: one event edge per link setting the route token, one parent route on the token.
MODEL = """\
def int Token = 0;
state Root named "Root" {
    event HS named "HS";
    state Manual named "Manual";
    state Auto named "Auto" {
        state S1 named "S1";
        state S2 named "S2";
        state Settled named "Settled";
        [*] -> S1;
        S1 -> S2;
        S2 -> Settled;
        S1 -> [*] : /HS effect { Token = 7; };
        S2 -> [*] : /HS effect { Token = 7; };
        Settled -> [*] : /HS effect { Token = 7; };
    }
    Auto -> Manual : if [Token == 7] effect { Token = 0; };
    [*] -> Manual;
}
"""

_ENV: dict[str, object] = {}


def env():
    if "env" not in _ENV:
        _ENV["env"] = build_eval_environment(
            model_text=MODEL,
            source_mappings=[],
            source_exclusions=[],
            timeout_seconds=60,
            fbmcq_solver_timeout_ms=20_000,
            fbmcq_max_bound=5,
            fbmcq_process_wall_seconds=30.0,
        )
    return _ENV["env"]


def occupancy(source: str, cycles: int) -> bool:
    expr = (
        f'occupancy_after(source="{source}", trigger="Root.HS", '
        f'target="Root.Manual", within_cycles={cycles}) is True'
    )
    return env().eval_assert(expr, "eventless-completion regression").value


def test_the_event_is_observable_where_no_eventless_edge_competes():
    """Pins the half that already worked, so a fix cannot trade one for the other."""

    assert occupancy("Root.Auto.Settled", 1) is True


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Known defect, pinned before the fix so the fix has something to satisfy. "
        "strict=True on purpose: once the settle semantics land these XPASS and the "
        "suite fails until this marker is removed, so the record cannot go stale."
    ),
)
@pytest.mark.parametrize("source", ["Root.Auto.S1", "Root.Auto.S2", "Root.Auto"])
@pytest.mark.parametrize("cycles", [1, 2, 3, 9])
def test_an_eventless_completion_edge_must_not_swallow_the_event(source, cycles):
    """The obligation holds in this model; the predicate must not deny it.

    Parametrised over the horizon because the bug is not a horizon shortfall --
    every value fails, which is what rules out `within_cycles` as the remedy.
    """

    assert occupancy(source, cycles) is True, (source, cycles)
