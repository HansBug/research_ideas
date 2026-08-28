"""The manual segmentation layer, and the one specification that made it necessary.

`nl_segments` is produced by splitting the NL on physical newlines (`nodes.py`), which is
correct for nine of the corpus's ten specifications because they write one numbered
requirement per line. The tenth (`f1c3dc88…`, shared by pairs 0000/0010/0020/0030/0040/0050)
puts all of its requirements on a single line with inconsistent numbering, so the line split
collapses the whole specification into one segment -- and `segment_disposition` is keyed on
those segments, so the model can only return one coarse verdict for the entire spec.

The fix is not a cleverer splitter. That spec numbers two different clauses `4`, writes
`4when` with no separator, and mixes `1 ` with `3.`; "how many requirements is this" has no
machine-decidable answer. So the boundaries are annotated by hand, once, against the author's
own numbering, and the annotation is data rather than code.

What these tests pin down:

  - the override is keyed by NL content digest, so all six pairs sharing a spec get the same
    boundaries and none can be missed
  - segments are verbatim slices: concatenating them reproduces the source, whitespace aside.
    This restores the coverage assertion the previous pipeline had and this one dropped
  - the annotation carries no model element names -- it says how the prose divides, not what
    is wrong with any state machine, which is what keeps it out of oracle territory
  - `prepare` prefers the override when one exists and records which path it took, so a run
    record shows whether its segments were annotated or split
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from paper_stm_feedback_loop.common.nl_segmentation import (
    OVERRIDES_PATH,
    load_segmentation_overrides,
    resolve_nl_segments,
)
from paper_stm_feedback_loop.common.inputs import load_feedback_loop_inputs
from paper_stm_feedback_loop.discover import nodes
from paper_stm_feedback_loop.discover.schemas import DiscoverInput

#: The specification the override exists for, and every pair that shares it.
MALFORMED_DIGEST_PREFIX = "f1c3dc88371b"
AFFECTED_CASES = ("0000", "0010", "0020", "0030", "0040", "0050")


def _report_root() -> Path:
    return (
        Path(__file__).resolve().parents[2]
        / "representation"
        / "reports"
        / "llms_emp_r45_java_60"
    )


def _nl(case: str) -> str:
    return (_report_root() / "pairs" / case / "nl.txt").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------------------
# the annotation file itself
# ---------------------------------------------------------------------------------------


def test_overrides_file_exists_and_declares_its_schema() -> None:
    assert OVERRIDES_PATH.exists(), f"缺少人工分段标注文件：{OVERRIDES_PATH}"
    data = json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))
    assert data["schema_version"] == "paper1.nl_segmentation_override.v1"
    assert data["overrides"], "标注文件不应为空"


def test_override_covers_the_malformed_specification() -> None:
    overrides = load_segmentation_overrides()
    keys = [k for k in overrides if k.startswith(MALFORMED_DIGEST_PREFIX)]
    assert keys, f"未找到 {MALFORMED_DIGEST_PREFIX} 的标注"


def test_segments_are_verbatim_slices_of_the_source() -> None:
    """Concatenating the annotated segments must reproduce the NL, whitespace aside.

    This is the coverage assertion the previous pipeline enforced and the current one
    dropped. Annotating boundaries is legitimate; silently rewording the author's text while
    doing so is not, and only a character-level check catches the difference.
    """
    overrides = load_segmentation_overrides()
    for digest, entry in overrides.items():
        source = next(
            (_nl(c) for c in AFFECTED_CASES
             if entry["nl_sha256"].startswith(digest[:12])
             and _sha_prefix(_nl(c)) == digest[:12]),
            None,
        )
        assert source is not None, f"标注 {digest} 找不到对应的 nl.txt"
        joined = "".join(entry["segments"].values())
        assert _squash(joined) == _squash(source), (
            f"{digest} 的分段拼接与原文不符 —— 标注只能切，不能改字"
        )


def test_annotation_names_no_model_elements() -> None:
    """The annotation must not leak oracle information.

    It answers "where does one requirement end", which is a property of the prose. If a
    segment mentioned an FCSTM path or a pair id it would be answering something else.
    """
    overrides = load_segmentation_overrides()
    blob = json.dumps(overrides, ensure_ascii=False)
    for forbidden in ("llms_emp_feedback_final_", "R45RouteToken", "UnspecifiedInitial",
                      "state:", "macro:", "compiler:"):
        assert forbidden not in blob, f"标注中出现了模型元素标识 `{forbidden}`"


def test_every_affected_case_resolves_to_the_same_boundaries() -> None:
    """Keyed by content digest, so the six pairs sharing this spec cannot diverge."""
    resolved = {c: resolve_nl_segments(_nl(c)) for c in AFFECTED_CASES}
    first = resolved[AFFECTED_CASES[0]]
    for case, got in resolved.items():
        assert got == first, f"{case} 的分段与 {AFFECTED_CASES[0]} 不一致"
    assert first.source == "manual_override"
    assert len(first.segments) > 1, "编号损坏的规格不应只切出一段"


def test_segment_ids_mark_themselves_as_manual() -> None:
    """`NL-M` rather than `NL-L`, so any downstream reader can tell without a lookup."""
    got = resolve_nl_segments(_nl("0000"))
    assert all(re.fullmatch(r"NL-M\d{3}", k) for k in got.segments), got.segments.keys()


# ---------------------------------------------------------------------------------------
# unannotated specifications keep the existing behaviour, byte for byte
# ---------------------------------------------------------------------------------------


@pytest.mark.parametrize("case", ["0029", "0012", "0001", "0006"])
def test_unannotated_specs_fall_back_to_the_line_split(case: str) -> None:
    nl = _nl(case)
    got = resolve_nl_segments(nl)
    expected = {
        f"NL-L{index:03d}": line.strip()
        for index, line in enumerate(nl.splitlines(), start=1)
        if line.strip()
    }
    assert got.segments == expected
    assert got.source == "line_split"


def test_all_whitespace_input_still_reaches_the_nl_all_fallback() -> None:
    got = resolve_nl_segments("   \n  \n")
    assert list(got.segments) == ["NL-ALL"]
    assert got.source == "line_split"


# ---------------------------------------------------------------------------------------
# the override actually reaches the frozen inputs, which is the whole point
# ---------------------------------------------------------------------------------------


def _discover_input(case: str) -> DiscoverInput:
    bundle = load_feedback_loop_inputs(pair_dir=_report_root() / "pairs" / case)
    return DiscoverInput(
        run_id=f"{bundle.pair_id}-test",
        natural_language=bundle.nl_text,
        stm_text=bundle.fcstm_text,
        source_trace=bundle.source_trace.data,
        manifest={"working_contract": bundle.working_contract.data},
        profile="test",
        language="en-US",
    )


def test_prepare_uses_the_override_and_records_that_it_did() -> None:
    frozen = nodes._fallback_prepare(_discover_input("0000"))
    assert len(frozen.nl_segments) > 1, (
        "编号损坏的规格经标注后不应仍是单段 —— 否则下游只能给一个粗粒度裁决"
    )
    assert all(k.startswith("NL-M") for k in frozen.nl_segments)
    assert frozen.nl_segmentation_source == "manual_override"


def test_prepare_leaves_unannotated_pairs_untouched() -> None:
    frozen = nodes._fallback_prepare(_discover_input("0029"))
    assert all(k.startswith("NL-L") for k in frozen.nl_segments)
    assert frozen.nl_segmentation_source == "line_split"
    assert len(frozen.nl_segments) == 13


def test_affected_pair_directories_carry_a_visible_note() -> None:
    """A reader opening `pairs/0000/` must find out there before using `nl.txt`.

    The annotation living in another directory is not discoverable from here, and this is
    exactly the path someone reaches for when they want "the NL for pair 0000".
    """
    for case in AFFECTED_CASES:
        note = _report_root() / "pairs" / case / "SEGMENTATION_NOTE.md"
        assert note.exists(), f"pairs/{case}/ 缺少分段说明"
        text = note.read_text(encoding="utf-8")
        assert "nl_segmentation" in text, f"pairs/{case}/ 的说明未指向标注文件"


def _squash(text: str) -> str:
    return re.sub(r"\s+", "", text)


def _sha_prefix(text: str) -> str:
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
