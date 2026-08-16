"""Fold the manual review of the lexical strata back in, producing a point value.

`stratify_candidates.py` classifies by phrase, which makes `nl_named` an upper bound: the
regex fires on any reason that cites the NL, and citing the NL is not the same as the NL
having *named the element that is missing*. Reviewers then went through those rows one at
a time against the NL text, and `extra` rows through a harm test. This script merges those
two passes over the lexical baseline.

Inputs, all produced by review passes and all optional -- a missing file leaves its rows
at the lexical verdict, so the number degrades to the bound rather than silently changing:

  /tmp/nlcheck/result{1..4}.json   per-batch review of the `nl_named` rows
  /tmp/nlcheck/extra_harm.json     harm test over the `extra` rows

Precedence: manual over lexical, always. The lexical pass exists to make the manual pass
finite, not to overrule it.

Usage: merge_manual_stratification.py [--json <out>] [--md <out>]
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from collections import Counter, defaultdict

# ⚠️ 2026-08-17 归档：本文件原在 `discover_matrix/` 顶层，`HERE` 即指那一层；
# ⛔ 归档到 `archive/r10_ledger_v1_and_v46/scripts/` 后深度多了两层，`HERE / "manual_review"`
# 会解析到不存在的 `scripts/manual_review`。⭐ 故改为指向归档根（它保留了原 discover_matrix
# 的内部布局：manual_review/ · v46/ · verdicts/ …），⛔ 不数层数、按目录名锚定。
_F = pathlib.Path(__file__).resolve()
HERE = next(p for p in _F.parents if p.name == "r10_ledger_v1_and_v46")
NLCHECK = pathlib.Path("/tmp/nlcheck")

#: Which strata a finding may be admitted from. `over_specification` is admissible only
#: when the harm test passed -- being invented by the model makes it attributable, not
#: automatically a defect.
ADMISSIBLE = {"wellformedness", "nl_contradiction", "nl_named", "over_specification"}

#: The review pass may move a row to any of these; anything else is a protocol error and
#: is reported rather than absorbed.
REVIEW_VERDICTS = {
    "confirmed": None,  # stay where the lexical pass put it
    "reference_only": "reference_only",
    "wellformedness": "wellformedness",
    "nl_contradiction": "nl_contradiction",
    "nl_named": "nl_named",
    "over_specification": "over_specification",
    "uncertain_stratum": "uncertain_stratum",
}
HARM_VERDICTS = {"harmful", "benign", "uncertain"}


def load_baseline() -> list[dict]:
    from stratify_candidates import classify

    rows = []
    for path in sorted((HERE / "manual_review").glob("*-review.json")):
        review = json.loads(path.read_text())
        cross = review.get("cross_reference") or {}
        for index, diff in enumerate(review.get("diffs") or []):
            if diff.get("verdict") not in {"problem", "extra"} or diff.get("out_of_scope"):
                continue
            stratum, trigger = classify(diff.get("reason") or "", diff["verdict"])
            rows.append({
                "case": review["case"], "group": cross.get("group"), "llm": cross.get("llm"),
                "diff_index": index, "verdict": diff["verdict"],
                "lexical_stratum": stratum, "lexical_trigger": trigger,
                "stratum": stratum, "decided_by": "lexical",
                "assertable": (diff.get("assertable") or "").strip(),
                "case_has_ledger_e1": bool((cross.get("ledger") or {}).get("e1_ids")),
                "reason_head": (diff.get("reason") or "")[:120],
            })
    return rows


def apply_batch5(rows: list[dict], complaints: list[str]) -> int:
    """Batch 5 covers what the other four did not: the rows the lexical pass could not
    classify at all, the rows it excluded, and a spot check of the two strata nobody
    reviewed in full. Without it the count is not a point value, because 12 rows would
    still be sitting on a machine verdict nobody looked at."""
    path = NLCHECK / "result5.json"
    if not path.exists():
        complaints.append(
            "批 5 缺失（result5.json）——unclassified 与 reference_only 共 12 条从未经人工判定，"
            "且 wellformedness / nl_contradiction 两层未抽验"
        )
        return 0
    payload = json.loads(path.read_text())
    index = {(r["case"], r["diff_index"]): r for r in rows}
    applied = 0
    for item in payload.get("part_a") or []:
        key = (item["case"], item["diff_index"])
        row = index.get(key)
        if row is None:
            complaints.append(f"批 5: {key} 不在基线里")
            continue
        verdict = item.get("verdict")
        if verdict not in REVIEW_VERDICTS or verdict == "confirmed":
            complaints.append(f"批 5: {key} 未知归层 {verdict!r}")
            continue
        row["stratum"] = REVIEW_VERDICTS[verdict]
        row["review_verdict"] = verdict
        row["nl_evidence"] = item.get("nl_evidence") or ""
        row["review_note"] = item.get("note") or ""
        row["decided_by"] = "batch5_reclassify"
        applied += 1
    # A spot check that disagreed is a correction, so apply it; one that agreed is
    # evidence about the stratum as a whole, recorded on the row for traceability.
    for item in payload.get("part_b_spotcheck") or []:
        key = (item["case"], item["diff_index"])
        row = index.get(key)
        if row is None:
            complaints.append(f"批 5 抽验: {key} 不在基线里")
            continue
        row["spotchecked"] = True
        row["spotcheck_agreed"] = bool(item.get("agree"))
        if not item.get("agree"):
            target = item.get("correct_stratum")
            if target not in {v for v in REVIEW_VERDICTS.values() if v}:
                complaints.append(f"批 5 抽验: {key} 给出未知的 correct_stratum {target!r}")
                continue
            row["stratum"] = target
            row["review_note"] = item.get("note") or ""
            row["decided_by"] = "batch5_spotcheck"
            applied += 1
    return applied


def apply_nl_review(rows: list[dict], complaints: list[str]) -> int:
    index = {(r["case"], r["diff_index"]): r for r in rows}
    applied = 0
    for batch in range(1, 5):
        path = NLCHECK / f"result{batch}.json"
        if not path.exists():
            complaints.append(f"批 {batch} 的复核结果缺失（{path.name}）——该批仍停在词法上界")
            continue
        payload = json.loads(path.read_text())
        for item in payload.get("items") or []:
            key = (item["case"], item["diff_index"])
            row = index.get(key)
            if row is None:
                complaints.append(f"批 {batch}: {key} 不在基线里（可能已被 extra 短路移层）")
                continue
            verdict = item.get("verdict")
            if verdict not in REVIEW_VERDICTS:
                complaints.append(f"批 {batch}: {key} 未知复核判定 {verdict!r}")
                continue
            target = REVIEW_VERDICTS[verdict]
            # An `extra` row is decided by the harm test, not by the NL-naming review; if a
            # batch touched one, keep the harm test authoritative and say so.
            if row["verdict"] == "extra":
                complaints.append(
                    f"批 {batch}: {key} 是 extra 档，其归属由有害性判定决定，已忽略本条 NL 复核"
                )
                continue
            row["review_verdict"] = verdict
            row["nl_evidence"] = item.get("nl_evidence") or ""
            row["review_note"] = item.get("note") or ""
            if target is not None:
                row["stratum"] = target
            row["decided_by"] = "nl_review"
            applied += 1
    return applied


def apply_harm(rows: list[dict], complaints: list[str]) -> int:
    path = NLCHECK / "extra_harm.json"
    if not path.exists():
        complaints.append(
            "extra 有害性判定缺失（extra_harm.json）——31 条 extra 仍按可归因即可入计，"
            "这是上界"
        )
        return 0
    payload = json.loads(path.read_text())
    index = {(r["case"], r["diff_index"]): r for r in rows}
    applied = 0
    for item in payload.get("items") or []:
        key = (item["case"], item["diff_index"])
        row = index.get(key)
        if row is None:
            complaints.append(f"有害性判定: {key} 不在基线里")
            continue
        if row["verdict"] != "extra":
            complaints.append(f"有害性判定: {key} 不是 extra 档，已忽略")
            continue
        verdict = item.get("verdict")
        if verdict not in HARM_VERDICTS:
            complaints.append(f"有害性判定: {key} 未知判定 {verdict!r}")
            continue
        row["harm"] = verdict
        row["harm_consequence"] = item.get("consequence") or ""
        row["harm_assertion"] = item.get("assertion") or ""
        row["harm_verified"] = item.get("verified") or ""
        row["decided_by"] = "harm_test"
        if verdict == "benign":
            row["stratum"] = "over_specification_benign"
        elif verdict == "uncertain":
            row["stratum"] = "uncertain_stratum"
        applied += 1

    # A harmful `extra` whose consequence is already booked by a `problem` in the same pair
    # must not be counted twice. `0056`#3 binds *identically* to `0056`#1, so admitting
    # both would report one defect as two expected issues -- and inflating the denominator
    # is the failure mode this whole stratification exists to avoid.
    for entry in payload.get("harmful_but_duplicate_of_an_existing_problem") or []:
        m = re.match(r"(\d{4})#(\d+)", str(entry))
        if not m:
            complaints.append(f"有害性判定: 无法解析的重复标记 {entry!r}")
            continue
        row = index.get((m.group(1), int(m.group(2))))
        if row is None:
            complaints.append(f"有害性判定: 重复标记 {entry!r} 不在基线里")
            continue
        row["stratum"] = "over_specification_duplicate"
        row["duplicate_of"] = str(entry)
        row["decided_by"] = "harm_test_dedup"
    return applied


def apply_parent_rulings(rows: list[dict], complaints: list[str]) -> int:
    """Parent-session rulings, for the cases where two review passes disagreed or a
    reported measurement did not reproduce. Kept in its own file with per-ruling evidence
    so that overruling a reviewer is itself auditable rather than an unexplained edit to
    the numbers."""
    path = NLCHECK / "parent_rulings.json"
    if not path.exists():
        return 0
    payload = json.loads(path.read_text())
    index = {(r["case"], r["diff_index"]): r for r in rows}
    applied = 0
    for ruling in payload.get("rulings") or []:
        key = (ruling["case"], ruling["diff_index"])
        row = index.get(key)
        if row is None:
            complaints.append(f"主裁定: {key} 不在基线里")
            continue
        scope = (ruling.get("ruling") or {}).get("out_of_scope")
        stratum = (ruling.get("ruling") or {}).get("stratum")
        if scope:
            # Moving a row out of scope removes it from `problems_in_scope` entirely, so it
            # leaves the stratification rather than changing layer inside it.
            row["stratum"] = f"out_of_scope_{scope}"
            row["parent_ruling"] = ruling
            row["decided_by"] = "parent_ruling"
            applied += 1
        elif stratum:
            # A ruling that moves the row to a different layer *within* scope -- e.g. parking
            # a row whose own review_note says the call was not made.
            row["stratum"] = stratum
            row["parent_ruling"] = ruling
            row["decided_by"] = "parent_ruling"
            applied += 1
        # A ruling may also replace the assertion without moving the layer: the reviewer's
        # original basis can be withdrawn and a stronger one substituted while the finding
        # itself stands. `0050`#4 is exactly that -- same layer, different evidence.
        new_assert = (ruling.get("ruling") or {}).get("assertable")
        if new_assert:
            row["assertable_superseded"] = row.get("assertable")
            row["assertable"] = new_assert
            row["parent_ruling"] = ruling
            row["decided_by"] = "parent_ruling"
    return applied


def check_duplicate_markers(rows: list[dict], complaints: list[str]) -> None:
    """A row carrying `duplicate_of` must not also sit in an admissible layer.

    `0056`#3 did both: the harm test deduped it against `0056`#1 ("identical binding") while
    a later pass moved it back to `over_specification`, leaving the row simultaneously
    flagged as a duplicate and counted as an admissible finding. That is a double-count of
    one defect, and nothing in the pipeline objected -- so it is checked here."""
    for row in rows:
        if row.get("duplicate_of") and row["stratum"] in ADMISSIBLE:
            complaints.append(
                f"重复标记冲突: {row['case']}#{row['diff_index']} 带 duplicate_of "
                f"（{row['duplicate_of']}）却落在可入层 {row['stratum']}——"
                f"同一缺陷会被计两次，须显式裁定")


def summarise(rows: list[dict]) -> dict:
    by = Counter(r["stratum"] for r in rows)
    adm = [r for r in rows if r["stratum"] in ADMISSIBLE]
    # A row still on the lexical verdict is only acceptable if its stratum was spot
    # checked -- `wellformedness` and `nl_contradiction` key on phrases like 死端 /
    # 吸收 / 方向写反, which are far less ambiguous than `nl_named`'s "mentions the NL".
    # Rows in a stratum nobody sampled are genuinely unreviewed and block the claim.
    sampled = {r["stratum"] for r in rows if r.get("spotchecked")}
    unreviewed = [r for r in rows
                  if r["decided_by"] == "lexical" and r["stratum"] not in sampled]
    # `uncertain_stratum` does not block the point-value claim: those rows *were* reviewed
    # and are parked for a stated reason (their assertion returns None, so no positive
    # judgement is available on the current predicate surface). They are excluded from the
    # admissible count and reported separately. What blocks the claim is a row whose
    # stratum nobody ever looked at -- that is an unknown, not a known exclusion.
    pending = unreviewed
    return {
        "in_scope": len(rows),
        "by_stratum": dict(by),
        "admissible": len(adm),
        "admissible_cases": len({r["case"] for r in adm}),
        "admissible_on_cases_without_ledger_e1": sum(
            1 for r in adm if not r["case_has_ledger_e1"]),
        "still_at_lexical_bound": sum(1 for r in rows if r["decided_by"] == "lexical"),
        "lexical_but_stratum_sampled": sum(
            1 for r in rows if r["decided_by"] == "lexical" and r["stratum"] in sampled),
        "unreviewed": len(unreviewed),
        "spotchecked": sum(1 for r in rows if r.get("spotchecked")),
        "spotcheck_disagreed": sum(
            1 for r in rows if r.get("spotchecked") and not r.get("spotcheck_agreed")),
        "sampled_strata": sorted(sampled),
        "uncertain": by.get("uncertain_stratum", 0),
        "is_point_value": not pending,
    }


def main() -> int:
    sys.path.insert(0, str(HERE))
    complaints: list[str] = []
    rows = load_baseline()
    n_nl = apply_nl_review(rows, complaints)
    n_harm = apply_harm(rows, complaints)
    n_b5 = apply_batch5(rows, complaints)
    n_pr = apply_parent_rulings(rows, complaints)
    check_duplicate_markers(rows, complaints)
    s = summarise(rows)

    print(f"基线 {s['in_scope']} 条计入问题；NL 复核落地 {n_nl} 条，"
          f"有害性判定落地 {n_harm} 条，批 5 归层/抽验落地 {n_b5} 条，"
          f"主裁定 {n_pr} 条\n")
    print("| 层 | 条数 | 可入 E1 |")
    print("| --- | ---: | :-: |")
    for name, n in sorted(s["by_stratum"].items(), key=lambda kv: -kv[1]):
        print(f"| `{name}` | {n} | {'✓' if name in ADMISSIBLE else '✗'} |")
    verdict = "**点值**" if s["is_point_value"] else "**仍是上界**"
    print(f"\n{verdict}：可入 E1 = **{s['admissible']}** / {s['in_scope']}"
          f"（分布在 {s['admissible_cases']} 个 case）")
    if s["uncertain"]:
        print(f"另有 **{s['uncertain']}** 条已审阅但搁置（断言在当前谓词面上返回 None、"
              f"给不出正面判定），已排除在可入之外")
    print(f"其中落在台帐无 E1 的 case 上：**{s['admissible_on_cases_without_ledger_e1']}** 条")
    if not s["is_point_value"]:
        print(f"⚠ 未收敛：{s['unreviewed']} 条所在层从未被审视，"
              f"{s['uncertain']} 条判定困难")
    else:
        print(f"（其中 {s['lexical_but_stratum_sampled']} 条仍是词法判定，但其所在层已抽验 "
              f"{s['spotchecked']} 条、纠正 {s['spotcheck_disagreed']} 条）")

    print("\n### 按 NL 组")
    per: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        per[r["group"]]["total"] += 1
        if r["stratum"] in ADMISSIBLE:
            per[r["group"]]["adm"] += 1
    print("| NL 组 | 可入 | 计入问题 |")
    print("| --- | ---: | ---: |")
    for g in sorted(per):
        print(f"| {g} | **{per[g]['adm']}** | {per[g]['total']} |")

    if complaints:
        print(f"\n### 校验（{len(complaints)} 条）\n")
        for c in complaints:
            print(f"- {c}")

    if "--json" in sys.argv:
        dest = pathlib.Path(sys.argv[sys.argv.index("--json") + 1])
        dest.write_text(json.dumps({
            "what_this_is": (
                "把 nl_named 的逐条 NL 复核与 extra 的有害性判定，合并到词法分层基线上，"
                "得到可入 expected issue 的点值。人工判定优先于词法判定。"
            ),
            "admissible_strata": sorted(ADMISSIBLE),
            "summary": s,
            "complaints": complaints,
            "rows": rows,
        }, ensure_ascii=False, indent=1) + "\n")
        print(f"\n已写 {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
