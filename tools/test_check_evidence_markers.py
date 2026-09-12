"""`check_evidence_markers` 的回归测试。

这个工具存在的理由：`story/README.md` §2 声明六档标记「全目录通用」，而实测里
``【】`` 长出了约 60 种变体、其中 82 处落在六档作用域内。⛔ 后果不是不整齐，是
**读者无法再从形态上判断依据强度**——而约束它们的声明写在文件抬头，离使用处
七十多行远。⚠️ 那种远距离约束已经失效过一次：``【用户明确…】`` 被误用成引语标记
8 处,使「引用了多少条用户原话」这个数虚报近一倍。

测试的两个重点，缺一不可：
1. **真违规必须报**——四类形态（六档带后缀 / 组合档 / 非六档 / 空标记）各有改法；
2. **讲规则的地方不许报**——代码块与行内代码里的 ``【】`` 是在举例说明规则本身，
   ⛔ 报它们等于让工具与它要保护的文档打架。实测：本工具刚上线时就把
   `README.md` 里那张「⛔ 禁止写法 / ⭐ 正确写法」对照表整行报了出来。
"""

from __future__ import annotations

import pathlib

from tools.check_evidence_markers import SIX, classify, scan


def _w(tmp: pathlib.Path, rel: str, body: str) -> None:
    p = tmp / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")


def test_all_six_tiers_are_clean() -> None:
    for tier in SIX:
        assert classify(tier) is None, tier


def test_dated_six_tier_gets_the_parenthesis_fix() -> None:
    """最常见的违规：六档后面直接跟日期。"""
    v = classify("仓库裁定 2026-08-11")
    assert v is not None and v[0] == "六档带后缀"
    assert v[1] == "【仓库裁定】（2026-08-11）"


def test_combo_tier_is_split_and_ordered() -> None:
    """组合档实测出现过两种相反顺序，故建议改法必须给出固定顺序。"""
    a = classify("v46 实测 + 仓库裁定")
    b = classify("仓库裁定 + v46 实测")
    assert a is not None and b is not None
    assert a[1] == b[1] == "【v46 实测】【仓库裁定】"


def test_non_tier_marker_is_moved_to_the_other_bracket() -> None:
    v = classify("用户明确裁定 2026-08-11")
    assert v is not None and v[0] == "非六档"
    assert v[1] == "〔用户明确裁定 2026-08-11〕"


def test_empty_marker_is_reported() -> None:
    v = classify("")
    assert v is not None and v[1] == "删除"


def test_combo_containing_a_non_tier_is_not_silently_accepted() -> None:
    v = classify("v46 实测 + 用户明确裁定")
    assert v is not None and "非六档" in v[0]


def test_fenced_code_block_is_skipped(tmp_path: pathlib.Path) -> None:
    """⛔ 代码块里的 `【】` 是在讲规则本身，不是在标注依据。"""
    _w(tmp_path, "TODO.md", "```\n【用户明确裁定 2026-08-11】\n```\n")
    assert scan(tmp_path) == []


def test_inline_code_is_skipped(tmp_path: pathlib.Path) -> None:
    """⭐ 这是本工具上线时真实误报过的一类：README 的对照表整行被报出来。

    那张表逐字写着「⛔ 禁止写法 `【仓库裁定 2026-08-11】` / ⭐ 正确写法 …」——
    ⛔ 报它等于让工具与它要保护的文档打架。
    """
    _w(tmp_path, "TODO.md", "禁止 `【仓库裁定 2026-08-11】`，改用 `【仓库裁定】（2026-08-11）`\n")
    assert scan(tmp_path) == []


def test_real_violation_outside_code_is_reported(tmp_path: pathlib.Path) -> None:
    _w(tmp_path, "TODO.md", "这条是 【用户明确裁定】 定的。\n")
    bad = scan(tmp_path)
    assert len(bad) == 1
    assert bad[0][0] == "TODO.md" and bad[0][1] == 1 and bad[0][3] == "非六档"


def test_out_of_scope_file_is_not_scanned(tmp_path: pathlib.Path) -> None:
    """⚠️ `claim_evidence_map.md` 自带八档强度表（【推论】等），不在作用域内。"""
    _w(tmp_path, "story/claim_evidence_map.md", "强度 【推论】\n")
    assert scan(tmp_path) == []


def test_reported_line_number_is_correct(tmp_path: pathlib.Path) -> None:
    _w(tmp_path, "GUIDE.md", "第一行\n\n【用户明确澄清】\n")
    assert [b[1] for b in scan(tmp_path)] == [3]


def test_multiple_markers_on_one_line(tmp_path: pathlib.Path) -> None:
    _w(tmp_path, "STATUS.md", "【v46 实测】合规，【用户明确裁定】不合规\n")
    bad = scan(tmp_path)
    assert len(bad) == 1 and bad[0][2] == "用户明确裁定"


def test_the_real_regression_shape(tmp_path: pathlib.Path) -> None:
    """复现真实现场：同一文件里四类违规并存，且六档正常项不受影响。"""
    _w(
        tmp_path,
        "PENDING_DECISIONS.md",
        "\n".join(
            [
                "【导师原话】这句没问题。",
                "【仓库裁定 2026-08-11】带了日期。",
                "【v46 实测 + 仓库裁定】组合档。",
                "【我方提出 · 导师未反对】非六档。",
                "【】空的。",
            ]
        )
        + "\n",
    )
    # ⛔ 用集合比,不用 sorted —— 中文的码点序不直观,写死顺序只会让断言脆。
    assert {b[3] for b in scan(tmp_path)} == {"六档带后缀", "组合档", "非六档", "空标记"}
    # 六档正常项不受影响：5 行里只有 4 行违规。
    assert len(scan(tmp_path)) == 4
