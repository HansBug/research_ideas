"""抽一份**盲判样本**：抹掉 pair id 与调优/留出分组，交独立判定者复判。

## 为什么需要

`holdout.py` 的构造纪律保证了**暴露分组**外生于结果（分组只读仓库历史与制品，从不读运行结果）。
但它管不到**结果判定**：每一条「命中 / 未命中」都是知道这格是调优格还是留出格的同一个人做的。

独立裁决把这一点列为共演化溢价那条主张的两个执行缺陷之一，另一个是混杂未调整。四条判别标准里：

    1. 暴露变量外生于结果        ✅  holdout.py:40
    2. 暴露在观测前冻结          ⚠️  pair 级成立，记录级烧毁不成立
    3. **结果判定对暴露状态盲**   ❌  ← 本工具补的就是这一条
    4. 暴露与结果之外的差异可控   ❌  层构成不同，已用直接标准化处理

条件 3 是四条里**唯一零语料成本**可补的 —— 不需要新 pair、不消耗任何 hold-out 资格。

## 盲化抹掉什么

| 字段 | 处理 | 为什么 |
| :-- | :-- | :-- |
| pair id（`0035` 等） | 替换为 `PAIR-A`…，映射另存 | 四位数字是分组的直接指纹 |
| 台账记录 id（`EIS-0035-02`） | 替换为 `REC-nn` | 同上，且 id 内嵌 pair |
| 模型路径前缀 `llms_emp_feedback_final_0018.` | 替换为 `M.` | 每条 statement 与 issue 里都有 |
| 带（调优 / 已烧毁 / 可报） | **不出现** | 这正是要盲掉的暴露变量 |
| 轮次、臂 | 保留 | 不泄漏分组，且判定需要它们区分重复观测 |

**不抹掉**语义内容 —— 判定的依据必须仍然是 NL、模型文本与台账 statement 的语义同一性，否则复判
的不是同一件事。

## 抽样

固定种子（`--seed`，默认 20260807），按 `(记录, 臂)` 为单元分层抽样：每个带按其占比抽，避免全落在
某一带。默认 40 个判定单元 —— 裁决建议的量，够算 Cohen $\kappa$ 且不至于让复判者疲劳。

**分层用的是带，而抽出来的样本不带带标签** —— 分层保证覆盖，盲化保证判定无偏，两者不矛盾。

## 输出

`blind_sample/` 下两份：

- `sample.json` —— 交给复判者的，无任何分组信息
- `key.json` —— 映射与原判定，**复判者不可见**，只用于事后算一致性

`--verify` 检查 `sample.json` 里是否残留任何四位 pair id、`EIS-` 前缀或带名称；残留即非零退出。
这条检查存在的理由与 `holdout.py --verify` 相同：**盲化不能靠「我记得抹了」**。
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import random
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "blind_sample"
#: 四位 pair id 的任何出现形式，含 `EIS-0035-02` 与 `llms_emp_feedback_final_0035`。
_LEAK = re.compile(r"\b\d{4}\b|EIS-|llms_emp_feedback_final")
_BAND_WORDS = ("调优", "留出", "已烧毁", "可报", "hold-out", "holdout", "tuned", "burned")
TUNED_PAIRS = ("0000", "0006", "0029", "0050")


def _ledger() -> dict[str, dict]:
    payload = json.loads((HERE / "manual_review" / "expected_issue_set.json").read_text())
    records = payload.get("records")
    if not records:
        records = next(
            v for v in payload.values()
            if isinstance(v, list) and v and isinstance(v[0], dict) and "id" in v[0]
        )
    return {str(r["id"]): r for r in records}


def _scrub(text: str) -> str:
    """抹掉 pair 指纹，保留语义。`M.` 前缀让路径仍然可读、可比对。"""

    text = re.sub(r"llms_emp_feedback_final_\d{4}", "M", text)
    return re.sub(r"\b\d{4}\b", "NNNN", text)


def _blind_output(pair: str, arm: str, rounds: int) -> list[dict]:
    """该格三轮的已发布发现，盲化后交给复判者。

    只给 `issues` —— 判定的问题是「管线是否**发现并发布**了这条缺陷」，而排除项与观察项按定义
    没有发布。把它们一并给出会让复判者对「发现了但被制度静默」也判 1，那是另一个量。
    """

    base = HERE.parents[2] / "runs" / "paper1" / "matrix-v22"
    out = []
    for n in range(1, rounds + 1):
        path = base / f"run{n}" / f"{pair}-{arm}" / "discover-completed.json"
        if not path.is_file():
            out.append({"round": n, "issues": None, "note": "该轮无产物"})
            continue
        payload = json.loads(path.read_text())
        items = []
        for issue in (payload.get("issues") or []):
            items.append({
                "title": _scrub(str(issue.get("title") or issue.get("summary") or "")),
                "detail": _scrub(str(issue.get("detail") or issue.get("rationale") or ""))[:700],
            })
        out.append({"round": n, "issues": items})
    return out


def _band(pair: str, record_id: str, reportable: set[str]) -> str:
    if pair in TUNED_PAIRS:
        return "hist"
    return "reportable" if record_id in reportable else "burned"


def build(verdicts_path: pathlib.Path, size: int, seed: int) -> tuple[dict, dict]:
    payload = json.loads(verdicts_path.read_text())
    verdicts = payload.get("verdicts") or {}
    ledger = _ledger()
    frozen = json.loads((HERE / "holdout.json").read_text())
    reportable = set(frozen.get("reportable_records") or [])

    units = []
    for record_id, arms in verdicts.items():
        record = ledger.get(record_id) or {}
        pair = str(record.get("pair", ""))[-4:]
        if not pair:
            continue
        for arm, series in arms.items():
            if not isinstance(series, list):
                continue
            valid = [x for x in series if x is not None]
            if not valid:
                continue
            units.append({
                "record_id": record_id, "pair": pair, "arm": arm, "series": series,
                "band": _band(pair, record_id, reportable),
            })
    if not units:
        raise SystemExit("ERROR: no judgeable units in the verdict table.")

    # 按带分层，比例分配。分层保证覆盖，盲化保证无偏 —— 两者不矛盾。
    by_band: dict[str, list] = collections.defaultdict(list)
    for u in units:
        by_band[u["band"]].append(u)
    rng = random.Random(seed)
    picked = []
    for band, group in sorted(by_band.items()):
        group = sorted(group, key=lambda u: (u["record_id"], u["arm"]))
        quota = max(1, round(size * len(group) / len(units)))
        rng.shuffle(group)
        picked.extend(group[:quota])
    rng.shuffle(picked)

    pair_alias = {}
    for u in picked:
        pair_alias.setdefault(u["pair"], f"PAIR-{chr(65 + len(pair_alias))}")

    sample = {"seed": seed, "unit_count": len(picked), "items": []}
    key = {"seed": seed, "pair_alias": pair_alias, "items": []}
    for i, u in enumerate(picked, 1):
        record = ledger.get(u["record_id"]) or {}
        alias = pair_alias[u["pair"]]
        statement = str(record.get("statement") or "")
        statement = re.sub(r"llms_emp_feedback_final_\d{4}", "M", statement)
        statement = re.sub(r"\b\d{4}\b", "NNNN", statement)
        sample["items"].append({
            "unit_id": f"U{i:03d}",
            "model_alias": alias,
            "arm": u["arm"],
            "rounds": len(u["series"]),
            "expected_defect": statement,
            "layer": record.get("layer"),
            "predicate": record.get("predicate") or record.get("primary_predicate"),
            # 判定所需的产出必须在样本里，否则复判者无从判断 —— 首版只给了台账 statement，
            # 那样复判的是「这条缺陷听起来像不像被发现了」，不是同一件事。
            "pipeline_output_per_round": _blind_output(u["pair"], u["arm"], len(u["series"])),
            "task": ("对每一轮的 pipeline_output 逐轮判断：其中是否有一条与 expected_defect "
                     "**语义同一**的发现（同一命题，不是同一元素 —— 触及了正确元素却得出相反"
                     "结论算未发现）。输出每轮 1/0，并给一句依据。"),
        })
        key["items"].append({
            "unit_id": f"U{i:03d}", "record_id": u["record_id"], "pair": u["pair"],
            "arm": u["arm"], "band": u["band"], "original_series": u["series"],
        })
    return sample, key


def verify(sample_path: pathlib.Path) -> list[str]:
    text = sample_path.read_text()
    problems = []
    for m in set(_LEAK.findall(text)):
        if m == "NNNN":
            continue
        problems.append(f"残留 pair 指纹：{m!r}")
    for word in _BAND_WORDS:
        if word in text:
            problems.append(f"残留带名称：{word!r}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("verdicts_json", nargs="?", type=pathlib.Path,
                        default=HERE / "verdicts" / "v22_manual.json")
    parser.add_argument("--size", type=int, default=40)
    parser.add_argument("--seed", type=int, default=20260807)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args(argv)

    if args.verify:
        path = OUT / "sample.json"
        if not path.is_file():
            print(f"no {path}", file=sys.stderr)
            return 2
        problems = verify(path)
        if problems:
            print("盲化不完整：", file=sys.stderr)
            for p in problems:
                print(f"  - {p}", file=sys.stderr)
            return 1
        print(f"ok: {path} 无 pair 指纹、无带名称残留")
        return 0

    sample, key = build(args.verdicts_json, args.size, args.seed)
    OUT.mkdir(exist_ok=True)
    (OUT / "sample.json").write_text(json.dumps(sample, ensure_ascii=False, indent=1))
    (OUT / "key.json").write_text(json.dumps(key, ensure_ascii=False, indent=1))
    bands = collections.Counter(i["band"] for i in key["items"])
    print(f"抽出 {sample['unit_count']} 个判定单元，seed={args.seed}")
    print(f"  按带分布（仅在 key 里，sample 不含）：{dict(bands)}")
    print(f"  别名映射 {len(key['pair_alias'])} 个 pair")
    problems = verify(OUT / "sample.json")
    print("  盲化自检：" + ("✅ 干净" if not problems else f"❌ {len(problems)} 处残留"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
