"""Compatibility import for the arm-neutral structured runtime.

The implementation lives in :mod:`utils.structured_runtime` so Semantic Judge
and method share exact retry, receipt, usage, and serialization behavior
without either package importing the other.
"""

from utils import structured_runtime as _shared_runtime
from utils.structured_runtime import *  # noqa: F403


def __getattr__(name: str):
    """Forward historical private helper imports to the shared implementation."""

    return getattr(_shared_runtime, name)
