"""一次运行的全部格子是否跑在同一份代码上，以及那份代码是哪个 commit。

## 为什么需要

run record 里没有代码版本字段（`discover-run-started` 有 `pyfcstm_version`，没有本仓库的
commit），所以「这次运行归属哪个 commit」只能靠时间戳反推 —— 而这正是审查「实验是否公平」时
最先要查的东西。`CLAUDE.md` §3.5.1 因此要求开跑前先 push。

但 push 只保证起点可追，不保证**运行期间代码没变**。每个格子是一个新起的 `python -m` 进程，
所以在长跑中途改 pipeline 源码，会让后启动的格子用另一份代码 —— 66 格跑几小时，中途提交是很
自然的事，而结果会变成一次异质运行，且没有任何东西会提示。

本脚本做两件事：

1. **落一份 manifest**（`--record`）：把开跑 commit、格集、时间戳写进 eval 目录。写在这里而不是
   `runs/` 下，是因为 `runs/` 被 gitignore，而这条事实必须进版本库才叫可追。
2. **核验同质性**（`--verify`）：比对 manifest 里的 commit 与当前 HEAD 之间，pipeline 的
   `src/` 有没有被改过；再比对每格完成时间是否都晚于该 commit。

只看 `src/`：eval 侧脚本不参与运行，改它们不影响任何格子的产出。
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SRC_GLOB = "*/pipeline/feedback_loop/src/*"
MANIFEST = HERE / "run_manifests.json"


def _git(*args: str) -> str:
    done = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if done.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {done.stderr.strip()}")
    return done.stdout.strip()


def _load() -> dict:
    if MANIFEST.is_file():
        return json.loads(MANIFEST.read_text())
    return {}


def record(generation: str, base: pathlib.Path) -> int:
    import run_grid

    head = _git("rev-parse", "HEAD")
    dirty = _git("status", "--porcelain")
    tracked_dirty = [line for line in dirty.splitlines() if not line.startswith("??")]
    manifests = _load()
    manifests[generation] = {
        "launch_commit": head,
        "launch_commit_short": head[:9],
        "launched_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "grid": run_grid.grid(),
        "base": str(base),
        # 起跑时工作区若不干净，那次运行就不完全归属于任何一个 commit。如实记录，不修饰。
        "worktree_clean_at_launch": not tracked_dirty,
        "uncommitted_at_launch": tracked_dirty,
    }
    MANIFEST.write_text(json.dumps(manifests, ensure_ascii=False, indent=1) + "\n")
    print(f"recorded {generation}: commit {head[:9]}, {len(manifests[generation]['grid'])} pairs")
    if tracked_dirty:
        print("⚠️ 起跑时工作区不干净，这次运行不完全归属于该 commit：", file=sys.stderr)
        for line in tracked_dirty:
            print(f"    {line}", file=sys.stderr)
        return 1
    return 0


def verify(generation: str) -> int:
    manifests = _load()
    entry = manifests.get(generation)
    if not entry:
        print(
            f"no manifest for {generation}. 没有 manifest 就无法判断同质性 —— 这不是"
            "「同质」，是「不知道」，所以非零退出。",
            file=sys.stderr,
        )
        return 2
    launch = entry["launch_commit"]
    changed = _git("diff", "--name-only", f"{launch}..HEAD", "--", SRC_GLOB).splitlines()
    problems = []
    if changed:
        problems.append(
            f"pipeline 源码在开跑后被改过 {len(changed)} 个文件。后启动的格子用的是另一份"
            f"代码，这次运行是异质的：\n    " + "\n    ".join(changed[:10])
        )
    unstaged = _git("diff", "--name-only", "--", SRC_GLOB).splitlines()
    if unstaged:
        problems.append(f"pipeline 源码当前有未提交改动：{unstaged[:6]}")
    if not entry.get("worktree_clean_at_launch", True):
        problems.append(
            "起跑时工作区就不干净，见 manifest 的 `uncommitted_at_launch`；"
            "这次运行不完全归属于任何一个 commit"
        )
    base = pathlib.Path(entry["base"])
    if base.is_dir():
        cells = sorted(base.glob("run*/*/discover-completed.json"))
        print(f"{generation}: commit {entry['launch_commit_short']}, 已完成 {len(cells)} 格")
    else:
        print(f"{generation}: commit {entry['launch_commit_short']}, 运行目录尚不存在")
    for problem in problems:
        print(f"FAIL {problem}", file=sys.stderr)
    if problems:
        return 1
    print("ok: 开跑至今 pipeline 源码未变，运行同质")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("generation", help="如 v22")
    parser.add_argument("--record", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--base", type=pathlib.Path)
    args = parser.parse_args(argv)
    if args.record:
        base = args.base or (ROOT / "runs" / "paper1" / f"matrix-{args.generation}")
        return record(args.generation, base)
    if args.verify:
        return verify(args.generation)
    parser.error("需要 --record 或 --verify")
    return 2


if __name__ == "__main__":
    sys.exit(main())
