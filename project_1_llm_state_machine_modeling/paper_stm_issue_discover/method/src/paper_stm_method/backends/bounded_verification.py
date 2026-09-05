"""Bounded progress probes executed by the native FCSTM ``.fbmcq`` engine."""

from __future__ import annotations

from typing import Any

from ..compiler.lowering import PredicatePlan
from ..inputs.models import ModelIR
from .fcstm_native import (
    NativeFCSTM,
    all_states,
    execute_fbmcq,
    load_native_fcstm,
    native_load_failure,
    native_receipt,
    resolve_state,
    state_path,
)


def _v1_scope_states(native: NativeFCSTM, initial_scope: object) -> tuple[tuple[Any, ...], str | None]:
    """Restrict V1 to reachable native stable leaves in its execution scope.

    Root-closed V1 must not turn a structurally unreachable dead-end into a
    violation. Reachability comes from pyfcstm's native leaf-level topology
    projection; FBMCQ still supplies the actual progress verdict for each
    retained configuration. An explicit state scope is a hot initial scope, so
    its exact leaf and its native topology-reachable leaves are included.
    """

    from pyfcstm.verify.topology import topological_reachable_set, unreachable_states

    if initial_scope in (None, "closed_fcstm", "cold"):
        anchor = native.machine.root_state
        excluded = set(unreachable_states(native.machine))
        reachable = {
            state_path(state)
            for state in all_states(native)
            if state_path(state) not in excluded
        }
    else:
        anchor = resolve_state(native, initial_scope)
        if anchor is None:
            return (), "the V1 initial_scope does not resolve to one native FCSTM state"
        anchor_path = state_path(anchor)
        reachable = {
            anchor_path,
            *topological_reachable_set(native.machine).get(anchor_path, ()),
        }
    prefix = state_path(anchor) + "."
    states = tuple(
        state
        for state in all_states(native)
        if state.is_stoppable
        and state_path(state) in reachable
        and (state is anchor or state_path(state).startswith(prefix))
    )
    if not states:
        return (), "the declared V1 scope contains no native stable leaf configurations"
    return states, None


def _v1_progress_query(state: Any) -> str:
    """Ask FBMCQ for one real post-step configuration change from a stable leaf."""

    path = state_path(state)
    return (
        f'init state("{path}");\n'
        f'check reach <= 1: !active("{path}") || terminated();'
    )


def run_bounded_verification(plan: PredicatePlan, model: ModelIR, receipt_id: str):
    """Evaluate V1 through native FCSTM objects and FBMCQ only."""

    predicate = plan.predicate_id or "unknown"
    try:
        native = load_native_fcstm(model)
    except Exception as exc:  # noqa: BLE001 - preserve loader failure in execution audit.
        return native_load_failure(receipt_id, predicate, model, exc)
    inputs = plan.inputs

    if predicate == "V1":
        states, scope_error = _v1_scope_states(native, inputs.get("initial_scope"))
        if scope_error is not None:
            return native_receipt(receipt_id, predicate, native, "unknown", "V1 requires a closed scope of native stable nonterminal FCSTM configurations.", scope_error, backend_family="fbmcq", algorithm_version="pyfcstm.fbmcq.v1")
        probes: list[dict[str, Any]] = []
        blocked: list[dict[str, Any]] = []
        failures: list[dict[str, Any]] = []
        for state in states:
            probe = execute_fbmcq(
                receipt_id=f"{receipt_id}:{state_path(state)}",
                predicate=predicate,
                native=native,
                query=_v1_progress_query(state),
                reason="Native FBMCQ searched for a committed successor configuration from one exact stable leaf.",
                basis="native State.is_stoppable plus .fbmcq reach",
            )
            entry = {
                "state": state_path(state),
                "terminal_state": probe.terminal_state,
                "verdict": probe.verdict,
                "query": probe.run_metadata.get("fbmcq_query"),
                "solve": probe.run_metadata.get("fbmcq_solve"),
                "receipt": probe.to_dict(),
            }
            probes.append(entry)
            if probe.terminal_state != "completed" or probe.verdict not in {"true", "false"}:
                failures.append(entry)
            elif probe.verdict == "false":
                blocked.append(entry)
        metadata = {"v1_native_progress_probes": probes, "fbmcq_query_count": len(probes)}
        if failures:
            return native_receipt(receipt_id, predicate, native, "unknown", "At least one native V1 progress query did not reach a Boolean FBMCQ result; no deadlock verdict is claimed.", "per-state native V1 FBMCQ execution failure", backend_family="fbmcq", algorithm_version="pyfcstm.fbmcq.v1", metadata=metadata)
        verdict = "false" if blocked else "true"
        return native_receipt(receipt_id, predicate, native, verdict, "Every native stable leaf in the declared scope was checked for a real one-step successor configuration through FBMCQ.", "native State.is_stoppable and per-state .fbmcq reachability", backend_family="fbmcq", algorithm_version="pyfcstm.fbmcq.v1", counterexample=blocked, metadata=metadata)

    return native_receipt(receipt_id, predicate, native, "unknown", "The bounded backend received an unknown frozen predicate ID.", "explicit native bounded-verification dispatch boundary", backend_family="fbmcq", algorithm_version="pyfcstm.fbmcq.v1")


__all__ = ["run_bounded_verification"]
