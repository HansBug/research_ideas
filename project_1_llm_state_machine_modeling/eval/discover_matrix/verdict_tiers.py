"""命中判定的三层：A 层确定性、B 层人工判编码等价、C 层分歧闸。

## 为什么分三层，而不是「全人工」或「全自动」

**全自动做不到。** 台账的陈述是散文，而同一个缺陷可以被合法地编码成不同的谓词与绑定 ——
`HIT_CRITERION.md` §3 列了四种成立形态，只有第一种（直接对应）是机械可判的。实测（v35，132 判定位）：
按 (谓词, 绑定, 真值) 完全相等去判，只复现人工 89 条命中里的 **28 条（31%）**。

**全人工也不行，而且已经出过错。** v35 那一轮我在 132 位上犯了两处**作用域误判**
（`EIS-0032-01` 记成 3/6、`EIS-0029-05` 记成 2/6），都是拿「同一个 pair、同一类谓词」的邻近性
代替读台账 statement。这两处恰好都是 A 层判 0 而人工判命中 —— **分歧本身就是警报**。

所以分工是：**A 层负责检索与自动确认，人只做判断，而机器与人的分歧变成一道必须书面交代的闸。**

## 三层的确切定义

### A 层 —— 确定性，无人参与

issue 命中记录 R ⟺ 该 issue 引用的某条断言，其 (谓词, 绑定) 与 R 的某条**已记真值**的台账断言完全
相等，且其实测真值等于台账记的那个值。

- 只看**已发布 issue 引用的**断言。被排除的发现不算命中 —— 它没有进入产物。
- 台账的 `measured` 是字符串 `"False"` 而非布尔 `False`，必须先归一化；不归一化会让每一条都判不等。
- 实测性质：**假阳 0，假阴 50**（v35）。A 层从不宣称一个人会否掉的命中，所以它的输出可以直接采信；
  它只是不完备。

### B 层 —— 人工判编码等价

A 层未确认的每一位，本模块打印一张对照表：台账 primary 的表达式与期望真值，该格全部断言的
(谓词, 绑定, 真值)，以及逐项差异（谓词 / 锚点 / 其余绑定 / 真值 哪一项不同）。

人只回答一个问题：**这两种编码是不是同一个命题。** 不检索、不猜绑定。

### C 层 —— 分歧闸

- 人判命中而 A 层未确认 → **必须**写出等价性论证，并点明属 `HIT_CRITERION.md` §3 四种形态的哪一种。
  这是 v35 那两处误判会被拦住的地方：把「作用域邻近」写成论证时它自己站不住。
- A 层确认而人判未命中 → 两者之一必错，不得并存，必须就地解决。

## 审计输出

每一位都记「由谁判定、依据是什么」，不只是 yes/no：

    {"record_id": ..., "cell": ..., "hit": true,
     "decided_by": "tier_a" | "human",
     "tier_a": {"matched": true, "assertion_id": ..., "expression": ..., "truth_value": false},
     "human": {"equivalence_form": "蕴含更根本的原因", "argument": ..., "cited_assertion_ids": [...]}}

用法：

    python -m verdict_tiers --generation matrix-v36                # A 层 + B 层对照表
    python -m verdict_tiers --generation matrix-v36 --verdicts v.json --audit out.json
"""

from __future__ import annotations

import argparse
import ast
import collections
import json
import re
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
RUNS = REPO / "runs" / "paper1"
LEDGER = HERE / "manual_review" / "expected_issue_set.json"

_CELL = re.compile(r"^(\d{4})-(claude|gpt)$")

#: `HIT_CRITERION.md` §3 的四种成立形态，逐字取自该文件。人工判命中时必须点名其中一种。
#:
#: 闭集是这道闸的全部力量所在：一个不属于任何形态的「等价性论证」就是没有论证。
EQUIVALENCE_FORMS = (
    "直接对应",
    "合取项之一",
    "负向命题的正向对偶",
    "蕴含更根本的原因",
)


def _as_bool(raw: Any) -> bool | None:
    """台账的 `measured` 是字符串 `"False"`，不是布尔。

    不归一化会让 `False is "False"` 恒假，于是每一条都判不等 —— 实测踩过：一次复测把 91 条
    全报成「台账与实现不一致」，而真实答案是 0 条。
    """

    if isinstance(raw, bool):
        return raw
    if isinstance(raw, str) and raw.strip() in ("True", "False"):
        return raw.strip() == "True"
    return None


def _parse_call(expression: str) -> tuple[str, tuple[tuple[str, Any], ...]] | None:
    """`f(a=1, b="x")` -> `("f", (("a",1),("b","x")))`；`all`/`any` 与位置参数返回 None。"""

    try:
        node = ast.parse((expression or "").strip(), mode="eval").body
    except (SyntaxError, ValueError):
        return None
    if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
        return None
    if node.func.id in ("all", "any") or node.args:
        return None
    bindings = {}
    for keyword in node.keywords:
        if keyword.arg is None:
            return None
        try:
            bindings[keyword.arg] = ast.literal_eval(keyword.value)
        except (ValueError, SyntaxError):
            return None
    return node.func.id, tuple(sorted(bindings.items()))


def ledger_claims() -> dict[str, dict[str, Any]]:
    """record_id -> {pair, layer, statement, claims: {(pred, bindings): expected_bool}}"""

    out: dict[str, dict[str, Any]] = {}
    for record in json.loads(LEDGER.read_text())["records"]:
        claims: dict[tuple[str, tuple[tuple[str, Any], ...]], bool] = {}
        primary_expression = ""
        for assertion in record.get("assertions") or ():
            expected = _as_bool(assertion.get("measured"))
            parsed = _parse_call(assertion.get("expression") or "")
            if assertion.get("role") == "primary":
                primary_expression = str(assertion.get("expression") or "")
            if parsed is not None and expected is not None:
                claims[parsed] = expected
        out[record["id"]] = {
            "pair": str(record["pair"])[-4:],
            "layer": record.get("layer"),
            "statement": record.get("statement", ""),
            "primary_expression": primary_expression,
            "primary_predicate": record.get("primary_predicate"),
            "in_scope": record.get("in_scope"),
            "expressible": record.get("expressible_with_closed_vocabulary"),
            "claims": claims,
        }
    return out


def cell_evidence(cell_dir: Path) -> dict[str, Any]:
    """该格已发布 issue 引用的断言，以及每条断言的谓词调用与真值。"""

    published: set[str] = set()
    completed = cell_dir / "discover-completed.json"
    if completed.is_file():
        try:
            payload = json.loads(completed.read_text())
        except (OSError, json.JSONDecodeError):
            payload = {}
        for issue in payload.get("issues") or ():
            published.update(issue.get("assertion_ids") or ())
    calls: list[dict[str, Any]] = []
    for record_path in sorted(cell_dir.glob("records/*release-results*/record.json")):
        try:
            payload = json.loads(record_path.read_text())
        except (OSError, json.JSONDecodeError):
            continue

        def walk(node: Any) -> None:
            if isinstance(node, dict):
                detail = node.get("check_detail")
                if isinstance(detail, dict):
                    assertion_id = node.get("assertion_id")
                    for trace in detail.get("function_call_trace") or ():
                        name = trace.get("function")
                        kwargs = trace.get("kwargs") or {}
                        if not name:
                            continue
                        calls.append(
                            {
                                "assertion_id": assertion_id,
                                "published": assertion_id in published,
                                "predicate": name,
                                "bindings": tuple(sorted(kwargs.items())),
                                "result": trace.get("result"),
                                "assertion_truth": node.get("truth_value"),
                            }
                        )
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)

        walk(payload)
    return {"published_assertion_ids": sorted(published), "calls": calls}


def tier_a(record: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    """确定性判定。匹配即返回它匹配到的那一条，让判定可复核。"""

    for call in evidence["calls"]:
        if not call["published"]:
            continue
        key = (call["predicate"], call["bindings"])
        expected = record["claims"].get(key)
        if expected is None:
            continue
        if call["result"] is expected:
            return {
                "matched": True,
                "assertion_id": call["assertion_id"],
                "predicate": call["predicate"],
                "bindings": dict(call["bindings"]),
                "result": call["result"],
                "expected": expected,
            }
    return {"matched": False}


def _diff(record: dict[str, Any], call: dict[str, Any]) -> list[str]:
    """台账 primary 与一条产出断言逐项差异 —— B 层人工判断看的就是这个。"""

    primary = next(iter(record["claims"]), None)
    if primary is None:
        return ["台账无机械可判的断言"]
    (predicate, bindings) = primary
    expected = record["claims"][primary]
    out = []
    if predicate != call["predicate"]:
        out.append(f"谓词 {predicate} vs {call['predicate']}")
    ledger_bindings, call_bindings = dict(bindings), dict(call["bindings"])
    for key in sorted(set(ledger_bindings) | set(call_bindings)):
        left, right = ledger_bindings.get(key), call_bindings.get(key)
        if left != right:
            out.append(f"{key}: {left!r} vs {right!r}")
    if call["result"] is not expected:
        out.append(f"真值 期望 {expected} vs 实测 {call['result']}")
    return out or ["无差异（应已被 A 层确认）"]


def build(base: Path) -> dict[str, Any]:
    ledger = ledger_claims()
    cells = []
    for completed in sorted(base.glob("run*/*/discover-completed.json")):
        match = _CELL.match(completed.parent.name)
        if match:
            cells.append((completed.parent.parent.name, match.group(1), match.group(2), completed.parent))
    grid = sorted({pair for _r, pair, _a, _d in cells})
    positions = []
    for record_id, record in sorted(ledger.items()):
        if record["pair"] not in grid:
            continue
        if not record["in_scope"]:
            continue
        for round_name, pair, arm, directory in cells:
            if pair != record["pair"]:
                continue
            evidence = cell_evidence(directory)
            verdict = tier_a(record, evidence)
            entry = {
                "record_id": record_id,
                "cell": f"{round_name}/{pair}-{arm}",
                "layer": record["layer"],
                "expressible_with_closed_vocabulary": record["expressible"],
                "tier_a": verdict,
            }
            if not verdict["matched"]:
                entry["comparison"] = {
                    "ledger_primary": record["primary_expression"],
                    "candidates": [
                        {
                            "assertion_id": call["assertion_id"],
                            "predicate": call["predicate"],
                            "bindings": dict(call["bindings"]),
                            "result": call["result"],
                            "differs_in": _diff(record, call),
                        }
                        for call in evidence["calls"]
                        if call["published"]
                    ],
                }
            positions.append(entry)
    return {
        "base": str(base),
        "grid": grid,
        "records": sorted({p["record_id"] for p in positions}),
        "positions": positions,
        "tier_a_confirmed": sum(1 for p in positions if p["tier_a"]["matched"]),
        "needs_human": sum(1 for p in positions if not p["tier_a"]["matched"]),
    }


def apply_human(built: dict[str, Any], verdicts: dict[str, Any]) -> dict[str, Any]:
    """合入人工判定并执行 C 层分歧闸。

    `verdicts` 形如 `{"<record_id>|<cell>": {"hit": true, "equivalence_form": ..., "argument": ...}}`。
    """

    problems: list[str] = []
    audit = []
    for entry in built["positions"]:
        key = f"{entry['record_id']}|{entry['cell']}"
        human = verdicts.get(key)
        a_hit = entry["tier_a"]["matched"]
        if a_hit:
            if human is not None and human.get("hit") is False:
                problems.append(
                    f"{key}: A 层确认命中而人工判未命中 —— 两者之一必错，不得并存"
                )
            audit.append({**entry, "hit": True, "decided_by": "tier_a"})
            continue
        if human is None:
            problems.append(f"{key}: A 层未确认且无人工判定 —— 该位未判")
            continue
        if not human.get("hit"):
            audit.append({**entry, "hit": False, "decided_by": "human", "human": human})
            continue
        form = human.get("equivalence_form")
        argument = str(human.get("argument") or "").strip()
        if form not in EQUIVALENCE_FORMS:
            problems.append(
                f"{key}: 人工判命中但 equivalence_form={form!r} 不在 "
                f"HIT_CRITERION §3 的四种形态内：{list(EQUIVALENCE_FORMS)}"
            )
        if len(argument) < 20:
            problems.append(
                f"{key}: 人工判命中但等价性论证过短（{len(argument)} 字）—— C 层要求书面交代"
            )
        audit.append({**entry, "hit": True, "decided_by": "human", "human": human})
    hits = sum(1 for a in audit if a["hit"])
    by_source = collections.Counter(a["decided_by"] for a in audit if a["hit"])
    return {
        "base": built["base"],
        "positions_total": len(built["positions"]),
        "positions_audited": len(audit),
        "hits": hits,
        "hits_by_decider": dict(by_source),
        "gate_problems": problems,
        "audit": audit,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base")
    parser.add_argument("--generation")
    parser.add_argument("--verdicts", help="人工判定 JSON")
    parser.add_argument("--audit", help="审计输出路径")
    args = parser.parse_args(argv)
    if args.base:
        base = Path(args.base)
        if not base.is_absolute():
            base = REPO / base
    elif args.generation:
        base = RUNS / args.generation
    else:
        raise SystemExit("需要 --base 或 --generation")
    built = build(base)
    if not built["positions"]:
        raise SystemExit(f"{base} 下没有可判定位 —— 拒绝输出一份看起来正常的空结果")
    if args.verdicts:
        verdicts = json.loads(Path(args.verdicts).read_text())
        result = apply_human(built, verdicts)
        if args.audit:
            Path(args.audit).write_text(
                json.dumps(result, ensure_ascii=False, indent=1) + "\n"
            )
        print(
            f"判定位 {result['positions_total']} ｜ 命中 {result['hits']} "
            f"（A 层 {result['hits_by_decider'].get('tier_a', 0)}，"
            f"人工 {result['hits_by_decider'].get('human', 0)}）"
        )
        for problem in result["gate_problems"]:
            print(f"  ⚠️ {problem}")
        return 1 if result["gate_problems"] else 0
    print(json.dumps(built, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
