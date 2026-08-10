"""PR-B2 real/mock LLM stage execution units.

This module deliberately does **not** implement the full top-down runtime
control flow.  It provides the PR-B2 slice needed by PR-C: reusable execution
units for SL-1 / SL-5 / SL-7 / SL-9 / SL-10B with bounded LLM-layer retry and
self-contained interaction records.

Academic constraints encoded here:

- provider/schema/empty-output failures may retry because they are LLM-layer
  noise rather than model-quality evidence;
- deterministic feedback failures are never retried here and remain PR-B1/PR-C
  runtime decisions;
- every LLM call records prompt, raw output, parsed output, schema validation,
  usage, provider/model, attempts and retry errors;
- records are redacted before they are ready for AgentLoopRunRecord ingestion;
- ``suggested_fix`` in SL-9 is prompt context only, not an instruction to copy.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
import time
from dataclasses import asdict, dataclass, field, is_dataclass
from typing import Any, Callable, Literal, Optional, Protocol

from method.gpt_client import chat as real_env_chat
from method.gpt_client import get_default_model
from method.schema import (
    FixPlan,
    FixRequestBatch,
    GroundingMap,
    ModelReviewFeedback,
    RepairReviewFeedback,
    ReviewRunMeta,
    RevisedFixPlan,
    SL10RepairReviewOutput,
    StageResultMeta,
    TestScenario,
)
from method.stages.ids import STAGE_SPECS_BY_ID, StageId, StageStatus
from method.stages.sl_delta_review_prompt import build_sl10b_delta_review_prompt, parse_sl10b_delta_review_response
from method.stages.sl_initial_modeling_prompt import build_sl1_initial_modeling_prompt, parse_sl1_initial_modeling_response
from method.stages.sl_model_review_prompt import build_sl7_model_review_prompt, parse_sl7_model_review_response
from method.stages.sl_repair_prompt import build_sl9_repair_prompt
from method.stages.sl10_repair_review_prompt import build_sl10_repair_review_prompt, parse_sl10_repair_review_response
from method.stages.sl_scenario_generation_prompt import build_sl5_scenario_generation_prompt, parse_sl5_scenario_generation_response
from method.stages.sl_prompt_common import strip_fence


SECRET_TEXT_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "env_secret_assignment",
        re.compile(
            r"\b(?:LLM_API_KEY|OPENAI_API_KEY|ANTHROPIC_API_KEY|API_KEY|TOKEN|PASSWORD|PASSWD|SECRET|AUTHORIZATION)"
            r"\s*[:=]\s*\\?[\'\"]?[^\s`\'\"<>\\]{8,}\\?[\'\"]?",
            re.IGNORECASE,
        ),
    ),
    ("openai_api_key", re.compile(r"sk-[A-Za-z0-9][A-Za-z0-9_-]{7,}")),
    ("github_oauth_token", re.compile(r"gh[opsur]_[A-Za-z0-9_]{8,}")),
    ("github_pat", re.compile(r"github_pat_[A-Za-z0-9_]{8,}")),
    ("bearer_token", re.compile(r"Bearer\s+[A-Za-z0-9._\-]{12,}", re.IGNORECASE)),
)
SECRET_FIELD_EXACT_KEYS = {
    "api_key",
    "apikey",
    "token",
    "password",
    "passwd",
    "secret",
    "authorization",
    "access_token",
    "refresh_token",
    "bearer_token",
    "llm_api_key",
    "openai_api_key",
    "anthropic_api_key",
}
SECRET_FIELD_SUFFIXES = ("_api_key", "_token", "_password", "_passwd", "_secret", "_authorization")


def _stage_progress_enabled() -> bool:
    raw = os.environ.get("AGENT_LOOP_PROGRESS_LOG", os.environ.get("LLM_PROGRESS_LOG", "true"))
    return str(raw).strip().lower() not in {"0", "false", "no", "off", "disabled"}


def _stage_progress(stage_id: StageId, message: str, **payload: Any) -> None:
    if not _stage_progress_enabled():
        return
    safe = " ".join(
        f"{key}={str(value).replace(chr(10), ' ')[:180]}"
        for key, value in payload.items()
        if value is not None
    )
    print(f"[agent-loop][{stage_id.value}] {message}" + (f" {safe}" if safe else ""), file=sys.stdout, flush=True)


@dataclass
class LLMStageConfig:
    """Provider/retry contract for one PR-B2 LLM stage call."""

    provider_mode: str = "real_env"
    model: Optional[str] = None
    temperature: float = 0.0
    seed: Optional[int] = None
    max_tokens: Optional[int] = None
    max_prompt_tokens: Optional[int] = 128_000
    prompt_token_estimator: str = "chars_per_token"
    prompt_chars_per_token: float = 4.0
    max_retries: int = 2
    record_prompts: bool = True
    record_raw_outputs: bool = True
    redact_secrets: bool = True

    def __post_init__(self) -> None:
        if self.provider_mode not in {"real_env", "mock"}:
            raise ValueError("LLMStageConfig.provider_mode must be real_env or mock")
        if not isinstance(self.max_retries, int) or isinstance(self.max_retries, bool) or self.max_retries < 0:
            raise ValueError("LLMStageConfig.max_retries must be a non-negative int")
        if self.max_tokens is not None and self.max_tokens <= 0:
            raise ValueError("LLMStageConfig.max_tokens must be positive when provided")
        if self.max_prompt_tokens is not None and self.max_prompt_tokens <= 0:
            raise ValueError("LLMStageConfig.max_prompt_tokens must be positive when provided")
        if self.prompt_token_estimator not in {"chars_per_token", "tiktoken_optional"}:
            raise ValueError("LLMStageConfig.prompt_token_estimator must be chars_per_token or tiktoken_optional")
        if self.prompt_chars_per_token <= 0:
            raise ValueError("LLMStageConfig.prompt_chars_per_token must be positive")
        if self.temperature < 0:
            raise ValueError("LLMStageConfig.temperature must be >= 0")


class ChatProvider(Protocol):
    """Small provider protocol used by PR-B2 stage units."""

    @property
    def provider_name(self) -> str:
        ...

    @property
    def model_id(self) -> str:
        ...

    def chat(
        self,
        *,
        messages: list[dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        seed: Optional[int] = None,
        response_format: Optional[dict[str, Any]] = None,
    ) -> tuple[str, dict[str, Any], str]:
        ...


@dataclass
class MockLLMProvider:
    """Deterministic mock provider for PR-B2 TDD tests.

    ``errors`` and ``responses`` are consumed attempt-by-attempt.  Errors are
    consumed before responses so a test can model transient provider failures.
    """

    responses: list[str] = field(default_factory=list)
    errors: list[Exception] = field(default_factory=list)
    provider_name: str = "mock"
    model_id: str = "mock-model"
    calls: list[dict[str, Any]] = field(default_factory=list)

    @property
    def call_count(self) -> int:
        return len(self.calls)

    def chat(
        self,
        *,
        messages: list[dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        seed: Optional[int] = None,
        response_format: Optional[dict[str, Any]] = None,
    ) -> tuple[str, dict[str, Any], str]:
        self.calls.append(
            {
                "messages": messages,
                "model": model,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "seed": seed,
                "response_format": response_format,
            }
        )
        if self.errors:
            raise self.errors.pop(0)
        if not self.responses:
            return "", {"prompt_tokens": 1, "completion_tokens": 0, "total_tokens": 1, "model": model or self.model_id}, model or self.model_id
        content = self.responses.pop(0)
        usage = {"prompt_tokens": 1, "completion_tokens": 1 if content else 0, "total_tokens": 2 if content else 1, "model": model or self.model_id}
        return content, usage, model or self.model_id


class RealEnvLLMProvider:
    """OpenAI-compatible provider backed by ``method.gpt_client``.

    The provider reads environment variables only through ``gpt_client``.  It
    never reads a ``.env`` file directly.
    """

    provider_name = "openai-compatible-env"

    @property
    def model_id(self) -> str:
        try:
            return get_default_model()
        except Exception:
            return "env:LLM_MODEL"

    def chat(
        self,
        *,
        messages: list[dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        seed: Optional[int] = None,
        response_format: Optional[dict[str, Any]] = None,
    ) -> tuple[str, dict[str, Any], str]:
        content, usage = real_env_chat(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            seed=seed,
            response_format=response_format,
        )
        return content, usage, str(usage.get("model") or model or self.model_id)


@dataclass
class LLMStageRun:
    """Result of one PR-B2 LLM stage unit."""

    stage_id: str
    ok: bool
    parsed_output: Any
    interaction: dict[str, Any]
    stage_meta: StageResultMeta
    feedback: Any = None
    redaction_report: list[dict[str, Any]] = field(default_factory=list)


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(v) for v in value]
    if is_dataclass(value) and not isinstance(value, type):
        return _jsonable(asdict(value))
    return str(value)


def _hash_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _hash_payload(value: Any) -> str:
    return _hash_text(json.dumps(_jsonable(value), ensure_ascii=False, sort_keys=True, default=str))


def _prompt_char_count(messages: list[dict[str, str]]) -> int:
    return sum(len(str(message.get("content", ""))) for message in messages)


def estimate_prompt_tokens(
    messages: list[dict[str, str]],
    *,
    estimator: str = "chars_per_token",
    chars_per_token: float = 4.0,
    model: str | None = None,
) -> int:
    """Lightweight pre-request prompt-token estimate for budget gating.

    The default intentionally mirrors ``method.gpt_client``'s chars/4 proxy so
    PR-E1 does not gain a hard dependency on tokenizer packages.  If a local
    environment already has ``tiktoken`` and explicitly asks for
    ``tiktoken_optional``, use it as a best-effort estimate; otherwise fall back
    to the same chars-per-token calculation.
    """

    prompt_chars = _prompt_char_count(messages)
    if estimator == "tiktoken_optional":
        try:
            import tiktoken  # type: ignore[import-not-found]

            try:
                encoding = tiktoken.encoding_for_model(model or "")
            except Exception:
                encoding = tiktoken.get_encoding("cl100k_base")
            # Chat message framing differs by model/provider; add a small
            # per-message overhead while keeping the estimate lightweight.
            return sum(len(encoding.encode(str(message.get("content", "")))) + 4 for message in messages) + 2
        except Exception:
            pass
    return int(math.ceil(max(0, prompt_chars) / chars_per_token))


def _redaction_placeholder(secret: str, reason: str) -> str:
    digest = hashlib.sha256(secret.encode("utf-8")).hexdigest()[:16]
    return f"<redacted:{reason}:sha256:{digest}>"


def _redaction_report_item(path: str, *, reason: str, replacement: str, affects_replay: bool) -> dict[str, Any]:
    return {
        "field_path": path,
        "reason": reason,
        "replacement": replacement,
        "affects_replay": affects_replay,
    }


def _redact_text(value: str, path: str, report: list[dict[str, Any]], *, affects_replay: bool) -> str:
    redacted = value
    for reason, pattern in SECRET_TEXT_PATTERNS:

        def repl(match: re.Match[str]) -> str:
            replacement = _redaction_placeholder(match.group(0), reason)
            report.append(_redaction_report_item(path, reason=reason, replacement=replacement, affects_replay=affects_replay))
            return replacement

        redacted = pattern.sub(repl, redacted)
    return redacted


def _is_secret_field_key(key_text: str) -> bool:
    """Return True for field names that semantically carry credentials.

    Keep this narrower than a substring match: audit metadata such as
    ``prompt_tokens`` / ``total_tokens`` must remain numeric for replay and cost
    accounting, while fields like ``openai_api_key`` or ``access_token`` must be
    removed from public run records.
    """

    normalized = re.sub(r"[^a-z0-9]+", "_", key_text.lower()).strip("_")
    return normalized in SECRET_FIELD_EXACT_KEYS or normalized.endswith(SECRET_FIELD_SUFFIXES)


def _redact_payload(value: Any, path: str, report: list[dict[str, Any]], *, affects_replay: bool = True) -> Any:
    if isinstance(value, str):
        return _redact_text(value, path, report, affects_replay=affects_replay)
    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            item_path = f"{path}.{key_text}" if path else key_text
            if _is_secret_field_key(key_text):
                secret_material = item if isinstance(item, str) else json.dumps(_jsonable(item), ensure_ascii=False, sort_keys=True, default=str)
                replacement = _redaction_placeholder(str(secret_material), "secret_field")
                report.append(_redaction_report_item(item_path, reason="secret_field", replacement=replacement, affects_replay=affects_replay))
                redacted[key_text] = replacement
            else:
                redacted[key_text] = _redact_payload(item, item_path, report, affects_replay=affects_replay)
        return redacted
    if isinstance(value, (list, tuple)):
        return [_redact_payload(item, f"{path}[{i}]", report, affects_replay=affects_replay) for i, item in enumerate(value)]
    return value


def redact_run_record_payload(
    value: Any,
    *,
    path: str = "run_record",
    affects_replay: bool = True,
) -> tuple[Any, list[dict[str, Any]]]:
    """Redact secrets from non-LLM run-record surfaces.

    PR-B2 already redacts each LLM interaction before it is appended to the run
    record.  PR-C also stores raw NL, final DSL, repair history and logs in the
    self-contained ``AgentLoopRunRecord``.  Those surfaces may accidentally
    contain copied credentials (for example a user pasting ``LLM_API_KEY=...``
    into NL), so expose the same redaction policy for the runtime driver.
    """

    report: list[dict[str, Any]] = []
    return _redact_payload(value, path, report, affects_replay=affects_replay), report


def _stage_meta(stage_id: StageId, *, ok: bool, raw_output: str, prompt_messages: list[dict[str, str]], validation_error: str | None = None) -> StageResultMeta:
    spec = STAGE_SPECS_BY_ID[stage_id.value]
    if ok:
        status = StageStatus.OK
    else:
        status = StageStatus.ERROR
    return StageResultMeta(
        stage_id=stage_id.value,
        stage_kind=spec.kind,
        enabled=True,
        ran=True,
        status=status,
        ok=ok,
        stage_error=validation_error if not ok else None,
        output_validation_error=validation_error,
        input_hash=_hash_payload(prompt_messages),
        prompt_hash=_hash_payload(prompt_messages),
        output_hash=_hash_text(raw_output or validation_error or ""),
    )


def _review_meta(
    *,
    stage_id: StageId,
    provider_name: str,
    model_id: str,
    prompt_template_version: str,
    prompt_messages: list[dict[str, str]],
    raw_output: str,
    parsed_schema_version: str,
    schema_ok: bool,
    validation_error: str | None,
    config: LLMStageConfig,
    retry_count: int,
    failure_policy: Literal["fail_open", "fail_closed", "audit_only"] = "fail_closed",
) -> ReviewRunMeta:
    return ReviewRunMeta(
        provider=provider_name,
        model_id=model_id,
        resolved_model_id=model_id,
        prompt_template_version=prompt_template_version,
        prompt_hash=_hash_payload(prompt_messages),
        input_hash=_hash_payload(prompt_messages),
        temperature=config.temperature,
        seed=config.seed,
        retry_count=retry_count,
        raw_output_hash=_hash_text(raw_output or validation_error or ""),
        raw_output_path=None,
        parsed_schema_version=parsed_schema_version,
        schema_validation_ok=schema_ok,
        schema_validation_error=validation_error,
        cache_key=f"{stage_id.value}:{_hash_payload(prompt_messages)}",
        decision_threshold=None,
        failure_policy=failure_policy,
        replay_key=f"{stage_id.value}:{_hash_payload(prompt_messages)}",
    )


def _provider_for(config: LLMStageConfig, provider: Optional[ChatProvider]) -> ChatProvider:
    if provider is not None:
        return provider
    if config.provider_mode == "mock":
        return MockLLMProvider(model_id=config.model or "mock-model")
    return RealEnvLLMProvider()


def _attempt_payload(
    *,
    stage_id: StageId,
    attempt_index: int,
    status: str,
    raw_output: str,
    parsed_output: Any,
    usage: dict[str, Any],
    model_id: str,
    provider_name: str,
    error_kind: str | None = None,
    error_message: str | None = None,
    elapsed_seconds: float | None = None,
) -> dict[str, Any]:
    payload = {
        "stage_id": stage_id.value,
        "attempt_index": attempt_index,
        "status": status,
        "schema_validation_ok": status == "ok",
        "error_kind": error_kind,
        "error_message": error_message,
        "raw_output_hash": _hash_text(raw_output or error_message or ""),
        "raw_output": raw_output,
        "parsed_output": _jsonable(parsed_output),
        "usage": _jsonable(usage),
        "model_id": model_id,
        "provider": provider_name,
    }
    if elapsed_seconds is not None:
        payload["elapsed_seconds"] = elapsed_seconds
    return payload


def _redaction_failed_message(exc: Exception) -> str:
    return f"LLM interaction redaction failed fail-closed: {type(exc).__name__}"


def _redaction_failed_report(field_path: str) -> dict[str, Any]:
    return {
        "field_path": field_path,
        "reason": "redaction_failed",
        "replacement": "<omitted:redaction_failed>",
        "affects_replay": True,
    }


def _safe_usage_summary(usage: dict[str, Any]) -> dict[str, Any]:
    """Whitelist provider usage fields that are safe without a redactor."""

    safe: dict[str, Any] = {}
    for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
        value = usage.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            safe[key] = value
    model = usage.get("model")
    if isinstance(model, str):
        safe["model_hash"] = _hash_text(model)
    return safe


def _redaction_failed_stage_run(
    *,
    stage_id: StageId,
    prompt_template_version: str,
    prompt_messages: list[dict[str, str]],
    parsed_schema_version: str,
    config: LLMStageConfig,
    provider_name: str,
    model_id: str,
    raw_output: str,
    attempts: list[dict[str, Any]],
    usage: dict[str, Any],
    failure_policy: Literal["fail_open", "fail_closed", "audit_only"],
    field_path: str,
    exc: Exception,
) -> LLMStageRun:
    """Return a minimal safe failed stage run when redaction itself crashes.

    PR-C treats redaction failures as audit failures, not as ordinary
    best-effort logging warnings.  This helper intentionally discards prompt,
    raw-output, parsed-output and attempt payload surfaces, preserving only
    hashes and provider/model metadata so the runtime can still write a
    secret-safe invalid run record.
    """

    message = _redaction_failed_message(exc)
    retry_count = max(0, len(attempts) - 1)
    meta = _stage_meta(
        stage_id,
        ok=False,
        raw_output=raw_output,
        prompt_messages=prompt_messages,
        validation_error=message,
    )
    review_meta = _review_meta(
        stage_id=stage_id,
        provider_name=provider_name,
        model_id=model_id,
        prompt_template_version=prompt_template_version,
        prompt_messages=prompt_messages,
        raw_output=raw_output,
        parsed_schema_version=parsed_schema_version,
        schema_ok=False,
        validation_error=message,
        config=config,
        retry_count=retry_count,
        failure_policy=failure_policy,
    )
    interaction = {
        "stage_id": stage_id.value,
        "provider": provider_name,
        "model_id": model_id,
        "resolved_model_id": model_id,
        "prompt_template_version": prompt_template_version,
        "prompt_hash": review_meta.prompt_hash,
        "input_hash": review_meta.input_hash,
        "temperature": config.temperature,
        "seed": config.seed,
        "retry_count": retry_count,
        "raw_output_hash": review_meta.raw_output_hash,
        "raw_output_path": None,
        "parsed_schema_version": parsed_schema_version,
        "prompt_messages_omitted": "redaction_failed",
        "raw_output_omitted": "redaction_failed",
        "parsed_output_omitted": "redaction_failed",
        "attempt_count": len(attempts),
        "schema_validation_ok": False,
        "schema_validation_error": message,
        "usage": _safe_usage_summary(usage),
        "retry_error": {
            "error_kind": "redaction_failed",
            "error_message": message,
        },
        "review_meta": asdict(review_meta),
        "provider_mode": config.provider_mode,
        "real_llm_provider_api": config.provider_mode == "real_env",
        "redaction_failed": True,
        "redaction_failure_path": field_path,
        "omitted": "redaction_failed",
        "llm_retry_scope": "provider/network/schema/empty-output only; deterministic feedback is not retried here",
    }
    return LLMStageRun(
        stage_id=stage_id.value,
        ok=False,
        parsed_output={},
        interaction=interaction,
        stage_meta=meta,
        redaction_report=[_redaction_failed_report(field_path)],
    )


def _mark_stage_run_redaction_failed(
    run: LLMStageRun,
    *,
    stage_id: StageId,
    field_path: str,
    exc: Exception,
) -> LLMStageRun:
    """Fail-close an already-created LLMStageRun after adapter reshaping fails."""

    message = _redaction_failed_message(exc)
    run.ok = False
    run.parsed_output = {}
    run.stage_meta.ok = False
    run.stage_meta.status = StageStatus.ERROR
    run.stage_meta.stage_error = message
    run.stage_meta.output_validation_error = message

    old_interaction = dict(run.interaction or {})
    review_meta = old_interaction.get("review_meta")
    if isinstance(review_meta, dict):
        review_meta = {
            **review_meta,
            "schema_validation_ok": False,
            "schema_validation_error": message,
            "failure_policy": review_meta.get("failure_policy", "fail_closed"),
        }
    safe_interaction = {
        "stage_id": stage_id.value,
        "provider": old_interaction.get("provider", "<unknown>"),
        "model_id": old_interaction.get("model_id", "<unknown>"),
        "resolved_model_id": old_interaction.get("resolved_model_id", old_interaction.get("model_id", "<unknown>")),
        "prompt_template_version": old_interaction.get("prompt_template_version"),
        "prompt_hash": old_interaction.get("prompt_hash"),
        "input_hash": old_interaction.get("input_hash"),
        "temperature": old_interaction.get("temperature"),
        "seed": old_interaction.get("seed"),
        "retry_count": old_interaction.get("retry_count", 0),
        "raw_output_hash": old_interaction.get("raw_output_hash"),
        "raw_output_path": None,
        "parsed_schema_version": old_interaction.get("parsed_schema_version"),
        "prompt_messages_omitted": "redaction_failed",
        "raw_output_omitted": "redaction_failed",
        "parsed_output_omitted": "redaction_failed",
        "attempt_count": len(old_interaction.get("attempts", []) or []),
        "schema_validation_ok": False,
        "schema_validation_error": message,
        "retry_error": {
            "error_kind": "redaction_failed",
            "error_message": message,
        },
        "review_meta": review_meta,
        "provider_mode": old_interaction.get("provider_mode"),
        "real_llm_provider_api": old_interaction.get("real_llm_provider_api"),
        "redaction_failed": True,
        "redaction_failure_path": field_path,
        "omitted": "redaction_failed",
        "llm_retry_scope": old_interaction.get("llm_retry_scope"),
    }
    run.interaction = {key: value for key, value in safe_interaction.items() if value is not None}
    run.redaction_report.append(_redaction_failed_report(field_path))
    return run


def _run_llm_stage(
    *,
    stage_id: StageId,
    prompt_template_version: str,
    prompt_messages: list[dict[str, str]],
    parser: Callable[[str], Any],
    parsed_schema_version: str,
    config: LLMStageConfig,
    provider: Optional[ChatProvider] = None,
    response_format: Optional[dict[str, Any]] = None,
    empty_output_invalid: bool = True,
    failure_policy: Literal["fail_open", "fail_closed", "audit_only"] = "fail_closed",
) -> LLMStageRun:
    chat_provider = _provider_for(config, provider)
    attempts: list[dict[str, Any]] = []
    last_raw = ""
    last_usage: dict[str, Any] = {}
    last_model_id = config.model or getattr(chat_provider, "model_id", "")
    last_error: str | None = None
    last_error_kind: str | None = None
    parsed: Any = {}
    schema_ok = False
    prompt_chars = _prompt_char_count(prompt_messages)
    estimated_prompt_tokens = estimate_prompt_tokens(
        prompt_messages,
        estimator=config.prompt_token_estimator,
        chars_per_token=config.prompt_chars_per_token,
        model=last_model_id,
    )
    prompt_budget = config.max_prompt_tokens

    for attempt_index in range(config.max_retries + 1):
        attempt_started = time.monotonic()
        _stage_progress(
            stage_id,
            "attempt_start",
            attempt=f"{attempt_index}/{config.max_retries}",
            provider=chat_provider.provider_name,
            model=last_model_id,
            prompt_chars=prompt_chars,
            estimated_prompt_tokens=estimated_prompt_tokens,
            prompt_budget=prompt_budget,
            response_format=response_format.get("type") if isinstance(response_format, dict) else None,
        )
        try:
            raw_output, usage, model_id = chat_provider.chat(
                messages=prompt_messages,
                model=config.model,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                seed=config.seed,
                response_format=response_format,
            )
            last_raw = raw_output
            last_usage = usage
            last_model_id = model_id
        except Exception as exc:  # provider/network/timeout/rate-limit are provider-layer here.
            elapsed = time.monotonic() - attempt_started
            last_error_kind = "provider_error"
            last_error = f"provider failure: {type(exc).__name__}: {str(exc)[:300]}"
            _stage_progress(stage_id, "attempt_provider_error", attempt=attempt_index, elapsed=f"{elapsed:.2f}s", error=last_error)
            attempts.append(
                _attempt_payload(
                    stage_id=stage_id,
                    attempt_index=attempt_index,
                    status="provider_error",
                    raw_output="",
                    parsed_output={"error": last_error},
                    usage={},
                    model_id=last_model_id,
                    provider_name=chat_provider.provider_name,
                    error_kind=last_error_kind,
                    error_message=last_error,
                    elapsed_seconds=elapsed,
                )
            )
            continue

        if empty_output_invalid and not raw_output.strip():
            elapsed = time.monotonic() - attempt_started
            last_error_kind = "empty_output"
            last_error = "empty LLM output"
            _stage_progress(stage_id, "attempt_empty_output", attempt=attempt_index, elapsed=f"{elapsed:.2f}s")
            attempts.append(
                _attempt_payload(
                    stage_id=stage_id,
                    attempt_index=attempt_index,
                    status="empty_output",
                    raw_output=raw_output,
                    parsed_output={"error": last_error},
                    usage=usage,
                    model_id=model_id,
                    provider_name=chat_provider.provider_name,
                    error_kind=last_error_kind,
                    error_message=last_error,
                    elapsed_seconds=elapsed,
                )
            )
            continue

        try:
            parsed = parser(raw_output)
            schema_ok = True
            last_error = None
            last_error_kind = None
            elapsed = time.monotonic() - attempt_started
            _stage_progress(
                stage_id,
                "attempt_schema_ok",
                attempt=attempt_index,
                elapsed=f"{elapsed:.2f}s",
                raw_chars=len(raw_output),
                usage=_jsonable(usage),
            )
            attempts.append(
                _attempt_payload(
                    stage_id=stage_id,
                    attempt_index=attempt_index,
                    status="ok",
                    raw_output=raw_output,
                    parsed_output=parsed,
                    usage=usage,
                    model_id=model_id,
                    provider_name=chat_provider.provider_name,
                    elapsed_seconds=elapsed,
                )
            )
            break
        except Exception as exc:
            elapsed = time.monotonic() - attempt_started
            last_error_kind = "schema_invalid"
            last_error = f"schema invalid: {type(exc).__name__}: {str(exc)[:300]}"
            _stage_progress(stage_id, "attempt_schema_invalid", attempt=attempt_index, elapsed=f"{elapsed:.2f}s", raw_chars=len(raw_output), error=last_error)
            attempts.append(
                _attempt_payload(
                    stage_id=stage_id,
                    attempt_index=attempt_index,
                    status="schema_invalid",
                    raw_output=raw_output,
                    parsed_output={"error": last_error},
                    usage=usage,
                    model_id=model_id,
                    provider_name=chat_provider.provider_name,
                    error_kind=last_error_kind,
                    error_message=last_error,
                    elapsed_seconds=elapsed,
                )
            )

    retry_count = max(0, len(attempts) - 1)
    retry_error: dict[str, str] | None = None if schema_ok else {"error_kind": last_error_kind or "unknown", "error_message": last_error or "unknown LLM failure"}
    validation_error = None if schema_ok or retry_error is None else retry_error["error_message"]
    meta = _stage_meta(stage_id, ok=schema_ok, raw_output=last_raw, prompt_messages=prompt_messages, validation_error=validation_error)
    review_meta = _review_meta(
        stage_id=stage_id,
        provider_name=chat_provider.provider_name,
        model_id=last_model_id,
        prompt_template_version=prompt_template_version,
        prompt_messages=prompt_messages,
        raw_output=last_raw,
        parsed_schema_version=parsed_schema_version,
        schema_ok=schema_ok,
        validation_error=validation_error,
        config=config,
        retry_count=retry_count,
        failure_policy=failure_policy,
    )
    prompt_messages_payload = prompt_messages if config.record_prompts else []
    raw_output_payload = last_raw if config.record_raw_outputs else ""
    interaction = {
        "stage_id": stage_id.value,
        "provider": chat_provider.provider_name,
        "model_id": last_model_id,
        "resolved_model_id": last_model_id,
        "prompt_template_version": prompt_template_version,
        "prompt_hash": review_meta.prompt_hash,
        "input_hash": review_meta.input_hash,
        "temperature": config.temperature,
        "seed": config.seed,
        "retry_count": retry_count,
        "raw_output_hash": review_meta.raw_output_hash,
        "raw_output_path": None,
        "parsed_schema_version": parsed_schema_version,
        "prompt_messages": prompt_messages_payload,
        "raw_output": raw_output_payload,
        "parsed_output": _jsonable(parsed),
        "schema_validation_ok": schema_ok,
        "schema_validation_error": review_meta.schema_validation_error,
        "usage": _jsonable(last_usage),
        "prompt_chars": prompt_chars,
        "estimated_prompt_tokens": estimated_prompt_tokens,
        "prompt_token_budget": prompt_budget,
        "prompt_token_estimator": config.prompt_token_estimator,
        "chars_per_token_estimate": config.prompt_chars_per_token,
        "prompt_budget_exceeded_before_request": (
            estimated_prompt_tokens > prompt_budget if prompt_budget is not None else False
        ),
        "attempts": attempts,
        "retry_error": retry_error,
        "review_meta": asdict(review_meta),
        "provider_mode": config.provider_mode,
        "real_llm_provider_api": config.provider_mode == "real_env",
        "llm_retry_scope": "provider/network/schema/empty-output only; deterministic feedback is not retried here",
    }
    redaction_report: list[dict[str, Any]] = []
    if config.redact_secrets:
        try:
            interaction = _redact_payload(interaction, "llm_interaction", redaction_report)
        except Exception as exc:
            return _redaction_failed_stage_run(
                stage_id=stage_id,
                prompt_template_version=prompt_template_version,
                prompt_messages=prompt_messages,
                parsed_schema_version=parsed_schema_version,
                config=config,
                provider_name=chat_provider.provider_name,
                model_id=last_model_id,
                raw_output=last_raw,
                attempts=attempts,
                usage=last_usage,
                failure_policy=failure_policy,
                field_path="llm_interaction",
                exc=exc,
            )
    return LLMStageRun(stage_id=stage_id.value, ok=schema_ok, parsed_output=parsed, interaction=interaction, stage_meta=meta, redaction_report=redaction_report)


def run_sl1_initial_modeling_llm(
    *,
    nl: str,
    spec_json: dict[str, Any] | None = None,
    upstream_lists: dict[str, Any] | None = None,
    pyfcstm_grammar_digest: str | None = None,
    config: Optional[LLMStageConfig] = None,
    provider: Optional[ChatProvider] = None,
) -> LLMStageRun:
    cfg = config or LLMStageConfig()
    version = "sl1-initial-modeling.v1"
    prompt = build_sl1_initial_modeling_prompt(
        nl=nl,
        spec_json=spec_json,
        upstream_lists=upstream_lists,
        pyfcstm_grammar_digest=pyfcstm_grammar_digest,
        prompt_template_version=version,
    )
    return _run_llm_stage(
        stage_id=StageId.SL_1_INITIAL_MODELING,
        prompt_template_version=version,
        prompt_messages=prompt,
        parser=parse_sl1_initial_modeling_response,
        parsed_schema_version="SL1InitialModeling.v1",
        config=cfg,
        provider=provider,
        response_format={"type": "json_object"},
    )


def run_sl5_scenario_generation_llm(
    *,
    nl: str,
    current_dsl: str,
    inspect_json: dict[str, Any] | None = None,
    design_summary: dict[str, Any] | None = None,
    grounding_map: Any | None = None,
    coverage_directive: str | None = None,
    previous_scenarios: list[Any] | None = None,
    config: Optional[LLMStageConfig] = None,
    provider: Optional[ChatProvider] = None,
) -> LLMStageRun:
    cfg = config or LLMStageConfig()
    version = "sl5-scenario-generation.v2"
    prompt = build_sl5_scenario_generation_prompt(
        nl=nl,
        current_dsl=current_dsl,
        inspect_json=inspect_json,
        design_summary=design_summary,
        grounding_map=grounding_map,
        coverage_directive=coverage_directive,
        previous_scenarios=previous_scenarios,
        prompt_template_version=version,
    )
    run = _run_llm_stage(
        stage_id=StageId.SL_5_SCENARIO_GENERATION,
        prompt_template_version=version,
        prompt_messages=prompt,
        parser=parse_sl5_scenario_generation_response,
        parsed_schema_version="TestScenario.list.v1",
        config=cfg,
        provider=provider,
        response_format={"type": "json_object"},
    )
    # Keep the typed return convenient for PR-C while preserving a stable
    # top-level JSON shape in the interaction record for audit/replay.  This is
    # done after the generic runner, so re-apply redaction to the reshaped
    # surfaces before returning them to run-record writers.
    if not run.ok:
        return run
    extra_report: list[dict[str, Any]] = []
    reshaped = {"scenarios": _jsonable(run.parsed_output)}
    try:
        run.interaction["parsed_output"] = (
            _redact_payload(reshaped, "llm_interaction.parsed_output", extra_report)
            if cfg.redact_secrets
            else reshaped
        )
    except Exception as exc:
        return _mark_stage_run_redaction_failed(
            run,
            stage_id=StageId.SL_5_SCENARIO_GENERATION,
            field_path="llm_interaction.parsed_output",
            exc=exc,
        )
    if run.interaction.get("attempts"):
        for i, attempt in enumerate(run.interaction["attempts"]):
            if attempt.get("status") == "ok" and isinstance(attempt.get("parsed_output"), list):
                attempt_reshaped = {"scenarios": attempt["parsed_output"]}
                try:
                    attempt["parsed_output"] = (
                        _redact_payload(
                            attempt_reshaped,
                            f"llm_interaction.attempts[{i}].parsed_output",
                            extra_report,
                        )
                        if cfg.redact_secrets
                        else attempt_reshaped
                    )
                except Exception as exc:
                    return _mark_stage_run_redaction_failed(
                        run,
                        stage_id=StageId.SL_5_SCENARIO_GENERATION,
                        field_path=f"llm_interaction.attempts[{i}].parsed_output",
                        exc=exc,
                    )
    run.redaction_report.extend(extra_report)
    return run


def run_sl9_repair_llm(
    *,
    nl: str,
    current_dsl: str,
    fix_plan: FixPlan | RevisedFixPlan | dict[str, Any] | None = None,
    fix_request_batch: FixRequestBatch | dict[str, Any] | None = None,
    fix_log: list[dict[str, Any]] | None = None,
    repair_memory: dict[str, Any] | None = None,
    grounding_map: Any | None = None,
    selected_diagnostics: list[dict[str, Any]] | None = None,
    grammar_digest: str | None = None,
    preserve_list: list[str] | None = None,
    scenario_summary: dict[str, Any] | None = None,
    repair_target: str | None = None,
    config: Optional[LLMStageConfig] = None,
    provider: Optional[ChatProvider] = None,
) -> LLMStageRun:
    cfg = config or LLMStageConfig()
    version = "sl9-repair.v2"
    prompt = build_sl9_repair_prompt(
        nl=nl,
        current_dsl=current_dsl,
        fix_plan=fix_plan,
        fix_request_batch=fix_request_batch,
        fix_log=fix_log,
        repair_memory=repair_memory,
        grounding_map=grounding_map,
        selected_diagnostics=selected_diagnostics,
        grammar_digest=grammar_digest,
        preserve_list=preserve_list,
        scenario_summary=scenario_summary,
        repair_target=repair_target,
        prompt_template_version=version,
    )

    def parse_repair(raw: str) -> dict[str, str]:
        stripped = strip_fence(raw)
        try:
            parsed = json.loads(stripped)
        except Exception:
            parsed = None
        if isinstance(parsed, dict) and parsed.get("candidate_dsl") is not None:
            dsl = strip_fence(str(parsed.get("candidate_dsl") or ""))
            if not dsl and any(decision.get("decision") == "accept" for decision in parsed.get("decisions", []) if isinstance(decision, dict)):
                raise ValueError("SL-9 candidate_dsl must be non-empty when a request is accepted")
            return {
                **parsed,
                "candidate_dsl": dsl,
            }
        # Real providers sometimes wrap DSL in Markdown fences despite the
        # prompt saying "no fences".  Fence-wrapped DSL is an LLM formatting
        # artifact, not a semantic repair decision; normalize it here so PR-C
        # does not feed fenced text into deterministic parse/semantic stages.
        dsl = stripped
        if not dsl:
            raise ValueError("SL-9 candidate_dsl must be non-empty")
        return {"candidate_dsl": dsl}

    run = _run_llm_stage(
        stage_id=StageId.SL_9_REPAIR,
        prompt_template_version=version,
        prompt_messages=prompt,
        parser=parse_repair,
        parsed_schema_version="SL9RepairCandidate.v1",
        config=cfg,
        provider=provider,
        response_format=None,
    )
    if run.ok and isinstance(run.parsed_output, dict):
        normalized = _jsonable(run.parsed_output)
        extra_report: list[dict[str, Any]] = []
        try:
            run.interaction["parsed_output"] = (
                _redact_payload(
                    normalized,
                    "llm_interaction.parsed_output",
                    extra_report,
                )
                if cfg.redact_secrets
                else normalized
            )
        except Exception as exc:
            return _mark_stage_run_redaction_failed(
                run,
                stage_id=StageId.SL_9_REPAIR,
                field_path="llm_interaction.parsed_output",
                exc=exc,
            )
        if run.interaction.get("attempts"):
            for i, attempt in enumerate(run.interaction["attempts"]):
                if attempt.get("status") == "ok":
                    try:
                        attempt["parsed_output"] = (
                            _redact_payload(
                                normalized,
                                f"llm_interaction.attempts[{i}].parsed_output",
                                extra_report,
                            )
                            if cfg.redact_secrets
                            else normalized
                        )
                    except Exception as exc:
                        return _mark_stage_run_redaction_failed(
                            run,
                            stage_id=StageId.SL_9_REPAIR,
                            field_path=f"llm_interaction.attempts[{i}].parsed_output",
                            exc=exc,
                        )
        run.redaction_report.extend(extra_report)
    return run




def _policy_mode(policy: dict[str, Any] | None, *, default: str) -> str:
    if not isinstance(policy, dict):
        return default
    return str(
        policy.get("mode")
        or policy.get("model_review_mode")
        or policy.get("delta_review_mode")
        or policy.get("review_mode")
        or default
    )


def _review_failure_policy(mode: str) -> Literal["fail_closed", "audit_only"]:
    return "audit_only" if mode == "audit_only" else "fail_closed"


def _sl7_feedback_ok(*, schema_ok: bool, decision: str, blocking_findings: list[dict[str, Any]], mode: str) -> bool:
    if not schema_ok:
        return False
    if mode == "audit_only":
        return True
    if mode in {"blocking", "blocking_major_only"}:
        return not (decision == "fail" and bool(blocking_findings))
    return decision in {"pass", "audit_only"}


def _sl10b_feedback_ok(*, schema_ok: bool, decision: str, mode: str) -> bool:
    if not schema_ok:
        return False
    if mode == "audit_only":
        return True
    return decision == "accept"

def run_sl7_model_review_llm(
    *,
    nl: str,
    current_dsl: str,
    grounding_map: Any,
    inspect_json: dict[str, Any] | None = None,
    design_diagnostics_summary: dict[str, Any] | None = None,
    sim_summary: dict[str, Any] | None = None,
    five_component_summary: dict[str, Any] | None = None,
    warning_budget_exhausted: list[str] | None = None,
    review_policy: dict[str, Any] | None = None,
    config: Optional[LLMStageConfig] = None,
    provider: Optional[ChatProvider] = None,
) -> LLMStageRun:
    cfg = config or LLMStageConfig()
    version = "sl7-model-review.v1"
    prompt = build_sl7_model_review_prompt(
        nl=nl,
        current_dsl=current_dsl,
        grounding_map=grounding_map,
        inspect_json=inspect_json,
        design_diagnostics_summary=design_diagnostics_summary,
        sim_summary=sim_summary,
        five_component_summary=five_component_summary,
        warning_budget_exhausted=warning_budget_exhausted,
        review_policy=review_policy,
        prompt_template_version=version,
    )
    mode = _policy_mode(review_policy, default="blocking_major_only")
    run = _run_llm_stage(
        stage_id=StageId.SL_7_MODEL_REVIEW,
        prompt_template_version=version,
        prompt_messages=prompt,
        parser=parse_sl7_model_review_response,
        parsed_schema_version="ModelReviewFeedback.v1",
        config=cfg,
        provider=provider,
        response_format={"type": "json_object"},
        failure_policy=_review_failure_policy(mode),
    )
    parsed = run.parsed_output if isinstance(run.parsed_output, dict) else {}
    review_meta = ReviewRunMeta(**run.interaction["review_meta"])
    decision = parsed.get("decision", "invalid_output") if run.ok else "invalid_output"
    risk_level = parsed.get("risk_level", "major" if not run.ok else "none")
    blocking_findings = parsed.get("blocking_findings", [])
    feedback = ModelReviewFeedback(
        ok=_sl7_feedback_ok(schema_ok=run.ok, decision=decision, blocking_findings=blocking_findings, mode=mode),
        decision=decision,
        risk_level=risk_level,
        findings=parsed.get("findings", []),
        blocking_findings=blocking_findings,
        review_meta=review_meta,
        meta=run.stage_meta,
    )
    run.feedback = feedback
    return run


def run_sl10b_delta_review_llm(
    *,
    nl: str,
    grounding_map: Any,
    old_dsl: str,
    candidate_dsl: str,
    fix_plan: FixPlan | RevisedFixPlan | dict[str, Any],
    diff_summary: dict[str, Any] | None = None,
    delta_review_policy: dict[str, Any] | None = None,
    config: Optional[LLMStageConfig] = None,
    provider: Optional[ChatProvider] = None,
) -> LLMStageRun:
    cfg = config or LLMStageConfig()
    version = "sl10b-delta-review.v1"
    prompt = build_sl10b_delta_review_prompt(
        nl=nl,
        grounding_map=grounding_map,
        old_dsl=old_dsl,
        candidate_dsl=candidate_dsl,
        fix_plan=fix_plan,
        diff_summary=diff_summary,
        prompt_template_version=version,
    )
    mode = _policy_mode(delta_review_policy, default="blocking_major_only")
    run = _run_llm_stage(
        stage_id=StageId.SL_10B_DELTA_REVIEW,
        prompt_template_version=version,
        prompt_messages=prompt,
        parser=parse_sl10b_delta_review_response,
        parsed_schema_version="RepairReviewFeedback.delta_review.v1",
        config=cfg,
        provider=provider,
        response_format={"type": "json_object"},
        failure_policy=_review_failure_policy(mode),
    )
    parsed = run.parsed_output if isinstance(run.parsed_output, dict) else {}
    review_meta = ReviewRunMeta(**run.interaction["review_meta"])
    decision = parsed.get("decision", "revise") if run.ok else "revise"
    drift_risk = parsed.get("drift_risk", "major" if decision != "accept" else "none")
    feedback_ok = _sl10b_feedback_ok(schema_ok=run.ok, decision=decision, mode=mode)
    feedback = RepairReviewFeedback(
        ok=feedback_ok,
        target_resolved=feedback_ok,
        regression_detected=(mode != "audit_only") and decision in {"reject", "revise"},
        drift_risk=drift_risk,
        delta_review=parsed if parsed else {"decision": "revise", "error": run.interaction.get("schema_validation_error")},
        review_meta=review_meta,
        meta=run.stage_meta,
    )
    run.feedback = feedback
    return run


def run_sl10_repair_review_llm(
    *,
    nl: str,
    grounding_map: Any,
    old_dsl: str,
    candidate_dsl: str,
    request_batch: Any,
    sl9_decisions: Any,
    fix_log: list[dict[str, Any]] | None = None,
    diff_summary: dict[str, Any] | None = None,
    local_check_evidence: dict[str, Any] | None = None,
    scenario_summary: dict[str, Any] | None = None,
    review_policy: dict[str, Any] | None = None,
    config: Optional[LLMStageConfig] = None,
    provider: Optional[ChatProvider] = None,
) -> LLMStageRun:
    cfg = config or LLMStageConfig()
    version = "sl10-repair-review.v1"
    prompt = build_sl10_repair_review_prompt(
        nl=nl,
        grounding_map=grounding_map,
        old_dsl=old_dsl,
        candidate_dsl=candidate_dsl,
        request_batch=request_batch,
        sl9_decisions=sl9_decisions,
        fix_log=fix_log,
        diff_summary=diff_summary,
        local_check_evidence=local_check_evidence,
        scenario_summary=scenario_summary,
        prompt_template_version=version,
    )
    mode = _policy_mode(review_policy, default="blocking_major_only")
    run = _run_llm_stage(
        stage_id=StageId.SL_10_REPAIR_REVIEW,
        prompt_template_version=version,
        prompt_messages=prompt,
        parser=parse_sl10_repair_review_response,
        parsed_schema_version="SL10RepairReviewOutput.v1",
        config=cfg,
        provider=provider,
        response_format={"type": "json_object"},
        failure_policy=_review_failure_policy(mode),
    )
    parsed = run.parsed_output if isinstance(run.parsed_output, dict) else {}
    review_meta = ReviewRunMeta(**run.interaction["review_meta"])
    decision = parsed.get("decision", "invalid_output") if run.ok else "invalid_output"
    target_resolved = bool(parsed.get("target_resolved", decision == "pass"))
    regression_detected = bool(parsed.get("regression_detected", decision != "pass"))
    drift_risk = parsed.get("drift_risk", "none" if decision == "pass" else "major")
    ok = bool(
        run.ok
        and decision == "pass"
        and target_resolved
        and not regression_detected
        and drift_risk in {"none", "minor"}
    )
    if run.ok and decision == "pass" and not ok:
        decision = "rework"
        instructions = [str(item) for item in parsed.get("rework_instructions", [])]
        instructions.append(
            "SL-10 pass was downgraded because its own fields reported "
            f"target_resolved={target_resolved}, "
            f"regression_detected={regression_detected}, drift_risk={drift_risk}."
        )
    else:
        instructions = [str(item) for item in parsed.get("rework_instructions", [])]
    feedback = SL10RepairReviewOutput(
        ok=ok,
        decision=decision,
        target_resolved=target_resolved,
        regression_detected=regression_detected,
        drift_risk=drift_risk,
        rework_instructions=instructions,
        evidence=parsed.get("evidence", []),
        local_override_rationale=[str(item) for item in parsed.get("local_override_rationale", [])],
        local_check_evidence=local_check_evidence or {},
        review_meta=review_meta,
        meta=run.stage_meta,
    )
    run.feedback = feedback
    return run


__all__ = [
    "ChatProvider",
    "LLMStageConfig",
    "LLMStageRun",
    "MockLLMProvider",
    "RealEnvLLMProvider",
    "redact_run_record_payload",
    "run_sl1_initial_modeling_llm",
    "run_sl5_scenario_generation_llm",
    "run_sl7_model_review_llm",
    "run_sl9_repair_llm",
    "run_sl10_repair_review_llm",
    "run_sl10b_delta_review_llm",
]
