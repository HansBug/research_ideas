"""Compare predicate gold with frozen v60 evidence without rerunning the method.

The output is explanatory only.  FULL/PARTIAL relations come from the frozen
current-v4 adjudication and this module never changes hit, W, or K/N/I.  A
different actual predicate is retained for semantic review rather than treated
as an automatic miss.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from paper_stm_evaluation.predicate_gold import (
    PredicateGoldAnnotation,
    PredicateGoldDataset,
    canonical_sha256,
    sha256_path,
    write_json,
)

SCHEMA_VERSION = "paper1.predicate-gold.expected-vs-actual.v1"


def _pointer(document: Any, pointer: str) -> Any:
    """Resolve one RFC 6901 pointer without string-searching structured data."""

    if pointer == "":
        return document
    if not pointer.startswith("/"):
        raise ValueError(f"invalid JSON pointer: {pointer}")
    value = document
    for token in pointer[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(value, list):
            value = value[int(token)]
        else:
            value = value[token]
    return value


def _selected(annotation: PredicateGoldAnnotation) -> Any:
    """Return the exact or proxy reference property, when one exists."""

    return annotation.gold_property or annotation.proxy_property


def _expected_bucket(annotation: PredicateGoldAnnotation) -> str:
    """Name one stable expected-property analysis bucket."""

    selected = _selected(annotation)
    if selected is None:
        return "UNSUPPORTED_EXACT"
    if selected.predicate_ids:
        ids = "+".join(sorted(set(selected.predicate_ids)))
        return f"COMPOSITE:{ids}" if selected.composition else ids
    return f"EVALUATION_ONLY:{selected.property_id}"


def _expected_inputs(annotation: PredicateGoldAnnotation) -> dict[str, Any]:
    """Flatten source-provenanced expected typed inputs for comparison."""

    selected = _selected(annotation)
    if selected is None:
        return {}
    return {item.field_name: item.normalized_value for item in selected.typed_inputs}


def _actual_inputs(report: dict[str, Any]) -> dict[str, Any] | None:
    """Recover report-bound frozen inputs or declare them unobservable."""

    direct = report.get("predicate_inputs")
    if isinstance(direct, dict) and direct:
        return direct
    receipt = report.get("execution_receipt")
    if isinstance(receipt, dict):
        typed = receipt.get("typed_inputs")
        if isinstance(typed, dict):
            raw = typed.get("raw_values")
            if isinstance(raw, dict) and raw:
                return raw
    return None


def _input_comparison(expected: dict[str, Any], actual: dict[str, Any] | None) -> str:
    """Compare only common typed fields; absence remains NOT_OBSERVABLE."""

    if not expected:
        return "NOT_APPLICABLE"
    if actual is None or not all(name in actual for name in expected):
        return "NOT_OBSERVABLE_FROM_RAW"
    return "MATCH" if all(actual[name] == value for name, value in expected.items()) else "MISMATCH"


def _report_projection(
    *,
    comparison_root: Path,
    decision: dict[str, Any],
    expected_predicate_ids: set[str],
    expected_inputs: dict[str, Any],
) -> dict[str, Any]:
    """Project one frozen current-v4 decision and its exact raw report."""

    raw_path = comparison_root / decision["raw_method_path"]
    if sha256_path(raw_path) != decision["raw_sha256"]:
        raise ValueError(f"raw hash mismatch for {decision['original_report_id']}")
    raw_document = json.loads(raw_path.read_text(encoding="utf-8"))
    report = _pointer(raw_document, decision["raw_json_pointer"])
    usage = decision["predicate_usage"]
    predicate_id = usage.get("predicate_id") or report.get("predicate_id")
    actual_inputs = _actual_inputs(report)
    input_comparison = (
        _input_comparison(expected_inputs, actual_inputs)
        if predicate_id in expected_predicate_ids
        else "NOT_APPLICABLE"
    )
    terminal = usage.get("terminal_result")
    return {
        "report_id": decision["original_report_id"],
        "pair_id": decision["pair_id"],
        "round": decision["round"],
        "canonical_class": decision["canonical_class"],
        "relation": None,
        "predicate_id": predicate_id,
        "actual_typed_inputs": actual_inputs,
        "typed_inputs_observable": actual_inputs is not None,
        "input_comparison": input_comparison,
        "receipt_present": bool(usage.get("receipt_present")),
        "executed_with_receipt": bool(usage.get("executed_with_receipt")),
        "terminal_result": terminal,
        "terminal_usage": bool(usage.get("executed_with_receipt"))
        and isinstance(terminal, bool),
        "canonical_predicate_contribution": bool(decision.get("predicate_contribution")),
        "false_contribution": bool(decision.get("predicate_contribution"))
        and terminal is False,
        "report_bound_binding": predicate_id is not None and actual_inputs is not None,
        "raw_path": decision["raw_method_path"],
        "raw_json_pointer": decision["raw_json_pointer"],
        "raw_sha256": decision["raw_sha256"],
    }


def _issue_classification(
    annotation: PredicateGoldAnnotation,
    full_reports: list[dict[str, Any]],
) -> str:
    """Classify observed composition without redefining hit eligibility."""

    if not full_reports:
        return "NOT_HIT"
    selected = _selected(annotation)
    if selected is None:
        return "UNSUPPORTED_GOLD_BUT_FULL_HIT"
    expected_ids = set(selected.predicate_ids)
    if not expected_ids:
        return "EVALUATION_ONLY_GOLD_ACTUAL_REQUIRES_SEMANTIC_REVIEW"
    same = [row for row in full_reports if row["predicate_id"] in expected_ids]
    if any(row["input_comparison"] == "MATCH" for row in same):
        return "EXPECTED_ID_AND_INPUT_MATCH"
    if any(row["input_comparison"] == "MISMATCH" for row in same):
        return "EXPECTED_ID_INPUT_MISMATCH"
    if same:
        return "EXPECTED_ID_INPUT_NOT_OBSERVABLE"
    if any(row["predicate_id"] is not None for row in full_reports):
        return "ALTERNATE_PREDICATE_REQUIRES_SEMANTIC_REVIEW"
    return "NO_PREDICATE_ON_FULL_HIT"


def build_analysis(
    *,
    canonical_path: Path,
    decisions_path: Path,
    comparison_root: Path,
    generated_at: str,
) -> dict[str, Any]:
    """Build the deterministic issue-level expected-vs-actual analysis."""

    gold = PredicateGoldDataset.model_validate_json(
        canonical_path.read_text(encoding="utf-8")
    )
    decisions_document = json.loads(decisions_path.read_text(encoding="utf-8"))
    decisions = decisions_document["decisions"]
    by_expected: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for decision in decisions:
        for relation in decision["expected_relations"]:
            if relation["relation"] in {"FULL_MATCH", "PARTIAL_MATCH"}:
                by_expected[relation["expected_id"]].append(
                    (relation["relation"], decision)
                )

    rows: list[dict[str, Any]] = []
    matrix: Counter[tuple[str, str]] = Counter()
    predicate_stats: dict[str, Counter[str]] = defaultdict(Counter)
    for ledger_id, annotation in sorted(gold.items.items()):
        selected = _selected(annotation)
        expected_ids = set(selected.predicate_ids) if selected else set()
        expected_inputs = _expected_inputs(annotation)
        full_reports: list[dict[str, Any]] = []
        partial_reports: list[dict[str, Any]] = []
        for relation, decision in by_expected.get(ledger_id, []):
            report = _report_projection(
                comparison_root=comparison_root,
                decision=decision,
                expected_predicate_ids=expected_ids,
                expected_inputs=expected_inputs,
            )
            report["relation"] = relation
            (full_reports if relation == "FULL_MATCH" else partial_reports).append(report)
        full_reports.sort(key=lambda item: (item["round"], item["report_id"]))
        partial_reports.sort(key=lambda item: (item["round"], item["report_id"]))
        bucket = _expected_bucket(annotation)
        actual_ids = sorted(
            {
                report["predicate_id"] or "NO_PREDICATE"
                for report in full_reports
            }
        )
        actual_bucket = "+".join(actual_ids) if actual_ids else "NOT_HIT"
        classification = _issue_classification(annotation, full_reports)
        matrix[(bucket, actual_bucket)] += 1
        predicate_stats[bucket]["ledger_count"] += 1
        predicate_stats[bucket]["full_hit_count"] += bool(full_reports)
        predicate_stats[bucket]["supported_count"] += bool(full_reports or partial_reports)
        predicate_stats[bucket]["full_expected_round_hits"] += len(
            {report["round"] for report in full_reports}
        )
        row = {
            "ledger_id": ledger_id,
            "pair_id": annotation.pair_id,
            "family": annotation.family,
            "d_tier": annotation.d_tier,
            "l_tier": annotation.l_tier,
            "gold_status": annotation.gold_status.value,
            "expected_bucket": bucket,
            "expected_property_id": selected.property_id if selected else None,
            "expected_predicate_ids": sorted(expected_ids),
            "expected_typed_inputs": expected_inputs,
            "full_hit": bool(full_reports),
            "supported": bool(full_reports or partial_reports),
            "classification": classification,
            "full_reports": full_reports,
            "partial_reports": partial_reports,
        }
        rows.append(row)

    stats = []
    for bucket, counts in sorted(predicate_stats.items()):
        denominator = counts["ledger_count"]
        stats.append(
            {
                "expected_bucket": bucket,
                "ledger_count": denominator,
                "full_hit_count": counts["full_hit_count"],
                "full_hit_rate": counts["full_hit_count"] / denominator,
                "supported_count": counts["supported_count"],
                "supported_rate": counts["supported_count"] / denominator,
                "full_expected_round_hits": counts["full_expected_round_hits"],
                "expected_round_denominator": denominator * 3,
                "full_expected_round_hit_rate": counts["full_expected_round_hits"]
                / (denominator * 3),
            }
        )
    unsigned = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at,
        "canonical_path": canonical_path.as_posix(),
        "canonical_sha256": sha256_path(canonical_path),
        "current_v4_decisions_path": decisions_path.as_posix(),
        "current_v4_decisions_sha256": sha256_path(decisions_path),
        "analysis_role": (
            "Offline composition analysis only; it does not redefine FULL/PARTIAL hit, W, or K/N/I."
        ),
        "method_reruns": 0,
        "judge_reruns": 0,
        "provider_experiment_calls": 0,
        "full_experiment_reruns": 0,
        "total_ledger_issues": len(rows),
        "full_hit_issues": sum(row["full_hit"] for row in rows),
        "supported_issues": sum(row["supported"] for row in rows),
        "classification_counts": dict(
            sorted(Counter(row["classification"] for row in rows).items())
        ),
        "predicate_statistics": stats,
        "matrix": [
            {
                "expected_bucket": expected,
                "actual_full_hit_predicates": actual,
                "ledger_count": count,
            }
            for (expected, actual), count in sorted(matrix.items())
        ],
        "items": rows,
    }
    return {**unsigned, "analysis_sha256": canonical_sha256(unsigned)}


def write_tsv(analysis: dict[str, Any], path: Path) -> None:
    """Write one deterministic flat mirror for manual matrix review."""

    path.parent.mkdir(parents=True, exist_ok=True)
    columns = (
        "ledger_id",
        "pair_id",
        "family",
        "d_tier",
        "l_tier",
        "gold_status",
        "expected_bucket",
        "expected_predicate_ids",
        "full_hit",
        "supported",
        "classification",
        "actual_full_predicate_ids",
        "full_report_ids",
        "partial_report_ids",
    )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for item in analysis["items"]:
            writer.writerow(
                {
                    **{key: item[key] for key in columns[:7]},
                    "expected_predicate_ids": "|".join(item["expected_predicate_ids"]),
                    "full_hit": str(item["full_hit"]).lower(),
                    "supported": str(item["supported"]).lower(),
                    "classification": item["classification"],
                    "actual_full_predicate_ids": "|".join(
                        sorted(
                            {
                                report["predicate_id"] or "NO_PREDICATE"
                                for report in item["full_reports"]
                            }
                        )
                    ),
                    "full_report_ids": "|".join(
                        report["report_id"] for report in item["full_reports"]
                    ),
                    "partial_report_ids": "|".join(
                        report["report_id"] for report in item["partial_reports"]
                    ),
                }
            )


def main(argv: list[str] | None = None) -> int:
    """Build the JSON and TSV expected-vs-actual views."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--current-v4-decisions", type=Path, required=True)
    parser.add_argument("--comparison-root", type=Path, required=True)
    parser.add_argument("--generated-at", required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-tsv", type=Path, required=True)
    args = parser.parse_args(argv)
    analysis = build_analysis(
        canonical_path=args.canonical,
        decisions_path=args.current_v4_decisions,
        comparison_root=args.comparison_root,
        generated_at=args.generated_at,
    )
    write_json(args.output_json, analysis)
    write_tsv(analysis, args.output_tsv)
    print(
        json.dumps(
            {
                "total": analysis["total_ledger_issues"],
                "full_hit_issues": analysis["full_hit_issues"],
                "analysis_sha256": analysis["analysis_sha256"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
