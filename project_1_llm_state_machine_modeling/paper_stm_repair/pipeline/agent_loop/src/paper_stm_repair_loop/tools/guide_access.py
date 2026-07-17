from __future__ import annotations

from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable


@dataclass
class GuideAccessState:
    """Attempt-local guide access ledger shared by all Discover tools."""

    sequence: int = 0
    fcstm_read_at: int | None = None
    fbmcq_read_at: int | None = None
    events: list[dict[str, Any]] = field(default_factory=list)

    def record_attempt(self, tool_name: str, *, property_batch: bool = False) -> int:
        self.sequence += 1
        self.events.append(
            {
                "sequence": self.sequence,
                "event": "tool_attempt",
                "tool_name": tool_name,
                "property_batch": property_batch,
            }
        )
        return self.sequence

    def mark_read(self, guide_kind: str, metadata: dict[str, Any]) -> int:
        self.sequence += 1
        event = {
            "sequence": self.sequence,
            "event": "guide_read",
            "guide_kind": guide_kind,
            "resource_name": metadata.get("resource_name"),
            "sha256": metadata.get("sha256"),
            "pyfcstm_version": metadata.get("pyfcstm_version"),
        }
        self.events.append(event)
        if guide_kind == "fcstm" and self.fcstm_read_at is None:
            self.fcstm_read_at = self.sequence
        elif guide_kind == "fbmcq" and self.fbmcq_read_at is None:
            self.fbmcq_read_at = self.sequence
        return self.sequence

    def has_read(self, guide_kind: str) -> bool:
        if guide_kind == "fcstm":
            return self.fcstm_read_at is not None
        if guide_kind == "fbmcq":
            return self.fbmcq_read_at is not None
        raise ValueError(f"unknown guide kind: {guide_kind}")

    def first_attempt_at(self, tool_name: str, *, after: int | None = None) -> int | None:
        """Return the first matching tool-attempt sequence after an optional gate."""

        sequences = [
            int(item["sequence"])
            for item in self.events
            if item.get("event") == "tool_attempt"
            and item.get("tool_name") == tool_name
            and (after is None or int(item["sequence"]) > after)
        ]
        return min(sequences) if sequences else None


def prerequisite_result(blocked_tool: str, required_tool: str) -> dict[str, Any]:
    return {
        "execution_status": "prerequisite_required",
        "blocked_tool": blocked_tool,
        "required_tool": required_tool,
        "message": f"Call {required_tool} successfully before the first attempt to use {blocked_tool}.",
        "limitations": [
            "tool_not_executed",
            "no_model_or_query_evidence_produced",
            "guide_first_protocol_is_fail_closed",
        ],
    }


def guard_tool(
    tool: Any,
    state: GuideAccessState,
    *,
    require_fcstm: bool = True,
    require_fbmcq_when: Callable[[tuple[Any, ...], dict[str, Any]], bool] | None = None,
) -> Any:
    """Wrap a StructuredTool with attempt-local guide prerequisites."""

    from ..schemas.tools import SimpleStructuredTool

    original = tool.func

    @wraps(original)
    def guarded(*args: Any, **kwargs: Any) -> Any:
        property_batch = bool(
            require_fbmcq_when is not None and require_fbmcq_when(args, kwargs)
        )
        state.record_attempt(tool.name, property_batch=property_batch)
        if require_fcstm and not state.has_read("fcstm"):
            return prerequisite_result(tool.name, "read_fcstm_guide")
        if (
            require_fbmcq_when is not None
            and property_batch
            and not state.has_read("fbmcq")
        ):
            return prerequisite_result(tool.name, "read_fbmcq_guide")
        return original(*args, **kwargs)

    description = str(tool.description)
    prerequisite_text = (
        "\n\nGuide prerequisite\n------------------\n"
        "The Controller rejects this call with ``execution_status=prerequisite_required`` "
        "unless ``read_fcstm_guide`` succeeded earlier in this Agent attempt."
    )
    if require_fbmcq_when is not None:
        prerequisite_text += (
            " A batch containing any ``check_kind=property`` also requires an earlier "
            "successful ``read_fbmcq_guide`` call."
        )
    guarded.__doc__ = description + prerequisite_text
    return SimpleStructuredTool(
        func=guarded,
        name=tool.name,
        description=guarded.__doc__,
        args_schema=tool.args_schema,
    )


def property_batch_requested(args: tuple[Any, ...], kwargs: dict[str, Any]) -> bool:
    checks = kwargs.get("checks")
    if checks is None and args:
        checks = args[0]
    if not isinstance(checks, list):
        return False
    for check in checks:
        if hasattr(check, "check_kind"):
            kind = getattr(check, "check_kind")
        elif isinstance(check, dict):
            kind = check.get("check_kind")
        else:
            kind = None
        if kind == "property":
            return True
    return False


__all__ = [
    "GuideAccessState",
    "guard_tool",
    "prerequisite_result",
    "property_batch_requested",
]
