"""机械核验：每条引文是否**逐字**存在于它自称的出处，且落在允许的节里。

⛔ 本工具**只做定位，不做裁定**（仓库纪律〈机械代理只能定位不能裁定〉）。它回答的是
「这句话在不在那里」，⛔ **不回答**「这句话算不算一条义务」—— 后者必须人工读原文。

三项检查：

1. **逐字存在**：引文（归一化空白后）出现在该案例的 `### 1. 原文摘录` 节里。
   ⚠️ 允许省略号切分：引文含 `...` / `…` 时，按片段分别检查且要求保持先后顺序。
2. **节位合法**：⛔ 引文若只出现在 `### 2. 基于原文整理后的自然语言描述`（我们自己写的
   英文转述）里，判 `WRONG_SECTION` —— 拿它当外部依据等于自证。
3. **义务标志词在场**：`obligation_marker` 是否逐字出现在引文里。
   ⚠️ 这一项**只是线索**：标志词在场**不等于**它表达义务（"was discharged **until** …" 是
   实验叙述，"three modes: A, B, C" 是列举），⛔ 判定仍归人工。

用法：

    python verify_quotes.py --findings findings.json --out report.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_ENTRY_HEAD = re.compile(r"^## 条目\s*\d+\s*[:：]\s*(.+?)\s*$")
_H3 = re.compile(r"^### (\d+)\.")
_ELLIPSIS = re.compile(r"\s*(?:\.\.\.|…)\s*")


def _find_sources() -> Path:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "sources" / "SUMMARY.md"
        if candidate.is_file():
            return candidate.parent
    raise RuntimeError("向上未找到 sources/SUMMARY.md")


def _norm(text: str) -> str:
    """归一化：折叠空白、去掉 Markdown 引用前缀与强调标记、统一引号。

    ⛔ 不做大小写归一 —— 引文要求逐字，大小写不同就是改写过。
    """
    text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)
    text = text.replace("**", "").replace("`", "")
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", text).strip()


def _sections(stm_md: Path) -> dict[str, str]:
    """返回该文件**所有条目**各 `### N.` 节正文的并集，键是节号字符串。

    ⚠️ 按条目定位是错的：3 个目录各含 2 个界内条目，按 directory 建索引会漏掉第二个，
    使那些条目下的合法引文被误判 `NOT_FOUND`（首版就栽在这里）。⭐ 而本工具要回答的问题
    是「这句话在不在**摘录节**里」，⛔ 不是「它在不在**哪个条目的**摘录节里」——
    节位合法性只取决于节号，与条目无关。
    """
    if not stm_md.is_file():
        return {}
    lines = stm_md.read_text(encoding="utf-8").splitlines()

    out: dict[str, list[str]] = {}
    current: str | None = None
    for line in lines:
        if _ENTRY_HEAD.match(line) or line.startswith("## "):
            current = None
            continue
        m = _H3.match(line)
        if m:
            current = m.group(1)
            out.setdefault(current, [])
            continue
        if current is not None:
            out[current].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def _contains_in_order(haystack: str, fragments: list[str]) -> bool:
    pos = 0
    for frag in fragments:
        if not frag:
            continue
        idx = haystack.find(frag, pos)
        if idx < 0:
            return False
        pos = idx + len(frag)
    return True


def check(finding: dict, sources: Path) -> dict:
    directory = finding.get("directory", "")
    quote = finding.get("verbatim_quote", "")
    marker = finding.get("obligation_marker", "")
    stm = sources / directory / "STM.md"

    result = {
        "directory": directory,
        "predicate": finding.get("predicate"),
        "quote_head": quote[:90],
        "quote_status": None,
        "found_in_sections": [],
        "marker_status": None,
    }

    if not stm.is_file():
        result["quote_status"] = "NO_SOURCE_FILE"
        return result

    secs = _sections(stm)
    if not secs:
        result["quote_status"] = "NO_SECTIONS"
        return result

    frags = [_norm(f) for f in _ELLIPSIS.split(quote) if _norm(f)]
    for num, body in secs.items():
        if _contains_in_order(_norm(body), frags):
            result["found_in_sections"].append(num)

    if not result["found_in_sections"]:
        result["quote_status"] = "NOT_FOUND"
    elif "1" in result["found_in_sections"]:
        result["quote_status"] = "OK"
    else:
        # 只在转述节 / 判定节里找到 —— 这是自证，必须打回
        result["quote_status"] = "WRONG_SECTION"

    if marker:
        result["marker_status"] = "OK" if _norm(marker).lower() in _norm(quote).lower() else "MARKER_NOT_IN_QUOTE"
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--findings", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--sources", type=Path, default=None)
    args = parser.parse_args(argv)

    sources = args.sources if args.sources is not None else _find_sources()
    findings = json.loads(args.findings.read_text(encoding="utf-8"))

    reports = [check(f, sources) for f in findings]
    from collections import Counter

    counts = Counter(r["quote_status"] for r in reports)
    marker_counts = Counter(r["marker_status"] for r in reports if r["marker_status"])

    print(f"核验 {len(reports)} 条")
    for k, v in counts.most_common():
        print(f"  引文 {k}: {v}")
    for k, v in marker_counts.most_common():
        print(f"  标志词 {k}: {v}")

    bad = [r for r in reports if r["quote_status"] != "OK"]
    for r in bad[:25]:
        print(f"  ⛔ {r['quote_status']:16s} {r['directory']:50s} {r['predicate']}")
        print(f"      {r['quote_head']}")

    if args.out:
        args.out.write_text(json.dumps(reports, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
