"""no-provider SC control helpers for external stage consumers.

``ids.py`` remains the canonical enum/constant source for stage identifiers and
stage metadata.  ``api.py`` is the broad skill-facing facade that re-exports SD
and SL helpers.  This module sits between them: it exposes small deterministic
SC/control summaries derived from ``ids.py`` so skills can inspect stage order
and stage kinds without importing the full runtime or any provider adapter.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from method.stages.ids import ALL_STAGE_SPECS, StageKind, StageSpec

SC_CONTROL_SCHEMA_VERSION = "lg-m1-b.stage-control.v1"


def canonical_stage_ids() -> list[str]:
    """Return the canonical active SC/SD/SL stage id sequence."""

    return [spec.stage_id for spec in ALL_STAGE_SPECS]


def stage_specs_by_kind() -> dict[str, list[StageSpec]]:
    """Group active stage specs by kind without mutating the canonical specs."""

    grouped: dict[str, list[StageSpec]] = defaultdict(list)
    for spec in ALL_STAGE_SPECS:
        grouped[spec.kind.value].append(spec)
    return dict(grouped)


def build_stage_control_summary() -> dict[str, Any]:
    """Build a JSON-safe no-provider summary for skill health checks."""

    grouped = stage_specs_by_kind()
    stage_ids = canonical_stage_ids()
    return {
        "schema_version": SC_CONTROL_SCHEMA_VERSION,
        "stage_count": len(stage_ids),
        "stage_ids": stage_ids,
        "control_stage_ids": [spec.stage_id for spec in grouped.get(StageKind.CONTROL.value, [])],
        "deterministic_stage_ids": [spec.stage_id for spec in grouped.get(StageKind.DETERMINISTIC.value, [])],
        "llm_stage_ids": [spec.stage_id for spec in grouped.get(StageKind.LLM.value, [])],
        "source": "method.stages.ids.ALL_STAGE_SPECS",
        "provider_free": True,
        "full_loop_free": True,
    }


__all__ = [
    "SC_CONTROL_SCHEMA_VERSION",
    "build_stage_control_summary",
    "canonical_stage_ids",
    "stage_specs_by_kind",
]
