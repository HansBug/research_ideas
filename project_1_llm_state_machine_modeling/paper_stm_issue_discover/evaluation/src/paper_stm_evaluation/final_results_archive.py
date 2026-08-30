"""Archive frozen v60/X1v2 audit surfaces and recompute final paper metrics offline.

The tool is deliberately evaluator-only.  It copies structured, auditable JSON and
Markdown from immutable run roots, excludes provider request streams, and never
imports an archive into discovery, grounding, routing, evidence, or Judge code.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from paper_stm_evaluation.x1v2_witness_audit import (
    X1v2FullHitMaxWitnessAudit,
    X1v2WitnessLevelAudit,
    validate_x1v2_witness_audit_artifacts,
    witness_audit_statistics,
)

ARCHIVE_SCHEMA = "paper1.final-results-archive.v1"
SUMMARY_SCHEMA = "paper1.final-results-summary.v1"
PROVENANCE_SCHEMA = "paper1.final-results-provenance-map.v1"
_MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)(?:\s+[^)]*)?\)")
EXCLUDED_RULES = [
    {"rule": "**/llm/**", "reason": "Provider request/response stream and cache; structured method, W2, Judge, usage, and cost audit surfaces are copied separately."},
    {"rule": "**/*.lock and **/*.part", "reason": "Transient runtime synchronization or interrupted-write state is not evidence."},
    {"rule": "**/launcher.log", "reason": "Reproducible process log is not required for metric, evidence, or cost recomputation."},
]

_VALID_NOVEL_REAUDIT_COLUMNS = (
    "report_id",
    "pair_id",
    "round",
    "strict_da",
    "a0_type",
    "corrected_kni",
    "relation",
    "ledger_ids",
    "group_key",
    "reason",
    "basis",
    "source_refs",
)


def _manifest_generation_metadata(command: str) -> dict[str, str]:
    """Describe the provider-free tool invocation that generated one manifest."""

    return {
        "generator": "paper_stm_evaluation.final_results_archive",
        "generation_command": command,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }


def _load(path: Path) -> dict[str, Any]:
    """Load a JSON object and reject non-object audit inputs."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _write(path: Path, value: Any) -> None:
    """Write stable UTF-8 JSON without modifying immutable input artifacts."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    """Return SHA-256 for one archived file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _included_file(path: Path) -> bool:
    """Keep structured audit artifacts while excluding provider and transient files."""

    if "llm" in path.parts or path.suffix in {".lock", ".part"} or path.name == "launcher.log":
        return False
    return path.suffix in {".json", ".md"}


def _copy_tree(source: Path, destination: Path) -> int:
    """Copy the selected structured audit surface and return its file count."""

    copied = 0
    for item in sorted(source.rglob("*")):
        if not item.is_file() or not _included_file(item):
            continue
        target = destination / item.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
        copied += 1
    return copied


def _validate_v60_valid_novel_reaudit(archive: Path) -> None:
    """Validate the additive 444-row D/A and K/N/I reaudit against frozen Judge data."""

    review_root = archive / "reviews"
    tsv_path = review_root / "12_v60_valid_novel_posthoc_reaudit.tsv"
    json_path = review_root / "12_v60_valid_novel_posthoc_reaudit.json"
    if not tsv_path.is_file() and not json_path.is_file():
        return
    if not tsv_path.is_file() or not json_path.is_file():
        raise ValueError("v60 VALID_NOVEL reaudit requires both TSV and JSON")

    with tsv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if tuple(reader.fieldnames or ()) != _VALID_NOVEL_REAUDIT_COLUMNS:
            raise ValueError("v60 VALID_NOVEL reaudit TSV must have the fixed 12-column schema")
        tsv_rows = list(reader)

    audit = _load(json_path)
    decisions = audit.get("decisions")
    if not isinstance(decisions, list) or not all(isinstance(item, dict) for item in decisions):
        raise ValueError("v60 VALID_NOVEL reaudit JSON decisions must be an object list")
    if len(tsv_rows) != 444 or len(decisions) != 444:
        raise ValueError("v60 VALID_NOVEL reaudit must contain exactly 444 rows")

    def decision_as_tsv(decision: dict[str, Any]) -> dict[str, str]:
        return {
            "report_id": str(decision.get("report_id", "")),
            "pair_id": str(decision.get("pair_id", "")),
            "round": str(decision.get("round", "")),
            "strict_da": str(decision.get("strict_da", "")),
            "a0_type": str(decision.get("a0_type") or ""),
            "corrected_kni": str(decision.get("corrected_kni", "")),
            "relation": str(decision.get("relation", "")),
            "ledger_ids": ";".join(str(value) for value in decision.get("ledger_ids", [])),
            "group_key": str(decision.get("group_key", "")),
            "reason": str(decision.get("reason", "")),
            "basis": str(decision.get("basis", "")),
            "source_refs": ";".join(str(value) for value in decision.get("source_refs", [])),
        }

    if tsv_rows != [decision_as_tsv(decision) for decision in decisions]:
        raise ValueError("v60 VALID_NOVEL reaudit TSV and JSON decisions differ")

    report_ids = [str(decision["report_id"]) for decision in decisions]
    if len(set(report_ids)) != len(report_ids):
        raise ValueError("v60 VALID_NOVEL reaudit contains duplicate report IDs")
    current_root = archive / "raw" / "v60_current"
    composite = _load(current_root / "judge" / "composite" / "summary.json")
    frozen_novel_ids = {
        str(outcome["original_report_id"])
        for result in _pair_results(current_root, composite)
        for outcome in result.get("report_outcomes", [])
        if isinstance(outcome, dict) and outcome.get("validity") == "VALID_NOVEL"
    }
    if set(report_ids) != frozen_novel_ids:
        raise ValueError("v60 VALID_NOVEL reaudit report IDs do not close over frozen Judge N")

    da_counts: Counter[str] = Counter()
    kni_counts: Counter[str] = Counter()
    relation_counts: Counter[str] = Counter()
    a0_counts: Counter[str] = Counter()
    group_verdicts: dict[str, set[tuple[str, str, str, str, tuple[str, ...]]]] = defaultdict(set)
    for decision in decisions:
        report_id = str(decision["report_id"])
        pair_id = str(decision["pair_id"])
        strict_da = str(decision["strict_da"])
        a0_type = decision.get("a0_type")
        corrected_kni = str(decision["corrected_kni"])
        relation = str(decision["relation"])
        ledger_ids = tuple(str(value) for value in decision.get("ledger_ids", []))
        group_key = str(decision.get("group_key", ""))
        source_refs = decision.get("source_refs")
        if not report_id.startswith(f"{pair_id}:r{decision['round']}:"):
            raise ValueError(f"reaudit identity fields disagree: {report_id}")
        if strict_da not in {"D2", "D1", "D0", "A0"}:
            raise ValueError(f"invalid strict D/A value for {report_id}: {strict_da}")
        if strict_da == "A0":
            if a0_type not in {"FALSE_POSITIVE", "NOT_A_DEFECT_CLAIM"}:
                raise ValueError(f"invalid A0 subtype for {report_id}: {a0_type!r}")
            a0_counts[str(a0_type)] += 1
        elif a0_type is not None:
            raise ValueError(f"non-A0 row carries an A0 subtype: {report_id}")
        if strict_da in {"D0", "A0"}:
            expected_kni, expected_relations = "I", {"NO_MATCH"}
        elif relation in {"FULL_MATCH", "PARTIAL_MATCH"}:
            expected_kni, expected_relations = "K", {"FULL_MATCH", "PARTIAL_MATCH"}
        else:
            expected_kni, expected_relations = "N", {"NO_MATCH"}
        if corrected_kni != expected_kni or relation not in expected_relations:
            raise ValueError(f"D/A, relation, and K/N/I do not close for {report_id}")
        if (corrected_kni == "K") != bool(ledger_ids):
            raise ValueError(f"only K rows may carry ledger IDs, and every K row must carry one: {report_id}")
        if re.match(rf"^{re.escape(pair_id)}[:|]", group_key) is None:
            raise ValueError(f"reaudit group crosses or omits its pair boundary: {report_id}")
        if not str(decision.get("reason", "")).strip() or not str(decision.get("basis", "")).strip():
            raise ValueError(f"reaudit reason/basis is empty: {report_id}")
        if not isinstance(source_refs, list) or not source_refs:
            raise ValueError(f"reaudit source_refs is empty: {report_id}")
        for source_ref in source_refs:
            value = str(source_ref)
            if value.startswith(("raw/", "reference/")):
                relative_path, _, fragment = value.partition("#")
                target = archive / relative_path
                if not target.is_file():
                    raise ValueError(f"reaudit archive source does not exist for {report_id}: {value}")
                if target.name == "ledger.json" and fragment:
                    pointed: Any = _load(target)
                    for component in fragment.strip("/").split("/"):
                        if not isinstance(pointed, dict) or component not in pointed:
                            raise ValueError(f"reaudit ledger fragment does not resolve for {report_id}: {value}")
                        pointed = pointed[component]
        da_counts[strict_da] += 1
        kni_counts[corrected_kni] += 1
        relation_counts[relation] += 1
        group_verdicts[group_key].add((strict_da, str(a0_type or ""), corrected_kni, relation, ledger_ids))

    if any(len(verdicts) != 1 for verdicts in group_verdicts.values()):
        raise ValueError("v60 VALID_NOVEL reaudit has a group with heterogeneous verdicts")
    summary = audit.get("summary", {})
    expected_summary = {
        "report_rows": len(decisions),
        "decision_groups": len(group_verdicts),
        "strict_da": {key: da_counts[key] for key in ("D2", "D1", "D0", "A0")},
        "corrected_kni": {key: kni_counts[key] for key in ("K", "N", "I")},
        "relation": {key: relation_counts[key] for key in ("FULL_MATCH", "PARTIAL_MATCH", "NO_MATCH")},
        "a0_type": {key: a0_counts[key] for key in ("FALSE_POSITIVE", "NOT_A_DEFECT_CLAIM")},
    }
    for key, value in expected_summary.items():
        if summary.get(key) != value:
            raise ValueError(f"v60 VALID_NOVEL reaudit summary mismatch: {key}")
    recorded_hash = str(audit.get("artifacts", {}).get("tsv_sha256", ""))
    if recorded_hash != _sha256(tsv_path).removeprefix("sha256:"):
        raise ValueError("v60 VALID_NOVEL reaudit TSV hash is stale")


def _copy_file(source: Path, destination: Path) -> None:
    """Copy one declared immutable input with parent creation."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def _source_runs(composite_path: Path) -> list[dict[str, Any]]:
    """Read the source-run provenance entries retained by a Judge composite."""

    return [item for item in _load(composite_path).get("source_runs", []) if isinstance(item, dict)]


def _copy_judge_sources(composite_path: Path, destination: Path) -> list[dict[str, Any]]:
    """Copy every source Judge run selected or retained by a composite."""

    copied: list[dict[str, Any]] = []
    for source in _source_runs(composite_path):
        manifest_path = Path(str(source["manifest_path"])).resolve()
        source_root = manifest_path.parent
        run_id = str(source["run_id"])
        _copy_tree(source_root, destination / run_id)
        copied.append({
            "run_id": run_id,
            "source_root": str(source_root),
            "archived_path": str((destination / run_id).relative_to(destination.parents[3])),
            "manifest_sha256": source.get("manifest_hash"),
            "terminal_sha256": source.get("terminal_hash"),
        })
    return copied


def _pair_results(side_root: Path, composite: dict[str, Any]) -> list[dict[str, Any]]:
    """Resolve the exact composite-selected pair results inside an archive side."""

    results: list[dict[str, Any]] = []
    for receipt in composite.get("pair_receipts", []):
        if not isinstance(receipt, dict):
            continue
        run_id = str(receipt["source_run_id"])
        pair_id = str(receipt["pair_id"])
        path = side_root / "judge" / "source_runs" / run_id / "pairs" / f"{pair_id}.json"
        result = _load(path)
        if _sha256(path) != receipt.get("result_hash"):
            raise ValueError(f"pair hash mismatch for {path}")
        results.append(result)
    return results


def _ratio(count: int, denominator: int) -> dict[str, Any]:
    """Keep numerator and denominator together for final-paper metrics."""

    return {"count": count, "denominator": denominator, "rate": None if denominator == 0 else count / denominator}


def _ledger_levels(ledger_path: Path) -> dict[str, str]:
    """Read external L labels only in the evaluator/reporting layer."""

    items = _load(ledger_path).get("items", {})
    return {str(key): str(value.get("L")) for key, value in items.items() if isinstance(value, dict)}


def _aggregate_judge(pair_results: Iterable[dict[str, Any]], levels: dict[str, str]) -> dict[str, Any]:
    """Recompute hit, K/N/I, cluster, and per-round metrics from PairJudgeResult JSON."""

    expected_rows: list[dict[str, Any]] = []
    report_rows: list[dict[str, Any]] = []
    for result in pair_results:
        pair_id, round_number = str(result["pair_id"]), int(result["round"])
        for outcome in result.get("expected_outcomes", []):
            if not isinstance(outcome, dict):
                continue
            expected_rows.append({
                "pair_id": pair_id,
                "round": round_number,
                "expected_id": str(outcome["ledger_id"]),
                "full": bool(outcome.get("hit")),
                "supported": bool(outcome.get("supported")),
            })
        for outcome in result.get("report_outcomes", []):
            if not isinstance(outcome, dict):
                continue
            report_rows.append({
                "pair_id": pair_id,
                "round": round_number,
                "validity": str(outcome.get("validity")),
                "cluster": str(outcome.get("root_cause_cluster_key")),
            })

    by_expected: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in expected_rows:
        by_expected[row["expected_id"]].append(row)
    if any(len(rows) != 3 for rows in by_expected.values()):
        raise ValueError("every expected issue must have exactly three selected rounds")

    def hit_views(ids: list[str]) -> dict[str, Any]:
        rows = [by_expected[issue_id] for issue_id in ids]
        return {
            "round_level_full": _ratio(sum(item["full"] for group in rows for item in group), len(rows) * 3),
            "hit_at_3": _ratio(sum(any(item["full"] for item in group) for group in rows), len(rows)),
            "hit_at_all": _ratio(sum(all(item["full"] for item in group) for group in rows), len(rows)),
        }

    all_ids = sorted(by_expected)
    l2_ids = [issue_id for issue_id in all_ids if levels.get(issue_id) == "L2"]
    validity_counts = Counter(row["validity"] for row in report_rows)
    clusters: dict[str, set[str]] = defaultdict(set)
    for row in report_rows:
        clusters[f"{row['pair_id']}:r{row['round']}::{row['cluster']}"] .add(row["validity"])
    known_cluster_count = sum("VALID_KNOWN" in values for values in clusters.values())
    novel_cluster_count = sum("VALID_KNOWN" not in values and "VALID_NOVEL" in values for values in clusters.values())
    valid_cluster_count = known_cluster_count + novel_cluster_count
    invalid_cluster_count = sum(values == {"INVALID"} for values in clusters.values())
    valid_reports = validity_counts["VALID_KNOWN"] + validity_counts["VALID_NOVEL"]
    return {
        "expected_rows": expected_rows,
        "round_count": 3,
        "pair_count": len({str(result["pair_id"]) for result in pair_results}),
        "overall": hit_views(all_ids),
        "l2": hit_views(l2_ids),
        "match_counts": {
            "FULL": sum(row["full"] for row in expected_rows),
            "PARTIAL": sum(not row["full"] and row["supported"] for row in expected_rows),
            "NONE": sum(not row["supported"] for row in expected_rows),
        },
        "report_validity": {
            "counts": {key: validity_counts[key] for key in ("VALID_KNOWN", "VALID_NOVEL", "INVALID")},
            "total": len(report_rows),
            "semantic_precision": valid_reports / len(report_rows) if report_rows else None,
        },
        "cluster_validity": {
            "counts": {
                "VALID_KNOWN": known_cluster_count,
                "VALID_NOVEL": novel_cluster_count,
                "VALID": valid_cluster_count,
                "INVALID": invalid_cluster_count,
            },
            "total": len(clusters),
            "semantic_precision": valid_cluster_count / len(clusters) if clusters else None,
        },
        "per_round": [
            {
                "round": round_number,
                "overall_full": _ratio(sum(row["full"] for row in expected_rows if row["round"] == round_number), len(all_ids)),
                "l2_full": _ratio(sum(row["full"] for row in expected_rows if row["round"] == round_number and row["expected_id"] in l2_ids), len(l2_ids)),
                "report_validity": {
                    "counts": {key: sum(row["validity"] == key and row["round"] == round_number for row in report_rows) for key in ("VALID_KNOWN", "VALID_NOVEL", "INVALID")},
                },
            }
            for round_number in (1, 2, 3)
        ],
    }


def _current_witness(evaluator_path: Path) -> dict[str, Any]:
    """Recompute max witness levels from the expected-witness rows, not report totals."""

    rows = _load(evaluator_path).get("rows", [])
    full_rows = [row for row in rows if row.get("match_status") == "FULL"]
    counts = Counter(str(row.get("max_witness_level")) for row in full_rows)
    all_w2 = sum(str(row.get("max_witness_level")) == "W2" for row in rows)
    return {
        "full_hit_max_witness": {
            "denominator": len(full_rows),
            "counts": {level: counts[level] for level in ("W2", "W1", "W0")},
        },
        "w2_all_expected": _ratio(all_w2, len(rows)),
    }


def _registry_predicates(registry_path: Path) -> dict[str, dict[str, Any]]:
    """Flatten the frozen registry families without changing their definitions."""

    predicates: dict[str, dict[str, Any]] = {}
    for family_index, family in enumerate(_load(registry_path).get("families", [])):
        definitions = family.get("predicates", []) if isinstance(family, dict) else family
        if not isinstance(definitions, list):
            continue
        for definition in definitions:
            if isinstance(definition, dict) and isinstance(definition.get("id"), str):
                predicates[str(definition["id"])] = {
                    "family": str(definition["id"])[0],
                    "family_index": family_index,
                    "name": definition.get("name"),
                    "semantics": definition.get("semantics"),
                    "inputs": definition.get("inputs", []),
                }
    if len(predicates) != 19:
        raise ValueError(f"expected 19 frozen predicates, found {len(predicates)}")
    return predicates


def _predicate_table(method_root: Path, registry_path: Path, feasibility: dict[str, Any], planned: list[str]) -> list[dict[str, Any]]:
    """Derive stage-separated predicate counts from archived method evidence records."""

    definitions = _registry_predicates(registry_path)
    route_counts: Counter[str] = Counter()
    precise_binding_counts: Counter[str] = Counter()
    for path in sorted((method_root / "method").glob("*/round-*.json")):
        record = _load(path)
        for evidence in record.get("evidence_records", []):
            if not isinstance(evidence, dict):
                continue
            plan = evidence.get("plan")
            predicate_id = evidence.get("predicate_id")
            if predicate_id is None and isinstance(plan, dict):
                predicate_id = plan.get("predicate_id")
            if predicate_id not in definitions:
                continue
            route_counts[str(predicate_id)] += 1
            binding = evidence.get("binding")
            if isinstance(binding, dict) and binding.get("precise") is True:
                precise_binding_counts[str(predicate_id)] += 1
    rows: list[dict[str, Any]] = []
    for predicate_id in sorted(definitions):
        row = dict(definitions[predicate_id])
        audit = feasibility.get(predicate_id, {})
        row.update({
            "predicate_id": predicate_id,
            "planned_in_selected_protocol": predicate_id in planned,
            "candidate_route_count": route_counts[predicate_id],
            "precise_binding_count": precise_binding_counts[predicate_id],
            "receipt_count": audit.get("receipt_count", 0),
            "terminal_execution_count": audit.get("terminal_execution_count", 0),
            "executed_pass": audit.get("executed_pass", 0),
            "executed_violation": audit.get("executed_violation", 0),
            "witness_counts": audit.get("witness_counts", {}),
            "input_contract_missing": audit.get("input_contract_missing", 0),
            "out_of_fragment": audit.get("out_of_fragment", 0),
            "unsupported_backend_failure_count": audit.get("unsupported_backend_failure_count", 0),
            "failure_kinds": audit.get("failure_kinds", {}),
            "zero_use_reason": audit.get("zero_use_reason"),
            "reason": audit.get("reason"),
            "basis": audit.get("basis"),
        })
        rows.append(row)
    return rows


def _file_manifest(root: Path, *, excluded_relative_paths: set[str] | None = None) -> list[dict[str, Any]]:
    """List archived files while excluding only declared self-referential paths."""

    excluded = excluded_relative_paths or set()
    files: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative_path = str(path.relative_to(root))
        if relative_path in excluded:
            continue
        files.append({"path": relative_path, "bytes": path.stat().st_size, "sha256": _sha256(path)})
    return files


def _publication_file_manifest(root: Path) -> list[dict[str, Any]]:
    """List only the current v4 publication surface, excluding raw and superseded layers."""

    exact = {
        "README.md",
        "SCHEMA.md",
        "report/v60_current_vs_x1v2_baseline_v4_cn.md",
        "reviews/publication_docs_inventory_v4.json",
        "reviews/publication_docs_inventory_v4.tsv",
        "reviews/track_a_numeric_provenance_v4.md",
        "reviews/track_b_semantic_fairness_v4.md",
        "reviews/track_c_docs_navigation_academic_v4.md",
        "reviews/final_publication_surface_review_v4.md",
    }
    prefixes = (
        "derived/fair_comparison_v4/",
        "derived/manual_adjudication_v4_current_reaudit/",
        "derived/manual_adjudication_v3_baseline_ni/",
    )
    excluded_prefixes = (
        "derived/manual_adjudication_v3_baseline_ni/proposals/",
    )
    archive_only_provenance = {
        "derived/manual_adjudication_v3_baseline_ni/reviews/academic_citation_review.md",
        "derived/manual_adjudication_v3_baseline_ni/reviews/numeric_recompute_review_v3.md",
    }
    files: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative_path = path.relative_to(root).as_posix()
        if relative_path not in exact and not relative_path.startswith(prefixes):
            continue
        if relative_path in archive_only_provenance or relative_path.startswith(excluded_prefixes):
            continue
        files.append({"path": relative_path, "bytes": path.stat().st_size, "sha256": _sha256(path)})
    return files


def _repository_root() -> Path:
    """Locate the checked-out repository that owns this evaluator-only module."""

    for candidate in Path(__file__).resolve().parents:
        if (candidate / ".git").exists():
            return candidate
    raise ValueError("could not locate repository root for archive link validation")


def _resolve_relative(path: Path, root: Path, *, label: str) -> Path:
    """Resolve one archive reference while refusing paths that escape its root."""

    resolved_root = root.resolve()
    resolved_path = path.resolve()
    try:
        resolved_path.relative_to(resolved_root)
    except ValueError as error:
        raise ValueError(f"{label} escapes its allowed root: {path}") from error
    return resolved_path


def _validate_archive_metadata(archive: Path) -> None:
    """Check declared schemas and stable archive-relative provenance mappings."""

    manifest_specs = (
        (archive / "archive_manifest.json", ARCHIVE_SCHEMA),
        (archive / "raw" / "v60_current" / "archive_manifest.json", ARCHIVE_SCHEMA),
        (archive / "raw" / "x1v2_baseline" / "archive_manifest.json", ARCHIVE_SCHEMA),
    )
    for manifest_path, expected_schema in manifest_specs:
        manifest = _load(manifest_path)
        if manifest.get("schema") != expected_schema:
            raise ValueError(f"unexpected manifest schema in {manifest_path}: {manifest.get('schema')!r}")
        if not isinstance(manifest.get("included_files"), list):
            raise ValueError(f"manifest does not declare included_files: {manifest_path}")

    summary = _load(archive / "derived" / "recomputed_summary.json")
    if summary.get("schema") != SUMMARY_SCHEMA:
        raise ValueError(f"unexpected summary schema: {summary.get('schema')!r}")

    provenance_path = archive / "provenance_path_mapping.json"
    provenance = _load(provenance_path)
    if provenance.get("schema") != PROVENANCE_SCHEMA:
        raise ValueError(f"unexpected provenance schema: {provenance.get('schema')!r}")
    mappings = provenance.get("mappings")
    if not isinstance(mappings, list) or not mappings:
        raise ValueError("provenance mapping is missing stable archive-relative paths")
    for mapping in mappings:
        if not isinstance(mapping, dict) or not isinstance(mapping.get("archive_relative_path"), str):
            raise ValueError("invalid provenance mapping entry")
        target = _resolve_relative(
            archive / mapping["archive_relative_path"],
            archive,
            label="provenance mapping",
        )
        if not target.exists():
            raise ValueError(f"provenance mapping target is absent: {target}")


def _validate_markdown_links(archive: Path, *, repository_root: Path | None = None) -> None:
    """Require every local Markdown link to resolve inside the checked-out repository."""

    repository = (repository_root or _repository_root()).resolve()
    for markdown_path in sorted(archive.rglob("*.md")):
        for match in _MARKDOWN_LINK.finditer(markdown_path.read_text(encoding="utf-8")):
            destination = match.group(1).strip()
            if destination.startswith(("#", "http://", "https://", "mailto:")):
                continue
            local_path = destination.split("#", maxsplit=1)[0].split("?", maxsplit=1)[0]
            # Repository review Markdown uses ``path:line`` as a stable source
            # location.  Resolve the file portion while preserving the line
            # number in the rendered link text.
            line_suffix = re.search(r":\d+$", local_path)
            if line_suffix:
                local_path = local_path[:line_suffix.start()]
            if not local_path:
                continue
            resolved = (markdown_path.parent / local_path).resolve()
            try:
                relative_to_repository = resolved.relative_to(repository)
            except ValueError as error:
                raise ValueError(f"Markdown link escapes repository: {markdown_path} -> {destination}") from error
            if "runs" in relative_to_repository.parts:
                raise ValueError(f"Markdown link points to transient runs data: {markdown_path} -> {destination}")
            if not resolved.exists():
                raise ValueError(f"Markdown link is missing: {markdown_path} -> {destination}")


def _copy_inputs(args: argparse.Namespace) -> dict[str, Any]:
    """Create the stable raw/reference archive from the declared immutable roots."""

    archive = args.archive_root.resolve()
    if archive.exists():
        shutil.rmtree(archive)
    archive.mkdir(parents=True)
    current = archive / "raw" / "v60_current"
    baseline = archive / "raw" / "x1v2_baseline"
    _copy_tree(args.current_method_root.resolve(), current / "method")
    _copy_tree(args.current_judge_root.resolve(), current / "judge" / "composite")
    _copy_judge_sources(args.current_judge_root.resolve() / "summary.json", current / "judge" / "source_runs")
    _copy_tree(args.baseline_method_root.resolve(), baseline / "method")
    _copy_file(args.baseline_judge_composite.resolve(), baseline / "judge" / "composite-summary.json")
    _copy_judge_sources(args.baseline_judge_composite.resolve(), baseline / "judge" / "source_runs")
    _copy_file(args.baseline_cost_audit.resolve(), baseline / "method" / "corrected_cost_audit.json")
    _copy_file(args.ledger.resolve(), archive / "reference" / "ledger.json")
    _copy_file(args.registry.resolve(), archive / "reference" / "predicate_registry.json")
    _copy_file(args.source_catalog.resolve(), archive / "reference" / "current_source_catalog.json")
    return {"archive": archive, "current": current, "baseline": baseline}


def _summary(paths: dict[str, Any]) -> dict[str, Any]:
    """Build the machine-readable final comparison solely from archived files."""

    archive, current, baseline = paths["archive"], paths["current"], paths["baseline"]
    levels = _ledger_levels(archive / "reference" / "ledger.json")
    current_composite = _load(current / "judge" / "composite" / "summary.json")
    baseline_composite = _load(baseline / "judge" / "composite-summary.json")
    current_metrics = _aggregate_judge(_pair_results(current, current_composite), levels)
    baseline_metrics = _aggregate_judge(_pair_results(baseline, baseline_composite), levels)
    current_eval = current / "judge" / "composite" / "evaluator"
    current_evaluation = _load(current_eval / "evaluation_summary.json")
    witness = _current_witness(current_eval / "expected_issue_witness_audit.json")
    current_summary = _load(current / "method" / "summary.json")
    baseline_records = sorted((baseline / "method").rglob("record.json"))
    if len(baseline_records) != 162:
        raise ValueError(f"expected 162 archived X1v2 records, found {len(baseline_records)}")
    baseline_record = _load(baseline_records[0])
    baseline_cost = _load(baseline / "method" / "corrected_cost_audit.json")
    baseline_witness_path = archive / "derived" / "x1v2_witness_level_audit.json"
    baseline_hit_witness_path = archive / "derived" / "x1v2_full_hit_max_witness_audit.json"
    baseline_witness = (
        witness_audit_statistics(
            X1v2WitnessLevelAudit.model_validate(_load(baseline_witness_path)),
            X1v2FullHitMaxWitnessAudit.model_validate(_load(baseline_hit_witness_path)),
        )
        if baseline_witness_path.is_file() and baseline_hit_witness_path.is_file()
        else {"status": "not_applicable", "reason": "This archived summary predates the evaluator-only X1v2 manual W audit; once the audit is finalized, X1v2 W is derived from its manual finding labels rather than the predicate receipt schema."}
    )
    current_cost = _load(current_eval / "judge_cost_audit.json").get("billing", {})
    return {
        "schema": SUMMARY_SCHEMA,
        "reason": "Provider-free recomputation from archived PairJudgeResult, expected-witness, method-summary, cost, ledger, and registry JSON.",
        "basis": "All paths are relative to the final archive and content hashes are checked by the validation command.",
        "sides": {
            "v60_current": {
                "method": {"run_id": current_summary.get("run_id"), "source_commit": current_summary.get("source_commit"), "profile": current_summary.get("profile"), "workers": current_summary.get("workers"), "transport_retries": current_summary.get("transport_retries")},
                "judge": {"commit": current_composite.get("semantic_judge_commit"), "protocol": current_composite.get("protocol_version"), "profile": current_composite.get("model_profile")},
                "metrics": current_metrics,
                "witness": witness,
                "planned_predicates": current_evaluation.get("planned_predicates", []),
                "planned_predicate_scope": current_evaluation.get("planned_predicate_scope"),
                "predicate_feasibility": current_evaluation.get("predicate_feasibility"),
                "predicate_table": _predicate_table(
                    current / "method",
                    archive / "reference" / "predicate_registry.json",
                    current_evaluation.get("predicate_feasibility", {}),
                    current_evaluation.get("planned_predicates", []),
                ),
                "cost": {"method_usd": current_summary.get("method_cost_usd"), "method_cost_eligible": current_summary.get("metrics", {}).get("cost", {}).get("eligible"), "judge_recorded_usd": current_cost.get("recorded_cost_usd"), "judge_cost_eligible": current_cost.get("cost_eligible"), "judge_unpriced_billable_call_count": current_cost.get("unpriced_billable_call_count"), "judge_logical_call_count": current_cost.get("logical_call_count")},
            },
            "x1v2_baseline": {
                "method": {"record_count": len(baseline_records), "profile": baseline_record.get("profile"), "configured_model": baseline_record.get("configured_model"), "source_commit": None, "reason": "The legacy X1v2 method record schema has 162 per-cell record.json files and no top-level source-commit summary."},
                "judge": {"commit": baseline_composite.get("semantic_judge_commit"), "protocol": baseline_composite.get("protocol_version"), "profile": baseline_composite.get("model_profile"), "execution_erratum_commit": baseline_composite.get("execution_erratum_commit")},
                "metrics": baseline_metrics,
                "witness": baseline_witness,
                "predicate_usage": {"status": "not_applicable", "reason": "X1v2 has no isomorphic 19-predicate registry or terminal PredicateExecutionReceipt schema."},
                "cost": {"method_usd": baseline_cost.get("corrected_method_cost_usd"), "method_cost_eligible": baseline_cost.get("cost_eligible"), "judge_recorded_usd": baseline_composite.get("total_incurred_cost_usd"), "judge_cost_eligible": True},
            },
        },
    }


def _write_manifests(paths: dict[str, Any], summary: dict[str, Any], source_args: argparse.Namespace) -> None:
    """Write side manifests and a top-level provenance manifest after copying."""

    archive = paths["archive"]
    source_map = {
        "v60_current": {"method_root": str(source_args.current_method_root.resolve()), "judge_root": str(source_args.current_judge_root.resolve())},
        "x1v2_baseline": {"method_root": str(source_args.baseline_method_root.resolve()), "judge_composite": str(source_args.baseline_judge_composite.resolve()), "cost_audit": str(source_args.baseline_cost_audit.resolve())},
    }
    for side, root in (("v60_current", paths["current"]), ("x1v2_baseline", paths["baseline"])):
        _write(root / "archive_manifest.json", {
            "schema": ARCHIVE_SCHEMA,
            "artifact_id": side,
            "source": source_map[side],
            "archived_relative_path": str(root.relative_to(archive)),
            "summary": summary["sides"][side],
            "included_files": _file_manifest(root, excluded_relative_paths={"archive_manifest.json"}),
            "excluded_rules": EXCLUDED_RULES,
            "offline_recomputation_complete": True,
            "known_data_gaps": summary["sides"][side].get("witness", {}).get("reason"),
            "reason": "Structured raw audit evidence is preserved separately from evaluator-derived summaries.",
            "basis": "File SHA-256 values and the provider-free recomputation command in README.md.",
            **_manifest_generation_metadata(
                "python3 -m paper_stm_evaluation.final_results_archive recompute --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline"
            ),
        })
    _write(archive / "archive_manifest.json", {
        "schema": ARCHIVE_SCHEMA,
        "artifact_id": "v60-current-vs-x1v2-baseline",
        "archive_relative_path": str(archive.relative_to(archive.parents[4])),
        "included_files": _file_manifest(archive, excluded_relative_paths={"archive_manifest.json", "publication_manifest.json"}),
        "excluded_rules": EXCLUDED_RULES,
        "offline_recomputation_complete": True,
        "reason": "Final paper archive for two frozen experimental arms.",
        "basis": "Per-side manifests and deterministic offline recomputation.",
        **_manifest_generation_metadata(
            "python3 -m paper_stm_evaluation.final_results_archive recompute --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline"
        ),
    })


def recompute(args: argparse.Namespace) -> int:
    """Refresh only evaluator-derived summary and manifests from archived immutable data."""

    archive = args.archive_root.resolve()
    paths = {"archive": archive, "current": archive / "raw" / "v60_current", "baseline": archive / "raw" / "x1v2_baseline"}
    summary = _summary(paths)
    _write(archive / "derived" / "recomputed_summary.json", summary)
    source_args = argparse.Namespace(
        current_method_root=Path(str(_load(paths["current"] / "archive_manifest.json")["source"]["method_root"])),
        current_judge_root=Path(str(_load(paths["current"] / "archive_manifest.json")["source"]["judge_root"])),
        baseline_method_root=Path(str(_load(paths["baseline"] / "archive_manifest.json")["source"]["method_root"])),
        baseline_judge_composite=Path(str(_load(paths["baseline"] / "archive_manifest.json")["source"]["judge_composite"])),
        baseline_cost_audit=Path(str(_load(paths["baseline"] / "archive_manifest.json")["source"]["cost_audit"])),
    )
    _write_manifests(paths, summary, source_args)
    return 0


def finalize(args: argparse.Namespace) -> int:
    """Hash the complete published archive after reports and reviews are added."""

    archive = args.archive_root.resolve()
    if not (archive / "archive_manifest.json").is_file():
        raise ValueError("archive_manifest.json is required before finalization")
    mappings: list[dict[str, str]] = []
    for side in ("v60_current", "x1v2_baseline"):
        manifest = _load(archive / "raw" / side / "archive_manifest.json")
        for source_key, source_path in manifest.get("source", {}).items():
            if not isinstance(source_path, str):
                continue
            if source_key == "method_root":
                target = f"raw/{side}/method"
            elif source_key in {"judge_root", "judge_composite"}:
                target = f"raw/{side}/judge"
            elif source_key == "cost_audit":
                target = f"raw/{side}/method/corrected_cost_audit.json"
            else:
                continue
            mappings.append({
                "side": side,
                "source_key": source_key,
                "source_original_path": source_path,
                "archive_relative_path": target,
            })
    _write(archive / "provenance_path_mapping.json", {
        "schema": PROVENANCE_SCHEMA,
        "reason": "Raw evidence retains original absolute provenance paths; this map supplies stable archive-relative roots for offline review.",
        "basis": "Per-side archive manifests generated from the declared immutable source roots.",
        "mappings": mappings,
    })
    _write(archive / "archive_manifest.json", {
        "schema": ARCHIVE_SCHEMA,
        "artifact_id": "v60-current-vs-x1v2-baseline",
        "archive_relative_path": str(archive.relative_to(archive.parents[4])),
        "included_files": _file_manifest(archive, excluded_relative_paths={"archive_manifest.json", "publication_manifest.json"}),
        "excluded_rules": EXCLUDED_RULES,
        "offline_recomputation_complete": True,
        "reason": "Top-level archive manifest regenerated after all evaluator-derived reports and review records are present.",
        "basis": "Every listed file has a stable repository-relative path, byte count, and SHA-256; publication_manifest.json is finalized afterward.",
        **_manifest_generation_metadata(
            "python3 -m paper_stm_evaluation.final_results_archive finalize --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline"
        ),
    })
    publication_files = _publication_file_manifest(archive)
    _write(archive / "publication_manifest.json", {
        "schema": ARCHIVE_SCHEMA,
        "artifact_id": "v60-current-vs-x1v2-baseline-publication",
        "archive_relative_path": str(archive.relative_to(archive.parents[4])),
        "included_files": publication_files,
        "excluded_rules": EXCLUDED_RULES,
        "publication_surface": {
            "current_headline": "report/v60_current_vs_x1v2_baseline_v4_cn.md",
            "current_canonical_prefix": "derived/manual_adjudication_v4_current_reaudit/",
            "baseline_canonical_prefix": "derived/manual_adjudication_v3_baseline_ni/",
            "comparison_prefix": "derived/fair_comparison_v4/",
            "historical_pointer": "archive_manifest.json",
        },
        "offline_recomputation_complete": True,
        "reason": "Publication manifest for the current v4 report and versioned canonical/derived layers only; raw and superseded layers remain bound by archive_manifest.json.",
        "basis": "The validate command checks every listed SHA-256 and validates the explicit v4 allowlist without treating raw or superseded layers as current headline data.",
        **_manifest_generation_metadata(
            "python3 -m paper_stm_evaluation.final_results_archive finalize --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline"
        ),
    })
    return 0


def build(args: argparse.Namespace) -> int:
    """Copy immutable audit data and emit its offline-recomputed machine summary."""

    paths = _copy_inputs(args)
    summary = _summary(paths)
    _write(paths["archive"] / "derived" / "recomputed_summary.json", summary)
    _write_manifests(paths, summary, args)
    return 0


def validate(args: argparse.Namespace) -> int:
    """Validate schemas, links, hashes, and regenerated metrics without a provider."""

    archive = args.archive_root.resolve()
    repository_root = (
        args.repository_root.resolve()
        if args.repository_root is not None
        else _repository_root()
    )
    _validate_archive_metadata(archive)
    _validate_markdown_links(archive, repository_root=repository_root)
    _validate_v60_valid_novel_reaudit(archive)
    for manifest_path in (
        archive / "archive_manifest.json",
        archive / "raw" / "v60_current" / "archive_manifest.json",
        archive / "raw" / "x1v2_baseline" / "archive_manifest.json",
    ):
        manifest = _load(manifest_path)
        root = manifest_path.parent
        for item in manifest["included_files"]:
            path = root / item["path"]
            if not path.is_file() or path.stat().st_size != item["bytes"] or _sha256(path) != item["sha256"]:
                raise ValueError(f"manifest mismatch: {path}")
    paths = {"archive": archive, "current": archive / "raw" / "v60_current", "baseline": archive / "raw" / "x1v2_baseline"}
    witness_audit = archive / "derived" / "x1v2_witness_level_audit.json"
    witness_hit_audit = archive / "derived" / "x1v2_full_hit_max_witness_audit.json"
    if witness_audit.is_file() or witness_hit_audit.is_file():
        if not (witness_audit.is_file() and witness_hit_audit.is_file()):
            raise ValueError("X1v2 witness audit and full-hit witness audit must be present together")
        validate_x1v2_witness_audit_artifacts(archive, repository_root)
    regenerated = _summary(paths)
    recorded = _load(archive / "derived" / "recomputed_summary.json")
    if regenerated != recorded:
        raise ValueError("recomputed summary differs from archived summary")
    publication_manifest = archive / "publication_manifest.json"
    if publication_manifest.is_file():
        manifest = _load(publication_manifest)
        if manifest.get("schema") != ARCHIVE_SCHEMA:
            raise ValueError(f"unexpected publication manifest schema: {manifest.get('schema')!r}")
        expected = _publication_file_manifest(archive)
        if manifest.get("included_files") != expected:
            raise ValueError("publication manifest does not cover the current archive")
        for item in manifest["included_files"]:
            path = archive / item["path"]
            if not path.is_file() or path.stat().st_size != item["bytes"] or _sha256(path) != item["sha256"]:
                raise ValueError(f"publication manifest mismatch: {path}")
    print("final-results archive validation passed")
    return 0


def _parser() -> argparse.ArgumentParser:
    """Define an explicit provider-free archive and validation CLI."""

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--archive-root", type=Path, required=True)
    build_parser.add_argument("--current-method-root", type=Path, required=True)
    build_parser.add_argument("--current-judge-root", type=Path, required=True)
    build_parser.add_argument("--baseline-method-root", type=Path, required=True)
    build_parser.add_argument("--baseline-judge-composite", type=Path, required=True)
    build_parser.add_argument("--baseline-cost-audit", type=Path, required=True)
    build_parser.add_argument("--ledger", type=Path, required=True)
    build_parser.add_argument("--registry", type=Path, required=True)
    build_parser.add_argument("--source-catalog", type=Path, required=True)
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--archive-root", type=Path, required=True)
    validate_parser.add_argument(
        "--repository-root",
        type=Path,
        help="Optional checked-out repository root for archive-relative Markdown and witness references when the evaluator is installed outside that checkout.",
    )
    recompute_parser = subparsers.add_parser("recompute")
    recompute_parser.add_argument("--archive-root", type=Path, required=True)
    finalize_parser = subparsers.add_parser("finalize")
    finalize_parser.add_argument("--archive-root", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the explicitly selected provider-free archive operation."""

    args = _parser().parse_args(argv)
    if args.command == "build":
        return build(args)
    if args.command == "finalize":
        return finalize(args)
    if args.command == "recompute":
        return recompute(args)
    return validate(args)


if __name__ == "__main__":
    raise SystemExit(main())
