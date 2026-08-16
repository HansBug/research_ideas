"""Helpers `build_gist.py` imports, reconstructed after an OS reinstall.

The original lived only in the untracked `runs/` tree and was lost; `build_gist.py`
itself had been committed, so only its two dependencies needed rebuilding.  Both
were reconstructed against the published matrix-v11 audit bundle rather than from
memory: `_segment_macro_sources` reproduces the exact `segment_macro_source_ids`
lists that bundle carries for pairs 0000 (6), 0050 (9) and 0029 (27), which is what
pins the semantics.

`EXPECTED` is deliberately absent.  `build_gist.py` imports it and never reads it --
a leftover of the keyword-matching hit criterion that `_expected_paths` replaced
after it credited pair 0006's unrelated cardinality finding to the effect-absence
defect.  Re-exporting a dead name would invite someone to use it again.
"""

from __future__ import annotations

import json
import pathlib
import re
from typing import Any, Iterator

# ⛔ 归档后深度多了两层，原先的 parents[N] 解析到 `paper_stm_issue_discover/`。
# ⭐ 改为按仓库根标志物向上锚定（CLAUDE.md §9.5-3）。
ROOT = next(_p for _p in pathlib.Path(__file__).resolve().parents if (_p / "CLAUDE.md").is_file() and (_p / ".git").exists())
SOURCE_TRACES = (
    ROOT
    / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/representation"
    / "reports/llms_emp_r45_java_60/source_traces"
)

#: `compiler:transition_segment:<source transition>:segment:<n>` is how the frozen
#: trace records that the converter split one source transition into several FCSTM
#: edges.  The audit reports the *source* ids, so the segment suffix is dropped and
#: the remainder deduplicated.
_SEGMENT = re.compile(r"transition_segment:(tr_\d+):")


def _walk(blob: Any, key: str) -> Iterator[Any]:
    """Yield every value stored under ``key`` anywhere inside ``blob``.

    The run records nest the same field at different depths depending on which
    node wrote them, so the audit reads them positionally rather than by a fixed
    path.  Recursion order is document order, which is what makes `latest()`
    return the last value written rather than an arbitrary one.
    """

    if isinstance(blob, dict):
        for name, value in blob.items():
            if name == key:
                yield value
            yield from _walk(value, key)
    elif isinstance(blob, (list, tuple)):
        for item in blob:
            yield from _walk(item, key)


def _segment_macro_sources(case: str) -> set[str]:
    """Return the source transitions the converter lowered into several edges.

    Reported so a reader can tell a finding about one FCSTM edge from a finding
    about a source transition that no longer exists as a single edge -- the second
    is representation debt whatever the assertion says about it.
    """

    path = SOURCE_TRACES / f"llms_emp_feedback_final_{case}.json"
    if not path.exists():
        return set()
    trace = json.loads(path.read_text())
    exclusions = trace.get("attribution_exclusions") or []
    found: set[str] = set()
    for entry in exclusions:
        match = _SEGMENT.search(str(entry))
        if match:
            found.add(f"source:transition:{match.group(1)}")
    return found


__all__ = ["_segment_macro_sources", "_walk"]
