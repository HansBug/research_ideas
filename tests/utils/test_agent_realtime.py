from __future__ import annotations

import asyncio
import json
import re
import threading
import time
from contextlib import redirect_stdout, suppress
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import httpx
from langchain_core.callbacks import BaseCallbackHandler, CallbackManager
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, AIMessageChunk, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, PrivateAttr
from rich.console import Console

from utils.agent import AgentApp, AgentEvent, AgentSpec
from utils.agent.runtime import _Renderer, _RunModelObserver, _public_stream_chunk
from utils.llm import LLMConfig


class _ProbeWriter:
    encoding = "utf-8"

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._parts: list[str] = []
        self.writes: list[tuple[float, str]] = []
        self.flushes: list[float] = []

    def write(self, value: str) -> int:
        with self._lock:
            self._parts.append(value)
            self.writes.append((time.monotonic(), value))
        return len(value)

    def flush(self) -> None:
        with self._lock:
            self.flushes.append(time.monotonic())

    def isatty(self) -> bool:
        return True

    def snapshot(self) -> str:
        with self._lock:
            return "".join(self._parts)


class _RealtimeProbe:
    def __init__(self, writer: _ProbeWriter) -> None:
        self.writer = writer
        self.model_calls = 0
        self.transport_snapshots: list[str] = []
        self.release_first_model = asyncio.Event()
        self.release_second_chunk = asyncio.Event()
        self.first_transport_entered = asyncio.Event()
        self.second_transport_entered = asyncio.Event()
        self.first_chunk_processed = asyncio.Event()
        self.tool_entered = threading.Event()
        self.release_tool = threading.Event()
        self.tool_snapshot = ""


class _BoundBarrierChatModel(ChatOpenAI):
    """Exercise the real ChatOpenAI bind_tools path without network access."""

    _probe: _RealtimeProbe = PrivateAttr()

    def __init__(self, probe: _RealtimeProbe) -> None:
        super().__init__(model="gpt-4o-mini", api_key="sk-test-not-real", streaming=True)
        self._probe = probe

    async def _astream(self, messages: list[Any], stop: list[str] | None = None, **kwargs: Any):
        self._probe.model_calls += 1
        call = self._probe.model_calls
        self._probe.transport_snapshots.append(self._probe.writer.snapshot())
        if call == 1:
            self._probe.first_transport_entered.set()
            await self._probe.release_first_model.wait()
            yield ChatGenerationChunk(
                message=AIMessageChunk(
                    content="",
                    tool_call_chunks=[
                        {
                            "name": "observe",
                            "args": '{"value":"evidence"}',
                            "id": "call-observe",
                            "index": 0,
                        }
                    ],
                )
            )
            return

        self._probe.second_transport_entered.set()
        yield ChatGenerationChunk(message=AIMessageChunk(content="first segment "))
        self._probe.first_chunk_processed.set()
        await self._probe.release_second_chunk.wait()
        yield ChatGenerationChunk(message=AIMessageChunk(content="second segment"))


class _EmptySemanticChunkModel(ChatOpenAI):
    async def _astream(self, messages: list[Any], stop: list[str] | None = None, **kwargs: Any):
        yield ChatGenerationChunk(message=AIMessageChunk(content=""))


def _patch_terminal_console(monkeypatch: Any, writer: _ProbeWriter) -> None:
    import rich.console

    console = Console(file=writer, force_terminal=True, color_system=None, width=120)
    monkeypatch.setattr(rich.console, "Console", lambda: console)


def test_bound_model_outputs_each_fact_before_the_next_stage(monkeypatch: Any) -> None:
    writer = _ProbeWriter()
    probe = _RealtimeProbe(writer)
    _patch_terminal_console(monkeypatch, writer)
    events: list[AgentEvent] = []

    def observe(value: str) -> dict[str, str]:
        """Return the supplied evidence value."""

        probe.tool_snapshot = writer.snapshot()
        probe.tool_entered.set()
        assert probe.release_tool.wait(timeout=5)
        return {"value": value}

    app = AgentApp._for_test(
        AgentSpec(name="realtime-bound", system_prompt="Use the registered observation tool.", tools=(observe,)),
        LLMConfig(model="gpt-4o-mini"),
        _BoundBarrierChatModel(probe),
    )

    async def scenario() -> None:
        task = asyncio.create_task(app.arun("perform the realtime probe", renderer="rich", on_event=events.append))
        try:
            await asyncio.wait_for(probe.first_transport_entered.wait(), timeout=5)
            assert "TURN 1 | MODEL INPUT" in probe.transport_snapshots[0]
            assert "perform the realtime probe" in probe.transport_snapshots[0]
            assert events[-1].kind == "model_started"
            assert events[-1].data["turn"] == 1

            probe.release_first_model.set()
            assert await asyncio.wait_for(asyncio.to_thread(probe.tool_entered.wait, 5), timeout=6)
            requested = next(event for event in events if event.kind == "model_completed" and event.data.get("turn") == 1)
            assert requested.data["tool_requests"][0]["status"] == "requested"
            assert "MODEL OUTPUT | TOOL CALL" in probe.tool_snapshot
            assert "status: requested" in probe.tool_snapshot

            probe.release_tool.set()
            await asyncio.wait_for(probe.second_transport_entered.wait(), timeout=5)
            assert "TOOL RESULT -> NEXT MODEL INPUT" in probe.transport_snapshots[1]

            await asyncio.wait_for(probe.first_chunk_processed.wait(), timeout=5)
            assert "first segment" in writer.snapshot()
            assert "second segment" not in writer.snapshot()
            probe.release_second_chunk.set()

            result = await asyncio.wait_for(task, timeout=5)
            assert result.status == "success", result.error
        finally:
            probe.release_first_model.set()
            probe.release_tool.set()
            probe.release_second_chunk.set()
            if not task.done():
                with suppress(Exception):
                    await asyncio.wait_for(task, timeout=5)

    asyncio.run(scenario())

    model_starts = [event for event in events if event.kind == "model_started" and event.data.get("call_kind") == "primary"]
    model_ends = [event for event in events if event.kind == "model_completed" and event.data.get("call_kind") == "primary"]
    assert len(model_starts) == len(model_ends) == 2
    for start in model_starts:
        assert start.data["started_at_utc"]
        assert start.data["timing_source"] == "provider_callback"
    for end in model_ends:
        assert end.data["ended_at_utc"]
        assert end.data["duration_seconds"] >= 0
        assert end.data["timing_source"] == "provider_callback"
    assert model_ends[1].data["time_to_first_chunk_seconds"] >= 0
    rendered = writer.snapshot()
    assert re.search(r"MODEL INPUT \| MESSAGES \| t=\+\d+\.\d{3}s", rendered)
    assert re.search(r"MODEL OUTPUT \| TOOL CALL \| model=\d+\.\d{3}s", rendered)
    assert re.search(r"TOOL RESULT -> NEXT MODEL INPUT \| queue=\d+\.\d{3}s \| execution=\d+\.\d{3}s", rendered)
    assert re.search(r"MODEL OUTPUT \| ASSISTANT \| model=\d+\.\d{3}s \| first_chunk=\d+\.\d{3}s", rendered)
    assert re.search(r"duration: \d+\.\d{3}s", rendered)


def test_model_callback_copy_preserves_existing_callbacks_without_mutation() -> None:
    observed: list[str] = []

    class ExistingCallback(BaseCallbackHandler):
        def on_chat_model_start(self, *args: Any, **kwargs: Any) -> None:
            observed.append("start")

        def on_llm_new_token(self, *args: Any, **kwargs: Any) -> None:
            observed.append("token")

        def on_llm_end(self, *args: Any, **kwargs: Any) -> None:
            observed.append("end")

    model = _EmptySemanticChunkModel(
        model="gpt-4o-mini",
        api_key="sk-test-not-real",
        streaming=True,
        callbacks=[ExistingCallback()],
    )
    callbacks_before = list(model.callbacks or [])
    result = AgentApp._for_test(
        AgentSpec(name="callback-copy", system_prompt="Answer directly."),
        LLMConfig(model="gpt-4o-mini"),
        model,
    ).run("hello", renderer="quiet")

    assert result.status == "success", result.error
    assert observed.count("start") == 1
    assert observed.count("end") == 1
    assert observed.count("token") >= 1
    assert observed[0] == "start" and observed[-1] == "end"
    assert list(model.callbacks or []) == callbacks_before


def test_model_callback_manager_copy_preserves_existing_callbacks() -> None:
    observed: list[str] = []

    class ExistingCallback(BaseCallbackHandler):
        def on_chat_model_start(self, *args: Any, **kwargs: Any) -> None:
            observed.append("start")

        def on_llm_end(self, *args: Any, **kwargs: Any) -> None:
            observed.append("end")

    callback = ExistingCallback()
    manager = CallbackManager([callback])
    model = _EmptySemanticChunkModel(
        model="gpt-4o-mini",
        api_key="sk-test-not-real",
        streaming=True,
        callbacks=manager,
    )
    result = AgentApp._for_test(
        AgentSpec(name="callback-manager-copy", system_prompt="Answer directly."),
        LLMConfig(model="gpt-4o-mini"),
        model,
    ).run("hello", renderer="quiet")

    assert result.status == "success", result.error
    assert observed == ["start", "end"]
    assert model.callbacks is manager
    assert manager.handlers == [callback]


def test_async_tool_request_and_result_are_visible_at_stage_boundaries(monkeypatch: Any) -> None:
    writer = _ProbeWriter()
    probe = _RealtimeProbe(writer)
    _patch_terminal_console(monkeypatch, writer)
    tool_entered = asyncio.Event()
    release_tool = asyncio.Event()
    tool_snapshot: list[str] = []

    async def observe(value: str) -> dict[str, str]:
        """Return one asynchronous observation."""

        tool_snapshot.append(writer.snapshot())
        tool_entered.set()
        await release_tool.wait()
        return {"value": value}

    app = AgentApp._for_test(
        AgentSpec(name="realtime-async", system_prompt="Use the registered observation tool.", tools=(observe,)),
        LLMConfig(model="gpt-4o-mini"),
        _BoundBarrierChatModel(probe),
    )

    async def scenario() -> Any:
        task = asyncio.create_task(app.arun("perform the async probe", renderer="rich"))
        try:
            await asyncio.wait_for(probe.first_transport_entered.wait(), timeout=5)
            probe.release_first_model.set()
            await asyncio.wait_for(tool_entered.wait(), timeout=5)
            assert "MODEL OUTPUT | TOOL CALL" in tool_snapshot[0]
            assert "status: requested" in tool_snapshot[0]
            release_tool.set()
            await asyncio.wait_for(probe.second_transport_entered.wait(), timeout=5)
            assert "TOOL RESULT -> NEXT MODEL INPUT" in probe.transport_snapshots[1]
            await asyncio.wait_for(probe.first_chunk_processed.wait(), timeout=5)
            probe.release_second_chunk.set()
            return await asyncio.wait_for(task, timeout=5)
        finally:
            probe.release_first_model.set()
            release_tool.set()
            probe.release_second_chunk.set()

    result = asyncio.run(scenario())
    assert result.status == "success", result.error


def test_jsonl_model_input_is_flushed_before_transport() -> None:
    writer = _ProbeWriter()
    probe = _RealtimeProbe(writer)

    def observe(value: str) -> dict[str, str]:
        """Return one JSONL observation."""

        probe.tool_entered.set()
        assert probe.release_tool.wait(timeout=5)
        return {"value": value}

    app = AgentApp._for_test(
        AgentSpec(name="realtime-jsonl", system_prompt="Use the tool.", tools=(observe,)),
        LLMConfig(model="gpt-4o-mini"),
        _BoundBarrierChatModel(probe),
    )

    async def scenario() -> Any:
        task = asyncio.create_task(app.arun("jsonl probe", renderer="jsonl"))
        try:
            await asyncio.wait_for(probe.first_transport_entered.wait(), timeout=5)
            snapshot = probe.transport_snapshots[0]
            assert '"kind": "model_started"' in snapshot
            assert "jsonl probe" in snapshot
            assert writer.flushes
            probe.release_first_model.set()
            assert await asyncio.wait_for(asyncio.to_thread(probe.tool_entered.wait, 5), timeout=6)
            probe.release_tool.set()
            await asyncio.wait_for(probe.first_chunk_processed.wait(), timeout=5)
            probe.release_second_chunk.set()
            return await asyncio.wait_for(task, timeout=5)
        finally:
            probe.release_first_model.set()
            probe.release_tool.set()
            probe.release_second_chunk.set()

    with redirect_stdout(writer):
        result = asyncio.run(scenario())
    assert result.status == "success", result.error


def test_observer_deduplicates_chat_and_llm_start_for_one_run_id() -> None:
    starts: list[str] = []
    observer = _RunModelObserver(
        lambda call_id, metadata, inputs: starts.append(call_id),
        lambda call_id, token, chunk, metadata: None,
        lambda call_id, response, metadata: None,
        lambda call_id, error, metadata: None,
    )

    observer.on_chat_model_start({}, [[]], run_id="same-run")
    observer.on_llm_start({}, ["prompt"], run_id="same-run")

    assert starts == ["same-run"]


def test_empty_or_usage_only_chunks_do_not_fake_first_chunk() -> None:
    events: list[AgentEvent] = []
    result = AgentApp._for_test(
        AgentSpec(name="empty-chunk", system_prompt="Answer directly."),
        LLMConfig(model="gpt-4o-mini"),
        _EmptySemanticChunkModel(model="gpt-4o-mini", api_key="sk-test-not-real", streaming=True),
    ).run("hello", renderer="quiet", on_event=events.append)

    assert result.status == "success", result.error
    completed = next(event for event in events if event.kind == "model_completed")
    assert completed.data["first_chunk_at_utc"] is None
    assert completed.data["time_to_first_chunk_seconds"] is None
    assert completed.data["timing_source"] == "provider_callback"
    assert result.usage[0]["first_chunk_at_utc"] is None
    assert result.usage[0]["time_to_first_chunk_seconds"] is None


def test_raw_reasoning_content_is_not_public_text_or_first_chunk() -> None:
    hidden = AIMessageChunk(
        content="",
        response_metadata={"reasoning_content": "private chain of thought"},
    )
    text, semantic = _public_stream_chunk(
        "private chain of thought",
        ChatGenerationChunk(message=hidden),
    )
    assert text == ""
    assert semantic is False

    visible = AIMessageChunk(
        content="",
        response_metadata={"reasoning_summary": "public summary"},
    )
    text, semantic = _public_stream_chunk("public summary", ChatGenerationChunk(message=visible))
    assert text == ""
    assert semantic is True


def test_bare_callback_token_without_public_chunk_is_not_visible() -> None:
    text, semantic = _public_stream_chunk("private chain of thought", None)
    assert text == ""
    assert semantic is False


def test_bare_callback_token_is_not_emitted_by_full_agent_run(tmp_path: Path) -> None:
    class BareReasoningModel(BaseChatModel):
        @property
        def _llm_type(self) -> str:
            return "bare-reasoning-test"

        def bind_tools(self, tools: Any, **kwargs: Any) -> "BareReasoningModel":
            return self

        def _generate(
            self,
            messages: list[Any],
            stop: list[str] | None = None,
            run_manager: Any = None,
            **kwargs: Any,
        ) -> ChatResult:
            if run_manager is not None:
                run_manager.on_llm_new_token("PRIVATE_CHAIN_OF_THOUGHT", chunk=None)
            return ChatResult(generations=[ChatGeneration(message=AIMessage(content="visible answer"))])

    events: list[AgentEvent] = []
    audit = tmp_path / "bare-reasoning.jsonl"
    result = AgentApp._for_test(
        AgentSpec(name="bare-reasoning", system_prompt="Answer directly."),
        LLMConfig(model="bare-reasoning-test"),
        BareReasoningModel(),
    ).run("hello", renderer="quiet", on_event=events.append, audit_out=audit)

    assert result.status == "success", result.error
    model_text = [event.data.get("text", "") for event in events if event.kind == "model_text"]
    assert all("PRIVATE_CHAIN_OF_THOUGHT" not in text for text in model_text)
    completed = next(event for event in events if event.kind == "model_completed")
    assert completed.data["first_chunk_at_utc"] is None
    assert completed.data["time_to_first_chunk_seconds"] is None
    assert "PRIVATE_CHAIN_OF_THOUGHT" not in audit.read_text(encoding="utf-8")


def test_jsonl_renderer_flushes_each_event() -> None:
    writer = _ProbeWriter()
    renderer = _Renderer("jsonl", "INFO", "flush-run")
    assert renderer.handler is not None
    renderer.handler.setStream(writer)

    with redirect_stdout(writer):
        renderer.render(
            AgentEvent(
                run_id="flush-run",
                seq=1,
                timestamp=datetime.now(timezone.utc),
                kind="model_started",
                data={"turn": 1, "prompt": "hello"},
            )
        )

    assert writer.flushes
    assert "model_started" in writer.snapshot()


def test_same_name_parallel_tools_link_results_by_tool_call_id() -> None:
    a_started = threading.Event()
    allow_a_to_finish = threading.Event()
    events: list[AgentEvent] = []

    def probe(value: str) -> dict[str, str]:
        """Return one concurrent observation."""

        if value == "a":
            a_started.set()
            assert allow_a_to_finish.wait(timeout=5)
        else:
            assert a_started.wait(timeout=5)
        return {"value": value}

    class ParallelModel(BaseChatModel):
        calls: int = Field(default=0)

        @property
        def _llm_type(self) -> str:
            return "parallel-tool-test"

        def bind_tools(self, tools: Any, **kwargs: Any) -> "ParallelModel":
            return self

        def _generate(self, messages: list[Any], stop: list[str] | None = None, run_manager: Any = None, **kwargs: Any) -> ChatResult:
            self.calls += 1
            if self.calls == 1:
                message = AIMessage(
                    content="",
                    tool_calls=[
                        {"name": "probe", "args": {"value": "a"}, "id": "call-a", "type": "tool_call"},
                        {"name": "probe", "args": {"value": "b"}, "id": "call-b", "type": "tool_call"},
                    ],
                )
            else:
                message = AIMessage(content="done")
            return ChatResult(generations=[ChatGeneration(message=message)])

    def observe(event: AgentEvent) -> None:
        events.append(event)
        if event.kind == "tool_completed" and event.data.get("tool_call_id") == "call-b":
            allow_a_to_finish.set()

    result = AgentApp._for_test(
        AgentSpec(name="parallel-tools", system_prompt="Use both tools.", tools=(probe,)),
        LLMConfig(model="parallel-tool-test"),
        ParallelModel(),
    ).run("run both", renderer="quiet", on_event=observe)

    assert result.status == "success", result.error
    completed = [event for event in events if event.kind == "tool_completed"]
    assert [event.data["tool_call_id"] for event in completed] == ["call-b", "call-a"]
    by_id = {record["tool_call_id"]: record for record in result.tool_calls}
    assert set(by_id) == {"call-a", "call-b"}
    for call_id, value in (("call-a", "a"), ("call-b", "b")):
        record = by_id[call_id]
        assert record["arguments"] == {"value": value}
        assert record["result"] == {"value": value}
        assert record["requested_at"] and record["started_at"] and record["finished_at"]
        assert record["queue_duration_seconds"] >= 0
        assert record["duration_seconds"] >= 0


def test_same_name_identical_parallel_tools_keep_orphan_execution_separate(tmp_path: Path) -> None:
    class IdenticalParallelModel(BaseChatModel):
        @property
        def _llm_type(self) -> str:
            return "identical-parallel-test"

        def bind_tools(self, tools: Any, **kwargs: Any) -> "IdenticalParallelModel":
            return self

        def _generate(self, messages: list[Any], stop: list[str] | None = None, run_manager: Any = None, **kwargs: Any) -> ChatResult:
            return ChatResult(
                generations=[
                    ChatGeneration(
                        message=AIMessage(
                            content="",
                            tool_calls=[
                                {"name": "probe", "args": {"value": "x"}, "id": "identical-a", "type": "tool_call"},
                                {"name": "probe", "args": {"value": "x"}, "id": "identical-b", "type": "tool_call"},
                            ],
                        )
                    )
                ]
            )

    entered = 0
    lock = asyncio.Lock()
    both_entered = asyncio.Event()

    async def probe(value: str) -> str:
        nonlocal entered
        async with lock:
            entered += 1
            invocation = entered
            if invocation == 2:
                both_entered.set()
        await both_entered.wait()
        if invocation == 1:
            raise RuntimeError("first identical call failed")
        await asyncio.Event().wait()
        return value

    audit = tmp_path / "identical-parallel.jsonl"
    result = AgentApp._for_test(
        AgentSpec(name="identical-parallel", system_prompt="Use the tool.", tools=(probe,)),
        LLMConfig(model="identical-parallel-test"),
        IdenticalParallelModel(),
    ).run("run", renderer="quiet", audit_out=audit)

    assert result.status == "failed"
    assert {item["status"] for item in result.tool_calls} == {"unresolved"}
    assert {item["mapping"] for item in result.tool_calls} == {"ambiguous"}
    records = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
    actions = [record for record in records if record.get("record") == "action"]
    assert len(actions) == 2
    assert {record.get("mapping") for record in actions} == {"orphan"}
    assert {record.get("status") for record in actions} == {"failed", "cancelled"}
    assert all(set(record["candidate_tool_call_ids"]) == {"identical-a", "identical-b"} for record in actions)


def test_model_duration_uses_monotonic_when_utc_moves_backward(monkeypatch: Any) -> None:
    import utils.agent.runtime as runtime

    clock = SimpleNamespace(
        monotonic=100.0,
        utc=datetime(2026, 7, 17, 12, 0, tzinfo=timezone.utc),
    )
    monkeypatch.setattr(runtime, "_monotonic", lambda: clock.monotonic)
    monkeypatch.setattr(runtime, "_utc_now", lambda: clock.utc)

    class RollbackModel(BaseChatModel):
        @property
        def _llm_type(self) -> str:
            return "rollback-test"

        def bind_tools(self, tools: Any, **kwargs: Any) -> "RollbackModel":
            return self

        def _generate(self, messages: list[Any], stop: list[str] | None = None, run_manager: Any = None, **kwargs: Any) -> ChatResult:
            clock.monotonic += 2.0
            clock.utc = clock.utc.replace(second=50) - timedelta(seconds=60)
            return ChatResult(generations=[ChatGeneration(message=AIMessage(content="done"))])

    result = AgentApp._for_test(
        AgentSpec(name="rollback", system_prompt="Answer."),
        LLMConfig(model="rollback-test"),
        RollbackModel(),
    ).run("go", renderer="quiet")

    assert result.status == "success", result.error
    assert result.usage[0]["duration_seconds"] == 2.0
    assert datetime.fromisoformat(result.usage[0]["ended_at_utc"]) < datetime.fromisoformat(
        result.usage[0]["started_at_utc"]
    )


def test_tool_duration_uses_monotonic_when_utc_moves_backward(monkeypatch: Any) -> None:
    import utils.agent.runtime as runtime

    clock = SimpleNamespace(
        monotonic=200.0,
        utc=datetime(2026, 7, 17, 13, 0, tzinfo=timezone.utc),
    )
    monkeypatch.setattr(runtime, "_monotonic", lambda: clock.monotonic)
    monkeypatch.setattr(runtime, "_utc_now", lambda: clock.utc)
    start_observed = threading.Event()

    class ToolClockModel(BaseChatModel):
        calls: int = Field(default=0)

        @property
        def _llm_type(self) -> str:
            return "tool-clock-test"

        def bind_tools(self, tools: Any, **kwargs: Any) -> "ToolClockModel":
            return self

        def _generate(self, messages: list[Any], stop: list[str] | None = None, run_manager: Any = None, **kwargs: Any) -> ChatResult:
            self.calls += 1
            message = (
                AIMessage(
                    content="",
                    tool_calls=[
                        {"name": "probe", "args": {}, "id": "clock-call", "type": "tool_call"}
                    ],
                )
                if self.calls == 1
                else AIMessage(content="done")
            )
            return ChatResult(generations=[ChatGeneration(message=message)])

    def probe() -> str:
        """Advance the controlled tool clock."""

        assert start_observed.wait(timeout=5)
        clock.monotonic += 2.0
        clock.utc -= timedelta(seconds=10)
        return "ok"

    def observe(event: AgentEvent) -> None:
        if event.kind == "tool_started":
            start_observed.set()

    result = AgentApp._for_test(
        AgentSpec(name="tool-clock", system_prompt="Use the tool.", tools=(probe,)),
        LLMConfig(model="tool-clock-test"),
        ToolClockModel(),
    ).run("go", renderer="quiet", on_event=observe)

    assert result.status == "success", result.error
    record = result.tool_calls[0]
    assert record["duration_seconds"] == 2.0
    assert datetime.fromisoformat(record["finished_at"]) < datetime.fromisoformat(record["started_at"])


def test_graph_fallback_has_one_terminal_and_no_fake_first_chunk(monkeypatch: Any) -> None:
    import utils.agent.runtime as runtime

    events: list[AgentEvent] = []

    class GraphWithoutModelCallbacks:
        def __init__(self, middleware: list[Any]) -> None:
            self.middleware = middleware

        async def astream_events(self, inputs: dict[str, Any], **kwargs: Any):
            messages = [HumanMessage(content="fallback input")]
            request = SimpleNamespace(
                messages=messages,
                system_message=SystemMessage(content="Fallback system."),
                tools=[],
                response_format=None,
                model_settings={},
            )
            capture = next(item for item in self.middleware if isinstance(item, runtime._RequestCaptureMiddleware))
            capture._capture(request)
            yield {
                "event": "on_chain_start",
                "name": "model",
                "run_id": "graph-model-1",
                "data": {"input": {"messages": messages}},
            }
            answer = AIMessage(content="fallback answer")
            yield {
                "event": "on_chain_end",
                "name": "model",
                "run_id": "graph-model-1",
                "data": {"output": {"messages": [answer]}},
            }
            yield {
                "event": "on_chain_end",
                "name": "fallback-agent",
                "run_id": "graph-root",
                "data": {"output": {"messages": [*messages, answer]}},
            }

    def fake_create_agent(*, middleware: list[Any], **kwargs: Any) -> GraphWithoutModelCallbacks:
        return GraphWithoutModelCallbacks(middleware)

    monkeypatch.setattr(runtime, "create_agent", fake_create_agent)
    model = _EmptySemanticChunkModel(
        model="gpt-4o-mini",
        api_key="sk-test-not-real",
        streaming=True,
    )
    result = AgentApp._for_test(
        AgentSpec(name="fallback-agent", system_prompt="Fallback system."),
        LLMConfig(model="gpt-4o-mini"),
        model,
    ).run("fallback input", renderer="quiet", on_event=events.append)

    assert result.status == "success", result.error
    starts = [event for event in events if event.kind == "model_started"]
    terminals = [event for event in events if event.kind in {"model_completed", "model_failed"}]
    assert len(starts) == len(terminals) == 1
    assert starts[0].data["timing_source"] == "graph_fallback"
    assert terminals[0].data["timing_source"] == "graph_fallback"
    assert terminals[0].data["first_chunk_at_utc"] is None
    assert result.usage[0]["timing_source"] == "graph_fallback"
    assert result.usage[0]["time_to_first_chunk_seconds"] is None


def test_graph_fallback_projects_chat_usage_to_canonical_chain_call(monkeypatch: Any) -> None:
    import utils.agent.runtime as runtime

    class BufferedFallbackGraph:
        def __init__(self, middleware: list[Any]) -> None:
            self.middleware = middleware

        async def astream_events(self, inputs: dict[str, Any], **kwargs: Any):
            messages = [HumanMessage(content="fallback input")]
            request = SimpleNamespace(
                messages=messages,
                system_message=SystemMessage(content="Fallback system."),
                tools=[],
                response_format=None,
                model_settings={},
            )
            capture = next(item for item in self.middleware if isinstance(item, runtime._RequestCaptureMiddleware))
            capture._capture(request)
            yield {
                "event": "on_chain_start",
                "name": "model",
                "run_id": "graph-canonical-1",
                "data": {"input": {"messages": messages}},
            }
            answer = AIMessage(
                content="fallback answer",
                usage_metadata={"input_tokens": 3, "output_tokens": 2, "total_tokens": 5},
            )
            yield {
                "event": "on_chat_model_end",
                "name": "ChatModel",
                "run_id": "chat-observer-1",
                "data": {"output": ChatResult(generations=[ChatGeneration(message=answer)])},
            }
            yield {
                "event": "on_chain_end",
                "name": "model",
                "run_id": "graph-canonical-1",
                "data": {"output": {"messages": [answer]}},
            }
            yield {
                "event": "on_chain_end",
                "name": "fallback-canonical",
                "run_id": "graph-root",
                "data": {"output": {"messages": [*messages, answer]}},
            }

    def fake_create_agent(*, middleware: list[Any], **kwargs: Any) -> BufferedFallbackGraph:
        return BufferedFallbackGraph(middleware)

    monkeypatch.setattr(runtime, "create_agent", fake_create_agent)
    result = AgentApp._for_test(
        AgentSpec(name="fallback-canonical", system_prompt="Fallback system."),
        LLMConfig(model="fallback-canonical"),
        _EmptySemanticChunkModel(model="gpt-4o-mini", api_key="sk-test-not-real", streaming=True),
    ).run("fallback input", renderer="quiet")

    assert result.status == "success", result.error
    assert len(result.usage) == 1
    assert result.usage[0]["model_call_id"] == "graph-canonical-1"
    assert result.usage[0]["input_tokens"] == 3
    assert result.usage[0]["ended_at_utc"] is not None
    assert result.usage[0]["timing_source"] == "graph_fallback"


def test_structured_output_keeps_official_tool_strategy_after_model_copy(monkeypatch: Any) -> None:
    import utils.agent.runtime as runtime
    from langchain.agents.structured_output import ToolStrategy

    class Answer(BaseModel):
        value: str

    class StructuredModel(BaseChatModel):
        @property
        def _llm_type(self) -> str:
            return "structured-tool-strategy-test"

        def bind_tools(self, tools: Any, **kwargs: Any) -> "StructuredModel":
            return self

        def _generate(self, messages: list[Any], stop: list[str] | None = None, run_manager: Any = None, **kwargs: Any) -> ChatResult:
            return ChatResult(
                generations=[
                    ChatGeneration(
                        message=AIMessage(
                            content="",
                            tool_calls=[
                                {
                                    "name": "Answer",
                                    "args": {"value": "ok"},
                                    "id": "structured-call",
                                    "type": "tool_call",
                                }
                            ],
                        )
                    )
                ]
            )

    real_create_agent = runtime.create_agent
    captured: list[Any] = []

    def capture_strategy(**kwargs: Any) -> Any:
        captured.append(kwargs.get("response_format"))
        return real_create_agent(**kwargs)

    monkeypatch.setattr(runtime, "create_agent", capture_strategy)
    result = AgentApp._for_test(
        AgentSpec(name="structured-strategy", system_prompt="Return structure.", output_schema=Answer),
        LLMConfig(model="structured-tool-strategy-test"),
        StructuredModel(),
    ).run("go", renderer="quiet")

    assert result.status == "success", result.error
    assert result.to_dict()["output"] == {"value": "ok"}
    assert len(captured) == 1 and isinstance(captured[0], ToolStrategy)


def test_cancellation_closes_started_model_with_runtime_fallback() -> None:
    class SlowModel(BaseChatModel):
        @property
        def _llm_type(self) -> str:
            return "cancel-realtime-test"

        def bind_tools(self, tools: Any, **kwargs: Any) -> "SlowModel":
            return self

        async def _agenerate(self, messages: list[Any], stop: list[str] | None = None, run_manager: Any = None, **kwargs: Any) -> ChatResult:
            await asyncio.sleep(60)
            return ChatResult(generations=[ChatGeneration(message=AIMessage(content="never"))])

        def _generate(self, messages: list[Any], stop: list[str] | None = None, run_manager: Any = None, **kwargs: Any) -> ChatResult:
            raise AssertionError("async generation required")

    async def scenario() -> tuple[Any, list[AgentEvent]]:
        events: list[AgentEvent] = []
        task = asyncio.create_task(
            AgentApp._for_test(
                AgentSpec(name="cancel-realtime", system_prompt="Answer."),
                LLMConfig(model="cancel-realtime-test"),
                SlowModel(),
            ).arun("go", renderer="quiet", on_event=events.append)
        )
        while not any(event.kind == "model_started" for event in events):
            await asyncio.sleep(0)
        task.cancel()
        return await task, events

    result, events = asyncio.run(scenario())
    assert result.status == "cancelled"
    terminal = next(event for event in events if event.kind == "model_failed")
    assert terminal.data["timing_source"] == "runtime_cancel_fallback"
    assert terminal.data["duration_seconds"] >= 0
    assert result.usage[0]["timing_source"] == "runtime_cancel_fallback"
    assert result.usage[0]["status"] == "cancelled"


def test_provider_error_is_rendered_immediately_after_input(monkeypatch: Any) -> None:
    writer = _ProbeWriter()
    _patch_terminal_console(monkeypatch, writer)

    class FailingStreamModel(ChatOpenAI):
        _entered: asyncio.Event = PrivateAttr()
        _release: asyncio.Event = PrivateAttr()

        def __init__(self) -> None:
            super().__init__(model="gpt-4o-mini", api_key="sk-test-not-real", streaming=True)
            self._entered = asyncio.Event()
            self._release = asyncio.Event()

        async def _astream(self, messages: list[Any], stop: list[str] | None = None, **kwargs: Any):
            self._entered.set()
            await self._release.wait()
            raise RuntimeError("provider probe failure")
            if False:  # pragma: no cover - keeps this an async generator
                yield ChatGenerationChunk(message=AIMessageChunk(content=""))

    async def scenario() -> tuple[Any, list[AgentEvent], str]:
        model = FailingStreamModel()
        events: list[AgentEvent] = []
        task = asyncio.create_task(
            AgentApp._for_test(
                AgentSpec(name="provider-failure", system_prompt="Answer."),
                LLMConfig(model="gpt-4o-mini"),
                model,
            ).arun("provider failure probe", renderer="rich", on_event=events.append)
        )
        await asyncio.wait_for(model._entered.wait(), timeout=5)
        before_failure = writer.snapshot()
        model._release.set()
        result = await asyncio.wait_for(task, timeout=5)
        return result, events, before_failure

    result, events, before_failure = asyncio.run(scenario())
    assert "TURN 1 | MODEL INPUT" in before_failure
    assert "provider failure probe" in before_failure
    failed = next(event for event in events if event.kind == "model_failed")
    assert failed.data["duration_seconds"] >= 0
    assert failed.data["timing_source"] == "provider_callback"
    assert "MODEL OUTPUT | FAILED" in writer.snapshot()
    assert result.status == "failed"
    assert not any(event.kind == "transport_retry_scheduled" for event in events)


def test_retryable_stream_failure_replays_request_without_repeating_tool(
    monkeypatch: Any,
    tmp_path: Path,
) -> None:
    import utils.agent.runtime as runtime

    monkeypatch.setattr(runtime, "_TRANSPORT_RETRY_DELAYS", (0.0, 0.0))
    writer = _ProbeWriter()
    _patch_terminal_console(monkeypatch, writer)
    tool_calls: list[str] = []
    model_calls = {"count": 0}

    def observe(value: str) -> dict[str, str]:
        """Return one deterministic observation."""

        tool_calls.append(value)
        return {"value": value}

    class RetryOnceModel(ChatOpenAI):
        def __init__(self) -> None:
            super().__init__(
                model="gpt-4o-mini",
                api_key="sk-test-not-real",
                streaming=True,
            )

        async def _astream(
            self,
            messages: list[Any],
            stop: list[str] | None = None,
            **kwargs: Any,
        ):
            model_calls["count"] += 1
            if model_calls["count"] == 1:
                yield ChatGenerationChunk(
                    message=AIMessageChunk(content="discarded partial response")
                )
                raise httpx.RemoteProtocolError("incomplete chunked read")
            if model_calls["count"] == 2:
                yield ChatGenerationChunk(
                    message=AIMessageChunk(
                        content="",
                        tool_call_chunks=[
                            {
                                "name": "observe",
                                "args": '{"value":"evidence"}',
                                "id": "observe-once",
                                "index": 0,
                            }
                        ],
                    )
                )
                return
            yield ChatGenerationChunk(
                message=AIMessageChunk(content="completed after transport recovery")
            )

    model = RetryOnceModel()
    audit = tmp_path / "transport-retry.jsonl"
    events: list[AgentEvent] = []
    result = AgentApp._for_test(
        AgentSpec(
            name="transport-retry",
            system_prompt="Use observe once, then answer.",
            tools=(observe,),
        ),
        LLMConfig(model="gpt-4o-mini"),
        model,
    ).run(
        "run",
        renderer="rich",
        on_event=events.append,
        audit_out=audit,
    )

    assert result.status == "success", result.error
    assert model_calls["count"] == 3
    assert tool_calls == ["evidence"]
    assert result.final_text == "completed after transport recovery"
    assert "discarded partial response" not in result.final_text
    assert result.model_calls_used == 3
    assert [item["status"] for item in result.usage] == [
        "failed",
        "completed",
        "completed",
    ]
    retries = [
        event for event in events if event.kind == "transport_retry_scheduled"
    ]
    recovered = [
        event for event in events if event.kind == "transport_retry_recovered"
    ]
    assert len(retries) == len(recovered) == 1
    assert retries[0].data["attempt_no"] == 1
    assert retries[0].data["next_attempt_no"] == 2
    assert retries[0].data["partial_response_observed"] is True
    assert recovered[0].data["attempt_no"] == 2
    assert retries[0].data["turn"] == recovered[0].data["turn"] == 1
    assert (
        retries[0].data["request_fingerprint"]
        == recovered[0].data["request_fingerprint"]
    )
    records = [
        json.loads(line)
        for line in audit.read_text(encoding="utf-8").splitlines()
    ]
    retry_records = [
        item for item in records if item.get("record") == "transport_retry"
    ]
    assert [item["operation"] for item in retry_records] == [
        "scheduled",
        "recovered",
    ]
    completed_tools = [
        item
        for item in records
        if item.get("record") == "action"
        and item.get("name") == "observe"
        and item.get("status") == "completed"
    ]
    assert len(completed_tools) == 1
    rendered = writer.snapshot()
    assert "MODEL TRANSPORT | RETRY SCHEDULED" in rendered
    assert "MODEL TRANSPORT | RECOVERED" in rendered


def test_retryable_stream_failure_stops_after_two_replays(
    monkeypatch: Any,
    tmp_path: Path,
) -> None:
    import utils.agent.runtime as runtime

    monkeypatch.setattr(runtime, "_TRANSPORT_RETRY_DELAYS", (0.0, 0.0))
    model_calls = {"count": 0}

    class AlwaysFailingModel(ChatOpenAI):
        def __init__(self) -> None:
            super().__init__(
                model="gpt-4o-mini",
                api_key="sk-test-not-real",
                streaming=True,
            )

        async def _astream(
            self,
            messages: list[Any],
            stop: list[str] | None = None,
            **kwargs: Any,
        ):
            model_calls["count"] += 1
            yield ChatGenerationChunk(message=AIMessageChunk(content="partial"))
            raise httpx.RemoteProtocolError("incomplete chunked read")

    model = AlwaysFailingModel()
    events: list[AgentEvent] = []
    audit = tmp_path / "transport-retry-exhausted.jsonl"
    result = AgentApp._for_test(
        AgentSpec(name="transport-retry-exhausted", system_prompt="Answer."),
        LLMConfig(model="gpt-4o-mini"),
        model,
    ).run(
        "run",
        renderer="quiet",
        on_event=events.append,
        audit_out=audit,
    )

    assert result.status == "failed"
    assert result.error and result.error["code"] == "provider_error"
    assert model_calls["count"] == 3
    assert result.model_calls_used == 3
    assert len(
        [event for event in events if event.kind == "transport_retry_scheduled"]
    ) == 2
    exhausted = [
        event for event in events if event.kind == "transport_retry_exhausted"
    ]
    assert len(exhausted) == 1
    assert exhausted[0].data["attempt_no"] == 3
    records = [
        json.loads(line)
        for line in audit.read_text(encoding="utf-8").splitlines()
    ]
    retry_records = [
        item for item in records if item.get("record") == "transport_retry"
    ]
    assert [item["operation"] for item in retry_records] == [
        "scheduled",
        "scheduled",
        "exhausted",
    ]


def test_tool_error_is_rendered_after_request_without_fake_result(monkeypatch: Any, tmp_path: Path) -> None:
    writer = _ProbeWriter()
    _patch_terminal_console(monkeypatch, writer)
    probe = _RealtimeProbe(writer)
    entered_snapshot: list[str] = []
    events: list[AgentEvent] = []

    def observe(value: str) -> dict[str, str]:
        """Raise after the model has requested this tool."""

        entered_snapshot.append(writer.snapshot())
        raise RuntimeError("tool probe failure")

    async def scenario() -> Any:
        app = AgentApp._for_test(
            AgentSpec(name="tool-error", system_prompt="Use the tool.", tools=(observe,)),
            LLMConfig(model="gpt-4o-mini"),
            _BoundBarrierChatModel(probe),
        )
        task = asyncio.create_task(
            app.arun(
                "tool error probe",
                renderer="rich",
                on_event=events.append,
                audit_out=tmp_path / "tool-error.jsonl",
            )
        )
        try:
            await asyncio.wait_for(probe.first_transport_entered.wait(), timeout=5)
            probe.release_first_model.set()
            return await asyncio.wait_for(task, timeout=5)
        finally:
            probe.release_first_model.set()
            if not task.done():
                with suppress(Exception):
                    await asyncio.wait_for(task, timeout=5)

    result = asyncio.run(scenario())
    assert result.status == "failed"
    assert result.error and result.error["code"] == "tool_error"
    assert entered_snapshot and "MODEL OUTPUT | TOOL CALL" in entered_snapshot[0]
    failed = next(event for event in events if event.kind == "tool_failed")
    assert failed.data["status"] == "failed"
    assert "TOOL ERROR" in writer.snapshot()
    assert not any(event.kind == "tool_completed" for event in events)
    records = [
        json.loads(line)
        for line in (tmp_path / "tool-error.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    action = next(record for record in records if record.get("record") == "action")
    assert action["status"] == "failed"
    assert action["error"]["code"] == "tool_error"
    assert action["started_at"] and action["finished_at"]
    assert action["duration_seconds"] >= 0


def test_tool_execution_cancellation_closes_without_fake_result() -> None:
    tool_entered = asyncio.Event()
    release_tool = asyncio.Event()
    events: list[AgentEvent] = []

    async def observe(value: str) -> dict[str, str]:
        """Wait inside a cancellable tool."""

        tool_entered.set()
        await release_tool.wait()
        return {"value": value}

    async def scenario() -> Any:
        writer = _ProbeWriter()
        probe = _RealtimeProbe(writer)
        app = AgentApp._for_test(
            AgentSpec(name="cancel-tool", system_prompt="Use the tool.", tools=(observe,)),
            LLMConfig(model="gpt-4o-mini"),
            _BoundBarrierChatModel(probe),
        )
        task = asyncio.create_task(app.arun("cancel tool", renderer="quiet", on_event=events.append))
        await asyncio.wait_for(probe.first_transport_entered.wait(), timeout=5)
        probe.release_first_model.set()
        await asyncio.wait_for(tool_entered.wait(), timeout=5)
        task.cancel()
        result = await task
        release_tool.set()
        return result

    result = asyncio.run(scenario())
    assert result.status == "cancelled"
    assert len(result.tool_calls) == 1
    record = result.tool_calls[0]
    assert record["status"] == "cancelled"
    assert "result" not in record
    assert record["started_at"] and record["finished_at"]
    assert record["duration_seconds"] >= 0
    assert any(event.kind == "tool_failed" and event.data["status"] == "cancelled" for event in events)


def test_cancellation_between_chunks_keeps_partial_text_without_terminal_duplication(monkeypatch: Any) -> None:
    writer = _ProbeWriter()
    probe = _RealtimeProbe(writer)
    _patch_terminal_console(monkeypatch, writer)
    events: list[AgentEvent] = []

    def observe(value: str) -> dict[str, str]:
        """Return immediately before the cancellable model turn."""

        return {"value": value}

    async def scenario() -> Any:
        task = asyncio.create_task(
            AgentApp._for_test(
                AgentSpec(name="cancel-between-chunks", system_prompt="Use the tool.", tools=(observe,)),
                LLMConfig(model="gpt-4o-mini"),
                _BoundBarrierChatModel(probe),
            ).arun("cancel after first chunk", renderer="rich", on_event=events.append)
        )
        await asyncio.wait_for(probe.first_transport_entered.wait(), timeout=5)
        probe.release_first_model.set()
        await asyncio.wait_for(probe.second_transport_entered.wait(), timeout=5)
        await asyncio.wait_for(probe.first_chunk_processed.wait(), timeout=5)
        assert "first segment" in writer.snapshot()
        assert "second segment" not in writer.snapshot()
        task.cancel()
        return await task

    result = asyncio.run(scenario())
    assert result.status == "cancelled"
    assert "first segment" in writer.snapshot()
    assert "second segment" not in writer.snapshot()
    second_terminals = [
        event
        for event in events
        if event.data.get("turn") == 2 and event.kind in {"model_completed", "model_failed"}
    ]
    assert len(second_terminals) == 1
    assert second_terminals[0].kind == "model_failed"
    assert second_terminals[0].data["timing_source"] == "runtime_cancel_fallback"


def test_cancellation_during_official_compact_closes_summary_trace(tmp_path: Path) -> None:
    class CancelCompactModel(BaseChatModel):
        calls: int = Field(default=0)
        _summary_started: asyncio.Event = PrivateAttr()

        def __init__(self) -> None:
            super().__init__()
            self._summary_started = asyncio.Event()

        @property
        def _llm_type(self) -> str:
            return "cancel-compact-test"

        def bind_tools(self, tools: Any, **kwargs: Any) -> "CancelCompactModel":
            return self

        async def _agenerate(self, messages: list[Any], **kwargs: Any) -> ChatResult:
            is_summary = any("Context Extraction Assistant" in str(getattr(message, "content", "")) for message in messages)
            if is_summary:
                self._summary_started.set()
                await asyncio.Event().wait()
            self.calls += 1
            if self.calls < 50:
                message = AIMessage(
                    content="",
                    tool_calls=[{"name": "probe", "args": {}, "id": f"compact-call-{self.calls}", "type": "tool_call"}],
                )
            else:
                message = AIMessage(content="done")
            return ChatResult(generations=[ChatGeneration(message=message)])

        def _generate(self, *args: Any, **kwargs: Any) -> ChatResult:
            raise AssertionError("async generation required")

    def probe() -> str:
        return "x" * 500

    async def scenario() -> tuple[Any, list[AgentEvent]]:
        events: list[AgentEvent] = []
        audit = tmp_path / "cancel-compact.jsonl"
        model = CancelCompactModel()
        task = asyncio.create_task(
            AgentApp._for_test(
                AgentSpec(name="cancel-compact", system_prompt="Use the tool.", tools=(probe,)),
                LLMConfig(model="cancel-compact-test", context_window_tokens=10_000, max_output_tokens=20),
                model,
            ).arun("run", renderer="quiet", compact_trigger_ratio=0.5, audit_out=audit, on_event=events.append)
        )
        await asyncio.wait_for(model._summary_started.wait(), timeout=10)
        task.cancel()
        return await task, events

    result, events = asyncio.run(scenario())
    assert result.status == "cancelled"
    compact_failed = next(event for event in events if event.kind == "compaction_failed")
    compact_model_failed = next(event for event in events if event.kind == "model_failed" and event.data.get("call_kind") == "compact")
    assert compact_failed.data["compaction_id"] == compact_model_failed.data["compaction_id"]
    assert compact_model_failed.data["timing_source"] == "runtime_cancel_fallback"
    compact_usage = [item for item in result.usage if item["call_kind"] == "compact"]
    assert len(compact_usage) == 1
    assert compact_usage[0]["status"] == "cancelled"
    assert compact_usage[0]["timing_source"] == "runtime_cancel_fallback"
    records = [json.loads(line) for line in (tmp_path / "cancel-compact.jsonl").read_text(encoding="utf-8").splitlines()]
    compact_records = [record for record in records if record.get("record") == "context" and record.get("operation") == "compact"]
    assert {record.get("status") for record in compact_records} >= {"started", "failed"}
    assert records[-1]["record"] == "finish"


def test_assistant_preamble_and_tool_call_share_one_output_phase(monkeypatch: Any) -> None:
    writer = _ProbeWriter()
    _patch_terminal_console(monkeypatch, writer)
    events: list[AgentEvent] = []

    class PreambleToolModel(ChatOpenAI):
        calls: int = Field(default=0)

        async def _astream(self, messages: list[Any], stop: list[str] | None = None, **kwargs: Any):
            self.calls += 1
            if self.calls == 1:
                yield ChatGenerationChunk(message=AIMessageChunk(content="先检查证据。"))
                yield ChatGenerationChunk(
                    message=AIMessageChunk(
                        content="",
                        tool_call_chunks=[
                            {
                                "name": "probe",
                                "args": '{"value":"evidence"}',
                                "id": "preamble-call",
                                "index": 0,
                            }
                        ],
                    )
                )
            else:
                yield ChatGenerationChunk(message=AIMessageChunk(content="完成。"))

    def probe(value: str) -> dict[str, str]:
        """Return the requested evidence."""

        return {"value": value}

    result = AgentApp._for_test(
        AgentSpec(name="preamble-tool", system_prompt="Use evidence.", tools=(probe,)),
        LLMConfig(model="gpt-4o-mini"),
        PreambleToolModel(model="gpt-4o-mini", api_key="sk-test-not-real", streaming=True),
    ).run("go", renderer="rich", on_event=events.append)

    assert result.status == "success", result.error
    first_output_events = [
        event.kind
        for event in events
        if event.data.get("turn") == 1
        and event.kind in {"model_text", "model_completed", "tool_started", "tool_completed"}
    ]
    assert first_output_events == ["model_text", "model_completed", "tool_started", "tool_completed"]
    first_completed = next(
        event for event in events if event.kind == "model_completed" and event.data.get("turn") == 1
    )
    assert first_completed.data["tool_requests"][0]["tool_call_id"] == "preamble-call"
    prompts = [event.data["prompt"] for event in events if event.kind == "model_started"]
    assert "[tool]" in prompts[1]
    assert "[assistant]" not in prompts[1]


def test_legacy_tool_delta_counts_as_first_public_chunk() -> None:
    class LegacyToolModel:
        def __init__(self) -> None:
            self.calls = 0

        def bind_tools(self, tools: Any, **kwargs: Any) -> "LegacyToolModel":
            return self

        async def astream(self, messages: list[Any], **kwargs: Any):
            self.calls += 1
            if self.calls == 1:
                yield AIMessageChunk(
                    content="",
                    tool_call_chunks=[
                        {"name": "probe", "args": '{"value":"x"}', "id": "legacy-call", "index": 0}
                    ],
                )
            else:
                yield AIMessageChunk(content="done")

    def probe(value: str) -> str:
        """Return a legacy observation."""

        return value

    events: list[AgentEvent] = []
    result = AgentApp._for_test(
        AgentSpec(name="legacy-tool-delta", system_prompt="Use the tool.", tools=(probe,)),
        LLMConfig(model="legacy-test"),
        LegacyToolModel(),
    ).run("go", renderer="quiet", on_event=events.append)

    assert result.status == "success", result.error
    first = next(
        event
        for event in events
        if event.kind == "model_completed" and event.data.get("turn") == 1
    )
    assert first.data["first_chunk_at_utc"] is not None
    assert first.data["time_to_first_chunk_seconds"] is not None


def test_concurrent_runs_keep_callbacks_turns_and_messages_isolated() -> None:
    shared = SimpleNamespace(arrived=0, release=asyncio.Event())

    class ConcurrentModel(BaseChatModel):
        @property
        def _llm_type(self) -> str:
            return "concurrent-run-test"

        def bind_tools(self, tools: Any, **kwargs: Any) -> "ConcurrentModel":
            return self

        async def _agenerate(self, messages: list[Any], stop: list[str] | None = None, run_manager: Any = None, **kwargs: Any) -> ChatResult:
            shared.arrived += 1
            if shared.arrived == 2:
                shared.release.set()
            await shared.release.wait()
            prompt = next(message.content for message in reversed(messages) if isinstance(message, HumanMessage))
            return ChatResult(generations=[ChatGeneration(message=AIMessage(content=f"answer:{prompt}"))])

        def _generate(self, messages: list[Any], stop: list[str] | None = None, run_manager: Any = None, **kwargs: Any) -> ChatResult:
            raise AssertionError("async generation required")

    async def scenario() -> tuple[Any, Any, list[AgentEvent], list[AgentEvent], ConcurrentModel]:
        model = ConcurrentModel()
        app = AgentApp._for_test(
            AgentSpec(name="concurrent", system_prompt="Answer."),
            LLMConfig(model="concurrent-run-test"),
            model,
        )
        left_events: list[AgentEvent] = []
        right_events: list[AgentEvent] = []
        left, right = await asyncio.gather(
            app.arun("LEFT-SENTINEL", renderer="quiet", on_event=left_events.append),
            app.arun("RIGHT-SENTINEL", renderer="quiet", on_event=right_events.append),
        )
        return left, right, left_events, right_events, model

    left, right, left_events, right_events, model = asyncio.run(scenario())
    assert left.final_text == "answer:LEFT-SENTINEL"
    assert right.final_text == "answer:RIGHT-SENTINEL"
    assert [event.data["turn"] for event in left_events if event.kind == "model_started"] == [1]
    assert [event.data["turn"] for event in right_events if event.kind == "model_started"] == [1]
    assert "RIGHT-SENTINEL" not in next(event.data["prompt"] for event in left_events if event.kind == "model_started")
    assert "LEFT-SENTINEL" not in next(event.data["prompt"] for event in right_events if event.kind == "model_started")
    assert model.callbacks is None or model.callbacks == []


def test_repeated_compactions_keep_unique_model_and_audit_links(tmp_path: Path) -> None:
    class RepeatedCompactModel(BaseChatModel):
        calls: int = Field(default=0)

        @property
        def _llm_type(self) -> str:
            return "repeated-compact-test"

        def bind_tools(self, tools: Any, **kwargs: Any) -> "RepeatedCompactModel":
            return self

        def _generate(self, messages: list[Any], stop: list[str] | None = None, run_manager: Any = None, **kwargs: Any) -> ChatResult:
            self.calls += 1
            if any(
                "Context Extraction Assistant" in str(getattr(message, "content", ""))
                for message in messages
            ):
                answer = AIMessage(content=f"summary-{self.calls}")
            elif self.calls <= 35:
                answer = AIMessage(
                    content="",
                    tool_calls=[
                        {
                            "name": "probe",
                            "args": {"value": self.calls},
                            "id": f"call-{self.calls}",
                            "type": "tool_call",
                        }
                    ],
                )
            else:
                answer = AIMessage(content="done")
            return ChatResult(generations=[ChatGeneration(message=answer)])

    def probe(value: int) -> int:
        """Return a compact-loop observation."""

        return value

    events: list[AgentEvent] = []
    audit = tmp_path / "compact-timing.jsonl"
    result = AgentApp._for_test(
        AgentSpec(name="repeated-compact", system_prompt="Keep probing.", tools=(probe,)),
        LLMConfig(model="repeated-compact-test", context_window_tokens=1020, max_output_tokens=20),
        RepeatedCompactModel(),
    ).run(
        "run",
        renderer="quiet",
        compact_trigger_ratio=0.5,
        audit_out=audit,
        on_event=events.append,
    )

    assert result.status == "success", result.error
    starts = [event for event in events if event.kind == "compaction_started"]
    assert len(starts) >= 2
    compact_ids = [event.data["compaction_id"] for event in starts]
    assert len(compact_ids) == len(set(compact_ids))
    for compaction_id in compact_ids:
        model_start = next(
            event
            for event in events
            if event.kind == "model_started" and event.data.get("compaction_id") == compaction_id
        )
        model_end = next(
            event
            for event in events
            if event.kind == "model_completed" and event.data.get("compaction_id") == compaction_id
        )
        compact_end = next(
            event
            for event in events
            if event.kind == "compaction_completed" and event.data.get("compaction_id") == compaction_id
        )
        assert model_start.data["model_call_id"] == model_end.data["model_call_id"]
        assert compact_end.data["model_call_id"] == model_end.data["model_call_id"]
        assert compact_end.data["duration_seconds"] == model_end.data["duration_seconds"]
        assert compact_end.data["timing_source"] == "provider_callback"

    records = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
    for compaction_id in compact_ids:
        linked = [
            record
            for record in records
            if record.get("record") == "context"
            and record.get("operation") == "compact"
            and record.get("compaction_id") == compaction_id
        ]
        assert {record["status"] for record in linked} >= {
            "started",
            "replacement_applied",
            "completed",
        }
        completed = next(record for record in linked if record["status"] == "completed")
        assert completed["model_call_id"]
        assert completed["duration_seconds"] >= 0
