from __future__ import annotations

import ast
import json
import math
import operator
import re
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

import click
from pydantic import BaseModel

from utils.agent import AgentApp, AgentError, AgentSpec
from utils.llm import load_llm_registry


class DemoAnswer(BaseModel):
    summary: str
    base_time: str
    offset_hours: float
    target_time: str
    evidence_ids: list[str]


_ISO_TIMESTAMP = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})"
)


def _last_timestamp(value: str) -> datetime:
    """Extract the final timezone-aware ISO timestamp from visible model text."""

    matches = _ISO_TIMESTAMP.findall(value)
    if not matches:
        raise ValueError("timestamp not found")
    parsed = datetime.fromisoformat(matches[-1].replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return parsed


_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _evaluate(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_evaluate(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        left, right = _evaluate(node.left), _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 8:
            raise ValueError("exponent too large")
        return _OPERATORS[type(node.op)](left, right)
    raise ValueError("only numeric arithmetic is allowed")


def _calculate_expression(expression: str) -> dict[str, float | str]:
    """安全计算一个只含数字和 + - * / ** 的 Python 数学表达式。"""

    tree = ast.parse(expression, mode="eval")
    value = _evaluate(tree)
    return {"expression": expression, "value": value, "evidence_id": "math-expression-001"}


def _current_system_time() -> dict[str, str]:
    """读取当前机器系统时间和时区。"""

    now = datetime.now().astimezone()
    eastern = now.astimezone(ZoneInfo("America/New_York"))
    return {
        "iso_time": now.isoformat(),
        "timezone": str(now.tzinfo),
        "us_eastern_iso_time": eastern.isoformat(),
        "evidence_id": "system-time-001",
    }


@click.command("python -m utils.agent")
@click.option("--config", type=click.Path(path_type=Path), default=None)
@click.option("--profile", default="gpt-5.5", show_default=True)
@click.option("--renderer", type=click.Choice(("auto", "rich", "jsonl", "quiet")), default="rich", show_default=True)
@click.option("--log-level", type=click.Choice(("DEBUG", "INFO", "WARNING", "ERROR")), default="INFO", show_default=True)
@click.option("--enable-think", is_flag=True, default=False, help="显式开启模型思考模式；默认关闭。")
@click.option("--reasoning-effort", type=click.Choice(("low", "medium", "high", "xhigh", "max")), default=None, help="单次推理 effort；不传则使用 provider 默认值。")
@click.option("--max-model-calls", type=click.IntRange(min=1), default=None, help="显式限制模型调用次数；默认不限制。")
@click.option("--max-tool-calls", type=click.IntRange(min=1), default=None, help="显式限制业务工具调用次数；默认不限制。")
@click.option("--max-turns", type=click.IntRange(min=1), default=None, help="显式限制模型轮数；默认不限制。")
@click.option("--max-seconds", type=click.FloatRange(min=0, min_open=True), default=None, help="显式限制整个运行的秒数；默认不限制。")
@click.option("--audit-out", type=click.Path(path_type=Path), default=Path("runs/utils-agent/demo-audit.jsonl"), show_default=True)
@click.option("--result-out", type=click.Path(path_type=Path), default=Path("runs/utils-agent/demo-result.json"), show_default=True)
def cli(
    config: Path | None,
    profile: str,
    renderer: str,
    log_level: str,
    enable_think: bool,
    reasoning_effort: str | None,
    max_model_calls: int | None,
    max_tool_calls: int | None,
    max_turns: int | None,
    max_seconds: float | None,
    audit_out: Path,
    result_out: Path,
) -> None:
    """真实调用所选 profile 的最小工具型 Agent 演示（默认 gpt-5.5）。"""

    registry = load_llm_registry(config)
    selected = registry.require(profile)

    from langchain_core.tools import tool

    @tool
    def calculate_expression(expression: str) -> dict[str, float | str]:
        """Evaluate a numeric arithmetic expression for the time offset.

        Purpose: obtain a reproducible numeric value for the requested offset.
        Input: expression containing only numbers and +, -, *, /, or **.
        Output: the original expression, its numeric value, and an evidence ID.
        Constraint: no names, attributes, function calls, or other Python syntax.
        """

        return _calculate_expression(expression)

    @tool
    def current_system_time() -> dict[str, str]:
        """Read the current system time and convert it to US Eastern time.

        Purpose: provide the time anchor for the calculation.
        Input: none.
        Output: local ISO time, timezone, US Eastern ISO time, and an evidence ID.
        """

        return _current_system_time()

    limits = {
        key: value
        for key, value in {
            "model_calls": max_model_calls,
            "tool_calls": max_tool_calls,
            "turns": max_turns,
            "seconds": max_seconds,
        }.items()
        if value is not None
    }
    spec = AgentSpec(
        name="utils-demo",
        system_prompt=(
            "You are a careful tool-using research agent. "
            "Available tools are current_system_time, which returns the local and US Eastern ISO timestamps with an evidence ID, "
            "and calculate_expression, which evaluates a numeric arithmetic expression and returns its value with an evidence ID. "
            "Use the available tools when evidence or calculation is needed, then return valid JSON with exactly the fields "
            "summary, base_time, offset_hours, target_time, and evidence_ids; summary must include the visible calculation steps "
            "and conclusion, and evidence_ids must cite the tool evidence."
        ),
        tools=(current_system_time, calculate_expression),
        output_schema=None if _is_deepseek_profile(selected) else DemoAnswer,
        limits=limits or None,
        require_tool_call=True,
    )
    app = AgentApp.from_config(spec, selected, model_options={"streaming": True, "stream_usage": True, "max_retries": 0})
    result = app.run(
        "请计算当前系统时间 (2 * 24) + 3 + (15 / 60) 小时后的美国东部时间。",
        renderer=renderer,
        log_level=log_level,
        think_mode=enable_think,
        reasoning_effort=reasoning_effort,
        audit_out=audit_out,
        result_out=result_out,
    )
    if result.status != "success":
        error = result.error or {"code": "agent_failed", "message": "agent failed"}
        detail = json.dumps(error.get("details"), ensure_ascii=False, sort_keys=True) if error.get("details") else "none"
        raise click.ClickException(f"{error.get('message', 'agent failed')}\ncode={error.get('code')}\ndetails={detail}")
    names = {item.get("name") for item in result.tool_calls if item.get("status") == "completed"}
    if (
        not {"current_system_time", "calculate_expression"}.issubset(names)
        or not result.real_llm
        or result.model != selected.model
        or (result.observed_model is not None and result.observed_model != selected.model)
        or (_is_deepseek_profile(selected) and not result.final_text.strip())
    ):
        raise click.ClickException("demo tool/model validation failed")
    if not _is_deepseek_profile(selected):
        answer = result.require_output()
        try:
            base_time = _last_timestamp(answer.base_time)
            target_time = _last_timestamp(answer.target_time)
            valid_offset = abs((target_time - base_time - timedelta(hours=51.25)).total_seconds()) <= 1
        except (TypeError, ValueError):
            valid_offset = False
        if (
            not math.isclose(answer.offset_hours, 51.25, rel_tol=0, abs_tol=1e-9)
            or set(answer.evidence_ids) != {"system-time-001", "math-expression-001"}
            or not valid_offset
        ):
            raise click.ClickException("demo structured output validation failed")


def _is_deepseek_profile(config: object) -> bool:
    model = str(getattr(config, "model", "")).lower()
    base_url = str(getattr(config, "base_url", "") or "")
    host = (urlsplit(base_url).hostname or "").lower()
    return model.startswith("deepseek-") or host.endswith("deepseek.com")


def main(argv: list[str] | None = None) -> int:
    try:
        cli.main(args=argv, prog_name="python -m utils.agent", standalone_mode=False)
    except (click.ClickException, AgentError, ValueError) as exc:
        click.echo(str(exc), err=True)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
