"""Redaction must remove secrets without damaging the research record.

The pair-0029 run record has `[REDACTED]` in place of the model state paths of
23 of its 55 assertions.  No secret was involved: the JWT alternative in
`SECRET_VALUE_RE` was written as a bare three-segment shape, and a long FCSTM
path such as
`llms_emp_feedback_final_0029.CollisionAvoidance.collision_avoidance_deactive`
matches it.  That silently corrupts the evidence chain and makes those runs
impossible to replay.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.common.telemetry import redact  # noqa: E402

REAL_PATHS_FROM_PAIR_0029 = [
    "llms_emp_feedback_final_0029.CollisionAvoidance.collision_avoidance_deactive",
    "llms_emp_feedback_final_0029.CollisionAvoidance.collision_avoidance_active",
    "llms_emp_feedback_final_0029.UrbanMode.lane_change_urban",
    "llms_emp_feedback_final_0029.pedestrian_detected_dist_to_rear_5_vel_30",
]


def test_model_state_paths_survive_redaction() -> None:
    for path in REAL_PATHS_FROM_PAIR_0029:
        assert redact(path) == path, path
        assert redact({"expression": f'simulate(initial_state="{path}")'}) == {
            "expression": f'simulate(initial_state="{path}")'
        }


def test_real_secrets_are_still_removed() -> None:
    assert "[REDACTED]" in redact("sk-abcdefghijklmnopqrstuvwxyz012345")
    assert "[REDACTED]" in redact("Bearer abcdefghijklmnopqrstuvwxyz")
    jwt = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        ".eyJzdWIiOiIxMjM0NTY3ODkwIn0"
        ".dBjftJeZ4CVPmB92K27uhbUJU1p1r0W1gFWFOEjXk"
    )
    assert "[REDACTED]" in redact(jwt)


def test_secret_bearing_keys_are_still_masked_wholesale() -> None:
    masked = redact({"api_key": "whatever", "authorization": "x", "state_path": "Root.A.b"})
    assert masked["api_key"] == "[REDACTED]"
    assert masked["authorization"] == "[REDACTED]"
    assert masked["state_path"] == "Root.A.b"
