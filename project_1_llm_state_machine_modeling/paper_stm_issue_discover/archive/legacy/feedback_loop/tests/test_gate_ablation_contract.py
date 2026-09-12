"""The ablation switch must fail loudly, and must cover every gate it claims to.

Two generations wired `DISCOVER_ABLATE_GATES` into two of the seven `step_findings` gates by
hand. A cell run with the switch set was then reported as an unaided baseline -- it was not one,
because five gates were still live, and no artifact recorded which. The number published from
that cell (`0/1/0`) was read as "the finding is unreachable without gates" when what it showed
was "the finding is unreachable without five gates".

Two failure shapes are guarded here:

1. A gate that exists but is not ablatable. `ABLATABLE_GATES` is the enumeration the run record
   writes, so a gate missing from it is a gate whose ablation silently does nothing.
2. A misspelled name. `DISCOVER_ABLATE_GATES=trigger_consuimng` used to start a fully gated run
   that a shell history would describe as an ablation. This is the same shape as the two silent
   degradations already found in this project -- a predicate tie-breaker disabled by a swallowed
   `ImportError`, and a fabrication scanner reading zero input files. Both returned a plausible
   value on misconfiguration instead of failing, and both published a wrong number for several
   generations. A misconfiguration that cannot be distinguished from success is the defect.
"""

from __future__ import annotations

import importlib
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover import nodes  # noqa: E402

#: Every gate the report and the PR comments describe as ablatable. Written out rather than
#: derived from the module, so adding a gate without adding it here fails.
EXPECTED_GATES = {
    "initialization_anchored",
    # v23 接线。它在 v22 就写好了（`capability.vacuous_containment_findings`），却只在
    # `nodes.py` 里当死导入放着 —— 因为它要求 `source_context.nl_parent`，而当时没有任何 prompt
    # 描述过这个字段，接线会让生产者被要求补一个它没被教过的东西，耗尽修复预算后整格隔离。
    # v23 先在 splitter prompt 里教了该字段，再接线。
    "vacuous_containment",
    "termination_proposal",
    "redundant_proposal",
    "root_anchored",
    "projection_anchored",
    "conceded_omission",
    "trigger_consuming",
    "source_blind_response",
    # v36 接线。它与其余门方向相反：其余门**拒绝**一类需求，这道门检查一份**申报**是否成立。
    # 由来是 splitter 与 requirement reviewer 的直接冲突 —— splitter 侧的入口义务触发器自陈
    # 「is mechanical: it does not depend on recognising a phrasing」，reviewer 侧的常设指令是
    # 「无 NL 出处即语义添加」，而 reviewer 看不到那条触发器；实测 0032 删 3/4 格、0047 删 5/6 格。
    #
    # ⚠️ 消融它的含义因此也相反：关掉它不是「少一道拒绝」，而是**派生申报不再被核验** ——
    # 一条声称派生的需求会带着未核验的 parent 与 scope 进入下游。做消融基线时要按这个方向读。
    "derivation_contract",
}


def test_every_gate_the_report_names_is_ablatable() -> None:
    assert set(nodes.ABLATABLE_GATES) == EXPECTED_GATES


def test_the_step_findings_gates_are_all_present() -> None:
    """`step_findings` is the block the coverage number is produced by; all of them must be here.

    数量从 7 变 8（v23 接线 `vacuous_containment`）。这里写活数而不是写死 8，因为把数字钉在测试里
    会让下一次接线看起来像「测试坏了」而不是「契约变了」—— 真正要守的是**两侧一致**：
    `ABLATABLE_GATES` 与报告里出现的门名不能有一方多出一项。
    """
    step_gates = EXPECTED_GATES - {"source_blind_response"}
    assert step_gates
    assert step_gates <= set(nodes.ABLATABLE_GATES)


def test_no_gate_is_ablated_by_default() -> None:
    """A normal run must be unaffected, or every published cell is an accidental ablation."""
    if os.environ.get("DISCOVER_ABLATE_GATES"):
        return  # the suite itself was launched with an ablation; nothing to assert
    assert nodes._ABLATED_GATES == frozenset()
    assert all(not nodes._ablated(name) for name in nodes.ABLATABLE_GATES)


def test_a_known_name_switches_exactly_that_gate_off() -> None:
    env = dict(os.environ, DISCOVER_ABLATE_GATES="root_anchored,conceded_omission")
    code = (
        "from paper_stm_feedback_loop.discover import nodes;"
        "print(sorted(nodes._ABLATED_GATES));"
        "print(nodes._ablated('root_anchored'), nodes._ablated('trigger_consuming'))"
    )
    done = subprocess.run(
        [sys.executable, "-c", code],
        env={**env, "PYTHONPATH": str(SRC)},
        capture_output=True,
        text=True,
    )
    assert done.returncode == 0, done.stderr
    assert "['conceded_omission', 'root_anchored']" in done.stdout
    assert "True False" in done.stdout


def test_a_misspelled_gate_name_refuses_to_start() -> None:
    """The whole point: an ablation that does nothing must not look like an ablation."""
    env = dict(os.environ, DISCOVER_ABLATE_GATES="trigger_consuimng")
    done = subprocess.run(
        [sys.executable, "-c", "from paper_stm_feedback_loop.discover import nodes"],
        env={**env, "PYTHONPATH": str(SRC)},
        capture_output=True,
        text=True,
    )
    assert done.returncode != 0
    assert "do not exist" in done.stderr
    assert "trigger_consuimng" in done.stderr


def test_asking_about_an_unknown_gate_at_a_call_site_is_an_error() -> None:
    """A typo in `_ablated("...")` would otherwise read as "this gate is never ablated"."""
    try:
        nodes._ablated("no_such_gate")
    except ValueError as exc:
        assert "unknown gate name" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("_ablated accepted a name that is not a gate")


def test_the_module_reloads_cleanly_so_the_checks_above_are_not_import_order_artifacts() -> None:
    importlib.reload(nodes)
    assert set(nodes.ABLATABLE_GATES) == EXPECTED_GATES


def test_every_incomplete_reconciliation_key_forces_partial_coverage() -> None:
    """The only defence against a lossy run reading as a complete pass has to be tested.

    C1 made three gates non-fatal: a structural defect in one finding now discards that finding
    and marks the cell `partial`, instead of killing the run. `partial` is therefore the *sole*
    signal that something was dropped — and nothing asserted it. A refactor could quietly remove
    any key from `INCOMPLETE_RECONCILIATION_KEYS` and every other test would still pass, at
    which point a cell that discarded findings would report `full`.
    """
    from paper_stm_feedback_loop.discover.nodes import (
        INCOMPLETE_RECONCILIATION_KEYS,
        coverage_status_of,
    )

    assert coverage_status_of((), {}) == "full"
    assert coverage_status_of((), {k: () for k in INCOMPLETE_RECONCILIATION_KEYS}) == "full"
    for key in INCOMPLETE_RECONCILIATION_KEYS:
        assert coverage_status_of((), {key: ({"any": "residue"},)}) == "partial", (
            f"a non-empty {key!r} must make the cell partial; without it a run that dropped "
            "a finding is indistinguishable from one that found everything"
        )


def test_report_and_publish_share_one_coverage_owner() -> None:
    """Two formulas for the same field is how the markdown says `full` and the JSON says `partial`."""
    import inspect

    from paper_stm_feedback_loop.discover import report

    src = inspect.getsource(report)
    assert "coverage_status_of" in src, "report.py must use the shared owner, not its own formula"
    assert "blocks_full_coverage for gap in coverage_gaps" not in src, (
        "report.py still computes coverage_status itself"
    )
