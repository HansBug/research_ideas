"""生成判定材料：**并列呈现**每个 pair 的台账期望与 X1 六格产出。⛔ 不做匹配、⛔ 不给判定。

⭐ 本脚本的职责边界与主臂 `present_for_judgment.py` 完全一致，理由也一样：判定必须人工逐条做。
那边的 docstring 记了直接证据——两条模型产出触及了正确的元素、却得出与台账**相反**的结论，
⛔ **任何按标题或元素相似度对齐的脚本都会把这两条判成命中。**

## ⛔ 三条禁止（由 tests/test_judge_material_shape.py 机械钉住）

材料里⛔ 不得出现：

1. **主臂在同一位的判定结果**（`hit` / `equivalence_form` / `argument`）。⚠️ 判定者读到「主臂这一位
   命中了」会被锚定。⭐ 这是本臂唯一能在不重判主臂（不违反 588 冻结）的前提下切断的污染通道。
2. **台账的「答案」字段**：`replay`（⚠️ 那是**期望真值**）· `assertions[].measured` ·
   `assertions[].expression` · `upstream.eight_cell_published`（往轮已发布 issue id）。
3. **四池归属**（满格 / 近满格 / 不稳定 / 零命中）。⚠️ 池由主臂结果算出，⛔ 它进材料等于把主臂的
   逐条表现告诉判定者。⭐ 池**只用于排判定顺序**，写进另一个文件（见下）。

## ⛔ 另外三个字段刻意不给，⚠️ 且这不构成两臂不对称

`primary_predicate` · `layer` · `direction`。

⭐ 主臂的 present 给 `primary_predicate`，因为那边两侧都有谓词、判定要做命题层对照。⛔ 但 X1 侧
只有散文——给台账的谓词名**没有对照对象，只剩引导作用**，而 `hit_criterion.md` §2 明写判据
「不是两者用的谓词是否相同」。⚠️ 给它反而是 §4 那条「以次充好」的入口。

`layer` / `direction` 是缺陷分类。⭐ `statement` 全文已含全部信息，分类只会提示「该找哪一类」。
⚠️ 主臂盲判样本器的注释也说 `layer`「标注者不该看到」（尽管它的实现给了——那是一处已知缺陷）。

## 物理分离：材料 vs 顺序

    materials/<seq>-<pair>.md   ← ⭐ 判定者读这个。⛔ 无池、⛔ 无主臂判定
    judging_order.tsv           ← ⛔ 判定者**不读**这个。含池归属，供事后审计排序是否分层

⚠️ 按仓库根 `CLAUDE.md` §9.5 第 6 条：**物理分离本身就是防泄漏机制**（实测约定式隔离合规率
0/2、物理拆分 2/2）。⛔ 不得因为「反正我记得不看」而把池写进材料。
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
# ⭐ `analysis/` → `src/` 这个方向的 import 是合理的：分析要读实现声明的语料位置。
# ⛔ 反方向不许（`src/` 是被测对象，它的依赖面被隔离测试钉死）。
# ⚠️ 这里刻意 import 而不是复制一份路径常量——复制就是第二真源，而语料路径一旦漂移，
# 两臂读的就是不同的输入，且看不出来。
_SRC = _HERE.parents[0] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from runner import REPORT_ROOT  # noqa: E402

PAPER = _HERE.parents[1]
MATRIX = PAPER / "discover_matrix"
LEDGER = MATRIX / "manual_review" / "expected_issue_set.json"
#: ⚠️ 主臂判定表。**只用于算池以排顺序**，⛔ 其内容一个字都不进材料。
MAIN_ARM_TIERS = MATRIX / "v46" / "verdicts" / "v46_tiers.json"

#: `00x8` 家族永久排除（`docs/protocol/nl_scope_rule.md`）。
OUT_OF_SCOPE_PAIRS = ("0008", "0018", "0028", "0038", "0048", "0058")

#: 逐条边界裁定剔除的记录。与 `metrics_at_k._boundary_ruled_ids()` 同源。
BOUNDARY_RULED = ("EIS-0043-02",)

#: ⛔ 绝不可进入材料的台账字段。
FORBIDDEN_LEDGER_FIELDS = (
    "replay",
    "assertions",
    "primary_predicate",
    "assertion_count",
    "has_negative_control",
    "upstream",
    "layer",
    "layer_basis",
    "direction",
    "element_of_M",
    "verdict",
    "decided_by",
    "expressible_with_closed_vocabulary",
    "homogeneity_group",
    "boundary_ruling",
    "boundary_rationale",
    "boundary_effect",
)


def load_reportable() -> list[dict[str, Any]]:
    """98 条 REPORTABLE：台账 126 条 − `00x8` 27 条 − 逐条边界裁定 1 条。

    ⛔ 不用台账的 `in_scope` 字段筛——它对 126 条全为 True，记的不是这件事（主臂踩过）。
    """

    payload = json.loads(LEDGER.read_text(encoding="utf-8"))
    records = payload["records"]
    kept = [
        r
        for r in records
        if str(r["pair"])[-4:] not in OUT_OF_SCOPE_PAIRS and r["id"] not in BOUNDARY_RULED
    ]
    if len(kept) != 98:
        raise SystemExit(
            f"REPORTABLE should be 98, got {len(kept)} (of {len(records)}). "
            "The denominator is the capability claim -- investigate before judging."
        )
    return kept


def main_arm_pools() -> dict[str, int]:
    """每条 REPORTABLE 记录在主臂的命中位数（0..6）。⚠️ **只用于排顺序。**"""

    payload = json.loads(MAIN_ARM_TIERS.read_text(encoding="utf-8"))
    hits: dict[str, int] = {}
    for record_id, value in payload.get("verdicts", {}).items():
        if not isinstance(value, dict):
            continue
        total = 0
        for key, series in value.items():
            if key == "direction" or not isinstance(series, list):
                continue
            total += sum(1 for v in series if v == 1)
        hits[record_id] = total
    return hits


def pool_of(hit_count: int) -> str:
    if hit_count >= 6:
        return "full"
    if hit_count == 5:
        return "near"
    if hit_count >= 1:
        return "unstable"
    return "zero"


def stratified_pair_order(records: list[dict[str, Any]]) -> list[tuple[str, dict[str, int]]]:
    """按四池**分层交错**排 pair 顺序。

    ⭐ 目的：任何时刻中断，已判 pair 集合都自动是分层代表的——于是 fallback「交已判子集」
    变成零成本，⛔ 不需要事后挑（而事后挑正是「按问题最明显挑」偏差的入口）。

    ⭐ 交错还有第二个作用：连续几个 pair 不会同属一池，⛔ 判定者形不成「这批都是满格」的印象。
    """

    pools = main_arm_pools()
    by_pair: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for record in records:
        pair = str(record["pair"])[-4:]
        by_pair[pair][pool_of(pools.get(record["id"], 0))] += 1

    # 每个 pair 的主池 = 它条目最多的那一池；平手时按固定序，保证可复现。
    priority = ("full", "near", "unstable", "zero")
    buckets: dict[str, list[str]] = {name: [] for name in priority}
    for pair in sorted(by_pair):
        counts = by_pair[pair]
        dominant = max(priority, key=lambda name: (counts.get(name, 0), -priority.index(name)))
        buckets[dominant].append(pair)

    order: list[tuple[str, dict[str, int]]] = []
    cursors = {name: 0 for name in priority}
    while any(cursors[n] < len(buckets[n]) for n in priority):
        for name in priority:
            if cursors[name] < len(buckets[name]):
                pair = buckets[name][cursors[name]]
                cursors[name] += 1
                order.append((pair, dict(by_pair[pair])))
    return order


def load_cells(run_root: Path, pair: str) -> list[dict[str, Any]]:
    """该 pair 的全部格（3 轮 × 2 臂），按 (轮, 臂) 排序。缺格如实标出。"""

    cells: list[dict[str, Any]] = []
    for round_index in (1, 2, 3):
        for arm in ("gpt", "claude"):
            path = run_root / f"run{round_index}" / f"{pair}-{arm}" / "record.json"
            if not path.is_file():
                cells.append(
                    {"round": round_index, "arm": arm, "missing": True, "issues": []}
                )
                continue
            record = json.loads(path.read_text(encoding="utf-8"))
            parsed = record.get("parsed_output") or {}
            cells.append(
                {
                    "round": round_index,
                    "arm": arm,
                    "missing": False,
                    "status": record.get("status"),
                    "failure": record.get("failure"),
                    "analysis": parsed.get("analysis"),
                    "issues": parsed.get("issues") or [],
                }
            )
    return cells


def render_pair(
    *,
    seq: int,
    pair: str,
    records: list[dict[str, Any]],
    cells: list[dict[str, Any]],
    report_root: Path,
) -> str:
    pair_dir = report_root / "pairs" / pair
    nl = (pair_dir / "nl.txt").read_text(encoding="utf-8").strip()
    puml = (pair_dir / "plantuml.puml").read_text(encoding="utf-8").strip()

    lines: list[str] = []
    lines.append(f"# 判定材料 {seq:02d} · pair {pair}")
    lines.append("")
    lines.append(
        "> ⛔ **本文件不含任何判定结果**（既无主臂的，也无台账的期望真值）。判据只有一条："
        "**我们的主张所表达的命题，与台账那条记录所表达的命题，是否指向同一个作者源缺陷。**"
    )
    lines.append(">")
    lines.append(
        "> ⭐ 判定时读下面的 **PlantUML 作者源**，⛔ 不读 `model.fcstm`（编译产物）——"
        "否则会把编译债务当成模型缺陷。"
    )
    lines.append("")
    lines.append("## 一、需求原文（NL，全文）")
    lines.append("")
    lines.append("```text")
    lines.append(nl)
    lines.append("```")
    lines.append("")
    lines.append("## 二、被审模型（PlantUML 作者源，全文）")
    lines.append("")
    lines.append("```plantuml")
    lines.append(puml)
    lines.append("```")
    lines.append("")
    lines.append(f"## 三、台账期望（本 pair {len(records)} 条，全部进能力分母）")
    lines.append("")
    for record in records:
        lines.append(f"### {record['id']}")
        lines.append("")
        lines.append(str(record.get("statement") or "").strip())
        lines.append("")
        evidence = str(record.get("nl_evidence") or "").strip()
        if evidence:
            lines.append(f"**NL 出处**：{evidence}")
            lines.append("")
        # ⭐⭐ 这个字段**必须**渲染，⛔ 它不是「答案」而是**判据本身的修正**：它记着 statement
        # 里的哪一部分归因依据**已被裁定撤回**、换用了什么判据。
        #
        # ⚠️ 初版漏了它，代价是实测出来的：X1 判定组按已撤回的 statement 判 `EIS-0000-02` 命中，
        # 而主臂判定者按改后的判据判未命中——跨臂对拍时表现为 5 位分歧，根因是**两侧在读不同的
        # 台账命题**。⛔ 那是判定伪影，方向抬高 X1。
        #
        # ⭐ 全语料只有 2 条非空（`EIS-0000-02` / `EIS-0050-01`），影响 12 位。
        superseded = str(record.get("basis_superseded_by_ruling") or "").strip()
        if superseded:
            lines.append(
                "⛔ **本条的原判据已被裁定部分撤回，判定时必须按撤回后的判据读，"
                "⛔ 不得按上面 statement 里已被放弃的那部分归因：**"
            )
            lines.append("")
            lines.append(f"> {superseded}")
            lines.append("")
    lines.append("## 四、X1 六格产出")
    lines.append("")
    for cell in cells:
        header = f"### run{cell['round']} · {cell['arm']}"
        if cell["missing"]:
            lines.append(f"{header} — ⚠️ **格缺失**（未落盘，该位记 `null`，⛔ 不记 0）")
            lines.append("")
            continue
        if cell.get("status") != "ok":
            lines.append(
                f"{header} — ⚠️ **格失败**（`{cell.get('failure')}`；该位记 `null`，⛔ 不记 0）"
            )
            lines.append("")
            continue
        lines.append(f"{header} — 报了 {len(cell['issues'])} 条")
        lines.append("")
        if not cell["issues"]:
            lines.append("⚠️ **本格未报任何 issue。**")
            lines.append("")
        for index, issue in enumerate(cell["issues"], 1):
            lines.append(f"**[{index}]** {str(issue.get('issue') or '').strip()}")
            lines.append("")
            lines.append(f"- **where**：{str(issue.get('where') or '').strip()}")
            lines.append(f"- **reason**：{str(issue.get('reason') or '').strip()}")
            lines.append("")
    lines.append("## 五、要填的位")
    lines.append("")
    lines.append(
        f"本 pair 共 {len(records)} 条记录 × 6 格 = **{len(records) * 6} 位**。"
        "每位填 `hit` / `equivalence_form`（命中时必填，四种形态之一）/ `argument`（命中时 ≥ 20 字）。"
    )
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build per-pair judging materials for the naive baseline arm."
    )
    parser.add_argument("--run-root", required=True, help="e.g. runs/paper1/x1-baseline-v1")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--report-root", default=None)
    args = parser.parse_args(argv)

    run_root = Path(args.run_root).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    materials = out_dir / "materials"
    materials.mkdir(parents=True, exist_ok=True)
    report_root = (
        Path(args.report_root).expanduser().resolve() if args.report_root else REPORT_ROOT
    )

    records = load_reportable()
    by_pair: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_pair[str(record["pair"])[-4:]].append(record)

    order = stratified_pair_order(records)
    order_lines = ["seq\tpair\trecords\tpool_full\tpool_near\tpool_unstable\tpool_zero"]
    total_positions = 0
    for seq, (pair, pools) in enumerate(order, 1):
        pair_records = sorted(by_pair[pair], key=lambda r: r["id"])
        cells = load_cells(run_root, pair)
        text = render_pair(
            seq=seq,
            pair=pair,
            records=pair_records,
            cells=cells,
            report_root=report_root,
        )
        (materials / f"{seq:02d}-{pair}.md").write_text(text, encoding="utf-8")
        total_positions += len(pair_records) * 6
        order_lines.append(
            f"{seq}\t{pair}\t{len(pair_records)}\t{pools.get('full', 0)}\t"
            f"{pools.get('near', 0)}\t{pools.get('unstable', 0)}\t{pools.get('zero', 0)}"
        )
    # ⛔ 池归属只进这个文件，判定者不读它（见模块 docstring 的物理分离）。
    (out_dir / "judging_order.tsv").write_text("\n".join(order_lines) + "\n", encoding="utf-8")

    print(
        f"wrote {len(order)} pair materials to {materials} "
        f"({total_positions} positions; expected 588)"
    )
    if total_positions != 588:
        print(
            f"⚠️ position count {total_positions} != 588 -- check the ledger and the grid",
            flush=True,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
