"""Check fixed report denominators, multi-target hits, and cluster resampling."""

import importlib.util
import json
from pathlib import Path


spec = importlib.util.spec_from_file_location("a2_analysis", Path(__file__).with_name("analyze.py"))
analysis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analysis)


def test_frozen_metrics_preserve_report_denominators_and_distinct_hit_units():
    items = {"a": {"L": "L0"}, "b": {"L": "L2"}}
    reports = []
    for i, (rnd, validity, tier, targets) in enumerate((
        (1, "VALID_KNOWN", "D0", ["a", "b"]),
        (1, "VALID_KNOWN", "D2", ["a"]),
        (2, "VALID_KNOWN", "D1", ["a"]),
        (3, "VALID_NOVEL", "D2", []),
        (3, "INVALID", None, []),
    )):
        reports.append(dict(original_report_id=str(i), pair_id="0000", round=rnd,
                            validity=validity, d_tier=tier, a0_subtype=None if tier else "FALSE_POSITIVE",
                            full_ledger_ids=targets, partial_ledger_ids=[]))
    result = analysis.quality(reports, items)
    assert [result[k] for k in ("reports", "K", "N", "I")] == [5, 3, 1, 1]
    assert result["precision"] == analysis.ratio(4, 5)
    assert result["hit1"] == analysis.ratio(3, 6)
    assert result["hit3"] == analysis.ratio(2, 2)
    assert result["hitall"] == analysis.ratio(0, 2)
    assert result["strict"]["precision"] == analysis.ratio(3, 5)
    assert result["strict"]["hit1"] == analysis.ratio(2, 6)
    same = dict(per_cluster={str(i): result for i in range(9)})
    compared = analysis.paired_uncertainty(same, same)
    for metric in compared["metrics"].values():
        assert metric["a2_minus_v61"] == 0 and metric["percentile95"] == [0, 0]
        assert metric["defined_replicates"] == 10000
    empty = analysis.quality([], items)
    zero = dict(per_cluster={str(i): empty for i in range(9)})
    undefined = analysis.paired_uncertainty(zero, same)
    assert undefined["metrics"]["precision"]["undefined_replicates"] == 10000
    assert undefined["metrics"]["precision"]["percentile95"] is None
    json.dumps(undefined, allow_nan=False)
