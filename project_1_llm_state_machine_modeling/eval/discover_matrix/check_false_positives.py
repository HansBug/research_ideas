"""Cross-check a matrix run against the adjudicated false-positive ledger.

The hit table answers "did we find the expected defects".  It says nothing about
what else got published, and that half decides whether the method is usable: a
run that finds all three expected defects while fabricating five is not a good
run.  `known_false_positives.json` records the adjudication for matrix-v16 --
which extras are grounded in the pair's NL and which the model does not have --
so a later run can be scored against it instead of re-argued from scratch.

Three outcomes matter:

    still fabricating   a fabricated finding reappeared -> the predicate defect
                        behind it is unfixed, and the fix (if one was made) did
                        not reach it
    fixed               a fabricated finding is gone -> report which, so the
                        claim rests on the ledger rather than on a total
    unadjudicated       an extra nobody has ruled on yet -> needs a human call
                        before the run's precision can be quoted

Matching is by (cell, requirement_id) *within one run*, not by title: titles are
LLM-written prose and change wording between runs on the same defect.  The run
matters because requirement ids do not survive it -- the splitter reuses them for
different claims, so `0006-claude/REQ-001` is the substate-count finding in
matrix-v16 and a missing mission-complete state in matrix-v18.  Replaying one
run's adjudications is what this script is for; scoring a *new* run is what
`detect_fabrications.py` is for, and that one re-derives each class from the model
and needs no ids.

Usage: check_false_positives.py <audit_dir> [run]
    <audit_dir>  the `audit/` bundle build_gist.py wrote
    [run]        which run's adjudications to replay (default: matrix-v16)
"""

from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
LEDGER = HERE / "known_false_positives.json"


def _cell_name(path: pathlib.Path) -> str:
    return path.name.removesuffix("-audit.json")


def _credited_titles(record: dict) -> set[str]:
    """Titles the hit criterion credited, so extras can be told from hits."""

    out: set[str] = set()
    for verdict in record.get("expected_issue_verdicts") or []:
        for key in ("hit_title", "matched_title", "title"):
            value = verdict.get(key)
            if value:
                out.add(str(value))
    return out


def scan(audit_dir: pathlib.Path, run: str = "matrix-v16") -> dict:
    ledger = json.loads(LEDGER.read_text())
    fabricated = {
        (entry["cell"], entry["requirement_id"]): entry
        for entry in ledger["fabricated"]
        if entry.get("run", "matrix-v16") == run
    }
    grounded = {
        (entry["cell"], req)
        for entry in ledger["grounded"]
        if entry.get("run", "matrix-v16") == run
        for req in entry["requirement_ids"]
    }
    if not fabricated and not grounded:
        raise SystemExit(f"no adjudications recorded for run {run!r}")

    seen: set[tuple[str, str]] = set()
    still: list[dict] = []
    unadjudicated: list[dict] = []
    incomplete: list[str] = []

    for path in sorted(audit_dir.glob("*-audit.json")):
        record = json.loads(path.read_text())
        cell = _cell_name(path)
        if record.get("terminal") != "completed":
            incomplete.append(f"{cell} (terminal={record.get('terminal')})")
            continue
        credited = _credited_titles(record)
        artifact = record.get("terminal_artifact") or {}
        for issue in artifact.get("issues") or []:
            requirement = str(issue.get("requirement_id") or "")
            key = (cell, requirement)
            seen.add(key)
            title = str(issue.get("title") or "")
            if title and title in credited:
                continue  # credited against an expected issue; not an extra
            if key in fabricated:
                still.append({"cell": cell, "requirement_id": requirement, "title": title,
                              "defect_class": fabricated[key]["defect_class"]})
            elif key not in grounded:
                unadjudicated.append({"cell": cell, "requirement_id": requirement, "title": title})

    return {
        "still_fabricating": still,
        "fixed": [
            {"cell": cell, "requirement_id": req, "defect_class": entry["defect_class"]}
            for (cell, req), entry in sorted(fabricated.items())
            if (cell, req) not in seen
        ],
        "unadjudicated": unadjudicated,
        # Reported rather than skipped: a fabricated finding absent because its
        # cell never finished is not a fix, and counting it as one would be the
        # easiest way to fake progress here.
        "incomplete_cells": incomplete,
    }


def main() -> int:
    if not 2 <= len(sys.argv) <= 3:
        print(__doc__)
        return 2
    run = sys.argv[2] if len(sys.argv) == 3 else "matrix-v16"
    print(f"回放 {run} 的判定\n")
    result = scan(pathlib.Path(sys.argv[1]), run)

    if result["incomplete_cells"]:
        print("未完成的格子（其缺失不计作修复）:")
        for cell in result["incomplete_cells"]:
            print(f"  {cell}")

    print(f"\n仍在捏造 {len(result['still_fabricating'])} 条:")
    for row in result["still_fabricating"]:
        print(f"  {row['cell']:22s} {row['requirement_id']:12s} [{row['defect_class']}] {row['title']}")

    print(f"\n已消失 {len(result['fixed'])} 条:")
    for row in result["fixed"]:
        print(f"  {row['cell']:22s} {row['requirement_id']:12s} [{row['defect_class']}]")

    print(f"\n待人工判定 {len(result['unadjudicated'])} 条:")
    for row in result["unadjudicated"]:
        print(f"  {row['cell']:22s} {row['requirement_id']:12s} {row['title']}")

    # Non-zero when something is still fabricated or unadjudicated, so this can
    # gate a run before its numbers are quoted anywhere.
    return 1 if (result["still_fabricating"] or result["unadjudicated"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
