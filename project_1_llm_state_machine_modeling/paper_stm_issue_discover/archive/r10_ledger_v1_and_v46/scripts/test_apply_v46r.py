"""整块替换必须真的是整块：不许留残、不许溢出、不许静默少写。

一次改 96 个判定位与六条簇，出错的方向恰好都是难以事后察觉的：
少删一条旧记录，结果里就同时存在新旧两份；多删一条，分母就悄悄变小。
所以四件事各锁一条测试。
"""

from __future__ import annotations

import json
import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import apply_v46r as A  # noqa: E402


@pytest.fixture()
def wired(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch):
    verdicts = tmp_path / "v46" / "unexpected_verdicts"
    verdicts.mkdir(parents=True)
    (verdicts / "G1.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in [
        {"cluster": "0000-1", "verdict": "REPRESENTATION_DEBT"},   # 在替换范围内
        {"cluster": "0029-1", "verdict": "NO_NL_BASIS"},           # 不在
    ]))
    tiers = tmp_path / "v46" / "verdicts" / "v46_tiers.json"
    tiers.parent.mkdir(parents=True)
    tiers.write_text(json.dumps({"rounds": ["run1", "run2", "run3"], "verdicts": {
        "EIS-0000-01": {"claude": [1, 1, 1], "gpt": [1, 1, 1]},
        "EIS-0029-01": {"claude": [0, 0, 0], "gpt": [1, 0, 0]},
    }}, ensure_ascii=False))
    human = tmp_path / "v46" / "verdicts" / "v46_human.json"
    human.write_text(json.dumps({
        "EIS-0000-01|run1/0000-gpt": {"hit": True, "argument": "旧"},
        "EIS-0029-01|run1/0029-gpt": {"hit": True, "argument": "留着"},
    }, ensure_ascii=False))

    monkeypatch.setattr(A, "TIERS", tiers)
    monkeypatch.setattr(A, "HUMAN", human)
    monkeypatch.setattr(A, "VERDICTS", verdicts)
    monkeypatch.setattr(A, "metrics", lambda v: {k: (1, 2) for k in ("hit@1", "hit@3", "hit@all")})
    return tmp_path


def _inputs(tmp: pathlib.Path, *, tiers: dict, human: dict, clusters: list[dict]):
    t = tmp / "t.json"; t.write_text(json.dumps(tiers, ensure_ascii=False))
    h = tmp / "h.json"; h.write_text(json.dumps(human, ensure_ascii=False))
    c = tmp / "c.jsonl"
    c.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in clusters))
    return ["--tiers", str(t), "--human", str(h), "--clusters", str(c)]


def test_in_scope_records_are_replaced_wholesale(wired: pathlib.Path) -> None:
    """旧的整条消失，新的整条到位，范围外的一个字节不动。"""

    argv = _inputs(wired,
                   tiers={"EIS-0000-01": {"claude": [0, 0, 0], "gpt": [0, 1, 0]}},
                   human={"EIS-0000-01|run1/0000-gpt": {"hit": False, "argument": "新"}},
                   clusters=[{"cluster": "0000-1", "verdict": "NO_NL_BASIS"}])
    assert A.main(argv) == 0

    v = json.loads(A.TIERS.read_text())["verdicts"]
    assert v["EIS-0000-01"] == {"claude": [0, 0, 0], "gpt": [0, 1, 0]}
    assert v["EIS-0029-01"] == {"claude": [0, 0, 0], "gpt": [1, 0, 0]}, "范围外被改了"

    h = json.loads(A.HUMAN.read_text())
    assert h["EIS-0000-01|run1/0000-gpt"]["argument"] == "新"
    assert h["EIS-0029-01|run1/0029-gpt"]["argument"] == "留着"

    kept = [json.loads(x) for x in (A.VERDICTS / "G1.jsonl").read_text().splitlines() if x.strip()]
    assert [k["cluster"] for k in kept] == ["0029-1"], "范围内的旧簇没删干净"
    fresh = [json.loads(x) for x in (A.VERDICTS / "G9.jsonl").read_text().splitlines() if x.strip()]
    assert [k["cluster"] for k in fresh] == ["0000-1"]


def test_a_missing_in_scope_record_is_refused(wired: pathlib.Path) -> None:
    """范围内的记录 v46r 没给，就是更改分母，不许静默留空。"""

    argv = _inputs(wired, tiers={}, human={}, clusters=[])
    with pytest.raises(SystemExit, match="更改分母"):
        A.main(argv)


def test_out_of_scope_input_is_refused(wired: pathlib.Path) -> None:
    """v46r 不该带回范围外的记录——带回了说明跑错了格集。"""

    argv = _inputs(wired,
                   tiers={"EIS-0000-01": {"claude": [0, 0, 0], "gpt": [0, 0, 0]},
                          "EIS-0029-01": {"claude": [1, 1, 1], "gpt": [1, 1, 1]}},
                   human={}, clusters=[])
    with pytest.raises(SystemExit, match="不属于这六个 pair"):
        A.main(argv)


def test_dry_run_writes_nothing(wired: pathlib.Path) -> None:
    before = A.TIERS.read_text()
    argv = _inputs(wired,
                   tiers={"EIS-0000-01": {"claude": [0, 0, 0], "gpt": [0, 0, 0]}},
                   human={}, clusters=[])
    assert A.main(argv + ["--dry-run"]) == 0
    assert A.TIERS.read_text() == before
    assert not (A.VERDICTS / "G9.jsonl").exists()
