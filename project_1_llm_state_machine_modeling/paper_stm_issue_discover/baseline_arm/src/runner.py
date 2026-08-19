"""单格执行：读 NL + PlantUML → 一次 LLM 调用 → 落一份自包含的可审计 record。

⛔ **本模块不 import 主臂（`paper_stm_feedback_loop`）的任何东西**，只用仓库根的 `utils.llm`。
判据与理由见 [../tests/test_isolation.py](../tests/test_isolation.py) 的 docstring：取「一个模块
都不进来」这个最强形态，代价是 transport 重试要自己写。

⚠️ **transport 重试的节奏不是随便定的**，照主臂踩过的坑：三次重试若相隔几微秒发出，会全部落进
同一个网关超时窗口，于是「重试三次」与「只试一次」结果完全相同，只是多花了时间。所以延迟必须
长于一个网关超时，且长到限流有机会清空。

## 失败处理（仓库根 `CLAUDE.md` §10）

只有两类允许整格失败：**provider 侧错误**、**schema 穷尽重试仍失败**。⭐ 但即使失败，本模块
**照旧落盘 record**（`status="failed"` + `failure`），⛔ 不静默丢格——一个没有产物的格等于该
样本从被测集里消失，而最容易失败的恰恰是信息量最大的那些格。

⚠️ schema 类失败**本身就是必须修的缺陷**，⛔ 不许靠调大重试次数了事：解析错误会作为定向反馈
回灌给同一次调用的下一轮（`schema_retry_feedback`），把模型引导到正确结构是我们的义务。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import uuid
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# 仓库根必须在 sys.path 上才能 `from utils.llm import ...`。
# ⚠️ parents[4] 是仓库根（本文件在 <repo>/project_1_.../paper_stm_issue_discover/baseline_arm/src/）。
# 搬迁本文件时必须同步改这个数字，否则会静默解析到错误目录。
_REPO_ROOT = Path(__file__).resolve().parents[4]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from schema import NaiveReview
from utils.llm import (
    adapter_name,
    create_chat_model,
    load_llm_registry,
    normalize_model_output_usage,
)

#: prompt 的唯一真源。⛔ 不在本文件内联副本（理由见 ../prompt/README.md 开头）。
PROMPT_FILE = _HERE.parents[0] / "prompt" / "naive_v1.txt"

#: 输入语料根。与主臂 `discover/cli.py` 的 `REPORT_ROOT` 指向**同一个目录**。
#:
#: ⛔⛔ **但两臂读的不是同一份文件，此前这里写错了。** 实测（`grep -rn 'plantuml|\.puml'` 主臂
#: 源码树只有一处注释命中）：
#:
#:   * X1  读 `pairs/<case>/nl.txt` + `pairs/<case>/plantuml.puml`（**作者源**）
#:   * 主臂读 `pairs/<case>/nl.txt` + `pairs/<case>/fcstm.fcstm`（**编译产物**）
#:     + `source_traces/` + `working_contracts/`
#:
#: ⭐ 唯一真正共用的是 `nl.txt`。⚠️ 这**不是**不公平——模型转换是 C-① 的一环，所以主臂只能看
#: 自己转换出来的中间表示，那是方法自身的代价。⛔ 但它必须被披露，因为**台账缺陷是按作者源标的**：
#: 转换既会擦掉缺陷（pair 0000 的 `state HumanDrivingMode { }` 空复合体在 fcstm 里变成普通
#: state），也会注入编译噪声。⚠️ ⛔ 两个方向都对主臂不利 —— ⛔⛔ 2026-08-12 更正：**这句不成立**。擦除方向确实存在但很小（5 个空复合体被压平、14 处身份重映射、16 行动作丢原文）；⛔ 而**显式化方向是净增益**（40 个合成状态 100% 是诊断命名，⛔ 诊断结论被直接写进状态名）。⭐ 活体激活口径下 main-only 9 位 = 1.53pp。见 talk §5.6.2。见 `preregistered.md` §9.1。
#: ⚠️ `_HERE.parents[1]` 已经是 `paper_stm_issue_discover`（初版误加了一层 `.parent`，指到了
#: `project_1_llm_state_machine_modeling`，`test_real_corpus_has_54_in_scope_pairs` 抓住了它）。
REPORT_ROOT = (
    _HERE.parents[1] / "pipeline" / "representation" / "reports" / "llms_emp_r45_java_60"
)

#: 重试前等待的秒数。⚠️ 刻意长于一个网关超时（见模块 docstring）。
TRANSPORT_RETRY_DELAYS: tuple[float, ...] = (5.0, 20.0, 60.0, 120.0, 240.0)

#: schema 解析失败的原地重试次数。⚠️ 调大这个数**不是** schema 失败的解法（`CLAUDE.md` §10）：
#: 反复失败说明 prompt / schema 设计有缺陷，要修设计。这里给的是吸收偶发结构抖动的余量。
SCHEMA_RETRIES = 2

SCHEMA_VERSION = "x1-baseline-arm/1"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_prompts(*, nl: str, plantuml: str, content_language: str) -> tuple[str, str]:
    """渲染 (system, user)。

    ⭐ system 来自 `prompt/naive_v1.txt`，只替换 `{content_language}` 一个占位符。
    ⭐ user 只是两份输入的容器：⛔ 没有任何引导语、⛔ 没有摘要、⛔ 没有截断。
    """

    template = PROMPT_FILE.read_text(encoding="utf-8")
    system = template.replace("{content_language}", content_language).strip()
    user = (
        "## Natural-language specification\n\n"
        f"{nl}\n\n"
        "## State machine model (PlantUML)\n\n"
        f"{plantuml}\n"
    )
    return system, user


def schema_retry_feedback(error_text: str) -> str:
    """把一次结构校验失败改写成**定向**反馈。

    ⛔ 只许携带结构信息（哪个字段、期望什么形状），⛔ 不许携带任何内容引导——否则它就是一条
    只在特定样本上触发的泄漏通道，而静态 grep prompt 常量抓不到它（`CLAUDE.md` §3.5.-1）。

    ⚠️ pydantic 的错误文本里可能出现输入片段（模型自己写的状态名之类）。那些片段来自模型自己
    的输出，回灌给它不构成我们的引导；但为了让本函数的输出可以被机械断言为「纯结构」，这里
    **只保留字段路径与错误类型**，把其余内容丢掉。
    """

    paths: list[str] = []
    for line in error_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("For further information"):
            continue
        # pydantic 的错误块形如 "issues.0.reason" 后跟一行缩进的说明。
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z0-9_]+)*", stripped):
            paths.append(stripped)
    detail = ", ".join(dict.fromkeys(paths)) or "(field path not reported)"
    return (
        "Your previous response did not satisfy the required output structure. "
        f"Offending field path(s): {detail}. "
        "Re-emit the same findings in the exact structure requested, filling every "
        "required field of every item. Do not change what you found."
    )


def load_pair(case: str, *, report_root: Path | None = None) -> dict[str, str]:
    """读一个 pair 的两份输入。⛔ 全文，⛔ 不截断。"""

    root = (report_root or REPORT_ROOT).expanduser().resolve()
    pair_dir = root / "pairs" / case
    nl_path = pair_dir / "nl.txt"
    puml_path = pair_dir / "plantuml.puml"
    for path in (nl_path, puml_path):
        if not path.is_file():
            raise FileNotFoundError(f"missing baseline-arm input: {path}")
    return {
        "nl": nl_path.read_text(encoding="utf-8"),
        "plantuml": puml_path.read_text(encoding="utf-8"),
        "nl_path": str(nl_path),
        "plantuml_path": str(puml_path),
    }


def _status_code(exc: BaseException) -> int | None:
    value = getattr(exc, "status_code", None)
    if isinstance(value, int):
        return value
    response = getattr(exc, "response", None)
    value = getattr(response, "status_code", None)
    return value if isinstance(value, int) else None


def _relay_upstream_failure(exc: BaseException) -> bool:
    """Recognize Hahacode's structured upstream outage receipt.

    The relay can encode an upstream outage as HTTP 400. This is intentionally
    a narrow diagnostic check, not a semantic or NL rule: ordinary malformed
    requests remain non-retryable.
    """

    body = getattr(exc, "body", None)
    if not isinstance(body, Mapping):
        return False
    error = body.get("error", body)
    if not isinstance(error, Mapping):
        return False
    message = error.get("message")
    if not isinstance(message, str) or not message.startswith("Upstream request failed"):
        return False
    return error.get("type") == "invalid_request_error" or (
        error.get("code") == "upstream_error" and error.get("type") == "new_api_error"
    )


def _retryable_provider_error(exc: BaseException) -> bool:
    """Return whether a failed call is eligible for a transport retry.

    A missing status code is not evidence of a provider failure.  In particular,
    local programming errors and unexpected SDK/value errors must be recorded and
    stopped rather than replayed as if the gateway were at fault.
    """

    if _relay_upstream_failure(exc):
        return True
    status = _status_code(exc)
    if status is not None:
        return status in {408, 409, 425, 429} or status >= 500
    return isinstance(exc, (ConnectionError, TimeoutError))


def _retry_after_seconds(exc: BaseException) -> float | None:
    """provider 自己说的等待时长优先于任何固定节奏——尊重它能避免 429 被重试成另一个 429。"""

    response = getattr(exc, "response", None)
    headers = getattr(response, "headers", None)
    if headers is None:
        return None
    try:
        raw = headers.get("retry-after") or headers.get("Retry-After")
    except (AttributeError, TypeError, ValueError):  # pragma: no cover - defensive
        return None
    if raw is None:
        return None
    try:
        value = float(str(raw).strip())
    except ValueError:
        return None
    return value if value >= 0 else None


def _is_schema_error(exc: BaseException) -> bool:
    """结构校验失败 vs transport 失败——两者的正确处置完全不同。"""

    name = type(exc).__name__
    if name in {"ValidationError", "OutputParserException"}:
        return True
    return callable(getattr(exc, "errors", None)) and _status_code(exc) is None


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    return repr(value)


def run_cell(
    *,
    case: str,
    profile: str,
    content_language: str = "zh-CN",
    report_root: Path | None = None,
    registry_path: str | None = None,
    transport_retries: int = 4,
    streaming: bool | None = None,
    round_index: int | None = None,
    arm_label: str | None = None,
) -> dict[str, Any]:
    """跑一格，返回自包含的 record。⛔ 本函数不抛异常给调用方；失败也返回 record。"""

    started = _utc_now()
    start_ns = time.perf_counter_ns()
    inputs = load_pair(case, report_root=report_root)
    system, user = build_prompts(
        nl=inputs["nl"], plantuml=inputs["plantuml"], content_language=content_language
    )

    registry = load_llm_registry(registry_path)
    config = registry.require(profile)
    # `adapter` 是 config 上的枚举值（决定 structured-output 的调用方式）；
    # `provider` 是它的稳定 transport 名，进 record 供审计。⚠️ `adapter_name` 收字符串，
    # ⛔ 不收 config——初版传了 config，报错文本把整个 config 打了出来。
    adapter = config.adapter
    provider = adapter_name(adapter)
    # Streaming is the repository-wide transport default.  The caller may
    # explicitly opt out with ``streaming=False`` / ``--no-stream``; adapter
    # selection must not silently change the timeout behavior of a cell.
    effective_streaming = True if streaming is None else streaming
    model = create_chat_model(
        config, streaming=effective_streaming, max_retries=0
    )

    structured_options: dict[str, Any] = {"include_raw": True}
    if adapter in {"openai", "openai-responses"}:
        # OpenAI 的 response_format JSON-schema 子集会拒绝 pydantic 的默认值与联合类型
        # （本 schema 的 `analysis: str | None` 正是那种情况）。function calling 接受它，
        # 且仍然是一次直接的模型响应，⛔ 不是工具循环。
        structured_options["method"] = "function_calling"
    structured = model.with_structured_output(NaiveReview, **structured_options)

    from langchain_core.messages import HumanMessage, SystemMessage

    attempts: list[dict[str, Any]] = []
    parsed: NaiveReview | None = None
    usage: dict[str, Any] = {}
    observed_model: str | None = None
    failure: str | None = None
    schema_feedback: str | None = None
    schema_failures = 0
    transport_failures = 0
    terminal_failure_class: str | None = None

    total_budget = transport_retries + SCHEMA_RETRIES + 1
    for attempt_index in range(1, total_budget + 1):
        attempt_started = _utc_now()
        attempt_start_ns = time.perf_counter_ns()
        messages: list[Any] = [SystemMessage(content=system)]
        if schema_feedback is None:
            messages.append(HumanMessage(content=user))
        else:
            messages.append(HumanMessage(content=f"{user}\n\n{schema_feedback}"))
        try:
            response = structured.invoke(messages)
            raw = response.get("raw") if isinstance(response, dict) else None
            value = response.get("parsed") if isinstance(response, dict) else response
            parsing_error = (
                response.get("parsing_error") if isinstance(response, dict) else None
            )
            if parsing_error is not None:
                raise parsing_error
            if value is None:
                raise ValueError("provider returned no parsed structured output")
            parsed = value
            usage = normalize_model_output_usage(raw) or {}
            metadata = getattr(raw, "response_metadata", None) or {}
            observed = metadata.get("model_name") or metadata.get("model")
            observed_model = str(observed) if observed else None
            attempts.append(
                {
                    "attempt": attempt_index,
                    "kind": "schema_retry" if schema_feedback else "initial",
                    "status": "ok",
                    "retryable": False,
                    "will_retry": False,
                    "cost_counted": True,
                    "billing_disposition": "counted",
                    "started_at": attempt_started.isoformat(),
                    "elapsed_ms": (time.perf_counter_ns() - attempt_start_ns) / 1e6,
                }
            )
            break
        except Exception as exc:  # noqa: BLE001 - 分类后分别处置，见下
            schema_error = _is_schema_error(exc)
            provider_error = _retryable_provider_error(exc)
            if schema_error:
                status = "schema_error"
                retryable = False
                schema_failures += 1
                will_retry = schema_failures <= SCHEMA_RETRIES
                # Schema repair is a billable business correction, not a free
                # transport retry, even though it is issued in the same node.
                cost_counted = True
                billing_disposition = "counted"
                failure_class = "schema_exhausted"
            elif provider_error:
                status = "provider_error"
                retryable = True
                transport_failures += 1
                will_retry = transport_failures <= transport_retries
                cost_counted = not will_retry
                billing_disposition = (
                    "provider_error_retry_exempt" if will_retry else "counted"
                )
                failure_class = "transport_exhausted"
            else:
                status = "internal_error"
                retryable = False
                will_retry = False
                cost_counted = True
                billing_disposition = "counted"
                failure_class = "internal_error"
            attempts.append(
                {
                    "attempt": attempt_index,
                    "kind": "schema_retry" if schema_feedback else "initial",
                    "status": status,
                    "retryable": retryable,
                    "will_retry": will_retry,
                    "cost_counted": cost_counted,
                    "billing_disposition": billing_disposition,
                    "error_type": type(exc).__name__,
                    "error": str(exc)[:4000],
                    "status_code": _status_code(exc),
                    "started_at": attempt_started.isoformat(),
                    "elapsed_ms": (time.perf_counter_ns() - attempt_start_ns) / 1e6,
                }
            )
            if schema_error:
                if not will_retry:
                    failure = f"schema exhausted after {schema_failures} attempts: {exc}"
                    terminal_failure_class = failure_class
                    break
                schema_feedback = schema_retry_feedback(str(exc))
                continue
            if not provider_error:
                failure = f"internal error after {attempt_index} attempt(s): {exc}"
                terminal_failure_class = failure_class
                break
            if not will_retry:
                failure = f"transport exhausted after {transport_failures} attempts: {exc}"
                terminal_failure_class = failure_class
                break
            hinted = _retry_after_seconds(exc)
            delay = (
                hinted
                if hinted is not None
                else TRANSPORT_RETRY_DELAYS[
                    min(transport_failures - 1, len(TRANSPORT_RETRY_DELAYS) - 1)
                ]
            )
            time.sleep(delay)

    finished = _utc_now()
    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "arm": "naive_baseline",
        "cell_id": uuid.uuid4().hex,
        "case": case,
        "pair_id": f"llms_emp_feedback_final_{case}",
        "round": round_index,
        "arm_label": arm_label,
        "profile": profile,
        "adapter": adapter,
        "provider": provider,
        "streaming": effective_streaming,
        "configured_model": config.model,
        "observed_model": observed_model,
        "content_language": content_language,
        # ⭐ 证明「没压输出预算」：记录 profile 声明的上限，且本 runner 从不覆盖它。
        "profile_max_output_tokens": config.max_output_tokens,
        "profile_context_window_tokens": config.context_window_tokens,
        "max_output_tokens_override": None,
        "temperature_override": None,
        "prompt_file": str(PROMPT_FILE.relative_to(PROMPT_FILE.parents[2])),
        "prompt_sha256": sha256_text(PROMPT_FILE.read_text(encoding="utf-8")),
        "system_prompt": system,
        "user_prompt": user,
        "inputs": {
            "nl_path": inputs["nl_path"],
            "plantuml_path": inputs["plantuml_path"],
            "nl_sha256": sha256_text(inputs["nl"]),
            "plantuml_sha256": sha256_text(inputs["plantuml"]),
            "nl_chars": len(inputs["nl"]),
            "plantuml_chars": len(inputs["plantuml"]),
            "truncated": False,
        },
        "started_at": started.isoformat(),
        "finished_at": finished.isoformat(),
        "elapsed_ms": (time.perf_counter_ns() - start_ns) / 1e6,
        "status": "ok" if parsed is not None else "failed",
        "failure": failure,
        "failure_class": (
            None
            if parsed is not None
            else (terminal_failure_class or ("schema_exhausted" if schema_failures > SCHEMA_RETRIES else "transport_exhausted"))
        ),
        "parsed_output": _jsonable(parsed) if parsed is not None else None,
        "issue_count": len(parsed.issues) if parsed is not None else None,
        "usage": _jsonable(usage),
        "attempts": attempts,
    }
    return record


def write_record(record: dict[str, Any], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "record.json"
    path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run one naive-baseline cell (single prompt, no loop, no tools)."
    )
    parser.add_argument("--case", required=True, help="four-digit pair id, e.g. 0000")
    parser.add_argument("--profile", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--content-language", choices=("zh-CN", "en-US"), default="zh-CN")
    parser.add_argument("--report-root", default=None)
    parser.add_argument("--llm-config", default=None)
    parser.add_argument("--transport-retries", type=int, default=4)
    stream_mode = parser.add_mutually_exclusive_group()
    stream_mode.add_argument(
        "--stream",
        dest="streaming",
        action="store_true",
        help="Force streaming responses (the default).",
    )
    stream_mode.add_argument(
        "--no-stream",
        dest="streaming",
        action="store_false",
        help="Force complete non-streaming responses.",
    )
    parser.set_defaults(streaming=True)
    parser.add_argument("--round", type=int, default=None)
    parser.add_argument("--arm-label", default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    record = run_cell(
        case=args.case,
        profile=args.profile,
        content_language=args.content_language,
        report_root=Path(args.report_root) if args.report_root else None,
        registry_path=args.llm_config,
        transport_retries=args.transport_retries,
        streaming=args.streaming,
        round_index=args.round,
        arm_label=args.arm_label,
    )
    path = write_record(record, Path(args.output_dir))
    print(
        f"[{record['status']}] case={record['case']} profile={record['profile']} "
        f"issues={record['issue_count']} -> {path}"
    )
    # ⭐ 失败也落盘（见模块 docstring），但退出码要能被编排层看见。
    return 0 if record["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
