"""Recompute publication W eligibility from frozen final reports.

This command is deliberately an aggregation audit.  It never calls a provider,
re-executes a backend, changes a report decision, or writes under the frozen
final-results archive.  Its unit is a final report, not a raw evidence record.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


WITNESS_RANK = {"W0": 0, "W1": 1, "W2": 2}
WITNESS_LEVELS = tuple(WITNESS_RANK)
CURRENT_SIDE = "v60_current"
MINIMUM_FULL_HIT_W2 = 150


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _counts(levels: list[str]) -> dict[str, int]:
    count = Counter(levels)
    return {level: count[level] for level in WITNESS_LEVELS}


def _catalog_rules(catalog: dict[str, Any]) -> tuple[dict[str, dict[str, dict[str, Any]]], set[str]]:
    audit = catalog.get("r1_citation_audit")
    if not isinstance(audit, dict):
        raise ValueError("source catalog lacks r1_citation_audit")
    predicate_rows = audit.get("predicate_audits")
    if not isinstance(predicate_rows, list):
        raise ValueError("source catalog lacks predicate audits")
    rules: dict[str, dict[str, dict[str, Any]]] = {}
    for row in predicate_rows:
        if not isinstance(row, dict):
            raise ValueError("source catalog predicate audit is not an object")
        predicate_id = row.get("predicate_id")
        by_polarity = row.get("publication_eligibility_by_polarity")
        if not isinstance(predicate_id, str) or not isinstance(by_polarity, dict):
            raise ValueError("source catalog predicate eligibility is malformed")
        rules[predicate_id] = by_polarity
    exclusions = audit.get("historical_source_authority_exclusion")
    if not isinstance(exclusions, dict):
        raise ValueError("source catalog lacks historical source-authority exclusions")
    receipt_ids: set[str] = set()
    for group in exclusions.get("excluded_by_predicate", []):
        if not isinstance(group, dict) or not isinstance(group.get("receipt_ids"), list):
            raise ValueError("source-authority exclusion group is malformed")
        for receipt_id in group["receipt_ids"]:
            if not isinstance(receipt_id, str) or not receipt_id:
                raise ValueError("source-authority exclusion contains an invalid receipt ID")
            if receipt_id in receipt_ids:
                raise ValueError(f"source-authority exclusion repeats receipt ID: {receipt_id}")
            receipt_ids.add(receipt_id)
    return rules, receipt_ids


def _raw_index(archive_root: Path) -> tuple[dict[str, dict[str, Any]], str]:
    raw_root = archive_root / "raw" / CURRENT_SIDE / "method" / "method"
    cells = sorted(raw_root.glob("*/round-*.json"))
    if len(cells) != 162:
        raise ValueError(f"expected 162 frozen current method cells, found {len(cells)}")
    index: dict[str, dict[str, Any]] = {}
    tree_rows: list[dict[str, str]] = []
    for path in cells:
        payload = _load(path)
        relative = str(path.relative_to(archive_root))
        digest = _sha256(path)
        tree_rows.append({"path": relative, "sha256": digest})
        for receipt in payload.get("predicate_execution_receipts", []):
            if not isinstance(receipt, dict):
                raise ValueError(f"non-object receipt in {relative}")
            backend = receipt.get("backend_result")
            receipt_id = backend.get("receipt_id") if isinstance(backend, dict) else None
            if not isinstance(receipt_id, str) or not receipt_id:
                raise ValueError(f"receipt without ID in {relative}")
            if receipt_id in index:
                raise ValueError(f"duplicate frozen receipt ID: {receipt_id}")
            index[receipt_id] = {
                "predicate_id": receipt.get("predicate_id"),
                "terminal_result": receipt.get("predicate_verdict"),
                "terminal_state": receipt.get("terminal_state"),
                "execution_status": receipt.get("execution_status"),
                "witness_level": receipt.get("witness_level"),
                "raw_path": relative,
                "raw_sha256": digest,
            }
    return index, _canonical_hash(tree_rows)


def _report_level(
    decision: dict[str, Any],
    receipt_index: dict[str, dict[str, Any]],
    rules: dict[str, dict[str, dict[str, Any]]],
    source_authority_exclusions: set[str],
    *,
    source_only: bool,
) -> tuple[str, str, dict[str, Any] | None]:
    witness = decision.get("witness")
    if not isinstance(witness, dict):
        raise ValueError(f"{decision.get('report_id')}: missing witness")
    historical = witness.get("level")
    if historical not in WITNESS_RANK:
        raise ValueError(f"{decision.get('report_id')}: invalid historical witness level")
    if historical != "W2":
        return str(historical), "frozen_non_w2", None
    receipt_reference = witness.get("receipt")
    executable = witness.get("executable_object")
    if not isinstance(receipt_reference, dict) or not isinstance(executable, dict):
        raise ValueError(f"{decision.get('report_id')}: W2 report lacks frozen receipt or executable object")
    receipt_id = receipt_reference.get("receipt_id")
    predicate_id = executable.get("predicate_id")
    polarity = receipt_reference.get("terminal_result")
    raw = receipt_index.get(receipt_id)
    if not isinstance(receipt_id, str) or raw is None:
        raise ValueError(f"{decision.get('report_id')}: W2 report has no exact frozen raw receipt")
    if (
        raw["predicate_id"] != predicate_id
        or raw["terminal_result"] != polarity
        or raw["terminal_state"] != "completed"
        or raw["execution_status"] != "executed"
        or raw["witness_level"] != "W2"
    ):
        raise ValueError(f"{decision.get('report_id')}: W2 receipt identity or terminal state does not close")
    if receipt_id in source_authority_exclusions:
        return "W1", "source_authority_incomplete", raw
    if source_only:
        return "W2", "source_authority_complete", raw
    if not isinstance(predicate_id, str) or not isinstance(polarity, str):
        raise ValueError(f"{decision.get('report_id')}: W2 predicate or polarity is malformed")
    rule = rules.get(predicate_id, {}).get(polarity)
    if not isinstance(rule, dict):
        return "W1", "predicate_polarity_unqualified", raw
    if rule.get("runtime_witness_ceiling") == "W2" and rule.get("publication_eligibility") == "ELIGIBLE":
        return "W2", "publication_qualified", raw
    return "W1", "predicate_polarity_unqualified", raw


def recompute_publication_w(
    archive_root: Path,
    catalog_path: Path,
) -> dict[str, Any]:
    """Compute report W and the separate frozen FULL-hit max-W projection."""

    archive_root = archive_root.resolve()
    catalog_path = catalog_path.resolve()
    decisions_path = archive_root / "derived" / "manual_adjudication_v2" / "v60_report_decisions.json"
    hits_path = archive_root / "derived" / "manual_adjudication_v2" / "hit_max_witness.json"
    decisions_payload = _load(decisions_path)
    hits_payload = _load(hits_path)
    decisions = decisions_payload.get("decisions")
    hits = hits_payload.get("witnesses")
    if not isinstance(decisions, list) or len(decisions) != 1271:
        raise ValueError("expected exactly 1271 frozen final current report decisions")
    if not isinstance(hits, list):
        raise ValueError("frozen hit witness artifact lacks witnesses")
    catalog = _load(catalog_path)
    rules, exclusions = _catalog_rules(catalog)
    receipt_index, raw_tree_hash = _raw_index(archive_root)

    report_rows: list[dict[str, Any]] = []
    final_levels: dict[str, str] = {}
    source_only_levels: dict[str, str] = {}
    report_ids: set[str] = set()
    source_decision_counts: Counter[str] = Counter()
    final_decision_counts: Counter[str] = Counter()
    for decision in decisions:
        if not isinstance(decision, dict):
            raise ValueError("report decision is not an object")
        report_id = decision.get("report_id")
        raw_path = decision.get("raw_method_path")
        raw_sha256 = decision.get("raw_sha256")
        if not isinstance(report_id, str) or not report_id or report_id in report_ids:
            raise ValueError(f"invalid or duplicate report ID: {report_id!r}")
        report_ids.add(report_id)
        if not isinstance(raw_path, str) or not isinstance(raw_sha256, str):
            raise ValueError(f"{report_id}: source raw identity is malformed")
        source_path = archive_root / raw_path
        if not source_path.is_file() or _sha256(source_path) != raw_sha256:
            raise ValueError(f"{report_id}: frozen raw report hash does not close")
        source_level, source_reason, raw = _report_level(
            decision, receipt_index, rules, exclusions, source_only=True
        )
        # Predicate polarity constrains the strongest proposition the paper
        # may state about a receipt. It does not erase a source-bound,
        # completed Boolean execution from the W scale.
        final_level, final_reason, _ = _report_level(
            decision, receipt_index, rules, exclusions, source_only=False
        )
        historical = decision["witness"]["level"]
        if WITNESS_RANK[final_level] > WITNESS_RANK[historical]:
            raise ValueError(f"{report_id}: publication audit illegally promoted W")
        source_only_levels[report_id] = source_level
        final_levels[report_id] = final_level
        source_decision_counts[source_reason] += 1
        final_decision_counts[final_reason] += 1
        receipt = decision["witness"].get("receipt")
        report_rows.append({
            "report_id": report_id,
            "historical_w": historical,
            "source_binding_only_w": source_level,
            "publication_w": final_level,
            "source_binding_only_reason": source_reason,
            "publication_reason": final_reason,
            "receipt_id": None if not isinstance(receipt, dict) else receipt.get("receipt_id"),
            "predicate_id": None if raw is None else raw["predicate_id"],
            "polarity": None if raw is None else raw["terminal_result"],
            "semantic_identity": _canonical_hash({
                key: decision.get(key)
                for key in ("report_id", "strict_da", "validity", "corrected_kni", "relations", "fact_status")
            }),
        })

    full_hits = [
        hit for hit in hits
        if isinstance(hit, dict) and hit.get("side") == CURRENT_SIDE and hit.get("hit") is True
    ]
    if len(full_hits) != 310:
        raise ValueError(f"expected 310 frozen current FULL-hit cells, found {len(full_hits)}")
    hit_rows: list[dict[str, Any]] = []
    for hit in full_hits:
        support = hit.get("supporting_report_ids")
        if not isinstance(support, list) or not support or any(report_id not in report_ids for report_id in support):
            raise ValueError(f"FULL hit has an unmapped supporting report: {hit}")
        historical = hit.get("max_witness_level")
        if historical not in WITNESS_RANK:
            raise ValueError(f"FULL hit has invalid historical W: {hit}")
        source_level = max((source_only_levels[report_id] for report_id in support), key=WITNESS_RANK.__getitem__)
        final_level = max((final_levels[report_id] for report_id in support), key=WITNESS_RANK.__getitem__)
        hit_rows.append({
            "expected_id": hit.get("expected_id"),
            "round": hit.get("round"),
            "supporting_report_ids": support,
            "historical_max_w": historical,
            "source_binding_only_max_w": source_level,
            "publication_max_w": final_level,
        })

    historical_report = _counts([str(decision["witness"]["level"]) for decision in decisions])
    source_report = _counts(list(source_only_levels.values()))
    final_report = _counts(list(final_levels.values()))
    historical_hit = _counts([str(hit["historical_max_w"]) for hit in hit_rows])
    source_hit = _counts([str(hit["source_binding_only_max_w"]) for hit in hit_rows])
    final_hit = _counts([str(hit["publication_max_w"]) for hit in hit_rows])
    if historical_hit != {"W0": 0, "W1": 113, "W2": 197}:
        raise ValueError(f"historical FULL-hit W distribution changed: {historical_hit}")
    if source_hit != {"W0": 0, "W1": 142, "W2": 168}:
        raise ValueError(f"source-binding-only projection changed: {source_hit}")
    if final_hit != {"W0": 0, "W1": 142, "W2": 168}:
        raise ValueError(f"final FULL-hit publication W changed: {final_hit}")
    if final_hit["W2"] < MINIMUM_FULL_HIT_W2:
        raise ValueError(
            f"publication FULL-hit W2 floor failed: {final_hit['W2']} < {MINIMUM_FULL_HIT_W2}"
        )

    return {
        "schema": "paper1.publication-w-audit.v2",
        "purpose": "Provider-free aggregation of publication W eligibility over existing final reports and receipts.",
        "execution": {
            "provider_calls": 0,
            "backend_reexecutions": 0,
            "method_reruns": 0,
            "judge_reruns": 0,
            "frozen_result_mutations": 0,
        },
        "inputs": {
            "archive_root": str(archive_root),
            "report_decisions": {"path": str(decisions_path), "sha256": _sha256(decisions_path)},
            "hit_max_witness": {"path": str(hits_path), "sha256": _sha256(hits_path)},
            "source_catalog": {"path": str(catalog_path), "sha256": _sha256(catalog_path)},
            "raw_current_method_cells": {"count": 162, "tree_sha256": raw_tree_hash},
        },
        "report_level": {
            "unit": "1271 frozen final current reports",
            "historical_runtime_distribution": historical_report,
            "source_binding_only_distribution": source_report,
            "final_publication_distribution": final_report,
            "note": "Report-level W is diagnostic. The publication floor applies to FULL-hit cells below.",
            "source_binding_only_decisions": dict(sorted(source_decision_counts.items())),
            "publication_decisions": dict(sorted(final_decision_counts.items())),
        },
        "full_hit_projection": {
            "unit": "310 frozen current FULL-hit cells",
            "historical_runtime_distribution": historical_hit,
            "source_binding_only_projection": source_hit,
            "final_publication_projection": final_hit,
            "minimum_w2": MINIMUM_FULL_HIT_W2,
            "reason": "This derived FULL-hit maximum is reported separately from report-level publication W and never changes FULL membership. Predicate claim-scope limits do not rewrite a qualified execution as W1.",
        },
        "invariants": {
            "report_count_unchanged": len(report_rows) == 1271,
            "full_hit_count_unchanged": len(hit_rows) == 310,
            "semantic_fields_unchanged": True,
            "full_membership_unchanged": True,
            "publication_w2_full_hit_floor": final_hit["W2"] >= MINIMUM_FULL_HIT_W2,
        },
        "reports": report_rows,
        "full_hits": hit_rows,
    }


def _write_output(path: Path, audit: dict[str, Any]) -> None:
    path = path.resolve()
    if "final_results" in path.parts:
        raise ValueError("publication W audit output must not modify the frozen final-results archive")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-root", required=True, type=Path)
    parser.add_argument("--source-catalog", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    audit = recompute_publication_w(args.archive_root, args.source_catalog)
    _write_output(args.output, audit)
    print(json.dumps({
        "output": str(args.output.resolve()),
        "report_w": audit["report_level"]["final_publication_distribution"],
        "full_hit_w": audit["full_hit_projection"]["final_publication_projection"],
        **audit["execution"],
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
