"""查出「拿本研究自己的材料当独立领域证据」的条目。

⭐ 这条检查的由来：一路裁定者发现有条目引了 `arXiv:2604.00275` 作独立文献，⛔ 而它
在本仓库里登记为**种子语料来源**。⚠️ 用被评测对象自身证明「这类检查在领域里常见」是
**自证式取证**（仓库根 `CLAUDE.md` §3.5）—— ⛔ 审稿人一旦发现会连带质疑整张表的取证纪律。

⛔ **三层身份，⛔ 后果完全不同，⛔ 不得一概而论**：

| 层 | 是什么 | 处置 |
| :-- | :-- | :-- |
| ⛔⛔ **seed** | `corpora/seed_library/` —— 本研究 NL+STM 对的**来源池** | ⛔ **剔除**：用自己的数据源证明自己的谓词该存在，是自证 |
| ⚠️ **baseline** | `baselines/` —— 本文定位为对照 / 相关工作的论文 | ⭐ **保留但必须标注**：引它说「该领域确实这么做」是正当的相关工作用法，⛔ 但不得混在独立文献里不作声 |
| ✅ **一般收藏** | `state_machine_types/` 等领域文库 | ✅ **无问题** —— ⭐ 一篇论文碰巧被我们收藏，⛔ 不使它变成「我们的」 |

⛔ **身份判定只认该目录自己那篇**（`bibtex.bib` 的第一条 entry 的 title / doi / eprint）。
⚠️ 首版拿目录里**全部文本**的 DOI 做匹配，⛔ 于是把 `DESC.md` **参考文献列表**里的
Harel 1987 也算成「我们的」—— ⭐ 那是彻底的误报，⛔ 而误报会把真问题淹掉。

用法：

    python detect_self_citation.py --findings cd_findings.json --out self_cite.json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def _find_project_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "baselines").is_dir() and (parent / "sources").is_dir():
            return parent
    raise RuntimeError("向上未找到 project_1 根（需同时含 baselines/ 与 sources/）")


def _own_identity(directory: Path) -> tuple[str, str | None, str | None] | None:
    """取该目录**自身**那篇的 (title, doi, arxiv_id) —— ⛔ 只看 bibtex 第一条 entry。"""
    bib = directory / "bibtex.bib"
    if not bib.is_file():
        return None
    text = bib.read_text(encoding="utf-8", errors="replace")
    first = text.split("@")[1] if "@" in text else text
    m_title = re.search(r'title\s*=\s*[{"]+(.+?)[}"]+\s*,', first, re.S | re.I)
    if not m_title:
        return None
    m_doi = re.search(r'doi\s*=\s*[{"]([^}"]+)', first, re.I)
    m_arx = re.search(r'(?:eprint|arxiv)\s*=\s*[{"]?\s*(\d{4}\.\d{4,5})', first, re.I)
    title = re.sub(r"\s+", " ", m_title.group(1)).strip()
    return title, (m_doi.group(1) if m_doi else None), (m_arx.group(1) if m_arx else None)


def _norm(text: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def build_index(root: Path) -> dict[tuple[str, str], tuple[str, str | None, str | None]]:
    index: dict[tuple[str, str], tuple[str, str | None, str | None]] = {}
    for kind, parent in (
        ("seed", root / "paper_stm_issue_discover" / "corpora" / "seed_library"),
        ("baseline", root / "baselines"),
    ):
        if not parent.is_dir():
            continue
        for d in sorted(parent.iterdir()):
            if not d.is_dir():
                continue
            identity = _own_identity(d)
            if identity:
                index[(kind, d.name)] = identity
    return index


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--findings", type=Path, required=True)
    p.add_argument("--out", type=Path)
    p.add_argument("--root", type=Path, default=None)
    args = p.parse_args(argv)

    root = args.root or _find_project_root()
    index = build_index(root)
    findings = json.loads(args.findings.read_text(encoding="utf-8"))

    flagged = []
    for i, f in enumerate(findings):
        ftitle = _norm(f.get("title"))
        fident = f.get("identifier") or ""
        for (kind, slug), (title, doi, arx) in index.items():
            same_title = bool(ftitle) and _norm(title) == ftitle
            same_doi = bool(doi) and doi in fident
            same_arx = bool(arx) and arx in fident
            if same_title or same_doi or same_arx:
                flagged.append(
                    {
                        "index": i,
                        "kind": kind,
                        "slug": slug,
                        "predicate": f.get("predicate"),
                        "title": f.get("title"),
                        "matched_on": "title" if same_title else ("doi" if same_doi else "arxiv"),
                    }
                )
                break

    seed = [x for x in flagged if x["kind"] == "seed"]
    baseline = [x for x in flagged if x["kind"] == "baseline"]
    print(f"检查 {len(findings)} 条证据，比对 {len(index)} 个自有目录")
    print(f"⛔⛔ 引了**种子语料来源**（自证，须剔除）：{len(seed)} 条")
    for x in seed:
        print(f"    {x['predicate']:22s} ← {x['slug']}（{x['matched_on']}）")
    print(f"⚠️ 引了 **baselines/**（须标注，⛔ 不必然剔除）：{len(baseline)} 条")
    for x in baseline:
        print(f"    {x['predicate']:22s} ← {x['slug']}（{x['matched_on']}）")

    if args.out:
        args.out.write_text(json.dumps(flagged, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
