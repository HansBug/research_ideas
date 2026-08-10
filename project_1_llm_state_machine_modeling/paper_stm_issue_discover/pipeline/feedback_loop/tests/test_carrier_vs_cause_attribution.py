"""归因分流：被排除的元素是「作者所写之物的 lowering」还是「投影插入的替身」。

## 这套测试钉的是什么

`R45RouteToken` 是投影**加到每一个模型上**的路由变量 —— `nodes.py` 自己的注释写着
"that one carries no information about the author"。而跨层组迁移在 FCSTM 里的唯一实现形式就是经它
路由，于是**任何**关于跨层退出的行为证据都必然触碰它、必然被判 `representation_debt` 而永不发布。

实测：`0000` 的 `stays_in(AutoNavigating, <复合接管事件>)` 取 False —— 与台账为该缺陷指定的 primary
逐字相同、真值正确 —— 却因此没能发布。**台账指定的判据在旧规则下结构性不可发布**，这是规则的问题
而不是模型漏检。

新分支与既有的 `_omission_placeholder_only` 完全对称，两条都读合同自己的角色分类：

- 已有：全部排除元素是 `omission_surrogate` + 声明类谓词 → 替身**就是**那个遗漏
- 新增：全部排除元素是 `carrier` + 作者确实声明了见证该 False 的迁移 → 载体只是作者那条边的 lowering

三个条件缺任何一个都会把「运行经过了作者从未写过的节点」误判成作者的责任，所以下面每一条都有负控。
"""

from __future__ import annotations

from paper_stm_feedback_loop.discover.nodes import (
    _AUTHOR_EDGE_WITNESSES_FALSE,
    _carrier_only_and_author_declared_it,
)

CARRIER_REF = "compiler:route_control:R45RouteToken"
SURROGATE_REF = "compiler:state:Sys.M.UnspecifiedInitial"
ROLES = {
    "route_control:R45RouteToken": "carrier",
    "R45RouteToken": "carrier",
    "state:Sys.M.UnspecifiedInitial": "omission_surrogate",
    "Sys.M.UnspecifiedInitial": "omission_surrogate",
}
BINDINGS = {"source": "Sys.M.Leaf", "trigger": "Sys.evt"}


def _yes(source: str, trigger: str) -> bool:
    return True


def _no(source: str, trigger: str) -> bool:
    return False


def _undecidable(source: str, trigger: str) -> None:
    return None


def _call(**over):
    kwargs = {
        "debt_refs": (CARRIER_REF,),
        "predicate": "stays_in",
        "bindings": BINDINGS,
        "roles": ROLES,
        "author_declares_edge": _yes,
    }
    kwargs.update(over)
    return _carrier_only_and_author_declared_it(**kwargs)


def test_carrier_plus_author_declared_edge_is_safe() -> None:
    """三条都成立 —— 这就是 0000 那条被结构性封死的发现。"""

    assert _call() is True


def test_an_omission_surrogate_among_the_refs_refuses() -> None:
    """⭐ 负控：有一个排除元素不是 carrier，证据就还搭在别的东西上。

    此时它两边都说不了：既不能说载体只是 lowering，也不能说替身就是遗漏。
    """

    assert _call(debt_refs=(CARRIER_REF, SURROGATE_REF)) is False


def test_an_unclassified_ref_refuses() -> None:
    """⭐ 负控：角色映射查不到的引用不得当作 carrier 放行。"""

    assert _call(debt_refs=(CARRIER_REF, "compiler:whatever:Sys.Unknown")) is False


def test_missing_contract_refuses() -> None:
    """⭐ 负控：无合同（`roles` 为空）时退回原行为，不静默重分类每一个判定。"""

    assert _call(roles={}) is False


def test_author_did_not_declare_the_edge_refuses() -> None:
    """⭐ 负控：退出只因投影插入的路由而存在时，仍判 representation_debt。

    这是本条规则的**全部风险所在** —— 少了它，规则就变成「凡触碰 carrier 皆放行」。
    """

    assert _call(author_declares_edge=_no) is False


def test_undecidable_probe_refuses() -> None:
    """⭐ 负控：谓词拒答或环境不可用时不放行 —— 无法判定不等于放行。"""

    assert _call(author_declares_edge=_undecidable) is False


def test_only_predicates_whose_false_an_author_edge_witnesses() -> None:
    """⭐ 负控：不得外溢到别的行为谓词。

    `occupancy_after` / `reaches` 的 False 可以由「运行走了作者没写的路」造成，
    此时 `event_consumed` 为真也不能证明退出是作者的。
    """

    for predicate in ("occupancy_after", "reaches", "containment", "initial_target", None):
        assert _call(predicate=predicate) is False, predicate
    assert _AUTHOR_EDGE_WITNESSES_FALSE == {"stays_in"}


def test_incomplete_bindings_refuse() -> None:
    for bindings in ({}, {"source": "Sys.M.Leaf"}, {"trigger": "Sys.evt"}, None):
        assert _call(bindings=bindings) is False, bindings


def test_no_debt_refs_is_not_this_branch() -> None:
    assert _call(debt_refs=()) is False


def test_the_leaf_constraint_that_makes_the_probe_sound_is_the_predicates_own() -> None:
    """判据的可靠性依赖 `stays_in` 只接受叶态，这一点由谓词本身强制，不是本模块的假设。

    叶态没有内部可去处，所以作者在其上声明的该事件迁移只能是出边 —— 自环会让 `stays_in` 为真，
    而本分支的前提正是它为假。若哪天 `stays_in` 开始接受复合态，这条判据就不再可靠：复合态上
    「消费了该事件」可以由某个子态消费而复合态自身仍不退出，`event_consumed` 为真便不再蕴含退出。
    """

    import pytest

    from paper_stm_feedback_loop.assertions.exceptions import UnsupportedEvidence
    from paper_stm_feedback_loop.assertions.runtime import EvalEnvironment

    model = """
    state Sys named "Sys" {
        event evt named "evt";
        state M named "M" {
            state Leaf named "Leaf";
            state Other named "Other";
            [*] -> Leaf;
            Leaf -> Other : /evt;
        }
        [*] -> M;
    }
    """
    api = EvalEnvironment(model_text=model).predicates
    # 叶态可答 —— 这是判据实际使用的形状。
    assert api.stays_in(source="Sys.M.Leaf", trigger="Sys.evt") is False
    # 复合态被拒 —— 这正是让 `event_consumed` 足以蕴含「退出」的那条约束。
    with pytest.raises(UnsupportedEvidence, match="composite"):
        api.stays_in(source="Sys.M", trigger="Sys.evt")
