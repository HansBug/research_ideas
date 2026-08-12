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


def _domain_diversity_ok(n_sources: int, n_domains: int) -> bool:
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
    "main/heimdahl_tse96.txt": "doi:10.1109/32.503933",
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
            key = canonical_source(f)
            slot = evidence[pred].setdefault(
                key,
                {
                    "kind": "literature",
                    "domain": f.get("system_or_domain", "?"),
                    "read_level": f.get("read_level"),
                    "title": f.get("title"),
                    "n_quotes": 0,
                },
            )
            slot["n_quotes"] += 1

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
                "corpus_domains": sorted(domains),
                "n_corpus_domains": len(domains),
                "corpus_diversity_ok": _domain_diversity_ok(len(real), len(domains)),
                "meets_target": len(srcs) >= TARGET_SOURCES,
                "meets_minimum": len(srcs) >= MIN_SOURCES,
                "source_keys": sorted(srcs),
            }
        )

    width = max(len(r["predicate"]) for r in rows)
    print(f"{'谓词'.ljust(width)}  族  真实系统  文献  合计  语料领域  语料多样性  达标(>={TARGET_SOURCES})")
    for r in rows:
        flag = "✅" if r["meets_target"] else ("🟡" if r["meets_minimum"] else "⛔")
        div = "✅" if r["corpus_diversity_ok"] else "⛔"
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
            json.dumps({"rows": rows, "evidence": {k: v for k, v in evidence.items()}}, ensure_ascii=False, indent=1),
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
