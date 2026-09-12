#!/usr/bin/env python3
"""Rebuild v3 canonical baseline data from the explicit pane5 register.

The register is the only source of new D/A and relation decisions.  Frozen
v2 data is used for the non-K scope, the original-category migration field,
and the unchanged W association; it cannot supply a new semantic label.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from paper_stm_evaluation.manual_adjudication_v3_baseline_ni import (
    A0Type,
    BaselineReportDecisionV3,
    DATier,
    DecisionSetV3,
    DefectClaimStatus,
    FactStatus,
    NormativeStatus,
    Pane5RegisterV3,
    Relation,
    Validity,
    Witness,
    WitnessLevel,
)


ARCHIVE_MARKER = "final_results/v60_current_vs_x1v2_baseline/"


def load(path: Path) -> Any:
    """Read one UTF-8 JSON artifact."""

    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    """Return a prefixed SHA-256 for one file."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_path(path: str, archive: Path) -> Path:
    """Resolve an old absolute/archive-marked path into the archive."""

    if ARCHIVE_MARKER in path:
        path = path.split(ARCHIVE_MARKER, 1)[1]
    prefix = "project_1_llm_state_machine_modeling/paper_stm_issue_discover/"
    path = path.removeprefix(prefix)
    return archive / path


def raw_inventory(archive: Path) -> dict[str, dict[str, Any]]:
    """Enumerate raw report identity and exact finding text."""

    result: dict[str, dict[str, Any]] = {}
    for path in sorted((archive / "raw/x1v2_baseline/method").glob("run*/*/record.json")):
        run = int(path.parts[-3].removeprefix("run"))
        pair = path.parts[-2].split("-", 1)[0]
        document = load(path)
        for index, finding in enumerate(document.get("parsed_output", {}).get("issues", [])):
            report_id = f"{pair}:r{run}:baseline_issue_{index + 1}"
            if report_id in result:
                raise ValueError(f"duplicate raw report {report_id}")
            result[report_id] = {
                "path": path.relative_to(archive).as_posix(),
                "pointer": f"/parsed_output/issues/{index}",
                "sha256": sha(path),
                "finding": finding,
                "pair_id": pair,
                "round": run,
                "finding_index": index,
            }
    return result


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write a deterministic fixed-column mirror of canonical decisions."""

    fields = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({
                key: json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                if isinstance(value, (dict, list, tuple)) else ("" if value is None else value)
                for key, value in row.items()
            })


def main() -> None:
    """Rebuild the canonical non-K decision and dense relation files."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-root", type=Path, required=True)
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    v3 = archive / "derived/manual_adjudication_v3_baseline_ni"
    old = load(archive / "derived/manual_adjudication_v2/x1v2_report_decisions.json")["decisions"]
    old_by_id = {row["report_id"]: row for row in old}
    register_payload = load(v3 / "pane5_adjudications_v3.json")
    register = Pane5RegisterV3.model_validate(register_payload)
    register_by_id = {row.report_id: row for row in register.rows}
    raw = raw_inventory(archive)
    expected_ids = tuple(load(archive / "reference/ledger.json")["items"])
    non_k_ids = {rid for rid, row in old_by_id.items() if row["corrected_kni"] != "K"}
    if len(raw) != 512 or len(non_k_ids) != 233 or set(register_by_id) != non_k_ids:
        raise ValueError("raw, frozen non-K scope, and pane5 register do not close")
    snapshot = load(v3 / "frozen_k_snapshot_v3.json")
    if snapshot.get("count") != 279 or set(row["report_id"] for row in snapshot["rows"]) != {rid for rid, row in old_by_id.items() if row["corrected_kni"] == "K"}:
        raise ValueError("frozen K snapshot does not close")

    decisions: list[BaselineReportDecisionV3] = []
    dense: list[dict[str, Any]] = []
    for report_id in sorted(non_k_ids):
        old_row = old_by_id[report_id]
        final = register_by_id[report_id]
        raw_row = raw[report_id]
        finding = raw_row["finding"]
        if (final.pair_id, final.round, final.finding_index) != (raw_row["pair_id"], raw_row["round"], raw_row["finding_index"]):
            raise ValueError(f"pane5/raw identity mismatch: {report_id}")
        if tuple(x.expected_id for x in final.relations) != expected_ids:
            raise ValueError(f"pane5 relation order mismatch: {report_id}")
        relation_rows = tuple(final.relations)
        positive = any(x.relation in {Relation.FULL_MATCH, Relation.PARTIAL_MATCH} for x in relation_rows)
        validity = Validity.INVALID if final.d_tier in {DATier.D0, DATier.A0} else (Validity.VALID_KNOWN if positive else Validity.VALID_NOVEL)
        kni = "I" if validity == Validity.INVALID else ("K" if positive else "N")
        if final.validity != validity or final.corrected_kni != kni:
            raise ValueError(f"pane5 closure mismatch: {report_id}")
        if final.d_tier == DATier.A0:
            fact_status = FactStatus.REFUTED
            a0_type = A0Type.FALSE_POSITIVE
            normative = NormativeStatus.NOT_ESTABLISHED
            claim_status = DefectClaimStatus.NO_DEFECT_CLAIM
        elif final.d_tier == DATier.D0:
            fact_status = FactStatus.ESTABLISHED
            a0_type = None
            normative = NormativeStatus.NOT_ESTABLISHED
            claim_status = DefectClaimStatus.NO_DEFECT_CLAIM
        else:
            fact_status = FactStatus.ESTABLISHED
            a0_type = None
            normative = NormativeStatus.ESTABLISHED
            claim_status = DefectClaimStatus.DEFECT_CLAIM
        old_witness = old_row["witness"]
        witness = Witness(
            level=WitnessLevel(old_witness["level"]),
            concrete_locations=(old_witness.get("concrete_location") or finding.get("where") or "raw report locus",),
            executable_object=None,
            receipt=None,
            artifact_sha256=None,
            terminal_result=None,
            reason=f"{report_id}: W is retained as an independent evidence axis and cannot decide D/A, validity, or K/N/I.",
            basis=f"{report_id}: the frozen W association is carried forward without a post-hoc upgrade.",
        )
        decision = BaselineReportDecisionV3(
            side="x1v2_baseline",
            pair_id=final.pair_id,
            round=final.round,
            original_report_id=report_id,
            finding_index=final.finding_index,
            raw_method_path=raw_row["path"],
            raw_json_pointer=raw_row["pointer"],
            raw_sha256=raw_row["sha256"],
            claim_pointer=raw_row["pointer"] + "/issue",
            where_pointer=raw_row["pointer"] + "/where",
            raw_text={"issue": finding.get("issue", ""), "where": finding.get("where", ""), "reason": finding.get("reason", ""), "basis": finding.get("basis")},
            observed_source_fact_status=fact_status,
            normative_violation_status=normative,
            defect_claim_status=claim_status,
            d_tier=final.d_tier,
            a0_type=a0_type,
            validity=validity,
            corrected_kni=kni,
            relations=relation_rows,
            full_ledger_ids=tuple(x.expected_id for x in relation_rows if x.relation == Relation.FULL_MATCH),
            partial_ledger_ids=tuple(x.expected_id for x in relation_rows if x.relation == Relation.PARTIAL_MATCH),
            no_match_ledger_ids=tuple(x.expected_id for x in relation_rows if x.relation == Relation.NO_MATCH),
            witness=witness,
            source_loci=final.source_loci,
            reason=final.reason,
            basis=final.basis,
            source_refs=final.source_refs,
            original_category=final.original_category,
            reclassification_from=final.original_category,
            reclassification_to=kni,
            reclassified_from_non_k=True,
            reclassification_reason=f"{report_id}: migration is derived from the frozen pre-v3 scope category {final.original_category} and the pane5 source-backed D/A plus dense relation closure; no historical semantic label supplies the new result.",
            canonical_group_key=final.canonical_group_key if kni != "K" else None,
            review=final.review,
            scoring=True,
            diagnostic_only=False,
        )
        decisions.append(decision)
        dense.extend({
            "side": "x1v2_baseline",
            "pair_id": final.pair_id,
            "round": final.round,
            "report_id": report_id,
            "expected_id": relation.expected_id,
            "relation": relation.relation.value,
            "reason": relation.reason,
            "basis": relation.basis,
            "source_refs": [x.model_dump(mode="json") for x in relation.source_refs],
            "report_owned_field_refs": list(relation.report_owned_field_refs),
        } for relation in relation_rows)

    envelope = DecisionSetV3(
        side="x1v2_baseline",
        raw_non_k_count=len(decisions),
        decisions=tuple(decisions),
        input_inventory_sha256=sha(v3 / "inventory.json"),
        frozen_k_snapshot_sha256=snapshot["snapshot_projection_sha256"],
        reviewer_coverage="233/233 final rows are explicit pane5 register rows with two retained independent proposal opinions, source-read evidence digests, and human confirmation.",
        generated_by="rebuild_baseline_v3_from_pane5_register.py@v3.1",
    )
    rows = [x.model_dump(mode="json") for x in envelope.decisions]
    (v3 / "baseline_report_decisions_v3.json").write_text(json.dumps(envelope.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (v3 / "baseline_relation_decisions_v3.json").write_text(json.dumps({"schema": "paper1.manual-adjudication.v3-baseline-ni.relations", "rows": dense}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_tsv(v3 / "baseline_report_decisions_v3.tsv", rows)
    print(json.dumps({"status": "PASS", "decisions": len(decisions), "relations": len(dense), "d_tiers": dict(Counter(x.d_tier.value for x in decisions)), "kni": dict(Counter(x.corrected_kni for x in decisions))}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
