from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from ..adapters.scxml import ScxmlOptions, convert_scxml
from ..report import repo_commit, sha256_file, sha256_text, write_json
from ..toolchain import ToolPreflight, ToolchainSetupError, run_plantuml_on_candidate
from .plantuml import NormalizationResult, classify_plantuml_issue, normalize_plantuml
from .semantic_audit import audit_plantuml_semantic_preservation

RECOVERY_REPORT_VERSION = "r3.1.plantuml_recovery_report.v0"
NORMALIZATION_LEDGER_VERSION = "r3.1.normalization_ledger.v0"

DEFAULT_PAIR_SOURCES = [
    Path("project_1_llm_state_machine_modeling/paper_stm_repair/corpora/seed_library/llms-emp-stm-subset/assets/extracted/pairs.jsonl"),
    Path("project_1_llm_state_machine_modeling/paper_stm_repair/corpora/seed_library/unified-uml-multimodal-validation/assets/extracted/pairs.jsonl"),
]


@dataclass(frozen=True)
class PlantumlPair:
    seed_id: str
    pair_id: str
    row_index: int
    nl_sha256: str
    stm0_sha256: str
    stm0_text: str
    nl_text: str | None
    llm: str | None
    generation_model_or_method: str | None
    source_pairs_path: Path
    source_locator: str | None
    source_line_sha256: str
    source_file_sha256: str


def _rel(path: Path | None, repo_root: Path) -> str | None:
    if path is None:
        return None
    path = path.resolve()
    repo = repo_root.resolve()
    try:
        return str(path.relative_to(repo))
    except ValueError:
        parts = list(path.parts)
        if "runs" in parts:
            idx = parts.index("runs")
            return str(Path(*parts[idx:]))
        if "reports" in parts:
            idx = parts.index("reports")
            return str(Path(*parts[idx:]))
        if "tmp" in parts:
            return f"external-run-artifact/{path.name}"
        return f"external-local-artifact/{path.name}"


def _tail(text: str, limit: int = 1200) -> str:
    text = text.strip()
    return text[-limit:] if len(text) > limit else text


def _is_plantuml_record(record: dict[str, Any]) -> bool:
    if record.get("stm_format") == "plantuml":
        return True
    return str(record.get("stm0_text", "")).lstrip().startswith("@startuml")


def load_plantuml_pairs(repo_root: Path, pair_sources: Iterable[Path] | None = None, *, limit: int | None = None) -> list[PlantumlPair]:
    pairs: list[PlantumlPair] = []
    for source in pair_sources or DEFAULT_PAIR_SOURCES:
        source_path = source if source.is_absolute() else repo_root / source
        if not source_path.exists():
            continue
        source_text = source_path.read_text(encoding="utf-8")
        source_file_sha = sha256_file(source_path)
        for row_index, line in enumerate(source_text.splitlines()):
            if not line.strip():
                continue
            record = json.loads(line)
            if not _is_plantuml_record(record):
                continue
            pairs.append(
                PlantumlPair(
                    seed_id=record.get("seed_id") or source_path.parents[2].name,
                    pair_id=record.get("pair_id") or f"{source_path.stem}_{row_index:04d}",
                    row_index=row_index,
                    nl_sha256=record.get("nl_sha256") or sha256_text(record.get("nl_text", "")),
                    stm0_sha256=record.get("stm0_sha256") or sha256_text(record.get("stm0_text", "")),
                    stm0_text=record.get("stm0_text", ""),
                    nl_text=record.get("nl_text"),
                    llm=record.get("llm"),
                    generation_model_or_method=record.get("generation_model_or_method"),
                    source_pairs_path=source_path,
                    source_locator=record.get("source_locator"),
                    source_line_sha256=sha256_text(line),
                    source_file_sha256=source_file_sha,
                )
            )
            if limit is not None and len(pairs) >= limit:
                return pairs
    return pairs


def selected_example_pairs(repo_root: Path) -> set[str]:
    selected_dir = repo_root / "project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples"
    out: set[str] = set()
    for meta_path in selected_dir.glob("*/source_meta.json"):
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if meta.get("stm_format") == "plantuml" and meta.get("pair_id"):
            out.add(meta["pair_id"])
    return out


def _source_line_sha256(path: Path, row_index: int) -> str | None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return None
    if row_index < 0 or row_index >= len(lines):
        return None
    return sha256_text(lines[row_index])


def _source_file_immutability(repo_root: Path, paths: Iterable[Path], before: dict[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted({p.resolve() for p in paths}, key=str):
        after = sha256_file(path) if path.exists() else None
        before_sha = before.get(str(path))
        rows.append({
            "source_pairs_path": _rel(path, repo_root),
            "source_file_sha256_before": before_sha,
            "source_file_sha256_after": after,
            "source_file_unchanged": before_sha == after,
        })
    return rows


def _git_status_porcelain(repo_root: Path) -> list[str]:
    try:
        out = subprocess.check_output(["git", "status", "--porcelain"], cwd=repo_root, text=True)
    except Exception:
        return ["<git-status-unavailable>"]
    return [line for line in out.splitlines() if line.strip()]


def _canonical_parse_pass(canonical: dict[str, Any] | None) -> bool:
    if not canonical:
        return False
    model = canonical.get("model", {})
    return bool(
        canonical.get("status") == "converted"
        and model.get("states")
        and model.get("transitions")
    )


def _seed_class(seed_id: str) -> str:
    if seed_id == "llms-emp-stm-subset":
        return "llms_emp_cross_llm"
    if seed_id == "unified-uml-multimodal-validation":
        return "unified_synthetic"
    return "other"


def _safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)[:96]


def _sanitize_rel_string(value: str | None, repo_root: Path) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        return value
    try:
        return _rel(Path(value), repo_root) if value.startswith("/") else value
    except Exception:
        return value


def _run_member(path: Path | str | None, repo_root: Path, run_dir: Path) -> str | None:
    if path is None:
        return None
    p = Path(path)
    if not p.is_absolute():
        p = repo_root / p
    try:
        return str(p.resolve().relative_to(run_dir.resolve()))
    except ValueError:
        return _rel(p, repo_root)


def _sanitize_run_or_repo_rel_string(value: str | None, repo_root: Path, run_dir: Path) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        return value
    try:
        return _run_member(Path(value), repo_root, run_dir)
    except Exception:
        return value


def _preflight_summary(preflight: ToolPreflight | None, repo_root: Path, run_dir: Path) -> dict[str, Any] | None:
    if preflight is None:
        return None
    meta = preflight.to_metadata()
    version = meta.get("tool_version")
    if isinstance(version, str):
        version = version.splitlines()[0] if version.splitlines() else version
    evidence = meta.get("evidence") or {}
    return {
        "tool_name": meta.get("tool_name"),
        "tool_version_head": version,
        "tool_source_url": meta.get("tool_source_url"),
        "tool_invocation_status": meta.get("tool_invocation_status"),
        "syntax_status": meta.get("syntax_status"),
        "structured_export_status": meta.get("structured_export_status"),
        "structured_export_format": meta.get("structured_export_format"),
        "structured_export_sha256": meta.get("structured_export_sha256"),
        "structured_export_path": _sanitize_run_or_repo_rel_string(meta.get("structured_export_path"), repo_root, run_dir),
        "command": meta.get("command"),
        "returncode": meta.get("returncode"),
        "stdout_tail": _tail(meta.get("stdout_tail") or "", 300),
        "stderr_tail": _tail(meta.get("stderr_tail") or "", 500),
        "fallback_reason": _tail(meta.get("fallback_reason") or "", 500) if meta.get("fallback_reason") else None,
        "scxml_returncode": evidence.get("scxml_returncode"),
        "no_text_fallback_policy": evidence.get("no_text_fallback_policy"),
    }


def _recovery_bucket(raw_converted: bool, normalized_converted: bool, norm: NormalizationResult) -> str:
    if raw_converted:
        return "already_converted_before_normalization"
    if not normalized_converted:
        return "failed_after_normalization"
    if norm.low_risk_candidate:
        return "low_risk_scxml_pass"
    return "high_risk_scxml_pass"


def _main_eligibility(raw_converted: bool, normalized_converted: bool, norm: NormalizationResult) -> bool:
    return (not raw_converted) and normalized_converted and norm.low_risk_candidate


def _main_eligibility_with_semantic_audit(raw_converted: bool, normalized_converted: bool, norm: NormalizationResult, semantic_audit: dict[str, Any] | None) -> bool:
    return (
        _main_eligibility(raw_converted, normalized_converted, norm)
        and semantic_audit is not None
        and bool(semantic_audit.get("pass"))
    )


def _profile(canonical: dict[str, Any] | None, norm: NormalizationResult) -> dict[str, Any]:
    if not canonical:
        return {
            "states_count": 0,
            "transitions_count": 0,
            "hierarchy_level": None,
            "transition_label_avg_chars": 0.0,
            "alias_count": len(norm.alias_declarations),
            "semantic_risk_counts": dict(Counter(c.semantic_risk for c in norm.changes)),
        }
    transitions = canonical.get("model", {}).get("transitions", [])
    labels = [t.get("label") or "" for t in transitions]
    avg = round(sum(len(x) for x in labels) / len(labels), 2) if labels else 0.0
    return {
        "states_count": len(canonical.get("model", {}).get("states", [])),
        "transitions_count": len(transitions),
        "hierarchy_level": canonical.get("model", {}).get("hierarchy_level"),
        "transition_label_avg_chars": avg,
        "alias_count": len(norm.alias_declarations),
        "semantic_risk_counts": dict(Counter(c.semantic_risk for c in norm.changes)),
    }


def _parse_scxml_canonical(preflight: ToolPreflight, *, pair: PlantumlPair, repo_root: Path) -> dict[str, Any] | None:
    path = preflight.structured_export_path
    if not path:
        return None
    scxml_path = Path(path)
    if not scxml_path.is_absolute():
        scxml_path = repo_root / scxml_path
    result = convert_scxml(
        scxml_path,
        example_id=pair.pair_id,
        seed_id=pair.seed_id,
        options=ScxmlOptions(
            adapter="plantuml",
            source_format="plantuml",
            conversion_source="official_scxml",
            canonical_extraction_method="PlantUML normalized candidate -tscxml export parsed by xml.etree.ElementTree",
            status_on_success="converted",
            fallback_used=False,
            fallback_scope=None,
            timing_level="none",
            source_language="PlantUML state diagram",
        ),
        structured_export_relpath=path,
        structured_export_sha256=preflight.structured_export_sha256,
    )
    if result.status == "blocked":
        return None
    return result.to_canonical_dict()


def run_recovery(
    *,
    repo_root: Path,
    reports_dir: Path,
    run_dir: Path,
    run_id: str,
    pair_sources: Iterable[Path] | None = None,
    limit: int | None = None,
    created_at: str | None = None,
    generation_command: str | None = None,
) -> dict[str, Any]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(parents=True, exist_ok=True)
    normalized_dir = run_dir / "normalized_candidates"
    normalized_dir.mkdir(parents=True, exist_ok=True)
    pairs = load_plantuml_pairs(repo_root, pair_sources, limit=limit)
    generator_code_commit = repo_commit(repo_root)
    generator_git_status = _git_status_porcelain(repo_root)
    source_file_sha_before = {
        str(path.resolve()): sha256_file(path)
        for path in {pair.source_pairs_path for pair in pairs}
        if path.exists()
    }
    selected_pair_ids = selected_example_pairs(repo_root)
    created = created_at or datetime.now(timezone.utc).isoformat()
    ledger_rows: list[dict[str, Any]] = []
    items: list[dict[str, Any]] = []
    raw_immutability: list[dict[str, Any]] = []

    for index, pair in enumerate(pairs):
        raw_text = pair.stm0_text if pair.stm0_text.endswith("\n") else pair.stm0_text + "\n"
        raw_sha_before = sha256_text(raw_text)
        raw_candidate = normalized_dir / f"{index:04d}__{_safe_name(pair.seed_id)}__{_safe_name(pair.pair_id)}__raw.puml"
        normalized_candidate = normalized_dir / f"{index:04d}__{_safe_name(pair.seed_id)}__{_safe_name(pair.pair_id)}__normalized.puml"
        raw_candidate.write_text(raw_text, encoding="utf-8")
        norm = normalize_plantuml(raw_text)
        normalized_candidate.write_text(norm.normalized_text, encoding="utf-8")

        raw_preflight: ToolPreflight | None = None
        normalized_preflight: ToolPreflight | None = None
        raw_setup_error: str | None = None
        normalized_setup_error: str | None = None
        try:
            raw_preflight = run_plantuml_on_candidate(
                raw_candidate,
                example_id=f"{pair.seed_id}__{pair.pair_id}__raw",
                repo_root=repo_root,
                reports_dir=run_dir,
                export_subdir="official_scxml",
                output_stem="raw",
            )
        except ToolchainSetupError as exc:
            raw_setup_error = str(exc)
            raise
        raw_ok = bool(raw_preflight and raw_preflight.syntax_status == "ok" and raw_preflight.structured_export_status == "scxml_export_ok")
        if raw_ok:
            normalized_ok = False
        else:
            try:
                normalized_preflight = run_plantuml_on_candidate(
                    normalized_candidate,
                    example_id=f"{pair.seed_id}__{pair.pair_id}__normalized",
                    repo_root=repo_root,
                    reports_dir=run_dir,
                    export_subdir="official_scxml",
                    output_stem="normalized",
                )
            except ToolchainSetupError as exc:
                normalized_setup_error = str(exc)
                raise
            normalized_ok = bool(
                normalized_preflight
                and normalized_preflight.syntax_status == "ok"
                and normalized_preflight.structured_export_status == "scxml_export_ok"
            )
        canonical = None
        raw_canonical_parse_pass = False
        normalized_canonical_parse_pass = False
        if raw_ok and raw_preflight:
            canonical = _parse_scxml_canonical(raw_preflight, pair=pair, repo_root=repo_root)
            raw_canonical_parse_pass = _canonical_parse_pass(canonical)
        elif normalized_ok and normalized_preflight:
            canonical = _parse_scxml_canonical(normalized_preflight, pair=pair, repo_root=repo_root)
            normalized_canonical_parse_pass = _canonical_parse_pass(canonical)
        raw_converted = raw_ok and raw_canonical_parse_pass
        normalized_converted = normalized_ok and normalized_canonical_parse_pass
        semantic_audit = None
        if not raw_converted and norm.changes:
            semantic_audit = audit_plantuml_semantic_preservation(
                raw_text,
                norm.normalized_text,
                introduced_alias_declarations=norm.alias_declarations,
                rule_ids=norm.rule_ids,
            )
        bucket = _recovery_bucket(raw_converted, normalized_converted, norm)
        main_included = _main_eligibility_with_semantic_audit(raw_converted, normalized_converted, norm, semantic_audit)
        issue_category = classify_plantuml_issue(raw_text, norm)
        profile = _profile(canonical, norm)
        item = {
            "seed_id": pair.seed_id,
            "seed_class": _seed_class(pair.seed_id),
            "pair_id": pair.pair_id,
            "row_index": pair.row_index,
            "source_pairs_path": _rel(pair.source_pairs_path, repo_root),
            "source_locator": pair.source_locator,
            "source_line_sha256": pair.source_line_sha256,
            "source_file_sha256": pair.source_file_sha256,
            "nl_sha256": pair.nl_sha256,
            "stm0_sha256": pair.stm0_sha256,
            "llm": pair.llm,
            "generation_model_or_method": pair.generation_model_or_method,
            "raw_candidate_path": _run_member(raw_candidate, repo_root, run_dir),
            "normalized_candidate_path": _run_member(normalized_candidate, repo_root, run_dir) if not raw_ok else None,
            "raw_sha256": norm.raw_sha256,
            "normalized_sha256": norm.normalized_sha256,
            "raw_scxml_pass": raw_ok,
            "normalized_scxml_pass": normalized_ok,
            "raw_canonical_parse_pass": raw_canonical_parse_pass,
            "normalized_canonical_parse_pass": normalized_canonical_parse_pass,
            "raw_conversion_pass": raw_converted,
            "normalized_conversion_pass": normalized_converted,
            "recovery_bucket": bucket,
            "technical_scxml_pass_all_rules": (not raw_converted) and normalized_converted,
            "low_risk_scxml_pass": (not raw_converted) and normalized_converted and norm.low_risk_candidate,
            "main_eligibility_included": main_included,
            "has_high_risk_loss": norm.has_high_risk_loss,
            "concurrency_degraded": norm.concurrency_degraded,
            "semantic_preservation_audit": semantic_audit,
            "semantic_preservation_pass": bool(semantic_audit and semantic_audit.get("pass")),
            "issue_category": issue_category,
            "rule_ids": norm.rule_ids,
            "changes_count": len(norm.changes),
            "normalization_noop": len(norm.changes) == 0,
            "no_regression_guard_pass": pair.pair_id in selected_pair_ids and raw_converted and len(norm.changes) == 0,
            "raw_preflight": _preflight_summary(raw_preflight, repo_root, run_dir),
            "normalized_preflight": _preflight_summary(normalized_preflight, repo_root, run_dir),
            "raw_setup_error": raw_setup_error,
            "normalized_setup_error": normalized_setup_error,
            "canonical_profile": profile,
            "selected_seed_example_no_regression": pair.pair_id in selected_pair_ids and raw_converted,
        }
        items.append(item)
        source_line_sha_after = _source_line_sha256(pair.source_pairs_path, pair.row_index)
        source_file_sha_after = sha256_file(pair.source_pairs_path) if pair.source_pairs_path.exists() else None
        raw_immutability.append({
            "seed_id": pair.seed_id,
            "pair_id": pair.pair_id,
            "raw_sha256_before": raw_sha_before,
            "raw_sha256_after": sha256_text(raw_text),
            "raw_text_unchanged": raw_sha_before == sha256_text(raw_text),
            "source_pairs_path": _rel(pair.source_pairs_path, repo_root),
            "source_line_sha256_before": pair.source_line_sha256,
            "source_line_sha256_after": source_line_sha_after,
            "source_line_unchanged": pair.source_line_sha256 == source_line_sha_after,
            "source_file_sha256_before": pair.source_file_sha256,
            "source_file_sha256_after": source_file_sha_after,
            "source_file_unchanged": pair.source_file_sha256 == source_file_sha_after,
        })
        for seq, change in enumerate(norm.changes, start=1):
            row = {
                "ledger_version": NORMALIZATION_LEDGER_VERSION,
                "run_id": run_id,
                "seed_id": pair.seed_id,
                "pair_id": pair.pair_id,
                "row_index": pair.row_index,
                "change_index": seq,
                "raw_sha256": norm.raw_sha256,
                "normalized_sha256": norm.normalized_sha256,
                "normalized_candidate_path": _run_member(normalized_candidate, repo_root, run_dir),
                "technical_scxml_pass_all_rules": item["technical_scxml_pass_all_rules"],
                "low_risk_scxml_pass": item["low_risk_scxml_pass"],
                "main_eligibility_included": item["main_eligibility_included"],
                "semantic_preservation_pass": item["semantic_preservation_pass"],
                "semantic_preservation_audit_status": (semantic_audit or {}).get("status"),
                "repair_contribution_allowed": False,
                **change.to_dict(),
            }
            ledger_rows.append(row)

    ledger_path = reports_dir / "plantuml_normalization_ledger.jsonl"
    ledger_text = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in ledger_rows)
    ledger_path.write_text(ledger_text, encoding="utf-8")
    summary = _summarize(items, pairs)
    report_doc = {
        "report_version": RECOVERY_REPORT_VERSION,
        "run_id": run_id,
        "created_at": created,
        "repo_commit": generator_code_commit,
        "repo_commit_semantics": "Clean generator-code commit captured before writing report/run artifacts; the PR head that commits this report can be a later artifact commit.",
        "generator_code_commit": generator_code_commit,
        "generator_worktree_dirty": bool(generator_git_status),
        "generator_git_status_porcelain": generator_git_status,
        "artifact_commit_note": "If this committed report is reviewed at a later PR head, compare generator_code_commit with the parent/code commit used to generate artifacts rather than requiring repo_commit to equal the artifact commit itself.",
        "generation_command": generation_command or "python -m paper_stm_repair_conversion.cli recover-plantuml",
        "schema_version": "r3.1.plantuml_recovery.v0",
        "conversion_contract": "R3.1 only normalizes PlantUML before official -tscxml; canonical STM must still come from official SCXML.",
        "temporary_probe_reference": {
            "path": "temporary read-only v2 probe outside repo (not committed)",
            "temporary_v2_estimate": {"failed": 499, "recovered": 250, "rate_percent": 50.1},
            "status": "production report supersedes the temporary v2 prototype estimate for committed R3.1 evidence; production metrics are the only citable numbers for this PR.",
        },
        "input_sources": [_rel((s if s.is_absolute() else repo_root / s), repo_root) for s in (pair_sources or DEFAULT_PAIR_SOURCES)],
        "normalization_rules_path": "project_1_llm_state_machine_modeling/paper_stm_repair/conversion/normalization/plantuml_rules.json",
        "normalization_ledger_path": _rel(ledger_path, repo_root),
        "normalization_ledger_sha256": sha256_text(ledger_text),
        "source_file_immutability": _source_file_immutability(repo_root, (pair.source_pairs_path for pair in pairs), source_file_sha_before),
        "raw_immutability": raw_immutability,
        "summary": summary,
        "semantic_preservation_audit_summary": _semantic_preservation_summary(items),
        "artifact_archive": {
            "policy": "High-cardinality raw/normalized PlantUML and official SCXML files are preserved as a single committed zip archive under the conversion workspace, not as thousands of loose PR files.",
            "archive_path": "project_1_llm_state_machine_modeling/paper_stm_repair/conversion/artifacts/plantuml_recovery/r3_1_committed/workdir.zip",
            "archive_sha256_path": "project_1_llm_state_machine_modeling/paper_stm_repair/conversion/artifacts/plantuml_recovery/r3_1_committed/workdir.zip.sha256",
            "manifest_path": "project_1_llm_state_machine_modeling/paper_stm_repair/conversion/artifacts/plantuml_recovery/r3_1_committed/manifest.json",
            "zip_member_path_semantics": "Item paths under raw_candidate_path, normalized_candidate_path and preflight.structured_export_path use zip member paths relative to workdir.zip root; extract the zip under a temporary directory to inspect exact candidate/SCXML artifacts.",
        },
        "items": items,
    }
    report_path = reports_dir / "plantuml_recovery_report.json"
    write_json(report_path, report_doc)
    write_recovery_summary(reports_dir / "plantuml_recovery_summary.md", report_doc)
    return report_doc


def _count_by(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for item in items:
        val = str(item.get(key) if item.get(key) is not None else "NA")
        row = out.setdefault(val, {"raw_total": 0, "converted_before": 0, "failed_before": 0, "technical_scxml_pass_all_rules": 0, "low_risk_scxml_pass": 0, "main_eligibility_included": 0, "failed_after": 0})
        row["raw_total"] += 1
        if item["raw_conversion_pass"]:
            row["converted_before"] += 1
        else:
            row["failed_before"] += 1
            if item["technical_scxml_pass_all_rules"]:
                row["technical_scxml_pass_all_rules"] += 1
            if item["low_risk_scxml_pass"]:
                row["low_risk_scxml_pass"] += 1
            if item["main_eligibility_included"]:
                row["main_eligibility_included"] += 1
            if not item["normalized_conversion_pass"]:
                row["failed_after"] += 1
    return out


def _summarize(items: list[dict[str, Any]], pairs: list[PlantumlPair]) -> dict[str, Any]:
    raw_total = len(items)
    converted_before = sum(1 for i in items if i["raw_conversion_pass"])
    failed_before = raw_total - converted_before
    technical = sum(1 for i in items if i["technical_scxml_pass_all_rules"])
    low_risk = sum(1 for i in items if i["low_risk_scxml_pass"])
    main = sum(1 for i in items if i["main_eligibility_included"])
    failed_after = sum(1 for i in items if (not i["raw_conversion_pass"] and not i["normalized_conversion_pass"]))
    by_llm = _count_by(items, "llm")
    by_seed_class = _count_by(items, "seed_class")
    # Cross-LLM gate is meaningful only for LLMS-EMP, whose rows carry an explicit `llm` field.
    # Rows without LLM labels (for example Unified synthetic data) are excluded from this claim gate.
    expected_llms = {"Claude", "DeepSeek", "GPT-4", "GPT-4o", "Kimi", "Llama"}
    eligible_composition_by_llm = _eligible_composition_by_llm(items, expected_llms)
    eligible_by_llm = {
        llm: eligible_composition_by_llm[llm]["eligible_after"]
        for llm in sorted(expected_llms)
    }
    eligible_values = list(eligible_by_llm.values())
    if eligible_values and min(eligible_values) > 0:
        ratio: float | None = round(max(eligible_values) / min(eligible_values), 3)
    else:
        ratio = None
    llm_gate_pass = all(v >= 5 for v in eligible_values) and ratio is not None and ratio <= 2
    naturally = [i["canonical_profile"] for i in items if i["raw_conversion_pass"]]
    recovered = [i["canonical_profile"] for i in items if i["main_eligibility_included"]]
    return {
        "raw_total": raw_total,
        "unique_nl_total": len({p.nl_sha256 for p in pairs}),
        "converted_before": converted_before,
        "failed_before": failed_before,
        "technical_scxml_pass_all_rules": technical,
        "low_risk_scxml_pass": low_risk,
        "main_eligibility_included": main,
        "high_risk_scxml_pass": technical - low_risk,
        "failed_after": failed_after,
        "by_seed": _count_by(items, "seed_id"),
        "by_seed_class": by_seed_class,
        "by_issue_category": _count_by(items, "issue_category"),
        "by_llm": by_llm,
        "llms_emp_cross_llm_gate": {
            "passed": llm_gate_pass,
            "eligible_after_by_llm": eligible_by_llm,
            "eligible_after_composition_by_llm": eligible_composition_by_llm,
            "eligible_after_values": eligible_values,
            "max_min_ratio": ratio,
            "rule": "每个 LLM eligible_after >= 5 且 max/min <= 2 才允许谨慎 cross-LLM aggregate claim；否则只能 coverage/eligibility audit 或 negative finding。",
        },
        "profile_comparison": {
            "naturally_converted": _profile_aggregate(naturally),
            "main_recovered": _profile_aggregate(recovered),
            "interpretation": "Recovered subset is a normalized eligibility subset, not an unbiased representative of the original generation distribution.",
        },
    }


def _semantic_preservation_summary(items: list[dict[str, Any]]) -> dict[str, Any]:
    audited = [i for i in items if i.get("semantic_preservation_audit")]
    failed = [i for i in audited if not i.get("semantic_preservation_pass")]
    low_risk_failed = [
        i for i in failed
        if i.get("low_risk_scxml_pass") or (i.get("normalized_conversion_pass") and not i.get("has_high_risk_loss"))
    ]
    by_status = dict(Counter((i.get("semantic_preservation_audit") or {}).get("status", "not_audited") for i in audited))
    by_rule: dict[str, dict[str, int]] = {}
    for item in audited:
        status = "pass" if item.get("semantic_preservation_pass") else "fail"
        for rule_id in item.get("rule_ids") or ["<no_rule>"]:
            row = by_rule.setdefault(rule_id, {"audited": 0, "pass": 0, "fail": 0})
            row["audited"] += 1
            row[status] += 1
    return {
        "audit_version": "r3.1.plantuml_semantic_preservation.v0",
        "audited_total": len(audited),
        "pass_total": len(audited) - len(failed),
        "fail_total": len(failed),
        "low_risk_fail_total": len(low_risk_failed),
        "main_eligibility_requires_pass": True,
        "by_status": by_status,
        "by_rule": by_rule,
        "failed_pair_ids": [i["pair_id"] for i in failed],
        "low_risk_failed_pair_ids": [i["pair_id"] for i in low_risk_failed],
    }


def _eligible_composition_by_llm(items: list[dict[str, Any]], expected_llms: set[str]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for llm in sorted(expected_llms):
        rows = [i for i in items if i.get("seed_class") == "llms_emp_cross_llm" and i.get("llm") == llm]
        natural = sum(1 for i in rows if i["raw_conversion_pass"])
        recovered_main = sum(1 for i in rows if i["main_eligibility_included"])
        high_risk = sum(1 for i in rows if i["technical_scxml_pass_all_rules"] and not i["low_risk_scxml_pass"])
        failed_after = sum(1 for i in rows if not i["raw_conversion_pass"] and not i["normalized_conversion_pass"])
        eligible_after = natural + recovered_main
        rescue_share = round(recovered_main / eligible_after, 3) if eligible_after else None
        out[llm] = {
            "raw_total": len(rows),
            "naturally_converted": natural,
            "recovered_main": recovered_main,
            "recovered_high_risk_supplementary": high_risk,
            "eligible_after": eligible_after,
            "failed_after": failed_after,
            "rescue_share_of_eligible_after": rescue_share,
        }
    return out


def _profile_aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {"count": 0, "avg_states": 0.0, "avg_transitions": 0.0, "avg_transition_label_chars": 0.0, "hierarchy_counts": {}, "avg_alias_count": 0.0}
    return {
        "count": len(rows),
        "avg_states": round(sum(r["states_count"] for r in rows) / len(rows), 2),
        "avg_transitions": round(sum(r["transitions_count"] for r in rows) / len(rows), 2),
        "avg_transition_label_chars": round(sum(r["transition_label_avg_chars"] for r in rows) / len(rows), 2),
        "hierarchy_counts": dict(Counter(str(r.get("hierarchy_level")) for r in rows)),
        "avg_alias_count": round(sum(r["alias_count"] for r in rows) / len(rows), 2),
    }


def _md_table_counts(title: str, rows: dict[str, dict[str, int]]) -> list[str]:
    lines = [f"## {title}", "", "| 维度 | raw | before converted | before failed | technical pass | low-risk pass | main eligible | failed after |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for key, val in sorted(rows.items()):
        lines.append(f"| `{key}` | {val['raw_total']} | {val['converted_before']} | {val['failed_before']} | {val['technical_scxml_pass_all_rules']} | {val['low_risk_scxml_pass']} | {val['main_eligibility_included']} | {val['failed_after']} |")
    lines.append("")
    return lines


def write_recovery_summary(path: Path, report: dict[str, Any]) -> None:
    s = report["summary"]
    lines = [
        "# R3.1 PlantUML pre-SCXML normalization / recovery 摘要",
        "",
        "本文件由 `python -m paper_stm_repair_conversion.cli recover-plantuml` 生成。它是 R3.1 conversion eligibility 证据，不是 Better STM repair 实验结果。",
        "",
        "## 核心结论",
        "",
        f"- PlantUML 一手 pair 总数：{s['raw_total']}；unique NL：{s['unique_nl_total']}。",
        f"- 原始 PlantUML 官方 SCXML 已可转换：{s['converted_before']}；原始失败：{s['failed_before']}。",
        f"- all-rules 技术通过：{s['technical_scxml_pass_all_rules']}；其中低风险通过：{s['low_risk_scxml_pass']}；主 eligibility 纳入：{s['main_eligibility_included']}；高风险仅 supplementary：{s['high_risk_scxml_pass']}。",
        f"- normalization 后仍失败：{s['failed_after']}。",
        f"- LLMS-EMP cross-LLM gate：{'通过' if s['llms_emp_cross_llm_gate']['passed'] else '未通过'}；ratio={s['llms_emp_cross_llm_gate']['max_min_ratio']}。",
        "- 临时 v2 probe 的 250/499 只是早期 prototype estimate；本文件中的 production report 已取代该估计，论文主 claim 只能使用 low-risk / main eligibility 口径。",
        f"- source-level semantic preservation audit：审计 {report['semantic_preservation_audit_summary']['audited_total']} 个 normalized candidates；通过 {report['semantic_preservation_audit_summary']['pass_total']}；失败 {report['semantic_preservation_audit_summary']['fail_total']}；低风险失败 {report['semantic_preservation_audit_summary']['low_risk_fail_total']}。",
        "",
    ]
    lines.extend(_md_table_counts("按 seed 统计", s["by_seed"]))
    lines.extend(_md_table_counts("按 seed class 统计", s["by_seed_class"]))
    lines.extend(_md_table_counts("按错误类别统计", s["by_issue_category"]))
    lines.extend(_md_table_counts("按 LLM 统计", s["by_llm"]))
    lines.extend([
        "## LLMS-EMP eligible_after 组成",
        "",
        "| LLM | raw | naturally converted | recovered main | high-risk supplementary | eligible after | failed after | rescue share |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for llm, row in s["llms_emp_cross_llm_gate"]["eligible_after_composition_by_llm"].items():
        lines.append(f"| `{llm}` | {row['raw_total']} | {row['naturally_converted']} | {row['recovered_main']} | {row['recovered_high_risk_supplementary']} | {row['eligible_after']} | {row['failed_after']} | {row['rescue_share_of_eligible_after']} |")
    lines.extend([
        "",
        "解释：该表只说明 LLMS-EMP 在 conversion eligibility 层面恢复到可谨慎 aggregate 的平衡；不同 LLM 的 eligible_after 由 naturally-converted 与 recovered-main 的比例不同，不能直接当作原始 STM 质量同分布证据。",
        "",
    ])
    lines.extend([
        "## recovered vs naturally-converted profile",
        "",
        "| subset | count | avg states | avg transitions | avg transition label chars | hierarchy counts | avg alias count |",
        "|---|---:|---:|---:|---:|---|---:|",
    ])
    for name, row in s["profile_comparison"].items():
        if name == "interpretation":
            continue
        lines.append(f"| `{name}` | {row['count']} | {row['avg_states']} | {row['avg_transitions']} | {row['avg_transition_label_chars']} | `{row['hierarchy_counts']}` | {row['avg_alias_count']} |")
    lines.extend([
        "",
        "解释：recovered subset 是 normalized eligibility subset，不是原始生成分布的无偏代表；若后续论文引用，必须保留该限制。",
        "",
        "## source-level semantic preservation audit",
        "",
        "该审计逐项比较 raw PlantUML 与 normalized PlantUML 的状态声明、状态注释、迁移 source/target/label 与结构残留行；normalizer 新增的 alias declaration 会被反解回原始 label，非 PlantUML `stm` heading 与 normalizer comment 只作为语法修复痕迹忽略。它证明的是转换前规范化的 source-signature-preserving / 结构签名保持，不是定理级严格语义等价证明；任何低风险修复若未通过该审计，均不得进入主 eligibility。",
        "",
        "| 指标 | 数量 |",
        "|---|---:|",
        f"| audited_total | {report['semantic_preservation_audit_summary']['audited_total']} |",
        f"| pass_total | {report['semantic_preservation_audit_summary']['pass_total']} |",
        f"| fail_total | {report['semantic_preservation_audit_summary']['fail_total']} |",
        f"| low_risk_fail_total | {report['semantic_preservation_audit_summary']['low_risk_fail_total']} |",
        "",
        "| rule_id | audited | pass | fail |",
        "|---|---:|---:|---:|",
    ])
    for rule_id, row in sorted(report["semantic_preservation_audit_summary"]["by_rule"].items()):
        lines.append(f"| `{rule_id}` | {row['audited']} | {row['pass']} | {row['fail']} |")
    lines.extend([
        "",
        "## 文件与证据",
        "",
        "- JSON report: `plantuml_recovery_report.json`",
        f"- normalization ledger: `{report['normalization_ledger_path']}`",
        f"- generator code commit: `{report['generator_code_commit']}`；该字段记录写出 report 前的 clean 代码提交，承载 report 的 artifact commit 可以是后续提交。",
        f"- generator worktree dirty: `{report['generator_worktree_dirty']}`",
        "- canonical STM 不由 normalizer 直接生成；所有 recovered 判定均基于官方 PlantUML SCXML。",
        f"- full workdir archive: `{report['artifact_archive']['archive_path']}`；report 中 `raw_candidate_path` / `normalized_candidate_path` / `structured_export_path` 对应 zip 内 member 路径。",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")
