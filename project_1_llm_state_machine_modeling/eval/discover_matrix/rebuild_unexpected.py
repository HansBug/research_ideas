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
VERDICTS = HERE / "unexpected_verdicts"
SEEDS = HERE.parents[1] / "paper_stm_repair" / "selected_seed_examples"

#: 六类裁定。⛔ 没有第七类，也不设「待定」——证据不足不是裁定类别，见 UNEXPECTED_TAXONOMY.md。
ORDER = (
    "VALID_UNRECORDED",
    "REPRESENTATION_DEBT",
    "NO_NL_BASIS",
    "FALSE_POSITIVE",
    "PREDICATE_ARTIFACT",
    "OUT_OF_SCOPE",
)
LABEL = {
    "VALID_UNRECORDED": "✅ 真漏记",
    "REPRESENTATION_DEBT": "⚙️ 表示债务",
    "NO_NL_BASIS": "📄 无 NL 依据",
    "FALSE_POSITIVE": "❌ 假阳性",
    "PREDICATE_ARTIFACT": "🔧 谓词产物",
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
            for field in ("cluster", "verdict", "fact", "nl"):
                if not (record.get(field) or "").strip():
                    raise SystemExit(f"{path.name}:{lineno} 缺字段 {field}：{record.get('cluster')}")
            verdict = record["verdict"]
            if verdict in RETIRED:
                raise SystemExit(
                    f"{record['cluster']} 用了已作废的标签 {verdict}：{RETIRED[verdict]}"
                )
            if verdict not in ORDER:
                raise SystemExit(f"{record['cluster']} 的裁定 {verdict} 不在六类内")
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
                    "cells_of_6", "predicate_families", "judged_by"])
        for r in sorted(rows, key=lambda r: r["cluster"]):
            w.writerow([r["cluster"], r["cluster"][:4], r["verdict"],
                        r.get("subclass", ""), r.get("merge_key", ""), r["_cells"],
                        "|".join(r["_fams"]), r["_group"]])

    by_pair: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for r in rows:
        by_pair[r["cluster"][:4]][r["verdict"]] += 1
    with (VERDICTS / "by_pair.tsv").open("w") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["pair", "簇数", *ORDER])
        for pair in sorted(by_pair):
            w.writerow([pair, sum(by_pair[pair].values()), *(by_pair[pair][k] for k in ORDER)])

    groups: dict[str, dict[str, list[str]]] = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in rows:
        if r["verdict"] in ("VALID_UNRECORDED", "MERGE_INTO_LEDGER"):
            groups[r["verdict"]][r["cluster"][:4]].append(r["cluster"])
    with (VERDICTS / "final_rootcause.tsv").open("w") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["root_id", "pair", "终裁", "簇数", "并入的簇"])
        for verdict, tag in (("VALID_UNRECORDED", "台账漏记"), ("MERGE_INTO_LEDGER", "并入台账")):
            for pair in sorted(groups[verdict]):
                members = sorted(groups[verdict][pair])
                w.writerow([f"{pair}-{'ROOT' if verdict == 'VALID_UNRECORDED' else 'MERGE'}",
                            pair, tag, len(members), " ".join(members)])


def write_evidence(rows: list[dict]) -> None:
    counts = collections.Counter(r["verdict"] for r in rows)
    by_pair: dict[str, list[dict]] = collections.defaultdict(list)
    for r in rows:
        by_pair[r["cluster"][:4]].append(r)
    out = [
        "# v46 意外发现逐簇判据（全 %d 条）" % len(rows), "",
        "[V46_UNEXPECTED_ADJUDICATION.md](./V46_UNEXPECTED_ADJUDICATION.md) 的证据附件。",
        "裁定口径见 [UNEXPECTED_TAXONOMY.md](./UNEXPECTED_TAXONOMY.md)。", "",
        "⚠️ **本文件由 `unexpected_verdicts/G*.jsonl` 生成（`rebuild_unexpected.py`），jsonl 是真源。**",
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
    (HERE / "V46_UNEXPECTED_EVIDENCE.md").write_text("\n".join(out))


def _distinct(rows: list[dict]) -> int:
    """去重数 = 不同 `merge_key` 的个数。

    ⛔ 缺 `merge_key` 的记录**各自单独计一个**（用 cluster 号兜底），而不是被丢掉——
    丢掉会让去重数偏小、比值偏大，方向恰好是「显得产出更冗余」，是有利于我们的错，
    因此更要防。缺失会在 `main()` 里报出来。
    """

    return len({r.get("merge_key") or r["cluster"] for r in rows})


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

    missing_key = [r["cluster"] for r in rows if not r.get("merge_key")]
    if missing_key:
        print(f"\n⚠️ {len(missing_key)} 条缺 merge_key，已各自单独计一个去重单元"
              f"（去重数因此偏大、比值偏小）：{missing_key[:8]}", file=sys.stderr)

    if args.check:
        print("\n✅ --check 模式，未写盘")
        return 0

    write_tsvs(rows)
    write_subclass_table(rows)
    write_evidence(rows)
    print("\n✅ 已重建 cluster_index.tsv / by_pair.tsv / final_rootcause.tsv / subclass_table.tsv / V46_UNEXPECTED_EVIDENCE.md")
    print("⚠️ 正文里的表 A / 表 B / 表 C 与各处叙述数字仍需人工核对——本脚本不改正文。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
