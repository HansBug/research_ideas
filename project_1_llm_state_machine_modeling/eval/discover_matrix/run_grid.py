"""The pair grid a generation runs, read from disk rather than typed.

Written after the same mistake twice in one round: a measurement script carried the grid as a
literal and had `0058` in it, which has never been in the grid, while `0000` was missing. The
number it produced (22 affected scopes, actually 16) went into a pre-registration document. A
grid that is typed is a second source of a fact that already exists in two places on disk.

Precedence:
  1. `--grid` on the command line, for a generation that deliberately changes the set.
  2. The most recent `runs/paper1/matrix-*/run1/` directory listing, which is what a generation
     actually ran -- the only unfalsifiable record of it.
  3. `holdout.json`'s `run_pairs` union its `holdout`, which is what the frozen bookkeeping
     says is in play.

Deliberately no hardcoded fallback. A checkout with neither runs nor a frozen hold-out cannot
know the grid, and guessing is how the wrong number gets into a document that claims to be
pre-registered.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
RUNS = REPO / "runs" / "paper1"

_CELL = re.compile(r"^(\d{4})-(claude|gpt)$")


def from_runs(generation: str | None = None) -> list[str]:
    """Pairs that a generation's `run1/` actually contains. Newest generation if unspecified."""

    if not RUNS.is_dir():
        return []
    candidates = sorted(
        (d for d in RUNS.glob("matrix-*") if (d / "run1").is_dir()),
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )
    if generation:
        candidates = [d for d in candidates if d.name == generation or d.name.endswith(generation)]
    for directory in candidates:
        pairs = set()
        for cell in (directory / "run1").iterdir():
            match = _CELL.match(cell.name)
            if match and cell.is_dir():
                pairs.add(match.group(1))
        if pairs:
            return sorted(pairs)
    return []


def from_frozen() -> list[str]:
    """`run_pairs` union `holdout`: what the frozen bookkeeping says is in play."""

    path = HERE / "holdout.json"
    if not path.is_file():
        return []
    frozen = json.loads(path.read_text())
    return sorted(set(frozen.get("run_pairs") or ()) | set(frozen.get("holdout") or ()))


def grid(explicit: str | None = None, generation: str | None = None) -> list[str]:
    """The grid, by the precedence in the module docstring. Raises rather than guessing."""

    if explicit:
        pairs = sorted({p.strip() for p in re.split(r"[,\s]+", explicit) if p.strip()})
        if pairs:
            return pairs
    for source in (lambda: from_runs(generation), from_frozen):
        pairs = source()
        if pairs:
            return pairs
    raise SystemExit(
        "cannot determine the grid: no `runs/paper1/matrix-*/run1/` and no `holdout.json`. "
        "Pass it with `--grid` and say in the report where it came from."
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grid")
    parser.add_argument("--generation", help="e.g. matrix-v21")
    parser.add_argument("--source", action="store_true", help="print where it came from")
    args = parser.parse_args()
    pairs = grid(args.grid, args.generation)
    if args.source:
        origin = (
            "--grid"
            if args.grid
            else ("runs" if from_runs(args.generation) == pairs else "holdout.json")
        )
        print(f"{len(pairs)} pairs from {origin}: {' '.join(pairs)}")
    else:
        print(" ".join(pairs))
