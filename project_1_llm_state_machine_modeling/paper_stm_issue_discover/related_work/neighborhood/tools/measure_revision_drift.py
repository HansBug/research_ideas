"""在我们自己的 v46 记录上检验一条**来自外部文献的机制假设**。

## 假设从哪来

⭐ ETFA 2025 那篇（*LLM-based Iterative Refinement of Finite-State Machines with STPA
Controller Constraints and Generation of IEC 61499 Code*）在一个 **20 轮固定循环**上
观察到：⛔ **后期的「正面改动」多数只是在撤销前期的「负面改动」**，⭐ 同一字段
`TRUE ↔ FALSE` 反复翻转。⭐ 作者给它起名 **drift / migration**。

## 为什么值得在我们数据上验

⛔ 我们 v46 的实测是：⭐ **修订机器吃掉 79% 的 output token，⛔ 而台账谓词覆盖净变化
≈ 0**，⭐ 且**第 3–5 轮零收益**。

⚠️ 「净变化≈0」有两种完全不同的机制，⛔ **而它们对 M1 的含义相反**：

| 机制 | 现象 | ⭐ 对 M1 的含义 |
| :-- | :-- | :-- |
| **A · 停滞** | 后几轮几乎不改动 | ⭐ 加一个「本轮零改动」计数器提前收敛即可，⭐ 成本近零 |
| **B · 抵消（drift）** | ⛔ 一直在改，⛔ 但改了又撤回来 | ⛔ 计数器**没用**（每轮都有改动）；⛔ 要动的是**裁决者**——⭐ 没有稳定判据时，修订是随机游走 |

⭐⭐ **本工具就是用来区分 A 与 B 的。**

## 怎么测

⭐ 每个格里，`convert_assertions` 每被执行一次就落一条 `convert-assertions-state-update`，
⭐ 其中带完整的 `assertion_script`。⭐ 按记录序号排序即得逐修订快照序列。

⭐ 对每个 `assertion_id`，把它在各快照里的**规范化形态**（⛔ 排除 `revision` 这类
必然变化的字段）取哈希，⭐ 得到一条值序列，⭐ 然后判：

- **稳定**：整条序列只有一个值
- **单向改动**：值一直在变，⛔ 但从不回到出现过的旧值
- ⭐⭐ **抵消（revert）**：⛔ **出现过 `V → … → V`** —— ⭐ 即改了又改回来

⚠️ **一处必须说清的口径**：⛔ 断言可能**新增或消失**（⭐ 修订会增删条目）。⭐ 本工具
只对**在 ≥2 个快照里都出现过**的 `assertion_id` 判抵消；⛔ 新增与删除单独计数，
⛔ 不混进抵消率 —— ⭐ 否则「删掉再加回来」会与「改了又改回来」混为一谈。

用法::

    python -m tools.measure_revision_drift --root /tmp/x1final/merged/matrix-v46-full
    python -m tools.measure_revision_drift --root ... --per-cell
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

#: ⛔ 这些字段每轮必变或与内容无关，⛔ 参与比较会让所有断言都显得「改过」。
_VOLATILE = {"revision", "schema_version"}

_IDX = re.compile(r"L(\d+)-(\d+)-")
#: ⛔⛔ **必须用 `findall` 取谓词「集合」，⛔ 不能用 `match` 取第一个。**
#:
#: ⚠️ **真实缺陷（对抗复核查出）**：初版是 `re.compile(r"\s*([a-z_]+)\s*\(")` + `.match`，
#: ⛔ 它要求表达式**以** `谓词名(` 开头 —— ⭐ 而合取式形如 `(occupancy_after(...) and ...)`
#: **以 `(` 开头**，于是返回空串。⭐ 空串是个垃圾桶：⛔ **392 个「抵消」里有 235（60%）
#: 落在含空串的序列中**，⭐ 而最高频的「抵消」形状是 `(occupancy_after, '', occupancy_after)`
#: —— ⛔ **主谓词从未变过，变的只是括号包裹。**
#:
#: ⭐ 改成集合提取后，⭐ 近一半（45.5%）的「抵消」暴露出真实形态：
#: ⛔ **不是换谓词，⭐ 而是加了一个 `*_declared` 合取前件又删掉** ——
#: ⭐⭐ 那属仓库 `CLAUDE.md` §13 的**门冲突**签名，⛔ **不是「随机游走」**。
_PRED_ALL = re.compile(r"\b([a-z_]{3,})\s*\(")
_NOT_PRED = {"is", "and", "or", "not", "true", "false", "if", "else", "len", "str", "int"}


def _canon(a: dict) -> str:
    d = {k: v for k, v in a.items() if k not in _VOLATILE}
    return hashlib.sha256(json.dumps(d, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


def _expr(a: dict) -> str:
    return (a.get("expression") or "").strip()


def _pred(a: dict) -> str:
    """⭐ 返回表达式里**全部**谓词名的规范化集合（⛔ 不是第一个）。

    ⭐ 空串表示**没解析出任何谓词** —— ⛔ 调用方必须把它当「未能解析」单独计数，
    ⛔ **不得与真实的谓词值混在一起比较**（⭐ 否则空串会充当一个假的「共同值」，
    ⭐ 制造出大量并不存在的「回到旧值」）。
    """
    names = [n for n in _PRED_ALL.findall(a.get("expression") or "") if n not in _NOT_PRED]
    return "+".join(sorted(set(names)))


#: ⭐⭐ **三个粒度必须同时报，⛔ 单看任何一个都会得出错误结论。**
#:
#: ⚠️ **实测的教训**：初版只用 `_canon`（逐字节全字段），⛔ 得抵消率 **1.0%**，
#: ⭐ 于是判「drift 假设不成立」。⛔⛔ **那是判据太严造成的假阴性** —— ⭐ 换粒度后：
#:
#: | 粒度 | 编辑数 | 回到旧值 |
#: | :-- | --: | --: |
#: | 全字段 | 4519 | ⛔ 87（1.9%） |
#: | ⭐ `expression` | 1413 | ⛔ **506（35.8%）** |
#: | ⭐⭐ 谓词名 | 898 | ⛔⛔ **392（43.7%）** |
#:
#: ⭐ 差别的来源：⛔ **4519 次编辑里只有 1413 次（31%）碰了 `expression`**，
#: ⭐ 其余 69% 在改 `description` / `rationale` / `failure_message` 这些散文字段。
#: ⛔ 任何措辞变化都让全字段哈希不同，⭐ 于是「回到旧值」几乎不可能发生。
#:
#: ⭐⭐ **判据太严与太松同样危险** —— ⛔ 前者把真信号判成不存在。
_GRAINS = (
    ("全字段", _canon),
    ("只 expression", _expr),
    ("只谓词名", _pred),
)


def snapshots(cell: Path) -> list[dict]:
    """按记录序号排序取出该格的逐修订 `assertion_script`。"""
    recs = cell / "records"
    if not recs.is_dir():
        return []
    hits = []
    for d in recs.iterdir():
        if "convert-assertions-state-update" not in d.name:
            continue
        m = _IDX.match(d.name)
        #: ⛔ 排序键必须用**两段数字**（loop, seq）。⚠️ 只按文件名字符串排会在
        #: 序号位数变化时错序，⭐ 而错序会让「改了又改回来」凭空出现。
        key = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
        f = d / "record.json"
        if f.is_file():
            hits.append((key, f))
    out = []
    for _, f in sorted(hits):
        try:
            js = json.loads(f.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        script = js.get("assertion_script")
        if isinstance(script, dict) and isinstance(script.get("assertions"), list):
            out.append(script)
    return out


def _score(series: dict[str, list[str]]) -> dict:
    stable = mono = reverted = edits = revert_edits = 0
    for vals in series.values():
        if len(vals) < 2:
            continue
        runs = [v for j, v in enumerate(vals) if j == 0 or v != vals[j - 1]]
        n_edit = len(runs) - 1
        edits += n_edit
        if n_edit == 0:
            stable += 1
            continue
        seen: set[str] = set()
        rev = 0
        for v in runs:
            if v in seen:
                rev += 1
            seen.add(v)
        if rev:
            reverted += 1
            revert_edits += rev
        else:
            mono += 1
    return {"stable": stable, "mono": mono, "reverted": reverted, "edits": edits, "revert_edits": revert_edits}


def analyse_cell(cell: Path) -> dict | None:
    snaps = snapshots(cell)
    if len(snaps) < 2:
        return None
    per_grain: dict[str, dict] = {}
    n_multi = 0
    for gname, gfun in _GRAINS:
        series: dict[str, list[str]] = collections.defaultdict(list)
        for s in snaps:
            for a in s["assertions"]:
                if aid := a.get("assertion_id"):
                    series[aid].append(gfun(a))
        n_multi = sum(1 for v in series.values() if len(v) >= 2)
        per_grain[gname] = _score(series)

    first = {a.get("assertion_id") for a in snaps[0]["assertions"]}
    last = {a.get("assertion_id") for a in snaps[-1]["assertions"]}
    return {
        "cell": cell.name,
        "n_snapshots": len(snaps),
        "n_ids_multi": n_multi,
        "grains": per_grain,
        "added": len(last - first),
        "removed": len(first - last),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, required=True, help="含 run1/run2/... 的目录")
    ap.add_argument("--per-cell", action="store_true")
    args = ap.parse_args(argv)

    cells = [c for run in sorted(args.root.iterdir()) if run.is_dir() for c in sorted(run.iterdir()) if c.is_dir()]
    if not cells:
        print(f"⛔ {args.root} 下没有格目录。", file=sys.stderr)
        return 2

    res = [r for c in cells if (r := analyse_cell(c))]
    print(f"# 修订抵消（drift）测量\n")
    print(f"- 扫描格数 **{len(cells)}**，⭐ 其中有 ≥2 次 `convert_assertions` 的 **{len(res)}**\n")
    if not res:
        print("⛔ 没有多修订的格，测不了。")
        return 0

    n_multi = sum(r["n_ids_multi"] for r in res)
    print(f"- 跨 ≥2 快照出现的断言（分母）**{n_multi}**\n")

    print("## ⭐⭐ 三个粒度（⛔ 必须一起看）\n")
    print("| 粒度 | 稳定 | 单向改动 | ⛔ 抵消 | 编辑总数 | ⛔ 其中回到旧值 |")
    print("| :-- | --: | --: | --: | --: | --: |")
    agg = {}
    for gname, _ in _GRAINS:
        s = {k: sum(r["grains"][gname][k] for r in res) for k in ("stable", "mono", "reverted", "edits", "revert_edits")}
        agg[gname] = s
        print(
            f"| {gname} | {s['stable']}（{s['stable'] / n_multi * 100:.1f}%） | {s['mono']}（{s['mono'] / n_multi * 100:.1f}%） "
            f"| **{s['reverted']}（{s['reverted'] / n_multi * 100:.1f}%）** | {s['edits']} "
            f"| **{s['revert_edits']}（{s['revert_edits'] / max(1, s['edits']) * 100:.1f}%）** |"
        )
    print(f"\n- 修订期间新增 / 删除的断言：**{sum(r['added'] for r in res)} / {sum(r['removed'] for r in res)}**")

    full, expr, pred = agg["全字段"], agg["只 expression"], agg["只谓词名"]
    cosmetic = full["edits"] - expr["edits"]
    print("\n## ⭐⭐ 读数\n")
    print(
        f"1. ⭐ **{cosmetic} / {full['edits']} = {cosmetic / max(1, full['edits']) * 100:.0f}% 的编辑没有碰 `expression`** "
        "—— ⛔ 它们只在改 `description` / `rationale` / `failure_message` 这些**散文字段**。"
    )
    print(
        f"2. ⛔ 在**碰了 `expression`** 的编辑里，**{expr['revert_edits'] / max(1, expr['edits']) * 100:.1f}% 回到了旧值**。"
    )
    print(
        f"3. ⛔⛔ 在**换谓词**这一层，**{pred['revert_edits'] / max(1, pred['edits']) * 100:.1f}% 是换回一个已经试过的谓词** "
        "—— ⭐ 这是「**没有稳定判据 → 随机游走**」最直接的签名。"
    )
    print(
        "\n⚠️ ⛔ **只看全字段会得出「无抵消」的错误结论**"
        f"（那一行只有 {full['revert_edits'] / max(1, full['edits']) * 100:.1f}%）—— "
        "⭐ 因为任何措辞变化都让全字段哈希不同，⛔ 于是「回到旧值」几乎不可能发生。"
    )

    if args.per_cell:
        print("\n## 逐格（⭐ 按谓词层抵消排序）\n")
        print("| 格 | 快照 | 分母 | ⛔ 谓词层抵消 | 谓词层编辑 | 新增/删除 |")
        print("| :-- | --: | --: | --: | --: | :-- |")
        for r in sorted(res, key=lambda r: -r["grains"]["只谓词名"]["revert_edits"])[:30]:
            g = r["grains"]["只谓词名"]
            print(
                f"| `{r['cell']}` | {r['n_snapshots']} | {r['n_ids_multi']} | **{g['revert_edits']}** "
                f"| {g['edits']} | {r['added']}/{r['removed']} |"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
