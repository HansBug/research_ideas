"""一个代次的耗时与 token 汇总：逐环节、逐臂、逐 pair，以及总计。

## 为什么需要它

每格的 `discover-completed.json` 已经带了完整的 `telemetry_summary`（14 个字段，含逐节点耗时、
逐 LLM 角色耗时、逐角色 token 与 token 总计）。缺的不是采集，是**汇总** —— 没有任何东西把一个
代次的格加起来，于是「这一代次花了多少、慢在哪一环」每次都靠临时脚本重算，而临时脚本的口径
每次都可能不同。

## 两种时间不可混用

- `node_elapsed_ms_sum` 是**串行累加**。某格实测 800 秒，但那是各节点耗时相加，不是该格的墙钟。
- **墙钟**只能来自启动器记录的起止时间（`WALLCLOCK.txt`），因为格是并发跑的：48 格串行累加约
  8.25 小时，`MAX=8` 下实际墙钟 1.61 小时。

报成本用累加值（它与 token 同源、可复算），报「跑完要多久」必须用墙钟。本模块两个都给，并且
在输出里把它们分开标注 —— 混用会让「预计 9 到 11 小时」这类结论差出 5 倍。

用法：

    python -m matrix_cost --generation matrix-v36
    python -m matrix_cost --base runs/paper1/matrix-v36 --json
"""

from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
# ⛔ 归档后深度多了两层，原先的 parents[N] 解析到 `paper_stm_issue_discover/`。
# ⭐ 改为按仓库根标志物向上锚定（CLAUDE.md §9.5-3）。
REPO = next(_p for _p in Path(__file__).resolve().parents if (_p / "CLAUDE.md").is_file() and (_p / ".git").exists())
RUNS = REPO / "runs" / "paper1"

_CELL = re.compile(r"^(\d{4})-(claude|gpt)$")
#: `tokens` 里的字段。`None` 表示 provider 没报，与 0 不同 —— 前者是缺测，后者是真的没用。
_TOKEN_FIELDS = (
    "input_tokens",
    "output_tokens",
    "total_tokens",
    "cache_read_input_tokens",
    "cache_creation_input_tokens",
    "reasoning_tokens",
)


def _cells(base: Path) -> list[tuple[str, str, str, dict[str, Any]]]:
    """(round, pair, arm, telemetry) —— 只收落盘完成的格。"""

    out = []
    for completed in sorted(base.glob("run*/*/discover-completed.json")):
        match = _CELL.match(completed.parent.name)
        if not match:
            continue
        try:
            payload = json.loads(completed.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        out.append(
            (
                completed.parent.parent.name,
                match.group(1),
                match.group(2),
                payload.get("telemetry_summary") or {},
            )
        )
    return out


def _wallclock(base: Path) -> dict[str, Any]:
    """启动器写下的墙钟。缺失时明确说缺，不用累加值冒充。

    ⚠️ **必须处理续跑。** `one()` 在每次尝试开头检查 `discover-completed.json` 就返回，所以对同一个
    BASE 重跑启动器会跳过已落盘的格 —— 324 格中断后直接续跑是**预期用法**。那样 `WALLCLOCK.txt`
    里会有多段，而逐行读取时后者覆盖前者，读到的是**最后一段**的起止：一次「跑了 9 小时、中断、
    再跑 20 分钟补完」会被报成 20 分钟。

    所以分段耗时要相加，并把段数打出来 —— 读者据此知道这个数字是一次跑完还是拼起来的。
    """

    path = base / "WALLCLOCK.txt"
    if not path.is_file():
        return {"available": False, "note": "无 WALLCLOCK.txt —— 该代次的墙钟无法复原，不得用累加值代替"}
    fields: dict[str, str] = {}
    segment_seconds: list[int] = []
    for line in path.read_text().splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        fields[key] = value
        if re.fullmatch(r"segment_\d+_elapsed_seconds", key):
            try:
                segment_seconds.append(int(value))
            except ValueError:
                pass
    out: dict[str, Any] = {"available": True, **fields}
    if segment_seconds:
        total = sum(segment_seconds)
        out["segments"] = len(segment_seconds)
        out["elapsed_seconds"] = total
        out["elapsed"] = f"{total // 3600}h{total % 3600 // 60:02d}m{total % 60:02d}s"
        if len(segment_seconds) > 1:
            out["segments_note"] = (
                f"续跑 {len(segment_seconds)} 段，耗时为各段之和"
                f"（{'+'.join(str(s) for s in segment_seconds)} 秒）；不是一次跑完"
            )
    return out


def summarise(base: Path) -> dict[str, Any]:
    cells = _cells(base)
    node_ms: dict[str, float] = collections.defaultdict(float)
    role_ms: dict[str, float] = collections.defaultdict(float)
    role_tokens: dict[str, dict[str, int]] = collections.defaultdict(
        lambda: collections.defaultdict(int)
    )
    tokens: dict[str, int] = collections.defaultdict(int)
    #: 缺测计数：某字段有多少格没报。分母不写清楚，`cache_creation` 全 None 会被读成「缓存没生效」。
    #:
    #: **每个字段都预置 0**，不是 defaultdict 按需建键。否则「表里没有 `input_tokens` 这一行」与
    #: 「它 0 缺测」在输出里长得一样，读者无从分辨「统计过且都报了」和「压根没统计这个字段」——
    #: 与仓库纪律「任何 0/从不/全部 的结果先打分母」同一条。
    missing: dict[str, int] = {field: 0 for field in _TOKEN_FIELDS}
    by_arm: dict[str, dict[str, float]] = collections.defaultdict(
        lambda: collections.defaultdict(float)
    )
    by_pair: dict[str, dict[str, float]] = collections.defaultdict(
        lambda: collections.defaultdict(float)
    )
    calls = attempts = retries = 0
    for _round, pair, arm, telemetry in cells:
        calls += telemetry.get("llm_call_count") or 0
        attempts += telemetry.get("transport_attempt_count") or 0
        retries += telemetry.get("retry_count") or 0
        for name, value in (telemetry.get("node_elapsed_ms_by_name") or {}).items():
            node_ms[name] += float(value or 0)
        for role, value in (telemetry.get("llm_elapsed_ms_by_role") or {}).items():
            role_ms[role] += float(value or 0)
        for role, counts in (telemetry.get("tokens_by_role") or {}).items():
            for key, value in (counts or {}).items():
                role_tokens[role][key] += int(value or 0)
        cell_tokens = telemetry.get("tokens") or {}
        for field in _TOKEN_FIELDS:
            value = cell_tokens.get(field)
            if value is None:
                missing[field] += 1
            else:
                tokens[field] += int(value)
        elapsed = float(telemetry.get("node_elapsed_ms_sum") or 0)
        by_arm[arm]["cells"] += 1
        by_arm[arm]["node_ms"] += elapsed
        by_arm[arm]["total_tokens"] += int(cell_tokens.get("total_tokens") or 0)
        by_arm[arm]["llm_calls"] += telemetry.get("llm_call_count") or 0
        by_pair[pair]["cells"] += 1
        by_pair[pair]["node_ms"] += elapsed
        by_pair[pair]["total_tokens"] += int(cell_tokens.get("total_tokens") or 0)
    return {
        "base": str(base),
        "cells_completed": len(cells),
        "llm_calls": calls,
        "transport_attempts": attempts,
        "transport_retries": retries,
        "node_ms_serial_sum": sum(node_ms.values()),
        "node_ms_by_stage": dict(sorted(node_ms.items(), key=lambda kv: -kv[1])),
        "llm_ms_by_role": dict(sorted(role_ms.items(), key=lambda kv: -kv[1])),
        "tokens": dict(tokens),
        "tokens_missing_in_cells": missing,
        "tokens_by_role": {r: dict(v) for r, v in sorted(role_tokens.items())},
        "by_arm": {a: dict(v) for a, v in sorted(by_arm.items())},
        "by_pair": {p: dict(v) for p, v in sorted(by_pair.items())},
        "wallclock": _wallclock(base),
    }


def _hms(ms: float) -> str:
    seconds = int(ms / 1000)
    return f"{seconds // 3600}h{seconds % 3600 // 60:02d}m{seconds % 60:02d}s"


def render(summary: dict[str, Any]) -> str:
    lines = [
        f"# 代次成本汇总 — {Path(summary['base']).name}",
        "",
        f"完成格数 **{summary['cells_completed']}** ｜ LLM 调用 **{summary['llm_calls']}** ｜ "
        f"传输尝试 {summary['transport_attempts']} ｜ 传输重试 {summary['transport_retries']}",
        "",
    ]
    wall = summary["wallclock"]
    if wall.get("available"):
        lines += [
            f"**墙钟**：{wall.get('started_at','?')} → {wall.get('finished_at','?')}"
            f"（{wall.get('elapsed','?')}，并发 MAX={wall.get('max_concurrency','?')}）",
            "",
        ]
        if wall.get("segments_note"):
            lines += [f"⚠️ {wall['segments_note']}", ""]
    else:
        lines += [f"⚠️ 墙钟不可用：{wall.get('note')}", ""]
    lines += [
        f"**串行累加耗时** {_hms(summary['node_ms_serial_sum'])} —— 这是各节点耗时相加，"
        "不是墙钟；格是并发跑的，两者不可混用。",
        "",
        "## 逐环节耗时（串行累加）",
        "",
        "| 环节 | 耗时 | 占比 |",
        "|:--|--:|--:|",
    ]
    total = summary["node_ms_serial_sum"] or 1
    for name, value in summary["node_ms_by_stage"].items():
        lines.append(f"| `{name}` | {_hms(value)} | {value / total * 100:.1f}% |")
    lines += ["", "## Token", "", "| 字段 | 合计 | 缺测格数 |", "|:--|--:|--:|"]
    for field in _TOKEN_FIELDS:
        got = summary["tokens"].get(field)
        miss = summary["tokens_missing_in_cells"].get(field, 0)
        lines.append(
            f"| `{field}` | {got:,} |".replace(",", " ") + f" {miss} |"
            if got is not None
            else f"| `{field}` | — | {miss} |"
        )
    lines += ["", "## 逐 LLM 角色", "", "| 角色 | 耗时 | input | output | total |", "|:--|--:|--:|--:|--:|"]
    for role, ms in summary["llm_ms_by_role"].items():
        tok = summary["tokens_by_role"].get(role, {})
        lines.append(
            f"| `{role}` | {_hms(ms)} | {tok.get('input', 0)} | {tok.get('output', 0)} | "
            f"{tok.get('total', 0)} |"
        )
    lines += ["", "## 逐臂", "", "| 臂 | 格数 | 串行耗时 | LLM 调用 | total tokens |", "|:--|--:|--:|--:|--:|"]
    for arm, row in summary["by_arm"].items():
        lines.append(
            f"| {arm} | {int(row['cells'])} | {_hms(row['node_ms'])} | "
            f"{int(row['llm_calls'])} | {int(row['total_tokens'])} |"
        )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", help="运行目录，例如 runs/paper1/matrix-v36")
    parser.add_argument("--generation", help="代次名，例如 matrix-v36")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.base:
        base = Path(args.base)
        if not base.is_absolute():
            base = REPO / base
    elif args.generation:
        base = RUNS / args.generation
    else:
        candidates = sorted(
            (d for d in RUNS.glob("matrix-*") if d.is_dir()),
            key=lambda d: d.stat().st_mtime,
            reverse=True,
        )
        if not candidates:
            raise SystemExit(f"没有可用的运行目录：{RUNS}")
        base = candidates[0]
    if not base.is_dir():
        raise SystemExit(f"运行目录不存在：{base}")
    summary = summarise(base)
    if not summary["cells_completed"]:
        raise SystemExit(f"{base} 下没有落盘完成的格 —— 拒绝输出一份看起来正常的空汇总")
    print(json.dumps(summary, ensure_ascii=False, indent=1) if args.json else render(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
