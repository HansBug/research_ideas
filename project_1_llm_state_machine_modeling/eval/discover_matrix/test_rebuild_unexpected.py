"""重建器只许改形状，不许改裁定，且必须拦住「待定」。

锁四件事，每一件都对应本目录真实犯过的错：

1. **改了真源就必须能一键重建全部派生物。** 手工重建四次错四次，全是「改了 jsonl 忘了重建某一份」。
2. **已作废的标签必须硬拦。** `UNCERTAIN`（没查完）与 `MERGE_INTO_LEDGER`（内容已被台账承载、
   根本不属意外发现）都曾短暂存在过；留着它们重建等于把「没查」和「不该在这」冒充成裁定。
3. **裁定原样透传。** 重建器不做判定，jsonl 说什么就是什么。
4. **缺字段直接失败。** 判据不全的裁定不是裁定，不能靠空字符串蒙混过关。
"""

from __future__ import annotations

import csv
import json
import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import rebuild_unexpected as R  # noqa: E402


def _seed(tmp: pathlib.Path, records: list[dict]) -> pathlib.Path:
    verdicts = tmp / "unexpected_verdicts"
    verdicts.mkdir(parents=True, exist_ok=True)
    (verdicts / "G1.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in records)
    )
    return verdicts


def _rec(cluster: str, verdict: str, **kw) -> dict:
    base = {"cluster": cluster, "verdict": verdict, "fact": "某事实", "nl": "某 NL 依据"}
    base.update(kw)
    return base


@pytest.fixture()
def wired(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> pathlib.Path:
    verdicts = _seed(tmp_path, [
        _rec("0017-1", "VALID_UNRECORDED"),
        _rec("0017-2", "REPRESENTATION_DEBT"),
        _rec("0029-1", "NO_NL_BASIS"),
    ])
    monkeypatch.setattr(R, "VERDICTS", verdicts)
    monkeypatch.setattr(R, "HERE", tmp_path)
    return tmp_path


@pytest.mark.parametrize(
    ("label", "match"),
    [("UNCERTAIN", "证据不足不是裁定类别"), ("MERGE_INTO_LEDGER", "不属意外发现")],
)
def test_retired_labels_are_rejected_not_rendered(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, label: str, match: str
) -> None:
    """作废标签带着它重建必须失败，而不是渲染出多一列。

    `MERGE_INTO_LEDGER` 尤其重要：它当初的存在本身就是分类错误——内容已被台账承载的产出
    不属于意外发现，留在桶里会让分母虚高 13/293。
    """

    verdicts = _seed(tmp_path, [_rec("0044-2", label), _rec("0044-3", "NO_NL_BASIS")])
    monkeypatch.setattr(R, "VERDICTS", verdicts)
    monkeypatch.setattr(R, "HERE", tmp_path)
    with pytest.raises(SystemExit, match=match):
        R.main([])
    # 关键：拒绝时不得留下半成品派生物，否则下游会读到只重建了一半的表。
    assert not (tmp_path / "V46_UNEXPECTED_EVIDENCE.md").exists()


def test_all_derived_artifacts_are_rebuilt_together(wired: pathlib.Path) -> None:
    """四份派生物必须一次全出——漏掉任何一份就是历史上那四次错。"""

    assert R.main([]) == 0
    for name in ("cluster_index.tsv", "by_pair.tsv", "final_rootcause.tsv"):
        assert (wired / "unexpected_verdicts" / name).is_file(), name
    assert (wired / "V46_UNEXPECTED_EVIDENCE.md").is_file()


def test_verdicts_pass_through_untouched(wired: pathlib.Path) -> None:
    """重建器不做判定。"""

    R.main([])
    index = {
        row["cluster"]: row["verdict"]
        for row in csv.DictReader((wired / "unexpected_verdicts" / "cluster_index.tsv").open(), delimiter="\t")
    }
    assert index == {
        "0017-1": "VALID_UNRECORDED",
        "0017-2": "REPRESENTATION_DEBT",
        "0029-1": "NO_NL_BASIS",
    }


def test_evidence_covers_every_cluster(wired: pathlib.Path) -> None:
    """逐簇证据不许抽样——少一簇，那一簇的判据就没人能复核。"""

    R.main([])
    text = (wired / "V46_UNEXPECTED_EVIDENCE.md").read_text()
    for cluster in ("0017-1", "0017-2", "0029-1"):
        assert f"**{cluster}**" in text, cluster


def test_missing_evidence_field_fails_loudly(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """判据不全的裁定不是裁定。"""

    verdicts = _seed(tmp_path, [_rec("0017-1", "VALID_UNRECORDED", fact="")])
    monkeypatch.setattr(R, "VERDICTS", verdicts)
    monkeypatch.setattr(R, "HERE", tmp_path)
    with pytest.raises(SystemExit, match="缺字段 fact"):
        R.main([])


def test_unknown_verdict_label_fails(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """五类之外没有第六类。新造标签必须撞墙，否则分类学形同虚设。"""

    verdicts = _seed(tmp_path, [_rec("0017-1", "PROBABLY_FINE")])
    monkeypatch.setattr(R, "VERDICTS", verdicts)
    monkeypatch.setattr(R, "HERE", tmp_path)
    with pytest.raises(SystemExit, match="不在五类内"):
        R.main([])


def test_check_mode_does_not_write(wired: pathlib.Path) -> None:
    assert R.main(["--check"]) == 0
    assert not (wired / "V46_UNEXPECTED_EVIDENCE.md").exists()
