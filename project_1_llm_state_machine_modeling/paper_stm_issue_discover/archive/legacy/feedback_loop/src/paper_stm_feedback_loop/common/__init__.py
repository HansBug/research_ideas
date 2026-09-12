"""Shared, dependency-light primitives for the feedback-loop pipeline.

Common modules are import-boundary clean and must not depend on the legacy
``paper_stm_repair_loop`` package.
"""

__all__ = [
    "config",
    "inputs",
    "records",
    "source_trace",
    "telemetry",
]
