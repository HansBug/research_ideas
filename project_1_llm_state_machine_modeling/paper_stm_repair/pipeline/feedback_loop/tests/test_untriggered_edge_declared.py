"""`untriggered_edge_declared` 的语义边界。

⚠️ 这个谓词存在的理由是 `edge_declared` 必填 `trigger`，而声明里有相当一部分迁移不带触发，
因此无法成为任何声明类谓词的主体。

⛔ **最危险的替代设计是给 `edge_declared` 传 `event=None`。** `structure.transitions` 把 `None`
过滤器当作**未设置**，于是该调用会匹配**任意**触发的边 —— 把 False 变成 True，静默撤回当前成立的
发现。本文件的 `test_does_not_match_a_triggered_edge` 就是钉住这个区别的。
"""

from __future__ import annotations

import pytest

from paper_stm_feedback_loop.assertions.predicate_api import PredicateAPI

MODEL = """
state Sys {
    state Idle;
    state Warm;
    state Done;
    Idle -> Warm : go;
    Warm -> Done;
    [*] -> Idle;
}
"""


def _api(text: str = MODEL) -> PredicateAPI:
    from paper_stm_feedback_loop.assertions.runtime import build_eval_environment

    return build_eval_environment(
        model_text=text,
        source_mappings=[],
        source_exclusions=[],
        timeout_seconds=30,
        fbmcq_solver_timeout_ms=15_000,
        fbmcq_max_bound=4,
        fbmcq_process_wall_seconds=20.0,
    ).predicates


def test_matches_a_declared_trigger_free_edge() -> None:
    """正对照：`Warm -> Done` 无触发，应为 True。"""
    assert _api().untriggered_edge_declared(source="Sys.Warm", target="Sys.Done") is True


def test_does_not_match_a_triggered_edge() -> None:
    """⭐ 关键负对照：`Idle -> Warm : go` **带**触发，必须为 False。

    若为 True，说明实现把 trigger 过滤器当成了「不过滤」—— 那正是 `event=None` 方案的失效模式。
    """
    assert _api().untriggered_edge_declared(source="Sys.Idle", target="Sys.Warm") is False


def test_false_for_an_edge_that_is_not_declared_at_all() -> None:
    """未声明的边为 False —— 声明类谓词的 False 就是发现。"""
    assert _api().untriggered_edge_declared(source="Sys.Done", target="Sys.Idle") is False


def test_edge_declared_still_refuses_every_no_trigger_sentinel() -> None:
    """回归闸：本次改动**不得**顺手放宽 `edge_declared`。

    它必须继续拒绝所有「无触发」哨兵；新能力只经由新谓词提供。这条钉住「现有调用完全不动」，
    即上一轮 review 的 C2（丢掉现有命中）在本设计下不可能发生。
    """
    from paper_stm_feedback_loop.assertions.exceptions import UnsupportedEvidence

    api = _api()
    for sentinel in ("", "[*]", "-"):
        with pytest.raises(UnsupportedEvidence):
            api.edge_declared(source="Sys.Warm", trigger=sentinel, target="Sys.Done")
    with pytest.raises(TypeError):
        api.edge_declared(source="Sys.Warm", target="Sys.Done")  # type: ignore[call-arg]


def test_registered_in_the_closed_vocabulary() -> None:
    """谓词必须同时登记进词表与 capability，否则断言脚本调不到 / 归因层不认。"""
    from paper_stm_feedback_loop.discover.capability import EVIDENCE_CAPABILITY
    from paper_stm_feedback_loop.discover.predicates import PREDICATE_NAMES

    assert "untriggered_edge_declared" in PREDICATE_NAMES
    assert "untriggered_edge_declared" in EVIDENCE_CAPABILITY
