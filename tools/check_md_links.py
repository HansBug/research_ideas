#!/usr/bin/env python3
"""扫全库 Markdown 引用，报出指不到东西的那些。

重构后最容易留下的伤是死链：文件搬走了，指向它的链接还停在旧路径。死链不会让任何
测试变红，只会让导引在读者点下去的那一刻失效——所以必须机器扫。

本工具查三类，缺一类就会把「零死链」误读成「引用都有效」：

1. **相对链接** ``[x](./y.md)``——目标文件是否存在。
2. **仓库内的绝对 GitHub blob URL**——``https://github.com/<owner>/<repo>/blob/<ref>/<path>``。
   ⚠️ 只查 ``--repo-slug`` 指定的那个仓库，其路径部分可以对着工作区校验。实测有一批
   ``manual_review/eis_issue/*.md`` 的 blob URL 停在改名前的旧路径，而只扫相对链接的
   版本**一条都报不出来**——「修复前 0、修复后 0」不代表没坏，代表尺子量不了。
3. **行号引用**——``见 xxx.md 第 N 行``。行号是脆定位符：一次纯格式化提交（自然段
   不折行）就重排了大量文件，10 处引用里 9 处失效、4 处越界到文件长度之外。它**静默
   失效**：文件在、链接通、只有行号错，读者跳过去看到不相干的内容，比断链更难发现。
   本工具只能查「越界」这一半（行号 > 文件行数）；指到错误内容的那一半查不了，
   所以正确做法仍是**别用行号**，改用 ``§号 + 逐字片段``。

**已知的合法例外**：仓库规范文档里会用示例路径讲「相对链接该怎么写」，它们是排版
示例不是真链接。这类按目标值识别并豁免——不能靠「反正 CLAUDE.md 都跳过」，那会把
CLAUDE.md 里真正的死链一起放过。

行内代码跨度（反引号内）里的内容一律不算引用。文档里引用链接语法本身时会写成
``` `[X.md](...x.md)` ```，把它当真链接扫会产生误报。
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

#: 讲解链接写法时的示例目标，不指向真实文件。
_ILLUSTRATIVE = {
    "./GUIDE.md", "./paper-a/STM.md", "../BASELINE.md", "./relative/path.md",
    "./SUMMARY.md", "./README.md",
}

_SKIP_DIRS = {".git", "runs", "__pycache__", "venv", "node_modules", "pyfcstm",
              ".omx", ".pytest_cache"}

_LINK = re.compile(r"\[([^\]\n]{1,120})\]\((\.[^)\s]+)\)")
_BLOB = re.compile(r"https://github\.com/([\w.-]+/[\w.-]+)/blob/[^/\s)]+/([^)\s#]+)")
_LINENO = re.compile(r"\[([^\]\n]{1,120})\]\((\.[^)\s]+?\.md)\)[^\n]{0,40}?第\s*(\d+)\s*[-–—]?\s*\d*\s*行")
#: 代码围栏与行内代码——其中的内容不是引用。
_FENCE = re.compile(r"^\s*(```|~~~)", re.M)
_INLINE_CODE = re.compile(r"`[^`\n]*`")


def _strip_code(text: str) -> str:
    """把代码围栏与行内代码替换成等长空白，保持字节偏移不变以便算行号。"""
    out, in_fence = [], False
    for line in text.split("\n"):
        if _FENCE.match(line):
            in_fence = not in_fence
            out.append(" " * len(line))
            continue
        out.append(" " * len(line) if in_fence
                   else _INLINE_CODE.sub(lambda m: " " * len(m.group(0)), line))
    return "\n".join(out)


def _lineno(text: str, pos: int) -> int:
    return text[:pos].count("\n") + 1


def scan(root: pathlib.Path, repo_slug: str | None) -> list[tuple[str, int, str, str]]:
    """返回 (相对路径, 行号, 类别, 说明)。"""
    bad: list[tuple[str, int, str, str]] = []
    repo_root = _find_repo_root(root)
    for md in sorted(root.rglob("*.md")):
        if any(part in _SKIP_DIRS for part in md.parts):
            continue
        try:
            raw = md.read_text(errors="replace")
        except OSError:
            continue
        text = _strip_code(raw)
        rel = str(md.relative_to(root))

        for m in _LINK.finditer(text):
            target = m.group(2)
            if target in _ILLUSTRATIVE:
                continue
            if not (md.parent / target.split("#")[0]).exists():
                bad.append((rel, _lineno(text, m.start()), "relative", target))

        if repo_slug:
            for m in _BLOB.finditer(text):
                if m.group(1) != repo_slug:
                    continue  # 指向别的仓库，无从校验
                if not (repo_root / m.group(2)).exists():
                    bad.append((rel, _lineno(text, m.start()), "blob-url", m.group(2)))

        for m in _LINENO.finditer(text):
            target = (md.parent / m.group(2)).resolve()
            if not target.exists():
                continue  # 已由 relative 这一类报过
            try:
                total = len(target.read_text(errors="replace").split("\n"))
            except OSError:
                continue
            if int(m.group(3)) > total:
                bad.append((rel, _lineno(text, m.start()), "lineno-oob",
                            f"{m.group(2)} 第 {m.group(3)} 行，但该文件只有 {total} 行"))
    return bad


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    for p in [start, *start.parents]:
        if (p / ".git").exists():
            return p
    return start


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", nargs="?", default=".", help="扫描根目录")
    ap.add_argument("--repo-slug", default="HansBug/research_ideas",
                    help="用于校验绝对 blob URL 的 owner/repo；置空则跳过该类")
    ap.add_argument("--list", action="store_true", help="逐条列出而不是按文件汇总")
    args = ap.parse_args(argv[1:])

    root = pathlib.Path(args.root).resolve()
    bad = scan(root, args.repo_slug or None)

    kinds: dict[str, int] = {}
    for _, _, kind, _ in bad:
        kinds[kind] = kinds.get(kind, 0) + 1
    detail = "，".join(f"{k} {v}" for k, v in sorted(kinds.items())) or "无"
    print(f"失效引用 {len(bad)} 条（{detail}）")

    if args.list:
        for f, ln, kind, what in bad:
            print(f"  {f}:{ln}  [{kind}] {what}")
    else:
        by_file: dict[str, int] = {}
        for f, _, _, _ in bad:
            by_file[f] = by_file.get(f, 0) + 1
        for f, n in sorted(by_file.items(), key=lambda x: -x[1])[:25]:
            print(f"  {n:3}  {f}")
        if len(by_file) > 25:
            print(f"  … 另 {len(by_file) - 25} 个文件")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
