"""Unified OpenAI-compatible LLM client for the agent loop.

All LLM calls in the agent loop (SpecExtractor / Modeler / Repair / Judge adapter /
NL summary / baseline replication) MUST go through this module. This is the sole
place in the codebase that instantiates an ``OpenAI`` client.

Environment contract
--------------------

Three environment variables MUST be set (typically by ``source .env`` in shell
before running any method script):

- ``LLM_ENDPOINT``: OpenAI-compatible proxy base URL (e.g.
  ``https://sub2api-new-api.deepghs.org/``)
- ``LLM_API_KEY``: Bearer token for the proxy
- ``LLM_MODEL``: Default model name to call (e.g. ``gpt-5.5``)
- ``LLM_REQUEST_TIMEOUT_SECONDS``: Optional request timeout. Defaults to
  ``600`` seconds so provider/proxy hangs become retryable provider failures
  instead of stalling long PR-E1 experiments forever. Set to ``0`` or
  ``none`` to disable the explicit timeout for one-off diagnostics.

The code reads these via ``os.environ`` only — **the ``.env`` file is never
read directly**. Switching the active model is done by editing ``.env`` and
re-sourcing it; the code does not change.

Fail-loudly philosophy
----------------------

Missing env vars raise ``KeyError`` immediately. There is no silent fallback
because a silent default would let one run accidentally mix LLM_MODEL between
samples, which would invalidate the experiment.
"""

from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI

DEFAULT_REQUEST_TIMEOUT_SECONDS = 600.0
DEFAULT_SDK_MAX_RETRIES = 0


def get_request_timeout_seconds() -> float | None:
    """Return the OpenAI client request timeout from process env.

    This timeout is intentionally separate from output length: ``max_tokens``
    stays unset unless callers explicitly pass it.  The timeout only prevents
    provider/proxy sockets from hanging forever, which would otherwise make
    invalid infrastructure failures indistinguishable from slow experiments.
    """

    raw = os.environ.get("LLM_REQUEST_TIMEOUT_SECONDS")
    if raw is None or not raw.strip():
        return DEFAULT_REQUEST_TIMEOUT_SECONDS
    value = raw.strip().lower()
    if value in {"0", "none", "null", "off", "false", "disabled"}:
        return None
    try:
        timeout = float(value)
    except ValueError as exc:
        raise ValueError("LLM_REQUEST_TIMEOUT_SECONDS must be a positive number, 0, or none") from exc
    if timeout <= 0:
        return None
    return timeout


def get_llm_client() -> OpenAI:
    """Return an OpenAI-compatible client bound to ``LLM_ENDPOINT`` + ``LLM_API_KEY``.

    The proxy at ``LLM_ENDPOINT`` is expected to expose the standard OpenAI
    ``/v1/chat/completions`` path. The OpenAI SDK appends ``/v1/...`` to the
    base URL automatically, so ``LLM_ENDPOINT`` should be the proxy root (e.g.
    ``https://sub2api-new-api.deepghs.org/``).

    Raises
    ------
    KeyError
        If ``LLM_ENDPOINT`` or ``LLM_API_KEY`` is not set in ``os.environ``.
        Run ``source .env`` in your shell first.
    """
    endpoint = os.environ["LLM_ENDPOINT"]  # noqa: SIM112 — raise on missing
    api_key = os.environ["LLM_API_KEY"]

    # OpenAI SDK requires base_url to end in /v1 OR no /v1 (it will append).
    # Normalize: if user gave a path that already has /v1 keep it; else append v1.
    base_url = endpoint.rstrip("/")
    if not base_url.endswith("/v1"):
        base_url = base_url + "/v1"

    # The agent loop already has auditable stage-level retry records
    # (``LoopConfig.llm_max_retries``).  The OpenAI SDK default is another
    # hidden retry layer, which can multiply provider/proxy 50x or timeout
    # stalls and leave PR-E1 evidence without a precise failing stage.  Keep the
    # transport client fail-fast and let the loop record every retry attempt.
    timeout = get_request_timeout_seconds()
    if timeout is None:
        return OpenAI(base_url=base_url, api_key=api_key, max_retries=DEFAULT_SDK_MAX_RETRIES)
    return OpenAI(base_url=base_url, api_key=api_key, timeout=timeout, max_retries=DEFAULT_SDK_MAX_RETRIES)


def get_default_model() -> str:
    """Return the default LLM model from ``LLM_MODEL`` env var.

    Raises
    ------
    KeyError
        If ``LLM_MODEL`` is not set. Run ``source .env`` first.
    """
    return os.environ["LLM_MODEL"]


def chat(
    *,
    messages: list[dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.0,
    max_tokens: Optional[int] = None,
    seed: Optional[int] = None,
    response_format: Optional[dict] = None,
) -> tuple[str, dict]:
    """One-shot chat completion with token usage tracking.

    Parameters
    ----------
    messages
        OpenAI-style messages list (``[{"role": "...", "content": "..."}, ...]``).
    model
        Override the default ``LLM_MODEL`` env var. ``None`` uses env default.
    temperature
        Sampling temperature. Default 0.0 for reproducibility.
    max_tokens
        Optional output cap.
    seed
        Optional integer seed (some providers honor this for determinism).
    response_format
        Optional ``{"type": "json_object"}`` to force JSON output.

    Returns
    -------
    (content, usage)
        ``content``: assistant message string.
        ``usage``: ``{"prompt_tokens": int, "completion_tokens": int, "total_tokens": int, "model": str}``.
    """
    client = get_llm_client()
    actual_model = model or get_default_model()

    kwargs: dict = {
        "model": actual_model,
        "messages": messages,
        "temperature": temperature,
    }
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens
    if seed is not None:
        kwargs["seed"] = seed
    if response_format is not None:
        kwargs["response_format"] = response_format

    resp = client.chat.completions.create(**kwargs)
    content = resp.choices[0].message.content or ""
    usage = {
        "prompt_tokens": getattr(resp.usage, "prompt_tokens", 0),
        "completion_tokens": getattr(resp.usage, "completion_tokens", 0),
        "total_tokens": getattr(resp.usage, "total_tokens", 0),
        "model": actual_model,
    }
    return content, usage
