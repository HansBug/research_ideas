"""Deprecated repository compatibility export for deterministic route replay."""

from paper_stm_method.tools import route_replay as _implementation
from paper_stm_method.tools.route_replay import *  # noqa: F403


def __getattr__(name: str):
    """Forward historical private route-replay helpers without duplicating logic."""

    return getattr(_implementation, name)
