"""⛔ 判定材料的泄漏面：三条禁止 + 三条必需。

⚠️ **这是与 `test_prompt_no_leakage.py` 不同的泄漏面**，⛔ 两者不可互相代替：
那个管**生成端 prompt**（对照臂能看到什么），本文件管**判定端材料**（判定者能看到什么）。

⭐ 本文件替代了「混臂盲判」那个提议。⚠️ 混臂盲判必须重判主臂已冻结的位（与 588 冻结冲突），
而判定者被主臂结果锚定这一条通道，⭐ **可以在不重判主臂的前提下直接切断**——只要主臂的逐位判定
根本不进材料。⛔ 一条会失败的测试，不是一句注释。

⚠️ 仓库已有同类先例 `discover_matrix/test_judge_materials_carry_no_verdicts.py`，但它有三个
已知盲区（只扫 3 个静态文档不扫样本本身 · pair 编号白名单硬编码 11 个 · 文件缺失时
`pytest.skip` 而非失败）。⭐ 本文件扫**生成出来的材料本身**，且⛔ 缺文件即失败。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

ARM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ARM / "src"))

import present  # noqa: E402


def _fake_run_root(tmp_path: Path, pairs: list[str]) -> Path:
    """造一个最小 run root：每 pair 六格，内容刻意含可被误当成"答案"的词。"""

    root = tmp_path / "runs"
    for pair in pairs:
        for round_index in (1, 2, 3):
            for arm in ("gpt", "claude"):
                cell = root / f"run{round_index}" / f"{pair}-{arm}"
                cell.mkdir(parents=True, exist_ok=True)
                (cell / "record.json").write_text(
                    json.dumps(
                        {
                            "status": "ok",
                            "parsed_output": {
                                "analysis": "read both inputs",
                                "issues": [
                                    {
                                        "issue": f"finding on {pair}",
                                        "where": "some state",
                                        "reason": "the spec asks otherwise",
                                    }
                                ],
                            },
                        },
                        ensure_ascii=False,
                    ),
                    encoding="utf-8",
                )
    return root


@pytest.fixture(scope="module")
def built(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    """用真台账 + 真主臂 tiers（只用于算池）跑一次完整生成。"""

    tmp_path = tmp_path_factory.mktemp("judge")
    records = present.load_reportable()
    pairs = sorted({str(r["pair"])[-4:] for r in records})
    run_root = _fake_run_root(tmp_path, pairs)
    out_dir = tmp_path / "out"
    code = present.main(["--run-root", str(run_root), "--out-dir", str(out_dir)])
    assert code == 0, "generation must report exactly 588 positions"
    materials = sorted((out_dir / "materials").glob("*.md"))
    assert materials, "no materials were written"
    return {"out": out_dir, "materials": out_dir / "materials"}


def _all_material_text(built: dict[str, Path]) -> dict[str, str]:
    return {
        path.name: path.read_text(encoding="utf-8")
        for path in sorted(built["materials"].glob("*.md"))
    }


# --------------------------------------------------------------- 三条禁止


def test_materials_carry_no_main_arm_verdicts(built: dict[str, Path]) -> None:
    """⛔ 禁止一：主臂在同一位的判定结果。判定者读到它会被锚定。"""

    # 主臂判定表里的真实论证片段——若材料里出现任何一段，就是直接泄漏。
    human = json.loads(
        (
            ARM.parent / "discover_matrix" / "v46" / "verdicts" / "v46_human.json"
        ).read_text(encoding="utf-8")
    )
    samples = [
        str(entry.get("argument") or "")[:40]
        for entry in list(human.values())[:40]
        if str(entry.get("argument") or "").strip()
    ]
    assert samples, "fixture guard: expected some main-arm arguments to compare against"
    for name, text in _all_material_text(built).items():
        for sample in samples:
            assert sample not in text, f"{name} leaks a main-arm argument: {sample!r}"


def test_materials_carry_no_ledger_answer_fields(built: dict[str, Path]) -> None:
    """⛔ 禁止二：台账的「答案」字段——尤其 `replay`（那是**期望真值**）。"""

    banned = (
        "replay",
        "primary_predicate",
        "eight_cell_published",
        "ledger_eval_asserts",
        "measured_by_batch",
        "negative_control",
        "boundary_ruling",
        "layer_basis",
        "expressible_with_closed_vocabulary",
    )
    for name, text in _all_material_text(built).items():
        for needle in banned:
            assert needle not in text, f"{name} leaks ledger answer field {needle!r}"


def test_materials_carry_no_pool_membership(built: dict[str, Path]) -> None:
    """⛔ 禁止三：四池归属。⚠️ 池由主臂结果算出，它进材料等于交出主臂的逐条表现。"""

    banned = ("满格", "近满格", "不稳定", "零命中", "pool_full", "pool_zero", "6/6", "0/6")
    for name, text in _all_material_text(built).items():
        for needle in banned:
            assert needle not in text, f"{name} leaks pool membership via {needle!r}"


def test_pool_membership_lives_only_in_the_order_file(built: dict[str, Path]) -> None:
    """⭐ 物理分离：池只在 `judging_order.tsv` 里，判定者不读那个文件。"""

    order = (built["out"] / "judging_order.tsv").read_text(encoding="utf-8")
    assert "pool_full" in order and "pool_zero" in order, (
        "the order file is where pool membership belongs -- it is the audit trail for "
        "whether the judging sequence was really stratified"
    )


# --------------------------------------------------------------- 三条必需


def test_materials_carry_the_author_source_not_the_compiled_artifact(
    built: dict[str, Path],
) -> None:
    """⭐ 必需一：PlantUML 作者源。⛔ 且不得给 `model.fcstm`（编译产物）。

    ⚠️ 判缺陷读作者源不读编译产物——主臂在这一点上「八组栽七组」。
    """

    for name, text in _all_material_text(built).items():
        assert "```plantuml" in text, f"{name} is missing the PlantUML author source"
        assert "@startuml" in text, f"{name}'s PlantUML block looks empty"
        # ⚠️ 初版断言 `".fcstm" not in text`，被材料头部那句**纪律提示**（「⛔ 不读
        # `model.fcstm`」）命中——那句话正确且必要，是断言太粗。⭐ 要禁的是编译产物的
        # **内容**，⛔ 不是提到它的名字。
        assert "```fcstm" not in text, f"{name} embeds a compiled-artifact code block"
        # 正向：那句纪律提示必须在，否则判定者不知道该读哪份制品。
        assert "不读 `model.fcstm`" in text, (
            f"{name} lost the 'read the author source, not the compiled artifact' notice"
        )


def test_materials_carry_full_nl_and_ledger_statements(built: dict[str, Path]) -> None:
    """⭐ 必需二：NL 全文 + 台账 statement。⛔ 都不许截断。"""

    records = {r["id"]: r for r in present.load_reportable()}
    seen: set[str] = set()
    for name, text in _all_material_text(built).items():
        assert "## 一、需求原文" in text, f"{name} is missing the NL section"
        for record_id in re.findall(r"EIS-\d{4}-\d{2}", text):
            seen.add(record_id)
            statement = str(records[record_id]["statement"]).strip()
            assert statement in text, (
                f"{name} truncated the statement of {record_id}; judging on a truncated "
                "statement is how a conclusion clause gets cut off"
            )
    assert len(seen) == 98, f"materials must cover all 98 REPORTABLE records, saw {len(seen)}"


def test_materials_carry_all_six_cells_per_pair(built: dict[str, Path]) -> None:
    """⭐ 必需三：六格全在。⚠️ 缺格必须**显式标出**，⛔ 不能静默消失。"""

    for name, text in _all_material_text(built).items():
        for round_index in (1, 2, 3):
            for arm in ("gpt", "claude"):
                assert f"### run{round_index} · {arm}" in text, (
                    f"{name} is missing cell run{round_index}/{arm}"
                )


def test_missing_cell_is_reported_as_null_not_zero(tmp_path: Path) -> None:
    """⚠️ 缺格记 `null`，⛔ 不记 0——把 null 读成 0 会无声压低命中率。"""

    records = present.load_reportable()
    pair = str(records[0]["pair"])[-4:]
    run_root = _fake_run_root(tmp_path, [pair])
    # 删掉一格
    (run_root / "run2" / f"{pair}-gpt" / "record.json").unlink()
    out_dir = tmp_path / "out"
    present.main(["--run-root", str(run_root), "--out-dir", str(out_dir)])
    text = next((out_dir / "materials").glob(f"*-{pair}.md")).read_text(encoding="utf-8")
    assert "格缺失" in text
    assert "`null`" in text and "不记 0" in text


def test_position_count_is_exactly_588(built: dict[str, Path]) -> None:
    """⭐ 588 = 98 × 2 × 3。⛔ 少一位就是改分母。"""

    order = (built["out"] / "judging_order.tsv").read_text(encoding="utf-8").splitlines()
    total = sum(int(line.split("\t")[2]) for line in order[1:])
    assert total == 98, f"pair records must sum to 98, got {total}"
    assert total * 6 == 588


def test_judging_order_is_stratified_not_sequential(built: dict[str, Path]) -> None:
    """⭐ 顺序必须分层交错，⛔ 不是 pair 号顺序。

    ⚠️ 这条是 fallback 零成本的前提：任何时刻中断，已判集合都自动分层代表。
    """

    order = (built["out"] / "judging_order.tsv").read_text(encoding="utf-8").splitlines()
    pairs = [line.split("\t")[1] for line in order[1:]]
    assert pairs != sorted(pairs), (
        "the judging order is plain pair order; then an interrupted run yields a "
        "low-pair-number subset, not a stratified one"
    )
    # 相邻两个 pair 不应总是同一主池（交错的直接体现）。
    dominant = []
    for line in order[1:]:
        cells = line.split("\t")
        counts = {
            "full": int(cells[3]),
            "near": int(cells[4]),
            "unstable": int(cells[5]),
            "zero": int(cells[6]),
        }
        dominant.append(max(counts, key=lambda k: counts[k]))
    same_neighbour = sum(1 for a, b in zip(dominant, dominant[1:]) if a == b)
    assert same_neighbour < len(dominant) * 0.6, (
        f"{same_neighbour}/{len(dominant) - 1} adjacent pairs share a dominant pool; "
        "the interleave is not working"
    )
