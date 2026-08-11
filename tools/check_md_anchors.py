#!/usr/bin/env python3
"""校验「§号 + 逐字片段」式跨文件引用——片段是否还能在目标文件里逐字找到。

仓库纪律禁止用「第 N 行」做跨文件引用（行号会被任何重排静默打掉），要求改用
``§号 + 逐字片段``。但那条纪律换来的是**另一种**静默失效：正文一改写，片段就找不到了，
而**链接仍然通、§号仍然存在**，所以 ``check_md_links`` 一条都报不出来。

实测代价：一次「把 Related Work 第 5 轴由候选转正」的改写，重写了 ``paper_story.md`` §10，
同一个 commit 里两份预案的 **10 处锚点**随之失配，其中两处让两份文件对同一件事给出
**相反指令**（一处说「正式纳入第五条轴」，另一处说「⛔ 不再作为候选陈列」）。
当时的验证结论是「失效引用净增 0」——那句话字面属实，因为用的尺子量不到这一类。

**判据**：一行里如果既出现指向某个 ``.md`` 的链接、又出现 ``「…」`` 包起来的片段，
那些片段就应当能在该目标文件里逐字找到。找不到即失配。

**归一化**：比对前去掉 Markdown 强调标记（``**`` ``*`` `` ` ``）与全部空白。
理由是加粗边界最容易漂移——同一句话，引用方把 ``**`` 收在句中、目标文件收在句末，
字面不等但**内容完全一致**，报出来只会淹没真问题。
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

#: 一行内指向某个 .md 的相对链接。
_LINK = re.compile(r"\]\((\.{1,2}/[^)\s#]+\.md)")
#: 直角引号包起来的片段。⚠️ 允许内部出现强调标记，故不排除 * 与 `。
_FRAG = re.compile(r"「([^「」\n]{%d,})」" % 6)
#: 省略号——含它的片段本就不是逐字引用，跳过而不是误报。
_ELLIPSIS = re.compile(r"[…]|\.{3,}")

#: 链接与片段之间允许的最大字符距离——超出就不是同一个锚点了。
_SPAN = 120

_SKIP_DIRS = {".git", "runs", "__pycache__", "venv", "node_modules", "pyfcstm",
              ".omx", ".pytest_cache", "archive"}


def normalize(text: str) -> str:
    """去掉强调标记与空白——加粗边界漂移不算失配。"""
    return re.sub(r"\s+", "", re.sub(r"[*`]", "", text))


def scan(root: pathlib.Path) -> list[tuple[str, int, str, str]]:
    """返回 (引用方相对路径, 行号, 目标文件, 找不到的片段)。

    ⛔ **按位置邻近匹配，不按「同一行」匹配。** 一行里完全可以既有指向 A 的链接、
    又有与 A 无关的引述——实测 ``paper_story.md`` 有一行链接指向 ``README.md``
    而同行的 ``「…」`` 引的是 talks 里的导师原话。按「同行」判会过报到 121 处，
    把真问题淹掉。⚠️ 一个报 121 次狼的工具比没有工具更糟。

    真正的锚点形态是三者**顺序相邻**：``](路径) … §号 … 「片段」``。
    这里要求片段起点落在链接之后 ``_SPAN`` 字符内，且其间出现过 ``§``。
    """
    bad: list[tuple[str, int, str, str]] = []
    for md in sorted(root.rglob("*.md")):
        if any(part in _SKIP_DIRS for part in md.parts):
            continue
        try:
            lines = md.read_text(errors="replace").split("\n")
        except OSError:
            continue
        cache: dict[pathlib.Path, str] = {}
        for lineno, line in enumerate(lines, 1):
            for lm in _LINK.finditer(line):
                target = (md.parent / lm.group(1)).resolve()
                if not target.is_file() or target == md.resolve():
                    continue                    # 断链归 check_md_links 管
                window = line[lm.end(): lm.end() + _SPAN]
                # 片段必须在链接之后，且链接与片段之间出现过 §号。
                for fm in _FRAG.finditer(window):
                    if "§" not in window[: fm.start()]:
                        continue
                    frag = fm.group(1)
                    if _ELLIPSIS.search(frag):
                        continue                # 带省略号的本就不是逐字引用
                    if target not in cache:
                        try:
                            cache[target] = normalize(target.read_text(errors="replace"))
                        except OSError:
                            cache[target] = ""
                    if normalize(frag) not in cache[target]:
                        bad.append((str(md.relative_to(root)), lineno,
                                    lm.group(1), frag))
    return bad


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", nargs="?", default=".", help="扫描根目录")
    ap.add_argument("--list", action="store_true", help="逐条列出而不是按文件汇总")
    args = ap.parse_args(argv[1:])

    root = pathlib.Path(args.root).resolve()
    bad = scan(root)
    print(f"失配锚点 {len(bad)} 处")

    if args.list:
        for f, ln, rel, frag in bad:
            shown = frag if len(frag) <= 60 else frag[:57] + "…"
            print(f"  {f}:{ln}  → {rel}\n      「{shown}」")
    else:
        by_file: dict[str, int] = {}
        for f, _, _, _ in bad:
            by_file[f] = by_file.get(f, 0) + 1
        for f, n in sorted(by_file.items(), key=lambda x: -x[1]):
            print(f"  {n:3}  {f}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
