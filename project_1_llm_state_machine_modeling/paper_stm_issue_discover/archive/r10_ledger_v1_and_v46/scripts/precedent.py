"""按台账记录查历代判例：判过什么、按哪种等价形态、理由是什么。

## 为什么需要它

判定是本流水线里**最大的一个独立误差源**，而且误差方向单向偏低
（见 [adjudication_recheck.py](./adjudication_recheck.py) 的模块说明：v41 的 6 位判错全是
「命中被判成未命中」）。`adjudication_recheck` 是**事后**安全网 —— 它把「同一形态判出两种
结果」的位捞出来交给人重读。事后捞总比不捞好，但更省事的是**判之前先看判例**。

324 格一代要判约 594 位。没有判例索引时，同一条台账记录在不同 pair、不同轮次上会被反复
重新推理，而每次重新推理都是一次独立的犯错机会；有判例时，绝大多数位只需确认「这次的 issue
是不是与判过命中的那种措辞同形」。

## 这个脚本做什么，不做什么

**做**：把历代对某条记录的判定、等价形态、理由聚合到一起，并给出该记录在各代的命中分布。

**不做**：不给建议、不猜本代该判什么、不做任何字面匹配打分。

这条边界与 `adjudication_recheck` 同源，理由也同一条：**机械代理只能定位，不能裁定**。
两条 issue 字面接近不等于陈述同一个缺陷 —— 本目录有过实证，v20run1 有两条产出触及了正确的
元素却得出与台账**相反**的结论。所以本脚本只呈现历史，不参与判断；看完判例仍要读本代的
issue 原文与台账原文。

⚠️ 判例是**参考**不是**先例约束**。若本代的产出形态确实不同，就该判出不同结果 —— 那不是
不一致，那是判对了。真正的不一致是「同形态判出两种结果」，那由 `adjudication_recheck` 抓。

用法::

    precedent.py EIS-0040-01
    precedent.py --pair 0040
    precedent.py --all --hits-only
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

#: 历代人工判定文件。顺序即时间序，后面的代次更接近当前口径。
#: 只收**已完成判定**的代次；进行中的代次不入判例，否则会拿半成品当先例。
DEFAULT_SOURCES: tuple[tuple[str, str], ...] = (
    ("v37", "/tmp/v37_human.json"),
    ("v40", "/tmp/v40_human.json"),
    ("v41", "/tmp/v41_human.json"),
    ("v44", "/tmp/v44_human.json"),
    ("v45", "/tmp/v45_human.json"),
)


def load(sources: tuple[tuple[str, str], ...] = DEFAULT_SOURCES) -> dict[str, list[dict]]:
    """`record_id -> [{generation, cell, hit, equivalence_form, argument}]`。

    读不到的代次**跳过并记名**，不静默忽略：判例少一代与判例为空长得一样，而前者只是
    文件不在本机，后者意味着这条记录从没判过 —— 两者对判定者的意义完全不同。
    """

    index: dict[str, list[dict]] = collections.defaultdict(list)
    for generation, path in sources:
        file = pathlib.Path(path)
        if not file.is_file():
            index.setdefault("__missing__", []).append({"generation": generation, "path": path})
            continue
        try:
            payload = json.loads(file.read_text())
        except (OSError, json.JSONDecodeError):
            index.setdefault("__missing__", []).append({"generation": generation, "path": path})
            continue
        for key, verdict in payload.items():
            if "|" not in key:
                continue
            record_id, cell = key.split("|", 1)
            index[record_id].append(
                {
                    "generation": generation,
                    "cell": cell,
                    "hit": bool(verdict.get("hit")),
                    "equivalence_form": verdict.get("equivalence_form"),
                    "argument": verdict.get("argument"),
                }
            )
    return dict(index)


def summarise(entries: list[dict]) -> dict:
    by_generation: dict[str, list[int]] = collections.defaultdict(list)
    forms: collections.Counter = collections.Counter()
    arguments: list[str] = []
    for entry in entries:
        by_generation[entry["generation"]].append(1 if entry["hit"] else 0)
        if entry["hit"] and entry["equivalence_form"]:
            forms[entry["equivalence_form"]] += 1
        if entry["argument"] and entry["argument"] not in arguments:
            arguments.append(entry["argument"])
    return {
        "by_generation": {g: (sum(v), len(v)) for g, v in by_generation.items()},
        "forms": dict(forms),
        "arguments": arguments,
    }


def render(record_id: str, entries: list[dict]) -> str:
    stats = summarise(entries)
    lines = [f"### {record_id}"]
    trend = "  ".join(
        f"{g} {h}/{n}" for g, (h, n) in sorted(stats["by_generation"].items())
    )
    lines.append(f"  历代: {trend or '（无判例）'}")
    if stats["forms"]:
        lines.append(
            "  命中形态: " + " ｜ ".join(f"{k} ×{v}" for k, v in stats["forms"].items())
        )
    for argument in stats["arguments"]:
        lines.append(f"  · {argument}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("record_id", nargs="?", help="如 EIS-0040-01")
    parser.add_argument("--pair", help="该 pair 的全部记录，如 0040")
    parser.add_argument("--all", action="store_true", help="全部有判例的记录")
    parser.add_argument("--hits-only", action="store_true", help="只列曾经命中过的记录")
    args = parser.parse_args(argv)

    index = load()
    missing = index.pop("__missing__", [])
    if missing:
        names = ", ".join(f"{m['generation']}({m['path']})" for m in missing)
        print(f"⚠️ 读不到的判例来源：{names} —— 下面的判例**不完整**\n", file=sys.stderr)

    if args.record_id:
        keys = [args.record_id]
    elif args.pair:
        keys = sorted(k for k in index if k.split("-")[1] == args.pair)
    elif args.all:
        keys = sorted(index)
    else:
        parser.error("给一个 record_id，或 --pair，或 --all")

    shown = 0
    for key in keys:
        entries = index.get(key)
        if not entries:
            print(f"### {key}\n  （无判例 —— 这条记录历代都没被判过）")
            continue
        if args.hits_only and not any(e["hit"] for e in entries):
            continue
        print(render(key, entries))
        shown += 1
    if args.all or args.pair:
        print(f"\n共 {shown} 条记录有判例。⚠️ 判例是参考不是先例约束：本代产出形态若确实不同，"
              f"就该判出不同结果。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
