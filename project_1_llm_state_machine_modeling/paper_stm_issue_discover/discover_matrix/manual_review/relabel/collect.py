#!/usr/bin/env python3
"""把作者填好的工作单解析成结构化 JSON。

用法：

    python3 collect.py                       # 全部 54 份 → relabel_result.json
    python3 collect.py --pairs 0000 0009
    python3 collect.py --out /tmp/x.json
    python3 collect.py --stdout              # 不写盘，只打印

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
import newfields as NF                             # noqa: E402
import sources as S                                # noqa: E402

SCHEMA = "paper1.relabel.result.v1"

_RE_CHECK = re.compile(r"\[\s*([xX✓√])\s*\]\s*([^\[\n]+)")
_RE_EMPTY_BOX = re.compile(r"\[\s*\]\s*([^\[\n]+)")
_RE_FIELD = re.compile(r"^\s*([一-龥A-Za-z_][一-龥A-Za-z0-9_ ()（）/]*?)\s*[:：]\s*(.*)$")


def parse_choice(line):
    """从 `裁决: [x] 保留  [ ] 修正` 抽出被勾选项。返回 (被勾选列表, 全部选项)。"""
    chosen = [m.group(2).strip() for m in _RE_CHECK.finditer(line)]
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


def parse_checklist(body):
    """解析 §4 的清单块。返回 [{iid, checked, text, finding}]。"""
    items = []
    cur = None
    for line in body.splitlines():
        m = re.match(r"^\[\s*([xX✓√ ]?)\s*\]\s*([A-Z]+-\d+)\s*(.*)$", line)
        if m:
            cur = {"iid": m.group(2), "checked": bool(m.group(1).strip()),
                   "text": m.group(3).strip(), "finding": None}
            items.append(cur)
            continue
        if cur is None:
            continue
        m = re.match(r"^\s*发现\s*[:：]\s*(.*)$", line)
        if m:
            cur["finding"] = m.group(1).strip() or None
            cur["_in_finding"] = True
            continue
        if cur.get("_in_finding") and line.strip() and not line.strip().startswith("·"):
            cur["finding"] = ((cur["finding"] or "") + "\n" + line.strip()).strip()
    for it in items:
        it.pop("_in_finding", None)
    return items


def parse_new(body, pair):
    """解析 §5 的新增登记块。返回 [{id, pair, fields, derived}]。

    ⭐ `fields` 是人工填的 8 项（5 必填 + 3 可选）；`derived` 是
    [newfields.py](./newfields.py) `derive()` 当下能算出来的部分 ——
    ⛔ 算不出来的字段留 `None` 并在 `pending` 里写明为什么，⛔ 不猜。
    """
    chunks = re.split(r"^###\s+", body, flags=re.M)
    out = []
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        head, _, rest = chunk.partition("\n")
        nid = head.strip()
        if not re.match(r"^NEW-\d{4}-\d+", nid):
            continue
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
        if fb.is_untouched(body, kind, pair):
            out["untouched_keys"].append(key)
        if kind == "pair":
            out["summary"] = parse_fields(body)
        elif kind == "ledger":
            out["ledger"].append({"id": key, **parse_fields(body)})
        elif kind == "candidate":
            out["candidates"].append({
                "key": key,
                "source": ("valid_unrecorded" if key.startswith("VU-")
                           else "review_diff" if key.startswith("DIFF-")
                           else "unmatched_issue" if key.startswith("UM-")
                           else "unknown"),
                **parse_fields(body),
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
        path = os.path.join(args.dir, f"{pair}.md")
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
            "new_issues": sum(len(v["new_issues"]) for v in result.values()),
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
