"""L1 replay harness: rerun a recorded run's producer outputs at zero cost.

Verifying a control-flow change used to require a real matrix run.  For pair
0029 that was ~95 minutes and 1.66M tokens to answer a question the recorded
artifacts already contain: given the same producer outputs, where does the
graph go now?
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover.replay import (  # noqa: E402
    RecordedCall,
    ReplayResponder,
    load_recorded_calls,
)
from paper_stm_feedback_loop.discover.schemas import (  # noqa: E402
    AssertionReview,
    RequirementReview,
    RequirementSet,
)


def _calls() -> list[RecordedCall]:
    return [
        RecordedCall(
            sequence=0,
            role="requirement_splitter",
            revision=1,
            parsed_output={
                "revision": 1,
                "requirements": [
                    {
                        "requirement_id": "REQ-001",
                        "statement": "Recorded requirement.",
                        "verification_kind": "structure",
                    }
                ],
                "segment_disposition": {"NL-L001": "covered"},
            },
        ),
        RecordedCall(
            sequence=1,
            role="requirement_reviewer",
            revision=1,
            parsed_output={
                "decision": "accept",
                "reviewed_revision": 1,
                "rationale": "Recorded acceptance.",
            },
        ),
    ]


def test_recorded_outputs_are_replayed_in_order() -> None:
    responder = ReplayResponder(calls=_calls())
    first = responder.invoke_structured(
        role="x", schema=RequirementSet, system_prompt="", user_input=""
    )
    assert first.requirements[0].requirement_id == "REQ-001"
    review = responder.invoke_structured(
        role="x", schema=RequirementReview, system_prompt="", user_input=""
    )
    assert review.decision == "accept"
    assert responder.summary()["consumed"]["requirement_splitter"] == 1


def test_roles_the_recording_never_reached_are_synthesized_and_counted() -> None:
    """A recorded run that died early has no reviewer output to replay.

    Progressing past that point is the *expected* outcome of an isolation fix,
    so the harness must not treat it as an error -- but it must label it, or a
    replay result could be misread as covered by the recording.
    """

    responder = ReplayResponder(calls=_calls())
    review = responder.invoke_structured(
        role="x", schema=AssertionReview, system_prompt="", user_input=""
    )
    assert review.decision == "accept"
    assert "SYNTHETIC" in review.rationale
    assert responder.summary()["synthesized"] == {"assertion_reviewer": 1}


def test_strict_mode_refuses_to_invent_a_missing_role() -> None:
    responder = ReplayResponder(calls=_calls(), allow_synthetic=False)
    with pytest.raises(LookupError):
        responder.invoke_structured(
            role="x", schema=AssertionReview, system_prompt="", user_input=""
        )


def test_load_recorded_calls_reads_an_immutable_record_tree(tmp_path: Path) -> None:
    record_dir = tmp_path / "L000-000005-requirement-splitter-llm-call-completed"
    record_dir.mkdir(parents=True)
    (record_dir / "record.json").write_text(
        json.dumps(
            {
                "role": "requirement_splitter",
                "revision": 1,
                "parsed_output": {"revision": 1, "requirements": []},
            }
        ),
        encoding="utf-8",
    )
    calls = load_recorded_calls(tmp_path)
    assert [c.role for c in calls] == ["requirement_splitter"]
