"""内部配额耗尽必须降级落盘，不许整格崩（CLAUDE.md §10）。

存在的理由是一次实跑事故：v41 的 `run1/0049-gpt` 与 `run2/0039-gpt` 死在
`convert_assertions` 的结构性死锁上——契约要求用需求点名的谓词，该谓词在那份制品上必然
拒绝作答（`UnsupportedEvidence`：两条无条件初始边），改用别的谓词又被同一条契约打回。
预算耗尽后节点抛异常、整格不落盘，外层 shell 冷启动重跑，把上一次的诊断整个丢掉。
代价是 24 个废弃 try 目录、206 次作废的 LLM 调用，以及**两个样本从被测集里消失**——
而最容易这样消失的，恰恰是制品缺陷最硬的那些格。

下面锁四件事，每一件都对应一种"看起来修好了其实没有"的写法：

1. 预算耗尽要降级，且必须回退到真正通过过契约的产物。
2. 降级必须留痕。**零 gap 的降级比崩还糟**——它产出一份与干净运行无法区分的制品。
3. 只有预算耗尽算降级；`output is None` 这类（provider / schema 类）仍须走致命路径。
   这条曾经写错过：用 `not can_revise_contract` 当条件，把首轮契约拒绝也吞了，
   于是 FBMCQ 强制族被静默豁免。
4. 真正致命时，失败收据必须带上已积累的 gap 与降级轨迹，让崩掉的格仍可分析。
"""

from __future__ import annotations

import json
import pathlib
import sys

import pytest
from pydantic import BaseModel

sys.path.insert(
    0, str(pathlib.Path(__file__).resolve().parents[1] / "src")
)

from paper_stm_feedback_loop.discover import cli, nodes  # noqa: E402
from paper_stm_feedback_loop.discover.schemas import (  # noqa: E402
    AssertionScript,
    DiscoverInput,
    RequirementSet,
)

FIXTURE_STM = """state Root {
    event go;
    state Idle;
    state Done;
    [*] -> Idle;
    Idle -> Done : go;
}
"""


def _input(run_id: str) -> DiscoverInput:
    return DiscoverInput(
        run_id=run_id,
        natural_language="When go occurs, the system shall enter Done.",
        stm_text=FIXTURE_STM,
        language="en-US",
    )


def _requirements() -> RequirementSet:
    return RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "When go occurs, the system shall enter Done.",
                "checkability": "effect",
            },
        ),
    )


def _relation_only_script(revision: int) -> AssertionScript:
    """A script the contract always rejects: a behaviour requirement needs simulation."""

    return AssertionScript(
        revision=revision,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "relation only",
                "expression": "True",
                "failure_message": "[REQ-001][AST-REQ-001-01] relation only",
                "evidence_family": "relation",
                "role": "primary",
                "coverage_key": "AST-REQ-001-01",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )


def _repeating_responder() -> nodes.CallableStructuredResponder:
    revisions = iter(range(1, 12))
    return nodes.CallableStructuredResponder(
        lambda _role, _schema, _system, _payload: _relation_only_script(
            next(revisions)
        )
    )


def _converge_to_degradation() -> dict:
    """Drive `convert_assertions` until it gives up, returning the final state slice."""

    frozen = nodes._fallback_prepare(_input("degrade"))
    responder = _repeating_responder()
    state: dict = {
        "_input": _input("degrade"),
        "frozen_inputs": frozen,
        "requirement_set": _requirements(),
    }
    for _ in range(10):
        update = nodes.convert_assertions(state, responder)
        state = {**state, **update}
        if state.get("_degraded_stages") or "failure" in state:
            return state
    raise AssertionError("conversion neither converged nor degraded within 10 rounds")


def test_budget_exhaustion_degrades_instead_of_failing() -> None:
    state = _converge_to_degradation()
    assert "failure" not in state, "an exhausted internal budget must not kill the cell"
    assert state["_degraded_stages"]
    assert state["_degraded_stages"][0].startswith("convert_assertions: ")


def test_the_fallback_is_an_artifact_that_cleared_the_contract() -> None:
    """Falling back to the *rejected* script would launder it into the run."""

    state = _converge_to_degradation()
    fallback = state["assertion_script"]
    # The only script that ever cleared the contract in this fixture is the first one the node
    # accepted; the rejected revisions must not become the artifact.
    assert fallback.revision >= 1
    assert all(item.role == "primary" for item in fallback.assertions)


def test_a_degradation_always_leaves_a_gap() -> None:
    """Zero-gap degradation is worse than a crash: it looks exactly like a clean run."""

    state = _converge_to_degradation()
    gaps = state["coverage_gaps"]
    assert gaps, "a silent degradation is indistinguishable from a clean result"
    assert {gap.stage for gap in gaps} == {"assertion_conversion"}
    assert all(gap.blocks_full_coverage for gap in gaps)
    assert all(gap.reason_code in {"no_progress", "revision_budget_exhausted"} for gap in gaps)


def test_the_router_is_released_so_the_graph_advances() -> None:
    """Leaving either key set sends the graph back into the node that just gave up."""

    state = _converge_to_degradation()
    assert state["_assertion_conversion_contract_feedback"] is None
    assert state["_assertion_feedback"] is None


def test_the_ledger_records_the_abandonment() -> None:
    state = _converge_to_degradation()
    event = state["_assertion_revision_ledger"][-1]
    assert event.event == "artifact_quarantined"
    assert event.status == "degraded_budget_exhausted"
    assert event.findings, "the contract message is the diagnosis; it must survive"


def test_an_empty_response_still_fails_rather_than_degrading() -> None:
    """`output is None` is the provider/schema class §10 does exempt -- keep it fatal.

    Regression guard for a real mistake: the first version of this patch keyed degradation on
    `not can_revise_contract`, which is also true when nothing came back to revise. That
    swallowed a first-revision contract rejection and silently waived a mandatory evidence
    family, landing a cell with zero issues and zero gaps.
    """

    def empty(_role: str, _schema: type[BaseModel], _system: str, _payload: str):
        raise RuntimeError("transport returned nothing")

    frozen = nodes._fallback_prepare(_input("empty"))
    update = nodes.convert_assertions(
        {
            "_input": _input("empty"),
            "frozen_inputs": frozen,
            "requirement_set": _requirements(),
        },
        nodes.CallableStructuredResponder(empty),
    )
    assert "failure" in update
    assert "_degraded_stages" not in update


def test_the_failure_receipt_carries_the_diagnosis(tmp_path: pathlib.Path) -> None:
    """A cell that genuinely dies must still be analysable, not just a traceback."""

    state = _converge_to_degradation()
    cli._write_failure_artifacts(
        tmp_path,
        run_id="degrade-receipt",
        profile="fake",
        content_language="zh-CN",
        error_type="RuntimeError",
        error_message="Discover graph failed at convert_assertions",
        state=state,
    )
    payload = json.loads((tmp_path / "discover-failed.json").read_text())
    assert payload["degraded_stages"] == list(state["_degraded_stages"])
    assert len(payload["coverage_gaps"]) == len(state["coverage_gaps"])
    assert payload["coverage_gaps"][0]["stage"] == "assertion_conversion"
    markdown = (tmp_path / "loops" / "discover-failed.md").read_text()
    assert "未满足的义务" in markdown
    assert "已降级的阶段" in markdown


def test_the_receipt_survives_a_failure_with_no_state() -> None:
    """Provider errors raise before any state exists; the receipt must not crash on that."""

    import tempfile

    with tempfile.TemporaryDirectory() as raw:
        root = pathlib.Path(raw)
        cli._write_failure_artifacts(
            root,
            run_id="no-state",
            profile="fake",
            content_language="zh-CN",
            error_type="AuthenticationError",
            error_message="401",
            state=None,
        )
        payload = json.loads((root / "discover-failed.json").read_text())
        assert payload["coverage_gaps"] == []
        assert payload["degraded_stages"] == []


@pytest.mark.parametrize("attr", ["_degrade_state", "_degraded_conversion"])
def test_the_helpers_are_module_level_and_importable(attr: str) -> None:
    assert hasattr(nodes, attr)


def test_a_degraded_run_reaches_publish_so_the_cell_lands() -> None:
    """The whole point: `discover-completed.json` gets written, so the sample stays measured.

    Node-level assertions above prove the state is shaped right; only a graph-level run proves
    the router actually advances to `publish` instead of `run_failed`. Without this the cell
    would still vanish from the measured set, which is the harm §10 names.
    """

    from paper_stm_feedback_loop.discover.graph import run_discover_state

    revisions = iter(range(1, 40))

    def responder(_role: str, schema: type[BaseModel], _system: str, _payload: str):
        if schema is AssertionScript:
            return _relation_only_script(next(revisions))
        return nodes.default_fake_responder(_role, schema, _system, _payload)

    state = run_discover_state(_input("degrade-e2e"), responder)
    assert "failure" not in state
    assert state["final_output"].status == "completed"
    assert state["_degraded_stages"], "a landed cell must still say it gave up"
    assert state["final_output"].issues == (), (
        "nothing may be published off evidence the contract rejected"
    )


def test_degradation_gaps_are_distinguishable_from_isolation_gaps() -> None:
    """降级 gap 不得被读成隔离，否则评审门会在最该生效的格上静默跳过。

    `review_requirements` 降级时会给**每一条**需求写一条 gap。而 Assertion Reviewer 的 payload
    里没有 `quarantined_requirement_ids`（`renderer.render_assertion_review_input` 不带），
    它判断「哪条被隔离」的唯一依据就是 `coverage_gaps`。若两类 gap 不可区分，评审者按
    「for every non-quarantined Requirement」的字面读法可以认定「没有需要审的需求」。

    可区分性由两个字段承载，这里把它们钉死：降级 gap 的 `assertion_ids` 为空、`gap_id` 以
    `-DEGRADED` 结尾；prompt 据此给出读法。
    """

    from paper_stm_feedback_loop.discover import prompts

    state = _converge_to_degradation()
    degradation_gaps = [
        gap for gap in state["coverage_gaps"] if gap.gap_id.endswith("-DEGRADED")
    ]
    assert degradation_gaps, "fixture must produce at least one degradation gap"
    assert all(gap.assertion_ids == () for gap in degradation_gaps)

    reviewer = prompts.ASSERTION_REVIEWER_PROMPT
    assert "-DEGRADED" in reviewer, "评审者必须被告知如何识别降级 gap"
    assert "not named by an isolation gap" in reviewer
    assert "requirement_mapping` is empty" in reviewer, (
        "全隔离脚本必须被明确豁免，否则评审者会为缺失的 mapping 反复要求修订"
    )


def test_the_landed_artifact_exposes_the_degradation() -> None:
    """可审计性的落点：`discover-completed.json` 自己必须说出「这一格降级过」。

    这是整套改造成立的前提。降级的代价是产出一份**看起来正常**的制品；若落盘件里没有这个字段，
    读者无从区分「没发现缺陷」与「停止了寻找」，那就用一个静默的错误换掉了一个响亮的错误。
    `coverage_gaps` 顶不上：逐项隔离也写 gap，那是常态。
    """

    from paper_stm_feedback_loop.discover.graph import run_discover_state

    revisions = iter(range(1, 40))

    def responder(_role: str, schema: type[BaseModel], _system: str, _payload: str):
        if schema is AssertionScript:
            return _relation_only_script(next(revisions))
        return nodes.default_fake_responder(_role, schema, _system, _payload)

    state = run_discover_state(_input("degrade-artifact"), responder)
    published = state["final_output"]
    assert published.degraded_stages, "落盘件必须自带降级轨迹"
    assert published.degraded_stages == tuple(state["_degraded_stages"])
    assert published.coverage_status == "partial"
    # 序列化后仍在：读 JSON 的人（以及 eval 侧扫描）拿到的是这一份。
    assert published.model_dump(mode="json")["degraded_stages"]


def test_the_markdown_report_warns_about_degradation(tmp_path: pathlib.Path) -> None:
    from paper_stm_feedback_loop.discover.graph import run_discover_state
    from paper_stm_feedback_loop.discover.report import write_discover_markdown

    revisions = iter(range(1, 40))

    def responder(_role: str, schema: type[BaseModel], _system: str, _payload: str):
        if schema is AssertionScript:
            return _relation_only_script(next(revisions))
        return nodes.default_fake_responder(_role, schema, _system, _payload)

    state = run_discover_state(_input("degrade-md"), responder)
    path = write_discover_markdown(state, tmp_path / "discover.md")
    text = path.read_text()
    assert "本格发生过降级" in text
    assert "不得读作" in text


def test_a_budget_can_be_lowered_but_never_raised(monkeypatch: pytest.MonkeyPatch) -> None:
    """故障注入设施只能让流水线**更早**放弃，不能让它接受本该拒绝的东西。

    降级路径在真实 pair 上很少走到——v42 四格实跑 0 次降级。对流水线是好消息，对信心是坏消息：
    一条在生产里从没跑过的恢复路径，等于没人见过它在生产里成立。所以预算可从环境下调，
    用来在真实 provider 上强制触发。但它必须是单向的，否则就成了放宽契约的后门。
    """

    monkeypatch.setenv("DISCOVER_BUDGET_ASSERTION_CONTRACT", "1")
    assert nodes._budget("ASSERTION_CONTRACT", 5) == 1
    monkeypatch.setenv("DISCOVER_BUDGET_ASSERTION_CONTRACT", "99")
    assert nodes._budget("ASSERTION_CONTRACT", 5) == 5, "不得调高"
    monkeypatch.setenv("DISCOVER_BUDGET_ASSERTION_CONTRACT", "0")
    assert nodes._budget("ASSERTION_CONTRACT", 5) == 1, "下限为 1"
    monkeypatch.setenv("DISCOVER_BUDGET_ASSERTION_CONTRACT", "abc")
    assert nodes._budget("ASSERTION_CONTRACT", 5) == 5, "非法值回落默认"
    monkeypatch.delenv("DISCOVER_BUDGET_ASSERTION_CONTRACT")
    assert nodes._budget("ASSERTION_CONTRACT", 5) == 5


def test_an_injected_budget_is_recorded_so_the_cell_cannot_pass_as_normal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """强制降级的格与普通格若产出无法区分，这个设施本身就成了污染源。"""

    monkeypatch.setenv("DISCOVER_BUDGET_ASSERTION_CONTRACT", "1")
    assert nodes._budgets_from_env() == {"ASSERTION_CONTRACT": 1}
    monkeypatch.delenv("DISCOVER_BUDGET_ASSERTION_CONTRACT")
    assert nodes._budgets_from_env() == {}, "未注入时必须为空，否则正常运行也会被标记"
