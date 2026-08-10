"""Historical marker for the removed A0-A4 legacy full-loop implementation.

LG-M1-C2 removes the old full-loop active API from this module.  New modeling
or ablation work must use either the canonical staged entrypoint
``archive.agent_loop_method.loop.run_agent_loop`` or the deterministic ablation asset under
``archive.agent_loop_method.experiments.ablation``.  This file remains only so provenance scans can
explain why historical documents mention ``archive.agent_loop_method.legacy_loop``; it deliberately
exports no runnable loop.
"""

from __future__ import annotations

REMOVED_LEGACY_LOOP_NOTE = (
    "The old A0-A4 legacy full-loop implementation was removed from active API "
    "surface by LG-M1-C2; use archive.agent_loop_method.loop.run_agent_loop or "
    "archive.agent_loop_method.experiments.ablation instead."
)

__all__ = ["REMOVED_LEGACY_LOOP_NOTE"]
