"""把两个 annotator 的 JSON 输出渲染成中文 markdown 评审包。

输出文件：``packs/<case_id>/<condition>/<component_kind>.md``

每一行：
- ref 原文 / pred 原文
- Claude 提案 + 理由 + confidence
- gpt-5.5 提案 + 理由 + confidence
- 签字勾选区（采纳 Claude / gpt-5.5 / 修改 / 否决）

签字交由 ``review/load.py`` 解析回 parquet。
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional


_STATUS_ZH = {"TP": "TP（命中）", "FP": "FP（假阳）", "FN": "FN（漏报）"}


def _annot_index(annot: dict[str, Any]) -> dict[tuple[Optional[str], Optional[str]], dict[str, Any]]:
    """Build index keyed by (ref_id, pred_id)."""
    out: dict[tuple[Optional[str], Optional[str]], dict[str, Any]] = {}
    if not annot or "annotations" not in annot:
        return out
    for row in annot.get("annotations", []) or []:
        key = (row.get("ref_id"), row.get("pred_id"))
        out[key] = row
    return out


def _all_keys(
    ref_instances: list[dict[str, Any]],
    pred_instances: list[dict[str, Any]],
    claude_index: dict[tuple, dict[str, Any]],
    codex_index: dict[tuple, dict[str, Any]],
) -> list[tuple[Optional[str], Optional[str]]]:
    """Union over both annotators + any orphan ref/pred not mentioned by either.

    Sort: TP-ish pairs first (both ids non-null), then FN (ref-only), then FP (pred-only).
    """
    seen: set[tuple] = set()
    rows: list[tuple] = []
    for k in list(claude_index.keys()) + list(codex_index.keys()):
        if k in seen:
            continue
        seen.add(k)
        rows.append(k)
    # add orphans
    for r in ref_instances:
        k = (r["id"], None)
        if k not in seen and not any(k0 for k0 in seen if k0[0] == r["id"]):
            seen.add(k)
            rows.append(k)
    for p in pred_instances:
        k = (None, p["id"])
        if k not in seen and not any(k0 for k0 in seen if k0[1] == p["id"]):
            seen.add(k)
            rows.append(k)

    def sort_key(k):
        ref, pred = k
        if ref and pred:
            return (0, ref)
        if ref:
            return (1, ref)
        return (2, pred or "")
    rows.sort(key=sort_key)
    return rows


def _find_instance(instances: list[dict[str, Any]], iid: Optional[str]) -> Optional[dict[str, Any]]:
    if iid is None:
        return None
    for x in instances:
        if x.get("id") == iid:
            return x
    return None


def _instance_brief(inst: Optional[dict[str, Any]]) -> str:
    if inst is None:
        return "（无）"
    name = inst.get("name") or inst.get("expr") or inst.get("code") or ""
    text = (inst.get("text") or "").strip().replace("\n", " ")
    if len(text) > 200:
        text = text[:200] + "…"
    parts = []
    if name:
        parts.append(f"`{name}`")
    if text:
        parts.append(f"原文：`{text}`")
    return "；".join(parts) if parts else "（空）"


def _annot_brief(row: Optional[dict[str, Any]]) -> str:
    if row is None:
        return "（未提及）"
    status = row.get("status", "?")
    mk = row.get("match_kind", "?")
    conf = row.get("confidence", 0.0)
    try:
        conf = float(conf)
    except Exception:
        conf = 0.0
    status_zh = _STATUS_ZH.get(status, status)
    rationale = (row.get("rationale") or "").strip().replace("\n", " ")
    return f"**{status_zh}**（match_kind={mk}, confidence={conf:.2f}）  \n  理由：{rationale}"


def render_pack(
    *,
    case_id: str,
    condition: str,
    component_kind: str,
    ref_instances: list[dict[str, Any]],
    pred_instances: list[dict[str, Any]],
    claude_result: Optional[dict[str, Any]],
    codex_result: Optional[dict[str, Any]],
    out_path: Path,
    nl_text: str = "",
    ref_model_text: str = "",
    pred_model_text: str = "",
) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    cidx = _annot_index(claude_result or {})
    gidx = _annot_index(codex_result or {})
    keys = _all_keys(ref_instances, pred_instances, cidx, gidx)

    component_zh = {
        "states": "states (状态)",
        "transitions": "transitions (迁移)",
        "guards": "guards (守卫)",
        "actions": "actions (动作)",
        "hierarchical_states": "hierarchical_states (层次状态)",
    }.get(component_kind, component_kind)

    lines = [
        f"# 评审包 — {case_id} / {condition} / {component_zh}",
        "",
        f"- ref 实例数：**{len(ref_instances)}**",
        f"- pred 实例数：**{len(pred_instances)}**",
        f"- Claude annotations：**{len((claude_result or {}).get('annotations', []))}**",
        f"- gpt-5.5 annotations：**{len((codex_result or {}).get('annotations', []))}**",
        "",
        "## 待评审材料",
        "",
    ]
    if nl_text.strip():
        lines += [
            "### 1) NL 原文（来自 sources/<case>/STM.md §2）",
            "",
            nl_text.strip(),
            "",
        ]
    if ref_model_text.strip():
        lines += [
            "### 2) Reference 状态机模型（人工签字 ref，作为 ground-truth）",
            "",
            "```",
            ref_model_text.strip(),
            "```",
            "",
        ]
    if pred_model_text.strip():
        lines += [
            "### 3) Predicted 状态机模型（被评对象，本条件下的输出）",
            "",
            "```",
            pred_model_text.strip(),
            "```",
            "",
        ]
    lines += [
        "---",
        "",
        "## 使用说明",
        "",
        "对每一行，在 **签字** 段勾选 `[x]`（4 选 1）：",
        "",
        "- `[ ] 采纳 Claude`",
        "- `[ ] 采纳 gpt-5.5`",
        "- `[ ] 修改 → final_status: ___ （TP/FP/FN）`",
        "- `[ ] 否决（两边都不对）→ final_status: ___`",
        "",
        "**自动预勾选规则**：",
        "",
        "- ✅ Claude 与 gpt-5.5 **完全一致** → 已默认勾选 `[x] 采纳 Claude`（与 gpt-5.5 等价）。如你不认同请手动改。",
        "- 🔴 两边 **不一致** → 留空 + heading 标 `🔴 需复议`，请你亲自决定。",
        "- 🟡 仅一方有提案 → 留空 + heading 标 `🟡 单票`，请你确认。",
        "- 🔴 两方都未对该行给出意见 → 留空 + heading 标 `🔴 双方未提案`。",
        "",
        "勾选默认空 → 该行视为未签字。把对应方框写成 `[x]` 表示采纳。`修改/否决` 时填写 final_status。备注栏可写任何文字。",
        "",
        "---",
        "",
    ]

    for idx, (ref_id, pred_id) in enumerate(keys, start=1):
        ref_inst = _find_instance(ref_instances, ref_id)
        pred_inst = _find_instance(pred_instances, pred_id)
        row_id = f"row{idx:03d}"

        claude_row = cidx.get((ref_id, pred_id))
        codex_row = gidx.get((ref_id, pred_id))
        claude_status = (claude_row or {}).get("status")
        codex_status = (codex_row or {}).get("status")

        # Decide auto-prefill behavior:
        # - both present and same status -> auto-prefill "采纳 Claude" (任选一边,两边等价)
        # - both present but disagree     -> 🔴 留空待你复议
        # - 只有一方有                    -> 🟡 留空（只一票）
        # - 两方都没有                    -> 🔴 留空 N/A
        if claude_status and codex_status:
            if claude_status == codex_status:
                heading_flag = "✅"
                claude_box = "[x]"
                codex_box = "[ ]"
                hint = "_两个 annotator 一致 → 已默认勾选 “采纳 Claude”（与 gpt-5.5 等价）；如不认同请手动改勾_"
            else:
                heading_flag = "🔴 需复议"
                claude_box = "[ ]"
                codex_box = "[ ]"
                hint = f"_⚠️ 两边不一致：Claude={claude_status} / gpt-5.5={codex_status}，请人工裁定_"
        elif claude_status or codex_status:
            heading_flag = "🟡 单票"
            claude_box = "[ ]"
            codex_box = "[ ]"
            who = "Claude" if claude_status else "gpt-5.5"
            hint = f"_⚠️ 仅 {who} 给了提案，另一方缺失；请确认_"
        else:
            heading_flag = "🔴 双方未提案"
            claude_box = "[ ]"
            codex_box = "[ ]"
            hint = "_⚠️ 两个 annotator 都未对这一行给出意见，需要你直接判定_"

        lines.append(f"## #{idx} {heading_flag}  ref `{ref_id or '∅'}` ↔ pred `{pred_id or '∅'}`  <!-- {row_id} -->")
        lines.append("")
        lines.append(f"- **ref 实例**：{_instance_brief(ref_inst)}")
        lines.append(f"- **pred 实例**：{_instance_brief(pred_inst)}")
        lines.append("")
        lines.append(f"- **Claude 提案**：{_annot_brief(claude_row)}")
        lines.append(f"- **gpt-5.5 提案**：{_annot_brief(codex_row)}")
        lines.append("")
        lines.append(f"{hint}")
        lines.append("")
        lines.append("**签字**：")
        lines.append(f"- {claude_box} 采纳 Claude")
        lines.append(f"- {codex_box} 采纳 gpt-5.5")
        lines.append("- [ ] 修改 → final_status: ____  （TP/FP/FN）")
        lines.append("- [ ] 否决 → final_status: ____")
        lines.append("- 备注：")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Footer: per-annotator summary
    lines.append("## Annotator 自报告 summary")
    lines.append("")
    for name, r in (("Claude", claude_result), ("gpt-5.5", codex_result)):
        if not r:
            lines.append(f"- **{name}**: （无结果）")
            continue
        s = r.get("summary", {}) or {}
        lines.append(
            f"- **{name}**：TP={s.get('tp', '?')}, FP={s.get('fp', '?')}, "
            f"FN={s.get('fn', '?')}；notes：{s.get('notes', '')}"
        )
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path
