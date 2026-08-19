"""编排 324 格：54 pair × 2 profile × 3 轮，⭐ 幂等、可中断续跑。

## ⚠️ 为什么不复用主臂的 `launch_cells_serial.sh`

那个脚本有两个会静默出错的坑，⛔ 照抄会踩：

1. `REPO=/home/zhangshaoang/oo-projects/research_ideas` 是**硬编码的另一个 clone**；本工作树是
   `research_ideas-3`。
2. `set -a; source "$REPO/.env"; set +a` —— 仓库根 `CLAUDE.md` §5.1 已明确：**本仓库没有
   `.env`**，配置真源是 `.llmconfig.yml`，凭据由 `--profile` 决议。那一行是已归档旧 agent loop
   的遗留，⛔ 且它曾把「`.env` 不存在」误判成鉴权失败、杀掉 4 个正常运行的格。

所以本脚本：路径全用 `Path(__file__)` 相对解析、⛔ 不碰任何环境变量凭据、只传 `--profile`。

## ⚠️ 开跑前必须确认没有残留工作进程（`CLAUDE.md` §3.5.1）

停止一次编排必须杀两层：杀编排进程**不杀**它已经派出的工作进程，而那些进程不随父进程退出而
终止。若此时重启并写入同一输出目录，就会有两个写者各自维护计数器与文件句柄，产出**静默污染**的
记录。本脚本 `--check-stale` 在开跑前主动查一次，⛔ 发现残留就拒绝启动。

⭐ 本编排在**同进程**内用线程池跑（LLM 调用是 IO bound），所以「残留工作进程」只可能来自上一次
的 `launch.py` 或手工 `runner.py`——两者都在下面的特征里。

## 幂等

已存在且 `status == "ok"` 的格直接跳过。⭐ 这使中断续跑是安全的，也使「补跑失败格」不需要另写
脚本。⛔ 但**不重跑已 ok 的格**：重跑等于重新采样，会悄悄改变分布。
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from runner import REPORT_ROOT, run_cell, write_record  # noqa: E402

#: 两条臂：profile → 短名。⭐ 与主臂 v46 完全相同的两个模型（§4B.2「⛔ 不许降级」）。
ARMS: tuple[tuple[str, str], ...] = (("gpt-5.5", "gpt"), ("claude-opus-4-7", "claude"))

ROUNDS = (1, 2, 3)


def parse_arms(raw: str | None) -> tuple[tuple[str, str], ...]:
    """解析可选的 profile:label 覆盖，默认保持历史 X1v2 两臂。"""

    if raw is None:
        return ARMS
    parsed: list[tuple[str, str]] = []
    for item in raw.split(","):
        profile, separator, label = item.partition(":")
        if not separator or not profile.strip() or not label.strip():
            raise SystemExit(
                f"invalid --profiles entry {item!r}; expected profile:label"
            )
        parsed.append((profile.strip(), label.strip()))
    if not parsed:
        raise SystemExit("--profiles must contain at least one profile:label entry")
    return tuple(parsed)

#: ⛔ 永久排除的 `00x8` 家族（`docs/protocol/nl_scope_rule.md`）：那份 NL 要求 fork/join 与秒级
#: 时间约束，其忠实模型在 M = (S,E,V,Tr,A) 里无法表示。⭐ 判据只读 `nl.txt`、与运行结果无关。
OUT_OF_SCOPE_SUFFIX = "8"

_print_lock = threading.Lock()


def in_scope_cases(report_root: Path | None = None) -> list[str]:
    root = (report_root or REPORT_ROOT).expanduser().resolve()
    cases = sorted(p.name for p in (root / "pairs").iterdir() if p.is_dir())
    kept = [c for c in cases if not c.endswith(OUT_OF_SCOPE_SUFFIX)]
    if len(kept) != 54:
        raise SystemExit(
            f"expected 54 in-scope pairs, found {len(kept)} (of {len(cases)} total). "
            "The grid is fixed at 54 by nl_scope_rule.md -- investigate before running."
        )
    return kept


def own_process_chain() -> set[str]:
    """自己 + 全部进程祖先的 pid。

    ⚠️ **初版只排除 `os.getpid()`，于是这道检查把自己拒了。** 包裹本进程的 shell
    （`bash -c '... launch.py ...'`）、`nohup`、`timeout` 都会在自己之上留下**含相同命令行**的
    祖先进程，它们逐个都会命中特征串。⛔ 排除集必须是整条祖先链，⛔ 不是单个 pid。

    ⭐ 这个 bug 的形态值得记：一道安全检查把**保护对象本身**当成了威胁。
    """

    chain: set[str] = set()
    pid = os.getpid()
    while pid > 0 and str(pid) not in chain:
        chain.add(str(pid))
        try:
            stat = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8")
        except OSError:
            break
        # comm 字段可能含空格与括号，取最后一个 ')' 之后再切。
        tail = stat[stat.rfind(")") + 1 :].split()
        if len(tail) < 2:
            break
        try:
            pid = int(tail[1])
        except ValueError:
            break
    return chain


def find_stale_workers() -> list[str]:
    """上一次编排留下的工作进程。⛔ 有残留就不许开跑。"""

    needles = ("baseline_arm/src/runner.py", "baseline_arm/src/launch.py")
    try:
        out = subprocess.run(
            ["ps", "-eo", "pid,lstart,args"], capture_output=True, text=True, timeout=30
        ).stdout
    except Exception:  # pragma: no cover - defensive
        return []
    mine = own_process_chain()
    hits: list[str] = []
    for line in out.splitlines():
        if not any(n in line for n in needles):
            continue
        if line.split(maxsplit=1)[0] in mine:
            continue
        hits.append(line.strip())
    return hits


def cell_dir(out_root: Path, round_index: int, case: str, arm_label: str) -> Path:
    return out_root / f"run{round_index}" / f"{case}-{arm_label}"


def already_done(path: Path) -> bool:
    record = path / "record.json"
    if not record.is_file():
        return False
    try:
        return json.loads(record.read_text(encoding="utf-8")).get("status") == "ok"
    except Exception:  # pragma: no cover - a corrupt record must be re-run
        return False


def _log(message: str) -> None:
    with _print_lock:
        stamp = datetime.now(timezone.utc).strftime("%H:%M:%S")
        print(f"[{stamp}] {message}", flush=True)


def _one(
    *,
    case: str,
    profile: str,
    arm_label: str,
    round_index: int,
    out_root: Path,
    content_language: str,
    registry_path: str | None,
    transport_retries: int,
    streaming: bool | None,
) -> dict[str, Any]:
    target = cell_dir(out_root, round_index, case, arm_label)
    if already_done(target):
        _log(f"skip  run{round_index}/{case}-{arm_label} (already ok)")
        return json.loads((target / "record.json").read_text(encoding="utf-8"))
    started = time.perf_counter()
    try:
        record = run_cell(
            case=case,
            profile=profile,
            content_language=content_language,
            registry_path=registry_path,
            transport_retries=transport_retries,
            streaming=streaming,
            round_index=round_index,
            arm_label=arm_label,
        )
    except Exception as exc:  # noqa: BLE001
        # ⛔ 编排层也不许让一格把整批带崩（`CLAUDE.md` §10）。落一份 failed record。
        record = {
            "schema_version": "x1-baseline-arm/1",
            "arm": "naive_baseline",
            "case": case,
            "round": round_index,
            "arm_label": arm_label,
            "profile": profile,
            "status": "failed",
            "failure": f"orchestrator-level error: {type(exc).__name__}: {exc}",
            "failure_class": "orchestrator_error",
            "parsed_output": None,
            "issue_count": None,
        }
    write_record(record, target)
    elapsed = time.perf_counter() - started
    _log(
        f"{record['status']:>6} run{round_index}/{case}-{arm_label} "
        f"issues={record.get('issue_count')} {elapsed:.1f}s"
    )
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the 324-cell naive-baseline grid.")
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--parallel", type=int, default=16)
    parser.add_argument("--content-language", choices=("zh-CN", "en-US"), default="zh-CN")
    parser.add_argument("--llm-config", default=None)
    parser.add_argument("--transport-retries", type=int, default=4)
    parser.add_argument(
        "--profiles",
        default=None,
        help=(
            "Comma-separated profile:label entries. When omitted, use the frozen "
            "historical ARMS tuple; e.g. gpt-5.6-terra:terra."
        ),
    )
    stream_mode = parser.add_mutually_exclusive_group()
    stream_mode.add_argument("--stream", dest="streaming", action="store_true")
    stream_mode.add_argument("--no-stream", dest="streaming", action="store_false")
    # All grid cells use streaming unless the operator explicitly selects
    # ``--no-stream``.  This keeps baseline transport behavior comparable to
    # the method and avoids adapter-dependent first-token timeouts.
    parser.set_defaults(streaming=True)
    parser.add_argument("--rounds", default="1,2,3", help="comma-separated round indices")
    parser.add_argument("--cases", default=None, help="comma-separated subset, for smoke only")
    parser.add_argument(
        "--allow-stale",
        action="store_true",
        help="⛔ only for the case where you have personally verified the reported "
        "processes are unrelated",
    )
    args = parser.parse_args(argv)

    stale = find_stale_workers()
    if stale and not args.allow_stale:
        print("⛔ refusing to start: baseline-arm processes are still running:", flush=True)
        for line in stale:
            print(f"    {line}", flush=True)
        print(
            "Kill them first (see CLAUDE.md §3.5.1: two writers into one output dir "
            "produce silently corrupted records), then retry.",
            flush=True,
        )
        return 2

    out_root = Path(args.output_root).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    cases = (
        [c.strip() for c in args.cases.split(",") if c.strip()]
        if args.cases
        else in_scope_cases()
    )
    rounds = [int(r) for r in args.rounds.split(",") if r.strip()]
    arms = parse_arms(args.profiles)

    plan = [
        (round_index, case, profile, arm_label)
        for round_index in rounds
        for case in cases
        for profile, arm_label in arms
    ]
    _log(
        f"grid: {len(cases)} cases x {len(arms)} arms x {len(rounds)} rounds = {len(plan)} cells; "
        f"parallel={args.parallel}; out={out_root}"
    )

    records: list[dict[str, Any]] = []
    wall_started = datetime.now(timezone.utc)
    # ⭐ 按轮次分批：中断时至少留下**完整的轮次**，而 `@k` 口径按轮组织，半个轮次用不上。
    for round_index in rounds:
        batch = [item for item in plan if item[0] == round_index]
        _log(f"--- round {round_index}: {len(batch)} cells ---")
        with ThreadPoolExecutor(max_workers=args.parallel) as pool:
            futures = [
                pool.submit(
                    _one,
                    case=case,
                    profile=profile,
                    arm_label=arm_label,
                    round_index=round_index,
                    out_root=out_root,
                    content_language=args.content_language,
                    registry_path=args.llm_config,
                    transport_retries=args.transport_retries,
                    streaming=args.streaming,
                )
                for _r, case, profile, arm_label in batch
            ]
            for future in as_completed(futures):
                records.append(future.result())

    ok = [r for r in records if r.get("status") == "ok"]
    failed = [r for r in records if r.get("status") != "ok"]
    manifest = {
        "schema_version": "x1-baseline-arm-manifest/1",
        "generation": out_root.name,
        "started_at": wall_started.isoformat(),
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "cases": cases,
        "rounds": rounds,
        "arms": [{"profile": p, "label": label} for p, label in arms],
        "cells_planned": len(plan),
        "cells_ok": len(ok),
        "cells_failed": len(failed),
        "issue_total": sum(r.get("issue_count") or 0 for r in ok),
        "usage_total": {
            "input_tokens": sum((r.get("usage") or {}).get("input_tokens") or 0 for r in ok),
            "output_tokens": sum((r.get("usage") or {}).get("output_tokens") or 0 for r in ok),
        },
        "failures": [
            {
                "case": r.get("case"),
                "round": r.get("round"),
                "arm": r.get("arm_label"),
                "failure_class": r.get("failure_class"),
                "failure": r.get("failure"),
            }
            for r in failed
        ],
    }
    (out_root / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _log(
        f"done: {len(ok)} ok / {len(failed)} failed; issues={manifest['issue_total']}; "
        f"in={manifest['usage_total']['input_tokens']} out={manifest['usage_total']['output_tokens']}"
    )
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
