from __future__ import annotations

import time
from typing import Any

from langchain_openai import ChatOpenAI

from ..llm_telemetry import record_llm_operation, usage_dict_from_response
from ..utils import ensure_json


def content_to_text(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            text = getattr(item, "text", None)
            if isinstance(text, str):
                parts.append(text)
            else:
                parts.append(str(item))
        return "".join(parts)
    return "" if content is None else str(content)


def _invoke_transport(
    llm: ChatOpenAI,
    messages: list[tuple[str, str]],
    *,
    json_mode: bool = False,
    allow_stream_fallback: bool = True,
) -> tuple[str, dict[str, Any]]:
    runnable = llm.bind(response_format={"type": "json_object"}) if json_mode else llm
    stats = {
        "transport_call_count": 0,
        "failed_transport_call_count": 0,
        "latency_s": 0.0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "used_stream": False,
    }
    start = time.perf_counter()
    try:
        response = runnable.invoke(messages)
    except Exception:
        stats["transport_call_count"] += 1
        stats["failed_transport_call_count"] += 1
        stats["latency_s"] += time.perf_counter() - start
        raise
    stats["transport_call_count"] += 1
    stats["latency_s"] += time.perf_counter() - start
    usage = usage_dict_from_response(response)
    stats["prompt_tokens"] += usage["prompt_tokens"]
    stats["completion_tokens"] += usage["completion_tokens"]
    stats["total_tokens"] += usage["total_tokens"]
    text = content_to_text(getattr(response, "content", response)).strip()
    if text or not allow_stream_fallback:
        return text, stats

    start = time.perf_counter()
    chunks: list[str] = []
    try:
        for chunk in runnable.stream(messages):
            stats["used_stream"] = True
            part = content_to_text(getattr(chunk, "content", chunk)).strip()
            if part:
                chunks.append(part)
            usage = usage_dict_from_response(chunk)
            stats["prompt_tokens"] += usage["prompt_tokens"]
            stats["completion_tokens"] += usage["completion_tokens"]
            stats["total_tokens"] += usage["total_tokens"]
    except Exception:
        stats["transport_call_count"] += 1
        stats["failed_transport_call_count"] += 1
        stats["latency_s"] += time.perf_counter() - start
        raise
    stats["transport_call_count"] += 1
    stats["latency_s"] += time.perf_counter() - start
    return "".join(chunks).strip(), stats


def invoke_llm_text(
    llm: ChatOpenAI,
    messages: list[tuple[str, str]],
    *,
    json_mode: bool = False,
    operation: str = "generic_text",
) -> str:
    start = time.perf_counter()
    stats: dict[str, Any] = {
        "transport_call_count": 0,
        "failed_transport_call_count": 0,
        "latency_s": 0.0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "used_stream": False,
    }
    success = False
    error_type: str | None = None
    try:
        text, stats = _invoke_transport(llm, messages, json_mode=json_mode)
        success = bool(text)
        return text
    except Exception as exc:
        error_type = type(exc).__name__
        raise
    finally:
        record_llm_operation(
            operation=operation,
            success=success,
            json_mode=json_mode,
            repair_used=False,
            used_stream=bool(stats["used_stream"]),
            transport_call_count=int(stats["transport_call_count"]),
            failed_transport_call_count=int(stats["failed_transport_call_count"]),
            latency_s=time.perf_counter() - start,
            prompt_tokens=int(stats["prompt_tokens"]),
            completion_tokens=int(stats["completion_tokens"]),
            total_tokens=int(stats["total_tokens"]),
            error_type=error_type,
        )


def invoke_llm_json(
    llm: ChatOpenAI,
    messages: list[tuple[str, str]],
    *,
    operation: str = "generic_json",
) -> dict[str, Any] | None:
    start = time.perf_counter()
    stats: dict[str, Any] = {
        "transport_call_count": 0,
        "failed_transport_call_count": 0,
        "latency_s": 0.0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "used_stream": False,
    }
    success = False
    error_type: str | None = None
    repair_used = False
    try:
        raw, primary_stats = _invoke_transport(llm, messages, json_mode=True)
        for key in stats:
            if key == "used_stream":
                stats[key] = bool(stats[key] or primary_stats[key])
            else:
                stats[key] += primary_stats[key]
        payload = ensure_json(raw)
        success = isinstance(payload, dict)
        return payload
    except Exception as exc:
        error_type = type(exc).__name__
        try:
            repair_used = True
            raw, fallback_stats = _invoke_transport(llm, messages, json_mode=False)
            for key in stats:
                if key == "used_stream":
                    stats[key] = bool(stats[key] or fallback_stats[key])
                else:
                    stats[key] += fallback_stats[key]
            repair, repair_stats = _invoke_transport(
                llm,
                [
                    ("system", "Convert the previous answer into strict JSON only."),
                    ("user", raw),
                ],
                json_mode=True,
                allow_stream_fallback=True,
            )
            for key in stats:
                if key == "used_stream":
                    stats[key] = bool(stats[key] or repair_stats[key])
                else:
                    stats[key] += repair_stats[key]
            payload = ensure_json(repair)
            success = isinstance(payload, dict)
            return payload
        except Exception as repair_exc:
            error_type = type(repair_exc).__name__
            return None
    finally:
        record_llm_operation(
            operation=operation,
            success=success,
            json_mode=True,
            repair_used=repair_used,
            used_stream=bool(stats["used_stream"]),
            transport_call_count=int(stats["transport_call_count"]),
            failed_transport_call_count=int(stats["failed_transport_call_count"]),
            latency_s=time.perf_counter() - start,
            prompt_tokens=int(stats["prompt_tokens"]),
            completion_tokens=int(stats["completion_tokens"]),
            total_tokens=int(stats["total_tokens"]),
            error_type=error_type,
        )
