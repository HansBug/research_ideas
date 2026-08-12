#!/usr/bin/env python3
"""边界门双判据：对 `state_machine_types/SUMMARY.md` 的 669 行主表逐行判界内 / 界外。

⛔ 本脚本存在的理由是一次真实的可复现性失败。`pool_audit.md` 初版给出
「剔除 242 / 669 = 36.2%，界内池 427」这组数，却**只用散文描述**界外关键词
（「UPPAAL 系、PRISM/MRMC、CPN/GSPN、mCRL2/BIP、混成」），没给词表也没给脚本。
独立复核者按那段散文反推，得到的是 261 / 669 = 39.0%、界内池 408，且
`仅emoji命中` 与 `两者同时` 两项无论怎么收窄词表都到不了初版报的 18 / 148。

⭐ 教训：一个依赖词表的计数，**词表就是它的一部分**。把百分比写进文档而把词表留在
脑子里，等于交出一个不可复核的数——而这恰恰是初版自己用来批评上一版「692 行里
212 行」那个数的同一条罪状。

判据（任一为真即剔除）：
  ① 「形式主义」列命中 OUT_KEYWORDS 之一
  ② 「主类」列 emoji ∈ OUT_EMOJI

⚠️ 判据 ② 是**整行**剔除，与 #179 §4.0.2「同一篇论文可以部分可用」有原理性冲突：
被 ② 剔掉的行没有回捞路径。实测暴露面很小（见 --audit 输出），但冲突本身要记着。
"""
from __future__ import annotations
import argparse, pathlib, re, sys
from collections import Counter

#: 界外形式主义关键词。⚠️ 改动此表会改变所有下游百分比，改前先跑 --audit 看差异。
OUT_KEYWORDS = (
    "timed", "TIOA", "UPPAAL", "clock", "real-time", "RT-LOTOS",
    "Petri", "CPN", "GSPN", "PNML", "TimeNET", "GreatSPN", "Woflan", "TAPAAL", "Tina",
    "CSP", "CCS", "mCRL2", "LOTOS", "process algebra", "pi-calculus", "BIP", "FDR",
    "stochastic", "probabilistic", "PRISM", "MRMC", "VESTA", "Ymer", "Markov", "PTA", "CSL",
    "hybrid", "continuous", "orthogonal",
)
#: 界外主类 emoji：时间/时钟自动机、混成/随机、Petri 网。
OUT_EMOJI = ("⏱️", "🌊", "🕸️")

_ROW = re.compile(r"^\|")


def load_rows(summary: pathlib.Path) -> list[dict[str, str]]:
    """解析主表（表头以 `| # | 主类 |` 开头的那张）。⛔ 不含 emoji 口径小表。"""
    lines = summary.read_text(encoding="utf-8").split("\n")
    head_i = next(
        i for i, l in enumerate(lines)
        if l.startswith("|") and "主类" in l and "#" in l.split("|")[1]
    )
    cols = [c.strip() for c in lines[head_i].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for l in lines[head_i + 2:]:
        if not _ROW.match(l):
            break
        cells = [c.strip() for c in l.strip("|").split("|")]
        if len(cells) != len(cols):
            continue
        rows.append(dict(zip(cols, cells)))
    return rows


def judge(row: dict[str, str]) -> tuple[bool, bool]:
    """返回 (形式主义列命中, 主类 emoji 命中)。"""
    f = row.get("形式主义", "")
    by_kw = any(k.lower() in f.lower() for k in OUT_KEYWORDS)
    by_emoji = any(e in row.get("主类", "") for e in OUT_EMOJI)
    return by_kw, by_emoji


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("summary", nargs="?", default="project_1_llm_state_machine_modeling/state_machine_types/SUMMARY.md")
    ap.add_argument("--audit", action="store_true", help="额外打印判据②的暴露面与年份分布")
    a = ap.parse_args(argv[1:])

    rows = load_rows(pathlib.Path(a.summary))
    only_f = only_e = both = 0
    inside: list[dict[str, str]] = []
    for r in rows:
        by_kw, by_emoji = judge(r)
        if by_kw and by_emoji:
            both += 1
        elif by_kw:
            only_f += 1
        elif by_emoji:
            only_e += 1
        else:
            inside.append(r)
    cut = only_f + only_e + both
    print(f"主表行数            {len(rows)}")
    print(f"仅形式主义列命中     {only_f}")
    print(f"仅主类 emoji 命中    {only_e}")
    print(f"两者同时命中         {both}")
    print(f"合计剔除            {cut} / {len(rows)} = {cut / len(rows):.1%}")
    print(f"界内候选池          {len(inside)}")

    def year_of(r: dict[str, str]) -> int | None:
        m = re.search(r"(19|20)\d{2}", r.get("年份", ""))
        return int(m.group(0)) if m else None

    y = [year_of(r) for r in inside]
    print(f"  其中 2022 年起     {sum(1 for v in y if v and v >= 2022)}")

    if a.audit:
        print("\n--- 判据②的暴露面（⚠️ 整行剔除与「部分可用」的冲突） ---")
        risk = [
            r for r in rows
            if judge(r)[1] and not judge(r)[0]
            and re.search(r"state machine|statechart|automat", r.get("形式主义", ""), re.I)
        ]
        print(f"仅被 emoji 剔除、且形式主义列含离散状态机族词的行数: {len(risk)}")
        for r in risk:
            print(f"  · {r.get('标题', '')[:70]}  [{r.get('形式主义', '')[:50]}]")
        print("\n--- 剔除集主类分布 ---")
        print(dict(Counter(r.get("主类", "") for r in rows if any(judge(r)))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
