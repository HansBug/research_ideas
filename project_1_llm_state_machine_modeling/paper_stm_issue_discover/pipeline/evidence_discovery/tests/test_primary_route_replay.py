"""Regression tests for the provider-free primary-route A/B cohort boundary."""

from __future__ import annotations

import pytest

from pipeline.evidence_discovery.route_replay import _predicate_null_evidence_rows


def _record(obligation_id: str, predicate_id: str | None, witness_level: str) -> dict[str, object]:
    """Build one minimal historical evidence row for cohort-selection coverage."""

    return {
        "obligation_id": obligation_id,
        "plan": {"predicate_id": predicate_id},
        "witness_level": witness_level,
    }


def test_primary_route_replay_targets_only_final_predicate_null_w1_evidence() -> None:
    """Auxiliary execute candidates and W0/null rows cannot inflate the 88-style cohort."""

    selected = _predicate_null_evidence_rows(
        {
            "evidence_records": [
                _record("fixture:null-w1", None, "W1"),
                _record("fixture:null-w0", None, "W0"),
                _record("fixture:s2-w1", "S2", "W1"),
                _record("fixture:null-w2", None, "W2"),
            ]
        }
    )

    assert list(selected) == ["fixture:null-w1"]
    assert selected["fixture:null-w1"][0] == 0


def test_primary_route_replay_rejects_duplicate_final_evidence_identity() -> None:
    """A source run cannot silently count one final predicate-null obligation twice."""

    with pytest.raises(ValueError, match="duplicate predicate-null W1 evidence"):
        _predicate_null_evidence_rows(
            {
                "evidence_records": [
                    _record("fixture:duplicate", None, "W1"),
                    _record("fixture:duplicate", None, "W1"),
                ]
            }
        )
