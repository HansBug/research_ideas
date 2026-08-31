"""Build and validate canonical predicate-gold pilot annotations for pair 0000."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from paper_stm_evaluation.predicate_gold import (
    ANNOTATION_BATCH_SCHEMA_VERSION,
    CandidateProperty,
    Confidence,
    ExactnessRelation,
    ExecutableProperty,
    ExecutionRecord,
    ExecutionState,
    GoldMode,
    GoldStatus,
    PositiveControl,
    PositiveControlStatus,
    PredicateGoldAnnotation,
    PredicateGoldAnnotationBatch,
    PropertyComposition,
    ReviewOpinion,
    ReviewTrack,
    SourceRef,
    canonical_sha256,
    sha256_path,
    write_json,
)
from paper_stm_evaluation.predicate_gold_review import (
    Pane5ArbitrationBatch,
    PreExecutionDisposition,
    TrackAProposalBatch,
    TrackBProposalBatch,
    TrackCReviewBatch,
)


def _ref(repo_root: Path, path: Path, *, pointer: str | None = None, element: str | None = None) -> SourceRef:
    """Build one stable source reference for a canonical execution record."""

    return SourceRef(
        repository_path=path.resolve().relative_to(repo_root.resolve()).as_posix(),
        sha256=sha256_path(path),
        json_pointer=pointer,
        line_start=None,
        line_end=None,
        model_element=element,
        excerpt=None,
    )


def _review_opinion_a(batch: TrackAProposalBatch, row: Any) -> ReviewOpinion:
    """Project one blind obligation proposal into the canonical opinion contract."""

    unsigned = {
        "opinion_id": f"{batch.reviewer_id}:{row.ledger_id}",
        "reviewer_id": batch.reviewer_id,
        "track": ReviewTrack.A_OBLIGATION,
        "input_sha256": canonical_sha256({"input_manifest": batch.input_manifest_sha256, "row": row.proposal_sha256}),
        "normalized_obligation_sha256": canonical_sha256(row.normalized_obligation.model_dump(mode="json")),
        "property_proposal_sha256": None,
        "proposed_status": None,
        "proposed_exactness_relation": None,
        "proposed_predicate_ids": [],
        "reason": row.reason,
        "basis": row.basis,
        "source_refs": [item.model_dump(mode="json") for item in row.source_refs],
        "other_tracks_visible": False,
        "v60_actual_visible": False,
        "confidence": row.confidence,
        "reviewed_at": row.reviewed_at,
    }
    return ReviewOpinion(**unsigned, opinion_sha256=canonical_sha256(unsigned))


def _b_proposed_status(disposition: PreExecutionDisposition) -> GoldStatus:
    """Map a pre-result execution proposal to the corresponding conditional final status."""

    return {
        PreExecutionDisposition.EXACT_EXECUTION_CANDIDATE: GoldStatus.EXACT_FALSE,
        PreExecutionDisposition.COMPOSITE_EXACT_EXECUTION_CANDIDATE: GoldStatus.COMPOSITE_EXACT_FALSE,
        PreExecutionDisposition.PROXY_EXECUTION_CANDIDATE: GoldStatus.SOUND_FALSE_PROXY,
        PreExecutionDisposition.UNSUPPORTED_EXACT_CANDIDATE: GoldStatus.UNSUPPORTED_EXACT,
    }[disposition]


def _review_opinion_b(batch: TrackBProposalBatch, row: Any) -> ReviewOpinion:
    """Project one blind pre-execution property proposal into canonical review evidence."""

    selected = next((candidate for candidate in row.candidate_properties if candidate.candidate_id == row.selected_candidate_id), None)
    unsigned = {
        "opinion_id": f"{batch.reviewer_id}:{row.ledger_id}",
        "reviewer_id": batch.reviewer_id,
        "track": ReviewTrack.B_PROPERTY,
        "input_sha256": canonical_sha256(
            {
                "input_manifest": batch.input_manifest_sha256,
                "capability_audit": batch.capability_audit_sha256,
                "row": row.proposal_sha256,
            }
        ),
        "normalized_obligation_sha256": canonical_sha256(row.normalized_obligation.model_dump(mode="json")),
        "property_proposal_sha256": row.proposal_sha256,
        "proposed_status": _b_proposed_status(row.proposed_disposition),
        "proposed_exactness_relation": row.proposed_exactness_relation,
        "proposed_predicate_ids": list(selected.predicate_ids) if selected else [],
        "reason": row.reason,
        "basis": row.basis,
        "source_refs": [item.model_dump(mode="json") for item in row.source_refs],
        "other_tracks_visible": False,
        "v60_actual_visible": False,
        "confidence": row.confidence,
        "reviewed_at": row.reviewed_at,
    }
    return ReviewOpinion(**unsigned, opinion_sha256=canonical_sha256(unsigned))


def _review_opinion_c(batch: TrackCReviewBatch, row: Any) -> ReviewOpinion:
    """Project one post-proposal execution review into canonical review evidence."""

    unsigned = {
        "opinion_id": f"{batch.reviewer_id}:{row.ledger_id}",
        "reviewer_id": batch.reviewer_id,
        "track": ReviewTrack.C_EXECUTION,
        "input_sha256": row.input_packet_sha256,
        "normalized_obligation_sha256": row.normalized_obligation_sha256,
        "property_proposal_sha256": row.property_proposal_sha256,
        "proposed_status": row.proposed_status,
        "proposed_exactness_relation": row.proposed_exactness_relation,
        "proposed_predicate_ids": [],
        "reason": row.reason,
        "basis": row.basis,
        "source_refs": [item.model_dump(mode="json") for item in row.source_refs],
        "other_tracks_visible": True,
        "v60_actual_visible": False,
        "confidence": row.confidence,
        "reviewed_at": row.reviewed_at,
    }
    return ReviewOpinion(**unsigned, opinion_sha256=canonical_sha256(unsigned))


def _candidate_projection(row: Any, final_relation: ExactnessRelation) -> tuple[CandidateProperty, ...]:
    """Retain Track B candidates while applying pane5's relation correction to its selected P."""

    projected: list[CandidateProperty] = []
    for candidate in row.candidate_properties:
        if candidate.candidate_id != row.selected_candidate_id or final_relation == candidate.exactness_relation:
            projected.append(candidate)
            continue
        projected.append(
            candidate.model_copy(
                update={
                    "exactness_relation": final_relation,
                    "selected": False,
                    "semantic_gaps": (
                        *candidate.semantic_gaps,
                        "Pane5 adopted Track C's implication analysis: this representation constraint is not entailed by O and does not establish O.",
                    ),
                    "reason": candidate.reason
                    + " Pane5 rejected the proposed implication after Track C showed that O permits other encodings and P omits required execution semantics.",
                }
            )
        )
    return tuple(projected)


def _receipt_refs(repo_root: Path, root: Path, receipt: dict[str, Any], *, include_replay: bool) -> tuple[SourceRef, ...]:
    """Reference the parent, every constituent, and optional replay audit."""

    refs = [_ref(repo_root, root / "receipt.json", element="composite parent receipt")]
    refs.extend(
        _ref(repo_root, root / item["receipt_path"], element=item["request_id"])
        for item in receipt["constituents"]
    )
    if include_replay:
        refs.append(_ref(repo_root, root / "replay" / "replay_audit.json", element="composite replay audit"))
    return tuple(refs)


def _execution(repo_root: Path, gold_root: Path, root: Path, receipt: dict[str, Any]) -> ExecutionRecord:
    """Build a final completed-false execution record from saved composite bytes."""

    query_path = root / "query.json"
    code = next(item for item in receipt["code_hashes"] if item["role"] == "composite_runner")
    return ExecutionRecord(
        state=ExecutionState.COMPLETED_BOOLEAN,
        verdict=False,
        query_path=query_path.relative_to(gold_root).as_posix(),
        query_sha256=sha256_path(query_path),
        command=tuple(receipt["command"]),
        backend_id="evaluation-only-non-short-circuit-frozen-predicate-composite",
        backend_version=receipt["source_commit"],
        backend_code_sha256=code["sha256"],
        artifact_sha256=receipt["artifact_sha256"],
        domain=None,
        bound=None,
        seed=None,
        started_at=receipt["started_at"],
        completed_at=receipt["completed_at"],
        receipt_refs=_receipt_refs(repo_root, root, receipt, include_replay=True),
        counterexample_refs=tuple(
            _ref(
                repo_root,
                root / item["receipt_path"].replace("receipt.json", "raw_receipt.json"),
                pointer="/counterexample",
                element=item["request_id"],
            )
            for item in receipt["constituents"]
            if item["verdict"] is False
        ),
        replay_status="REPLAY_MATCH",
        reason="The parent and all four constituents completed; the saved provider-free replay matched state, Boolean and semantic projection for every constituent.",
    )


def _positive_control(repo_root: Path, control_root: Path, provenance: Path, receipt: dict[str, Any]) -> PositiveControl:
    """Build the terminal-true minimal-repair control record."""

    refs = (*_receipt_refs(repo_root, control_root, receipt, include_replay=True), _ref(repo_root, provenance, element="minimal repair provenance"))
    return PositiveControl(
        status=PositiveControlStatus.COMPLETED_TRUE,
        control_kind="precommitted minimal repair of both root initial-carrier event attachments",
        artifact_path=receipt["artifact_path"],
        artifact_sha256=receipt["artifact_sha256"],
        verdict=True,
        receipt_refs=refs,
        contamination_check="PASS: control bytes and provenance were frozen before same-issue defective execution; Track C checked the byte-level diff and v60 actual output remained hidden.",
        vacuity_check="PASS: both root initial carriers remain present and all four trigger/guard constituents execute; the true result is not caused by an empty carrier inventory.",
        reason="The control removes only the two forbidden initial-carrier event attachments, preserves both carriers and guards, completes true on all constituents, and replays identically.",
    )


def main() -> int:
    """Build the three schema-valid pilot canonical rows after arbitration."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--created-at", required=True)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    paper_root = repo_root / "project_1_llm_state_machine_modeling" / "paper_stm_issue_discover"
    gold_root = paper_root / "discover_matrix" / "ledger_v2" / "predicate_gold_v1"
    inventory = json.loads((gold_root / "inventory.json").read_text(encoding="utf-8"))
    ledger = json.loads((paper_root / "discover_matrix/ledger_v2/ledger.json").read_text(encoding="utf-8"))
    pair = next(item for item in inventory["pairs"] if item["pair_id"] == "0000")
    a_batch = TrackAProposalBatch.model_validate_json((gold_root / "review/pilot_independent/track_a_pair_0000.json").read_text(encoding="utf-8"))
    b_batch = TrackBProposalBatch.model_validate_json((gold_root / "review/pilot_independent/track_b_pair_0000.json").read_text(encoding="utf-8"))
    c_batch = TrackCReviewBatch.model_validate_json((gold_root / "review/track_c_independent/pilot_pair_0000.json").read_text(encoding="utf-8"))
    arbitration_batch = Pane5ArbitrationBatch.model_validate_json((gold_root / "review/arbitration/pilot_pair_0000.json").read_text(encoding="utf-8"))
    a_rows = {row.ledger_id: row for row in a_batch.rows}
    b_rows = {row.ledger_id: row for row in b_batch.rows}
    c_rows = {row.ledger_id: row for row in c_batch.rows}
    arbitrations = {row.ledger_id: row for row in arbitration_batch.rows}
    rows: list[PredicateGoldAnnotation] = []

    for ledger_id in sorted(a_rows):
        a_row = a_rows[ledger_id]
        b_row = b_rows[ledger_id]
        c_row = c_rows[ledger_id]
        arbitration_row = arbitrations[ledger_id]
        arbitration = arbitration_row.arbitration
        candidates = _candidate_projection(b_row, arbitration.final_exactness_relation)
        opinions = (
            _review_opinion_a(a_batch, a_row),
            _review_opinion_b(b_batch, b_row),
            _review_opinion_c(c_batch, c_row),
        )
        exact = ledger_id == "INS-0000-04"
        selected = next((candidate for candidate in candidates if candidate.candidate_id == b_row.selected_candidate_id), None)
        if exact and selected is None:
            raise ValueError("exact pilot row lost its selected Track B candidate")

        gold_property = None
        execution = None
        positive_control = None
        false_refs: tuple[SourceRef, ...] = ()
        counterexample_refs: tuple[SourceRef, ...] = ()
        predicate_ids: tuple[str, ...] = ()
        if exact and selected is not None:
            request_path = gold_root / "receipts/INS-0000-04/defective/request.json"
            request = json.loads(request_path.read_text(encoding="utf-8"))
            defect_root = request_path.parent
            control_root = gold_root / "receipts/INS-0000-04/positive_control"
            defect_receipt = json.loads((defect_root / "receipt.json").read_text(encoding="utf-8"))
            control_receipt = json.loads((control_root / "receipt.json").read_text(encoding="utf-8"))
            composition = PropertyComposition(
                operator="AND",
                constituent_ids=tuple(item["request_id"] for item in request["constituents"]),
                truth_definition="Evaluate all four S3/S5 constituents; the parent is true iff every constituent is true. No constituent is skipped after a false result.",
                no_short_circuit=True,
            )
            gold_property = ExecutableProperty(
                property_id=selected.candidate_id,
                mode=GoldMode.COMPOSITE,
                predicate_ids=selected.predicate_ids,
                expression=selected.property_expression,
                typed_inputs=selected.typed_inputs,
                assumptions=selected.assumptions,
                semantic_scope=a_row.normalized_obligation.semantic_scope,
                timing=a_row.normalized_obligation.timing,
                rtc_semantics=a_row.normalized_obligation.rtc_semantics,
                composition=composition,
                proposal_sha256=b_row.proposal_sha256,
            )
            execution = _execution(repo_root, gold_root, defect_root, defect_receipt)
            positive_control = _positive_control(
                repo_root,
                control_root,
                gold_root / "controls/INS-0000-04/control_provenance.json",
                control_receipt,
            )
            false_refs = execution.receipt_refs
            counterexample_refs = execution.counterexample_refs
            predicate_ids = selected.predicate_ids

        unsupported = not exact
        capability_gap = ()
        unsupported_reason = None
        if ledger_id == "EIS-0000-01":
            capability_gap = (
                "No trusted current oracle quantifies every reachable running configuration, dispatches Power_Off under guard/priority semantics, and observes whole-machine terminated() in the required RTC.",
                "The executed source-static direct-root-carrier property is representation-specific and UNRELATED to O after independent implication review.",
            )
            unsupported_reason = arbitration.reason
        elif ledger_id == "EIS-0000-02":
            capability_gap = (
                "The source leaves the takeover connective unresolved and supplies no canonical event identities or co-occurrence semantics.",
                "The executed source-static oracle invents exact tokens and a three-route encoding and does not check guard feasibility, event dispatch or RTC response.",
            )
            unsupported_reason = arbitration.reason

        annotation = PredicateGoldAnnotation(
            ledger_id=ledger_id,
            pair_id="0000",
            family=ledger_id.split("-")[0],
            ledger_sha256=inventory["ledger_sha256"],
            nl_path=pair["nl_path"],
            nl_sha256=pair["nl_sha256"],
            artifact_path=pair["fcstm_path"],
            artifact_sha256=pair["fcstm_sha256"],
            author_source_path=pair["plantuml_path"],
            author_source_sha256=pair["plantuml_sha256"],
            d_tier=ledger["items"][ledger_id]["D"],
            l_tier=ledger["items"][ledger_id]["L"],
            normalized_obligation=a_row.normalized_obligation,
            obligation_source_refs=a_row.normalized_obligation.source_refs,
            alternative_readings=a_row.alternative_readings,
            candidate_properties=candidates,
            rejected_candidate_ids=tuple(
                candidate.candidate_id for candidate in candidates if not exact or candidate.candidate_id != b_row.selected_candidate_id
            ),
            exactness_relation=arbitration.final_exactness_relation,
            gold_status=arbitration.final_status,
            gold_mode=GoldMode.COMPOSITE if exact else GoldMode.UNSUPPORTED,
            gold_property=gold_property,
            predicate_ids=predicate_ids,
            execution=execution,
            false_receipt_refs=false_refs,
            counterexample_refs=counterexample_refs,
            positive_control=positive_control,
            proxy_property=None,
            proxy_execution=None,
            unsupported_reason=unsupported_reason,
            capability_gap=capability_gap,
            reason=arbitration.reason,
            basis=arbitration.basis,
            review_opinions=opinions,
            reviewer_ids=tuple(opinion.reviewer_id for opinion in opinions),
            conflicts=arbitration_row.conflicts,
            arbitration=arbitration,
            confidence=Confidence.HIGH if exact else Confidence.MEDIUM,
            created_at=args.created_at,
        )
        if unsupported != (annotation.gold_status == GoldStatus.UNSUPPORTED_EXACT):
            raise ValueError("pilot unsupported status mismatch")
        rows.append(annotation)

    unsigned = {
        "schema_version": ANNOTATION_BATCH_SCHEMA_VERSION,
        "batch_id": "pilot_pair_0000",
        "pair_ids": ["0000"],
        "rows": [row.model_dump(mode="json") for row in rows],
        "created_at": args.created_at,
    }
    batch = PredicateGoldAnnotationBatch(**unsigned, batch_sha256=canonical_sha256(unsigned))
    output = gold_root / "canonical_batches" / "pilot_pair_0000.json"
    write_json(output, batch.model_dump(mode="json"))
    PredicateGoldAnnotationBatch.model_validate_json(output.read_text(encoding="utf-8"))
    print(f"wrote {output} ({len(batch.rows)} rows, {batch.batch_sha256})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
