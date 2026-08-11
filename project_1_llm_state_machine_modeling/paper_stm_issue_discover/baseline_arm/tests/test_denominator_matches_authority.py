"""⭐ 分母的**权威一致性**：X1 自己算的 98 条必须与 `metrics_at_k.REPORTABLE` 逐条相等。

## 为什么需要这条测试

隔离要求 X1 ⛔ 不 import 主臂侧模块，于是 `present.py` / `verdicts.py` 各自实现了一份「台账 −
`00x8` − 逐条边界裁定」的筛选。⚠️ **那是第二真源**：两份实现会漂移，而漂移的后果是**两臂分母
不同却看不出来** —— 正是仓库根 `CLAUDE.md` §3.5 条款 4「评测口径迁就结果」的形状，即便它是无意的。

⭐ 解法不是删掉一份（隔离面不能破），而是让漂移**在测试里炸**：用 subprocess 调权威实现取真值，
逐条比对。⛔ 不比数量，比**集合**——数量相等而成员不同是最恶劣的一种漂移。

## 为什么用 subprocess

`metrics_at_k` 在 `discover_matrix/` 下，import 它不违反隔离（隔离只禁 `paper_stm_feedback_loop`
与 `pyfcstm`）。⭐ 但用 subprocess 仍然更好：它把权威口径当成**外部事实**取用，而不是把它编进
X1 的依赖面——后者会让「X1 依赖什么」这个问题的答案随时间变模糊。
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ARM = Path(__file__).resolve().parents[1]
PAPER = ARM.parent
REPO_ROOT = ARM.parents[3]
MATRIX = PAPER / "discover_matrix"

sys.path.insert(0, str(ARM / "src"))

import present  # noqa: E402
import verdicts  # noqa: E402


def _authoritative_reportable() -> tuple[str, ...]:
    """从 `metrics_at_k.REPORTABLE` 取权威分母。"""

    program = (
        "import sys, json\n"
        f"sys.path.insert(0, {str(MATRIX)!r})\n"
        "import metrics_at_k as m\n"
        "print('REPORTABLE=' + json.dumps(list(m.REPORTABLE)))\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", program],
        capture_output=True,
        text=True,
        timeout=180,
        cwd=str(PAPER),
    )
    assert result.returncode == 0, (
        f"could not read the authoritative denominator:\n{result.stderr[-2000:]}"
    )
    line = [ln for ln in result.stdout.splitlines() if ln.startswith("REPORTABLE=")]
    assert line, f"probe produced nothing:\n{result.stdout}\n{result.stderr}"
    return tuple(json.loads(line[-1].removeprefix("REPORTABLE=")))


def test_present_denominator_equals_authority() -> None:
    authority = set(_authoritative_reportable())
    mine = {r["id"] for r in present.load_reportable()}
    assert mine == authority, (
        "present.load_reportable() drifted from metrics_at_k.REPORTABLE.\n"
        f"only in X1: {sorted(mine - authority)}\n"
        f"only in authority: {sorted(authority - mine)}"
    )


def test_verdicts_denominator_equals_authority() -> None:
    authority = set(_authoritative_reportable())
    mine = {r["id"] for r in verdicts.reportable_records()}
    assert mine == authority, (
        "verdicts.reportable_records() drifted from metrics_at_k.REPORTABLE.\n"
        f"only in X1: {sorted(mine - authority)}\n"
        f"only in authority: {sorted(authority - mine)}"
    )


def test_denominator_is_98_and_excludes_the_two_known_sources() -> None:
    """⚠️ 两个排除来源的**合法性相反**，⛔ 不可混谈（`nl_scope_rule.md`）。"""

    ids = {r["id"] for r in verdicts.reportable_records()}
    assert len(ids) == 98
    # 来源一：`00x8` 家族（范围先验，判据只读 nl.txt）
    assert not [i for i in ids if i.split("-")[1] in verdicts.OUT_OF_SCOPE_PAIRS]
    # 来源二：逐条边界裁定
    assert "EIS-0043-02" not in ids
    # ⭐ 但 EIS-0043-01 必须在——排除是逐条的，⛔ 不是整个 pair
    assert "EIS-0043-01" in ids


def test_position_keys_are_588_and_wellformed() -> None:
    keys = verdicts.expected_keys()
    assert len(keys) == 588
    assert len(set(keys)) == 588, "duplicate position keys"
    for key in keys:
        assert verdicts._KEY.match(key), f"malformed key {key!r}"


def test_equivalence_forms_match_the_protocol_closed_set() -> None:
    """⭐ 闭集必须与 `hit_criterion.md` §3 的四形态逐字一致。

    ⚠️ 主臂的实现也钉着同一个闭集；两处若漂移，两臂的判定就不同口径了。
    """

    protocol = (MATRIX / "docs" / "protocol" / "hit_criterion.md").read_text(encoding="utf-8")
    for form in verdicts.EQUIVALENCE_FORMS:
        assert f"**{form}**" in protocol, (
            f"form {form!r} is not declared in hit_criterion.md §3 -- the closed set drifted"
        )
    assert len(verdicts.EQUIVALENCE_FORMS) == 4
    assert set(verdicts.FORM_TO_DIRECTION) == set(verdicts.EQUIVALENCE_FORMS)


# --------------------------------------------------------------- C 层闸


def test_gate_rejects_missing_positions() -> None:
    table = {"verdicts": {verdicts.expected_keys()[0]: {"hit": False}}}
    problems = verdicts.validate(table)
    assert any("该位缺失" in p for p in problems)
    assert len(problems) >= 587


def test_gate_rejects_unjudged_null_entry() -> None:
    table = {"verdicts": {key: {"hit": False} for key in verdicts.expected_keys()}}
    key = verdicts.expected_keys()[3]
    table["verdicts"][key] = None
    problems = verdicts.validate(table)
    assert [p for p in problems if key in p and "未判" in p]


def test_gate_rejects_hit_without_form_or_short_argument() -> None:
    keys = verdicts.expected_keys()
    table = {"verdicts": {key: {"hit": False} for key in keys}}
    table["verdicts"][keys[0]] = {"hit": True, "equivalence_form": "谁知道", "argument": "x" * 40}
    table["verdicts"][keys[1]] = {"hit": True, "equivalence_form": "直接对应", "argument": "太短"}
    problems = verdicts.validate(table)
    assert [p for p in problems if keys[0] in p and "闭集" in p]
    assert [p for p in problems if keys[1] in p and "过短" in p]


def test_gate_accepts_a_complete_table() -> None:
    table = {
        "verdicts": {
            key: {"hit": False, "argument": "该格未报出指向同一处失误的主张。"}
            for key in verdicts.expected_keys()
        }
    }
    assert verdicts.validate(table) == []


def test_gate_requires_a_reason_when_hit_is_null() -> None:
    """⭐ `hit=null` 合法（格失败/未落盘），⛔ 但必须写明——否则与漏判不可区分。"""

    keys = verdicts.expected_keys()
    table = {"verdicts": {key: {"hit": False} for key in keys}}
    table["verdicts"][keys[0]] = {"hit": None}
    problems = verdicts.validate(table)
    assert [p for p in problems if keys[0] in p and "没写理由" in p]


# --------------------------------------------------------------- 格式转换


def test_null_is_not_zero_in_the_converted_table() -> None:
    """⚠️ 把 null 读成 0 会让分母虚高而分子不变，即无声压低命中率。"""

    keys = verdicts.expected_keys()
    table = {"verdicts": {key: {"hit": False, "argument": "未报。"} for key in keys}}
    target = keys[0]
    table["verdicts"][target] = {"hit": None, "argument": "该格 provider 侧失败，未落盘。"}
    converted = verdicts.to_format_b(table, generation="probe")
    record, _, cell = target.partition("|")
    arm = cell.rsplit("-", 1)[1]
    round_index = int(cell[3]) - 1
    assert converted["verdicts"][record][arm][round_index] is None
    # 其余位是 0，不是 None
    others = [v for i, v in enumerate(converted["verdicts"][record][arm]) if i != round_index]
    assert all(v == 0 for v in others)


def test_direction_is_mapped_to_the_english_enum() -> None:
    """⚠️ 格式 A 用中文形态、格式 B 的 `direction` 用英文枚举，⛔ 两套字面量不可混。"""

    keys = verdicts.expected_keys()
    table = {"verdicts": {key: {"hit": False, "argument": "未报。"} for key in keys}}
    target = keys[0]
    table["verdicts"][target] = {
        "hit": True,
        "equivalence_form": "蕴含更根本的原因",
        "argument": "模型根本没声明该变量，无变量则不可能有下降，故蕴含台账命题为假。",
    }
    converted = verdicts.to_format_b(table, generation="probe")
    record = target.split("|")[0]
    arm = target.rsplit("-", 1)[1]
    assert converted["verdicts"][record]["direction"][arm] == "implies"


def test_converted_table_covers_all_98_records() -> None:
    table = {
        "verdicts": {key: {"hit": False, "argument": "未报。"} for key in verdicts.expected_keys()}
    }
    converted = verdicts.to_format_b(table, generation="probe")
    assert len(converted["verdicts"]) == 98
    assert converted["rounds"] == 3
