"""Foundation state helpers for LangGraph compatibility smoke tests.

This module is deliberately narrow in LG-M1-D1.  The live runtime graph state
(``_GraphLoopState``) and subgraph states still depend on LG-C1 reducers,
LG-E2 Send fan-out, LG-E3 ToolNode wrapper evidence, and LG-C2 context
engineering fields, so they remain in ``method.langgraph_runtime`` until later
D-chain sub-PRs can move the matching behavior and evidence gates together.
"""

from __future__ import annotations

from typing import TypedDict


class CompatState(TypedDict, total=False):
    """Minimal C/E-free state used by LangGraph compatibility smoke tests."""

    value: int


# Compatibility alias for the existing private symbol exported by
# ``method.langgraph_runtime``.  Keeping the private spelling available avoids
# accidental consumer breakage while making the new foundation module explicit.
_CompatState = CompatState

__all__ = ["CompatState", "_CompatState"]
