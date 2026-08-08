"""分段脚本必须只读产出，不读 prompt。

这份测试存在的理由是一次已经发生的错误：分段的第一版对 splitter 的整条 LLM-call 记录做
`"predicate": "X"` 正则，而记录里的 `system_prompt` 本身含 8 处该形状（谓词词表的 worked
example 就是那个 JSON 写法）。于是「只在 prompt 里出现过的谓词」被算成「写进了需求集」，
① 报成 91（真值 135）、② 报成 71（真值 24），并据此得出「损失不集中在任何一环」这个**错误的**
中心论断，写进了 PR comment 与 issue #177。

所以下面锁的不是分段的具体数字，而是**它的数据来源**：只能是 `parsed_output.requirements`。
一个能被输入污染的度量工具，会把错误带进它支撑的每一个结论。
"""

from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import loss_stages  # noqa: E402


def _cell(tmp_path: pathlib.Path, *, parsed: list[dict], system_prompt: str) -> pathlib.Path:
    cell = tmp_path / "run1" / "0000-claude"
    record = cell / "records" / "L000-000001-requirement-splitter-llm-call-completed"
    record.mkdir(parents=True)
    (record / "record.json").write_text(
        json.dumps(
            {
                "role": "requirement_splitter",
                "system_prompt": system_prompt,
                "raw_response": json.dumps({"requirements": parsed}),
                "parsed_output": {"requirements": parsed},
            },
            ensure_ascii=False,
        )
    )
    return cell


def test_prompt_text_is_not_counted_as_output(tmp_path: pathlib.Path) -> None:
    """system_prompt 里的谓词名不得进入统计——这正是原缺陷。"""

    cell = _cell(
        tmp_path,
        parsed=[{"predicate": "occupancy_after"}],
        # 谓词词表的 worked example 在 prompt 里就是这个形状。
        system_prompt=(
            'predicate_bindings examples: {"predicate": "terminates", ...} '
            'and {"predicate": "edge_declared", ...} and {"predicate": "invariant", ...}'
        ),
    )
    written = loss_stages.requirement_predicates(cell)
    assert written == {"occupancy_after"}
    for injected in ("terminates", "edge_declared", "invariant"):
        assert injected not in written, injected


def test_raw_response_is_not_counted_either(tmp_path: pathlib.Path) -> None:
    """`raw_response` 与 `parsed_output` 通常一致，但前者是未校验文本，不作真源。"""

    cell = tmp_path / "run1" / "0000-claude"
    record = cell / "records" / "L000-000001-requirement-splitter-llm-call-completed"
    record.mkdir(parents=True)
    (record / "record.json").write_text(
        json.dumps(
            {
                "raw_response": '{"requirements": [{"predicate": "reaches"}]}',
                "parsed_output": {"requirements": [{"predicate": "containment"}]},
            }
        )
    )
    assert loss_stages.requirement_predicates(cell) == {"containment"}


def test_every_revision_counts(tmp_path: pathlib.Path) -> None:
    """一条需求在某一版被写出、后被评审删掉，仍算「写过」——那是 ② 不是 ①。"""

    cell = tmp_path / "run1" / "0000-claude"
    for index, predicate in enumerate(("stays_in", "occupancy_after"), start=1):
        record = (
            cell / "records" / f"L000-00000{index}-requirement-splitter-llm-call-completed"
        )
        record.mkdir(parents=True)
        (record / "record.json").write_text(
            json.dumps({"parsed_output": {"requirements": [{"predicate": predicate}]}})
        )
    assert loss_stages.requirement_predicates(cell) == {"stays_in", "occupancy_after"}


def test_a_malformed_record_is_skipped_not_fatal(tmp_path: pathlib.Path) -> None:
    """分段跑在几百格上，一份坏记录不该让整次统计失败。"""

    cell = tmp_path / "run1" / "0000-claude"
    bad = cell / "records" / "L000-000001-requirement-splitter-llm-call-completed"
    bad.mkdir(parents=True)
    (bad / "record.json").write_text("{not json")
    good = cell / "records" / "L000-000002-requirement-splitter-llm-call-completed"
    good.mkdir(parents=True)
    (good / "record.json").write_text(
        json.dumps({"parsed_output": {"requirements": [{"predicate": "cardinality"}]}})
    )
    assert loss_stages.requirement_predicates(cell) == {"cardinality"}


def test_stages_are_mutually_exclusive_and_named() -> None:
    """六段 + 命中，名字集合固定；分段结果不得出现表外的段名。"""

    assert len(set(loss_stages.STAGES)) == 7
    assert loss_stages.STAGES[0] == "命中"
    assert loss_stages.STAGES[-1] == "⑥ 台账无 primary"
