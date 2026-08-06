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
2. **Never run, and never published as run.** No directory under `runs/` mentions the pair, and
   the pair is absent from `published_run_ledger.json` -- the frozen record of pairs whose
   Discover behaviour was already observed and written up elsewhere (PR #158 §五 and its gist).
   The first version of this rule checked only `runs/` directory names, and two pairs whose
   results had been published in a PR comment passed it.
3. **NL group disjoint from the tuned cells.** The pair's `group` is not one of `TUNED_GROUPS`.
   Same group means the same requirement text and the same reference model, so a rule written
   against one member acts on every member -- something a pair-id spelling check cannot see.
4. **Judgeable.** Only ledger records with `in_scope: true` and
   `expressible_with_closed_vocabulary: true` count. A record outside paper1's `M = (S, E, V,
   Tr, A)` boundary, or one the closed predicate vocabulary cannot state, is unfindable by
   construction -- counting it would report a boundary as a capability gap.
5. **Non-trivial denominator.** The pair must carry at least two judgeable records.
6. **Layer-stratified, then ascending, group-capped.** Walk candidates in ascending pair id.
   Admit a pair if it introduces a `layer` not yet covered, until all four layers are present;
   then keep admitting in ascending id order, at most `MAX_PER_GROUP` per NL group, until
   `HOLDOUT_SIZE` pairs are held.

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
    python -m holdout --verify     # checks the frozen set is still uncontaminated

`--verify` deliberately does NOT recompute the candidate pool. It checks only the two properties
that must keep holding: rule 1 (still unnamed) and rule 4 (ledger denominator unchanged). Running
the hold-out is what rule 2 forbids *before* freezing, so recomputing it afterwards would make
the check fail on its first legitimate use -- and fail with the same message as a real burn.
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LEDGER = HERE / "manual_review" / "expected_issue_set.json"
FROZEN = HERE / "holdout.json"
#: 已被运行且结果已公开的 pair。规则 2 查这里而不是只查 runs/ 的目录名。
PUBLISHED_RUNS = HERE / "published_run_ledger.json"
PIPELINE = REPO / "project_1_llm_state_machine_modeling" / "paper_stm_repair" / "pipeline" / "feedback_loop"
RUNS = REPO / "runs"

#: Six pairs against four cells: 18 cell-rounds per generation against the previous 12. Chosen
#: from the round budget, not from the candidates -- see rule 5.
HOLDOUT_SIZE = 10

#: 四个调优格所属的 NL group。同 group 意味着同一份需求文本与同一份参考模型，
#: 因此针对某个调优格写下的规则天然作用于同 group 的其它 pair——按 pair id 拼写
#: 判污染完全看不到这一层。实测：0010 与 0000/0050 同属 NL08，0009 与 0029 同属 NL05。
TUNED_GROUPS = ("NL03", "NL05", "NL08")

#: 同一 group 最多取几个，避免某一族的句法特性主导整个 hold-out。
MAX_PER_GROUP = 3

LAYERS = ("wellformedness", "nl_named", "over_specification", "nl_contradiction")


def _naming_in_prose(pair: str) -> re.Pattern[str]:
    """Any bare mention of the four-digit id. The only matcher; there is no second one.

    The enumerating form above produced a false negative on every held-out pair: commit bodies
    write `0018/0038`, `0018(9)、0038(4)`, and plain `0048`, none of which match `pair 0018` or
    `0018-claude`. One commit body even states outright that its rule was written after watching
    two held-out pairs fail -- the exact motive taint the hold-out exists to exclude -- and the
    detector reported the set clean.

    This is the fourth recurrence of one mistake: defining detection as a spelling enumeration,
    so the next spelling escapes. Earlier rounds went gate -> predicate catalogue, element name
    -> prose description, static prompt -> runtime feedback. The fix is to stop enumerating:
    a bare four-digit id has no competing meaning, so match it and let a human adjudicate the
    rare incidental hit.

    ⚠️ Recurrences five and six were the *same function surviving in half the call sites*.
    Round five: `compute()` was moved to this matcher and `--verify` -- the gate -- was left on
    the enumerating one. Round six: `--verify`'s commit-body branch was moved and its
    source-and-test branch was left, on the argument that source text is full of four-digit
    numbers which are not pair ids. That argument was never measured, and it is false. Across
    all sixty ids in `src/` and `tests/`:

        bare id                269 hits, 18 ids
        enumerating form                  6 ids
        reachable only by the bare id     139 hits, 17 ids -- and *zero* are false positives

    The feared spellings cannot match: `\b` fails inside `L000-000018-` and `tr_0043` because
    a digit and an underscore are word characters. Two of the 139 are live rule-1 violations
    (`0019, 0043 and 0053` in the attribution branch; `Pair 0047` -- capitalised, which is all
    it took -- in the coactivity gate). One matcher, therefore, and no ambiguity argument
    without a measurement behind it.
    """
    return re.compile(rf"\b{pair}\b")


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


def _run_pairs_from_dirs() -> set[str]:
    """Pair ids that appear as a *cell directory* under `runs/`, e.g. `v19run1/0007-claude`.

    Matching pair ids anywhere in the path text is what an earlier version did, with
    `rf"{pair}-\\w+"`. Record files are named `L000-000005-requirement-...`, so every four-digit
    id matched some record sequence number in some unrelated cell, the candidate pool came back
    empty, and `--freeze` wrote an empty hold-out without complaint. Only the cell directory's
    own name identifies which pair was run.
    """
    if not RUNS.is_dir():
        return set()
    found = set()
    # Walk at any depth -- cell dirs sit at runs/<campaign>/<matrix>/<round>/<pair>-<profile>,
    # and a fixed-depth glob missed the aborted v19 rounds entirely, leaving four pairs in the
    # hold-out whose output had already been read. Prune `records/` so this stays cheap.
    for root, dirs, _ in os.walk(RUNS):
        dirs[:] = [d for d in dirs if d not in ("records", "loops")]
        for name in dirs:
            head, _, rest = name.partition("-")
            if rest and len(head) == 4 and head.isdigit():
                found.add(head)
    return found


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
    source, commits = _source_and_test_text(), _commit_text()
    ran_dirs = _run_pairs_from_dirs()

    published = json.loads(PUBLISHED_RUNS.read_text())
    ran_published = set(published["ran_and_published"])
    group_of = {}
    for record in records:
        group_of[pair_of(record)] = record.get("group")

    named, run, flagged = {}, {}, {}
    for pair in all_pairs:
        pattern = _naming_in_prose(pair)
        where = []
        if pattern.search(source):
            where.append("pipeline_source_or_tests")
        # Bare four-digit mentions in commit bodies are *flagged*, not auto-excluded.
        #
        # Enumerating spellings gave false negatives on all seven held-out pairs. Matching the
        # bare id gives false positives instead -- 40 of 48 pairs appear in some commit body,
        # mostly inside ledger statistics like "7 个 case 连候选都未记录（0003 0012 … 0052）",
        # which is not rule authoring. Auto-excluding on either rule is wrong; the pool goes to
        # zero on one and stays contaminated on the other.
        #
        # What actually decides taint is motive, not mention (CLAUDE.md §3.5.-1 手段 1): was a
        # rule written *because* this pair failed? That is a human judgement over the commit
        # body, so this records the evidence and refuses to pretend it is automatic.
        prose_hits = _naming_in_prose(pair).findall(commits)
        if prose_hits:
            flagged[pair] = len(prose_hits)
        named[pair] = where
        # 目录名 + 已公开运行台账。前者只覆盖本仓库 runs/，后者覆盖 PR/gist。
        run[pair] = pair in ran_dirs or pair in ran_published

    judgeable: dict[str, list[dict]] = collections.defaultdict(list)
    for record in records:
        if _judgeable(record):
            judgeable[pair_of(record)].append(record)

    candidates = [
        pair
        for pair in all_pairs
        if not named[pair]
        and not run[pair]
        and group_of.get(pair) not in TUNED_GROUPS
        and len(judgeable[pair]) >= 2
    ]

    held: list[str] = []
    covered: set[str] = set()
    per_group: collections.Counter = collections.Counter()

    def admit(pair: str) -> None:
        held.append(pair)
        covered.update(r["layer"] for r in judgeable[pair])
        per_group[group_of.get(pair)] += 1

    for pair in candidates:  # rule 6, phase 1: cover every layer
        if {r["layer"] for r in judgeable[pair]} - covered:
            admit(pair)
        if covered >= set(LAYERS):
            break
    for pair in candidates:  # rule 6, phase 2: ascending fill, group-capped
        if len(held) >= HOLDOUT_SIZE:
            break
        if pair in held or per_group[group_of.get(pair)] >= MAX_PER_GROUP:
            continue
        admit(pair)
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
        # Mentioned by bare id in some commit body. NOT auto-excluded -- see `_naming_in_prose`.
        # Each needs a human motive judgement before it can be used or dismissed.
        "flagged_for_motive_adjudication": dict(sorted(flagged.items())),
        "run_pairs": sorted(p for p, r in run.items() if r),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "holdout": held,
        "holdout_groups": {p: group_of.get(p) for p in held},
        "excluded_tuned_groups": list(TUNED_GROUPS),
        "max_per_group": MAX_PER_GROUP,
        "frozen_at_commit": subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True
        ).stdout.strip(),
        "previously_run_and_published": sorted(ran_published),
        "run_seen_in_runs_dir": sorted(ran_dirs),
        "holdout_detail": [summarise(p) for p in held],
        "holdout_judgeable_total": sum(len(judgeable[p]) for p in held),
        "holdout_layer_coverage": dict(
            collections.Counter(
                r["layer"] for p in held for r in judgeable[p]
            )
        ),
        "excluded_records_inside_holdout_pairs": excluded_here,
        # 分层 @k 需要每层足够条目；不足时必须显式声明该层不报，而不是用 2~3 条撑出一个百分比。
        "layers_reportable_at_k": {
            layer: (
                sum(1 for p in held for r in judgeable[p] if r["layer"] == layer) >= 4
            )
            for layer in LAYERS
        },
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
        # 一个空的或过小的 hold-out 写盘后与一个合法的 hold-out 在形状上无从区分，
        # 而它会让此后每个 @k 都算在一个空分母上。规则配错必须拒绝，不能静默产出。
        if len(fresh["holdout"]) < 5 or fresh["holdout_judgeable_total"] < 20:
            print(
                f"refusing to freeze an undersized set: {len(fresh['holdout'])} pairs / "
                f"{fresh['holdout_judgeable_total']} records (need >=5 pairs and >=20 records). "
                f"candidate pool was {fresh['candidate_count']}; check the exclusion rules.",
                file=sys.stderr,
            )
            return 2
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
        # Reconcile against what is *recorded* as burned rather than re-deciding it. Once a
        # pair is burned, the report has to explain why -- and explaining why means writing
        # its id down, which trips a spelling detector forever after. Under the old check
        # there was no way to record a burn without leaving the suite permanently red, so
        # the red stopped meaning "something new happened".
        burned = frozen.get("burned") or {}
        reportable = frozen.get("reportable_holdout") or frozen["holdout"]
        held = list(reportable)
        # 只校验「冻结集是否仍然未被污染」，不重算候选池。
        #
        # 上一版把 `frozen["holdout"] == compute()["holdout"]` 当作校验，于是第一次正常使用
        # 就把它摧毁了：hold-out 一旦跑过，规则 2（未跑过）就把这些 pair 自己剔除，重算结果
        # 必然是另一组，测试永久变红——而「被点名烧毁」与「正常跑过」产出同一条失败信息。
        # 这正是 `ec9c4dfe` 自己写下的判据「配错必须无法与成功区分开来，否则它就是缺陷」的
        # 反例。「未跑过」是冻结时刻的一次性前置条件，记录为 frozen_at_commit 即可；此后需要
        # 持续成立的只有规则 1（未被点名）与规则 3（可判定）。
        source, commits = _source_and_test_text(), _commit_text()
        problems = []
        burned_now = {}
        for pair in held:
            where = []
            # Same matcher as prose. The "ambiguous in source" argument that justified a second
            # one here measured 139 bare-id hits with zero false positives, two of them live
            # rule-1 violations the enumerating form was hiding.
            if _naming_in_prose(pair).search(source):
                where.append("pipeline_source_or_tests")
            # Bodies write `0018/0038`, `0018(9)、0038(4)`, plain `0048`; none matched the
            # enumerating form, and all four reportable pairs were named this way while
            # `--verify` reported the set clean.
            if _naming_in_prose(pair).search(commits):
                where.append("commit_body")
            if where:
                burned_now[pair] = where
        # A pair named in a commit body is not automatically burned: §3.5.-1 手段 1 says the
        # judgement is motive, not spelling. Recording that a pair is *reportable* names it too.
        # So a naming hit is reconciled against `burned_records` -- if every record of that pair
        # which a rule was designed against is recorded there, the remaining records stay
        # reportable and the hit is a notice, not a failure.
        burned_records = frozen.get("burned_records") or {}
        detail = {x["pair"]: x["record_ids"] for x in frozen.get("holdout_detail") or ()}
        # A naming hit demands an adjudication, not an automatic verdict either way. Two ways
        # to satisfy it: the records a rule was designed against are recorded in
        # `burned_records`, or the naming is recorded in `motive_adjudicated` with its reasoning
        # and a verdict. What stays a failure is a naming nobody has ruled on.
        # Per *naming site*, not per pair. The previous version asked whether any record of the
        # pair was burned -- so once one was, every later naming of that pair, whatever its
        # motive and whichever other record it targeted, passed unexamined. That is a rubber
        # stamp, and it let two real contaminations through: `0043` named in the attribution
        # branch for `EIS-0043-02`, and `0047` named in the coactivity gate for `EIS-0047-01`,
        # both waved past by burns recorded for a different record of the same pair.
        adjudicated = frozen.get("motive_adjudicated") or {}
        unaccounted = {}
        for pair, where in burned_now.items():
            covered = set()
            for record in detail.get(pair) or ():
                entry = burned_records.get(record)
                if isinstance(entry, dict):
                    covered.update(entry.get("named_at") or ())
            ruling = adjudicated.get(pair)
            if isinstance(ruling, dict) and ruling.get("verdict") and ruling.get("reasoning"):
                covered.update(ruling.get("covers") or ())
            missing = [site for site in where if site not in covered]
            if missing:
                unaccounted[pair] = missing
        if unaccounted != burned_now:
            accounted = sorted(set(burned_now) - set(unaccounted))
            if accounted:
                print(
                    f"note: every naming site accounted for at record level: {accounted}",
                    file=sys.stderr,
                )
        burned_now = unaccounted
        if burned_now:
            problems.append(
                f"held-out pairs have since been named: {burned_now}. A hold-out that has "
                "been written about is no longer one; record it under `burned` with its "
                "mechanism and evidence, move it out of `reportable_holdout`, and say so in "
                "the report. If no replacement exists, say that too."
            )
        # A pair cannot be both burned and reportable; the two lists are what the bands in
        # `metrics_at_k.py` read, so an overlap would put co-evolved cells back into the
        # capability claim without anything noticing.
        overlap = sorted(set(burned) & set(reportable))
        if overlap:
            problems.append(f"pairs are both burned and reportable: {overlap}")
        if burned:
            print(
                f"note: {len(burned)} held-out pair(s) recorded as burned "
                f"({', '.join(sorted(burned))}); capability claims use "
                f"{len(reportable)} pair(s).",
                file=sys.stderr,
            )
        ledger = json.loads(LEDGER.read_text())
        judgeable_now = collections.Counter(
            str(r["pair"])[-4:] for r in ledger["records"] if _judgeable(r)
        )
        for row in frozen["holdout_detail"]:
            if judgeable_now[row["pair"]] != row["judgeable_records"]:
                problems.append(
                    f"ledger changed for {row['pair']}: frozen {row['judgeable_records']} "
                    f"judgeable records, now {judgeable_now[row['pair']]}. The denominator "
                    "moved after freezing; report both counts or re-freeze."
                )
        for problem in problems:
            print(f"FAIL {problem}", file=sys.stderr)
        if problems:
            return 1
        # Not "still unnamed" -- most of them are named, and the run above prints exactly which.
        # The success line said the opposite of what the same invocation had just reported two
        # lines earlier, so a reader skimming for the verdict got the reassuring half.
        reportable = frozen.get("reportable_records") or ()
        print(
            f"ok: every naming site accounted for; {len(reportable)} of "
            f"{frozen['holdout_judgeable_total']} records remain reportable "
            f"({', '.join(reportable) or 'none'}), frozen at "
            f"{frozen.get('frozen_at_commit', '?')[:9]}"
        )

    if not (args.freeze or args.verify):
        print(json.dumps(fresh, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
