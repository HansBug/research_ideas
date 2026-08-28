"""Replay a recorded Discover run's LLM outputs against the current graph.

Why this exists
---------------
Verifying a control-flow or contract change used to mean paying for a real
matrix run.  For pair 0029 that was ~95 minutes and 1.66M tokens across two
models, to answer a question the recorded artifacts already contain: *given the
exact same producer outputs, where does the graph go now?*

Every ``*-llm-call-completed`` record already stores ``parsed_output`` as a
complete structured object, plus ``role`` and ``revision``.  Feeding those back
in order reruns the whole StateGraph deterministically at zero token cost.

Scope and limits
----------------
Replay is valid for **control-flow and contract changes** -- budgets, routing,
isolation, mandatory-evidence rules -- because those consume producer output
without changing what the producer would say.  It is **not** valid for prompt
changes: once the prompt differs, the recorded output no longer represents what
the model would produce.  Prompt changes need a static consistency test (see
``tests/test_contract_prompt_consistency.py``) and, eventually, a real run.

When the graph asks for more calls of a role than the recording holds -- which
is exactly what a successful isolation fix looks like, since it should need
*fewer* -- the responder replays the final recorded output for that role and
counts the overrun.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic import BaseModel

__all__ = ["RecordedCall", "ReplayResponder", "load_recorded_calls"]

_ROLE_BY_SCHEMA = {
    "RequirementSet": "requirement_splitter",
    "RequirementReview": "requirement_reviewer",
    "AssertionScript": "assertion_converter",
    "AssertionReview": "assertion_reviewer",
    "DiscoverAdjudication": "result_adjudicator",
}


@dataclass(frozen=True)
class RecordedCall:
    """One recorded structured LLM response."""

    sequence: int
    role: str
    revision: int | None
    parsed_output: dict[str, Any]


def load_recorded_calls(records_dir: str | Path) -> list[RecordedCall]:
    """Read every recorded LLM call from an immutable record directory.

    :param records_dir: the run's ``records/`` directory.
    :return: calls in recorded order.
    """

    root = Path(records_dir)
    calls: list[RecordedCall] = []
    for index, path in enumerate(sorted(root.glob("*-llm-call-completed/record.json"))):
        payload = json.loads(path.read_text(encoding="utf-8"))
        parsed = payload.get("parsed_output")
        if not isinstance(parsed, dict):
            continue
        calls.append(
            RecordedCall(
                sequence=index,
                role=str(payload.get("role")),
                revision=payload.get("revision"),
                parsed_output=parsed,
            )
        )
    return calls


@dataclass
class ReplayResponder:
    """A :class:`StructuredResponder` that returns recorded outputs in order.

    :param calls: recorded calls, typically from :func:`load_recorded_calls`.
    """

    calls: list[RecordedCall]
    consumed: dict[str, int] = field(default_factory=dict)
    overruns: dict[str, int] = field(default_factory=dict)
    #: Roles the recording never reached, answered with a neutral synthetic
    #: response instead.  A non-empty value is itself a finding: it means the
    #: replayed graph progressed past the point where the recorded run died.
    synthesized: dict[str, int] = field(default_factory=dict)
    allow_synthetic: bool = True

    def _next_for_role(self, role: str) -> dict[str, Any] | None:
        pool = [call for call in self.calls if call.role == role]
        if not pool:
            if not self.allow_synthetic:
                raise LookupError(f"no recorded {role} call to replay")
            self.synthesized[role] = self.synthesized.get(role, 0) + 1
            return None
        index = self.consumed.get(role, 0)
        self.consumed[role] = index + 1
        if index >= len(pool):
            self.overruns[role] = self.overruns.get(role, 0) + 1
            return pool[-1].parsed_output
        return pool[index].parsed_output

    def invoke_structured(
        self, *, role: str, schema: type[BaseModel], system_prompt: str, user_input: str
    ) -> BaseModel:
        del system_prompt, user_input
        recorded_role = _ROLE_BY_SCHEMA.get(schema.__name__, role)
        recorded = self._next_for_role(recorded_role)
        if recorded is None:
            return _synthetic_response(schema)
        payload = dict(recorded)
        if schema.__name__ == "AssertionReview":
            # The graph rebinds this to the live script hash; the recorded value
            # belongs to a script the replayed graph may have already filtered.
            payload["reviewed_script_hash"] = "TO_BE_PATCHED"
        if schema.__name__ == "AssertionScript":
            # Revisions must strictly increase; replay may skip recorded rounds
            # once isolation removes the need for them.
            payload["revision"] = self.consumed.get(recorded_role, 1)
        return schema.model_validate(payload)

    def take_last_observation(self) -> None:
        return None

    def summary(self) -> dict[str, Any]:
        """Return how many recorded calls each role consumed."""

        available = {
            role: sum(1 for call in self.calls if call.role == role)
            for role in {call.role for call in self.calls}
        }
        return {
            "available": available,
            "consumed": dict(self.consumed),
            "overruns": dict(self.overruns),
            "synthesized": dict(self.synthesized),
        }


def _synthetic_response(schema: type[BaseModel]) -> BaseModel:
    """Neutral stand-in for a role the recorded run never reached.

    Deliberately minimal, and always counted in ``summary()["synthesized"]`` so
    a replay result can never be read as if the recording had covered that role.
    """

    name = schema.__name__
    if name == "AssertionReview":
        return schema.model_validate(
            {
                "decision": "accept",
                "reviewed_script_hash": "TO_BE_PATCHED",
                "rationale": (
                    "SYNTHETIC replay stand-in: the recorded run never reached "
                    "the Assertion Reviewer."
                ),
            }
        )
    if name == "DiscoverAdjudication":
        return schema.model_validate(
            {
                "has_confirmed_issues": False,
                "rationale": (
                    "SYNTHETIC replay stand-in: the recorded run never reached "
                    "adjudication."
                ),
            }
        )
    if name == "RequirementReview":
        return schema.model_validate(
            {
                "decision": "accept",
                "reviewed_revision": 1,
                "rationale": "SYNTHETIC replay stand-in.",
            }
        )
    raise LookupError(f"no synthetic stand-in for {name}")
