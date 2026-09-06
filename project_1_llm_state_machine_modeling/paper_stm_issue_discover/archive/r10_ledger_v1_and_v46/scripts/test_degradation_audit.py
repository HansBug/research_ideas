"""降级扫描器必须只认 `degraded_stages`，且不能把降级格算进精度侧。

锁的是两处容易写错的判据：

1. **不能用 `coverage_status == "partial"` 代替。** 逐项隔离也会 partial，那是常态；
   用它当判据会把大多数正常格误报成降级，报警一旦失真就等于没有。
2. **降级格必须被排除在精度侧之外，但保留在召回侧。** 它确实产出了制品，命中就是命中；
   但某个阶段停止了把关，它发布的东西没经过完整评审。两侧一起排除会浪费样本，
   两侧都不排除会污染精度。
"""

from __future__ import annotations

import json
import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import degradation_audit  # noqa: E402


def _cell(root: pathlib.Path, name: str, payload: dict, *, failed: bool = False) -> None:
    run, cell = name.split("/")
    target = root / run / cell
    target.mkdir(parents=True, exist_ok=True)
    filename = "discover-failed.json" if failed else "discover-completed.json"
    (target / filename).write_text(json.dumps(payload, ensure_ascii=False))


@pytest.fixture()
def generation(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> str:
    root = tmp_path / "matrix-test"
    _cell(
        root,
        "run1/0001-claude",
        {"issues": [{"title": "a"}], "coverage_status": "full", "degraded_stages": []},
    )
    # partial but NOT degraded: ordinary per-item isolation. Must not be reported.
    _cell(
        root,
        "run1/0002-claude",
        {
            "issues": [{"title": "b"}],
            "coverage_status": "partial",
            "degraded_stages": [],
            "coverage_gaps": [
                {"gap_id": "GAP-AST-1-REVIEW", "assertion_ids": ["AST-1"]},
                # 需求级隔离：assertion_ids 天然为空，但它是常态隔离而非降级。
                {"gap_id": "GAP-REQ-032-REVIEW", "assertion_ids": []},
            ],
        },
    )
    _cell(
        root,
        "run2/0003-gpt",
        {
            "issues": [],
            "coverage_status": "partial",
            "degraded_stages": ["convert_assertions: budget exhausted"],
            "coverage_gaps": [{"gap_id": "GAP-REQ-001-CONVERSION-DEGRADED", "assertion_ids": []}],
        },
    )
    _cell(
        root,
        "run3/0004-gpt",
        {"error_type": "AuthenticationError", "error_message": "401", "coverage_gaps": []},
        failed=True,
    )
    monkeypatch.setattr(degradation_audit, "RUNS", tmp_path)
    return "matrix-test"


def test_only_degraded_stages_counts_as_degradation(generation: str) -> None:
    result = degradation_audit.scan(generation)
    assert result["landed"] == 3
    assert result["degraded"] == 1
    assert [item["cell"] for item in result["degraded_cells"]] == ["run2/0003-gpt"]


def test_partial_coverage_alone_is_not_degradation(generation: str) -> None:
    """逐项隔离是常态；用 partial 当判据会让报警失真。"""

    result = degradation_audit.scan(generation)
    partial_but_clean = next(
        item for item in result["cells"] if item["cell"] == "run1/0002-claude"
    )
    assert partial_but_clean["coverage_status"] == "partial"
    assert partial_but_clean["degraded"] is False
    assert partial_but_clean["isolation_gaps"] == 2, (
        "断言级与需求级隔离都算隔离；需求级的 assertion_ids 天然为空，不得据此当成降级"
    )
    assert partial_but_clean["degradation_gaps"] == 0


def test_degraded_cells_are_kept_out_of_precision_only(generation: str) -> None:
    result = degradation_audit.scan(generation)
    assert "run2/0003-gpt" not in result["eligible_for_precision"]
    assert set(result["eligible_for_precision"]) == {
        "run1/0001-claude",
        "run1/0002-claude",
    }
    # 仍在总表里，因此召回侧照常可用。
    assert "run2/0003-gpt" in {item["cell"] for item in result["cells"]}


def test_a_cell_that_never_landed_is_reported_separately(generation: str) -> None:
    result = degradation_audit.scan(generation)
    assert result["not_landed"] == 1
    assert result["failed_cells"][0]["error_type"] == "AuthenticationError"


def test_a_stale_failure_receipt_is_ignored_when_the_retry_landed(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """重试成功后旧收据仍在盘上；把它算成未落盘会虚报失败数。"""

    root = tmp_path / "matrix-stale"
    _cell(root, "run1/0009-gpt", {"issues": [], "degraded_stages": []})
    _cell(root, "run1/0009-gpt", {"error_type": "RuntimeError"}, failed=True)
    monkeypatch.setattr(degradation_audit, "RUNS", tmp_path)
    result = degradation_audit.scan("matrix-stale")
    assert result["landed"] == 1
    assert result["not_landed"] == 0


def test_abandoned_try_directories_are_not_counted_as_separate_cells(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`run1/0039-gpt.try3` 与 `run1/0039-gpt` 是同一格。

    启动器在每次整格重试前把目录改名为 `<cell>.tryN`，于是每次放弃的尝试都留下自己的失败收据。
    把它们当独立的格，会让 v41 的「未落盘」从 2 虚报成 13——一个用来把安静问题变响亮的工具，
    绝不能自己制造响亮的假问题。
    """

    root = tmp_path / "matrix-try"
    for suffix in (".try1", ".try2", ".try3"):
        _cell(root, f"run1/0039-gpt{suffix}", {"error_type": "RuntimeError"}, failed=True)
    _cell(root, "run1/0039-gpt", {"error_type": "RuntimeError"}, failed=True)
    monkeypatch.setattr(degradation_audit, "RUNS", tmp_path)
    result = degradation_audit.scan("matrix-try")
    assert result["not_landed"] == 1
    assert result["failed_cells"][0]["cell"] == "run1/0039-gpt"


def test_a_try_directory_does_not_shadow_the_landed_cell(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "matrix-try2"
    _cell(root, "run1/0030-gpt.try4", {"error_type": "RuntimeError"}, failed=True)
    _cell(root, "run1/0030-gpt", {"issues": [], "degraded_stages": []})
    monkeypatch.setattr(degradation_audit, "RUNS", tmp_path)
    result = degradation_audit.scan("matrix-try2")
    assert result["landed"] == 1
    assert result["not_landed"] == 0
