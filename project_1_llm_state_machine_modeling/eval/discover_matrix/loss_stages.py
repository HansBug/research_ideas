"""把未命中位按「最深到达的环节」分段，用于定位损失集中在流水线的哪一层。

## 为什么这个脚本必须在仓库里，而不是每次现写

它的第一版是临时脚本，产出的分段（① 91 / ② 71）被写进了 PR comment 与 issue #177，并据此
得出「损失不集中在任何一环」这个中心论断。**那个论断是错的**，因为分段本身错了：脚本对
splitter 的整条 LLM-call 记录做 `"predicate": "X"` 正则，而记录里的 `system_prompt` 字段
本身含 8 处该形状（谓词词表的 worked example 就是那个 JSON 写法）。于是「只在 prompt 里
出现过的谓词」被算成「写进了需求集」。

改用 `parsed_output.requirements[].predicate` 后：① 是 **135** 不是 91，② 是 **24** 不是 71。
损失是**集中的** —— ① 需求层占全部未命中的 39%，是第二大段的近三倍。

教训有两条，都值得留在这里：

1. **产出记录里同时装着输入和输出。** 对整条记录做正则，量到的是两者之和。任何「模型写了
   什么」的统计都必须指名到 `parsed_output`，不能图省事 dump 整个对象。
2. **能改变结论的度量工具必须落库并带测试。** 临时脚本没有回归，错误会活到它支撑的每一个
   结论里。

## 六段的定义（互斥，按最深到达者归段）

- **⑥** 台账无 `primary_predicate` —— 不可机械判定。注意它**不是损失**：这些位的命中率与
  全量相当，人工判编码等价照样接住。
- **①** 需求层：该谓词在**该格任何一版需求集**里都没被写出来，且从未被调用。
- **②** 断言层：需求写了，但没有对应断言跑起来。
- **③** 真值层：断言跑了，但从未取到台账期望的真值。
- **④** 发布层：取到了期望真值，但没被任何已发布 issue 引用。
- **⑤** 判定层：已发布且真值对，但绑定/命题不符。

用法::

    python loss_stages.py --generation matrix-v37 --audit /tmp/v37_audit_324.json
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import verdict_tiers as V  # noqa: E402

REPO = HERE.parents[2]
RUNS = REPO / "runs" / "paper1"

STAGES = (
    "命中",
    "① 需求层",
    "② 断言层",
    "③ 真值层",
    "④ 发布层",
    "⑤ 判定层",
    "⑥ 台账无 primary",
)


def requirement_predicates(cell_dir: pathlib.Path) -> set[str]:
    """Predicates the splitter actually wrote, across every revision of this cell.

    ⚠️ Reads `parsed_output` only.  The enclosing record also carries `system_prompt` and
    `raw_response`; the first contains the predicate catalogue's worked examples in the same
    JSON shape, so a regex over the whole record counts prompt text as產出.
    """

    written: set[str] = set()
    pattern = "records/*requirement-splitter-llm-call-completed*/record.json"
    for record_path in sorted(cell_dir.glob(pattern)):
        try:
            payload = json.loads(record_path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        parsed = payload.get("parsed_output")
        if not isinstance(parsed, dict):
            continue
        for requirement in parsed.get("requirements") or ():
            if isinstance(requirement, dict) and requirement.get("predicate"):
                written.add(str(requirement["predicate"]))
    return written


def stage_of(
    entry: dict, ledger: dict, cell_dir: pathlib.Path, cache: dict
) -> str:
    """Which stage this judged position died at."""

    if entry["hit"]:
        return "命中"
    record = ledger[entry["record_id"]]
    predicate = record.get("primary_predicate")
    if not predicate:
        return "⑥ 台账无 primary"
    if cell_dir not in cache:
        cache[cell_dir] = (
            V.cell_evidence(cell_dir),
            requirement_predicates(cell_dir),
        )
    evidence, written = cache[cell_dir]
    calls = [call for call in evidence["calls"] if call["predicate"] == predicate]
    if predicate not in written and not calls:
        return "① 需求层"
    if not calls:
        return "② 断言层"
    if not any(call["result"] is False for call in calls):
        return "③ 真值层"
    if not any(call["published"] and call["result"] is False for call in calls):
        return "④ 发布层"
    return "⑤ 判定层"


def classify(generation: str, audit_path: pathlib.Path) -> dict:
    root = RUNS / generation
    ledger = V.ledger_claims()
    audit = json.loads(audit_path.read_text())["audit"]
    cache: dict = {}
    totals: collections.Counter = collections.Counter()
    by_predicate: dict[str, collections.Counter] = collections.defaultdict(
        collections.Counter
    )
    by_pair: dict[str, collections.Counter] = collections.defaultdict(
        collections.Counter
    )
    for entry in audit:
        run, cell = entry["cell"].split("/")
        stage = stage_of(entry, ledger, root / run / cell, cache)
        totals[stage] += 1
        pair = ledger[entry["record_id"]]["pair"]
        by_pair[pair][stage] += 1
        if stage not in {"命中", "⑥ 台账无 primary"}:
            predicate = ledger[entry["record_id"]].get("primary_predicate")
            if predicate:
                by_predicate[stage][predicate] += 1
    return {
        "generation": generation,
        "positions": sum(totals.values()),
        "totals": dict(totals),
        "by_predicate": {k: dict(v) for k, v in by_predicate.items()},
        "by_pair": {k: dict(v) for k, v in by_pair.items()},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--generation", required=True)
    parser.add_argument("--audit", required=True, type=pathlib.Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = classify(args.generation, args.audit)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return 0
    total = result["positions"]
    print(f"{result['generation']}  {total} 位\n")
    for stage in STAGES:
        count = result["totals"].get(stage, 0)
        print(f"  {stage:<18}{count:>4}  {count / total:>6.1%}")
    for stage in STAGES[1:-1]:
        composition = result["by_predicate"].get(stage)
        if composition:
            top = sorted(composition.items(), key=lambda kv: -kv[1])[:8]
            print(f"\n{stage} 谓词构成: " + " ｜ ".join(f"{k} {v}" for k, v in top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
