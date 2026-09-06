#!/usr/bin/env python3
"""从 `results/unexpected_verdicts/X1-*.jsonl` 重建 X1 多报侧的全部派生表。

## 为什么不直接用主臂的 `discover_matrix/rebuild_unexpected.py`

三处不兼容，都不是可以「改个路径」绕过的：

1. 主臂脚本把真源路径写死在 `v46/unexpected_verdicts`，且从 `/tmp/unexp_pkg` 的证据包补
   `出现格数` 与 `谓词族`。⛔ X1 无谓词、无断言签名，谓词族一栏**不存在被度量的对象**
   （事前登记 §8.4），所以表 3 在 X1 上是空表而不是待填表。
2. 主臂的分母闭合有三个去向（桶内 / 台账已承载 / 真阴性）。⛔ X1 **没有真阴性档**——
   剔真阴性要把断言在冻结制品上重新求值，而 X1 的 issue 不是可求值命题。X1 另有一个
   主臂没有的去向：**产出可判定性**（三段文本合起来仍不能定位到任一元素或结构）。
3. ⛔⛔ `REPRESENTATION_DEBT` 在 X1 上**结构性为空**：该类的定义是「事实在编译产物上为真、
   而作者在 `stm0.puml` 里已逐字表达」，X1 读的输入 `plantuml.puml` 与 `stm0.puml` 逐字节相同
   （sha256 已核验），它从未见过编译产物，不可能报出一条编译损失。本脚本把它当作**硬错误**
   拦下，而不是允许出现的 0 行。

⚠️ 与主臂脚本相同的两条纪律照旧：**本脚本只做汇总与格式化，不做任何判定**；裁定只能改 jsonl。
`merge_key` 是去重单元 `(pair, 根因)` 的实现，跨 pair / 跨 verdict / 跨 subclass 的 key
一律判为「去重单元被破坏」并报错。

用法::

    python -m baseline_arm.analysis.rebuild_unexpected_x1          # 重建 tables.md 并打印分布
    python -m baseline_arm.analysis.rebuild_unexpected_x1 --check  # 只校验，不写盘
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import statistics
import sys

HERE = pathlib.Path(__file__).resolve().parent
RESULTS = HERE.parent / "results"
VERDICTS = RESULTS / "unexpected_verdicts"

#: ⛔ 四类。`REPRESENTATION_DEBT` 不在其中——见模块 docstring 第 3 条。
ORDER = ("VALID_UNRECORDED", "NO_NL_BASIS", "FALSE_POSITIVE", "OUT_OF_SCOPE")
LABEL = {
    "VALID_UNRECORDED": "✅ 真漏记",
    "NO_NL_BASIS": "📄 无 NL 依据",
    "FALSE_POSITIVE": "❌ 假阳性",
    "OUT_OF_SCOPE": "🚫 越界",
}
BANNED = {
    "REPRESENTATION_DEBT": (
        "表示债务在 X1 上结构性为空：X1 读的是作者源 plantuml.puml（与 stm0.puml 逐字节相同），"
        "从未见过编译产物，不可能报出一条 R4.5 编译损失。看起来像债务的簇实为对作者源本身的主张，"
        "应走流程 ⑥ 判 NO_NL_BASIS 或 VALID_UNRECORDED"
    ),
    "MERGE_INTO_LEDGER": "内容已被台账承载者不属意外发现，应移入 ledger_accounted.jsonl",
    "UNCERTAIN": "证据不足不是裁定类别，回读原件后裁死",
}

REQUIRED = ("cluster", "verdict", "fact", "nl", "subclass", "merge_key", "merge_reason")


def load() -> list[dict]:
    rows: list[dict] = []
    paths = sorted(VERDICTS.glob("X1-*.jsonl"))
    if not paths:
        raise SystemExit(f"没有找到任何 X1-*.jsonl：{VERDICTS}")
    for path in paths:
        if path.name.endswith(("-ledger_accounted.jsonl", "-undecidable.jsonl")):
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            record = json.loads(line)
            for field in REQUIRED:
                if not (record.get(field) or "").strip():
                    raise SystemExit(
                        f"{path.name}:{lineno} 缺字段 {field}：{record.get('cluster')}"
                    )
            verdict = record["verdict"]
            if verdict in BANNED:
                raise SystemExit(f"{record['cluster']} 用了禁用标签 {verdict}：{BANNED[verdict]}")
            if verdict not in ORDER:
                raise SystemExit(f"{record['cluster']} 的裁定 {verdict} 不在四类内")
            cells = int(record.get("cells_of_6") or 0)
            if not 1 <= cells <= 6:
                raise SystemExit(f"{record['cluster']} 的 cells_of_6={cells} 不在 1..6")
            record["_group"] = path.stem
            record["_pair"] = record["cluster"].split("-")[0]
            rows.append(record)
    dupes = [c for c, n in collections.Counter(r["cluster"] for r in rows).items() if n > 1]
    if dupes:
        raise SystemExit(f"簇重复：{dupes}")
    _check_merge_units(rows)
    return rows


def _check_merge_units(rows: list[dict]) -> None:
    """`merge_key` 必须是 `(pair, 根因)` 的实现，不许跨 pair / verdict / subclass。"""
    by_key: dict[str, list[dict]] = collections.defaultdict(list)
    for r in rows:
        by_key[r["merge_key"]].append(r)
    broken = []
    for key, group in by_key.items():
        for dim in ("_pair", "verdict", "subclass"):
            if len({g[dim] for g in group}) > 1:
                broken.append(f"{key} 跨 {dim}：{sorted({g[dim] for g in group})}")
        if not key.startswith(group[0]["_pair"] + "-"):
            broken.append(f"{key} 未以 pair 前缀开头")
    if broken:
        raise SystemExit("去重单元被破坏：\n  " + "\n  ".join(broken))


def _side(path: pathlib.Path) -> list[dict]:
    rows = []
    for p in sorted(VERDICTS.glob(f"X1-*{path.name}")):
        rows += [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    return rows


def _pct(n: int, d: int) -> str:
    return f"{100.0 * n / d:.1f}%" if d else "—"


def build(rows: list[dict]) -> str:
    accounted = _side(pathlib.Path("-ledger_accounted.jsonl"))
    undecidable = _side(pathlib.Path("-undecidable.jsonl"))
    closure = {}
    for p in sorted(VERDICTS.glob("X1-*-closure.json")):
        closure[p.stem] = json.loads(p.read_text(encoding="utf-8"))

    total = len(rows)
    dedup = len({r["merge_key"] for r in rows})
    out: list[str] = []
    w = out.append

    w("# X1 朴素基线臂 · 多报侧全量统计表\n")
    w("⚠️ **本文件整份由 `unexpected_verdicts/X1-*.jsonl` 生成**"
      "（[../../analysis/rebuild_unexpected_x1.py](../../analysis/rebuild_unexpected_x1.py)）。"
      "**不要手工编辑**，也不要在别处保存这些表的副本。\n")
    w("裁定口径见主臂 [unexpected_taxonomy.md](../../../discover_matrix/docs/protocol/unexpected_taxonomy.md)，"
      "X1 侧的三条适配（判事实的基准换成作者源、表示债务结构性为空、新增产出可判定性档）"
      "见本文件 §表 0 下方的说明与 [preregistered.md §8.4](../../preregistered.md)。\n")
    w("\n---\n")

    # 表 0
    w("\n## 表 0　分母闭合\n")
    w("| 去向 | 条数 | 说明 |")
    w("| :-- | --: | :-- |")
    w(f"| 多报侧桶内 | {total} | 本文件其余各表的分母 |")
    w(f"| `X1-*-ledger_accounted.jsonl` | {len(accounted)} | 内容已被台账记录承载，按定义不属意外发现 |")
    w(f"| `X1-*-undecidable.jsonl` | {len(undecidable)} | ⭐ **X1 特有**：三段文本合起来仍不能定位到制品上任一元素或结构，⛔ 不塞进四类 |")
    w("| 真阴性 | **该档在 X1 上不存在** | 剔真阴性要把断言在冻结制品上重新求值，而 X1 的 issue 不是可求值命题。"
      "⚠️ 这使 X1 桶内分母相对主臂**偏大一个未知量**，方向对 X1 不利 |")
    w(f"| **最初簇总数** | **{total + len(accounted) + len(undecidable)}** | |")

    # 表 1
    w("\n---\n")
    w("\n## 表 1　大类分布（双分母）\n")
    w("去重单元 = `(pair, 根因)`；同 pair 同一处失误合并计 1，不同 pair 不合并。\n")
    w("| 大类 | 条目数 | 占比 | 去重数 | 占比 | 条目/去重 | 子类数 |")
    w("| :-- | --: | --: | --: | --: | --: | --: |")
    w("| ⚙️ 表示债务 | **0** | 0.0% | **0** | 0.0% | — | 0 |")
    for v in ORDER:
        sub = [r for r in rows if r["verdict"] == v]
        d = len({r["merge_key"] for r in sub})
        ratio = f"{len(sub) / d:.2f}" if d else "—"
        w(f"| {LABEL[v]} | {len(sub)} | {_pct(len(sub), total)} | {d} | {_pct(d, dedup)} | "
          f"{ratio} | {len({r['subclass'] for r in sub})} |")
    w(f"| **合计** | **{total}** | 100% | **{dedup}** | 100% | "
      f"**{total / dedup:.2f}** | {len({r['subclass'] for r in rows})} |")
    w("\n⛔ **表示债务那一行的 0 不是「没测到」，是「结构性不存在」**："
      "X1 读的输入 `plantuml.puml` 与作者源 `stm0.puml` 逐字节相同（sha256 已核验），"
      "它从未见过 R4.5 的编译产物，因而不可能报出一条编译损失。"
      "⚠️ 主臂该类占 134 条目（46.5%）/ 30 去重（24.2%），是主臂多报侧最大的一块。\n")

    # 表 2
    w("\n---\n")
    w("\n## 表 2　子类分布（双分母）\n")
    for v in ORDER:
        sub = [r for r in rows if r["verdict"] == v]
        if not sub:
            continue
        w(f"\n### {LABEL[v]}　{len(sub)} 条目 / {len({r['merge_key'] for r in sub})} 去重\n")
        w("| 子类 | 条目数 | 去重数 | 条目/去重 | 涉及 pair | 中位出现_of_6 | ≥4 格 |")
        w("| :-- | --: | --: | --: | --: | --: | --: |")
        counts = collections.Counter(r["subclass"] for r in sub)
        for name, n in counts.most_common():
            g = [r for r in sub if r["subclass"] == name]
            d = len({r["merge_key"] for r in g})
            cells = [int(r["cells_of_6"]) for r in g]
            w(f"| `{name}` | {n} | {d} | {n / d:.2f} | {len({r['_pair'] for r in g})} | "
              f"{statistics.median(cells):g} | {sum(1 for c in cells if c >= 4)} |")

    # 表 3
    w("\n---\n")
    w("\n## 表 3　谓词族 × 裁定\n")
    w("⛔ **该表在 X1 上不存在被度量的对象。** X1 无谓词、无断言签名——"
      "⭐ 这不是能力缺陷，是对照臂**按设计不携带 C-② 闭合词表**。"
      "⛔ 不得拿主臂的表 3 去暗示 X1 的谓词行为。\n")

    # 表 4
    w("\n---\n")
    w("\n## 表 4　稳定性（出现格数 × 裁定）\n")
    w("全网格每簇最多出现在 6 格（2 模型 × 3 轮）。\n")
    w("| 大类 | 1 格 | 2 格 | 3 格 | 4 格 | 5 格 | 6 格 | 合计 | ≥4 格占比 |")
    w("| :-- | --: | --: | --: | --: | --: | --: | --: | --: |")
    grand = [0] * 7
    for v in ORDER:
        sub = [r for r in rows if r["verdict"] == v]
        if not sub:
            continue
        hist = [sum(1 for r in sub if int(r["cells_of_6"]) == k) for k in range(1, 7)]
        for i, n in enumerate(hist):
            grand[i] += n
        w(f"| {LABEL[v]} | " + " | ".join(str(n) for n in hist) +
          f" | {len(sub)} | {_pct(sum(hist[3:]), len(sub))} |")
    w("| **合计** | " + " | ".join(f"**{n}**" for n in grand[:6]) +
      f" | **{total}** | {_pct(sum(grand[3:6]), total)} |")
    one = grand[0]
    w(f"\n**{one}/{total}（{_pct(one, total)}）只出现在 1 个格里。**\n")

    # 表 5
    w("\n---\n")
    w("\n## 表 5　多成员合并组（成员数 >= 4）\n")
    sizes = collections.Counter(r["merge_key"] for r in rows)
    big = [(k, n) for k, n in sizes.most_common() if n >= 4]
    if big:
        w("| merge_key | 成员数 | 大类 |")
        w("| :-- | --: | :-- |")
        for k, n in big:
            v = next(r["verdict"] for r in rows if r["merge_key"] == k)
            w(f"| `{k}` | {n} | {LABEL[v]} |")
    else:
        w("本轮无成员数 >= 4 的合并组。")
    multi = sum(1 for n in sizes.values() if n > 1)
    w(f"\n{dedup} 组 = {multi} 个多成员组 + {dedup - multi} 个单成员组。\n")

    # 表 6
    w("\n---\n")
    w("\n## 表 6　⭐ X1 特有：产出可判定性\n")
    w("事前登记 [§8.4](../../preregistered.md) 定义的新裁定路径：一条 issue 的 "
      "`issue` + `where` + `reason` 三段合起来**仍不能定位到制品上任一元素或结构**时，"
      "记为独立统计量，⛔ 不塞进四类。\n")
    und_members = sum(len(r.get("members") or []) for r in undecidable)
    w("| 口径 | 数 |")
    w("| :-- | --: |")
    w(f"| 不可定位簇 | {len(undecidable)} |")
    w(f"| 不可定位 issue 条 | {und_members} |")
    w(f"| 占最初簇总数 | {_pct(len(undecidable), total + len(accounted) + len(undecidable))} |")
    w("\n⚠️ 主臂无此档：它的每条 issue 都由断言签名（谓词 + 元素绑定）承载，按构造必可定位。"
      "⛔ 所以这一栏**不能**读作「主臂 0 条、X1 若干条 → 主臂更好」——两侧不是同类对象。\n")

    # 表 7
    w("\n---\n")
    w("\n## 表 7　各判定组闭合自检\n")
    if closure:
        keys = ("issues_total", "unclaimed_before", "moved_to_claimed", "moved_to_unclaimed",
                "unclaimed_after", "bucket_clusters", "bucket_members",
                "ledger_accounted_members", "undecidable_members")
        w("| 组 | " + " | ".join(keys) + " | 闭合 |")
        w("| :-- | " + " | ".join("--:" for _ in keys) + " | :-- |")
        agg = collections.Counter()
        for g in sorted(closure):
            c = closure[g]
            for k in keys:
                agg[k] += int(c.get(k) or 0)
            ok = (int(c.get("unclaimed_after") or 0)
                  == int(c.get("bucket_members") or 0)
                  + int(c.get("ledger_accounted_members") or 0)
                  + int(c.get("undecidable_members") or 0))
            w(f"| {g.replace('X1-', '').replace('-closure', '')} | "
              + " | ".join(str(c.get(k)) for k in keys) + f" | {'✅' if ok else '⛔'} |")
        w("| **合计** | " + " | ".join(f"**{agg[k]}**" for k in keys) + " | |")
    else:
        w("⛔ 未找到任何 `X1-*-closure.json`。")

    return "\n".join(out) + "\n"


def merge_groups_tsv(rows: list[dict]) -> str:
    """去重组总表。与主臂 `merge_groups.tsv` 同列，便于两臂对读。"""
    by: dict[str, list[dict]] = collections.defaultdict(list)
    for r in rows:
        by[r["merge_key"]].append(r)
    lines = ["\t".join(("merge_key", "verdict", "subclass", "pair", "成员数",
                        "成员簇", "累计格次", "merge_reason"))]
    for key in sorted(by, key=lambda k: (-len(by[k]), k)):
        g = by[key]
        lines.append("\t".join((
            key, g[0]["verdict"], g[0]["subclass"], g[0]["_pair"], str(len(g)),
            " ".join(r["cluster"] for r in g),
            str(sum(int(r["cells_of_6"]) for r in g)),
            g[0]["merge_reason"].replace("\t", " ").replace("\n", " "),
        )))
    return "\n".join(lines) + "\n"


def evidence_md(rows: list[dict]) -> str:
    """逐簇判据。⚠️ 由 jsonl 生成，⛔ 直接编辑本文件会在下次重建时静默丢失。"""
    out = ["# X1 多报侧逐簇判据（全 %d 条）\n" % len(rows)]
    out.append("⚠️ **本文件由 `unexpected_verdicts/X1-*.jsonl` 生成**"
               "（[../../analysis/rebuild_unexpected_x1.py](../../analysis/rebuild_unexpected_x1.py)），"
               "jsonl 是真源。改裁定请改 jsonl 再跑重建。\n")
    out.append("⭐ **判事实的基准是作者源 `stm0.puml`**（X1 的输入 `plantuml.puml` 与它逐字节相同），"
               "⛔ 不是编译产物 `model.fcstm`。\n")
    by_pair: dict[str, list[dict]] = collections.defaultdict(list)
    for r in rows:
        by_pair[r["_pair"]].append(r)
    for pair in sorted(by_pair):
        g = sorted(by_pair[pair], key=lambda r: int(r["cluster"].split("-")[1]))
        tally = collections.Counter(LABEL[r["verdict"]] for r in g)
        out.append("\n## pair %s — %d 簇　%s\n" % (
            pair, len(g), "　".join(f"{k}×{v}" for k, v in tally.most_common())))
        for r in g:
            out.append("**%s** ｜ %s ｜ `%s` ｜ %s/6 格 ｜ %s\n" % (
                r["cluster"], LABEL[r["verdict"]], r["subclass"], r["cells_of_6"], r["_group"]))
            out.append("- **主张**：%s" % r.get("claim", "—"))
            out.append("- **事实**：%s" % r["fact"])
            out.append("- **NL**：%s" % r["nl"])
            out.append("- **去重**：`%s` —— %s" % (r["merge_key"], r["merge_reason"]))
            out.append("- **成员**：%s\n" % " ".join(r.get("members") or []))
    return "\n".join(out) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="只校验，不写盘")
    args = parser.parse_args()

    rows = load()
    text = build(rows)
    target = RESULTS / "unexpected_verdicts" / "tables.md"
    if args.check:
        if not target.is_file() or target.read_text(encoding="utf-8") != text:
            print("⛔ tables.md 与真源不一致，请重跑本脚本", file=sys.stderr)
            raise SystemExit(1)
        print("✅ tables.md 与真源一致")
        return
    target.write_text(text, encoding="utf-8")
    (VERDICTS / "merge_groups.tsv").write_text(merge_groups_tsv(rows), encoding="utf-8")
    (VERDICTS / "evidence.md").write_text(evidence_md(rows), encoding="utf-8")
    print(f"写出 {target}、merge_groups.tsv、evidence.md")
    counts = collections.Counter(r["verdict"] for r in rows)
    for v in ORDER:
        sub = [r for r in rows if r["verdict"] == v]
        print(f"  {LABEL[v]:<12} {counts[v]:>4} 条目 / {len({r['merge_key'] for r in sub}):>3} 去重")
    print(f"  {'合计':<12} {len(rows):>4} 条目 / {len({r['merge_key'] for r in rows}):>3} 去重")


if __name__ == "__main__":
    main()
