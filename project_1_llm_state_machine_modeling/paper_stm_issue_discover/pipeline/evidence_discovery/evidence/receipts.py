from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RawReceipt(BaseModel):
    """Structured terminal receipt emitted by one deterministic evidence backend."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    receipt_id: str = Field(min_length=1, description="Stable identifier for this backend execution receipt.")
    backend: str = Field(min_length=1, description="Backend implementation and predicate dispatch label.")
    terminal_state: str = Field(min_length=1, description="Backend terminal state, including completed, unknown, timeout, or unsupported.")
    verdict: str = Field(min_length=1, description="Backend result such as true, false, or unknown; never a W or D level.")
    reason: str = Field(min_length=1, description="Non-empty explanation of the backend result and its boundary.")
    basis: str = Field(min_length=1, description="Non-empty algorithm, input, or diagnostic basis for the backend result.")
    counterexample: list[dict[str, Any]] = Field(default_factory=list, description="Structured counterexample facts when the backend finds a violating result.")
    trace: list[dict[str, Any]] = Field(default_factory=list, description="Structured execution or graph trace supporting the backend result.")
    run_metadata: dict[str, Any] = Field(default_factory=dict, description="Version, input hash, boundary, and diagnostic metadata for this execution.")

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")
