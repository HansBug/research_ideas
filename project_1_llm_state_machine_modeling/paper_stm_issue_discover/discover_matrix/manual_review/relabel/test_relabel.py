"""重标工作区的回归测试。

钉住四件**出错就会静默毁掉这轮人工工作**的事：

1. ⛔ 生成器不许改台账。
2. ⛔ `00x8` 越界 pair 不许有工作单。
3. ⭐ 生成器幂等，且重跑**不吃掉**人工填写的内容。
4. ⭐ 每份工作单自包含 —— 台账里该 pair 的每一条都有裁决区。

跑法：`python3 -m pytest test_relabel.py -q`（在本目录下）。
"""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import collect as C            # noqa: E402
import fillblocks as fb        # noqa: E402
import sources as S            # noqa: E402
from pumlmodel import PumlModel  # noqa: E402


def _sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def test_generator_does_not_touch_the_ledger():
    """⛔ 台账冻结。它是 v46 与 X1 两轮判定的比对对象，改它比改结果更严重。"""
    ledger = os.path.join(S.MANUAL_REVIEW, "expected_issue_set.json")
    before = _sha(ledger)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([sys.executable, os.path.join(HERE, "generate.py"),
                        "--pairs", "0000", "--out", tmp],
                       check=True, capture_output=True)
    assert _sha(ledger) == before


def test_out_of_scope_pairs_get_no_worksheet():
    """⛔ `00x8` 不进网格也不进分母 —— 给它们做工作单等于把分母改错。"""
    for pair in S.OUT_OF_SCOPE_PAIRS:
        assert not os.path.exists(os.path.join(HERE, f"{pair}.md")), \
            f"{pair} 是越界 pair，不该有工作单"
    assert len(S.IN_SCOPE_PAIRS) == 54
    assert set(S.OUT_OF_SCOPE_PAIRS) == {"0008", "0018", "0028", "0038", "0048", "0058"}


def test_every_in_scope_pair_has_a_worksheet():
    for pair in S.IN_SCOPE_PAIRS:
        assert os.path.exists(os.path.join(HERE, f"{pair}.md")), \
            f"{pair} 缺工作单 —— 跑 generate.py"


@pytest.mark.parametrize("pair", ["0000", "0010", "0029", "0044", "0059"])
def test_worksheet_covers_every_ledger_record_of_that_pair(pair):
    """⭐ 自包含：该 pair 的每一条台账记录都要有裁决区，否则会被静默漏判。"""
    with open(os.path.join(HERE, f"{pair}.md"), encoding="utf-8") as fh:
        text = fh.read()
    blocks = fb.extract(text)
    for rec in S.ledger_records(pair):
        assert rec["id"] in blocks, f"{pair} 缺 {rec['id']} 的裁决区"


def test_generate_is_idempotent_and_preserves_human_input():
    """⭐ 重跑生成器不许吃掉人工填写 —— 这条塌了整轮工作就没了。"""
    pair = "0000"
    src = os.path.join(HERE, f"{pair}.md")
    with tempfile.TemporaryDirectory() as tmp:
        dst = os.path.join(tmp, f"{pair}.md")
        shutil.copy(src, dst)
        with open(dst, encoding="utf-8") as fh:
            text = fh.read()
        marker = "理由: 这是人工写的理由，重跑必须留住"
        text = text.replace("裁决: [ ] 保留  [ ] 修正",
                            "裁决: [x] 保留  [ ] 修正", 1)
        text = text.replace("理由:\n修正后的 statement:",
                            f"{marker}\n修正后的 statement:", 1)
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(text)

        for _ in range(2):
            subprocess.run([sys.executable, os.path.join(HERE, "generate.py"),
                            "--pairs", pair, "--out", tmp],
                           check=True, capture_output=True)
        with open(dst, encoding="utf-8") as fh:
            after = fh.read()
        assert marker in after
        assert "[x] 保留" in after

        # 第三次不该再产生任何改动
        before = _sha(dst)
        subprocess.run([sys.executable, os.path.join(HERE, "generate.py"),
                        "--pairs", pair, "--out", tmp],
                       check=True, capture_output=True)
        assert _sha(dst) == before

        parsed = C.collect_pair(pair, dst)
        rec = next(r for r in parsed["ledger"] if r["id"] == "EIS-0000-01")
        assert rec["裁决"]["chosen"] == ["保留"]
        assert "重跑必须留住" in rec["理由"]


@pytest.mark.parametrize("seed", ["0", "1", "12345"])
def test_generation_is_deterministic_across_hash_seeds(seed):
    """⛔ 生成结果不许随 `PYTHONHASHSEED` 变。

    ⚠️ 这条是实测出来的：`regroup_unmatched` 原本用 `frozenset` 当分组键，而
    `str(frozenset)` 的元素顺序随 hash seed 变 —— 54 份里有 16 份每跑一次行序就变一次，
    于是每次重跑都是一个假 diff，人工填写与材料更新混在一起无法分辨。
    """
    env = dict(os.environ, PYTHONHASHSEED=seed)
    proc = subprocess.run([sys.executable, os.path.join(HERE, "generate.py"), "--check"],
                          check=True, capture_output=True, text=True, env=env)
    assert '"would_write": 0' in proc.stdout, proc.stdout


def test_orphan_blocks_are_kept_not_dropped():
    """⚠️ 材料变动导致 key 消失时，人工内容必须搬进 §9，⛔ 不许静默丢。"""
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "0000.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(fb.render("EIS-9999-99", "ledger", "理由: 不该丢的内容"))
        subprocess.run([sys.executable, os.path.join(HERE, "generate.py"),
                        "--pairs", "0000", "--out", tmp],
                       check=True, capture_output=True)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        assert "不该丢的内容" in text
        assert "孤儿填写区" in text


def test_puml_parser_reads_every_pair_without_leftovers():
    """解析器必须吃下全部 60 份作者源 —— 漏行会让 §4 清单静默少条目。"""
    for pair in S.ALL_PAIRS:
        model = PumlModel(S.puml_text(pair), pair)
        assert not model.unparsed_lines, f"{pair} 有未解析行：{model.unparsed_lines[:3]}"
        assert not model.parse_warnings, f"{pair} 解析告警：{model.parse_warnings}"
        assert model.states, f"{pair} 解析出 0 个状态"


def test_parser_reads_author_source_not_the_projection():
    """⛔ 结构摘要必须锚在作者源 —— 投影合成的占位符不许出现在里面。"""
    synthetic = re.compile(r"UnspecifiedInitial|InvalidInitial|FinalWait|R45RouteToken")
    for pair in S.IN_SCOPE_PAIRS:
        model = PumlModel(S.puml_text(pair), pair)
        for name in model.states:
            assert not synthetic.search(name), \
                f"{pair} 的解析结果里出现了投影合成元素 {name} —— 读错了源"


def test_ledger_reportable_denominator_is_98():
    """⛔ 分母口径钉死：126 − 27（`00x8`）− 1（`EIS-0043-02` 逐条边界裁定）= 98。

    两种剔除来源不同，⛔ 不可混谈：前者是 NL 层的建模对象筛选，后者是逐条裁定。
    """
    all_recs = S.ledger()["records"]
    assert len(all_recs) == 126
    minus_scope = [r for r in all_recs if r["pair"] not in S.OUT_OF_SCOPE_PAIRS]
    assert len(minus_scope) == 99
    assert len(S.ledger_records(reportable_only=True)) == 98


def test_checklist_never_asks_about_clocks_or_concurrency():
    """⛔ 清单不许把建模对象之外的东西写成待查项（$M$ 无 $C$、无 $Inv$、无正交区）。

    ⚠️ 判据不是「不许出现这些词」—— 时序类检查项**必须**出现「⛔ 不是要求建时钟」
    这句免责，否则作者会误以为该记时间约束。所以判据是：出现越界词的条目，同一条里
    必须带一个显式否定。
    """
    import checklist as CK
    banned = re.compile(r"时钟|计时器|不变式|正交区|并发")
    negation = re.compile(r"⛔ 注意不是要求|⛔ 不|不是要求|不需要建|不在范围")
    for pair in S.IN_SCOPE_PAIRS:
        model = PumlModel(S.puml_text(pair), pair)
        segs, _ = S.nl_segments(pair)
        for _, note, items in CK.build(model, segs, S.ledger_records(pair), pair):
            for it in items:
                if banned.search(it.text):
                    assert negation.search(it.text), \
                        f"{pair} {it.iid} 提到越界概念却没写免责：{it.text[:120]}"


def test_no_hard_wrapping_inside_paragraphs():
    """⛔ Markdown 自然段内不许硬折行（仓库硬规矩）。

    ⚠️ 这条也是实测出来的：`source_meta.json` 的 `model_name` 字段里带真实换行，
    直接插进段落会让 6 份工作单的第一段被折断 —— CommonMark 把软换行渲染成一个空格，
    中文段落于是多出一个空格。
    """
    repo = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.dirname(HERE)))))
    targets = [os.path.join(HERE, f) for f in sorted(os.listdir(HERE))
               if f.endswith(".md")]
    proc = subprocess.run(
        [sys.executable, "-m", "tools.unwrap_markdown", "--check", *targets],
        cwd=repo, capture_output=True, text=True)
    if proc.returncode == 1 and "No module named" in proc.stderr:
        pytest.skip("tools.unwrap_markdown 不可用")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_worksheets_carry_no_verdicts():
    """⛔ 材料不许替作者裁决 —— 裁决区必须是空模板。"""
    for pair in S.IN_SCOPE_PAIRS:
        data = C.collect_pair(pair, os.path.join(HERE, f"{pair}.md"))
        for rec in data["ledger"]:
            assert not rec.get("裁决", {}).get("chosen"), f"{pair} {rec['id']} 已被预填裁决"
        for cand in data["candidates"]:
            assert not cand.get("裁决", {}).get("chosen"), f"{pair} {cand['key']} 已被预填裁决"
        for chk in data["checklist"]:
            for it in chk["items"]:
                assert not it["checked"], f"{pair} {it['iid']} 已被预勾选"
                assert not it["finding"], f"{pair} {it['iid']} 已被预填发现"
        assert not data["new_issues"], f"{pair} 的 §5 被预填了新增条目"
