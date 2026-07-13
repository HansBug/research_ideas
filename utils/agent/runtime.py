from __future__ import annotations

import asyncio
import contextlib
import hashlib
import inspect
import json
import logging
import math
import os
import re
import tempfile
import time
import uuid
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TypeVar
from urllib.parse import urlsplit

from pydantic import BaseModel

from utils.llm import LLMConfig, LLMRegistry

try:
    from langchain.agents import create_agent
    from langchain.agents.middleware import AgentMiddleware
    from langchain_core.language_models import BaseChatModel
    from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessage, ToolMessage
    from langchain_core.outputs import ChatGeneration, ChatResult
    from langchain_core.tools import StructuredTool
    from pydantic import PrivateAttr
except Exception:  # pragma: no cover - import errors are reported at construction time
    create_agent = None  # type: ignore[assignment]
    AgentMiddleware = object  # type: ignore[assignment,misc]
    BaseChatModel = AIMessage = AIMessageChunk = BaseMessage = ToolMessage = object  # type: ignore[assignment,misc]
    ChatGeneration = ChatResult = object  # type: ignore[assignment,misc]
    StructuredTool = object  # type: ignore[assignment,misc]
    PrivateAttr = lambda *args, **kwargs: None  # type: ignore[assignment]


T = TypeVar("T")
_MODEL_OPTIONS = frozenset({"streaming", "stream_usage", "timeout", "max_retries"})
_MODEL_CALL_OPTIONS = frozenset({"temperature", "top_p", "max_tokens", "max_completion_tokens", "stop", "seed", "reasoning_effort", "verbosity"})
_IDENTITY_KEYS = frozenset(
    {"model", "base_url", "api_key", "headers", "authorization", "openai_api_key", "default_headers"}
)
_SECRET_KEY = re.compile(r"(api[_-]?key|authorization|token|secret|password|cookie|headers?)", re.I)
_USAGE_KEY = re.compile(
    r"^(?:usage|token[_-]?usage|(?:prompt|completion|input|output|total|reasoning|cached|cache_read_input|cache_creation_input|accepted_prediction|rejected_prediction|audio|text)[_-]?tokens?(?:[_-].*)?)$",
    re.I,
)
_NON_SECRET_FLAG_KEY = re.compile(r"(?:configured|present|enabled|set|available)$", re.I)
_ENDPOINT_KEY = re.compile(r"(?:base[_-]?url|api[_-]?url|endpoint)", re.I)
_SECRET_VALUE = re.compile(r"\b(?:sk|sess|key)[-_][A-Za-z0-9_-]{8,}\b", re.I)
_DEFAULT_GRAPH_RECURSION_LIMIT = 1_000_000
_DEFAULT_CONTEXT_ROLLOVER_LIMIT = 1_000_000


class AgentError(Exception):
    """安全、可序列化的运行错误。"""

    def __init__(self, code: str, message: str, *, details: Mapping[str, Any] | None = None):
        self.code = code
        self.message = message
        self.details = dict(details or {})
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True)
class AgentSpec:
    name: str
    system_prompt: str
    tools: tuple[Any, ...] = ()
    output_schema: type[BaseModel] | None = None
    limits: Mapping[str, int | float | None] | None = None
    require_tool_call: bool = False

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.system_prompt.strip():
            raise ValueError("agent_spec_invalid: name and system_prompt are required")
        names = tuple(_tool_name(tool) for tool in self.tools)
        if len(names) != len(set(names)):
            raise ValueError("agent_spec_invalid: duplicate tool name")
        limits = dict(self.limits or {})
        allowed = {"model_calls", "tool_calls", "turns", "seconds"}
        unknown = set(limits) - allowed
        if unknown:
            raise ValueError(f"agent_spec_invalid: unknown limit keys: {sorted(unknown)}")
        if any(value is not None and (not isinstance(value, (int, float)) or value <= 0) for value in limits.values()):
            raise ValueError("agent_spec_invalid: limits must be positive")
        object.__setattr__(self, "limits", limits)

    @property
    def tool_names(self) -> tuple[str, ...]:
        return tuple(_tool_name(tool) for tool in self.tools)


@dataclass(frozen=True)
class AgentEvent:
    run_id: str
    seq: int
    timestamp: datetime
    kind: str
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "seq": self.seq,
            "timestamp": self.timestamp.isoformat(),
            "kind": self.kind,
            "data": _safe_json(self.data),
        }


@dataclass
class AgentRunResult:
    run_id: str
    status: str
    output: Any
    final_text: str
    tool_calls: list[dict[str, Any]]
    usage: dict[str, Any] | None
    error: dict[str, Any] | None
    real_llm: bool
    model: str
    observed_model: str | None
    academic_eligible: bool
    context_manifest_hash: str | None

    def __post_init__(self) -> None:
        # Public result objects retain the normal model/tool shape while protecting secrets.
        self.output = _redact_public(self.output)
        self.final_text = _redact(self.final_text)
        self.tool_calls = _redact_public(self.tool_calls)
        self.usage = _redact_public(self.usage)
        self.error = _redact_public(self.error)

    def require_output(self) -> T:
        if self.status != "success" or self.output is None:
            error = self.error or {"code": "missing_output", "message": "run has no successful output"}
            raise AgentError(str(error.get("code", "missing_output")), str(error.get("message", "missing output")))
        return self.output

    def to_dict(self) -> dict[str, Any]:
        return _redact(
            _safe_json(
                {
                    "run_id": self.run_id,
                    "status": self.status,
                    "output": self.output,
                    "final_text": self.final_text,
                    "tool_calls": self.tool_calls,
                    "usage": self.usage,
                    "error": self.error,
                    "real_llm": self.real_llm,
                    "model": self.model,
                    "observed_model": self.observed_model,
                    "academic_eligible": self.academic_eligible,
                    "context_manifest_hash": self.context_manifest_hash,
                }
            )
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, allow_nan=False)


def _tool_name(tool: Any) -> str:
    name = getattr(tool, "name", None) or getattr(tool, "__name__", None)
    if not name:
        raise ValueError("agent_spec_invalid: every tool needs a name")
    return str(name)


def _tool_description(tool: Any) -> str:
    description = str(getattr(tool, "description", None) or inspect.getdoc(tool) or "").strip()
    return description or f"Invoke the registered tool '{_tool_name(tool)}'."


def _tool_schema(tool: Any) -> dict[str, Any]:
    schema = getattr(tool, "args_schema", None)
    if schema is not None and hasattr(schema, "model_json_schema"):
        return schema.model_json_schema()
    try:
        return {"type": "object", "properties": {name: {"type": "string"} for name in inspect.signature(tool).parameters}}
    except (TypeError, ValueError):
        return {"type": "object"}


def _langchain_tools(tools: Sequence[Any]) -> list[Any]:
    """Give bare callables a usable description before LangGraph converts them."""

    converted: list[Any] = []
    for tool in tools:
        if getattr(tool, "name", None):
            converted.append(tool)
            continue
        description = inspect.getdoc(tool) or _tool_name(tool)
        converted.append(StructuredTool.from_function(tool, description=description))
    return converted


def _validate_model_options(options: Mapping[str, Any] | None) -> None:
    supplied = set(options or {})
    forbidden = supplied & _IDENTITY_KEYS
    unknown = supplied - _MODEL_OPTIONS
    if unknown or forbidden:
        raise ValueError(f"model_options_not_allowed: {sorted(unknown or forbidden)}")


def _validate_model_call_options(options: Mapping[str, Any] | None) -> None:
    supplied = set(options or {})
    forbidden = supplied & _IDENTITY_KEYS
    unknown = supplied - _MODEL_CALL_OPTIONS
    if forbidden or unknown:
        raise ValueError(f"model_call_options_not_allowed: {sorted(forbidden or unknown)}")


def _is_deepseek_config(config: LLMConfig) -> bool:
    host = (urlsplit(config.base_url or "").hostname or "").lower()
    return host.endswith("deepseek.com") or config.model.lower().startswith("deepseek-")


def _is_openai_reasoning_model(config: LLMConfig) -> bool:
    """Identify OpenAI reasoning model IDs whose official API accepts ``none``."""

    model = config.model.lower()
    return not _is_deepseek_config(config) and model.startswith(("gpt-5", "o1", "o3", "o4"))


def _resolve_inference_options(
    config: LLMConfig,
    *,
    model_call_options: Mapping[str, Any] | None,
    think_mode: bool,
    reasoning_effort: str | None,
) -> tuple[dict[str, Any], bool | None]:
    if not isinstance(think_mode, bool):
        raise ValueError("think_mode must be a boolean")
    if reasoning_effort is not None and not isinstance(reasoning_effort, str):
        raise ValueError("reasoning_effort must be a string or None")
    if reasoning_effort is not None and not think_mode:
        raise ValueError("reasoning_effort requires think_mode=True")
    options = dict(model_call_options or {})
    if reasoning_effort is not None:
        existing = options.get("reasoning_effort")
        if existing is not None and existing != reasoning_effort:
            raise ValueError("reasoning_effort was supplied twice with different values")
        options["reasoning_effort"] = reasoning_effort

    deepseek = _is_deepseek_config(config)
    effective_think_mode = think_mode
    if not think_mode and _is_openai_reasoning_model(config):
        # OpenAI documents gpt-5.5's default as medium.  Pin ``none`` for the
        # framework's explicit think-off default instead of relying on a
        # provider default that would change the experiment semantics.
        options["reasoning_effort"] = "none"
    if deepseek and effective_think_mode is not None:
        extra_body = dict(options.get("extra_body") or {})
        thinking = dict(extra_body.get("thinking") or {})
        thinking["type"] = "enabled" if effective_think_mode else "disabled"
        extra_body["thinking"] = thinking
        options["extra_body"] = extra_body
    return options, effective_think_mode


def _hash_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _normalize_context(context: Sequence[str | Mapping[str, Any]] | None) -> list[dict[str, Any]]:
    pages: list[dict[str, Any]] = []
    seen: set[str] = set()
    snapshot_ref: str | None = None
    for index, raw in enumerate(context or (), start=1):
        if isinstance(raw, str):
            page = {"id": f"page-{index}", "text": raw}
        elif isinstance(raw, Mapping):
            page = dict(raw)
        else:
            raise ValueError("context_invalid: page must be a string or mapping")
        text = page.get("text")
        if not isinstance(text, str):
            raise ValueError("context_invalid: page.text must be a string")
        page_id = str(page.get("id") or f"page-{index}")
        if page_id in seen:
            raise ValueError("context_duplicate_id")
        seen.add(page_id)
        expected_hash = _hash_text(text)
        if page.get("hash") is not None and page["hash"] != expected_hash:
            raise ValueError("context_hash_mismatch")
        current_snapshot = page.get("snapshot")
        if snapshot_ref is None:
            snapshot_ref = current_snapshot
        elif current_snapshot != snapshot_ref:
            raise ValueError("context_snapshot_drift")
        source = page.get("source")
        if isinstance(source, str) and (source.startswith("/") or ".." in source.split("/")):
            raise ValueError("context_source_invalid")
        pages.append(
            {
                "id": page_id,
                "text": text,
                "hash": expected_hash,
                "snapshot": current_snapshot,
                "cursor": page.get("cursor"),
                "next_cursor": page.get("next_cursor"),
                "source": source,
            }
        )
    return pages


def _build_context_manifest(pages: Sequence[Mapping[str, Any]]) -> str:
    payload = [
        {key: page.get(key) for key in ("id", "hash", "snapshot", "cursor", "next_cursor")}
        for page in pages
    ]
    return _hash_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def _safe_json(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return _safe_json(value.model_dump(mode="json"))
    if isinstance(value, Mapping):
        return {str(key): _safe_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_safe_json(item) for item in value]
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("json_export_failed: non-finite float")
        return value
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)
    return repr(value)


def _redact(value: Any, *, key: str | None = None) -> Any:
    if key and _is_secret_key(key):
        return "[redacted]"
    if key and _ENDPOINT_KEY.search(key) and isinstance(value, str):
        return _redact_text(value, redact_endpoints=True)
    if isinstance(value, Mapping):
        return {str(k): _redact(v, key=str(k)) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_redact(item) for item in value]
    if isinstance(value, str):
        return _redact_text(value)
    return value


def _is_secret_key(key: str) -> bool:
    return bool(_SECRET_KEY.search(key) and not _USAGE_KEY.fullmatch(key) and not _NON_SECRET_FLAG_KEY.search(key))


def _model_output_messages(value: Any) -> list[Any]:
    """Return model messages from standard LangChain event payloads."""

    if isinstance(value, BaseMessage):
        return [value]
    generations = getattr(value, "generations", None)
    if generations:
        messages: list[Any] = []
        for generation_group in generations:
            for generation in generation_group if isinstance(generation_group, (list, tuple)) else (generation_group,):
                message = getattr(generation, "message", None)
                if isinstance(message, BaseMessage):
                    messages.append(message)
        return messages
    return _messages_from_event(value)


def _model_metadata(value: Any) -> tuple[dict[str, Any] | None, str | None]:
    """Read usage/model identity from LangChain's standard message metadata."""

    usage: dict[str, Any] | None = None
    observed_model: str | None = None
    for message in _model_output_messages(value):
        response_metadata = getattr(message, "response_metadata", {}) or {}
        if isinstance(response_metadata, Mapping):
            usage_value = response_metadata.get("token_usage") or response_metadata.get("usage")
            if isinstance(usage_value, Mapping):
                usage = dict(usage_value)
            observed_model = observed_model or response_metadata.get("model_name") or response_metadata.get("model")
        usage_metadata = getattr(message, "usage_metadata", None)
        if usage is None and isinstance(usage_metadata, Mapping):
            usage = dict(usage_metadata)
    return usage, observed_model if isinstance(observed_model, str) else None


def _redact_text(value: str, *, redact_endpoints: bool = False) -> str:
    value = _SECRET_VALUE.sub("[redacted_secret]", value)
    lowered = value.lower()
    if "bearer " in lowered:
        cursor = 0
        pieces: list[str] = []
        while True:
            marker = lowered.find("bearer ", cursor)
            if marker < 0:
                pieces.append(value[cursor:])
                break
            end = marker + len("bearer ")
            while end < len(value) and not value[end].isspace():
                end += 1
            pieces.extend((value[cursor:marker], "Bearer [redacted_bearer]"))
            cursor = end
        value = "".join(pieces)
    if redact_endpoints:
        lowered = value.lower()
        cursor = 0
        pieces = []
        while True:
            starts = [index for index in (lowered.find("http://", cursor), lowered.find("https://", cursor)) if index >= 0]
            if not starts:
                pieces.append(value[cursor:])
                break
            start = min(starts)
            end = start
            while end < len(value) and not value[end].isspace() and value[end] not in "'\"},)]":
                end += 1
            pieces.extend((value[cursor:start], "[redacted_endpoint]"))
            cursor = end
        value = "".join(pieces)
    return value


def _redact_public(value: Any) -> Any:
    safe = _redact(_safe_json(value))
    if isinstance(value, BaseModel):
        try:
            return type(value).model_validate(safe)
        except Exception:
            return safe
    return safe


def _redact_exception_text(value: str) -> str:
    return _redact_text(value, redact_endpoints=True)


def _exception_details(exc: BaseException) -> dict[str, Any]:
    module = type(exc).__module__.lower()
    source = "provider" if getattr(exc, "status_code", None) is not None or "openai" in module or "httpx" in module else "runtime"
    details: dict[str, Any] = {"source": source, "type": type(exc).__name__}
    if message := str(exc):
        details["message"] = _redact_exception_text(message)
    for attribute in ("status_code", "code", "request_id"):
        value = getattr(exc, attribute, None)
        if value is not None and isinstance(value, (str, int, float, bool)):
            details[attribute] = _redact(value)
    body = getattr(exc, "body", None)
    if isinstance(body, Mapping):
        safe_body: dict[str, Any] = {}
        for key in ("type", "code", "status_code", "request_id", "param", "message"):
            if key in body:
                value = body[key]
                safe_body[key] = _redact_exception_text(value) if isinstance(value, str) else _redact(value, key=key)
        if safe_body:
            details["body"] = safe_body
    return details


def _atomic_write(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(_safe_json(payload), stream, ensure_ascii=False, sort_keys=True, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except Exception:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(temporary)
        raise


class _AuditWriter:
    def __init__(self, path: Path | None, run_id: str):
        self.path = path
        self.run_id = run_id
        self.temporary: Path | None = None
        try:
            if path is not None:
                if path.exists() and not path.is_file():
                    raise OSError("audit output path is not a file")
                path.parent.mkdir(parents=True, exist_ok=True)
                fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
                self.temporary = Path(temporary)
                self.stream = os.fdopen(fd, "w", encoding="utf-8")
            else:
                self.stream = None
        except OSError as exc:
            raise AgentError("audit_write_failed", "audit output cannot be opened") from exc
        self.order = 0

    @property
    def enabled(self) -> bool:
        return self.stream is not None

    def write(self, record: Mapping[str, Any]) -> None:
        if self.stream is None:
            return
        self.order += 1
        payload = _redact(_safe_json({"run_id": self.run_id, "order": self.order, **record}))
        self.stream.write(json.dumps(payload, ensure_ascii=False, sort_keys=True, allow_nan=False) + "\n")
        self.stream.flush()

    def close(self) -> None:
        if self.stream is not None:
            try:
                self.stream.flush()
                os.fsync(self.stream.fileno())
                self.stream.close()
                if self.path is not None and self.temporary is not None:
                    os.replace(self.temporary, self.path)
                    self.temporary = None
            except (OSError, ValueError) as exc:
                with contextlib.suppress(OSError):
                    self.stream.close()
                if self.temporary is not None:
                    with contextlib.suppress(OSError):
                        os.unlink(self.temporary)
                    self.temporary = None
                raise AgentError("audit_write_failed", "audit output could not be finalized") from exc


def _level_for_event(kind: str) -> int:
    if kind == "heartbeat":
        return logging.DEBUG
    if kind in {"context_failed", "tool_failed"}:
        return logging.WARNING
    if kind == "failed":
        return logging.ERROR
    return logging.INFO


class _Renderer:
    def __init__(self, mode: str, log_level: str, run_id: str):
        if mode not in {"auto", "rich", "jsonl", "quiet"}:
            raise AgentError("config_error", f"unknown renderer: {mode}")
        self.mode = mode
        self.logger = logging.getLogger(f"utils.agent.{run_id}")
        self.logger.handlers.clear()
        self.logger.propagate = False
        level_name = str(log_level).upper()
        if level_name not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise AgentError("config_error", f"unknown log level: {log_level}")
        self.logger.setLevel(getattr(logging, level_name))
        self.handler: logging.Handler | None = None
        self.console = None
        self._Panel = None
        self._Rule = None
        self._Text = None
        self._Live = None
        self._assistant_live = None
        self._assistant_turn = None
        self._assistant_text = ""
        self._output_turn = None
        if mode in {"auto", "rich"}:
            try:
                from rich.console import Console
                from rich.live import Live
                from rich.logging import RichHandler
                from rich.panel import Panel
                from rich.rule import Rule
                from rich.text import Text

                self.console = Console()
                if mode == "auto" and not self.console.is_terminal:
                    self.mode = "jsonl"
                else:
                    self.mode = "rich"
                if self.mode == "rich":
                    self._Panel = Panel
                    self._Rule = Rule
                    self._Text = Text
                    self._Live = Live
                    self.handler = RichHandler(console=self.console, show_path=False, show_time=False, markup=False)
            except ImportError:
                self.mode = "jsonl"
        if self.mode == "jsonl":
            self.handler = logging.StreamHandler()
            self.handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
        if self.handler is not None:
            self.logger.addHandler(self.handler)

    @staticmethod
    def message(event: AgentEvent) -> str:
        data = event.data
        if event.kind == "failed":
            message = f"\n################ AGENT FAILED ##################\ncode={data.get('code')} message={data.get('message')}"
            if data.get("details"):
                message += f"\ndetails={_preview(json.dumps(_safe_json(data['details']), ensure_ascii=False, sort_keys=True), 4000)}"
            return message + "\n#################################################"
        if event.kind == "completed":
            result = data.get("output") if data.get("output") is not None else data.get("final_text", "")
            message = f"\n################ AGENT COMPLETE ################\nstatus=success\nresult={_preview(str(result), 4000)}"
            return message + "\n#################################################"
        messages = {
            "run_started": f"agent run started run_id={event.run_id} model={data.get('model')} real_llm={data.get('real_llm')} streaming={data.get('streaming')} think_mode={data.get('think_mode')} reasoning_effort={data.get('reasoning_effort')}",
            "heartbeat": f"heartbeat elapsed={data.get('elapsed_seconds', 0):.1f}s",
            "context_loaded": f"context loaded pages={data.get('page_count')} manifest={data.get('context_manifest_hash')}",
            "context_rollover": f"context rollover attempt={data.get('attempt_id')}",
            "context_failed": f"context failed code={data.get('code')} message={data.get('message')}",
            "model_started": f"\n================ TURN {data.get('turn')} | MODEL INPUT ================\n" + (f"input messages:\n{_preview(str(data.get('prompt', '')), 12000)}" if data.get("prompt") else ""),
            "model_text": f"model output | assistant: {_preview(str(data.get('text', '')), 4000)}",
            "model_completed": f"---------------- TURN {data.get('turn')} | MODEL OUTPUT | tool_count={data.get('tool_count')} ----------------",
            "tool_started": f"model tool call -> {data.get('name')} id={data.get('tool_call_id')}",
            "tool_completed": f"tool result -> next model input | {data.get('name')} id={data.get('tool_call_id')}: {_preview(str(data.get('result')), 4000)}",
            "tool_failed": f"tool error <- {data.get('name')}: {data.get('error')}",
            "structured_output": f"model output | structured result: {data.get('output')}",
            "failed": f"\n################ AGENT FAILED ##################\ncode={data.get('code')} message={data.get('message')}\n#################################################",
        }
        return messages.get(event.kind, f"{event.kind}: {data}")

    def render(self, event: AgentEvent) -> None:
        if self.mode == "quiet":
            return
        if _level_for_event(event.kind) < self.logger.level:
            return
        message = self.message(event)
        if self.mode == "jsonl":
            payload = event.to_dict()
            payload["level"] = logging.getLevelName(_level_for_event(event.kind))
            payload["message"] = message
            print(json.dumps(payload, ensure_ascii=False, sort_keys=True), flush=True)
            return
        if self.mode == "rich" and self.console is not None and self._Text is not None:
            self._render_rich(event, message)
            return
        self.logger.log(_level_for_event(event.kind), message)

    def _render_rich(self, event: AgentEvent, message: str) -> None:
        """Render high-signal lifecycle events as visual Rich blocks."""

        assert self.console is not None
        Text = self._Text
        Panel = self._Panel
        Rule = self._Rule
        data = event.data
        if event.kind == "model_text":
            self._ensure_model_output_boundary(data.get("turn"))
            self._render_assistant_text(data)
            return
        if event.kind in {"model_started", "model_completed", "completed", "failed"}:
            self._finish_assistant_text()
        if event.kind == "run_started" and Panel is not None:
            body = Text()
            body.append(f"run_id: {event.run_id}\n", style="dim")
            body.append(f"model: {data.get('model')}\n", style="cyan")
            body.append(f"real_llm: {data.get('real_llm')}")
            self.console.print(Panel(body, title="AGENT RUN", border_style="blue", padding=(0, 1), expand=True))
            return
        if event.kind == "context_loaded" and Panel is not None:
            body = Text()
            body.append(f"pages: {data.get('page_count')}\n", style="bold")
            body.append(f"manifest: {data.get('context_manifest_hash')}", style="dim")
            self.console.print(Panel(body, title="CONTEXT LOADED", border_style="blue", padding=(0, 1), expand=True))
            return
        if event.kind == "context_rollover" and Panel is not None:
            body = Text(f"attempt: {data.get('attempt_id')}\nreplayed actions: {data.get('replayed_actions')}")
            self.console.print(Panel(body, title="CONTEXT ROLLOVER", border_style="yellow", padding=(0, 1), expand=True))
            return
        if event.kind == "context_failed" and Panel is not None:
            body = Text()
            body.append(f"code: {data.get('code')}\n", style="bold red")
            body.append(f"message: {data.get('message')}")
            self.console.print(Panel(body, title="CONTEXT ERROR", border_style="red", padding=(0, 1), expand=True))
            return
        if event.kind == "heartbeat" and Panel is not None:
            body = Text(f"elapsed: {data.get('elapsed_seconds', 0):.1f}s\nattempt: {data.get('attempt_id')}", style="dim")
            self.console.print(Panel(body, title="HEARTBEAT", border_style="dim", padding=(0, 1), expand=True))
            return
        if event.kind == "model_started" and Rule is not None:
            self.console.print(Rule(f"TURN {data.get('turn')} | MODEL INPUT", style="cyan"))
            prompt = data.get("prompt")
            if Panel is not None:
                self.console.print(
                    Panel(
                        Text(_preview(str(prompt), 12000) if prompt else "no new messages; history already shown"),
                        title="MODEL INPUT | MESSAGES",
                        border_style="cyan",
                        padding=(0, 1),
                    )
                )
            return
        if event.kind == "model_completed" and Rule is not None:
            self._ensure_model_output_boundary(data.get("turn"), data.get("tool_count"))
            structured_request = data.get("structured_request")
            if structured_request and Panel is not None:
                body = Text()
                body.append("kind: structured\n", style="dim")
                body.append(f"name: {structured_request.get('name')}\n", style="bold")
                body.append(f"tool_call_id: {structured_request.get('tool_call_id')}\n", style="dim")
                body.append(f"status: {structured_request.get('status')}\n", style="yellow")
                body.append("arguments:\n", style="bold")
                body.append(_preview(json.dumps(structured_request.get("arguments", {}), ensure_ascii=False, sort_keys=True), 4000))
                self.console.print(Panel(body, title="MODEL OUTPUT | STRUCTURED CALL", border_style="yellow", padding=(0, 1), expand=True))
            return
        if event.kind == "completed" and Panel is not None:
            body = Text()
            body.append("status: ", style="bold")
            body.append("SUCCESS\n", style="bold green")
            body.append(f"run_id: {event.run_id}\n", style="dim")
            body.append(f"model: {data.get('model')}\n\n", style="cyan")
            body.append("result:\n", style="bold")
            body.append(_preview(str(data.get("output") if data.get("output") is not None else data.get("final_text", "")), 4000))
            self.console.print()
            self.console.print(
                Panel(
                    body,
                    title="[bold white on green] AGENT COMPLETE [/bold white on green]",
                    border_style="green",
                    padding=(1, 2),
                    expand=True,
                )
            )
            self.console.print()
            return
        if event.kind == "failed" and Panel is not None:
            body = Text()
            body.append(f"code: {data.get('code')}\n", style="bold red")
            body.append(f"message: {data.get('message')}")
            if data.get("details"):
                body.append("\ndetails:\n", style="bold")
                body.append(_preview(json.dumps(_safe_json(data["details"]), ensure_ascii=False, sort_keys=True), 4000), style="dim")
            self.console.print(
                Panel(
                    body,
                    title="AGENT FAILED",
                    border_style="red",
                    padding=(1, 2),
                    expand=True,
                )
            )
            return
        if event.kind == "structured_output" and Panel is not None:
            body = Text()
            body.append("kind: structured\n", style="dim")
            body.append("status: completed\n", style="bold green")
            body.append("result:\n", style="bold")
            body.append(_preview(json.dumps(_safe_json(data.get("output")), ensure_ascii=False, sort_keys=True), 4000))
            self.console.print(Panel(body, title="MODEL OUTPUT | STRUCTURED RESULT", border_style="green", padding=(0, 1), expand=True))
            return
        if event.kind in {"tool_started", "tool_completed", "tool_failed"}:
            prefix_styles = {
                "tool_started": ("MODEL OUTPUT | TOOL CALL: ", "bold yellow"),
                "tool_completed": ("TOOL RESULT -> NEXT MODEL INPUT: ", "bold green"),
                "tool_failed": ("tool error <- ", "bold red"),
            }
            prefix, style = prefix_styles[event.kind]
            if event.kind in {"tool_started", "tool_completed", "tool_failed"} and Panel is not None:
                if event.kind == "tool_started":
                    tool_body = Text()
                    tool_body.append("kind: business\n", style="dim")
                    tool_body.append(f"name: {data.get('name')}\n", style="bold")
                    tool_body.append(f"tool_call_id: {data.get('tool_call_id')}\n", style="dim")
                    tool_body.append("status: started\n", style="yellow")
                    tool_body.append("arguments:\n", style="bold")
                    tool_body.append(_preview(json.dumps(_safe_json(data.get("arguments")), ensure_ascii=False, sort_keys=True), 4000))
                    title, border = "MODEL OUTPUT | TOOL CALL", "yellow"
                elif event.kind == "tool_completed":
                    tool_body = Text()
                    tool_body.append("kind: business\n", style="dim")
                    tool_body.append(f"name: {data.get('name')}\n", style="bold")
                    tool_body.append(f"tool_call_id: {data.get('tool_call_id')}\n", style="dim")
                    tool_body.append("status: completed\n", style="bold green")
                    tool_body.append(f"arguments: {_preview(json.dumps(_safe_json(data.get('arguments')), ensure_ascii=False, sort_keys=True), 4000)}\n")
                    tool_body.append("result:\n", style="bold")
                    tool_body.append(_preview(json.dumps(_safe_json(data.get("result")), ensure_ascii=False, sort_keys=True), 4000))
                    title, border = "TOOL RESULT -> NEXT MODEL INPUT", "green"
                else:
                    tool_body = Text()
                    tool_body.append("kind: business\n", style="dim")
                    tool_body.append(f"name: {data.get('name')}\n", style="bold")
                    tool_body.append(f"tool_call_id: {data.get('tool_call_id')}\n", style="dim")
                    tool_body.append("status: failed\n", style="bold red")
                    tool_body.append(f"error: {data.get('error')}", style="red")
                    title, border = "TOOL ERROR", "red"
                self.console.print(Panel(tool_body, title=title, border_style=border, padding=(0, 1), expand=True))
                return
            line = Text(prefix, style=style)
            if event.kind == "tool_started":
                body = f"{data.get('name')}({data.get('arguments')}) id={data.get('tool_call_id')}"
            elif event.kind == "tool_completed":
                body = _preview(str(data.get("result")), 4000)
            elif event.kind == "tool_failed":
                body = str(data.get("error"))
            else:
                body = str(data.get("output"))
            line.append(body)
            self.console.print(line)
            return
        if Panel is not None:
            self.console.print(
                Panel(
                    Text(message),
                    title=str(event.kind).upper(),
                    border_style="white",
                    padding=(0, 1),
                    expand=True,
                )
            )
            return
        self.logger.log(_level_for_event(event.kind), message)

    def _ensure_model_output_boundary(self, turn: Any, tool_count: Any = None) -> None:
        if self.console is None or self._Rule is None or self._output_turn == turn:
            return
        suffix = f" | tool_count={tool_count}" if tool_count is not None else ""
        self.console.print(self._Rule(f"TURN {turn} | MODEL OUTPUT{suffix}", style="green"))
        self._output_turn = turn

    def _assistant_panel(self) -> Any:
        assert self._Panel is not None
        assert self._Text is not None
        return self._Panel(
            self._Text(_preview(self._assistant_text, 4000)),
            title="MODEL OUTPUT | ASSISTANT",
            border_style="cyan",
            padding=(0, 1),
            expand=True,
        )

    def _render_assistant_text(self, data: Mapping[str, Any]) -> None:
        if self.console is None or self._Panel is None or self._Text is None:
            return
        turn = data.get("turn")
        if self._assistant_turn != turn:
            self._finish_assistant_text()
            self._assistant_turn = turn
            self._assistant_text = ""
        self._assistant_text += str(data.get("text", ""))
        if self._Live is None:
            self.console.print(self._assistant_panel())
            return
        if self._assistant_live is None:
            self._assistant_live = self._Live(self._assistant_panel(), console=self.console, refresh_per_second=10, transient=False)
            self._assistant_live.start(refresh=True)
        else:
            self._assistant_live.update(self._assistant_panel(), refresh=True)

    def _finish_assistant_text(self) -> None:
        if self._assistant_live is not None:
            self._assistant_live.update(self._assistant_panel(), refresh=True)
            self._assistant_live.stop()
            self._assistant_live = None
            if self.console is not None:
                self.console.print()
        self._assistant_turn = None
        self._assistant_text = ""

    def close(self) -> None:
        self._finish_assistant_text()
        if self.handler is not None:
            self.logger.removeHandler(self.handler)
            self.handler.close()


class _AgentGuardMiddleware(AgentMiddleware):
    """LangChain middleware executed between model and ToolNode."""

    def __init__(self, spec: AgentSpec, *, context_window_tokens: int | None = None, max_output_tokens: int | None = None, counters: dict[str, int] | None = None):
        self.spec = spec
        self.context_window_tokens = context_window_tokens
        self.max_output_tokens = max_output_tokens
        self.counters = counters if counters is not None else {"model_calls": 0, "tool_calls": 0, "turns": 0}

    def _before_model(self, state: Mapping[str, Any]) -> None:
        limits = self.spec.limits or {}
        if limits.get("model_calls") is not None and self.counters["model_calls"] >= limits["model_calls"]:
            raise AgentError("limit_exceeded", "model_calls limit exceeded")
        if limits.get("turns") is not None and self.counters["turns"] >= limits["turns"]:
            raise AgentError("limit_exceeded", "turns limit exceeded")
        if self.context_window_tokens and self.max_output_tokens and self.counters["model_calls"] > 0:
            estimate = _estimate_messages(state.get("messages", [])) + _estimate_agent_overhead(self.spec)
            if estimate + self.max_output_tokens > self.context_window_tokens:
                raise AgentError("context_rollover", "model context approaching window")
        self.counters["turns"] += 1
        self.counters["model_calls"] += 1

    def before_model(self, state: Mapping[str, Any], runtime: Any) -> None:
        self._before_model(state)

    async def abefore_model(self, state: Mapping[str, Any], runtime: Any) -> None:
        self._before_model(state)

    def _after_model(self, state: Mapping[str, Any]) -> None:
        messages = state.get("messages", [])
        last = next((message for message in reversed(messages) if isinstance(message, AIMessage)), None)
        if last is None:
            return
        calls = list(getattr(last, "tool_calls", None) or [])
        registered = set(self.spec.tool_names)
        structured_names = set()
        if self.spec.output_schema is not None:
            structured_names.add(self.spec.output_schema.__name__)
        unknown = [call.get("name") for call in calls if call.get("name") not in registered | structured_names]
        if unknown:
            raise AgentError("tool_not_allowed", f"tool is not registered: {unknown[0]}")
        business = [call for call in calls if call.get("name") in registered]
        structured = [call for call in calls if call.get("name") in structured_names]
        if business and structured:
            raise AgentError("mixed_terminal_tool", "structured output cannot share a model turn with a business tool")
        limits = self.spec.limits or {}
        if limits.get("tool_calls") is not None and self.counters["tool_calls"] + len(business) > limits["tool_calls"]:
            raise AgentError("limit_exceeded", "tool_calls limit exceeded")
        self.counters["tool_calls"] += len(business)

    def after_model(self, state: Mapping[str, Any], runtime: Any) -> None:
        self._after_model(state)

    async def aafter_model(self, state: Mapping[str, Any], runtime: Any) -> None:
        self._after_model(state)


class _ReplayToolMiddleware(AgentMiddleware):
    """Rollover 时注入已经完成的工具结果，避免再次执行副作用。"""

    def __init__(self, cache: dict[str, Any], *, enabled: bool, provenance: dict[str, list[bool]] | None = None):
        self.cache = cache
        self.enabled = enabled
        self.provenance = provenance if provenance is not None else {}

    @staticmethod
    def _key(call: Mapping[str, Any]) -> str:
        return f"{call.get('name')}:{json.dumps(_safe_json(call.get('args', {})), ensure_ascii=False, sort_keys=True)}"

    def wrap_tool_call(self, request: Any, handler: Callable[[Any], Any]) -> Any:
        call = request.tool_call
        key = self._key(call)
        if self.enabled and self.cache.get(key):
            self.provenance.setdefault(key, []).append(True)
            return ToolMessage(
                content=self.cache[key].pop(0),
                name=call.get("name"),
                tool_call_id=call.get("id"),
                additional_kwargs={"replayed": True},
            )
        result = handler(request)
        if not self.enabled and isinstance(result, ToolMessage):
            self.cache.setdefault(key, []).append(result.content)
        if isinstance(result, ToolMessage):
            self.provenance.setdefault(key, []).append(False)
        return result

    async def awrap_tool_call(self, request: Any, handler: Callable[[Any], Any]) -> Any:
        call = request.tool_call
        key = self._key(call)
        if self.enabled and self.cache.get(key):
            self.provenance.setdefault(key, []).append(True)
            return ToolMessage(
                content=self.cache[key].pop(0),
                name=call.get("name"),
                tool_call_id=call.get("id"),
                additional_kwargs={"replayed": True},
            )
        result = await handler(request)
        if not self.enabled and isinstance(result, ToolMessage):
            self.cache.setdefault(key, []).append(result.content)
        if isinstance(result, ToolMessage):
            self.provenance.setdefault(key, []).append(False)
        return result


def _build_replay_cache(records: Sequence[Mapping[str, Any]]) -> dict[str, list[Any]]:
    cache: dict[str, list[Any]] = {}
    for record in records:
        key = f"{record.get('name')}:{json.dumps(_safe_json(record.get('arguments', {})), ensure_ascii=False, sort_keys=True)}"
        cache.setdefault(key, []).append(record.get("result"))
    return cache


class _ModelOptionsMiddleware(AgentMiddleware):
    """Apply per-inference model settings without changing profile identity."""

    def __init__(self, options: Mapping[str, Any] | None):
        self.options = dict(options or {})

    def wrap_model_call(self, request: Any, handler: Callable[[Any], Any]) -> Any:
        settings = {**(request.model_settings or {}), **self.options}
        return handler(request.override(model_settings=settings))

    async def awrap_model_call(self, request: Any, handler: Callable[[Any], Any]) -> Any:
        settings = {**(request.model_settings or {}), **self.options}
        return await handler(request.override(model_settings=settings))

class _LegacyModelAdapter(BaseChatModel):
    """仅兼容 tests 中的旧式 ``astream`` 测试桩，不属于公共 API。"""

    _inner: Any = PrivateAttr()

    def __init__(self, inner: Any):
        super().__init__()
        self._inner = inner

    @property
    def _llm_type(self) -> str:
        return "legacy-test-model"

    def bind_tools(self, tools: Any, **kwargs: Any) -> "_LegacyModelAdapter":
        binder = getattr(self._inner, "bind_tools", None)
        if binder is not None:
            binder(tools, **kwargs)
        return self

    async def _agenerate(self, messages: list[Any], stop: list[str] | None = None, **kwargs: Any) -> Any:
        chunks: list[Any] = []
        async for chunk in self._inner.astream(messages, **kwargs):
            chunks.append(chunk)
        if not chunks:
            message = AIMessage(content="")
        else:
            current = chunks[0]
            for chunk in chunks[1:]:
                current = current + chunk
            if isinstance(current, AIMessageChunk):
                message = AIMessage(content=current.content, tool_calls=current.tool_calls, response_metadata=current.response_metadata)
            elif isinstance(current, AIMessage):
                message = current
            else:
                message = AIMessage(content=_message_text(current))
        return ChatResult(generations=[ChatGeneration(message=message)])

    def _generate(self, messages: list[Any], stop: list[str] | None = None, **kwargs: Any) -> Any:
        return asyncio.run(self._agenerate(messages, stop=stop, **kwargs))


class AgentApp:
    def __init__(self, spec: AgentSpec, config: LLMConfig, model: Any, *, real_llm: bool = True):
        self.spec = spec
        self.config = config
        self.model = model
        self.real_llm = real_llm

    @classmethod
    def from_registry(cls, spec: AgentSpec, registry: LLMRegistry, profile: str | None = None, *, model_options: Mapping[str, Any] | None = None) -> "AgentApp":
        name = registry.default_name if profile is None else profile
        return cls.from_config(spec, registry.require(name), model_options=model_options)

    @classmethod
    def from_config(cls, spec: AgentSpec, config: LLMConfig, *, model_options: Mapping[str, Any] | None = None) -> "AgentApp":
        _validate_model_options(model_options)
        if config.api_key is None:
            raise AgentError("config_error", "api_key is required for a real model run")
        try:
            from langchain_openai import ChatOpenAI
        except ImportError as exc:  # pragma: no cover
            raise AgentError("config_error", "langchain-openai is required") from exc
        kwargs = config.connection_kwargs()
        if config.max_output_tokens is not None:
            kwargs["max_completion_tokens"] = config.max_output_tokens
        kwargs.update({"streaming": True, "stream_usage": True, "max_retries": 0})
        kwargs.update(dict(model_options or {}))
        try:
            model = ChatOpenAI(**kwargs)
        except Exception as exc:
            raise AgentError("config_error", "model construction failed", details=_exception_details(exc)) from exc
        return cls(spec, config, model)

    @classmethod
    def _for_test(cls, spec: AgentSpec, config: LLMConfig, model: Any) -> "AgentApp":
        if not isinstance(model, BaseChatModel) and hasattr(model, "astream"):
            model = _LegacyModelAdapter(model)
        return cls(spec, config, model, real_llm=False)

    def run(self, input_text: str, **options: Any) -> AgentRunResult:
        return asyncio.run(self.arun(input_text, **options))

    async def arun(
        self,
        input_text: str,
        *,
        context: Sequence[str | Mapping[str, Any]] | None = None,
        renderer: str = "auto",
        log_level: str = "INFO",
        think_mode: bool = False,
        reasoning_effort: str | None = None,
        on_event: Callable[[AgentEvent], None] | None = None,
        audit_out: Path | None = None,
        result_out: Path | None = None,
        model_call_options: Mapping[str, Any] | None = None,
    ) -> AgentRunResult:
        _validate_model_call_options(model_call_options)
        inference_options, effective_think_mode = _resolve_inference_options(
            self.config,
            model_call_options=model_call_options,
            think_mode=think_mode,
            reasoning_effort=reasoning_effort,
        )
        inference_summary = {
            "streaming": getattr(self.model, "streaming", None),
            "think_mode": effective_think_mode,
            "reasoning_effort": inference_options.get("reasoning_effort"),
        }
        try:
            pages = _normalize_context(context)
        except ValueError as exc:
            raise AgentError("context_invalid", str(exc)) from exc
        run_id = uuid.uuid4().hex
        manifest = _build_context_manifest(pages) if pages else None
        renderer_obj = _Renderer(renderer, log_level, run_id)
        audit = _AuditWriter(Path(audit_out) if audit_out is not None else None, run_id)
        started = time.monotonic()
        seq = 0
        attempt_id = "attempt-1"
        turn = 0
        status = "failed"
        output: Any = None
        final_text = ""
        usage: dict[str, Any] | None = None
        observed_model: str | None = None
        error: dict[str, Any] | None = None
        tool_calls: list[dict[str, Any]] = []
        pending_tool_ids: dict[str, list[str]] = {}
        active_tool_records: dict[str, dict[str, Any]] = {}
        replay_provenance: dict[str, list[bool]] = {}
        shown_message_keys: set[str] = set()
        system_shown = False
        streamed_turns: set[int] = set()
        audit_ok = audit.enabled
        business_tool_called = False
        tool_error_seen = False
        heartbeat_task: asyncio.Task[None] | None = None

        def emit(kind: str, data: Mapping[str, Any]) -> None:
            nonlocal seq
            seq += 1
            event = AgentEvent(run_id, seq, datetime.now(timezone.utc), kind, _redact(_safe_json(dict(data))))
            renderer_obj.render(event)
            if on_event is not None:
                on_event(event)

        def audit_write(record: Mapping[str, Any], *, turn_value: int | None = None) -> None:
            nonlocal audit_ok
            try:
                audit.write(
                    {
                        "attempt_id": attempt_id,
                        "turn": turn if turn_value is None else turn_value,
                        "context_manifest_hash": manifest,
                        **record,
                    }
                )
            except Exception as exc:
                audit_ok = False
                raise AgentError("audit_write_failed", "audit output failed") from exc

        async def heartbeat() -> None:
            while True:
                await asyncio.sleep(1)
                emit("heartbeat", {"elapsed_seconds": time.monotonic() - started, "attempt_id": attempt_id})

        replay_records: list[dict[str, Any]] = []
        replay_queue: list[dict[str, Any]] = []
        replay_enqueued = 0

        def replay_key(name: Any, arguments: Any) -> str:
            return f"{name}:{json.dumps(_safe_json(arguments), ensure_ascii=False, sort_keys=True)}"

        def take_replay(request: Mapping[str, Any]) -> dict[str, Any] | None:
            key = replay_key(request.get("name"), request.get("arguments", {}))
            for index, record in enumerate(replay_queue):
                if replay_key(record.get("name"), record.get("arguments", {})) == key:
                    return replay_queue.pop(index)
            return None

        async def consume(graph: Any) -> dict[str, Any] | None:
            nonlocal turn, final_text, output, usage, observed_model, business_tool_called, system_shown, tool_error_seen
            messages: list[Any] = [{"role": "user", "content": _input_with_context(input_text, pages)}]
            if attempt_id != "attempt-1":
                for record in replay_records:
                    call = {
                        "name": record["name"],
                        "args": record["arguments"],
                        "id": record["tool_call_id"],
                        "type": "tool_call",
                    }
                    result = record.get("result")
                    content = result if isinstance(result, str) else json.dumps(_safe_json(result), ensure_ascii=False, sort_keys=True)
                    messages.extend(
                        [
                            AIMessage(content="", tool_calls=[call]),
                            ToolMessage(content=content, name=record["name"], tool_call_id=record["tool_call_id"]),
                        ]
                    )
            inputs = {"messages": messages}
            stream_kwargs: dict[str, Any] = {"version": "v2"}
            # LangGraph's default recursion limit is 25.  That is an internal
            # graph safeguard, not an AgentSpec budget, so raise it unless the
            # caller explicitly supplied a finite budget.  Test doubles from
            # older callers may not expose the newer ``config`` parameter.
            try:
                stream_signature = inspect.signature(graph.astream_events)
            except (TypeError, ValueError):  # pragma: no cover - unusual proxy objects
                stream_signature = None
            if stream_signature is None or "config" in stream_signature.parameters or any(
                parameter.kind is inspect.Parameter.VAR_KEYWORD for parameter in stream_signature.parameters.values()
            ):
                stream_kwargs["config"] = {"recursion_limit": _graph_recursion_limit(self.spec)}
            async for event in graph.astream_events(inputs, **stream_kwargs):
                name = str(event.get("name") or "")
                kind = str(event.get("event") or "")
                data = event.get("data") or {}
                if kind == "on_chain_start" and name == "model":
                    turn += 1
                    prompt, system_shown = _prompt_from_messages(data.get("input"), self.spec.system_prompt, shown_message_keys, system_shown)
                    emit("model_started", {"attempt_id": attempt_id, "turn": turn, "prompt": prompt})
                elif kind == "on_chat_model_start":
                    observed_model = observed_model or data.get("metadata", {}).get("model_name")
                elif kind == "on_chat_model_end":
                    model_usage, model_name = _model_metadata(data.get("output"))
                    usage = model_usage or usage
                    observed_model = observed_model or model_name
                elif kind == "on_chat_model_stream":
                    chunk = data.get("chunk")
                    text = _message_text(chunk) if chunk is not None else ""
                    if text:
                        streamed_turns.add(turn)
                        emit("model_text", {"attempt_id": attempt_id, "turn": turn, "text": text})
                elif kind == "on_chain_end" and name == "model":
                    messages = _messages_from_event(data.get("output"))
                    ai = next((message for message in reversed(messages) if isinstance(message, AIMessage)), None)
                    if ai is not None:
                        calls = list(getattr(ai, "tool_calls", None) or [])
                        if _message_text(ai) and not calls and turn not in streamed_turns:
                            emit("model_text", {"attempt_id": attempt_id, "turn": turn, "text": _message_text(ai)})
                        _mark_message_shown(ai, shown_message_keys)
                        structured_name = self.spec.output_schema.__name__ if self.spec.output_schema is not None else None
                        requests = [
                            _tool_request(call, attempt_id, turn, kind="structured" if call.get("name") == structured_name else "business")
                            for call in calls
                        ]
                        structured_requests = [request for request in requests if request["kind"] == "structured"]
                        emit(
                            "model_completed",
                            {
                                "attempt_id": attempt_id,
                                "turn": turn,
                                "tool_count": len(calls),
                                "output": _message_text(ai) if not calls else "",
                                "structured_request": structured_requests[0] if structured_requests else None,
                            },
                        )
                        for request in requests:
                            if request["kind"] == "business":
                                replay = take_replay(request) if attempt_id != "attempt-1" else None
                                if replay is None:
                                    pending_tool_ids.setdefault(str(request["name"]), []).append(str(request["tool_call_id"]))
                                else:
                                    replay_record = {
                                        **request,
                                        "status": "completed",
                                        "result": replay["result"],
                                        "replayed": True,
                                        "started_at": datetime.now(timezone.utc).isoformat(),
                                        "finished_at": datetime.now(timezone.utc).isoformat(),
                                    }
                                    tool_calls.append(replay_record)
                                    business_tool_called = True
                                    emit("tool_started", {"name": request["name"], "tool_call_id": request["tool_call_id"], "arguments": request["arguments"], "status": "started", "attempt_id": attempt_id, "turn": turn, "replayed": True})
                                    emit("tool_completed", {"name": request["name"], "tool_call_id": request["tool_call_id"], "arguments": request["arguments"], "result": replay["result"], "status": "completed", "attempt_id": attempt_id, "turn": turn, "replayed": True})
                            else:
                                tool_calls.append({**request, "status": "requested", "started_at": datetime.now(timezone.utc).isoformat()})
                        # ``_message_text`` deliberately excludes provider
                        # thinking/reasoning blocks; audit is an academic
                        # behavior record and must not persist hidden CoT.
                        audit_write({"record": "decision", "message": _message_text(ai), "tool_requests": requests, "reasoning_summary": _visible_reasoning(ai)})
                        unknown_requests = [item for item in requests if item["name"] not in self.spec.tool_names and item["name"] != structured_name]
                        business_requests = [item for item in requests if item["name"] in self.spec.tool_names]
                        if unknown_requests:
                            for request in unknown_requests:
                                audit_write({"record": "action", "kind": "business", "name": request["name"], "tool_call_id": request["tool_call_id"], "arguments": request["arguments"], "status": "rejected", "error": {"code": "tool_not_allowed", "message": "tool is not registered"}})
                        if structured_name and business_requests and any(item["name"] == structured_name for item in requests):
                            for request in business_requests:
                                audit_write({"record": "action", "kind": "business", "name": request["name"], "tool_call_id": request["tool_call_id"], "arguments": request["arguments"], "status": "rejected", "error": {"code": "mixed_terminal_tool", "message": "structured output cannot share a model turn with a business tool"}})
                    model_usage, model_name = _model_metadata(data.get("output"))
                    usage = model_usage or usage
                    observed_model = observed_model or model_name
                elif kind == "on_tool_start":
                    ids = pending_tool_ids.get(name, [])
                    call_id = ids.pop(0) if ids else str(event.get("run_id") or uuid.uuid4().hex)
                    args = data.get("input")
                    name_value = name
                    key = replay_key(name_value, args)
                    provenance = replay_provenance.get(key, [])
                    was_replay = bool(provenance and provenance.pop(0))
                    if was_replay:
                        record = next(
                            (
                                item
                                for item in reversed(tool_calls)
                                if item.get("name") == name_value
                                and item.get("attempt_id") == attempt_id
                                and item.get("replayed") is True
                                and item.get("arguments") == _safe_json(args)
                            ),
                            None,
                        )
                    else:
                        record = None
                    if record is None:
                        record = {"kind": "business", "name": name_value, "tool_call_id": call_id, "attempt_id": attempt_id, "turn": turn, "arguments": _safe_json(args), "status": "started", "started_at": datetime.now(timezone.utc).isoformat()}
                        tool_calls.append(record)
                    active_tool_records[str(event.get("run_id") or call_id)] = record
                    if not was_replay:
                        emit("tool_started", {"name": name_value, "tool_call_id": call_id, "arguments": _safe_json(args), "status": "started", "attempt_id": attempt_id, "turn": turn})
                elif kind == "on_tool_end":
                    result_value = _tool_result_value(data.get("output"))
                    execution_id = str(event.get("run_id") or "")
                    record = active_tool_records.pop(execution_id, None)
                    if record is None:
                        record = next((item for item in reversed(tool_calls) if item["name"] == name and item["status"] == "started"), None)
                    replayed = _is_replayed_tool_result(data.get("output"))
                    if record is not None:
                        if record.get("status") == "completed" and record.get("replayed"):
                            replayed = True
                        else:
                            record.update({"status": "completed", "result": _safe_json(result_value), "replayed": replayed, "finished_at": datetime.now(timezone.utc).isoformat()})
                        business_tool_called = True
                        if not replayed and record.get("status") == "completed":
                            replay_records.append({"name": record["name"], "tool_call_id": record["tool_call_id"], "attempt_id": record["attempt_id"], "turn": record["turn"], "arguments": record["arguments"], "result": record["result"]})
                            audit_write({"record": "action", **record})
                    if not (record and record.get("replayed")):
                        emit("tool_completed", {"name": name, "tool_call_id": record.get("tool_call_id") if record else None, "arguments": record.get("arguments") if record else data.get("input"), "result": _safe_json(result_value), "status": "completed", "attempt_id": attempt_id, "turn": turn})
                elif kind == "on_tool_error":
                    tool_error_seen = True
                    raw_error = data.get("error")
                    safe_error = {"code": "tool_error", "message": "registered tool failed"}
                    if isinstance(raw_error, BaseException):
                        safe_error["details"] = _exception_details(raw_error)
                    execution_id = str(event.get("run_id") or "")
                    record = active_tool_records.pop(execution_id, None)
                    if record is None:
                        record = next((item for item in reversed(tool_calls) if item["name"] == name and item["status"] == "started"), None)
                    if record is None:
                        record = {"kind": "business", "name": name, "tool_call_id": event.get("tool_call_id") or event.get("run_id"), "attempt_id": attempt_id, "turn": turn, "arguments": _safe_json(data.get("input")), "status": "failed"}
                        tool_calls.append(record)
                    record.update({"status": "failed", "error": safe_error, "finished_at": datetime.now(timezone.utc).isoformat()})
                    audit_write({"record": "action", **record})
                    emit("tool_failed", {"name": name, "tool_call_id": record.get("tool_call_id") if record else None, "arguments": record.get("arguments") if record else None, "error": safe_error, "status": "failed", "attempt_id": attempt_id, "turn": turn})
                elif kind == "on_chain_end" and name in {"LangGraph", self.spec.name}:
                    state = data.get("output") or {}
                    output = state.get("structured_response")
                    messages = state.get("messages") or []
                    final = next((message for message in reversed(messages) if isinstance(message, AIMessage)), None)
                    if final is not None:
                        final_text = _message_text(final)
                    structured_record = next((item for item in reversed(tool_calls) if item.get("kind") == "structured" and item.get("status") == "requested"), None)
                    if output is not None:
                        if structured_record is not None:
                            structured_record.update({"status": "completed", "result": _safe_json(output), "finished_at": datetime.now(timezone.utc).isoformat()})
                            audit_write({"record": "action", **structured_record})
                        emit("structured_output", {"attempt_id": attempt_id, "turn": turn, "output": _safe_json(output)})
                    return state
            return None

        try:
            if not input_text.strip():
                raise AgentError("input_invalid", "input_text must not be empty")
            emit("run_started", {"model": self.config.model, "has_context": bool(pages), "real_llm": self.real_llm, **inference_summary, "structured_output_mode": "langgraph_response_format" if self.spec.output_schema is not None else None})
            if pages:
                emit("context_loaded", {"attempt_id": attempt_id, "page_count": len(pages), "context_manifest_hash": manifest, "pages": [{"id": page["id"], "hash": page["hash"]} for page in pages]})
            audit_write(
                {
                    "record": "context",
                    "input_text": input_text,
                    "system_prompt": self.spec.system_prompt,
                    "agent_name": self.spec.name,
                    "model": self.config.model,
                    "inference": inference_summary,
                    "structured_output_mode": "langgraph_response_format" if self.spec.output_schema is not None else None,
                    "tools": [{"name": _tool_name(tool), "description": _tool_description(tool), "schema": _tool_schema(tool)} for tool in self.spec.tools],
                    "output_schema": self.spec.output_schema.model_json_schema() if self.spec.output_schema else None,
                    "pages": pages,
                }
            )
            if self.config.context_window_tokens is not None and self.config.max_output_tokens is not None:
                estimated = max(1, math.ceil(len(_input_with_context(input_text, pages)) / 4)) + _estimate_agent_overhead(self.spec)
                if estimated + self.config.max_output_tokens > self.config.context_window_tokens:
                    emit("context_failed", {"code": "context_budget_exceeded", "message": "context cannot fit without truncation"})
                    raise AgentError("context_budget_exceeded", "context cannot fit without truncation")
            if create_agent is None:
                raise AgentError("config_error", "langchain is required")
            heartbeat_task = asyncio.create_task(heartbeat())
            seconds = (self.spec.limits or {}).get("seconds")
            counters = {"model_calls": 0, "tool_calls": 0, "turns": 0}
            rollover_count = 0
            while True:
                guard = _AgentGuardMiddleware(
                    self.spec,
                    context_window_tokens=self.config.context_window_tokens,
                    max_output_tokens=self.config.max_output_tokens,
                    counters=counters,
                )
                replay_cache = _build_replay_cache(replay_queue)
                # Let LangGraph select the provider-native structured-output
                # strategy (or its official tool-calling fallback).  Do not
                # force a hand-selected tool choice here: OpenAI-compatible
                # providers differ in how they implement structured output.
                response_format = self.spec.output_schema
                graph = create_agent(
                    model=self.model,
                    tools=_langchain_tools(self.spec.tools),
                    system_prompt=self.spec.system_prompt,
                    response_format=response_format,
                    middleware=[guard, _ReplayToolMiddleware(replay_cache, enabled=rollover_count > 0, provenance=replay_provenance), _ModelOptionsMiddleware(inference_options)],
                    name=self.spec.name,
                )
                try:
                    if seconds is None:
                        await consume(graph)
                    else:
                        remaining = float(seconds) - (time.monotonic() - started)
                        if remaining <= 0:
                            raise AgentError("limit_exceeded", "seconds limit exceeded")
                        await asyncio.wait_for(consume(graph), timeout=remaining)
                    break
                except AgentError as exc:
                    if exc.code != "context_rollover" or rollover_count >= _DEFAULT_CONTEXT_ROLLOVER_LIMIT:
                        if exc.code == "context_rollover":
                            raise AgentError("context_budget_exceeded", "context cannot fit without truncation") from exc
                        raise
                    rollover_count += 1
                    attempt_id = f"attempt-{rollover_count + 1}"
                    replay_queue.extend(replay_records[replay_enqueued:])
                    replay_enqueued = len(replay_records)
                    system_shown = False
                    shown_message_keys.clear()
                    emit("context_rollover", {"attempt_id": attempt_id, "context_manifest_hash": manifest, "replayed_actions": len(replay_records)})
                    audit_write({"record": "context", "pages": pages, "rollover": True, "replayed_actions": replay_records})
            if self.spec.require_tool_call and not business_tool_called:
                raise AgentError("tool_required", "a business tool call was required")
            if self.spec.output_schema is not None and output is None:
                raise AgentError("structured_output_invalid", "structured output was not returned")
            status = "success"
        except asyncio.TimeoutError as exc:
            details = _exception_details(exc)
            if details.get("source") == "provider":
                error = {
                    "code": "provider_error",
                    "message": "LLM provider request timed out; inspect provider type, request_id, and diagnostics",
                    "details": details,
                }
            else:
                error = {"code": "limit_exceeded", "message": "seconds limit exceeded", "details": details}
        except asyncio.CancelledError:
            status = "cancelled"
            error = {"code": "cancelled", "message": "agent run was cancelled"}
        except AgentError as exc:
            error = {"code": exc.code, "message": exc.message}
            if exc.details:
                error["details"] = _redact(_safe_json(exc.details))
        except Exception as exc:
            details = _exception_details(exc)
            if tool_error_seen:
                error = {"code": "tool_error", "message": "registered tool execution failed; inspect details for the tool and failure cause"}
            elif details.get("source") == "provider":
                error = {"code": "provider_error", "message": "LLM provider request failed; inspect provider type, status, code, request_id, and details"}
            elif self.spec.output_schema is not None:
                error = {"code": "structured_output_invalid", "message": "structured output validation failed; inspect the model response and schema diagnostics"}
            else:
                error = {"code": "runtime_error", "message": "agent runtime failed; inspect the diagnostic details"}
            error["details"] = details
        finally:
            if heartbeat_task is not None:
                heartbeat_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await heartbeat_task
            try:
                for record in tool_calls:
                    if record.get("status") in {"started", "requested"}:
                        if error is None:
                            error = {"code": "incomplete_tool", "message": "tool execution did not produce a completion event"}
                            status = "failed"
                        record.update({"status": "failed", "error": error, "finished_at": datetime.now(timezone.utc).isoformat()})
                        audit_write({"record": "action", **record})
                audit_write({"record": "finish", "status": status, "final_text": final_text, "output": output, "error": error, "reason": "structured_output" if output is not None else ("final_answer" if status == "success" else (error or {}).get("code", "runtime_error"))})
            except AgentError:
                error = {"code": "audit_write_failed", "message": "audit output failed"}
                status = "failed"
            try:
                audit.close()
            except AgentError:
                audit_ok = False
                error = {"code": "audit_write_failed", "message": "audit output could not be finalized"}
                status = "failed"
            if error is None:
                emit("completed", {"model": self.config.model, "output": _safe_json(output), "final_text": final_text})
            else:
                emit("failed", error)
            renderer_obj.close()
        academic_eligible = audit.enabled and audit_ok and status == "success"
        result = AgentRunResult(run_id, status, output, final_text, tool_calls, usage, error, self.real_llm, self.config.model, observed_model, academic_eligible, manifest)
        if result_out is not None:
            try:
                _atomic_write(Path(result_out), result.to_dict())
            except Exception as exc:
                raise AgentError("json_export_failed", "result output failed") from exc
        return result


def _input_with_context(input_text: str, pages: Sequence[Mapping[str, Any]]) -> str:
    parts = [input_text]
    if pages:
        rendered = "\n\n".join(f"[{page['id']}]\n{page['text']}" for page in pages)
        parts.append(f"上下文页面（按顺序，不可改写）：\n{rendered}")
    return "\n\n".join(parts)


def _estimate_messages(messages: Sequence[Any]) -> int:
    text = "\n".join(_message_text(message) for message in messages)
    return max(1, math.ceil(len(text) / 4))


def _estimate_agent_overhead(spec: AgentSpec) -> int:
    payload = {
        "system_prompt": spec.system_prompt,
        "tools": [
            {"name": _tool_name(tool), "description": _tool_description(tool), "schema": _tool_schema(tool)}
            for tool in spec.tools
        ],
        "output_schema": spec.output_schema.model_json_schema() if spec.output_schema else None,
    }
    return max(1, math.ceil(len(json.dumps(_safe_json(payload), ensure_ascii=False, sort_keys=True)) / 4)) + 1024


def _graph_recursion_limit(spec: AgentSpec) -> int:
    """Choose a graph safeguard without imposing a default AgentSpec budget.

    A finite business limit needs only a small amount of graph headroom: a
    model node, optional tool node, and middleware events per turn.  With no
    finite count configured, use a large safeguard so LangGraph's default 25
    does not become an accidental maximum iteration count.  The explicit
    ``seconds`` limit remains enforced by ``asyncio.wait_for``.
    """

    limits = spec.limits or {}
    finite_counts = [
        int(math.ceil(float(limits[key])))
        for key in ("model_calls", "tool_calls", "turns")
        if limits.get(key) is not None
    ]
    if not finite_counts:
        return _DEFAULT_GRAPH_RECURSION_LIMIT
    return max(100, 4 * max(finite_counts) + 32)


def _preview(value: str, limit: int = 4000) -> str:
    if len(value) <= limit:
        return value
    head = int(limit * 0.7)
    tail = limit - head
    return f"{value[:head]}\n... [中间省略 {len(value) - limit} 字符] ...\n{value[-tail:]}"


def _message_key(message: Any) -> str:
    identity = getattr(message, "id", None) or ""
    return f"{identity}:{getattr(message, 'type', message.__class__.__name__)}:{_message_text(message)}"


def _mark_message_shown(message: Any, shown: set[str]) -> None:
    shown.add(_message_key(message))


def _prompt_from_messages(value: Any, system_prompt: str, shown: set[str], system_shown: bool) -> tuple[str, bool]:
    messages = _messages_from_event(value)
    parts: list[str] = []
    if not system_shown:
        parts.append(f"[system]\n{system_prompt}")
        system_shown = True
    for message in messages:
        key = _message_key(message)
        if key in shown:
            continue
        shown.add(key)
        role = getattr(message, "type", None) or message.__class__.__name__
        parts.append(f"[{role}]\n{_message_text(message)}")
    return _preview("\n\n".join(parts), 12000), system_shown


def _messages_from_event(value: Any) -> list[Any]:
    if isinstance(value, Mapping):
        value = value.get("messages", [])
    if isinstance(value, (list, tuple)):
        messages: list[Any] = []
        for item in value:
            update = getattr(item, "update", None)
            if update is not None:
                messages.extend(_messages_from_event(update))
            elif isinstance(item, Mapping) and "update" in item:
                messages.extend(_messages_from_event(item["update"]))
            elif isinstance(item, BaseMessage):
                messages.append(item)
        return messages
    update = getattr(value, "update", None)
    if update is not None:
        return _messages_from_event(update)
    return []


def _message_text(message: Any) -> str:
    text = getattr(message, "text", None)
    if text is not None:
        return str(text)
    content = getattr(message, "content", "")
    return content if isinstance(content, str) else str(content or "")


def _tool_request(call: Mapping[str, Any], attempt_id: str, turn: int, *, kind: str) -> dict[str, Any]:
    return {
        "kind": kind,
        "name": call.get("name"),
        "tool_call_id": call.get("id"),
        "arguments": _safe_json(call.get("args", {})),
        "attempt_id": attempt_id,
        "turn": turn,
        "status": "requested",
    }


def _tool_result_value(value: Any) -> Any:
    if isinstance(value, ToolMessage):
        content = value.content
        if isinstance(content, str):
            try:
                parsed = json.loads(content)
            except json.JSONDecodeError:
                return content
            return parsed if isinstance(parsed, (dict, list)) else content
        return content
    return value


def _is_replayed_tool_result(value: Any) -> bool:
    if not isinstance(value, ToolMessage):
        return False
    metadata = getattr(value, "additional_kwargs", {}) or {}
    return isinstance(metadata, Mapping) and metadata.get("replayed") is True


def _visible_reasoning(message: Any) -> str | None:
    metadata = getattr(message, "response_metadata", {}) or {}
    if isinstance(metadata, Mapping):
        value = metadata.get("reasoning_summary") or metadata.get("rationale")
        return value if isinstance(value, str) else None
    return None
