"""把盲判结果与原判定对齐，算一致性、偏倚方向，以及**双报**的 hit@k。

## 为什么要成为固定环节而不是一次性补救

40 单元抽样盲判暴露的不是「某一条判错了」，而是**判据在不同带上的严格程度不一致**：原判在调优带
与烧毁带更宽松（净偏 +3 / +8），在可报带更严格（净偏 −3）。两个方向都抬高共演化溢价。

这与上一代次发布时被抓到的「『有据』判据比『未命中』判据松」是同一类问题在**反方向**上的复发。
一次性补救修不掉它，因为**没有盲判就无法自查** —— 判定者知道哪格是调优格，这个信息进不了任何
自动检查。

## 三件本工具必须同时给出的

1. **一致性**：Cohen $\kappa$ 与原始一致率。κ 而非一致率单独用，因为两个都倾向判 0 的判定者会有
   很高的一致率而没有任何可靠性。
2. **偏倚是否与带相关**。这是**唯一**能检出暴露偏倚的检验：若分歧在各带上对称，不盲不构成问题；
   若不对称，原判定的数字方向可疑。
3. **双报的 hit@k**：原判定值与盲判值并列，且**不得只给一个**。§3.5 条款 4 的构成要件是「更改
   分母或判据**且**未双报」—— 双报是它的解药，不是修饰。

## 一条不能省的纪律

盲判值高于原判定时，**不得单方面采纳**。三条判据：

- 覆盖是否完整（部分覆盖 + 有利方向 = 在样本内挑选，与迁就结果不可区分）
- 偏倚是否单向（双向偏倚意味着全面重判的净方向未知）
- 采纳后是否恰好越过某条目标线（若是，举证责任在提出者）

`--adopt` 才会把盲判写成新判定表，且要求 `--coverage-complete`；缺省只报，不改。
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


def _load_blind(path: pathlib.Path) -> dict[str, list]:
    """接受两种形态：裸 `{U001: [1,0,1]}`，或带 `blind_verdicts` 包装的。"""

    payload = json.loads(path.read_text())
    if "blind_verdicts" in payload:
        payload = payload["blind_verdicts"]
    out = {}
    for key, value in payload.items():
        if key.startswith("_"):
            continue
        if isinstance(value, list):
            out[key] = value
    if not out:
        raise SystemExit(f"ERROR: no unit verdicts in {path}")
    return out


def _kappa(pairs: list[tuple[int, int]]) -> tuple[float, float, float]:
    n = len(pairs)
    if not n:
        return 0.0, 0.0, 0.0
    agree = sum(1 for a, b in pairs if a == b)
    po = agree / n
    a1 = sum(1 for a, _ in pairs) and sum(1 for a, _ in pairs if a == 1) / n
    b1 = sum(1 for _, b in pairs if b == 1) / n
    pe = a1 * b1 + (1 - a1) * (1 - b1)
    # pe == 1 时 κ 无定义（两个判定者都把每一位判成同一个值）。报 nan 而不是除零。
    kappa = float("nan") if pe >= 1.0 else (po - pe) / (1 - pe)
    return po, pe, kappa


def _hit_at_k(series_by_unit: dict[str, list], units: list[str], rounds: int) -> dict:
    """`rounds` 不是可选的 —— 见 `atall` 那行。

    `all(series)` 在丢掉 `None` 之后回答的是「我观测到的那几轮都命中吗」，不是
    「三轮都命中吗」。一个只跑了两轮、两轮都中的单元会被计成三轮全中：缺测越多
    这个数字越好看，方向恰好是错的。判据必须同时约束元数与谓词。
    """

    hits = triples = at3 = atall = items = 0
    for unit in units:
        series = [x for x in (series_by_unit.get(unit) or []) if x is not None]
        if not series:
            continue
        items += 1
        triples += len(series)
        hits += sum(series)
        at3 += 1 if any(series) else 0
        atall += 1 if len(series) == rounds and all(series) else 0
    if not items:
        return {}
    return {
        "hit@1": f"{hits}/{triples} = {hits / triples * 100:.1f}%",
        "hit@3": f"{at3}/{items} = {at3 / items * 100:.1f}%",
        "hit@all": f"{atall}/{items} = {atall / items * 100:.1f}%",
    }


def analyse(blind_paths: list[pathlib.Path], key_path: pathlib.Path, rounds: int = 3) -> dict:
    blind: dict[str, list] = {}
    for path in blind_paths:
        overlap = set(blind) & set(_load_blind(path))
        if overlap:
            # 两份盲判覆盖同一单元时，静默 update 会让后者悄悄覆盖前者。
            raise SystemExit(f"ERROR: {path} 与已读入的部分重叠：{sorted(overlap)[:5]}")
        blind.update(_load_blind(path))
    key = json.loads(key_path.read_text())
    items = {i["unit_id"]: i for i in key["items"]}

    # `unit_id` 是位置编号，换 `--size` 就换一套映射。首版没有这道检查，于是 40 单元的盲判结果
    # 配 68 单元的 key 算出 κ = −0.2 —— 一个看起来像「判定完全不可靠」的真发现，实为编号错配。
    # 有 `sample_id` 就必须相符；缺失则大声警告而不是静默计算。
    expected = key.get("sample_id")
    declared = {p: json.loads(p.read_text()).get("sample_id") for p in blind_paths}
    if expected:
        wrong = {str(p): d for p, d in declared.items() if d and d != expected}
        if wrong:
            raise SystemExit(
                f"ERROR: sample_id 不符，拒绝计算。key={expected}，盲判文件={wrong}。"
                "换过 --size 或 --seed 就会这样 —— 用同一组参数重建 key，或改用对应的盲判结果。"
            )
        if not any(declared.values()):
            print("⚠️ 盲判文件未声明 sample_id：无法验证它答的是这份 key。"
                  "若 κ 异常低（接近 0 或为负），首先怀疑编号错配，不要先怀疑判定者。",
                  file=sys.stderr)

    missing = [u for u in items if u not in blind]
    coverage = 1.0 - len(missing) / len(items) if items else 0.0

    pairs: list[tuple[int, int]] = []
    by_band: dict[str, list[tuple[int, int]]] = collections.defaultdict(list)
    orig_by_unit: dict[str, list] = {}
    for unit, item in items.items():
        orig = item["original_series"]
        orig_by_unit[unit] = orig
        b = blind.get(unit)
        if b is None:
            continue
        for i, o in enumerate(orig):
            if o is None or i >= len(b) or b[i] is None:
                continue
            pairs.append((o, b[i]))
            by_band[item["band"]].append((o, b[i]))

    po, pe, kappa = _kappa(pairs)
    bands: dict[str, dict] = {}
    for band, sub in sorted(by_band.items()):
        orig_lenient = sum(1 for a, b in sub if a == 1 and b == 0)
        blind_lenient = sum(1 for a, b in sub if a == 0 and b == 1)
        bands[band] = {
            "n": len(sub),
            "orig_more_lenient": orig_lenient,
            "blind_more_lenient": blind_lenient,
            "net": orig_lenient - blind_lenient,
        }
    directions = {v["net"] > 0 for v in bands.values() if v["net"]}
    return {
        "blind_units": len(blind),
        "key_units": len(items),
        "coverage": round(coverage, 3),
        "missing_units": missing,
        "paired_positions": len(pairs),
        "agreement": f"{sum(1 for a, b in pairs if a == b)}/{len(pairs)} = {po * 100:.1f}%",
        "expected_agreement": f"{pe * 100:.1f}%",
        "cohen_kappa": None if kappa != kappa else round(kappa, 3),
        "by_band": bands,
        "bias_is_one_directional": len(directions) <= 1,
        "hit_at_k": {
            band: {
                "as_judged": _hit_at_k(
                    orig_by_unit,
                    [u for u, i in items.items() if i["band"] == band], rounds),
                "blind": _hit_at_k(
                    blind,
                    [u for u, i in items.items() if i["band"] == band and u in blind],
                    rounds),
            }
            for band in sorted({i["band"] for i in items.values()})
        },
        "adoption_gate": {
            "coverage_complete": not missing,
            "bias_one_directional": len(directions) <= 1,
            "note": ("盲判值高于原判定时不得单方面采纳。覆盖不完整 + 有利方向 = 在样本内挑选，"
                     "与「口径迁就结果」在形式上不可区分，即使动机纯正。"),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("blind", nargs="+", type=pathlib.Path,
                        help="一份或多份盲判结果 json（拆份时给多个）")
    parser.add_argument("--key", type=pathlib.Path,
                        default=HERE / "blind_sample" / "key.json")
    parser.add_argument("--rounds", type=int, default=3)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = analyse(args.blind, args.key, args.rounds)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return 0
    print(f"盲判单元 {result['blind_units']} / 台账单元 {result['key_units']}  "
          f"覆盖 {result['coverage'] * 100:.0f}%")
    if result["missing_units"]:
        print(f"  ⚠️ 未覆盖 {len(result['missing_units'])} 个：{result['missing_units'][:8]}")
    print(f"配对判定位 {result['paired_positions']}")
    print(f"  一致 {result['agreement']}   期望一致 {result['expected_agreement']}")
    print(f"  Cohen κ = {result['cohen_kappa']}")
    print("\n偏倚是否与带相关（唯一能检出暴露偏倚的检验）：")
    for band, v in result["by_band"].items():
        print(f"  {band:11s} n={v['n']:3d}  原判更宽松 {v['orig_more_lenient']:2d}  "
              f"盲判更宽松 {v['blind_more_lenient']:2d}  净偏 {v['net']:+3d}")
    print(f"  → 偏倚单向？{'是' if result['bias_is_one_directional'] else '否（净方向未知）'}")
    print("\nhit@k 双报（左=原判定，右=盲判）：")
    for band, v in result["hit_at_k"].items():
        a, b = v["as_judged"], v["blind"]
        if not a and not b:
            continue
        print(f"  {band}")
        for metric in ("hit@1", "hit@3", "hit@all"):
            print(f"    {metric:8s} {a.get(metric, '—'):>18s}   |   {b.get(metric, '—'):>18s}")
    gate = result["adoption_gate"]
    print(f"\n采纳闸门：覆盖完整 {'✅' if gate['coverage_complete'] else '❌'}  "
          f"偏倚单向 {'✅' if gate['bias_one_directional'] else '❌'}")
    print(f"  {gate['note']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
