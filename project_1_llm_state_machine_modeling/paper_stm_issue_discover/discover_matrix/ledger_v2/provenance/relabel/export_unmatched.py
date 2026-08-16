#!/usr/bin/env python3
"""把两臂产出中**机械未匹配任何台账条目**的 issue 导出成 `unmatched_issues.json`。

⚠️ 为什么要单独一步导出：原始 run record 在 `runs/` 下，而 `runs/` 被 `.gitignore`
排除。工作单必须自包含，所以先把需要的文本抽出来落成一个可入库的 JSON。

⛔ 本脚本只读 run record，不写任何 run record、不改任何台账。

两臂的数据形状不同，必须分开说：

| | X1 朴素基线臂 | 主臂 v46 |
| :-- | :-- | :-- |
| 原始记录 | `runs/paper1/x1-baseline-v1/run{N}/<pair>-<arm>/record.json` → `.parsed_output.issues[]` | `runs/paper1/matrix-v46-full/run{N}/<pair>-<model>/discover-completed.json` → `.issues[]` |
| issue 形状 | `{issue, where, reason}` | `{issue_id, title, rationale, requirement_ids, ...}`（⛔ 无 `where`） |
| 未认领判据 | **人工**判据①②③（`comparison.md` §1.3），落在 `verdicts_x1.json.unclaimed_issues`，再减去 `X1-J*-reclaim.tsv` 的改判 | **机械** `round_variance._match`：元素重叠 ≥2（谓词一致时 ≥1），并列最高分不强配 |
| 本仓库是否有原始记录 | ✅ 有 | ⛔ **无** —— 在姊妹 clone `research_ideas/` 里 |

⚠️ 主臂原始记录不在本 clone。若 `--v46-runs` 指向的目录不存在，主臂部分会标为
`unavailable` 并写明原因，⛔ 不静默为空。
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MANUAL_REVIEW = os.path.dirname(HERE)

sys.path.insert(0, HERE)

# ⭐ 锚点一律复用 sources.py 的「按目录名向上找」，⛔ 不再数层数。
# ⚠️ 本文件在 2026-08-17 之前写的是 `PAPER = dirname(dirname(MANUAL_REVIEW))`：
# 归档进 `archive/r10_.../` 之后它实际解析到了 `archive/`，REPO 也随之偏移一层。
# 这类错位不会报错，只会让下面两个 runs 目录读成空 —— 正是 CLAUDE.md §9.5-3 说的那种静默失败。
from sources import PAPER  # noqa: E402

# `<repo>/project_1_llm_state_machine_modeling/paper_stm_issue_discover` → 上两级即仓库根。
# ⭐ 起点 PAPER 本身是按目录名找到的，所以这两级不随本文件搬家而变；⛔ 也不写死 checkout 目录名。
REPO = os.path.dirname(os.path.dirname(PAPER))

DEFAULT_X1_RUNS = os.path.join(REPO, "runs", "paper1", "x1-baseline-v1")
DEFAULT_V46_RUNS = os.path.join(
    os.path.dirname(REPO), "research_ideas", "runs", "paper1", "matrix-v46-full")


def _read_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _norm(text):
    return re.sub(r"\s+", " ", (text or "").strip().lower())


# ------------------------------------------------------------------ X1

def collect_x1(run_root):
    """返回 {pair: [entry]}，entry 是**未认领**（post-reclaim）的 issue。"""
    verdicts_path = os.path.join(
        PAPER, "baseline_arm", "results", "verdicts_x1.json")
    unclaimed = _read_json(verdicts_path)["unclaimed_issues"]

    # 减去 reclaim.tsv 里被改判为 claimed 的
    reclaimed = set()
    for f in sorted(glob.glob(os.path.join(
            PAPER, "baseline_arm", "results", "unexpected_verdicts",
            "X1-J*-reclaim.tsv"))):
        with open(f, "r", encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        head = lines[0].split("\t")
        for line in lines[1:]:
            if not line.strip():
                continue
            row = dict(zip(head, line.split("\t")))
            if row.get("new") == "claimed":
                reclaimed.add((row["cell"], int(row["idx"])))

    # X1-J*.jsonl 的 members 反查：已进多报桶的 issue 已经有裁定
    bucketed = {}
    for f in sorted(glob.glob(os.path.join(
            PAPER, "baseline_arm", "results", "unexpected_verdicts", "X1-J*.jsonl"))):
        if "-reclaim" in f or "-closure" in f:
            continue
        with open(f, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                for m in rec.get("members") or []:
                    mm = re.match(r"^(.*)#(\d+)$", m)
                    if mm:
                        bucketed[(mm.group(1), int(mm.group(2)))] = {
                            "cluster": rec.get("cluster"),
                            "verdict": rec.get("verdict"),
                            "subclass": rec.get("subclass"),
                        }

    out = {}
    missing_cells = []
    for cell, idxs in sorted(unclaimed.items()):
        run, tail = cell.split("/", 1)
        pair = tail.split("-", 1)[0]
        path = os.path.join(run_root, run, tail, "record.json")
        if not os.path.exists(path):
            missing_cells.append(cell)
            continue
        issues = (_read_json(path).get("parsed_output") or {}).get("issues") or []
        for idx in idxs:
            if (cell, idx) in reclaimed:
                continue
            if idx < 1 or idx > len(issues):
                continue
            it = issues[idx - 1]
            out.setdefault(pair, []).append({
                "arm": "X1",
                "cell": cell,
                "idx": idx,
                "issue": it.get("issue"),
                "where": it.get("where"),
                "reason": it.get("reason"),
                "adjudicated": bucketed.get((cell, idx)),
            })
    return out, missing_cells


# ------------------------------------------------------------------ 主臂 v46

def collect_v46(run_root, cell_pairs, ledger_pairs):
    """机械未匹配：复用 `round_variance` 的签名与匹配器。

    ⚠️ ⛔ 不能直接跑 `round_variance.main()` —— 它的 `PAIRS` 由「磁盘上最新的
    `runs/paper1/matrix-*`」推出，在不同 clone 上给出不同的 pair 集，会**静默**
    算出与已发布数字不同的结果。这里显式传台账自己的 pair 集。
    """
    if not os.path.isdir(run_root):
        return None, f"主臂原始 run record 不在本仓库：`{run_root}` 不存在"
    try:
        import round_variance as rv
    except Exception as exc:               # pragma: no cover
        return None, f"无法导入 round_variance：{exc}"

    # ⛔ 必须先钉住 PAIRS 再取台账 —— `_ledger_by_pair()` 会按 `rv.PAIRS` 过滤，
    # 而 `rv.PAIRS` 默认由磁盘上最新的 `runs/paper1/matrix-*` 推出，在不同 clone 上
    # 给出不同的 pair 集，会静默算出与已发布数字不同的结果。
    rv.PAIRS = tuple(sorted(ledger_pairs))
    ledger = rv._ledger_by_pair()

    out = {}
    for run in sorted(os.listdir(run_root)):
        rd = os.path.join(run_root, run)
        if not os.path.isdir(rd) or not run.startswith("run"):
            continue
        for cell in sorted(os.listdir(rd)):
            path = os.path.join(rd, cell, "discover-completed.json")
            if not os.path.exists(path):
                continue
            pair = cell.split("-", 1)[0]
            if pair not in cell_pairs:
                continue
            # ⛔ 必须走 `_read_cell` —— `discover-completed.json` 不总是带
            # `requirement_set`，缺了它签名就是空集、必然判为未匹配，会**虚高**
            # 未匹配数（实测：不走 fallback 得 944，走了得 755）。
            import pathlib
            cellinfo = rv._read_cell(pathlib.Path(os.path.join(rd, cell)))
            if not cellinfo or cellinfo.get("terminal") != "completed":
                continue
            data = cellinfo["record"]
            reqs = cellinfo["requirements"]
            entries = ledger.get(pair, [])
            for issue in data.get("issues") or []:
                sig = rv._issue_signature(issue, reqs)
                hit = rv._match(sig, entries)
                if hit is not None:
                    continue
                out.setdefault(pair, []).append({
                    "arm": "v46",
                    "cell": f"{run}/{cell}",
                    "issue_id": issue.get("issue_id"),
                    "issue": issue.get("title"),
                    "where": None,
                    "reason": issue.get("rationale"),
                    "requirement_ids": issue.get("requirement_ids"),
                    "adjudicated": None,
                })
    return out, None


# ------------------------------------------------------------------ 去重

def dedupe(entries):
    """按 (issue 文本, where) 归并同一主张的多格重复，保留一条代表 + 出现的格。"""
    buckets = {}
    for e in entries:
        key = hashlib.sha1(
            (_norm(e.get("issue")) + "||" + _norm(e.get("where"))).encode("utf-8")
        ).hexdigest()[:12]
        b = buckets.setdefault(key, dict(e, cells=[], key=key))
        b["cells"].append(e.get("cell"))
        if len(_norm(e.get("reason"))) > len(_norm(b.get("reason"))):
            b["reason"] = e.get("reason")
        if e.get("adjudicated") and not b.get("adjudicated"):
            b["adjudicated"] = e["adjudicated"]
    out = list(buckets.values())
    for b in out:
        b["cells"] = sorted(set(b["cells"]))
        b["cell_count"] = len(b["cells"])
        b.pop("cell", None)
    out.sort(key=lambda b: (-b["cell_count"], b["key"]))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--x1-runs", default=DEFAULT_X1_RUNS)
    ap.add_argument("--v46-runs", default=DEFAULT_V46_RUNS)
    ap.add_argument("--out", default=os.path.join(HERE, "unmatched_issues.json"))
    args = ap.parse_args()

    import sources

    ledger_pairs = sorted({r["pair"] for r in sources.ledger()["records"]})
    # 单元格侧不按台账 pair 集过滤：**台账 0 条的 pair 恰恰最可能有漏**，
    # 把它们的产出全判为未匹配是正确结果，不是噪声。
    cell_pairs = set(sources.IN_SCOPE_PAIRS)

    notes = []
    by_pair = {}

    x1, missing = collect_x1(args.x1_runs)
    if missing:
        notes.append(f"X1：{len(missing)} 个格的 record.json 不存在（{missing[:5]} …）")
    for p, v in x1.items():
        by_pair.setdefault(p, []).extend(v)

    v46, err = collect_v46(args.v46_runs, cell_pairs, ledger_pairs)
    if err:
        notes.append(f"主臂 v46：{err}")
    for p, v in (v46 or {}).items():
        by_pair.setdefault(p, []).extend(v)

    merged = {p: dedupe(v) for p, v in sorted(by_pair.items())}

    payload = {
        "schema": "paper1.relabel.unmatched_issues.v1",
        "what_this_is": (
            "两臂产出中机械 / 人工判为「未匹配任何台账条目」的 issue 文本。"
            "⛔ 只读导出，不改任何台账。X1 侧口径为 post-reclaim 的未认领；"
            "主臂侧口径为 round_variance._match 不返回任何台账条目。"
        ),
        "sources": {
            "x1_runs": args.x1_runs,
            "v46_runs": args.v46_runs,
            "x1_unclaimed": "baseline_arm/results/verdicts_x1.json .unclaimed_issues",
            "x1_reclaim": "baseline_arm/results/unexpected_verdicts/X1-J*-reclaim.tsv",
            "v46_matcher": "discover_matrix/round_variance.py _issue_signature/_match",
        },
        "notes": notes,
        "totals": {
            "pairs": len(merged),
            "dedup_groups": sum(len(v) for v in merged.values()),
            "x1_raw": sum(len(v) for v in x1.values()),
            "v46_raw": sum(len(v) for v in (v46 or {}).values()),
        },
        "by_pair": merged,
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
    print(json.dumps(payload["totals"], ensure_ascii=False))
    for n in notes:
        print("⚠️", n)


if __name__ == "__main__":
    main()
