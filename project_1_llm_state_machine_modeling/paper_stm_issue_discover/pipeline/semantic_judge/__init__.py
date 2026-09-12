"""Deprecated compatibility namespace for the relocated Semantic Judge.

The authoritative package is ``paper_stm_judge``.  This namespace only keeps
historical internal imports and test node IDs stable and is never released with
the method package.
"""

from __future__ import annotations

import sys
from pathlib import Path

_PAPER_ROOT = Path(__file__).resolve().parents[2]
_JUDGE_SOURCE = _PAPER_ROOT / "judge" / "src"
for _source in (_JUDGE_SOURCE,):
    if str(_source) not in sys.path:
        sys.path.insert(0, str(_source))

from paper_stm_judge import (
    JUDGE_ALGORITHM_VERSION,
    PROTOCOL_SHA256,
    PROTOCOL_VERSION,
    CandidateReport,
    CoreClaimTruth,
    ExpectedIssue,
    JudgeScaleAudit,
    MatchStrength,
    PositiveMatchStrength,
    ReportValidity,
    SemanticMetrics,
    UnifiedJudgeInput,
)

__path__ = [str(Path(__file__).resolve().parent), str(_JUDGE_SOURCE / "paper_stm_judge")]
__all__ = [
    "JUDGE_ALGORITHM_VERSION",
    "PROTOCOL_SHA256",
    "PROTOCOL_VERSION",
    "CandidateReport",
    "CoreClaimTruth",
    "ExpectedIssue",
    "JudgeScaleAudit",
    "MatchStrength",
    "PositiveMatchStrength",
    "ReportValidity",
    "SemanticMetrics",
    "UnifiedJudgeInput",
]
