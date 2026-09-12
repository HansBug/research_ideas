"""`onepass_merge.py` 的合流语义与**四道拒绝路径**。

拒绝路径为什么必须有测试：它们全都是「缺数据 / 数据不匹配时应当拒绝，而不是给个默认值」。这类逻辑
一旦静默失效，症状是**得到一个看起来正常的数字**，而不是报错 —— 本目录已经栽过三次：

1. `check_partition_closure.py` 首版在未传 `--over` 时 `.get("holds", True)` 放行，于是在最该拦的
   情形（没给多报数据）反而通过。
2. κ 曾算出 −0.2，因为 `unit_id` 是**位置性**的、不是内容寻址的，40 单元的判定被对到 68 单元的 key 上。
3. `build_gist.py` 漏了 `.try` 排除，格数 66→24、issue 246→82，**且无任何报错**。

所以这里对每条拒绝都断言它**确实拒绝**，而不只是断言正常路径能跑通。
"""

from __future__ import annotations

import importlib.util
import json
import pathlib

import pytest

HERE = pathlib.Path(__file__).resolve().parent
# ⛔ 归档后脚本与测试同在 `scripts/`，原先的 `…/ "discover_matrix"` 指向不存在的目录。
MATRIX = HERE
SAMPLE_DIR = MATRIX / "onepass_sample"


def _module():
    path = MATRIX / "onepass_merge.py"
    if not path.is_file():
        pytest.skip("no onepass_merge.py")
    spec = importlib.util.spec_from_file_location("onepass_merge", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fixture():
    """真样本 + key。没有它们就跳过 —— 合成一份会把 alias 契约也一起编造。"""

    s, k = SAMPLE_DIR / "sample.json", SAMPLE_DIR / "key.json"
    if not (s.is_file() and k.is_file()):
        pytest.skip("no onepass sample on disk")
    return json.loads(s.read_text()), json.loads(k.read_text())


def _annotation(sample: dict, *, flip_every: int = 0) -> dict:
    """一份完整标注。`flip_every > 0` 时每 N 条改成 `boundary`，用于造分歧。"""

    labels, n = {}, 0
    for item in sample["items"]:
        aliases = [d["record_alias"] for d in item["expected_defects"]]
        for index, issue in enumerate(item["published_issues"]):
            if aliases and index == 0:
                label = f"hits:{aliases[0]}"
            elif index == 1:
                label = "fabricated"
            else:
                label = "grounded-extra"
            n += 1
            if flip_every and n % flip_every == 0:
                label = "boundary"
            labels[issue["issue_uid"]] = {"label": label, "form": None, "why": "fixture"}
    return {"annotator": "X", "sample_id": sample["sample_id"],
            "labels": labels, "unhit_expected": {}}


def test_identical_annotations_give_kappa_one() -> None:
    module = _module()
    sample, key = _fixture()
    a = _annotation(sample)
    merged = module.merge(sample, key, a, dict(a), "error")
    assert merged["kappa_label"]["kappa"] == 1.0
    assert merged["kappa_coverage"]["kappa"] == 1.0
    assert merged["kappa_label"]["disagreements"] == 0


def test_coverage_kappa_is_never_below_label_kappa() -> None:
    """覆盖侧 κ 是标签 κ 的**粗化**，必然 ≥ 后者。

    这不是经验观察，是构造性事实：两人可以对「哪条 issue 命中了它」分歧但同意「它被命中了」，
    粗化只抹掉分歧、不造出分歧。

    钉住它的理由：**只报覆盖侧 κ 会系统性高估一致性。** 前几代次报的 κ=0.980 正是覆盖侧口径 ——
    那个数没错，但它不能证明标注者对「这条 issue 是什么」一致。
    """

    module = _module()
    sample, key = _fixture()
    merged = module.merge(
        sample, key, _annotation(sample), _annotation(sample, flip_every=7), "conservative"
    )
    label = merged["kappa_label"]["kappa"]
    coverage = merged["kappa_coverage"]["kappa"]
    assert label is not None and coverage is not None
    assert coverage >= label, (
        f"覆盖侧 κ={coverage} < 标签 κ={label}。粗化不可能造出分歧 —— "
        "若真的出现，说明覆盖侧派生逻辑引入了标签层没有的分歧源。"
    )


def test_disagreement_with_error_policy_is_refused() -> None:
    module = _module()
    sample, key = _fixture()
    with pytest.raises(SystemExit) as excinfo:
        module.merge(sample, key, _annotation(sample),
                     _annotation(sample, flip_every=5), "error")
    assert "分歧" in str(excinfo.value)


def test_incomplete_annotation_is_refused() -> None:
    """缺标注不得当成某个默认标签。零输入不能读成一次干净的检查。"""

    module = _module()
    sample, key = _fixture()
    incomplete = _annotation(sample)
    incomplete["labels"].pop(next(iter(incomplete["labels"])))
    with pytest.raises(SystemExit) as excinfo:
        module.merge(sample, key, incomplete, _annotation(sample), "error")
    assert "不完整" in str(excinfo.value)


def test_sample_id_mismatch_is_refused(tmp_path: pathlib.Path) -> None:
    """按位置配对不同样本会算出无意义的 κ —— 上一代次实测 −0.2。"""

    module = _module()
    sample, _ = _fixture()
    bad = _annotation(sample)
    bad["sample_id"] = "deadbeef00000000"
    path = tmp_path / "annotation_X.json"
    path.write_text(json.dumps(bad))
    with pytest.raises(SystemExit) as excinfo:
        module._load(path, sample["sample_id"])
    assert "sample_id" in str(excinfo.value)


def test_hits_and_fabricated_cannot_both_count_the_same_issue() -> None:
    """不变量：`hit-evidence ∩ fabricated = ∅`，**靠构造成立**。

    上一代次的 `台账命中 / 台账外` 划分实测 ≥23/82 双计，因为两侧用了两个不同的匹配器。这里两侧从
    同一份标签派生，一条 issue 只有一个标签，所以双计**不可表达** —— 这条测试确认派生逻辑没有把它
    重新引入（例如把 `hits:` 也计入 fabricated 池）。
    """

    module = _module()
    sample, key = _fixture()
    a = _annotation(sample)
    merged = module.merge(sample, key, a, dict(a), "error")

    hit_uids = {uid for uid, v in a["labels"].items() if v["label"].startswith("hits:")}
    fab_uids = {uid for uid, v in a["labels"].items() if v["label"] == "fabricated"}
    assert not (hit_uids & fab_uids)
    assert sum(merged["over_by_arm_A"].values()) == len(fab_uids), (
        "多报计数与 `fabricated` 标签数不符 —— 派生逻辑把别的标签也算进去了"
    )


def test_to_verdicts_shape_matches_what_full_tables_consumes() -> None:
    module = _module()
    sample, key = _fixture()
    a = _annotation(sample)
    verdicts = module.to_verdicts(module.merge(sample, key, a, dict(a), "error"))
    assert verdicts["verdicts"]
    for record_id, arms in verdicts["verdicts"].items():
        assert record_id.startswith("EIS-")
        for arm, series in arms.items():
            assert arm in ("claude", "gpt")
            assert isinstance(series, list) and series
            assert all(v in (0, 1, None) for v in series)
