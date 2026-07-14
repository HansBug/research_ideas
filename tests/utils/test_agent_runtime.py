from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path

import pytest
from pydantic import Field
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessageChunk, ToolMessage
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from utils.agent import AgentApp, AgentError, AgentEvent, AgentSpec
from utils.llm import LLMConfig


class FakeStreamingModel:
    def __init__(self) -> None:
        self.calls = 0

    def bind_tools(self, tools, **kwargs):
        return self

    async def astream(self, messages, **kwargs):
        self.calls += 1
        if self.calls == 1:
            yield AIMessageChunk(
                content="",
                tool_call_chunks=[
                    {"name": "lookup", "args": '{"value": "ok"}', "id": "call-1", "index": 0}
                ],
            )
        else:
            yield AIMessageChunk(content="工具结果已读取")


def test_tool_call_and_academic_audit_are_exported(tmp_path: Path) -> None:
    def lookup(value: str) -> dict[str, str]:
        return {"value": value}

    app = AgentApp._for_test(
        AgentSpec(name="demo", system_prompt="use lookup", tools=(lookup,), require_tool_call=True),
        LLMConfig(model="gpt-5.5", api_key="key"),
        FakeStreamingModel(),
    )
    audit = tmp_path / "audit.jsonl"
    result_path = tmp_path / "result.json"
    events = []

    result = app.run("read", audit_out=audit, result_out=result_path, renderer="quiet", on_event=events.append)

    assert result.status == "success"
    assert result.academic_eligible is True
    assert result.tool_calls[0]["name"] == "lookup"
    assert [event.kind for event in events] == [
        "run_started",
        "model_started",
        "model_completed",
        "tool_started",
        "tool_completed",
        "context_usage",
        "model_started",
        "model_text",
        "model_completed",
        "context_usage",
        "completed",
    ]
    records = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
    assert [record["record"] for record in records] == ["context", "decision", "action", "context", "decision", "context", "finish"]
    assert all("heartbeat" not in record for record in records)
    assert json.loads(result_path.read_text(encoding="utf-8"))["status"] == "success"
    assert {"tool_call_id", "status"}.issubset(result.tool_calls[0])


def test_tool_events_keep_standard_call_metadata() -> None:
    def lookup(value: str) -> dict[str, str]:
        """Look up one value from the test fixture."""
        return {"value": value}

    events = []
    AgentApp._for_test(
        AgentSpec(name="tool-metadata", system_prompt="use lookup", tools=(lookup,), require_tool_call=True),
        LLMConfig(model="gpt-5.5"),
        FakeStreamingModel(),
    ).run("read", renderer="quiet", on_event=events.append)

    started = next(event for event in events if event.kind == "tool_started")
    completed = next(event for event in events if event.kind == "tool_completed")
    for event, status in ((started, "started"), (completed, "completed")):
        assert event.data["name"] == "lookup"
        assert event.data["tool_call_id"] == "call-1"
        assert event.data["status"] == status
        assert "arguments" in event.data
    assert completed.data["result"] == {"value": "ok"}


def test_next_model_prompt_shows_tool_inputs_without_assistant_history() -> None:
    def lookup(value: str) -> dict[str, str]:
        return {"value": value}

    events = []
    AgentApp._for_test(
        AgentSpec(name="prompt-history", system_prompt="use lookup", tools=(lookup,), require_tool_call=True),
        LLMConfig(model="gpt-5.5", api_key="key"),
        FakeStreamingModel(),
    ).run("read", renderer="quiet", on_event=events.append)
    prompts = [event.data["prompt"] for event in events if event.kind == "model_started"]
    assert len(prompts) == 2
    assert "[tool]" in prompts[1]
    assert "[assistant]" not in prompts[1]


def test_missing_audit_is_not_academic_eligible() -> None:
    def lookup(value: str) -> dict[str, str]:
        return {"value": value}

    app = AgentApp._for_test(
        AgentSpec(name="plain", system_prompt="answer", tools=(lookup,)),
        LLMConfig(model="gpt-5.5", api_key="key"),
        FakeStreamingModel(),
    )
    result = app.run("answer", renderer="quiet")
    assert result.status == "success"
    assert result.academic_eligible is False


def test_invalid_context_emits_structured_failure_and_audit_finish(tmp_path: Path) -> None:
    app = AgentApp._for_test(
        AgentSpec(name="invalid-context", system_prompt="answer"),
        LLMConfig(model="gpt-5.5"),
        FakeStreamingModel(),
    )
    events: list[AgentEvent] = []
    audit = tmp_path / "invalid-context.jsonl"
    result = app.run(
        "answer",
        context=[{"id": "bad", "hash": "sha256:not-the-text-hash", "text": "facts"}],
        renderer="quiet",
        audit_out=audit,
        on_event=events.append,
    )

    assert result.status == "failed"
    assert result.error is not None
    assert result.error["code"] == "context_invalid"
    assert [event.kind for event in events] == ["run_started", "context_failed", "failed"]
    records = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
    assert records[0]["record"] == "context"
    assert records[-1]["record"] == "finish"
    assert records[-1]["error"]["code"] == "context_invalid"


class _TwoToolModel(BaseChatModel):
    calls: int = Field(default=0)

    @property
    def _llm_type(self) -> str:
        return "two-tool-test"

    def bind_tools(self, tools, **kwargs):
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        self.calls += 1
        tool_calls = []
        if self.calls == 1:
            tool_calls = [
                {"name": "first", "args": {}, "id": "call-first", "type": "tool_call"},
                {"name": "second", "args": {}, "id": "call-second", "type": "tool_call"},
            ]
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content="done", tool_calls=tool_calls))])


def test_multiple_registered_tools_are_allowed_without_default_limit() -> None:
    calls: list[str] = []

    def first() -> str:
        """first tool."""
        calls.append("first")
        return "one"

    def second() -> str:
        """second tool."""
        calls.append("second")
        return "two"

    result = AgentApp._for_test(
        AgentSpec(name="multi", system_prompt="use both", tools=(first, second)),
        LLMConfig(model="gpt-5.5"),
        _TwoToolModel(),
    ).run("run", renderer="quiet")

    assert result.status == "success"
    assert sorted(calls) == ["first", "second"]
    assert sorted(item["name"] for item in result.tool_calls) == ["first", "second"]


def test_graph_recursion_safeguard_is_not_an_implicit_agent_budget() -> None:
    from utils.agent.runtime import _DEFAULT_GRAPH_RECURSION_LIMIT, _graph_recursion_limit

    assert _graph_recursion_limit(AgentSpec(name="unbounded", system_prompt="answer")) == _DEFAULT_GRAPH_RECURSION_LIMIT
    assert _DEFAULT_GRAPH_RECURSION_LIMIT > 25
    assert _graph_recursion_limit(AgentSpec(name="bounded", system_prompt="answer", limits={"turns": 3})) >= 100


def test_demo_forwards_only_explicit_limits(monkeypatch: pytest.MonkeyPatch) -> None:
    from utils.agent import demo

    captured: dict[str, object] = {}

    class Registry:
        def require(self, name: str) -> LLMConfig:
            return LLMConfig(model=name, api_key="key")

    class Result:
        status = "failed"
        error = {"code": "stop", "message": "captured"}

    class App:
        def run(self, *_args: object, **kwargs: object) -> Result:
            captured["input"] = _args[0]
            captured["run"] = kwargs
            return Result()

    def make_app(spec: AgentSpec, *_args: object, **_kwargs: object) -> App:
        captured["spec"] = spec
        return App()

    monkeypatch.setattr(demo, "load_llm_registry", lambda _path: Registry())
    monkeypatch.setattr(demo.AgentApp, "from_config", staticmethod(make_app))
    with pytest.raises(Exception):
        demo.cli.main(args=["--renderer", "quiet"], standalone_mode=False)
    assert captured["spec"].limits == {}
    assert captured["input"] == "请计算当前系统时间 (2 * 24) + 3 + (15 / 60) 小时后的美国东部时间。"
    assert "51.25" not in captured["spec"].system_prompt

    captured.clear()
    with pytest.raises(Exception):
        demo.cli.main(
            args=[
                "--renderer",
                "quiet",
                "--max-model-calls",
                "2",
                "--max-tool-calls",
                "5",
                "--max-turns",
                "3",
                "--max-seconds",
                "12.5",
            ],
            standalone_mode=False,
        )
    assert captured["spec"].limits == {"model_calls": 2, "tool_calls": 5, "turns": 3, "seconds": 12.5}


def test_demo_expression_tool_supports_numeric_modulo_only() -> None:
    from utils.agent.demo import _calculate_expression

    assert _calculate_expression("66.083333 % 24")["value"] == pytest.approx(18.083333)
    with pytest.raises((SyntaxError, ValueError)):
        _calculate_expression("2026-07-13T14:52:09-04:00 + 51.25 hours")


def test_explicit_tool_limit_blocks_before_tool_node() -> None:
    called = False

    def first() -> str:
        """first tool."""
        nonlocal called
        called = True
        return "one"

    def second() -> str:
        """second tool."""
        return "two"

    result = AgentApp._for_test(
        AgentSpec(name="bounded", system_prompt="use both", tools=(first, second), limits={"tool_calls": 1}),
        LLMConfig(model="gpt-5.5"),
        _TwoToolModel(),
    ).run("run", renderer="quiet")

    assert result.status == "failed"
    assert result.error is not None
    assert result.error["code"] == "limit_exceeded"
    assert result.error["message"] == "tool_calls limit exceeded"
    assert called is False


class _RepeatToolModel(BaseChatModel):
    calls: int = Field(default=0)

    @property
    def _llm_type(self) -> str:
        return "repeat-tool-test"

    def bind_tools(self, tools, **kwargs):
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        self.calls += 1
        if self.calls <= 2:
            tool_calls = [{"name": "probe", "args": {}, "id": f"probe-{self.calls}", "type": "tool_call"}]
        else:
            tool_calls = []
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content="done", tool_calls=tool_calls))])


def test_same_arguments_in_same_attempt_are_not_replayed() -> None:
    executions: list[int] = []

    def probe() -> str:
        """probe current state."""
        executions.append(1)
        return f"value-{len(executions)}"

    result = AgentApp._for_test(
        AgentSpec(name="repeat", system_prompt="probe twice", tools=(probe,)),
        LLMConfig(model="gpt-5.5"),
        _RepeatToolModel(),
    ).run("run", renderer="quiet")

    assert result.status == "success"
    assert executions == [1, 1]
    assert len(result.tool_calls) == 2
    assert {item["tool_call_id"] for item in result.tool_calls} == {"probe-1", "probe-2"}


def test_operator_events_redact_secret_values() -> None:
    class _TextModel(BaseChatModel):
        @property
        def _llm_type(self) -> str:
            return "text-test"

        def bind_tools(self, tools, **kwargs):
            return self

        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            return ChatResult(generations=[ChatGeneration(message=AIMessage(content="done"))])

    events = []
    AgentApp._for_test(
        AgentSpec(name="redact", system_prompt="DO_NOT_LEAK_SYSTEM", tools=()),
        LLMConfig(model="gpt-5.5"),
        _TextModel(),
    ).run("sk-abcdefghijklmnop123456", renderer="quiet", on_event=events.append)

    serialized = json.dumps([event.to_dict() for event in events], ensure_ascii=False)
    assert "sk-abcdefghijklmnop123456" not in serialized
    assert "DO_NOT_LEAK_SYSTEM" in serialized


def test_redaction_handles_secret_prefix_case_without_hiding_usage() -> None:
    from utils.agent.runtime import _redact

    value = {
        "message": "SK-UPPERCASE12345678 SESS-MixedCase12345678",
        "token_usage": {"prompt_tokens": 7, "completion_tokens": 2},
        "prompt_tokens_details": {"cached_tokens": 1},
        "completion_tokens_details": {"reasoning_tokens": 3},
        "input_token_details": {"cached_tokens": 4},
        "output_token_details": {"reasoning_tokens": 5},
        "secret_value": "hidden",
        "api_key_value": "hidden-too",
        "password_hash": "hidden-hash",
        "my_token": "hidden-token",
        "api_key_configured": True,
    }
    redacted = _redact(value)
    serialized = json.dumps(redacted, ensure_ascii=False)
    assert "SK-UPPERCASE12345678" not in serialized
    assert "SESS-MixedCase12345678" not in serialized
    assert redacted["token_usage"] == {"prompt_tokens": 7, "completion_tokens": 2}
    assert redacted["prompt_tokens_details"] == {"cached_tokens": 1}
    assert redacted["completion_tokens_details"] == {"reasoning_tokens": 3}
    assert redacted["input_token_details"] == {"cached_tokens": 4}
    assert redacted["output_token_details"] == {"reasoning_tokens": 5}
    assert redacted["secret_value"] == "[redacted]"
    assert redacted["api_key_value"] == "[redacted]"
    assert redacted["password_hash"] == "[redacted]"
    assert redacted["my_token"] == "[redacted]"
    assert redacted["api_key_configured"] is True


def test_redaction_keeps_research_ids_and_scrubs_provider_tokens_and_url_credentials() -> None:
    from utils.agent.runtime import _redact

    value = (
        "key-research-153 https://example.org/docs?topic=agent&api_key=sk-live-secret-123456 "
        "hf_abcdefghijklmnopqrstuvwxyz123456 ghp_abcdefghijklmnopqrstuvwxyz123456"
    )
    redacted = _redact(value)
    assert "key-research-153" in redacted
    assert "example.org/docs" in redacted
    assert "sk-live-secret-123456" not in redacted
    assert "api_key=%5Bredacted%5D" in redacted
    assert "hf_abcdefghijklmnopqrstuvwxyz123456" not in redacted
    assert "ghp_abcdefghijklmnopqrstuvwxyz123456" not in redacted


def test_stream_holdback_does_not_delay_ordinary_text_but_holds_split_credentials() -> None:
    from utils.agent.runtime import _StreamHoldback

    ordinary = _StreamHoldback(())
    assert ordinary.feed("ordinary output") == "ordinary output"
    assert ordinary.withheld_chars == 0

    secret = "sk-configured-secret-12345678"
    streamed = _StreamHoldback((secret,))
    assert streamed.feed("prefix ") == "prefix "
    assert streamed.feed("sk-conf") == ""
    assert streamed.feed("igured-secret-12345678", final=True) == "[redacted_secret]"

    delimited = _StreamHoldback(())
    assert delimited.feed("sk-id ") == "sk-id "

    for prefix, suffix in (("Bearer", " token12345"), ("sk", "-abcdefghijklmnopqrstuv"), ("hf", "_abcdefghijklmnopqrstuvwxyz123456")):
        split = _StreamHoldback(())
        assert split.feed(prefix) == ""
        assert suffix.strip() not in split.feed(suffix, final=True)

    bearer = _StreamHoldback(())
    assert bearer.feed("Bearer ") == ""
    assert bearer.feed("token12345", final=True) == "Bearer [redacted_bearer]"

    for first, second, secret_fragment in (
        ("https://user", ":pass@host/x", ":pass@"),
        ("https://x/?api_key=", "supersecret123", "supersecret123"),
        ("ht", "tps://user:pass@host/x", ":pass@"),
    ):
        url = _StreamHoldback(())
        assert url.feed(first) == ""
        rendered = url.feed(second, final=True)
        assert secret_fragment not in rendered


def test_redaction_handles_truncated_credential_fingerprints_without_hiding_ids() -> None:
    from utils.agent.runtime import _redact_text, _redact_with_inventory

    secret = "sk-conf-abcdefghijklmnopqrstuv12345678"
    assert "sk-conf...5678" not in _redact_text("provider rejected key sk-conf...5678")
    for text in (
        "invalid key ending ...5678",
        "OpenAI error: api_key ...5678 is invalid",
        "invalid api key '...5678'",
        "The provided API key ...5678 was rejected",
        "key ...5678 expired",
    ):
        assert "5678" not in _redact_with_inventory(text, (secret,))
    assert _redact_with_inventory("key-research-153", (secret,)) == "key-research-153"
    for text in ("key research ...5678", "key-research-153 ...5678", "token budget ...5678"):
        assert _redact_with_inventory(text, (secret,)) == text


def test_redaction_covers_known_provider_token_formats_without_generic_hiding() -> None:
    from utils.agent.runtime import _redact_text, _StreamHoldback

    tokens = (
        "xai-abcdefghij1234567890abcdefghijkl",
        "gsk_abcdefghij1234567890abcdefghij",
        "pplx-abcdefghij1234567890abcdef",
        "tgp_v1_abcdefghij1234567890abcdefghij",
        "fw_abcdefghij1234567890abcdefgh",
        "mist-abcdefghij1234567890abcdef",
        "r8_abcdefghij1234567890abcdef",
    )
    for token in tokens:
        assert token not in _redact_text(f"provider token {token}")
        prefix = token[:3]
        streamed = _StreamHoldback(())
        assert streamed.feed(f"auth {prefix}") == ""
        assert token not in streamed.feed(token[3:], final=True)
    for label, token in (
        ("api_key=", "xai-abcdefghij1234567890abcdefghijkl"),
        ("token=", "tgp_v1_abcdefghij1234567890abcdefghij"),
        ("auth:", "fw_abcdefghij1234567890abcdefgh"),
        ("authorization=", "mist-abcdefghij1234567890abcdef"),
    ):
        streamed = _StreamHoldback(())
        assert streamed.feed(label + token[:3]) == ""
        assert token not in streamed.feed(token[3:], final=True)
    assert _redact_text("key-research-153") == "key-research-153"
    assert _redact_text("the bearer of the message") == "the bearer of the message"
    for run_id in (
        "gsk_baseline_v1_epoch_100",
        "fw_ablation_run_smoke",
        "sk-branch-152",
        "tgp_v1_train_epoch_000042",
    ):
        assert _redact_text(run_id) == run_id


def test_redaction_covers_anthropic_and_openai_project_tokens_without_hiding_ids() -> None:
    from utils.agent.runtime import _StreamHoldback, _redact_text

    tokens = (
        "sk-ant-api03-abcdefghijklmnopqrstuvwxyz1234567890",
        "sk-proj-abcdefghijklmnopqrstuvwxyz1234567890",
    )
    for token in tokens:
        assert token not in _redact_text(f"provider token {token}")
        streamed = _StreamHoldback(())
        assert streamed.feed(f"response {token[:9]}") == "response "
        assert token not in streamed.feed(token[9:], final=True)

    for token in ("sk-ant-api03-real...5678", "sk-proj-abcdef012...5678"):
        assert "5678" not in _redact_text(f"provider rejected {token}")

    for academic_id in ("sk-ant-baseline-1", "sk-project-plan-2026"):
        assert _redact_text(academic_id) == academic_id


def test_bearer_redaction_keeps_plain_english_phrases() -> None:
    from utils.agent.runtime import _redact_text

    assert _redact_text("Standard bearer authentication is required") == "Standard bearer authentication is required"
    assert _redact_text("bearer credentials required") == "bearer credentials required"
    assert _redact_text("the bearer instrument was returned") == "the bearer instrument was returned"
    assert "token12345" not in _redact_text("Bearer token12345")
    assert "opaque-token-123" not in _redact_text("Bearer opaque-token-123")


def test_compact_threshold_uses_official_input_window_without_output_subtraction() -> None:
    from utils.agent.runtime import _model_capacity

    context, output, safe_input, _sources = _model_capacity(
        object(), LLMConfig(model="gpt-5.5", context_window_tokens=1_050_000, max_output_tokens=128_000)
    )
    assert context == 1_050_000
    assert output == 128_000
    assert safe_input == 1_050_000


def test_redaction_handles_unseparated_google_and_aws_fingerprints() -> None:
    from utils.agent.runtime import _redact_text

    assert "AKIAIOSF...MPLE" not in _redact_text("AKIAIOSF...MPLE was rejected")
    assert "AIzaSyABC...WXYZ" not in _redact_text("AIzaSyABC...WXYZ rate limit")


def test_redaction_preserves_non_secret_headers_and_redacts_header_credentials() -> None:
    from utils.agent.runtime import _redact, _redact_with_inventory

    headers = {
        "Content-Type": "application/json",
        "X-Request-Id": "req-123",
        "Authorization": "Bearer abcdefgh123456",
        "X-Api-Key": "sk-abcdefghijklmnop123456",
    }
    expected = {
        "Content-Type": "application/json",
        "X-Request-Id": "req-123",
        "Authorization": "[redacted]",
        "X-Api-Key": "[redacted]",
    }
    assert _redact({"headers": headers}) == {"headers": expected}
    assert _redact_with_inventory({"headers": headers}, ()) == {"headers": expected}


def test_usage_conflict_includes_cache_and_reasoning_details() -> None:
    from utils.agent.runtime import _model_usage_info

    class _Usage:
        llm_output = {"token_usage": {"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12, "cached_tokens": 1, "reasoning_tokens": 3}}

    message = AIMessage(
        content="done",
        usage_metadata={
            "input_tokens": 10,
            "output_tokens": 2,
            "total_tokens": 12,
            "input_token_details": {"cache_read": 7},
            "output_token_details": {"reasoning": 3},
        },
    )
    _Usage.generations = [[ChatGeneration(message=message)]]
    _, _, conflict, _ = _model_usage_info(_Usage())
    assert conflict is True


def test_model_usage_and_observed_model_are_read_from_chat_model_end() -> None:
    class _UsageModel(BaseChatModel):
        @property
        def _llm_type(self) -> str:
            return "usage-test"

        def bind_tools(self, tools, **kwargs):
            return self

        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            return ChatResult(
                generations=[
                    ChatGeneration(
                        message=AIMessage(
                            content="done",
                            response_metadata={
                                "token_usage": {"prompt_tokens": 7, "completion_tokens": 2},
                                "model_name": "provider-model",
                            },
                        )
                    )
                ]
            )

    result = AgentApp._for_test(
        AgentSpec(name="usage", system_prompt="answer"),
        LLMConfig(model="configured-model"),
        _UsageModel(),
    ).run("run", renderer="quiet")

    assert result.status == "success"
    assert result.usage[0]["input_tokens"] == 7
    assert result.usage[0]["output_tokens"] == 2
    assert result.usage[0]["source"] == "provider"
    assert result.observed_model == "provider-model"


def test_model_usage_reads_public_llm_output_token_usage() -> None:
    from utils.agent.runtime import _model_usage_info

    value = ChatResult(
        generations=[ChatGeneration(message=AIMessage(content="done"))],
        llm_output={"token_usage": {"prompt_tokens": 11, "completion_tokens": 3}, "model_name": "provider-model"},
    )
    usage, observed, conflict, model = _model_usage_info(value)
    assert usage == {"prompt_tokens": 11, "completion_tokens": 3}
    assert observed[0]["source"] == "llm_output.token_usage"
    assert conflict is False
    assert model == "provider-model"


def test_model_text_is_not_rewritten_by_runtime_postprocessing() -> None:
    class _RawTextModel(BaseChatModel):
        @property
        def _llm_type(self) -> str:
            return "raw-text-test"

        def bind_tools(self, tools, **kwargs):
            return self

        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            return ChatResult(generations=[ChatGeneration(message=AIMessage(content="<analysis>visible</analysis>\\nanswer"))])

    events = []
    result = AgentApp._for_test(
        AgentSpec(name="raw-output", system_prompt="answer", tools=()),
        LLMConfig(model="gpt-5.5"),
        _RawTextModel(),
    ).run("run", renderer="quiet", on_event=events.append)

    assert result.status == "success"
    assert result.final_text == "<analysis>visible</analysis>\\nanswer"
    assert next(event for event in events if event.kind == "model_text").data["text"] == result.final_text


def test_hidden_thinking_blocks_are_excluded_from_academic_audit(tmp_path: Path) -> None:
    class _ThinkingModel(BaseChatModel):
        @property
        def _llm_type(self) -> str:
            return "thinking-test"

        def bind_tools(self, tools, **kwargs):
            return self

        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            return ChatResult(
                generations=[
                    ChatGeneration(
                        message=AIMessage(
                            content=[
                                {"type": "thinking", "thinking": "PRIVATE-CHAIN"},
                                {"type": "text", "text": "visible answer"},
                            ]
                        )
                    )
                ]
            )

    audit = tmp_path / "audit.jsonl"
    result = AgentApp._for_test(
        AgentSpec(name="thinking-audit", system_prompt="answer"),
        LLMConfig(model="gpt-5.5"),
        _ThinkingModel(),
    ).run("run", renderer="quiet", audit_out=audit)

    assert result.status == "success"
    serialized = audit.read_text(encoding="utf-8")
    assert "PRIVATE-CHAIN" not in serialized
    assert "visible answer" in serialized


def test_result_export_redacts_secret_tool_values() -> None:
    def lookup(value: str) -> dict[str, str]:
        return {"value": value, "token": "sk-abcdefghijklmnop123456"}

    result = AgentApp._for_test(
        AgentSpec(name="result-redact", system_prompt="use lookup", tools=(lookup,), require_tool_call=True),
        LLMConfig(model="gpt-5.5", api_key="key"),
        FakeStreamingModel(),
    ).run("read", renderer="quiet")

    assert "sk-abcdefghijklmnop123456" not in result.to_json()
    assert result.tool_calls[0]["result"]["token"] == "[redacted]"
    assert "sk-abcdefghijklmnop123456" not in json.dumps(result.tool_calls, ensure_ascii=False)


def test_tool_result_preserves_scalar_text_but_decodes_structured_json() -> None:
    from utils.agent.runtime import _tool_result_value

    scalar = ToolMessage(content="123", name="probe", tool_call_id="scalar")
    structured = ToolMessage(content='{"value": 123}', name="probe", tool_call_id="structured")
    assert _tool_result_value(scalar) == "123"
    assert _tool_result_value(structured) == {"value": 123}


def test_exception_details_redact_endpoint_and_bearer_token() -> None:
    from utils.agent.runtime import _exception_details

    class ProviderError(Exception):
        status_code = 401
        code = "unauthorized"
        request_id = "req-1"
        body = {
            "message": "Bearer opaque-token-123 https://provider.invalid/v1/chat/completions",
            "type": "invalid_request_error",
            "param": None,
        }

    details = _exception_details(ProviderError("Bearer opaque-token-123 https://provider.invalid/v1"))
    serialized = json.dumps(details, ensure_ascii=False)
    assert "opaque-token-123" not in serialized
    assert "provider.invalid" not in serialized
    assert details["status_code"] == 401
    assert details["request_id"] == "req-1"
    assert "Bearer [redacted_bearer]" in details["message"]
    assert "[redacted_endpoint]" in details["message"]


def test_provider_timeout_is_not_reported_as_agent_budget() -> None:
    class ProviderStreamTimeout(asyncio.TimeoutError):
        __module__ = "openai._exceptions"

    class _TimeoutModel(BaseChatModel):
        @property
        def _llm_type(self) -> str:
            return "provider-timeout-test"

        def bind_tools(self, tools, **kwargs):
            return self

        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            raise ProviderStreamTimeout("provider stream timed out")

    result = AgentApp._for_test(
        AgentSpec(name="provider-timeout", system_prompt="answer"),
        LLMConfig(model="gpt-5.5"),
        _TimeoutModel(),
    ).run("run", renderer="quiet")

    assert result.status == "failed"
    assert result.error is not None
    assert result.error["code"] == "provider_error"


def test_cancelled_run_has_structured_status_and_audit_finish(tmp_path: Path) -> None:
    class _SlowModel(BaseChatModel):
        @property
        def _llm_type(self) -> str:
            return "slow-test"

        def bind_tools(self, tools, **kwargs):
            return self

        async def _agenerate(self, messages, stop=None, run_manager=None, **kwargs):
            await asyncio.sleep(60)
            return ChatResult(generations=[ChatGeneration(message=AIMessage(content="never"))])

        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            raise AssertionError("the async test model must use _agenerate")

    async def cancel_run() -> object:
        audit = tmp_path / "cancelled.jsonl"
        task = asyncio.create_task(
            AgentApp._for_test(
                AgentSpec(name="cancelled", system_prompt="answer"),
                LLMConfig(model="gpt-5.5"),
                _SlowModel(),
            ).arun("run", renderer="quiet", audit_out=audit)
        )
        await asyncio.sleep(0.05)
        task.cancel()
        return await task

    result = asyncio.run(cancel_run())
    assert result.status == "cancelled"
    assert result.error == {"code": "cancelled", "message": "agent run was cancelled"}
    records = [json.loads(line) for line in (tmp_path / "cancelled.jsonl").read_text(encoding="utf-8").splitlines()]
    assert records[-1]["record"] == "finish"
    assert records[-1]["status"] == "cancelled"


def test_redaction_preserves_normal_urls_in_model_content() -> None:
    from utils.agent.runtime import _redact

    value = "参考 https://example.org/docs 完成任务"
    assert _redact(value) == value
    assert _redact({"url": "https://example.org/docs"}) == {"url": "https://example.org/docs"}
    assert _redact({"api_url": "https://provider.invalid/v1"}) == {"api_url": "[redacted_endpoint]"}


def test_invalid_audit_path_is_structured_error(tmp_path: Path) -> None:
    def lookup() -> str:
        """lookup."""
        return "ok"

    app = AgentApp._for_test(
        AgentSpec(name="audit-path", system_prompt="answer", tools=(lookup,)),
        LLMConfig(model="gpt-5.5"),
        FakeStreamingModel(),
    )
    with pytest.raises(AgentError, match="audit_write_failed"):
        app.run("answer", renderer="quiet", audit_out=tmp_path)


def test_audit_finalize_failure_returns_structured_failed_result(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    def lookup() -> str:
        """lookup."""
        return "ok"

    app = AgentApp._for_test(
        AgentSpec(name="audit-finalize", system_prompt="answer", tools=(lookup,)),
        LLMConfig(model="gpt-5.5"),
        FakeStreamingModel(),
    )

    def fail_close(_audit: object) -> None:
        raise AgentError("audit_write_failed", "audit output could not be finalized")

    from utils.agent import runtime

    monkeypatch.setattr(runtime._AuditWriter, "close", fail_close)
    result = app.run("answer", renderer="quiet", audit_out=tmp_path / "audit.jsonl")
    assert result.status == "failed"
    assert result.error == {"code": "audit_write_failed", "message": "audit output could not be finalized"}
    assert result.academic_eligible is False


def test_rich_renderer_marks_turns_and_completion() -> None:
    from rich.console import Console
    from utils.agent.runtime import _Renderer

    output = StringIO()
    renderer = _Renderer("rich", "INFO", "run-rich")
    renderer.console = Console(file=output, force_terminal=False, color_system=None)
    now = datetime.now(timezone.utc)
    renderer.render(AgentEvent("run-rich", 1, now, "model_started", {"turn": 1, "prompt": "hello"}))
    renderer.render(AgentEvent("run-rich", 2, now, "model_text", {"turn": 1, "text": "answer"}))
    renderer.render(AgentEvent("run-rich", 3, now, "model_completed", {"turn": 1, "tool_count": 0}))
    renderer.render(AgentEvent("run-rich", 4, now, "structured_output", {"output": {"ok": True}}))
    renderer.render(AgentEvent("run-rich", 5, now, "completed", {"model": "gpt-5.5", "output": {"ok": True}, "final_text": '{"ok": true}'}))
    rendered = output.getvalue()
    assert "TURN 1 | MODEL INPUT" in rendered
    assert "MODEL OUTPUT | ASSISTANT" in rendered
    assert "assistant: answer" not in rendered
    assert "AGENT COMPLETE" in rendered
    assert "SUCCESS" in rendered
    assert "result:" in rendered
    assert rendered.count("{'ok': True}") == 1


def test_rich_agent_run_panel_exposes_behavior_fingerprints_without_raw_prompt() -> None:
    from rich.console import Console
    from utils.agent.runtime import _Renderer

    output = StringIO()
    renderer = _Renderer("rich", "INFO", "run-config")
    renderer.console = Console(file=output, force_terminal=False, color_system=None)
    now = datetime.now(timezone.utc)
    renderer.render(
        AgentEvent(
            "run-config",
            1,
            now,
            "run_started",
            {
                "agent": "demo",
                "profile": "gpt-5.5",
                "model": "gpt-5.5",
                "real_llm": True,
                "adapter": "langchain-openai/chat-completions",
                "streaming": True,
                "stream_usage": True,
                "think_mode": False,
                "reasoning_effort": "none",
                "system_prompt_hash": "sha256:" + "a" * 64,
                "tools_hash": "sha256:" + "b" * 64,
                "input_hash": "sha256:" + "c" * 64,
                "context_manifest_hash": None,
                "tools": ["probe"],
                "limits": {},
                "compact": {"enabled": True, "trigger_ratio": 0.85, "threshold": 800, "keep_messages": 20},
            },
        )
    )
    rendered = output.getvalue()
    assert "behavior" in rendered
    assert "system=sha256:aaaaaaaaaaaa" in rendered
    assert "prompt" not in rendered.lower()


def test_rich_completion_panel_keeps_full_result() -> None:
    from rich.console import Console
    from utils.agent.runtime import _Renderer

    output = StringIO()
    renderer = _Renderer("rich", "INFO", "run-full-result")
    renderer.console = Console(file=output, force_terminal=False, color_system=None)
    now = datetime.now(timezone.utc)
    payload = "x" * 5001
    renderer.render(
        AgentEvent(
            "run-full-result",
            1,
            now,
            "completed",
            {"model": "gpt-5.5", "output": payload, "final_text": payload},
        )
    )
    rendered = output.getvalue()
    # Rich wraps long unbroken text across panel lines; every character must
    # still be present in the final panel.
    assert rendered.count("x") == len(payload)
    assert "中间省略" not in rendered


def test_rich_renderer_shows_structured_call_and_result_in_output_phase() -> None:
    from rich.console import Console
    from utils.agent.runtime import _Renderer

    output = StringIO()
    renderer = _Renderer("rich", "INFO", "run-structured")
    renderer.console = Console(file=output, force_terminal=False, color_system=None)
    now = datetime.now(timezone.utc)
    renderer.render(AgentEvent("run-structured", 1, now, "model_started", {"turn": 1, "prompt": "go"}))
    renderer.render(
        AgentEvent(
            "run-structured",
            2,
            now,
            "model_completed",
            {
                "turn": 1,
                "tool_count": 1,
                "output": "",
                "structured_request": {
                    "kind": "structured",
                    "name": "Answer",
                    "tool_call_id": "structured-1",
                    "status": "requested",
                    "arguments": {"answer": "ok"},
                },
            },
        )
    )
    renderer.render(AgentEvent("run-structured", 3, now, "structured_output", {"output": {"answer": "ok"}}))
    rendered = output.getvalue()
    assert "MODEL OUTPUT | STRUCTURED CALL" in rendered
    assert "MODEL OUTPUT | STRUCTURED RESULT" not in rendered
    assert "status: requested" in rendered
    assert "structured-1" in rendered
    assert "purpose:" not in rendered
    assert "STRUCTURE RESULT VALIDATED" not in rendered


def test_rich_renderer_preserves_input_output_tool_timing() -> None:
    from rich.console import Console
    from utils.agent.runtime import _Renderer

    output = StringIO()
    renderer = _Renderer("rich", "DEBUG", "run-order")
    renderer.console = Console(file=output, force_terminal=False, color_system=None)
    now = datetime.now(timezone.utc)
    sequence = [
        AgentEvent("run-order", 1, now, "model_started", {"turn": 1, "prompt": "user input"}),
        AgentEvent("run-order", 2, now, "model_completed", {"turn": 1, "tool_count": 1}),
        AgentEvent("run-order", 3, now, "tool_started", {"name": "probe", "arguments": {}, "tool_call_id": "call-1"}),
        AgentEvent("run-order", 4, now, "tool_completed", {"name": "probe", "result": {"value": 1}}),
        AgentEvent("run-order", 5, now, "model_started", {"turn": 2, "prompt": "[tool] {\"value\": 1}"}),
        AgentEvent("run-order", 6, now, "model_text", {"turn": 2, "text": "answer"}),
        AgentEvent("run-order", 7, now, "model_completed", {"turn": 2, "tool_count": 0}),
        AgentEvent("run-order", 8, now, "structured_output", {"output": {"answer": "answer"}}),
        AgentEvent("run-order", 9, now, "completed", {"model": "gpt-5.5", "output": {"answer": "answer"}, "final_text": '{"answer":"answer"}'}),
        AgentEvent("run-order", 10, now, "heartbeat", {"elapsed_seconds": 1.0, "attempt_id": "attempt-1"}),
    ]
    for event in sequence:
        renderer.render(event)
    rendered = output.getvalue()
    markers = [
        "TURN 1 | MODEL INPUT",
        "TURN 1 | MODEL OUTPUT",
        "MODEL OUTPUT | TOOL CALL",
        "TOOL RESULT -> NEXT MODEL INPUT",
        "TURN 2 | MODEL INPUT",
        "TURN 2 | MODEL OUTPUT",
        "MODEL OUTPUT | ASSISTANT",
        "AGENT COMPLETE",
        "HEARTBEAT",
    ]
    positions = [rendered.index(marker) for marker in markers]
    assert positions == sorted(positions)
    assert "assistant: answer" not in rendered
    assert "INFO" not in rendered
    assert "DEBUG" not in rendered


def test_system_prompt_is_forwarded_without_runtime_suffix() -> None:
    class _CaptureModel(BaseChatModel):
        captured: list[object] = Field(default_factory=list)

        @property
        def _llm_type(self) -> str:
            return "capture"

        def bind_tools(self, tools, **kwargs):
            return self

        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            self.captured = list(messages)
            return ChatResult(generations=[ChatGeneration(message=AIMessage(content="done"))])

    model = _CaptureModel()
    system_prompt = "Use the exact experiment protocol."
    result = AgentApp._for_test(
        AgentSpec(name="prompt-identity", system_prompt=system_prompt),
        LLMConfig(model="gpt-5.5"),
        model,
    ).run("raw task", renderer="quiet")
    assert result.status == "success"
    system_messages = [message for message in model.captured if getattr(message, "type", "") == "system"]
    assert len(system_messages) == 1
    assert system_messages[0].content == system_prompt
    human_messages = [message for message in model.captured if getattr(message, "type", "") == "human"]
    assert len(human_messages) == 1
    assert human_messages[0].content == "raw task"


def test_demo_profile_defaults_to_gpt_but_accepts_other_configured_model(monkeypatch: pytest.MonkeyPatch) -> None:
    from utils.agent import demo
    from utils.agent.demo import DemoAnswer

    class Registry:
        def require(self, name: str) -> LLMConfig:
            assert name == "research-model"
            return LLMConfig(model="research-model", api_key="key")

    class Result:
        status = "success"
        real_llm = True
        academic_eligible = True
        model = "research-model"
        observed_model = "research-model"
        final_text = "51.25 hours"
        tool_calls = [
            {"name": "current_system_time", "status": "completed"},
            {"name": "calculate_expression", "status": "completed"},
        ]

        def require_output(self) -> DemoAnswer:
            return DemoAnswer(
                summary="51.25 hours",
                base_time="2026-07-13T11:15:25-04:00",
                offset_hours=51.25,
                target_time="2026-07-15T14:30:25-04:00",
                evidence_ids=["system-time-001", "math-expression-001"],
            )

    class App:
        def run(self, *_args: object, **_kwargs: object) -> Result:
            return Result()

    monkeypatch.setattr(demo, "load_llm_registry", lambda _path: Registry())
    monkeypatch.setattr(demo.AgentApp, "from_config", staticmethod(lambda *_args, **_kwargs: App()))
    demo.cli.main(
        args=["--profile", "research-model", "--renderer", "quiet"],
        standalone_mode=False,
    )


def test_demo_rejects_result_without_academic_audit(monkeypatch: pytest.MonkeyPatch) -> None:
    import click
    from utils.agent import demo

    class Registry:
        def require(self, name: str) -> LLMConfig:
            return LLMConfig(model=name, api_key="key")

    class Result:
        status = "success"
        real_llm = True
        academic_eligible = False
        model = "research-model"
        observed_model = "research-model"
        tool_calls = [
            {"name": "current_system_time", "status": "completed"},
            {"name": "calculate_expression", "status": "completed"},
        ]

    class App:
        def run(self, *_args: object, **_kwargs: object) -> Result:
            return Result()

    monkeypatch.setattr(demo, "load_llm_registry", lambda _path: Registry())
    monkeypatch.setattr(demo.AgentApp, "from_config", staticmethod(lambda *_args, **_kwargs: App()))
    with pytest.raises(click.ClickException, match="demo tool/model validation failed"):
        demo.cli.main(args=["--profile", "research-model", "--renderer", "quiet"], standalone_mode=False)


def test_demo_rejects_inconsistent_structured_timestamps(monkeypatch: pytest.MonkeyPatch) -> None:
    import click
    from utils.agent import demo
    from utils.agent.demo import DemoAnswer

    class Registry:
        def require(self, name: str) -> LLMConfig:
            return LLMConfig(model=name, api_key="key")

    class Result:
        status = "success"
        real_llm = True
        academic_eligible = True
        model = "research-model"
        observed_model = "research-model"
        tool_calls = [
            {"name": "current_system_time", "status": "completed"},
            {"name": "calculate_expression", "status": "completed"},
        ]

        def require_output(self) -> DemoAnswer:
            return DemoAnswer(
                summary="valid-looking but inconsistent",
                base_time="2026-07-13T11:15:25-04:00",
                offset_hours=51.25,
                target_time="2026-07-13T12:15:25-04:00",
                evidence_ids=["system-time-001", "math-expression-001"],
            )

    class App:
        def run(self, *_args: object, **_kwargs: object) -> Result:
            return Result()

    monkeypatch.setattr(demo, "load_llm_registry", lambda _path: Registry())
    monkeypatch.setattr(demo.AgentApp, "from_config", staticmethod(lambda *_args, **_kwargs: App()))
    with pytest.raises(click.ClickException, match="demo structured output validation failed"):
        demo.cli.main(args=["--profile", "research-model", "--renderer", "quiet"], standalone_mode=False)


def test_official_compact_is_ordered_after_context_and_before_next_model() -> None:
    class CompactModel(BaseChatModel):
        calls: int = Field(default=0)

        @property
        def _llm_type(self) -> str:
            return "compact-test"

        def bind_tools(self, tools, **kwargs):
            return self

        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            self.calls += 1
            if any("Context Extraction Assistant" in str(getattr(item, "content", "")) for item in messages):
                return ChatResult(generations=[ChatGeneration(message=AIMessage(content="summary of prior work"))])
            if self.calls <= 20:
                message = AIMessage(
                    content="",
                    tool_calls=[{"name": "probe", "args": {}, "id": f"call-{self.calls}", "type": "tool_call"}],
                )
            else:
                message = AIMessage(content="done")
            return ChatResult(generations=[ChatGeneration(message=message)])

    def probe() -> str:
        """Return a small observation."""
        return "ok"

    events: list[AgentEvent] = []
    result = AgentApp._for_test(
        AgentSpec(name="compact-order", system_prompt="use probe", tools=(probe,)),
        LLMConfig(model="compact-test", context_window_tokens=1020, max_output_tokens=20),
        CompactModel(),
    ).run("run", renderer="quiet", compact_trigger_ratio=0.5, on_event=events.append)

    assert result.status == "success", result.error
    kinds = [event.kind for event in events]
    compact_start = kinds.index("compaction_started")
    context_before = max(index for index, kind in enumerate(kinds[:compact_start]) if kind == "context_usage")
    compact_model_start = next(
        index
        for index in range(compact_start + 1, len(kinds))
        if kinds[index] == "model_started" and events[index].data.get("call_kind") == "compact"
    )
    compact_model_complete = next(
        index
        for index in range(compact_model_start + 1, len(kinds))
        if kinds[index] == "model_completed" and events[index].data.get("call_kind") == "compact"
    )
    compact_complete = kinds.index("compaction_completed")
    next_primary_model = next(
        index
        for index in range(compact_complete + 1, len(kinds))
        if kinds[index] == "model_started" and events[index].data.get("call_kind") == "primary"
    )
    assert context_before < compact_start < compact_model_start < compact_model_complete < compact_complete < next_primary_model
    for index in (compact_model_start, compact_model_complete):
        assert events[index].data.get("model_call_id")
    assert kinds.count("context_usage") >= 1


def test_compact_with_too_few_messages_fails_closed_without_next_model() -> None:
    class CompactModel(BaseChatModel):
        @property
        def _llm_type(self) -> str:
            return "compact-no-progress"

        def bind_tools(self, tools, **kwargs):
            return self

        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            return ChatResult(
                generations=[
                    ChatGeneration(
                        message=AIMessage(
                            content="",
                            tool_calls=[{"name": "probe", "args": {}, "id": "call-1", "type": "tool_call"}],
                        )
                    )
                ]
            )

    def probe() -> str:
        return "ok"

    events: list[AgentEvent] = []
    result = AgentApp._for_test(
        AgentSpec(name="compact-no-progress", system_prompt="use probe", tools=(probe,)),
        LLMConfig(model="compact-no-progress", context_window_tokens=100, max_output_tokens=10),
        CompactModel(),
    ).run("run", renderer="quiet", compact_trigger_ratio=0.5, on_event=events.append)
    assert result.status == "failed"
    assert result.error is not None
    assert result.error["code"] in {"context_budget_exceeded", "compact_error"}
    kinds = [event.kind for event in events]
    assert kinds.index("compaction_started") < kinds.index("compaction_failed")
    assert "compaction_completed" not in kinds
    assert kinds.count("model_started") == 1


def test_compact_audit_keeps_native_summary_and_call_links(tmp_path: Path) -> None:
    class CompactModel(BaseChatModel):
        calls: int = Field(default=0)

        @property
        def _llm_type(self) -> str:
            return "compact-audit-test"

        def bind_tools(self, tools, **kwargs):
            return self

        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            self.calls += 1
            if any("Context Extraction Assistant" in str(getattr(item, "content", "")) for item in messages):
                return ChatResult(generations=[ChatGeneration(message=AIMessage(content="native compact summary"))])
            if self.calls <= 20:
                return ChatResult(
                    generations=[
                        ChatGeneration(
                            message=AIMessage(
                                content="",
                                tool_calls=[{"name": "probe", "args": {}, "id": f"call-{self.calls}", "type": "tool_call"}],
                            )
                        )
                    ]
                )
            return ChatResult(generations=[ChatGeneration(message=AIMessage(content="done"))])

    def probe() -> str:
        return "ok"

    audit = tmp_path / "compact.jsonl"
    events: list[AgentEvent] = []
    result = AgentApp._for_test(
        AgentSpec(name="compact-audit", system_prompt="use probe", tools=(probe,)),
        LLMConfig(model="compact-audit-test", context_window_tokens=1020, max_output_tokens=20),
        CompactModel(),
    ).run("run", renderer="quiet", compact_trigger_ratio=0.5, audit_out=audit, on_event=events.append)
    assert result.status == "success", result.error
    records = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
    compact_done = [record for record in records if record.get("record") == "context" and record.get("operation") == "compact" and record.get("status") == "completed"]
    assert compact_done
    assert compact_done[-1]["summary"] == "native compact summary"
    assert compact_done[-1]["summary_hash"].startswith("sha256:")
    decisions = [record for record in records if record.get("record") == "decision"]
    assert all(record.get("model_call_id") for record in decisions)
    refs = [ref for record in decisions for ref in record.get("input_message_refs", [])]
    assert refs and all("source_seq" in ref for ref in refs)
    completed_event = next(event for event in events if event.kind == "compaction_completed")
    assert completed_event.data["source_refs"]
    assert all(ref.get("source_seq") is not None for ref in completed_event.data["source_refs"])


def test_compact_summary_failure_stops_before_next_primary_turn() -> None:
    class FailingCompactModel(BaseChatModel):
        calls: int = Field(default=0)

        @property
        def _llm_type(self) -> str:
            return "compact-summary-failure"

        def bind_tools(self, tools, **kwargs):
            return self

        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            self.calls += 1
            if any("Context Extraction Assistant" in str(getattr(item, "content", "")) for item in messages):
                raise RuntimeError("summary provider unavailable")
            return ChatResult(
                generations=[
                    ChatGeneration(
                        message=AIMessage(
                            content="",
                            tool_calls=[{"name": "probe", "args": {}, "id": f"call-{self.calls}", "type": "tool_call"}],
                        )
                    )
                ]
            )

    def probe() -> str:
        return "ok"

    events: list[AgentEvent] = []
    result = AgentApp._for_test(
        AgentSpec(name="compact-summary-failure", system_prompt="use probe", tools=(probe,)),
        LLMConfig(model="compact-summary-failure", context_window_tokens=1020, max_output_tokens=20),
        FailingCompactModel(),
    ).run("run", renderer="quiet", compact_trigger_ratio=0.5, on_event=events.append)
    assert result.status == "failed"
    assert result.error is not None
    assert result.error["code"] == "compact_error"
    kinds = [event.kind for event in events]
    assert "compaction_failed" in kinds
    assert "compaction_completed" not in kinds
    failed_index = kinds.index("compaction_failed")
    assert not any(
        event.kind == "model_started" and event.data.get("call_kind") == "primary"
        for event in events[failed_index + 1 :]
    )


def test_receipt_hash_matches_final_result_and_audit(tmp_path: Path) -> None:
    def lookup(value: str) -> dict[str, str]:
        """Return a fixed observation."""
        return {"value": value}

    audit = tmp_path / "trace.jsonl"
    result_path = tmp_path / "result.json"
    result = AgentApp._for_test(
        AgentSpec(name="receipt", system_prompt="answer", tools=(lookup,), require_tool_call=True),
        LLMConfig(model="gpt-5.5"),
        FakeStreamingModel(),
    ).run("run", renderer="quiet", audit_out=audit, result_out=result_path)

    assert result.academic_eligible is True
    receipt = json.loads((tmp_path / "trace.jsonl.receipt.json").read_text(encoding="utf-8"))
    import hashlib

    assert receipt["audit_sha256"] == "sha256:" + hashlib.sha256(audit.read_bytes()).hexdigest()
    assert receipt["result_sha256"] == "sha256:" + hashlib.sha256(result_path.read_bytes()).hexdigest()
    assert all("recorded_at_utc" in json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines())


def test_context_panel_has_two_logical_lines() -> None:
    from rich.console import Console
    from utils.agent.runtime import _Renderer

    output = StringIO()
    renderer = _Renderer("rich", "INFO", "context-panel")
    renderer.console = Console(file=output, force_terminal=False, color_system=None)
    renderer.render(
        AgentEvent(
            "context-panel",
            1,
            datetime.now(timezone.utc),
            "context_usage",
            {
                "turn": 4,
                "usage": {"input_tokens": 100, "output_tokens": 20, "total_tokens": 120},
                "context_basis_tokens": 150,
                "context_window_tokens": 1000,
                "compact_threshold": 800,
                "basis_source": ["langchain_estimate"],
                "decision": "not_required",
            },
        )
    )
    rendered = output.getvalue()
    assert "CONTEXT | TURN 4" in rendered
    assert "context ~150/1,000" in rendered
    assert rendered.count("turn 4") == 1


def test_context_basis_prefers_provider_input_over_output_tokens() -> None:
    from utils.agent.runtime import _ContextMeter

    meter = _ContextMeter(system_prompt="answer")
    meter.record({"input_tokens": 100, "output_tokens": 900, "total_tokens": 1000})

    tokens, sources = meter.count([])

    assert tokens == 1000
    assert sources == ["provider_total_anchor"]
    assert meter.estimate([]) != 100


def test_context_meter_uses_maximum_public_usage_anchor() -> None:
    from utils.agent.runtime import _ContextMeter

    meter = _ContextMeter(system_prompt="answer")
    meter.record(
        {"input_tokens": 100, "output_tokens": 10, "total_tokens": 110},
        observed_usages=[
            {"source": "llm_output.token_usage", "usage": {"prompt_tokens": 180, "completion_tokens": 20, "total_tokens": 200}}
        ],
    )
    tokens, sources = meter.count([])
    assert tokens == 200
    assert sources == ["provider_total_anchor"]


def test_output_target_cannot_use_audit_sidecar_path(tmp_path: Path) -> None:
    from utils.agent.runtime import _validate_output_paths

    audit = tmp_path / "trace.jsonl"
    with pytest.raises(AgentError, match="derived sidecar"):
        _validate_output_paths(audit, audit.with_name(audit.name + ".lock"))


def test_result_and_audit_redact_configured_key_across_boundaries(tmp_path: Path) -> None:
    class _LeakModel(BaseChatModel):
        @property
        def _llm_type(self) -> str:
            return "leak-test"

        def bind_tools(self, tools, **kwargs):
            return self

        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            return ChatResult(generations=[ChatGeneration(message=AIMessage(content="key=sk-configured-secret-123456"))])

    audit = tmp_path / "trace.jsonl"
    result_path = tmp_path / "result.json"
    result = AgentApp._for_test(
        AgentSpec(name="redact-config", system_prompt="answer"),
        LLMConfig(model="gpt-5.5", api_key="sk-configured-secret-123456"),
        _LeakModel(),
    ).run("run", renderer="quiet", audit_out=audit, result_out=result_path)
    assert result.status == "success"
    serialized = result.to_json() + audit.read_text(encoding="utf-8")
    assert "sk-configured-secret-123456" not in serialized


def test_result_public_fields_redact_anthropic_and_project_tokens() -> None:
    from utils.agent.runtime import AgentRunResult

    anthropic = "sk-ant-api03-abcdefghijklmnopqrstuvwxyz1234567890"
    project = "sk-proj-abcdefghijklmnopqrstuvwxyz1234567890"
    result = AgentRunResult(
        run_id="run-redact",
        status="success",
        output={"token": anthropic},
        final_text=f"provider returned {project}",
        tool_calls=[{"name": "probe", "result": {"value": anthropic}}],
        usage=[],
        error=None,
        real_llm=True,
        model="gpt-5.5",
        observed_model="gpt-5.5",
        academic_eligible=False,
        context_manifest_hash=None,
    )

    serialized = json.dumps(result.to_dict(), ensure_ascii=False)
    assert anthropic not in serialized
    assert project not in serialized
