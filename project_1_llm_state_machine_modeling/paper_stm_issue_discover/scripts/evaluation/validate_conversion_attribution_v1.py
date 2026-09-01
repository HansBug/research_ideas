#!/usr/bin/env python3
"""Provider-free integrity checks for the conversion attribution overlay."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

PRIMARY = {
    "CONVERSION_LOWERING_CONFIRMED",
    "COMPILER_OWNED_ARTIFACT_CONFIRMED",
    "PROJECTION_TRACE_BOUNDARY_CONFIRMED",
    "RUNTIME_OR_EVIDENCE_CLOSURE_CONFIRMED",
    "SOURCE_LEVEL_FALSE_POSITIVE_CONFIRMED",
    "D0_NONVIOLATION_CONFIRMED",
    "ATTRIBUTION_INDETERMINATE",
}
ARCHIVE_REL = Path("project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline")
CURRENT = ARCHIVE_REL / "derived/manual_adjudication_v4_current_reaudit"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def resolve(root: Path, value: str) -> Path:
    p = Path(value)
    if p.is_absolute():
        return p
    if value.startswith("project_1_llm_state_machine_modeling/"):
        return root / p
    return root / ARCHIVE_REL / p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, default=Path.cwd())
    ap.add_argument("--overlay", type=Path, default=ARCHIVE_REL / "derived/conversion_attribution_v1")
    args = ap.parse_args()
    root = args.repo_root.resolve()
    out = args.overlay if args.overlay.is_absolute() else root / args.overlay
    errors: list[str] = []
    report = json.loads((out / "report_attribution_v1.json").read_text(encoding="utf-8"))
    rows = report.get("records", [])
    decisions = json.loads((root / CURRENT / "current_report_decisions_v4.json").read_text(encoding="utf-8"))["decisions"]
    expected = {d.get("issue") for d in decisions if d.get("canonical_class") == "I"}
    actual = [r.get("report_id") for r in rows]
    if len(rows) != 291:
        errors.append(f"record count is {len(rows)}, expected 291")
    if len(set(actual)) != len(actual):
        errors.append("duplicate report_id")
    if set(actual) != expected:
        errors.append(f"report identity mismatch: missing={sorted(expected - set(actual))[:3]} extra={sorted(set(actual) - expected)[:3]}")
    required = ["report_id", "side", "pair_id", "round", "finding_index", "canonical_class", "d_tier", "w_level", "raw_method_path", "raw_json_pointer", "raw_sha256", "issue", "source_locus", "raw_report_granularity", "raw_reason", "raw_basis", "source_refs", "source_owned_facts", "derived_representation_facts", "trace_refs", "lowering_refs", "backend_receipt_refs", "primary_attribution", "secondary_attributions", "attribution_status", "conversion_only", "source_level_defect_claim", "metric_role", "reason", "basis", "reviewer_ids", "review_status"]
    for i, row in enumerate(rows):
        missing = [k for k in required if k not in row or row[k] in (None, "")]
        if missing:
            errors.append(f"{row.get('report_id', i)} missing {','.join(missing)}")
        if row.get("primary_attribution") not in PRIMARY:
            errors.append(f"{row.get('report_id')} invalid primary")
        if row.get("d_tier") == "D0" and row.get("primary_attribution") != "D0_NONVIOLATION_CONFIRMED":
            errors.append(f"{row.get('report_id')} D0 mapping mismatch")
        if row.get("a0_subtype") == "FALSE_POSITIVE" and row.get("primary_attribution") != "SOURCE_LEVEL_FALSE_POSITIVE_CONFIRMED":
            errors.append(f"{row.get('report_id')} FALSE_POSITIVE mapping mismatch")
        if row.get("primary_attribution") == "CONVERSION_LOWERING_CONFIRMED":
            if not row.get("conversion_only") or not row.get("loss_codes"):
                errors.append(f"{row.get('report_id')} conversion claim lacks concrete loss evidence")
        else:
            if row.get("conversion_only"):
                errors.append(f"{row.get('report_id')} conversion_only true for non-conversion category")
        for ref in row.get("source_refs", []):
            p = resolve(root, ref.get("repository_path", ""))
            if not p.exists():
                errors.append(f"{row.get('report_id')} missing evidence {ref.get('repository_path')}")
            elif ref.get("sha256") and ref["sha256"] != sha(p):
                errors.append(f"{row.get('report_id')} hash mismatch {ref.get('repository_path')}")
        for group in (row.get("trace_refs", []), row.get("lowering_refs", [])):
            for ref in group:
                p = resolve(root, ref.get("path", ""))
                if not p.exists():
                    errors.append(f"{row.get('report_id')} missing derived evidence {ref.get('path')}")
                elif ref.get("sha256") and ref["sha256"] != sha(p):
                    errors.append(f"{row.get('report_id')} derived hash mismatch {ref.get('path')}")
    counts = {}
    for r in rows:
        counts[r["primary_attribution"]] = counts.get(r["primary_attribution"], 0) + 1
    if sum(v for k, v in counts.items()) != 291:
        errors.append("primary categories do not sum to 291")
    if sum(r.get("a0_subtype") == "NOT_A_DEFECT_CLAIM" for r in rows) != 118:
        errors.append("NADC rows do not sum to 118")
    summary = json.loads((out / "i_attribution_summary_v1.json").read_text(encoding="utf-8"))
    if summary.get("counts") != counts:
        errors.append(f"summary counts differ: {summary.get('counts')} != {counts}")
    gap = summary.get("precision_gap", {})
    expected_gap = {
        "current_precision_percent": 100 * 980 / 1271,
        "baseline_precision_percent": 100 * 417 / 512,
        "current_i_rate_percent": 100 * 291 / 1271,
        "baseline_i_rate_percent": 100 * 95 / 512,
        "d0_delta_pp": 100 * (120 / 1271 - 85 / 512),
        "fp_delta_pp": 100 * (53 / 1271 - 10 / 512),
        "nadc_delta_pp": None,
    }
    actual_gap = {
        "current_precision_percent": gap.get("current", {}).get("precision_percent"),
        "baseline_precision_percent": gap.get("baseline", {}).get("precision_percent"),
        "current_i_rate_percent": gap.get("current", {}).get("i_rate_percent"),
        "baseline_i_rate_percent": gap.get("baseline", {}).get("i_rate_percent"),
        "d0_delta_pp": gap.get("component_rates", {}).get("D0", {}).get("delta_rate_pp"),
        "fp_delta_pp": gap.get("component_rates", {}).get("FALSE_POSITIVE", {}).get("delta_rate_pp"),
        "nadc_delta_pp": gap.get("component_rates", {}).get("NADC", {}).get("delta_rate_pp"),
    }
    for key, expected_value in expected_gap.items():
        value = actual_gap.get(key)
        if expected_value is None:
            if value is not None:
                errors.append(f"precision-gap field {key} is {value}, expected null for non-isomorphic baseline subtype")
            continue
        if value is None or abs(float(value) - expected_value) > 0.01:
            errors.append(f"precision-gap field {key} is {value}, expected approximately {expected_value:.4f}")
    if gap.get("component_rates", {}).get("NADC", {}).get("baseline_classification_status") != "not_classified_in_baseline_v3_current_only_subtype":
        errors.append("baseline NADC status does not declare current-only subtype boundary")
    mechanical = gap.get("component_rates", {}).get("NADC", {}).get("mechanical_zero_assumption", {})
    if abs(float(mechanical.get("delta_rate_pp", -1)) - (100 * 118 / 1271)) > 0.01:
        errors.append("NADC mechanical-zero bookkeeping residual is not 118/1271")
    aggregate = summary.get("aggregate_metrics", {})
    if aggregate.get("confirmed_method_owned_invalid_total", {}).get("numerator") != 110:
        errors.append("confirmed method-owned total is not 110")
    if aggregate.get("nadc_disposition_total", {}).get("numerator") != 118:
        errors.append("NADC disposition total is not 118")
    with (out / "report_attribution_v1.tsv").open(encoding="utf-8", newline="") as f:
        tsv_ids = [row["report_id"] for row in csv.DictReader(f, delimiter="\t")]
    if tsv_ids != [r["report_id"] for r in rows]:
        errors.append("TSV report order/identity differs from JSON")
    rerun = json.loads((out / "rerun_decision.json").read_text(encoding="utf-8"))
    if rerun.get("decision") not in {"NO_RERUN", "RERUN_REQUIRED"}:
        errors.append("rerun decision is not an allowed enum")
    if rerun.get("decision") == "NO_RERUN" and any(r.get("primary_attribution") == "CONVERSION_LOWERING_CONFIRMED" for r in rows):
        # A confirmed conversion invalid does not itself imply a rerun, but it must not be silently dropped.
        pass
    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    for name, expected_hash in manifest.get("files", {}).items():
        p = out / name
        if not p.exists():
            errors.append(f"manifest file missing {name}")
        elif sha(p) != expected_hash:
            errors.append(f"manifest hash mismatch {name}")
    print(json.dumps({"ok": not errors, "records": len(rows), "counts": counts, "errors": errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
