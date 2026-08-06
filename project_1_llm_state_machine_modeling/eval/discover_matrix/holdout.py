"""The hold-out pair set: chosen by an executable rule, before any of them is run.

Why this file exists
--------------------
Eighteen generations of the discover matrix were reported on four cells -- 0000, 0006, 0029,
0050 -- and every gate, prompt sentence and worked example in the pipeline was written while
looking at those four. Six rounds of leak audit each found residue in a form the previous round
had not searched for, ending with a class that carries no ledger identifier at all: the NL
sentence shape, the predicate combination, the expected truth value and the answer's cardinality
are together enough to hand over the answer. Text audit cannot bound that, because "the prompt
contains no answer" is a negative claim and every round searched only the forms already known.

So the coverage number from those four cells cannot separate discovery capability from
co-evolution, however clean the prompt looks. This module fixes the only construction that can:
pairs that were never involved in authoring anything, frozen before they are run.

The selection rule, in full
--------------------------
1. **Never named.** The pair id does not appear in the feedback-loop pipeline source, its tests,
   or the body of any commit in the repository. `pair 0050`, `0050-claude`,
   `feedback_final_0050` and `EIS-0050-` all count as naming it.
2. **Never run.** No directory under `runs/` mentions the pair.
3. **Judgeable.** Only ledger records with `in_scope: true` and
   `expressible_with_closed_vocabulary: true` count. A record outside paper1's `M = (S, E, V,
   Tr, A)` boundary, or one the closed predicate vocabulary cannot state, is unfindable by
   construction -- counting it would report a boundary as a capability gap.
4. **Non-trivial denominator.** The pair must carry at least two judgeable records.
5. **Layer-stratified, then ascending.** Walk candidates in ascending pair id. Admit a pair if
   it introduces a `layer` not yet covered, until all four layers are present; then keep
   admitting in ascending id order until `HOLDOUT_SIZE` pairs are held.

Every step is a property of the ledger and the repository, never of a result. Nothing here can
be tuned after seeing an outcome, which is the whole point: rule 5 is arbitrary on purpose, and
arbitrary-but-fixed is what makes it a hold-out rather than a selection.

What this does NOT establish
----------------------------
The ledger records for these pairs were written by the same person who wrote the rules. They
were written from the artifacts, not from pipeline output, and no pipeline run has ever seen
these pairs -- but "the ledger author is independent of the rule author" is false here and
cannot be made true by any construction available in this repository. What the hold-out removes
is the loop through *observed pipeline behaviour*; it does not remove the shared author.

Usage
-----
    python -m holdout --freeze     # writes holdout.json, refusing if it already exists
    python -m holdout --verify     # recomputes and diffs against the frozen file

`--verify` is what the test calls. It fails if a held-out pair has since been named anywhere,
which is the guard that keeps a future commit from silently burning the hold-out.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LEDGER = HERE / "manual_review" / "expected_issue_set.json"
FROZEN = HERE / "holdout.json"
PIPELINE = REPO / "project_1_llm_state_machine_modeling" / "paper_stm_repair" / "pipeline" / "feedback_loop"
RUNS = REPO / "runs"

#: Six pairs against four cells: 18 cell-rounds per generation against the previous 12. Chosen
#: from the round budget, not from the candidates -- see rule 5.
HOLDOUT_SIZE = 6

LAYERS = ("wellformedness", "nl_named", "over_specification", "nl_contradiction")


def _naming(pair: str) -> re.Pattern[str]:
    """Every spelling by which the corpus refers to a pair."""
    return re.compile(
        rf"(pair[ _-]?{pair}\b|{pair}-claude|{pair}-gpt|feedback_final_{pair}\b|EIS-{pair}-)"
    )


def _source_and_test_text() -> str:
    parts = []
    for root in (PIPELINE / "src", PIPELINE / "tests"):
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.py")):
            parts.append(path.read_text(errors="ignore"))
    return "\n".join(parts)


def _commit_text() -> str:
    done = subprocess.run(
        ["git", "log", "--format=%s%n%b", "--all"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    if done.returncode != 0:  # pragma: no cover
        raise RuntimeError(f"git log failed: {done.stderr.strip()}")
    return done.stdout


def _run_dir_text() -> str:
    if not RUNS.is_dir():
        return ""
    return "\n".join(str(p) for p in RUNS.rglob("*") if p.is_dir())


def _judgeable(record: dict) -> bool:
    return (
        record.get("in_scope") is True
        and record.get("expressible_with_closed_vocabulary") is True
    )


def compute() -> dict:
    ledger = json.loads(LEDGER.read_text())
    records = ledger["records"]

    def pair_of(record: dict) -> str:
        return str(record["pair"])[-4:]

    all_pairs = sorted({pair_of(r) for r in records})
    source, commits, run_dirs = _source_and_test_text(), _commit_text(), _run_dir_text()

    named, run = {}, {}
    for pair in all_pairs:
        pattern = _naming(pair)
        where = []
        if pattern.search(source):
            where.append("pipeline_source_or_tests")
        if pattern.search(commits):
            where.append("commit_body")
        named[pair] = where
        run[pair] = bool(re.search(rf"{pair}-(claude|gpt)", run_dirs))

    judgeable: dict[str, list[dict]] = collections.defaultdict(list)
    for record in records:
        if _judgeable(record):
            judgeable[pair_of(record)].append(record)

    candidates = [
        pair
        for pair in all_pairs
        if not named[pair] and not run[pair] and len(judgeable[pair]) >= 2
    ]

    held: list[str] = []
    covered: set[str] = set()
    for pair in candidates:  # rule 5, phase 1: cover every layer
        layers = {r["layer"] for r in judgeable[pair]}
        if layers - covered:
            held.append(pair)
            covered |= layers
        if covered >= set(LAYERS):
            break
    for pair in candidates:  # rule 5, phase 2: ascending fill
        if len(held) >= HOLDOUT_SIZE:
            break
        if pair not in held:
            held.append(pair)
    held.sort()

    def summarise(pair: str) -> dict:
        rows = judgeable[pair]
        return {
            "pair": pair,
            "judgeable_records": len(rows),
            "record_ids": sorted(r["id"] for r in rows),
            "by_layer": dict(collections.Counter(r["layer"] for r in rows)),
            "by_direction": dict(collections.Counter(r.get("direction", "?") for r in rows)),
        }

    excluded_here = [
        r["id"] for r in records if pair_of(r) in held and not _judgeable(r)
    ]
    return {
        "schema": "DiscoverHoldout/v1",
        "what_this_is": (
            "Ledger pairs that were never involved in authoring any rule, prompt sentence or "
            "worked example, frozen before any of them was run. Reported coverage should be "
            "read from these; the four historical cells measure method-sample co-evolution."
        ),
        "selection_rule": [
            "never named in pipeline source, pipeline tests, or any commit body",
            "never run (no runs/ directory mentions the pair)",
            "records counted only when in_scope and expressible_with_closed_vocabulary",
            "at least two such records",
            f"layer-stratified over {list(LAYERS)}, then ascending pair id, to {HOLDOUT_SIZE}",
        ],
        "tainted_pairs": {p: w for p, w in sorted(named.items()) if w},
        "run_pairs": sorted(p for p, r in run.items() if r),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "holdout": held,
        "holdout_detail": [summarise(p) for p in held],
        "holdout_judgeable_total": sum(len(judgeable[p]) for p in held),
        "holdout_layer_coverage": dict(
            collections.Counter(
                r["layer"] for p in held for r in judgeable[p]
            )
        ),
        "excluded_records_inside_holdout_pairs": excluded_here,
        "caveat": (
            "The ledger for these pairs shares an author with the rules. The hold-out removes "
            "the loop through observed pipeline behaviour, not the shared author."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--freeze", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args(argv)
    fresh = compute()

    if args.freeze:
        if FROZEN.exists():
            print(f"refusing to overwrite {FROZEN.name}; a hold-out is frozen once", file=sys.stderr)
            return 2
        FROZEN.write_text(json.dumps(fresh, ensure_ascii=False, indent=1) + "\n")
        print(f"frozen -> {FROZEN}")

    if args.verify:
        if not FROZEN.exists():
            print(f"{FROZEN.name} missing; run --freeze first", file=sys.stderr)
            return 2
        frozen = json.loads(FROZEN.read_text())
        problems = []
        if frozen["holdout"] != fresh["holdout"]:
            problems.append(f"holdout drifted: frozen {frozen['holdout']} vs now {fresh['holdout']}")
        burned = sorted(set(frozen["holdout"]) & set(fresh["tainted_pairs"]))
        if burned:
            problems.append(
                f"held-out pairs are now named in source or commits: {burned}. "
                "A hold-out that has been written about is no longer one."
            )
        for problem in problems:
            print(f"FAIL {problem}", file=sys.stderr)
        if problems:
            return 1
        print(f"ok: {frozen['holdout']} still clean, {frozen['holdout_judgeable_total']} records")

    if not (args.freeze or args.verify):
        print(json.dumps(fresh, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
