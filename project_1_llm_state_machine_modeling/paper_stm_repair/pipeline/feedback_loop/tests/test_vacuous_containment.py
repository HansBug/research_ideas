"""A containment requirement whose parent is read off the model checks nothing.

`containment(parent=P, child=P.X)` cannot come back False: a declared path's own prefix *is*
its parent, so the answer follows from how the two strings were spelled. Measured over the
corpus, 567 of 567 calls in that shape return True; over one generation's three rounds, the
nested spelling was True 28 times and False never, while the cross-level spelling was False 25
times and True never.

The tempting fix -- refusing the shape inside the predicate -- is wrong, and trying it is what
established where the rule belongs. A direct child's path is *always* its parent's path plus
one segment, so a predicate-level refusal leaves `containment` unable to return True at all,
and four existing behaviour tests say so immediately. The shape is not the defect.

The defect is where `parent` came from. Bound to what the *sentence* says, the check is
ordinary: True when the model agrees, False when it buries the element somewhere else, and
that False is the finding. Bound to the declared path's own prefix, it asks "is this element
where the model put it" and answers yes. Both look identical at the call site -- the same two
strings in the same relation -- and differ only in provenance, which is visible at the
requirement stage and nowhere else.

So the rule lives with the other requirement-stage gates and reads `source_context.nl_parent`:
the level the specification puts the element at, written down before the model's own prefix is
consulted. Where the two agree there is no obligation to check; where they disagree, that is
the requirement.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover import capability  # noqa: E402


class _Req:
    """The subset of a Requirement the gate reads."""

    def __init__(self, bindings: dict, nl_parent: object = "__absent__", rid: str = "REQ-001"):
        self.requirement_id = rid
        self.predicate = "containment"
        self.predicate_bindings = bindings
        self.limitations: tuple[str, ...] = ()
        self.source_context = (
            {} if nl_parent == "__absent__" else {"nl_parent": nl_parent}
        )


def _nested(nl_parent: object = "__absent__") -> _Req:
    return _Req({"parent": "Sys.Outer", "child": "Sys.Outer.Inner"}, nl_parent)


def test_a_parent_equal_to_the_childs_own_prefix_is_refused() -> None:
    """The shape that cannot come back False, with no evidence the level came from the NL."""
    findings = capability.vacuous_containment_findings((_nested(),))
    assert findings, "a self-prefixed containment must be refused"
    assert "Sys.Outer.Inner" in findings[0]


def test_the_finding_says_where_the_parent_must_come_from() -> None:
    """A refusal the producer cannot act on gets argued with instead of fixed."""
    finding = capability.vacuous_containment_findings((_nested(),))[0]
    assert "source_context.nl_parent" in finding
    assert "sentence" in finding.lower()


def test_agreement_is_admitted_because_refusing_it_has_no_legal_answer() -> None:
    """`nl_parent` 等于已声明前缀 —— 这条需求由构造成立，但**放行**而不是拒。

    该分支原本拒绝，理由是「模型按构造已满足，这次 check 白花」。那是**成本论证，不是正确性
    论证**，而它与另外两条指令构成无解闭环：splitter prompt 说 containment 语言必须产出
    containment 需求，评审员规则说只用效果迁移表示它属 material omission。生产者产出 → 本门
    要求删 → 评审员要求加回 → 本门再拒。两侧预算都有限，所以不是死循环而是**整格隔离**。

    激活面证实这不是理论风险：v21+v22 的 480 条 containment 绑定里 **302 条（63%）是自前缀
    形状**，v22 的 68 格中 32 格至少命中一次，单个需求集最多 11 条，而修复预算只有 5 次且与
    其它契约错误共用。

    门要拦的位移由另外两支覆盖 —— `nl_parent` 缺失（无从判断来源）与 `nl_parent` 指向别处
    （明知句子说的是另一层却绑在模型的摆放上）。「句子本来就说这一层」是**正确的需求**，
    只是恰好由构造成立：放行的代价是一次无信息的 check，拒绝的代价是整格数据。
    """
    assert capability.vacuous_containment_findings((_nested(nl_parent="Sys.Outer"),)) == ()


def test_a_proposed_child_is_admitted_because_its_false_is_a_real_finding() -> None:
    """`child` 未声明时，`containment` 返回 False —— 那是元素缺失，不是空洞查询。

    本门的整个前提是「已声明路径的自前缀必为其父，所以答案由拼写决定」。`child` 是提名路径时
    前提不成立：答案由模型决定。没有别的门兜住这一类（`redundant_proposal_findings` 只在叶名
    在词表里另有声明时才拦），而 v23 恰好抬高了它的出现概率 —— prompt 早教「路径写成
    `<句子所指的父>.<名字>`」，v23 又新教「parent 绑句子所指的层」，两条叠加后
    `nl_parent + "." + name` 作 child 是自然产物。
    """
    req = _Req({"parent": "Sys.Outer", "child": "Sys.Outer.Missing"})
    assert capability.vacuous_containment_findings((req,), ["Sys.Outer", "Sys.Outer.Inner"]) == ()
    # 不传词表时退回旧行为 —— 老 bundle 与不提供词表的调用方不受影响。
    assert capability.vacuous_containment_findings((req,)) != ()


def test_disagreement_is_admitted_and_is_the_whole_point() -> None:
    """The sentence puts it one level up; the model buries it. The False is the finding."""
    req = _Req({"parent": "Sys", "child": "Sys.Outer.Inner"}, nl_parent="Sys")
    assert capability.vacuous_containment_findings((req,)) == ()


def test_a_cross_level_pair_is_admitted_even_without_nl_parent() -> None:
    """Only the self-prefixed shape needs its provenance justified.

    A `parent` that is not the child's prefix cannot have been copied off the child, so the
    gate has nothing to catch and demanding the field would be pure friction.
    """
    req = _Req({"parent": "Sys.Other", "child": "Sys.Outer.Inner"})
    assert capability.vacuous_containment_findings((req,)) == ()


def test_a_grandchild_is_admitted() -> None:
    """`containment` is direct membership, so two segments deep is discriminating."""
    req = _Req({"parent": "Sys", "child": "Sys.Outer.Inner"})
    assert capability.vacuous_containment_findings((req,)) == ()


def test_other_predicates_are_untouched() -> None:
    req = _Req({"parent": "Sys.Outer", "child": "Sys.Outer.Inner"})
    req.predicate = "initial_target"
    assert capability.vacuous_containment_findings((req,)) == ()


def test_a_missing_binding_is_not_this_gates_business() -> None:
    """Unresolved or absent bindings have their own gate; this one must not double-report."""
    assert capability.vacuous_containment_findings((_Req({"parent": "Sys.Outer"}),)) == ()
    assert capability.vacuous_containment_findings((_Req({}),)) == ()


def test_a_correctly_filled_nl_parent_that_is_ignored_is_still_refused() -> None:
    """填对了字段却不照做 —— 这是最该拦的形态，而原设计放行了它。

    门的三分支里，「`nl_parent` 缺失」与「`nl_parent` 等于绑定」都拦，只有「`nl_parent` 指向别的
    层」放行。可那正是完整的位移：生产者**知道**句子说的是另一层（它自己写在字段里），仍把断言绑在
    模型的摆放上。

    不补这一支，唯一能绕过这道门的方式就是**把字段填对** —— 一道要求记录 provenance 的门，如果只在
    provenance 缺失时才拦，就等于奖励「填了但不照做」。
    """
    item = _Req({"parent": "Sys.Outer", "child": "Sys.Outer.Inner"}, "Sys", "REQ-DISPLACED")
    findings = capability.vacuous_containment_findings([item])
    assert len(findings) == 1, findings
    assert "nl_parent='Sys'" in findings[0]
    assert "the level the sentence names" in findings[0]


def test_a_cross_level_binding_is_never_touched_whatever_nl_parent_says() -> None:
    """可判别绑定按构造不是自前缀形状，门连看都看不到它 —— 这是「不压真命中」的全部依据。"""
    for nl_parent in ("__absent__", "Sys", "Sys.Outer"):
        item = _Req({"parent": "Sys", "child": "Sys.Outer.Inner"}, nl_parent, "REQ-OK")
        assert capability.vacuous_containment_findings([item]) == (), nl_parent
