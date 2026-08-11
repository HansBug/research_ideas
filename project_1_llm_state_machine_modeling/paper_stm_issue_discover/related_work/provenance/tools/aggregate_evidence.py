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


def canonical_source(finding: dict) -> str:
    """把 identifier 归一到「一篇论文一个键」。

    ⚠️ **这不是洁癖，是修一个真实的计数缺陷。** 同一篇论文在不同条目里的 identifier
    写法各异 —— 实测 Dwyer ICSE 1999 出现过 `DOI 10.1145/302405.302672`、
    `DOI: 10.1145/302405.302672 ; 全文 PDF: …`、`https://matthewbdwyer.github.io/psp/`
    等 **6 种**写法，⛔ 按原样去重会把它算成 6 个独立来源。⭐ 而「多源」这条要求
    的全部意义就在于**源要互相独立**。

    归一优先级：DOI → arXiv ID → URL 的 host+path（去 query）→ 标题。
    """
    ident = finding.get("identifier") or ""
    m = _DOI.search(ident)
    if m:
        return "doi:" + m.group(0).rstrip(".,;)").lower()
    if "arxiv" in ident.lower():
        m = _ARXIV.search(ident)
        if m:
            return "arxiv:" + m.group(1)
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
