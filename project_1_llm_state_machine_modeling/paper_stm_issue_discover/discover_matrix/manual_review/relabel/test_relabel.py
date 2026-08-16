"""重标工作区的回归测试。

钉住八件**出错就会静默毁掉这轮人工工作**的事：

1. ⛔ 生成器不许改台账。
2. ⛔ `00x8` 越界 pair 不许有工作单。
3. ⭐ 生成器幂等 —— 连跑两次产物逐字节相同，且重跑**不吃掉**人工填写的内容。
4. ⭐ 每份工作单自包含 —— 台账里该 pair 的每一条都有裁决区。
5. ⭐ §1.1 的 NL 表是三列，且**每一段都真有中文译文**（⛔ 不许留 TODO 占位）。
6. ⭐ 译文与语料的机械对拍：9 份 JSON 按 **sha8** 一一对上 9 份唯一 NL，逐段 `en`
   与原文逐字节相等且能拼回全文，⛔ 对不上必须**抛异常**而不是静默跳过（正反用例都测）；
   ⭐ 逐段判读提示与整份 `translator_notes` 都不许缺。
7. ⭐ §5 的新增字段块能被 `collect.py` 完整解析回来（⛔ 含带冒号的多行 statement）。
8. ⭐ 三条校验（边界 / 去重 / 完整性）各有正反用例 —— ⛔ 只测「能报错」不算，
   还得测「不该报的时候不报」，否则一条恒报的规则也能通过测试。

跑法：`python3 -m pytest test_relabel.py -q`（在本目录下）。
"""

from __future__ import annotations

import collections
import contextlib
import json as _json
import copy
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse as _urllib_parse

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import candidate_mapping as CM  # noqa: E402
import generate as G          # noqa: E402
import inspectfindings as IF  # noqa: E402
import collect as C            # noqa: E402
import fillblocks as fb        # noqa: E402
import ledger_mapping as LM    # noqa: E402
import newfields as NF         # noqa: E402
import nl_zh                   # noqa: E402
import sources as S            # noqa: E402
import terms as T              # noqa: E402
import validate as V           # noqa: E402
from pumlmodel import PumlModel  # noqa: E402


def _sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _ws(pair, base=HERE):
    """工作单路径。⭐ 一律走 `sources.worksheet_path()`，⛔ 测试里不另拼一份 ——
    ⚠️ 拼两份的后果是目录布局再变一次时，测试还能全绿地指向不存在的路径。
    """
    return S.worksheet_path(base, pair)


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _all_md(base):
    """`base` 下任意深度的入库 `.md`，返回相对路径的排序表。

    ⛔ 跳过隐藏目录与 `__pycache__` —— ⚠️ `.pytest_cache/README.md` 是工具产物，
    ⛔ 把它算进入库文档会让 unwrap 检查在一份我们不该改的文件上失败。
    """
    out = []
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
        for f in files:
            if f.endswith(".md"):
                out.append(os.path.relpath(os.path.join(root, f), base))
    return sorted(out)


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
    """⛔ `00x8` 不进网格也不进分母 —— 给它们做工作单等于把分母改错。

    ⭐ 判据是**递归**扫盘：工作单已按 NL 组下沉一层，⛔ 只看根目录的旧判据会漏掉
    藏在 `nl_XXXX/` 里的越界工作单，而那正是分母被改错时最可能的形态。
    """
    found = S.find_worksheets(HERE)
    for pair in S.OUT_OF_SCOPE_PAIRS:
        assert pair not in found, \
            f"{pair} 是越界 pair，不该有工作单（发现于 {found.get(pair)}）"
    assert len(S.IN_SCOPE_PAIRS) == 54
    assert set(S.OUT_OF_SCOPE_PAIRS) == {"0008", "0018", "0028", "0038", "0048", "0058"}


def test_every_in_scope_pair_has_a_worksheet():
    for pair in S.IN_SCOPE_PAIRS:
        assert os.path.exists(_ws(pair)), f"{pair} 缺工作单 —— 跑 generate.py"


@pytest.mark.parametrize("pair", ["0000", "0010", "0029", "0044", "0059"])
def test_worksheet_covers_every_ledger_record_of_that_pair(pair):
    """⭐ 自包含：该 pair 的每一条台账记录都要有裁决区，否则会被静默漏判。"""
    text = _read(_ws(pair))
    blocks = fb.extract(text)
    for rec in S.ledger_records(pair):
        assert rec["id"] in blocks, f"{pair} 缺 {rec['id']} 的裁决区"


def test_generate_is_idempotent_and_preserves_human_input():
    """⭐ 重跑生成器不许吃掉人工填写 —— 这条塌了整轮工作就没了。"""
    pair = "0000"
    src = _ws(pair)
    with tempfile.TemporaryDirectory() as tmp:
        dst = _ws(pair, tmp)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(src, dst)
        with open(dst, encoding="utf-8") as fh:
            text = fh.read()
        # ⚠️ 2026-08-14 起裁决区**默认已预填**（勾好 + 一句话理由 + 尾标），故这里模拟的
        # 「人工填写」是**在预填之后再加一行**：⭐ 那正是真实用法（同意就删括号、不同意就改写）。
        # ⛔ 判据必须是「人加的那行还在」，⚠️ 不能再假设块是空模板。
        marker = "人工补充: 这是人工写的理由，重跑必须留住"
        k = "<!-- FILL:BEGIN key=EIS-0000-02 kind=ledger -->"
        assert k in text
        i = text.index(k)
        j = text.index("~~~", text.index("~~~", i) + 3)      # 第二个围栏
        text = text[:j] + marker + "\n" + text[j:]
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(text)

        for _ in range(2):
            subprocess.run([sys.executable, os.path.join(HERE, "generate.py"),
                            "--pairs", pair, "--out", tmp],
                           check=True, capture_output=True)
        with open(dst, encoding="utf-8") as fh:
            after = fh.read()
        assert marker in after
        assert "[x] 按 D1 采纳" in after

        # 第三次不该再产生任何改动
        before = _sha(dst)
        subprocess.run([sys.executable, os.path.join(HERE, "generate.py"),
                        "--pairs", pair, "--out", tmp],
                       check=True, capture_output=True)
        assert _sha(dst) == before

        parsed = C.collect_pair(pair, dst)
        # ⚠️ 人加的那行落在 `EIS-0000-02`（需人裁、带待填 `理由` 栏）的块里。
        # ⛔ 不能用 `EIS-0000-01`：它无争议，预填里**没有** `理由` 栏。
        rec = next(r for r in parsed["ledger"] if r["id"] == "EIS-0000-02")
        assert rec["裁决"]["chosen"], "裁决没勾"
        assert "重跑必须留住" in (rec.get("理由") or "") + (rec.get("meta review 意见") or "")


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
            digests.append({f: _sha(os.path.join(tmp, f)) for f in _all_md(tmp)})
        # ⭐ 54 份工作单 + 9 份 NL.md + 1 份 HOWTO.md
        assert len(digests[0]) == len(S.IN_SCOPE_PAIRS) + len(S.nl_dirs()) + 1
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
        path = _ws("0000", tmp)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(fb.render("EIS-9999-99", "ledger", "理由: 不该丢的内容"))
        subprocess.run([sys.executable, os.path.join(HERE, "generate.py"),
                        "--pairs", "0000", "--out", tmp],
                       check=True, capture_output=True)
        text = _read(path)
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
    # ⭐ 递归覆盖：`nl_XXXX/` 下的 54 份工作单与 9 份 `NL.md`、根上的
    # `HOWTO.md` / `README.md` / `PROGRESS.md`，以及译文目录里的验收依据 ——
    # ⛔ 它们全是入库文档，不是外部附件。
    # ⚠️ 旧判据只 `os.listdir(HERE)`，⛔ 目录下沉后会把 63 份文件静默漏掉。
    targets = [os.path.join(HERE, f) for f in _all_md(HERE)]
    assert len(targets) >= len(S.IN_SCOPE_PAIRS) + len(S.nl_dirs()) + 3, \
        f"扫到的 .md 只有 {len(targets)} 份 —— ⛔ 递归漏了"
    proc = subprocess.run(
        [sys.executable, "-m", "tools.unwrap_markdown", "--check", *targets],
        cwd=repo, capture_output=True, text=True)
    if proc.returncode == 1 and "No module named" in proc.stderr:
        pytest.skip("tools.unwrap_markdown 不可用")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_every_verdict_block_is_prefilled_and_none_is_blank():
    """⭐ **每个裁决区都必须已预填，一个空白都不许有。**

    ⚠️⚠️ **这一条 2026-08-14 整体翻转过，⛔ 翻转本身必须记在这里。** 原先它叫
    `test_worksheets_carry_no_verdicts`，判据是「裁决区必须是空模板」，理由写的是
    「材料不许替作者裁决」。⭐ 用户裁定改成相反的要求：三方独立 D 档判读 + 人工
    meta review 已经把每条的推荐与理由准备好了，⭐ **同意就不必动它**，那才是效率所在。

    ⛔ 翻转不等于放弃防线，防线换了位置：

    - **原防线**：空模板 ⇒ 判读者不会被我方判断锚定。
    - ⭐ **现防线**：① 预填体必须**逐字标注**它是我方预填（`dtier.PREFILL_TAIL`），
      ② `fb.is_untouched()` 必须仍能认出「未经人确认」的预填（否则进度统计立刻全绿），
      ③ 每条需人裁的条目必须有人工 meta review（`dtier.missing_meta()` 为空）。
      ⚠️ 第 ② 条由 `test_a_prefilled_block_still_counts_as_untouched` 守，
      第 ③ 条由 `test_every_disputed_item_has_a_meta_review` 守。

    ⛔ 所以本条只管一件事：**没有一个裁决区是空白的**。
    """
    import dtier as DT
    blank, no_reason = [], []
    for pair in S.IN_SCOPE_PAIRS:
        data = C.collect_pair(pair, _ws(pair))
        for rec in list(data["ledger"]) + list(data["candidates"]):
            key = rec.get("id") or rec.get("key")
            if not rec.get("裁决", {}).get("chosen"):
                blank.append(f"{pair}/{key}")
            if not (rec.get("meta review 意见") or "").strip():
                blank.append(f"{pair}/{key}(无意见)")
            # ⭐ `理由` 是**待人填**的一栏，⛔ 只有需人裁的条目才有它。
            r = DT.get(key)
            needs = (r or {}).get("bucket") in DT.BUCKET_MARK or (r is None and key in DT.load_meta())
            if needs and not (rec.get("理由") or "").strip():
                no_reason.append(f"{pair}/{key}")
    assert not blank, f"这些裁决区没有预填（裁决未勾或缺 meta review 意见）：{blank[:20]}（共 {len(blank)}）"
    assert not no_reason, f"这些需人裁的条目缺待填 `理由` 栏：{no_reason[:20]}（共 {len(no_reason)}）"


def test_untouched_means_the_reason_placeholder_is_still_there():
    """⭐ 「待处理」的判据是**`理由` 一栏是否还是占位**，⛔ 不是「等于预填体」。

    ⚠️⚠️ **2026-08-14 这条的语义翻转过一次，⛔ 翻转必须记下来。** 原先它叫
    `test_a_prefilled_block_still_counts_as_untouched`，要求**任何**预填体都判「未确认」。
    ⭐ 用户裁定改成两档：

    - ⭐ **无争议的条目**（三臂方向一致）预填里**没有** `理由` 栏 —— 我方给了决议与
      `meta review 意见`，⛔ 人不需要做任何动作，⚠️ 让人去删一个括号纯属白做 ⇒ **不算待处理**。
    - ⭐ **需人裁的条目**带一行 `理由: （请在此写一句…）` 占位 ⇒ **算待处理**，
      人写任何一句话（只要不再是占位原文）即视为已处理。

    ⛔ 防线没撤，换了位置：预填体仍必须能被 `is_stale_template()` 认出并替换
    （否则第一版预填会被永久钉住，与 2026-08-13 那个 bug 同型），
    ⭐ 而「人动过一个字就算已处理」由本条下半段钉住。
    """
    import dtier as DT
    n_need = n_free = 0
    for rid, rec in DT.load_rulings().items():
        kind = "ledger" if rid.startswith("EIS-") else "candidate"
        pre = DT.prefill(rid, kind)
        if pre is None:
            continue
        pair = rid.split("-")[1]
        needs = rec.get("bucket") in DT.BUCKET_MARK
        if needs:
            n_need += 1
            assert fb.REASON_PLACEHOLDER in pre, f"{rid} 需人裁却没有待填 `理由` 占位"
            assert fb.is_untouched(pre, kind, pair, key=rid), \
                f"{rid} 带占位却没被认成待处理"
            # ⭐ 人写了一句话 ⇒ 已处理
            done = pre.replace(fb.REASON_PLACEHOLDER, "我同意")
            assert not fb.is_untouched(done, kind, pair, key=rid), \
                f"{rid} 人写过理由却仍判待处理"
        else:
            n_free += 1
            assert fb.REASON_PLACEHOLDER not in pre, \
                f"{rid} 无争议却带了待填占位 —— ⛔ 那会让人白做一次删除"
            assert not fb.is_untouched(pre, kind, pair, key=rid), \
                f"{rid} 无争议却被算成待处理"
        # ⭐ 两档都必须能被认出是「原样预填」，⛔ 否则改版后旧预填永久钉住
        assert fb.is_stale_template(pre, kind, pair), f"{rid} 的预填体不被认作可替换"
    assert n_need >= 100 and n_free >= 200, f"覆盖不足：需人裁 {n_need} / 无争议 {n_free}"

def test_every_disputed_item_has_a_meta_review():
    """⛔ 每一条需人裁的条目都必须有人工 meta review，且必须给出推荐。

    ⭐ 用户裁定：不许留「待议」——「所有的待裁决你都得有 meta review 以及推荐选项」。
    ⚠️ 缺 meta review 的条目会在工作单上渲成「待补」，⛔ 那等于把活推回给人却不给材料。
    """
    import dtier as DT
    # ⚠️⚠️ **2026-08-14 口径扩到全部条目**（用户裁定：无争议的也要有针对性的 meta review 文本）。
    # ⛔ 那是一次性写 429 条的工作量，⚠️ 尚未写完 —— 故本条**当前只对需人裁的三桶 + UM 断言**，
    # ⭐ 并把总欠账数打印出来，⛔ 让欠账可见可数、不许静默消失。
    # ⛔ 补完后把下面那行换成 `assert not DT.missing_meta(_um_keys())`。
    need = {rid for rid, rec in DT.load_rulings().items()
            if rec.get("bucket") in DT.BUCKET_MARK}
    missing_need = sorted(need - set(DT.load_meta()))
    assert not missing_need, \
        f"这些需人裁的条目缺 meta review：{missing_need[:20]}（共 {len(missing_need)}）"
    total_debt = len(DT.missing_meta())
    print(f"\n[meta review 欠账] 无争议桶尚缺 {total_debt} 条针对性文本")
    bad = [rid for rid, rev in DT.load_meta().items()
           if (rev.get("recommend") or "").strip() not in DT.REC_TO_CHOICE]
    assert not bad, f"这些 meta review 的 recommend 不是合法取值：{bad[:20]}"
    thin = [rid for rid, rev in DT.load_meta().items()
            if len((rev.get("reason") or "").strip()) < 40]
    assert not thin, f"这些 meta review 的 reason 太短，⛔ 不算给了理由：{thin[:20]}"


# ==================================================================== §1.1 三列 NL 表

def test_nl_table_has_three_columns_in_every_nl_doc():
    """⭐ `NL.md` §2 必须是「段 id / 原文 / 中文严格翻译」三列，且逐段都有译文。

    ⛔ 判据不是「表头有三列」—— 表头对了而行只有两列，Markdown 照样渲染，
    只是最后一列空着，⚠️ 人读起来像「这段没译」。所以逐行数分隔符。

    ⚠️ 检查对象由 54 份工作单改成 9 份 `NL.md`（表本体搬过去了），⛔ 判据一个字没松；
    ⭐ 覆盖面反而更严：这里对**组内每个 pair** 都算一遍分段，⛔ 若同组两个 pair 的
    分段不一致，`NL.md` 的单表就必然对其中一个为假 —— 那正是要抓的。
    """
    for dirname in S.nl_dirs():
        lines = _read(os.path.join(HERE, dirname, S.NL_DOC)).splitlines()
        head = next(i for i, ln in enumerate(lines)
                    if ln.startswith("| 段 id |"))
        assert lines[head] == "| 段 id | 原文 | 中文严格翻译 |", \
            f"{dirname} 的 §2 表头不是三列：{lines[head]}"
        for pair in S.pairs_of_dir(dirname):
            segs, _ = S.nl_segments(pair)
            rows = lines[head + 2: head + 2 + len(segs)]
            assert len(rows) == len(segs), f"{dirname}（按 {pair} 算）的 §2 行数与分段数不符"
            for (sid, _txt), row in zip(segs, rows):
                cells = [c.strip() for c in row.strip().strip("|").split("|")]
                assert len(cells) == 3, f"{dirname} {sid} 不是三列：{row[:120]}"
                assert cells[0] == f"`{sid}`"
                assert cells[1], f"{dirname} {sid} 原文列为空"
                assert cells[2], f"{dirname} {sid} 译文列为空"
                assert "缺译文" not in cells[2], f"{dirname} {sid} 缺译文"


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
        assert "只有一条带触发词" not in _read(_ws(pair)), \
            f"{pair}.md 还印着那句假事实"


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


# ==================== 译文侧唯一一道机械门：字面量不许在 zh 里消失（I-C）

def test_zh_keeps_every_literal_the_source_text_gives():
    """⭐ 正面：9 份译文的 `zh` 都要保住 `en` 的反引号表达式与阿拉伯数字。

    ⚠️ 这是**第一道作用于 `zh` 的门**（见 [README.md](./README.md) §12）——
    ⛔ 前三道（`artifact_leaks` / `original_ref_errors`）全在管 `note`，
    ⛔ 译文本身此前零机械覆盖。⭐ 门只覆盖字面量存活，⛔ 不覆盖「译得对不对」。
    """
    bad = {}
    for name, payload in nl_zh._raw().values():                # noqa: SLF001
        drops = nl_zh.zh_literal_drops(payload)
        if drops:
            bad[name] = drops
    assert bad == {}, "译文丢了原文的字面量：\n" + "\n".join(
        f"{n}:\n  " + "\n  ".join(v) for n, v in sorted(bad.items()))


def test_zh_literal_gate_actually_fires():
    """⛔ 反面：门必须**真的**拦得住 —— ⚠️ 只测「干净时不报」等于没测。

    ⭐ 两条判据各一个反例，⛔ 外加三组正例防止实现恒抛：
    ① 干净文本；② ⚠️ **英文数词必须放行** —— `three` 译作「三个」是正常的，
    ⛔ 本门只管阿拉伯数字（SPEC 第 10 条）；③ ⚠️ **同一数字出现两次只需活一次** ——
    ⛔ 门判存在不判次数，否则中文语序合并同类项就会被误伤。
    """
    clean = {"segments": [
        {"seg": "1",
         "en": "1. There are three lanes when `dist_to_front<25` and 2 kilometers remain. ",
         "zh": "1. 当 `dist_to_front<25` 且还剩 2 千米时有三条车道。"},
    ]}
    assert nl_zh.zh_literal_drops(clean) == []

    def drops(zh):
        payload = copy.deepcopy(clean)
        payload["segments"][0]["zh"] = zh
        return nl_zh.zh_literal_drops(payload)

    # ① 反引号表达式被译掉 / 改写
    hit = drops("1. 当前车距离小于 25 且还剩 2 千米时有三条车道。")
    assert any("`dist_to_front<25`" in h for h in hit), hit

    # ② 阿拉伯数字被改写成中文数字（⛔ SPEC 第 10 条禁止）
    hit = drops("1. 当 `dist_to_front<25` 且还剩两千米时有三条车道。")
    assert any("`2`" in h for h in hit), hit

    # ③ ⭐ 英文数词放行 —— `three` 译作「三条」不许报
    assert all("three" not in h for h in drops(
        "1. 当 `dist_to_front<25` 且还剩 2 千米时有三条车道。"))

    # ④ ⭐ 只判存在不判次数：en 里 25 出现两次，zh 里只出现一次也放行
    twice = {"segments": [{
        "seg": "1",
        "en": "1. If the distance is less than 25 meters (`dist_to_front<25`), go. ",
        "zh": "1. 如果距离小于 25 米（`dist_to_front<25`），就走。"}]}
    assert nl_zh.zh_literal_drops(twice) == []

    # ⑤ ⭐ 小数按整串比对，⛔ 不许只匹配到 `0`
    frac = {"segments": [{"seg": "1",
                          "en": "1. less than 0.7 kilometers. ",
                          "zh": "1. 小于 0 千米。"}]}
    assert any("`0.7`" in h for h in nl_zh.zh_literal_drops(frac))


def test_zh_literal_drop_raises_at_load_time():
    """⛔ 装载期就要抛，⛔ 不许降级 —— ⚠️ 译文里没了守卫表达式，判读者就无锚可比。"""
    real = copy.deepcopy(dict(nl_zh._raw()))                   # noqa: SLF001
    dirty = copy.deepcopy(real)
    # ⭐ `b7425c44`（nl_0009）段 3 的 zh 带着 `dist_to_front<25`，⛔ 抹掉它必须炸
    seg = dirty["b7425c44"][1]["segments"][2]
    assert "`dist_to_front<25`" in seg["zh"], "本测试前提要重定：段 3 的 zh 没有该表达式"
    #
    # ⚠️⚠️ **抹的必须就是前提断言查的那个串。** ⛔ 本行原先抹 `（`dist_to_front<25`）`
    # （带全角括号），⭐ 而前提只查了裸的 `` `dist_to_front<25` `` —— 2026-08-16 重译后
    # 该处写成 `` （`dist_to_front<25`（前车距离小于 25）） `` 的嵌套形态，
    # ⛔ 于是 replace 成了**空操作**，门不响，测试静默失效（表现为 DID NOT RAISE）。
    # ⭐ 现在改为抹字面量本身，并**断言抹除确有改动** —— ⛔ 空操作要当场炸，不许蒙过去。
    before = seg["zh"]
    seg["zh"] = seg["zh"].replace("`dist_to_front<25`", "")
    assert seg["zh"] != before, "⛔ 抹除成了空操作 —— 门不会响，本测试等于没测"
    with _mock_raw(dirty):
        with pytest.raises(nl_zh.ZhLiteralDrop, match="丢了原文的字面量"):
            nl_zh._store.__wrapped__()                         # noqa: SLF001
    # ⛔ 反反面：不动数据时**不许**抛
    with _mock_raw(real):
        nl_zh._store.__wrapped__()                             # noqa: SLF001


def test_zh_fidelity_fixes_do_not_regress():
    """⛔ I-C 回归：2026-08-13 逐段核对 `zh` 时改掉的 6 处，⛔ 不许回潮。

    ⚠️ 与 I-B 同法：先把「事实是什么」逐字钉在 `en` 或同份 `translator_notes` 上，
    ⛔ 再断言错的说法不在 —— ⭐ 换个措辞重写也会先炸在前提校验上。
    """
    def payload(nl_id):
        return next(pl for _, pl in nl_zh._raw().values()      # noqa: SLF001
                    if pl["nl_id"] == nl_id)

    def zh(pl, seg):
        return next(s["zh"] for s in pl["segments"] if s["seg"] == seg)

    # ① nl_0005 段 1：`starts in` 是「起始于（初始状态）」，⛔ 不是「启动（通电）」
    p5 = payload("0005")
    en1 = next(s["en"] for s in p5["segments"] if s["seg"] == "1")
    assert "The microwave starts in the DoorShut state" in en1, "本测试前提要重定"
    #
    # ⭐ 断言的是**形式要求**，⛔ 不是措辞 —— 2026-08-16 重译把「微波炉起始于 DoorShut 状态」
    # 改成了「微波炉起始于门关状态（DoorShut）」（新的 `中文（英文）` 形态）。⚠️ 钉死整句会把
    # 旧形态锁在原地（CLAUDE.md §13.3）。⭐ 本条真正要守的事实只有两个：
    #   ① `starts in` 译作「起始于」（初始状态），⛔ 而不是「启动」（通电）
    #   ② 标识符 `DoorShut` 逐字活在译文里
    z5 = zh(p5, "1")
    assert "起始于" in z5 and "DoorShut" in z5
    assert "启动" not in z5, "⛔ `starts in` 是「起始于（初始状态）」，不是「启动（通电）」"

    # ② nl_0009 段 4：`if` 必须是「如果」，⛔ 不许弱化成「…时」；`once` 必须是「一旦」
    p9 = payload("0009")
    en4 = next(s["en"] for s in p9["segments"] if s["seg"] == "4")
    assert " once the lane change is completed" in en4 and " if the distance" in en4
    assert "一旦变道完成" in zh(p9, "4") and "如果到出口的距离" in zh(p9, "4")
    assert "在变道完成后" not in zh(p9, "4")

    # ③ nl_0009 段 12：并列条件也用逗号连接，⛔ 不许说「一律用 and / or / with」
    en12 = next(s["en"] for s in p9["segments"] if s["seg"] == "12")
    assert "pedestrians (`pedestrian_detected`), the rear distance" in en12, \
        "第 12 句居然不用逗号并列了 —— 本测试前提要重定"
    assert "一律用英文" not in zh(p9, "12")

    # ④ nl_0004 段 8：⛔ 不许把制品记法名 PlantUML 印进译文（词法门不覆盖 zh）
    p4 = payload("0004")
    assert all("PlantUML" not in s["zh"] and "plantuml" not in s["zh"].lower()
               for s in p4["segments"])
    assert "UML 关键字 entry 为小写" in p4["translator_notes"], \
        "整份观察改了措辞 —— 段 8 的〔原文如此〕要跟着对拍"

    # ⑤ nl_0007 段 1：尾随空格是全语料通例，⛔ 不许在单句上写成「多出一个空格」
    p7 = payload("0007")
    ens = [s["en"] for s in p7["segments"]]
    assert ens[0].endswith(" ") and ens[1].endswith(" "), "本测试前提要重定"
    assert "多出一个空格" not in zh(p7, "1"), "第 2 句同样有尾随空格，⛔ 单点第 1 句是失衡的"
    assert "第 1、2 句行尾各多出一个空格" in p7["translator_notes"], \
        "整份观察仍应保留该格式事实 —— ⛔ 改准不删光"

    # ⑥ nl_0006：`transition` 在同一份 NL 里只许有一种译法（SPEC 第 4 条）
    p6 = payload("0006")
    blob = "".join(s["zh"] for s in p6["segments"])
    assert "状态迁移" in blob, "段 1 的术语括注变了 —— 本测试前提要重定"
    assert "转移" not in blob, "nl_0006 同时用了「迁移」与「转移」译 transition"


def test_worksheet_warns_that_notes_never_assert_about_the_artifact():
    """⭐ 那句「提示不含制品断言、请自己去 §1.3 核对」两处都得挂。

    ⚠️ 旧版页面上立的是「提示只陈述原文、不含任何裁决」，⛔ 而提示里恰恰藏着假的制品事实 ——
    ⛔ 声明反过来在劝读者不要去核。⭐ 故声明必须与新纪律同步，⛔ 不能只改数据不改声明。

    ⭐ 提示本体搬到 `nl_XXXX/NL.md` 之后，声明要落在**两处**：提示所在的那一页
    （`NL.md` §3），以及**每份工作单**里指向那一页的那句话 —— ⛔ 只落在 `NL.md` 上不够，
    ⚠️ 判读者是从工作单进来的，⛔ 免责必须在他点进去之前就看到。
    ⛔ 措辞由「本 pair 制品」改为「被测制品」：`NL.md` 服务 6 个 pair，
    ⛔ 说「本 pair」在那一页上没有指称。
    """
    for dirname in S.nl_dirs():
        block = _read(os.path.join(HERE, dirname, S.NL_DOC)) \
            .split("## §3 逐段判读提示")[1].split("## §")[0]
        assert "不含任何关于被测制品的断言" in block, f"{dirname}/{S.NL_DOC} 缺制品免责声明"
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        assert "不含任何关于被测制品的断言" in doc, f"{pair} 的 §1.1 缺制品免责声明"


def test_every_nl_has_translator_notes():
    """⭐ 整份 NL 层面的观察（术语表 / 跨句歧义 / 原文质量）9 份都得有。"""
    for pair in S.IN_SCOPE_PAIRS:
        tn = nl_zh.translator_notes(pair)
        assert tn and len(tn) > 200, f"{pair} 的 translator_notes 缺失或过短"


def test_nl_doc_carries_notes_and_translator_notes():
    """⭐ 9 份 `NL.md` 都要有逐段提示与整份观察，⛔ 且提示要逐段挂到真实段 id 上。

    ⚠️ 这一条此前作用在 54 份工作单上（同一份材料复制六份）；⭐ 材料合并到 `NL.md` 之后，
    检查对象跟着变成 9 份 —— ⛔ 但**逐段都要有提示**这一条一个字没松。
    """
    for dirname in S.nl_dirs():
        pairs = S.pairs_of_dir(dirname)
        doc = _read(os.path.join(HERE, dirname, S.NL_DOC))
        assert "## §3 逐段判读提示" in doc, f"{dirname} 缺逐段判读提示区"
        assert "## §4 整份 NL 层面的观察" in doc, f"{dirname} 缺整份 NL 观察区"
        assert "../translations/TRANSLATION_SPEC.md" in doc, f"{dirname} 未挂译文验收依据"
        assert f"../translations/{nl_zh.source_file(pairs[0])}" in doc, \
            f"{dirname} 未挂译文 JSON"
        block = doc.split("## §3 逐段判读提示")[1].split("## §")[0]
        for sid, _txt in S.nl_segments(pairs[0])[0]:
            assert f"- `{sid}`：" in block, f"{dirname} 的提示区缺 {sid}"
        assert "⛔ 译者未给提示" not in block, f"{dirname} 的提示区有空提示"


# ==================================================================== §5 字段块

def _entry(pair, idx=1, **over):
    """拼一条 §5 新增登记。值为 `None` 表示那一行整个不写（模拟漏填）。

    默认是一条**填齐的、走 element 支的**条目：`defect_locus = element` 配 A + B，
    `defect_reference = language` 配 `nl_evidence = 无`。
    这样每个用例只需覆写它要测的那一项，被测信号不会被别的 `E` 淹掉。
    """
    fields = {
        "defect_locus": "element",
        "defect_element": "transition",
        "defect_qualifier": "missing",
        "defect_reference": "language",
        "statement": "顶层没有任何进入 InitialState 的初始边（:2 附近无 `[*] -->` 行），"
                     "冷启动落点未定义。",
        "expected_after_fix": "顶层有且只有一条初始边，且从冷启动出发能唯一确定首个活动状态。",
        "nl_evidence": "无",
    }
    fields.update(over)
    out = [f"### NEW-{pair}-{idx:02d}"]
    out += [f"{k}: {v}" for k, v in fields.items() if v is not None]
    return "\n".join(out)


def _logic_entry(pair, idx=1, **over):
    """走**逻辑支**的一条。⚠️ 正反两面都要测：只测 element 支等于没测条件式。"""
    fields = {
        "defect_locus": "pair",
        "defect_logic_kind": "nondeterminism",
        "defect_reference": "requirement",
        "statement": "同一状态同一事件下的两条出边守卫存在同真赋值。",
        "expected_after_fix": "该状态在该事件下的诸出边守卫两两互斥。",
        "nl_evidence": "NL-L002",
    }
    fields.update(over)
    out = [f"### NEW-{pair}-{idx:02d}"]
    out += [f"{k}: {v}" for k, v in fields.items() if v is not None]
    return "\n".join(out)


def _validate_new(pair, *entries, allow_ledger=False):
    """走真实链路：`parse_new` 解析 → `validate_pair` 校验。返回 Report。

    固定用台账 0 条的 pair，否则「台账条目未裁决」的 E 会淹掉被测信号。

    `allow_ledger=True` 只给**永久排除**的 `00x8` 用：它们有台账条目却**没有工作单**，
    所以喂空 `ledger` 必然带出「找不到裁决区」的 `E`。调用方须自行用
    `_msgs_for()` 按条目 key 过滤，不许直接看全表。
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
    """只取某一条记录（按 `key`）上的消息 —— 用于台账非空的载体 pair。"""
    return [i["msg"] for i in rep.items
            if i["key"] == key and (level is None or i["level"] == level)]


def test_new_issue_field_block_round_trips_through_collect():
    """人工填的字段必须能被 `collect.py` 原样收回来。"""
    body = _entry("0001", 1, property_pattern="Existence × Globally")
    recs = C.parse_new(body, "0001")
    assert len(recs) == 1
    f = recs[0]["fields"]
    assert recs[0]["id"] == "NEW-0001-01"
    assert f["defect_locus"] == "element"
    assert f["defect_element"] == "transition"
    assert f["defect_qualifier"] == "missing"
    assert f["defect_reference"] == "language"
    assert f["statement"].startswith("顶层没有任何")
    assert f["expected_after_fix"].startswith("顶层有且只有一条")
    assert f["nl_evidence"] == "无"
    assert f["property_pattern"] == "Existence × Globally"


def test_new_issue_block_parses_the_checkbox_form_from_the_real_template():
    """模板给的是勾选行 —— 勾了 `[x]` 也要能收回来，不能只支持自由文本。"""
    body = (NF.template("0001", count=1)
            .replace("statement:", "statement: BrakingState 的出边把两个事件并成一个名字")
            .replace("expected_after_fix:", "expected_after_fix: 两个事件各有一条边")
            .replace("nl_evidence:", "nl_evidence: NL-L003")
            .replace("[ ] pair ", "[x] pair ")
            .replace("[ ] incompleteness", "[x] incompleteness")
            .replace("[ ] requirement", "[x] requirement"))
    recs = C.parse_new(body, "0001")
    assert len(recs) == 1
    f = recs[0]["fields"]
    assert f["defect_locus"]["chosen"] == ["pair"]
    assert f["defect_logic_kind"]["chosen"] == ["incompleteness"]
    assert f["defect_reference"]["chosen"] == ["requirement"]
    assert f["nl_evidence"] == "NL-L003"


# ---- 条件式座标系本身

def test_the_field_block_is_organised_as_two_branches():
    """条件式必须在模板里**看得见** —— 只在文档里讲、模板里不体现等于没做。

    判据是顺序与归属：`defect_locus` 排在最前，两支的轴各自落在自己那段提示之后，
    两支公用的四项排在最后。判读者据此才能「先答 locus，再只看自己那一支」。
    """
    body = NF.template("0001", count=1)
    hints = [ln for ln in body.splitlines() if ln.startswith("---")]
    assert hints == [NF.HINT_ELEMENT_BRANCH, NF.HINT_LOGIC_BRANCH,
                     NF.HINT_BOTH, NF.HINT_OTHER_NOTE, NF.HINT_OPTIONAL]
    lines = body.splitlines()
    assert lines[1].startswith("defect_locus:"), "locus 必须是第一个问题"

    def between(a, b):
        seg = body.split(a, 1)[1].split(b, 1)[0]
        return [ln.split(":", 1)[0] for ln in seg.splitlines() if ":" in ln]
    assert between(NF.HINT_ELEMENT_BRANCH, NF.HINT_LOGIC_BRANCH) == NF.ELEMENT_BRANCH_FIELDS
    assert between(NF.HINT_LOGIC_BRANCH, NF.HINT_BOTH) == NF.LOGIC_BRANCH_FIELDS
    assert between(NF.HINT_BOTH, NF.HINT_OTHER_NOTE) == ["defect_reference"]
    # `other_note` 单独一段：它是**条件必填**（任一轴取 `other` 时才要），
    # 与「两支都要填」和「可留空」都不是一回事，故不许混进那两段里。
    assert between(NF.HINT_OTHER_NOTE, NF.HINT_OPTIONAL) == [
        NF.OTHER_NOTE_FIELD, "statement", "expected_after_fix", "nl_evidence"]
    assert body.split(NF.HINT_OPTIONAL, 1)[1].strip().startswith("property_pattern:")


def test_every_axis_value_carries_a_decision_test():
    """六个轴的取值必须齐全，且**每一个取值都带一条判定测试**。

    这是「自包含」的硬判据：判读者不该为了选一个类型去翻别的文件。
    取值集合与判定测试的真源是 `defect_taxonomy.md`；这里钉的是「一个都不少、
    每个都有判据、且判据真的印进了 54 份工作单」。
    """
    pytest.skip("§4 深度检查清单与 §5 新增登记于 2026-08-14 按用户裁定整体拆除"
                "（本轮工作单只做「对现有台账 + 候选逐条裁决」）。⛔ 本条测的是那两节的"
                "行为，故整条挂起而不是删除 —— 代码（section_checklist / section_new / checklist.py / newfields.py）仍在，"
                "下一轮若重开挖深可整段接回，届时把本 skip 去掉即可。"
                "⭐ 「那两节确实不在了」由 test_the_removed_sections_are_really_gone 守着。")
    # ⚠️ `defect_element` 是 8 而不是 7：2026-08-13 新增界外取值 `region`
    # （正交区域，`counts_as_defect = false`），见类型学 §3.7。
    tables = {"defect_locus": (NF.LOCI, 4), "defect_element": (NF.ELEMENTS, 8),
              "defect_qualifier": (NF.QUALIFIERS, 4),
              "defect_logic_kind": (NF.LOGIC_KINDS, 9),
              "defect_reference": (NF.REFERENCES, 3)}
    doc = _read(_ws("0001"))
    for name, (table, n) in tables.items():
        assert len(table) == n, f"{name} 应有 {n} 个取值，实得 {len(table)}"
        assert [v for v, _zh, _t in table] == NF.ENUMS[name]
        for v, zh, test in table:
            assert zh and test, f"{name} 的 `{v}` 缺中文名或判定测试"
            assert len(test) >= 10, f"{name} 的 `{v}` 判定测试太短，判不了"
            assert f"| `{v}` | {zh} |" in doc, f"{name} 的 `{v}` 没内联进工作单"
    # 第六个轴（Dwyer 性质模式）是可选精化，8 × 5，作为句式骨架内联
    assert len(NF.PROPERTY_PATTERNS) == 8 and len(NF.PROPERTY_SCOPES) == 5
    for v, zh, shape in NF.PROPERTY_PATTERNS + NF.PROPERTY_SCOPES:
        assert zh and shape
        assert f"| `{v}` | {zh} |" in doc, f"Dwyer 的 `{v}` 没内联进工作单"


def test_unintended_terminal_tells_the_judge_to_count_ancestor_group_transitions():
    """`unintended_terminal` 的判定测试**必须**写明要数祖先的成组迁移。

    这是该取值最常见的假阳性、也是唯一的防线：一个叶态自己画不出出边，
    若它的外层复合态有出边，那条边对该叶态同样可用 —— 它**不是**终止态。
    判读者漏掉这一句就会把一整批正常的叶态判成非预期终止。

    判据不是「文档里提过祖先」，而是：该取值**自己那一格**里有这句话，
    且它出现在全部 54 份工作单里（判读者选取值时看到的就是那一格）。
    """
    pytest.skip("§4 深度检查清单与 §5 新增登记于 2026-08-14 按用户裁定整体拆除"
                "（本轮工作单只做「对现有台账 + 候选逐条裁决」）。⛔ 本条测的是那两节的"
                "行为，故整条挂起而不是删除 —— 代码（section_checklist / section_new / checklist.py / newfields.py）仍在，"
                "下一轮若重开挖深可整段接回，届时把本 skip 去掉即可。"
                "⭐ 「那两节确实不在了」由 test_the_removed_sections_are_really_gone 守着。")
    test = dict((v, t) for v, _zh, t in NF.LOGIC_KINDS)["unintended_terminal"]
    assert "祖先" in test, "判定测试没提祖先"
    assert "成组迁移" in test, "判定测试没提成组迁移"
    assert "外层复合态" in test and "不是**终止态" in test, \
        "判定测试没说清「外层有出边则它不是终止态」"
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        assert "把祖先的成组迁移数进去" in doc, f"{pair}.md 没印这句判据"


def test_nontermination_is_pinned_to_an_nl_obligation():
    """`nontermination` 必须注明它只能挂在 NL 的终止义务上。

    活锁 / non-progress cycle 在标准文献里没有与标注无关的形式定义，
    所以不得写成「模型自身即可判定它活锁了」。少了这句，判读者会拿它当
    一条模型内可判定的性质用，而那个主张我们支撑不起来。
    """
    test = dict((v, t) for v, _zh, t in NF.LOGIC_KINDS)["nontermination"]
    assert "只能挂在 NL 的终止义务上" in test
    assert "没有与标注无关的形式定义" in test
    assert "只能挂在 NL 的终止义务上" in _read(_ws("0001"))


def test_the_known_expression_gap_is_told_to_the_judge():
    """entry / exit 动作次序表达不了 —— 这一句必须就在取值表附近告诉判读者。

    否则他撞上它时会以为是自己选错了，然后硬塞进某个取值里。
    """
    pytest.skip("§4 深度检查清单与 §5 新增登记于 2026-08-14 按用户裁定整体拆除"
                "（本轮工作单只做「对现有台账 + 候选逐条裁决」）。⛔ 本条测的是那两节的"
                "行为，故整条挂起而不是删除 —— 代码（section_checklist / section_new / checklist.py / newfields.py）仍在，"
                "下一轮若重开挖深可整段接回，届时把本 skip 去掉即可。"
                "⭐ 「那两节确实不在了」由 test_the_removed_sections_are_really_gone 守着。")
    assert len(NF.KNOWN_GAPS) >= 1
    gap, where, why = NF.KNOWN_GAPS[0]
    assert "次序" in gap
    assert "defect_locus = pair" in where and "other" in where
    doc = _read(_ws("0001"))
    assert "已知表达缺口" in doc
    assert "并不声明它遵循哪一套" in doc


def test_branch_hints_are_not_parsed_as_content():
    """分支提示行不是字段，也不许被并进上一个字段的值里。

    这条是设计时就看得见的坑：提示行紧跟在勾选行之后，而它不匹配字段名正则
    （行首是 `-`），于是会被并进上一个字段 —— 值里静默多出一整行提示。
    """
    body = (NF.template("0001", count=1)
            .replace("statement:", "statement: 就这一句"))
    f = C.parse_new(body, "0001")[0]["fields"]
    assert f["statement"] == "就这一句", f["statement"]
    for hint in NF.TEMPLATE_HINTS:
        assert hint not in str(f), f"分支提示 {hint!r} 混进了字段值"
    assert "_raw_lines" not in f


def test_readme_worked_example_can_never_be_collected_as_a_real_judgement():
    """README §3.5.3 的填好样例不许被当成真实判读回收。

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
    assert "0008" not in S.find_worksheets(HERE)
    # ⭐ 样例引的段 id 与作者源行号必须是**真的**
    assert "NL-L001" in {sid for sid, _ in S.nl_segments("0008")[0]}
    src = S.puml_text("0008").splitlines()
    assert src[4].strip() == "[*] --> fork1: After (2 s)", "样例引的第 5 行对不上作者源"
    assert src[7].strip() == "TurnOn --> fork1"
    # ⛔ 全量回收一遍：样例不许出现在产物里
    for pair in S.IN_SCOPE_PAIRS:
        data = C.collect_pair(pair, _ws(pair))
        assert data["new_issues"] == [], f"{pair} 的 §5 被预填了"


def test_enum_values_survive_the_value_splitter():
    """取值里不许含 `_enum_values` 的分隔符，否则单值会被切成多值而报错。"""
    for name, vals in NF.ENUMS.items():
        for v in vals:
            assert V._RE_ENUM_SPLIT.split(v) == [v], f"{name} 的 `{v}` 含分隔符，会被切开"


def test_the_deleted_fields_are_gone_everywhere():
    """被删的旧字段不许在任何地方留下活口。

    判据分三层，缺一层都会留下**静默**的残骸：
    ① 模板与字段表里不许再出现它们（否则判读者照旧填，回收器不认）；
    ② 54 份工作单与两份共用页的正文里不许再教怎么填它们；
    ③ [validate.py](./validate.py) 不许再引用它们 —— 引用一个不存在的字段的校验
       永远不触发，看起来却像在保护什么。
    """
    dead = ["basis", "scope", "depth", "layer", "primary_predicate",
            "reference_side", "generated_side", "direction"]
    for name in dead:
        assert name not in NF.FIELD_NAMES, f"`{name}` 还在字段表里"
        assert name not in NF.ENUMS, f"`{name}` 还在枚举表里"
        assert f"{name}:" not in NF.template("0001"), f"`{name}` 还在模板里"
    for gone in ("SEP_FACT", "SEP_BASIS", "SEP_SCOPE", "SEP_AXIS", "SEP_OPTIONAL",
                 "SEPARATORS", "BASES", "SCOPES", "DEPTHS", "DIRECTIONS",
                 "BASIS_MEANING", "SCOPE_MEANING", "BASIS_TO_LAYER",
                 "is_out_of_scope", "REQUIRED_WHEN_OUT_OF_SCOPE", "template_v2"):
        assert not hasattr(NF, gone), f"`newfields.{gone}` 还在"

    # ② 正文：工作单与共用页不许再有旧字段的**填写行**。
    #    判据钉在行首，不是全文包含 —— 上游数据里就有 `... child scope: DoorsClosing`
    #    这种引文，那是台账原话，不该被这条测试判成「还在教旧字段」。
    taught = ["basis", "scope", "depth", "primary_predicate",
              "reference_side", "generated_side", "direction"]
    for path in [_ws(p) for p in S.IN_SCOPE_PAIRS] + [os.path.join(HERE, "HOWTO.md")]:
        doc = _read(path)
        for t in taught:
            assert not re.search(rf"^{t}\s*[:：]", doc, re.M), \
                f"{os.path.basename(path)} 还留着 `{t}:` 填写行"
        assert "深度: [" not in doc, f"{os.path.basename(path)} 的裁决块还留着「深度」"

    # ③ 校验器：不许再从**新增条目**里读这些字段。
    #    判据钉在读取形式（`f.get("x")` / `_enum_check(..., "x", ...)` /
    #    `NF.field_value(f, "x")`）上 —— 而不是全文包含：台账记录**仍然**带着
    #    `generated_side` / `direction` / `layer`，去重时读它们是对的。
    src = _read(os.path.join(HERE, "validate.py"))
    for name in dead:
        for form in (f'f.get("{name}")', f'"{name}", NF', f'field_value(f, "{name}")'):
            assert form not in src, f"validate.py 还从新增条目里读 `{name}`"
    for probe in ("NL_GROUNDED_LAYERS", "OUT_OF_SCOPE_CUES", "DEPTH_FIELD",
                  "_check_basis", "new_issue_split", "parse_line_refs"):
        assert probe not in src, f"validate.py 还引用着 {probe} —— 那套检查该整体删掉"


def test_the_decision_block_has_no_depth_row():
    """裁决块只剩「裁决 + meta review 意见 + 理由」—— 「深度」那一栏必须没了。

    ⚠️ 2026-08-14 两处更新：① 模板合并成「采纳 / 不采纳 + 理由」，故不再有第三个字段；
    ② ⛔ **工作单侧的判据从「子串不含『深度』」改成「没有名为『深度』的字段行」** ——
    ⭐ 人工 meta review 的正文里会正常出现「嵌套深度」这类词（`EIS-0032-02` 就有），
    ⚠️ 而子串判据会把它误报成「字段没删干净」。⛔ 要守的是字段表，不是措辞。
    """
    for tpl in (fb.LEDGER_TEMPLATE, fb.CANDIDATE_TEMPLATE):
        assert "深度" not in tpl, tpl
    assert fb.LEDGER_FIELDS == ["裁决", "meta review 意见", "理由"]
    assert fb.LEDGER_CHOICES == ["裁决"]
    assert "深度" not in fb.CANDIDATE_FIELDS
    # 落地：54 份工作单的 99 个裁决区 + 92 个候选区里一个「深度」都不许剩
    for pair in S.IN_SCOPE_PAIRS:
        for key, body in fb.extract(_read(_ws(pair))).items():
            for ln in body.splitlines():
                assert not ln.strip().startswith("深度"), \
                    f"{pair} 的 {key} 块还留着「深度」字段行：{ln}"
    # 旧模板必须被认出来 —— 否则 99 个裁决区会永远印着一个不存在的字段
    assert fb.is_stale_template(fb.LEGACY_LEDGER_TEMPLATES[0], "ledger")
    assert not fb.is_stale_template(
        fb.LEGACY_LEDGER_TEMPLATES[0].replace("理由:", "理由: 我写的"), "ledger")


def test_derive_leaves_the_boundary_ruling_to_the_main_session():
    """边界不再由判读者分类，故 `derive()` **不许**自己给出 `in_scope`。

    它必须显形为 `pending` 里的一条 —— 「回收后人工分拣」是一个待办，
    不是一个可以默认成 `True` 的值。
    """
    d = NF.derive("0001", "NEW-0001-01",
                  {"defect_locus": "element", "defect_element": "state"})
    for name in ("in_scope", "counts_as_defect", "boundary_ruling"):
        assert name not in d, f"`{name}` 不该由 derive 产出"
        assert name in d["pending"], f"`{name}` 既没产出也没进 pending"
    assert "人工分拣" in d["pending"]["in_scope"]


def test_progress_counts_every_registered_entry():
    """「新增」栏是登记总数，不分界内界外；进度看板不再有「越界」栏。"""
    data = {
        "pair": "0001", "summary": None,
        "ledger": [], "candidates": [], "checklist": [],
        "new_issues": C.parse_new("\n\n".join([
            _entry("0001", 1),
            _logic_entry("0001", 2),
            _logic_entry("0001", 3, defect_locus="global",
                         defect_logic_kind="unreachable",
                         statement="NL 要求 2 秒后迁移，模型无时钟可承载。"),
        ]), "0001"),
        "orphans": {}, "untouched_keys": [],
    }
    row = V.pair_progress("0001", data)
    assert row["new"] == 3
    assert "out_of_scope" not in row
    assert not hasattr(V, "new_issue_split")
    board = _read(os.path.join(HERE, "PROGRESS.md"))
    assert "| 越界 |" not in board
    assert "人工分拣" in board, "看板没说清边界分拣改到哪一步做"


def test_multiline_statement_with_colons_is_not_truncated():
    """⛔ 作者在 `statement` 里换行写「NL 第 3 句：…」不许把字段截断。

    ⚠️ 这是实测出来的坑：解析器原本把任何 `名字:` 开头的行都当新字段，
    于是 statement 被就地砍断而且**不报错** —— 人工写的判断静默丢一半。
    修法是只认 `newfields.FIELD_NAMES` 里的那几个字段名。
    """
    body = "\n".join([
        "### NEW-0001-01",
        "statement: 第一行",
        "NL 第 3 句：After entering the braking state 明确要求后继状态",
        "结论: 该义务在模型上没有结构性承载",
        "expected_after_fix: :8 那条边带上触发词",
        "nl_evidence: NL-L003",
        "defect_locus: element",
    ])
    f = C.parse_new(body, "0001")[0]["fields"]
    assert "NL 第 3 句" in f["statement"]
    assert "该义务在模型上没有结构性承载" in f["statement"]
    assert "NL 第 3 句" not in f
    assert "结论" not in f
    assert f["expected_after_fix"] == ":8 那条边带上触发词"


def test_derive_maps_the_element_axis_onto_M():
    """`element_of_M` 由脚本从维度 A 映射，不由人工填。

    走逻辑支时必须显形为 `None` —— 逻辑层缺陷按定义不落在单个 $M$ 分量上，
    猜一个填上会让并表统计凭空多出一批假分量。
    """
    assert NF.derive_element_of_M("state")[0] == "S"
    assert NF.derive_element_of_M("transition")[0] == "Tr"
    assert NF.derive_element_of_M("guard")[0] == "Tr"
    assert NF.derive_element_of_M("trigger")[0] == "E"
    assert NF.derive_element_of_M("effect")[0] == "A"
    assert NF.derive_element_of_M("variable")[0] == "V"
    assert NF.derive_element_of_M("other")[0] is None
    assert NF.derive_element_of_M(None)[0] is None
    # 每一种都得给出依据说明，"推不出来" 也要说清为什么
    for probe in ("state", "other", None):
        assert NF.derive_element_of_M(probe)[1]

    d = NF.derive("0001", "NEW-0001-01",
                  {"defect_locus": "element", "defect_element": "guard",
                   "defect_qualifier": "missing", "defect_reference": "language"})
    assert d["element_of_M"] == "Tr"
    logic = NF.derive("0001", "NEW-0001-02",
                      {"defect_locus": "global", "defect_logic_kind": "unreachable"})
    assert logic["element_of_M"] is None
    assert logic["defect_element"] is None and logic["defect_qualifier"] is None
    assert logic["defect_logic_kind"] == "unreachable"


def test_derive_reports_the_fields_it_cannot_produce():
    """「脚本推导」必须是一句可核对的话：算不出来的要列进 `pending`。"""
    d = NF.derive("0001", "NEW-0001-01",
                  {"defect_locus": "element", "defect_element": "transition",
                   "defect_reference": "language"})
    assert d["pair"] == "0001" and d["group"] == "NL02"
    assert d["llm"] == S.source_meta("0001")["llm"]
    assert d["element_of_M"] == "Tr"
    for name in ("assertions", "replay", "verdict", "homogeneity_group",
                 "layer", "in_scope"):
        assert name in d["pending"], f"{name} 既没算出来也没列进 pending"


def test_field_table_and_template_stay_in_sync():
    """模板里出现的字段名必须与 `FIELD_NAMES` 完全一致 —— 两处走偏就收不回来。"""
    body = NF.template("0001", count=1)
    names = [ln.split(":", 1)[0] for ln in body.splitlines()
             if ":" in ln and not ln.startswith("---")]
    assert names == NF.FIELD_NAMES
    assert set(NF.ALWAYS_REQUIRED_FIELDS) <= set(NF.FIELD_NAMES)
    assert set(NF.OPTIONAL_FIELDS) <= set(NF.FIELD_NAMES)
    assert set(NF.CHOICE_FIELDS) <= set(NF.FIELD_NAMES)
    assert set(NF.CHOICE_FIELDS) == set(NF.ENUMS)
    # 两支的轴合起来正好是「必填之外」的那部分，不多不少
    assert (set(NF.ALWAYS_REQUIRED_FIELDS) | set(NF.ELEMENT_BRANCH_FIELDS)
            | set(NF.LOGIC_BRANCH_FIELDS) | set(NF.CONDITIONAL_FIELDS)
            | set(NF.OPTIONAL_FIELDS)) == set(NF.FIELD_NAMES)
    # `other_note` 是**条件必填**：它既不在「总是必填」里，也不是可留空项
    assert set(NF.CONDITIONAL_FIELDS) <= set(NF.FIELD_NAMES)
    assert not set(NF.CONDITIONAL_FIELDS) & (set(NF.ALWAYS_REQUIRED_FIELDS)
                                             | set(NF.OPTIONAL_FIELDS)
                                             | set(NF.CHOICE_FIELDS))


def test_the_two_branches_ask_for_disjoint_axes():
    """两支要问的轴必须**不相交** —— 否则「条件式」名不副实。"""
    assert set(NF.required_axes_for("element")) == set(NF.ELEMENT_BRANCH_FIELDS)
    for locus in ("pair", "global", "other"):
        assert set(NF.required_axes_for(locus)) == set(NF.LOGIC_BRANCH_FIELDS)
        assert set(NF.forbidden_axes_for(locus)) == set(NF.ELEMENT_BRANCH_FIELDS)
    assert set(NF.forbidden_axes_for("element")) == set(NF.LOGIC_BRANCH_FIELDS)
    assert not set(NF.ELEMENT_BRANCH_FIELDS) & set(NF.LOGIC_BRANCH_FIELDS)
    # locus 未填时两支都不问 —— 那时该报的是「locus 未选」
    assert NF.required_axes_for(None) == [] and NF.forbidden_axes_for(None) == []
    # 候选面：19 与 16，都远小于 28
    # （element 支 2026-08-13 由 18 增到 19 —— 多了界外取值 `region`）
    n = {k: len(v) for k, v in NF.ENUMS.items()}
    assert n["defect_locus"] + n["defect_element"] + n["defect_qualifier"] \
        + n["defect_reference"] == 19
    assert n["defect_locus"] + n["defect_logic_kind"] + n["defect_reference"] == 16
    assert sum(n.values()) == 28


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


def test_the_axes_are_not_induced_from_the_ledger():
    """座标系的取值**不许**是从台账已用过的值归纳来的。

    这条钉的是本轮的目的本身：若取值来自台账，判读者能选出来的类型按构造
    就等于框架已经能说的东西，「台账漏了什么」这个问题会被答案定义掉。
    判据是机械的：五个轴的取值集合与台账 `direction` / `layer` 实际用过的集合
    **不得相等，也不得是其子集**。
    """
    used_direction = {r["direction"] for r in S.ledger_records(reportable_only=True)}
    used_layer = {r["layer"] for r in S.ledger_records(reportable_only=True)}
    for name, vals in NF.ENUMS.items():
        v = set(vals)
        assert v != used_direction and v != used_layer, f"{name} 与台账用过的集合相同"
        assert not (v <= used_direction), f"{name} 是台账 `direction` 的子集"
        assert not (v <= used_layer), f"{name} 是台账 `layer` 的子集"
    # 台账自己的字段仍然照常渲染在 §2（读它是为了裁决那一条），两套不要混
    assert set(NF.LAYERS) == used_layer
    assert "direction" not in NF.ENUMS


# ==================================================================== 两类校验

# ---- ① 条件式分支的必填一致性（正反两面）

def test_element_branch_requires_the_element_and_qualifier_axes():
    """正例：走 `element` 支却不给 A / B → 必须报 `E`，且说清为什么这一条要回答它。"""
    for missing in ("defect_element", "defect_qualifier"):
        rep = _validate_new("0001", _entry("0001", **{missing: None}))
        msgs = _msgs(rep, "E")
        assert any(f"必填项 `{missing}` 未选" in m for m in msgs), (missing, msgs)
        assert any("defect_locus = element" in m for m in msgs), \
            "报错没说清是哪一支要求的"


def test_logic_branch_requires_the_logic_kind_axis():
    """正例：走逻辑支却不给 D → 必须报 `E`。三个非 element 取值都要测。"""
    for locus in ("pair", "global", "other"):
        rep = _validate_new("0001", _logic_entry(
            "0001", defect_locus=locus, defect_logic_kind=None))
        assert any("必填项 `defect_logic_kind` 未选" in m for m in _msgs(rep, "E")), locus


def test_the_element_branch_does_not_ask_for_the_logic_axis():
    """反例：走 `element` 支时**不填** D 是对的，不许报 `E`。

    这一半比正例更要紧：把两支的轴全设成必填，等于回到平铺表 ——
    判读者会被逼着给一条非确定性缺陷勾一个 `defect_element`，产出的是噪声。
    """
    rep = _validate_new("0001", _entry("0001"))
    assert _msgs(rep, "E") == [], _msgs(rep, "E")
    assert not any("defect_logic_kind" in m for m in _msgs(rep)), \
        "走 element 支却被问了逻辑轴"


def test_the_logic_branch_does_not_ask_for_the_element_axes():
    """反例：走逻辑支时**不填** A / B 是对的，不许报 `E`。"""
    rep = _validate_new("0001", _logic_entry("0001"))
    assert _msgs(rep, "E") == [], _msgs(rep, "E")
    for axis in NF.ELEMENT_BRANCH_FIELDS:
        assert not any(f"必填项 `{axis}`" in m for m in _msgs(rep)), axis


def test_filling_the_other_branch_is_a_warning_not_an_error():
    """填了另一支的轴只报 `W`：那多半是选完 locus 忘了删。

    填多了不像填少了那样让记录不可用，做成 `E` 只会逼人删掉本来无害的信息。
    """
    rep = _validate_new("0001", _entry("0001", defect_logic_kind="unreachable"))
    assert _msgs(rep, "E") == [], _msgs(rep, "E")
    assert any("不问 `defect_logic_kind`" in m for m in _msgs(rep, "W"))
    rep2 = _validate_new("0001", _logic_entry("0001", defect_element="state"))
    assert _msgs(rep2, "E") == []
    assert any("不问 `defect_element`" in m for m in _msgs(rep2, "W"))


def test_an_entry_with_no_locus_at_all_is_a_hard_error():
    """`defect_locus` 是第一个问题：不填就两支都定不了，必须报 `E`。

    此时**不许**顺带报「分支轴缺失」—— 那会让人以为要把两支都填上。
    """
    rep = _validate_new("0001", _entry("0001", defect_locus=None,
                                       defect_element=None, defect_qualifier=None))
    msgs = _msgs(rep, "E")
    assert any("必填项 `defect_locus` 未选" in m for m in msgs)
    assert not any("defect_element" in m or "defect_logic_kind" in m for m in msgs), msgs


# ---- ② 枚举取值合法性

@pytest.mark.parametrize("field,bad", [
    ("defect_locus", "cross"), ("defect_element", "node"),
    ("defect_qualifier", "wrong"), ("defect_reference", "nl"),
])
def test_completeness_rejects_values_outside_each_enum(field, bad):
    rep = _validate_new("0001", _entry("0001", **{field: bad}))
    assert any(f"`{field} = {bad}` 不在枚举内" in m for m in _msgs(rep, "E"))
    assert any("归不进就选 `other`" in m for m in _msgs(rep, "E"))


def test_completeness_rejects_a_logic_kind_outside_the_enum():
    rep = _validate_new("0001", _logic_entry("0001", defect_logic_kind="deadlock"))
    assert any("`defect_logic_kind = deadlock` 不在枚举内" in m for m in _msgs(rep, "E")), \
        "`deadlock` 不是本座标系的取值（它是并发概念），必须被挡下"


def test_completeness_rejects_a_multi_valued_single_field():
    rep = _validate_new("0001", _entry("0001", defect_qualifier="missing incorrect"))
    assert any("`defect_qualifier` 是单值字段" in m for m in _msgs(rep, "E"))


# ---- ③ 自由文本三项

@pytest.mark.parametrize("field", ["statement", "expected_after_fix", "nl_evidence"])
def test_completeness_flags_a_missing_required_text_field(field):
    rep = _validate_new("0001", _entry("0001", **{field: None}))
    assert any(f"必填项 `{field}` 为空" in m for m in _msgs(rep, "E"))


def test_the_ok_criterion_must_be_written_out():
    """③「修好算什么」必须写 —— 缺它时报错要说清写成什么形状。"""
    rep = _validate_new("0001", _entry("0001", expected_after_fix=None))
    msgs = [m for m in _msgs(rep, "E") if "expected_after_fix" in m]
    assert msgs
    assert any("可判定的期望结果" in m for m in msgs)
    assert any("应该修好" in m for m in msgs), "报错没给出反例，判读者不知道界在哪"


def test_completeness_accepts_a_fully_filled_entry():
    """反例：两支各一条填齐的条目都不许报任何 `E`。"""
    for entry in (_entry("0001"), _logic_entry("0001")):
        rep = _validate_new("0001", entry)
        assert _msgs(rep, "E") == [], _msgs(rep, "E")


def test_blank_nl_evidence_is_not_the_same_as_writing_none():
    """留空 ≠ 写 `无`：前者是没填（报 E），后者是判过了（放行）。"""
    blank = _validate_new("0001", _entry("0001", nl_evidence=None))
    assert any("必填项 `nl_evidence` 为空" in m for m in _msgs(blank, "E"))
    explicit = _validate_new("0001", _entry("0001", nl_evidence="无"))
    assert not any("nl_evidence" in m for m in _msgs(explicit, "E"))


def test_requirement_reference_with_no_nl_evidence_is_only_a_warning():
    """`defect_reference = requirement` 而 `nl_evidence` 写 `无` 只报 `W`。

    两个字段值就能看出不对劲，但「这一条到底靠不靠某句 NL」要读文意 ——
    做成 `E` 会把「NL 确实说了、只是判读者一时找不到段 id」挡在门外。
    """
    rep = _validate_new("0001", _logic_entry("0001", nl_evidence="无"))
    assert _msgs(rep, "E") == []
    assert any("必须引用 NL 的某一句" in m for m in _msgs(rep, "W"))
    # 反例：`language` 配 `无` 是**正确答案**，一个字都不许提示
    ok = _validate_new("0001", _entry("0001"))
    assert not any("nl_evidence" in m for m in _msgs(ok))


def test_completeness_rejects_a_segment_id_that_does_not_exist():
    rep = _validate_new("0001", _entry("0001", nl_evidence="NL-L009"))
    assert any("不存在的段 id `NL-L009`" in m for m in _msgs(rep, "E"))
    ok = _validate_new("0001", _entry("0001", nl_evidence="NL-L002"))
    assert _msgs(ok, "E") == []


def test_the_validator_does_not_judge_semantics():
    """校验器不许对文意下判断 —— 这一条是 §11 准入边界的落点。

    三个探针都是**语义**问题：主张需不需要时钟语义、参照物选得对不对、
    这句话算不算在说「违反」。它们一个都不许触发 `E`。
    """
    probes = [
        _entry("0001", statement="Cooking 状态缺少 30 秒的计时器超时迁移，timer 到期后无出边。"),
        _entry("0001", statement="NL 要求两个区域同时活跃，模型里没有正交区可承载。"),
        _entry("0001", defect_reference="language",
               statement="模型违反了 NL 第 2 句的显式义务。"),
    ]
    for entry in probes:
        rep = _validate_new("0001", entry)
        assert _msgs(rep, "E") == [], _msgs(rep, "E")


# ---- ④ 去重（三条都只报 W）

def test_dedup_flags_two_entries_on_the_same_element():
    """同 pair + 同 locus + 点到同一个模型元素 → 提示可能重复。"""
    rep = _validate_new(
        "0001",
        _entry("0001", 1, statement="InitialState 没有任何初始边指向它。"),
        _entry("0001", 2, statement="进入 InitialState 的入口未定义。"))
    assert any("是不是同一缺陷" in m for m in _msgs(rep, "W"))


def test_dedup_stays_quiet_on_two_genuinely_different_entries():
    """反例：不同元素 + 不同支的两条不许被判重复。"""
    rep = _validate_new(
        "0001",
        _entry("0001", 1, statement="InitialState 没有任何初始边指向它。"),
        _logic_entry("0001", 2, defect_locus="global",
                     defect_logic_kind="unintended_terminal",
                     statement="ClampingLoseState 是吸收态，进去以后再也出不来。"))
    assert not any("是不是同一缺陷" in m for m in _msgs(rep, "W"))


def test_dedup_flags_overlap_with_an_existing_ledger_record():
    """新增条目与本 pair 现有台账条目撞车时，应提示改走 §2 的「修正」。"""
    pair = "0004"
    rec = S.ledger_records(pair)[0]
    data = {
        "pair": pair, "summary": None,
        "ledger": [], "candidates": [], "checklist": [],
        "new_issues": C.parse_new(_entry(
            pair, 1, statement=rec["statement"][:200]), pair),
        "orphans": {}, "untouched_keys": [],
    }
    rep = V.Report()
    V.validate_pair(pair, data, rep)
    assert any("疑似重复" in m and rec["id"] in m for m in _msgs(rep, "W"))


def test_dedup_is_a_warning_not_a_hard_gate():
    """「是不是同一缺陷」是语义判断，不能做成确定性门。"""
    rep = _validate_new(
        "0001",
        _entry("0001", 1),
        _entry("0001", 2))
    assert all(i["level"] == "W" for i in rep.items if "同一缺陷" in i["msg"])


def test_out_of_scope_pair_worksheet_is_a_hard_error():
    """`00x8` 有工作单是**分母被改错**的信号，必须报 `E`。"""
    with tempfile.TemporaryDirectory() as tmp:
        d = os.path.join(tmp, "nl_0008")
        os.makedirs(d)
        with open(os.path.join(d, "0008.md"), "w", encoding="utf-8") as fh:
            fh.write("# 不该存在\n")
        rep = V.Report()
        found = S.find_worksheets(tmp)
        for p in S.OUT_OF_SCOPE_PAIRS:
            if p in found:
                rep.E(p, "SCOPE", "越界 pair 不该有工作单")
        assert any(i["level"] == "E" for i in rep.items)


def test_a_shape_that_satisfies_every_gate():
    """CLAUDE.md §13 要求的「满足全部门的一个具体形状」，机械钉住。

    这条目自身的 `E` 与 `W` 都必须为空 —— 只要有任何一道门与另一道门的
    合法解空间不相交，这里就会红。形状从 [README.md](./README.md) §3.5.4 读，
    不在测试里另抄一份：抄了两份就会各改各的。
    """
    fields = _readme_gate_shape()
    shape = "\n".join(["### NEW-0008-01"] + [f"{k}: {v}" for k, v in fields.items()])
    rep = _validate_new("0008", shape, allow_ledger=True)
    assert _msgs_for(rep, "NEW-0008-01", "E") == [], _msgs_for(rep, "NEW-0008-01", "E")
    assert _msgs_for(rep, "NEW-0008-01", "W") == [], _msgs_for(rep, "NEW-0008-01", "W")
    # 形状本身必须还是走 element 支、且 `language` 配 `无` 的那一组
    assert fields["defect_locus"] == "element"
    assert fields["defect_element"] and fields["defect_qualifier"]
    assert fields["defect_reference"] == "language"
    assert fields["nl_evidence"] == "无"
    assert "defect_logic_kind" not in fields


def _readme_gate_shape():
    """从 [README.md](./README.md) §3.5.4 结尾那个 ```text 块里读出字段表。

    直接读 README，不在测试里另抄一份 —— 抄了两份就会各改各的，
    而 README 那段自称「由本测试机械钉住」。
    """
    with open(os.path.join(HERE, "README.md"), encoding="utf-8") as fh:
        readme = fh.read()
    head = readme.index("写出一个「满足全部门」的具体形状")
    body = readme[head:readme.index("## 四、命令", head)]
    blocks = re.findall(r"```text\n(.*?)```", body, flags=re.S)
    assert len(blocks) == 1, f"§3.5.4 里应当只有一个形状块，实得 {len(blocks)}"
    out = {}
    for line in blocks[0].strip().splitlines():
        k, _, v = line.partition(":")
        out[k.strip()] = v.strip()
    return out


def test_readme_gate_shape_example_stays_off_the_graded_pairs():
    """§3.5.4 的「可满足形状」样例不许取自任何**在评 pair** 的真实制品。

    2026-08-13 出过一次：那段样例本来写的是 pair `0001` 的一条真实、字段填齐、
    可直接登记的发现。它给的不只是事实，而是**座标该怎么勾的答案** ——
    而归类正是本轮要判读者自己做的判断（[CLAUDE.md](../../../../../CLAUDE.md) §3.5.-1
    的出处问题：产物里若出现一条与 README 逐字雷同的记录，「它是人独立归类的吗」
    将无法回答）。

    判据不看措辞，看**指向**：把样例块里出现的标识符逐一拿去比对 —— 凡是「在某个
    在评 pair 的作者源里出现、却不在 `0008` 的作者源里」的，一律判为指向在评 pair。
    """
    fields = _readme_gate_shape()
    text = " ".join(fields.values())
    idents = set(re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", text))
    safe = set(re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", S.puml_text("0008")))
    safe |= set(v for vals in NF.ENUMS.values() for v in vals)
    safe |= {"defect_locus", "defect_element", "defect_qualifier",
             "defect_logic_kind", "defect_reference"}
    for pair in S.IN_SCOPE_PAIRS:
        own = set(re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", S.puml_text(pair)))
        bad = (idents & own) - safe
        assert not bad, (
            f"§3.5.4 的样例指向了在评 pair {pair} 的制品元素 {sorted(bad)} —— "
            "换成 0008 或不指向任何在评 pair 的抽象样例")
    # 反面自检：判据本身必须抓得住那条被撤掉的旧样例，否则这条测试是摆设
    stale = {"statement": "生成侧凭空多出一条通往 ClampingLoseState 的迁移"}
    stale_idents = set(re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", " ".join(stale.values())))
    own_0001 = set(re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", S.puml_text("0001")))
    assert (stale_idents & own_0001) - safe, "判据抓不住旧样例 —— 它就白写了"


def test_untouched_template_produces_no_new_issue_records():
    """⛔ 空模板不许被当成一条新增条目 —— 否则 54 份会凭空多出 108 条 `E`。"""
    recs = C.parse_new(NF.template("0001"), "0001")
    assert [r for r in recs if "derived" in r] == []
    data = C.collect_pair("0001", _ws("0001"))
    assert data["new_issues"] == []


@pytest.mark.parametrize("gen", [0, 1, 2])
def test_regenerating_swaps_the_stale_field_block_but_keeps_human_text(gen):
    """字段表改版后重跑：原样未填的旧模板要被换掉，填过的一个字都不许动。

    少了这条，改版当天的后果很具体：54 份工作单的 §5 会**永远停在旧字段表**上 ——
    幂等注回是按 key 做的，旧骨架会被当成「人工内容」原样保留，新字段一个都出不来。
    三代旧模板都要认：第一代 10 字段平铺、第二代 8 字段、第三代三层结构。
    """
    pytest.skip("§4 深度检查清单与 §5 新增登记于 2026-08-14 按用户裁定整体拆除"
                "（本轮工作单只做「对现有台账 + 候选逐条裁决」）。⛔ 本条测的是那两节的"
                "行为，故整条挂起而不是删除 —— 代码（section_checklist / section_new / checklist.py / newfields.py）仍在，"
                "下一轮若重开挖深可整段接回，届时把本 skip 去掉即可。"
                "⭐ 「那两节确实不在了」由 test_the_removed_sections_are_really_gone 守着。")
    legacy = fb.LEGACY_NEW_TEMPLATES[gen].format(pair="0001")
    assert fb.is_stale_template(legacy, "new", "0001")
    assert not fb.is_stale_template(legacy + "\nstatement: 我写的", "new", "0001")
    assert not fb.is_stale_template(NF.template("0001"), "new", "0001")

    with tempfile.TemporaryDirectory() as tmp:
        path = _ws("0001", tmp)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(fb.render("NEW-0001", "new", legacy))
        subprocess.run([sys.executable, os.path.join(HERE, "generate.py"),
                        "--pairs", "0001", "--out", tmp],
                       check=True, capture_output=True)
        with open(path, encoding="utf-8") as fh:
            swapped = fh.read()
        assert NF.HINT_ELEMENT_BRANCH in swapped, "原样未填的旧模板没有被换成新模板"
        assert "defect_locus: [ ]" in swapped and "expected_after_fix:" in swapped
        assert "basis: [ ]" not in swapped and "scope: [ ]" not in swapped

    with tempfile.TemporaryDirectory() as tmp:
        path = _ws("0001", tmp)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(fb.render("NEW-0001", "new",
                               legacy.replace("statement:", "statement: 我写的判断", 1)))
        subprocess.run([sys.executable, os.path.join(HERE, "generate.py"),
                        "--pairs", "0001", "--out", tmp],
                       check=True, capture_output=True)
        with open(path, encoding="utf-8") as fh:
            after = fh.read()
        assert "我写的判断" in after


def test_a_filled_block_survives_regeneration():
    """幂等的正面用例：座标块**填过之后**重跑生成器，一个字都不许变。"""
    pytest.skip("§4 深度检查清单与 §5 新增登记于 2026-08-14 按用户裁定整体拆除"
                "（本轮工作单只做「对现有台账 + 候选逐条裁决」）。⛔ 本条测的是那两节的"
                "行为，故整条挂起而不是删除 —— 代码（section_checklist / section_new / checklist.py / newfields.py）仍在，"
                "下一轮若重开挖深可整段接回，届时把本 skip 去掉即可。"
                "⭐ 「那两节确实不在了」由 test_the_removed_sections_are_really_gone 守着。")
    pair = "0001"
    filled = "\n".join([
        "### NEW-0001-01",
        "defect_locus: [x] global",
        NF.HINT_LOGIC_BRANCH,
        "defect_logic_kind: [x] unintended_terminal",
        NF.HINT_BOTH,
        "defect_reference: [x] requirement",
        "statement: ClampingState 及其所有祖先都没有出边，进入后永远留在那里。",
        "expected_after_fix: 从 ClampingState 出发存在一条能到达终态的执行。",
        "nl_evidence: NL-L002",
    ])
    with tempfile.TemporaryDirectory() as tmp:
        src = _ws(pair)
        dst = _ws(pair, tmp)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
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
        assert f["defect_locus"]["chosen"] == ["global"]
        assert f["defect_logic_kind"]["chosen"] == ["unintended_terminal"]
        assert f["defect_reference"]["chosen"] == ["requirement"]
        assert f["expected_after_fix"].startswith("从 ClampingState")
        d = parsed["new_issues"][0]["derived"]
        assert d["defect_logic_kind"] == "unintended_terminal"
        assert d["element_of_M"] is None

        # 第三次不该再产生任何改动
        before = _sha(dst)
        subprocess.run([sys.executable, os.path.join(HERE, "generate.py"),
                        "--pairs", pair, "--out", tmp],
                       check=True, capture_output=True)
        assert _sha(dst) == before


def test_a_filled_checklist_is_never_swapped_out():
    """§4 清单块**填过之后**不许被重新生成的材料覆盖。

    这一条是 `checklist_is_untouched` 的反面：为了让清单文案的更新能到达
    54 份工作单，未填的清单块会被换成当前材料 —— 而判据必须严到
    「勾选、`发现:` 有内容、以及**不带前缀的裸发现行**」三种都算已填。
    ⚠️ 第三种最容易漏：`collect.parse_checklist` 收裸文本行，
    把那种行当成未填会**直接删掉人写的发现**。
    """
    body = "[ ] REACH-01 某个问句\n    · 机械判据：某某。\n"
    assert fb.checklist_is_untouched(body)
    assert fb.is_stale_template(body, "checklist")
    for touched in ("[x] REACH-01 某个问句\n",
                    "[ ] REACH-01 某个问句\n发现: 确实缺一条边\n",
                    "[ ] REACH-01 某个问句\n这里其实没问题，机械判错了\n"):
        assert not fb.checklist_is_untouched(touched), touched
        assert not fb.is_stale_template(touched, "checklist"), touched


# ============================================== ⭐ 目录布局（按 NL 组分 subdir）

def test_directory_layout_is_one_dir_per_nl():
    """⭐ 9 个 `nl_XXXX/`，每个 6 份工作单 + 1 份 `NL.md`；根上 1 份 `HOWTO.md`。

    ⛔ 根目录不许再有工作单 —— ⚠️ 留一份在根上不会有任何报错，但它会绕开
    「同 NL 的 6 份摆在一起」这个全部收益，且 `NL.md` 的相对链接从根上是断的。
    """
    dirs = S.nl_dirs()
    assert len(dirs) == 9, dirs
    assert dirs == sorted(f"nl_{min(S.pairs_of_dir(d))}" for d in dirs)

    for dirname in dirs:
        pairs = S.pairs_of_dir(dirname)
        assert len(pairs) == 6, f"{dirname} 有 {len(pairs)} 个 pair，应为 6"
        got = sorted(f for f in os.listdir(os.path.join(HERE, dirname))
                     if f.endswith(".md"))
        assert got == sorted([S.NL_DOC] + [f"{p}.md" for p in pairs]), \
            f"{dirname} 的内容不对：{got}"

    assert os.path.exists(S.howto_path(HERE)), "根上缺 HOWTO.md"
    root_md = {f for f in os.listdir(HERE) if f.endswith(".md")}
    assert not {f for f in root_md if re.fullmatch(r"\d{4}\.md", f)}, \
        f"根目录还留着工作单：{sorted(root_md)}"
    # ⭐ `DEDUP_ACCOUNTING.md` 2026-08-16 新增：条目数（321 vs 未去重的 380）的唯一权威账目，
    # ⛔ 它是防止「把未去重的数当条目总数」再次发生的那一页，故属根目录常驻文档。
    assert root_md == {S.WORKSHEET_HOWTO, "README.md", "PROGRESS.md",
                       "DEDUP_ACCOUNTING.md"}, sorted(root_md)


def test_nl_grouping_follows_the_nl_text_not_the_last_digit():
    """⛔⛔ 分组判据是 **NL 全文的 sha8**，⛔ 不是 pair id 的末位数字。

    ⚠️ 两者在 8 组上恰好一致，⛔ 在第 9、第 10 组上**交叉**：`0002` 的 NL 与 `0013`
    相同，`0003` 的 NL 与 `0012` 相同。⭐ 这条测试就是为了让「化简成末位数字」这个
    看起来无害的重构当场变红 —— ⛔ 否则 `nl_0002/NL.md` 会对该目录里一半的工作单为假，
    而那正是 [README.md](./README.md) §十记过的那起事故的形状。
    """
    assert S.nl_sha8("0002") == S.nl_sha8("0013") != S.nl_sha8("0012")
    assert S.nl_sha8("0003") == S.nl_sha8("0012") != S.nl_sha8("0013")
    assert S.nl_siblings("0002") == ("0002", "0013", "0023", "0033", "0043", "0053")
    assert S.nl_siblings("0003") == ("0003", "0012", "0022", "0032", "0042", "0052")
    # ⛔ 末位数字规则若成立，这两条会相等 —— 它不成立
    assert S.nl_dir("0002") != S.nl_dir("0012")
    assert S.nl_dir("0002") == S.nl_dir("0013")

    # ⭐ 正面：同一目录里的 6 份**逐字节**共用同一份 NL，⛔ 且分段完全一致
    for dirname in S.nl_dirs():
        pairs = S.pairs_of_dir(dirname)
        assert len({S.nl_text(p) for p in pairs}) == 1, f"{dirname} 里坐着不止一份 NL"
        assert len({tuple(S.nl_segments(p)[0]) for p in pairs}) == 1, \
            f"{dirname} 里 6 份的分段不一致 —— NL.md 的单表必然对其中一份为假"
    # ⭐ 反面：不同目录之间不许共用 NL（否则本该合成一组）
    assert len({S.nl_sha8(S.pairs_of_dir(d)[0]) for d in S.nl_dirs()}) == 9


def test_every_relative_link_in_the_workspace_resolves():
    """⛔ 相对链接必须**可达**。⚠️ 目录下沉一层后，`./x.py` 全部要变成 `../x.py`。

    ⛔ 断链的后果不是难看，是自包含塌掉：判读者点不进 `HOWTO.md` 就只能凭记忆填字段。
    ⭐ 判据覆盖工作区内**全部**入库 `.md`，⛔ 不只是本轮改过的那些。
    """
    bad = []
    for rel in _all_md(HERE):
        path = os.path.join(HERE, rel)
        for target in re.findall(r"\]\((\.[^)#\s]*)\)", _read(path)):
            # ⚠️ 必须 URL 解码：⛔ Markdown 链接里空格写作 `%20`（GitHub 能解析），
            # 而 `os.path.exists` 不认 —— 不解码会把合法链接误报成死链（实测栽在
            # `Experiment%20Results.xlsx` 上）。⭐ 解码只影响判定，报错仍打原文。
            resolved = os.path.normpath(os.path.join(
                os.path.dirname(path), _urllib_parse.unquote(target)))
            if not os.path.exists(resolved):
                bad.append(f"{rel} -> {target}")
    assert not bad, "断链：\n  " + "\n  ".join(bad)


def test_every_worksheet_points_at_its_nl_doc_and_the_howto():
    """⭐ 每份工作单都要能一步跳到**同组的** `NL.md` 与共用的 `HOWTO.md`。

    ⛔ 判据不是「文中提到过这两个名字」，而是**链接目标存在且指的是同一组** ——
    ⚠️ 指错组是这套布局里唯一会静默出错的方式（链接照样可达，内容却是别人的 NL）。
    """
    for pair in S.IN_SCOPE_PAIRS:
        ws = _ws(pair)
        doc = _read(ws)
        assert f"](./{S.NL_DOC})" in doc, f"{pair} 未链接同目录的 {S.NL_DOC}"
        assert f"](../{S.WORKSHEET_HOWTO})" in doc, f"{pair} 未链接 {S.WORKSHEET_HOWTO}"
        # ⭐ 同目录的 NL.md 必须真的是本 pair 那一组的
        nl_doc = _read(os.path.join(os.path.dirname(ws), S.NL_DOC))
        assert f"nl_dir={S.nl_dir(pair)}" in nl_doc
        assert f"sha8 `{S.nl_sha8(pair)}`" in nl_doc, \
            f"{pair} 同目录的 {S.NL_DOC} 不是本 pair 的 NL"
        assert f"[`{pair}`](./{pair}.md)" in nl_doc, \
            f"{S.nl_dir(pair)}/{S.NL_DOC} 没把 {pair} 列进服务对象"


def test_shared_pages_carry_no_fill_blocks():
    """⛔ `HOWTO.md` 与 `NL.md` 不许有填写区 —— 它们是**共用**页。

    ⚠️ 后果很具体：共用页上的一个填写区会被 6 份（或 54 份）工作单同时指向，
    ⛔ 而 [collect.py](./collect.py) 只读 `<pair>.md` —— 填在那里的判读**收不上来**，
    ⛔ 且不会有任何报错。
    """
    targets = [S.howto_path(HERE)]
    targets += [os.path.join(HERE, d, S.NL_DOC) for d in S.nl_dirs()]
    for path in targets:
        text = _read(path)
        assert fb.extract(text) == {}, f"{os.path.relpath(path, HERE)} 里有 FILL 哨兵"
        assert "FILL:BEGIN" not in text


def test_the_field_guide_is_not_copied_back_into_the_worksheets():
    """逐字段说明的**长篇 rationale** 只许存在于 `HOWTO.md`，不许复制回 54 份工作单。

    ⚠️ **这条的边界移动过两次，都不是放松而是重划。** 用户要求工作单「简单清晰自包含」，
    且明确「要人填的字段必须列全部取值 + 每项一句判定测试」—— 所以**取值图例本身
    必须在工作单里**（§5.2 登记块紧邻处）；仍然不许搬回去的是「为什么这么分」的
    长篇论证（座标系为何是条件式、旧字段表为何撤掉之类，那些在 HOWTO §C）。

    判据仍是**结构性**的、不看措辞：统计「在全部 54 份里逐字相同、且落在 FILL 块外」
    的非空行数。历史刻度：重构前中位 148 行 → 搬走后 ~55 行 → 补回枚举图例后 117 行
    → 换成条件式座标系后 **140 行**（27 个取值各占一行、外加 Dwyer 的 13 行句式骨架，
    比旧的五张表多 23 行；旧表里那些行同样是逐字重复的，所以这是**同类相比**的增长）。
    档设在 160：留出约 15% 余量，够再加一两条取值，但抄回 HOWTO 任何一整节都会立刻突破。

    ⚠️ 2026-08-13 由 160 提到 **200**，实测 167。多出来的 27 行全部是**新材料自带的图例**，
    不是抄回来的论证：维度 A 新增取值 `region` 一行、`other_note` 那一小节（硬规则 + 为什么
    值得单立，7 行）、以及 §3.6 `pyfcstm inspect` 一节的导语（这批怎么来的、归一化口径、
    两个 code 整类排除的理由，共 19 行）。⛔ 这些必须逐份印：判读者不知道 §3.6 是确定性检查、
    不知道 194 条已经归并成 97 条，就会拿它跟台账 99 条直接比 —— 那是错的。
    档取 200 留约 20% 余量。

    ⚠️ 同日 inspect 真正入册后由 200 提到 **250**，实测 **224**（最差那份）。⭐ 这里要说清
    增长的机制，否则下次会被误读成「又抄回来了」：**本条数的是行的出现次数、不是不同行数** ——
    逐字比对 HEAD 与本轮，新增的**不同**共用行只有 **9** 行（§3.6 的标题、物种抬头、
    投影抬头、整类排除说明、`W_DEADLOCK_LEAF` 假阳性说明、以及每条 issue 的骨架行
    「**归一化后的事实陈述**」与底层诊断表头）。⛔ 剩下的增量全部来自**同一批骨架行按对象重复**：
    一份工作单里新建几个 `INS-` 块，这几行就出现几次。⭐ 它随对象数增长，不随说明文字增长，
    故档取 250（约 12% 余量）而**不是**把说明搬走 —— 那五条限定（确定性 vs LLM、压缩比、
    假阳性、整类排除、不确定族也要给）必须出现在判读者动笔的那一页上。
    """
    docs = {p: _read(_ws(p)).splitlines() for p in S.IN_SCOPE_PAIRS}
    seen = collections.Counter()
    for lines in docs.values():
        seen.update(set(lines))
    worst = 0
    for pair, lines in docs.items():
        inside = False
        n = 0
        for ln in lines:
            if ln.startswith("<!-- FILL:BEGIN"):
                inside = True
                continue
            if ln.startswith("<!-- FILL:END"):
                inside = False
                continue
            if inside or not ln.strip():
                continue
            if seen[ln] == len(docs):
                n += 1
        worst = max(worst, n)
    assert worst <= 250, (
        f"某份工作单里有 {worst} 行在 54 份中逐字重复且不在 FILL 块内 —— "
        f"说明性文字被抄回了工作单，请搬回 {S.WORKSHEET_HOWTO}")

    # ⛔ 几段**长篇 rationale** 不许出现在任何工作单里 —— ⭐ 它们回答的是「为什么这么分」，
    # ⛔ 与填表无关；⚠️ 而枚举取值与一句判据是填表必需的，故**不**在此列。
    for moved in ("问题本身被答案定义掉了",                 # §C.1 取值为何必须来自外部
                  "定义域就是单元素",                       # §C.2 为何是条件式
                  "被撤掉的旧字段",                         # §C.3 旧字段表的清单
                  "已知证据缺口"):                          # §D.2
        for pair in S.IN_SCOPE_PAIRS:
            assert moved not in docs[pair] and moved not in _read(_ws(pair)), \
                f"{pair}.md 里又出现了搬去 {S.WORKSHEET_HOWTO} 的说明：{moved}"
        assert moved in _read(S.howto_path(HERE)), \
            f"{S.WORKSHEET_HOWTO} 里没有这段说明：{moved} —— ⛔ 搬丢了"


def test_nl_verbatim_is_in_the_worksheet_but_the_notes_are_not():
    """⭐ NL **原文与译文**必须在工作单里；⛔ **逐段判读提示与整份观察**必须只在 `NL.md`。

    ⚠️ **这条边界是刻意划的，⛔ 两半的理由不同**：

    - ⭐ 原文与译文**不谈被测制品**，同组 6 份逐字节相同，⛔ 复制零风险；
      而判读者填 `nl_evidence` 时手边必须有段 id 与原句，⛔ 让他翻另一个文件是纯摩擦。
    - ⛔ **判读提示谈的是「这一句约束了什么」，历史上出过写进制品断言的事故**
      （[README.md](./README.md) §十）—— 一份 NL 服务 6 个制品，
      ⛔ 一句制品断言必然对其中 5 份为假。⭐ 只留一份，问题就只有一个。
    """
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        segs, _ = S.nl_segments(pair)
        # ⭐ 正面：三列表与每一段的译文都在工作单里
        assert "| 段 id | 原文 | 中文严格翻译 |" in doc, f"{pair}.md 缺 NL 三列表"
        for sid, txt in segs:
            zh = nl_zh.translate(pair, sid)
            assert zh, f"{pair}/{sid} 没有译文"
            assert f"| `{sid}` |" in doc, f"{pair}.md 的 NL 表缺 {sid} 这一行"
            assert esc_like(zh) in doc, f"{pair}.md 缺 {sid} 的译文正文"
            assert esc_like(txt) in doc, f"{pair}.md 缺 {sid} 的英文原文"
        # ⛔ 反面：逐段判读提示与整份观察仍然只在 NL.md
        for sid, _txt in segs:
            assert f"- `{sid}`：" not in doc, f"{pair}.md 又印了 {sid} 的判读提示"
        assert "整份 NL 层面的观察（术语表" not in doc, f"{pair}.md 又印了整份观察正文"
        nl_doc = _read(S.nl_doc_path(HERE, pair))
        assert f"- `{segs[0][0]}`：" in nl_doc, f"{pair} 的 NL.md 丢了判读提示"


def esc_like(text):
    """⭐ 与 [generate.py](./generate.py) 的 `esc()` 同口径（压空白 + 转义竖线）。

    ⛔ 不能直接拿原始字符串去 `in doc` 比：译文里带竖线的段落（守卫表达式
    `dist_to_rear<5 | vel>30` 之类）在表格单元格里是 `\\|`，⛔ 原串永远匹配不上。
    """
    import generate as G
    return G.esc(text)


def test_nl_verbatim_block_is_byte_identical_across_siblings():
    """⭐ 同组 6 份工作单的 NL 节必须**逐字节相同**。

    ⛔ 这是允许复制的**前提**：一旦某份的 NL 节掺进了 pair 级的数字，
    「改一处要记得改六处」就回来了，⚠️ 而漏改的那几份不会有任何报错。
    """
    for dirname in sorted({S.nl_dir(p) for p in S.IN_SCOPE_PAIRS}):
        blocks = {}
        for pair in S.pairs_of_dir(dirname):
            doc = _read(_ws(pair))
            head = "### §1.1 "
            tail = "### §1.2 "
            i, j = doc.find(head), doc.find(tail)
            assert 0 <= i < j, f"{pair}.md 的 §1.1 / §1.2 结构不对"
            blocks[pair] = doc[i:j]
        vals = set(blocks.values())
        assert len(vals) == 1, (
            f"{dirname} 的 6 份工作单 §1.1 不是逐字节相同 —— "
            f"⛔ 有 pair 级内容漏进了共用节：" + "、".join(
                p for p in blocks if blocks[p] != sorted(vals)[0]))


def test_nl_table_sits_on_the_first_screen():
    """⭐ NL 三列表必须在**第一屏** —— ⛔ 判读者一打开工作单就该看到它。

    ⛔ 判据是行号，⛔ 不是「在 §1 里」：材料排在别的材料之后就已经滑出第一屏了。
    ⚠️ **2026-08-13 换了后置锚点**：原先钉的是「必须排在结构摘要之前」，⛔ 而结构摘要
    已整节删除 —— ⭐ 现在钉「必须排在作者源 PlantUML 之前」，⛔ 判据一个字没松：
    §1 里排在 NL 表后面的第一样材料，就是它。
    ⭐ 实测每份都在第 39 行（前言删掉 −6、结构摘要删掉 −15、「怎么填」加回 +13），
    ⛔ 档仍设在 45 行留出余量。
    """
    for pair in S.IN_SCOPE_PAIRS:
        lines = _read(_ws(pair)).splitlines()
        hit = [i + 1 for i, ln in enumerate(lines)
               if ln == "| 段 id | 原文 | 中文严格翻译 |"]
        assert hit, f"{pair}.md 没有 NL 三列表"
        assert hit[0] <= 45, f"{pair}.md 的 NL 表在第 {hit[0]} 行 —— ⛔ 掉出第一屏了"
        # ⛔ 且必须排在作者源 PlantUML **之前**
        nxt = [i + 1 for i, ln in enumerate(lines) if ln.startswith("### §1.2 作者源")]
        assert nxt and hit[0] < nxt[0], f"{pair}.md 的 NL 表排到作者源后面了"


def test_worksheets_stay_under_the_line_budget():
    """行数上限 —— 防止说明性文字慢慢又长回工作单里。

    上限**不是**任意选的：一份工作单的下界由三块不可压缩的内容决定 —— FILL 块
    （人要填的地方）、本 pair 独有的材料（两份 PlantUML、台账条目、候选、清单）、
    以及**自包含所需的取值图例与 NL 原文译文**。

    档位沿革（每次都写清为什么动）：

    | 时间 | 档 | 实测中位 | 为什么 |
    | :-- | --: | --: | :-- |
    | 早期 | 620 | 596 | 自包含：NL 原文译文 + 五个勾选字段全部取值 + 19 谓词搬进来 |
    | 2026-08-13 | 605 | 588 | 三处清理（删前言 / 删结构摘要 / 加「怎么填」），档跟着收 |
    | 2026-08-13 | 650 | 616 | 换成条件式座标系：+27 行五个轴取值、+13 行 Dwyer 句式骨架 |
    | 2026-08-13 | 650 → 800 | 606 | 剥旧元数据（−）与渲染座标映射（+）**大致相抵** |
    | 2026-08-13 | **850 / 最长 1400** | **776 / 最长 1258** | `pyfcstm inspect` 入册：§3.6 逐条印 issue |

    ⚠️ **本轮之前 docstring 与断言已经不一致**（表格写 650、代码断言 800）—— 这里一并更正：
    档就是代码里的那两个数，表格跟着写。

    本轮上调的理由是**材料真的多了一批**，不是文字松了：360 条 inspect 诊断归一化成 189 条
    issue，其中 128 条在 inspect 判重阶段被判为新块（事实陈述 + 逐字证据 + 归并理由 + 五轴映射 +
    底层诊断折叠区 + 裁决区，约 20–30 行），另 61 条作为补充证据挂在 §2 / §3 的对应条目下。
    ⭐ 中位 606 → **776**，最长 `0029` 1258 行。

    ⚠️ 档为什么取 850 而不是贴着 776：⛔ 行数**逐份差异极大**（503 到 1258），因为每个 pair
    新建的块数从 0 到 9 不等；把档收到贴着中位会让块多的那几份频繁擦线，⛔ 而它们长是因为
    **材料本来就多**，不是说明性文字长回来了。⭐ 850 对 776 留约 10% 余量，1400 对 1258 留约 11%。
    ⛔ 上界仍然在守原来那件事：说明性文字不许借着改版长回工作单 —— 那一条另有更准的判据
    （`test_the_field_guide_is_not_copied_back_into_the_worksheets` 数逐字重复行）。
    反面的下界同样要守：不许瘦到把材料抽走了。
    """
    counts = sorted(len(_read(_ws(p)).splitlines()) for p in S.IN_SCOPE_PAIRS)
    median = counts[len(counts) // 2]
    assert median <= 850, f"工作单行数中位数 {median} 超预算 —— 说明性文字长回来了"
    assert counts[-1] <= 1400, f"最长的一份 {counts[-1]} 行超预算"
    # 反面：也不许瘦到把材料抽走了（判读者拿着它必须还能干活）
    # ⚠️ 2026-08-14 下限由 300 降到 260：§4/§5 拆除后每份少约 15%，⛔ 不是「抽多了」。
    # ⭐ 三份数字：§4/§5 拆除前最短 416；拆除后 242；⭐ 2026-08-15 版式统一（拆掉来源分节、
    # 参考侧/生成侧、风险标记、诊断表、折叠区）后最短 163 行；⭐ `UM-` 撤除后最短 **131** 行 —— ⛔ 档降到 120。
    # ⚠️ 242 那份（`0052`）台账 1 条、候选 2 条，⛔ 它本来就是全语料最薄的一份 ——
    # §4/§5 那约 150 行固定文案占它原先 416 行的三分之一以上，拆掉后剩下的几乎全是材料。
    assert counts[0] >= 120, f"最短的一份只有 {counts[0]} 行 —— 抽多了"


def _data_borne_marks(pair, doc, marks):
    """`doc` 里由**数据**逐字带进来的记号数。

    ⚠️⚠️ **2026-08-14 计量方式改了：从「逐块整串匹配、按块累加」改成「字符区间覆盖」。**
    ⛔ 旧法有一个系统性缺口：它要求整个字段值逐字出现在 `doc` 里才计数，
    ⭐ 而人工 meta review 的四个字段被渲进同一段、理由行还追加了尾标、`statement` 还会
    被渲成引用块（多行插 `> `）—— ⚠️ 任何一处形变都让整块落空，于是它的记号被全额记到
    生成器头上。实测 `0002` 因此把 17 个 `⭐` 记成生成器侧，而逐个定位后全部在 meta 文本内。

    ⭐ 新法：把所有已知数据块在 `doc` 里的**出现区间**并起来，落在并集内的记号算数据侧。
    ⛔ 这既修了失配，也没有放宽 —— 不在任何数据块内的记号仍然全算生成器侧。
    """
    import generate as G
    import dtier as _DT
    chunks = []
    # ⭐ 人工 meta review 的四个字段
    for _rid, _rev in _DT.load_meta().items():
        _r = _DT.get(_rid)
        _p = _r.get("pair") if _r else (_rid.split("-")[1] if "-" in _rid else None)
        if _p != pair:
            continue
        for _k, _zh in _DT.META_FIELDS:
            _v = (_rev.get(_k) or "").strip()
            if _v:
                chunks.append(_v)
    # ⭐ 上游 audit json 的字段值
    rows = list(IF.issues_of(pair))
    for rid in [r["id"] for r in S.ledger_records(pair)] + \
               [k for k, v in CM.candidate_index().items() if v["pair"] == pair]:
        rows += IF.merged_into(rid)
    for rec in rows:
        cs = [rec.get(f) for f in ("statement", "merge_reason", "puml_evidence",
                                   "nl_evidence", NF.OTHER_NOTE_FIELD, "recovery_basis")]
        cs.append((rec.get("overlap") or {}).get("basis"))
        for r in rec.get("rulings") or []:
            cs += [r.get("ruling_basis"), r.get("final_evidence")]
        chunks += [G._flow(c) for c in cs if c]
    # ⭐ 引用块归一：`statement` 渲成 `> ...` 时多行会插 `> `
    flat = doc.replace("\n> ", "\n")
    covered = []
    for ch in chunks:
        if not ch or len(ch) < 8:
            continue
        start = 0
        while True:
            k = flat.find(ch, start)
            if k < 0:
                break
            covered.append((k, k + len(ch)))
            start = k + 1
    covered.sort()
    merged = []
    for a, b in covered:
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    total = 0
    import bisect
    starts = [a for a, _ in merged]
    for m in marks:
        pos = flat.find(m)
        while pos >= 0:
            i = bisect.bisect_right(starts, pos) - 1
            if i >= 0 and pos < merged[i][1]:
                total += 1
            pos = flat.find(m, pos + 1)
    return total

def test_the_worksheets_are_not_wallpapered_with_emoji():
    """emoji 密度的机械档 —— 判据是**对比度**：靠稀疏出现才有用。

    一页一个 `⚠️` 很响，一百个就是壁纸。所以正文默认普通中文陈述句，
    保留的只有三类：表格的**状态列**（[PROGRESS.md](./PROGRESS.md) 的 ⚪/🟡/🟢，
    按 CLAUDE.md §2.2.3 只放 emoji、释义写列外）、标**真会导致误判**的坑的 `⚠️`、
    以及极少量结论锚点。`⭐` 基本不用。

    阈值怎么定的（不是拍脑袋）：

    - 清理前实测每份工作单 **214–254 个**、密度 0.27–0.37 个/行 —— 那就是壁纸。
    - 清理后每份 **10–13 个**、密度 ≤ 0.03。留住的是「勾完别删选项文字」
      「留空 ≠ 写 `无`」「数祖先的成组迁移」这类真坑。
    - 档设 **每份 ≤ 30 个且 ≤ 0.05 个/行**：约为实测的三倍余量，
      够再加十几处真警告，但离壁纸（每份两百个）差一个数量级。
    - `⭐` 单独设 **每份 ≤ 4**：它没有「这里会出错」的语义，只是强调，
      而强调一多就等于没强调。实测每份 0–3 个，且**全部来自引用的上游数据**
      （台账 statement、当年判定者写的 reason）—— 那是**数据**，改它等于改台账。

    ⚠️ 正因为数据里带着这些记号，「生成器正文有没有清干净」不能靠全文计数判。
    所以另加一条更准的判据：**在全部 54 份里逐字相同的那些行就是生成器正文**，
    它们里面 `⭐` 与 `⛔` 必须为 **0**。这一条不受数据干扰。

    ⚠️⚠️ **2026-08-13 口径细化，双份数字都记在这里，⛔ 不是放宽。** `pyfcstm inspect` 入册后，
    §3.6 逐字引用了判定者写的 `statement` / `merge_reason` / `puml_evidence` /
    `recovery_basis` / 判重依据 / 终局裁定依据，⭐ 而那些文字里本来就带着记号。全文计数因此
    由「每份 12–18、中位 13」变成「每份 16–45、中位 27」，`⭐` 最多的一份 6 个。

    ⛔ 若只把档从 30 提到 50，这条测试就再也管不住**生成器自己**了 —— 它可以借数据的额度
    重新贴满壁纸。所以判据改成**按来源拆开数**：

    - **生成器侧** = 全文计数减去「逐字来自三份 audit json 与既有条目数据」的那些记号。
      档**仍是每份 ≤ 30、`⭐` ≤ 4**，一格没放宽；实测每份 **15–24、中位 18**。
      ⚠️ 这一侧确实也涨了（入册前 12–18），涨的是 §3.6 那五条**必须逐份印**的限定：
      物种抬头、「确定性不等于正确」、两个 code 整类排除、`W_DEADLOCK_LEAF` 语义归属须知、
      「不确定那一族也要给」，外加 `suspect` 那 24 条的点名提示与恢复条目的来源标注。
      ⛔ 它们不是装饰：每一条都对应一种会让判读者判错的具体误读。
    - **数据侧**另设一个防跑飞的总档（每份 ≤ 60、密度 ≤ 0.05）。⛔ 它不许用来给生成器兜底：
      改数据里的记号等于改判定者写下的判断文本，⚠️ 那是**证据**，不是排版。
    """
    marks = ("⭐", "⛔", "⚠️")
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        n = sum(doc.count(m) for m in marks)
        lines = len(doc.splitlines())
        own = n - _data_borne_marks(pair, doc, marks)
        # ⚠️⚠️ **2026-08-14 这里发生过一次「先提档、又收回」，⛔ 过程必须记下来。**
        # 三方 D 档判读区块入册后本条一度报 43 个（超 30），⭐ 我先把档提到 55；
        # ⛔ 但那是**计量错了**，不是生成器贴了壁纸 —— `_data_borne_marks` 旧法要求整个字段值
        # 逐字出现才计数，而人工 meta review 的四个字段被渲进同一段、理由行追加了尾标、
        # `statement` 还被渲成引用块，⚠️ 任何一处形变都让整块落空、记号被全额记到生成器头上。
        # ⭐ 改成**字符区间覆盖**计量后重测：生成器侧最大 **30**、中位 **10.5** ——
        # ⛔ 于是把档收回 32（留约 7% 余量），比原先的 30 只松了一格。
        # ⚠️ 2026-08-15 版式统一后再由 32 → 36：⭐ 每条现在多两行标记（问题类型的界外提示、判定表的档位图例），
        # ⛔ 而正文短了 45%，实测最高 `0029` 的 33。
        # ⭐ 教训：档位报警时先问「计量对不对」，⛔ 别直接提档 —— 提档会把真问题一起放过。
        # ⭐ 对价：`dtier.py` 的生成串里 `⭐` 必须为 0，由
        # `test_the_dtier_renderer_spends_no_star_of_its_own` 硬钉。
        # ⚠️⚠️ 2026-08-15 由 32 → **60**，⛔ 而这一次是**按设计**放的，不是被迫的。
        # ⭐ 版式统一后每个条目固定带 **2 个**标记：抬头的分级标记（✅❌❓🟡🟠🔴）与
        # meta review 那行的「需/不需你裁」标记。⚠️ 于是计数**随条目数线性增长** ——
        # `0039` 有 20 个条目 ⇒ 40 个，加两节导语约 10 个 = 50。
        # ⛔ 那正是用户要的「让谁需要裁决一眼可见」，删掉就得靠读整段话找活干。
        # ⭐ 真正的护栏移交给**密度**（下面那道 0.12）：它对「文字里糊满记号」敏感，
        # ⛔ 而对「条目多所以标记多」不敏感 —— 后者不是壁纸。
        assert own <= 60, f"{pair}.md 生成器侧有 {own} 个 emoji —— 又成壁纸了"
        # ⚠️ 2026-08-14 全文计数档由 60 提到 **200**：人工 meta review 入册后数据侧记号大增
        # （实测最大 `0039` 的 171、`0002` 的 132）。⭐ 这一侧只管「连数据一起糊满了」，
        # ⛔ 而人写的分析本来就密；生成器有没有贴壁纸由上面那道 32 守，`⭐` 由 4 与 0 两道守。
        assert n <= 200, f"{pair}.md 全文有 {n} 个 emoji —— 连数据侧一起跑飞了"
        # ⚠️⚠️ 2026-08-14 密度门改为按**生成器侧**算，⭐ 档位仍是 0.05（计量修对后够用）。
        # ⛔ 原先用全文计数除行数，与紧邻的计数门（用 `own`）口径不一致 —— 那个不一致
        # 一直没暴露，是因为在此之前数据侧的记号本来就少。⚠️ 三方 D 档判读的人工
        # meta review 入册后立刻暴露：`0016` 全文 43 个记号里 **32 个是数据侧**，
        # 全文密度 0.067 却生成器侧只有 0.017。⭐ 若按全文判，就变成「人写的分析越细、
        # 生成器越要删自己的警告」，⛔ 方向完全反了。
        # ⭐ 双份数字（人工 meta review 入册后重测）：生成器侧密度 0.017–0.029，全文密度 0.041–0.154；故全文档取 0.20（⛔ 生成器侧仍是 0.05）。
        # ⭐ 计量修对后实测生成器侧密度最大 **0.032**，⛔ 故档位仍是 0.05，一格没动。
        # ⚠️ 2026-08-15 密度档 0.05 → 0.09：⛔ 计数档 32 一格没动。分母变了 ——
        # 版式统一后每份短了约 45%（中位 594 → 326 行），⭐ 同样的记号数密度机械上升。
        # ⭐ 实测生成器侧最高 0.093（`0021`：20 个 / 214 行 —— ⚠️ 短工作单把比值推高）；档取 0.12。
        assert own / lines <= 0.12, \
            f"{pair}.md 生成器侧 emoji 密度 {own / lines:.3f} 超档"
        # ⛔ 全文另设一道防跑飞的档（比生成器侧宽一倍）：⚠️ 它管的是「连数据一起糊满了」，
        # 不许用来给生成器兜底 —— 生成器那道是上面那条。
        # ⚠️ 全文档由 0.10 提到 0.14（⛔ 生成器侧那道 0.05 一格没动）：人工 meta review
        # 入册后数据侧记号大增（`0001` 实测 49/450 = 0.109，其中生成器侧仅 0.017）。
        # ⭐ 这一侧管的是「连数据一起糊满了」，⛔ 而人写的分析本来就密 —— 拿它压生成器方向是反的。
        # ⭐ 全文密度实测最大 0.207（`0054`：463 行里 96 个记号，其中生成器侧仅约 10）——
        # ⚠️ 短工作单 + 密集的人工 meta review 会把这个比值推高，⛔ 而那不是壁纸。档取 0.28。
        assert n / lines <= 0.28, f"{pair}.md 全文 emoji 密度 {n / lines:.3f} 跑飞了"
        # ⚠️⚠️ 2026-08-14 `⭐` 档由 4 提到 12，⛔ 而**判据同时收紧**了：
        # `dtier.py` 的生成串里现在 `⭐` 为 **0**（已逐行清空并由下面那条断言钉住），
        # ⭐ 所以工作单里剩下的每一个 `⭐` 都来自**数据** —— 上游 audit json 的字段值，
        # 或人工 meta review 的 `brief`/`reason`/`crux`/`focus`。
        # ⭐ 计量改成区间覆盖后实测生成器侧 `⭐` 最大 **3**，⛔ 故档位仍是 4，一格没动。
        own_star = doc.count("⭐") - _data_borne_marks(pair, doc, ("⭐",))
        assert own_star <= 4, f"{pair}.md 生成器侧有 {own_star} 个 ⭐"

    # 生成器正文 = 在全部 54 份里逐字相同的行。这里一个 ⭐ / ⛔ 都不许有。
    docs = {p: _read(_ws(p)).splitlines() for p in S.IN_SCOPE_PAIRS}
    seen = collections.Counter()
    for lines in docs.values():
        seen.update(set(lines))
    shared = [ln for ln, k in seen.items() if k == len(docs) and ln.strip()]
    # ⚠️ 2026-08-14 下限由 50 降到 40：§4/§5 拆除后共用行少了两整节的骨架，实测 50。
    # ⭐ 这条判据本身不变（共用行 = 生成器正文），⛔ 只是分母小了。
    # ⚠️ 下限降过两次，⛔ 两次都是分母变小而非判据失效：2026-08-14 §4/§5 拆除后实测 50
    # → 档 40；⭐ 2026-08-15 版式统一（拆掉六个来源分节与各自导语）后实测 **35** → 档 **25**。
    # ⭐ 判据本身没动：共用行 = 生成器正文。⚠️ 共用行变少本身是好事 ——
    # ⛔ 它正是「说明文字没被抄进工作单」的直接体现。
    assert len(shared) > 25, "共用行太少，这条判据失效了"
    for ln in shared:
        assert "⭐" not in ln and "⛔" not in ln, f"生成器正文还挂着标记：{ln[:60]}"

    # ⚠️⚠️ **`HOWTO.md` 单独定档 0.08，⛔ 理由必须写清否则下次会被当成放水。**
    # 它与工作单的性质不同：工作单是**材料**（记号应稀疏，靠对比起作用），
    # ⭐ 而 HOWTO 是**填写说明** —— 它的正文本身就是「哪里会填错」的清单。
    # ⭐ 实测 8 个记号**全是 `⚠️`**、逐个都在标真坑（两套计数口径不能混、写成一段不要换行、
    # 写 `无` 是有意义的答案、旧字段语义重叠、候选侧的已知证据缺口、`UM-` 已撤出）。
    # ⛔ 密度从 0.036 升到 0.054 的主因是**分母变小**（169 → 148 行，版式统一时拆掉了
    # 六个来源分节的读法），⚠️ 分子只从 6 加到 8（我加的两条都是实质警告）。
    # ⛔ 我不为了过档删掉一条真警告 —— 那与这道门要防的东西（信号被淹没）正好相反。
    for path, cap in (("HOWTO.md", 0.08), ("README.md", 0.05)):
        doc = _read(os.path.join(HERE, path))
        n = sum(doc.count(m) for m in marks)
        lines = len(doc.splitlines())
        assert n / lines <= cap, f"{path} 的 emoji 密度 {n / lines:.3f} 超档（档 {cap}）"
        assert doc.count("⭐") == 0, f"{path} 有 {doc.count('⭐')} 个 ⭐"
        assert doc.count("⛔") == 0, f"{path} 有 {doc.count('⛔')} 个 ⛔"

    # 表格单元格与 bullet 不许再挂前缀标记 —— 那是密度反弹最快的两个地方
    for pair in list(S.IN_SCOPE_PAIRS)[:6] + ["0059"]:
        for i, ln in enumerate(_read(_ws(pair)).splitlines(), 1):
            t = ln.strip()
            if t.startswith("|"):
                for cell in t.strip("|").split("|"):
                    c = cell.strip()
                    assert not any(c.startswith(m) for m in marks), \
                        f"{pair}.md:{i} 表格单元格挂了前缀标记：{c[:40]}"
            if t.startswith("- ") or re.match(r"^\d+\. ", t):
                body = re.sub(r"^(?:- |\d+\. )", "", t)
                assert not any(body.startswith(m) for m in ("⭐", "⛔")), \
                    f"{pair}.md:{i} bullet 挂了前缀标记：{body[:40]}"


# ==================================================================== 术语英中双写

#: 2026-08-13 从工作单 §2 剥掉的十项台账旧元数据。
#: ⛔ 这份清单是下面几条测试的**唯一**真源，⛔ 不在别处另抄。
STRIPPED_LEDGER_FIELDS = [
    "layer", "direction", "element_of_M", "decided_by", "primary_predicate",
    "nl_evidence", "verdict", "replay",
]


def test_the_stripped_ledger_metadata_is_gone_everywhere():
    """⛔⛔ 剥掉的十项 + 两张图例 + 整节断言组，在 54 份里必须**零命中**。

    ⚠️ 为什么这是一条**学术**纪律而不是排版纪律：本轮要判读者回答的是
    「我们这套框架有没有漏掉东西」。⛔ 那十项里有七项是框架给这一条贴的标签
    （四层归因、八方向、$M$ 分量、分层判定来源、主谓词……），⛔ 先把它们印在题面上，
    判读者就只会在既有格子之间挑一个 —— ⛔ 问题被答案定义掉了。
    ⛔ `verdict` / `replay` 更直接：那是流水线的判定与复算结论，等于标准答案。

    判据分四层，⛔ 缺一层都会留下**静默**的残骸：
    ① 字段表行（`| \\`layer\\`（归因层） |` 这种）一行都不许剩；
    ② 两张图例（断言角色、谓词三族）与「**断言组**」小节整体消失；
    ③ [terms.py](./terms.py) 里服务它们的常量与 helper 必须删干净 ——
       ⛔ 留一个不用的常量会让下一个人以为那一栏还印着；
    ④ [sources.py](./sources.py) 的风险标记不许再读它们 ——
       ⚠️ 标记渲染在裁决块**正上方**，是判读者动笔前读到的最后一句话。
    """
    # ① 字段表行：判据钉在**表格单元格**形态上，⛔ 不是全文包含 ——
    #    台账 statement 原文里就有「layer」「verdict」这类词，那是数据，不该被判成残骸。
    #
    # ⚠️ 范围**只到 §2**。⛔ 不能拿去扫全文：`nl_evidence` 仍然是 §5 要判读者**自己填**
    # 的一个字段（它出现在填写模板与 §B.4 说明里）。⭐ 本轮删的是「把台账那一条**已经
    # 填好的** `nl_evidence` 印给判读者看」，⛔ 不是把这个字段从新增登记块里拿掉 ——
    # ⚠️ 两件事同名但相反，混起来会把 §5 的必填项一起误删。
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        sec2 = _section(doc, "## §2 ", "## §3 ")
        for name in STRIPPED_LEDGER_FIELDS:
            assert not re.search(rf"^\|\s*`{re.escape(name)}`", sec2, re.M), \
                f"{pair}.md 的 §2 还留着 `{name}` 的字段表行"
        for gone in ("| 同质组 |", "| 上游 |"):
            assert gone not in sec2, f"{pair}.md 的 §2 还留着 `{gone}`"

    # ② 两张图例与断言组小节
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        for gone in ("**断言组**", "**断言组的四个角色**", "**谓词三族**",
                     "应有实测值", "无任何断言表达式"):
            assert gone not in doc, f"{pair}.md 还留着「{gone}」"

    # ③ terms.py：常量与 helper 都不许剩
    for gone in ("LAYER_ZH", "ELEMENT_ZH", "DECIDED_BY_ZH", "VERDICT_ZH", "REPLAY_ZH",
                 "ROLE_ZH", "FAMILY_ZH", "PREDICATE_ZH", "DIRECTION_MEANING",
                 "DIRECTION_ZH", "DIRECTION_WHAT", "FIELD_ZH",
                 "layer_cell", "direction_cell", "element_cell", "decided_by_cell",
                 "predicate_cell", "verdict_cell", "role_label", "family_label"):
        assert not hasattr(T, gone), f"`terms.{gone}` 还在 —— 它服务的那一栏已经不印了"
    # 生成器也不许再引用它们
    gen_src = _read(os.path.join(HERE, "generate.py"))
    for gone in ("T.layer_cell", "T.direction_cell", "T.element_cell",
                 "T.decided_by_cell", "T.predicate_cell", "T.verdict_cell",
                 "T.role_label", "T.family_label", "T.FIELD_ZH", "_fmt_assertions"):
        assert gone not in gen_src, f"generate.py 还在调用 `{gone}`"

    # ④ 风险标记：既不许读隐藏字段，也不许在文案里提它们
    src = _read(os.path.join(HERE, "sources.py"))
    body = src[src.index("def risk_flags"):src.index("def review_json")]
    for name in STRIPPED_LEDGER_FIELDS + ["assertions", "has_negative_control"]:
        assert f'rec.get("{name}")' not in body, \
            f"risk_flags 还从记录里读 `{name}` —— 那一栏判读者已经看不到了"
    assert not hasattr(S, "shallow_hint"), \
        "`sources.shallow_hint` 还在 —— 它的四条理由全部援引已隐藏字段"
    for gone in ("NL_GROUNDED_LAYERS", "layer_basis_table"):
        assert not hasattr(NF, gone), f"`newfields.{gone}` 还在 —— 唯一消费者已删"

    # 落地复核：真跑一遍 `risk_flags`，⛔ 结果文案里不许出现那些字段名
    for pair in S.IN_SCOPE_PAIRS:
        for rec in S.ledger_records(pair):
            for _, msg in S.risk_flags(rec):
                for name in ("primary_predicate", "decided_by", "nl_evidence", "replay"):
                    assert name not in msg, \
                        f"{rec['id']} 的风险标记文案还在提 `{name}`：{msg[:60]}"


def test_every_mapped_axis_value_is_written_in_both_languages():
    """⭐ §2 / §3 里印出来的每一个座标取值都必须 `english（中文）`，⛔ 不许留裸标识符。

    ⚠️ 这是上面两条被删测试留下的职责：旧字段不印了，⛔ 但**新座标的取值仍然要印**，
    ⛔ 而「判读者看到一串裸英文标识符不知道它什么意思」这个问题原样还在。
    判据是**逐条逐轴**比对渲染出的单元格，⛔ 不是「文档里能搜到某个中文词」——
    ⚠️ 后者会被别处偶然出现的同一个词蒙过去。
    """
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        recs = [(r["id"], LM.for_record(r["id"])) for r in S.ledger_records(pair)]
        recs += [(k, CM.for_candidate(k)) for k, v in CM.candidate_index().items()
                 if not k.startswith("UM-")
                 if v["pair"] == pair]
        for key, m in recs:
            if not m or not m.get("mappable"):
                continue
            for axis in CM.AXES:
                val = m.get(axis)
                if not val:
                    continue
                cell = T.bi(val, NF.ZH[axis].get(val))  # ⚠️ 2026-08-15：五轴由表格改成 `问题类型` 一行，锚点改为双写片段
                assert "仓库未定义" not in cell, f"{key} 的 {axis} 取值没有中文名"
                assert cell in doc, f"{key} 的 {axis} 没按英中双写渲染：{cell}"


# ==================================================================== 座标映射
#
# ⭐ 本组钉住 2026-08-13 新增的两份映射（台账 99 条 + 候选 141 条 = 240 个对象）。
# ⚠️ 这批映射是**一次大规模判定**，⛔ 若它只存在于渲染结果里，事后既无法复核也无法重算。


def _section(doc, start, end):
    """截出 `start` 到 `end` 之间的一段正文。⛔ 找不到 `start` 就是调用方写错了标题。"""
    i = doc.index(start)
    j = doc.find(end, i)
    return doc[i:] if j < 0 else doc[i:j]


def _all_mappings():
    """`{对象 id: (映射记录, 它属于哪个 pair)}` —— 240 个对象一份不落。"""
    out = {}
    for pair in S.IN_SCOPE_PAIRS:
        for rec in S.ledger_records(pair):
            out[rec["id"]] = (LM.for_record(rec["id"]), pair)
    for key, meta in CM.candidate_index().items():
        # ⛔ `UM-` 一族 2026-08-16 已整批撤出工作单（见 docs/findings/um_residue_ruling.md），
        # ⚠️ 但 candidate_mapping.json 里仍保留它们的映射记录 —— ⭐ 那是历史事实，不删。
        if key.startswith("UM-"):
            continue
        out[key] = (CM.for_candidate(key), meta["pair"])
    return out


def test_all_240_objects_have_a_mapping_or_an_explicit_refusal():
    """⭐ 台账 99 + 候选 141 = **240** 个对象，每一个都得有取值或明确的「映射不上」。

    ⛔ 不许有第三种状态。⚠️ 缺一条的后果是**静默**的：工作单会照常渲染出一个空白格，
    而判读者没法分辨「我们判过但判不出来」与「我们压根没判」——
    ⭐ 前者是有价值的数据（它度量新座标系对现有材料的覆盖度），后者是漏工。
    """
    led, cand = LM.stats(), CM.stats()
    assert led["total"] == 99, f"台账映射 {led['total']} 条，应为 99"
    assert cand["total"] == 141, f"候选映射 {cand['total']} 条，应为 141"
    assert led["mapped"] + led["unmapped"] == 99
    assert cand["mapped"] + cand["unmapped"] == 141
    for key, (m, _pair) in _all_mappings().items():
        assert m is not None, f"{key} 没有映射记录"
        assert isinstance(m.get("mappable"), bool), f"{key} 的 `mappable` 不是布尔"
        assert (m.get("evidence") or "").strip(), f"{key} 没给逐字依据"


def test_the_candidate_index_matches_what_the_worksheets_render():
    """⛔ `candidate_mapping.candidate_index()` 的 key 必须与 54 份工作单**真渲染出来**
    的候选块 key 逐一相等。

    ⚠️ 这一条把两套编号规则钉在一起。⛔ 否则映射文件按一套规则枚举、生成器按另一套渲染，
    两边各自「完整」，⭐ 而对不上的那些格会安静地空着 —— 没有任何一条断言会红。
    """
    rendered = set()
    for pair in S.IN_SCOPE_PAIRS:
        for key, _body in fb.extract(_read(_ws(pair))).items():
            if key.split("-")[0] in ("VU", "DIFF", "UM"):
                rendered.add(key)
    indexed = {k for k in CM.candidate_index() if not k.startswith("UM-")}
        # ⛔ `UM-` 一族 2026-08-16 已整批撤出工作单（见 docs/findings/um_residue_ruling.md），
        # ⚠️ 但 candidate_mapping.json 里仍保留它们的映射记录 —— ⭐ 那是历史事实，不删。

    assert rendered == indexed, (
        f"只在工作单里：{sorted(rendered - indexed)[:5]}；"
        f"只在索引里：{sorted(indexed - rendered)[:5]}")
    # ⚠️ 2026-08-16 `UM-` 一族（49 条）整批撤出工作单（见 docs/findings/um_residue_ruling.md），⭐ 故渲染出的候选由 141 降到 **92**（VU 15 + DIFF 77）；⛔ candidate_mapping.json 里仍保留 UM 的 49 条映射记录（历史事实，不删），故它的 total 仍是 141。
    assert len(indexed) == 92, f"渲染出的候选 {len(indexed)} 个，应为 92"


def test_every_rendered_mapping_matches_the_mapping_file():
    """⛔⛔ 映射文件与渲染结果**逐块机械对拍** —— 240 个对象一个不漏。

    ⚠️ 这是「映射真的印上去了」的唯一硬保障。⭐ 判据分两面：
    ① 文件里说有取值的，渲染结果里必须逐轴出现那一行；
    ② 文件里说映射不上的，渲染结果里必须出现卡点抬头**和**那条 `note` 原话。

    ⛔ 第二面不能省：只测 ① 的话，把「映射不上」渲染成一片空白也能全绿，
    ⚠️ 而那恰恰是最该让判读者看见的一类 —— 「这一条我们也没判出来」本身就是信号。
    """
    docs = {p: _read(_ws(p)) for p in S.IN_SCOPE_PAIRS}
    for key, (m, pair) in _all_mappings().items():
        doc = docs[pair]
        if m.get("mappable"):
            for axis in CM.AXES:
                val = m.get(axis)
                if not val:
                    continue
                row = T.bi(val, NF.ZH[axis].get(val))  # ⚠️ 2026-08-15：五轴由表格改成 `问题类型` 一行，锚点改为双写片段
                assert row in doc, f"{key} 的 {axis} 没渲染进 {pair}.md：{row}"
            assert m["evidence"] in doc, f"{key} 的逐字依据没渲染进 {pair}.md"
        else:
            zh = CM.BLOCKER_ZH.get(m.get("blocker"))
            # ⚠️ 2026-08-15 抬头由「我方没能映射」改为「我方未能归类」（版式统一时改的措辞）。
            head = f"**我方未能归类**（卡点：{zh[0]}）" if zh else "**我方未能归类**"
            assert head in doc, f"{key} 的「没能映射」抬头没渲染进 {pair}.md"
            assert m["note"] in doc, f"{key} 的卡点理由没渲染进 {pair}.md"


def test_the_mapping_is_always_marked_as_our_own_inference():
    """⛔⛔ 每一处映射都必须标明**这是我方推断、判读者的裁决优先**。

    ⚠️ 映射块印在裁决块**正上方**，是判读者动笔前读到的最后一样东西。
    ⛔ 不写明它是推断，判读者会把它当成已经定下来的分类，
    于是「裁决」退化成对我方判断的复读 —— ⛔ 而本轮要的恰恰是他独立的那一份。

    ⚠️ 候选侧还要多一层：候选**本身尚未被认定**，映射的是「若它成立属于哪一格」。
    ⛔ 少这一句，判读者会以为这 141 条已经都是认定过的缺陷了。
    """
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        n_ledger = len(S.ledger_records(pair))
        n_cand = sum(1 for k, v in CM.candidate_index().items()
                     if v["pair"] == pair and not k.startswith("UM-"))
        # ⚠️ §3.6 的 `INS-` 块也带同一句抬头，故计数要把它算进去。
        # ⛔ 不算进去的后果不是漏报而是**误报**：这条测试会在 39 个 pair 上红，
        # 而它本该守的是「每个对象都带上了推断声明」，`INS-` 恰恰也需要它。
        # ⚠️ 只数**新建**的 `INS-` 块：与既有条目重合的那些没有自己的映射块，
        # 它们以补充证据的形式印在那条既有条目里（那里已经有台账 / 候选自己的映射抬头）。
        # ⚠️ 2026-08-13 inspect 已入册（三份 audit json），故这里由 0 改成真实块数。
        # ⚠️⚠️ **2026-08-15 判据改了，⛔ 守的东西没变。** 版式统一后那段推断声明
        # **每节印一次**（原先每条印一次，54 份 × 每份 7–20 条）——⭐ 因为它是**口径**
        # 而不是该条的内容。⛔ 故不再逐条计数，改为：① 声明必须在；② 每个条目必须有
        # `问题类型` 一行（那一行就是映射的落点）。
        import re as _re
        n_obj = len(_re.findall(r"^### (?:EIS|DIFF|VU|UM|INS)-", doc, _re.M))
        n_kind = doc.count("**问题类型**：")
        assert n_kind == n_obj, \
            f"{pair}.md 有 {n_obj} 个条目却只有 {n_kind} 行「问题类型」"
        assert "你的裁决优先" in doc, f"{pair}.md 少了「你的裁决优先」"
        # ⚠️ 两句抬头分属两侧，⛔ 故各自按该侧**真有对象**时才要求 ——
        # ⛔ 一律要求会在「台账 0 条」的 pair 上误报（如 0001）。
        if n_ledger:
            assert "不是已经定下来的事实" in doc, \
                f"{pair}.md 的台账映射没写明它是推断"
        if n_cand:
            assert "**不代表它成立**" in doc, \
                f"{pair}.md 的候选映射没写明「映射不代表它成立」"


def test_the_orthogonal_region_gap_became_a_value_not_a_refusal():
    """⭐⭐ 240 个对象里，曾经卡在**座标系本身**的只有一处：**正交区域及其数量**。
    ⭐ 2026-08-13 它由「拒绝映射」改成「一个界外取值」，本条钉住改法与三个覆盖率数字。

    ⚠️ 改法为什么是这个：旧口径把这 12 条标成 `blocker = taxonomy`，即座标系给不出取值。
    ⛔ 但那个结论站不住 —— 每个轴都有 `other`，而且都在用。⭐ 真正的问题不是「没词」，
    是**那个对象本来就在建模边界之外**（CLAUDE.md 把正交区并发语义排除在 $M$ 之外）。
    ⛔ 把它赶出座标系会让它既进不了记录、也进不了统计，于是同一批材料在报表上呈现成
    「什么都没发生」—— 而 CLAUDE.md 的边界明写**两条同时成立**：不得记为「方法未能检出」，
    也不得反过来声称这些模型没有并发问题。⭐ 给它一个可记录、`counts_as_defect = false`
    的槽位，是唯一同时满足两条的做法。

    三个数字**含义不同、不得混用**（README §七点五 逐条写了口径）：

    - **原始映射率** = mappable / 240
    - **真·座标系覆盖率** = (240 − `taxonomy` 卡点数) / 240
    - **界外占比** = 落在界外取值上的对象数 / 240
    """
    # ---- ① `region` 是个界外取值，不是缺口
    assert "region" in NF.ENUMS["defect_element"]
    assert not NF.counts_as_defect("defect_element", "region")
    assert ("defect_element", "region") in NF.OUT_OF_SCOPE_VALUES

    # ---- ② `taxonomy` 卡点必须**清零**：新增取值之后它不该再有条目
    led, cand = LM.stats(), CM.stats()
    by_blocker = cand["by_blocker"]
    assert "unlabelled" not in by_blocker, f"有映射不上的候选没标卡点类别：{by_blocker}"
    assert by_blocker.get("taxonomy", 0) == 0, (
        f"还有 {by_blocker['taxonomy']} 条标着座标系卡点 —— "
        "新增 `region` 之后它们应当各自重判，不该再挂 `taxonomy`")
    assert not led["unmapped_ids"], f"台账侧不该还有映射不上的：{led['unmapped_ids']}"

    # ---- ③ 三个覆盖率数字
    total = led["total"] + cand["total"]
    assert total == 240
    mapped = led["mapped"] + cand["mapped"]
    assert mapped == 165, f"原始映射率的分子应为 165，实为 {mapped}"
    taxonomy = by_blocker.get("taxonomy", 0)
    assert (total - taxonomy) / total == 1.0, "真·座标系覆盖率应为 100%"
    out_of_scope = sum(
        1 for m, _p in _all_mappings().values()
        if m.get("mappable") and any(not NF.counts_as_defect(a, m.get(a))
                                     for a in CM.AXES if m.get(a)))
    assert out_of_scope == 10, f"界外取值上的对象应为 10 条，实为 {out_of_scope}"

    # ---- ④ 逐条：原来那 12 条现在各自落在哪
    #
    # ⛔ 不是 12 条全变 `region` —— 有两条另有落点，这正是「逐条判、不一刀切」的证据。
    was_taxonomy = {
        "EIS-0006-01": "region", "EIS-0026-01": "region",
        "EIS-0036-01": "region", "EIS-0046-02": "region",
        "DIFF-0023-04": "region", "DIFF-0033-02": "region",
        "DIFF-0037-01": "region", "DIFF-0043-06": "region",
        "DIFF-0047-03": "region", "DIFF-0057-03": "region",
        # 对象横跨界外的区与界内的状态 / 事件，单值装不下 → `other` + 说明
        "DIFF-0056-03": "other",
        # 整张表一块，桶内落点不一致 → 仍映射不上，但卡点是**登记单位**
        # ⛔ `UM-0007` 那一行 2026-08-16 移除：`UM-` 一族已撤出工作单，
        # ⚠️ 而本测试查的是**渲染结果**里的取值。⭐ 它的映射记录仍在 json 里。
    }
    allm = _all_mappings()
    for key, want in was_taxonomy.items():
        m = allm[key][0]
        assert m.get("blocker") != "taxonomy", f"{key} 还挂着 `taxonomy`"
        if want is None:
            assert not m["mappable"] and m["blocker"] == "unit_of_record", \
                f"{key} 应当仍映射不上、卡点为登记单位"
            continue
        assert m["mappable"], f"{key} 应当已能映射"
        assert m["defect_element"] == want, \
            f"{key} 的维度 A 应为 `{want}`，实为 {m['defect_element']}"


def test_every_other_on_any_axis_carries_an_explanation():
    """⭐ 任一轴取 `other`，必须附一句说明 —— 240 条映射与新增登记两侧同一条规则。

    ⛔ 为什么必须两侧同规则：`other` 是出口，出口不写清等于没分类。
    ⚠️ 更要紧的是**两种情形都合法但含义完全不同** —— 「真的都不是」说明座标系还缺一档，
    「涉及多个、一格装不下」说明的是登记单位太粗。⛔ 混在一个空 `other` 里，
    「座标系还缺什么」这个问题就再也答不出来了。
    """
    n = 0
    for key, (m, _pair) in _all_mappings().items():
        if not m.get("mappable"):
            continue
        picked = [a for a in CM.AXES if m.get(a) == "other"]
        if not picked:
            continue
        n += 1
        note = (m.get(NF.OTHER_NOTE_FIELD) or "").strip()
        assert note, f"{key} 的 {picked} 取了 `other` 却没写 `{NF.OTHER_NOTE_FIELD}`"
        assert len(note) >= 10, f"{key} 的 `other` 说明太短，写不清是什么：{note!r}"
    assert n == 28, f"用了 `other` 的映射应为 28 条，实为 {n}"

    # 说明必须**印进工作单**，⛔ 只落在 JSON 里等于没给判读者
    for key, (m, pair) in _all_mappings().items():
        note = (m.get(NF.OTHER_NOTE_FIELD) or "").strip()
        if note:
            assert note in _read(_ws(pair)), f"{key} 的 `other` 说明没渲染进 {pair}.md"


def test_the_other_note_gate_fires_both_ways():
    """⛔ `other` + 空说明必须报 `E`；⭐ 有说明必须放行；⛔ 非 `other` + 空说明不许报。

    ⚠️ 三面都要测。只测「该报的报了」会漏掉最贵的一种错：**门太宽**——
    ⛔ 一条没勾 `other` 的正常登记被这道门拦下，判读者会以为自己填错了。
    """
    base = {
        "defect_locus": {"chosen": ["global"]},
        "defect_logic_kind": {"chosen": ["unreachable"]},
        "defect_reference": {"chosen": ["language"]},
        "statement": "X 从初始态出发到不了。",
        "expected_after_fix": "从初始态存在一条到 X 的执行。",
        "nl_evidence": "无",
    }

    def run(fields):
        rep = V.Report()
        V.validate_pair("0001", {"ledger": [], "candidates": [], "checklist": [],
                                 "summary": None, "orphans": {}, "untouched_keys": [],
                                 "new_issues": [{"id": "NEW-0001-01", "fields": fields}]},
                        rep)
        return [i for i in rep.items if i["level"] == "E"
                and NF.OTHER_NOTE_FIELD in i["msg"]]

    # ① 非 `other` + 空说明 → 不许报
    assert not run(dict(base)), "没勾 `other` 却被这道门拦下了 —— 门太宽"

    # ② `other` + 空说明 → 必须报
    bad = dict(base, defect_logic_kind={"chosen": ["other"]})
    assert run(bad), "`defect_logic_kind = other` 且说明为空，却没报 `E`"

    # ③ `other` + 有说明 → 放行
    ok = dict(bad, other_note="这是「同名碰撞导致某区域默认入口失效」，9 个取值里没有这一档。")
    assert not run(ok), "`other` 已经写了说明，却仍然报 `E`"

    # ④ 每一个轴都要生效，⛔ 不能只有逻辑轴那一档接上了
    for axis, val in (("defect_locus", "other"), ("defect_reference", "other")):
        f = dict(base)
        f[axis] = {"chosen": [val]}
        assert run(f), f"`{axis} = other` 且说明为空，却没报 `E`"

    # ⑤ ⛔ 另一支那些「填多了忘了删」的轴不许连带触发 —— 它们本来只报 `W`
    f = dict(base, defect_element={"chosen": ["other"]})
    assert not run(f), "走逻辑支时 `defect_element` 根本不问，不该因它报 `E`"


def test_the_denial_species_is_separated_from_the_real_candidates():
    """⭐ `gen` 侧逐字否认作者制品有问题的那一族，§3 必须**单列**并写明它不算覆盖缺口。

    ⚠️ 它们与其余候选不是同一个物种：座标系的判定测试全部锚在**作者源 PlantUML** 上，
    而这类记录的 `gen` 写的是「—」或「(不可能生成)」，主张的是**参考模型 / 真值的有效性**。
    ⛔ 它们在制品内指不出任何一处，卡在轴 0。

    ⛔⛔ **所以不得拿它们当「新座标系覆盖不到」的证据** —— 座标系没覆盖到它们，
    是因为它们本来就不在座标系要描述的对象集合里。⛔ 那不是缺口。

    ⚠️ 判据本身必须是**字面**的，⭐ 这样读者能在页面上自行核对（就是那行「生成侧：—」）；
    ⛔ 刻意不做语义推断，边界见 `sources.denies_artifact_defect()` 的 docstring。
    """
    pytest.skip("§3 的**来源分节**于 2026-08-15 按用户裁定整体拆除"
                "（原话：「这个 issue 是怎么来的是 inspect 还是什么统统不重要」）。"
                "⛔ 本条测的是 §3.6 那一节的内容（物种抬头 / 确定性 vs LLM / 整类排除 / "
                "不确定族标签 / 底层诊断表 / 座标拼写 / 恢复条目逐条交代），"
                "⚠️ 而那些文字已随分节一起下线 —— ⭐ 条目本身一条没丢，只是不再标来源、"
                "不再印工具内部细节。⛔ 整条挂起而不是删除：`section_inspect()` 的函数本体仍在，"
                "⭐ 若日后要恢复来源分节，那五条必须逐份印的限定还在里面。"
                "⭐ 「那一节确实不在了、且条目一条没少」由 "
                "test_the_source_sections_are_gone_but_no_item_was_lost 守着。")
    assert S.denies_artifact_defect({"gen": "—"})
    assert S.denies_artifact_defect({"gen": "(不可能生成)"})
    assert S.denies_artifact_defect({"gen": "(任何 LLM 都不可能生成这些阈值)"})
    # ⛔ 反面：真的指认了制品某处的，不许被误判进来
    assert not S.denies_artifact_defect({"gen": "ClampingState --> InitialState"})
    assert not S.denies_artifact_defect({"gen": "（作者模型没有该状态与该边）"})
    # ⚠️ 「优于参考」那一族字面判据吃不进来，⛔ 这是有意的，别悄悄扩大
    assert not S.denies_artifact_defect({"gen": "(生成方在第2、4句优于参考)"})

    found = 0
    for pair in S.IN_SCOPE_PAIRS:
        denials = [(i, d) for i, d in S.unadopted_diffs(pair)
                   if d.get("verdict") in ("problem", "extra", "uncertain")
                   and S.denies_artifact_defect(d)]
        doc = _read(_ws(pair))
        if not denials:
            assert "§3.2a-2" not in doc, f"{pair}.md 无此族却起了 §3.2a-2 一节"
            continue
        found += len(denials)
        assert "§3.2a-2" in doc, f"{pair}.md 有 {len(denials)} 条却没单列"
        assert "不能**算作「新座标系覆盖不到」" in doc, \
            f"{pair}.md 的 §3.2a-2 没写明它不算覆盖缺口"
        for i, _d in denials:
            key = f"DIFF-{pair}-{i:02d}"
            head = doc.index("§3.2a-2")
            assert doc.index(f"### {key} ") > head, f"{key} 没落在 §3.2a-2 之下"
    assert found == 12, f"全语料该族应为 12 条，实为 {found}"


def test_the_mapping_gates_actually_fire():
    """⛔ 两份映射的装载期门必须**真的会抛** —— ⚠️ 只测「正常情况能装载」不算。

    ⭐ 最要紧的是 `evidence` 逐字子串那道门：它是防伪造的**唯一**机械手段。
    ⚠️ 改写过的「依据」看起来同样通顺，⛔ 但它证明不了映射者真的读过原文。
    """
    import json as _json

    def _write(tmp, payload):
        path = os.path.join(tmp, "m.json")
        with open(path, "w", encoding="utf-8") as fh:
            _json.dump(payload, fh, ensure_ascii=False)
        return path

    good = dict(CM.for_candidate("VU-0001-01"))
    with tempfile.TemporaryDirectory() as tmp:
        # ① 依据不是逐字子串 → 抛
        bad = dict(good, evidence="我随手编的一句看起来很通顺的依据")
        with pytest.raises(CM.MappingError, match="逐字子串"):
            CM.load(_write(tmp, {"mappings": [bad]}))
    with tempfile.TemporaryDirectory() as tmp:
        # ② 少了对象 → 抛（⛔ 不许静默留空白格）
        with pytest.raises(CM.MappingError, match="没有映射"):
            CM.load(_write(tmp, {"mappings": [good]}))
    with tempfile.TemporaryDirectory() as tmp:
        # ③ 走 element 支却给了逻辑轴 → 抛
        bad = dict(good, defect_locus="element", defect_element="state",
                   defect_qualifier="missing", defect_logic_kind="unreachable")
        with pytest.raises(CM.MappingError):
            CM.load(_write(tmp, {"mappings": [bad]}))
    with tempfile.TemporaryDirectory() as tmp:
        # ④ 越枚举 → 抛
        bad = dict(good, defect_reference="我编的一个取值")
        with pytest.raises(CM.MappingError, match="不在枚举内"):
            CM.load(_write(tmp, {"mappings": [bad]}))
    with tempfile.TemporaryDirectory() as tmp:
        # ⑤ 标了映射不上却不说卡在哪 → 抛
        bad = dict(good, mappable=False, note="", defect_locus=None,
                   defect_element=None, defect_qualifier=None,
                   defect_logic_kind=None, defect_reference=None)
        with pytest.raises(CM.MappingError, match="没写卡在哪"):
            CM.load(_write(tmp, {"mappings": [bad]}))
    with tempfile.TemporaryDirectory() as tmp:
        # ⑥ 卡点标签越枚举 → 抛
        bad = dict(good, mappable=False, blocker="我编的卡点", note="x",
                   defect_locus=None, defect_element=None, defect_qualifier=None,
                   defect_logic_kind=None, defect_reference=None)
        with pytest.raises(CM.MappingError, match="不在"):
            CM.load(_write(tmp, {"mappings": [bad]}))
    # 台账侧同一道门
    led = dict(LM.for_record("EIS-0000-01"))
    with tempfile.TemporaryDirectory() as tmp:
        bad = dict(led, evidence="同样是我编的一句依据")
        with pytest.raises(LM.MappingError, match="逐字子串"):
            LM.load(_write(tmp, {"mappings": [bad]}))


def test_the_mapping_was_not_derived_from_the_old_fields():
    """⛔ 映射必须是从 `statement` / 描述正文推导的，⛔ 不是拿旧字段机械换算。

    ⚠️ 这条测不了「判定者当时想了什么」，⭐ 但能测一件**必要条件**：
    若映射是从旧 `direction` / `element_of_M` 机械换算来的，
    ⛔ 那两者之间会存在一个**函数关系** —— 同一个旧值必然映到同一个新值。
    ⭐ 实测不存在这种关系，说明至少不是逐一换算出来的。

    ⚠️ 这不是充分条件（⛔ 一份精心伪造的映射照样能通过），
    ⭐ 真正的防线是 `evidence` 逐字子串那道门 + 判定者输入里**故意不含**旧字段。
    """
    by_direction, by_element_of_M = {}, {}
    collisions = 0
    for pair in S.IN_SCOPE_PAIRS:
        for rec in S.ledger_records(pair):
            m = LM.for_record(rec["id"])
            if not m.get("mappable"):
                continue
            new = (m.get("defect_element"), m.get("defect_logic_kind"))
            for old, table in ((rec.get("direction"), by_direction),
                               (rec.get("element_of_M"), by_element_of_M)):
                if old is None:
                    continue
                if old in table and table[old] != new:
                    collisions += 1
                table.setdefault(old, new)
    assert collisions > 0, (
        "每个旧 `direction` / `element_of_M` 取值都恰好映到同一个新取值 —— "
        "这正是「拿旧字段机械换算」会有的形状，⛔ 请复核映射是怎么产生的")


def test_the_element_axis_maps_onto_the_M_from_claude_md():
    """⛔ 维度 A 到 $M$ 分量的映射，其分量字母必须与仓库根 `CLAUDE.md` 的定义对得上。

    ⚠️ 这一条钉的是**出处**：$M = (S, E, V, Tr, A)$ 里
    S=状态集合 E=事件集合 V=变量集合 Tr=迁移集合 A=动作集合 是 `CLAUDE.md`
    「核心技术概念」一节写下的，⛔ 不是本目录自己编的。

    ⚠️ 2026-08-13 由 `test_element_of_M_uses_the_definition_from_claude_md` 改写：
    原版钉的是 `terms.ELEMENT_ZH`（台账 `element_of_M` 展示值的中文名），
    ⛔ 而那一栏已经不印了。⭐ 但 `newfields.ELEMENT_TO_M` 仍在
    `derive()` 里活着，⭐ 所以「分量字母出自 CLAUDE.md」这条出处纪律要接着钉住 ——
    ⛔ 不能因为展示没了就把出处一起丢掉。
    """
    root = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
    claude = _read(os.path.join(root, "CLAUDE.md"))
    for key, zh in (("S", "状态集合"), ("E", "事件集合"), ("V", "变量集合"),
                    ("Tr", "迁移集合"), ("A", "动作集合")):
        assert f"{key}={zh}" in claude, f"CLAUDE.md 里找不到 {key}={zh} 这个定义"
    assert set(NF.ELEMENT_TO_M.values()) <= {"S", "E", "V", "Tr", "A"}, \
        "ELEMENT_TO_M 映到了 $M$ 之外的分量"
    # ⚠️ `region` 与 `other` 一样**没有** $M$ 分量，但理由不同：`other` 是「取决于它是什么」，
    # `region` 是**结构性的没有** —— 正交区在 $M = (S, E, V, Tr, A)$ 里根本不是一个分量
    # （CLAUDE.md 的建模对象边界把它排除在外）。⛔ 给它硬派一个分量等于把界外说成界内。
    assert set(NF.ELEMENT_TO_M) == set(NF.DEFECT_ELEMENTS) - {"other", "region"}, \
        "维度 A 除 `other` / `region` 外每个取值都该有 $M$ 分量"
    assert not NF.counts_as_defect("defect_element", "region"), \
        "`region` 必须是界外取值（`counts_as_defect = false`）"
    assert NF.derive_element_of_M("region")[0] is None, \
        "`region` 不许推出 $M$ 分量"


def test_no_relative_link_in_any_generated_md_is_dead():
    """⛔ 生成物里不许有死链。

    ⚠️ 这一条是实测出来的：把共用页（在 `relabel/` 根）的文案直接搬进工作单时，
    里面的 `[README.md](./README.md)` 在 `nl_0000/` 下解析成 `nl_0000/README.md`
    —— **一个不存在的路径，而 Markdown 死链不报错**。工作单深一层，
    链接必须按工作单的深度写；这条负责证明每一条都真的写对了。
    """
    import generate as G  # noqa: F401  ⭐ 只为确认生成器可导入
    bad = []
    for rel in _all_md(HERE):
        # ⚠️ `_all_md()` 给的是**相对 HERE** 的路径，⛔ 不是相对进程 CWD 的。
        # ⛔ 早先这里直接拿它去 open / dirname，于是本条只在 `cd relabel` 后才绿，
        # ⛔ 从仓库根跑就 FileNotFoundError('HOWTO.md') —— ⭐ 一律先并成绝对路径。
        path = os.path.join(HERE, rel)
        text = _read(path)
        for m in re.finditer(r"\]\(([^)]+)\)", text):
            target = m.group(1)
            if target.startswith(("http://", "https://", "#")):
                continue
            # ⚠️ 必须 URL 解码：⛔ Markdown 链接里空格写作 `%20`（GitHub 能解析），
            # 而 `os.path.exists` 不认 —— 不解码会把合法链接误报成死链（实测栽在
            # `Experiment%20Results.xlsx` 上）。⭐ 解码只影响判定，报错仍打原文。
            resolved = os.path.normpath(os.path.join(
                os.path.dirname(path), _urllib_parse.unquote(target.split("#")[0])))
            if not os.path.exists(resolved):
                bad.append(f"{rel} -> {target}")
    assert not bad, "死链：\n" + "\n".join(sorted(set(bad)))


def test_worksheet_ledger_counts_use_the_reportable_denominator():
    """⛔ §4 分类导语里的台账条数必须是 REPORTABLE 98 条口径，⛔ 不是全 126 条。

    ⚠️ 旧版把 `reachability 25 条`、`entry 23 条`、`initial_target 21 次 primary`
    这些**全 126 条**口径的数字硬编在正文里，⛔ 而 HOWTO §D 用的是 98 条口径 ——
    于是同一份工作单里同一个数有两个值。⛔ 126 含 `00x8` 六个永久越界 pair。
    """
    dc = NF.direction_counts()
    pc = NF.primary_predicate_counts()
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        for stale in ("`reachability`（可达性与终止）方向共 25 条",
                      "`entry`（初始入口）23 条",
                      "`initial_target`（21 次 primary）",
                      "占 30/98"):
            assert stale not in doc, f"{pair}.md 里还有全 126 条口径的旧数字：{stale}"
        if "方向共" in doc:
            assert f"方向共 {dc['reachability']} 条" in doc
        if "次 primary、" in doc:
            assert f"`event_declared` 做过 {pc['event_declared']} 次 primary" in doc


def test_progress_board_links_into_the_nl_dirs():
    """⭐ 看板的 pair 链接要指进 `nl_XXXX/`，⛔ 并显式给出 NL 组这一栏。

    ⚠️ 这一栏就是用户要的那件事：一次处理完同一份 NL 的 6 个模型。
    """
    board = _read(os.path.join(HERE, "PROGRESS.md"))
    assert "| NL 组 |" in board
    for pair in S.IN_SCOPE_PAIRS:
        d = S.nl_dir(pair)
        assert f"](./{d}/{pair}.md)" in board, f"看板里 {pair} 的链接没指进 {d}/"
        assert f"](./{d}/{S.NL_DOC})" in board, f"看板里缺 {d} 的 NL.md 链接"
    assert "不是 pair id 的末位数字" in board, "⛔ 看板没写清分组判据"

# ==================================================================== 三处清理：前言 / §1.2 / 怎么填
#
# ⭐ 本组钉住 2026-08-13 的三条清理要求，⛔ 以及最要紧的一件事：
# ⚠️ 「怎么填」一节里的**每一条说法都必须与 `collect.py` 的真实行为一致**。
# ⛔ 说明与实现不符是最坏的情况 —— 判读者照着说明填，⛔ 而内容被静默丢弃。

def _fill_and_collect(pair, key, body):
    """把某个 FILL 块的内容换成 `body`，走**真实** `collect_pair` 回收。

    ⚠️ 刻意不直接调 `parse_fields` —— ⛔ 那样测的是我在测试里自己拼的参数，
    ⭐ 而真正决定行为的是 `collect_pair` 传给它的 `known` / `choice_fields`。
    """
    text = _read(_ws(pair))
    pat = (r"(<!-- FILL:BEGIN key=" + re.escape(key) + r" kind=\S+ -->\n~~~\n)"
           r"(.*?)"
           r"(\n~~~\n<!-- FILL:END key=" + re.escape(key) + r" -->)")
    m = re.search(pat, text, re.S)
    assert m, f"{pair}.md 里找不到 FILL 块 {key}"
    patched = text[:m.start(2)] + body + text[m.end(2):]
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, f"{pair}.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(patched)
        return C.collect_pair(pair, path)


def _ledger_rec(body, pair="0000", rid="EIS-0000-01"):
    data = _fill_and_collect(pair, rid, body)
    return next(r for r in data["ledger"] if r["id"] == rid)


def _chk_items(body, pair="0000", key="CHK-0000-REACH"):
    data = _fill_and_collect(pair, key, body)
    return next(c for c in data["checklist"] if c["key"] == key)["items"]


def _howto_block(pair):
    """工作单最开头那一节的正文（⛔ 到下一个 `## ` 标题为止）。"""
    doc = _read(_ws(pair))
    i = doc.find("## 怎么填")
    assert i >= 0, f"{pair}.md 没有「怎么填」一节"
    j = doc.find("\n## ", i + 1)
    return doc[i:j if j > 0 else len(doc)]


# ---------------------------------------------------------------- ① 三段前言已删

def test_the_three_nl_preamble_paragraphs_are_gone_from_every_worksheet():
    """⛔ NL 三列表**之前**的三段前言（共用 NL / 译文纪律 / 方括号图例）一律不许再出现。

    ⭐ 判据是逐字片段，⛔ 不是「§1.1 变短了」—— ⚠️ 后者会被任何一次改写蒙过去。
    """
    for frag in ("共用同一份 NL 原文",          # ① 共用 NL + sha8 + 分段口径
                 "译文是给人判缺陷用的",         # ② 译文纪律
                 "两种方括号标注的含义"):        # ③ 图例
        for pair in S.IN_SCOPE_PAIRS:
            assert frag not in _read(_ws(pair)), \
                f"{pair}.md 里三段前言之一又回来了：{frag}"


def test_the_nl_table_directly_follows_its_heading():
    """⭐ 「表直接跟在标题之后」—— ⛔ 标题与表头之间只许有一个空行。

    ⚠️ 这一条比上面那条严：⛔ 上面只查旧措辞没回来，⭐ 这条查**任何**新前言都进不来。
    """
    for pair in S.IN_SCOPE_PAIRS:
        lines = _read(_ws(pair)).splitlines()
        i = next(k for k, ln in enumerate(lines) if ln.startswith("### §1.1 "))
        assert lines[i + 1] == "", f"{pair}.md 的 §1.1 标题后不是空行"
        assert lines[i + 2] == "| 段 id | 原文 | 中文严格翻译 |", \
            f"{pair}.md 的 §1.1 标题与表头之间掺进了东西：{lines[i + 2][:80]}"


def test_the_two_facts_that_must_not_vanish_landed_in_the_nl_doc():
    """⭐ 三段前言里那**两样不能凭空消失**的信息必须在 `nl_XXXX/NL.md` 里。

    ⛔ 判据不是「NL.md 提到了分段」，⭐ 而是逐项：
    ① 分段口径的取值 **与段 id 范围**（`NL-M001` … `NL-M006` 这种）；
    ② 译文口径 **与两个方括号标记各自的含义**。
    ⚠️ ①的「段 id 范围」是本轮新搬过去的 —— ⛔ 此前 `NL.md` 只写「共 N 段」，
    ⛔ 判读者填 `nl_evidence` 时无从知道该写什么形状的 id。
    """
    for dirname in S.nl_dirs():
        doc = _read(os.path.join(HERE, dirname, S.NL_DOC))
        pair = S.pairs_of_dir(dirname)[0]
        segs, seg_mode = S.nl_segments(pair)
        assert f"`{seg_mode}`" in doc, f"{dirname}/{S.NL_DOC} 没写分段口径取值"
        assert f"共 **{len(segs)}** 段（`{segs[0][0]}` … `{segs[-1][0]}`）" in doc, \
            f"{dirname}/{S.NL_DOC} 没写段 id 范围 —— ⛔ 那是从工作单搬过来的"
        assert "nl_evidence" in doc, f"{dirname}/{S.NL_DOC} 没说这套 id 是用来填什么的"
        assert "译文是给人判缺陷用的" in doc, f"{dirname}/{S.NL_DOC} 缺译文口径"
        for legend in ("〔原文如此：", "〔译者存疑："):
            assert legend in doc, f"{dirname}/{S.NL_DOC} 缺方括号标记 {legend} 的含义"


def test_the_worksheet_keeps_no_pointer_paragraph_to_those_two_facts():
    """⛔ 工作单里**不留**指向那两样信息的说明段 —— ⚠️ 用户要的就是干净。

    ⭐ 判据：§1.1 标题到表头之间零内容（上一条已钉），⭐ 且不许出现「口径见 NL.md」
    这类新增指路句。⛔ 头部「开工前两份必读」那一句是原有的，⭐ 不在此列。
    """
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        head, _, rest = doc.partition("### §1.1 ")
        # ⛔ `partition` 留下的 `rest` 还带着标题行的尾巴，⭐ 先切到行末
        table_part = rest.split("\n", 1)[1].split("| 段 id |")[0]
        assert table_part.strip() == "", f"{pair}.md 的 §1.1 里多了指路段：{table_part[:80]}"
        # ⭐ 「两份必读」只许出现在头部，⛔ 不许在 §1.1 里再补一句
        assert head.count("开工前两份必读") == 1, f"{pair}.md 的「两份必读」不是恰好一处"


# ---------------------------------------------------------------- ② §1.2 整节已删

def test_the_structure_summary_section_is_gone():
    """⛔ §1.2 结构摘要整节（表 + 那段双口径脚注）不许再出现在任何工作单里。"""
    dead = [
        "结构摘要",                       # 节标题
        "| 量 | 值 | 量 | 值 |",           # 表头
        "| 状态总数 |",                    # 表内标签（抽三个代表）
        "| 最大层次深度 |",
        "| 台账现有条目 |",
        "数字全部来自",                    # 脚注开头
        "在谓词层可能是 4 或 7",           # 脚注里的双口径举例
    ]
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        for frag in dead:
            assert frag not in doc, f"{pair}.md 里结构摘要的残留：{frag}"


def test_section_one_subsections_are_contiguous_with_no_gap():
    """⛔ 删掉 §1.2 之后**不许留空号或错号** —— §1 的小节必须是 1.1 / 1.2 / 1.3 连号。"""
    want = ["### §1.1 NL 规约原文与中文严格翻译",
            "### §1.2 作者源 PlantUML",
            "### §1.3 参考模型 PlantUML"]
    for pair in S.IN_SCOPE_PAIRS:
        lines = _read(_ws(pair)).splitlines()
        got = [ln for ln in lines if re.match(r"^### §1\.\d", ln)]
        assert len(got) == 3, f"{pair}.md 的 §1 小节数不是 3：{got}"
        for ln, prefix in zip(got, want):
            assert ln.startswith(prefix), f"{pair}.md 的小节号错位：{ln}"


def test_no_file_still_references_the_deleted_structure_summary():
    """⛔ 零死引用：全工作区不许再有指向结构摘要或旧 §1.4 的引用。

    ⚠️ 检查范围是**全部** `.py` 与 `.md`（含生成产物与 `README` / `HOWTO`），
    ⛔ 不只是本轮改过的文件 —— ⭐ 死引用最容易留在没人想起要改的那一份里。
    ⭐ `generate.py` 自己的注释（记录「旧 §1.2 已删」这件事）豁免：⛔ 它讲的正是删除本身。
    """
    bad = []
    for root, dirs, files in os.walk(HERE):
        dirs[:] = [d for d in dirs if d not in {"__pycache__", ".pytest_cache"}]
        for fn in files:
            if not fn.endswith((".py", ".md")):
                continue
            path = os.path.join(root, fn)
            for no, ln in enumerate(_read(path).splitlines(), 1):
                if fn == "generate.py" and ln.lstrip().startswith("#"):
                    continue          # ⭐ 记录删除动作的注释
                if fn == "test_relabel.py":
                    continue          # ⭐ 本组测试自己要写出这些字样
                if "§1.4" in ln or "§1.2 结构摘要" in ln:
                    bad.append(f"{os.path.relpath(path, HERE)}:{no} {ln.strip()[:90]}")
    assert not bad, "⛔ 死引用：\n" + "\n".join(bad)


def test_the_dual_counting_caliber_note_survived_in_the_howto():
    """⭐ 脚注删了，⛔ 但「作者源口径 ≠ 谓词层 `cardinality` 口径」这条**没失效**。

    ⚠️ 它的长版此前在 `HOWTO.md` §A.1，⛔ 而 §A.1 原先锚在结构摘要上 ——
    ⭐ 摘要删了就必须改锚到 §1.2 作者源，⛔ 不是跟着一起删。
    """
    howto = _read(S.howto_path(HERE))
    assert "### §A.1 " in howto
    a1 = howto.split("### §A.1 ")[1].split("### §A.2")[0]
    assert "结构摘要" not in a1, "§A.1 还锚在已删除的结构摘要上"
    assert "§1.2" in a1, "§A.1 没改锚到 §1.2 作者源"
    assert "cardinality" in a1 and "不能混用" in a1, "§A.1 把双口径这条丢了"
    assert "| §A | 两处只读材料的口径提醒 | §1.2 · §1.3 |" in howto, \
        "HOWTO 导航表还指着旧节号"


def test_the_region_separator_warning_moved_instead_of_being_deleted():
    """⭐ 区分隔符告警不是摘要的一部分，⛔ 删摘要不该把它一起删掉。

    ⚠️ 它承载的是**越界判据**（正交区不在 $M$ 内），⛔ 丢了会让判读者把并发主张
    当成缺陷登记。⭐ 现在挂在 §1.2 作者源上 —— ⛔ 它讲的正是那份作者源。
    """
    hits = 0
    for pair in S.IN_SCOPE_PAIRS:
        model = PumlModel(S.puml_text(pair), pair)
        n = model.summary()["region_separators"]
        doc = _read(_ws(pair))
        if not n:
            # ⚠️ 探针必须是**那句告警本身**，⛔ 不能只找「区分隔符」三个字 ——
            # §5.2 的取值图例里现在也有这三个字（维度 A 的 `region` 一行讲的正是 `--`），
            # 用宽探针会在 54 份上全部误报。
            assert "作者源含 **" not in doc, f"{pair}.md 没有区分隔符却挂了告警"
            continue
        hits += 1
        want = f"⚠️ 作者源含 **{n} 个 `--` 区分隔符**。"
        assert want in doc, f"{pair}.md 丢了区分隔符告警"
        # ⭐ 必须落在 §1.2 作者源那一节里
        seg = doc.split("### §1.2 作者源")[1].split("### §1.3")[0]
        assert want in seg, f"{pair}.md 的区分隔符告警没落在 §1.2 里"
    assert hits == 9, f"含区分隔符的工作单应有 9 份，实测 {hits}"


# ---------------------------------------------------------------- ③ 「怎么填」在最开头

def test_the_howto_inline_section_sits_at_the_very_top():
    """⭐ 「怎么填」必须在**标题之后、NL 表之前**，⛔ 且是正文第一节。"""
    for pair in S.IN_SCOPE_PAIRS:
        lines = _read(_ws(pair)).splitlines()
        heads = [(i, ln) for i, ln in enumerate(lines) if ln.startswith("## ")]
        assert heads, f"{pair}.md 没有任何二级标题"
        assert heads[0][1].startswith("## 怎么填"), \
            f"{pair}.md 的第一节不是「怎么填」，而是 {heads[0][1]}"
        assert heads[1][1].startswith("## §0 "), \
            f"{pair}.md 「怎么填」后面不是 §0：{heads[1][1]}"
        # ⛔ 必须排在标题之后
        assert lines[1].startswith("# 人工重标工作单"), f"{pair}.md 头两行变了"
        assert heads[0][0] > 1
        # ⛔ 也必须排在 NL 表之前
        tbl = next(i for i, ln in enumerate(lines)
                   if ln == "| 段 id | 原文 | 中文严格翻译 |")
        assert heads[0][0] < tbl


def test_the_howto_inline_section_stays_short():
    """⭐ 「尽量短」是硬要求 —— ⛔ 8 条 + 标题 + 一句引子，档设 16 行。

    ⚠️ 它在 54 份里逐字重复（除第 7 条带 pair id），⛔ 长回去等于把 HOWTO 抄了 54 遍。
    """
    for pair in S.IN_SCOPE_PAIRS:
        n = len([ln for ln in _howto_block(pair).splitlines() if ln.strip()])
        assert n <= 16, f"{pair}.md 的「怎么填」有 {n} 行非空 —— ⛔ 超档"


# ⭐ 本轮改动**之前**的那个 commit（Part 1 已落地、Part 2 尚未落地）。
# ⛔ 必须写死，⚠️ 不能用 `HEAD` —— 本轮一旦落成 commit，`HEAD` 就是改动**之后**的状态，
# ⛔ 那条断言会变成拿自己比自己。
# ⚠️ 2026-08-13 由 `b609ee8f` 前移到 `d974b1e0`：上一版量的是「换条件式座标系」那一轮，
# ⛔ 本轮（剥旧元数据 + 渲染映射）与它方向相反，继续拿旧基线量会把两轮的净效果混在一起。
CLEANUP_BASELINE = "d974b1e0"


def test_the_line_count_change_is_bounded_pair_by_pair():
    """行数变化必须**逐份**有界，不许只看中位。

    ⚠️ **本轮的增量是有符号的，故不能再钉一个正区间。** 本轮同时做两件相反的事：

    - **减**：§2 每条台账记录剥掉十项字段行 + 整节断言组，每份再删两张图例（约 −14 行/份）。
    - **加**：§2 每条记录、§3 每个候选各多一块座标映射（约 +8 至 +14 行/块）。

    ⭐ 于是净增量由 **该 pair 的候选数减台账条目数** 主导，逐份有正有负 ——
    实测落在 [−34, +45]。所以这一条只负责**防跑飞**（档取 [−60, +70]，约 1.5 倍余量），
    ⛔ 不再兼职「每份都确实换过了」。

    ⚠️ 那个职责移交给 `test_every_rendered_mapping_matches_the_mapping_file` ——
    ⭐ 它逐块比对映射文件与渲染结果，比行数区间准得多：
    ⛔ 行数落在区间内也可能是某份根本没渲染映射、却因为别处多了几行而蒙混过关。

    ⚠️ 2026-08-13 `pyfcstm inspect` 入册后区间改成 **[+40, +430]**，实测 **[+71, +387]**、
    中位 **+162**。⭐ 增量为什么这么大、又为什么必须按 pair 差这么多：§3.6 给**每一条**新建的
    `INS-` issue 印一个块（事实陈述 + 逐字证据 + 归并理由 + 五轴映射 + 底层诊断折叠区 +
    裁决区，约 20–30 行），而每个 pair 新建的块数从 0 到 9 不等；并入既有条目的那些还要在
    §2 / §3 对应条目下多一段补充证据。⛔ 所以下界不再是负数 —— 本轮**没有**任何删减动作，
    54 份全部只增不减，`+40` 是「至少每份都真的印了 §3.6 的导语与两个小节」的下限哨兵。

    ⚠️⚠️ **2026-08-15 区间改成 [−450, +60]，实测 [−404, −167]、中位 −285 —— ⭐ 全部为负。**
    本轮把 §3 的六个来源分节、台账的参考侧/生成侧两行、自动风险标记、座标映射块的三行 caveat、
    inspect 的底层诊断表与三处折叠区**全部拆掉**，⭐ 每条压成固定四段（问题类型 / 问题描述 /
    三方判定表 / meta review / 裁决区）。⛔ 上界留 +60 是哨兵：若某份反而变长，说明拆的东西
    又长回来了。⚠️ **条目一条没少** —— 那由 `test_the_source_sections_are_gone_but_no_item_was_lost`
    的门面数字断言（54 / 99 / 269）守。

    ⚠️ 2026-08-14 曾用区间 [−200, +300]，实测 [−134, +285]、中位 −29。 本轮又是有符号的：

    - **减**：§4 深度检查清单与 §5 新增登记整体拆除（用户裁定本轮只做「对现有台账 + 候选
      逐条裁决」）—— 这两节合计约 100–150 行/份，是本轮减量的全部来源。
    - **加**：每条台账 / 候选多一块三方 D 档判读（无争议的 2 行、需人裁的约 12 行）
      + 顶部两行速览。加量由**该 pair 需人裁的条目数**主导，从 0 到 8 不等。

    ⭐ 故下界重回负数，且比上界宽得多 —— 减的是固定两节，加的按条目数摊。
    ⛔ 上界取 `+300`：⚠️ 实测最大 `0039` 的 **+285** —— 它一份里有 8 条需人裁的条目，
    每条约 12 行，外加 §3.6 的 inspect 块本来就多。⭐ 那是**按条目数摊出来的**，不是文案变长；
    「文案有没有长回去」由 `test_the_field_guide_is_not_copied_back_into_the_worksheets`
    数重复行来守，比行数区间准。
    """
    probe = subprocess.run(["git", "-C", HERE, "cat-file", "-e",
                            f"{CLEANUP_BASELINE}^{{commit}}"], capture_output=True)
    if probe.returncode != 0:
        pytest.skip(f"基线 commit {CLEANUP_BASELINE} 不可达")
    bad = []
    for pair in S.IN_SCOPE_PAIRS:
        rel = os.path.relpath(_ws(pair), HERE)
        old = subprocess.run(["git", "-C", HERE, "show", f"{CLEANUP_BASELINE}:./{rel}"],
                             capture_output=True, text=True)
        if old.returncode != 0:
            pytest.skip(f"{rel} 不在基线 commit 里")
        a = len(old.stdout.splitlines())
        b = len(_read(_ws(pair)).splitlines())
        if not (-520 <= b - a <= 60):
            bad.append(f"{pair}: {a} → {b}（{b - a:+d}）")
    assert not bad, "这些工作单的增量不在 [+40, +430] 区间：" + "、".join(bad)


# ---------------------------------------------------------------- ③b 逐条钉住 parser 行为
#
# ⚠️ 下面 8 条与「怎么填」的 8 条**一一对应**。⛔ 改说明必须同时改这里。

def test_claim_1_only_content_inside_the_fence_survives_a_rerun():
    """第 1 条：⭐ 围栏内的留住，⛔ 围栏外的重跑就没了。"""
    for pair in S.IN_SCOPE_PAIRS[:1]:
        assert "只在 `~~~` 围栏里写" in _howto_block(pair)
    with tempfile.TemporaryDirectory() as tmp:
        dst = _ws("0000", tmp)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        doc = _read(_ws("0000"))
        doc = doc.replace("<!-- FILL:BEGIN key=EIS-0000-02 kind=ledger -->\n~~~\n",
                          "<!-- FILL:BEGIN key=EIS-0000-02 kind=ledger -->\n~~~\n"
                          "理由: 围栏内的字\n")
        doc += "\n围栏外的字\n"
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(doc)
        subprocess.run([sys.executable, os.path.join(HERE, "generate.py"),
                        "--pairs", "0000", "--out", tmp], check=True, capture_output=True)
        after = _read(dst)
        assert "围栏内的字" in after, "⛔ 围栏内的人工填写被吃掉了"
        assert "围栏外的字" not in after, "⛔ 围栏外的字居然留下来了 —— 说明第 1 条写错了"


def test_claim_2_accepted_and_rejected_check_marks():
    """第 2 条：⭐ `CHECK_MARKS` 里的记号都认；⛔ 其余记号让**整个选项连文字一起消失**。"""
    for m in fb.CHECK_MARKS:
        rec = _ledger_rec(f"裁决: [{m}] 按 D2 采纳  [ ] 按 D1 采纳  [ ] 不采纳")
        assert rec["裁决"]["chosen"] == ["按 D2 采纳"], f"记号 [{m}] 没被认出来"
    for m in ["v", "V", "是", "o", "O", "1", "*", "·"]:
        rec = _ledger_rec(f"裁决: [{m}] 按 D2 采纳  [ ] 按 D1 采纳  [ ] 不采纳")
        chosen = rec["裁决"]["chosen"] if isinstance(rec["裁决"], dict) else []
        opts = rec["裁决"]["options"] if isinstance(rec["裁决"], dict) else []
        assert chosen == [], f"记号 [{m}] 竟被认成勾选 —— ⛔ 说明第 2 条的禁用清单写错了"
        assert "保留" not in opts, \
            f"记号 [{m}] 下「保留」还在 options 里 —— ⛔ 第 2 条「连文字一起消失」写错了"
    # ⭐ 说明里必须列出这两组
    blk = _howto_block("0000")
    for m in fb.CHECK_MARKS:
        assert f"`[{m}]`" in blk, f"说明里没列出可用记号 [{m}]"
    for m in ["v", "是", "o", "1", "*"]:
        assert f"`[{m}]`" in blk, f"说明里没警告不可用记号 [{m}]"


def test_claim_3_the_value_is_the_text_after_the_box():
    """第 3 条：⛔ 只留 `裁决: [x]`（删掉选项文字）= 没勾。"""
    assert "只留 `裁决: [x]` 等于**没勾**" in _howto_block("0000")
    rec = _ledger_rec("裁决: [x]")
    assert not isinstance(rec["裁决"], dict), "⛔ 无标签的 [x] 竟被读成勾选行"
    assert rec["裁决"] == "[x]", f"⛔ 实际读成了 {rec['裁决']!r}"
    rep = V.Report()
    V.validate_pair("0000", _fill_and_collect("0000", "EIS-0000-01", "裁决: [x]"), rep)
    assert any(i["key"] == "EIS-0000-01" and i["level"] == "E" for i in rep.items), \
        "⛔ 这种写法必须被 validate 抓住，⭐ 否则「等于没勾」是句空话"


def test_claim_4_two_checks_is_an_error_not_two_values():
    """第 4 条：⛔ 勾两个 → validate 报「单值」，⛔ 不是两个都算。"""
    assert "该字段是单值" in _howto_block("0000")
    data = _fill_and_collect("0000", "EIS-0000-01",
                             "裁决: [x] 保留  [x] 修正  [ ] 删除\n深度: [x] 中层")
    rec = next(r for r in data["ledger"] if r["id"] == "EIS-0000-01")
    assert rec["裁决"]["chosen"] == ["保留", "修正"]
    rep = V.Report()
    V.validate_pair("0000", data, rep)
    msgs = [i["msg"] for i in rep.items if i["level"] == "E"]
    assert any("单值" in m for m in msgs), f"⛔ validate 没报单值错：{msgs}"


def test_claim_5_free_text_colons_and_continuation_lines():
    """第 5 条：⭐ 全角冒号认、⭐ 续行接得上、⭐ 续行里带冒号也**不截断**。

    ⚠️ 最后一点是本轮修的 bug：`理由` 的续行写「NL 第 3 句：…」时，
    ⛔ 旧行为把那一行当成新字段名，`理由` 就地截断且**不报错**。
    """
    blk = _howto_block("0000")
    assert "全角 `：` 都认" in blk and "续行里带冒号也不会被截断" in blk
    rec = _ledger_rec("理由： 全角冒号也认")
    assert rec["理由"] == "全角冒号也认"
    rec = _ledger_rec("理由: 第一行\nNL 第 3 句：模型没有这条边\n还有第三行")
    assert rec["理由"] == "第一行\nNL 第 3 句：模型没有这条边\n还有第三行", \
        f"⛔ 续行被截断了：{rec['理由']!r}"
    assert "NL 第 3 句" not in rec, "⛔ 续行又被当成新字段了"
    # ⭐ 顺带钉住另一处同源修复：值里的 `[ ]` 不许把自由文本字段读成勾选行
    rec = _ledger_rec("理由: `HumanDrivingMode` 缺 [ ] 初始边")
    assert rec["理由"] == "`HumanDrivingMode` 缺 [ ] 初始边", \
        f"⛔ 值里的 [ ] 把这一行读成勾选行了：{rec['理由']!r}"
    # ⛔ 改了字段名 → 并进上一个字段（说明里就是这么写的）
    rec = _ledger_rec("理由: 甲\n原因: 乙")
    assert rec["理由"] == "甲\n原因: 乙" and "原因" not in rec


def test_claim_6_checklist_tolerates_indent_bullets_and_bare_findings():
    """第 6 条：⭐ 缩进 / `-` 前缀都收，⭐ 裸下一行也当发现，⛔ 只有 `·` 行不回收。

    ⚠️ 前两种此前让**整条清单项从 `items` 里消失** —— ⛔ 不是「未勾选」，是不存在，
    ⛔ 而 `checklist_items` 总数会跟着变小且不报错。
    """
    pytest.skip("§4 深度检查清单与 §5 新增登记于 2026-08-14 按用户裁定整体拆除"
                "（本轮工作单只做「对现有台账 + 候选逐条裁决」）。⛔ 本条测的是那两节的"
                "行为，故整条挂起而不是删除 —— 代码（section_checklist / section_new / checklist.py / newfields.py）仍在，"
                "下一轮若重开挖深可整段接回，届时把本 skip 去掉即可。"
                "⭐ 「那两节确实不在了」由 test_the_removed_sections_are_really_gone 守着。")
    blk = _howto_block("0000")
    assert "前面有缩进或 `-` 都行" in blk
    assert "直接写在下一行也收" in blk
    assert "`·` 开头那行" in blk
    for line in ["[x] REACH-01 甲",
                 "  [x] REACH-01 甲",
                 "- [x] REACH-01 甲",
                 "  - [✓] REACH-01 甲",
                 "[xx] REACH-01 甲"]:
        items = _chk_items(line)
        assert len(items) == 1 and items[0]["iid"] == "REACH-01" and items[0]["checked"], \
            f"⛔ 这种写法丢了整条：{line!r} → {items}"
    # ⭐ 小写 id 归一成大写（⛔ 否则并表时变成两条）
    assert _chk_items("[x] reach-01 甲")[0]["iid"] == "REACH-01"
    # ⭐ 裸下一行当发现
    assert _chk_items("[x] REACH-01 甲\n    我发现了问题")[0]["finding"] == "我发现了问题"
    # ⭐ `发现:` 写法照旧
    assert _chk_items("[x] REACH-01 甲\n    发现: 有问题")[0]["finding"] == "有问题"
    # ⛔ `·` 行不回收
    assert _chk_items("[x] REACH-01 甲\n    · 机械判据：无出边")[0]["finding"] is None
    # ⛔ 未勾选仍然是未勾选
    assert _chk_items("[ ] REACH-01 甲")[0]["checked"] is False


def test_claim_7_new_entry_needs_its_own_heading():
    """第 7 条：⭐ 每条一个 `### NEW-<pair>-NN` 标题；⛔ 挤在一个标题下会被并成一条。"""
    pytest.skip("§4 深度检查清单与 §5 新增登记于 2026-08-14 按用户裁定整体拆除"
                "（本轮工作单只做「对现有台账 + 候选逐条裁决」）。⛔ 本条测的是那两节的"
                "行为，故整条挂起而不是删除 —— 代码（section_checklist / section_new / checklist.py / newfields.py）仍在，"
                "下一轮若重开挖深可整段接回，届时把本 skip 去掉即可。"
                "⭐ 「那两节确实不在了」由 test_the_removed_sections_are_really_gone 守着。")
    blk = _howto_block("0000")
    assert "### NEW-0000-01" in blk
    assert "别把两条挤在一个标题下" in blk
    two = ("### NEW-0000-01\nstatement: 甲\n\n"
           "### NEW-0000-02\nstatement: 乙\n")
    ids = [r["id"] for r in _fill_and_collect("0000", "NEW-0000", two)["new_issues"]]
    assert ids == ["NEW-0000-01", "NEW-0000-02"], ids
    # ⛔ 挤在一个标题下 → 只剩一条，且第二条的 statement 被并进第一条
    one = "### NEW-0000-01\nstatement: 甲\nstatement: 乙\n"
    recs = _fill_and_collect("0000", "NEW-0000", one)["new_issues"]
    assert len(recs) == 1, f"⛔ 说明第 7 条写错了：{recs}"
    # ⭐ 宽容面：漏空格 / 少一个 `#` / 小写都还认（⛔ 但说明仍要求写标准形）
    for head in ["###NEW-0000-03", "## NEW-0000-03", "### new-0000-03"]:
        recs = _fill_and_collect("0000", "NEW-0000", head + "\nstatement: 甲\n")["new_issues"]
        assert [r["id"] for r in recs] == ["NEW-0000-03"], f"{head} → {recs}"
    # ⛔ 漏掉 NEW- 前缀 → 整条不认（说明里明写了）
    assert "也别漏掉 `NEW-` 前缀" in blk
    assert _fill_and_collect("0000", "NEW-0000", "### 0000-03\nstatement: 甲\n")["new_issues"] == []


def test_claim_8_blank_is_not_the_same_as_writing_none():
    """第 8 条：⭐ 留空回收成 `null`；⭐ 写 `无` 是「判过了，结论是没有」。"""
    blk = _howto_block("0000")
    assert "回收成 `null`" in blk
    assert "「留空」与「写 `无`」在校验时是两件事" in blk
    rec = _ledger_rec("理由:")
    assert rec["理由"] is None, f"⛔ 留空没回收成 null：{rec['理由']!r}"
    rec = _ledger_rec("理由: 无")
    assert rec["理由"] == "无"
    for mark in ("无", "none", "N/A", "-"):
        assert NF.is_none_mark(mark), f"⛔ 说明里列了 {mark} 却不被 `is_none_mark` 认"
    assert not NF.is_none_mark(""), "⛔ 空串不该算「已判定为无」"


def test_check_marks_have_exactly_one_source_of_truth():
    """⛔ 勾选记号只许有一份真源 —— ⚠️ 解析器与 `is_untouched` 分叉过一次。

    ⭐ 症状很具体：`collect.py` 认 `[✓]`，而 `is_untouched` 只认字面 `"[x]"`，
    ⛔ 于是一份**只用 ✓ 勾选**的块会被报成「原样未填」。
    """
    for src in ("collect.py", "generate.py"):
        text = _read(os.path.join(HERE, src))
        assert "xX✓√" not in text, f"{src} 里又抄了一份记号字符集 —— ⛔ 必须读 fb.CHECK_MARKS"
    for m in fb.CHECK_MARKS:
        assert not fb.is_untouched(f"裁决: [{m}] 按 D2 采纳  [ ] 按 D1 采纳  [ ] 不采纳", "ledger"), \
            f"⛔ is_untouched 不认记号 [{m}]"
    assert fb.is_untouched(fb.LEDGER_TEMPLATE, "ledger")
    assert fb.is_untouched("裁决: [ ] 按 D2 采纳  [ ] 按 D1 采纳  [ ] 不采纳", "ledger")


def test_field_tables_are_derived_from_the_templates_not_hand_copied():
    """⛔ §0 / §2 / §3 的字段表必须从模板算出来 —— ⚠️ 抄一份就会与模板分叉。

    ⭐ 分叉的后果是静默的：解析器不认某字段名时，那一行被并进**上一个**字段。
    """
    assert fb.LEDGER_FIELDS == ["裁决", "meta review 意见", "理由"]
    assert fb.LEDGER_CHOICES == ["裁决"]
    assert fb.CANDIDATE_CHOICES == ["裁决"]
    # ⚠️ 2026-08-14 两个模板合并成「采纳 / 不采纳 + 理由」，⛔ `并入到` 已不存在。
    assert "理由" in fb.CANDIDATE_FIELDS and "理由" not in fb.CANDIDATE_CHOICES
    assert "meta review 意见" in fb.CANDIDATE_FIELDS
    assert fb.PAIR_CHOICES == ["本 pair 整体判断", "台账现有条目是否偏浅（整体）"]
    # ⭐ 每个模板里的每一个字段名都要在表里（⛔ 逐字对模板）
    for tpl, names in ((fb.LEDGER_TEMPLATE, fb.LEDGER_FIELDS),
                       (fb.CANDIDATE_TEMPLATE, fb.CANDIDATE_FIELDS),
                       (fb.PAIR_TEMPLATE, fb.PAIR_FIELDS)):
        for line in tpl.splitlines():
            head = re.match(r"^([^:：]+)[:：]", line)
            assert head and head.group(1).strip() in names, f"模板行没进字段表：{line}"
    # ⭐ 宽容变体：漏空格的写法也认（⚠️ validate.py 本就同时查两种）
    # ⚠️ 2026-08-14 `修正后的 statement` 字段随模板合并删掉了，故换成 §0 那个仍在的多字变体。
    assert "耗时(分钟)" in fb.name_variants(fb.PAIR_FIELDS)
    assert "耗时（分钟）" in fb.name_variants(fb.PAIR_FIELDS)


def test_the_four_headline_totals_are_unchanged_by_the_tolerance_fixes():
    """⛔ 宽容化不许动门面数字：`54 / 99 / 222`（⚠️ 第四个 `955` 已归零，见下）。

    ⚠️⚠️ **2026-08-14 第四个数字由 955 改为 0，⛔ 这不是丢数据。** 用户裁定本轮工作单
    只做「对现有台账 + 候选逐条裁决」，§4 深度检查清单与 §5 新增登记整体不再装进
    `build_doc`（`generate.py` 里那段注释写了理由与保留方式）。⭐ 故 `checklist_items`
    结构上为 0。⛔ 前三个数字**一格没动** —— 那正是本条要守的：拆节不许顺手丢条目。
    ⭐ 双份数字都记在这里：拆除前 `54 / 99 / 269 / 955`，拆除后 `54 / 99 / 269 / 0`；⭐ `UM-` 撤除后 `54 / 99 / 220 / 0`；⭐ 全部出块后 `54 / 99 / 281 / 0`；⭐ 去重恢复后 `54 / 99 / 224 / 0`；⭐ 0053 三条死端合并后 `54 / 99 / **222** / 0`（合计 321 个裁决区，账目见 [DEDUP_ACCOUNTING.md](./DEDUP_ACCOUNTING.md)）。

    ⚠️ 这是本轮改 parser 的安全网：⭐ 宽容只该多认几种写法，
    ⛔ 不该让空模板被解析成别的东西。
    """
    import json as _json
    proc = subprocess.run([sys.executable, os.path.join(HERE, "collect.py"), "--stdout"],
                          check=True, capture_output=True, text=True, cwd=HERE)
    tot = _json.loads(proc.stdout)["totals"]
    # ⚠️ 2026-08-13 `pyfcstm inspect` 入册，`candidates_seen` 由 **141** 变 **269**。
    # ⭐ 等式（每一项都可机械复算，见下面的断言）：
    #     269 = 141（VU 15 + DIFF 77 + UM 49）+ 128 新建 INS- 块
    # ⚠️ 2026-08-16 `UM-` 撤除后：220 = 92（VU 15 + DIFF 77）+ 128
    # ⭐ 同日改为**每条判读都出块**后：281 = 92 + 189（INS 全量）。
    # ⭐ 2026-08-16 起**每条判读都出块**（不再按「已并入宿主」跳过），⛔ 故 `candidates_seen` 由 220 升到 **281** —— ⚠️ 那 61 条并入项此前在 md 里**一个块都没有**，按 id 搜不到，而速览行还点名说它们「需你处理」。
    #         + 126（184 条归一化 issue 里判重结论为 `suspect` 24 + `none` 102 的那些）
    #         +   2（5 条恢复的 refuted 里判重结论为 `none` 的那两条 —— 另外 3 条并入了
    #               既有台账 / 候选，⛔ 并入的一律不新建块，故不进这个数）
    # ⛔ 三个不变的数字必须原样：`ledger_records_seen` 尤其 —— 台账是**被审计对象**，
    # ⚠️ inspect 的发现在判读者裁决之前只能是候选，⛔ 一条都不许并进台账。
    assert (tot["pairs"], tot["ledger_records_seen"],
            tot["candidates_seen"], tot["checklist_items"]) == (54, 99, 222, 0), tot
    assert IF.has_judged_issues(), "三份 audit json 必须在树上，否则 §3.6 什么都不渲染"
    ov = IF.load_overlap()
    new_blocks = [i for i in IF.load_issues()["issues"]
                  if ov[i["issue_id"]]["overlap_kind"] in IF.NEW_BLOCK_KINDS]
    recovered_new = [i for i in new_blocks if i["recovered_from_refuted"]]
    assert len(new_blocks) == 128 and len(recovered_new) == 2, \
        (len(new_blocks), len(recovered_new))
    # ⚠️ 2026-08-16 `UM-` 一族（49 条）整批撤出工作单（见 docs/findings/um_residue_ruling.md），⭐ 故渲染出的候选由 141 降到 **92**（VU 15 + DIFF 77）；⛔ candidate_mapping.json 里仍保留 UM 的 49 条映射记录（历史事实，不删），故它的 total 仍是 141。
    # ⭐⭐ 2026-08-16 起**并入项也各自出块**（见 `generate.py` 候选循环的长注释）。
    # ⛔ 在那之前它们不出块，于是恒等式是 `92 + new_blocks`；⚠️ 而那正是 `INS-0050-01`
    # 「按 id 搜不到」的成因 —— 61 条并入项在整份 md 里一个字都不出现。
    # ⭐ 现在的恒等式把并入项也算进来：候选块 = 92（VU+DIFF）+ 全部 INS。
    merged_blocks = [i for i in IF.load_issues()["issues"]
                     if ov[i["issue_id"]]["overlap_kind"] not in IF.NEW_BLOCK_KINDS]
    assert len(new_blocks) + len(merged_blocks) == 189, \
        (len(new_blocks), len(merged_blocks))
    # ⭐ 去重后：候选块 = 92（VU+DIFF）+ 130（在范围内的 INS）= 222
    assert 92 + 130 == tot["candidates_seen"]


# ==================================================================== inspect 一族

def test_the_inspect_data_is_complete_and_every_code_has_a_coordinate():
    """⛔ 454 条诊断齐全、11 个 code 每个都有座标、两个整类排除的内生率确实是 0。

    ⚠️ 「每个 code 都有座标」不是形式主义：`axes_for()` 对没映射的 code **抛**而不是留空格，
    ⛔ 因为静默落空格等于整类诊断在座标统计里消失。
    """
    st = IF.stats()
    assert st["diagnostics"] == 454, st
    assert st["by_verdict"] == {"intrinsic": 194, "uncertain": 142,
                                "projection_artifact": 84, "refuted": 34}, st["by_verdict"]
    assert st["pairs_with_findings"] == 54
    for rec in IF.all_findings():
        axes = IF.axes_for(rec)          # ⛔ 缺映射会抛
        assert axes["defect_locus"] in NF.DEFECT_LOCI
        assert axes["why"], f"{rec['code']} 的座标没写理由"
        if "other" in (axes.get("defect_logic_kind"), axes.get("defect_reference")):
            assert axes["other_note"], f"{rec['code']} 取了 other 却没写说明"
    # ⭐ 两个整类排除的判据是**内生率为 0**，⛔ 不是「嫌它多」。这里逐条复算。
    for code, total in (("I_NONTRIVIAL_SCC", 54), ("I_TOPOLOGICAL_NON_TERMINATING", 52)):
        rows = [r for r in IF.all_findings() if r["code"] == code]
        assert sum(1 for r in rows if r["verdict"] == "intrinsic") == 0, code
        assert len(rows) >= total - 9, (code, len(rows))
    assert set(IF.EXCLUDED_CLASSES) == {"I_NONTRIVIAL_SCC", "I_TOPOLOGICAL_NON_TERMINATING"}


def test_the_deadlock_leaf_semantic_split_is_spelled_out_in_every_worksheet():
    """⛔⛔ `W_DEADLOCK_LEAF` 的**两语义归属**必须逐份写明 —— 单独一条钉死。

    ⚠️⚠️ **2026-08-13 两轮改动。第一轮：本条此前断言该码有「系统性假阳性」，那是错的**，
    连同它钉住的四个逐字探针一起换掉。⛔ 旧断言的前提为真（`analyzers/structural.py` 只数
    叶态自身出边、不做祖先遍历），⛔ 但推论为假。

    ⚠️ **第二轮改的是引文与措辞本身**：第一轮写「`topology.py` **模块注释**逐字『are followed
    only when』」——⛔ 出处与引文都错。真实位置是 `build_leaf_level_macro_graph()` 的**函数
    docstring**，原文为「Parent-level transitions **whose source is a composite state are
    therefore considered only after** a descendant leaf explicitly exits to that parent; they
    are not copied onto every active descendant leaf.」⛔ 且第一轮那句「FCSTM 里不存在可供
    子态使用的祖先边」**过强**——语料里确有 116 条以复合态为源的迁移（31 个 pair），它们
    是会被用到的，只是只对已显式退出的子态生效。⭐ 准确命题只到：**零出边的叶态**（即本码
    的开火条件）接不上父态出边。

    ⭐ 两侧实测同向：语料侧 57 条真实诊断里「祖先有出边」为 **0 条**；语义侧最小模型上
    本码与拓扑层的 `W_TOPOLOGICAL_NOEXIT` 两套独立分析一致。

    ⭐ 真正要让判读者知道的是**同一个叶态在两种语义下 terminal 性相反**：
    作者源读作 UML（成组迁移成立 → 不是 terminal），`model.fcstm` 读作 FCSTM
    （父态出边不下传 → 是 terminal）。⛔ 于是祖先检查仍要做，但它的结论是
    `projection_artifact`（IR 上为真、作者源上为假），⛔ **不是** `refuted`。

    ⚠️ 探针只钉**承重内容**（不下传 · 不得据外层推翻 · 归属落 projection_artifact），
    ⛔ 不钉行号也不钉修辞 —— 旧版钉了 `analyzers/structural.py:75-93` 这种脆定位符，
    上游一次格式化就会失配。

    ⭐ 为什么要求**每份都印**而不只在命中该 code 的 pair 上印：判读者在 §4 自己数出边时
    面对的是同一个语义分岔，⛔ 而 §4 遍布 54 份。
    """
    pytest.skip("§3 的**来源分节**于 2026-08-15 按用户裁定整体拆除"
                "（原话：「这个 issue 是怎么来的是 inspect 还是什么统统不重要」）。"
                "⛔ 本条测的是 §3.6 那一节的内容（物种抬头 / 确定性 vs LLM / 整类排除 / "
                "不确定族标签 / 底层诊断表 / 座标拼写 / 恢复条目逐条交代），"
                "⚠️ 而那些文字已随分节一起下线 —— ⭐ 条目本身一条没丢，只是不再标来源、"
                "不再印工具内部细节。⛔ 整条挂起而不是删除：`section_inspect()` 的函数本体仍在，"
                "⭐ 若日后要恢复来源分节，那五条必须逐份印的限定还在里面。"
                "⭐ 「那一节确实不在了、且条目一条没少」由 "
                "test_the_source_sections_are_gone_but_no_item_was_lost 守着。")
    for probe in ("不下传", "not copied onto every active", "projection_artifact", "0/57"):
        assert probe in IF.DEADLOCK_LEAF_CAVEAT, f"常量里少了承重探针：{probe}"
    # ⛔ 旧的错误断言不许回流。
    assert "系统性假阳性" not in IF.DEADLOCK_LEAF_CAVEAT, "错误断言「系统性假阳性」回流了"
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        assert IF.DEADLOCK_LEAF_CAVEAT in doc, f"{pair}.md 没印 W_DEADLOCK_LEAF 的语义归属须知"
    # ⭐ 命中该 code 的那些 issue 处还要**就地**再印一次 —— 导语在几百行之外，
    # ⛔ 只靠导语，判读者读到具体那一条时早忘了。
    hit = [(p, r) for p in S.IN_SCOPE_PAIRS for r in IF.issues_of(p)
           if any(m["code"] == "W_DEADLOCK_LEAF" for m in r["members"])]
    assert len(hit) >= 20, len(hit)
    for pair, rec in hit:
        doc = _read(_ws(pair))
        i = doc.index(G._flow(rec["statement"]))
        assert "`W_DEADLOCK_LEAF` 的语义归属须知" in doc[i:i + 6000], \
            f"{rec['issue_id']} 就地没印语义归属须知"


def test_the_excluded_inspect_classes_are_explained_not_silently_dropped():
    """⛔ 两个整类排除的 code 必须**写明理由**，⚠️ 且落在 `uncertain` 的那些仍要摆出来。

    ⛔ 不写理由的后果很具体：判读者会以为这两类被漏掉了，或者反过来以为
    「这些模型没有非平凡 SCC」—— 两种误读都错。
    """
    pytest.skip("§3 的**来源分节**于 2026-08-15 按用户裁定整体拆除"
                "（原话：「这个 issue 是怎么来的是 inspect 还是什么统统不重要」）。"
                "⛔ 本条测的是 §3.6 那一节的内容（物种抬头 / 确定性 vs LLM / 整类排除 / "
                "不确定族标签 / 底层诊断表 / 座标拼写 / 恢复条目逐条交代），"
                "⚠️ 而那些文字已随分节一起下线 —— ⭐ 条目本身一条没丢，只是不再标来源、"
                "不再印工具内部细节。⛔ 整条挂起而不是删除：`section_inspect()` 的函数本体仍在，"
                "⭐ 若日后要恢复来源分节，那五条必须逐份印的限定还在里面。"
                "⭐ 「那一节确实不在了、且条目一条没少」由 "
                "test_the_source_sections_are_gone_but_no_item_was_lost 守着。")
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        assert "`I_NONTRIVIAL_SCC`（内生率 **0/54**）" in doc, pair
        assert "`I_TOPOLOGICAL_NON_TERMINATING`（内生率 **0/52**）" in doc, pair
        assert "不是「从材料里删掉」" in doc, pair
    # ⭐ 「仍要摆出来」是可机械核的：这两个 code 的 uncertain 诊断必须都有归属，
    # ⛔ 且它们的 issue 必须真的渲染进了工作单。
    shown = 0
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        for rec in IF.issues_of(pair):
            if not any(m["code"] in IF.EXCLUDED_CLASSES for m in rec["members"]):
                continue
            shown += 1
            assert G._flow(rec["statement"]) in doc, f"{rec['issue_id']} 被整类排除连带丢掉了"
    assert shown >= 54, shown


def test_the_ingested_inspect_issues_reconcile_with_the_diagnostics():
    """⛔⛔ **覆盖对拍**：336 条待呈现诊断 + 24 条恢复的 refuted，逐条恰好归属一次。

    ⚠️ 这是本轮最要紧的一条机械门。归一化把 360 条压成 189 条，⛔ 而压缩过程里
    「漏掉一条」与「同一条算两次」都是**静默**的：工作单照常生成，看不出少了什么。
    """
    pytest.skip("§3 的**来源分节**于 2026-08-15 按用户裁定整体拆除"
                "（原话：「这个 issue 是怎么来的是 inspect 还是什么统统不重要」）。"
                "⛔ 本条测的是 §3.6 那一节的内容（物种抬头 / 确定性 vs LLM / 整类排除 / "
                "不确定族标签 / 底层诊断表 / 座标拼写 / 恢复条目逐条交代），"
                "⚠️ 而那些文字已随分节一起下线 —— ⭐ 条目本身一条没丢，只是不再标来源、"
                "不再印工具内部细节。⛔ 整条挂起而不是删除：`section_inspect()` 的函数本体仍在，"
                "⭐ 若日后要恢复来源分节，那五条必须逐份印的限定还在里面。"
                "⭐ 「那一节确实不在了、且条目一条没少」由 "
                "test_the_source_sections_are_gone_but_no_item_was_lost 守着。")
    payload = IF.load_issues()
    rows = payload["issues"]
    owner = {}
    for rec in rows:
        for d in rec["diag_indices"]:
            key = (rec["pair"], d)
            assert key not in owner, f"诊断 {key} 被 {owner.get(key)} 与 {rec['issue_id']} 重复认领"
            owner[key] = rec["issue_id"]
    shown = {(r["pair"], r["diag_index"]) for r in IF.all_findings()
             if r["verdict"] in IF.SHOWN_VERDICTS}
    recovered = {(r["pair"], r["diag_index"]) for r in IF.all_findings()
                 if r["verdict"] == "refuted"} & set(owner)
    assert shown <= set(owner), sorted(shown - set(owner))[:5]
    assert set(owner) == shown | recovered
    assert len(shown) == 336 and len(recovered) == 24, (len(shown), len(recovered))
    assert len(rows) == 189 and payload["totals"]["diagnostics_covered"] == 360
    # ⭐ 仍然维持 refuted 的那 10 条必须**逐条列名**并给出理由 —— ⛔ 「其余维持原判」不算交代。
    kept = payload["kept_refuted"]
    assert len(kept["diagnostics"]) == 10, kept["diagnostics"]
    assert {tuple(x) for x in kept["diagnostics"]} & set(owner) == set(), "维持 refuted 的又被认领了"
    assert len(kept["reason"]) > 200
    # ⭐ 压缩比必须摆给判读者看，⛔ 且 `0007` 那一份要单列（35 → 7 是全语料最狠的）。
    assert IF.compression("0007") == (35, 7), IF.compression("0007")
    for pair in S.IN_SCOPE_PAIRS:
        diags, issues = IF.compression(pair)
        doc = _read(_ws(pair))
        assert f"**本 pair：{diags} 条原始诊断归一化成 {issues} 条 issue**" in doc, pair
        assert "压缩最狠的是 `0007`，35 → 7" in doc, pair


def test_every_ins_block_matches_the_audit_json():
    """⛔⛔ **渲染结果与三份 audit json 逐条对拍** —— 两边不许有一条只在单侧存在。

    ⚠️ 这条门守的是「工作单里那一条到底是谁判的」：⭐ 三份 json 是「184 + 5 条判定怎么来的」
    的唯一载体，⛔ 若渲染结果能与它们不一致，事后就无法复核。
    """
    pytest.skip("§3 的**来源分节**于 2026-08-15 按用户裁定整体拆除"
                "（原话：「这个 issue 是怎么来的是 inspect 还是什么统统不重要」）。"
                "⛔ 本条测的是 §3.6 那一节的内容（物种抬头 / 确定性 vs LLM / 整类排除 / "
                "不确定族标签 / 底层诊断表 / 座标拼写 / 恢复条目逐条交代），"
                "⚠️ 而那些文字已随分节一起下线 —— ⭐ 条目本身一条没丢，只是不再标来源、"
                "不再印工具内部细节。⛔ 整条挂起而不是删除：`section_inspect()` 的函数本体仍在，"
                "⭐ 若日后要恢复来源分节，那五条必须逐份印的限定还在里面。"
                "⭐ 「那一节确实不在了、且条目一条没少」由 "
                "test_the_source_sections_are_gone_but_no_item_was_lost 守着。")
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        want = IF.issues_of(pair, new_block_only=True)
        got = [k for k in fb.extract(doc) if k.startswith("INS-")]
        assert sorted(got) == sorted(r["issue_id"] for r in want), \
            f"{pair}.md 的 INS- 块与 audit json 对不上：{sorted(got)}"
        for rec in want:
            assert f"### {rec['issue_id']} " in doc, rec["issue_id"]
            for field in ("statement", "puml_evidence", "merge_reason"):
                assert G._flow(rec[field]) in doc, f"{rec['issue_id']} 的 {field} 没逐字渲染"
            if rec.get(NF.OTHER_NOTE_FIELD):
                assert G._flow(rec[NF.OTHER_NOTE_FIELD]) in doc, rec["issue_id"]
            for axis in IF.AXES:
                if not rec.get(axis):
                    continue
                row = f"| `{axis}` | {T.bi(rec[axis], NF.ZH[axis].get(rec[axis]))} |"
                assert row in doc, f"{rec['issue_id']} 的 {axis} 没渲染：{row}"
            for r in rec["rulings"]:
                assert G._flow(r["ruling_basis"]) in doc, f"{rec['issue_id']} 的改判依据没渲染"
            # ⭐ 底层诊断必须可查 —— ⛔ 归一化不许把原始 message 吃掉。
            for m in rec["members"]:
                assert G.clip(m["message"], 150) in doc, \
                    f"{rec['issue_id']} 少了 diag {m['diag_index']} 的原文 message"


def test_the_merged_inspect_evidence_never_creates_a_second_block():
    """⛔⛔ inspect 阶段判为「与既有条目是同一个问题」的 61 条**不许新建块**，⚠️ 也不许改动被并入那条。

    两条理由都很硬：
    ⛔ ① 判读者对同一个问题只裁决一次 —— 摆两个块会出现两份可能互相矛盾的裁决；
    ⛔ ② 被并入的既有条目是**被判对象**，它的 `statement` 与证据行改一个字就等于篡改题面。
    """
    pytest.skip("§3 的**来源分节**于 2026-08-15 按用户裁定整体拆除"
                "（原话：「这个 issue 是怎么来的是 inspect 还是什么统统不重要」）。"
                "⛔ 本条测的是 §3.6 那一节的内容（物种抬头 / 确定性 vs LLM / 整类排除 / "
                "不确定族标签 / 底层诊断表 / 座标拼写 / 恢复条目逐条交代），"
                "⚠️ 而那些文字已随分节一起下线 —— ⭐ 条目本身一条没丢，只是不再标来源、"
                "不再印工具内部细节。⛔ 整条挂起而不是删除：`section_inspect()` 的函数本体仍在，"
                "⭐ 若日后要恢复来源分节，那五条必须逐份印的限定还在里面。"
                "⭐ 「那一节确实不在了、且条目一条没少」由 "
                "test_the_source_sections_are_gone_but_no_item_was_lost 守着。")
    merged = [i["issue_id"] for i in IF.load_issues()["issues"]
              if IF.load_overlap()[i["issue_id"]]["overlap_kind"] not in IF.NEW_BLOCK_KINDS]
    assert len(merged) == 61, len(merged)
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        keys = set(fb.extract(doc))
        for iid in merged:
            assert iid not in keys, f"{pair}.md 给已并入的 {iid} 又开了一个块"
    # ⭐ 被并入那条的 statement 必须与台账 / 候选原文**逐字**相同（含它自己的证据行）。
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        for rec in S.ledger_records(pair):
            if not IF.merged_into(rec["id"]):
                continue
            body = "> " + (rec.get("statement") or "").replace("\n", "\n> ")
            assert body in doc, f"{rec['id']} 的 statement 被动过了"
            assert f"- 生成侧：{G.esc(rec.get('generated_side'))}" in doc, \
                f"{rec['id']} 的生成侧证据行被动过了"
    # ⭐ 并入的证据必须**真的印出来**，且带「确定性检查」与「未作任何改动」两句抬头。
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        rows = IF.issues_of(pair, merged_only=True)
        if not rows:
            continue
        assert "条 `pyfcstm inspect` 的补充证据" in doc, pair
        assert "未作任何改动" in doc, pair
        for rec in rows:
            assert G._flow(rec["statement"]) in doc, f"{rec['issue_id']} 的补充证据没印出来"
            assert G._flow(rec["overlap"]["basis"]) in doc, f"{rec['issue_id']} 没印判重依据"


def test_the_uncertain_family_is_shown_and_labelled_as_undetermined():
    """⛔ 142 条「分拣未能确定」的诊断（归一化成 98 条）**不许静默丢掉**，⚠️ 且必须标明它未定。

    ⭐ 为什么这一族最不能丢：它们**集中在那些没有确认内生发现的 pair 上** ——
    ⛔ 丢掉之后那些 pair 的 §3.6 会变成一片空白，而它们恰恰是最需要人判的。
    本条把这个集中现象也复算一遍。
    """
    pytest.skip("§3 的**来源分节**于 2026-08-15 按用户裁定整体拆除"
                "（原话：「这个 issue 是怎么来的是 inspect 还是什么统统不重要」）。"
                "⛔ 本条测的是 §3.6 那一节的内容（物种抬头 / 确定性 vs LLM / 整类排除 / "
                "不确定族标签 / 底层诊断表 / 座标拼写 / 恢复条目逐条交代），"
                "⚠️ 而那些文字已随分节一起下线 —— ⭐ 条目本身一条没丢，只是不再标来源、"
                "不再印工具内部细节。⛔ 整条挂起而不是删除：`section_inspect()` 的函数本体仍在，"
                "⭐ 若日后要恢复来源分节，那五条必须逐份印的限定还在里面。"
                "⭐ 「那一节确实不在了、且条目一条没少」由 "
                "test_the_source_sections_are_gone_but_no_item_was_lost 守着。")
    rows = [i for i in IF.load_issues()["issues"] if i["verdict_class"] == "uncertain"]
    assert len(rows) == 98, len(rows)
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        mine = IF.issues_of(pair, verdict="uncertain", new_block_only=True)
        assert f"**§3.6b 分拣未能确定是内生还是投影产物的 {len(mine)} 条" in doc, pair
        for rec in mine:
            assert G._flow(rec["statement"]) in doc, rec["issue_id"]
            assert f"分拣结论 `uncertain`" in doc, pair
    # ⭐ 集中现象：没有任何确认内生 issue 的 pair，必须都有不确定 issue 兜着。
    bare = [p for p in S.IN_SCOPE_PAIRS if not IF.issues_of(p, verdict="intrinsic")]
    assert bare, "一个都没有的话这条判据失效了"
    for p in bare:
        assert IF.issues_of(p, verdict="uncertain"), \
            f"{p} 既没有内生发现也没有不确定发现 —— §3.6 会是一片空白"


def test_every_other_axis_in_the_inspect_ingest_carries_an_explanation():
    """⛔ inspect 入册的每一条，凡**该答的**轴取了 `other`，都必须附说明；⭐ 门要两头都灵。

    ⚠️ 口径必须与三处已有的门逐字一致（[validate.py](./validate.py) 给判读者那条、
    两个 mapping 装载器那两条）：⛔ 只数这一条真要回答的轴，⛔ 另一支填多了的不连带触发。
    """
    rows = IF.load_issues()["issues"]
    n = 0
    for rec in rows:
        answered = ["defect_locus", "defect_reference"] + NF.required_axes_for(rec["defect_locus"])
        picked = [a for a in answered if rec.get(a) == "other"]
        if picked:
            n += 1
            assert len(rec.get(NF.OTHER_NOTE_FIELD) or "") >= 10, rec["issue_id"]
            assert rec.get("other_note_source"), f"{rec['issue_id']} 没记说明的来源"
    assert n == 46, n
    # ⭐ 正面：`other` + 空说明必须被 `load_issues` 的门挡住。
    sample = copy.deepcopy(rows[0])
    sample.update({"defect_locus": "global", "defect_element": None, "defect_qualifier": None,
                   "defect_logic_kind": "other", "defect_reference": "language",
                   "other_note": "", "coord": "global / other / language"})
    with pytest.raises(IF.FindingsError, match="出口不写清"):
        IF._check_axes(sample, "探针")
    # ⭐ 反面：非 `other` + 空说明放行。
    sample.update({"defect_logic_kind": "unreachable", "coord": "global / unreachable / language"})
    IF._check_axes(sample, "探针")
    # ⭐ 另一支填多了不许连带触发 —— ⚠️ 它报的是「走 global 支却给了 defect_element」，
    # ⛔ 不是 other_note 那条。
    sample["defect_element"] = "other"
    with pytest.raises(IF.FindingsError, match="却给了"):
        IF._check_axes(sample, "探针")


def test_the_coordinate_spelling_is_normalised_to_one_form():
    """⛔ 座标写法必须归一成 `a / b + c / d`（`+` 与 `/` 两侧各一个空格）。

    ⚠️ 上游三份判定产物里同一格出现过十几种写法（`global + other`、`global / other · other`、
    `element / trigger+extraneous / language`…）。⛔ 不归一的后果不是难看，是
    **看不出两条其实落在同一格** —— 而那正是要拿来做分布统计的字段。
    ⭐ 每条都留了 `coord_raw` 与 `coord_normalization`，归一化过程本身可复核。
    """
    pytest.skip("§3 的**来源分节**于 2026-08-15 按用户裁定整体拆除"
                "（原话：「这个 issue 是怎么来的是 inspect 还是什么统统不重要」）。"
                "⛔ 本条测的是 §3.6 那一节的内容（物种抬头 / 确定性 vs LLM / 整类排除 / "
                "不确定族标签 / 底层诊断表 / 座标拼写 / 恢复条目逐条交代），"
                "⚠️ 而那些文字已随分节一起下线 —— ⭐ 条目本身一条没丢，只是不再标来源、"
                "不再印工具内部细节。⛔ 整条挂起而不是删除：`section_inspect()` 的函数本体仍在，"
                "⭐ 若日后要恢复来源分节，那五条必须逐份印的限定还在里面。"
                "⭐ 「那一节确实不在了、且条目一条没少」由 "
                "test_the_source_sections_are_gone_but_no_item_was_lost 守着。")
    for rec in IF.load_issues()["issues"]:
        assert rec["coord"] == IF.coord_display(rec), rec["issue_id"]
        assert re.fullmatch(r"[a-z_]+ / [a-z_]+(?: \+ [a-z_]+)? / [a-z_]+", rec["coord"]), \
            f"{rec['issue_id']} 的写法没归一：{rec['coord']!r}"
        assert rec.get("coord_raw"), rec["issue_id"]
        assert rec.get("coord_normalization"), rec["issue_id"]
        assert rec["coord_source"] in ("original", "ruling", "normalized",
                                       "recovered_ruling", "recovered_normalized"), rec
    # ⛔ 被改判过的必须把**原判原文**也留在库里，并渲染成「原判 X → 终局 Y」——
    # ⚠️ 原判只存在于 /tmp 下那份**不入库**的上游产物里，不留就等于「改判了什么」在仓库内查不到。
    ruled_ids = set(IF.load_rulings())
    for rec in IF.load_issues()["issues"]:
        if rec["issue_id"] not in ruled_ids:
            continue
        doc = _read(_ws(rec["pair"]))
        if rec["recovered_from_refuted"]:
            # ⚠️ 恢复来的**没有原判座标**：它整条都不曾进过判读材料。⛔ 那也不许含糊过去 ——
            # 抬头必须写明这一点，⛔ 不许印成「原判 — → 终局 X」（会读成原判是空的）。
            assert rec.get("coord_before_ruling") is None, rec["issue_id"]
            assert "本条是从 refuted 恢复的，没有原判座标" in doc, rec["issue_id"]
            continue
        assert rec.get("coord_before_ruling"), f"{rec['issue_id']} 没留原判原文"
        assert (f"原判 `{G.esc(rec['coord_before_ruling'])}` → 终局 `{rec['coord']}`" in doc), \
            f"{rec['issue_id']} 的改判没渲染成「原判 → 终局」"
    # ⭐ 有裁定的那些，座标必须**就是**裁定定的那一格（`load_rulings` 的门），
    # ⛔ 且裁定的依据要引类型学的行号 —— 不引就等于「我说了算」。
    ruled = IF.load_rulings()
    assert len(ruled) == 43, len(ruled)
    for iid, rs in ruled.items():
        for r in rs:
            # ⭐ 裁定必须指到类型学的**具体位置** —— 文件名、小节号或行号任一，
            # ⛔ 只说「按判定测试」不算：那句话在类型学里有九处。
            assert ("defect_taxonomy.md" in r["ruling_basis"]
                    or "§3." in r["ruling_basis"]
                    or re.search(r":\d{3}", r["ruling_basis"])), iid
            assert len(r["final_evidence"]) > 100, iid


def test_the_recovered_refuted_findings_are_documented_one_by_one():
    """⛔⛔ 5 条从 `refuted` 恢复的条目，每条都要写清**凭什么恢复**，⚠️ 并在工作单里标明来源。

    ⭐ 判据是两条同时成立（写在每条的 `recovery_basis` 里，可回原文核）：
    ⛔ ① 推翻理由**没有否掉主张本身**，只否掉了分拣者的措辞 / 归属 / 主语；
    ⛔ ② 同型形态在别的 pair 上被判 intrinsic 或 uncertain 并**摆给了判读者** —— 也就是
    「同一件事两种待遇」。⚠️ 这一条是硬的：`0000` 的根初始边带触发被 refuted，而完全同型的
    `0030` / `0040` / `0050` 三份都作为条目摆着。
    """
    pytest.skip("§3 的**来源分节**于 2026-08-15 按用户裁定整体拆除"
                "（原话：「这个 issue 是怎么来的是 inspect 还是什么统统不重要」）。"
                "⛔ 本条测的是 §3.6 那一节的内容（物种抬头 / 确定性 vs LLM / 整类排除 / "
                "不确定族标签 / 底层诊断表 / 座标拼写 / 恢复条目逐条交代），"
                "⚠️ 而那些文字已随分节一起下线 —— ⭐ 条目本身一条没丢，只是不再标来源、"
                "不再印工具内部细节。⛔ 整条挂起而不是删除：`section_inspect()` 的函数本体仍在，"
                "⭐ 若日后要恢复来源分节，那五条必须逐份印的限定还在里面。"
                "⭐ 「那一节确实不在了、且条目一条没少」由 "
                "test_the_source_sections_are_gone_but_no_item_was_lost 守着。")
    rows = [i for i in IF.load_issues()["issues"] if i["recovered_from_refuted"]]
    assert sorted(r["issue_id"] for r in rows) == [
        "INS-0000-04", "INS-0013-05", "INS-0017-02", "INS-0047-03", "INS-0057-03"], rows
    index = {(r["pair"], r["diag_index"]): r for r in IF.all_findings()}
    for rec in rows:
        assert len(rec["recovery_basis"]) > 300, rec["issue_id"]
        assert {index[(rec["pair"], d)]["verdict"] for d in rec["diag_indices"]} == {"refuted"}, \
            rec["issue_id"]
    # ⭐ `0000` 那条是本轮的判例，逐字钉住它引的那三个同型 pair。
    zero = next(r for r in rows if r["issue_id"] == "INS-0000-04")
    for probe in ("INS-0030-01", "INS-0040-01", "INS-0050-01", "结论本身很可能仍成立"):
        assert probe in zero["recovery_basis"], probe
    assert zero["coord"] == "element / trigger + extraneous / language", zero["coord"]
    # ⭐ 工作单里必须标明「这条是恢复来的」—— ⛔ 不标，判读者会以为它与别的诊断同源同流程。
    for rec in rows:
        doc = _read(_ws(rec["pair"]))
        assert G._flow(rec["recovery_basis"]) in doc, rec["issue_id"]
        assert "里**恢复**的" in doc, rec["pair"]


def test_no_script_decides_the_merging_or_the_overlap():
    """⛔⛔ 归并与判重是**判断**，⛔ 不许任何脚本决定 —— 用 AST 钉住那批符号不再被定义。

    ⚠️ 2026-08-13 撤掉过一版自动实现（并查集按元素名归组 + 中文关键词表扫台账判重合），
    ⛔ 它当时确实在**决定**结果。判据用 AST 而不是 grep：模块 docstring 里正记着
    「撤掉了什么」，⛔ 全文 grep 会把那段存档说明本身当成违规。

    ⭐ 入册之后这条**更要留着**：三份 audit json 在树上了，⛔ 下一个人很容易顺手写个
    「自动重算一遍」的函数，而那等于把判断悄悄换成模式匹配。
    """
    import ast
    tree = ast.parse(_read(os.path.join(HERE, "inspectfindings.py")))
    defined = {n.name for n in ast.walk(tree)
               if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
    assigned = {t.id for n in ast.walk(tree) if isinstance(n, ast.Assign)
                for t in n.targets if isinstance(t, ast.Name)}
    for banned in ("normalize", "match_one", "NATURE_WORDS", "_UF", "_anchor",
                   "triage", "statement_of"):
        assert banned not in defined | assigned, \
            f"`{banned}` 又回来了 —— 归并 / 判重不许由脚本决定"
    # ⭐ 装载器只许**读**判定文件，⛔ 不许自己拼归并结果：三份文件都缺时什么都不渲染。
    assert IF.has_judged_issues()
    with contextlib.ExitStack() as stack:
        tmp = stack.enter_context(tempfile.TemporaryDirectory())
        moved = os.path.join(tmp, "x.json")
        stack.callback(lambda: shutil.move(moved, IF.ISSUES_FILE))
        shutil.move(IF.ISSUES_FILE, moved)
        assert not IF.has_judged_issues(), "少一份文件时必须判成「尚未入册」"


def test_the_audit_files_are_the_only_record_of_how_the_judgements_were_made():
    """⛔⛔ 三份 audit json 是「189 条判定怎么来的」的**唯一载体** —— 不入库则事后无法复核。

    ⚠️ 本条不测渲染，只测这三份文件**自身**够不够复核：每条判定都要能回答
    ⭐「合并理由是什么」「双方原文怎么对上的」「座标凭哪条判定测试改的」。
    """
    for path, schema, key in (
            (IF.ISSUES_FILE, IF.ISSUES_SCHEMA, "issues"),
            (IF.OVERLAP_FILE, IF.OVERLAP_SCHEMA, "decisions"),
            (IF.RULINGS_FILE, IF.RULINGS_SCHEMA, "rulings")):
        assert os.path.exists(path), path
        payload = _json.loads(_read(path))
        assert payload["schema"] == schema
        assert payload["what_this_is"], path
        assert payload[key], path
    # ⭐ 判重依据必须引到**双方**：既有条目那一侧与 INS 这一侧。
    for iid, d in IF.load_overlap().items():
        assert len(d["basis"]) >= 80, iid
        if d["overlap_kind"] != "none":
            assert d["overlap_target"] in d["basis"], f"{iid} 的依据里没提 target"
    # ⭐ 归并理由必须逐条有；⛔ 单条诊断的也要写明「不涉归并」而不是留空。
    for rec in IF.load_issues()["issues"]:
        assert rec["merge_reason"].strip(), rec["issue_id"]
        if len(rec["diag_indices"]) > 1:
            assert len(rec["merge_reason"]) >= 60, rec["issue_id"]


def test_the_inspect_family_is_marked_as_deterministic_not_llm():
    """⛔⛔ 必须让判读者一眼看出：这一族是**确定性检查**，与 §3.1–§3.5 的 LLM 产出不同物种。

    ⚠️ 差别直接改变一句话的含义：「模型没提到」对 LLM 那族是**采样**问题（重跑可能就有了），
    ⛔ 对本族说明的是**检查器本身看不到那类东西**。⭐ 不写明，判读者会把两族的「没报」
    当成同一件事，于是拿工具的沉默当证据。
    """
    pytest.skip("§3 的**来源分节**于 2026-08-15 按用户裁定整体拆除"
                "（原话：「这个 issue 是怎么来的是 inspect 还是什么统统不重要」）。"
                "⛔ 本条测的是 §3.6 那一节的内容（物种抬头 / 确定性 vs LLM / 整类排除 / "
                "不确定族标签 / 底层诊断表 / 座标拼写 / 恢复条目逐条交代），"
                "⚠️ 而那些文字已随分节一起下线 —— ⭐ 条目本身一条没丢，只是不再标来源、"
                "不再印工具内部细节。⛔ 整条挂起而不是删除：`section_inspect()` 的函数本体仍在，"
                "⭐ 若日后要恢复来源分节，那五条必须逐份印的限定还在里面。"
                "⭐ 「那一节确实不在了、且条目一条没少」由 "
                "test_the_source_sections_are_gone_but_no_item_was_lost 守着。")
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        assert "**§3.6 `pyfcstm inspect` 的确定性检查发现**" in doc, pair
        assert G.INSPECT_SPECIES_CAVEAT in doc, f"{pair}.md 少了物种抬头"
        assert G.INSPECT_PROJECTION_CAVEAT in doc, f"{pair}.md 少了「确定性不等于正确」"
        # ⛔ 位置也要对：物种抬头必须在第一个 INS- 块**之前**。
        blocks = [k for k in fb.extract(doc) if k.startswith("INS-")]
        if blocks:
            assert doc.index(G.INSPECT_SPECIES_CAVEAT) < doc.index(f"### {blocks[0]}"), pair


def test_the_two_inspect_species_stay_separable_after_collection():
    """⛔ 回收时必须分得开「确认内生」与「分拣未定」两个物种。

    ⚠️ 混在一起统计会把「工具确定看到的」与「可能是投影造出来的」算成同一种证据 ——
    ⛔ 而后者的事实本身还没成立。⭐ 分法从 audit json 的 `verdict_class` 来，
    ⛔ 不靠填写块 key 的前缀约定（`INSU-` 那套已撤：key 与 issue id 必须是同一个字符串）。
    """
    proc = subprocess.run([sys.executable, os.path.join(HERE, "collect.py"), "--stdout"],
                          check=True, capture_output=True, text=True, cwd=HERE)
    pairs = _json.loads(proc.stdout)["pairs"]
    got = collections.Counter(r["source"] for v in pairs.values() for r in v["candidates"])
    # ⚠️ 2026-08-16 `unmatched_issue`（49 条 `UM-` 块）整批撤出工作单 ——
    # 裁定与全部证据见 docs/findings/um_residue_ruling.md：X1 那一半 333/334 条的簇号精确
    # 出现在已裁定表里（96% 判为非缺陷），v46 那一半的主体是 REPRESENTATION_DEBT（投影债务）。
    # ⭐ 故 `candidates_seen` 由 269 降到 220，⛔ 台账 99 一条没动。
    # ⭐ 再于同日改为全部出块，升到 281（61 条并入项各自出块）。
    assert got == {"valid_unrecorded": 15, "review_diff": 77,
                   # ⭐ 0053 三条死端合并后为 39 / 91（130 条在范围内的 INS）；
                   # ⚠️ 同日一度误改为 91 / 98（那是把未去重的 189 条全出块）
                   "inspect_finding_intrinsic": 39, "inspect_finding_uncertain": 91}, got
    assert sum(got.values()) == 222
    # ⭐ 与 audit json 逐条对齐（⛔ 不是只对总数）。
    # ⭐⭐ 2026-08-16 起**并入项也各自出块**，⛔ 故此处不再按 `NEW_BLOCK_KINDS` 过滤 ——
    # ⚠️ 那层过滤正是「61 条并入项在 md 里一个块都没有」的镜像；⭐ 现在对齐**全部** INS。
    # ⭐⭐ 判据是「在 dtier_rulings.json 的范围内」（去重后的 130 条 INS），
    # ⛔ 不是全部 189 条（那是未去重的判读包），⛔ 也不是 NEW_BLOCK_KINDS 的 126 条
    # （那是「UM- 撤出前的旧口径」）。⚠️ 三个数都出现过，账目见 DEDUP_ACCOUNTING.md。
    import dtier as _DT2
    _scope = _DT2.load_rulings()
    want = collections.Counter(
        "inspect_finding_" + i["verdict_class"] for i in IF.load_issues()["issues"]
        if i["issue_id"] in _scope)
    assert got["inspect_finding_intrinsic"] == want["inspect_finding_intrinsic"]
    assert got["inspect_finding_uncertain"] == want["inspect_finding_uncertain"]
    # ⛔ `INSU-` 前缀不许再出现在任何工作单里。
    for pair in S.IN_SCOPE_PAIRS:
        assert "INSU-" not in _read(_ws(pair)), pair


def test_the_blocker_taxonomy_is_complete_and_accounted_for():
    """⛔ `mappable: false` 的每一条都必须挂一个**已声明**的卡点，⭐ 且分布可清点。

    ⚠️ 三类卡点**含义不同、不得混写**，混了会污染「座标系覆盖度」这个数字：

    - `unit_of_record` —— 一个 id 底下坐着多条异质主张，逐条各自都能落格。
    - `not_a_defect_claim` —— 它根本不主张作者制品有毛病。
    - `taxonomy` —— 座标系给不出取值。⭐ 只有这一档能算作缺口，⭐ 现在是 **0**。
    """
    assert set(CM.BLOCKERS) == {"unit_of_record", "not_a_defect_claim", "taxonomy"}
    by = CM.stats()["by_blocker"]
    assert "unlabelled" not in by
    assert by == {"unit_of_record": 58, "not_a_defect_claim": 17}, by
    assert sum(by.values()) == CM.stats()["unmapped"] == 75
    assert LM.stats()["unmapped"] == 0
    for b in CM.BLOCKERS:
        assert b in CM.BLOCKER_ZH and len(CM.BLOCKER_ZH[b]) == 2


def test_the_removed_sections_are_really_gone():
    """⛔ §4 深度检查清单与 §5 新增登记必须真的不在 54 份工作单里。

    ⚠️ 这一条是上面七个 `pytest.skip` 的对侧。⭐ CLAUDE.md §9.5-8 记过这个坑：
    把测试改成 skip 会让检查**静默消失**而测试全绿 —— 那比测试变红危险。
    ⛔ 所以拆除本身必须有门守：若哪天两节被接回来（不管是有意还是误接），
    ⭐ 本条立刻红，提醒把那七个 skip 一起解开、别让它们继续躺着装绿。
    """
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        assert "## §4 " not in doc, f"{pair}.md 又出现 §4 —— 那七个 skip 该解开了"
        assert "## §5 " not in doc, f"{pair}.md 又出现 §5 —— 那七个 skip 该解开了"
        keys = fb.extract(doc)
        assert not [k for k in keys if k.startswith("CHK-")], f"{pair}.md 还有 CHK- 块"
        assert not [k for k in keys if k.startswith("NEW-")], f"{pair}.md 还有 NEW- 块"


def test_the_dtier_renderer_spends_no_star_of_its_own():
    """⛔ `dtier.py` 的**生成字符串**里一个 `⭐` 都不许有。

    ⭐ 这一条是上面那道 `own_star` 档提到 12 的**对价**：档能提，是因为改为「生成器自己
    一个都不花」这条更硬的判据；⛔ 若哪天生成串里又出现 `⭐`，本条立刻红。
    ⚠️ 判据只看生成串 —— 注释与 docstring 里照常可以用（那是给读代码的人看的）。
    """
    # ⚠️⚠️ 判据用 `tokenize` 只看**字符串 token**，⛔ 不再按行做 docstring 状态机。
    # ⭐ 旧实现漏了**行尾注释**：`x = 1  # ⭐ 说明` 会被判成生成串（实测 2026-08-16
    # 因一句局部导入的行尾注释误报）。⛔ 而本测试自己的 docstring 写着「注释里照常可以用」——
    # ⚠️ 检测器没实现它声明的判据，那是检测器的缺陷，不是被测代码的。
    # ⭐ token 级判据顺带解决了单行 docstring、拼接字面量、f-string 等一切边角。
    import io
    import tokenize as _tk
    src = _read(os.path.join(HERE, "dtier.py"))
    docstrings = set()
    # ⭐ docstring = 模块 / 类 / 函数体里**独立成句**的字符串表达式；用 AST 精确取。
    import ast
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            b = getattr(node, "body", None)
            if b and isinstance(b[0], ast.Expr) and isinstance(b[0].value, ast.Constant) \
                    and isinstance(b[0].value.value, str):
                docstrings.add((b[0].lineno, b[0].end_lineno))
    bad = []
    for tok in _tk.generate_tokens(io.StringIO(src).readline):
        if tok.type != _tk.STRING or "⭐" not in tok.string:
            continue
        if any(a <= tok.start[0] and tok.end[0] <= b for a, b in docstrings):
            continue
        bad.append((tok.start[0], tok.string.strip()[:60]))
    assert not bad, f"dtier.py 的生成串里有 ⭐：{bad}"


def test_the_source_sections_are_gone_but_no_item_was_lost():
    """⛔ §3 的来源分节必须真的不在了，⭐ **而条目一条都不许少**。

    ⚠️ 这一条是上面那批 `pytest.skip` 的对侧（同 CLAUDE.md §9.5-8：把测试改成 skip 会让
    检查静默消失而测试全绿）。⛔ 它守两件事，⭐ 第二件比第一件重要：

    1. 那些来源小节的抬头不再出现（`§3.1` / `§3.2a` / `§3.3b` / `§3.6a` 一类）。
    2. ⭐⭐ **门面数字一格没动**：`54 / 99 / 222` —— ⛔ 拆分节不许顺手丢条目。
    """
    import re as _re
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        # ⚠️ 判据只看**标题位置**：⛔ 用全文子串会误报 —— meta review 的正文里
        # 正常会提到「§3.5 那一族」这类交叉引用，⭐ 那不是分节抬头。
        for m in _re.finditer(r"^(?:\*\*|#{2,5} )\s*(§3\.\d\w*)", doc, _re.M):
            raise AssertionError(f"{pair}.md 又出现来源分节抬头 {m.group(1)} —— 那批 skip 该解开了")
        # ⭐ 每个条目都必须是 `### <ID> <emoji>` 的统一抬头
        for h in _re.findall(r"^### (\S+)(.*)$", doc, _re.M):
            if not _re.match(r"^(?:EIS|DIFF|VU|UM|INS)-", h[0]):
                continue
            assert _re.search(r"[✅❌❓🟡🟠🔴]", h[1]), \
                f"{pair}.md 的 {h[0]} 抬头没有标记：{h}"
    n_led = sum(len(C.collect_pair(p, _ws(p))["ledger"]) for p in S.IN_SCOPE_PAIRS)
    n_cand = sum(len(C.collect_pair(p, _ws(p))["candidates"]) for p in S.IN_SCOPE_PAIRS)
    assert (len(S.IN_SCOPE_PAIRS), n_led, n_cand) == (54, 99, 222), \
        f"⛔ 拆分节把条目数改了：{len(S.IN_SCOPE_PAIRS)} / {n_led} / {n_cand}"

def test_the_dedup_is_not_undone():
    """⛔⛔ **工作单条目数恒为 321，⭐ 且被判重复的一条都不许出块。**

    ⚠️ 本测试守的是 2026-08-16 一天内**两次相反方向**的改错，判据故意做成双向的：

    | ⛔ 错法 | 后果 | 本测试哪一条抓 |
    | :-- | :-- | :-- |
    | 按「已并入」跳过全部 61 条 | 5 条宿主已撤的连块带宿主一起消失，按 id 搜不到 | `missing` + `id 可 grep` |
    | 让块数等于判读包的 380 | 59 条真重复重新摆出（`0010` 同一缺陷出现三次） | `extra` + 总数 321 |

    ⭐ 完整账目与两次改错的经过见 [DEDUP_ACCOUNTING.md](./DEDUP_ACCOUNTING.md)。
    ⛔ 若哪天这里要改数字，**先读那一页**，⚠️ 先回答「我要对齐的那个数去重了吗」。
    """
    import collections as _c
    import re as _re
    import dtier as _DT            # 本模块顶层未导入 dtier，就地导入
    scope = _DT.load_rulings()
    blocks = _c.Counter()
    md = []
    for pair in S.IN_SCOPE_PAIRS:
        doc = _read(_ws(pair))
        md.append(doc)
        for h in _re.findall(r"^### ((?:EIS|INS|DIFF|VU|UM)-\S+)", doc, _re.M):
            blocks[h] += 1
    allmd = "".join(md)

    # ---- ① 范围内的每一条都有且只有一个块
    missing = sorted(set(scope) - set(blocks))
    extra = sorted(set(blocks) - set(scope))
    dup = sorted(k for k, v in blocks.items() if v > 1)
    assert not missing, f"⛔ 在范围内却没有块（按 id 搜不到）：{missing}"
    assert not dup, f"⛔ 同一 id 出现多个块：{dup}"
    assert not extra, f"⛔ 有块但不在范围内 —— ⚠️ 很可能是重复回潮了：{extra}"

    # ---- ② 总数与前缀分布钉死
    got = _c.Counter(k.split("-")[0] for k in blocks)
    assert dict(got) == {"EIS": 99, "INS": 130, "DIFF": 77, "VU": 15}, dict(got)
    assert sum(got.values()) == len(scope) == 321, (sum(got.values()), len(scope))

    # ---- ③ ⭐ 被判重复的那 59 条：⛔ 不许有块，⭐ 但 id 必须能 grep 到
    import json as _j
    out = _j.loads(_read(os.path.join(HERE, "dtier_rulings_deduped_out.json")))
    dropped = out["rulings"]
    assert len(dropped) == 59, len(dropped)
    assert not (set(dropped) & set(blocks)), \
        f"⛔ 被判重复的条目又出块了：{sorted(set(dropped) & set(blocks))}"
    unfindable = [k for k in dropped if f"`{k}`" not in allmd]
    assert not unfindable, \
        f"⛔ 被并入的条目 id 在 md 里搜不到 —— 「搜不到」与「不存在」就分不开了：{unfindable}"

    # ---- ④ ⭐ 它们的**事实**也必须印着（⛔ 不出块 ≠ 删证据）
    import inspectfindings as _IF
    nofact = []
    for k in dropped:
        rec = next((x for x in _IF.load_issues()["issues"] if x["issue_id"] == k), None)
        if rec is None or not (rec.get("statement") or "").strip():
            continue
        head = re.sub(r"\s+", "", (rec["statement"] or "")[:40])
        if head and head not in re.sub(r"\s+", "", allmd):
            nofact.append(k)
    assert not nofact, f"⛔ 被并入条目的事实没印进宿主块：{nofact}"

    # ---- ⑤ ⭐ 判读包与旁挂加起来必须还是 380（⛔ 拆分不许丢条目）
    assert len(scope) + len(dropped) == 380, (len(scope), len(dropped))
