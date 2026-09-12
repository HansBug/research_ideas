"""按谓词聚合证据：独立来源数 + 领域覆盖 + 缺口。

⭐ **计数单位是「互相独立的真实系统」，⛔ 不是「条目数」。** 同一篇论文里摘出三句话
支撑同一条谓词，那仍然只是**一个**来源 —— 否则「多源」这条要求就被同一篇论文自己满足了。

⛔ **这里算出来的一切都不是比例。** `sources/` 不是抽样框（它的收录标准恰好选中了要测的
那个性质），任何 K/N 都是在因变量上做选择。见
`discover_matrix/docs/protocol/method_provenance_policy.md` §一.5。

⭐ 领域多样性判据：N 个源应覆盖 min(3, N) 个以上不同领域。

用法：

    python aggregate_evidence.py --phase-a phaseA.json --external cd.json --out agg.json
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

#: 19 条谓词的族归属，与 `discover/predicates.py` 的 family 字段一致
FAMILY = {
    "state_declared": "S", "variable_declared": "S", "event_declared": "S",
    "containment": "S", "initial_target": "S", "edge_declared": "S",
    "effect_declared": "S", "action_declared": "S", "guard_distinguishable": "S",
    "cardinality": "S",
    "occupancy_after": "B", "event_consumed": "B", "stays_in": "B",
    "variable_delta_after": "B", "reaches": "B", "terminates": "B",
    "invariant": "P", "response_within": "P", "persists_until": "P",
}

#: 用户在 L2 子 PR 上给的目标：每条谓词尽量不少于这个数的独立真实系统
TARGET_SOURCES = 6
#: policy §一.5 的硬下限
MIN_SOURCES = 3


def _domain_diversity_ok(n_sources: int, n_domains: int) -> bool | None:
    """N 个源应覆盖 min(3, N) 个以上不同领域；⭐ 无源时返回 None（**不适用**）。

    ⚠️ ⛔ **2026-08-12 修**：原实现在 `n_sources == 0` 时 `min(3, 0) == 0`，⭐ 判据**恒真** ——
    ⛔ 于是语料侧 0 源的 `containment` 与 `variable_delta_after` 拿到「多样性 ✅」，
    ⛔ 而 2 源 1 领域的 `initial_target` 反被标 ⛔。⭐ 任何读工具输出的人会得到相反印象。
    """
    if n_sources == 0:
        return None
    return n_domains >= min(3, n_sources)


_DOI = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")
_ARXIV = re.compile(r"(?:arxiv[:\s/]*)?(\d{4}\.\d{4,5})", re.I)

#: 本地抽取全文路径 —— ⭐ 开采本地 PDF 时 identifier 写作「文件路径:行号」。
_LOCAL = re.compile(r"(/tmp/[\w/.\-]+\.txt)")

#: ⭐⭐ **本地抽取文件 → 出版物**的显式映射。
#:
#: ⚠️ **为什么必须显式列表而不能靠正则**：⭐ 判断「`paperA.txt` 与 `paperA_thesis.txt`
#: 是同一项工作的技术报告版与博士论文版」是一次**学术判断**，⛔ 不是字符串相似度问题。
#: ⭐ 落在这张表里就必须能说清依据；⛔ 表外的路径按 `file:<basename>` 归一（⭐ 至少去掉行号），
#: ⛔ 但那只是止损，⭐ 新增开采源时应当在此登记。
#:
#: ⚠️ **这条修的是一个真实缺陷**（2026-08-12 补强轮实测）：⭐ 8 条 `guard_distinguishable`
#: 证据实际只来自 **4 份文档**，⛔ 而按含行号的原始串归一会算成 **8 个独立来源** ——
#: ⭐ 裁定者已独立指出「⛔ 写普遍性时按 4 计，不按 9 计」。⛔ 这与 docstring 里记的
#: 「Dwyer 一篇被算成 6 个」是**同一个缺陷、新的触发条件**。
_LOCAL_TO_WORK = {
    #: Heitmeyer, Jeffords, Labaw, ACM TOSEM 5(3), 1996（SCR 自动一致性检查）
    "hjl96_ase01/A.txt": "doi:10.1145/234426.234431",
    #: Heimdahl & Leveson, IEEE TSE 22(6), 1996（层次状态机需求的完备性与一致性）
    #: ⚠️ ⛔ **2026-08-12 更正**：此处原写 `doi:10.1109/32.503933`，⛔ 而该 DOI **不存在**
    #: （Crossref 返回 `Resource not found`）。⭐ 真实 DOI 由 Crossref 核出为 `10.1109/32.508311`
    #: （题录逐字吻合：Completeness and consistency in hierarchical state-based requirements,
    #: TSE 22(6):363-377, 1996）。⛔ 那个假 DOI 来自更早一轮某条已通过裁定的证据 —— ⭐ 即
    #: **裁定层不核验引用真实性**，⛔ 而 Q1/C+D 证据基从未跑过 `verify_citations.py`。
    "main/heimdahl_tse96.txt": "doi:10.1109/32.508311",
    #: ⭐ Torre 等的 UML 一致性规则工作：⭐ TR SCE-15-01（2016）与博士论文（2018）
    #: 是**同一项系统映射研究**的两个版本 —— ⛔ 规则表逐条同号同文，⛔ 不得计两个来源。
    "paperA.txt": "work:torre-uml-consistency-rules",
    "paperA_thesis.txt": "work:torre-uml-consistency-rules",
    #: Lange & Chaudron 一系（⭐ 2003 那篇是唯一显式建模状态机的）
    "lange_umlinconsist03.txt": "work:lange-uml-inconsistency",
    "lange_thesis.txt": "work:lange-uml-inconsistency",
    "lange_ease04.txt": "work:lange-uml-inconsistency",
    "lange_step05.txt": "work:lange-uml-inconsistency",
    "lange_exp_techreport.txt": "work:lange-uml-inconsistency",
    #: OORTs（UMD TR CS-TR-4353 / UMIACS-TR-2002-33）
    "oort_tr4353.txt": "url:cs.umd.edu/projects/softeng/eseg/papers/cs-tr4353.pdf",
    #: OMG UML 2.5.1（formal/2017-12-05）
    "uml251/uml251.txt": "url:omg.org/spec/uml/2.5.1",
}


#: ⭐⭐ **已核实的键别名**：⛔ 左侧是**经核验不存在或非规范**的标识符，⭐ 右侧是核验过的正确键。
#:
#: ⚠️ ⛔ **为什么需要它**：⭐ 同标题归并会保留字典序最小的键，⛔ 而那可能恰好是**假的**那个。
#: ⭐ 实测：`10.1109/32.503933` 与 `10.1109/32.508311` 指向同一篇（Heimdahl & Leveson,
#: TSE 22(6):363-377, 1996），⛔ 而前者在 Crossref 上返回 `Resource not found`、
#: ⭐ 后者题录逐字吻合。⛔ 让假 DOI 当代表键，等于把一条不可解析的引用写进交付表。
#:
#: ⛔ **准入**：⭐ 只收**逐条核验过**的别名（⭐ 核验方式写在注释里），⛔ 不许凭相似度加。
_KEY_ALIASES = {
    #: ⭐ Crossref 实测：`503933` → `Resource not found`；`508311` → 题录吻合
    "doi:10.1109/32.503933": "doi:10.1109/32.508311",
}


def _apply_alias(key: str) -> str:
    key = _KEY_ALIASES.get(key, key)
    return _SOURCE_FAMILIES.get(key, key)


def _local_work_key(ident: str) -> str | None:
    """本地抽取路径 → 出版物键；⛔ 未登记时退回 `file:<basename>`（⭐ 已去行号）。"""
    hits = _LOCAL.findall(ident)
    if not hits:
        return None
    for path in hits:
        for suffix, work in _LOCAL_TO_WORK.items():
            if path.endswith(suffix):
                return work
    #: ⛔ 未登记：⭐ 至少把行号去掉，⛔ 否则同一文件的不同行会被算成不同来源
    return "file:" + hits[0].rsplit("/", 1)[-1].lower()


#: ⭐⭐ **本文 baseline 来源**：⛔ 这些论文被本研究定位为**对照 / 相关工作**。
#:
#: ⚠️ [methodology.md](../methodology.md) §4.5 已定纪律：⭐ 「**保留但必须标注** —— ⭐ 引它说
#: 『该领域确实这么做』是正当的相关工作用法，⛔ **但不得混在独立文献里不作声**」。
#: ⛔ 而 2026-08-12 的敌意评审实测：⭐ 这 3 条仍在交付表里**未加任何标注**，
#: ⚠️ 且其所在行的备注列正在用来源数说「⭐ 同时有 N 个领域证据来源 —— 让 claim 更硬」。
#: ⛔ **拿自己的对照工作把自己的 claim 说硬，且不作声。**
#:
#: ⭐ 现改为**工具层强制**：⛔ 命中即在行内标出 `baseline_sources`，⛔ 不靠人记得。
#: ⚠️ ⛔ **它们不被剔除** —— ⭐ 引用相关工作本身合法，⛔ 缺的只是标注。
_BASELINE_MARKERS = (
    "2508.03215",      #: sysmbench —— A System Model Generation Benchmark from NL Requirements
    "2510.14348",      #: Automated Extraction of Protocol State Machines from 3GPP
    "sysmbench",
    "agentic-flow",
)


#: ⭐⭐ **同一事实的规约面与实现面**：⛔ 不得按面值计两个独立观测。
#:
#: ⚠️ [SUMMARY.md](../SUMMARY.md) §4.1 已定：⭐ 「**OMG UML 2.5.1 与前批的 Eclipse UML2
#: `validateInitialVertex` 是同一事实的规约与实现两面** —— ⛔ 日后任何 UML 家族证据
#: 被采纳时**不得按面值计两个独立观测**」。⛔ 而实测该规则**未被施行**：
#: `initial_target` 同时含两个键。⭐ 现改为工具层归并。
#:
#: ⛔ **准入从严**：⭐ 只收「⭐ 后者是前者的**参考实现或逐条转写**」这类关系
#: （⛔ 依据写在注释里），⛔ 不许凭「同一组织」或「主题相近」合并。
_SOURCE_FAMILIES = {
    #: ⭐ Eclipse UML2 把 OMG UML 规范的 constraint **逐条实现**成 `validate*` 方法
    #: （⭐ 实测方法名与数量 1:1 吻合：Region 4 / State 5 / Pseudostate 9 / Transition 9）
    "url:download.eclipse.org/modeling/mdt/uml2/javadoc/2.1.1/org/eclipse/uml2/uml/region.html":
        "work:omg-uml-2.5.1",
    "url:www.omg.org/spec/uml/2.5.1/pdf": "work:omg-uml-2.5.1",
    "url:omg.org/spec/uml/2.5.1": "work:omg-uml-2.5.1",
}

#: ⭐ 工具文档 / 语言规范 / 开源实现 —— ⛔ 用于报告来源**构成**。
#:
#: ⚠️ [coverage_audit.md](../coverage_audit.md) 点名要求：⭐ 「`initial_target` 的来源里
#: 同行评议为零……⛔ **这个构成必须写进表**，⚠️ 否则审稿人一查就是『你们最基础的
#: 一条谓词全靠 MathWorks 文档』」。⛔ 该要求此前未执行，⭐ 现改为工具层自动输出。
_TOOLDOC = re.compile(
    r"mathworks|itemis|eclipse|omg\.org|w3\.org|scxml|readthedocs|spesml|/docs?\.|github\.com",
    re.I,
)


def _is_toolset_source(key: str) -> bool:
    return bool(_TOOLDOC.search(key))


def _is_baseline(finding: dict) -> bool:
    blob = ((finding.get("identifier") or "") + " " + (finding.get("title") or "")).lower()
    return any(m in blob for m in _BASELINE_MARKERS)


def canonical_source(finding: dict) -> str:
    """把 identifier 归一到「一篇论文一个键」。

    ⚠️ **这不是洁癖，是修一个真实的计数缺陷。** 同一篇论文在不同条目里的 identifier
    写法各异 —— 实测 Dwyer ICSE 1999 出现过 `DOI 10.1145/302405.302672`、
    `DOI: 10.1145/302405.302672 ; 全文 PDF: …`、`https://matthewbdwyer.github.io/psp/`
    等 **6 种**写法，⛔ 按原样去重会把它算成 6 个独立来源。⭐ 而「多源」这条要求
    的全部意义就在于**源要互相独立**。

    归一优先级：DOI → arXiv ID → **本地抽取全文路径** → URL 的 host+path（去 query）→ 标题。

    ⭐ 「本地抽取全文路径」这一档是 2026-08-12 补强轮新增的，⛔ 见 `_LOCAL_TO_WORK`。
    """
    ident = finding.get("identifier") or ""
    m = _DOI.search(ident)
    if m:
        return "doi:" + m.group(0).rstrip(".,;)").lower()
    if "arxiv" in ident.lower():
        m = _ARXIV.search(ident)
        if m:
            return "arxiv:" + m.group(1)
    local = _local_work_key(ident)
    if local:
        return local
    m = re.search(r"https?://([^\s?#]+)", ident)
    if m:
        return "url:" + m.group(1).rstrip("/.,;").lower()
    if ident.strip():
        return "raw:" + re.sub(r"\s+", " ", ident.strip()).lower()[:120]
    return "title:" + re.sub(r"[^a-z0-9]+", " ", (finding.get("title") or "").lower()).strip()


def merge_by_title(evidence: dict) -> list[dict]:
    """同一谓词内、标准化标题完全相同的键合并为一个来源。

    ⚠️ ⛔ **这个函数必须被所有消费者共用。** `canonical_source` 逐条处理、看不到别的
    条目，因此同一篇论文若在不同条目里分别用了 DOI 与 arXiv ID，会被算成两个来源。
    ⛔ **2026-08-12 实测：该逻辑最初只写在 `aggregate_evidence.main()` 里，
    于是 `build_provenance_table` 不做归并、逐条表比总账多出 5 个来源。**
    ⭐ 这与「`canonical_source` 曾被复制两份」是同一类缺陷的第三次发作 ——
    ⛔ 凡是「两处都要做同一件事」的实现，必须共用一个函数，不能各写各的。

    ⛔ 归并判据从严：只在同一谓词内、标准化后标题完全相同且非空时合并；不做模糊匹配。
    """
    merge_log: list[dict] = []
    for pred, srcs in evidence.items():
        by_title: dict[str, list[str]] = defaultdict(list)
        for key, slot in srcs.items():
            #: ⚠️ ⛔ `.lower()` 不可省 —— 少了它，`[^a-z0-9]` 会把大写字母当分隔符替换掉，
            #: 于是仅大小写不同的同一标题会被判为两个。
            norm = re.sub(r"[^a-z0-9]+", " ", (slot.get("title") or "").lower()).strip()
            if norm:
                by_title[norm].append(key)
        for norm, keys in by_title.items():
            if len(keys) < 2:
                continue
            keep = sorted(keys)[0]
            for drop in sorted(keys)[1:]:
                srcs[keep]["n_quotes"] += srcs[drop]["n_quotes"]
                srcs[keep]["is_baseline"] = srcs[keep].get("is_baseline") or srcs[drop].get("is_baseline")
                del srcs[drop]
                merge_log.append({"predicate": pred, "title": norm[:80], "kept": keep, "merged": drop})
    return merge_log


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-a", type=Path, help="界内语料提取结果（来源 B）")
    parser.add_argument("--external", type=Path, nargs="*", default=[], help="来源 C/D 结果")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)

    # (predicate) -> {source_key: {"kind": ..., "domain": ..., "n_quotes": int}}
    evidence: dict[str, dict[str, dict]] = defaultdict(dict)

    if args.phase_a and args.phase_a.is_file():
        for f in json.loads(args.phase_a.read_text(encoding="utf-8")):
            pred = f.get("predicate")
            key = f"sources/{f.get('directory')}"
            slot = evidence[pred].setdefault(
                key, {"kind": "real_system", "domain": f.get("domain", "?"), "n_quotes": 0}
            )
            slot["n_quotes"] += 1

    for path in args.external:
        path = Path(path)
        if not path.is_file():
            continue
        for f in json.loads(path.read_text(encoding="utf-8")):
            pred = f.get("predicate")
            key = _apply_alias(canonical_source(f))
            slot = evidence[pred].setdefault(
                key,
                {
                    "kind": "literature",
                    "domain": f.get("system_or_domain", "?"),
                    "read_level": f.get("read_level"),
                    "title": f.get("title"),
                    "n_quotes": 0,
                    "is_baseline": _is_baseline(f),
                },
            )
            slot["n_quotes"] += 1
            if _is_baseline(f):
                slot["is_baseline"] = True

    #: ⭐⭐ **同标题归并**（2026-08-12 新增）—— ⛔ 修一个 `canonical_source` **在结构上修不了**的缺陷。
    #:
    #: ⚠️ `canonical_source` 逐条处理，⛔ **看不到别的条目**，⭐ 因此同一篇论文若在不同条目里
    #: 分别用了 DOI 与 arXiv ID（⭐ 或 DOI 与出版社 PDF URL），⛔ 会被算成两个独立来源。
    #: ⚠️ 【实测 2026-08-12】敌意评审在 5 条谓词上抓到这一形态：`guard_distinguishable`
    #: （Heimdahl & Leveson 的两个 DOI 串，⛔ 其中一个还不存在）· `event_consumed`
    #: （arXiv + DOI）· `invariant`（DOI + 出版社 PDF）· `reaches` / `response_within`
    #: （同一篇 Specification Patterns for Robotic Missions 的 arXiv + DOI）。
    #:
    #: ⛔ **归并判据从严**：⭐ 只在**同一条谓词内**、⭐ 且标准化后标题**完全相同且非空**时合并；
    #: ⛔ 不做模糊匹配（⚠️ 那会把不同论文错并，⭐ 而错并的方向是把数字做小、更难被发现）。
    #: ⭐ 每次合并都写进 `merged_by_title`，⛔ 便于审计。
    #: ⭐⭐ **具名真实系统轴**（2026-08-12 新增）。
    #:
    #: ⚠️ ⛔ **为什么单列一条轴而不是把它并进 `real_systems`**：⭐ `real_systems` 数的是
    #: **我们语料库 `sources/` 里的条目**，⛔ 而文献侧同样含大量具名真实系统
    #: （⭐ A-7E OFP · TCAS II · Darlington SDS1 · Volvo XC90 …）。⛔ 把后者并进前者会改变
    #: 一个已冻结列的语义；⭐ 单列则两边都能看，⛔ 且不动任何既有数字。
    #:
    #: ⛔ **判据写死，⛔ 不许事后放宽**：⭐ ① `named_system` 非空且不以 `NONE` 开头；
    #: ⭐ ② 裁定者的 `_named_ok` **不得**为 `overstated`（⚠️ 实测 11 条被判夸大）。
    #: ⛔ 未经裁定的条目不计入本轴。
    named_systems: dict[str, set[str]] = defaultdict(set)
    for path in args.external:
        path = Path(path)
        if not path.is_file():
            continue
        for f in json.loads(path.read_text(encoding="utf-8")):
            ns = (f.get("named_system") or "").strip()
            if not ns or ns.upper().startswith("NONE"):
                continue
            if f.get("_named_ok") == "overstated":
                continue
            #: ⭐ 同一系统在不同条目里的写法不同（⭐ 常带括注），⭐ 取首段做归一
            named_systems[f["predicate"]].add(ns.split("（")[0].split(" —— ")[0].strip()[:60])

    merge_log = merge_by_title(evidence)

    rows = []
    for pred, family in sorted(FAMILY.items(), key=lambda kv: (kv[1], kv[0])):
        srcs = evidence.get(pred, {})
        real = {k: v for k, v in srcs.items() if v["kind"] == "real_system"}
        lit = {k: v for k, v in srcs.items() if v["kind"] == "literature"}
        # ⛔ 领域多样性**只在语料侧算**。⚠️ 文献侧的 `system_or_domain` 是自由文本，
        # 几乎一条一个唯一串 —— 把它当领域数会得出「invariant 覆盖 41 个领域」这种假数。
        # ⭐ 文献侧的领域分散度是**定性**的，由各检索轨在 gap 报告里逐条说明，⛔ 不在此处编数。
        domains = {v["domain"] for v in real.values() if v["domain"] and v["domain"] != "?"}
        rows.append(
            {
                "predicate": pred,
                "family": family,
                "real_systems": len(real),
                "literature": len(lit),
                "total_sources": len(srcs),
                #: ⛔ 本文 baseline 来源（⭐ 保留但必须标注，见 `_BASELINE_MARKERS`）
                "baseline_sources": sorted(k for k, v in srcs.items() if v.get("is_baseline")),
                #: ⭐ 来源构成：⛔ 工具文档 / 规范 / 开源实现 占多少（⭐ coverage_audit 点名要求）
                "n_tooldoc_sources": sum(1 for k in srcs if _is_toolset_source(k)),
                "named_real_systems": sorted(named_systems.get(pred, ())),
                "n_named_real_systems": len(named_systems.get(pred, ())),
                #: ⭐ 语料侧条目 + 文献侧具名系统 —— ⛔ 两者都是「真实系统」，⭐ 只是来路不同
                "real_systems_total": len(real) + len(named_systems.get(pred, ())),
                "corpus_domains": sorted(domains),
                "n_corpus_domains": len(domains),
                "corpus_diversity_ok": _domain_diversity_ok(len(real), len(domains)),
                "meets_target": len(srcs) >= TARGET_SOURCES,
                "meets_minimum": len(srcs) >= MIN_SOURCES,
                "source_keys": sorted(srcs),
            }
        )

    if merge_log:
        print(f"⭐ 同标题归并 {len(merge_log)} 处（⛔ 否则会重复计数）：")
        for m in merge_log:
            print(f"   {m['predicate']:<24} {m['merged']}  →  {m['kept']}")
        print()

    width = max(len(r["predicate"]) for r in rows)
    print(f"{'谓词'.ljust(width)}  族  真实系统  文献  合计  语料领域  语料多样性  达标(>={TARGET_SOURCES})")
    for r in rows:
        flag = "✅" if r["meets_target"] else ("🟡" if r["meets_minimum"] else "⛔")
        div = {True: "✅", False: "⛔", None: "n/a"}[r["corpus_diversity_ok"]]
        print(
            f"{r['predicate'].ljust(width)}  {r['family']}  "
            f"{r['real_systems']:>8}  {r['literature']:>4}  {r['total_sources']:>4}  "
            f"{r['n_corpus_domains']:>8}  {div:>9}  {flag}"
        )

    below = [r["predicate"] for r in rows if not r["meets_target"]]
    print(f"\n未达 {TARGET_SOURCES} 源的谓词（{len(below)}）：{', '.join(below) if below else '无'}")
    nodiv = [r["predicate"] for r in rows if not r["corpus_diversity_ok"]]
    print(f"⚠️ 语料侧领域多样性不足（{len(nodiv)}）：{', '.join(nodiv) if nodiv else '无'}")
    print("⛔ 文献侧的领域分散度是定性的，见各检索轨的 gap 报告；此处不编数。")

    if args.out:
        args.out.write_text(
            json.dumps(
                {"rows": rows, "evidence": dict(evidence), "merged_by_title": merge_log},
                ensure_ascii=False, indent=1,
            ),
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
