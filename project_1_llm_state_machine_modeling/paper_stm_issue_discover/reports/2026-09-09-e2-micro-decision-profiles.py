#!/usr/bin/env python3
"""Build the compact, redacted audit for E2 observable decision traces.

The script reads only frozen E2 source JSON. It never calls a provider and it
does not modify experiment inputs, prompts, validators, or eligibility rules.
"""

from __future__ import annotations

import collections
import hashlib
import json
import math
from pathlib import Path
from statistics import mean, median


MODELS = ("luna", "sonnet", "qwen", "muse")
BACKBONE_MODELS = ("sonnet", "qwen", "muse")
PAIR_COUNT = 54
ROUND_COUNT = 3

KEEP_KEYS = (
    "issue_id",
    "contract_id",
    "contract_ids",
    "obligation_id",
    "property",
    "expected_direction",
    "violation_direction",
    "locus_kind",
    "locus_names",
    "predicate_id",
    "evidence_types",
    "source_refs",
    "element_refs",
    "requirement_quote",
    "title",
    "observed",
    "reason",
    "basis",
    "strongest_rebuttal",
    "strongest_defeater",
    "grounding",
    "defeater_disposition",
    "defeater_kind",
    "witness_level",
    "coverage_class",
    "issue_emitted",
    "d_level",
)


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in (here, *here.parents):
        if (parent / "project_1_llm_state_machine_modeling").is_dir():
            return parent
    raise RuntimeError("repository root not found")


ROOT = repo_root()
PAPER = ROOT / "project_1_llm_state_machine_modeling" / "paper_stm_issue_discover"
RESULTS = PAPER / "final_results" / "e2_20260907"
RAW = RESULTS / "raw"
LUNA_RESULTS = PAPER / "final_results" / "v61_source_divergence_vs_x1v2_baseline"
LUNA_OURS = LUNA_RESULTS / "raw" / "v61_current" / "method" / "method"
LUNA_BASELINE = PAPER / "final_results" / "v60_current_vs_x1v2_baseline" / "raw" / "x1v2_baseline" / "method"
DERIVED = ROOT / "runs" / "paper1" / "e2_20260907" / "derived"
OUTPUT = DERIVED / "micro_decision_profiles.json"


def relative_source(path, root):
    return f"{root.name}/{path.relative_to(root).as_posix()}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return "sha256:" + digest.hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def compact(value):
    if isinstance(value, dict):
        return {key: value[key] for key in KEEP_KEYS if key in value}
    return value


def text_stats(values):
    lengths = [len(value) for value in values if isinstance(value, str)]
    if not lengths:
        return {"n": 0, "mean": 0, "median": 0, "min": 0, "max": 0}
    return {
        "n": len(lengths),
        "mean": round(mean(lengths), 2),
        "median": median(lengths),
        "min": min(lengths),
        "max": max(lengths),
    }


def normalized_entropy(counts):
    """Return normalized Shannon entropy over non-zero categories."""
    total = sum(counts.values())
    categories = [value for value in counts.values() if value]
    if total == 0 or len(categories) <= 1:
        return 0.0
    entropy = -sum((value / total) * math.log2(value / total) for value in categories)
    return round(entropy / math.log2(len(categories)), 4)


def safe_finish(provider_response):
    if not isinstance(provider_response, dict):
        return None
    return provider_response.get("finish_reason") or provider_response.get("stop_reason")


def usage_item(item):
    if not isinstance(item, dict):
        return {"raw_type": type(item).__name__}
    observed = item.get("observed_usage") or {}
    output_details = item.get("output_token_details") or {}
    return {
        "model_call_id": item.get("model_call_id"),
        "model": item.get("model"),
        "status": item.get("status"),
        "input_tokens": item.get("input_tokens", observed.get("input_tokens")),
        "output_tokens": item.get("output_tokens", observed.get("output_tokens")),
        "reasoning_tokens": item.get("reasoning_tokens", output_details.get("reasoning")),
        "total_tokens": item.get("total_tokens", observed.get("total_tokens")),
        "duration_seconds": item.get("duration_seconds"),
        "time_to_first_chunk_seconds": item.get("time_to_first_chunk_seconds"),
        "finish_reason": safe_finish(item.get("provider_response")),
        "provider_response": item.get("provider_response"),
        "output_budget": item.get("output_budget"),
        "source": item.get("source"),
        "usage_conflict": item.get("usage_conflict"),
    }


def call_summary(call):
    usage = call.get("usage")
    if isinstance(usage, dict):
        usage = [usage]
    if not isinstance(usage, list):
        usage = []
    return {
        "kind": call.get("kind"),
        "status": call.get("status"),
        "real_llm": call.get("real_llm"),
        "schema_validation_failures": call.get("schema_validation_failures", []),
        "attempt_count": len(call.get("attempts", [])) if isinstance(call.get("attempts"), list) else None,
        "usage": [usage_item(item) for item in usage],
    }


def stage_trace(data):
    stages = data.get("stage_outputs", {})
    extraction = stages.get("contract_extraction", {})
    completion = stages.get("contract_completion", {})
    grounding = stages.get("discovery_grounding", {})
    d_stage = stages.get("d_adjudication", {})
    correction = stages.get("validate_d", {})
    branches = []
    for branch in grounding.get("branches", []) or []:
        if not isinstance(branch, dict):
            continue
        branches.append(
            {
                "reason": branch.get("reason"),
                "basis": branch.get("basis"),
                "additional_contracts": [compact(item) for item in branch.get("additional_contracts", []) or []],
            }
        )
    return {
        "contract_extraction": {
            "reason": extraction.get("reason"),
            "basis": extraction.get("basis"),
            "contracts": [compact(item) for item in extraction.get("contracts", []) or []],
            "transition_groups": extraction.get("transition_groups", []),
        },
        "contract_completion": {
            "reason": completion.get("reason"),
            "basis": completion.get("basis"),
            "additional_contracts": [
                compact(item)
                for item in (completion.get("response") or {}).get("additional_contracts", []) or []
            ],
            "merge_dispositions": completion.get("merge_dispositions", []),
        },
        "discovery_grounding": {
            "reason": grounding.get("reason"),
            "basis": grounding.get("basis"),
            "branches": branches,
        },
        "d_adjudication": {
            "reason": d_stage.get("reason"),
            "basis": d_stage.get("basis"),
            "decisions": [compact(item) for item in d_stage.get("decisions", []) or []],
        },
        "validate_d": {
            "reason": correction.get("reason"),
            "basis": correction.get("basis"),
            "repair_attempted": correction.get("repair_attempted"),
            "initial_missing_ids": correction.get("initial_missing_ids", []),
            "initial_extra_ids": correction.get("initial_extra_ids", []),
            "repair_missing_ids": correction.get("repair_missing_ids", []),
            "repair_extra_ids": correction.get("repair_extra_ids", []),
        },
    }


def lexical_hints(record):
    text = " ".join(str(record.get(key) or "") for key in ("reason", "basis", "strongest_rebuttal")).lower()
    terms = {
        "natural_language": ("natural language", "requirement", "specification", "nl"),
        "author_source": ("author-source", "source_inventory", "plantuml", "modelir", "source"),
        "deterministic": ("inspection", "verify_fact", "reachability_fact", "closed_model", "predicate", "backend"),
        "execution": ("execution", "simulation", "receipt", "smt_fact", "verify_fact"),
        "alternative_reading": ("competent alternative", "alternative reading", "one could argue", "under one competent"),
    }
    return {name: any(term in text for term in values) for name, values in terms.items()}


def candidate_metrics(issues, evidence_records, d_decisions):
    props = collections.Counter(item.get("property") for item in issues)
    directions = collections.Counter(item.get("violation_direction") for item in issues)
    evidence = collections.Counter(
        evidence_type
        for item in issues
        for evidence_type in item.get("evidence_types", []) or []
    )
    hints = collections.Counter()
    for item in issues:
        for name, present in lexical_hints(item).items():
            if present:
                hints[name] += 1
    d_disposition = collections.Counter(item.get("defeater_disposition") for item in d_decisions)
    grounding = collections.Counter(item.get("grounding") for item in d_decisions)
    return {
        "raw_issue_candidates": len(issues),
        "evidence_record_count": len(evidence_records),
        "report_issue_cluster_count": 0,
        "property_counts": dict(props),
        "direction_counts": dict(directions),
        "property_entropy": normalized_entropy(props),
        "direction_entropy": normalized_entropy(directions),
        "evidence_entropy": normalized_entropy(evidence),
        "evidence_type_counts": dict(evidence),
        "predicate_bound": sum(item.get("predicate_id") is not None for item in issues),
        "locus_named": sum(bool(item.get("locus_names")) for item in issues),
        "source_ref_present": sum(bool(item.get("source_refs")) for item in issues),
        "reason_present": sum(bool(item.get("reason")) for item in issues),
        "basis_present": sum(bool(item.get("basis")) for item in issues),
        "strongest_rebuttal_present": sum(bool(item.get("strongest_rebuttal")) for item in issues),
        "lexical_hints": dict(hints),
        "reason_chars": text_stats([item.get("reason") for item in issues]),
        "basis_chars": text_stats([item.get("basis") for item in issues]),
        "rebuttal_chars": text_stats([item.get("strongest_rebuttal") for item in issues]),
        "d_defeater_disposition": dict(d_disposition),
        "d_grounding": dict(grounding),
    }


def ours_cell(model, path, compact_cells, source_root, judge_cells):
    data = read_json(path)
    pair = str(data.get("pair_id"))
    round_number = int(data.get("round"))
    issues = [compact(item) for item in (data.get("model_output") or {}).get("issues", []) or []]
    evidence_records = [compact(item) for item in data.get("evidence_records", []) or []]
    report_clusters = [compact(item) for item in data.get("report_issue_clusters", []) or []]
    trace = stage_trace(data)
    d_decisions = trace["d_adjudication"]["decisions"]
    metrics = candidate_metrics(issues, evidence_records, d_decisions)
    metrics["report_issue_cluster_count"] = len(report_clusters)
    compact_cell = compact_cells.get((pair, round_number, "ours"), {})
    historical_cell = judge_cells.get((pair, round_number, "ours"), {})
    calls = [call_summary(call) for call in data.get("llm_calls", []) or []]
    return {
        "model": model,
        "arm": "ours",
        "pair": pair,
        "round": round_number,
        "source_path": relative_source(path, source_root),
        "source_sha256": sha256(path),
        "run_id": data.get("run_id"),
        "status": data.get("status"),
        "eligible": data.get("eligible"),
        "eligibility_reasons": data.get("eligibility_reasons", []),
        "errors": data.get("errors", []),
        "calls": calls,
        "stage_trace": trace,
        "issues": issues,
        "evidence_records": evidence_records,
        "report_issue_clusters": report_clusters,
        "micro_metrics": metrics,
        "judge_snapshot": {
            "status": compact_cell.get("judge_status") or ("historical_readonly" if historical_cell else None),
            "audit": compact_cell.get("judge_audit"),
            "reports": len(compact_cell.get("reports", [])) or historical_cell.get("reports"),
            "schema_failures": compact_cell.get("schema_failures"),
            "audit_errors": compact_cell.get("audit_errors"),
            "source": historical_cell.get("source"),
            "sha256": historical_cell.get("sha256"),
            "judge_commit": historical_cell.get("judge_commit"),
        },
    }


def baseline_cell(model, path, source_root):
    data = read_json(path)
    parsed = data.get("parsed_output") or {}
    issues = parsed.get("issues", []) if isinstance(parsed, dict) else []
    usage = data.get("usage")
    if isinstance(usage, dict):
        usage = [usage]
    return {
        "model": model,
        "arm": "baseline",
        "pair": str(data.get("pair_id")),
        "round": int(data.get("round")),
        "source_path": relative_source(path, source_root),
        "source_sha256": sha256(path),
        "status": data.get("status"),
        "issue_count": data.get("issue_count"),
        "issues": issues,
        "analysis": parsed.get("analysis") if isinstance(parsed, dict) else None,
        "usage": [usage_item(item) for item in usage or []],
        "micro_metrics": {
            "issue_count": len(issues),
            "reason_present": sum(bool(item.get("reason")) for item in issues if isinstance(item, dict)),
            "reason_chars": text_stats(
                [item.get("reason") for item in issues if isinstance(item, dict)]
            ),
        },
    }


def issue_key(issue):
    return (
        issue.get("property"),
        tuple(issue.get("locus_names") or []),
        issue.get("violation_direction"),
    )


def js_divergence(left, right):
    keys = set(left) | set(right)
    l_total = sum(left.values()) or 1
    r_total = sum(right.values()) or 1
    lp = {key: left.get(key, 0) / l_total for key in keys}
    rp = {key: right.get(key, 0) / r_total for key in keys}
    midpoint = {key: (lp[key] + rp[key]) / 2 for key in keys}

    def kl(dist, base):
        return sum(value * math.log2(value / base[key]) for key, value in dist.items() if value)

    return round((kl(lp, midpoint) + kl(rp, midpoint)) / 2, 6)


def aggregate(cells):
    stats = {}
    for model in MODELS:
        model_cells = [cell for cell in cells if cell["model"] == model and cell["arm"] == "ours"]
        by_round = {}
        for round_number in range(1, ROUND_COUNT + 1):
            by_round[str(round_number)] = aggregate_subset(
                [cell for cell in model_cells if cell["round"] == round_number]
            )
        stats[model] = {"all_rounds": aggregate_subset(model_cells), "by_round": by_round}
    return stats


def aggregate_subset(cells):
    props = collections.Counter()
    directions = collections.Counter()
    evidence = collections.Counter()
    hints = collections.Counter()
    calls = collections.Counter()
    call_status = collections.Counter()
    d_disposition = collections.Counter()
    candidates = []
    reason_values = []
    basis_values = []
    rebuttal_values = []
    for cell in cells:
        metrics = cell["micro_metrics"]
        props.update(metrics["property_counts"])
        directions.update(metrics["direction_counts"])
        evidence.update(metrics["evidence_type_counts"])
        hints.update(metrics["lexical_hints"])
        candidates.extend(cell["issues"])
        for call in cell["calls"]:
            calls[call["kind"]] += 1
            call_status[(call["kind"], call["status"])] += 1
        d_disposition.update(metrics["d_defeater_disposition"])
        reason_values.extend(item.get("reason") for item in cell["issues"])
        basis_values.extend(item.get("basis") for item in cell["issues"])
        rebuttal_values.extend(item.get("strongest_rebuttal") for item in cell["issues"])
    return {
        "cells": len(cells),
        "raw_issue_candidates": len(candidates),
        "mean_candidates_per_cell": round(len(candidates) / len(cells), 4) if cells else 0,
        "property_counts": dict(props),
        "direction_counts": dict(directions),
        "property_entropy": normalized_entropy(props),
        "direction_entropy": normalized_entropy(directions),
        "evidence_entropy": normalized_entropy(evidence),
        "evidence_type_counts": dict(evidence),
        "lexical_hint_counts": dict(hints),
        "calls_by_kind": dict(calls),
        "call_status": {f"{kind}:{status}": count for (kind, status), count in call_status.items()},
        "d_defeater_disposition": dict(d_disposition),
        "reason_chars": text_stats(reason_values),
        "basis_chars": text_stats(basis_values),
        "rebuttal_chars": text_stats(rebuttal_values),
        "predicate_bound": sum(item.get("predicate_id") is not None for item in candidates),
        "locus_named": sum(bool(item.get("locus_names")) for item in candidates),
        "source_ref_present": sum(bool(item.get("source_refs")) for item in candidates),
        "strongest_rebuttal_present": sum(bool(item.get("strongest_rebuttal")) for item in candidates),
    }


def agreement(cells):
    indexed = {
        (cell["model"], cell["pair"], cell["round"]): {issue_key(item) for item in cell["issues"]}
        for cell in cells
        if cell["arm"] == "ours"
    }
    rows = []
    for pair in sorted({cell["pair"] for cell in cells if cell["arm"] == "ours"}):
        for round_number in range(1, ROUND_COUNT + 1):
            for index, left in enumerate(MODELS):
                for right in MODELS[index + 1:]:
                    a = indexed[(left, pair, round_number)]
                    b = indexed[(right, pair, round_number)]
                    union = a | b
                    rows.append(
                        {
                            "pair": pair,
                            "round": round_number,
                            "models": [left, right],
                            "jaccard_property_locus_direction": round(len(a & b) / len(union), 6) if union else 1.0,
                            "intersection": len(a & b),
                            "union": len(union),
                        }
                    )
    return rows


def round_transitions(cells):
    grouped = collections.defaultdict(dict)
    for cell in cells:
        if cell["arm"] == "ours":
            grouped[(cell["model"], cell["pair"])][cell["round"]] = {issue_key(item) for item in cell["issues"]}
    rows = []
    for (model, pair), rounds in sorted(grouped.items()):
        for left_round, right_round in ((1, 2), (2, 3)):
            left = rounds[left_round]
            right = rounds[right_round]
            rows.append(
                {
                    "model": model,
                    "pair": pair,
                    "from_round": left_round,
                    "to_round": right_round,
                    "retained": len(left & right),
                    "added": len(right - left),
                    "dropped": len(left - right),
                }
            )
    return rows


def main():
    compact_cells = {}
    for model in BACKBONE_MODELS:
        compact_data = read_json(RESULTS / model / "cells.json")
        for cell in compact_data["cells"]:
            compact_cells[(str(cell["pair"]), int(cell["round"]), cell["arm"])] = cell

    luna_history = read_json(RESULTS / "luna_history.json")
    historical_judge_cells = {}
    for arm in ("ours", "baseline"):
        for cell in luna_history["verification"]["arms"][arm]["cells"]:
            historical_judge_cells[(str(cell["pair_id"]), int(cell["round"]), arm)] = cell

    cells = []
    for model in MODELS:
        if model == "luna":
            source_root = PAPER / "final_results"
            ours_root = LUNA_OURS
            baseline_root = LUNA_BASELINE
            ours_paths = sorted(ours_root.glob("*/round-*.json"))
            baseline_paths = [
                path
                for run in ("run1", "run2", "run3")
                for path in sorted((baseline_root / run).glob("*-luna/record.json"))
            ]
        else:
            source_root = RESULTS
            ours_root = RAW / model / "ours"
            baseline_root = RAW / model / "baseline"
            ours_paths = sorted(ours_root.glob("r*-*/*/method/*/round-*.json"))
            baseline_paths = sorted(baseline_root.rglob("record.json"))
        if len(ours_paths) != PAIR_COUNT * ROUND_COUNT or len(baseline_paths) != PAIR_COUNT * ROUND_COUNT:
            raise SystemExit(f"{model}: unexpected source count {len(ours_paths)} / {len(baseline_paths)}")
        cells.extend(
            ours_cell(
                model,
                path,
                compact_cells,
                source_root,
                historical_judge_cells,
            )
            for path in ours_paths
        )
        cells.extend(baseline_cell(model, path, source_root) for path in baseline_paths)

    ours_cells = [cell for cell in cells if cell["arm"] == "ours"]
    baseline_stats = {}
    for model in MODELS:
        model_cells = [cell for cell in cells if cell["model"] == model and cell["arm"] == "baseline"]
        issue_counts = [cell["micro_metrics"]["issue_count"] for cell in model_cells]
        reasons = [item.get("reason") for cell in model_cells for item in cell["issues"]]
        baseline_stats[model] = {
            "cells": len(model_cells),
            "status_counts": dict(collections.Counter(cell["status"] for cell in model_cells)),
            "issue_count": {
                "total": sum(issue_counts),
                "mean_per_cell": round(mean(issue_counts), 4),
                "median_per_cell": median(issue_counts),
            },
            "reason_chars": text_stats(reasons),
        }

    audit = {
        "schema": "paper1.e2.micro-decision-profile.v1",
        "scope": {
            "models": list(MODELS),
            "arms": ["ours", "baseline"],
            "pairs": PAIR_COUNT,
            "rounds": ROUND_COUNT,
            "ours_cells": len(ours_cells),
            "baseline_cells": len(cells) - len(ours_cells),
            "judge": "gpt-5.6-luna (compact judge snapshot only; no new calls)",
        },
        "source": {
            "results_root": "final_results/e2_20260907",
            "raw_root": "final_results/e2_20260907/raw",
            "historical_luna_ours_root": "final_results/v61_source_divergence_vs_x1v2_baseline/raw/v61_current/method/method",
            "historical_luna_baseline_root": "final_results/v60_current_vs_x1v2_baseline/raw/x1v2_baseline/method",
            "compact_schema": "paper1.e2.frozen-decisions.v1",
            "field_boundary": {
                "candidate_reason_basis": "model-produced observable rationale/basis in ours source output",
                "judge_reason_basis": "Luna judge fields in compact cells and judge_source; excluded from candidate profile",
                "baseline_reason": "baseline free-form issue.reason; no typed basis/evidence contract",
                "hidden_chain_of_thought": "not observed or inferred",
            },
        },
        "definitions": {
            "candidate_key": ["property", "locus_names", "violation_direction"],
            "lexical_hints": "transparent term-presence indicators for review triage; not semantic labels",
            "candidate_breadth": "B = raw_issue_candidates / cells",
            "binding_rate": "R_f = count of raw candidates with field f present / raw_issue_candidates; f is source_refs, locus_names, or predicate_id",
            "normalized_shannon_entropy": {
                "formula": "H_norm = -sum_i(p_i * log2(p_i)) / log2(k)",
                "p_i": "count_i / sum_j(count_j) over non-zero categories",
                "k": "number of non-zero categories in the subset",
                "edge_case": "0 when the total is zero or k <= 1",
                "interpretation": "0 means concentration in one observed category; 1 means a uniform distribution across the observed categories",
                "scope": "computed separately for property_counts, direction_counts, and evidence_type_counts; zero-count categories are excluded and raw counts remain the companion evidence",
            },
            "lexical_hint_rate": "R_term = candidates whose reason/basis/strongest_rebuttal contains a term in the fixed transparent list / raw_issue_candidates",
            "dossier_disposition": "counts and within-D proportions use d_adjudication dossier records as denominator; they are not candidate rates",
            "agreement": "Jaccard over normalized candidate keys within the same pair and round",
            "round_transition": "set retention/add/drop between adjacent rounds",
            "micro_denominators": "candidate or call as stated; pair/cluster remains the inferential unit",
        },
        "aggregate_ours": aggregate(ours_cells),
        "baseline_summary": baseline_stats,
        "agreement": agreement(ours_cells),
        "round_transitions": round_transitions(ours_cells),
        "cells": cells,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
