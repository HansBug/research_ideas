from __future__ import annotations

import ast
import math
import operator
import re
from datetime import datetime, timedelta
from pathlib import Path
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
@click.option("--audit-out", type=click.Path(path_type=Path), default=Path("runs/utils-agent/demo-audit.jsonl"), show_default=True)
@click.option("--result-out", type=click.Path(path_type=Path), default=Path("runs/utils-agent/demo-result.json"), show_default=True)
def cli(config: Path | None, profile: str, renderer: str, log_level: str, audit_out: Path, result_out: Path) -> None:
    """真实调用所选 profile 的最小工具型 Agent 演示（默认 gpt-5.5）。"""

    registry = load_llm_registry(config)
    selected = registry.require(profile)

    from langchain_core.tools import tool

    @tool
    def calculate_expression(expression: str) -> dict[str, float | str]:
        """安全计算数字数学表达式。"""

        return _calculate_expression(expression)

    @tool
    def current_system_time() -> dict[str, str]:
        """读取当前机器系统时间。"""

        return _current_system_time()

    spec = AgentSpec(
        name="utils-demo",
        system_prompt=(
            "请计算当前系统时间 (2 * 24) + 3 + (15 / 60) 小时后的美国东部时间。"
        ),
        tools=(current_system_time, calculate_expression),
        output_schema=DemoAnswer,
        require_tool_call=True,
    )
    app = AgentApp.from_config(spec, selected, model_options={"streaming": True, "stream_usage": True, "max_retries": 0})
    result = app.run(
        "请完成上述时间计算并给出结构化答案。",
        renderer=renderer,
        log_level=log_level,
        audit_out=audit_out,
        result_out=result_out,
    )
    if result.status != "success":
        raise click.ClickException((result.error or {}).get("message", "agent failed"))
    answer = result.require_output()
    names = {item.get("name") for item in result.tool_calls if item.get("status") == "completed"}
    try:
        base_time = _last_timestamp(answer.base_time)
        target_time = _last_timestamp(answer.target_time)
        valid_offset = abs((target_time - base_time - timedelta(hours=51.25)).total_seconds()) <= 1
    except (TypeError, ValueError):
        valid_offset = False
    if (
        not {"current_system_time", "calculate_expression"}.issubset(names)
        or not result.real_llm
        or result.model != selected.model
        or (result.observed_model is not None and result.observed_model != selected.model)
        or not math.isclose(answer.offset_hours, 51.25, rel_tol=0, abs_tol=1e-9)
        or set(answer.evidence_ids) != {"system-time-001", "math-expression-001"}
        or not valid_offset
    ):
        raise click.ClickException("demo tool/model validation failed")


def main(argv: list[str] | None = None) -> int:
    try:
        cli.main(args=argv, prog_name="python -m utils.agent", standalone_mode=False)
    except (click.ClickException, AgentError, ValueError) as exc:
        click.echo(str(exc), err=True)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
