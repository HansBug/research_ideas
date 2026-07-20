from __future__ import annotations

import json
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
        "witness",
        "replay_status",
        "raw",
    }
)


class FBMCQAPI:
    """Structured pyfcstm FBMCQ facade for direct-eval assertions.

    Parameters: ``model_text`` is the Controller-frozen FCSTM artifact.
    ``timeout_ms`` and ``max_bound`` are Controller policy limits. ``bmc_runner``
    is an optional test seam with the same call contract as
    ``pyfcstm.entry.bmc.build_bmc_output``. The Agent supplies only a complete
    FBMCQ query string, never model/query paths.

    Returns: ``fbmcq(query)`` returns an immutable observation with exactly
    ``canonical_query``, solver ``status``, strict bool ``holds``, parsed
    ``bound``, structured ``witness``, ``replay_status``, and raw structured
    report. Stable results can be asserted as ``fbmcq('...').holds is True``.

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
        bmc_runner: Callable[..., tuple[str, int]] | None = None,
    ) -> None:
        self.model_text = model_text
        self.timeout_ms = timeout_ms
        self.max_bound = max_bound
        self.bmc_runner = bmc_runner or build_bmc_output

    def fbmcq(self, query: str) -> FrozenView:
        if not isinstance(self.model_text, str) or not self.model_text.strip():
            raise UnsupportedEvidence("fbmcq requires frozen model_text")
        if not isinstance(query, str) or not query.strip():
            raise UnsupportedEvidence("fbmcq query must be a non-empty complete query")
        try:
            parsed = parse_bmc_query(query)
            canonical_query = str(parsed)
        except Exception as exc:
            raise UnsupportedEvidence("fbmcq query parse failed") from exc

        with TemporaryDirectory(prefix="paper1-fbmcq-") as directory:
            root = Path(directory)
            model_path = root / "STM_0.fcstm"
            query_path = root / "assertion.fbmcq"
            model_path.write_text(self.model_text, encoding="utf-8")
            query_path.write_text(canonical_query + "\n", encoding="utf-8")
            try:
                report_text, exit_code = self.bmc_runner(
                    str(model_path),
                    str(query_path),
                    json_output=True,
                    timeout_ms=self.timeout_ms,
                    max_bound=self.max_bound,
                )
            except TypeError:
                # Test seams may intentionally expose only positional paths.
                report_text, exit_code = self.bmc_runner(
                    str(model_path), str(query_path)
                )
            except TimeoutError:
                raise
            except Exception as exc:
                raise UnsupportedEvidence("fbmcq execution failed") from exc

        try:
            report = json.loads(report_text)
        except (TypeError, json.JSONDecodeError) as exc:
            raise UnsupportedEvidence("fbmcq did not return structured JSON") from exc
        if exit_code not in {0, 1} or not isinstance(report, dict):
            raise UnsupportedEvidence(f"fbmcq exited without stable result: {exit_code}")

        result = report.get("result")
        prop = report.get("property")
        replay = report.get("replay")
        if not isinstance(result, dict) or not isinstance(prop, dict):
            raise UnsupportedEvidence("fbmcq report lacks result/property objects")
        incomplete_status = result.get("incomplete_status")
        if incomplete_status == "timeout" or result.get("status") == "timeout":
            raise TimeoutError("fbmcq solver timed out")
        if result.get("incomplete") is True or result.get("status") in {
            "unknown",
            "incomplete",
        }:
            raise UnsupportedEvidence(
                f"fbmcq result is incomplete: {incomplete_status or result.get('status')}"
            )
        holds = result.get("property_satisfied")
        if not isinstance(holds, bool):
            raise UnsupportedEvidence("fbmcq result lacks strict bool property_satisfied")
        if isinstance(replay, dict) and replay.get("ok") is not True:
            raise UnsupportedEvidence("fbmcq witness/counterexample replay mismatch")

        data: dict[str, Any] = {
            "canonical_query": canonical_query,
            "status": result.get("status"),
            "holds": holds,
            "bound": prop.get("bound"),
            "witness": report.get("witness"),
            "replay_status": "ok" if isinstance(replay, dict) else "not_applicable",
            "raw": report,
        }
        return FrozenView("fbmcq", data, allowed_fields=FBMCQ_FIELDS)


__all__ = ["FBMCQAPI", "FBMCQ_FIELDS"]
