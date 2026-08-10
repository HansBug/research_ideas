from __future__ import annotations

from functools import wraps
from typing import Any, Callable

from ..schemas.tools import SimpleStructuredTool


def enforce_mandatory_tool(
    tool: SimpleStructuredTool,
    required_tool_resolver: Callable[[], str | None],
    attempt_log: list[dict[str, Any]] | None = None,
) -> SimpleStructuredTool:
    """Prevent a globally registered but currently hidden tool from executing."""

    original = tool.func

    def json_value(value: Any) -> Any:
        if hasattr(value, "model_dump"):
            return value.model_dump(mode="json")
        if isinstance(value, list):
            return [json_value(item) for item in value]
        if isinstance(value, tuple):
            return [json_value(item) for item in value]
        if isinstance(value, dict):
            return {str(key): json_value(item) for key, item in value.items()}
        return value

    def record_attempt(
        *,
        required_tool: str | None,
        result: dict[str, Any],
        call_args: tuple[Any, ...],
        call_kwargs: dict[str, Any],
    ) -> None:
        if attempt_log is None:
            return
        attempt_log.append(
            {
                "sequence": len(attempt_log) + 1,
                "tool_name": tool.name,
                "required_tool": required_tool,
                "arguments": {
                    "args": json_value(call_args),
                    "kwargs": json_value(call_kwargs),
                },
                **result,
            }
        )

    @wraps(original)
    def guarded(*args: Any, **kwargs: Any) -> Any:
        required_tool = required_tool_resolver()
        if required_tool is not None and tool.name != required_tool:
            result = {
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
                "required_actions": [
                    {
                        "action_id": "MANDATORY-TOOL-ACTION-001",
                        "problem": (
                            f"{tool.name} cannot produce evidence until the current "
                            f"protocol step {required_tool} is completed."
                        ),
                        "recommended_tools": [required_tool],
                        "recommended_action": (
                            f"Do not repeat {tool.name}. Call {required_tool} next "
                            "with arguments that satisfy that tool's documented "
                            "purpose and schema, inspect its returned evidence or "
                            "feedback, and only then continue the workflow."
                        ),
                        "coverage_improvement": (
                            "Completing the required protocol step creates the "
                            "missing evidence or state transition instead of "
                            "repeating a call that cannot execute."
                        ),
                        "pass_criteria": (
                            f"{required_tool} returns a completed or accepted result "
                            "and the protocol no longer reports it as required."
                        ),
                    }
                ],
                "limitations": [
                    "tool_not_executed",
                    "no_model_or_query_evidence_produced",
                ],
            }
            record_attempt(
                required_tool=required_tool,
                result=result,
                call_args=args,
                call_kwargs=kwargs,
            )
            return result
        result = original(*args, **kwargs)
        execution_status = (
            str(result.get("execution_status") or "completed")
            if isinstance(result, dict)
            else "completed"
        )
        record_attempt(
            required_tool=required_tool,
            result={
                "execution_status": execution_status,
                "tool_executed": execution_status
                not in {"mandatory_tool_rejected", "prerequisite_required"},
            },
            call_args=args,
            call_kwargs=kwargs,
        )
        return result

    guarded.__doc__ = (
        str(tool.description)
        + "\n\nMandatory protocol gate\n-----------------------\n"
        + "The runtime rechecks the current mandatory step immediately before "
        + "execution. A globally registered but currently nonselected tool returns "
        + "``execution_status=mandatory_tool_rejected`` and its underlying logic is "
        + "not executed. The response names ``required_tool`` and provides a "
        + "structured corrective action; follow it instead of repeating the rejected "
        + "call."
    )
    return SimpleStructuredTool(
        func=guarded,
        name=tool.name,
        description=guarded.__doc__,
        args_schema=tool.args_schema,
        handle_validation_error=tool.handle_validation_error,
    )


__all__ = ["enforce_mandatory_tool"]
