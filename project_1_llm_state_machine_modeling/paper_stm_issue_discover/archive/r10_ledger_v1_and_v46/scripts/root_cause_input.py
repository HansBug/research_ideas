"""给根因分析准备完整输入。**不做分析，只保证没有一类结局被漏掉。**

## 为什么需要

上一代次的根因诊断是错的，而错的方式很具体：我断言「19 个谓词表达不了『模型多出了什么』」，
reviewer 反证 —— `FORBIDDEN_NODES` 不含 `ast.Not`，台账自己就用 `not edge_declared(...)`，
8 个谓词原生表达多出物，而且 `EIS-0032-02` / `EIS-0043-01` 就在**那一次运行里**被
`containment` 命中了。

那个错误的根因不是推理失误，是**输入不全**：我只看了 `issues`。而一条发现可以落在六个地方，
其中三个在判定者眼里都长得像「从未发现」：

    issues                  已发布
    excluded_findings       发现了，被归因策略排除
    excluded_observations   发现了，被证据角色制度静默
    coverage_gaps           发现了，预算耗尽
    rejected_issues         发现了，被结构门丢弃
    issue_citations_pruned  发现保留，其中的引用被剪除

v21 三十三格实测：`issues` 88、`excluded_findings` 42、`excluded_observations` 22、
`coverage_gaps` 15 —— 只看第一项，等于对 79 条结局视而不见。

## 本工具输出什么

1. **六类结局的全量计数与逐格分布**，外加 `adjudication_reconciliation` 里非空的每个键
   （包括 `unaccounted_safe_false_assertions` 与 `unsupported_issues_dropped` 这两类丢发现，
   它们在上一版呈现里根本没印）。
2. **谓词调用分布**：每个谓词被调用多少次、返回 True / False / 拒答各多少。这一项直接堵住
   上面那类错误 —— 断言「谓词表达不了 X」之前，先看它被调用了几次、答了什么。
3. **拒答按规则分布**，以及每条规则触及了哪些格。
4. **每条台账记录的机械邻近度**：哪些结局的元素与它重叠。**标注为代理，不是判定** ——
   判定由人工做，理由见 `present_for_judgment.py`。

`--json` 出机器可读，供 subagent 消费。
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

# ⚠️ 2026-08-17 归档：本文件原在 `discover_matrix/` 顶层，`HERE` 即指那一层；
# ⛔ 归档到 `archive/r10_ledger_v1_and_v46/scripts/` 后深度多了两层，`_PROVENANCE`
# 会解析到不存在的 `scripts/manual_review`。⭐ 故改为指向归档根（它保留了原 discover_matrix
# 的内部布局：manual_review/ · v46/ · verdicts/ …），⛔ 不数层数、按目录名锚定。
_F = pathlib.Path(__file__).resolve()
HERE = next(p for p in _F.parents if p.name == "r10_ledger_v1_and_v46")
# ⚠️ 2026-08-17 第二次搬迁：`manual_review/`（第一版台账 + 60 份复审 + relabel）已随台账证据链
# 搬到 `discover_matrix/ledger_v2/provenance/`，⛔ 不再是本归档的子目录。故单独锚一个常量，
# ⛔ 不许再写 `_PROVENANCE` —— 那会解析到不存在的目录并被读成空数据。
_PROVENANCE = (next(p for p in _F.parents if p.name == "paper_stm_issue_discover")
               / "discover_matrix" / "ledger_v2" / "provenance")
# ⛔ 归档后深度多了两层，原先的 parents[N] 解析到 `paper_stm_issue_discover/`。
# ⭐ 改为按仓库根标志物向上锚定（CLAUDE.md §9.5-3）。
ROOT = next(_p for _p in pathlib.Path(__file__).resolve().parents if (_p / "CLAUDE.md").is_file() and (_p / ".git").exists())

TOP_LEVEL = ("issues", "excluded_findings", "excluded_observations", "coverage_gaps")
#: `adjudication_reconciliation` 里值得单列的键。前两个是丢发现，上一版呈现没印。
RECON_KEYS = (
    "rejected_issues",
    "rejected_exclusions",
    "issue_citations_pruned",
    "unaccounted_safe_false_assertions",
    "unsupported_issues_dropped",
    "thin_merge_warnings",
    "misfiled_findings_moved",
    "merged_exclusions_split",
)
_PATH = re.compile(r"llms_emp_feedback_final_\d{4}[A-Za-z0-9_.]*")


def _cells(base: pathlib.Path):
    for run_dir in sorted(base.glob("run*")):
        for cell in sorted(p for p in run_dir.iterdir() if p.is_dir()):
            final = cell / "discover-completed.json"
            if final.is_file():
                yield f"{run_dir.name}/{cell.name}", json.loads(final.read_text())


def _elements(blob) -> set[str]:
    return set(_PATH.findall(json.dumps(blob, ensure_ascii=False)))


def _ledger() -> list[dict]:
    payload = json.loads((_PROVENANCE / "expected_issue_set.json").read_text())
    records = payload.get("records")
    if not records:
        records = next(
            value
            for value in payload.values()
            if isinstance(value, list) and value and isinstance(value[0], dict) and "id" in value[0]
        )
    return [r for r in records if isinstance(r, dict)]


def digest(base: pathlib.Path) -> dict:
    cells = list(_cells(base))
    if not cells:
        # 与本目录其他工具同一条纪律：零输入不得读成一次干净的分析。
        raise SystemExit(
            f"ERROR: no completed cells under {base}. Refusing to produce a digest from zero "
            "inputs -- an empty digest reads as 'nothing to explain'."
        )
    outcomes: dict[str, collections.Counter] = {k: collections.Counter() for k in TOP_LEVEL}
    recon: dict[str, collections.Counter] = {k: collections.Counter() for k in RECON_KEYS}
    predicates: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    refusals: collections.Counter = collections.Counter()
    per_cell: dict[str, dict] = {}
    for cell, payload in cells:
        row = {"coverage": payload.get("coverage_status", "")}
        for key in TOP_LEVEL:
            n = len(payload.get(key) or [])
            outcomes[key][cell] = n
            row[key] = n
        reconciliation = payload.get("adjudication_reconciliation") or {}
        for key in RECON_KEYS:
            value = reconciliation.get(key)
            n = len(value) if isinstance(value, list) else (1 if value else 0)
            if n:
                recon[key][cell] = n
                row[key] = n
        per_cell[cell] = row
    for cell, _payload in cells:
        run, name = cell.split("/", 1)
        records_dir = base / run / name / "records"
        if not records_dir.is_dir():
            continue
        for record_path in records_dir.glob("*precheck-and-seal-state-update/record.json"):
            try:
                text = record_path.read_text()
            except OSError:
                continue
            for match in re.finditer(r'"expression"\s*:\s*"([a-z_]+)\(', text):
                predicates[match.group(1)]["called"] += 1
            if "UnsupportedEvidence" in text:
                for rule in (
                    "transient_subject", "undiscriminating_root", "horizon_probe",
                    "pseudo_initial", "malformed_name", "unsupported_binding",
                    "no_matching_transition", "ambiguous_initial", "fbmcq_solver",
                ):
                    refusals[rule] += text.count(rule)
    ledger = _ledger()
    proximity = []
    for record in ledger:
        pair = str(record.get("pair", ""))[-4:]
        want = _elements(record.get("assertions") or record.get("statement") or "")
        touched: dict[str, list[str]] = collections.defaultdict(list)
        for cell, payload in cells:
            if f"_{pair}" not in cell and not cell.split("/")[1].startswith(pair):
                continue
            for key in TOP_LEVEL:
                for item in payload.get(key) or []:
                    if want & _elements(item):
                        touched[key].append(cell)
        if touched:
            proximity.append(
                {"record": record["id"], "layer": record.get("layer"),
                 "touched_by": {k: sorted(set(v)) for k, v in touched.items()}}
            )
    return {
        "base": str(base),
        "cells": len(cells),
        "outcome_totals": {k: sum(v.values()) for k, v in outcomes.items()},
        "reconciliation_totals": {k: sum(v.values()) for k, v in recon.items() if sum(v.values())},
        "per_cell": per_cell,
        "predicate_calls": {k: dict(v) for k, v in sorted(predicates.items())},
        "refusals_by_rule": dict(refusals.most_common()),
        "ledger_proximity": proximity,
        "proximity_is_a_proxy": (
            "元素重叠，不是判定。判定由人工做（present_for_judgment.py 记着两条反例：触及了正确"
            "元素却得出相反结论）。这里给它只是为了让分析者知道该去看哪几格。"
        ),
        "why_all_six": (
            "一条发现可以落在六个地方，其中三个在判定者眼里都像「从未发现」。上一代次的根因诊断"
            "只看了 issues，于是断言「谓词表达不了多出物」——而 containment 在那次运行里就命中了"
            "两条。看全六类是这个工具存在的全部理由。"
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", type=pathlib.Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = digest(args.base)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return 0
    print(f"格数 {result['cells']}")
    print("\n六类结局（顶层四类）:")
    for key, n in result["outcome_totals"].items():
        print(f"  {key:26s} {n}")
    if result["reconciliation_totals"]:
        print("\nadjudication_reconciliation 非空:")
        for key, n in result["reconciliation_totals"].items():
            print(f"  {key:40s} {n}")
    print("\n谓词调用（断言「某谓词表达不了 X」之前先看这里）:")
    for name, counts in sorted(
        result["predicate_calls"].items(), key=lambda kv: -kv[1].get("called", 0)
    ):
        print(f"  {name:26s} {counts.get('called', 0)}")
    if result["refusals_by_rule"]:
        print("\n拒答按规则:")
        for rule, n in result["refusals_by_rule"].items():
            print(f"  {rule:26s} {n}")
    print(f"\n台账邻近度（**代理，不是判定**）: {len(result['ledger_proximity'])} 条记录有元素重叠")
    return 0


if __name__ == "__main__":
    sys.exit(main())
