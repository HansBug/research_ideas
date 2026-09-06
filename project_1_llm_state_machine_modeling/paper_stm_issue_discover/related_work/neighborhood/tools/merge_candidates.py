"""把八路检索各自的候选表合并去重成一张总表。

⭐ 存在的理由：八路检索是**故意重叠**的（arXiv / ACM / IEEE / 语义 / venue / 本地 / 引文 /
综述都会捞到同一批热门工作），⛔ 重叠本身是覆盖度的证据，⭐ 但总表必须去重，
否则「候选 N 篇」这个数字会被重复计数虚高。

⛔ **去重优先级**（与仓库 `CLAUDE.md` 论文集规范一致）：

1. DOI（标准化后精确匹配）
2. arXiv id（去版本号，`2501.01234v2` → `2501.01234`）
3. 标准化标题（小写、去非字母数字、压空格）

⚠️ **第 3 条会漏**：同一工作的会议版与期刊版标题常有细微差异（副标题、"Extended"
前缀）。⛔ 本脚本**不做模糊匹配** —— 那会把不同工作误并。⭐ 疑似重复由人工在
`search_ledger.md` 的「疑似重复待裁」一节处理。

用法::

    python -m tools.merge_candidates --src /tmp/l3/search --out candidates.jsonl
    python -m tools.merge_candidates --src /tmp/l3/search --markdown
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

#: ⭐ arXiv id 的两种写法都要认：新式 `2501.01234`、旧式 `cs.SE/0501001`。
_ARXIV = re.compile(r"(?:arxiv[.:/ ]+)?(\d{4}\.\d{4,5})(?:v\d+)?", re.I)
_DOI = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")


def norm_title(s: str) -> str:
    """标题标准化。

    ⚠️ `.lower()` 必须在 `re.sub` **之前** —— 少了它，`[^a-z0-9]` 会把所有大写字母
    当成分隔符替换掉，于是仅大小写不同的标题反而合并不上。⛔ 本仓库在 L2 的
    `merge_by_title` 上栽过一次同样的坑。
    """
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def norm_doi(s: str) -> str | None:
    m = _DOI.search(s or "")
    if not m:
        return None
    #: ⭐ 末尾常被 markdown 链接语法带上 `)` 或 `.`，剥掉。
    return m.group(0).rstrip(").,;").lower()


def norm_arxiv(s: str) -> str | None:
    m = _ARXIV.search(s or "")
    return m.group(1) if m else None


def parse_tables(path: Path) -> list[dict]:
    """从一份 markdown 里抽出所有像候选表的行。

    ⛔ 不假设列顺序 —— 八路 agent 的表头会有出入。⭐ 按表头文字认列，
    认不出的列原样塞进 `extra`，⛔ 不丢弃（丢弃会静默损失信息）。
    """
    rows: list[dict] = []
    header: list[str] | None = None
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells if c):
            continue  #: 分隔行
        if header is None:
            header = cells
            continue
        if len(cells) != len(header):
            continue
        rec = dict(zip(header, cells))
        #: ⭐ 只保留看起来是候选行的：必须有标题样的字段且有年份或链接。
        blob = " ".join(cells)
        if len(blob) < 20:
            continue
        rows.append({"_src": path.name, **rec})
    return rows


def pick(rec: dict, *keys: str) -> str:
    for k in rec:
        kl = k.lower()
        if any(t in kl for t in keys):
            v = (rec[k] or "").strip()
            if v and v not in {"-", "—", "n/a"}:
                return v
    return ""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", type=Path, default=Path("/tmp/l3/search"))
    #: ⛔⛔ 默认 glob **必须**是 `A*_*.md` 而不是 `*.md`。
    #: ⚠️ 实测：检索 agent 会往同一目录写临时抓取物（`paper_clean.md`、`atlas.txt`、
    #: `hal.html` …）。⛔ 用 `*.md` 会把 `paper_clean.md` 里的**论文正文表格**
    #: 当成候选表解析进来 —— ⭐ 而且它长得很像候选表（有 `|`、有标题、有年份），
    #: ⛔ **不会报错，只会让候选数虚高且混入不存在的条目**。
    ap.add_argument("--glob", default="A*_*.md", help="⛔ 别放宽成 *.md")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--markdown", action="store_true")
    args = ap.parse_args(argv)

    files = sorted(args.src.glob(args.glob))
    if not files:
        print(f"⛔ {args.src} 下没有 .md，检索还没产出。", file=sys.stderr)
        return 2

    raw: list[dict] = []
    per_file = Counter()
    for f in files:
        got = parse_tables(f)
        per_file[f.name] = len(got)
        raw.extend(got)

    #: 三级 key 归并。⭐ 一条记录可能同时有 DOI 与 arXiv，两个 key 都要建索引，
    #: 否则 A 路只给 DOI、B 路只给 arXiv 时会漏并。
    merged: dict[str, dict] = {}
    alias: dict[str, str] = {}

    def resolve(k: str) -> str:
        seen = set()
        while k in alias and k not in seen:
            seen.add(k)
            k = alias[k]
        return k

    for rec in raw:
        blob = " ".join(str(v) for v in rec.values())
        title = pick(rec, "标题", "title")
        keys = []
        if d := norm_doi(blob):
            keys.append(f"doi:{d}")
        if a := norm_arxiv(blob):
            keys.append(f"arxiv:{a}")
        if title and (nt := norm_title(title)):
            keys.append(f"title:{nt}")
        if not keys:
            continue
        keys = [resolve(k) for k in keys]
        primary = next((k for k in keys if k in merged), keys[0])
        for k in keys:
            if k != primary:
                alias[k] = primary
        slot = merged.setdefault(primary, {"keys": set(), "srcs": set(), "rows": []})
        slot["keys"].update(keys)
        slot["srcs"].add(rec["_src"])
        slot["rows"].append(rec)

    out = []
    for key, slot in merged.items():
        rows = slot["rows"]
        blob = " ".join(str(v) for r in rows for v in r.values())
        out.append({
            "key": key,
            "title": max((pick(r, "标题", "title") for r in rows), key=len, default=""),
            "year": next((y for r in rows if (y := pick(r, "年", "year"))), ""),
            "venue": next((v for r in rows if (v := pick(r, "venue", "会议", "期刊"))), ""),
            "doi": norm_doi(blob) or "",
            "arxiv": norm_arxiv(blob) or "",
            "boundary": next((b for r in rows if (b := pick(r, "边界", "boundary"))), ""),
            "llm_gate": next((g for r in rows if (g := pick(r, "llm"))), ""),
            "task": next((t for r in rows if (t := pick(r, "任务", "task"))), ""),
            "found_by": sorted(slot["srcs"]),
            "n_sources": len(slot["srcs"]),
        })
    out.sort(key=lambda r: (-r["n_sources"], r.get("year", ""), r["title"]))

    print(f"# 候选合并\n", file=sys.stderr)
    print(f"- 输入文件 {len(files)} 份，原始行 {len(raw)}", file=sys.stderr)
    for n, c in per_file.most_common():
        print(f"  - {n}: {c}", file=sys.stderr)
    print(f"- ⭐ 去重后 **{len(out)}** 条", file=sys.stderr)
    overlap = Counter(r["n_sources"] for r in out)
    print(f"- 被 k 路同时捞到的分布：{dict(sorted(overlap.items()))}", file=sys.stderr)

    if args.out:
        args.out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in out), encoding="utf-8")
        print(f"- 已写 {args.out}", file=sys.stderr)
    if args.markdown:
        print("| # | 标题 | 年 | Venue | 边界 | 任务 | 几路捞到 | 链接 |")
        print("| --: | :-- | :-- | :-- | :-- | :-- | --: | :-- |")
        for i, r in enumerate(out, 1):
            link = f"https://arxiv.org/abs/{r['arxiv']}" if r["arxiv"] else (f"https://doi.org/{r['doi']}" if r["doi"] else "")
            print(f"| {i} | {r['title'][:80]} | {r['year']} | {r['venue'][:24]} | {r['boundary']} | {r['task'][:20]} | {r['n_sources']} | {link} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
