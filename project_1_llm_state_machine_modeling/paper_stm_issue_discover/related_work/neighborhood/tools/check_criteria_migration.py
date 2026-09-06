r"""口径迁移检查器 —— 扫旧口径标志物，报哪些文件还没挂口径注。

⭐ **它服务的场景**：`issue #189` 把 paper1 的问题从「NL 对齐」改为「NL 满足性」，
于是「`hit@k` 是主指标」「19 条谓词是闭合词表」「−15.82pp 可归因于架构」这些说法
全部需要重挂。本轨已迁完（`CRITERIA_MIGRATION.md`），⛔ 而伞 PR 还有约 500 行待迁
（684 份 md / 108,509 行）。本脚本就是那份迁移检查清单的生成器。

⛔⛔ **它能判什么、不能判什么，必须先说清**：

- ⭐ **能判**：某文件有没有旧口径标志物；有的话，该文件有没有**挂口径注**
  （即含 `CRITERIA_MIGRATION.md` 或 `issues/189` 的引用）。这是纯词法判定，完美可判。
- ⛔ **不能判**：注得对不对。⭐ 一个文件可以挂了注却把映射写反 —— 那要靠 review。
- ⛔ **不能判**：某处标志物是否**口径无关**。⭐ 实测本轨 63 处 §E 命中里 62 处是
  「不利结果的写法」「无方差对照」「任务不同构」这类与我方问题定义无关的观察 ——
  ⛔ 机器分不出来，所以本脚本用**显式豁免表**（`_EXEMPT`）记录人工裁定，而不是猜。

⭐ 按仓库 `CLAUDE.md` §11 的准入边界：本脚本是**工具**不是 schema validator，
它的输出是清单与提醒，⛔ 不构成对任何产物的一票否决。

⚠️⚠️ **一个已实际踩到的计数陷阱，写在这里备查**：

用 **一次** ``awk '/^## E\./{e=1} /^## F\./{e=0} e && /标志物/' cards/*.md`` 统计时，
``e`` 这个 flag **跨文件边界不会重置** —— 于是某卡若缺 ``## F.``，后续所有文件
都被当成还在 §E 里。⭐⭐ 本轨首次统计因此得 **62**，逐文件重跑后是 **63**。
⭐ 正确写法是逐文件循环（本脚本的 `iter_section_hits` 即按文件切分）。

跑法::

    cd project_1_llm_state_machine_modeling/paper_stm_issue_discover/related_work/neighborhood
    python tools/check_criteria_migration.py .
    python tools/check_criteria_migration.py ../..            # 扫整个 paper1 工作区
    python tools/check_criteria_migration.py . --section E    # 只看卡片 §E
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

#: 旧口径标志物 —— ⭐ 每条附「新状态」，与 `CRITERIA_MIGRATION.md` §1 一一对应。
#: ⛔ 改这张表必须同步改那份文档，⭐ 否则脚本与真源会各说一套。
MARKERS: dict[str, str] = {
    r"hit@1|hit@3|hit@all": "降为分量：主指标改为按 L 分层的 hit@k + witnessed fraction",
    r"闭合词表": "降级为『常见形状库 + worked example』，不再是准入条件",
    r"19 条谓词|19 个谓词": "命题升级：从『我们的词表有依据』到『自由表达层必须能表达全部』",
    r"−15\.82|-15\.82|15\.82pp": "数字仍真，归因作废（三重混淆，不可归因于架构）",
    r"355/588|60\.4%": "同上；且从未做过 substantive / mutation-surviving 两个真空探针",
    r"台账 9[89] 条|98 条台账|99 条台账": "可能严重低估：L2 那格 6 → [31, 117]",
    r"model\.fcstm|编译产物": "被检制品改为作者源 stm0.puml，编译产物只作可执行介质",
    r"NL 覆盖性|覆盖性本身": "问题改为 NL 满足性（测试预言问题的一个实例）",
}

#: 挂了口径注的判据 —— ⭐ 文件级即可，⛔ 不要求逐行（doc 级 banner 足够）。
_ANNOTATED = re.compile(r"CRITERIA_MIGRATION\.md|issues/189|issue #189")

#: ⛔⛔ **显式豁免表：人工裁定「此处标志物口径无关」的文件。**
#: ⭐ 每条必须写理由 —— ⛔ 没理由的豁免等于把检查关掉。
#: ⚠️ key 是相对扫描根的 posix 路径；⭐ 支持 `dir/**` 前缀。
_EXEMPT: dict[str, str] = {
    "CRITERIA_MIGRATION.md": "它就是映射真源本身",
    "tools/**": "脚本里出现标志物是因为它要扫标志物",
    "search_ledger.md": "检索台账，实测 0 处标志物（列在此防回归）",
    "assets.md": "资产总表，实测 0 处",
    "pipeline_forms.md": "流水线形态对照，实测 0 处",
    # ⭐⭐ 卡片豁免的依据是一次**穷尽**审计（2026-08-14），⛔ 不是抽样：
    #   · §E「对 M1 的意义」 **63** 行 → ⛔ 与新口径直接冲突的**仅 1 行**（`_ours-v46.md`，已就地改写，
    #     ⭐ 故该卡不在本豁免内、并已单独挂注）；⭐ 其余 62 行是「不利结果的写法」10 ·
    #     「无方差 / 无 `@k` 对照」19 ·「先例计数 / 闭合对照」15 ·「任务不同构」5 · 统计与诚实度写法若干。
    #   · §E 之外 **84** 行 → ⭐ 全部是「与我们对照」的**事实陈述** 25 ·「不利结果写法」11 ·
    #     「无方差 / `@k`」6 ·「先例计数与对照表行」其余。
    # ⭐ 这两批的共同性质：**对照物变了，⛔ 但每条陈述的事实内容仍真**。
    #   例：「它不是『闭合词表 + LLM 自动选』的先例」——⭐ 新口径下该数的是
    #   「开放 `L_expr` + 合式性门」的先例，⛔ 但「本篇没有选类环节」这个事实不变。
    # ⚠️⛔ **审计中发现一个本脚本的假阳性**：某卡表格里的 `60.4%` 是**外部论文自己的数**，
    #   ⛔ 与我们的 `hit@1` 无关 —— 纯巧合同值。⭐ 按仓库 `CLAUDE.md` §3.9.7，
    #   这个方向的错（多报一个不需迁移的）是**保守**的，⛔ 不改结论；⭐ 反向那个才会。
    # ⛔ 系统性的对照物变更已挂在 `EXTRACTION_SCHEMA.md` 的「是否闭合」字段上 ——
    #   ⭐ 那是所有卡片共用的 schema，⛔ 改一处即覆盖 30 张。
    "cards/**": (
        "穷尽审计过：§E 63 行里 Type 4 仅 1 行（已单独改写并挂注），"
        "余 62 行与 §E 外 84 行均为『对照物变、事实仍真』；"
        "系统性变更已挂在 EXTRACTION_SCHEMA.md 的『是否闭合』字段"
    ),
    # ⛔⛔ **下面这批是「不得就地改写」，⭐ 与「口径无关」是两个不同的豁免理由。**
    # ⭐ 按仓库 `CLAUDE.md` §3.5.1：事前登记的**全部价值**来自「它写在看到结果之前」，
    #   ⛔ 就地改写会毁掉证据链；⭐ 代次归档同理（`CLAUDE.md` §9.5 第 6 条：
    #   代次分析是「这条规则当初为什么加」的唯一载体）。
    # ⭐ 正确处置是**在索引层加读法注**（说明该文件按旧口径写成），⛔ 不是改文件本身。
    # ⚠️ 所以这批出现在检查清单上是**误导** —— 它会指使人去改事前登记。
    # ⚠️ 用 basename 前缀而非精确名 —— ⭐ 实测仓库里有 `preregistered.md` ×9、
    #   `preregistered_actionability.md`、`preregistered_calibre.md` 共 **12** 份，
    #   ⛔ 只挂精确名会漏掉后两种。
    "preregistered*": "事前登记：价值来自『写在看到结果之前』，⛔ 就地改写会毁证据链",
    "docs/generations/**": "代次归档：是『这条规则当初为什么加』的唯一载体",
    "generations/**": "同上（另一处代次归档路径）",
    "archive/**": "已归档路线：按 §9.5 第 1 条完整保留，⛔ 不随口径变更改写",
    "reports/**": "带日期的运行报告：是当时那次运行的记录，⛔ 不是当前主张",
}


def _is_exempt(rel: str) -> str | None:
    """返回豁免理由，⭐ 不豁免则 None。

    ⚠️⛔ **`dir/**` 必须同时按前缀与「路径分量边界后的后缀」匹配。** ⭐ 理由是本脚本
    支持从任意根扫：从 `neighborhood/` 扫时卡片的 rel 是 `cards/x.md`，⛔ 而从
    `paper_stm_issue_discover/` 扫时是 `related_work/neighborhood/cards/x.md` ——
    ⛔ 只做前缀匹配会让同一份文件在两种扫法下得到**不同**结论。
    ⭐ 边界限定（`/` 之后）是为了不让 `cards/**` 误命中 `flashcards/`。
    """
    if rel in _EXEMPT:
        return _EXEMPT[rel]
    base = rel.rsplit("/", 1)[-1]
    for pat, why in _EXEMPT.items():
        if pat.endswith("*") and not pat.endswith("/**"):
            # ⭐ basename 前缀项（如 `preregistered*`）—— ⛔ 只比 basename，不比路径。
            if base.startswith(pat[:-1]):
                return why
            continue
        if not pat.endswith("/**"):
            # ⭐ 精确路径项同样允许「边界后缀」命中，⛔ 否则换根后同样会不一致。
            if rel.endswith("/" + pat):
                return why
            continue
        stem = pat[:-2]  # 形如 "cards/"
        if rel.startswith(stem) or ("/" + stem) in rel:
            return why
    return None


def scan_text(text: str) -> dict[str, int]:
    """逐标志物数**行数**（⛔ 不是出现次数）。

    ⭐ 用行数是因为出现次数会聚集在少数行上 —— ⛔ 本轨曾按次数报「53 处」，
    ⭐ 而那其实只有 27 行，读起来像 53 个独立地点。行数才是迁移工作量。
    """
    counts: dict[str, int] = {}
    lines = text.splitlines()
    for pat in MARKERS:
        rx = re.compile(pat)
        n = sum(1 for ln in lines if rx.search(ln))
        if n:
            counts[pat] = n
    return counts


def iter_section_hits(text: str, section: str) -> list[str]:
    """只取某一节内的命中行。

    ⛔⛔ **本函数按单个文件的文本调用，⭐ 这就是上面那个 awk 陷阱的修法** ——
    ⭐ 节内标志(`inside`)是局部变量，⛔ 不可能泄漏到下一个文件。
    """
    head = re.compile(rf"^## {re.escape(section)}\.")
    other = re.compile(r"^## [A-Z]\.")
    any_marker = re.compile("|".join(MARKERS))
    out: list[str] = []
    inside = False
    for ln in text.splitlines():
        if head.match(ln):
            inside = True
            continue
        if inside and other.match(ln):
            inside = False
        if inside and any_marker.search(ln):
            out.append(ln)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="扫旧口径标志物，报未挂口径注的文件")
    ap.add_argument("root", type=Path, help="扫描根目录")
    ap.add_argument("--section", help="只统计卡片某一节（如 E）内的命中")
    ap.add_argument("--quiet", action="store_true", help="只报未挂注的")
    args = ap.parse_args(argv)

    root: Path = args.root.resolve()
    if not root.is_dir():
        print(f"⛔ 不是目录: {root}", file=sys.stderr)
        return 2

    unannotated: list[tuple[str, int]] = []
    # ⭐ 通配豁免按「哪条规则」聚合，⛔ 不要每份文件复述一遍长理由 ——
    #   扫伞（684 份 md）时那会把有用输出淹掉。
    exempt_groups: dict[str, list[tuple[str, int]]] = {}
    total_files = total_lines = total_hits = 0

    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:  # ⭐ 降级，⛔ 不抛
            print(f"⚠️ 读不了 {rel}: {exc}", file=sys.stderr)
            continue

        total_files += 1
        total_lines += len(text.splitlines())

        if args.section:
            hits = iter_section_hits(text, args.section)
            if hits and not args.quiet:
                print(f"{rel}: §{args.section} 内 {len(hits)} 行")
            total_hits += len(hits)
            continue

        counts = scan_text(text)
        if not counts:
            continue
        n = sum(counts.values())
        total_hits += n

        # ⭐⭐ **挂注优先于豁免**：⛔ 若反过来，一份落在豁免通配里、但自己确实挂了注的文件
        #   （如 `cards/_ours-v46.md`）会被报成「已豁免」而不是「已挂注」—— ⭐ 那会掩盖
        #   「这一张卡是被单独改写过的」这个事实。
        if _ANNOTATED.search(text):
            if not args.quiet:
                print(f"✅ {rel}: {n} 行，已挂口径注")
            continue

        why = _is_exempt(rel)
        if why:
            exempt_groups.setdefault(why, []).append((rel, n))
            continue

        unannotated.append((rel, n))

    if exempt_groups and not args.quiet:
        for why, items in exempt_groups.items():
            lines_n = sum(n for _, n in items)
            print(f"⚪ 已豁免 {len(items)} 份 / {lines_n} 行 —— {why}")

    print(f"\n扫了 {total_files} 份 md / {total_lines} 行，旧口径 {total_hits} 行")

    if unannotated:
        print(f"\n⛔ {len(unannotated)} 份有旧口径标志物但**未挂口径注**：")
        for rel, n in sorted(unannotated, key=lambda x: -x[1]):
            print(f"   {n:4d} 行  {rel}")
        print("\n⭐ 修法：在文件顶部挂一条指向 CRITERIA_MIGRATION.md 的口径注，")
        print("   ⛔ 或把它加进 _EXEMPT 并写明为什么此处标志物口径无关。")
        return 1

    print("✅ 所有含旧口径标志物的文件都已挂注或已豁免")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
