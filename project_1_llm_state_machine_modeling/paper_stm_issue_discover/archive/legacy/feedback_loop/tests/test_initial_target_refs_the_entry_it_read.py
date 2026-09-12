"""`initial_target` decides False by reading the default entry, then does not
declare it -- so attribution cannot see that the False is a converter artifact.

Found in matrix-v16's published output.  0029-claude published
"HighwayMode 的初始子状态不是 enter_hwy" and "UrbanMode 的初始子状态不是
enter_urban" as confirmed issues, both attributed `safe` with
`source_refs = {HighwayMode, HighwayMode.enter_hwy}` and no exclusions.  Neither
is a defect of the authored model.  The converter gives every composite that has
a cross-boundary transition a synthetic default entry:

    state UnspecifiedInitial named "Unspecified initial";
    [*] -> enter_hwy : if [R45RouteToken == 5] ...;   # the authored route
    [*] -> UnspecifiedInitial;                        # synthetic, unconditional

`UnspecifiedInitial` is listed in the pair's `attribution_exclusions`, so an
assertion resting on it is representation debt by policy and must not be
published.  But the predicate never says it rested on it: it answers False
*because* the unconditional entry targets `UnspecifiedInitial`, and reports refs
covering only the composite and the child that was asked about.  Attribution has
no exclusion to match, marks the binding `safe`, and a fabricated defect reaches
the issue list.

The refs contract is the predicate's job, and the class docstring says so: "the
predicate is the only thing that knows: it chose the query".  A False that hinges
on an element it will not name cannot be filtered by anything downstream.

Two facts pin the diagnosis rather than one, since either alone has an innocent
reading: the sibling call naming the synthetic state answers True, and the failing
call's refs omit the very state that made it fail.
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.assertions import build_eval_environment  # noqa: E402

#: The converter's lowering, reduced to one composite: an authored entry behind a
#: route-token guard plus the synthetic unconditional default.
MODEL = """\
def int Token = 0;
state Root named "Root" {
    event go named "go";
    state Mode named "Mode" {
        state Authored named "Authored";
        state Synthetic named "Unspecified initial";
        [*] -> Authored : if [Token == 5] effect { Token = 0; };
        [*] -> Synthetic;
        Synthetic -> [*] : /go effect { Token = 5; };
    }
    state Idle named "Idle";
    [*] -> Idle;
    Idle -> Mode : /go;
}
"""

_ENV: dict[str, object] = {}


def env():
    if "env" not in _ENV:
        _ENV["env"] = build_eval_environment(
            model_text=MODEL,
            source_mappings=[],
            # The real runs pass the converter's exclusion list; the refs contract
            # this pins is independent of it, so keep the environment minimal.
            source_exclusions=[],
            timeout_seconds=60,
            fbmcq_solver_timeout_ms=20_000,
            fbmcq_max_bound=5,
            fbmcq_process_wall_seconds=30.0,
        )
    return _ENV["env"]


def call(child: str):
    expr = f'initial_target(composite="Root.Mode", child="Root.Mode.{child}") is True'
    result = env().eval_assert(expr, "initial_target refs regression")
    return result.value, tuple(result.function_call_trace[0].model_refs or ())


def test_the_synthetic_default_entry_is_what_makes_the_call_false():
    """Establishes the premise: the False is about `Synthetic`, not about `Authored`."""

    assert call("Authored")[0] is False
    assert call("Synthetic")[0] is True


def test_a_false_initial_target_declares_the_entry_that_decided_it():
    """Otherwise attribution cannot tell a real defect from a lowering artifact.

    Asserted on the refs rather than on the attribution status because refs are
    where the omission is: `bind_attribution` already matches exclusions against
    whatever the predicate reports, and reports nothing to match here.
    """

    value, refs = call("Authored")
    assert value is False
    assert any("Synthetic" in ref for ref in refs), refs


# --- the same omission on the single-entry branch ---------------------------------
#
# The fix above landed only on the branch that resolves a unique *unconditional*
# entry among several.  The branch that returns immediately because there is only
# one entry at all kept returning without noting it -- and that is the common case:
# 25 of the 60-pair corpus's composites across 18 pairs take it, against 10 for the
# multi-entry branch.
#
# The visible damage was an inconsistency in the expected-issue ledger that read as
# reviewer discretion.  Pair 0019's `CollisionAvoidanceSystem` was accepted as a real
# missing-initial-edge defect; pair 0029's `HighwayMode` -- same shape, same synthetic
# entry, same exclusion list -- was excluded as representation debt.  0029 has five
# entries and went through the noting branch, so attribution saw the artifact and
# filtered it.  0019, 0043 and 0053 have exactly one and went through this branch, so
# attribution saw nothing and marked them `safe`.  Same evidence, two answers, decided
# by which branch the model's shape happened to select.

SINGLE_ENTRY_MODEL = """\
def int Token = 0;
state Root named "Root" {
    event go named "go";
    state Mode named "Mode" {
        state Wanted named "Wanted";
        state Synthetic named "Unspecified initial";
        [*] -> Synthetic;
        Synthetic -> [*] : /go effect { Token = 5; };
    }
    state Idle named "Idle";
    [*] -> Idle;
    Idle -> Mode : /go;
}
"""

_SINGLE: dict[str, object] = {}


def single_env():
    if "env" not in _SINGLE:
        _SINGLE["env"] = build_eval_environment(
            model_text=SINGLE_ENTRY_MODEL,
            source_mappings=[],
            source_exclusions=[],
            timeout_seconds=60,
            fbmcq_solver_timeout_ms=20_000,
            fbmcq_max_bound=5,
            fbmcq_process_wall_seconds=30.0,
        )
    return _SINGLE["env"]


def single_call(child: str):
    expr = f'initial_target(composite="Root.Mode", child="Root.Mode.{child}") is True'
    result = single_env().eval_assert(expr, "initial_target single-entry refs regression")
    return result.value, tuple(result.function_call_trace[0].model_refs or ())


def test_the_lone_synthetic_entry_is_what_makes_the_single_entry_call_false():
    """Premise for the test below: `Mode` declares exactly one entry, the synthetic one."""

    assert single_call("Wanted")[0] is False
    assert single_call("Synthetic")[0] is True


def test_a_false_from_the_single_entry_branch_also_declares_its_entry():
    """The common branch needs the refs contract as much as the multi-entry one.

    Without this, a False that rests entirely on a converter-synthesised entry is
    indistinguishable from a False that rests on the authored model, on 25 of the
    corpus's composites.
    """

    value, refs = single_call("Wanted")
    assert value is False
    assert any("Synthetic" in ref for ref in refs), refs
