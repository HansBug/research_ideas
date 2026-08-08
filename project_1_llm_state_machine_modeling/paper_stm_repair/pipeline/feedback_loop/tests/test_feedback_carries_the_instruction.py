"""评审反馈必须带上「要改成什么」，隔离必须留下「是哪道门」。

两条性质合在一份文件里，因为它们是同一个毛病的两面：**上游手里已经有的结构化信息，在传给
下游时被丢掉了**，于是下游只能猜。

- `required_change` 是两个 review schema 的必填字段（`Field(min_length=1)`），而 `nodes.py`
  的五处反馈构造点都只转发 `f.message`。全仓库对该字段**零读取点**；抽样 184 条长度 ≥25 的
  `required_change`，在同格后续 prompt 里逐字命中 0 条。评审被强制写出来的东西，一半没发出去。
- 需求层的三道 step gate 会隔离需求。v37 实测 861 份快照里 167 份发生隔离、覆盖 66 个 cell，
  但在 19,893 个 run 文件里 grep 十道门的消息签名，**七道命中 0 个文件** —— 「哪道门摘的」
  无法从运行记录恢复，于是门贡献度审计与「该门从未触发」的退役判断都失去证据基础。

两条都锁**性质**不锁措辞：前者只要求指令半边到达，后者只要求门名可被机械提取。
"""

from __future__ import annotations

from paper_stm_feedback_loop.discover.nodes import _review_findings


class _Finding:
    def __init__(self, message: str, required_change: str) -> None:
        self.message = message
        self.required_change = required_change


def test_the_instruction_half_reaches_the_producer() -> None:
    findings = _review_findings(
        [_Finding("REQ-004 binds an element the model does not declare", "bind Sys.ModeA instead")]
    )
    assert len(findings) == 1
    assert "REQ-004 binds an element the model does not declare" in findings[0]
    assert "bind Sys.ModeA instead" in findings[0], "required_change 未到达生产者"


def test_every_finding_keeps_both_halves() -> None:
    findings = _review_findings(
        [_Finding("first problem", "first fix"), _Finding("second problem", "second fix")]
    )
    assert len(findings) == 2
    for rendered, (problem, fix) in zip(
        findings, [("first problem", "first fix"), ("second problem", "second fix")], strict=True
    ):
        assert problem in rendered and fix in rendered


def test_a_blank_required_change_does_not_leave_a_dangling_arrow() -> None:
    """schema 要求非空，但渲染器不得依赖它——空值时只出 message，不出空指令。"""

    assert _review_findings([_Finding("just a message", "")]) == ("just a message",)
    assert _review_findings([_Finding("just a message", "   ")]) == ("just a message",)


def test_no_construction_site_forwards_message_alone() -> None:
    """五处构造点必须走同一个渲染器。

    锁的是「单一归属地」：只要还有一处直接写 `f.message`，`required_change` 就会在那条路径上
    继续丢失，而丢失是静默的。
    """

    import inspect

    from paper_stm_feedback_loop.discover import nodes

    source = inspect.getsource(nodes)
    assert "findings=tuple(f.message for f in output.findings)" not in source
    assert source.count("findings=_review_findings(output.findings)") == 5


def test_quarantine_is_attributed_to_a_named_gate() -> None:
    """隔离事件的 findings 必须以 `[<gate>]` 起头，使「哪道门触发过」成为一次 grep。"""

    import inspect
    import re

    from paper_stm_feedback_loop.discover import nodes

    source = inspect.getsource(nodes)
    assert 'f"[{name}] {finding}"' in source, "门名未被写进隔离 finding"
    # 隔离事件必须真的进入需求侧 ledger，而不是只算出来不写盘。
    quarantine = source[source.index("if quarantined_requirements:") :]
    assert 'event="artifact_quarantined"' in quarantine
    assert "findings=gate_attribution" in quarantine
    assert "item_ids=quarantined_requirements" in quarantine
    # 归因必须来自逐门配对，而不是事后从一锅 finding 里猜。
    assert re.search(r"attributed_findings:\s*tuple\[tuple\[str, str\], \.\.\.\]", source)
