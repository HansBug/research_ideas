"""Run a single ablation configuration on the slice and save results.

Usage:
    python -m state_machine_review_corpus.etl.run_ablation_config \
        --config A_only \
        --record-limit 12 --summary-limit 12 --component-limit 12 --protocol-limit 4 \
        --output etl/out/phase14_combined/report_iter_A_only.json

Configs supported:
    iter_a_only / iter_b_only / iter_c_only / iter_abc / iter_a_b / iter_a_c
    (via --iter-a / --iter-b / --iter-c boolean flags)
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from project_ex1_llm_judge_for_stm.src.expert_review.benchmark import (
    _evaluate_task_bundle,
    _load_benchmark_tables,
    build_benchmark_slices,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", type=Path, required=True)
    parser.add_argument("--record-limit", type=int, default=12)
    parser.add_argument("--summary-limit", type=int, default=12)
    parser.add_argument("--component-limit", type=int, default=12)
    parser.add_argument("--protocol-limit", type=int, default=4)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--rerun-count", type=int, default=0)
    parser.add_argument("--rubric", action="store_true", default=False,
                        help="Master on/off for rubric_llm_enabled")
    parser.add_argument("--iter-a", action="store_true", default=False,
                        help="Iter-A: asymmetric sanity bounds (looser for summary/protocol)")
    parser.add_argument("--iter-b", action="store_true", default=False,
                        help="Iter-B: append differentiation hint to rubric prompt")
    parser.add_argument("--iter-c", nargs="*", default=None,
                        help="Iter-C: list of regimes where rubric applies (default all)")
    parser.add_argument("--config-label", type=str, default="ablation")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--llm-mode", type=str, default="auto", choices=["auto", "off"])
    parser.add_argument("--model", type=str, default="gpt-5.5")
    parser.add_argument("--provider-order", nargs="*", default=["airouter"])
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--max-workers", type=int, default=1,
                        help="Task-level parallelism (default 1 = sequential, backward compat)")
    args = parser.parse_args()

    records, protocols, availability = _load_benchmark_tables(args.base_dir)
    slice_tasks = build_benchmark_slices(
        records, protocols,
        record_limit=args.record_limit,
        summary_limit=args.summary_limit,
        component_limit=args.component_limit,
        protocol_limit=args.protocol_limit,
        seed=args.seed,
    )

    total = 0
    for regime, tasks in slice_tasks.items():
        for t in tasks:
            if t.metadata is None:
                t.metadata = {}
            t.metadata["rubric_llm_enabled"] = args.rubric
            t.metadata["rubric_iter_a_asymmetric"] = args.iter_a
            t.metadata["rubric_iter_b_diff_prompt"] = args.iter_b
            if args.iter_c is not None:
                t.metadata["rubric_iter_c_regimes"] = list(args.iter_c)
            total += 1
    print(f"[{args.config_label}] tasks={total} flags rubric={args.rubric} A={args.iter_a} B={args.iter_b} C={args.iter_c}", flush=True)

    t0 = time.time()
    report = _evaluate_task_bundle(
        slice_tasks,
        llm_mode=args.llm_mode,
        rerun_count=args.rerun_count,
        report_label=f"week1_iter:{args.config_label}",
        metadata={
            "scope": "ablation",
            "config_label": args.config_label,
            "rubric": args.rubric,
            "iter_a": args.iter_a,
            "iter_b": args.iter_b,
            "iter_c": args.iter_c,
        },
        review_cache=None,
        model=args.model,
        provider_order=args.provider_order if args.llm_mode == "auto" else None,
        temperature=args.temperature,
        timeout=args.timeout,
        max_workers=args.max_workers,
    )
    elapsed = time.time() - t0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    print(f"[{args.config_label}] elapsed_min={elapsed/60:.1f}", flush=True)
    print(f"[{args.config_label}] HAI={report.get('HAI', 0):.4f} HAI_legacy={report.get('HAI_legacy', 0):.4f}", flush=True)
    print(f"[{args.config_label}] RAS={report['record_metrics'].get('RAS', 0):.4f} SAS={report['summary_metrics'].get('SAS', 0):.4f}", flush=True)


if __name__ == "__main__":
    main()
