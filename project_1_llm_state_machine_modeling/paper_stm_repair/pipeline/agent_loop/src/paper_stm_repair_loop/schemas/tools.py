from __future__ import annotations

import inspect
from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Literal

from .common import DiscoverCheckDraft


class StrictToolModel(BaseModel):
    """Base class for Agent-facing tool schemas: strict types and no extras."""

    model_config = ConfigDict(extra="forbid", strict=True)


ExecutionStatus = Literal["completed", "invalid_arguments", "tool_unavailable", "execution_error", "unknown", "timeout", "incomplete"]


class FrozenTaskSnapshot(StrictToolModel):
    stage: str
    loop_no: int
    model: dict[str, Any]
    targets: list[Any] = Field(default_factory=list)
    current_records: dict[str, Any]
    readable_history: list[Any] = Field(default_factory=list)


class ReadTaskInput(StrictToolModel):
    pass


class QueryModelInput(StrictToolModel):
    query_kind: Literal["states", "events", "transitions", "variables", "diagnostics"]
    name_contains: str | None = None
    offset: int = 0
    limit: int = 50


class ModelQueryResult(StrictToolModel):
    execution_status: ExecutionStatus
    query_kind: Literal["states", "events", "transitions", "variables", "diagnostics"]
    matched_items: list[dict[str, Any]] = Field(default_factory=list)
    total_matches: int = Field(default=0, ge=0)
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=50, ge=1)
    truncated: bool = False
    model_sha256: str
    limitations: list[str] = Field(default_factory=list)


class ObserveTraceInput(StrictToolModel):
    events: list[str]
    max_steps: int | None = None


class TraceObservation(StrictToolModel):
    execution_status: ExecutionStatus
    model_sha256: str
    requested_events: list[str] = Field(default_factory=list)
    cycles: int = Field(default=0, ge=0)
    input_events: list[str] = Field(default_factory=list)
    consumed_events: list[str] = Field(default_factory=list)
    unconsumed_events: list[str] = Field(default_factory=list)
    final_configuration: dict[str, Any] = Field(default_factory=dict)
    diagnostics: list[dict[str, Any]] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class LookupSourceTraceInput(StrictToolModel):
    element_refs: list[str]
    direction: Literal["source_to_fcstm", "fcstm_to_source"] = "fcstm_to_source"


class EvaluateChecksInput(StrictToolModel):
    checks: list[DiscoverCheckDraft] = Field(min_length=1)


class SourceTraceLookupResult(StrictToolModel):
    execution_status: ExecutionStatus
    direction: Literal["source_to_fcstm", "fcstm_to_source"]
    requested_refs: list[str] = Field(default_factory=list)
    exact_matches: list[dict[str, Any]] = Field(default_factory=list)
    ambiguous_matches: list[dict[str, Any]] = Field(default_factory=list)
    untraceable_refs: list[str] = Field(default_factory=list)
    trace_sha256: str
    limitations: list[str] = Field(default_factory=list)


__all__ = [
    "ExecutionStatus",
    "EvaluateChecksInput",
    "FrozenTaskSnapshot",
    "LookupSourceTraceInput",
    "ModelQueryResult",
    "ObserveTraceInput",
    "QueryModelInput",
    "ReadTaskInput",
    "SourceTraceLookupResult",
    "StrictToolModel",
    "TraceObservation",
]

class SimpleStructuredTool:
    """Compatibility constructor that returns a real LangChain StructuredTool."""

    def __new__(
        cls,
        *,
        func: Any,
        name: str,
        description: str,
        args_schema: type[BaseModel],
    ) -> Any:
        from langchain_core.tools import StructuredTool

        return StructuredTool.from_function(
            func=func,
            name=name,
            description=inspect.cleandoc(description),
            args_schema=args_schema,
        )

__all__.append("SimpleStructuredTool")
