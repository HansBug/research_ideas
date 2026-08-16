"""统计 19 个谓词与三个族在**台账侧**与**模型产出侧**各自出现多少次。

两侧问的不是同一件事，所以分母不同质、**不可相除**：

- **台账侧**：人工标注每条已知缺陷时，为它写下的断言用了哪些谓词。它反映的是
  「要表达这批已知缺陷，需要哪些谓词」——是一份**需求侧的谓词需求分布**。
- **产出侧**：324 格运行中，方法自己生成并最终支撑已发布 issue 的断言用了哪些谓词。
  它反映的是「方法实际在用哪些谓词」——是一份**供给侧的谓词使用分布**。

两侧的差就是本脚本的用处：某谓词在台账侧需求高而产出侧供给低，说明方法没在该形态上取证。

族归属直接读 `predicates.py` 的 `family_of`，不在此处复制一份定义。
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

# ⚠️ 2026-08-17 归档：本文件原在 `discover_matrix/` 顶层，`HERE` 即指那一层；
# ⛔ 归档到 `archive/r10_ledger_v1_and_v46/scripts/` 后深度多了两层，`HERE / "manual_review"`
# 会解析到不存在的 `scripts/manual_review`。⭐ 故改为指向归档根（它保留了原 discover_matrix
# 的内部布局：manual_review/ · v46/ · verdicts/ …），⛔ 不数层数、按目录名锚定。
_F = pathlib.Path(__file__).resolve()
HERE = next(p for p in _F.parents if p.name == "r10_ledger_v1_and_v46")
RUNS = pathlib.Path.home() / "oo-projects/research_ideas/runs/paper1/matrix-v46-full"
LEDGER = HERE / "manual_review" / "expected_issue_set.json"

#: `state_declared(state="...", kind="leaf") is True` -> `state_declared`
_CALL = re.compile(r"\b([a-z_][a-z0-9_]*)\s*\(")

_FAMILY_LABEL = {"S": "结构", "B": "仿真", "P": "有界模型检查"}
_FAMILY_ORDER = ("S", "B", "P")


def _predicate_names() -> tuple[dict[str, str], list[str]]:
    """从 pyfcstm 侧的谓词定义读族归属，避免在本文件里复制一份。"""

    root = HERE.parent.parent / "paper_stm_issue_discover/pipeline/feedback_loop/src"
    sys.path.insert(0, str(root))
    from paper_stm_feedback_loop.discover.predicates import (  # noqa: E402
        PREDICATE_ORDER,
        family_of,
    )

    return {n: family_of(n) for n in PREDICATE_ORDER}, list(PREDICATE_ORDER)


def _predicates_in(expression: str, known: set[str]) -> list[str]:
    return [n for n in _CALL.findall(expression or "") if n in known]


def ledger_side(known: set[str]) -> tuple[collections.Counter, collections.Counter]:
    """台账侧：只数**可判记录**（进入能力分母的那 98 条）。"""

    sys.path.insert(0, str(HERE))
    import metrics_at_k as mk

    reportable = set(mk.REPORTABLE)
    payload = json.loads(LEDGER.read_text())
    records = payload["records"] if isinstance(payload, dict) else payload

    per_predicate: collections.Counter = collections.Counter()
    primary_only: collections.Counter = collections.Counter()
    for record in records:
        rid = record.get("id") or record.get("record_id")
        if rid not in reportable:
            continue
        for assertion in record.get("assertions") or []:
            # 台账自带 `predicates` 字段；缺失时才回退到从表达式抽取。
            names = [n for n in (assertion.get("predicates") or []) if n in known]
            if not names:
                names = _predicates_in(assertion.get("expression", ""), known)
            per_predicate.update(names)
            if assertion.get("role") == "primary":
                primary_only.update(names)
    return per_predicate, primary_only


def _assertions_of(cell: pathlib.Path) -> dict[str, dict]:
    """一格里所有断言，按 id 索引。断言在修订台账的 artifact_delta 里累积。"""

    out: dict[str, dict] = {}
    for record in sorted(cell.glob("records/*/record.json")):
        try:
            payload = json.loads(record.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        stack = [payload]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                if "assertion_id" in node and "expression" in node:
                    out[node["assertion_id"]] = node
                stack.extend(node.values())
            elif isinstance(node, list):
                stack.extend(node)
    return out


def output_side(known: set[str]) -> tuple[collections.Counter, collections.Counter, int, int]:
    """产出侧：支撑**已发布 issue** 的断言用了哪些谓词，逐格计数。

    同时给一份「全部生成的断言」口径——两者的差是「生成了但没走到发布」的部分。
    """

    published: collections.Counter = collections.Counter()
    generated: collections.Counter = collections.Counter()
    cells = issues = 0
    for completed in sorted(RUNS.glob("run*/*/discover-completed.json")):
        cell = completed.parent
        try:
            payload = json.loads(completed.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        cells += 1
        assertions = _assertions_of(cell)
        for assertion in assertions.values():
            generated.update(_predicates_in(assertion.get("expression", ""), known))
        for issue in payload.get("issues") or []:
            issues += 1
            for aid in issue.get("assertion_ids") or []:
                found = assertions.get(aid)
                if found:
                    published.update(_predicates_in(found.get("expression", ""), known))
    return published, generated, cells, issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--markdown", action="store_true", help="输出可直接贴进报告的表")
    args = parser.parse_args(argv)

    family, order = _predicate_names()
    known = set(order)
    led_all, led_primary = ledger_side(known)
    pub, gen, cells, issues = output_side(known)

    print(f"# 谓词使用分布（台账侧 vs 产出侧）\n")
    print(f"产出侧扫描 {cells} 格、{issues} 条已发布 issue。\n")

    fam_rows = collections.defaultdict(lambda: [0, 0, 0, 0])
    for name in order:
        f = family[name]
        fam_rows[f][0] += led_all[name]
        fam_rows[f][1] += led_primary[name]
        fam_rows[f][2] += pub[name]
        fam_rows[f][3] += gen[name]

    print("## 族级\n")
    print("| 族 | 台账侧断言 | 其中 primary | 产出侧支撑已发布 issue | 产出侧全部生成 |")
    print("| :-- | --: | --: | --: | --: |")
    tot = [0, 0, 0, 0]
    for f in _FAMILY_ORDER:
        r = fam_rows[f]
        for i in range(4):
            tot[i] += r[i]
        print(f"| **{_FAMILY_LABEL[f]}** | {r[0]} | {r[1]} | {r[2]} | {r[3]} |")
    print(f"| **合计** | **{tot[0]}** | **{tot[1]}** | **{tot[2]}** | **{tot[3]}** |")

    print("\n## 谓词级\n")
    print("| 族 | 谓词 | 台账侧 | 其中 primary | 产出侧已发布 | 产出侧全部 |")
    print("| :-- | :-- | --: | --: | --: | --: |")
    for name in sorted(order, key=lambda n: (_FAMILY_ORDER.index(family[n]), -pub[n], n)):
        print(f"| {_FAMILY_LABEL[family[name]]} | `{name}` | {led_all[name]} | "
              f"{led_primary[name]} | {pub[name]} | {gen[name]} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
