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

from contextlib import contextmanager
import os
import signal
import sys
import threading
import time
from typing import Any, Optional

from openai import OpenAI

DEFAULT_REQUEST_TIMEOUT_SECONDS = 600.0
DEFAULT_SDK_MAX_RETRIES = 0
DEFAULT_STREAM_PROGRESS_INTERVAL_SECONDS = 5.0
DEFAULT_STREAM_PROGRESS_CHUNK_INTERVAL = 512


class LLMRequestTimeoutError(TimeoutError):
    """Raised when the repo-level LLM request deadline expires."""


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


def _env_bool(name: str, *, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    value = raw.strip().lower()
    if value in {"1", "true", "yes", "y", "on", "enabled"}:
        return True
    if value in {"0", "false", "no", "n", "off", "disabled"}:
        return False
    raise ValueError(f"{name} must be a boolean-like value")


def get_stream_enabled() -> bool:
    """Return whether chat completions should use streaming.

    PR-E1 real runs found that stream mode can keep proxy/Cloudflare chains
    alive during long structured generations.  Therefore streaming is the
    default; set ``LLM_STREAM=false`` only for an explicit diagnostic/control
    run.
    """

    return _env_bool("LLM_STREAM", default=True)


def get_progress_log_enabled() -> bool:
    """Return whether provider progress should be printed to stdout.

    These messages are intentionally prompt-safe: they include sizes, stage-less
    timing and model identifiers, but never API keys, full prompts or raw model
    outputs.  PR-E1 wrappers capture stdout with ``tee``/files so this becomes
    operator-facing evidence of request progress.
    """

    return _env_bool("LLM_PROGRESS_LOG", default=True)


def _prompt_char_count(messages: list[dict[str, str]]) -> int:
    total = 0
    for message in messages:
        content = message.get("content", "")
        total += len(content if isinstance(content, str) else str(content))
    return total


def _emit_progress(message: str) -> None:
    if not get_progress_log_enabled():
        return
    print(message, file=sys.stdout, flush=True)


def _safe_choice_delta_content(chunk: Any) -> str:
    choices = getattr(chunk, "choices", None)
    if not choices:
        return ""
    first = choices[0]
    delta = getattr(first, "delta", None)
    content = getattr(delta, "content", None) if delta is not None else None
    if content is None and isinstance(delta, dict):
        content = delta.get("content")
    if content is None:
        return ""
    return str(content)


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


@contextmanager
def _request_deadline(timeout_seconds: float | None):
    """Apply a repo-level hard deadline around a single provider request.

    OpenAI/httpx timeouts are still passed to the SDK, but PR-E1 real runs have
    shown that a local proxy/socket chain may remain parked in ``poll`` longer
    than the SDK timeout.  A POSIX alarm gives the experiment an outer,
    auditable fail-fast boundary so provider infrastructure failures are
    persisted as LLM-stage ``provider_error`` attempts instead of leaving the
    whole run without a record.

    The alarm is only installed in the main thread, which is the normal mode
    for the per-case PR-E1 worker processes.  In other contexts we fall back to
    the SDK timeout to avoid unsafe cross-thread signal handling.
    """

    if timeout_seconds is None or timeout_seconds <= 0:
        yield
        return
    if threading.current_thread() is not threading.main_thread() or not hasattr(signal, "SIGALRM"):
        yield
        return

    def _handle_timeout(signum: int, frame: object) -> None:  # noqa: ARG001
        raise LLMRequestTimeoutError(f"LLM provider request exceeded {timeout_seconds:g} seconds")

    old_handler = signal.getsignal(signal.SIGALRM)
    old_timer = signal.getitimer(signal.ITIMER_REAL)
    signal.signal(signal.SIGALRM, _handle_timeout)
    signal.setitimer(signal.ITIMER_REAL, timeout_seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, old_timer[0], old_timer[1])
        signal.signal(signal.SIGALRM, old_handler)


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

    prompt_chars = _prompt_char_count(messages)
    timeout_seconds = get_request_timeout_seconds()
    stream_enabled = get_stream_enabled()
    started = time.monotonic()
    _emit_progress(
        "[llm] request start "
        f"model={actual_model} stream={stream_enabled} messages={len(messages)} "
        f"prompt_chars={prompt_chars} timeout={timeout_seconds if timeout_seconds is not None else 'none'} "
        f"max_tokens={max_tokens if max_tokens is not None else 'unset'}"
    )

    if stream_enabled:
        chunks: list[str] = []
        chunk_count = 0
        first_chunk_seconds: float | None = None
        completion_chars = 0
        last_progress_at = started
        try:
            with _request_deadline(timeout_seconds):
                stream = client.chat.completions.create(stream=True, **kwargs)
                for chunk in stream:
                    chunk_count += 1
                    delta = _safe_choice_delta_content(chunk)
                    if delta:
                        if first_chunk_seconds is None:
                            first_chunk_seconds = time.monotonic() - started
                            _emit_progress(
                                "[llm] stream first_chunk "
                                f"model={actual_model} after={first_chunk_seconds:.2f}s"
                            )
                        chunks.append(delta)
                        completion_chars += len(delta)
                    now = time.monotonic()
                    if (
                        now - last_progress_at >= DEFAULT_STREAM_PROGRESS_INTERVAL_SECONDS
                        or chunk_count % DEFAULT_STREAM_PROGRESS_CHUNK_INTERVAL == 0
                    ):
                        _emit_progress(
                            "[llm] stream progress "
                            f"model={actual_model} elapsed={now - started:.1f}s "
                            f"chunks={chunk_count} completion_chars={completion_chars}"
                        )
                        last_progress_at = now
        except Exception as exc:
            _emit_progress(
                "[llm] request error "
                f"model={actual_model} stream=True elapsed={time.monotonic() - started:.1f}s "
                f"error={type(exc).__name__}"
            )
            raise
        elapsed = time.monotonic() - started
        content = "".join(chunks)
        _emit_progress(
            "[llm] stream complete "
            f"model={actual_model} elapsed={elapsed:.1f}s chunks={chunk_count} "
            f"completion_chars={completion_chars}"
        )
        usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "model": actual_model,
            "stream": True,
            "chunk_count": chunk_count,
            "first_chunk_seconds": first_chunk_seconds,
            "elapsed_seconds": elapsed,
            "prompt_chars": prompt_chars,
            "completion_chars": completion_chars,
            "message_count": len(messages),
        }
        return content, usage

    try:
        with _request_deadline(timeout_seconds):
            resp = client.chat.completions.create(**kwargs)
    except Exception as exc:
        _emit_progress(
            "[llm] request error "
            f"model={actual_model} stream=False elapsed={time.monotonic() - started:.1f}s "
            f"error={type(exc).__name__}"
        )
        raise
    content = resp.choices[0].message.content or ""
    elapsed = time.monotonic() - started
    usage = {
        "prompt_tokens": getattr(resp.usage, "prompt_tokens", 0),
        "completion_tokens": getattr(resp.usage, "completion_tokens", 0),
        "total_tokens": getattr(resp.usage, "total_tokens", 0),
        "model": actual_model,
        "stream": False,
        "elapsed_seconds": elapsed,
        "prompt_chars": prompt_chars,
        "completion_chars": len(content),
        "message_count": len(messages),
    }
    _emit_progress(
        "[llm] request complete "
        f"model={actual_model} stream=False elapsed={elapsed:.1f}s completion_chars={len(content)}"
    )
    return content, usage
