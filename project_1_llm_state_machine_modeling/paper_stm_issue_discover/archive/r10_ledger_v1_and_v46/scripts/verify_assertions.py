"""Re-run every proposed assertion independently, then tally predicate coverage.

The batches report a measured value for each assertion they wrote. This script does not
take that on trust: it evaluates each expression again against the same corpus and compares.
A batch that mis-transcribes a return value, or writes an expression that only worked in its
own scratch harness, would otherwise inflate the coverage figure -- and coverage is the
number the whole exercise exists to produce.

Verdict per row:

  captured        the assertion returned False -- the defect is expressible and caught
  not_captured    returned True -- the assertion does not discriminate, so it is not
                  evidence of anything
  inconclusive    returned None or raised -- `None` is "cannot decide", never "false"
  disputed        our value disagrees with what the batch reported

Only `captured` counts toward "expressible with an existing predicate".

Usage: verify_assertions.py [--json <out>] [--limit N]
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
REVIEWS = HERE / "manual_review"
PREDCHECK = pathlib.Path("/tmp/predcheck")
#: `HERE` is paper_stm_issue_discover/discover_matrix, so the project root is two levels up -- one level was
#: wrong and every evaluation came back as ModuleNotFoundError, i.e. "inconclusive",
#: which would have silently reported zero coverage.
PROJECT = HERE.parents[1]
CORPUS = (PROJECT / "paper_stm_issue_discover/pipeline/representation/reports"
          / "llms_emp_r45_java_60")
FEEDBACK_SRC = PROJECT / "paper_stm_issue_discover/pipeline/feedback_loop/src"

CLOSED = {
    "state_declared": "S", "variable_declared": "S", "event_declared": "S",
    "containment": "S", "initial_target": "S", "edge_declared": "S",
    "effect_declared": "S", "action_declared": "S", "guard_distinguishable": "S",
    "cardinality": "S", "occupancy_after": "B", "event_consumed": "B",
    "stays_in": "B", "variable_delta_after": "B", "reaches": "B", "terminates": "B",
    "invariant": "P", "response_within": "P", "persists_until": "P",
}
SAFE_BUILTINS = {"all", "any", "not", "len", "bool", "sum"}

_ENVS: dict[str, object] = {}


def env_for(case: str):
    """One evaluation environment per pair, cached -- building one is not cheap and a
    batch of 153 rows revisits the same pair many times."""
    if case not in _ENVS:
        if str(FEEDBACK_SRC) not in sys.path:
            sys.path.insert(0, str(FEEDBACK_SRC))
        from paper_stm_feedback_loop.assertions import build_eval_environment

        stem = f"llms_emp_feedback_final_{case}"
        trace = json.loads((CORPUS / f"source_traces/{stem}.json").read_text())
        _ENVS[case] = build_eval_environment(
            model_text=(CORPUS / f"fcstm/{stem}.fcstm").read_text(),
            source_mappings=trace.get("mappings") or [],
            source_exclusions=trace.get("attribution_exclusions") or [],
            timeout_seconds=60, fbmcq_solver_timeout_ms=5000,
            fbmcq_max_bound=3, fbmcq_process_wall_seconds=15.0,
        )
    return _ENVS[case]


def names_in(expr: str) -> list[str]:
    """Call names outside quoted spans. Quoted spans matter: `invariant` and
    `persists_until` take an fbmcq condition *string* whose own calls (`active`, `in`) are
    not predicates."""
    bare = re.sub(r"(['\"]).*?\1", "''", expr or "", flags=re.S)
    return [m.rstrip("( ") for m in re.findall(r"[A-Za-z_][A-Za-z_0-9]*\s*\(", bare)]


def evaluate(case: str, expr: str) -> tuple[str, str]:
    """(verdict, raw) for one expression, evaluated here rather than trusted."""
    try:
        result = env_for(case).eval_assert(expr, "独立复跑")
    except Exception as exc:  # noqa: BLE001 - any failure is inconclusive, and we say which
        return "inconclusive", f"{type(exc).__name__}: {exc}"[:180]
    value = result.value
    if value is False:
        return "captured", "False"
    if value is True:
        return "not_captured", "True"
    return "inconclusive", repr(value)


def load_batches() -> tuple[list[dict], list[str]]:
    rows, complaints = [], []
    for n in range(1, 6):
        path = PREDCHECK / f"result{n}.json"
        if not path.exists():
            complaints.append(f"批 {n} 结果缺失（{path.name}）——该批 items 未纳入统计")
            continue
        payload = json.loads(path.read_text())
        for item in payload.get("items") or []:
            rows.append({**item, "batch": n})
    return rows, complaints


def main() -> int:
    rows, complaints = load_batches()
    if not rows:
        print("没有任何批次结果，先等 agent 产出")
        for c in complaints:
            print(f"  - {c}")
        return 1

    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    checked = rows[:limit] if limit else rows
    verdicts = Counter()
    by_pred: Counter[str] = Counter()
    disputed, illegal, gaps = [], [], []

    for row in checked:
        expr = (row.get("assertion") or "").strip()
        claimed = row.get("expressible")
        if not claimed or not expr:
            gaps.append(row)
            verdicts["declared_not_expressible"] += 1
            continue
        used = names_in(expr)
        outside = sorted({n for n in used if n not in CLOSED and n not in SAFE_BUILTINS})
        if outside:
            # An expression leaning on a legacy primitive does not demonstrate that the
            # closed vocabulary covers the defect, which is the question being asked.
            illegal.append({**row, "outside": outside})
            verdicts["uses_non_closed"] += 1
            continue
        verdict, raw = evaluate(row["case"], expr)
        row["verified_verdict"] = verdict
        row["verified_raw"] = raw
        reported = str(row.get("measured_raw", "")).strip()
        if reported and reported.lower() not in raw.lower():
            row["dispute"] = f"批次报 {reported!r}，复跑 {raw!r}"
            disputed.append(row)
        verdicts[verdict] += 1
        if verdict == "captured":
            for n in used:
                if n in CLOSED:
                    by_pred[n] += 1
                    break

    total = len(checked)
    cap = verdicts["captured"]
    print(f"独立复跑 {total} 条（共 {len(rows)} 条已提交）\n")
    print("| 复跑结论 | 条数 | 含义 |")
    print("| --- | ---: | --- |")
    labels = [
        ("captured", "断言返回 **False** —— 缺陷可被现有谓词表述并捕获"),
        ("not_captured", "返回 True —— 断言不判别，不能作为证据"),
        ("inconclusive", "返回 None 或抛异常 —— 无法判定，不算可表述"),
        ("uses_non_closed", "用了 19 谓词之外的原语 —— 不算现有谓词可表述"),
        ("declared_not_expressible", "批次自己判为不可表述"),
    ]
    for key, desc in labels:
        if verdicts[key]:
            print(f"| `{key}` | **{verdicts[key]}** | {desc} |")
    print(f"\n**可用现有谓词表述并捕获：{cap} / {total}（{cap/total:.0%}）**")
    print(f"**不可表述：{total - cap}**")

    if by_pred:
        print("\n| 谓词 | 族 | 捕获条数 |")
        print("| --- | :-: | ---: |")
        for name, n in by_pred.most_common():
            print(f"| `{name}` | {CLOSED[name]} | {n} |")
        unused = sorted(set(CLOSED) - set(by_pred))
        print(f"\n未捕获任何条目的谓词 {len(unused)} 个："
              + "、".join(f"`{u}`" for u in unused))

    if disputed:
        print(f"\n### 与批次报告不一致 {len(disputed)} 条\n")
        for row in disputed:
            print(f"- `{row['case']}`#{row['diff_index']}: {row['dispute']}")
    if illegal:
        print(f"\n### 使用了非封闭谓词 {len(illegal)} 条\n")
        for row in illegal:
            print(f"- `{row['case']}`#{row['diff_index']}: {'、'.join(row['outside'])}")
    if complaints:
        print(f"\n### 校验\n")
        for c in complaints:
            print(f"- {c}")

    if "--json" in sys.argv:
        dest = pathlib.Path(sys.argv[sys.argv.index("--json") + 1])
        dest.write_text(json.dumps({
            "what_this_is": "对各批提出的断言独立复跑，统计现有 19 谓词的真实覆盖。"
                            "只有复跑返回 False 才计入可表述。",
            "totals": {"checked": total, "submitted": len(rows), "captured": cap,
                       "by_verdict": dict(verdicts), "by_predicate": dict(by_pred)},
            "disputed": disputed, "uses_non_closed": illegal,
            "not_expressible": gaps, "complaints": complaints, "rows": checked,
        }, ensure_ascii=False, indent=1) + "\n")
        print(f"\n已写 {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
