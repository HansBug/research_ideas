from __future__ import annotations

import hashlib
from collections import defaultdict
from typing import Any

from ..eval_env.simulation import SimulationAPI
from ..schemas.tools import ObserveTraceInput, SimpleStructuredTool


def _model_from_snapshot(snapshot: dict[str, Any]) -> tuple[str, str]:
    model = snapshot.get("model") if isinstance(snapshot.get("model"), dict) else {}
    text = model.get("content") or model.get("fcstm")
    digest = model.get("model_sha256") or model.get("sha256") or model.get("fcstm_sha256")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("observe_trace requires frozen FCSTM content")
    if not isinstance(digest, str) or not digest:
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return text, digest


def execute(
    model_text: str,
    *,
    question: str,
    root_node_ids: list[str],
    cycles: list[list[str]],
    reason: str,
) -> dict[str, Any]:
    """Execute one exploratory cycle sequence against the frozen model."""

    observation = SimulationAPI(model_text).simulate(cycles=cycles)
    return {
        "execution_status": "completed",
        "question": question,
        "root_node_ids": list(root_node_ids),
        "requested_cycles": cycles,
        "cycles": [cycle.to_json()["data"] for cycle in observation.cycles],
        "final": observation.final.to_json()["data"],
        "model_sha256": observation.model_sha256,
        "reason": reason,
        "limitations": [
            "exploratory_trace_only",
            "cannot_project_root",
            "formal_assertion_still_requires_registered_eval_assert",
        ],
    }


def build_tool(
    snapshot: dict[str, Any],
    *,
    max_calls_per_root: int = 2,
    max_cycles_per_call: int = 16,
) -> SimpleStructuredTool:
    """Build the bounded exploratory ``observe_trace`` tool."""

    model_text, model_sha256 = _model_from_snapshot(snapshot)
    calls_by_root: dict[str, int] = defaultdict(int)
    completed_requests: set[str] = set()

    def observe_trace(
        question: str,
        root_node_ids: list[str],
        cycles: list[list[str]],
        reason: str,
    ) -> dict[str, Any]:
        """Purpose
        -------
        Explore one named FCSTM cycle/setup question against the frozen STM_0 so
        the Agent can design or repair a registered simulation assertion. This is
        a diagnostic microscope, not the formal Root-evaluation path.

        When to use
        -----------
        Use only when the frozen inventory does not reveal the exact explicit
        setup cycles needed by a named Root, especially around hierarchy,
        eventless transitions, or a deep state. Use the shortest distinguishing
        sequence and stop once the question is answered.

        When not to use
        ----------------
        Do not enumerate event permutations, replay every requirement, duplicate
        an already registered `simulate(...)` assertion, search for any failure,
        or treat a successful/failed trace as a Root verdict. Final evidence must
        still be a registered latest expression executed through `eval_assert`.

        Parameters
        ----------
        `question` is one concrete evidence gap, not a generic request to inspect
        the model. `root_node_ids` is a non-empty list of affected registered or
        planned Root IDs. `cycles` is a non-empty `list[list[str]]`: each outer
        item is exactly one FCSTM cycle and each inner list is the complete event
        set supplied in that cycle; `[]` is an explicit eventless/init cycle.
        `reason` explains why this exact bounded trace is necessary in the run
        content language. No paths, model text, arbitrary code, or expected
        outcome are accepted.

        Returns
        -------
        A structured result containing `execution_status`, the original question
        and Root IDs, requested cycles, one immutable observation per cycle,
        final observation, frozen `model_sha256`, original reason, and
        limitations. Each cycle includes index, terminal-safe ``is_ended``,
        active states, variables, input/consumed/unconsumed events,
        fired-transition field, and limitations. A completed top-level machine
        is reported as ``is_ended=true`` with empty active states; do not append
        another cycle after termination or infer completion by querying an
        active state that no longer exists.

        Execution
        ---------
        Validate budgets and duplicate identity, then call pyfcstm
        `SimulationRuntime.cycle` exactly once for every caller-provided outer
        cycle. The wrapper inserts no hidden initialization or stabilization
        cycle. It records public structured cycle results and never parses an
        exception message as a behavior fact.

        Failure semantics
        -----------------
        Empty/malformed cycles, unknown event names, runtime errors, duplicate
        requests, more than the configured calls per Root, or too many cycles
        fail closed. They do not create an assertion result or Root verdict.

        Evidence limitations
        --------------------
        One finite trace supports only the supplied sequence. It cannot establish
        absence of another behavior, global correctness, NL completeness, source
        attribution, formal proof, or Repair eligibility.

        Permissions
        -----------
        Read-only current frozen model only. No arbitrary paths, alternate
        run/case/model, network, shell, Python/Z3, writes, mutation,
        reference/gold data, Repair, Confirm, or final submission.

        Examples
        --------
        `{"question":"Does the eventless transition after interception require an explicit empty cycle?","root_node_ids":["ROOT-002"],"cycles":[[],["Root.Interception_Detected"],[]],"reason":"Determine the shortest setup before registering ROOT-002's simulation assertion."}`

        For a top-level final target use a terminal-safe sequence such as
        `{"question":"Does stop terminate the machine?","root_node_ids":["ROOT-003"],"cycles":[[],["Root.stop"]],"reason":"Observe the final cycle's is_ended flag before registering the completion assertion."}`.
        """

        if len(cycles) > max_cycles_per_call:
            return {
                "execution_status": "invalid_arguments",
                "question": question,
                "root_node_ids": root_node_ids,
                "model_sha256": model_sha256,
                "reason": reason,
                "limitations": ["max_cycles_per_observe_exceeded"],
            }
        exhausted = sorted(
            root_id
            for root_id in root_node_ids
            if calls_by_root[root_id] >= max_calls_per_root
        )
        if exhausted:
            return {
                "execution_status": "invalid_arguments",
                "question": question,
                "root_node_ids": root_node_ids,
                "model_sha256": model_sha256,
                "reason": reason,
                "limitations": ["max_observe_trace_calls_per_root_exceeded", *exhausted],
            }
        identity = hashlib.sha256(
            repr((question, tuple(root_node_ids), cycles)).encode("utf-8")
        ).hexdigest()
        if identity in completed_requests:
            return {
                "execution_status": "invalid_arguments",
                "question": question,
                "root_node_ids": root_node_ids,
                "model_sha256": model_sha256,
                "reason": reason,
                "limitations": ["duplicate_trace_request_not_executed"],
            }
        try:
            result = execute(
                model_text,
                question=question,
                root_node_ids=root_node_ids,
                cycles=cycles,
                reason=reason,
            )
        except Exception as exc:
            return {
                "execution_status": "execution_error",
                "question": question,
                "root_node_ids": root_node_ids,
                "model_sha256": model_sha256,
                "reason": reason,
                "error": {"type": type(exc).__name__, "message": str(exc)},
                "limitations": ["trace_not_observed", "cannot_project_root"],
            }
        completed_requests.add(identity)
        for root_id in root_node_ids:
            calls_by_root[root_id] += 1
        return result

    return SimpleStructuredTool(
        func=observe_trace,
        name="observe_trace",
        description=observe_trace.__doc__ or "observe_trace",
        args_schema=ObserveTraceInput,
    )


__all__ = ["build_tool", "execute"]
