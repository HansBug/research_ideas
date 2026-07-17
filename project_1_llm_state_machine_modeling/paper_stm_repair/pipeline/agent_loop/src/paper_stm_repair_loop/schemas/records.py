from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid")

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
