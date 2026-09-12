"""Judge efficiency report from run receipts: requests, tokens, cost, repair turns, arbitration, wall-clock.

usage: efficiency_report.py --run-dir <dir> [--run-dir <dir> ...] [--label <text>]

Each run dir is a CLI output dir holding ``<run-id>/pairs/*.json`` (and ``failures/``).
Quality stays the primary gate; these numbers are the efficiency gate registered in
``calibration/preregistered.md`` (iteration 8 onward).
"""
from __future__ import annotations

import argparse
import glob
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


def _ts(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def summarize(run_dir: Path) -> dict:
    calls = Counter()
    tokens_in = tokens_out = 0
    turns_total = calls_total = repaired = 0
    cost = 0.0
    reports = 0
    pairs = 0
    failed = len(glob.glob(str(run_dir / "*" / "failures" / "*.json")))
    arbitrated_reports = 0
    wall: dict[str, list[datetime]] = defaultdict(list)
    for path in sorted(glob.glob(str(run_dir / "*" / "pairs" / "*.json"))):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        run_id = Path(path).parents[1].name
        pairs += 1
        reports += len(data.get("report_outcomes") or [])
        arbitrated_reports += len(data.get("validity_arbitration_certificates") or [])
        for receipt in data.get("call_receipts") or []:
            phase = "_".join(receipt.get("phase", "?").split("_")[:2])
            calls[phase] += 1
            calls_total += 1
            usage = receipt.get("usage") or []
            usage = usage if isinstance(usage, list) else [usage]
            turns = [u for u in usage if isinstance(u, dict)]
            turns_total += len(turns)
            repaired += len(turns) > 1
            tokens_in += sum(int(u.get("input_tokens") or u.get("prompt_tokens") or 0) for u in turns)
            tokens_out += sum(int(u.get("output_tokens") or u.get("completion_tokens") or 0) for u in turns)
            cost += float(receipt.get("cost_usd") or 0)
            for key in ("started_at_utc", "ended_at_utc"):
                stamp = _ts(receipt.get(key))
                if stamp:
                    wall[run_id].append(stamp)
    per_round = {rid: (max(ts) - min(ts)).total_seconds() / 60 for rid, ts in wall.items() if ts}
    all_ts = [t for ts in wall.values() for t in ts]
    return {
        "run_dir": str(run_dir),
        "pairs": pairs,
        "reports": reports,
        "failed_pairs": failed,
        "calls": calls_total,
        "calls_by_phase": dict(calls),
        "calls_per_report": calls_total / reports if reports else 0,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "tokens_in_per_report": tokens_in / reports if reports else 0,
        "tokens_out_per_report": tokens_out / reports if reports else 0,
        "cost_usd": cost,
        "cost_per_report": cost / reports if reports else 0,
        "repair_turn_rate": repaired / calls_total if calls_total else 0,
        "turns_per_call": turns_total / calls_total if calls_total else 0,
        "arbitrated_report_rate": arbitrated_reports / reports if reports else 0,
        "wall_minutes_per_round": per_round,
        "wall_minutes_total": (max(all_ts) - min(all_ts)).total_seconds() / 60 if all_ts else 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, action="append", required=True)
    parser.add_argument("--label", default="")
    args = parser.parse_args()
    rows = [summarize(d) for d in args.run_dir]
    print(f"# Judge efficiency report {args.label}".rstrip())
    print()
    print("| run dir | pairs | reports | failed | calls | calls/report | in tok/report | out tok/report | USD | USD/report | repair-turn rate | arbitrated reports | wall min (total; per round) |")
    print("| :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | :-- |")
    for r in rows:
        per_round = ", ".join(f"{k}:{v:.0f}" for k, v in sorted(r["wall_minutes_per_round"].items()))
        print(
            f"| `{Path(r['run_dir']).name}` | {r['pairs']} | {r['reports']} | {r['failed_pairs']} | {r['calls']} | {r['calls_per_report']:.2f} | {r['tokens_in_per_report']:,.0f} | {r['tokens_out_per_report']:,.0f} | {r['cost_usd']:.2f} | {r['cost_per_report']:.4f} | {r['repair_turn_rate']:.0%} | {r['arbitrated_report_rate']:.0%} | {r['wall_minutes_total']:.0f}; {per_round} |"
        )
    print()
    for r in rows:
        print(f"- `{Path(r['run_dir']).name}` calls by phase: " + ", ".join(f"{k}={v}" for k, v in sorted(r["calls_by_phase"].items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
