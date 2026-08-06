"""在当前语义下重算「被排除的发现是否会变可采」。用于预注册 §六 / §八 要求的双报。

## 为什么需要它

V1 / V2 / V4 / V5 与本代次的 Q1 角色翻转都改的是**断言可采性**：把 `unattributed` 或
`representation_debt` 转成 `safe`。`status == "safe"` 是进入 `issues` 的唯一闸门，所以这些修法
**直接抬高 `hit@k` 的分子而分母不变**。预注册因此要求双报：v21 的数字要以「as published」与
「re-derived under 当前谓词」两列并排给出。

## 上一版路径为什么办不到

`detect_fabrications.py` 的 `scan()` 第一行就是

    issues = artifact.get("issues") or []
    if not issues: continue

它**只遍历已发布 issue**，没有任何分支读 `excluded_findings`。而双报要测的恰恰是「条目从
`excluded_findings` 搬进 `issues`」这个方向。实测 v21 三十三格：

    issues 88 | excluded_findings 42（unattributed 24 + representation_debt 18）
    excluded_observations 22 | coverage_gaps 15

那 42 条候选一条都进不了重导出结果，于是那条被预注册为公平性控制的路径**只能把 v21 的分子往下
调**，方向与它要控制的机制相反。文档把这个方向写成「回测不模拟修订路径」所致的下界 —— 结论
（v21' ≤ v21-under-v22）对，理由不对：真实主因是重导出器没有任何机制重新采信被排除项。

## 本脚本做什么、不做什么

**做**：对每条 `excluded_findings`，取归因层记录的 `exclusion_refs` 与该断言的谓词，用**当前**
`exclusion_roles` / `_omission_placeholder_only` 重算「这些排除项是否只是遗漏替身」。若答案由
False 变 True，该条在当前语义下会得到 `safe`，即会被发布。

**不做**：不重跑修订循环，不重跑 LLM，不重新执行断言。所以这是**下界**，而且理由要说全两条：

  1. 重新采信只在**已经产出的**排除项上算。当前语义下生产者会走一条不同的修订路径，可能产出
     另一批断言，那批不在这里。
  2. 只重算可采性判定这一步。谓词返回值沿用冻结产物，不重新求值。

`--json` 出机器可读结果，供 gist 与 comment 引用。
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PIPELINE_SRC = ROOT / "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/feedback_loop/src"
if str(PIPELINE_SRC) not in sys.path:
    sys.path.insert(0, str(PIPELINE_SRC))

#: 被重新采信的条目按这个原因分类，使「哪条修法起了作用」在报告里可追。
REASONS = {
    "omission_only": "全部排除项在当前角色判据下都是遗漏替身（V4/V5 + Q1 角色翻转）",
    "still_debt": "至少一条排除项是 carrier，仍为表示债务",
    "unattributed": "无排除项可算——它是 unattributed，需要 V1/V2 的祖先/前置条件回退，"
                    "而那要重跑归因层，本脚本不做",
}


def _contract_for(pair: str) -> dict | None:
    """该 pair 的 working contract。找不到就返回 None，调用方回落叶名表并说明。"""

    matches = sorted(ROOT.glob(f"**/working_contracts/*{pair[-4:]}*.json"))
    for path in matches:
        try:
            return json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
    return None


def rederive(audit_dir: pathlib.Path) -> dict:
    """逐条重算被排除发现的可采性。"""

    from paper_stm_feedback_loop.discover.nodes import (  # noqa: E402
        _omission_placeholder_only,
        exclusion_roles,
    )

    files = sorted(audit_dir.glob("*-audit.json"))
    if not files:
        # 与 detect_fabrications 同一条纪律：零输入不得读成一次干净的扫描。
        raise SystemExit(
            f"ERROR: no *-audit.json under {audit_dir}. This reads the audit bundle built by "
            "build_gist.py, not a raw round directory. Refusing to report a count from zero "
            "inputs -- that reads as 'nothing would be re-admitted'."
        )
    rows: list[dict] = []
    tally: collections.Counter = collections.Counter()
    no_contract: set[str] = set()
    for path in files:
        record = json.loads(path.read_text())
        if record.get("terminal") != "completed":
            continue
        cell = path.name.removesuffix("-audit.json")
        pair = str(record.get("pair") or "")
        artifact = record.get("terminal_artifact") or {}
        excluded = artifact.get("excluded_findings") or []
        if not excluded:
            continue
        contract = _contract_for(pair)
        if contract is None:
            no_contract.add(pair)
        roles = exclusion_roles(contract)
        bindings = {
            b.get("assertion_id"): b
            for b in (record.get("attribution_bindings") or [])
            if isinstance(b, dict)
        }
        predicates = {
            a.get("assertion_id"): a
            for a in (record.get("assertions") or [])
            if isinstance(a, dict)
        }
        for finding in excluded:
            status = str(finding.get("attribution_status") or "")
            for assertion_id in finding.get("assertion_ids") or []:
                binding = bindings.get(assertion_id) or {}
                refs = list(binding.get("exclusion_refs") or ())
                predicate = _predicate_of(predicates.get(assertion_id) or {})
                if not refs:
                    reason = "unattributed"
                    admitted = False
                else:
                    admitted = bool(_omission_placeholder_only(refs, predicate, roles))
                    reason = "omission_only" if admitted else "still_debt"
                tally[(status, reason)] += 1
                rows.append(
                    {
                        "cell": cell,
                        "pair": pair,
                        "issue_id": finding.get("issue_id") or "",
                        "title": finding.get("title") or "",
                        "assertion_id": assertion_id,
                        "predicate": predicate,
                        "status_as_published": status,
                        "exclusion_refs": refs,
                        "readmitted_under_current": admitted,
                        "reason": reason,
                    }
                )
    return {
        "audit_dir": str(audit_dir),
        "excluded_findings_examined": len(rows),
        "readmitted": sum(1 for r in rows if r["readmitted_under_current"]),
        "by_status_and_reason": {f"{s}/{r}": n for (s, r), n in sorted(tally.items())},
        "pairs_without_contract": sorted(no_contract),
        "rows": rows,
        "bound": "lower",
        "bound_reasons": [
            "只在已经产出的排除项上重算；当前语义下生产者会走不同的修订路径，"
            "可能产出另一批断言，那批不在此处",
            "只重算可采性判定这一步；谓词返回值沿用冻结产物，不重新求值",
        ],
    }


def _predicate_of(assertion: dict) -> str:
    """断言调用的谓词名。归因层按谓词决定是否给遗漏豁免，所以它必须取对。"""

    expression = str(assertion.get("expression") or "")
    head = expression.split("(", 1)[0].strip()
    # `all([state_declared(...)])` 这类折叠写法：取第一个已知谓词名，而不是 builtin。
    if head in {"all", "any", "bool", "not"}:
        from paper_stm_feedback_loop.assertions.predicate_api import PREDICATE_NAMES

        for name in sorted(PREDICATE_NAMES, key=len, reverse=True):
            if f"{name}(" in expression:
                return name
    return head


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit_dir", type=pathlib.Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = rederive(args.audit_dir)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return 0
    print(f"被排除发现（断言级）: {result['excluded_findings_examined']}")
    print(f"当前语义下会被重新采信: {result['readmitted']}")
    for key, count in result["by_status_and_reason"].items():
        print(f"  {key}: {count}")
    if result["pairs_without_contract"]:
        print(f"⚠️ 无 working contract 的 pair（回落叶名表，结果偏保守）: "
              f"{result['pairs_without_contract']}")
    print(f"\n这是**{result['bound']}界**，两条理由：")
    for reason in result["bound_reasons"]:
        print(f"  - {reason}")
    readmitted = [r for r in result["rows"] if r["readmitted_under_current"]]
    if readmitted:
        print(f"\n逐条（{len(readmitted)} 条）：")
        for row in readmitted:
            print(f"  {row['cell']:34} {row['assertion_id']:18} {row['predicate']:16} "
                  f"{row['status_as_published']} -> safe")
            print(f"     {row['title'][:110]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
