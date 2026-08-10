"""Compatibility shim for the historical PR-2A deterministic loop.

The deterministic/ablation implementation now lives in
``method.experiments.ablation.deterministic_loop``.  This module is retained so
older tests, scripts, and historical references can still import the previous
``method.pr2a_loop`` path, but new code should use the functional ablation path
instead.
"""

from __future__ import annotations

from method.experiments.ablation import deterministic_loop as _deterministic_loop
from method.experiments.ablation.deterministic_loop import *  # noqa: F401,F403
from method.experiments.ablation.deterministic_loop import (
    DeterministicLoopConfig,
    ReviewPolicy,
    run_deterministic_ablation_loop,
    run_pr2a_deterministic_loop,
)

__all__ = [
    *getattr(_deterministic_loop, "__all__", []),
    "DeterministicLoopConfig",
    "ReviewPolicy",
    "run_deterministic_ablation_loop",
    "run_pr2a_deterministic_loop",
]
