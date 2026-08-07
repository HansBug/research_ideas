"""把两位标注者的一次标注结果合流，派生覆盖侧与多报侧，并算 $\\kappa$。

## 为什么两侧能从同一份标注派生

判定单元是 **(格, 轮)**，每条 issue 恰好一个标签。于是：

    覆盖侧  H(记录, 臂, 轮) = 1  ⟺  该 unit 里存在 issue 标 `hits:<该记录>`
    多报侧  over(unit)          = 该 unit 里标 `fabricated` 的条数

**不变量「hit-evidence ∩ 台账外 = ∅」靠构造成立** —— 一条 issue 只有一个标签，它不可能同时进入两个
计数。这与 `check_partition_closure.py` 事后查同一件事的区别是：那里查的是两个匹配器切同一批对象是否
一致（v22 实测 23/82 双计），这里**两侧不再是两个任务**，所以不一致无法表达。

## κ 算在哪一层

两个 κ 都报，因为它们回答不同问题：

| κ | 定义域 | 回答 |
| :-- | :-- | :-- |
| `kappa_label` | 249 条 issue 的**五分类标签** | 标注者对「这条 issue 是什么」是否一致 |
| `kappa_coverage` | 204 个 (记录, 臂, 轮) 位的**二值命中** | 派生出的覆盖判定是否一致 |

后者是前者的粗化，**必然 ≥ 前者** —— 两人可以对「哪条 issue 命中了它」有分歧但同意「它被命中了」。
所以 `kappa_coverage` 高不能替 `kappa_label` 作证；只报前者会高估一致性。

## 分歧处置

`--on-disagree` 与 `blind_to_verdicts.py` 同一套语义：`error`（默认，拒绝合流）/ `conservative`
（分歧记未命中）/ `optimistic`（记命中）/ `null`（记 None，进入 eligibility filter）。

默认 `error` 是有意的：**分歧数应当先被人看到再决定怎么处置**，而不是被一个默认值静默吸收。
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "onepass_sample"
LABELS = ("hits", "grounded-extra", "boundary", "fabricated", "duplicate-of")


def _coarse(label: str) -> str:
    """五分类里 `hits:X` 与 `duplicate-of:Y` 带参数，粗化到标签名本身。"""

    return label.split(":", 1)[0] if ":" in label else label


def _load(path: pathlib.Path, sample_id: str) -> dict:
    payload = json.loads(path.read_text())
    got = payload.get("sample_id")
    if got != sample_id:
        # sample_id 不匹配即拒绝。上一代次正是因为按**位置**配对（`unit_id` 是位置性的，不是
        # 内容寻址的）而把 40 单元的判定对到 68 单元的 key 上，算出 κ = −0.2。
        raise SystemExit(
            f"ERROR: {path.name} 的 sample_id={got!r} 与样本 {sample_id!r} 不符。"
            "拒绝合流 —— 按位置配对不同样本会算出无意义的 κ。"
        )
    return payload


def kappa(pairs: list[tuple[str, str]]) -> dict:
    """多分类 Cohen κ。"""

    if not pairs:
        return {"n": 0, "kappa": None,
                "note": "零输入。空结果与完全一致不可区分，所以这是错误而不是 κ=1"}
    n = len(pairs)
    agree = sum(1 for a, b in pairs if a == b)
    po = agree / n
    ca = collections.Counter(a for a, _ in pairs)
    cb = collections.Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return {
        "n": n,
        "agreement": f"{agree}/{n} = {po * 100:.1f}%",
        "kappa": None if pe >= 1.0 else round((po - pe) / (1 - pe), 3),
        "disagreements": n - agree,
    }


def merge(sample: dict, key: dict, a: dict, b: dict, on_disagree: str) -> dict:
    uids = [i["issue_uid"] for item in sample["items"] for i in item["published_issues"]]
    la, lb = a.get("labels") or {}, b.get("labels") or {}

    missing = {
        "A": [u for u in uids if u not in la],
        "B": [u for u in uids if u not in lb],
    }
    if missing["A"] or missing["B"]:
        # 缺标注不得当成某个默认标签。**零输入不能读成一次干净的检查** —— 本目录反复出现的错误。
        raise SystemExit(
            f"ERROR: 标注不完整。A 缺 {len(missing['A'])} 条，B 缺 {len(missing['B'])} 条"
            f"（共 {len(uids)} 条）。前 5 条 A 缺：{missing['A'][:5]}"
        )

    label_pairs = [(_coarse(la[u]["label"]), _coarse(lb[u]["label"])) for u in uids]

    # ---- 覆盖侧派生 ----
    by_unit = {item["unit_id"]: item for item in sample["items"]}
    key_by_unit = {item["unit_id"]: item for item in key["items"]}
    coverage: dict[tuple[str, str, str], tuple[int | None, int, int]] = {}
    cov_pairs: list[tuple[str, str]] = []
    for unit_id, item in by_unit.items():
        kitem = key_by_unit[unit_id]
        run, arm = kitem["run"], kitem["arm"]
        for alias, meta in kitem["record_aliases"].items():
            ha = any(la[i["issue_uid"]]["label"] == f"hits:{alias}"
                     for i in item["published_issues"])
            hb = any(lb[i["issue_uid"]]["label"] == f"hits:{alias}"
                     for i in item["published_issues"])
            cov_pairs.append(("1" if ha else "0", "1" if hb else "0"))
            if ha == hb:
                value: int | None = 1 if ha else 0
            elif on_disagree == "error":
                value = None
            elif on_disagree == "conservative":
                value = 0
            elif on_disagree == "optimistic":
                value = 1
            else:
                value = None
            coverage[(meta["record_id"], arm, run)] = (value, int(ha), int(hb))

    disagree_cov = sum(1 for x, y in cov_pairs if x != y)
    if on_disagree == "error" and disagree_cov:
        raise SystemExit(
            f"ERROR: 覆盖侧有 {disagree_cov}/{len(cov_pairs)} 个位分歧，而 --on-disagree=error。"
            "分歧数应当先被人看到再决定处置，不要让默认值静默吸收它。"
            "看过之后用 --on-disagree {conservative|optimistic|null} 重跑。"
        )

    # ---- 多报侧派生（不变量靠构造，无需检查）----
    over = collections.Counter()
    for unit_id, item in by_unit.items():
        for i in item["published_issues"]:
            if _coarse(la[i["issue_uid"]]["label"]) == "fabricated":
                over[key_by_unit[unit_id]["arm"]] += 1

    dist = {
        "A": dict(collections.Counter(_coarse(v["label"]) for v in la.values())),
        "B": dict(collections.Counter(_coarse(v["label"]) for v in lb.values())),
    }
    return {
        "sample_id": sample["sample_id"],
        "on_disagree": on_disagree,
        "issue_count": len(uids),
        "kappa_label": kappa(label_pairs),
        "kappa_coverage": kappa(cov_pairs),
        "label_distribution": dist,
        "over_by_arm_A": dict(over),
        "coverage": coverage,
        "_invariant": ("hit-evidence ∩ fabricated = ∅，靠构造成立："
                       "一条 issue 只有一个标签，不可能同时进入两个计数"),
    }


def to_verdicts(merged: dict) -> dict:
    """→ `verdicts/*.json` 的形状，供 `full_tables.py` / `metrics_at_k.py` 直接消费。"""

    series: dict[str, dict[str, dict[int, int | None]]] = collections.defaultdict(
        lambda: collections.defaultdict(dict)
    )
    for (record_id, arm, run), (value, _, _) in merged["coverage"].items():
        series[record_id][arm][int(run[3:]) - 1] = value
    out: dict[str, dict[str, list]] = {}
    for record_id, arms in series.items():
        out[record_id] = {
            arm: [by_run.get(i) for i in range(max(by_run) + 1)]
            for arm, by_run in arms.items()
        }
    return {
        "_source": "onepass_merge.py",
        "sample_id": merged["sample_id"],
        "annotators": ["A", "B"],
        "on_disagree": merged["on_disagree"],
        "kappa_label": merged["kappa_label"].get("kappa"),
        "kappa_coverage": merged["kappa_coverage"].get("kappa"),
        "verdicts": out,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--on-disagree", default="error",
                        choices=("error", "conservative", "optimistic", "null"))
    parser.add_argument("--write-verdicts", type=pathlib.Path)
    args = parser.parse_args(argv)

    sample = json.loads((OUT / "sample.json").read_text())
    key = json.loads((OUT / "key.json").read_text())
    if key.get("sample_id") != sample.get("sample_id"):
        raise SystemExit("ERROR: sample.json 与 key.json 的 sample_id 不符")
    a = _load(OUT / "annotation_A.json", sample["sample_id"])
    b = _load(OUT / "annotation_B.json", sample["sample_id"])

    merged = merge(sample, key, a, b, args.on_disagree)
    print(f"一次标注合流 @ sample_id={merged['sample_id']}  issue {merged['issue_count']} 条")
    for name in ("kappa_label", "kappa_coverage"):
        k = merged[name]
        print(f"  {name:16s} κ={k.get('kappa')}  一致 {k.get('agreement')}  分歧 {k.get('disagreements')}")
    print(f"  标签分布 A: {merged['label_distribution']['A']}")
    print(f"           B: {merged['label_distribution']['B']}")
    print(f"  多报（A 的 fabricated 计数，按臂）: {merged['over_by_arm_A']}")
    print(f"\n⚠️ kappa_coverage 是 kappa_label 的粗化，**必然 ≥** 后者。只报前者会高估一致性。")

    if args.write_verdicts:
        args.write_verdicts.write_text(
            json.dumps(to_verdicts(merged), ensure_ascii=False, indent=1)
        )
        print(f"\n已写 {args.write_verdicts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
