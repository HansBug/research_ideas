"""Native FCSTM execution adapters shared by every frozen predicate backend.

``ModelIR`` remains an attribution and binding projection.  Predicate truth is
always obtained from a freshly loaded :class:`pyfcstm.model.StateMachine`, its
public verification APIs, ``SimulationRuntime``, or a compiled ``.fbmcq``
query.  Keeping this boundary in one module prevents a future backend from
silently treating the lightweight projection as an execution model.
"""

from __future__ import annotations

import hashlib
import multiprocessing
import os
import queue
import time
from pathlib import Path
from typing import Any

from ..evidence.receipts import RawReceipt
from ..inputs.fcstm_native_projection import (
    NativeFCSTMDocument as NativeFCSTM,
    NativeFCSTMError,
    NativeTransitionCarrier,
    all_events,
    all_states,
    all_transition_carriers,
    all_transitions,
    load_native_document,
    native_transition_endpoints,
    resolve_event,
    resolve_state,
    resolve_state_paths,
    state_path,
    transition_by_reference,
    transition_owner_path,
)
from ..inputs.models import ModelIR

def load_native_fcstm(model: ModelIR) -> NativeFCSTM:
    """Load the exact closed FCSTM source used by the current predicate plan."""

    return load_native_document(model.source_text)


def transition_by_ref(native: NativeFCSTM, reference: object) -> NativeTransitionCarrier | None:
    """Resolve one source reference through native spans and combo provenance."""

    return transition_by_reference(native, reference)


def parse_effect_operation(native: NativeFCSTM, value: object) -> Any | None:
    """Parse one requirement-side effect with the native FCSTM operation grammar.

    The synthetic wrapper carries the current native declaration environment and
    is parsed by ``pyfcstm`` itself.  It never interprets the inspected FCSTM
    source with method-owned text logic.  A null result means the supplied
    requirement phrase is not one executable FCSTM operation and must not
    become an S6 verdict.
    """

    if not isinstance(value, str) or not value.strip():
        return None
    declarations = "\n".join(
        str(definition.to_ast_node())
        for definition in native.machine.defines.values()
    )
    effect = value.strip()
    if effect.endswith(";"):
        effect = effect[:-1].rstrip()
    wrapper_source = "\n".join(
        part
        for part in (
            declarations,
            "state EvidenceDiscoveryEffectWrapper {",
            "    state Carrier;",
            "    state Sink;",
            "    [*] -> Carrier;",
            f"    Carrier -> Sink effect {{ {effect}; }};",
            "}",
        )
        if part
    )
    try:
        from pyfcstm.model import load_state_machine_from_text

        wrapper = load_state_machine_from_text(wrapper_source)
    except Exception:  # noqa: BLE001 - invalid typed input is not a verdict.
        return None
    carriers = [
        transition
        for transition in wrapper.root_state.transitions
        if transition.from_state == "Carrier" and transition.to_state == "Sink"
    ]
    if len(carriers) != 1 or len(carriers[0].effects) != 1:
        return None
    return carriers[0].effects[0].to_ast_node()


def native_receipt(
    receipt_id: str,
    predicate: str,
    native: NativeFCSTM,
    verdict: str,
    reason: str,
    basis: str,
    *,
    backend_family: str,
    algorithm_version: str,
    terminal_state: str | None = None,
    counterexample: list[dict[str, Any]] | None = None,
    trace: list[dict[str, Any]] | None = None,
    metadata: dict[str, Any] | None = None,
    failure_kind: str | None = None,
) -> RawReceipt:
    """Build a receipt whose execution identity names the native FCSTM engine."""

    run_metadata = {
        "algorithm_version": algorithm_version,
        "execution_model": "pyfcstm.model.StateMachine",
        "fcstm_source_hash": native.source_hash,
        "closed_input": True,
    }
    if metadata:
        run_metadata.update(metadata)
    if failure_kind is not None:
        run_metadata["failure_kind"] = failure_kind
    return RawReceipt(
        receipt_id=receipt_id,
        backend=f"{backend_family}:{predicate}",
        terminal_state=terminal_state or ("completed" if verdict in {"true", "false"} else "unsupported"),
        verdict=verdict,
        reason=reason,
        basis=basis,
        counterexample=counterexample or [],
        trace=trace or [],
        run_metadata=run_metadata,
    )


def native_load_failure(receipt_id: str, predicate: str, model: ModelIR, exc: Exception) -> RawReceipt:
    """Preserve a native-loader failure as a failed execution audit record."""

    source_hash = "sha256:" + hashlib.sha256(model.source_text.encode("utf-8")).hexdigest()
    return RawReceipt(
        receipt_id=receipt_id,
        backend=f"fcstm_native:{predicate}",
        terminal_state="error",
        verdict="unknown",
        reason="The closed FCSTM artifact could not be loaded by the native pyfcstm model implementation; no predicate verdict is claimed.",
        basis=f"pyfcstm.model.load_state_machine_from_text; exception={type(exc).__name__}: {exc}",
        run_metadata={
            "algorithm_version": "fcstm-native-loader.v1",
            "execution_model": "pyfcstm.model.StateMachine",
            "fcstm_source_hash": source_hash,
            "closed_input": True,
            "failure_kind": "backend_error",
        },
    )


_DEFAULT_FBMCQ_WALL_CLOCK_TIMEOUT_MS = 15_000
_DEFAULT_FBMCQ_MEMORY_LIMIT_BYTES = 2 * 1024 * 1024 * 1024
_FBMCQ_ALGORITHM_VERSION = "pyfcstm.fbmcq.isolated.v2"


def _configured_positive_int(name: str, default: int) -> int:
    """Read one positive local execution limit without making configuration fatal."""

    value = os.environ.get(name)
    if value is None:
        return default
    try:
        parsed = int(value)
    except ValueError:
        return default
    return parsed if parsed > 0 else default


def fbmcq_wall_clock_timeout_ms() -> int:
    """Return the configurable full-chain FBMCQ wall-clock budget."""

    return _configured_positive_int(
        "EVIDENCE_FBMCQ_WALL_CLOCK_TIMEOUT_MS",
        _DEFAULT_FBMCQ_WALL_CLOCK_TIMEOUT_MS,
    )


def fbmcq_memory_limit_bytes() -> int:
    """Return the configurable per-query isolated-worker RSS safety limit."""

    return _configured_positive_int(
        "EVIDENCE_FBMCQ_MEMORY_LIMIT_BYTES",
        _DEFAULT_FBMCQ_MEMORY_LIMIT_BYTES,
    )


def _query_hash(query: str) -> str:
    """Return a stable identity for one complete FBMCQ source query."""

    return "sha256:" + hashlib.sha256(query.encode("utf-8")).hexdigest()


def _native_model_stats(machine: Any) -> dict[str, int]:
    """Collect inexpensive native inventory counts for execution telemetry."""

    states = tuple(machine.walk_states())
    return {
        "state_count": len(states),
        "transition_count": sum(len(state.transitions) for state in states),
        "variable_count": len(machine.defines),
    }


def _emit_fbmcq_stage(
    progress_queue: Any,
    telemetry: list[dict[str, Any]],
    *,
    stage: str,
    event: str,
    started_at: float,
) -> None:
    """Persist one worker-stage boundary locally and notify the parent promptly."""

    row = {
        "stage": stage,
        "event": event,
        "elapsed_ms": round((time.monotonic() - started_at) * 1000, 3),
    }
    telemetry.append(row)
    try:
        progress_queue.put(row)
    except (OSError, ValueError):
        # The parent may already have terminated this worker after its own
        # deadline. It will synthesize the terminal failure receipt.
        return


def _set_worker_memory_limit(limit_bytes: int) -> dict[str, Any]:
    """Apply a POSIX address-space guard when the platform exposes one."""

    result: dict[str, Any] = {"requested_bytes": limit_bytes, "applied": False}
    try:
        import resource
    except ImportError:
        result["mechanism"] = "parent_rss_monitor"
        return result
    try:
        _, hard_limit = resource.getrlimit(resource.RLIMIT_AS)
        selected_limit = limit_bytes if hard_limit in {-1, resource.RLIM_INFINITY} else min(limit_bytes, hard_limit)
        resource.setrlimit(resource.RLIMIT_AS, (selected_limit, selected_limit))
    except (OSError, ValueError):
        result["mechanism"] = "parent_rss_monitor"
        return result
    result.update({"applied": True, "mechanism": "RLIMIT_AS", "effective_bytes": selected_limit})
    return result


def _fbmcq_worker(
    source_text: str,
    query: str,
    solver_timeout_ms: int,
    memory_limit_bytes: int,
    progress_queue: Any,
    result_queue: Any,
) -> None:
    """Run every native FBMCQ stage in a process the caller can terminate.

    The worker returns only JSON-compatible canonical payloads. The parent owns
    receipt creation so a deadline or memory kill still becomes a terminal,
    auditable result rather than an abandoned cell.
    """

    started_at = time.monotonic()
    telemetry: list[dict[str, Any]] = []
    active_stage = "native_load"
    memory_limit = _set_worker_memory_limit(memory_limit_bytes)
    try:
        # Publish the first stage before lazy imports so a short parent deadline
        # never has to guess whether startup, native loading, or a later stage
        # was still active when the worker was reclaimed.
        _emit_fbmcq_stage(progress_queue, telemetry, stage=active_stage, event="start", started_at=started_at)
        from pyfcstm.bmc.engine import prepare_bmc_query
        from pyfcstm.bmc.properties import compile_bmc_property
        from pyfcstm.bmc.relation import build_bmc_core_formula
        from pyfcstm.bmc.witness import (
            decode_bmc_witness,
            replay_bmc_witness,
            solve_bmc_property,
        )
        from pyfcstm.model import load_state_machine_from_text

        machine = load_state_machine_from_text(source_text)
        model_stats = _native_model_stats(machine)
        _emit_fbmcq_stage(progress_queue, telemetry, stage=active_stage, event="end", started_at=started_at)

        active_stage = "query_prepare"
        _emit_fbmcq_stage(progress_queue, telemetry, stage=active_stage, event="start", started_at=started_at)
        context = prepare_bmc_query(machine, query)
        _emit_fbmcq_stage(progress_queue, telemetry, stage=active_stage, event="end", started_at=started_at)

        active_stage = "core_build"
        _emit_fbmcq_stage(progress_queue, telemetry, stage=active_stage, event="start", started_at=started_at)
        core = build_bmc_core_formula(context)
        _emit_fbmcq_stage(progress_queue, telemetry, stage=active_stage, event="end", started_at=started_at)

        active_stage = "property_compile"
        _emit_fbmcq_stage(progress_queue, telemetry, stage=active_stage, event="start", started_at=started_at)
        formula = compile_bmc_property(core)
        _emit_fbmcq_stage(progress_queue, telemetry, stage=active_stage, event="end", started_at=started_at)

        active_stage = "solve"
        _emit_fbmcq_stage(progress_queue, telemetry, stage=active_stage, event="start", started_at=started_at)
        result = solve_bmc_property(formula, timeout_ms=solver_timeout_ms)
        _emit_fbmcq_stage(progress_queue, telemetry, stage=active_stage, event="end", started_at=started_at)

        payload: dict[str, Any] = {
            "kind": "result",
            "model_stats": model_stats,
            "query_bound": context.bound,
            "formula": formula.to_canonical(),
            "solve": result.to_canonical(),
            "result_status": result.status,
            "property_satisfied": result.property_satisfied,
            "stage_telemetry": telemetry,
            "memory_limit": memory_limit,
        }
        if result.status == "sat" and result.model is not None:
            active_stage = "decode"
            _emit_fbmcq_stage(progress_queue, telemetry, stage=active_stage, event="start", started_at=started_at)
            witness = decode_bmc_witness(formula, result.model)
            _emit_fbmcq_stage(progress_queue, telemetry, stage=active_stage, event="end", started_at=started_at)

            active_stage = "replay"
            _emit_fbmcq_stage(progress_queue, telemetry, stage=active_stage, event="start", started_at=started_at)
            replay = replay_bmc_witness(machine, witness)
            _emit_fbmcq_stage(progress_queue, telemetry, stage=active_stage, event="end", started_at=started_at)
            payload["witness"] = witness.to_canonical()
            payload["replay"] = replay.to_canonical()
            payload["trace"] = [frame.to_canonical() for frame in witness.frames]
        payload["stage_telemetry"] = telemetry
        result_queue.put(payload)
    except MemoryError:
        # Formula construction, canonicalization, and solver marshaling can
        # all raise MemoryError after the worker's resource guard fires.
        result_queue.put(
            {
                "kind": "exception",
                "failure_stage": active_stage,
                "exception_type": "MemoryError",
                "exception_message": "FBMCQ worker exceeded its available memory.",
                "stage_telemetry": telemetry,
                "memory_limit": memory_limit,
            }
        )
    except Exception as exc:  # noqa: BLE001 - native/parser/Z3 failures must terminalize in the parent audit.
        result_queue.put(
            {
                "kind": "exception",
                "failure_stage": active_stage,
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
                "stage_telemetry": telemetry,
                "memory_limit": memory_limit,
            }
        )


def _drain_fbmcq_progress(progress_queue: Any, telemetry: list[dict[str, Any]]) -> None:
    """Copy every currently available worker stage event without blocking."""

    while True:
        try:
            telemetry.append(progress_queue.get_nowait())
        except queue.Empty:
            return
        except (EOFError, OSError, ValueError):
            return


def _poll_fbmcq_result(result_queue: Any) -> dict[str, Any] | None:
    """Return a completed worker payload if one has arrived without blocking."""

    try:
        return result_queue.get_nowait()
    except queue.Empty:
        return None
    except (EOFError, OSError, ValueError):
        return None


def _linux_worker_rss_bytes(pid: int | None) -> int | None:
    """Read a child RSS sample on Linux; RLIMIT_AS remains the portable fallback."""

    if pid is None:
        return None
    try:
        status = (Path("/proc") / str(pid) / "status").read_text(encoding="utf-8")
    except OSError:
        return None
    for line in status.splitlines():
        if line.startswith("VmRSS:"):
            fields = line.split()
            if len(fields) >= 2 and fields[1].isdigit():
                return int(fields[1]) * 1024
    return None


def _terminate_worker(process: Any) -> None:
    """Terminate one isolated query worker and escalate only when necessary."""

    if not process.is_alive():
        return
    process.terminate()
    process.join(timeout=0.5)
    if process.is_alive():
        if hasattr(process, "kill"):
            process.kill()
        elif process.pid is not None:
            os.kill(process.pid, 9)
        process.join(timeout=0.5)


def _fbmcq_metadata(
    *,
    native: NativeFCSTM,
    query: str,
    solver_timeout_ms: int,
    wall_clock_timeout_ms: int,
    memory_limit_bytes: int,
    elapsed_ms: float,
    telemetry: list[dict[str, Any]],
    payload: dict[str, Any] | None,
    worker_exit_code: int | None,
    failure_stage: str | None,
) -> dict[str, Any]:
    """Build common isolated-FBMCQ metadata for completed and failed receipts."""

    result_payload = payload or {}
    execution = {
        "wall_clock_deadline_ms": wall_clock_timeout_ms,
        "memory_limit_bytes": memory_limit_bytes,
        "solver_timeout_ms": solver_timeout_ms,
        "elapsed_ms": round(elapsed_ms, 3),
        "failure_stage": failure_stage,
        "worker_exit_code": worker_exit_code,
        "stage_telemetry": result_payload.get("stage_telemetry", telemetry),
        "memory_limit": result_payload.get("memory_limit", {"requested_bytes": memory_limit_bytes}),
    }
    metadata: dict[str, Any] = {
        "fbmcq_query": query,
        "fbmcq_query_hash": _query_hash(query),
        "fbmcq_execution": execution,
        "fbmcq_model_stats": result_payload.get(
            "model_stats",
            _native_model_stats(native.machine),
        ),
    }
    for key, metadata_key in (
        ("query_bound", "fbmcq_query_bound"),
        ("formula", "fbmcq_formula"),
        ("solve", "fbmcq_solve"),
        ("witness", "fbmcq_witness"),
        ("replay", "fbmcq_replay"),
    ):
        if key in result_payload:
            metadata[metadata_key] = result_payload[key]
    return metadata


def execute_fbmcq(
    *,
    receipt_id: str,
    predicate: str,
    native: NativeFCSTM,
    query: str,
    reason: str,
    basis: str,
    timeout_ms: int = 5_000,
    wall_clock_timeout_ms: int | None = None,
    memory_limit_bytes: int | None = None,
    worker_start_method: str | None = None,
) -> RawReceipt:
    """Execute one native ``.fbmcq`` query inside an auditable killable worker.

    The caller's ``timeout_ms`` remains the native solver budget. The separate
    wall-clock deadline covers native loading, query preparation, macro-step
    core construction, property compilation, solve, decode, and replay. A
    timeout or resource failure therefore becomes a terminal failure receipt,
    never a hanging method cell or a Boolean verdict.
    """

    wall_clock = wall_clock_timeout_ms or fbmcq_wall_clock_timeout_ms()
    memory_limit = memory_limit_bytes or fbmcq_memory_limit_bytes()
    started_at = time.monotonic()
    telemetry: list[dict[str, Any]] = []
    payload: dict[str, Any] | None = None
    abort_reason: str | None = None
    failure_stage: str | None = None
    try:
        context = multiprocessing.get_context(worker_start_method or "spawn")
    except ValueError as exc:
        return native_receipt(
            receipt_id,
            predicate,
            native,
            "unknown",
            "The native .fbmcq worker could not start with the requested process policy; no Boolean predicate verdict is claimed.",
            basis + f"; invalid FBMCQ worker start method: {exc}",
            backend_family="fbmcq",
            algorithm_version=_FBMCQ_ALGORITHM_VERSION,
            terminal_state="error",
            metadata={"fbmcq_query": query, "fbmcq_query_hash": _query_hash(query)},
            failure_kind="backend_error",
        )
    progress_queue = context.Queue()
    result_queue = context.Queue(maxsize=1)
    process = context.Process(
        target=_fbmcq_worker,
        args=(native.source_text, query, timeout_ms, memory_limit, progress_queue, result_queue),
        daemon=True,
    )
    try:
        process.start()
    except (OSError, RuntimeError) as exc:
        # OSError covers OS process/resource failures; RuntimeError covers a
        # disallowed nested-daemon start. Both are backend audit facts.
        progress_queue.close()
        result_queue.close()
        progress_queue.join_thread()
        result_queue.join_thread()
        return native_receipt(
            receipt_id,
            predicate,
            native,
            "unknown",
            "The isolated native .fbmcq worker could not start; no Boolean predicate verdict is claimed.",
            basis + f"; FBMCQ worker start exception={type(exc).__name__}: {exc}",
            backend_family="fbmcq",
            algorithm_version=_FBMCQ_ALGORITHM_VERSION,
            terminal_state="error",
            metadata={
                "fbmcq_query": query,
                "fbmcq_query_hash": _query_hash(query),
                "fbmcq_execution": {
                    "wall_clock_deadline_ms": wall_clock,
                    "memory_limit_bytes": memory_limit,
                    "failure_stage": "worker_start",
                },
            },
            failure_kind="backend_error",
        )
    try:
        while process.is_alive() and payload is None:
            _drain_fbmcq_progress(progress_queue, telemetry)
            payload = _poll_fbmcq_result(result_queue)
            if payload is not None:
                break
            elapsed_ms = (time.monotonic() - started_at) * 1000
            rss_bytes = _linux_worker_rss_bytes(process.pid)
            if rss_bytes is not None and rss_bytes > memory_limit:
                abort_reason = "memory_limit"
                failure_stage = telemetry[-1]["stage"] if telemetry else "native_load"
                _terminate_worker(process)
                break
            if elapsed_ms >= wall_clock:
                abort_reason = "wall_clock_deadline"
                failure_stage = telemetry[-1]["stage"] if telemetry else "native_load"
                _terminate_worker(process)
                break
            process.join(timeout=0.02)
        _drain_fbmcq_progress(progress_queue, telemetry)
        if payload is None:
            payload = _poll_fbmcq_result(result_queue)
        if process.is_alive() and payload is not None:
            process.join(timeout=0.2)
        if process.is_alive():
            abort_reason = abort_reason or "worker_did_not_exit"
            failure_stage = failure_stage or (telemetry[-1]["stage"] if telemetry else "native_load")
            _terminate_worker(process)
    finally:
        elapsed_ms = (time.monotonic() - started_at) * 1000
        worker_exit_code = process.exitcode
        progress_queue.close()
        result_queue.close()
        progress_queue.join_thread()
        result_queue.join_thread()
    if abort_reason is not None:
        metadata = _fbmcq_metadata(
            native=native,
            query=query,
            solver_timeout_ms=timeout_ms,
            wall_clock_timeout_ms=wall_clock,
            memory_limit_bytes=memory_limit,
            elapsed_ms=elapsed_ms,
            telemetry=telemetry,
            payload=payload,
            worker_exit_code=worker_exit_code,
            failure_stage=failure_stage,
        )
        metadata["fbmcq_execution"]["abort_reason"] = abort_reason
        is_timeout = abort_reason == "wall_clock_deadline"
        return native_receipt(
            receipt_id,
            predicate,
            native,
            "unknown",
            "The isolated native .fbmcq execution exceeded its wall-clock or memory safety boundary; no Boolean predicate verdict is claimed.",
            basis + f"; isolated FBMCQ abort={abort_reason}; stage={failure_stage}",
            backend_family="fbmcq",
            algorithm_version=_FBMCQ_ALGORITHM_VERSION,
            terminal_state="timeout" if is_timeout else "error",
            metadata=metadata,
            failure_kind="timeout" if is_timeout else "backend_error",
        )
    if payload is None:
        metadata = _fbmcq_metadata(
            native=native,
            query=query,
            solver_timeout_ms=timeout_ms,
            wall_clock_timeout_ms=wall_clock,
            memory_limit_bytes=memory_limit,
            elapsed_ms=elapsed_ms,
            telemetry=telemetry,
            payload=None,
            worker_exit_code=worker_exit_code,
            failure_stage=telemetry[-1]["stage"] if telemetry else "native_load",
        )
        return native_receipt(
            receipt_id,
            predicate,
            native,
            "unknown",
            "The isolated native .fbmcq worker exited without a complete terminal payload; no Boolean predicate verdict is claimed.",
            basis + "; isolated FBMCQ worker exited without result payload",
            backend_family="fbmcq",
            algorithm_version=_FBMCQ_ALGORITHM_VERSION,
            terminal_state="error",
            metadata=metadata,
            failure_kind="backend_error",
        )
    if payload.get("kind") == "exception":
        failure_stage = str(payload.get("failure_stage", "native_load"))
        metadata = _fbmcq_metadata(
            native=native,
            query=query,
            solver_timeout_ms=timeout_ms,
            wall_clock_timeout_ms=wall_clock,
            memory_limit_bytes=memory_limit,
            elapsed_ms=elapsed_ms,
            telemetry=telemetry,
            payload=payload,
            worker_exit_code=worker_exit_code,
            failure_stage=failure_stage,
        )
        metadata["exception_type"] = payload.get("exception_type", "unknown")
        return native_receipt(
            receipt_id,
            predicate,
            native,
            "unknown",
            "The isolated native .fbmcq pipeline raised a backend exception; the failed execution is not a predicate violation.",
            basis + f"; FBMCQ exception={payload.get('exception_type')}: {payload.get('exception_message')}; stage={failure_stage}",
            backend_family="fbmcq",
            algorithm_version=_FBMCQ_ALGORITHM_VERSION,
            terminal_state="error",
            metadata=metadata,
            failure_kind="backend_error",
        )
    metadata = _fbmcq_metadata(
        native=native,
        query=query,
        solver_timeout_ms=timeout_ms,
        wall_clock_timeout_ms=wall_clock,
        memory_limit_bytes=memory_limit,
        elapsed_ms=elapsed_ms,
        telemetry=telemetry,
        payload=payload,
        worker_exit_code=worker_exit_code,
        failure_stage=None,
    )
    trace = list(payload.get("trace", []))
    replay = payload.get("replay")
    if replay is not None and not replay.get("ok", False):
        return native_receipt(
            receipt_id,
            predicate,
            native,
            "unknown",
            "The native .fbmcq solver produced a witness whose required FCSTM replay did not close; no Boolean predicate result is admitted.",
            basis + "; pyfcstm BMC witness replay mismatch",
            backend_family="fbmcq",
            algorithm_version=_FBMCQ_ALGORITHM_VERSION,
            terminal_state="error",
            metadata=metadata,
            trace=trace,
            failure_kind="backend_error",
        )
    if payload.get("property_satisfied") is True:
        verdict = "true"
    elif payload.get("property_satisfied") is False:
        verdict = "false"
    elif payload.get("result_status") == "timeout":
        return native_receipt(
            receipt_id,
            predicate,
            native,
            "unknown",
            "The native .fbmcq solve timed out before it could establish a Boolean predicate verdict.",
            basis + "; pyfcstm BMC solve timeout",
            backend_family="fbmcq",
            algorithm_version=_FBMCQ_ALGORITHM_VERSION,
            terminal_state="timeout",
            metadata=metadata,
            trace=trace,
            failure_kind="timeout",
        )
    else:
        return native_receipt(
            receipt_id,
            predicate,
            native,
            "unknown",
            "The native .fbmcq solve ended without a complete Boolean predicate verdict.",
            basis + f"; pyfcstm BMC status={payload.get('result_status')}",
            backend_family="fbmcq",
            algorithm_version=_FBMCQ_ALGORITHM_VERSION,
            terminal_state="error",
            metadata=metadata,
            trace=trace,
            failure_kind="backend_error",
        )
    return native_receipt(
        receipt_id,
        predicate,
        native,
        verdict,
        reason,
        basis + "; isolated pyfcstm .fbmcq native-load/prepare/core/property/solve/decode/replay",
        backend_family="fbmcq",
        algorithm_version=_FBMCQ_ALGORITHM_VERSION,
        metadata=metadata,
        trace=trace,
    )


__all__ = [
    "NativeFCSTM",
    "NativeFCSTMError",
    "NativeTransitionCarrier",
    "all_states",
    "all_events",
    "all_transition_carriers",
    "all_transitions",
    "execute_fbmcq",
    "fbmcq_memory_limit_bytes",
    "fbmcq_wall_clock_timeout_ms",
    "load_native_fcstm",
    "native_load_failure",
    "native_receipt",
    "native_transition_endpoints",
    "resolve_state",
    "resolve_event",
    "resolve_state_paths",
    "state_path",
    "transition_by_ref",
    "transition_owner_path",
]
