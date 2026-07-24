from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from paper_stm_feedback_loop.assertions import AssertionChecker, build_eval_environment
from paper_stm_feedback_loop.common.inputs import FeedbackLoopInputs, load_feedback_loop_inputs
from paper_stm_feedback_loop.common.records import ImmutableRecordStore

from .graph import run_discover_state
from .report import telemetry_summary, write_discover_markdown
from .responder import DirectStructuredResponder
from .schemas import DiscoverInput, LLMCallRecord, NodeExecutionRecord
from .utils import sha256_data

REPORT_ROOT = Path(
    "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/"
    "representation/reports/llms_emp_r45_java_60"
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
    parser.add_argument("--fbmcq-solver-timeout-ms", type=int)
    parser.add_argument("--fbmcq-max-bound", type=int)
    parser.add_argument("--fbmcq-process-wall-seconds", type=float)
    parser.add_argument("--transport-retries", type=int, default=2)
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


def _discover_input(
    bundle: FeedbackLoopInputs,
    profile: str,
    content_language: str,
    run_id: str,
    tool_env_hash: str,
) -> DiscoverInput:
    manifest: dict[str, Any] = {
        "input_summary": bundle.summary(),
        "working_contract": (
            bundle.working_contract.data if bundle.working_contract is not None else {}
        ),
        "tool_env_hash": tool_env_hash,
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
    environment = build_eval_environment(
        model_text=bundle.fcstm_text,
        source_mappings=source_entries,
        timeout_seconds=args.assertion_timeout_seconds,
        fbmcq_solver_timeout_ms=args.fbmcq_solver_timeout_ms,
        fbmcq_max_bound=args.fbmcq_max_bound,
        fbmcq_process_wall_seconds=args.fbmcq_process_wall_seconds,
    )
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
    discover_input = _discover_input(
        bundle, args.profile, args.content_language, run_id, tool_env_hash
    )
    records.append(
        "discover-run-started",
        {
            "schema_name": "DiscoverRunStarted",
            "schema_version": "v1",
            "run_id": run_id,
            "profile": args.profile,
            "content_language": args.content_language,
            "inputs": bundle.summary(),
            "tool_env_hash": tool_env_hash,
        },
    )
    responder = DirectStructuredResponder(
        args.profile,
        registry_path=args.llm_config,
        max_output_tokens=args.max_output_tokens,
        transport_retries=args.transport_retries,
    )
    seen_nodes: set[str] = set()
    seen_calls: set[str] = set()

    def on_update(node_name: str, update: dict[str, Any]) -> None:
        print(f"[discover] {node_name}", flush=True)
        for record in update.get("node_execution_records", []):
            if record.node_call_id not in seen_nodes:
                records.append(f"{record.node_name}-{record.status}", record)
                seen_nodes.add(record.node_call_id)
        for call in update.get("llm_call_records", []):
            if call.llm_call_id not in seen_calls:
                records.append(f"{call.role}-llm-call-{call.status}", call)
                for attempt in call.transport_attempts:
                    records.append(
                        f"{call.role}-transport-attempt-{attempt.get('status', 'unknown')}",
                        attempt,
                    )
                seen_calls.add(call.llm_call_id)
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
    except Exception as exc:
        records.append(
            "discover-run-failed",
            {
                "schema_name": "DiscoverRunFailed",
                "schema_version": "v1",
                "run_id": run_id,
                "error_type": type(exc).__name__,
                "error_message": str(exc),
            },
        )
        raise

    node_records: list[NodeExecutionRecord] = state.get("node_execution_records", [])
    llm_calls: list[LLMCallRecord] = state.get("llm_call_records", [])
    summary = telemetry_summary(node_records, llm_calls)
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
        json.dump(completed.model_dump(mode="json"), stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    write_discover_markdown(state, output_root / "loops" / "discover.md")
    print(f"[discover] completed: {output_root}", flush=True)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
