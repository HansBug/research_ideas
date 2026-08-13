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
    """风险标记的判据文本。

    ⛔ **只读工作单 §2 仍然印出来的那几项**（`statement` + 参考侧 / 生成侧）。
    2026-08-13 之前它还读 `layer_basis` 与全部断言表达式 —— 那些字段现在不再呈现，
    ⚠️ 继续读它们会让标记**无法被判读者核对**：页面上找不到触发它的那句话，
    于是提示只能被当成「系统说的」照单全收，而这恰恰是自动标记最该避免的用法。
    """
    return " ".join([rec.get("statement") or "",
                     rec.get("generated_side") or "",
                     rec.get("reference_side") or ""])


def risk_flags(rec):
    """自动风险标记。⛔ 这些是**提示**，不是裁决 —— 打了标记不等于该条不成立。

    ⛔⛔ **判据只许读工作单 §2 仍然印出来的字段。** 2026-08-13 的剥旧元数据一轮里，
    读已隐藏字段的五类标记整体删除：`lexical`（读 `decided_by`）、`no_primary`
    （读 `primary_predicate`）、`no_assertion`（读断言组）、`no_nl_evidence`
    （读 `layer` + `nl_evidence`）、以及 `replay`（读 `replay`）。

    ⚠️ 其中 `replay` 那条最要紧：它把流水线的复算结论**逐字印在裁决块正上方**
    （「主断言未被复算确认」）。判读者要独立判这一条成不成立，而这句话先一步告诉他
    流水线怎么判的 —— 那是锚定，不是提示。⛔ 剩下四类的问题同类但轻一些：
    它们援引页面上已经看不到的字段，判读者无从核对。
    """
    flags = []
    nar = _narrative(rec)
    if _RE_PROJECTION_STRONG.search(nar):
        flags.append((
            "projection_named",
            "读了投影 —— statement 或证据行里直接提到 fcstm 或「投影」。"
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
    if rec.get("boundary_ruling"):
        flags.append((
            "boundary",
            f"已有边界裁定 `{rec.get('boundary_ruling')}`："
            f"{rec.get('boundary_rationale') or '（无理由记录）'}",
        ))
    if rec.get("pending_statement_rewrite"):
        flags.append(("pending_rewrite", "该条 statement 已被登记为待重写。"))
    return flags


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


#: `gen` 字段**逐字否认作者制品在该处有东西**的两种写法。
#: ⛔ 判据只认这两种字面形态，⛔ 不做语义推断 —— 见 `denies_artifact_defect()`。
_GEN_DENIAL_DASHES = ("—", "-", "", "无")
_GEN_DENIAL_PHRASE = "不可能生成"


def denies_artifact_defect(diff):
    """这条审阅 diff 的 `gen` 字段是不是**逐字否认作者制品在该处有问题**？

    ⚠️⚠️ **这类记录与其余候选不是同一个物种，⛔ §3 必须把它们分出来单列。**

    座标系的判定测试全部锚在**作者源 PlantUML** 上（类型学 §3.0）。而这一类记录的
    `gen` 侧写的是「—」或「(不可能生成)」，即逐字声明**作者制品在该处什么都没有、
    也不该有**；它真正主张的是**参考模型 / 真值的有效性**（「参考侧含 NL 推不出的内容，
    任何 LLM 都无法复现却会计入 FN」），⛔ 不是一种缺陷形态。这类在制品内指不出任何
    一处，卡在轴 0。

    ⛔⛔ **所以它们不得被拿去当「新座标系覆盖不到」的证据。** 座标系没覆盖到它们是
    因为它们本来就不在座标系要描述的对象集合里 —— ⛔ 那不是缺口。⭐ 真缺口只有一处，
    见 [candidate_mapping.py](./candidate_mapping.py) 的 `BLOCKERS` 说明。

    判据是**字面**的，故可被读者在页面上自行核对（渲染出来的「生成侧：—」那一行就是
    依据）：`gen` 去空白后为破折号 / 空 / 「无」，或含「不可能生成」。
    ⛔ 刻意**不**做语义推断 —— 相邻还有一族 `gen` 写「(生成方在第 2、4 句优于参考)」
    的记录（全语料 5 条），它们同样不指认制品缺陷，⚠️ 但「优于参考」是一句**相对评价**
    而非否认，字面判据吃不进来，故本函数**不收**它们；要处理那一族需要另立判据。
    """
    gen = (diff.get("gen") or "").strip()
    return gen in _GEN_DENIAL_DASHES or _GEN_DENIAL_PHRASE in gen


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
