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
    initial_state: str | None = None,
    initial_vars: dict[str, int | float] | None = None,
) -> dict[str, Any]:
    """Execute one exploratory cycle sequence against the frozen model."""

    model_sha256 = hashlib.sha256(model_text.encode("utf-8")).hexdigest()
    try:
        observation = SimulationAPI(model_text).simulate(
            cycles=cycles, initial_state=initial_state, initial_vars=initial_vars
        )
    except Exception as exc:
        return _recoverable_inconclusive_failure(
            execution_status=_execution_status_for_exception(exc),
            question=question,
            root_node_ids=root_node_ids,
            cycles=cycles,
            initial_state=initial_state,
            initial_vars=initial_vars,
            reason=reason,
            model_sha256=model_sha256,
            exc=exc,
        )
    cycle_records = [cycle.to_json()["data"] for cycle in observation.cycles]
    unconsumed_inputs = [
        event
        for cycle in cycle_records
        for event in cycle.get("unconsumed_events", [])
    ]
    causality_guidance = (
        " One or more supplied events were unconsumed. Do not attribute the final "
        "state to those events; for a local hot-start event proposition, put the "
        "event in the first caller cycle and verify source state, event consumption, "
        "and target state in order."
        if unconsumed_inputs
        else ""
    )
    return {
        "execution_status": "completed",
        "question": question,
        "root_node_ids": list(root_node_ids),
        "requested_cycles": cycles,
        "requested_initialization": observation.requested_initialization.to_json()["data"],
        "effective_initialization": observation.effective_initialization.to_json()["data"],
        "cycles": cycle_records,
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
            f"the same proposition.{causality_guidance}"
        ),
        "pass_criteria": (
            "The next semantic actions revise and evaluate the implicated assertion. Another exploratory "
            "call is justified only when this result exposes one distinct unresolved "
            "condition for the same stable Root ID and the next reason names it. "
            "If the proposition attributes a state change to an event, the recorded "
            "source state, consumed event, and resulting target state must align."
        ),
        "limitations": [
            "exploratory_trace_only",
            "cannot_project_root",
            "formal_assertion_still_requires_registered_eval_assert",
            "hot_start_requires_exact_state_and_complete_variables",
        ],
    }


def _execution_status_for_exception(exc: Exception) -> str:
    if isinstance(exc, ValueError):
        return "invalid_arguments"
    return "execution_error"


def _recoverable_inconclusive_failure(
    *,
    execution_status: str,
    question: str,
    root_node_ids: list[str],
    cycles: list[list[str]],
    initial_state: str | None,
    initial_vars: dict[str, int | float] | None,
    reason: str,
    model_sha256: str,
    exc: Exception,
) -> dict[str, Any]:
    return {
        "execution_status": execution_status,
        "evidence_status": "inconclusive",
        "question": question,
        "root_node_ids": list(root_node_ids),
        "requested_cycles": cycles,
        "requested_initialization": {
            "mode": "hot" if initial_state is not None else "cold",
            "state": initial_state,
            "variables": dict(initial_vars or {}),
        },
        "model_sha256": model_sha256,
        "reason": reason,
        "error": {
            "status": "recoverable",
            "type": type(exc).__name__,
            "message": str(exc),
        },
        "recommended_tools": ["observe_trace", "query_model"],
        "recommended_action": (
            "Treat this as recoverable inconclusive trace evidence, not a Root "
            "verdict. Correct the exact hot-start state/complete variables, event "
            "name, or cycle setup using the error details; query the frozen model "
            "when the exact state, variable, or event spelling is uncertain, then "
            "retry only the same stable Root if the named evidence gap remains."
        ),
        "pass_criteria": (
            "A corrected request completes with one relevant observation, or a "
            "precise model query resolves the same setup gap before revising and "
            "evaluating the registered assertion."
        ),
        "limitations": [
            "inconclusive_evidence",
            "recoverable_failure",
            "trace_not_observed",
            "cannot_project_root",
            "no_root_verdict",
        ],
    }


def build_tool(
    snapshot: dict[str, Any],
    *,
    max_calls_per_root: int | None = None,
    max_cycles_per_call: int | None = None,
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
        initial_state: str | None = None,
        initial_vars: dict[str, int | float] | None = None,
    ) -> dict[str, Any]:
        """Purpose
        -------
        Diagnose one named FCSTM cycle/setup gap against the frozen STM_0 so the
        Agent can repair a registered simulation assertion. This is
        a diagnostic microscope, not the formal Root-evaluation path.

        When to use
        -----------
        After the mandatory guide/task read phase, use it either once for a
        targeted provisional clause Root to determine exact initialization/events
        before registration, or after registration when an inconclusive result or
        coverage finding names one exact trace gap. Use the shortest distinguishing
        sequence and stop once the question is answered. Reuse the stable Root ID;
        never mint suffix variants or new IDs to prolong exploration.

        When not to use
        ----------------
        Do not enumerate event permutations, replay every requirement, duplicate
        an already registered `simulate(...)` assertion, search for any failure,
        perform a model-wide trace sweep, use it before reading the frozen task, or treat a successful/failed
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
        Optional `initial_state` plus `initial_vars` requests a hot start from one
        exact dotted state path; hot start requires every declared persistent
        variable value. With `initial_state=None`, optional partial `initial_vars`
        overrides only named declared variables while omitted variables retain
        declaration initializers; effective full values are returned. Omitting
        both fields preserves the default cold-start contract.
        A cold start needs a leading `[]`. A complete hot start does not. For a
        local "while in S, E leads to T" question, put E in the first hot-start
        caller cycle and verify that E is consumed and T follows that cycle;
        otherwise an event-free/completion transition may leave S before E.
        In hierarchical FCSTM execution, the same supplied event may appear
        more than once in one cycle's ``consumed_events`` while nested and
        ancestor-level forced transitions process it. Use membership in
        ``consumed_events`` plus absence from ``unconsumed_events``; never
        require an exact count of one or treat duplicate labels alone as an
        issue.
        `reason` explains why this exact bounded trace is necessary in the run
        content language. No filesystem paths, model text, arbitrary code, or
        expected outcome are accepted. Use the exact registered Root ID. Suffix
        variants such as ROOT-CLAUSE-005-01B are rejected rather than treated as a
        new proposition.

        Returns
        -------
        A structured result containing `execution_status`, the original question
        and Root IDs, requested cycles, requested/effective initialization
        records, one immutable observation per cycle, final observation, frozen
        `model_sha256`, original reason, and explicit `recommended_tools`,
        `recommended_action`, `pass_criteria`, and limitations. Each cycle
        includes index, terminal-safe ``is_ended``,
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
        cycle. Cold initialization remains default-compatible; hot initialization
        is delegated to pyfcstm only after the exact state and complete variable
        request has been sealed. It records public structured cycle results and
        never parses an exception message as a behavior fact.

        Event-causality interpretation
        ------------------------------
        Final-state equality alone does not prove that an input event caused the
        transition. Compare effective initialization and prior cycle state with
        the event cycle's input/consumed/unconsumed events and resulting active
        states. If the event is unconsumed or the target was reached earlier,
        treat the trace as insufficient for that causal proposition and follow
        the returned corrective guidance. Duplicate entries for one supplied
        event do not by themselves prove repeated external consumption or a
        model issue.

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
        attribution, formal proof, or Repair eligibility. Hot starts skip entry
        boundary actions by pyfcstm design and are setup evidence, not proof that
        the model can reach that state from cold initialization.

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

        if max_cycles_per_call is not None and len(cycles) > max_cycles_per_call:
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
            if max_calls_per_root is not None
            and calls_by_root[root_id] >= max_calls_per_root
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
            repr((question, tuple(root_node_ids), cycles, initial_state, initial_vars)).encode("utf-8")
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
                initial_state=initial_state,
                initial_vars=initial_vars,
                reason=reason,
            )
        except Exception as exc:
            return _recoverable_inconclusive_failure(
                execution_status=_execution_status_for_exception(exc),
                question=question,
                root_node_ids=root_node_ids,
                cycles=cycles,
                initial_state=initial_state,
                initial_vars=initial_vars,
                reason=reason,
                model_sha256=model_sha256,
                exc=exc,
            )
        if result.get("execution_status") != "completed":
            return result
        completed_requests.add(identity)
        for root_id in root_node_ids:
            calls_by_root[root_id] += 1
        registered = registered_root_ids() if registered_root_ids is not None else set()
        if not (set(root_node_ids) & registered):
            result["recommended_tools"] = ["register_coverage_plan"]
            result["recommended_action"] = (
                "Use this targeted pre-registration observation to finish the "
                "same provisional Root's positive assertion, then register the "
                "complete coverage plan. Do not expand into an inventory sweep."
            )
            result["pass_criteria"] = (
                "The complete plan registers one stable Root and an assertion whose "
                "initialization and event sequence match this observation."
            )
        return result

    return SimpleStructuredTool(
        func=observe_trace,
        name="observe_trace",
        description=observe_trace.__doc__ or "observe_trace",
        args_schema=ObserveTraceInput,
    )


__all__ = ["build_tool", "execute"]
