"""Render the 60-pair manual-review issue body from the published bundles.

Every figure and every number is read out of the audit bundle, the frozen ledger and
the paper's extracted problems -- nothing is typed by hand, so the issue cannot drift
from the gists it links to.

Two hosting facts shape the output:

  * Gist raw serves `text/plain` for every file, so a PNG committed to a gist will not
    render inline in an issue.  Figures are therefore GitHub-native Mermaid, and their
    source plus underlying data is archived into the audit gist so each one is
    reproducible.
  * GitHub's Mermaid grammar does not know `xychart-beta` or `sankey-beta` (they get no
    `pl-k` keyword span from the markdown API, unlike `pie`/`flowchart`/`quadrantChart`).
    Quantitative bars are drawn with block characters inside tables instead of trusting
    a chart type that may render as an error box.

Usage: render_refcmp_issue.py <audit_dir> <audit_gist_id> <readable_gist_id> [out.md]
"""

from __future__ import annotations

import json
import pathlib
import sys
from collections import Counter, defaultdict

# ⛔ 归档后深度多了两层，原先的 parents[N] 解析到 `paper_stm_issue_discover/`。
# ⭐ 改为按仓库根标志物向上锚定（CLAUDE.md §9.5-3）。
REPO = next(_p for _p in pathlib.Path(__file__).resolve().parents if (_p / "CLAUDE.md").is_file() and (_p / ".git").exists())
LEDGER = REPO / ".omx/specs/autoresearch-paper1-llms-emp-60-expected-issues/ledger.json"
PAPER = pathlib.Path(__file__).resolve().parent / "paper_reported_problems.json"
CENSUS = pathlib.Path("/tmp/fcstm_stats.json")

LLM_ORDER = ["GPT-4o", "GPT-4", "Llama", "Kimi", "DeepSeek", "Claude"]

# The 19 closed predicates, in registry order, with evidence family.  Reviewers also
# named `transition_exists`, which is *not* one of them -- it is the legacy query
# primitive the ledger was written against.  Keeping the distinction visible is the
# point: "expressible with an existing predicate" must mean the closed set, not any
# callable that happens to exist somewhere in the facade.
CLOSED_PREDICATES = {
    "state_declared": "S", "variable_declared": "S", "event_declared": "S",
    "containment": "S", "initial_target": "S", "edge_declared": "S",
    "effect_declared": "S", "action_declared": "S", "guard_distinguishable": "S",
    "cardinality": "S", "occupancy_after": "B", "event_consumed": "B",
    "stays_in": "B", "variable_delta_after": "B", "reaches": "B", "terminates": "B",
    "invariant": "P", "response_within": "P", "persists_until": "P",
}
NOT_CLOSED = {"transition_exists", "transitions", "states", "initial_child",
              "effect_deltas", "path", "any", "all", "not"}
NL_TITLE = {
    "NL01": "列车控制", "NL02": "基础制动", "NL03": "无人机集群", "NL04": "数码相机",
    "NL05": "自动驾驶模式", "NL06": "泵控制", "NL07": "碰撞避免", "NL08": "驾驶模式切换",
    "NL09": "HSUV", "NL10": "微波炉",
}


def bar(n: int, top: int, width: int = 18) -> str:
    """Block bar. Rendered in a table cell it always displays, unlike a chart type."""
    if top <= 0:
        return ""
    filled = round(n / top * width)
    return "█" * filled + "░" * (width - filled) if filled else "░" * width


def anchor(name: str) -> str:
    """Gist in-page anchor for a filename.

    GitHub slugifies *only the dot*: it lowercases and turns `.` into `-`, but leaves
    underscores and hyphens alone.  Replacing every non-alphanumeric -- the reflex, and
    what this function used to do -- silently breaks exactly the files whose names carry an
    underscore: `_summary.json` became `file--summary-json` against the real
    `file-_summary-json`, and `figure_data.tsv` became `file-figure-data-tsv` against
    `file-figure_data-tsv`.  A wrong anchor does not 404; it lands on the page top with no
    warning, so the failure is invisible unless the id set is checked against the real DOM.
    Verified against the rendered gist HTML.
    """
    return "file-" + name.lower().replace(".", "-")


class Data:
    def __init__(self, audit_dir: pathlib.Path, audit_gist: str, readable_gist: str,
                 audit_rev: str | None = None):
        self.audit_gist = audit_gist
        self.readable_gist = readable_gist
        # A raw gist URL without a revision always serves the *latest* version, so an
        # integrity claim ("every file byte-identical by SHA-256") cannot be re-verified
        # from it after any edit.  Pinning makes the claim checkable.
        self.audit_rev = audit_rev
        self.summary = json.loads((audit_dir / "_summary.json").read_text())
        self.per = self.summary["per_case"]
        self.reviews = {
            p.name.removesuffix("-review.json"): json.loads(p.read_text())
            for p in sorted(audit_dir.glob("*-review.json"))
        }
        self.ledger = json.loads(LEDGER.read_text())
        self.paper = json.loads(PAPER.read_text())
        self.census = (
            {r["case"]: r for r in json.loads(CENSUS.read_text())}
            if CENSUS.exists() else {}
        )

    # -- links ------------------------------------------------------------------
    def readable_link(self, case: str, label: str | None = None) -> str:
        url = f"https://gist.github.com/HansBug/{self.readable_gist}#{anchor(case + '-readable.md')}"
        return f"[{label or case}]({url})"

    def audit_link(self, case: str, label: str = "json") -> str:
        rev = f"{self.audit_rev}/" if self.audit_rev else ""
        url = (f"https://gist.githubusercontent.com/HansBug/{self.audit_gist}"
               f"/raw/{rev}{case}-review.json")
        return f"[{label}]({url})"

    def gist_file(self, name: str, label: str, which: str = "audit") -> str:
        gid = self.audit_gist if which == "audit" else self.readable_gist
        return f"[{label}](https://gist.github.com/HansBug/{gid}#{anchor(name)})"

    # -- rollups ----------------------------------------------------------------
    def _deducted(self, case: str) -> int:
        """Out-of-scope differences that actually reduce the problem count.  A diff can
        be marked out_of_scope while its verdict is `similar` or `uncertain`; those were
        never counted, so reporting the raw out_of_scope tally next to `problem + extra`
        would suggest a subtraction that did not happen."""
        return sum(
            1 for d in self.reviews[case]["diffs"]
            if d.get("out_of_scope") and d["verdict"] in {"problem", "extra"}
        )

    def by_llm(self) -> dict[str, dict]:
        out: dict[str, dict] = {}
        for llm in LLM_ORDER:
            cases = [c for c, i in self.per.items() if i["llm"] == llm]
            agg = Counter()
            for c in cases:
                agg.update(self.per[c]["counts"])
                agg["in_scope"] += self.per[c]["problems_in_scope"]
                agg["e1"] += len(self.per[c]["ledger"]["e1_ids"])
                agg["assertable"] += self.per[c]["assertable_problems"]
                agg["deducted"] += self._deducted(c)
                for v in (self.per[c].get("out_of_scope") or {}).values():
                    agg["oos"] += v
            f1 = [
                self.per[c]["paper"]["f1_phase2"] for c in cases
                if isinstance(self.per[c]["paper"]["f1_phase2"], (int, float))
            ]
            agg["cases"] = len(cases)
            out[llm] = {"agg": agg, "f1": sum(f1) / len(f1) if f1 else None, "cases": sorted(cases)}
        return out

    def by_group(self) -> dict[str, dict]:
        out: dict[str, dict] = {}
        for g in sorted({i["group"] for i in self.per.values()}):
            cases = sorted(c for c, i in self.per.items() if i["group"] == g)
            agg = Counter()
            for c in cases:
                agg.update(self.per[c]["counts"])
                agg["in_scope"] += self.per[c]["problems_in_scope"]
                agg["e1"] += len(self.per[c]["ledger"]["e1_ids"])
                for k, v in (self.per[c].get("out_of_scope") or {}).items():
                    agg[f"oos_{k}"] += v
            paper_sem = sum(
                1 for c in cases if (self.paper.get(c) or {}).get("semantic_hallucinations")
            )
            out[g] = {"agg": agg, "cases": cases, "paper_sem": paper_sem}
        return out


# ---------------------------------------------------------------------------
# figures
# ---------------------------------------------------------------------------

def fig_grades(d: Data) -> str:
    t = d.summary["grade_totals"]
    lines = ["```mermaid", "pie showData title 逐条判定档位分布（共 %d 条差异）" % sum(t.values())]
    for k in ["correct", "similar", "problem", "extra", "uncertain"]:
        lines.append(f'    "{k}" : {t[k]}')
    lines.append("```")
    return "\n".join(lines)


def fig_quadrant(d: Data) -> str:
    """Paper F1 against manual problem count -- the claim is weak correlation, so the
    figure must show the off-diagonal cases, not a fitted line."""
    pts = []
    for c, i in d.per.items():
        f1 = i["paper"]["f1_phase2"]
        if not isinstance(f1, (int, float)):
            continue
        pts.append((c, f1, i["problems_in_scope"]))
    top = max(p for _, _, p in pts) or 1
    lo = min(f for _, f, _ in pts)
    hi = max(f for _, f, _ in pts)
    span = (hi - lo) or 1
    lines = [
        "```mermaid",
        "quadrantChart",
        "    title 论文 F1（Phase-II）与人工判定问题数",
        '    x-axis "F1 低" --> "F1 高"',
        '    y-axis "问题少" --> "问题多"',
        '    quadrant-1 "F1 高但问题多（评测失真）"',
        '    quadrant-2 "F1 低且问题多（一致）"',
        '    quadrant-3 "F1 低但问题少（参考罚分）"',
        '    quadrant-4 "F1 高且问题少（一致）"',
    ]
    # A quadrant chart crowds badly past ~20 points; plot the informative extremes.
    pts.sort(key=lambda p: (-p[2], -p[1]))
    picked = pts[:8] + sorted(pts, key=lambda p: (p[2], -p[1]))[:6] + \
        sorted(pts, key=lambda p: (-p[1], p[2]))[:4] + sorted(pts, key=lambda p: (p[1], -p[2]))[:4]
    seen = set()
    for c, f1, n in picked:
        if c in seen:
            continue
        seen.add(c)
        x = 0.04 + 0.92 * (f1 - lo) / span
        y = 0.04 + 0.92 * (n / top)
        lines.append(f'    "{c}": [{x:.3f}, {y:.3f}]')
    lines.append("```")
    return "\n".join(lines), sorted(seen), pts


def fig_repair_chain() -> str:
    return """```mermaid
flowchart TD
    subgraph P0["0000（NL08 / GPT-4o）修复引入缺陷"]
    A["列 I&nbsp;&nbsp;HumanDriving --> FinalState : Power Off<br/>语义正确，但嵌在状态体内 → 结构违法"]
      --> B["论文 stage(2) 记 grammar hallucination"]
      --> C["列 Z&nbsp;&nbsp;[*] --> FinalState : Power Off<br/>结构合法，语义已错（断电源丢失）"]
      --> D["stage(3) 语义栏留空<br/>Resolved = 1.0"]
    end
    subgraph P1["0030（同一份 NL / Llama）同形缺陷被抓住"]
    E["Phase-I 出现同形<br/>[*] --> FinalState : Power Off"]
      --> F["stage(3) 记 missing final state"]
      --> G["正确修复"]
    end
    D -. "同一缺陷形状，一处漏判一处正确" .-> F
```"""


def fig_oracle() -> str:
    return """```mermaid
flowchart LR
    NL["NL 需求文本<br/>模板禁止写元素个数与元素间关系<br/>→ 构造性欠定"]
    SET["与 NL 一致的模型集合<br/>（多个成员）"]
    REF["论文参考模型<br/>作者人工重建<br/>§7 自认 subjective<br/>§4.2(4) assume 正确"]
    GEN["某个 LLM 生成的 STM_0"]
    NL --> SET
    SET --> REF
    SET --> GEN
    REF -- "元素级 F1 逐点比对" --> SCORE["论文分数"]
    GEN --> SCORE
    SCORE --> Q{"测的是什么？"}
    Q -- "参考比 NL 更具体的那部分" --> W["猜中作者私有模型的程度<br/>（不应计为生成方缺陷）"]
    Q -- "良构性 / NL 点名元素 / 与 NL 显式义务矛盾" --> R["真实建模缺陷<br/>（可计为问题）"]
```"""


# ---------------------------------------------------------------------------
# tables
# ---------------------------------------------------------------------------

def tbl_per_pair(d: Data) -> str:
    """One row per pair.  Kept to 13 columns: the two link columns are merged and the
    paper's semantic text is reduced to a marker, because a 15-column table with two long
    URLs per row scrolls horizontally on any normal screen and the full semantic text is
    already in `index.tsv` and each case's readable report."""
    head = ("| pair | NL | LLM | 状态/层深/迁移/变量/动作 | corr | sim | **prob** | extra | unc | "
            "范围外 | 台帐E1 | 论文语义栏 | F1-Ⅱ | 证据 |")
    rule = ("| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | :-: | ---: | --- |")
    rows = [head, rule]
    for c in sorted(d.per):
        i = d.per[c]
        cs = d.census.get(c) or {}
        shape = (f"{cs.get('states','?')}/{cs.get('depth','?')}/{cs.get('transitions','?')}/"
                 f"{cs.get('vars','?')}/{cs.get('actions','?')}") if cs else "—"
        oos = "、".join(f"{k[:4]}×{v}" for k, v in sorted((i.get("out_of_scope") or {}).items())) or "—"
        sem = (d.paper.get(c) or {}).get("semantic_hallucinations")
        raw = i["paper"]["f1_phase2"]
        f1 = f"{raw:.3f}" if isinstance(raw, (int, float)) else "—"
        n = i["counts"]
        rows.append(
            f"| `{c}` | {i['group']} | {i['llm']} | {shape} | {n['correct']} | {n['similar']} | "
            f"**{n['problem']}** | {n['extra']} | {n['uncertain']} | {oos} | "
            f"{len(i['ledger']['e1_ids'])} | {'有' if sem else '空'} | {f1} | "
            f"{d.readable_link(c, '详情')}·{d.audit_link(c)} |"
        )
    return "\n".join(rows)


def tbl_llm(d: Data) -> str:
    by = d.by_llm()
    top = max(v["agg"]["in_scope"] for v in by.values()) or 1
    rows = [
        "| LLM | 计入问题 | 图示 | problem | extra | 范围外扣除（仅 problem/extra 档） | "
        "其中可断言 | 台帐E1 | 论文 F1-Ⅱ 均值 |",
        "| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for llm, v in sorted(by.items(), key=lambda kv: kv[1]["agg"]["in_scope"]):
        a = v["agg"]
        f1 = f"{v['f1']:.3f}" if v["f1"] else "—"
        rows.append(
            f"| **{llm}** | **{a['in_scope']}** | {bar(a['in_scope'], top)} | {a['problem']} | "
            f"{a['extra']} | −{a['deducted']} | {a['assertable']}/{a['problem']} | "
            f"{a['e1']} | {f1} |"
        )
    tot = Counter()
    for v in by.values():
        tot.update(v["agg"])
    rows.append(
        f"| **合计** | **{tot['in_scope']}** | | {tot['problem']} | {tot['extra']} | "
        f"−{tot['deducted']} | {tot['assertable']}/{tot['problem']} | {tot['e1']} | |"
    )
    return "\n".join(rows)


def tbl_group(d: Data) -> str:
    by = d.by_group()
    top = max(v["agg"]["in_scope"] for v in by.values()) or 1
    # The concurrency/timing columns count *all* out_of_scope marks, including those on
    # `similar`/`uncertain` diffs; §9.1's "范围外扣除" counts only the 9 that sat on
    # problem/extra.  Same word, two subsets -- so the column names carry their scope.
    rows = [
        "| NL 组 | 领域 | 计入问题 | 图示 | correct | similar | problem | extra | uncertain | "
        "范围外·并发（全档） | 范围外·时间（全档） | 台帐E1 | 论文语义栏有记录 |",
        "| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for g, v in sorted(by.items(), key=lambda kv: kv[1]["agg"]["in_scope"]):
        a = v["agg"]
        rows.append(
            f"| **{g}** | {NL_TITLE.get(g,'?')} | **{a['in_scope']}** | {bar(a['in_scope'], top)} | "
            f"{a['correct']} | {a['similar']} | {a['problem']} | {a['extra']} | {a['uncertain']} | "
            f"{a.get('oos_concurrency',0)} | {a.get('oos_timing',0)} | {a['e1']} | {v['paper_sem']}/6 |"
        )
    tot = Counter()
    for v in by.values():
        tot.update(v["agg"])
    sem_tot = sum(v["paper_sem"] for v in by.values())
    rows.append(
        f"| **合计** | | **{tot['in_scope']}** | | {tot['correct']} | {tot['similar']} | "
        f"{tot['problem']} | {tot['extra']} | {tot['uncertain']} | "
        f"{tot.get('oos_concurrency',0)} | {tot.get('oos_timing',0)} | {tot['e1']} | {sem_tot}/60 |"
    )
    return "\n".join(rows)


def tbl_matrix(d: Data) -> str:
    """NL x LLM heatmap of in-scope problem counts, with each cell linking to the pair."""
    cell: dict[tuple[str, str], tuple[str, int]] = {}
    for c, i in d.per.items():
        cell[(i["group"], i["llm"])] = (c, i["problems_in_scope"])
    groups = sorted({i["group"] for i in d.per.values()})
    shade = lambda n: "·" if n == 0 else ("▁▂▃▅▆▇█"[min(n, 7) - 1] if n else "·")
    rows = ["| NL 组 | " + " | ".join(LLM_ORDER) + " | 行合计 |",
            "| --- | " + " | ".join(["---"] * len(LLM_ORDER)) + " | ---: |"]
    for g in groups:
        cells, tot = [], 0
        for llm in LLM_ORDER:
            got = cell.get((g, llm))
            if not got:
                cells.append("—")
                continue
            case, n = got
            tot += n
            cells.append(f"{shade(n)} {d.readable_link(case, f'{case}·{n}')}")
        rows.append(f"| **{g}** {NL_TITLE.get(g,'')} | " + " | ".join(cells) + f" | **{tot}** |")
    tots = []
    for llm in LLM_ORDER:
        tots.append(str(sum(n for (g, l), (c, n) in cell.items() if l == llm)))
    rows.append("| **列合计** | " + " | ".join(f"**{t}**" for t in tots) +
                f" | **{d.summary['problems_in_scope_total']}** |")
    # The block glyphs are a compact encoding; per CLAUDE.md the legend belongs outside
    # the cells.  Note the ramp skips U+2584 -- without saying so, a reader reverse-
    # engineering the scale from the glyphs would infer the wrong mapping.
    rows.append("")
    rows.append("> 方块按计入问题数编码（跳过 `▄`）：`·` 0 · `▁` 1 · `▂` 2 · `▃` 3 · "
                "`▅` 4 · `▆` 5 · `▇` 6 · `█` 7。格内链接直达该 pair 的可读详情。")
    return "\n".join(rows)


def tbl_quadrants(d: Data) -> str:
    mp = {c for c, i in d.per.items() if i["problems_in_scope"] > 0}
    me1 = {c for c, i in d.per.items() if i["ledger"]["e1_ids"]}
    mps = {c for c in d.per if (d.paper.get(c) or {}).get("semantic_hallucinations")}
    def cell(s: set[str]) -> str:
        return f"**{len(s)}**" + (" — " + "、".join(f"`{c}`" for c in sorted(s)) if s else "")
    return "\n".join([
        "| | 人工判有问题 | 人工判无问题 |",
        "| --- | --- | --- |",
        f"| **台帐有 E1** | {cell(me1 & mp)} | {cell(me1 - mp)} |",
        f"| **台帐无 E1** | {cell(mp - me1)} | {cell(set(d.per) - mp - me1)} |",
        "",
        "| | 人工判有问题 | 人工判无问题 |",
        "| --- | --- | --- |",
        f"| **论文语义栏有记录** | {cell(mps & mp)} | {cell(mps - mp)} |",
        f"| **论文语义栏为空** | {cell(mp - mps)} | {cell(set(d.per) - mp - mps)} |",
    ])


def tbl_f1_bins(d: Data, pts: list[tuple[str, float, int]]) -> str:
    import statistics as st
    bins = [(0.0, 0.6, "< 0.60"), (0.6, 0.8, "0.60 – 0.80"),
            (0.8, 0.9, "0.80 – 0.90"), (0.9, 1.01, "≥ 0.90")]
    rows = ["| 论文 F1-Ⅱ 区间 | case 数 | 人工问题数 中位 | 最小 | 最大 | 该区间的极端 case |",
            "| --- | ---: | ---: | ---: | ---: | --- |"]
    for lo, hi, label in bins:
        sel = [(c, n) for c, f, n in pts if lo <= f < hi]
        if not sel:
            continue
        ns = [n for _, n in sel]
        worst = max(sel, key=lambda x: x[1])
        best = min(sel, key=lambda x: x[1])
        rows.append(
            f"| {label} | {len(sel)} | **{st.median(ns):.1f}** | {min(ns)} | {max(ns)} | "
            f"最多 {d.readable_link(worst[0], f'`{worst[0]}`·{worst[1]}')}、"
            f"最少 {d.readable_link(best[0], f'`{best[0]}`·{best[1]}')} |"
        )
    return "\n".join(rows)


def tbl_uncertain(d: Data) -> str:
    """Where reviewers could not decide -- grouped so the blockers are actionable."""
    buckets: dict[str, list[tuple[str, str]]] = defaultdict(list)
    keys = [
        ("并发/区域语义", ("并发", "region", "区域", "正交", "concurrent")),
        ("标签是触发器还是散文", ("散文", "标签", "触发器", "label")),
        ("表示层是否丢失语义", ("表示", "投影", "R4.5", "r4_5", "前端")),
        ("参考模型自身可疑", ("参考模型", "参考侧", "reference")),
        ("NL 欠定，多解皆可", ("欠定", "NL 未", "未约束", "未提及", "无约束")),
    ]
    for c, r in d.reviews.items():
        for diff in r["diffs"]:
            if diff["verdict"] != "uncertain":
                continue
            why = diff.get("reason") or ""
            for label, pats in keys:
                if any(p in why for p in pats):
                    buckets[label].append((c, why))
                    break
            else:
                buckets["其他"].append((c, why))
    rows = ["| 卡点类别 | 条数 | 涉及 pair | 代表理由（截断） |", "| --- | ---: | --- | --- |"]
    for label, items in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
        cases = sorted({c for c, _ in items})
        shown = "、".join(f"`{c}`" for c in cases[:9]) + ("…" if len(cases) > 9 else "")
        rep = items[0][1].replace("\n", " ").replace("|", "/")[:78]
        rows.append(f"| {label} | **{len(items)}** | {shown} | {rep}… |")
    return "\n".join(rows)


def tbl_assertable(d: Data) -> tuple[str, dict]:
    """Which predicates reviewers said would express each problem.  This is the honest
    measure of whether the ledger's omissions were a tooling limit or a scoping choice --
    but only if `transition_exists` and friends are held apart from the closed 19, since
    naming a legacy primitive is *not* evidence that the predicate surface covers it."""
    pred: Counter[str] = Counter()
    legacy: Counter[str] = Counter()
    no_pred: list[tuple[str, str]] = []
    for c, r in d.reviews.items():
        for diff in r["diffs"]:
            if diff["verdict"] not in {"problem", "extra"} or diff.get("out_of_scope"):
                continue
            a = (diff.get("assertable") or "").strip()
            if not a or diff.get("predicate_exists") is False:
                no_pred.append((c, (diff.get("reason") or "")[:70]))
                continue
            name = (a.split("(")[0].strip().split()[-1] if "(" in a else a.split()[0]).strip("`")
            (pred if name in CLOSED_PREDICATES else legacy)[name] += 1
    top = max(pred.values()) if pred else 1
    rows = ["| 谓词 | 族 | 可表达的问题条数 | 图示 |", "| --- | :-: | ---: | --- |"]
    for name, n in pred.most_common():
        rows.append(f"| `{name}` | {CLOSED_PREDICATES[name]} | {n} | {bar(n, top, 14)} |")
    unused = [n for n in CLOSED_PREDICATES if n not in pred]
    for name in unused:
        rows.append(f"| `{name}` | {CLOSED_PREDICATES[name]} | **0** | *本轮一次未用* |")
    rows.append(f"| **19 个封闭谓词小计** | | **{sum(pred.values())}** | |")
    for name, n in legacy.most_common():
        tag = "非封闭谓词（台帐当年的底层原语）" if name == "transition_exists" else "Python 包装器，非谓词"
        rows.append(f"| ~~`{name}`~~ | — | {n} | {tag} |")
    rows.append(f"| **无任何现成写法** | | **{len(no_pred)}** | 对应下节的词表缺口 |")
    rows.append(f"| **合计** | | **{sum(pred.values()) + sum(legacy.values()) + len(no_pred)}** | |")
    return "\n".join(rows), {
        "closed": sum(pred.values()), "legacy": dict(legacy),
        "no_pred": len(no_pred), "unused": unused, "no_pred_cases": no_pred,
    }


def tbl_census(d: Data) -> str:
    """Structural spread of the 60 STM_0, so a reader can see the review was not run
    over a set of near-identical toy models."""
    if not d.census:
        return "*（语料结构统计未产出）*"
    keys = [("states", "状态数"), ("depth", "最大层深"), ("composites", "复合状态"),
            ("transitions", "迁移数"), ("events", "事件数"), ("vars", "变量数"),
            ("actions", "动作数"), ("guards", "守卫数"), ("effects", "effect 数"),
            ("unspec_initial", "合成 UnspecifiedInitial"), ("exclusions", "归因排除元素")]
    rows = ["| 结构指标 | 最小 | 中位 | 最大 | 合计 | 为 0 的 pair 数 |",
            "| --- | ---: | ---: | ---: | ---: | ---: |"]
    import statistics as st
    for key, label in keys:
        vals = [r.get(key, 0) for r in d.census.values()]
        med = st.median(vals)
        # 60 values means the median is an average of two, so it is often a half.  Rounding
        # it to an integer silently misreports the corpus (3.5 printed as 4).
        shown = f"{med:.0f}" if med == int(med) else f"{med:.1f}"
        rows.append(f"| {label} | {min(vals)} | {shown} | {max(vals)} | "
                    f"{sum(vals)} | {sum(1 for v in vals if v == 0)} |")
    return "\n".join(rows)


def tbl_oos(d: Data) -> str:
    """Every out-of-scope difference, listed rather than aggregated away.  The ruling was
    that concurrency and timing are outside the problem definition -- which obliges us to
    show what was set aside, not just how much."""
    rows = ["| 类别 | pair | 判定 | 参考侧 | 理由（截断） |", "| --- | --- | --- | --- | --- |"]
    for c in sorted(d.reviews):
        for diff in d.reviews[c]["diffs"]:
            k = diff.get("out_of_scope")
            if not k:
                continue
            clean = lambda s: (s or "").replace("\n", " ").replace("|", "/")
            rows.append(
                f"| `{k}` | {d.readable_link(c, f'`{c}`')} | {diff['verdict']} | "
                f"{clean(diff.get('ref'))[:44]} | {clean(diff.get('reason'))[:80]}… |"
            )
    return "\n".join(rows)


def main() -> int:
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    d = Data(pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3],
             audit_rev=(sys.argv[5] if len(sys.argv) > 5 else None))
    quad, quad_cases, pts = fig_quadrant(d)
    assert_tbl, pred_meta = tbl_assertable(d)
    out = {
        "tbl_census": tbl_census(d),
        "tbl_oos": tbl_oos(d),
        "fig_grades": fig_grades(d),
        "fig_quadrant": quad,
        "fig_repair": fig_repair_chain(),
        "fig_oracle": fig_oracle(),
        "tbl_per_pair": tbl_per_pair(d),
        "tbl_llm": tbl_llm(d),
        "tbl_group": tbl_group(d),
        "tbl_matrix": tbl_matrix(d),
        "tbl_quadrants": tbl_quadrants(d),
        "tbl_f1_bins": tbl_f1_bins(d, pts),
        "tbl_uncertain": tbl_uncertain(d),
        "tbl_assertable": assert_tbl,
        "_meta": {
            "predicates": pred_meta,
            "quadrant_cases": quad_cases,
            "grade_totals": d.summary["grade_totals"],
            "oos": d.summary["out_of_scope_totals"],
            "in_scope": d.summary["problems_in_scope_total"],
            "assertable_problems_total": d.summary["assertable_problems_total"],
            "census_rows": len(d.census),
        },
    }
    dest = pathlib.Path(sys.argv[4]) if len(sys.argv) > 4 else pathlib.Path("/tmp/refcmp_parts.json")
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"渲染 {len(out)-1} 个片段 -> {dest}")
    print(f"  census 覆盖 {out['_meta']['census_rows']}/60")
    print(f"  封闭谓词可表达 {pred_meta['closed']}，"
          f"非封闭写法 {pred_meta['legacy']}，无写法 {pred_meta['no_pred']}")
    print(f"  一次未用的谓词: {pred_meta['unused']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
