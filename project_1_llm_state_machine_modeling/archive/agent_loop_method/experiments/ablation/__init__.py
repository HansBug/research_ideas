"""Deterministic and ablation experiment entrypoints for method-level studies.

This package hosts research assets that are intentionally *not* the default
LangGraph agent-loop runtime.  They are useful for ablation, deterministic
replay, and historical smoke tests where the academic question is to isolate a
factor without invoking the full provider-backed loop.
"""

from .deterministic_loop import (
    DeterministicLoopConfig,
    ReviewPolicy,
    run_deterministic_ablation_loop,
    run_pr2a_deterministic_loop,
)

__all__ = [
    "DeterministicLoopConfig",
    "ReviewPolicy",
    "run_deterministic_ablation_loop",
    "run_pr2a_deterministic_loop",
]
