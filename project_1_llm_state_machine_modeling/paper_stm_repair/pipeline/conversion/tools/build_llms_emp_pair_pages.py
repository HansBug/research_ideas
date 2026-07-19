#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shutil
from collections import Counter
from pathlib import Path


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "project_1_llm_state_machine_modeling").is_dir():
            return parent
    raise RuntimeError("repository root not found")


REPO_ROOT = _repo_root()
PAPER_ROOT = REPO_ROOT / "project_1_llm_state_machine_modeling/paper_stm_repair"
PAIRS_PATH = (
    PAPER_ROOT
    / "corpora/seed_library/llms-emp-stm-subset/assets/extracted"
    / "feedback_final_pairs.jsonl"
)
EVIDENCE_DIR = (
    PAPER_ROOT / "pipeline/representation/reports/llms_emp_r45_java_60"
)
MANUAL_ROW_RE = re.compile(
    r"^\| `(?P<case>\d{4})` \| `[0-9a-f]{64}` \| `[0-9a-f]{64}` "
    r"\| PASS \| (?P<notes>.+) \|$"
)


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _fence(language: str, text: str) -> str:
    suffix = "" if text.endswith("\n") else "\n"
    return f"```{language}\n{text}{suffix}```"


def _table_text(value: object) -> str:
    return str(value or "-").replace("|", "\\|").replace("\n", "<br>")


def _display_text(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines())


def _stage_lineage_lines(source_row: dict) -> list[str]:
    lines = [
        "| stage | output cell | present | output SHA-256 | feedback | resolved |",
        "|---|---|---|---|---|---|",
    ]
    for item in source_row["stage_lineage"]:
        output = item["output"]
        feedback = item["feedback"]
        resolved = item["resolved"]
        lines.append(
            "| `{stage}` | `{cell}` | `{present}` | `{sha}` | {feedback} | {resolved} |".format(
                stage=item["stage_id"],
                cell=output.get("cell") or "-",
                present=str(output["present"]).lower(),
                sha=output.get("sha256") or "-",
                feedback=_table_text(feedback.get("value")),
                resolved=_table_text(resolved.get("value")),
            )
        )
    return lines


def _normalization_lines(comparison: dict) -> list[str]:
    mappings = comparison["source_normalization_mappings"]
    if not mappings:
        return ["本组没有 source-input normalization。"]
    lines = [
        "| raw ref | rule | before | after |",
        "|---|---|---|---|",
    ]
    for item in mappings:
        lines.append(
            f"| `{item['raw_ref']}` | `{item['rule_id']}` | "
            f"`{_table_text(item['before'])}` | `{_table_text(item['after'])}` |"
        )
    return lines


def _official_identity_lines(reconciliation: dict) -> list[str]:
    lines = [
        f"- status：`{reconciliation['status']}`",
        f"- canonical / official states：`{reconciliation['canonical_state_count_after']}` / `{reconciliation['official_state_count']}`",
        f"- aligned transition endpoints：`{reconciliation['transition_identity_alignment_count']}`",
    ]
    state_remaps = reconciliation["state_identity_remaps"]
    transition_remaps = reconciliation["transition_endpoint_remaps"]
    if state_remaps:
        lines.extend(
            [
                "",
                "| source-parser identity | pinned PlantUML identity | raw ref | reason |",
                "|---|---|---|---|",
                *[
                    f"| `{item['before']}` | `{item['after']}` | `{item['raw_ref']}` | `{item['reason']}` |"
                    for item in state_remaps
                ],
            ]
        )
    else:
        lines.extend(["", "本组 state identity 无需重映射。"])
    if transition_remaps:
        lines.extend(
            [
                "",
                "| transition | source before -> after | target before -> after | raw ref |",
                "|---|---|---|---|",
                *[
                    "| `{transition}` | `{source_before}` -> `{source_after}` | "
                    "`{target_before}` -> `{target_after}` | `{raw_ref}` |".format(
                        transition=item["transition_id"],
                        source_before=item["source_before"],
                        source_after=item["source_after"],
                        target_before=item["target_before"],
                        target_after=item["target_after"],
                        raw_ref=item["raw_ref"],
                    )
                    for item in transition_remaps
                ],
            ]
        )
    else:
        lines.extend(["", "本组 transition endpoint 无需重映射。"])
    return lines


def _concurrent_region_lines(comparison: dict) -> list[str]:
    mappings = comparison["concurrent_region_mappings"]
    if not mappings:
        return ["本组没有 PlantUML orthogonal/concurrent region separator。"]
    lines = [
        "| owner | region | direct states | direct transitions | separator before | separator after |",
        "|---|---:|---|---|---|---|",
    ]
    for item in mappings:
        lines.append(
            "| `{owner}` | {region} | {states} | {transitions} | {before} | {after} |".format(
                owner=item.get("owner_scope") or "__root__",
                region=item["region_index"],
                states=_table_text(", ".join(item["state_ids"]) or "-"),
                transitions=_table_text(", ".join(item["transition_ids"]) or "-"),
                before=_table_text(", ".join(item["separator_before_raw_refs"]) or "-"),
                after=_table_text(", ".join(item["separator_after_raw_refs"]) or "-"),
            )
        )
    return lines


def _debt_lines(comparison: dict) -> list[str]:
    reasons = Counter(
        item["reason_code"] for item in comparison["operational_debts"]
    )
    return [
        "| reason code | count |",
        "|---|---:|",
        *[f"| `{reason}` | {count} |" for reason, count in sorted(reasons.items())],
    ]


def build_pair_pages() -> None:
    source_rows = [
        json.loads(line)
        for line in PAIRS_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    comparison_rows = {
        row["case_id"]: row
        for row in (
            json.loads(line)
            for line in (EVIDENCE_DIR / "comparison.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        )
    }
    manual_notes = {
        match.group("case"): match.group("notes")
        for line in (EVIDENCE_DIR / "MANUAL_REVIEW.md")
        .read_text(encoding="utf-8")
        .splitlines()
        if (match := MANUAL_ROW_RE.fullmatch(line)) is not None
    }
    expected_cases = [f"{index:04d}" for index in range(60)]
    actual_cases = [row["pair_id"][-4:] for row in source_rows]
    if actual_cases != expected_cases:
        raise RuntimeError(f"expected sequential 0000..0059 cases, got {actual_cases}")
    if set(comparison_rows) != set(expected_cases) or set(manual_notes) != set(expected_cases):
        raise RuntimeError("comparison/manual review does not cover all 60 cases")

    pages_dir = EVIDENCE_DIR / "pairs"
    pages_dir.mkdir(parents=True, exist_ok=True)
    for stale_page in pages_dir.glob("[0-9][0-9][0-9][0-9].md"):
        stale_page.unlink()
    for stale_dir in pages_dir.glob("[0-9][0-9][0-9][0-9]"):
        if stale_dir.is_dir():
            shutil.rmtree(stale_dir)

    index_lines = [
        "# LLMS-EMP Phase-II final 60 组 NL + PlantUML STM0 + FCSTM STM0",
        "",
        "从 `0000` 到 `0059` 逐行点击“3-in-one Markdown”，即可在同一 GitHub 页面完整查看 NL、作者 Phase-II 最终 PlantUML 和转换后 FCSTM。每组目录同时提供 `nl.txt`、`plantuml.puml`、`fcstm.fcstm` 三个原始文件。",
        "",
        "`structure_preserved` 只表示 R4.5 结构保真，不表示行为等价；执行与 Discover 资格仍以每页记录为准。",
        "",
        "| case | LLM | 模型/场景 | 3-in-one Markdown | 原始 NL | 原始 PlantUML | 原始 FCSTM | 结构 | 执行 | Discover |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for index, source_row in enumerate(source_rows):
        pair_id = source_row["pair_id"]
        case_id = pair_id[-4:]
        comparison = comparison_rows[case_id]
        case_report = json.loads(
            (EVIDENCE_DIR / "case_reports" / f"{pair_id}.json").read_text(
                encoding="utf-8"
            )
        )
        detailed = case_report["comparison"]
        official_identity = case_report["official_identity_reconciliation"]
        nl_text = source_row["nl_text"]
        source_text = source_row["stm0_text"]
        fcstm_path = EVIDENCE_DIR / "fcstm" / f"{pair_id}.fcstm"
        fcstm_text = fcstm_path.read_text(encoding="utf-8")
        nl_sha256 = _sha256_text(nl_text)
        source_sha256 = _sha256_text(source_text)
        fcstm_sha256 = _sha256_text(fcstm_text)
        if nl_sha256 != source_row["nl_sha256"]:
            raise RuntimeError(f"NL hash drift for {case_id}")
        if source_sha256 != source_row["stm0_sha256"]:
            raise RuntimeError(f"source hash drift for {case_id}")
        if source_sha256 != comparison["source_sha256"]:
            raise RuntimeError(f"comparison source hash drift for {case_id}")
        if fcstm_sha256 != comparison["fcstm_sha256"]:
            raise RuntimeError(f"FCSTM hash drift for {case_id}")

        case_dir = pages_dir / case_id
        case_dir.mkdir()
        (case_dir / "nl.txt").write_text(nl_text, encoding="utf-8")
        (case_dir / "plantuml.puml").write_text(source_text, encoding="utf-8")
        (case_dir / "fcstm.fcstm").write_text(fcstm_text, encoding="utf-8")

        navigation = []
        if index > 0:
            navigation.append(
                f"[上一组 `{index - 1:04d}`](../{index - 1:04d}/README.md)"
            )
        navigation.append("[返回 60 组索引](../../PAIR_INDEX.md)")
        if index + 1 < len(source_rows):
            navigation.append(
                f"[下一组 `{index + 1:04d}`](../{index + 1:04d}/README.md)"
            )
        page_lines = [
            f"# Pair `{case_id}`：NL + PlantUML STM0 + FCSTM STM0",
            "",
            " | ".join(navigation),
            "",
            f"- LLM：`{source_row.get('llm') or '-'}`",
            f"- 模型/场景：{_table_text(source_row.get('model_name'))}",
            f"- 作者输出阶段：`{source_row['selected_stage_column']}`",
            f"- 作者输出单元格：`{source_row['selected_stage_cell']}`；Excel row：`{source_row['source_excel_row']}`",
            f"- Phase-I fallback：`{str(source_row['is_phase_i_fallback']).lower()}`",
            f"- 相对 Phase-I 是否变化：`{str(source_row['phase_i_changed']).lower()}`",
            f"- Phase-I PlantUML SHA-256：`{source_row['phase_i_stm0_sha256']}`",
            f"- NL SHA-256：`{nl_sha256}`",
            f"- PlantUML SHA-256：`{source_sha256}`",
            f"- FCSTM SHA-256：`{fcstm_sha256}`",
            f"- 结构裁决：`{comparison['verdict']}`",
            f"- source states / transitions：`{comparison['source_state_count']}` / `{comparison['source_transition_count']}`",
            f"- mapped / blocked / silent drop：`{comparison['mapped_transition_count']}` / `{comparison['blocked_transition_count']}` / `{comparison['silently_dropped_transition_count']}`",
            f"- final / lifecycle / body coverage：`{comparison['final_transition_coverage']}` / `{comparison['lifecycle_action_coverage']}` / `{comparison['body_line_coverage']}`",
            f"- concurrent region / separator coverage：`{comparison['concurrent_region_coverage']}` / `{comparison['concurrent_region_separator_coverage']}`",
            f"- source normalization coverage：`{comparison['source_normalization_coverage']}`",
            f"- official raw / validation：`{comparison['official_raw_status']}` / `{comparison['official_validation_status']}`",
            f"- official identity states / transitions：`{comparison['official_identity_state_count']}` / `{comparison['official_identity_transition_count']}`",
            f"- official identity remaps：state `{comparison['official_identity_state_remap_count']}` / transition endpoint `{comparison['official_identity_transition_remap_count']}`",
            f"- AST audit：`{comparison['ast_audit_status']}`",
            f"- FCSTM execution eligible：`{str(comparison['fcstm_execution_eligible']).lower()}`",
            f"- Discover eligible：`{str(comparison['discover_eligible']).lower()}`",
            f"- 主 session 对读：{manual_notes[case_id]}",
            "- 三个原始文件："
            "[NL](./nl.txt) | [PlantUML](./plantuml.puml) | [FCSTM](./fcstm.fcstm)",
            "- 审计入口："
            f"[canonical](../../canonical/{pair_id}.json) | "
            f"[冻结 FCSTM](../../fcstm/{pair_id}.fcstm) | "
            f"[case report](../../case_reports/{pair_id}.json) | "
            "[人工总账](../../MANUAL_REVIEW.md)",
            "",
            "## 作者阶段 lineage",
            "",
            *_stage_lineage_lines(source_row),
            "",
            "## Official identity ledger",
            "",
            *_official_identity_lines(official_identity),
            "",
            "## Source normalization ledger",
            "",
            *_normalization_lines(detailed),
            "",
            "## Concurrent region ledger",
            "",
            *_concurrent_region_lines(detailed),
            "",
            "## Operational debt",
            "",
            *_debt_lines(detailed),
            "",
            "## NL",
            "",
            _fence("text", _display_text(nl_text)),
            "",
            "## 作者 Phase-II 最终 PlantUML STM0",
            "",
            _fence("plantuml", source_text),
            "",
            "## 转换后 FCSTM STM0",
            "",
            _fence("fcstm", fcstm_text),
            "",
            " | ".join(navigation),
            "",
        ]
        (case_dir / "README.md").write_text(
            "\n".join(page_lines), encoding="utf-8"
        )
        index_lines.append(
            "| `{case}` | `{llm}` | {model} | [查看三元组](./pairs/{case}/README.md) | "
            "[nl.txt](./pairs/{case}/nl.txt) | [plantuml.puml](./pairs/{case}/plantuml.puml) | "
            "[fcstm.fcstm](./pairs/{case}/fcstm.fcstm) | `{verdict}` | `{execution}` | `{discover}` |".format(
                case=case_id,
                llm=_table_text(source_row.get("llm")),
                model=_table_text(source_row.get("model_name")),
                verdict=comparison["verdict"],
                execution=str(comparison["fcstm_execution_eligible"]).lower(),
                discover=str(comparison["discover_eligible"]).lower(),
            )
        )

    (EVIDENCE_DIR / "PAIR_INDEX.md").write_text(
        "\n".join(index_lines) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    build_pair_pages()
