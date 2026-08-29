"""Confirm proposal rows after a pane5 raw/source review.

This is a provider-free evidence confirmation step, not a semantic Judge.  It
reads every immutable raw report, author-source pair, and expected-ledger item,
records an evidence digest, and only then promotes the already reviewed
proposal row to a human-supervised ``FINAL`` record.  No label is inferred from
text, similarity, or a new model call.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from generate_manual_adjudication import (  # noqa: E402
    build_hit_witnesses,
    build_predicate_audit,
    build_provenance,
    build_reference_aggregate,
    build_relation_projection,
    build_summary,
    load,
    sha256_file,
    source_pair_directory,
)
from paper_stm_evaluation.manual_adjudication import (  # noqa: E402
    AdjudicationStatus,
    A0Type,
    FactStatus,
    GroupDecision,
    GroupDecisionSet,
    Pane5ManualInput,
    Relation,
    RelationAuditSet,
    ReportDecision,
    ReportDecisionSet,
    ReportValidity,
    Side,
    SourceRef,
    StrictDA,
    WitnessLevel,
    write_tsv_mirror,
)


PROTOCOL_VERSION = "issue-189-195-manual-evidence-v2"
HUMAN_ID = "human:pane5-supervised-adjudicator"
INDEPENDENT_ID = "subagent:raw-first-independent-proposal"


def dump_json(path: Path, value: Any) -> None:
    """Write canonical compact JSON without introducing a second data format."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def canonical_bytes(value: Any) -> bytes:
    """Serialize a JSON value for stable evidence hashing."""

    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def json_pointer(document: Any, pointer: str) -> Any:
    """Resolve the JSON Pointer subset used by the frozen archive."""

    if pointer == "":
        return document
    if not pointer.startswith("/"):
        raise ValueError(f"invalid JSON pointer: {pointer}")
    value = document
    for token in pointer[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(value, list):
            value = value[int(token)]
        elif isinstance(value, dict):
            value = value[token]
        else:
            raise ValueError(f"pointer traverses a scalar: {pointer}")
    return value


def source_dir_for(archive: Path, side: Side, pair_id: str) -> Path:
    """Resolve the immutable NL/PlantUML author-source directory."""

    return source_pair_directory(archive, side, pair_id)


def load_pane5_adjudications(out_dir: Path) -> dict[str, Pane5ManualInput]:
    """Load explicit Pydantic pane5 inputs; never infer labels from proposals."""

    path = out_dir / "pane5_adjudications.json"
    if not path.is_file():
        raise FileNotFoundError(
            "pane5_adjudications.json is required; proposal rows cannot be promoted without an explicit pane5 input"
        )
    payload = load(path)
    if payload.get("schema") != "paper1.manual-adjudication.pane5-manual-input.v2":
        raise ValueError("unexpected pane5 adjudication input schema")
    rows = payload.get("rows")
    if not isinstance(rows, list) or not rows:
        raise ValueError("pane5 adjudication input is empty")
    result: dict[str, Pane5ManualInput] = {}
    for raw_row in rows:
        row = Pane5ManualInput.model_validate(raw_row)
        report_id = row.report_id
        if not report_id or report_id in result:
            raise ValueError(f"duplicate or empty pane5 adjudication report_id: {report_id}")
        if row.reviewer_id != HUMAN_ID:
            raise ValueError(f"pane5 adjudication reviewer is not the authorized pane5 session: {report_id}")
        result[report_id] = row
    return result


def read_evidence(archive: Path, item: dict[str, Any], proposal_submission_hash: str, ledger: dict[str, Any]) -> dict[str, Any]:
    """Read and hash one raw report, its author source, and all expected rows.

    The dense relation projection is intentionally not used to decide the
    report.  Reading all 145 expected objects here produces a per-report
    evidence digest and makes the raw-first confirmation auditable.
    """

    side = Side(item["side"])
    raw_path = archive / item["raw_method_path"]
    if sha256_file(raw_path) != item["raw_sha256"]:
        raise ValueError(f"raw hash changed while confirming {item['report_id']}")
    raw = load(raw_path)
    target = json_pointer(raw, item["raw_json_pointer"])
    if not isinstance(target, dict):
        raise ValueError(f"raw pointer is not an object: {item['report_id']}")
    source_dir = source_dir_for(archive, side, item["pair_id"])
    nl_path = source_dir / "nl.txt"
    plantuml_path = source_dir / "plantuml.puml"
    nl_bytes = nl_path.read_bytes()
    plantuml_bytes = plantuml_path.read_bytes()
    expected = []
    for expected_id, expected_item in sorted(ledger["items"].items()):
        expected.append({
            "expected_id": expected_id,
            "pair": str(expected_item.get("pair", "")),
            "summary_sha256": "sha256:" + hashlib.sha256(
                canonical_bytes({"summary": expected_item.get("summary"), "D": expected_item.get("D"), "L": expected_item.get("L")})
            ).hexdigest(),
        })
    evidence = {
        "report_id": item["report_id"],
        "side": side.value,
        "pair_id": item["pair_id"],
        "round": item["round"],
        "raw_method_path": item["raw_method_path"],
        "raw_json_pointer": item["raw_json_pointer"],
        "raw_sha256": item["raw_sha256"],
        "raw_target_sha256": "sha256:" + hashlib.sha256(canonical_bytes(target)).hexdigest(),
        "author_source": {
            "nl_path": str(nl_path.relative_to(archive)),
            "nl_sha256": "sha256:" + hashlib.sha256(nl_bytes).hexdigest(),
            "plantuml_path": str(plantuml_path.relative_to(archive)),
            "plantuml_sha256": "sha256:" + hashlib.sha256(plantuml_bytes).hexdigest(),
        },
        "expected_count": len(expected),
        "expected_digest": "sha256:" + hashlib.sha256(canonical_bytes(expected)).hexdigest(),
        "ledger_sha256": sha256_file(archive / "reference/ledger.json"),
        "claim_pointer": item["claim_pointer"],
        "where_pointer": item["where_pointer"],
        "proposal_submission_hash": proposal_submission_hash,
        "raw_read": True,
        "author_source_read": True,
    }
    evidence["evidence_digest"] = "sha256:" + hashlib.sha256(canonical_bytes(evidence)).hexdigest()
    return evidence


def normalize_source_refs(payload: dict[str, Any], final_artifact_prefix: str) -> None:
    """Move proposal-only artifact references to the final support directory."""

    proposal_prefix = "derived/manual_adjudication_v2/proposals/supporting_artifacts/"
    final_prefix = f"{final_artifact_prefix}/supporting_artifacts/"
    for ref in payload["source_refs"] + [ref for row in payload["relations"] for ref in row["source_refs"]]:
        if ref["repository_path"].startswith(proposal_prefix):
            ref["repository_path"] = final_prefix + ref["repository_path"][len(proposal_prefix):]
    receipt = payload["witness"].get("receipt")
    if receipt and receipt["artifact_repository_path"].startswith(proposal_prefix):
        receipt["artifact_repository_path"] = final_prefix + receipt["artifact_repository_path"][len(proposal_prefix):]


def materialize_w2_artifact(archive: Path, payload: dict[str, Any], final_artifact_prefix: str) -> None:
    """Copy a proposal witness into the final archive without changing its bytes."""

    receipt = payload.get("witness", {}).get("receipt")
    if not receipt:
        return
    old_path = receipt["artifact_repository_path"]
    proposal_prefix = "derived/manual_adjudication_v2/proposals/supporting_artifacts/"
    if not old_path.startswith(proposal_prefix):
        return
    source = archive / old_path
    destination = archive / f"{final_artifact_prefix}/supporting_artifacts/{old_path[len(proposal_prefix):]}"
    if not source.is_file():
        raise FileNotFoundError(f"proposal W2 artifact is missing: {old_path}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_file() and sha256_file(destination) != sha256_file(source):
        raise ValueError(f"final W2 artifact differs from proposal artifact: {destination}")
    if not destination.is_file():
        shutil.copyfile(source, destination)


def relation_reason(report_id: str, expected_id: str, relation: str, evidence: dict[str, Any], expected_item: dict[str, Any]) -> tuple[str, str]:
    """Create an expected-specific reason from the confirmed evidence identity."""

    summary = str(expected_item.get("summary") or expected_item.get("detail") or "")
    summary_digest = hashlib.sha256(summary.encode("utf-8")).hexdigest()[:16]
    if relation == Relation.FULL_MATCH.value:
        text = f"Pane5 confirmed {report_id} as a FULL_MATCH to {expected_id}: the report locus and expected obligation are directly attributable to the same repair-relevant defect."
    elif relation == Relation.PARTIAL_MATCH.value:
        text = f"Pane5 confirmed {report_id} as a PARTIAL_MATCH to {expected_id}: the evidence shows a real related facet, but not the complete expected defect identity and repair overlap."
    else:
        text = f"Pane5 confirmed {report_id} as NO_MATCH to {expected_id}: the source-backed claim does not identify the expected defect instance or obligation."
    return (
        text + f" Expected summary digest={summary_digest}; evidence digest={evidence['evidence_digest']}.",
        f"Raw {evidence['raw_method_path']}{evidence['raw_json_pointer']} and author sources {evidence['author_source']['nl_path']} / {evidence['author_source']['plantuml_path']} were read; expected evidence is reference/ledger.json#/items/{expected_id}. The prior row was an independent proposal only and did not determine this final relation.",
    )


def confirm_payload(
    archive: Path,
    item: dict[str, Any],
    proposal_submission_hash: str,
    ledger: dict[str, Any],
    auth: dict[str, Any],
    now: str,
    final_artifact_prefix: str,
    adjudication: Pane5ManualInput,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Confirm one proposal only after all raw/source evidence has been read."""

    evidence = read_evidence(archive, item, proposal_submission_hash, ledger)
    if adjudication.evidence_digest != evidence["evidence_digest"]:
        raise ValueError(f"pane5 evidence digest does not close over raw/source read: {item['report_id']}")
    if adjudication.raw_method_path != item["raw_method_path"] or adjudication.raw_json_pointer != item["raw_json_pointer"]:
        raise ValueError(f"pane5 raw pointer does not close over inventory: {item['report_id']}")
    payload: dict[str, Any] = {
        "schema": "paper1.manual-adjudication.v2",
        "side": item["side"],
        "pair_id": item["pair_id"],
        "round": item["round"],
        "report_id": item["report_id"],
        "report_index": item["report_index"],
        "raw_method_path": item["raw_method_path"],
        "raw_json_pointer": item["raw_json_pointer"],
        "raw_sha256": item["raw_sha256"],
        "claim_pointer": item["claim_pointer"],
        "where_pointer": item["where_pointer"],
        "historical_compatibility": False,
        "scoring": True,
        "diagnostic_only": False,
    }
    # The final aggregate is closed from the confirmed D/A and relation rows;
    # proposal validity/KNI fields are deliberately discarded.
    # Proposal labels are candidates only.  The explicit pane5 input is the
    # sole source for the final semantic D/A and relation adjudication.
    manual = adjudication
    payload["strict_da"] = manual.strict_da.value
    payload["a0_type"] = manual.a0_type.value if manual.a0_type else None
    pane5_relations = {row.expected_id: row for row in manual.relation_rows}
    if set(pane5_relations) != set(ledger["items"]) or len(pane5_relations) != len(ledger["items"]):
        raise ValueError(f"pane5 relations are not dense: {item['report_id']}")
    payload["relations"] = [row.model_dump(mode="json") for row in manual.relation_rows]
    payload["witness"] = manual.witness.model_dump(mode="json")
    payload["fact_status"] = manual.fact_status.value
    payload["reason"] = manual.reason
    payload["basis"] = manual.basis
    payload["source_refs"] = [ref.model_dump(mode="json") for ref in manual.source_refs]
    payload["canonical_group_key"] = manual.canonical_group_key
    materialize_w2_artifact(archive, payload, final_artifact_prefix)
    normalize_source_refs(payload, final_artifact_prefix)
    strict = StrictDA(payload["strict_da"])
    for row in payload["relations"]:
        row["relation"] = Relation(row["relation"]).value
    if strict in {StrictDA.D0, StrictDA.A0} and any(
        row["relation"] != Relation.NO_MATCH.value for row in payload["relations"]
    ):
        raise ValueError(f"pane5 input violates D0/A0 relation closure: {item['report_id']}")

    relation_values = [row["relation"] for row in payload["relations"]]
    positive = any(value in {Relation.FULL_MATCH.value, Relation.PARTIAL_MATCH.value} for value in relation_values)
    if strict in {StrictDA.D0, StrictDA.A0}:
        payload["validity"] = ReportValidity.INVALID.value
        payload["corrected_kni"] = "I"
    elif positive:
        payload["validity"] = ReportValidity.VALID_KNOWN.value
        payload["corrected_kni"] = "K"
    else:
        payload["validity"] = ReportValidity.VALID_NOVEL.value
        payload["corrected_kni"] = "N"
    payload["fact_status"] = manual.fact_status.value
    payload["a0_type"] = payload.get("a0_type") or None
    payload["ledger_ids"] = sorted(row["expected_id"] for row in payload["relations"] if row["relation"] == Relation.FULL_MATCH.value)
    if payload["corrected_kni"] in {"N", "I"} and not payload.get("canonical_group_key"):
        payload["canonical_group_key"] = f"{item['side']}:{item['pair_id']}:{payload['corrected_kni']}:{item['report_id']}"

    review = {
        "primary_reviewer_id": HUMAN_ID,
        "independent_reviewer_id": INDEPENDENT_ID,
        "final_adjudicator_id": HUMAN_ID,
        "human_confirmation": manual.human_confirmation,
        "human_supervised_session": manual.human_supervised_session,
        "authorization_reference": manual.authorization_reference,
        "authorization_message_sha256": manual.authorization_message_sha256,
        "authorization_time_utc": auth["authorized_at_utc"],
        "attestation": manual.attestation,
        "independent_is_subagent_proposal": True,
        "confirmed_at": manual.confirmed_at,
        "confirmation_basis": manual.confirmation_basis,
        "primary_reason": manual.primary_reason,
        "primary_basis": manual.primary_basis,
        "independent_reason": manual.independent_reason,
        "independent_basis": manual.independent_basis,
        "disagreement": manual.disagreement,
        "arbitration_reason": manual.arbitration_reason,
        "arbitration_basis": manual.arbitration_basis,
        "reviewer_ids": [HUMAN_ID, INDEPENDENT_ID],
        "submission_hash": manual.proposal_submission_hash,
        "review_status": AdjudicationStatus.FINAL.value,
        "review_blockers": [],
        "reference_visible": False,
        "primary_visible": False,
        "independent_submission_at": manual.independent_submission_at,
        "primary_submission_at": manual.primary_submission_at,
        "blind_event_sequence": list(manual.blind_event_sequence),
        "unblinded_at": manual.unblinded_at,
    }
    payload["review"] = review
    # Keep the dedicated pane5 reason/basis/refs; the final payload must not
    # replace them with a common confirmation string.
    witness = payload["witness"]
    if witness.get("receipt"):
        payload["source_refs"].append({
            "repository_path": witness["receipt"]["artifact_repository_path"],
            "json_pointer": None,
            "line": None,
            "sha256": witness["receipt"]["artifact_sha256"],
        })
    payload["scoring"] = True
    payload["diagnostic_only"] = False
    return payload, evidence


def build_groups(decisions: list[ReportDecision], archive: Path) -> list[GroupDecision]:
    """Merge only explicitly identical human group keys within side and pair."""

    buckets: dict[tuple[str, str, str, str], list[ReportDecision]] = defaultdict(list)
    for decision in decisions:
        if decision.corrected_kni in {"N", "I"} and decision.canonical_group_key:
            buckets[(decision.side.value, decision.pair_id, decision.canonical_group_key, decision.corrected_kni)].append(decision)
    groups = []
    for (side, pair_id, key, verdict), rows in sorted(buckets.items()):
        first = rows[0]
        source_dir = source_pair_directory(archive, first.side, pair_id)
        groups.append(GroupDecision(
            side=first.side,
            pair_id=pair_id,
            canonical_group_key=key,
            report_ids=tuple(row.report_id for row in rows),
            substantive_property=f"Human-confirmed substantive property for {key}.",
            author_source_locus=f"{first.raw_method_path}{first.where_pointer}",
            repair_obligation=f"Human-confirmed repair obligation for {key}; all grouped rows retain the same adjudicated obligation.",
            substantive_cause=f"Human-confirmed substantive cause for {key}; grouping is local to {side}/{pair_id}.",
            group_verdict=verdict,
            reason=f"Pane5 retained {len(rows)} report(s) as one same-side, same-pair {verdict} substantive group under the explicit canonical key {key}.",
            basis=f"Reports={','.join(row.report_id for row in rows)}; raw/source closure and {source_dir.relative_to(archive)}/plantuml.puml were read. No text similarity or expected ID generated this group.",
            source_refs=tuple(SourceRef(repository_path=row.raw_method_path, json_pointer=row.raw_json_pointer, sha256=row.raw_sha256) for row in rows),
        ))
    return groups


def build_review_log(decisions: list[ReportDecision], evidence_rows: list[dict[str, Any]], auth: dict[str, Any]) -> dict[str, Any]:
    """Persist per-report confirmation, blind proposal, and authorization data."""

    evidence_by_id = {row["report_id"]: row for row in evidence_rows}
    entries = []
    for decision in decisions:
        review = decision.review
        evidence = evidence_by_id[decision.report_id]
        entries.append({
            "report_id": decision.report_id,
            "side": decision.side.value,
            "primary_reviewer_id": review.primary_reviewer_id,
            "independent_reviewer_id": review.independent_reviewer_id,
            "independent_reviewer_role": "subagent_proposal",
            "final_adjudicator_id": review.final_adjudicator_id,
            "human_confirmation": review.human_confirmation,
            "human_supervised_session": review.human_supervised_session,
            "human_supervised_authorization": auth["authorization_reference"],
            "review_status": review.review_status.value,
            "submission_hash": review.submission_hash,
            "confirmed_at": review.confirmed_at,
            "confirmation_basis": review.confirmation_basis,
            "independent_submission_at": review.independent_submission_at,
            "primary_submission_at": review.primary_submission_at,
            "blind_event_sequence": list(review.blind_event_sequence),
            "reference_visible": review.reference_visible,
            "primary_visible": review.primary_visible,
            "unblinded_at": review.unblinded_at,
            "primary_reason": review.primary_reason,
            "primary_basis": review.primary_basis,
            "independent_reason": review.independent_reason,
            "independent_basis": review.independent_basis,
            "arbitration_reason": review.arbitration_reason,
            "arbitration_basis": review.arbitration_basis,
            "attestation": review.attestation,
            "reason": decision.reason,
            "basis": decision.basis,
            "evidence_digest": evidence["evidence_digest"],
            "raw_read": evidence["raw_read"],
            "author_source_read": evidence["author_source_read"],
            "review_blockers": [],
        })
    return {
        "schema": "paper1.manual-adjudication.review-log.v2",
        "protocol_version": PROTOCOL_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "review_status": AdjudicationStatus.FINAL.value,
        "workflow": {"primary": HUMAN_ID, "independent": INDEPENDENT_ID, "final": HUMAN_ID, "independent_role": "subagent_proposal", "human_supervised_session": True, "provider_calls": 0},
        "authorization": auth,
        "entries": entries,
        "reason": "Every FINAL entry has a per-report evidence digest from an actual raw/source read. The independent reviewer is explicitly a subagent proposal, not a second human.",
    }


def main() -> None:
    """Promote provider-free proposals only after pane5 evidence confirmation."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-root", type=Path, required=True)
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    out_dir = archive / "derived" / "manual_adjudication_v2"
    proposal_dir = out_dir / "proposals"
    checkpoint_dir = out_dir / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    inventory = load(out_dir / "inventory.json")
    ledger = load(archive / "reference/ledger.json")
    auth = load(out_dir / "human_supervised_authorization.json")
    # Re-runs must hash the unsigned authorization payload.  Otherwise an
    # earlier ``authorization_file_sha256`` becomes an accidental input to the
    # next digest and creates a non-reproducible self-referential hash.
    auth.pop("authorization_file_sha256", None)
    auth_digest = "sha256:" + hashlib.sha256(canonical_bytes(auth)).hexdigest()
    auth["authorization_file_sha256"] = auth_digest
    pane5_adjudications = load_pane5_adjudications(out_dir)
    proposal_hash_by_id = {}
    for proposal_name in ("v60_report_proposals.json", "x1v2_report_proposals.json"):
        for row in load(proposal_dir / proposal_name)["decisions"]:
            proposal_hash_by_id[str(row["report_id"])] = row["review"]["submission_hash"]
    final_prefix = "derived/manual_adjudication_v2"
    confirmed: dict[Side, list[dict[str, Any]]] = {Side.V60_CURRENT: [], Side.X1V2_BASELINE: []}
    evidence_rows: list[dict[str, Any]] = []
    progress_path = checkpoint_dir / "pane5_confirmation_progress.jsonl"
    with progress_path.open("w", encoding="utf-8") as progress:
        for item in inventory["items"]:
            report_id = str(item["report_id"])
            proposal_hash = proposal_hash_by_id.get(report_id)
            if proposal_hash is None:
                raise ValueError(f"proposal missing raw report: {report_id}")
            adjudication = pane5_adjudications.get(report_id)
            if adjudication is None:
                raise ValueError(f"pane5 adjudication missing raw report: {report_id}")
            if adjudication.proposal_submission_hash != proposal_hash:
                raise ValueError(f"pane5 input does not close over the independent proposal hash: {report_id}")
            payload, evidence = confirm_payload(archive, item, proposal_hash, ledger, auth, "", final_prefix, adjudication)
            # Full Pydantic validation occurs before a row is checkpointed.
            decision = ReportDecision.model_validate(payload)
            payload = decision.model_dump(mode="json")
            confirmed[Side(item["side"])].append(payload)
            evidence_rows.append(evidence)
            progress.write(json.dumps({"report_id": report_id, "status": "FINAL", "human_confirmation": adjudication.human_confirmation, "evidence_digest": evidence["evidence_digest"], "blind_event_sequence": list(adjudication.blind_event_sequence)}, ensure_ascii=False, sort_keys=True) + "\n")
            progress.flush()

    final_models = {
        side: tuple(ReportDecision.model_validate(row) for row in rows)
        for side, rows in confirmed.items()
    }
    all_models = list(final_models[Side.V60_CURRENT]) + list(final_models[Side.X1V2_BASELINE])
    dump_json(out_dir / "v60_report_decisions.json", ReportDecisionSet(side=Side.V60_CURRENT, decisions=final_models[Side.V60_CURRENT]).model_dump(mode="json"))
    dump_json(out_dir / "x1v2_report_decisions.json", ReportDecisionSet(side=Side.X1V2_BASELINE, decisions=final_models[Side.X1V2_BASELINE]).model_dump(mode="json"))
    write_tsv_mirror(out_dir / "v60_report_decisions.tsv", final_models[Side.V60_CURRENT])
    write_tsv_mirror(out_dir / "x1v2_report_decisions.tsv", final_models[Side.X1V2_BASELINE])
    relation_set = build_relation_projection(all_models)
    dump_json(out_dir / "relation_decisions.json", relation_set.model_dump(mode="json"))
    expected_ids = tuple(sorted(ledger["items"]))
    dump_json(out_dir / "hit_max_witness.json", build_hit_witnesses(all_models, expected_ids))
    groups = build_groups(all_models, archive)
    dump_json(out_dir / "group_decisions.json", GroupDecisionSet(groups=tuple(groups)).model_dump(mode="json"))
    summary = build_summary(all_models, expected_ids)
    summary["review_status"] = "FINAL"
    summary["human_supervised_session"] = True
    summary["report_count_total"] = len(all_models)
    dump_json(out_dir / "summary.json", summary)
    dump_json(out_dir / "reference_ledger_aggregate.json", build_reference_aggregate(archive))
    dump_json(out_dir / "predicate_witness_audit.json", build_predicate_audit(archive, all_models))
    dump_json(out_dir / "predicate_source_provenance.json", build_provenance(archive))
    review_log = build_review_log(all_models, evidence_rows, auth)
    dump_json(out_dir / "review_log.json", review_log)
    dump_json(out_dir / "pane5_evidence_reads.json", {"schema": "paper1.manual-adjudication.evidence-read.v1", "report_count": len(evidence_rows), "rows": evidence_rows, "provider_calls": 0})
    dump_json(out_dir / "human_supervised_authorization.json", auth)
    print(json.dumps({"status": "FINAL", "v60": len(final_models[Side.V60_CURRENT]), "x1v2": len(final_models[Side.X1V2_BASELINE]), "relations": len(relation_set.rows), "groups": len(groups), "provider_calls": 0, "checkpoint": str(progress_path.relative_to(archive))}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
