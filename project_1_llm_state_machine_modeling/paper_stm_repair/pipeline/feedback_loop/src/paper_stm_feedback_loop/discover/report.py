from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from .schemas import DiscoverGraphState, LLMCallRecord, NodeExecutionRecord


def telemetry_summary(
    nodes: list[NodeExecutionRecord], calls: list[LLMCallRecord]
) -> dict[str, Any]:
    node_elapsed: dict[str, float] = defaultdict(float)
    role_elapsed: dict[str, float] = defaultdict(float)
    role_tokens: dict[str, dict[str, int]] = defaultdict(
        lambda: {"input": 0, "output": 0, "total": 0}
    )
    totals: dict[str, int | None] = {}
    for field in (
        "input_tokens",
        "output_tokens",
        "total_tokens",
        "cache_read_input_tokens",
        "cache_creation_input_tokens",
        "reasoning_tokens",
    ):
        observed = [
            getattr(call, field) for call in calls if getattr(call, field) is not None
        ]
        totals[field] = sum(observed) if observed else None
    for record in nodes:
        node_elapsed[record.node_name] += record.elapsed_ms
    for call in calls:
        role_elapsed[call.role] += call.elapsed_ms
        for field, key in (
            ("input_tokens", "input"),
            ("output_tokens", "output"),
            ("total_tokens", "total"),
        ):
            value = getattr(call, field)
            if value is not None:
                role_tokens[call.role][key] += value
    return {
        "node_count": len(nodes),
        "llm_call_count": len(calls),
        "transport_attempt_count": sum(len(call.transport_attempts) for call in calls),
        "retry_count": sum(max(0, len(call.transport_attempts) - 1) for call in calls),
        "node_elapsed_ms_sum": sum(record.elapsed_ms for record in nodes),
        "llm_elapsed_ms_sum": sum(call.elapsed_ms for call in calls),
        "node_elapsed_ms_by_name": dict(sorted(node_elapsed.items())),
        "llm_elapsed_ms_by_role": dict(sorted(role_elapsed.items())),
        "tokens": totals,
        "tokens_by_role": dict(sorted(role_tokens.items())),
        "core_usage_reported_calls": sum(
            call.usage_status in {"complete", "partial"} for call in calls
        ),
        "cache_usage_reported_calls": sum(
            call.cache_read_input_tokens is not None
            or call.cache_creation_input_tokens is not None
            for call in calls
        ),
        "reasoning_usage_reported_calls": sum(
            call.reasoning_tokens is not None for call in calls
        ),
    }


def _json(value: Any) -> str:
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, default=str)


def _cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", "<br>")


def render_discover_markdown(state: DiscoverGraphState) -> str:
    frozen = state["frozen_inputs"]
    requirements = state["requirement_set"]
    requirement_review = state["requirement_review"]
    script = state["assertion_script"]
    assertion_review = state["assertion_review"]
    public = state["assertion_check_public"]
    released = state["released_assertion_results"]
    attribution = state["attribution_projection"]
    adjudication = state["adjudication"]
    coverage_gaps = state.get("coverage_gaps", ())
    # Same owner as `publish`; a divergence here means the human-readable artifact and the
    # machine-readable one disagree about whether the run was complete.
    from .nodes import coverage_status_of

    coverage_status = coverage_status_of(
        coverage_gaps, state.get("_adjudication_reconciliation", {})
    )
    adjudication_reconciliation = state.get("_adjudication_reconciliation", {})
    nodes = state.get("node_execution_records", [])
    calls = state.get("llm_call_records", [])
    summary = telemetry_summary(nodes, calls)
    zh = frozen.language == "zh-CN"
    title = "Discover 运行报告" if zh else "Discover Run Report"
    lines = [
        f"# {title}",
        "",
        (
            "本文件由确定性 Python renderer 从不可变运行记录生成，未调用 LLM。"
            if zh
            else "This file was rendered deterministically from immutable run records without an LLM."
        ),
        "",
        "## Run Identity",
        "",
        f"- `run_id`: `{frozen.run_id}`",
        f"- `profile`: `{frozen.profile}`",
        f"- `content_language`: `{frozen.language}`",
        f"- `tool_env_hash`: `{frozen.tool_env_hash}`",
        f"- `coverage_status`: `{coverage_status}`",
        # 降级必须出现在人读的第一屏。它与 coverage_status 不同：partial 是常态（逐项隔离
        # 也会 partial），而「某个阶段放弃了预算」不是常态，且它决定这一格的零结果能不能
        # 读作「没发现缺陷」。
        *(
            [
                "",
                "> ⚠️ **本格发生过降级**：下列阶段耗尽内部预算后放弃了义务并继续推进。",
                "> 该格的零结果不得读作「未发现缺陷」。",
                "",
                *(f"> - {entry}" for entry in state.get("_degraded_stages", ())),
            ]
            if state.get("_degraded_stages")
            else []
        ),
        "",
        "### Input Hashes",
        "",
        "```json",
        _json(frozen.input_hashes),
        "```",
        "",
        "## Requirements",
        "",
        "| ID | Kind | Quantifier | Statement | Coverage obligation | Source context | Rationale |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in requirements.requirements:
        lines.append(
            f"| `{item.requirement_id}` | `{item.verification_kind}` | `{item.quantifier}` | {_cell(item.statement)} | {_cell(_json(item.coverage_obligation))} | {_cell(_json(item.source_context))} | {_cell(item.rationale)} |"
        )
    lines.extend(
        [
            "",
            "### Requirement Review",
            "",
            "```json",
            _json(requirement_review),
            "```",
            "",
            "## Accepted Assertion Script",
            "",
            "```python",
            script.prefix.rstrip(),
        ]
    )
    for item in script.assertions:
        lines.append(f"assert ({item.expression}), {item.failure_message!r}")
    lines.extend(
        [
            "```",
            "",
            "### Public Check",
            "",
            "```json",
            _json(public),
            "```",
            "",
            "### Assertion Review",
            "",
            "```json",
            _json(assertion_review),
            "```",
            "",
            "## Released Results And Evidence",
            "",
            "| Assertion | Requirement | Role | Coverage key | Result | Family | Failure Message | Evidence Calls |",
            "| --- | --- | --- | --- | --- | --- | --- | ---: |",
        ]
    )
    for result in released.results:
        lines.append(
            f"| `{result.assertion_id}` | `{result.requirement_id}` | `{result.role}` | `{result.coverage_key}` | `{result.truth_value}` | `{result.evidence_family}` | {_cell(result.failure_message or '')} | {len(result.evidence_record_ids)} |"
        )
    lines.extend(
        [
            "",
            "### Full Evidence Records",
            "",
            "```json",
            _json([result.model_dump(mode="json") for result in released.results]),
            "```",
            "",
            "## Coverage Gaps",
            "",
            "```json",
            _json([gap.model_dump(mode="json") for gap in coverage_gaps]),
            "```",
            "",
            "## Attribution",
            "",
            "```json",
            _json(attribution),
            "```",
            "",
            "## Adjudication",
            "",
            "```json",
            _json(adjudication),
            "```",
            "",
            "### Deterministic Adjudication Reconciliation",
            "",
            "```json",
            _json(adjudication_reconciliation),
            "```",
            "",
            "## Telemetry",
            "",
            "```json",
            _json(summary),
            "```",
            "",
            "### LLM Calls",
            "",
            "| Role | Revision | Profile | Model | Input | Output | Total | Cache Read | Elapsed ms | Attempts |",
            "| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for call in calls:
        values = [
            call.role,
            str(call.revision),
            call.profile,
            call.observed_model or call.configured_model or "unavailable",
            str(call.input_tokens) if call.input_tokens is not None else "null",
            str(call.output_tokens) if call.output_tokens is not None else "null",
            str(call.total_tokens) if call.total_tokens is not None else "null",
            str(call.cache_read_input_tokens)
            if call.cache_read_input_tokens is not None
            else "null",
            f"{call.elapsed_ms:.1f}",
            str(len(call.transport_attempts)),
        ]
        lines.append("| " + " | ".join(values) + " |")
    lines.append("")
    return "\n".join(lines)


def write_discover_markdown(state: DiscoverGraphState, path: str | Path) -> Path:
    target = Path(path).expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8") as stream:
        stream.write(render_discover_markdown(state))
    return target


__all__ = ["render_discover_markdown", "telemetry_summary", "write_discover_markdown"]
