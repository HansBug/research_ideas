from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PostBatchInvestigationState:
    """Track bounded post-batch microscopes by distinct eligible check batch."""

    evaluation_invocations: list[dict[str, Any]]
    completed_tools: dict[str, set[str]] = field(default_factory=dict)

    def latest_eligible_batch(self) -> str | None:
        for invocation in reversed(self.evaluation_invocations):
            result = invocation.get("result")
            if not isinstance(result, dict):
                continue
            gate = result.get("gate")
            drafts_sha256 = result.get("drafts_sha256")
            if (
                result.get("execution_status") == "completed"
                and isinstance(gate, dict)
                and gate.get("eligible") is True
                and isinstance(drafts_sha256, str)
                and drafts_sha256
            ):
                return drafts_sha256
        return None

    def already_completed(self, tool_name: str, batch_sha256: str) -> bool:
        return tool_name in self.completed_tools.get(batch_sha256, set())

    def mark_completed(self, tool_name: str, batch_sha256: str) -> None:
        self.completed_tools.setdefault(batch_sha256, set()).add(tool_name)


__all__ = ["PostBatchInvestigationState"]
