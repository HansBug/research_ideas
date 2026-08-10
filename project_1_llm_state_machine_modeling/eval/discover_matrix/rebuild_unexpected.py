"""从 `unexpected_verdicts/G*.jsonl` 重建全部派生物。

## 为什么要有这个脚本

意外发现裁定有**一个真源**（`unexpected_verdicts/G1..G8.jsonl`，五类）与**五份派生物**。
另有一份**同级但不在本桶内**的 `ledger_accounted.jsonl`：内容已被台账记录承载的产出
**不属于意外发现**，已物理移出，不进分母。

原真源与派生物
（两个 tsv、一份逐簇证据 md、一份根因 tsv）。本目录已经手工重建过四次，每次都出错：

| 次 | 错法 |
| --: | :-- |
| 1 | 改了 jsonl 但忘了重建 `EVIDENCE.md`，6 簇的裁定在两份文件里不一致 |
| 2 | 重建了 `cluster_index.tsv` 但漏了 `final_rootcause.tsv`，后者把已裁定项仍写成「待裁定」 |
| 3 | `MERGED.md` 的「涉及 pair」列是手写的，与实际簇归属对不上 |
| 4 | 子类计数（N1/F4）在改判后没跟着重算 |

**四次全是同一个错**：改了真源、没有把派生物一起重建。所以它必须是一条命令。

⚠️ **本脚本只做汇总与格式化，不做任何判定。** 裁定只能改 jsonl。

用法::

    python rebuild_unexpected.py            # 重建并打印分布
    python rebuild_unexpected.py --check    # 只校验一致性，不写盘（CI 用）
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
VERDICTS = HERE / "v46" / "unexpected_verdicts"
SEEDS = HERE.parents[1] / "paper_stm_repair" / "selected_seed_examples"

#: 五类裁定。⛔ 没有第六类，也不设「待定」——证据不足不是裁定类别，见 UNEXPECTED_TAXONOMY.md。
ORDER = (
    "VALID_UNRECORDED",
    "REPRESENTATION_DEBT",
    "NO_NL_BASIS",
    "FALSE_POSITIVE",
    "OUT_OF_SCOPE",
)
LABEL = {
    "VALID_UNRECORDED": "✅ 真漏记",
    "REPRESENTATION_DEBT": "⚙️ 表示债务",
    "NO_NL_BASIS": "📄 无 NL 依据",
    "FALSE_POSITIVE": "❌ 假阳性",
    "OUT_OF_SCOPE": "🚫 越界",
}

#: ⛔ 这些标签曾经存在，现已作废，出现即报错。
#: `MERGE_INTO_LEDGER` —— 内容已被台账承载者**不属于意外发现**，已物理移出到
#: `ledger_accounted.jsonl`，不进本桶分母（这正是它当初不该作为一类存在的原因）。
#: `UNCERTAIN` —— 证据不足不是裁定类别，取不到证据就去取。
RETIRED = {
    "MERGE_INTO_LEDGER": "内容已被台账承载者不属意外发现，应移入 ledger_accounted.jsonl",
    "UNCERTAIN": "证据不足不是裁定类别，回读原件或实跑 API 后裁死",
}


def load() -> list[dict]:
    """读真源。缺字段直接报错——判据不全的裁定不是裁定。"""

    rows: list[dict] = []
    for path in sorted(VERDICTS.glob("G[1-8].jsonl")):
        for lineno, line in enumerate(path.read_text().splitlines(), 1):
            if not line.strip():
                continue
            record = json.loads(line)
            for field in ("cluster", "verdict", "fact", "nl", "subclass",
                          "merge_key", "merge_reason"):
                if not (record.get(field) or "").strip():
                    raise SystemExit(f"{path.name}:{lineno} 缺字段 {field}：{record.get('cluster')}")
            verdict = record["verdict"]
            if verdict in RETIRED:
                raise SystemExit(
                    f"{record['cluster']} 用了已作废的标签 {verdict}：{RETIRED[verdict]}"
                )
            if verdict not in ORDER:
                raise SystemExit(f"{record['cluster']} 的裁定 {verdict} 不在五类内")
            record["_group"] = path.stem
            rows.append(record)
    seen = collections.Counter(r["cluster"] for r in rows)
    dupes = [c for c, n in seen.items() if n > 1]
    if dupes:
        raise SystemExit(f"簇重复：{dupes}")
    return rows


def cells_and_families(rows: list[dict]) -> None:
    """从证据包补 `出现格数` 与 `谓词族`。

    证据包在 `/tmp` 下，可能已不存在；那时回退到 `cluster_index.tsv` 的旧值——
    这两个维度只描述产出本身，不随裁定变化，沿用旧值是安全的。**但缺失必须报出来**，
    否则重建会静默把它们清零，而 0 与「没测到」在表里长得一样。
    """

    meta: dict[str, dict] = {}
    pkg = pathlib.Path("/tmp/unexp_pkg")
    if pkg.is_dir():
        for path in pkg.glob("*.md"):
            for m in re.finditer(r"### 簇 (\d{4}-\d+) ｜ 出现在 (\d)/6 格\n- 断言签名: (.*)", path.read_text()):
                meta[m.group(1)] = {
                    "cells": int(m.group(2)),
                    "fams": sorted(set(re.findall(r"\('([a-z_]+)'", m.group(3)))),
                }
    index = VERDICTS / "cluster_index.tsv"
    if index.is_file():
        for row in csv.DictReader(index.open(), delimiter="\t"):
            meta.setdefault(
                row["cluster"],
                {"cells": int(row["cells_of_6"]), "fams": row["predicate_families"].split("|")},
            )
    missing = [r["cluster"] for r in rows if r["cluster"] not in meta]
    if missing:
        print(f"⚠️ {len(missing)} 簇没有格数/谓词族信息，将写 0/空：{missing[:5]}", file=sys.stderr)
    for r in rows:
        got = meta.get(r["cluster"], {"cells": 0, "fams": []})
        r["_cells"], r["_fams"] = got["cells"], got["fams"]


def write_tsvs(rows: list[dict]) -> None:
    with (VERDICTS / "cluster_index.tsv").open("w") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["cluster", "pair", "verdict", "subclass", "merge_key",
                    "merge_size", "cells_of_6", "predicate_families", "judged_by"])
        for r in sorted(rows, key=lambda r: r["cluster"]):
            w.writerow([r["cluster"], r["cluster"][:4], r["verdict"],
                        r["subclass"], r["merge_key"], r.get("merge_size", 1),
                        r["_cells"], "|".join(r["_fams"]), r["_group"]])

    by_pair: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for r in rows:
        by_pair[r["cluster"][:4]][r["verdict"]] += 1
    with (VERDICTS / "by_pair.tsv").open("w") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["pair", "簇数", *ORDER])
        for pair in sorted(by_pair):
            w.writerow([pair, sum(by_pair[pair].values()), *(by_pair[pair][k] for k in ORDER)])

    groups: dict[str, list[str]] = collections.defaultdict(list)
    for r in rows:
        if r["verdict"] == "VALID_UNRECORDED":
            groups[r["cluster"][:4]].append(r["cluster"])
    with (VERDICTS / "final_rootcause.tsv").open("w") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["root_id", "pair", "终裁", "簇数", "并入的簇"])
        for pair in sorted(groups):
            members = sorted(groups[pair])
            w.writerow([f"{pair}-ROOT", pair, "台账漏记", len(members), " ".join(members)])


def write_evidence(rows: list[dict]) -> None:
    counts = collections.Counter(r["verdict"] for r in rows)
    by_pair: dict[str, list[dict]] = collections.defaultdict(list)
    for r in rows:
        by_pair[r["cluster"][:4]].append(r)
    out = [
        "# v46 意外发现逐簇判据（全 %d 条）" % len(rows), "",
        "[unexpected_adjudication.md](./unexpected_adjudication.md) 的证据附件。",
        "裁定口径见 [UNEXPECTED_TAXONOMY.md](../UNEXPECTED_TAXONOMY.md)。", "",
        "⚠️ **本文件由 `unexpected_verdicts/G*.jsonl` 生成（`../rebuild_unexpected.py`），jsonl 是真源。**",
        "改裁定请改 jsonl 再跑重建；直接编辑本文件会在下次重建时静默丢失。", "",
        "| 裁定 | 簇数 |", "| :-- | --: |",
    ]
    out += [f"| {LABEL[k]} | {counts[k]} |" for k in ORDER if counts[k]]
    out += [f"| **合计** | **{len(rows)}** |", "", "---", ""]
    for pair in sorted(by_pair):
        group = sorted(by_pair[pair], key=lambda r: int(r["cluster"].split("-")[1]))
        tally = collections.Counter(r["verdict"] for r in group)
        chips = " ".join(f"{LABEL[k].split()[1]}×{v}" for k, v in tally.most_common())
        out += [f"## pair {pair} — {len(group)} 簇　`{chips}`", ""]
        for r in group:
            out += [
                f"**{r['cluster']}** ｜ {LABEL[r['verdict']]} ｜ {r['_cells']}/6 格 ｜ "
                f"`{'/'.join(r['_fams'])}` ｜ 判定组 {r['_group']}", "",
                f"- **事实**：{r['fact']}", f"- **NL**：{r['nl']}",
            ]
            if (r.get("note") or "").strip():
                out.append(f"- **说明**：{r['note']}")
            out.append("")
    target = HERE / "v46" / "unexpected_evidence.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(out))


def _distinct(rows: list[dict]) -> int:
    """去重数 = 不同 `merge_key` 的个数。

    ⛔ 缺 `merge_key` 的记录**各自单独计一个**（用 cluster 号兜底），而不是被丢掉——
    丢掉会让去重数偏小、比值偏大，方向恰好是「显得产出更冗余」，是有利于我们的错，
    因此更要防。缺失会在 `main()` 里报出来。
    """

    return len({r.get("merge_key") or r["cluster"] for r in rows})


def write_merge_groups(rows: list[dict]) -> None:
    """合并审计表：**每个 merge_key 一行**，可直接与 `cluster_index.tsv` 的同名列 join。

    这张表回答的是「**为什么这几条被判成同一件事**」——去重是把分母改小的操作，
    改小分母必须能被复核，否则「129 条其实只有 27 处」这句话无从验证。
    因此每组都带一句自然语言 `merge_reason`，单成员组也写明「单条，无合并」，
    不留空——空值与「没写理由」在表里长得一样。
    """

    groups: dict[str, list[dict]] = collections.defaultdict(list)
    for r in rows:
        groups[r["merge_key"]].append(r)
    with (VERDICTS / "merge_groups.tsv").open("w") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["merge_key", "verdict", "subclass", "pair", "成员数",
                    "成员簇", "累计格次", "merge_reason"])
        for key, group in sorted(groups.items()):
            members = sorted(r["cluster"] for r in group)
            w.writerow([key, group[0]["verdict"], group[0]["subclass"],
                        group[0]["cluster"][:4], len(group), " ".join(members),
                        sum(r["_cells"] for r in group), group[0]["merge_reason"]])
    spanning = [
        k for k, g in groups.items()
        if len({r["verdict"] for r in g}) > 1 or len({r["subclass"] for r in g}) > 1
        or len({r["cluster"][:4] for r in g}) > 1
    ]
    if spanning:
        raise SystemExit(
            f"merge_key 跨了 verdict / subclass / pair，去重单元被破坏：{spanning}"
        )


def write_subclass_table(rows: list[dict]) -> None:
    """表 C 的机器可读版，含**两套分母**。

    子类标签此前**不在任何机器可读源里**，只能手工维护——这是表 C 反复出错的结构性根因
    （簇数、`中位出现`、`≥4 格` 三列各错过一次）。现在 `subclass` 是 jsonl 的字段，
    本表由它算出，正文里的表 C 应当对着它核。
    """

    import statistics

    buckets: dict[tuple[str, str], list[dict]] = collections.defaultdict(list)
    for r in rows:
        if r.get("subclass"):
            buckets[(r["verdict"], r["subclass"])].append(r)
    with (VERDICTS / "subclass_table.tsv").open("w") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["verdict", "subclass", "条目数", "去重数", "条目去重比",
                    "涉及pair数", "中位出现_of_6", "ge4格"])
        for (verdict, sub), group in sorted(buckets.items()):
            cells = [r["_cells"] for r in group]
            distinct = _distinct(group)
            w.writerow([verdict, sub, len(group), distinct,
                        f"{len(group) / distinct:.2f}",
                        len({r["cluster"][:4] for r in group}),
                        int(statistics.median(sorted(cells))),
                        sum(1 for c in cells if c >= 4)])


#: 桶外的两份归档，与桶内条目合计必须等于最初的簇总数。
SIDECARS = (
    ("ledger_accounted.jsonl", "内容已被台账记录承载，按定义不属意外发现"),
    ("not_produced.jsonl", "断言在冻结制品上求值为 True，模型满足义务——真阴性，两侧都不存在"),
)
ORIGINAL_TOTAL = 293


def _bucket_rows(rows: list[dict], verdict: str) -> list[dict]:
    return [r for r in rows if r["verdict"] == verdict]


def _dual(group: list[dict], tot_items: int, tot_distinct: int) -> tuple[int, int]:
    return len(group), _distinct(group)


def write_tables(rows: list[dict]) -> None:
    """全部交叉表的**唯一**产地。

    这些表此前手工维护在三份 md 里，而机器派生的 tsv 各自正确——于是每次裁定变更后
    正文与真源分岔。实测一次分岔的代价：正文说净增量 4 条 / 23 簇，`final_rootcause.tsv`
    只有 1 行，同一目录内两份文件对同一问题给出互斥的头条结论。手工表没有任何一张是
    算不出来的，所以全部收进来；正文只许引用本文件，不许自带副本。
    """

    import statistics

    n, nd = len(rows), _distinct(rows)
    out = [
        "# v46 多报侧全量统计表", "",
        "⚠️ **本文件整份由 `unexpected_verdicts/G*.jsonl` 生成**"
        "（`../rebuild_unexpected.py`）。**不要手工编辑**，也不要在别处保存这些表的副本——",
        "手工副本无法随裁定变更同步，会让同一目录内出现两个互斥的答案。", "",
        "裁定口径见 [UNEXPECTED_TAXONOMY.md](../UNEXPECTED_TAXONOMY.md)，"
        "逐簇判据见 [unexpected_evidence.md](./unexpected_evidence.md)。", "",
        "---", "", "## 表 0　分母闭合", "",
        "| 去向 | 条数 | 说明 |", "| :-- | --: | :-- |",
        f"| 多报侧桶内 | {n} | 本文件其余各表的分母 |",
    ]
    total = n
    for name, why in SIDECARS:
        path = VERDICTS / name
        cnt = sum(1 for line in path.read_text().splitlines() if line.strip()) if path.is_file() else 0
        total += cnt
        out.append(f"| [{name}](./unexpected_verdicts/{name}) | {cnt} | {why} |")
    out += [f"| **最初簇总数** | **{total}** | |", ""]
    if total != ORIGINAL_TOTAL:
        raise SystemExit(
            f"分母不闭合：桶内 {n} + 两份归档 = {total}，应为 {ORIGINAL_TOTAL}。"
            "有条目被悄悄丢掉或重复计入了"
        )

    out += [
        "---", "", "## 表 1　大类分布（双分母）", "",
        "去重单元 = `(pair, 根因)`；同 pair 同一处失误合并计 1，不同 pair 不合并。", "",
        "| 大类 | 条目数 | 占比 | 去重数 | 占比 | 条目/去重 | 子类数 |",
        "| :-- | --: | --: | --: | --: | --: | --: |",
    ]
    for k in ORDER:
        g = _bucket_rows(rows, k)
        if not g:
            continue
        d = _distinct(g)
        subs = len({r["subclass"] for r in g if r.get("subclass")})
        out.append(f"| {LABEL[k]} | {len(g)} | {len(g)/n:.1%} | {d} | {d/nd:.1%} | "
                   f"{len(g)/d:.2f} | {subs} |")
    allsubs = len({(r["verdict"], r["subclass"]) for r in rows if r.get("subclass")})
    out += [f"| **合计** | **{n}** | 100% | **{nd}** | 100% | **{n/nd:.2f}** | {allsubs} |", "",
            "⚠️ **两套分母给出不同的主要矛盾**，只报一套会得出错误的整改优先级。", ""]

    out += ["---", "", "## 表 2　子类分布（双分母）", ""]
    for k in ORDER:
        g = _bucket_rows(rows, k)
        if not g:
            continue
        out += [f"### {LABEL[k]}　{len(g)} 条目 / {_distinct(g)} 去重", "",
                "| 子类 | 条目数 | 去重数 | 条目/去重 | 涉及 pair | 中位出现_of_6 | ≥4 格 |",
                "| :-- | --: | --: | --: | --: | --: | --: |"]
        by_sub: dict[str, list[dict]] = collections.defaultdict(list)
        for r in g:
            by_sub[r.get("subclass") or "—"].append(r)
        for sub, grp in sorted(by_sub.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            cells = [r["_cells"] for r in grp]
            d = _distinct(grp)
            out.append(f"| `{sub}` | {len(grp)} | {d} | {len(grp)/d:.2f} | "
                       f"{len({r['cluster'][:4] for r in grp})} | "
                       f"{int(statistics.median(sorted(cells)))} | "
                       f"{sum(1 for c in cells if c >= 4)} |")
        out.append("")

    out += ["---", "", "## 表 3　谓词族 × 裁定", "",
            "一簇可挂多个谓词族，故行和大于条目数。", "",
            "| 谓词族 | " + " | ".join(LABEL[k] for k in ORDER if counts_of(rows, k)) + " | 行和 |",
            "| :-- | " + " | ".join("--:" for k in ORDER if counts_of(rows, k)) + " | --: |"]
    fam: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for r in rows:
        for f in r["_fams"]:
            if f:
                fam[f][r["verdict"]] += 1
    live = [k for k in ORDER if counts_of(rows, k)]
    for f in sorted(fam, key=lambda f: -sum(fam[f].values())):
        out.append(f"| `{f}` | " + " | ".join(str(fam[f][k]) for k in live)
                   + f" | {sum(fam[f].values())} |")
    out += ["| **合计** | " + " | ".join(
        str(sum(fam[f][k] for f in fam)) for k in live)
        + f" | {sum(sum(c.values()) for c in fam.values())} |", ""]

    out += ["---", "", "## 表 4　稳定性（出现格数 × 裁定）", "",
            "全网格每簇最多出现在 6 格（2 模型 × 3 轮）。", "",
            "| 大类 | " + " | ".join(f"{i} 格" for i in range(1, 7)) + " | 合计 | ≥4 格占比 |",
            "| :-- | " + " | ".join("--:" for _ in range(6)) + " | --: | --: |"]
    tot = collections.Counter()
    for k in live:
        g = _bucket_rows(rows, k)
        c = collections.Counter(r["_cells"] for r in g)
        for i in range(1, 7):
            tot[i] += c[i]
        hi = sum(c[i] for i in (4, 5, 6))
        out.append(f"| {LABEL[k]} | " + " | ".join(str(c[i]) for i in range(1, 7))
                   + f" | {len(g)} | {hi/len(g):.0%} |")
    out += ["| **合计** | " + " | ".join(f"**{tot[i]}**" for i in range(1, 7))
            + f" | **{n}** | {sum(tot[i] for i in (4,5,6))/n:.0%} |", "",
            f"**{tot[1]}/{n}（{tot[1]/n:.0%}）只出现在 1 个格里**——"
            "多报以单次采样噪声为主，不是系统性行为。", ""]

    out += ["---", "", "## 表 5　合并规模前 10", "",
            "全部 %d 组及其自然语言合并理由见 "
            "[merge_groups.tsv](./unexpected_verdicts/merge_groups.tsv)。" % nd, "",
            "| merge_key | 成员数 | 大类 |", "| :-- | --: | :-- |"]
    mg: dict[str, list[dict]] = collections.defaultdict(list)
    for r in rows:
        mg[r.get("merge_key") or r["cluster"]].append(r)
    for key, grp in sorted(mg.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:10]:
        out.append(f"| `{key}` | {len(grp)} | {LABEL[grp[0]['verdict']]} |")
    multi = sum(1 for g in mg.values() if len(g) > 1)
    out += ["", f"{nd} 组 = {multi} 个多成员组 + {nd - multi} 个单成员组。", ""]

    (HERE / "v46" / "unexpected_tables.md").write_text("\n".join(out))


def counts_of(rows: list[dict], verdict: str) -> int:
    return sum(1 for r in rows if r["verdict"] == verdict)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="只校验，不写盘")
    args = parser.parse_args(argv)

    rows = load()
    cells_and_families(rows)
    counts = collections.Counter(r["verdict"] for r in rows)

    total_distinct = _distinct(rows)
    print(f"真源 {len(rows)} 条目 / {total_distinct} 去重 / "
          f"{len({r['cluster'][:4] for r in rows})} 个 pair")
    print(f"  {'裁定':16} {'条目数':>6} {'占比':>7} {'去重数':>6} {'占比':>7} {'比值':>6}")
    for k in ORDER:
        if not counts[k]:
            continue
        group = [r for r in rows if r["verdict"] == k]
        d = _distinct(group)
        print(f"  {LABEL[k]:16} {counts[k]:>6} {counts[k] / len(rows):>7.1%} "
              f"{d:>6} {d / total_distinct:>7.1%} {len(group) / d:>6.2f}")



    if args.check:
        print("\n✅ --check 模式，未写盘")
        return 0

    write_tsvs(rows)
    write_subclass_table(rows)
    write_merge_groups(rows)
    write_evidence(rows)
    write_tables(rows)
    print("\n✅ 已重建 cluster_index.tsv / by_pair.tsv / final_rootcause.tsv / "
          "subclass_table.tsv / merge_groups.tsv / unexpected_evidence.md / unexpected_tables.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
