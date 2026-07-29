"""A table is what gets quoted, so its numbers have to refuse to mislead.

The specific failure this guards: an unfinished cell has zero published issues
because it never got to publish any.  Printing that zero next to a previous run's
count reads as "the false positive is gone", which is exactly the claim this whole
round is trying to establish -- so it is the one number that must not be faked by
omission.  `check_false_positives.py` already refuses the same inference; the table
has to refuse it too, and more firmly, because a reader sees the table first.

Run:
    PYTHONPATH=<repo root> pytest project_1_llm_state_machine_modeling/eval/discover_matrix
"""

from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import report_tables  # noqa: E402


def _bundle(tmp_path, cells):
    for cell in cells:
        record = {
            "pair": cell["pair"],
            "profile": cell["profile"],
            "terminal": cell["terminal"],
            "requirements": [{}] * cell.get("requirements", 0),
            "assertions": [{}] * cell.get("assertions", 0),
            "expected_issue_verdicts": cell.get("verdicts", []),
            "expected_ledger_provenance": "reconstructed",
            "telemetry": {"llm_calls": 3, "node_elapsed_ms": 600000},
            "terminal_artifact": {
                "issues": [{}] * cell.get("issues", 0),
                "excluded_findings": [{}] * cell.get("excluded", 0),
                "satisfied_requirement_ids": ["R"] * cell.get("satisfied", 0),
            },
        }
        name = f"{cell['pair']}-{cell['profile']}-audit.json"
        (tmp_path / name).write_text(json.dumps(record))
    return tmp_path


def test_an_unfinished_cell_shows_no_counts_at_all(tmp_path):
    """Its zero is an artefact of not finishing, not a result."""

    current = _bundle(
        tmp_path / "now",
        [{"pair": "0050", "profile": "gpt-5.5", "terminal": "missing", "issues": 0}],
    ) if (tmp_path / "now").mkdir() or True else None
    previous = _bundle(
        tmp_path / "before",
        [{"pair": "0050", "profile": "gpt-5.5", "terminal": "completed", "issues": 1}],
    ) if (tmp_path / "before").mkdir() or True else None

    cells = report_tables._cells(current)
    prior = {report_tables._short(c): c for c in report_tables._cells(previous)}
    table = report_tables.per_cell_table(cells, prior)

    row = [line for line in table.splitlines() if "0050-gpt" in line][0]
    assert "| — |" in row, row
    # And specifically not the comparison that would read as an improvement.
    assert "前轮 1" not in row, row


def test_a_finished_cell_does_carry_the_comparison(tmp_path):
    """Otherwise the guard would hide the real improvement too."""

    (tmp_path / "now").mkdir()
    (tmp_path / "before").mkdir()
    current = _bundle(
        tmp_path / "now",
        [{"pair": "0050", "profile": "gpt-5.5", "terminal": "completed", "issues": 0}],
    )
    previous = _bundle(
        tmp_path / "before",
        [{"pair": "0050", "profile": "gpt-5.5", "terminal": "completed", "issues": 1}],
    )
    cells = report_tables._cells(current)
    prior = {report_tables._short(c): c for c in report_tables._cells(previous)}
    row = [
        line
        for line in report_tables.per_cell_table(cells, prior).splitlines()
        if "0050-gpt" in line
    ][0]
    assert "0 (前轮 1)" in row, row


def test_the_rollup_says_so_when_a_cell_did_not_finish(tmp_path):
    """A hit rate over an incomplete matrix is not the matrix's hit rate."""

    (tmp_path / "b").mkdir()
    bundle = _bundle(
        tmp_path / "b",
        [
            {
                "pair": "0000", "profile": "gpt-5.5", "terminal": "completed",
                "verdicts": [{"expected_issue": "EXP-0000-IT-001", "verdict": "命中"}],
            },
            {
                "pair": "0029", "profile": "gpt-5.5", "terminal": "missing",
                "verdicts": [{"expected_issue": "EXP-0029-GC-001", "verdict": "run 未完成"}],
            },
        ],
    )
    rollup = report_tables.verdict_rollup(report_tables._cells(bundle))
    assert "本轮有未完成格子" in rollup
    assert "0029-gpt" in rollup
    assert "不是完整结果" in rollup


def test_a_missing_scan_is_not_reported_as_clean(tmp_path):
    (tmp_path / "empty").mkdir()
    text = report_tables.fabrication_section(tmp_path / "empty")
    assert "不得读作干净结果" in text


def test_a_failed_scan_is_not_reported_as_clean(tmp_path):
    (tmp_path / "failed").mkdir()
    (tmp_path / "failed" / "_fabrication_scan.json").write_text(
        json.dumps({"error": "RuntimeError: corpus gone", "cells_scanned": ["a", "b"]})
    )
    text = report_tables.fabrication_section(tmp_path / "failed")
    assert "捏造扫描失败" in text
    assert "不得读作干净结果" in text
