"""量 v23 改动 1 的效果：containment 绑定的锚点从「自前缀」移到「NL 指定的层」了吗。

## 为什么需要一个脚本而不是几条 grep

这个量在本轮被反复算过，每次口径都不同，而不同口径给出的结论互相矛盾：

    断言层，全部记录相加        480 / 302 / 63%
    需求层，全部记录相加        399 / 227 / 57%
    需求层，每格取末份           48 →  48   净 0
    断言层，每格取末份，按条数   106 →  90   −16
    断言层，逐轮消失的具体绑定           3

前两行的差别是**层**（需求 vs 断言），三四行的差别是**取样**（全部相加 vs 每格末份），四五行的
差别是**计数单位**（条数 vs 身份）。任何一个数单独出现都会被当成「那个量」，而它们回答的不是同
一个问题。所以这里把三个维度都做成显式参数，且默认输出全部组合 —— 让口径写在表里，而不是留在
某次对话中。

## 三个必须分开的维度

1. `--layer requirement|assertion` —— 需求层是「模型打算查什么」，断言层是「实际执行了什么」。
   一条需求可按 `coverage_obligation.aggregation` 展开成多条断言，所以两层的绝对数不可比。
2. `--sample last|all` —— `last` 每格只取末份记录（该格最终的状态），`all` 把该格所有修订记录
   相加（会把同一条绑定按修订次数重复计数）。判「最终产出是什么形状」只能用 `last`。
3. `--unit count|identity` —— `count` 数条数，`identity` 数不同的 `(parent, child)` 对。
   两者的差就是重复断言量：本轮正是这个差揭出「−16 是去重、不是删除」。

## 「自前缀」的定义

`parent == child` 去掉最后一段。即绑定把父锚在**模型自己声明**的那一层上 —— 这样的 containment
结构上永远返回 True，不可能成为发现。跨层则相反：`parent` 是 NL 指定的层，模型若放错就返回
False，而那个 False 就是发现。

`--nl-parent` 另报 `source_context.nl_parent` 的填充率（v23 新教的字段，历史填充 0/227）。
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

#: 断言层的表达式形态带转义引号：`containment(parent=\"...\", child=\"...\")`。
#: 首版正则用了未转义的 `"`，于是四个阶段全报 0 条 —— 一个「全零」结果看起来像「该现象不存在」，
#: 而实际是匹配器坏了。凡是全零，先怀疑匹配器。
_ASSERTION = re.compile(r'containment\(parent=\\?"([^"\\]+)\\?",\s*child=\\?"([^"\\]+)\\?"\)')

_STAGES = {
    "requirement": "split-requirements",
    "assertion": "convert-assertions",
}


def _declared_parent(child: str) -> str:
    return child.rsplit(".", 1)[0] if "." in child else ""


def _pairs_from_requirements(path: pathlib.Path) -> list[tuple[str, str, bool]]:
    """→ [(parent, child, 带 nl_parent)]"""

    try:
        payload = json.loads(path.read_text())
    except (OSError, ValueError):
        return []
    requirements = (payload.get("requirement_set") or {}).get("requirements") or []
    out = []
    for requirement in requirements:
        if requirement.get("predicate") != "containment":
            continue
        bindings = requirement.get("predicate_bindings") or {}
        context = requirement.get("source_context") or {}
        out.append((
            str(bindings.get("parent", "")),
            str(bindings.get("child", "")),
            bool(context.get("nl_parent")),
        ))
    return out


def _pairs_from_assertions(path: pathlib.Path) -> list[tuple[str, str, bool]]:
    try:
        text = path.read_text()
    except OSError:
        return []
    return [(m.group(1), m.group(2), False) for m in _ASSERTION.finditer(text)]


def measure(base: pathlib.Path, layer: str, sample: str, unit: str) -> dict:
    stage = _STAGES[layer]
    reader = _pairs_from_requirements if layer == "requirement" else _pairs_from_assertions
    # `parents[2]`，不是 `parent.parent`。路径是
    # `run1/0000-claude/records/L000-…-<stage>-state-update/record.json`，往上第一层是那个
    # `L000-…` 目录、第二层是 `records/`、**第三层才是格目录**。首版少了一层，于是 `cells` 全是
    # `records/`，随后 `cell.glob("records/…")` 找 `records/records/…` → 八个组合全报 0。
    # 本文件的 docstring 写着「凡是全零，先怀疑匹配器」，而这次坏的是路径而非正则 —— 同一条
    # 纪律仍然适用：**全零是「测不到」，不是「不存在」**。「按臂」一列打印出 `records` 就是证据。
    # `.try<N>` 后缀的目录是失败后被挪开的尝试，不是格。首版把它们算进去，于是「按臂」多出一条
    # 叫 `gpt.try2` 的臂，且它的绑定被计入总量 —— 一次失败运行的中间产物混进了最终形状统计。
    # 与 `generation_history.py` 同一条口径（那里写的是 `"try" not in p.name`）。
    cells = sorted({
        p.parents[2] for p in base.glob(f"run*/*/records/*{stage}-state-update/record.json")
        if ".try" not in p.parents[2].name
    })
    if not cells:
        raise SystemExit(
            f"ERROR: no {stage} records under {base}. Refusing to report zeros -- a zero here "
            "reads as 'the shape does not occur', which is what a broken matcher also looks like."
        )
    self_prefix: collections.Counter = collections.Counter()
    cross: collections.Counter = collections.Counter()
    with_nl: collections.Counter = collections.Counter()
    per_cell = {}
    for cell in cells:
        records = sorted(cell.glob(f"records/*{stage}-state-update/record.json"))
        chosen = records[-1:] if sample == "last" else records
        seen: set[tuple[str, str]] = set()
        s = c = n = 0
        for record in chosen:
            for parent, child, has_nl in reader(record):
                key = (parent, child)
                if unit == "identity":
                    if key in seen:
                        continue
                    seen.add(key)
                if parent == _declared_parent(child):
                    s += 1
                else:
                    c += 1
                if has_nl:
                    n += 1
        label = f"{cell.parent.name}/{cell.name}"
        arm = cell.name.rsplit("-", 1)[-1]
        self_prefix[arm] += s
        cross[arm] += c
        with_nl[arm] += n
        per_cell[label] = {"self_prefix": s, "cross_level": c, "with_nl_parent": n}
    total_s, total_c = sum(self_prefix.values()), sum(cross.values())
    total = total_s + total_c
    return {
        "base": str(base),
        "layer": layer,
        "sample": sample,
        "unit": unit,
        "cells": len(cells),
        "self_prefix": total_s,
        "cross_level": total_c,
        "total": total,
        "self_prefix_pct": round(total_s / total * 100, 1) if total else None,
        "with_nl_parent": sum(with_nl.values()),
        "by_arm": {
            arm: {"self_prefix": self_prefix[arm], "cross_level": cross[arm],
                  "with_nl_parent": with_nl[arm]}
            for arm in sorted(set(self_prefix) | set(cross))
        },
        "per_cell": per_cell,
        "definition": (
            "自前缀 = parent 等于 child 去掉末段，即锚在模型自己声明的层上，结构上恒真、不可能"
            "成为发现。跨层 = parent 是 NL 指定的层，模型放错则返回 False，而那个 False 就是发现。"
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", type=pathlib.Path)
    parser.add_argument("--layer", choices=sorted(_STAGES), default=None)
    parser.add_argument("--sample", choices=("last", "all"), default=None)
    parser.add_argument("--unit", choices=("count", "identity"), default=None)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--per-cell", action="store_true")
    args = parser.parse_args(argv)

    combos = [(l, s, u)
              for l in ([args.layer] if args.layer else sorted(_STAGES))
              for s in ([args.sample] if args.sample else ("last", "all"))
              for u in ([args.unit] if args.unit else ("count", "identity"))]
    results = [measure(args.base, l, s, u) for l, s, u in combos]
    if args.json:
        print(json.dumps(results if len(results) > 1 else results[0], ensure_ascii=False, indent=1))
        return 0
    print(f"{'层':11s} {'取样':5s} {'单位':9s} {'格':>4s} {'自前缀':>6s} {'跨层':>5s} "
          f"{'自前缀%':>7s} {'带nl_parent':>11s}")
    for r in results:
        pct = f"{r['self_prefix_pct']}%" if r["self_prefix_pct"] is not None else "—"
        print(f"  {r['layer']:9s} {r['sample']:5s} {r['unit']:9s} {r['cells']:4d} "
              f"{r['self_prefix']:6d} {r['cross_level']:5d} {pct:>7s} {r['with_nl_parent']:11d}")
    print("\n按臂（取 requirement/last/count）：")
    for r in results:
        if (r["layer"], r["sample"], r["unit"]) != ("requirement", "last", "count"):
            continue
        for arm, v in r["by_arm"].items():
            print(f"  {arm:8s} 自前缀 {v['self_prefix']:4d}  跨层 {v['cross_level']:4d}  "
                  f"带 nl_parent {v['with_nl_parent']:4d}")
        if args.per_cell:
            print("\n逐格：")
            for label, v in sorted(r["per_cell"].items()):
                print(f"  {label:22s} 自前缀 {v['self_prefix']:3d} 跨层 {v['cross_level']:3d} "
                      f"nl_parent {v['with_nl_parent']:3d}")
    print("\n⚠️ 四个组合的数字**不可互相替代**。层的差别是「打算查什么」vs「实际执行了什么」；"
          "取样的差别是「最终形状」vs「累计出现」；单位的差别就是重复量。本轮五次口径错误里有三次"
          "源于把其中一个当成了「那个量」。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
