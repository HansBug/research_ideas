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
        "model_started",
        "model_text",
        "model_completed",
        "completed",
    ]
    records = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
    assert [record["record"] for record in records] == ["context", "decision", "action", "decision", "finish"]
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
    assert result.error == {"code": "limit_exceeded", "message": "tool_calls limit exceeded"}
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


def test_rollover_replay_keeps_replayed_and_new_same_argument_calls(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from utils.agent import runtime

    class _Graph:
        def __init__(self, attempt: int):
            self.attempt = attempt

        async def astream_events(self, _inputs, version: str):
            assert version == "v2"
            if self.attempt == 1:
                yield {"event": "on_chain_start", "name": "model", "data": {"input": {"messages": []}}}
                yield {
                    "event": "on_chain_end",
                    "name": "model",
                    "data": {"output": {"messages": [AIMessage(content="", tool_calls=[{"name": "probe", "args": {}, "id": "id-1", "type": "tool_call"}])] }},
                }
                yield {"event": "on_tool_start", "name": "probe", "run_id": "exec-1", "data": {"input": {}}}
                yield {"event": "on_tool_end", "name": "probe", "run_id": "exec-1", "data": {"output": ToolMessage(content="old", name="probe", tool_call_id="id-1")}}
                raise AgentError("context_rollover", "test rollover")

            yield {"event": "on_chain_start", "name": "model", "data": {"input": {"messages": []}}}
            yield {
                "event": "on_chain_end",
                "name": "model",
                "data": {
                    "output": {
                        "messages": [
                            AIMessage(
                                content="",
                                tool_calls=[
                                    {"name": "probe", "args": {}, "id": "id-2", "type": "tool_call"},
                                    {"name": "probe", "args": {}, "id": "id-3", "type": "tool_call"},
                                ],
                            )
                        ]
                    }
                },
            }
            yield {"event": "on_tool_start", "name": "probe", "run_id": "exec-3", "data": {"input": {}}}
            yield {"event": "on_tool_end", "name": "probe", "run_id": "exec-3", "data": {"output": ToolMessage(content="new", name="probe", tool_call_id="id-3")}}
            yield {"event": "on_chain_end", "name": "LangGraph", "data": {"output": {"messages": [AIMessage(content="done")]}}}

    created = 0

    def fake_create_agent(**_kwargs):
        nonlocal created
        created += 1
        return _Graph(created)

    monkeypatch.setattr(runtime, "create_agent", fake_create_agent)

    def probe() -> str:
        return "unused"

    events = []
    result = AgentApp._for_test(
        AgentSpec(name="rollover", system_prompt="probe", tools=(probe,), require_tool_call=True),
        LLMConfig(model="gpt-5.5"),
        object(),
    ).run("run", renderer="quiet", on_event=events.append, audit_out=tmp_path / "audit.jsonl")

    assert result.status == "success"
    assert [(item["tool_call_id"], item.get("replayed", False)) for item in result.tool_calls] == [("id-1", False), ("id-2", True), ("id-3", False)]
    tool_events = [event for event in events if event.kind in {"tool_started", "tool_completed"}]
    assert [event.data["tool_call_id"] for event in tool_events] == ["id-1", "id-1", "id-2", "id-2", "id-3", "id-3"]
    records = [json.loads(line) for line in (tmp_path / "audit.jsonl").read_text(encoding="utf-8").splitlines()]
    actions = [record for record in records if record.get("record") == "action"]
    assert [record["tool_call_id"] for record in actions] == ["id-1", "id-3"]
    rollover = next(record for record in records if record.get("record") == "context" and record.get("rollover"))
    assert [record["tool_call_id"] for record in rollover["replayed_actions"]] == ["id-1"]


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
    ).run("sk-secret12345678", renderer="quiet", on_event=events.append)

    serialized = json.dumps([event.to_dict() for event in events], ensure_ascii=False)
    assert "sk-secret12345678" not in serialized
    assert "DO_NOT_LEAK_SYSTEM" in serialized


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
        return {"value": value, "token": "sk-secret12345678"}

    result = AgentApp._for_test(
        AgentSpec(name="result-redact", system_prompt="use lookup", tools=(lookup,), require_tool_call=True),
        LLMConfig(model="gpt-5.5", api_key="key"),
        FakeStreamingModel(),
    ).run("read", renderer="quiet")

    assert "sk-secret12345678" not in result.to_json()
    assert result.tool_calls[0]["result"]["token"] == "[redacted]"
    assert "sk-secret12345678" not in json.dumps(result.tool_calls, ensure_ascii=False)


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


def test_redaction_preserves_normal_urls_in_model_content() -> None:
    from utils.agent.runtime import _redact

    value = "参考 https://example.org/docs 完成任务"
    assert _redact(value) == value
    assert _redact({"url": "https://example.org/docs"}) == {"url": "https://example.org/docs"}
    assert _redact({"api_url": "https://provider.invalid/v1"}) == {"api_url": "[redacted_endpoint]"}


def test_rollover_replay_queue_does_not_swallow_new_duplicate_call() -> None:
    from utils.agent.runtime import _ReplayToolMiddleware

    class Request:
        tool_call = {"name": "probe", "args": {}, "id": "call-1"}

    calls: list[str] = []
    provenance: dict[str, list[bool]] = {}

    def handler(_request: Request) -> ToolMessage:
        calls.append("executed")
        return ToolMessage(content="new", name="probe", tool_call_id="call-2")

    middleware = _ReplayToolMiddleware({"probe:{}": ["old"]}, enabled=True, provenance=provenance)
    replayed = middleware.wrap_tool_call(Request(), handler)
    new_call = middleware.wrap_tool_call(Request(), handler)
    assert replayed.content == "old"
    assert replayed.additional_kwargs["replayed"] is True
    assert new_call.content == "new"
    assert calls == ["executed"]
    assert provenance["probe:{}"] == [True, False]


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
    assert "MODEL OUTPUT | STRUCTURED RESULT" in rendered
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
