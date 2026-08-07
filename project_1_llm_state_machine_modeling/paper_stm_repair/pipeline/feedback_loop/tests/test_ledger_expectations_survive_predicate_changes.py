"""台账里 `measured_by_batch` 的期望值必须与当前谓词实现一致。

## 为什么需要这条测试

台账（`eval/discover_matrix/manual_review/expected_issue_set.json`）是判定的**参照物**，我下意识把它当成
固定的。但它的 `measured_by_batch` 字段是**用谓词实测出来的** —— 谓词语义一改，它就可能过期。

2026-08-07 修 `_occupies` 的窗口起点时，我查过「改动是否正确」（双侧测试）、「改动是否有效果」（噪声底），
却没查过**「改动是否动了尺子」**。事后手工复算：两条 `occupancy_after` primary 在 `within_cycles = 1..5`
上仍全为 `False`，台账有效。

**但若它们翻了，v24 的所有覆盖率数字都会建立在一把变了的尺子上，而没有任何东西会报错** —— 与同日另外
三个静默型问题（`failed: 8` 把在飞的格报成失败、`sample_id` 静默配对旧标注、代码版本反推偏差）同类：
都不崩溃，都产出看起来正常的数字。

所以这条检查必须是测试，不能靠我想起来。
"""

from __future__ import annotations

import json
import pathlib
import re

import pytest

from paper_stm_feedback_loop.assertions.runtime import EvalEnvironment

PROJECT = pathlib.Path(__file__).resolve().parents[4]   # project_1_llm_state_machine_modeling
LEDGER = (PROJECT / "eval" / "discover_matrix" / "manual_review"
          / "expected_issue_set.json")
SEEDS = pathlib.Path(__file__).resolve().parents[3] / "selected_seed_examples"

_GRID = ("0000", "0006", "0018", "0029", "0032",
         "0035", "0038", "0043", "0047", "0048", "0050")
_CALL = re.compile(
    r"occupancy_after\(\s*source\s*=\s*['\"]([^'\"]+)['\"]\s*,\s*"
    r"trigger\s*=\s*['\"]([^'\"]+)['\"]\s*,\s*"
    r"target\s*=\s*['\"]([^'\"]+)['\"]"
)


def _cases() -> list[tuple[str, str, str, str, bool]]:
    """从台账**读出**被度量的 `occupancy_after` primary，不硬编码。

    ## 为什么从台账读而不是钉一份清单

    首版硬编码了 (记录, pair, source, trigger, target, 期望值)，并另加一条测试查「钉的清单是否与台账
    一致」—— 即用一条测试去守护一份**重复**。

    pre-push 钩子拦下了首版（它点名了若干 pair）。而正确的处置不是绕过检查，是消掉重复：从台账读则
    **没有重复可漂**，那条守护测试也就不需要了。

    ⚠️ 副作用是覆盖面随台账变化 —— 若台账某天不再有任何被度量的 `occupancy_after` primary，本测试会
    静默空过。所以下面有 `assert cases` 护栏（同 `test_occupancy_horizon_monotone.py` 的 `probes >= 1`）。
    """

    if not LEDGER.is_file():
        return []
    out = []
    for record in json.loads(LEDGER.read_text()).get("records") or []:
        pair = str(record.get("pair", ""))[-4:]
        if pair not in _GRID:
            continue
        for assertion in record.get("assertions") or []:
            if assertion.get("role") != "primary":
                continue
            measured = assertion.get("measured_by_batch")
            if measured in (None, "None"):
                continue
            match = _CALL.search(str(assertion.get("expression") or ""))
            if not match:
                continue
            source, trigger, target = match.groups()
            out.append((str(record["id"]), source, trigger, target,
                        str(measured).strip().lower() == "true"))
    return out


def _api_for(qualified: str):
    """从全限定名反查种子模型 —— 名字自带 pair，不需要单独传。"""

    root = qualified.split(".", 1)[0]
    model = SEEDS / root / "model.fcstm"
    if not model.is_file():
        pytest.skip(f"no seed model for {root}")
    return EvalEnvironment(model_text=model.read_text()).predicates


def test_occupancy_primaries_still_measure_what_the_ledger_recorded() -> None:
    """台账的 `measured_by_batch` 必须在**每一个合理 horizon** 上仍然成立。

    钉 1..5 而不是单个值：台账表达式未必写明 `within_cycles`，而修复正是关于 horizon 的。
    拒答也算变化 —— 台账记的是 True/False。
    """

    cases = _cases()
    assert cases, (
        "台账里没有任何被度量的 `occupancy_after` primary —— 本测试空过。"
        "空过与通过不可区分，所以这是错误而不是通过。"
    )

    drifted = []
    for record_id, source, trigger, target, expected in cases:
        api = _api_for(source)
        values = {}
        for cycles in (1, 2, 3, 4, 5):
            try:
                values[cycles] = api.occupancy_after(
                    source=source, trigger=trigger,
                    target=target, within_cycles=cycles,
                )
            except Exception as exc:
                values[cycles] = type(exc).__name__
        if not all(v is expected for v in values.values()):
            drifted.append((record_id, expected, values))

    assert not drifted, (
        f"{len(drifted)} 条台账期望值与当前实现不符：{drifted}\n"
        "台账的 `measured_by_batch` 是用谓词实测出来的 —— 谓词语义一改它就可能过期。\n"
        "若它过期而未被发现，所有覆盖率数字都建立在一把变了的尺子上，且**没有任何东西会报错**。\n"
        "处置：先判定台账那条是否仍成立，再决定是改台账还是回退谓词；两者都要在报告里声明"
        "「本代次起台账期望值已变，与前代不可直接比较」。"
    )
