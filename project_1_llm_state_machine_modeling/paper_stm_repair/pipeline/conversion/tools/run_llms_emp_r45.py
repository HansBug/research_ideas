#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "project_1_llm_state_machine_modeling").is_dir():
            return parent
    raise RuntimeError("repository root not found")


REPO_ROOT = _repo_root()
CONVERSION_SRC = (
    REPO_ROOT
    / "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/conversion/src"
)
REPRESENTATION_SRC = (
    REPO_ROOT
    / "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation/src"
)
PYFCSTM_SRC = REPO_ROOT / "pyfcstm"
for source_root in (CONVERSION_SRC, REPRESENTATION_SRC, PYFCSTM_SRC):
    sys.path.insert(0, str(source_root))

from paper_stm_repair_conversion.adapters.plantuml_source import (  # noqa: E402
    PLANTUML_SHA256,
    PLANTUML_VERSION,
    parse_plantuml_source,
    resolve_plantuml_jar,
)
from paper_stm_repair_representation.plantuml_source_lowering import (  # noqa: E402
    lower_plantuml_source,
)
from paper_stm_repair_representation.plantuml_source_audit import (  # noqa: E402
    audit_lowered_artifact,
)


PAPER_ROOT = REPO_ROOT / "project_1_llm_state_machine_modeling/paper_stm_repair"
DEFAULT_PAIRS = (
    PAPER_ROOT
    / "corpora/seed_library/llms-emp-stm-subset/assets/extracted"
    / "feedback_final_pairs.jsonl"
)
DEFAULT_OUTPUT = PAPER_ROOT / "pipeline/representation/reports/llms_emp_r45_java_60"


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_text(text: str) -> str:
    return _sha256_bytes(text.encode("utf-8"))


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _git(*args: str, cwd: Path = REPO_ROOT) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, text=True, capture_output=True, check=True
    ).stdout.strip()


def _checked_out_pyfcstm_commit() -> str:
    expected_row = _git("ls-tree", "HEAD", "pyfcstm").split()
    if len(expected_row) < 3 or expected_row[1] != "commit":
        raise RuntimeError("pyfcstm gitlink is missing from the research repository")
    expected_commit = expected_row[2]
    required_source = PYFCSTM_SRC / "pyfcstm/model/load.py"
    if not required_source.is_file():
        raise RuntimeError(
            "pyfcstm submodule is not initialized; run "
            "`git submodule update --init --recursive pyfcstm`"
        )
    actual_root = Path(
        _git("rev-parse", "--show-toplevel", cwd=PYFCSTM_SRC)
    ).resolve()
    if actual_root != PYFCSTM_SRC.resolve():
        raise RuntimeError(
            "pyfcstm path resolved to the parent repository instead of a submodule checkout"
        )
    actual_commit = _git("rev-parse", "HEAD", cwd=PYFCSTM_SRC)
    if actual_commit != expected_commit:
        raise RuntimeError(
            f"pyfcstm checkout {actual_commit} does not match gitlink {expected_commit}"
        )
    return actual_commit


def _display(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT))


def _prepare_output_dir(output_dir: Path) -> None:
    manual_review = output_dir / "MANUAL_REVIEW.md"
    if manual_review.is_file():
        raise RuntimeError(
            f"reviewed output is frozen by {manual_review}; use --output-dir "
            "with a fresh replay directory instead of deleting manual evidence"
        )
    if output_dir.exists():
        shutil.rmtree(output_dir)
    for name in ("canonical", "fcstm", "case_reports", "parse_inspect"):
        (output_dir / name).mkdir(parents=True, exist_ok=True)


def _summary_markdown(manifest: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    summary = manifest["summary"]
    lines = [
        "# LLMS-EMP Phase-II final 60 例 Java PlantUML -> FCSTM R4.5 复验",
        "",
        "## 结论",
        "",
        f"- Java source frontend：`{summary['source_parse_ok']}/60`。",
        f"- raw PlantUML 官方直接接受：`{summary['official_raw_state_diagram']}/60`；其余 `{summary['official_raw_not_state_diagram']}` 条含非官方扩展/伪语法。",
        f"- Java official-validation normalization 后 `StateDiagram`：`{summary['official_validation_state_diagram']}/60`。",
        f"- pinned PlantUML internal identity oracle：官方 behavior links `{summary['official_validation_links']}`，source transitions `{summary['source_transitions']}`，差值 `{summary['official_validation_link_delta']:+d}`；note/presentation attachment 在 identity reconciliation 前过滤。",
        f"- source transition：`{summary['source_transitions']}`；FCSTM macro 映射 `{summary['mapped_transitions']}`，结构 blocked `{summary['blocked_transitions']}`，静默丢失 `{summary['silently_dropped_transitions']}`。",
        f"- final boundary：`{summary['final_transitions_mapped']}/{summary['final_transitions_source']}`。",
        f"- opaque state body：`{summary['body_lines_mapped']}/{summary['body_lines_source']}`；均保存在 FCSTM display metadata 与 trace，不解释为 timing/guard/action。",
        f"- lifecycle action：`{summary['lifecycle_actions_mapped']}/{summary['lifecycle_actions_source']}` 结构保存；state-owned action 以 abstract hook 保留，ownerless action 仅保存在 metadata/trace，二者都不冒充已注册行为。",
        f"- PlantUML concurrent region：`{summary['concurrent_regions_mapped']}/{summary['concurrent_regions_source']}`；region separator：`{summary['concurrent_region_separators_mapped']}/{summary['concurrent_region_separators_source']}`，仅保留结构与顺序，不声称 FCSTM 已实现正交并发执行。",
        f"- 作者 workbook transport normalization：`{summary['source_normalizations_mapped']}/{summary['source_normalizations_source']}`；raw source、normalized source、规则与逐行 before/after 均进入 ledger。",
        f"- FCSTM parse/inspect：`{summary['fcstm_parse_ok']}/60` / `{summary['fcstm_inspect_ok']}/60`。",
        f"- pyfcstm AST 独立反查：`{summary['ast_audit_ok']}/60`。",
        f"- pinned PlantUML qualified identity：states `{summary['official_identity_states_aligned']}/{summary['source_states']}`；transition endpoints `{summary['official_identity_transitions_aligned']}/{summary['source_transitions']}`；state remap `{summary['official_identity_state_remaps']}`；endpoint remap `{summary['official_identity_transition_remaps']}`。",
        f"- R4.5 structural preservation：`{summary['structure_preserved']}/60`；structure blocked：`{summary['structure_blocked']}/60`。",
        f"- FCSTM execution eligible：`{summary['fcstm_execution_eligible']}/60`；Discover eligible：`{summary['discover_eligible']}/60`。",
        "",
        "结构通过不等于行为等价。无/多/非法 initial、ownerless lifecycle、opaque state body、无标签 fan-out 与显式 fork 进入 `operational_debts`；转换器保留这些 source facts，但不推断 guard/effect/timing/concurrency。",
        "",
        "60 例逐例人工/LLM 对读、官方源码逆向结论与真实 PlantUML/FCSTM 例子见 [Issue #161 技术报告](../../../../reports/2026-07-19-issue-161-plantuml-java-frontend.md)。",
        "",
        "## 代表性样例",
        "",
        "| case | structural verdict | states | transitions | mapped | blocked | final | lifecycle | raw official | normalized official |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    selected = {"0000", "0022", "0053", "0054", "0058"}
    for row in rows:
        if row["case_id"] not in selected:
            continue
        lines.append(
            "| `{case_id}` | `{verdict}` | {source_state_count} | {source_transition_count} | "
            "{mapped_transition_count} | {blocked_transition_count} | {final_transition_coverage} | "
            "{lifecycle_action_coverage} | `{official_raw_status}` | `{official_validation_status}` |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## 机器证据入口",
            "",
            "- `manifest.json`：版本、哈希、总计与 eligibility 口径。",
            "- `comparison.jsonl`：60 例逐项摘要。",
            "- `canonical/*.json`：Java source canonical + 官方 internal model 快照。",
            "- `fcstm/*.fcstm`：60 个新 FCSTM STM0。",
            "- `case_reports/*.json`：逐迁移 mapping、operational debt、name map 与 AST audit。",
            "- `parse_inspect/*.json`：pyfcstm 结构化 inspect 输出。",
            "",
        ]
    )
    return "\n".join(lines)


def _manual_review_template(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Phase-II final 60 组人工/LLM 对读模板",
        "",
        "每行必须在完整阅读 NL、作者最终 PlantUML、转换后 FCSTM、normalization/region ledger 后，将 `PENDING` 改为 `PASS`，并填写本组特有的保真判断。结构保真不等于行为等价。",
        "",
        "| case | source SHA-256 | FCSTM SHA-256 | verdict | notes |",
        "|---|---|---|---|---|",
    ]
    lines.extend(
        f"| `{row['case_id']}` | `{row['source_sha256']}` | "
        f"`{row['fcstm_sha256']}` | PENDING | 待逐组对读 |"
        for row in rows
    )
    lines.append("")
    return "\n".join(lines)


def run(*, pairs_path: Path, output_dir: Path, plantuml_jar: Path) -> dict[str, Any]:
    pyfcstm_commit = _checked_out_pyfcstm_commit()
    from pyfcstm.diagnostics.inspect import inspect_model
    from pyfcstm.model.load import load_state_machine_from_text

    research_commit = _git("rev-parse", "HEAD")
    research_branch = _git("branch", "--show-current")
    tracked_dirty_before_run = bool(
        _git("status", "--porcelain", "--untracked-files=no")
    )
    output_dir = output_dir.resolve()
    allowed_root = (PAPER_ROOT / "pipeline/representation/reports").resolve()
    if output_dir != allowed_root and allowed_root not in output_dir.parents:
        raise ValueError(f"output must stay under {allowed_root}: {output_dir}")
    _prepare_output_dir(output_dir)

    rows = [
        json.loads(line)
        for line in pairs_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(rows) != 60:
        raise RuntimeError(f"expected 60 LLMS-EMP pairs, got {len(rows)}")

    comparison_rows: list[dict[str, Any]] = []
    official_rows: list[dict[str, Any]] = []
    verdicts: Counter[str] = Counter()
    blocker_reasons: Counter[str] = Counter()
    debt_reasons: Counter[str] = Counter()
    totals: Counter[str] = Counter()
    for index, row in enumerate(rows):
        pair_id = row["pair_id"]
        case_id = pair_id[-4:]
        canonical = parse_plantuml_source(
            row["stm0_text"],
            example_id=pair_id,
            source_name=f"{pair_id}.puml",
            plantuml_jar=plantuml_jar,
        )
        if canonical["metadata"]["source_sha256"] != row["stm0_sha256"]:
            raise RuntimeError(f"Java canonical raw source hash drift for {pair_id}")
        if canonical["status"] != "converted":
            raise RuntimeError(
                f"Java source frontend is not complete for {pair_id}: "
                f"{canonical['metadata']['unparsed_semantic_lines']}"
            )
        lowered = lower_plantuml_source(canonical)
        model = load_state_machine_from_text(lowered["fcstm"])
        inspect_report = inspect_model(model).to_json()
        ast_audit = audit_lowered_artifact(
            canonical=canonical,
            fcstm=lowered["fcstm"],
            comparison=lowered["comparison"],
            model=model,
            inspect_report=inspect_report,
        )

        canonical_path = output_dir / "canonical" / f"{pair_id}.json"
        fcstm_path = output_dir / "fcstm" / f"{pair_id}.fcstm"
        case_report_path = output_dir / "case_reports" / f"{pair_id}.json"
        inspect_path = output_dir / "parse_inspect" / f"{pair_id}.json"
        _write_json(canonical_path, canonical)
        fcstm_path.write_text(lowered["fcstm"], encoding="utf-8")
        _write_json(inspect_path, inspect_report)

        comparison = lowered["comparison"]
        diagnostics = inspect_report.get("diagnostics", [])
        severity_counts = Counter(item.get("severity", "unknown") for item in diagnostics)
        official_raw = canonical["metadata"]["official_model"]
        official_validation = canonical["metadata"]["official_validation"]
        official_identity = canonical["metadata"]["official_identity_reconciliation"]
        if official_identity["status"] != "aligned":
            raise RuntimeError(
                f"official identity reconciliation is not aligned for {pair_id}: "
                f"{official_identity}"
            )
        case_report = {
            "schema_version": "r4_5.llms_emp_java_case_report.v3",
            "pair_index": index,
            "pair_id": pair_id,
            "case_id": case_id,
            "llm": row.get("llm"),
            "model_name": row.get("model_name"),
            "selected_stage": row.get("selected_stage"),
            "selected_stage_cell": row.get("selected_stage_cell"),
            "source_excel_row": row.get("source_excel_row"),
            "is_phase_i_fallback": row.get("is_phase_i_fallback"),
            "phase_i_changed": row.get("phase_i_changed"),
            "stage_lineage": row.get("stage_lineage", []),
            "source_sha256": row["stm0_sha256"],
            "canonical_sha256": _sha256_text(
                json.dumps(canonical, ensure_ascii=False, sort_keys=True)
            ),
            "fcstm_sha256": _sha256_text(lowered["fcstm"]),
            "canonical_path": _display(canonical_path),
            "fcstm_path": _display(fcstm_path),
            "parse_inspect_path": _display(inspect_path),
            "comparison": comparison,
            "ast_audit": ast_audit,
            "name_mapping": lowered["name_mapping"],
            "inspect_metrics": inspect_report.get("metrics", {}),
            "inspect_diagnostic_severities": dict(severity_counts),
            "official_raw_status": official_raw["status"],
            "official_validation_status": official_validation["model"]["status"],
            "official_validation_source_input_normalizations": official_validation[
                "source_input_normalizations"
            ],
            "official_validation_normalizations": official_validation["normalizations"],
            "official_identity_reconciliation": official_identity,
        }
        _write_json(case_report_path, case_report)

        summary_row = {
            "pair_index": index,
            "pair_id": pair_id,
            "case_id": case_id,
            "llm": row.get("llm"),
            "model_name": row.get("model_name"),
            "selected_stage": row.get("selected_stage"),
            "selected_stage_cell": row.get("selected_stage_cell"),
            "source_excel_row": row.get("source_excel_row"),
            "is_phase_i_fallback": row.get("is_phase_i_fallback"),
            "phase_i_changed": row.get("phase_i_changed"),
            "source_sha256": row["stm0_sha256"],
            "canonical_sha256": case_report["canonical_sha256"],
            "fcstm_sha256": case_report["fcstm_sha256"],
            "verdict": comparison["verdict"],
            "discover_eligible": comparison["discover_eligible"],
            "fcstm_execution_eligible": comparison["fcstm_execution_eligible"],
            "operational_status": comparison["operational_status"],
            "source_state_count": comparison["source_state_count"],
            "source_transition_count": comparison["source_transition_count"],
            "mapped_transition_count": comparison["mapped_transition_count"],
            "blocked_transition_count": comparison["blocked_transition_count"],
            "silently_dropped_transition_count": comparison[
                "silently_dropped_transition_count"
            ],
            "final_transition_coverage": comparison["final_transition_coverage"],
            "lifecycle_action_coverage": comparison["lifecycle_action_coverage"],
            "body_line_coverage": comparison["body_line_coverage"],
            "concurrent_region_coverage": comparison["concurrent_region_coverage"],
            "concurrent_region_separator_coverage": comparison[
                "concurrent_region_separator_coverage"
            ],
            "source_normalization_coverage": comparison[
                "source_normalization_coverage"
            ],
            "ast_audit_status": ast_audit["status"],
            "official_raw_status": official_raw["status"],
            "official_validation_status": official_validation["model"]["status"],
            "official_validation_link_count": official_validation["model"].get("counts", {}).get("links", 0),
            "official_validation_link_delta": official_validation["model"].get("counts", {}).get("links", 0)
            - comparison["source_transition_count"],
            "official_identity_status": official_identity["status"],
            "official_identity_state_count": official_identity["official_state_count"],
            "official_identity_transition_count": official_identity[
                "transition_identity_alignment_count"
            ],
            "official_identity_state_remap_count": len(
                official_identity["state_identity_remaps"]
            ),
            "official_identity_transition_remap_count": len(
                official_identity["transition_endpoint_remaps"]
            ),
            "parse_status": "ok",
            "inspect_status": "ok",
            "inspect_error_count": severity_counts.get("error", 0),
            "case_report_path": _display(case_report_path),
        }
        comparison_rows.append(summary_row)
        official_rows.append(
            {
                "pair_id": pair_id,
                "raw": official_raw,
                "validation": official_validation,
            }
        )
        verdicts[comparison["verdict"]] += 1
        for blocker in comparison["blockers"]:
            blocker_reasons[blocker["reason_code"]] += 1
        for debt in comparison["operational_debts"]:
            debt_reasons[debt["reason_code"]] += 1
        totals["source_states"] += comparison["source_state_count"]
        totals["source_transitions"] += comparison["source_transition_count"]
        totals["mapped_transitions"] += comparison["mapped_transition_count"]
        totals["blocked_transitions"] += comparison["blocked_transition_count"]
        totals["silent_drops"] += comparison["silently_dropped_transition_count"]
        body_mapped, body_source = map(int, comparison["body_line_coverage"].split("/"))
        totals["body_lines_mapped"] += body_mapped
        totals["body_lines_source"] += body_source
        lifecycle_mapped, lifecycle_source = map(
            int, comparison["lifecycle_action_coverage"].split("/")
        )
        totals["lifecycle_actions_mapped"] += lifecycle_mapped
        totals["lifecycle_actions_source"] += lifecycle_source
        final_mapped, final_source = map(int, comparison["final_transition_coverage"].split("/"))
        totals["final_transitions_mapped"] += final_mapped
        totals["final_transitions_source"] += final_source
        regions_mapped, regions_source = map(
            int, comparison["concurrent_region_coverage"].split("/")
        )
        totals["concurrent_regions_mapped"] += regions_mapped
        totals["concurrent_regions_source"] += regions_source
        separators_mapped, separators_source = map(
            int, comparison["concurrent_region_separator_coverage"].split("/")
        )
        totals["concurrent_region_separators_mapped"] += separators_mapped
        totals["concurrent_region_separators_source"] += separators_source
        normalizations_mapped, normalizations_source = map(
            int, comparison["source_normalization_coverage"].split("/")
        )
        totals["source_normalizations_mapped"] += normalizations_mapped
        totals["source_normalizations_source"] += normalizations_source
        totals["parse_ok"] += 1
        totals["inspect_ok"] += severity_counts.get("error", 0) == 0
        totals["ast_audit_ok"] += ast_audit["status"] == "passed"
        totals["fcstm_execution_eligible"] += comparison["fcstm_execution_eligible"]
        totals["discover_eligible"] += comparison["discover_eligible"]
        totals["official_raw_state"] += official_raw["status"] == "state_diagram"
        totals["official_validation_state"] += (
            official_validation["model"]["status"] == "state_diagram"
        )
        totals["official_validation_links"] += official_validation["model"].get("counts", {}).get("links", 0)
        totals["official_identity_states"] += official_identity["official_state_count"]
        totals["official_identity_transitions"] += official_identity[
            "transition_identity_alignment_count"
        ]
        totals["official_identity_state_remaps"] += len(
            official_identity["state_identity_remaps"]
        )
        totals["official_identity_transition_remaps"] += len(
            official_identity["transition_endpoint_remaps"]
        )

    comparison_path = output_dir / "comparison.jsonl"
    comparison_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in comparison_rows),
        encoding="utf-8",
    )
    official_path = output_dir / "official_models.jsonl"
    official_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in official_rows),
        encoding="utf-8",
    )
    manifest = {
        "schema_version": "r4_5.llms_emp_java_batch.v3",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "research_commit": research_commit,
        "research_branch": research_branch,
        "tracked_worktree_dirty_before_run": tracked_dirty_before_run,
        "pyfcstm_commit": pyfcstm_commit,
        "plantuml_version": PLANTUML_VERSION,
        "plantuml_jar_sha256": PLANTUML_SHA256,
        "pairs_path": _display(pairs_path),
        "pairs_sha256": _sha256_bytes(pairs_path.read_bytes()),
        "output_dir": _display(output_dir),
        "attribution": "representation_conversion_not_repair",
        "r4_5_boundary": "preserve source structure, boundaries, labels, and lifecycle; do not infer guard/effect/timing/concurrency",
        "summary": {
            "examples": 60,
            "source_parse_ok": 60,
            "official_raw_state_diagram": totals["official_raw_state"],
            "official_raw_not_state_diagram": 60 - totals["official_raw_state"],
            "official_validation_state_diagram": totals["official_validation_state"],
            "official_validation_links": totals["official_validation_links"],
            "official_validation_link_delta": (
                totals["official_validation_links"] - totals["source_transitions"]
            ),
            "source_states": totals["source_states"],
            "official_identity_states_aligned": totals["official_identity_states"],
            "official_identity_transitions_aligned": totals[
                "official_identity_transitions"
            ],
            "official_identity_state_remaps": totals[
                "official_identity_state_remaps"
            ],
            "official_identity_transition_remaps": totals[
                "official_identity_transition_remaps"
            ],
            "source_transitions": totals["source_transitions"],
            "mapped_transitions": totals["mapped_transitions"],
            "blocked_transitions": totals["blocked_transitions"],
            "silently_dropped_transitions": totals["silent_drops"],
            "body_lines_source": totals["body_lines_source"],
            "body_lines_mapped": totals["body_lines_mapped"],
            "lifecycle_actions_source": totals["lifecycle_actions_source"],
            "lifecycle_actions_mapped": totals["lifecycle_actions_mapped"],
            "final_transitions_source": totals["final_transitions_source"],
            "final_transitions_mapped": totals["final_transitions_mapped"],
            "concurrent_regions_source": totals["concurrent_regions_source"],
            "concurrent_regions_mapped": totals["concurrent_regions_mapped"],
            "concurrent_region_separators_source": totals[
                "concurrent_region_separators_source"
            ],
            "concurrent_region_separators_mapped": totals[
                "concurrent_region_separators_mapped"
            ],
            "source_normalizations_source": totals["source_normalizations_source"],
            "source_normalizations_mapped": totals["source_normalizations_mapped"],
            "fcstm_parse_ok": totals["parse_ok"],
            "fcstm_inspect_ok": totals["inspect_ok"],
            "ast_audit_ok": totals["ast_audit_ok"],
            "structure_preserved": verdicts["structure_preserved"],
            "structure_blocked": verdicts["structure_blocked"],
            "fcstm_execution_eligible": totals["fcstm_execution_eligible"],
            "discover_eligible": totals["discover_eligible"],
            "blocker_reasons": dict(blocker_reasons),
            "operational_debt_reasons": dict(debt_reasons),
        },
    }
    _write_json(output_dir / "manifest.json", manifest)
    (output_dir / "SUMMARY.md").write_text(
        _summary_markdown(manifest, comparison_rows), encoding="utf-8"
    )
    (output_dir / "MANUAL_REVIEW_TEMPLATE.md").write_text(
        _manual_review_template(comparison_rows), encoding="utf-8"
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pairs", type=Path, default=DEFAULT_PAIRS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--plantuml-jar", type=Path)
    args = parser.parse_args()
    jar = resolve_plantuml_jar(args.plantuml_jar)
    manifest = run(
        pairs_path=args.pairs.resolve(),
        output_dir=args.output_dir,
        plantuml_jar=jar,
    )
    print(json.dumps(manifest["summary"], ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
