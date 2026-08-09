"""`00x8` 先验越界 与 hold-out 已废止 是**两条互不相干**的策略。

写这个文件是因为它们被混为一谈过一次，代价是一次 360 格的误启动：`metrics_at_k.py` 报
「可报记录缺 27 条 …… 即剔除不利样本」，读的人（我）把它当成 hold-out 残留，于是把 `00x8`
并回网格。两条策略的差别是硬的：

| | 说的是什么 | 依据 |
| :-- | :-- | :-- |
| 不设 hold-out | **不许**因样本表现或参与规则编写而改分母 | METHOD_PROVENANCE_POLICY.md |
| `00x8` 越界 | 有些规约本来就不是本方法要建模的对象 | NL_SCOPE_RULE.md |

把前者套到后者上，就会得出「排除 00x8 = 剔除不利样本」这个错误结论。事实相反：被排除集里
`0018` 的 `hit@1` = 66.7%，高于全量均值 53.9% —— 若目的是挑数字，不会把它一起排掉。

所以工具必须**自己把这两件事说清楚**，散文防不住复发。
"""

from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import metrics_at_k as M  # noqa: E402
import nl_scope_filter as N  # noqa: E402


def test_the_denominator_excludes_out_of_scope_records() -> None:
    """分母 = 台账全部 − NL 越界。99 而不是 126。"""

    assert len(M.OUT_OF_SCOPE) == 27
    assert len(M.REPORTABLE) == 99
    assert len(M.REPORTABLE) + len(M.OUT_OF_SCOPE) == len(M._all_record_ids())
    assert not set(M.REPORTABLE) & set(M.OUT_OF_SCOPE)


def test_out_of_scope_is_exactly_the_00x8_family() -> None:
    """越界集由 NL 判定导出，不是手写的 id 清单 —— 手写清单会和 nl_scope_filter 漂移。"""

    assert N.excluded_pairs() == ["0008", "0018", "0028", "0038", "0048", "0058"]
    pairs = {record[4:8] for record in M.OUT_OF_SCOPE}
    assert pairs == set(N.excluded_pairs())


def test_a_missing_in_scope_record_is_still_refused() -> None:
    """废止 hold-out 不等于放松分母：范围内记录少一条仍须拒算。"""

    verdicts = {r: {"claude": [1], "gpt": [1]} for r in M.REPORTABLE[1:]}
    problems = M.validate(verdicts, {}, rounds=1, require_direction=False)
    assert any("范围内记录缺" in p for p in problems), problems


def test_the_refusal_message_says_it_is_not_about_00x8() -> None:
    """报错必须自己撇清 —— 上一次就是这句话没撇清才导致误启动。"""

    verdicts = {r: {"claude": [1], "gpt": [1]} for r in M.REPORTABLE[1:]}
    text = " ".join(M.validate(verdicts, {}, rounds=1, require_direction=False))
    assert "00x8" in text
    assert "NL_SCOPE_RULE.md" in text


def test_an_out_of_scope_record_in_the_table_is_refused_too() -> None:
    """镜像检查：越界记录被混进判定表，说明网格改错了，必须拒算。

    没有这一条，把 `00x8` 并回网格跑出来的结果会被静默接受 —— 那正是上次发生的事。
    """

    verdicts = {r: {"claude": [1], "gpt": [1]} for r in M.REPORTABLE}
    verdicts[M.OUT_OF_SCOPE[0]] = {"claude": [1], "gpt": [1]}
    problems = M.validate(verdicts, {}, rounds=1, require_direction=False)
    assert any("NL 越界记录" in p and "网格被改错" in p for p in problems), problems
