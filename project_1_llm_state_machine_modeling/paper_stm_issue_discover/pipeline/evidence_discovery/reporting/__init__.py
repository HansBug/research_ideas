"""Deprecated compatibility namespace for relocated offline evaluation modules.

The authoritative implementation is ``paper_stm_evaluation``.  This adapter
contains no evaluation logic and is excluded from all public release bundles.
"""

from __future__ import annotations

import sys
from importlib import import_module
from pathlib import Path

_PAPER_ROOT = Path(__file__).resolve().parents[3]
_EVALUATION_SOURCE = _PAPER_ROOT / "evaluation" / "src"
_METHOD_SOURCE = _PAPER_ROOT / "method" / "src"
for _source in (_EVALUATION_SOURCE, _METHOD_SOURCE):
    if str(_source) not in sys.path:
        sys.path.insert(0, str(_source))

_COMPATIBLE_MODULES = (
    "applicability",
    "cost_correction",
    "evaluation_summary",
    "expected_issue_witness",
    "judge_cost_audit",
    "judge_input_projection",
    "method_composite",
    "paired_comparison",
    "soundness_shadow",
    "stage_loss",
    "x1v2_witness_audit",
)
for _module_suffix in _COMPATIBLE_MODULES:
    _module = sys.modules.setdefault(
        f"{__name__}.{_module_suffix}",
        import_module(f"paper_stm_evaluation.{_module_suffix}"),
    )
    setattr(sys.modules[__name__], _module_suffix, _module)

__path__ = [str(Path(__file__).resolve().parent), str(_EVALUATION_SOURCE / "paper_stm_evaluation")]
