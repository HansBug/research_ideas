from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "src/paper_stm_repair_loop/nl_segmenter.py"


def load_segmenter():
    spec = importlib.util.spec_from_file_location("paper1_nl_segmenter_under_test", MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_segmenter_is_stable_and_does_not_split_and_or_then():
    segmenter = load_segmenter()
    raw = (
        "# Mission\r\n"
        "The UAV count decreases and the system returns to Searching.\r\n"
        "Then it waits.\r\n"
        "- Attack Complete then return and decrement\r\n"
    )

    first = segmenter.segment_nl(raw)
    second = segmenter.segment_nl(raw)

    assert first.segments == second.segments
    assert [segment["segment_kind"] for segment in first.segments] == [
        "title",
        "prose",
        "prose",
        "list_item",
    ]
    assert first.segments[1]["text"] == (
        "The UAV count decreases and the system returns to Searching."
    )
    assert first.segments[3]["text"] == "- Attack Complete then return and decrement"
    assert first.segments[0]["segment_id"] == "SEG-NL-001"
    assert first.segments[0]["segmenter_version"] == "paper1.nl_segmenter.v1"


def test_segmenter_crlf_offset_map_hash_and_non_whitespace_coverage():
    segmenter = load_segmenter()
    raw = "Alpha.\r\n\r\n1. Beta and Gamma then Delta\r\nPlain? Next!"
    result = segmenter.segment_nl(raw)

    assert result.normalized_text == "Alpha.\n\n1. Beta and Gamma then Delta\nPlain? Next!"
    assert result.offset_map[len("Alpha.\n")] == len("Alpha.\r\n")
    assert result.segments[0]["text"] == "Alpha."
    assert result.segments[1]["text"] == "1. Beta and Gamma then Delta"
    assert result.segments[2]["text"] == "Plain?"
    assert result.segments[3]["text"] == "Next!"
    for segment in result.segments:
        assert segment["sha256"] == segmenter.sha256_text(segment["text"])

    covered = set()
    for segment in result.segments:
        covered.update(range(segment["start_offset"], segment["end_offset"]))
    for index, char in enumerate(result.normalized_text):
        if not char.isspace():
            assert index in covered
