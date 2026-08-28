"""Sealed assertion result contract.

Ported pure assertion result semantics from legacy agent_loop eval_env at source
commit c8c1ccba and adapted for prefix-plus-terminal-assert scripts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any, Literal

AssertionOutcome = Literal["valid", "sealed_false", "invalid"]


@dataclass(frozen=True)
class SealedAssertionResult:
    """Outcome of one LLM assertion script.

    `sealed_false` is emitted only when the terminal assertion expression
    evaluates to strict `False`. All exceptions, including `AssertionError`, are
    invalid rather than sealed.
    """

    outcome: AssertionOutcome
    value: bool | None
    terminal_expression: str | None
    reason: str
    error: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_valid(self) -> bool:
        return self.outcome == "valid"

    @property
    def is_sealed_false(self) -> bool:
        return self.outcome == "sealed_false"

    @property
    def is_invalid(self) -> bool:
        return self.outcome == "invalid"

    def to_json(self) -> dict[str, Any]:
        return {
            "outcome": self.outcome,
            "value": self.value,
            "terminal_expression": self.terminal_expression,
            "reason": self.reason,
            "error": self.error,
            "metadata": self.metadata,
        }


class InMemorySealedStore:
    """Keep truth-bearing payloads outside LangGraph state until release."""

    def __init__(self) -> None:
        self._payloads: dict[str, Any] = {}
        self._lock = Lock()

    def put(self, sealed_hash: str, payload: Any) -> str:
        with self._lock:
            if sealed_hash in self._payloads and self._payloads[sealed_hash] != payload:
                raise ValueError("sealed hash collision with different payload")
            self._payloads[sealed_hash] = payload
        return f"sealed://{sealed_hash}"

    def release(self, sealed_hash: str) -> Any:
        with self._lock:
            if sealed_hash not in self._payloads:
                raise KeyError(f"sealed payload not found: {sealed_hash}")
            return self._payloads[sealed_hash]


__all__ = ["AssertionOutcome", "InMemorySealedStore", "SealedAssertionResult"]
