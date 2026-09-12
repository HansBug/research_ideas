"""Resolve a specification's requirement boundaries, preferring annotation over line split.

`nl_segments` decides the key space of `segment_disposition`, so it decides how finely the
model is allowed to answer: one segment, one verdict. Splitting on physical newlines gets
this right for nine of the corpus's ten specifications, because they write one numbered
requirement per line. It gets it wrong for the tenth, which puts everything on one line -- the
whole specification collapses into a single segment and the model can only return one coarse
verdict for all of its requirements.

A cleverer splitter does not fix that one. It numbers two different clauses `4`, writes
`4when` with no separator, and mixes `1 ` with `3.`; in the same sentence `> 10` shows that a
bare digit can also be a value, so no "bare digit means item number" rule can be safe. "How
many requirements is this" has no machine-decidable answer there, so the boundaries are
annotated by hand, once, against the author's own numbering, and shipped as data.

Two properties make the annotation auditable rather than a fudge:

  it is keyed by NL content digest, so every pair sharing a specification resolves to the
  same boundaries and none can be silently missed; and its segments are verbatim slices, so
  concatenating them reproduces the source. That second check is the coverage assertion the
  previous pipeline enforced and this one dropped -- annotating where the prose divides is
  legitimate, quietly rewording it while doing so is not.

What the annotation is *not*: it says nothing about any state machine. It answers "where does
one requirement end", which is a property of the prose, not of the model under test. Nothing
in it may name a model element, and `tests/test_nl_segmentation_override.py` enforces that.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
from dataclasses import dataclass
from typing import Literal

#: The annotation lives with the corpus rather than inside `reports/`, because `reports/` is
#: the deterministic output of `run_llms_emp_r45.py` and is covered by a publication seal.
#: A hand-written artefact in there would break the property that everything under it was
#: machine-generated.
OVERRIDES_PATH = (
    pathlib.Path(__file__).resolve().parents[5]
    / "corpora"
    / "nl_segmentation"
    / "overrides.json"
)

SegmentationSource = Literal["manual_override", "line_split"]


@dataclass(frozen=True)
class ResolvedSegments:
    """Segments plus how they were obtained.

    The provenance travels with the data because a run record that shows `NL-M001` without
    saying why would leave a reader guessing whether the boundaries were annotated or
    inferred. `source` is written into `FrozenDiscoverInputs` for exactly that reason.
    """

    segments: dict[str, str]
    source: SegmentationSource
    nl_sha256: str


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _squash(text: str) -> str:
    return re.sub(r"\s+", "", text)


def load_segmentation_overrides(path: pathlib.Path | None = None) -> dict[str, dict]:
    """Read the annotation file, or return nothing if it is absent.

    Absence is a valid state -- a checkout without the corpus still runs, it just falls back
    to the line split everywhere. A malformed file is not valid and raises, because silently
    ignoring a broken annotation would reintroduce the single-segment behaviour it exists to
    prevent, and do so invisibly.
    """
    target = path or OVERRIDES_PATH
    if not target.exists():
        return {}
    payload = json.loads(target.read_text(encoding="utf-8"))
    version = payload.get("schema_version")
    if version != "paper1.nl_segmentation_override.v1":
        raise ValueError(f"未知的分段标注 schema：{version!r}（{target}）")
    overrides = payload.get("overrides")
    if not isinstance(overrides, dict):
        raise ValueError(f"分段标注缺少 overrides 对象：{target}")
    return overrides


def line_split_segments(natural_language: str) -> dict[str, str]:
    """The default: one segment per non-blank physical line.

    Kept identical to what `discover/nodes.py` did before this module existed, including the
    two quirks. Ids carry the physical line number rather than an ordinal, so a blank line
    leaves a permanent hole in the sequence; and an all-whitespace input falls back to a
    single `NL-ALL`. Neither is triggered by the current corpus (no specification contains a
    blank line), but changing them here would silently alter every unannotated pair.
    """
    return {
        f"NL-L{index:03d}": line.strip()
        for index, line in enumerate(natural_language.splitlines(), start=1)
        if line.strip()
    } or {"NL-ALL": natural_language.strip()}


def resolve_nl_segments(
    natural_language: str, overrides: dict[str, dict] | None = None
) -> ResolvedSegments:
    """Annotated boundaries when this specification has them, otherwise the line split."""
    digest = _digest(natural_language)
    table = load_segmentation_overrides() if overrides is None else overrides
    entry = table.get(digest[:12])
    if entry is None or entry.get("nl_sha256") != digest:
        # A digest-prefix hit whose full hash disagrees means the annotation was written
        # against different text. Falling through to the line split is the safe reading:
        # better a coarse segmentation than boundaries taken from another document.
        return ResolvedSegments(line_split_segments(natural_language), "line_split", digest)
    segments = entry.get("segments")
    if not isinstance(segments, dict) or not segments:
        raise ValueError(f"分段标注 {digest[:12]} 的 segments 为空或格式错误")
    joined = "".join(segments.values())
    if _squash(joined) != _squash(natural_language):
        raise ValueError(
            f"分段标注 {digest[:12]} 的拼接结果与原文不符 —— 标注只能切分，不能改字"
        )
    return ResolvedSegments({k: v.strip() for k, v in segments.items()},
                            "manual_override", digest)
