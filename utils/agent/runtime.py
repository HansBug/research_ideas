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
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any, TypeVar
from urllib.parse import quote, urlsplit

from pydantic import BaseModel

from utils.llm import LLMConfig, LLMRegistry

try:
    from langchain.agents import create_agent
    from langchain.agents.middleware import AgentMiddleware, SummarizationMiddleware
    from langchain.agents.middleware.summarization import DEFAULT_SUMMARY_PROMPT
    from langchain_core.language_models import BaseChatModel
    from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessage, HumanMessage, SystemMessage, ToolMessage
    from langchain_core.messages.utils import count_tokens_approximately
    from langchain_core.callbacks import BaseCallbackHandler
    from langchain_core.outputs import ChatGeneration, ChatResult
    from langchain_core.tools import StructuredTool
    from pydantic import PrivateAttr
except Exception:  # pragma: no cover - import errors are reported at construction time
    create_agent = None  # type: ignore[assignment]
    AgentMiddleware = object  # type: ignore[assignment,misc]
    BaseChatModel = AIMessage = AIMessageChunk = BaseMessage = HumanMessage = SystemMessage = ToolMessage = object  # type: ignore[assignment,misc]
    ChatGeneration = ChatResult = object  # type: ignore[assignment,misc]
    StructuredTool = object  # type: ignore[assignment,misc]
    SummarizationMiddleware = object  # type: ignore[assignment,misc]
    DEFAULT_SUMMARY_PROMPT = ""  # type: ignore[assignment]
    count_tokens_approximately = None  # type: ignore[assignment]
    BaseCallbackHandler = object  # type: ignore[assignment,misc]

    def PrivateAttr(*args: Any, **kwargs: Any) -> None:  # type: ignore[misc]
        return None


T = TypeVar("T")
_MODEL_OPTIONS = frozenset({"streaming", "stream_usage", "timeout", "max_retries"})
_MODEL_CALL_OPTIONS = frozenset({"temperature", "top_p", "max_tokens", "stop", "seed", "verbosity"})
_IDENTITY_KEYS = frozenset(
    {"model", "base_url", "api_key", "headers", "authorization", "openai_api_key", "default_headers"}
)
_SECRET_KEY = re.compile(r"(api[_-]?key|authorization|token|secret|password|cookie|headers?)", re.I)
_USAGE_KEY = re.compile(
    r"^(?:usage|token[_-]?usage|(?:prompt|completion|input|output|total|reasoning|cached|cache_read_input|cache_creation_input|accepted_prediction|rejected_prediction|audio|text)[_-]?tokens?(?:[_-].*)?)$",
    re.I,
)
_NON_SECRET_FLAG_KEY = re.compile(r"(?:configured|present|enabled|set|available)$", re.I)
_NON_SECRET_NUMERIC_KEY = re.compile(r"(?:^|_)(?:context|context_window|context_basis|max_output|safe_input|compact_threshold|threshold|window|max_input|input|output|total|prompt|completion|cached|reasoning)(?:_tokens)?$", re.I)
_ENDPOINT_KEY = re.compile(r"(?:base[_-]?url|api[_-]?url|endpoint)", re.I)
_SECRET_MAPPING_CONTAINERS = frozenset({"headers", "default_headers"})
_BEARER_VALUE = re.compile(
    r"(?i)\bBearer\s*(?=[A-Za-z0-9._~+/=-]{8,}\b)(?=[A-Za-z0-9._~+/=-]*[0-9._~+/=-])"
    r"[A-Za-z0-9._~+/=-]+"
)
_BEARER_PROVIDER_VALUE = re.compile(
    r"(?i)\bBearer\s*(?:"
    r"(?:sk-ant-|sk-proj-)[A-Za-z0-9][A-Za-z0-9_-]{20,}|"
    r"(?:sk-|sess-)[A-Za-z0-9][A-Za-z0-9_-]{15,}|"
    r"(?:hf_|ghp_|gho_)[A-Za-z0-9]{20,}|"
    r"AIza[0-9A-Za-z_-]{20,}|AKIA[0-9A-Z]{16}|"
    r"gsk_[A-Za-z0-9_-]{24,}|pplx-[A-Za-z0-9_-]{24,}|r8_[A-Za-z0-9_-]{24,}|"
    r"xai-[A-Za-z0-9_-]{24,}|tgp_v1_[A-Za-z0-9_-]{24,}|fw_[A-Za-z0-9_-]{24,}|mist-[A-Za-z0-9_-]{24,})"
)
# Provider credential formats that are safe to recognise by prefix.  ``key-``
# is deliberately excluded: research identifiers commonly use that shape and
# configured credentials are still redacted through the run-scoped inventory.
_SECRET_VALUE = re.compile(
    r"(?:\b(?:sk-ant|sk-proj)[-_][A-Za-z0-9][A-Za-z0-9_-]{20,}\b|"
    r"\b(?:sk|sess)[-_][A-Za-z0-9]{16,}\b|\bhf_[A-Za-z0-9]{20,}\b|"
    r"\bgh[po]_[A-Za-z0-9]{20,}\b|\bAIza[0-9A-Za-z_-]{20,}\b|\bAKIA[0-9A-Z]{16}\b|"
    r"\bgsk_[A-Za-z0-9_-]{24,}\b|\bpplx-[A-Za-z0-9_-]{24,}\b|"
    r"\br8_[A-Za-z0-9_-]{24,}\b|"
    r"\bxai-[A-Za-z0-9_-]{24,}\b|\btgp_v1_[A-Za-z0-9_-]{24,}\b|"
    r"\bfw_[A-Za-z0-9_-]{24,}\b|\bmist-[A-Za-z0-9_-]{24,}\b)",
    re.I,
)
_PARTIAL_SECRET_VALUE = re.compile(
    r"\b(?:sk-ant|sk-proj)[-_][A-Za-z0-9_-]{2,}\.\.\.[A-Za-z0-9]{4,}\b|"
    r"\b(?:sk|sess|hf|gh[po]|gsk|pplx|r8)[-_][A-Za-z0-9]{2,}\.\.\.[A-Za-z0-9]{4,}\b|"
    r"\b(?:AIza|AKIA)[A-Za-z0-9]{2,}\.\.\.[A-Za-z0-9]{4,}\b|"
    r"\b(?:xai-|tgp_v1_|fw_|mist-)[A-Za-z0-9_-]{2,}\.\.\.[A-Za-z0-9]{4,}\b",
    re.I,
)
_CONTEXT_SECRET_VALUE = re.compile(
    r"(?i)(\b(?:api[ _-]?key|authorization|access[ _-]?token|user[ _-]?token|token|secret|credential|auth)\b\s*(?:[:=]\s*)?)"
    r"((?:sk-ant-|sk-proj-)[A-Za-z0-9][A-Za-z0-9_-]{20,}|"
    r"(?:sk-|sess-)[A-Za-z0-9][A-Za-z0-9_-]{15,}|"
    r"(?:hf_|ghp_|gho_)[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{20,}|AKIA[0-9A-Z]{16}|"
    r"(?:xai-|gsk_|pplx-|tgp_v1_|fw_|mist-|r8_)[A-Za-z0-9_-]{8,})"
)
_CONTEXT_SECRET_PREFIX = re.compile(
    r"(?i)\b(?:api[ _-]?key|authorization|access[ _-]?token|user[ _-]?token|token|secret|credential|auth)\b\s*(?:[:=]\s*)?$"
)
_DEFAULT_GRAPH_RECURSION_LIMIT = 1_000_000
_DEFAULT_COMPACT_TRIGGER_RATIO = 0.85
_DEFAULT_COMPACT_KEEP_MESSAGES = 20
_ELIGIBILITY_SCOPE = "agent_behavior_trace"


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
    retry_missing_structured_output: bool = False

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
        if self.retry_missing_structured_output and self.output_schema is None:
            raise ValueError(
                "agent_spec_invalid: retry_missing_structured_output needs output_schema"
            )
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
    usage: list[dict[str, Any]]
    error: dict[str, Any] | None
    real_llm: bool
    model: str
    observed_model: str | None
    academic_eligible: bool
    context_manifest_hash: str | None
    profile: str = "direct"
    context_window_tokens: int | None = None
    max_output_tokens: int | None = None
    safe_input_tokens: int | None = None
    capacity_source: dict[str, str] = field(default_factory=dict)
    eligibility_scope: str = _ELIGIBILITY_SCOPE
    eligibility_reasons: list[str] = field(default_factory=list)
    trace_commit_id: str | None = None
    model_calls_used: int = 0
    model_calls_reserved: int = 0
    compact_count: int = 0
    started_at_utc: str | None = None
    ended_at_utc: str | None = None
    duration_seconds: float | None = None

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
                    "profile": self.profile,
                    "context_window_tokens": self.context_window_tokens,
                    "max_output_tokens": self.max_output_tokens,
                    "safe_input_tokens": self.safe_input_tokens,
                    "capacity_source": self.capacity_source,
                    "eligibility_scope": self.eligibility_scope,
                    "eligibility_reasons": self.eligibility_reasons,
                    "trace_commit_id": self.trace_commit_id,
                    "model_calls_used": self.model_calls_used,
                    "model_calls_reserved": self.model_calls_reserved,
                    "compact_count": self.compact_count,
                    "started_at_utc": self.started_at_utc,
                    "ended_at_utc": self.ended_at_utc,
                    "duration_seconds": self.duration_seconds,
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
    for key in ("max_tokens", "max_completion_tokens"):
        value = (options or {}).get(key)
        if value is not None and (isinstance(value, bool) or not isinstance(value, int) or value <= 0):
            raise ValueError(f"model_call_options_invalid: {key} must be a positive integer")


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
    if not think_mode and options.get("reasoning_effort") is not None:
        raise ValueError("reasoning_effort requires think_mode=True")
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


def _dependency_versions() -> dict[str, str | None]:
    names = ("python", "langchain", "langgraph", "langchain-openai", "langchain-deepseek", "openai")
    result: dict[str, str | None] = {"python": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}"}
    for name in names[1:]:
        try:
            result[name] = version(name)
        except PackageNotFoundError:
            result[name] = None
    return result


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
    if key and _is_secret_key(key) and not (isinstance(value, Mapping) and key.lower() in _SECRET_MAPPING_CONTAINERS):
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
    return bool(_SECRET_KEY.search(key) and not _USAGE_KEY.fullmatch(key) and not _NON_SECRET_FLAG_KEY.search(key) and not _NON_SECRET_NUMERIC_KEY.search(key))


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


def _model_usage_candidates(value: Any) -> list[dict[str, Any]]:
    """Collect only public LangChain usage surfaces, retaining each observation."""

    candidates: list[dict[str, Any]] = []
    llm_output = getattr(value, "llm_output", None)
    if llm_output is None and isinstance(value, Mapping):
        llm_output = value.get("llm_output")
    if isinstance(llm_output, Mapping):
        usage_value = llm_output.get("token_usage") or llm_output.get("usage")
        if isinstance(usage_value, Mapping):
            candidates.append({"source": "llm_output.token_usage", "usage": dict(usage_value)})
    for message in _model_output_messages(value):
        usage_metadata = getattr(message, "usage_metadata", None)
        if isinstance(usage_metadata, Mapping):
            candidates.append({"source": "usage_metadata", "usage": dict(usage_metadata)})
        response_metadata = getattr(message, "response_metadata", {}) or {}
        if isinstance(response_metadata, Mapping):
            usage_value = response_metadata.get("token_usage") or response_metadata.get("usage")
            if isinstance(usage_value, Mapping):
                candidates.append({"source": "llm_output.token_usage", "usage": dict(usage_value)})
    return candidates


def _model_usage_info(value: Any) -> tuple[dict[str, Any] | None, list[dict[str, Any]], bool, str | None]:
    candidates = _model_usage_candidates(value)
    llm_output = getattr(value, "llm_output", None)
    if llm_output is None and isinstance(value, Mapping):
        llm_output = value.get("llm_output")
    selected: dict[str, Any] | None = None
    # usage_metadata is the terminal public message surface and wins over the
    # legacy llm_output mapping when both are present.
    for source in ("usage_metadata", "llm_output.token_usage"):
        selected_item = next((item for item in candidates if item["source"] == source), None)
        if selected_item is not None:
            selected = dict(selected_item["usage"])
            break
    normalized = [
        {
            "source": item["source"],
            "usage": _safe_json(item["usage"]),
        }
        for item in candidates
    ]
    comparable = [
        (
            _usage_number(item["usage"], "input_tokens", "prompt_tokens"),
            _usage_number(item["usage"], "output_tokens", "completion_tokens"),
            _usage_number(item["usage"], "total_tokens"),
        )
        for item in candidates
    ]
    # Cache and reasoning details are part of provider usage too.  Comparing
    # only input/output/total lets two contradictory observations look equal.
    def usage_signature(item_usage: Mapping[str, Any]) -> tuple[int | None, ...]:
        input_details = item_usage.get("input_token_details")
        output_details = item_usage.get("output_token_details")
        input_details = input_details if isinstance(input_details, Mapping) else {}
        output_details = output_details if isinstance(output_details, Mapping) else {}

        def first_number(*values: int | None) -> int | None:
            return next((value for value in values if value is not None), None)

        return (
            _usage_number(item_usage, "input_tokens", "prompt_tokens"),
            _usage_number(item_usage, "output_tokens", "completion_tokens"),
            _usage_number(item_usage, "total_tokens"),
            first_number(
                _usage_number(input_details, "cache_read", "cached_tokens", "cache_read_input_tokens"),
                _usage_number(item_usage, "cache_read", "cached_tokens", "cache_read_input_tokens"),
            ),
            first_number(
                _usage_number(input_details, "cache_creation", "cache_creation_input_tokens", "cache_write_tokens"),
                _usage_number(item_usage, "cache_creation", "cache_creation_input_tokens", "cache_write_tokens"),
            ),
            first_number(
                _usage_number(output_details, "reasoning", "reasoning_tokens"),
                _usage_number(item_usage, "reasoning", "reasoning_tokens"),
            ),
        )

    comparable = [usage_signature(item["usage"]) for item in candidates]
    conflict = len({item for item in comparable if any(value is not None for value in item)}) > 1
    observed_model: str | None = None
    for message in _model_output_messages(value):
        response_metadata = getattr(message, "response_metadata", {}) or {}
        if isinstance(response_metadata, Mapping):
            candidate = response_metadata.get("model_name") or response_metadata.get("model")
            if isinstance(candidate, str):
                observed_model = observed_model or candidate
    if observed_model is None and isinstance(llm_output, Mapping):
        candidate = llm_output.get("model_name") or llm_output.get("model")
        if isinstance(candidate, str):
            observed_model = candidate
    return selected, normalized, conflict, observed_model


def _validate_compact_trigger_ratio(value: float | None) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AgentError("config_error", "compact_trigger_ratio must be a number or None")
    ratio = float(value)
    if not math.isfinite(ratio) or not 0 < ratio <= 1:
        raise AgentError("config_error", "compact_trigger_ratio must be in (0, 1]")
    return ratio


def _usage_number(usage: Mapping[str, Any] | None, *keys: str) -> int | None:
    if not isinstance(usage, Mapping):
        return None
    for key in keys:
        value = usage.get(key)
        if isinstance(value, (int, float)) and math.isfinite(float(value)) and value >= 0:
            return int(value)
    return None


def _normalize_usage(
    usage: Mapping[str, Any] | None,
    *,
    model: str,
    call_kind: str,
    turn: int,
    status: str = "completed",
    observed_usages: Sequence[Mapping[str, Any]] | None = None,
    usage_conflict: bool = False,
    response_id: str | None = None,
) -> dict[str, Any]:
    """Normalize public LangChain/provider usage without inventing missing values."""

    input_tokens = _usage_number(usage, "input_tokens", "prompt_tokens")
    output_tokens = _usage_number(usage, "output_tokens", "completion_tokens")
    total_tokens = _usage_number(usage, "total_tokens")
    if total_tokens is None and input_tokens is not None and output_tokens is not None:
        total_tokens = input_tokens + output_tokens
    input_details = dict(usage.get("input_token_details") or {}) if isinstance(usage, Mapping) and isinstance(usage.get("input_token_details"), Mapping) else {}
    output_details = dict(usage.get("output_token_details") or {}) if isinstance(usage, Mapping) and isinstance(usage.get("output_token_details"), Mapping) else {}
    cache_read = _usage_number(input_details, "cache_read", "cached_tokens", "cache_read_input_tokens")
    cache_creation = _usage_number(input_details, "cache_creation", "cache_creation_input_tokens", "cache_write_tokens")
    reasoning = _usage_number(output_details, "reasoning", "reasoning_tokens")
    if cache_read is None:
        cache_read = _usage_number(usage, "cache_read", "cached_tokens", "prompt_cache_hit_tokens")
    if cache_creation is None:
        cache_creation = _usage_number(usage, "cache_creation", "cache_creation_input_tokens", "cache_write_tokens", "prompt_cache_miss_tokens")
    if reasoning is None:
        reasoning = _usage_number(usage, "reasoning", "reasoning_tokens")
    return {
        "model_call_id": None,
        "call_kind": call_kind,
        "turn": turn,
        "started_at_utc": None,
        "ended_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "model": model,
        "response_id": response_id,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "input_token_details": {"cache_read": cache_read, "cache_creation": cache_creation},
        "output_token_details": {"reasoning": reasoning},
        "source": "provider" if usage else "unavailable",
        "unavailable_reason": None if usage else "adapter_did_not_expose_provider_usage",
        "usage_conflict": usage_conflict,
        "observed_usage": _safe_json(dict(usage or {})),
        "observed_usages": _safe_json(list(observed_usages or [])),
    }


class _ContextMeter:
    """One conservative context measurement shared by display and middleware.

    Provider usage describes a completed request, while the next request also
    contains newly appended AI/tool messages.  Keep the completed request's
    anchors and add only a public LangChain estimate for that delta.  The pure
    estimate remains available to ``SummarizationMiddleware`` so a stale
    provider anchor can never control its trigger.
    """

    def __init__(self, *, tools: Sequence[Any] = (), system_prompt: str = "", output_schema: type[BaseModel] | None = None):
        self.tools = _langchain_tools(tools)
        self.system_prompt = system_prompt
        self.output_schema = output_schema
        self.provider_input: int | None = None
        self.provider_total: int | None = None
        self.primary_input_keys: tuple[str, ...] = ()
        self.primary_output_keys: tuple[str, ...] = ()
        self.last_sources: list[str] = []

    def begin_primary(self, messages: Iterable[Any] = ()) -> None:
        """Remember the next request while retaining the provider anchor.

        A provider's terminal usage belongs to the previous request, but it is
        still the most accurate anchor for the next request's growing prefix.
        It is invalidated only when official compaction replaces that prefix.
        """

        self.primary_input_keys = tuple(_message_key(message) for message in messages)

    def record(
        self,
        usage: Mapping[str, Any] | None,
        *,
        call_kind: str = "primary",
        observed_usages: Sequence[Mapping[str, Any]] | None = None,
    ) -> None:
        if call_kind != "primary":
            return
        candidates: list[Mapping[str, Any]] = []
        if isinstance(usage, Mapping):
            candidates.append(usage)
        for item in observed_usages or ():
            candidate = item.get("usage") if isinstance(item, Mapping) else None
            if isinstance(candidate, Mapping):
                candidates.append(candidate)
        input_values = [_usage_number(item, "input_tokens", "prompt_tokens") for item in candidates]
        total_values = [_usage_number(item, "total_tokens") for item in candidates]
        input_tokens = max((value for value in input_values if value is not None), default=None)
        total_tokens = max((value for value in total_values if value is not None), default=None)
        if input_tokens is not None:
            self.provider_input = max(self.provider_input or 0, input_tokens)
        if total_tokens is not None:
            self.provider_total = max(self.provider_total or 0, total_tokens)

    def finish_primary(self, messages: Iterable[Any]) -> None:
        self.primary_output_keys = tuple(_message_key(message) for message in messages)

    def invalidate_provider_anchor(self) -> None:
        """Invalidate usage from the pre-compact primary state."""

        self.provider_input = None
        self.provider_total = None
        self.primary_input_keys = ()
        self.primary_output_keys = ()

    def estimate(self, messages: Iterable[Any]) -> int | None:
        if count_tokens_approximately is None:
            return None
        try:
            return int(
                count_tokens_approximately(
                    ([SystemMessage(content=self.system_prompt)] if self.system_prompt else [])
                    + list(messages)
                    + ([SystemMessage(content=json.dumps(self.output_schema.model_json_schema(), ensure_ascii=False, sort_keys=True))] if self.output_schema is not None else []),
                    tools=self.tools or None,
                    use_usage_metadata_scaling=False,
                )
            )
        except Exception:
            return None

    @staticmethod
    def _message_delta(messages: Sequence[Any], prefix: tuple[str, ...]) -> list[Any]:
        if not prefix:
            return list(messages)
        keys = tuple(_message_key(message) for message in messages)
        if len(keys) >= len(prefix) and keys[: len(prefix)] == prefix:
            return list(messages[len(prefix) :])
        return list(messages)

    @staticmethod
    def _estimate_delta(messages: Sequence[Any]) -> int | None:
        if not messages or count_tokens_approximately is None:
            return 0
        try:
            return int(count_tokens_approximately(messages, use_usage_metadata_scaling=False))
        except Exception:
            return None

    def count(self, messages: Iterable[Any]) -> tuple[int | None, list[str]]:
        current = list(messages)
        estimate = self.estimate(current)
        if estimate is None:
            return None, ["unavailable"]
        candidates: list[tuple[int, str]] = [(estimate, "langchain_estimate")]
        if self.provider_total is not None:
            prefix = self.primary_output_keys or self.primary_input_keys
            delta = self._estimate_delta(self._message_delta(current, prefix))
            if delta is not None:
                candidates.append((self.provider_total + delta, "provider_total_anchor"))
        if self.provider_input is not None:
            delta = self._estimate_delta(self._message_delta(current, self.primary_input_keys))
            if delta is not None:
                candidates.append((self.provider_input + delta, "provider_input_plus_delta"))
        value = max(candidates, key=lambda item: item[0])[0]
        sources = [name for candidate, name in candidates if candidate == value]
        self.last_sources = sources
        return value, sources


def _model_capacity(model: Any, config: LLMConfig, *, max_output_override: int | None = None) -> tuple[int | None, int | None, int | None, dict[str, str]]:
    """Resolve capacity only from explicit config or an effective official endpoint."""

    context = config.context_window_tokens
    max_output = max_output_override if max_output_override is not None else config.max_output_tokens
    sources = {
        "context_window": "config" if context is not None else "unknown",
        "max_output": "run_override" if max_output_override is not None else ("config" if max_output is not None else "unknown"),
    }
    if context is None or max_output is None:
        profile = getattr(model, "profile", None)
        profile = profile if isinstance(profile, Mapping) else {}
        if context is None and isinstance(profile.get("max_input_tokens"), int):
            context = int(profile["max_input_tokens"])
            sources["context_window"] = "official_profile"
        if max_output is None and isinstance(profile.get("max_output_tokens"), int):
            max_output = int(profile["max_output_tokens"])
            sources["max_output"] = "official_profile"
    # LangChain's official model profile exposes ``max_input_tokens`` as the
    # input capacity used by SummarizationMiddleware.  Do not subtract the
    # separately reported output reserve locally: that would silently lower
    # the provider's documented context capacity and trigger compact early.
    safe_input = context
    return context, max_output, safe_input, sources


def _effective_model_base_url(model: Any, config: LLMConfig | None = None) -> Any:
    root_client = getattr(model, "root_client", None)
    return (
        getattr(model, "openai_api_base", None)
        or getattr(model, "base_url", None)
        or getattr(root_client, "base_url", None)
        or (config.base_url if config is not None else None)
    )


def _endpoint_fingerprint(value: Any) -> str | None:
    if not value:
        return None
    try:
        parsed = urlsplit(str(value))
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            return None
        host = parsed.hostname.lower()
        port = parsed.port
        path = parsed.path.rstrip("/")
        normalized = f"{parsed.scheme.lower()}://{host}{f':{port}' if port is not None else ''}{path}"
        return "sha256:" + hashlib.sha256(("agent-endpoint\0" + normalized).encode("utf-8")).hexdigest()
    except (TypeError, ValueError):
        return None


def _behavior_fingerprint(payload: Mapping[str, Any]) -> str:
    return _hash_text(json.dumps(_safe_json(dict(payload)), ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def _sensitive_inventory(config: LLMConfig, pages: Sequence[Mapping[str, Any]]) -> tuple[str, ...]:
    values: set[str] = set()
    if config.api_key is not None:
        values.add(config.api_key.get_secret_value())
    for page in pages:
        for key, value in page.items():
            if _is_secret_key(str(key)) and isinstance(value, str) and value:
                values.add(value)
    return tuple(sorted((value for value in values if len(value) >= 4), key=len, reverse=True))


class _StreamHoldback:
    """Hold only a credential-shaped token across streamed chunk boundaries."""

    _PREFIXES = (
        "sk-", "sk-ant-", "sk-proj-", "sess-", "hf_", "ghp_", "gho_", "AIza", "AKIA", "xai-", "gsk_", "pplx-", "tgp_v1_", "fw_", "mist-", "r8_", "Bearer ", "Bearer",
    )
    _URL_PREFIXES = ("http://", "https://")

    def __init__(self, secrets: Sequence[str]):
        self.secrets = tuple(secrets)
        self.buffer = ""
        self.withheld_chars = 0
        self.redaction_hits = 0

    def _safe_end(self) -> int:
        end = len(self.buffer)
        for secret in self.secrets:
            position = self.buffer.find(secret)
            if position >= 0:
                end = position
                break

            # Keep a suffix that is a prefix of a configured secret.  This is
            # the only inventory-based holdback needed for a split token.
            for size in range(min(len(secret) - 1, len(self.buffer)), 0, -1):
                start = len(self.buffer) - size
                if self.buffer[start:] == secret[:size]:
                    end = min(end, start)
                    break

        token_end = len(self.buffer.rstrip(" \n\t\r"))
        token_prefix = self.buffer[:token_end]
        token_start = max(
            token_prefix.rfind(" "), token_prefix.rfind("\n"), token_prefix.rfind("\t"), token_prefix.rfind("\r")
        ) + 1
        token_tail = self.buffer[token_start:]
        delimiter = re.search(r"\s", token_tail)
        token = token_tail if delimiter is None else token_tail[: delimiter.start()]
        # A delimited token is complete and can be released immediately.  An
        # unterminated credential-shaped token stays buffered until the next
        # chunk or the terminal callback, so a split credential cannot leak.
        if delimiter is None:
            token_lower = token.lower()
            if any(
                prefix.lower().startswith(token_lower) or token_lower.startswith(prefix.lower())
                for prefix in self._PREFIXES
            ):
                hold_start = token_start
                context = self.buffer[:token_start]
                context_match = _CONTEXT_SECRET_PREFIX.search(context)
                if context_match is not None:
                    hold_start = context_match.start()
                end = min(end, hold_start)
            for separator in ("=", ":"):
                separator_position = token_lower.find(separator)
                if separator_position <= 0:
                    continue
                candidate = token_lower[separator_position + 1 :]
                if not candidate:
                    continue
                if any(
                    prefix.lower().startswith(candidate) or candidate.startswith(prefix.lower())
                    for prefix in self._PREFIXES
                ):
                    context = self.buffer[:token_start] + token[: separator_position + 1]
                    context_match = _CONTEXT_SECRET_PREFIX.search(context)
                    if context_match is not None:
                        end = min(end, context_match.start())
                        break
            if any(prefix.startswith(token_lower) or token_lower.startswith(prefix) for prefix in self._URL_PREFIXES):
                # URL credentials/query values can be split after the scheme
                # or parameter name; keep the URL token for one parser pass.
                end = min(end, token_start)
        elif delimiter.start() == len(token_tail) - 1:
            # ``Bearer `` can be split exactly after its delimiter.  Keep the
            # prefix until the following chunk so the bearer value is redacted
            # as one credential rather than emitting a marker and leaking the
            # value on its own.
            if any(prefix.rstrip().lower() == token.lower() for prefix in self._PREFIXES):
                end = min(end, token_start)
        trailing_context = _CONTEXT_SECRET_PREFIX.search(self.buffer)
        if trailing_context is not None:
            end = min(end, trailing_context.start())
        return max(0, end)

    def feed(self, text: str, *, final: bool = False) -> str:
        self.buffer += str(text)
        if final:
            safe = self.buffer
            self.buffer = ""
        else:
            end = self._safe_end()
            safe = self.buffer[:end]
            self.buffer = self.buffer[end:]
            self.withheld_chars += len(self.buffer)
        redacted = _redact_with_inventory(safe, self.secrets)
        if redacted != safe:
            self.redaction_hits += 1
        return redacted

    def report(self, channel: str) -> dict[str, Any]:
        return {
            "channel": channel,
            "hits": self.redaction_hits,
            "withheld_chars": self.withheld_chars,
        }


def _redact_credential_url(value: str) -> str:
    """Redact credentials in a URL while preserving ordinary URL content."""

    try:
        parsed = urlsplit(value)
    except ValueError:
        return value
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return value
    if parsed.username is not None or parsed.password is not None:
        host = parsed.hostname or ""
        if ":" in host:
            host = f"[{host}]"
        if parsed.port is not None:
            host = f"{host}:{parsed.port}"
        netloc = f"[redacted]@{host}"
    else:
        netloc = parsed.netloc
    query = parsed.query
    if query:
        fields = []
        for part in query.split("&"):
            key, _, item = part.partition("=")
            if _is_secret_key(key) or (item and _SECRET_VALUE.search(item)):
                fields.append(f"{key}={quote('[redacted]', safe='')}")
            else:
                fields.append(part)
        query = "&".join(fields)
    return parsed._replace(netloc=netloc, query=query).geturl()


def _redact_text(value: str, *, redact_endpoints: bool = False) -> str:
    value = _PARTIAL_SECRET_VALUE.sub("[redacted_secret]", value)
    value = _BEARER_PROVIDER_VALUE.sub("Bearer [redacted_bearer]", value)
    value = _SECRET_VALUE.sub("[redacted_secret]", value)
    value = _CONTEXT_SECRET_VALUE.sub(r"\1[redacted_secret]", value)
    value = _BEARER_VALUE.sub("Bearer [redacted_bearer]", value)
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
    else:
        # In ordinary model text, keep normal links intact but scrub only URL
        # userinfo/query credentials.
        value = re.sub(
            r"https?://[^\s'\"},)]*",
            lambda match: _redact_credential_url(match.group(0)),
            value,
            flags=re.I,
        )
    return value


def _redact_public(value: Any) -> Any:
    safe = _redact(_safe_json(value))
    if isinstance(value, BaseModel):
        try:
            return type(value).model_validate(safe)
        except Exception:
            return safe
    return safe


def _redact_with_inventory(value: Any, secrets: Sequence[str]) -> Any:
    """Apply the normal structural policy plus exact run-scoped credentials."""

    if isinstance(value, BaseModel):
        redacted = _redact_with_inventory(_redact(_safe_json(value)), secrets)
        if isinstance(redacted, Mapping):
            try:
                return type(value).model_validate(redacted)
            except Exception:
                return redacted
        return redacted
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            if _is_secret_key(key_text) and not (isinstance(item, Mapping) and key_text.lower() in _SECRET_MAPPING_CONTAINERS):
                result[key_text] = "[redacted]"
            elif _ENDPOINT_KEY.search(key_text) and isinstance(item, str):
                result[key_text] = _redact_with_inventory(_redact_text(item, redact_endpoints=True), secrets)
            else:
                result[key_text] = _redact_with_inventory(item, secrets)
        return result
    if isinstance(value, (list, tuple)):
        return [_redact_with_inventory(item, secrets) for item in value]
    if isinstance(value, str):
        value = _redact_text(value)
        for secret in secrets:
            if secret:
                value = value.replace(secret, "[redacted_secret]")
                if len(secret) >= 8:
                    prefix = secret[:6]
                    suffix = secret[-4:]
                    value = re.sub(
                        re.escape(prefix) + r"\.\.\." + re.escape(suffix),
                        "[redacted_secret]",
                        value,
                        flags=re.I,
                    )
                    value = re.sub(
                        rf"(?i)(\bapi[ _-]?key\b[^\n]{{0,20}}['\"]?\.\.\.){re.escape(suffix)}\b",
                        r"\1[redacted_secret]",
                        value,
                    )
                    value = re.sub(
                        rf"(?i)(\b(?:key|token|secret)\b[^\n]{{0,20}}\b(?:ending|suffix|fingerprint)\b[^\n]{{0,12}}\.\.\.){re.escape(suffix)}\b",
                        r"\1[redacted_secret]",
                        value,
                    )
                    value = re.sub(
                        rf"(?i)(\bkey\b\s+['\"]?\.\.\.){re.escape(suffix)}\b(?=[^\.\n]{{0,20}}\b(?:invalid|rejected|expired|revoked|unauthorized|error)\b)",
                        r"\1[redacted_secret]",
                        value,
                    )
                    # Provider diagnostics may spell out a key suffix without
                    # an ellipsis.  Redact only when the same line contains
                    # both credential/error language and a suffix marker; a
                    # bare academic number remains untouched.
                    for suffix_size in (8, 6, 4):
                        suffix_value = secret[-suffix_size:]
                        marker = re.compile(r"(?i)\b(?:ending|ends?|suffix|last|tail|fingerprint|finishes?)\b")
                        credential_context = re.compile(
                            r"(?i)\b(?:api[ _-]?key|key|token|secret|credential|invalid|rejected|expired|revoked|unauthorized|error)\b"
                        )
                        suffix_pattern = re.compile(rf"(?i)(?<![A-Za-z0-9]){re.escape(suffix_value)}(?![A-Za-z0-9])")
                        lines = value.splitlines(keepends=True)
                        for index, line in enumerate(lines):
                            if marker.search(line) and credential_context.search(line) and suffix_pattern.search(line):
                                lines[index] = suffix_pattern.sub("[redacted_secret]", line)
                        value = "".join(lines)
        return value
    return value


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


def _atomic_write(path: Path, payload: Mapping[str, Any], *, run_id: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    suffix = f".{run_id}" if run_id else ""
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}{suffix}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(_safe_json(payload), stream, ensure_ascii=False, sort_keys=True, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        _fsync_parent(path)
    except Exception:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(temporary)
        raise


def _fsync_parent(path: Path) -> None:
    try:
        fd = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    except OSError:
        pass


class _AuditWriter:
    def __init__(self, path: Path | None, run_id: str, *, result_path: Path | None = None):
        self.path = path
        self.result_path = result_path
        self.run_id = run_id
        self.temporary: Path | None = None
        self.trace_commit_id = uuid.uuid4().hex
        self.published = False
        self.lock_paths: list[Path] = []
        self._lock_files: list[Any] = []
        self.sensitive_values: tuple[str, ...] = ()
        try:
            if path is not None or result_path is not None:
                if path is not None and path.exists() and not path.is_file():
                    raise OSError("audit output path is not a file")
                if result_path is not None and result_path.exists() and not result_path.is_file():
                    raise OSError("result output path is not a file")
                anchor = path or result_path
                assert anchor is not None
                anchor.parent.mkdir(parents=True, exist_ok=True)
                receipt = path.with_name(path.name + ".receipt.json") if path is not None else None
                targets = sorted({target for target in (path, result_path, receipt) if target is not None}, key=str)
                self.lock_paths = [target.with_name(target.name + ".lock") for target in targets]
                import fcntl
                for lock_path in self.lock_paths:
                    lock_file = lock_path.open("a+", encoding="utf-8")
                    try:
                        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    except OSError as exc:
                        lock_file.close()
                        raise OSError("audit/result output is already locked") from exc
                    self._lock_files.append(lock_file)
                if path is not None:
                    self.temporary = path.with_name(f".{path.name}.{run_id}.part")
                    if self.temporary.exists():
                        raise OSError("audit output part already exists")
                    fd = os.open(self.temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                    self.stream = os.fdopen(fd, "w", encoding="utf-8")
                else:
                    self.stream = None
            else:
                self.stream = None
        except (ImportError, OSError) as exc:
            self.release_lock()
            raise AgentError("audit_write_failed", "audit output cannot be opened") from exc
        self.order = 0

    @property
    def enabled(self) -> bool:
        return self.stream is not None

    def write(self, record: Mapping[str, Any]) -> None:
        if self.stream is None:
            return
        self.order += 1
        payload = _redact_with_inventory(
            _safe_json({"run_id": self.run_id, "seq": self.order, "order": self.order, "recorded_at_utc": datetime.now(timezone.utc).isoformat(), **record}),
            self.sensitive_values,
        )
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
                    _fsync_parent(self.path)
                    self.temporary = None
                    self.published = True
            except (OSError, ValueError) as exc:
                with contextlib.suppress(OSError):
                    self.stream.close()
                if self.temporary is not None:
                    with contextlib.suppress(OSError):
                        os.unlink(self.temporary)
                    self.temporary = None
                raise AgentError("audit_write_failed", "audit output could not be finalized") from exc

    def set_sensitive_values(self, values: Sequence[str]) -> None:
        self.sensitive_values = tuple(value for value in values if value)

    def release_lock(self) -> None:
        if not self._lock_files:
            return
        import fcntl
        for lock_file in self._lock_files:
            with contextlib.suppress(Exception):
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            with contextlib.suppress(Exception):
                lock_file.close()
        self._lock_files = []


def _file_sha256(path: Path | None) -> str | None:
    if path is None or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _publish_receipt(audit_path: Path | None, result_path: Path | None, *, run_id: str, trace_commit_id: str, finish_seq: int, eligibility_scope: str, status: str) -> tuple[bool, Path | None]:
    if audit_path is None or not audit_path.is_file():
        return False, None
    receipt = audit_path.with_name(audit_path.name + ".receipt.json")
    payload = {
        "run_id": run_id,
        "trace_commit_id": trace_commit_id,
        "audit_sha256": _file_sha256(audit_path),
        "result_sha256": _file_sha256(result_path),
        "finish_seq": finish_seq,
        "eligibility_scope": eligibility_scope,
        "artifact_status": "committed",
        "agent_status": status,
    }
    try:
        _atomic_write(receipt, payload, run_id=run_id)
        observed = json.loads(receipt.read_text(encoding="utf-8"))
        if observed != payload or _file_sha256(audit_path) != payload["audit_sha256"] or _file_sha256(result_path) != payload["result_sha256"]:
            return False, receipt
    except Exception:
        return False, receipt
    return True, receipt


def _validate_output_paths(audit_path: Path | None, result_path: Path | None) -> tuple[Path | None, Path | None]:
    try:
        audit = audit_path.resolve(strict=False) if audit_path is not None else None
        result = result_path.resolve(strict=False) if result_path is not None else None
    except (OSError, RuntimeError) as exc:
        raise AgentError("config_error", "output path cannot be resolved") from exc
    receipt = audit.with_name(audit.name + ".receipt.json") if audit is not None else None
    if audit is not None and result is not None and audit == result:
        raise AgentError("config_error", "audit_out and result_out must be different files")
    if receipt is not None and result is not None and receipt == result:
        raise AgentError("config_error", "result_out must not overwrite the audit receipt")
    # A caller must not select a derived sidecar as an output target.  This
    # check is structural (and therefore catches paths that do not exist yet),
    # unlike ``samefile`` which can only inspect existing inodes.
    output_targets = {target for target in (audit, result) if target is not None}
    derived_sidecars = {
        sidecar
        for target in (audit, result, receipt)
        if target is not None
        for sidecar in (
            target.with_name(target.name + ".receipt.json"),
            target.with_name(target.name + ".lock"),
        )
    }
    conflicting_sidecars = output_targets & derived_sidecars
    if conflicting_sidecars:
        conflict = sorted(str(path) for path in conflicting_sidecars)[0]
        raise AgentError("config_error", f"output path conflicts with a derived sidecar: {conflict}")
    for left, right in ((audit, result), (audit, receipt), (result, receipt)):
        if left is None or right is None or not left.exists() or not right.exists():
            continue
        try:
            if left.samefile(right):
                raise AgentError("config_error", "audit/result/receipt paths alias the same file")
        except OSError:
            continue
    derived = [path for path in (audit, result, receipt) if path is not None]
    derived.extend(path.with_name(path.name + ".lock") for path in (audit, result, receipt) if path is not None)
    for target in (audit, result):
        if target is None:
            continue
        stale_parts = list(target.parent.glob(f".{target.name}.*.part"))
        if stale_parts:
            raise AgentError("config_error", f"output part already exists: {stale_parts[0]}")
        derived.extend(stale_parts)
    for index, left in enumerate(derived):
        for right in derived[index + 1 :]:
            if not left.exists() or not right.exists():
                continue
            try:
                if left.samefile(right):
                    raise AgentError("config_error", "audit/result/receipt/part paths alias the same file")
            except OSError:
                continue
    return audit, result


def _level_for_event(kind: str) -> int:
    if kind == "heartbeat":
        return logging.DEBUG
    if kind in {"context_failed", "tool_failed", "model_failed", "compaction_failed"}:
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
        self._compact_live = None
        self._compact_id = None
        self._compact_text = ""
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
            "run_started": f"AGENT RUN | profile={data.get('profile')} model={data.get('model')} real={data.get('real_llm')}",
            "heartbeat": f"heartbeat elapsed={data.get('elapsed_seconds', 0):.1f}s",
            "context_loaded": f"context loaded pages={data.get('page_count')} manifest={data.get('context_manifest_hash')}",
            "context_failed": f"context failed code={data.get('code')} message={data.get('message')}",
            "model_started": f"\n================ TURN {data.get('turn')} | MODEL INPUT ================\n" + (f"input messages:\n{_preview(str(data.get('prompt', '')), 12000)}" if data.get("prompt") else ""),
            "model_text": "MODEL OUTPUT | ASSISTANT",
            "model_completed": f"TURN {data.get('turn')} | MODEL OUTPUT | tool_count={data.get('tool_count')}",
            "tool_started": f"MODEL OUTPUT | TOOL CALL name={data.get('name')} id={data.get('tool_call_id')}",
            "tool_completed": f"TOOL RESULT -> NEXT MODEL INPUT name={data.get('name')} id={data.get('tool_call_id')}",
            "tool_failed": f"TOOL ERROR name={data.get('name')}",
            "structured_output": "MODEL OUTPUT | STRUCTURED CALL",
            "context_usage": "\n".join(str(line) for line in data.get("lines", ())),
            "failed": f"\n################ AGENT FAILED ##################\ncode={data.get('code')} message={data.get('message')}\n#################################################",
        }
        return messages.get(event.kind, f"{event.kind}: {data}")

    @staticmethod
    def _mapping(value: Any) -> Mapping[str, Any]:
        return value if isinstance(value, Mapping) else {}

    @staticmethod
    def _number(value: Any) -> str:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return "unknown"
        return f"{value:,.0f}"

    @staticmethod
    def _setting(value: Any, *, default: str = "unknown") -> str:
        if value is None:
            return default
        if isinstance(value, bool):
            return str(value).lower()
        return str(value)

    @staticmethod
    def _fingerprint(value: Any) -> str:
        if value is None:
            return "unavailable"
        text = str(value)
        prefix, separator, digest = text.partition(":")
        if separator and prefix == "sha256":
            return f"sha256:{digest[:12]}"
        if re.fullmatch(r"[0-9a-fA-F]{32,}", text):
            return f"sha256:{text[:12]}"
        return _preview(text, 24)

    @staticmethod
    def _first(*values: Any, default: Any = None) -> Any:
        return next((value for value in values if value is not None), default)

    def _run_started_body(self, event: AgentEvent) -> Any:
        cls = self
        data = event.data
        effective = cls._mapping(data.get("effective_options"))
        inference = cls._mapping(data.get("inference"))
        capacity = cls._mapping(data.get("capacity"))
        capacity_source = cls._mapping(
            cls._first(
                data.get("capacity_source"), capacity.get("capacity_source"), capacity.get("source"), default={}
            )
        )
        limits = cls._mapping(data.get("limits"))
        compact = cls._mapping(data.get("compact"))

        def option(name: str, *aliases: str, default: Any = None) -> Any:
            keys = (name, *aliases)
            for source in (data, effective, inference):
                for key in keys:
                    if source.get(key) is not None:
                        return source[key]
            return default

        tool_value = cls._first(data.get("tool_names"), data.get("tools"), default=())
        if isinstance(tool_value, str):
            tool_names = tool_value
        elif isinstance(tool_value, Sequence):
            names = [item.get("name") if isinstance(item, Mapping) else str(item) for item in tool_value]
            tool_names = ", ".join(str(name) for name in names if name) or "none"
        else:
            tool_names = "none"

        sampling = cls._mapping(option("sampling", default={}))

        def sampling_value(key: str, value: Any) -> Any:
            if key != "stop":
                return value
            if isinstance(value, str):
                return 1
            return len(value) if isinstance(value, Sequence) else 1

        if sampling:
            sampling_text = ",".join(
                f"{key}={sampling_value(key, value)}"
                for key, value in sampling.items()
                if value is not None
            )
        else:
            sampling_fields = {
                key: option(key)
                for key in ("temperature", "top_p", "seed", "verbosity", "stop")
            }
            configured = {key: value for key, value in sampling_fields.items() if value is not None}
            sampling_text = (
                ",".join(
                    f"{key}={sampling_value(key, value)}"
                    for key, value in configured.items()
                )
                if configured
                else "provider-default"
            )

        def limit(name: str) -> str:
            value = limits.get(name)
            return "unlimited" if value is None else str(value)

        context_window = cls._first(
            data.get("context_window_tokens"), capacity.get("context_window_tokens"), capacity.get("context_window")
        )
        max_output = cls._first(
            data.get("max_output_tokens"), capacity.get("max_output_tokens"), capacity.get("max_output")
        )
        safe_input = cls._first(
            data.get("safe_input_tokens"), capacity.get("safe_input_tokens"), capacity.get("safe_input")
        )
        context_source = capacity_source.get("context_window", "unknown")
        output_source = capacity_source.get("max_output", "unknown")
        compact_ratio = cls._first(
            data.get("compact_trigger_ratio"), compact.get("trigger_ratio"), compact.get("ratio")
        )
        compact_threshold = cls._first(
            data.get("compact_threshold_tokens"), compact.get("threshold_tokens"), compact.get("threshold")
        )
        compact_enabled = cls._first(data.get("compact_enabled"), compact.get("enabled"))
        if compact_enabled is None:
            compact_enabled = compact_ratio is not None
        ratio_text = f"{float(compact_ratio) * 100:g}%" if isinstance(compact_ratio, (int, float)) else "unknown"
        summary = cls._first(compact.get("summary"), data.get("summary_model"), default="same model/inference")
        keep = cls._first(compact.get("keep_messages"), data.get("compact_keep_messages"), default=20)

        config_fingerprint = cls._fingerprint(data.get("config_fingerprint"))
        endpoint_fingerprint = cls._fingerprint(data.get("endpoint_fingerprint"))
        output_schema = cls._first(
            data.get("output_schema_name"), data.get("output_schema"), data.get("structured_output")
        )
        if isinstance(output_schema, Mapping):
            output_schema = output_schema.get("title") or "configured"
        strategy = cls._first(
            data.get("structured_output_strategy"),
            data.get("structured_output_mode"),
            default="langgraph-auto" if output_schema else "none",
        )

        lines = (
            f"run       id={event.run_id} · agent={cls._setting(cls._first(data.get('agent'), data.get('agent_name'), data.get('name')))} · profile={cls._setting(data.get('profile'), default='direct')} · model={cls._setting(data.get('model'))} · real={cls._setting(data.get('real_llm'))}",
            f"model     adapter={cls._setting(data.get('adapter'), default='unknown')} · config={config_fingerprint} · endpoint={endpoint_fingerprint} · stream={cls._setting(option('streaming'))} · usage={cls._setting(option('stream_usage'))}",
            f"inference think={cls._setting(option('think_mode'), default='false')} · effort={cls._setting(option('reasoning_effort'), default='none')} · sampling={sampling_text} · retries={cls._setting(option('max_retries'), default='unknown')} · timeout={cls._setting(option('timeout'), default='default')}",
            f"behavior  system={cls._fingerprint(data.get('system_prompt_hash'))} · tools={cls._fingerprint(data.get('tools_hash'))} · input={cls._fingerprint(data.get('input_hash'))} · context={cls._fingerprint(data.get('context_manifest_hash'))}",
            f"inputs    system_chars={cls._number(data.get('system_chars'))} · task_chars={cls._number(data.get('input_chars'))} · context_pages={cls._number(data.get('context_pages'))}",
            f"tools     count={cls._number(data.get('tool_count', len(tool_names.split(', ')) if tool_names != 'none' else 0))} · allowlist={tool_names} · required={cls._setting(cls._first(data.get('require_tool_call'), data.get('required_tool')), default='false')} · multiple=allowed",
            f"output    schema={cls._setting(output_schema, default='none')} · strategy={strategy}",
            f"limits    model={limit('model_calls')} · tools={limit('tool_calls')} · turns={limit('turns')} · time={limit('seconds')}",
            f"context   pages={cls._number(data.get('context_pages'))} · window={cls._number(context_window)} ({context_source}) · max_output={cls._number(max_output)} ({output_source}) · safe_input={cls._number(safe_input)}",
            f"compact   enabled={cls._setting(compact_enabled)} · trigger={ratio_text} ({cls._number(compact_threshold)}) · keep={keep} messages · summary={summary}",
        )
        return cls._Text("\n".join(lines))

    def _context_usage_body(self, data: Mapping[str, Any]) -> Any:
        cls = self
        usage = cls._mapping(cls._first(data.get("usage"), data.get("provider_usage"), default={}))
        input_details = cls._mapping(
            cls._first(usage.get("input_token_details"), usage.get("prompt_tokens_details"), default={})
        )
        output_details = cls._mapping(
            cls._first(usage.get("output_token_details"), usage.get("completion_tokens_details"), default={})
        )
        input_tokens = cls._first(usage.get("input_tokens"), usage.get("prompt_tokens"))
        output_tokens = cls._first(usage.get("output_tokens"), usage.get("completion_tokens"))
        total_tokens = usage.get("total_tokens")
        cache_read = cls._first(
            input_details.get("cache_read"), input_details.get("cached_tokens"), usage.get("cached_tokens")
        )
        reasoning = cls._first(output_details.get("reasoning"), output_details.get("reasoning_tokens"))
        if total_tokens is None and isinstance(input_tokens, (int, float)) and isinstance(output_tokens, (int, float)):
            total_tokens = input_tokens + output_tokens

        turn = data.get("turn", "?")
        if input_tokens is None and output_tokens is None and total_tokens is None:
            reason = cls._first(usage.get("unavailable_reason"), data.get("unavailable_reason"))
            first_line = f"turn {turn} · tokens unavailable"
            if reason:
                first_line += f" ({_preview(str(reason), 72)})"
        else:
            first_line = f"turn {turn} · {cls._number(input_tokens)} in + {cls._number(output_tokens)} out = {cls._number(total_tokens)}"
            if cache_read is not None:
                first_line += f" · cache={cls._number(cache_read)}"
            if reasoning is not None:
                first_line += f" · reasoning={cls._number(reasoning)}"

        basis = cls._mapping(data.get("context_basis"))
        capacity = cls._mapping(data.get("capacity"))
        compact = cls._mapping(data.get("compact"))
        basis_tokens = cls._first(
            data.get("context_basis_tokens"),
            data.get("context_tokens"),
            basis.get("tokens"),
            basis.get("context_basis_tokens"),
        )
        window = cls._first(
            data.get("context_window_tokens"), capacity.get("context_window_tokens"), capacity.get("context_window")
        )
        threshold = cls._first(
            data.get("compact_threshold_tokens"),
            data.get("compact_threshold"),
            compact.get("threshold_tokens"),
            compact.get("threshold"),
        )
        ratio = data.get("compact_trigger_ratio")
        source = cls._first(data.get("basis_source"), basis.get("source"), default="")
        approximate = data.get("estimated") is True or "estimate" in str(source)
        marker = "~" if approximate else ""

        if basis_tokens is None:
            context_text = f"context unavailable/{cls._number(window)}" if window is not None else "context unknown"
        elif window is None:
            context_text = "context unknown"
        else:
            percent = float(basis_tokens) / float(window) * 100 if window else 0.0
            context_text = f"context {marker}{cls._number(basis_tokens)}/{cls._number(window)} tokens ({percent:.1f}%)"

        decision_value = data.get("decision")
        if isinstance(decision_value, Mapping):
            decision_value = cls._first(decision_value.get("status"), decision_value.get("compact_decision"))
        decision = str(decision_value or "").lower()
        labels = {"required": "REQUIRED", "run_ending": "run ending", "disabled": "disabled"}
        if basis_tokens is not None and threshold is not None:
            suffix = f" {labels[decision]}" if decision in labels else ""
            ratio_text = f" ({float(ratio) * 100:g}%)" if isinstance(ratio, (int, float)) else ""
            compact_text = f"compact@{cls._number(threshold)}{ratio_text}{suffix}"
        elif decision == "disabled":
            compact_text = "compact disabled"
        else:
            compact_text = "compact unavailable"
        return cls._Text(f"{first_line}\n{context_text} · {compact_text}")

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
        if event.kind == "compaction_summary":
            self._render_compaction_summary(data)
            return
        if event.kind in {"compaction_started", "compaction_completed", "compaction_failed"}:
            self._finish_compaction_summary()
        if event.kind == "model_text":
            self._ensure_model_output_boundary(data.get("turn"))
            self._render_assistant_text(data)
            return
        if event.kind in {"model_started", "model_completed"} and data.get("call_kind") == "compact":
            # Compact transport has its own lifecycle and streaming summary
            # panel; keep its model events in the event/audit stream without
            # adding a duplicate user-facing MODEL INPUT/OUTPUT block.
            return
        if event.kind == "model_failed" and Panel is not None:
            self._finish_assistant_text()
            self._ensure_model_output_boundary(data.get("turn"))
            body = Text()
            body.append(f"model_call_id: {data.get('model_call_id')}\n", style="dim")
            body.append("status: failed\n", style="bold red")
            body.append(_preview(json.dumps(_safe_json(data.get("error")), ensure_ascii=False, sort_keys=True), 4000), style="red")
            self.console.print(Panel(body, title="MODEL OUTPUT | FAILED", border_style="red", padding=(0, 1), expand=True))
            return
        if event.kind in {"model_started", "model_completed", "context_usage", "completed", "failed"}:
            self._finish_assistant_text()
        if event.kind == "run_started" and Panel is not None:
            body = self._run_started_body(event)
            self.console.print(Panel(body, title="AGENT RUN", border_style="blue", padding=(0, 1), expand=True))
            return
        if event.kind == "context_loaded":
            # Page inventory is an audit fact; CONTEXT panels are reserved for
            # per-turn token consumption and compact decisions.
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
        if event.kind == "context_usage" and Panel is not None:
            self.console.print(
                Panel(
                    self._context_usage_body(data),
                    title=f"CONTEXT | TURN {data.get('turn', '?')}",
                    border_style="magenta",
                    padding=(0, 1),
                    expand=True,
                )
            )
            return
        if event.kind == "compaction_started" and Panel is not None:
            self.console.print(Panel(Text(f"compaction_id: {data.get('compaction_id')}\nstatus: started"), title="COMPACTION | START", border_style="yellow", padding=(0, 1), expand=True))
            return
        if event.kind == "compaction_completed" and Panel is not None:
            self.console.print(Panel(Text(f"compaction_id: {data.get('compaction_id')}\nstatus: completed"), title="COMPACTION | COMPLETE", border_style="green", padding=(0, 1), expand=True))
            return
        if event.kind == "compaction_failed" and Panel is not None:
            self.console.print(Panel(Text(f"compaction_id: {data.get('compaction_id')}\nerror: {data.get('error')}"), title="COMPACTION | FAILED", border_style="red", padding=(0, 1), expand=True))
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
                body.append(_preview(json.dumps(structured_request.get("arguments", {}), ensure_ascii=False, sort_keys=True, indent=2), 4000))
                self.console.print(Panel(body, title="MODEL OUTPUT | STRUCTURED CALL", border_style="yellow", padding=(0, 1), expand=True))
            return
        if event.kind == "completed" and Panel is not None:
            body = Text()
            body.append("status: ", style="bold")
            body.append("SUCCESS\n", style="bold green")
            body.append(f"run_id: {event.run_id}\n", style="dim")
            body.append(f"model: {data.get('model')}\n\n", style="cyan")
            body.append("result:\n", style="bold")
            # The completion panel is the final operator-facing result view;
            # unlike streaming previews, it must retain the complete payload.
            body.append(str(data.get("output") if data.get("output") is not None else data.get("final_text", "")))
            self.console.print(
                Panel(
                    body,
                    title="[bold white on green] AGENT COMPLETE [/bold white on green]",
                    border_style="green",
                    padding=(1, 2),
                    expand=True,
                )
            )
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
        if event.kind == "structured_output":
            # The structured request is already visible in MODEL OUTPUT. The
            # validated result belongs only in the final AGENT COMPLETE panel.
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
                    tool_body.append(_preview(json.dumps(_safe_json(data.get("arguments")), ensure_ascii=False, sort_keys=True, indent=2), 4000))
                    title, border = "MODEL OUTPUT | TOOL CALL", "yellow"
                elif event.kind == "tool_completed":
                    tool_body = Text()
                    tool_body.append("kind: business\n", style="dim")
                    tool_body.append(f"name: {data.get('name')}\n", style="bold")
                    tool_body.append(f"tool_call_id: {data.get('tool_call_id')}\n", style="dim")
                    tool_body.append("status: completed\n", style="bold green")
                    tool_body.append(f"arguments: {_preview(json.dumps(_safe_json(data.get('arguments')), ensure_ascii=False, sort_keys=True, indent=2), 4000)}\n")
                    tool_body.append("result:\n", style="bold")
                    tool_body.append(_preview(json.dumps(_safe_json(data.get("result")), ensure_ascii=False, sort_keys=True, indent=2), 4000))
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

    def _compact_panel(self) -> Any:
        assert self._Panel is not None and self._Text is not None
        return self._Panel(self._Text(_preview(self._compact_text, 12000)), title="COMPACTION | SUMMARY", border_style="yellow", padding=(0, 1), expand=True)

    def _render_compaction_summary(self, data: Mapping[str, Any]) -> None:
        if self.console is None or self._Panel is None or self._Text is None:
            return
        compaction_id = data.get("compaction_id")
        if self._compact_id != compaction_id:
            self._finish_compaction_summary()
            self._compact_id = compaction_id
            self._compact_text = ""
        self._compact_text += str(data.get("delta", ""))
        if self._Live is None:
            self.console.print(self._compact_panel())
            return
        if self._compact_live is None:
            self._compact_live = self._Live(self._compact_panel(), console=self.console, refresh_per_second=10, transient=False)
            self._compact_live.start(refresh=True)
        else:
            self._compact_live.update(self._compact_panel(), refresh=True)

    def _finish_compaction_summary(self) -> None:
        if self._compact_live is not None:
            self._compact_live.update(self._compact_panel(), refresh=True)
            self._compact_live.stop()
            self._compact_live = None
            if self.console is not None:
                self.console.print()
        self._compact_id = None
        self._compact_text = ""

    def close(self) -> None:
        self._finish_assistant_text()
        self._finish_compaction_summary()
        if self.handler is not None:
            self.logger.removeHandler(self.handler)
            self.handler.close()


class _CallLedger:
    """Small run-scoped reservation ledger for primary and compact transports."""

    def __init__(self, limit: int | float | None):
        self.limit = int(limit) if limit is not None else None
        self.reserved = 0
        self.started = 0
        self.completed = 0
        self.cancelled = 0
        self._next = 0
        self.pending: list[str] = []
        self.by_call: dict[str, str] = {}

    def reserve(self, count: int) -> list[str]:
        if count <= 0:
            return []
        if self.limit is not None and self.reserved + count > self.limit:
            raise AgentError("limit_exceeded", "model_calls limit exceeded")
        reservations: list[str] = []
        for _ in range(count):
            self._next += 1
            reservation = f"model-reservation-{self._next}"
            reservations.append(reservation)
            self.pending.append(reservation)
        self.reserved += count
        return reservations

    def start(self, call_id: str, call_kind: str) -> str | None:
        reservation = self.pending.pop(0) if self.pending else None
        if reservation is not None:
            self.by_call[call_id] = reservation
        self.started += 1
        return reservation

    def complete(self, call_id: str | None) -> None:
        if call_id is not None:
            self.by_call.pop(call_id, None)
        self.completed += 1

    def cancel_pending(self) -> None:
        self.cancelled += len(self.pending)
        self.pending.clear()

    @property
    def used(self) -> int:
        return self.started


class _AgentGuardMiddleware(AgentMiddleware):
    """LangChain middleware executed between model and ToolNode."""

    def __init__(
        self,
        spec: AgentSpec,
        *,
        context_meter: _ContextMeter | None = None,
        compact_threshold: int | None = None,
        ledger: _CallLedger | None = None,
        deadline: float | None = None,
        reported_usage_enabled: Callable[[], bool] | None = None,
        counters: dict[str, int] | None = None,
    ):
        self.spec = spec
        self.context_meter = context_meter
        self.compact_threshold = compact_threshold
        self.ledger = ledger or _CallLedger((spec.limits or {}).get("model_calls"))
        self.deadline = deadline
        self.reported_usage_enabled = reported_usage_enabled
        self.counters = counters if counters is not None else {"model_calls": 0, "tool_calls": 0, "turns": 0}

    def _before_model(self, state: Mapping[str, Any]) -> None:
        limits = self.spec.limits or {}
        if self.deadline is not None and time.monotonic() >= self.deadline:
            raise AgentError("limit_exceeded", "seconds limit exceeded before model transport")
        if limits.get("turns") is not None and self.counters["turns"] >= limits["turns"]:
            raise AgentError("limit_exceeded", "turns limit exceeded")
        messages = list(state.get("messages", []) or [])
        basis = self.context_meter.count(messages)[0] if self.context_meter is not None else None
        reported = max(
            (
                _usage_number(getattr(message, "usage_metadata", None), "total_tokens") or 0
                for message in messages
                if isinstance(getattr(message, "usage_metadata", None), Mapping)
            ),
            default=0,
        ) if self.reported_usage_enabled is None or self.reported_usage_enabled() else 0
        needs_compact = self.compact_threshold is not None and max(basis or 0, reported) >= self.compact_threshold
        self.ledger.reserve(2 if needs_compact else 1)
        self.counters["turns"] += 1
        self.counters["model_calls"] = self.ledger.reserved

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


class _CompactTracker:
    """Run-scoped state shared by the official summarizer and its post-guard."""

    def __init__(self, meter: _ContextMeter, threshold: int):
        self.meter = meter
        self.threshold = threshold
        self.triggered = False
        self.before_keys: tuple[str, ...] = ()
        self.last_estimate: int | None = None
        self.reported_usage_enabled = True

    def token_counter(self, messages: Iterable[Any]) -> int:
        materialized = list(messages)
        estimate = self.meter.estimate(materialized) or 0
        reported = max(
            (
                _usage_number(getattr(message, "usage_metadata", None), "total_tokens") or 0
                for message in materialized
                if isinstance(getattr(message, "usage_metadata", None), Mapping)
            ),
            default=0,
        ) if self.reported_usage_enabled else 0
        if max(estimate, reported) >= self.threshold and not self.triggered:
            self.triggered = True
            self.before_keys = tuple(_message_key(message) for message in materialized)
        self.last_estimate = estimate
        return estimate

    def reset(self) -> None:
        self.triggered = False
        self.before_keys = ()
        self.last_estimate = None
        self.reported_usage_enabled = False

    def primary_completed(self) -> None:
        self.reported_usage_enabled = True


class _CompactPostGuardMiddleware(AgentMiddleware):
    """Fail closed after official summarization if state did not progress."""

    def __init__(
        self,
        tracker: _CompactTracker,
        on_success: Callable[[int | None], None] | None = None,
        on_failure: Callable[[AgentError], None] | None = None,
    ):
        self.tracker = tracker
        self.on_success = on_success
        self.on_failure = on_failure

    def _check(self, state: Mapping[str, Any]) -> None:
        if not self.tracker.triggered:
            return
        messages = list(state.get("messages", []) or [])
        keys = tuple(_message_key(message) for message in messages)
        estimate = self.tracker.meter.estimate(messages)
        error: AgentError | None = None
        if keys == self.tracker.before_keys:
            error = AgentError("context_budget_exceeded", "compact reached its trigger but middleware produced no state replacement")
        elif any(_message_text(message).startswith("Error generating summary:") for message in messages):
            error = AgentError("compact_error", "official summarization returned an error message instead of a summary")
        elif estimate is None or estimate >= self.tracker.threshold:
            error = AgentError("context_budget_exceeded", "compact did not reduce the visible context below its trigger")
        if error is not None:
            self.tracker.reset()
            if self.on_failure is not None:
                self.on_failure(error)
            raise error
        self.tracker.reset()
        if self.on_success is not None:
            self.on_success(estimate)

    def before_model(self, state: Mapping[str, Any], runtime: Any) -> None:
        self._check(state)

    async def abefore_model(self, state: Mapping[str, Any], runtime: Any) -> None:
        self._check(state)


class _ModelOptionsMiddleware(AgentMiddleware):
    """Apply per-inference model settings without changing profile identity."""

    def __init__(
        self,
        options: Mapping[str, Any] | None,
        *,
        forced_tool_choice: Any | None = None,
        tool_choice_resolver: Callable[[], Any | None] | None = None,
    ):
        self.options = dict(options or {})
        self.forced_tool_choice = forced_tool_choice
        self.tool_choice_resolver = tool_choice_resolver

    def _tool_choice(self) -> Any | None:
        if self.forced_tool_choice is not None:
            return self.forced_tool_choice
        if self.tool_choice_resolver is None:
            return None
        return self.tool_choice_resolver()

    @staticmethod
    def _request_tool_name(tool: Any) -> str:
        if isinstance(tool, Mapping):
            function = tool.get("function")
            function = function if isinstance(function, Mapping) else {}
            name = tool.get("name") or function.get("name")
            return str(name or "")
        return _tool_name(tool)

    def wrap_model_call(self, request: Any, handler: Callable[[Any], Any]) -> Any:
        settings = {**(request.model_settings or {}), **self.options}
        overrides: dict[str, Any] = {"model_settings": settings}
        tool_choice = self._tool_choice()
        if tool_choice is not None:
            overrides["tool_choice"] = tool_choice
            if self.forced_tool_choice is None and self.tool_choice_resolver is not None:
                # LangChain ToolStrategy otherwise replaces a requested business
                # tool with ``tool_choice=any`` whenever a structured-output tool
                # is present. Temporarily suppress that terminal surface while a
                # caller-declared mandatory business step is active.
                overrides["response_format"] = None
                overrides["tools"] = [
                    tool
                    for tool in list(getattr(request, "tools", None) or [])
                    if self._request_tool_name(tool) == tool_choice
                ]
        return handler(request.override(**overrides))

    async def awrap_model_call(self, request: Any, handler: Callable[[Any], Any]) -> Any:
        settings = {**(request.model_settings or {}), **self.options}
        overrides: dict[str, Any] = {"model_settings": settings}
        tool_choice = self._tool_choice()
        if tool_choice is not None:
            overrides["tool_choice"] = tool_choice
            if self.forced_tool_choice is None and self.tool_choice_resolver is not None:
                overrides["response_format"] = None
                overrides["tools"] = [
                    tool
                    for tool in list(getattr(request, "tools", None) or [])
                    if self._request_tool_name(tool) == tool_choice
                ]
        return await handler(request.override(**overrides))


def _request_projection(request: Any) -> dict[str, Any]:
    """Build the public ModelRequest view used for rendered-input auditing."""

    response_format = getattr(request, "response_format", None)
    if isinstance(response_format, type) and hasattr(response_format, "model_json_schema"):
        response_format = response_format.model_json_schema()
    elif hasattr(response_format, "__dict__"):
        response_format = _safe_json(vars(response_format))
    tools = []
    for tool in list(getattr(request, "tools", None) or []):
        if isinstance(tool, Mapping):
            function = tool.get("function")
            function = function if isinstance(function, Mapping) else {}
            tools.append(
                {
                    "name": str(tool.get("name") or function.get("name") or ""),
                    "description": str(
                        tool.get("description") or function.get("description") or ""
                    ),
                    "schema": _safe_json(
                        tool.get("parameters") or function.get("parameters") or {}
                    ),
                }
            )
        else:
            tools.append({"name": _tool_name(tool), "description": _tool_description(tool), "schema": _tool_schema(tool)})
    system_message = getattr(request, "system_message", None)
    return {
        "system": _message_text(system_message) if system_message is not None else None,
        "messages": [_message_text(message) for message in list(getattr(request, "messages", None) or [])],
        "tools": tools,
        "tool_choice": _safe_json(getattr(request, "tool_choice", None)),
        "response_format": _safe_json(response_format),
        "model_settings": _safe_json(dict(getattr(request, "model_settings", None) or {})),
    }


def _tool_completion_status(
    result: Any,
) -> tuple[str, dict[str, Any] | None, bool]:
    """Translate an explicit no-execution tool result into audit semantics."""

    if not isinstance(result, Mapping):
        return "completed", None, True
    execution_status = result.get("execution_status")
    if execution_status not in {
        "mandatory_tool_rejected",
        "prerequisite_required",
    }:
        return "completed", None, True
    raw_error = result.get("error")
    if isinstance(raw_error, Mapping):
        error = {
            "code": str(raw_error.get("code") or execution_status),
            "message": str(
                raw_error.get("message") or "registered tool was not executed"
            ),
        }
    else:
        error = {
            "code": str(execution_status),
            "message": str(
                result.get("message") or "registered tool was not executed"
            ),
        }
    return "rejected", error, False


class _RequestCaptureMiddleware(AgentMiddleware):
    """Capture the effective public ModelRequest after model options are applied."""

    def __init__(self, captures: list[dict[str, Any]]):
        self.captures = captures

    def _capture(self, request: Any) -> None:
        projection = _request_projection(request)
        self.captures.append(
            {
                "projection": projection,
                "rendered_input_hash": _hash_text(json.dumps(projection, ensure_ascii=False, sort_keys=True, separators=(",", ":"))),
                "captured_at_utc": datetime.now(timezone.utc).isoformat(),
            }
        )

    def wrap_model_call(self, request: Any, handler: Callable[[Any], Any]) -> Any:
        self._capture(request)
        return handler(request)

    async def awrap_model_call(self, request: Any, handler: Callable[[Any], Any]) -> Any:
        self._capture(request)
        return await handler(request)


class _RunModelObserver(BaseCallbackHandler):
    """Public callback boundary for streamed model text and terminal usage."""

    def __init__(self, on_start: Callable[[str, Mapping[str, Any]], None], on_token: Callable[[str, str, Any, Mapping[str, Any]], None], on_end: Callable[[str, Any, Mapping[str, Any]], None], on_error: Callable[[str, BaseException, Mapping[str, Any]], None]):
        self._on_start = on_start
        self._on_token = on_token
        self._on_end = on_end
        self._on_error = on_error

    def on_chat_model_start(self, serialized: Mapping[str, Any], messages: list[Any], *, run_id: Any, parent_run_id: Any = None, tags: list[str] | None = None, metadata: Mapping[str, Any] | None = None, **kwargs: Any) -> None:
        self._on_start(str(run_id), dict(metadata or {}))

    def on_llm_start(self, serialized: Mapping[str, Any], prompts: list[str], *, run_id: Any, parent_run_id: Any = None, tags: list[str] | None = None, metadata: Mapping[str, Any] | None = None, **kwargs: Any) -> None:
        self._on_start(str(run_id), dict(metadata or {}))

    def on_llm_new_token(self, token: str, *, chunk: Any = None, run_id: Any, parent_run_id: Any = None, tags: list[str] | None = None, **kwargs: Any) -> None:
        if token:
            self._on_token(str(run_id), str(token), chunk, {})

    def on_llm_end(self, response: Any, *, run_id: Any, parent_run_id: Any = None, tags: list[str] | None = None, **kwargs: Any) -> None:
        self._on_end(str(run_id), response, {})

    def on_llm_error(self, error: BaseException, *, run_id: Any, parent_run_id: Any = None, tags: list[str] | None = None, **kwargs: Any) -> None:
        self._on_error(str(run_id), error, {})

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

    async def _agenerate(
        self,
        messages: list[Any],
        stop: list[str] | None = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> Any:
        chunks: list[Any] = []
        async for chunk in self._inner.astream(messages, **kwargs):
            chunks.append(chunk)
            if run_manager is not None:
                token = _message_text(chunk)
                if token:
                    callback = getattr(run_manager, "on_llm_new_token", None)
                    if callback is not None:
                        callback_result = callback(token, chunk=chunk)
                        if inspect.isawaitable(callback_result):
                            await callback_result
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
        run_manager = kwargs.pop("run_manager", None)
        return asyncio.run(self._agenerate(messages, stop=stop, run_manager=run_manager, **kwargs))


class AgentApp:
    def __init__(self, spec: AgentSpec, config: LLMConfig, model: Any, *, real_llm: bool = True, profile: str = "direct"):
        self.spec = spec
        self.config = config
        self.model = model
        self.real_llm = real_llm
        self.profile = profile
        self.adapter_name = (
            "langchain-deepseek/chat-completions"
            if type(model).__module__.split(".", 1)[0] == "langchain_deepseek"
            else ("test/model" if not real_llm else "langchain-openai/chat-completions")
        )

    @classmethod
    def from_registry(cls, spec: AgentSpec, registry: LLMRegistry, profile: str | None = None, *, model_options: Mapping[str, Any] | None = None) -> "AgentApp":
        name = registry.default_name if profile is None else profile
        return cls.from_config(spec, registry.require(name), model_options=model_options, profile=name)

    @classmethod
    def from_config(cls, spec: AgentSpec, config: LLMConfig, *, model_options: Mapping[str, Any] | None = None, profile: str = "direct") -> "AgentApp":
        _validate_model_options(model_options)
        if config.api_key is None:
            raise AgentError("config_error", "api_key is required for a real model run")
        deepseek = _is_deepseek_config(config)
        try:
            if deepseek:
                from langchain_deepseek import ChatDeepSeek as ChatModel
            else:
                from langchain_openai import ChatOpenAI as ChatModel
        except ImportError as exc:  # pragma: no cover
            package = "langchain-deepseek" if deepseek else "langchain-openai"
            raise AgentError("config_error", f"{package} is required") from exc
        kwargs = config.connection_kwargs()
        if config.max_output_tokens is not None:
            kwargs["max_tokens" if deepseek else "max_completion_tokens"] = config.max_output_tokens
        kwargs["use_responses_api"] = False
        kwargs.update({"streaming": True, "stream_usage": True, "max_retries": 0})
        kwargs.update(dict(model_options or {}))
        try:
            model = ChatModel(**kwargs)
        except Exception as exc:
            raise AgentError("config_error", "model construction failed", details=_exception_details(exc)) from exc
        return cls(spec, config, model, profile=profile)

    @classmethod
    def _for_test(cls, spec: AgentSpec, config: LLMConfig, model: Any) -> "AgentApp":
        if not isinstance(model, BaseChatModel) and hasattr(model, "astream"):
            model = _LegacyModelAdapter(model)
        return cls(spec, config, model, real_llm=False, profile="test")

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
        compact_trigger_ratio: float | None = _DEFAULT_COMPACT_TRIGGER_RATIO,
        on_event: Callable[[AgentEvent], None] | None = None,
        audit_out: Path | None = None,
        result_out: Path | None = None,
        model_call_options: Mapping[str, Any] | None = None,
        tool_choice_resolver: Callable[[], Any | None] | None = None,
        tool_choice_policy_name: str | None = None,
    ) -> AgentRunResult:
        if (tool_choice_resolver is None) != (tool_choice_policy_name is None):
            raise ValueError(
                "tool_choice_resolver and tool_choice_policy_name must be supplied together"
            )
        if tool_choice_resolver is not None and not callable(tool_choice_resolver):
            raise ValueError("tool_choice_resolver must be callable")
        if tool_choice_policy_name is not None and not tool_choice_policy_name.strip():
            raise ValueError("tool_choice_policy_name must be non-empty")
        _validate_model_call_options(model_call_options)
        compact_trigger_ratio = _validate_compact_trigger_ratio(compact_trigger_ratio)
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
            "stream_usage": getattr(self.model, "stream_usage", None),
            "max_retries": getattr(self.model, "max_retries", None),
            "timeout": getattr(self.model, "request_timeout", None) or getattr(self.model, "timeout", None),
            "tool_choice_policy": tool_choice_policy_name,
        }
        max_output_override = None
        if model_call_options:
            max_tokens_value = model_call_options.get("max_tokens")
            max_completion_value = model_call_options.get("max_completion_tokens")
            if max_tokens_value is not None and max_completion_value is not None and max_tokens_value != max_completion_value:
                raise AgentError("config_error", "max_tokens and max_completion_tokens cannot disagree")
            max_output_override = max_tokens_value if max_tokens_value is not None else max_completion_value
        context_window_tokens, max_output_tokens, safe_input_tokens, capacity_source = _model_capacity(
            self.model,
            self.config,
            max_output_override=max_output_override if isinstance(max_output_override, int) else None,
        )
        compact_threshold = (
            math.floor(context_window_tokens * compact_trigger_ratio)
            if context_window_tokens is not None and compact_trigger_ratio is not None
            else None
        )
        context_error: AgentError | None = None
        try:
            pages = _normalize_context(context)
        except ValueError as exc:
            # Keep preflight failures on the same observable run path as
            # provider/tool failures: callers receive an event and an audit
            # finish record before the structured error is raised.
            pages = []
            context_error = AgentError("context_invalid", str(exc))
        run_id = uuid.uuid4().hex
        manifest = _build_context_manifest(pages) if pages else None
        endpoint_fingerprint = _endpoint_fingerprint(_effective_model_base_url(self.model, self.config))
        behavior_fingerprint = _behavior_fingerprint(
            {
                "profile": self.profile,
                "model": self.config.model,
                "adapter": self.adapter_name,
                "endpoint_fingerprint": endpoint_fingerprint,
                "capacity": {"context_window_tokens": context_window_tokens, "max_output_tokens": max_output_tokens, "safe_input_tokens": safe_input_tokens, "capacity_source": capacity_source},
                "inference": inference_options,
                "limits": dict(self.spec.limits or {}),
                "tools_hash": _behavior_fingerprint({"tools": [_tool_schema(tool) for tool in self.spec.tools]}),
                "output_schema_hash": _behavior_fingerprint(self.spec.output_schema.model_json_schema()) if self.spec.output_schema else None,
                "system_prompt_hash": _hash_text(self.spec.system_prompt),
                "input_hash": _hash_text(input_text),
                "context_manifest_hash": manifest,
                "compact": {"ratio": compact_trigger_ratio, "threshold": compact_threshold},
                "tool_choice_policy": tool_choice_policy_name,
            }
        )
        canonical_audit_out, canonical_result_out = _validate_output_paths(Path(audit_out) if audit_out is not None else None, Path(result_out) if result_out is not None else None)
        renderer_obj = _Renderer(renderer, log_level, run_id)
        audit = _AuditWriter(canonical_audit_out, run_id, result_path=canonical_result_out)
        started = time.monotonic()
        started_at_utc = datetime.now(timezone.utc)
        ended_at_utc: datetime | None = None
        duration_seconds: float | None = None
        seq = 0
        attempt_id = "attempt-1"
        turn = 0
        status = "failed"
        output: Any = None
        final_text = ""
        usage: list[dict[str, Any]] = []
        observed_model: str | None = None
        error: dict[str, Any] | None = None
        tool_calls: list[dict[str, Any]] = []
        pending_tool_ids: dict[str, list[str]] = {}
        active_tool_records: dict[str, dict[str, Any]] = {}
        failed_tool_call_ids: set[str] = set()
        shown_message_keys: set[str] = set()
        system_shown = False
        streamed_turns: set[int] = set()
        audit_ok = audit.enabled
        business_tool_called = False
        tool_error_seen = False
        heartbeat_task: asyncio.Task[None] | None = None
        context_meter = _ContextMeter(tools=self.spec.tools, system_prompt=self.spec.system_prompt, output_schema=self.spec.output_schema)
        compact_count = 0
        last_compaction_id: str | None = None
        compact_tracker = _CompactTracker(context_meter, compact_threshold) if compact_threshold is not None else None
        compaction_summary_info: dict[str, dict[str, Any]] = {}
        compaction_source_refs: dict[str, list[dict[str, Any]]] = {}
        compaction_failure_errors: dict[str, AgentError] = {}
        stream_holdbacks: dict[str, _StreamHoldback] = {}
        sensitive_values = _sensitive_inventory(self.config, pages)
        audit.set_sensitive_values(sensitive_values)
        model_call_started: dict[str, datetime] = {}
        model_call_kinds: dict[str, str] = {}
        context_events_seen: set[int] = set()
        current_model_call_id: str | None = None
        current_rendered_input_hash: str | None = None
        current_input_messages_snapshot: list[Any] = []
        last_state_messages_snapshot: list[Any] = []
        failure_context_emitter: Callable[[], None] | None = None
        partial_texts: dict[str, str] = {}
        transport_errors: dict[str, dict[str, Any]] = {}
        decision_written_turns: set[int] = set()
        callback_usage_ids: set[str] = set()
        callback_summary_ids: set[str] = set()
        pending_model_inputs: dict[int, tuple[str, list[Any], str | None]] = {}
        request_captures: list[dict[str, Any]] = []
        request_capture_by_call: dict[str, dict[str, Any]] = {}
        message_source_refs: dict[str, tuple[int, str]] = {}
        message_source_by_id: dict[str, tuple[int, str]] = {}
        source_state: dict[str, tuple[int, str] | None] = {
            "latest_decision": None,
            "latest_action": None,
            "latest_compact": None,
        }
        initial_context_seq: int | None = None
        started_turns: set[int] = set()
        compaction_announced_turns: set[int] = set()
        compaction_failure_ids: set[str] = set()
        ledger = _CallLedger((self.spec.limits or {}).get("model_calls"))
        ledger_started_ids: set[str] = set()
        ledger_completed_ids: set[str] = set()
        primary_ledger_calls: dict[int, str] = {}

        def ledger_start(call_id: str, call_kind: str) -> str | None:
            if call_id in ledger_started_ids:
                return ledger.by_call.get(call_id)
            reservation = ledger.start(call_id, call_kind)
            ledger_started_ids.add(call_id)
            return reservation

        def ledger_complete(call_id: str) -> None:
            if call_id not in ledger_started_ids or call_id in ledger_completed_ids:
                return
            ledger.complete(call_id)
            ledger_completed_ids.add(call_id)

        def emit(kind: str, data: Mapping[str, Any]) -> None:
            nonlocal seq
            seq += 1
            event = AgentEvent(
                run_id,
                seq,
                datetime.now(timezone.utc),
                kind,
                _redact_with_inventory(_safe_json(dict(data)), sensitive_values),
            )
            if kind == "context_usage" and isinstance(data.get("turn"), int):
                context_events_seen.add(int(data["turn"]))
            renderer_obj.render(event)
            if on_event is not None:
                on_event(event)

        def audit_write(record: Mapping[str, Any], *, turn_value: int | None = None) -> int | None:
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
                return audit.order if audit.enabled else None
            except Exception as exc:
                audit_ok = False
                raise AgentError("audit_write_failed", "audit output failed") from exc

        def message_ref(message: Any) -> dict[str, Any]:
            source = message_source_refs.get(_message_key(message))
            identity = getattr(message, "id", None)
            if source is None and identity:
                source = message_source_by_id.get(str(identity))
            source_seq = source[0] if source else None
            source_record = source[1] if source else None
            if source_seq is None and (getattr(message, "type", None) in {"human", "user"}):
                source_seq = initial_context_seq
                source_record = "context" if source_seq is not None else None
            if source_seq is None:
                role = getattr(message, "type", None)
                if role == "ai":
                    source = source_state.get("latest_decision")
                elif role == "tool":
                    tool_call_id = getattr(message, "tool_call_id", None)
                    source = message_source_by_id.get(str(tool_call_id)) if tool_call_id else None
                    source = source or source_state.get("latest_action")
                else:
                    source = source_state.get("latest_compact") or source_state.get("latest_decision") or source_state.get("latest_action")
                source_seq = source[0] if source else None
                source_record = source[1] if source else None
            return _message_ref(message, source_seq=source_seq, source_record=source_record)

        async def heartbeat() -> None:
            while True:
                await asyncio.sleep(1)
                emit("heartbeat", {"elapsed_seconds": time.monotonic() - started, "attempt_id": attempt_id})

        def compaction_validated(post_estimate: int | None) -> None:
            if last_compaction_id is None:
                return
            failure = compaction_failure_errors.get(last_compaction_id)
            if failure is not None:
                # A failed summary must never be treated as a successful state
                # replacement, even if the middleware returns an error-shaped
                # message to the graph.
                raise AgentError(failure.code, failure.message, details=failure.details)
            info = compaction_summary_info.get(last_compaction_id, {})
            emit(
                "compaction_completed",
                {
                    "compaction_id": last_compaction_id,
                    "model_call_id": info.get("model_call_id"),
                    "summary_hash": info.get("summary_hash"),
                    "source_refs": compaction_source_refs.get(last_compaction_id, []),
                    "post_basis": post_estimate,
                    "status": "completed",
                },
            )
            audit_write(
                {
                    "record": "context",
                    "record_type": "context",
                    "operation": "compact",
                    "compaction_id": last_compaction_id,
                    "model_call_id": info.get("model_call_id"),
                    "summary": info.get("summary"),
                    "summary_hash": info.get("summary_hash"),
                    "source_refs": compaction_source_refs.get(last_compaction_id, []),
                    "post_basis": post_estimate,
                    "usage": info.get("usage"),
                    "status": "completed",
                }
            )

        def compaction_failed(exc: AgentError) -> None:
            if last_compaction_id is None:
                return
            if last_compaction_id in compaction_failure_ids:
                return
            compaction_failure_ids.add(last_compaction_id)
            compaction_failure_errors[last_compaction_id] = exc
            emit(
                "compaction_failed",
                {
                    "compaction_id": last_compaction_id,
                    "source_refs": compaction_source_refs.get(last_compaction_id, []),
                    "error": {"code": exc.code, "message": exc.message},
                    "status": "failed",
                },
            )
            audit_write(
                {
                    "record": "context",
                    "record_type": "context",
                    "operation": "compact",
                    "compaction_id": last_compaction_id,
                    "summary": compaction_summary_info.get(last_compaction_id, {}).get("summary"),
                    "partial_summary": compaction_summary_info.get(last_compaction_id, {}).get("partial_summary"),
                    "summary_hash": compaction_summary_info.get(last_compaction_id, {}).get("summary_hash"),
                    "source_refs": compaction_source_refs.get(last_compaction_id, []),
                    "error": {"code": exc.code, "message": exc.message},
                    "status": "failed",
                }
            )

        def record_transport_usage(
            raw_usage: Mapping[str, Any] | None,
            call_id: str | None,
            call_kind: str,
            call_turn: int,
            *,
            status: str = "completed",
            observed_usages: Sequence[Mapping[str, Any]] | None = None,
            usage_conflict: bool = False,
            response_id: str | None = None,
        ) -> None:
            item = _normalize_usage(
                raw_usage,
                model=self.config.model,
                call_kind=call_kind,
                turn=call_turn,
                status=status,
                observed_usages=observed_usages,
                usage_conflict=usage_conflict,
                response_id=response_id,
            )
            item["model_call_id"] = call_id
            started_at = model_call_started.get(call_id or "")
            if started_at is not None:
                item["started_at_utc"] = started_at.isoformat()
                item["duration_seconds"] = max(0.0, (datetime.now(timezone.utc) - started_at).total_seconds())
            usage.append(item)
            if raw_usage or observed_usages:
                context_meter.record(raw_usage, call_kind=call_kind, observed_usages=observed_usages)

        def callback_start(call_id: str, metadata: Mapping[str, Any]) -> None:
            nonlocal compact_count, last_compaction_id, current_model_call_id, current_rendered_input_hash
            model_call_started.setdefault(call_id, datetime.now(timezone.utc))
            call_kind = "compact" if metadata.get("lc_source") == "summarization" else "primary"
            reservation_id = None
            if call_kind == "compact" or turn not in primary_ledger_calls:
                reservation_id = ledger_start(call_id, call_kind)
            if request_captures:
                capture = request_captures.pop(0)
                capture["model_call_id"] = call_id
                capture["reservation_id"] = reservation_id
                request_capture_by_call[call_id] = capture
                current_rendered_input_hash = capture.get("rendered_input_hash")
            if metadata.get("lc_source") == "summarization":
                if turn not in compaction_announced_turns:
                    compact_count += 1
                    last_compaction_id = f"compact-{compact_count}"
                callback_summary_ids.add(call_id)
                model_call_kinds[call_id] = "compact"
                compaction_source_refs.setdefault(last_compaction_id or "", [message_ref(message) for message in last_state_messages_snapshot])
                if turn not in compaction_announced_turns:
                    compaction_announced_turns.add(turn)
                    emit("compaction_started", {"compaction_id": last_compaction_id, "after_turn": turn, "threshold": compact_threshold, "source_refs": compaction_source_refs.get(last_compaction_id or "", [])})
                emit(
                    "model_started",
                    {
                        "attempt_id": attempt_id,
                        "turn": turn,
                        "model_call_id": call_id,
                        "call_kind": "compact",
                        "prompt": "[official compact] summarize the prior agent context",
                        "input_message_refs": [message_ref(message) for message in last_state_messages_snapshot],
                    },
                )
            else:
                model_call_kinds.setdefault(call_id, "primary")
                # Publish MODEL INPUT even when the provider fails before its
                # first token; otherwise the audit would lose the failed
                # transport's causal input reference.
                current_model_call_id = call_id
                ensure_primary_started(call_id)

        def consume_request_capture(call_id: str | None) -> dict[str, Any]:
            """Bind a middleware capture even when provider callbacks start first."""

            key = call_id or ""
            capture = request_capture_by_call.get(key)
            if capture is None and request_captures:
                capture = request_captures.pop(0)
                capture["model_call_id"] = call_id
                request_capture_by_call[key] = capture
            return capture or {}

        def ensure_primary_started(call_id: str) -> None:
            nonlocal current_model_call_id, current_rendered_input_hash
            if turn in started_turns:
                return
            current_model_call_id = call_id
            model_call_kinds[call_id] = "primary"
            prompt, input_messages, rendered_hash = pending_model_inputs.get(turn, ("", [], None))
            capture = request_capture_by_call.get(call_id)
            current_rendered_input_hash = (capture or {}).get("rendered_input_hash") or rendered_hash
            started_turns.add(turn)
            emit("model_started", {"attempt_id": attempt_id, "turn": turn, "model_call_id": call_id, "call_kind": "primary", "prompt": prompt, "input_message_refs": [message_ref(item) for item in input_messages]})

        def callback_token(call_id: str, token: str, chunk: Any, metadata: Mapping[str, Any]) -> None:
            holdback = stream_holdbacks.setdefault(call_id, _StreamHoldback(sensitive_values))
            safe_token = holdback.feed(token)
            if not safe_token:
                return
            partial_texts[call_id] = partial_texts.get(call_id, "") + safe_token
            if call_id in callback_summary_ids or model_call_kinds.get(call_id) == "compact":
                emit("compaction_summary", {"compaction_id": last_compaction_id, "model_call_id": call_id, "delta": safe_token})
            else:
                ensure_primary_started(call_id)
                streamed_turns.add(turn)
                emit("model_text", {"attempt_id": attempt_id, "turn": turn, "model_call_id": call_id, "call_kind": "primary", "text": safe_token})

        def callback_end(call_id: str, response: Any, metadata: Mapping[str, Any]) -> None:
            nonlocal observed_model
            if call_id in callback_usage_ids:
                return
            callback_usage_ids.add(call_id)
            ledger_complete(call_id)
            holdback = stream_holdbacks.get(call_id)
            if holdback is not None:
                safe_tail = holdback.feed("", final=True)
                if safe_tail:
                    partial_texts[call_id] = partial_texts.get(call_id, "") + safe_tail
                    if model_call_kinds.get(call_id) == "compact" or call_id in callback_summary_ids:
                        emit("compaction_summary", {"compaction_id": last_compaction_id, "model_call_id": call_id, "delta": safe_tail})
                    else:
                        ensure_primary_started(call_id)
                        streamed_turns.add(turn)
                        emit("model_text", {"attempt_id": attempt_id, "turn": turn, "model_call_id": call_id, "call_kind": "primary", "text": safe_tail})
            raw_usage, observed_usages, usage_conflict, model_name = _model_usage_info(response)
            call_kind = model_call_kinds.get(call_id, "primary")
            if call_kind == "primary":
                ensure_primary_started(call_id)
            response_id = next(
                (
                    getattr(message, "response_metadata", {}).get("id")
                    or getattr(message, "response_metadata", {}).get("response_id")
                    for message in _model_output_messages(response)
                    if isinstance(getattr(message, "response_metadata", {}), Mapping)
                ),
                None,
            )
            record_transport_usage(
                raw_usage,
                call_id,
                call_kind,
                turn,
                observed_usages=observed_usages,
                usage_conflict=usage_conflict,
                response_id=response_id if isinstance(response_id, str) else None,
            )
            if call_kind == "primary" and compact_tracker is not None:
                compact_tracker.primary_completed()
            if call_kind == "compact":
                summary_messages = _model_output_messages(response)
                summary_text = next(
                    (_message_text(message) for message in summary_messages if _message_text(message)),
                    partial_texts.get(call_id, ""),
                )
                summary_hash = _hash_text(summary_text)
                compaction_summary_info[last_compaction_id or ""] = {
                    "model_call_id": call_id,
                    "summary": summary_text,
                    "summary_hash": summary_hash,
                    "usage": usage[-1] if usage else None,
                }
                emit(
                    "model_completed",
                    {
                        "attempt_id": attempt_id,
                        "turn": turn,
                        "model_call_id": call_id,
                        "call_kind": "compact",
                        "tool_count": 0,
                        "output": summary_text,
                    },
                )
            if isinstance(model_name, str):
                observed_model = observed_model or model_name

        def callback_error(call_id: str, exc: BaseException, metadata: Mapping[str, Any]) -> None:
            ledger_complete(call_id)
            ledger.cancelled += 1
            holdback = stream_holdbacks.get(call_id)
            if holdback is not None:
                safe_tail = holdback.feed("", final=True)
                if safe_tail:
                    partial_texts[call_id] = partial_texts.get(call_id, "") + safe_tail
                    if model_call_kinds.get(call_id) == "compact" or call_id in callback_summary_ids:
                        emit("compaction_summary", {"compaction_id": last_compaction_id, "model_call_id": call_id, "delta": safe_tail})
                    else:
                        ensure_primary_started(call_id)
                        emit("model_text", {"attempt_id": attempt_id, "turn": turn, "model_call_id": call_id, "call_kind": "primary", "text": safe_tail})
            transport_errors[call_id] = _exception_details(exc)
            call_kind = model_call_kinds.get(call_id, "primary")
            if not any(item.get("model_call_id") == call_id for item in usage):
                record_transport_usage(None, call_id, call_kind, turn, status="failed")
            if call_kind == "compact":
                info = compaction_summary_info.setdefault(last_compaction_id or "", {})
                info["partial_summary"] = partial_texts.get(call_id, "")
                compaction_failed(AgentError("compact_error", "summary model transport failed"))
            emit("model_failed", {"model_call_id": call_id, "call_kind": model_call_kinds.get(call_id, "primary"), "turn": turn, "error": transport_errors[call_id]})

        def redaction_report() -> list[dict[str, Any]]:
            return [
                holder.report("summary" if call_id in callback_summary_ids else "primary")
                for call_id, holder in stream_holdbacks.items()
                if holder.redaction_hits or holder.withheld_chars
            ]

        observer = _RunModelObserver(callback_start, callback_token, callback_end, callback_error)

        async def consume(
            graph: Any,
            initial_messages: Sequence[Any] | None = None,
        ) -> dict[str, Any] | None:
            nonlocal turn, final_text, output, observed_model, business_tool_called, system_shown, tool_error_seen, compact_count, last_compaction_id, current_model_call_id, current_rendered_input_hash, current_input_messages_snapshot, last_state_messages_snapshot, failure_context_emitter
            messages: list[Any] = (
                list(initial_messages)
                if initial_messages is not None
                else [{"role": "user", "content": _input_with_context(input_text, pages)}]
            )
            last_state_messages: list[Any] = list(messages)
            current_input_messages: list[Any] = list(messages)
            last_state_messages_snapshot = list(last_state_messages)
            context_emitted_turns: set[int] = set()

            def record_model_usage(
                raw_usage: Mapping[str, Any] | None,
                call_id: str | None,
                call_kind: str,
                call_turn: int,
                *,
                status: str = "completed",
                observed_usages: Sequence[Mapping[str, Any]] | None = None,
                usage_conflict: bool = False,
                response_id: str | None = None,
            ) -> None:
                item = _normalize_usage(
                    raw_usage,
                    model=self.config.model,
                    call_kind=call_kind,
                    turn=call_turn,
                    status=status,
                    observed_usages=observed_usages,
                    usage_conflict=usage_conflict,
                    response_id=response_id,
                )
                item["model_call_id"] = call_id
                started_at = model_call_started.get(call_id or "")
                if started_at is not None:
                    item["started_at_utc"] = started_at.isoformat()
                    item["duration_seconds"] = max(0.0, (datetime.now(timezone.utc) - started_at).total_seconds())
                usage.append(item)
                if raw_usage or observed_usages:
                    context_meter.record(raw_usage, call_kind=call_kind, observed_usages=observed_usages)

            def emit_context_usage(context_turn: int, state_messages: Iterable[Any], *, run_ending: bool = False) -> None:
                if context_turn in context_emitted_turns:
                    return
                context_emitted_turns.add(context_turn)
                estimated, sources = context_meter.count(state_messages)
                latest = usage[-1] if usage and usage[-1].get("turn") == context_turn and usage[-1].get("call_kind") == "primary" else None
                input_tokens = latest.get("input_tokens") if latest else None
                output_tokens = latest.get("output_tokens") if latest else None
                total_tokens = latest.get("total_tokens") if latest else None
                cache_read = (latest or {}).get("input_token_details", {}).get("cache_read")
                reasoning = (latest or {}).get("output_token_details", {}).get("reasoning")
                if total_tokens is None:
                    first = f"turn {context_turn} · tokens unavailable (provider usage unavailable)"
                else:
                    first = f"turn {context_turn} · {input_tokens:,} in" if isinstance(input_tokens, (int, float)) else f"turn {context_turn} · ? in"
                    if cache_read is not None:
                        first += f" · cache={cache_read:,}" if isinstance(cache_read, (int, float)) else f" · cache={cache_read}"
                    first += f" + {output_tokens:,} out" if isinstance(output_tokens, (int, float)) else " + ? out"
                    if reasoning is not None:
                        first += f" · reasoning={reasoning:,}" if isinstance(reasoning, (int, float)) else f" · reasoning={reasoning}"
                    first += f" = {total_tokens:,}" if isinstance(total_tokens, (int, float)) else f" = {total_tokens}"
                if context_window_tokens is None or estimated is None:
                    second = "context unknown · compact unavailable"
                else:
                    percent = estimated / context_window_tokens * 100
                    marker = "~" if "provider_input" not in sources else ""
                    if compact_threshold is None:
                        second = f"context {marker}{estimated:,}/{context_window_tokens:,} ({percent:.1f}%) · compact disabled"
                    else:
                        decision = "run ending" if run_ending else ("REQUIRED" if estimated >= compact_threshold else "not required")
                        ratio_text = f" ({compact_trigger_ratio * 100:g}%)" if isinstance(compact_trigger_ratio, (int, float)) else ""
                        second = f"context {marker}{estimated:,}/{context_window_tokens:,} ({percent:.1f}%) · compact@{compact_threshold:,}{ratio_text} {decision}"
                decision = "run_ending" if run_ending else ("required" if estimated is not None and compact_threshold is not None and estimated >= compact_threshold else "not_required")
                payload = {"turn": context_turn, "usage": latest, "context_tokens": estimated, "context_basis_tokens": estimated, "context_window_tokens": context_window_tokens, "compact_trigger_ratio": compact_trigger_ratio, "compact_threshold": compact_threshold, "basis_source": sources, "decision": decision, "lines": [first, second], "estimated": bool(sources and "provider_input" not in sources)}
                emit("context_usage", payload)
                audit_write({"record": "context", "record_type": "context", "operation": "turn_context", "model_call_id": (latest or {}).get("model_call_id"), "usage": latest, "context_basis_tokens": estimated, "basis_source": sources, "context_window_tokens": context_window_tokens, "safe_input_tokens": safe_input_tokens, "compact_trigger_ratio": compact_trigger_ratio, "compact_threshold": compact_threshold, "compact_decision": decision})

            def emit_failure_context() -> None:
                if turn > 0:
                    emit_context_usage(
                        turn, last_state_messages_snapshot, run_ending=True
                    )

            failure_context_emitter = emit_failure_context
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
                stream_kwargs["config"] = {"recursion_limit": _graph_recursion_limit(self.spec), "callbacks": [observer]}
            elif "config" in stream_kwargs:
                stream_kwargs["config"]["callbacks"] = [observer]
            async for event in graph.astream_events(inputs, **stream_kwargs):
                name = str(event.get("name") or "")
                kind = str(event.get("event") or "")
                data = event.get("data") or {}
                if kind == "on_chain_start" and name == "model":
                    incoming_messages = _messages_from_event(data.get("input")) or last_state_messages
                    if turn > 0:
                        emit_context_usage(turn, incoming_messages)
                    turn += 1
                    model_call_id = str(event.get("run_id") or uuid.uuid4().hex)
                    primary_ledger_calls[turn] = model_call_id
                    ledger_start(model_call_id, "primary")
                    current_model_call_id = None
                    model_call_started[model_call_id] = datetime.now(timezone.utc)
                    prompt, system_shown = _prompt_from_messages(data.get("input"), self.spec.system_prompt, shown_message_keys, system_shown)
                    current_input_messages = incoming_messages
                    last_state_messages = list(incoming_messages)
                    current_input_messages_snapshot = list(current_input_messages)
                    context_meter.begin_primary(current_input_messages)
                    current_rendered_input_hash = _hash_text(json.dumps(_safe_json({"system_prompt": self.spec.system_prompt, "messages": [_message_text(item) for item in current_input_messages], "tools": [_tool_schema(tool) for tool in self.spec.tools], "output_schema": self.spec.output_schema.model_json_schema() if self.spec.output_schema else None, "settings": inference_options}), ensure_ascii=False, sort_keys=True, separators=(",", ":")))
                    pending_model_inputs[turn] = (prompt, list(current_input_messages), current_rendered_input_hash)
                elif kind == "on_chain_start" and name.startswith("SummarizationMiddleware.before_model"):
                    summary_input_messages = _messages_from_event(data.get("input")) or last_state_messages
                    estimate, _sources = context_meter.count(summary_input_messages)
                    summary_messages = _messages_from_event(data.get("input")) or last_state_messages
                    if compact_threshold is not None and estimate is not None and estimate >= compact_threshold and turn not in compaction_announced_turns:
                        compact_count += 1
                        last_compaction_id = f"compact-{compact_count}"
                        compaction_announced_turns.add(turn)
                        compact_source_refs = [message_ref(message) for message in summary_messages]
                        compaction_source_refs[last_compaction_id] = compact_source_refs
                        emit("compaction_started", {"compaction_id": last_compaction_id, "after_turn": turn, "basis": estimate, "basis_source": _sources, "threshold": compact_threshold, "source_refs": compact_source_refs})
                        compact_seq = audit_write({"record": "context", "record_type": "context", "operation": "compact", "compaction_id": last_compaction_id, "after_turn": turn, "basis": estimate, "basis_source": _sources, "threshold": compact_threshold, "source_refs": compact_source_refs, "status": "started", "summary_template": "langgraph_default"})
                        if compact_seq is not None:
                            source_state["latest_compact"] = (compact_seq, "context")
                elif kind == "on_chat_model_start":
                    metadata = data.get("metadata", {}) or {}
                    observed_model = observed_model or metadata.get("model_name")
                elif kind == "on_chat_model_end":
                    model_usage, observed_usages, usage_conflict, model_name = _model_usage_info(data.get("output"))
                    call_id = str(event.get("run_id") or "") or None
                    call_kind = model_call_kinds.get(call_id or "", "primary")
                    if call_id not in callback_usage_ids and not any(item.get("turn") == turn and item.get("call_kind") == call_kind and item.get("source") == "provider" for item in usage):
                        record_model_usage(model_usage, call_id, call_kind, turn, observed_usages=observed_usages, usage_conflict=usage_conflict)
                    observed_model = observed_model or model_name
                elif kind == "on_chat_model_stream":
                    # Model text is emitted only by the bound public callback.
                    # The graph event remains an accounting signal and is not
                    # rendered, avoiding duplicate assistant output.
                    continue
                elif kind == "on_chain_end" and name == "model":
                    chain_call_id = str(event.get("run_id") or primary_ledger_calls.get(turn) or "")
                    if chain_call_id:
                        ledger_complete(primary_ledger_calls.get(turn, chain_call_id))
                    messages = _messages_from_event(data.get("output"))
                    if messages:
                        existing_keys = {_message_key(message) for message in last_state_messages}
                        last_state_messages.extend(message for message in messages if _message_key(message) not in existing_keys)
                    last_state_messages_snapshot = list(last_state_messages)
                    context_meter.finish_primary(last_state_messages)
                    if turn not in started_turns:
                        prompt, input_messages, rendered_hash = pending_model_inputs.get(turn, ("", [], None))
                        current_model_call_id = current_model_call_id or str(event.get("run_id") or uuid.uuid4().hex)
                        current_rendered_input_hash = rendered_hash
                        started_turns.add(turn)
                        emit("model_started", {"attempt_id": attempt_id, "turn": turn, "model_call_id": current_model_call_id, "call_kind": "primary", "prompt": prompt, "input_message_refs": [message_ref(item) for item in input_messages]})
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
                        for request in requests:
                            request["model_call_id"] = current_model_call_id
                        structured_requests = [request for request in requests if request["kind"] == "structured"]
                        emit(
                            "model_completed",
                            {
                                "attempt_id": attempt_id,
                                "turn": turn,
                                "model_call_id": current_model_call_id,
                                "call_kind": "primary",
                                "tool_count": len(calls),
                                "output": _message_text(ai) if not calls else "",
                                "structured_request": structured_requests[0] if structured_requests else None,
                            },
                        )
                        for request in requests:
                            if request["kind"] == "business":
                                pending_tool_ids.setdefault(str(request["name"]), []).append(str(request["tool_call_id"]))
                            else:
                                tool_calls.append({**request, "status": "requested", "started_at": datetime.now(timezone.utc).isoformat()})
                        # ``_message_text`` deliberately excludes provider
                        # thinking/reasoning blocks; audit is an academic
                        # behavior record and must not persist hidden CoT.
                        capture = consume_request_capture(current_model_call_id)
                        decision_seq = audit_write({"record": "decision", "record_type": "decision", "model_call_id": current_model_call_id, "call_kind": "primary", "status": "completed", "message": _message_text(ai), "output_message_ref": _message_ref(ai), "input_message_refs": [message_ref(item) for item in current_input_messages], "reasoning_summary": _visible_reasoning(ai), "rendered_input_hash": current_rendered_input_hash, "rendered_input_scope": "langchain_model_request", "rendered_input_projection": (capture or {}).get("projection"), "usage": next((item for item in reversed(usage) if item.get("turn") == turn and item.get("call_kind") == "primary"), None)})
                        if decision_seq is not None:
                            source_state["latest_decision"] = (decision_seq, "decision")
                            message_source_refs[_message_key(ai)] = (decision_seq, "decision")
                            if getattr(ai, "id", None):
                                message_source_by_id[str(ai.id)] = (decision_seq, "decision")
                        decision_written_turns.add(turn)
                        unknown_requests = [item for item in requests if item["name"] not in self.spec.tool_names and item["name"] != structured_name]
                        business_requests = [item for item in requests if item["name"] in self.spec.tool_names]
                        if unknown_requests:
                            for request in unknown_requests:
                                audit_write({"record": "action", "kind": "business", "name": request["name"], "tool_call_id": request["tool_call_id"], "arguments": request["arguments"], "status": "rejected", "error": {"code": "tool_not_allowed", "message": "tool is not registered"}})
                        if structured_name and business_requests and any(item["name"] == structured_name for item in requests):
                            for request in business_requests:
                                audit_write({"record": "action", "kind": "business", "name": request["name"], "tool_call_id": request["tool_call_id"], "arguments": request["arguments"], "status": "rejected", "error": {"code": "mixed_terminal_tool", "message": "structured output cannot share a model turn with a business tool"}})
                    model_usage, observed_usages, usage_conflict, model_name = _model_usage_info(data.get("output"))
                    if model_usage and not any(item.get("turn") == turn and item.get("call_kind") == "primary" and item.get("source") == "provider" for item in usage):
                        record_model_usage(model_usage, current_model_call_id, "primary", turn, observed_usages=observed_usages, usage_conflict=usage_conflict)
                    elif not any(item.get("turn") == turn and item.get("call_kind") == "primary" for item in usage):
                        record_model_usage(None, current_model_call_id, "primary", turn, status="unavailable")
                    observed_model = observed_model or model_name
                elif kind == "on_tool_start":
                    ids = pending_tool_ids.get(name, [])
                    call_id = ids.pop(0) if ids else str(event.get("run_id") or uuid.uuid4().hex)
                    args = data.get("input")
                    name_value = name
                    record = {"kind": "business", "name": name_value, "tool_call_id": call_id, "attempt_id": attempt_id, "turn": turn, "arguments": _safe_json(args), "status": "started", "started_at": datetime.now(timezone.utc).isoformat()}
                    tool_calls.append(record)
                    active_tool_records[str(event.get("run_id") or call_id)] = record
                    emit("tool_started", {"name": name_value, "tool_call_id": call_id, "arguments": _safe_json(args), "status": "started", "attempt_id": attempt_id, "turn": turn})
                elif kind == "on_tool_end":
                    result_value = _tool_result_value(data.get("output"))
                    completion_status, completion_error, tool_executed = (
                        _tool_completion_status(result_value)
                    )
                    execution_id = str(event.get("run_id") or "")
                    record = active_tool_records.pop(execution_id, None)
                    if record is None:
                        record = next((item for item in reversed(tool_calls) if item["name"] == name and item["status"] == "started"), None)
                    if record is not None:
                        finished_at = datetime.now(timezone.utc)
                        started_at = datetime.fromisoformat(record["started_at"])
                        record.update(
                            {
                                "status": completion_status,
                                "result": _safe_json(result_value),
                                "tool_executed": tool_executed,
                                "finished_at": finished_at.isoformat(),
                                "duration_seconds": max(
                                    0.0, (finished_at - started_at).total_seconds()
                                ),
                            }
                        )
                        if completion_error is not None:
                            record["error"] = completion_error
                        if tool_executed:
                            business_tool_called = True
                        action_seq = audit_write({"record": "action", "record_type": "action", **record})
                        if action_seq is not None and isinstance(data.get("output"), BaseMessage):
                            message_source_refs[_message_key(data["output"])] = (action_seq, "action")
                        if action_seq is not None:
                            source_state["latest_action"] = (action_seq, "action")
                            message_source_by_id[str(record.get("tool_call_id"))] = (action_seq, "action")
                    if isinstance(data.get("output"), BaseMessage):
                        last_state_messages = [*last_state_messages, data["output"]]
                    emit(
                        "tool_completed" if tool_executed else "tool_rejected",
                        {
                            "name": name,
                            "tool_call_id": record.get("tool_call_id") if record else None,
                            "arguments": record.get("arguments") if record else data.get("input"),
                            "result": _safe_json(result_value),
                            "status": completion_status,
                            "tool_executed": tool_executed,
                            "error": completion_error,
                            "attempt_id": attempt_id,
                            "turn": turn,
                        },
                    )
                    if not active_tool_records:
                        tool_context_tokens, _tool_sources = context_meter.count(last_state_messages)
                        if compact_threshold is not None and tool_context_tokens is not None and tool_context_tokens >= compact_threshold:
                            emit_context_usage(turn, last_state_messages)
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
                    failed_tool_call_ids.add(str(record.get("tool_call_id")))
                    if record.get("started_at"):
                        finished_at = datetime.fromisoformat(record["finished_at"])
                        started_at = datetime.fromisoformat(record["started_at"])
                        record["duration_seconds"] = max(0.0, (finished_at - started_at).total_seconds())
                    action_seq = audit_write({"record": "action", **record})
                    if action_seq is not None and isinstance(data.get("output"), BaseMessage):
                        message_source_refs[_message_key(data["output"])] = (action_seq, "action")
                    if action_seq is not None:
                        source_state["latest_action"] = (action_seq, "action")
                        message_source_by_id[str(record.get("tool_call_id"))] = (action_seq, "action")
                    emit("tool_failed", {"name": name, "tool_call_id": record.get("tool_call_id") if record else None, "arguments": record.get("arguments") if record else None, "error": safe_error, "status": "failed", "attempt_id": attempt_id, "turn": turn})
                elif kind == "on_chain_end" and name.startswith("SummarizationMiddleware.before_model"):
                    replacement = data.get("output") or {}
                    replacement_messages = _messages_from_event(replacement.get("messages") if isinstance(replacement, Mapping) else replacement)
                    context_meter.invalidate_provider_anchor()
                    replacement_refs = [message_ref(message) for message in replacement_messages]
                    replacement_projection = _compact_replacement_projection(replacement_messages)
                    replacement_seq = audit_write({"record": "context", "record_type": "context", "operation": "compact", "compaction_id": last_compaction_id, "replacement": replacement_projection, "replacement_refs": replacement_refs, "replacement_hash": _hash_text(json.dumps(replacement_refs, ensure_ascii=False, sort_keys=True)), "status": "replacement_applied"})
                    if replacement_seq is not None:
                        source_state["latest_compact"] = (replacement_seq, "context")
                        for message in replacement_messages:
                            message_source_refs[_message_key(message)] = (replacement_seq, "context")
                            if getattr(message, "id", None):
                                message_source_by_id[str(message.id)] = (replacement_seq, "context")
                elif kind == "on_chain_end" and name in {"LangGraph", self.spec.name}:
                    state = data.get("output") or {}
                    output = state.get("structured_response")
                    messages = state.get("messages") or []
                    final = next((message for message in reversed(messages) if isinstance(message, AIMessage)), None)
                    if final is not None:
                        final_text = _message_text(final)
                    pending_structured = [
                        item
                        for item in tool_calls
                        if item.get("kind") == "structured"
                        and item.get("status") == "requested"
                    ]
                    structured_record = pending_structured[-1] if pending_structured else None
                    if output is not None:
                        for rejected in pending_structured[:-1]:
                            rejected.update(
                                {
                                    "status": "rejected",
                                    "error": {
                                        "code": "structured_output_invalid",
                                        "message": (
                                            "structured output call was rejected by schema "
                                            "validation and retried"
                                        ),
                                    },
                                    "finished_at": datetime.now(timezone.utc).isoformat(),
                                }
                            )
                            audit_write({"record": "action", **rejected})
                        if structured_record is not None:
                            structured_record.update({"status": "completed", "result": _safe_json(output), "finished_at": datetime.now(timezone.utc).isoformat()})
                            audit_write({"record": "action", **structured_record})
                        emit("structured_output", {"attempt_id": attempt_id, "turn": turn, "model_call_id": (structured_record or {}).get("model_call_id") or current_model_call_id, "call_kind": "primary", "output": _safe_json(output)})
                    emit_context_usage(turn, messages or last_state_messages, run_ending=True)
                    return state
            return None

        try:
            if not input_text.strip():
                raise AgentError("input_invalid", "input_text must not be empty")
            emit("run_started", {
                "profile": self.profile,
                "agent": self.spec.name,
                "model": self.config.model,
                "started_at_utc": started_at_utc.isoformat(),
                "adapter": self.adapter_name,
                "real_llm": self.real_llm,
                "has_context": bool(pages),
                "context_status": "invalid" if context_error is not None else ("loaded" if pages else "none"),
                "config_fingerprint": behavior_fingerprint,
                "system_prompt_hash": _hash_text(self.spec.system_prompt),
                "input_hash": _hash_text(input_text),
                "tools_hash": _behavior_fingerprint({"tools": [_tool_schema(tool) for tool in self.spec.tools]}),
                "output_schema_hash": _behavior_fingerprint(self.spec.output_schema.model_json_schema()) if self.spec.output_schema else None,
                "context_manifest_hash": manifest,
                "endpoint_ref": self.profile or "direct",
                "endpoint_fingerprint": endpoint_fingerprint,
                "dependency_versions": _dependency_versions(),
                "system_chars": len(self.spec.system_prompt),
                "input_chars": len(input_text),
                "context_pages": len(pages),
                "tool_count": len(self.spec.tools),
                "summary_template_hash": _hash_text(DEFAULT_SUMMARY_PROMPT) if compact_threshold is not None else None,
                "effective_options": inference_options,
                "capacity": {"context_window_tokens": context_window_tokens, "max_output_tokens": max_output_tokens, "safe_input_tokens": safe_input_tokens, "capacity_source": capacity_source},
                "compact": {"enabled": compact_trigger_ratio is not None and compact_threshold is not None, "trigger_ratio": compact_trigger_ratio, "threshold": compact_threshold, "keep_messages": _DEFAULT_COMPACT_KEEP_MESSAGES},
                "limits": dict(self.spec.limits or {}),
                "tools": list(self.spec.tool_names),
                "required_tool": self.spec.require_tool_call,
                "retry_missing_structured_output": self.spec.retry_missing_structured_output,
                "structured_output": self.spec.output_schema.__name__ if self.spec.output_schema is not None else None,
                **inference_summary,
            })
            if pages:
                emit("context_loaded", {"attempt_id": attempt_id, "page_count": len(pages), "context_manifest_hash": manifest, "pages": [{"id": page["id"], "hash": page["hash"]} for page in pages]})
            initial_context_seq = audit_write(
                {
                    "record": "context",
                    "record_type": "context",
                    "profile": self.profile,
                    "adapter": self.adapter_name,
                    "config_fingerprint": behavior_fingerprint,
                    "endpoint_ref": self.profile or "direct",
                    "endpoint_fingerprint": endpoint_fingerprint,
                    "dependency_versions": _dependency_versions(),
                    "input_text": input_text,
                    "system_prompt": self.spec.system_prompt,
                    "agent_name": self.spec.name,
                    "started_at_utc": started_at_utc.isoformat(),
                    "model": self.config.model,
                    "inference": inference_summary,
                    "structured_output_mode": "langgraph_response_format" if self.spec.output_schema is not None else None,
                    "tools": [{"name": _tool_name(tool), "description": _tool_description(tool), "schema": _tool_schema(tool)} for tool in self.spec.tools],
                    "output_schema": self.spec.output_schema.model_json_schema() if self.spec.output_schema else None,
                    "pages": pages,
                    "context_status": "invalid" if context_error is not None else ("loaded" if pages else "none"),
                    "capacity": {"context_window_tokens": context_window_tokens, "max_output_tokens": max_output_tokens, "safe_input_tokens": safe_input_tokens, "capacity_source": capacity_source},
                    "compact": {"trigger_ratio": compact_trigger_ratio, "threshold": compact_threshold, "keep_messages": _DEFAULT_COMPACT_KEEP_MESSAGES},
                    "summary_template": "langgraph_default" if compact_threshold is not None else None,
                    "summary_template_hash": _hash_text(DEFAULT_SUMMARY_PROMPT) if compact_threshold is not None else None,
                    "limits": dict(self.spec.limits or {}),
                    "retry_missing_structured_output": self.spec.retry_missing_structured_output,
                    "redaction_report": [],
                    "eligibility_scope": _ELIGIBILITY_SCOPE,
                }
            )
            if context_error is not None:
                emit(
                    "context_failed",
                    {
                        "attempt_id": attempt_id,
                        "code": context_error.code,
                        "message": context_error.message,
                    },
                )
                raise context_error
            if create_agent is None:
                raise AgentError("config_error", "langchain is required")
            heartbeat_task = asyncio.create_task(heartbeat())
            seconds = (self.spec.limits or {}).get("seconds")
            counters = {"model_calls": 0, "tool_calls": 0, "turns": 0}
            deadline = started + float(seconds) if seconds is not None else None
            guard = _AgentGuardMiddleware(
                self.spec,
                context_meter=context_meter,
                compact_threshold=compact_threshold,
                ledger=ledger,
                deadline=deadline,
                reported_usage_enabled=(lambda: compact_tracker is None or compact_tracker.reported_usage_enabled),
                counters=counters,
            )
            primary_model = self.model.with_config(callbacks=[observer]) if hasattr(self.model, "with_config") else self.model
            model_options_middleware = _ModelOptionsMiddleware(
                inference_options,
                tool_choice_resolver=tool_choice_resolver,
            )
            middleware: list[Any] = [
                model_options_middleware,
                _RequestCaptureMiddleware(request_captures),
                guard,
            ]
            if compact_threshold is not None and compact_trigger_ratio is not None:
                summary_model = primary_model.with_config(metadata={"lc_source": "summarization"}) if hasattr(primary_model, "with_config") else primary_model
                summary_model = summary_model.bind(**inference_options) if inference_options else summary_model
                middleware.append(
                    SummarizationMiddleware(
                        summary_model,
                        trigger=("tokens", compact_threshold),
                        keep=("messages", _DEFAULT_COMPACT_KEEP_MESSAGES),
                        token_counter=compact_tracker.token_counter if compact_tracker is not None else (lambda state_messages: context_meter.estimate(state_messages) or 0),
                        trim_tokens_to_summarize=None,
                    )
                )
                middleware.append(_CompactPostGuardMiddleware(compact_tracker, compaction_validated, compaction_failed))
            graph = create_agent(
                model=primary_model,
                tools=_langchain_tools(self.spec.tools),
                system_prompt=self.spec.system_prompt,
                response_format=self.spec.output_schema,
                middleware=middleware,
                name=self.spec.name,
            )
            terminal_state: dict[str, Any] | None
            if seconds is None:
                terminal_state = await consume(graph)
            else:
                remaining = float(seconds) - (time.monotonic() - started)
                if remaining <= 0:
                    raise AgentError("limit_exceeded", "seconds limit exceeded")
                terminal_state = await asyncio.wait_for(
                    consume(graph), timeout=remaining
                )
            if (
                output is None
                and self.spec.output_schema is not None
                and self.spec.retry_missing_structured_output
            ):
                retry_message = HumanMessage(
                    content=(
                        "The previous path ended without the required structured output. "
                        "Continue the same task from the complete visible history. Complete "
                        "any still-missing mandatory business-tool step, then return exactly "
                        "one structured output. Do not end with prose or an empty response."
                    )
                )
                audit_write(
                    {
                        "record": "context",
                        "record_type": "context",
                        "operation": "missing_structured_output_retry",
                        "status": "started",
                        "previous_turn": turn,
                        "instruction_hash": _hash_text(_message_text(retry_message)),
                    }
                )
                current_mandatory_choice = (
                    tool_choice_resolver() if tool_choice_resolver is not None else None
                )
                model_options_middleware.forced_tool_choice = (
                    None if current_mandatory_choice is not None else "required"
                )
                terminal_messages = (
                    list(terminal_state.get("messages") or [])
                    if isinstance(terminal_state, Mapping)
                    else []
                )
                replay_messages, rejected_calls = _prepare_recovery_history(
                    terminal_messages or last_state_messages_snapshot,
                    structured_name=self.spec.output_schema.__name__,
                    business_names=self.spec.tool_names,
                )
                for rejected_call in rejected_calls:
                    is_structured = (
                        rejected_call.get("name") == self.spec.output_schema.__name__
                    )
                    rejected_record = {
                        "kind": "structured" if is_structured else "business",
                        "name": rejected_call.get("name"),
                        "tool_call_id": rejected_call.get("tool_call_id"),
                        "arguments": None,
                        "attempt_id": attempt_id,
                        "turn": turn,
                        "status": "rejected",
                        "started_at": datetime.now(timezone.utc).isoformat(),
                        "finished_at": datetime.now(timezone.utc).isoformat(),
                        "error": {
                            "code": (
                                "structured_output_invalid"
                                if is_structured
                                else "tool_arguments_invalid"
                            ),
                            "message": (
                                "provider returned a malformed structured-output tool call; "
                                "the invalid terminal assistant message was excluded from replay"
                                if is_structured
                                else "provider returned malformed arguments for a registered "
                                "business tool that was not executed; the invalid terminal "
                                "assistant message was excluded from replay"
                            ),
                        },
                    }
                    tool_calls.append(rejected_record)
                    audit_write({"record": "action", **rejected_record})
                if rejected_calls:
                    audit_write(
                        {
                            "record": "context",
                            "record_type": "context",
                            "operation": "recovery_history_sanitized",
                            "status": "completed",
                            "rejected_calls": rejected_calls,
                            "retained_message_count": len(replay_messages),
                        }
                    )
                retry_messages = [
                    *replay_messages,
                    retry_message,
                ]
                if seconds is None:
                    await consume(graph, retry_messages)
                else:
                    remaining = float(seconds) - (time.monotonic() - started)
                    if remaining <= 0:
                        raise AgentError("limit_exceeded", "seconds limit exceeded")
                    await asyncio.wait_for(
                        consume(graph, retry_messages), timeout=remaining
                    )
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
                    "phase": "model_transport",
                    "remediation": "verify endpoint availability, timeout, and provider request id",
                }
            else:
                error = {"code": "limit_exceeded", "message": "seconds limit exceeded", "details": details, "phase": "run_budget", "remediation": "increase the explicit seconds limit or shorten the task"}
        except asyncio.CancelledError:
            status = "cancelled"
            error = {"code": "cancelled", "message": "agent run was cancelled"}
        except AgentError as exc:
            error = {"code": exc.code, "message": exc.message}
            if exc.details:
                error["details"] = _redact(_safe_json(exc.details))
            error.setdefault("phase", "agent_runtime")
            error.setdefault("remediation", "inspect code, message, and details; verify model/tool/configuration inputs")
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
            error["phase"] = "agent_runtime"
            error["remediation"] = "inspect details for provider, tool, or runtime ownership before retrying"
        finally:
            if heartbeat_task is not None:
                heartbeat_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await heartbeat_task
            try:
                if error is not None and current_model_call_id is not None and turn not in decision_written_turns:
                    capture = consume_request_capture(current_model_call_id)
                    audit_write(
                        {
                            "record": "decision",
                            "record_type": "decision",
                            "model_call_id": current_model_call_id,
                            "call_kind": model_call_kinds.get(current_model_call_id, "primary"),
                            "status": "cancelled" if status == "cancelled" else "failed",
                            "message": partial_texts.get(current_model_call_id, ""),
                            "input_message_refs": [message_ref(item) for item in current_input_messages_snapshot],
                            "rendered_input_hash": current_rendered_input_hash,
                            "rendered_input_scope": "langchain_model_request",
                            "rendered_input_projection": capture.get("projection"),
                            "usage": next((item for item in reversed(usage) if item.get("model_call_id") == current_model_call_id), None),
                            "error": transport_errors.get(current_model_call_id) or error,
                        }
                    )
                    decision_written_turns.add(turn)
                ledger.cancel_pending()
                ended_at_utc = datetime.now(timezone.utc)
                duration_seconds = max(0.0, time.monotonic() - started)
                for record in tool_calls:
                    if record.get("status") in {"started", "requested"}:
                        if error is None:
                            error = {"code": "incomplete_tool", "message": "tool execution did not produce a completion event"}
                            status = "failed"
                        finished_at = datetime.now(timezone.utc)
                        started_at = datetime.fromisoformat(record["started_at"]) if record.get("started_at") else finished_at
                        unfinished_status = "cancelled" if error.get("code") in {"tool_error", "provider_error", "cancelled"} else "failed"
                        record.update({"status": unfinished_status, "error": error, "finished_at": finished_at.isoformat(), "duration_seconds": max(0.0, (finished_at - started_at).total_seconds())})
                        emit("tool_failed", {"name": record.get("name"), "tool_call_id": record.get("tool_call_id"), "arguments": record.get("arguments"), "error": error, "status": unfinished_status, "attempt_id": record.get("attempt_id"), "turn": record.get("turn")})
                        audit_write({"record": "action", **record})
                if error is not None and turn > 0 and failure_context_emitter is not None and turn not in context_events_seen:
                    failure_context_emitter()
                if canonical_result_out is not None:
                    provisional_eligible = bool(audit.enabled and audit_ok and status == "success")
                    provisional_reasons = ["trace_complete_pending_commit"] if provisional_eligible else ["agent_failed"]
                    provisional_result = AgentRunResult(
                        run_id, status,
                        _redact_with_inventory(output, sensitive_values),
                        _redact_with_inventory(final_text, sensitive_values),
                        _redact_with_inventory(tool_calls, sensitive_values),
                        _redact_with_inventory(usage, sensitive_values),
                        _redact_with_inventory(error, sensitive_values),
                        self.real_llm, self.config.model,
                        observed_model, provisional_eligible, manifest, profile=self.profile,
                        context_window_tokens=context_window_tokens, max_output_tokens=max_output_tokens,
                        safe_input_tokens=safe_input_tokens, capacity_source=capacity_source,
                        eligibility_scope=_ELIGIBILITY_SCOPE, eligibility_reasons=provisional_reasons,
                        trace_commit_id=audit.trace_commit_id, model_calls_used=ledger.used,
                        model_calls_reserved=ledger.reserved, compact_count=compact_count,
                        started_at_utc=started_at_utc.isoformat(),
                        ended_at_utc=ended_at_utc.isoformat() if ended_at_utc is not None else None,
                        duration_seconds=duration_seconds,
                    )
                    try:
                        _atomic_write(canonical_result_out, provisional_result.to_dict(), run_id=run_id)
                    except Exception as exc:
                        error = {"code": "json_export_failed", "message": "result output failed; audit finish records the export failure", "details": _exception_details(exc), "phase": "result_export", "remediation": "inspect result output path and permissions"}
                        status = "failed"
                audit_error = dict(error or {})
                audit_error.pop("remediation", None)
                audit_write({"record": "finish", "record_type": "finish", "trace_commit_id": audit.trace_commit_id, "status": status, "agent_status": status, "started_at_utc": started_at_utc.isoformat(), "ended_at_utc": ended_at_utc.isoformat(), "duration_seconds": duration_seconds, "model_calls_used": ledger.used, "model_calls_reserved": ledger.reserved, "compact_count": compact_count, "usage": usage, "trace_complete": True, "trace_commit_pending": True, "academic_eligible": False, "eligibility_reasons": ["trace_complete_pending_commit"], "final_text": final_text, "output": output, "error": audit_error or None, "redaction_report": redaction_report(), "reason": "structured_output" if output is not None else ("final_answer" if status == "success" else (error or {}).get("code", "runtime_error"))})
            except AgentError:
                error = {"code": "audit_write_failed", "message": "audit output failed"}
                status = "failed"
            try:
                audit.close()
            except AgentError:
                audit_ok = False
                error = {"code": "audit_write_failed", "message": "audit output could not be finalized"}
                status = "failed"
        trace_commit_id = audit.trace_commit_id
        eligibility_reasons = []
        if not audit.enabled:
            eligibility_reasons.append("audit_disabled")
        if status != "success":
            eligibility_reasons.append("agent_failed")
        candidate_eligible = bool(audit.enabled and audit_ok and status == "success")
        if candidate_eligible:
            # The final result is serialized before publishing the receipt;
            # include the expected commit reason now so its hash remains stable.
            eligibility_reasons.extend(("trace_complete", "receipt_committed"))
        academic_eligible = candidate_eligible
        result = AgentRunResult(
            run_id, status,
            _redact_with_inventory(output, sensitive_values),
            _redact_with_inventory(final_text, sensitive_values),
            _redact_with_inventory(tool_calls, sensitive_values),
            _redact_with_inventory(usage, sensitive_values),
            _redact_with_inventory(error, sensitive_values),
            self.real_llm, self.config.model,
            observed_model, academic_eligible, manifest, profile=self.profile,
            context_window_tokens=context_window_tokens, max_output_tokens=max_output_tokens,
            safe_input_tokens=safe_input_tokens, capacity_source=capacity_source,
            eligibility_scope=_ELIGIBILITY_SCOPE, eligibility_reasons=eligibility_reasons,
            trace_commit_id=trace_commit_id,
            model_calls_used=ledger.used,
            model_calls_reserved=ledger.reserved,
            compact_count=compact_count,
            started_at_utc=started_at_utc.isoformat(),
            ended_at_utc=ended_at_utc.isoformat() if ended_at_utc is not None else None,
            duration_seconds=duration_seconds,
        )
        receipt_ok, _receipt_path = _publish_receipt(canonical_audit_out, canonical_result_out, run_id=run_id, trace_commit_id=trace_commit_id, finish_seq=audit.order, eligibility_scope=_ELIGIBILITY_SCOPE, status=status)
        # The first receipt commits the provisional result hash.  Once the
        # commit point exists, publish the final in-memory eligibility view and
        # refresh the receipt so its result hash still matches the file.
        if receipt_ok and audit.enabled and status == "success" and canonical_result_out is not None:
            try:
                _atomic_write(canonical_result_out, result.to_dict(), run_id=run_id)
                receipt_ok, _receipt_path = _publish_receipt(
                    canonical_audit_out,
                    canonical_result_out,
                    run_id=run_id,
                    trace_commit_id=trace_commit_id,
                    finish_seq=audit.order,
                    eligibility_scope=_ELIGIBILITY_SCOPE,
                    status=status,
                )
            except Exception:
                receipt_ok = False
        audit.release_lock()
        if audit.enabled and status == "success" and not receipt_ok:
            status = "failed"
            error = {"code": "audit_write_failed", "message": "academic receipt could not be committed"}
            result.status = status
            result.error = error
            result.academic_eligible = False
            result.eligibility_reasons = [reason for reason in result.eligibility_reasons if reason not in {"trace_complete", "receipt_committed"}] + ["receipt_missing_or_invalid"]
        academic_eligible = bool(receipt_ok and candidate_eligible)
        if academic_eligible:
            result.academic_eligible = True
            result.eligibility_reasons = ["trace_complete", "receipt_committed"]
        elif "receipt_missing_or_invalid" not in result.eligibility_reasons:
            result.eligibility_reasons.append("receipt_missing_or_invalid")
        if canonical_result_out is not None and not receipt_ok:
            with contextlib.suppress(Exception):
                _atomic_write(canonical_result_out, result.to_dict(), run_id=run_id)
        if error is None and status == "success":
            emit("completed", {"model": self.config.model, "profile": self.profile, "output": _safe_json(output), "final_text": final_text, "usage": usage, "academic_eligible": academic_eligible, "eligibility_scope": _ELIGIBILITY_SCOPE})
        else:
            emit("failed", {**(error or {"code": "runtime_error", "message": "agent run failed"}), "eligibility_scope": _ELIGIBILITY_SCOPE, "academic_eligible": False})
        renderer_obj.close()
        return result


def _input_with_context(input_text: str, pages: Sequence[Mapping[str, Any]]) -> str:
    parts = [input_text]
    if pages:
        rendered = "\n\n".join(f"[{page['id']}]\n{page['text']}" for page in pages)
        parts.append(f"上下文页面（按顺序，不可改写）：\n{rendered}")
    return "\n\n".join(parts)


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


def _message_ref(
    message: Any,
    *,
    source_seq: int | None = None,
    source_record: str | None = None,
) -> dict[str, Any]:
    role = getattr(message, "type", None) or message.__class__.__name__
    identity = getattr(message, "id", None)
    text = _message_text(message)
    ref = {
        "id": str(identity) if identity else None,
        "role": str(role),
        "content_hash": _hash_text(text),
        "content": _safe_json(text),
        "source_seq": source_seq,
        "source_record": source_record,
    }
    protocol_calls = _message_protocol_tool_calls(message)
    if protocol_calls:
        ref["tool_calls"] = protocol_calls
    tool_call_id = getattr(message, "tool_call_id", None)
    if tool_call_id:
        ref["tool_call_id"] = str(tool_call_id)
    return ref


def _message_protocol_tool_calls(message: Any) -> list[dict[str, Any]]:
    """Return visible tool-call identities, including provider-invalid calls."""

    descriptors: dict[str, dict[str, Any]] = {}

    def add(call: Mapping[str, Any], *, valid: bool, source: str) -> None:
        function = call.get("function")
        function = function if isinstance(function, Mapping) else {}
        call_id = call.get("id") or call.get("tool_call_id")
        name = call.get("name") or function.get("name")
        if call_id is None and name is None:
            return
        key = str(call_id) if call_id is not None else f"name:{name}:{len(descriptors)}"
        current = descriptors.get(key)
        item = {
            "tool_call_id": str(call_id) if call_id is not None else None,
            "name": str(name) if name is not None else None,
            "valid": bool(valid),
            "source": source,
        }
        if current is None or (valid and not current["valid"]):
            descriptors[key] = item

    for call in list(getattr(message, "tool_calls", None) or []):
        if isinstance(call, Mapping):
            add(call, valid=True, source="tool_calls")
    for call in list(getattr(message, "invalid_tool_calls", None) or []):
        if isinstance(call, Mapping):
            add(call, valid=False, source="invalid_tool_calls")
    additional = getattr(message, "additional_kwargs", None)
    raw_calls = additional.get("tool_calls") if isinstance(additional, Mapping) else None
    for call in list(raw_calls or []):
        if isinstance(call, Mapping):
            add(call, valid=False, source="provider_raw_tool_calls")
    return list(descriptors.values())


def _prepare_recovery_history(
    messages: Sequence[Any],
    *,
    structured_name: str,
    business_names: Sequence[str] = (),
) -> tuple[list[Any], list[dict[str, Any]]]:
    """Validate provider tool-message ordering before replaying terminal state.

    A malformed provider response may survive as ``invalid_tool_calls`` or raw
    ``additional_kwargs.tool_calls`` even though LangGraph cannot execute it.
    Replaying that terminal assistant message violates the OpenAI-compatible
    message protocol. Only a final, invalid call to the configured structured
    output tool, or to a registered business tool that was never executable, may
    be excluded and retried. Missing responses for valid calls, unknown tools,
    or corruption in the middle of history fail closed.
    """

    history = list(messages)
    recoverable_names = {structured_name, *business_names}
    pending: dict[str, dict[str, Any]] = {}
    pending_index: int | None = None
    for index, message in enumerate(history):
        if pending:
            if isinstance(message, ToolMessage):
                response_id = str(getattr(message, "tool_call_id", "") or "")
                if response_id not in pending:
                    raise AgentError(
                        "message_protocol_invalid",
                        "tool response does not match the preceding assistant tool calls",
                        details={"tool_call_id": response_id, "pending_tool_call_ids": sorted(pending)},
                    )
                pending.pop(response_id)
                continue
            raise AgentError(
                "message_protocol_invalid",
                "assistant tool calls are not immediately followed by all required tool responses",
                details={"pending_tool_call_ids": sorted(pending), "message_index": index},
            )

        calls = _message_protocol_tool_calls(message)
        calls_without_ids = [item for item in calls if not item.get("tool_call_id")]
        if calls_without_ids:
            if (
                index == len(history) - 1
                and all(not item["valid"] for item in calls_without_ids)
                and all(item.get("name") in recoverable_names for item in calls_without_ids)
            ):
                return history[:index], calls_without_ids
            raise AgentError(
                "message_protocol_invalid",
                "tool call without an ID cannot be safely replayed",
                details={"tool_calls": calls_without_ids, "message_index": index},
            )
        calls_with_ids = [item for item in calls if item.get("tool_call_id")]
        if calls_with_ids:
            pending = {str(item["tool_call_id"]): item for item in calls_with_ids}
            pending_index = index

    if not pending:
        return history, []
    assert pending_index is not None
    dangling = list(pending.values())
    if (
        pending_index == len(history) - 1
        and all(not item["valid"] for item in dangling)
        and all(item.get("name") in recoverable_names for item in dangling)
    ):
        return history[:pending_index], dangling
    raise AgentError(
        "message_protocol_invalid",
        "terminal history contains incomplete tool calls that cannot be safely replayed",
        details={
            "pending_tool_calls": dangling,
            "message_index": pending_index,
            "structured_output_tool": structured_name,
        },
    )


def _compact_replacement_projection(messages: Sequence[Any]) -> dict[str, Any]:
    """Export only visible replacement evidence, never raw LangGraph state."""

    refs = [_message_ref(message) for message in messages]
    return {"message_count": len(refs), "message_refs": refs}


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


def _visible_reasoning(message: Any) -> str | None:
    metadata = getattr(message, "response_metadata", {}) or {}
    if isinstance(metadata, Mapping):
        value = metadata.get("reasoning_summary") or metadata.get("rationale")
        return value if isinstance(value, str) else None
    return None
