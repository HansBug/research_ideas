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
import re
import sys  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import metrics_at_k as mak  # noqa: E402  —— 比率闸门的**唯一归属地**，不在此重实现

RUNS = HERE.parents[2] / "runs" / "paper1"
TUNED_PAIRS = ("0000", "0006", "0029", "0050")

#: 「运行代理式主张」的**候选**指纹：闭词表无法把结构主张绑到瞬时伪状态（`Junction*`/`Join*`/
#: `fork*`/`choice*`），产出方于是改用下游可占据后继。见 `HIT_CRITERION.md` §4.5。
#:
#: ## ⚠️ 故意过宽，且这个方向是有意选的
#:
#: 首版写成收紧式（要求「伪状态」与「代理/后继」在 40 字内同现）。逐条人工核对发现它**漏了 3 条**
#: 真代理，根因是一个字：我写 `后继`、原文写 `后续`。
#:
#: 但真正的教训不是那个 bug。**这个数只用于算上限，而在上限计算里过度包含是安全方向** ——
#: 上限变松不会低估歧义影响，漏包含才会。收紧的动机是「精确」，而精确性在这里是错误的优化目标。
#:
#: 所以：本正则**故意过宽**，输出一律标为「候选」而非「确认」。确认数必须由人逐条读原文给出
#: （已知过宽命中的例子：`0050` 的 `ISSUE-M004-front-distance-missing` 说「不能由路由变量或仅以
#: 事件名代理替代」，那是**拒绝**用代理；`0035` 的两条用的是「动作声明作行为需求的结构代理」，
#: 与伪状态无关）。
_PROXY = re.compile(r"瞬时伪状态|运行代理|以其后续|下游代理|代理|proxy|transient pseudo")

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
            "boundary": entry.get("boundary_ruling") or "in_scope",
            "predicate": entry.get("primary_predicate") or "—",
            "statement": str(entry.get("statement") or "").strip(),
            "claude": series.get("claude"),
            "gpt": series.get("gpt"),
        })
    return rows


def proxy_reading_bound(generation: str, pos_rows: list[dict]) -> dict | None:
    """读法 A 的**上限**（`HIT_CRITERION.md` §4.5 要求并列报出）。

    读法 A（把 issue 的命题读成它引用的 requirement）需要逐条命题人工匹配，**机械算不出来**。
    但它的上限可以：把每条**候选**代理式 issue 所在 (pair, 臂, 轮) 的**全部**未命中位都当成命中。

    两重过宽叠加（候选过滤器过宽 + 该格该轮全部未命中位都算），所以这是一个**很松的上限**。
    松是有意的：按「先算上限」的判据顺序，若连这个上限都不足以翻转结论，就不必进入逐条裁定。

    返回 None 表示该代次无候选。
    """

    base = RUNS / f"matrix-{generation}"
    if not base.is_dir():
        return None
    index = {r["record_id"]: r for r in pos_rows}
    gain: set[tuple[str, str, int]] = set()
    proxy_issues = 0
    for run_dir in sorted(base.glob("run*")):
        if not run_dir.name[3:].isdigit():
            continue
        for cell in sorted(p for p in run_dir.iterdir() if p.is_dir() and ".try" not in p.name):
            final = cell / "discover-completed.json"
            if not final.is_file() or "-" not in cell.name:
                continue
            pair, arm = cell.name.rsplit("-", 1)
            issues = json.loads(final.read_text()).get("issues") or []
            found = [i for i in issues if _PROXY.search(str(i.get("rationale") or ""))]
            if not found:
                continue
            proxy_issues += len(found)
            slot = int(run_dir.name[3:]) - 1
            for record_id, row in index.items():
                if row["pair"] != pair:
                    continue
                series = row.get(arm)
                if isinstance(series, list) and slot < len(series) and series[slot] == 0:
                    gain.add((record_id, arm, slot))
    if not proxy_issues:
        return None
    return {"proxy_issues": proxy_issues, "upper_bound_gain": len(gain),
            "slots": sorted(gain)}


def _series_md(series) -> str:
    if not isinstance(series, list):
        return "· · ·"
    return " ".join("✅" if v == 1 else ("✗" if v == 0 else "·") for v in series)


def _hits(series) -> int:
    return sum(1 for v in series if v == 1) if isinstance(series, list) else 0


def run_validity(generation: str) -> list[str]:
    """运行有效性证据：代码版本 + 模型漂移 + src 冻结。

    报告必须**自带**这些，而不是让读者自己去跑（§3.7 自包含）。三项都可从冻结产物机械复算。

    `src` 冻结那一项特别值得机械化：它是**双侧**判据（有改动就非空），不依赖我记得去查什么。
    对照今天早些时候的 C-0 —— `predicate_api.py` 被误提交，而我用一个单侧 grep 确认「没问题」。
    """

    base = RUNS / f"matrix-{generation}"
    out = ["#### 运行有效性（可从冻结产物机械复算）\n"]
    version = base / "CODE_VERSION.txt"
    if version.is_file():
        lines = [l.strip() for l in version.read_text().splitlines() if l.strip()]
        out.append(f"- 代码版本：`{lines[0][:12] if lines else '?'}`"
                   + (f"，src 最后一次改动 `{lines[1]}`" if len(lines) > 1 else ""))
        out.append(f"- **src 冻结**：复算 `git log {lines[0][:12] if lines else 'BASE'}..HEAD -- "
                   f"'.../feedback_loop/src/'`，应为空")
    else:
        out.append(f"- ⚠️ 无 `CODE_VERSION.txt` —— 该代次的代码版本只能靠时间戳反推（§3.5.1 要求先 push）")
    drift: collections.Counter = collections.Counter()
    for run_dir in sorted(base.glob("run*")) if base.is_dir() else []:
        for record in run_dir.rglob("*llm-call*/record.json"):
            try:
                payload = json.loads(record.read_text())
            except Exception:
                continue
            asked = payload.get("request_model") or payload.get("model")
            got = payload.get("response_model") or payload.get("model")
            if asked:
                drift[(str(asked), str(got))] += 1
    if drift:
        bad = {k: v for k, v in drift.items() if k[0] != k[1]}
        out.append(f"- 模型漂移：{'**零**' if not bad else f'⚠️ **{sum(bad.values())} 次不一致** {bad}'}"
                   f"（共 {sum(drift.values())} 次调用）")
    out.append("")
    return out


def render(generation: str, verdicts_path: pathlib.Path) -> str:
    cell_rows = cells(generation)
    pos_rows = positions(generation, verdicts_path)
    out: list[str] = run_validity(generation)

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
    oos = [r for r in pos_rows if r["boundary"] == "out_of_scope"]
    out.append(f"命中 **{hit_pos}/{n_pos} = {hit_pos / n_pos * 100:.1f}%**（`hit@1`）。"
               "**全部记录入表入算，不过滤、不分带。**\n")
    if oos:
        # 越界记录**不静默剔除**：两个分母都报。静默剔除会让读者无法核对方向 —— 而这次剔除使
        # 数字**下降**（越界的那条是 6/6 命中），若只报剔除后的数，读者会以为剔除是自利的。
        k = sum(len(r["claude"] or []) + len(r["gpt"] or []) for r in oos)
        kh = sum(_hits(r["claude"]) + _hits(r["gpt"]) for r in oos)
        out.append(
            f"⚠️ 其中 **{len(oos)} 条**经独立边界裁定为 `out_of_scope`"
            f"（{'、'.join('`' + r['record_id'] + '`' for r in oos)}），占 {k} 位、命中 {kh} 位。"
            f"**剔除后：{hit_pos - kh}/{n_pos - k} = {(hit_pos - kh) / (n_pos - k) * 100:.1f}%** —— "
            f"注意方向是**下降**，因为越界记录在命中侧。两个分母都列，不静默剔除。\n")
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

    # ---- 读法 A 的上限（§4.5 强制并列）----
    bound = proxy_reading_bound(generation, pos_rows)
    out.append("#### `HIT_CRITERION.md` §4.5 强制并列：伪状态**运行代理**式主张的双读法\n")
    if bound is None:
        out.append("本代次**无**代理式 issue，两读法数值相同。\n")
    else:
        gain = bound["upper_bound_gain"]
        out.append(
            f"本代次有 **{bound['proxy_issues']}** 条**候选** issue 疑似用「下游可占据后继」替代无法"
            f"绑定的瞬时伪状态（过滤器**故意过宽**，确认数须人工逐条读原文；v23 实测 14 候选里 7 条真、"
            f"7 条假 —— 假的包括「**拒绝**用代理」与「动作声明作结构代理」两类）。"
            f"一条 issue 的命题读成**它引用的 requirement**（读法 A）还是**断言的字面主张**（读法 B）"
            f"影响判定，而本文件此前未规定走向。\n")
        out.append("| 读法 | `hit@1` | 说明 |")
        out.append("| :-- | --: | :-- |")
        out.append(f"| **B（判定所用）** | **{hit_pos}/{n_pos} = {hit_pos / n_pos * 100:.1f}%** | "
                   "断言字面主张；§4「更弱的命题」不算命中 |")
        out.append(f"| A 的**极宽上限** | {hit_pos + gain}/{n_pos} = "
                   f"{(hit_pos + gain) / n_pos * 100:.1f}% | "
                   f"候选过滤器过宽 **＋** 该格该轮全部未命中位都算命中（+{gain} 位）—— 两重过宽叠加 |")
        out.append("")
        out.append(f"增量上限 **{(hit_pos + gain) / n_pos * 100 - hit_pos / n_pos * 100:+.1f}pp**。"
                   "上限口径极度宽松，逐条匹配远低于此 —— 但它可复算，且足以判断该歧义能否翻转结论。\n")

    # ---- 逐带小计（不出比率，比率由 metrics_at_k 的闸门管）----
    out.append("#### 逐问题类型命中小计 —— 「哪类缺陷发现得好」\n")
    out.append("比率是否够格报由 `metrics_at_k.ratio_gate()` 裁定（**闸门的唯一归属地**，本文件不重实现）。"
               "⛔ = 该层分母或粒度不满足，比率不可作描述性结论，只看原始计数。\n")
    out.append("| 问题类型（layer） | 记录 | 判定位 | 命中位 | hit@1 | hit@3 | hit@all | 闸门 |")
    out.append("| :-- | --: | --: | --: | --: | --: | --: | :-: |")
    gated: list[tuple[str, list[str]]] = []
    for band in sorted({r["layer"] for r in pos_rows}):
        group = [r for r in pos_rows if r["layer"] == band]
        if not group:
            continue
        npos = sum(len(r["claude"] or []) + len(r["gpt"] or []) for r in group)
        nhit = sum(_hits(r["claude"]) + _hits(r["gpt"]) for r in group)
        at3 = sum(1 for r in group for s in (r["claude"], r["gpt"]) if _hits(s) >= 1)
        atall = sum(1 for r in group for s in (r["claude"], r["gpt"])
                    if isinstance(s, list) and s and all(v == 1 for v in s))
        failed = mak.ratio_gate([r["record_id"] for r in group], npos)
        mark = "✅" if not failed else "⛔"
        out.append(f"| `{band}` | {len(group)} | {npos} | {nhit} | "
                   f"{nhit / npos * 100:.1f}% | {at3}/{len(group) * 2} = {at3 / (len(group) * 2) * 100:.1f}% | "
                   f"{atall}/{len(group) * 2} = {atall / (len(group) * 2) * 100:.1f}% | {mark} |")
        if failed:
            gated.append((band, failed))
    out.append("")
    for band, failed in gated:
        out.append(f"- ⛔ `{band}`：" + "；".join(failed))
    if gated:
        out.append("")
    # 全体一行也过闸门 —— 它才是报告里最常被引用的那个数。
    whole = mak.ratio_gate([r["record_id"] for r in pos_rows], n_pos)
    out.append(f"**全体 `hit@1` = {hit_pos}/{n_pos} = {hit_pos / n_pos * 100:.1f}%**，闸门 "
               + ("✅ 够格报为描述性比率" if not whole else "⛔ " + "；".join(whole)) + "。")
    infer = mak.ratio_gate([r["record_id"] for r in pos_rows], n_pos, inferential=True)
    out.append(f"跨代次差的**显著性**：" + ("✅ 可断言" if not infer else "⛔ " + "；".join(infer)) + "\n")
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
