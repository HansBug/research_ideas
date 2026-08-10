#!/usr/bin/env python3
"""Put a fresh eight-cell run next to the recorded baseline, per issue #175 §7.3.

This is arithmetic, not adjudication. `cells.json` has no generator -- its `matches_manual_diff`
mapping and its evidence prose were written by hand, and `HIT_CRITERION.md` §5 is explicit that
a mechanical verdict is not final. So this script reports what changed in the shapes that can
be counted, and leaves "is this the same defect the ledger means" to the person doing the
re-annotation.

What it can settle on its own is narrower and still worth having:

  published vs distinct   -- the merge change succeeded exactly when these agree, and that
                             comparison needs no judgement once the defects are annotated
  the pre-registered      -- issue #175 §7.2 fixed, before the run, that EIS-0050-01 counts
  hit shape                  only via `state_declared`; the superseded `event_declared`
                             spelling does not. Recording the shape here keeps that from
                             being relitigated against whatever the run produced
  the attribution split   -- §7.6 asks that a `state_declared(...auto_final)` which lands as
                             representation_debt or unattributed be read as an attribution-layer
                             miss rather than a splitter failure. Those look identical in a
                             count, so they are separated here

Usage: compare_run_to_baseline.py <run_dir> [--json]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from issue_compat import requirement_ids_of  # noqa: E402

CELLS = HERE / "manual_review" / "loop_audit" / "cells.json"

#: The eight-cell baseline, read from `cells.json` totals rather than restated here so the
#: two cannot drift apart.
BASELINE_KEYS = (
    "published",
    "distinct_manual_defects_hit",
    "missed",
    "over_reported",
)

#: Fixed by issue #175 §7.2 before the run, so the verdict cannot be chosen after seeing the
#: output. `EIS-0050-01`'s basis was changed by parent ruling on 2026-07-30: the disjunctive
#: reading of the specification's comma list was withdrawn, and with it
#: `event_declared(...human_steering_cmd)`. Only the state spelling counts.
PREREGISTERED_HIT_SHAPES = {
    "EIS-0050-01": {
        "counts": "state_declared",
        "does_not_count": "event_declared",
        "why": "parent ruling 2026-07-30 superseded the event_declared basis",
    }
}


def _load_cells() -> dict:
    return json.loads(CELLS.read_text(encoding="utf-8"))


def _cell_dirs(run_dir: pathlib.Path) -> list[pathlib.Path]:
    return sorted(
        path.parent
        for path in run_dir.glob("*/discover-completed.json")
    )


def _summarise_cell(cell_dir: pathlib.Path) -> dict:
    record = json.loads((cell_dir / "discover-completed.json").read_text())
    issues = record.get("issues") or []
    excluded = record.get("excluded_findings") or []
    merged = [i for i in issues if len(requirement_ids_of(i)) > 1]
    return {
        "cell": cell_dir.name,
        "status": record.get("status"),
        "coverage_status": record.get("coverage_status"),
        "published": len(issues),
        "merged_issues": len(merged),
        "merge_groups": [
            {
                "issue_id": i.get("issue_id"),
                "requirement_ids": list(requirement_ids_of(i)),
                "shared_root_cause": i.get("shared_root_cause"),
                "shared_elements": list(i.get("shared_elements") or []),
            }
            for i in merged
        ],
        "excluded_findings": len(excluded),
        "satisfied": list(record.get("satisfied_requirement_ids") or []),
        # §7.6: the same claim can arrive attributed or not, and only the first is published.
        # Separating them is what tells a splitter failure from an attribution-layer one.
        "auto_final_published": [
            i.get("issue_id")
            for i in issues
            if "auto_final" in json.dumps(i, ensure_ascii=False)
        ],
        "auto_final_excluded": [
            {"issue_id": e.get("issue_id"), "attribution_status": e.get("attribution_status")}
            for e in excluded
            if "auto_final" in json.dumps(e, ensure_ascii=False)
        ],
        # The deterministic layer's three repair signals. They are on disk either way; if no
        # tool surfaces them, "the adjudicator systematically confuses the two baskets" stays
        # invisible while every run reports clean.
        "rationale_citations_annotated": (
            record.get("adjudication_reconciliation") or {}
        ).get("rationale_citations_annotated")
        or [],
        "misfiled_findings_moved": (
            record.get("adjudication_reconciliation") or {}
        ).get("misfiled_findings_moved")
        or [],
        "thin_merge_warnings": (
            record.get("adjudication_reconciliation") or {}
        ).get("thin_merge_warnings")
        or [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=pathlib.Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    baseline = _load_cells()["totals"]
    cells = [_summarise_cell(d) for d in _cell_dirs(args.run_dir)]
    published = sum(c["published"] for c in cells)

    report = {
        "run_dir": str(args.run_dir),
        "cells_found": len(cells),
        "baseline": {k: baseline.get(k) for k in BASELINE_KEYS},
        "this_run": {
            "published": published,
            "merged_issues": sum(c["merged_issues"] for c in cells),
            "excluded_findings": sum(c["excluded_findings"] for c in cells),
        },
        "preregistered_hit_shapes": PREREGISTERED_HIT_SHAPES,
        "cells": cells,
        # Stated rather than computed: the count of distinct defects is the output of the
        # manual pass described in §7.2, and inventing a number here would make the very
        # comparison this script exists to support look already settled.
        "requires_manual_annotation": [
            "distinct_manual_defects_hit -- per-item matches_manual_diff against the ledger",
            "missed -- which expected issues produced nothing",
            "over_reported -- published issues matching no expected issue",
            "merge correctness -- each merge group checked against §7.5",
        ],
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print(f"run: {args.run_dir}   cells: {len(cells)}")
    print(f"\n{'cell':<16}{'status':<12}{'cov':<8}{'pub':>4}{'merged':>8}{'excl':>6}"
          f"{'moved':>7}{'thin':>6}  auto_final")
    for c in cells:
        af = ",".join(c["auto_final_published"]) or "-"
        if c["auto_final_excluded"]:
            af += " (excluded: " + ",".join(
                f"{x['issue_id']}={x['attribution_status']}" for x in c["auto_final_excluded"]
            ) + ")"
        print(f"{c['cell']:<16}{str(c['status']):<12}{str(c['coverage_status']):<8}"
              f"{c['published']:>4}{c['merged_issues']:>8}{c['excluded_findings']:>6}"
              f"{len(c['misfiled_findings_moved']):>7}{len(c['thin_merge_warnings']):>6}  {af}")
    print(f"\npublished this run: {published}   baseline: {baseline.get('published')}")
    print(f"merged issues:      {report['this_run']['merged_issues']}")
    merges = [g for c in cells for g in c["merge_groups"]]
    if merges:
        print("\nmerge groups (each must be checked against §7.5):")
        for g in merges:
            print(f"  {g['issue_id']}: {' + '.join(g['requirement_ids'])}")
            print(f"     cause: {g['shared_root_cause']}")
            print(f"     elements: {g['shared_elements']}")
    moved = [(c["cell"], m) for c in cells for m in c["misfiled_findings_moved"]]
    if moved:
        print("\n被确定性层归位的发现（LLM 放错筐，非拒绝）:")
        for cell, m in moved:
            print(f"  {cell}: {m['issue_id']}  {m['from']} → {m['to']}"
                  f"  报告={m.get('reported_status')} 绑定={m.get('binding_status')}")
    thin = [(c["cell"], w) for c in cells for w in c["thin_merge_warnings"]]
    if thin:
        print("\n单元素合并（需人工复核）:")
        for cell, w in thin:
            print(f"  {cell}: {w['issue_id']}  {w['shared_elements']}")
    print("\nstill requires the manual pass of §7.2:")
    for item in report["requires_manual_annotation"]:
        print(f"  - {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
