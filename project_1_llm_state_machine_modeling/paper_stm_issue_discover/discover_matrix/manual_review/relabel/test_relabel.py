"""重标工作区的回归测试。

钉住八件**出错就会静默毁掉这轮人工工作**的事：

1. ⛔ 生成器不许改台账。
2. ⛔ `00x8` 越界 pair 不许有工作单。
3. ⭐ 生成器幂等 —— 连跑两次产物逐字节相同，且重跑**不吃掉**人工填写的内容。
4. ⭐ 每份工作单自包含 —— 台账里该 pair 的每一条都有裁决区。
5. ⭐ §1.2 的 NL 表是三列，且**每一段都真有中文译文**（⛔ 不许留 TODO 占位）。
6. ⭐ 译文与语料的机械对拍：9 份 JSON 按 **sha8** 一一对上 9 份唯一 NL，逐段 `en`
   与原文逐字节相等且能拼回全文，⛔ 对不上必须**抛异常**而不是静默跳过（正反用例都测）；
   ⭐ 逐段判读提示与整份 `translator_notes` 都不许缺。
7. ⭐ §5 的新增字段块能被 `collect.py` 完整解析回来（⛔ 含带冒号的多行 statement）。
8. ⭐ 三条校验（边界 / 去重 / 完整性）各有正反用例 —— ⛔ 只测「能报错」不算，
   还得测「不该报的时候不报」，否则一条恒报的规则也能通过测试。

跑法：`python3 -m pytest test_relabel.py -q`（在本目录下）。
"""

from __future__ import annotations

import contextlib
import copy
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


def test_two_consecutive_full_runs_are_byte_identical():
    """⭐ 连跑两次，54 份产物**逐字节相同**。

    ⚠️ 与上一条的差别：那条测的是「重跑不吃人工填写」，走的是单个 pair；
    这条测的是**全量**材料侧的稳定性 —— ⛔ 只要有一处把当前时间、集合序或字典序写进正文，
    每次重跑就是一个假 diff，人工填写与材料更新混在一起再也分不开。
    """
    with tempfile.TemporaryDirectory() as tmp:
        digests = []
        for _ in range(2):
            subprocess.run([sys.executable, os.path.join(HERE, "generate.py"),
                            "--out", tmp], check=True, capture_output=True)
            digests.append({f: _sha(os.path.join(tmp, f))
                            for f in sorted(os.listdir(tmp)) if f.endswith(".md")})
        assert len(digests[0]) == len(S.IN_SCOPE_PAIRS)
        assert digests[0] == digests[1], "两次全量生成的产物不逐字节相同"


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
    # ⭐ 译文目录里的验收依据也算 —— ⛔ 它是入库文档，不是外部附件
    trans = os.path.join(HERE, "translations")
    targets += [os.path.join(trans, f) for f in sorted(os.listdir(trans))
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
        d = nl_zh.digest8(pair)
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
    assert nl_zh.digest8("0008") not in nl_zh.TRANSLATIONS


def test_translation_keeps_state_names_in_english():
    """⭐ 状态名 / 变量名一律保留英文原样 —— 抽查两组里逐字出现的标识符。"""
    checks = {
        "b7425c44": ["AutonomousMode", "InitialState", "HighwayMode", "UrbanMode",
                     "enter_hwy", "lane_change", "dist_to_front", "auto_finished",
                     "collision_avoidance_deactive"],
        "934e19bd": ["DoorShut", "DoorOpen", "DoorOpenWithItem",
                     "DoorShutWithItem", "ReadytoCook", "Cooking"],
    }
    for digest, names in checks.items():
        blob = " ".join(nl_zh.TRANSLATIONS[digest].values())
        for name in names:
            assert name in blob, f"{digest} 的译文里丢了标识符 {name}"


# ============================================== 译文 JSON 与语料的机械对拍

def test_every_translation_file_matches_a_real_nl_by_sha8():
    """⭐ 9 份 JSON 的 `sha8` 必须各自对上一份在评语料的 `nl.txt`，⛔ 且一一对应。

    ⚠️ 这是回填的**唯一**匹配依据 —— 译文不带 pair 号，只带 sha8。若 `nl.txt` 改了字节，
    sha8 变化，这里就会红；⛔ 静默跳过的后果是那 6 个 pair 整份缺译而没人发现。
    """
    files = nl_zh._raw()                                       # noqa: SLF001
    by_sha8 = {}
    for pair in S.IN_SCOPE_PAIRS:
        by_sha8.setdefault(nl_zh.digest8(pair), []).append(pair)
    assert len(by_sha8) == 9, f"在评 54 个 pair 应只覆盖 9 份唯一 NL，实得 {len(by_sha8)}"
    assert set(files) == set(by_sha8), (
        f"译文文件与语料的 sha8 集合不等：\n"
        f"  只在译文里：{sorted(set(files) - set(by_sha8))}\n"
        f"  只在语料里：{sorted(set(by_sha8) - set(files))}")
    for sha8, pairs in by_sha8.items():
        assert len(pairs) == 6, f"{sha8} 覆盖 {len(pairs)} 个 pair，应为 6"
        # ⭐ sha8 是 sha256 的真前缀，⛔ 不是别的什么摘要
        full = hashlib.sha256(S.nl_text(pairs[0]).encode("utf-8")).hexdigest()
        assert full.startswith(sha8)


def test_translation_en_concatenates_back_to_the_raw_nl():
    """⛔ 逐段 `en` 拼回去必须还原 `nl.txt` —— ⚠️ 拼接口径**因份而异**。

    `0000` 走人工分段（切点在行内），逐段 `en` **直接**拼接即得原文；其余 8 份按物理行切，
    需用 `\\n` 拼接。⭐ 两种口径都试，⛔ 但**必须有一种逐字节还原**；
    ⚠️ 只要一份都还原不了，就说明译文对着另一版原文写的，⛔ 那份译文全部作废。

    ⭐ 另外逐段比一遍 `en == 原文段`：⛔ 整篇拼接相等而段边界错位，只有逐段比才抓得住。
    """
    for sha8, (name, j) in nl_zh._raw().items():               # noqa: SLF001
        pair = next(p for p in S.IN_SCOPE_PAIRS if nl_zh.digest8(p) == sha8)
        raw = S.nl_text(pair)
        ens = [s["en"] for s in j["segments"]]
        assert any(c == raw or c == raw.rstrip("\n")
                   for c in ("".join(ens), "\n".join(ens), "\n".join(ens) + "\n")), \
            f"{name} 的 en 无论直接拼还是换行拼都还原不出 {pair} 的 nl.txt"
        segs, _ = S.nl_segments(pair)
        assert len(segs) == len(ens), f"{name} 段数 {len(ens)} ≠ 语料分段数 {len(segs)}"
        for (sid, txt), en in zip(segs, ens):
            assert en == txt, f"{name} 的 {sid} 段 en 与原文不逐字节相等"


@contextlib.contextmanager
def _mock_raw(payload):
    """临时替换 `nl_zh._raw()` 的返回值。⭐ 只用于在本文件内制造反例。"""
    original = nl_zh._raw                                      # noqa: SLF001
    nl_zh._raw = lambda: payload                               # noqa: SLF001
    try:
        yield
    finally:
        nl_zh._raw = original                                  # noqa: SLF001


def test_translation_mismatch_raises_instead_of_skipping():
    """⛔ 对不上要**报错**，⛔ 不许静默跳过 —— 正反两面都测。

    ⚠️ 只测「正常时不报错」等于没测：一个永远返回 `None` 的装载器也能过。
    所以这里把一份 JSON 的 `en` 改坏、再塞一个孤儿 sha8，
    ⭐ 断言它**确实**抛 `TranslationMismatch`；⛔ 最后再验一遍不动数据时不抛。
    """
    real = copy.deepcopy(dict(nl_zh._raw()))                   # noqa: SLF001

    broken = copy.deepcopy(real)
    broken["f1c3dc88"][1]["segments"][0]["en"] += " 混入的一个字"
    with _mock_raw(broken):
        with pytest.raises(nl_zh.TranslationMismatch, match="逐字节"):
            nl_zh._store.__wrapped__()                         # noqa: SLF001

    orphan = copy.deepcopy(real)
    orphan["deadbeef"] = ("nl_9999.json", {"sha8": "deadbeef", "segments": []})
    with _mock_raw(orphan):
        with pytest.raises(nl_zh.TranslationMismatch, match="对不上任何在评 pair"):
            nl_zh._store.__wrapped__()                         # noqa: SLF001

    # ⛔ 反反面：不动数据时**不许**抛 —— 否则上面两条对一个恒抛的实现也成立
    with _mock_raw(real):
        nl_zh._store.__wrapped__()                             # noqa: SLF001


def test_every_nl_segment_has_a_reading_note():
    """⭐ 按 SPEC 每段都要有判读提示 —— ⛔ 缺提示等于把歧义判断悄悄推给读者。"""
    assert nl_zh.missing_notes() == []


# ================================================== 判读提示不许指涉被测制品（C-①）

def test_no_translation_note_mentions_the_artifact():
    """⛔ 9 份译文的 `note` / `translator_notes` 里不许有**任何**制品指涉。

    ⚠️ 这是 2026-08-13 审计查出的 C 级问题的回归门（见 [README.md](./README.md) §十）：
    一份 NL 服务 6 个 pair，译文按 NL 分组注入，⛔ 于是一句关于某一份制品的话会被逐字印进
    6 份工作单、对其中 5 份为假。⭐ 实测规模：79 条可核验断言里 68 条在至少一个兄弟上为假。
    """
    bad = {}
    for name, payload in nl_zh._raw().values():                # noqa: SLF001
        leaks = nl_zh.artifact_leaks(payload)
        if leaks:
            bad[name] = leaks
    assert bad == {}, "译文提示里有制品指涉：\n" + "\n".join(
        f"{n}:\n  " + "\n  ".join(v) for n, v in sorted(bad.items()))


def test_nl_0001_note_does_not_miscount_the_triggers_the_source_text_gives():
    """⛔ I-A 回归：剥离制品断言时，`nl_0001` 的转向**新写出了一条关于原文的假事实**。

    ⚠️ 逐字（当时印在 `0001` `0011` `0021` `0031` `0041` `0051` 六份工作单上）：
    「…在原文中都没有依据，**三条迁移中也只有一条带触发词**」。⛔ 它是假的 ——
    NL 第 2 句给出的三条迁移**各自都带一个触发**（`receives a brake signal` /
    `the signal transmission fails` / `the signal feedback is sent`），
    ⭐ 没有触发的是**第 3 句**那条（braking → brake caliper clamping）。
    ⛔ 而且它与同一段自己的话打架：前面刚写「原文三句只点到…**三个信号**」。

    ⚠️ 危害形态与 C-① 同类，只是对象从制品换成原文：判读者据此可能记下一条并不存在的
    缺陷（「制品给两条迁移编了原文没给的触发」），⛔ 而这类记录会进入重标产物。
    """
    payload = next(pl for _, pl in nl_zh._raw().values()          # noqa: SLF001
                   if pl["nl_id"] == "0001")
    tn = payload["translator_notes"]
    seg2 = next(s["en"] for s in payload["segments"] if s["seg"] == "2")
    seg3 = next(s["en"] for s in payload["segments"] if s["seg"] == "3")

    # ⭐ 先把「事实是什么」逐字钉在原文上，⛔ 不靠记忆
    for cue in ("receives a brake signal",
                "the signal transmission fails",
                "the signal feedback is sent"):
        assert cue in seg2, f"NL 第 2 句里找不到触发 {cue!r}"
    assert not re.search(r"\b(when|if|once|upon|after receiv)", seg3, flags=re.I), \
        "NL 第 3 句居然带触发词了 —— 本测试的前提要重定"

    # ⛔ 那句假事实不许在（含换个说法再犯）
    assert "三条迁移中也只有一条带触发词" not in tn
    assert not re.search(r"三条迁移[^。；]{0,12}(只有一条|仅一条|只有 ?1 ?条)", tn), tn

    # ⭐ 全组六份工作单里也不许残留
    for pair in ("0001", "0011", "0021", "0031", "0041", "0051"):
        with open(os.path.join(HERE, f"{pair}.md"), encoding="utf-8") as fh:
            assert "只有一条带触发词" not in fh.read(), f"{pair}.md 还印着那句假事实"


def test_artifact_leak_gate_actually_fires():
    """⛔ 反面：门必须**真的**拦得住 —— ⚠️ 只测「干净时不报」等于没测。

    ⭐ 四个反例逐一覆盖两条判据，⛔ 外加一个「干净」正例防止实现恒抛：
    禁用词（中文入口词 `模型`）、制品文件名（`plantuml.puml`）、
    `translator_notes` 与 `note` 两个字段各测一次、以及原文里没有的驼峰标识符。
    """
    clean = {"segments": [{"seg": "1",
                           "en": "1. The system begins in the PumpControl state. ",
                           "zh": "1. 系统起始于 PumpControl。",
                           "note": "约束初始点：起点是 PumpControl，原文未给出触发。"}],
             "translator_notes": "原文只有一句，未点名任何事件名。"}
    assert nl_zh.artifact_leaks(clean) == []

    def leaks(**over):
        payload = copy.deepcopy(clean)
        if "note" in over:
            payload["segments"][0]["note"] = over["note"]
        if "tn" in over:
            payload["translator_notes"] = over["tn"]
        return nl_zh.artifact_leaks(payload)

    # ① 中文入口词，note 侧
    hit = leaks(note="模型中不存在任何以 PumpState 为目标的迁移。")
    assert any("`模型`" in h and "segments[1].note" in h for h in hit)

    # ② 制品文件名，translator_notes 侧
    hit = leaks(tn="见 plantuml.puml 的两条 -- 分隔符。")
    assert any("`plantuml`" in h and "translator_notes" in h for h in hit)

    # ③ 原文里没有的驼峰标识符（⛔ 只可能来自某一份制品）
    hit = leaks(note="起点其实落在 InitialState 上。")
    assert any("`InitialState`" in h for h in hit)

    # ④ 原文里没有的下划线标识符
    hit = leaks(note="守卫写作 dist_to_front>=25。")
    assert any("`dist_to_front`" in h for h in hit)

    # ⑤ ⭐ 正例复核：原文**点了名**的标识符必须放行，⛔ 否则译文没法讲原文点了什么
    assert leaks(note="本句唯一点名的状态是 PumpControl。") == []


def test_artifact_leak_raises_at_load_time():
    """⛔ 装载期就要抛，⛔ 不许降级成「这一份跳过」—— ⚠️ 材料错了就不该产出工作单。"""
    real = copy.deepcopy(dict(nl_zh._raw()))                   # noqa: SLF001
    dirty = copy.deepcopy(real)
    dirty["f1c3dc88"][1]["segments"][0]["note"] += "（模型中无此状态）"
    with _mock_raw(dirty):
        with pytest.raises(nl_zh.NoteArtifactLeak, match="指涉了被测制品"):
            nl_zh._store.__wrapped__()                         # noqa: SLF001
    # ⛔ 反反面：不动数据时**不许**抛
    with _mock_raw(real):
        nl_zh._store.__wrapped__()                             # noqa: SLF001


# ============================ 提示讲原文也得讲对：词法可判定的那一小块（I-B）

def test_no_translation_note_points_at_a_nonexistent_place_in_the_source():
    """⭐ 正面：9 份译文里所有**指向原文的引用**都要指得到。

    ⚠️ 这是 2026-08-13 第二轮全量核对的回归门（见 [README.md](./README.md) §11）：
    上一轮剥掉「讲制品」之后，还剩一类零机械覆盖的错 —— ⛔ **讲原文、但讲错了**。
    ⭐ 其中只有三种能被完美判定（[CLAUDE.md] §11），全放在 `original_ref_errors()`：
    句号越界、段 id 不存在、引文与 `en` 不逐字。⛔ 数错 / 范围说错不可机械判定，靠人工复核。
    """
    bad = {}
    for sha8, (name, payload) in nl_zh._raw().items():         # noqa: SLF001
        pair = next(p for p in S.IN_SCOPE_PAIRS if nl_zh.digest8(p) == sha8)
        segs, _ = S.nl_segments(pair)
        errs = nl_zh.original_ref_errors(payload, [sid for sid, _ in segs])
        if errs:
            bad[name] = errs
    assert bad == {}, "译文提示里有指不到原文的引用：\n" + "\n".join(
        f"{n}:\n  " + "\n  ".join(v) for n, v in sorted(bad.items()))


def test_original_ref_gate_actually_fires():
    """⛔ 反面：门必须**真的**拦得住 —— ⚠️ 只测「干净时不报」等于没测。

    ⭐ 三条判据各一个反例，⛔ 外加两组正例防止实现恒抛：
    ① 干净文本；② ⚠️ **示意写法必须放行** —— `"either ... or"`、`"begins in X"`
    这类含省略号或单大写字母占位符的引文不是逐字引用，⛔ 拒了就是误伤
    （离线实测：不跳过则 86 条 ASCII 引文里 8 条被误拒，全是示意写法）。
    """
    clean = {"segments": [
        {"seg": "1", "en": "1. The system begins in the PumpControl state. ",
         "zh": "1. 系统起始于 PumpControl。",
         "note": "第 1 句只点了 PumpControl，未给出触发。"},
        {"seg": "2", "en": "2. It then moves on. ",
         "zh": "2. 随后它继续。", "note": "第 2 句无新元素。"},
    ], "translator_notes": "原文两句，引一句原样：\"begins in the PumpControl state\"。"}
    ids = ["NL-L001", "NL-L002"]
    assert nl_zh.original_ref_errors(clean, ids) == []

    def errs(**over):
        payload = copy.deepcopy(clean)
        if "note" in over:
            payload["segments"][0]["note"] = over["note"]
        if "tn" in over:
            payload["translator_notes"] = over["tn"]
        return nl_zh.original_ref_errors(payload, ids)

    # ① 定位式 · 句号越界（本份只有 2 段）
    hit = errs(note="见第 5 句的说明。")
    assert any("第 5 句" in h and "只有 2 段" in h for h in hit), hit
    assert errs(note="见第 2 句的说明。") == []          # ⭐ 边界内必须放行

    # ② 定位式 · 段 id 不存在
    hit = errs(tn="详见 NL-L007 那一段。")
    assert any("NL-L007" in h for h in hit), hit
    assert errs(tn="详见 NL-L002 那一段。") == []        # ⭐ 存在的 id 必须放行

    # ③ 引用式 · 引文与 en 对不上（⛔ 差一个词就算）
    hit = errs(note="原文写的是 \"begins in the PumpState state\"。")
    assert any("PumpState" in h for h in hit), hit

    # ④ ⭐ 示意写法放行 —— ⛔ 这两条不许报，否则门会误伤合规文本
    assert errs(note="原文用 \"either ... or\" 结构，也写作 \"begins in X\"。") == []
    assert errs(note="\"the conditions A, B, and C\" 之间的连接词未给出。") == []

    # ⑤ ⭐ 非 ASCII 引文不在本条管辖内（中文引号内容不参与逐字比对）
    assert errs(note="译文把它写作 \"起始于 PumpControl\"。") == []


def test_original_ref_error_raises_at_load_time():
    """⛔ 装载期就要抛，⛔ 不许降级 —— ⚠️ 引错位置会把判读者指到别的句子上。"""
    real = copy.deepcopy(dict(nl_zh._raw()))                   # noqa: SLF001
    dirty = copy.deepcopy(real)
    # ⭐ `f1c3dc88`（nl_0000）只有 6 段，⛔ 引「第 9 段」必然指不到
    dirty["f1c3dc88"][1]["segments"][0]["note"] += "（详见第 9 段）"
    with _mock_raw(dirty):
        with pytest.raises(nl_zh.NoteOriginalRefError, match="指不到原文"):
            nl_zh._store.__wrapped__()                         # noqa: SLF001
    # ⛔ 反反面：不动数据时**不许**抛
    with _mock_raw(real):
        nl_zh._store.__wrapped__()                             # noqa: SLF001


def test_translation_notes_do_not_miscount_what_the_source_text_says():
    """⛔ I-B 回归：第二轮全量核对里逐条打掉的**关于原文的假事实**，⛔ 不许回潮。

    ⚠️ 每一条都先把「事实是什么」逐字钉在 `en` 上，⛔ 再断言那句错话不在 ——
    ⭐ 这样即便日后有人换个说法重写，前半段的前提校验也会先炸。
    """
    def payload(nl_id):
        return next(pl for _, pl in nl_zh._raw().values()      # noqa: SLF001
                    if pl["nl_id"] == nl_id)

    # ① nl_0000：`final state` 原文第 6 段就有，⛔ 不许再说它「未出现于原文」
    p0 = payload("0000")
    en0 = "".join(s["en"] for s in p0["segments"])
    assert "final state" in en0, "NL-0000 里居然没有 final state —— 本测试前提要重定"
    assert "initial pseudostate（初始伪状态）、final state（终态）" not in p0["translator_notes"]

    # ② nl_0000：第 5 段确实写了 mode，⛔ 不许把它排除在 mode 组之外
    seg5 = next(s["en"] for s in p0["segments"] if s["seg"] == "5")
    assert "human driving mode" in seg5
    assert "第 1、2、3 段用 mode" not in p0["translator_notes"]

    # ③ nl_0006：代词 it 只有 3 次（第 2、3、4 段各一次），⛔ 不是 4 次
    p6 = payload("0006")
    n_it = sum(len(re.findall(r"\bit\b", s["en"])) for s in p6["segments"])
    assert n_it == 3, f"NL-0006 的 it 实测 {n_it} 次 —— 本测试前提要重定"
    assert not re.search(r"代词 it[^。]{0,20}4 次", p6["translator_notes"])

    # ④ nl_0009：第 13 句的三个条件也是裸标识符，⛔ 不许说「其余布尔条件一律 x=true」
    p9 = payload("0009")
    seg13 = next(s["en"] for s in p9["segments"] if s["seg"] == "13")
    for bare in ("`front_inactive`", "`rear_inactive`", "`pedestrian_inactive`"):
        assert bare in seg13, f"NL-0009 第 13 句里找不到 {bare}"
    note12 = next(s["note"] for s in p9["segments"] if s["seg"] == "12")
    assert "NL 其余布尔条件一律写作" not in note12

    # ⑤ nl_0009：单位在散文里给过（"2 kilometers"），⛔ 不许说「全文未声明单位」
    seg4 = next(s["en"] for s in p9["segments"] if s["seg"] == "4")
    assert "2 kilometers" in seg4
    blob = p9["translator_notes"] + "".join(s["note"] for s in p9["segments"])
    assert "全文未声明单位" not in blob
    assert "NL 全文未声明 `dist_to_exit` 的单位" not in blob

    # ⑥ nl_0003：译文的〔译者存疑〕里不许再指认原文没有的事件名
    p3 = payload("0003")
    en3 = "".join(s["en"] for s in p3["segments"])
    for ident in ("Accelerate Signal", "Brake Signal", "Stop Signal"):
        assert ident not in en3, f"NL-0003 原文里居然有 {ident} —— 本测试前提要重定"
        assert all(ident not in s["zh"] for s in p3["segments"]), \
            f"nl_0003 的 zh 里还留着原文没有的 {ident}"


def test_worksheet_warns_that_notes_never_assert_about_the_artifact():
    """⭐ 54 份工作单的提示区都要挂那句「提示不含制品断言、请自己去 §1.3 核对」。

    ⚠️ 旧版页面上立的是「提示只陈述原文、不含任何裁决」，⛔ 而提示里恰恰藏着假的制品事实 ——
    ⛔ 声明反过来在劝读者不要去核。⭐ 故声明必须与新纪律同步，⛔ 不能只改数据不改声明。
    """
    for pair in S.IN_SCOPE_PAIRS:
        with open(os.path.join(HERE, f"{pair}.md"), encoding="utf-8") as fh:
            block = fh.read().split("⭐ 逐段判读提示")[1].split("</details>")[0]
        assert "不含任何关于本 pair 制品的断言" in block, f"{pair} 的提示区缺制品免责声明"


def test_every_nl_has_translator_notes():
    """⭐ 整份 NL 层面的观察（术语表 / 跨句歧义 / 原文质量）9 份都得有。"""
    for pair in S.IN_SCOPE_PAIRS:
        tn = nl_zh.translator_notes(pair)
        assert tn and len(tn) > 200, f"{pair} 的 translator_notes 缺失或过短"


def test_worksheet_carries_notes_and_translator_notes():
    """⭐ 54 份工作单都要有逐段提示与整份观察，⛔ 且提示要逐段挂到真实段 id 上。"""
    for pair in S.IN_SCOPE_PAIRS:
        with open(os.path.join(HERE, f"{pair}.md"), encoding="utf-8") as fh:
            doc = fh.read()
        assert "⭐ 逐段判读提示" in doc, f"{pair} 缺逐段判读提示区"
        assert "⭐ 整份 NL 层面的观察" in doc, f"{pair} 缺整份 NL 观察区"
        assert "./translations/TRANSLATION_SPEC.md" in doc, f"{pair} 未挂译文验收依据"
        assert f"./translations/{nl_zh.source_file(pair)}" in doc, f"{pair} 未挂译文 JSON"
        block = doc.split("⭐ 逐段判读提示")[1].split("</details>")[0]
        for sid, _txt in S.nl_segments(pair)[0]:
            assert f"- `{sid}`：" in block, f"{pair} 的提示区缺 {sid}"
            assert "⛔ 译者未给提示" not in block, f"{pair} 的提示区有空提示"


# ==================================================================== §5 字段块

def _entry(pair, idx=1, **over):
    """拼一条 §5 新增登记。⭐ 值为 `None` 表示那一行整个不写（模拟漏填）。

    ⭐ 默认是一条**填齐的、界内的、依据自洽的**条目：`basis = 模型自身` 配
    `nl_evidence = 无`，`scope = 界内`。⛔ 这样每个用例只需覆写它要测的那一项，
    被测信号不会被别的 `E` 淹掉。
    """
    fields = {
        "statement": "顶层没有任何进入 InitialState 的初始边，冷启动落点未定义。",
        "generated_side": ":2 [*] --> InitialState",
        "basis": "模型自身",
        "nl_evidence": "无",
        "scope": "界内",
        "direction": "entry",
        "depth": "中层",
    }
    fields.update(over)
    out = [f"### NEW-{pair}-{idx:02d}"]
    out += [f"{k}: {v}" for k, v in fields.items() if v is not None]
    return "\n".join(out)


def _validate_new(pair, *entries, allow_ledger=False):
    """⭐ 走真实链路：`parse_new` 解析 → `validate_pair` 校验。返回 Report。

    ⛔ 固定用台账 0 条的 pair，否则「台账条目未裁决」的 E 会淹掉被测信号。

    ⚠️ `allow_ledger=True` 只给**永久排除**的 `00x8` 用：它们有台账条目却**没有工作单**，
    所以喂空 `ledger` 必然带出「找不到裁决区」的 `E`。⭐ 调用方须自行用
    `_msgs_for()` 按条目 key 过滤，⛔ 不许直接看全表。
    """
    if not allow_ledger:
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


def _msgs_for(rep, key, level=None):
    """⭐ 只取某一条记录（按 `key`）上的消息 —— ⛔ 用于台账非空的载体 pair。"""
    return [i["msg"] for i in rep.items
            if i["key"] == key and (level is None or i["level"] == level)]


def test_new_issue_field_block_round_trips_through_collect():
    """⭐ 人工填的 10 个字段必须能被 `collect.py` 原样收回来。"""
    body = _entry("0001", 1, primary_predicate="initial_target",
                  reference_side="参考侧有 [*] --> Init", layer="wellformedness")
    recs = C.parse_new(body, "0001")
    assert len(recs) == 1
    f = recs[0]["fields"]
    assert recs[0]["id"] == "NEW-0001-01"
    assert f["statement"].startswith("顶层没有任何")
    assert f["generated_side"] == ":2 [*] --> InitialState"
    assert f["basis"] == "模型自身"
    assert f["nl_evidence"] == "无"
    assert f["scope"] == "界内"
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
            .replace("[ ] NL显式义务", "[x] NL显式义务")
            .replace("[ ] 界内", "[x] 界内")
            .replace("[ ] guard ", "[x] guard ")
            .replace("[ ] 深层", "[x] 深层"))
    recs = C.parse_new(body, "0001")
    assert len(recs) == 1
    f = recs[0]["fields"]
    assert f["basis"]["chosen"] == ["NL显式义务"]
    assert f["scope"]["chosen"] == ["界内"]
    assert f["direction"]["chosen"] == ["guard"]
    assert f["depth"]["chosen"] == ["深层"]
    assert f["nl_evidence"] == "NL-L003"


# ---- ⭐ 三层结构本身

def test_the_field_block_is_organised_in_three_layers():
    """⭐ 三层必须在模板里**看得见** —— ⛔ 只在文档里讲、模板里不体现等于没做。"""
    body = NF.template("0001", count=1)
    order = [ln for ln in body.splitlines() if ln.startswith("---")]
    assert order == [NF.SEP_FACT, NF.SEP_BASIS, NF.SEP_SCOPE,
                     NF.SEP_AXIS, NF.SEP_OPTIONAL]
    # ⭐ 每层的字段必须落在自己那一段里
    def between(a, b):
        seg = body.split(a, 1)[1].split(b, 1)[0]
        return [ln.split(":", 1)[0] for ln in seg.splitlines() if ":" in ln]
    assert between(NF.SEP_FACT, NF.SEP_BASIS) == ["statement", "generated_side"]
    assert between(NF.SEP_BASIS, NF.SEP_SCOPE) == ["basis", "nl_evidence"]
    assert between(NF.SEP_SCOPE, NF.SEP_AXIS) == ["scope"]
    assert between(NF.SEP_AXIS, NF.SEP_OPTIONAL) == ["direction", "depth"]


def test_layer_separators_are_not_parsed_as_content():
    """⛔ 分层小标题不是字段，⛔ 也不许被并进上一个字段的值里。

    ⚠️ 这条是设计时就看得见的坑：`--- ② 依据层 · … ---` 紧跟在 `generated_side:`
    之后，而它不匹配字段名正则（行首是 `-`），于是会被**并进 `generated_side`** ——
    定位串静默多出一整行，行号解析与去重判据一起脏掉。
    """
    body = (NF.template("0001", count=1)
            .replace("generated_side:", "generated_side: :5"))
    f = C.parse_new(body, "0001")[0]["fields"]
    assert f["generated_side"] == ":5", f["generated_side"]
    for sep in NF.SEPARATORS:
        assert sep not in str(f), f"分层小标题 {sep!r} 混进了字段值"
    assert "_raw_lines" not in f


def test_readme_worked_example_can_never_be_collected_as_a_real_judgement():
    """⛔ README §3.6.3 的填好样例不许被当成真实判读回收。

    三重保险，⭐ 三条都测：① 它写在 README 里，而 [collect.py](./collect.py) 只读
    54 份 `<pair>.md`；② README 里**没有** `FILL` 哨兵，`fb.extract` 抽不出任何块；
    ③ 它用的 pair 是 `0008` —— 永久排除、**不生成工作单**，所以那个 id
    永远不可能出现在任何被回收的文件里。
    """
    with open(os.path.join(HERE, "README.md"), encoding="utf-8") as fh:
        readme = fh.read()
    assert "NEW-0008-01" in readme, "README 的填好样例不见了"
    assert fb.extract(readme) == {}, "README 里出现了 FILL 哨兵 —— 会被误当成填写块"
    assert "0008" in S.OUT_OF_SCOPE_PAIRS
    assert not os.path.exists(os.path.join(HERE, "0008.md"))
    # ⭐ 样例引的段 id 与作者源行号必须是**真的**
    assert "NL-L001" in {sid for sid, _ in S.nl_segments("0008")[0]}
    src = S.puml_text("0008").splitlines()
    assert src[4].strip() == "[*] --> fork1: After (2 s)", "样例引的第 5 行对不上作者源"
    assert src[7].strip() == "TurnOn --> fork1"
    # ⛔ 全量回收一遍：样例不许出现在产物里
    for pair in S.IN_SCOPE_PAIRS:
        data = C.collect_pair(pair, os.path.join(HERE, f"{pair}.md"))
        assert data["new_issues"] == [], f"{pair} 的 §5 被预填了"


def test_out_of_scope_and_in_scope_are_told_apart_by_the_scope_field():
    """⭐ 边界层的判据是判读者勾的 `scope`，⛔ 不是词法命中。"""
    assert NF.is_out_of_scope("越界·时钟或不变式")
    assert NF.is_out_of_scope("越界·并发或正交区")
    assert not NF.is_out_of_scope("界内")
    assert not NF.is_out_of_scope(None)
    # ⛔ 取值里不许含 `_enum_values` 的分隔符，否则单值会被切成多值
    for v in NF.SCOPES + NF.BASES:
        assert V._RE_ENUM_SPLIT.split(v) == [v], f"{v} 含分隔符，会被切开"


def test_derive_marks_an_out_of_scope_entry_as_not_a_defect():
    """⛔ 标了越界的**不得计入缺陷统计** —— 但也**不许丢**。"""
    oos = NF.derive("0001", "NEW-0001-01",
                    {"generated_side": ":5", "scope": "越界·时钟或不变式"})
    assert oos["in_scope"] is False
    assert oos["counts_as_defect"] is False
    assert oos["boundary_ruling"] == "out_of_scope"
    assert "越界·时钟或不变式" in oos["boundary_effect"]

    inside = NF.derive("0001", "NEW-0001-02",
                       {"generated_side": ":5", "scope": "界内"})
    assert inside["in_scope"] is True and inside["counts_as_defect"] is True
    assert inside["boundary_ruling"] is None

    # ⛔ 没勾 `scope` 时不许默认「在界内」—— 未判就必须显形
    unknown = NF.derive("0001", "NEW-0001-03", {"generated_side": ":5"})
    assert unknown["in_scope"] is None and unknown["counts_as_defect"] is None
    assert "in_scope" in unknown["pending"]


def test_progress_counts_exclude_out_of_scope_entries():
    """⛔ 越界条目进「越界」栏，⛔ 不进「新增」栏 —— 两栏都要对。"""
    data = {
        "pair": "0001", "summary": None,
        "ledger": [], "candidates": [], "checklist": [],
        "new_issues": C.parse_new("\n\n".join([
            _entry("0001", 1),
            _entry("0001", 2, scope="越界·并发或正交区",
                   statement="NL 要求两个区域同时活跃，模型无正交区。"),
            _entry("0001", 3, scope="越界·时钟或不变式",
                   statement="NL 要求 2 秒后迁移，模型无时钟。"),
        ]), "0001"),
        "orphans": {}, "untouched_keys": [],
    }
    row = V.pair_progress("0001", data)
    assert row["new"] == 1, "越界条目被算进了缺陷统计"
    assert row["out_of_scope"] == 2
    counted, oos = V.new_issue_split(data)
    assert len(counted) == 1 and len(oos) == 2
    # ⭐ 越界条目仍然完整落盘 —— ⛔ 不许被丢掉
    assert len(data["new_issues"]) == 3


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
                  {"generated_side": ":5", "primary_predicate": "edge_declared",
                   "scope": "界内"})
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
    assert len(NF.REQUIRED_FIELDS) == 7 and len(NF.OPTIONAL_FIELDS) == 3
    # ⭐ 勾选字段必须都在字段表里，⛔ 否则模板给了勾选行而回收器按自由文本读
    assert set(NF.CHOICE_FIELDS) <= set(NF.FIELD_NAMES)
    assert set(NF.REQUIRED_WHEN_OUT_OF_SCOPE) <= set(NF.REQUIRED_FIELDS)


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


def test_boundary_gate_stays_quiet_when_the_author_already_marked_it_out_of_scope():
    """⭐ 反例：已经自己勾了越界的**不再提醒** —— ⛔ 再报一遍只是噪声。

    ⚠️ 这一条和上面几条是一对：词法门只在「勾了界内、而文本像越界」时才说话。
    """
    rep = _validate_new("0001", "\n".join([
        "### NEW-0001-01",
        "statement: NL 要求 2 秒的 timer 超时迁移，模型无时钟可承载。",
        "generated_side: :5",
        "scope: 越界·时钟或不变式",
    ]))
    assert not any("疑似越界" in m for m in _msgs(rep))


def test_boundary_warning_names_the_scope_the_author_actually_chose():
    """⭐ 提醒里要写清「你勾的是界内」并给出改法 —— ⛔ 否则判读者不知道要动哪个字段。"""
    rep = _validate_new("0001", _entry(
        "0001", statement="Cooking 缺少 30 秒 timer 到期后的出边。"))
    msg = next(m for m in _msgs(rep, "W") if "疑似越界" in m)
    assert "`界内`" in msg and "不计入缺陷统计" in msg


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


# ---- ④⭐ 依据自洽（② 依据层）

def test_basis_nl_obligation_requires_a_segment_id():
    """⛔ 正例：依据在 NL 上，就必须指到**哪一段**。"""
    rep = _validate_new("0001", _entry(
        "0001", basis="NL显式义务", nl_evidence="NL 第 2 句说了"))
    assert any("给不出本 pair 的 NL 段 id" in m for m in _msgs(rep, "E"))
    # ⛔ 写 `无` 同样不行 —— 依据自称在 NL 上，却又说没有 NL 依据
    rep = _validate_new("0001", _entry("0001", basis="NL显式义务", nl_evidence="无"))
    assert any("给不出本 pair 的 NL 段 id" in m for m in _msgs(rep, "E"))


def test_basis_underspecified_also_requires_a_segment_id():
    """⭐ `NL欠指定` 同样要指到那一句 —— ⛔ 不指出来就无法复核它到底欠在哪。"""
    rep = _validate_new("0001", _entry("0001", basis="NL欠指定", nl_evidence="无"))
    assert any("给不出本 pair 的 NL 段 id" in m for m in _msgs(rep, "E"))


def test_basis_with_a_segment_id_passes():
    """⛔ 反例：给了真段 id 的 NL 类依据不许报 `E` —— 恒报的规则等于没有规则。"""
    for basis in NF.NL_BASED_BASES:
        rep = _validate_new("0001", _entry(
            "0001", basis=basis,
            nl_evidence="NL-L002 逐字含 'it transitions from the initial state'",
            layer="nl_named" if basis == "NL显式义务" else None))
        assert _msgs(rep, "E") == [], (basis, _msgs(rep, "E"))


def test_model_intrinsic_basis_may_write_none_for_nl_evidence():
    """⛔ 反例：`模型自身` + `无` 是最常见的正确组合，⛔ 不许报错。"""
    rep = _validate_new("0001", _entry("0001", basis="模型自身", nl_evidence="无"))
    assert _msgs(rep, "E") == []
    assert not any("basis" in m for m in _msgs(rep, "W"))


def test_underspecified_basis_must_not_claim_a_violation():
    """⛔ 标了「NL 欠指定」就**不得**同时声称模型「违反」了 NL。

    ⭐ 分两半判，⛔ 不许混：`layer = nl_contradiction` 是两个枚举字段的定值冲突，
    只看字段值就能判定 → `E`；`statement` 里写没写「违反」要读文意、会误伤
    （例如判读者写的是「不违反」）→ 只能 `W`。判据见 [CLAUDE.md] §11。
    """
    hard = _validate_new("0001", _entry(
        "0001", basis="NL欠指定", nl_evidence="NL-L002", layer="nl_contradiction"))
    assert any("不能并存" in m and "欠指定" in m for m in _msgs(hard, "E"))

    soft = _validate_new("0001", _entry(
        "0001", basis="NL欠指定", nl_evidence="NL-L002",
        statement="模型违反了 NL 第 2 句要求的源状态。"))
    assert any("出现了「违反」类措辞" in m for m in _msgs(soft, "W"))
    assert _msgs(soft, "E") == []          # ⛔ 词法判据不许升级成 E


def test_underspecified_basis_worded_as_unspecified_is_accepted():
    """⛔ 反例：改写成「原文未规定」之后不许再报 —— 那正是我们要的写法。"""
    rep = _validate_new("0001", _entry(
        "0001", basis="NL欠指定", nl_evidence="NL-L002",
        statement="NL 第 2 句未指明该迁移的源状态，模型自行选择了 InitialState 这一读法。"))
    assert _msgs(rep, "E") == []
    assert not any("违反" in m for m in _msgs(rep, "W"))


def test_reference_model_basis_cannot_be_recorded_as_an_nl_contradiction():
    """⛔ 参考模型不是 NL，与它不同谈不上「与 NL 的显式义务矛盾」。

    ⚠️ 本测试只断言**形式要求**（哪两个取值不能并存、报错要指出一条出路），
    ⛔ 不钉住报错正文里举了哪个案例 —— 钉住案例会把措辞锁死在原地
    （[CLAUDE.md](../../../../../CLAUDE.md) §13 第 3 条）。⭐ 事实上这条报错 2026-08-13
    换过例子：旧版拿 `EIS-0005-02` 当教科书案例，⛔ 而那个推论不成立（见 README §7.1）。
    """
    rep = _validate_new("0001", _entry(
        "0001", basis="参考模型", nl_evidence="无", layer="nl_contradiction"))
    msgs = _msgs(rep, "E")
    assert any("参考模型" in m and "不能并存" in m for m in msgs)
    assert any("layer" in m and "留空" in m for m in msgs), msgs


def test_reference_model_basis_alone_is_flagged_as_insufficient():
    """⭐ 参考模型不是正确答案 —— 单靠它支撑的条目要提示「待裁定」。"""
    rep = _validate_new("0001", _entry("0001", basis="参考模型", nl_evidence="无"))
    assert any("单独不足以" in m for m in _msgs(rep, "W"))
    assert _msgs(rep, "E") == []           # ⛔ 但它是允许登记的，⛔ 不是硬错


def test_model_intrinsic_basis_conflicts_with_an_nl_layer():
    """⛔ `模型自身` 与 `nl_named` / `nl_contradiction` 是定值冲突 → `E`。"""
    for layer in ("nl_named", "nl_contradiction"):
        rep = _validate_new("0001", _entry(
            "0001", basis="模型自身", nl_evidence="NL-L002", layer=layer))
        assert any("`basis = 模型自身`" in m and "不能并存" in m
                   for m in _msgs(rep, "E")), layer
    # ⛔ 反例：与 `wellformedness` 并存是正常的
    ok = _validate_new("0001", _entry(
        "0001", basis="模型自身", nl_evidence="无", layer="wellformedness"))
    assert _msgs(ok, "E") == []


def test_basis_checks_are_silent_when_basis_is_not_filled_yet():
    """⛔ 反例：`basis` 还没勾时，依据自洽检查不许瞎报 —— 那时该报的是「必填项未选」。"""
    rep = _validate_new("0001", _entry("0001", basis=None, nl_evidence="无"))
    assert any("必填项 `basis` 未选" in m for m in _msgs(rep, "E"))
    assert not any("不能并存" in m for m in _msgs(rep))


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
        "0001", basis="NL显式义务",
        nl_evidence="NL-L002 逐字含 'it transitions from the initial state'",
        primary_predicate="initial_target", layer="nl_named",
        reference_side="参考侧写了 [*] --> Init"))
    assert _msgs(rep, "E") == []


def test_completeness_of_an_out_of_scope_entry_needs_only_the_fact_layer():
    """⭐ 越界条目只需 ① 事实层两项 + `scope`。

    ⛔ 硬要它填 `basis` / `direction` / `depth` 只会逼判读者瞎勾一个 ——
    它不是缺陷，谈「依据强度」「缺陷方向」本来就没有意义。
    """
    rep = _validate_new("0001", "\n".join([
        "### NEW-0001-01",
        "statement: NL 要求本状态在 2 秒后自动迁移，模型里没有任何时间语义可承载它。",
        "generated_side: :5",
        "scope: 越界·时钟或不变式",
    ]))
    assert _msgs(rep, "E") == [], _msgs(rep, "E")


def test_an_entry_with_no_scope_at_all_is_a_hard_error():
    """⛔ 反例：`scope` 是必填 —— 不填就是边界层没判，⛔ 不许默认成「界内」。"""
    rep = _validate_new("0001", _entry("0001", scope=None))
    assert any("必填项 `scope` 未选" in m for m in _msgs(rep, "E"))


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


def test_none_nl_evidence_conflicts_with_an_nl_grounded_layer():
    """⛔ 只有 `nl_named` / `nl_contradiction` 两层按台账定义要 NL 逐字依据。

    ⚠️ 判据来自 `layer_basis` 原话，⛔ 不是「除 `wellformedness` 外都要」：
    `over_specification` 的原话是「生成方凭空多出，且造成可断言的负面后果」，
    ⛔ 一个字没提 NL，台账既有 6 条里也有 5 条 `nl_evidence` 为空。
    """
    assert set(NF.NL_GROUNDED_LAYERS) == {"nl_named", "nl_contradiction"}
    for layer in NF.NL_GROUNDED_LAYERS:
        rep = _validate_new("0001", _entry("0001", nl_evidence="无", layer=layer))
        assert any("不能并存" in m for m in _msgs(rep, "E")), layer
    for layer in ("wellformedness", "over_specification"):
        ok = _validate_new("0001", _entry("0001", nl_evidence="无", layer=layer))
        assert _msgs(ok, "E") == [], (layer, _msgs(ok, "E"))


def test_over_specification_has_a_shape_that_satisfies_every_gate():
    """⭐ CLAUDE.md §13 要求的「满足本门且同时满足既有各门的一个具体形状」，⛔ 机械钉住。

    ⚠️ 2026-08-13 之前 `over_specification` 的合法解空间是**空的**：`nl_evidence` 按定义
    只能写 `无`（NL 对凭空多出的元素什么也没说），而当时那道门要求非 `wellformedness` 层
    必须给段 id；改 `layer = wellformedness` 是误分类，段 id 按定义不存在，
    ⛔ 唯一能过门的做法是把 `layer` 留空 —— 于是这一层在新增条目里被系统性抹掉。

    ⭐ 下面这条就是那个「具体形状」，⛔ 它必须同时过**全部**门：`E` 与 `W` 都为空。
    """
    fields = _readme_gate_shape()
    shape = "\n".join(["### NEW-0008-01"] + [f"{k}: {v}" for k, v in fields.items()])
    rep = _validate_new("0008", shape, allow_ledger=True)
    assert _msgs_for(rep, "NEW-0008-01", "E") == [], _msgs_for(rep, "NEW-0008-01", "E")
    assert _msgs_for(rep, "NEW-0008-01", "W") == [], _msgs_for(rep, "NEW-0008-01", "W")
    # ⛔ 形状本身必须还是那一组取值 —— 换了任何一项，这条测试就不再是 §13 要的那个证明
    assert fields["basis"] == "模型自身"
    assert fields["layer"] == "over_specification"
    assert fields["nl_evidence"] == "无"
    assert fields["scope"] == "界内"


def _readme_gate_shape():
    """从 [README.md](./README.md) §3.6.4 结尾那个 ```text 块里读出字段表。

    ⭐ 直接读 README，⛔ 不在测试里另抄一份 —— 抄了两份就会各改各的，
    而 README 那段自称「由本测试机械钉住」。
    """
    with open(os.path.join(HERE, "README.md"), encoding="utf-8") as fh:
        readme = fh.read()
    head = readme.index("按 §13 的要求，写出一个")
    body = readme[head:readme.index("## 四、命令", head)]
    blocks = re.findall(r"```text\n(.*?)```", body, flags=re.S)
    assert len(blocks) == 1, f"§3.6.4 里应当只有一个形状块，实得 {len(blocks)}"
    out = {}
    for line in blocks[0].strip().splitlines():
        k, _, v = line.partition(":")
        out[k.strip()] = v.strip()
    return out


def test_risk_flag_and_validate_gate_agree_on_which_layers_need_nl_evidence():
    """⛔ I-B 回归：两处规范文本对同一件事给出**相反**的教法（§13 第 2 条）。

    ⚠️ 2026-08-13 出过一次：[validate.py](./validate.py) 的门已经收窄成
    `NF.NL_GROUNDED_LAYERS`（只拦 `nl_named` / `nl_contradiction`），
    ⛔ 而 [sources.py](./sources.py) 的 `no_nl_evidence` 风险标记还写着
    `layer != "wellformedness"` —— ⛔ 于是它对 5 条 `over_specification` 说
    「该层按定义需要 NL 逐字依据」，而 README 同一个 commit 里写着「那是设计如此」。

    ⛔ 落点极其要命：这个标记渲染在「自动风险标记」块里，**紧挨着该条的裁决块上方** ——
    ⛔ 判读者在动笔那一行之前读到的最后一句话，就是那条相反的教法。
    """
    base = next(r for r in S.ledger_records("0001") or S.ledger_records(reportable_only=True))
    for layer in NF.LAYERS:
        rec = dict(base, layer=layer, nl_evidence="")
        flagged = any(k == "no_nl_evidence" for k, _ in S.risk_flags(rec))
        assert flagged == (layer in NF.NL_GROUNDED_LAYERS), (
            f"`{layer}` 上风险标记与 validate 的门不一致："
            f"标记 {flagged} / 门 {layer in NF.NL_GROUNDED_LAYERS}")
        # ⛔ 反向：validate 那道门必须给出同一个答案（⭐ 走真实链路，⛔ 不看常量）
        rep = _validate_new("0001", _entry("0001", layer=layer, nl_evidence="无"))
        gated = any("要求 NL 逐字依据" in m for m in _msgs(rep, "E"))
        assert gated == flagged, (
            f"`{layer}`：validate 门 {gated} / 风险标记 {flagged} —— "
            "⛔ 两处对同一件事说了相反的话")

    # ⛔ 实测影响面：收窄后只剩这两条，⛔ 五条 `over_specification` 不再被标
    marked = sorted(r["id"] for r in S.ledger_records(reportable_only=True)
                    if r["pair"] not in S.OUT_OF_SCOPE_PAIRS
                    and any(k == "no_nl_evidence" for k, _ in S.risk_flags(r)))
    assert marked == ["EIS-0005-02", "EIS-0024-03"], marked

    # ⛔ 落地检查：那 5 份工作单的裁决块上方不许再有相反教法
    for pair in ("0002", "0007", "0032", "0039", "0046"):
        with open(os.path.join(HERE, f"{pair}.md"), encoding="utf-8") as fh:
            text = fh.read()
        assert "非 wellformedness 层却无" not in text, f"{pair}.md 还印着旧教法"
        assert "该层按定义需要 NL 逐字依据" not in text, f"{pair}.md 还印着旧教法"


def test_readme_gate_shape_example_stays_off_the_graded_pairs():
    """⛔ I-C 回归：§3.6.4 的「可满足形状」样例不许取自任何**在评 pair** 的真实制品。

    ⚠️ 2026-08-13 出过一次：那段样例本来写的是 pair `0001` 的一条真实、字段填齐、
    可直接登记的发现（`:14 OperationalState --> ClampingLoseState`，作者源第 14 行逐字如此）。
    ⛔ 它给的不只是事实（`0001.md` 的清单里本来就有），⛔ 而是 `basis` / `layer` /
    `direction` / `depth` **该怎么归类的答案** —— 而字段归类正是本轮要判读者自己做的判断。
    ⛔ 后果按 [CLAUDE.md](../../../../../CLAUDE.md) §3.5.-1：产物里若出现一条与 README
    逐字雷同的记录，「它是人独立发现并归类的吗」将无法回答。

    ⭐ 判据不看措辞，看**指向**：把样例块里出现的标识符逐一拿去比对 —— 凡是「在某个在评
    pair 的作者源里出现、却不在 `0008` 的作者源里」的，一律判为指向在评 pair。
    ⭐ 这与 `test_every_exemplar_slot_resolves_off_group`（§5 样例跨组回避）、
    `test_readme_worked_example_can_never_be_collected_as_a_real_judgement`（§3.6.3 用
    `0008`）是同一条纪律的第三处落点 —— ⛔ 此前只钉了前两处，§3.6.4 是漏的那一处。
    """
    fields = _readme_gate_shape()
    text = " ".join(fields.values())
    idents = set(re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", text))
    safe = set(re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", S.puml_text("0008")))
    safe |= {"over_specification", "reachability", "hierarchy", "guard", "entry",
             "effect_action", "event", "cardinality", "unclassified"}
    for pair in S.IN_SCOPE_PAIRS:
        own = set(re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", S.puml_text(pair)))
        bad = (idents & own) - safe
        assert not bad, (
            f"§3.6.4 的样例指向了在评 pair {pair} 的制品元素 {sorted(bad)} —— "
            "⛔ 换成 0008 或不指向任何在评 pair 的抽象样例")
    # ⛔ 反面自检：判据本身必须抓得住那条被撤掉的旧样例，⚠️ 否则这条测试是摆设
    stale = {"statement": "生成侧凭空多出一条通往 ClampingLoseState 的迁移",
             "generated_side": ":14 OperationalState --> ClampingLoseState"}
    stale_idents = set(re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", " ".join(stale.values())))
    own_0001 = set(re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", S.puml_text("0001")))
    assert (stale_idents & own_0001) - safe, "判据抓不住旧样例 —— 它就白写了"


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


@pytest.mark.parametrize("legacy", [
    fb.LEGACY_NEW_TEMPLATES[0].format(pair="0001"),      # 第一代：10 字段平铺
    NF.template_v2("0001"),                              # 第二代：8 字段、无三层
])
def test_regenerating_swaps_the_stale_field_block_but_keeps_human_text(legacy):
    """⭐ 字段表改版后重跑：原样未填的旧模板要被换掉，⛔ 填过的一个字都不许动。

    ⛔ 少了这条，改版当天的后果很具体：54 份工作单的 §5 会**永远停在旧字段表**上 ——
    幂等注回是按 key 做的，旧骨架会被当成「人工内容」原样保留，三层字段一个都出不来。
    """
    assert fb.is_stale_template(legacy, "new", "0001")
    assert not fb.is_stale_template(legacy + "\nstatement: 我写的", "new", "0001")
    assert not fb.is_stale_template(NF.template("0001"), "new", "0001")

    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "0001.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(fb.render("NEW-0001", "new", legacy))
        subprocess.run([sys.executable, os.path.join(HERE, "generate.py"),
                        "--pairs", "0001", "--out", tmp],
                       check=True, capture_output=True)
        with open(path, encoding="utf-8") as fh:
            swapped = fh.read()
        assert NF.SEP_BASIS in swapped, "原样未填的旧模板没有被换成三层模板"
        assert "basis: [ ]" in swapped and "scope: [ ]" in swapped

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


def test_a_filled_three_layer_block_survives_regeneration():
    """⭐ 幂等的正面用例：三层块**填过之后**重跑生成器，一个字都不许变。"""
    pair = "0001"
    filled = "\n".join([
        "### NEW-0001-01",
        NF.SEP_FACT,
        "statement: ClampingState 没有任何出边，进入后永远留在那里。",
        "generated_side: :8, :9",
        NF.SEP_BASIS,
        "basis: [x] 模型自身  [ ] NL显式义务",
        "nl_evidence: 无",
        NF.SEP_SCOPE,
        "scope: [x] 界内",
        NF.SEP_AXIS,
        "direction: [x] reachability",
        "depth: [x] 中层",
    ])
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(HERE, f"{pair}.md")
        dst = os.path.join(tmp, f"{pair}.md")
        shutil.copy(src, dst)
        with open(dst, encoding="utf-8") as fh:
            text = fh.read()
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(text.replace(NF.template(pair), filled, 1))

        for _ in range(2):
            subprocess.run([sys.executable, os.path.join(HERE, "generate.py"),
                            "--pairs", pair, "--out", tmp],
                           check=True, capture_output=True)
        parsed = C.collect_pair(pair, dst)
        assert len(parsed["new_issues"]) == 1
        f = parsed["new_issues"][0]["fields"]
        assert f["generated_side"] == ":8, :9"
        assert f["basis"]["chosen"] == ["模型自身"]
        assert f["scope"]["chosen"] == ["界内"]
        assert f["direction"]["chosen"] == ["reachability"]
        d = parsed["new_issues"][0]["derived"]
        assert d["in_scope"] is True and d["counts_as_defect"] is True

        # ⭐ 第三次不该再产生任何改动
        before = _sha(dst)
        subprocess.run([sys.executable, os.path.join(HERE, "generate.py"),
                        "--pairs", pair, "--out", tmp],
                       check=True, capture_output=True)
        assert _sha(dst) == before
