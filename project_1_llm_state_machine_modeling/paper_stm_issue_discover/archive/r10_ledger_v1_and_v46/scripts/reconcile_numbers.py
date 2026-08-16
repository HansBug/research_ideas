"""Cross-check every headline number against every other source that reports it.

Issue #171 now carries figures from six independent passes -- the review bundle, the
stratification, the defect classification, the predicate-coverage batches, the scope audit
and the loop audit. Each was produced by a different agent from a different angle, so the
failure mode is not one wrong number but two sources quietly disagreeing while both look
authoritative. Anything published in the issue has to reconcile here first.

Each check states the invariant it enforces and where both sides come from, so a future
reader can see *why* the numbers must agree rather than just that they did.

Exit code is non-zero if any check fails, so this can gate publication.

Usage: reconcile_numbers.py [--json <out>]
"""

from __future__ import annotations

import json
import pathlib
import sys
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent
MR = HERE / "manual_review"


def load(path: pathlib.Path):
    return json.loads(path.read_text()) if path.exists() else None


def main() -> int:
    summary = load(MR / "_summary.json")
    final = load(MR / "final_stratification.json")
    defects = load(MR / "defect_classification.json")
    verified = load(MR / "predicate_coverage/verified_assertions.json")
    scope = load(MR / "loop_audit/scope.json")
    cells = load(MR / "loop_audit/cells.json")
    replay = load(MR / "loop_audit/replay_attribution.json")
    rescope = load(MR / "rescope.json")

    checks: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str) -> None:
        checks.append((name, bool(ok), detail))

    # --- the review bundle is the root of everything else -------------------------
    g = summary["grade_totals"]
    total_diffs = sum(g.values())
    check("档位合计 = 418",
          total_diffs == 418,
          f"correct {g['correct']} + similar {g['similar']} + problem {g['problem']} "
          f"+ extra {g['extra']} + uncertain {g['uncertain']} = {total_diffs}")

    oos = summary["out_of_scope_totals"]
    check("范围外标记 = 29（并发 24 + 时间 5）",
          sum(oos.values()) == 29,
          f"{oos}")

    # 154 is the pre-ruling baseline; 153 is after 0013#1 was ruled out of scope.
    base = summary["problems_in_scope_total"]
    check("计入问题基线 = 154 = problem + extra − 9",
          base == 154 == g["problem"] + g["extra"] - 9,
          f"{g['problem']} + {g['extra']} − 9 = {base}")

    rows = final["rows"]
    ruled_out = [r for r in rows if r["stratum"] == "out_of_scope_concurrency"]
    in_scope_rows = [r for r in rows if r["stratum"] != "out_of_scope_concurrency"]
    check("主裁定后 = 153",
          len(rows) == 154 and len(ruled_out) == 1 and len(in_scope_rows) == 153,
          f"分层 {len(rows)} 行 − 主裁定 {len(ruled_out)} = {len(in_scope_rows)}")

    # --- stratification vs its own summary ---------------------------------------
    adm_strata = set(final["admissible_strata"])
    adm = [r for r in rows if r["stratum"] in adm_strata]
    # 130 -> 129 -> 126. Each drop was a parent ruling with per-row evidence:
    #   0056#3  duplicate_of marker alongside an admissible stratum; its own note said
    #           the call had not been made
    #   0016#5 / 0033#3 / 0019#4  primary assertion bound to the wrong element, so its
    #           False was vacuous -- the correctly bound assertion returns True, i.e. it
    #           proves the premise (the generator declared it) rather than any consequence
    check("可入 E1 = 126，与 final_stratification 的 summary 自洽",
          len(adm) == final["summary"]["admissible"] == 126,
          f"逐行数 {len(adm)}，summary 报 {final['summary']['admissible']}")

    dup_admissible = [r for r in rows if r.get("duplicate_of") and r["stratum"] in adm_strata]
    check("没有任何带 duplicate_of 的行落在可入层（否则同一缺陷被计两次）",
          not dup_admissible,
          "0 条" if not dup_admissible else
          "、".join(f"{r['case']}#{r['diff_index']}" for r in dup_admissible))

    parked = [r for r in rows if r["stratum"] == "uncertain_stratum"]
    # Parking a row must never be silent: it has to carry either a parent ruling or the
    # measured evidence that the predicate surface gave no positive answer. The two live
    # under different keys because they came from different passes (`0044`#1 from the harm
    # test's own probes, `0056`#3 from a parent ruling).
    documented = [r for r in parked if r.get("parent_ruling") or r.get("review_note")
                  or r.get("harm_verified")]
    check("搁置层 = 5 条，且每条都有裁定或实测记录",
          len(parked) == 5 and len(documented) == 5,
          "、".join(f"{r['case']}#{r['diff_index']}（{r.get('decided_by')}）" for r in parked))

    by_stratum = Counter(r["stratum"] for r in rows)
    check("各层之和 = 154",
          sum(by_stratum.values()) == 154,
          ", ".join(f"{k} {v}" for k, v in by_stratum.most_common()))

    # --- defect classification covers exactly the admissible set ------------------
    if defects:
        drows = defects["rows"]
        check("缺陷方向分类覆盖 126 条可入",
              len(drows) == 126,
              f"{len(drows)} 行")
        dsum = sum(defects["totals"]["by_direction"].values())
        check("方向合计 = 126",
              dsum == 126,
              f"{defects['totals']['by_direction']}")
        keys = {(r["case"], r["diff_index"]) for r in drows}
        akeys = {(r["case"], r["diff_index"]) for r in adm}
        check("方向分类的键集 = 可入集",
              keys == akeys,
              f"仅在分类里 {len(keys - akeys)}，仅在可入里 {len(akeys - keys)}")

    # --- predicate coverage is over the 153, not the 130 --------------------------
    if verified:
        t = verified["totals"]
        check("谓词复跑覆盖 153 条",
              t["checked"] == t["submitted"] == 153,
              f"复跑 {t['checked']}，提交 {t['submitted']}")
        check("可表述 123 + 不可表述 30 = 153",
              t["captured"] + len(verified["not_expressible"]) == 153,
              f"{t['captured']} + {len(verified['not_expressible'])}")
        check("零条与批次报告不一致、零条断言写错、零条用非封闭谓词",
              not verified["disputed"] and not verified["uses_non_closed"]
              and t["by_verdict"].get("not_captured", 0) == 0,
              f"disputed {len(verified['disputed'])}, "
              f"non_closed {len(verified['uses_non_closed'])}, "
              f"not_captured {t['by_verdict'].get('not_captured', 0)}")
        pred_sum = sum(t["by_predicate"].values())
        check("按谓词的捕获数之和 = 123",
              pred_sum == t["captured"] == 123,
              f"{pred_sum} vs captured {t['captured']}")

    # --- scope audit -------------------------------------------------------------
    if scope:
        st = scope["totals"]
        check("范畴审计：153 条全部 in_scope",
              st["in_scope"] == 153 and st["out_of_scope"] == 0,
              f"in {st['in_scope']}, out {st['out_of_scope']}")

    # --- loop audit --------------------------------------------------------------
    if cells:
        ct = cells["totals"]
        # Two conventions live in this file and mixing them is the trap. `hit` counts
        # *published issues* (20); `distinct_manual_defects_hit` counts them after folding
        # issues that describe one defect (0000's two Power_Off issues; 0029's
        # REQ-007+REQ-008). The 22 denominator is in defects, so only the folded figure
        # closes against it. 20 + 6 = 26 is not an error, it is a category mismatch.
        hit = ct["distinct_manual_defects_hit"]
        denom = ct["admissible_manual_defect_instances_over_8_cells"]
        check("8 格子：去重命中 + 漏检 = 应命中（缺陷口径）",
              hit + ct["missed"] == denom == 22,
              f"命中 {hit} + 漏检 {ct['missed']} = {hit + ct['missed']}，分母 {denom}")
        check("发布条数 ≥ 去重缺陷数（两个口径的方向必须一致）",
              ct["published"] >= hit == 16 and ct["published"] == 20,
              f"发布 {ct['published']} 条 issue 覆盖 {hit} 个去重缺陷")
        check("8 格子多报 = 0",
              ct["over_reported"] == 0,
              f"{ct['over_reported']}")
        stage = cells["missed_by_stage"]
        check("漏检的环节分布之和 = 漏检数",
              sum(stage.values()) == ct["missed"],
              ", ".join(f"{k} {v}" for k, v in stage.items() if v))

    # --- attribution replay ------------------------------------------------------
    if replay:
        flat = replay.get("totals") or replay
        # The producer namespaces these as `attr::safe`. Tolerate the prefix, but do NOT
        # tolerate absence: a check that silently skips when a key is renamed is worse than
        # no check, because the run still prints all-green.
        def attr(key: str):
            return flat.get(f"attr::{key}", flat.get(key))

        tri = [attr(k) for k in ("safe", "representation_debt", "unattributed")]
        if all(isinstance(x, int) for x in tri):
            check("归因重放：safe + debt + unattributed = 123（= 可表述条数）",
                  sum(tri) == 123 == flat.get("captured"),
                  f"safe {tri[0]} + debt {tri[1]} + unattributed {tri[2]} = {sum(tri)}")
            killed = tri[1] + tri[2]
            check("归因致死率 = 46%",
                  round(killed / 123 * 100) == 46,
                  f"({tri[1]} + {tri[2]}) / 123 = {killed / 123:.1%}")
        else:
            check("归因重放：三个归因档位都能读到",
                  False,
                  f"读不到 safe/representation_debt/unattributed，实际键：{sorted(flat)}")

    # --- rescope -----------------------------------------------------------------
    if rescope:
        rt = rescope.get("totals") or {}
        if rt:
            check("RESCOPE：problem 135 + extra 31 − 9 = 157（规范重判口径）",
                  rt.get("problems_in_scope") == 157,
                  f"{rt}")

    passed = sum(1 for _n, ok, _d in checks if ok)
    print(f"一致性检查 {passed} / {len(checks)} 通过\n")
    print("| 检查项 | 结果 | 依据 |")
    print("| --- | :-: | --- |")
    for name, ok, detail in checks:
        print(f"| {name} | {'✓' if ok else '**✗**'} | {detail} |")

    failed = [(n, d) for n, ok, d in checks if not ok]
    if failed:
        print(f"\n### 未通过 {len(failed)} 项 —— 这些数字不得写进 issue\n")
        for name, detail in failed:
            print(f"- **{name}**：{detail}")

    if "--json" in sys.argv:
        dest = pathlib.Path(sys.argv[sys.argv.index("--json") + 1])
        dest.write_text(json.dumps({
            "what_this_is": "issue #171 所有公开数字的交叉一致性检查。"
                            "六个独立来源各自报同一批数，任何两者不一致都必须先解决再发布。",
            "passed": passed, "total": len(checks),
            "checks": [{"name": n, "ok": ok, "detail": d} for n, ok, d in checks],
        }, ensure_ascii=False, indent=1) + "\n")
        print(f"\n已写 {dest}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
