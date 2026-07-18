from __future__ import annotations

from functools import wraps
from typing import Any, Callable

from ..schemas.tools import SimpleStructuredTool


def enforce_mandatory_tool(
    tool: SimpleStructuredTool,
    required_tool_resolver: Callable[[], str | None],
) -> SimpleStructuredTool:
    """Prevent a globally registered but currently hidden tool from executing."""

    original = tool.func

    @wraps(original)
    def guarded(*args: Any, **kwargs: Any) -> Any:
        required_tool = required_tool_resolver()
        if required_tool is not None and tool.name != required_tool:
            return {
                "execution_status": "mandatory_tool_rejected",
                "tool_executed": False,
                "requested_tool": tool.name,
                "required_tool": required_tool,
                "error": {
                    "code": "mandatory_tool_mismatch",
                    "message": (
                        f"{tool.name} was not executed because {required_tool} is the "
                        "only allowed tool in this protocol step."
                    ),
                },
                "limitations": [
                    "tool_not_executed",
                    "no_model_or_query_evidence_produced",
                ],
            }
        return original(*args, **kwargs)

    guarded.__doc__ = (
        str(tool.description)
        + "\n\nMandatory protocol gate\n-----------------------\n"
        + "The runtime rechecks the current mandatory step immediately before "
        + "execution. A globally registered but currently nonselected tool returns "
        + "``execution_status=mandatory_tool_rejected`` and its underlying logic is "
        + "not executed."
    )
    return SimpleStructuredTool(
        func=guarded,
        name=tool.name,
        description=guarded.__doc__,
        args_schema=tool.args_schema,
    )


__all__ = ["enforce_mandatory_tool"]
