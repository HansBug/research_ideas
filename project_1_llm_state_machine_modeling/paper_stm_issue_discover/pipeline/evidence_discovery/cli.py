from __future__ import annotations

import argparse
import json
from pathlib import Path

from .orchestration.runner import run_experiment


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the frozen evidence_discovery method and independent judge.")
    parser.add_argument("--report-root", required=True)
    parser.add_argument("--ledger", required=True)
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
        "--allow-live",
        action="store_true",
        help="Explicit review gate for real provider/full-protocol execution; fixture mode does not need it.",
    )
    args = parser.parse_args(argv)
    summary = run_experiment(
        report_root=Path(args.report_root),
        ledger_path=Path(args.ledger),
        output_dir=Path(args.output_dir),
        profile=args.profile,
        rounds=args.rounds,
        resume=args.resume,
        allow_live=args.allow_live,
        pair_ids=args.pair_ids,
    )
    print(json.dumps({"output_dir": str(Path(args.output_dir).resolve()), "summary": summary}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
