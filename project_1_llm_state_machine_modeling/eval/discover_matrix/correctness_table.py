#!/usr/bin/env python3
"""Per-cell correctness, not just stability: how many expected defects, and what else got reported.

Stability answers "does the same input give the same answer". It says nothing about whether
that answer is right -- `0050-claude` was perfectly stable across three rounds at zero issues,
and zero is the wrong number there. So this reports coverage and over-reporting side by side.

Three columns matter and they are established three different ways:

  **n/N** -- expected defects matched. `N` is the ledger's count for the pair; `n` comes from
  the same mechanical proxy `round_variance.py` uses (element overlap, predicate as a
  tiebreaker). A proxy, and `HIT_CRITERION.md` §5 reserves the verdict for a person.

  **unexpected** -- published issues no ledger entry claims. This is *not* the same as
  "fabricated". The ledger is 126 entries over 60 pairs assembled by hand; a real defect
  nobody wrote down is unexpected and correct. Calling every unmatched issue a false positive
  would credit the ledger with completeness it does not have.

  **verdict per unexpected issue** -- so the distinction above can actually be made. Each one
  gets two machine-checkable facts and one classification:

    `assertion_still_false`  the primary assertion re-derived against the current predicates.
                             False here means the issue does not survive its own evidence.
    `evidence_is_own`        whether the False rests on an element in `attribution_exclusions`
                             -- i.e. on something the projection introduced rather than
                             something the author wrote.
    `known_false_positive`   whether `(run, cell, requirement_id)` is in the adjudicated
                             ledger of false positives.

  Both facts true and not a known false positive => `plausible-unlisted`: an issue the current
  layer stands behind, which the ledger happens not to list. Anything else is named for what
  failed. `plausible-unlisted` is a queue for human adjudication, not a pass.

Usage: correctness_table.py <run_dir> [<run_dir> ...] [--json]
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
from round_variance import (  # noqa: E402
    MODELS,
    PAIRS,
    _issue_signature,
    _ledger_by_pair,
    _match,
    _read_cell,
)

KNOWN_FP = HERE / "known_false_positives.json"


def _known_false_positives() -> set[tuple[str, str]]:
    """Adjudicated false positives, keyed `(cell, requirement_id)`.

    The file keys on `(run, cell, requirement_id)` and warns that a requirement id means
    different things in different runs. Dropping `run` here is deliberate and stated: these
    are fresh runs whose ids no entry can match exactly, so the pair is used as a *hint* and
    a hit is reported rather than acted on.
    """
    if not KNOWN_FP.exists():
        return set()
    payload = json.loads(KNOWN_FP.read_text(encoding="utf-8"))
    entries = payload.get("false_positives") or payload.get("entries") or []
    out: set[tuple[str, str]] = set()
    for entry in entries:
        cell, requirement = entry.get("cell"), entry.get("requirement_id")
        if cell and requirement:
            out.add((str(cell), str(requirement)))
    return out


def _fabrication_findings(
    run_dir: pathlib.Path, scan_dirs: list[pathlib.Path]
) -> dict[tuple[str, str], list[dict]] | None:
    """`_fabrication_scan.json` for this run, indexed by `(cell, requirement_id)`.

    `None` means no scan was found for this run, and the caller reports `unknown` rather than
    assuming a clean result -- a missing file reading the same as an empty findings list is
    exactly the confusion that would let an unverified issue look adjudicated. The scan runs
    at bundle time (`build_gist.py`), not at run time, so its location has to be supplied.

    Matching is by run directory name, because scanning every bundle on the machine and
    merging the results would attribute one run's findings to another.
    """
    matched: dict[tuple[str, str], list[dict]] = {}
    found = False
    for base in scan_dirs:
        for path in base.rglob("_fabrication_scan.json"):
            if run_dir.name not in path.parts:
                continue
            found = True
            payload = json.loads(path.read_text(encoding="utf-8"))
            for finding in payload.get("findings") or []:
                key = (str(finding.get("cell")), str(finding.get("requirement_id")))
                matched.setdefault(key, []).append(finding)
    return matched if found else None


def _classify(
    cell: str,
    issue: dict,
    fabrication: dict[tuple[str, str], list[dict]] | None,
    known_fp: set[tuple[str, str]],
) -> dict:
    """One unexpected issue, with the facts a reader would otherwise have to dig for."""
    requirements = requirement_ids_of(issue)
    hits = [f for rid in requirements for f in (fabrication or {}).get((cell, rid), [])]
    classes = {str(f.get("defect_class", "")) for f in hits}
    flagged_fp = any((cell, rid) in known_fp for rid in requirements)

    if any(c.startswith("published-issue-no-longer-false") for c in classes):
        verdict, why = "does-not-reproduce", "主断言重算不再为 False"
    elif "false-rests-on-converter-owned-element" in classes:
        verdict, why = "rests-on-projection", "False 依赖投影注入的元素，非作者所写"
    elif "unparseable-assertion" in classes:
        verdict, why = "unverifiable", "断言表达式无法解析，无法重算"
    elif flagged_fp:
        verdict, why = "known-false-positive", "命中已裁定假阳台账（按 cell+requirement 提示）"
    elif fabrication is None:
        verdict, why = "unknown", "未找到该轮的 _fabrication_scan.json，无机器判据"
    else:
        verdict, why = "plausible-unlisted", "重算仍为 False 且证据非投影所有；台账未列，待人工裁定"
    return {
        "issue_id": issue.get("issue_id"),
        "requirement_ids": list(requirements),
        "title": issue.get("title"),
        "verdict": verdict,
        "why": why,
        "fabrication_classes": sorted(classes),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dirs", nargs="+", type=pathlib.Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--scan-dir",
        type=pathlib.Path,
        action="append",
        default=[],
        help="directory holding gist bundles with _fabrication_scan.json, e.g. /tmp/v2gist",
    )
    args = parser.parse_args()

    ledger = _ledger_by_pair()
    known_fp = _known_false_positives()
    report: dict[str, dict] = {}

    for run_dir in args.run_dirs:
        fabrication = _fabrication_findings(run_dir, args.scan_dir)
        for pair in PAIRS:
            entries = ledger[pair]
            for model in MODELS:
                cell = f"{pair}-{model}"
                data = _read_cell(run_dir / cell)
                if data is None or data.get("terminal") != "completed":
                    continue
                issues = data["record"].get("issues") or []
                matched: dict[str, list[str]] = {}
                unexpected: list[dict] = []
                for issue in issues:
                    hit = _match(_issue_signature(issue, data["requirements"]), entries)
                    if hit:
                        matched.setdefault(hit[0], []).append(issue.get("issue_id"))
                    else:
                        unexpected.append(_classify(cell, issue, fabrication, known_fp))
                report.setdefault(cell, {"N": len(entries), "rounds": {}})["rounds"][
                    run_dir.name
                ] = {
                    "published": len(issues),
                    "n": len(matched),
                    "matched": {k: v for k, v in sorted(matched.items())},
                    "missed": sorted(e["id"] for e in entries if e["id"] not in matched),
                    "unexpected": unexpected,
                    # Two issues matching one ledger entry is a duplicate the merge change
                    # exists to remove, and it is invisible in `published` alone.
                    "duplicate_matches": {
                        k: v for k, v in matched.items() if len(v) > 1
                    },
                }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print(f"{'cell':<14}{'N':>3}  n/N per round        多报/轮   命中的台账条目")
    for cell, info in report.items():
        rounds = info["rounds"]
        ns = "/".join(str(r["n"]) for r in rounds.values())
        us = "/".join(str(len(r["unexpected"])) for r in rounds.values())
        union = sorted({k for r in rounds.values() for k in r["matched"]})
        print(f"{cell:<14}{info['N']:>3}  {ns:<20} {us:<9} "
              f"{','.join(x.replace('EIS-','') for x in union) or '-'}")

    print("\n=== 多报逐条判据 ===")
    any_unexpected = False
    for cell, info in report.items():
        for run_name, r in info["rounds"].items():
            for u in r["unexpected"]:
                any_unexpected = True
                print(f"  {run_name}/{cell}  {u['verdict']:<22} {u['why']}")
                print(f"      {u['issue_id'][:56]}  reqs={u['requirement_ids']}")
                print(f"      {(u['title'] or '')[:88]}")
    if not any_unexpected:
        print("  （无）")

    print("\n=== 同一台账条目被报多次（重复）===")
    dups = [(rn, c, k, v) for c, i in report.items()
            for rn, r in i["rounds"].items() for k, v in r["duplicate_matches"].items()]
    for rn, c, k, v in dups:
        print(f"  {rn}/{c}: {k} ← {v}")
    if not dups:
        print("  （无）")

    print("\n⚠️ n/N 用机械代理匹配；`plausible-unlisted` 是待人工裁定的队列，不是通过。"
          "\n   台账 126 条是人工汇编，不具完备性 —— 未匹配不等于虚报。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
