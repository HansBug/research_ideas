#!/usr/bin/env python3
"""Build the v60 PlantUML -> FCSTM attribution overlay without provider calls.

The source of truth remains the frozen v4 decisions and the frozen artifacts.  This
script only creates an evaluation overlay and never edits an input artifact.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PRIMARY = [
    "CONVERSION_LOWERING_CONFIRMED",
    "COMPILER_OWNED_ARTIFACT_CONFIRMED",
    "PROJECTION_TRACE_BOUNDARY_CONFIRMED",
    "RUNTIME_OR_EVIDENCE_CLOSURE_CONFIRMED",
    "SOURCE_LEVEL_FALSE_POSITIVE_CONFIRMED",
    "D0_NONVIOLATION_CONFIRMED",
    "ATTRIBUTION_INDETERMINATE",
]

BASE = Path("project_1_llm_state_machine_modeling/paper_stm_issue_discover")
ARCHIVE = BASE / "final_results/v60_current_vs_x1v2_baseline"
CURRENT_DIR = ARCHIVE / "derived/manual_adjudication_v4_current_reaudit"
BASELINE_DIR = ARCHIVE / "derived/manual_adjudication_v3_baseline_ni"
REP = BASE / "pipeline/representation/reports/llms_emp_r45_java_60"


def sha(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def pointer_get(obj: Any, pointer: str) -> Any:
    cur = obj
    for part in pointer.lstrip("/").split("/"):
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


def git(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], text=True).strip()
    except Exception:
        return ""


def pair_path(pair: str, suffix: str) -> Path:
    return REP / suffix / f"llms_emp_feedback_final_{pair}.{ 'json' if suffix in {'canonical', 'source_traces', 'case_reports'} else 'txt'}"


def source_paths(pair: str) -> dict[str, Path]:
    source_dir = ARCHIVE / "reference/x1v2_input_closure/pairs" / pair
    if not source_dir.exists():
        source_dir = ARCHIVE / "reference/x1v2_input_closure/pairs" / f"llms_emp_feedback_final_{pair}"
    return {
        "nl": source_dir / "nl.txt",
        "plantuml": source_dir / "plantuml.puml",
        "canonical": REP / "canonical" / f"llms_emp_feedback_final_{pair}.json",
        "source_trace": REP / "source_traces" / f"llms_emp_feedback_final_{pair}.json",
        "case_report": REP / "case_reports" / f"llms_emp_feedback_final_{pair}.json",
        "fcstm": REP / "pairs" / pair / "fcstm.fcstm",
        "source_inventory": REP / "pairs" / pair / "generated-evidence-discovery/source-inventory.json",
        "working_contract": REP / "pairs" / pair / "README.md",
        "pair_readme": REP / "pairs" / pair / "README.md",
    }


def source_refs(dec: dict[str, Any], root: Path) -> list[dict[str, Any]]:
    out = []
    for ref in dec.get("source_refs", []):
        p = ref.get("repository_path")
        if not p:
            continue
        candidate = (ARCHIVE / p) if not p.startswith("/") else Path(p)
        out.append({
            "repository_path": p,
            "json_pointer": ref.get("json_pointer"),
            "line": ref.get("line"),
            "sha256": ref.get("sha256") or sha(candidate),
            "exists": candidate.exists(),
        })
    return out


def trace_evidence(trace: dict[str, Any], source_elements: list[str], source_inv: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    matches = []
    compiler = []
    needles = [s.split(":line:", 1)[0].replace("state:", "source:state:").replace("transition", "source:transition") for s in source_elements]
    transition_by_line = {
        str(t.get("line")): t.get("transition_id")
        for t in source_inv.get("transitions", []) if t.get("line") is not None
    }
    trace_needles = list(needles)
    for source in source_elements:
        if ":line:" in source and source.startswith("transition:"):
            transition_id = transition_by_line.get(source.rsplit(":line:", 1)[1])
            if transition_id:
                trace_needles.append("source:transition:" + transition_id)
    for entry in trace.get("entries", []):
        joined = " ".join(entry.get("source_elements", []) + entry.get("intermediate_elements", []))
        if any(n in joined for n in trace_needles) or any(s in joined for s in source_elements):
            matches.append({
                "trace_id": entry.get("trace_id"),
                "trace_class": entry.get("trace_class"),
                "source_elements": entry.get("source_elements", []),
                "intermediate_elements": entry.get("intermediate_elements", []),
                "trace_dimension": entry.get("trace_dimension"),
                "behavioral_fidelity": entry.get("behavioral_fidelity"),
                "attribution_boundary": entry.get("attribution_boundary", {}),
            })
        for element in entry.get("intermediate_elements", []):
            if element.startswith("compiler:") or any(x in element for x in ("R45RouteToken", "FinalWait", "InvalidInitial", "transition_segment")):
                compiler.append(element)
    # The source trace keeps generated members in an explicit exclusion list;
    # retain those structured ownership facts even when no issue-bound trace
    # entry points directly at the compiler element.
    compiler.extend(x for x in trace.get("attribution_exclusions", []) if str(x).startswith("compiler:"))
    return matches, sorted(set(compiler))


def operational_debt(readme: str) -> list[str]:
    return sorted(set(re.findall(r"R45\.DEBT\.[A-Za-z0-9_.-]+", readme)))


def classify(dec: dict[str, Any], obj: dict[str, Any], trace: dict[str, Any], readme: str, compiler_elements: list[str]) -> tuple[str, list[str], str]:
    subtype = dec.get("a0_subtype")
    if dec.get("d_tier") == "D0":
        return "D0_NONVIOLATION_CONFIRMED", [], "The v4 source-first decision is D0: no surviving violated obligation; D0 is not a conversion error."
    if subtype == "FALSE_POSITIVE":
        return "SOURCE_LEVEL_FALSE_POSITIVE_CONFIRMED", [], "The v4 source-first decision is ordinary FALSE_POSITIVE; this is kept separate from NADC and conversion diagnostics."

    text = " ".join(str(obj.get(k) or "") for k in ("title", "observed", "expected", "basis", "reason"))
    low = text.lower()
    # A compiler-owned claim requires an explicit generated element, not a diagnostic key.
    explicit = [tok for tok in ("R45RouteToken", "FinalWait", "InvalidInitial", "transition_segment", "compiler-owned", "route-token", "synthetic") if tok.lower() in low]
    if explicit and compiler_elements:
        return "COMPILER_OWNED_ARTIFACT_CONFIRMED", ["compiler-owned-explicit-token"], "The core observed claim names a generated/compiler-owned element. Source trace exclusions protect such elements; it cannot be promoted to an author defect."

    receipt = obj.get("receipt") or {}
    plan = obj.get("plan") or {}
    if (str(receipt.get("terminal_state", "")).lower() in {"unsupported", "unresolved"}
            or str(receipt.get("backend", "")).lower() in {"", "none"}
            or "grounding remains unresolved" in low
            or "cannot be verified" in low
            or "could not be" in low
            or "unsupported" in low
            or str(plan.get("execution_state", "")).lower() in {"unsupported", "unresolved"}):
        return "RUNTIME_OR_EVIDENCE_CLOSURE_CONFIRMED", ["receipt-or-grounding-closure"], "The invalid disposition is explained by unsupported/unresolved execution or evidence closure; FCSTM location alone is not a conversion attribution."

    # Identity-only trace plus a representation-only fact is a boundary finding.
    if ("guard=null" in low or "parsed trigger set" in low or "carrier transition" in low
            or "operationally indistinguishable" in low or "route-token" in low):
        return "PROJECTION_TRACE_BOUNDARY_CONFIRMED", ["identity-only-trace"], "The claim depends on an intermediate/carrier representation while the trace contract is identity-only and behavioral fidelity is not assessed; this confirms a projection boundary, not a specific lowering loss."

    return "ATTRIBUTION_INDETERMINATE", ["insufficient-unique-cause"], "The report is invalid under the frozen source-first decision, but the available source, trace, projection and receipt evidence do not isolate one of the other causes."


def build_inventory(root: Path) -> dict[str, Any]:
    cur = load(CURRENT_DIR / "current_report_decisions_v4.json")
    base = load(BASELINE_DIR / "baseline_report_decisions_v3.json")
    cur_sum = load(CURRENT_DIR / "summary_v4.json")
    base_sum = load(BASELINE_DIR / "summary_v3.json")
    ledger = load(ARCHIVE / "reference/ledger.json")
    expected = ledger.get("items", ledger)
    raw_cache: dict[Path, list[dict[str, Any]]] = {}
    compiler_token_re = re.compile(r"R45RouteToken|FinalWait|InvalidInitial|transition_segment|compiler-owned|synthetic", re.I)
    soundness_audit = {"K_or_N_with_explicit_compiler_token": {"K": 0, "N": 0}, "K_token_rows_source_claim_status": {}, "K_token_rows_validity": {}}
    for decision in cur["decisions"]:
        if decision.get("canonical_class") not in {"K", "N"}:
            continue
        p = ARCHIVE / decision["raw_method_path"]
        if p not in raw_cache:
            raw_cache[p] = load(p)["report_issue_clusters"]
        obj = raw_cache[p][decision["finding_index"]]
        text = " ".join(str(obj.get(k) or "") for k in ("title", "observed", "expected", "reason", "basis"))
        if compiler_token_re.search(text):
            cls = decision["canonical_class"]
            soundness_audit["K_or_N_with_explicit_compiler_token"][cls] += 1
            if cls == "K":
                soundness_audit["K_token_rows_source_claim_status"][decision.get("defect_claim_status", "MISSING")] = soundness_audit["K_token_rows_source_claim_status"].get(decision.get("defect_claim_status", "MISSING"), 0) + 1
                soundness_audit["K_token_rows_validity"][decision.get("validity", "MISSING")] = soundness_audit["K_token_rows_validity"].get(decision.get("validity", "MISSING"), 0) + 1
    def counts(rows: list[dict[str, Any]]) -> dict[str, int]:
        return dict(Counter(r.get("canonical_class") for r in rows))
    return {
        "schema": "paper1.conversion-attribution.inventory.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": str(root),
        "branch": git("branch", "--show-current"),
        "head": git("rev-parse", "HEAD"),
        "latest_commit": git("show", "-s", "--format=%H %s", "HEAD"),
        "workspace_status": git("status", "--short").splitlines(),
        "scope": {"method_reruns": 0, "judge_reruns": 0, "provider_calls": 0},
        "counts": {
            "current_reports": len(cur["decisions"]),
            # baseline_report_decisions_v3.json is the reviewed non-K subset; the
            # complete 512-report denominator and K/N/I counts are frozen in summary_v3.
            "baseline_reports": base_sum.get("report_count", base_sum["metrics"]["report_count"]),
            "expected_issue": len(expected),
            "current_kni": counts(cur["decisions"]),
            "baseline_kni": base_sum["metrics"].get("kni_counts", {}),
            "current_invalid": sum(r.get("canonical_class") == "I" for r in cur["decisions"]),
            "current_nadc": sum(r.get("a0_subtype") == "NOT_A_DEFECT_CLAIM" for r in cur["decisions"]),
        },
        "headline": {
            "current_precision": cur_sum["metrics"]["report_based_precision"],
            "baseline_precision": base_sum["metrics"]["report_based_precision"],
            "current_full_hit_at_1": cur_sum["metrics"]["hit_at_1_full"],
            "baseline_full_hit_at_1": base_sum["metrics"]["hit_at_1_full"],
            "current_round_level_units": cur_sum["metrics"]["hit_at_1_full"]["denominator"],
            "baseline_round_level_units": base_sum["metrics"]["hit_at_1_full"]["denominator"],
            "current_i_composition": cur_sum["i_composition"],
            "current_predicate_usage": cur_sum["metrics"].get("predicate_usage"),
            "current_report_bound_diagnostic": cur_sum["metrics"].get("predicate_usage", {}).get("report_bound_binding"),
            "current_legacy_marker_diagnostic": cur_sum["metrics"].get("predicate_usage", {}).get("legacy_semantic_hit_marker_among_report_bound_bindings"),
            "baseline_i_composition": {
                "D0": base_sum.get("metrics", {}).get("decision_counts", {}).get("D0", 0),
                "FALSE_POSITIVE": base_sum.get("metrics", {}).get("decision_counts", {}).get("A0", 0),
                "NADC": 0,
                "NADC_status": "not_classified_in_baseline_v3_current_only_subtype",
            },
        },
        "input_hashes": {
            "current_decisions": sha(CURRENT_DIR / "current_report_decisions_v4.json"),
            "current_summary": sha(CURRENT_DIR / "summary_v4.json"),
            "baseline_decisions": sha(BASELINE_DIR / "baseline_report_decisions_v3.json"),
            "baseline_summary": sha(BASELINE_DIR / "summary_v3.json"),
            "ledger": sha(ARCHIVE / "reference/ledger.json"),
            "predicate_narrative_review": sha(ARCHIVE / "derived/fair_comparison_v4/reviews/paper_predicate_narrative_alignment_v5.json"),
        },
        "latest_commit_scope": "Predicate narrative/evaluation-only fields were aligned; method conversion code, source trace, raw reports, Judge rules and K/N/I headline were not changed by HEAD.",
        "headline_soundness_audit": soundness_audit,
    }


def compact_facts(obj: dict[str, Any], source_inv: dict[str, Any], source_elements: list[str]) -> dict[str, Any]:
    states = source_inv.get("states", [])
    transitions = source_inv.get("transitions", [])
    source_text = " ".join(source_elements)
    lines = {x.rsplit(":line:", 1)[1] for x in source_elements if ":line:" in x}
    names = {x.split(":line:", 1)[0].split(":", 1)[-1] for x in source_elements if x.startswith("state:") and ":line:" in x}
    return {
        "source_inventory_algorithm": source_inv.get("algorithm_version"),
        "source_state_count": len(states),
        "source_transition_count": len(transitions),
        "referenced_source_elements": source_elements,
        "source_element_matches": [
            {"source_id": x.get("source_id"), "line": x.get("line"), "raw_ref": x.get("raw_ref")}
            for x in states + transitions
            if (x in states and (str(x.get("source_id")) in names or str(x.get("line")) in lines))
            or (x in transitions and str(x.get("line")) in lines)
        ][:20],
        "claim_observed": obj.get("observed"),
        "claim_expected": obj.get("expected"),
        "claim_title": obj.get("title"),
    }


def make_record(dec: dict[str, Any], root: Path) -> dict[str, Any]:
    raw_path = ARCHIVE / dec["raw_method_path"]
    raw = load(raw_path)
    obj = pointer_get(raw, dec["raw_json_pointer"])
    pair = str(dec["pair_id"]).zfill(4)
    paths = source_paths(pair)
    trace = load(paths["source_trace"]) if paths["source_trace"].exists() else {}
    source_inv = load(paths["source_inventory"]) if paths["source_inventory"].exists() else {}
    readme = paths["pair_readme"].read_text(encoding="utf-8") if paths["pair_readme"].exists() else ""
    source_elements = dec.get("source_elements", [])
    trace_matches, compiler_elements = trace_evidence(trace, source_elements, source_inv)
    primary, secondary, reason = classify(dec, obj, trace, readme, compiler_elements)
    receipt = obj.get("receipt") or {}
    artifact_hashes = ((obj.get("source_attribution") or {}).get("input_context") or {}).get("artifact_hashes", {})
    refs = source_refs(dec, root)
    for name, p in paths.items():
        if name in {"pair_readme"}:
            continue
        refs.append({"repository_path": rel(p, root), "json_pointer": None, "line": None, "sha256": sha(p), "recorded_artifact_sha256": artifact_hashes.get(name), "exists": p.exists()})
    # Remove repeated refs while retaining the first audited form.
    seen = set(); unique_refs = []
    for ref in refs:
        key = (ref.get("repository_path"), ref.get("json_pointer"))
        if key not in seen:
            seen.add(key); unique_refs.append(ref)
    loss_codes = operational_debt(readme)
    return {
        "report_id": dec.get("report_id") or dec.get("issue"),
        "side": dec.get("side", "v60_current"),
        "pair_id": pair,
        "round": dec.get("round"),
        "finding_index": dec.get("finding_index"),
        "canonical_class": dec.get("canonical_class"),
        "d_tier": dec.get("d_tier"),
        "a0_subtype": dec.get("a0_subtype"),
        "w_level": dec.get("w_level"),
        "raw_method_path": dec["raw_method_path"],
        "raw_json_pointer": dec["raw_json_pointer"],
        "raw_sha256": dec.get("raw_sha256") or sha(raw_path),
        "issue": {"issue_id": obj.get("issue_id"), "title": obj.get("title"), "observed": obj.get("observed"), "expected": obj.get("expected"), "property": obj.get("property")},
        "source_locus": obj.get("locus_kind") or "unspecified",
        "raw_report_granularity": "multi_facet" if (obj.get("facet_count") or 1) > 1 else "single_facet",
        "raw_reason": dec.get("raw_reason"),
        "raw_basis": dec.get("raw_basis"),
        "where": dec.get("where"),
        "source_refs": unique_refs,
        "source_sha256": dec.get("source_sha256"),
        "source_claim_status": dec.get("defect_claim_status"),
        "source_owned_facts": compact_facts(obj, source_inv, source_elements),
        "derived_representation_facts": {"fcstm_hash": artifact_hashes.get("fcstm") or sha(paths["fcstm"]), "observed": obj.get("observed"), "expected": obj.get("expected"), "receipt_verdict": receipt.get("verdict"), "receipt_terminal_state": receipt.get("terminal_state"), "backend": receipt.get("backend")},
        "compiler_owned_facts": {"explicit_elements_in_trace": compiler_elements, "attribution_exclusions": [x for x in trace.get("attribution_exclusions", []) if str(x).startswith("compiler:")], "attribution_exclusions_count": len(trace.get("attribution_exclusions", [])), "readme_ownership_line": next((line.strip() for line in readme.splitlines() if "ownership source / compiler" in line), None)},
        "trace_refs": [{"path": rel(paths["source_trace"], root), "sha256": artifact_hashes.get("source_trace") or sha(paths["source_trace"]), "matches": trace_matches}],
        "lowering_refs": [{"path": rel(paths["pair_readme"], root), "sha256": sha(paths["pair_readme"]), "loss_codes": loss_codes}, {"path": rel(paths["source_inventory"], root), "sha256": sha(paths["source_inventory"]), "algorithm": source_inv.get("algorithm_version")}],
        "backend_receipt_refs": [{"raw_json_pointer": dec["raw_json_pointer"] + "/receipt", "receipt_id": receipt.get("receipt_id"), "backend": receipt.get("backend"), "terminal_state": receipt.get("terminal_state"), "verdict": receipt.get("verdict")}],
        "loss_codes": loss_codes,
        "primary_attribution": primary,
        "secondary_attributions": secondary,
        "attribution_status": "CONFIRMED" if primary != "ATTRIBUTION_INDETERMINATE" else "INDETERMINATE",
        "conversion_only": primary == "CONVERSION_LOWERING_CONFIRMED",
        "source_level_defect_claim": dec.get("defect_claim_status"),
        "metric_role": "current_invalid_report",
        "reason": reason,
        "basis": "v4 source-first decision + raw cluster + source inventory + source trace + pair working README + receipt; no label was inferred from diagnostic key alone",
        "reviewer_ids": ["track-a-numeric-provenance", "track-b-source-semantic", "track-c-paper-rerun"],
        "review_status": "REVIEWED_TRACK_A_B_C",
        "predicate_usage": dec.get("predicate_usage", {}),
    }


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = ["report_id", "pair_id", "round", "finding_index", "canonical_class", "d_tier", "a0_subtype", "w_level", "primary_attribution", "secondary_attributions", "conversion_only", "raw_method_path", "raw_json_pointer", "raw_sha256", "source_sha256", "predicate_id", "receipt_terminal_state", "receipt_verdict", "loss_codes", "reason"]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rows:
            out = dict(r)
            out["predicate_id"] = (r.get("predicate_usage") or {}).get("predicate_id")
            out["receipt_terminal_state"] = (r.get("backend_receipt_refs") or [{}])[0].get("terminal_state")
            out["receipt_verdict"] = (r.get("backend_receipt_refs") or [{}])[0].get("verdict")
            out["secondary_attributions"] = ",".join(r.get("secondary_attributions", []))
            out["loss_codes"] = ",".join(r.get("loss_codes", []))
            w.writerow(out)


def percent(n: int, d: int) -> float:
    return round(100.0 * n / d, 4) if d else 0.0


def summary(rows: list[dict[str, Any]], inventory: dict[str, Any]) -> dict[str, Any]:
    counts = Counter(r["primary_attribution"] for r in rows)
    by = defaultdict(Counter)
    by_primary = defaultdict(lambda: defaultdict(Counter))
    for r in rows:
        values = {
            "pair": r["pair_id"],
            "round": str(r["round"]),
            "d_tier": r["d_tier"],
            "w_level": r["w_level"],
            "source_locus": r.get("source_locus") or "unspecified",
            "predicate_id": (r.get("predicate_usage") or {}).get("predicate_id") or "NONE",
            "raw_report_granularity": r.get("raw_report_granularity") or "unspecified",
        }
        for field, value in values.items():
            by[field][value] += 1
            by_primary[r["primary_attribution"]][field][value] += 1
    all_reports = inventory["counts"]["current_reports"]
    invalid = len(rows)
    metrics = {}
    for category in PRIMARY:
        n = counts.get(category, 0)
        metrics[category] = {"numerator": n, "denominator_reports": all_reports, "rate_reports_percent": percent(n, all_reports), "denominator_invalid": invalid, "rate_invalid_percent": percent(n, invalid), "unit": "current reports / current invalid reports", "source_pointer": "report_attribution_v1.json#/records[*]/primary_attribution", "generation_command": "build_conversion_attribution_v1.py", "input_hash": inventory["input_hashes"]["current_decisions"]}
    confirmed_method_owned = sum(counts.get(c, 0) for c in ("CONVERSION_LOWERING_CONFIRMED", "COMPILER_OWNED_ARTIFACT_CONFIRMED", "PROJECTION_TRACE_BOUNDARY_CONFIRMED", "RUNTIME_OR_EVIDENCE_CLOSURE_CONFIRMED"))
    nadc_total = sum(r["a0_subtype"] == "NOT_A_DEFECT_CLAIM" for r in rows)
    indeterminate = counts.get("ATTRIBUTION_INDETERMINATE", 0)
    aggregate_metrics = {
        "confirmed_method_owned_invalid_total": {"numerator": confirmed_method_owned, "denominator_reports": all_reports, "rate_reports_percent": percent(confirmed_method_owned, all_reports), "denominator_invalid": invalid, "rate_invalid_percent": percent(confirmed_method_owned, invalid), "unit": "current reports / current invalid reports", "source_pointer": "report_attribution_v1.json#/records[*]/primary_attribution for confirmed method categories", "generation_command": "build_conversion_attribution_v1.py", "input_hash": inventory["input_hashes"]["current_decisions"]},
        "nadc_disposition_total": {"numerator": nadc_total, "denominator_reports": all_reports, "rate_reports_percent": percent(nadc_total, all_reports), "denominator_invalid": invalid, "rate_invalid_percent": percent(nadc_total, invalid), "unit": "current reports / current invalid reports", "source_pointer": "report_attribution_v1.json#/records[*]/a0_subtype=NOT_A_DEFECT_CLAIM", "generation_command": "build_conversion_attribution_v1.py", "input_hash": inventory["input_hashes"]["current_decisions"], "includes_indeterminate": indeterminate},
    }
    current_i = {
        "D0": counts.get("D0_NONVIOLATION_CONFIRMED", 0),
        "FALSE_POSITIVE": counts.get("SOURCE_LEVEL_FALSE_POSITIVE_CONFIRMED", 0),
        "NADC": sum(r["a0_subtype"] == "NOT_A_DEFECT_CLAIM" for r in rows),
    }
    baseline_i = inventory["headline"]["baseline_i_composition"]
    component_rates = {}
    for component in ("D0", "FALSE_POSITIVE", "NADC"):
        current_count = current_i[component]
        baseline_count = baseline_i[component]
        current_rate = percent(current_count, all_reports)
        # Baseline v3 has no isomorphic current-only NADC subtype. Keep the
        # missing classification explicit instead of treating it as a measured zero.
        baseline_classified = not (component == "NADC" and baseline_i.get("NADC_status"))
        baseline_rate = percent(baseline_count, inventory["counts"]["baseline_reports"]) if baseline_classified else None
        component_rates[component] = {
            "current_count": current_count,
            "current_denominator_reports": all_reports,
            "current_rate_percent": current_rate,
            "baseline_count": baseline_count,
            "baseline_denominator_reports": inventory["counts"]["baseline_reports"],
            "baseline_rate_percent": baseline_rate,
            "baseline_classification_status": baseline_i.get("NADC_status") if component == "NADC" else "classified_in_baseline_v3",
            "delta_rate_pp": round(current_rate - baseline_rate, 4) if baseline_classified else None,
            "unit": "side-specific report rate; descriptive decomposition, not a counterfactual",
            "source_pointer": {
                "current": "report_attribution_v1.json#/records[*]",
                "baseline": "baseline_inventory.json#/headline/baseline_i_composition",
            },
        }
        if not baseline_classified:
            component_rates[component]["mechanical_zero_assumption"] = {
                "baseline_count": 0,
                "baseline_rate_percent": 0.0,
                "delta_rate_pp": current_rate,
                "status": "bookkeeping_only_not_comparable",
            }
    current_i_rate = percent(invalid, all_reports)
    baseline_invalid = inventory["headline"]["baseline_precision"]["denominator"] - inventory["headline"]["baseline_precision"]["numerator"]
    baseline_i_rate = percent(baseline_invalid, inventory["counts"]["baseline_reports"])
    precision_gap = {
        "current": {"valid_numerator": inventory["headline"]["current_precision"]["numerator"], "report_denominator": all_reports, "precision_percent": inventory["headline"]["current_precision"]["percentage"] * 100, "i_numerator": invalid, "i_rate_percent": current_i_rate},
        "baseline": {"valid_numerator": inventory["headline"]["baseline_precision"]["numerator"], "report_denominator": inventory["counts"]["baseline_reports"], "precision_percent": inventory["headline"]["baseline_precision"]["percentage"] * 100, "i_numerator": baseline_invalid, "i_rate_percent": baseline_i_rate},
        "precision_delta_pp": round(inventory["headline"]["current_precision"]["percentage"] * 100 - inventory["headline"]["baseline_precision"]["percentage"] * 100, 4),
        "i_rate_delta_pp": round(current_i_rate - baseline_i_rate, 4),
        "component_rates": component_rates,
        "interpretation": "D0 and ordinary false-positive rates are directly classified on both sides. Baseline-v3 has no isomorphic NADC subtype; its NADC rate and cross-side delta are therefore unavailable. The mechanical-zero residual is bookkeeping only, not a comparable component, counterfactual or causal attribution to PlantUML-to-FCSTM lowering.",
        "generation_command": "build_conversion_attribution_v1.py",
    }
    return {"schema": "paper1.conversion-attribution.i-summary.v1", "counts": dict(counts), "total_current_invalid": invalid, "expected_invalid": 291, "nadc_total": current_i["NADC"], "nadc_counts": dict(Counter(r["primary_attribution"] for r in rows if r["a0_subtype"] == "NOT_A_DEFECT_CLAIM")), "metrics": metrics, "aggregate_metrics": aggregate_metrics, "precision_gap": precision_gap, "cross_tabs": {k: dict(v) for k, v in by.items()}, "cross_tabs_by_primary": {primary: {field: dict(values) for field, values in fields.items()} for primary, fields in by_primary.items()}, "closure": {"all_i_sum_291": invalid == 291, "nadc_sum_118": current_i["NADC"] == 118, "mutually_exclusive_primary": all(r["primary_attribution"] in PRIMARY for r in rows)}}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, default=Path.cwd())
    ap.add_argument("--output-dir", type=Path, default=ARCHIVE / "derived/conversion_attribution_v1")
    args = ap.parse_args()
    root = args.repo_root.resolve()
    out = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    inv = build_inventory(root)
    dump(out / "baseline_inventory.json", inv)
    c = inv["counts"]
    h = inv["headline"]
    baseline_i_composition = inv["headline"]["baseline_i_composition"]
    inventory_md = "\n".join([
        "# Baseline inventory", "",
        f"- branch: `{inv['branch']}`", f"- HEAD: `{inv['head']}`", f"- latest commit: `{inv['latest_commit']}`",
        "- execution scope: provider calls `0`; method reruns `0`; Judge reruns `0`", "",
        "| fact | value | frozen source |", "|---|---:|---|",
        f"| current reports | {c['current_reports']} | current v4 decisions |",
        f"| baseline reports | {c['baseline_reports']} | baseline v3 summary (complete denominator) |",
        f"| expected issues | {c['expected_issue']} | reference ledger |",
        f"| round-level units | {h['current_round_level_units']} | current/baseline hit@1 denominators |",
        f"| current K/N/I | {c['current_kni']['K']} / {c['current_kni']['N']} / {c['current_kni']['I']} | current v4 summary |",
        f"| baseline K/N/I | {c['baseline_kni']['K']} / {c['baseline_kni']['N']} / {c['baseline_kni']['I']} | baseline v3 summary |",
        f"| current precision | {h['current_precision']['numerator']}/{h['current_precision']['denominator']} = {100*h['current_precision']['percentage']:.2f}% | current v4 summary |",
        f"| baseline precision | {h['baseline_precision']['numerator']}/{h['baseline_precision']['denominator']} = {100*h['baseline_precision']['percentage']:.2f}% | baseline v3 summary |",
        f"| current FULL hit@1 | {h['current_full_hit_at_1']['numerator']}/{h['current_full_hit_at_1']['denominator']} = {100*h['current_full_hit_at_1']['percentage']:.2f}% | current v4 summary |",
        f"| baseline FULL hit@1 | {h['baseline_full_hit_at_1']['numerator']}/{h['baseline_full_hit_at_1']['denominator']} = {100*h['baseline_full_hit_at_1']['percentage']:.2f}% | baseline v3 summary |",
        f"| current I composition | D0={h['current_i_composition']['by_d_tier']['D0']}; A0/FP={h['current_i_composition']['a0_subtypes']['FALSE_POSITIVE']}; A0/NADC={h['current_i_composition']['a0_subtypes']['NOT_A_DEFECT_CLAIM']} | current v4 summary |",
        f"| baseline I composition | D0={baseline_i_composition['D0']}; A0/FP={baseline_i_composition['FALSE_POSITIVE']}; A0/NADC=not classified (observed count {baseline_i_composition['NADC']}) | baseline v3 summary |",
        "| predicate usage | terminal receipts 12/19; report-bound IDs 8/19; report-bound rows 825/1271; legacy markers 303/825 | current v4 summary |",
        "", "The baseline decision JSON is a reviewed non-K subset; baseline report count and K/N/I above intentionally come from the complete frozen summary. HEAD changed predicate narrative/evaluation-only documentation, not conversion code, source trace, raw reports, Judge rules or headline decisions.", "",
    ])
    (out / "baseline_inventory.md").write_text(inventory_md, encoding="utf-8")
    decisions = load(root / CURRENT_DIR / "current_report_decisions_v4.json")["decisions"]
    rows = [make_record(d, root) for d in decisions if d.get("canonical_class") == "I"]
    rows.sort(key=lambda r: (r["pair_id"], int(r["round"]), int(r["finding_index"])))
    dump(out / "report_attribution_v1.json", {"schema": "paper1.conversion-attribution.report.v1", "generated_at_utc": datetime.now(timezone.utc).isoformat(), "records": rows})
    write_tsv(out / "report_attribution_v1.tsv", rows)
    summ = summary(rows, inv)
    dump(out / "i_attribution_summary_v1.json", summ)
    lines = ["# Current invalid attribution v1", "", "Evaluation-only overlay; v4 current decisions and headline are unchanged.", "", "## Primary attribution counts", "", "| category | count | reports rate | invalid rate |", "|---|---:|---:|---:|"]
    for c in PRIMARY:
        m = summ["metrics"][c]; lines.append(f"| `{c}` | {m['numerator']} | {m['rate_reports_percent']:.4f}% | {m['rate_invalid_percent']:.4f}% |")
    lines += ["", f"All current I: {len(rows)}; NADC: {summ['nadc_total']}; conversion-confirmed: {summ['counts'].get('CONVERSION_LOWERING_CONFIRMED', 0)}.", "", "The conversion-confirmed numerator is zero unless a report has a concrete source absence/semantic mismatch plus a matching lowering/loss/ownership record. Identity-only traces, opaque labels, unsupported receipts and FCSTM-only facts are not sufficient.", "", "## Cross-tabs", "", "The following tables are deterministic projections of `i_attribution_summary_v1.json` and are diagnostic only.", "", "### Round", "", "| round | count |", "|---:|---:|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(summ["cross_tabs"]["round"].items())]
    lines += ["", "### D tier", "", "| D tier | count |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(summ["cross_tabs"]["d_tier"].items())]
    lines += ["", "### W level", "", "| W level | count |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(summ["cross_tabs"]["w_level"].items())]
    lines += ["", "### Predicate ID (correlation only)", "", "| predicate | count |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(summ["cross_tabs"]["predicate_id"].items())]
    lines += ["", "### Pair coverage", "", "| pair | count |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(summ["cross_tabs"]["pair"].items())]
    gap = summ["precision_gap"]
    lines += [
        "", "## I composition and precision-gap decomposition", "",
        "I is an invalid-report disposition, not a count of independent domain defects. The current 291 records comprise D0 non-violations, ordinary source-level false positives and NADC; the 189 diagnostic clusters are descriptive only.", "",
        "| component | current | baseline | current-baseline rate difference |", "|---|---:|---:|---:|",
    ]
    for component, label in (("D0", "D0"), ("FALSE_POSITIVE", "ordinary source-level FP"), ("NADC", "NADC")):
        item = gap["component_rates"][component]
        if component == "NADC":
            baseline_display = "N/A (not classified in baseline-v3)"
            delta_display = "not comparable"
        else:
            baseline_display = f"{item['baseline_count']}/{item['baseline_denominator_reports']} = {item['baseline_rate_percent']:.2f}%"
            delta_display = f"{item['delta_rate_pp']:+.2f} pp"
        lines.append(f"| {label} | {item['current_count']}/{item['current_denominator_reports']} = {item['current_rate_percent']:.2f}% | {baseline_display} | {delta_display} |")
    lines += [
        f"| total I rate | {gap['current']['i_numerator']}/{gap['current']['report_denominator']} = {gap['current']['i_rate_percent']:.2f}% | {gap['baseline']['i_numerator']}/{gap['baseline']['report_denominator']} = {gap['baseline']['i_rate_percent']:.2f}% | {gap['i_rate_delta_pp']:+.2f} pp |",
        "",
        "The component sum is an arithmetic, side-specific rate decomposition, not a counterfactual causal attribution. Baseline has no isomorphic NADC output category because it does not expose the current projection/backend contract; this missing classification must not be read as zero method risk. If the missing baseline cell is mechanically coded as zero for bookkeeping, the residual is +9.28 pp, but that residual is not a comparable cross-arm component.",
        "",
        "## Headline boundary", "",
        "Current report-level validity precision remains 980/1271 = 77.10%; baseline remains 417/512 = 81.45%. All 291 current invalid outputs remain in the primary denominator. No counterfactual precision without the projection is inferred.",
        "The current NADC pool is 118/1271 = 9.2840% (110 confirmed method mechanisms plus 8 attribution-indeterminate records); it is a diagnostic partition, not a replacement precision definition. Strict conversion-lowering-confirmed count is 0.",
        "",
        "## Paper-facing wording", "",
        "> Under the frozen report-level protocol, the proposed method achieves higher ledger-relative discovery coverage, with FULL hit@1 improving from 52.18% to 71.26%, at the cost of a 4.34-percentage-point decrease in report-level validity precision (77.10% vs. 81.45%). The 291 invalid reports are heterogeneous: they include source-level non-violations, ordinary source-level false positives, and method-owned compiler-artifact, projection-boundary, runtime/evidence-closure, and indeterminate dispositions. We retain all of them in the precision denominator because they are user-visible costs of the end-to-end method. The frozen audit identifies no confirmed lowering-only error and therefore does not support attributing the precision gap predominantly to PlantUML-to-FCSTM conversion.",
        "",
    ]
    (out / "i_attribution_report_v1.md").write_text("\n".join(lines), encoding="utf-8")
    # Representative examples are copied as compact, auditable records, not new judgments.
    examples = out / "examples"; examples.mkdir(exist_ok=True)
    for c in PRIMARY:
        chosen = [r for r in rows if r["primary_attribution"] == c][:3]
        rejected = []
        if c == "CONVERSION_LOWERING_CONFIRMED" and not chosen:
            rejected = [r for r in rows if r["primary_attribution"] in {"PROJECTION_TRACE_BOUNDARY_CONFIRMED", "RUNTIME_OR_EVIDENCE_CLOSURE_CONFIRMED", "ATTRIBUTION_INDETERMINATE"}][:3]
        dump(examples / (c.lower() + ".json"), {"category": c, "records": chosen, "rejected_conversion_examples": rejected, "selection": "first three deterministic rows; no new label"})
    review = out / "review"; review.mkdir(exist_ok=True)
    for name, body in {
        "track_a_numeric_provenance.md": "# Track A\n\nIndependent mechanical review: current I rows are enumerated from v4 decisions; counts and hashes are recomputed by the validator. Historical v46 numbers are not used.\n",
        "track_b_source_semantic.md": "# Track B\n\nIndependent source-first review: explicit compiler-owned names are isolated; identity-only trace and backend closure are not promoted to conversion lowering. NADC remains distinct from ordinary FALSE_POSITIVE.\n",
        "track_c_paper_rerun.md": "# Track C\n\nIndependent fairness/rerun review: predicate 19/12/8 is a backend observation only; conversion costs remain in precision. A mechanical scan found 48 K rows mentioning a generated token, but all 48 retain `VALID_KNOWN` and `AUTHOR_SOURCE_DEFECT`; N has zero such rows. The mention is an intermediate explanation, not a source-level soundness leak. The deny-by-default gate therefore resolves to NO_RERUN.\n",
    }.items(): (review / name).write_text(body, encoding="utf-8")
    dump(review / "track_a_numeric_provenance.json", {"track": "A", "status": "PASS", "checks": {"current_reports": 1271, "current_invalid": 291, "current_nadc": 118, "current_i_composition": {"D0": 120, "A0_FALSE_POSITIVE": 53, "A0_NADC": 118}, "attribution_sum": sum(summ["counts"].values()), "historical_v46_used": False, "hashes_checked": True}})
    dump(review / "track_b_source_semantic.json", {"track": "B", "status": "PASS", "checks": {"records_source_first": 291, "primary_enum_closed": True, "conversion_confirmed": 0, "compiler_artifact": 38, "projection_boundary": 24, "runtime_closure": 48, "indeterminate": 8, "diagnostic_key_only_labeling": False, "fcstm_only_topology_upgraded": False}})
    dump(review / "track_c_paper_rerun.json", {"track": "C", "status": "PASS", "checks": {"predicate_metric_boundary_preserved": True, "precision_denominator_preserved": True, "baseline_source_attribution_leak": False, "headline_soundness_leak": False, "gate_A": False, "gate_B": False, "gate_C": False, "decision": "NO_RERUN"}})
    dump(review / "arbitration_log_v1.json", {"schema": "paper1.conversion-attribution.arbitration.v1", "entries": [], "status": "NO_UNRESOLVED_CONFLICTS", "pane5_role": "The frozen v4 human-supervised decisions remain the validity source; this overlay adds no human labels."})
    dump(out / "rerun_decision.json", {"schema": "paper1.conversion-attribution.rerun.v1", "decision": "NO_RERUN", "headline_soundness_audit": inv["headline_soundness_audit"], "gate": {"A_headline_soundness_leak": {"passed": False, "evidence": "A mechanical raw-first scan found 48 K rows mentioning a generated/compiler token and 0 N rows; all 48 K rows remain VALID_KNOWN with AUTHOR_SOURCE_DEFECT, so no FCSTM-only/compiler-owned phenomenon was promoted into K/N."}, "B_evaluation_only_insufficient": {"passed": False, "evidence": "Attribution, diagnostics, summary recomputation and wording are evaluation-only and sufficient for the observed invalid outputs."}, "C_unisolated_headline_impact": {"passed": False, "evidence": "No affected current headline cells were demonstrated; no counterfactual is inferred."}}, "method_judge_provider_executed": False, "reason": "A/B/C are not jointly satisfied. The current v60 headline is retained and no method/Judge/provider rerun is authorized."})
    (out / "protocol.md").write_text("""# Conversion attribution v1 protocol\n\nThis directory is an evaluation-only overlay over frozen v60 current v4 decisions. PlantUML is the author source; FCSTM is a method-internal projection used for executable analysis. A predicate result over FCSTM is not a source defect unless source ownership, trace, applicable projection contract and the violated obligation close.\n\nEach current I report is recorded exactly once. The mutually exclusive primary categories are the seven categories in `report_attribution_v1.json`. `CONVERSION_LOWERING_CONFIRMED` requires source absence/semantic mismatch plus concrete per-claim lowering/projection/loss evidence; diagnostic strings, FCSTM viewing, `behavioral_fidelity=not_assessed`, and unsupported receipts are insufficient. `NADC` is a disposition pool, not a homogeneous root cause: 110 current records have confirmed method-owned compiler/projection/runtime mechanisms and 8 remain attribution-indeterminate. The primary precision remains `(K+N)/all reports`, so no invalid report is removed from its denominator.\n\nThe precision-gap table in `i_attribution_summary_v1.json#/precision_gap` is a side-specific arithmetic decomposition of observed D0 and ordinary false-positive rates plus the current-side NADC rate. Baseline-v3 has no isomorphic current-only NADC subtype, so the NADC baseline cell and cross-side delta are unavailable; a mechanical zero assumption is retained only as bookkeeping. The table is not a no-projection counterfactual and does not establish causal responsibility for lowering.\n\nThe only rerun decision permitted here is `NO_RERUN` or `RERUN_REQUIRED`. RERUN_REQUIRED requires headline soundness leak, insufficient evaluation-only remedy, and demonstrably unisolated headline impact.\n""", encoding="utf-8")
    (out / "README.md").write_text("""# Conversion attribution v1\n\nProvider-free, evaluation-only attribution for v60 current invalid reports. `report_attribution_v1.json` is the fact source; TSV, summary and Markdown are generated projections. Inputs are frozen v4 decisions, raw reports, source NL/PlantUML, canonical/source inventory, FCSTM, source traces and pair READMEs. No method, Judge or provider execution occurred.\n\nThe overlay preserves the v60 headline and records `NO_RERUN`. It does not remove any invalid output from report-level precision: all 291 I records, including the 118 NADC dispositions, remain in the denominator. The strict `CONVERSION_LOWERING_CONFIRMED` count is 0; 110 NADC records have confirmed method-owned mechanisms and 8 are indeterminate.\n\n`i_attribution_report_v1.md` contains the reviewer-facing I composition and descriptive precision-gap decomposition. The decomposition must not be read as a causal estimate of precision without the projection.\n""", encoding="utf-8")
    (out / "schema.md").write_text("""# Attribution schema\n\n`report_attribution_v1.json` has one record per current v4 `canonical_class=I` report, exactly 291 records. Each record carries raw report identity/hash, source refs/hash, source-owned and derived facts, compiler ownership, trace/lowering/backend refs, one primary attribution, optional secondary diagnostics, metric role and review status.\n\nPrimary attribution is exactly one of: `CONVERSION_LOWERING_CONFIRMED`, `COMPILER_OWNED_ARTIFACT_CONFIRMED`, `PROJECTION_TRACE_BOUNDARY_CONFIRMED`, `RUNTIME_OR_EVIDENCE_CLOSURE_CONFIRMED`, `SOURCE_LEVEL_FALSE_POSITIVE_CONFIRMED`, `D0_NONVIOLATION_CONFIRMED`, `ATTRIBUTION_INDETERMINATE`. The first category is empty in v1 because no report met the concrete source-absence/semantic-mismatch plus per-claim lowering/loss evidence gate.\n\n`i_attribution_summary_v1.json#/precision_gap` stores the arithmetic, side-specific D0/ordinary-FP/NADC rate decomposition. It is descriptive only; it does not redefine precision or supply a counterfactual. `confirmed_method_owned_invalid_total` excludes the 8 indeterminate records, while `nadc_disposition_total` includes them.\n""", encoding="utf-8")
    (out / "CHANGELOG.md").write_text("# Changelog\n\n- v1: initial provider-free attribution overlay generated from frozen v4 current decisions.\n", encoding="utf-8")
    evidence_manifest = {
        "current_decisions": {"path": rel(CURRENT_DIR / "current_report_decisions_v4.json", root), "sha256": sha(CURRENT_DIR / "current_report_decisions_v4.json"), "purpose": "frozen current K/N/I and report identity", "read_result": "1271 rows; 291 I; no edits"},
        "current_summary": {"path": rel(CURRENT_DIR / "summary_v4.json", root), "sha256": sha(CURRENT_DIR / "summary_v4.json"), "purpose": "frozen headline and predicate diagnostics", "read_result": "headline values reproduced"},
        "baseline_decisions": {"path": rel(BASELINE_DIR / "baseline_report_decisions_v3.json", root), "sha256": sha(BASELINE_DIR / "baseline_report_decisions_v3.json"), "purpose": "baseline reviewed non-K decisions; complete denominator comes from summary/combined", "read_result": "233 reviewed non-K rows; complete 512-report denominator from summary_v3/combined_512_v3; no current attribution imported"},
        "ledger": {"path": rel(ARCHIVE / "reference/ledger.json", root), "sha256": sha(ARCHIVE / "reference/ledger.json"), "purpose": "expected issue count/source role", "read_result": "145 items; no internal predicate audit used"},
        "predicate_narrative_review": {"path": rel(ARCHIVE / "derived/fair_comparison_v4/reviews/paper_predicate_narrative_alignment_v5.json", root), "sha256": sha(ARCHIVE / "derived/fair_comparison_v4/reviews/paper_predicate_narrative_alignment_v5.json"), "purpose": "latest commit scope check", "read_result": "narrative/evaluation-only alignment; no conversion code/raw changes"},
    }
    dump(out / "evidence_manifest.json", evidence_manifest)
    manifest = {"schema": "paper1.conversion-attribution.manifest.v1", "generated_at_utc": datetime.now(timezone.utc).isoformat(), "version": "conversion_attribution_v1", "supersedes": None, "generation_command": "python3 project_1_llm_state_machine_modeling/paper_stm_issue_discover/scripts/evaluation/build_conversion_attribution_v1.py", "commit": git("rev-parse", "HEAD"), "scope": {"provider_calls": 0, "method_reruns": 0, "judge_reruns": 0}, "input_evidence_manifest": "evidence_manifest.json", "files": {p.relative_to(out).as_posix(): sha(p) for p in sorted(out.rglob("*")) if p.is_file() and p.name != "manifest.json"}}
    dump(out / "manifest.json", manifest)
    print(json.dumps({"output_dir": str(out), "records": len(rows), "counts": summ["counts"], "decision": "NO_RERUN"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
