"""发布层的三条纪律，各配一条负控。

这些都不是假想问题。dry-run review 用 v21 真实产物走了一遍第 5 步，三条全部复现：

  `build_gist.py run1 run2 run3 <out>`  → main() 只读 argv[1] 与 argv[2]，于是 **run2 变成
                                          输出目录**、run3 被丢弃、`<out>` 从未创建，而它
                                          打印的是成功信息。分析产物写进了证据目录。
  三轮写进同一 out                       → 文件名 stem 是 `PAIR-PROFILE`，后一轮覆盖前一轮：
                                          三次调用各打印 `wrote 11 cells`、无告警，最终包里
                                          12 份文件、索引只剩 run3。
  发布包里的机械判定                     → `expected_issue_verdicts` 读的是另一份台账
                                          （`EXP-*` 16 条），对持有可报记录 `EIS-0032-02` 的
                                          `0032` 写「本 pair 无期望问题 / 0 confirmed 即为
                                          正解」，旁边还挂着 `provenance: frozen`。

第一条我自己写守卫时又漏了一半：先只拦了「out 是轮次目录的祖先」，没拦「out 就在 `runs/` 之
下」，于是负控用那条命令的真实故障形态立刻打回来。所以三种形态各留一条断言。
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PY = ROOT / "venv" / "bin" / "python"
V21 = ROOT / "runs" / "paper1" / "matrix-v21"


def _run(*args: str):
    return subprocess.run(
        [str(PY), str(HERE / "build_gist.py"), *args],
        cwd=HERE,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": f"{ROOT}:{HERE}", "PATH": "/usr/bin:/bin", "HOME": str(pathlib.Path.home())},
    )


def _skip_without_v21():
    if not (V21 / "run1").is_dir():
        import pytest

        pytest.skip("no v21 run bundle in this checkout")


def test_it_refuses_to_write_into_a_round_directory() -> None:
    """The literal failure of the pre-registered double-report command."""
    _skip_without_v21()
    done = _run(str(V21 / "run1"), str(V21 / "run2"))
    assert done.returncode == 1, done.stdout
    assert "refusing to write" in done.stderr
    # And it must not have written anything on the way to refusing.
    assert not (V21 / "run2" / "audit").exists()


def test_it_refuses_an_out_dir_that_contains_the_round() -> None:
    _skip_without_v21()
    done = _run(str(V21 / "run1"), str(V21))
    assert done.returncode == 1, done.stdout


def test_it_refuses_anywhere_under_runs() -> None:
    """The half I missed the first time. `runs/` holds evidence, not analysis products."""
    _skip_without_v21()
    done = _run(str(V21 / "run1"), str(ROOT / "runs" / "paper1" / "nowhere"))
    assert done.returncode == 1, done.stdout
    assert not (ROOT / "runs" / "paper1" / "nowhere").exists()


def test_three_rounds_do_not_collapse_into_one(tmp_path) -> None:
    """Round in the file stem and in the index, and the index accumulates across rounds."""
    _skip_without_v21()
    rounds = [str(V21 / f"run{n}") for n in (1, 2, 3) if (V21 / f"run{n}").is_dir()]
    if len(rounds) < 2:
        import pytest

        pytest.skip("need at least two rounds")
    done = _run(*rounds, str(tmp_path / "bundle"))
    assert done.returncode == 0, done.stderr
    audits = sorted((tmp_path / "bundle" / "audit").glob("*-audit.json"))
    assert len(audits) >= 11 * len(rounds), [p.name for p in audits]
    index = (tmp_path / "bundle" / "audit" / "run-index.tsv").read_text().splitlines()
    header = index[0].split("\t")
    assert "round" in header
    seen = {line.split("\t")[header.index("round")] for line in index[1:]}
    assert seen == {pathlib.Path(r).name for r in rounds}, seen


def test_the_bundle_carries_no_machine_verdict(tmp_path) -> None:
    """Raw material for the human judgement, and no second version of the conclusion."""
    _skip_without_v21()
    done = _run(str(V21 / "run1"), str(tmp_path / "bundle"))
    assert done.returncode == 0, done.stderr
    for path in (tmp_path / "bundle" / "audit").glob("*-audit.json"):
        payload = json.loads(path.read_text())
        assert "expected_issue_verdicts" not in payload, path.name
        assert "expected_records_for_judgment" in payload, path.name
        assert payload["expected_ledger"].endswith("expected_issue_set.json")
        assert payload["expected_ledger_sha256"]


def test_the_0032_cell_shows_its_reportable_record(tmp_path) -> None:
    """The specific regression: it used to say this pair had no expected issue at all.

    `0032` holds `EIS-0032-02`, one of the records the capability claim rests on. Under the old
    ledger it had zero `EXP-*` entries, so the published bundle told the reader that zero
    confirmed issues was the correct answer for it.
    """
    _skip_without_v21()
    done = _run(str(V21 / "run1"), str(tmp_path / "bundle"))
    assert done.returncode == 0, done.stderr
    matches = list((tmp_path / "bundle" / "audit").glob("*0032*-audit.json"))
    if not matches:
        import pytest

        pytest.skip("0032 not in this round")
    rows = json.loads(matches[0].read_text())["expected_records_for_judgment"]
    ids = {row["record"] for row in rows}
    assert "EIS-0032-02" in ids, rows
    reportable = [row for row in rows if "可报" in row["eligibility"]]
    assert reportable, rows


def test_the_readme_scope_is_derived_from_the_data(tmp_path) -> None:
    """It used to name four pairs and two models regardless of what the bundle held."""
    _skip_without_v21()
    done = _run(str(V21 / "run1"), str(tmp_path / "bundle"))
    assert done.returncode == 0, done.stderr
    readme = (tmp_path / "bundle" / "readable" / "README.md").read_text()
    assert "0032" in readme.split("\n")[2] or "0032" in readme[:400], readme[:400]
    assert "0000 / 0006 / 0029 / 0050," not in readme
