"""Scheduling contracts without providers or child processes."""

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from paper_stm_method.orchestration import runner
from paper_stm_judge import artifacts


def test_three_round_pools_wait_for_smoke_without_duplicate_cells(monkeypatch, tmp_path):
    script = Path(__file__).resolve().parents[2] / "discover_matrix/docs/generations/a3_20260910/run_batches.py"
    spec = importlib.util.spec_from_file_location("a3_batches", script)
    batches = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(batches)
    monkeypatch.setattr(runner, "FROZEN_PAIR_IDS", ("0000", "0001", "0002", "0003"))
    monkeypatch.setattr(artifacts, "adapt_evidence_discovery_release", lambda *a: ([], SimpleNamespace(source_hash="fixture"), 1, "fixture"))

    def write(path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data))

    smoke_judge = tmp_path / "smoke-judge"
    write(smoke_judge / "run_manifest.json", {"source_root": str(tmp_path / "old-smoke")})
    for pair in ("0000", "0001", "0002"):
        write(tmp_path / "sonnet/smoke-corrected/method" / pair / "round-1.json", {"eligible": True, "status": "completed"})
    active, launched, submitted = [], [], set()
    ticks = 0

    class Process:
        def __init__(self, kind, rnd):
            self.kind, self.round, self.pid = kind, rnd, len(launched) + 1
            self.returncode = None
            self.polls = 0

        def poll(self):
            self.polls += 1
            if self.polls >= 2:
                self.returncode = 0
                if self in active:
                    active.remove(self)
            return self.returncode

    def launch(command, log):
        kind = "method" if "paper_stm_method.cli" in command else "judge"
        value = lambda flag: command[command.index(flag) + 1]
        rnd = int(value("--round")) if "--round" in command else None
        workers = int(value("--workers"))
        assert workers == (16 if kind == "method" else 8)
        assert not any(p.kind == kind and (kind == "method" or p.round == rnd) for p in active)
        if kind == "judge" and rnd == 1:
            assert ticks >= 2, "r1 launched before the external smoke pool drained"
        directory = Path(value("--output-dir")) / value("--run-id")
        selected = [command[i+1] for i, flag in enumerate(command) if flag == "--pair-id"]
        model = "sonnet" if "sonnet" in directory.parts else "luna"
        if kind == "method":
            for pair in selected:
                for r in (rnd,) if rnd else (1, 2, 3):
                    write(directory / "method" / pair / f"round-{r}.json", {"eligible": True, "status": "completed"})
            write(directory / "summary.json", {"failed_pairs": []})
        else:
            for pair in selected:
                key = model, pair, rnd
                assert key not in submitted
                submitted.add(key)
                write(directory / "pairs" / f"{pair}.json", {"status": "completed"})
        process = Process(kind, rnd)
        active.append(process)
        launched.append(process)
        return process

    def sleep(seconds):
        nonlocal ticks
        ticks += 1
        if ticks == 2:
            for pair in ("0000", "0001", "0002"):
                write(smoke_judge / "pairs" / f"{pair}.json", {"status": "completed"})
        assert ticks < 50

    monkeypatch.setattr(batches, "launch", launch)
    monkeypatch.setattr(batches.time, "sleep", sleep)
    batches.run(tmp_path, smoke_judge)
    assert len(submitted) == 21
    assert {p.round for p in launched if p.kind == "judge"} == {1, 2, 3}


def test_tool_envelope_recovery_accepts_only_complete_first_payload(monkeypatch):
    directory = Path(__file__).resolve().parents[2] / "discover_matrix/docs/generations/a3_20260910"
    monkeypatch.syspath_prepend(str(directory))
    from recover_tool_envelope import recover_arguments

    value = {"basis": "Fixture", "reason": 'Original reason</reason>\n<parameter name="issues">[]'}
    result = recover_arguments(value)
    assert result.reason == "Original reason" and result.issues == []
    with pytest.raises(ValueError):
        recover_arguments({**value, "reason": value["reason"] + " trailing text"})
    with pytest.raises(AssertionError):
        recover_arguments({**value, "reason": "No parameter boundary"})


def test_content_counts_distinguish_reports_from_expected_units(monkeypatch):
    directory = Path(__file__).resolve().parents[2] / "discover_matrix/docs/generations/a3_20260910"
    monkeypatch.syspath_prepend(str(directory))
    from analyze_a3 import content_breakdown

    items = {e: {"pair": "0000", "L": "L1", "axes": {"defect_element": "transition"}, "summary": e}
             for e in ("shared", "lost", "gained")}

    def report(ids, validity="VALID_KNOWN", rnd=1):
        return {"round": rnd, "validity": validity, "full_ledger_ids": ids, "property": "reachability",
                "predicate_id": "R1", "witness_level": "W1", "published_claim": {"locus_kind": "transition"}}

    a3 = {"reports": [report(["shared", "gained"]), report(["shared"]), report(["lost"], "INVALID")]}
    full = {"reports": [report(["shared", "lost"]), report(["shared"], rnd=2)]}
    result = content_breakdown(a3, full, items)
    assert {k: len(v) for k, v in result["partitions"].items()} == {"shared": 1, "full_only": 2, "a3_only": 1}
    counts = result["axes"]["defect_element"]["transition"]
    assert counts["expected_round_units"] == 9
    assert counts["a3_hit_units"] == 2 and counts["full_hit_units"] == 3
    assert result["report_groups"]["a3"]["predicate_id"]["R1"] == {"VALID_KNOWN": 2, "INVALID": 1}
