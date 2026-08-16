"""Whether the provider served the model that was asked for, per cell and per call.

The run record keeps `configured_model` and `observed_model` as separate fields, which is the
only way to notice that a proxy quietly served something else. That matters more in this
generation than in any before it: the `gpt-5.5` arm goes through a third-party gateway, and if
that gateway routes to a different model, the two arms are no longer comparing what the report
says they compare -- while every cell still completes and every number still looks reasonable.

Also reports which calls have no usage at all. A cell whose usage is missing cannot support a
cost claim, and silently averaging over it understates the cost of the arm.

Usage:
    check_model_drift.py runs/paper1/matrix-v22
    check_model_drift.py runs/paper1/matrix-v22 --strict   # exit 1 on any drift
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

#: Fields a call record uses to say what was asked for and what answered.
ASKED = ("configured_model", "model_id")
SERVED = ("observed_model", "raw_response.response_metadata.model_name")


def _dig(payload: dict, dotted: str):
    node = payload
    for part in dotted.split("."):
        if not isinstance(node, dict):
            return None
        node = node.get(part)
    return node


def _calls(cell: Path):
    for record in sorted((cell / "records").glob("*llm-call-completed/record.json")):
        try:
            yield record, json.loads(record.read_text())
        except (OSError, json.JSONDecodeError):
            continue


def audit(base: Path) -> tuple[dict, list[str]]:
    """Per-arm model census and the list of drifted or usage-less calls."""

    census: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    problems: list[str] = []
    for run in sorted(base.glob("run*")):
        for cell in sorted(p for p in run.iterdir() if p.is_dir() and (p / "records").is_dir()):
            # `0047-gpt.try1` 是失败重试留下的目录。上一版把它当成一条名为 `gpt.try2` 的臂，
            # 于是漂移审计里凭空多出一条臂，而它的调用其实属于同一条 gpt 臂的作废尝试。
            # 作废的尝试**仍然要审**（若网关在那次代换了模型，那是真事实），但要归到它自己
            # 的臂上，并单独标出来 —— 它不进主结果统计。
            arm = cell.name.rsplit("-", 1)[-1]
            attempt = ""
            if "." in arm:
                arm, _, attempt = arm.partition(".")
                arm = f"{arm} (作废尝试 {attempt})"
            for record, payload in _calls(cell):
                asked = next((payload.get(k) for k in ASKED if payload.get(k)), None)
                served = next((_dig(payload, k) for k in SERVED if _dig(payload, k)), None)
                census[arm][f"{asked} -> {served}"] += 1
                if asked and served and asked != served:
                    problems.append(
                        f"drift {run.name}/{cell.name}/{record.parent.name}: "
                        f"asked {asked!r}, served {served!r}"
                    )
                if payload.get("usage_status") not in {"complete", None} or (
                    payload.get("total_tokens") in (None, 0)
                ):
                    problems.append(
                        f"no usage {run.name}/{cell.name}/{record.parent.name}: "
                        f"status={payload.get('usage_status')!r} total={payload.get('total_tokens')!r}"
                    )
    return census, problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", type=Path)
    parser.add_argument("--strict", action="store_true", help="exit 1 when anything is reported")
    args = parser.parse_args(argv)
    if not args.base.is_dir():
        print(f"no such directory: {args.base}", file=sys.stderr)
        return 2
    census, problems = audit(args.base)
    if not census:
        # Refusing to print a clean bill of health for a directory with no calls in it: an empty
        # audit reading as "no drift" is how a missing run becomes a passing check.
        print(f"no llm-call records under {args.base}", file=sys.stderr)
        return 2
    for arm, counts in sorted(census.items()):
        print(f"{arm}:")
        for pair, count in counts.most_common():
            print(f"  {count:5d}  {pair}")
    if problems:
        print(f"\n{len(problems)} problem(s):", file=sys.stderr)
        for problem in problems[:40]:
            print(f"  {problem}", file=sys.stderr)
        if len(problems) > 40:
            print(f"  ... and {len(problems) - 40} more", file=sys.stderr)
    return 1 if (problems and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
