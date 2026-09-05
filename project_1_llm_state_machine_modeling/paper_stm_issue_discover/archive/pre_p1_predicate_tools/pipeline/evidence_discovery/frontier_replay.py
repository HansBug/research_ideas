"""Deprecated repository compatibility export for deterministic frontier replay."""

from paper_stm_method.tools import frontier_replay as _implementation
from paper_stm_method.tools.frontier_replay import *  # noqa: F403


def __getattr__(name: str):
    """Forward historical private frontier-replay helpers without duplicating logic."""

    return getattr(_implementation, name)
