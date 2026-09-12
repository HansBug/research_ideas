"""逐行 audit-trail 汇总 — 把人工签字 + 双 annotator 提案 + ref/pred 实例
原文 + 原始 raw JSON 指针拼成一张可追溯结构化表。

输出 3 件套，均落 ``eval/results/`` 下：

1. ``full_annotations.parquet``：列见 ``FULL_COLUMNS``。每行 = packs 里 ``## #N``
   一行 + 两个 annotator 对该 pair 的完整意见 + 你的签字结果 + 反向指针。
   这张表是 paper-claim 的最终证据载体。
2. ``full_annotations.csv``：同上 CSV 版（便于手工 grep / Excel 复核）。
3. ``REPORT.md``：中文 human-readable 报告，含口径声明 + 关键统计 + 分歧抽样 +
   指向 ``full_annotations.parquet`` 的列字典。

签字完成性硬检查：任何 ``user_choice == "unsigned"`` → 直接 raise，并打印未签
名清单 + 对应 markdown 路径。
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import pandas as pd


FULL_COLUMNS = [
    # locator
    "case_id", "condition", "component_kind", "row_id",
    # ref instance (ground-truth side)
    "ref_id", "ref_name", "ref_text",
    # pred instance (model-under-eval side)
    "pred_id", "pred_name", "pred_text",
    # claude annotation (full)
    "claude_status", "claude_match_kind", "claude_confidence", "claude_rationale",
    # codex annotation (full)
    "codex_status", "codex_match_kind", "codex_confidence", "codex_rationale",
    # agreement
    "agreement",
    # user sign-off
    "auto_marked", "user_choice", "user_final_status", "user_note",
    # audit pointers
    "pack_path", "raw_claude_path", "raw_codex_path",
]


class UnsignedRowsError(RuntimeError):
    """有评审包行尚未签字，refuse to finalize。"""


def _load_json(p: Path) -> Optional[dict[str, Any]]:
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _index_raw_by_pair(raw_blob: Optional[dict[str, Any]]) -> dict[tuple[Optional[str], Optional[str]], dict[str, Any]]:
    out: dict[tuple, dict] = {}
    if not raw_blob:
        return out
    for row in raw_blob.get("annotations", []) or []:
        key = (row.get("ref_id"), row.get("pred_id"))
        out[key] = row
    return out


def _find_instance_text(instances: list[dict[str, Any]], iid: Optional[str]) -> tuple[str, str]:
    """Return (name, text) for the given instance id, or empty strings if not found."""
    if iid is None:
        return "", ""
    for x in instances:
        if x.get("id") == iid:
            name = (
                x.get("name")
                or x.get("expr")
                or x.get("code")
                or ""
            )
            return str(name), str(x.get("text", ""))
    return "", ""


def _classify_agreement(claude_row: Optional[dict], codex_row: Optional[dict]) -> str:
    """One of: 'both_agree' / 'disagree' / 'claude_only' / 'codex_only' / 'neither'."""
    cs = (claude_row or {}).get("status")
    gs = (codex_row or {}).get("status")
    if cs and gs:
        return "both_agree" if cs == gs else "disagree"
    if cs and not gs:
        return "claude_only"
    if gs and not cs:
        return "codex_only"
    return "neither"


def build_full_annotations(
    *,
    reviewed_parquet: Path,
    raw_dir: Path,
    refs_dir: Path,
    preds_dir: Path,
    packs_dir: Path,
) -> pd.DataFrame:
    """Join reviewed.parquet with raw annotator JSON + ref/pred component
    JSONs to produce the full audit-trail DataFrame.
    """
    reviewed = pd.read_parquet(reviewed_parquet)
    if not len(reviewed):
        return pd.DataFrame(columns=FULL_COLUMNS)

    # cache of (case, kind) -> ref instances
    ref_cache: dict[str, dict[str, list[dict]]] = {}
    pred_cache: dict[tuple[str, str], dict[str, list[dict]]] = {}

    def _ref_instances(case_id: str, kind: str) -> list[dict]:
        if case_id not in ref_cache:
            blob = _load_json(refs_dir / case_id / "ref_components.json") or {}
            ref_cache[case_id] = blob
        return (ref_cache[case_id] or {}).get(kind, []) or []

    def _pred_instances(case_id: str, condition: str, kind: str) -> list[dict]:
        key = (case_id, condition)
        if key not in pred_cache:
            blob = _load_json(preds_dir / case_id / f"{condition}.json") or {}
            pred_cache[key] = blob
        return (pred_cache[key] or {}).get(kind, []) or []

    # cache of (case, cond, kind) -> (claude_index, codex_index, paths)
    raw_cache: dict[tuple, tuple[dict, dict, Path, Path]] = {}

    def _raw_for(case_id: str, condition: str, kind: str):
        key = (case_id, condition, kind)
        if key not in raw_cache:
            d = raw_dir / case_id / condition / kind
            c_blob = _load_json(d / "claude.json")
            g_blob = _load_json(d / "codex.json")
            raw_cache[key] = (
                _index_raw_by_pair(c_blob),
                _index_raw_by_pair(g_blob),
                d / "claude.json",
                d / "codex.json",
            )
        return raw_cache[key]

    rows: list[dict[str, Any]] = []
    for _, r in reviewed.iterrows():
        case_id = r["case_id"]
        condition = r["condition"]
        kind = r["component_kind"]
        ref_id = r["ref_id"] if pd.notna(r["ref_id"]) else None
        pred_id = r["pred_id"] if pd.notna(r["pred_id"]) else None

        ref_inst = _ref_instances(case_id, kind)
        pred_inst = _pred_instances(case_id, condition, kind)
        ref_name, ref_text = _find_instance_text(ref_inst, ref_id)
        pred_name, pred_text = _find_instance_text(pred_inst, pred_id)

        c_idx, g_idx, c_path, g_path = _raw_for(case_id, condition, kind)
        c_row = c_idx.get((ref_id, pred_id))
        g_row = g_idx.get((ref_id, pred_id))

        pack_path = packs_dir / case_id / condition / f"{kind}.md"

        rows.append({
            "case_id": case_id,
            "condition": condition,
            "component_kind": kind,
            "row_id": r["row_id"],

            "ref_id": ref_id,
            "ref_name": ref_name,
            "ref_text": ref_text,

            "pred_id": pred_id,
            "pred_name": pred_name,
            "pred_text": pred_text,

            "claude_status": (c_row or {}).get("status", ""),
            "claude_match_kind": (c_row or {}).get("match_kind", ""),
            "claude_confidence": float((c_row or {}).get("confidence", 0.0) or 0.0),
            "claude_rationale": (c_row or {}).get("rationale", ""),

            "codex_status": (g_row or {}).get("status", ""),
            "codex_match_kind": (g_row or {}).get("match_kind", ""),
            "codex_confidence": float((g_row or {}).get("confidence", 0.0) or 0.0),
            "codex_rationale": (g_row or {}).get("rationale", ""),

            "agreement": _classify_agreement(c_row, g_row),

            "auto_marked": bool(r.get("auto_marked", False)),
            "user_choice": r["user_choice"],
            "user_final_status": r.get("user_final_status", "") or "",
            "user_note": r.get("user_note", "") or "",

            "pack_path": str(pack_path),
            "raw_claude_path": str(c_path),
            "raw_codex_path": str(g_path),
        })

    df = pd.DataFrame(rows, columns=FULL_COLUMNS)
    return df


def check_signoff_complete(df: pd.DataFrame) -> None:
    """Raise ``UnsignedRowsError`` if any row is unsigned, with full pointer list."""
    unsigned = df[df["user_choice"] == "unsigned"]
    if not len(unsigned):
        return
    lines = [
        f"❌ 共 {len(unsigned)} 行尚未签字，refuse to finalize。请回到下列 markdown 包逐行勾选：",
        "",
    ]
    grouped = unsigned.groupby(["case_id", "condition", "component_kind"])
    for (case, cond, kind), grp in grouped:
        rowids = sorted(grp["row_id"].tolist())
        path = grp.iloc[0]["pack_path"]
        lines.append(f"- {path}  ({len(grp)} 行: {', '.join(rowids)})")
    msg = "\n".join(lines)
    raise UnsignedRowsError(msg)


def _zh(s: str) -> str:
    return {
        "states": "状态",
        "transitions": "迁移",
        "guards": "守卫",
        "actions": "动作",
        "hierarchical_states": "层次状态",
        "TP": "TP（命中）",
        "FP": "FP（假阳）",
        "FN": "FN（漏报）",
        "both_agree": "✅ 一致",
        "disagree": "🔴 不一致",
        "claude_only": "🟡 仅 Claude",
        "codex_only": "🟡 仅 gpt-5.5",
        "neither": "🔴 双方未提案",
        "accept_claude": "采纳 Claude",
        "accept_codex": "采纳 gpt-5.5",
        "amend": "修改",
        "reject": "否决",
        "unsigned": "未签字",
    }.get(s, s)


def _prf(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    p = tp / (tp + fp) if (tp + fp) else 0.0
    r = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) else 0.0
    return p, r, f1


def build_report_md(df: pd.DataFrame, *, out_path: Path) -> Path:
    """中文 audit-trail report — 指向 full_annotations.parquet 的 human-readable summary。"""
    L: list[str] = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    L += [
        "# Path 1 评审结果 audit-trail 报告",
        "",
        f"生成时间：`{now}`",
        "",
        "本报告是 `full_annotations.parquet` 的 human-readable 浓缩版。每一项 P/R/F1 都可以反向追溯到具体的 `(case_id, condition, component_kind, row_id)` + 两 annotator 的 rationale + 你的签字行为。",
        "",
        "## 1. 数据完成度",
        "",
        f"- **总行数**：{len(df)}",
        f"- **已签字**：{int((df['user_choice']!='unsigned').sum())}",
        f"- **未签字**：{int((df['user_choice']=='unsigned').sum())}（>0 视为未完成评审）",
        f"- **自动预勾选（两边一致 ✅）**：{int(df['auto_marked'].sum())} 行 — 这些行人工已默认采纳",
        f"- **需人工裁定的行**：{int((~df['auto_marked']).sum())} 行（含 🔴 / 🟡 单票 / 双方未提案）",
        "",
        "## 2. 签字选择分布",
        "",
        "| user_choice | 行数 | 占比 |",
        "| --- | ---: | ---: |",
    ]
    choice_counts = df["user_choice"].value_counts(dropna=False)
    total = len(df)
    for c, n in choice_counts.items():
        L.append(f"| {_zh(c)}（`{c}`） | {n} | {n / total * 100:.1f}% |")
    L += [
        "",
        "## 3. 双 annotator 一致性分布",
        "",
        "| agreement | 行数 | 占比 | 说明 |",
        "| --- | ---: | ---: | --- |",
    ]
    agreement_zh_desc = {
        "both_agree": "两边给同一 TP/FP/FN 标签，默认 ✅ 采纳 Claude",
        "disagree": "两边给不同标签，🔴 需要你裁定",
        "claude_only": "仅 Claude 给提案；可能 gpt-5.5 把这对解构成两条单边行",
        "codex_only": "仅 gpt-5.5 给提案；可能 Claude 把这对解构成两条单边行",
        "neither": "两边都没对该 pair 给出意见（极少出现）",
    }
    ag_counts = df["agreement"].value_counts(dropna=False)
    for k, n in ag_counts.items():
        L.append(f"| {_zh(k)} | {n} | {n / total * 100:.1f}% | {agreement_zh_desc.get(k, '')} |")
    L += ["", "## 4. 最终 P/R/F1（基于 `user_final_status` 计算）", ""]
    # detail per (case, cond, kind)
    signed = df[df["user_choice"] != "unsigned"].copy()
    L += [
        "### 4.1 按 case × condition × component",
        "",
        "| case_id | condition | component | TP | FP | FN | P | R | F1 |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for (case, cond, kind), grp in signed.groupby(["case_id", "condition", "component_kind"]):
        tp = int((grp["user_final_status"] == "TP").sum())
        fp = int((grp["user_final_status"] == "FP").sum())
        fn = int((grp["user_final_status"] == "FN").sum())
        p, r, f1 = _prf(tp, fp, fn)
        L.append(f"| {case} | {cond} | {_zh(kind)}（`{kind}`） | {tp} | {fp} | {fn} | {p:.3f} | {r:.3f} | **{f1:.3f}** |")
    L += ["", "### 4.2 按 case × condition 的 macro F1（5-component 平均）", ""]
    L += ["| case_id | condition | components_scored | macro F1 |", "| --- | --- | ---: | ---: |"]
    for (case, cond), grp in signed.groupby(["case_id", "condition"]):
        f1s = []
        for _, sub in grp.groupby("component_kind"):
            tp = int((sub["user_final_status"] == "TP").sum())
            fp = int((sub["user_final_status"] == "FP").sum())
            fn = int((sub["user_final_status"] == "FN").sum())
            _, _, f1 = _prf(tp, fp, fn)
            f1s.append(f1)
        macro = sum(f1s) / len(f1s) if f1s else 0.0
        L.append(f"| {case} | {cond} | {len(f1s)} | **{macro:.3f}** |")
    L += ["", "### 4.3 按 condition 的 overall F1（aggregate TP/FP/FN）", ""]
    L += ["| condition | TP | FP | FN | P | R | F1 |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for cond, grp in signed.groupby("condition"):
        tp = int((grp["user_final_status"] == "TP").sum())
        fp = int((grp["user_final_status"] == "FP").sum())
        fn = int((grp["user_final_status"] == "FN").sum())
        p, r, f1 = _prf(tp, fp, fn)
        L.append(f"| {cond} | {tp} | {fp} | {fn} | {p:.3f} | {r:.3f} | **{f1:.3f}** |")
    L += ["", "## 5. 用户介入热点（auto_marked=False 的行）", ""]
    hot = df[~df["auto_marked"]].copy()
    if len(hot):
        L.append(f"共 {len(hot)} 行需要你亲自审核，签字分布如下：")
        L += ["", "| pack | row_id | agreement | claude→codex | user_choice | final | note |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
        for _, h in hot.iterrows():
            pack_short = Path(h["pack_path"]).relative_to(Path(h["pack_path"]).parents[3]).as_posix()
            c2g = f"{h['claude_status'] or '—'}→{h['codex_status'] or '—'}"
            note = (h["user_note"] or "").replace("|", "\\|").strip()
            L.append(
                f"| `{pack_short}` | {h['row_id']} | {_zh(h['agreement'])} | {c2g} | "
                f"{_zh(h['user_choice'])} | {h['user_final_status'] or '—'} | {note} |"
            )
    else:
        L.append("（无）所有行 annotator 都一致，全部自动勾选；你只签字未自动勾选行 0 行。")
    L += [
        "",
        "## 6. 反向追溯字段说明 (`full_annotations.parquet` 列字典)",
        "",
        "| 列 | 含义 |",
        "| --- | --- |",
        "| `case_id`, `condition`, `component_kind`, `row_id` | 行定位四元组 |",
        "| `ref_id` / `ref_name` / `ref_text` | ref 实例 id + 名字 + 原文片段（指回 `data/refs/<case>/ref_components.json`）|",
        "| `pred_id` / `pred_name` / `pred_text` | pred 实例 id + 名字 + 原文片段（指回 `data/preds/<case>/<condition>.json`）|",
        "| `claude_status` / `claude_match_kind` / `claude_confidence` / `claude_rationale` | Claude annotator 完整提案 |",
        "| `codex_status` / `codex_match_kind` / `codex_confidence` / `codex_rationale` | gpt-5.5 annotator 完整提案 |",
        "| `agreement` | both_agree / disagree / claude_only / codex_only / neither |",
        "| `auto_marked` | 该行是否被自动 ✅ 预勾选（两边完全一致才会 True） |",
        "| `user_choice` | accept_claude / accept_codex / amend / reject / unsigned |",
        "| `user_final_status` | 你最终签字的 TP / FP / FN（aggregate 唯一信源）|",
        "| `user_note` | 你写的备注 |",
        "| `pack_path` | 该行所在的中文 markdown 包路径 |",
        "| `raw_claude_path` / `raw_codex_path` | 两个 annotator 的原始 JSON 全文路径 |",
        "",
        "## 7. 审计追溯链",
        "",
        "1. paper 写 \"manually evaluated\" → 证据来源是本表 `user_final_status` 列",
        "2. 任何 reviewer 可对任一行追问 \"为啥这条是 TP\" → 直接打开 `pack_path` 看 ref/pred 原文 + 双 annotator rationale + 你的签字行",
        "3. 任何对 metric 的复盘 → P/R/F1 公式见 §4，全部从 `user_final_status` 列重算可复现",
        "",
    ]
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(L), encoding="utf-8")
    return out_path


def finalize_all(
    *,
    reviewed_parquet: Path,
    raw_dir: Path,
    refs_dir: Path,
    preds_dir: Path,
    packs_dir: Path,
    out_dir: Path,
) -> dict[str, Path]:
    """End-to-end finalize: build full_annotations + sanity check + report."""
    df = build_full_annotations(
        reviewed_parquet=reviewed_parquet,
        raw_dir=raw_dir,
        refs_dir=refs_dir,
        preds_dir=preds_dir,
        packs_dir=packs_dir,
    )
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    full_pq = out_dir / "full_annotations.parquet"
    full_csv = out_dir / "full_annotations.csv"
    df.to_parquet(full_pq, index=False)
    df.to_csv(full_csv, index=False)

    # Sanity check AFTER persisting (so user can still see audit even when refused)
    check_signoff_complete(df)

    report_md = build_report_md(df, out_path=out_dir / "REPORT.md")
    return {
        "full_annotations_parquet": full_pq,
        "full_annotations_csv": full_csv,
        "report_md": report_md,
    }
