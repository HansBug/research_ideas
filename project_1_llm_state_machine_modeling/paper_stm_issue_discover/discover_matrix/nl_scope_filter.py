"""按 paper1 的建模对象 `M = (S, E, V, Tr, A)` 先验筛选评测语料。

## 为什么筛选单位是 NL，不是 pair

60 个 pair 由 **10 份不同 NL** 各生成 6 个。逐 pair 判定会留下「挑掉某几格」的空间；
按 NL 判定没有 —— 一份 NL 的 6 个 pair 同进同出。

## 判据（先验，只读 NL 文本，不看任何结果）

`CLAUDE.md` 把 project_1 的建模对象写死为 `M = (S, E, V, Tr, A)`，并明确
**时钟变量与不变式、正交区并发均排除在建模对象之外**。因此一份 NL 若要求：

* **fork / join 伪状态** —— UML 的并发构造，忠实模型需要正交区，而 `M` 无区分量；
* **执行时间 / 秒级约束** —— 忠实模型需要时钟与不变式，而 `M` 两者皆无；

则该 NL 的忠实模型**无法在 `M` 中表示**，其 pair 族不在本方法的断言对象内。

⚠️ 这不是「排除表现差的样本」。实测：被排除的 NL 有 6 个 pair，其中 `0018` 的 `hit@1` 为 66.7%，
**高于全量均值 53.9%**。筛选同时排掉了优于均值的样本。

## 实测结论（本脚本产出）

10 份 NL 中**恰好 1 份**同时含 fork/join 与密集计时（11 处 fork/join、17 处计时），
其余 9 份 fork/join 为 0、计时最多 3 处。该份 NL 的 6 个 pair 是 `0008` `0018` `0028`
`0038` `0048` `0058`（**全部以 8 结尾**）。

## 用法

    python nl_scope_filter.py                 # 打印 10 份 NL 的判定表
    python nl_scope_filter.py --excluded      # 只打印被排除的 pair，供其他脚本消费
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import pathlib
import re
import sys

SEED = (
    pathlib.Path(__file__).resolve().parents[2]
    / "paper_stm_issue_discover"
    / "selected_seed_examples"
)

# 并发构造：fork / join 伪状态。`M` 无正交区，无法忠实表示。
CONCURRENCY = re.compile(r"\bfork\w*|\bjoin\w*", re.IGNORECASE)
# 时间约束：执行时间、秒级边界、计时器。`M` 无时钟变量与不变式。
TIMING = re.compile(
    r"\b\d+\s*second|\bseconds\b|execution time|maximum of|minimum of|within \d+|timer|\bdelay\b",
    re.IGNORECASE,
)

# 一份 NL 触发排除所需的最小证据量。
#
# ⚠️ 阈值不是为了调数字，而是为了区分「规约要求该特性」与「文字里偶然出现该词」。
# 实测分布是**双峰且间隔极大**：并发 11 vs 0（其余 9 份全为 0），计时 17 vs 3 vs 0。
#
# 敏感性实测（扫 并发 1–11 × 计时 1–17 共 187 组）：
#   * **154 / 187 组给出完全相同的 6 个 pair** —— 即并发 1–11 × 计时 4–17 全域一致
#   * 只有计时 ≤ 3 时划分改变：那会把 `934e19bd`（3 处计时、0 处并发）也拉进来，变成 12 个 pair
#
# 所以本判定对并发阈值**完全不敏感**，对计时阈值只在 3/4 之间有一个断点，而 4 以上全域一致。
# 复现：见本文件末尾的 `_sensitivity()`。
MIN_CONCURRENCY = 2
MIN_TIMING = 5


def nl_groups() -> dict[str, list[str]]:
    """→ {NL 内容哈希: [pair ...]}，按 `nl.txt` 内容归并。"""
    groups: dict[str, list[str]] = collections.defaultdict(list)
    for d in sorted(SEED.glob("llms_emp_feedback_final_*")):
        nl = d / "nl.txt"
        if not nl.is_file():
            continue
        text = nl.read_text(encoding="utf-8", errors="replace").strip()
        groups[hashlib.sha256(text.encode()).hexdigest()[:8]].append(d.name[-4:])
    return dict(groups)


def classify() -> list[dict]:
    rows = []
    for h, pairs in nl_groups().items():
        text = (SEED / f"llms_emp_feedback_final_{pairs[0]}" / "nl.txt").read_text(
            encoding="utf-8", errors="replace"
        )
        conc = len(CONCURRENCY.findall(text))
        time = len(TIMING.findall(text))
        out_of_scope = conc >= MIN_CONCURRENCY or time >= MIN_TIMING
        rows.append(
            {
                "nl": h,
                "pairs": sorted(pairs),
                "concurrency_hits": conc,
                "timing_hits": time,
                "out_of_scope": out_of_scope,
                "reason": (
                    "requires fork/join (no orthogonal regions in M)"
                    if conc >= MIN_CONCURRENCY
                    else "requires timing (no clocks or invariants in M)"
                    if time >= MIN_TIMING
                    else ""
                ),
            }
        )
    return sorted(rows, key=lambda r: (-r["concurrency_hits"], -r["timing_hits"]))


def excluded_pairs() -> list[str]:
    return sorted(p for r in classify() if r["out_of_scope"] for p in r["pairs"])


def _sensitivity(global_c: int = 11, global_t: int = 17) -> tuple[int, int, list[str]]:
    """扫阈值网格，返回 (与基线一致的组合数, 总组合数, 与基线一致的阈值范围描述)。

    这条存在的理由：一个可以调阈值调出想要结果的筛选不是先验筛选。把不敏感性做成可复算的，
    而不是在文档里断言它。
    """
    global MIN_CONCURRENCY, MIN_TIMING
    keep_c, keep_t = MIN_CONCURRENCY, MIN_TIMING
    base = tuple(excluded_pairs())
    same = []
    try:
        for c in range(1, global_c + 1):
            for t in range(1, global_t + 1):
                MIN_CONCURRENCY, MIN_TIMING = c, t
                if tuple(excluded_pairs()) == base:
                    same.append((c, t))
    finally:
        MIN_CONCURRENCY, MIN_TIMING = keep_c, keep_t
    total = global_c * global_t
    if same:
        cs = sorted({c for c, _ in same})
        ts = sorted({t for _, t in same})
        rng = [f"并发 {min(cs)}–{max(cs)} × 计时 {min(ts)}–{max(ts)}"]
    else:
        rng = ["（无）"]
    return len(same), total, rng


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--excluded", action="store_true", help="只打印被排除的 pair，空格分隔")
    ap.add_argument("--sensitivity", action="store_true", help="扫阈值网格，验证划分不敏感")
    args = ap.parse_args(argv)

    if args.sensitivity:
        n, total, rng = _sensitivity()
        print(f"与基线划分一致：{n} / {total} 组阈值 —— {rng[0]}")
        print(f"基线：并发 ≥ {MIN_CONCURRENCY} 或 计时 ≥ {MIN_TIMING} → {' '.join(excluded_pairs())}")
        return 0

    if args.excluded:
        print(" ".join(excluded_pairs()))
        return 0

    rows = classify()
    print(f"{'NL':<10}{'pair 数':>7}{'并发':>6}{'计时':>6}{'范围内':>8}  pairs")
    for r in rows:
        print(
            f"{r['nl']:<10}{len(r['pairs']):>7}{r['concurrency_hits']:>6}"
            f"{r['timing_hits']:>6}{('✗ 排除' if r['out_of_scope'] else '✓'):>8}"
            f"  {','.join(r['pairs'])}"
        )
    ex = excluded_pairs()
    print(f"\n阈值：并发 ≥ {MIN_CONCURRENCY} 或 计时 ≥ {MIN_TIMING}")
    print(f"被排除：{len(ex)} / 60 个 pair —— {' '.join(ex)}")
    print(f"保留：{60 - len(ex)} 个 pair")
    for r in rows:
        if r["out_of_scope"]:
            print(f"\n{r['nl']}: {r['reason']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
