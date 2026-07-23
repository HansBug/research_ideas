from __future__ import annotations

from typing import Any

from pydantic import Field
from typing_extensions import Literal

from .tools import NonBlankString, StrictToolModel


class InspectModelInput(StrictToolModel):
    reason: NonBlankString


class InspectModelResult(StrictToolModel):
    execution_status: Literal["completed", "no_new_fact", "tool_unavailable"]
    parse_status: str | None = None
    semantic_status: str | None = None
    inspect_status: str | None = None
    executable: bool
    diagnostics: list[dict[str, Any]] = Field(default_factory=list)
    inspect: dict[str, Any] = Field(default_factory=dict)
    metrics: dict[str, Any] = Field(default_factory=dict)
    model: dict[str, Any] = Field(default_factory=dict)
    check: dict[str, Any] = Field(default_factory=dict)
    limitations: list[str] = Field(default_factory=list)
    recommended_next_evidence: list[str] = Field(default_factory=list)
    record_id: str | None = None
    reason: str = ""
