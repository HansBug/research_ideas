from __future__ import annotations

import hashlib
from collections import defaultdict
from collections.abc import Callable
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


def _provisional_root_ids(snapshot: dict[str, Any]) -> set[str]:
    current = snapshot.get("current_records")
    if not isinstance(current, dict):
        return set()
    requirements = current.get("coverage_requirements")
    if not isinstance(requirements, list):
        return set()
    return {
        f"ROOT-{item['clause_id']}"
        for item in requirements
        if isinstance(item, dict)
        and isinstance(item.get("clause_id"), str)
        and item["clause_id"]
    }


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
        "recommended_tools": [
            "revise_assertion",
            "eval_assert",
        ],
        "recommended_action": (
            "Use this post-registration observation immediately to revise the "
            "implicated registered assertion and execute its latest version. Do not enumerate "
            "unrelated event/state combinations or mint a new Root ID to continue "
            "the same proposition."
        ),
        "pass_criteria": (
            "The next semantic actions revise and evaluate the implicated assertion. Another exploratory "
            "call is justified only when this result exposes one distinct unresolved "
            "condition for the same stable Root ID and the next reason names it."
        ),
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
    registered_root_ids: Callable[[], set[str]] | None = None,
) -> SimpleStructuredTool:
    """Build the bounded exploratory ``observe_trace`` tool."""

    model_text, model_sha256 = _model_from_snapshot(snapshot)
    provisional_root_ids = _provisional_root_ids(snapshot)
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
        Diagnose one named FCSTM cycle/setup gap against the frozen STM_0 so the
        Agent can repair a registered simulation assertion. This is
        a diagnostic microscope, not the formal Root-evaluation path.

        When to use
        -----------
        Use only after successful plan registration, and only when a latest
        registered evaluation is inconclusive or a failed coverage review explicitly
        names this tool and one exact trace gap. Use the shortest distinguishing
        sequence and stop once the question is answered. Reuse the exact registered
        Root ID; never mint suffix variants or new IDs to prolong exploration.

        When not to use
        ----------------
        Do not enumerate event permutations, replay every requirement, duplicate
        an already registered `simulate(...)` assertion, search for any failure,
        perform a model-wide trace sweep, use this tool before registration, or treat a successful/failed
        trace as a Root verdict. When the result answers the named question, the
        next semantic actions must be `revise_assertion` followed by `eval_assert`. Another
        trace is justified only by one distinct unresolved condition exposed by
        the result for the same stable Root ID. Final evidence must still be a
        registered latest expression executed through `eval_assert`.

        Parameters
        ----------
        `question` is one concrete evidence gap, not a generic request to inspect
        the model. `root_node_ids` is a non-empty list of affected registered Root
        IDs. `cycles` is a non-empty `list[list[str]]`: each outer
        item is exactly one FCSTM cycle and each inner list is the complete event
        set supplied in that cycle; `[]` is an explicit eventless/init cycle.
        `reason` explains why this exact bounded trace is necessary in the run
        content language. No paths, model text, arbitrary code, or expected
        outcome are accepted. Use the exact registered Root ID. Suffix variants such as
        ROOT-CLAUSE-005-01B are rejected rather than treated as a new proposition.

        Returns
        -------
        A structured result containing `execution_status`, the original question
        and Root IDs, requested cycles, one immutable observation per cycle,
        final observation, frozen `model_sha256`, original reason, and
        explicit `recommended_tools`, `recommended_action`, `pass_criteria`, and
        limitations. Each cycle includes index, terminal-safe ``is_ended``,
        active states, variables, input/consumed/unconsumed events,
        fired-transition field, and limitations. A completed top-level machine
        is reported as ``is_ended=true`` with empty active states; do not append
        another cycle after termination or infer completion by querying an
        active state that no longer exists.

        Execution
        ---------
        Validate stable Root identity, budgets, and duplicate identity, then call pyfcstm
        `SimulationRuntime.cycle` exactly once for every caller-provided outer
        cycle. The wrapper inserts no hidden initialization or stabilization
        cycle. It records public structured cycle results and never parses an
        exception message as a behavior fact.

        Failure semantics
        -----------------
        Empty/malformed cycles, unknown or suffixed Root IDs, unknown event names,
        runtime errors, duplicate requests, more than the configured calls per
        Root, or too many cycles fail closed. They do not create an assertion
        result or Root verdict. Every failure returns a corrective action and pass
        criterion; minting a new Root ID is never a valid recovery.

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
        `{"question":"Does the eventless transition after interception require an explicit empty cycle?","root_node_ids":["ROOT-002"],"cycles":[[],["Root.Interception_Detected"],[]],"reason":"Resolve the failed review's setup gap before revising ROOT-002's simulation assertion."}`

        For a top-level final target use a terminal-safe sequence such as
        `{"question":"Does stop terminate the machine?","root_node_ids":["ROOT-003"],"cycles":[[],["Root.stop"]],"reason":"Observe the final cycle's is_ended flag before revising the registered completion assertion."}`.
        """

        allowed_root_ids = set(provisional_root_ids)
        if registered_root_ids is not None:
            allowed_root_ids.update(registered_root_ids())
        invalid_root_ids = sorted(set(root_node_ids) - allowed_root_ids)
        if invalid_root_ids:
            return {
                "execution_status": "invalid_arguments",
                "question": question,
                "root_node_ids": root_node_ids,
                "model_sha256": model_sha256,
                "reason": reason,
                "allowed_root_ids": sorted(allowed_root_ids),
                "recommended_tools": ["observe_trace"],
                "recommended_action": (
                    "Use the exact registered Root ID named by the inconclusive "
                    "evaluation or failed review. Do not add a suffix or mint a "
                    "replacement ID to bypass prior exploration."
                ),
                "pass_criteria": (
                    "The next semantic action uses an allowed stable Root ID and "
                    "answers the named post-registration gap without replaying the same proposition under a new identity."
                ),
                "limitations": ["unstable_or_unknown_root_id", *invalid_root_ids],
            }

        if len(cycles) > max_cycles_per_call:
            return {
                "execution_status": "invalid_arguments",
                "question": question,
                "root_node_ids": root_node_ids,
                "model_sha256": model_sha256,
                "reason": reason,
                "recommended_tools": ["observe_trace"],
                "recommended_action": (
                    "Shorten the sequence to the minimum cycles that distinguish "
                    "the named question, then retry with the same stable Root ID."
                ),
                "pass_criteria": (
                    f"The corrected request has at most {max_cycles_per_call} cycles "
                    "and tests only the named uncertainty."
                ),
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
                "recommended_tools": [
                    "revise_assertion",
                    "eval_assert",
                ],
                "recommended_action": (
                    "Do not mint a replacement Root ID. Use the observations already "
                    "collected for this proposition to revise and evaluate the implicated assertion."
                ),
                "pass_criteria": (
                    "The next semantic action advances the existing stable Root into revised executable evidence without another trace."
                ),
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
                "recommended_tools": [
                    "revise_assertion",
                    "eval_assert",
                ],
                "recommended_action": (
                    "Do not repeat or cosmetically rewrite this request. Incorporate "
                    "the existing observation into the latest registered assertion."
                ),
                "pass_criteria": (
                    "The next semantic action changes the ledger by assertion revision or latest assertion execution."
                ),
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
                "recommended_tools": ["observe_trace", "query_model"],
                "recommended_action": (
                    "Use the error details to correct the exact event name or cycle "
                    "setup. Retry the same stable Root only if the named uncertainty "
                    "remains; otherwise inspect the precise model relation and revise the registered assertion."
                ),
                "pass_criteria": (
                    "A corrected request completes with a relevant observation, or a "
                    "precise model query resolves the same named evidence gap."
                ),
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
