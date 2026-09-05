"""Deprecated repository compatibility export for deterministic probe replay."""

from paper_stm_method.tools import execution_probe_replay as _implementation
from paper_stm_method.tools.execution_probe_replay import *  # noqa: F403


def __getattr__(name: str):
    """Forward historical private execution-probe helpers without duplicating logic."""

    return getattr(_implementation, name)
