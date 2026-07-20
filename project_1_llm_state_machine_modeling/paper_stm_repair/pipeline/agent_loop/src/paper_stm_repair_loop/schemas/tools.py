from __future__ import annotations

import inspect
from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Literal

class StrictToolModel(BaseModel):
    """Base class for Agent-facing tool schemas: strict types and no extras."""

    model_config = ConfigDict(extra="forbid", strict=True)


ExecutionStatus = Literal[
    "completed",
    "prerequisite_required",
    "invalid_arguments",
    "tool_unavailable",
    "execution_error",
    "unknown",
    "timeout",
    "incomplete",
    "inconclusive",
]


class FrozenTaskSnapshot(StrictToolModel):
    stage: str
    loop_no: int
    model: dict[str, Any]
    targets: list[Any] = Field(default_factory=list)
    current_records: dict[str, Any]
    readable_history: list[Any] = Field(default_factory=list)


class ReadTaskInput(StrictToolModel):
    reason: str = Field(min_length=1)


class ReadGuideInput(StrictToolModel):
    reason: str = Field(min_length=1)


class QueryModelInput(StrictToolModel):
    query_kind: Literal["states", "events", "transitions", "variables", "diagnostics"]
    name_contains: str | None = None
    offset: int = 0
    limit: int = 50
    root_node_ids: list[str] = Field(default_factory=list)
    reason: str = Field(min_length=1)


class ModelQueryResult(StrictToolModel):
    execution_status: ExecutionStatus
    query_kind: Literal["states", "events", "transitions", "variables", "diagnostics"]
    matched_items: list[dict[str, Any]] = Field(default_factory=list)
    total_matches: int = Field(default=0, ge=0)
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=50, ge=1)
    truncated: bool = False
    model_sha256: str
    root_node_ids: list[str] = Field(default_factory=list)
    reason: str = ""
    limitations: list[str] = Field(default_factory=list)


class ObserveTraceInput(StrictToolModel):
    question: str = Field(min_length=1)
    root_node_ids: list[str] = Field(min_length=1)
    cycles: list[list[str]] = Field(min_length=1)
    reason: str = Field(min_length=1)


class TraceObservation(StrictToolModel):
    execution_status: ExecutionStatus
    question: str
    root_node_ids: list[str] = Field(min_length=1)
    requested_cycles: list[list[str]] = Field(min_length=1)
    cycles: list[dict[str, Any]] = Field(default_factory=list)
    final: dict[str, Any] = Field(default_factory=dict)
    model_sha256: str
    reason: str = ""
    limitations: list[str] = Field(default_factory=list)


class LookupSourceTraceInput(StrictToolModel):
    element_refs: list[str]
    direction: Literal["source_to_fcstm", "fcstm_to_source"] = "fcstm_to_source"
    reason: str = Field(min_length=1)


class SourceTraceLookupResult(StrictToolModel):
    execution_status: ExecutionStatus
    direction: Literal["source_to_fcstm", "fcstm_to_source"]
    requested_refs: list[str] = Field(default_factory=list)
    exact_matches: list[dict[str, Any]] = Field(default_factory=list)
    ambiguous_matches: list[dict[str, Any]] = Field(default_factory=list)
    untraceable_refs: list[str] = Field(default_factory=list)
    trace_sha256: str
    reason: str = ""
    limitations: list[str] = Field(default_factory=list)


__all__ = [
    "ExecutionStatus",
    "FrozenTaskSnapshot",
    "LookupSourceTraceInput",
    "ModelQueryResult",
    "ObserveTraceInput",
    "QueryModelInput",
    "ReadGuideInput",
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
