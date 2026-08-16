"""把 v46r 的六个 pair **整块替换**进 v46 结果，而不是打补丁。

## 为什么必须是整块替换

那六个 pair 的 v46 结果产自一份含语料原句的 prompt，该句同时是其中一份制品里的事件声明名。
受影响的位不能挑着改：一格里的判定彼此依赖（同一份产出支撑多条记录），只换「看起来受影响」
的几位会得到一个既非 v46 也非 v46r 的混合体，而它对应不上任何一次真实运行。

所以本脚本的契约是：

1. **覆盖侧**：这六个 pair 的全部台账记录，其 `v46_tiers` 判定位与 `v46_human` 逐位条目
   **先全删再全写**。删不掉说明范围算错了，直接报错。
2. **多报侧**：这六个 pair 在 `G*.jsonl` 里的全部簇**先全删再全写**。
3. 其余 48 个 pair 一个字节都不动。
4. 替换前后各打印一次两侧数字，两套都必须出现在报告里。

⛔ 不提供「只换某几位」的入口。要那个的时候，说明该重新想清楚替换范围。

用法::

    apply_v46r.py --tiers v46r_tiers.json --human v46r_human.json \\
                  --clusters v46r_clusters.jsonl [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

# ⚠️ 2026-08-17 归档：本文件原在 `discover_matrix/` 顶层，`HERE` 即指那一层；
# ⛔ 归档到 `archive/r10_ledger_v1_and_v46/scripts/` 后深度多了两层，`HERE / "manual_review"`
# 会解析到不存在的 `scripts/manual_review`。⭐ 故改为指向归档根（它保留了原 discover_matrix
# 的内部布局：manual_review/ · v46/ · verdicts/ …），⛔ 不数层数、按目录名锚定。
_F = pathlib.Path(__file__).resolve()
HERE = next(p for p in _F.parents if p.name == "r10_ledger_v1_and_v46")
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

#: 受影响的 NL 家族。判据只读 `nl.txt`，与运行结果无关。
PAIRS = ("0000", "0010", "0020", "0030", "0040", "0050")

TIERS = HERE / "v46" / "verdicts" / "v46_tiers.json"
HUMAN = HERE / "v46" / "verdicts" / "v46_human.json"
VERDICTS = HERE / "v46" / "unexpected_verdicts"


def _in_scope(record_id: str) -> bool:
    """`EIS-0010-04` -> pair `0010`。"""

    parts = record_id.split("-")
    return len(parts) >= 2 and parts[1] in PAIRS


def metrics(verdicts: dict) -> dict:
    import metrics_at_k as mk

    reportable = set(mk.REPORTABLE)
    n1 = d1 = h3 = ha = den = 0
    for rid, arms in verdicts.items():
        if rid not in reportable:
            continue
        for key, values in arms.items():
            if key == "direction":
                continue
            den += 1
            d1 += len(values)
            n1 += sum(1 for v in values if v == 1)
            h3 += any(v == 1 for v in values)
            ha += all(v == 1 for v in values)
    return {"hit@1": (n1, d1), "hit@3": (h3, den), "hit@all": (ha, den)}


def show(tag: str, m: dict) -> None:
    print(f"  {tag:8}", end="")
    for k in ("hit@1", "hit@3", "hit@all"):
        num, den = m[k]
        print(f"  {k} {num}/{den} = {num / den:.1%}", end="")
    print()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--tiers", required=True, type=pathlib.Path,
                        help="v46r 的判定表：{record: {claude: [...], gpt: [...]}}")
    parser.add_argument("--human", required=True, type=pathlib.Path,
                        help="v46r 的逐位人工判定：{'REC|run/cell': {...}}")
    parser.add_argument("--clusters", required=True, type=pathlib.Path,
                        help="v46r 的多报侧裁定 jsonl，字段同 G*.jsonl")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    payload = json.loads(TIERS.read_text())
    verdicts: dict = payload["verdicts"]
    before = metrics(verdicts)

    new_tiers = json.loads(args.tiers.read_text())
    out_of_scope = [r for r in new_tiers if not _in_scope(r)]
    if out_of_scope:
        raise SystemExit(f"v46r 判定表里有不属于这六个 pair 的记录：{out_of_scope}")

    # ---- 覆盖侧：先全删，再全写 ----
    dropped = [r for r in list(verdicts) if _in_scope(r)]
    missing = sorted(set(dropped) - set(new_tiers))
    if missing:
        raise SystemExit(
            f"v46 里这 {len(missing)} 条记录属于替换范围，v46r 却没给出判定：{missing}。"
            "整块替换不允许留空——少一条就是更改分母"
        )
    for rid in dropped:
        del verdicts[rid]
    verdicts.update(new_tiers)

    human = json.loads(HUMAN.read_text())
    human = {k: v for k, v in human.items() if not _in_scope(k.split("|")[0])}
    human.update(json.loads(args.human.read_text()))

    after = metrics(verdicts)

    # ---- 多报侧：先全删，再全写 ----
    new_clusters = [json.loads(line) for line in
                    args.clusters.read_text().splitlines() if line.strip()]
    bad = [c["cluster"] for c in new_clusters if c["cluster"][:4] not in PAIRS]
    if bad:
        raise SystemExit(f"v46r 簇里有不属于这六个 pair 的：{bad}")
    removed = 0
    rewritten: dict[pathlib.Path, list[str]] = {}
    for path in sorted(VERDICTS.glob("G*.jsonl")):
        keep = []
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            if record["cluster"][:4] in PAIRS:
                removed += 1
                continue
            keep.append(line)
        rewritten[path] = keep

    print(f"替换范围：覆盖侧 {len(dropped)} 条记录 / {len(dropped) * 6} 位"
          f"｜多报侧删 {removed} 簇、写 {len(new_clusters)} 簇")
    print("\n变更前后双份数字（两套都必须出现在报告里）：")
    show("v46", before)
    show("v46r", after)
    print("  净变化：", end="")
    for k in ("hit@1", "hit@3", "hit@all"):
        b, a = before[k], after[k]
        print(f"  {k} {(a[0] / a[1] - b[0] / b[1]) * 100:+.1f}pp", end="")
    print()

    if args.dry_run:
        print("\n--dry-run，未写盘")
        return 0

    TIERS.write_text(json.dumps(payload, ensure_ascii=False, indent=1))
    HUMAN.write_text(json.dumps(human, ensure_ascii=False, indent=1))
    for path, keep in rewritten.items():
        path.write_text("\n".join(keep) + ("\n" if keep else ""))
    target = VERDICTS / "G9.jsonl"
    target.write_text("\n".join(json.dumps(c, ensure_ascii=False) for c in new_clusters) + "\n")
    print(f"\n✅ 已写入 {TIERS.name} / {HUMAN.name} / G1–G8 与 {target.name}")
    print("⚠️ 还要跑 `python3 rebuild_unexpected.py` 重建全部派生物")
    return 0


if __name__ == "__main__":
    sys.exit(main())
