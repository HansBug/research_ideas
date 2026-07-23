from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Literal


class RecordModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EvidenceScopeMetadata(RecordModel):
    """Reviewer-visible evidence metadata for one assertion attempt."""

    initialization: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Requested and effective cold/hot initialization, state, variables, "
            "cycles, final observation, and limitations for simulation evidence."
        ),
    )
    formal: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Canonical formal query, parsed property kind, finite bound, bound "
            "origin, assumptions, solver status, witness, replay status, and limitations."
        ),
    )
    check: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Check-result, model, tool, schema, and backend fingerprints used to "
            "produce the evidence record."
        ),
    )
    policy: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Evidence-policy fingerprint and assumption provenance that define how "
            "the attempt may be interpreted by reviewers and renderers."
        ),
    )
    formal_bound_origin: Literal["requirement_bound", "analysis_bound"] | None = None


class Record(RecordModel):
    record_id: str
    sequence: int
    logical_loop_index: int = 0
    record_type: str
    stage: str = "B-discover"
    loop_id: str = "loop-000"
    previous_record_id: str | None = None
    previous_record_sha256: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    artifact_refs: list[dict[str, Any]] = Field(default_factory=list)
    record_sha256: str
