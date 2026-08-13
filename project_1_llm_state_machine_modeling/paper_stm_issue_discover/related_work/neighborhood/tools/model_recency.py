"""按「论文里用的 LLM 是哪一代」给 30 张卡排序，并算出距我们主臂的代际差。

## 为什么需要这个工具

`design_evidence.md` 的四档分级（① 受控对照 / ② 端到端 / ③ 仅理由 / ④ 单点）只回答了
「对照是否受控」，**完全没回答「用的是哪一代模型」**。这两件事独立：

- 一篇 2024 年用 `GPT-4` 的 ① 档受控对照，方法学上无懈可击，但它测的能力区间
  在 2026-08 已经不存在；
- 一篇 2026 年用 `GPT-5.1` 的 ③ 档设计理由没有数字，但它描述的是当代模型的行为。

对我们（主臂 `gpt-5.5` 2026-04-23 / `claude-opus-4-7` 2026-04-16）而言，
**后者的参考价值可能高于前者**。这个轴此前一次都没量过。

## 最长优先匹配：这不是优化，是正确性要求

⛔⛔ **模型名之间存在前缀包含关系，朴素匹配会把新模型记成旧模型。**

具体地：`GPT-4` 是 `GPT-4o` / `GPT-4o-mini` / `GPT-4.1` / `GPT-4.1-mini` 的前缀。
若按任意顺序匹配并取首个命中，`GPT-4o-mini`（2024-07-18）会被记成 `GPT-4`（2023-03），
**凭空多算 16 个月的代际差**；`GPT-4.1`（2025-04-14）会被记成 2023-03，**多算 25 个月**。

同理 `Claude 3` 是 `Claude 3.5 Sonnet` / `Claude 3.7 Sonnet` 的前缀，
`DeepSeek-V3` 是 `DeepSeek-V3.1` / `DeepSeek-V3.2-Exp` 的前缀，
`Llama 3` 是 `Llama 3.1` / `Llama 3.3` 的前缀，
`Qwen2.5` 是 `Qwen2.5-1M` / `Qwen2.5-Coder` 的前缀。

⭐ 所以 `_PATTERNS` **按模式串长度降序排序后**才做匹配，并且每个模式两端加
「非模型名字符」边界（⛔ 不能用 `\b`：`\b` 认为 `.` 与 `-` 是边界，
于是 `GPT-4\b` 会在 `GPT-4.1` 里命中 `GPT-4` 后面那个 `.`）。

## ⚠️ 已知的假阳性来源（本工具**不**自动排除，只做标记）

1. **参考文献里的模型名**。`etfa2025` 全文只有一处 `GPT`，在参考文献
   「ChatGPT for PLC/DCS」的题名里；`synthesizing-protocol-specs` 引的 (23) 是
   `OpenAI, GPT-4 technical report, arXiv:2303.08774`。这两处都不是「实验用了该模型」。
2. **卡片作者自己的评述**。卡里会写「⛔ 与 PAT-Agent 的 o3-mini / claude-3-7 一代不同」，
   那是在评论**别的**论文。
3. **对照组 / baseline 的模型**。有些卡列了被评测的 18 个模型，那不是「主结果模型」。
4. ⛔⛔ **卡与卡之间互相引用对方的模型。** 实测三例：`internetware2025` 与 `models2024`
   各命中一次 `GPT-5.1`，⛔ 但那是卡作者在**引用 SoSyM 那篇**做代际对照
   （「⭐ 因为 SoSyM 那篇用 GPT-5.1 仍然观察到同类的语义盲区」）。
   ⭐ 两篇自己的主结果分别是 `GPT-4o-2024-11-20`（2024-11）与 `GPT-3.5` 生成 + `GPT-4` 检测（2023-03）。
   ⛔ **按最新命中会把它们从 C/D 档洗成 A 档 —— 与 `_OURS_KEYS` 那个坑同向。**
5. ⚠️ **一篇论文内部可能跨代。** `sosym2026` 的 Table 7 全部 69 条来自 GPT-3.5/GPT-4，
   ⭐ 而 §5.2.2 那次补充对照用 GPT-5.1。⭐⭐ **这两部分必须分开评**：
   前者的绝对数字要打折，⭐ 后者（「GPT-5.1 仍看不见两跳路径」）**反而是全库最耐久的发现之一** ——
   ⭐ 在当代模型上仍成立的失败模式，比在旧模型上观察到同一模式**更有说服力**。

⭐ 因此本工具的输出是**候选集与命中计数**，⛔ 不是判定。判定必须回卡与原文。
⭐ 这与 `CLAUDE.md` §11 是同一条纪律：**词法判据不得冒充语义判断** ——
「卡里出现了 GPT-4 这个串」与「该论文主结果用 GPT-4」是两件事。

## 用法

    python -m tools.model_recency            # 全表
    python -m tools.model_recency --tsv      # 制表符分隔，便于贴进 Markdown
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

_CARDS = Path(__file__).resolve().parent.parent / "cards"

#: 我们自己的主臂。两个模型取**较早**的那个当参照点，使代际差不被高估。
_OURS = {"gpt-5.5": date(2026, 4, 23), "claude-opus-4-7": date(2026, 4, 16)}
_REF = min(_OURS.values())

#: 模型名 → 发布年月。来源：仓库 `llm_model_landscape/0[2-8]-*.md`（官方来源已核）。
#: ⚠️ 只到月的条目按该月 1 日计，故代际差有 ±1 月的量化噪声；
#: ⛔ 这不影响分档（档宽 6 个月以上）。
#:
#: ⛔⛔ **本表只收 landscape 里查得到的型号。** ⚠️ 首版硬编码了 `gpt-5.2 = (2025,12)`，
#: ⛔ 而 `llm_model_landscape/02-openai-models.md` 里**根本没有这个型号**
#: （⭐ 该表从 `gpt-5.3-codex` 2026-02-05 直跳 `gpt-5.1` 2025-11-13）。
#: ⛔ 即 docstring 声称的来源与实际内容不符 —— ⭐ **这类「工具自称有出处、实际是猜的」
#: 比缺数据危险得多**，⛔ 因为下游会把它当已核事实引用。
#: ⭐ 处置：从表里移除，改由 `_UNPRICED` 显式报「已知型号但 landscape 无条目」。
#: ⭐⭐ **正确的修法是回写 landscape，⛔ 不是反过来相信工具。**

#: ⭐ 卡里出现过、但 `llm_model_landscape` 无条目的型号。⛔ 不猜日期，只报缺口。
_NOT_IN_LANDSCAPE: dict[str, str] = {
    "gpt-5.2": "zenodo-simulink 卡的 C=2 臂用它；landscape 待回写",
}
_RELEASE: dict[str, tuple[int, int]] = {
    # OpenAI
    "gpt-5.5": (2026, 4), "gpt-5.4-mini": (2026, 3), "gpt-5.4": (2026, 3),
    "gpt-5.3-codex": (2026, 2), "gpt-5.1": (2025, 11),
    "gpt-5-mini": (2025, 8), "gpt-5-nano": (2025, 8), "gpt-5": (2025, 8),
    "o4-mini": (2025, 4), "o3-mini": (2025, 1), "o3": (2025, 4),
    "gpt-4.1-mini": (2025, 4), "gpt-4.1-nano": (2025, 4), "gpt-4.1": (2025, 4),
    "gpt-4o-mini": (2024, 7), "gpt-4o": (2024, 5),
    "gpt-4-turbo": (2023, 3), "gpt-4": (2023, 3), "gpt-3.5-turbo": (2023, 3),
    "gpt-3.5": (2023, 3), "gpt-oss-20b": (2025, 8), "gpt-oss-120b": (2025, 8),
    # Anthropic
    "claude-opus-4-8": (2026, 5), "claude-opus-4-7": (2026, 4),
    "claude-sonnet-4-6": (2026, 2), "claude-opus-4-6": (2026, 2),
    "claude-opus-4-5": (2025, 11), "claude-haiku-4-5": (2025, 10),
    "claude-sonnet-4-5": (2025, 9), "claude-4-opus": (2025, 5),
    "claude-4-sonnet": (2025, 5), "claude-sonnet-4": (2025, 5),
    "claude-3-7-sonnet": (2025, 2), "claude-3-5-sonnet": (2024, 10),
    "claude-3-5-haiku": (2024, 10), "claude-3-opus": (2024, 3),
    "claude-3-sonnet": (2024, 3), "claude-3-haiku": (2024, 3),
    # Google
    "gemini-3-5": (2026, 5), "gemini-3-flash": (2025, 12), "gemini-3-pro": (2025, 11),
    "gemini-2-5-flash": (2025, 6), "gemini-2-5-pro": (2025, 6),
    "gemini-2-0-flash": (2025, 2), "gemini-1-5-pro": (2024, 5),
    "gemini-1-5-flash": (2024, 5), "gemini-1-0-pro": (2024, 2), "gemini-pro": (2024, 2),
    # DeepSeek
    "deepseek-v4": (2026, 4), "deepseek-v3-2": (2025, 9), "deepseek-v3-1": (2025, 8),
    "deepseek-r1-0528": (2025, 5), "deepseek-v3-0324": (2025, 3),
    "deepseek-r1": (2025, 1), "deepseek-v3": (2024, 12),
    # Meta
    "llama-4": (2025, 4), "llama-3-3": (2024, 12), "llama-3-2": (2024, 9),
    "llama-3-1": (2024, 7), "llama-3": (2024, 4),
    # Alibaba
    "qwen3-7": (2026, 6), "qwen3-6": (2026, 4), "qwen3-5": (2026, 2),
    "qwen3-coder": (2025, 7), "qwen3": (2025, 4),
    "qwen2-5-coder": (2024, 9), "qwen2-5": (2024, 9),
    # xAI
    "grok-4-20": (2026, 3), "grok-4": (2025, 11), "grok-3": (2025, 4),
}

#: 卡里的写法 → `_RELEASE` 的键。⭐ 一个模型有多种写法（空格 / 连字符 / 点 / 大小写），
#: ⛔ 逐一列出比写通用正则安全：通用正则会把 `Claude 3.5` 和 `Claude 3` 混起来。
_ALIASES: dict[str, str] = {
    "gpt-5.5": "gpt-5.5", "gpt 5.5": "gpt-5.5",
    "gpt-5.4": "gpt-5.4", "gpt-5.2": "gpt-5.2",
    "gpt-5.1": "gpt-5.1", "gpt 5.1": "gpt-5.1",
    # ⛔ `gpt-5.2` 保留别名以便**报出缺口**，⛔ 但它不在 `_RELEASE` 里，故不参与分档
    "gpt-5.2": "gpt-5.2",
    "gpt-5-mini": "gpt-5-mini", "gpt-5-nano": "gpt-5-nano",
    "gpt-5": "gpt-5", "gpt 5": "gpt-5",
    "o4-mini": "o4-mini", "o4 mini": "o4-mini",
    "o3-mini": "o3-mini", "o3 mini": "o3-mini",
    "gpt-4.1-mini": "gpt-4.1-mini", "gpt-4.1 mini": "gpt-4.1-mini",
    "gpt-4.1": "gpt-4.1",
    "gpt-4o-mini": "gpt-4o-mini", "gpt-4o mini": "gpt-4o-mini",
    "gpt-4o": "gpt-4o",
    "gpt-4-turbo": "gpt-4-turbo", "gpt-4 turbo": "gpt-4-turbo",
    "gpt-4": "gpt-4", "gpt 4": "gpt-4",
    "gpt-3.5-turbo": "gpt-3.5-turbo", "gpt-3.5": "gpt-3.5", "gpt 3.5": "gpt-3.5",
    "gpt-oss-20b": "gpt-oss-20b", "gpt-oss-120b": "gpt-oss-120b",
    "claude-opus-4-7": "claude-opus-4-7", "claude opus 4.7": "claude-opus-4-7",
    "claude-opus-4-5": "claude-opus-4-5", "claude opus 4.5": "claude-opus-4-5",
    "claude-sonnet-4-6": "claude-sonnet-4-6", "claude sonnet 4.6": "claude-sonnet-4-6",
    "claude-4.5-sonnet": "claude-sonnet-4-5", "claude-4-5-sonnet": "claude-sonnet-4-5",
    "claude sonnet 4.5": "claude-sonnet-4-5",
    "claude-4.5-haiku": "claude-haiku-4-5", "claude haiku 4.5": "claude-haiku-4-5",
    "claude sonnet 4": "claude-sonnet-4", "claude-sonnet-4": "claude-sonnet-4",
    "claude 4 opus": "claude-4-opus", "claude opus 4": "claude-4-opus",
    "claude-3-7-sonnet": "claude-3-7-sonnet", "claude 3.7 sonnet": "claude-3-7-sonnet",
    "claude-3.7-sonnet": "claude-3-7-sonnet", "claude-3-7": "claude-3-7-sonnet",
    "claude 3.5 sonnet": "claude-3-5-sonnet", "claude-3.5-sonnet": "claude-3-5-sonnet",
    "claude 3 haiku": "claude-3-haiku", "claude-3-haiku": "claude-3-haiku",
    "gemini-3-pro": "gemini-3-pro", "gemini 3 pro": "gemini-3-pro",
    "gemini-2.5-pro": "gemini-2-5-pro", "gemini 2.5 pro": "gemini-2-5-pro",
    "gemini-2.5-flash": "gemini-2-5-flash",
    "gemini-1.5-pro": "gemini-1-5-pro", "gemini 1.5 pro": "gemini-1-5-pro",
    "gemini-pro": "gemini-pro", "gemini pro": "gemini-pro",
    "deepseek-v3.1": "deepseek-v3-1", "deepseek v3.1": "deepseek-v3-1",
    "deepseek-r1-0528": "deepseek-r1-0528",
    "deepseek-r1": "deepseek-r1", "deepseek r1": "deepseek-r1",
    "deepseek-v3": "deepseek-v3", "deepseek v3": "deepseek-v3",
    "llama4": "llama-4", "llama 4": "llama-4", "llama-4": "llama-4",
    "llama-3.3": "llama-3-3", "llama3.3": "llama-3-3",
    "llama-3.1": "llama-3-1", "llama3.1": "llama-3-1",
    "qwen3": "qwen3", "qwen-3": "qwen3",
    "qwen2.5-coder": "qwen2-5-coder", "qwen2.5": "qwen2-5",
    "grok-4-fast": "grok-4", "grok-4": "grok-4",
}

#: ⛔⛔ **边界不能用 `\b`。** `\b` 把 `.` 和 `-` 当作单词边界，于是 `gpt-4\b`
#: 在 `gpt-4.1` 里会命中（`4` 与 `.` 之间就是一个 `\b`），把 2025-04 记成 2023-03。
#: ⭐ 改成显式的「前后不得紧跟模型名可能包含的字符」。
_LEFT = r"(?<![A-Za-z0-9.\-])"
_RIGHT = r"(?![A-Za-z0-9.\-])"

#: ⭐ 按模式串长度降序 —— 见模块 docstring「最长优先匹配」一节。
_PATTERNS: list[tuple[str, str, re.Pattern[str]]] = [
    (alias, key, re.compile(_LEFT + re.escape(alias).replace(r"\ ", r"[\s\-]") + _RIGHT, re.I))
    for alias, key in sorted(_ALIASES.items(), key=lambda kv: -len(kv[0]))
]


def _months_behind(key: str) -> int:
    y, m = _RELEASE[key]
    return (_REF.year - y) * 12 + (_REF.month - m)


def _tier(months: int) -> str:
    if months <= 6:
        return "A 同代"
    if months <= 16:
        return "B 近一代"
    if months <= 28:
        return "C 隔代"
    return "D 两代以上"


#: ⛔⛔ **必须把我方主臂的两个型号从「最新命中」里剔除。**
#: ⚠️ 首版没剔，结果 **30 张卡里 16 张被判「A 同代」**，⛔ 其中 **12 张**的唯一依据是
#: 卡里出现了 `gpt-5.5` / `claude-opus-4-7` —— ⭐ 而那是**每张卡的「与我们对比」那一节**
#: 在提我们自己的模型，⛔ 不是该论文用了它们。
#: ⭐ 典型：`llm-guided-predicate-discovery` 主结果是 `gpt-3.5-turbo`（2023-03，落后 37 个月），
#: ⛔ 却因为卡里提了一次我们的型号而被判成同代 —— ⛔⛔ **这个方向的错误最危险，
#: 因为它把旧证据洗成新证据，正是本次重评要防的那件事。**
_OURS_KEYS = frozenset(_OURS)


def scan(text: str, *, drop_ours: bool = True) -> dict[str, int]:
    """返回 {模型键: 命中次数}。最长优先：命中后把该片段挖空，防止子串重复计数。

    `drop_ours` 默认剔除我方主臂型号 —— 见上方注释。
    """
    counts: dict[str, int] = {}
    buf = text
    missing: dict[str, int] = {}
    for _alias, key, pat in _PATTERNS:
        hits = pat.findall(buf)
        if hits:
            if key in _NOT_IN_LANDSCAPE:
                missing[key] = missing.get(key, 0) + len(hits)
                buf = pat.sub("  ", buf)
                continue
            counts[key] = counts.get(key, 0) + len(hits)
            buf = pat.sub("  ", buf)  # 挖空，使 `gpt-4` 不再命中 `gpt-4o` 的残留
    if drop_ours:
        counts = {k: v for k, v in counts.items() if k not in _OURS_KEYS}
    if missing:
        counts["__no_landscape_entry__"] = sum(missing.values())
    return counts


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tsv", action="store_true", help="制表符分隔输出")
    args = ap.parse_args(argv)

    rows = []
    for path in sorted(_CARDS.glob("*.md")):
        counts = scan(path.read_text(encoding="utf-8"))
        if not counts:
            rows.append((path.stem, "—", "", "", "无命中"))
            continue
        # ⭐ 「最新命中」用于分档：一篇论文若报了多个模型，它至少接触过最新那个。
        # ⚠️ 这**高估**了代际新度（主结果可能用的是较旧的那个），⛔ 故必须回卡核。
        gap = counts.pop("__no_landscape_entry__", 0)
        if not counts:
            rows.append((path.stem, "⛔ 仅无 landscape 条目的型号", "", "缺口", f"gpt-5.2×{gap}"))
            continue
        newest = min(counts, key=_months_behind)
        m = _months_behind(newest)
        rows.append((
            path.stem,
            f"{newest} ({_RELEASE[newest][0]}-{_RELEASE[newest][1]:02d})",
            f"{m:>3d}",
            _tier(m),
            " · ".join(f"{k}×{v}" for k, v in sorted(counts.items(), key=lambda kv: _months_behind(kv[0])))
            + (f"  ⛔ ＋gpt-5.2×{gap}（landscape 无条目）" if gap else ""),
        ))

    rows.sort(key=lambda r: (r[2] == "", r[2]))
    sep = "\t" if args.tsv else "  "
    if not args.tsv:
        print(f"参照点 = {_REF}（主臂较早者）；今天 2026-08\n")
        print(f"{'卡':44s}{sep}{'最新命中模型':26s}{sep}{'月差':>4s}{sep}{'档':10s}{sep}全部命中")
        print("-" * 150)
    for r in rows:
        print(f"{r[0]:44s}{sep}{r[1]:26s}{sep}{r[2]:>4s}{sep}{r[3]:10s}{sep}{r[4]}")

    print()
    tally: dict[str, int] = {}
    for r in rows:
        tally[r[3]] = tally.get(r[3], 0) + 1
    print("分档计数：" + " · ".join(f"{k} {v}" for k, v in sorted(tally.items())))
    print("\n⚠️ 「最新命中」按卡内出现过的最新模型分档，这是**上界**：主结果可能用更旧的那个。")
    print("⚠️ 参考文献题名、卡作者对别篇的评述、被评测的 baseline 列表都会命中 —— 判定必须回卡与原文。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
