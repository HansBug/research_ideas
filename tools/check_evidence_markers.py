#!/usr/bin/env python3
"""校验依据强度标记的形态：``【…】`` 内必须恰好是六档之一。

`story/README.md` §2 定了六档依据强度标记（导师原话 / 导师原话背书 / v46 实测 /
仓库裁定 / AI 建议·待确认 / 待定），并声明「全目录通用」。但实测里 ``【】`` 长出了
**约 60 种变体**，其中 82 处落在六档体系的作用域内：``【用户明确裁定 2026-08-11】``、
``【v46 实测 + 仓库裁定】``、``【我方提出 · 导师未反对】``、``【2026-08-11 盘点】`` ……

⛔ 这些变体单看每一个都有理由，合起来的后果是**读者无法再从形态上判断依据强度**。
逐节读的人看到七八种 ``【】``，只能猜哪个是正式档。而约束它们的声明写在文件抬头，
离使用处七十多行远——⚠️ **靠远处的声明约束近处的形态，已经失效过一次**：
``【用户明确…】`` 被误用成引语标记 8 处，使「引用了多少条用户原话」这个数虚报近一倍。

**判据**：作用域内的每个 ``【…】``，其内容必须**逐字**等于六档之一。

**不属六档的依据标注改用 ``〔…〕``** —— 形态上就不可能被误认。两类合法：
``〔用户明确裁定 yyyy-mm-dd〕`` / ``〔用户明确澄清 yyyy-mm-dd〕``、
``〔我方提出 · 导师未反对〕``。

⚠️ 作用域是**声明使用六档的那些文件**，不是全仓：`claim_evidence_map.md` 自带一套
八档强度表（``【推论】`` 等），`state_machine_types/` 有 ``【控制系统状态机】`` 一类
领域标签——那些是别的标注体系，⛔ 本工具不管。
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

#: `story/README.md` §2 的六档，逐字。
SIX = (
    "导师原话",
    "导师原话背书",
    "v46 实测",
    "仓库裁定",
    "AI 建议·待确认",
    "待定",
)

#: 声明使用六档的文件（相对论文工作区根）。⚠️ 新增文件若使用六档须登记到这里,
#: 否则它的违规不会被查到——这是本工具已知的边界,不是遗漏。
SCOPE = (
    "story/README.md",
    "story/paper_story.md",
    "story/paper_outline.md",
    "story/blueprint_proposal.md",
    "story/model_scope.md",
    "story/terminology_policy.md",
    "PENDING_DECISIONS.md",
    "TODO.md",
    "GUIDE.md",
    "STATUS.md",
    "SUMMARY.md",
)

_MARK = re.compile(r"【([^】]*)】")

#: 六档紧跟日期或补注 —— 最常见的违规形态,单独报以给出精确改法。
_DATED = re.compile(r"^(%s)[\s，,：:]" % "|".join(map(re.escape, SIX)))
#: 组合档,如 `【v46 实测 + 仓库裁定】`。实测出现过两种相反顺序。
_COMBO = re.compile(r"\+")


def classify(inner: str) -> tuple[str, str] | None:
    """返回 (违规类型, 建议改法);合规则返回 None。"""
    if inner in SIX:
        return None
    # ⛔ 组合档必须先判。`_DATED` 的 `[\s，,：:]` 会吃掉 `+` 前的空格,于是
    # `v46 实测 + 仓库裁定` 被它先命中,报成「六档带后缀」、建议改法给出
    # `【v46 实测】（+ 仓库裁定）` —— 那个改法本身仍然违规,且丢掉了「顺序固定」
    # 这条要点(组合档实测出现过两种相反顺序)。顺序颠倒过来即修。
    if _COMBO.search(inner):
        parts = [p.strip() for p in inner.split("+")]
        if all(p in SIX for p in parts):
            parts.sort(key=SIX.index)
            return "组合档", "".join(f"【{p}】" for p in parts)
        return "组合档(含非六档)", "拆开,非六档部分改用〔〕"
    if _DATED.match(inner):
        head = next(s for s in SIX if inner.startswith(s))
        rest = inner[len(head):].lstrip(" ，,：:")
        return "六档带后缀", f"【{head}】（{rest}）"
    if not inner.strip():
        return "空标记", "删除"
    return "非六档", f"〔{inner}〕"


def scan(root: pathlib.Path) -> list[tuple[str, int, str, str, str]]:
    """返回 (相对路径, 行号, 原标记内容, 违规类型, 建议改法)。"""
    bad: list[tuple[str, int, str, str, str]] = []
    for rel in SCOPE:
        f = root / rel
        if not f.is_file():
            continue
        try:
            lines = f.read_text(errors="replace").split("\n")
        except OSError:
            continue
        fence = None
        for lineno, line in enumerate(lines, 1):
            # 代码块内的 `【】` 多是在讲规则本身,不算违规。
            m = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
            if m:
                fence = None if fence else m.group(1)[0] * 3
                continue
            if fence:
                continue
            for mm in _MARK.finditer(line):
                # 行内代码里的同样是在举例,跳过。
                before = line[: mm.start()]
                if before.count("`") % 2 == 1:
                    continue
                verdict = classify(mm.group(1))
                if verdict:
                    bad.append((rel, lineno, mm.group(1), *verdict))
    return bad


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "root",
        nargs="?",
        default="project_1_llm_state_machine_modeling/paper_stm_issue_discover",
        help="论文工作区根",
    )
    ap.add_argument("--list", action="store_true", help="逐条列出")
    args = ap.parse_args(argv[1:])

    bad = scan(pathlib.Path(args.root).resolve())
    print(f"形态违规 {len(bad)} 处")
    if args.list:
        for rel, ln, inner, kind, fix in bad:
            print(f"  {rel}:{ln}  [{kind}] 【{inner}】\n      → {fix}")
    else:
        by: dict[str, int] = {}
        for _, _, _, kind, _ in bad:
            by[kind] = by.get(kind, 0) + 1
        for kind, n in sorted(by.items(), key=lambda x: -x[1]):
            print(f"  {n:3}  {kind}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
