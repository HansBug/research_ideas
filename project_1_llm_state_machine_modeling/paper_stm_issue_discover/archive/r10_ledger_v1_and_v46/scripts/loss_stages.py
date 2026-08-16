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

## 分段定义（互斥，按最深到达者归段）

- **⑥** 台账无 `primary_predicate` —— 不可机械判定。注意它**不是损失**：这些位的命中率与
  全量相当，人工判编码等价照样接住。
- **①** 需求层：该谓词在**该格任何一版需求集**里都没被写出来，且从未被调用。
- **②** 断言层：需求写了，但没有对应断言跑起来。
- **③** 真值层：断言跑了，但从未取到台账期望的真值。
- **④** 发布层：取到了期望真值，但没被任何已发布 issue 引用。
- **⑤** 绑定层：该谓词**发布过**，但绑的不是台账问的那组元素——报到了同一片区域、指错了对象。
- **⑦** 台账 primary 存在但解析不出 `(谓词, 绑定) -> 期望真值`（``all([...])`` 等形态）。机械不可判，
  与「台账根本没有 primary」是两回事，分开记，免得把「判不了」读成「不该判」。

⚠️ **旧口径里的「⑤ 判定层」在严格绑定判据下必然为空**，因为「已发布 + 绑定相符 + 真值等于期望」
恰好就是 `tier_a` 的命中条件——一个位不可能同时满足它又被判未命中。旧 ⑤ 的 53 位全部是按谓词名
松散匹配的产物。现在的 ⑤ 换了定义：**谓词发布过但绑错对象**，这才是当初想从 ⑤ 读出的东西。

## ③ 与旧 ⑤ 为什么恒为空

两者都是严格判据下的**结构性空段**，不是数据碰巧如此：

- **③ 真值层**：绑定逐字相符地问同一个问题，在同一份制品上必然得到台账记的那个真值——谓词是
  确定性的。所以「问对了却没取到期望真值」不可能发生。
- **旧 ⑤ 判定层**（已发布 + 绑定相符 + 真值对）恰是 `tier_a` 的命中条件，一个位不可能同时
  满足它又被判未命中。代码里那条分支现在直接 `raise`，用来发现分段与判定两侧判据漂移。

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

# ⛔ 归档后深度多了两层，原先的 parents[N] 解析到 `paper_stm_issue_discover/`。
# ⭐ 改为按仓库根标志物向上锚定（CLAUDE.md §9.5-3）。
REPO = next(_p for _p in pathlib.Path(__file__).resolve().parents if (_p / "CLAUDE.md").is_file() and (_p / ".git").exists())
RUNS = REPO / "runs" / "paper1"

STAGES = (
    "命中",
    "① 需求层",
    "② 断言层",
    "③ 真值层",
    "④ 发布层",
    "⑤ 绑定层",
    "⑥ 台账无 primary",
    "⑦ primary 不可机械解析",
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


def _answers_the_claim(call: dict, bindings: tuple, ) -> bool:
    """Does this call ask the ledger's question, or merely a same-named one?

    Same rule as `verdict_tiers.tier_a`: every binding key the ledger wrote must be present and
    equal; the only extra keys allowed are observation-horizon parameters. Deliberately shared
    with tier_a rather than reimplemented -- if the two drift, a position can be "answered"
    for segmentation and "unanswered" for adjudication at the same time.
    """

    call_bindings = dict(call["bindings"])
    ledger_bindings = dict(bindings)
    if set(ledger_bindings) - set(call_bindings):
        return False
    if set(call_bindings) - set(ledger_bindings) - V._HORIZON_BINDINGS:
        return False
    return all(ledger_bindings[key] == call_bindings[key] for key in ledger_bindings)


def stage_of(
    entry: dict, ledger: dict, cell_dir: pathlib.Path, cache: dict
) -> str:
    """Which stage this judged position died at.

    ⚠️ The first version compared **predicate names only** and hardcoded the expected truth
    value to `False`. Both are wrong and they compounded:

    - A ledger claim like ``not edge_declared(cruise, dist_to_exit_2, FinishState)`` expects the
      inner call to be **True**; hardcoding False meant the position could never reach ④/⑤ on
      its own evidence, and instead matched some unrelated `edge_declared` call elsewhere in the
      cell. Measured on v37: **13 of the 24 ④ positions were misfiled this way.**
    - Matching on the name alone counts "the cell asked a different question with the same
      predicate" as "the cell asked this question". That is precisely the distinction ①/②/③ are
      supposed to draw, so the error was self-concealing.

    The expected truth value and the bindings both come from `record["claims"]`, the same source
    `verdict_tiers.tier_a` adjudicates against. A record may carry several claims (``any([...])``
    forms); the position is credited with the **deepest** stage any single claim reached, since
    getting one claim further is genuine progress on that position.
    """

    if entry["hit"]:
        return "命中"
    record = ledger[entry["record_id"]]
    claims = record.get("claims") or {}
    if not record.get("primary_predicate"):
        return "⑥ 台账无 primary"
    if not claims:
        # A primary that exists but does not parse into (predicate, bindings) -> expected.
        # Mechanically unjudgeable -- but NOT the same as having no primary, so it gets its own
        # label. Folding it into ⑥ would quietly inflate "the ledger did not ask" with "the tool
        # cannot read what the ledger asked".
        return "⑦ primary 不可机械解析"
    if cell_dir not in cache:
        cache[cell_dir] = (
            V.cell_evidence(cell_dir),
            requirement_predicates(cell_dir),
        )
    evidence, written = cache[cell_dir]

    depth = {"① 需求层": 1, "⑤ 绑定层": 2, "② 断言层": 3, "③ 真值层": 4, "④ 发布层": 5}
    reached = "① 需求层"
    for (predicate, bindings), expected in claims.items():
        same_predicate = [c for c in evidence["calls"] if c["predicate"] == predicate]
        answering = [c for c in same_predicate if _answers_the_claim(c, bindings)]
        if predicate not in written and not same_predicate:
            stage = "① 需求层"
        elif not answering:
            # The predicate exists in this cell but nothing bound the way the ledger asks: the
            # question was never posed. Split by whether the cell nonetheless *published*
            # something with this predicate -- "reported the neighbourhood, bound the wrong
            # object" is a different problem from "asked nothing of the kind", and lumping them
            # together is what made the old ⑤ unreadable.
            stage = (
                "⑤ 绑定层"
                if any(c["published"] for c in same_predicate)
                else "② 断言层"
            )
        elif not any(c["result"] is expected for c in answering):
            stage = "③ 真值层"
        elif not any(c["published"] and c["result"] is expected for c in answering):
            stage = "④ 发布层"
        else:
            # Published + bindings match + result == expected is exactly `tier_a`'s hit
            # condition, so this position would have been auto-credited as a hit and never
            # reached `stage_of`. Unreachable by construction; assert rather than invent a
            # stage for it.
            raise AssertionError(
                f"{entry['record_id']}@{entry['cell']}: tier_a should have matched "
                f"{predicate}{bindings}; segmentation and adjudication have drifted apart"
            )
        if depth[stage] > depth[reached]:
            reached = stage
    return reached


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
