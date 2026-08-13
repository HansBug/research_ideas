"""重标材料的**只读**数据源装载层。

⛔ 本模块只读。它**从不写** `expected_issue_set.json`，也从不写任何既有台账、
verdict 或 run record。人工重标的产物全部落在 `relabel/` 目录内。

数据源清单（全部为仓库内既有文件）：

| 用途 | 路径 |
| :-- | :-- |
| NL 规约 | `selected_seed_examples/llms_emp_feedback_final_<pair>/nl.txt` |
| 作者源模型 | `selected_seed_examples/llms_emp_feedback_final_<pair>/stm0.puml` |
| NL 人工分段标注 | `corpora/nl_segmentation/overrides.json` |
| 参考模型 | `corpora/seed_library/llms-emp-stm-subset/assets/raw/drive_download/Experiment Results.xlsx` 的 `STM Results!D<row>` |
| 现有台账 | `discover_matrix/manual_review/expected_issue_set.json` |
| 审阅 agent 原始 diff | `discover_matrix/manual_review/<pair>-review.json` |
| X1 臂多报裁定 | `baseline_arm/results/unexpected_verdicts/X1-J*.jsonl` |
| 主臂 v46 多报裁定 | `discover_matrix/v46/unexpected_verdicts/G*.jsonl` |
"""

from __future__ import annotations

import functools
import glob
import hashlib
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
MANUAL_REVIEW = os.path.dirname(HERE)
DISCOVER_MATRIX = os.path.dirname(MANUAL_REVIEW)
PAPER = os.path.dirname(DISCOVER_MATRIX)

SEEDS = os.path.join(PAPER, "selected_seed_examples")
CORPORA = os.path.join(PAPER, "corpora")
BASELINE_ARM = os.path.join(PAPER, "baseline_arm")
V46 = os.path.join(DISCOVER_MATRIX, "v46")

XLSX = os.path.join(
    CORPORA, "seed_library", "llms-emp-stm-subset", "assets", "raw",
    "drive_download", "Experiment Results.xlsx",
)

# ⛔ 建模对象边界（CLAUDE.md）：M = (S, E, V, Tr, A)，无时钟、无不变式、无正交区。
# 由这条边界导出的永久排除：`00x8` 六个 pair 的 NL 要求 fork/join 与秒级时间约束。
OUT_OF_SCOPE_PAIRS = ("0008", "0018", "0028", "0038", "0048", "0058")
ALL_PAIRS = tuple(f"{i:04d}" for i in range(60))
IN_SCOPE_PAIRS = tuple(p for p in ALL_PAIRS if p not in OUT_OF_SCOPE_PAIRS)

# 19 谓词封闭词表（predicate_coverage/BRIEF.md）
PREDICATES = {
    "S": ["state_declared", "variable_declared", "event_declared", "containment",
          "initial_target", "edge_declared", "effect_declared", "action_declared",
          "guard_distinguishable", "cardinality"],
    "B": ["occupancy_after", "event_consumed", "stays_in", "variable_delta_after",
          "reaches", "terminates"],
    "P": ["invariant", "response_within", "persists_until"],
}
ALL_PREDICATES = [p for v in PREDICATES.values() for p in v]

LAYERS = ["wellformedness", "nl_named", "over_specification", "nl_contradiction"]
ELEMENTS_OF_M = ["S", "E", "V", "Tr", "A"]


def _read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def seed_dir(pair):
    return os.path.join(SEEDS, f"llms_emp_feedback_final_{pair}")


def nl_text(pair):
    return _read(os.path.join(seed_dir(pair), "nl.txt"))


def puml_text(pair):
    return _read(os.path.join(seed_dir(pair), "stm0.puml"))


def source_meta(pair):
    return json.loads(_read(os.path.join(seed_dir(pair), "source_meta.json")))


# ---------------------------------------------------------------- 目录布局

WORKSHEET_HOWTO = "HOWTO.md"
NL_DOC = "NL.md"


def nl_sha8(pair):
    """该 pair 的 NL 全文 sha256 前 8 位。⭐ 与译文 JSON 的 `sha8` 字段同口径。"""
    return hashlib.sha256(nl_text(pair).encode("utf-8")).hexdigest()[:8]


@functools.lru_cache(maxsize=1)
def _nl_dir_index():
    """`{sha8: 目录名}`，目录名取该组**最小的 pair id**（如 `nl_0002`）。

    ⛔⛔ **分组判据是 NL 全文的 sha8，⛔ 不是 pair id 的末位数字。** 两者在 8 组上恰好
    一致，⛔ 但在第 9、第 10 组上**不一致** —— 实测（`nl_text` 的 sha8 直接可复核）：

    - `0002` 的 NL 与 `0013` `0023` `0033` `0043` `0053` 相同（sha8 `a391765d`）；
    - `0003` 的 NL 与 `0012` `0022` `0032` `0042` `0052` 相同（sha8 `9fe426ba`）。

    ⭐ 即 `0002` / `0003` 与 `0012` / `0013` 是**交叉**的。⛔ 若按末位数字分目录，
    `nl_0002/` 里就会同时坐着两份**不同**的 NL，而该目录的 `NL.md` 只能对其中一份为真 ——
    ⛔ 那正好复刻了 [README.md](./README.md) §十记过的那起事故（一份材料被印到不属于它的
    工作单上，且旁边还立着一句免责声明劝读者不要去核）。
    ⛔ 所以这里**永远**按 sha8 分，⛔ 不许「化简」成末位数字。
    """
    groups = {}
    for pair in IN_SCOPE_PAIRS:
        groups.setdefault(nl_sha8(pair), []).append(pair)
    return {sha: f"nl_{min(ps)}" for sha, ps in groups.items()}


def nl_dir(pair):
    """该 pair 的工作单所在子目录名（相对 `relabel/`）。"""
    return _nl_dir_index()[nl_sha8(pair)]


def nl_dirs():
    """全部 9 个 NL 子目录名，按名字升序。"""
    return sorted(set(_nl_dir_index().values()))


@functools.lru_cache(maxsize=1)
def _pairs_by_dir():
    out = {}
    for pair in IN_SCOPE_PAIRS:
        out.setdefault(nl_dir(pair), []).append(pair)
    return {d: tuple(sorted(ps)) for d, ps in out.items()}


def pairs_of_dir(dirname):
    """该子目录下的 6 个 pair。"""
    return _pairs_by_dir()[dirname]


def nl_siblings(pair):
    """与该 pair **共用同一份 NL** 的 6 个 pair（含自己）。"""
    return _pairs_by_dir()[nl_dir(pair)]


def worksheet_path(base, pair):
    """工作单路径 `<base>/nl_XXXX/<pair>.md`。"""
    return os.path.join(base, nl_dir(pair), f"{pair}.md")


def nl_doc_path(base, pair):
    """该 pair 所属 NL 组的 NL 材料页 `<base>/nl_XXXX/NL.md`。"""
    return os.path.join(base, nl_dir(pair), NL_DOC)


def howto_path(base):
    """填写说明页 `<base>/HOWTO.md` —— 54 份工作单共用一份。"""
    return os.path.join(base, WORKSHEET_HOWTO)


def find_worksheets(base):
    """列出 `<base>` 下**任意深度**的 `<4 位数字>.md`，返回 `{pair: 路径}`。

    ⭐ 递归是必须的：工作单已经按 NL 组下沉了一层，⛔ 而 `00x8` 的越界检查要能抓住
    「有人把工作单放在任何地方」这件事 —— ⛔ 只扫根目录会漏掉子目录里的越界工作单。
    """
    out = {}
    for root, _dirs, files in os.walk(base):
        for f in files:
            if re.fullmatch(r"\d{4}\.md", f):
                out.setdefault(f[:-3], os.path.join(root, f))
    return out


# ---------------------------------------------------------------- NL 分段

@functools.lru_cache(maxsize=1)
def _nl_overrides():
    path = os.path.join(CORPORA, "nl_segmentation", "overrides.json")
    return json.loads(_read(path))["overrides"]


def nl_segments(pair):
    """按 pipeline 的同一口径分段：有人工标注用标注，否则按物理行切。

    返回 [(seg_id, text)]。⭐ 与 `common/nl_segmentation.py` 的策略一致，故台账里
    「NL 第 N 句」的编号可以直接对上。
    """
    text = nl_text(pair)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    ov = _nl_overrides().get(digest[:12])
    if ov and ov.get("nl_sha256") == digest:
        return [(k, v) for k, v in sorted(ov["segments"].items())], "manual_override"
    out = []
    n = 0
    for line in text.splitlines():
        if not line.strip():
            continue
        n += 1
        out.append((f"NL-L{n:03d}", line))
    return out, "line_split"


@functools.lru_cache(maxsize=1)
def _nl_group_by_digest():
    """NL 全文 digest → 组名（`NL01` … `NL10`）。

    ⭐ 真源是 `<pair>-review.json` 的 `group` 字段 —— 台账只覆盖 48 个 pair，
    其中 `NL02` 组（`0001` `0011` `0021` `0031` `0041` `0051`）**台账 0 条**，
    只查台账会漏掉这一组。
    """
    out = {}
    for pair in ALL_PAIRS:
        rv = review_json(pair)
        g = (rv or {}).get("group") or (rv or {}).get("nl_group")
        if not g:
            continue
        out.setdefault(hashlib.sha256(nl_text(pair).encode("utf-8")).hexdigest()[:12], g)
    return out


def nl_group(pair):
    """该 pair 所属的 NL 组名。⭐ 同组 6 个 pair 共用同一份 NL 规约。"""
    digest = hashlib.sha256(nl_text(pair).encode("utf-8")).hexdigest()[:12]
    return _nl_group_by_digest().get(digest)


# ---------------------------------------------------------------- 参考模型

@functools.lru_cache(maxsize=1)
def _reference_column():
    """从作者 workbook 的 `STM Results!D` 列读参考 PlantUML。

    ⚠️ 参考模型**不在** `selected_seed_examples/` 里 —— 那里只有 NL 与被测的生成
    制品。它只存在于原始 workbook 的 D 列，故这里直读 xlsx。读不到时返回空字典，
    生成的工作单会显式写「参考模型不可用」而不是静默省略。
    """
    try:
        import openpyxl
    except ImportError:
        return {}
    if not os.path.exists(XLSX):
        return {}
    wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
    ws = wb["STM Results"]
    out = {}
    for row in range(2, 200):
        v = ws.cell(row=row, column=4).value
        if v:
            out[row] = str(v)
    wb.close()
    return out


def reference_puml(pair):
    meta = source_meta(pair)
    row = meta.get("source_excel_row")
    col = _reference_column()
    if not col:
        return None, "openpyxl 不可用或 workbook 缺失"
    txt = col.get(row)
    if not txt:
        return None, f"workbook STM Results!D{row} 为空"
    return txt, f"STM Results!D{row}"


# ---------------------------------------------------------------- 台账

@functools.lru_cache(maxsize=1)
def ledger():
    return json.loads(_read(os.path.join(MANUAL_REVIEW, "expected_issue_set.json")))


def ledger_records(pair=None, reportable_only=False):
    recs = ledger()["records"]
    if reportable_only:
        recs = [r for r in recs
                if r["pair"] not in OUT_OF_SCOPE_PAIRS
                and r.get("boundary_ruling") != "out_of_scope"]
    if pair is not None:
        recs = [r for r in recs if r["pair"] == pair]
    return recs


# ---------------------------------------------------------------- 风险标记

_RE_PROJECTION_STRONG = re.compile(r"fcstm|FCSTM|投影|R4\.5|R45")
_RE_PROJECTION_ARTIFACT = re.compile(
    r"UnspecifiedInitial|InvalidInitial|FinalWait|R45RouteToken|_GaStep"
)


def _narrative(rec):
    parts = [rec.get("statement") or "", rec.get("generated_side") or "",
             rec.get("reference_side") or "", rec.get("layer_basis") or ""]
    for a in rec.get("assertions") or []:
        parts += [str(a.get("expression") or ""), str(a.get("context") or ""),
                  str(a.get("rewrote_from") or "")]
    return " ".join(parts)


def risk_flags(rec):
    """自动风险标记。⛔ 这些是**提示**，不是裁决 —— 打了标记不等于该条不成立。"""
    flags = []
    if rec.get("decided_by") == "lexical":
        flags.append((
            "lexical",
            "只过正则未二读 —— `decided_by = lexical`，该条从未经过 NL 复读或有害性检验，"
            "分层依据只有词法匹配。",
        ))
    nar = _narrative(rec)
    if _RE_PROJECTION_STRONG.search(nar):
        flags.append((
            "projection_named",
            "读了投影 —— statement / 断言里直接提到 fcstm 或「投影」。"
            "投影是本仓库的 `plantuml_source_lowering.py`，它会合成作者从未写过的元素；"
            "请核对该条主张在**作者源 PlantUML** 上是否同样成立。",
        ))
    elif _RE_PROJECTION_ARTIFACT.search(nar):
        flags.append((
            "projection_artifact",
            "读了投影（间接）—— 证据里出现了投影合成的占位符名"
            "（`UnspecifiedInitial` / `InvalidInitial*` / `FinalWait*` / `R45RouteToken` / `_GaStep*`）。"
            "作者源里没有这些元素，请核对主张在作者源上如何表述。",
        ))
    if not rec.get("primary_predicate"):
        flags.append((
            "no_primary",
            "不可分层 —— 无 `primary_predicate`，该条没有可执行的主断言，"
            "命中判定只能靠人读。",
        ))
    if not (rec.get("assertions") or []):
        flags.append(("no_assertion", "无任何断言表达式。"))
    # ⚠️ 这个标记只对**按台账自己的 `layer_basis` 定义确实要求 NL 逐字依据**的两层生效。
    # ⛔ 2026-08-13 之前它写作 `layer != "wellformedness"`，于是把 `over_specification`
    # 一并标了出来 —— 而那一层的 `layer_basis` 是「生成方凭空多出，且造成可断言的负面后果」，
    # 一个字都没提 NL，既有 6 条里 5 条 `nl_evidence` 本就为空，⭐ 那是设计如此、不是漏填。
    # ⛔ 这个标记渲染在裁决块**正上方**，是判读者动笔前读到的最后一句话；与
    # [validate.py](./validate.py) 的同一道门给出相反教法，会直接把判读结论带偏
    # （[CLAUDE.md](../../../../../CLAUDE.md) §13 第 2 条）。判据的唯一真源是
    # `newfields.NL_GROUNDED_LAYERS`，⛔ 不在本文件另抄一份。
    # ⭐ 延迟导入：`newfields` 在模块级导入本文件，⛔ 顶层 import 会成环。
    import newfields as _NF
    if (not (rec.get("nl_evidence") or "").strip()
            and rec.get("layer") in _NF.NL_GROUNDED_LAYERS):
        flags.append((
            "no_nl_evidence",
            f"`layer = {rec.get('layer')}` 却无 `nl_evidence` —— 这一层的台账定义"
            f"（「{_NF.layer_basis_table().get(rec.get('layer'))}」）要求 NL 逐字依据。"
            "依据多半躺在 `statement` 正文里没抄进字段，重标时补上段 id 即可。"
            "仅 `nl_named` / `nl_contradiction` 会被标；"
            "`wellformedness` 与 `over_specification` 两层**不要求** NL 依据，"
            "它们的 `nl_evidence` 为空是设计如此，不是漏填。",
        ))
    if rec.get("boundary_ruling"):
        flags.append((
            "boundary",
            f"已有边界裁定 `{rec.get('boundary_ruling')}`："
            f"{rec.get('boundary_rationale') or '（无理由记录）'}",
        ))
    if (rec.get("replay") or {}).get("verdict") not in ("captured",):
        flags.append((
            "replay",
            f"replay 状态为 `{(rec.get('replay') or {}).get('verdict')}`"
            f"（value = {(rec.get('replay') or {}).get('value')}）—— 主断言未被复算确认。",
        ))
    if rec.get("pending_statement_rewrite"):
        flags.append(("pending_rewrite", "该条 statement 已被登记为待重写。"))
    return flags


def shallow_hint(rec):
    """「可能偏浅」的机械提示。不是裁决 —— 判读者仍要自己判这一条成不成立、够不够深。

    判据只看**断言形状**，不看内容：单个存在性谓词、单元素、无佐证断言 → 提示可能偏浅。

    ⚠️ 2026-08-13 由 `depth_hint` 更名：工作单的 `depth`（表层 / 中层 / 深层）字段
    已删除，旧名会让人以为这里在提示该往那个字段里填什么。它提示的是**台账这一条**
    可能只说到「某元素不存在」而没说到「因此运行时会怎样」。
    """
    prim = rec.get("primary_predicate")
    existence = {"state_declared", "event_declared", "variable_declared",
                 "effect_declared", "action_declared", "edge_declared", "containment"}
    n_assert = len(rec.get("assertions") or [])
    elems = set()
    for a in rec.get("assertions") or []:
        elems |= set(a.get("elements") or [])
    reasons = []
    if prim in existence:
        reasons.append(f"主谓词 `{prim}` 属存在性 / 声明类")
    if n_assert <= 1:
        reasons.append(f"断言数 {n_assert}（无佐证）")
    if len(elems) <= 1:
        reasons.append(f"点名元素 {len(elems)} 个")
    if not rec.get("has_negative_control"):
        reasons.append("无负控")
    shallow = prim in existence and n_assert <= 1
    return shallow, reasons


# ---------------------------------------------------------------- 审阅 diff

def review_json(pair):
    path = os.path.join(MANUAL_REVIEW, f"{pair}-review.json")
    if not os.path.exists(path):
        return None
    return json.loads(_read(path))


@functools.lru_cache(maxsize=1)
def _ledger_diff_index():
    used = {}
    for r in ledger()["records"]:
        u = r.get("upstream") or {}
        rf, di = u.get("review_file"), u.get("diff_index")
        if rf is None or di is None:
            continue
        used.setdefault(rf, {}).setdefault(di, []).append(r["id"])
    return used


def unadopted_diffs(pair):
    """审阅 agent 产出但**未进台账**的 diff。

    返回 [(idx, diff, 排除理由)]。「排除理由」是 diff 自己的 verdict 与相关字段 ——
    ⚠️ 当年没有单独记录「为什么不收」，只有该 diff 被判成什么。这是已知的证据缺口。
    """
    rv = review_json(pair)
    if rv is None:
        return []
    used = _ledger_diff_index().get(f"{pair}-review.json", {})
    out = []
    for i, d in enumerate(rv.get("diffs") or []):
        if i in used:
            continue
        out.append((i, d))
    return out


def adopted_diff_ids(pair):
    return _ledger_diff_index().get(f"{pair}-review.json", {})


# ---------------------------------------------------------------- 多报侧裁定

def _pair_of_cluster(cid):
    m = re.match(r"^(\d{4})", str(cid or ""))
    return m.group(1) if m else None


@functools.lru_cache(maxsize=1)
def unexpected_verdicts():
    """两臂多报侧的逐簇裁定。返回 {pair: [record]}，record 带 `_arm` / `_file`。"""
    out = {}
    specs = [
        ("X1", os.path.join(BASELINE_ARM, "results", "unexpected_verdicts", "X1-J*.jsonl")),
        ("v46", os.path.join(V46, "unexpected_verdicts", "G*.jsonl")),
    ]
    for arm, pattern in specs:
        for path in sorted(glob.glob(pattern)):
            for line in _read(path).splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                pair = _pair_of_cluster(rec.get("cluster"))
                if pair is None:
                    continue
                rec["_arm"] = arm
                rec["_file"] = os.path.basename(path)
                out.setdefault(pair, []).append(rec)
    return out


def valid_unrecorded(pair):
    return [r for r in unexpected_verdicts().get(pair, [])
            if r.get("verdict") == "VALID_UNRECORDED"]


def other_unexpected(pair):
    return [r for r in unexpected_verdicts().get(pair, [])
            if r.get("verdict") != "VALID_UNRECORDED"]


@functools.lru_cache(maxsize=1)
def ledger_accounted():
    """多报侧被判为「与台账同根、匹配器未归并」的簇。

    ⭐ 这类对重标很有用：它们说明台账那一条的**措辞或谓词选择**没能覆盖同一缺陷的
    另一种自然表述 —— 这是「偏浅」的一个具体形态。
    """
    out = {}
    for arm, path in (
        ("X1", os.path.join(BASELINE_ARM, "results", "unexpected_verdicts")),
        ("v46", os.path.join(V46, "unexpected_verdicts")),
    ):
        for f in sorted(glob.glob(os.path.join(path, "*ledger_accounted.jsonl"))):
            for line in _read(f).splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                pair = _pair_of_cluster(rec.get("cluster"))
                if pair is None:
                    continue
                rec["_arm"] = arm
                rec["_file"] = os.path.basename(f)
                out.setdefault(pair, []).append(rec)
    return out


@functools.lru_cache(maxsize=1)
def unclaimed_reclaims():
    """`X1-J*-reclaim.tsv` —— 机械未匹配（unclaimed）后被人工改判的条目。

    ⭐ 仍标 `unclaimed` 的那些，就是「两臂产出中未匹配任何台账条目」的具体清单。
    """
    out = {}
    for f in sorted(glob.glob(os.path.join(
            BASELINE_ARM, "results", "unexpected_verdicts", "*reclaim.tsv"))):
        lines = _read(f).splitlines()
        if not lines:
            continue
        head = lines[0].split("\t")
        for line in lines[1:]:
            if not line.strip():
                continue
            row = dict(zip(head, line.split("\t")))
            cell = row.get("cell", "")
            m = re.search(r"(\d{4})", cell)
            if not m:
                continue
            row["_file"] = os.path.basename(f)
            out.setdefault(m.group(1), []).append(row)
    return out


# ---------------------------------------------------------------- 未匹配 issue 清单

UNMATCHED_ISSUES_FILE = os.path.join(HERE, "unmatched_issues.json")


def unmatched_issues(pair):
    """两臂产出中机械未匹配任何台账条目的 issue（若已导出）。

    ⚠️ 这份清单来自 `unmatched_issues.json`，由 `export_unmatched.py` 从原始 run
    record 导出。原始 run record 在 `runs/`（`.gitignore` 排除），⛔ 因此该文件
    可能不存在 —— 不存在时工作单会显式写「未导出」，而不是静默为空。
    """
    if not os.path.exists(UNMATCHED_ISSUES_FILE):
        return None
    data = json.loads(_read(UNMATCHED_ISSUES_FILE))
    return data.get("by_pair", {}).get(pair, [])
