from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


STATUS_CODES = {
    "converted": "R3.STATUS.converted",
    "partial": "R3.STATUS.partial",
    "blocked": "R3.STATUS.blocked",
    "unsupported": "R3.STATUS.unsupported",
}

TIMING_LEVELS = {"none", "qualitative", "clock", "timed_constraints", "unknown"}
HIERARCHY_LEVELS = {"flat", "hierarchical", "concurrent", "unknown"}


@dataclass
class State:
    id: str
    label: str
    kind: str = "state"
    parent: str | None = None
    raw_ref: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "kind": self.kind,
            "parent": self.parent,
            "raw_ref": self.raw_ref,
            "attributes": self.attributes,
        }


@dataclass
class Transition:
    id: str
    source: str
    target: str
    event: str | None = None
    guard: str | None = None
    action: str | None = None
    label: str | None = None
    scope: str | None = None
    raw_ref: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "source": self.source,
            "target": self.target,
            "event": self.event,
            "guard": self.guard,
            "action": self.action,
            "label": self.label,
            "scope": self.scope,
            "raw_ref": self.raw_ref,
            "attributes": self.attributes,
        }


@dataclass
class Loss:
    loss_id: str
    example_id: str
    source_ref: str | None
    canonical_ref: str | None
    loss_type: str
    severity: str
    rationale: str
    needs_manual_review: bool = False
    repair_contribution_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "loss_id": self.loss_id,
            "example_id": self.example_id,
            "source_ref": self.source_ref,
            "canonical_ref": self.canonical_ref,
            "loss_type": self.loss_type,
            "severity": self.severity,
            "rationale": self.rationale,
            "repair_contribution_allowed": self.repair_contribution_allowed,
            "needs_manual_review": self.needs_manual_review,
            "loss_code": f"R3.LOSS.{self.loss_type}.{self.severity}",
        }


@dataclass
class ConversionResult:
    example_id: str
    seed_id: str
    source_format: str
    adapter: str
    status: str
    states: list[State] = field(default_factory=list)
    transitions: list[Transition] = field(default_factory=list)
    variables: list[dict[str, Any]] = field(default_factory=list)
    initial_states: list[str] = field(default_factory=list)
    final_states: list[str] = field(default_factory=list)
    timing_level: str = "none"
    hierarchy_level: str = "flat"
    blocking_reason: str | None = None
    diagnostics: list[dict[str, Any]] = field(default_factory=list)
    losses: list[Loss] = field(default_factory=list)
    canonical_model_name: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "r3.canonical_stm.v0",
            "example_id": self.example_id,
            "seed_id": self.seed_id,
            "source_format": self.source_format,
            "adapter": self.adapter,
            "status": self.status,
            "status_reason_code": STATUS_CODES[self.status],
            "model": {
                "name": self.canonical_model_name or self.example_id,
                "states": [s.to_dict() for s in self.states],
                "transitions": [t.to_dict() for t in self.transitions],
                "variables": self.variables,
                "initial_states": self.initial_states,
                "final_states": self.final_states,
                "timing_level": self.timing_level,
                "hierarchy_level": self.hierarchy_level,
            },
            "diagnostics": self.diagnostics,
            "metadata": self.metadata,
        }

    def losses_dicts(self) -> list[dict[str, Any]]:
        return [loss.to_dict() for loss in self.losses]
