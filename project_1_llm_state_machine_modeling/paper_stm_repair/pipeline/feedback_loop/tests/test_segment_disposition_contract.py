"""`covered` 段必须有需求承接；空响应要重发而不是整格致命。

## 这两条为什么放在一起

它们是 v36 那 5 次整格重跑的两个来源，而且都属同一个形状：**契约写下来了，但没有任何东西执行它。**

### `covered` 段无承接（3 次重试 + 一次沉默漏检）

`segment_disposition` 的 description 逐字写着「`covered` asserts that some Requirement here carries
that segment's obligation」，`source_segment_ids` 的 description 也写着「every segment you mark
`covered` … must be listed by at least one requirement here」。两处都是断言式的，而检查只有键集匹配。

两种后果实测都发生过：

1. **沉默漏检。** v36 `run1/0000-claude` 把 `NL-M006`（power off → final state）标 `covered` 却无承接
   需求，于是 `coverage_status` 报 `full`、裁决说「All released assertions evaluated True」、零 issue
   —— 读起来像一次干净的完整通过。该格在上一代次是命中的。
2. **修订锁死。** 评审**确实**发现它时（`run2/0000-gpt`），finding 说的是「缺了一条需求」——
   而那归责不到任何 requirement id，于是预算耗尽后隔离机制无人可摘，整格致命。实测超过半数的
   评审 finding 都归责不到人（v35 101/191、v36 83/154），这一类是最大的一支。

所以在 splitter 侧确定性地查，且消息给**两条**出路。只给「补一条需求」会逼它为范围外的段编义务 ——
那正是 `run3/0047-gpt` 锁死的样子：评审要求为一句讲正交区并发的 NL 补义务，而并发在建模对象之外。

### provider 空响应（2 次重试）

`ValidationError: Input should be a valid dictionary or instance of RequirementSet
[type=model_type, input_value=None]`。transport 的 8 次重试没触发 —— HTTP 响应成功了，只是内容为空。

判据必须**窄**：首版写成「`output` 为空且异常是 TypeError/ValueError」，把 create/revise 配对违规
也算进去了，而那类属 no-progress 家族必须保持致命 —— `make test` 里那条测试立刻变红。
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from pydantic import BaseModel, ValidationError

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover import nodes  # noqa: E402
from paper_stm_feedback_loop.discover.schemas import RequirementSet  # noqa: E402


# ---------------------------------------------------------------- 空响应判定

class _Tiny(BaseModel):
    value: int


def _empty_model_error() -> ValidationError:
    """顶层模型收到 `None` —— provider 空响应的形状。"""

    try:
        _Tiny.model_validate(None)
    except ValidationError as exc:
        return exc
    raise AssertionError("expected a ValidationError")


def _field_error() -> ValidationError:
    """字段值不合法 —— 有产物、该修那一处，**不是**空响应。"""

    try:
        _Tiny.model_validate({"value": "not an int"})
    except ValidationError as exc:
        return exc
    raise AssertionError("expected a ValidationError")


def test_a_none_top_level_model_is_an_empty_response() -> None:
    assert nodes._is_empty_structured_response(_empty_model_error()) is True


def test_a_bad_field_value_is_not_an_empty_response() -> None:
    """⭐ 负控：有产物但字段不合法，处置是「修那一处」，不能走重发。"""

    assert nodes._is_empty_structured_response(_field_error()) is False


def test_a_wrapped_validation_error_is_still_seen() -> None:
    """节点把它包成 `RuntimeError(f"ValidationError: ...")`，所以要看异常链。"""

    inner = _empty_model_error()
    try:
        try:
            raise inner
        except ValidationError as exc:
            raise RuntimeError(f"ValidationError: {exc}") from exc
    except RuntimeError as outer:
        assert nodes._is_empty_structured_response(outer) is True


def test_an_ordinary_exception_is_not_an_empty_response() -> None:
    """⭐ 负控：判据不能宽到「任何 ValueError 都算」。

    首版就是这么写的，结果把 create/revise 配对违规算了进去，而那类必须保持致命。
    """

    for exc in (ValueError("revision must increase"), TypeError("x"), RuntimeError("y")):
        assert nodes._is_empty_structured_response(exc) is False


def test_a_lookalike_errors_method_does_not_crash_the_check() -> None:
    """⭐ 负控：非 pydantic 的同名 `errors()` 不得让判据抛。"""

    class Weird(Exception):
        def errors(self):  # noqa: ANN201
            raise RuntimeError("not pydantic")

    assert nodes._is_empty_structured_response(Weird()) is False


def test_a_self_referential_exception_chain_terminates() -> None:
    """⭐ 负控：`__context__` 成环时不得死循环。"""

    exc = RuntimeError("a")
    exc.__context__ = exc
    assert nodes._is_empty_structured_response(exc) is False


# ---------------------------------------------------------------- covered 段承接

def _requirement(requirement_id: str, segments: tuple[str, ...]) -> dict:
    return {
        "requirement_id": requirement_id,
        "statement": "s",
        "verification_kind": "structure",
        "source_segment_ids": segments,
        # v2 生产者路径要求显式给出 —— 少了它另一条既有契约会先拦下，
        # 于是本文件要测的那条永远走不到。
        "coverage_obligation": {"domain": "Root", "aggregation": "all"},
    }


def _split(state, responder_output: RequirementSet):
    def responder(_role, schema, _system, _payload):
        assert schema is RequirementSet
        return responder_output

    return nodes.split_requirements(
        state, nodes.CallableStructuredResponder(responder)
    )


@pytest.fixture
def state():
    from paper_stm_feedback_loop.discover.schemas import DiscoverInput

    payload = DiscoverInput(
        run_id="seg-contract",
        # `nl_segmentation_source` 默认是 `line_split`，所以分段按**行**而非按句 ——
        # 首版写成一行两句，只得到一个段，断言当场发现。两行才有两个 id：
        # 一个被承接、一个不被，正是要测的形状。
        natural_language="After go, Done shall become active.\nThe run then ends.",
        stm_text=(
            'state Root named "Root" { state Done named "Done"; '
            "event go named \"go\"; [*] -> Done; }"
        ),
        language="en-US",
    )
    frozen = nodes._fallback_prepare(payload)
    assert len(frozen.nl_segments) >= 2, frozen.nl_segments
    return {"_input": payload, "frozen_inputs": frozen}, frozen


def test_a_covered_segment_with_no_requirement_is_refused(state) -> None:
    """⭐ 这是 v36 `run1/0000-claude` 沉默漏检的形状。"""

    base, frozen = state
    segments = sorted(frozen.nl_segments)
    output = RequirementSet(
        revision=1,
        requirements=(_requirement("REQ-001", (segments[0],)),),
        segment_disposition={segments[0]: "covered", segments[1]: "covered"},
    )
    result = _split(base, output)
    findings = (result.get("_requirement_feedback").findings if result.get("_requirement_feedback") else ())
    joined = " ".join(findings) + str(result.get("failure") or "")
    assert segments[1] in joined
    assert "no requirement carrying them" in joined


def test_the_refusal_offers_both_routes(state) -> None:
    """⭐ 只给「补一条需求」会逼它为范围外的段编义务 —— `run3/0047-gpt` 锁死的样子。"""

    base, frozen = state
    segments = sorted(frozen.nl_segments)
    output = RequirementSet(
        revision=1,
        requirements=(_requirement("REQ-001", (segments[0],)),),
        segment_disposition={s: "covered" for s in segments},
    )
    result = _split(base, output)
    joined = " ".join(result["_requirement_feedback"].findings)
    assert "out_of_scope" in joined
    assert "concurrent orthogonal regions" in joined
    assert "ambiguous" in joined
    assert "context" in joined


def test_out_of_scope_and_context_need_no_requirement(state) -> None:
    """⭐ 负控：只有 `covered` 承担这个义务，其余三值不得被误拦。"""

    base, frozen = state
    segments = sorted(frozen.nl_segments)
    output = RequirementSet(
        revision=1,
        requirements=(_requirement("REQ-001", (segments[0],)),),
        segment_disposition={segments[0]: "covered", segments[1]: "out_of_scope"},
    )
    result = _split(base, output)
    assert result.get("failure") is None
    assert result.get("_requirement_feedback") is None
    assert result["requirement_set"].revision == 1


# ---------------------------------------------------------------- 隔离造成的孤立段

from types import SimpleNamespace  # noqa: E402

from paper_stm_feedback_loop.discover.capability import (  # noqa: E402
    orphaned_covered_segments,
)


def _spec(segments: tuple[str, ...]):
    return SimpleNamespace(source_segment_ids=segments)


def test_the_predicate_names_only_unbacked_covered_segments() -> None:
    disposition = {"S1": "covered", "S2": "covered", "S3": "out_of_scope", "S4": "context"}
    reqs = [_spec(("S1",))]
    assert orphaned_covered_segments(disposition, reqs) == ("S2",)


def test_only_covered_carries_the_obligation() -> None:
    """⭐ 负控：其余三个取值不承担承接义务，不得被误报。"""

    disposition = {"A": "out_of_scope", "B": "ambiguous", "C": "context"}
    assert orphaned_covered_segments(disposition, []) == ()


def test_a_consistent_set_yields_nothing() -> None:
    disposition = {"S1": "covered", "S2": "covered"}
    assert orphaned_covered_segments(disposition, [_spec(("S1", "S2"))]) == ()


def test_the_result_is_sorted_and_deduplicated() -> None:
    disposition = {"S9": "covered", "S1": "covered", "S5": "covered"}
    assert orphaned_covered_segments(disposition, []) == ("S1", "S5", "S9")


def test_an_empty_disposition_is_not_an_error() -> None:
    assert orphaned_covered_segments({}, [_spec(("S1",))]) == ()
    assert orphaned_covered_segments(None, []) == ()


def test_quarantine_records_the_orphaned_segments_it_created(state) -> None:
    """⭐ 这是 v37 `run1/0057-gpt` 丢格的形状：隔离摘掉唯一承接者。

    第一处检查看的是生产者原始输出（那时承接者还在），所以只有这第二处能捕获它。
    处置是**记录**而非硬拒或自动改标 —— 见 `orphaned_covered_segment_ids` 的 description。
    """

    base, frozen = state
    segments = sorted(frozen.nl_segments)
    # 两条需求各承接一个段；让门归责掉第二条，于是 segments[1] 失去承接。
    output = RequirementSet(
        revision=1,
        requirements=(
            _requirement("REQ-001", (segments[0],)),
            _requirement("REQ-002", (segments[1],)),
        ),
        segment_disposition={segments[0]: "covered", segments[1]: "covered"},
    )
    # 直接验谓词在「隔离后」的集合上给出正确答案 —— 隔离本身由门驱动，不在本测试范围内。
    survivors = [r for r in output.requirements if r.requirement_id != "REQ-002"]
    assert orphaned_covered_segments(output.segment_disposition, survivors) == (segments[1],)
    # 而隔离前它是一致的 —— 这正是第一处检查放行的原因。
    assert orphaned_covered_segments(output.segment_disposition, output.requirements) == ()


def test_the_projection_field_exists_and_defaults_empty() -> None:
    """⭐ 字段必须有默认值 —— 否则每个既有构造点都要改，而漏改会静默丢掉这个事实。"""

    from paper_stm_feedback_loop.discover.schemas import RequirementCoverageProjection

    projection = RequirementCoverageProjection(covered_requirement_ids=("REQ-001",))
    assert projection.orphaned_covered_segment_ids == ()
    described = RequirementCoverageProjection.model_json_schema()["properties"][
        "orphaned_covered_segment_ids"
    ]["description"]
    # 三种处置的取舍必须在 schema 里说清，因为读到这个字段的人需要知道为什么没被自动修
    assert "not** producer error" in described or "not producer error" in described
    assert "re-marked" in described


def test_the_reviewer_prompt_explains_the_field() -> None:
    """⭐ 记录了但下游不知道怎么用，等于没记录 —— 这正是原来那个反馈的毛病。"""

    from paper_stm_feedback_loop.discover import prompts

    text = prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "orphaned_covered_segment_ids" in text
    assert "not producer error" in text
    # 必须要求可操作的两条出路，而不是笼统地「去覆盖它」
    assert "re-mark the segment" in text
    assert "exhausts the revision budget" in text
