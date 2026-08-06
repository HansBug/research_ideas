"""提名一个名字时必须点名看过的在位候选 —— 加载信息，不改动作。

v22 的判定发现同一个动作（把 NL 的名词绑成 `state_declared` 的路径）既产出真命中也产出噪声，
而两者**从产出上分不开**：

    命中   `auto_final`（NL 逐字点名，模型里无任何对应物）
    命中   `choice3`（NL 点名，模型自造 `fork2` 顶替了它的位置）
    命中   `Join1`（NL 点名，模型只声明了 `Join2`）
    噪声   `Idle`（NL 点名，而模型声明的是 `IdleState` —— 同一个东西换了拼写）
    噪声   `Inactive`（NL 通篇没有这个概念）

下游看到的都是一条 False。区别只在**提名时作者判断了什么**，而那个判断此后不可恢复。

所以这条约束要求把判断写下来，**不改变任何断言**：路径不变、谓词不变、绑定不变、返回值不变。
凡是压制这个动作的方案都不可采纳 —— 台账自己就用 `state_declared(NL 名)` 编码上面三条命中，
按编辑距离压制会把 `choice3`（与 `choice1` 距离 1）和 `Join1`（与 `Join2` 距离 1）一起杀掉。
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover import prompts  # noqa: E402

MARKER = "incumbent considered:"


def test_the_splitter_asks_for_the_incumbents_by_name() -> None:
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    assert MARKER in text
    # 必须给出「一个都没有」的写法，否则作者在真空场景下无从下笔，只能省略。
    assert f"{MARKER} none" in text


def test_it_is_stated_as_additive_and_not_as_a_hedge() -> None:
    """这条约束的全部安全性依赖于它不改动作 —— 所以 prompt 必须自己说清。

    若被读成「可以用它来软化主张」，它就变成了 `limitations` 已知的失败形态：写进限制、
    什么都不断言，而 `limitations` 永远不会返回 False。
    """
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    window = text[text.index(MARKER) : text.index(MARKER) + 900]
    assert "keep the proposed path" in window
    assert "never comes back False" in window or "not a hedge" in window


def test_it_covers_every_proposal_not_only_the_doubtful_ones() -> None:
    """只在「拿不准时」记录，等于让最需要区分的那些跳过 —— 作者拿得准的恰恰是它判错的时候。"""
    # prompt 是折行的，所以按词比对而不是按连续子串 —— 断言写成 "every proposed name" 会因为
    # 一个换行而假红，而那与它要守的性质无关。
    text = " ".join(prompts.REQUIREMENT_SPLITTER_PROMPT.split())
    marker = " ".join(MARKER.split())
    window = text[max(0, text.index(marker) - 600) : text.index(marker) + 900]
    assert "for every proposed name" in window
    assert "confident" in window


def test_the_two_findings_it_separates_are_spelled_out() -> None:
    """约束若不说清它在分辨什么，会退化成一句无人认真填的样板。"""
    window = prompts.REQUIREMENT_SPLITTER_PROMPT
    start = window.index("Whenever you propose a name")
    block = window[start : start + 900]
    assert "named the thing differently" in block
    assert "absent" in block
    # 必须说明为什么此刻不做就永远做不了。
    assert "unrecoverable" in block or "one False either way" in block
