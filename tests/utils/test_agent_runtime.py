from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import Field
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessageChunk
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from utils.agent import AgentApp, AgentSpec
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

    result = app.run("read", audit_out=audit, result_out=result_path, renderer="quiet")

    assert result.status == "success"
    assert result.academic_eligible is True
    assert result.tool_calls[0]["name"] == "lookup"
    records = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
    assert [record["record"] for record in records] == ["context", "decision", "action", "decision", "finish"]
    assert all("heartbeat" not in record for record in records)
    assert json.loads(result_path.read_text(encoding="utf-8"))["status"] == "success"


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
