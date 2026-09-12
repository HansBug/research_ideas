from summarize import _quality


def test_quality_preserves_hit_and_false_positive_ids() -> None:
    judgement = {
        "judgement": {
            "ledger_assessments": [
                {
                    "ledger_id": "L-02",
                    "baseline_run1": {"hit": False},
                    "method_run1": {"hit": True},
                },
                {
                    "ledger_id": "L-01",
                    "baseline_run1": {"hit": True},
                    "method_run1": {"hit": True},
                },
            ],
            "emission_assessments": [
                {
                    "cell": "method_run1",
                    "emitted_id": "M-02",
                    "false_positive": True,
                },
                {
                    "cell": "baseline_run1",
                    "emitted_id": "B-01",
                    "false_positive": False,
                },
                {
                    "cell": "method_run1",
                    "emitted_id": "M-01",
                    "false_positive": False,
                },
            ],
        }
    }

    result = _quality(judgement)

    assert result["ledger_total"] == 2
    assert result["baseline_ledger_hits"] == 1
    assert result["baseline_ledger_hit_ids"] == ["L-01"]
    assert result["method_ledger_hits"] == 2
    assert result["method_ledger_hit_ids"] == ["L-01", "L-02"]
    assert result["baseline_emissions"] == {
        "emitted": 1,
        "false_positive": 0,
        "false_positive_ids": [],
    }
    assert result["method_emissions"] == {
        "emitted": 2,
        "false_positive": 1,
        "false_positive_ids": ["M-02"],
    }
