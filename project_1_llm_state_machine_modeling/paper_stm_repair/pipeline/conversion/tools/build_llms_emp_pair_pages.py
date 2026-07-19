#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shutil
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
    / "corpora/seed_library/llms-emp-stm-subset/assets/extracted/pairs.jsonl"
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
        "# LLMS-EMP 60 组 NL + PlantUML STM0 + FCSTM STM0",
        "",
        "从 `0000` 到 `0059` 逐行点击“3-in-one Markdown”，即可在同一 GitHub 页面完整查看 NL、原装 PlantUML STM0 和转换后 FCSTM STM0。每组目录同时提供 `nl.txt`、`plantuml.puml`、`fcstm.fcstm` 三个原始文件。",
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
            f"- NL SHA-256：`{nl_sha256}`",
            f"- PlantUML SHA-256：`{source_sha256}`",
            f"- FCSTM SHA-256：`{fcstm_sha256}`",
            f"- 结构裁决：`{comparison['verdict']}`",
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
            "## NL",
            "",
            _fence("text", _display_text(nl_text)),
            "",
            "## 原装 PlantUML STM0",
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
