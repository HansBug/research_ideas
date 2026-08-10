from __future__ import annotations

import json
import os
import time
from pathlib import Path

import pytest

from paper_stm_repair_loop.eval_env.fbmcq import FBMCQAPI, FBMCQTimeoutError


MODEL = """state Root {
    event go;
    state Idle;
    state Done;
    [*] -> Idle;
    Idle -> Done : go;
}
"""


def isolated_runner(_model_path: str, _query_path: str, **_kwargs):
    return json.dumps(
        {
            "result": {"status": "sat", "property_satisfied": True},
            "property": {"kind": "reach", "bound": 2},
            "replay": {"ok": True},
            "child_pid": os.getpid(),
        }
    ), 0


def large_report_runner(_model_path: str, _query_path: str, **_kwargs):
    return json.dumps(
        {
            "result": {"status": "sat", "property_satisfied": True},
            "property": {"kind": "reach", "bound": 2},
            "replay": {"ok": True},
            "witness": "x" * (2 * 1024 * 1024),
        }
    ), 0


def sleeping_runner(_model_path: str, _query_path: str, **_kwargs):
    while True:
        time.sleep(1)


def pid_file_sleeping_runner(_model_path: str, query_path: str, **_kwargs):
    pid_file = Path(query_path).with_name("child.pid")
    pid_file.write_text(str(os.getpid()), encoding="utf-8")
    while True:
        time.sleep(1)


def test_fbmcq_runner_executes_in_spawned_child_process():
    obs = FBMCQAPI(MODEL, bmc_runner=isolated_runner).fbmcq(
        'check reach <= 2: active("Root.Done");'
    )

    assert obs.raw["child_pid"] != os.getpid()
    assert obs.process_isolation == "multiprocessing_spawn"


def test_fbmcq_has_no_parent_wall_countdown_when_timeout_is_not_explicit():
    started = time.monotonic()
    obs = FBMCQAPI(
        MODEL, process_wall_seconds=None, bmc_runner=isolated_runner
    ).fbmcq(
        'check reach <= 2: active("Root.Done");'
    )

    assert obs.holds is True
    assert time.monotonic() - started < 5


def test_fbmcq_large_child_report_does_not_deadlock_before_parent_read():
    obs = FBMCQAPI(
        MODEL,
        process_wall_seconds=5,
        bmc_runner=large_report_runner,
    ).fbmcq('check reach <= 2: active("Root.Done");')

    assert obs.holds is True
    assert len(obs.raw["witness"]) == 2 * 1024 * 1024


def test_fbmcq_explicit_timeout_terminates_kills_joins_and_reports_metadata():
    started = time.monotonic()
    with pytest.raises(FBMCQTimeoutError) as excinfo:
        FBMCQAPI(
            MODEL,
            timeout_ms=100,
            process_wall_seconds=0.1,
            bmc_runner=pid_file_sleeping_runner,
        ).fbmcq(
            'check reach <= 2: active("Root.Done");'
        )

    assert time.monotonic() - started < 5
    metadata = excinfo.value.metadata
    assert metadata["inconclusive_kind"] == "timeout"
    assert metadata["process_wall_seconds"] == 0.1
    assert metadata["process_joined"] is True
    assert metadata["process_alive_after_join"] is False
    child_pid = metadata.get("child_pid")
    if child_pid is not None:
        try:
            os.kill(int(child_pid), 0)
        except ProcessLookupError:
            pass
        else:  # pragma: no cover - failure branch documents no residual child
            raise AssertionError(f"FBMCQ child process still exists: {child_pid}")
