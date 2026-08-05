#!/usr/bin/env python3
"""Measure how much an eight-cell result moves between identical runs.

Issue #175 planned a before/after comparison on one run per configuration. The first run
made that plan unusable: `0050-claude` published one issue in a smoke run and zero in the
matrix run, on the same commit with the same inputs. Nothing downstream can be read until
the size of that movement is known, because an effect smaller than the noise is not an
effect.

So this reports spread first and central tendency second. For each cell it lists what every
round published, and marks a cell **unstable** when the rounds disagree at all -- not when
they disagree by some threshold. A single flip is enough to make a one-run comparison
unsound, which is the question being asked.

The mapping from a published issue to a `EIS-*` ledger entry is a *mechanical proxy*: it
matches on the ledger's `primary_predicate` plus the distinctive model elements named in its
assertion, and it is wrong whenever a defect is expressible in more than one predicate. It is
here to make the rounds comparable to each other, not to settle whether a defect was found --
`HIT_CRITERION.md` §5 reserves that for a person, and this script prints the caveat with the
numbers rather than in a footnote.

Usage: round_variance.py <run_dir> [<run_dir> ...] [--json]
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from issue_compat import requirement_ids_of  # noqa: E402

LEDGER = HERE / "manual_review" / "expected_issue_set.json"
CELLS = HERE / "manual_review" / "loop_audit" / "cells.json"

PAIRS = ("0000", "0006", "0029", "0050")
MODELS = ("claude", "gpt")

#: Path segments that carry no discriminating power -- every element in a pair shares the
#: namespace prefix, so leaving it in would make every issue match every ledger entry.
_NOISE = re.compile(r"^(llms_emp_feedback_final_\d+|state|event|source|target|leaf|composite|any)$")


def _elements(text: str) -> set[str]:
    """Distinctive names in a blob of text, namespace prefixes stripped."""
    out: set[str] = set()
    for token in re.findall(r"[A-Za-z_][A-Za-z_0-9.]{2,}", text):
        for part in token.split("."):
            if len(part) > 3 and not _NOISE.match(part):
                out.add(part.lower())
    return out


def _ledger_by_pair() -> dict[str, list[dict]]:
    records = json.loads(LEDGER.read_text(encoding="utf-8"))["records"]
    by_pair: dict[str, list[dict]] = collections.defaultdict(list)
    for record in records:
        if record["pair"] not in PAIRS:
            continue
        assertion_text = json.dumps(record.get("assertions") or [], ensure_ascii=False)
        by_pair[record["pair"]].append(
            {
                "id": record["id"],
                "predicate": record.get("primary_predicate"),
                "elements": _elements(assertion_text),
                "statement": (record.get("statement") or "")[:90],
            }
        )
    return by_pair


def _issue_signature(issue: dict, requirements: dict[str, dict]) -> tuple[str | None, set[str]]:
    """The predicate and elements a published issue rests on.

    Read from the Requirements it names rather than from its prose: a title is written by
    the model and varies between rounds even when the underlying binding does not, which is
    precisely the variation this script must not mistake for a different defect.
    """
    predicates, elements = set(), set()
    for rid in requirement_ids_of(issue):
        requirement = requirements.get(rid) or {}
        if requirement.get("predicate"):
            predicates.add(requirement["predicate"])
        elements |= _elements(json.dumps(requirement.get("predicate_bindings") or {},
                                         ensure_ascii=False))
    elements |= _elements(" ".join(issue.get("shared_elements") or ()))
    return (sorted(predicates)[0] if len(predicates) == 1 else None), elements


def _match(issue_sig: tuple[str | None, set[str]], entries: list[dict]) -> tuple[str, bool] | None:
    """Best ledger entry for one issue, plus whether the predicate agreed.

    Element overlap decides; the predicate only breaks ties. Filtering on the predicate was
    the first attempt and it was wrong: the same defect is often expressible more than one
    way, and `EIS-0000-01` is the case in point -- the ledger records it under
    `occupancy_after` while run1 reported it under `terminates`. Both describe the same
    misplaced `Power_Off` edge, and a filter would have scored that as a miss.

    The predicate agreement is returned rather than discarded, because a match found without
    it is the weaker kind and a reader deserves to see which is which. `None` on a tie stays:
    a forced match would manufacture the hit this is meant to detect.
    """
    predicate, elements = issue_sig
    scored = []
    for entry in entries:
        overlap = len(elements & entry["elements"])
        if overlap < 2:
            continue
        agrees = predicate is not None and entry["predicate"] == predicate
        scored.append((overlap + (2 if agrees else 0), overlap, agrees, entry["id"]))
    if not scored:
        return None
    scored.sort(reverse=True)
    if len(scored) > 1 and scored[0][0] == scored[1][0]:
        return None
    return scored[0][3], scored[0][2]


def _read_cell(cell_dir: pathlib.Path) -> dict | None:
    completed = cell_dir / "discover-completed.json"
    if not completed.exists():
        failed = cell_dir / "discover-failed.json"
        return {"terminal": "failed" if failed.exists() else "missing"} if failed.exists() else None
    record = json.loads(completed.read_text())
    requirements = {}
    adjudication_reqs = record.get("requirement_set") or {}
    for requirement in (adjudication_reqs.get("requirements") or []):
        requirements[requirement["requirement_id"]] = requirement
    if not requirements:
        # `discover-completed.json` does not always carry the requirement set; fall back to
        # the last split-requirements state update, which does.
        updates = sorted(cell_dir.glob("records/*split-requirements-state-update/record.json"))
        if updates:
            blob = json.loads(updates[-1].read_text())
            for requirement in _find_requirements(blob):
                requirements[requirement["requirement_id"]] = requirement
    return {"terminal": "completed", "record": record, "requirements": requirements}


def _find_requirements(blob: object, depth: int = 0) -> list[dict]:
    if depth > 8:
        return []
    if isinstance(blob, dict):
        candidate = blob.get("requirements")
        if isinstance(candidate, list) and candidate and isinstance(candidate[0], dict):
            if "requirement_id" in candidate[0]:
                return candidate
        for value in blob.values():
            found = _find_requirements(value, depth + 1)
            if found:
                return found
    elif isinstance(blob, list):
        for value in blob:
            found = _find_requirements(value, depth + 1)
            if found:
                return found
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dirs", nargs="+", type=pathlib.Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    ledger = _ledger_by_pair()
    baseline_cells = {c["cell"]: c for c in json.loads(CELLS.read_text())["cells"]}

    rounds: dict[str, dict[str, dict]] = {}
    for run_dir in args.run_dirs:
        name = run_dir.name
        rounds[name] = {}
        for pair in PAIRS:
            for model in MODELS:
                cell = f"{pair}-{model}"
                data = _read_cell(run_dir / cell)
                if data is None:
                    continue
                if data["terminal"] != "completed":
                    rounds[name][cell] = {"terminal": data["terminal"]}
                    continue
                issues = data["record"].get("issues") or []
                matched, unmatched, weak = [], 0, []
                for issue in issues:
                    hit = _match(_issue_signature(issue, data["requirements"]), ledger[pair])
                    if hit:
                        matched.append(hit[0])
                        if not hit[1]:
                            weak.append(hit[0])
                    else:
                        unmatched += 1
                rounds[name][cell] = {
                    "terminal": "completed",
                    "published": len(issues),
                    "merged": sum(1 for i in issues if len(requirement_ids_of(i)) > 1),
                    "excluded": len(data["record"].get("excluded_findings") or []),
                    "eis_matched": sorted(set(matched)),
                    # Matched on elements alone -- the ledger records the defect under a
                    # different predicate. Real (EIS-0000-01 is `occupancy_after` there and
                    # `terminates` here) but weaker, so it is surfaced rather than merged in.
                    "eis_matched_predicate_differs": sorted(set(weak)),
                    "unmatched_issues": unmatched,
                    "titles": [i.get("title") for i in issues],
                }

    report = {"rounds": list(rounds), "cells": {}, "unstable_cells": [], "stable_cells": []}
    for pair in PAIRS:
        for model in MODELS:
            cell = f"{pair}-{model}"
            per_round = {r: rounds[r].get(cell) for r in rounds}
            done = [v for v in per_round.values() if v and v.get("terminal") == "completed"]
            if not done:
                continue
            published = [v["published"] for v in done]
            eis_sets = [tuple(v["eis_matched"]) for v in done]
            unstable = len(set(published)) > 1 or len(set(eis_sets)) > 1
            entry = {
                "rounds_completed": len(done),
                "rounds_attempted": len([v for v in per_round.values() if v]),
                "published": published,
                "published_spread": (min(published), max(published)),
                "eis_matched_per_round": [list(s) for s in eis_sets],
                "eis_union": sorted({e for s in eis_sets for e in s}),
                "eis_intersection": sorted(set.intersection(*[set(s) for s in eis_sets])) if eis_sets else [],
                "merged": [v["merged"] for v in done],
                "baseline_published": len(baseline_cells.get(cell, {}).get("published") or []),
                "unstable": unstable,
            }
            report["cells"][cell] = entry
            (report["unstable_cells"] if unstable else report["stable_cells"]).append(cell)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print(f"rounds: {', '.join(report['rounds'])}\n")
    print(f"{'cell':<14}{'base':>5}{'published/round':>18}{'merged':>9}  EIS 命中（机械代理）")
    for cell, e in report["cells"].items():
        pub = ",".join(str(p) for p in e["published"])
        mark = " ⚠" if e["unstable"] else "  "
        inter = ",".join(x.replace("EIS-", "") for x in e["eis_intersection"]) or "-"
        union = ",".join(x.replace("EIS-", "") for x in e["eis_union"]) or "-"
        both = inter if inter == union else f"{inter}  (并集 {union})"
        print(f"{cell:<14}{e['baseline_published']:>5}{pub:>16}{mark}"
              f"{','.join(str(m) for m in e['merged']):>9}  {both}")
    print(f"\n不稳定的格（轮次间不一致）: {len(report['unstable_cells'])} / {len(report['cells'])}")
    for c in report["unstable_cells"]:
        print(f"  ⚠ {c}: published {report['cells'][c]['published']}")
    print("\n⚠ EIS 映射是机械代理（predicate + 元素重叠），不能替代 HIT_CRITERION.md §5 的人工判定。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
