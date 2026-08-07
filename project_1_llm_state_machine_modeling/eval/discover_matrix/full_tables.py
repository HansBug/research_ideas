"""把一代次的**全部**格与**全部**判定位渲成 comment 可直接贴的 Markdown 表。

## 为什么需要这个工具，以及为什么它不分带

前几代次的 comment 只报了「能力主张带」的 2–4 条记录，而实际有 66 个格、204 个判定位。

**带划分本身是套错的工具，现已废止。** hold-out 服务的是泛化性声明（「在未见过的模型上命中率 X%」）。
本研究的贡献是**从真实模型归纳问题类型与判定能力** —— 语料是研究对象本身，不是留出测试集。这与工具
论文、实证研究里「看遍全部语料写规则，然后报告工具在这些语料上找到什么」是同一种设计。

而 hold-out 在此的实际后果是把分母掐死到 2 条（`DENOMINATOR_EXHAUSTION.md`：126 → 0）。一个把可测
总体摧毁到 2 条的纪律，保护不了任何主张。

**仍然全额生效的是另一条线**：不得把答案或不该可见的信息喂进去（§3.5 条款 1–3 —— prompt / gate /
运行时反馈里不得出现台账元素名、期望真值、针对单样本的特判）。这条与 hold-out 是**两条不同的线**，
此前被我捆在一起了。

所以：**全部 34 条记录、204 个判定位、66 个格一律入表入算**，不过滤、不分带。代价是**不能声称对未见
模型的泛化** —— 报告里必须写明这一点，那是主张边界，不是分母边界。

## 两张表

1. `cells()` —— 66 格：run × pair × arm，每格的 issue 数、coverage_gaps、拒答、重试痕迹
2. `positions()` —— 204 位：34 条台账记录 × 2 臂 × 3 轮，逐条带 layer / 主谓词 / 缺陷简述

分组维度是**问题类型（`layer`）**，不是带 —— 那才是「归纳问题类型与判定能力」的实际维度，也是唯一能回答「哪类缺陷发现得好、哪类差」的切法。

命中格用 ✅、未命中用 ✗、无判定用 ·（后者与 0 不同，必须可区分 —— 空结果读成「未命中」是本目录
反复出现的错误）。
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
RUNS = HERE.parents[2] / "runs" / "paper1"
TUNED_PAIRS = ("0000", "0006", "0029", "0050")

def _ledger() -> dict[str, dict]:
    payload = json.loads((HERE / "manual_review" / "expected_issue_set.json").read_text())
    records = payload.get("records") or []
    return {str(r["id"]): r for r in records}


def cells(generation: str) -> list[dict]:
    """66 格逐格实况。`.try` 目录单独计数为重试痕迹，不混入正表。"""

    base = RUNS / f"matrix-{generation}"
    if not base.is_dir():
        raise SystemExit(f"ERROR: no {base}")

    retries: collections.Counter = collections.Counter()
    for run_dir in sorted(base.glob("run*")):
        for path in run_dir.iterdir():
            if path.is_dir() and ".try" in path.name:
                retries[(run_dir.name, path.name.split(".try")[0])] += 1

    rows = []
    for run_dir in sorted(base.glob("run*")):
        if not run_dir.name[3:].isdigit():
            continue
        for cell in sorted(p for p in run_dir.iterdir() if p.is_dir() and ".try" not in p.name):
            if "-" not in cell.name:
                continue
            pair, arm = cell.name.rsplit("-", 1)
            final = cell / "discover-completed.json"
            if not final.is_file():
                rows.append({"run": run_dir.name, "pair": pair, "arm": arm,
                             "status": "未完成", "issues": None, "gaps": None,
                             "rejected": None, "retries": retries.get((run_dir.name, cell.name), 0)})
                continue
            payload = json.loads(final.read_text())
            rows.append({
                "run": run_dir.name, "pair": pair, "arm": arm, "status": "完成",
                "issues": len(payload.get("issues") or []),
                "gaps": len(payload.get("coverage_gaps") or []),
                "rejected": len(payload.get("rejected_issues") or []),
                "excluded": len(payload.get("excluded_findings") or [])
                + len(payload.get("excluded_observations") or []),
                "retries": retries.get((run_dir.name, cell.name), 0),
            })
    return rows


def positions(generation: str, verdicts_path: pathlib.Path) -> list[dict]:
    """204 位逐位实况，含层、主谓词、缺陷简述与逐轮 0/1/None。"""

    payload = json.loads(verdicts_path.read_text())
    verdicts = payload.get("verdicts") or {}
    ledger = _ledger()

    rows = []
    for record_id in sorted(verdicts):
        if record_id == "direction":   # 合流元数据，不是台账记录
            continue
        entry = ledger.get(record_id) or {}
        pair = str(entry.get("pair", ""))[-4:] or record_id.split("-")[1]
        series = verdicts[record_id]
        rows.append({
            "record_id": record_id,
            "pair": pair,
            "layer": entry.get("layer") or "?",
            "predicate": entry.get("primary_predicate") or "—",
            "statement": str(entry.get("statement") or "").strip(),
            "claude": series.get("claude"),
            "gpt": series.get("gpt"),
        })
    return rows


def _series_md(series) -> str:
    if not isinstance(series, list):
        return "· · ·"
    return " ".join("✅" if v == 1 else ("✗" if v == 0 else "·") for v in series)


def _hits(series) -> int:
    return sum(1 for v in series if v == 1) if isinstance(series, list) else 0


def render(generation: str, verdicts_path: pathlib.Path) -> str:
    cell_rows = cells(generation)
    pos_rows = positions(generation, verdicts_path)
    out: list[str] = []

    # ---- 表 1：66 格 ----
    done = sum(1 for r in cell_rows if r["status"] == "完成")
    total_issues = sum(r["issues"] or 0 for r in cell_rows)
    total_retry = sum(r["retries"] for r in cell_rows)
    out.append(f"### 表 1 · 全部 {len(cell_rows)} 格逐格实况\n")
    out.append(f"完成 **{done}/{len(cell_rows)}**，已发布 issue 合计 **{total_issues}** 条，"
               f"重试痕迹 **{total_retry}** 次。`gap` = `coverage_gaps`，`rej` = `rejected_issues`，"
               f"`exc` = `excluded_findings` + `excluded_observations`（**这三类看起来都像「没发现」**）。\n")

    pairs = sorted({r["pair"] for r in cell_rows})
    runs = sorted({r["run"] for r in cell_rows})
    index = {(r["run"], r["pair"], r["arm"]): r for r in cell_rows}
    out.append("| pair | " + " | ".join(
        f"{r[3:]}·{a}" for r in runs for a in ("claude", "gpt")) + " | 合计 |")
    out.append("| :-- | " + " | ".join(":-:" for _ in runs for _ in range(2)) + " | --: |")
    for pair in pairs:
        line, tot = [], 0
        for run in runs:
            for arm in ("claude", "gpt"):
                r = index.get((run, pair, arm))
                if not r or r["status"] != "完成":
                    line.append("—")
                    continue
                tot += r["issues"]
                extra = "".join(
                    s for s, n in (("g", r["gaps"]), ("r", r["rejected"]), ("e", r.get("excluded", 0)))
                    if n
                )
                line.append(f"{r['issues']}{('^' + extra) if extra else ''}")
        out.append(f"| `{pair}` | " + " | ".join(line) + f" | {tot} |")
    out.append("")
    out.append("上标 `g`/`r`/`e` 表示该格另有 `coverage_gaps` / `rejected_issues` / `excluded_*`。"
               "**全部 11 个 pair 均参与规则归纳**，故本表是方法在其归纳语料上的表现 —— "
               "这是主张边界（不声称对未见模型泛化），不是分母边界。\n")

    # ---- 表 2：全部判定位 ----
    n_pos = sum(len(r["claude"] or []) + len(r["gpt"] or []) for r in pos_rows)
    out.append(f"### 表 2 · 全部 {len(pos_rows)} 条台账记录 × 2 臂 × 3 轮 = {n_pos} 个判定位\n")
    hit_pos = sum(_hits(r["claude"]) + _hits(r["gpt"]) for r in pos_rows)
    out.append(f"命中 **{hit_pos}/{n_pos} = {hit_pos / n_pos * 100:.1f}%**（`hit@1`）。"
               "**全部记录入表入算，不过滤、不分带。**\n")
    out.append("| 记录 | 层 | 主谓词 | claude | gpt | 缺陷简述 |")
    out.append("| :-- | :-- | :-- | :-: | :-: | :-- |")
    for r in sorted(pos_rows, key=lambda x: (x["layer"], x["record_id"])):
        stmt = r["statement"].replace("|", "\\|").replace("\n", " ")
        if len(stmt) > 150:
            stmt = stmt[:150] + "…"
        out.append(
            f"| `{r['record_id']}` | {r['layer']} | "
            f"`{r['predicate']}` | {_series_md(r['claude'])} | {_series_md(r['gpt'])} | {stmt} |"
        )
    out.append("")

    # ---- 逐带小计（不出比率，比率由 metrics_at_k 的闸门管）----
    out.append("#### 逐问题类型命中小计 —— 「哪类缺陷发现得好」\n")
    out.append("| 问题类型（layer） | 记录 | 判定位 | 命中位 | hit@1 | hit@3 | hit@all |")
    out.append("| :-- | --: | --: | --: | --: | --: | --: |")
    for band in sorted({r["layer"] for r in pos_rows}):
        group = [r for r in pos_rows if r["layer"] == band]
        if not group:
            continue
        npos = sum(len(r["claude"] or []) + len(r["gpt"] or []) for r in group)
        nhit = sum(_hits(r["claude"]) + _hits(r["gpt"]) for r in group)
        at3 = sum(1 for r in group for s in (r["claude"], r["gpt"]) if _hits(s) >= 1)
        atall = sum(1 for r in group for s in (r["claude"], r["gpt"])
                    if isinstance(s, list) and s and all(v == 1 for v in s))
        out.append(f"| `{band}` | {len(group)} | {npos} | {nhit} | "
                   f"{nhit / npos * 100:.1f}% | {at3}/{len(group) * 2} = {at3 / (len(group) * 2) * 100:.1f}% | "
                   f"{atall}/{len(group) * 2} = {atall / (len(group) * 2) * 100:.1f}% |")
    out.append("")
    out.append("⚠️ `hit@3` / `hit@all` 按 **(记录, 臂)** 计数，不是按记录 —— 一条记录在两臂上可以"
               "一边稳定命中、一边全轮未命中，合成一个数会把这件事抹掉。分母 = 记录数 × 2 臂。")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generation", required=True)
    parser.add_argument("--verdicts", type=pathlib.Path, required=True)
    parser.add_argument("--out", type=pathlib.Path)
    args = parser.parse_args(argv)

    if not args.verdicts.is_file():
        print(f"ERROR: no {args.verdicts}", file=sys.stderr)
        return 2
    text = render(args.generation, args.verdicts)
    if args.out:
        args.out.write_text(text)
        print(f"已写入 {args.out}（{len(text.splitlines())} 行，{len(text)} 字符）")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
