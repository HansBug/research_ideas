"""多轮 gist 的 README 摘要必须报**累计**格数，不是最后一轮。

## 为什么需要这条测试

`build_gist.py` 的 `main()` 对每个轮目录调一次 `_build`，而 `_build` 各写一次 README —— 后覆盖前。
于是一次传三个轮目录后，README 头部写「Cells completed: 22/22」而包里有 66 格。**文件数是对的（数据
完整），只有摘要行被覆盖。**

我在 v23 的 PR comment 里**披露**过这件事（「README 头部是单轮口径」），但没修工具。结果它在 v24 又
出现了 —— 而下一个读 gist 的人若没读到那句说明，就会以为只跑了 22 格。

📌 **披露不等于修复。** 当时选了便宜的那个，成本是每代次重复披露 + 依赖读者读到那句话。这条测试把
成本一次性付掉。
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
# ⛔ 归档后脚本与测试同在 `scripts/`，原先的 `…/ "discover_matrix"` 指向不存在的目录。
TOOL = HERE / "build_gist.py"


def _cell(run: pathlib.Path, name: str, *, issues: int) -> None:
    cell = run / name
    (cell / "records").mkdir(parents=True)
    (cell / "discover-completed.json").write_text(json.dumps({
        "schema_name": "DiscoverCompleted", "status": "completed",
        "coverage_status": "full",
        "issues": [{"issue_id": f"ISSUE-{i}", "title": f"t{i}", "rationale": "r",
                    "requirement_ids": [], "assertion_ids": [],
                    "attribution_status": "safe"} for i in range(issues)],
        "excluded_findings": [], "excluded_observations": [], "coverage_gaps": [],
        "satisfied_requirement_ids": [],
    }, ensure_ascii=False))


def test_readme_counts_every_round_not_just_the_last(tmp_path: pathlib.Path) -> None:
    if not TOOL.is_file():
        pytest.skip("no build_gist.py")

    runs = tmp_path / "runs"
    for index, run_name in enumerate(("run1", "run2", "run3"), start=1):
        run = runs / run_name
        run.mkdir(parents=True)
        _cell(run, "0000-claude", issues=index)      # 每轮 issue 数不同，防「碰巧相等」
        _cell(run, "0006-gpt", issues=index)

    out = tmp_path / "bundle"
    result = subprocess.run(
        [sys.executable, str(TOOL), str(runs / "run1"), str(runs / "run2"),
         str(runs / "run3"), str(out)],
        capture_output=True, text=True, timeout=300,
    )
    assert result.returncode == 0, result.stderr[-2000:]

    for name in ("readable", "audit"):
        readme = out / name / "README.md"
        assert readme.is_file(), f"{name} 缺 README"
        text = readme.read_text()
        assert "Cells completed: 6/6" in text, (
            f"{name}/README.md 未报累计格数。三轮各 2 格共 6 格，"
            f"而 README 里的摘要行是：\n"
            + "\n".join(l for l in text.splitlines() if "Cells completed" in l)
            + "\n\n若它写 2/2，说明 README 仍被最后一轮覆盖 —— 读者会以为只跑了一轮。"
        )
        # issue 总数 = (1+1) + (2+2) + (3+3) = 12
        assert "Confirmed issues: 12." in text, (
            f"{name}/README.md 的 issue 总数不是累计值。"
            + "\n".join(l for l in text.splitlines() if "Confirmed issues" in l)
        )
