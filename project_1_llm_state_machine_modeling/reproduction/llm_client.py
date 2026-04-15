from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI

from config import CACHE_ROOT, DEFAULT_MODEL, DEFAULT_PROVIDER_ORDER, PROVIDERS, resolve_api_env


PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [("system", "{system_prompt}"), ("user", "{user_prompt}")]
)


@dataclass
class LLMResult:
    provider: str
    model: str
    text: str
    raw_mode: str
    cached: bool = False


class LLMClient:
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        provider_order: Iterable[str] | None = None,
        timeout: int = 180,
    ) -> None:
        self.model = model
        self.provider_order = list(provider_order or DEFAULT_PROVIDER_ORDER)
        self.timeout = timeout
        self.env = resolve_api_env()
        CACHE_ROOT.mkdir(parents=True, exist_ok=True)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        temperature: float = 0.0,
        max_output_tokens: int = 4000,
        cache_key: str | None = None,
        reasoning_effort: str = "high",
    ) -> LLMResult:
        cache_path = self._cache_path(
            cache_key=cache_key,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )
        if cache_path.exists():
            payload = json.loads(cache_path.read_text(encoding="utf-8"))
            return LLMResult(
                provider=payload["provider"],
                model=payload["model"],
                text=payload["text"],
                raw_mode=payload["raw_mode"],
                cached=True,
            )

        errors: list[str] = []
        for provider_key in self.provider_order:
            provider = PROVIDERS[provider_key]
            api_key = self._resolve_api_key(provider.env_keys)
            if not api_key:
                errors.append(f"{provider_key}:missing_api_key")
                continue
            client = OpenAI(
                api_key=api_key,
                base_url=provider.base_url,
                timeout=self.timeout,
                max_retries=0,
            )
            attempts = (
                ("responses", self._responses_create),
                ("chat", self._chat_create),
            )
            for raw_mode, fn in attempts:
                try:
                    text = fn(
                        client=client,
                        system_prompt=system_prompt,
                        user_prompt=user_prompt,
                        temperature=temperature,
                        max_output_tokens=max_output_tokens,
                        reasoning_effort=reasoning_effort,
                    )
                    if text:
                        result = LLMResult(
                            provider=provider_key,
                            model=self.model,
                            text=text.strip(),
                            raw_mode=raw_mode,
                            cached=False,
                        )
                        cache_path.write_text(
                            json.dumps(
                                {
                                    "provider": result.provider,
                                    "model": result.model,
                                    "text": result.text,
                                    "raw_mode": result.raw_mode,
                                },
                                ensure_ascii=False,
                                indent=2,
                            ),
                            encoding="utf-8",
                        )
                        return result
                except Exception as exc:
                    errors.append(f"{provider_key}:{raw_mode}:{type(exc).__name__}:{exc}")
        raise RuntimeError("All providers failed: " + " | ".join(errors))

    def _resolve_api_key(self, env_keys: Iterable[str]) -> str | None:
        for env_key in env_keys:
            value = self.env.get(env_key)
            if value:
                return value
        return None

    def _cache_path(
        self,
        *,
        cache_key: str | None,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_output_tokens: int,
    ) -> Path:
        if cache_key is None:
            digest_input = {
                "model": self.model,
                "providers": self.provider_order,
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "temperature": temperature,
                "max_output_tokens": max_output_tokens,
            }
            cache_key = hashlib.sha256(
                json.dumps(digest_input, ensure_ascii=False, sort_keys=True).encode("utf-8")
            ).hexdigest()
        else:
            cache_key = hashlib.sha256(cache_key.encode("utf-8")).hexdigest()
        return CACHE_ROOT / f"{cache_key}.json"

    def _message_payload(self, system_prompt: str, user_prompt: str) -> list[dict[str, str]]:
        messages = PROMPT_TEMPLATE.invoke(
            {"system_prompt": system_prompt, "user_prompt": user_prompt}
        ).to_messages()
        role_map = {"system": "system", "human": "user", "ai": "assistant"}
        payload: list[dict[str, str]] = []
        for message in messages:
            payload.append(
                {"role": role_map.get(message.type, message.type), "content": str(message.content)}
            )
        return payload

    def _responses_create(
        self,
        *,
        client: OpenAI,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_output_tokens: int,
        reasoning_effort: str,
    ) -> str:
        response = client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=user_prompt,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )
        return getattr(response, "output_text", "").strip()

    def _responses_stream(
        self,
        *,
        client: OpenAI,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_output_tokens: int,
        reasoning_effort: str,
    ) -> str:
        with client.responses.stream(
            model=self.model,
            instructions=system_prompt,
            input=user_prompt,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        ) as stream:
            for _ in stream:
                pass
            response = stream.get_final_response()
        return getattr(response, "output_text", "").strip()

    def _chat_create(
        self,
        *,
        client: OpenAI,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_output_tokens: int,
        reasoning_effort: str,
    ) -> str:
        response = client.chat.completions.create(
            model=self.model,
            messages=self._message_payload(system_prompt, user_prompt),
            temperature=temperature,
            max_tokens=max_output_tokens,
        )
        return response.choices[0].message.content or ""

    def _chat_stream(
        self,
        *,
        client: OpenAI,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_output_tokens: int,
        reasoning_effort: str,
    ) -> str:
        stream = client.chat.completions.create(
            model=self.model,
            messages=self._message_payload(system_prompt, user_prompt),
            temperature=temperature,
            max_tokens=max_output_tokens,
            stream=True,
        )
        parts: list[str] = []
        for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta.content
            if delta:
                parts.append(delta)
        return "".join(parts).strip()
