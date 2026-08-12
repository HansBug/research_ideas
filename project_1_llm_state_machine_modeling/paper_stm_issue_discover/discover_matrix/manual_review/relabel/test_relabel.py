"""重标工作区的回归测试。

钉住七件**出错就会静默毁掉这轮人工工作**的事：

1. ⛔ 生成器不许改台账。
2. ⛔ `00x8` 越界 pair 不许有工作单。
3. ⭐ 生成器幂等，且重跑**不吃掉**人工填写的内容。
4. ⭐ 每份工作单自包含 —— 台账里该 pair 的每一条都有裁决区。
5. ⭐ §1.2 的 NL 表是三列，且**每一段都真有中文译文**（⛔ 不许留 TODO 占位）。
6. ⭐ §5 的新增字段块能被 `collect.py` 完整解析回来（⛔ 含带冒号的多行 statement）。
7. ⭐ 三条校验（边界 / 去重 / 完整性）各有正反用例 —— ⛔ 只测「能报错」不算，
   还得测「不该报的时候不报」，否则一条恒报的规则也能通过测试。

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
import newfields as NF         # noqa: E402
import nl_zh                   # noqa: E402
import sources as S            # noqa: E402
import validate as V           # noqa: E402
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


# ==================================================================== §1.2 三列 NL 表

def test_nl_table_has_three_columns_in_every_worksheet():
    """⭐ §1.2 必须是「段 id / 原文 / 中文严格翻译」三列，且逐段都有译文。

    ⛔ 判据不是「表头有三列」—— 表头对了而行只有两列，Markdown 照样渲染，
    只是最后一列空着，⚠️ 人读起来像「这段没译」。所以逐行数分隔符。
    """
    for pair in S.IN_SCOPE_PAIRS:
        with open(os.path.join(HERE, f"{pair}.md"), encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        head = next(i for i, ln in enumerate(lines)
                    if ln.startswith("| 段 id |"))
        assert lines[head] == "| 段 id | 原文 | 中文严格翻译 |", \
            f"{pair} 的 §1.2 表头不是三列：{lines[head]}"
        segs, _ = S.nl_segments(pair)
        rows = lines[head + 2: head + 2 + len(segs)]
        assert len(rows) == len(segs), f"{pair} 的 §1.2 行数与分段数不符"
        for (sid, _txt), row in zip(segs, rows):
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            assert len(cells) == 3, f"{pair} {sid} 不是三列：{row[:120]}"
            assert cells[0] == f"`{sid}`"
            assert cells[1], f"{pair} {sid} 原文列为空"
            assert cells[2], f"{pair} {sid} 译文列为空"
            assert "缺译文" not in cells[2], f"{pair} {sid} 缺译文"


def test_every_nl_segment_has_a_chinese_translation():
    """⛔ 54 份工作单覆盖的每一段 NL 都必须有译文，⛔ 一段都不许缺。

    ⚠️ 译文按 **NL 全文 digest** 索引，所以 `nl.txt` 改一个字节就会查不到 ——
    ⭐ 那正是本测试要抓的：材料变了而译文没跟上，⛔ 不许静默沿用旧译。
    """
    assert nl_zh.missing() == []


def test_no_stale_translations_left_behind():
    """⚠️ 反向：译文表里不许留下已经对不上任何在评 pair 的孤儿键。"""
    used = set()
    for pair in S.IN_SCOPE_PAIRS:
        d = nl_zh.digest(pair)
        for sid, _ in S.nl_segments(pair)[0]:
            used.add((d, sid))
    orphan = [(d, s) for d, segs in nl_zh.TRANSLATIONS.items()
              for s in segs if (d, s) not in used]
    assert orphan == [], f"译文表里有孤儿键：{orphan}"


def test_translations_do_not_break_the_markdown_table():
    """⛔ 译文里不许出现未转义的 `|` 或换行 —— 会把三列表格撕开。"""
    for digest, segs in nl_zh.TRANSLATIONS.items():
        for sid, zh in segs.items():
            assert "|" not in zh, f"{digest} {sid} 译文含 `|`"
            assert "\n" not in zh, f"{digest} {sid} 译文含换行"


def test_out_of_scope_nl_group_has_no_translation():
    """⛔ `00x8` 组不生成工作单，故译文表**不该**收它 —— 收了就说明有人想给它做工作单。"""
    d = nl_zh.digest("0008")
    assert d not in nl_zh.TRANSLATIONS


def test_translation_keeps_state_names_in_english():
    """⭐ 状态名 / 变量名一律保留英文原样 —— 抽查两组里逐字出现的标识符。"""
    checks = {
        "b7425c44960b": ["AutonomousMode", "InitialState", "HighwayMode", "UrbanMode",
                         "enter_hwy", "lane_change", "dist_to_front", "auto_finished",
                         "collision_avoidance_deactive"],
        "934e19bd4ae2": ["DoorShut", "DoorOpen", "DoorOpenWithItem",
                         "DoorShutWithItem", "ReadytoCook", "Cooking"],
    }
    for digest, names in checks.items():
        blob = " ".join(nl_zh.TRANSLATIONS[digest].values())
        for name in names:
            assert name in blob, f"{digest} 的译文里丢了标识符 {name}"


# ==================================================================== §5 字段块

def _entry(pair, idx=1, **over):
    """拼一条 §5 新增登记。⭐ 值为 `None` 表示那一行整个不写（模拟漏填）。"""
    fields = {
        "statement": "顶层没有任何进入 InitialState 的初始边，冷启动落点未定义。",
        "generated_side": ":2 [*] --> InitialState",
        "nl_evidence": "无",
        "direction": "entry",
        "depth": "中层",
    }
    fields.update(over)
    out = [f"### NEW-{pair}-{idx:02d}"]
    out += [f"{k}: {v}" for k, v in fields.items() if v is not None]
    return "\n".join(out)


def _validate_new(pair, *entries):
    """⭐ 走真实链路：`parse_new` 解析 → `validate_pair` 校验。返回 Report。

    ⛔ 固定用台账 0 条的 pair，否则「台账条目未裁决」的 E 会淹掉被测信号。
    """
    assert not S.ledger_records(pair), f"{pair} 有台账条目，不适合当本测试的载体"
    data = {
        "pair": pair,
        "summary": {"本 pair 整体判断": {"chosen": ["台账在本 pair 上够用"], "options": []}},
        "ledger": [], "candidates": [], "checklist": [],
        "new_issues": C.parse_new("\n\n".join(entries), pair),
        "orphans": {}, "untouched_keys": [],
    }
    rep = V.Report()
    V.validate_pair(pair, data, rep)
    return rep


def _msgs(rep, level=None):
    return [i["msg"] for i in rep.items if level is None or i["level"] == level]


def test_new_issue_field_block_round_trips_through_collect():
    """⭐ 人工填的 8 个字段必须能被 `collect.py` 原样收回来。"""
    body = _entry("0001", 1, primary_predicate="initial_target",
                  reference_side="参考侧有 [*] --> Init", layer="wellformedness")
    recs = C.parse_new(body, "0001")
    assert len(recs) == 1
    f = recs[0]["fields"]
    assert recs[0]["id"] == "NEW-0001-01"
    assert f["statement"].startswith("顶层没有任何")
    assert f["generated_side"] == ":2 [*] --> InitialState"
    assert f["nl_evidence"] == "无"
    assert f["direction"] == "entry"
    assert f["depth"] == "中层"
    assert f["primary_predicate"] == "initial_target"
    assert f["layer"] == "wellformedness"


def test_new_issue_block_parses_the_checkbox_form_from_the_real_template():
    """⭐ 模板给的是勾选行 —— 勾了 `[x]` 也要能收回来，⛔ 不能只支持自由文本。"""
    body = (NF.template("0001", count=1)
            .replace("statement:", "statement: BrakingState 的出边把两个事件并成一个名字")
            .replace("generated_side:", "generated_side: 第 8 行")
            .replace("nl_evidence:", "nl_evidence: NL-L003")
            .replace("[ ] guard ", "[x] guard ")
            .replace("[ ] 深层", "[x] 深层"))
    recs = C.parse_new(body, "0001")
    assert len(recs) == 1
    f = recs[0]["fields"]
    assert f["direction"]["chosen"] == ["guard"]
    assert f["depth"]["chosen"] == ["深层"]
    assert f["nl_evidence"] == "NL-L003"


def test_multiline_statement_with_colons_is_not_truncated():
    """⛔ 作者在 `statement` 里换行写「NL 第 3 句：…」不许把字段截断。

    ⚠️ 这是实测出来的坑：解析器原本把任何 `名字:` 开头的行都当新字段，
    于是 statement 被就地砍断而且**不报错** —— 人工写的判断静默丢一半。
    修法是只认 8 个已知字段名（`newfields.FIELD_NAMES`）。
    """
    body = "\n".join([
        "### NEW-0001-01",
        "statement: 第一行",
        "NL 第 3 句：After entering the braking state 明确要求后继状态",
        "结论: 该义务在模型上没有结构性承载",
        "generated_side: :8",
        "nl_evidence: NL-L003",
        "direction: hierarchy",
        "depth: 深层",
    ])
    f = C.parse_new(body, "0001")[0]["fields"]
    assert "NL 第 3 句" in f["statement"]
    assert "该义务在模型上没有结构性承载" in f["statement"]
    assert "NL 第 3 句" not in f
    assert "结论" not in f
    assert f["generated_side"] == ":8"


def test_derive_fills_element_of_M_from_the_author_source_line():
    """⭐ `element_of_M` 由脚本从作者源行号反查，⛔ 不由人工填。"""
    assert NF.derive_element_of_M("0001", ":5 InitialState --> BrakingState")[0] == "Tr"
    assert NF.derive_element_of_M("0001", "第 9 行")[0] == "A"
    assert NF.derive_element_of_M("0001", ":2, :5")[0] == "Tr"
    # ⛔ 没行号又没结构族谓词 → 推不出，必须显形为 None
    assert NF.derive_element_of_M("0001", "BrakingState 那条边")[0] is None
    # ⭐ 退路：结构族谓词的确定性映射
    assert NF.derive_element_of_M("0001", "BrakingState", "state_declared")[0] == "S"
    # ⛔ 行为族谓词不许当依据 —— 分量取决于主张本身
    assert NF.derive_element_of_M("0001", "BrakingState", "reaches")[0] is None


def test_derive_reports_the_fields_it_cannot_produce():
    """⛔「脚本推导」必须是一句可核对的话：算不出来的要列进 `pending`。"""
    d = NF.derive("0001", "NEW-0001-01",
                  {"generated_side": ":5", "primary_predicate": "edge_declared"})
    assert d["pair"] == "0001" and d["group"] == "NL02" and d["in_scope"] is True
    assert d["llm"] == S.source_meta("0001")["llm"]
    assert d["element_of_M"] == "Tr"
    assert d["expressible_with_closed_vocabulary"] is True
    for name in ("assertions", "replay", "verdict", "homogeneity_group"):
        assert name in d["pending"], f"{name} 既没算出来也没列进 pending"


def test_field_table_and_template_stay_in_sync():
    """⛔ 模板里出现的字段名必须与 `FIELD_NAMES` 完全一致 —— 两处走偏就收不回来。"""
    body = NF.template("0001", count=1)
    names = [ln.split(":", 1)[0] for ln in body.splitlines() if ":" in ln]
    assert names == NF.FIELD_NAMES
    assert NF.REQUIRED_FIELDS + NF.OPTIONAL_FIELDS == NF.FIELD_NAMES
    assert len(NF.REQUIRED_FIELDS) == 5 and len(NF.OPTIONAL_FIELDS) == 3


def test_every_exemplar_slot_resolves_off_group():
    """⛔ §5 的样例不许取自本 pair 所属的 NL 组 —— 兄弟 pair 共用 NL，那是泄题。"""
    for pair in S.IN_SCOPE_PAIRS:
        for slot in NF.EXEMPLARS:
            rec = NF.exemplar(slot, pair)
            assert rec is not None, f"{pair} 的 {slot} 挑不到样例"
            assert S.nl_group(rec["pair"]) != S.nl_group(pair), \
                f"{pair} 的 {slot} 样例 {rec['id']} 与本 pair 同属 {S.nl_group(pair)}"


def test_exemplars_are_real_ledger_records():
    """⛔ 样例必须逐字来自台账，⛔ 不许是编的。"""
    index = {r["id"]: r for r in S.ledger_records(reportable_only=True)}
    for slot, ids in NF.EXEMPLARS.items():
        for rid in ids:
            assert rid in index, f"{slot} 的样例 {rid} 不在台账 REPORTABLE 里"


def test_direction_enum_matches_what_the_ledger_actually_uses():
    """⛔ 枚举不许拍脑袋：8 个取值必须与台账 98 条实际用过的完全一致。

    ⚠️ 全 126 条里还有第 9 个 `pseudostate`，但它**全部落在 `00x8`** 上 ——
    那 6 个 pair 的 fork/join 不在 $M$ 内，所以本轮不设该取值。
    """
    used = {r["direction"] for r in S.ledger_records(reportable_only=True)}
    assert used == set(NF.DIRECTIONS)
    all_used = {r["direction"] for r in S.ledger()["records"]}
    assert all_used - used == {"pseudostate"}
    for r in S.ledger()["records"]:
        if r["direction"] == "pseudostate":
            assert r["pair"] in S.OUT_OF_SCOPE_PAIRS
    assert set(NF.LAYERS) == {r["layer"] for r in S.ledger_records(reportable_only=True)}


# ==================================================================== 三条校验

# ---- ①⛔ 边界门

def test_boundary_gate_flags_a_clock_claim():
    """⛔ 正例：主张需要时钟语义 → 必须提示越界。"""
    rep = _validate_new("0001", _entry(
        "0001", statement="Cooking 状态缺少 30 秒的计时器超时迁移，timer 到期后无出边。"))
    assert any("疑似越界" in m for m in _msgs(rep, "W"))


def test_boundary_gate_flags_a_concurrency_claim():
    rep = _validate_new("0001", _entry(
        "0001", statement="两个区域应当并发同时活跃，模型缺少 fork 伪状态。"))
    assert any("疑似越界" in m for m in _msgs(rep, "W"))


def test_boundary_gate_stays_quiet_on_an_in_scope_claim():
    """⛔ 反例：一条正常的层次缺陷不许被报越界 —— 恒报的门等于没有门。"""
    rep = _validate_new("0001", _entry("0001"))
    assert not any("疑似越界" in m for m in _msgs(rep))


def test_boundary_gate_does_not_scan_the_locator_field():
    """⭐ 反例：`generated_side` 引用一行叫 `Timer` 的状态**不**使主张越界。

    ⚠️ 判的是「这条主张需不需要时钟语义」，⛔ 不是「文本里有没有 timer 这个词」。
    ⛔ 若把定位串也扫进去，微波炉那一组（`0005` 系列）会被整组误报。
    """
    rep = _validate_new("0001", _entry(
        "0001", generated_side=":5 Timer --> Idle（该状态名恰好叫 Timer）"))
    assert not any("疑似越界" in m for m in _msgs(rep))


def test_boundary_gate_is_a_warning_not_a_hard_gate():
    """⛔ 边界判据是词法、会误伤，故只能是 `W`。⛔ 做成 `E` 会把正确答案挡在门外。"""
    rep = _validate_new("0001", _entry(
        "0001", statement="缺少 timer 到期后的出边。"))
    assert [i["level"] for i in rep.items if "疑似越界" in i["msg"]] == ["W"]


def test_out_of_scope_pair_worksheet_is_a_hard_error():
    """⛔ 这一条相反：`00x8` 出现工作单是确定性事实，必须报 `E`。"""
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, "0008.md"), "w", encoding="utf-8") as fh:
            fh.write("x")
        proc = subprocess.run(
            [sys.executable, os.path.join(HERE, "validate.py"),
             "--dir", tmp, "--pairs", "0001", "--json"],
            capture_output=True, text=True)
        assert '"level": "E"' in proc.stdout
        assert "越界 pair 不该有工作单" in proc.stdout


# ---- ②⛔ 重复检查

def test_dedup_flags_two_entries_on_the_same_source_line():
    rep = _validate_new(
        "0001",
        _entry("0001", 1, generated_side=":5 InitialState --> BrakingState"),
        _entry("0001", 2, statement="这条边的守卫条件完全缺失，两条出边无法区分。",
               generated_side=":5", direction="guard"))
    assert any("同一作者源行" in m for m in _msgs(rep, "W"))


def test_dedup_flags_same_direction_on_the_same_element():
    """⭐ 任务口径：同 pair + 同元素 + 同缺陷方向 → 提示可能重复。"""
    rep = _validate_new(
        "0001",
        _entry("0001", 1, statement="InitialState 没有任何初始边指向它。",
               generated_side="InitialState", direction="entry"),
        _entry("0001", 2, statement="进入 InitialState 的入口未定义。",
               generated_side="InitialState 元素", direction="entry"))
    assert any("是不是同一缺陷" in m for m in _msgs(rep, "W"))


def test_dedup_stays_quiet_on_two_genuinely_different_entries():
    """⛔ 反例：不同元素 + 不同方向的两条不许被判重复。"""
    rep = _validate_new(
        "0001",
        _entry("0001", 1, statement="InitialState 没有任何初始边指向它。",
               generated_side=":2", direction="entry"),
        _entry("0001", 2, statement="ClampingLoseState 是吸收态，进去以后再也出不来。",
               generated_side=":14", direction="reachability"))
    assert not any("是不是同一缺陷" in m for m in _msgs(rep, "W"))


def test_dedup_flags_overlap_with_an_existing_ledger_record():
    """⭐ 新增条目与本 pair 现有台账条目撞车时，应提示改走 §2 的「修正」。"""
    pair = "0004"
    rec = S.ledger_records(pair)[0]
    data = {
        "pair": pair, "summary": None,
        "ledger": [], "candidates": [], "checklist": [],
        "new_issues": C.parse_new(_entry(
            pair, 1, statement=rec["statement"][:200],
            generated_side="DoorsClosing", direction=rec["direction"]), pair),
        "orphans": {}, "untouched_keys": [],
    }
    rep = V.Report()
    V.validate_pair(pair, data, rep)
    assert any("疑似重复" in m and rec["id"] in m for m in _msgs(rep, "W"))


def test_dedup_is_a_warning_not_a_hard_gate():
    """⛔「是不是同一缺陷」是语义判断，⛔ 不能做成确定性门。"""
    rep = _validate_new(
        "0001",
        _entry("0001", 1, generated_side=":5"),
        _entry("0001", 2, generated_side=":5"))
    assert all(i["level"] == "W" for i in rep.items if "同一缺陷" in i["msg"])


# ---- ③⭐ 完整性

@pytest.mark.parametrize("field", ["statement", "generated_side", "nl_evidence"])
def test_completeness_flags_a_missing_required_text_field(field):
    rep = _validate_new("0001", _entry("0001", **{field: None}))
    assert any(f"必填项 `{field}` 为空" in m for m in _msgs(rep, "E"))


@pytest.mark.parametrize("field", ["direction", "depth"])
def test_completeness_flags_a_missing_required_enum_field(field):
    rep = _validate_new("0001", _entry("0001", **{field: None}))
    assert any(f"必填项 `{field}` 未选" in m for m in _msgs(rep, "E"))


def test_completeness_accepts_a_fully_filled_entry():
    """⛔ 反例：填齐的条目不许报任何 `E`。"""
    rep = _validate_new("0001", _entry(
        "0001", nl_evidence="NL-L002 逐字含 'it transitions from the initial state'",
        primary_predicate="initial_target", layer="nl_named",
        reference_side="参考侧写了 [*] --> Init"))
    assert _msgs(rep, "E") == []


def test_completeness_rejects_a_direction_outside_the_enum():
    rep = _validate_new("0001", _entry("0001", direction="pseudostate"))
    assert any("`direction = pseudostate` 不在枚举内" in m for m in _msgs(rep, "E"))
    assert any("unclassified" in m for m in _msgs(rep, "E"))


@pytest.mark.parametrize("field,bad", [
    ("depth", "很深"), ("layer", "wellformed"), ("direction", "reachable"),
])
def test_completeness_rejects_values_outside_each_enum(field, bad):
    rep = _validate_new("0001", _entry("0001", **{field: bad}))
    assert any(f"`{field} = {bad}` 不在枚举内" in m for m in _msgs(rep, "E"))


def test_completeness_rejects_a_multi_valued_single_field():
    rep = _validate_new("0001", _entry("0001", depth="中层 深层"))
    assert any("`depth` 是单值字段" in m for m in _msgs(rep, "E"))


def test_completeness_rejects_an_invented_predicate():
    rep = _validate_new("0001", _entry("0001", primary_predicate="has_initial_edge"))
    assert any("不在 19 谓词封闭词表内" in m for m in _msgs(rep, "E"))


def test_completeness_accepts_the_explicit_none_predicate():
    """⭐ 写 `无` 是合法答案 —— 它说明 19 谓词覆盖不到，⛔ 那本身是发现。"""
    rep = _validate_new("0001", _entry("0001", primary_predicate="无"))
    assert not any("谓词" in m for m in _msgs(rep, "E"))


def test_blank_nl_evidence_is_not_the_same_as_writing_none():
    """⛔⛔ 留空 ≠ 写 `无`：前者是没填（报 E），后者是判过了（放行）。"""
    blank = _validate_new("0001", _entry("0001", nl_evidence=None))
    assert any("必填项 `nl_evidence` 为空" in m for m in _msgs(blank, "E"))
    explicit = _validate_new("0001", _entry("0001", nl_evidence="无"))
    assert not any("nl_evidence" in m for m in _msgs(explicit, "E"))


def test_none_nl_evidence_conflicts_with_a_non_wellformedness_layer():
    """⛔ 除 `wellformedness` 外三层按定义都要 NL 逐字依据 —— 与 `无` 不能并存。"""
    rep = _validate_new("0001", _entry(
        "0001", nl_evidence="无", layer="nl_named"))
    assert any("不能并存" in m for m in _msgs(rep, "E"))
    ok = _validate_new("0001", _entry(
        "0001", nl_evidence="无", layer="wellformedness"))
    assert _msgs(ok, "E") == []


def test_completeness_rejects_a_segment_id_that_does_not_exist():
    rep = _validate_new("0001", _entry("0001", nl_evidence="NL-L009"))
    assert any("不存在的段 id `NL-L009`" in m for m in _msgs(rep, "E"))
    ok = _validate_new("0001", _entry("0001", nl_evidence="NL-L002"))
    assert _msgs(ok, "E") == []


def test_completeness_rejects_a_line_number_past_the_end_of_the_source():
    rep = _validate_new("0001", _entry("0001", generated_side=":999"))
    assert any("只有 16 行" in m for m in _msgs(rep, "E"))


def test_untouched_template_produces_no_new_issue_records():
    """⛔ 空模板不许被当成一条新增条目 —— 否则 54 份会凭空多出 108 条 `E`。"""
    recs = C.parse_new(NF.template("0001"), "0001")
    assert [r for r in recs if "derived" in r] == []
    data = C.collect_pair("0001", os.path.join(HERE, "0001.md"))
    assert data["new_issues"] == []


def test_regenerating_swaps_the_stale_field_block_but_keeps_human_text():
    """⭐ 字段表改版后重跑：原样未填的旧模板要被换掉，⛔ 填过的一个字都不许动。"""
    legacy = fb.LEGACY_NEW_TEMPLATES[0].format(pair="0001")
    assert fb.is_stale_template(legacy, "new", "0001")
    assert not fb.is_stale_template(legacy + "\nstatement: 我写的", "new", "0001")
    assert not fb.is_stale_template(NF.template("0001"), "new", "0001")

    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "0001.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(fb.render("NEW-0001", "new",
                               legacy.replace("statement:", "statement: 我写的判断", 1)))
        subprocess.run([sys.executable, os.path.join(HERE, "generate.py"),
                        "--pairs", "0001", "--out", tmp],
                       check=True, capture_output=True)
        with open(path, encoding="utf-8") as fh:
            after = fh.read()
        assert "我写的判断" in after
