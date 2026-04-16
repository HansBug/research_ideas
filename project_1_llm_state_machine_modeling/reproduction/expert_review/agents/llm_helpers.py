from __future__ import annotations

from typing import Any

from langchain_openai import ChatOpenAI

from ..expert_review_utils import ensure_json


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


def invoke_llm_text(
    llm: ChatOpenAI,
    messages: list[tuple[str, str]],
    *,
    json_mode: bool = False,
) -> str:
    runnable = llm.bind(response_format={"type": "json_object"}) if json_mode else llm
    response = runnable.invoke(messages)
    text = content_to_text(getattr(response, "content", response)).strip()
    if text:
        return text
    chunks: list[str] = []
    for chunk in runnable.stream(messages):
        part = content_to_text(getattr(chunk, "content", chunk)).strip()
        if part:
            chunks.append(part)
    return "".join(chunks).strip()


def invoke_llm_json(
    llm: ChatOpenAI,
    messages: list[tuple[str, str]],
) -> dict[str, Any] | None:
    try:
        raw = invoke_llm_text(llm, messages, json_mode=True)
        return ensure_json(raw)
    except Exception:
        try:
            raw = invoke_llm_text(llm, messages, json_mode=False)
            repair = invoke_llm_text(
                llm,
                [
                    ("system", "Convert the previous answer into strict JSON only."),
                    ("user", raw),
                ],
                json_mode=True,
            )
            return ensure_json(repair)
        except Exception:
            return None
