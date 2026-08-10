"""把一代次的 token 消耗与耗时导出成可审计的逐格 / 逐环节表。

## 为什么要落库

代次之间比命中率时，绕不开「这一代是不是靠多花算力换来的」。没有 token 与耗时数据，
这个问题只能靠猜；有了它，命中率的提升可以除以成本，变成「每百万 output token 命中多少位」
这类可比的量。v46 相对 v37 的需求数多 58%、issue 多 95%，成本侧必须同时报出来，否则
读者无从判断提升是效率提升还是投入提升。

数据全部取自各格 `discover-completed.json` 的 `telemetry_summary`，那是流水线自己写的
运行记录，不是事后估算。**本脚本不做任何推断，只做汇总与除法。**

⚠️ 三个口径要分清，混起来会得出相反结论：

- `input_tokens` 含 prompt 与全部回灌的反馈，会随修订轮数放大；
- `output_tokens` 才是模型实际生成量，跨代比较应以它为准；
- `cache_read_input_tokens` 在本仓库的 provider 配置下常为 0，不代表没有缓存，
  只代表 provider 没报。**为 0 的字段不得写成「无缓存」。**

用法::

    run_telemetry.py --generation matrix-v46-full --out /tmp/v46_telemetry.json
    run_telemetry.py --generation matrix-v46-full --compare matrix-v37
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import statistics
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
RUNS = REPO / "runs" / "paper1"


def collect(generation: str) -> dict:
    """逐格遥测。`.tryN` 目录排除——它们是被放弃的尝试，算进来会虚增成本。"""

    root = RUNS / generation
    cells: list[dict] = []
    for receipt in sorted(root.glob("run*/*/discover-completed.json")):
        if ".try" in str(receipt):
            continue
        payload = json.loads(receipt.read_text())
        telemetry = payload.get("telemetry_summary") or {}
        tokens = telemetry.get("tokens") or {}
        cells.append(
            {
                "cell": f"{receipt.parent.parent.name}/{receipt.parent.name}",
                "run": receipt.parent.parent.name,
                "pair": receipt.parent.name.split("-")[0],
                "arm": receipt.parent.name.split("-", 1)[1],
                "input_tokens": tokens.get("input_tokens") or 0,
                "output_tokens": tokens.get("output_tokens") or 0,
                "total_tokens": tokens.get("total_tokens") or 0,
                "cache_read_input_tokens": tokens.get("cache_read_input_tokens") or 0,
                "reasoning_tokens": tokens.get("reasoning_tokens"),
                "llm_call_count": telemetry.get("llm_call_count") or 0,
                "node_count": telemetry.get("node_count") or 0,
                "retry_count": telemetry.get("retry_count") or 0,
                "transport_attempt_count": telemetry.get("transport_attempt_count") or 0,
                "llm_elapsed_ms": telemetry.get("llm_elapsed_ms_sum") or 0,
                "node_elapsed_ms": telemetry.get("node_elapsed_ms_sum") or 0,
                "tokens_by_role": telemetry.get("tokens_by_role") or {},
                "llm_elapsed_ms_by_role": telemetry.get("llm_elapsed_ms_by_role") or {},
                "node_elapsed_ms_by_name": telemetry.get("node_elapsed_ms_by_name") or {},
                "issues": len(payload.get("issues") or []),
                "degraded": bool(payload.get("degraded_stages")),
            }
        )
    return {"generation": generation, "cells": cells}


def _sum_by(cells: list[dict], key: str, field: str) -> dict[str, int]:
    out: collections.Counter = collections.Counter()
    for cell in cells:
        for name, value in (cell.get(key) or {}).items():
            if isinstance(value, dict):
                out[name] += value.get(field) or 0
            else:
                out[name] += value or 0
    return dict(out)


def summarise(data: dict) -> dict:
    cells = data["cells"]
    if not cells:
        return {"generation": data["generation"], "cells": 0}
    out_tokens = [c["output_tokens"] for c in cells]
    in_tokens = [c["input_tokens"] for c in cells]
    node_ms = [c["node_elapsed_ms"] for c in cells]
    return {
        "generation": data["generation"],
        "cells": len(cells),
        "input_tokens_total": sum(in_tokens),
        "output_tokens_total": sum(out_tokens),
        "total_tokens_total": sum(c["total_tokens"] for c in cells),
        "llm_calls_total": sum(c["llm_call_count"] for c in cells),
        "node_elapsed_ms_total": sum(node_ms),
        "llm_elapsed_ms_total": sum(c["llm_elapsed_ms"] for c in cells),
        "output_tokens_per_cell": {
            "median": statistics.median(out_tokens),
            "mean": round(statistics.mean(out_tokens), 1),
            "max": max(out_tokens),
            "min": min(out_tokens),
        },
        "node_elapsed_s_per_cell": {
            "median": round(statistics.median(node_ms) / 1000, 1),
            "mean": round(statistics.mean(node_ms) / 1000, 1),
            "max": round(max(node_ms) / 1000, 1),
        },
        # 逐环节：token 按角色（LLM 调用者），耗时按节点名（图节点）。两者维度不同，
        # 不可相加 —— 角色是「谁在生成」，节点是「图跑到哪一步」。
        # ⚠️ `tokens_by_role` 的子键是 `input`/`output`/`total`，**不是** `input_tokens`。
        # 顶层 `tokens` 用的才是带 `_tokens` 后缀的名字。两处命名不一致，按错的键取会
        # 静默得到全 0 —— 而「全 0」和「该角色没消耗」在表里长得一样。
        "output_tokens_by_role": _sum_by(cells, "tokens_by_role", "output"),
        "input_tokens_by_role": _sum_by(cells, "tokens_by_role", "input"),
        "llm_elapsed_ms_by_role": _sum_by(cells, "llm_elapsed_ms_by_role", ""),
        "node_elapsed_ms_by_name": _sum_by(cells, "node_elapsed_ms_by_name", ""),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--generation", required=True)
    parser.add_argument("--out", type=pathlib.Path)
    parser.add_argument("--compare", help="另一代次，用于并列成本对比")
    args = parser.parse_args(argv)

    data = collect(args.generation)
    summary = summarise(data)
    if args.out:
        args.out.write_text(
            json.dumps({"summary": summary, "cells": data["cells"]}, ensure_ascii=False, indent=1)
        )
        print(f"逐格 {summary['cells']} 行 → {args.out}")

    def show(s: dict) -> None:
        print(f"\n### {s['generation']}  {s['cells']} 格")
        print(f"  output token 合计 {s['output_tokens_total']:,} ｜ input {s['input_tokens_total']:,} "
              f"｜ 合计 {s['total_tokens_total']:,}")
        print(f"  LLM 调用 {s['llm_calls_total']:,} 次 ｜ 节点耗时合计 "
              f"{s['node_elapsed_ms_total']/3600000:.1f} 机时")
        o = s["output_tokens_per_cell"]
        print(f"  每格 output token: 中位 {o['median']:,} 均值 {o['mean']:,} 最大 {o['max']:,}")
        e = s["node_elapsed_s_per_cell"]
        print(f"  每格墙钟: 中位 {e['median']}s 均值 {e['mean']}s 最大 {e['max']}s")
        print("  逐角色 output token:")
        for k, v in sorted(s["output_tokens_by_role"].items(), key=lambda kv: -kv[1]):
            print(f"     {k:22} {v:>10,}  ({v / s['output_tokens_total']:.1%})")
        print("  逐节点耗时:")
        for k, v in sorted(s["node_elapsed_ms_by_name"].items(), key=lambda kv: -kv[1])[:8]:
            print(f"     {k:22} {v/3600000:>7.2f} 机时  ({v / s['node_elapsed_ms_total']:.1%})")

    show(summary)
    if args.compare:
        other = summarise(collect(args.compare))
        show(other)
        if other["output_tokens_total"]:
            r = summary["output_tokens_total"] / other["output_tokens_total"]
            print(f"\n  output token 比值 {summary['generation']} / {other['generation']} = {r:.2f}×")
    return 0


if __name__ == "__main__":
    sys.exit(main())
