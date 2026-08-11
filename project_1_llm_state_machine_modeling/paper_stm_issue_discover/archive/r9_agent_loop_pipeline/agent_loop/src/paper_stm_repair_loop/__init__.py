"""Runnable paper1 agent-loop stages.

The package root intentionally avoids importing stage implementations eagerly.
Discover has a comparatively large optional runtime surface (LLM providers,
pyfcstm simulation, and FBMCQ); importing a schema or deterministic evaluator
must not initialize that surface.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

__version__ = "0.1.0"

if TYPE_CHECKING:
    from utils.llm import LLMRegistry

    from .schemas.discovery import DiscoverCompleted


def run_discover(run_dir: Path, registry: "LLMRegistry") -> "DiscoverCompleted":
    """Lazily dispatch one B-discover run through the stage implementation."""

    from .agents.discover import run_discover as _run_discover

    return _run_discover(run_dir, registry)


def __getattr__(name: str) -> Any:
    if name == "DiscoverCompleted":
        from .schemas.discovery import DiscoverCompleted

        return DiscoverCompleted
    raise AttributeError(name)


__all__ = ["DiscoverCompleted", "run_discover"]
