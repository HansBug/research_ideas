"""runner 的行为契约：输入完整性、降级不崩、record 自包含。

⚠️ 按仓库根 `CLAUDE.md` §10：「降级路径必须与正常路径一样有测试；只在正常路径上有测试的降级
等于没有。」所以这里对 provider 错误与 schema 错误两条路径都断言，⛔ 不只测 happy path。

⛔ 本文件不发起任何真实 API 调用：全部用假 model 注入（`monkeypatch`），⭐ 且 prompt generator
不读取任何凭据来源。
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ARM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ARM / "src"))

import runner
from schema import NaiveIssue, NaiveReview


class _FakeConfig:
    adapter = "openai"
    model = "fake-model-1"
    max_output_tokens = 65536
    context_window_tokens = 400000


class _FakeRegistry:
    def require(self, profile: str) -> _FakeConfig:
        return _FakeConfig()


class _FakeStructured:
    """按脚本依次抛出 / 返回，用来驱动重试路径。"""

    def __init__(self, script: list[object]) -> None:
        self.script = list(script)
        self.calls: list[list[object]] = []

    def invoke(self, messages: list[object]) -> object:
        self.calls.append(messages)
        item = self.script.pop(0) if self.script else self.script
        if isinstance(item, Exception):
            raise item
        return item


class _FakeModel:
    def __init__(self, structured: _FakeStructured) -> None:
        self._structured = structured
        self.structured_options: dict[str, object] = {}

    def with_structured_output(self, schema: object, **options: object) -> _FakeStructured:
        self.structured_options = dict(options)
        return self._structured


def _ok_response(issues: int = 2) -> dict[str, object]:
    return {
        "parsed": NaiveReview(
            analysis="looked at both",
            issues=[
                NaiveIssue(issue=f"i{n}", where=f"w{n}", reason=f"r{n}")
                for n in range(issues)
            ],
        ),
        "raw": None,
        "parsing_error": None,
    }


@pytest.fixture()
def wired(monkeypatch: pytest.MonkeyPatch):
    """把 registry 与 model 工厂换成假的，返回一个装配函数。"""

    def _wire(script: list[object]) -> _FakeModel:
        structured = _FakeStructured(script)
        model = _FakeModel(structured)
        monkeypatch.setattr(runner, "load_llm_registry", lambda _path=None: _FakeRegistry())
        # ⛔ 刻意**不** mock `adapter_name`：它是纯查表函数、不碰凭据，让真函数跑才能抓住
        # 调用侧传错参数。⚠️ 初版把 config 整个传了进去，mock 掉之后测试全绿、真实 smoke 才炸。
        # 每一个被 mock 掉的纯函数都是一处测试盲区。
        monkeypatch.setattr(
            runner, "create_chat_model", lambda *a, **k: model
        )
        monkeypatch.setattr(runner, "normalize_model_output_usage", lambda _raw: {})
        monkeypatch.setattr(runner.time, "sleep", lambda _s: None)
        return model

    return _wire


# --------------------------------------------------------------------------- 输入完整性


def test_prompt_carries_both_inputs_verbatim() -> None:
    """⛔ 不许截断（§4B.2「必须给」栏）。逐字包含是可断言的最强形式。"""

    nl = "REQ ONE.\n" * 400
    puml = "@startuml\nstate A\n@enduml\n" * 50
    system, user = runner.build_prompts(nl=nl, plantuml=puml, content_language="zh-CN")
    assert nl in user and puml in user
    assert "{content_language}" not in system, "placeholder must be substituted"
    assert "zh-CN" in system


def test_load_pair_reads_the_shared_inputs(tmp_path: Path) -> None:
    root = tmp_path / "reports"
    pair = root / "pairs" / "0000"
    pair.mkdir(parents=True)
    (pair / "nl.txt").write_text("spec text", encoding="utf-8")
    (pair / "plantuml.puml").write_text("@startuml\n@enduml\n", encoding="utf-8")
    loaded = runner.load_pair("0000", report_root=root)
    assert loaded["nl"] == "spec text"
    assert "@startuml" in loaded["plantuml"]


def test_load_pair_reports_missing_input(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        runner.load_pair("9999", report_root=tmp_path)


def test_real_corpus_has_54_in_scope_pairs() -> None:
    """⭐ 网格恒为 54 pair：`00x8` 家族按 `nl_scope_rule.md` 永久排除。"""

    pairs = sorted(p.name for p in (runner.REPORT_ROOT / "pairs").iterdir() if p.is_dir())
    assert len(pairs) == 60, f"corpus should hold 60 pairs, found {len(pairs)}"
    in_scope = [c for c in pairs if not c.endswith("8")]
    assert len(in_scope) == 54
    assert [c for c in pairs if c.endswith("8")] == [
        "0008",
        "0018",
        "0028",
        "0038",
        "0048",
        "0058",
    ]


# --------------------------------------------------------------------------- 正常路径


def test_ok_cell_records_everything_needed_for_audit(wired, tmp_path: Path) -> None:
    model = wired([_ok_response(3)])
    record = runner.run_cell(
        case="0000", profile="fake", report_root=_corpus_stub(tmp_path)
    )
    assert record["status"] == "ok"
    assert record["issue_count"] == 3
    # 自包含：不看别的文件也能复核这一格跑了什么。
    for key in (
        "system_prompt",
        "user_prompt",
        "prompt_sha256",
        "configured_model",
        "adapter",
        "provider",
        "profile_max_output_tokens",
        "inputs",
        "attempts",
        "usage",
    ):
        assert key in record, f"record is missing audit field {key!r}"
    # 真 `adapter_name` 的返回值，证明它是按字符串调用的。
    assert record["provider"] == "langchain-openai/chat-completions", record["provider"]
    assert record["inputs"]["truncated"] is False
    # ⭐ 证明没压输出预算，也没覆盖采样参数。
    assert record["max_output_tokens_override"] is None
    assert record["temperature_override"] is None
    assert record["profile_max_output_tokens"] == 65536
    # openai adapter 必须走 function_calling（理由见 runner 内注释）。
    assert model.structured_options.get("method") == "function_calling"
    assert model.structured_options.get("include_raw") is True


def test_empty_issue_list_is_a_valid_answer(wired, tmp_path: Path) -> None:
    """⭐「这份模型符合需求」是合法答案，⛔ 不是失败。"""

    wired([_ok_response(0)])
    record = runner.run_cell(case="0000", profile="fake", report_root=_corpus_stub(tmp_path))
    assert record["status"] == "ok"
    assert record["issue_count"] == 0


# --------------------------------------------------------------------------- 降级路径


class _TransportBoom(RuntimeError):
    status_code = 504


def test_transport_error_retries_then_records_failure(wired, tmp_path: Path) -> None:
    """provider 侧错误：重试，穷尽后**落盘** failed，⛔ 不抛给调用方。"""

    wired([_TransportBoom("gateway timeout")] * 6)
    record = runner.run_cell(
        case="0000", profile="fake", report_root=_corpus_stub(tmp_path), transport_retries=2
    )
    assert record["status"] == "failed"
    assert record["failure_class"] == "transport_exhausted"
    assert record["parsed_output"] is None
    kinds = [a["status"] for a in record["attempts"]]
    assert kinds.count("provider_error") == 3, kinds
    assert record["attempts"][0]["billing_disposition"] == "provider_error_retry_exempt"
    assert record["attempts"][-1]["billing_disposition"] == "counted"


def test_unknown_error_is_recorded_without_transport_retry(wired, tmp_path: Path) -> None:
    """未知内部异常不得被误分类为 provider failure。"""

    wired([RuntimeError("local invariant failed")] * 6)
    record = runner.run_cell(
        case="0000", profile="fake", report_root=_corpus_stub(tmp_path), transport_retries=2
    )
    assert record["status"] == "failed"
    assert record["failure_class"] == "internal_error"
    assert len(record["attempts"]) == 1
    assert record["attempts"][0]["status"] == "internal_error"
    assert record["attempts"][0]["billing_disposition"] == "counted"


def test_transport_error_then_success(wired, tmp_path: Path) -> None:
    wired([_TransportBoom("429"), _ok_response(1)])
    record = runner.run_cell(case="0000", profile="fake", report_root=_corpus_stub(tmp_path))
    assert record["status"] == "ok"
    assert record["issue_count"] == 1


def test_responses_relay_upstream_receipt_is_retryable() -> None:
    class RelayedProviderError(Exception):
        body = {
            "error": {
                "code": "upstream_error",
                "message": "Upstream request failed request-id=fixture",
                "type": "new_api_error",
            }
        }

    assert runner._retryable_provider_error(RelayedProviderError()) is True


def test_schema_error_feeds_targeted_feedback_back(wired, tmp_path: Path) -> None:
    """⭐ schema 失败必须**原地重试并回灌定向反馈**，⛔ 不是冷启动重来。"""

    from pydantic import ValidationError

    try:
        NaiveReview(issues=[{"issue": "x", "where": "y"}])  # reason missing
    except ValidationError as exc:
        boom = exc
    else:  # pragma: no cover
        pytest.fail("expected a ValidationError to build the fixture")

    model = wired([boom, _ok_response(2)])
    record = runner.run_cell(case="0000", profile="fake", report_root=_corpus_stub(tmp_path))
    assert record["status"] == "ok"
    # 第二次调用的 user message 必须带上反馈，且反馈点名了字段路径。
    second = model._structured.calls[1]
    text = "".join(getattr(m, "content", "") for m in second)
    assert "did not satisfy the required output structure" in text
    assert "reason" in text
    assert record["attempts"][0]["status"] == "schema_error"


def test_schema_error_exhausted_is_recorded_as_a_defect(wired, tmp_path: Path) -> None:
    """⚠️ schema 穷尽失败允许整格失败，⛔ 但必须留下 failure_class 供追修。"""

    from pydantic import ValidationError

    try:
        NaiveReview(issues=[{"issue": "x"}])
    except ValidationError as exc:
        boom = exc
    else:  # pragma: no cover
        pytest.fail("expected a ValidationError to build the fixture")

    wired([boom] * 8)
    record = runner.run_cell(case="0000", profile="fake", report_root=_corpus_stub(tmp_path))
    assert record["status"] == "failed"
    assert record["failure_class"] == "schema_exhausted"


def test_write_record_is_stable_json(wired, tmp_path: Path) -> None:
    wired([_ok_response(1)])
    record = runner.run_cell(case="0000", profile="fake", report_root=_corpus_stub(tmp_path))
    path = runner.write_record(record, tmp_path / "out")
    import json

    reloaded = json.loads(path.read_text(encoding="utf-8"))
    assert reloaded["schema_version"] == runner.SCHEMA_VERSION
    assert reloaded["arm"] == "naive_baseline"


# --------------------------------------------------------------------------- 反馈纯度


def test_retry_feedback_is_purely_structural() -> None:
    feedback = runner.schema_retry_feedback(
        "1 validation error for NaiveReview\n"
        "issues.0.reason\n"
        "  Field required [type=missing, input_value={'issue': 'Idle state absent'}]"
    )
    assert "issues.0.reason" in feedback
    # ⛔ 模型自己写的内容片段不得被回灌成引导（这里是 'Idle state absent'）。
    assert "Idle" not in feedback
    assert "input_value" not in feedback


def _corpus_stub(tmp_path: Path) -> Path:
    root = tmp_path / "reports"
    pair = root / "pairs" / "0000"
    pair.mkdir(parents=True, exist_ok=True)
    (pair / "nl.txt").write_text("the system shall idle", encoding="utf-8")
    (pair / "plantuml.puml").write_text("@startuml\nstate Idle\n@enduml\n", encoding="utf-8")
    return root
