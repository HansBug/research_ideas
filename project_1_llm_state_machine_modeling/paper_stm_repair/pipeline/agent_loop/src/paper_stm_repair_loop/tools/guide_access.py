from __future__ import annotations

import json
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

    def mark_attempt_outcome(
        self,
        sequence: int,
        *,
        execution_status: str,
        tool_executed: bool,
    ) -> None:
        event = next(
            item for item in self.events if int(item.get("sequence", -1)) == sequence
        )
        event["execution_status"] = execution_status
        event["tool_executed"] = tool_executed


def prerequisite_result(blocked_tool: str, required_tool: str) -> dict[str, Any]:
    return {
        "execution_status": "prerequisite_required",
        "blocked_tool": blocked_tool,
        "required_tool": required_tool,
        "message": f"Call {required_tool} successfully before the first attempt to use {blocked_tool}.",
        "required_actions": [
            {
                "action_id": "GUIDE-PREREQUISITE-ACTION-001",
                "problem": (
                    f"{blocked_tool} cannot execute before the required semantics "
                    f"resource {required_tool} has been read."
                ),
                "recommended_tools": [required_tool],
                "recommended_action": (
                    f"Do not repeat {blocked_tool}. Call {required_tool} with a "
                    "non-empty reason, inspect the returned guide metadata and "
                    "content, then retry the blocked workflow step only if still needed."
                ),
                "coverage_improvement": (
                    "Reading the required guide supplies the exact semantics needed "
                    "to compose a valid subsequent tool call."
                ),
                "pass_criteria": (
                    f"{required_tool} returns execution_status=completed and a later "
                    f"{blocked_tool} call is no longer blocked by this prerequisite."
                ),
            }
        ],
        "limitations": [
            "tool_not_executed",
            "no_model_or_query_evidence_produced",
            "guide_first_protocol_is_fail_closed",
        ],
    }


def _with_recovery_guidance(
    tool_name: str, result: dict[str, Any]
) -> dict[str, Any]:
    status = str(result.get("execution_status") or "completed")
    if status in {"completed", "no_new_task_fact", "no_new_guide_fact"}:
        return result
    if result.get("required_actions"):
        return result

    if tool_name == "eval_assert" and (
        status == "inconclusive" or result.get("match_status") == "inconclusive"
    ):
        recommended_tools = ["revise_assertion"]
        action = (
            "Inspect inconclusive_reason, limitations, exception, and function_calls. "
            "Call revise_assertion for the affected latest assertion chain with a "
            "semantically equivalent but executable positive predicate, then evaluate "
            "that new exact expression. Do not repeat the unchanged eval_assert call."
        )
        criteria = (
            "revise_assertion accepts a new version and eval_assert returns "
            "execution_status=completed with match_status=matches or contradicts."
        )
    elif tool_name == "eval_assert":
        recommended_tools = ["eval_assert"]
        action = (
            "Use the missing_latest_required_assertions or registered plan to copy one "
            "latest assertion expression exactly, then call eval_assert with that exact "
            "string and a non-empty reason. Do not revise a registered assertion merely "
            "because this call supplied an unknown or stale expression."
        )
        criteria = (
            "eval_assert matches exactly one latest registered expression and executes "
            "it, returning its assertion_chain_id and match_status."
        )
    elif tool_name == "revise_assertion" and (
        status == "prerequisite_required"
        and "read_fbmcq_guide_before_registering_or_revising_fbmcq"
        in set(result.get("limitations") or [])
    ):
        recommended_tools = ["read_fbmcq_guide"]
        action = (
            "Do not repeat revise_assertion yet. Call read_fbmcq_guide, inspect the "
            "official grammar and semantic metadata, then submit the FBMCQ revision "
            "again only if it still preserves the Root obligation."
        )
        criteria = (
            "read_fbmcq_guide returns execution_status=completed and the subsequent "
            "revise_assertion call is no longer blocked by the FBMCQ prerequisite."
        )
    elif tool_name == "observe_trace":
        recommended_tools = ["observe_trace", "revise_assertion"]
        action = (
            "Inspect limitations and any execution error, then correct qualified event "
            "names, explicit initialization, and cycle structure before one new "
            "observe_trace call. If the requested behavior is not observable with this "
            "bounded trace, use revise_assertion to select a compatible evidence route. "
            "Do not repeat unchanged cycles."
        )
        criteria = (
            "A corrected observe_trace call completes with a new bounded observation, "
            "or revise_assertion accepts a compatible evidence route that is then evaluated."
        )
    elif tool_name == "lookup_source_trace":
        recommended_tools = ["query_model", "lookup_source_trace"]
        action = (
            "Inspect limitations, use query_model or the frozen read_task inventory to "
            "obtain exact element refs, then call lookup_source_trace with corrected "
            "non-empty refs and direction. Do not repeat the unchanged lookup."
        )
        criteria = (
            "lookup_source_trace returns execution_status=completed for exact current-model "
            "refs; ambiguous or untraceable mappings remain explicit domain evidence."
        )
    else:
        recommended_tools = [tool_name]
        action = (
            f"Inspect the {tool_name} error and limitations, correct the named input or "
            "payload fields according to this tool's documented schema, and call it "
            "again only with a materially changed request."
        )
        criteria = f"{tool_name} returns execution_status=completed or accepted=true."

    enriched = dict(result)
    enriched["required_actions"] = [
        {
            "action_id": f"{tool_name.upper()}-RECOVERY-ACTION-001",
            "problem": (
                f"{tool_name} returned execution_status={status}; this call did not "
                "produce terminal usable evidence."
            ),
            "recommended_tools": recommended_tools,
            "recommended_action": action,
            "coverage_improvement": (
                "The corrected call or assertion revision produces new evidence instead "
                "of repeating the same non-progressing request."
            ),
            "pass_criteria": criteria,
        }
    ]
    return enriched


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

    def validation_guidance(exc: Exception) -> str:
        errors = [
            str(item.get("msg") or item)
            for item in getattr(exc, "errors", lambda: [])()
        ] or [str(exc)]
        return json.dumps(
            {
                "execution_status": "invalid_arguments",
                "tool_executed": False,
                "errors": errors,
                "required_actions": [
                    {
                        "action_id": f"{tool.name.upper()}-SCHEMA-ACTION-001",
                        "problem": f"{tool.name} input did not satisfy its strict schema.",
                        "recommended_tools": [tool.name],
                        "recommended_action": (
                            f"Read the named validation errors and {tool.name} parameter "
                            "contract, correct every missing, extra, or mistyped field, "
                            "then call the tool with a materially changed payload. Do not "
                            "repeat the rejected JSON unchanged."
                        ),
                        "coverage_improvement": (
                            "A schema-valid call allows the intended evidence operation "
                            "to execute instead of failing at transport validation."
                        ),
                        "pass_criteria": (
                            f"{tool.name} accepts the corrected schema and executes its "
                            "business logic."
                        ),
                    }
                ],
                "limitations": ["tool_input_schema_rejected", "tool_not_executed"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )

    @wraps(original)
    def guarded(*args: Any, **kwargs: Any) -> Any:
        property_batch = bool(
            require_fbmcq_when is not None and require_fbmcq_when(args, kwargs)
        )
        sequence = state.record_attempt(tool.name, property_batch=property_batch)
        if require_fcstm and not state.has_read("fcstm"):
            result = prerequisite_result(tool.name, "read_fcstm_guide")
            state.mark_attempt_outcome(
                sequence,
                execution_status="prerequisite_required",
                tool_executed=False,
            )
            return result
        if (
            require_fbmcq_when is not None
            and property_batch
            and not state.has_read("fbmcq")
        ):
            result = prerequisite_result(tool.name, "read_fbmcq_guide")
            state.mark_attempt_outcome(
                sequence,
                execution_status="prerequisite_required",
                tool_executed=False,
            )
            return result
        result = original(*args, **kwargs)
        if isinstance(result, dict):
            result = _with_recovery_guidance(tool.name, result)
        execution_status = (
            str(result.get("execution_status") or "completed")
            if isinstance(result, dict)
            else "completed"
        )
        state.mark_attempt_outcome(
            sequence,
            execution_status=execution_status,
            tool_executed=True,
        )
        return result

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
    validation_handler = tool.handle_validation_error or validation_guidance
    return SimpleStructuredTool(
        func=guarded,
        name=tool.name,
        description=guarded.__doc__,
        args_schema=tool.args_schema,
        handle_validation_error=validation_handler,
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
