"""证据分布分析：回答「19 条谓词的上游证据为什么厚薄不均」。

这个工具存在的理由是一条**指控**，而不是一项统计需求：

    「弱证据的那些谓词，是不是照着 54 个 pair 的缺陷反推出来的？」

如果指控成立，证据量应当与**案例用量正相关** —— 每条谓词都因为「能抓住某个案例
缺陷」而入选，而案例缺陷是真实缺陷的样本，于是真实系统里也该常见。本工具复算这个
相关性，并按族聚合，把分布的形状摆出来让人自己判断。

⛔ **本工具不做规范性判断。** 它只输出数字；「这个分布说明了什么」写在
[../evidence_distribution.md](../evidence_distribution.md)，由人裁定。

用法：

    python -m tools.analyze_evidence_distribution                # 读默认路径
    python -m tools.analyze_evidence_distribution --agg X.json   # 指定裁定后聚合
    python -m tools.analyze_evidence_distribution --markdown     # 输出 md 表格
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

#: ⭐ 台账用量与族归属从 `build_provenance_table.py` **导入**，⛔ 不在本文件重复定义。
#: 复制一份出来会立刻变成第二事实源 —— 两处数字漂移时无人知道该信哪个。
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_provenance_table import FAMILY, FAMILY_CN, LEDGER, META_DEFINED  # noqa: E402


def _find_default_agg() -> Path | None:
    """向上找 `results/agg_final.json`；找不到返回 None 而不是抛。

    ⛔ 不用 `parents[N]` 数层级：改变目录深度会让它**静默**解析到错误路径，
    而空输入在本工具里会被读成「所有谓词证据为 0」—— 那是个看起来像结论的假象。
    """
    for parent in Path(__file__).resolve().parents:
        for cand in (parent / "results" / "agg_final.json", parent / "agg_final.json"):
            if cand.is_file():
                return cand
    fallback = Path("/tmp/l2/results/agg_final.json")
    return fallback if fallback.is_file() else None


def spearman(xs: list[float], ys: list[float]) -> float:
    """秩相关。用秩而非原值，因为证据量是重尾的（`invariant` 41 vs 中位数 3）。"""

    def rank(v: list[float]) -> list[float]:
        order = sorted(range(len(v)), key=lambda i: v[i])
        out = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1  #: 并列取平均秩
            for k in range(i, j + 1):
                out[order[k]] = avg
            i = j + 1
        return out

    rx, ry = rank(xs), rank(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else 0.0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--agg", type=Path, default=None, help="裁定后聚合 JSON")
    ap.add_argument("--markdown", action="store_true", help="输出 Markdown 表格")
    args = ap.parse_args(argv)

    agg_path = args.agg or _find_default_agg()
    if agg_path is None or not agg_path.is_file():
        print("⛔ 未找到裁定后聚合 JSON；请用 --agg 显式指定。", file=sys.stderr)
        return 2

    rows = json.loads(agg_path.read_text(encoding="utf-8"))["rows"]
    evid = {r["predicate"]: r for r in rows}

    missing = set(LEDGER) - set(evid)
    if missing:
        print(f"⛔ 聚合里缺这些谓词，数字会失真：{sorted(missing)}", file=sys.stderr)
        return 2

    preds = list(LEDGER)
    led = [LEDGER[p][0] for p in preds]          #: 台账断言数 = 案例期望缺陷用到它多少次
    pub = [LEDGER[p][2] for p in preds]          #: 已发布支撑 = v46 制品上它被断言多少次
    real = [float(evid[p]["real_systems"]) for p in preds]
    lit = [float(evid[p]["literature"]) for p in preds]

    print(f"# 证据分布分析（源：{agg_path}）\n")
    print("## 1. 案例用量 vs 上游证据量：秩相关\n")
    print("⭐ 若「照着案例反推」成立，这几个 rho 应当**显著为正**。\n")
    pairs = [
        ("台账断言（案例期望缺陷）", "界内真实系统", led, real),
        ("台账断言（案例期望缺陷）", "文献", led, lit),
        ("已发布支撑（制品实际断言）", "界内真实系统", pub, real),
    ]
    for xn, yn, xv, yv in pairs:
        print(f"- `{xn}` × `{yn}` : **rho = {spearman(xv, yv):+.3f}**")

    print("\n## 2. 按族聚合\n")
    hdr = "| 族 | 谓词数 | 台账断言 | 占比 | 界内真实系统 | 占比 | 文献 | 真实系统/谓词 |"
    print(hdr)
    print("| :-- | --: | --: | --: | --: | --: | --: | --: |")
    for fam in ("P", "B", "S"):
        m = [p for p in preds if FAMILY[p] == fam]
        L = sum(LEDGER[p][0] for p in m)
        R = sum(evid[p]["real_systems"] for p in m)
        Li = sum(evid[p]["literature"] for p in m)
        print(
            f"| {FAMILY_CN[fam]} | {len(m)} | {L} | {L / sum(led) * 100:.1f}% | "
            f"{R} | {R / sum(real) * 100:.1f}% | {Li} | {R / len(m):.1f} |"
        )
    print(f"| **合计** | {len(preds)} | {sum(led):.0f} | 100% | {sum(real):.0f} | 100% | {sum(lit):.0f} | {sum(real) / len(preds):.1f} |")

    print("\n## 3. 两端对照\n")
    print("**证据最厚的 4 条 —— 案例用了多少：**\n")
    for p in sorted(preds, key=lambda p: -evid[p]["real_systems"])[:4]:
        print(f"- `{p}`：界内真实系统 **{evid[p]['real_systems']}**，⭐ 台账断言仅 **{LEDGER[p][0]}**")
    print("\n**案例用得最多的 4 条 —— 证据多少：**\n")
    for p in sorted(preds, key=lambda p: -LEDGER[p][0])[:4]:
        cls = "②" if p in META_DEFINED else ("③" if evid[p]["total_sources"] < 3 else "①")
        print(f"- `{p}`（{cls}）：台账断言 **{LEDGER[p][0]}**，→ 界内真实系统 **{evid[p]['real_systems']}**、文献 **{evid[p]['literature']}**")

    print("\n## 4. 真正暴露的格子\n")
    print("⭐ 判据：**③ 类**（无外部依据）**且**台账断言进入前 1/3 —— 即「案例很依赖它、上游却给不出出处」。\n")
    cut = sorted(led, reverse=True)[len(preds) // 3]
    exposed = [
        p for p in preds
        if p not in META_DEFINED and evid[p]["total_sources"] < 3 and LEDGER[p][0] >= cut
    ]
    if exposed:
        for p in exposed:
            print(f"- ⛔ `{p}`：台账断言 {LEDGER[p][0]}（阈值 {cut}）· 来源 {evid[p]['total_sources']} 条")
    else:
        print("- ⭐ 无。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
