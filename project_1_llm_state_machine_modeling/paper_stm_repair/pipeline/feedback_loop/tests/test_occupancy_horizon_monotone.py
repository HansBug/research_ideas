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

## The first fix was wrong in the mirror direction, and this file could not see it

Scanning *every* cycle — the obvious reading of "within" — makes the predicate
return True when the machine was **already** in the target and the trigger *took
it away*. `_simulate` builds `[settle...] + [[trigger]] + [[]...]`, so cycle 0 is
the configuration *before* the trigger was offered. Measured on pair 0006:

    Attack --Attack_Complete--> AttackingTarget
      cycle 0: [..., Attack, AttackingTarget]   <- before the trigger
      cycle 1: [..., Searching]                 <- after it

Ten of eleven pairs had such flips, all False->True, i.e. **findings eaten**.

**And every assertion in the first version of this file passed anyway** — because
they only fail when the implementation answers False too often. A monotonicity
identity is satisfied by `return True`. So the file was single-sided: it could
never catch the mirror error, which is why 1594 tests went green on a change that
ate findings in ten pairs.

That is the reason `test_trigger_must_move_the_machine_there` below exists. A
one-sided acceptance criterion is not an acceptance criterion; it is a way of
confirming what you already believe.

`_HORIZON_PROBE` cannot catch this either: it searches only *upward*
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


#: Calls whose correct answer is **False**: the machine is already inside the
#: target at cycle 0 and the trigger moves it out. Pinned as a pair to the
#: monotonicity tests above -- those can only fail on too many Falses, these can
#: only fail on too many Trues, and the implementation has to satisfy both.
MUST_BE_FALSE = (
    ("0006", "UAVSwarmStateMachine.Attack", "Attack_Complete",
     "UAVSwarmStateMachine.Attack.AttackingTarget"),
)


@pytest.mark.parametrize("pair,source,trigger,target", MUST_BE_FALSE)
def test_trigger_must_move_the_machine_there(
    pair: str, source: str, trigger: str, target: str
) -> None:
    """A trigger that *leaves* the target does not count as occupying it.

    This is the half the first version of this file was missing. `occupancy_after`
    asks about "after the trigger", so ordering is part of the proposition: a
    window that starts before the trigger lands turns "it took the machine away"
    into "it is there".
    """

    env = _api(pair)
    prefix = f"llms_emp_feedback_final_{pair}."
    values = [
        env.predicates.occupancy_after(
            source=prefix + source,
            trigger=prefix + trigger,
            target=prefix + target,
            within_cycles=cycles,
        )
        for cycles in (1, 2, 4)
    ]
    assert not any(values), (
        f"occupancy_after credited a trigger that moved the machine *out* of "
        f"{target}: {dict(zip((1, 2, 4), values))}. Cycle 0 is the configuration "
        "before the trigger was offered; the scan window must start where the "
        "trigger was consumed."
    )


@pytest.mark.parametrize("pair", ["0000", "0006", "0029"])
def test_hit_frame_is_never_before_the_trigger_frame(pair: str) -> None:
    """第二条恒等式：命中帧的下标必须 ≥ 触发被消费的帧下标。

    单调性（上面那两个测试）对错误实现同样成立 —— settle / cold-start 前缀的长度**与 c 无关**，
    所以「扫全部帧」产生的假阳性在**每一个** c 上都是 True，天然满足单调不减，也天然绕过
    `_HORIZON_PROBE`（它只向上搜）。

    换言之：一条只查单调性的验收判据**无法把正确修法与错误修法区分开**。这一条补的正是那个缺口 ——
    它直接检查窗口的起点，而起点是错误实现与正确实现唯一的差别。

    选这三个 pair 是因为它们都有 `settle > 0` 的 composite 源（全语料 217/627 = 34.6% 的可 pin 配置
    如此），而那正是假阳性的来源面。

    ⚠️ **三个都是本项目迭代所用的格。** 首版曾把某个格当作样本外证据，构造纪律当场
    拦下（`FAIL held-out pairs have since been named`）。它的两条记录其实早已烧毁，所以那次点名不损失
    任何可报记录 —— 但检查器**按 pair 判、不看记录状态**，这是对的：动机是自述的，点名是可查的。

    我选它的理由（有 `settle > 0` 的 composite 源）是通用技术性质，与该样本的任何缺陷无关。**但
    「理由通用」不构成豁免。** 正确处置是换 pair 而不是登记烧毁 —— 该性质在 34.6% 的配置上成立，
    调优格里必然有，所以换掉的代价是零。
    """

    env = _api(pair)
    api = env.predicates
    states = [row.path for row in api.structure.states()][:10]
    events = [row.qualified_name for row in api.structure.events()][:3]

    violations = []
    probes = 0
    for source in states:
        for trigger in events:
            try:
                view = api._simulate(source=source, trigger=trigger, cycles=4)
            except Exception:
                continue
            cycles = list(getattr(view, "cycles", ()) or ())
            fired = next(
                (
                    index
                    for index, cycle in enumerate(cycles)
                    if trigger in (getattr(cycle, "consumed_events", ()) or ())
                ),
                None,
            )
            if fired is None:
                continue
            # 只出现在触发帧**之前**的状态，不得被判为「触发之后占据」。
            before = {
                str(item)
                for cycle in cycles[:fired]
                for item in (getattr(cycle, "active_states", ()) or ())
            }
            after = {
                str(item)
                for cycle in cycles[fired:]
                for item in (getattr(cycle, "active_states", ()) or ())
            }
            for target in before - after:
                if target not in states:
                    continue
                probes += 1
                try:
                    hit = api.occupancy_after(
                        source=source, trigger=trigger, target=target, within_cycles=4
                    )
                except Exception:
                    # 拒答不是有序性问题；但它**不能**让这一格静默消失，否则一道新门就能把
                    # 整条验收变成空过。所以 probes 已在上面计数。
                    continue
                if hit:
                    violations.append((source, trigger, target))

    # 空过护栏：这条测试的鉴别力来自「只在触发前出现过的状态」这一探测面，实测 0000→3 / 0006→7 /
    # 0029→2。将来任何拒绝这些 source 的门（扩大 `_reject_transient_subject`、composite pin 拒绝
    # 路径等）都会让探测面归零，而**零违规与零探测在断言上不可区分** —— 那时这条验收会静默变绿。
    #
    # 这与第一轮 I-3 是同一型错误：判据看起来通过了，实际是没有被行使。
    assert probes >= 1, (
        f"{pair} 上没有任何可探测的 (source, trigger, target)：探测面已归零，这条验收未被行使。"
        "空过与通过不可区分，所以这是错误而不是通过。"
    )
    assert not violations, (
        f"{len(violations)} 处命中发生在触发帧之前（{pair}）：{violations[:3]}。"
        "occupancy_after 问的是「触发**之后**」，所以扫描窗口必须从触发被消费的那一帧开始。"
    )
