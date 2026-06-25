"""PlantUML pre-SCXML normalization for R3.1 recovery.

This package never creates canonical STM directly.  It only prepares auditable
PlantUML candidates that must still pass the official PlantUML ``-tscxml``
toolchain before any canonical model can be produced by the R3 SCXML adapter.
"""

from .plantuml import NormalizationChange, NormalizationResult, normalize_plantuml

__all__ = ["NormalizationChange", "NormalizationResult", "normalize_plantuml"]
