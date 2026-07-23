from __future__ import annotations

import json
import hashlib
import multiprocessing as mp
import pickle
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Callable

from pyfcstm.bmc.parse import parse_bmc_query
from pyfcstm.entry.bmc import build_bmc_output

from .exceptions import UnsupportedEvidence
from .views import FrozenView


FBMCQ_FIELDS = frozenset(
    {
        "canonical_query",
        "status",
        "holds",
        "bound",
        "formal_property_kind",
        "formal_bound",
        "controller_max_bound",
        "query_origin",
        "assumption_basis",
        "process_isolation",
        "witness",
        "replay_status",
        "limitations",
        "raw",
    }
)

FBMCQ_LIMITATIONS = (
    "finite_horizon_only",
    "exact_query_and_assumptions_only",
    "does_not_establish_unbounded_correctness",
)


class FBMCQTimeoutError(TimeoutError):
    """FBMCQ wall-clock timeout with structured inconclusive metadata."""

    def __init__(self, message: str, *, metadata: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.metadata = metadata or {}


class FBMCQUnsupportedEvidence(UnsupportedEvidence):
    """FBMCQ inconclusive evidence with structured metadata."""

    def __init__(self, message: str, *, metadata: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.metadata = metadata or {}


def _unsupported(message: str, **metadata: Any) -> FBMCQUnsupportedEvidence:
    return FBMCQUnsupportedEvidence(message, metadata=metadata)


def _run_bmc_child(
    result_path: str,
    runner: Callable[..., tuple[str, int]],
    model_path: str,
    query_path: str,
    kwargs: dict[str, Any],
) -> None:
    try:
        report_text, exit_code = runner(model_path, query_path, **kwargs)
        message = {"ok": True, "report_text": report_text, "exit_code": exit_code}
    except BaseException as exc:  # pragma: no cover - exercised through parent metadata
        message = {
            "ok": False,
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "metadata": getattr(exc, "metadata", None),
        }
    Path(result_path).write_text(
        json.dumps(message, ensure_ascii=False, allow_nan=False),
        encoding="utf-8",
    )


def _is_spawn_pickleable(value: Any) -> bool:
    try:
        pickle.dumps(value)
    except Exception:
        return False
    return True


class FBMCQAPI:
    """Structured pyfcstm FBMCQ facade for direct-eval assertions.

    Parameters: ``model_text`` is the Controller-frozen FCSTM artifact.
    ``timeout_ms`` and ``max_bound`` are Controller policy limits. ``bmc_runner``
    is an optional test seam with the same call contract as
    ``pyfcstm.entry.bmc.build_bmc_output``. The Agent supplies only a complete
    FBMCQ query string, never model/query paths.

    Returns: ``fbmcq(query)`` returns an immutable observation with exactly
    ``canonical_query``, solver ``status``, strict bool ``holds``, parsed
    ``bound``, structured ``witness``, ``replay_status``, stable ``limitations``,
    and raw structured report. Stable results can be asserted as
    ``fbmcq('...').holds is True``.

    Execution: parse the complete query with pyfcstm, write Controller-owned
    temporary model/query files, call ``build_bmc_output(..., json_output=True)``,
    parse the normative JSON report, and require a solved boolean property plus
    successful witness/counterexample replay when replay is present. No legacy
    check batch, exception-string parser, second LLM, or synthesized property is
    involved.

    Failure semantics: malformed query/model, nonzero CLI exit, timeout,
    unknown/incomplete solver result, missing bool property result, malformed
    JSON, or replay mismatch raises ``UnsupportedEvidence`` (or ``TimeoutError``
    for timeout). Direct eval therefore produces an inconclusive result, never a
    false contradiction.

    Evidence limitations: FBMCQ is bounded by the query and Controller policy.
    A stable result supports only that exact query/profile; it does not establish
    unbounded correctness, NL fidelity, source attribution, or semantic coverage.

    Permissions: read-only Controller-bound model and temporary files created
    inside a private temporary directory. No Agent-supplied paths, filesystem
    traversal, shell, imports, environment, network, mutation, or reference/gold
    data are exposed.

    Example: ``fbmcq('check reach <= 8: active("Root.Attack");').holds is True``
    checks the exact bounded reachability query after the FBMCQ guide was read.
    """

    family = "formal"

    def __init__(
        self,
        model_text: str | None,
        *,
        timeout_ms: int | None = None,
        max_bound: int | None = None,
        process_wall_seconds: float | None = None,
        bmc_runner: Callable[..., tuple[str, int]] | None = None,
    ) -> None:
        self.model_text = model_text
        self.timeout_ms = timeout_ms
        self.max_bound = max_bound
        self.process_wall_seconds = process_wall_seconds
        self.bmc_runner = bmc_runner or build_bmc_output

    def fbmcq(self, query: str) -> FrozenView:
        if not isinstance(self.model_text, str) or not self.model_text.strip():
            raise _unsupported("fbmcq requires frozen model_text", inconclusive_kind="missing_model")
        if not isinstance(query, str) or not query.strip():
            raise _unsupported(
                "fbmcq query must be a non-empty complete query",
                inconclusive_kind="malformed_query",
            )
        try:
            parsed = parse_bmc_query(query)
            canonical_query = str(parsed)
        except Exception as exc:
            raise _unsupported(
                "fbmcq query parse failed",
                inconclusive_kind="malformed_query",
                origin="exact_agent_query",
                query=query,
                parser_exception_type=type(exc).__name__,
                parser_exception_message=str(exc),
            ) from exc

        parsed_property = getattr(parsed, "property", None)
        formal_property_kind = getattr(parsed_property, "kind", None)
        formal_bound = getattr(parsed_property, "bound", None)
        if not isinstance(formal_property_kind, str) or not isinstance(formal_bound, int):
            raise _unsupported(
                "fbmcq parsed query lacks typed property kind/bound",
                inconclusive_kind="malformed_query",
                origin="exact_agent_query",
                canonical_query=canonical_query,
            )
        assumption_basis = tuple(str(item) for item in getattr(parsed, "assumptions", ()) or ())
        base_metadata = {
            "query_origin": "exact_agent_query",
            "canonical_query": canonical_query,
            "formal_property_kind": formal_property_kind,
            "formal_bound": formal_bound,
            "controller_max_bound": self.max_bound,
            "assumption_basis": list(assumption_basis),
            "query_sha256": hashlib.sha256(
                canonical_query.encode("utf-8")
            ).hexdigest(),
            "model_sha256": hashlib.sha256(
                self.model_text.encode("utf-8")
            ).hexdigest(),
        }
        if self.max_bound is not None and formal_bound > self.max_bound:
            raise _unsupported(
                "fbmcq query exceeds Controller analysis bound",
                inconclusive_kind="analysis_bound_exceeded",
                **base_metadata,
            )

        with TemporaryDirectory(prefix="paper1-fbmcq-") as directory:
            root = Path(directory)
            model_path = root / "STM_0.fcstm"
            query_path = root / "assertion.fbmcq"
            model_path.write_text(self.model_text, encoding="utf-8")
            query_path.write_text(canonical_query + "\n", encoding="utf-8")
            runner_kwargs: dict[str, Any] = {"json_output": True}
            if self.timeout_ms is not None:
                runner_kwargs["timeout_ms"] = self.timeout_ms
            if self.max_bound is not None:
                runner_kwargs["max_bound"] = self.max_bound
            try:
                report_text, exit_code, process_metadata = self._run_bmc(
                    str(model_path), str(query_path), runner_kwargs, base_metadata
                )
            except FBMCQTimeoutError:
                raise
            except FBMCQUnsupportedEvidence:
                raise
            except TimeoutError as exc:
                raise FBMCQTimeoutError(
                    "fbmcq solver timed out",
                    metadata={"inconclusive_kind": "timeout", **base_metadata},
                ) from exc
            except TypeError:
                # Backward-compatible seam for older local tests that expose only
                # positional paths and cannot accept structured policy kwargs.
                try:
                    report_text, exit_code = self.bmc_runner(str(model_path), str(query_path))
                    process_metadata = {"process_isolation": "direct_unpickleable_test_seam"}
                except Exception as exc:
                    raise _unsupported(
                        "fbmcq execution failed",
                        inconclusive_kind="execution_error",
                        exception_type=type(exc).__name__,
                        exception_message=str(exc),
                        **base_metadata,
                    ) from exc
            except Exception as exc:
                raise _unsupported(
                    "fbmcq execution failed",
                    inconclusive_kind="execution_error",
                    exception_type=type(exc).__name__,
                    exception_message=str(exc),
                    **base_metadata,
                ) from exc

        try:
            report = json.loads(report_text)
        except (TypeError, json.JSONDecodeError) as exc:
            raise _unsupported(
                "fbmcq did not return structured JSON",
                inconclusive_kind="malformed_report",
                exception_type=type(exc).__name__,
                exception_message=str(exc),
                **base_metadata,
            ) from exc
        if exit_code not in {0, 1} or not isinstance(report, dict):
            raise _unsupported(
                f"fbmcq exited without stable result: {exit_code}",
                inconclusive_kind="unstable_exit",
                exit_code=exit_code,
                **base_metadata,
            )

        result = report.get("result")
        prop = report.get("property")
        replay = report.get("replay")
        if not isinstance(result, dict) or not isinstance(prop, dict):
            raise _unsupported(
                "fbmcq report lacks result/property objects",
                inconclusive_kind="malformed_report",
                **base_metadata,
            )
        reported_kind = prop.get("kind")
        reported_bound = prop.get("bound")
        reported_query = report.get("canonical_query") or report.get("query")
        if (
            reported_kind != formal_property_kind
            or reported_bound != formal_bound
            or (isinstance(reported_query, str) and reported_query.strip() != canonical_query.strip())
        ):
            raise _unsupported(
                "fbmcq structured report does not match parsed exact query",
                inconclusive_kind="structured_report_mismatch",
                reported_property_kind=reported_kind,
                reported_bound=reported_bound,
                reported_query=reported_query,
                **base_metadata,
            )
        incomplete_status = result.get("incomplete_status")
        if incomplete_status == "timeout" or result.get("status") == "timeout":
            raise FBMCQTimeoutError(
                "fbmcq solver timed out",
                metadata={"inconclusive_kind": "timeout", **base_metadata},
            )
        if result.get("incomplete") is True or result.get("status") in {
            "unknown",
            "incomplete",
        }:
            raise _unsupported(
                f"fbmcq result is incomplete: {incomplete_status or result.get('status')}",
                inconclusive_kind="budget_or_incomplete",
                solver_status=result.get("status"),
                incomplete_status=incomplete_status,
                **base_metadata,
            )
        holds = result.get("property_satisfied")
        if not isinstance(holds, bool):
            raise _unsupported(
                "fbmcq result lacks strict bool property_satisfied",
                inconclusive_kind="malformed_report",
                **base_metadata,
            )
        replay_status = "not_applicable"
        if isinstance(replay, dict):
            replay_status = "ok" if replay.get("ok") is True else "mismatch"
            if replay.get("ok") is not True:
                raise _unsupported(
                    "fbmcq witness/counterexample replay mismatch",
                    inconclusive_kind="replay_mismatch",
                    replay_status=replay_status,
                    replay=replay,
                    **base_metadata,
                )

        data: dict[str, Any] = {
            "canonical_query": canonical_query,
            "status": result.get("status"),
            "holds": holds,
            "bound": formal_bound,
            "formal_property_kind": formal_property_kind,
            "formal_bound": formal_bound,
            "controller_max_bound": self.max_bound,
            "query_origin": "exact_agent_query",
            "assumption_basis": assumption_basis,
            "process_isolation": process_metadata.get("process_isolation"),
            "witness": report.get("witness"),
            "replay_status": replay_status,
            "limitations": FBMCQ_LIMITATIONS,
            "raw": report,
        }
        return FrozenView("fbmcq", data, allowed_fields=FBMCQ_FIELDS)

    def _run_bmc(
        self,
        model_path: str,
        query_path: str,
        runner_kwargs: dict[str, Any],
        base_metadata: dict[str, Any],
    ) -> tuple[str, int, dict[str, Any]]:
        if self.bmc_runner is not build_bmc_output and not _is_spawn_pickleable(self.bmc_runner):
            report_text, exit_code = self.bmc_runner(model_path, query_path, **runner_kwargs)
            return report_text, exit_code, {"process_isolation": "direct_unpickleable_test_seam"}

        ctx = mp.get_context("spawn")
        result_path = str(Path(query_path).with_name("fbmcq-child-result.json"))
        process = ctx.Process(
            target=_run_bmc_child,
            args=(
                result_path,
                self.bmc_runner,
                model_path,
                query_path,
                runner_kwargs,
            ),
        )
        process.start()
        child_pid = process.pid
        timeout_s = self.process_wall_seconds
        process.join(timeout_s)
        if process.is_alive():
            process.terminate()
            process.join(1.0)
            if process.is_alive():
                process.kill()
                process.join(1.0)
            raise FBMCQTimeoutError(
                "fbmcq solver timed out",
                metadata={
                    "inconclusive_kind": "timeout",
                    "process_wall_seconds": self.process_wall_seconds,
                    "timed_out_stage": "build_or_solve_or_replay",
                    "child_pid": child_pid,
                    "process_joined": not process.is_alive(),
                    "process_alive_after_join": process.is_alive(),
                    "process_exitcode": process.exitcode,
                    **base_metadata,
                },
            )
        try:
            message = json.loads(Path(result_path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise _unsupported(
                "fbmcq child exited without structured result",
                inconclusive_kind="child_no_result",
                child_pid=child_pid,
                process_exitcode=process.exitcode,
                **base_metadata,
            ) from exc
        if not message.get("ok"):
            raise _unsupported(
                "fbmcq child execution failed",
                inconclusive_kind="execution_error",
                exception_type=message.get("exception_type"),
                exception_message=message.get("exception_message"),
                child_metadata=message.get("metadata"),
                child_pid=child_pid,
                process_exitcode=process.exitcode,
                **base_metadata,
            )
        return (
            message.get("report_text"),
            message.get("exit_code"),
            {
                "process_isolation": "multiprocessing_spawn",
                "child_pid": child_pid,
                "process_exitcode": process.exitcode,
            },
        )


__all__ = [
    "FBMCQAPI",
    "FBMCQ_FIELDS",
    "FBMCQ_LIMITATIONS",
    "FBMCQTimeoutError",
    "FBMCQUnsupportedEvidence",
]
