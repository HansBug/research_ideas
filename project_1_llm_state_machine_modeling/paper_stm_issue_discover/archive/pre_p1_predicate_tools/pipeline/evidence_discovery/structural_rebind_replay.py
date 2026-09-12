"""Deprecated repository compatibility export for structural rebind replay."""

from paper_stm_method.tools import structural_rebind_replay as _implementation
from paper_stm_method.tools.structural_rebind_replay import *  # noqa: F403


def __getattr__(name: str):
    """Forward historical private structural-rebind helpers without duplicating logic."""

    return getattr(_implementation, name)
