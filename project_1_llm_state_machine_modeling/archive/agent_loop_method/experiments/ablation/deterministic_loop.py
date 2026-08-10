"""Deterministic ablation integration loop.

Migrated from the historical PR-2A implementation. The functionality is kept
as a deterministic/ablation research asset, not as the default LangGraph
agent-loop runtime.

This runner wires the PR-0/PR-1A/PR-1B/PR-2B contracts into one local,
replayable agent loop without calling any real LLM provider/API.  SL-9 is
represented by deterministic candidate injection; PR-2B adds fake/replay
SL-7 and SL-10B review wiring so review prompts, raw outputs, parsed outputs,
ReviewRunMeta and failure behavior are auditable in one run record.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import re
import subprocess
from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from method.gpt_client import chat as llm_chat
from method.gpt_client import get_default_model
from method.run_record import agent_loop_run_record_path, write_agent_loop_run_record
from method.schema import (
    AgentLoopResult,
    AgentLoopRunRecord,
    FeedbackBundle,
    FixPlan,
    GroundingMap,
    IterTrace,
    ModelArtifact,
    ModelReviewFeedback,
    RepairRejection,
    RepairReviewFeedback,
    ReviewRunMeta,
    ScenarioSet,
    StageContext,
    StageResultMeta,
    TestScenario,
    RevisedFixPlan,
)
from method.stages.ids import FEEDBACK_SOURCE_TO_STAGE_ID, STAGE_SPECS_BY_ID, FeedbackSource, StageId, StageStatus
from method.stages.sd_tools import (
    freeze_scenario_set,
    mark_warning_repair_attempt,
    run_sd2_parse,
    run_sd3_semantic,
    run_sd4_design,
    run_sd5a_scenario_coverage,
    run_sd6_sim,
    run_sd8_fix_plan,
    run_sd10_repair_review,
)
from method.stages.sl_delta_review_prompt import build_sl10b_delta_review_prompt, parse_sl10b_delta_review_response
from method.stages.sl_model_review_prompt import build_sl7_model_review_prompt, parse_sl7_model_review_response
from method.stages.sl_repair_prompt import build_sl9_repair_prompt

SC_0_STAGE_GRAPH = [
    StageId.SC_0_START.value,
    StageId.SD_2_PARSE.value,
    StageId.SD_3_SEMANTIC.value,
    StageId.SD_4_DESIGN.value,
    StageId.SL_5_SCENARIO_GENERATION.value,
    StageId.SD_5A_SCENARIO_COVERAGE.value,
    StageId.SC_5F_SCENARIO_FREEZE.value,
    StageId.SD_6_SIM.value,
    StageId.SL_7_MODEL_REVIEW.value,
    StageId.SD_8_FIX_PLAN.value,
    StageId.SL_9_REPAIR.value,
    StageId.SD_10_REPAIR_REVIEW.value,
    StageId.SL_10B_DELTA_REVIEW.value,
    StageId.SC_11_ACCEPT_CANDIDATE.value,
    StageId.SC_12_EXIT.value,
    StageId.SC_13_TRACE_AUDIT.value,
]

RUN_RECORD_SCHEMA_VERSION = "pr2b.agent-loop-run-record.v1"


@dataclass
class ReviewPolicy:
    """Policy for PR-2B fake/replay lightweight LLM reviews.

    Defaults are audit-only so PR-2B cannot silently change the PR-2A
    deterministic baseline or Path1/Path2 main-result eligibility.  Blocking
    mode is opt-in and still uses fake/replay responses only.
    """

    enable_model_review: bool = False
    enable_delta_review: bool = False
    model_review_mode: str = "audit_only"
    delta_review_mode: str = "audit_only"
    failure_policy: str = "audit_only"
    decision_threshold: float | None = None
    require_replay: bool = True

    def __post_init__(self) -> None:
        for field_name in ("model_review_mode", "delta_review_mode"):
            value = getattr(self, field_name)
            if value not in {"audit_only", "blocking"}:
                raise ValueError(f"ReviewPolicy.{field_name} must be audit_only or blocking")
        if self.failure_policy not in {"audit_only", "fail_open", "fail_closed"}:
            raise ValueError("ReviewPolicy.failure_policy must be audit_only, fail_open, or fail_closed")
        if self.decision_threshold is not None and not 0 <= float(self.decision_threshold) <= 1:
            raise ValueError("ReviewPolicy.decision_threshold must be within [0, 1]")

    def review_meta_failure_policy(self, *, delta: bool = False) -> str:
        mode = self.delta_review_mode if delta else self.model_review_mode
        if mode == "blocking":
            return "fail_closed"
        if mode in {"fail_open", "fail_closed"}:
            return mode
        if self.failure_policy in {"fail_open", "fail_closed", "audit_only"}:
            return self.failure_policy
        return "audit_only"

    def is_model_review_blocking(self, feedback: ModelReviewFeedback) -> bool:
        return self.enable_model_review and self.model_review_mode == "blocking" and feedback.decision == "fail" and bool(feedback.blocking_findings)

    def is_delta_review_blocking_reject(self, parsed: dict[str, Any]) -> bool:
        return self.enable_delta_review and self.delta_review_mode == "blocking" and parsed.get("decision") in {"reject", "revise"}


@dataclass
class DeterministicLoopConfig:
    """Configuration for the PR-2A deterministic runner."""

    initial_dsl: str
    scenarios: list[TestScenario] = field(default_factory=list)
    repair_candidates: list[str] = field(default_factory=list)
    grounding_map: GroundingMap | None = None
    run_id: str = ""
    output_dir: str | Path = "runs"
    max_iterations: int = 3
    policy_profile: str = "generated_candidate"
    seed: int | None = None
    path_context: dict[str, Any] = field(default_factory=dict)
    review_policy: ReviewPolicy = field(default_factory=ReviewPolicy)
    review_provider_mode: str = "fake_replay"
    review_model: str | None = None
    review_max_tokens: int | None = None
    review_max_retries: int = 2
    review_replay_responses: dict[str, str] = field(default_factory=dict)
    review_provider_failures: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.review_provider_mode not in {"fake_replay", "real_env"}:
            raise ValueError("DeterministicLoopConfig.review_provider_mode must be fake_replay or real_env")
        if self.review_max_tokens is not None and self.review_max_tokens <= 0:
            raise ValueError("DeterministicLoopConfig.review_max_tokens must be positive when provided")
        if self.review_max_retries < 0:
            raise ValueError("DeterministicLoopConfig.review_max_retries must be >= 0")


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _hash_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _short_hash(value: Any) -> str:
    return "sha256:" + hashlib.sha256(repr(_jsonable(value)).encode("utf-8")).hexdigest()


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(v) for v in value]
    if is_dataclass(value) and not isinstance(value, type):
        return _jsonable(asdict(value))
    if is_dataclass(value) and isinstance(value, type):
        return f"<non-json:dataclass-type:{value.__name__}>"
    return str(value)


def _strict_jsonable(value: Any) -> Any:
    """JSON-normalize run-record payloads while preserving audit visibility."""
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if math.isfinite(value):
            return value
        if math.isnan(value):
            return "<non-json-float:nan>"
        return "<non-json-float:inf>" if value > 0 else "<non-json-float:-inf>"
    if isinstance(value, dict):
        return {str(k): _strict_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_strict_jsonable(v) for v in value]
    if is_dataclass(value) and not isinstance(value, type):
        return _strict_jsonable(asdict(value))
    if is_dataclass(value) and isinstance(value, type):
        return f"<non-json:dataclass-type:{value.__name__}>"
    return f"<non-json:{type(value).__name__}>"


def _json_normalized_changed(original: Any, normalized: Any) -> bool:
    try:
        changed = normalized != original
    except Exception:
        return True
    return changed if isinstance(changed, bool) else True


def _record_payload_sanitized_log(field: str, *, message: str | None = None) -> dict[str, Any]:
    return {
        "ts": _utc_now(),
        "level": "error",
        "event": "record_payload_sanitized",
        "field": field,
        "message": message or "non-json record payload normalized; run excluded from Path1/Path2 main results",
    }


SECRET_TEXT_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("openai_api_key", re.compile(r"sk-[A-Za-z0-9][A-Za-z0-9_-]{7,}")),
    ("github_oauth_token", re.compile(r"gh[o|p|s|u|r]_[A-Za-z0-9_]{8,}")),
    ("github_pat", re.compile(r"github_pat_[A-Za-z0-9_]{8,}")),
    ("bearer_token", re.compile(r"Bearer\s+[A-Za-z0-9._\-]{12,}", re.IGNORECASE)),
)
SECRET_KEYWORDS = ("api_key", "apikey", "token", "password", "passwd", "secret", "authorization")


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


def _redact_run_record_payload(value: Any, path: str, report: list[dict[str, Any]], *, affects_replay: bool = True) -> Any:
    """Remove common secrets before persisting the self-contained run record.

    The agent-loop record is intended for Path1/Path2 audit and handoff.  It
    must preserve prompt/response evidence, but not raw API keys or tokens.  The
    replacement keeps a stable digest so replay/debug consumers can tell whether
    two redacted values were the same without seeing the original secret.
    """
    if isinstance(value, str):
        return _redact_text(value, path, report, affects_replay=affects_replay)
    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            item_path = f"{path}.{key_text}" if path else key_text
            if isinstance(item, str) and any(keyword in key_text.lower() for keyword in SECRET_KEYWORDS):
                replacement = _redaction_placeholder(item, "secret_field")
                report.append(_redaction_report_item(item_path, reason="secret_field", replacement=replacement, affects_replay=affects_replay))
                redacted[key_text] = replacement
            else:
                redacted[key_text] = _redact_run_record_payload(item, item_path, report, affects_replay=affects_replay)
        return redacted
    if isinstance(value, list):
        return [_redact_run_record_payload(item, f"{path}[{i}]", report, affects_replay=affects_replay) for i, item in enumerate(value)]
    if isinstance(value, tuple):
        return [_redact_run_record_payload(item, f"{path}[{i}]", report, affects_replay=affects_replay) for i, item in enumerate(value)]
    return value


def _strict_record_field(field: str, value: Any, logs: list[dict[str, Any]]) -> tuple[Any, bool]:
    try:
        normalized = _strict_jsonable(value)
    except Exception as e:
        logs.append(
            _record_payload_sanitized_log(
                field,
                message=f"record payload normalization failed: {type(e).__name__}: {e}",
            )
        )
        return f"<non-json-normalization-error:{type(value).__name__}:{type(e).__name__}>", True
    changed = _json_normalized_changed(value, normalized)
    if changed:
        logs.append(_record_payload_sanitized_log(field))
    return normalized, changed


def _meta(stage_id: StageId, *, ok: bool = True, status: StageStatus | None = None, stage_error: str | None = None) -> StageResultMeta:
    spec = STAGE_SPECS_BY_ID[stage_id.value]
    return StageResultMeta(
        stage_id=stage_id.value,
        stage_kind=spec.kind,
        enabled=True,
        ran=True,
        status=status or (StageStatus.OK if ok else StageStatus.FAIL),
        ok=ok,
        stage_error=stage_error,
    )


def _stage_ids(stage_records: list[StageResultMeta]) -> list[str]:
    return [meta.stage_id for meta in stage_records]


def _append_stage(stage_records: list[StageResultMeta], meta: StageResultMeta) -> StageResultMeta:
    stage_records.append(meta)
    return meta


def _feedback_bundle(
    *,
    parse_feedback: Any = None,
    semantic_feedback: Any = None,
    design_feedback: Any = None,
    sim_feedback: Any = None,
    model_review_feedback: Any = None,
    stage_results: list[StageResultMeta] | None = None,
    include_model_review: bool = False,
) -> FeedbackBundle:
    enabled_sources = [
        FeedbackSource.PARSE.value,
        FeedbackSource.SEMANTIC.value,
        FeedbackSource.DESIGN.value,
        FeedbackSource.SIM.value,
    ]
    if include_model_review:
        enabled_sources.append(FeedbackSource.MODEL_REVIEW.value)
    return FeedbackBundle(
        enabled_sources=enabled_sources,
        parse=parse_feedback,
        semantic=semantic_feedback,
        design=design_feedback,
        sim=sim_feedback,
        model_review=model_review_feedback,
        stage_results=list(stage_results or []),
    )


def _select_feedback(bundle: FeedbackBundle, review_policy: ReviewPolicy | None = None) -> tuple[str, Any, str] | None:
    """Pick the first feedback item that should trigger repair."""
    if bundle.parse is not None and not bundle.parse.ok:
        return FeedbackSource.PARSE.value, bundle.parse, FEEDBACK_SOURCE_TO_STAGE_ID[FeedbackSource.PARSE.value]
    if bundle.semantic is not None and not bundle.semantic.ok:
        return FeedbackSource.SEMANTIC.value, bundle.semantic, FEEDBACK_SOURCE_TO_STAGE_ID[FeedbackSource.SEMANTIC.value]
    if bundle.design is not None and bundle.design.blocking_items:
        return FeedbackSource.DESIGN.value, bundle.design, FEEDBACK_SOURCE_TO_STAGE_ID[FeedbackSource.DESIGN.value]
    if bundle.sim is not None and not bundle.sim.ok:
        return FeedbackSource.SIM.value, bundle.sim, FEEDBACK_SOURCE_TO_STAGE_ID[FeedbackSource.SIM.value]
    if review_policy is not None and bundle.model_review is not None and review_policy.is_model_review_blocking(bundle.model_review):
        return FeedbackSource.MODEL_REVIEW.value, bundle.model_review, FEEDBACK_SOURCE_TO_STAGE_ID[FeedbackSource.MODEL_REVIEW.value]
    return None


def _environment() -> dict[str, Any]:
    git_commit = ""
    try:
        git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        git_commit = "unknown"
    pyfcstm_version = ""
    try:
        import pyfcstm  # type: ignore

        pyfcstm_version = getattr(pyfcstm, "__version__", "unknown")
    except Exception:
        pyfcstm_version = "unavailable"
    return {
        "git_commit": git_commit,
        "python_version": platform.python_version(),
        "pyfcstm_version": pyfcstm_version,
        "runner": "method.experiments.ablation.deterministic_loop.run_deterministic_ablation_loop",
        "llm_provider": "none",
    }


def _llm_interaction_meta(
    stage_id: StageId,
    *,
    prompt_messages: list[dict[str, str]],
    raw_output: str,
    ok: bool,
    validation_error: str | None = None,
) -> StageResultMeta:
    if ok:
        status = StageStatus.OK
    elif validation_error:
        status = StageStatus.ERROR
    else:
        status = StageStatus.FAIL
    meta = _meta(stage_id, ok=ok, status=status, stage_error=validation_error)
    meta.prompt_hash = _short_hash(prompt_messages)
    meta.input_hash = _short_hash(prompt_messages)
    meta.output_hash = _hash_text(raw_output) if raw_output else _hash_text(validation_error or "")
    meta.output_validation_error = validation_error
    return meta


def _make_review_meta(
    *,
    provider: str,
    model_id: str,
    prompt_template_version: str,
    prompt_messages: list[dict[str, str]],
    raw_output: str,
    parsed_schema_version: str,
    schema_validation_ok: bool,
    failure_policy: str,
    replay_key: str,
    decision_threshold: float | None = None,
    schema_validation_error: str | None = None,
    seed: int | None = None,
    retry_count: int = 0,
) -> ReviewRunMeta:
    return ReviewRunMeta(
        provider=provider,
        model_id=model_id,
        resolved_model_id=model_id,
        prompt_template_version=prompt_template_version,
        prompt_hash=_short_hash(prompt_messages),
        input_hash=_short_hash(prompt_messages),
        temperature=0.0,
        seed=seed,
        retry_count=retry_count,
        raw_output_hash=_hash_text(raw_output) if raw_output else _hash_text(schema_validation_error or ""),
        raw_output_path=None,
        parsed_schema_version=parsed_schema_version,
        schema_validation_ok=schema_validation_ok,
        schema_validation_error=schema_validation_error,
        cache_key=replay_key,
        decision_threshold=decision_threshold,
        failure_policy=failure_policy,  # type: ignore[arg-type]
        replay_key=replay_key,
    )


def _review_interaction_payload(
    *,
    stage_id: StageId,
    prompt_messages: list[dict[str, str]],
    raw_output: str,
    parsed_output: dict[str, Any],
    review_meta: ReviewRunMeta,
    schema_validation_ok: bool,
    note: str,
    usage: dict[str, Any] | None = None,
    attempts: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "stage_id": stage_id.value,
        "provider": review_meta.provider,
        "model_id": review_meta.model_id,
        "resolved_model_id": review_meta.resolved_model_id,
        "prompt_template_version": review_meta.prompt_template_version,
        "prompt_hash": review_meta.prompt_hash,
        "input_hash": review_meta.input_hash,
        "temperature": review_meta.temperature,
        "seed": review_meta.seed,
        "retry_count": review_meta.retry_count,
        "raw_output_hash": review_meta.raw_output_hash,
        "raw_output_path": review_meta.raw_output_path,
        "parsed_schema_version": review_meta.parsed_schema_version,
        "prompt_messages": prompt_messages,
        "raw_output": raw_output,
        "parsed_output": parsed_output,
        "schema_validation_ok": schema_validation_ok,
        "schema_validation_error": review_meta.schema_validation_error,
        "cache_key": review_meta.cache_key,
        "replay_key": review_meta.replay_key,
        "decision_threshold": review_meta.decision_threshold,
        "failure_policy": review_meta.failure_policy,
        "review_meta": asdict(review_meta),
        "usage": usage or {},
        "attempts": attempts or [],
        "note": note,
    }


def _review_replay_lookup(cfg: DeterministicLoopConfig, stage_id: StageId, iteration: int) -> tuple[str | None, str]:
    key = f"{stage_id.value}:{iteration}"
    if key in cfg.review_replay_responses:
        return cfg.review_replay_responses[key], key
    stage_key = stage_id.value
    if stage_key in cfg.review_replay_responses:
        return cfg.review_replay_responses[stage_key], stage_key
    return None, key


def _call_real_review_llm(
    *,
    prompt_messages: list[dict[str, str]],
    cfg: DeterministicLoopConfig,
    stage_id: StageId,
) -> tuple[str, dict[str, Any], str]:
    """Call the real OpenAI-compatible review provider configured by ``.env``.

    PR-3 uses this only for representative handoff smoke.  The main agent-loop
    experiment record still stores the full prompt, raw output, parsed output
    and provider/model metadata; API keys are never persisted.
    """
    if stage_id.value in cfg.review_provider_failures:
        raise RuntimeError("provider failure")
    model_id = cfg.review_model or get_default_model()
    raw_output, usage = llm_chat(
        messages=prompt_messages,
        model=cfg.review_model,
        temperature=0.0,
        seed=cfg.seed,
        max_tokens=cfg.review_max_tokens,
        response_format={"type": "json_object"},
    )
    return raw_output, usage, model_id


def _review_attempt_payload(
    *,
    stage_id: StageId,
    attempt_index: int,
    status: str,
    raw_output: str,
    usage: dict[str, Any] | None,
    model_id: str,
    error_kind: str | None = None,
    error_message: str | None = None,
    parsed_output: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "stage_id": stage_id.value,
        "attempt_index": attempt_index,
        "status": status,
        "schema_validation_ok": status == "ok",
        "error_kind": error_kind,
        "error_message": error_message,
        "raw_output_hash": _hash_text(raw_output) if raw_output else _hash_text(error_message or ""),
        "raw_output": raw_output,
        "parsed_output": parsed_output or {},
        "usage": usage or {},
        "model_id": model_id,
        "provider": "openai-compatible-env",
    }


def _llm_retry_log(
    *,
    stage_id: StageId,
    attempt_index: int,
    max_retries: int,
    error_kind: str,
    error_message: str,
    raw_output: str,
) -> dict[str, Any]:
    return {
        "ts": _utc_now(),
        "level": "warning",
        "event": "llm_review_attempt_failed",
        "stage_id": stage_id.value,
        "attempt_index": attempt_index,
        "max_retries": max_retries,
        "will_retry": attempt_index < max_retries,
        "error_kind": error_kind,
        "error_message": error_message,
        "raw_output_hash": _hash_text(raw_output) if raw_output else _hash_text(error_message),
    }


def _run_real_review_llm_with_retry(
    *,
    prompt_messages: list[dict[str, str]],
    cfg: DeterministicLoopConfig,
    stage_id: StageId,
    parser: Callable[[str], dict[str, Any]],
    invalid_parsed_factory: Callable[[str], dict[str, Any]],
    logs: list[dict[str, Any]],
) -> tuple[str, dict[str, Any], str, dict[str, Any], bool, str | None, list[dict[str, Any]], int]:
    """Call a real review LLM with bounded retry for provider/schema noise.

    Retry is intentionally limited to LLM stages and only for two low-probability
    failure classes that do not reflect deterministic model quality:
    provider/network errors and invalid JSON/schema output.  Every attempt is
    preserved in the run record so Path1/Path2 can audit retries instead of
    silently smoothing over experimental instability.
    """
    max_retries = cfg.review_max_retries
    attempts: list[dict[str, Any]] = []
    last_raw_output = ""
    last_usage: dict[str, Any] = {}
    try:
        last_model_id = cfg.review_model or get_default_model()
    except Exception:
        last_model_id = cfg.review_model or "env:LLM_MODEL"
    last_error: str | None = None
    last_error_kind = "unknown"
    parsed = invalid_parsed_factory("no attempt")

    for attempt_index in range(max_retries + 1):
        try:
            raw_output, usage, model_id = _call_real_review_llm(
                prompt_messages=prompt_messages,
                cfg=cfg,
                stage_id=stage_id,
            )
            last_raw_output = raw_output
            last_usage = usage
            last_model_id = model_id
        except Exception as e:
            last_error_kind = "provider_error"
            last_error = f"provider failure: {type(e).__name__}: {str(e)[:300]}"
            attempts.append(
                _review_attempt_payload(
                    stage_id=stage_id,
                    attempt_index=attempt_index,
                    status="provider_error",
                    raw_output="",
                    usage={},
                    model_id=last_model_id,
                    error_kind=last_error_kind,
                    error_message=last_error,
                    parsed_output=invalid_parsed_factory(last_error),
                )
            )
            logs.append(
                _llm_retry_log(
                    stage_id=stage_id,
                    attempt_index=attempt_index,
                    max_retries=max_retries,
                    error_kind=last_error_kind,
                    error_message=last_error,
                    raw_output="",
                )
            )
            continue

        try:
            parsed = parser(raw_output)
            attempts.append(
                _review_attempt_payload(
                    stage_id=stage_id,
                    attempt_index=attempt_index,
                    status="ok",
                    raw_output=raw_output,
                    usage=usage,
                    model_id=model_id,
                    parsed_output=parsed,
                )
            )
            if attempt_index > 0:
                logs.append(
                    {
                        "ts": _utc_now(),
                        "level": "info",
                        "event": "llm_review_retry_recovered",
                        "stage_id": stage_id.value,
                        "attempt_index": attempt_index,
                        "retry_count": attempt_index,
                        "max_retries": max_retries,
                    }
                )
            return raw_output, usage, model_id, parsed, True, None, attempts, attempt_index
        except Exception as e:  # pragma: no cover - parser implementation is tested separately
            last_error_kind = "schema_invalid"
            last_error = f"schema invalid: {type(e).__name__}: {str(e)[:300]}"
            parsed = invalid_parsed_factory(last_error)
            attempts.append(
                _review_attempt_payload(
                    stage_id=stage_id,
                    attempt_index=attempt_index,
                    status="schema_invalid",
                    raw_output=raw_output,
                    usage=usage,
                    model_id=model_id,
                    error_kind=last_error_kind,
                    error_message=last_error,
                    parsed_output=parsed,
                )
            )
            logs.append(
                _llm_retry_log(
                    stage_id=stage_id,
                    attempt_index=attempt_index,
                    max_retries=max_retries,
                    error_kind=last_error_kind,
                    error_message=last_error,
                    raw_output=raw_output,
                )
            )

    exhausted_error = f"retry exhausted after {max_retries} retries: {last_error or 'unknown LLM failure'}"
    if attempts:
        attempts[-1]["retry_exhausted"] = True
    logs.append(
        {
            "ts": _utc_now(),
            "level": "error",
            "event": "llm_review_retry_exhausted",
            "stage_id": stage_id.value,
            "max_retries": max_retries,
            "error_kind": last_error_kind,
            "error_message": exhausted_error,
        }
    )
    return last_raw_output, last_usage, last_model_id, parsed, False, exhausted_error, attempts, max_retries


def _run_sl7_model_review(
    *,
    nl: str,
    current_dsl: str,
    context: StageContext,
    bundle: FeedbackBundle,
    cfg: DeterministicLoopConfig,
    iteration: int,
    llm_interactions: list[dict[str, Any]],
    logs: list[dict[str, Any]],
) -> tuple[ModelReviewFeedback, StageResultMeta, bool]:
    prompt_version = "sl7-model-review.v1"
    review_policy_payload = asdict(cfg.review_policy)
    prompt_messages = build_sl7_model_review_prompt(
        nl=nl,
        current_dsl=current_dsl,
        grounding_map=cfg.grounding_map or context.grounding_map,
        inspect_json=context.inspect_json,
        design_diagnostics_summary=asdict(bundle.design) if bundle.design is not None else {},
        sim_summary=asdict(bundle.sim) if bundle.sim is not None else {},
        warning_budget_exhausted=[key for key, state in context.warning_budget_state.items() if getattr(state, "budget_exhausted", False)],
        review_policy=review_policy_payload,
        prompt_template_version=prompt_version,
    )
    raw_output, replay_key = _review_replay_lookup(cfg, StageId.SL_7_MODEL_REVIEW, iteration)
    failure_policy = cfg.review_policy.review_meta_failure_policy(delta=False)
    provider = "fake-replay"
    model_id = "fake-sl7-review"
    usage: dict[str, Any] = {}
    attempts: list[dict[str, Any]] = []
    retry_count = 0
    note = "PR-2B fake/replay model review; no real provider/API called"
    parsed: dict[str, Any]
    schema_ok = False
    error: str | None = None

    if cfg.review_provider_mode == "real_env":
        provider = "openai-compatible-env"
        replay_key = "real-env:" + replay_key
        note = "PR-3 real .env SL-7 model review call recorded in AgentLoopRunRecord; provider/schema noise uses bounded retry"
        raw_output, usage, model_id, parsed, schema_ok, error, attempts, retry_count = _run_real_review_llm_with_retry(
            prompt_messages=prompt_messages,
            cfg=cfg,
            stage_id=StageId.SL_7_MODEL_REVIEW,
            parser=parse_sl7_model_review_response,
            invalid_parsed_factory=lambda message: {
                "decision": "invalid_output",
                "risk_level": "major",
                "findings": [],
                "blocking_findings": [],
                "error": message,
            },
            logs=logs,
        )
    elif StageId.SL_7_MODEL_REVIEW.value in cfg.review_provider_failures:
        error = "provider failure"
        parsed = {"decision": "invalid_output", "risk_level": "major", "findings": [], "blocking_findings": [], "error": error}
        logs.append({"ts": _utc_now(), "level": "error", "event": "llm_review_provider_failure", "stage_id": StageId.SL_7_MODEL_REVIEW.value})
        provider = "fake-error"
        raw_output = ""
    else:
        if raw_output is None and not cfg.review_policy.require_replay:
            raw_output = json.dumps({"decision": "audit_only", "risk_level": "none", "findings": [], "blocking_findings": []}, ensure_ascii=False)
            replay_key = "default-fake:" + replay_key
        if raw_output is None:
            error = "replay miss"
            parsed = {"decision": "invalid_output", "risk_level": "major", "findings": [], "blocking_findings": [], "error": error}
            logs.append({"ts": _utc_now(), "level": "error", "event": "llm_review_replay_miss", "stage_id": StageId.SL_7_MODEL_REVIEW.value, "replay_key": replay_key})
            raw_output = ""
        else:
            try:
                parsed = parse_sl7_model_review_response(raw_output)
                schema_ok = True
            except Exception as e:  # pragma: no cover - exact parser type is intentionally not part of contract
                parsed = {"decision": "invalid_output", "risk_level": "major", "findings": [], "blocking_findings": [], "error": str(e)}
                error = str(e)
                logs.append({"ts": _utc_now(), "level": "error", "event": "llm_review_invalid_output", "stage_id": StageId.SL_7_MODEL_REVIEW.value, "message": error})

    review_meta = _make_review_meta(
        provider=provider,
        model_id=model_id,
        prompt_template_version=prompt_version,
        prompt_messages=prompt_messages,
        raw_output=raw_output,
        parsed_schema_version="ModelReviewFeedback.v1",
        schema_validation_ok=schema_ok,
        schema_validation_error=error,
        failure_policy=failure_policy,
        replay_key=replay_key,
        decision_threshold=cfg.review_policy.decision_threshold,
        seed=cfg.seed,
        retry_count=retry_count,
    )
    ok = schema_ok and (parsed.get("decision") in {"pass", "audit_only"} or cfg.review_policy.model_review_mode == "audit_only")
    meta = _llm_interaction_meta(StageId.SL_7_MODEL_REVIEW, prompt_messages=prompt_messages, raw_output=raw_output, ok=ok, validation_error=error)
    feedback = ModelReviewFeedback(
        ok=ok,
        decision=parsed.get("decision", "invalid_output"),
        risk_level=parsed.get("risk_level", "major"),
        findings=parsed.get("findings", []),
        blocking_findings=parsed.get("blocking_findings", []),
        review_meta=review_meta,
        meta=meta,
    )
    llm_interactions.append(
        _review_interaction_payload(
            stage_id=StageId.SL_7_MODEL_REVIEW,
            prompt_messages=prompt_messages,
            raw_output=raw_output,
            parsed_output=parsed,
            review_meta=review_meta,
            schema_validation_ok=schema_ok,
            note=note,
            usage=usage,
            attempts=attempts,
        )
    )
    return feedback, meta, not schema_ok

def _run_sl10b_delta_review(
    *,
    nl: str,
    old_dsl: str,
    candidate_dsl: str,
    fix_plan: FixPlan,
    cfg: DeterministicLoopConfig,
    iteration: int,
    llm_interactions: list[dict[str, Any]],
    logs: list[dict[str, Any]],
) -> tuple[dict[str, Any], ReviewRunMeta, StageResultMeta, bool]:
    prompt_version = "sl10b-delta-review.v1"
    diff_summary = {"old_dsl_hash": _hash_text(old_dsl), "candidate_dsl_hash": _hash_text(candidate_dsl), "fix_plan_target": fix_plan.target}
    prompt_messages = build_sl10b_delta_review_prompt(
        nl=nl,
        grounding_map=cfg.grounding_map,
        old_dsl=old_dsl,
        candidate_dsl=candidate_dsl,
        fix_plan=fix_plan,
        diff_summary=diff_summary,
        prompt_template_version=prompt_version,
    )
    raw_output, replay_key = _review_replay_lookup(cfg, StageId.SL_10B_DELTA_REVIEW, iteration)
    failure_policy = cfg.review_policy.review_meta_failure_policy(delta=True)
    provider = "fake-replay"
    model_id = "fake-sl10b-delta-review"
    usage: dict[str, Any] = {}
    attempts: list[dict[str, Any]] = []
    retry_count = 0
    note = "PR-2B fake/replay delta review; no real provider/API called"
    error: str | None = None
    schema_ok = False
    parsed: dict[str, Any]

    if cfg.review_provider_mode == "real_env":
        provider = "openai-compatible-env"
        replay_key = "real-env:" + replay_key
        note = "PR-3 real .env SL-10B delta review call recorded in AgentLoopRunRecord; provider/schema noise uses bounded retry"
        raw_output, usage, model_id, parsed, schema_ok, error, attempts, retry_count = _run_real_review_llm_with_retry(
            prompt_messages=prompt_messages,
            cfg=cfg,
            stage_id=StageId.SL_10B_DELTA_REVIEW,
            parser=parse_sl10b_delta_review_response,
            invalid_parsed_factory=lambda message: {
                "decision": "revise",
                "drift_risk": "major",
                "drift_evidence": [],
                "required_revision": [],
                "error": message,
            },
            logs=logs,
        )
    elif StageId.SL_10B_DELTA_REVIEW.value in cfg.review_provider_failures:
        raw_output = ""
        parsed = {"decision": "revise", "drift_risk": "major", "drift_evidence": [], "required_revision": [], "error": "provider failure"}
        error = "provider failure"
        provider = "fake-error"
        logs.append({"ts": _utc_now(), "level": "error", "event": "llm_review_provider_failure", "stage_id": StageId.SL_10B_DELTA_REVIEW.value})
    else:
        if raw_output is None and not cfg.review_policy.require_replay:
            raw_output = json.dumps({"decision": "accept", "drift_risk": "none", "drift_evidence": [], "required_revision": []}, ensure_ascii=False)
            replay_key = "default-fake:" + replay_key
        if raw_output is None:
            raw_output = ""
            parsed = {"decision": "revise", "drift_risk": "major", "drift_evidence": [], "required_revision": [], "error": "replay miss"}
            error = "replay miss"
            logs.append({"ts": _utc_now(), "level": "error", "event": "llm_review_replay_miss", "stage_id": StageId.SL_10B_DELTA_REVIEW.value, "replay_key": replay_key})
        else:
            try:
                parsed = parse_sl10b_delta_review_response(raw_output)
                schema_ok = True
            except Exception as e:  # pragma: no cover
                parsed = {"decision": "revise", "drift_risk": "major", "drift_evidence": [], "required_revision": [], "error": str(e)}
                error = str(e)
                logs.append({"ts": _utc_now(), "level": "error", "event": "llm_review_invalid_output", "stage_id": StageId.SL_10B_DELTA_REVIEW.value, "message": error})

    review_meta = _make_review_meta(
        provider=provider,
        model_id=model_id,
        prompt_template_version=prompt_version,
        prompt_messages=prompt_messages,
        raw_output=raw_output,
        parsed_schema_version="RepairReviewFeedback.delta_review.v1",
        schema_validation_ok=schema_ok,
        schema_validation_error=error,
        failure_policy=failure_policy,
        replay_key=replay_key,
        decision_threshold=cfg.review_policy.decision_threshold,
        seed=cfg.seed,
        retry_count=retry_count,
    )
    ok = schema_ok and parsed.get("decision") == "accept"
    meta = _llm_interaction_meta(StageId.SL_10B_DELTA_REVIEW, prompt_messages=prompt_messages, raw_output=raw_output, ok=ok or cfg.review_policy.delta_review_mode == "audit_only", validation_error=error)
    llm_interactions.append(
        _review_interaction_payload(
            stage_id=StageId.SL_10B_DELTA_REVIEW,
            prompt_messages=prompt_messages,
            raw_output=raw_output,
            parsed_output=parsed,
            review_meta=review_meta,
            schema_validation_ok=schema_ok,
            note=note,
            usage=usage,
            attempts=attempts,
        )
    )
    return parsed, review_meta, meta, not schema_ok

def _make_sl9_meta(prompt_messages: list[dict[str, str]], candidate_dsl: str, *, ok: bool = True) -> StageResultMeta:
    meta = _meta(StageId.SL_9_REPAIR, ok=ok, status=StageStatus.OK if ok else StageStatus.ERROR)
    meta.prompt_hash = _short_hash(prompt_messages)
    meta.output_hash = _hash_text(candidate_dsl)
    return meta


def _run_feedback_round(
    *,
    nl: str,
    current_dsl: str,
    scenario_set: ScenarioSet | None,
    grounding_map: GroundingMap | None,
    policy_profile: str,
    carried_warning_budget: dict[str, Any],
) -> tuple[StageContext, FeedbackBundle, list[StageResultMeta]]:
    context = StageContext(
        nl=nl,
        current_dsl=current_dsl,
        grounding_map=grounding_map,
        scenario_set=scenario_set,
        warning_budget_state=carried_warning_budget,
    )
    stage_results: list[StageResultMeta] = []

    parse_feedback, parse_meta = run_sd2_parse(current_dsl, context)
    stage_results.append(parse_meta)
    if not parse_feedback.ok:
        return context, _feedback_bundle(parse_feedback=parse_feedback, stage_results=stage_results), stage_results

    semantic_feedback, semantic_meta, _build = run_sd3_semantic(current_dsl, context)
    stage_results.append(semantic_meta)
    if not semantic_feedback.ok:
        return context, _feedback_bundle(
            parse_feedback=parse_feedback,
            semantic_feedback=semantic_feedback,
            stage_results=stage_results,
        ), stage_results

    design_feedback, design_meta = run_sd4_design(context, policy_profile=policy_profile)  # type: ignore[arg-type]
    stage_results.append(design_meta)
    bundle = _feedback_bundle(
        parse_feedback=parse_feedback,
        semantic_feedback=semantic_feedback,
        design_feedback=design_feedback,
        stage_results=stage_results,
    )
    if scenario_set is not None:
        sim_feedback, sim_meta = run_sd6_sim(current_dsl, scenario_set, context)
        stage_results.append(sim_meta)
        bundle.sim = sim_feedback
        bundle.stage_results.append(sim_meta)
    return context, bundle, stage_results


def _scenario_set_for_current_dsl(
    cfg: DeterministicLoopConfig,
    *,
    current_dsl: str,
    context: StageContext,
) -> tuple[ScenarioSet, list[StageResultMeta], dict[str, Any]]:
    coverage, coverage_meta = run_sd5a_scenario_coverage(current_dsl, cfg.scenarios)
    scenario_set, freeze_meta = freeze_scenario_set(
        cfg.scenarios,
        source_dsl_hash=_hash_text(current_dsl),
        source_inspect_hash=_short_hash(context.inspect_json) if context.inspect_json is not None else "",
        source_grounding_hash=_short_hash(cfg.grounding_map) if cfg.grounding_map is not None else None,
        coverage_report=coverage,
        epoch=0,
    )
    sl5_meta = _meta(StageId.SL_5_SCENARIO_GENERATION, ok=True)
    sl5_meta.output_hash = _short_hash(cfg.scenarios)
    return scenario_set, [sl5_meta, coverage_meta, freeze_meta], coverage


def _build_record(
    *,
    cfg: DeterministicLoopConfig,
    nl: str,
    status: str,
    current_dsl: str,
    run_started_at: str,
    stage_records: list[StageResultMeta],
    iteration_records: list[dict[str, Any]],
    llm_interactions: list[dict[str, Any]],
    deterministic_feedback: dict[str, Any],
    repair_history: list[dict[str, Any]],
    scenario_history: list[dict[str, Any]],
    logs: list[dict[str, Any]],
    error_message: str | None = None,
    force_invalid: bool = False,
) -> AgentLoopRunRecord:
    sanitized = force_invalid
    redaction_report: list[dict[str, Any]] = []
    nl_payload = _redact_run_record_payload(nl, "input_bundle.nl", redaction_report, affects_replay=True)
    path_context_redacted = _redact_run_record_payload(cfg.path_context, "input_bundle.path_context", redaction_report, affects_replay=True)
    iteration_records_redacted = _redact_run_record_payload(iteration_records, "iteration_records", redaction_report, affects_replay=True)
    llm_interactions_redacted = _redact_run_record_payload(llm_interactions, "llm_interactions", redaction_report, affects_replay=True)
    deterministic_feedback_redacted = _redact_run_record_payload(deterministic_feedback, "deterministic_feedback", redaction_report, affects_replay=True)
    repair_history_redacted = _redact_run_record_payload(repair_history, "repair_history", redaction_report, affects_replay=True)
    scenario_history_redacted = _redact_run_record_payload(scenario_history, "scenario_history", redaction_report, affects_replay=True)
    final_dsl_payload = _redact_run_record_payload(current_dsl, "final_artifacts.final_dsl", redaction_report, affects_replay=True)
    stage_records_redacted = _redact_run_record_payload([asdict(meta) for meta in stage_records], "stage_records", redaction_report, affects_replay=True)
    error_message_payload = _redact_run_record_payload(error_message, "final_artifacts.error_message", redaction_report, affects_replay=False)

    path_context_payload, changed = _strict_record_field("input_bundle.path_context", path_context_redacted, logs)
    sanitized = sanitized or changed
    iteration_records_payload, changed = _strict_record_field("iteration_records", iteration_records_redacted, logs)
    sanitized = sanitized or changed
    llm_interactions_payload, changed = _strict_record_field("llm_interactions", llm_interactions_redacted, logs)
    sanitized = sanitized or changed
    deterministic_feedback_payload, changed = _strict_record_field("deterministic_feedback", deterministic_feedback_redacted, logs)
    sanitized = sanitized or changed
    repair_history_payload, changed = _strict_record_field("repair_history", repair_history_redacted, logs)
    sanitized = sanitized or changed
    scenario_history_payload, changed = _strict_record_field("scenario_history", scenario_history_redacted, logs)
    sanitized = sanitized or changed
    final_dsl_payload, changed = _strict_record_field("final_artifacts.final_dsl", final_dsl_payload, logs)
    sanitized = sanitized or changed
    stage_records_payload, changed = _strict_record_field("stage_records", stage_records_redacted, logs)
    sanitized = sanitized or changed
    error_message_payload, changed = _strict_record_field("final_artifacts.error_message", error_message_payload, logs)
    sanitized = sanitized or changed
    logs_redacted = _redact_run_record_payload(logs, "logs", redaction_report, affects_replay=False)
    logs_payload, changed = _strict_record_field("logs", logs_redacted, logs)
    sanitized = sanitized or changed

    final_status = "invalid" if sanitized else status
    main_result_eligible = final_status == "success"
    record = AgentLoopRunRecord(
        schema_version=RUN_RECORD_SCHEMA_VERSION,
        run_id=cfg.run_id,
        created_at=run_started_at,
        status=final_status,  # type: ignore[arg-type]
        input_bundle={
            "nl": nl_payload,
            "initial_dsl_hash": _hash_text(cfg.initial_dsl),
            "path_context": path_context_payload,
        },
        run_config={
            "max_iterations": cfg.max_iterations,
            "policy_profile": cfg.policy_profile,
            "seed": cfg.seed,
            "sl9_mode": "fake_replay_candidate_injection",
            "review_policy": asdict(cfg.review_policy),
            "review_mode": cfg.review_provider_mode,
            "review_model": cfg.review_model,
            "review_max_tokens": cfg.review_max_tokens,
            "review_max_retries": cfg.review_max_retries,
            "real_llm_provider_api": cfg.review_provider_mode == "real_env",
        },
        environment=_environment(),
        stage_graph={
            "planned": SC_0_STAGE_GRAPH,
            "executed": _stage_ids(stage_records),
        },
        stage_records=stage_records_payload,
        iteration_records=iteration_records_payload,
        llm_interactions=llm_interactions_payload,
        deterministic_feedback=deterministic_feedback_payload,
        repair_history=repair_history_payload,
        scenario_history=scenario_history_payload,
        final_artifacts={
            "final_dsl": final_dsl_payload,
            "final_dsl_hash": _hash_text(current_dsl),
            "verdict": final_status,
            "main_result_eligible": main_result_eligible,
            "path_result_filter": "include only status == success and main_result_eligible == true",
            "error_message": error_message_payload,
        },
        logs=logs_payload,
        replay_index={
            "stage_by_index": {str(i): meta.stage_id for i, meta in enumerate(stage_records)},
            "iteration_count": len(iteration_records),
            "record_replay_command": "python -m method.run_record <path>",
        },
        redaction_report=redaction_report,
    )
    return record


def run_deterministic_ablation_loop(nl: str, cfg: DeterministicLoopConfig) -> AgentLoopResult:
    """Run the deterministic ablation loop and persist a run record."""
    run_id = cfg.run_id or "pr2a-" + hashlib.sha256(f"{nl}\n{cfg.initial_dsl}".encode("utf-8")).hexdigest()[:12]
    cfg.run_id = run_id
    run_started_at = _utc_now()
    result = AgentLoopResult(llm_model="fake-none")
    stage_records: list[StageResultMeta] = []
    iteration_records: list[dict[str, Any]] = []
    llm_interactions: list[dict[str, Any]] = []
    repair_history: list[dict[str, Any]] = []
    scenario_history: list[dict[str, Any]] = []
    deterministic_feedback: dict[str, Any] = {"iterations": []}
    logs: list[dict[str, Any]] = []
    current_dsl = cfg.initial_dsl
    status = "failed"
    error_message: str | None = None
    warning_budget_state: dict[str, Any] = {}
    pending_rejection = None
    pending_original_plan: FixPlan | None = None
    force_invalid_record = False

    _append_stage(stage_records, _meta(StageId.SC_0_START, ok=True))

    scenario_set: ScenarioSet | None = None

    for iteration in range(max(1, cfg.max_iterations)):
        context, bundle, feedback_stage_results = _run_feedback_round(
            nl=nl,
            current_dsl=current_dsl,
            scenario_set=scenario_set,
            grounding_map=cfg.grounding_map,
            policy_profile=cfg.policy_profile,
            carried_warning_budget=warning_budget_state,
        )
        warning_budget_state = context.warning_budget_state
        if iteration == 0 and scenario_set is None:
            stage_records.extend(feedback_stage_results)
            if bundle.parse is not None and bundle.parse.ok and bundle.semantic is not None and bundle.semantic.ok:
                scenario_set, scenario_stage_metas, _coverage = _scenario_set_for_current_dsl(
                    cfg,
                    current_dsl=current_dsl,
                    context=context,
                )
                context.scenario_set = scenario_set
                scenario_history.append(asdict(scenario_set))
                sim_feedback, sim_meta = run_sd6_sim(current_dsl, scenario_set, context)
                bundle.sim = sim_feedback
                bundle.stage_results.append(sim_meta)
                feedback_stage_results.append(sim_meta)
                trace_sim_rows = [sim_meta]
            else:
                scenario_stage_metas = []
                trace_sim_rows = []
            stage_records.extend(scenario_stage_metas)
            stage_records.extend(trace_sim_rows)
        else:
            stage_records.extend(feedback_stage_results)

        if cfg.review_policy.enable_model_review and bundle.sim is not None and bundle.sim.ok:
            model_review, model_review_meta, model_review_invalid = _run_sl7_model_review(
                nl=nl,
                current_dsl=current_dsl,
                context=context,
                bundle=bundle,
                cfg=cfg,
                iteration=iteration,
                llm_interactions=llm_interactions,
                logs=logs,
            )
            bundle.model_review = model_review
            bundle.enabled_sources.append(FeedbackSource.MODEL_REVIEW.value)
            bundle.stage_results.append(model_review_meta)
            feedback_stage_results.append(model_review_meta)
            stage_records.append(model_review_meta)
            force_invalid_record = force_invalid_record or model_review_invalid

        selected = _select_feedback(bundle, cfg.review_policy)
        design_payload = asdict(bundle.design) if bundle.design is not None else None
        sim_payload = asdict(bundle.sim) if bundle.sim is not None else None
        deterministic_feedback["iterations"].append(
            {
                "iteration": iteration,
                "parse": asdict(bundle.parse) if bundle.parse is not None else None,
                "semantic": asdict(bundle.semantic) if bundle.semantic is not None else None,
                "design": design_payload,
                "sim": sim_payload,
                "model_review": asdict(bundle.model_review) if bundle.model_review is not None else None,
            }
        )
        trace = IterTrace(
            iteration=iteration,
            model=ModelArtifact(dsl_text=current_dsl, iteration=iteration, produced_by="modeler" if iteration == 0 else "repair"),
            feedback=bundle,
            stage_results=list(feedback_stage_results),
            stage_context_summary=asdict(context.to_summary()),
            warning_budget_state=dict(context.warning_budget_state),
            scenario_epoch=scenario_set.epoch if scenario_set is not None else None,
        )
        result.iter_traces.append(trace)

        iteration_record: dict[str, Any] = {
            "iteration": iteration,
            "dsl_hash": _hash_text(current_dsl),
            "stage_ids": _stage_ids(feedback_stage_results),
            "stage_context_summary": asdict(context.to_summary()),
            "warning_budget_state": {k: asdict(v) for k, v in context.warning_budget_state.items()},
            "scenario_epoch": scenario_set.epoch if scenario_set is not None else None,
            "selected_feedback": None,
            "repair_review": None,
            "model_review": asdict(bundle.model_review) if bundle.model_review is not None else None,
        }

        if selected is None:
            _append_stage(stage_records, _meta(StageId.SC_12_EXIT, ok=True))
            status = "success"
            iteration_record["exit_reason"] = "all_required_feedback_ok"
            iteration_records.append(iteration_record)
            result.status = "converged"
            break

        source, feedback, source_stage = selected
        iteration_record["selected_feedback"] = {"source": source, "source_stage": source_stage}

        pending_retry = pending_rejection is not None and pending_original_plan is not None
        candidate_available = iteration < len(cfg.repair_candidates)
        if not candidate_available or (iteration >= cfg.max_iterations - 1 and not pending_retry):
            _append_stage(stage_records, _meta(StageId.SC_12_EXIT, ok=False, status=StageStatus.FAIL))
            status = "failed"
            error_message = "repair budget exhausted or no deterministic candidate available"
            iteration_record["exit_reason"] = error_message
            iteration_records.append(iteration_record)
            result.status = "not_converged"
            break

        if pending_rejection is not None and pending_original_plan is not None:
            fix_plan, fix_meta = run_sd8_fix_plan(
                None,
                source="repair_review",
                rejection=pending_rejection,
                original=pending_original_plan,
            )
        else:
            fix_plan, fix_meta = run_sd8_fix_plan(
                feedback,
                source=source,
                source_stage=source_stage,
                grounding_map=cfg.grounding_map,
                before_dsl=current_dsl,
            )
        _append_stage(stage_records, fix_meta)
        if isinstance(fix_plan, RevisedFixPlan):
            effective_fix_plan = fix_plan.original
            plan_kind = "RevisedFixPlan"
        else:
            effective_fix_plan = fix_plan
            plan_kind = "FixPlan"
        assert isinstance(effective_fix_plan, FixPlan)

        candidate_dsl = cfg.repair_candidates[min(iteration, len(cfg.repair_candidates) - 1)]
        prompt_messages = build_sl9_repair_prompt(
            nl=nl,
            current_dsl=current_dsl,
            fix_plan=fix_plan,
            grounding_map=cfg.grounding_map,
            selected_diagnostics=effective_fix_plan.evidence,
            preserve_list=effective_fix_plan.required_preserve_element_ids,
            scenario_summary={
                "scenario_set_id": scenario_set.scenario_set_id if scenario_set is not None else None,
                "epoch": scenario_set.epoch if scenario_set is not None else None,
                "n_scenarios": len(scenario_set.scenarios) if scenario_set is not None else 0,
            },
        )
        sl9_meta = _make_sl9_meta(prompt_messages, candidate_dsl)
        _append_stage(stage_records, sl9_meta)
        llm_interactions.append(
            {
                "stage_id": StageId.SL_9_REPAIR.value,
                "provider": "fake",
                "model_id": "deterministic-candidate-injection",
                "prompt_template_version": "sl9-repair.v1",
                "prompt_hash": sl9_meta.prompt_hash,
                "input_hash": _hash_text(current_dsl),
                "raw_output_hash": sl9_meta.output_hash,
                "prompt_messages": prompt_messages,
                "raw_output": candidate_dsl,
                "parsed_output": {"candidate_dsl": candidate_dsl},
                "schema_validation_ok": True,
                "replay_key": f"fake-sl9:{run_id}:{iteration}",
                "note": "PR-2A never calls a real LLM provider/API.",
            }
        )
        if source == FeedbackSource.DESIGN.value and bundle.design is not None:
            mark_warning_repair_attempt(
                context.warning_budget_state,
                [item.instance_key for item in bundle.design.blocking_items],
            )

        repair_review, repair_review_meta = run_sd10_repair_review(
            nl=nl,
            grounding_map=cfg.grounding_map,
            old_dsl=current_dsl,
            candidate_dsl=candidate_dsl,
            fix_plan=effective_fix_plan,
            scenario_set=scenario_set,
        )
        _append_stage(stage_records, repair_review_meta)
        if repair_review.ok and cfg.review_policy.enable_delta_review:
            delta_review, delta_meta, delta_stage_meta, delta_invalid = _run_sl10b_delta_review(
                nl=nl,
                old_dsl=current_dsl,
                candidate_dsl=candidate_dsl,
                fix_plan=effective_fix_plan,
                cfg=cfg,
                iteration=iteration,
                llm_interactions=llm_interactions,
                logs=logs,
            )
            _append_stage(stage_records, delta_stage_meta)
            force_invalid_record = force_invalid_record or delta_invalid
            repair_review.delta_review = delta_review
            repair_review.review_meta = delta_meta
            if cfg.review_policy.is_delta_review_blocking_reject(delta_review):
                rejection = RepairRejection(
                    rejected_by_stage=StageId.SL_10B_DELTA_REVIEW.value,
                    reason="delta_review_" + str(delta_review.get("decision", "reject")),
                    target_resolved=False,
                    regression_detected=repair_review.regression_detected,
                    drift_risk=delta_review.get("drift_risk", "major"),
                    evidence=delta_review.get("drift_evidence", []),
                )
                repair_review.ok = False
                repair_review.target_resolved = False
                repair_review.drift_risk = rejection.drift_risk
                repair_review.local_rejection = rejection
        iteration_record["repair_review"] = asdict(repair_review)
        trace.repair_review = repair_review
        repair_history.append(
            {
                "iteration": iteration,
                "plan_kind": plan_kind,
                "fix_plan": asdict(effective_fix_plan),
                "revised_fix_plan": asdict(fix_plan) if isinstance(fix_plan, RevisedFixPlan) else None,
                "candidate_dsl": candidate_dsl,
                "candidate_dsl_hash": _hash_text(candidate_dsl),
                "repair_review": asdict(repair_review),
                "accepted": repair_review.ok,
            }
        )
        if repair_review.ok:
            _append_stage(stage_records, _meta(StageId.SC_11_ACCEPT_CANDIDATE, ok=True))
            trace.repair = ModelArtifact(dsl_text=candidate_dsl, iteration=iteration + 1, produced_by="repair")
            current_dsl = candidate_dsl
            iteration_record["accepted_candidate"] = True
            iteration_record["exit_reason"] = "candidate_accepted_by_repair_review"
            pending_rejection = None
            pending_original_plan = None
            iteration_records.append(iteration_record)
            if iteration >= cfg.max_iterations - 1:
                _append_stage(stage_records, _meta(StageId.SC_12_EXIT, ok=True))
                status = "success"
                result.status = "converged"
                break
            continue

        pending_rejection = repair_review.local_rejection
        pending_original_plan = effective_fix_plan
        if iteration < cfg.max_iterations - 1 and iteration + 1 < len(cfg.repair_candidates) and pending_rejection is not None:
            _append_stage(stage_records, _meta(StageId.SC_11_ACCEPT_CANDIDATE, ok=False, status=StageStatus.FAIL))
            iteration_record["accepted_candidate"] = False
            iteration_record["exit_reason"] = "repair_review_rejected_retry_with_revised_fix_plan"
            iteration_records.append(iteration_record)
            continue

        _append_stage(stage_records, _meta(StageId.SC_11_ACCEPT_CANDIDATE, ok=False, status=StageStatus.FAIL))
        _append_stage(stage_records, _meta(StageId.SC_12_EXIT, ok=False, status=StageStatus.FAIL))
        status = "rejected"
        error_message = repair_review.local_rejection.reason if repair_review.local_rejection else "repair rejected"
        iteration_record["accepted_candidate"] = False
        iteration_record["exit_reason"] = error_message
        iteration_records.append(iteration_record)
        result.status = "not_converged"
        break
    else:
        _append_stage(stage_records, _meta(StageId.SC_12_EXIT, ok=False, status=StageStatus.FAIL))
        status = "budget_exhausted"
        error_message = "max_iterations exhausted"
        result.status = "not_converged"

    result.final_dsl = current_dsl
    result.final_artifact = ModelArtifact(dsl_text=current_dsl, iteration=len(result.iter_traces), produced_by="repair")
    result.final_feedback = result.iter_traces[-1].feedback if result.iter_traces else None
    result.error_message = error_message

    trace_meta = _meta(StageId.SC_13_TRACE_AUDIT, ok=True)
    _append_stage(stage_records, trace_meta)
    record = _build_record(
        cfg=cfg,
        nl=nl,
        status=status,
        current_dsl=current_dsl,
        run_started_at=run_started_at,
        stage_records=stage_records,
        iteration_records=iteration_records,
        llm_interactions=llm_interactions,
        deterministic_feedback=deterministic_feedback,
        repair_history=repair_history,
        scenario_history=scenario_history,
        logs=logs,
        error_message=error_message,
        force_invalid=force_invalid_record,
    )
    path = write_agent_loop_run_record(record, agent_loop_run_record_path(cfg.output_dir, run_id))
    result.run_record_path = str(path)
    result.run_record_id = run_id
    return result


# Historical compatibility alias. New code should import and call
# run_deterministic_ablation_loop from this module.
run_pr2a_deterministic_loop = run_deterministic_ablation_loop


__all__ = [
    "DeterministicLoopConfig",
    "ReviewPolicy",
    "run_deterministic_ablation_loop",
    "run_pr2a_deterministic_loop",
]
