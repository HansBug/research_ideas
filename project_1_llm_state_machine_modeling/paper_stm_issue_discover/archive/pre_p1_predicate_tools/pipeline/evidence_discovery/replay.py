"""Deprecated repository compatibility export for provider-free W-state replay."""

from paper_stm_method.tools import replay as _implementation
from paper_stm_method.tools.replay import *  # noqa: F403


def __getattr__(name: str):
    """Forward historical private replay helpers without duplicating logic."""

    return getattr(_implementation, name)
