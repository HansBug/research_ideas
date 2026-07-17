from __future__ import annotations

import copy
from collections.abc import Callable
from typing import Any

from ..schemas.tools import ObserveTraceInput, TraceObservation, SimpleStructuredTool
from .post_batch_investigation import PostBatchInvestigationState

_LIMITATIONS = [
    "exploratory_trace_only",
    "single_trace_cannot_prove_correctness",
    "bounded_to_frozen_model",
]


def _model_sha256_from(snapshot: dict[str, Any]) -> str:
    for key in ("model_sha256", "fcstm_sha256"):
        value = snapshot.get(key)
        if isinstance(value, str) and value:
            return value
    model = snapshot.get("model")
    if isinstance(model, dict):
        for key in ("model_sha256", "fcstm_sha256"):
            value = model.get(key)
            if isinstance(value, str) and value:
                return value
    return "unknown"


def _known_events(snapshot: dict[str, Any]) -> set[str]:
    inspect = snapshot.get("normalized_inspect") or snapshot.get("inspect")
    if not isinstance(inspect, dict) and isinstance(snapshot.get("model"), dict):
        inspect = snapshot["model"].get("normalized_inspect") or snapshot["model"].get("inspect")
    events: set[str] = set()
    if isinstance(inspect, dict):
        for item in inspect.get("events", []) or []:
            if isinstance(item, dict):
                for key in ("qualified_name", "name", "path"):
                    value = item.get(key)
                    if isinstance(value, str) and value:
                        events.add(value)
            elif isinstance(item, str):
                events.add(item)
    return events


def _normalize_runner_result(raw: Any, requested_events: list[str], model_sha256: str) -> dict[str, Any]:
    if not isinstance(raw, dict):
        return TraceObservation(
            execution_status="execution_error",
            model_sha256=model_sha256,
            requested_events=requested_events,
            input_events=requested_events,
            diagnostics=[{"code": "runner_returned_non_object", "severity": "error"}],
            limitations=[*_LIMITATIONS, "runner_result_not_structured"],
        ).model_dump(mode="json")
    status = raw.get("execution_status") or raw.get("status") or "completed"
    if status not in {"completed", "invalid_arguments", "tool_unavailable", "execution_error", "unknown", "timeout", "incomplete"}:
        status = "execution_error"
    consumed = raw.get("consumed_events") or raw.get("consumed") or []
    unconsumed = raw.get("unconsumed_events") or [event for event in requested_events if event not in consumed]
    cycles = raw.get("cycles")
    if not isinstance(cycles, int) or cycles < 0:
        cycles = len(consumed) if isinstance(consumed, list) else 0
    final_configuration = raw.get("final_configuration") or {}
    if not final_configuration:
        current_state = raw.get("current_state") or raw.get("state")
        if current_state is not None:
            final_configuration = {"current_state": current_state}
    diagnostics = raw.get("diagnostics") or raw.get("errors") or []
    if isinstance(diagnostics, dict):
        diagnostics = [diagnostics]
    diagnostics = [item if isinstance(item, dict) else {"message": str(item)} for item in diagnostics]
    return TraceObservation(
        execution_status=status,  # type: ignore[arg-type]
        model_sha256=str(raw.get("model_sha256") or model_sha256),
        requested_events=requested_events,
        cycles=cycles,
        input_events=list(raw.get("input_events") or requested_events),
        consumed_events=list(consumed) if isinstance(consumed, list) else [],
        unconsumed_events=list(unconsumed) if isinstance(unconsumed, list) else [],
        final_configuration=final_configuration if isinstance(final_configuration, dict) else {"value": final_configuration},
        diagnostics=diagnostics,
        limitations=[*_LIMITATIONS, *list(raw.get("limitations", []) or [])],
    ).model_dump(mode="json")


def execute(
    model_text: str,
    events: list[str],
    model_path: str = "<memory>",
    max_steps: int | None = None,
    runner: Callable[..., Any] | None = None,
    model_sha256: str = "unknown",
) -> dict[str, Any]:
    """Purpose: observe one finite event trace on the frozen current STM.

    Parameters: ``model_text`` and ``model_path`` are controller-bound legacy
    compatibility inputs, not Agent parameters; new Agent registration should use
    ``build_tool`` so the model is closed over.  Agent parameters are ``events``
    (a JSON list of qualified event strings) and optional positive ``max_steps``.
    ``runner`` is an injected deterministic simulation callable for tests or the
    controller; it may accept ``events`` and ``max_steps`` by keyword or position.
    The Agent cannot pass arbitrary paths, alternate model text, run id, case id,
    URL, shell command, Python/Z3, or reference/gold data.

    Returns: ``TraceObservation`` with ``execution_status``, ``model_sha256``,
    ``requested_events``, ``cycles``, ``input_events``, ``consumed_events``,
    ``unconsumed_events``, ``final_configuration``, ``diagnostics``, and
    ``limitations``.  Empty, unknown, or over-budget traces are structured
    failures rather than raw exceptions.

    Execution: validates arguments, checks the step bound, invokes the injected
    deterministic runner when supplied, and normalizes its structured result.  If
    no runner is supplied, a conservative ``tool_unavailable`` result is returned
    instead of attempting hidden filesystem or simulator access.

    Failure semantics: empty event list, invalid event names, or ``max_steps``
    smaller than the requested sequence return ``invalid_arguments``. Runner
    exceptions return ``execution_error`` with a code only. Runner timeout/unknown
    statuses are preserved as structured statuses and never converted to pass.

    Evidence limitations: this is a post-batch diagnostic microscope, not a
    coverage engine. It must not be used for exhaustive event permutation,
    repeated-prefix search, or duplicating scenarios already executed by
    ``evaluate_checks``. A trace is an observation of one bounded path. Even a
    clean no-counterexample trace cannot prove global correctness, NL alignment,
    source closure, property satisfaction, absence of bugs, or repair success.

    Permissions: read-only against the frozen model; no arbitrary paths, model
    replacement, run/case selector, network, shell, Python/Z3 execution, writes,
    or reference/gold access.

    Example: with a runner returning ``{"execution_status":"completed","consumed_events":["Root.go"],"final_configuration":{"state":"Root.Done"}}``, ``execute("...", ["Root.go"], runner=runner, model_sha256="m1")`` returns a ``TraceObservation`` with ``consumed_events=["Root.go"]`` and ``model_sha256="m1"``.
    """

    try:
        params = ObserveTraceInput.model_validate({"events": events, "max_steps": max_steps})
    except Exception as exc:
        return TraceObservation(
            execution_status="invalid_arguments",
            model_sha256=model_sha256,
            requested_events=events if isinstance(events, list) else [],
            input_events=events if isinstance(events, list) else [],
            diagnostics=[{"code": "invalid_arguments", "kind": type(exc).__name__}],
            limitations=[*_LIMITATIONS, "invalid_arguments"],
        ).model_dump(mode="json")
    if not params.events or any(not isinstance(event, str) or not event.strip() for event in params.events):
        return TraceObservation(
            execution_status="invalid_arguments",
            model_sha256=model_sha256,
            requested_events=params.events,
            input_events=params.events,
            diagnostics=[{"code": "empty_or_invalid_event_sequence", "severity": "error"}],
            limitations=[*_LIMITATIONS, "event_sequence_must_be_non_empty"],
        ).model_dump(mode="json")
    if params.max_steps is not None and len(params.events) > params.max_steps:
        return TraceObservation(
            execution_status="invalid_arguments",
            model_sha256=model_sha256,
            requested_events=params.events,
            input_events=params.events,
            unconsumed_events=params.events,
            diagnostics=[{"code": "max_steps_less_than_event_count", "severity": "error"}],
            limitations=[*_LIMITATIONS, "bounded_step_limit_exceeded"],
        ).model_dump(mode="json")
    if runner is None:
        return TraceObservation(
            execution_status="tool_unavailable",
            model_sha256=model_sha256,
            requested_events=params.events,
            input_events=params.events,
            unconsumed_events=params.events,
            diagnostics=[{"code": "deterministic_trace_runner_unavailable", "severity": "error"}],
            limitations=[*_LIMITATIONS, "runner_required"],
        ).model_dump(mode="json")
    try:
        try:
            raw = runner(events=params.events, max_steps=params.max_steps)
        except TypeError:
            raw = runner(params.events, params.max_steps)
    except TimeoutError:
        return TraceObservation(
            execution_status="timeout",
            model_sha256=model_sha256,
            requested_events=params.events,
            input_events=params.events,
            unconsumed_events=params.events,
            diagnostics=[{"code": "runner_timeout", "severity": "error"}],
            limitations=[*_LIMITATIONS, "timeout_not_pass"],
        ).model_dump(mode="json")
    except Exception as exc:
        return TraceObservation(
            execution_status="execution_error",
            model_sha256=model_sha256,
            requested_events=params.events,
            input_events=params.events,
            unconsumed_events=params.events,
            diagnostics=[{"code": "runner_exception", "kind": type(exc).__name__, "severity": "error"}],
            limitations=[*_LIMITATIONS, "exception_message_not_evidence"],
        ).model_dump(mode="json")
    return _normalize_runner_result(raw, params.events, model_sha256)


def build_tool(
    snapshot: dict[str, Any],
    runner: Callable[..., Any] | None,
    investigation_state: PostBatchInvestigationState | None = None,
) -> SimpleStructuredTool:
    """Purpose: create ``observe_trace`` bound to the current frozen model.

    Parameters: ``snapshot`` supplies the frozen model hash and optional inspect
    event names; ``runner`` is an injected deterministic simulation callable owned
    by the controller/test harness.  Agents only provide ``ObserveTraceInput``.

    Returns: a ``StructuredTool`` named ``observe_trace`` with strict input schema
    and ``TraceObservation`` output semantics.

    Execution: when a protocol state is supplied, requires one distinct eligible
    ``evaluate_checks`` batch and permits one completed trace microscope for that
    batch; then validates events and delegates to the injected runner.

    Failure semantics: unknown events, empty sequence, over-budget steps, missing
    runner, runner timeout, and runner exception each produce structured status;
    none is silently treated as a clean trace.

    Evidence limitations: optional exploratory evidence only; one trace cannot
    confirm correctness, source closure, or repair eligibility by itself.

    Permissions: no Agent-supplied model/path/run/case/network/shell/Python/Z3 or
    reference/gold inputs; no writes.

    Example: ``build_tool(snapshot, runner).invoke({"events":["Root.go"],"max_steps":3})`` returns a ``TraceObservation`` tied to ``snapshot``'s model hash.
    """

    frozen = copy.deepcopy(snapshot)
    model_sha256 = _model_sha256_from(frozen)
    known_events = _known_events(frozen)

    def observe_trace(events: list[str], max_steps: int | None = None) -> dict[str, Any]:
        """Purpose
        -------
        Execute one exploratory, finite event sequence against the frozen current
        ``STM_0`` to answer a concrete diagnostic question that remains after an
        eligible full-batch ``evaluate_checks`` result. The Controller enforces
        at most one completed trace microscope per distinct eligible draft-batch
        hash; re-evaluating the same drafts does not reopen trace exploration.
        Use it to distinguish one
        named uncertainty about consumption, stutter/no-progress behavior, reached
        configuration, or runtime diagnostics. It is not a coverage engine: do
        not enumerate event permutations, duplicate evaluated scenarios, repeat
        a prefix family, search all traces, or produce an issue/quality verdict.

        Parameters
        ----------
        ``events`` (required JSON array of strings): non-empty ordered sequence of
        qualified event identifiers known to frozen inspect, for example
        ``["Root.start", "Root.stop"]``. Order is execution order; each item is
        offered in a separate cycle by the bound runner.
        ``max_steps`` (optional positive integer or null): execution cap. When
        supplied it must be at least the number of requested events. It limits
        this observation only and does not change the model or global profile.
        The strict input accepts no initial state, variables, model text, path,
        run/case ID, arbitrary action, or extra field.

        Returns
        -------
        A ``TraceObservation`` JSON object:

        - ``execution_status``: ``completed``, ``invalid_arguments``,
          ``tool_unavailable``, ``execution_error``, ``unknown``, ``timeout``, or
          ``incomplete``.
        - ``model_sha256``: frozen model identity.
        - ``requested_events``: exact validated request order.
        - ``cycles``: number of normalized runtime cycles represented.
        - ``input_events``: events actually offered to the runner.
        - ``consumed_events`` / ``unconsumed_events``: explicit accounting; an
          unconsumed event is an observation, not automatically a defect.
        - ``final_configuration``: runner-reported active state/configuration.
        - ``diagnostics``: structured runtime diagnostics, never hidden prose.
        - ``limitations``: boundedness and failure/interpretation constraints.

        Execution
        ---------
        1. Require a distinct eligible full-batch ``evaluate_checks`` result and
           reject repeated trace exploration for the same draft-batch hash.
        2. Validate non-empty strings, qualified names against frozen inspect when
           available, and ``max_steps``.
        3. Invoke the Controller-injected deterministic runner on the already bound
           model; no model/path argument is accepted from the Agent.
        4. Normalize cycles, event accounting, final configuration, diagnostics,
           status, and model hash into the strict output schema.
        5. Preserve timeout/unknown/incomplete/error instead of coercing them to a
           successful domain observation. No latest-state reload or record update
           occurs.

        Failure semantics
        -----------------
        Missing eligible evaluation returns ``prerequisite_required``. A second
        trace for the same eligible draft batch returns ``invalid_arguments`` and
        must not be retried. Empty/non-string events, unknown qualified event, or too-small/nonpositive
        ``max_steps`` returns ``invalid_arguments`` without execution. Missing
        runner returns ``tool_unavailable``. Runner exception/non-object output is
        ``execution_error``. Timeout, unknown, and incomplete remain distinct.
        A completed trace with unconsumed events is still a completed tool call;
        its behavioral meaning must be compared with NL/source expectations.

        Evidence limitations
        --------------------
        ``evaluate_checks`` owns batch coverage. This tool is only for the shortest
        distinguishing sequence needed by a remaining named evidence gap; stop
        after that gap is answered. A finite trace may illustrate or refute one proposition under that exact
        input order. It cannot independently prove global correctness, absence of
        another path, NL alignment, source closure, unbounded reachability or
        unreachability, completeness, or a confirmed issue. A no-counterexample
        observation is never a proof. Always cite the model hash and limitations.

        Permissions
        -----------
        Read-only execution of the current-attempt frozen model. No arbitrary
        paths, alternate model/run/case, custom initial snapshot, network, shell,
        Python/Z3, mutation, writes, future-stage data, or hidden reference/gold
        assets.

        Example
        -------
        Input ``{"events":["Root.go"],"max_steps":2}`` may return
        ``{"execution_status":"completed","model_sha256":"...","requested_events":["Root.go"],"cycles":1,"input_events":["Root.go"],"consumed_events":["Root.go"],"unconsumed_events":[],"final_configuration":{"current_state":"Root.Done"},"diagnostics":[],"limitations":[...]}``.
        """

        batch_sha256 = (
            investigation_state.latest_eligible_batch()
            if investigation_state is not None
            else None
        )
        if investigation_state is not None and batch_sha256 is None:
            return TraceObservation(
                execution_status="prerequisite_required",
                model_sha256=model_sha256,
                requested_events=events,
                input_events=events,
                unconsumed_events=events,
                diagnostics=[
                    {
                        "code": "eligible_evaluate_checks_required_first",
                        "severity": "error",
                    }
                ],
                limitations=[*_LIMITATIONS, "post_batch_investigation_only"],
            ).model_dump(mode="json")
        if (
            investigation_state is not None
            and batch_sha256 is not None
            and investigation_state.already_completed("observe_trace", batch_sha256)
        ):
            return TraceObservation(
                execution_status="invalid_arguments",
                model_sha256=model_sha256,
                requested_events=events,
                input_events=events,
                unconsumed_events=events,
                diagnostics=[
                    {
                        "code": "post_batch_trace_already_completed",
                        "severity": "error",
                    }
                ],
                limitations=[*_LIMITATIONS, "one_trace_per_distinct_eligible_batch"],
            ).model_dump(mode="json")
        if known_events:
            unknown = [event for event in events if event not in known_events]
            if unknown:
                return TraceObservation(
                    execution_status="invalid_arguments",
                    model_sha256=model_sha256,
                    requested_events=events,
                    input_events=events,
                    unconsumed_events=events,
                    diagnostics=[{"code": "unknown_event", "refs": unknown, "severity": "error"}],
                    limitations=[*_LIMITATIONS, "unknown_event_not_executed"],
                ).model_dump(mode="json")
        result = execute("", events, "<frozen>", max_steps, runner, model_sha256)
        if (
            investigation_state is not None
            and batch_sha256 is not None
            and result.get("execution_status") == "completed"
        ):
            investigation_state.mark_completed("observe_trace", batch_sha256)
        return result

    return SimpleStructuredTool(func=observe_trace, name="observe_trace", description=observe_trace.__doc__ or "observe_trace", args_schema=ObserveTraceInput)
