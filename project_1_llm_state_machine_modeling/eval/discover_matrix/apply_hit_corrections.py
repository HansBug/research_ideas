"""把逐格复核翻转的命中位应用到判定表，并给出变更前后双份 `metric@k`。

## 为什么需要它

`MERGE_INTO_LEDGER` 这一类的存在本身就说明命中侧被低估了：那些产出是模型**确实找到了**、
但匹配器没认出对应哪条台账记录的缺陷。它们掉进了「意外发现」桶，而正确归宿是命中侧。

改命中数字是本仓库代价最大的操作，所以这里定死三条：

1. **只接受显式的 (record, cell, hit) 三元组**，不做任何推断、不做关键词匹配。
   翻转清单由人工逐格裁定产出，本脚本只负责应用与算术。
2. **必须同时打印变更前后两套数字**。只报新数字等于抹掉口径变更，
   [CLAUDE.md](../../../CLAUDE.md) §3.5 把「评测口径迁就结果」列为 C 级。
3. **拒绝把 `False` 翻成 `True` 以外的操作**。本轮的复核方向是单向的（找回被漏配的命中）；
   若某次复核发现应当**下调**，那是另一件事，必须单独走一轮并说明理由——
   混在一起会让人无法判断净变化来自哪一侧。

⚠️ 越界记录（`00x8` 家族与 `EIS-0043-02`）由 `metrics_at_k` 的口径排除，本脚本沿用，
不重新发明分母。

用法::

    apply_hit_corrections.py --flips flips.json --dry-run   # 只看差异
    apply_hit_corrections.py --flips flips.json             # 写盘
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

TIERS = HERE / "v46" / "verdicts" / "v46_tiers.json"
HUMAN = HERE / "v46" / "verdicts" / "v46_human.json"


def out_of_scope() -> set[str]:
    import metrics_at_k as M

    return set(M._out_of_scope_record_ids())


def metrics(verdicts: dict, skip: set[str]) -> dict:
    """`hit@1` / `hit@3` / `hit@all`，口径与 `metrics_at_k` 一致。"""

    n1 = d1 = h3 = ha = den = 0
    for rid, arms in verdicts.items():
        if rid in skip:
            continue
        for values in arms.values():
            d1 += len(values)
            n1 += sum(1 for v in values if v == 1)
            den += 1
            if any(v == 1 for v in values):
                h3 += 1
            if all(v == 1 for v in values):
                ha += 1
    return {"hit@1": (n1, d1), "hit@3": (h3, den), "hit@all": (ha, den)}


def show(tag: str, m: dict) -> None:
    print(f"  {tag:10}", end="")
    for k in ("hit@1", "hit@3", "hit@all"):
        num, den = m[k]
        print(f"  {k} {num}/{den} = {num / den:.1%}", end="")
    print()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--flips", required=True, type=pathlib.Path,
                        help="JSON 列表，每项 {record, cell, hit, argument, equivalence_form}")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    flips = json.loads(args.flips.read_text())
    to_true = [f for f in flips if f.get("hit") is True]
    if len(to_true) != len(flips):
        raise SystemExit("本脚本只接受翻成 True 的修正；下调需单独走一轮并说明理由")

    payload = json.loads(TIERS.read_text())
    rounds: list[str] = payload["rounds"]
    verdicts: dict = payload["verdicts"]
    before = metrics(verdicts, out_of_scope())

    applied, rejected = [], []
    for f in to_true:
        rid, cell = f["record"], f["cell"]
        run, arm = cell.split("/", 1)
        arm = arm.split("-", 1)[1]
        if rid not in verdicts or arm not in verdicts[rid]:
            rejected.append((rid, cell, "记录或臂不在判定表内"))
            continue
        idx = rounds.index(run)
        old = verdicts[rid][arm][idx]
        if old == 1:
            rejected.append((rid, cell, "该位本来就是命中，翻转无意义"))
            continue
        verdicts[rid][arm][idx] = 1
        applied.append((rid, cell, old))

    after = metrics(verdicts, out_of_scope())

    print(f"翻转清单 {len(flips)} 条 ｜ 应用 {len(applied)} ｜ 拒绝 {len(rejected)}")
    for rid, cell, why in rejected:
        print(f"  ⛔ {rid} @ {cell}：{why}")
    print("\n变更前后双份数字（两套都必须出现在报告里）：")
    show("变更前", before)
    show("变更后", after)
    print("\n净变化：", end="")
    for k in ("hit@1", "hit@3", "hit@all"):
        b, a = before[k], after[k]
        print(f"  {k} {(a[0] / a[1] - b[0] / b[1]) * 100:+.1f}pp", end="")
    print()

    if args.dry_run:
        print("\n--dry-run，未写盘")
        return 0

    TIERS.write_text(json.dumps(payload, ensure_ascii=False, indent=1))
    # 人工判定表同步，保持两份文件不打架
    human = json.loads(HUMAN.read_text())
    for f in to_true:
        key = f"{f['record']}|{f['cell']}"
        entry = human.get(key, {})
        entry["hit"] = True
        entry["equivalence_form"] = f.get("equivalence_form") or entry.get("equivalence_form")
        entry["argument"] = f.get("argument") or entry.get("argument")
        entry["recheck"] = "v46 逐格复核翻转：原判未命中系匹配器漏配"
        human[key] = entry
    HUMAN.write_text(json.dumps(human, ensure_ascii=False, indent=1))
    print(f"\n✅ 已写入 {TIERS.name} 与 {HUMAN.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
