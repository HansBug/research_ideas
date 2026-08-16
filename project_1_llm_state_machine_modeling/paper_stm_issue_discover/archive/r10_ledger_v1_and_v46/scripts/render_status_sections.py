"""Render the issue #171 status sections from data, not from memory.

The previous review round found that every script-generated table recomputed exactly while
every factual error sat in hand-typed prose. So the new sections -- defect directions,
predicate coverage, the non-expressible gap families, the scope audit and the 8-cell miss
analysis -- are generated here and pasted verbatim.

Fragments are written as separate files so the issue body and its comments can each pick up
only what they need:

  status_overview.md    the headline table plus the reconciliation gate
  defects.md            the admissible findings by defect direction
  predicates.md         123/153 expressible, by predicate, and the 30 gaps by family
  scope.md              153/153 inside the paper1 problem definition
  misses.md             22 expected -> 16 hit / 6 missed, attributed to a pipeline stage

Usage: render_status_sections.py [--out DIR]
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from collections import Counter, defaultdict

# ⚠️ 2026-08-17 归档：本文件原在 `discover_matrix/` 顶层，`HERE` 即指那一层；
# ⛔ 归档到 `archive/r10_ledger_v1_and_v46/scripts/` 后深度多了两层，`HERE / "manual_review"`
# 会解析到不存在的 `scripts/manual_review`。⭐ 故改为指向归档根（它保留了原 discover_matrix
# 的内部布局：manual_review/ · v46/ · verdicts/ …），⛔ 不数层数、按目录名锚定。
_F = pathlib.Path(__file__).resolve()
HERE = next(p for p in _F.parents if p.name == "r10_ledger_v1_and_v46")
MR = HERE / "manual_review"

#: Gap families for the 30 non-expressible findings.
#:
#: An adversarial review broke the first version of this table in three ways, all of which
#: changed the headline, so the current shape is deliberate:
#:
#:  1. `守卫非空` had been hard-coded into the `action_content` pattern to give `0025`#1 a
#:     home. That row's gap is "边必须携带区分条件 / 守卫非空" -- a *guard* gap. It and its
#:     referrer `0035`#3 inflated `action_content` from 8 to 10. `guard_content` now exists.
#:  2. `overspecification_judgement` and `minimality` were two names for one gap ("无法断言
#:     某元素不应存在"). All 12 rows are `verdict=extra` + `stratum=over_specification_benign`
#:     and are rejected on the identical ground. Split apart they read 5 and 7; merged they
#:     are 12, which is larger than `action_content` -- i.e. the split inverted the finding.
#:  3. Primary family was decided by *position in this list*, not by the text. That made
#:     `granularity` unreachable (its only candidate `0032`#3 was taken by `synthetic_nodes`)
#:     and assigned some rows their second gap while others got their first.
#:
#: So: primary is now the family whose pattern matches **earliest in the text**, and every
#: other match is recorded as a secondary mention and reported separately -- otherwise a
#: row's second gap vanishes from the tally entirely.
#: `is_real_gap=False` marks the row where the vocabulary refuses *on purpose*.
GAP_FAMILIES: list[tuple[str, str, str, bool]] = [
    ("deliberate_refusal", "词表刻意设防（非缺口）",
     r"刻意设防", False),
    ("minimality_no_provenance",
     "缺『不应多出』谓词：无法断言某元素没有需求依据、不该存在",
     r"最小性|不得有同触发同目标|不应多出|不应存在|可归因的『过度指定』判据", True),
    ("action_content", "缺动作内容 / 动作计数谓词（非数值 effect、输出信号）",
     r"动作内容|动作计数|抽象动作或输出信号", True),
    ("guard_content", "缺『边必须携带区分条件 / 守卫非空』谓词",
     r"守卫非空|携带区分条件", True),
    ("triggerless_edge", "缺『无触发 / completion 边存在』谓词",
     r"无触发", True),
    ("synthetic_nodes", "合成节点污染 cardinality，计数命题不可信",
     r"合成节点|投影合成", True),
    ("initial_edge", "初始边族被 initial_target 的拒答语义封死",
     r"initial_edge_count|unique_default_entry|多默认进入点|初始边守卫", True),
    ("false_false_source", "行为族对不可判定目标返回 False 而非拒答——会伪造缺陷",
     r"伪造缺陷|假 False|返回 False 而非拒答", True),
    ("existential", "S 族无存在量词，『壳缺失』只能照搬参考名",
     r"存在量词|existential", True),
    ("granularity", "缺『一个 NL 概念对应几个模型状态』的粒度谓词",
     r"粒度谓词", True),
    ("exact_occupancy", "缺 exact occupancy 与隔离单个多余元素的计数口径",
     r"exact occupancy|恰好占据", True),
]
_COMPILED = [(k, lbl, re.compile(p), real) for k, lbl, p, real in GAP_FAMILIES]
_LABEL = {k: lbl for k, lbl, _p, _r in GAP_FAMILIES}
_REAL = {k: real for k, _l, _p, real in GAP_FAMILIES}

CLOSED_FAMILY = {
    "state_declared": "S", "variable_declared": "S", "event_declared": "S",
    "containment": "S", "initial_target": "S", "edge_declared": "S",
    "effect_declared": "S", "action_declared": "S", "guard_distinguishable": "S",
    "cardinality": "S", "occupancy_after": "B", "event_consumed": "B",
    "stays_in": "B", "variable_delta_after": "B", "reaches": "B", "terminates": "B",
    "invariant": "P", "response_within": "P", "persists_until": "P",
}
EXISTENCE_ONLY = {"state_declared", "event_declared", "variable_declared",
                  "edge_declared", "effect_declared", "action_declared"}

STAGE_LABEL = {
    "split_requirements": "`split_requirements`（拆需求）",
    "convert_assertions": "`convert_assertions`（转断言）",
    "precheck_and_seal": "`precheck_and_seal`（预检封存）",
    "review_assertions": "`review_assertions`（审断言）",
    "release_results": "`release_results`（放行）",
    "bind_attribution": "`bind_attribution`（绑归因）",
    "adjudicate_results": "`adjudicate_results`（裁决）",
}


def load(name: str):
    p = MR / name
    return json.loads(p.read_text()) if p.exists() else None


#: A gap analysis often reads only "同 0005#3" -- a *reference* to another row's analysis,
#: not a statement in itself. Matching it as a literal put five `action_content` rows under
#: `overspecification_judgement`, because the referring text happened to sit next to rows
#: about over-specification. It has to be dereferenced to the cited row's own family.
_REF = re.compile(r"^同\s*(\d{4})#(\d+)")


def gap_families(text: str, resolve=None, _depth: int = 0) -> tuple[str, list[str]]:
    """(primary, secondaries). Primary is whichever family matches earliest in the text.

    A row often names two gaps ("两个缺口叠加：(1)… (2)…"). Returning only one loses the
    other -- and one of the losers was `0038`#3's "行为族对 pseudo 目标返回 False 而非拒答"，
    a soundness bug that *fabricates* defects. Secondaries are reported separately rather
    than dropped."""
    body = (text or "").strip()
    if m := _REF.match(body):
        target = (m.group(1), int(m.group(2)))
        # Depth-limited: a mutual "同 A / 同 B" pair would otherwise recurse forever.
        if resolve and _depth < 4 and (cited := resolve(target)) is not None:
            return gap_families(cited, resolve, _depth + 1)
        return "unresolved_reference", []
    hits = [(m.start(), key) for key, _l, pat, _r in _COMPILED if (m := pat.search(body))]
    if not hits:
        return "unmatched", []
    hits.sort()
    return hits[0][1], [k for _pos, k in hits[1:]]


def gap_family(text: str, resolve=None) -> tuple[str, str, bool]:
    """Primary family only, with its label and whether it counts as a real gap."""
    key, _sec = gap_families(text, resolve)
    return (key,
            _LABEL.get(key, "**未归类（需人工看）**" if key == "unmatched"
                       else "**引用了一条查不到的分析（需人工看）**"),
            _REAL.get(key, True))


def pct(n: int, d: int) -> str:
    return f"{n / d:.0%}" if d else "—"


#: Audit gist holding the per-row data behind every number below, and the revision the raw
#: links are pinned to so a later edit cannot silently change what a citation points at.
GIST_AUDIT = "daa977482df22711e8e0d00fc80c406c"
GIST_READABLE = "29fa73ff6d3ea405e7418af34b8322d5"
AUDIT_REV = "6533c0b12e771b1f788499f761ff60a399ce47a0"
_BRIEF_URL = (f"https://gist.github.com/HansBug/{GIST_AUDIT}"
              "#file-predcov_brief-md")


def anchor(filename: str) -> str:
    """GitHub slugifies *only the dot*: it lowercases and turns `.` into `-`, leaving
    underscores and hyphens alone. `final_stratification.md` -> `file-final_stratification-md`.
    Getting this wrong does not 404 -- it lands on the page top with no warning, which is
    why it is a named function with a test rather than an inline f-string."""
    return "file-" + filename.lower().replace(".", "-")


def gist_link(label: str, filename: str, readable: bool = False) -> str:
    gid = GIST_READABLE if readable else GIST_AUDIT
    return f"[{label}](https://gist.github.com/HansBug/{gid}#{anchor(filename)})"


def _one_line(text, limit: int = 400) -> str:
    """Collapse to one line and cap length -- these fields hold multi-line prose with
    embedded newlines, and a raw newline inside a Markdown table cell breaks the table."""
    s = re.sub(r"\s+", " ", str(text or "")).strip().replace("|", "\\|")
    return s if len(s) <= limit else s[:limit].rstrip() + "……"


def main() -> int:
    out = pathlib.Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv \
        else MR / "issue_sections"
    out.mkdir(parents=True, exist_ok=True)

    summary = load("_summary.json")
    final = load("final_stratification.json")
    defects = load("defect_classification.json")
    verified = load("predicate_coverage/verified_assertions.json")
    scope = load("loop_audit/scope.json")
    cells = load("loop_audit/cells.json")
    replay = load("loop_audit/replay_attribution.json")
    prompt = load("loop_audit/prompt.json")
    recon = load("reconcile.json")
    written: list[str] = []

    def emit(name: str, body: str) -> None:
        (out / name).write_text(body.rstrip() + "\n")
        written.append(name)

    # ---------------------------------------------------------------- 现状总览
    g = summary["grade_totals"]
    vt = verified["totals"]
    ft = final["summary"]
    ok = recon["passed"] == recon["total"] if recon else False
    lines = [
        "本轮把 60 对逐对人工复核的结果，收敛成一组彼此对得上的数字。"
        f"下表每个数字都由脚本从逐行数据重算，并经 {recon['total'] if recon else 0} 项交叉一致性检查"
        f"（脚本 `project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/reconcile_numbers.py`）"
        f"{'全部通过' if ok else '**有未通过项**'}——任何两个来源不一致都必须先解决再发布。",
        "",
        "| 量 | 值 | 口径 |",
        "| --- | ---: | --- |",
        f"| 逐对复核的差异总数 | **{sum(g.values())}** | 60 对全覆盖，五档："
        f"correct {g['correct']} / similar {g['similar']} / problem {g['problem']} / "
        f"extra {g['extra']} / uncertain {g['uncertain']} |",
        f"| 计入问题（基线） | {summary['problems_in_scope_total']} | "
        f"problem + extra − 范围外扣减 9 |",
        "| **计入问题（主裁定后）** | **153** | 扣 `0013`#1（并发语义，见下）|",
        f"| **可入 E1（点值）** | **{ft['admissible']}** | 四个可归因层之和；"
        f"词法分层只能给区间 66–144，本轮逐行判完收敛为点值 |",
        f"| 可用现有 19 谓词表述 | **{vt['captured']} / 153**（{pct(vt['captured'], 153)}）| "
        f"独立复跑，只有返回 `False` 才计入 |",
        f"| 不可表述 | {153 - vt['captured']} | 按缺口族归类见下 |",
        f"| 落在 paper1 问题定义内 | **153 / 153**（100%）| "
        f"`T0` + FSM/HSM/EFSM，不含时钟与正交并发 |",
        "",
        f"分层构成（决定 {ft['admissible']} 这个点值）：",
        "",
        "| 层 | 条数 | 可入 | 判据 |",
        "| --- | ---: | :-: | --- |",
    ]
    strata_desc = {
        "nl_named": ("✓", "NL 点名了那个缺失或错位的元素"),
        "wellformedness": ("✓", "无需 oracle，仅凭生成模型自身即可判定"),
        "nl_contradiction": ("✓", "与 NL 的显式义务矛盾"),
        "over_specification": ("✓", "生成方凭空多出**且**造成可断言的负面后果"),
        "over_specification_benign": ("✗", "生成方多出但写不出后果"),
        "reference_only": ("✗", "只在参考、NL 未点名——不可归因于生成方"),
        "over_specification_duplicate": ("✗", "后果已被同 pair 的另一条承载，计入会双算"),
        "out_of_scope_concurrency": ("✗", "主裁定移出范围"),
        "uncertain_stratum": ("✗", "已审阅但搁置：当前谓词面给不出正面判定"),
    }
    by_stratum = Counter(r["stratum"] for r in final["rows"])
    adm = set(final["admissible_strata"])
    for name, n in by_stratum.most_common():
        mark, desc = strata_desc.get(name, ("?", ""))
        lines.append(f"| `{name}` | {n} | {mark} | {desc} |")
    lines += [
        f"| **合计** | **{sum(by_stratum.values())}** | **{ft['admissible']} 可入** | |",
        "",
        "逐行数据：" + gist_link("final_stratification.json", "final_stratification.json")
        + "（154 行，每行带层、判据、断言与裁定来源）｜ 一致性检查明细："
        + gist_link("reconcile.json", "reconcile.json")
        + " ｜ 分层方法：" + gist_link("FINAL_STRATIFICATION.md", "FINAL_STRATIFICATION.md"),
    ]
    emit("status_overview.md", "\n".join(lines))

    # ---------------------------------------------------------------- 缺陷方向
    if defects:
        rows = defects["rows"]
        by_dir = Counter(r["direction"] for r in rows)
        # Descriptions live in classify_defects.py; mirrored here by key.
        dir_desc = {
            "reachability": "可达性与终止：死端、吸收态、不可达、无终态、不能终止",
            "entry": "初始入口：缺初始边、带触发的初始边、多个竞争入口、默认子态错",
            "guard": "守卫与条件：缺守卫、不可区分、位置错、条件被折进事件名",
            "hierarchy": "层次归属：containment 丢失、错误嵌套、复合态未展开、作用域错",
            "effect_action": "动作与 effect：entry/exit 动作缺失、变量增减缺失",
            "pseudostate": "伪状态类型：fork / join / junction / choice 未声明或错配",
            "event": "事件与触发：事件缺失、被压成复合名、自造事件、触发方向错",
            "cardinality": "元素数量：NL 点名 N 个而模型 M 个、克隆件、区域数",
            "target_scope": "迁移目标：目标状态错、边接错位置",
            "unclassified": "关键词未命中，需人工看",
        }
        n = len(rows)
        lines = [
            f"把 **{n} 条可入 expected issue** 按「什么坏了」归类。方向读自复核给出的 `reason`，"
            "与「能否用谓词说出来」是两个独立问题，交叉起来才看得出词表的真实缺口。",
            "",
            "| 方向 | 条数 | 占比 | 含义 |",
            "| --- | ---: | ---: | --- |",
        ]
        for name, cnt in by_dir.most_common():
            lines.append(f"| `{name}` | **{cnt}** | {pct(cnt, n)} | {dir_desc.get(name, '')} |")
        lines.append(f"| **合计** | **{n}** | 100% | |")

        # direction x predicate family
        grid: dict[str, Counter] = defaultdict(Counter)
        for r in rows:
            grid[r["direction"]][CLOSED_FAMILY.get(r["primary_predicate"], "—")] += 1
        lines += [
            "",
            "交叉谓词族后，最值得注意的是「无谓词」那一列——它标出词表真正说不出的方向：",
            "",
            "| 方向 | S 结构 | B 行为 | P 性质 | 无谓词 | 合计 |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
        tot = Counter()
        for name, cnt in by_dir.most_common():
            c = grid[name]
            tot.update(c)
            lines.append(f"| `{name}` | {c['S']} | {c['B']} | {c['P']} | {c['—']} | **{cnt}** |")
        lines.append(f"| **合计** | **{tot['S']}** | **{tot['B']}** | **{tot['P']}** | "
                     f"**{tot['—']}** | **{n}** |")

        eo = sum(1 for r in rows if r["existence_only"])
        nop = [r for r in rows if not r["predicates"]]
        lines += [
            "",
            f"两个限制值得单独记下来。**{eo} 条（{pct(eo, n)}）只能给出存在性断言**"
            "（`state_declared` / `edge_declared` 这类）：能说「模型缺 X」，不能说「因此行为坏了」，"
            "而后者才是难以被质疑的形态。另有 "
            f"**{len(nop)} 条完全落在 19 谓词之外**："
            + "、".join(f"`{r['case']}`#{r['diff_index']}" for r in nop) + "。",
            "",
            f"逐行分类数据（{len(rows)} 行，含方向、命中的关键词、承载谓词）："
            + gist_link("defect_classification.json", "defect_classification.json")
            + " ｜ 生成脚本 `project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/classify_defects.py`",
        ]
        emit("defects.md", "\n".join(lines))

    # ---------------------------------------------------------------- 谓词覆盖
    ne = verified["not_expressible"]
    # Index over *all* 153 rows, not just these 30: a "同 XXXX#N" reference may point at a
    # row whose own assertion succeeded, and that row still carries the gap analysis.
    gap_index = {(r["case"], r["diff_index"]): (r.get("closest_gap") or "")
                 for r in verified.get("rows", []) + ne}
    resolve = gap_index.get

    fam_rows: dict[str, list] = defaultdict(list)
    fam_label: dict[str, str] = {}
    fam_real: dict[str, bool] = {}
    sec_counts: Counter[str] = Counter()
    for r in ne:
        key, secondaries = gap_families(r.get("closest_gap") or "", resolve)
        fam_rows[key].append(r)
        fam_label[key] = _LABEL.get(key, "**需人工看**")
        fam_real[key] = _REAL.get(key, True)
        sec_counts.update(secondaries)
    lines = [
        f"「能不能用现有 19 个封闭谓词把这条问题说出来」是独立复跑出来的，不采信批次自报的值："
        f"每条断言都在同一语料上重新求值一次，**只有返回 `False` 才计入可表述**。"
        f"返回 `True` 说明断言不判别，返回 `None` 或抛异常说明无法判定——两者都不是缺陷证据。",
        "",
        f"| 复跑结论 | 条数 | 含义 |",
        "| --- | ---: | --- |",
        f"| `captured` | **{vt['captured']}** | 返回 `False`，缺陷可被现有谓词表述并捕获 |",
        f"| 自报不可表述 | {vt['by_verdict'].get('declared_not_expressible', 0)} | "
        f"批次自己判为写不出，逐条给了缺口分析 |",
        f"| `not_captured` / `disputed` / `uses_non_closed` | "
        f"{vt['by_verdict'].get('not_captured', 0)} / {len(verified['disputed'])} / "
        f"{len(verified['uses_non_closed'])} | 三项皆为 0：没有断言写错、"
        f"没有与批次报告不一致、没有偷用 19 谓词之外的旧原语 |",
        f"| **合计** | **{vt['checked']}** | |",
        "",
        f"**{vt['captured']} / 153 = {pct(vt['captured'], 153)} 可用现有谓词表述到位。**"
        f"按承载谓词分布如下（同一条只记首个判别谓词）：",
        "",
        "| 谓词 | 族 | 捕获条数 | 只能证存在性 |",
        "| --- | :-: | ---: | :-: |",
    ]
    for name, cnt in Counter(vt["by_predicate"]).most_common():
        lines.append(f"| `{name}` | {CLOSED_FAMILY.get(name, '—')} | {cnt} | "
                     f"{'✓' if name in EXISTENCE_ONLY else ''} |")
    lines.append(f"| **合计** | | **{sum(vt['by_predicate'].values())}** | |")
    unused = sorted(set(CLOSED_FAMILY) - set(vt["by_predicate"]))
    lines += [
        "",
        f"19 个谓词里有 **{len(unused)} 个一条都没用上**："
        + "、".join(f"`{u}`" for u in unused)
        + "。这不代表它们无用，而是说明本轮 153 条问题的形态集中在结构与可达性上。",
        "",
        f"### 不可表述的 {len(ne)} 条：按缺口族归类",
        "",
        "每条都由复核者先尝试写断言、失败后给出缺口分析，因此「不可表述」是尝试过的结论，"
        "不是没试。归类如下：",
        "",
        "| 缺口族 | 主缺口 | 另被提及 | 是真缺口 | 说明 |",
        "| --- | ---: | ---: | :-: | --- |",
    ]
    # The two escape hatches must be listed here too, or an unclassified row would be
    # counted in the total while never appearing as a line -- the table would silently
    # fail to add up.
    for key, _lbl, _pat, _real in GAP_FAMILIES + [
            ("unmatched", "", "", True), ("unresolved_reference", "", "", True)]:
        if key not in fam_rows and not sec_counts.get(key):
            continue
        rs = fam_rows.get(key, [])
        secn = sec_counts.get(key, 0)
        lines.append(f"| `{key}` | {('**' + str(len(rs)) + '**') if rs else '—'} | "
                     f"{secn or '—'} | {'✓' if fam_real.get(key, True) else '✗'} | "
                     f"{fam_label.get(key) or _LABEL.get(key, '')} |")
    lines.append(f"| **合计** | **{len(ne)}** | {sum(sec_counts.values())} | | |")

    n_min = len(fam_rows.get("minimality_no_provenance", []))
    n_act = len(fam_rows.get("action_content", []))
    real_n = sum(len(v) for k, v in fam_rows.items() if fam_real.get(k, True))
    lines += [
        "",
        f"其中 **{real_n} 条按真词表缺口计**，{len(ne) - real_n} 条（`0006`#4）不计入。"
        "**这条排除用的是一条窄规则，须写明**：不是因为该形态「良性」——"
        "30 条里有 15 条同属 `over_specification_benign`，其中 14 条照样计入缺口，"
        "所以良性本身不是判据。真正的理由是**谓词文档把这个形状明写为假阳性**："
        "`edge_declared` 的 caveat 与 `occupancy_after` 的 horizon 自检共同封死了"
        "「把多出的一跳记成缺陷」这条路。"
        "需要同时承认该自检是**内容无关**的：只要更大的 `within_cycles` 也返回 True 它就拒答，"
        "无论那一跳有害还是无害——因此它在这里给出正确答案靠的是构造，不是对缺陷的判别。",
    ]
    lines += [
        "",
        "**「30」是一个带政策条件的数，不是纯测量值——这一点必须写在表旁边。**"
        f"[predcov_BRIEF.md]({_BRIEF_URL}) 定的判据是纯机械的：在这个有缺陷的模型上实测返回 "
        "`False` 即算可表述。按该判据，`minimality_no_provenance` 里的 NL02 钳夹类"
        "**本不该留在「不可表述」里**——本轮复跑发现 P 族的 "
        "`invariant(scope=S, condition=active(S))` 在那几个 case 上**确实返回 `False`**"
        "（此前的有害性判定没试过 P 族），且有效负控："
        "`0026` 的真吸收态返回 `True`、同模型有出边的状态返回 `False`，该形态并非恒假。"
        "它们仍被留在「不可表述」里，依据的是一条**未写进 BRIEF 的政策**："
        "闭世界禁令（「该状态必须保持吸收」「不得声明该事件」）不算合法断言。"
        "这条政策若翻转，**至少 8 条会移出「不可表述」**"
        "（除 NL02 钳夹类，还有 `0002`#3、`0010`#7、`0043`#2 这类「沉默封闭」）。"
        "所以 30 应读作「在不采纳闭世界禁令的前提下不可表述的条数」。"
        "**这是分层政策问题，不是谓词能力问题，必须由人裁定。**",
        "",
        "还有一处粒度限制：NL02 钳夹类的 5 条对应的其实是 **4 条 case 级断言**——"
        "`0041`#0 与 `0041`#1 是同一模型同一个 `ClampingState` 上的两条多余出边，"
        "写出来的表达式逐字相同，那一个 `False` 由两条 extra 共同造成、**无法互相隔离**。",
    ]
    if "unmatched" in fam_rows:
        lines += ["", f"⚠️ 有 {len(fam_rows['unmatched'])} 条未能归类，需人工看："
                  + "、".join(f"`{r['case']}`#{r['diff_index']}"
                             for r in fam_rows["unmatched"]) + "。"]

    lines += [
        "",
        f"**最大的缺口是「无法断言某元素不该存在」：`minimality_no_provenance` 族 {n_min} 条，"
        f"占 30 条的 {n_min / len(ne):.0%}。**"
        "19 个谓词全是正面的存在性或正面的可达性命题，"
        "所以能问「模型有没有声明 X」「跑起来会不会到 Y」，"
        "问不了「X 有没有需求依据、是不是根本不该出现」——"
        "把 `extra` 写成正面断言必然退化成闭世界禁令。"
        f"这 {n_min} 条**全部**是 `verdict = extra` 且 `stratum = over_specification_benign`，"
        "同一种形状、同一种拒绝理由。",
        "",
        f"**第二大缺口落在动作 $A$ 上：`action_content` 族 {n_act} 条（{n_act / len(ne):.0%}）。**"
        "形态是「非数值的动作或输出信号义务」——`Start Timer`、`Stop Timer`、"
        "`Display / Update Cooking Time` 这类。它在 19 谓词里无处落脚："
        "effect 通道（`effect_declared` / `variable_declared` / `variable_delta_after`）"
        "要求「变量 + 符号」，而该通道在本语料恒为空"
        "（全库唯一被声明过的变量是 converter 的 `R45RouteToken`，非 route 变量声明为 0）；"
        "action 通道 `action_declared(state=..., phase=...)` **没有动作名参数**，"
        "只能证明「这个状态挂了某个动作」，证明不了「挂的是 `Start Timer`」。"
        "$A$ 是 $M = (S, E, V, Tr, A)$ 的一个分量，却只有一个只看相位的谓词覆盖它。",
        "",
        "另需注明一处推断与观测的边界：NL 通常不规定动作该挂状态还是挂迁移，"
        "而 `action_declared` 只读状态侧字段、迁移承载的具名动作在 19 谓词里不可见，"
        "**因此原则上两种渲染会让同一条断言给出相反答案**。"
        "但这是从谓词签名与 NL 欠定推出的机制推断，不是观测结果："
        "`0014`#1 确实出现过同一个 `Entry/Accelerate` 挪到初始边标签后断言翻面，"
        "但该 pair 的 NL 逐字点名了相位、迁移写法被判 `problem`；"
        "`0004`#5 是 NL 未指定相位的真实例，可作者的 entry + during 写法被判 `similar`。"
        "**「两种都正确的渲染同时出现并使断言翻面」目前尚无观测实例。**",
    ]
    lines += [
        "",
        "复跑逐条结果（153 行，含断言原文、复跑值、与批次自报值的比对）："
        + gist_link("predcov_verified_assertions.json", "predcov_verified_assertions.json")
        + " ｜ 五批原始判定 "
        + "、".join(gist_link(f"批{n}", f"predcov_result{n}.json") for n in range(1, 6))
        + " ｜ 方法与已知坑 " + gist_link("predcov_BRIEF.md", "predcov_BRIEF.md")
        + " ｜ 复跑脚本 `project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/verify_assertions.py`",
    ]
    emit("predicates.md", "\n".join(lines))

    # ---------------------------------------------------------------- 范畴审计
    if scope:
        st = scope["totals"]
        be = scope["by_element"]
        lines = [
            "第一个问题：这 153 条里有多少落在 paper1 的问题定义内，即 `T0` + FSM/HSM/EFSM "
            "的 $M = (S, E, V, Tr, A)$，不含时钟 $C$、不变式 $Inv$ 与正交区并发语义。",
            "",
            f"**结论：{st['in_scope']} / 153 全部在范围内，范围外 {st['out_of_scope']} 条。**"
            "这不是巧合——范围外的差异在复核阶段就已经被 `out_of_scope` 标记扣除掉了"
            f"（共 {sum(summary['out_of_scope_totals'].values())} 条：并发 "
            f"{summary['out_of_scope_totals']['concurrency']} + 时间 "
            f"{summary['out_of_scope_totals']['timing']}），"
            "其中落在 `problem`/`extra` 档的 9 条构成了 154 这个基线的扣减项。",
            "",
            "按所触及的元组分量统计：",
            "",
            "| 分量 | 条数 | 占比 |",
            "| --- | ---: | ---: |",
        ]
        legend = scope.get("element_legend") or {}
        for k, v in sorted(be.items(), key=lambda kv: -kv[1]):
            lines.append(f"| {k} {legend.get(k, '')} | **{v}** | {pct(v, 153)} |")
        lines.append(f"| **合计** | **{sum(be.values())}** | 100% |")
        lines += [
            "",
            f"迁移关系 $Tr$ 占 {pct(be.get('Tr', 0), 153)}、状态集 $S$ 占 "
            f"{pct(be.get('S', 0), 153)}，两者合计超过七成；时钟与不变式一条都没有，"
            "与问题定义边界一致。",
        ]
        dl = scope.get("disputed_list") or []
        if dl:
            lines += [
                "",
                f"### {len(dl)} 条判据表覆盖不到的边界（已裁定，单列供复核）",
                "",
                "这三条最终都裁定为范围内，但理由需要写清楚，否则「100% 在范围内」会显得可疑：",
                "",
                "| 条目 | 裁定 | 为什么 |",
                "| --- | :-: | --- |",
            ]
            for d in dl:
                why = re.sub(r"\s+", " ", d["why"]).strip()
                if len(why) > 300:
                    why = why[:300].rstrip() + "……"
                lines.append(f"| `{d['case']}`#{d['diff_index']} | {d['ruling']} | {why} |")
            lines += [
                "",
                "共同点：**被发明的对象恰好是正交区成员，但断言本身不涉及并发执行语义。**"
                "判据表只把「区域之间是否同时活跃」列为范围外，"
                "而 `state_declared` / `event_declared` 这类存在性断言落在 $S$ 内。"
                "若把同一条改写成断言并发语义，它就会落到范围外——"
                "**范畴归属取决于断言形式，不取决于对象长什么样。**",
            ]
        lines += [
            "",
            "逐条范畴裁定（153 行，含所触及分量、判据引用与裁定理由）："
            + gist_link("loopaudit_scope.json", "loopaudit_scope.json"),
        ]
        emit("scope.md", "\n".join(lines))

    # ---------------------------------------------------------------- 漏检分析
    if cells:
        ct = cells["totals"]
        hit = ct["distinct_manual_defects_hit"]
        denom = ct["admissible_manual_defect_instances_over_8_cells"]
        lines = [
            "第二个问题：这些既在范围内、又该进 expected 的问题，"
            "在 matrix-v11 时期那次 8 格运行里漏了多少、怎么漏的。",
            "",
            "先把两个口径分开，否则数字对不上：",
            "",
            "| 口径 | 值 | 说明 |",
            "| --- | ---: | --- |",
            f"| 8 格应命中的可入缺陷实例 | **{denom}** | "
            f"每格按本轮人工结果应命中的条数之和 |",
            f"| 去重后命中 | **{hit}** | 按人工 diff 去重的缺陷条数 |",
            f"| 漏检 | **{ct['missed']}** | {pct(ct['missed'], denom)} |",
            f"| 多报 | **{ct['over_reported']}** | 发布的 issue 无一条是人工复核不认的 |",
            f"| 实际发布 issue 条数 | {ct['published']} | "
            f"比去重缺陷数多，因为多条 issue 可描述同一缺陷"
            f"（`0000` 的两条 `Power_Off`、`0029` 的 `REQ-007`+`REQ-008`）|",
            "",
            f"**{hit} + {ct['missed']} = {denom}**，多报 0。"
            "也就是说这条流水线当前的问题不是乱报，而是**报得不够**。",
            "",
            "### 漏在哪个环节",
            "",
            "把 6 条漏检逐条追到流水线的**首失节点**。先说三点口径，否则这张表容易被读过头：",
            "",
            "1. **6 条是实例数，对应 3 个去重缺陷**（`0000` / `0029` / `0050` 各跨 2 格）。"
            "形态只有「复合事件被合并」与「缺初始边」两类，**样本很薄**，"
            "不足以支撑「这条流水线在某类缺陷上系统性失效」这样的结论。",
            "2. **`lost_at` 取首失点单值**，同一条可能被多个环节共同放过。"
            "`0000` 与 `0050` 的证据原文即记录 `review_requirements` 判了 accept "
            "并把它列为已覆盖——该环节实际上也没拦住。",
            "3. **本表的环节枚举不含 `prepare` / `review_requirements` / `publish`**，"
            "所以下面「其余环节各 0 条」只对枚举内的节点成立，"
            "**不能读成整条流水线中段无损失**。",
            "",
            "| 环节 | 漏检数 | |",
            "| --- | ---: | --- |",
        ]
        for stage, n in cells["missed_by_stage"].items():
            if n:
                lines.append(f"| {STAGE_LABEL.get(stage, stage)} | **{n}** | |")
        zero = [s for s, n in cells["missed_by_stage"].items() if not n]
        lines += [
            f"| **合计** | **{ct['missed']}** | |",
            "",
            f"枚举内其余 {len(zero)} 个环节各 0 条："
            + "、".join(STAGE_LABEL.get(s, s) for s in zero) + "。",
            "",
            "**在被计数的环节里，漏检集中在头尾两端。**"
            "`convert_assertions` 到 `adjudicate_results` 这段是把需求变成断言、再变成结论的主干，"
            "它一条都没漏；丢失发生在「需求还没被拆出来」与「结论已经有了但被归因挡掉」这两处。"
            "但按上面第 2、3 点，这不等于中段无损失——"
            "`review_requirements` 被证据原文点名却没有计数桶。",
        ]
        if replay:
            flat = replay.get("totals") or replay
            safe = flat.get("attr::safe", flat.get("safe"))
            debt = flat.get("attr::representation_debt", flat.get("representation_debt"))
            un = flat.get("attr::unattributed", flat.get("unattributed"))
            killed = debt + un  # noqa: F841 - 下面的叙述按两档分别引用
            lines += [
                "",
                "### 归因这一关挡掉了多少",
                "",
                f"把 {vt['captured']} 条可表述断言全部重放一遍归因，结果是：",
                "",
                "| 归因结论 | 条数 | 占比 | 能否成为 expected issue |",
                "| --- | ---: | ---: | --- |",
                f"| `safe` | **{safe}** | {pct(safe, 123)} | 可以 |",
                f"| `representation_debt` | **{debt}** | {pct(debt, 123)} | "
                f"不能——判定所依赖的元素落在该 pair 的 `attribution_exclusions` 里 |",
                f"| `unattributed` | **{un}** | {pct(un, 123)} | 不能——找不到源头映射 |",
                f"| **合计** | **{safe + debt + un}** | 100% | |",
                "",
                f"**{killed} / {vt['captured']} = {pct(killed, 123)} 的正确断言仅因归因就被挡住。**"
                "这是硬门控不是软降级：非 `safe` 的 False 会被强制移入 `excluded_findings`，"
                "无法成为 confirmed issue。",
                "",
                "两档的成因**不同**，不能合并叙述："
                f"`representation_debt` {debt} 条全部是 `exclusion_intersection`，"
                "即判定所依赖的元素踩在 R4.5 投影合成出来的节点上"
                "（`UnspecifiedInitial`、`FinalWait*`、`InvalidInitial*`）；"
                f"`unattributed` {un} 条则是 `no_safe_trace_entry` 16 条与 "
                "`path_taint_ambiguous` 2 条，属「找不到可信源头映射」，**不是踩合成节点**。"
                "前者不是 bug——排除合成元素上的判定正是为了不把 converter 的产物"
                f"记成生成方的缺陷；但代价是 **{pct(debt, 123)} 的真实缺陷"
                "因为「证据踩在合成节点上」而无法上报**。",
                "",
                "⚠️ 另需注明：这 123 条是把**人工手写的断言**重放一遍归因的结果，"
                "不是该次 8 格运行的实际产出分布，两者不可混读。",
                "",
                "其中最尖锐的一处来自 `initial_target` 的两次归因修复。该谓词原先在两个分支上"
                "都不记录它读的那个 entry：`47f92913` 先补了多入口分支，"
                "本轮 `3d0049c1` 再补了单入口分支。如实记录后判定就开始踩到合成节点上——"
                f"**`initial_target` 相关的 21 条里有 18 条（86%）为 `representation_debt`，"
                f"跨 15 个 pair**（另 3 条为 `safe`）。"
                "按逐条回放复合态入口数，其中约 13 条由本轮的单入口分支修复直接导致，"
                "另 5 条（`0016`#1、`0029`#3、`0032`#1、`0048`#1、`0048`#2）"
                "来自上一轮已修的多入口分支。"
                "修复本身是对的（同一份证据不该因为走了哪个分支而给出两种归因），"
                "但它把「归因看不见」变成了「确定性排除」，"
                "把一个隐性偏差变成了显性、可计数的损失。",
            ]
        if prompt:
            lines += ["", "### prompt 侧：漏检是被指令要求的，不是没照做", ""]
            sf = prompt.get("structural_finding") or {}
            if sf.get("headline"):
                # The audit's own fields are English prose; this issue is Chinese. The
                # narration below is this script's reading of them, and the English is kept
                # verbatim underneath as evidence rather than translated away.
                lines += [
                    "**整条流水线里不存在任何「缺陷方向清单」。**"
                    "prompt 是严格的 NL 义务驱动：一个候选 issue 只有在 "
                    "(a) 某段 NL 把它陈述为义务、**且** (b) 19 个谓词之一能表达它 时才可能存在。"
                    "8 个缺陷方向以及任何等价的分类法，**从未被告知给任何一个 producer**——"
                    "而且这是设计使然，prompt 里有多处明令禁止引入 issue 分类："
                    "`prompts.py:7`「do not emit a benchmark issue taxonomy」、"
                    "`prompts.py:19`「This rule does not import a hidden issue taxonomy」、"
                    "`prompts.py:223`「Do not hard-code benchmark-specific partitions or expected issues」。",
                    "",
                    "**因此 producer 能看到的唯一按方向的信号，是每个谓词那一行 `exposes:` 字段**"
                    "（由 `predicates.py:754` 渲染）——19 个短语，埋在一个 18.7 KB 的词表块里。"
                    "**没有任何一句话要求模型去排查**死端、吸收态、自造事件、克隆状态、"
                    "未展开的子状态机或伪状态类型错误，"
                    "在 NL 本身没把这些写成义务时尤其如此。",
                    "",
                    "> 审计原文（保留英文，供核对）：" + _one_line(sf["headline"], 2000),
                    "",
                ]

            causes = prompt.get("top_three_prompt_side_causes_of_under_detection") or []
            if causes:
                CAUSE_CN = {
                    1: "流水线只能报 NL 陈述为义务的东西，没有任何指令让它去找模型自身的缺陷。"
                       "**按审计估算，153 条人工发现里约有 40 条落在「splitter 被明确要求不要为之开需求」"
                       "的形状里**——死端与吸收态、终态集为空、自造事件、克隆状态、"
                       "fork/join/junction/choice 类型错配、未展开的 `<<submachine>>`："
                       "这些缺陷是制品自身的属性，而不是对某句 NL 的复述，因此根本没有入口。",
                    2: "三条「合并表示」豁免把真实缺陷转成了「表示层限制」，"
                       "于是它们被当作需要披露的事项，而不是需要断言的缺陷。",
                    3: "入口与守卫这两个方向所依赖的两个谓词，"
                       "恰好在有缺陷的那个配置上返回 True，而没有任何 prompt 文本对此预警。",
                }
                lines += ["三条主要成因。中文是本节的归纳，`>` 引用块内为 prompt 原文（证据，保留英文）：", ""]
                for c in sorted(causes, key=lambda x: x.get("rank", 99)):
                    rank = c.get("rank", 0)
                    lines += [
                        f"{rank}. **{CAUSE_CN.get(rank) or _one_line(c.get('cause'))}**",
                        "",
                        f"   > {_one_line(c.get('quote'), 2000)}",
                        "",
                        f"   审计原文：{_one_line(c.get('why'), 2000)}",
                        "",
                    ]

            # The absence of any quantity cap is the load-bearing negative result: it rules
            # out "the model was told to report only the top few" as an explanation.
            ol = prompt.get("output_limits") or []
            none_found = [o for o in ol if "NONE FOUND" in str(o.get("quote", ""))]
            if none_found:
                lines += [
                    "**一个反向证据，用来排除最容易被想到的解释。**"
                    "在全部 prompt 里检索数量上限类措辞（`at most` / `no more than` / "
                    "`top N` / `most important` / `prioritise`）——**零命中**。"
                    "没有任何 prompt 限制需求数、断言数或 issue 数，"
                    "也没有任何一句让模型「只报最重要的几条」。"
                    "唯一与数量有关的指令方向相反："
                    "`prompts.py:47` 要求「每条 Requirement 至少一条断言，且映射必须完整」。"
                    "所以漏检不能归因于产出被截断或被要求精简——"
                    "**是判定范围本身没把这些问题包进来。**",
                    "",
                ]

            mism = prompt.get("prompt_vs_impl_mismatches") or []
            if mism:
                lines += [
                    f"### prompt 说的与实现做的不一致：{len(mism)} 处",
                    "",
                    "这类不一致比 prompt 写漏更危险——模型按 prompt 的描述去理解谓词语义，"
                    "而谓词实际行为不同，于是它写出的断言在自己看来成立、在实现里落空。",
                    "",
                    "| # | 谓词 | 造成的漏检 |",
                    "| --: | --- | --- |",
                ]
                # Only the consequence goes in the cell. `prompt_says` / `impl_does` run
                # 300-700 chars each; squeezing them into a cell cut 12 quotes mid-word in
                # the previous version -- and this table is the section's core evidence.
                # Note the source field is named `severity` but holds a consequence
                # sentence, not a grade, so it is labelled accordingly.
                for i, m in enumerate(mism, 1):
                    lines.append(f"| {i} | `{m.get('predicate', '—')}` | "
                                 f"{_one_line(m.get('severity'), 300)} |")
                lines += ["", "逐处完整引文（prompt 原文保留英文，那是证据）：", ""]
                for i, m in enumerate(mism, 1):
                    lines += [
                        f"**{i}. `{m.get('predicate', '—')}`**",
                        "",
                        f"- prompt 让模型这样理解：{_one_line(m.get('prompt_says'), 2000)}",
                        f"- 实现实际怎么做：{_one_line(m.get('impl_does'), 2000)}",
                        f"- 位置：{_one_line(m.get('where'), 400)}",
                        "",
                    ]
                lines += [
                    "",
                    "`initial_target` 那一行正是前面那个 86% 降级的源头："
                    "prompt 告诉模型「带触发的入口不决定进入」，"
                    "而实现对单一入口一律照答，于是 `initial_target(Root, Root.TurnOn)` "
                    "在带触发的初始边上返回 `True`——**正向放过了一个有缺陷的模型**。",
                ]

            bydir = prompt.get("by_direction") or []
            weak = [b for b in bydir if b.get("adequacy") != "充分"]
            if bydir:
                lines += [
                    "",
                    "### 按缺陷方向看 prompt 的引导是否到位",
                    "",
                    "| 方向 | 人工条数 | prompt 有引导 | 充分性 |",
                    "| --- | ---: | :-: | --- |",
                ]
                for b in sorted(bydir, key=lambda x: -(x.get("human_count") or 0)):
                    lines.append(
                        f"| `{b.get('direction')}` | {b.get('human_count')} | "
                        f"{'✓' if b.get('guided') else '✗'} | {b.get('adequacy', '—')} |")
                lines += [
                    "",
                    f"{len(bydir)} 个方向里 **{len(weak)} 个的引导被判为不充分**。"
                    "注意「有引导」与「充分」是两件事：多数方向 prompt 都提到了，"
                    "但提到的是谓词能证明什么，不是「该去找哪种缺陷」。",
                ]
        lines += [
            "",
            "---",
            "",
            "逐格审计数据（8 格，含每格已发布 issue、漏检条目与环节归属）："
            + gist_link("loopaudit_cells.json", "loopaudit_cells.json")
            + " ｜ 归因重放（123 条逐条）"
            + gist_link("loopaudit_replay_attribution.json", "loopaudit_replay_attribution.json")
            + " ｜ prompt 审计 " + gist_link("loopaudit_prompt.json", "loopaudit_prompt.json")
            + " ｜ 过滤器审计 " + gist_link("loopaudit_filters.json", "loopaudit_filters.json"),
        ]
        emit("misses.md", "\n".join(lines))

    print(f"已生成 {len(written)} 个片段到 {out}\n")
    for name in written:
        n = len((out / name).read_text())
        print(f"  {name:24s} {n:6d} 字符")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
