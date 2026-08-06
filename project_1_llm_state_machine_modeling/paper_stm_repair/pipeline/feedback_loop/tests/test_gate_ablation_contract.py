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
    "termination_proposal",
    "redundant_proposal",
    "root_anchored",
    "projection_anchored",
    "conceded_omission",
    "trigger_consuming",
    "source_blind_response",
}


def test_every_gate_the_report_names_is_ablatable() -> None:
    assert set(nodes.ABLATABLE_GATES) == EXPECTED_GATES


def test_the_seven_step_findings_gates_are_all_present() -> None:
    """`step_findings` is the block the coverage number is produced by; all seven must be here."""
    step_gates = EXPECTED_GATES - {"source_blind_response"}
    assert len(step_gates) == 7
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
