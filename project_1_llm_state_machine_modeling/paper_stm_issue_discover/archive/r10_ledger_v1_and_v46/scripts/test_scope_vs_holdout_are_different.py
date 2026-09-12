"""`00x8` 先验越界 与 hold-out 已废止 是**两条互不相干**的策略。

写这个文件是因为它们被混为一谈过一次，代价是一次 360 格的误启动：`metrics_at_k.py` 报
「可报记录缺 27 条 …… 即剔除不利样本」，读的人（我）把它当成 hold-out 残留，于是把 `00x8`
并回网格。两条策略的差别是硬的：

| | 说的是什么 | 依据 |
| :-- | :-- | :-- |
| 不设 hold-out | **不许**因样本表现或参与规则编写而改分母 | docs/protocol/method_provenance_policy.md |
| `00x8` 越界 | 有些规约本来就不是本方法要建模的对象 | docs/protocol/nl_scope_rule.md |

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
    """分母 = 台账全部 − NL 越界 − 逐条边界裁定。98 而不是 126。

    27 条 NL 越界（`00x8`）+ 1 条 `boundary_ruling: out_of_scope`（`EIS-0043-02`，
    独立裁定判为表示层产物、`boundary_effect` 明写「从能力分母剔除」）。
    """

    assert len(M.OUT_OF_SCOPE) == 28
    assert len(M.REPORTABLE) == 98
    assert len(M.REPORTABLE) + len(M.OUT_OF_SCOPE) == len(M._all_record_ids())
    assert not set(M.REPORTABLE) & set(M.OUT_OF_SCOPE)


def test_out_of_scope_is_exactly_the_00x8_family_plus_ruled_records() -> None:
    """越界集由 NL 判定 + 台账裁定共同导出，不是手写 id 清单（手写会与两个来源漂移）。"""

    assert N.excluded_pairs() == ["0008", "0018", "0028", "0038", "0048", "0058"]
    nl_side = {r for r in M.OUT_OF_SCOPE if r[4:8] in set(N.excluded_pairs())}
    assert len(nl_side) == 27
    ruled = set(M.OUT_OF_SCOPE) - nl_side
    assert ruled == {"EIS-0043-02"}, ruled


def test_a_boundary_ruling_in_the_ledger_is_actually_honoured() -> None:
    """裁定写在数据里而工具不读，等于没裁定。

    `EIS-0043-02` 的 `boundary_effect` 明写「从能力分母剔除」，而 `in_scope` 字段对
    126 条全为 True（它记的不是这件事）。工具原先只按 pair 扣，于是这条虽被裁定却仍
    进了分母 —— v46 首份报告的 hit@1 因此偏高 0.4pp。
    """

    import json
    import pathlib

    payload = json.loads(pathlib.Path(M.LEDGER).read_text())
    ruled = [r for r in payload["records"] if r.get("boundary_ruling") == "out_of_scope"]
    assert ruled, "台账里应存在被裁定越界的记录，否则本测试测不到东西"
    for record in ruled:
        assert record["id"] not in set(M.REPORTABLE), (
            f'{record["id"]} 被裁定 out_of_scope 却仍在分母内'
        )
        # 该记录的 in_scope 仍为 True —— 正是不能依赖它的原因。
        assert record.get("in_scope") is True


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
    assert "docs/protocol/nl_scope_rule.md" in text


def test_an_out_of_scope_record_in_the_table_is_refused_too() -> None:
    """镜像检查：越界记录被混进判定表，说明网格改错了，必须拒算。

    没有这一条，把 `00x8` 并回网格跑出来的结果会被静默接受 —— 那正是上次发生的事。
    """

    verdicts = {r: {"claude": [1], "gpt": [1]} for r in M.REPORTABLE}
    verdicts[M.OUT_OF_SCOPE[0]] = {"claude": [1], "gpt": [1]}
    problems = M.validate(verdicts, {}, rounds=1, require_direction=False)
    assert any("NL 越界记录" in p and "网格被改错" in p for p in problems), problems
