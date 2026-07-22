from __future__ import annotations

import inspect
import keyword
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from typing_extensions import Literal

class StrictToolModel(BaseModel):
    """Base class for Agent-facing tool schemas: strict types and no extras."""

    model_config = ConfigDict(extra="forbid", strict=True)


NonBlankString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


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
    reason: NonBlankString


class ReadGuideInput(StrictToolModel):
    reason: NonBlankString


class QueryModelInput(StrictToolModel):
    query_kind: Literal["states", "events", "transitions", "variables", "diagnostics"]
    name_contains: str | None = None
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=50, ge=1, le=500)
    root_node_ids: list[NonBlankString] = Field(default_factory=list)
    reason: NonBlankString


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
    root_node_ids: list[NonBlankString] = Field(min_length=1)
    cycles: list[list[NonBlankString]] = Field(min_length=1)
    reason: NonBlankString


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
    element_refs: list[NonBlankString] = Field(min_length=1)
    direction: Literal["source_to_fcstm", "fcstm_to_source"] = "fcstm_to_source"
    reason: NonBlankString


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

def _structured_tool_from_function(**kwargs: Any) -> Any:
    """Create a LangChain tool without dropping keyword-named public fields."""

    from langchain_core.tools import StructuredTool

    class ExactKeywordSchemaTool(StructuredTool):
        @property
        def tool_call_schema(self) -> Any:
            schema = super().tool_call_schema
            args_schema = self.args_schema
            if not isinstance(args_schema, type) or not issubclass(args_schema, BaseModel):
                return schema

            full_schema = args_schema.model_json_schema()
            full_properties = full_schema.get("properties", {})
            if isinstance(schema, dict):
                exposed_properties = schema.get("properties", {})
            else:
                exposed_properties = schema.model_json_schema().get("properties", {})
            omitted = set(full_properties) - set(exposed_properties)
            if omitted and all(keyword.iskeyword(name) for name in omitted):
                return {**full_schema, "description": self.description}
            return schema

    return ExactKeywordSchemaTool.from_function(**kwargs)


class SimpleStructuredTool:
    """Compatibility constructor that returns a real LangChain StructuredTool."""

    def __new__(
        cls,
        *,
        func: Any,
        name: str,
        description: str,
        args_schema: type[BaseModel],
        handle_validation_error: Any = False,
    ) -> Any:
        return _structured_tool_from_function(
            func=func,
            name=name,
            description=inspect.cleandoc(description),
            args_schema=args_schema,
            handle_validation_error=handle_validation_error,
        )

__all__.append("SimpleStructuredTool")
