from __future__ import annotations

import argparse
import json
from pathlib import Path

from .orchestration.runner import run_experiment


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the frozen evidence_discovery method.")
    parser.add_argument("--report-root", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--profile", default="gpt-5.6-luna")
    parser.add_argument("--rounds", type=int, default=3)
    parser.add_argument(
        "--pair-id",
        dest="pair_ids",
        action="append",
        help="Explicit frozen pair ID to run; repeat for a diagnostic subset (required for live runs).",
    )
    parser.add_argument("--resume", action="store_true", help="Resume valid cells already present in output-dir.")
    parser.add_argument(
        "--run-id",
        help="Exact 32-hex run identity to create or resume; artifacts live under output-dir/run-id.",
    )
    parser.add_argument(
        "--allow-live",
        action="store_true",
        help="Explicit provider-free review gate for any live provider execution; fixture mode does not need it.",
    )
    parser.add_argument(
        "--allow-full-live",
        action="store_true",
        help="Second explicit gate for the frozen 54-pair three-round run after representative-pair review.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Independent pair processes; each pair owns its method terminalization.",
    )
    parser.add_argument(
        "--transport-retries",
        type=int,
        default=8,
        help="In-place provider transport retries before the one local dead-call retry.",
    )
    parser.add_argument(
        "--no-stream",
        action="store_true",
        help="Use non-streaming calls with only the 300-second total timeout.",
    )
    parser.add_argument(
        "--predecessor-snapshot",
        help="Preserved diagnostic run root recorded for provenance only; no cells are imported.",
    )
    args = parser.parse_args(argv)
    summary = run_experiment(
        report_root=Path(args.report_root),
        output_dir=Path(args.output_dir),
        profile=args.profile,
        rounds=args.rounds,
        resume=args.resume,
        allow_live=args.allow_live,
        allow_full_live=args.allow_full_live,
        pair_ids=args.pair_ids,
        workers=args.workers,
        transport_retries=args.transport_retries,
        streaming=not args.no_stream,
        run_id=args.run_id,
        predecessor_snapshot=args.predecessor_snapshot,
    )
    print(json.dumps({"output_dir": summary["artifact_root"], "run_id": summary["run_id"], "summary": summary}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
