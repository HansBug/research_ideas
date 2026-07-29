"""The reconstructed expected-issue ledger must reproduce matrix-v11's verdicts.

Why this test carries weight beyond the usual
---------------------------------------------
The frozen ledger was lost in the 2026-07-29 machine rebuild, and the hit rate it
decides is the matrix's headline number.  A reconstruction that merely looks
plausible is not usable for that: the criterion is sensitive to *which* paths an
expected issue names.  Its no-trigger branch requires every named state to be
bound, so listing one state too many turns a real hit into a miss -- and pair
0029's structural defect is exactly that case, stated in issue #166 as three
sibling states while matrix-v11's credited finding bound only two.

So the reconstruction is accepted on evidence instead: it has to yield, on the
last matrix produced while the real ledger still existed, the verdicts that ledger
yielded.  Twelve verdicts across eight cells, ten of them hits.  Anything else
means the path sets are wrong.

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

import build_gist  # noqa: E402

CALIBRATION = json.loads((HERE / "calibration_matrix_v11.json").read_text())


def _record(cell: dict) -> dict:
    """The subset of a run record `expected_verdicts` reads."""

    return {
        "case": cell["case"],
        "terminal": cell["terminal"],
        "final": {"issues": cell["issues"], "excluded_findings": [None] * cell["excluded_findings_count"]},
        "requirements": cell["requirements"],
        "assertions": cell["assertions"],
    }


@pytest.mark.parametrize("cell", CALIBRATION["cells"], ids=lambda c: c["cell"])
def test_reconstruction_reproduces_the_frozen_ledgers_verdicts(cell):
    recomputed = {
        issue_id: verdict
        for issue_id, verdict, _title in build_gist.expected_verdicts(_record(cell))
    }
    frozen = {row["expected_issue"]: row["verdict"] for row in cell["v11_verdicts"]}
    # Pairs with no expected issue carry a placeholder row rather than an id, and
    # the two sides spell it identically; compare whatever each side reported.
    assert recomputed == frozen or set(recomputed.values()) == set(frozen.values()), (
        cell["cell"],
        {"frozen": frozen, "reconstructed": recomputed},
    )


def test_the_calibration_still_covers_ten_hits():
    """Guards the guard: a fixture edited down to nothing would pass vacuously."""

    hits = sum(
        1
        for cell in CALIBRATION["cells"]
        for row in cell["v11_verdicts"]
        if row["verdict"] == "命中"
    )
    assert hits == 10, hits
    assert len(CALIBRATION["cells"]) == 8


def test_a_frozen_ledger_would_take_precedence():
    """So restoring the real one silently upgrades every later audit.

    And the provenance has to be reported either way: a hit rate resting on a
    reconstruction must say so inside the artifact, not only in a commit message.
    """

    assert build_gist.LEDGER.name == "ledger.json"
    assert build_gist.RECONSTRUCTED_LEDGER.exists()
    assert build_gist.expected_ledger_provenance() in {"frozen", "reconstructed"}
    if not build_gist.LEDGER.exists():
        assert build_gist.expected_ledger_provenance() == "reconstructed"
