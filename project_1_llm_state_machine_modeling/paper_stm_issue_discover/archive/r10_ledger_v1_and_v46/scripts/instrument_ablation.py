"""对比两个判定装置下的同一批标注：跨条件位移 vs 组内分歧。

## 判据的构造

每个条件下有**两位**独立标注者，所以每个条件自带一个**判定方差**估计（两人的覆盖侧分歧位数）。
于是不需要额外的"同装置重判"对照：

    跨条件位移 ≤ max(组内分歧)        → 不可归因
    max(组内分歧) < 位移 ≤ 2×         → 弱信号
    位移 > 2× max(组内分歧)           → 可作装置效应讨论

⚠️ 这与运行侧的噪声底是**两种不同的方差**：运行侧测「同装置下重复运行」，这里测「同装置下不同判定者」。
`hit@1` 的逐轮极差不作本工具的判据。

## 为什么不能只比 hit@1 的两个数

两位标注者可能各自命中 110 个位而**不是同一批 110**（v24 泄漏装置下实测正是如此：A 110、B 110、
分歧 4 个位）。所以位移必须按**逐位比对**算，不能按聚合数相减 —— 后者会把两个方向的变化抵消掉。
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys

# ⚠️ 2026-08-17 归档：本文件原在 `discover_matrix/` 顶层，`HERE` 即指那一层；
# ⛔ 归档到 `archive/r10_ledger_v1_and_v46/scripts/` 后深度多了两层，`HERE / "manual_review"`
# 会解析到不存在的 `scripts/manual_review`。⭐ 故改为指向归档根（它保留了原 discover_matrix
# 的内部布局：manual_review/ · v46/ · verdicts/ …），⛔ 不数层数、按目录名锚定。
_F = pathlib.Path(__file__).resolve()
HERE = next(p for p in _F.parents if p.name == "r10_ledger_v1_and_v46")
OUT = HERE / "onepass_sample"



def hits_aliases(label: str | None) -> frozenset[str]:
    """`hits:A` → {A}；`hits:A+B` → {A, B}；其他标签 → 空集。

    ⚠️ 多别名形式是判据的一条**修正**：一条 issue 的正文可能同时陈述两条期望缺陷的事实，而
    「一条 issue 一个标签」曾迫使标注者二选一，另一条被记为未命中。两位标注者独立报告了这个
    系统性低估，故 `hits:` 允许 `+` 连接。

    ⛔ 读取器必须用本函数，不得写 `label == f"hits:{alias}"` —— 精确比较会让 `hits:A+B` 既不匹配
    A 也不匹配 B，等于把这条修正静默吃掉，且**表现为覆盖率下降**而不是报错。
    """
    if not isinstance(label, str) or not label.startswith("hits:"):
        return frozenset()
    return frozenset(part.strip() for part in label[5:].split("+") if part.strip())

def _coverage(sample: dict, key: dict, labels: dict) -> dict[tuple[str, str, str], int]:
    """→ {(record_id, arm, run): 0|1}，按 `hits:<alias>` 派生。"""

    by_unit = {i["unit_id"]: i for i in key["items"]}
    out = {}
    for item in sample["items"]:
        kitem = by_unit[item["unit_id"]]
        for alias, meta in kitem["record_aliases"].items():
            hit = any(
                alias in hits_aliases(labels.get(i["issue_uid"], {}).get("label"))
                for i in item["published_issues"]
            )
            out[(meta["record_id"], kitem["arm"], kitem["run"])] = int(hit)
    return out


def _load(path: pathlib.Path) -> dict:
    """Normalise both annotation shapes to a flat ``{issue_uid: {"label": ...}}``.

    Two shapes exist in the corpus and they must both be readable by one reader:

    ``v1.0`` (v24 and earlier)   ``{"labels": {uid: {...}}, "unhit_expected": {...}}``
    ``v1.2`` (v25 onward)        ``{"units": [{"issues": [{"issue_uid": ..., "label": ...}]}]}``

    ⚠️ Reading only ``labels`` silently yields ``{}`` for a v1.2 file, and every downstream
    count then comes out **zero** -- which is indistinguishable from a real "nothing hit".
    That is exactly how the first ablation run reported ``clean hit@1 = 0/204`` while both
    annotators had in fact labelled 133 and 132 hits. Hence :func:`main` asserts a non-empty
    load per file rather than trusting the number it gets.
    """
    doc = json.loads(path.read_text())
    if isinstance(doc.get("labels"), dict):
        return doc["labels"]
    flat: dict = {}
    for unit in doc.get("units") or []:
        for issue in unit.get("issues") or []:
            uid = issue.get("issue_uid")
            if uid:
                flat[uid] = issue
    return flat


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--leaky-a", type=pathlib.Path, required=True)
    parser.add_argument("--leaky-b", type=pathlib.Path, required=True)
    parser.add_argument("--clean-a", type=pathlib.Path, required=True)
    parser.add_argument("--clean-b", type=pathlib.Path, required=True)
    args = parser.parse_args(argv)

    sample = json.loads((OUT / "sample.json").read_text())
    key = json.loads((OUT / "key.json").read_text())
    for name, path in vars(args).items():
        if not path.is_file():
            print(f"ERROR: no {path}", file=sys.stderr)
            return 2

    labels = {name: _load(path) for name, path in vars(args).items()}
    for name, lab in labels.items():
        if not lab:
            raise SystemExit(
                f"{name} ({vars(args)[name]}) 读出 0 条标签 —— 几乎必然是 schema 不认，"
                f"不是标注者一条都没判。已知形状：v1.0 顶层 'labels'、v1.2 顶层 'units[].issues[]'。"
            )
    cov = {name: _coverage(sample, key, lab) for name, lab in labels.items()}
    slots = sorted(cov["leaky_a"])

    def spread(x: str, y: str) -> int:
        return sum(1 for s in slots if cov[x][s] != cov[y][s])

    within_leaky = spread("leaky_a", "leaky_b")
    within_clean = spread("clean_a", "clean_b")
    # 跨条件：逐位比对（不是聚合相减）。取两位标注者的保守合并（both hit → 1）。
    def merged(x: str, y: str) -> dict:
        return {s: int(cov[x][s] == 1 and cov[y][s] == 1) for s in slots}

    ml, mc = merged("leaky_a", "leaky_b"), merged("clean_a", "clean_b")
    shift_pos = sum(1 for s in slots if ml[s] != mc[s])
    up = sum(1 for s in slots if ml[s] == 0 and mc[s] == 1)
    down = sum(1 for s in slots if ml[s] == 1 and mc[s] == 0)

    noise = max(within_leaky, within_clean)
    verdict = ("不可归因" if shift_pos <= noise
               else "弱信号" if shift_pos <= 2 * noise
               else "**可作装置效应讨论**")

    print(f"判定位 {len(slots)}\n")
    print("| 量 | 值 |")
    print("| :-- | --: |")
    print(f"| 泄漏装置组内分歧 | {within_leaky} |")
    print(f"| 干净装置组内分歧 | {within_clean} |")
    print(f"| **跨条件位移（逐位）** | **{shift_pos}** |")
    print(f"| 其中 未中→命中 | {up} |")
    print(f"| 其中 命中→未中 | {down} |")
    print(f"\n组内方差上界 {noise} → **{verdict}**")
    for name in ("leaky", "clean"):
        m = merged(f"{name}_a", f"{name}_b")
        h = sum(m.values())
        print(f"  {name:6s} 保守合并 hit@1 = {h}/{len(slots)} = {h/len(slots)*100:.1f}%")
    print("\n⚠️ 位移按**逐位**算，不按聚合数相减 —— 后者会把两个方向的变化抵消。"
          f"本次 {up} 升 / {down} 降，聚合差仅 {up-down:+d}。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
