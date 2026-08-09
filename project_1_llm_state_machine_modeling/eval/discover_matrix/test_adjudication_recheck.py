"""横向一致性检查必须能抓住 v41 那两处真实判错，且不得越权改判。

下面的 fixture 是从 v41 实跑里逐字取的：台账 primary 取自 `EIS-0030-02` / `EIS-0040-01` /
`EIS-0040-03`，issue 标题取自各格实际发布内容。这三条当时判出了互相矛盾的结果，
而这正是工具存在的理由——所以它必须在这份 fixture 上报警。

`test_prose_overlap_would_have_missed_these` 锁的是设计选择本身：这个工具**不能**基于台账散文
做词元重合。第一版就是那么写的，在这两处真实判错上得分接近 0，因为「断电」与 `Power_Off`、
「自动驾驶」与 `Autonomous` 是语义对应而非字面对应。
"""

from __future__ import annotations

import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import adjudication_recheck as R  # noqa: E402

P = "llms_emp_feedback_final_"

LEDGER = {
    "EIS-0030-02": {
        "statement": "自动驾驶激活期间无法断电，NL 第5句的断电义务只覆盖了一半作用域。",
        "primary_expression": (
            f'event_consumed(source="{P}0030.Autonomous.Navigating", '
            f'trigger="{P}0030.Power_Off")'
        ),
    },
    "EIS-0040-01": {
        "statement": "自动驾驶激活期间无法断电，NL 第5句断电义务只覆盖一半作用域。",
        "primary_expression": (
            f'event_consumed(source="{P}0040.Autonomous.AutoInitial", '
            f'trigger="{P}0040.Power_Off")'
        ),
    },
    "EIS-0040-03": {
        "statement": "复合状态的初始迁移带触发事件，进入自动驾驶后无任何子状态处于激活。",
        "primary_expression": (
            f'occupancy_after(source="{P}0040.HumanDriving", '
            f'trigger="{P}0040.front_distance_10", target="{P}0040.Autonomous.AutoInitial")'
        ),
    },
    "EIS-0014-03": {
        "statement": "'Entry: Emergency Stop' 在 PlantUML 里不是动作语法，被降级成虚假子状态。",
        "primary_expression": (
            f"not state_declared(state='{P}0014.EmergencyStopping.Entry', kind='any')"
        ),
    },
}

TITLES = {
    "run2/0030-claude": ["Power_Off 在 Autonomous 运行上下文中不会终止运行"],
    "run1/0040-claude": ["Power_Off 在 Autonomous 中未使系统终止"],
    "run1/0040-gpt": ["front_distance_10 触发后未在一个周期内处于 Autonomous"],
    "run3/0040-gpt": ["front_distance_10 未在运行时使系统进入 Autonomous"],
    "run1/0014-claude": ["EmergencyStopping 未声明 entry 阶段动作（Emergency Stop）"],
    "run2/0020-gpt": ["模型未声明规范要求的 Power_On 事件"],
}


@pytest.fixture(autouse=True)
def _stub_titles(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(R, "published_titles", lambda _gen, cell: TITLES.get(cell, []))


def _entry(record_id: str, cell: str, hit: bool, decided_by: str = "human") -> dict:
    return {"record_id": record_id, "cell": cell, "hit": hit, "decided_by": decided_by}


def test_the_real_power_off_inconsistency_is_flagged() -> None:
    """v41 判错之一：同一句「Power_Off 在 Autonomous 不终止」，一处命中一处未命中。

    两条台账绑的 source 不同（`Navigating` vs `AutoInitial`），但两处 issue 都只指认了
    `Autonomous` + `Power_Off`——在已发布文本这一层是同一句话，理应同判。
    """

    audit = [
        _entry("EIS-0030-02", "run2/0030-claude", hit=True),
        _entry("EIS-0040-01", "run1/0040-claude", hit=False),
    ]
    flagged = R.inconsistencies("matrix-v41", audit, LEDGER)
    assert len(flagged) == 1
    assert flagged[0]["miss_side"]["record_id"] == "EIS-0040-01"
    assert flagged[0]["hit_side"]["record_id"] == "EIS-0030-02"


def test_the_real_occupancy_inconsistency_is_flagged() -> None:
    """判错之二：同一台账条目、同一句 issue，run1 判命中而 run3 判未命中。"""

    audit = [
        _entry("EIS-0040-03", "run1/0040-gpt", hit=True),
        _entry("EIS-0040-03", "run3/0040-gpt", hit=False),
    ]
    flagged = R.inconsistencies("matrix-v41", audit, LEDGER)
    assert len(flagged) == 1
    assert flagged[0]["miss_side"]["cell"] == "run3/0040-gpt"


def test_prose_overlap_would_have_missed_these() -> None:
    """锁住设计选择：散文比对在这两处上给不出信号，所以工具必须比对 primary 的元素名。"""

    statement = LEDGER["EIS-0040-01"]["statement"]
    title = TITLES["run1/0040-claude"][0]
    shared = set(statement) & set(title)
    assert not (shared - set(" ，。的了是在与和或未无不有被从到对中下上个条")), shared

    elements = R.primary_elements(LEDGER["EIS-0040-01"]["primary_expression"])
    score, _ = R.coverage(elements, title)
    assert score >= R.DEFAULT_THRESHOLD


def test_different_predicates_are_not_flagged() -> None:
    """谓词不同就不是同一形态——否则工作清单会淹掉真正的不一致。"""

    audit = [
        _entry("EIS-0040-01", "run1/0040-claude", hit=True),
        _entry("EIS-0014-03", "run1/0014-claude", hit=False),
    ]
    assert R.inconsistencies("matrix-v41", audit, LEDGER) == []


def test_tier_a_positions_are_never_flagged() -> None:
    """A 层是确定性判据，不存在人的口径漂移；把它拉进来只会制造噪声。"""

    audit = [
        _entry("EIS-0030-02", "run2/0030-claude", hit=True, decided_by="tier_a"),
        _entry("EIS-0040-01", "run1/0040-claude", hit=False, decided_by="tier_a"),
    ]
    assert R.inconsistencies("matrix-v41", audit, LEDGER) == []


def test_a_cell_that_published_nothing_relevant_is_not_flagged() -> None:
    """该格根本没报这个缺陷时判未命中是对的，不该进人工复核清单。"""

    audit = [_entry("EIS-0040-01", "run2/0020-gpt", hit=False)]
    assert R.worklist("matrix-v41", audit, LEDGER, R.DEFAULT_THRESHOLD) == []


def test_worklist_surfaces_a_miss_whose_cell_published_a_matching_issue() -> None:
    audit = [_entry("EIS-0040-01", "run1/0040-claude", hit=False)]
    items = R.worklist("matrix-v41", audit, LEDGER, R.DEFAULT_THRESHOLD)
    assert [item["record_id"] for item in items] == ["EIS-0040-01"]
    assert items[0]["matched_issue"] == "Power_Off 在 Autonomous 中未使系统终止"


def test_worklist_ignores_hits() -> None:
    """已判命中的位不需要人再读；工作清单只服务于「可能低估」这一个方向。"""

    audit = [_entry("EIS-0040-01", "run1/0040-claude", hit=True)]
    assert R.worklist("matrix-v41", audit, LEDGER, R.DEFAULT_THRESHOLD) == []


def test_the_tool_reports_locations_not_verdicts() -> None:
    """硬边界：输出里不得出现任何形似改判的字段。机械代理只能定位，不能裁定。"""

    audit = [
        _entry("EIS-0030-02", "run2/0030-claude", hit=True),
        _entry("EIS-0040-01", "run1/0040-claude", hit=False),
    ]
    for pair in R.inconsistencies("matrix-v41", audit, LEDGER):
        for side in pair.values():
            assert set(side) == {
                "record_id",
                "cell",
                "hit",
                "predicate",
                "statement",
                "matched_issue",
                "score",
            }


def test_the_corpus_prefix_is_stripped() -> None:
    """前缀出现在每个标识符上，留着会让所有位都「高度重合」。"""

    elements = R.primary_elements(LEDGER["EIS-0030-02"]["primary_expression"])
    assert not any("llms_emp" in part for part in elements)
    assert {"autonomous", "navigating", "power", "off"} <= elements
