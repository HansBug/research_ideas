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

#: The same cell goes by two names. Run directories and this table use `0029-claude`; the
#: adjudicated ledger and `detect_fabrications.py` both use the full profile
#: (`0029-claude-opus-4-7`). Joining on the raw string silently matched nothing, so every
#: verdict fell through to the default branch and looked like a checked result.
_MODEL_ALIASES = {"claude-opus-4-7": "claude", "gpt-5.5": "gpt"}


def _canonical_cell(cell: str) -> str:
    text = str(cell)
    for long_name, short in _MODEL_ALIASES.items():
        if text.endswith(f"-{long_name}"):
            return text[: -len(long_name)] + short
    return text


def _adjudicated() -> tuple[set[tuple[str, str]], set[tuple[str, str]]]:
    """The two adjudicated sets, kept apart: `(fabricated, grounded)`.

    Merging them is the mistake the file itself warns against -- "Mixing the two kinds
    understates precision when a grounded extra is counted as a false positive". `grounded`
    records extras the ledger does not list but the pair's NL supports; those are correct
    findings, not noise.

    Keyed `(cell, requirement_id)` with `run` dropped, which is deliberate and limited:
    the file's own `id_matching_caveat` says a requirement id means different things across
    runs, so a hit here is a *hint that a same-shaped finding was adjudicated before*, not a
    verdict on this one. The report says so where it uses it.
    """
    if not KNOWN_FP.exists():
        return set(), set()
    payload = json.loads(KNOWN_FP.read_text(encoding="utf-8"))
    fabricated: set[tuple[str, str]] = set()
    grounded: set[tuple[str, str]] = set()
    for entry in payload.get("fabricated") or []:
        cell, requirement = entry.get("cell"), entry.get("requirement_id")
        if cell and requirement:
            fabricated.add((_canonical_cell(cell), str(requirement)))
    for entry in payload.get("grounded") or []:
        cell = entry.get("cell")
        # `grounded` entries carry `requirement_ids` (plural); reading only the singular key
        # was the second half of why this join never fired.
        for requirement in entry.get("requirement_ids") or ([entry.get("requirement_id")] if entry.get("requirement_id") else []):
            if cell and requirement:
                grounded.add((_canonical_cell(cell), str(requirement)))
    return fabricated, grounded


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
                key = (
                    _canonical_cell(finding.get("cell")),
                    str(finding.get("requirement_id")),
                )
                matched.setdefault(key, []).append(finding)
    return matched if found else None


def _classify(
    cell: str,
    issue: dict,
    fabrication: dict[tuple[str, str], list[dict]] | None,
    adjudicated: tuple[set[tuple[str, str]], set[tuple[str, str]]],
) -> dict:
    """One unexpected issue, with the facts a reader would otherwise have to dig for."""
    fabricated_set, grounded_set = adjudicated
    requirements = requirement_ids_of(issue)
    hits = [f for rid in requirements for f in (fabrication or {}).get((cell, rid), [])]
    classes = {str(f.get("defect_class", "")) for f in hits}
    same_shape_fabricated = any((cell, rid) in fabricated_set for rid in requirements)
    same_shape_grounded = any((cell, rid) in grounded_set for rid in requirements)

    if any(c.startswith("published-issue-no-longer-false") for c in classes):
        verdict, why = "does-not-reproduce", "主断言重算不再为 False（含谓词拒答）"
    elif "false-rests-on-converter-owned-element" in classes:
        verdict, why = "rests-on-projection", "False 依赖投影注入的元素，非作者所写"
    elif "unparseable-assertion" in classes:
        verdict, why = "unverifiable", "断言表达式无法解析，无法重算"
    elif same_shape_fabricated:
        verdict, why = "same-shape-adjudicated-fabricated", "同 cell+requirement 曾被裁定为捏造（跨 run 仅作提示）"
    elif same_shape_grounded:
        verdict, why = "same-shape-adjudicated-grounded", "同 cell+requirement 曾被裁定为 grounded：台账未列但 NL 支持"
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
        "same_shape_adjudicated": (
            "fabricated" if same_shape_fabricated
            else ("grounded" if same_shape_grounded else None)
        ),
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
    adjudicated = _adjudicated()
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
                        unexpected.append(_classify(cell, issue, fabrication, adjudicated))
                report.setdefault(cell, {"N": len(entries), "rounds": {}})["rounds"][
                    run_dir.name
                ] = {
                    "published": len(issues),
                    "n": len(matched),
                    "matched": {k: v for k, v in sorted(matched.items())},
                    "missed": sorted(e["id"] for e in entries if e["id"] not in matched),
                    "unexpected": unexpected,
                    # A claim the splitter produced and the attribution layer refused. It is
                    # not a miss by the same mechanism as "never asserted", and a table over
                    # published issues alone cannot see it -- yet on `0050-claude` that is
                    # the entire story of the cell.
                    "blocked_by_attribution": [
                        {
                            "issue_id": e.get("issue_id"),
                            "requirement_ids": list(requirement_ids_of(e)),
                            "attribution_status": e.get("attribution_status"),
                            "title": e.get("title"),
                        }
                        for e in (data["record"].get("excluded_findings") or [])
                    ],
                    # Two issues matching one ledger entry is a duplicate the merge change
                    # exists to remove, and it is invisible in `published` alone.
                    "duplicate_matches": {
                        k: v for k, v in matched.items() if len(v) > 1
                    },
                }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print(f"{'cell':<14}{'N':>3}  n/N per round   多报/轮   归因挡/轮  命中并集         从未命中")
    for cell, info in report.items():
        rounds = info["rounds"]
        ns = "/".join(str(r["n"]) for r in rounds.values())
        us = "/".join(str(len(r["unexpected"])) for r in rounds.values())
        bs = "/".join(str(len(r["blocked_by_attribution"])) for r in rounds.values())
        union = sorted({k for r in rounds.values() for k in r["matched"]})
        never = sorted(set.intersection(*[set(r["missed"]) for r in rounds.values()]))
        print(f"{cell:<14}{info['N']:>3}  {ns:<15} {us:<9} {bs:<10} "
              f"{','.join(x.replace('EIS-','') for x in union) or '-':<16} "
              f"{','.join(x.replace('EIS-','') for x in never) or '-'}")

    print("\n=== 被归因层挡住的断言（提出了但未发布）===")
    blocked = [(rn, c, b) for c, i in report.items()
               for rn, r in i["rounds"].items() for b in r["blocked_by_attribution"]]
    for rn, c, b in blocked:
        print(f"  {rn}/{c}  {b['attribution_status']:<20} {(b['title'] or '')[:58]}")
    if not blocked:
        print("  （无）")

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
