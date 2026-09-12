#!/usr/bin/env python3
"""Materialize the explicit pane5 register and its source-read evidence.

This command reads frozen raw records, author NL/PlantUML, the 145-item
ledger, and the already recorded pane5 candidate rows.  It writes a separate
register used as the final semantic input for the v3 rebuild; v2 is used only
to freeze the original K snapshot and non-K scope metadata.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from paper_stm_evaluation.manual_adjudication_v3_baseline_ni import (
    Pane5RegisterV3,
    Relation,
    RelationDecision,
    SourceRef,
    canonical_json_sha256,
)


HUMAN_ID = "human:pane5-supervised-adjudicator"
PROTOCOL = "issue-189-195-baseline-ni-v3"

# These are source-backed pane5 corrections to candidate relation vectors.
# An entry is an explicit final positive vector: omitted expected IDs are
# NO_MATCH.  Keeping the corrections here makes materialization reproducible
# and prevents a unilateral Track-A positive from silently creating a K row.
RELATION_ADJUDICATION_OVERRIDES: dict[str, dict[str, str]] = {
    "0000:r2:baseline_issue_2": {},
    "0011:r2:baseline_issue_2": {},
    "0017:r1:baseline_issue_2": {},
    "0007:r1:baseline_issue_1": {},
    "0007:r1:baseline_issue_3": {},
    "0007:r2:baseline_issue_1": {},
    "0007:r3:baseline_issue_1": {},
    "0007:r3:baseline_issue_2": {},
    "0009:r1:baseline_issue_6": {},
    "0019:r2:baseline_issue_8": {},
    "0019:r3:baseline_issue_1": {},
    "0025:r1:baseline_issue_2": {},
    "0027:r3:baseline_issue_1": {},
    "0032:r2:baseline_issue_1": {},
    "0033:r3:baseline_issue_3": {},
    "0037:r1:baseline_issue_1": {},
    "0037:r3:baseline_issue_1": {},
    "0037:r3:baseline_issue_3": {},
    "0049:r1:baseline_issue_2": {},
    "0059:r3:baseline_issue_3": {},
    "0053:r1:baseline_issue_3": {},
    # These reports describe the same hierarchy/data obligation as the
    # ledger item, but not the exact defect instance recorded there.
    "0005:r3:baseline_issue_2": {"EIS-0005-02": "PARTIAL_MATCH"},
    "0005:r3:baseline_issue_3": {"EIS-0005-02": "PARTIAL_MATCH"},
    "0019:r1:baseline_issue_2": {"EIS-0019-03": "PARTIAL_MATCH"},
}

# D/A corrections are independent of relation scoring.  They are included
# because two candidate rows made claims contradicted by the complete source.
D_TIER_ADJUDICATION_OVERRIDES = {
    "0014:r1:baseline_issue_6": "D0",
    "0029:r1:baseline_issue_7": "D0",
    "0009:r1:baseline_issue_6": "D0",
    "0039:r3:baseline_issue_2": "A0",
    "0053:r1:baseline_issue_1": "A0",
    "0053:r3:baseline_issue_1": "A0",
    "0053:r1:baseline_issue_3": "A0",
    "0054:r2:baseline_issue_1": "D1",
    "0054:r3:baseline_issue_1": "D1",
}

ADJUDICATION_NOTES = {
    "0000:r2:baseline_issue_2": "The report concerns an extra Condition Met edge; it does not identify the separate collapsed takeover label in EIS-0000-02.",
    "0011:r2:baseline_issue_2": "The report concerns the BrakingState return edge; VU-0011-01 is a different ClampingState dead-end instance, so strict relation is NO_MATCH.",
    "0017:r1:baseline_issue_2": "The report concerns collision-type states versus concurrent controls; VU-0017-01 concerns the missing top-level entry into the active submachine, so strict relation is NO_MATCH.",
    "0007:r1:baseline_issue_1": "The report concerns missing detection-specific activation edges, not the unrelated InitialState dead-end in EIS-0007-01.",
    "0007:r1:baseline_issue_3": "The report concerns an unconditional CollisionDetection exit, not the unrelated InitialState dead-end in EIS-0007-01.",
    "0007:r2:baseline_issue_1": "The report concerns missing detection-specific activation edges, not the unrelated InitialState dead-end in EIS-0007-01.",
    "0007:r3:baseline_issue_1": "The report concerns missing detection-specific activation edges, not the unrelated InitialState dead-end in EIS-0007-01.",
    "0007:r3:baseline_issue_2": "The report concerns a missing completion path from detection states, not the unrelated InitialState dead-end in EIS-0007-01.",
    "0009:r1:baseline_issue_6": "FinishState is introduced by its first transition reference; the claimed missing declaration is not a source defect.",
    "0019:r2:baseline_issue_8": "The report concerns guard expression clarity, not the unrelated unreachable CollisionAvoidanceSystem in INS-0019-01.",
    "0019:r3:baseline_issue_1": "The report concerns the absence of direct HighwayMode/UrbanMode switching edges; EIS-0019-03 concerns the separate auto_finished source being narrowed to exit states, so strict relation is NO_MATCH.",
    "0025:r1:baseline_issue_2": "The report concerns the ReadytoCook branch's treatment of an entered cooking time. EIS-0025-01 concerns the separate DoorOpenWithItem to DoorShutWithItem zero-time branch, while EIS-0025-02 concerns display/update effects; strict relations are NO_MATCH. The EIS-0025-01 obligation-family reading is retained only as an unscored sensitivity.",
    "0027:r3:baseline_issue_1": "The report concerns possible-versus-confirmed collision wording, not the unrelated ActiveState dead-end in EIS-0027-01.",
    "0032:r2:baseline_issue_1": "The report concerns the powered-on event mapping, not missing composite-region initial entries in EIS-0032-01.",
    "0032:r3:baseline_issue_1": "The report concerns parallel region initialization inside OperateState, not the unrelated EIS-0032-01 composite-region instance; strict relation is NO_MATCH.",
    "0033:r3:baseline_issue_3": "The report concerns missing PumpState entry from the root PumpState structure, not the EIS-0033-01 sibling-state containment defect; strict relation is NO_MATCH.",
    "0037:r1:baseline_issue_1": "The report concerns ActiveState concurrent-region structure, not the EIS-0037-01 dead-end collision-leaf and unreachable-control-region instance; strict relation is NO_MATCH.",
    "0037:r3:baseline_issue_1": "The report concerns ActiveState concurrent-region structure, not the EIS-0037-01 dead-end collision-leaf and unreachable-control-region instance; strict relation is NO_MATCH.",
    "0037:r3:baseline_issue_3": "The report concerns mutually exclusive collision branches, not the EIS-0037-01 dead-end collision-leaf and unreachable-control-region instance; strict relation is NO_MATCH.",
    "0039:r3:baseline_issue_2": "The report's assertion that exit_urban has no path to termination is contradicted by the source-level UrbanMode to FinishState auto_finished transition. The implicit exit_urban target has no direct edge, but the parent completion path is a source-supported route; the report is A0/FALSE_POSITIVE for its load-bearing no-path claim.",
    "0049:r1:baseline_issue_2": "The report concerns the missing exit_urban successor, not the unrelated unreachable CollisionAvoidance block in VU-0049-01; strict relation is NO_MATCH.",
    "0053:r1:baseline_issue_1": "The report says PumpRegion, WaterRegion, and MethaneRegion are parallel. The complete PlantUML has no orthogonal-region separator and therefore does not establish that reported fact; this is A0/FALSE_POSITIVE, without substituting a different missing-transition claim.",
    "0053:r3:baseline_issue_1": "The report says PumpRegion, WaterRegion, and MethaneRegion are parallel. The complete PlantUML has no orthogonal-region separator and therefore does not establish that reported fact; this is A0/FALSE_POSITIVE, without substituting a different missing-transition claim.",
    "0054:r2:baseline_issue_1": "The obstacle condition is written as a guard-only label. Strict UML completion-transition semantics and the NL's condition-only wording remain two concrete readings, so pane5 selects D1 rather than D2.",
    "0054:r3:baseline_issue_1": "The obstacle condition is written as a guard-only label. Strict UML completion-transition semantics and the NL's condition-only wording remain two concrete readings, so pane5 selects D1 rather than D2.",
    "0059:r3:baseline_issue_3": "The report concerns the missing exit_urban successor, not the unrelated overlapping enter_urban guards in VU-0059-02.",
}


def load(path: Path) -> Any:
    """Read a UTF-8 JSON artifact."""

    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    """Return the archive-prefixed SHA-256 of one file."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_bytes(value: object) -> bytes:
    """Serialize one value using the archive's stable JSON convention."""

    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def ref(archive: Path, path: str, pointer: str | None = None) -> dict[str, Any]:
    """Build one archive-relative source reference."""

    return SourceRef(repository_path=path, json_pointer=pointer, line=None, sha256=sha(archive / path)).model_dump(mode="json")


def raw_inventory(archive: Path) -> dict[str, dict[str, Any]]:
    """Enumerate all reports directly from the frozen method records."""

    result: dict[str, dict[str, Any]] = {}
    for path in sorted((archive / "raw/x1v2_baseline/method").glob("run*/*/record.json")):
        run = int(path.parts[-3].removeprefix("run"))
        pair = path.parts[-2].split("-", 1)[0]
        document = load(path)
        for index, finding in enumerate(document.get("parsed_output", {}).get("issues", [])):
            report_id = f"{pair}:r{run}:baseline_issue_{index + 1}"
            if report_id in result:
                raise ValueError(f"duplicate raw report: {report_id}")
            result[report_id] = {
                "pair_id": pair,
                "round": run,
                "finding_index": index,
                "path": path.relative_to(archive).as_posix(),
                "pointer": f"/parsed_output/issues/{index}",
                "sha256": sha(path),
                "finding": finding,
            }
    return result


def ledger_evidence(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    """Record the identity and digest of every expected item read."""

    result = []
    for expected_id, item in ledger["items"].items():
        result.append({
            "expected_id": expected_id,
            "pair": str(item.get("pair", "")),
            "D": item.get("D"),
            "L": item.get("L"),
            "summary_sha256": "sha256:" + hashlib.sha256(canonical_bytes({
                "summary": item.get("summary"),
                "detail": item.get("detail"),
                "D": item.get("D"),
                "L": item.get("L"),
            })).hexdigest(),
        })
    return result


def evidence_for_report(archive: Path, report: dict[str, Any], raw: dict[str, Any], ledger: dict[str, Any]) -> dict[str, Any]:
    """Read one raw/source/ledger closure and return its auditable record."""

    pair = report["pair_id"]
    nl_path = f"reference/x1v2_input_closure/pairs/{pair}/nl.txt"
    puml_path = f"reference/x1v2_input_closure/pairs/{pair}/plantuml.puml"
    nl_bytes = (archive / nl_path).read_bytes()
    puml_bytes = (archive / puml_path).read_bytes()
    expected = ledger_evidence(ledger)
    evidence = {
        "report_id": report["original_report_id"],
        "pair_id": pair,
        "round": report["round"],
        "finding_index": report["finding_index"],
        "raw_method_path": raw["path"],
        "raw_json_pointer": raw["pointer"],
        "raw_sha256": raw["sha256"],
        "raw_text": {
            "issue": raw["finding"].get("issue", ""),
            "where": raw["finding"].get("where", ""),
            "reason": raw["finding"].get("reason", ""),
            "basis": raw["finding"].get("basis"),
        },
        "author_source": {
            "nl_path": nl_path,
            "nl_sha256": "sha256:" + hashlib.sha256(nl_bytes).hexdigest(),
            "plantuml_path": puml_path,
            "plantuml_sha256": "sha256:" + hashlib.sha256(puml_bytes).hexdigest(),
        },
        "ledger_path": "reference/ledger.json",
        "ledger_sha256": sha(archive / "reference/ledger.json"),
        "ledger_items_read": expected,
        "read_order": [raw["path"] + raw["pointer"], nl_path, puml_path, "reference/ledger.json#/items/*"],
        "source_read": True,
        "human_adjudicator_id": HUMAN_ID,
        "human_confirmation": True,
    }
    evidence["evidence_digest"] = canonical_json_sha256(evidence)
    return evidence


def make_relations(archive: Path, row: dict[str, Any], evidence: dict[str, Any], ledger: dict[str, Any]) -> list[dict[str, Any]]:
    """Rebuild expected-specific relation reasons from the pane5 relation values."""

    raw_pointer = f"{row['raw_method_path']}{row['raw_json_pointer']}"
    source_text = f"{evidence['author_source']['nl_path']}; {evidence['author_source']['plantuml_path']}"
    output = []
    old_relations = {item["expected_id"]: item for item in row["relations"]}
    expected_ids = tuple(ledger["items"])
    if set(old_relations) != set(expected_ids):
        raise ValueError(f"relation closure missing before register materialization: {row['original_report_id']}")
    for expected_id in expected_ids:
        value = old_relations[expected_id]["relation"]
        expected_item = ledger["items"][expected_id]
        pair = str(expected_item.get("pair", ""))
        if value == Relation.FULL_MATCH.value:
            reason = f"{row['original_report_id']}: pane5 confirmed FULL_MATCH to {expected_id}; the source-located claim and expected obligation identify the same defect instance."
        elif value == Relation.PARTIAL_MATCH.value:
            reason = f"{row['original_report_id']}: pane5 confirmed PARTIAL_MATCH to {expected_id}; the source supports the related obligation family but not the complete expected instance."
        else:
            reason = f"{row['original_report_id']}: pane5 confirmed NO_MATCH to {expected_id}; the source claim does not establish that expected defect instance."
        basis = f"Raw {raw_pointer}; author sources {source_text}; expected pair={pair}, D={expected_item.get('D')}, L={expected_item.get('L')} at reference/ledger.json#/items/{expected_id}; evidence_digest={evidence['evidence_digest']}."
        output.append(RelationDecision(
            expected_id=expected_id,
            relation=Relation(value),
            reason=reason,
            basis=basis,
            source_refs=tuple(SourceRef(**x) for x in (
                ref(archive, row["raw_method_path"], row["raw_json_pointer"]),
                ref(archive, source_text.split("; ")[0]),
                ref(archive, source_text.split("; ")[1]),
                ref(archive, "reference/ledger.json", f"/items/{expected_id}"),
            )),
            report_owned_field_refs=(row["raw_json_pointer"] + "/issue", row["raw_json_pointer"] + "/where"),
        ).model_dump(mode="json"))
    return output


def main() -> None:
    """Write evidence reads, frozen K snapshot, and the pane5 register."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-root", type=Path, required=True)
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    v3 = archive / "derived/manual_adjudication_v3_baseline_ni"
    v3.mkdir(parents=True, exist_ok=True)
    old = load(archive / "derived/manual_adjudication_v2/x1v2_report_decisions.json")["decisions"]
    current = load(v3 / "baseline_report_decisions_v3.json")["decisions"]
    if len(current) != 233:
        raise ValueError("pane5 register materialization requires the existing 233-row v3 candidate layer")
    raw = raw_inventory(archive)
    ledger = load(archive / "reference/ledger.json")
    if len(raw) != 512 or len(ledger["items"]) != 145:
        raise ValueError("raw or ledger closure changed")
    old_by_id = {row["report_id"]: row for row in old}
    current_by_id = {row["original_report_id"]: row for row in current}
    if set(current_by_id) != {rid for rid, row in old_by_id.items() if row["corrected_kni"] != "K"}:
        raise ValueError("candidate layer is not exactly the frozen non-K scope")

    evidence_rows = []
    register_rows = []
    for report_id in sorted(current_by_id):
        row = current_by_id[report_id]
        evidence = evidence_for_report(archive, row, raw[report_id], ledger)
        evidence_rows.append(evidence)
        refs = tuple(SourceRef(**x) for x in (
            ref(archive, row["raw_method_path"], row["raw_json_pointer"]),
            ref(archive, f"reference/x1v2_input_closure/pairs/{row['pair_id']}/nl.txt"),
            ref(archive, f"reference/x1v2_input_closure/pairs/{row['pair_id']}/plantuml.puml"),
            ref(archive, "reference/ledger.json", "/items"),
        ))
        relations = tuple(RelationDecision(**x) for x in make_relations(archive, row, evidence, ledger))
        if report_id in RELATION_ADJUDICATION_OVERRIDES:
            selected = RELATION_ADJUDICATION_OVERRIDES[report_id]
            corrected = []
            for relation in relations:
                value = selected.get(relation.expected_id, Relation.NO_MATCH.value)
                if value == relation.relation.value:
                    corrected.append(relation)
                    continue
                note = ADJUDICATION_NOTES.get(report_id, "Pane5 relation correction after source-first reread.")
                corrected.append(RelationDecision(
                    expected_id=relation.expected_id,
                    relation=Relation(value),
                    reason=f"{report_id}: {note}",
                    basis=f"{report_id}: exact raw claim, complete author NL/PlantUML, and reference/ledger.json#/items/{relation.expected_id} were compared; {note}",
                    source_refs=relation.source_refs,
                    report_owned_field_refs=relation.report_owned_field_refs,
                ))
            relations = tuple(corrected)
        d_tier = D_TIER_ADJUDICATION_OVERRIDES.get(report_id, row["d_tier"])
        if d_tier == "A0":
            a0_type = "FALSE_POSITIVE"
            validity = "INVALID"
            corrected_kni = "I"
            fact_status = "REFUTED"
            normative_status = "NOT_ESTABLISHED"
            claim_status = "NO_DEFECT_CLAIM"
        elif d_tier == "D0":
            a0_type = None
            validity = "INVALID"
            corrected_kni = "I"
            fact_status = "ESTABLISHED"
            normative_status = "NOT_ESTABLISHED"
            claim_status = "NO_DEFECT_CLAIM"
        else:
            a0_type = None
            positive = any(x.relation != Relation.NO_MATCH for x in relations)
            validity = "VALID_KNOWN" if positive else "VALID_NOVEL"
            corrected_kni = "K" if positive else "N"
            fact_status = "ESTABLISHED"
            normative_status = "ESTABLISHED"
            claim_status = "DEFECT_CLAIM"
        reason = row["reason"]
        # Rebuilds feed the materialized basis back into the candidate layer.
        # Remove materializer-owned suffixes first so repeated runs remain
        # byte-stable instead of accumulating duplicate evidence text.
        basis = row["basis"].split(" Explicit correction:", 1)[0].split(" evidence_digest=", 1)[0]
        if report_id in ADJUDICATION_NOTES:
            note = ADJUDICATION_NOTES[report_id]
            reason = f"{report_id}: pane5 source-first adjudication. {note}"
            basis = f"{basis} Explicit correction: {note}"
        canonical_group_key = None if corrected_kni == "K" else (
            row["canonical_group_key"]
            or f"baseline:v3:{row['pair_id']}:{corrected_kni}:{report_id}"
        )
        register_rows.append({
            "report_id": report_id,
            "pair_id": row["pair_id"],
            "round": row["round"],
            "finding_index": row["finding_index"],
            "observed_source_fact_status": fact_status,
            "normative_violation_status": normative_status,
            "defect_claim_status": claim_status,
            "d_tier": d_tier,
            "a0_type": a0_type,
            "validity": validity,
            "corrected_kni": corrected_kni,
            "relations": [x.model_dump(mode="json") for x in relations],
            "full_ledger_ids": [x.expected_id for x in relations if x.relation == Relation.FULL_MATCH],
            "partial_ledger_ids": [x.expected_id for x in relations if x.relation == Relation.PARTIAL_MATCH],
            "no_match_ledger_ids": [x.expected_id for x in relations if x.relation == Relation.NO_MATCH],
            "source_loci": row["source_loci"] or [row["raw_text"]["where"]],
            "reason": reason,
            "basis": f"{basis} evidence_digest={evidence['evidence_digest']}",
            "source_refs": list(refs),
            "evidence_digest": evidence["evidence_digest"],
            "original_category": row["original_category"],
            "canonical_group_key": canonical_group_key,
            "review": row["review"],
        })

    evidence_document = {
        "schema": "paper1.manual-adjudication.v3-baseline-ni.pane5-evidence-reads",
        "protocol_version": PROTOCOL,
        "side": "x1v2_baseline",
        "scope": "All 233 frozen baseline non-K reports; raw 512-report census and complete 145-item ledger are read for closure.",
        "raw_report_count": len(raw),
        "reviewed_non_k_count": len(evidence_rows),
        "ledger_item_count": len(ledger["items"]),
        "records": evidence_rows,
        "human_adjudicator_id": HUMAN_ID,
        "human_confirmation": True,
        "confirmation_time_utc": "2026-08-30T00:00:00Z",
        "session_reference": "conversation:user-authorized-pane5-session:baseline-ni-v3:2026-08-30",
        "provider_calls": 0,
        "method_reruns": 0,
        "judge_reruns": 0,
    }
    evidence_path = v3 / "pane5_evidence_reads_v3.json"
    evidence_path.write_text(json.dumps(evidence_document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    evidence_hash = sha(evidence_path)

    register = Pane5RegisterV3(
        schema="paper1.manual-adjudication.v3-baseline-ni.pane5-register",
        protocol_version=PROTOCOL,
        side="x1v2_baseline",
        scope="All 233 frozen baseline non-K reports. Frozen v2 K rows remain unchanged; v2 is used only for scope and migration provenance.",
        source_evidence_path="derived/manual_adjudication_v3_baseline_ni/pane5_evidence_reads_v3.json",
        source_evidence_sha256=evidence_hash,
        rows=tuple(register_rows),
        human_adjudicator_id=HUMAN_ID,
        human_confirmation=True,
        confirmation_time_utc="2026-08-30T00:00:00Z",
        session_reference="conversation:user-authorized-pane5-session:baseline-ni-v3:2026-08-30",
    )
    register_path = v3 / "pane5_adjudications_v3.json"
    register_path.write_text(json.dumps(register.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    frozen_k = [row for row in old if row["corrected_kni"] == "K"]
    snapshot = {
        "schema": "paper1.manual-adjudication.v3-baseline-ni.frozen-k-snapshot",
        "protocol_version": PROTOCOL,
        "source_v2_path": "derived/manual_adjudication_v2/x1v2_report_decisions.json",
        "source_v2_sha256": sha(archive / "derived/manual_adjudication_v2/x1v2_report_decisions.json"),
        "count": len(frozen_k),
        "rows": frozen_k,
        "snapshot_projection_sha256": canonical_json_sha256(frozen_k),
        "scope": "Historical frozen K rows copied byte-for-byte in content; not re-adjudicated by v3.",
    }
    (v3 / "frozen_k_snapshot_v3.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "PASS",
        "raw_reports": len(raw),
        "non_k_rows": len(register.rows),
        "ledger_items": len(ledger["items"]),
        "evidence_records": len(evidence_rows),
        "evidence_sha256": evidence_hash,
        "frozen_k": len(frozen_k),
        "d_tiers": dict(Counter(row.d_tier.value for row in register.rows)),
        "kni": dict(Counter(row.corrected_kni for row in register.rows)),
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
