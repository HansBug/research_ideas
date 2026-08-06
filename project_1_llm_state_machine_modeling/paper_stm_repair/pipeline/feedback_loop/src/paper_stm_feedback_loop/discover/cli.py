from __future__ import annotations

import argparse
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from paper_stm_feedback_loop.assertions import AssertionChecker, build_eval_environment
from paper_stm_feedback_loop.assertions.fbmcq import probe_fbmcq_feasibility
from paper_stm_feedback_loop.common.inputs import (
    FeedbackLoopInputs,
    load_feedback_loop_inputs,
)
from paper_stm_feedback_loop.common.records import ImmutableRecordStore

from .graph import run_discover_state
from .nodes import ABLATABLE_GATES, _ABLATED_GATES
from .nodes import exclusion_roles, inserted_state_paths
from .report import telemetry_summary, write_discover_markdown
from .responder import DirectStructuredResponder
from .schemas import DiscoverInput, LLMCallRecord, NodeExecutionRecord
from .utils import sha256_data

# Resolve from the pipeline location, not the process working directory. This
# keeps ``make -C .../feedback_loop discover-pair`` and direct module execution
# on the same representation input root.
REPORT_ROOT = (
    Path(__file__).resolve().parents[4]
    / "representation"
    / "reports"
    / "llms_emp_r45_java_60"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the independent paper1 Requirement-to-Assertion Discover graph."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--pair-id",
        help="Formal pair id such as 0000 or llms_emp_feedback_final_0000.",
    )
    mode.add_argument("--case-id", help="Identity for explicit custom input files.")
    parser.add_argument("--report-root", default=str(REPORT_ROOT))
    parser.add_argument("--nl-file")
    parser.add_argument("--fcstm-file")
    parser.add_argument("--source-trace-file")
    parser.add_argument("--working-contract-file")
    parser.add_argument("--profile", required=True)
    parser.add_argument(
        "--content-language", choices=("zh-CN", "en-US"), default="zh-CN"
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--llm-config")
    parser.add_argument("--max-output-tokens", type=int)
    parser.add_argument("--assertion-timeout-seconds", type=int)
    # Bounded formal checking has no natural termination guarantee: the formula
    # build alone is exponential in the bound over a dense transition relation.
    # Leaving these unset made process.join(None) block forever, which is what
    # turned one bad assertion in pair 0029 into a 495-second precheck and an
    # operator kill.  Defaults are policy, so they are also recorded per run.
    parser.add_argument("--fbmcq-solver-timeout-ms", type=int, default=30_000)
    parser.add_argument("--fbmcq-max-bound", type=int, default=8)
    parser.add_argument("--fbmcq-process-wall-seconds", type=float, default=60.0)
    parser.add_argument("--fbmcq-canary-bound", type=int, default=3)
    parser.add_argument("--fbmcq-canary-wall-seconds", type=float, default=45.0)
    parser.add_argument("--skip-fbmcq-canary", action="store_true")
    parser.add_argument("--transport-retries", type=int, default=4)
    return parser


def _formal_pair(args: argparse.Namespace) -> FeedbackLoopInputs:
    raw = str(args.pair_id)
    match = re.search(r"(\d{4})$", raw)
    if match is None:
        raise ValueError("formal --pair-id must end with a four-digit case id")
    case = match.group(1)
    pair_id = f"llms_emp_feedback_final_{case}"
    report_root = Path(args.report_root).expanduser().resolve()
    return load_feedback_loop_inputs(
        pair_dir=report_root / "pairs" / case,
        report_root=report_root,
        pair_id=pair_id,
    )


def _custom_pair(args: argparse.Namespace) -> FeedbackLoopInputs:
    missing = [
        name
        for name, value in {
            "--nl-file": args.nl_file,
            "--fcstm-file": args.fcstm_file,
            "--source-trace-file": args.source_trace_file,
        }.items()
        if value is None
    ]
    if missing:
        raise ValueError(f"custom mode requires: {', '.join(missing)}")
    return load_feedback_loop_inputs(
        pair_id=args.case_id,
        nl_path=args.nl_file,
        fcstm_path=args.fcstm_file,
        source_trace_path=args.source_trace_file,
        working_contract_path=args.working_contract_file,
    )


def _pyfcstm_version() -> str:
    """Best-effort pyfcstm identity for the run record's evidence chain."""

    try:
        import importlib.metadata as _md

        return _md.version("pyfcstm")
    except Exception:
        try:
            import pyfcstm

            return str(getattr(pyfcstm, "__version__", "unknown"))
        except Exception:
            return "unknown"


def _discover_input(
    bundle: FeedbackLoopInputs,
    profile: str,
    content_language: str,
    run_id: str,
    tool_env_hash: str,
    fbmcq_canary: dict[str, Any] | None = None,
    resource_options: dict[str, Any] | None = None,
) -> DiscoverInput:
    manifest: dict[str, Any] = {
        "input_summary": bundle.summary(),
        "working_contract": (
            bundle.working_contract.data if bundle.working_contract is not None else {}
        ),
        "tool_env_hash": tool_env_hash,
        "fbmcq_canary": fbmcq_canary or {},
        "resource_options": resource_options or {},
    }
    return DiscoverInput(
        run_id=run_id,
        natural_language=bundle.nl_text,
        stm_text=bundle.fcstm_text,
        source_trace=bundle.source_trace.data,
        manifest=manifest,
        profile=profile,
        language=content_language,
    )


def _prepare_output(path: str) -> Path:
    root = Path(path).expanduser().resolve()
    if root.exists() and any(root.iterdir()):
        raise FileExistsError(f"output directory is not empty: {root}")
    root.mkdir(parents=True, exist_ok=True)
    return root


def _write_failure_artifacts(
    output_root: Path,
    *,
    run_id: str,
    profile: str,
    content_language: str,
    error_type: str,
    error_message: str,
) -> None:
    """Persist a deterministic failure receipt without rewriting records.

    A failed revision loop is still an auditable experiment outcome.  The
    immutable node/LLM/transport records are the detailed source; this small
    receipt makes the terminal failure discoverable without pretending that a
    partial run produced a completed Discover result.
    """

    loops = output_root / "loops"
    loops.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_name": "DiscoverRunFailure",
        "schema_version": "v2",
        "run_id": run_id,
        "status": "failed",
        "profile": profile,
        "content_language": content_language,
        "error_type": error_type,
        "error_message": error_message,
        "records_dir": "records",
    }
    with (output_root / "discover-failed.json").open("x", encoding="utf-8") as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    with (loops / "discover-failed.md").open("x", encoding="utf-8") as stream:
        stream.write("# Discover 运行失败记录\n\n")
        stream.write("本文件由确定性 CLI 生成；运行失败不等于问题不存在。\n\n")
        stream.write(f"- `run_id`: `{run_id}`\n")
        stream.write(f"- `profile`: `{profile}`\n")
        stream.write("- `status`: `failed`\n")
        stream.write(f"- `error_type`: `{error_type}`\n")
        stream.write(f"- `error_message`: {error_message}\n\n")
        stream.write(
            "所有已产生的 node、LLM、transport attempt 和 revision feedback "
            "仍保存在 [`records/`](../records/)；该失败收据不把部分结果伪装成 completed。\n"
        )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.profile == "fake":
        raise ValueError("the public CLI is real-only; fake responders are test-only")
    output_root = _prepare_output(args.output_dir)
    records = ImmutableRecordStore(output_root / "records", loop_index=0)
    bundle = _formal_pair(args) if args.pair_id else _custom_pair(args)
    run_id = (
        f"{bundle.pair_id}-{args.profile}-"
        f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    )
    source_entries = bundle.source_trace.data.get("entries", [])
    source_entries = source_entries if isinstance(source_entries, list) else []
    source_exclusions = bundle.source_trace.data.get("attribution_exclusions", [])
    source_exclusions = source_exclusions if isinstance(source_exclusions, list) else []
    environment = build_eval_environment(
        model_text=bundle.fcstm_text,
        source_mappings=source_entries,
        source_exclusions=source_exclusions,
        exclusion_roles=exclusion_roles(
            bundle.working_contract.data
            if getattr(bundle, "working_contract", None) is not None
            else None
        ),
        inserted_states=inserted_state_paths(
            bundle.working_contract.data
            if getattr(bundle, "working_contract", None) is not None
            else None
        ),
        timeout_seconds=args.assertion_timeout_seconds,
        fbmcq_solver_timeout_ms=args.fbmcq_solver_timeout_ms,
        fbmcq_max_bound=args.fbmcq_max_bound,
        fbmcq_process_wall_seconds=args.fbmcq_process_wall_seconds,
    )
    resource_options = {
        "assertion_timeout_seconds": args.assertion_timeout_seconds,
        "fbmcq_solver_timeout_ms": args.fbmcq_solver_timeout_ms,
        "fbmcq_max_bound": args.fbmcq_max_bound,
        "fbmcq_process_wall_seconds": args.fbmcq_process_wall_seconds,
        "fbmcq_canary_bound": args.fbmcq_canary_bound,
        "fbmcq_canary_wall_seconds": args.fbmcq_canary_wall_seconds,
    }
    tool_env_hash = sha256_data(
        {
            "vars_hash": environment.vars_hash,
            "function_registry_hash": environment.function_registry_hash,
            "resource_options": {
                "assertion_timeout_seconds": args.assertion_timeout_seconds,
                "fbmcq_solver_timeout_ms": args.fbmcq_solver_timeout_ms,
                "fbmcq_max_bound": args.fbmcq_max_bound,
                "fbmcq_process_wall_seconds": args.fbmcq_process_wall_seconds,
            },
        }
    )
    # Probe once, before any LLM call, whether bounded formal checking can run
    # on this model at all.  Cheap on healthy pairs (<1 s) and decisive on the
    # ones where it would otherwise hang inside a per-assertion precheck.
    fbmcq_canary: dict[str, Any] = {}
    if not args.skip_fbmcq_canary:
        fbmcq_canary = probe_fbmcq_feasibility(
            bundle.fcstm_text,
            bound=args.fbmcq_canary_bound,
            wall_seconds=args.fbmcq_canary_wall_seconds,
        )
    discover_input = _discover_input(
        bundle,
        args.profile,
        args.content_language,
        run_id,
        tool_env_hash,
        fbmcq_canary=fbmcq_canary,
        resource_options=resource_options,
    )
    records.append(
        "discover-run-started",
        {
            "schema_name": "DiscoverRunStarted",
            "schema_version": "v2",
            "run_id": run_id,
            "profile": args.profile,
            "content_language": args.content_language,
            "inputs": bundle.summary(),
            "tool_env_hash": tool_env_hash,
            # Self-contained evidence chain: never make an auditor reverse a hash
            # to learn which resource limits a run actually used.
            "resource_options": resource_options,
            "fbmcq_canary": fbmcq_canary,
            "pyfcstm_version": _pyfcstm_version(),
        },
    )
    last_stream_heartbeat: dict[str, float] = {}

    def on_stream_chunk(role: str, chunk_count: int, elapsed_ms: float) -> None:
        now = time.monotonic()
        previous = last_stream_heartbeat.get(role)
        if chunk_count != 1 and previous is not None and now - previous < 5.0:
            return
        print(
            f"[discover] {role} stream chunk={chunk_count} "
            f"elapsed={elapsed_ms / 1000:.1f}s",
            flush=True,
        )
        last_stream_heartbeat[role] = now

    responder = DirectStructuredResponder(
        args.profile,
        registry_path=args.llm_config,
        max_output_tokens=args.max_output_tokens,
        transport_retries=args.transport_retries,
        on_stream_chunk=on_stream_chunk,
    )
    seen_nodes: set[str] = set()
    seen_calls: set[str] = set()

    def on_update(node_name: str, update: dict[str, Any]) -> None:
        emitted_node_record = False
        for record in update.get("node_execution_records", []):
            if record.node_call_id not in seen_nodes:
                print(
                    f"[discover] {record.node_name} revision={record.revision} "
                    f"status={record.status} call={record.node_call_id}",
                    flush=True,
                )
                records.append(f"{record.node_name}-{record.status}", record)
                seen_nodes.add(record.node_call_id)
                emitted_node_record = True
        for call in update.get("llm_call_records", []):
            if call.llm_call_id not in seen_calls:
                records.append(f"{call.role}-llm-call-{call.status}", call)
                for attempt in call.transport_attempts:
                    records.append(
                        f"{call.role}-transport-attempt-{attempt.get('status', 'unknown')}",
                        attempt,
                    )
                seen_calls.add(call.llm_call_id)
        if not emitted_node_record:
            print(f"[discover] {node_name} state-update", flush=True)
        snapshot = {
            key: value
            for key, value in update.items()
            if key not in {"node_execution_records", "llm_call_records"}
        }
        if snapshot:
            records.append(f"{node_name}-state-update", snapshot)

    try:
        state = run_discover_state(
            discover_input,
            responder,
            assertion_checker=AssertionChecker(environment),
            on_update=on_update,
        )
    except KeyboardInterrupt:
        records.append(
            "discover-run-interrupted",
            {
                "schema_name": "DiscoverRunInterrupted",
                "schema_version": "v2",
                "run_id": run_id,
                "reason": "operator_interrupt_after_observed_no_progress",
            },
        )
        _write_failure_artifacts(
            output_root,
            run_id=run_id,
            profile=args.profile,
            content_language=args.content_language,
            error_type="KeyboardInterrupt",
            error_message="operator interrupt after observed no progress",
        )
        raise
    except Exception as exc:
        records.append(
            "discover-run-failed",
            {
                "schema_name": "DiscoverRunFailed",
                "schema_version": "v2",
                "run_id": run_id,
                "error_type": type(exc).__name__,
                "error_message": str(exc),
            },
        )
        _write_failure_artifacts(
            output_root,
            run_id=run_id,
            profile=args.profile,
            content_language=args.content_language,
            error_type=type(exc).__name__,
            error_message=str(exc),
        )
        raise

    node_records: list[NodeExecutionRecord] = state.get("node_execution_records", [])
    llm_calls: list[LLMCallRecord] = state.get("llm_call_records", [])
    summary = telemetry_summary(node_records, llm_calls)
    # Which gates were live, recorded from the process that ran rather than reconstructed from
    # a launch command afterwards. Without this an ablated cell and a fully gated cell produce
    # byte-identical artifacts, and the only evidence of the difference is a shell history --
    # which is how a two-of-seven ablation came to be read back as an unaided baseline.
    summary = {
        **summary,
        "gate_ablation": {
            "env": os.environ.get("DISCOVER_ABLATE_GATES", ""),
            "ablated": sorted(_ABLATED_GATES),
            # Deliberately not called `active`: these are the *ablatable* gates that stayed on,
            # not the gates that were live. A reader who takes `active: [8 items]` for "the eight
            # gates that ran" repeats v18's error one level up -- there, "two of seven off" was
            # read as "no gates"; here, "eight ablatable" would be read as "eight total".
            "ablatable_active": [n for n in ABLATABLE_GATES if n not in _ABLATED_GATES],
            # Rules written against a specific pair that `DISCOVER_ABLATE_GATES` cannot switch
            # off. Listed so no cell can be labelled an unaided baseline on the strength of the
            # field above.
            "non_ablatable_pair_motivated_gates": [
                "unresolved_reference_findings",
                "procedure_mismatch (Gate D)",
                "substituted_binding_findings",
                "mandatory_waiver",
                "misspelled_binding_findings",
                "placeholder_bindings",
                "adjudication-side checks (6 sites)",
                # v21/A1. Its trigger is `is_pseudo`, derived by pyfcstm from the model and
                # naming no pair -- but it was written after watching 0018/0038 publish 17
                # vacuously-false findings, and every pair it can fire on shares one NL group
                # with those two. So it is pair-motivated in origin whatever its wording, and
                # its effect is structurally unmeasurable in this corpus.
                "transient_subject (A1)",
            ],
            # The splitter/converter prompts were themselves tuned on the four historical cells
            # and have no switch at all. This is the ceiling on what any ablation can show.
            "prompt_level_tuning_not_ablatable": True,
        },
    }
    completed = state["final_output"].model_copy(
        update={
            "telemetry_summary": summary,
            "content_language": args.content_language,
        }
    )
    state["final_output"] = completed
    records.append("discover-completed", completed)
    final_json = output_root / "discover-completed.json"
    with final_json.open("x", encoding="utf-8") as stream:
        json.dump(
            completed.model_dump(mode="json"), stream, ensure_ascii=False, indent=2
        )
        stream.write("\n")
    write_discover_markdown(state, output_root / "loops" / "discover.md")
    print(f"[discover] completed: {output_root}", flush=True)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
