"""编排层的守卫：残留进程检查⛔ 不许把自己拒掉，网格规模⛔ 不许漂。

⚠️ 这个文件是**回归测试**：初版 `find_stale_workers()` 只排除 `os.getpid()`，于是它匹配到了
包裹自己的父 shell（`bash -c '... launch.py ...'`）并拒绝启动。⛔ 而当时的调用带 `| tail`，
管道把退出码 2 换成了 tail 的 0 —— 一个 fail-safe 的拒绝因此看起来像**成功完成**，直到去读
manifest 才发现它不存在。

⭐ 两条都要钉住：守卫的自指 bug（本文件），以及⛔ 跑网格时不许用管道吞退出码（写进 README）。
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ARM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ARM / "src"))

import launch  # noqa: E402


def test_own_process_chain_includes_self_and_ancestors() -> None:
    chain = launch.own_process_chain()
    assert str(os.getpid()) in chain, "the chain must contain this process"
    assert str(os.getppid()) in chain, "the chain must contain the parent"
    assert len(chain) >= 2


def test_guard_does_not_flag_itself_when_launched_through_a_shell() -> None:
    """⭐ 核心回归：经 shell 包装启动时，守卫必须报「无残留」。

    ⚠️ 复现初版的失败条件——父进程的命令行里含 `baseline_arm/src/launch.py` 这个特征串。
    """

    program = (
        "import sys, json\n"
        f"sys.path.insert(0, {str(ARM / 'src')!r})\n"
        "import launch\n"
        "print('STALE=' + json.dumps(launch.find_stale_workers()))\n"
    )
    # 刻意经 `bash -c` 启动，且让父进程的 args 里出现特征串。
    shell_cmd = (
        f"# baseline_arm/src/launch.py marker for the guard to trip over\n"
        f"exec {sys.executable} -c {_quote(program)}"
    )
    result = subprocess.run(
        ["bash", "-c", shell_cmd], capture_output=True, text=True, timeout=120
    )
    assert result.returncode == 0, f"probe failed:\n{result.stderr}"
    line = [ln for ln in result.stdout.splitlines() if ln.startswith("STALE=")]
    assert line, f"probe produced no verdict:\n{result.stdout}\n{result.stderr}"
    import json

    stale = json.loads(line[-1].removeprefix("STALE="))
    assert stale == [], (
        "the guard flagged its own ancestor chain; that is the initial bug "
        f"(reported: {stale})"
    )


def test_grid_is_fixed_at_54_pairs() -> None:
    """⛔ 网格恒为 54：`00x8` 家族永久排除，且规模漂移必须炸而不是静默。"""

    cases = launch.in_scope_cases()
    assert len(cases) == 54
    assert not [c for c in cases if c.endswith("8")]


def test_arms_are_the_same_two_models_as_the_main_arm() -> None:
    """⛔ 不许降级模型档（§4B.2 的「不许省」栏）。"""

    assert launch.ARMS == (("gpt-5.5", "gpt"), ("claude-opus-4-7", "claude"))
    assert launch.ROUNDS == (1, 2, 3)


def test_parse_arms_supports_an_explicit_smoke_profile() -> None:
    assert launch.parse_arms("gpt-5.6-terra:terra") == (("gpt-5.6-terra", "terra"),)


def test_parse_arms_rejects_malformed_entries() -> None:
    import pytest

    with pytest.raises(SystemExit, match="profile:label"):
        launch.parse_arms("gpt-5.6-terra")


def test_cell_dir_layout_matches_the_judging_material_reader() -> None:
    """目录布局是 `present.py` 与判定表键的共同约定，改它会静默断开两侧。"""

    path = launch.cell_dir(Path("/tmp/out"), 2, "0007", "claude")
    assert path == Path("/tmp/out/run2/0007-claude")


def _quote(text: str) -> str:
    return "'" + text.replace("'", "'\"'\"'") + "'"
