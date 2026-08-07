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

import pytest

from paper_stm_feedback_loop.assertions.runtime import EvalEnvironment

PROJECT = pathlib.Path(__file__).resolve().parents[4]   # project_1_llm_state_machine_modeling
LEDGER = (PROJECT / "eval" / "discover_matrix" / "manual_review"
          / "expected_issue_set.json")
SEEDS = pathlib.Path(__file__).resolve().parents[3] / "selected_seed_examples"

#: 逐条钉住：(记录 id, pair, source, trigger, target, 台账记录的期望值)。
#:
#: 只列 `role == "primary"` 且谓词为 `occupancy_after` 的 —— 那是**被度量的**那条断言。
#: `negative_control` 与 `recovered_unverified` 的 `measured_by_batch` 是 `None`，无期望值可钉。
OCCUPANCY_PRIMARIES = (
    ("EIS-0000-01", "0000", "HumanDrivingMode", "Power_Off", "FinalState", False),
    ("EIS-0035-02", "0035", "DoorOpen", "Door_Closed", "DoorShut", False),
)


def _api(pair: str):
    model = SEEDS / f"llms_emp_feedback_final_{pair}" / "model.fcstm"
    if not model.is_file():
        pytest.skip(f"no seed model for {pair}")
    return EvalEnvironment(model_text=model.read_text()).predicates


@pytest.mark.parametrize(
    "record_id,pair,source,trigger,target,expected", OCCUPANCY_PRIMARIES
)
def test_occupancy_primary_still_measures_what_the_ledger_recorded(
    record_id: str, pair: str, source: str, trigger: str, target: str, expected: bool
) -> None:
    """台账的 `measured_by_batch` 必须在**每一个合理 horizon** 上仍然成立。

    钉 1..5 而不是单个值：台账的表达式未必写明 `within_cycles`，而修复正是关于 horizon 的。
    若某个 horizon 上翻了，说明台账那条的期望值依赖被改掉的语义。
    """

    api = _api(pair)
    prefix = f"llms_emp_feedback_final_{pair}."
    values = {}
    for cycles in (1, 2, 3, 4, 5):
        try:
            values[cycles] = api.occupancy_after(
                source=prefix + source, trigger=prefix + trigger,
                target=prefix + target, within_cycles=cycles,
            )
        except Exception as exc:      # 拒答也是一种变化 —— 台账记的是 True/False
            values[cycles] = type(exc).__name__

    assert all(v is expected for v in values.values()), (
        f"{record_id} 的台账期望值是 {expected}，但当前实现给出 {values}。\n"
        "台账的 `measured_by_batch` 是用谓词实测出来的 —— 谓词语义一改它就可能过期。\n"
        "若它过期而未被发现，所有覆盖率数字都建立在一把变了的尺子上，且**没有任何东西会报错**。\n"
        "处置：先判定台账那条是否仍成立，再决定是改台账还是回退谓词；两者都要在报告里声明"
        "「本代次起台账期望值已变，与前代不可直接比较」。"
    )


def test_the_pinned_list_still_matches_the_ledger() -> None:
    """本文件钉的清单必须与台账实际内容一致 —— 否则台账新增条目时这条测试会静默失效。

    这是「测试自身的覆盖面也会漂」的防护：若台账后来又加了一条 `occupancy_after` primary 而没加进
    `OCCUPANCY_PRIMARIES`，上面的参数化测试仍然全绿，但新条目未被保护。
    """

    if not LEDGER.is_file():
        pytest.skip("no ledger on disk")
    records = json.loads(LEDGER.read_text()).get("records") or []
    grid = {"0000", "0006", "0018", "0029", "0032",
            "0035", "0038", "0043", "0047", "0048", "0050"}
    found = set()
    for record in records:
        if str(record.get("pair", ""))[-4:] not in grid:
            continue
        for assertion in record.get("assertions") or []:
            if assertion.get("role") != "primary":
                continue
            text = str(assertion.get("expression") or "")
            if "occupancy_after" not in text:
                continue
            if assertion.get("measured_by_batch") in (None, "None"):
                continue
            found.add(str(record["id"]))

    pinned = {row[0] for row in OCCUPANCY_PRIMARIES}
    assert found == pinned, (
        f"台账里有 `measured_by_batch` 的 occupancy_after primary 是 {sorted(found)}，"
        f"而本文件钉的是 {sorted(pinned)}。差集未被保护 —— 请同步 `OCCUPANCY_PRIMARIES`。"
    )
