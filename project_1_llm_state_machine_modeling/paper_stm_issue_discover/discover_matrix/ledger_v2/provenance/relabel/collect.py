#!/usr/bin/env python3
"""把作者填好的工作单解析成结构化 JSON。

用法：

    python3 collect.py                       # 全部 54 份 → relabel_result.json
    python3 collect.py --pairs 0000 0009
    python3 collect.py --out /tmp/x.json
    python3 collect.py --stdout              # 不写盘，只打印

⭐ 工作单按 NL 组分在 `nl_XXXX/` 子目录里；路径由 `sources.worksheet_path()` 算，
⛔ 不靠 glob 扫盘（扫漏会静默变成「这份没填」）。

⛔ 本脚本**不合并回台账**。它只把 Markdown 里的勾选与自由文本转成 JSON；
合并是另一件事，需要单独的裁决与 PR。⛔ 它也不会修改 `<pair>.md`。

⚠️ 解析是**保守**的：看不懂的行原样收进 `raw_lines`，⛔ 不猜、不丢。
若某个字段既没勾选也没文本，值为 `null` 而不是空串 —— 「没填」与「填了空」
在校验时是两件事。
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import fillblocks as fb                            # noqa: E402
import inspectfindings as IF                        # noqa: E402
import newfields as NF                             # noqa: E402
import sources as S                                # noqa: E402

SCHEMA = "paper1.relabel.result.v1"

# ⭐ 勾选记号取自 [fillblocks.py](./fillblocks.py) 的 `CHECK_MARKS` —— ⛔ 不在这里另抄一份，
# ⚠️ 否则解析器与 `is_untouched` 会认不同的记号（那正是修掉的一个 bug）。
_RE_CHECK = re.compile(r"\[\s*[" + fb.CHECK_MARKS + r"]+\s*\]\s*([^\[\n]+)")
_RE_EMPTY_BOX = re.compile(r"\[\s*\]\s*([^\[\n]+)")
_RE_FIELD = re.compile(r"^\s*([一-龥A-Za-z_][一-龥A-Za-z0-9_ ()（）/]*?)\s*[:：]\s*(.*)$")


def parse_choice(line):
    """从 `裁决: [x] 保留  [ ] 修正` 抽出被勾选项。返回 (被勾选列表, 全部选项)。

    ⚠️ 取值就是**框后面那段文字**，⛔ 不是框的位置 —— 所以勾完把选项文字删掉
    （只留 `裁决: [x]`）等于**没勾**：`[x]` 后面没有任何字符，正则不匹配，
    ⛔ 那一行会退化成自由文本 `"[x]"`。⭐ 「怎么填」一节为此专门警告了一条。
    """
    chosen = [m.group(1).strip() for m in _RE_CHECK.finditer(line)]
    allopts = chosen + [m.group(1).strip() for m in _RE_EMPTY_BOX.finditer(line)]
    return chosen, allopts


def parse_fields(body, known=None, choice_fields=None):
    """把一个填写块解析成 {字段名: 值}。

    值的形态有两种：勾选行 → `{"chosen": [...], "options": [...]}`；
    自由文本行 → 字符串（可跨行，直到下一个已知字段名）。

    ⭐ `known` 给定时，**只有这些名字**能起一个新字段，其余带冒号的行一律并进当前字段。
    ⛔ 不给 `known` 会踩一个真坑：作者在 `statement` 里另起一行写
    「NL 第 3 句：…」，`NL 第 3 句` 恰好匹配字段名正则，于是那一行被当成新字段，
    `statement` 被就地截断而且**不报错**。§5 的新增登记块因此一律传 `known`。

    ⭐ `choice_fields` 给定时，**只有这些名字**可能被读成勾选行；其余一律读成文本。
    ⛔ 这条同样是实测出来的：作者写 `generated_side: [*] --> FinalState`，
    值里的 `[*]` 让旧判据（「值里同时有 `[` 和 `]` 就是勾选行」）把它读成一个
    **零选项的勾选行**，于是 `generated_side` 变成空 —— ⚠️ 而 `[*]` 恰恰是
    PlantUML 初始 / 终态伪状态的写法，⛔ 入口类缺陷的定位串几乎必然带它。
    ⭐ 兜底：即使没给 `choice_fields`，也只有在真的解析出选项时才算勾选行。
    """
    out = {}
    raw = []
    cur = None
    for line in body.splitlines():
        if not line.strip():
            if cur:
                out[cur] += "\n"
            continue
        # §5 的分支提示行不是内容，也不是字段。
        # 不剔除的后果很具体：`--- 上一行选了 element…---` 紧跟在勾选行之后，
        # 而它不匹配字段名正则（行首是 `-`），于是会被并进上一个字段的值里 ——
        # 值里静默多出一整行提示，去重判据与并表都跟着脏掉。
        if line.strip() in NF.TEMPLATE_HINTS:
            continue
        m = _RE_FIELD.match(line)
        if m and known is not None and m.group(1).strip() not in known:
            m = None
        if m is not None:
            name, rest = m.group(1).strip(), m.group(2)
            if choice_fields is None or name in choice_fields:
                chosen, opts = parse_choice(rest)
                if opts:
                    out[name] = {"chosen": chosen, "options": opts}
                    cur = None
                    continue
            out[name] = rest.strip()
            cur = name
            continue
        if cur and isinstance(out.get(cur), str):
            out[cur] = (out[cur] + "\n" + line.strip()).strip()
        else:
            raw.append(line.rstrip())
    for k, v in list(out.items()):
        if isinstance(v, str):
            v = v.strip()
            out[k] = v or None
    if raw:
        out["_raw_lines"] = raw
    return out


# ⭐ 清单项行。⛔ 三处宽容都是实测出来的**静默丢整条**写法：
#   ① 行首缩进或 Markdown 任务列表前缀（`- [x] REACH-01`）—— ⚠️ 而 `- [ ]` 恰恰是
#      GitHub 任务列表的通行写法，⛔ 支持任务列表的编辑器会自动补上那个 `-`；
#   ② 记号写成 `[✔]`（不在旧字符集内）或 `[xx]`（旧正则只收一个字符）；
#   ③ id 写成小写 `reach-01`（旧正则只收 `[A-Z]+`）。
# ⛔ 这三种写法此前都让**整条清单项从 `items` 里消失** —— 不是「未勾选」，是不存在：
# ⚠️ `checklist_items` 总数跟着变小，⛔ 而没有任何一处会报错。
_RE_CHK_ITEM = re.compile(
    r"^\s*(?:[-*+]\s+)?\[\s*([" + fb.CHECK_MARKS + r"]*)\s*\]\s*([A-Za-z]+-\d+)\s*(.*)$")

# ⭐ `·` 开头的是**机器生成的机械判据行**，⛔ 刻意不回收（它不是给人写的）。
_RE_CHK_MACHINE = "·"


def parse_checklist(body):
    """解析 §4 的清单块。返回 [{iid, checked, text, finding}]。

    ⭐ `iid` 一律**归一成大写**：作者手打 `reach-01` 与机器给的 `REACH-01` 必须是同一条，
    ⛔ 否则并表时会变成两条。

    ⚠️ 清单项**下面**的自由文本，不带 `发现:` 前缀也照收进 `finding` —— ⛔ 旧行为是
    整行丢弃且**不留痕迹**（`parse_checklist` 没有 `raw_lines` 兜底），⭐ 而「勾上之后
    直接在下一行写发现」是最自然的写法。⛔ 唯一不收的是 `·` 开头那行。
    """
    items = []
    cur = None
    for line in body.splitlines():
        m = _RE_CHK_ITEM.match(line)
        if m:
            cur = {"iid": m.group(2).upper(), "checked": bool(m.group(1).strip()),
                   "text": m.group(3).strip(), "finding": None}
            items.append(cur)
            continue
        if cur is None:
            continue
        m = re.match(r"^\s*发现\s*[:：]\s*(.*)$", line)
        if m:
            cur["finding"] = m.group(1).strip() or None
            continue
        if line.strip() and not line.strip().startswith(_RE_CHK_MACHINE):
            cur["finding"] = ((cur["finding"] or "") + "\n" + line.strip()).strip()
    return items


def parse_new(body, pair):
    """解析 §5 的新增登记块。返回 [{id, pair, fields, derived}]。

    `fields` 是人工填的项：条件式座标系的几个勾选轴 + `statement` +
    `expected_after_fix` + `nl_evidence`（+ 可选 `property_pattern`）；
    `derived` 是 [newfields.py](./newfields.py) `derive()` 当下能算出来的部分 ——
    算不出来的字段留 `None` 并在 `pending` 里写明为什么，不猜。

    走 element 支时 `derive()` 会把维度 A 映成 `element_of_M`（`state` → `S`、
    `transition` / `guard` → `Tr`、`trigger` → `E`、`effect` → `A`、`variable` → `V`）；
    走逻辑支时该字段留 `None` —— 逻辑层缺陷按定义不落在单个 $M$ 分量上。
    """
    # ⭐ `#` 的个数与后面的空格都放宽：⛔ 写成 `###NEW-…`（漏空格）或 `## NEW-…`（少一个 `#`）
    # 此前**不会**切出新条目，⚠️ 于是该条的全部字段被并进**上一条**（若它是第一条则整条消失）——
    # ⛔ 两种都是静默的。⭐ id 也放宽到大小写不敏感，并归一成大写。
    chunks = re.split(r"^#{2,6}\s*", body, flags=re.M)
    out = []
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        head, _, rest = chunk.partition("\n")
        m = re.match(r"^NEW-\d{4}-\d+", head.strip(), re.I)
        if not m:
            continue
        # ⭐ 只取匹配到的那一段当 id：标题后面若跟了别的字（`### NEW-0000-03 （补）`），
        # ⛔ 旧行为会把整行当 id，于是 id 里混进注释。
        nid = m.group(0).upper()
        fields = parse_fields(rest, known=NF.FIELD_NAMES,
                              choice_fields=NF.CHOICE_FIELDS)
        rec = {"id": nid, "pair": pair, "fields": fields}
        if not _is_blank_new(rec):
            rec["derived"] = NF.derive(pair, nid, fields)
        out.append(rec)
    return out


def _is_blank_new(rec):
    f = rec.get("fields") or {}
    for k, v in f.items():
        if k.startswith("_"):
            continue
        if isinstance(v, dict):
            if v.get("chosen"):
                return False
        elif v:
            return False
    return True


def _locus_counts(result):
    """新增条目按 `defect_locus` 的分布。未填的计入 `未填`。"""
    from collections import Counter
    c = Counter(NF.field_value(r.get("fields") or {}, "defect_locus") or "未填"
                for v in result.values() for r in v["new_issues"])
    return dict(sorted(c.items()))


def _candidate_source(key):
    """候选填写块 key → 它的来源。⛔ inspect 一族要连**物种**一起报。

    ⚠️ 三份 audit json 不在树上时退回 `inspect_finding` —— ⛔ 不许抛：`collect.py` 的职责是
    回收人填的内容，⛔ 判定文件缺失不该让整轮回收失败（照 CLAUDE.md §10 降级而不是崩）。
    """
    for prefix, name in (("VU-", "valid_unrecorded"), ("DIFF-", "review_diff"),
                         ("UM-", "unmatched_issue")):
        if key.startswith(prefix):
            return name
    if key.startswith("INS-"):
        try:
            return "inspect_finding_" + IF.verdict_class_of(key)
        except Exception:
            return "inspect_finding"
    return "unknown"


def collect_pair(pair, path):
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    blocks = fb.extract(text)
    kinds = {}
    for m in re.finditer(r"<!--\s*FILL:BEGIN\s+key=(\S+)\s+kind=(\S+)\s*-->", text):
        kinds[m.group(1)] = m.group(2)

    out = {
        "pair": pair,
        "summary": None,
        "ledger": [],
        "candidates": [],
        "checklist": [],
        "new_issues": [],
        "orphans": {},
        "untouched_keys": [],
    }
    for key, body in blocks.items():
        kind = kinds.get(key, "orphan")
        # ⚠️ 清单块必须走专用判据 `checklist_is_untouched`:通用的 `is_untouched`
        # 只比模板全等,而清单块的模板含逐条 id 与机械判据行,判读者哪怕一个字没填,
        # 渲染出的 body 也与「空模板」不字面相等 —— 于是未填的清单块被误报成已填。
        # 实测 `0039` 五个未填清单块里有四个被误报。
        if kind == "checklist":
            untouched = fb.checklist_is_untouched(body)
        else:
            untouched = fb.is_untouched(body, kind, pair, key=key)
        if untouched:
            out["untouched_keys"].append(key)
        # ⭐ §0 / §2 / §3 三种块也必须传 `known` 与 `choice_fields`（表在 `fillblocks` 里，
        # ⛔ 逐字从模板算出来）—— ⚠️ 此前只有 §5 传，于是这三种块吃着两个静默丢内容的坑：
        # 续行里带冒号会截断当前字段、值里带 `[ ]` 会被误读成勾选行。⭐ 见 `fillblocks` 的注释。
        if kind == "pair":
            out["summary"] = parse_fields(body, known=fb.name_variants(fb.PAIR_FIELDS),
                                          choice_fields=fb.name_variants(fb.PAIR_CHOICES))
        elif kind == "ledger":
            out["ledger"].append({
                "id": key,
                **parse_fields(body, known=fb.name_variants(fb.LEDGER_FIELDS),
                               choice_fields=fb.name_variants(fb.LEDGER_CHOICES)),
            })
        elif kind == "candidate":
            out["candidates"].append({
                "key": key,
                # ⚠️ inspect 一族的两个物种（确认内生 / 分拣未定）**必须在回收时分得开** ——
                # ⛔ 混在一起统计会把「工具确定看到的」与「可能是投影造出来的」算成同一种证据。
                # ⭐ 分法由 [inspect_issues.json](./inspect_issues.json) 的 `verdict_class` 给，
                # ⛔ 不再靠 `INSU-` 这种前缀约定：填写块的 key 与 issue id 必须是同一个字符串，
                # ⚠️ 两套命名会让「工作单里那一条对应 audit json 里哪一条」需要转换才能对上。
                "source": _candidate_source(key),
                **parse_fields(body, known=fb.name_variants(fb.CANDIDATE_FIELDS),
                               choice_fields=fb.name_variants(fb.CANDIDATE_CHOICES)),
            })
        elif kind == "checklist":
            out["checklist"].append({"key": key, "items": parse_checklist(body)})
        elif kind == "new":
            out["new_issues"] = [r for r in parse_new(body, pair) if not _is_blank_new(r)]
        else:
            out["orphans"][key] = body
    out["ledger"].sort(key=lambda r: r["id"])
    out["candidates"].sort(key=lambda r: r["key"])
    out["checklist"].sort(key=lambda r: r["key"])
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pairs", nargs="*", default=None)
    ap.add_argument("--dir", default=HERE)
    ap.add_argument("--out", default=os.path.join(HERE, "relabel_result.json"))
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args()

    pairs = args.pairs or list(S.IN_SCOPE_PAIRS)
    result = {}
    missing = []
    for pair in pairs:
        # ⭐ 工作单在 `nl_XXXX/` 子目录里，⛔ 不在 `--dir` 根上。
        # ⚠️ 这里**不用** glob 扫盘，而是按 `IN_SCOPE_PAIRS` 逐个算路径 —— ⛔ 扫盘扫漏
        # 会静默变成「这个 pair 没填」，而按名单取路径缺一份就进 `missing_worksheets`。
        path = S.worksheet_path(args.dir, pair)
        if not os.path.exists(path):
            missing.append(pair)
            continue
        result[pair] = collect_pair(pair, path)

    payload = {
        "schema": SCHEMA,
        "collected_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "what_this_is": (
            "人工重标工作单的结构化回收结果。⛔ 这不是台账 —— 合并回 "
            "expected_issue_set.json 需要单独的裁决与 PR。"
        ),
        "missing_worksheets": missing,
        "totals": {
            "pairs": len(result),
            "ledger_records_seen": sum(len(v["ledger"]) for v in result.values()),
            "candidates_seen": sum(len(v["candidates"]) for v in result.values()),
            # 登记总数。边界（时钟 / 不变式 / 并发）不再由判读者分类，故这里
            # **不再拆**「界内 / 越界」两栏 —— 分拣改为回收后由主 session 读
            # `statement` 自由文本人工做，见 [README.md](./README.md) §二.1。
            "new_issues": sum(len(v["new_issues"]) for v in result.values()),
            # 走 element 支与走逻辑支各多少条。这是**座标系自己的**分布，
            # 确定性可算（只看 `defect_locus` 一个字段），拿来看判读者实际用到了哪一支。
            "new_issues_by_locus": _locus_counts(result),
            "checklist_items": sum(len(c["items"]) for v in result.values()
                                   for c in v["checklist"]),
            "checklist_checked": sum(1 for v in result.values() for c in v["checklist"]
                                     for i in c["items"] if i["checked"]),
            "checklist_findings": sum(1 for v in result.values() for c in v["checklist"]
                                      for i in c["items"] if i["finding"]),
            "untouched_blocks": sum(len(v["untouched_keys"]) for v in result.values()),
            "orphan_blocks": sum(len(v["orphans"]) for v in result.values()),
        },
        "pairs": result,
    }
    text = json.dumps(payload, ensure_ascii=False, indent=1)
    if args.stdout:
        print(text)
    else:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(json.dumps(payload["totals"], ensure_ascii=False))
        if missing:
            print("⚠️ 缺工作单：" + " ".join(missing))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
