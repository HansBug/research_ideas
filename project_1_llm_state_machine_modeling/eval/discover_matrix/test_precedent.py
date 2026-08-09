"""判例索引只许呈现历史，不许参与判断，且不许把「读不到」伪装成「没判过」。

三件事各对应一条真实教训：

1. **判例缺失必须响。** 判例少一代与判例为空长得一样，而前者只是文件不在本机，
   后者意味着这条记录从没判过 —— 两者对判定者的意义完全相反。
2. **不给建议。** 机械代理只能定位不能裁定（本目录实证：v20run1 有两条产出触及了正确
   元素却得出与台账相反的结论，任何字面相似度打分都会把它们判成命中）。
3. **判例是参考不是先例约束。** 输出必须自己说这句话，否则读者会把「历代都命中」
   读成「本代也该判命中」。
"""

from __future__ import annotations

import json
import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import precedent as P  # noqa: E402


@pytest.fixture()
def sources(tmp_path: pathlib.Path) -> tuple[tuple[str, str], ...]:
    a = tmp_path / "a.json"
    a.write_text(json.dumps({
        "EIS-0040-01|run1/0040-claude": {"hit": True, "equivalence_form": "直接对应",
                                         "argument": "issue 点名了 Power_Off 不终止"},
        "EIS-0040-01|run1/0040-gpt": {"hit": False},
        "EIS-0039-01|run1/0039-claude": {"hit": False},
    }, ensure_ascii=False))
    b = tmp_path / "b.json"
    b.write_text(json.dumps({
        "EIS-0040-01|run2/0040-claude": {"hit": True, "equivalence_form": "蕴含更根本的原因",
                                         "argument": "不被消费是不终止的成因"},
    }, ensure_ascii=False))
    return (("gA", str(a)), ("gB", str(b)), ("gMissing", str(tmp_path / "nope.json")))


def test_it_aggregates_across_generations(sources) -> None:
    index = P.load(sources)
    entries = index["EIS-0040-01"]
    assert len(entries) == 3
    stats = P.summarise(entries)
    assert stats["by_generation"] == {"gA": (1, 2), "gB": (1, 1)}
    assert stats["forms"] == {"直接对应": 1, "蕴含更根本的原因": 1}
    assert len(stats["arguments"]) == 2


def test_a_missing_source_is_reported_not_swallowed(sources) -> None:
    """读不到的代次必须记名 —— 否则判例不完整会被当成判例为空。"""

    index = P.load(sources)
    assert "__missing__" in index
    assert index["__missing__"][0]["generation"] == "gMissing"


def test_a_record_never_judged_is_distinguishable_from_all_miss(sources) -> None:
    index = P.load(sources)
    assert "EIS-9999-01" not in index          # 从没判过
    assert index["EIS-0039-01"][0]["hit"] is False  # 判过，判的是未命中


def test_the_output_never_recommends_a_verdict(sources) -> None:
    """呈现历史即可；出现任何形式的建议措辞都是越界。"""

    text = P.render("EIS-0040-01", P.load(sources)["EIS-0040-01"])
    for banned in ("建议", "应判", "推荐", "疑似命中", "likely", "suggest"):
        assert banned not in text, f"输出里出现了越界措辞：{banned}"


def test_the_summary_states_that_precedent_is_not_binding(
    sources, capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(P, "DEFAULT_SOURCES", sources)
    P.main(["--all"])
    out = capsys.readouterr().out
    assert "判例是参考不是先例约束" in out
