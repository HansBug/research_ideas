"""LLM 调用辅助 —— 统一处理 transport / JSON 解析 / repair / telemetry。

**作用**：把所有 LLM 调用的横切关注点集中到 3 个公开函数：

1. :func:`invoke_llm_text` —— 用于纯文本输出（如 final_synthesizer 精化
   reason_text）；
2. :func:`invoke_llm_json` —— 用于 JSON-mode 输出（rubric_scorer / 各
   ``*_with_llm`` 入口）；自动包含一次 "repair" 兜底（先 free-form 拿
   text 再用 LLM 转 JSON）；
3. :func:`content_to_text` —— LangChain message ``.content`` 字段
   多形态归一化（str / list[ContentBlock] / 等）。

**设计思路**：

* **不做业务判断**：本模块只搬数据（messages → text/json）+ 记录
  telemetry，业务校验（schema / sanity bound）在调用方做；
* **JSON repair 一次**：::func:`invoke_llm_json` 主路径失败时尝试
  free-form + repair-prompt；再失败返回 ``None``；
* **总有 telemetry**：所有调用经过 :func:`llm_telemetry.record_llm_operation`
  累加到当前 ``llm_run_context``，无 silent skip。

**已知 caveat**：

* :func:`invoke_llm_json` 返回 ``None`` 时不抛异常——调用方必须显式
  处理 ``None`` 走 fallback。这是 issue I-4 silent fallback 的源头之一。
"""

from __future__ import annotations

import time
from typing import Any

from langchain_openai import ChatOpenAI

from ..llm_telemetry import record_llm_operation, usage_dict_from_response
from ..utils import ensure_json


def content_to_text(content: object) -> str:
    """把 LangChain message ``.content`` 多形态字段归一化为字符串。

    支持 ``str`` / ``list[ContentBlock]`` / ``None`` / 其它，对每种
    情况返回最合理的字符串表示。

    :param content: ``response.content`` 之类的字段
    :return: 归一化后的字符串

    Examples::

        >>> content_to_text("hello")
        'hello'
        >>> content_to_text(None)
        ''
    """
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
    """内部 helper：实际发起 LLM 调用并采集 transport 级 stats。

    若 invoke 返回空文本且 ``allow_stream_fallback=True``，会切到 stream
    模式拼接 chunk。

    :param llm: ChatOpenAI 实例
    :param messages: ``[("system", text), ("user", text), ...]``
    :param json_mode: 是否走 ``response_format={"type": "json_object"}``
    :param allow_stream_fallback: 空响应时是否回退 stream 模式
    :return: ``(text, stats_dict)`` 二元组
    """
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
    """以纯文本形式调用 LLM 并返回响应文本。

    :param llm: ChatOpenAI 实例
    :param messages: 消息列表
    :param json_mode: 是否启用 JSON 模式（一般纯文本调用应保持
        ``False``）
    :param operation: telemetry 用的 operation 标识符
    :return: LLM 响应文本（已 strip）
    :raises Exception: transport 层失败会上抛；本函数不做 silent fallback

    .. note::
        与 :func:`invoke_llm_json` 不同，本函数遇到 LLM 异常**直接抛**，
        让调用方决定是否 fallback。
    """
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
    """以 JSON 模式调用 LLM；失败时尝试 repair；最终失败返回 ``None``。

    完整流程::

        1. 先按 json_mode=True 调用一次，:func:`utils.ensure_json` 解析
        2. 失败则 free-form 调一次拿 text，再用 repair-prompt 让 LLM
           把 text 转 JSON
        3. 仍失败返回 ``None``

    :param llm: ChatOpenAI 实例
    :param messages: 消息列表
    :param operation: telemetry 标识
    :return: 解析后的 dict；全部失败返回 ``None``
    :rtype: dict[str, Any] | None

    .. note::
        本函数遇到失败时**返回 None 而非抛异常**——这是为了让 ``*_with_llm``
        函数能直接 ``if payload is None: fallback to deterministic``。
        但这与 strict-llm 协议有张力（issue I-4）。
    """
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
